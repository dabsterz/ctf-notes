# Independent simulated-human review: forensics

Reviewer 1: Windows-oriented solver with basic terminal skills. Date: 2026-10-25. This is an agent simulation, not a real human participant study. No human completion times were measured or invented.

## Verdict and ratings

The three supplied executable tasks were independently completed using written guide instructions. The fourth task was completed as navigation/tool selection only; no capture was supplied or manufactured. These small tasks are usable, but the shortest path still contains unnecessary reading and the policy text needs updating against the newly supplied PDF.

| Dimension | Score / 10 | Reason |
| --- | ---: | --- |
| Findability | 7 | Artifact table leads directly to PNG, tar and events. HTTP object recovery requires a detour beyond the linked network chooser. |
| Command usability | 8 | Supplied helpers and PowerShell JSON command work with filename/path substitution. WSL entry instructions exist, but are distant from first use. |
| Clarity | 7 | Outputs and evidence limits are clear. Stale policy uncertainty and an EVTX-first JSON route add interpretation. |
| Instruction economy | 6 | The task cards are compact; the opening setup paragraph, broad comparison tables and repeated policy caveats impose extra effort. |
| Recovery | 8 | The tar existing-directory recovery works exactly as described. Environment and empty-HTTP alternatives are useful, though only the tar failure was exercised. |
| Overall arithmetic mean | **7.2** | (7 + 8 + 7 + 6 + 8) / 5 = 7.2. |

Anchor applied: 7-8 is usable with minor gaps; 5-6 requires repeated interpretation. Volume is not a positive rating factor.

## Boundaries and consulted pages

Allowed task brief: `usability-tests/human-review-20261025/forensics/TASKS.md`; adjacent inputs: `holiday.png`, `backup.tar`, `audit.json`. No capture exists there.

Reading path: `README.md` → `QUICKSTART.md` artifact table → PNG trailer / Duplicate tar files / Process event / Network conversation. Followed `TOOL-CHOOSER.md` for Network and its failure advice; consulted `chapters/00-tool-rules.md` for WSL entry and environment policy; manually selected `chapters/04-network.md`, specifically Machine and scope and HTTP, credentials, and files, to locate HTTP object export. The broader pages were retrieved as text; only relevant sections informed the tasks. The long network chapter made section selection more important, not task success more impressive.

Policy audit only: `review/tool-policy.json` and the root `Practice Environment Setup Guide.pdf`. Website audit only: relevant static portions of `index.html`. No prior usability reports, answer keys, fixture generators, source CTF skills, internet sources, or other reviewers were consulted. The general using-superpowers file was read initially; its subagent stop rule applied, and no solving skill was used. No guide files were edited.

## Execution record

Execution cwd for the WSL helper runs was the assigned forensics folder. Because scratch files were restricted to that folder, the guide's `recipes/...` path was replaced with `../../../recipes/...`; supplied input names replaced examples. This is ordinary file navigation, not a newly invented parser. PowerShell `wsl` was used as the tool transport to execute the displayed Linux commands inside real WSL Ubuntu, rather than substituting host Python. The guide explains `wsl` entry and `/mnt/c` path mapping in `chapters/00-tool-rules.md:40` onward. No Kali commands ran.

Environment checks: `Get-Command python,python3,wsl,xxd,strings -ErrorAction SilentlyContinue`, `wsl --list --quiet`, `wsl --list --verbose`, and `wsl python3 --version`. WSL listed Ubuntu-24.04 (default) and docker-desktop; WSL Python reported **3.12.3**. Host Python was `C:\Python314\python.exe`, and host strings was a MinGW installation. Host `xxd` was not found. Those host findings were not counted as event-tool availability or used to run the CTF helpers.

### 1. Concealed text in holiday.png: independent success

Written basis: `QUICKSTART.md:61-71`. Actual commands, each dispatched from PowerShell:

```powershell
wsl python3 ../../../recipes/png_tail.py holiday.png
wsl xxd -l 128 png-trailer.bin
wsl strings -a png-trailer.bin
```

Observed: IHDR, IDAT and IEND each reported `CRC OK`; `trailing bytes: 26`; preview `b'CSG_FLAG{after_the_pixels}'`; saved `png-trailer.bin`. Both hex view and strings exposed `CSG_FLAG{after_the_pixels}`. No pixel-steganography knowledge or handwritten code was necessary. The preview alone already answered this fixture; the two inspection commands were verification, not necessary discovery steps. The card's explicit limitation about pixel steganography is useful.

### 2. Recover old memo while preserving versions: independent success

Written basis: `QUICKSTART.md:73-87`. Actual commands:

```powershell
wsl python3 ../../../recipes/tar_keep.py backup.tar --out tar-parts
wsl strings -a tar-parts/000000.bin
Get-Content tar-parts/manifest.jsonl
Get-Content tar-parts/000001.bin
```

Observed: `000000.bin 'memo.txt' 27 bytes` previewed `CSG_FLAG{keep_the_old_copy}`; `000001.bin 'memo.txt' 34 bytes` previewed `Nothing useful in the newest copy.` The manifest maps both original names to separate saved files. The answer and later version remained available separately. The command, output interpretation, and mapping explanation were sufficient without archive-domain knowledge.

Error-recovery attempt: deliberately repeated the first extraction command with the same `--out tar-parts`. It returned `Tar extraction stopped: [Errno 17] File exists: 'tar-parts'`. Following the card's instruction to choose a new output name, ran:

```powershell
wsl python3 ../../../recipes/tar_keep.py backup.tar --out tar-parts-retry
```

It again saved both entries and a manifest successfully. This is tested recovery, not a paper claim. The old directory was not removed or overwritten.

### 3. Process record timestamp, command and inference: independent success

Written basis: `QUICKSTART.md:106-113`. Actual command from workspace root:

```powershell
Get-Content -Raw 'human-guide/usability-tests/human-review-20261025/forensics/audit.json' | ConvertFrom-Json | Format-List
```

Observed provider `Microsoft-Windows-Security-Auditing`, EventID `4688`, timestamp **2026-10-25T06:12:34Z**, executable `C:\Temp\check.exe`, full command **`C:\Temp\check.exe --read memo.txt`**. The guide's field table identifies UTC and process creation, and its final sentence states that this event alone does not establish successful completion or payload effects. Therefore it **does not prove memo.txt was successfully read**. No EVTX command or suspect executable was run.

Friction: the JSON command is buried after a 10-line EVTX code block and a field table. A basic user with JSON has to skip irrelevant extraction code before finding their one-line route.

### 4. capture.pcapng HTTP download route: navigation success, execution not attempted

`QUICKSTART.md:12` points to Network conversation. `QUICKSTART.md:117-126` identifies Windows Wireshark/TShark and HTTP host/path/stream inspection. `TOOL-CHOOSER.md` Network lists Wireshark as supporting object export, but links back to the conversation card rather than to the export recipe. That was a navigation dead end for the narrower goal of recovering a download.

Manual chapter navigation reached `chapters/04-network.md:50`, HTTP, credentials, and files. The exact provided recovery command is at line 57:

```powershell
& $tshark -n -r capture.pcapng --export-objects http,out/http
```

The preceding Machine and scope block defines `$tshark` as `C:\Program Files\Wireshark\tshark.exe` and creates `out`. This is a sufficient written route for ordinary captured HTTP response objects. `Test-Path 'C:/Program Files/Wireshark/tshark.exe'` returned True, but presence is not successful launch or PCAP processing. No capture exists in the task folder. I did not run TShark against fabricated data, claim an exported object, or test TLS recovery. Navigation selection met this task's stated scope; actual recovery remains untested.

## Policy cross-check

The existing workbook transcription confirms the tool locations used here: Windows sheet `C9/I9` Wireshark native Windows, `C43/I43` TShark native Windows, `C14/I14` Python 3 in WSL, `C18/I18` strings in WSL, and `C35/I35` xxd in WSL. Windows B5 and H14 prohibit AI-related libraries; H14 permits other libraries. Kali B4 also prohibits AI-related additions. The guide is accurate on these locations and the workbook distinctions. I used the authorized JSON transcription, not an independent XLSX reparse.

The new PDF changes the practical advice:

- **PDF page 7 explicitly allows physical/electronic references, personal notes, cheat sheets, personal repositories, and scripts created before the competition.** `README.md:25` still tells readers to confirm handbook/prepared-script permission; `QUICKSTART.md:234` repeats that the workbook does not establish it. That statement about the workbook alone may be technically true, but it is incomplete advice with this supplied PDF available. Smallest fix: cite PDF page 7 and say these materials are permitted. Keep removable-media uncertainty separate because page 7 does not address that medium.
- **PDF page 5 permits libraries, dependencies, plugins and packages that are not related to Generative AI**, while unlisted standalone applications require approval. `chapters/00-tool-rules.md:88` and `:96` frame package setup as WSL-only and leave Kali permission unresolved. The newer document provides broader permission; reconcile its wording with the workbook's stricter AI/ML wording rather than repeatedly pushing the reader into uncertainty. This is a documentation issue; no packages were installed during the review.
- PDF pages 6, 8, 9 and 21 support allowed technical references, the generative-AI ban, no outside assistance, and no challenge-file uploads to online services. Page 8 additionally permits viewing automatic search-result AI summaries. The guide's broad practical no-AI route is safe for these tasks, but it is not a complete restatement of that exception.

PDF extraction used host `python` with PyMuPDF only for the review, not a challenge solve or claimed event route. The first console print failed with a cp1252 UnicodeEncodeError. Repeating with `python -X utf8` successfully displayed the PDF text. That recovery came from reviewer tooling knowledge, not from the cheat sheet, and earns no guide recovery credit.

## Website check and limitations

Supported computer-use inventory returned `apps: []` and `browsers: []`. Therefore no clicks, screenshots, layout, command-copy behavior, downloaded recipes, or runtime browser search were tested. Static `index.html:101` sets the initial chapter to quickstart. Lines 126-137 implement all-word section matching, title-weighted ranking and a no-result message suggesting fewer words or synonyms. This is useful discoverability design, but source inspection is not proof the website works in Chrome.

A broad source search initially matched the site's enormous embedded-data line and produced truncated output. I narrowed to the relevant application lines afterward. This is an inspection-tool detour, not evidence that a human browser user would see that data or suffer the same issue. Console text rendered some UTF-8 punctuation incorrectly under Windows PowerShell; I do not attribute that to the browser rendering.

## Top issues and smallest changes

1. **Stale permission uncertainty creates needless organizer-check work.** Evidence: `README.md:25`, `QUICKSTART.md:234`, and `chapters/00-tool-rules.md:96`, compared with PDF pages 5 and 7. Replace these with a concise current permission summary and exact PDF page references. Do not add a new checklist.
2. **The JSON process route is unnecessarily subordinate to EVTX.** Evidence: `QUICKSTART.md:91-113`. Start with two input links, “JSON” and “EVTX”; show the one-line JSON command first or make the EVTX block expandable on the site. Keep the field meanings and the limit on causal inference.
3. **HTTP-download recovery is one link too far away.** Evidence: `QUICKSTART.md:126` links to the general chooser, whereas the useful export command is `chapters/04-network.md:57`. Add a direct “Recover an HTTP download” link to that section, or a small dedicated card. Do not copy the entire network chapter into the quick reference.
4. **The first setup paragraph mixes too many independent decisions.** Evidence: `QUICKSTART.md:5`; actual WSL entry is in `chapters/00-tool-rules.md:40-48`. Collapse the quick-reference setup into “Linux commands: open WSL [how]. Replace example filenames. Keep recipes beside this guide.” Put website-only recipe downloads and Kali availability notes behind the setup link. The existing WSL mapping explanation is useful and should remain available.
5. **PNG inspection can be conditional.** Evidence: `QUICKSTART.md:66-71`. The helper already prints CRCs, trailer length and text preview. Label xxd/strings as “If the preview is unclear” to reduce mechanical command repetition. Keep the recovery branches and pixel-channel limitation; those prevent false conclusions.

## What deserves to stay

The artifact jump table, one-command tar extractor, numbered version mapping, output previews, explicit success criteria, JSON field meanings, UTC preservation, and tested existing-directory recovery all earned their space. They converted these fixtures into straightforward tasks without asking the user to become a programmer. The shortest productive surface is the task card, not the comparison table or a full chapter.

## Honest limits

Three deliberately small fixtures do not establish broad forensics competence or general recipe correctness. WSL was real Ubuntu 24.04 on this host, not the organizer's validated image; Kali was not accessed. No network file extraction was executed. No browser interaction was possible. No destructive or corrupt archive, damaged PNG, absent WSL distribution, missing WSL Python, or EVTX file was tested. Only an existing-output-directory failure was exercised as guide recovery. This report is a simulated basic-user walkthrough with actual command evidence, not a human usability experiment and not a claim of a flawless guide.

