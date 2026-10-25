"""Loopback-only synthetic web challenge. Reviewers must not inspect this file."""
import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def encode(value):
    return base64.urlsafe_b64encode(json.dumps(value).encode()).rstrip(b'=').decode()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/session':
            result={'token':encode({'alg':'HS256','typ':'JWT'})+'.'+encode({'sub':'practice','role':'user'})+'.invalid'}; status=200
        elif self.path=='/flag':
            try:
                token=self.headers.get('Authorization','').removeprefix('Bearer ')
                part=token.split('.')[1]
                claims=json.loads(base64.urlsafe_b64decode(part+'='*(-len(part)%4)))
            except Exception: claims={}
            result={'flag':'CTF{new_request_verified}'} if claims.get('role')=='admin' else {'error':'admin required'}
            status=200 if 'flag' in result else 403
        else: result={'error':'not found'};status=404
        body=json.dumps(result).encode()
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def log_message(self,*args): pass

print('Synthetic challenge listening at http://127.0.0.1:18766',flush=True)
HTTPServer(('127.0.0.1',18766),Handler).serve_forever()
