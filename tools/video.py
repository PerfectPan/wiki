#!/usr/bin/env python3
"""
video.py - 把视频来源整理成转录稿和幻灯片抽帧。

目前主要面向 B 站视频：B 站的视频页、字幕和播放地址接口都有风控，被拦下时
需要先在浏览器会话里取一次播放地址，再用 --capture 喂回来。转录和抽帧都在本地做。

用法:
  python3 tools/video.py streams <视频页 URL> [--capture <json>] [--out <目录>]
  python3 tools/video.py transcribe <音频或视频文件> --out-dir <目录> [--language zh]
  python3 tools/video.py slides <视频文件> --out-dir <目录> [--interval 60] [--frames 330,570]

产物:
  <目录>/meta.json        来源元信息（标题、作者、时长）
  <目录>/streams.json     可下载的音频、视频流地址
  <目录>/transcript.srt   转录（绝对时间戳）
  <目录>/transcript.md    按段落整理的转录稿，每段带起始时间
  <目录>/*.png            缩略图总览或指定时间点的整帧
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
BILIBILI_REFERER = "https://www.bilibili.com/"
VIEW_API = "https://api.bilibili.com/x/web-interface/view"
PLAYURL_API = "https://api.bilibili.com/x/player/wbi/playurl"
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
    """直连被拦下时，给一段可以在浏览器会话里直接跑的取数脚本。"""
    bvid = bvid or "<BV 号>"
    query = (
        f"https://api.bilibili.com/x/player/wbi/playurl?bvid={bvid}"
        f"&cid={cid or '<cid>'}&fnval=16&fnver=0&fourk=1"
    )
    return (
        "B 站直连被风控拦下（页面和接口都会返回 412）。用浏览器会话取一次播放地址：\n"
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


def http_bytes(url: str, referer: str | None = None, attempts: int = 3) -> bytes:
    """带浏览器 UA 取内容；B 站的媒体地址还会检查 Referer。"""
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
                raise FetchBlocked(f"HTTP 412（风控）：{url}", needs_browser=True) from error
            last_error = error
        except URLError as error:
            last_error = error
        if attempt + 1 < attempts:
            time.sleep(1.5 * (attempt + 1))
    raise FetchBlocked(f"请求失败：{url}（{last_error}）", needs_browser=True)


def http_json(url: str, referer: str | None = None) -> dict:
    try:
        payload = json.loads(http_bytes(url, referer=referer).decode("utf-8", errors="replace"))
    except json.JSONDecodeError as error:
        raise FetchBlocked(f"接口没有返回 JSON（可能被风控拦下）：{url}", needs_browser=True) from error
    if isinstance(payload, dict) and payload.get("code") not in (0, None):
        raise FetchBlocked(
            f"接口返回错误码 {payload.get('code')}: {payload.get('message')}", needs_browser=True
        )
    return payload


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


def resolve_streams(url: str, capture: Path | None = None) -> dict:
    """拿到标题、时长和可下载的音频、视频地址。"""
    bvid = parse_bvid(url)
    if not bvid:
        raise FetchBlocked(f"URL 里没有 BV 号：{url}")
    if capture:
        return from_capture(capture, url)
    view = http_json(f"{VIEW_API}?bvid={bvid}", referer=f"{BILIBILI_REFERER}video/{bvid}/")
    data = view.get("data") or {}
    if not data.get("cid"):
        raise FetchBlocked(f"没有取到 cid：{bvid}", needs_browser=True)
    playurl = http_json(
        f"{PLAYURL_API}?bvid={bvid}&cid={data['cid']}&fnval=16&fnver=0&fourk=1",
        referer=f"{BILIBILI_REFERER}video/{bvid}/",
    )
    dash = (playurl.get("data") or {}).get("dash") or {}
    owner = data.get("owner") or {}
    return {
        "bvid": bvid,
        "cid": str(data["cid"]),
        "title": data.get("title", ""),
        "owner": owner.get("name", ""),
        "duration": data.get("duration", 0),
        "audio_url": pick_audio(dash).get("baseUrl", ""),
        "video_url": pick_video(dash).get("baseUrl", ""),
        "source": "api",
    }


def download(url: str, path: Path, referer: str = BILIBILI_REFERER) -> Path:
    """下载媒体流。B 站的 CDN 偶发 SSL 中断，这里重试几次。"""
    payload = http_bytes(url, referer=referer, attempts=3)
    if not payload:
        raise FetchBlocked(f"下载到 0 字节：{url}")
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


def command_streams(args: argparse.Namespace) -> None:
    out_dir = Path(args.out)
    try:
        info = resolve_streams(args.url, Path(args.capture) if args.capture else None)
    except FetchBlocked as error:
        hint = f"\n\n{browser_hint(parse_bvid(args.url))}" if error.needs_browser else ""
        die(f"{error}{hint}")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meta.json").write_text(
        json.dumps({key: info[key] for key in ("bvid", "cid", "title", "owner", "duration", "source")},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (out_dir / "streams.json").write_text(
        json.dumps({"audio_url": info["audio_url"], "video_url": info["video_url"]}, indent=2),
        encoding="utf-8",
    )
    print(f"标题: {info['title']}")
    print(f"作者: {info['owner']}")
    print(f"时长: {int(info['duration']) // 60} 分 {int(info['duration']) % 60} 秒")
    print(f"音频流: {'有' if info['audio_url'] else '无'}；视频流: {'有' if info['video_url'] else '无'}")
    print(f"已写入: {out_dir / 'meta.json'}、{out_dir / 'streams.json'}")


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

    streams = subparsers.add_parser("streams", help="解析元信息和媒体流地址")
    streams.add_argument("url", help="B 站视频页 URL")
    streams.add_argument("--capture", help="浏览器会话里取到的 JSON（元信息 + playurl 返回体）")
    streams.add_argument("--out", default=".", help="输出目录")
    streams.set_defaults(handler=command_streams)

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
