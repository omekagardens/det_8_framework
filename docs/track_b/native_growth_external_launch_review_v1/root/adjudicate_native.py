"""Root text/metadata reconciliation of RI138; no subject loading or execution."""
import importlib.util
from pathlib import Path

s = importlib.util.spec_from_file_location('metadata', '/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
m.D = Path(__file__).resolve().parent
Q = m.B/'ri138-native-external-launch-source-92pbd52w'
R = m.B/'ri138-launch-independent-review-6xGu5oak'
OLD = m.B/'ri136-native-policy-dispatch-source-g_z472z7'

def packet(root):
    handoff = m.load(root/'HANDOFF.json')
    names = ['HANDOFF.json']+[Path(x['path']).name for x in handoff['files']]
    assert sorted(names) == sorted(p.name for p in root.iterdir())
    return [m.verify(x['path'], x) for x in handoff['files']]+[m.identity(root/'HANDOFF.json')]

source, review = packet(Q), packet(R)
deps = m.load(Q/'SOURCE_DEPENDENCIES.json')['protected_files']
prior = m.load(OLD/'SOURCE_DEPENDENCIES.json')['protected_files']
by_path = {x['path']: x for x in deps}
old = {x['path']: x for x in prior}
assert len(deps) == len(by_path) == 396 and len(old) == 373
for path, row in old.items():
    assert {k:v for k,v in row.items() if k!='role'} == {k:v for k,v in by_path[path].items() if k!='role'}
observations = []
ids = {}
for row in deps:
    got = m.verify(row['path'], row['identity'])
    expected = row['identity']
    assert got['resolved_path'] == expected['resolved_path'] and got['symlink_chain'] == expected['symlinks']
    observations.append(got)
    ids[row['path']] = expected
ids[str(Q/'SOURCE_DEPENDENCIES.json')] = dict(m.ref(Q/'SOURCE_DEPENDENCIES.json'), resolved_path=str(Q/'SOURCE_DEPENDENCIES.json'), symlinks=[])

def refs(value):
    count = 0
    if isinstance(value, dict):
        if type(value.get('path')) is str and type(value.get('bytes')) is int and type(value.get('sha256')) is str and len(value['sha256']) == 64:
            expected = ids[value['path']]
            for key in ('path','bytes','sha256','resolved_path','symlinks'):
                if key in value:
                    assert value[key] == expected[key]
            count += 1
        count += sum(refs(x) for x in value.values())
    elif isinstance(value, list):
        count += sum(refs(x) for x in value)
    return count

new_admin = []
for row in deps:
    if row['path'] not in old and row['access_policy'] == 'metadata-identities-only-no-scientific-body-decoding':
        new_admin.append(dict(path=row['path'], references=refs(m.load(row['path']))))
assert len(new_admin) == 11 and sum(x['references'] for x in new_admin) == 1699
subject = m.load(Q/'SOURCE_IDENTITIES.json')
assert refs(subject) == 16
assert subject['subjects'] == m.load(OLD/'SOURCE_IDENTITIES.json')['subjects']
correspondence = m.load(Q/'SOURCE_CORRESPONDENCE.json')
unchanged = []
for group, oldrole, newrole in [('custody','ri134_native','custody'), ('launcher','ri136_dispatcher','launcher')]:
    before = Path(correspondence['sources'][oldrole]['path']).read_bytes().splitlines(keepends=True)
    after = Path(correspondence['sources'][newrole]['path']).read_bytes().splitlines(keepends=True)
    for row in correspondence['exact_unchanged_definitions'][group]:
        a = b''.join(before[row['old_start']-1:row['old_end']])
        b = b''.join(after[row['new_start']-1:row['new_end']])
        assert a == b and m.pin(b) == dict(bytes=row.get('bytes',row.get('whole_definition_bytes')),sha256=row['sha256'])
        unchanged.append(dict(component=group,name=row['name'],**m.pin(b)))
assert len(unchanged) == 8
verdict = m.load(R/'INDEPENDENT_SOURCE_REVIEW.json')
assert verdict['status'] == 'REQUIRE_F01_F02_REPAIR_BEFORE_LAUNCH_ADMISSION'
assert [x['id'] for x in verdict['blocking_findings']] == ['F01','F02']
check = m.load(R/'OPAQUE_TEXT_CHECK_V3.json')
assert check['success'] and not check['errors']
history = m.load(R/'CHECKER_HISTORY.json')
assert [x['actual_tool_completion']['exit_code'] for x in history['runs']] == [1,1,0]
for row in history['runs']:
    m.verify(row['result']['path'],row['result'])
    m.verify(row['source']['path'],row['source'])
result = m.save('RI138_ROOT_RECONCILIATION.json', dict(schema='ri138-root-source-reconciliation-v1',status='PASS_METADATA_SOURCE_FINDINGS_REQUIRE_REPAIR',source=source,review=review,dependency_observations=observations,inherited=373,added=23,new_administrative_bodies=new_admin,subject_references=16,literal_definitions=unchanged,independent_full_source_lines=2364,root_fresh_manual_scope='Full independent review and complete relevant ordinary-signal/acquisition/ownership/phase and primary-error/pipe-cleanup paths; not all2364 executable lines.',reviewer_reported_actual_history=history,root_subject_execution=False,current_runtime_inventory=False,older_administrative_traversal_inherited=True))
print(result)
decision = m.save('RI138_ROOT_ADJUDICATION.json', dict(schema='ri138-root-source-adjudication-v1',status='REQUIRE_F01_F02_IMMUTABLE_SOURCE_REPAIR',source=m.ref(Q/'HANDOFF.json'),independent_review=m.ref(R/'HANDOFF.json'),root_reconciliation=result,root_review=m.ref(m.D/'RI138_ROOT_SOURCE_REVIEW.md'),findings=verdict['blocking_findings'],source_accepted_for_execution=False,execution_admitted=False,controls_executed=0,next_item='RI140',original_packet_preserved=True,native_scientific_question='Actual C2/C3 signs and simultaneous shared H30 feasibility remain blocked on source repair, qualification and genuine execution admission.',ret_paused=True))
print(decision)
