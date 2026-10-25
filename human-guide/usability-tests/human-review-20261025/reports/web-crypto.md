# Web and crypto: simulated human usability review

Overall usefulness: **6.8/10**. The short cards successfully carry two supplied crypto inputs through recovery and locate the web-discovery route. A labeled input stops at an unwritten preparation step. The deeper material adds substantial reading without fixing that particular gap.

This is an agent simulation of a reader with basic web/crypto familiarity under competition pressure, not an actual human study. No human completion times are claimed. Only this review's brief/fixtures and the current human guide were used; no answer key, preparation script, previous report, source skill, or other review was consulted. Guide files were not edited.

## Ratings

Higher instruction-economy scores mean less burden. Anchors: 9–10 ready with minimal friction; 7–8 minor gaps; 5–6 repeated interpretation; 3–4 major missing bridges; 0–2 unusable.

| Dimension | Score | Reason |
| --- | ---: | --- |
| Findability | 8 | README immediately points to the quick sheet; the artifact table identifies RSA and Base64. Recovery links target whole chapters, however. |
| Command usability | 8 | The two relevant helpers ran in WSL without dependencies or code editing. URL/wordlist substitutions remain for web. |
| Clarity | 7 | Environment labels and success checks are useful. Recognizing a label is described, removing one is not. |
| Instruction economy | 6 | Good short cards coexist with competing entry instructions, duplicated tool choices, and unnecessary uncertainty about notes permission. |
| Recovery | 5 | Existing-directory recovery worked exactly as written. Labeled Base64 recovery dead-ended after following the indicated chapter. |

Arithmetic mean: `(8 + 8 + 7 + 6 + 5) / 5 = 6.8`.

## Route and execution conditions

Started at `human-guide/README.md:3`, then `human-guide/QUICKSTART.md:7`. Visited RSA (`QUICKSTART.md:128`), Decode layers (`:142`), Web paths (`:18`), the linked miscellaneous chapter's representation/encoding sections (`chapters/11-miscellaneous.md:23` and `:48`), the crypto chapter's bytes/RSA sections (`chapters/07-cryptography.md:64`, `:198`, `:223`), web baseline/route sections (`chapters/02-web-exploitation.md:21`, `:72`), the chooser's Web table (`TOOL-CHOOSER.md:9`), and tool rules (`chapters/00-tool-rules.md:5`). Paths in the rest of this report are relative to `human-guide/` unless otherwise stated.

Windows PowerShell was the host. `wsl --list --quiet` showed Ubuntu-24.04 and docker-desktop; WSL Python reported `Python 3.12.3`. There was no supplied organizer Kali connection or live challenge URL. No Kali scan or exploitation was performed. Host `Get-Command` found no ffuf; that does not establish absence on the organizer's Kali machine.

To keep writes inside the assigned scratch folder, I copied only the existing `rsa.py` and `layers.py` helpers into that folder's `recipes/`, retaining the documented relative layout. I invoked each documented `python3 ...` command using the PowerShell wrapper `wsl -d Ubuntu-24.04 --`. This is actual WSL execution, **not a host-Python substitution**. Filename and output-directory substitutions are shown below. No fixture-solving code or preprocessing was invented.

Browser inventory returned `apps: []` and `browsers: []`. Website observations below are **static source review**, not verified clicks, visual layout, clipboard behavior, or search interactions.

## Task 1 — raw RSA: success on corrected fixture

The brief supplied raw `n,e,c`. The quick card says use the route when factors are known or suspected close (`QUICKSTART.md:130`). Nothing in the brief established close factors, so this requires a bounded hypothesis; the same card explains the helper's 100,000-step limit (`:140`).

Exact guide command after filename substitution:

```bash
python3 recipes/rsa.py numbers.json
```

Actual invocation prepended `wsl -d Ubuntu-24.04 --`. Final output, exit 0:

```text
factors: 32416187567 32416190071
re-encryption: OK
plaintext bytes: b'CSG_OK'
saved: rsa-plain.bin
No padding removed. Without length, leading zero bytes cannot be recovered.
```

One command and one filename substitution recovered the requested plaintext. The output directly implements the card's success check. The deeper RSA examples are unnecessary here and would require replacing toy constants if used instead (`chapters/07-cryptography.md:205`, `:230`, `:254`).

Fixture limitation: the first run returned `b'\n\\^\xce\xa0s\xd7\x05\x00'` with re-encryption OK. The parent reported that its intended encoded text exceeded the modulus and corrected the fixture. I reran the same command; I did not inspect its correction record or derive a hidden answer. The original non-text output is **not counted against the guide**. This review does not claim `CSG_OK` is a complete competition-format flag.

## Task 2 — note.txt: success, including one recovery test

Followed Decode layers, `QUICKSTART.md:142`.

```bash
python3 recipes/layers.py note.txt --out decoded
```

Actual invocation again used WSL. Output:

```text
layer1: 35 bytes; header: 789c730e768f77f3
layer2: 27 bytes; preview: b'CSG_FLAG{unwrap_then_check}'
complete compressed stream; extra trailing bytes: 0
saved in: decoded
```

The preview supplies the answer without opening binary files. One command and one filename substitution; no deeper chapter was needed.

To test the written recovery branch, I repeated the command. It exited 1 with `Decoding stopped: [Errno 17] File exists: 'decoded'`. Following `QUICKSTART.md:150`, I substituted `--out decoded-retry`; exit 0, same decoded flag. The guidance works and preserves the original/output history.

## Task 3 — labeled.txt: blocked by missing input-preparation instruction

The file begins `payload=`. I used the same card without silently stripping it:

```bash
python3 recipes/layers.py labeled.txt --out labeled-decoded
```

Actual WSL result, exit 1:

```text
Decoding stopped: Excess data after padding
```

`QUICKSTART.md:150` says to check whether text includes a label. This identifies a plausible cause but never says to copy only the value into a fresh file or preserve the Base64 padding. Following its “Other encodings” link reaches the entire 523-line miscellaneous chapter. Section 3 offers an encoding table and `encoding_toys.py`, which creates and decodes its own hardcoded message (`chapters/11-miscellaneous.md:62`–`:78`); it does not accept the supplied file or demonstrate removing `payload=`. The crypto encoding section likewise demonstrates a toy round-trip (`chapters/07-cryptography.md:64`).

I stopped before deleting the label or writing parsing logic. That would supply an unwritten preprocessing bridge, explicitly excluded by this test. This is an instruction gap, not a decoder bug. Minimal fix: “If the line is `payload=VALUE`, save only VALUE to a new text file, retaining any final `=` padding, then rerun with that filename.” A literal example and direct section link would be enough; another long script is unnecessary.

## Task 4 — HTTP 200 for every path: route success, execution intentionally untested

`QUICKSTART.md:18` provides the relevant route immediately:

```bash
curl -i 'http://challenge.example/a-name-that-should-not-exist'
ffuf -u 'http://challenge.example/FUZZ' -w words.txt -ac -rate 20 -maxtime 60
```

The card then requests a candidate with `curl -i 'http://challenge.example/candidate'`. At `:27`, it explicitly warns that 200 can be a custom error page and tells the reader to retry without `-ac` if automatic filtering hides candidates. That is relevant, concise recovery guidance.

Missing prerequisites in this fixture: actual permitted URL/base path, supplied/provisioned Kali access and installed curl/ffuf, a relevant wordlist, and any necessary session/authentication context. The quick card asks for `words.txt` but does not show one-name-per-line creation. The deep chapter supplies it at `chapters/02-web-exploitation.md:99` using `printf '%s\n' profile export status > routes.txt`, while requiring evidence for the `/api/` prefix and those names (`:96`, `:103`). This resolves the preparation question, but costs another page and a change of filenames/prefix.

To distinguish results using written guidance: compare fake-path and candidate response content, not only status; the deep baseline command saves headers/body (`chapters/02-web-exploitation.md:36`), and the chapter tells the reader to repeat the unchanged request and account for dynamic nonces/timestamps before using length differences (`:28`). A differing body/length is a lead to inspect, not proof of a valid hidden route. The quick and deep ffuf examples use different rate/time defaults (`QUICKSTART.md:24` versus `chapters/02-web-exploitation.md:100`) without explaining which to prefer.

Task status: **success at locating commands/prerequisites and interpreting 200 responses; live execution untested**. No live-service success is claimed or needed by the brief.

## Reading burden and website entry point

The quick sheet is the strongest contest surface: 234 lines total, a clear artifact-to-card table, and short success/error notes. RSA and normal decoding each require copying one line. It should remain the default.

The opening README also tells readers “Start with triage and the tooling rules” at `README.md:17`, after already recommending the quick sheet at `:3`. That creates a second perceived starting sequence. Remove the duplicate starting instruction; put setup/policy reading in a single pre-event link.

Deep links currently make readers choose again among 575 lines of web, 593 of crypto, or 523 of miscellaneous material. Those lengths are document sizes, not claims that a human read every line. For the failed labeled input, the chapter adds code-copy burden without the needed bridge. Link the quick card to an exact recovery subsection and retain the deep chapters as optional reference.

Static website source shows quickstart as the default (`index.html:101`, `:119`), a generated section index (`:97`), per-block copy buttons with a manual-copy fallback (`:78`), and search across all chapters (`:126`). These are promising burden reductions, but no browser was available to verify them. Search requires every query word in the section (`:131`), so a natural-language symptom may need shorter queries; the no-results message correctly suggests fewer words (`:137`). A copy button cannot resolve missing preparation steps.

## Restriction cross-check

Read the original workbook's exported cells in `review/tool-policy.json`, rather than relying only on guide summaries: Windows C14/I14 identify Python in WSL (`:117`, `:123`); H14 permits added libraries except AI/ML (`:122`); Kali C30 lists curl (`:702`), C48 lists ffuf (`:864`); unapproved B51/B52 list online analysis and online compilers/decompilers (`:2204`, `:2209`). The guide's local Python routes and Kali labels agree with these relevant entries. The warning against casually invoking online FactorDB attacks is useful (`chapters/07-cryptography.md:334`).

Read the supplied root `Practice Environment Setup Guide.pdf` with installed fitz. Host Python was used **only for PDF extraction**, not the task solvers. Initial console extraction hit a cp1252 UnicodeEncodeError; rerunning `python -X utf8` fixed that review-tool issue. PDF p4 confirms separate Kali access; pp6/21 prohibit challenge uploads to online services; pp8/9 prohibit AI assistance and external help during competition. This is a pre-event synthetic review, not assistance in an active competition.

One avoidable policy burden: `README.md:25` asks the user to confirm permission for a handbook/prepared scripts, and `QUICKSTART.md:234` repeats uncertainty. The supplied PDF **p7 explicitly allows** personal notes, cheat sheets, digital references, personal repositories, and scripts created before competition. Cite that allowance directly; it does not establish permission for every removable medium. PDF p5 also permits libraries/dependencies/plugins/packages subject to its non-Generative-AI rule without a Windows-only qualifier; reconcile that with the workbook's stricter AI/ML wording and the guide's repeated environment-installation cautions. Do not turn it into permission for unapproved standalone apps.

## Smallest useful changes

1. Add the single labeled-value preparation sentence to Decode layers and link directly to it.
2. Put a one-name-per-line wordlist example beside the Web paths command; briefly state the comparison criteria and align scan defaults.
3. Keep the quick sheet as the sole contest starting instruction. Move provenance/build-validation discussion out of the initial reading path.
4. Replace redundant notes/scripts permission uncertainty with the supplied PDF p7 allowance.
5. Retain the existing environment labels, bounded helpers, preview output, re-encryption check, and fresh-directory recovery; these materially helped.

No score credit was given for chapter volume, source coverage, historical tests, or website features that could not be exercised. This review covers only the four assigned tasks and should not be generalized to every recipe.
