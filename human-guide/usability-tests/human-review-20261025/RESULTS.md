> This review rates the frozen version before the environment-PDF integration. See snapshot.json for its hashes. Scores were not remeasured after edits.

# Human usefulness assessment

**Overall: 6.8/10. Useful task cards, but too much navigation and some missing preparation steps.** Three fresh subagents independently tested the current guide as constrained human readers. These ratings are agent judgments, not results from real human participants.

| Reviewer | Findability | Commands | Clarity | Instruction economy | Recovery | Overall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Forensics](reports/forensics.md) | 7 | 8 | 7 | 6 | 8 | **7.2/10** |
| [Reversing](reports/reverse.md) | 8 | 8 | 6 | 5 | 5 | **6.4/10** |
| [Web and crypto](reports/web-crypto.md) | 8 | 8 | 7 | 6 | 5 | **6.8/10** |

Each overall score is the arithmetic mean of five dimensions. Higher instruction economy means less unnecessary work. The cross-review average is descriptive, not a statistically validated measure.

## What actually worked

**8 of 9 supplied local tasks succeeded.** PNG trailer, archive versions, process-event interpretation, byte transform, decoded VM, crash offset, corrected RSA, and layered decoding were completed. Labeled Base64 was blocked because the guide identified the problem without explaining the input-preparation step. Ordinary readers may already know how to remove a label; this test deliberately required the guide to supply that instruction.

Python helper tests ran in actual Ubuntu WSL; the event JSON command ran in Windows PowerShell. Existing-directory recovery worked for tar and decoding. The reversing reviewer exercised crash-pattern verification failure and recovery. The parent separately checked saved outputs and the VM answer; all nine artifact/answer checks passed. This count is verification checks, not nine solved tasks.

Each reviewer also assessed one transfer scenario: HTTP file recovery, an unfamiliar stripped binary, or web discovery where every response is HTTP 200. The HTTP routes were located; the reversing route lacked a sufficient beginner bridge from binary instructions to helper inputs. **None of those three scenarios was an end-to-end live challenge test.**

## Changes with the highest benefit

1. **Make the quick reference the single starting point.** Move setup, provenance and repeated rule explanations behind one link. Preserve visible environment labels. The evaluated quick reference has about 1,725 whitespace-delimited words; the full handbook about 75,332. Full chapters should remain optional reference.
2. **Replace general advice with the missing small steps.** Show how to save only a labeled Base64 value, create a short wordlist, and reach HTTP object export directly. Put the one-line JSON event command before the longer EVTX route.
3. **Add one compact reversing walkthrough.** Show an actual annotated disassembly/decompiler excerpt and how it becomes `key_hex`, `rotation` and `expected`. The current helpers succeed on prepared JSON; that does not demonstrate that a beginner can obtain the JSON.
4. **Remove obsolete permission uncertainty.** The supplied environment PDF page 7 explicitly allows notes, cheat sheets and prewritten scripts. Page 5 addresses non-generative-AI libraries/dependencies/plugins/packages. Reconcile this with the workbook's stricter AI/ML wording and named exclusions once, rather than repeating unresolved setup advice. Unlisted standalone apps still require organizer approval.
5. **Keep success checks and short recovery branches.** Output previews, forward/re-encryption checks and fresh-output-directory instructions helped. Make extra inspection commands conditional when the preview already answers the task.

Evidence: `QUICKSTART.md:5`, `:27`, `:91-113`, `:126`, `:150`, `:164`, `:192`, `:234`; `README.md:17`, `:25`; `chapters/04-network.md:57`; `chapters/06-reverse-engineering.md:182-208`; `chapters/00-tool-rules.md:88-96`. Review reports include precise command transcripts and the reasoning behind each score.

## Integrity and limitations

The parent initially created an RSA fixture whose intended plaintext exceeded its modulus. The reviewer caught the non-text result; the parent corrected the fixture and the reviewer reran the same command. That fixture error did not reduce the guide score. Original/corrected inputs and reason are preserved in `fixture-correction.json`.

All 30 snapshotted guide/helper files remained unchanged during review. Reports and fixture outputs were added separately; the guide was not rewritten during evaluation. No browser was exposed, so website inspection was static only: no live usability, layout, copy-button or download claim is made. No organizer Kali machine, portal or competition challenge was used. These small fixtures favor existing helpers and do not establish general competition readiness.

[Method](METHOD.md) | [Verification](validation.json) | [Snapshot](snapshot.json)
