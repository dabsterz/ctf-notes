# Tool matrix: the complete supplied list

Source: `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`. Recorded versions are copied as supplied, not independently verified. Blank installation notes do not establish availability. The unapproved reasons are retained verbatim. The workbook contains some replacement characters; these are preserved rather than guessed.

Windows/WSL and Kali are separate environments. See the location column before choosing a command. For non-AI additions, named exclusions and hosted-service restrictions, use [Competition setup](COMPETITION.md#what-is-allowed).

## Windows / WSL · 39 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| CyberChef | Latest (browser-based, no install) | Bookmark | — | Approved Tool List for Windows!C8 |
| Wireshark | Latest | installed in Windows | — | Approved Tool List for Windows!C9 |
| PDF Viewer | Any current version | installed in Windows | — | Approved Tool List for Windows!C10 |
| OpenVPN Client | Latest | installed in Windows | — | Approved Tool List for Windows!C11 |
| Google Chrome | Latest | installed in Windows | — | Approved Tool List for Windows!C12 |
| Windows Subsystem for Linux (WSL) | Latest | installed in Windows | — | Approved Tool List for Windows!C13 |
| Python 3 | Latest 3.x — confirm exact version before install | installed in WSL | Libraries may be added freely EXCEPT any AI/ML-related library (e.g. no LLM, machine-learning, or generative-AI frameworks).  | Approved Tool List for Windows!C14 |
| uv | Latest | installed in WSL | Same rule as Python 3 — any library OK except AI/ML-related packages | Approved Tool List for Windows!C15 |
| gdb | Latest (distro package) | installed in WSL | — | Approved Tool List for Windows!C16 |
| objdump | Bundled with GNU Binutils | installed in WSL | — | Approved Tool List for Windows!C17 |
| strings | Bundled with GNU Binutils | installed in WSL | — | Approved Tool List for Windows!C18 |
| zsteg | Latest (Ruby gem) | installed in WSL | — | Approved Tool List for Windows!C19 |
| binwalk | Latest | installed in WSL | — | Approved Tool List for Windows!C20 |
| ExifTool | Latest | installed in WSL | — | Approved Tool List for Windows!C21 |
| pdftotext (Poppler utils) | Latest | installed in WSL | — | Approved Tool List for Windows!C22 |
| can-utils | Latest | installed in WSL | — | Approved Tool List for Windows!C23 |
| cannelloni | Latest | installed in WSL | — | Approved Tool List for Windows!C24 |
| zeek | Latest | installed in WSL | — | Approved Tool List for Windows!C25 |
| ZBar | Latest | installed in WSL | — | Approved Tool List for Windows!C26 |
| Burp Suite Community Edition | 2026.4.x (confirm latest at install time) | installed in WSL | — | Approved Tool List for Windows!C27 |
| jq | Latest | installed in WSL | — | Approved Tool List for Windows!C28 |
| Ghidra | 12.1.4 | installed in WSL | — | Approved Tool List for Windows!C29 |
| The Sleuth Kit | Latest | installed in WSL | — | Approved Tool List for Windows!C30 |
| OpenSSL | Latest 3.x | installed in WSL | — | Approved Tool List for Windows!C31 |
| xz | Latest | installed in WSL | — | Approved Tool List for Windows!C32 |
| qpdf | Latest | installed in WSL | — | Approved Tool List for Windows!C33 |
| llvm-mc (LLVM tools) | Latest | installed in WSL | — | Approved Tool List for Windows!C34 |
| xxd | Bundled with Vim | installed in WSL | — | Approved Tool List for Windows!C35 |
| fsck.fat (dosfstools) | Latest | installed in WSL | — | Approved Tool List for Windows!C36 |
| RsaCtfTool | Latest (GitHub script, run via Python 3) | installed in WSL | — | Approved Tool List for Windows!C37 |
| volatility3 | Latest | installed in WSL | — | Approved Tool List for Windows!C38 |
| OpenSSH-Session-Key-Recovery | — | installed in volatility3 | Plugin for Volatility3 | Approved Tool List for Windows!C39 |
| x64dbg | Latest | installed in Windows | Portable zip (snapshot_*.zip). Extract and run; no installer. | Approved Tool List for Windows!C40 |
| Autopsy | Latest | installed in Windows | MSI installer (bundles Java and The Sleuth Kit). Administrator rights required. | Approved Tool List for Windows!C41 |
| HxD | Latest | installed in Windows | Installer or portable edition. | Approved Tool List for Windows!C42 |
| tshark | Latest | installed in Windows | Included in the Wireshark installer (TShark component). | Approved Tool List for Windows!C43 |
| Notepad++ | Latest | installed in Windows | Installer (x64). A portable edition is also available. | Approved Tool List for Windows!C44 |
| dnSpyEx (dnSpy) | Latest | installed in Windows | Portable zip. Use dnSpy-net-win64.zip (self-contained; no .NET installation needed). | Approved Tool List for Windows!C45 |
| Eric Zimmerman's Tools | Latest | installed in Windows | Run Get-ZimmermanTools.ps1 to download the tools. Internet access and the .NET Desktop Runtime are required. | Approved Tool List for Windows!C46 |

## Kali · 161 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| .NET SDK | 6.0.400 | — | — | Approved Tool List for Kali!C8 |
| 7-Zip (7z) | 26.02 | — | — | Approved Tool List for Kali!C9 |
| aircrack-ng | 1.7 | — | — | Approved Tool List for Kali!C10 |
| ALEAPP (Android Logs Events And Protobuf Parser) | - | — | No installation information recorded | Approved Tool List for Kali!C11 |
| Android Studio | - | — | No installation information recorded | Approved Tool List for Kali!C12 |
| angr | (not captured) | pipx (angr) | — | Approved Tool List for Kali!C13 |
| AperiSolve | (not captured) | git (/opt/tools/AperiSolve) | — | Approved Tool List for Kali!C14 |
| Apktool | 2.7.0-dirty | — | — | Approved Tool List for Kali!C15 |
| asar (@electron/asar) | 4.3.1 | — | — | Approved Tool List for Kali!C16 |
| Audacity | (not captured) | /usr/bin/audacity | — | Approved Tool List for Kali!C17 |
| AutoIt-Ripper | (not captured) | pipx (autoit-ripper) | — | Approved Tool List for Kali!C18 |
| BinDiff | 8 | — | Build @568181968 (Sep 25 2023) | Approved Tool List for Kali!C19 |
| bkcrack | 1.8.1 (2025-10-25) | — | — | Approved Tool List for Kali!C20 |
| bulk_extractor | 2.1.1 | — | — | Approved Tool List for Kali!C21 |
| bvi | (not captured) | — | Interactive tool; the version check returned 'Input is not from a terminal' | Approved Tool List for Kali!C22 |
| Bytecode Viewer | 2.13.2 | Fat Jar | — | Approved Tool List for Kali!C23 |
| bzip2 | 1.0.8 | — | — | Approved Tool List for Kali!C24 |
| cabextract | 1.11 | — | — | Approved Tool List for Kali!C25 |
| capa | 9.4.0 | — | — | Approved Tool List for Kali!C26 |
| Chainsaw | 2.16.5 | — | — | Approved Tool List for Kali!C27 |
| checksec | 2.6.0 | — | — | Approved Tool List for Kali!C28 |
| crypto-attacks | (not captured) | git (/opt/tools/crypto-attacks) | — | Approved Tool List for Kali!C29 |
| curl | 8.21.0 | — | — | Approved Tool List for Kali!C30 |
| Cutter | (not captured) | AppImage (/opt/tools/cutter.AppImage) | The GUI needs FUSE | Approved Tool List for Kali!C31 |
| DB Browser for SQLite | 3.13.1 | — | — | Approved Tool List for Kali!C32 |
| DBeaver Community Edition | 26.1.3 | — | — | Approved Tool List for Kali!C33 |
| Detect It Easy (DIE) | 3.21 | — | — | Approved Tool List for Kali!C34 |
| dex2jar | 2.1-nightly-28 | — | — | Approved Tool List for Kali!C35 |
| Didier Stevens Beta tools (onedump.py) | (not captured) | git (/opt/tools/Beta) | — | Approved Tool List for Kali!C36 |
| Didier Stevens Suite (pdfid.py, pdf-parser.py, oledump.py and others) | (not captured) | git (/opt/tools/DidierStevensSuite) | — | Approved Tool List for Kali!C37 |
| Docker Engine and Compose plugin | 28.5.2+dfsg4 | — | — | Approved Tool List for Kali!C38 |
| dwarf2json | 0.9.0 | — | — | Approved Tool List for Kali!C39 |
| Eclipse Temurin JDK (OpenJDK) | 25.0.4 (2026-07-21) | — | Reported as 'openjdk' | Approved Tool List for Kali!C40 |
| ewf-tools (libewf) | 20140816 | — | — | Approved Tool List for Kali!C41 |
| Exploit-DB / searchsploit (offline archive) | 2026-08-19 | — | Version is the archive date | Approved Tool List for Kali!C42 |
| factordb-python | (not captured) | pip (factordb-python) | — | Approved Tool List for Kali!C43 |
| FakeNet-NG | (not captured) | /opt/tools/flare-fakenet-ng (fakenet in PATH) | — | Approved Tool List for Kali!C44 |
| Fernflower | (not captured) | /opt/tools/fernflower/build/libs/fernflower.jar (/usr/local/bin/fernflower) | — | Approved Tool List for Kali!C45 |
| Feroxbuster | 2.13.1 | — | — | Approved Tool List for Kali!C46 |
| FFmpeg | (not captured) | apt (ffmpeg) | — | Approved Tool List for Kali!C47 |
| ffuf | 2.1.0-dev | — | — | Approved Tool List for Kali!C48 |
| file (libmagic) | 5.47 | — | — | Approved Tool List for Kali!C49 |
| FLOSS (FLARE Obfuscated String Solver) | (not captured) | pipx (flare-floss) | — | Approved Tool List for Kali!C50 |
| foremost | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C51 |
| FQLite | (not captured) | /opt/fqlite/bin/fqlite (symlinked to /usr/local/bin) | — | Approved Tool List for Kali!C52 |
| Frida | 17.23.3 | — | — | Approved Tool List for Kali!C53 |
| GCC, G++ and build tools (build-essential, make, CMake, pkg-config) | 15.3.0 | — | Debian gcc 15.3.0-2 | Approved Tool List for Kali!C54 |
| GEF (GDB Enhanced Features) | (not captured) | /opt/tools/gef.py | Load with: gdb -x /opt/tools/gef.py. Not auto-sourced, to avoid a clash with peda | Approved Tool List for Kali!C55 |
| Git | 2.53.0 | — | — | Approved Tool List for Kali!C56 |
| Gitleaks | (not captured) | — | The tool does not report a version (set at build time) | Approved Tool List for Kali!C57 |
| G'MIC (gmic) | (not captured) | — | Version not captured (the command started the G'MIC interpreter) | Approved Tool List for Kali!C58 |
| GNU Wget | 1.25.0 | — | — | Approved Tool List for Kali!C59 |
| Go | 1.26.5 | — | — | Approved Tool List for Kali!C60 |
| Gobuster | 3.8.2 | — | — | Approved Tool List for Kali!C61 |
| GoReSym | (not captured) | go install (github.com/mandiant/GoReSym@latest) | — | Approved Tool List for Kali!C62 |
| GTFOBins (offline copy) | (not captured) | git (/opt/tools/GTFOBins.github.io) | — | Approved Tool List for Kali!C63 |
| gzip | 1.13 | — | — | Approved Tool List for Kali!C64 |
| HackTricks (offline copy) | (not captured) | git (/opt/tools/hacktricks) | — | Approved Tool List for Kali!C65 |
| hashcat | 7.1.2 | — | — | Approved Tool List for Kali!C66 |
| hashid | 3.1.4 | — | — | Approved Tool List for Kali!C67 |
| Hayabusa | (not captured) | — | Version not captured (the --version option is not supported) | Approved Tool List for Kali!C68 |
| hcxtools | 7.1.2 | — | Version of hcxpcapngtool | Approved Tool List for Kali!C69 |
| Hindsight (pyhindsight) | (not captured) | pipx (pyhindsight) | — | Approved Tool List for Kali!C70 |
| hlextend | (not captured) | Python module (/usr/local/lib/python3.14/dist-packages/hlextend.py) | — | Approved Tool List for Kali!C71 |
| Hydra | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C72 |
| iLEAPP (iOS Logs, Events, And Plists Parser) | - | — | No installation information recorded | Approved Tool List for Kali!C73 |
| ImageMagick | 7.1.2-27 | — | — | Approved Tool List for Kali!C74 |
| Impacket | 0.14.0 | — | — | Approved Tool List for Kali!C75 |
| innoextract | dev build | — | — | Approved Tool List for Kali!C76 |
| internet_detector | (not captured) | apt (inetsim) | Provided by the apt package 'inetsim' | Approved Tool List for Kali!C77 |
| IPython | 9.17.1 | — | — | Approved Tool List for Kali!C78 |
| jadx (jadx-gui) | 1.5.6 | — | — | Approved Tool List for Kali!C79 |
| John the Ripper (jumbo) | 1.9.0-Jumbo-1 | — | — | Approved Tool List for Kali!C80 |
| Jpeginfo | 1.7.1 | — | — | Approved Tool List for Kali!C81 |
| js-beautify | 2.0.3 | — | — | Approved Tool List for Kali!C82 |
| js-deobfuscator | (not captured) | npm (js-deobfuscator) | — | Approved Tool List for Kali!C83 |
| jwt_tool | (not captured) | /opt/tools/jwt_tool (/usr/local/bin/jwt_tool) | — | Approved Tool List for Kali!C84 |
| Katana | (not captured) | go install (github.com/projectdiscovery/katana/cmd/katana@latest) | — | Approved Tool List for Kali!C85 |
| legion | 0.7.0 | — | — | Approved Tool List for Kali!C86 |
| libesedb tools | 20240420 | — | Version of esedbexport | Approved Tool List for Kali!C87 |
| LibreOffice | 26.8.0.3 | — | — | Approved Tool List for Kali!C88 |
| lrzip | 0.660 | — | — | Approved Tool List for Kali!C89 |
| ltrace | 0.7.91 | — | — | Approved Tool List for Kali!C90 |
| lz4 | 1.10.0 | — | — | Approved Tool List for Kali!C91 |
| lzip | 1.26 | — | — | Approved Tool List for Kali!C92 |
| mac_apt | (not captured) | git (/opt/tools/mac_apt) | — | Approved Tool List for Kali!C93 |
| MediaInfo | (not captured) | — | Version not captured | Approved Tool List for Kali!C94 |
| Metasploit Framework | 6.5.2-dev | — | — | Approved Tool List for Kali!C95 |
| mimikatz | 2.2.0 | Wine (Windows binary) | — | Approved Tool List for Kali!C96 |
| Miniforge3 (conda) | (not captured) | /home/kali/miniforge3 | — | Approved Tool List for Kali!C97 |
| multimon-ng | (not captured) | apt (multimon-ng) | — | Approved Tool List for Kali!C98 |
| mupdf-tools (mutool) | 1.27.0 | — | — | Approved Tool List for Kali!C99 |
| NASM (Netwide Assembler) | 3.01 | — | — | Approved Tool List for Kali!C100 |
| Nmap (with Ncat / Nping) | 7.99 | — | — | Approved Tool List for Kali!C101 |
| Node.js (with npm) | 24.21.0 | — | — | Approved Tool List for Kali!C102 |
| obfuscator-io-deobfuscator | 1.0.6 | — | — | Approved Tool List for Kali!C103 |
| Obsidian | (not captured) | — | Version not captured; startup reported that ~/.config/obsidian/obsidian.json does not exist | Approved Tool List for Kali!C104 |
| oletools (full suite: olevba, oleid, oleobj, rtfobj, mraptor, msodde, olemeta, oletimes, pyxswf) | (not captured) | pipx (oletools) | — | Approved Tool List for Kali!C105 |
| OllyDbg | 1.10-1kali5 | Wine (Windows binary) | — | Approved Tool List for Kali!C106 |
| OpenStego | (not captured) | GitHub .deb package | — | Approved Tool List for Kali!C107 |
| padding-oracle-attacker | (not captured) | — | Version not captured (the command printed a banner only) | Approved Tool List for Kali!C108 |
| PARI/GP | 2.17.4 | — | — | Approved Tool List for Kali!C109 |
| PayloadsAllTheThings (offline copy) | (not captured) | git (/opt/tools/PayloadsAllTheThings) | — | Approved Tool List for Kali!C110 |
| peda | (not captured) | /opt/tools/peda (sourced in ~/.gdbinit) | — | Approved Tool List for Kali!C111 |
| peepdf-3 | (not captured) | pipx (peepdf-3) | — | Approved Tool List for Kali!C112 |
| pff-tools (libpff) | 20231205 | — | Version of pffexport | Approved Tool List for Kali!C113 |
| Plaso (log2timeline, psort, pinfo) | 20260119-1kali1 | — | — | Approved Tool List for Kali!C114 |
| pngcheck | (not captured) | apt (pngcheck) | — | Approved Tool List for Kali!C115 |
| pwndbg | (not captured) | /opt/tools/pwndbg | setup.sh completed | Approved Tool List for Kali!C116 |
| pycdc (Decompyle++) | (not captured) | — | Version not captured (no --version option) | Approved Tool List for Kali!C117 |
| pyinstxtractor-ng | (not captured) | pipx (pyinstxtractor-ng) | — | Approved Tool List for Kali!C118 |
| pypykatz | 0.6.13 | — | — | Approved Tool List for Kali!C119 |
| Python 2.7 | 2.7.18 | — | — | Approved Tool List for Kali!C120 |
| Python 3.11 (via uv) | - | — | No installation information recorded | Approved Tool List for Kali!C121 |
| qemu-img (qemu-utils) | 11.0.3 | — | — | Approved Tool List for Kali!C122 |
| radare2 | 6.0.5 | — | — | Approved Tool List for Kali!C123 |
| rat-king-parser | 4.2.4 | — | — | Approved Tool List for Kali!C124 |
| RegRipper | 3.0 | — | — | Approved Tool List for Kali!C125 |
| ripgrep (rg) | 15.2.0 | — | — | Approved Tool List for Kali!C126 |
| rockyou.txt (Kali 'wordlists' package) | (not captured) | /usr/share/wordlists/rockyou.txt | — | Approved Tool List for Kali!C127 |
| ROPgadget | 7.7 | — | — | Approved Tool List for Kali!C128 |
| rtptools (rtpdump, rtpplay and others) | (not captured) | /opt/tools/rtptools | Built from source | Approved Tool List for Kali!C129 |
| Rust (rustup, rustc, cargo) | 1.95.0 (2026-04-14) | — | Built from a source tarball | Approved Tool List for Kali!C130 |
| rustscan | 2.4.1 | — | — | Approved Tool List for Kali!C131 |
| SageMath | - | — | No installation information recorded | Approved Tool List for Kali!C132 |
| SecLists | (not captured) | /usr/bin/seclists | — | Approved Tool List for Kali!C133 |
| socat | 1.8.1.3 | — | — | Approved Tool List for Kali!C134 |
| Sonic Visualiser | 5.2.1 | — | — | Approved Tool List for Kali!C135 |
| SoX (Sound eXchange) | 14.7.1.2 | — | SoX_ng build | Approved Tool List for Kali!C136 |
| SQLCipher Community Edition — CLI | SQLite 3.53.4 / SQLCipher 4.18.0 | — | — | Approved Tool List for Kali!C137 |
| sqlite3 | 3.53.4 | — | — | Approved Tool List for Kali!C138 |
| sqlmap | 1.10.8 (stable) | — | — | Approved Tool List for Kali!C139 |
| sstv (command-line SSTV decoder) | (not captured) | pip (PySSTV) | — | Approved Tool List for Kali!C140 |
| steghide | 0.6.0 | — | — | Approved Tool List for Kali!C141 |
| stegseek | 0.6 | — | — | Approved Tool List for Kali!C142 |
| stegsnow (SNOW) | (not captured) | apt (stegsnow) | — | Approved Tool List for Kali!C143 |
| StegSolve | (not captured) | — | Version not captured (GUI tool; it was started without a display) | Approved Tool List for Kali!C144 |
| strace | 7.0 | — | — | Approved Tool List for Kali!C145 |
| Subfinder | 2.16.0 | — | — | Approved Tool List for Kali!C146 |
| Sublime Text | Build 4215 | — | — | Approved Tool List for Kali!C147 |
| tar | 1.35 | — | — | Approved Tool List for Kali!C148 |
| tcpdump | 4.99.6 | — | — | Approved Tool List for Kali!C149 |
| TestDisk and PhotoRec | 7.2 | — | — | Approved Tool List for Kali!C150 |
| unar | 1.10.8 | — | — | Approved Tool List for Kali!C151 |
| uncompyle6 | 3.9.3 | — | — | Approved Tool List for Kali!C152 |
| unpyc3 (unpyc37-3.10) | (not captured) | git (/opt/tools/unpyc3) | — | Approved Tool List for Kali!C153 |
| unrar | (not captured) | /usr/bin/unrar | — | Approved Tool List for Kali!C154 |
| unzip | 6.0-30 | — | — | Approved Tool List for Kali!C155 |
| UPX | 4.2.4 | — | — | Approved Tool List for Kali!C156 |
| Visual Studio Code | 1.141.2 | — | — | Approved Tool List for Kali!C157 |
| Volatility 2 | (not captured) | git (/opt/tools/volatility) | — | Approved Tool List for Kali!C158 |
| Volatility 2 community plugins | (not captured) | git (/opt/tools/community) | — | Approved Tool List for Kali!C159 |
| Volatility 2 profiles (Linux and macOS) | (not captured) | git (/opt/tools/profiles) | — | Approved Tool List for Kali!C160 |
| Volatility 3 community plugins (community3) | (not captured) | git (/opt/tools/community3) | — | Approved Tool List for Kali!C161 |
| VS Code extension: C/C++ (ms-vscode.cpptools) | (not captured) | VS Code extension (ms-vscode.cpptools) | — | Approved Tool List for Kali!C162 |
| VS Code extension: Python (ms-python.python) | (not captured) | VS Code extension (ms-python.python) | — | Approved Tool List for Kali!C163 |
| YARA | 4.5.8 | — | — | Approved Tool List for Kali!C164 |
| yara-python (and YARA on Linux) | (not captured) | pip (yara-python) | — | Approved Tool List for Kali!C165 |
| zip | (not captured) | — | Installed; version not captured | Approved Tool List for Kali!C166 |
| zstd | 1.5.7 | — | — | Approved Tool List for Kali!C167 |
| Zui (formerly Brim) | (not captured) | — | Version not captured (the command only printed a startup message) | Approved Tool List for Kali!C168 |

## Not approved · 82 entries

| Tool | Version | Installation/location | Notes/reason | Workbook source |
| --- | --- | --- | --- | --- |
| API Monitor | — | — | The challenges can be solved without it. | Unapproved List!B6 |
| Arsenal Image Mounter (Free Mode) | — | — | Alternative tools are available. | Unapproved List!B7 |
| Binary Ninja (Free) | — | — | Cannot be supported in the provided environment. | Unapproved List!B8 |
| BlobRunner (32-bit and 64-bit) | — | — | The challenges can be solved without it. | Unapproved List!B9 |
| Build Tools for Visual Studio 2026 (C++ workload) | — | — | Alternative tools are available. | Unapproved List!B10 |
| capa Explorer Web | — | — | The challenges can be solved without it. | Unapproved List!B11 |
| Cmder | — | — | Alternative tools are available. | Unapproved List!B12 |
| CodeTrack | — | — | The challenges can be solved without it. | Unapproved List!B13 |
| Copy As Python-Requests (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B14 |
| CryptoTester | — | — | License or source cannot be verified. | Unapproved List!B15 |
| Cygwin | — | — | Alternative tools are available. | Unapproved List!B16 |
| DCT-Image-Steganography | — | — | Not permitted under the competition rules. | Unapproved List!B17 |
| de4dot (de4dot-cex build) | — | — | Cannot be supported in the provided environment. | Unapproved List!B18 |
| Decompiler.com | — | — | Not permitted under the competition rules. | Unapproved List!B19 |
| Dirsearch | — | — | Cannot be supported in the provided environment. | Unapproved List!B20 |
| Dissect (Fox-IT DFIR framework) | — | — | Cannot be supported in the provided environment. | Unapproved List!B21 |
| dll_to_exe | — | — | The challenges can be solved without it. | Unapproved List!B22 |
| dnlib | — | — | The challenges can be solved without it. | Unapproved List!B23 |
| DotDumper | — | — | The challenges can be solved without it. | Unapproved List!B24 |
| Exeinfo PE | — | — | The challenges can be solved without it. | Unapproved List!B25 |
| FdSig | — | — | License or source cannot be verified. | Unapproved List!B26 |
| Fiddler Classic | — | — | Requires a commercial license. | Unapproved List!B27 |
| GarbageMan and psnotify | — | — | The challenges can be solved without it. | Unapproved List!B28 |
| GoStringUngarbler | — | — | The challenges can be solved without it. | Unapproved List!B29 |
| GraphQL Raider (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B30 |
| Hackvertor (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B31 |
| HashMyFiles | — | — | The challenges can be solved without it. | Unapproved List!B32 |
| HollowsHunter | — | — | The challenges can be solved without it. | Unapproved List!B33 |
| IDA Free | — | — | Cannot be supported in the provided environment. | Unapproved List!B34 |
| IDR (Interactive Delphi Reconstructor) | — | — | The challenges can be solved without it. | Unapproved List!B35 |
| IFPSTools.NET (ifpsdasm) | — | — | The challenges can be solved without it. | Unapproved List!B36 |
| ImHex | — | — | Cannot be supported in the provided environment. | Unapproved List!B37 |
| Inno Setup Decompiler | — | — | License or source cannot be verified. | Unapproved List!B38 |
| innounp | — | — | The challenges can be solved without it. | Unapproved List!B39 |
| JWT Editor (Burp Suite extension) | — | — | Cannot be supported in the provided environment. | Unapproved List!B40 |
| Kernel OST Viewer (free) | — | — | The challenges can be solved without it. | Unapproved List!B41 |
| magiceye-solver | — | — | Cannot be supported in the provided environment. | Unapproved List!B42 |
| Malcode Analyst Pack (MAP) | — | — | The challenges can be solved without it. | Unapproved List!B43 |
| malware-jail | — | — | The challenges can be solved without it. | Unapproved List!B44 |
| MemProcFS | — | — | Cannot be supported in the provided environment. | Unapproved List!B45 |
| MMSSTV | — | — | Cannot be supported in the provided environment. | Unapproved List!B46 |
| MobSF | — | — | Cannot be supported in the provided environment. | Unapproved List!B47 |
| NETReactorSlayer | — | — | The challenges can be solved without it. | Unapproved List!B48 |
| OffVis | — | — | The challenges can be solved without it. | Unapproved List!B49 |
| OneNoteAnalyzer | — | — | The challenges can be solved without it. | Unapproved List!B50 |
| Online analysis services (VirusTotal, CrackStation, etc.) | — | — | Not permitted under the competition rules. | Unapproved List!B51 |
| Online decompilers and compilers (websites - nothing to install) | — | — | Not permitted under the competition rules. | Unapproved List!B52 |
| PDBReSym | — | — | The challenges can be solved without it. | Unapproved List!B53 |
| PDFStreamDumper | — | — | Alternative tools are available. | Unapproved List!B54 |
| PE-sieve | — | — | The challenges can be solved without it. | Unapproved List!B55 |
| pe_unmapper | — | — | The challenges can be solved without it. | Unapproved List!B56 |
| PEiD | — | — | License or source cannot be verified. | Unapproved List!B57 |
| Photocraft | — | — | License or source cannot be verified. | Unapproved List!B58 |
| pkg-unpacker | — | — | The challenges can be solved without it. | Unapproved List!B59 |
| ProcDOT | — | — | The challenges can be solved without it. | Unapproved List!B60 |
| Process Dump (pd32 / pd64) | — | — | The challenges can be solved without it. | Unapproved List!B61 |
| Process Monitor | — | — | Alternative tools are available. | Unapproved List!B62 |
| PST Walker | — | — | Requires a commercial license. | Unapproved List!B63 |
| pylingual | — | — | Cannot be supported in the provided environment. | Unapproved List!B64 |
| Recaf | — | — | Cannot be supported in the provided environment. | Unapproved List!B65 |
| reg_export | — | — | The challenges can be solved without it. | Unapproved List!B66 |
| Regshot | — | — | The challenges can be solved without it. | Unapproved List!B67 |
| RunDotNetDll | — | — | The challenges can be solved without it. | Unapproved List!B68 |
| RX-SSTV | — | — | Cannot be supported in the provided environment. | Unapproved List!B69 |
| scdbg (with GUI) | — | — | The challenges can be solved without it. | Unapproved List!B70 |
| SCLauncher (32-bit and 64-bit) | — | — | The challenges can be solved without it. | Unapproved List!B71 |
| Scylla / x64dbg plugins | — | — | Alternative tools are available. | Unapproved List!B72 |
| sfextract (SingleFileExtractor) | — | — | The challenges can be solved without it. | Unapproved List!B73 |
| shellcode_launcher | — | — | The challenges can be solved without it. | Unapproved List!B74 |
| sigBits | — | — | Cannot be supported in the provided environment. | Unapproved List!B75 |
| stegdetect | — | — | Cannot be supported in the provided environment. | Unapproved List!B76 |
| SysTools SQLite Viewer (free edition) | — | — | Requires a commercial license. | Unapproved List!B77 |
| Time Travel Debugging (TTD) | — | — | The challenges can be solved without it. | Unapproved List!B78 |
| TweakPNG | — | — | Cannot be supported in the provided environment. | Unapproved List!B79 |
| Universal Extractor 2 (UniExtract2) | — | — | The challenges can be solved without it. | Unapproved List!B80 |
| VBDec | — | — | The challenges can be solved without it. | Unapproved List!B81 |
| Volatility 3 symbol tables (windows/linux/mac zip) | — | — | Cannot be supported in the provided environment. | Unapproved List!B82 |
| VS Code extension: WSL (ms-vscode-remote.remote-wsl) | — | — | The challenges can be solved without it. | Unapproved List!B83 |
| WinDbg | — | — | Alternative tools are available. | Unapproved List!B84 |
| Windows Terminal | — | — | Alternative tools are available. | Unapproved List!B85 |
| WinDump (for Npcap) | — | — | Alternative tools are available. | Unapproved List!B86 |
| YAFU (Yet Another Factoring Utility) | — | — | Cannot be supported in the provided environment. | Unapproved List!B87 |

