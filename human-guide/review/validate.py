"""Static validation of generated artifacts; does not execute challenge recipes."""
import ast
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
for path in sorted((ROOT / 'chapters').glob('*.md')):
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
    if rendered.find(['script', 'iframe', 'object', 'embed', 'img']):
        errors.append(f'{chapter["id"]}: active or external markup in chapter')
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
summary = {'chapters': len(payload['chapters']), 'tool_rows': len(payload['tools']),
           'original_files': len(inventory), 'code_blocks': fence_count, 'python_blocks_compiled': python_count,
           'errors': errors, 'warnings': warnings,
           'browser_check': 'Unavailable: no browsers exposed by computer-use tool; live interaction and visual layout not verified.'}
(ROOT / 'review/validation.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary, indent=2))
raise SystemExit(bool(errors))
