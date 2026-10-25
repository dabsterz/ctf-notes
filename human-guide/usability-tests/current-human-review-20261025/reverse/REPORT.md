# Current human review: reversing

Persona: intermediate Linux user, new to reversing. Reviewed the current shipped guide on 2026-10-25, independently of prior reviews. Overall **7.6/10** (equal mean of five dimensions).

| Dimension | Score | Reason |
|---|---:|---|
| Findability | 8 | Quick-reference task table immediately identifies all three helpers. Stripped-binary guidance requires an extra chooser/sidebar hop. CPTS search gives labeled results. |
| Command usability | 9 | All three exact shipped helpers ran successfully with filename adaptations in actual WSL; output includes useful validation. |
| Clarity | 7 | Transform order, supported VM scope, and memory-order bytes are explicit. Extracting constants from stripped code still assumes reversing knowledge. |
| Instruction economy | 8 | Three concrete inputs need only short cards. The unfamiliar-ELF route needs several chapter sections and interpretation. |
| Recovery | 6 | Pattern no-match guidance allows recovery on supplied bytes. Successful lookup can also validate incorrectly ordered bytes; harder static-analysis recovery remains high-level. |

## Scope and reading path

1. Read this sandbox's TASKS.md and its compare.json, machine.json and register.txt. Read human-guide/README.md as instructed.
2. Followed README to QUICKSTART.md. Its task table and Static reversing, XOR and rotation, Small VM, Crash offset cards supplied the routes. Read the short quick reference, not the complete handbook.
3. Followed Static reversing to TOOL-CHOOSER.md#reverse-engineering (lines 87–102). Used a narrow heading/keyword search in chapters/06-reverse-engineering.md, then read sections 4–5 (lines 163–219), 8 (309–332), and the related worked checker and debugger sections 3 and 6 (112–162, 221–266). No source skills, builder code, fixture generators, answer keys, previous reviews, or other task folders were read.
4. Independently opened index.html in real local Chrome through Playwright. Expanded Vernon's CPTS notes and opened All CPTS notes. Search `buffer` gave 31 sections and only a file-transfer CPTS hit, so searched `strings` (45 sections), then chose the visibly labeled CPTS / PrivEsc/Linux/SUID Sticky Bit result. This is relevant to initial inspection of a suspicious binary, not a replacement reversing workflow.

No human elapsed-time estimates are asserted. Browser automation only operated/read rendered UI; it did not inspect embedded guide data or solve challenges. No guide edits, installs, external research, target execution, or remote requests were performed. No algorithms were invented.

## Actual command results

Commands ran inside Ubuntu-24.04 WSL with Python 3.12.3. Working directory was `/mnt/c/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/usability-tests/current-human-review-20261025/reverse`, whose recipes directory contains the supplied exact helpers. No interpreter substitution was needed. `commands.log` preserves commands and output.

| Task | Status | Evidence |
|---|---|---|
| 1: supplied XOR/ROL constants | Passed | `python3 recipes/transform.py compare.json` printed `forward check: OK`, `candidate bytes: b'CSG_FLAG{byte_order_counts}'`, and wrote checker-plain.bin. This verifies the supplied mathematical checker, not an absent executable. |
| 2: decoded one-byte VM | Passed | `python3 recipes/vm_byte.py machine.json` printed `candidate: 72 / 0x48 / b'H'`, trace `LOAD_INPUT: 0x48 -> XOR: 0x63 -> ADD: 0x74 -> CMP: 0x74 all comparisons: OK`, candidate count 1. |
| 3: crash offset | Passed | `python3 recipes/pattern.py --length 512`, then `python3 recipes/pattern.py --find 61616862 --sent pattern.bin` printed `197` and `verified against sent file: pattern.bin ; length: 512`. Removing spaces from the explicitly memory-ordered crash bytes was the only input adaptation. |
| 4: unfamiliar stripped ELF | Navigation assessed; partial instructional bridge | No binary was supplied, so no ELF was analyzed and no constants were extracted. The guide supplies strings, function listing, xrefs, entry-point inspection, decompilation and argument-memory inspection. It does not fully teach the new reverser how to recognize the startup call target or trace key, rotation and stored-table data into the helper JSON. |

The fourth task's limitations are not blamed on missing fixture execution: it was expressly navigation-only. The missing teaching bridge is observable in the instructions. `QUICKSTART.md:171` says select a function from afl. The deeper chapter at line 188 says inspect the startup routine's call target without showing a representative startup disassembly or how to recognize that target. Section 5 says follow string references but does not show the beginner the relevant reference UI action. Section 3 is helpful, but its source already declares key and expected arrays, and its compile command preserves debug symbols. Section 6 usefully explains memcmp argument registers and expected-buffer inspection; there is no equivalent illustrated extraction of a repeated key and rotation from an unknown loop.

Kali/radare2 and Ghidra were walkthrough-only here. Their execution/availability was not validated, and no replacement tools were used to claim completion of task 4.

## Failure and recovery

A deliberate byte-order probe, `--find 62686161 --sent pattern.bin`, returned **55, verified**, although register.txt explicitly supplied memory order `61 61 68 62`. Returning to the supplied ordering gave **197**. This is not a helper bug: both four-byte sequences occur in the generated pattern. It demonstrates that the word "verified" means membership in sent data, not correctness of debugger byte interpretation.

To exercise the documented no-match route explicitly, ran `python3 recipes/pattern.py --find ffffffff --sent pattern.bin`. Output: `-1` and `not verified: wrong generator or crash bytes outside sent pattern`. This was an intentional invalid-byte probe, not the supplied crash value. Following the quick-reference instruction to check the generator/bytes, reread register.txt, kept its stated memory order, and reran `--find 61616862 --sent pattern.bin`, recovering 197 with verification. No new solver or undocumented conversion was added.

## Website and CPTS check

At 1440×1000, commands were comfortably readable and displayed without horizontal clipping on the tested note. Search results clearly distinguish CPTS from the edited competition chapters. The CPTS index explicitly says these are original study notes, not a competition-approved tool list. The note itself shows `Personal reference · Event tool rules`; README separately warns the notes are unfiltered. I would consult event rules/lookup before executing their commands. None of the CPTS commands was executed.

Page: `index.html#cpts-privesc-linux-suid-sticky-bit-a4af3b7a--suid-sticky-bit`.

Clicked Copy on the two-line binary-inspection block and read back the actual browser clipboard after enabling clipboard permissions in the test context. It exactly contained:

```text
strings /usr/bin/passwd_flag
cat /usr/bin/passwd_flag
```

One screenshot was present. Full size changed its control to Fit width; DOM rendered dimensions matched the native 824×183 image. Visually inspected the resulting screenshot: terminal text is legible. Fit width restored successfully. `browser.log` records these checks; browser scripts and PNG evidence are alongside this report.

Harness limitations and recovery: the initial exact-text locator matched a hidden collapsed sidebar entry and timed out. Replaced it with the visible search-result link; this was automation targeting, not a human navigation failure. The initial clipboard read was denied by browser permissions; enabling clipboard-read/write for the owned test context allowed an actual content check. A transient Copy label was sampled before it updated; screenshots show Copied. Successful harness runs close their owned Chrome browser; the failed node run exited. No desktop user tabs were operated.

## Top three actionable findings

1. **Add one stripped-binary extraction walkthrough.** At `chapters/06-reverse-engineering.md:188`, `:206`, and `:309`, show a short annotated startup/call trace and transform loop; explain how to identify the input pointer, repeated key length, rotation and expected bytes, and transfer those observations into checker.json. The current source-visible toy at `:112` is helpful practice but does not bridge the unfamiliar-binary task for this persona.
2. **Link the static card directly to its detailed workflow.** `QUICKSTART.md:171` only links Reverse tool choices. Add direct links to reverse chapter sections 4–6, with a clear stripped/no-main branch. The chooser at `TOOL-CHOOSER.md:87` provides alternative tools and first actions, but leaves the beginner to locate the actual walkthrough through chapter navigation.
3. **Make offset verification's limitation explicit.** At `QUICKSTART.md:201–210`, say that sent-file verification checks membership only and that a reversed register value can accidentally produce another valid offset. Show one concise distinction between register numeric display and bytes in memory order, plus the existing requirement to confirm the overwrite position in the actual program when one is available. The supplied task is clear; the broader recovery wording could prevent false confidence.
