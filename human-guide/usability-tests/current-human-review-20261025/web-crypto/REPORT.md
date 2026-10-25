# Human-style web/crypto usability review

Overall **8.6/10**, equal mean of findability 9, commands 8, clarity 8, instruction economy 9, recovery 9. The three supplied files were solved with shipped helpers; the fourth task was a navigation-only walkthrough. This is a bounded simulated human review with basic web/crypto familiarity, not measured human timing or a whole-handbook audit.

## Reading and environment

Started at `human-guide/README.md`, followed `QUICKSTART.md`, and searched only RSA, decode/Base64, and web path terms. Read Quickstart lines 20–30 and 135–157. For task 4 followed its linked `chapters/02-web-exploitation.md`, reading the environment table and route-map excerpt (lines 9–19, 95–103). No source skills, builder code, previous reviews, fixture generators, or answer keys were read. No independent solving algorithm was written or substituted.

Actual execution used installed Ubuntu-24.04 WSL, Python 3.12.3. `wsl --list --quiet` showed Ubuntu-24.04 and docker-desktop, not Kali. Each Linux command below ran in `/mnt/c/Users/verno/Downloads/ctf-skills-main/ctf-skills-main/human-guide/usability-tests/current-human-review-20261025/web-crypto`, using `wsl -d Ubuntu-24.04 -- bash -lc "cd … && COMMAND"`. This wrapper selects the existing distro and the supplied task folder; helper commands only adapt filenames/output names. No packages were installed. Kali and a live service were unavailable and unnecessary for the navigation-only task.

## Executed tasks and recovery

**1 — RSA: solved.** Quickstart RSA explains JSON input, optional factors, success criteria, bounded Fermat fallback, and padding limitations. The supplied JSON already matched its input format. Actual command:

```text
python3 recipes/rsa.py numbers.json
factors: 32416187567 32416190071
re-encryption: OK
plaintext bytes: b'CSG_OK'
saved: rsa-plain.bin
No padding removed. Without length, leading zero bytes cannot be recovered.
```

**2 — encoded note: solved.** Actual command from Decode layers:

```text
python3 recipes/layers.py note.txt --out decoded-note
layer1: 35 bytes; header: 789c730e768f77f3
layer2: 27 bytes; preview: b'CSG_FLAG{unwrap_then_check}'
complete compressed stream; extra trailing bytes: 0
saved in: decoded-note
```

**3 — labeled response: solved after the documented failure/recovery.** First ran the helper directly:

```text
python3 recipes/layers.py labeled.txt --out decoded-labeled
Decoding stopped: Excess data after padding
```

Quickstart line 157 explicitly says that for `payload=VALUE` save only VALUE in a new file, retaining final `=` padding, then rerun with that filename; it also advises a fresh output name if a directory exists. I manually copied `Q1NHX0ZMQUd7bGFiZWxzX25lZWRfYV9zdGVwfQ==` into `labeled-value.txt`. The editor-equivalent PowerShell action was `Set-Content -LiteralPath 'human-guide/usability-tests/current-human-review-20261025/web-crypto/labeled-value.txt' -Value 'Q1NHX0ZMQUd7bGFiZWxzX25lZWRfYV9zdGVwfQ==' -Encoding ascii`. This implements the written preparation, without inventing extraction logic. Recovery command:

```text
python3 recipes/layers.py labeled-value.txt --out decoded-labeled-value
layer1: 28 bytes; header: 4353475f464c4147
no zlib/gzip header; inspect layer1: b'CSG_FLAG{labels_need_a_step}'
saved in: decoded-labeled-value
```

The real error wording differs from the guide's category label “Strict Base64 error,” but the following `payload=VALUE` example made the remedy clear. No bridge was missing for these three fixtures.

**4 — all paths return HTTP 200: navigation walkthrough complete; no scan executed.** Route: README → Quick reference → Web paths → More web recipes → Web chapter environment table and small route map. Documented commands:

```bash
curl -i 'http://challenge.example/a-name-that-should-not-exist'
printf '%s\n' profile export status > words.txt
ffuf -u 'http://challenge.example/FUZZ' -w words.txt -ac -t 1 -rate 1 -timeout 10 -maxtime 30
curl -i 'http://challenge.example/candidate'
```

The deeper route additionally records JSON with `-mc all -of json -o routes.json`. Prerequisites: a supplied challenge URL, reachable service, Kali with curl/ffuf present, and short plausible route names derived from links/source. These are example names to replace. Local WSL does not imply ffuf availability; the chapter expressly distinguishes that. The fake path establishes the error response. Compare the candidate response to it, rather than accepting 200 as success; inspect the returned content. If automatic calibration hides candidates, the Quickstart says inspect the baseline and retry without `-ac`. There was no service, so no result differentiation or exploit success is claimed.

## Independent offline website check

Used installed Chrome via the supplied Playwright-core harness, with browser context offline, at 1440×1000. `browser-review.cjs` automates only visible UI reading/clicking and screenshots; it never reads embedded guide data. Each owned browser closes in `finally`.

Entered `ffuf` in the visible search box: 10 section results, including Quick reference / Web paths, Web security / route map, and CPTS / Enumeration/Service Enumeration/80,443 http. Clicked the CPTS result, then independently clicked its `80,443 http` sidebar link; both opened the same note. Reference: `cpts/pages/cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8.md`, website anchor `#cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8--80443-http`.

The note is legible in the desktop screenshots, with code panels and visible Copy controls. Clicking the first Copy button produced “Copied” and the clipboard contained both original nmap command lines, preserving their newline. The first automation attempt incorrectly assumed the accessible name was exactly “Copy”; inspection showed “Copy shell block.” Selecting the visible Copy text fixed the harness. This is an automation-locator error, not a guide defect. `browser-log.txt` records the successful run. The note has zero images, so no Full size/Fit width control was present and that behavior was not tested. Screenshots: `browser-search-ffuf.png`, `browser-cpts-http.png`, and `browser-cpts-http-top.png` (the latter filename does not guarantee top-of-page placement).

Policy is distinguishable: README says personal notes are unfiltered against competition restrictions; CPTS.md line 5 says they are not a competition-approved tool list. The note itself labels “Personal reference” and links “Event tool rules.” Clicking that link opened Competition setup, which describes organizer approval for unlisted standalone apps and the event restrictions. I did not run CPTS examples or interpret their presence as approval.

## Actionable top three findings

1. **Add an editorial correction beside the personal HTTP note's directory ffuf example.** `cpts/pages/cpts-enumeration-service-enumeration-80-443-http-3d6bc3e8.md:22` puts `FUZZ` in `Host: siteisup.htb/FUZZ`, while its URL has no path placeholder. As written, it varies a Host header containing a slash, not the directory path described by its heading. It also hardcodes `-fs 1131` without deriving a baseline. This is a reading-level mismatch, not a live-tested failure. Keep originals intact if needed, but route readers to the reviewed Quickstart command and explain that filter values are challenge-specific.
2. **Make HTTP-200 comparison criteria one sentence more concrete.** `QUICKSTART.md:30` says “response that differs” and correctly warns about custom errors; `chapters/02-web-exploitation.md:103` asks for manual inspection. Add body/error-template, response length, and redirect/authentication comparisons immediately there, so a basic solver knows which differences are meaningful. The route is usable now; the missing specificity costs interpretation under pressure.
3. **Carry the explicit CPTS policy warning onto individual notes.** `CPTS.md:5` and README Contents are clear, but the searched HTTP note only shows “Personal reference · Event tool rules.” Add a short “original notes; tools/commands are not event-vetted” sentence near that link. Search can bypass the landing-page explanation, and examples such as the hardcoded ffuf filter make that distinction operationally relevant.

## Score rationale and limits

| Dimension | Score | Basis |
|---|---:|---|
| Findability | 9 | Short reference directly exposed all required routes; one ordinary website query found a relevant personal note. |
| Command usability | 8 | All three helpers ran unchanged except filenames; the encountered personal-note ffuf example needs correction/context. |
| Clarity | 8 | Environments, success outputs, and recovery are explicit; response comparison and direct-entry CPTS caveats could be more concrete. |
| Instruction economy | 9 | Three solves needed only two short Quickstart sections; the web walkthrough needed one focused linked excerpt. |
| Recovery | 9 | The actual labeled-input failure had an applicable written recovery and worked on the next attempt. |

No human timing was invented. RSA beyond this supplied close-factor case, other compression formats, fullsize image behavior, remote Kali commands, scanning behavior, mobile rendering, and broader CPTS correctness remain untested. These are scope limits, not failed guide functionality. The ordinary PowerShell display of README had a few encoding artifacts (for example the middle dot), while the Chrome text displayed normally; this was not scored as a website defect.
