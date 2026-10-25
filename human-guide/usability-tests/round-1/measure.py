"""Reproducible document-size metrics; not a human reading-time estimate."""
import json
import re
from pathlib import Path

guide = Path(__file__).resolve().parents[2]
rows = []
for path in sorted((guide / 'chapters').glob('*.md')):
    source = path.read_text(encoding='utf-8')
    code = []
    prose = []
    opened = False
    current = []
    blocks = []
    for line in source.splitlines():
        if line.startswith('```'):
            if opened:
                blocks.append(current)
                code.extend(current)
                current = []
            opened = not opened
        elif opened:
            current.append(line)
        else:
            prose.append(line)
    rows.append({'chapter':path.name, 'total_lines':len(source.splitlines()),
                 'prose_whitespace_words':len(' '.join(prose).split()),
                 'code_lines':len(code), 'code_blocks':len(blocks),
                 'longest_code_block_lines':max(map(len,blocks),default=0),
                 'headings':len(re.findall(r'^#{1,6} ',source,re.M))})
result = {'definition':'Whitespace-separated tokens outside fenced code, including tables/headings/links. Counts measure document size, not reading difficulty or human time.',
          'chapters':rows,
          'totals':{key:sum(row[key] for row in rows) for key in ['total_lines','prose_whitespace_words','code_lines','code_blocks','headings']}}
(Path(__file__).parent/'size-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result['totals']))
print('Longest chapters by prose word count:',[(r['chapter'],r['prose_whitespace_words']) for r in sorted(rows,key=lambda r:r['prose_whitespace_words'],reverse=True)[:5]])
