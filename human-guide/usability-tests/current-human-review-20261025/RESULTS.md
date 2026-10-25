# Human usefulness assessment of the current guide

**Overall: 8.3/10. The short reference is useful under pressure; unfamiliar reversing and some imported personal-note commands still need work.** Three fresh-context subagents independently tested the frozen version at commit `b550a6f`. These are simulated human-reader judgments, not a study with real human participants.

| Reviewer | Findability | Commands | Clarity | Instruction economy | Recovery | Overall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Forensics beginner](forensics/REPORT.md) | 9 | 9 | 8 | 9 | 9 | **8.8** |
| [Linux user new to reversing](reverse/REPORT.md) | 8 | 9 | 7 | 8 | 6 | **7.6** |
| [Basic web/crypto solver](web-crypto/REPORT.md) | 9 | 8 | 8 | 9 | 9 | **8.6** |

Each score is out of 10. Higher instruction economy means less unnecessary reading. Overall is the equal-weight arithmetic mean of the five dimensions; the combined mean is 8.3333, rounded to 8.3.

## What was actually tested

**9/9 supplied local exercises completed.** The forensics reviewer recovered a PNG trailer, retained both versions of a tar member, and correctly interpreted a process event without claiming successful file access. The reversing reviewer recovered and forward-checked a transformed input, found the single accepted VM byte, and verified the crash offset. The web/crypto reviewer recovered raw RSA plaintext, decoded a layered message, and recovered labeled Base64 after following the written preparation step.

The reviewers used actual Ubuntu WSL Python and native Windows PowerShell as appropriate. Each exercised recovery: a pre-existing tar output directory, unmatched crash bytes, or a labeled Base64 decoding error. The parent independently checked saved files, transform/RSA arithmetic, pattern bytes, and score calculations; the VM and event answers also agree with the reports. See [validation.json](validation.json).

Three additional scenarios were **navigation-only**: HTTP download recovery, locating the input comparison in an unfamiliar stripped ELF, and distinguishing real paths when every HTTP response is 200. No PCAP, ELF, or live web service was supplied for those scenarios. They do not count as additional solved challenges.

All three reviewers also used the actual offline website in Chrome, using rendered search results and sidebar links to find a relevant CPTS note. Clipboard contents were checked against displayed commands. One reviewer tested a note with a screenshot and verified Full size/Fit width; the other two selected notes without images and did not claim image testing. The parent inspected representative saved screenshots. No CPTS command was executed against a target.

## What improved relative to the earlier review

| Reviewer | Earlier human-style review | Current review |
| --- | ---: | ---: |
| Forensics | 7.2 | 8.8 |
| Reversing | 6.4 | 7.6 |
| Web/crypto | 6.8 | 8.6 |
| Combined | **6.8** | **8.3** |

The same small fixture inputs were reused without previous answers or outputs. In the earlier review, labeled Base64 stopped at a missing preparation instruction; this round completed that step using the current guide. Reviewers now found the short task cards economical, and the website search/copy controls worked in an actual browser. Earlier review browser observations were static only.

This is a descriptive comparison, not a measured 1.5-point improvement in real human performance: reviewers differ, ratings are subjective, and this round adds CPTS/browser checks. The exercises favor supplied helpers and do not establish readiness for unseen competition challenges. The earlier comparison is specifically [the 6.8/10 human-style assessment](../human-review-20261025/RESULTS.md), not the separate historical round-2 rating.

## Highest-value changes identified

1. **Annotate the incorrect directory-fuzzing command in the personal HTTP note.** In `cpts/pages/cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8.md:22`, the directory-enumeration example places `FUZZ` inside `Host: siteisup.htb/FUZZ` while the URL has no path placeholder. It varies a slash-containing Host header instead of the directory path described. The hardcoded `-fs 1131` also needs a challenge-specific baseline. Preserve the original snapshot, but add an editorial correction or point readers to the reviewed quick-reference command. This is a static command/description mismatch, not a live-tested exploit failure.
2. **Add one annotated stripped-binary-to-helper walkthrough.** The reversing chapter has useful commands and a source-visible toy, but a new reverser still has to recognize the startup call target, repeated key, rotation, and expected table. Show the extraction and resulting JSON together, and link the static quick card directly to it. References: `chapters/06-reverse-engineering.md:188,206,309`; `QUICKSTART.md:171`.
3. **Keep prerequisites beside deep-linked commands.** The HTTP export section uses `$tshark`, whose assignment is earlier in the chapter. A direct quick-reference arrival has to backtrack. Include the prerequisite link/assignment at that entry point. Reference: `chapters/04-network.md:50-59`.

Smaller findings: clarify that sent-pattern verification checks membership, not debugger byte-order interpretation (both the correct and reversed four-byte sequences produced valid offsets); name concrete comparisons for HTTP-200 false positives; make the unvetted status of CPTS notes explicit on pages reached directly through search; and put process-event interpretation immediately after the JSON command, before the longer EVTX alternative.

## Integrity and limits

All **276 snapshotted guide/helper/CPTS/asset files remained unchanged** during review. Only this review directory was added; the report does not silently apply fixes and then attach old scores to new content. Browser automation targeting mistakes, local shell path mistakes, and clipboard permission setup were disclosed and excluded from guide scores.

No organizer portal, competition VM, remote target, installation, outside research, or independent solving algorithm was used. Reviewers could use ordinary path/filename substitutions and browser harness code. No human reading speeds or completion times are claimed. This is a bounded usability review, not an audit of all 102 CPTS notes or all command correctness.

[Method](METHOD.md) · [Frozen snapshot](snapshot.json) · [Parent verification script](verify.py) · [Verification results](validation.json)
