# Command-first notes implementation plan

**Goal:** Keep the user's existing navigation and dark workspace, while making category pages useful as copy/paste contest references.

**Approved scope:** The user requested research and edits, explicitly prefers the current structure, wants substantially fewer words and more usable commands, especially web. Routine editorial and implementation choices proceed within that request.

**Architecture:** Store concise task cards in `human-guide/quick/`. Preserve the previous 12 category chapters byte-for-byte in `reference/chapters/`. The builder composes each existing chapter path from its quick version plus an optional Full reference disclosure. Same sidebar routes, existing deep links and complete offline Markdown remain available. Search and deep links reveal disclosures automatically. Original Obsidian snapshots remain untouched.

**Editorial pattern:** Task heading; platform; short complete command block; success observation; one recovery instruction. Define values where needed, mark examples, omit shell prompts and incomplete snippets from runnable copy paths. Do not infer tool approval from personal notes. Keep setup close to use.

**Research:** NN/g scanning research; Google developer style guidance for procedures, command formatting and placeholders. Store source links and applications in `human-guide/review/readability-research.md`. Avoid claiming a reading-level formula proves command correctness or human speed.

- [x] Write the web task cards and independently authored cards for the other eleven categories.
- [x] Add and test Markdown disclosure rendering, preserved old anchors, search navigation into collapsed content, and readable outlines.
- [x] Add a concise editorial correction to the known personal HTTP ffuf example, preserving imported raw bytes.
- [x] Verify command syntax and representative web requests against a disposable local fixture; verify existing helpers and policy/provenance.
- [x] Measure default-view prose and command coverage, inspect Chrome desktop/mobile, rebuild Markdown and ZIP, and record limitations.

**Review focus:** copied blocks must include prerequisite variables; shell dialect labels must match; placeholders must be explicit; success criteria must not overclaim; archived text/old anchors must remain intact. Historical usability scores must stay attached to their frozen versions.
