# Independent simulated human review 2: reversing

Persona: intermediate Linux user, new to reversing. This is an AI simulation constrained to the guide, not a recruited human study. No human timing, participant observations, or end-to-end raw-binary success is claimed. Assessment date: 2026-10-25.

Overall usefulness: **6.4/10**, arithmetic mean of the five scores below. The prepared-input cards work well. The point at which a beginner must derive those inputs remains substantially harder than the cards suggest.

| Dimension | Score | Reason |
|---|---:|---|
| Findability | 8 | README leads directly to task cards; binary/checker and crash rows are recognizable. Raw reversing guidance requires another trip through tool choice and a long chapter. |
| Command usability | 8 | Three supplied fixtures produce explicit verified results with ordinary filename substitution. Environment labels are useful. No binary/decompiler commands could be tested against a supplied executable. |
| Clarity | 6 | Preconditions and byte order are clear. Choosing the stripped function and deriving key/rotation/table remain expert interpretation steps. |
| Instruction economy | 5 | Compact cards coexist with repeated environment/policy cautions and extensive advanced material. A simple beginner bridge is harder to find than the breadth suggests. |
| Recovery | 5 | Pattern-length failure is diagnosable and recoverable. “Correct the decoded semantics” and “change the model” are stop signs for this persona, not recovery procedures. |

Scale applied: 9–10 minimal friction; 7–8 minor gaps; 5–6 repeated interpretation; 3–4 major missing bridges; 0–2 unusable. Breadth and historical validation counts did not increase scores.

## Route and boundaries

Started at `human-guide/README.md:3`, followed `QUICKSTART.md`. Consulted its opening environment instructions, task table, Static reversing, XOR and rotation, Small VM, Crash offset, and Before the event. For task 4, followed the reverse tool choice (`TOOL-CHOOSER.md:89`) and the reverse chapter: environment checks, identification, toy checker, radare2, Ghidra, comparison breakpoint, transform and VM sections. Checked the crash chapter's pattern instructions (`chapters/08-binary-exploitation.md:183`, `:241`) and chooser crash row (`TOOL-CHOOSER.md:126`). Some chapter reads returned more material than needed; no broad advanced recipes were executed.

Only assigned `reverse/TASKS.md` and its three neighboring input files were used as challenge evidence. No old usability reports, keys, fixture generator, original CTF skills, other reviewer results, or external research supplied missing logic. No guide files changed. All generated challenge outputs are in this review's `reverse/` folder.

The guide normally asks for a terminal in `human-guide` (`QUICKSTART.md:5`). To keep all generated files in the allowed scratch directory, I stayed in `human-guide/usability-tests/human-review-20261025/reverse` and substituted `../../../recipes/` for `recipes/`. This is a reviewer-harness adaptation, not an instruction supplied by the guide.

## Executed tasks and evidence

PowerShell host checks:

```text
wsl --list --verbose
  Ubuntu-24.04: Stopped, version 2 (default)
  docker-desktop: Stopped, version 2
python --version
  Python 3.14.4
wsl -d Ubuntu-24.04 -- bash -lc 'command -v python3 gdb objdump strings xxd r2; python3 --version'
  /usr/bin/python3
  /usr/bin/gdb
  /usr/bin/objdump
  /usr/bin/strings
  /usr/bin/xxd
  Python 3.12.3
```

There was no `r2` result. This is local Ubuntu WSL, not the organizer's Kali VM. No Kali connection was available or attempted. Ghidra installation/GUI operation was not established.

An initial reviewer path mistake used `../../../../recipes/` for transform, VM, pattern generation and lookup. Each failed with `can't open file ... recipes ... [Errno 2] No such file or directory`. Correcting the extra `../` recovered immediately. This is recorded transparently and is not scored as a guide defect. The corrected native Windows `python` commands below first succeeded as a portability substitute; they were then repeated using actual WSL Python, so the final success evidence is not host-only.

**Task 1 — success for prepared constants.** The fixture already used the exact fields illustrated at `QUICKSTART.md:171`. No extraction or domain reasoning was necessary.

```text
python ../../../recipes/transform.py compare.json
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/transform.py compare.json
  forward check: OK
  candidate bytes: b'CSG_FLAG{byte_order_counts}'
  saved: checker-plain.bin
```

Both invocations produced the same result. The helper's forward check verifies the stated transform, not an absent original executable's entire input path. The narrow model is expressly stated at `QUICKSTART.md:168` and `:178`.

**Task 2 — success for already decoded VM instructions.** The JSON matches the documented program format (`QUICKSTART.md:182`–`:192`).

```text
python ../../../recipes/vm_byte.py machine.json
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/vm_byte.py machine.json
  candidate: 72 / 0x48 / b'H'
  LOAD_INPUT: 0x48 -> XOR: 0x63 -> ADD: 0x74 -> CMP: 0x74 all comparisons: OK
  candidate count: 1
```

This solves the supplied one-byte machine. It does not demonstrate decoding an unfamiliar VM. The full chapter starts by asking the reader to find the dispatch loop and recover semantics (`chapters/06-reverse-engineering.md:381`); its runnable example already declares every opcode at `:386`.

**Task 3 — success, with tested failure recovery.** `register.txt` explicitly supplies memory-order bytes and the guide's generator/length. Joining `61 61 68 62` as `61616862` is ordinary input transcription. Native Windows commands first returned:

```text
python ../../../recipes/pattern.py --length 512
  wrote 512 bytes
python ../../../recipes/pattern.py --find 61616862 --sent pattern.bin
  197
  verified against sent file: pattern.bin ; length: 512
```

A deliberately absent sequence (`python ../../../recipes/pattern.py --find 00000000 --sent pattern.bin`) returned `-1` and `not verified: wrong generator or crash bytes outside sent pattern`; restoring `61616862` returned 197 verified. A more realistic, independently executed WSL recovery checked truncated generated input:

```text
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/pattern.py --length 128
  wrote 128 bytes
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/pattern.py --find 61616862 --sent pattern.bin
  197
  not verified: wrong generator or crash bytes outside sent pattern
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/pattern.py --length 512
  wrote 512 bytes
wsl -d Ubuntu-24.04 -- python3 ../../../recipes/pattern.py --find 61616862 --sent pattern.bin
  197
  verified against sent file: pattern.bin ; length: 512
```

`QUICKSTART.md:203` explains the outside-sent-input failure; the fixture states length 512, so recovery needed no extra domain knowledge. Caution for a novice: the helper still prints numeric 197 before “not verified.” The second line must determine whether to trust it. No actual crash process or saved return-slot verification was possible with these fixtures.

**Task 4 — partial guidance, blocked at raw-evidence-to-constants bridge; paper assessment only.** No ELF was supplied, as the task explicitly states. I could find a starting route but could not honestly claim to have located a real comparison or extracted constants.

`QUICKSTART.md:164` says to select a function address from `afl`; it does not say which candidate or how to recognize the input loop. The deeper chapter improves this: imported `memcmp` cross-references (`chapters/06-reverse-engineering.md:182`), `ie`/startup target when `main` is missing (`:188`), and string virtual-address references (`:190`). GDB argument inspection at `:241`–`:243` provides a concrete route to a comparison table if the relevant call can be reached.

The remaining novice gap is following unfamiliar instructions backward from that comparison to identify the key bytes, key length, rotate width/count and exact operation order. `:208` asks to identify uses and set correct array lengths, while the toy source already reveals its constants before the solver. There is no observed-disassembly-to-JSON worked example. The task's unfamiliar stripped binary may also lack imported comparisons. At this point I stopped rather than writing an expert solver or inventing analysis. Finding instructions is partial success; extracting an unknown check is unverified and beyond the supplied beginner bridge.

## Website and policy checks

Supported browser inventory was actually requested with `cua.getState()` and returned `apps: [], browsers: []`. Website assessment is therefore static source only. `index.html:101` and `:119` make quickstart the default; `:69`–`:73` group shortcuts before the chapters. Section search requires every search word (`:131`), with a fewer-words/synonym fallback at `:137`. Copy buttons include clipboard, legacy copy and manual-selection fallbacks (`:87`–`:93`). These features should help navigation, but live search, scrolling, clipboard behavior, narrow-screen layout and downloads were not verified.

Checked the original `Practice Environment Setup Guide.pdf` using fitz text extraction, not guide assertions. PDF page 4 describes separate remote Kali with VPN/SSH/RDP; page 5 permits non-generative-AI libraries, dependencies, plugins and packages while requiring approval for unlisted standalone applications. Page 7 expressly permits physical/electronic notes, cheat sheets, personal repositories and scripts created before competition. Pages 8–9 prohibit generative AI and external assistance during competition. Pages 6 and 21 prohibit challenge-file uploads to online services. This review is preparatory, not a competition solve.

`review/tool-policy.json:117`/`:123` place Python 3 in WSL; `:267`/`:273` place Ghidra in WSL; `:1539` lists Kali radare2; `:1989` and `:2119` place Binary Ninja Free and IDA Free in the unapproved sheet. The tested helper route and proposed tool locations are consistent with those records. Availability of local Ubuntu software does not prove organizer installation.

The guide's repeated “confirm prepared notes/scripts” caveat is unnecessary for the materials expressly allowed on PDF page 7: `README.md:25`, `QUICKSTART.md:234`, and reverse chapter `:7`. The README is technically correct that the workbook alone does not establish permission, but it fails to use the supplied PDF that does. Removable-media permission remains a separate matter, not established by that page.

## Minimal improvements, without adding another long chapter

1. Keep the existing three helper cards. Add one link immediately before their input JSON: “Have only a binary? Start here.” Replace the current toy source-first exercise with a compact annotated disassembly/decompiler excerpt showing where each of `key_hex`, `rotation` and `expected` comes from. Show one byte through the forward transform. This addresses the actual missing bridge rather than adding tool breadth.
2. Make the raw-binary route choose one beginner default, Ghidra, with exact string-reference navigation and a single fallback for absent strings/imported comparisons. Keep the radare2 route as an alternative. The present `afl` candidate selection (`QUICKSTART.md:164`) is too open-ended for a first reverser.
3. Move advanced anti-analysis, emulation and unusual-pattern material behind a clear “advanced reference” boundary. Preserve it for experienced readers; do not put it on the shortest route to extracting a byte table. The chapter's 552 lines substantially exceed the four-task requirement.
4. Replace repeated notes/scripts permission caveats with one accurate page-7 policy sentence in the entry page and a link elsewhere. Keep per-command machine labels; those prevented real environment confusion and should not be cut.
5. On pattern lookup failure, make “NOT VERIFIED” the leading line; only present the numeric position as a possible full-generator match. On VM/model mismatch, link to one worked semantic correction instead of only “correct the decoded semantics” (`QUICKSTART.md:192`).

Final outcome: three prepared-fixture successes, one successful bounded failure-recovery exercise, and one paper-only raw-reversing assessment that identifies a major beginner bridge still missing. No end-to-end raw ELF solve, organizer Kali test, GUI decompilation or live website test was performed.
