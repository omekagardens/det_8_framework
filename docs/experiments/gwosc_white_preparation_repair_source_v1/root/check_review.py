"""Root opaque-file and literal-text reconciliation; never loads subject code."""
import importlib.util
from pathlib import Path
import difflib
import re

sp = importlib.util.spec_from_file_location('metadata', '/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m = importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
m.D = Path(__file__).resolve().parent
S = m.B / 'ri135-white-preparation-repair-source-lski1ize'
R = m.B / 'ri135-preparation-repair-independent-review-0ysy6sdb'
P = m.B / 'ri133-white-runtime-preparation-source-lrck33ys'

def sealed(base, size, digest, field):
    handoff = m.verify(base/'HANDOFF.json', dict(bytes=size, sha256=digest))
    h = m.load(base/'HANDOFF.json')
    rows = [m.verify(x['path'], x) for x in h[field]] + [handoff]
    assert sorted(str(x) for x in base.iterdir()) == sorted(x['path'] for x in rows)
    assert all(not x['symlink_chain'] for x in rows)
    return rows

source = sealed(S, 5902, '4291a055c4cc125d4a07fe6be4fec0e0c5945dc31225cc4bda079fce84824b1d', 'artifacts')
review = sealed(R, 2187, 'bd035e6017edf7c15b6c2f33e4519d8a43c66da00a9dd862fb50bb1a6dfd5d8e', 'files')
predecessor = sealed(P, 5719, '480188c24c2b4a0062e7a1b882d8a11eb1f7786c987224d23d22ece22927be59', 'artifacts')
d = m.load(S/'DEPENDENCIES.source-only.json')
old = m.load(P/'DEPENDENCIES.source-only.json')
deps = [m.verify(x['path'], x) for x in d['opaque_files']]
assert len(deps) == len({x['path'] for x in deps}) == 253
assert sum(x['bytes'] for x in deps) == 16220282
index = {x['path']: x for x in d['opaque_files']}
assert len(old['opaque_files']) == 228
assert all(index[x['path']] == x for x in old['opaque_files'])
additions = [x for x in d['opaque_files'] if x['path'] not in {v['path'] for v in old['opaque_files']}]
assert len(additions) == 25
for field in ('historical_optional_namespaces', 'historical_runtime', 'packet_handoff', 'packet_namespace', 'packet_root', 'root_adjudication', 'status'):
    assert d[field] == old[field], field
historic = d['historical_interpreter']
provenance = d['historical_interpreter_provenance']
assert index[historic['path']] == historic and index[provenance['path']] == provenance
h = m.load(provenance['path'])
assert h['schema'] == 'ri121-reviewed-runtime-metadata-candidate-handoff-v1'
assert h['status'] == 'METADATA_CANDIDATE_INDEPENDENTLY_VERIFIED_NOT_RUNTIME_ADMITTED'
assert [x for x in h['files'] if x['path'] == historic['path']] == [historic]
binding = m.load(historic['path'])
assert len(binding['symlink_chain']) == 4

def spans(text):
    lines = text.splitlines(keepends=True)
    starts = [(i, re.match(r'def (\w+)\(', s).group(1)) for i, s in enumerate(lines) if re.match(r'def \w+\(', s)]
    return {name: ''.join(lines[i:starts[n+1][0] if n+1 < len(starts) else len(lines)]).rstrip() for n, (i, name) in enumerate(starts)}

c = m.load(S/'SOURCE_CORRESPONDENCE.json')
same_functions = []; changed = []; patch = ''
for row in c['changed_modules']:
    name = row['module']; a = (P/name).read_text(); b = (S/name).read_text()
    m.verify(row['old']['path'], row['old']); m.verify(row['new']['path'], row['new'])
    aa = spans(a); bb = spans(b)
    same = sorted(x for x in aa if x in bb and aa[x] == bb[x])
    changed_names = sorted(x for x in aa if x in bb and aa[x] != bb[x])
    added = sorted(set(bb)-set(aa))
    assert same == row['unchanged_functions']
    assert sorted(changed_names+added) == sorted(row['changed_top_level_text_ranges'])
    same_functions.extend(dict(module=name, name=x, **m.pin(aa[x].encode())) for x in same)
    changed.append(dict(module=name, changed=changed_names, added=added))
    patch += ''.join(difflib.unified_diff(a.splitlines(keepends=True), b.splitlines(keepends=True), fromfile=str(P/name), tofile=str(S/name)))
assert patch == (S/'REPAIR.diff').read_text()
assert len(same_functions) == 42
a = (P/'prepare.py').read_text(); b = (S/'prepare.py').read_text(); retained = []
for start, end in [('GUARD_IDS = ', 'BOUNDS = '), ('BOUNDS = ', 'M = None')]:
    aa = a[a.index(start):a.index(end)].rstrip(); bb = b[b.index(start):b.index(end)].rstrip()
    assert aa == bb
    retained.append(dict(start=start, **m.pin(bb.encode())))
control = (S/'fault_controls.source-only.py').read_text()
groups = {
    'F01': ['positive', 'pre_admission_read', 'occupied', 'mkdir', 'post_admission_read', 'initial_source_read', 'attempt_open', 'attempt_partial', 'secondary_post', 'secondary_source', 'secondary_namespace', 'secondary_checks', 'three_secondary', 'final_partial'],
    'F02': ['positive', 'named_path', 'resolved_path', 'link_literal', 'link_order', 'link_omitted', 'target_bytes', 'target_sha', 'provenance_missing', 'snapshot_alias', 'snapshot_target'],
}
ids = []
for label, wanted in groups.items():
    literal = control.split(label+' = (', 1)[1].split(')\n', 1)[0]
    assert re.findall(r"'([^']+)'", literal) == wanted
    ids += [label+'_'+x for x in wanted]
assert len(ids) == 25
review_json = m.load(R/'INDEPENDENT_SOURCE_REVIEW.json')
assert review_json['status'] == 'PASS_BOUNDED_UNEXECUTED_SOURCE_ONLY'
assert review_json['blocking_findings'] == []
assert review_json['execution_authorized'] is False
assert review_json['subject_authorship'] is False
assert review_json['controls']['executed'] == 0
assert sum(len((S/x).read_text().splitlines()) for x in ('prepare.py', 'runtime_metadata.py', 'fault_controls.source-only.py')) == 1365
for row in source+review+predecessor+deps:
    assert m.identity(row['path']) == row
print(m.save('ROOT_REVIEW_RECONCILIATION.json', dict(
    schema='ri135-root-source-reconciliation-v1', status='PASS_OPAQUE_AND_LITERAL_ONLY',
    checker=m.ref(__file__), source=source, review=review, predecessor=predecessor,
    dependencies=deps, inherited=228, additions=additions, dependency_count=253,
    dependency_bytes=16220282, exact_source_namespace=12, exact_review_namespace=6,
    unchanged_functions=same_functions, changed_functions=changed, full_patch_identical=True,
    unchanged_bounds_and_guard_literals=retained, ordered_focused_controls=ids,
    authentic_historical_interpreter=historic, authentic_provenance=provenance,
    source_and_dependency_full_identities_unchanged_after=True,
    historical_binding_link_count=4, current_runtime_observed=False,
    target_syntax_or_execution=False, scientific_body_decode=False,
    fixture_execution=False, independent_full_1365_line_review=review_json['full_review'],
    root_scope='Independent identities, two-module delta, 42 retained functions, bounds and 25 literal IDs; root manual repair/control-path reading. Full RI130 namespace/pair/history walk belongs to the separate nonauthor review.'
)))
