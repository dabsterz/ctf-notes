"""Parent-only independent answer/evidence and score checks after reviewers finish."""
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parents[1]/'usability-tests/round-2'
key=json.loads((ROOT/'answer-key.json').read_text(encoding='utf-8-sig'))
weights=dict(findability=.25,command_readiness=.25,interpretation=.15,cognitive_load=.25,tool_environment=.10)
results=[];seen=set()
for name in ('web-crypto','forensics','reverse-misc'):
    report=json.loads((ROOT/'reports'/f'{name}.json').read_text(encoding='utf-8-sig'))
    assert set(report['dimensions'])==set(weights)
    assert all(1<=score<=5 for score in report['dimensions'].values())
    calculated=round(2*sum(report['dimensions'][k]*w for k,w in weights.items()),2)
    assert calculated==report['overall_10']
    for task in report['tasks']:
        assert task['id'] not in seen
        seen.add(task['id'])
        assert str(task['candidate'])==key[task['id']],task
        assert task['status']=='completed',task
    results.append(dict(reviewer=name,overall_10=calculated,study_10=report['study_10'],lookup_count=report['lookup_count'],completed=len(report['tasks'])))
assert seen==set(key)
outputs={'rsa':'web-crypto/rsa-plain.bin','layers':'web-crypto/decoded/layer2.bin',
         'png':'forensics/png-trailer.bin','tar':'forensics/tar-parts/000000.bin',
         'checker':'reverse-misc/checker-plain.bin'}
for task,path in outputs.items():assert (ROOT/path).read_bytes()==key[task].encode(),path
assert (ROOT/'forensics/tar-parts/000001.bin').read_bytes()!=key['tar'].encode()
pattern=(ROOT/'reverse-misc/pattern.bin').read_bytes();crash=(ROOT/'reverse-misc/crash.bin').read_bytes()
offset=int(key['offset']);assert len(pattern)==512 and pattern[offset:offset+4]==crash
event=json.loads((ROOT/'forensics/events.json').read_text(encoding='utf-8-sig'))
assert event['TimeCreated']+' | '+event['CommandLine']==key['event']
assert event['Provider']=='Microsoft-Windows-Security-Auditing' and event['EventID']==4688
checker=json.loads((ROOT/'reverse-misc/checker.json').read_text(encoding='utf-8-sig'))
secret=bytes.fromhex(checker['key_hex']);r=checker['rotation']
forward=[]
for i,x in enumerate(key['checker'].encode()):
    y=x^secret[i%len(secret)];forward.append(((y<<r)|(y>>(8-r)))&255)
assert forward==checker['expected']
assert ((ord(key['vm'])^18)+9)&255==81
rsa=json.loads((ROOT/'web-crypto/rsa.json').read_text(encoding='utf-8-sig'))
assert pow(int.from_bytes(key['rsa'].encode(),'big'),rsa['e'],rsa['n'])==rsa['c']
http=[]
for name,expected_status in [('token.txt',403),('edited-token.txt',200)]:
    token=(ROOT/'web-crypto'/name).read_text(encoding='utf-8-sig').strip()
    request=urllib.request.Request('http://127.0.0.1:18766/flag',headers={'Authorization':'Bearer '+token})
    try:
        response=urllib.request.urlopen(request,timeout=5)
    except urllib.error.HTTPError as error:
        response=error
    with response:
        status=response.status;data=json.load(response)
    assert status==expected_status
    if status==200:assert data['flag']==key['web']
    http.append(dict(token=name,status=status))
result=dict(reviewers=results,candidates_verified=9,fully_completed=9,
            mean_contest_score=round(sum(r['overall_10'] for r in results)/3,2),
            extracted_files_checked=list(outputs),independent_checks=['checker forward arithmetic','RSA re-encryption','VM byte arithmetic','crash slice','event fields','duplicate preservation'],loopback_http=http,
            caveat='Synthetic clue-rich tasks and simulated reviewers; descriptive ratings, not population estimates or real human speed measurements.')
(ROOT/'verified-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
