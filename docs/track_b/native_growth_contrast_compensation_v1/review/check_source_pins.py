"""RI124 opaque metadata checks only; never import or execute scientific sources."""
import hashlib
import json
from pathlib import Path

E = Path('/Volumes/AI_DATA/development/det-review-evidence/ri124-compensation-support-UjbAZpTk')
O = Path('/Volumes/AI_DATA/development/det-review-evidence/ri124-independent-proof-review-hZW9Bs5Z')

def pin(path):
    data = Path(path).read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

handoff_ref = {'path': str(E / 'HANDOFF.json'), 'bytes': 6468, 'sha256': 'a883a826a25f0fce18876e028fced6e40f7359c9b5e46098046fc13c5c15227e'}
refs = [('assigned handoff', handoff_ref)]
# Only these source-identity metadata objects are decoded; scientific bodies are opaque.
for name in ('HANDOFF.json', 'SOURCES.json', 'SUPPORT_SOURCE_IDENTITIES.json'):
    obj = json.loads((E / name).read_text())
    def visit(value, location):
        if isinstance(value, dict):
            if all(k in value for k in ('path', 'bytes', 'sha256')):
                refs.append((location, {k: value[k] for k in ('path', 'bytes', 'sha256')}))
            for key, child in value.items():
                visit(child, location + '.' + key)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, location + '[' + str(index) + ']')
    visit(obj, name)
checks = []
for role, expected in refs:
    observed = pin(expected['path'])
    checks.append({'role': role, 'expected': expected, 'observed': observed, 'matches': observed == expected})
extra_reads = [
    '/Volumes/AI_DATA/development/det-review-evidence/ri117-coupled-positive-family-QrAaK5YQ/CONNECTED_CONSTRAINTS_LEMMA.md',
    '/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/ROOT_QUADRATIC_POSITIVITY_REVIEW.json',
    '/Volumes/AI_DATA/development/det-review-evidence/ri122-saved-math-review-TlZje57F/SOURCE_OBLIGATIONS_REVIEW.md',
]
report = {
    'schema': 'ri124-independent-opaque-source-pin-check-v1',
    'status': 'PASS_OPAQUE_SOURCE_IDENTITIES' if all(x['matches'] for x in checks) else 'FAIL_OPAQUE_SOURCE_IDENTITIES',
    'scope': 'Whole-file length/hash comparisons of declared metadata references only; no mathematical computation or scientific source execution.',
    'declared_reference_occurrences': len(checks),
    'distinct_declared_paths': len({x['expected']['path'] for x in checks}),
    'checks': checks,
    'additional_textually_read_source_identities': [pin(p) for p in extra_reads],
    'all_match': all(x['matches'] for x in checks),
    'target_or_helper_execution': False,
    'scientific_arithmetic_execution': False,
    'repository_or_git_mutation': False,
}
with (O / 'SOURCE_PIN_CHECK.json').open('x') as out:
    out.write(json.dumps(report, indent=2, sort_keys=True) + '\n')
print(json.dumps({'status': report['status'], 'occurrences': len(checks), 'distinct_paths': report['distinct_declared_paths'], 'report': pin(O / 'SOURCE_PIN_CHECK.json')}))
if not report['all_match']:
    raise SystemExit(1)
