"""Parent-only checks after the independent reviews are complete."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
key = json.loads((ROOT / 'answer-key.json').read_text(encoding='utf-8-sig'))
weights = dict(findability=.25, command_readiness=.25, interpretation=.15,
               cognitive_load=.25, tool_environment=.10)
seen = set()
results = []
for name in ('web-crypto', 'forensics', 'reverse-misc'):
    report = json.loads((ROOT / 'reports' / (name + '.json')).read_text(encoding='utf-8-sig'))
    assert set(report['dimensions']) == set(weights)
    assert all(1 <= x <= 5 for x in report['dimensions'].values())
    score = round(2 * sum(report['dimensions'][d] * w for d, w in weights.items()), 2)
    assert score == report['overall_10'], (name, score)
    tasks = []
    for task in report['tasks']:
        task_id = task['id']
        assert task_id not in seen
        seen.add(task_id)
        candidate = task['candidate']
        # VM reviewer reports the byte in decimal; key records its ASCII character.
        if task_id == 'vm':
            candidate = chr(int(candidate))
        assert candidate == key[task_id]['expected'], task_id
        tasks.append(dict(id=task_id, candidate_matches=True, status=task['status']))
    assert report['common_lookup']['radare2_environment'] == 'Kali'
    assert 'Ghidra' in report['common_lookup']['alternative']
    assert 'WSL' in report['common_lookup']['alternative']
    results.append(dict(reviewer=name, overall_10=score,
                        study_10=report['study_10'], tasks=tasks))
assert seen == set(key)

artifacts = {
    'rsa': 'web-crypto/rsa-plaintext.bin',
    'layers': 'web-crypto/layer2.bin',
    'png': 'forensics/png-parts/trailer.bin',
    'tar': 'forensics/out/tar-members/000000.bin',
}
for task_id, path in artifacts.items():
    assert (ROOT / path).read_bytes().strip() == key[task_id]['expected'].encode(), path
pattern = (ROOT / 'reverse-misc/pattern.bin').read_bytes()
crash = (ROOT / 'reverse-misc/crash.bin').read_bytes()
assert len(pattern) == 512
assert pattern[173:177] == crash
output = dict(reviewers=results, exact_candidates=9,
              complete=8, partial=1, common_lookups_correct=3,
              mean_contest_score=round(sum(r['overall_10'] for r in results)/3, 2),
              binary_artifact_checks=list(artifacts), pattern_slice_verified=True,
              note='VM decimal 75 normalized to ASCII K. Partial event interpretation remains partial.')
(ROOT / 'verified-results.json').write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
print(json.dumps(output, indent=2))
