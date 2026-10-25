"""Package the reader-facing files after build and validation succeed."""
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
validation = json.loads((root / 'review/validation.json').read_text(encoding='utf-8'))
if validation['errors']:
    raise SystemExit('Refusing to package: aggregate validation has errors')
paths = [root / name for name in ['index.html', 'HANDBOOK.md', 'README.md', 'TOOL-MATRIX.md', 'SOURCE-COVERAGE.md', 'LICENSE']]
paths += sorted((root / 'chapters').glob('*.md'))
paths += [root / 'review' / name for name in ['validation.json', 'editorial-validation.md', 'combined-coverage.json', 'tool-policy.json']]
archive = root / 'Cyber-SEA-Game-Human-Guide.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as output:
    for path in paths:
        output.write(path, 'Cyber-SEA-Game-Human-Guide/' + path.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as check:
    assert check.testzip() is None
    assert len(check.namelist()) == len(paths)
    assert check.read('Cyber-SEA-Game-Human-Guide/index.html') == (root / 'index.html').read_bytes()
    assert check.read('Cyber-SEA-Game-Human-Guide/HANDBOOK.md') == (root / 'HANDBOOK.md').read_bytes()
print(json.dumps({'archive': str(archive), 'files': len(paths), 'bytes': archive.stat().st_size}))
