"""Check preserved references and report default-view prose, not human speed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('guide_build', ROOT / 'build.py')
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)
before = json.loads((ROOT / 'review/readability-before.json').read_text())
metrics = {}


def counts(source):
    doc = BeautifulSoup(build.render_markdown(source, 'measure'), 'html.parser')
    blocks = len(doc.select('pre'))
    for node in doc.select('pre, table'):
        node.decompose()
    return len(doc.get_text(' ', strip=True).split()), blocks


for name, digest in before.items():
    archive = ROOT / 'reference/chapters' / name
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == digest, name
    original = archive.read_text(encoding='utf-8')
    quick = (ROOT / 'quick' / name).read_text(encoding='utf-8')
    composed = (ROOT / 'chapters' / name).read_text(encoding='utf-8')
    assert composed == build.compose_chapter(quick, original), name
    old_words, old_blocks = counts(original)
    new_words, new_blocks = counts(quick)
    assert new_words < old_words, name
    assert new_blocks >= 8, name
    old_doc = BeautifulSoup(build.render_markdown(original, name[:-3]), 'html.parser')
    new_doc = BeautifulSoup(build.render_markdown(composed, name[:-3]), 'html.parser')
    old_ids = {n['id'] for n in old_doc.select('[id]')}
    assert old_ids <= {n['id'] for n in new_doc.select('[id]')}, name
    details = new_doc.select_one('details.deep-reference')
    assert details and not details.has_attr('open'), name
    old_code = [n.get_text().replace('-E separator=,', "-E 'separator=,'") for n in old_doc.select('pre code')]
    assert old_code == [n.get_text() for n in details.select('pre code')], name
    metrics[name] = {'previous_prose_words': old_words, 'default_prose_words': new_words,
                     'prose_reduction_percent': round(100 * (1 - new_words / old_words), 1),
                     'default_code_blocks': new_blocks, 'retained_reference_code_blocks': old_blocks}

manifest = json.loads((ROOT / 'cpts/manifest.json').read_text())
for record in manifest['notes'] + manifest['assets']:
    assert hashlib.sha256((ROOT / record['file']).read_bytes()).hexdigest() == record['sha256']
http_note = next(n for n in manifest['notes'] if n['path'] == 'Enumeration/Service Enumeration/80,443 http.md')
source = (ROOT / 'cpts/pages' / (http_note['id'] + '.md')).read_text(encoding='utf-8')
assert 'Editor correction' in source and 'ffuf -u "$URL/FUZZ"' in source
assert '-H "Host: siteisup.htb/FUZZ"' not in source
result = {'categories': len(metrics), 'default_code_blocks': sum(v['default_code_blocks'] for v in metrics.values()),
          'metrics': metrics, 'checks': ['Archive hashes unchanged', 'Original code blocks and anchors retained with explicit TShark comma-quoting correction', 'Collapsed reference rendered correctly', 'Personal raw notes and images unchanged', 'Personal HTTP example corrected in presentation'],
          'scope': 'Prose counts exclude fenced code and tables. Measures the default reading path; full reference remains available. No new human-usability score is claimed.'}
(ROOT / 'review/readability-validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
