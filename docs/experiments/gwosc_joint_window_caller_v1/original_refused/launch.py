"""RI121 bounded synthetic caller; prospective source, no execution authority."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import sys
import time

SCIENCE = {
 'primary.py': {'bytes':20346,'sha256':'aea35e5840d96e0aee1bacf258d94a735171e201ac1c02fee23a2151feed7d10'},
 'validator.py': {'bytes':23321,'sha256':'b915ae587e9193c51a66c79f0dd987adb9f1e114a285503297521729ab987707'},
 'qualify.py': {'bytes':14435,'sha256':'23ccba3faff451894fbfbd35024b5575e25fc42f1d6d4616e052d8a89ddb58c3'},
}
SCIENCE_ROOT = '/Volumes/AI_DATA/development/det-review-evidence/ri119-joint-window-source-119uwunz'
ROOT_REVIEW = {'path':'/Volumes/AI_DATA/development/det-review-evidence/ri119-root-source-review-kc_ahnj9/ROOT_ADJUDICATION.json',
               'bytes':4979,'sha256':'8e1deba9fc9f5fa02009aad02d5f7222dc4162aeb8d0f542d51eeca66d91de67'}
AUDIT_OK = {'status':'all_saved_fields_match','historical_controls_reexecuted':False,
            'scientific_independent_reconstruction':True}
VALIDATION_OK = {'status':'all_fields_independently_match','cases':9,'bounds':3,'groups':12}


def row_body(row,control):
    control.require(type(row) is dict and set(row)=={'path','bytes','sha256'},'exact evidence pin missing')
    path=Path(row['path'])
    control.require(path.is_absolute() and path==path.resolve() and not path.is_symlink(),'evidence path differs')
    return control.verified_body(path,{k:row[k] for k in ('bytes','sha256')})


def parsed_row(row,control):
    body=row_body(row,control);value=control.parse_json(body)
    control.require(body==control.canonical(value),'noncanonical evidence')
    return value


def source_admission(manifest,control):
    root=Path(manifest['root'])
    evidence=manifest['evidence']
    control.require(set(evidence)=={'scientific_source_acceptance','caller_source_acceptance','runtime_acceptance'},'evidence keys')
    control.require(evidence['scientific_source_acceptance']==ROOT_REVIEW,'RI119 acceptance differs')
    source=parsed_row(ROOT_REVIEW,control)
    control.require(source['schema']=='ri119-root-synthetic-source-adjudication-v1' and
                    source['status']=='ACCEPT_SCIENTIFIC_SOURCE_AND_CONTRACT_ONLY' and
                    source['qualification_executed'] is False and source['active_execution_admission'] is False,
                    'RI119 source-only status differs')
    expected=[{'relative':name,'original':SCIENCE_ROOT+'/'+name,'copy':str(root/'science'/name),'pin':pin}
              for name,pin in SCIENCE.items()]
    control.require(manifest['sources']==expected and manifest['inputs']==[], 'exact three-source empty-input closure differs')
    control.require([Path(x['path']).name for x in manifest['helpers']]==
                    ['control.py','runtime_support.py','launch.py','worker.py'],'complete caller helper closure differs')
    control.require(all(x['path']==str(root/Path(x['path']).name) for x in manifest['helpers']), 'helper path differs')
    history=parsed_row(manifest['history_closure'],control)
    control.require(type(history) is list and len({x['path'] for x in history})==len(history), 'provenance closure inventory')
    for row in history: row_body(row,control)
    control.require(ROOT_REVIEW in history,'scientific source review omitted from provenance')
    caller=parsed_row(evidence['caller_source_acceptance'],control)
    control.require(caller['schema']=='ri121-root-caller-source-adjudication-v1' and
                    caller['status']=='ACCEPT_EXACT_SYNTHETIC_CALLER_SOURCE_ONLY' and
                    caller['target_execution'] is False and caller['helpers']==manifest['helpers'] and
                    caller['sources']==expected and caller['history_closure']==manifest['history_closure'] and
                    caller['fixed_limits']==manifest['limits'] and caller['report_domain']==manifest['report_domain'],
                    'current caller source acceptance differs')
    domain=parsed_row(manifest['report_domain'],control)
    control.require(domain['schema']=='ri121-declared-report-domain-v1' and
                    domain['status']=='SOURCE_ORACLE_DECLARATION_NOT_AN_EXECUTED_RESULT', 'declared report domain status')
    control.require(manifest['claim']=='Fixed synthetic joint-window arithmetic qualification only; no empirical or physical validation.', 'claim boundary differs')
    template_row=caller['source_template']
    control.require(template_row['path']==str(root/'MANIFEST.source-only-template.json'),'source template path differs')
    template=parsed_row(template_row,control)
    control.require(template['schema']=='ri121-source-only-manifest-template-v1' and
                    template['status']=='NOT_AUTHORIZED_SOURCE_TEMPLATE_ONLY','invalid prospective template')
    normalized=control.parse_json(control.canonical(manifest))
    normalized['schema']=template['schema'];normalized['status']=template['status']
    normalized['runtime_inventory']=None;normalized['expected_runtime']=None
    normalized['evidence']['caller_source_acceptance']=None
    normalized['evidence']['runtime_acceptance']=None
    control.require(control.canonical(normalized)==control.canonical(template),
                    'active manifest differs outside explicit root-owned runtime/acceptance slots')
    runtime=parsed_row(evidence['runtime_acceptance'],control)
    control.require(runtime['schema']=='ri121-root-current-runtime-adjudication-v1' and
                    runtime['status']=='ACCEPT_CURRENT_STDLIB_INTERPRETER_CLOSURE' and
                    runtime['runtime_inventory']==manifest['runtime_inventory'] and
                    runtime['interpreter']==manifest['interpreter'] and
                    runtime['expected_runtime']==manifest['expected_runtime'] and
                    runtime['complete_pure_python_stdlib'] is True and runtime['site_startup_surface_bound'] is True and
                    runtime['non_os_shared_library_closure_bound'] is True and
                    runtime['fresh_actual_profile_checked'] is True and runtime['scientific_targets_executed'] is False,
                    'fresh actual runtime prerequisite not established')
    return {'evidence':evidence,'history_closure':manifest['history_closure'],'history':history,
            'source_count':3,'inputs':[],'boundary':'RI119 source and current caller/runtime acceptance; qualification must execute now.'}


def mode_admission(manifest,mode,control):
    root=Path(manifest['root']);path=root/('ADMIT_'+mode.upper()+'.json')
    control.require(manifest['mode_admissions'][mode]==str(path) and path==path.resolve() and
                    not path.is_symlink(),'mode admission path differs')
    body=control.verified_body(path,control.file_pin(path));value=control.parse_json(body)
    control.require(body==control.canonical(value),'noncanonical mode admission')
    required={'schema','status','mode','phase','freeze','caller_source_acceptance','command','launcher_command','normal_acceptance'}
    control.require(type(value) is dict and set(value)==required and
                    value['schema']=='ri121-root-mode-admission-v1' and value['status']=='AUTHORIZED_SINGLE_SYNTHETIC_MODE' and
                    value['mode']==mode and value['phase']==manifest['phase'] and
                    value['freeze']==control.file_pin(root/'AUTHORIZED_FREEZE.json') and
                    value['caller_source_acceptance']==manifest['evidence']['caller_source_acceptance'] and
                    value['command']==manifest['runs'][mode]['command'] and
                    value['launcher_command']==manifest['runs'][mode]['launcher_command'],'separate root mode admission differs')
    if mode=='normal':
        control.require(value['normal_acceptance'] is None,'normal admission cannot claim future completion')
    else:
        review=parsed_row(value['normal_acceptance'],control);run=manifest['runs']['normal']
        control.require(review['schema']=='ri121-root-normal-synthetic-review-v1' and
                        review['status']=='ACCEPT_NORMAL_SYNTHETIC_EXECUTION_AND_CUSTODY' and
                        review['freeze']==value['freeze'] and review['all41_controls_per_implementation'] is True and
                        review['complete_independent_saved_validation'] is True and
                        review['receipt']=={'path':run['receipt'],**control.file_pin(run['receipt'])} and
                        review['result']=={'path':run['stdout'],**control.file_pin(run['stdout'])} and
                        review['worker']=={'path':run['worker_receipt'],**control.file_pin(run['worker_receipt'])} and
                        review['custody']=={'path':run['custody'],**control.file_pin(run['custody'])},
                        'normal review not bound to actual completed attempt')
        row_body(review['genuine_outer'],control)
    return {'path':str(path),'pin':control.identity(body),'normal_acceptance':value['normal_acceptance']}


def captured_module(name,path,body):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None or name in sys.modules: raise ValueError('captured module unavailable')
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module
    exec(compile(body,str(path),'exec'),module.__dict__)
    return module


def runtime_helper(manifest,control):
    name='ri121_runtime_support'
    if name in sys.modules:return sys.modules[name]
    row=next(x for x in manifest['helpers'] if Path(x['path']).name=='runtime_support.py')
    return captured_module(name,row['path'],control.verified_body(row['path'],row['pin']))


def current_runtime(manifest,control):
    return runtime_helper(manifest,control).verify(manifest,control)


def current_profile(manifest,mode,control):
    return runtime_helper(manifest,control).profile(manifest,mode,control)


def verify_custody(manifest,mode,control):
    """Parent checks complete retained report and actual worker bindings.

    Does not rerun scientific targets outside the child budget or pretend a
    saved label comparison independently witnesses historical execution.
    """
    run=manifest['runs'][mode]
    custody_body=control.verified_body(run['custody'],control.file_pin(run['custody']))
    value=control.parse_json(custody_body)
    control.require(control.canonical(value)==custody_body,'noncanonical custody bytes')
    keys={'schema','phase','mode','report','freeze','captured_sources','saved_result_validation',
          'scientific_validation','full_validator_passed','genuine_run_completed','inputs','claim'}
    control.require(type(value) is dict and set(value)==keys and value['schema']=='ri121-synthetic-custody-v1' and
                    value['phase']==manifest['phase'] and value['mode']==mode and value['inputs']==[] and
                    value['claim']==manifest['claim'] and value['freeze']==control.file_pin(Path(manifest['root'])/'AUTHORIZED_FREEZE.json'),
                    'synthetic custody envelope differs')
    pin=control.file_pin(run['stdout'])
    control.require(pin['bytes']<=2097152,'saved qualification body bound')
    body=control.verified_body(run['stdout'],pin);report=control.parse_json(body)
    control.require(control.canonical(report)==body,'whole canonical qualification bytes differ')
    domain=parsed_row(manifest['report_domain'],control)
    # All fields except scientific_result are a complete source-defined oracle.
    control.require(type(report) is dict and set(report)==set(domain['qualification_envelope'])|{'scientific_result'},'qualification root')
    control.require(canonical_pin({k:v for k,v in report.items() if k!='scientific_result'})==
                    canonical_pin(domain['qualification_envelope']),'full saved controls/scope/counts/coverage differ')
    science=report['scientific_result']
    control.require(type(science) is dict and set(science)==set(domain['scientific_envelope'])|{'cases','bounds'},'scientific root')
    control.require(canonical_pin({k:v for k,v in science.items() if k not in ('cases','bounds')})==
                    canonical_pin(domain['scientific_envelope']),'complete scientific scope/method differs')
    control.require(type(science['cases']) is list and [x.get('id') for x in science['cases']]==domain['case_ids'] and
                    type(science['bounds']) is list and [x.get('id') for x in science['bounds']]==domain['bound_ids'],'complete case/bound inventory')
    control.require(value['report']=={'path':run['stdout'],**pin} and value['captured_sources']==SCIENCE and
                    value['full_validator_passed'] is True and value['genuine_run_completed'] is True and
                    canonical_pin(value['saved_result_validation'])==canonical_pin(AUDIT_OK) and
                    canonical_pin(value['scientific_validation'])==canonical_pin(VALIDATION_OK),'genuine run/full saved validation custody differs')
    return {'custody_pin':control.file_pin(run['custody']),'report_pin':pin,'captured_sources':SCIENCE,
            'saved_result_validation':AUDIT_OK,'scientific_validation':VALIDATION_OK,
            'full_validator_passed':True,'genuine_run_completed':True}


def canonical_parts(value):
    for piece in json.JSONEncoder(sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False).iterencode(value):
        yield piece.encode('ascii')
    yield b'\n'



def canonical_pin(value):
    digest, length = hashlib.sha256(), 0
    for piece in canonical_parts(value):
        digest.update(piece)
        length += len(piece)
    return {'bytes':length,'sha256':digest.hexdigest()}



def file_equal(left, right):
    with Path(left).open('rb') as a, Path(right).open('rb') as b:
        while True:
            aa, bb = a.read(1024 * 1024), b.read(1024 * 1024)
            if aa != bb:
                return False
            if not aa:
                return True



def monitor_text(value):
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.decode('ascii', errors='backslashreplace')
    return str(value)



def reap_owned(child, record, started):
    """Terminate only our started session; an exit race still reaches wait()."""
    if child.poll() is None:
        try:
            os.killpg(child.pid, signal.SIGKILL)
        except ProcessLookupError:
            record.setdefault('termination_events', []).append('owned_process_group_already_exited')
    record['child_exit_code'] = child.wait()
    if record.get('child_elapsed_seconds') is None:
        record['child_elapsed_seconds'] = time.monotonic() - started
    elapsed = record['child_elapsed_seconds']
    gap = elapsed - record['samples'][-1]['elapsed_seconds'] if record['samples'] else None
    record['final_sample_to_reap_gap_seconds'] = gap
    record['final_sample_gap_passed'] = gap is not None and gap <= 0.1
    if record['stop_reason'] is None:
        if elapsed > 180:
            record['stop_reason'] = 'wall_time_limit'
        elif gap is None:
            record['stop_reason'] = 'no_rss_sample'
        elif gap > 0.1:
            record['stop_reason'] = 'rss_final_sample_deadline_missed'



def admit_command(manifest, mode, control):
    """The exact worker-argv guard used by main and fabricated negative controls."""
    root = Path(manifest['root'])
    command = [manifest['interpreter']['named_path'], '-I', '-B']
    if mode == 'optimized':
        command.append('-O')
    command += [str(root / 'worker.py'), str(root / 'AUTHORIZED_FREEZE.json'), mode]
    control.require(manifest['runs'][mode]['command'] == command, 'worker command differs')
    return command



def main():
    if len(sys.argv) != 3 or sys.argv[2] not in ('normal', 'optimized'):
        raise ValueError('expected authorized manifest and one mode')
    freeze_path, mode = Path(sys.argv[1]), sys.argv[2]
    root = Path(__file__).resolve().parent
    if freeze_path != root / 'AUTHORIZED_FREEZE.json' or freeze_path != freeze_path.resolve() or freeze_path.is_symlink():
        raise ValueError('unexpected authorization path')
    raw = freeze_path.read_bytes()
    manifest = json.loads(raw)
    item = next(row for row in manifest['helpers'] if row['path'] == str(root / 'control.py'))
    body = (root / 'control.py').read_bytes()
    if {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()} != item['pin']:
        raise ValueError('control source differs before import')
    spec = importlib.util.spec_from_file_location('ri121_supervisor_control', root / 'control.py')
    control = importlib.util.module_from_spec(spec)
    exec(compile(body, str(root / 'control.py'), 'exec'), control.__dict__)
    manifest = control.parse_json(raw)
    control.require(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
                    sys.flags.optimize == (0 if mode == 'normal' else 1), 'supervisor flags differ')
    control.require(dict(os.environ) == manifest['environment'], 'supervisor environment differs')
    phase = manifest['phase']
    expected = {'fabricated_joint_window_qualification': ('ri121-synthetic-qualification-freeze-v1', 'authorized_synthetic_qualification')}
    control.require(phase in expected and (manifest['schema'], manifest['status']) == expected[phase], 'prospective phase is not authorization')
    control.require(raw == control.canonical(manifest) and manifest['root'] == str(root), 'noncanonical freeze/root')
    control.require(manifest['limits'] == {'wall_seconds': 180, 'rss_kib': 524288,
                        'target_poll_seconds': 0.025, 'maximum_sample_gap_seconds': 0.1, 'ps_timeout_seconds': 0.05}, 'resource limits differ')
    control.require(manifest['environment'] == {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TZ': 'UTC',
                       'TMPDIR': str(root / 'tmp'), 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1',
                       'MKL_NUM_THREADS': '1', 'VECLIB_MAXIMUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1',
                       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}, 'exact environment differs')
    control.require(manifest['context'] == 'fixed_synthetic_joint_window_arithmetic_only', 'synthetic context differs')
    run = manifest['runs'][mode]
    admit_command(manifest, mode, control)
    launcher_command=[manifest['interpreter']['named_path'],'-I','-B']
    if mode=='optimized': launcher_command.append('-O')
    launcher_command += [str(root/'launch.py'),str(root/'AUTHORIZED_FREEZE.json'),mode]
    control.require(run['launcher_command']==launcher_command,'outer command differs')
    suffixes = {'stdout':'RESULT.json','stderr':'stderr','receipt':'receipt.json',
                'worker_receipt':'runtime.json','claim':'attempt.json','custody':'CUSTODY.json'}
    for key, suffix in suffixes.items():
        path = root / 'controls' / mode / suffix
        control.require(run[key] == str(path) and path.parent == path.parent.resolve(), 'exclusive output path differs')
        control.require(not path.exists() and not path.is_symlink(), 'prior attempt/output exists')
    admission_before = mode_admission(manifest, mode, control)
    previous = None
    if mode == 'optimized':
        previous = control.parse_json(Path(manifest['runs']['normal']['receipt']).read_bytes())
        control.require(previous['success'] is True and previous['freeze'] == control.identity(raw) and previous['phase'] == phase,
                        'normal predecessor not successful on same freeze')
        for key in ('stdout', 'stderr', 'worker_receipt', 'custody'):
            control.require(control.file_pin(manifest['runs']['normal'][key]) == previous['outputs'][key], 'normal output drift')
        control.require(verify_custody(manifest, 'normal', control) == previous['verified_custody'], 'normal custody drift')
    record = {'schema': 'ri121-synthetic-supervisor-receipt-v1', 'phase': phase, 'mode': mode,
              'freeze': control.identity(raw), 'command': run['command'], 'environment': manifest['environment'],
              'limits': manifest['limits'], 'source_before': None, 'source_after': None, 'runtime_before': None, 'runtime_after': None,
              'acceptance_before': None, 'acceptance_after': None, 'mode_admission_before': admission_before, 'mode_admission_after': None, 'process_before': None, 'process_after': None, 'loaded_modules_before': None, 'loaded_modules_after': None, 'verified_custody': None, 'samples': [], 'monitor_attempts': [],
              'peak_sampled_rss_kib': 0, 'child_exit_code': None, 'child_elapsed_seconds': None, 'stop_reason': None, 'success': False, 'outputs': {},
              'monitor_scope': 'one reviewed RI121 synthetic worker; sampled RSS, not a hard OS cap'}
    control.write_exclusive(run['claim'], {'freeze': record['freeze'], 'phase': phase, 'mode': mode, 'command': run['command']})
    child, started = None, None
    try:
        record['source_before'] = control.verify_sources(manifest)
        record['acceptance_before'] = source_admission(manifest, control)
        record['runtime_before'] = current_runtime(manifest, control)
        record['process_before'] = current_profile(manifest, mode, control)
        record['loaded_modules_before'] = runtime_helper(manifest, control).loaded_files(manifest, control)
        with Path(run['stdout']).open('xb') as out, Path(run['stderr']).open('xb') as err:
            started = time.monotonic()
            child = subprocess.Popen(run['command'], cwd=root, env=manifest['environment'], stdout=out, stderr=err, start_new_session=True)
            last_sample = started
            while child.poll() is None:
                now = time.monotonic()
                if now - started > 180:
                    record['stop_reason'] = 'wall_time_limit'
                    break
                if now - last_sample > 0.1:
                    record['stop_reason'] = 'rss_sample_deadline_missed'
                    break
                try:
                    observation = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(child.pid)], stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE, timeout=0.05, check=False)
                except BaseException as exc:
                    record['monitor_attempts'].append({'elapsed_seconds': time.monotonic() - started,
                        'exception': type(exc).__name__, 'message': str(exc),
                        'stdout': monitor_text(getattr(exc, 'stdout', None)),
                        'stderr': monitor_text(getattr(exc, 'stderr', None))})
                    raise
                stamp = time.monotonic()
                record['monitor_attempts'].append({'elapsed_seconds': stamp - started, 'returncode': observation.returncode,
                    'stdout': monitor_text(observation.stdout), 'stderr': monitor_text(observation.stderr)})
                finished = child.poll() is not None
                text = observation.stdout.strip()
                if observation.returncode != 0 or not text.isdigit():
                    if finished:
                        break
                    record['stop_reason'] = 'rss_monitor_unavailable'
                    break
                rss = int(text)
                record['samples'].append({'elapsed_seconds': stamp - started, 'rss_kib': rss, 'gap_seconds': stamp - last_sample})
                record['peak_sampled_rss_kib'] = max(record['peak_sampled_rss_kib'], rss)
                if stamp - last_sample > 0.1:
                    record['stop_reason'] = 'rss_sample_deadline_missed'
                    break
                last_sample = stamp
                if rss > 524288:
                    record['stop_reason'] = 'sampled_resident_memory_limit'
                    break
                if finished:
                    break
                time.sleep(min(0.025, max(0.0, 180 - (time.monotonic() - started))))
            reap_owned(child, record, started)
    except BaseException as exc:
        record['stop_reason'] = 'supervisor_' + type(exc).__name__
        record['error'] = str(exc)
    finally:
        if child is not None:
            try:
                reap_owned(child, record, started)
            except BaseException as exc:
                record['termination_error'] = {'type': type(exc).__name__, 'message': str(exc)}
                record['stop_reason'] = 'owned_child_termination_failed'
                if record.get('child_elapsed_seconds') is None:
                    record['child_elapsed_seconds'] = time.monotonic() - started
        try:
            record['mode_admission_after'] = mode_admission(manifest, mode, control)
            control.require(record['mode_admission_after'] == record['mode_admission_before'], 'mode admission changed')
            record['process_after'] = current_profile(manifest, mode, control) if record['process_before'] is not None else None
            control.require(record['process_after'] == record['process_before'], 'current process profile changed')
            record['loaded_modules_after'] = runtime_helper(manifest, control).loaded_files(manifest, control)
            if record['loaded_modules_before'] is not None:
                control.require(all(record['loaded_modules_after'].get(k) == v for k,v in record['loaded_modules_before'].items()), 'loaded origins changed')
            record['source_after'] = control.verify_sources(manifest)
            record['runtime_after'] = current_runtime(manifest, control)
            record['acceptance_after'] = source_admission(manifest, control) if record['acceptance_before'] is not None else None
            control.require(record['acceptance_after'] == record['acceptance_before'], 'source acceptance evidence changed')
            for key in ('stdout', 'stderr', 'worker_receipt', 'custody'):
                if Path(run[key]).exists():
                    record['outputs'][key] = control.file_pin(run[key])
            if record['child_exit_code'] == 0 and record['stop_reason'] is None:
                worker = control.parse_json(Path(run['worker_receipt']).read_bytes())
                control.require(worker['schema'] == 'ri121-synthetic-worker-receipt-v1' and worker['phase'] == phase and worker['mode'] == mode and
                                type(worker['exit_code']) is int and worker['exit_code'] == 0 and worker['error'] is None and worker['freeze'] == record['freeze'],
                                'worker completion receipt failed')
                control.require(worker['operation']['result'] == {'path': run['stdout'], **record['outputs']['stdout']} and
                                worker['operation']['custody'] == {'path': run['custody'], **record['outputs']['custody']}, 'worker output binding differs')
                control.require(record['outputs']['stderr'] == {'bytes':0,'sha256':hashlib.sha256(b'').hexdigest()}, 'worker stderr not empty')
                control.require(worker['source_before'] == worker['source_after'] == record['source_before'] == record['source_after'] and
                                worker['runtime_bytes_before'] == worker['runtime_bytes_after'] == record['runtime_before'] == record['runtime_after'] and
                                worker['runtime_before'] == worker['runtime_after'] == record['process_before'] == record['process_after'] and
                                worker['acceptance_before'] == worker['acceptance_after'] == record['acceptance_before'] == record['acceptance_after'],
                                'worker/parent source runtime acceptance differs')
                control.require(worker['mode_admission_before'] == worker['mode_admission_after'] == record['mode_admission_before'] == record['mode_admission_after'], 'root mode admission drift')
                control.require(worker['captured_sources_before'] == worker['captured_sources_after'] == SCIENCE and
                                worker['full_validator_passed'] is True and worker['genuine_run_started'] is True and
                                worker['genuine_run_completed'] is True and worker.get('postcheck_error') is None,
                                'captured run/full validation sequence differs')
                control.require(type(worker['loaded_modules_before']) is dict and type(worker['loaded_modules_after']) is dict and
                                all(worker['loaded_modules_after'].get(k) == v for k,v in worker['loaded_modules_before'].items()),
                                'worker loaded-module origins changed')
                record['verified_custody'] = verify_custody(manifest, mode, control)
                control.require(canonical_pin(worker['saved_result_validation']) == canonical_pin(AUDIT_OK) and
                                canonical_pin(worker['scientific_validation']) == canonical_pin(VALIDATION_OK),
                                'complete saved audit/scientific validation binding differs')
                if mode == 'optimized':
                    normal = manifest['runs']['normal']
                    control.require(control.file_pin(normal['stdout']) == previous['outputs']['stdout'] == record['outputs']['stdout'] and
                                    file_equal(normal['stdout'], run['stdout']), 'normal/optimized scientific bytes differ')
                    control.require(verify_custody(manifest, 'normal', control) == previous['verified_custody'], 'normal custody changed')
                    control.require(previous['verified_custody']['report_pin'] == record['verified_custody']['report_pin'] and
                                    previous['verified_custody']['captured_sources'] == record['verified_custody']['captured_sources'],
                                    'mode report/source identity differs')
                record['success'] = True
        except BaseException as exc:
            record['stop_reason'] = 'postcheck_' + type(exc).__name__
            record['postcheck_error'] = str(exc)
            record['success'] = False
        control.write_exclusive(run['receipt'], record)
    return 0 if record['success'] else 1



if __name__ == '__main__':
    raise SystemExit(main())
