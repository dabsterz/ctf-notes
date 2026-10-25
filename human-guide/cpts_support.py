"""Read-only Obsidian import and offline presentation of Vernon's CPTS notes."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import quote


def note_id(path: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', path.removesuffix('.md').lower()).strip('-')
    return 'cpts-' + slug + '-' + hashlib.sha256(path.encode()).hexdigest()[:8]


def prose_lines(source):
    """Yield prose/fence/code without treating Bash [[ ... ]] as wiki links."""
    fence = None
    for line in source.splitlines():
        marker = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if marker and (fence is None or (marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip())):
            fence = marker[1] if fence is None else None
            # Obsidian accepts loose language labels; Python Markdown does not.
            # Keep command lines untouched and normalize only the fence metadata.
            label = re.match(r'[A-Za-z0-9_+.#-]+', marker[2].strip()) if fence else None
            yield 'fence', marker[1] + (label[0] if label else '')
        else:
            yield ('code' if fence else 'prose'), line


def image_references(source):
    for kind, line in prose_lines(source):
        if kind == 'prose':
            for name in re.findall(r'!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]', line):
                yield name


def convert_note(source: str, images: dict[str, str]) -> str:
    lines = []
    for kind, line in prose_lines(source):
        if kind == 'prose':
            line = re.sub(r'!\[\[([^\]|]+)(?:\|[^\]]*)?\]\]',
                          lambda m: '![' + m[1] + '](' + images[m[1]] + ')' if m[1] in images else m[0], line)
            if re.fullmatch(r'https?://[^\s<>]+', line.strip()):
                line = '<' + line.strip() + '>'
            if re.fullmatch(r'#{1,6}\s*', line):
                line = ''
        lines.append(line)
    return '\n'.join(lines) + '\n'


def import_vault(source: Path, root: Path, excluded: set[str]) -> dict:
    source = source.resolve()
    paths = sorted(source.rglob('*.md'), key=lambda p: p.relative_to(source).as_posix().casefold())
    known = {p.relative_to(source).as_posix() for p in paths}
    if not excluded <= known:
        raise ValueError('Excluded paths do not exist: ' + str(excluded - known))
    notes, wanted = [], set()
    # Read first: an unexpected cloud/read error must not create a partial import.
    contents = {}
    for path in paths:
        relative = path.relative_to(source).as_posix()
        if relative in excluded:
            continue
        raw = path.read_bytes()
        text = raw.decode('utf-8-sig')
        contents[relative] = raw
        wanted.update(image_references(text))
    assets, asset_bytes = [], {}
    for name in sorted(wanted):
        candidates = [p for p in source.parent.rglob(Path(name).name) if p.is_file() and p.name == name]
        if len(candidates) != 1:
            raise ValueError(f'Expected one attachment for {name}; found {len(candidates)}')
        raw = candidates[0].read_bytes()
        if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
            raise ValueError('Unsupported or invalid PNG attachment: ' + name)
        asset_bytes[name] = raw
        assets.append({'name': name, 'file': 'cpts/assets/' + name,
                       'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
    for relative, raw in contents.items():
        target = root / 'cpts/original' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
        notes.append({'path': relative, 'file': target.relative_to(root).as_posix(),
                      'id': note_id(relative), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
    for asset in assets:
        target = root / asset['file']; target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(asset_bytes[asset['name']])
    manifest = {'source_root': str(source), 'notes': notes, 'assets': assets,
                'excluded': sorted(excluded), 'exclusion_reason': 'User requested omission of the two OneDrive sync-error notes.'}
    (root / 'cpts/manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    return manifest


def build_cpts(root, render, merge):
    manifest_path = root / 'cpts/manifest.json'
    if not manifest_path.exists():
        return []
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    image_paths = {a['name']: '../assets/' + quote(a['name']) for a in manifest['assets']}
    images = {}
    for a in manifest['assets']:
        raw = (root / a['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == a['sha256']
        images[image_paths[a['name']]] = 'data:image/png;base64,' + base64.b64encode(raw).decode('ascii')
    chapters = []
    overview = ["# Vernon's CPTS notes", '',
                f"**{len(manifest['notes'])} personal notes**, organized as in the Obsidian vault. Screenshots are included offline.", '',
                'These are your original study notes, not a competition-approved tool list. Check [event tool rules](COMPETITION.md#what-is-allowed) before using their tools or setup commands.', '',
                'Browse the folders in the sidebar, or use the main search. The ZIP contains the original Markdown and screenshots; [CPTS notes as one Markdown file](CPTS-NOTES.md) is also included.', '']
    previous = None
    for record in sorted(manifest['notes'], key=lambda n: (Path(n['path']).parent.as_posix(), n['path'])):
        path = Path(record['path']); folder = path.parent.as_posix()
        if folder != previous:
            overview.extend(['## ' + ('General' if folder == '.' else folder), ''])
            previous = folder
        overview.append(f'- [{path.stem}](cpts/pages/{record["id"]}.md)')
        raw = (root / record['file']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == record['sha256']
        body = convert_note(raw.decode('utf-8-sig'), image_paths)
        source = '# ' + path.stem + '\n\n' + body
        target = root / 'cpts/pages' / (record['id'] + '.md')
        target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(source.encode('utf-8'))
        chapters.append({'id': record['id'], 'title': path.stem, 'group': 'CPTS NOTES',
                         'path': target.relative_to(root).as_posix(), 'note_path': record['path'],
                         'markdown': source, 'html': render(source, record['id'], images=images)})
    overview.extend(['', 'Two unreadable OneDrive notes were omitted at your request: `Exploits/Web Exploits.md` and `Exploits/Web Shells-DESKTOP-0GERI6L.md`.', ''])
    intro = '\n'.join(overview)
    (root / 'CPTS.md').write_bytes(intro.encode('utf-8'))
    index = {'id': 'cpts', 'title': "Vernon's CPTS notes", 'group': 'CPTS NOTES', 'path': 'CPTS.md',
             'markdown': intro, 'html': render(intro, 'cpts')}
    book = "# Vernon's CPTS notes\n\nPersonal reference; consult COMPETITION.md before using a tool during the event.\n\n"
    book += '\n'.join(f'- [{c["note_path"]}](#{c["id"]})' for c in chapters)
    for c in chapters:
        book += '\n\n---\n\n<a id="' + c['id'] + '"></a>\n\n' + merge(c['markdown'].replace('../assets/', 'cpts/assets/'), c['id'])
    (root / 'CPTS-NOTES.md').write_bytes(book.encode('utf-8'))
    # This is a file download, not another reader route.
    index['html'] = index['html'].replace('href="#cpts-notes"', 'href="CPTS-NOTES.md" download="CPTS-NOTES.md"')
    return [index] + chapters


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vault', type=Path)
    parser.add_argument('--exclude', action='append', default=[])
    args = parser.parse_args()
    result = import_vault(args.vault, Path(__file__).resolve().parent, set(args.exclude))
    print(json.dumps({'notes': len(result['notes']), 'images': len(result['assets']), 'excluded': result['excluded']}))
