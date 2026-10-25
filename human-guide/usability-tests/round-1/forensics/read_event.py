import json
from pathlib import Path
record = json.loads(Path('events.json').read_text())
print('EventID:', record['EventID'])
print('UTC time as stored:', record['TimeCreated'])
print('Executable:', record['NewProcessName'])
print('Full command line:', record['ProcessCommandLine'])
