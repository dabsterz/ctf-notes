# Independent human-use review: reverse / misc

Persona: experienced CTF generalist with basic reversing familiarity, seeking a fast lookup under time pressure. This is a constrained human-style reviewer simulation, not a study with a human participant. The handbook was the sole technical reference. I started with README.md and the assigned START.md. I did not inspect hidden fixture generators, server code, answer keys, original skills, earlier reviews, other reviewers, or the internet. No handbook files were modified.

## Outcome

| Task | Status | Exact result | Evidence and scope |
| --- | --- | --- | --- |
| Checker | Completed, executed | `CTF{invert_in_order}` | Copied guide rotation helpers; adapted JSON input, inverse composition, and forward verification. All 20 output bytes exactly matched `expected`. |
| Crash offset | Completed, executed | `173` | Copied guide pattern script unchanged; `--find 61616763` returned 173. Generated the specified 512-byte pattern and verified bytes 173:177 equal `crash.bin`. |
| Custom VM | Completed, executed | decimal `75`, hex `0x4b`, ASCII `K` | Applied the guide's subtract/mask and XOR inverse rules, adapted its interpreter to JSON opcode rows, and added the supplied LOAD_INPUT/CMP semantics. Trace: `4b -> 68 -> 6f`; `111 == 111: True`. |
| Shared tool lookup | Completed, document lookup | radare2: **Kali**, row 123; local alternative: **Ghidra in Windows WSL**, row 29 | TOOL-MATRIX.md:170 and :32, corroborated by reverse chapter:14–15. This establishes the documented route, not actual installation or operation. |

No actual binaries, exploitation, debugger sessions, or external endpoints were used. There were no failed executions or repair retries. All Python runs used **host Windows Python 3.14.4**, a portability proxy only; WSL and Kali were not tested. No website/browser UI was tested.

## Chronological navigation and command log

Commands ran from the repository root unless stated. PowerShell excerpts used `$a=Get-Content <path>; START..END | ForEach-Object { '{0}: {1}' -f ($_+1),$a[$_] }`, where the zero-based ranges below correspond to the recorded one-based lines. This reads a bounded displayed excerpt; it did not expose the full chapter to the reviewer.

1. `Get-Content -Path human-guide/README.md -TotalCount 80` — returned all 37 lines. Learned that shorter category chapters and TOOL-MATRIX.md exist. No browser was opened.
2. `Get-Content -Path human-guide/usability-tests/round-1/reverse-misc/START.md -TotalCount 80` — read the assigned three tasks and common lookup.
3. `Get-ChildItem -Path human-guide/chapters -Name` and `Get-ChildItem -Path human-guide/usability-tests/round-1/reverse-misc -Name` — title navigation. Selected reverse engineering and binary exploitation; miscellaneous appeared a possible VM route. `Get-Date -Format o` returned `2026-10-25T21:53:50.0571101+07:00`.
4. `Get-Content .../reverse-misc/checker.json`, `Get-Content .../reverse-misc/payload.json`, and `Format-Hex -Path .../reverse-misc/crash.bin` — read only assigned artifacts. Crash bytes were `61 61 67 63` in memory order.
5. `rg -n '^#{1,4} |ROL|rotate|rotation|de_bruijn|virtual machine|VM' human-guide/chapters/06-reverse-engineering.md human-guide/chapters/08-binary-exploitation.md human-guide/chapters/11-miscellaneous.md` — one combined title/keyword lookup, 80 result lines. Located transform section 8, pattern section 5, and reverse VM section 10. Did not open the miscellaneous VM section because reverse already had the concrete interpreter.
6. Opened reverse chapter **307–347** (zero-based `306..346`, 41 lines). Found `rol8`, `ror8`, the inverse direction warning, XOR reversal, and modular subtraction. Adapted into `reverse-misc/solve_checker.py` (initial write). `python --version` returned `Python 3.14.4`. `python human-guide/usability-tests/round-1/reverse-misc/solve_checker.py` succeeded immediately.
7. Opened binary exploitation **179–242** (`178..241`, 64 lines). Copied lines **186–220** unchanged to `reverse-misc/pattern.py` with `$a[185..219] | Set-Content -Encoding utf8 .../pattern.py`. Ran `python human-guide/usability-tests/round-1/reverse-misc/pattern.py --find 61616763`; output `173`.
8. Opened reverse chapter **377–428** (`376..427`, 52 lines). Adapted the tiny interpreter into `reverse-misc/solve_vm.py`. Ran `python human-guide/usability-tests/round-1/reverse-misc/solve_vm.py`; result and comparison succeeded immediately. Used the already read inverse rules from section 8; did not invent a solver algorithm or import an external one.
9. `rg -n -i 'radare2|ghidra' human-guide/TOOL-MATRIX.md human-guide/chapters/06-reverse-engineering.md` — 16 result lines. The matrix supplied exact platform, version, and workbook coordinates. Chapter rows supplied the static-analysis route. No tool installation was attempted.
10. In the assigned `reverse-misc` directory, ran `python pattern.py --length 512` (output `wrote 512 bytes`), then `python -c "from pathlib import Path; p=Path('pattern.bin').read_bytes(); c=Path('crash.bin').read_bytes(); print('length:', len(p)); print('slot at 173:', p[173:177].hex()); print('crash bytes:', c.hex()); assert p[173:177] == c; print('512-byte pattern verification passed')"`. This added only basic I/O verification, not a new offset algorithm.
11. Opened reverse chapter **7–46** (`6..45`, 40 lines) to verify environment caveats. It explicitly separates Windows native, Windows WSL, and Kali. A second `Get-Date -Format o` returned `2026-10-25T21:54:34.1955943+07:00`.
12. Counted lines/whitespace-separated words from the already displayed excerpt ranges and original queries for this report. These were measurement replays, not new navigation or new guide content. Wrote this report and companion JSON.

The timestamps are actual tool timestamps, not a claim about human reading speed. No reading-time estimate or simulated 10-minute duration is used.

## Effort and text burden

A lookup means a guide navigation/read action, including the directory-title inventory. There were **8 guide lookups**: README, chapter inventory, heading/keyword query, three recipe excerpts, tool query, and environment excerpt. There were also **2 fixture-read actions** (START, grouped artifact reads). The chronological log has extra execution/measurement events; these are not additional reference lookups. No dead-end search or wrong-page detour occurred. The miscellaneous title results were incidental scan burden, not a separate chapter visit.

| First actionable run / result | New displayed reference material | Cumulative displayed guide text before that point |
| --- | --- | --- |
| Checker solver | README 37 lines / 543 words; title/keyword results 80 / 1,013; transform excerpt 41 / 356 | **158 lines / 1,912 words** |
| Offset `--find` | Pattern excerpt 64 / 332 | **222 lines / 2,244 words** |
| VM solver | VM excerpt 52 / 543 | **274 lines / 2,787 words** |
| Tool answer | Tool query 16 / 457 | **290 lines / 3,244 words** |
| Final environment verification | Environment excerpt 40 / 372 | **330 lines / 3,616 words** |

These are exposed text counts, not words a human necessarily reads. Query counts include path/line prefixes. Directory names, fixture text, tool wrappers, and script output are excluded. The broad title scan inflated the exposed burden; a user who already knows the chapter anchors could do better. No chapter or whole corpus was ingested.

There were **3 initial script writes**, **2 substantive adaptation passes**, **0 repair edits**, and **0 failed command attempts**. Six Python invocations included one version check and five task runs. The offset recipe needed zero source edits and one `--find` argument substitution. `python3` was replaced by host `python` for the proxy execution.

Adaptations were not silently treated as copy-paste:

- Checker: added JSON/Path input plumbing, parsed the hex key, composed `ror8(y, rotation) ^ key[i % len(key)]`, decoded ASCII, and added a forward comparison. The operation inverses come directly from reverse:309 and :327, but this complete data-to-answer loop is absent from the displayed recipe.
- Pattern: copied the full script exactly. Only shell command, path, and hex argument differed. The extra truncation check read files and compared an already determined slice.
- VM: changed numeric flat bytecode into JSON instruction rows, mapped string opcode names, supplied LOAD_INPUT and CMP handlers from the task specification, adjusted logging, added a final success assertion, and calculated the candidate by reversing the supplied XOR/ADD sequence using section 8. This is a meaningful small implementation, not merely substituting constants into the example. The guide supplied the dispatcher scaffold, byte-width mask, instruction budget, and inverse rules.

## Scoring

Higher cognitive-load score means less load. Ratings are independent and apply only to this tested slice.

| Dimension | Score / 5 | Weight | Reason |
| --- | ---: | ---: | --- |
| Findability | 4 | 25% | Descriptive chapter/section titles found all routes on the first query; a symptom-to-recipe index would avoid a long title scan. |
| Command readiness | 3 | 25% | Pattern is immediately runnable. Checker requires a data loop; VM requires input/comparison and representation adaptation. |
| Interpretation | 4 | 15% | Inversion direction, memory-order hex, `-1`, byte masking, and environment boundaries are unusually explicit. VM example demonstrates output production rather than solving an input comparison. |
| Cognitive load | 3 | 25% | Useful code is embedded among background and advanced-case discussion; 330 exposed lines and two implementation passes are noticeable for a timed lookup. |
| Tool/environment clarity | 5 | 10% | Platform table and workbook coordinates agree, distinguish WSL from native Windows, and warn installation is not assured. |

Weighted mean = `4*0.25 + 3*0.25 + 4*0.15 + 3*0.25 + 5*0.10 = 3.60`.

**Timed cheat-sheet usefulness: 7.2/10. Study-reference usefulness: 8.5/10.** The latter reflects strong explanation and safeguards in the inspected routes; it is not a rating of unread chapters. Task-specific usability impression: checker 4/5, offset 5/5, VM 3/5, shared lookup 5/5 (these are descriptive, not a second scoring formula).

## Findings and top three fixes

1. **Put a complete transform-to-input recipe before the rotation unit test.** `human-guide/chapters/06-reverse-engineering.md:309` explains direction well, but :314–324 supplies only rotation helpers and a round-trip test. :327 supplies inverse rules in prose. The checker was solvable without missing knowledge, yet the reviewer still had to assemble parsing, key repetition, inverse order, and forward validation. A compact input/expected/key example would improve readiness immediately.
2. **Add a small input-check VM example alongside the emitting toy.** `human-guide/chapters/06-reverse-engineering.md:384` lists load/XOR/add/emit/halt, :402–406 implements those operations, and :410 asserts a fixed emitted output. It does not show the common LOAD_INPUT/CMP/success condition route. The prose at :379 and table at :418 help modeling, but the timed user still needs meaningful new code. Include a one-byte input, comparison, trace, candidate derivation, and explicit 8-bit state reset.
3. **Provide a short task-first jump list and keep advanced cautions below it.** `human-guide/README.md:13` begins the category contents description; `human-guide/chapters/06-reverse-engineering.md:307`, :377, and `human-guide/chapters/08-binary-exploitation.md:179` are the exact useful destinations. Add links labelled “invert XOR + rotate,” “four crash bytes -> offset,” and “custom VM input check.” In the transform excerpt, :329–346 moves into prefix hashes and MBA; the VM excerpt goes from :414 into emulation tooling at :416–428. Those are useful study material but add scrolling burden to these small tasks.

The pattern recipe is the strongest existing cheat sheet: `human-guide/chapters/08-binary-exploitation.md:208` describes the argument, :239 gives byte order and failure interpretation, and :241 warns against comparing generators. The only optional improvement is a direct `--find HEXBYTES` command adjacent to the script and a reminder to verify the offset lies within the pattern length actually sent. Here that verification passed.

## Example concise rewrite

**Before** — reverse:309 explains transform direction; :314–324 tests rotation; :327 says how XOR and modular addition invert. A reader must join them into a solver.

**After** — put this short recipe before the explanatory material:

> **Stored table is `ROL8(input[i] XOR key[i % len(key)], r)`?** Undo operations right-to-left: rotate right, then XOR. With the `rol8`/`ror8` helpers below, fill `expected`, `key`, and `r`, then run:
>
> ```python
> plain = bytes(ror8(y, r) ^ key[i % len(key)]
>               for i, y in enumerate(expected))
> assert [rol8(x ^ key[i % len(key)], r)
>         for i, x in enumerate(plain)] == list(expected)
> print(plain)  # Decode only after the forward check passes.
> ```
>
> **If ADD is another stage:** invert it with `(value - amount) & 255`, in reverse stage order. Keep a forward check against the original table.

This rewrite stays within algorithms already present in the guide and makes the successful path explicit.

## Limits and artifacts

The input transforms and VM opcode semantics were already extracted by the fixture. This did not test finding a native checker in a decompiler, recovering opcodes, recognizing an unfamiliar cipher, installing tools, exploiting a stack overflow, or live VM debugging. The offset bytes were provided in memory order. The tasks are deliberately easy and do not validate broader advanced coverage.

Safe local artifacts are under `human-guide/usability-tests/round-1/reverse-misc/`: `solve_checker.py`, `pattern.py`, `pattern.bin`, and `solve_vm.py`. Result assertions and traces were executed; common tool availability is documentary only. No actual browser interactions or human reading-time claims are made. PowerShell displayed some punctuation as mojibake in excerpts; I did not attribute that terminal-decoding behavior to a website defect.
