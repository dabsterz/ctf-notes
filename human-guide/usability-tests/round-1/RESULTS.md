# Human-style usability evaluation

The tested guide is useful, but requires too much assembly for a fast contest reference. Three independent simulated reviewers rated contest usefulness **7.3/10 on average**, versus **8.5/10 as a study reference**. These are subjective ratings of the tested material, not measured human performance.

## Results

| Reviewer | Contest use /10 | Study use /10 | Task outcomes | Guide lookups |
| --- | ---: | ---: | --- | ---: |
| Web / crypto | 6.7 | 8.5 | 3 complete | 18 |
| Forensics | 7.9 | 8.5 | 2 complete, 1 partial | 14 |
| Reverse / misc | 7.2 | 8.5 | 3 complete | 8 |

All nine answer candidates matched the withheld answer key. Eight tasks were fully supported; the event task remains **partial** because field extraction succeeded but interpreting event 4688 required knowledge supplied by the task brief rather than the guide. All three reviewers correctly located radare2 in Kali and Ghidra in Windows WSL. This checks documented placement, not installed tool operation.

Lookups include navigation, searches and bounded excerpts; web/crypto includes two provenance-only lookups. Different tasks and reviewer navigation styles mean these counts are not a speed ranking. No human completion times were estimated.

## What caused the burden

1. **Examples require assembly.** RSA uses toy plaintext and generated ciphertext instead of accepting challenge n/e/c; the reader combines factoring, decryption and byte conversion from different examples. The reverse transform section supplies rotation helpers and inverse rules, but the reader writes the complete loop. The VM example emits fixed output; adapting it to an input comparison requires meaningful code. See [crypto](../../../chapters/07-cryptography.md) lines 196–214 and 238–253; [reverse](../../../chapters/06-reverse-engineering.md) lines 307–327 and 377–410.
2. **Useful recipes are separated from the obvious entry point.** The web JWT decoder and concrete mutation example are far apart. Base64 plus zlib is under malware, so the web/crypto reviewer first searched miscellaneous without finding it. The duplicate-tar warning shares a paragraph with OOXML. See [web](../../../chapters/02-web-exploitation.md) lines 174–211 and 541–567; [malware](../../../chapters/09-malware.md) lines 41–80; [forensics](../../../chapters/03-forensics.md) lines 137–169.
3. **Some recipes stop before the next action or interpretation.** The PNG walker saves trailing bytes but does not immediately show their inspection command. The Windows event filter includes 4688 without explaining its fields and meaning. See [steganography](../../../chapters/05-steganography.md) lines 51–83 and [forensics](../../../chapters/03-forensics.md) lines 297–308.

The burden is not uniformly excessive prose before every command: the web/crypto reviewer found most recipe introductions short, and the forensics reviewer found longer working scripts justified. Cutting explanations indiscriminately would lose useful success checks. The better change is to make the shortest complete path easier to find and run.

## What worked

- The crash-pattern recipe ran unchanged and returned the correct offset.
- PNG parsing and duplicate-preserving tar extraction worked, including retaining evidence that ordinary extraction might miss.
- Re-encryption checks, forward transform checks, and server-response validation helped distinguish a candidate from a verified answer.
- Every reviewer rated tool/environment clarity 5/5.

## Recommended revision

Keep the full handbook as a reference. Add a compact contest layer in both Markdown and the website, with one task per card:

**Recognize → Run → Expected result → If it fails.**

Each card should name the environment, accept real input filenames or values, provide a complete command, and show a concrete success check. Link deeper explanations below the card. Prioritize RSA, XOR/rotation, VM input checks, JWT requests, layered decoding, and Windows event interpretation. These are proposed changes; this evaluation did not modify the guide.

## Method and verification

Exactly three fresh-context agents simulated human lookup behavior. They used narrow searches and bounded excerpts, executed commands against nine synthetic local tasks, and recorded adaptations instead of silently filling gaps with specialist knowledge. They were instructed not to read original skills, hidden fixture code, the answer key, external sources or other reports. Ordinary Python/file/HTTP glue was permitted and counted as adaptation. These constraints reduce shortcuts but do not turn agents into human participants.

Ratings weight findability 25%, command readiness 25%, interpretation 15%, low cognitive load 25%, and tool/environment clarity 10%. The parent independently checked score arithmetic and all candidates, directly checked four extracted binary artifacts and the crash-pattern slice, and reran the checker, VM and loopback JWT scripts. VM decimal 75 was normalized to ASCII K. The verified mean is 7.27/10, rounded above to 7.3.

Execution used native Windows Python as a portability proxy. WSL/Kali installations and website navigation, layout and clipboard behavior were not tested; no browser surface was available. Tasks were deliberately small and clue-rich, so this is a recipe-usability check, not proof of performance on unseen competition challenges. The environment lookup checks the guide against its own tool matrix; this round did not independently re-audit every workbook entry.

The 16 chapters contain 253 code blocks and 288 headings. The size measurement counts 43,453 whitespace-separated tokens outside fenced code, including tables, links and headings; this is document size, not a precise natural-language word count or reading-time estimate.

## Evidence

- [Testing protocol](METHOD.md)
- [Web/crypto report](reports/web-crypto.md)
- [Forensics report](reports/forensics.md)
- [Reverse/misc report](reports/reverse-misc.md)
- [Machine-checked results](verified-results.json)
- [Recheck script](grade.py)
- [Document-size measurements](size-metrics.json)

Guide baseline: commit `3a884be4748d1b1cbee118cbab6264e5712219c4`. Only evaluation artifacts were added; the existing guide remains unchanged.
