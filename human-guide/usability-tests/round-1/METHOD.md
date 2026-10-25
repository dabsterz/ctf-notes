# Human-style cheat-sheet usability test

Requested evaluation: three independent subagents test whether the guide helps a human solver during a CTF, with particular attention to instruction burden.

Baseline: commit `3a884be4748d1b1cbee118cbab6264e5712219c4`. The published guide is not edited during this test.

## Participants and tasks

These are simulated human walkthroughs by three independent agents, not a study with real human participants. They received fresh contexts and no access to prior reviewer ratings or each other's reports.

| Tester | Simulated familiarity | Assigned practical tasks |
| --- | --- | --- |
| Web/crypto | Competent generalist; basic Python/HTTP | Modify a JWT in a loopback challenge; recover raw RSA plaintext; decode Base64 then zlib |
| Forensics | Intermediate Windows forensic solver | Recover PNG trailing data; preserve duplicate tar members; interpret an exported process-creation event |
| Reverse/misc | Experienced CTF generalist | Invert a byte checker; find a crash-pattern offset; invert and verify a small VM |

All three also locate radare2's listed environment and an approved Windows/WSL static-analysis alternative.

Fixtures are synthetic and include useful clues. Several tasks test executing a known technique rather than discovering an unknown vulnerability. They do not represent the full difficulty or variety of the competition. The web service binds only to `127.0.0.1:18765`.

Reviewers must use the guide as their technical reference. They may inspect titles, perform narrow text searches, and read bounded excerpts. They may not preload the whole corpus, inspect original skill sources, consult the internet, inspect fixture-generation code or the answer key, or silently solve missing steps from specialist knowledge. Ordinary file handling and basic script glue are permitted and must be logged.

## Evidence and rubric

Reviewers record chronological lookups, copied commands, edits, actual outputs, failed attempts, and interpretation gaps. Results are categorized as completed, partial or blocked. Agent elapsed time is not presented as measured human reading time. The parent checks final candidates against the withheld answer key and verifies scoring arithmetic.

Each dimension is rated 1–5: 1 unusable, 2 major friction, 3 usable with effort, 4 efficient with small edits, 5 immediate clear action.

| Dimension | Weight |
| --- | --- |
| Findability | 25% |
| Command readiness | 25% |
| Result interpretation | 15% |
| Low cognitive load | 25% |
| Tool/environment clarity | 10% |

The contest-use rating is twice the weighted mean, giving a scale out of ten. A high cognitive-load dimension score means low burden. Study-handbook usefulness is a separate subjective rating. The three-reviewer average is a descriptive summary, not a calibrated population estimate.

## Limits

Execution uses local Windows Python as a portability proxy. It does not validate the organizer's WSL/Kali installations. The event tool restrictions remain part of the evaluation. The computer-use inventory returned no browsers, so real website navigation, visual layout and clipboard behavior are not evaluated. Results apply primarily to the shared written content.

`size-metrics.json` counts whitespace-separated tokens outside fenced code, including headings and tables. It measures document size, not the number of necessary instructions or reading time.
