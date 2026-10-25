# Cyber SEA Game · Human CTF field guide

Start with **[the short contest reference](QUICKSTART.md)** or **[the offline website](index.html)**, which opens on that same short guide. Use **[Choose a tool](TOOL-CHOOSER.md)** for category tables of strengths, weaknesses, event environments and first commands. The **[complete handbook](HANDBOOK.md)** keeps the deeper explanations.

The ZIP includes ready-to-run helpers in `recipes/`. Extract it, open a terminal in the extracted folder, and run the quick-reference commands there. If you have only `index.html`, its **Recipe downloads** page can save each embedded script offline. Put downloads in a `recipes` subfolder. The original 16 category/rules chapters are still in `chapters/`.

## Website

Double-click `index.html` and open it in Chrome. No server, installation, account, or internet connection is needed. All chapters, search data, styles, and application code are embedded in that one file. External documentation links open only when you choose them.

The website opens as a dark technical workspace with collapsible chapter groups, an outline, task shortcuts and readable command panels. Use **Focus** to hide the side panels, **Aa** to choose 16/18/20 px text, and **Light** to switch themes. Long scripts have an **Expand** control; copying always preserves the original command text.

`/` focuses full-text search; Escape clears an active search or closes mobile navigation. Search finds sections containing all your words. **Export** offers Markdown download and printing of the current page. On a narrow screen, **Chapters** opens navigation and **On this page** expands the section outline. Theme and text size are saved locally when the browser permits it. The website needs no external fonts, account or runtime downloads.

The **Tool lookup** button filters all 282 workbook entries by environment and approval status. Windows-sheet entries may be installed in WSL; read the installation location before using a command. The complete table is also in [TOOL-MATRIX.md](TOOL-MATRIX.md).

## Contents

**[Vernon's CPTS notes](CPTS.md)** is a separate sidebar section with 102 notes in their original folders and 33 screenshots available offline. Search includes these notes; screenshots offer **Full size** and **Fit width**. [CPTS-NOTES.md](CPTS-NOTES.md) combines them into one Markdown file. Keep `cpts/assets/` beside it for images, or use the self-contained website.

This is a snapshot, not live synchronization. The Obsidian vault was not modified; byte-identical originals are in `cpts/original/`. Two unreadable notes were omitted at your request: `Exploits/Web Exploits.md` and `Exploits/Web Shells-DESKTOP-0GERI6L.md`. These personal notes retain their original commands and have not been filtered against competition tool restrictions; use the event tool rules and lookup before running them.

The competition PDF lists seven categories: Digital Forensics, Malware Analysis, Web Security, Reverse Engineering, OSINT, Cryptography and Miscellaneous. The website groups these together. Network, steganography and pwn remain supporting reference material.

The original agent-oriented repository is preserved. [SOURCE-COVERAGE.md](SOURCE-COVERAGE.md) accounts for every original file and explains consolidation or exclusion. This is a substantive human rewrite, not a line-for-line copy. Advanced entries identify prerequisites and limits; they do not claim a historical exploit works unchanged on an arbitrary target.

## Competition scope

The handbook reconciles the supplied `Practice Environment Setup Guide.pdf` with `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`. Read [Competition setup](COMPETITION.md) once for access, rules, machine limits and the practice/competition distinction. The workbook contains 39 Windows/WSL entries, 161 Kali entries and 82 unapproved entries; original locations and reasons remain in the matrix.

The PDF expressly permits notes, cheat sheets and prewritten scripts (p.7). Non-generative-AI libraries, dependencies, plugins and packages may be installed (p.5); the workbook's stricter AI/ML exclusions and named unapproved entries still guide the practical routes. Unlisted standalone apps require organizer approval. No AI tools are needed to read or use this independent guide.

## Validation and limits

The build checks workbook row counts and provenance, inert rendering of HTML payloads, unique anchors, Markdown/website consistency, local links, Python-block syntax, coverage completeness, and preservation of the original files. Self-contained examples are checked separately where practical. These checks do not prove every recipe against every tool version or a live challenge.

The interface was rendered and tested in installed Chrome from the local HTML file, offline. All 125 pages were checked at 1440, 768 and 320 px widths; selected desktop/mobile screenshots were visually reviewed. Main text colors were checked in both themes, with larger-text, spacing and print checks. These checks are not a full accessibility certification or an organizer-environment test. [UI research and verification](review/ui-research.md).

The original repository's tests passed: 109 passed, 9 skipped, with 1,892 subtests passed. Those tests are separate from the new handbook validation.

The revised handbook contains the quick reference, competition setup, tool chooser, 16 reading chapters, recipe source/downloads and two reference appendices. The unchanged environment PDF is included in `sources/` in the ZIP; keep that folder beside the website to open its source links. All 286 original files are accounted for in the source map. Earlier category checks included 37 local web/crypto/misc examples, 11 reverse/pwn examples, and synthetic forensic/decoder checks. The latest PDF reconciliation is recorded in [the environment audit](review/environment-audit.md); build-check counts are in `review/validation.json`. Earlier usability scores describe the versions tested, not a new rating of this revision.

## Attribution

Adapted from the supplied ctf-skills repository. Original copyright © 2026 Lukasz Jagiello. The [original MIT license](LICENSE) is included. This guide is not an official AJCCBC or TrendAI/Trend Micro publication.

Personal CPTS notes are supplied by Vernon and are separate from the original ctf-skills attribution above.
