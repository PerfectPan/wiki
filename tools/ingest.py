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


def main():
    parser = argparse.ArgumentParser(description="抓取网页并存入 raw/sources/")
    parser.add_argument("url", help="网页 URL 或 GitHub 仓库 URL")
    parser.add_argument("--type", default="blog", choices=["blog", "doc", "repo"], help="来源类型")
    args = parser.parse_args()

    url = args.url
    source_type = args.type

    # 确定保存路径
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_dir = os.path.join(repo_root, "raw", "sources")
    os.makedirs(sources_dir, exist_ok=True)

    today = date.today().isoformat()

    # GitHub 仓库：抓取 README
    if is_github_repo(url):
        print(f"GitHub 仓库: {url}")
        readme_content, repo_name = fetch_github_readme(url)
        slug = slugify(repo_name.replace("/", "-"))
        base_name = f"{today}-{slug}"
        md_path = os.path.join(sources_dir, f"{base_name}.md")

        header = build_source_header(url, "repo", repo_name)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(header + readme_content)
        print(f"已保存 README: {md_path}")
        print(f"\n仓库: {repo_name}")
        print(f"类型: repo")
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
