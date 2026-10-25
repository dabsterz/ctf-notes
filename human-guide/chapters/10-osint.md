# OSINT

Set `FILE`/`DIR` to supplied evidence. Run Bash in the stated environment. [Full reference](#full-reference) · [Tool chooser](../TOOL-CHOOSER.md#osint). Record URLs, timestamps and independent confirmation.

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

## Full reference

<details class="deep-reference" markdown="1">
<summary>Explanations, advanced cases and sources</summary>

# OSINT from supplied evidence

**Quick route:** [Short commands](../QUICKSTART.md#osint) · [Tool strengths and weaknesses](../TOOL-CHOOSER.md#osint). Use this chapter for deeper explanations.

Build an evidence trail from a clue to an answer. Preserve exact identifiers, original text, dates, and uncertainty. A matching username, reused photograph, or hosting IP is a lead; it does not independently establish identity or location.

Manual Google searches, technical references and Google Translate are explicitly allowed by PDF p.6. Work from supplied clues and corroborate public evidence. Do not upload challenge images to reverse-image services, use face recognition or ask outsiders/bots for assistance. [Reference and communication rules](../COMPETITION.md#what-is-allowed).

## Environment and local inventory

**Windows native:** Chrome and a PDF viewer, Windows workbook rows 12 and 10. **WSL:** Python 3, ExifTool, pdftotext, strings (Windows rows 14, 21, 22, 18). **Kali:** Git, ripgrep, ImageMagick, SQLite, MediaInfo (Kali rows 56, 126, 74, 138, 94). Keep those environments distinct; a Kali tool is not automatically installed in WSL.

Use a notebook or CSV with these columns:

```text
clue_id,source_file,source_offset_or_page,observation,hypothesis,confidence,next_check
```

Example observation: “profile-export.json contains account ID 123 and display name Harbor.” Hypothesis: “Harbor is the account's current alias.” The number is more stable than a display name, but exported metadata can still be fabricated.

**Kali**, search a supplied evidence directory without contacting its links:

```bash
rg -n -i 'username|handle|author|identifier|location|latitude|longitude' evidence
rg -n -i 'https?://|mailto:|t\.me/|github\.com/' evidence
```

**WSL**, inspect media metadata and PDF text:

```bash
exiftool -a -u -g1 evidence/photo.jpg
exiftool -GPSLatitude -GPSLongitude -GPSLatitudeRef -GPSLongitudeRef -n evidence/photo.jpg
pdftotext -layout evidence/document.pdf document.txt
strings -a -n 6 evidence/blob.bin > blob-strings.txt
```

Expected result: concrete coordinates, timestamps, embedded names, document titles, or linked identifiers. Metadata can be edited or stripped; absence is not proof of deception. Do not assume every social platform always removes every metadata field.

## Parse saved pages and JSON

Saved HTML may include richer JSON-LD or application state than the visible page. In Chrome, open a **copy** only if its active-content behavior is understood; otherwise read as text. Search for `application/ld+json`, `author`, `identifier`, `content`, and media URLs. Keep archived fetch date separate from the page's claimed publication date.

This **WSL standard-library** script extracts link targets and script blocks from a local saved page. It does not fetch them. Save as `page_extract.py`:

```python
from html.parser import HTMLParser
from pathlib import Path

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.blocks=[]; self.current=None
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        for key in ('href','src'):
            if key in attrs: self.links.append((tag,key,attrs[key]))
        if tag=='script': self.current=[attrs.get('type',''),[]]
    def handle_data(self,data):
        if self.current is not None: self.current[1].append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.current is not None:
            self.blocks.append(self.current); self.current=None

p=Page(); p.feed(Path('page.html').read_text(encoding='utf-8',errors='replace'))
for item in p.links: print(item)
out=Path('page-scripts'); out.mkdir(exist_ok=True)
for i,(kind,chunks) in enumerate(p.blocks):
    (out/f'{i:03d}.txt').write_text(''.join(chunks),encoding='utf-8')
    print(i,kind)
```

Read extracted JSON with `python3 -m json.tool page-scripts/000.txt` when that block is actual JSON. JavaScript assignments are not JSON; extract the value deliberately rather than executing the block. An HTTP 200 status can be a login wall or generic “not found” page; compare body content and stable identifiers.

## Aliases, social exports, and timestamps

In supplied profile exports, correlate numeric IDs, explicit cross-links, avatar history, post IDs, and dates. Same handles on different platforms are not identity proof. Numeric suffixes could be postal codes, years, random numbers, or deliberate misdirection; test alternatives against independent evidence.

For a Twitter-style Snowflake **known to use that scheme**, decode its creation timestamp locally:

```python
from datetime import datetime,timezone
snowflake=1234567890123456789  # replace with the observed numeric ID
milliseconds=(snowflake>>22)+1288834974657
print(datetime.fromtimestamp(milliseconds/1000,timezone.utc).isoformat())
```

Discord uses a different epoch; other services use entirely different ID schemes. A calculated timestamp does not prove an account belongs to a person. Retain the original identifier alongside the derived time.

For saved social-media datasets, inspect all supplied posts/replies, bios, playlist descriptions, role names, emoji frames, and image variants. Short-duration GIF frames can hide text; use the steganography chapter's animation workflow. Preserve playlist/album order when testing acrostics. For gaming data, include realm/server and character IDs; a character name without server context is ambiguous.

A supplied fitness route can identify a **challenge location** from its path and landmarks. Do not infer or expose a real person's home from privacy-zone boundaries. Use the exact endpoint/waypoint requested by the challenge, and distinguish a route from the camera position.

## Unicode and encoded clues

Before normalizing text, list its codepoints. Homoglyph encodings often mix Latin and Cyrillic lookalikes, but emoji, accents, and smart punctuation are not automatically secret bits. **WSL:**

```python
from pathlib import Path
import unicodedata
text=Path('post.txt').read_text(encoding='utf-8')
for i,c in enumerate(text):
    print(i,repr(c),f'U+{ord(c):04X}',unicodedata.name(c,'CONTROL'))
pairs={'a':'\u0430','e':'\u0435','o':'\u043e','p':'\u0440','c':'\u0441','x':'\u0445'}
zeros=set(pairs); ones=set(pairs.values())
bits=''.join('0' if c in zeros else '1' for c in text if c in zeros|ones)
for shift in range(8):
    b=bits[shift:]
    data=bytes(int(b[i:i+8],2) for i in range(0,len(b)-7,8))
    print(shift,repr(data))
```

The explicit alphabet is a hypothesis; change it only with evidence. Whole-text ASCII/non-ASCII encoding is a different scheme and includes spaces/punctuation differently. Record the choice so someone else can reproduce it.

For a Base58 clue, preserve leading `1` characters as leading zero bytes:

```python
from pathlib import Path
alphabet='123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
s=Path('base58.txt').read_text().strip()
number=0
for ch in s: number=number*58+alphabet.index(ch)
zeroes=len(s)-len(s.lstrip('1'))
decoded=b'\0'*zeroes+number.to_bytes((number.bit_length()+7)//8,'big')
print(repr(decoded))
```

Validate a Base58Check checksum when the format requires one. Strings of 32/40/64 hexadecimal characters can be MD5/SHA-1/SHA-256, but may also be random IDs, Tor fingerprints, keys, or data. Length is a classification clue, not a definitive algorithm detector.

## Geolocation without image uploads

Make an observation sheet before choosing a country: readable sign fragments, writing systems, road numbers, driving side, rail crossings, building layout, terrain, coastline, shadows, and unique small objects. Generic architecture and vegetation should carry low confidence. A Cyrillic sign does not uniquely identify Russia, and motorway sign colors vary by road class; the source's one-feature country table was too strong.

**Kali ImageMagick**, row 74, makes local inspection copies:

```bash
magick photo.jpg -crop 600x300+120+80 +repage -resize 200% sign.png
magick sign.png -flop mirrored-sign.png
magick sign.png -colorspace Gray -auto-level contrast-sign.png
```

The crop is `width×height+x+y`; measure it on the image. `-flop` mirrors horizontally. Use nearest-neighbor scaling for pixel grids; ordinary photo inspection can use other interpolation. Preserve the original and record transformations. Do not invent illegible letters; keep alternate readings in the notes.

Compare candidate photographs/maps already supplied by the organizer. Verify at least two independent scene constraints: building alignment plus road geometry, or sign plus coastline. For exact viewpoint tasks, match camera position using foreground poles, paths, bollards, and the relative alignment of distant buildings. The subject's coordinate can differ substantially from the camera's.

For newspaper or product clues, use supplied catalogs/archives: record publication date, page number, headline, model number, voltage/capacity, and dimensions. A matching brand without the exact model is insufficient. For a series of music landmarks, solve locations first, then assemble the per-image key numbers in the specified order; do not adjust uncertain locations merely to force readable ASCII.

## Coordinates and local spatial checks

Latitude/longitude order and hemisphere signs are frequent errors. Decimal degrees are not degrees-minutes-seconds. An MGRS string includes zone, latitude band, grid square, and equally precise easting/northing digits; do not treat it as a decimal coordinate. A short Plus Code needs a reference locality; a full Open Location Code does not. What3Words is a distinct system and cannot be converted using a guessed word grid.

For non-AI Python libraries, PDF p.5 permits additions in either environment subject to named exclusions; use a documented coordinate conversion library only after checking its input/output convention. Do not assume public conversion websites are an approved analysis route. If the required proprietary lookup is unavailable, preserve the verified coordinates and state the conversion dependency.

For a supplied `places.csv` with `name,lat,lon`, this **WSL** script ranks locations near a clue coordinate using a spherical distance:

```python
import csv,math
latitude,longitude=13.7563,100.5018  # replace with clue coordinates
def distance(lat,lon):
    a,b=map(math.radians,(latitude,lat))
    dlat=b-a; dlon=math.radians(lon-longitude)
    h=math.sin(dlat/2)**2+math.cos(a)*math.cos(b)*math.sin(dlon/2)**2
    return 6371000*2*math.asin(min(1,math.sqrt(h)))
rows=[]
with open('places.csv',newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        rows.append((distance(float(row['lat']),float(row['lon'])),row['name']))
for metres,name in sorted(rows)[:20]: print(round(metres,1),name)
```

Expected result: a candidate list, not a final match. Ten metres may be smaller than the map's coordinate error. For a supplied OSM JSON export, filter `elements[].tags` for `shop`, `amenity`, `railway`, and `tourism`, then compare proximity locally. Ways may need geometry/centroids; a node-only export can omit the desired business entirely.

## DNS, registration, archives, and infrastructure

Start with supplied DNS captures, zone files, WHOIS/RDAP exports, certificate records, or archive indexes. Extract TXT/CNAME/MX records and preserve answer timestamps/TTL. TXT records can consist of multiple strings within one record: join those in order, but do not merge independent answers arbitrarily.

A stored archive index can reveal old URLs and date ranges; an archived snapshot's timestamp is the crawl time, not the original publication time. Compare saved old/new pages for changed aliases and links. For saved Google Docs/Sheets exports, preserve document IDs and sheet IDs; a private-access response is not a puzzle to bypass.

Registrars, shared name servers, shared IPs, and ASNs are infrastructure correlations, not ownership proof. IP geolocation may point to a provider, VPN, or coarse regional estimate. A reused SSH host key or certificate can indicate a reused image/configuration rather than one physical server. Tor relay fingerprint/family data in a supplied export can support chronology, but does not identify a user.

Active DNS queries, zone transfers, service fingerprinting, and scanning belong only to a challenge-designated target and the permitted tools for that machine. This offline chapter does not turn a public hostname found in evidence into an attack target. Do not copy the historical cross-challenge infrastructure-pivot advice into event practice.

## Repository and file-metadata pivots

**Kali Git**, row 56, on a supplied local repository:

```bash
git -C repo log --all --format='%H %aI %an <%ae> %cn <%ce>'
git -C repo log --all --diff-filter=D --name-status
git -C repo log --all -p -- '*.private' '*.key' '*.txt'
git -C repo show COMMIT:path/to/file
```

Replace `COMMIT` with an observed ID. Examine `.mailmap`, README links, contributors, commit messages, and supplied issue/review exports. Author/committer fields are user-controlled; most Git history is not cryptographically signed. Even a valid signature needs a trusted key-to-identity link.

For a supplied `.DS_Store`, inspect filenames with a permitted local non-AI parser in WSL; Finder metadata indicates names seen in a directory, not contents or necessarily current files. Do not recursively fetch discovered paths from unrelated sites. For TTF remapping clues, a non-AI `fontTools` script can inspect cmap and glyph contours locally; contour matching works best against the exact reference font and normalization, not any arbitrary standard font.

## Finish the chain

For each answer component, record the source, exact observation, transformation, and independent confirmation. Keep rejected hypotheses too when they explain ambiguity. A final location should state whether it is a building, camera point, route waypoint, or coordinate grid cell, with the requested precision.

Source material adapted: all five files in `ctf-osint/`. Agent automation, paid/API-key services, public image uploads, face recognition, credentialed Discord enumeration, live bot interaction, invasive location inference, and cross-challenge pivots were excluded. Their underlying local evidence-reading methods are retained where useful.

</details>
