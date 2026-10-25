# Competition environment reconciliation

Updated 25 October 2026 from all 23 pages of the supplied `Practice Environment Setup Guide.pdf`, including its rendered slides, and the original tool workbook. This audit supersedes older environment/permission statements in historical review reports. The original source files remain unchanged.

## Source-to-guide audit

| PDF pages | Requirement or fact | Current reader-facing destination |
| --- | --- | --- |
| 1, 12–13 | Competition 26–27 October; practice 19–23 October on own computer; practice divider at p.12 | Competition setup opening and practice-only section; no reuse of practice quotas as competition rules |
| 2 | Jeopardy, CTFd submission, different daily sets, seven named categories | Seven-category website navigation and handbook order; category/flag/schedule section |
| 3 | Windows 11 Pro, Core Ultra 5 235H, 32 GB RAM, 1 TB SSD, 64-bit, 1920×1200; hotel network/IP restriction | Machine table and access section; laptop/WSL/remote files distinguished |
| 4 | Kali t3.large, 2 vCPU, 8 GiB, 40 GB, GUI, VPN before SSH/RDP; Defender-sensitive tools placed on Kali | Machine limits, resource-check commands, access sequence and malware chapter |
| 5, 22 | Organizer installs approved tools/requests, versions fixed at mid-October installation; non-generative-AI libraries/dependencies/plugins/packages permitted; unlisted standalone apps require approval | Central rules table; targeted WSL uv and Kali venv examples; version-check advice |
| 5, 21 | No personal commercial licenses to bypass common environment | Rules table; existing free/listed alternatives retained |
| 6 | Manual search, technical references, HackTricks, PayloadsAllTheThings and Translate allowed; no challenge-file uploads | Rules table, OSINT and excluded-workflow chapters; local analysis routes retained |
| 7 | Physical/electronic notes, cheat sheets, books, digital references, personal Notion/GitHub and prepared scripts allowed | Entry pages and quick reference now state allowance; obsolete confirmation language removed |
| 8 | No generative-AI assistants or AI-generated solutions/scripts/analysis; automatic search summaries exception; screen monitoring | Rules table states prohibition and exception; monitoring noted below and in setup |
| 9–10 | Team collaboration/notes retention allowed; no outside assistance, external sharing or unofficial outside-team channels; phones deposited; monitoring | Rules table and access/file-transfer guidance; official channel supplied on the day |
| 11 | Day 1 set 10:00–17:00; Day 2 set 09:00–13:00; write-up/presentations 13:00–15:30 | Schedule table and first-ten-minutes note-taking guidance; venue briefing governs changes |
| 14–16 | Practice portal, four participant accounts, Gmail mapping/domain, 14-day invitation and PX onboarding | Clearly labelled practice-only reference; no real credentials copied |
| 17–18 | Practice start takes about 20 minutes, three launches/account, Terminate consumes session; status panel then VPN then SSH/RDP | Practice-only quota; access sequence explicitly attributed to practice panel and subject to current event instructions |
| 19–20 | Practice Welcome flag in user profile; typical `CSG_FLAG{...}`, full CTFd submission | Practice-only file search; typical format on quick sheet and setup, without overriding challenge-specific instructions |
| 21–23 | Online-upload and commercial-license FAQ, Defender placement, version timing, verify access | Rules/access sections; no public analysis upload or Defender-disabling workaround |

The PDF states screen/activity monitoring. This is informational; it adds no solver step. Its screenshot's six-hour practice experience display is not treated as a competition runtime limit. Removable-media permission is not asserted because the PDF does not settle it. The supplied practice URL/account allocation is not represented as a guaranteed competition-day allocation.

## Reconciliation decisions

- Preserve all 282 workbook rows and installation locations: 39 Windows/WSL, 161 Kali, 82 unapproved. A tool's availability is separate from its permission. WSL runs on the laptop; it is not remote Kali.
- Keep the workbook's broader AI/ML exclusion alongside the PDF's generative-AI rule. Do not silently treat the new PDF as approval of individually named rejected tools. The guide uses listed alternatives and labels this conservative reconciliation; original failure/prohibition reasons remain visible.
- Apply the PDF's general non-AI package allowance to both environments. Do not label it WSL-only. A pip-distributed standalone app is still a standalone app; its packaging is not an approval loophole.
- Use a short local candidate list and supported CPU tools on the two-vCPU Kali instance. AWS's primary specification independently identifies t3.large as lacking an accelerator; this is linked beside the hashcat guidance.
- Keep ordinary manual documentation/research access distinct from uploading live challenge material or asking outsiders to solve it. Personal repository reference access does not authorize publishing live files/answers as a transfer mechanism.

## Verification and scope

`environment-validation.json` records the source/copy hashes, 23-page count, category agreement, offline links, source preservation, stale-policy checks and packaging inputs. Aggregate `validation.json` checks every generated chapter against its Markdown, link targets, anchors, recipe sources, Python syntax and the original 286-file inventory. The tool-chooser checker independently reparses the XLSX, rather than trusting the exported policy JSON alone.

The browser DOM test verifies the seven-category order, competition setup route, PDF page link, search/copy/download logic, tool filters and absence of external runtime requests. It does not establish visual layout or real-browser clipboard/dialog behavior. PowerShell snippets receive parser checks; the existing process-event test uses mock XML, not a real EVTX file. Package verification compares every ZIP member byte-for-byte to its source.

Verification performed for this revision: 16 builder/helper unit tests; all 282 workbook entries and 72 chooser rows checked; 7 PowerShell blocks parsed; 20 Bash blocks checked with WSL `bash -n`; process-event field-mapping check passed; JavaScript syntax passed. Generated-content validation covered 22 pages, 287 code blocks and 106 compilable Python blocks. The DOM suite passed 9 check groups. These counts describe checks, not live challenge solves.

No competition portal, VPN, organizer VM, real credentials or remote challenge was used. New venv examples were syntax/source-checked, not installed into organizer machines. Prepared-script tests and historical usability reports cover their stated local examples only. Their old scores are not reassessments of this PDF revision.

## Completion evidence

The final build includes quick reference, competition setup, all 16 existing chapters, chooser, recipe downloads and appendices in both HTML and Markdown. The ZIP includes the unchanged PDF and scripts. Source-to-guide mapping above covers every substantive rule, resource, access step, schedule and practice limitation in the PDF; no category guide or original source was removed.
