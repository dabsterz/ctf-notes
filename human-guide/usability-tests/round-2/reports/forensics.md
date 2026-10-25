# Round 2: simulated intermediate Windows forensic solver

This is an independent simulated-human walkthrough, not a participant study. No human timing claims are made. No internet, browser, WSL or Kali execution was used. The three assigned artifacts were solved using native Windows Python as the allowed portability proxy.

## Results

| Task | Status | Candidate | Evidence |
| --- | --- | --- | --- |
| PNG | Completed | `CTF{new_png_tail}` | Unmodified helper walked IHDR, IDAT and IEND, reported all three CRCs OK, and saved 17 trailing bytes in `forensics/png-trailer.bin`; saved text independently read back. |
| tar | Completed | `CTF{older_tar_entry}` | Unmodified helper saved both `note.txt` occurrences as `tar-parts/000000.bin` (20 bytes) and `000001.bin` (34 bytes). Manifest retains original name and occurrence index. The first member contains the candidate; later member says it contains no answer. |
| event | Completed | `2026-10-25T03:04:05Z \| C:\Temp\runner.exe --mode audit` | Supplied JSON identifies Microsoft-Windows-Security-Auditing event 4688, executable `C:\Temp\runner.exe`, and that full command line. |

The event establishes an audited process start at the supplied UTC timestamp with the recorded command line. It does not establish successful completion, malicious intent, payload effects, or a file-creation event. These distinctions are explicitly supported by QUICKSTART.md:108-113. The export uses `TimeCreated`, while the card names `SystemTime`; mapping the supplied timestamp to UTC used its `Z` suffix and ordinary export-field interpretation.

## Chronological lookups and actions

Lookup count is six reference operations (two initial files, one targeted search, two separate excerpts, one post-solve table review); artifact reads and execution are not counted as guide lookups.

1. Read README.md and assigned START.md. README clearly directed me to QUICKSTART and TOOL-CHOOSER and explained included recipes.
2. Targeted `rg -n` for PNG/IEND/tar/event/Sysmon/forensic/memory/PCAP/disk across QUICKSTART.md and TOOL-CHOOSER.md; listed only the assigned fixture folder.
3. Read QUICKSTART.md:61-114, covering all three relevant task cards. No detailed chapter needed.
4. Read TOOL-CHOOSER.md:41-68 for disk, memory and PCAP choices.
5. From the assigned forensics folder, ran `python ../../../recipes/png_tail.py carrier.png`, `python ../../../recipes/tar_keep.py evidence.tar --out tar-parts`, and `python -m json.tool events.json`. Both recipe files were unchanged. All commands succeeded on the first attempt.
6. Read saved PNG bytes, first tar member and tar manifest with PowerShell `Get-Content` to verify recovery and preservation.
7. After solving, inspected Steganography and OSINT rows at TOOL-CHOOSER.md:71-85 and :145-159, alongside the previously read Forensics/Network rows.

Code edits: none. Invented algorithms: none. Local glue/adaptations: `python` replaced `python3`; recipe paths were adjusted to the task working folder; Python's standard JSON pretty-printer replaced the WSL `jq` suggestion; PowerShell file reads replaced `strings` for these already-readable outputs. No custom parser or extraction logic was needed. Initial PowerShell reads rendered UTF-8 punctuation incorrectly; using `Get-Content -Encoding UTF8` resolved display noise. No recipe or artifact-processing errors occurred.

## Tool selection

- Disk image: Autopsy on Windows for GUI artifact correlation; indexing may be slow. Sleuth Kit in WSL is the precise extraction alternative, but requires the correct partition offset.
- Memory dump: Volatility 3 in WSL, beginning with `vol -f memory.raw windows.info` and `windows.pslist`; symbol/layer compatibility may prevent useful parsing. The table explicitly distinguishes Kali's Volatility 2 entries.
- PCAP: Wireshark on Windows for conversations and streams; TLS payloads remain opaque without suitable secrets. TShark on Windows provides repeatable summaries, with distinct capture/display filter syntaxes to learn.

These are table-supported selections, not claims that the tools were installed or executed.

## Table clarity and material issues

The four requested tables consistently provide the decision, strength, weakness, environment and first action together. Forensics rows (TOOL-CHOOSER.md:47-53) distinguish disk, memory and artifact parsers well. Network rows (:63-68) distinguish offline capture analysis from active scanning. Steganography rows (:76-83) distinguish carrier families and false positives. OSINT rows (:153-157) separate clues from corroboration and keep local and browser workflows understandable. No material tool-selection error was demonstrated in this bounded review; dependency availability and version behavior were not tested.

Two small usability gaps remain:

- QUICKSTART.md:113 gives only a WSL `jq` route even though the process-event card is presented as Windows PowerShell. A native `Get-Content -Raw events.json | ConvertFrom-Json | Format-List` option would remove an unnecessary environment switch for Windows readers.
- QUICKSTART.md:109 names `SystemTime`; the supplied export uses `TimeCreated`. Adding that common alias would make interpretation fully mechanical, similar to the command-line alias already documented at :111.

TOOL-CHOOSER.md:63 compresses the Wireshark UI route: explicitly applying the selected conversation as a filter before following a packet's TCP stream would be easier for a newcomer than “select packets.” This is a minor instruction-precision concern, not a verified application defect.

## Ratings

| Dimension | Score / 5 | Weight | Reason |
| --- | --- | --- | --- |
| Findability | 5 | .25 | Three adjacent cards located by one targeted search. |
| Command readiness | 4 | .25 | Included scripts ran unchanged; Windows invocation and JSON-viewing adaptations remained. |
| Interpretation | 5 | .15 | CRC/trailer evidence, duplicate-member preservation and event limits were explicit. |
| Cognitive load (higher = less burden) | 5 | .25 | No algorithm construction, detailed chapter reading or broad tool trial needed. |
| Tool/environment | 4 | .10 | Useful explicit environment labels, but local Windows JSON inspection is missing. |

Overall: **9.3/10** (2 × weighted mean). Separate study usefulness: **9.0/10**, reflecting clear conceptual limits and tool tradeoffs, while deep practical capability and real event setup remain untested. This score assesses this revised guide and these fresh tasks independently; it is not a measured round-to-round improvement or participant result.

