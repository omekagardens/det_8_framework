"""Root metadata-only review; certificate and scientific referents stay opaque."""
from pathlib import Path
import hashlib
import importlib.util
import sys

B = Path('/Volumes/AI_DATA/development/det-review-evidence')
D = B / 'ri196-root-pair-applicability-review-wurq10uo'
Q = B / 'ri197-manual-original-pair-proof-dh668vz_'
O = B / 'ri191-exact-pair-witness-source-uu414bjg'
helper = B / 'ri122-root-execution-review-6whn_vky/metadata.py'
assert hashlib.sha256(helper.read_bytes()).hexdigest() == 'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
spec = importlib.util.spec_from_file_location('metadata', helper)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D = D
handoff_pin = sys.argv[1]
assert hashlib.sha256((Q / 'HANDOFF.json').read_bytes()).hexdigest() == handoff_pin
h = m.load(Q / 'HANDOFF.json')
rows = h['payloads']
assert sorted(p.name for p in Q.iterdir()) == sorted(['HANDOFF.json'] + [Path(r['path']).name for r in rows])
fresh = {}
for row in rows:
    assert Path(row['path']).parent == Q
    fresh[row['path']] = m.verify(row['path'], row)
fresh[str(Q / 'HANDOFF.json')] = m.identity(Q / 'HANDOFF.json')
deps = m.load(Q / 'SOURCE_DEPENDENCIES.json')
old = m.load(O / 'SOURCE_DEPENDENCIES.json')
identities = m.load(Q / 'SOURCE_IDENTITIES.json')
old_identities = m.load(O / 'SOURCE_IDENTITIES.json')
selected = deps['protected_files']
by_path = {r['path']: r for r in selected}
assert len(by_path) == len(selected) == 423
assert len(old['protected_files']) == 389
for previous in old['protected_files']:
    current = by_path[previous['path']]
    assert {k: v for k, v in current.items() if k != 'role'} == {k: v for k, v in previous.items() if k != 'role'}
boundaries = [k for k in old if k not in ('schema', 'status', 'protected_files', 'scope')]
for key in boundaries:
    assert deps[key] == old[key]
assert identities['inherited_RI191_source_identities'] == old_identities
assert identities['unchanged_obligations'] == old_identities['unchanged_obligations']
assert identities['scope'] == deps['scope']
for row in selected:
    assert row['identity']['path'] == row['path']
    current = m.verify(row['path'], row['identity'])
    assert current['resolved_path'] == row['identity']['resolved_path']
    assert current['symlink_chain'] == row['identity']['symlinks']
    fresh[row['path']] = current
admission = m.load(D / 'RI197_MANUAL_BODY_ADMISSION.json')
certificate = admission['identity']
assert m.identity(certificate['path']) == certificate
assert deps['ri197_literal_certificate_exception']['path'] == certificate['path']
assert deps['ri197_literal_certificate_exception']['literal_read_only'] is True
assert deps['ri197_literal_certificate_exception']['automatic_scientific_JSON_parsing'] is False
assert deps['ri197_literal_certificate_exception']['automated_typed_reference_expansion'] is False
for p, row in fresh.items():
    assert m.identity(p) == row
report = dict(
    schema='ri197-root-bounded-metadata-check-v1', status='PASS',
    subject=m.ref(Q / 'HANDOFF.json'), checker=m.ref(Path(__file__)),
    selected_dependencies=len(selected), inherited_rows=389,
    inherited_boundary_objects=boundaries,
    whole_inherited_source_identity_object_equal=True,
    unchanged_obligations_equal=True,
    subject_namespace_files=len(rows) + 1,
    fresh_identity_count=len(fresh), fresh_identities=list(fresh.values()),
    historical_stat_compared_to_current=False,
    scientific_json_decoded=False, mathematical_formula_evaluated=False,
    manual_proof_review_separate=True,
)
print(m.save('RI197_ROOT_METADATA_CHECK.json', report))
