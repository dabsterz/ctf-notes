"""Static validation of generated artifacts; does not execute challenge recipes."""
import ast
import base64
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []
python_count = 0
fence_count = 0
for path in sorted((ROOT / 'chapters').glob('*.md')) + [ROOT / n for n in ('QUICKSTART.md', 'COMPETITION.md', 'TOOL-CHOOSER.md', 'RECIPES.md')]:
    source = path.read_text(encoding='utf-8')
    fences = re.findall(r'^(`{3,}|~{3,})([^\n]*)\n', source, re.M)
    opened = None
    for fence, info in fences:
        if opened is None:
            opened = fence
            fence_count += 1
        elif fence[0] == opened[0] and len(fence) >= len(opened) and not info.strip():
            opened = None
    if opened:
        errors.append(f'{path.name}: unclosed code fence')
    for match in re.finditer(r'^```python[^\n]*\n(.*?)^```\s*$', source, re.M | re.S):
        python_count += 1
        try:
            compile(match.group(1), f'{path.name}:{source[:match.start()].count(chr(10))+1}', 'exec')
        except SyntaxError as exc:
            errors.append(str(exc))
    for match in re.finditer(r"python3?\s+-\s+<<\s*['\"]?(\w+)['\"]?[^\n]*\n(.*?)^\1\s*$", source, re.M | re.S):
        python_count += 1
        try:
            compile(match.group(2), f'{path.name}:heredoc:{source[:match.start()].count(chr(10))+1}', 'exec')
        except SyntaxError as exc:
            errors.append(str(exc))

page = (ROOT / 'index.html').read_text(encoding='utf-8')
doc = BeautifulSoup(page, 'html.parser')
payload = json.loads(doc.find('script', id='guide-data').string)
ids = {c['id'] for c in payload['chapters']} | {'tools', 'content'}
for chapter in payload['chapters']:
    rendered = BeautifulSoup(chapter['html'], 'html.parser')
    heading_ids = [node['id'] for node in rendered.find_all(id=True)]
    duplicates = [key for key, count in Counter(heading_ids).items() if count > 1]
    if duplicates:
        errors.append(f'{chapter["id"]}: duplicate heading IDs {duplicates}')
    ids.update(heading_ids)
    if rendered.find(['script', 'iframe', 'object', 'embed']):
        errors.append(f'{chapter["id"]}: active or external markup in chapter')
    for image in rendered.find_all('img'):
        if chapter['group'] != 'CPTS NOTES' or not image.get('src', '').startswith('data:image/png;base64,'):
            errors.append(f'{chapter["id"]}: unexpected image source')
    path = ROOT / chapter['path']
    if path.read_text(encoding='utf-8') != chapter['markdown']:
        errors.append(f'{chapter["id"]}: website differs from chapter Markdown')
for chapter in payload['chapters']:
    rendered = BeautifulSoup(chapter['html'], 'html.parser')
    for a in rendered.find_all('a', href=True):
        href = a['href']
        if href.startswith('#') and href[1:] not in ids:
            errors.append(f'{chapter["id"]}: missing anchor {href}')
        elif not href.startswith(('http:', 'https:', '#')) and not (ROOT / Path(chapter['path']).parent / href.split('#')[0]).exists():
            errors.append(f'{chapter["id"]}: missing local target {href}')
if doc.find('script', src=True) or doc.find('link', href=True) or doc.find('img', src=True):
    errors.append('External/runtime assets found')
if payload['markdown'] != (ROOT / 'HANDBOOK.md').read_text(encoding='utf-8'):
    errors.append('Embedded Markdown download differs from HANDBOOK.md')
for name, source in payload['recipes'].items():
    if source != (ROOT / 'recipes' / name).read_text(encoding='utf-8'):
        errors.append('Embedded recipe differs: ' + name)
    compile(source, name, 'exec')
book = payload['markdown']
manifest = json.loads((ROOT / 'cpts/manifest.json').read_text(encoding='utf-8'))
asset_hashes = {a['sha256'] for a in manifest['assets']}
notes = [c for c in payload['chapters'] if c.get('note_path')]
assert {c['id'] for c in notes} == {n['id'] for n in manifest['notes']}
assert not set(manifest['excluded']) & {n['path'] for n in manifest['notes']}
for record in manifest['notes'] + manifest['assets']:
    assert hashlib.sha256((ROOT / record['file']).read_bytes()).hexdigest() == record['sha256']
seen_images = set()
for chapter in notes:
    for image in BeautifulSoup(chapter['html'], 'html.parser').find_all('img'):
        digest = hashlib.sha256(base64.b64decode(image['src'].split(',', 1)[1], validate=True)).hexdigest()
        assert digest in asset_hashes
        seen_images.add(digest)
assert seen_images == asset_hashes
assert payload['cptsMarkdown'] == (ROOT / 'CPTS-NOTES.md').read_text(encoding='utf-8')
(ROOT / 'review/cpts-validation.json').write_text(json.dumps({'notes': len(notes), 'images': len(seen_images), 'excluded': manifest['excluded'], 'checks': ['All imported files match snapshot SHA-256 hashes', 'All note IDs present and unique', 'All referenced PNGs embedded offline', 'Separate Markdown download matches CPTS-NOTES.md']}, indent=2), encoding='utf-8')
book_ids = set(re.findall(r'<a id="([^"]+)"></a>', book))
# Exclude fenced examples: a literal Markdown payload is not a navigation link.
book_prose = re.sub(r'^```[^\n]*\n.*?^```\s*$', '', book, flags=re.M | re.S)
for anchor in re.findall(r'\]\(#([^)]*)\)', book_prose):
    if anchor not in book_ids:
        errors.append('Combined Markdown missing anchor: ' + anchor)
inventory = json.loads((ROOT / 'review/source-inventory.json').read_text(encoding='utf-8'))
coverage = json.loads((ROOT / 'review/combined-coverage.json').read_text(encoding='utf-8'))
if {i['source'] for i in inventory} != {c['source'] for c in coverage}:
    errors.append('Source coverage does not match original inventory')
pending = [c['source'] for c in coverage if c['disposition'] == 'pending']
if pending:
    errors.append(f'{len(pending)} original sources still pending editorial disposition')
for item in inventory:
    original = ROOT.parent / item['source']
    if hashlib.sha256(original.read_bytes()).hexdigest() != item['sha256']:
        errors.append('Original modified: ' + item['source'])
for item in coverage:
    destination = item.get('chapter', '')
    if destination and not (ROOT / destination).exists():
        errors.append(f'{item["source"]}: missing destination {destination}')
browser_check = 'Current build has not completed the separate Chrome UI checks.'
browser_report = ROOT / 'review/ui-validation.json'
if browser_report.exists():
    ui = json.loads(browser_report.read_text(encoding='utf-8'))
    if ui.get('html_sha256') == hashlib.sha256((ROOT / 'index.html').read_bytes()).hexdigest() and not ui.get('errors'):
        browser_check = 'Automated local-file Chrome rendering and interaction passed; see ui-validation.json and ui-research.md for scope and screenshot review.'
summary = {'chapters': len(payload['chapters']), 'tool_rows': len(payload['tools']),
           'original_files': len(inventory), 'code_blocks': fence_count, 'python_blocks_compiled': python_count,
           'errors': errors, 'warnings': warnings,
           'browser_check': browser_check}
(ROOT / 'review/validation.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
raise SystemExit(bool(errors))
