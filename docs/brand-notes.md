# Brand notes — `/dev/null`

A private journal: conversational prose, reflective essays, technical curiosity,
and occasional deadpan humor. This design supersedes the earlier green/serif
and impressionist directions.

## Palette and typography

| Role | Light | Dark |
| --- | --- | --- |
| Paper | `#f7f5f0` | `#201e1b` |
| Secondary surface | `#f0ece5` | `#29251f` |
| Ink | `#292622` | `#e8e3d9` |
| Secondary ink | `#746b63` | `#b7ada2` |
| Accent | `#934c42` | `#d89e8e` |
| Rule | `#dcd6cd` | `#494039` |

Noto Serif SC for headings; Noto Sans SC for prose and controls; system mono for
`/dev/null`. Desktop prose is 18px with 1.85 line-height, about 34–38 Chinese
characters per line. Mobile prose is 17px. Local fonts remain fallbacks.

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
