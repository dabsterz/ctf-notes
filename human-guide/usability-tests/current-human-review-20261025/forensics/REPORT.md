# Human usability review: forensics

Scope: a simulated Windows-oriented beginner with basic terminal skills, using only shipped human documentation and shipped recipes. This is an agent-performed usability simulation, not an observed human study. No human timings are claimed. Tested locally on 2026-10-25. No guide edits, installs, remote targets, external research, custom solving algorithms, source-skill reading, or answer keys.

## Ratings

| Dimension | Score | Reason |
|---|---:|---|
| Findability | 9 | README leads directly to a short task table; all four requested tasks have accurate routes. CPTS search returns an explicitly labelled personal note. |
| Command usability | 9 | All three executable tasks worked after filename substitution. Actual WSL and PowerShell environments were used. HTTP deep-link command needs the setup block above it. |
| Clarity | 8 | Output meanings and limits are unusually explicit. The personal-note tool distinction requires reading its index/README, and the JSON explanation follows the larger EVTX alternative. |
| Instruction economy | 9 | Three local answers need only a handful of commands and the quick reference. Deeper network setup requires a small backtrack. |
| Recovery | 9 | Existing tar output directory produces a clear error and the documented fresh-name recovery succeeds without losing prior copies. |

Overall: **8.8/10**, equal arithmetic mean. Scores describe these bounded tasks, not every chapter or a live event.

## Reading route and environment

1. Read `human-guide/README.md`, then supplied `TASKS.md` and input-directory listing.
2. Followed README to `QUICKSTART.md`; read the initial table and relevant PNG, tar, process, and network cards. The initial 180-line terminal read also exposed adjacent quick cards; they were not used for solving.
3. Followed terminal setup link to `COMPETITION.md#open-this-guide` (lines 5-9). WSL working-directory inheritance and Python version check are documented there. An excerpt also showed environment and policy context.
4. Used `QUICKSTART.md#network-conversation` -> `chapters/04-network.md#http-credentials-and-files`; read the chapter opening/setup and HTTP section, not the complete chapter.
5. Opened offline `index.html` in installed Chrome via the supplied Playwright harness. Clicked the visible `Recover an HTTP download` link and verified destination `#04-network--http-credentials-and-files` and its heading. Then searched `Wireshark`, selected the CPTS-labelled `AD Reconnaissance` result, and used its sidebar `All CPTS notes` link.

All task commands ran from `human-guide/usability-tests/current-human-review-20261025/forensics`, where the supplied `recipes/` folder sits beside inputs. `wsl --list --quiet` showed Ubuntu-24.04 and docker-desktop. `wsl python3 --version` returned `Python 3.12.3`. Prefixing each Linux command with `wsl` is a normal PowerShell invocation adaptation of entering WSL first. Python and strings were available; no tool substitution or installation was necessary. TShark/Wireshark execution was intentionally not attempted for the navigation-only task.

## Actual command evidence

### Task 1: concealed PNG text — passed

From `QUICKSTART.md:64` (PNG trailer):

```text
PS> wsl python3 recipes/png_tail.py holiday.png
b'IHDR' 13 CRC OK
b'IDAT' 12 CRC OK
b'IEND' 0 CRC OK
trailing bytes: 26 preview: b'CSG_FLAG{after_the_pixels}'
saved: png-trailer.bin
Chunk walk only; not a full PNG validity check.
```

Answer: `CSG_FLAG{after_the_pixels}`. The printed preview gives the text directly; no custom decoder was needed. This establishes appended data, not pixel steganography or full PNG validity.

### Task 2: earlier tar memo — passed

From `QUICKSTART.md:74` (Duplicate tar files):

```text
PS> wsl python3 recipes/tar_keep.py backup.tar --out tar-parts
000000.bin 'memo.txt' 27 bytes; preview: b'CSG_FLAG{keep_the_old_copy}'
000001.bin 'memo.txt' 34 bytes; preview: b'Nothing useful in the newest copy.'
manifest: tar-parts/manifest.jsonl
PS> wsl strings -a tar-parts/000000.bin
CSG_FLAG{keep_the_old_copy}
PS> Get-Content tar-parts/manifest.jsonl
{"index": 0, "name": "memo.txt", "saved": "000000.bin", "size": 27}
{"index": 1, "name": "memo.txt", "saved": "000001.bin", "size": 34}
```

Earlier memo: `CSG_FLAG{keep_the_old_copy}`. Both members survive as numbered files. The manifest read is ordinary inspection of the file the card explicitly points to.

Deliberate documented failure/recovery:

```text
PS> wsl python3 recipes/tar_keep.py backup.tar --out tar-parts
Tar extraction stopped: [Errno 17] File exists: 'tar-parts'
PS> wsl python3 recipes/tar_keep.py backup.tar --out tar-parts-retry
000000.bin 'memo.txt' 27 bytes; preview: b'CSG_FLAG{keep_the_old_copy}'
000001.bin 'memo.txt' 34 bytes; preview: b'Nothing useful in the newest copy.'
manifest: tar-parts-retry/manifest.jsonl
```

The card says to choose a fresh `--out` name. That recovered immediately and kept the first extraction.

### Task 3: supplied process record — passed

From `QUICKSTART.md:90` (Process event):

```text
PS> Get-Content -Raw audit.json | ConvertFrom-Json | Format-List
Provider       : Microsoft-Windows-Security-Auditing
EventID        : 4688
TimeCreated    : 2026-10-25T06:12:34Z
NewProcessName : C:\Temp\check.exe
CommandLine    : C:\Temp\check.exe --read memo.txt
```

Timestamp: **2026-10-25T06:12:34Z (UTC)**. Full command: **C:\Temp\check.exe --read memo.txt**. This record indicates process creation and the recorded command line. It does **not** prove that memo.txt was successfully read. That limitation is stated explicitly in the card; no extra forensic inference was needed.

### Task 4: capture to HTTP download route — navigation passed, not executed

Start: packet capture row -> Network conversation (`QUICKSTART.md:122`) -> Recover an HTTP download. Website link lands on Network / HTTP, credentials, and files (`chapters/04-network.md:50`). Tool: **Windows TShark**, with Windows Wireshark as the graphical conversation-inspection route.

The earlier Machine and scope block defines `$tshark` and creates `out`. The HTTP block's relevant command is:

```powershell
& $tshark -n -r capture.pcapng --export-objects http,out/http
```

Expected result stated by the guide: exported response objects. The guide distinguishes downloads from POST uploads and warns that Export Objects does not cover every upload. This was a reading/navigation walkthrough only: no supplied capture existed, none was fabricated, and no capture-tool execution is claimed.

## Independent CPTS website check

Visible search `Wireshark` returned 14 sections, including `CPTS / Reconnaissance/AD Reconnaissance`. Selected it through its search-result link. It shows Wireshark, Tcpdump, Responder, Fping and Kerbrute commands. The visible header says `Personal reference` and links `Event tool rules`. Sidebar `All CPTS notes` explicitly says original study notes are not a competition-approved tool list. README also says their commands were not filtered against competition restrictions. Therefore the `sudo -E wireshark` command is personal Linux study material, not evidence that Linux Wireshark is the event's approved location; the event network chapter specifies native Windows Wireshark/TShark. No CPTS command was executed.

Copy: clicked the first visible Copy control, saw `Copied` and the placeholder reminder, and read clipboard text `sudo -E wireshark` with its trailing newline. Reading: selected 20 px via the Reading text size dropdown, captured and visually inspected `cpts-read-copy.png`; headings, command text and controls were legible at 1440x1000. No screenshot/image was present in this chosen note (image count 0); Full size/Fit width is therefore not applicable and is not claimed tested. All owned Chrome instances are closed in harness `finally` blocks.

Artifacts: `website-initial.png`, `http-navigation.png`, `cpts-search.png`, `cpts-note.png`, `cpts-read-copy.png`. Browser scripts are preserved, with `browser-verified.js` the successful final copy/read/sidebar run.

## Three actionable findings

1. **Minor command-context gap:** `QUICKSTART.md:133` links straight into `chapters/04-network.md:50-59`, whose copied block uses `$tshark` initialized only in the earlier Machine and scope block (lines 13-24). Add a visible prerequisite link or the one-line assignment to the HTTP card so a Windows beginner entering through that anchor can copy it directly. No execution failure was induced for this navigation-only task.
2. **Minor policy discoverability:** the CPTS `AD Reconnaissance` note at `index.html#cpts-reconnaissance-ad-reconnaissance-cbb23af1--ad-reconnaissance` labels itself only `Personal reference · Event tool rules`. The explicit unfiltered-tool warning is on `CPTS.md:5` and README. Repeat that short warning in individual note headers so a search arrival understands it before copying `sudo -E wireshark` or other environment-specific commands.
3. **Small reading-order improvement:** `QUICKSTART.md:90-120` places the longer EVTX alternative between the supplied-JSON command and the field/interpretation table. Put the table and the successful-completion limitation immediately after the JSON command, then the EVTX alternative. This would reduce scrolling for this very straightforward record-reading task.

These are incremental improvements, not blockers. The executable tasks were already usable.

## Harness limitations and errors (not guide failures)

One `rg` call used a repository-relative chapter path while inside the task folder and failed; rerunning at workspace root corrected it. Default PowerShell decoding displayed some Unicode arrows as mojibake, whereas Chrome and explicit UTF-8 reads showed them correctly. Neither is counted against the guide.

The first browser search snapshot was taken before its debounce; waiting for Search results corrected that. A Copy locator wrongly assumed its accessible name was exactly `Copy`; inspecting the visible button's accessibility label showed `Copy shell-session block`, which succeeded. Attempts to click an HTML `<option>` directly timed out; selecting the visible Reading text size combobox succeeded. These are automation-locator errors, not evidence that human clicking fails. Scripts preserve those unsuccessful attempts. No timing data from the harness is treated as human effort.
