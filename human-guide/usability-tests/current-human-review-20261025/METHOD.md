# Current guide: independent simulated-human review

Three fresh-context agents assess the frozen guide at commit `b550a6f30d97bf9212d38f04b6f037c18a199b98`. Personas: Windows-oriented forensics beginner; intermediate Linux user new to reversing; solver with basic web/crypto familiarity. These are constrained agent simulations, not recruited human participants.

## Tasks and boundaries

- Start at the reader README, then follow the website or linked Markdown using bounded searches and relevant excerpts.
- Each reviewer receives three executable local exercises plus one transfer/navigation scenario without a live target. The inputs are copied from the earlier human review (including its corrected RSA input), with previous outputs and solutions removed. Reusing the inputs helps compare task coverage; it is not a new unseen challenge benchmark.
- Add actual offline Chrome interaction with the current website: find a relevant CPTS note, navigate/search, distinguish personal notes from competition tool approval, and assess command copying and screenshot controls where present.
- Use documented solving commands and supplied scripts. Ordinary filename and working-directory substitutions are allowed and must be disclosed. Do not invent algorithms, preprocessing, or missing instructions to rescue the guide.
- Do not read prior reports, other reviewers' findings, answer keys, fixture generators, source CTF skills, builder/application implementation, or outside sources. Browser harness code may operate visible UI, but may not inspect the embedded data to bypass reader navigation.
- Exercise a documented recovery branch. Record commands, results, reading paths, assumptions, unnecessary reading, and unavailable tools. Do not install tools, touch remote targets, or execute commands from personal CPTS notes against infrastructure.
- Write outputs only inside the assigned reviewer folder. Keep the guide unchanged throughout evaluation. The snapshot hashes 276 reader, helper, asset and CPTS files.

## Rating

Score findability, command usability, clarity, instruction economy, and recovery from 0 to 10. Higher instruction economy means less unnecessary effort. Overall is the equal-weight arithmetic mean of these five scores.

Anchors: 9-10 minimal friction; 7-8 minor gaps; 5-6 repeated interpretation; 3-4 major missing bridges; 0-2 unusable. The parent checks arithmetic and saved evidence without changing the reviewers' judgments.

## Limits

These small synthetic inputs favor the supplied helpers. Prepared JSON is not equivalent to reverse-engineering an unknown binary. Navigation scenarios are not solved live challenges. Actual local WSL/PowerShell and Chrome interaction must be distinguished from organizer-machine availability. No human reading speed or completion times are measured. Comparisons with the earlier 6.8/10 review are descriptive judgments from different simulated readers; the added website/CPTS checks also change the scope.
