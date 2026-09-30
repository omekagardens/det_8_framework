"""RI157 independent bounded provenance check; no scientific operand decoding."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re

R = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-independent-cap-review-wt1tl1ip')
Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-correlated-capacity-proof-tusjyk77')
P = Path('/Volumes/AI_DATA/development/det-review-evidence/ri155-strict-capacity-proof-jv0xliup')
V = Path('/Volumes/AI_DATA/development/det-review-evidence/ri155-independent-capacity-review-3gu50gvs')
ROOT = Path('/Volumes/AI_DATA/development/det-review-evidence/ri155-root-capacity-review-0f1typdz')
ASSIGN = Path('/Volumes/AI_DATA/development/det-review-evidence/ri157-root-review-jco7p6tf/NATIVE_REVIEW_ASSIGNMENT.json')
HELPER = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
body = HELPER.read_bytes()
if len(body) != 3144 or hashlib.sha256(body).hexdigest() != 'd2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':
    raise ValueError('trusted administrative helper pin differs')
spec = importlib.util.spec_from_file_location('ri157_trusted_metadata', HELPER)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.D = R
checks = []
observed = {}
refs = []
extended = []

def require(ok, label):
    if not ok:
        raise ValueError(label)
    checks.append(label)

def typed_equal(a, b):
    return json.dumps(a, sort_keys=True, allow_nan=False) == json.dumps(b, sort_keys=True, allow_nan=False)

def identity(path):
    path = str(path)
    require(Path(path).is_absolute() and os.path.normpath(path) == path, 'canonical absolute path: ' + path)
    if path not in observed:
        observed[path] = m.identity(path)
    require(observed[path]['bytes'] <= 67108864, 'bounded opaque file: ' + path)
    require(observed[path]['resolved_path'] == path and observed[path]['symlink_chain'] == [], 'literal unlinked identity: ' + path)
    return observed[path]

def pin(row, context):
    require(type(row) is dict and type(row.get('path')) is str and type(row.get('bytes')) is int and row['bytes'] >= 0 and type(row.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']) is not None, 'typed identity: ' + context)
    actual = identity(row['path'])
    require(m.pure(actual) == m.pure(row), 'byte pin: ' + context)
    for k in ('resolved_path', 'symlinks', 'symlink_chain'):
        if k in row:
            expected = actual['symlink_chain'] if k == 'symlinks' else actual[k]
            require(typed_equal(row[k], expected), 'identity field ' + k + ': ' + context)
    return actual

def admin(path):
    """Only called with current administrative files or classification-allowlisted paths."""
    path = str(path)
    before = identity(path)
    data = Path(path).read_bytes()
    require(m.pin(data) == m.pure(before), 'administrative read bound to identity: ' + path)
    def closed_pairs(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError('duplicate administrative key: ' + path)
            out[k] = v
        return out
    return json.loads(data, object_pairs_hook=closed_pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError('nonfinite metadata')))

pin(dict(path=str(ASSIGN), bytes=1764, sha256='8a007487ce1abb1c57a41cdc222327a8bf2e31ce4107dad8e85c22a7d55d2269'), 'assignment')
pin(dict(path=str(Q/'HANDOFF.json'), bytes=10114, sha256='968e3c853ce107aceff080126b8ca22f8ba846bbba914ff0b13a32360c660b8c'), 'subject handoff')
assignment = admin(ASSIGN)
H = admin(Q/'HANDOFF.json')
expected_names = ['ANALYTIC_RESULT.json','AUTHOR_CHECKS.json','CANONICAL_CAP_BOUND.md','CORRELATED_CAPACITY_SYNTHESIS.md','CORRELATED_CONTRAST_BOUND.md','DEPENDENCY_NOTES.md','HANDOFF.json','HANDOFF.md','SOURCE_DEPENDENCIES.json','SOURCE_IDENTITIES.json']
require(sorted(H['namespace']) == expected_names and sorted(x.name for x in Q.iterdir()) == expected_names, 'exact current ten-file namespace')
require(len(H['payloads']) == 9 and sorted(Path(x['path']).name for x in H['payloads']) == [n for n in expected_names if n != 'HANDOFF.json'], 'complete current nine-payload coverage')
for x in H['payloads']:
    require(Path(x['path']).parent == Q, 'subject payload own directory: ' + x['path'])
    pin(x, 'current payload')
D = admin(Q/'SOURCE_DEPENDENCIES.json')
S = admin(Q/'SOURCE_IDENTITIES.json')
rows = D['protected_files']
require(len(rows) == 223, 'exact 223 selected dependencies')
index = {r['path']: r for r in rows}
require(len(index) == 223 and list(index) == sorted(index), 'unique ordered literal dependencies')
classes = {}
policies = {
 'analytic-source-text-or-review': 'text-reading-and-opaque-identity-no-execution',
 'selected-administrative-proof-provenance': 'metadata-identities-only-no-scientific-body-decoding',
 'opaque-historical-acceptance-or-source-support': 'opaque-bytes-only-no-recursive-reference-expansion',
 'opaque-scientific-historical-premise': 'opaque-bytes-only-no-scientific-body-decoding'}
for n, r in enumerate(rows, 1):
    require(set(r) == {'role','path','identity','classification','access_policy','reference_provenance'}, 'closed dependency row: ' + r['path'])
    require(r['role'] == 'dep_%04d' % n and r['identity']['path'] == r['path'], 'role and path: ' + r['path'])
    require(set(r['identity']) == {'path','resolved_path','bytes','sha256','symlinks'}, 'closed manifest identity: ' + r['path'])
    require(r['classification'] in policies and r['access_policy'] == policies[r['classification']], 'access boundary: ' + r['path'])
    classes[r['classification']] = classes.get(r['classification'], 0) + 1
    pin(r['identity'], r['path'])
require(classes == {'analytic-source-text-or-review':83, 'selected-administrative-proof-provenance':77, 'opaque-historical-acceptance-or-source-support':62, 'opaque-scientific-historical-premise':1}, 'exact classification counts')
require(sum(r['identity']['bytes'] for r in rows) == 9791698, 'selected byte total')
old = admin(P/'SOURCE_DEPENDENCIES.json')['protected_files']
require(len(old) == 193, '193 predecessor rows')
without_role = lambda r: {k:v for k,v in r.items() if k != 'role'}
for r in old:
    require(r['path'] in index and typed_equal(without_role(r), without_role(index[r['path']])), 'entire inherited row except role: ' + r['path'])
old_paths = {r['path'] for r in old}
new_paths = set(index) - old_paths
additions = {str(P/n) for n in expected_names if n not in ['CANONICAL_CAP_BOUND.md','CORRELATED_CAPACITY_SYNTHESIS.md','CORRELATED_CONTRAST_BOUND.md']}
# Both predecessor seals below supply complete packet names, avoiding a guessed file list.
additions = set()
for directory in (P, V):
    h = admin(directory/'HANDOFF.json')
    names = sorted(x.name for x in directory.iterdir())
    require(names == sorted(h['namespace']) and len(names) == 10, 'complete predecessor namespace: ' + str(directory))
    require(sorted(Path(x['path']).name for x in h['payloads']) == [n for n in names if n != 'HANDOFF.json'], 'predecessor payload coverage: ' + str(directory))
    for x in h['payloads']:
        require(Path(x['path']).parent == directory, 'predecessor own path: ' + x['path'])
        pin(x, 'predecessor seal')
    additions.update(str(directory/n) for n in names)
additions.update(str(ROOT/n) for n in ('NATIVE_SUCCESSOR_ASSIGNMENT.json','RI155_ROOT_ADJUDICATION.json','ROOT_MANUAL_REVIEW.md','ROOT_METADATA_REPLAY.json','adjudicate_native.py','check_native.py','METADATA_CHECK.json','RI157_GRID_PREMISE_CLARIFICATION.json'))
additions.update(('/Volumes/AI_DATA/development/det-review-evidence/ri154-root-relocation-review-3sgyua6i/NATIVE_REVIEW_ASSIGNMENT.json','/Volumes/AI_DATA/development/det_8_framework-ret/docs/track_b/native_joint_growth_extension_v1/EXTENSION.md'))
require(len(additions) == 30 and new_paths == additions, 'exact thirty current additions')

def scan(value, origin, trail='$'):
    if type(value) is dict:
        if all(k in value for k in ('path','bytes','sha256')):
            path = value['path']
            require(type(path) is str and (path in index or path == str(Q/'SOURCE_DEPENDENCIES.json')), 'closed typed reference: ' + origin + trail)
            pin(value, origin + trail)
            refs.append(dict(origin=origin, pointer=trail, path=path))
            if 'state' in value and 'symlink_chain' in value:
                require(type(value['state']) is list and len(value['state']) == 7 and all(type(v) is int for v in value['state']), 'historical seven-field state: ' + origin + trail)
                extended.append(dict(origin=origin, pointer=trail, path=path, historical_state_preserved_not_current=True))
        for k,v in value.items():
            scan(v, origin, trail + '/' + k)
    elif type(value) is list:
        for n,v in enumerate(value):
            scan(v, origin, trail + '/' + str(n))

allowed = [r['path'] for r in rows if r['classification'] == 'selected-administrative-proof-provenance']
for path in allowed:
    scan(admin(path), path)
require(len(refs) == 1616 and len(extended) == 17, '1616 historical typed references and seventeen historical states')
historical_count = len(refs)
scan(S, str(Q/'SOURCE_IDENTITIES.json'))
require(len(refs) - historical_count == 89 and len(extended) == 17, '89 current premise references')
pairs = []
for key, x in S['source_text_counterparts']['published'].items():
    y = S['premise_texts'][key]
    require(x['path'] in index and y['path'] in index and x['path'] != y['path'], 'distinct selected counterpart paths: ' + key)
    require(Path(x['path']).read_bytes() == Path(y['path']).read_bytes(), 'full byte counterpart equality: ' + key)
    pairs.append(dict(key=key, published=x, external=y))
require(len(pairs) == 4, 'four complete source pairs')
source_references = []
for name in ('CORRELATED_CAPACITY_SYNTHESIS.md','CANONICAL_CAP_BOUND.md','CORRELATED_CONTRAST_BOUND.md'):
    text = (Q/name).read_text()
    require(re.search(r'^(<{7}|={7}|>{7})( |$)', text, re.M) is None, 'no conflict markers: ' + name)
    require(re.search(r'[ \t]+$', text, re.M) is None, 'no trailing whitespace: ' + name)
    for path in re.findall(r'`(/Volumes/[^` \n]+\.(?:md|json|py))`', text):
        require(path in index or (Path(path).parent == Q and Path(path).name in expected_names), 'literal manuscript reference: ' + path)
        source_references.append(dict(manuscript=name, path=path))
require(len(source_references) == 6, 'six literal manuscript references')
A = admin(Q/'ANALYTIC_RESULT.json')
C = admin(Q/'AUTHOR_CHECKS.json')
for key in ('actual_v_greater_than_B_proved','actual_v_less_equal_B_proved','actual_joint_capacities_proved','actual_adequate_q_v_joint_budget_proved','actual_W_C2_C3_signs_decided','actual_rho_in_delta0_proved','full_H30_decided','grid_premise_accepted','grid_premise_used','actual_individual_root_order_decided','actual_positive_part_branch_decided'):
    require(A[key] is False and H[key] is False, 'retained open boundary: ' + key)
require(A['actual_canonical_cap_branch_proved'] is True and H['actual_canonical_cap_branch_proved'] is True, 'new cap claim is declared only')
require(C['preseal_check']['command_chunk'] == 'a7e617' and C['preseal_check']['exit_code'] == 0 and C['preseal_check']['receipt']['stage'] == 'preseal8' and len(C['preseal_check']['receipt']['current_payloads']) == 8, 'actual author preseal scope retained')
require(C['diagnostics']['failed_main_commands'] == [] and C['diagnostics']['failed_coauthor_commands_reported'] == [], 'author disclosed failures empty, not independent execution assertion')
require(admin(ROOT/'RI157_GRID_PREMISE_CLARIFICATION.json')['reading']['exit_code'] == 1, 'historical failed root read remains retained')
for path, before in list(observed.items()):
    require(typed_equal(m.identity(path), before), 'final fresh identity unchanged: ' + path)
require(len(observed) == 234, '234 complete final identity rechecks')
report = dict(schema='ri157-independent-administrative-check-v1', status='PASS_ADMINISTRATIVE_IDENTITIES_NOT_PROOF_OR_EXECUTION_ACCEPTANCE',
 predicates=len(checks), dependencies=223, selected_bytes=9791698, inherited_rows=193, exact_additions=sorted(additions), administrative_bodies=77,
 historical_typed_references=1616, current_typed_references=89, historical_extended_identities=extended,
 historical_state_compared_to_current=False, source_pairs=pairs, literal_source_references=source_references, final_fresh_identities=234,
 subject_namespace=expected_names, subject_handoff=m.ref(Q/'HANDOFF.json'), assignment=m.ref(ASSIGN), trusted_helper=m.ref(HELPER),
 class_counts=classes, predicates_completed=checks, observed_identities=list(observed.values()), typed_reference_occurrences=refs,
 scope=dict(scientific_decode=False, target_execution=False, engine=False, current_runtime_or_card=False, coefficient_or_scale_evaluation=False, repository_write=False, mathematical_checks='manual review only'))
ref = m.save('METADATA_CHECK.json', report)
print(json.dumps({k:report[k] for k in ('status','predicates','dependencies','selected_bytes','inherited_rows','administrative_bodies','historical_typed_references','current_typed_references','final_fresh_identities')}, sort_keys=True))
print(json.dumps(ref, sort_keys=True))
