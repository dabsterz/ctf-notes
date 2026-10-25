"""Check PDF provenance, integration and known obsolete policy statements.

Semantic reconciliation is documented separately in environment-audit.md.
This checks the delivered artifacts; it does not contact event infrastructure.
"""
import hashlib
import json
from pathlib import Path
import re

from bs4 import BeautifulSoup
import fitz

ROOT = Path(__file__).resolve().parents[1]
original = ROOT.parent / 'Practice Environment Setup Guide.pdf'
copy = ROOT / 'sources/practice-environment.pdf'
assert original.read_bytes() == copy.read_bytes(), 'PDF copy differs from source'
digest = hashlib.sha256(original.read_bytes()).hexdigest()
with fitz.open(original) as pdf:
    assert len(pdf) == 23
    pages = [' '.join(page.get_text().split()) for page in pdf]
    assert 'From here: how to use the Practice Session' in pages[11]
    assert 'Scripts created before the competition' in pages[6]
    assert 'Standalone applications not on the approved list require organizer approval' in pages[4]

page = BeautifulSoup((ROOT / 'index.html').read_text(encoding='utf-8'), 'html.parser')
data = json.loads(page.find('script', id='guide-data').string)
categories = [c for c in data['chapters'] if c['group'] == 'COMPETITION CATEGORIES']
names = ['Digital Forensics', 'Malware Analysis', 'Web Security', 'Reverse Engineering',
         'OSINT', 'Cryptography', 'Miscellaneous']
ids = ['03-forensics', '09-malware', '02-web-exploitation', '06-reverse-engineering',
       '10-osint', '07-cryptography', '11-miscellaneous']
assert [c['id'] for c in categories] == ids
positions = [pages[1].index(name) for name in names]
assert positions == sorted(positions), 'Category order differs from PDF'
competition = next(c for c in data['chapters'] if c['id'] == 'competition')
assert competition['markdown'] == (ROOT / 'COMPETITION.md').read_text(encoding='utf-8')
assert data['markdown'] == (ROOT / 'HANDBOOK.md').read_text(encoding='utf-8')
text = competition['markdown']
for term in ['32 GB RAM', '1 TB SSD', '2 vCPU, 8 GiB RAM, 40 GB disk',
             'CSG_FLAG{example_flag}', '10:00–17:00', '09:00–13:00',
             '13:00–15:30', 'Practice-session reference only',
             'not establish a three-launch quota for competition day']:
    assert term in text, 'Missing setup detail: ' + term
source_links = re.findall(r'sources/practice-environment\.pdf#page=(\d+)', text)
assert source_links and all(1 <= int(n) <= 23 for n in source_links)
assert (ROOT / 'sources/practice-environment.pdf').exists()

# Reader-facing source pages only. Old reviewer transcripts intentionally retain
# exact statements from the versions they evaluated.
files = list((ROOT / 'chapters').glob('*.md')) + [ROOT / n for n in
        ['README.md', 'QUICKSTART.md', 'COMPETITION.md', 'TOOL-CHOOSER.md', 'TOOL-MATRIX.md']]
obsolete = [
    'six main subjects', 'lists the six main categories', 'six official categories',
    'same installation permission is not inferred for Kali',
    'same installation permission on Kali',
    'does not establish a separate Kali installation permission',
    'Do not infer a separate Kali installation permission',
    'same installation policy was stated for Kali',
    'installation permission is not inferred',
    'does not establish permission to bring prepared notes/scripts',
    'does not establish whether bringing this handbook',
    'Confirm that point with the organizer',
    'only where the event permits it',
]
for path in files:
    source = path.read_text(encoding='utf-8')
    for phrase in obsolete:
        assert phrase not in source, f'{path.name}: obsolete policy: {phrase}'

result = {
    'pdf': {'original': original.name, 'copy': 'sources/practice-environment.pdf',
            'sha256': digest, 'bytes': original.stat().st_size, 'pages': 23,
            'copy_identical': True},
    'categories_in_pdf_order': names, 'source_page_links': len(source_links),
    'reader_pages_checked_for_obsolete_policy': len(files),
    'generated_setup_matches_source': True, 'handbook_matches_download': True,
    'scope': 'Provenance and integration checks; semantic page-by-page audit in environment-audit.md. No event infrastructure used.',
    'errors': [],
}
(ROOT / 'review/environment-validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
