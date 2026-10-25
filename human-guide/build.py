"""Build the offline handbook. Reading the result needs no Python or server."""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import markdown
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent


def load_tools() -> list[dict]:
    sheets = json.loads((ROOT / 'review/tool-policy.json').read_text(encoding='utf-8'))
    entries = []
    for sheet in sheets:
        rejected = sheet['name'] == 'Unapproved List'
        for cells in sheet['rows']:
            def value(column):
                return next((v for k, v in cells.items() if re.fullmatch(column + r'\d+', k)), '')
            if not value('A' if rejected else 'B').isdigit():
                continue
            cell = next(k for k in cells if re.fullmatch(('B' if rejected else 'C') + r'\d+', k))
            entries.append({
                'name': value('B' if rejected else 'C'),
                'status': 'Unapproved' if rejected else 'Approved',
                'platform': 'Not approved' if rejected else ('Kali' if sheet['name'].endswith('Kali') else 'Windows / WSL'),
                'version': '' if rejected else value('E'),
                'location': '' if rejected else value('I' if sheet['name'].endswith('Windows') else 'F'),
                'notes': value('C') if rejected else value('H' if sheet['name'].endswith('Windows') else 'G'),
                'sheet': sheet['name'], 'cell': cell,
                'url': value('F') if sheet['name'].endswith('Windows') else '',
            })
    return entries


def render_markdown(source: str, chapter_id: str, images: dict | None = None) -> str:
    result = markdown.markdown(source, extensions=['fenced_code', 'tables', 'toc', 'sane_lists', 'md_in_html'])
    soup = BeautifulSoup(result, 'html.parser')
    for bad in soup.find_all(['script', 'style', 'iframe', 'object', 'embed', 'form', 'input', 'button', 'img', 'link', 'meta']):
        if bad.name == 'img' and images and bad.get('src') in images:
            bad['src'] = images[bad['src']]
            bad['loading'] = 'lazy'
            bad['decoding'] = 'async'
            bad['class'] = 'cpts-image'
            continue
        bad.decompose()
    for tag in soup.find_all(True):
        for attribute in list(tag.attrs):
            allowed = {'id', 'class', 'href', 'title', 'colspan', 'rowspan'}
            if tag.name == 'img':
                allowed |= {'src', 'alt', 'loading', 'decoding'}
            if attribute not in allowed:
                del tag[attribute]
        if tag.has_attr('href'):
            href = tag['href']
            if urlsplit(href).scheme not in {'', 'https', 'http'} or href.startswith('//'):
                del tag['href']
            elif href.startswith(('https://', 'http://')):
                tag['rel'] = 'noopener noreferrer'
                tag['target'] = '_blank'
    for heading in soup.find_all(re.compile('^h[1-6]$')):
        if heading.get('id'):
            heading['id'] = chapter_id + '--' + heading['id']
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('#'):
            link['href'] = '#' + chapter_id + '--' + link['href'][1:]
        elif not urlsplit(link['href']).scheme:
            target, _, fragment = link['href'].partition('#')
            if target.endswith('.md'):
                target_id = Path(target).stem.lower()
                link['href'] = '#' + target_id + ('--' + fragment if fragment else '')
    for table in soup.find_all('table'):
        # Table pipes need a Markdown escape, but it must not reach copied shell text.
        for code in table.find_all('code'):
            if code.string is not None:
                code.string = code.string.replace('\\|', '|')
        wrapper = soup.new_tag('div', attrs={'class': 'table-scroll', 'tabindex': '0'})
        table.wrap(wrapper)
    return str(soup)


def compose_chapter(quick: str, original: str) -> str:
    """Keep the old reference and anchors behind a reader-controlled disclosure."""
    quick = re.sub(r'\]\(\.\./reference/chapters/[^)]+\.md\)', '](#full-reference)', quick)
    # A shorter display title must not discard the old title's deep link.
    body = original if quick.split('\n', 1)[0] != original.split('\n', 1)[0] else original.split('\n', 1)[1].lstrip('\n')
    # Native PowerShell otherwise drops the unquoted comma. Archive stays intact.
    body = body.replace('-E separator=,', "-E 'separator=,'")
    return (quick.rstrip() + '\n\n## Full reference\n\n'
            '<details class="deep-reference" markdown="1">\n'
            '<summary>Explanations, advanced cases and sources</summary>\n\n'
            + body.rstrip() + '\n\n</details>\n')


def table_cell(value: str) -> str:
    return value.replace('|', '\\|').replace('\r', '').replace('\n', '<br>') or '—'


def merge_markdown(source: str, chapter_id: str) -> str:
    """Preserve section-level jumps when separate Markdown files become one book."""
    soup = BeautifulSoup(render_markdown(source, chapter_id), 'html.parser')
    headings = iter(h['id'] for h in soup.find_all(re.compile('^h[1-6]$')))
    lines, fence = [], None
    def rewrite(match):
        target = match.group(2)
        path, _, fragment = target.partition('#')
        if target.startswith('#'):
            target = '#' + chapter_id + '--' + fragment
        elif not urlsplit(target).scheme and path.endswith('.md'):
            target = '#' + Path(path).stem.lower() + ('--' + fragment if fragment else '')
        return '[' + match.group(1) + '](' + target + ')'
    for line in source.splitlines():
        marker = re.match(r'^(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            lines.append(line)
            continue
        if fence is None:
            if re.match(r'^#{1,6} ', line):
                lines.extend([f'<a id="{next(headings)}"></a>', ''])
            line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', rewrite, line)
        lines.append(line)
    return '\n'.join(lines) + '\n'


def recipe_sources():
    recipes = {p.name: p.read_text(encoding='utf-8') for p in sorted((ROOT / 'recipes').glob('*.py'))}
    lines = ['# Recipe downloads and source', '',
             'The short guide uses these complete scripts. In the website, each download is embedded and works offline. Save it inside a folder named `recipes` beside your challenge files; run from the parent folder. The ZIP already contains this layout. In Markdown, each link points to the included file.', '',
             'Use WSL Python 3 from the supplied list. These helpers use the standard library only. Each script accepts `--help`. They implement the specific assumptions stated in the [quick reference](QUICKSTART.md); they do not choose an attack for you.', '']
    for name, source in recipes.items():
        lines += [f'## {name}', '', f'[Download {name}](recipes/{name})', '', '```python', source.rstrip(), '```', '']
    (ROOT / 'RECIPES.md').write_text('\n'.join(lines), encoding='utf-8')
    return recipes


def tool_matrix(tools):
    lines = ['# Tool matrix: the complete supplied list', '',
             'Source: `AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx`. Recorded versions are copied as supplied, not independently verified. Blank installation notes do not establish availability. The unapproved reasons are retained verbatim. The workbook contains some replacement characters; these are preserved rather than guessed.', '',
             'Windows/WSL and Kali are separate environments. See the location column before choosing a command. For non-AI additions, named exclusions and hosted-service restrictions, use [Competition setup](COMPETITION.md#what-is-allowed).', '']
    for platform in ['Windows / WSL', 'Kali', 'Not approved']:
        subset = [t for t in tools if t['platform'] == platform]
        lines += [f'## {platform} · {len(subset)} entries', '',
                  '| Tool | Version | Installation/location | Notes/reason | Workbook source |',
                  '| --- | --- | --- | --- | --- |']
        for t in subset:
            lines.append('| ' + ' | '.join(table_cell(v) for v in [t['name'], t['version'], t['location'], t['notes'], f"{t['sheet']}!{t['cell']}"]) + ' |')
        lines.append('')
    return '\n'.join(lines) + '\n'


def source_inventory():
    path = ROOT / 'review/source-inventory.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    entries = []
    for p in sorted(REPO.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(REPO)
        if any(part in {'human-guide', '__pycache__', '.pytest_cache', '.git', 'node_modules', 'docs'} for part in rel.parts):
            continue
        data = p.read_bytes()
        entries.append({'source': rel.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    path.write_text(json.dumps(entries, indent=2), encoding='utf-8')
    return entries


def build_coverage(inventory):
    reviews = {}
    for path in sorted((ROOT / 'review').glob('*-coverage.json')):
        if path.name == 'combined-coverage.json':
            continue
        items = json.loads(path.read_text(encoding='utf-8'))
        for item in items:
            item['source'] = item['source'].replace('\\', '/')
            if item['source'] in reviews:
                raise ValueError('Duplicate source review: ' + item['source'])
            reviews[item['source']] = item
    combined = []
    for record in inventory:
        source = record['source']
        if source in reviews:
            combined.append(record | reviews[source])
            continue
        if source.startswith(('ctf-',)) and not source.startswith('ctf-writeup/'):
            combined.append(record | {'chapter': '', 'disposition': 'pending', 'notes': 'Category review has not yet supplied a disposition.'})
            continue
        chapter = 'chapters/01-first-ten-minutes.md'
        if source.startswith('solve-challenge/') or source.startswith('ctf-writeup/'):
            status, note = 'adapted', 'Human triage, hypothesis logging, team handoff and writeup; AI routing and agent commands removed.'
        elif source.startswith('.opencode/'):
            status, note = 'excluded', 'Agent role/configuration instructions; category expertise is represented by the human chapters. No competition workflow depends on an agent.'
        elif source == 'scripts/install_ctf_tools.sh':
            chapter = 'chapters/00-tool-rules.md'
            status, note = 'excluded', 'Broad unrestricted installer conflicts with event whitelist. Use existing listed installations.'
        elif source == 'scripts/generate_catalog.py':
            status, note = 'replaced', 'Original catalog is an agent index with remote analytics. New site embeds complete human guides with no external runtime assets.'
        elif source.startswith(('evals/', 'tests/', 'scripts/', '.github/')):
            status, note = 'reference-only', 'Repository development/evaluation infrastructure or synthetic fixture, not event solving instructions. Inventory/structural review; not reproduced as a competition workflow.'
        elif source.endswith('.xlsx'):
            chapter = 'TOOL-MATRIX.md'
            status, note = 'adapted', 'All three sheets and 282 tool rows extracted with cell provenance and full remarks.'
        elif source == 'LICENSE':
            chapter = 'LICENSE'
            status, note = 'retained', 'Original MIT copyright and permission notice retained in the deliverable.'
        elif source == 'README.md':
            chapter = 'chapters/00-start-here.md'
            status, note = 'adapted', 'Category overview and navigation converted to human reading routes; agent setup excluded.'
        else:
            status, note = 'reference-only', 'Repository governance, configuration or contribution material; retained in original tree, not a challenge-solving recipe.'
        combined.append(record | {'chapter': chapter, 'disposition': status, 'notes': note})
    unknown = set(reviews) - {r['source'] for r in inventory}
    if unknown:
        raise ValueError('Review lists unknown original sources: ' + ', '.join(sorted(unknown)))
    (ROOT / 'review/combined-coverage.json').write_text(json.dumps(combined, indent=2, ensure_ascii=False), encoding='utf-8')
    lines = ['# Source coverage and editorial decisions', '',
             f'The original snapshot contains **{len(inventory)} files**, including **{sum(r["source"].endswith(".md") for r in inventory)} Markdown files**. Every file is listed below. Category guides were reviewed for human adaptation; infrastructure received inventory/structural review. This is not a claim that every historical exploit was executed or every source sentence was reproduced.', '',
             '**Adapted/merged** means useful content was rewritten or consolidated. **Reference-only** retains specialist/history or development context without presenting it as a ready event recipe. **Excluded** explains material incompatible with the event or human workflow. The chapter is the destination or nearest explanation. Review details and original SHA-256 hashes are in `review/combined-coverage.json`.', '',
             'Additional competition source: the subsequently supplied 23-page [environment PDF](sources/practice-environment.pdf) is reconciled in [Competition setup](COMPETITION.md). Its source/copy hash and page-by-page disposition are recorded separately in `review/environment-validation.json` and `review/environment-audit.md`; it is not silently added to the original 286-file baseline.', '',
             '| Original source | Disposition | Human destination | Review note |',
             '| --- | --- | --- | --- |']
    for item in combined:
        lines.append('| ' + ' | '.join(table_cell(str(item.get(k, ''))) for k in ['source', 'disposition', 'chapter', 'notes']) + ' |')
    return '\n'.join(lines) + '\n', combined


def main():
    tools = load_tools()
    inventory = source_inventory()
    matrix = tool_matrix(tools)
    (ROOT / 'TOOL-MATRIX.md').write_text(matrix, encoding='utf-8')
    coverage, records = build_coverage(inventory)
    (ROOT / 'SOURCE-COVERAGE.md').write_text(coverage, encoding='utf-8')
    (ROOT / 'LICENSE').write_bytes((REPO / 'LICENSE').read_bytes())
    recipes = recipe_sources()
    groups = [
        ('CONTEST SHORTCUTS', ['QUICKSTART.md', 'COMPETITION.md', 'TOOL-CHOOSER.md']),
        ('GET ORIENTED', ['chapters/00-start-here.md', 'chapters/00-tool-rules.md', 'chapters/01-first-ten-minutes.md']),
        ('COMPETITION CATEGORIES', ['chapters/' + name + '.md' for name in
          ['03-forensics', '09-malware', '02-web-exploitation', '06-reverse-engineering', '10-osint', '07-cryptography', '11-miscellaneous']]),
        ('SUPPORTING REFERENCE', ['chapters/' + name + '.md' for name in
          ['04-network', '05-steganography', '08-binary-exploitation', '13-pwn-practice-atlas', '14-advanced-crypto']]),
        ('REFERENCE', ['chapters/12-excluded-and-advanced.md', 'RECIPES.md', 'TOOL-MATRIX.md', 'SOURCE-COVERAGE.md']),
    ]
    paths = [(ROOT / path, group) for group, names in groups for path in names]
    assert {p for p, _ in paths if p.parent.name == 'chapters'} == set((ROOT / 'chapters').glob('*.md'))
    chapters = []
    for path, group in paths:
        quick = ROOT / 'quick' / path.name
        archived = ROOT / 'reference/chapters' / path.name
        if path.parent.name == 'chapters' and quick.exists():
            source = compose_chapter(quick.read_text(encoding='utf-8'), archived.read_text(encoding='utf-8'))
            path.write_bytes(source.encode('utf-8'))
        source = path.read_text(encoding='utf-8')
        title = re.search(r'^# (.+)$', source, re.M).group(1)
        chapters.append({'id': path.stem.lower(), 'title': title, 'group': group, 'path': path.relative_to(ROOT).as_posix(), 'markdown': source,
                         'html': render_markdown(source, path.stem.lower())})
    from cpts_support import build_cpts
    cpts_chapters = build_cpts(ROOT, render_markdown, merge_markdown)
    insert_at = next(i for i, c in enumerate(chapters) if c['group'] == 'REFERENCE')
    chapters[insert_at:insert_at] = cpts_chapters
    combined = '# Cyber SEA Game 2026 · Human CTF Handbook\n\nPrepared for Windows/WSL and Kali from the supplied repository, tool workbook and environment PDF. Start with the quick reference; competition setup holds the access and rules details.\n\n'
    combined += '\n'.join(f'- [{c["title"]}](#{c["id"]})' for c in chapters) + '\n\n'
    for c in chapters:
        merged_source = merge_markdown(c['markdown'].replace('../assets/', 'cpts/assets/') if c.get('note_path') else c['markdown'], c['id'])
        combined += f'\n\n---\n\n<a id="{c["id"]}"></a>\n\n' + merged_source
    combined += '\n\n---\n\n## Attribution and license\n\nAdapted from the supplied ctf-skills repository. Original copyright (c) 2026 Lukasz Jagiello. Personal CPTS notes supplied by Vernon are separate from this attribution.\n\n```text\n' + (ROOT / 'LICENSE').read_text(encoding='utf-8') + '\n```\n'
    (ROOT / 'HANDBOOK.md').write_text(combined, encoding='utf-8')
    if cpts_chapters:
        combined = combined.replace('[CPTS notes as one Markdown file](#cpts-notes)', '[CPTS notes as one Markdown file](CPTS-NOTES.md)')
        (ROOT / 'HANDBOOK.md').write_text(combined, encoding='utf-8')
    payload = {'chapters': chapters, 'tools': tools, 'markdown': combined, 'recipes': recipes,
               'cptsMarkdown': (ROOT / 'CPTS-NOTES.md').read_text(encoding='utf-8') if cpts_chapters else '',
               'stats': {'sources': len(inventory), 'chapters': len(chapters), 'commands': sum(len(re.findall(r'^```\w', c['markdown'], re.M)) for c in chapters)}}
    encoded = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    template = (ROOT / 'assets/template.html').read_text(encoding='utf-8')
    page = template.replace('/* EMBED_STYLE */', (ROOT / 'assets/style.css').read_text(encoding='utf-8'))
    page = page.replace('/* EMBED_APP */', (ROOT / 'assets/app.js').read_text(encoding='utf-8'))
    page = page.replace('/* EMBED_DATA */', encoded)
    (ROOT / 'index.html').write_text(page, encoding='utf-8')
    print(json.dumps({'chapters': len(chapters), 'tool_rows': len(tools), 'source_files': len(inventory), 'pending_sources': sum(r['disposition'] == 'pending' for r in records), 'html_bytes': len(page.encode()), 'markdown_bytes': len(combined.encode())}))


if __name__ == '__main__':
    main()
