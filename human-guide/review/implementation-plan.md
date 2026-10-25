# Human CTF handbook implementation plan

Goal: turn the repository into a readable, command-focused study and competition reference, delivered as standalone HTML and Markdown for Windows/WSL and Kali.

The user's request authorizes the conversion. Keep the original material intact. The website is a local document, with no account, AI service, remote assets, upload, server, or installation required to read it. Its content comes from the same chapter files as the combined Markdown.

## Deliverables

- `index.html`: offline website with chapter navigation, full-text search, copy buttons, section links, theme control, print, and Markdown download.
- `HANDBOOK.md`: combined handbook; `chapters/`: readable individual chapters.
- `TOOL-MATRIX.md`: every workbook entry with original platform, version, notes, and sheet/row provenance.
- `SOURCE-COVERAGE.md`: per-file disposition, separating adapted guides, supplemental history, and excluded agent machinery.
- `README.md`: opening instructions and verification limits.

## Work and checks

- [x] Read all three workbook sheets; retain policy and environment distinctions.
- [x] Review source categories independently and consolidate into human workflows with commands, expected evidence, troubleshooting, and advanced topic coverage.
- [x] Review repository infrastructure and retain attribution; do not turn installer/evaluation tooling into competition instructions.
- [x] Build the local site from Markdown with safe rendering of exploit payloads; test HTML escaping and offline assets.
- [x] Verify coverage, links, balanced fences, Python syntax and selected self-contained examples, static website behavior, and archive contents. Live browser checks were unavailable; this limitation is documented in the README and validation record.

## Decisions

The six official categories come first. Other repository topics remain supplementary. Tool approval is separate from actual availability. Missing or conflicting installation records remain visible. The handbook is preparatory material; organizer permission to bring prepared reference material is not established by the supplied tool list. Do not infer future questions from vendor identity.

## Review focus

Commands pasted into the wrong shell; approved packages absent in the installed Python environment; HTML payloads rendered as active markup; long tables and commands on small screens; searches hiding a relevant recipe; accidental omission of a source file; prohibited services retained in runnable instructions.
