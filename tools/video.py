#!/usr/bin/env python3
"""
video.py - 把视频来源整理成转录稿和幻灯片抽帧。

B 站接入交给 yt-dlp（它负责 wbi 签名、画质、cookie 和重试）；拿不到时再用浏览器会话
取一次播放地址、通过 --capture 喂回来。字幕优先，没有字幕再下载音频做本地转录。

用法:
  python3 tools/video.py probe <视频页 URL> [--capture <json>] [--cookies-from-browser chrome] [--out <目录>]
  python3 tools/video.py fetch <视频页 URL> [同上] [--no-subs] [--video]
  python3 tools/video.py transcribe <音频或视频文件> --out-dir <目录> [--language zh]
  python3 tools/video.py slides <视频文件> --out-dir <目录> [--interval 60] [--frames 330,570]

产物:
  <目录>/meta.json        来源元信息（标题、作者、时长、字幕情况）
  <目录>/subtitle.srt     官方字幕（有的话）
  <目录>/audio.m4a        音频（没有字幕时）
  <目录>/transcript.srt   转录（绝对时间戳）
  <目录>/transcript.md    按段落整理的转录稿，每段带起始时间
  <目录>/*.png            缩略图总览或指定时间点的整帧
"""

from __future__ import annotations

import argparse
import http.client
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BILIBILI_REFERER = "https://www.bilibili.com/"
PLAYURL_API = "https://api.bilibili.com/x/player/wbi/playurl"
SUBTITLE_LANGUAGES = ("zh-Hans", "zh-CN", "zh", "zh-Hant", "zh-TW", "en")
DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
DEFAULT_LANGUAGE = "zh"
REPAIR_MARGIN_SECONDS = 5.0
MAX_REPAIRS = 5


def die(message: str) -> None:
    print(f"错误: {message}", file=sys.stderr)
    sys.exit(1)


class FetchBlocked(RuntimeError):
    """拿不到来源或处理失败。

    needs_browser 为真时，说明失败原因是 B 站风控，提示里会附上浏览器会话的取数脚本；
    参数写错一类的问题不该让对方去开浏览器。
    """

    def __init__(self, message: str, needs_browser: bool = False):
        super().__init__(message)
        self.needs_browser = needs_browser


def parse_bvid(url: str) -> str | None:
    """从视频页 URL 里取出 BV 号。"""
    match = re.search(r"(BV[0-9A-Za-z]{10})", url)
    return match.group(1) if match else None


def browser_hint(bvid: str | None = None, cid: str | None = None) -> str:
    """连 yt-dlp 也拿不到时，给一段可以在浏览器会话里直接跑的取数脚本。"""
    bvid = bvid or "<BV 号>"
    query = (
        f"https://api.bilibili.com/x/player/wbi/playurl?bvid={bvid}"
        f"&cid={cid or '<cid>'}&fnval=16&fnver=0&fourk=1"
    )
    return (
        "yt-dlp 也没拿到内容。如果这是风控，可以在浏览器会话里直接取一次播放地址：\n"
        f"  1) 打开 https://www.bilibili.com/video/{bvid}/ ，等页面加载完；\n"
        "  2) 在页面上下文里执行（例如 browser-harness 的 js()）：\n"
        "     window.__INITIAL_STATE__.videoData 取 { bvid, cid, title, owner:{name}, duration }；\n"
        f"     再 fetch('{query}', {{credentials:'include'}}).then(r => r.json()) 取播放地址；\n"
        "  3) 把两次结果合成一个 JSON 文件，用 --capture <文件> 传回来。\n"
        "     也接受直接保存接口返回体（含 code/data/dash 字段），元信息用 meta 字段附上。"
    )


# --- 转录文本处理（纯函数，便于离线测试） ---------------------------------------


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


def format_clock(seconds: float) -> str:
    """把秒数写成 [分:秒]，用作转录稿里的段落标记。"""
    total = int(seconds)
    return f"[{total // 60:02d}:{total % 60:02d}]"


def parse_srt(text: str) -> list[Cue]:
    """解析 SRT，返回带绝对时间戳的 cue 列表。"""
    cues: list[Cue] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line for line in block.strip().split("\n") if line.strip()]
        if len(lines) < 3:
            continue
        match = re.match(
            r"(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)", lines[1]
        )
        if not match:
            continue
        parts = [int(value) for value in match.groups()]
        start = parts[0] * 3600 + parts[1] * 60 + parts[2] + parts[3] / 1000
        end = parts[4] * 3600 + parts[5] * 60 + parts[6] + parts[7] / 1000
        cues.append(Cue(start, end, " ".join(lines[2:]).strip()))
    return cues


def render_srt(cues: list[Cue]) -> str:
    """把 cue 列表写回 SRT。"""
    blocks = []
    for index, cue in enumerate(cues, start=1):
        blocks.append(f"{index}\n{_srt_time(cue.start)} --> {_srt_time(cue.end)}\n{cue.text}")
    return "\n\n".join(blocks) + "\n"


def _srt_time(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours, millis = divmod(millis, 3600 * 1000)
    minutes, millis = divmod(millis, 60 * 1000)
    secs, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def paragraph_markdown(cues: list[Cue], target_chars: int = 170) -> str:
    """把 cue 合并成段落，每段前面标出起始时间。"""
    paragraphs: list[str] = []
    buffer: list[str] = []
    length = 0
    start = 0.0
    for cue in cues:
        if not buffer:
            start = cue.start
        buffer.append(cue.text)
        length += len(cue.text)
        if length >= target_chars:
            paragraphs.append(f"**{format_clock(start)}** {''.join(buffer)}")
            buffer, length = [], 0
    if buffer:
        paragraphs.append(f"**{format_clock(start)}** {''.join(buffer)}")
    return "\n\n".join(paragraphs) + "\n"


def is_degenerate(text: str) -> bool:
    """判断一段文本是不是解码循环的产物。

    模型卡进循环时会连续输出同一个字（例如「对对对对…」），特征是用字种类极少。
    正常的口播句子即使很短，用字比例也不会这么低。
    """
    core = re.sub(r"[\s，。、！？,.!?…—]", "", text)
    if len(core) < 8:
        return False
    return len(set(core)) <= 3 or len(set(core)) / len(core) < 0.15


def find_degenerate_ranges(cues: list[Cue], min_seconds: float = 20.0) -> list[tuple[int, int]]:
    """找出连续成片、时长超过阈值的解码循环区间（闭区间索引）。"""
    ranges: list[tuple[int, int]] = []
    start: int | None = None
    for index, cue in enumerate(cues):
        if is_degenerate(cue.text):
            if start is None:
                start = index
            continue
        if start is not None:
            if cues[index - 1].end - cues[start].start >= min_seconds:
                ranges.append((start, index - 1))
            start = None
    if start is not None and cues[-1].end - cues[start].start >= min_seconds:
        ranges.append((start, len(cues) - 1))
    return ranges


def apply_repairs(
    cues: list[Cue],
    ranges: list[tuple[int, int]],
    replacements: list[list[Cue]],
    margin: float = REPAIR_MARGIN_SECONDS,
) -> list[Cue]:
    """用重跑结果替换解码循环区间。

    每个区间向外扩 margin 秒作为窗口，窗口内的原 cue 全部丢掉，换成重跑结果里
    落在同一窗口内的 cue；重跑拿不到有效内容时保留原 cue。
    """
    plans: list[tuple[tuple[float, float], list[Cue]]] = []
    for (first, last), replacement in zip(ranges, replacements):
        window = (max(0.0, cues[first].start - margin), cues[last].end + margin)
        usable = [
            cue
            for cue in replacement
            if cue.end > window[0] and cue.start < window[1] and not is_degenerate(cue.text)
        ]
        plans.append((window, usable))

    # 只有真的补回了内容，才丢掉窗口内的原 cue。
    # 跨在窗口边界上的原 cue 保留，否则它落在窗口外的那一小段就没人覆盖了。
    active = [window for window, usable in plans if usable]
    kept = [
        cue
        for cue in cues
        if not any(cue.start >= start and cue.end <= end for start, end in active)
    ]
    merged = kept + [cue for _, usable in plans for cue in usable]
    return sorted(merged, key=lambda cue: cue.start)


# --- 网络 ---------------------------------------------------------------------


def shorten(url: str, limit: int = 110) -> str:
    """媒体地址很长（带一堆签名参数），报错时截短一点。"""
    return url if len(url) <= limit else f"{url[:limit]}…"


def http_bytes(url: str, referer: str | None = None, attempts: int = 3) -> bytes:
    """带浏览器 UA 取内容；B 站的媒体地址还会检查 Referer。

    除了 HTTP 错误，还会碰到连接被直接断开的情况：同一种失败会重试几次。
    """
    headers = {"User-Agent": BROWSER_UA, "Accept-Language": "zh-CN,zh;q=0.9"}
    if referer:
        headers["Referer"] = referer
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return response.read()
        except HTTPError as error:
            if error.code == 412:
                raise FetchBlocked(f"HTTP 412（风控）：{shorten(url)}", needs_browser=True) from error
            last_error = error
        except (OSError, http.client.HTTPException) as error:
            # URLError 和 RemoteDisconnected 都在这里：B 站 CDN 会直接断连。
            last_error = error
        if attempt + 1 < attempts:
            time.sleep(1.5 * (attempt + 1))
    raise FetchBlocked(f"请求失败：{shorten(url)}（{last_error}）", needs_browser=True)


def pick_audio(dash: dict) -> dict:
    """音频取码率最高的一路。"""
    streams = dash.get("audio") or []
    if not streams:
        raise FetchBlocked("播放地址里没有音频流；可能需要登录才能取到。", needs_browser=True)
    return max(streams, key=lambda stream: stream.get("bandwidth", 0))


def pick_video(dash: dict, max_height: int | None = None) -> dict:
    """视频优先选 avc 编码（ffmpeg 抽帧兼容性最好），再按分辨率和码率排。"""
    streams = [stream for stream in (dash.get("video") or []) if stream.get("baseUrl")]
    if max_height:
        capped = [stream for stream in streams if stream.get("height", 0) <= max_height]
        streams = capped or streams
    if not streams:
        raise FetchBlocked("播放地址里没有视频流；可能需要登录才能取到。", needs_browser=True)

    def sort_key(stream: dict) -> tuple:
        codecs = stream.get("codecs", "")
        return (codecs.startswith("avc"), stream.get("height", 0), stream.get("bandwidth", 0))

    return max(streams, key=sort_key)


def from_capture(capture: Path, url: str) -> dict:
    """读取浏览器会话里存下来的元信息和播放地址。"""
    if not capture.exists():
        raise FetchBlocked(f"找不到 capture 文件：{capture}")
    try:
        payload = json.loads(capture.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise FetchBlocked(f"{capture} 不是合法 JSON：{error}") from error
    if not isinstance(payload, dict):
        raise FetchBlocked(f"{capture} 顶层应该是对象，里面放 meta 和 playurl 返回体。")
    meta = payload.get("meta") if isinstance(payload.get("meta"), dict) else {}
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    dash = data.get("dash") or {}
    if not dash:
        raise FetchBlocked(f"{capture} 里没有 dash 播放地址；请把 playurl 接口的返回体存进去。")
    video_data = meta.get("videoData") if isinstance(meta.get("videoData"), dict) else meta
    owner = video_data.get("owner")
    owner_name = owner.get("name") if isinstance(owner, dict) else owner
    return {
        "bvid": video_data.get("bvid") or parse_bvid(url) or "",
        "cid": str(video_data.get("cid") or data.get("cid") or ""),
        "title": video_data.get("title") or "",
        "owner": owner_name or "",
        "duration": video_data.get("duration") or 0,
        "audio_url": pick_audio(dash).get("baseUrl", ""),
        "video_url": pick_video(dash).get("baseUrl", ""),
        "source": "capture",
    }


def subtitle_languages(info: dict) -> list[str]:
    """列出 yt-dlp 这一趟能看到哪些字幕（人工字幕和自动字幕分开）。"""
    languages: list[str] = []
    for key in ("subtitles", "automatic_captions"):
        for language in (info.get(key) or {}):
            if language != "danmaku" and language not in languages:
                languages.append(language)
    return languages


# 记住真正能用的那个 yt-dlp 入口：同一次运行里要跑好几次命令，
# 没必要每次都先撞一遍旧版本。
_PREFERRED_YTDLP: list[str] | None = None


def ytdlp_candidates() -> list[list[str]]:
    """候选入口：先用 PATH 里的 yt-dlp，再用 uvx 拉的最新版。"""
    if _PREFERRED_YTDLP:
        return [list(_PREFERRED_YTDLP)]
    candidates: list[list[str]] = []
    if shutil.which("yt-dlp"):
        candidates.append(["yt-dlp"])
    if shutil.which("uvx"):
        candidates.append(["uvx", "--from", "yt-dlp", "yt-dlp"])
    if not candidates:
        raise FetchBlocked(
            "B 站接入需要 yt-dlp：brew install yt-dlp，或装 uv 后用 uvx --from yt-dlp 运行。"
        )
    return candidates


def looks_like_risk_control(text: str) -> bool:
    """判断 yt-dlp 的报错是不是 B 站风控（旧版本常见）。"""
    lowered = text.lower()
    return "412" in text or "风控" in text or "risk" in lowered or "precondition failed" in lowered


def run_ytdlp(
    arguments: list[str],
    *,
    cookies_from_browser: str | None = None,
    attempts: int = 3,
) -> subprocess.CompletedProcess:
    """跑 yt-dlp，带重试。

    到 B 站的连接会间歇性出现 SSL 中断，所以同一条命令会多跑几次。安装版过旧时
    B 站会返回 412，碰到这种情况直接换成 uvx 拉的最新版再试。真的被风控拦下时
    把 needs_browser 置上，让调用方提示去浏览器会话取数。
    """
    retries = ["--retries", "5", "--fragment-retries", "5", "--extractor-retries", "3"]
    candidates = ytdlp_candidates()
    if cookies_from_browser:
        arguments = [*arguments, "--cookies-from-browser", cookies_from_browser]

    result: subprocess.CompletedProcess | None = None
    for index, base in enumerate(candidates):
        command = base + retries + arguments
        for attempt in range(attempts):
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                global _PREFERRED_YTDLP
                _PREFERRED_YTDLP = list(base)
                return result
            tail = (result.stderr or "").strip()
            if looks_like_risk_control(tail):
                break
            if attempt + 1 < attempts:
                time.sleep(2.0 * (attempt + 1))
        if index + 1 < len(candidates):
            print("yt-dlp 没成功，改用 uvx 拉最新版再试一遍…", file=sys.stderr)
    tail = "\n".join(((result.stderr if result else "") or "").strip().split("\n")[-3:])
    raise FetchBlocked(f"yt-dlp 失败：{tail}", needs_browser=looks_like_risk_control(tail))


def ytdlp_info(url: str, cookies_from_browser: str | None = None) -> dict:
    """取元信息（不下载）：标题、作者、时长、可见的字幕语言。"""
    result = run_ytdlp(
        ["--dump-single-json", "--skip-download", "--no-playlist", url],
        cookies_from_browser=cookies_from_browser,
    )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise FetchBlocked(f"yt-dlp 没有返回 JSON：{error}") from error


def resolve_streams(
    url: str,
    capture: Path | None = None,
    cookies_from_browser: str | None = None,
) -> dict:
    """拿到标题、时长、字幕可用情况和下载方式。

    默认交给 yt-dlp（它负责 wbi 签名、画质和重试）；yt-dlp 也拿不到时，
    用浏览器会话存下来的 --capture JSON 走人工路径。
    """
    bvid = parse_bvid(url)
    if not bvid:
        raise FetchBlocked(f"URL 里没有 BV 号：{url}")
    if capture:
        return from_capture(capture, url)
    info = ytdlp_info(url, cookies_from_browser)
    return {
        "bvid": info.get("id") or bvid,
        "cid": str(info.get("cid") or ""),
        "title": info.get("title") or "",
        "owner": info.get("uploader") or info.get("channel") or "",
        "duration": info.get("duration") or 0,
        "subtitles": subtitle_languages(info),
        "audio_url": "",
        "video_url": "",
        "source": "yt-dlp",
    }


def fetch_media(
    url: str,
    out_dir: Path,
    *,
    kind: str = "audio",
    info: dict | None = None,
    cookies_from_browser: str | None = None,
) -> Path:
    """下载音频或视频。yt-dlp 路径交给 yt-dlp，capture 路径直接抓流地址。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    info = info or {}
    if info.get("source") == "capture":
        key = "audio_url" if kind == "audio" else "video_url"
        if not info.get(key):
            raise FetchBlocked(f"capture 里没有 {kind} 地址。")
        return download(info[key], out_dir / f"{kind}.m4s")
    selector = "bestaudio" if kind == "audio" else "bestvideo"
    template = str(out_dir / f"{kind}.%(ext)s")
    arguments = ["-f", selector, "--no-playlist"]
    if kind == "audio":
        arguments += ["-x", "--audio-format", "m4a"]
    arguments += ["-o", template, url]
    run_ytdlp(arguments, cookies_from_browser=cookies_from_browser)
    produced = sorted(out_dir.glob(f"{kind}.*"), key=lambda path: path.stat().st_mtime)
    if not produced:
        raise FetchBlocked(f"yt-dlp 没有产出 {kind} 文件：{out_dir}")
    return produced[-1]


def fetch_subtitles(
    url: str,
    out_dir: Path,
    *,
    cookies_from_browser: str | None = None,
    languages: tuple[str, ...] = SUBTITLE_LANGUAGES,
) -> tuple[list[Cue], str] | None:
    """先试官方字幕。没有就返回 None，让调用方回落到本地转录。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        run_ytdlp(
            [
                "--write-subs",
                "--write-auto-subs",
                "--sub-langs",
                ",".join(languages),
                "--sub-format",
                "srt",
                "--convert-subs",
                "srt",
                "--skip-download",
                "--no-playlist",
                "-o",
                str(out_dir / "subs.%(ext)s"),
                url,
            ],
            cookies_from_browser=cookies_from_browser,
        )
    except FetchBlocked as error:
        # 没登录时会报「字幕只有登录后才可用」，这也是正常情况；按没有字幕往下走。
        print(f"字幕这一步没有成功，按没有字幕处理：{error}", file=sys.stderr)
        return None
    produced = sorted(out_dir.glob("*.srt"))
    if not produced:
        return None

    def rank(path: Path) -> int:
        for index, language in enumerate(languages):
            if language in path.name:
                return index
        return len(languages)

    chosen = min(produced, key=rank)
    cues = parse_srt(chosen.read_text(encoding="utf-8", errors="replace"))
    if not cues:
        return None
    language = next((code for code in languages if code in chosen.name), chosen.stem)
    return cues, language


def download(url: str, path: Path, referer: str = BILIBILI_REFERER) -> Path:
    """下载媒体流。媒体地址带签名和时限，取到后尽快用（过期会 403）。"""
    payload = http_bytes(url, referer=referer, attempts=3)
    if not payload:
        raise FetchBlocked(f"下载到 0 字节：{shorten(url)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return path


# --- 转录 ---------------------------------------------------------------------


def run(command: list[str], quiet: bool = False) -> subprocess.CompletedProcess:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        tail = "\n".join((result.stderr or result.stdout or "").strip().split("\n")[-3:])
        raise FetchBlocked(f"命令失败：{' '.join(command[:3])} …\n{tail}")
    if not quiet and result.stderr:
        sys.stderr.write(result.stderr)
    return result


def whisper_command() -> list[str]:
    """本地优先用 mlx-whisper（Apple GPU）；没有时用 uvx 现装现跑。

    不要用 openai-whisper 的 MPS 后端：它会输出 NaN，且不报错。
    """
    if shutil.which("mlx_whisper"):
        return ["mlx_whisper"]
    if shutil.which("uvx"):
        return ["uvx", "--from", "mlx-whisper", "mlx_whisper"]
    raise FetchBlocked(
        "没有找到 mlx_whisper 或 uvx。macOS 上可以 pip install mlx-whisper，"
        "或安装 uv 后用 uvx --from mlx-whisper 运行。"
    )


def run_whisper(
    media: Path,
    work_dir: Path,
    *,
    language: str = DEFAULT_LANGUAGE,
    model: str = DEFAULT_MODEL,
    clip: tuple[float, float] | None = None,
    condition_on_previous_text: bool = True,
) -> list[Cue]:
    """跑一次转录，返回 cue 列表。clip 用来只重跑某一段。"""
    work_dir.mkdir(parents=True, exist_ok=True)
    command = whisper_command() + [
        str(media),
        "--model",
        model,
        "--language",
        language,
        "--task",
        "transcribe",
        "--output-dir",
        str(work_dir),
        "--output-format",
        "srt",
        "--verbose",
        "False",
    ]
    if clip:
        command += ["--clip-timestamps", f"{clip[0]},{clip[1]}"]
    if not condition_on_previous_text:
        command += ["--condition-on-previous-text", "False"]
    run(command)
    produced = sorted(work_dir.glob("*.srt"), key=lambda path: path.stat().st_mtime)
    if not produced:
        raise FetchBlocked(f"转录没有产出 SRT：{work_dir}")
    return parse_srt(produced[-1].read_text(encoding="utf-8"))


def transcribe_with_repair(
    media: Path,
    out_dir: Path,
    *,
    language: str = DEFAULT_LANGUAGE,
    model: str = DEFAULT_MODEL,
) -> tuple[list[Cue], dict]:
    """转录并在检测到解码循环时局部重跑。

    返回 (cue 列表, 报告)。报告里记录重跑的区间和是否仍然可疑。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    cues = run_whisper(media, out_dir / "asr-full", language=language, model=model)
    ranges = find_degenerate_ranges(cues)
    report: dict = {"cues": len(cues), "repairs": []}
    if not ranges:
        (out_dir / "transcript.srt").write_text(render_srt(cues), encoding="utf-8")
        (out_dir / "transcript.md").write_text(paragraph_markdown(cues), encoding="utf-8")
        return cues, report

    replacements: list[list[Cue]] = []
    for index, (first, last) in enumerate(ranges[:MAX_REPAIRS]):
        start = max(0.0, cues[first].start - REPAIR_MARGIN_SECONDS)
        end = cues[last].end + REPAIR_MARGIN_SECONDS
        try:
            redone = run_whisper(
                media,
                out_dir / f"asr-repair-{index + 1}",
                language=language,
                model=model,
                clip=(round(start, 1), round(end, 1)),
                condition_on_previous_text=False,
            )
        except FetchBlocked as error:
            print(f"警告: 重跑 {format_clock(start)} 失败：{error}", file=sys.stderr)
            redone = []
        repaired = [cue for cue in redone if not is_degenerate(cue.text)]
        report["repairs"].append(
            {
                "start": round(start, 1),
                "end": round(end, 1),
                "recovered": len(repaired),
                "ok": bool(repaired),
            }
        )
        replacements.append(repaired)

    cues = apply_repairs(cues, ranges[:MAX_REPAIRS], replacements)
    (out_dir / "transcript.srt").write_text(render_srt(cues), encoding="utf-8")
    (out_dir / "transcript.md").write_text(paragraph_markdown(cues), encoding="utf-8")
    report["remaining_degenerate"] = len(find_degenerate_ranges(cues, min_seconds=10.0))
    return cues, report


# --- 抽帧 ---------------------------------------------------------------------


def require_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise FetchBlocked(f"没有找到 {tool}；抽帧需要 ffmpeg（macOS 上 brew install ffmpeg）。")


def video_duration(path: Path) -> float:
    result = run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        quiet=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


def contact_sheets(
    video: Path, out_dir: Path, *, interval: float = 60.0, tiles: int = 5
) -> list[Path]:
    """每 interval 秒取一帧拼成缩略图总览，用来先看清整场讲了哪些页。"""
    require_ffmpeg()
    out_dir.mkdir(parents=True, exist_ok=True)
    duration = video_duration(video)
    span = interval * tiles * tiles
    sheets: list[Path] = []
    index = 1
    start = 0.0
    while start < duration or index == 1:
        path = out_dir / f"sheet-{index}.png"
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                str(start),
                "-t",
                str(span),
                "-i",
                str(video),
                "-vf",
                f"fps=1/{interval},scale=400:-1,tile={tiles}x{tiles}",
                "-frames:v",
                "1",
                "-y",
                str(path),
            ],
            quiet=True,
        )
        if path.exists() and path.stat().st_size > 0:
            sheets.append(path)
        start += span
        index += 1
    return sheets


def extract_frames(video: Path, out_dir: Path, timestamps: list[float]) -> list[Path]:
    """按时间点取整帧，用来读幻灯片上的表格和数字。"""
    require_ffmpeg()
    out_dir.mkdir(parents=True, exist_ok=True)
    frames: list[Path] = []
    for timestamp in timestamps:
        path = out_dir / f"frame-{int(timestamp)}s.png"
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                str(timestamp),
                "-i",
                str(video),
                "-frames:v",
                "1",
                "-y",
                str(path),
            ],
            quiet=True,
        )
        if path.exists():
            frames.append(path)
    return frames


# --- 命令行 -------------------------------------------------------------------


def parse_timestamps(value: str) -> list[float]:
    return [float(item) for item in re.split(r"[,\s]+", value.strip()) if item]


def probe_or_die(args: argparse.Namespace) -> dict:
    try:
        return resolve_streams(
            args.url,
            Path(args.capture) if args.capture else None,
            args.cookies_from_browser,
        )
    except FetchBlocked as error:
        hint = f"\n\n{browser_hint(parse_bvid(args.url))}" if error.needs_browser else ""
        die(f"{error}{hint}")


def describe(info: dict) -> list[str]:
    duration = int(info.get("duration") or 0)
    lines = [
        f"标题: {info.get('title') or '(未知)'}",
        f"作者: {info.get('owner') or '(未知)'}",
    ]
    if duration:
        lines.append(f"时长: {duration // 60} 分 {duration % 60} 秒")
    lines.append(f"取数方式: {info.get('source')}")
    if info.get("source") == "capture":
        lines.append(
            f"capture 流: 音频{'有' if info.get('audio_url') else '无'}；视频{'有' if info.get('video_url') else '无'}"
        )
    elif "subtitles" in info:
        available = info["subtitles"]
        lines.append(f"可见字幕: {', '.join(available) if available else '没有（未登录时通常拿不到）'}")
    return lines


def write_meta(out_dir: Path, info: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        key: info.get(key)
        for key in ("bvid", "cid", "title", "owner", "duration", "source", "subtitles")
        if info.get(key) is not None
    }
    path = out_dir / "meta.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def command_probe(args: argparse.Namespace) -> None:
    info = probe_or_die(args)
    for line in describe(info):
        print(line)
    print(f"已写入: {write_meta(Path(args.out), info)}")


def command_fetch(args: argparse.Namespace) -> None:
    info = probe_or_die(args)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for line in describe(info):
        print(line)
    print(f"已写入: {write_meta(out_dir, info)}")

    subtitles = None
    if not args.no_subs and info.get("source") != "capture":
        subtitles = fetch_subtitles(
            args.url, out_dir / "subs", cookies_from_browser=args.cookies_from_browser
        )
    if subtitles:
        cues, language = subtitles
        (out_dir / "subtitle.srt").write_text(render_srt(cues), encoding="utf-8")
        print(f"拿到官方字幕（{language}），{len(cues)} 段；不需要转录，下一步直接写正文")
    else:
        print("没有可用字幕，下一步下载音频做本地转录")
        media = fetch_media(
            args.url,
            out_dir,
            kind="audio",
            info=info,
            cookies_from_browser=args.cookies_from_browser,
        )
        print(f"音频: {media}")
    if args.video:
        video_path = fetch_media(
            args.url,
            out_dir,
            kind="video",
            info=info,
            cookies_from_browser=args.cookies_from_browser,
        )
        print(f"视频: {video_path}")


def command_transcribe(args: argparse.Namespace) -> None:
    media = Path(args.media)
    if not media.exists():
        die(f"找不到媒体文件：{media}")
    cues, report = transcribe_with_repair(
        media, Path(args.out_dir), language=args.language, model=args.model
    )
    print(f"转录 {len(cues)} 段，覆盖到 {format_clock(cues[-1].end) if cues else '0:00'}")
    for repair in report["repairs"]:
        state = "已补回" if repair["ok"] else "没有补回，保留原文"
        print(
            f"  解码循环 {format_clock(repair['start'])}–{format_clock(repair['end'])}："
            f"{state}（{repair['recovered']} 段）"
        )
    print(f"已写入: {Path(args.out_dir) / 'transcript.md'}、{Path(args.out_dir) / 'transcript.srt'}")


def command_slides(args: argparse.Namespace) -> None:
    video = Path(args.video)
    if not video.exists():
        die(f"找不到视频文件：{video}")
    out_dir = Path(args.out_dir)
    sheets = contact_sheets(video, out_dir, interval=args.interval) if not args.no_sheet else []
    for sheet in sheets:
        print(f"缩略图总览: {sheet}")
    if args.frames:
        for frame in extract_frames(video, out_dir, parse_timestamps(args.frames)):
            print(f"整帧: {frame}")


def main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(description="视频来源转录与抽帧")
    subparsers = parser.add_subparsers(dest="command", required=True)

    def add_source_options(sub: argparse.ArgumentParser) -> None:
        sub.add_argument("url", help="B 站视频页 URL")
        sub.add_argument("--capture", help="浏览器会话里取到的 JSON（元信息 + playurl 返回体）")
        sub.add_argument(
            "--cookies-from-browser",
            help="把浏览器登录态传给 yt-dlp（如 chrome），登录后能拿到字幕和更高画质",
        )

    probe = subparsers.add_parser("probe", help="只看元信息和字幕情况，不下载")
    add_source_options(probe)
    probe.add_argument("--out", default=".", help="输出目录")
    probe.set_defaults(handler=command_probe)

    fetch = subparsers.add_parser("fetch", help="下载字幕，或下载音频（必要时再下视频）")
    add_source_options(fetch)
    fetch.add_argument("--out", default=".", help="输出目录")
    fetch.add_argument("--no-subs", action="store_true", help="跳过字幕，直接下载音频")
    fetch.add_argument("--video", action="store_true", help="同时下载视频（抽帧用）")
    fetch.set_defaults(handler=command_fetch)

    transcribe = subparsers.add_parser("transcribe", help="转录并修掉解码循环")
    transcribe.add_argument("media", help="音频或视频文件")
    transcribe.add_argument("--out-dir", default=".", help="输出目录")
    transcribe.add_argument("--language", default=DEFAULT_LANGUAGE, help="语言，默认 zh")
    transcribe.add_argument("--model", default=DEFAULT_MODEL, help="Whisper 模型")
    transcribe.set_defaults(handler=command_transcribe)

    slides = subparsers.add_parser("slides", help="生成缩略图总览和指定时间点的整帧")
    slides.add_argument("video", help="视频文件")
    slides.add_argument("--out-dir", default=".", help="输出目录")
    slides.add_argument("--interval", type=float, default=60.0, help="缩略图间隔秒数，默认 60")
    slides.add_argument("--frames", help="要取整帧的时间点，逗号或空格分隔")
    slides.add_argument("--no-sheet", action="store_true", help="只取整帧，不做缩略图总览")
    slides.set_defaults(handler=command_slides)

    args = parser.parse_args(argv)
    try:
        args.handler(args)
    except FetchBlocked as error:
        die(str(error))


if __name__ == "__main__":
    main(sys.argv[1:])
