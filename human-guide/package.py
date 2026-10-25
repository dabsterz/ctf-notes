"""Package the reader-facing files after build and validation succeed."""
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
validation = json.loads((root / 'review/validation.json').read_text(encoding='utf-8'))
if validation['errors']:
    raise SystemExit('Refusing to package: aggregate validation has errors')
paths = [root / name for name in ['index.html', 'HANDBOOK.md', 'QUICKSTART.md', 'COMPETITION.md', 'TOOL-CHOOSER.md', 'RECIPES.md', 'README.md', 'TOOL-MATRIX.md', 'SOURCE-COVERAGE.md', 'LICENSE']]
paths += [root / 'sources/practice-environment.pdf', root / 'review/environment-audit.md', root / 'review/environment-validation.json']
paths += [root / 'review/ui-research.md', root / 'review/ui-validation.json']
paths += [root / 'review/ui' / name for name in ['desktop-dark.png', 'mobile-dark.png', 'command-view.png', 'tool-chooser.png']]
paths += sorted((root / 'recipes').glob('*.py'))
paths += sorted((root / 'chapters').glob('*.md'))
paths += [root / 'review' / name for name in ['validation.json', 'editorial-validation.md', 'improvement-validation.md', 'combined-coverage.json', 'tool-policy.json', 'tool-chooser-validation.json', 'site-validation.json']]
paths += [root / 'usability-tests/round-2' / name for name in ['RESULTS.md', 'verified-results.json']]
paths += sorted((root / 'usability-tests/round-2/reports').glob('*.md'))
review = root / 'usability-tests/human-review-20261025'
paths += [review / name for name in ['RESULTS.md', 'METHOD.md', 'snapshot.json', 'validation.json', 'fixture-correction.json', 'verified-outputs.json']]
paths += sorted((review / 'reports').glob('*.md'))
archive = root / 'Cyber-SEA-Game-Human-Guide.zip'
manifest = json.loads((root / 'cpts/manifest.json').read_text(encoding='utf-8'))
paths += [root / name for name in ['CPTS.md', 'CPTS-NOTES.md', 'cpts/manifest.json', 'review/cpts-validation.json']]
paths += [root / record['file'] for record in manifest['notes'] + manifest['assets']]
paths += [root / 'cpts/pages' / (record['id'] + '.md') for record in manifest['notes']]
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    for path in paths:
        output.write(path, 'Cyber-SEA-Game-Human-Guide/' + path.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as check:
    assert check.testzip() is None
    assert len(check.namelist()) == len(paths)
    assert check.read('Cyber-SEA-Game-Human-Guide/index.html') == (root / 'index.html').read_bytes()
    assert check.read('Cyber-SEA-Game-Human-Guide/HANDBOOK.md') == (root / 'HANDBOOK.md').read_bytes()
    for path in paths:
        assert check.read('Cyber-SEA-Game-Human-Guide/' + path.relative_to(root).as_posix()) == path.read_bytes()
print(json.dumps({'archive': str(archive), 'files': len(paths), 'bytes': archive.stat().st_size}))
