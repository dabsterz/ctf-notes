# Web / crypto human-cheatsheet usability test

This is an agent simulation of a competent human generalist under contest pressure, not a real human participant study. No timings are claimed. Entry was README.md, then the assigned START.md. Technical reference was only the human guide. No original skill sources, server implementation, preparation script, answer key, prior reviews, other tester reports, or external internet were read. The only network target was http://127.0.0.1:18765.

All three practice tasks completed. The common tool lookup completed as a read-only reference check. Execution used native Windows Python 3.14.4 from PowerShell as the requested portability proxy. WSL, Kali, browsers, the website UI, Ghidra, and radare2 were NOT executed or tested.

## Ordered lookup log

A lookup means one narrow text search, file-inventory view, or separately selected document/range. Multiple ranges in one shell invocation count separately because a human still jumps to each. Fixture input reads and runtime commands are listed separately, not counted as guide lookups. All excerpts were bounded; the complete handbook was searched for one term, never preloaded for reasoning.

| # | Query / page jump | Result |
|---|---|---|
| 1 | Read human-guide/README.md | Learned shorter chapters exist; tool list is TOOL-MATRIX.md; Windows rows may mean WSL. |
| — | Read web-crypto/START.md | Three tasks, known JWT verification omission, textbook RSA, Base64 after zlib, tool lookup. |
| 2 | `rg --files human-guide/chapters human-guide/usability-tests/round-1/web-crypto` | Identified web, crypto, miscellaneous chapter names and fixture names. |
| 3 | `rg -n -i 'jwt' human-guide/chapters/02-web-exploitation.md` | Main JWT section at 174 and confirmed missing-verification toy at 541. |
| 4 | Web lines 174–211 | Decoder, condition for editing claims, token placeholder; no HTTP request recipe here. |
| 5 | Web lines 541–571 | Exact claim modification algorithm, instructions to use captured token and verify server result. |
| — | Execute GET /session and JWT test | Baseline denied, edited claim accepted; evidence below. |
| — | Read rsa.json | n=1050809297549059047257, e=65537, c=851485018878019216495. |
| 6 | `rg -n -i 'textbook\|small exponent\|cube\|integer root\|padding\|RSA'` in crypto (actual command used regex alternatives with `|`) | Known-factor, factor-check, and structural recipes. e=65537 did not suggest low-exponent route. |
| 7 | Crypto lines 196–257 | Fermat bounded check plus known-factor private exponent and re-encryption verification. |
| 8 | `rg -n 'to_bytes\|bit_length'` in crypto (regex alternatives) | Bytes section at 71; warning about lost leading zeros at 80. |
| 9 | Crypto lines 60–90 | Integer-to-bytes example assumes original length already known. |
| — | Execute RSA adaptation | Bounded Fermat immediately returned factors; re-encryption matched. |
| — | Read message.txt | `eJxzDnGrzkmsTC0qjk8sSo1PqixJLa4FAFmwCIM=`. |
| 10 | `rg -n -i 'zlib\|base64'` in 11-miscellaneous.md (regex alternatives) | Base64/hex toy, no zlib hit. This was the only unsuccessful category route. |
| 11 | `rg -n -i 'zlib' human-guide/HANDBOOK.md` | Several CRC/format mentions, plus relevant Base64 compression recipe at 4154. |
| 12 | Handbook lines 4137–4190 | Complete bounded decompressor preserving layer1.bin and layer2.bin. |
| 13 | `rg -n 'Decode scripts\|For a Base64 layer\|decoded bytes:'` in 09-malware.md (regex alternatives) | Located corresponding chapter lines 41,55,77 for provenance. |
| — | Execute decoder | Both layers preserved and text recovered. |
| 14 | `rg -n -i 'radare2\|ghidra' human-guide/TOOL-MATRIX.md` (regex alternatives) | Ghidra Windows worksheet / WSL row; radare2 Kali row. |
| 15 | Tool matrix lines 1–39 | Environment distinction and Ghidra location confirmed. |
| 16 | Tool matrix lines 43–54 | Kali heading confirmed. |
| 17 | Tool matrix lines 161–173 | radare2 6.0.5, Kali C123, installation note blank. |
| 18 | Malware lines 41–80, plus `python --version` | Re-read just the recipe range to make exact chapter citations; interpreter is Python 3.14.4. |

**Guide lookup count: 18**, including 2 provenance-only lookups (#13 and #18). The solving/reference route itself used 16. Three additional fixture reads were START.md, rsa.json, and message.txt. The task totals are orientation 2, JWT 3, RSA 4, layers 5 (2 for provenance), tools 4.

## Executed evidence and adaptation

Scripts are retained in the sibling `../web-crypto/` fixture directory. They are the actual executed scripts, not hypothetical walkthroughs. No guide files were changed.

### 1. JWT — completed

Algorithm: [02-web-exploitation.md:549](../../../chapters/02-web-exploitation.md#L549) through line 564. The guide explicitly says this models a verifier that omits signatures and recommends server verification at line 567. I preserved the captured header/signature and changed only role to admin. This is a missing-verification exploit, not a valid signature forgery.

Actual scripts: `../web-crypto/get_session.py`, `../web-crypto/test_jwt.py`. The first uses basic `urllib.request.urlopen` to GET the supplied session endpoint and save its JSON response. The second copies guide encode/decode and claim mutation, loads the captured token, and uses a small independently authored HTTP wrapper for baseline and edited requests. The HTTP/file wrapper is generalist glue; no independent attack algorithm was supplied.

Actual commands from workspace root:

```powershell
python human-guide/usability-tests/round-1/web-crypto/get_session.py
python human-guide/usability-tests/round-1/web-crypto/test_jwt.py | Tee-Object human-guide/usability-tests/round-1/web-crypto/jwt-output.txt
```

Actual stdout:

```text
GET /session: {"token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiAicHJhY3RpY2UiLCAicm9sZSI6ICJ1c2VyIn0.invalid"}
baseline claims: {'sub': 'practice', 'role': 'user'}
baseline GET /flag: (403, '{"error": "admin required"}')
modified: eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJzdWIiOiJwcmFjdGljZSIsInJvbGUiOiJhZG1pbiJ9.invalid
modified GET /flag: (200, '{"flag": "CTF{verify_the_signature}"}')
```

Candidate: `CTF{verify_the_signature}`. Expected baseline HTTPError 403 was caught and printed. No unhandled error or failed execution occurred.

### 2. RSA — completed

Algorithm: Fermat at `07-cryptography.md:238–250`, private exponent and re-encryption at `:201–213`, byte conversion at `:71`. Trying the bounded close-prime check on this single modulus was a heuristic, not a claim that the supplied facts established close primes.

Actual script: `../web-crypto/test_rsa.py`. It loads n/e/c from the fixture, uses the guide Fermat function without algorithm changes, then combines the guide private-exponent and verification lines. I removed toy encryption and its known-message assertion. Independent sizing glue `(recovered.bit_length() + 7) // 8` supplies a minimal byte length; this formula is not printed by the guide. The guide does warn about leading zeros. Integer-only textbook RSA does not establish an original leading-zero count, so this is a minimal-length plaintext candidate.

```powershell
python human-guide/usability-tests/round-1/web-crypto/test_rsa.py | Tee-Object human-guide/usability-tests/round-1/web-crypto/rsa-output.txt
```

Actual stdout:

```text
Fermat factors: (32416187567, 32416190071)
plaintext integer: 4851580194599952765
re-encryption: 851485018878019216495 matches: True
minimal-length plaintext bytes: b'CTF{rsa}'
```

Candidate: `b'CTF{rsa}'`, saved as rsa-plaintext.bin. p*q and re-encryption assertions passed. No runtime errors occurred. No external factoring tool or hidden answer was used.

### 3. Base64 + zlib — completed

Algorithm: `09-malware.md:58–77`. Actual script: `../web-crypto/decode_layer.py`. Changed only the input filename from encoded.txt to message.txt in the decoder; added byte/header/text prints for inspection. No decompression repair or invented domain algorithm.

```powershell
Push-Location human-guide/usability-tests/round-1/web-crypto
python decode_layer.py | Tee-Object layer-output.txt
Pop-Location
```

Actual stdout:

```text
decoded bytes: 21 unused trailing bytes: 0
layer 1 header: 789c length: 29
layer 2 bytes: b'CTF{layers_are_bytes}'
layer 2 text: CTF{layers_are_bytes}
```

Candidate: `CTF{layers_are_bytes}`. Original message.txt remains; layer1.bin contains 29 compressed bytes; layer2.bin contains 21 decoded bytes. Strict Base64 decode passed, decompressor EOF assertion passed, unused trailing bytes was zero. No runtime errors occurred.

### Common tool lookup — completed, read-only

radare2 is listed in **Kali**, version 6.0.5, source cell `Approved Tool List for Kali!C123` (`TOOL-MATRIX.md:170`). A listed local static reversing alternative is **Ghidra**, version 12.1.4, **installed in WSL**, Windows worksheet C29 (`TOOL-MATRIX.md:32`). Blank radare2 installation information is not a guarantee of operational availability (`TOOL-MATRIX.md:3`). No tool installation or launch was attempted.

## Friction counts

Five guide code blocks required adaptation or extraction: JWT toy; RSA factor-check toy; RSA known-factor toy; bytes toy; compressed-layer decoder. Four scripts were authored/saved, three of which adapt guide attack/decoding recipes; the fourth only captures HTTP input. All four executed successfully on their first run.

Required conceptual edits: JWT 2 (replace synthetic token; add endpoint transport/response evidence); RSA 3 (use fixture n/e/c and remove toy-generated data/assertions; join factor output to decryption; choose output byte length); layers 1 (input filename). Total **6 task adaptation steps**, plus diagnostic output and path glue. This is a count of input/workflow changes, not changed source lines.

Explicit all-caps placeholder encountered: **1**, `PASTE_YOUR_CHALLENGE_TOKEN` at web line 199, in an inspection command that was not executed. Implicit input substitutions needed by used blocks: **5 fields/groups** — captured JWT, modulus n, exponent e, ciphertext c, compressed input filename. Known role=admin already matched the toy. There were no package-install detours. RSA needed one bytes-reference detour; layers needed one failed-category/search detour. Native Python was an intentional testing substitution for documented WSL Python, not a verified competition environment.

Narrative before action was usually short: web heading 174 to decoder code 180 has two prose lines/paragraphs (explanation and save instruction), and the relevant mutation heading 541 to code 545 has one paragraph. Crypto heading 196 to code 200 and close-prime heading 221 to code 225 each have one short save instruction. Bytes heading 62 to code 66 also has one short instruction. The compression recipe itself is immediate after its lead-in at malware 55 (code begins 57), but its parent heading is line 41: three paragraphs and an unrelated PowerShell example intervene before the relevant Python block. The main burden was locating and adapting toys, not long preambles at the final recipe.

## Scores

Scale: 1 unusable, 2 major friction, 3 usable with effort, 4 efficient with small edits, 5 immediate clear action. Higher cognitive-load score means lower load.

| Dimension | Score /5 | Weight | Reason |
|---|---:|---:|---|
| Findability | 3 | 25% | Web search worked; layered decoding required a whole-handbook search after a plausible chapter miss. |
| Command readiness | 3 | 25% | Recipes executed, but JWT transport and RSA composition/byte sizing were reader work. |
| Interpretation | 4 | 15% | JWT remote evidence warning, RSA re-encryption, and decompressor EOF give useful success checks. |
| Cognitive load | 3 | 25% | Selecting toy lines, removing assertions/data, and joining three RSA blocks required concentration. |
| Tool/environment clarity | 5 | 10% | Matrix answers Windows/WSL versus Kali explicitly and warns about missing location data. |

Weighted mean = 3*0.25 + 3*0.25 + 4*0.15 + 3*0.25 + 5*0.10 = **3.35/5**. Overall cheat-sheet usefulness = 2*3.35 = **6.7/10**. Separate study-handbook usefulness: **8.5/10**. The worked examples and explicit validation assumptions teach well; the material is less immediate when adapting to contest inputs.

## Top three fixes

1. **Give RSA a real-input entry point.** At `chapters/07-cryptography.md:203–212`, the known-factor example creates its own plaintext/ciphertext and asserts the already-known message. At `:252–253`, factor-check input and expected factors are also fixed toy data. `:71` needs an original byte length the solver does not have. Add a compact n/e/c input recipe that tries the bounded check, decrypts, prints bytes, and verifies re-encryption. Keep the learning toy below it.
2. **Cross-link compression from the obvious decoder route.** `chapters/11-miscellaneous.md:51` names Base64, while the actual Base64+zlib route is under malware at `chapters/09-malware.md:55`. Put a short `Base64 -> 78 9c / gzip header -> decode_layer.py` pointer beside the encoding table. The heading should mention Base64/gzip/zlib so chapter navigation can find it.
3. **Put captured-token mutation beside JWT inspection.** `chapters/02-web-exploitation.md:204` describes editing a claim, but its concrete mutator is at `:541–567`. Add a direct link and a small command accepting a token, then show the Bearer request shape. An experienced HTTP user can supply transport, but a cheat sheet should reduce that stitching work.

Concrete wording recommendation:

BEFORE (`02-web-exploitation.md:567`): “For the challenge, use your captured token and only the role/identity claim the broken verifier actually consumes. Send the modified token to the known flag endpoint, then verify the returned flag. A decoder displaying admin locally proves nothing about the server: a correct verifier rejects this token.”

AFTER: “Confirmed missing verification: replace the toy token with `/session`'s token; change the consumed role; send `Authorization: Bearer <modified>` to `/flag`. Success means the server returns the flag, not merely a local admin claim.”

A stronger code change would accept the token as a command-line input and leave the example token in a separate demonstration.

## Limits

This is one simulated tester and three deliberately narrow synthetic challenges whose starting brief already establishes important attack prerequisites. It measures discoverability and adapting supplied recipes, not open-ended vulnerability discovery. No real human behavior, contest speed, WSL/Kali operability, browser UI quality, broad cryptographic coverage, or tool installation success is inferred. No errors were hidden or rescued. The byte-sizing formula and HTTP/file/printing glue were independently supplied generalist work and were counted against command readiness. Verification is the local server response, RSA mathematics, and decoder consistency; the withheld answer key was not read.
