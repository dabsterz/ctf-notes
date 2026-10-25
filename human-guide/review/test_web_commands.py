"""Run selected published curl blocks against a loopback-only request recorder.

Run in WSL with python3 -B -m unittest discover -s human-guide/review
-p test_web_commands.py. Tests transport/quoting, not target vulnerabilities.
"""
import http.server
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import threading
import unittest
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which('bash') and shutil.which('curl') and __import__('os').name != 'nt', 'WSL Bash/curl integration')
class WebCommandTransport(unittest.TestCase):
    def test_published_curl_blocks(self):
        events = []

        class Recorder(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                self.record()

            def do_POST(self):
                self.record()

            def record(self):
                body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                events.append({'path': self.path, 'body': body, 'headers': dict(self.headers)})
                self.send_response(200)
                if self.path == '/login':
                    self.send_header('Set-Cookie', 'session=local-test; Path=/')
                self.end_headers()
                self.wfile.write(json.dumps({'path': self.path}).encode())

        server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Recorder)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        source = (ROOT / 'quick/02-web-exploitation.md').read_text(encoding='utf-8')
        sections = {title: body for title, body in re.findall(r'^## Quick: ([^\n]+)\n(.*?)(?=^## |\Z)', source, re.M | re.S)}
        selected = ['check a candidate manually', 'replay a logged-in request',
                    'send form data or JSON', 'compare access to two objects',
                    'test one SQL parameter', 'test a filename parameter',
                    'test a template or command field', 'test server-side URL fetching',
                    'upload a harmless marker']
        try:
            with tempfile.TemporaryDirectory() as tmp:
                for title in selected:
                    for block in re.findall(r'^```bash\n(.*?)^```', sections[title], re.M | re.S):
                        block = block.replace('http://challenge.example', f'http://127.0.0.1:{server.server_port}')
                        result = subprocess.run(['bash', '-c', block], cwd=tmp, capture_output=True, text=True, timeout=20)
                        # diff uses 1 for differing bodies; every other block must succeed.
                        self.assertIn(result.returncode, (0, 1) if 'diff -u' in block else (0,), (title, result.stderr))
                self.assertEqual((Path(tmp) / 'marker.txt').read_text(), 'CTF_UPLOAD_MARKER\n')
            self.assertEqual(len(events), 14)
            by_path = {urlsplit(event['path']).path: event for event in events}
            self.assertEqual(by_path['/api/me']['headers']['Cookie'], 'session=PASTE_YOUR_COOKIE')
            self.assertEqual(by_path['/profile']['headers']['Cookie'], 'session=local-test')
            self.assertEqual(parse_qs(by_path['/login']['body'].decode()), {'username': ['YOUR_USERNAME'], 'password': ['YOUR_PASSWORD']})
            self.assertEqual(json.loads(by_path['/api/profile']['body']), {'display_name': 'test'})
            ids = [parse_qs(urlsplit(e['path']).query)['id'][0] for e in events if urlsplit(e['path']).path == '/item']
            self.assertEqual(ids, ['1 AND 1=1', '1 AND 1=2'])
            self.assertEqual(parse_qs(urlsplit(by_path['/download']['path']).query)['file'], ['../../../../etc/hostname'])
            self.assertEqual(parse_qs(urlsplit(by_path['/render']['path']).query)['name'], ['{{7*7}}'])
            self.assertEqual(parse_qs(by_path['/ping']['body'].decode())['host'], ['127.0.0.1;printf CTF_MARKER'])
            self.assertEqual(parse_qs(by_path['/preview']['body'].decode())['url'], ['http://ORGANIZER_CALLBACK_HOST/test'])
            self.assertIn(b'CTF_UPLOAD_MARKER', by_path['/upload']['body'])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
