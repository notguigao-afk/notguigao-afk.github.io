# Brand notes — `/dev/null`

A private journal: conversational prose, reflective essays, technical curiosity,
and occasional deadpan humor. This design supersedes the earlier green/serif
and impressionist directions.

## Palette and typography

| Role | Light | Dark |
| --- | --- | --- |
| Paper | `#ffffff` | `#201e1b` |
| Secondary surface | `#f0ece5` | `#29251f` |
| Ink | `#000000` | `#e8e3d9` |
| Secondary ink | `#746b63` | `#b7ada2` |
| Accent | `#934c42` | `#d89e8e` |
| Rule | `#dcd6cd` | `#494039` |

Reading typography follows the actual `crush.pages` styles, audited on 2026-10-10:
body Times-Roman 12 pt, title bold Times 24 pt, relative single line spacing,
paragraph spacing 0 pt before / 12 pt after (title: 16.078125 pt after), black text.
The font and spacing values were decoded from the document's referenced styles,
not inferred from unused font names in its stylesheet.

Use local @font-face references to Times-Roman, Times-Bold, Times-Italic, and
Times-BoldItalic to avoid browser font-family aliases. CoreText on this Mac resolves
Times Chinese text to STSongti-TC-Regular (ascent + descent = 1.4em); use that local
face, then SC and Noto Serif SC fallbacks. This fallback observation is from the local
font engine; the document itself specifies Times, not a named Chinese font.
Web body is 16px (12pt), title 32px (24pt), natural single-line font metrics (about 1.4em for mixed Chinese text), paragraph gap
1em, maximum reading width 40rem. Font fallback and rasterization can differ on
other systems; this is a responsive web adaptation, not pixel-identical Pages rendering.
The original inline italics, bold statements, and italic closing paragraphs in Crush
must survive import. Do not replace author emphasis with invented blockquotes.
Noto Sans SC remains the UI face. All article words and paragraph boundaries stay intact.

Keep PaperMod's variables bridged on `html:root[data-theme="dark"]` and the
auto-dark media rule. The existing `--imp-*` variable names remain stable.

## Layout

- A single masthead, followed by an 11rem contents column and a reading column.
- The 64rem overall frame includes the gutter between the two columns.
- At less than 800px, navigation becomes one row and content becomes one column.
- Homepage opens directly with the newest post, then five earlier entries.
- The author's prose is unchanged. Dates and entries are generated from Hugo content.
- Moments show their complete text; long articles have a category return link.
- Warm dark mode, visible keyboard focus, reduced-motion support, and a functional
  skip link are required. No ornamental entrance animations or heavy cards.

## AI marginalia

Each published post has a short, original comment after the body, labeled
“AI 边批”. It is distinct from the author's prose, summaries, and RSS body.
The moments stream also shows the same signed comment after each complete note.

`data/annotations.toml` stores comments by content filename and references an
immutable author record containing name, exact model, effort, and generation date.
The current record is **Codex / GPT-6 Astra · High**, with model and effort supplied
by the user for the generation session. A different generation session should add
its own author record instead of rewriting the identity on existing comments.

When adding a post:

1. Read the complete article and write a specific, short comment. Favor deadpan
   observations and comic logic; for bereavement or disaster, use a gentler response.
2. Add the comment under `[posts.<content-filename>]` and reference its author record.
3. Use the model/effort actually reported for that session. Ask if unavailable;
   never infer them from a configured default or copy another generation's identity.
4. Run the checks below. A missing comment warns during Hugo builds and fails the
   invariant check. Comments are authored at edit time; there are no runtime API calls.

## Validation

Run `hugo --cacheDir /tmp/my-blog-hugo-cache`, then
`python3 scripts/ux_invariants.py` (Python 3.11+). The checks cover navigation,
accessibility basics, taxonomy names, and complete signed annotations on all posts.
Preview desktop/mobile widths, both themes, and article/annotation boundaries.
