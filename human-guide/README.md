# Cyber SEA Game · Human CTF field guide

Open **[the offline website](index.html)** or **[the complete Markdown handbook](HANDBOOK.md)**. Both contain the same guide. The category files are in `chapters/` if you prefer shorter documents.

## Website

Double-click `index.html` and open it in Chrome. No server, installation, account, or internet connection is needed. All chapters, search data, styles, and application code are embedded in that one file. External documentation links open only when you choose them.

The website includes full-text search, chapter navigation, a section index, command-copy buttons, light/dark themes, printing, a Markdown download, and a searchable tool list. `/` focuses search; Escape clears it. Search finds sections containing all your words. The print button prints the current view. On a narrow window, use **Chapters** to open navigation.

The **Tool lookup** button filters all 282 workbook entries by environment and approval status. Windows-sheet entries may be installed in WSL; read the installation location before using a command. The complete table is also in [TOOL-MATRIX.md](TOOL-MATRIX.md).

## Contents

Start with triage and the tooling rules. The six main subjects are web exploitation, forensics, network, steganography, reverse engineering, and cryptography. Supplementary chapters cover binary exploitation, malware, OSINT, miscellaneous challenges, advanced cryptography, historical pwn practice, and excluded agent workflows.

The original agent-oriented repository is preserved. [SOURCE-COVERAGE.md](SOURCE-COVERAGE.md) accounts for every original file and explains consolidation or exclusion. This is a substantive human rewrite, not a line-for-line copy. Advanced entries identify prerequisites and limits; they do not claim a historical exploit works unchanged on an arbitrary target.

## Competition scope

The handbook uses the supplied `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx` and [official 2026 rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/), checked on 25 October 2026. The workbook contains 39 Windows/WSL entries, 161 Kali entries, and 82 unapproved entries. Approved tools are not guaranteed operational. AI tooling and prohibited hosted analysis workflows have been excluded from the practical routes.

This is independent prepared study material. The tool whitelist does not establish permission to bring a handbook, prepared scripts, or removable media. Confirm that point with the organizer before event use. No AI tools are needed to read the deliverables.

## Validation and limits

The build checks workbook row counts and provenance, inert rendering of HTML payloads, unique anchors, Markdown/website consistency, local links, Python-block syntax, coverage completeness, and preservation of the original files. Self-contained examples are checked separately where practical. These checks do not prove every recipe against every tool version or a live challenge.

No browser is exposed in this session, so live browser interactions and visual layout could not be verified. The site JavaScript has been syntax-checked; its CSS includes narrow-window and print layouts. Commands involving organizer infrastructure, unavailable tools, or challenge-specific inputs were not executed.

The original repository's tests passed: 109 passed, 9 skipped, with 1,892 subtests passed. Those tests are separate from the new handbook validation.

The final handbook contains 16 reading chapters and two reference appendices. All 286 original files are accounted for in the source map. Category checks include 37 local web/crypto/misc examples, 11 reverse/pwn examples, and synthetic forensic/decoder checks. Detailed scope and untested workflows are recorded in `review/editorial-validation.md`; final build-check counts are in `review/validation.json`.

## Attribution

Adapted from the supplied ctf-skills repository. Original copyright © 2026 Lukasz Jagiello. The [original MIT license](LICENSE) is included. This guide is not an official AJCCBC or Trend Micro publication.
