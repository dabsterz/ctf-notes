# Round 2: web / crypto simulated walkthrough

Simulated competent-generalist walkthrough, not human participant research. Used native Windows Python as a portability proxy; no claim about Kali, WSL, browser or event availability. No hidden fixtures, server source, other reviews, original skills or internet were consulted.

| Task | Result | Evidence |
| --- | --- | --- |
| JWT | Completed: `CTF{new_request_verified}` | Baseline HTTP 403 `admin required`; edited token HTTP 200 with flag. Both responses saved beside the token files. |
| RSA | Completed: `R2_RSA` | Bounded default Fermat recipe found factors `32416187567`, `32416190071`; re-encryption OK; `rsa-plain.bin` saved. |
| Layers | Completed: `CTF{new_layer}` | Base64 decoded to 22 compressed bytes; 14-byte layer2; complete stream, zero trailing bytes. |

All three included recipes ran unchanged on the first attempt. Commands used `python ../../../recipes/jwt_claim.py token.txt`, `python ../../../recipes/rsa.py rsa.json`, and `python ../../../recipes/layers.py message.txt --out decoded`, from the assigned folder. No algorithms were invented and no recipe repairs or guide edits were made. One inline 12-line Python HTTP/file loop replaced the Bash curl commands, recorded the original 403 and edited 200, and saved each response. This was basic transport glue, not a JWT repair. `python3` became `python`, and recipe paths were adjusted to the task folder.

Seven chronological lookups: README; START; narrow task-term search of QUICKSTART/TOOL-CHOOSER; QUICKSTART 19-60; QUICKSTART 128-151; TOOL-CHOOSER 1-40; TOOL-CHOOSER selected 104-117 and 159-172. The last two occurred after solving. Directory listing and execution are not counted as guide lookups. No deeper chapter or recipe help was needed.

| Dimension | Score / 5 | Reason |
| --- | --- | --- |
| Findability | 5 | Task terms directly located compact routes. |
| Command readiness | 4 | Packaged scripts worked unchanged; request syntax needed native-Windows translation. |
| Interpretation | 5 | Server acceptance, re-encryption and compressed-stream completion gave clear evidence. |
| Cognitive load | 5 | Short local excerpts sufficed; high score means low burden. |
| Tool/environment | 4 | Environments were explicit; actual event deployments remain untested. |

Weighted overall: **9.3/10** (.25/.25/.15/.25/.10). Separate study usefulness: **9.0/10**. These are subjective simulated-walkthrough scores, not measured participant outcomes. No reading-time claim is made.

Tool selection: use ffuf for flexible hidden-path discovery or Gobuster for straightforward directory scans, with a nonexistent-path baseline and candidate verification. Use John for a known offline hash format, or hashcat when its mode and compute backend are known. Use Hydra for challenge-authorized live SSH guesses: service latency and lockouts apply; it does not crack offline hashes. No network guessing was performed.

The Web, Passwords, Cryptography and Misc tables state useful strengths and failure modes without treating every tool as interchangeable. No confirmed technical error was found within this restricted review; version-specific flags and workbook approvals were not independently verified. Small clarity improvements:

- `human-guide/TOOL-CHOOSER.md:34`: show one ambiguous hashid result so readers understand why shape is only a suggestion.
- `human-guide/TOOL-CHOOSER.md:112`: tie close primes directly to Fermat and the bounded Python fallback; the conditional help-first route otherwise adds a step for novices.
- `human-guide/TOOL-CHOOSER.md:165`: label the layers first command as the Base64/compression case or link its use-when paragraph; Python's general strengths are broader than this recipe.

The main remaining friction is shell/path context, not instruction volume. The guide correctly distinguishes WSL and Kali and warns about file transfer. Native PowerShell request copying still requires glue; that is a limitation of this proxy evaluation, not evidence that the documented Kali commands fail. The supplied synthetic tasks exercise successful routes only and do not establish general CTF solving performance.
