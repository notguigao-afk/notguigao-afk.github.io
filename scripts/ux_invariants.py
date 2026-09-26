#!/usr/bin/env python3
"""Build-output invariants for /dev/null. Run from repo root after `hugo`."""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
CSS_DIR = ROOT / "assets" / "css" / "extended"
failures: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def read(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file: {path}")
        return ""
    return path.read_text(encoding="utf-8")


def homepage_css() -> str:
    return read(CSS_DIR / "homepage.css")


def check_dark_token_bridge() -> None:
    css = homepage_css()
    if "html:root[data-theme=\"dark\"]" not in css and "html:root[data-theme='dark']" not in css:
        fail('homepage.css must re-bridge tokens on html:root[data-theme="dark"]')
    # Inside a dark :root rule, --theme must map back to the impressionist canvas.
    if not re.search(
        r"html:root\[data-theme=[\"']dark[\"']\]\s*\{[^}]*--theme:\s*var\(--imp-canvas\)",
        css,
        re.S,
    ):
        fail("dark html:root must set --theme: var(--imp-canvas)")
    if not re.search(
        r"html:root\[data-theme=[\"']auto[\"']\]\s*\{[^}]*--theme:\s*var\(--imp-canvas\)",
        css,
        re.S,
    ):
        fail("auto+prefers-dark html:root must set --theme: var(--imp-canvas)")


def public_html(rel: str) -> str:
    return read(PUBLIC / rel)


def check_skip_link() -> None:
    home = public_html("index.html")
    if 'class="skip-link"' not in home and "class='skip-link'" not in home:
        fail("home missing skip-link")
    if 'href="#main"' not in home:
        fail("skip-link must point at #main")
    if "跳到正文" not in home:
        fail("skip-link label must be 跳到正文")
    if not re.search(r"<main[^>]*id=\"main\"", home):
        fail("<main> must have id=main")


def check_header_a11y() -> None:
    home = public_html("index.html")
    if 'title="切换主题 (Alt + T)"' not in home:
        fail("theme toggle title must be 切换主题 (Alt + T)")
    css = read(CSS_DIR / "nav-tabs.css")
    if not re.search(
        r"\.site-header__brand-link\s*\{[^}]*min-height:\s*44px",
        css,
        re.S,
    ):
        fail("brand link must declare min-height: 44px")
    labels = read(CSS_DIR / "homepage.css") + read(CSS_DIR / "tab-panels.css")
    if re.search(r"font-size:\s*0\.72rem", labels):
        fail("UI labels must not use 0.72rem (<12px); use 0.75rem or larger")


def check_footer_zh() -> None:
    home = public_html("index.html")
    if "Powered by" in home:
        fail("footer must not use English Powered by")
    # Credit wraps Hugo/PaperMod in <a>; match the visible phrase.
    visible = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", home))
    if "用 Hugo 与 PaperMod 生成" not in visible:
        fail("footer must use 用 Hugo 与 PaperMod 生成")
    if 'aria-label="回到顶部"' not in home:
        fail("top-link aria-label must be 回到顶部")
    if "https://gohugo.io/?utm_source=papermod" not in home:
        fail("keep official Hugo credit URL")
    if "https://github.com/adityatelange/hugo-PaperMod/" not in home:
        fail("keep official PaperMod credit URL")


def check_404() -> None:
    page = public_html("404.html")
    if "<h1" not in page:
        fail("404 must have an h1")
    if "没有这一页" not in page:
        fail("404 h1/copy must include 没有这一页")
    if 'href="/categories/essays/"' not in page and 'href="/categories/essays"' not in page:
        fail("404 must link to essays")
    if re.search(r'class="not-found"', page) and "没有这一页" not in page:
        fail("do not ship PaperMod empty 404 numeral-only page")


def check_index_titles() -> None:
    tags = public_html("tags/index.html")
    cats = public_html("categories/index.html")
    posts = public_html("posts/index.html")
    if "<h1" in tags and "Tags" in tags and "标签" not in tags:
        fail("tags index still uses English Tags")
    if "标签" not in tags:
        fail("tags index must say 标签")
    if "分类" not in cats:
        fail("categories index must say 分类")
    if "文章" not in posts:
        fail("posts index must say 文章")
    if "class=\"terms-tags\"" in tags:
        fail("tags index must not use PaperMod terms-tags chips")


def check_wayfinding() -> None:
    home = public_html("index.html")
    about = public_html("about/index.html")
    for slug in ("essays", "gleanings", "moments"):
        if f"/categories/{slug}/" not in home:
            fail(f"sidebar must link to /categories/{slug}/")
    if "LMArena" in about or "Elo" in about:
        fail("about colophon must not include LMArena/Elo ranking")
    match = re.search(r'<ul class="about-map">(.*?)</ul>', about, re.S)
    if not match:
        fail("about page must include an about-map list")
    else:
        amap = match.group(1)
        for slug in ("essays", "gleanings", "moments"):
            if f"/categories/{slug}/" not in amap:
                fail(f"about map must link to /categories/{slug}/")


def check_polish() -> None:
    css = read(CSS_DIR / "tab-panels.css")
    if ".site-prose .paginav" not in css:
        fail("override .site-prose .paginav so next/prev titles do not wrap orphan glyphs")
    home = public_html("index.html")
    if "最近写下的" not in home or 'href="/posts/"' not in home:
        fail("homepage must expose recent writing and the full archive")
    notes = read(ROOT / "docs" / "brand-notes.md")
    if "html:root" not in notes:
        fail("brand-notes must document html:root dark bridge")


def check_annotations() -> None:
    data = tomllib.loads(read(ROOT / "data" / "annotations.toml"))
    posts = data.get("posts", {})
    authors = data.get("authors", {})
    for path in (ROOT / "content" / "posts").glob("*.md"):
        if path.stem == "_index":
            continue
        source = read(path)
        metadata = tomllib.loads(source.split("+++", 2)[1])
        if metadata.get("draft", False):
            continue
        entry = posts.get(path.stem, {})
        if not entry.get("text", "").strip():
            fail(f"missing reviewed annotation: {path.stem}")
            continue
        author = authors.get(entry.get("author"), {})
        if not all(author.get(k) for k in ("name", "model", "effort")):
            fail(f"incomplete annotation signature: {path.stem}")
        # Match current flat post paths; front matter may override the filename slug.
        slug = metadata.get("slug", path.stem)
        page = public_html(f"posts/{slug}/index.html")
        if page.count('aria-label="AI 边批"') != 1:
            fail(f"post must render exactly one AI annotation: {slug}")
        for value in (entry["text"], author.get("model", ""), author.get("effort", "")):
            if value not in page:
                fail(f"annotation text/signature missing from {slug}")


CHECKS = [
    check_dark_token_bridge,
    check_skip_link,
    check_header_a11y,
    check_footer_zh,
    check_404,
    check_index_titles,
    check_wayfinding,
    check_polish,
    check_annotations,
]


def main() -> int:
    for fn in CHECKS:
        fn()
    if failures:
        print("ux_invariants: FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("ux_invariants: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
