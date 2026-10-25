# Network captures

[Tool placement and competition rules](00-tool-rules.md). All commands read supplied captures offline. Enter observed paths, stream numbers and filters when prompted.

## Quick: find the interesting conversation

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
& $tshark -n -r $file -q -z io,phs
& $tshark -n -r $file -q -z conv,tcp
& $tshark -n -r $file -q -z conv,udp
& $tshark -n -r $file -q -z endpoints,ip
```

**Windows · Wireshark:** File → Open → capture; Statistics → Protocol Hierarchy, then Conversations. Select a TCP row → Follow Stream.

**Look for:** unusual protocols, byte-heavy flows and endpoint pairs.
**If not:** inspect other interfaces and UDP conversations.

## Quick: list HTTP requests and export files

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
$out = Read-Host 'New HTTP export directory'
New-Item -ItemType Directory -Path $out | Out-Null
& $tshark -n -r $file -Y http.request -T fields -E header=y `
  -e frame.number -e tcp.stream -e http.request.method -e http.host -e http.request.uri
& $tshark -n -r $file --export-objects "http,$out"
```

**Look for:** downloads, POST bodies, filenames and configuration data.
**If not:** uploads may require Follow → TCP Stream; export objects does not recover every upload.

## Quick: recover one TCP stream

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
$stream = Read-Host 'Observed TCP stream number'
& $tshark -n -r $file -q -z "follow,tcp,ascii,$stream"
& $tshark -n -r $file -Y "tcp.stream == $stream && tcp.len > 0" `
  -T fields -E header=y -E 'separator=,' -E quote=d `
  -e frame.number -e ip.src -e tcp.seq_raw -e tcp.len -e tcp.payload |
  Set-Content -Encoding ascii .\segments.csv
```

**Windows · Wireshark:** filter `tcp.stream == 3` using your stream number → select packet → Follow → TCP Stream → choose one direction → Show data as Raw → Save as.

**Look for:** complete application framing and consistent sequence ranges.
**If not:** check gaps/retransmissions; concatenating packet payloads is not reassembly.

## Quick: decrypt TLS using supplied secrets

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
$keys = Read-Host 'Supplied NSS keylog path'
$out = Read-Host 'New decrypted HTTP output directory'
New-Item -ItemType Directory -Path $out | Out-Null
& $tshark -n -r $file -o "tls.keylog_file:$keys" -Y http
& $tshark -n -r $file -o "tls.keylog_file:$keys" --export-objects "http,$out"
```

**Look for:** decoded HTTP and authenticated TLS records.
**If not:** match handshake/client random; RSA server keys cannot decrypt ECDHE or TLS 1.3.

## Quick: extract DNS and ICMP clues

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
& $tshark -n -r $file -Y 'dns.flags.response == 0' `
  -T fields -e frame.number -e dns.qry.name |
  Set-Content -Encoding ascii .\dns.tsv
& $tshark -n -r $file -Y 'icmp.type == 8' `
  -T fields -e frame.number -e icmp.ident -e icmp.seq -e data.data |
  Set-Content -Encoding ascii .\icmp.tsv
```

**Look for:** encoded labels, sequence fields, repeated lengths and unusual payloads.
**If not:** inspect timing and TXT answers; preserve ordering and distinguish retries.

## Quick: inspect authentication exchanges

**Windows · PowerShell / TShark**

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
& $tshark -n -r $file -Y ntlmssp -V |
  Set-Content -Encoding UTF8 .\ntlm-details.txt
& $tshark -n -r $file -Y 'smb2 || dcerpc || ntp || radius' -V |
  Set-Content -Encoding UTF8 .\auth-details.txt
```

**Look for:** usernames, domains and paired challenge/response messages.
**If not:** follow one exchange; do not mix different sessions or contact captured endpoints.

## Quick: make searchable protocol logs

**WSL · Zeek**

```bash
read -r -p 'Absolute capture path: ' FILE
read -r -p 'New log directory: ' OUT
mkdir "$OUT" && (cd "$OUT" && zeek -r "$FILE")
```

**Kali · tcpdump**, for a short packet view:

```bash
read -r -p 'Capture path: ' FILE
tcpdump -nn -r "$FILE" -c 30
tcpdump -nn -A -r "$FILE" -c 30 'tcp port 80'
```

**Look for:** `conn.log`, `dns.log`, `http.log`, endpoints and timestamps.
**If not:** inspect the packet-level stream; encrypted application content stays hidden.

## Quick: recover voice or keyboard evidence

**Windows · Wireshark:** Telephony → RTP → RTP Streams → select stream → Analyze / Play Streams → export audio. Check codec and sequence gaps.

**Windows · PowerShell / TShark**, after identifying the USB input device/endpoint:

```powershell
$tshark = 'C:\Program Files\Wireshark\tshark.exe'
$file = Read-Host 'Capture path'
$filter = Read-Host 'Display filter identifying the observed USB input endpoint'
& $tshark -n -r $file -Y "($filter) && usb.capdata" `
  -T fields -e frame.number -e usb.capdata |
  Set-Content -Encoding ascii .\hid.tsv
```

**Look for:** descriptor-defined reports; boot keyboards commonly use eight bytes.
**If not:** check report IDs/layout; use the full reference for UART, mouse and custom signal decoding.
