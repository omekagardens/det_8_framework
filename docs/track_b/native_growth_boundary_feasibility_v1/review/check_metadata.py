"""Independent administrative identities and source-text ranges only; no subjects executed."""
from pathlib import Path
import collections
import hashlib
import json
import os
import stat
import traceback

R = Path('/Volumes/AI_DATA/development/det-review-evidence/ri143-independent-feasibility-review-f68n6324')
Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri143-native-boundary-feasibility-0i0dbnge')
P = Path('/Volumes/AI_DATA/development/det-review-evidence/ri140-native-failure-repair-source-l_a4mna0')
CAP = 67108864


def require(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def identity(path, keep=False):
    path = Path(path)
    require(path.is_absolute() and path.resolve(strict=True) == path, 'literal path: '+str(path))
    prefix = Path('/')
    for component in path.parts[1:]:
        prefix /= component
        require(not prefix.is_symlink(), 'no symlink components')
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size <= CAP, 'bounded regular file')
    state = lambda s: (s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    total, digest, chunks = 0, hashlib.sha256(), []
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as source:
        require(state(os.fstat(source.fileno())) == state(before), 'opened drift')
        while True:
            block = source.read(65536)
            if not block:
                break
            total += len(block)
            require(total <= CAP, 'opaque read cap')
            digest.update(block)
            if keep:
                chunks.append(block)
        require(state(os.fstat(source.fileno())) == state(before), 'descriptor drift')
    require(state(path.lstat()) == state(before) and total == before.st_size, 'final drift')
    record = {'path':str(path),'resolved_path':str(path),'bytes':total,'sha256':digest.hexdigest(),'symlinks':[]}
    return record, b''.join(chunks) if keep else None


def simple(row):
    return {k:row[k] for k in ('path','bytes','sha256')}


def load(path):
    _, body = identity(path, True)
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'duplicate administrative key')
            out[k] = v
        return out
    def bad(value):
        raise ValueError('nonfinite administrative value: '+value)
    return json.loads(body, object_pairs_hook=pairs, parse_constant=bad)


def run():
    handoff_pin, _ = identity(Q/'HANDOFF.json')
    require(handoff_pin['bytes'] == 6743 and handoff_pin['sha256'] == '6ffa8638c138ccd481514d6ce8dd835d8c2c17f48e91c4215d80eb1e47546307', 'assigned handoff pin')
    handoff = load(Q/'HANDOFF.json')
    require(len(handoff['payloads']) == 13 and sorted(p.name for p in Q.iterdir()) == sorted(handoff['namespace']), 'exact14 namespace')
    require(len(handoff['namespace']) == 14, 'namespace count')
    payloads = []
    for row in handoff['payloads']:
        got, _ = identity(row['path'])
        require(simple(got) == row and Path(row['path']).parent == Q, 'payload exact pin/parent')
        payloads.append(got)
    require(sorted(Path(x['path']).name for x in payloads)+['HANDOFF.json'] != [], 'nonempty payload set')
    require(set(x['path'] for x in payloads)|{str(Q/'HANDOFF.json')} == {str(Q/n) for n in handoff['namespace']}, 'payload domain')
    current, old = load(Q/'SOURCE_DEPENDENCIES.json'), load(P/'SOURCE_DEPENDENCIES.json')
    rows, oldrows = current['protected_files'], old['protected_files']
    by, oldby = {r['path']:r for r in rows}, {r['path']:r for r in oldrows}
    require(len(rows) == len(by) == 450 and len(oldrows) == len(oldby) == 423, 'unique450 and423')
    strip = lambda r: {k:v for k,v in r.items() if k != 'role'}
    for path, row in oldby.items():
        require(path in by and canonical(strip(row)) == canonical(strip(by[path])), 'inherited complete object drift')
    actuals, total = [], 0
    for index, row in enumerate(rows, 1):
        require(row['role'] == 'dep_'+str(index).zfill(4), 'ordered role')
        got, _ = identity(row['path'])
        require(canonical(got) == canonical(row['identity']), 'opaque dependency drift: '+row['path'])
        actuals.append(got)
        total += got['bytes']
    require([r['path'] for r in rows] == sorted(by), 'sorted paths')
    require(total == 171097748 and max(x['bytes'] for x in actuals) == 31528781, 'byte totals')
    additions = [simple(x) for x in actuals if x['path'] not in oldby]
    require(len(additions) == 27, '27 additions')
    excluded_root = Path('/Volumes/AI_DATA/development/det-review-evidence/ri138-launch-independent-review-6xGu5oak')
    excluded = [str(excluded_root/n) for n in ('check_metadata.py','check_metadata_v2.py','OPAQUE_TEXT_CHECK.json','OPAQUE_TEXT_CHECK_V2.json')]
    require(not set(excluded)&set(by), 'four historical external diagnostics stay unopened/excluded')
    subjects, prior_subjects = load(Q/'SOURCE_IDENTITIES.json'), load(P/'SOURCE_IDENTITIES.json')
    require(canonical(subjects['unchanged_policy_subjects']) == canonical(prior_subjects['subjects']), 'full policy objects differ')
    policy_counts = {}
    for kind, count in [('native',77),('audit',62)]:
        obj = subjects['unchanged_policy_subjects'][kind]
        require(obj['case_count'] == count and len(obj['ordered_cases']) == count, 'ordered policy count')
        policy_counts[kind] = count
    for key, row in subjects['dispatcher_bindings'].items():
        require(canonical(row) == canonical(prior_subjects[key]), 'dispatcher identity role')
    known = {x['path']:x for x in actuals+payloads+[handoff_pin]}
    references = []
    def check_refs(value, location):
        if type(value) is dict:
            if type(value.get('path')) is str and type(value.get('bytes')) is int and type(value.get('sha256')) is str:
                require(value['path'] in known, 'unselected typed reference: '+location)
                got = known[value['path']]
                for key in ('path','bytes','sha256','resolved_path','symlinks'):
                    if key in value:
                        require(canonical(value[key]) == canonical(got[key]), 'reference drift: '+location+'.'+key)
                references.append(location)
            for key, member in value.items():
                check_refs(member, location+'.'+key)
        elif type(value) is list:
            for index, member in enumerate(value):
                check_refs(member, location+'['+str(index)+']')
    for name in ('SOURCE_IDENTITIES.json','SOURCE_APPLICABILITY.json','F01_BOUNDARIES.json','F02_BOUNDARIES.json'):
        check_refs(load(Q/name), name)
    namespaces = []
    for base in (P, Path('/Volumes/AI_DATA/development/det-review-evidence/ri140-independent-source-review-i57s4u4b')):
        historical = load(base/'HANDOFF.json');expected = historical['files']
        require(sorted(p.name for p in base.iterdir()) == sorted([Path(x['path']).name for x in expected]+['HANDOFF.json']), 'historical exact namespace')
        for row in expected:
            require(row == simple(known[row['path']]), 'historical handoff payload drift')
        namespaces.append({'path':str(base),'entries':len(expected)+1})
    f1, f2 = load(Q/'F01_BOUNDARIES.json'), load(Q/'F02_BOUNDARIES.json')
    wanted1 = []
    for i in range(1,16):
        wanted1.extend(['F01-'+str(i)+'-'+s for s in ('SIGTERM','SIGINT','SIGHUP')] if i in (1,2,10,14) else ['F01-'+str(i)])
    wanted2 = ['F02-1-UNREGISTER','F02-1-CLOSE']+['F02-'+str(i) for i in range(2,8)]
    require([r['id'] for r in f1['rows']] == wanted1 and [r['id'] for r in f2['cases']] == wanted2, '31 exact ordered IDs')
    locations = []
    for row in f1['rows']:
        require(row['executed'] is False and row['passed'] is False and row['available_mechanism_established'] is False, 'F01 blocked flags')
        require(bool(row['entry_preconditions']) and bool(row['first_reachable_refusal']), 'F01 gate detail')
        for loc in row['subject_locations']:
            locations.append({'id':row['id'],**loc})
    for row in f2['cases']:
        require(row['executed'] is False and row['available'] is False and row['controller_implemented'] is False and row['actual_outcome'] is None, 'F02 blocked flags')
        require(bool(row['entry_preconditions']) and bool(row['first_reachable_refusal']), 'F02 gate detail')
        for loc in row['source_locations']:
            locations.append({'id':row['id'],'path':f2['sources'][loc['source']]['path'],'start_line':loc['start_line'],'end_line':loc['end_line'],'purpose':loc['purpose']})
        record = row['expected_target_record']
        if record and 'original_message_characters' in record:
            require(len(record['message']) == record['original_message_characters'], 'literal error message length')
    require(len(locations) == 104, '104 source ranges')
    source_ranges = []
    for path in sorted({x['path'] for x in locations}):
        got, body = identity(path, True)
        require(canonical(got) == canonical(known[path]), 'source range pin')
        lines = body.decode('utf-8').splitlines(keepends=True)
        selected = set()
        for loc in [r for r in locations if r['path'] == path]:
            a,b = loc['start_line'],loc['end_line']
            require(type(a) is int and type(b) is int and 1 <= a <= b <= len(lines), 'source range domain')
            selected.update(range(a,b+1))
            loc['range_sha256'] = hashlib.sha256(''.join(lines[a-1:b]).encode()).hexdigest()
        source_ranges.append({'source':simple(got),'full_line_count':len(lines),'unique_referenced_lines':len(selected)})
    require(sum(x['unique_referenced_lines'] for x in source_ranges) == 670, '670 unique cited lines')
    app = load(Q/'SOURCE_APPLICABILITY.json')
    require(app['source_diffs'] == [] and app['modified_executable_source'] is False and app['new_controller_implemented'] is False, 'unchanged-design scope')
    require(app['disposition']['natural_EOF_source_reachable'] is True and app['disposition']['natural_EOF_qualification_established'] is False and app['disposition']['platform_wide_impossibility_claimed'] is False, 'bounded feasibility scope')
    return {'schema':'ri143-independent-opaque-and-text-check-v1','status':'PASS_ADMINISTRATIVE_IDENTITIES_ONLY','source_handoff':simple(handoff_pin),'payloads':[simple(x) for x in payloads],'namespace':handoff['namespace'],'dependencies':{'files':450,'bytes':total,'largest_bytes':31528781,'preserved_complete_objects_except_role':423,'additions':additions,'access_policies':dict(collections.Counter(r['access_policy'] for r in rows)),'all_identity_rows_sha256':hashlib.sha256(canonical(actuals).encode()).hexdigest()},'historical_namespaces':namespaces,'full_policy_objects_equal':True,'policy_counts':policy_counts,'typed_current_references_checked':len(references),'F01_ids':wanted1,'F02_ids':wanted2,'source_ranges':source_ranges,'all104_range_pins':locations,'excluded_external_diagnostics_not_opened':excluded,'review_method':'New reviewer-owned stdlib administrative script; stable seven-field no-follow file reads, duplicate-rejecting administrative JSON and opaque whole-file identities; source ranges read only as text. No subject imports, compilation, AST, probe, control, fixture, runtime/candidate observation or scientific-body decode.','focused_controls_executed':0,'policy_cases_executed':0,'current_runtime_observed':False,'root_acceptance':False,'execution_admission':False,'ret_paused':True}


if __name__ == '__main__':
    try:
        result = run()
        with (R/'OPAQUE_TEXT_CHECK.json').open('x') as out:
            json.dump(result,out,sort_keys=True,indent=2);out.write('\n')
        print(json.dumps({'status':result['status'],'dependencies':450,'bytes':171097748,'ranges':104,'ids':31,'result':simple(identity(R/'OPAQUE_TEXT_CHECK.json')[0])},indent=2))
    except BaseException as error:
        with (R/'CHECK_FAILURE.txt').open('x') as out:
            out.write(traceback.format_exc())
        raise
