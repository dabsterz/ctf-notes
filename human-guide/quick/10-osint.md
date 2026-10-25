# OSINT

Set `FILE`/`DIR` to supplied evidence. Run Bash in the stated environment. [Full reference](../reference/chapters/10-osint.md) · [Tool chooser](../TOOL-CHOOSER.md#osint). Record URLs, timestamps and independent confirmation.

## Quick: extract metadata and coordinates

**WSL · ExifTool.** Input: original supplied media.

```bash
FILE='clue.jpg'
exiftool -a -G1 -s "$FILE"
exiftool -n -GPSLatitude -GPSLongitude -GPSLatitudeRef -GPSLongitudeRef -DateTimeOriginal -OffsetTimeOriginal "$FILE"
```

**Look for:** GPS, camera model, software, timezone and comments.
**If not:** use visible signs/buildings; stripped metadata is common and metadata can be edited.

## Quick: search a supplied PDF

**WSL · pdftotext / Python 3.** Input: PDF; writes a text copy.

```bash
FILE='clue.pdf'
pdftotext -layout "$FILE" clue-text.txt
python3 - <<'PY'
from pathlib import Path
text = Path('clue-text.txt').read_text(errors='replace')
print(text[:12000])
PY
```

**Look for:** names, exact phrases, dates and footnote URLs.
**If not:** Windows PDF Viewer → Open → zoom the scanned page and transcribe distinctive text.

## Quick: search saved pages and exports

**Kali · ripgrep.** Input: directory of supplied HTML/JSON/text exports.

```bash
DIR='supplied'
rg -n -i 'application/ld\+json|author|datePublished|dateModified|identifier|canonical' "$DIR"
rg -n -o 'https?://[^"<>[:space:]]+' "$DIR"
```

**Look for:** stable IDs, original media URLs, aliases and publication claims.
**If not:** inspect scripts/application state; a crawl timestamp is not a publication timestamp.

## Quick: expose invisible Unicode

**WSL · Python 3.** Input: UTF-8 text copied without normalization.

```bash
FILE='message.txt'
python3 - "$FILE" <<'PY'
import sys, unicodedata
from pathlib import Path
text = Path(sys.argv[1]).read_text(encoding='utf-8')
for i, ch in enumerate(text):
    if not ch.isascii() or not ch.isprintable():
        print(i, f'U+{ord(ch):04X}', unicodedata.name(ch, 'UNNAMED'), repr(ch))
tags = ''.join(chr(ord(c)-0xE0000) for c in text if 0xE0020 <= ord(c) <= 0xE007E)
print('Unicode tag characters:', repr(tags))
PY
```

**Look for:** tag characters, zero-width symbols or lookalike letters.
**If not:** compare original spelling and context; arbitrary Unicode does not imply an encoding.

## Quick: search the web with a specific clue

**Windows · Chrome.** Use ordinary permitted text searches; substitute a phrase transcribed from the artifact. Example search syntax:

```text
"North Pier Clock" "1998"
"North Pier Clock" site:gov.uk
"North Pier Clock" filetype:pdf
```

Chrome → address bar → enter the query → open original source → record URL/date. For a location, compare road layout, sign text and building shape on permitted maps; keep camera position separate from the pictured landmark.

**Look for:** two independent details matching one candidate.
**If not:** remove one uncertain word or translate visible text; do not upload the image to an analysis service.

## Quick: save a designated page or RDAP response

**Kali · curl.** Put the exact organizer-designated HTTPS URL on one line in `assigned-url.txt`; for RDAP, use the supplied RDAP lookup URL. This performs one request and does not follow redirects. [curl options](https://curl.se/docs/manpage.html).

```bash
URL=$(cat assigned-url.txt)
curl --proto '=https' --max-time 20 --silent --show-error \
  --dump-header response-headers.txt --output response-body.txt "$URL"
```

**Look for:** status, redirect location, linked identifiers and registration events.
**If not:** read the error/status before repeating; shared hosting/registrars do not prove common ownership.

## Quick: inspect DNS and registration exports

**Kali · ripgrep.** Input: supplied zone, DNS, WHOIS or RDAP exports under `infrastructure`. `dig` and `whois` are not listed in this workbook; use saved evidence or the approved curl route above.

```bash
DIR='infrastructure'
rg -n -i '\b(TXT|CNAME|MX|NS|SOA|registrar|nameserver|registration|expiration|eventDate)\b' "$DIR"
```

**Look for:** TXT fragments, aliases and dated changes.
**If not:** request the challenge's supplied records; do not infer ownership from a shared IP.

## Quick: inspect a supplied Git history

**Kali · Git.** Input: local repository containing `.git`.

```bash
DIR='repo'
git -C "$DIR" log --all --format='%H %aI %an <%ae> %cn <%ce>'
git -C "$DIR" log --all --diff-filter=D --name-status
git -C "$DIR" log --all -p -- '*.txt' '*.md' '.mailmap'
git -C "$DIR" remote -v
```

**Look for:** deleted clues, changing aliases and repository URLs; `remote -v` only reads configuration.
**If not:** an exported/shallow copy may lack history. Author fields are user-controlled; corroborate them.
