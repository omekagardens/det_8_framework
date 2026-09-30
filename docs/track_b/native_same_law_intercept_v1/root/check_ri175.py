"""Independent bounded metadata replay, without mathematical execution."""
import hashlib
import importlib.util
from pathlib import Path

D = Path(__file__).parent
B = D.parent
hp = B / 'ri122-root-execution-review-6whn_vky/metadata.py'
raw = hp.read_bytes()
assert len(raw) == 3144 and hashlib.sha256(raw).hexdigest() == 'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
spec = importlib.util.spec_from_file_location('m', hp)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D = D
S = B / 'ri175-same-law-intercept-91oc0806'
P = B / 'ri173-same-law-endpoint-slope-ckec5j02'
m.verify(S / 'HANDOFF.json', dict(bytes=6328, sha256='3722b5a1fbd550f398be2b732d7ea0d99d12e69742e17583f07ef7ebb3eb8557'))
h = m.load(S / 'HANDOFF.json')
assert len(h['payloads']) == 7
assert sorted(p.name for p in S.iterdir()) == sorted(h['namespace']) == sorted(['HANDOFF.json'] + [Path(r['path']).name for r in h['payloads']])
identities = [m.identity(S / 'HANDOFF.json')] + [m.verify(r['path'], r) for r in h['payloads']]
d = m.load(S / 'SOURCE_DEPENDENCIES.json')
s = m.load(S / 'SOURCE_IDENTITIES.json')
by = {r['path']: r for r in d['protected_files']}
assert len(by) == 313 and list(by) == sorted(by)
for i, r in enumerate(by.values(), 1):
    assert r['role'] == 'dep_' + str(i).zfill(4) and r['path'] == r['identity']['path']
    identities.append(m.verify(r['path'], r['identity']))
assert sum(r['identity']['bytes'] for r in by.values()) == 18978311
old = m.load(P / 'SOURCE_DEPENDENCIES.json')
old_s = m.load(P / 'SOURCE_IDENTITIES.json')
omit = lambda r: {k: v for k, v in r.items() if k != 'role'}
assert len(old['protected_files']) == 300
for r in old['protected_files']:
    assert omit(r) == omit(by[r['path']])
for key in ('governance_stopping_boundary', 'historical_phase_record_boundary', 'predecessor_author_support_boundary', 'ri172_author_support_boundary'):
    assert d[key] == old[key]
for key in ('accepted_ri172_predecessor', 'accepted_ri168_premises', 'accepted_ri166_premises', 'accepted_ri157_premises', 'accepted_ri157_margin_scope', 'accepted_ri155_premises', 'accepted_ri153_premises', 'excluded_historical_inferences', 'accepted_ri151_premises', 'accepted_ri149_premises', 'root_accepted_additional_observation', 'accepted_ri147_premises', 'accepted_ri145_premises', 'accepted_analytic_packets', 'premise_texts', 'actual_source_text_reads', 'source_text_counterparts', 'immutable_numerical_certificate', 'unchanged_obligations', 'inherited_scope_clarification', 'identity_interpretation'):
    assert s[key] == old_s[key]
old_h = m.load(P / 'HANDOFF.json')
assert sorted(p.name for p in P.iterdir()) == sorted(old_h['namespace']) and len(old_h['namespace']) == 8
for r in old_h['payloads']:
    m.verify(r['path'], r)
refs = states = 0
def scan(value, current=False):
    global refs, states
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and type(value.get('bytes')) is int and isinstance(value.get('sha256'), str):
            assert value['path'] in by or (current and value['path'] == str(S / 'SOURCE_DEPENDENCIES.json'))
            found = m.verify(value['path'], value)
            if 'resolved_path' in value:
                assert found['resolved_path'] == value['resolved_path']
            if 'symlink_chain' in value:
                assert found['symlink_chain'] == value['symlink_chain']
            if 'symlinks' in value:
                assert found['symlink_chain'] == value['symlinks'] == []
            refs += 1
            states += int('state' in value)
        for child in value.values():
            scan(child, current)
    elif isinstance(value, list):
        for child in value:
            scan(child, current)
classes = {}
for r in by.values():
    cl = r['classification']
    classes[cl] = classes.get(cl, 0) + 1
    if cl == 'selected-administrative-proof-provenance':
        scan(m.load(r['path']))
assert classes == {'analytic-source-text-or-review':112, 'opaque-historical-acceptance-or-source-support':87, 'opaque-scientific-historical-premise':1, 'selected-administrative-proof-provenance':112, 'selected-administrative-governance-boundary':1}
assert refs == 3634 and states == 17
historical_refs = refs
refs = states = 0
scan(s, True)
assert refs == 157
decision = str(B / 'ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json')
scope = str(B / 'ri174-root-preparation-review-wm18ymsq/RI175_HISTORICAL_PREMISE_SCOPE.json')
exception = d['ri122_literal_read_exception']
assert exception['path'] == decision and exception['literal_read_authority'] == scope and exception['automated_typed_reference_expansion'] is False
assert by[decision]['classification'] == 'opaque-historical-acceptance-or-source-support'
assert s['historical_fixed_prefix_premise']['permission']['path'] == scope
assert s['historical_fixed_prefix_premise']['final_acceptance']['path'] == decision
assert s['historical_fixed_prefix_premise']['final_decision_automated_typed_reference_expansion'] is False
for key, row in s['source_text_counterparts']['published'].items():
    assert Path(row['path']).read_bytes() == Path(s['premise_texts'][key]['path']).read_bytes()
assert len(s['source_text_counterparts']['published']) == 4
assert len(identities) == 321
for row in identities:
    assert row['resolved_path'] == row['path'] and row['symlink_chain'] == []
    assert m.identity(row['path']) == row
assert sorted(p.name for p in S.iterdir()) == sorted(h['namespace'])
assert sorted(p.name for p in P.iterdir()) == sorted(old_h['namespace'])
print(m.save('RI175_ROOT_METADATA_CHECK.json', dict(status='PASS_FINITE_PROVENANCE_ONLY', identities=identities, selected_dependencies=313, selected_dependency_bytes=18978311, inherited_rows=300, historical_typed_references=historical_refs, current_typed_references=refs, historical_extended_state_noncomparisons=17, separate_byte_equal_pairs=4, current_whole_state_rechecks=321, scientific_body_decode=False, scientific_formula_execution=False, author_reported_final_receipt='ac9392')))
