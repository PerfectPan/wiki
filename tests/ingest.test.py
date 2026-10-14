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

CAPTURE = {
    "meta": {
        "bvid": "BV1Myez6LEKc",
        "cid": 42055370907,
        "title": "Local-first 同步引擎还缺什么",
        "owner": {"name": "六十四条悟"},
        "duration": 1521,
    },
    "data": {
        "dash": {
            "audio": [{"baseUrl": "https://example.com/audio", "bandwidth": 90671}],
            "video": [
                {"baseUrl": "https://example.com/video", "height": 480, "bandwidth": 90000, "codecs": "avc1.64001F"}
            ],
        }
    },
}


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
        page = "<title>T</title><article><p>" + "Page body text. " * 12 + "</p></article>"
        with patch.object(ingest, "fetch", return_value=page), \
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

    def test_short_direct_fetch_is_rejected(self):
        # 风控页和 JS 空壳会被解成几乎空的 Markdown；以前会写一个空文件并报「已保存」。
        with patch.object(ingest, "fetch", return_value="<title>T</title><article><p>Page</p></article>"):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                self.run_ingest("https://example.com/blocked")
        self.assertEqual(list(self.sources.iterdir()), [])

    def test_bilibili_video_uses_ytdlp_and_local_transcript(self):
        info = {"bvid": "BV1Myez6LEKc", "title": "Local-first 同步引擎还缺什么",
                "owner": "六十四条悟", "duration": 1521, "source": "yt-dlp", "subtitles": []}
        cues = [ingest.video.Cue(0.0, 2.0, "先讲目录怎么同步"), ingest.video.Cue(2.0, 4.0, "再看正文")]

        def fake_fetch(url, out_dir, **kwargs):
            out_dir.mkdir(parents=True, exist_ok=True)
            media = out_dir / ("audio.m4a" if kwargs.get("kind", "audio") == "audio" else "video.mp4")
            media.write_bytes(b"media")
            return media

        def fake_sheets(video_path, out_dir, **kwargs):
            out_dir.mkdir(parents=True, exist_ok=True)
            sheet = out_dir / "sheet-1.png"
            sheet.write_bytes(b"png")
            return [sheet]

        with patch.object(ingest.video, "resolve_streams", return_value=info), \
             patch.object(ingest.video, "fetch_subtitles", return_value=None), \
             patch.object(ingest.video, "fetch_media", side_effect=fake_fetch), \
             patch.object(ingest.video, "transcribe_with_repair", return_value=(cues, {"repairs": []})), \
             patch.object(ingest.video, "contact_sheets", side_effect=fake_sheets):
            self.run_ingest(
                "https://www.bilibili.com/video/BV1Myez6LEKc/",
                "--name", "bili-talk", "--slides",
            )
        text = (self.sources / "bili-talk.md").read_text()
        self.assertIn("type: video", text)
        self.assertIn("# Local-first 同步引擎还缺什么", text)
        self.assertIn("文字来自本地转录", text)
        self.assertIn("**[00:00]**", text)
        self.assertIn("先讲目录怎么同步", text)
        self.assertIn("raw/assets/bili-talk-slides-1.png", text)
        self.assertEqual(
            (self.root / "raw" / "assets" / "bili-talk-slides-1.png").read_bytes(), b"png"
        )

    def test_bilibili_prefers_official_subtitles(self):
        info = {"bvid": "BV1Myez6LEKc", "title": "有字幕的视频", "owner": "up主",
                "duration": 600, "source": "yt-dlp", "subtitles": ["zh-Hans"]}
        cues = [ingest.video.Cue(0.0, 3.0, "这一段来自官方字幕")]
        with patch.object(ingest.video, "resolve_streams", return_value=info), \
             patch.object(ingest.video, "fetch_subtitles", return_value=(cues, "zh-Hans")), \
             patch.object(ingest.video, "fetch_media", side_effect=AssertionError("字幕优先时不应下载媒体")), \
             patch.object(ingest.video, "transcribe_with_repair", side_effect=AssertionError("有字幕时不应转录")):
            self.run_ingest("https://www.bilibili.com/video/BV1Myez6LEKc/", "--name", "bili-subs")
        text = (self.sources / "bili-subs.md").read_text()
        self.assertIn("文字来自官方字幕（zh-Hans）", text)
        self.assertIn("这一段来自官方字幕", text)
        self.assertNotIn("机器转录", text)

    def test_bilibili_capture_path_downloads_streams(self):
        capture = self.root / "capture.json"
        capture.write_text(json.dumps(CAPTURE), encoding="utf-8")
        cues = [ingest.video.Cue(0.0, 1.0, "capture 路径")]
        with patch.object(ingest.video, "fetch_subtitles", side_effect=AssertionError("capture 路径不应试 yt-dlp 字幕")), \
             patch.object(ingest.video, "download", side_effect=lambda url, path, **kw: (path.parent.mkdir(parents=True, exist_ok=True), path.write_bytes(b"media"), path)[-1]), \
             patch.object(ingest.video, "transcribe_with_repair", return_value=(cues, {"repairs": []})):
            self.run_ingest(
                "https://www.bilibili.com/video/BV1Myez6LEKc/",
                "--name", "bili-capture", "--capture", str(capture),
            )
        text = (self.sources / "bili-capture.md").read_text()
        self.assertIn("capture 路径", text)

    def test_bilibili_blocked_direct_access_points_at_capture(self):
        blocked = ingest.video.FetchBlocked("yt-dlp 失败", needs_browser=True)
        with patch.object(ingest.video, "resolve_streams", side_effect=blocked), \
             patch.object(ingest, "die", side_effect=SystemExit) as die_mock:
            with self.assertRaises(SystemExit):
                self.run_ingest("https://www.bilibili.com/video/BV1Myez6LEKc/")
        self.assertEqual(list(self.sources.iterdir()), [])
        self.assertIn("--capture", die_mock.call_args.args[0])

    def test_bilibili_argument_errors_skip_the_browser_hint(self):
        broken = ingest.video.FetchBlocked("找不到 capture 文件：/nope.json")
        with patch.object(ingest.video, "resolve_streams", side_effect=broken), \
             patch.object(ingest, "die", side_effect=SystemExit) as die_mock:
            with self.assertRaises(SystemExit):
                self.run_ingest("https://www.bilibili.com/video/BV1Myez6LEKc/", "--capture", "/nope.json")
        self.assertNotIn("browser", die_mock.call_args.args[0])
        self.assertIn("找不到 capture 文件", die_mock.call_args.args[0])

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
        shutil.copy(ROOT / "tools" / "video.py", self.root / "tools" / "video.py")
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
