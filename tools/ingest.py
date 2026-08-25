#!/usr/bin/env python3
"""
ingest.py - 抓取网页并提取为 Markdown，存入 raw/sources/

用法:
  python3 tools/ingest.py <url> [--type blog|doc]

输出:
  raw/sources/YYYY-MM-DD-主题.html  (原始 HTML)
  raw/sources/YYYY-MM-DD-主题.md    (提取后的 Markdown)
"""

import argparse
import os
import re
import sys
from datetime import date
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import Request, urlopen


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
    """Clone GitHub 仓库并分析结构，返回分析报告"""
    import subprocess
    import tempfile

    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    owner, repo = parts[0], parts[1]
    repo_name = f"{owner}/{repo}"

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, repo)
        # shallow clone
        try:
            subprocess.run(
                ["git", "clone", "--depth", "1", url, repo_path],
                check=True,
                capture_output=True,
                timeout=120,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"clone 失败: {e.stderr.decode()}")

        lines = []
        lines.append(f"# {repo_name} 仓库分析\n")

        # 项目概览分析
        lines.append("## 项目概览\n")
        overview = analyze_repo_overview(repo_path)
        lines.append(overview)
        lines.append("")

        # 技术栈
        lines.append("## 技术栈\n")
        tech_stack = detect_tech_stack(repo_path)
        lines.append(tech_stack)
        lines.append("")

        # 项目规模
        lines.append("## 项目规模\n")
        stats = count_repo_stats(repo_path)
        lines.append(stats)
        lines.append("")

        # 目录结构
        lines.append("## 目录结构\n")
        lines.append("```")
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "dist", "build", ".next", ".venv", "venv", "__pycache__")]
            level = root.replace(repo_path, "").count(os.sep)
            if level > 3:
                continue
            indent = "  " * level
            dirname = os.path.basename(root)
            if level == 0:
                lines.append(f"{repo}/")
            else:
                lines.append(f"{indent}{dirname}/")
            subindent = "  " * (level + 1)
            for f in sorted(files):
                if f.startswith(".") and f not in (".gitignore", ".env.example"):
                    continue
                lines.append(f"{subindent}{f}")
        lines.append("```\n")

        # 关键文件内容
        key_files = ["README.md", "package.json", "Cargo.toml", "pyproject.toml", "go.mod", "Makefile", "CLAUDE.md", "AGENTS.md"]
        for kf in key_files:
            kf_path = os.path.join(repo_path, kf)
            if os.path.exists(kf_path):
                lines.append(f"## {kf}\n")
                lines.append("```")
                with open(kf_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    if len(content) > 5000:
                        content = content[:5000] + "\n... (truncated)"
                    lines.append(content)
                lines.append("```\n")

        return "\n".join(lines)


def analyze_repo_overview(repo_path: str) -> str:
    """分析项目概览：类型、用途、入口"""
    lines = []

    # 判断项目类型
    project_type = "unknown"
    entry_points = []

    if os.path.exists(os.path.join(repo_path, "package.json")):
        project_type = "Node.js"
        if os.path.exists(os.path.join(repo_path, "vite.config.ts")) or os.path.exists(os.path.join(repo_path, "vite.config.js")):
            project_type += " (Vite)"
        if os.path.exists(os.path.join(repo_path, "next.config.js")) or os.path.exists(os.path.join(repo_path, "next.config.ts")):
            project_type += " (Next.js)"
    elif os.path.exists(os.path.join(repo_path, "Cargo.toml")):
        project_type = "Rust"
    elif os.path.exists(os.path.join(repo_path, "pyproject.toml")) or os.path.exists(os.path.join(repo_path, "setup.py")):
        project_type = "Python"
    elif os.path.exists(os.path.join(repo_path, "go.mod")):
        project_type = "Go"

    lines.append(f"- **项目类型**: {project_type}")

    # 入口文件
    for entry in ["src/main.ts", "src/main.js", "src/index.ts", "src/index.js", "main.py", "main.go", "src/lib.rs"]:
        if os.path.exists(os.path.join(repo_path, entry)):
            entry_points.append(entry)
    if entry_points:
        lines.append(f"- **入口文件**: {', '.join(entry_points)}")

    # 测试框架
    test_frameworks = []
    if os.path.exists(os.path.join(repo_path, "vitest.config.ts")) or os.path.exists(os.path.join(repo_path, "vitest.config.js")):
        test_frameworks.append("Vitest")
    if os.path.exists(os.path.join(repo_path, "jest.config.js")) or os.path.exists(os.path.join(repo_path, "jest.config.ts")):
        test_frameworks.append("Jest")
    if os.path.exists(os.path.join(repo_path, "Cargo.toml")):
        test_frameworks.append("cargo test")
    if os.path.exists(os.path.join(repo_path, "pyproject.toml")):
        test_frameworks.append("pytest")
    if test_frameworks:
        lines.append(f"- **测试框架**: {', '.join(test_frameworks)}")

    return "\n".join(lines)


def detect_tech_stack(repo_path: str) -> str:
    """检测技术栈"""
    lines = []
    deps = set()

    # package.json
    pkg_path = os.path.join(repo_path, "package.json")
    if os.path.exists(pkg_path):
        try:
            import json
            with open(pkg_path) as f:
                pkg = json.load(f)
            for dep_type in ["dependencies", "devDependencies"]:
                if dep_type in pkg:
                    deps.update(pkg[dep_type].keys())
        except Exception:
            pass

    # 框架检测
    frameworks = {
        "react": "React",
        "vue": "Vue",
        "svelte": "Svelte",
        "next": "Next.js",
        "nuxt": "Nuxt",
        "express": "Express",
        "koa": "Koa",
        "fastify": "Fastify",
        "tailwindcss": "Tailwind CSS",
        "typescript": "TypeScript",
        "vite": "Vite",
        "webpack": "Webpack",
    }
    detected = [name for dep, name in frameworks.items() if any(dep in d.lower() for d in deps)]
    if detected:
        lines.append(f"- **框架/库**: {', '.join(detected)}")

    # 语言
    languages = []
    for ext, lang in [(".ts", "TypeScript"), (".tsx", "TypeScript/JSX"), (".js", "JavaScript"), (".py", "Python"), (".rs", "Rust"), (".go", "Go")]:
        if any(f.endswith(ext) for f in os.listdir(repo_path) if os.path.isfile(os.path.join(repo_path, f))):
            languages.append(lang)
    # 检查 src 目录
    src_path = os.path.join(repo_path, "src")
    if os.path.isdir(src_path):
        for root, dirs, files in os.walk(src_path):
            for f in files:
                for ext, lang in [(".ts", "TypeScript"), (".tsx", "TypeScript/JSX"), (".js", "JavaScript"), (".py", "Python"), (".rs", "Rust"), (".go", "Go")]:
                    if f.endswith(ext) and lang not in languages:
                        languages.append(lang)
            break
    if languages:
        lines.append(f"- **语言**: {', '.join(languages)}")

    if not lines:
        lines.append("- 无法自动检测，请查看关键文件")

    return "\n".join(lines)


def count_repo_stats(repo_path: str) -> str:
    """统计项目规模"""
    total_files = 0
    total_lines = 0
    code_lines = 0
    ext_count = {}

    skip_dirs = {".git", "node_modules", "dist", "build", ".next", ".venv", "venv", "__pycache__"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.startswith("."):
                continue
            total_files += 1
            ext = os.path.splitext(f)[1] or "(no ext)"
            ext_count[ext] = ext_count.get(ext, 0) + 1

            fpath = os.path.join(root, f)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                    lines = content.split("\n")
                    total_lines += len(lines)
                    code_lines += sum(1 for l in lines if l.strip() and not l.strip().startswith("//") and not l.strip().startswith("#"))
            except Exception:
                pass

    lines = []
    lines.append(f"- **文件总数**: {total_files}")
    lines.append(f"- **代码行数**: {code_lines} / {total_lines} (含空行/注释)")

    # 主要文件类型
    top_exts = sorted(ext_count.items(), key=lambda x: x[1], reverse=True)[:5]
    if top_exts:
        ext_str = ", ".join(f"{ext} ({count})" for ext, count in top_exts)
        lines.append(f"- **主要文件类型**: {ext_str}")

    return "\n".join(lines)


def slugify(text: str, max_len: int = 60) -> str:
    """从文本生成文件名 slug，优先保留 ASCII"""
    # 移除非 ASCII 字符（中文等），只保留英文、数字、连字符
    text = re.sub(r"[^\x00-\x7f]", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text).strip("-")
    return text[:max_len].lower()


def get_slug_from_url(url: str) -> str:
    """从 URL 提取 slug"""
    path = urlparse(url).path.rstrip("/")
    if path:
        last = path.split("/")[-1]
        # 去掉扩展名
        last = re.sub(r"\.[a-z]+$", "", last)
        if last:
            return slugify(last)
    return "untitled"


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


def build_source_header(url: str, source_type: str, title: str) -> str:
    """生成来源头"""
    today = date.today().isoformat()
    return f"""<!--
source: {url}
type: {source_type}
fetched: {today}
-->

"""


def is_youtube_url(url: str) -> bool:
    """判断是否是 YouTube 视频 URL"""
    parsed = urlparse(url)
    return parsed.netloc in ("www.youtube.com", "youtube.com", "youtu.be")


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
    args = parser.parse_args()

    url = args.url
    source_type = args.type

    # 确定保存路径
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_dir = os.path.join(repo_root, "raw", "sources")
    os.makedirs(sources_dir, exist_ok=True)

    today = date.today().isoformat()

    # YouTube 视频：获取字幕
    if is_youtube_url(url):
        print(f"YouTube 视频: {url}")
        slug = get_slug_from_url(url)
        base_name = f"{today}-{slug}"
        md_path = os.path.join(sources_dir, f"{base_name}.md")

        try:
            transcript, title = fetch_youtube_transcript(url)
            header = build_source_header(url, "video", title)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + f"# {title}\n\n" + transcript)
            print(f"已保存字幕: {md_path}")
        except Exception as e:
            print(f"获取字幕失败: {e}")
            header = build_source_header(url, "video", slug)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + f"# {slug}\n\n[获取字幕失败，请手动查看视频]({url})")
            print(f"已保存占位文件: {md_path}")

        print(f"\n类型: video")
        return

    # X 推文线程
    if is_x_url(url):
        print(f"X 推文: {url}")
        slug = get_slug_from_url(url)
        base_name = f"{today}-{slug}"
        md_path = os.path.join(sources_dir, f"{base_name}.md")

        try:
            thread = fetch_x_thread(url)
            header = build_source_header(url, "tweet", slug)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + thread)
            print(f"已保存推文: {md_path}")
        except Exception as e:
            print(f"抓取失败: {e}")
            header = build_source_header(url, "tweet", slug)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + f"[抓取失败，请手动复制推文内容]({url})")
            print(f"已保存占位文件: {md_path}")

        print(f"\n类型: tweet")
        return

    # GitHub 仓库：clone 分析结构，失败则回退到 README
    if is_github_repo(url):
        print(f"GitHub 仓库: {url}")
        slug = get_slug_from_url(url)
        base_name = f"{today}-{slug}"
        md_path = os.path.join(sources_dir, f"{base_name}.md")

        try:
            print("正在 clone 并分析仓库...")
            analysis = analyze_github_repo(url)
            header = build_source_header(url, "repo", slug)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + analysis)
            print(f"已保存仓库分析: {md_path}")
        except Exception as e:
            print(f"clone 分析失败 ({e})，回退到抓取 README...")
            readme_content, repo_name = fetch_github_readme(url)
            header = build_source_header(url, "repo", repo_name)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(header + readme_content)
            print(f"已保存 README: {md_path}")

        print(f"\n类型: repo")
        return

    # 普通网页：抓取 HTML 并转 Markdown
    print(f"抓取: {url}")
    html = fetch(url)

    # 提取标题
    title = extract_title(html)
    # 优先用 URL 的 slug，标题作为备选
    slug = get_slug_from_url(url) or slugify(title)
    base_name = f"{today}-{slug}"

    html_path = os.path.join(sources_dir, f"{base_name}.html")
    md_path = os.path.join(sources_dir, f"{base_name}.md")

    # 保存 HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"已保存 HTML: {html_path}")

    # 转换并保存 Markdown
    md = html_to_markdown(html)
    header = build_source_header(url, source_type, title)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(header + md)
    print(f"已保存 Markdown: {md_path}")

    print(f"\n标题: {title}")
    print(f"类型: {source_type}")


if __name__ == "__main__":
    main()
