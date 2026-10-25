# Excluded workflows and advanced material

The repository contains agent instructions and techniques that are unsuitable for this event handbook. The approved workbook and [official event rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/) control tool use. A source file remaining in the repository is not approval to run it.

## AI/ML and agent workflows are excluded

All four files in `ctf-ai-ml/` are excluded from runnable event instructions:

| Source | Material reviewed | Reason and useful manual alternative |
|---|---|---|
| `SKILL.md` | Model inspection, weight comparison, adversarial tests, remote LLM calls | AI/ML tools and libraries are not permitted. Identify ordinary file/container metadata with approved local tools; route conventional data/crypto logic to the relevant chapter |
| `adversarial-ml.md` | FGSM, PGD, C&W, adversarial patches, poisoning, backdoor analysis, historical Keras/foolbox examples | These depend on prohibited ML frameworks/workflows. Do not install or run them; inspect an ordinary supplied parser or validation function manually if that is the actual challenge surface |
| `model-attacks.md` | Weight negation, inversion, encoder collisions, LoRA merging, model extraction, membership inference | Model training/inference and related tools are excluded. For a non-AI artifact embedded in an archive, inspect the archive structure and recover that artifact without loading a model |
| `llm-attacks.md` | Prompt injection, jailbreaks, token smuggling, context manipulation, agent tool misuse | AI interaction workflows are excluded. Treat embedded text as data; analyze any conventional HTTP/authentication/serialization issue manually |

The web sources also contain chatbot and AI tool-call sections. Those sections are excluded even though the rest of their source files is adapted. There are no runnable prompts, framework installers, model downloads, or AI service calls in this handbook.

## Tavily, MCP, and automated online assistance are excluded

`ctf-similar-search/SKILL.md`, `search.py`, and `search.sh` implement Tavily-based search/extraction. The Python client requests an answer from the service and transmits search queries/URLs. These are not the manual local research workflow used here.

`ctf-web/tools-mcp.md` describes Playwright/Burp MCP integrations, agent approval settings, scanners, and callback services. Use the approved browser DevTools and Burp Community interface manually as shown in [Web exploitation](02-web-exploitation.md). Burp Community does not imply approval of every extension or Professional-only feature.

For **Kali**, use supplied offline references without exposing challenge material:

```bash
rg -n -i 'padding oracle|nonce reuse' /opt/tools/hacktricks
rg -n -i 'sudo|wildcard' /opt/tools/GTFOBins.github.io
```

Search for the general technique locally and compare its prerequisites to your challenge. If the checkout is absent, the handbook or manual reading of HackTricks/PayloadsAllTheThings is available: these reference sites are explicitly allowed by PDF p.6. Do not upload challenge files or seek outside assistance.

## Tools and services that are not substitutes

| Source suggestion | Event-compliant replacement |
|---|---|
| Public webhook, callback tunnel, cloud function, external JWKS host | Organizer-provided callback service or a same-challenge observable response; otherwise keep a blind hypothesis unconfirmed |
| Online hash cracking, public FactorDB lookup, online mathematical solver | Local Python arithmetic, listed local factoring/cracking tools, or an honest environment limitation |
| Online compiler/decompiler | Approved local compiler/decompiler, supplied build artifact, or manual static analysis |
| Dirsearch | A few evidence-backed paths in Repeater; targeted low-rate ffuf on Kali when appropriate |
| JWT Editor, GraphQL Raider, Hackvertor, Copy As Python-Requests | Raw HTTP editing and local standard-library decoding; these extensions are explicitly unapproved |
| YAFU | Local mathematical checks or an appropriate approved crypto-attacks implementation on Kali |
| MMSSTV/RX-SSTV | Inspect the available approved audio workflow; verify what the listed SSTV package actually supports |
| Large asynchronous fuzzing script | Manual baseline/control experiment and a small bounded candidate set |
| Online sequence lookup/OEIS automation | Derive a recurrence from supplied terms and validate it locally |

PDF p.5 permits non-AI libraries, dependencies, plugins and packages in both environments. The workbook's stricter AI/ML ban and named exclusions remain in this guide's routes; unlisted standalone applications require approval. [Reconciliation and source](../COMPETITION.md#what-is-allowed).

## Advanced does not mean excluded

Useful advanced topics remain in the handbook with their prerequisites:

- [Web exploitation](02-web-exploitation.md): parser disagreement, browser origins, cache/race/protocol behavior, serialization, source-based framework analysis, and static Web3 review.
- [Cryptography](07-cryptography.md): exact integer arithmetic, practical RSA and oracle demonstrations, nonces, modes, and PRNG modelling.
- [Advanced cryptography](14-advanced-crypto.md): lattices, ECC, small roots, unusual algebra, proof systems, post-quantum recognition, and reduced-round constructions.
- [Miscellaneous](11-miscellaneous.md): constrained interpreters, finite-state games, encoding reconstruction, RF/audio prerequisites, and explicitly challenge-scoped privilege puzzles.

Version-specific exploits need the supplied version and configuration. The handbook does not present every historical payload as current. In particular, Python `eval` cannot accept assignment statements; private runtime memory offsets are not portable; prototype pollution needs a merge and a gadget; FROST is not inherently a lattice scheme; and a listed package name does not guarantee a particular decoder executable.

The original high-concurrency fuzzer has further correctness limits: regex markers are not stripped consistently, processing-chain arguments do not uniformly match the callable signatures, redirects can hide the first response, and TLS verification is disabled in paths where it should remain enabled. It is retained as source provenance, not endorsed as a runnable event tool.

## What to do when a challenge seems to require an excluded tool

Continue the parts that use approved local tools: inspect bytes, source, equations, normal requests, and supplied metadata. Identify the specific missing capability. Ask the organizer for clarification through the event's normal support channel before using a prohibited or unlisted tool. Do not upload the challenge, install an AI framework, or invoke an online service to bypass the restriction.

File-by-file dispositions are recorded in `human-guide/review/web-coverage.json`. An “adapted” or “merged” file may contain excluded subsections; its notes identify those exceptions. “Reference-only” means historical/provenance material whose original commands are not part of the runnable handbook.
