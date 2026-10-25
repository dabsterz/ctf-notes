# Independent simulated-human review

Requested by the user because the guides contain too many instructions. Three fresh, isolated reviewers assess the same frozen guide, without earlier review results or one another's findings. These are agent simulations, not observations of real human participants.

## Method

- Entry: README, then quick reference or website. Reviewers may follow links but may not use outside research, source skills, answer keys, or unwritten solving code to fill gaps.
- Three supplied local tasks per reviewer plus one transfer/navigation scenario without a live target. New fixture values avoid simply repeating the earlier test answers.
- Roles: Windows-oriented forensics beginner; Linux user new to reversing; solver with basic web/crypto familiarity.
- Each reviewer records commands, results, consulted sections, assumptions, recovery and unnecessary reading. Unavailable competition software and host substitutions must be disclosed.
- Scores: findability, command usability, clarity, instruction economy, recovery, each 0?10. Higher instruction economy means less unnecessary effort. Overall score is the equal-weight arithmetic mean.
- Anchors: 9?10 minimal friction; 7?8 minor gaps; 5?6 repeated interpretation; 3?4 major missing bridges; 0?2 unusable.
- `snapshot.json` records hashes of the evaluated documents and helpers. The guide is not rewritten during evaluation.

## Limits

Fixtures are small synthetic exercises and favor the existing helper scripts. They cannot establish success on unseen competition challenges. The fourth scenario in each set is a walkthrough, not a solved challenge. No organizer portal, competition VM or remote target is used. Browser interaction, where unavailable, must not be claimed from source inspection. Scores are judgments by three agents, not statistical measurements of human performance or measured human completion times.
