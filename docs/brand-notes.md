# Brand notes — `/dev/null`

Short source of truth for display language, palette, and type. Supersedes warm-impressionist details in the 2026-07-27 homepage spec where they conflict.

## Language

| Layer | Rule |
|-------|------|
| UI labels, posts, about | **Chinese** by default |
| Site title | `/dev/null` (technical metaphor, intentional English) |
| URLs | English slugs only (`essays`, `gleanings`, `moments`, tags…) |
| Hero quote | English **epigraph** (intentional); Chinese **tagline** orients the reader |

Do not mix Chinese into paths or English into primary nav labels.

## Palette — Water Lilies

Cool green-white paper + pond teal ink + turquoise accents.

| Token | Role | Light (approx.) |
|-------|------|-----------------|
| `--imp-canvas` | Page ground | `#e8f2ef` |
| `--imp-surface` | Cards / chrome | `#f4faf8` |
| `--imp-ink` | Body text | `#142422` |
| `--imp-ink-muted` | Meta / secondary | `#2f4a45` |
| `--imp-sage` | Links, focus, accent | `#2f8f86` |
| `--imp-water` | Mid water (was lilac) | `#5eb0aa` |
| `--imp-aqua` | Shallow (was rose) | `#8ec9c0` |
| `--imp-pad` | Pad light (was gold) | `#9ecfbc` |
| `--imp-mist` | Haze washes | `#c5e8e4` |

Legacy aliases still defined: `--imp-lilac` → water, `--imp-rose` → aqua, `--imp-gold` → pad.

## Typography

- **Display & body:** Georgia stack + Noto Serif SC (CJK)
- **Mono:** system ui-monospace stack
- **Reading measure:** `--site-prose: 75ch`
- **Body line-height:** ~1.7–1.75

Load: `layouts/_partials/extend_head.html` (Noto Serif SC via Google Fonts).

## Page types

| Page | Layout language |
|------|-----------------|
| Home | Hero epigraph + topic entry chips |
| Essays / Gleanings | Magazine index rows |
| Moments | Note stream (narrower, dashed) |
| About | Full-frame ambient + semantic blocks |
| Posts | Centered 75ch prose |

## CSS load intent

`homepage.css` (tokens) → `typography.css` → `nav-tabs.css` → `tab-panels.css` (PaperMod extended CSS order by filename).
