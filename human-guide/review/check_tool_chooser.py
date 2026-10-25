"""Check comparison-table structure and every cited workbook cell against the XLSX itself."""
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from build import load_tools

NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
with zipfile.ZipFile(ROOT.parent/'AJCCBC_CTF2026_Tool_Review_List_261015r11.xlsx') as archive:
    shared = ET.fromstring(archive.read('xl/sharedStrings.xml'))
    strings = [''.join(node.itertext()) for node in shared.findall('s:si',NS)]
    rels = ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
    targets = {node.attrib['Id']:node.attrib['Target'] for node in rels}
    book = ET.fromstring(archive.read('xl/workbook.xml'))
    sheets = {}
    for sheet in book.findall('s:sheets/s:sheet',NS):
        rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
        target = targets[rid]
        path = target.lstrip('/') if target.startswith('/') else 'xl/'+target
        document = ET.fromstring(archive.read(path))
        cells = {}
        for cell in document.findall('.//s:sheetData/s:row/s:c',NS):
            value = cell.findtext('s:v','',NS)
            if cell.attrib.get('t') == 's': value = strings[int(value)]
            elif cell.attrib.get('t') == 'inlineStr': value = ''.join(cell.find('s:is',NS).itertext())
            cells[cell.attrib['r']] = value
        sheets[sheet.attrib['name']] = cells

tools = load_tools()
for tool in tools:
    assert sheets[tool['sheet']][tool['cell']] == tool['name'], tool
    if tool['status'] == 'Approved':
        row = tool['cell'][1:]
        location = sheets[tool['sheet']].get(('I' if tool['platform']=='Windows / WSL' else 'F')+row,'')
        assert location == tool['location'], tool['name']
approved = {('W' if t['platform']=='Windows / WSL' else 'K')+t['cell'][1:]:t for t in tools if t['status']=='Approved'}
source = (ROOT/'TOOL-CHOOSER.md').read_text(encoding='utf-8')
rows, references, categories = [], set(), []
category = None
for line in source.splitlines():
    if line.startswith('## '): category = line[3:]
    if not line.startswith('|') or line.startswith('| ---') or line.startswith('| Tool /'):
        continue
    columns = re.split(r'(?<!\\)\|',line)[1:-1]
    assert len(columns)==4, f'Broken table in {category}: {line}'
    refs = re.findall(r'\b[WK]\d+\b',columns[0])
    assert refs, f'Missing policy source: {line}'
    for ref in refs:
        assert ref in approved, f'Not an approved policy reference: {ref}'
        references.add(ref)
    rows.append(dict(category=category,label=columns[0].strip(),policy=[dict(ref=ref,name=approved[ref]['name'],location=approved[ref]['location']) for ref in refs]))
    if category not in categories: categories.append(category)
assert set(categories)=={'Web','Passwords and hashes','Forensics','Network','Steganography and audio','Reverse engineering','Cryptography','Binary exploitation','Malware','OSINT','Miscellaneous'}
result=dict(workbook_entries_verified=len(tools),category_tables=len(categories),comparison_rows=len(rows),distinct_approved_rows_referenced=len(references),rows=rows)
(ROOT/'review/tool-chooser-validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
