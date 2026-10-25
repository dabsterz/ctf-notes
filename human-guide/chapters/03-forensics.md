# Disk, memory, and host forensics

**Quick route:** [Short commands](../QUICKSTART.md#duplicate-tar-files) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#forensics). Use this chapter for deeper explanations.

Recover the smallest artifact that answers the question, then explain where it came from. A file name, a timestamp, and a matching hash are more useful than a directory full of unexplained carvings.

## Choose the right machine

Workbook references below use **Windows** for `Approved Tool List for Windows`, **Kali** for `Approved Tool List for Kali`, and **Unapproved** for `Unapproved List`.

| Environment | Available route | Workbook evidence |
|---|---|---|
| Windows native | Autopsy, HxD, Eric Zimmerman's tools; PowerShell built-ins | Windows rows 41, 42, 46 |
| Windows WSL | Python 3, strings, Sleuth Kit, xz, Volatility 3 | Windows rows 14, 18, 30, 32, 38 |
| Kali | EWF tools, qemu-img, TestDisk/PhotoRec, foremost, SQLite, Git, Volatility 2 | Kali rows 41, 122, 150, 51, 138, 56, 158 |

Commands marked **WSL** run in its Linux shell, not PowerShell. A Windows listing does not establish a Kali installation. Python snippets use WSL Python; the PDF permits non-AI libraries in both environments, subject to [named exclusions and package setup](00-tool-rules.md#non-ai-python-package-checks).

The event prohibits AI tools and public analysis uploads. Keep evidence local and act only on challenge endpoints. See the [competition rules](https://ajccbc.ncsa.or.th/cyber-sea-game-2026/).

## Preserve a baseline

Use this before extraction. `evidence.img` means the challenge-supplied image; `work` and `out` are new local directories.

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Path work,out
Copy-Item -LiteralPath .\evidence.img -Destination .\work\evidence.img
Get-FileHash -Algorithm SHA256 -LiteralPath .\evidence.img
Get-FileHash -Algorithm SHA256 -LiteralPath .\work\evidence.img
Get-Item -LiteralPath .\evidence.img | Select-Object Name,Length,LastWriteTimeUtc
```

The hashes should match. Record the original size and hash in your notes. The download's modification time is not necessarily the suspect's file timestamp.

**WSL, quick identification:**

```bash
xxd -l 128 work/evidence.img
strings -a -n 8 work/evidence.img > out/strings-ascii.txt
strings -a -e l -n 8 work/evidence.img > out/strings-utf16.txt
```

Search these text files in your editor. On Kali, `file work/evidence.img` is available (Kali row 49). A suffix such as `.dmp` does not distinguish full physical memory from a single-process minidump; inspect the signature before selecting a parser.

## Partition offsets and targeted recovery

**Use when:** the input is a raw disk or partition image. Sleuth Kit avoids mounting and journal replay. Run these in **WSL** (Windows row 30).

```bash
mmls work/evidence.img
```

Read the units printed above the table. Set `START` to the filesystem's start sector, not its byte offset. `SECTOR` is the image's sector size; 512 is an example, not a universal value. A partition-only image generally uses `START=0`.

```bash
START=2048
SECTOR=512
fsstat -b "$SECTOR" -o "$START" work/evidence.img > out/fsstat.txt
fls -b "$SECTOR" -o "$START" -r -p work/evidence.img > out/files.txt
fls -b "$SECTOR" -o "$START" -r -d -p work/evidence.img > out/deleted.txt
```

Choose an address printed by `fls`; `42` below is a placeholder. NTFS addresses can include attribute type and ID, for example `66-128-4`.

```bash
ADDR=42
istat -b "$SECTOR" -o "$START" work/evidence.img "$ADDR" > out/inode.txt
icat -b "$SECTOR" -o "$START" work/evidence.img "$ADDR" > out/recovered.bin
xxd -l 64 out/recovered.bin
```

Expected result: recovered bytes match the file's format and declared length. For a deleted FAT file, the directory entry may survive while the FAT cluster chain has been cleared. Contiguous recovery can work; fragmented recovery may require carving or extent reconstruction. A deleted name is not a promise that its contents survive.

If `fsstat` rejects the image, check offset units, sector size, compression/container format, and filesystem support before assuming corruption. `fls` puts a colon after every address; searching for `:` alone does **not** reliably identify alternate streams.

## Missing partitions, carving, and virtual disks

**Kali** (rows 150, 51, 122, 41):

```bash
testdisk /log work/evidence.img
photorec /log /d out/carved work/evidence.img
foremost -i work/evidence.img -o out/foremost
qemu-img info --backing-chain disk.vmdk
qemu-img convert -f vmdk -O raw disk.vmdk out/disk.raw
ewfinfo disk.E01
```

In TestDisk, use **Analyse**, then **Quick Search** and file listing/copying. Do not select **Write** on the evidence. Carve into a separate output directory. File carving loses original paths, timestamps, and often fragmented data; it complements filesystem recovery.

For VMDK, provide all split extents and backing snapshots in their expected relative paths. Converting only a delta file without its parent gives incomplete or incorrect results. OVA is a tar container; on Kali use `tar -tf machine.ova` before extracting selected members. A VM snapshot can contain separate `.vmem` and state files; retain both, and try the supported memory parser before assuming a converter is available.

Sparse VMDK fallback: read the header's sector-based grain size, grain-directory offset, and entries-per-table. A directory entry points to a grain table; a table entry points to a physical grain. Translate virtual sector to grain index and in-grain offset; zero entries represent unallocated grains. Do not concatenate sparse extents as if they were raw sectors.

## A reusable extent and byte-transform extractor

**WSL Python standard library.** Save as `carve.py`. Use when a verified filesystem record or format header gives a byte offset and length. This handles large inputs without loading the whole disk.

```python
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('image')
p.add_argument('output')
p.add_argument('offset', type=lambda x: int(x, 0))
p.add_argument('length', type=lambda x: int(x, 0))
p.add_argument('--stride', type=int, default=1)
p.add_argument('--phase', type=int, default=0)
a = p.parse_args()
assert a.offset >= 0 and a.length >= 0
assert a.stride > 0 and 0 <= a.phase < a.stride
assert a.offset + a.length <= Path(a.image).stat().st_size
with open(a.image, 'rb') as src, open(a.output, 'xb') as dst:
    src.seek(a.offset)
    remaining, consumed = a.length, 0
    while remaining:
        block = src.read(min(1024 * 1024, remaining))
        if not block:
            raise EOFError('short read')
        first = (a.phase - consumed) % a.stride
        dst.write(block[first::a.stride])
        remaining -= len(block)
        consumed += len(block)
```

```bash
python3 carve.py work/evidence.img out/extent.bin 0x400000 0x10000
python3 carve.py out/extent.bin out/even.bin 0 65536 --stride 2 --phase 0
python3 carve.py out/extent.bin out/odd.bin 0 65536 --stride 2 --phase 1
```

Null interleaving often makes every second byte zero and doubles the apparent size. Check both phases and validate the result with a parser. For fragmented files, extract each verified extent in **logical file order**, insert sparse holes where specified, and trim to the recorded file size.

XFS extent fields are packed and include allocation-group addressing: a filesystem block value cannot always be multiplied directly by block size without decoding the AG component. HFS+ resource forks have their own extents and logical size; examine both forks. ISO 9660 directory records contain extent LBA and data length; the usual logical block size is 2048, but read the volume descriptor. These are parsing workflows, not permission to install missing filesystem tools.

## Archives: list, test, then recover

**Kali:** `7z` row 9, `tar` row 148, `unzip` row 155, `bkcrack` row 20, John row 80. **WSL:** Python row 14 and xz row 32.

```bash
7z l archive.zip
7z t archive.zip
tar -tvf archive.tar.xz
unzip -l document.docx
```

OOXML documents are ZIPs: inspect `word/media/`, `xl/worksheets/`, embedded objects, and relationships. Do not enable macros.

### Keep duplicate tar members

For repeated tar names, standard extraction overwrites earlier versions. The [ready-to-run extractor](../QUICKSTART.md#duplicate-tar-files) accepts your archive filename, preserves every occurrence and prints previews. The following teaching example shows how it works in **WSL Python**; save it as `tar_versions.py`, replace `archive.tar.xz` with your filename and run `python3 tar_versions.py`:

```python
import tarfile
from pathlib import Path

out = Path('out/tar-members')
out.mkdir(parents=True, exist_ok=True)
total = 0
with tarfile.open('archive.tar.xz') as tf:
    for i, member in enumerate(tf):
        if not member.isfile():
            continue
        total += member.size
        if member.size > 64_000_000 or total > 512_000_000:
            raise ValueError('extraction budget exceeded')
        src = tf.extractfile(member)
        assert src is not None
        data = src.read(member.size + 1)
        assert len(data) == member.size
        (out / f'{i:06d}.bin').write_bytes(data)
        print(i, repr(member.name), member.size)
```

For nested archives, record each layer's input/output hash and stop when the format no longer matches. Limit depth and output size. A `.model` beside many compressed files can indicate dictionary compression such as FemtoZip; the dictionary is required and the original source's installer is not event-approved. Preserve the model and inspect supplied decompressor source rather than guessing a normal ZIP decoder.

ZIP repair must respect both local headers and central-directory records. Local filename length is at header `+26`; central-directory filename length at `+28`. Verify filename and extra-field boundaries before changing a copy. Bit 3 means sizes may appear in a later data descriptor, so a generic local-header parser cannot trust zero size fields. CRC32 and uncompressed size should match after recovery.

For an XZ file whose 12-byte header alone is damaged, the last footer can supply stream flags. **WSL**, save as `repair_xz.py`:

```python
from pathlib import Path
import struct, zlib

d = bytearray(Path('broken.xz').read_bytes())
assert len(d) >= 24 and d[-2:] == b'YZ'
footer = d[-12:]
assert zlib.crc32(footer[4:10]) == int.from_bytes(footer[:4], 'little')
flags = bytes(footer[8:10])
d[:12] = b'\xfd7zXZ\0' + flags + struct.pack('<I', zlib.crc32(flags))
Path('out/repaired.xz').write_bytes(d)
```

```bash
python3 repair_xz.py
xz -t out/repaired.xz
xz -dc out/repaired.xz > out/decompressed.bin
```

This assumes one stream with no trailing stream padding; account for padding or concatenated streams first. A valid footer does not prove the body is intact.

ZipCrypto known-plaintext attack, **Kali**, with an unencrypted reference ZIP containing the same compressed member:

```bash
bkcrack -C secret.zip -c report.txt -P known.zip -p report.txt
```

It needs at least 12 known plaintext bytes, including 8 contiguous bytes, at the encryption layer. For a compressed member, a file's uncompressed PNG magic alone is not enough. This does not apply to WinZip AES.

Replace `K0 K1 K2` with the three hexadecimal keys printed by the successful attack. Create a separate archive with a chosen local password, test it, then extract into a new directory. This assumes its members share the recovered original password. The `-U` operation is documented in the [official bkcrack usage](https://github.com/kimci86/bkcrack#change-password).

```bash
bkcrack -C secret.zip -k K0 K1 K2 -U out/unlocked.zip RecoveredOnly
7z t out/unlocked.zip -pRecoveredOnly
7z x out/unlocked.zip -pRecoveredOnly -oout/unlocked
```

If the original password was recovered independently, skip key recovery and use `7z t secret.zip` followed by `7z x secret.zip -oout/unlocked`; enter that password at the prompt. A CRC failure after unlocking suggests wrong plaintext alignment, a different member password, or damaged archive data.

## Memory: establish what the dump supports

**WSL Volatility 3**, Windows row 38:

```bash
vol --help
vol --offline -f memory.dmp windows.info
vol --offline -f memory.dmp windows.pslist
vol --offline -f memory.dmp windows.pstree
vol --offline -f memory.dmp windows.cmdline
vol --offline -f memory.dmp windows.netscan
vol --offline -f memory.dmp windows.filescan > out/filescan.txt
```

Use the installed plugin names printed by help; names can be versioned. `--offline` prevents automatic symbol retrieval. The symbol ZIP bundles are explicitly unavailable (**Unapproved row 82**). Existing matching symbols may or may not be present. An unsatisfied symbol requirement is an environment limitation, not proof the dump is empty. Keep the diagnostic and pivot to raw bytes or supported supplied profiles.

Choose a PID and address from the results; these values are examples:

```bash
PID=1234
PHYS=0x12345000
vol --offline -f memory.dmp -o out windows.memmap --pid "$PID" --dump
vol --offline -f memory.dmp -o out windows.dumpfiles --physaddr "$PHYS"
vol --offline -f memory.dmp windows.mftscan
```

Search recovered process bytes in ASCII and UTF-16LE. A process dump can be a virtual-address mapping, not a complete runnable executable. Match suspicious parentage, command line, network endpoints, and mapped regions before selecting a process.

**Kali Volatility 2** (rows 158–160) is a separate path for matching legacy profiles. Use `python2 /opt/tools/volatility/vol.py --info` to inspect available profiles/plugins. Run `imageinfo`, then validate the proposed profile using plausible process names and timestamps. `clipboard`, `consoles`, and `mftparser` are legacy plugin routes; do not translate their flags directly into Volatility 3 commands.

```bash
python2 /opt/tools/volatility/vol.py -f memory.raw imageinfo
PROFILE=Win7SP1x64
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" pslist
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" clipboard
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" consoles
python2 /opt/tools/volatility/vol.py -f memory.raw --profile="$PROFILE" mftparser > out/mft-memory.txt
```

`Win7SP1x64` is an example, not a default to force on every dump. Use a compatible profile that the installation actually lists. Empty clipboard output may mean unavailable pages or an unsupported OS artifact; it does not prove nothing was copied.

For an ELF core, **WSL GDB** (Windows row 16):

```bash
gdb -nx -nh -c core.dump
```

```text
info files
info proc mappings
info registers
x/32gx $sp
find 0x400000, 0x410000, "flag{"
dump binary memory out/region.bin 0x400000 0x410000
quit
```

Replace both addresses with a mapped region from this core. A universal 32-bit search range misses 64-bit heaps. GDB opens the core for analysis; do not run a recovered executable to inspect its strings.

## Keys, framebuffers, and unusual memory remnants

For ransomware, identify the cipher, key length, IV location, padding, and file layout from the recovered program. An AES key may remain near path strings or a configuration structure. Restrict candidates to those regions and test against **two independent known file signatures**. A successful authentication tag is much stronger evidence than printable plaintext. A timestamp-derived key search must reproduce the exact PRNG implementation and seed units; Python's random generator is not interchangeable with C, Ruby, or .NET PRNGs.

Full-disk encryption keys may appear as expanded AES schedules, but the source's key-finder and volume-mounting tools are not listed. Do not modify encryption headers or add passwords to evidence. Record key candidates and use only a supported approved decoder for the challenge format.

For possible screen remnants, render a bounded region as pixels. **WSL**, Pillow is a non-AI library under Windows row 14:

```python
from PIL import Image

offset, width, height = 0x100000, 1024, 256  # set from evidence/hypothesis
with open('memory.dmp', 'rb') as f:
    f.seek(offset)
    raw = f.read(width * height * 4)
assert len(raw) == width * height * 4
Image.frombytes('RGB', (width, height), raw, 'raw', 'BGRX').save('out/screen.png')
```

Try documented RGB/BGR/BGRA layouts and row stride; recognizable fragments can be partial or stale. In a minidump, file offsets differ from process virtual addresses. Parse its memory descriptors before translating an address into a file slice.

## Windows artifact timeline

**Windows native**, built-in PowerShell, on an exported EVTX file:

```powershell
Get-WinEvent -Path .\Security.evtx -Oldest |
  Where-Object { $_.Id -in 1102,4624,4688,4720,4726,4781 } |
  Select-Object TimeCreated,Id,ProviderName,Message |
  Export-Csv -NoTypeInformation -Encoding UTF8 .\out\security.csv
```

Missing message resources can produce blank descriptions. Export `ToXml()` to retain named event fields and UTC `SystemTime`. Event IDs are provider-specific: Security 1102 is audit clearing; 4720 account creation; 4781 account rename. RDP authentication event 1149 belongs to RemoteConnectionManager; LocalSessionManager 21/24/25 describe logon/disconnect/reconnect. Authentication success alone does not prove an interactive desktop was used.

**Security event 4688 records process creation.** `NewProcessName` identifies the executable; `CommandLine` contains arguments when command-line auditing captured them. Some JSON exports rename that field `ProcessCommandLine`. XML `SystemTime` ending in `Z` is UTC. A blank command line does not prove there were no arguments, and this event alone does not establish successful execution, malicious intent or payload effects. Use the [process-event quick card](../QUICKSTART.md#process-event) for a named-field extraction command. [Microsoft field definitions](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688).

Zimmerman tools are approved on **Windows row 46**. From their installed directory:

```powershell
.\MFTECmd.exe -f 'C:\case\$MFT' --csv C:\case\out
.\PECmd.exe -d C:\case\Prefetch --csv C:\case\out
.\AmcacheParser.exe -f C:\case\Amcache.hve --csv C:\case\out
.\EvtxECmd.exe -f C:\case\Security.evtx --csv C:\case\out
```

Replace `C:\case` with your evidence-copy directory. Confirm each executable's help if a version changes output flags. Amcache indicates file inventory/presence and may support an activity timeline; it is not by itself proof of execution. Prefetch run times require context. `$MFT` does not record the name of the process that created a file.

| Artifact | What to inspect | Next correlation |
|---|---|---|
| `$MFT` | Resident data, names, SI/FN timestamp differences | USN, logs, file contents |
| `$Extend\$UsnJrnl:$J` | Create/delete/rename/data-extension reasons | MFT reference + sequence number |
| `$Recycle.Bin\SID` | Pair `$I` metadata with matching `$R` content | Original path and deletion time |
| `NTUSER.DAT` | Run keys, MRU, user application settings | Process and file evidence |
| `SYSTEM` + `SAM` | Computer config, user/RID records | Account events; challenge hash task |
| `ConsoleHost_history.txt` | Typed PowerShell command text | Script-block/process events |
| Defender `Support\MPLog-*` | Detection, quarantine, ASR activity | DetectionHistory and file hashes |
| WMI `Repository\OBJECTS.DATA` | Consumer commands and filter/binding strings | WMI and process events |

USN writes can be coalesced; they do not assign an exact execution timestamp to each history line. Registry last-write time is a key modification time, not always account creation. SI/FN disagreement suggests a question to investigate, not automatic proof of timestomping. `EFSTMPWP` can indicate a free-space wipe attempt; it does not prove every free cluster was overwritten.

For ADS on an extracted NTFS file, **Windows native**:

```powershell
Get-Item -LiteralPath .\suspect.txt -Stream *
Get-Content -LiteralPath .\suspect.txt -Stream Zone.Identifier
```

For image-level ADS, examine `istat`'s named `$DATA` attributes and extract the complete `inode-type-id` address with `icat`. Copying a file to a filesystem without ADS support may discard the extra streams.

**Kali** SAM hash extraction (Impacket row 75), only from challenge-provided hives:

```bash
impacket-secretsdump -sam SAM -system SYSTEM LOCAL > out/sam-hashes.txt
```

This is offline extraction. Do not reuse recovered credentials against services outside the challenge.

## Browser, SQLite, Android, and Linux evidence

Work on a copied database alongside its `-wal` and `-shm` files. The WAL may hold the newest or deleted material. Opening only the main database can miss it. **Kali SQLite**, row 138:

```bash
sqlite3 -readonly History '.tables'
sqlite3 -readonly History '.schema urls'
sqlite3 -readonly History "SELECT url,title,datetime(last_visit_time/1000000-11644473600,'unixepoch') FROM urls ORDER BY last_visit_time;"
sqlite3 -readonly places.sqlite "SELECT url,title,datetime(last_visit_date/1000000,'unixepoch') FROM moz_places ORDER BY last_visit_date;"
```

Chrome uses microseconds since 1601; Firefox places uses microseconds since 1970. Schema differs by browser version. Password ciphertext is not decryptable merely because `Local State` exists: older `v10/v11` AES-GCM records require the actual master key; newer app-bound formats need their own supported recovery route. Verify authentication tags.

For supplied Android app directories, inspect `shared_prefs/*.xml`, `databases/*`, and backups before APK reversal. ALEAPP/iLEAPP are listed on Kali rows 11/73 but have no recorded installation information: do not promise they run. On Linux, correlate exported `auth.log`, shell history, service logs, cron definitions, and binaries. Shell history may lack timestamps or omit noninteractive commands.

SQLite edit-history tables can retain text removed later. After inspecting the actual schema, replay operations and inspect every intermediate state:

```python
import sqlite3
db = sqlite3.connect('file:notes.db?mode=ro', uri=True)
text = ''
for ident, op, pos, value in db.execute(
        'SELECT id,type,position,text FROM diffs ORDER BY id'):
    assert isinstance(pos, int) and 0 <= pos <= len(text)
    if op == 'insert':
        text = text[:pos] + value + text[pos:]
    elif op == 'remove':
        assert text[pos:pos + len(value)] == value
        text = text[:pos] + text[pos + len(value):]
    else:
        raise ValueError(op)
    if 'flag{' in text.lower():
        print(ident, repr(text))
```

Positions might be UTF-16 code units or bytes instead of Python characters; use the application's convention. For raw SQLite differences, decode record-header varints: serial types 0–9 have special meanings; even types ≥12 are blobs of `(type-12)/2` bytes, odd types ≥13 are text of `(type-13)/2` bytes. Changed type bytes can change interpretation without changing the visible payload.

## Git and container history

**Kali Git**, row 56, on a supplied local repository:

```bash
git -C recovered log --all --format=fuller --stat
git -C recovered reflog --all
git -C recovered fsck --full --unreachable --no-reflogs
git -C recovered show COMMIT:path/to/file
```

Replace `COMMIT` with an object ID printed by the earlier commands. `git log --all` excludes dangling commits; inspect the IDs from `fsck` explicitly. Recover deleted `.git/objects/xx/...` files with `icat` first and preserve their paths. Do not run garbage collection. For a corrupted loose object, decompress zlib and hash the full `type size\0content` record; matching the expected object ID validates a single-byte repair. If the repository uses SHA-256, do not assume SHA-1.

For a Docker save archive, inspect `manifest.json`, its config's `history`, and every layer tar in order. OCI archives instead use `index.json` and content-addressed descriptors. Whiteouts (`.wh.name`, `.wh..wh..opq`) remove earlier content from the final view but leave earlier layer bytes recoverable. Build history is useful but does not necessarily retain every command or secret after squashing/metadata changes. The tar extraction script above works without starting containers.

## Advanced filesystem cases: know the limits

| Pattern | Usable local approach | Validation and limitation |
|---|---|---|
| GPT GUID payload | Read LBA size and GPT header; entry-array LBA at `+72`, count `+80`, entry size `+84`; concatenate unique-GUID bytes at entry `+16` | Check header/table CRCs; GUID text representation changes byte order |
| FAT free space | Derive cluster size, rounded root-directory sectors, and data start from BPB; read clusters whose FAT entry is zero | Bound by data-region cluster count; preserve physical offsets instead of silently joining fragments |
| RAID 5 missing member | XOR corresponding bytes from all surviving aligned members | Equal sizes/offsets required; recovered member is not the logical array; stripe order and parity rotation still matter |
| APFS/Btrfs/ZFS snapshots | Identify historical roots and transaction/generation IDs; compare same file across roots | Installed TSK support varies; raw `APSB` hits are candidates, not valid snapshot proof |
| Damaged ZFS metadata | Preserve copies of labels/nvlists; validate block pointers and checksums before reconstruction | Fletcher4 uses 64-bit accumulators over 32-bit input words; source's 32-bit version was wrong |
| Kyoto Cabinet key damage | Record table slots/value offsets; reproduce the documented hash mapping with candidate keys | First binary difference is often a header/counter, not the target slot; no approved manager assumed |
| BSON chunk documents | Validate each 32-bit LE document length and trailing NUL; decode with non-AI `pymongo` in WSL | Sort by explicit chunk index, reject gaps/duplicates, then base64-decode |
| KeePass | Identify KDBX version/KDF, inspect installed John's extractor support | Never label all KDBX4/Argon2 material as a single hashcat mode |

For aligned equal-size RAID members, this **WSL** script creates the missing physical member in bounded chunks:

```python
from pathlib import Path
assert Path('disk1.img').stat().st_size == Path('disk3.img').stat().st_size
with open('disk1.img','rb') as a, open('disk3.img','rb') as b, open('out/disk2.img','xb') as out:
    while x := a.read(1024 * 1024):
        y = b.read(len(x))
        assert len(x) == len(y)
        out.write(bytes(i ^ j for i, j in zip(x, y)))
```

Do not create a live RAID array or run repair tools on the evidence. Filesystem repairs can overwrite the very orphaned records you want. Use supported read-only extraction, then a separate expendable copy if a justified repair path is available.

## Finish with a reproducible result

Record the input hash, partition/stream offset, inode or process ID, exact command, output hash, and the evidence supporting the answer. Keep observations separate from interpretations. A copied flag-shaped string can be a decoy; verify its relationship to the challenge question.

Source material adapted: `ctf-forensics/SKILL.md`, `disk-and-memory.md`, `disk-advanced.md`, `disk-recovery.md`, `linux-forensics.md`, and `windows.md` within `ctf-forensics/`. Network, media, and malware overlaps continue in the neighboring chapters. Historical installers, cloud CLI enumeration, unsupported snapshot mounters, and collision-generator recipes were removed from the competition workflow.
