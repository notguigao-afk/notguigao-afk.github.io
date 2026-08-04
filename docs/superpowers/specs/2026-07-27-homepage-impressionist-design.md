# Homepage Redesign — Ambient Impressionism (Scheme 3)

**Date:** 2026-07-27  
**Site:** Hugo + PaperMod (`notguigao-afk.github.io`)  
**Status:** Superseded in parts — see `docs/brand-notes.md` (2026-08)

> **What still holds:** full-bleed ambient hero + category entry after hero; no React; reduced-motion; 44px targets; content-first.  
> **What changed since this draft:** palette → Water Lilies cyan/turquoise (not warm lilac/gold paper); type → Georgia + Noto Serif SC (not Fraunces/Source Sans); home IA → hero + 3 topic chips from `data/topics.yaml` (not full recent/topics/about sections); URLs English with Chinese labels.

## 1. Goal

Redesign the **homepage only** so the first impression is an **ambient Impressionist canvas** (light, color haze, soft texture), while the **primary navigation affordance is topic/category entry** placed after the hero. Secondary content is a **slim hero** (title + one-line positioning). No React/shadcn; pure Hugo overrides + CSS.

## 2. Confirmed product decisions

| Axis | Choice |
|------|--------|
| Identity | Hybrid: technical writing primary, personal voice secondary |
| Visual | Ambient Impressionism (A) — atmosphere in color/texture, layout stays clear |
| Hero role | Slim supporting cast (short title + 1–2 lines) |
| Star content | Theme / category navigation |
| Layout scheme | **3 — Full-bleed hero canvas + category strip below** |
| Out of scope (v1) | Latest-posts list on home, newsletter form, profile photo, social icons (unless already in theme header) |

## 3. Skills / principles applied

| Skill | Application on this page |
|-------|---------------------------|
| `frontend-design` | One signature: full-viewport painterly light field; type pairing chosen for this brief, not generic SaaS |
| `ui-ux-pro-max` | Accessible contrast, touch targets ≥44px, no emoji-as-icons, reduced-motion |
| `design-system` | Three-layer tokens: primitive → semantic → component via CSS variables |
| `emil-design-eng` | Animate rarely; ease-out; only transform/opacity; under ~300ms for UI |
| `apple-design` | Size-specific tracking; hierarchy via weight + size + leading; restraint |
| `brand` | Voice: calm, specific, non-salesy; config-driven copy for consistency |
| `ui-styling` | Mobile-first layout; focus rings; semantic HTML |

## 4. Information architecture

```
┌─────────────────────────────────────────┐
│  Site header (PaperMod — keep as-is)    │
├─────────────────────────────────────────┤
│  FULL-BLEED HERO (min-height ~85–100vh) │
│  · painterly background (CSS only)      │
│  · eyebrow (optional short label)       │
│  · display title                        │
│  · one-line positioning + short bio     │
│  · scroll affordance → categories       │
├─────────────────────────────────────────┤
│  CATEGORY STRIP / RAIL                  │
│  · section label                        │
│  · horizontal-or-wrap chips / cards     │
│  · each: name, count, optional blurb    │
├─────────────────────────────────────────┤
│  Site footer (PaperMod — keep as-is)    │
└─────────────────────────────────────────┘
```

- Homepage does **not** list individual posts in v1.
- Clicking a category goes to the taxonomy list page (or custom topic URL).
- Inner pages (post, list) keep PaperMod defaults unless a follow-up task restyles them.

## 5. Visual design

### 5.1 Signature moment

**Full-bleed Impressionist light field** behind the slim hero: layered soft radial color washes (no photos required), subtle film grain/noise at low opacity, no hard card edges in the hero. Reading text sits on a **semi-solid scrim** or uses high-contrast ink so WCAG body contrast holds.

Avoid AI-default clichés: no cream+terracotta default pair alone; no acid-green-on-black terminal look; no dense broadsheet columns.

### 5.2 Color tokens (primitive → semantic)

Primitives (Impressionist-inspired, light-first):

| Token | Hex | Note |
|-------|-----|------|
| `--imp-canvas` | `#F4F0E8` | Warm paper ground |
| `--imp-mist` | `#E8EEF2` | Cool sky mist |
| `--imp-lilac` | `#C4B7D5` | Soft violet haze |
| `--imp-rose` | `#E8B4B8` | Muted rose |
| `--imp-gold` | `#D4A574` | Afternoon light |
| `--imp-sage` | `#9BB7A5` | Foliage note |
| `--imp-ink` | `#1C1917` | Primary text |
| `--imp-ink-muted` | `#57534E` | Secondary text |
| `--imp-surface` | `#FFFCF8` | Scrim / chip surface |
| `--imp-border` | `#E7E0D6` | Soft borders |

Semantic:

| Role | Maps to |
|------|---------|
| `--color-background` | canvas / layered washes |
| `--color-foreground` | ink |
| `--color-muted-foreground` | ink-muted |
| `--color-accent` | sage or gold (links, focus ring accent) |
| `--color-chip-bg` | surface |
| `--color-chip-border` | border |

Dark mode (v1 minimum): either inherit PaperMod toggle with overridden home tokens (deeper canvas `#1A1816`, lighter ink, softer washes) **or** force light home if contrast of washes fails QA. Prefer supporting PaperMod’s existing theme toggle.

### 5.3 Typography

| Role | Face | Usage |
|------|------|--------|
| Display | **Fraunces** (or **Newsreader** if Fraunces load fails) | Hero title only |
| Body / UI | **Source Sans 3** | Bio, labels, chips, section titles |
| Meta | Same as UI, smaller, tracking slightly open | counts, eyebrows |

Scale (fluid):

- Hero title: `clamp(2.25rem, 5vw, 3.75rem)`, line-height ~1.1, tracking ~`-0.02em`
- Bio: `1.05–1.125rem`, line-height 1.6
- Section label: `0.75–0.8125rem`, uppercase or small-caps optional, letter-spacing `0.08em`
- Chip label: `0.9375–1rem`, weight 500–600

Load fonts via `layouts/partials/extend_head.html` (Google Fonts or self-host later). `font-display: swap`.

### 5.4 Motion (emil / apple)

| Interaction | Behavior |
|-------------|----------|
| First paint | Optional one-time soft fade-in of hero text (opacity only, ~250ms ease-out) |
| Scroll cue | Gentle opacity pulse **only if** `prefers-reduced-motion: no-preference` |
| Category chip hover | `transform: translateY(-2px)` + border/color, 150–200ms ease-out; gate hover with `@media (hover: hover)` |
| Chip active | `scale(0.97)` ~120ms |
| Never | Parallax on large layers; animating layout width/height; motion on every scroll item |

### 5.5 Layout & responsive

- Hero: full viewport width; content max-width ~40–42rem, left-aligned or slightly offset (not dead-center brochure) for editorial feel; vertical center or upper-third balance.
- Category rail: full-width section with max-width container (~72rem); chips wrap on small screens; on wide screens prefer single row with wrap.
- Breakpoints: mobile-first; verify 375 / 768 / 1024 / 1440.
- Touch: chips min height 44px, gap ≥8px.

## 6. Content model

### 6.1 Config-driven hero (`hugo.toml`)

```toml
[params.homeHero]
  eyebrow = "笔记 · 工程 · 生活"
  title = "在光线里写代码"   # placeholder until user finalizes
  subtitle = "技术为主，也留下一点个人温度。"
  # optional longer bio (markdown allowed via RenderString)
  bio = ""
```

Fallback if empty: site `title` + existing `params.homeInfoParams` fields for backward compatibility.

### 6.2 Categories / topics

**Primary source:** `data/topics.yaml` so each topic can carry color, description, and link without waiting for many posts.

```yaml
# data/topics.yaml
- id: engineering
  name: 工程
  description: 构建、调试与系统笔记
  weight: 1
  accent: "#9BB7A5"
  url: "/categories/engineering/"   # or /tags/...
- id: essays
  name: 随笔
  description: 更慢一点的想法
  weight: 2
  accent: "#C4B7D5"
  url: "/categories/essays/"
```

**Fallback:** if `data/topics.yaml` missing, derive from site taxonomies (`categories` preferred, else `tags`), generate chips with name + count + taxonomy permalink; assign accents from a rotating palette.

Posts should use matching `categories` / `tags` over time so links resolve. Empty taxonomy pages are acceptable initially (Hugo may 404 until content exists — prefer linking only topics that exist **or** document that user must create section stubs).

**v1 rule:** Show all entries from `topics.yaml`; if URL 404 risk, link to `#` only when count is 0 and show count `0` — better: create minimal category content or use `url` only when taxonomy term exists. Implementation should skip broken links or use `relPermalink` from real terms when matched by name.

## 7. Technical architecture (Hugo)

### 7.1 Override strategy (do not fork PaperMod core)

| File | Purpose |
|------|---------|
| `layouts/index.html` | Custom home `main` only (or `layouts/home.html` if theme version supports it; PaperMod uses `list.html` + home checks — prefer overriding via `layouts/index.html` defining full page **or** `layouts/_default/list.html` carefully). **Chosen:** `layouts/index.html` that extends theme `baseof` if possible; if PaperMod lacks home-specific base, override `layouts/list.html` with `if .IsHome` branch that renders new partials, else `{{ partial "…" }}` to theme behavior — **safer:** `layouts/partials/home_custom.html` + copy minimal structure in `layouts/index.html` using theme baseof. |
| `layouts/_partials/home_hero.html` | Slim hero markup |
| `layouts/_partials/home_topics.html` | Category strip |
| `layouts/_partials/extend_head.html` | Fonts + home CSS hook |
| `assets/css/extended/homepage.css` | Tokens + hero + chips (PaperMod loads `assets/css/extended/*`) |
| `data/topics.yaml` | Topic definitions |
| `hugo.toml` | `params.homeHero`, keep `theme = PaperMod` |

PaperMod loads extended CSS from project `assets/css/extended/` — confirmed theme pattern.

### 7.2 Disable conflicting home partials

- Stop using default `homeInfoParams` block **or** leave it unused once custom index ignores `home_info.html`.
- Do not enable `profileMode` on home.

### 7.3 Accessibility checklist

- Real heading order: one `h1` in hero; section uses `h2`.
- Chip links: clear accessible names (topic name + count in text or `aria-label`).
- Focus visible: outline using accent ring, not outline:none.
- Contrast: body text ≥4.5:1 on scrim; large title ≥3:1.
- `prefers-reduced-motion` and `prefers-reduced-transparency` fallbacks (solid background if needed).

## 8. Copy / voice (defaults)

Tone: quiet, specific, hybrid engineer-writer. Chinese primary (site `languageCode = zh-cn`).

Placeholders until user edits config:

- Title: 可沿用站点名「我的个人博客」或更鲜明的短句（实现时用 config，便于改）
- Subtitle: 「技术笔记为主，也记录一点生活里的光。」

No emoji icons in UI chrome; hero may keep one textual glyph only if user insists (prefer none).

## 9. Non-goals / out of scope

- Redesigning post single templates, archive, search
- CMS, comments, analytics
- Photo uploads / generative art assets (CSS-only background in v1)
- English i18n
- Forcing commit of `public/` (CI builds with Hugo Actions)

## 10. Success criteria

1. Local `hugo server`: home shows full-bleed Impressionist hero + topic strip; no default PaperMod home-info card stack as primary.
2. Categories/topics navigate correctly for defined topics.
3. Lighthouse-ish basics: no horizontal scroll at 375px; focus visible; reduced-motion respected.
4. Production deploy via existing GitHub Actions still passes (Hugo ≥0.146).
5. User can change hero text and topics without editing HTML (toml + yaml only).

## 11. Implementation phases

1. Tokens + `homepage.css` extended styles  
2. `data/topics.yaml` + partials  
3. Home layout override wiring  
4. Config copy + disable old home info  
5. Visual QA light/dark + reduced motion  
6. Optional: push deploy after user approval  

## 12. Open items for user (non-blocking)

Can ship with placeholders; better if user provides:

- Final display name / hero title / subtitle  
- Final topic list (names, descriptions, preferred URLs)  
- Whether dark mode home should match the painterly theme or stay closer to PaperMod default  

---

**Self-review notes:** No TBD blockers for implementation; placeholders are explicit config keys. Scope is homepage-only. Category link resolution strategy is defined (yaml primary, taxonomy fallback).
