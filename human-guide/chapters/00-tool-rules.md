# Tools and competition rules

Use the [competition setup page](../COMPETITION.md) for the PDF's rules, VPN access and machine limits. This page covers the supplied workbook, `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`: **39 Windows/WSL entries, 161 Kali entries, and 82 unapproved entries**, including all installation remarks. Counts refer to rows, not unique executable names.

## Read approval and availability separately

| Label | What it means | What to do |
| --- | --- | --- |
| Approved · Windows | Listed on the Windows sheet and installed natively according to its location column. | Use the Windows GUI or PowerShell invocation shown. |
| Approved · WSL | Listed on the Windows sheet, but installed in WSL. | Enter the existing WSL environment first. |
| Approved · Kali | Listed on the Kali sheet for the supplied AWS environment. | Use that environment and check the recorded location. |
| Approved · availability uncertain | Listed, but version/path is missing or startup failed. | Check availability early; keep the documented alternative ready. |
| Unapproved | Appears on the unapproved sheet; reasons include installation failure and explicit prohibition. | Use the listed alternative. The PDF does not expressly clear these named entries; resolve a needed exception through official support. |
| Not listed | No explicit entry was found. | Unlisted standalone apps need organizer approval. Non-AI libraries/dependencies/plugins/packages follow PDF p.5. |

The guide conservatively keeps named unapproved entries out of its practical routes. An installation failure and a rule prohibition are different reasons; the matrix preserves the original wording.

Routine shell syntax and basic filesystem commands are operating-system facilities. For additions, follow [PDF p.5 and the workbook reconciliation](../COMPETITION.md#what-is-allowed); a permitted plugin is not necessarily installed, and a local tool listing does not authorize an online service.

## The important restrictions

Prepared notes and scripts are allowed. During competition, stay within assigned targets, collaborate within your team, and use permitted reference sites. Do not use generative-AI assistants, obtain outside help, share challenge content externally or upload challenge files to online services. Automatically displayed AI search summaries are the PDF's stated exception. [Complete rules and sources](../COMPETITION.md#what-is-allowed).

The workbook's Windows `B5`, Kali `B4`, and Windows `H14:H15` prohibit AI/ML libraries and tools. Keep this stricter exclusion alongside the PDF's non-generative-AI package allowance. Check installation separately from permission.

There are no agent/MCP instructions in the working recipes. Do not use the original repository's agent installer, AI model routing, promptfoo evaluations, Tavily search, or AI/ML attack tooling during the competition. Read the exclusions chapter for their dispositions.

The unapproved sheet explicitly rejects online analysis services and online decompilers/compilers (`B51:C52`), including examples such as VirusTotal and CrackStation. Do decompilation, decoding, hashing, and cracking locally with listed tools. The locally installed `factordb-python` entry does not resolve permission to upload a challenge modulus to FactorDB. Similarly, the listed local AperiSolve checkout does not authorize the public upload website.

## Windows is not the same thing as WSL

The workbook lists these as native Windows tools: Chrome, Wireshark/TShark, a PDF viewer, OpenVPN Client, x64dbg, Autopsy, HxD, Notepad++, dnSpyEx, and Eric Zimmerman's Tools. CyberChef is a browser bookmark. WSL itself is installed on Windows.

Python 3, uv, GDB, objdump, strings, zsteg, binwalk, ExifTool, pdftotext, can-utils, cannelloni, Zeek, ZBar, Burp Community, jq, Ghidra, Sleuth Kit, OpenSSL, xz, qpdf, llvm-mc, xxd, fsck.fat, RsaCtfTool, and Volatility 3 are marked as installed **in WSL**. The OpenSSH recovery plugin is marked as installed in Volatility 3. See Windows `C14:I39`.

Run this in **PowerShell** to see the existing distributions. It does not install anything:

```powershell
wsl --list --verbose
wsl
```

Use the existing distribution. A Windows path such as `C:\Users\YourName\Downloads\challenge.bin` normally becomes `/mnt/c/Users/YourName/Downloads/challenge.bin` inside WSL. Quote paths with spaces. Do not assume that files on the remote Kali AWS machine also exist on the Windows laptop.

Inside **WSL**, check the tools you will need:

```bash
python3 --version
command -v gdb objdump strings exiftool xxd binwalk
python3 -c "import sys; print(sys.executable)"
```

Inside **Kali**, check its separate installation:

```bash
command -v file curl rg r2 checksec ffuf sqlmap
r2 -v
python3 --version
```

Output paths prove that a command is discoverable. A missing path means it is not on `PATH`, not necessarily that it is absent. Check the tool matrix for `/opt/tools/...` locations before giving up. Running `--help` is often more reliable than `--version`; the workbook records several tools that do not support a version option.

## Predictable problems and approved alternatives

| Problem | Better route |
| --- | --- |
| IDA Free or Binary Ninja is unavailable | Ghidra in WSL, or radare2 on Kali. |
| Windows Procmon/WinDbg is unavailable | Use the specific x64dbg workflow or inspect offline artifacts with Autopsy/Zimmerman tools. Linux strace observes Linux programs only. |
| ImHex or an image-mounting utility is unavailable | HxD on Windows; xxd in WSL; Sleuth Kit extraction without mounting. |
| Copy As Python-Requests / JWT Editor / Hackvertor is unavailable | Burp Repeater, curl on Kali, Python standard library in WSL. |
| Dirsearch is unavailable | Approved ffuf, Gobuster, or Feroxbuster with a small, relevant wordlist and bounded rate. |
| SageMath is listed but does not start | Basic RSA/XOR/modular arithmetic recipes use Python; advanced lattice work still needs a working supported environment. |
| A Python package imports in one tool but not in `python3` | pipx isolates environments. Use the installed application entry point; do not assume every module is globally importable. |
| A GDB plugin fails or conflicts | Use `gdb -nx` for plain GDB; GEF is separately recorded at `/opt/tools/gef.py`. |
| Volatility reports missing symbols | Record the exact OS/build and existing symbols. The full Volatility 3 symbol-table ZIP collection is unapproved (`B82:C82`). Use other artifacts instead of promising a fix. |
| The listed SSTV command does not decode | The Kali entry says decoder but records PySSTV, which may be an encoder package. Check its help; use the audio diagnostic workflow and do not assume MMSSTV/RX-SSTV approval. |

## Non-AI Python package checks

Prefer standard-library recipes. For an optional library, verify it without running an installer:

```bash
python3 -c "import importlib.util; print({m: importlib.util.find_spec(m) is not None for m in ('Crypto', 'sympy', 'PIL', 'pwn', 'z3')})"
```

`True` means the active interpreter can find a module, not that its version is compatible or that every capability is permitted. `Crypto` is the import name typically provided by PyCryptodome; `PIL` comes from Pillow; `pwn` from pwntools; `z3` from z3-solver. These names are not interchangeable with package installation names. No blanket installation commands are included.

PDF p.5 permits non-AI libraries/dependencies/plugins/packages in either environment, subject to the named exclusions above. If a recipe needs PyCryptodome, first check `python3 --version`. Choose a fresh `.ctf-venv` directory in your challenge folder. **WSL, using its listed uv:**

```bash
uv venv --python "$(command -v python3)" .ctf-venv
uv pip install --python .ctf-venv/bin/python pycryptodome
.ctf-venv/bin/python -c 'from Crypto.Cipher import AES; print(AES.block_size)'
```

**Kali, if its existing Python supports venv/pip:**

```bash
python3 -m venv .ctf-venv
.ctf-venv/bin/python -m pip install pycryptodome
.ctf-venv/bin/python -c 'from Crypto.Cipher import AES; print(AES.block_size)'
```

The check should print `16`. Run your saved script with `.ctf-venv/bin/python your_script.py`. A new environment does not inherit all system packages. If venv, pip or package access is unavailable, use WSL's uv route or a standard-library alternative. These commands add a library; they do not approve an unlisted standalone app or its external tools. [Python venv](https://docs.python.org/3/library/venv.html), [uv environments](https://docs.astral.sh/uv/pip/environments/).

## Do not lose time to the repository installer

The source's `scripts/install_ctf_tools.sh all` is designed for an unrestricted agent workstation. It is not a competition setup step. It installs a broad collection that does not match this event's whitelist. Likewise, the original generated catalog loads external analytics and links to agent skills; this offline website does neither.

Use the tool matrix to resolve a concrete need. The PDF says installation used the latest versions available when it began in mid-October; workbook versions are a record, not a guarantee of the runtime version. Check the supplied tool's `--version` and `--help` before using version-sensitive options.
