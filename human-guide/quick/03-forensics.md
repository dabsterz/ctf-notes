# Digital forensics

[Tool placement and competition rules](00-tool-rules.md). Enter paths when prompted; run `recipes/` commands from the extracted guide root.

## Quick: preserve the original

**Windows · PowerShell**

```powershell
$file = Read-Host 'Evidence file path'
$copy = Read-Host 'New working-copy path'
Copy-Item -LiteralPath $file -Destination $copy
Get-FileHash -Algorithm SHA256 -LiteralPath $file,$copy
Get-Item -LiteralPath $file | Select-Object Name,Length,LastWriteTimeUtc
```

**Look for:** matching SHA256 hashes.
**If not:** recopy before extracting; download timestamps are not incident timestamps.

## Quick: find the filesystem

**WSL · Sleuth Kit**

```bash
read -r -p 'Raw disk image path: ' FILE
mmls "$FILE"
read -r -p 'Filesystem start sector from mmls (partition-only: 0): ' START
read -r -p 'Sector size in bytes from image information: ' SECTOR
fsstat -b "$SECTOR" -o "$START" "$FILE"
fls -b "$SECTOR" -o "$START" -r -p "$FILE" > files.txt
fls -b "$SECTOR" -o "$START" -r -d -p "$FILE" > deleted.txt
```

**Look for:** filenames and metadata addresses in `files.txt` and `deleted.txt`.
**If not:** check sector units and container format before assuming corruption.

## Quick: recover one listed file

**WSL · Sleuth Kit**

```bash
read -r -p 'Raw disk image path: ' FILE
read -r -p 'Filesystem start sector: ' START
read -r -p 'Sector size in bytes: ' SECTOR
read -r -p 'Metadata address from fls, without trailing colon: ' ADDR
read -r -p 'New recovered-file path: ' OUT
istat -b "$SECTOR" -o "$START" "$FILE" "$ADDR"
icat -b "$SECTOR" -o "$START" "$FILE" "$ADDR" > "$OUT"
xxd -l 64 "$OUT"
```

**Look for:** expected signature, size and content.
**If not:** deleted fragmented data may need carving.

## Quick: browse or carve a disk

**Windows · Autopsy:** New Case → enter case name/location → Add Data Source → Disk Image or VM File → select image → choose relevant ingest modules → Finish. Browse File Views and Deleted Files; right-click a file → Extract File(s).

**Kali · PhotoRec**

```bash
read -r -p 'Disk image path: ' FILE
read -r -p 'New carving output directory: ' OUT
photorec /log /d "$OUT" "$FILE"
```

**Look for:** valid recovered files; retain the extraction source.
**If not:** carving cannot reliably restore fragmented files or original paths.

## Quick: identify a virtual disk container

**Kali · qemu-img** — keep split extents and backing snapshots together.

```bash
read -r -p 'VMDK descriptor path: ' FILE
qemu-img info --backing-chain "$FILE"
read -r -p 'New raw image output path: ' OUT
qemu-img convert -f vmdk -O raw "$FILE" "$OUT"
```

**Kali · EWF tools**, for E01 instead:

```bash
read -r -p 'First E01 segment path: ' FILE
ewfinfo "$FILE"
```

**Look for:** complete backing chain, format and sector information.
**If not:** locate missing extents before conversion.

## Quick: inspect archives and preserve duplicate members

**Kali · 7-Zip**

```bash
read -r -p 'Archive path: ' FILE
7z l "$FILE"
7z t "$FILE"
read -r -p 'New extraction directory: ' OUT
7z x "$FILE" "-o$OUT"
```

**WSL · Python**, for tar archives with repeated names:

```bash
read -r -p 'Tar archive path: ' FILE
read -r -p 'New output directory: ' OUT
python3 recipes/tar_keep.py "$FILE" --out "$OUT"
```

**Look for:** valid checksums; duplicate versions indexed in `manifest.jsonl`.
**If not:** inspect encryption or header damage in the full reference.

## Quick: inspect supplied memory

**WSL · Volatility 3**, with installed matching symbols:

```bash
read -r -p 'Memory dump path: ' FILE
vol --offline -f "$FILE" windows.info
vol --offline -f "$FILE" windows.pstree
vol --offline -f "$FILE" windows.cmdline
vol --offline -f "$FILE" windows.netscan
vol --offline -f "$FILE" windows.filescan > filescan.txt
```

**Look for:** suspicious parentage, arguments, endpoints and file objects.
**If not:** symbol failures are environment limitations; check `vol --help`, then inspect raw strings.

## Quick: build a Windows event timeline

**Windows · PowerShell**

```powershell
$file = Read-Host 'Exported EVTX path'
Get-WinEvent -Path $file -Oldest |
  Where-Object { $_.Id -in 1102,4624,4688,4720,4726,4781 } |
  Select-Object TimeCreated,Id,ProviderName,Message |
  Export-Csv -NoTypeInformation -Encoding UTF8 .\events.csv
```

For missing message resources, preserve named XML fields:

```powershell
$file = Read-Host 'Exported EVTX path'
Get-WinEvent -Path $file -Oldest |
  ForEach-Object { $_.ToXml() } |
  Set-Content -Encoding UTF8 .\events-xml.txt
```

**Look for:** 4688 `NewProcessName`/`CommandLine`; XML `SystemTime` is UTC.
**If not:** check the provider; blank arguments may mean auditing was disabled.

## Quick: inspect browser or app databases

**Kali · SQLite**

```bash
read -r -p 'SQLite database path: ' FILE
sqlite3 -readonly "$FILE" '.tables'
sqlite3 -readonly "$FILE" '.schema'
read -r -p 'Read-only SELECT query using the displayed schema: ' QUERY
sqlite3 -readonly -header -column "$FILE" "$QUERY"
```

**Look for:** URLs, downloads, timestamps and identifiers.
**If not:** retain matching WAL/SHM files; normal queries do not recover deleted rows.
