"""RI139 SOURCE ONLY: direct-bootstrap repair of the RI137 focused25 launcher.

UNEXECUTED. Root authenticates this source, bootstrap/host and actual tool custody
externally. No production prepare.run/authenticate, target, profile or65 guards.
The complete unchanged RI135 module is loaded from authenticated captured bytes;
only its child_run monitor is called. No monitor globals are patched.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import time

HERE = Path(__file__).resolve().parent
BOOTSTRAP = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
CAP = 67108864
DEPENDENCY_PIN = {'path': str(HERE/'DEPENDENCIES.source-only.json'), 'bytes': 120094,
                  'sha256': '7be3dea02bd2f9d0e6dd565dbecad2977ed90eeab95612add058fd74a0be7309'}
PACKET_NAMES = ('AUTHORING_RECORD.md', 'DEPENDENCIES.source-only.json', 'HANDOFF.json',
                'METADATA_CHECK.json', 'PROTOCOL.md', 'REPAIR.diff', 'SOURCE_CORRESPONDENCE.json',
                'launch_controls.source-only.py')
F01 = ('positive', 'pre_admission_read', 'occupied', 'mkdir', 'post_admission_read', 'initial_source_read',
       'attempt_open', 'attempt_partial', 'secondary_post', 'secondary_source', 'secondary_namespace',
       'secondary_checks', 'three_secondary', 'final_partial')
F02 = ('positive', 'named_path', 'resolved_path', 'link_literal', 'link_order', 'link_omitted',
       'target_bytes', 'target_sha', 'provenance_missing', 'snapshot_alias', 'snapshot_target')
IDS = ['F01_'+x for x in F01]+['F02_'+x for x in F02]
LIMITS = {'child_seconds': 180, 'child_rss_kib': 524288, 'poll_seconds': 0.025,
          'maximum_sample_gap_seconds': 0.1, 'ps_timeout_seconds': 0.05,
          'stream_bytes': CAP, 'file_bytes': CAP, 'namespace_bytes': 536870912,
          'namespace_entries': 25000, 'parent_soft_seconds': 900, 'genuine_outer_timeout_seconds': 960}
PREMISES = {'genuine_bootstrap_host_preflight_external': True, 'genuine_tool_completion_external': True,
            'stable_supplier_host_and_no_descendants': True, 'apple_loader_and_cache_external': True,
            'sampled_child_only_not_parent_or_group_quota': True,
            'saved_parent_pid_not_authenticated_child_identity': True}


def need(ok, message):
    if not ok: raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')


def same(a, b, message):
    need(canonical(a) == canonical(b), message)


def keys(value, names, message):
    need(type(value) is dict and set(value) == set(names), message)


def pure(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def body(path):
    p = Path(path)
    need(p.is_absolute() and p.resolve(strict=True) == p and not p.is_symlink(), 'literal retained file')
    before = p.lstat()
    need(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= CAP, 'bounded regular retained file')
    state = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    with os.fdopen(os.open(p, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as f:
        need(state(os.fstat(f.fileno())) == state(before), 'opened file drift')
        data = f.read(CAP+1)
        need(state(os.fstat(f.fileno())) == state(before), 'descriptor drift')
    need(state(p.lstat()) == state(before) and len(data) == before.st_size <= CAP, 'retained file drift')
    return data


def ref(path):
    return {'path': str(path), **pure(body(path))}


def parse(data):
    def pairs(items):
        value = {}
        for k, v in items:
            need(k not in value, 'duplicate metadata key'); value[k] = v
        return value
    def bad(_): raise ValueError('nonfinite metadata')
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=bad)
    same(canonical(value).decode('ascii'), data.decode('ascii'), 'canonical metadata bytes')
    return value


def captured(row):
    keys(row, ('path', 'bytes', 'sha256'), 'closed FilePin')
    need(type(row['path']) is str and type(row['bytes']) is int and row['bytes'] >= 0
         and type(row['sha256']) is str and len(row['sha256']) == 64, 'typed FilePin')
    data = body(row['path']); same({'path': row['path'], **pure(data)}, row, 'FilePin drift')
    return data


def read(row):
    return parse(captured(row))


def save(path, value):
    data = canonical(value); need(len(data) <= CAP, 'bounded saved metadata')
    with path.open('xb') as f: f.write(data); f.flush(); os.fsync(f.fileno())
    return ref(path)


def tree(root):
    """Metadata-only full retention; no link traversal or target scientific decode."""
    need(root.is_absolute() and root.resolve(strict=True) == root and root.is_dir(), 'literal namespace root')
    rows = []; stack = [root]; total = 0
    while stack:
        parent = stack.pop()
        with os.scandir(parent) as it: entries = sorted(it, key=lambda x: x.name)
        for entry in entries:
            p = parent/entry.name; s = entry.stat(follow_symlinks=False); row = {'relative': str(p.relative_to(root))}
            if stat.S_ISLNK(s.st_mode): row.update(kind='symlink', target=os.readlink(p))
            elif stat.S_ISDIR(s.st_mode): row['kind'] = 'directory'; stack.append(p)
            else:
                need(stat.S_ISREG(s.st_mode), 'special namespace object')
                item = pure(body(p)); total += item['bytes']; row.update(kind='file', **item)
            rows.append(row)
            need(len(rows) <= LIMITS['namespace_entries'] and total <= LIMITS['namespace_bytes'], 'namespace limits')
    return sorted(rows, key=lambda x: x['relative'])


def separated(a, b):
    return a != b and a not in b.parents and b not in a.parents


def environment(root):
    return {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TZ': 'UTC', 'TMPDIR': str(root/'tmp'),
            'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
            'VECLIB_MAXIMUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1', '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}


def inspect_f01(row, output):
    kind = row['id'][4:]; e = row['evidence']; base = output/row['id']; out = base/'owned-output'
    keys(e, ('substitutions','events','calls','first_error','escaped','returncode','attempted_completion',
             'retained_tree','actual_runtime_or_production_admission'), 'F01 complete envelope')
    same(e['substitutions'], ['authentication','runtime snapshot/processes','source observation'], 'F01 substitutions')
    same(e['actual_runtime_or_production_admission'], False, 'F01 boundary')
    same(e['retained_tree'], tree(base), 'F01 complete retained tree')
    need(type(e['events']) is list and all(type(x) is str for x in e['events']), 'F01 events')
    pre = {'pre_admission_read':'CONTROL_PRE_ADMISSION_READ', 'occupied':'one fresh root-owned preparation output',
           'mkdir':'CONTROL_MKDIR_FAILURE'}
    counts = dict.fromkeys(('source_set','post','pre','source_tail','tree','checks','complete'), 0)
    if kind in pre:
        expected = {'type':'ValueError','message':pre[kind]}
        same(e['calls'], counts, 'F01 preownership counters'); same(e['first_error'], expected, 'F01 first refusal')
        same(e['escaped'], expected, 'F01 escaped refusal'); same(e['returncode'], None, 'F01 preownership return')
        same(e['attempted_completion'], [], 'F01 no invented completion')
        if kind == 'occupied':
            same(sorted(p.name for p in out.iterdir()), ['UNRELATED_OCCUPIED'], 'F01 occupied names')
            need(body(out/'UNRELATED_OCCUPIED') == b'preserve me\n', 'F01 occupied bytes')
        else: need(not os.path.lexists(out), 'F01 preownership output absent')
        return
    counts.update(source_set=1 if kind=='post_admission_read' else 2, post=1, pre=int(kind=='positive'),
                  source_tail=1, tree=1, checks=1, complete=1)
    same(e['calls'], counts, 'F01 exact owned counters')
    need(type(e['attempted_completion']) is list and len(e['attempted_completion']) == 1, 'F01 complete single attempt')
    complete = e['attempted_completion'][0]
    same(complete['admission'], ref(base/'FABRICATED_CONTROL_METADATA.json'), 'F01 authentic fabricated metadata pin')
    primary = {'post_admission_read':'CONTROL_POST_ADMISSION_READ','initial_source_read':'CONTROL_INITIAL_SOURCE_READ',
               'attempt_open':'CONTROL_ATTEMPT_OPEN'}.get(kind, 'CONTROL_ATTEMPT_PARTIAL')
    expected = None if kind=='positive' else {'type':'ValueError','message':primary}
    same(e['first_error'], expected, 'F01 first error'); same(complete['first_error'], expected, 'F01 preserved first error')
    same(complete['status'], 'CAPTURED_FOR_INDEPENDENT_REVIEW' if kind=='positive' else 'REFUSED_RETAIN_ALL_PARTIALS', 'F01 status')
    same(e['returncode'], None if kind=='final_partial' else int(kind!='positive'), 'F01 actual return')
    same(e['escaped'], {'type':'ValueError','message':'CONTROL_FINAL_RECEIPT_WRITE'} if kind=='final_partial' else None, 'F01 final refusal')
    tails = {'secondary_post':[('post_metadata','CONTROL_SECONDARY_POST')],
             'secondary_source':[('source_admission','CONTROL_SECONDARY_SOURCE')],
             'secondary_namespace':[('retain_namespace','CONTROL_SECONDARY_NAMESPACE')],
             'secondary_checks':[('save_checks','CONTROL_SECONDARY_CHECKS')],
             'three_secondary':[('post_metadata','CONTROL_SECONDARY_POST'),('source_admission','CONTROL_SECONDARY_SOURCE'),
                                ('retain_namespace','CONTROL_SECONDARY_NAMESPACE')]}.get(kind, [])
    same(complete['independent_tail_errors'], [{'tail':t,'type':'ValueError','message':m} for t,m in tails], 'F01 independent tails')
    partial = ('attempt_partial','secondary_post','secondary_source','secondary_namespace','secondary_checks','three_secondary','final_partial')
    if kind in partial:
        need(body(out/'ATTEMPT.json') == b'{"CONTROL_PARTIAL_ATTEMPT":', 'F01 partial initial bytes')
        same(e['events'].count('save_ATTEMPT.json'), 1, 'F01 no retry')
    if kind in ('post_admission_read','initial_source_read','attempt_open'):
        need(not os.path.lexists(out/'ATTEMPT.json'), 'F01 no fabricated initial receipt')
    if kind=='final_partial': need(body(out/'COMPLETE.json') == b'{"CONTROL_PARTIAL_COMPLETE":', 'F01 partial final bytes')
    else: same(read(ref(out/'COMPLETE.json')), complete, 'F01 full saved completion equality')


def inspect_f02(row, deps, historic):
    kind = row['id'][4:]; e = row['evidence']; expected = parse(canonical(historic))
    keys(e, ('current_binding_control_operand','genuine_historical_binding','historical_provenance','reads','calls','refusal',
             'snapshot_observers_substituted','provenance_after_authentication_mutated_in_memory',
             'actual_current_interpreter_observed'), 'F02 complete envelope')
    if kind=='named_path': expected['named_path'] += '.changed'
    if kind=='resolved_path': expected['resolved_path'] += '.changed'
    if kind in ('link_literal','snapshot_alias'): expected['symlink_chain'][0]['target'] = './python3.11'
    if kind=='link_order': expected['symlink_chain'] = list(reversed(expected['symlink_chain']))
    if kind=='link_omitted': expected['symlink_chain'] = expected['symlink_chain'][1:]
    if kind=='target_bytes': expected['target']['bytes'] += 1
    if kind in ('target_sha','snapshot_target'): expected['target']['sha256'] = '0'*64
    same(e['current_binding_control_operand'], expected, 'F02 exact fixed metadata mutation')
    same(e['genuine_historical_binding'], deps['historical_interpreter'], 'F02 historical binding role')
    same(e['historical_provenance'], deps['historical_interpreter_provenance'], 'F02 provenance role')
    snapshot = kind in ('snapshot_alias','snapshot_target')
    reads = ([deps['historical_optional_namespaces']['path']] if snapshot else [])+[deps['historical_interpreter_provenance']['path']]
    if kind!='provenance_missing': reads.append(deps['historical_interpreter']['path'])
    same(e['reads'], reads, 'F02 exact ordered reads before refusal')
    counts = dict.fromkeys(('host','sources','absences','namespaces','routes','loaders','interpreter','walk'), 0)
    if snapshot: counts.update(host=1,sources=1,absences=1,namespaces=1,routes=1,loaders=8,interpreter=1)
    same(e['calls'], counts, 'F02 exact observers and no later walk')
    message = 'historical interpreter handoff identity' if kind=='provenance_missing' else 'candidate interpreter differs from authentic historical binding'
    same(e['refusal'], None if kind=='positive' else {'type':'RuntimeError','message':message}, 'F02 exact first refusal')
    same(e['snapshot_observers_substituted'], snapshot, 'F02 observer boundary')
    same(e['provenance_after_authentication_mutated_in_memory'], kind=='provenance_missing', 'F02 provenance mutation boundary')
    same(e['actual_current_interpreter_observed'], False, 'F02 no runtime observation')


def inspect_controls(output, deps, control_pin, source_pins):
    report_pin = ref(output/'REPORT.json'); report = read(report_pin)
    keys(report, ('schema','controls','order','counts','sources_before','sources_after','sources_unchanged','status','admission',
                  'fixture_root','all_substitutions_explicit','runtime_profiles_or_65_caller_guards_executed','scientific_execution',
                  'production_admission_created','actual_current_runtime_qualified','ret_paused'), 'closed full control report')
    same(report['schema'], 'ri135-focused-fault-control-report-v1', 'control schema')
    same(report['order'], IDS, 'all25 exact order'); same(report['counts'], {'total':25,'passed':25,'failed':0}, 'control counts')
    same(report['status'], 'ALL25_FOCUSED_CONTROLS_PASSED', 'all control outcomes required')
    for k in ('sources_before','sources_after'): same(report[k], source_pins, 'control sources '+k)
    same(report['admission'], control_pin, 'control admission'); same(report['fixture_root'], str(output), 'control output')
    for k in ('sources_unchanged','all_substitutions_explicit','ret_paused'): same(report[k], True, k)
    for k in ('runtime_profiles_or_65_caller_guards_executed','scientific_execution','production_admission_created','actual_current_runtime_qualified'):
        same(report[k], False, k)
    need(type(report['controls']) is list and len(report['controls']) == 25, 'complete25 envelopes')
    historical = read(deps['historical_interpreter'])  # Saved interpreter metadata, never scientific operands.
    envelope_checks = []
    for identifier, row in zip(IDS, report['controls']):
        error = None
        try:
            keys(row, ('id','passed','evidence','error'), 'closed per-control result')
            same(row['id'], identifier, 'control identity'); same(row['passed'], True, 'individual pass'); same(row['error'], None, 'no control error')
            if identifier.startswith('F01_'): inspect_f01(row, output)
            else: inspect_f02(row, deps, historical)
        except BaseException as exc: error = {'type':type(exc).__name__,'message':str(exc)}
        envelope_checks.append({'id':identifier,'error':error})
    # Preserve the result of examining every present envelope before any failure is raised.
    save(output.parent/'ENVELOPE_CHECKS.json', {'report':report_pin,'checks':envelope_checks})
    need(all(x['error'] is None for x in envelope_checks), 'one or more saved control envelopes refused')
    namespace_pin = ref(output/'NAMESPACE.json'); namespace = read(namespace_pin)
    same(namespace, {'schema':'ri135-focused-controls-retained-namespace-v1','root':str(output),
                     'entries':[x for x in tree(output) if x['relative']!='NAMESPACE.json'],
                     'excluded_not_yet_written':['NAMESPACE.json'],'partial_failure_artifacts_retained':True}, 'full control namespace')
    return {'report':report_pin, 'namespace':namespace_pin, 'controls':IDS, 'count':25,
            'complete_administrative_envelopes_checked':True, 'scientific_evaluation':False}


def selected_bootstrap(preflight, deps):
    """Root-authenticated direct binding, not a self-authenticated loader proof."""
    binding = preflight['selected_interpreter_binding']
    keys(binding, ('path','resolved_path','bytes','sha256','state','symlink_chain'), 'closed selected interpreter binding')
    same(binding, deps['selected_bootstrap_binding'], 'genuine preflight selected interpreter identity')
    same([binding['path'],binding['resolved_path'],binding['symlink_chain']], [BOOTSTRAP,BOOTSTRAP,[]], 'literal direct bootstrap selection')
    captured({k:binding[k] for k in ('path','bytes','sha256')})
    actual = Path(BOOTSTRAP).lstat()
    same([actual.st_dev,actual.st_ino,actual.st_mode,actual.st_nlink,actual.st_size,actual.st_mtime_ns,actual.st_ctime_ns],
         binding['state'], 'selected interpreter state drift')
    same(sys.executable, BOOTSTRAP, 'direct interpreter descriptor')
    return binding


def prepare_launch(path):
    """Preownership authentication only; this function creates no evidence/card."""
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'normal isolated bootstrap')
    admission_pin = ref(path); card = read(admission_pin)
    keys(card, ('schema','status','launcher_handoff','launcher_review','launcher_adjudication','bootstrap_host_preflight',
                'controls_admission','output','environment_root','launcher_command','child_command','environment','limits','external_premises'), 'closed root launcher card')
    same(card['schema'], 'ri139-root-focused-launcher-admission-v1', 'launcher card schema')
    same(card['status'], 'AUTHORIZE_ONLY_RI135_FOCUSED25', 'launcher authority')
    same(card['limits'], LIMITS, 'unchanged resource bounds'); same(card['external_premises'], PREMISES, 'external premises')
    deps = read(DEPENDENCY_PIN)
    for item in deps['opaque_files']: captured(item)
    decision = read(deps['ri135_root_adjudication'])
    need(decision['source_accepted'] is True and decision['execution_admitted'] is False
         and decision['status']=='ACCEPT_BOUNDED_UNEXECUTED_F01_F02_REPAIR', 'accepted source only')
    same(card['launcher_handoff']['path'], str(HERE/'HANDOFF.json'), 'this exact launcher packet')
    handoff = read(card['launcher_handoff'])
    same(handoff['reservation'], str(HERE), 'packet reservation')
    same(sorted(p.name for p in HERE.iterdir()), list(PACKET_NAMES), 'closed launcher source namespace')
    own_pins = handoff['files']+[card['launcher_handoff']]
    same(sorted(x['path'] for x in own_pins), sorted(str(HERE/x) for x in PACKET_NAMES), 'complete source pin set')
    for item in own_pins: captured(item)
    card_pins = [admission_pin]+[card[k] for k in ('controls_admission','launcher_review','launcher_adjudication','bootstrap_host_preflight')]
    for item in card_pins: captured(item)
    need(len({x['path'] for x in card_pins}) == len(card_pins), 'distinct operation card/review/preflight roles')
    selected_bootstrap(read(card['bootstrap_host_preflight']), deps)
    out = Path(card['output']); envroot = Path(card['environment_root'])
    for key, p in (('output', out), ('environment_root', envroot)):
        need(type(card[key]) is str and str(p) == card[key] and p.is_absolute() and p.resolve() == p, 'literal operation path')
    need(not os.path.lexists(out) and out.parent.is_dir(), 'one fresh launcher output')
    need(envroot.is_dir() and separated(out, envroot), 'separate root environment')
    same(tree(envroot), [{'relative':'tmp','kind':'directory'}], 'root-prepared empty environment')
    for p in [out,envroot]+[Path(x['path']) for x in card_pins]:
        for sealed in deps['sealed_namespace_roots']: need(separated(p, Path(sealed)), 'operation path overlaps sealed namespace')
    for item in card_pins:
        need(separated(Path(item['path']), out) and separated(Path(item['path']), envroot), 'card/evidence output overlap')
    env = environment(envroot); same(card['environment'], env, 'exact declared environment')
    same(dict(os.environ), env, 'actual complete environment')
    command = [BOOTSTRAP,'-I','-B',deps['ri135_control']['path'],'--admission',card['controls_admission']['path'],'--output',str(out/'controls')]
    same(card['child_command'], command, 'exact only control child command')
    launcher = [BOOTSTRAP,'-I','-B',str(HERE/'launch_controls.source-only.py'),'--admission',str(path)]
    same(card['launcher_command'], launcher, 'exact launcher command'); same(sys.argv, launcher[3:], 'actual launcher arguments')
    sources = {name:pure(body(Path(deps['ri135_module']['path']).parent/name)) for name in deps['ri135_source_names']}
    control = read(card['controls_admission'])
    same(control, {'schema':'ri135-root-fault-control-admission-v1','status':'AUTHORIZE_F01_F02_NONSCIENTIFIC_CONTROLS_ONLY',
                   'sources':sources,'controls':IDS,'output':str(out/'controls'),
                   'independent_source_review':deps['ri135_independent_review'],'genuine_outer_required':True}, 'exact existing control card')
    module_bytes = captured(deps['ri135_module'])
    spec = importlib.util.spec_from_file_location('ri139_unchanged_ri135_monitor', deps['ri135_module']['path'])
    module = importlib.util.module_from_spec(spec)
    # Load the WHOLE authenticated capture at its original filename, never as __main__.
    exec(compile(module_bytes, deps['ri135_module']['path'], 'exec'), module.__dict__)
    same(module.environment(envroot), env, 'inherited exact environment applicability')
    return card, admission_pin, deps, own_pins, card_pins, sources, module_bytes, module


def run(path):
    card, admission_pin, deps, own_pins, card_pins, sources, captured_module, P = prepare_launch(path)
    out = Path(card['output']); envroot = Path(card['environment_root']); env = card['environment']
    first = None; tails = []; checks = {}; artifacts = {}; child = None; started = time.monotonic()
    def tail(name, action):
        try: checks[name] = action()
        except BaseException as exc: tails.append({'tail':name,'type':type(exc).__name__,'message':str(exc)})
    def sources_after():
        for row in own_pins: captured(row)
        same(sorted(p.name for p in HERE.iterdir()), list(PACKET_NAMES), 'source namespace postcheck')
        same({name:pure(body(Path(deps['ri135_module']['path']).parent/name)) for name in deps['ri135_source_names']}, sources, 'RI135 source postcheck')
        return 'PASS'
    def dependencies_after():
        for row in deps['opaque_files']: captured(row)
        return 'PASS'
    def cards_after():
        for row in card_pins: captured(row)
        selected_bootstrap(read(card['bootstrap_host_preflight']), deps)
        same(dict(os.environ), env, 'parent environment postcheck')
        same(tree(envroot), [{'relative':'tmp','kind':'directory'}], 'environment namespace postcheck')
        return 'PASS'
    def controls_after():
        value = inspect_controls(out/'controls', deps, card['controls_admission'], sources)
        artifacts['administrative_checks'] = save(out/'ADMINISTRATIVE_CHECKS.json', value)
        return value
    def namespace_after():
        return save(out/'NAMESPACE.json', {'schema':'ri139-retained-launcher-namespace-v1','root':str(out),
            'entries':tree(out),'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json'], 'all_partials_retained':True})
    out.mkdir(mode=0o700)
    try:
        # First owned operation is protected; original admission pin is never replaced.
        same(ref(path), admission_pin, 'admission drift after ownership')
        artifacts['attempt'] = save(out/'ATTEMPT.json', {'schema':'ri139-focused-launcher-attempt-v1','admission':admission_pin,
            'child_command':card['child_command'],'environment':env,'limits':LIMITS,'external_premises':PREMISES,
            'loaded_module':deps['ri135_module'],'captured_loaded_bytes':pure(captured_module),'scientific_execution':False})
        child = P.child_run(card['child_command'], out, 'FOCUSED25', 180, env)
        need(child['stdout']['bytes'] == 0, 'no unexpected focused-control stdout')
    except BaseException as exc:
        first = {'type':type(exc).__name__,'message':str(exc)}
    finally:
        # Independent groups all attempted, including after initial ATTEMPT failure.
        # Group-internal failures are retained; no receipt overwrite or retry occurs.
        tail('controls', controls_after)
        tail('source', sources_after)
        tail('dependency', dependencies_after)
        tail('card', cards_after)
        tail('namespace', namespace_after)
        if time.monotonic()-started > LIMITS['parent_soft_seconds']:
            tails.append({'tail':'parent_soft_deadline','type':'ValueError','message':'parent soft deadline exceeded'})
        complete = {'schema':'ri139-focused-launcher-completion-v1','status':'CAPTURED_FOR_ROOT_REVIEW' if first is None and not tails else 'REFUSED_RETAIN_ALL_PARTIALS',
            'admission':admission_pin,'launcher_command':card['launcher_command'],'child_command':card['child_command'],
            'environment':env,'limits':LIMITS,'external_premises':PREMISES,'first_error':first,'independent_tail_errors':tails,
            'checks':checks,'artifacts':artifacts,'child':child,'elapsed_seconds':time.monotonic()-started,
            'scientific_execution':False,'runtime_qualification':False,'ri130_65_guards_executed':False,
            'genuine_tool_completion_created':False,'ret_paused':True}
        # Final-write failure escapes without retry; outer stderr can retain the
        # original first error as well as this secondary receipt error.
        try: save(out/'COMPLETE.json', complete)
        except BaseException as exc:
            raise RuntimeError(canonical({'first_error':first,'independent_tail_errors':tails,
                'final_receipt_error':{'type':type(exc).__name__,'message':str(exc)}}).decode('ascii')) from exc
    return 0 if complete['status']=='CAPTURED_FOR_ROOT_REVIEW' else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--admission', type=Path, required=True)
    raise SystemExit(run(parser.parse_args().admission))
