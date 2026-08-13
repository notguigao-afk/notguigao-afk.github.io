#!/usr/bin/env python3
"""Build-output invariants for /dev/null. Run from repo root after `hugo`."""
from __future__ import annotations

import re
import sys
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


CHECKS = [check_dark_token_bridge, check_skip_link, check_header_a11y]


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
