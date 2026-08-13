# Unify Site Chrome Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 PaperMod 未覆盖的边角（暗色漏缝、404、标签/分类/文章索引、页脚）收进现有 Water Lilies 编辑部语言，并补齐 skip-link、触控区和标签字号等可访问性缺口。

**Architecture:** 不改 PaperMod 主题源文件。用站点级 override（`layouts/`、`assets/css/extended/`、`content/*/_index.md`）盖住默认页；暗色必须用比主题更高的选择器 `html:root[data-theme="dark"]` 把 `--theme` 等变量重新桥到 `--imp-*`。每项改动先写入 `scripts/ux_invariants.py` 断言，再改产物，最后 `hugo` 构建验证。

**Tech Stack:** Hugo ≥0.146 extended、PaperMod（submodule，只读）、站点 CSS（`assets/css/extended/*.css`）、Python 3 标准库做 HTML/CSS 不变量检查。不要引入新前端框架、不要加订阅表单、不要改成 Swiss/粉红 CTA。

## Global Constraints

- UI 文案默认中文；站点名保持 `/dev/null`；URL 只用英文 slug（`essays`、`gleanings`、`moments`、`tags`…）。见 `docs/brand-notes.md`。
- 色板保持 Water Lilies：`--imp-canvas #e8f2ef`、`--imp-ink #142422`、`--imp-sage #2f8f86` 及已有暗色对应值。禁止引入粉红 CTA 或黑白瑞士默认盘。
- 正文对比度 ≥4.5:1；交互热区 ≥44×44px；焦点只用 `:focus-visible`；尊重 `prefers-reduced-motion`。
- 不修改 `themes/PaperMod/**`。只新增/改站点根下的 `layouts/`、`assets/`、`content/`、`scripts/`、`docs/`。
- 保留 Hugo 与 PaperMod 的页脚链接（主题要求）；只把英文 “Powered by” 改成中文，不删链接。
- 不改文章正文内容。关于页 colophon 去掉 LMArena/Elo 排名，留一句安静的搭建说明。
- 验证命令以仓库根为 cwd。先 `hugo --destination public`（或 `-D` 若需草稿），再跑 `python3 scripts/ux_invariants.py`。
- 执行本计划时，把本文件同时落到 `docs/superpowers/plans/2026-08-13-unify-site-chrome.md`（仓库内可检索副本）。

## File map

| File | Responsibility |
|------|----------------|
| `scripts/ux_invariants.py` | 构建后 HTML/CSS 不变量。每个 Task 往里加断言，先红后绿。 |
| `assets/css/extended/homepage.css` | 原始色 token、暗色桥、Hero 水晕。 |
| `assets/css/extended/nav-tabs.css` | skip-link、品牌热区、主题按钮 title 的配套样式。 |
| `assets/css/extended/typography.css` | 页脚/标签最小字号（≥12px）。 |
| `assets/css/extended/tab-panels.css` | 索引列表、404、关于地图链接、分页块、colophon。 |
| `layouts/baseof.html` | 站点级骨架：`#main` + skip-link。从主题复制后只改这两处。 |
| `layouts/_partials/header.html` | 主题按钮完整 `title`。 |
| `layouts/_partials/footer.html` | 中文页脚 + 中文回顶 + 44px 回顶（整文件从主题复制后改文案与尺寸 class）。 |
| `layouts/404.html` | 中文 404 + 恢复链接。 |
| `layouts/taxonomy.html` | `/tags/`、`/categories/` 用 `tab-panel` 语言。 |
| `content/posts/_index.md` | 栏目标题「文章」。 |
| `content/tags/_index.md` | 标题「标签」。 |
| `content/categories/_index.md` | 标题「分类」。 |
| `data/topics.yaml` | 三张入口卡 accent（拉开明度）。 |
| `layouts/_partials/home_entry.html` | 色条形态：实线 / 双段 / 虚线。 |
| `content/about.md` | 「这里」三项改成真链接；缩短 colophon。 |
| `docs/brand-notes.md` | 补一句：索引页中文标题、暗色必须 `html:root` 桥接。 |

---

### Task 1: 不变量脚本 + 暗色 token 再桥接

**Files:**
- Create: `scripts/ux_invariants.py`
- Modify: `assets/css/extended/homepage.css`（`html[data-theme="dark"]` 块约 L57–L88）
- Test: `scripts/ux_invariants.py`（本任务只启用暗色桥接相关断言）

**Interfaces:**
- Consumes: 现有 `--imp-*` 原始量；PaperMod `themes/PaperMod/assets/css/core/theme-vars.css` 里的 `:root[data-theme="dark"]`（`--theme: rgb(29, 30, 32)`，选择器特异度 0,2,0）。
- Produces: `html:root[data-theme="dark"]` 与 `html:root[data-theme="auto"]`（在 `prefers-color-scheme: dark` 内）重新赋值 `--theme`、`--entry`、`--primary`、`--secondary`、`--content`、`--border`、`--code-bg`、`--tertiary` 为 `var(--imp-*)`。`check_dark_token_bridge()` 供后续任务继续调用。

**Why this selector:** `html[data-theme="dark"]` 特异度是 0,1,1，**赢不了** `:root[data-theme="dark"]`（0,2,0）。必须写成 `html:root[data-theme="dark"]`（0,2,1）。`[data-theme="dark"] .list { background: var(--theme) }` 也会因此吃到池塘底色，消掉首页右侧灰带。

- [ ] **Step 1: 写会失败的不变量脚本**

创建 `scripts/ux_invariants.py`，全文如下（后续任务只追加函数，不改这段骨架）：

```python
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


CHECKS = [check_dark_token_bridge]


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
```

- [ ] **Step 2: 跑脚本，确认失败**

Run: `python3 scripts/ux_invariants.py`

Expected: exit 1，至少包含 `html:root[data-theme="dark"]` 与 `--theme: var(--imp-canvas)` 两条失败。

- [ ] **Step 3: 改暗色块**

在 `assets/css/extended/homepage.css` 把现有：

```css
html[data-theme="dark"] {
  --imp-canvas: #0e1716;
  /* …其余 --imp-* 保持不动… */
  --imp-border: #2a4a45;
}
```

改成（`--imp-*` 值一字不改，只加选择器前缀和桥接）：

```css
html:root[data-theme="dark"] {
  --imp-canvas: #0e1716;
  --imp-mist: #1a3330;
  --imp-water: #3d8a84;
  --imp-aqua: #2f6b64;
  --imp-pad: #3d7a68;
  --imp-lilac: var(--imp-water);
  --imp-rose: var(--imp-aqua);
  --imp-gold: var(--imp-pad);
  --imp-sage: #5ec4b8;
  --imp-ink: #e6f5f2;
  --imp-ink-muted: #8fb5ae;
  --imp-surface: #152422;
  --imp-border: #2a4a45;

  --theme: var(--imp-canvas);
  --entry: var(--imp-surface);
  --primary: var(--imp-ink);
  --secondary: var(--imp-ink-muted);
  --content: var(--imp-ink);
  --border: var(--imp-border);
  --code-bg: color-mix(in srgb, var(--imp-mist) 55%, var(--imp-surface));
  --tertiary: color-mix(in srgb, var(--imp-border) 80%, var(--imp-mist));
}
```

同步改 `@media (prefers-color-scheme: dark)` 里的 `html[data-theme="auto"]` 为 `html:root[data-theme="auto"]`，并加上同一组 `--theme`…`--tertiary` 桥接。不要删浅色 `:root` 里已有的桥接。

- [ ] **Step 4: 再跑脚本，确认通过**

Run: `python3 scripts/ux_invariants.py`

Expected: `ux_invariants: OK`

- [ ] **Step 5: 构建确认无 Hugo 报错**

Run: `hugo --destination public`

Expected: exit 0。

- [ ] **Step 6: Commit**

```bash
git add scripts/ux_invariants.py assets/css/extended/homepage.css
git commit -m "fix(theme): re-bridge PaperMod dark tokens via html:root"
```

---

### Task 2: Skip link 与 `main` 地标

**Files:**
- Create: `layouts/baseof.html`（从 `themes/PaperMod/layouts/baseof.html` 复制）
- Modify: `assets/css/extended/nav-tabs.css`（文件末尾追加）
- Modify: `scripts/ux_invariants.py`（追加 `check_skip_link`）

**Interfaces:**
- Consumes: 主题 `baseof.html` 的 `data-theme` / `partialCached header/footer` 结构；body 已有 `id="top"`。
- Produces: 每个页面第一个可聚焦控件是 `<a class="skip-link" href="#main">跳到正文</a>`；`<main class="main" id="main">`。主题 footer 里已有的 `a[href^="#"]` 平滑滚动会作用到 `#main`，这是期望行为。

- [ ] **Step 1: 先加会失败的断言**

在 `scripts/ux_invariants.py` 的 `CHECKS` 列表加入 `check_skip_link`，函数：

```python
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
```

- [ ] **Step 2: 构建再跑，确认失败**

Run:

```bash
hugo --destination public && python3 scripts/ux_invariants.py
```

Expected: FAIL，`home missing skip-link`（暗色桥接断言仍应通过）。

- [ ] **Step 3: 覆盖 baseof**

复制 `themes/PaperMod/layouts/baseof.html` 到 `layouts/baseof.html`。只改 body 内开头与 main 标签，其余（版本检查、`data-theme`、`partialCached` 参数）保持原样：

```html
<body class="list" id="top">
    <a class="skip-link" href="#main">跳到正文</a>
    {{ partialCached "header.html" . .Page -}}
    <main class="main" id="main">
```

非 list 的 `body id="top"` 分支同样加上 skip-link，且 `<main class="main" id="main">`。两处都要改，不要只改 list。

- [ ] **Step 4: Skip-link 样式**

追加到 `assets/css/extended/nav-tabs.css` 末尾：

```css
.skip-link {
  position: absolute;
  left: var(--site-gutter, 1.25rem);
  top: 0.75rem;
  z-index: 100;
  padding: 0.55rem 0.85rem;
  min-height: 44px;
  border-radius: 0.35rem;
  background: var(--imp-ink, #142422);
  color: var(--imp-canvas, #e8f2ef);
  font-family: var(--type-body, Georgia, "Noto Serif SC", serif);
  font-size: 0.9375rem;
  text-decoration: none;
  transform: translateY(-150%);
  transition: transform 160ms var(--imp-ease-out, ease);
}

.skip-link:focus {
  transform: translateY(0);
  outline: 2px solid var(--imp-sage, #2f8f86);
  outline-offset: 3px;
}

@media (prefers-reduced-motion: reduce) {
  .skip-link {
    transition: none;
  }
}
```

未聚焦时移出视口，不要用 `display: none`（否则键盘也进不去）。

- [ ] **Step 5: 构建 + 脚本变绿**

Run:

```bash
hugo --destination public && python3 scripts/ux_invariants.py
```

Expected: `ux_invariants: OK`。抽查 `public/posts/zai-ti/index.html` 也含 `skip-link` 与 `id="main"`。

- [ ] **Step 6: Commit**

```bash
git add layouts/baseof.html assets/css/extended/nav-tabs.css scripts/ux_invariants.py
git commit -m "feat(a11y): add skip-to-content link and main landmark"
```

---

### Task 3: 触控区、标签字号、主题按钮 title

**Files:**
- Modify: `layouts/_partials/header.html`（主题按钮，约 L16）
- Modify: `assets/css/extended/nav-tabs.css`（`.site-header__brand-link`，约 L121–L128）
- Modify: `assets/css/extended/homepage.css`（`.home-entry__label`，约 L365–L373）
- Modify: `assets/css/extended/tab-panels.css`（`.about-map-label` 约 L514–L522；`.moments-eyebrow` 约 L877–L885）
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: Task 2 的 header/nav 结构。
- Produces: 品牌链接 min-height 44px；所有 section 小标签 `font-size` ≥ `0.75rem`；主题按钮 `title="切换主题 (Alt + T)"` 且保留 `aria-label="切换主题"`。

- [ ] **Step 1: 加失败断言**

```python
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
```

把 `check_header_a11y` 加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `python3 scripts/ux_invariants.py`

Expected: FAIL，上述三条。

- [ ] **Step 3: 改 markup 与 CSS**

`layouts/_partials/header.html` 主题按钮改为：

```html
<button id="theme-toggle" class="theme-toggle" accesskey="t" title="切换主题 (Alt + T)" aria-label="切换主题">
```

`nav-tabs.css` 的 `.site-header__brand-link` 增加：

```css
min-height: 44px;
display: inline-flex;
align-items: center;
```

（已有 `font-*` / `color` 保留。）

把这三处 `font-size: 0.72rem` 全部改为 `0.75rem`：

- `homepage.css` `.home-entry__label`
- `tab-panels.css` `.about-map-label`
- 若 `.moments-eyebrow` 已是 `0.75rem` 则不动；若仍更小，改为 `0.75rem`

- [ ] **Step 4: 构建 + 脚本变绿**

Run:

```bash
hugo --destination public && python3 scripts/ux_invariants.py
```

Expected: OK。

- [ ] **Step 5: Commit**

```bash
git add layouts/_partials/header.html assets/css/extended/nav-tabs.css assets/css/extended/homepage.css assets/css/extended/tab-panels.css scripts/ux_invariants.py
git commit -m "fix(a11y): 44px brand target, 12px labels, theme toggle title"
```

---

### Task 4: 中文页脚与回顶按钮

**Files:**
- Create: `layouts/_partials/footer.html`（从 `themes/PaperMod/layouts/_partials/footer.html` 复制）
- Modify: `assets/css/extended/nav-tabs.css` 或 `tab-panels.css`（回顶 44px）
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: 主题 footer 的版权逻辑、`extend_footer` hook、主题切换脚本、回顶脚本、代码复制脚本。这些脚本必须原样保留，否则主题按钮会失效。
- Produces: 页脚文案 `用 Hugo 与 PaperMod 生成`（链接 URL 不变）；回顶 `aria-label="回到顶部"`、`title="回到顶部 (Alt + G)"`；`.top-link` 宽高 44px。

- [ ] **Step 1: 加失败断言**

```python
def check_footer_zh() -> None:
    home = public_html("index.html")
    if "Powered by" in home:
        fail("footer must not use English Powered by")
    if "用 Hugo 与 PaperMod 生成" not in home:
        fail("footer must use 用 Hugo 与 PaperMod 生成")
    if 'aria-label="回到顶部"' not in home:
        fail("top-link aria-label must be 回到顶部")
    if "https://gohugo.io/?utm_source=papermod" not in home:
        fail("keep official Hugo credit URL")
    if "https://github.com/adityatelange/hugo-PaperMod/" not in home:
        fail("keep official PaperMod credit URL")
```

加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: FAIL，`Powered by` 仍在。

- [ ] **Step 3: 覆盖 footer**

复制主题 footer 到 `layouts/_partials/footer.html`。只改两处字符串，脚本一块不要动：

把：

```html
    <span>
        Powered by
        <a href="https://gohugo.io/?utm_source=papermod" rel="noopener" target="_blank">Hugo</a> &
        <a href="https://github.com/adityatelange/hugo-PaperMod/" rel="noopener" target="_blank">PaperMod</a>
    </span>
```

换成：

```html
    <span>
        用
        <a href="https://gohugo.io/?utm_source=papermod" rel="noopener" target="_blank">Hugo</a>
        与
        <a href="https://github.com/adityatelange/hugo-PaperMod/" rel="noopener" target="_blank">PaperMod</a>
        生成
    </span>
```

把回顶链接换成：

```html
<a href="#top" id="top-link" class="top-link hidden" aria-label="回到顶部" title="回到顶部 (Alt + G)" accesskey="g">
```

在 `nav-tabs.css` 末尾覆盖尺寸（主题默认 2.5rem = 40px）：

```css
.top-link {
  width: 44px;
  height: 44px;
  min-width: 44px;
  min-height: 44px;
}
```

- [ ] **Step 4: 构建 + 脚本变绿**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。手动点一次主题按钮，确认暗色仍切换（证明复制脚本没丢）。

- [ ] **Step 5: Commit**

```bash
git add layouts/_partials/footer.html assets/css/extended/nav-tabs.css scripts/ux_invariants.py
git commit -m "fix(i18n): Chinese footer credit and top-link label"
```

---

### Task 5: 中文 404，带恢复路径

**Files:**
- Create: `layouts/404.html`
- Modify: `assets/css/extended/tab-panels.css`（追加 `.tab-panel--missing`）
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: Task 2 的 `tab-panel` 外壳类名与 `--site-prose` 栏宽。
- Produces: 404 有一个可见 `h1`「没有这一页」、一句说明、三条链接（首页 `/`、随笔 `/categories/essays/`、关于 `/about/`）。不要再用主题的 `div.not-found` 超大 “404”。

- [ ] **Step 1: 加失败断言**

Hugo 的 404 输出是 `public/404.html`。

```python
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
```

加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: FAIL，缺「没有这一页」。

- [ ] **Step 3: 写 404 模板**

创建 `layouts/404.html`：

```html
{{- define "main" }}
<article class="tab-panel tab-panel--missing">
  <header class="tab-panel__header">
    <h1 class="tab-panel__title">没有这一页</h1>
    <p class="tab-panel__lede">链接可能写错了，或文章已经挪走。</p>
  </header>
  <p class="missing-actions">
    <a href="{{ "/" | relURL }}">回首页</a>
    <a href="{{ "/categories/essays/" | relURL }}">随笔</a>
    <a href="{{ "/about/" | relURL }}">关于</a>
  </p>
</article>
{{- end }}
```

追加样式到 `tab-panels.css`：

```css
.tab-panel--missing .missing-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem 1.25rem;
  margin: 0;
  font-family: var(--tp-font-body);
  font-size: 1.05rem;
}

.tab-panel--missing .missing-actions a {
  display: inline-flex;
  align-items: center;
  min-height: 44px;
  text-underline-offset: 0.18em;
}
```

- [ ] **Step 4: 构建 + 脚本变绿**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。`public/404.html` 能看到三个中文链接，没有孤零零的巨型 404。

- [ ] **Step 5: Commit**

```bash
git add layouts/404.html assets/css/extended/tab-panels.css scripts/ux_invariants.py
git commit -m "feat(404): Chinese recovery page in tab-panel language"
```

---

### Task 6: 标签 / 分类 / 文章索引收进编辑部语言

**Files:**
- Create: `layouts/taxonomy.html`
- Create: `content/posts/_index.md`
- Create: `content/tags/_index.md`
- Create: `content/categories/_index.md`
- Modify: `assets/css/extended/tab-panels.css`（`.index-terms`）
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: `layouts/list.html` 已对 `Kind == section` 调用 `tab_panel_list.html`（所以 `/posts/` 只要 `_index.md` 改标题即可）。`term.html` 已用于单个标签/分类，不要改它的杂志行。
- Produces: `/tags/` 标题「标签」、`/categories/` 标题「分类」、`/posts/` 标题「文章」。三个页面都不再出现英文 `Tags` / `Categories` / `Posts`。索引页用与栏目页相同的 `tab-panel` 头，词条是一行一行的链接（不是 PaperMod 小胶囊）。

- [ ] **Step 1: 加失败断言**

```python
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
```

加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: FAIL（当前 h1 是 Tags / Categories / Posts）。

- [ ] **Step 3: 写三个 _index.md**

`content/posts/_index.md`：

```toml
+++
title = '文章'
description = '全部已发表的笔记。'
+++
```

`content/tags/_index.md`：

```toml
+++
title = '标签'
description = '按话题浏览。'
+++
```

`content/categories/_index.md`：

```toml
+++
title = '分类'
description = '随笔、拾遗、不想上班。'
+++
```

不要给这些索引加进 `hugo.toml` 的 `menu.main`（五个 Tab 保持原样，索引页没有 active Tab 是预期）。

- [ ] **Step 4: 写 taxonomy 模板**

创建 `layouts/taxonomy.html`：

```html
{{- define "main" }}
<div class="tab-panel tab-panel--index">
  <header class="tab-panel__header">
    <h1 class="tab-panel__title">{{ .Title }}</h1>
    {{- with .Description }}
    <p class="tab-panel__lede">{{ . }}</p>
    {{- end }}
  </header>
  <ul class="index-terms">
    {{- $type := .Type }}
    {{- range .Data.Terms.Alphabetical }}
      {{- with site.GetPage (printf "/%s/%s" $type .Name) }}
    <li>
      <a class="index-terms__link" href="{{ .RelPermalink }}">
        <span class="index-terms__name">{{ .LinkTitle }}</span>
        <span class="index-terms__count">{{ .Pages | len }} 篇</span>
      </a>
    </li>
      {{- end }}
    {{- end }}
  </ul>
</div>
{{- end }}
```

追加样式：

```css
.index-terms {
  list-style: none;
  margin: 0;
  padding: 0;
}

.index-terms__link {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  column-gap: 1.5rem;
  align-items: baseline;
  min-height: 44px;
  padding: 0.9rem 0;
  border-bottom: 1px solid color-mix(in srgb, var(--tp-border) 90%, transparent);
  text-decoration: none;
  color: inherit;
}

.index-terms li:first-child .index-terms__link {
  border-top: 1px solid color-mix(in srgb, var(--tp-border) 90%, transparent);
}

.index-terms__name {
  font-family: var(--tp-font-display);
  font-size: 1.2rem;
  font-weight: 600;
}

.index-terms__count {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--tp-muted);
}

.index-terms__link:focus-visible {
  outline: 2px solid var(--tp-sage);
  outline-offset: 4px;
}
```

- [ ] **Step 5: 构建 + 脚本变绿**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。打开 `public/tags/index.html`、`public/categories/index.html`、`public/posts/index.html` 目视：中文标题、杂志行、无 `terms-tags`。

- [ ] **Step 6: Commit**

```bash
git add layouts/taxonomy.html content/posts/_index.md content/tags/_index.md content/categories/_index.md assets/css/extended/tab-panels.css scripts/ux_invariants.py
git commit -m "feat(ia): Chinese taxonomy and posts indexes in tab-panel layout"
```

---

### Task 7: 入口卡可分辨 + 关于页地图可点

**Files:**
- Modify: `data/topics.yaml`
- Modify: `layouts/_partials/home_entry.html`（swatch 加 modifier class）
- Modify: `assets/css/extended/homepage.css`（三种 swatch）
- Modify: `content/about.md`（地图三项包链接；缩短 colophon）
- Modify: `assets/css/extended/tab-panels.css`（`.about-map a`）
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: `home_entry.html` 已有 `--chip-accent` 与 `.home-entry__swatch`；关于页 `.about-map > li` 的 grid 结构。
- Produces: 三个 accent 拉开明度，且色条形态不同（实线 / 双段 / 虚线），不单靠色相。关于「这里」三项分别链到 `/categories/essays/`、`/categories/gleanings/`、`/categories/moments/`。Colophon 只留一句搭建说明，删除 Elo / LMArena / 「约第 33 名」。

锁定的 accent（仍在青绿家族，仅拉开明度）：

| id | accent | swatch |
|----|--------|--------|
| essays | `#1f6f68` | 实心条 `.home-entry__swatch--solid` |
| gleanings | `#3d9a90` | 双段 `.home-entry__swatch--split` |
| moments | `#7eb8a8` | 虚线 `.home-entry__swatch--dash` |

- [ ] **Step 1: 加失败断言**

```python
def check_wayfinding() -> None:
    home = public_html("index.html")
    about = public_html("about/index.html")
    yaml = read(ROOT / "data" / "topics.yaml")
    if "#1f6f68" not in yaml or "#3d9a90" not in yaml or "#7eb8a8" not in yaml:
        fail("topics.yaml must use the three locked accent hex values")
    if "home-entry__swatch--split" not in home or "home-entry__swatch--dash" not in home:
        fail("home chips must expose distinct swatch modifiers")
    if "LMArena" in about or "Elo" in about:
        fail("about colophon must not include LMArena/Elo ranking")
    for slug in ("essays", "gleanings", "moments"):
        if f"/categories/{slug}/" not in about:
            fail(f"about map must link to /categories/{slug}/")
```

加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: FAIL。

- [ ] **Step 3: 改 yaml 与 chip markup**

`data/topics.yaml`：

```yaml
- id: essays
  name: 随笔
  description: 生活与思考
  weight: 1
  accent: "#1f6f68"

- id: gleanings
  name: 拾遗
  description: 学习与经验
  weight: 2
  accent: "#3d9a90"

- id: moments
  name: 不想上班
  description: 碎片念头。不写成随笔的那种。
  weight: 3
  accent: "#7eb8a8"
```

`home_entry.html` 里 swatch 改为按 `id` 分形态：

```html
{{- $swatch := "solid" -}}
{{- if eq $id "gleanings" }}{{ $swatch = "split" }}{{ end -}}
{{- if eq $id "moments" }}{{ $swatch = "dash" }}{{ end -}}
<span class="home-entry__swatch home-entry__swatch--{{ $swatch }}" aria-hidden="true"></span>
```

CSS（加在现有 `.home-entry__swatch` 之后）：

```css
.home-entry__swatch--split {
  background: linear-gradient(
    90deg,
    var(--chip-accent) 0 46%,
    transparent 46% 54%,
    color-mix(in srgb, var(--chip-accent) 55%, var(--imp-mist)) 54% 100%
  );
}

.home-entry__swatch--dash {
  background: repeating-linear-gradient(
    90deg,
    var(--chip-accent) 0 0.55rem,
    transparent 0.55rem 0.85rem
  );
}
```

- [ ] **Step 4: 关于页地图与 colophon**

把 `content/about.md` 里的地图改成：

```html
<p class="about-map-label">这里</p>
<ul class="about-map">
<li><a href="{{ "/categories/essays/" | relURL }}"><strong>随笔</strong><span>生活里冒出来的想法</span></a></li>
<li><a href="{{ "/categories/gleanings/" | relURL }}"><strong>拾遗</strong><span>学过的、捡到的、不想再忘的</span></a></li>
<li><a href="{{ "/categories/moments/" | relURL }}"><strong>不想上班</strong><span>碎片念头，不写成随笔的那种</span></a></li>
</ul>
```

注意：这是 Goldmark + `unsafe = true` 的 HTML 内容页。Hugo 的 `relURL` **不会**在普通 markdown HTML 里执行。写成固定根路径：

```html
<li><a href="/categories/essays/"><strong>随笔</strong><span>生活里冒出来的想法</span></a></li>
<li><a href="/categories/gleanings/"><strong>拾遗</strong><span>学过的、捡到的、不想再忘的</span></a></li>
<li><a href="/categories/moments/"><strong>不想上班</strong><span>碎片念头，不写成随笔的那种</span></a></li>
```

Colophon 整段换成：

```html
<aside class="about-colophon" aria-label="站点说明">
<p class="about-colophon__brand">最初是在终端里搭起来的。</p>
<p class="about-colophon__lede">写得多慢都行。至少页面是自己的。</p>
</aside>
```

删掉 `about-colophon__meta` 那一行排名。

`tab-panels.css` 让地图里的 `a` 继承原来 `li` 的 grid（链接触及整行）：

```css
.about-map > li > a {
  display: contents;
  color: inherit;
  text-decoration: none;
}

.about-map > li:focus-within {
  outline: 2px solid var(--tp-sage);
  outline-offset: 4px;
}
```

`display: contents` 让 `strong`/`span` 仍走父级 grid。若某浏览器对 contents + 焦点不友好，改为让 `a` 自己变成与 `li` 相同的两列 grid，并去掉 `li` 上的 grid（不要两套并存）。以「整行可点、焦点可见、热区 ≥44px」为准。

- [ ] **Step 5: 构建 + 脚本变绿**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。

- [ ] **Step 6: Commit**

```bash
git add data/topics.yaml layouts/_partials/home_entry.html assets/css/extended/homepage.css assets/css/extended/tab-panels.css content/about.md scripts/ux_invariants.py
git commit -m "feat(home): distinct topic chips and linked about map"
```

---

### Task 8: 分页块、浅色 Hero 水晕、品牌笔记

**Files:**
- Modify: `assets/css/extended/tab-panels.css`（`.site-prose .paginav`）
- Modify: `assets/css/extended/homepage.css`（`.home-hero__wash--3` / `--4` 透明度）
- Modify: `docs/brand-notes.md`
- Modify: `scripts/ux_invariants.py`

**Interfaces:**
- Consumes: 主题 `.paginav`（`post-single.css`：50% 宽、大写 title、`--code-bg` 底）。站点已有 `layouts/_partials/post_nav_links.html`（文案「更新 / 更早」）。
- Produces: 文章底部分页不再折成「更早 »」+ 下一行一个字；浅色 Hero 水晕略加强；`docs/brand-notes.md` 记下暗色必须 `html:root` 桥接、索引页中文标题。

- [ ] **Step 1: 加失败断言**

```python
def check_polish() -> None:
    css = read(CSS_DIR / "tab-panels.css")
    if ".site-prose .paginav" not in css:
        fail("override .site-prose .paginav so next/prev titles do not wrap orphan glyphs")
    home_css = homepage_css()
    if not re.search(r"\.home-hero__wash--3\s*\{[^}]*opacity:\s*0\.55", home_css, re.S):
        fail("hero wash 3 opacity should be 0.55")
    if not re.search(r"\.home-hero__wash--4\s*\{[^}]*opacity:\s*0\.40", home_css, re.S):
        fail("hero wash 4 opacity should be 0.40")
    notes = read(ROOT / "docs" / "brand-notes.md")
    if "html:root" not in notes:
        fail("brand-notes must document html:root dark bridge")
```

加入 `CHECKS`。

- [ ] **Step 2: 跑脚本确认失败**

Run: `python3 scripts/ux_invariants.py`

Expected: FAIL。

- [ ] **Step 3: 分页与水晕**

`tab-panels.css` 追加：

```css
.site-prose .paginav {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem 1.25rem;
  background: transparent;
  border: none;
  border-radius: 0;
}

.site-prose .paginav a {
  width: auto;
  min-height: 44px;
  padding: 0.65rem 0;
}

.site-prose .paginav .next,
.site-prose .paginav .prev {
  overflow-wrap: anywhere;
}

.site-prose .paginav .title {
  text-transform: none;
  letter-spacing: 0.02em;
}
```

`homepage.css`：`.home-hero__wash--3` 的 `opacity` 从 `0.42` 改为 `0.55`；`.home-hero__wash--4` 从 `0.28` 改为 `0.40`。不要给 wash 加 parallax，不要动 `prefers-reduced-motion` 块。

- [ ] **Step 4: 更新 brand-notes**

在 `docs/brand-notes.md` 的 Palette 表后追加一小节（不要改现有 token 表）：

```markdown
## Implementation notes

- Dark mode must re-assign PaperMod `--theme` / `--entry` / `--primary` on `html:root[data-theme="dark"]` (higher specificity than the theme's `:root[data-theme="dark"]`).
- Index titles: `/posts/` → 文章, `/tags/` → 标签, `/categories/` → 分类. Do not put these in `menu.main`.
```

- [ ] **Step 5: 构建 + 脚本变绿**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。

- [ ] **Step 6: Commit**

```bash
git add assets/css/extended/tab-panels.css assets/css/extended/homepage.css docs/brand-notes.md scripts/ux_invariants.py
git commit -m "fix(ui): paginav wrap, stronger hero wash, document dark bridge"
```

---

### Task 9: 浏览器回归（交付前）

**Files:**
- 不改代码，除非回归发现回归。修完把对应断言补进 `scripts/ux_invariants.py` 再提交。

**Interfaces:**
- Consumes: Tasks 1–8 的全部产物。
- Produces: 一份过完的人工检查记录（写在最终回复里，不必单独文件）。

- [ ] **Step 1: 本地起站**

Run: `hugo server -D`

Expected: `http://localhost:1313/`。

- [ ] **Step 2: 浅色 1440 走查**

打开并点击：`/`、`/categories/essays/`、`/categories/gleanings/`、`/categories/moments/`、`/about/`、`/posts/zai-ti/`、`/posts/`、`/tags/`、`/categories/`、一个不存在的路径。确认：中文标题、skip-link 聚焦时出现、关于地图可进栏目、404 有三条出路、页脚是「用 Hugo 与 PaperMod 生成」、分页标题不再孤字折行。

- [ ] **Step 3: 暗色 1440**

点主题按钮。首页、关于、一篇正文：画布是池塘绿 `#0e1716` 系，**右侧/页脚不得再露出 PaperMod 灰 `#1d1e20`**。再切回浅色。

- [ ] **Step 4: 375 与 768**

首页芯片单列/三列；随笔杂志行在 375 叠成日期+标题+摘要；导航五 Tab 不横滑；品牌与主题按钮仍 ≥44px。

- [ ] **Step 5: 键盘**

从地址栏 Tab：第一项是「跳到正文」→ 回车落到 `#main`。继续 Tab 经过品牌、主题、五个 Tab、芯片。焦点环始终可见。

- [ ] **Step 6: 不变量最终跑一次**

Run: `hugo --destination public && python3 scripts/ux_invariants.py`

Expected: OK。若 Step 2–5 发现漏洞，先修再提交，不要带着红的脚本结束。

- [ ] **Step 7: 若有修复则提交**

```bash
git add -u
git commit -m "fix(qa): address visual regression from chrome unify"
```

没有修复则跳过本步。

---

## Self-review

**Spec coverage（对照 2026-08-13 UI/UX 评估建议 1–5）**

| 评估项 | Task |
|--------|------|
| 暗色 token 再桥、灰带 | Task 1 |
| 404 / tags / categories / posts / 页脚收进同一语言 | Tasks 4–6 |
| skip-link、品牌热区、12px 标签、主题 title、回顶中文 | Tasks 2–4 |
| 入口卡可分辨、关于地图可点 | Task 7 |
| 分页折行、浅色水晕、colophon 语气 | Tasks 7–8 |
| 375 / 暗色 / 键盘验收 | Task 9 |

**刻意不做（YAGNI）**

- 不改字体栈为 Newsreader + Roboto，不引入 Newsletter 订阅。
- 不把「文章/标签/分类」加进主导航。
- 不改 `themes/PaperMod/**`。
- 不加搜索、不加面包屑（站点只有两层，评估标为 Low）。

**Placeholder scan:** 无 TBD / “implement later” / “similar to Task N”。

**Type consistency:** 脚本入口始终是 `CHECKS` 里的 `check_*` 函数；公共读取器是 `read`、`public_html`、`homepage_css`。暗色选择器名称全计划统一为 `html:root[data-theme="dark"]`。
