#!/usr/bin/env python3
"""
ingest.py - 抓取来源并存入 raw/sources/

用法:
  python3 tools/ingest.py <url> [--type blog|doc|video]
  python3 tools/ingest.py <url> --name <文件名> [--author <作者>] [--published <日期>]
  python3 tools/ingest.py <url> --file <预抓正文>            # 会话侧 reader 抓到正文时用
  python3 tools/ingest.py <B站视频 URL> [--capture <JSON>] [--slides]

B 站视频走 tools/video.py：下载音频、本地转录、修掉解码循环，--slides 再存一份
幻灯片缩略图总览到 raw/assets/。被风控拦下时先用浏览器会话取播放地址，用 --capture 传回来。

输出:
  raw/sources/<name>.md    (日期保存在来源头中)
"""

import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen


def _load_video_module():
    """tools/video.py 不在包路径里，按文件加载，避免污染 sys.path。"""
    spec = importlib.util.spec_from_file_location("wiki_video", Path(__file__).with_name("video.py"))
    module = importlib.util.module_from_spec(spec)
    # dataclass 解析类型时要能在 sys.modules 里找到本模块。
    sys.modules["wiki_video"] = module
    spec.loader.exec_module(module)
    return module


video = _load_video_module()

# 直抓网页时，正文短于这个长度就认为是风控页或需要 JS 渲染的空壳。
MIN_DIRECT_BODY_CHARS = 80


def die(message: str) -> None:
    print(f"错误: {message}", file=sys.stderr)
    sys.exit(1)


def fetch(url: str) -> str:
    """抓取网页 HTML"""
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; wiki-ingest/1.0)"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def is_github_repo(url: str) -> bool:
    """判断是否是 GitHub 仓库 URL"""
    parsed = urlparse(url)
    if parsed.netloc != "github.com":
        return False
    parts = parsed.path.strip("/").split("/")
    return len(parts) >= 2 and parts[0] != "" and parts[1] != ""


def fetch_github_readme(url: str) -> tuple[str, str]:
    """抓取 GitHub 仓库的 README，返回 (markdown, repo_full_name)"""
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    owner, repo = parts[0], parts[1]

    # 尝试 main 和 master 分支
    for branch in ["main", "master"]:
        readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
        try:
            req = Request(readme_url, headers={"User-Agent": "wiki-ingest/1.0"})
            with urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    content = resp.read().decode("utf-8", errors="replace")
                    return content, f"{owner}/{repo}"
        except Exception:
            continue

    # 尝试其他常见 README 文件名
    for branch in ["main", "master"]:
        for name in ["README.rst", "README.txt", "readme.md"]:
            readme_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}"
            try:
                req = Request(readme_url, headers={"User-Agent": "wiki-ingest/1.0"})
                with urlopen(req, timeout=30) as resp:
                    if resp.status == 200:
                        content = resp.read().decode("utf-8", errors="replace")
                        return content, f"{owner}/{repo}"
            except Exception:
                continue

    raise RuntimeError(f"无法找到 {owner}/{repo} 的 README")


def analyze_github_repo(url: str) -> str:
    """抓取 GitHub 仓库元信息，返回精简的来源记录（不存 README 和目录树）"""
    import json

    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    owner, repo = parts[0], parts[1]
    repo_name = f"{owner}/{repo}"

    # 用 GitHub API 获取仓库元信息
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = Request(api_url, headers={"User-Agent": "wiki-ingest/1.0", "Accept": "application/vnd.github+json"})
        with urlopen(req, timeout=30) as resp:
            meta = json.loads(resp.read().decode("utf-8"))
    except Exception:
        meta = {}

    lines = []
    lines.append(f"# {repo_name}\n")

    description = meta.get("description", "")
    if description:
        lines.append(f"> {description}\n")

    lines.append("## 基本信息\n")
    lines.append(f"- **仓库**: [{repo_name}]({url})")
    if meta.get("homepage"):
        lines.append(f"- **官网**: {meta['homepage']}")
    if meta.get("language"):
        lines.append(f"- **主语言**: {meta['language']}")
    if meta.get("stargazers_count") is not None:
        lines.append(f"- **Stars**: {meta['stargazers_count']}")
    if meta.get("license"):
        lines.append(f"- **License**: {meta['license']['spdx_id']}")
    lines.append("")

    # 关键文档指向（不存内容，只给链接）
    lines.append("## 关键文档\n")
    lines.append(f"- [README]({url}#readme)")

    # 尝试获取 docs 目录
    docs_url = f"https://api.github.com/repos/{owner}/{repo}/contents/docs"
    try:
        req = Request(docs_url, headers={"User-Agent": "wiki-ingest/1.0"})
        with urlopen(req, timeout=15) as resp:
            docs = json.loads(resp.read().decode("utf-8"))
            if isinstance(docs, list):
                doc_files = [d for d in docs if d.get("type") == "file" and d["name"].endswith(".md")]
                for d in doc_files[:10]:
                    lines.append(f"- [{d['name']}]({d['html_url']})")
    except Exception:
        pass

    lines.append("")

    # 值得一看的关键文件：src/ 下的入口和核心模块
    lines.append("## 关键文件\n")
    key_dirs = ["src", "lib", "packages/core/src", "packages"]
    found_any = False
    for kd in key_dirs:
        kd_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{kd}"
        try:
            req = Request(kd_url, headers={"User-Agent": "wiki-ingest/1.0"})
            with urlopen(req, timeout=15) as resp:
                entries = json.loads(resp.read().decode("utf-8"))
                if not isinstance(entries, list):
                    continue
                # 优先列入口文件，再列核心子目录
                entry_files = [e for e in entries if e.get("type") == "file"]
                entry_dirs = [e for e in entries if e.get("type") == "dir"]
                for e in entry_files[:15]:
                    lines.append(f"- [{e['path']}]({e['html_url']})")
                    found_any = True
                for e in entry_dirs[:10]:
                    lines.append(f"- [{e['path']}/]({e['html_url']})")
                    found_any = True
                if found_any:
                    break
        except Exception:
            continue

    if not found_any:
        lines.append("- （未找到 src/ 目录，请查看仓库根目录）")

    lines.append("")
    lines.append("## 说明\n")
    lines.append("本记录只包含仓库元信息和文件链接，尚未核对具体实现。")

    return "\n".join(lines) + "\n"


def slugify(text: str, max_len: int = 60) -> str:
    """从文本生成文件名 slug，优先保留 ASCII"""
    # 移除非 ASCII 字符（中文等），只保留英文、数字、连字符
    text = re.sub(r"[^\x00-\x7f]", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-")
    return text[:max_len].rstrip("-").lower()


def get_slug_from_url(url: str) -> str:
    """从 URL 提取 slug"""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")
    if is_github_repo(url):
        return slugify(path.strip("/").split("/")[1].removesuffix(".git"))
    if is_youtube_url(url) and parsed.path == "/watch":
        return slugify(parse_qs(parsed.query).get("v", [""])[0])
    if path:
        last = path.split("/")[-1]
        # 去掉扩展名
        last = re.sub(r"\.[a-z]+$", "", last)
        if last:
            return slugify(last)
    return slugify(parsed.hostname or "")


def source_path(sources_dir: Path, name: str) -> Path:
    """原始素材只新增；日期命名的旧文件也需要先人工检查。"""
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        die("无法生成合法文件名；请用 --name 指定英文小写、数字和连字符组成的名称（不含扩展名）")
    target = sources_dir / f"{name}.md"
    existing = ([target] if target.exists() else []) + sorted(
        sources_dir.glob(f"[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-{name}.md")
    )
    if existing:
        die(f"素材已存在，未覆盖: {', '.join(str(path) for path in existing)}。同一对象请审阅后合并；不同对象请用 --name 区分。")
    return target


def save_source(path: Path, content: str) -> None:
    try:
        # 排他创建同时保护检查路径之后出现的文件。
        with path.open("x", encoding="utf-8") as stream:
            stream.write(content)
    except FileExistsError:
        die(f"素材已存在，未覆盖: {path}")


def extract_title(html: str) -> str:
    """提取页面标题"""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return title
    return "untitled"


def extract_article(html: str) -> str:
    """提取正文 HTML"""
    # 尝试 article 标签
    m = re.search(r"<article[^>]*>(.*?)</article>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    # 尝试 main 标签
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    # 回退到 body
    m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    if m:
        return m.group(1)
    return html


class MDConverter(HTMLParser):
    """HTML 转 Markdown"""

    def __init__(self):
        super().__init__()
        self.result = []
        self.current = []
        self.in_pre = False
        self.in_code = False
        self.table_rows = []
        self.current_row = []
        self.current_cell = []
        self.in_table = False
        self.in_tr = False
        self.in_cell = False
        self.list_stack = []
        self.in_li = False
        self.li_content = []
        self.heading_level = 0
        self.link_href = None
        self.link_text = []
        self.in_blockquote = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "pre":
            self.in_pre = True
            self.result.append("\n```\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = True
            self.current.append("`")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heading_level = int(tag[1])
        elif tag == "br":
            self.current.append("\n")
        elif tag == "table":
            self.in_table = True
            self.table_rows = []
        elif tag == "tr":
            self.in_tr = True
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = True
            self.current_cell = []
        elif tag in ("ul", "ol"):
            self.list_stack.append(tag)
        elif tag == "li":
            self.in_li = True
            self.li_content = []
        elif tag == "blockquote":
            self.in_blockquote = True
        elif tag == "a":
            self.link_href = attrs.get("href", "")
            self.link_text = []
        elif tag in ("strong", "b"):
            self.current.append("**")
        elif tag in ("em", "i"):
            self.current.append("*")

    def handle_endtag(self, tag):
        if tag == "pre":
            self.in_pre = False
            self.result.append("\n```\n")
        elif tag == "code" and not self.in_pre:
            self.in_code = False
            self.current.append("`")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            text = "".join(self.current).strip()
            if text:
                self.result.append("#" * self.heading_level + " " + text + "\n")
            self.current = []
            self.heading_level = 0
        elif tag == "p":
            text = "".join(self.current).strip()
            if text:
                self.result.append(text + "\n")
            self.current = []
        elif tag == "table":
            self.in_table = False
            if self.table_rows:
                self.result.append("\n")
                for i, row in enumerate(self.table_rows):
                    self.result.append("| " + " | ".join(row) + " |\n")
                    if i == 0:
                        self.result.append("| " + " | ".join(["---"] * len(row)) + " |\n")
                self.result.append("\n")
            self.table_rows = []
        elif tag == "tr":
            self.in_tr = False
            if self.current_row:
                self.table_rows.append(self.current_row)
            self.current_row = []
        elif tag in ("td", "th"):
            self.in_cell = False
            cell_text = "".join(self.current_cell).strip()
            self.current_row.append(cell_text)
            self.current_cell = []
        elif tag == "li":
            self.in_li = False
            text = "".join(self.li_content).strip()
            if text:
                prefix = "  " * (len(self.list_stack) - 1)
                marker = "- " if self.list_stack[-1] == "ul" else "1. "
                self.result.append(prefix + marker + text + "\n")
            self.li_content = []
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "blockquote":
            self.in_blockquote = False
        elif tag == "a":
            text = "".join(self.link_text).strip()
            if text and self.link_href:
                self.current.append(f"[{text}]({self.link_href})")
            elif text:
                self.current.append(text)
            self.link_href = None
            self.link_text = []
        elif tag in ("strong", "b"):
            self.current.append("**")
        elif tag in ("em", "i"):
            self.current.append("*")

    def handle_data(self, data):
        if self.in_pre:
            self.result.append(data)
        elif self.in_cell:
            self.current_cell.append(data)
        elif self.in_li:
            self.li_content.append(data)
        elif self.link_href is not None:
            self.link_text.append(data)
        else:
            self.current.append(data)


def html_to_markdown(html: str) -> str:
    """HTML 转 Markdown"""
    article = extract_article(html)
    # 移除 script 和 style
    article = re.sub(r"<script[^>]*>.*?</script>", "", article, flags=re.DOTALL)
    article = re.sub(r"<style[^>]*>.*?</style>", "", article, flags=re.DOTALL)

    converter = MDConverter()
    converter.feed(article)
    text = "".join(converter.result)

    # 清理复制按钮残留
    text = text.replace("TEXTCopy", "")
    text = text.replace("MarkdownCopy", "")
    text = text.replace("Copy", "")
    # 清理格式残留
    text = re.sub(r"\*+`+\*+", "", text)
    text = re.sub(r"`+([^`\n])", r"\1", text)

    # 清理
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip() + "\n"


def build_source_header(
    url: str,
    source_type: str,
    title: str,
    author: str | None = None,
    published: str | None = None,
    note: str | None = None,
) -> str:
    """生成来源头"""
    today = date.today().isoformat()
    lines = ["<!--", f"source: {url}", f"type: {source_type}"]
    if author:
        lines.append(f"author: {author}")
    if published:
        lines.append(f"published: {published}")
    lines.append(f"fetched: {today}")
    if note:
        lines.append(f"note: {note}")
    lines.append("-->")
    return "\n".join(lines) + "\n\n"


def first_heading(markdown: str) -> str:
    """取 Markdown 第一个标题作为标题备选"""
    m = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    return m.group(1).strip() if m else ""


def read_prefetched(path: str) -> tuple[str, dict]:
    """读取会话侧工具预抓的正文，返回 (markdown 正文, 元信息)。

    支持两种输入：Markdown 文件，或含 content/markdown/body 字段的 JSON
    （例如会话侧 web reader 工具的返回值），JSON 里的 title、author、
    publishedTime 会一并提取进元信息。
    """
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read().strip()

    if not raw.startswith("{"):
        return raw, {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return raw, {}

    if not isinstance(data, dict):
        return raw, {}

    node = data.get("text") if isinstance(data.get("text"), dict) else data
    body = ""
    for key in ("content", "markdown", "body"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            body = value.strip()
            break
    if not body:
        die(f"{path} 是 JSON 但找不到 content/markdown/body 字段；请保存正文为 Markdown 文件后重试")

    meta: dict = {}
    if isinstance(node.get("title"), str) and node["title"].strip():
        meta["title"] = node["title"].strip()
    if isinstance(node.get("author"), str) and node["author"].strip():
        meta["author"] = node["author"].strip()
    for key in ("publishedTime", "published_time", "published"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            # publishedTime 形如 2026-02-08T00:00:00.000Z，取日期部分
            meta["published"] = value.strip()[:10]
            break
    return body, meta


def is_youtube_url(url: str) -> bool:
    """判断是否是 YouTube 视频 URL"""
    parsed = urlparse(url)
    return parsed.netloc in ("www.youtube.com", "youtube.com", "youtu.be")


def is_bilibili_url(url: str) -> bool:
    """判断是否是 B 站视频 URL（带 BV 号的视频页）"""
    return "bilibili.com" in urlparse(url).netloc and video.parse_bvid(url) is not None


def guard_direct_body(body_md: str, url: str) -> str:
    """直抓得到的正文过短时不落盘。

    风控页和需要 JS 渲染的空壳都会被解成几乎空的 Markdown；以前会写一个空文件
    并报「已保存」，看起来成功了，但后面还得人工发现并清理。
    """
    visible = re.sub(r"[#*`>\s\-\[\]()]", "", body_md)
    if len(visible) < MIN_DIRECT_BODY_CHARS:
        die(
            f"直抓的正文只有 {len(visible)} 个字符，可能是风控页或需要 JS 渲染：{url}\n"
            "改用会话侧 reader 工具抓正文后 --file 传入；B 站视频可以走 tools/video.py 的流程。"
        )
    return body_md


def _timestamp_of(frame: Path) -> float:
    """从 `frame-330s.png` 这种文件名里取回时间点。"""
    match = re.search(r"-(\d+)s\.png$", frame.name)
    return float(match.group(1)) if match else 0.0


def bilibili_video_body(
    title: str,
    info: dict,
    cues: list,
    report: dict,
    sheet_names: list[str],
    frame_names: list[str],
    origin: str,
) -> str:
    """拼出 B 站视频素材的正文：头注释 + 按段落整理的转录稿。"""
    duration = int(info.get("duration") or 0)
    lines = [
        f"# {title}",
        "",
        "<!--",
        f"本文件由 tools/ingest.py 调用 tools/video.py 生成；文字来自{origin}。",
        f"讲者 / 发布账号：{info.get('owner') or '未知'}",
    ]
    if duration:
        lines.append(f"时长：{duration // 60} 分 {duration % 60} 秒")
    if origin == "本地转录":
        lines.append("机器转录没有人工逐句校对。")
    if sheet_names:
        lines.append("幻灯片缩略图总览：" + "、".join(f"raw/assets/{name}" for name in sheet_names))
    if frame_names:
        lines.append("按时间点取的整帧：" + "、".join(f"raw/assets/{name}" for name in frame_names))
    lines += [
        "幻灯片是这类分享的事实层：表格、数字和标题以幻灯片为准，转录只作旁证。",
        "转写里的专有名词可能有识别误差，写作前用幻灯片或公开资料核对。",
    ]
    for repair in report.get("repairs", []):
        state = "已局部重跑补回" if repair["ok"] else "重跑也没有补回，保留原样"
        lines.append(
            f"解码循环 {video.format_clock(repair['start'])}–{video.format_clock(repair['end'])}：{state}"
        )
    lines += ["-->", "", video.paragraph_markdown(cues).rstrip(), ""]
    return "\n".join(lines) + "\n"


def fetch_youtube_transcript(url: str) -> tuple[str, str]:
    """用 yt-dlp 获取 YouTube 视频字幕，返回 (transcript, title)"""
    import subprocess
    import json

    # 获取视频信息
    try:
        result = subprocess.run(
            ["yt-dlp", "--dump-json", "--skip-download", url],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp 失败: {result.stderr}")
        info = json.loads(result.stdout)
        title = info.get("title", "untitled")
    except FileNotFoundError:
        raise RuntimeError("yt-dlp 未安装，请运行: brew install yt-dlp")

    # 获取字幕
    try:
        result = subprocess.run(
            ["yt-dlp", "--write-subs", "--write-auto-subs", "--sub-langs", "en,zh", "--skip-download", "-o", "/tmp/%(id)s", url],
            capture_output=True,
            text=True,
            timeout=120,
        )
    except Exception:
        pass

    # 尝试读取下载的字幕文件
    import glob
    subtitle_files = glob.glob("/tmp/*.vtt") + glob.glob("/tmp/*.srt")
    if not subtitle_files:
        return f"[无字幕] 视频标题: {title}\n\n请手动查看视频: {url}", title

    # 读取第一个字幕文件
    subtitle_file = subtitle_files[0]
    with open(subtitle_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 清理字幕格式（去掉时间戳等）
    if subtitle_file.endswith(".vtt"):
        content = re.sub(r"WEBVTT.*?\n\n", "", content, count=1)
        content = re.sub(r"\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n", "", content)
    elif subtitle_file.endswith(".srt"):
        content = re.sub(r"\d+\n", "", content)
        content = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n", "", content)

    content = re.sub(r"\n{3,}", "\n\n", content).strip()

    # 清理临时文件
    for f in subtitle_files:
        os.remove(f)

    return content, title


def is_x_url(url: str) -> bool:
    """判断是否是 X (Twitter) URL"""
    parsed = urlparse(url)
    return parsed.netloc in ("x.com", "twitter.com", "www.x.com", "www.twitter.com")


def fetch_x_thread(url: str) -> str:
    """抓取 X 推文线程"""
    # X 的网页抓取比较复杂，需要登录或 API
    # 这里用一个简单的方式：尝试抓取页面，提取推文文本
    html = fetch(url)

    # 提取推文文本
    tweets = re.findall(r'<article[^>]*>.*?<div[^>]*data-testid="tweetText"[^>]*>(.*?)</div>', html, re.DOTALL)

    if not tweets:
        return f"[无法自动抓取] 请手动复制推文内容到 raw/sources/\n\n原始链接: {url}"

    lines = []
    for tweet in tweets:
        text = re.sub(r"<[^>]+>", "", tweet)
        text = html.unescape(text).strip()
        if text:
            lines.append(text)

    return "\n\n---\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="抓取网页并存入 raw/sources/")
    parser.add_argument("url", help="网页 URL 或 GitHub 仓库 URL")
    parser.add_argument("--type", default="blog", choices=["blog", "doc", "repo", "video", "tweet"], help="来源类型")
    parser.add_argument("--name", help="素材文件名，不含扩展名，使用英文小写和连字符")
    parser.add_argument("--file", help="预抓正文路径（Markdown，或含 content 字段的 JSON），给出时跳过直接抓取")
    parser.add_argument("--author", help="来源作者，写入头注释")
    parser.add_argument("--published", help="来源发布日期（YYYY-MM-DD），写入头注释")
    parser.add_argument("--capture", help="浏览器会话里取到的元信息和播放地址 JSON（B 站）")
    parser.add_argument(
        "--cookies-from-browser",
        help="把浏览器登录态传给 yt-dlp（如 chrome），登录后能拿到字幕和更高画质",
    )
    parser.add_argument("--no-subs", action="store_true", help="跳过官方字幕，直接做本地转录")
    parser.add_argument("--slides", action="store_true", help="给 B 站视频再存一份幻灯片缩略图总览到 raw/assets/")
    parser.add_argument(
        "--frames",
        help="配合 --slides 使用：再抽这几个时间点的整帧到 raw/assets/，如 330,570",
    )
    parser.add_argument("--language", default="zh", help="转录语言，默认 zh")
    args = parser.parse_args()

    url = args.url
    source_type = args.type
    if is_bilibili_url(url):
        source_type = "video"
    elif is_youtube_url(url):
        source_type = "video"
    elif is_x_url(url):
        source_type = "tweet"
    elif is_github_repo(url):
        source_type = "repo"

    sources_dir = Path(__file__).resolve().parent.parent / "raw" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    name = args.name if args.name is not None else get_slug_from_url(url)
    md_path = source_path(sources_dir, name)
    meta = {}
    note = None

    if args.file:
        print(f"使用预抓正文: {args.file}")
        body_md, meta = read_prefetched(args.file)
        title = meta.get("title") or first_heading(body_md) or name
        note = "body pre-fetched; direct fetch skipped"
    elif source_type == "video" and is_bilibili_url(url):
        work_dir = Path(tempfile.mkdtemp(prefix="wiki-video-"))
        try:
            info = video.resolve_streams(
                url,
                Path(args.capture) if args.capture else None,
                args.cookies_from_browser,
            )
        except video.FetchBlocked as error:
            hint = f"\n\n{video.browser_hint(video.parse_bvid(url))}" if error.needs_browser else ""
            die(f"{error}{hint}")
        title = info.get("title") or name
        print(f"B 站视频: {title}（取数方式：{info.get('source')}）")
        try:
            subtitles = None
            if not args.no_subs and info.get("source") != "capture":
                subtitles = video.fetch_subtitles(
                    url, work_dir / "subs", cookies_from_browser=args.cookies_from_browser
                )
            sheet_names: list[str] = []
            frame_names: list[str] = []
            if subtitles:
                cues, language = subtitles
                origin = f"官方字幕（{language}）"
                report: dict = {"repairs": []}
                print(f"用官方字幕，{len(cues)} 段，跳过转录")
            else:
                origin = "本地转录"
                media = video.fetch_media(
                    url,
                    work_dir,
                    kind="audio",
                    info=info,
                    cookies_from_browser=args.cookies_from_browser,
                )
                print("正在本地转录（mlx-whisper，首次会下载模型）…")
                cues, report = video.transcribe_with_repair(media, work_dir, language=args.language)
                print(f"转录 {len(cues)} 段，已修掉 {len(report.get('repairs', []))} 处解码循环")
            if args.slides:
                # 抽帧是附加产物：下载视频或抽帧失败不应该把已经拿到的转录搞丢。
                try:
                    video_path = video.fetch_media(
                        url,
                        work_dir,
                        kind="video",
                        info=info,
                        cookies_from_browser=args.cookies_from_browser,
                    )
                    assets_dir = sources_dir.parent / "assets"
                    assets_dir.mkdir(parents=True, exist_ok=True)
                    for index, sheet in enumerate(
                        video.contact_sheets(video_path, work_dir / "slides"), start=1
                    ):
                        asset = assets_dir / f"{name}-slides-{index}.png"
                        shutil.copyfile(sheet, asset)
                        sheet_names.append(asset.name)
                    for frame in (
                        video.extract_frames(
                            video_path,
                            work_dir / "frames",
                            video.parse_timestamps(args.frames),
                        )
                        if args.frames
                        else []
                    ):
                        asset = assets_dir / f"{name}-frame-{int(_timestamp_of(frame))}s.png"
                        shutil.copyfile(frame, asset)
                        frame_names.append(asset.name)
                except video.FetchBlocked as error:
                    print(f"抽帧没成功，转录照常写入：{error}", file=sys.stderr)
        except video.FetchBlocked as error:
            die(str(error))
        body_md = bilibili_video_body(title, info, cues, report, sheet_names, frame_names, origin)
        print(f"中间产物留在：{work_dir}")
    elif source_type == "video" and is_youtube_url(url):
        try:
            transcript, title = fetch_youtube_transcript(url)
            body_md = f"# {title}\n\n{transcript}"
        except Exception as error:
            print(f"获取字幕失败: {error}")
            title = name
            body_md = f"# {title}\n\n[获取字幕失败，请手动查看视频]({url})"
    elif source_type == "tweet" and is_x_url(url):
        title = name
        try:
            body_md = fetch_x_thread(url)
        except Exception as error:
            print(f"抓取失败: {error}")
            body_md = f"[抓取失败，请手动复制推文内容]({url})"
    elif source_type == "repo" and is_github_repo(url):
        print(f"正在获取仓库元信息: {url}")
        title = name
        body_md = analyze_github_repo(url)
    else:
        print(f"抓取: {url}")
        html = fetch(url)
        title = extract_title(html)
        body_md = guard_direct_body(html_to_markdown(html), url)

    header = build_source_header(
        url, source_type, title,
        author=args.author or meta.get("author"),
        published=args.published or meta.get("published"),
        note=note,
    )
    save_source(md_path, header + body_md.rstrip() + "\n")
    print(f"已保存 Markdown: {md_path}")
    print(f"\n标题: {title}")
    print(f"类型: {source_type}")


if __name__ == "__main__":
    main()
