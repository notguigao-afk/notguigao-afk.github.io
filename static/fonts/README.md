# Blog fonts

Noto Serif SC (reading text, weights 400–700) and Noto Sans SC (UI, weights
400–600) are served from this site. The unmodified variable WOFF2 files were
downloaded from the official Google Fonts service on 2026-10-23. Every subset
contains an `fvar` table. Content hashes in filenames make font updates cache-safe.

Source CSS request (modern Chromium user agent):

<https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400..600&family=Noto+Serif+SC:wght@400..700&display=swap>

The original family names, weight ranges, `font-display: swap`, and all 202
`unicode-range` declarations are retained in `assets/css/extended/fonts.css`. Only
the font URLs have changed. Browsers fetch the subsets needed by each page,
including new posts, rather than downloading whole CJK fonts. There are no
runtime requests to Google Fonts. Original font binaries have not been modified.

Upstream sources and licenses:

- Noto Serif SC: <https://github.com/google/fonts/tree/main/ofl/notoserifsc>,
  [SIL Open Font License](notoserifsc-OFL.txt).
- Noto Sans SC: <https://github.com/google/fonts/tree/main/ofl/notosanssc>,
  [SIL Open Font License](notosanssc-OFL.txt).
