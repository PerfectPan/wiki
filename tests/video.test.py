import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("wiki_video", ROOT / "tools" / "video.py")
video = importlib.util.module_from_spec(spec)
sys.modules["wiki_video"] = video
spec.loader.exec_module(video)

# 6 秒正常内容 + 40 秒解码循环 + 2 秒正常内容
SRT = """1
00:00:00,000 --> 00:00:03,000
先讲目录怎么同步

2
00:00:03,000 --> 00:00:06,000
再看正文怎么按需拉

3
00:00:06,000 --> 00:00:26,000
对对对对对对对对对对对对对对对对对对对对

4
00:00:26,000 --> 00:00:46,000
对对对对对对对对对对对对对对对对对对对对

5
00:00:46,000 --> 00:00:48,000
这才是结尾那段
"""

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
            "audio": [
                {"baseUrl": "https://example.com/audio-low", "bandwidth": 65558},
                {"baseUrl": "https://example.com/audio-high", "bandwidth": 90671},
            ],
            "video": [
                {"baseUrl": "https://example.com/video-360", "height": 360, "bandwidth": 90000, "codecs": "hvc1.1.6.L120.90"},
                {"baseUrl": "https://example.com/video-480", "height": 480, "bandwidth": 80000, "codecs": "avc1.64001F"},
            ],
        }
    },
}


class VideoTest(unittest.TestCase):
    def test_parse_bvid(self):
        self.assertEqual(video.parse_bvid("https://www.bilibili.com/video/BV1Myez6LEKc/?vd_source=x"), "BV1Myez6LEKc")
        self.assertIsNone(video.parse_bvid("https://example.com/watch?v=abc"))

    def test_srt_roundtrip(self):
        cues = video.parse_srt(SRT)
        self.assertEqual(len(cues), 5)
        self.assertAlmostEqual(cues[0].start, 0.0)
        self.assertEqual(cues[0].text, "先讲目录怎么同步")
        again = video.parse_srt(video.render_srt(cues))
        self.assertEqual([(cue.start, cue.text) for cue in again], [(cue.start, cue.text) for cue in cues])

    def test_paragraph_markdown_marks_segment_start(self):
        markdown = video.paragraph_markdown(video.parse_srt(SRT), target_chars=20)
        self.assertTrue(markdown.startswith("**[00:00]**"))
        self.assertIn("**[00:26]**", markdown)
        self.assertEqual(len(markdown.strip().split("\n\n")), 3)
        self.assertTrue(markdown.endswith("\n"))

    def test_degenerate_detection_ignores_short_repeats(self):
        self.assertTrue(video.is_degenerate("对对对对对对对对对对对对对对对对对对对对"))
        self.assertFalse(video.is_degenerate("对"))
        self.assertFalse(video.is_degenerate("这一页讲的是目录怎么同步"))

    def test_find_degenerate_ranges_needs_enough_duration(self):
        cues = video.parse_srt(SRT)
        self.assertEqual(video.find_degenerate_ranges(cues), [(2, 3)])
        self.assertEqual(video.find_degenerate_ranges(cues, min_seconds=100.0), [])

    def test_apply_repairs_swaps_window_and_keeps_neighbours(self):
        cues = video.parse_srt(SRT)
        replacement = [
            video.Cue(1.0, 2.0, "循环之前的内容"),
            video.Cue(8.0, 12.0, "重跑补回的第一段"),
            video.Cue(30.0, 34.0, "重跑补回的第二段"),
            video.Cue(47.0, 48.0, "循环之后的内容"),
        ]
        merged = video.apply_repairs(cues, [(2, 3)], [replacement])
        texts = [cue.text for cue in merged]
        # 窗口是 [6-5, 46+5]：完全落在窗口内的原 cue 被重跑结果替换，
        # 跨在窗口左边界上的第一段保留，不丢内容。
        self.assertIn("先讲目录怎么同步", texts)
        self.assertIn("重跑补回的第一段", texts)
        self.assertIn("重跑补回的第二段", texts)
        self.assertIn("循环之后的内容", texts)
        self.assertNotIn("这才是结尾那段", texts)
        self.assertNotIn("对对对对对对对对对对对对对对对对对对对对", texts)
        self.assertEqual([cue.start for cue in merged], sorted(cue.start for cue in merged))

    def test_apply_repairs_keeps_original_when_repair_is_empty(self):
        cues = video.parse_srt(SRT)
        merged = video.apply_repairs(cues, [(2, 3)], [[]])
        self.assertEqual(len(merged), len(cues))
        self.assertIn("对对对对对对对对对对对对对对对对对对对对", [cue.text for cue in merged])

    def test_apply_repairs_drops_repair_output_that_is_still_degenerate(self):
        cues = video.parse_srt(SRT)
        still_looping = [video.Cue(8.0, 12.0, "对对对对对对对对对对对对对对对对对对对对")]
        merged = video.apply_repairs(cues, [(2, 3)], [still_looping])
        self.assertEqual(len(merged), len(cues))

    def test_capture_picks_best_streams(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "capture.json"
            path.write_text(json.dumps(CAPTURE), encoding="utf-8")
            info = video.from_capture(path, "https://www.bilibili.com/video/BV1Myez6LEKc/")
        self.assertEqual(info["bvid"], "BV1Myez6LEKc")
        self.assertEqual(info["cid"], "42055370907")
        self.assertEqual(info["owner"], "六十四条悟")
        self.assertEqual(info["audio_url"], "https://example.com/audio-high")
        # avc 优先于 hvc1，即使分辨率更高
        self.assertEqual(info["video_url"], "https://example.com/video-480")

    def test_capture_without_dash_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "capture.json"
            path.write_text(json.dumps({"data": {}}), encoding="utf-8")
            with self.assertRaises(video.FetchBlocked):
                video.from_capture(path, "https://www.bilibili.com/video/BV1Myez6LEKc/")

    def test_missing_or_broken_capture_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            missing = Path(temp) / "missing.json"
            with self.assertRaises(video.FetchBlocked):
                video.from_capture(missing, "https://www.bilibili.com/video/BV1Myez6LEKc/")
            broken = Path(temp) / "broken.json"
            broken.write_text("not json", encoding="utf-8")
            with self.assertRaises(video.FetchBlocked):
                video.from_capture(broken, "https://www.bilibili.com/video/BV1Myez6LEKc/")

    def test_browser_hint_names_the_video(self):
        hint = video.browser_hint("BV1Myez6LEKc")
        self.assertIn("BV1Myez6LEKc", hint)
        self.assertIn("--capture", hint)


if __name__ == "__main__":
    unittest.main()
