"""RI144 SOURCE ONLY / UNEXECUTED: fifteen isolated selected_bootstrap controls.
Private provenance and explicit process-local observer doubles only. This is not
production authentication, a current supplier observation, or old25 execution.
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
import types

HERE = Path(__file__).resolve().parent
BOOTSTRAP = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
CAP = 67108864
DEPENDENCY_PIN = {'path':str(HERE/'DEPENDENCIES.source-only.json'),'bytes':162285,
 'sha256':'255ee1f97126e79ad31f2d2e00bcb1b513f23422051be7b1fba99b97b8b76f5d'}
LIMITS = {'namespace_entries':25000,'namespace_bytes':536870912}
SOURCE_NAMES = ('bootstrap_controls.source-only.py','launch_controls.source-only.py','DEPENDENCIES.source-only.json')
PACKET_NAMES = ('AUTHORING_RECORD.md','AUTHOR_DIAGNOSTICS.json','DEPENDENCIES.source-only.json','HANDOFF.json',
 'METADATA_CHECK.json','PROTOCOL.md','REPAIR.diff','SOURCE_CORRESPONDENCE.json',
 'bootstrap_controls.source-only.py','launch_controls.source-only.py')


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


def one_case(identifier, root, baseline, module_bytes, module_pin):
    directory = root/identifier
    directory.mkdir(mode=0o700)
    operand = recipe(identifier, baseline, directory/'PROVENANCE_DOUBLE.json')
    with (directory/'PROVENANCE_DOUBLE.json').open('xb') as f:
        f.write(operand['private_bytes']); f.flush(); os.fsync(f.fileno())
    # The complete, already authenticated production file is loaded, never a snippet.
    spec = importlib.util.spec_from_file_location('ri144_isolated_'+identifier, module_pin['path'])
    P = importlib.util.module_from_spec(spec)
    exec(compile(module_bytes, module_pin['path'], 'exec'), P.__dict__)
    same(P.BOOTSTRAP, BOOTSTRAP, 'selected literal supplier constant')
    real_need, real_read = P.need, P.read
    trace = []; observed = {'returned_binding':None,'first_refusal':None}
    def traced_need(ok, message):
        trace.append({'kind':'gate','name':message,'passed':bool(ok)})
        return real_need(ok, message)
    def private_read(row):
        trace.append({'kind':'observer','name':'private_provenance_read'})
        same(row, operand['declared_provenance'], 'only declared private provenance may be read')
        return real_read(row)
    def supplier_ref(path):
        same(str(path), BOOTSTRAP, 'only supplier-byte double may be observed')
        trace.append({'kind':'observer','name':'supplier_bytes'})
        return parse(canonical(operand['observations']['bytes']))
    class SupplierPath:
        def lstat(self):
            trace.append({'kind':'observer','name':'supplier_lstat'})
            names = ('st_dev','st_ino','st_mode','st_nlink','st_size','st_mtime_ns','st_ctime_ns')
            return types.SimpleNamespace(**dict(zip(names,operand['observations']['state'])))
    def isolated_path(value):
        if str(value)==BOOTSTRAP: return SupplierPath()
        same(str(value), str(directory/'PROVENANCE_DOUBLE.json'), 'only private provenance path may be accessed')
        return Path(value)
    class Descriptor:
        @property
        def executable(self):
            trace.append({'kind':'observer','name':'interpreter_descriptor'})
            return operand['observations']['descriptor']
    # Only this fresh non-main module's observer names change. Real read/body,
    # parse/keys/same/opaque and selected_bootstrap implementations stay intact.
    P.need, P.read, P.ref, P.Path, P.sys = traced_need, private_read, supplier_ref, isolated_path, Descriptor()
    before = canonical({'dependencies':operand['dependencies'],'preflight':operand['preflight']})
    try:
        observed['returned_binding'] = P.selected_bootstrap(operand['preflight'], operand['dependencies'])
    except BaseException as error:
        observed['first_refusal'] = {'type':type(error).__name__,'message':str(error)}
    evidence = {'baseline_binding':baseline,'dependency_operand':operand['dependencies'],
        'preflight_operand':operand['preflight'],'observer_doubles':operand['observations'],
        'private_provenance_declared':operand['declared_provenance'],
        'private_provenance_actual':ref(directory/'PROVENANCE_DOUBLE.json'),
        'complete_loaded_module':module_pin,'captured_loaded_bytes':pure(module_bytes),
        'trace':trace,**observed,'inputs_unchanged':before==canonical({'dependencies':operand['dependencies'],'preflight':operand['preflight']}),
        'substitutions':['private provenance file and closure operand','supplier byte observation','supplier lstat observation','sys.executable descriptor'],
        'real_private_reader_parser_and_comparisons':True,'actual_supplier_observed':False,'production_authenticate_called':False,
        'expected_trace':operand['trace'],'expected_first_refusal':operand['refusal'],'expected_returned_binding':operand['return_binding']}
    failure = None
    try:
        same(trace,operand['trace'],'complete ordered gates and reached observers')
        same(observed['first_refusal'],operand['refusal'],'exact first refusal')
        same(observed['returned_binding'],operand['return_binding'],'whole returned six-field binding')
        same(evidence['inputs_unchanged'],True,'control operands unchanged')
    except BaseException as error:
        failure={'type':type(error).__name__,'message':str(error)}
    return {'id':identifier,'passed':failure is None,'error':failure,'evidence':evidence}


def authenticate_control(path, output):
    need(sys.flags.isolated==1 and sys.flags.dont_write_bytecode==1 and sys.flags.optimize==0,'normal isolated controls')
    admission_pin=ref(path); card=read(admission_pin)
    keys(card,('schema','status','launcher_handoff','target_handoff','sources','controls','output','environment_root',
               'command','independent_source_review','genuine_outer_required'),'closed bootstrap control card')
    same(card['schema'],'ri144-root-bootstrap-control-admission-v1','control card schema')
    same(card['status'],'AUTHORIZE_ONLY_FIFTEEN_ISOLATED_BOOTSTRAP_EXPECTATIONS','control authority')
    same(card['controls'],IDS,'fixed fifteen controls'); same(card['output'],str(output),'exact control output')
    same(card['genuine_outer_required'],True,'genuine external supervision required')
    deps=read(DEPENDENCY_PIN)
    for row in deps['opaque_files']: captured(row)
    same(card['target_handoff'],deps['target_handoff'],'exact source target')
    same(card['independent_source_review'],deps['target_review'],'accepted nonauthor target review')
    decision=read(deps['target_adjudication'])
    same(decision['status'],'ACCEPT_EXACT_SOURCE_WITH_EXECUTION_PREREQUISITES','accepted target source only')
    same(decision['source_handoff'],deps['target_handoff'],'decision target')
    same(decision['execution_admitted'],False,'historical source decision is not execution admission')
    sources={name:pure(body(HERE/name)) for name in SOURCE_NAMES};same(card['sources'],sources,'complete controls source pins')
    same(card['launcher_handoff']['path'],str(HERE/'HANDOFF.json'),'exact packet handoff')
    handoff=read(card['launcher_handoff']); own=handoff['files']+[card['launcher_handoff']]
    same(sorted(p.name for p in HERE.iterdir()),list(PACKET_NAMES),'source namespace')
    same(sorted(x['path'] for x in own),sorted(str(HERE/n) for n in PACKET_NAMES),'whole packet pin set')
    for row in own: captured(row)
    envroot=Path(card['environment_root']);same(dict(os.environ),environment(envroot),'exact controlled child environment')
    same(card['command'],[BOOTSTRAP,'-I','-B',str(HERE/'bootstrap_controls.source-only.py'),'--admission',str(path),'--output',str(output)],'only child command')
    same(sys.argv,card['command'][3:],'actual child arguments')
    need(output.is_absolute() and output.resolve()==output and not os.path.lexists(output) and output.parent.is_dir(),'fresh literal control output')
    for sealed in deps['sealed_namespace_roots']: need(separated(output,Path(sealed)),'control output overlaps sealed namespace')
    for row in [admission_pin,*own]: need(separated(output,Path(row['path'])),'output overlaps authenticated input')
    need(separated(output,envroot),'output overlaps environment')
    target_dependencies=read(deps['target_dependencies'])
    same(target_dependencies['selected_bootstrap_binding'],deps['selected_bootstrap_binding'],'whole genuine baseline selection')
    same(target_dependencies['bootstrap_selection_provenance'],deps['bootstrap_selection_provenance'],'authentic target provenance')
    provenance=read(deps['bootstrap_selection_provenance'])
    same(provenance['selected_bootstrap_binding'],deps['selected_bootstrap_binding'],'historical declaration baseline')
    return admission_pin,card,deps,own,sources,captured(deps['target_module'])


def run(path, output):
    admission_pin,card,deps,own,sources,module_bytes=authenticate_control(path,output)
    results=[];first=None;tails=[];started=time.monotonic()
    def tail(name, action):
        try: action()
        except BaseException as error: tails.append({'tail':name,'type':type(error).__name__,'message':str(error)})
    def source_tail():
        for row in own: captured(row)
        same(sorted(p.name for p in HERE.iterdir()),list(PACKET_NAMES),'source namespace after controls')
        for row in deps['opaque_files']: captured(row)
    def card_tail():
        captured(admission_pin);same(dict(os.environ),environment(Path(card['environment_root'])),'control environment after')
    output.mkdir(mode=0o700)
    try:
        captured(admission_pin)
        save(output/'ATTEMPT.json',{'schema':'ri144-controls-attempt-v1','admission':admission_pin,
             'target':deps['target_module'],'controls':IDS,'old25_rerun':False,'supplier_observation_is_double':True})
        for identifier in IDS:
            try: row=one_case(identifier,output,deps['selected_bootstrap_binding'],module_bytes,deps['target_module'])
            except BaseException as error:
                row={'id':identifier,'passed':False,'error':{'type':type(error).__name__,'message':str(error)},'evidence':None}
            results.append(row)
            if not row['passed'] and first is None: first={'case':identifier,**row['error']}
    except BaseException as error: first=first or {'type':type(error).__name__,'message':str(error)}
    finally:
        tail('source_dependency',source_tail);tail('admission_environment',card_tail)
        passed=sum(row['passed'] is True for row in results)
        report={'schema':'ri144-fifteen-bootstrap-control-report-v1','status':'FIFTEEN_EXPECTATIONS_PASSED' if passed==15 and first is None and not tails else 'REFUSED_RETAIN_ALL_PARTIALS',
            'order':IDS,'controls':results,'counts':{'total':len(results),'passed':passed,'failed':len(results)-passed},
            'sources':sources,'target_handoff':deps['target_handoff'],'target_module':deps['target_module'],
            'admission':admission_pin,'output':str(output),'first_error':first,'independent_tail_errors':list(tails),
            'actual_supplier_observed':False,'production_authenticate_called':False,'old25_rerun':False,
            'scientific_execution':False,'current_runtime_qualified':False,'ret_paused':True,'elapsed_seconds':time.monotonic()-started}
        tail('report_write',lambda:save(output/'REPORT.json',report))
        tail('namespace_write',lambda:save(output/'NAMESPACE.json',{'schema':'ri144-control-namespace-v1','root':str(output),
             'entries':tree(output),'excluded_not_yet_written':['NAMESPACE.json'],'all_partials_retained':True}))
        if tails != report['independent_tail_errors']:
            raise RuntimeError(canonical({'first_error':first,'independent_tail_errors':tails}).decode('ascii'))
    return 0 if report['status']=='FIFTEEN_EXPECTATIONS_PASSED' else 1


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--admission',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    arguments=parser.parse_args();raise SystemExit(run(arguments.admission,arguments.output))
