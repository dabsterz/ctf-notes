# Round 2 reverse/misc simulated human review

Persona: experienced CTF generalist with basic reversing. This is a simulated human walkthrough, not a real participant study or a timing measurement. Execution used native Windows Python as a portability proxy. WSL, Kali, external documentation, and browser interactions were not exercised.

## Frozen solve assessment

Scores were frozen after the three solves and before inspecting the builder, app, tests, generated payload, or complete tool-matrix rows.

| Dimension | Score / 5 | Reason |
| --- | ---: | --- |
| Findability | 5 | A single targeted search found all three cards and the format-specific tool rows. |
| Command readiness | 4 | Unchanged helpers solved every fixture. Interpreter and relative path adaptations were needed for this test layout; verification of the offset required a short additional command. |
| Interpretation | 5 | Forward-check output, VM trace, and the offset card made success and constraints clear. |
| Cognitive load (higher is less burden) | 5 | Only a 56-line quick-reference excerpt and the reverse table were needed; no detailed chapters. |
| Tool/environment | 4 | Event environments are explicit, but the WSL-labelled Python cards do not document a native-Windows portability route. Native execution here does not establish event approval. |

Weighted overall: **9.3/10** using 2 × (0.25×5 + 0.25×4 + 0.15×5 + 0.25×5 + 0.10×4). Separate study usefulness: **9.0/10**; concise models and transparent outputs help learning, but these fixtures start after constants and VM semantics have been extracted.

## Chronological lookup and execution record

Technical lookup count: **6**, counted per source access: README, search of QUICKSTART, search of TOOL-CHOOSER, QUICKSTART excerpt, TOOL-CHOOSER excerpt, and pattern helper `--help`. Reading START and fixture inputs is excluded. Post-freeze reviewer inspection is excluded. The two searches shared one shell call.

1. Read `human-guide/README.md`, then assigned `reverse-misc/START.md`. README directly recommended QUICKSTART and TOOL-CHOOSER and explained the recipe layout.
2. Searched only QUICKSTART and TOOL-CHOOSER for reverse/checker/rotation/cyclic/offset/VM/radare/.NET/Android terms. Enumerated only the assigned fixture directory. No answer key, server, preparation script, earlier reports/fixtures, original skill corpus, or internet was read.
3. Read QUICKSTART lines 150–205 and TOOL-CHOOSER lines 87–103; read checker.json, vm.json, and a `Format-Hex` view of crash.bin. The latter showed `63 62 61 62` in memory order. PowerShell's default text decoding initially displayed typographic arrows and middle dots incorrectly; code and substantive text remained readable. Later reviewer reads explicitly used UTF-8.
4. From the assigned fixture folder, ran `python ../../../recipes/transform.py checker.json`. Output: `forward check: OK`, `candidate bytes: b'CTF{new_transform}'`, `saved: checker-plain.bin`. Completed checker.
5. Ran `python ../../../recipes/vm_byte.py vm.json`. Output: `candidate: 90 / 0x5a / b'Z'`; trace `LOAD_INPUT: 0x5a -> XOR: 0x48 -> ADD: 0x51 -> CMP: 0x51 all comparisons: OK`; candidate count 1. Completed VM. Independently readable arithmetic: 0x5a XOR 0x12 = 0x48; adding 9 gives 0x51 (81), the required comparison.
6. Ran `python ../../../recipes/pattern.py --help`. Help confirmed `--find` takes four memory-order bytes as eight hex digits.
7. Ran `python ../../../recipes/pattern.py --length 512`, which wrote a 512-byte pattern.bin. Ran `python ../../../recipes/pattern.py --length 512 --find 63626162`, which returned `281`.
8. Added a short verification command using pathlib, a byte slice, and `find`/`rfind`. My first command accidentally hard-coded `211`, not the returned `281`, and correctly printed `matches crash bytes: False`. This was reviewer transcription error, not a guide or helper failure. Corrected to `offset=281`; output: length 512, bytes `63626162`, match True, unique occurrence True, and inside sent length True. Completed offset.
9. Selected Ghidra, approved WSL W29, as the static Windows/WSL alternative to Kali radare2. Native binaries: Ghidra for decompilation and cross-references, objdump for quick disassembly, x64dbg for native Windows debugging. .NET: native Windows dnSpyEx; Android APK/DEX: Kali jadx, with native `.so` code routed back to native reversing. No availability or GUI operation was claimed.
10. Froze scores and results, then began the separate review below.

Code edits during solving: **none**. Recipe sources were neither read nor modified during the solves. Command adaptations: `python3` became the installed Windows `python`; recipe paths became `../../../recipes/…` to keep generated files in the assigned folder. Invented glue: `Format-Hex` to read the crash bytes, and the pathlib verification one-liner. No solver algorithm was invented. The helper's forward check was used as checker evidence, not described as an independent validator.

## Separate post-freeze tool-table review

Inspected Reverse (`TOOL-CHOOSER.md:87`), Pwn (`:119`), and Malware (`:134`) against the corresponding entries in TOOL-MATRIX. No material tool capability or event-environment error found. Matrix is local supplied-policy evidence; no online/version verification was attempted.

- `TOOL-CHOOSER.md:93–100`: format-specific selection is accurate and readable; Ghidra WSL, radare2 Kali, x64dbg Windows, dnSpyEx Windows, and jadx Kali match the matrix. The warnings distinguish decompilation from execution.
- `TOOL-CHOOSER.md:125–130`: checksec version-sensitive syntax, GEF's supplied `/opt/tools/gef.py` path, gadget limitations, Ncat's Nmap association, and strace's Linux/execution limitations are materially sound. A minor optional clarity improvement at `:127` is to say explicitly that the shown startup action is for GEF only; the combined pwndbg/GEF row supplies no pwndbg launch action.
- `TOOL-CHOOSER.md:140–145`: FLOSS, capa, Office tooling, YARA, and UPX roles and limitations are sound. UPX preserves the input by producing a separate output. Static versus runtime analysis is clear.
- Low-priority usability opportunity at `QUICKSTART.md:203`: include an optional ready-to-run check of the recovered bytes at the reported offset; the existing instruction says to check the range but does not supply the verification command. This would remove the only invented checking glue and reduce transcription errors.

## Separate post-freeze code review

Inspected the git diff and relevant implementation in `build.py` and `assets/app.js`; this was code inspection, not simulated human solving. No material defect was found in the changed download or section-link implementation for the current generated guide.

- `build.py:79–106` adds explicit chapter-scoped anchors to the merged Markdown and rewrites same-file and cross-file section references while preserving fenced code.
- `build.py:109–117,233` embeds recipe text; `assets/app.js:117–126` uses the literal relative href as a key, checks own properties, creates a text Blob, downloads with the original filename, and revokes the Blob URL. The downloaded file remains a script the user runs explicitly.
- `python -B -m unittest discover -s human-guide/review -p test_builder.py -v`: **5 passed**. `node --check human-guide/assets/app.js`: exit 0.
- Read-only generated-artifact inspection: **8 embedded recipe sources**, **0 source mismatches**, **0 broken embedded section links**, **0 broken merged section links**. This check read generated data and compared it to recipe files only after scores were frozen.
- Browser click/download behavior and visual layout remain unverified. Source inspection and syntax checks do not establish real browser execution. The merge implementation is purpose-built for the current ATX-heading/inline-link Markdown style; no claim is made that it implements every Markdown dialect.

No guide, builder, app, or test source was changed. Assigned-folder artifacts are checker-plain.bin and pattern.bin; this report and its JSON companion are under the requested reports directory.

## Final-fix review (scores remain frozen)

Reviewed the later `pattern.py --sent` addition, QUICKSTART crash-offset command, GEF/pwndbg wording, and table-inline-code pipe normalization in `build.py`. No material issue found in these changes. The new `--sent pattern.bin` route addresses the earlier offset-verification observation without user-written checking glue: temporary synthetic fixtures confirmed acceptance when the four-byte match ends exactly at the file boundary, rejection when the sent file is one byte too short, rejection of a different-generator file, rejection of an absent needle, and rejection of `--sent` without `--find`. Temporary files were confined to the assigned reverse-misc folder and cleaned; the original solve fixtures and results were unchanged. All **6 builder tests passed**, including the new table-pipe regression test. A focused rendering check confirmed the actual ROPgadget row yields exactly `ROPgadget --binary challenge --only 'pop|ret'`, and non-table inline/fenced code retains its literal backslashes. A targeted scan found no other escaped-pipe occurrences in QUICKSTART, TOOL-CHOOSER, or the human chapters that would be affected. The combined debugger row now explicitly labels its GEF route and directs pwndbg users to their configured debugger or plain GDB fallback. These are post-freeze code checks, not repeated solves or a new usability rating; no real-browser behavior was verified by this reviewer.
