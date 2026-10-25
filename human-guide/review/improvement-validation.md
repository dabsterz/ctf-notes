> Historical review of an earlier revision. For the supplied environment PDF and current policy reconciliation, see [environment-audit.md](environment-audit.md).

# Human-guide revision: verification and scope

## What changed

The website now opens on `QUICKSTART.md`, a short task index and matching command cards. `TOOL-CHOOSER.md` adds 11 category tables with 72 comparison rows referencing 66 distinct approved workbook entries. It deliberately selects useful alternatives rather than making the reader compare every installed utility; the complete 282-entry policy matrix remains available separately.

Eight standard-library scripts accept real filenames/values for RSA, layered decoding, JWT claim editing, XOR/rotation inversion, a one-byte VM, PNG trailers, duplicate tar preservation and crash patterns. Their source is included in `RECIPES.md`, embedded in the offline website for individual downloads, and packaged in the ZIP. Full chapters remain and link to the short routes.

The comparisons separate ffuf/Gobuster web discovery, John/hashcat offline cracking and Hydra online login testing. Every row gives strengths, weaknesses, a first action and event-specific environment. Tool names/doc links point to primary project or official distributor documentation. Those references support capabilities and syntax; the supplied workbook is the approval authority. Version-dependent options and actual organizer installations are not all executed here.

## Verification

- `python -m unittest discover -s human-guide/review -p 'test_*.py'`: builder contracts and helper behavior, including malformed inputs, bounded failures, duplicate preservation and exact byte checks. See command output for the final count.
- `python human-guide/review/check_tool_chooser.py`: directly reads the XLSX XML, verifies all 282 tool-name cells and approved installation locations against the retained extraction, and validates comparison table structure and every W/K reference.
- `python human-guide/review/validate.py`: generated content consistency, section links in website and combined Markdown, code syntax, embedded script equality and original-file hashes.
- `node --check human-guide/assets/app.js`: JavaScript syntax.
- `node human-guide/review/test_site.cjs PATH_TO_JSDOM`: eight DOM interaction groups with jsdom 26.1.0, installed only in a temporary developer-test directory. No Node dependency is needed to read the guide or packaged for contest use.
- `powershell -NoProfile -File human-guide/review/test_event_fields.ps1`: syntax-checks the PowerShell blocks and runs the exact event-mapping pipeline on synthetic XML. This does not test real EVTX ingestion.
- `python human-guide/review/grade_round2.py`: independent score/answer/artifact verification. Its HTTP check requires the owned loopback test server, which is stopped after evaluation.
- `python human-guide/package.py`: package contents and CRC checks; the ZIP includes both reading formats and helper scripts.

Three fresh simulated human reviewers completed nine new synthetic tasks using unchanged recipes. All candidates matched the withheld key. Scores averaged 9.3/10 for contest use versus the first round's 7.27/10, but this is not a controlled human study or a measured speed improvement. Their remaining clarity findings were addressed and the final pattern/rendering changes received a follow-up review. [Round 2 report](../usability-tests/round-2/RESULTS.md).

## Remaining practical limits

The computer-use inventory exposes no browser. DOM checks establish the tested application logic, not visual layout, browser permissions or real download dialogs. The helpers were executed with native Windows Python as a portability proxy; no claim is made about the event's WSL/Kali tool installations, GPU availability, live services, or every command in the full handbook.

The event's permission to bring prepared notes/scripts remains an organizer question already stated in the guide. No new tool installation or hosted analysis service is introduced as a contest route. Original source skills and workbook are preserved.
