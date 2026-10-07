import contextlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("wiki_ingest", ROOT / "tools" / "ingest.py")
ingest = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ingest)


class IngestTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = self.root / "raw" / "sources"
        self.sources.mkdir(parents=True)
        self.body = self.root / "body.json"
        self.body.write_text(json.dumps({
            "title": "Source title", "content": "# Source\n\nKept content.",
            "author": "Original author", "publishedTime": "2025-01-02T12:00:00Z",
        }))

    def run_ingest(self, *args):
        with patch.object(ingest, "__file__", str(self.root / "tools" / "ingest.py")), \
             patch.object(sys, "argv", ["ingest.py", *args]), \
             contextlib.redirect_stdout(io.StringIO()), \
             contextlib.redirect_stderr(io.StringIO()):
            ingest.main()

    def test_stable_name_keeps_dates_in_header(self):
        self.run_ingest("https://example.com/shared-memory", "--file", str(self.body))
        self.assertEqual([p.name for p in self.sources.iterdir()], ["shared-memory.md"])
        text = (self.sources / "shared-memory.md").read_text()
        self.assertIn("published: 2025-01-02", text)
        self.assertIn("fetched: " + ingest.date.today().isoformat(), text)
        self.assertIn("Kept content.", text)

    def test_prefetched_body_skips_fetch_for_every_source_type(self):
        cases = [
            ("https://github.com/example/Brain/tree/main/docs", "repo"),
            ("https://youtube.com/watch?v=abc_DEF", "video"),
            ("https://x.com/example/status/12345", "tweet"),
            ("https://example.com/docs", "blog"),
        ]
        with patch.object(ingest, "urlopen", side_effect=AssertionError("unexpected network")), \
             patch.object(ingest, "fetch_youtube_transcript", side_effect=AssertionError("unexpected download")):
            for url, kind in cases:
                self.run_ingest(url, "--name", kind, "--file", str(self.body))
                text = (self.sources / f"{kind}.md").read_text()
                self.assertIn(f"type: {kind}", text)
                self.assertIn("Kept content.", text)

    def test_direct_fetch_paths_share_stable_names(self):
        with patch.object(ingest, "fetch", return_value="<title>T</title><article><p>Page</p></article>"), \
             patch.object(ingest, "analyze_github_repo", return_value="# Repository"), \
             patch.object(ingest, "fetch_youtube_transcript", return_value=("Transcript", "Video")), \
             patch.object(ingest, "fetch_x_thread", return_value="Thread"):
            for url in [
                "https://example.com/an_article.html", "https://github.com/owner/Brain",
                "https://youtube.com/watch?v=abc_DEF", "https://x.com/author/status/12345",
            ]:
                self.run_ingest(url)
        self.assertEqual({p.name for p in self.sources.iterdir()},
                         {"an-article.md", "brain.md", "abc-def.md", "12345.md"})

    def test_existing_and_legacy_files_are_preserved(self):
        for filename in ["memory.md", "2025-01-02-memory.md"]:
            with self.subTest(filename=filename):
                path = self.sources / filename
                path.write_text("Keep original")
                with self.assertRaises(SystemExit), patch.object(ingest, "fetch", side_effect=AssertionError("unexpected fetch")):
                    self.run_ingest("https://example.com/memory")
                self.assertEqual(path.read_text(), "Keep original")
                self.assertEqual(list(self.sources.iterdir()), [path])
                path.unlink()

    def test_save_rejects_file_created_after_path_check(self):
        path = ingest.source_path(self.sources, "memory")
        path.write_text("Concurrent writer")
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            ingest.save_source(path, "Overwrite")
        self.assertEqual(path.read_text(), "Concurrent writer")

    def test_name_rejects_paths_and_non_kebab_case(self):
        for name in ["../outside", "a/b", "Upper", "with_space", "memory.md", ""]:
            with self.subTest(name=name), self.assertRaises(SystemExit):
                self.run_ingest("https://example.com/", "--name", name, "--file", str(self.body))
        self.assertEqual(list(self.sources.iterdir()), [])

    def test_cli_passes_name_and_metadata_as_literal_arguments(self):
        shutil.copytree(ROOT / "bin", self.root / "bin")
        (self.root / "tools").mkdir()
        shutil.copy(ROOT / "tools" / "ingest.py", self.root / "tools" / "ingest.py")
        shutil.copy(ROOT / "package.json", self.root / "package.json")
        author = "Reader $(touch unexpected-marker) `touch another-marker`"
        result = subprocess.run([
            str(self.root / "bin" / "wiki"), "ingest", "https://github.com/example/brain",
            "--name", "shared-brain", "--file", str(self.body), "--author", author,
            "--published", "2024-03-04",
        ], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.sources / "shared-brain.md").read_text()
        self.assertIn("author: " + author, text)
        self.assertIn("published: 2024-03-04", text)
        self.assertFalse((self.root / "unexpected-marker").exists())
        self.assertFalse((self.root / "another-marker").exists())


if __name__ == "__main__":
    unittest.main()
