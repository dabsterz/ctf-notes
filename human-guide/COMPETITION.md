# Competition setup and rules

Based on the supplied **Practice Environment Setup Guide**, read alongside the tool workbook. Page references below link to the [unchanged PDF included with this guide](sources/practice-environment.pdf). Pages 1–11 describe the competition; page 12 explicitly starts the **19–23 October practice-session** instructions. Do not assume practice launch quotas or credentials are competition-day rules.

## Open this guide

Extract the ZIP and open `index.html` in Chrome, or read `QUICKSTART.md`. Keep the `recipes/` and `sources/` folders beside it. For Python helpers, open PowerShell in the extracted folder and run `wsl`; its terminal inherits that working directory. Run the shown `python3 recipes/...` command there. Use the supplied remote Kali session for Kali-labelled commands; laptop files are not automatically present there.

Website-only copy: open [Recipe downloads](RECIPES.md), save a needed script into a `recipes` subfolder, and open a terminal in its parent folder. Helpers use the standard library. Check `python3 --version` on the machine you chose. The ZIP also carries the source PDF; `index.html` alone embeds the guide text and helpers, not that PDF.

## What is allowed

| Need | Competition rule | Source |
| --- | --- | --- |
| Bring this guide or prepared scripts | Physical/electronic notes, cheat sheets, books, digital references, personal Notion/GitHub references and scripts created before the competition are allowed | [p.7](sources/practice-environment.pdf#page=7) |
| Look up a technique | Google Search, technical/vendor/programming documentation, CVE databases, HackTricks, PayloadsAllTheThings, Microsoft docs, Linux manuals and Google Translate are allowed | [p.6](sources/practice-environment.pdf#page=6) |
| Add a missing library/dependency/plugin/package | Allowed when not related to generative AI; availability and compatibility still need checking | [p.5](sources/practice-environment.pdf#page=5) |
| Add an unlisted standalone application | Organizer approval is required; packaging an application with pip does not turn it into an unrestricted library | [p.5](sources/practice-environment.pdf#page=5) |
| Use personal commercial software | Personal commercial licenses, such as IDA, cannot be used to bypass the common environment | [pp.5,21](sources/practice-environment.pdf#page=21) |
| Use AI | Generative-AI assistants, code/script generation and challenge analysis are prohibited during competition. Automatically displayed search-result AI summaries may be viewed | [p.8](sources/practice-environment.pdf#page=8) |
| Use online analysis services | Do not upload challenge files to online services. Use local decoders, hash crackers and decompilers | [pp.6,21](sources/practice-environment.pdf#page=21) |
| Collaborate | Work freely within your team. No external help, external sharing of challenge content or unofficial communication outside the team. Notes may be kept afterward | [p.9](sources/practice-environment.pdf#page=9) |
| Use a phone at the table | Phones must be deposited; no external communication devices at competition tables | [p.10](sources/practice-environment.pdf#page=10) |

**Read the two sources together:** the workbook still identifies installed environments and named exclusions. Its AI/ML-library prohibition is broader than the PDF's generative-AI wording; this guide keeps AI/ML tools excluded. The PDF does not expressly clear individual entries on the workbook's Unapproved List. Use the listed alternatives; if you specifically need one of those entries, resolve that conflict through the official organizer channel. This is a conservative reconciliation, not a claim that every installation failure has the same reason as a rule prohibition. [Package setup commands](chapters/00-tool-rules.md#non-ai-python-package-checks).

## Choose the machine before the tool

| Environment | Supplied resources | Good starting jobs |
| --- | --- | --- |
| Windows 11 Pro laptop | Core Ultra 5 235H (2.40 GHz); 32 GB RAM; 1 TB SSD; 64-bit; 1920×1200 display | Native Wireshark, Autopsy, HxD, x64dbg and dnSpyEx; keep large evidence on the laptop |
| WSL on that laptop | Installed tools are identified by the workbook; it shares the laptop's resources and may have a lower configured memory limit | Python helpers, Ghidra, GDB, Volatility 3, Sleuth Kit and the listed Linux utilities |
| Remote Kali through Platform Experience | **t3.large: 2 vCPU, 8 GiB RAM, 40 GB disk**, GUI; SSH/RDP requires VPN | Kali-only tools, small targeted scans and local CPU-bound jobs; avoid several heavy jobs at once |

Hardware facts: [PDF pp.3–4](sources/practice-environment.pdf#page=3). AWS lists no accelerator for t3.large, so **do not plan on GPU hashcat cracking on this Kali instance**. Start with short clue-derived wordlists and a supported John format; `hashcat -I` checks its available compute backend. [AWS instance specifications](https://docs.aws.amazon.com/ec2/latest/instancetypes/gp.html).

**Kali, before extracting large files or running a heavy job:**

```bash
df -h .
free -h
nproc
```

Check free disk against the **expanded** archive size, not just its download size. Stream large files rather than reading them entirely into Python memory. Keep Windows-only parsers on Windows; move large work to an appropriate laptop tool when possible, not to an unapproved application.

The organizer put Defender-sensitive tools such as Hayabusa/Sigma rules, Metasploit and mimikatz on Kali. Use their supplied Kali location; **do not disable Defender or add laptop exclusions as the workaround**. [PDF pp.4,22](sources/practice-environment.pdf#page=22).

## Access: approved network, VPN, then Kali

**At the event:** use the organizer's approved hotel network and day-of access details. CTFd and related infrastructure are IP-restricted. The PDF identifies VPN as necessary for SSH/RDP to Kali. A failed portal connection from another network does not establish that the portal is down. [PDF pp.3–4](sources/practice-environment.pdf#page=3).

1. Open the supplied Platform Experience environment and wait for **Provisioning succeeded**.
2. Read the current **Kali IP**, **Kali username/password**, and **OpenVPN IP** from the cloud/status panel. The VPN endpoint and Kali address are different values.
3. In the installed Windows OpenVPN client, import/connect using the profile and instructions supplied by Platform Experience. Do not invent the VPN profile or ports.
4. Connect to **your Kali IP** by the provided SSH or RDP route. Use the supplied credentials, not a guessed `kali/kali` default.

The detailed panel sequence is from the **practice** section, [p.18](sources/practice-environment.pdf#page=18); follow the competition's current panel/instructions if they differ. No real portal login, VPN connection or VM launch was performed while preparing this guide.

**Windows PowerShell**, after replacing the placeholder with your assigned Kali IP:

```powershell
$kaliIp = 'YOUR_ASSIGNED_KALI_IP'
Test-NetConnection -ComputerName $kaliIp -Port 3389
mstsc /v:$kaliIp
```

This checks the usual RDP port, then opens Remote Desktop; use a different port only if Platform Experience specifies one. `TcpTestSucceeded : True` establishes reachability, not successful authentication. [Microsoft connection check](https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection) and [RDP client syntax](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc).

**SSH alternative**, only if the provided Windows client is present:

```powershell
Get-Command ssh,scp -ErrorAction SilentlyContinue
ssh YOUR_KALI_USER@YOUR_ASSIGNED_KALI_IP
```

For file transfer using that client:

```powershell
scp .\challenge.zip YOUR_KALI_USER@YOUR_ASSIGNED_KALI_IP:~/
scp YOUR_KALI_USER@YOUR_ASSIGNED_KALI_IP:~/answer.txt .\answer.txt
```

If the client is absent, use the supplied RDP route and organizer-supported transfer method; do not install an unlisted standalone client on assumption. WSL paths such as `/mnt/c/Users/...` reach the **local laptop**, not remote Kali. Do not publish challenge files or answers through a personal GitHub repository to transfer them. Prepared references and external sharing of live challenge content are different uses.

| Symptom | First useful check |
| --- | --- |
| CTFd does not open | Approved hotel network and exact current URL; then official support |
| Portal works but Kali does not | VPN connected, correct Kali IP (not OpenVPN IP), provisioning complete |
| RDP works but a WSL tool is missing | Those tools are on the laptop; enter WSL there or choose the Kali alternative |
| Script cannot find a file | Check the current machine and working directory before editing the script |
| A heavy job stalls | Check free RAM/disk, stop duplicate jobs, and narrow the candidate set |

## Categories, flags and time

This is a Jeopardy-style CTF with separate daily challenge sets and flag submission through CTFd. The PDF lists **seven categories**: Digital Forensics, Malware Analysis, Web Security, Reverse Engineering, OSINT, Cryptography and Miscellaneous. This guide's navigation follows that list. Network and steganography remain supporting techniques; pwn and historical practice remain supplementary. The earlier public-page grouping was different; this revision uses the supplied operational guide. [PDF p.2](sources/practice-environment.pdf#page=2).

Flags **typically** use `CSG_FLAG{example_flag}`. Submit the entire value, including prefix/braces, through CTFd; follow a challenge's explicit format if it differs. `CTF{...}` and short plaintexts in old examples are synthetic teaching results, not instructions to change the competition flag format. [PDF p.20](sources/practice-environment.pdf#page=20).

| Competition slot | What to prepare |
| --- | --- |
| 26 October: technical preparation 08:00–09:00; environment briefing 09:30–09:50 | Check the current access instructions, guide files and key tool launches |
| 26 October: Question Set 1, **10:00–17:00** | Solve and retain brief command/evidence notes |
| 27 October: Question Set 2, **09:00–13:00** | Different set from Day 1; reassess priorities |
| 27 October: **13:00–15:30 write-up and team presentations** | Preserve derivations and accepted verdicts while solving |

Times are copied from [PDF p.11](sources/practice-environment.pdf#page=11); use the venue's day-of briefing for changes. Official communication channels are supplied on the day. Organizers monitor screens and participant activity ([pp.8–10](sources/practice-environment.pdf#page=8)). No scoring details or presentation format beyond the PDF are assumed.

## Practice-session reference only

**Practice was 19–23 October 2026**, using your own computer; competition is 26–27 October on organizer laptops. The following comes from pages 12–20 and is not an instruction to spend another launch now. It does not establish a three-launch quota for competition day.

- The practice CTFd URL is `https://2026ctf.ajccbc-cyber-sea-game.net`. Each team receives four accounts, one per participant. Use the competition URL/account allocation supplied on the day. [pp.13–14](sources/practice-environment.pdf#page=14)
- Practice Gmail uses the same ID/password as CTFd, with the `@trend.training` domain on Google's normal Gmail sign-in. The invitation lasts 14 days. Find the Platform Experience invitation and complete onboarding. [pp.15–16](sources/practice-environment.pdf#page=15)
- Starting practice deployment takes **about 20 minutes**. Leave it alone while deploying. **Up to 3 launches per account; Terminate consumes the current session.** Repeated starts/terminations are not a troubleshooting loop. [p.17](sources/practice-environment.pdf#page=17)
- The practice **Misc → Welcome** challenge directs you to find `flag.txt` in your Kali user profile. After connecting, `find "$HOME" -maxdepth 2 -type f -name flag.txt` lists likely locations; use `cat` on the returned path. This is a practice task, not a promised competition flag location. [p.19](sources/practice-environment.pdf#page=19)

Keep the short [quick reference](QUICKSTART.md) open during solving. Use this setup page when the problem is access, environment, permission or workflow rather than the challenge itself.
