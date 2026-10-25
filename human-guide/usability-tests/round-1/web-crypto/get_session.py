import urllib.request
import urllib.error
from pathlib import Path
base = 'http://127.0.0.1:18765'
with urllib.request.urlopen(base + '/session') as response:
    body = response.read().decode()
print('GET /session:', body)
Path(__file__).with_name('session-response.txt').write_text(body, encoding='utf-8')
