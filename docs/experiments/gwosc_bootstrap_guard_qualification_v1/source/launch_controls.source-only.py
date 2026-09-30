"""RI144 SOURCE ONLY: narrow RI139 supervision adaptation for fifteen new guards.

UNEXECUTED. Root authenticates this source, bootstrap/host and actual tool custody
externally. No production prepare.run/authenticate, profile, scientific target or65 guards.
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
DEPENDENCY_PIN = {'path': str(HERE/'DEPENDENCIES.source-only.json'), 'bytes': 162285,
                  'sha256': '255ee1f97126e79ad31f2d2e00bcb1b513f23422051be7b1fba99b97b8b76f5d'}
PACKET_NAMES = ('AUTHORING_RECORD.md','AUTHOR_DIAGNOSTICS.json','DEPENDENCIES.source-only.json','HANDOFF.json',
 'METADATA_CHECK.json','PROTOCOL.md','REPAIR.diff','SOURCE_CORRESPONDENCE.json',
 'bootstrap_controls.source-only.py','launch_controls.source-only.py')
CONTROL_SOURCE_NAMES = ('bootstrap_controls.source-only.py','launch_controls.source-only.py','DEPENDENCIES.source-only.json')
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


# Fixed source declarations. Constructed only by a later separately admitted run.
IDS = ['B01','B02','B03','B04','B05','B06']+['B07_'+x for x in ('path','resolved_path','symlink_chain','bytes','sha256','state')]+['B08','B09','B10']


def recipe(identifier, baseline, provenance_path):
    need(identifier in IDS, 'closed fifteen control domain')
    clone = lambda x: parse(canonical(x))
    preflight = {'selected_interpreter_binding':clone(baseline)}
    provenance = {'schema':'ri144-private-provenance-double-v1', 'selected_bootstrap_binding':clone(baseline)}
    observation = {'bytes':{k:baseline[k] for k in ('path','bytes','sha256')},
                   'state':list(baseline['state']), 'descriptor':BOOTSTRAP}
    if identifier == 'B04': provenance['selected_bootstrap_binding']['bytes'] += 1
    raw = canonical(provenance)
    declared = {'path':str(provenance_path), **pure(raw)}
    if identifier == 'B03':
        provenance['selected_bootstrap_binding']['bytes'] += 1
        raw = canonical(provenance)  # Canonical private bytes differ from the unchanged declared pin.
    if identifier == 'B05': del preflight['selected_interpreter_binding']['state']
    if identifier == 'B06': preflight['selected_interpreter_binding']['extra'] = True
    if identifier.startswith('B07_'):
        field = identifier[4:]; value = preflight['selected_interpreter_binding']
        if field in ('path','resolved_path'): value[field] += '.changed'
        elif field == 'symlink_chain': value[field] = [{'path':BOOTSTRAP+'.alias','target':BOOTSTRAP}]
        elif field == 'bytes': value[field] += 1
        elif field == 'sha256': value[field] = '0'*64
        else: value['state'][1] += 1
    if identifier == 'B08': observation['bytes']['bytes'] += 1
    if identifier == 'B09': observation['state'][1] += 1
    if identifier == 'B10': observation['descriptor'] += '.changed'
    dependencies = {'bootstrap_selection_provenance':declared,
                    'opaque_files':[] if identifier=='B02' else [declared],
                    'selected_bootstrap_binding':clone(baseline)}
    message = {'B02':'bootstrap selection provenance absent from closure',
               'B03':'metadata reference drift','B04':'accepted direct bootstrap selection provenance',
               'B05':'closed selected interpreter binding','B06':'closed selected interpreter binding',
               'B08':'opaque evidence reference drift','B09':'selected interpreter state drift',
               'B10':'direct interpreter descriptor'}.get(identifier)
    if identifier.startswith('B07_'): message = 'genuine preflight selected interpreter identity'
    trace = []
    def gate(name):
        trace.append({'kind':'gate','name':name,'passed':name!=message})
        return name==message
    def observer(name): trace.append({'kind':'observer','name':name})
    stopped = gate('bootstrap selection provenance absent from closure')
    if not stopped:
        observer('private_provenance_read')
        for name in ('closed metadata FilePin','literal source/metadata path','bounded regular source/metadata',
                     'metadata opened drift','metadata descriptor drift','metadata read drift','metadata reference drift'):
            if gate(name): stopped=True; break
    if not stopped:
        for _ in range(8): gate('duplicate metadata key')  # Six binding keys, then the two private root keys.
        gate('canonical metadata framing')
        for name in ('accepted direct bootstrap selection provenance','closed selected interpreter binding',
                     'genuine preflight selected interpreter identity','literal direct bootstrap selection'):
            if gate(name): stopped=True; break
    if not stopped:
        observer('supplier_bytes'); stopped=gate('opaque evidence reference drift')
    if not stopped:
        observer('supplier_lstat'); stopped=gate('selected interpreter state drift')
    if not stopped:
        observer('interpreter_descriptor'); gate('direct interpreter descriptor')
    return {'private_bytes':raw,'declared_provenance':declared,'preflight':preflight,'dependencies':dependencies,
            'observations':observation,'trace':trace,
            'refusal':None if message is None else {'type':'ValueError','message':message},
            'return_binding':clone(baseline) if identifier=='B01' else None}


def inspect_controls(output, deps, control_pin, source_pins):
    report_pin=ref(output/'REPORT.json'); report=read(report_pin)
    keys(report,('schema','status','order','controls','counts','sources','target_handoff','target_module','admission','output',
                'first_error','independent_tail_errors','actual_supplier_observed','production_authenticate_called','old25_rerun',
                'scientific_execution','current_runtime_qualified','ret_paused','elapsed_seconds'),'closed bootstrap control report')
    same(report['schema'],'ri144-fifteen-bootstrap-control-report-v1','control report schema')
    same(report['order'],IDS,'exact fifteen order')
    need(type(report['controls']) is list and len(report['controls'])==15,'complete fifteen records required')
    same(report['sources'],source_pins,'whole actual control sources')
    same(report['target_handoff'],deps['target_handoff'],'target handoff binding')
    same(report['target_module'],deps['target_module'],'target module binding')
    same(report['admission'],control_pin,'control admission pin');same(report['output'],str(output),'control output')
    for name in ('actual_supplier_observed','production_authenticate_called','old25_rerun','scientific_execution','current_runtime_qualified'):
        same(report[name],False,'control scope '+name)
    same(report['ret_paused'],True,'RET remains paused')
    baseline=deps['selected_bootstrap_binding']; envelope_checks=[]
    for identifier,row in zip(IDS,report['controls']):
        error=None
        try:
            keys(row,('id','passed','error','evidence'),'closed case envelope')
            same(row['id'],identifier,'isolated case identity');same(row['passed'],True,'isolated expectation passed');same(row['error'],None,'no unexpected case error')
            operand=recipe(identifier,baseline,output/identifier/'PROVENANCE_DOUBLE.json')
            need(body(output/identifier/'PROVENANCE_DOUBLE.json')==operand['private_bytes'],'exact retained private provenance bytes')
            actual={'path':str(output/identifier/'PROVENANCE_DOUBLE.json'),**pure(operand['private_bytes'])}
            expected={'baseline_binding':baseline,'dependency_operand':operand['dependencies'],'preflight_operand':operand['preflight'],
                'observer_doubles':operand['observations'],'private_provenance_declared':operand['declared_provenance'],
                'private_provenance_actual':actual,'complete_loaded_module':deps['target_module'],
                'captured_loaded_bytes':{k:deps['target_module'][k] for k in ('bytes','sha256')},
                'trace':operand['trace'],'returned_binding':operand['return_binding'],'first_refusal':operand['refusal'],
                'inputs_unchanged':True,'substitutions':['private provenance file and closure operand','supplier byte observation','supplier lstat observation','sys.executable descriptor'],
                'real_private_reader_parser_and_comparisons':True,'actual_supplier_observed':False,'production_authenticate_called':False,
                'expected_trace':operand['trace'],'expected_first_refusal':operand['refusal'],'expected_returned_binding':operand['return_binding']}
            same(row['evidence'],expected,'entire isolated operand/trace/result envelope')
        except BaseException as exc: error={'type':type(exc).__name__,'message':str(exc)}
        envelope_checks.append({'id':identifier,'error':error})
    save(output.parent/'ENVELOPE_CHECKS.json',{'report':report_pin,'checks':envelope_checks})
    need(all(row['error'] is None for row in envelope_checks),'saved isolated expectation refused')
    same(report['counts'],{'total':15,'passed':15,'failed':0},'all fifteen counts')
    same(report['status'],'FIFTEEN_EXPECTATIONS_PASSED','all isolated expectations required')
    same(report['first_error'],None,'no earlier child failure');same(report['independent_tail_errors'],[],'all child tails required')
    need(type(report['elapsed_seconds']) in (int,float) and 0<=report['elapsed_seconds']<=180,'bounded control elapsed')
    same(read(ref(output/'ATTEMPT.json')),{'schema':'ri144-controls-attempt-v1','admission':control_pin,
         'target':deps['target_module'],'controls':IDS,'old25_rerun':False,'supplier_observation_is_double':True},'full actual control attempt')
    rows=tree(output)
    expected_names={'ATTEMPT.json','REPORT.json','NAMESPACE.json'}|set(IDS)|{i+'/PROVENANCE_DOUBLE.json' for i in IDS}
    same(sorted(row['relative'] for row in rows),sorted(expected_names),'exact full control namespace domain')
    for row in rows: same(row['kind'],'directory' if row['relative'] in IDS else 'file','control namespace kind')
    namespace_pin=ref(output/'NAMESPACE.json')
    same(read(namespace_pin),{'schema':'ri144-control-namespace-v1','root':str(output),
         'entries':[x for x in rows if x['relative']!='NAMESPACE.json'],'excluded_not_yet_written':['NAMESPACE.json'],
         'all_partials_retained':True},'complete retained control namespace')
    return {'report':report_pin,'namespace':namespace_pin,'controls':IDS,'count':15,
            'complete_administrative_envelopes_checked':True,'scientific_evaluation':False}


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
    same(card['schema'], 'ri144-root-bootstrap-launcher-admission-v1', 'launcher card schema')
    same(card['status'], 'AUTHORIZE_ONLY_RI144_FIFTEEN_BOOTSTRAP_GUARDS', 'launcher authority')
    same(card['limits'], LIMITS, 'unchanged resource bounds'); same(card['external_premises'], PREMISES, 'external premises')
    deps = read(DEPENDENCY_PIN)
    for item in deps['opaque_files']: captured(item)
    decision = read(deps['ri135_root_adjudication'])
    need(decision['source_accepted'] is True and decision['execution_admitted'] is False
         and decision['status']=='ACCEPT_BOUNDED_UNEXECUTED_F01_F02_REPAIR', 'accepted source only')
    target_decision=read(deps['target_adjudication'])
    same(target_decision['status'],'ACCEPT_EXACT_SOURCE_WITH_EXECUTION_PREREQUISITES','target source accepted')
    same(target_decision['source_handoff'],deps['target_handoff'],'exact target decision binding')
    same(target_decision['execution_admitted'],False,'target source acceptance is not execution admission')
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
    command = [BOOTSTRAP,'-I','-B',str(HERE/'bootstrap_controls.source-only.py'),'--admission',card['controls_admission']['path'],'--output',str(out/'controls')]
    same(card['child_command'], command, 'exact only control child command')
    launcher = [BOOTSTRAP,'-I','-B',str(HERE/'launch_controls.source-only.py'),'--admission',str(path)]
    same(card['launcher_command'], launcher, 'exact launcher command'); same(sys.argv, launcher[3:], 'actual launcher arguments')
    sources = {name:pure(body(HERE/name)) for name in CONTROL_SOURCE_NAMES}
    control = read(card['controls_admission'])
    same(control, {'schema':'ri144-root-bootstrap-control-admission-v1',
        'status':'AUTHORIZE_ONLY_FIFTEEN_ISOLATED_BOOTSTRAP_EXPECTATIONS','launcher_handoff':card['launcher_handoff'],
        'target_handoff':deps['target_handoff'],'sources':sources,'controls':IDS,'output':str(out/'controls'),
        'environment_root':str(envroot),'command':command,'independent_source_review':deps['target_review'],
        'genuine_outer_required':True}, 'exact changed-guard control card')
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
        same({name:pure(body(HERE/name)) for name in CONTROL_SOURCE_NAMES}, sources, 'RI144 source postcheck')
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
        return save(out/'NAMESPACE.json', {'schema':'ri144-retained-launcher-namespace-v1','root':str(out),
            'entries':tree(out),'excluded_not_yet_written':['NAMESPACE.json','COMPLETE.json'], 'all_partials_retained':True})
    out.mkdir(mode=0o700)
    try:
        # First owned operation is protected; original admission pin is never replaced.
        same(ref(path), admission_pin, 'admission drift after ownership')
        artifacts['attempt'] = save(out/'ATTEMPT.json', {'schema':'ri144-bootstrap-launcher-attempt-v1','admission':admission_pin,
            'child_command':card['child_command'],'environment':env,'limits':LIMITS,'external_premises':PREMISES,
            'loaded_module':deps['ri135_module'],'captured_loaded_bytes':pure(captured_module),'scientific_execution':False})
        child = P.child_run(card['child_command'], out, 'BOOTSTRAP15', 180, env)
        need(child['stdout']['bytes'] == 0, 'no unexpected bootstrap-control stdout')
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
        complete = {'schema':'ri144-bootstrap-launcher-completion-v1','status':'CAPTURED_FOR_ROOT_REVIEW' if first is None and not tails else 'REFUSED_RETAIN_ALL_PARTIALS',
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
