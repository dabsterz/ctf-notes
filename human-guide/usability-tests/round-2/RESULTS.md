# Revised guide: independent simulated walkthroughs

Three fresh-context agents used the revised short guide on nine new synthetic tasks. **All nine tasks completed; all answer candidates and score arithmetic were independently checked.** No included recipe required a solver code edit.

| Reviewer | Contest use /10 | Study use /10 | Completed |
| --- | ---: | ---: | ---: |
| Web / crypto | 9.3 | 9.0 | 3/3 |
| Forensics | 9.3 | 9.0 | 3/3 |
| Reverse / misc | 9.3 | 9.0 | 3/3 |

The earlier round averaged 7.27/10 for contest use and had eight complete tasks plus one partially supported interpretation. This round averaged 9.3/10. These are descriptive subjective ratings, **not measured real-human improvement**: reviewers and inputs differed, and the tasks were deliberately small and clue-rich. The guide now supports the process-event interpretation that was missing previously.

Reviewers used narrow searches and bounded excerpts rather than loading the entire handbook. They were prohibited from reading answer keys, fixture-generation/server code, prior reviews, original skill sources or outside references during solving. They used native Windows Python only as a portability proxy, with recorded interpreter/path adaptations. Their tool-choice answers correctly distinguished web discovery, offline hashing, online login attempts, disk/memory/capture work and binary formats. Tool availability was not tested on the organizer's machines.

## Findings addressed after scoring

- Added native PowerShell JSON viewing and the `TimeCreated` export alias beside `SystemTime`.
- Clarified the Wireshark conversation-filter-to-stream path.
- Explained ambiguous hash shape with an MD5/NTLM example; tied Fermat to close primes and a bounded fallback.
- Labelled the miscellaneous Python example specifically as Base64/compression.
- Clarified that the debugger startup instruction is the GEF route.
- Added `pattern.py --sent pattern.bin` so the offset helper verifies bytes against the actual input file. A follow-up reviewer checked accepted/rejected boundary cases.
- A parent DOM test found a Markdown escape leaking into the ROPgadget command. The builder now removes table-only pipe escapes from rendered code, with a regression check; the follow-up reviewer verified that non-table backslashes remain intact.

Scores remain frozen at the pre-fix assessment. The report does not invent a higher score for these follow-up edits.

## Evidence and limits

- [Web/crypto walkthrough](reports/web-crypto.md)
- [Forensics walkthrough](reports/forensics.md)
- [Reverse/misc walkthrough and follow-up code review](reports/reverse-misc.md)
- [Independent answer and score verification](verified-results.json)
- [DOM integration results](../../review/site-validation.json)

The parent checked five recovered files, both preserved tar versions, the crash slice, event fields, independent transform/VM/RSA arithmetic, and baseline-denied versus modified-accepted loopback HTTP responses. Reviewers reported their own mistakes and basic glue rather than silently rescuing missing algorithms.

The real website browser surface was unavailable. DOM integration exercises routing, search, copied text, embedded download contents, tool filtering and controls without external resource requests. It does not measure visual layout, real clipboard permissions or browser file dialogs. No claim is made about unseen challenge performance, human reading speed or WSL/Kali installation health.
