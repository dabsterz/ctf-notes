# Human guide improvements implementation plan

> **For agentic workers:** Use superpowers:executing-plans for implementation; use the three independent human-style reviewers for verification after the revision.

**Goal:** Make the existing offline website and Markdown useful during a contest, with complete short recipes and accurate category tool comparisons.

**Architecture:** Keep the detailed chapters. Add a short QUICKSTART.md as the website's landing page and a TOOL-CHOOSER.md organized by task/category. Small standard-library scripts remove the assembly burden identified in round 1; embed their source in the standalone website and include them in the ZIP. Build all formats from the same sources.

**Tech Stack:** Existing Python Markdown/BeautifulSoup builder, plain JavaScript/CSS, portable standard-library Python recipes.

**Spec:** User's active objective and human-guide/usability-tests/round-1/RESULTS.md. The user authorized improvements following that proposed short-card approach, plus category tables of strengths and weaknesses. No additional design decision is required from the user.

## Global constraints

- Preserve original source skills, detailed coverage, workbook and all 282 policy entries.
- Windows native, Windows WSL, and Kali must be distinguished for every tool recommendation.
- No prohibited tool, library or hosted service becomes an approved route through this revision.
- Commands accept real challenge inputs; record assumptions, observable success and a useful failure action.
- A shorter default reading path must not require reading the entire handbook.
- Tool tables cover every existing practical CTF category and distinguish discovery, online login guessing and offline hash cracking.
- Verify claims with official tool documentation; retain workbook coordinates.
- No install, deployment or push is needed for this revision.

## Review focus

- Invalid/missing inputs: recipe scripts exit clearly and do not present fabricated success.
- Ambiguous outputs: re-encrypt/forward-check candidates, preserve evidence and explain limits.
- Environment confusion: platform labels come from workbook entries, not platform popularity.
- Offline operation: embedded recipe downloads and chapter anchors work without fetching files.
- Instruction burden: default route is a small task card; tables are selected useful tools, with the full inventory separately available.

## Tasks

- [x] Add complete RSA, layered decoding, byte-transform, JWT, and VM-input recipes, plus extraction/offset helpers where needed. Run them on synthetic success and relevant failure inputs.
- [x] Write QUICKSTART.md and TOOL-CHOOSER.md; link each detailed category to the relevant short route/table. Fix missing 4688 interpretation and extraction follow-up steps.
- [x] Extend builder/navigation to prioritize the short guide and provide embedded recipe source/downloads. Preserve Markdown section links in the combined handbook. Add focused builder checks for those user-visible paths.
- [x] Build website, handbook and ZIP; check all local links, policy references, Python syntax, embedded/download content and packaging.
- [x] Repeat constrained human-style walkthroughs with the three reviewers using new fixtures. Review scores and friction without presenting agent timing as human timing. Correct material findings.
- [x] Record verification scope and limitations, then audit every objective before marking complete.

## Execution record

The existing shared workspace was retained for this authorized document revision. No merge, push or deployment is part of this goal. Both review rounds and original guide content are preserved.

Implemented 8 helpers, a short landing guide, 11 tool tables (72 comparisons / 66 distinct approved entries), category cross-links, embedded offline script downloads and precise merged Markdown anchors. Three fresh reviewers solved all 9 new cases; independent grading passed. Addressed all concrete clarity findings. Follow-up reviewer checked offset boundaries and table escaping. Evidence is in `human-guide/review/improvement-validation.md` and `human-guide/usability-tests/round-2/RESULTS.md`.

No design deviations requiring user decisions and no unresolved material review findings. Browser layout and organizer-installed tools are explicitly untested; DOM interaction tests and native-Python portability checks describe their narrower scope.
