# Start here: the human solver's field guide

This is a practical companion to the CTF skills repository: find the symptom you have, run a small test, interpret the result, and choose the next step. You do not need to know the vulnerability name before opening a chapter.

**Built for both Windows/WSL and Kali.** Commands tagged `bash` belong in a Linux terminal, including WSL. Commands tagged `powershell` belong in Windows PowerShell. A `python` block is a script: save it under the filename given, then run it using the Python interpreter in that environment. Never paste a multiline Bash command straight into PowerShell.

## What to read tonight

1. Read **Tools and competition rules** and check the tools you expect to use.
2. Work through **First ten minutes** with one small local file.
3. Choose two of the six main subjects: web, forensics, network, steganography, reverse engineering, and cryptography. Read their opening workflows, then try a concrete recipe.
4. Keep the **tool matrix** handy when a familiar program is missing. Approved does not mean installed correctly.
5. Use the supplementary pwn, malware, OSINT, miscellaneous, and advanced sections when the evidence calls for them.

The official 2026 event page identifies AJCCBC and Trend Micro, lists the six main categories, and gives 26–27 October in Bangkok. This guide prioritizes those subjects; the vendor's identity does not reveal tomorrow's challenges. [Official event page, checked 25 October 2026](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## Find your starting point

| What you have | First useful question | Open |
| --- | --- | --- |
| A website, cookie, request, or source archive | Where does my input reach a trust decision? | Web exploitation |
| A disk image, event log, registry hive, or memory dump | Which artifact answers the question, and in what time zone? | Forensics |
| A PCAP or stream of packets | Which conversation carries the relevant data? | Network |
| An image, audio file, PDF, or suspicious whitespace | Is it damaged, appended, encoded, or hiding a second layer? | Steganography |
| An ELF, EXE, APK, DLL, WASM, or bytecode file | Where is the input compared with the expected value? | Reverse engineering |
| Large numbers, ciphertext, an oracle, or encryption source | Which assumption does the implementation break? | Cryptography |
| A native program with an established corruption bug | What can I read or overwrite, and what protections matter? | Binary exploitation |
| A packed script or suspicious executable | Can I recover the behavior without executing it? | Malware |
| A clue about a place, identity, or domain | What independent evidence would distinguish the candidates? | OSINT |
| A restricted interpreter, layered encoding, game, or signal | What are the exact rules and data representation? | Miscellaneous |

Categories overlap. Recover a file from a packet capture, identify its format, then switch to the appropriate chapter. A remote port alone does not make a challenge pwn.

## How each recipe works

**Recognize:** the clues that justify trying it. **Run:** a command or complete small script. **Read the result:** what success, failure, and misleading output look like. **Next:** the cheapest evidence-backed follow-up.

Examples use names such as `challenge.bin`, `capture.pcapng`, and `image.png`. Replace them with your actual filenames. Addresses such as `challenge.example` are placeholders, not live targets. Addresses, offsets, stream numbers, process IDs, database names, and flags in examples are illustrative unless explicitly called a self-contained toy.

Commands are recipes, not a script to run top to bottom against every challenge. Read the surrounding paragraph before copying a block. Some blocks contain several alternatives; choose the one that matches your evidence.

## Read this guide in either format

- **Website:** open `index.html` in Chrome. It embeds all content, styles, and search data. It makes no network requests. Search accepts several words, such as `RSA shared prime` or `Windows event log`. Press `/` to focus search and Escape to return to the chapter.
- **Markdown:** open `HANDBOOK.md` for the whole guide, or a file in `chapters/` for a smaller topic. Obsidian, VS Code, Notepad++, or a plain text editor can read it.
- **Print:** the website's print button prints the current chapter. Search results can also be printed. Code blocks wrap in print but preserve their original text when copied.
- **Tool matrix:** look up the exact program name and its environment. The workbook is the authority for the supplied list, not a package's popularity.

The guide is prepared study material. The supplied list does not establish whether bringing this handbook, prepared scripts, or removable media is permitted. Check that specific point with the organizers before using it during the event. No AI service is needed to read it.

## Useful vocabulary

| Term | Meaning in a solve |
| --- | --- |
| Artifact | A file or record you can examine: capture, dump, log, image, or executable. |
| Baseline | A normal request or input whose output you record before changing one thing. |
| Primitive | A specific ability you have proved, such as reading one file or leaking one address. |
| Offset | A distance from a known starting point. State whether it is bytes, sectors, or a virtual address. |
| Endianness | The order of bytes in a number. x86 commonly stores the least significant byte first. |
| Encoding | A reversible representation, such as hex or Base64. It does not require a secret key. |
| Encryption | A keyed transformation. Correct decoding alone does not decrypt it. |
| Oracle | A service whose answers reveal something about a hidden value. |
| False positive | An output that resembles your answer without enough evidence to support it. |
| Pivot | Changing approach because a result points somewhere else. |

## What this edition preserves

The original repository remains available alongside this folder. Repeated agent instructions have been consolidated into human workflows. Advanced and historical material has its own sections, with prerequisites rather than promises that old exploits work on new systems. The source coverage appendix records where each original file went and what was excluded. Original examples are not all validated exploits; this edition is also not a guarantee that an organizer's installation will run every command unchanged.
