"""RI141 direct-bootstrap successor of RI135; NONSCIENTIFIC preparation only. UNEXECUTED.

Root authenticates this bootstrap script, its supplier and every admission
before startup. No invocation of WHITE targets, fixture makers or science
launchers exists here. Root still owns all acceptance and genuine outer custody.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
PACKET = Path('/Volumes/AI_DATA/development/det-review-evidence/ri130-white-qualification-caller-source-Q4Aq7hZg')
BOOTSTRAP = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
CAP = 67108864
PHASES = ('capture', 'profile_normal', 'profile_optimized', 'guards')
SOURCE_NAMES = ('prepare.py', 'runtime_metadata.py', 'DEPENDENCIES.source-only.json')
GUARD_HELPERS = ('control.py', 'caller_contract.py', 'evidence.py', 'monitor.py', 'worker.py', 'launch.py', 'runtime_support.py')
GUARD_IDS = tuple([side+'_'+kind for side in ('parent','worker') for kind in ('source','caller','runtime_acceptance','mode','late','late_postcheck')]
 +['capture_'+x for x in ('positive','changed_copy','buffer_drift','occupied')]
 +['monitor_'+x for x in ('positive','no_sample','wall','initial_gap','sample_gap','rss','nonzero','malformed','timeout','final_gap')]
 +['runtime_'+x for x in ('positive','absent_file','absent_dangling_link','missing_loader','changed_loader_declaration','changed_loader_path','missing_config')]
 +['static_'+x for x in ('positive','actual','extra','bool_limit','source_omitted','source_copy','helper_omitted','mode_command')]
 +['acceptance_'+x for x in ('positive','source_execution','caller_binding','caller_history','caller_ret','guards_absent','runtime_binding','runtime_loader','runtime_profile')]
 +['mode_'+x for x in ('normal_positive','optimized_positive','wrong_command','pre_missing','normal_incomplete','normal_drift')]
 +['relation_'+x for x in ('positive','science_file','wrong_link','extra_envelope','missing_artifact','postcheck','extra_namespace','control_message','tail_dropped')])
BOUNDS = {'snapshot_seconds': 180, 'profile_seconds': 30, 'guard_seconds': 180,
          'rss_kib': 524288, 'target_poll_seconds': 0.025, 'maximum_sample_gap_seconds': 0.1,
          'ps_timeout_seconds': 0.05, 'file_bytes': CAP, 'driver_soft_seconds': 900,
          'genuine_outer_timeout_seconds': 960}
M = None


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')


def same(a, b, message):
    need(canonical(a) == canonical(b), message)


def keys(value, names, message):
    need(type(value) is dict and set(value) == set(names), message)


def pure(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def body(path):
    path = Path(path)
    need(path.is_absolute() and path.resolve(strict=True) == path and not path.is_symlink(), 'literal source/metadata path')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= CAP, 'bounded regular source/metadata')
    state = lambda x: (x.st_dev, x.st_ino, x.st_mode, x.st_nlink, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as stream:
        need(state(os.fstat(stream.fileno())) == state(before), 'metadata opened drift')
        value = stream.read(CAP+1)
        need(state(os.fstat(stream.fileno())) == state(before), 'metadata descriptor drift')
    need(state(path.lstat()) == state(before) and len(value) == before.st_size <= CAP, 'metadata read drift')
    return value


def ref(path):
    return {'path': str(path), **pure(body(path))}


def parse(data):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, 'duplicate metadata key')
            value[key] = item
        return value
    def bad(_):
        raise ValueError('nonfinite metadata')
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=bad)
    need(canonical(value) == data, 'canonical metadata framing')
    return value


def read(row):
    keys(row, ('path', 'bytes', 'sha256'), 'closed metadata FilePin')
    value = body(row['path'])
    same({'path': row['path'], **pure(value)}, row, 'metadata reference drift')
    return parse(value)


def opaque(row):
    same(ref(row['path']), row, 'opaque evidence reference drift')
    return row


def save(path, value):
    data = canonical(value)
    need(len(data) <= CAP, 'bounded emitted metadata')
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    return ref(path)


def environment(root):
    return {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TZ': 'UTC', 'TMPDIR': str(root/'tmp'),
            'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
            'VECLIB_MAXIMUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1', '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}


def source_set():
    return {name: pure(body(HERE/name)) for name in SOURCE_NAMES}


def selected_bootstrap(preflight, dependencies):
    """Authenticate the direct supplier; genuine startup/loader custody is external."""
    provenance = dependencies['bootstrap_selection_provenance']
    need(provenance in dependencies['opaque_files'], 'bootstrap selection provenance absent from closure')
    historical = read(provenance)
    same(historical['selected_bootstrap_binding'], dependencies['selected_bootstrap_binding'],
         'accepted direct bootstrap selection provenance')
    binding = preflight['selected_interpreter_binding']
    keys(binding, ('path', 'resolved_path', 'bytes', 'sha256', 'state', 'symlink_chain'),
         'closed selected interpreter binding')
    same(binding, dependencies['selected_bootstrap_binding'], 'genuine preflight selected interpreter identity')
    same([binding['path'], binding['resolved_path'], binding['symlink_chain']],
         [BOOTSTRAP, BOOTSTRAP, []], 'literal direct bootstrap selection')
    opaque({key: binding[key] for key in ('path', 'bytes', 'sha256')})
    actual = Path(BOOTSTRAP).lstat()
    same([actual.st_dev, actual.st_ino, actual.st_mode, actual.st_nlink, actual.st_size,
          actual.st_mtime_ns, actual.st_ctime_ns], binding['state'], 'selected interpreter state drift')
    same(sys.executable, BOOTSTRAP, 'direct interpreter descriptor')
    return binding


def authenticate(path):
    """Post-startup checks complement, never replace, root pre-authentication."""
    admission = parse(body(path))
    keys(admission, ('schema', 'status', 'phase', 'sources', 'source_review', 'packet', 'output', 'environment_root',
                    'bootstrap', 'bootstrap_host_preflight', 'host', 'baseline_acceptance', 'normal_acceptance', 'profiles_acceptance',
                    'guard_admission', 'bounds', 'genuine_outer_required'), 'closed root preparation admission')
    need(admission['schema'] == 'ri141-root-preparation-admission-v1'
         and admission['status'] == 'AUTHORIZE_ONE_NONSCIENTIFIC_PREPARATION'
         and admission['phase'] in PHASES, 'separate preparation authorization')
    same(admission['sources'], source_set(), 'complete reviewed preparation source identities')
    opaque(admission['source_review'])
    same(admission['packet'], str(PACKET), 'exact accepted original RI130 packet')
    same(admission['bounds'], BOUNDS, 'fixed preparation bounds')
    need(admission['genuine_outer_required'] is True, 'actual outer custody required')
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'normal isolated bootstrap')
    root = Path(admission['output']); envroot = Path(admission['environment_root'])
    need(root.is_absolute() and root.resolve() == root and root != HERE and root != PACKET
         and HERE not in root.parents and PACKET not in root.parents, 'fresh external output namespace')
    need(envroot.is_absolute() and envroot.resolve(strict=True) == envroot
         and envroot not in (HERE, PACKET) and HERE not in envroot.parents and PACKET not in envroot.parents
         and (envroot/'tmp').is_dir() and (envroot/'tmp').resolve(strict=True) == envroot/'tmp', 'root-provided literal environment tmp')
    global M
    source = body(HERE/'runtime_metadata.py')
    same(pure(source), admission['sources']['runtime_metadata.py'], 'captured metadata helper identity')
    spec = importlib.util.spec_from_file_location('ri133_runtime_metadata', HERE/'runtime_metadata.py')
    M = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = M
    exec(compile(source, str(HERE/'runtime_metadata.py'), 'exec'), M.__dict__)
    same(source_set(), admission['sources'], 'source drift after helper load')
    dependencies = parse(body(HERE/'DEPENDENCIES.source-only.json'))
    need(dependencies['status'] == 'SEALED_SOURCE_DEPENDENCIES_NOT_RUNTIME_ACCEPTANCE', 'source dependency scope')
    same(M.BOOTSTRAP, BOOTSTRAP, 'driver and snapshot selected supplier agree')
    selected_bootstrap(read(admission['bootstrap_host_preflight']), dependencies)
    same(M.binding(BOOTSTRAP), admission['bootstrap'], 'externally bound bootstrap supplier')
    same({'uname': list(os.uname()), 'system_version': ref('/System/Library/CoreServices/SystemVersion.plist')}, admission['host'], 'root host check')
    return admission, dependencies


def acceptance(row, stage, admission):
    """External root decisions, never synthesized by this preparation source."""
    value = read(row)
    keys(value, ('schema', 'status', 'stage', 'sources', 'packet', 'environment_root', 'completions',
                 'genuine_outer', 'independent_review', 'scientific_execution'), 'closed root stage acceptance')
    need(value['schema'] == 'ri133-root-preparation-stage-review-v1'
         and value['status'] == 'ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE' and value['stage'] == stage,
         'external predecessor stage not accepted')
    for name in ('sources', 'packet', 'environment_root'):
        same(value[name], admission[name], 'accepted predecessor binding: ' + name)
    need(value['scientific_execution'] is False, 'predecessor scope')
    expected = {'baseline': ['capture'], 'normal': ['profile_normal'], 'profiles': ['profile_normal', 'profile_optimized']}[stage]
    same(list(value['completions']), sorted(expected), 'complete predecessor stage domain')
    same(list(value['genuine_outer']), sorted(expected), 'all genuine outer stage records')
    opaque(value['independent_review'])
    results = {}
    for phase in expected:
        result = read(value['completions'][phase])
        need(result['schema'] == 'ri133-preparation-completion-v1' and result['phase'] == phase
             and result['status'] == 'CAPTURED_FOR_INDEPENDENT_REVIEW' and result['first_error'] is None,
             'predecessor actual completion missing')
        same(result['sources'], admission['sources'], 'predecessor complete source binding')
        same(result['environment'], environment(Path(admission['environment_root'])), 'predecessor controlled environment')
        verify_saved_namespace(result, value['completions'][phase])
        # Root's saved genuine wrapper binds the actual returned tool receipt;
        # the raw tool output is retained opaquely and never self-generated here.
        outer = read(value['genuine_outer'][phase])
        keys(outer, ('schema', 'status', 'command', 'environment', 'exit_code', 'completion', 'raw_tool_receipt',
                     'external_timeout_seconds'), 'closed actual outer wrapper')
        need(outer['schema'] == 'ri133-root-genuine-outer-v1' and outer['status'] == 'ACTUAL_TOOL_COMPLETION'
             and type(outer['exit_code']) is int and outer['exit_code'] == 0, 'actual outer success absent')
        same(outer['completion'], value['completions'][phase], 'actual outer completion binding')
        same(outer['command'], result['command'], 'actual outer exact command')
        same(outer['environment'], result['environment'], 'actual outer exact environment')
        same(outer['external_timeout_seconds'], 960, 'actual outer preparation timeout')
        opaque(outer['raw_tool_receipt'])
        results[phase] = result
    return results


def verify_saved_namespace(result, completion_ref):
    keys(result, ('schema', 'phase', 'status', 'command', 'environment', 'admission', 'sources', 'artifacts',
        'first_error', 'independent_tail_errors', 'elapsed_seconds', 'scientific_targets_executed', 'actual_data_admitted',
        'full32_qualified', 'ret_paused', 'runtime_acceptance_created', 'genuine_outer_created'), 'closed saved completion')
    need(result['first_error'] is None and result['independent_tail_errors'] == [], 'successful saved completion has no discarded tails')
    for name in ('scientific_targets_executed', 'actual_data_admitted', 'full32_qualified', 'runtime_acceptance_created', 'genuine_outer_created'):
        need(result[name] is False, 'saved preparation scope '+name)
    need(result['ret_paused'] is True, 'RET remains paused')
    expected = {'PRE', 'PRE_completion', 'POST', 'POST_completion', 'checks', 'namespace'}
    if result['phase'].startswith('profile_'): expected.update(('PROFILE', 'PROFILE_completion'))
    if result['phase'] == 'guards': expected.update(('GUARDS_completion', 'GUARD_REPORT'))
    same(sorted(result['artifacts']), sorted(expected), 'complete saved artifact reference domain')
    root = Path(completion_ref['path']).parent
    same(completion_ref['path'], str(root/'COMPLETE.json'), 'saved completion location')
    filenames = {'PRE': 'PRE.stdout', 'POST': 'POST.stdout', 'PRE_completion': 'PRE.COMPLETION.json',
                 'POST_completion': 'POST.COMPLETION.json', 'checks': 'CHECKS.json', 'namespace': 'NAMESPACE.json',
                 'PROFILE': 'PROFILE.stdout', 'PROFILE_completion': 'PROFILE.COMPLETION.json',
                 'GUARDS_completion': 'GUARDS.COMPLETION.json', 'GUARD_REPORT': 'GUARD_REPORT.json'}
    for name, artifact in result['artifacts'].items():
        opaque(artifact)
        same(artifact['path'], str(root/filenames[name]), 'exact saved artifact role path')
    namespace = read(result['artifacts']['namespace'])
    keys(namespace, ('schema', 'root', 'entries', 'excluded_not_yet_written'), 'saved namespace fields')
    same(namespace['schema'], 'ri133-retained-namespace-v1', 'saved namespace schema')
    same(namespace['root'], str(root), 'saved namespace root')
    same(namespace['excluded_not_yet_written'], ['NAMESPACE.json', 'COMPLETE.json'], 'closed final two metadata exclusions')
    actual = M.tree(root)
    expected_entries = list(namespace['entries'])
    for name in ('NAMESPACE.json', 'COMPLETE.json'):
        item = ref(root/name)
        expected_entries.append({'relative': name, 'kind': 'file', 'bytes': item['bytes'], 'sha256': item['sha256']})
    same(actual, sorted(expected_entries, key=lambda item: item['relative']), 'complete saved file/directory/symlink namespace')
    check_top_namespace(root, result['phase'], actual)
    saved_admission = read(result['admission'])
    same(saved_admission['output'], str(root), 'saved admission owns root')
    same(saved_admission['phase'], result['phase'], 'saved phase admission')
    same(result['command'], [BOOTSTRAP, '-I', '-B', str(HERE/'prepare.py'), '--admission', result['admission']['path']], 'saved exact root invocation')
    for label in ['PRE', 'POST']+(['PROFILE'] if result['phase'].startswith('profile_') else ['GUARDS'] if result['phase'] == 'guards' else []):
        child = read(ref(root/(label+'.COMPLETION.json')))
        need(child['passed'] is True and child['first_error'] is None and child['tail_errors'] == []
             and child['stop_reason'] is None and type(child['child_exit_code']) is int and child['child_exit_code'] == 0,
             'actual child completion required '+label)
        opaque(child['stdout']); opaque(child['stderr'])
        same([child['stdout']['path'], child['stderr']['path']], [str(root/(label+'.stdout')), str(root/(label+'.stderr'))], 'child output namespace')
        need(child['stderr']['bytes'] == 0, 'saved child stderr')
        same(child['environment'], result['environment'], 'saved child environment')
        if label in ('PRE', 'POST'):
            command = [BOOTSTRAP, '-I', '-B', str(HERE/'prepare.py'), '--snapshot', result['admission']['path']]
        elif label == 'PROFILE':
            command = [M.VENV+'/bin/python', '-I', '-B']+(['-O'] if result['phase'] == 'profile_optimized' else [])+[str(PACKET/'profile_observe.source-only.py')]
        else:
            command = [M.VENV+'/bin/python', '-I', '-B', str(PACKET/'guard_controls.source-only.py'), '--packet', str(PACKET),
                       '--admission', saved_admission['guard_admission']['path'], '--output', str(root/'GUARD_REPORT.json')]
        same(child['command'], command, 'exact saved child command')
        attempt = read(ref(root/(label+'.ATTEMPT.json')))
        keys(attempt, ('command', 'environment', 'wall_seconds', 'pid_owner', 'scientific_target_entry'), 'closed actual child attempt')
        same(attempt['command'], command, 'actual child attempt command')
        same(attempt['environment'], result['environment'], 'actual child attempt environment')
        same(attempt['wall_seconds'], child['wall_seconds'], 'actual child attempt wall bound')
        need(type(attempt['pid_owner']) is int and attempt['pid_owner'] > 0 and attempt['scientific_target_entry'] is False, 'owned nonscientific child attempt')
        samples = child['samples']; need(type(samples) is list and bool(samples), 'at least one actual RSS sample')
        limit = 30 if label == 'PROFILE' else 180
        same(child['wall_seconds'], limit, 'saved per-stage wall bound')
        need(0 <= child['elapsed_seconds'] <= limit and 0 <= child['final_sample_to_reap_gap_seconds'] <= 0.1
             and child['final_sample_gap_passed'] is True, 'saved wall/final sample checks')
        previous = 0
        for sample in samples:
            keys(sample, ('elapsed_seconds', 'rss_kib', 'gap_seconds'), 'complete RSS sample')
            need(type(sample['rss_kib']) is int and 0 <= sample['rss_kib'] <= 524288
                 and 0 <= sample['gap_seconds'] <= 0.1 and sample['elapsed_seconds'] >= previous, 'saved RSS/gap bound')
            need(abs((sample['elapsed_seconds']-previous)-sample['gap_seconds']) < 1e-9, 'saved RSS gap reconstruction')
            previous = sample['elapsed_seconds']
        same(child['peak_sampled_rss_kib'], max(x['rss_kib'] for x in samples), 'saved peak reconstruction')
    need(type(result['elapsed_seconds']) in (int, float) and 0 <= result['elapsed_seconds'] <= 900, 'saved driver soft bound')
    same(read(result['artifacts']['PRE']), read(result['artifacts']['POST']), 'saved full pre/post metadata equality')
    return namespace


def check_top_namespace(root, phase, rows):
    expected = {'ATTEMPT.json', 'CHECKS.json', 'NAMESPACE.json', 'COMPLETE.json'}
    labels = ['PRE', 'POST']+(['PROFILE'] if phase.startswith('profile_') else ['GUARDS'] if phase == 'guards' else [])
    for label in labels:
        expected.update(label+suffix for suffix in ('.ATTEMPT.json', '.COMPLETION.json', '.stdout', '.stderr'))
    top = [row for row in rows if '/' not in row['relative']]
    if phase == 'guards':
        expected.add('GUARD_REPORT.json')
        report = read(ref(root/'GUARD_REPORT.json'))
        fixture = Path(report['fixture_root'])
        need(fixture.parent == root and fixture.name.startswith('ri130-nonscientific-guards-'), 'only owned guard fixture tree')
        expected.add(fixture.name)
    same(sorted(row['relative'] for row in top), sorted(expected), 'exact complete preparation top namespace')
    for row in top:
        need(row['kind'] == ('directory' if phase == 'guards' and row['relative'].startswith('ri130-nonscientific-guards-') else 'file'), 'top-level output kind')


def monitor_text(value):
    if value is None: return ''
    if isinstance(value, bytes): return value.decode('ascii', errors='backslashreplace')
    return str(value)


def child_run(command, out, label, seconds, env):
    """RI130 monitor/reap semantics, with an explicit preparation wall bound.

RSS samples observe only the owned child. Stable supplier/no descendants is a
premise; neither group termination nor samples constitute a hard OS quota.
"""
    stdout = out/(label+'.stdout'); stderr = out/(label+'.stderr')
    record = {'command': command, 'environment': env, 'wall_seconds': seconds,
              'samples': [], 'monitor_attempts': [], 'peak_sampled_rss_kib': 0,
              'stop_reason': None, 'child_exit_code': None, 'first_error': None, 'tail_errors': []}
    child = None
    started = time.monotonic()
    save(out/(label+'.ATTEMPT.json'), {'command': command, 'environment': env, 'wall_seconds': seconds,
                                     'pid_owner': os.getpid(), 'scientific_target_entry': False})
    try:
        with stdout.open('xb') as output, stderr.open('xb') as errors:
            child = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,
                                     cwd=out, env=env, start_new_session=True)
            last = started
            while child.poll() is None:
                now = time.monotonic()
                if now-started > seconds: record['stop_reason'] = 'wall_time_limit'; break
                if now-last > 0.1: record['stop_reason'] = 'rss_sample_deadline_missed'; break
                if stdout.stat().st_size > CAP or stderr.stat().st_size > CAP:
                    record['stop_reason'] = 'sampled_output_byte_limit'; break
                try:
                    observation = subprocess.run(['/bin/ps', '-o', 'rss=', '-p', str(child.pid)],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=0.05, check=False)
                except BaseException as exc:
                    record['monitor_attempts'].append({'elapsed_seconds': time.monotonic()-started,
                      'exception': type(exc).__name__, 'message': str(exc),
                      'stdout': monitor_text(getattr(exc, 'stdout', None)), 'stderr': monitor_text(getattr(exc, 'stderr', None))})
                    raise
                stamp = time.monotonic()
                record['monitor_attempts'].append({'elapsed_seconds': stamp-started, 'returncode': observation.returncode,
                   'stdout': monitor_text(observation.stdout), 'stderr': monitor_text(observation.stderr)})
                text = observation.stdout.strip()
                finished = child.poll() is not None
                if observation.returncode != 0 or not text.isdigit():
                    if finished: break
                    record['stop_reason'] = 'rss_monitor_unavailable'; break
                rss = int(text); gap = stamp-last
                record['samples'].append({'elapsed_seconds': stamp-started, 'rss_kib': rss, 'gap_seconds': gap})
                record['peak_sampled_rss_kib'] = max(record['peak_sampled_rss_kib'], rss)
                if gap > 0.1: record['stop_reason'] = 'rss_sample_deadline_missed'; break
                last = stamp
                if rss > 524288: record['stop_reason'] = 'sampled_resident_memory_limit'; break
                if finished: break
                time.sleep(min(0.025, max(0.0, seconds-(time.monotonic()-started))))
    except BaseException as exc:
        record['first_error'] = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        if child is not None:
            try:
                if child.poll() is None:
                    try: os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError: record.setdefault('termination_events', []).append('owned_group_already_exited')
                record['child_exit_code'] = child.wait()
                record['elapsed_seconds'] = time.monotonic()-started
                gap = record['elapsed_seconds']-record['samples'][-1]['elapsed_seconds'] if record['samples'] else None
                record['final_sample_to_reap_gap_seconds'] = gap
                record['final_sample_gap_passed'] = gap is not None and gap <= 0.1
                if record['stop_reason'] is None:
                    if record['elapsed_seconds'] > seconds: record['stop_reason'] = 'wall_time_limit'
                    elif gap is None: record['stop_reason'] = 'no_rss_sample'
                    elif gap > 0.1: record['stop_reason'] = 'rss_final_sample_deadline_missed'
            except BaseException as exc:
                record['tail_errors'].append({'type': type(exc).__name__, 'message': str(exc)})
        for name, path in [('stdout', stdout), ('stderr', stderr)]:
            try: record[name] = ref(path)
            except BaseException as exc:
                record[name] = None
                record['tail_errors'].append({'output': name, 'type': type(exc).__name__, 'message': str(exc)})
        record['passed'] = (record['first_error'] is None and not record['tail_errors'] and record['stop_reason'] is None
                            and record['child_exit_code'] == 0 and record['stderr'] is not None and record['stderr']['bytes'] == 0)
        save(out/(label+'.COMPLETION.json'), record)
    need(record['passed'], 'bounded child refused: '+label)
    return record
def dyld_attempts(message, preobserved):
    """Parse the ENTIRE saved dyld failure, including all repeated attempts."""
    extension = M.STDLIB+'/lib-dynload/_decimal.cpython-311-darwin.so'
    prefix = 'dlopen('+extension+', 0x0002): Library not loaded: /opt/homebrew/opt/mpdecimal/lib/libmpdec.3.dylib\n'
    need(type(message) is str and message.startswith(prefix), 'complete expected dlopen/library header')
    remainder = message[len(prefix):]
    match = re.match(r'  Referenced from: <[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}> '+re.escape(extension)+r'\n  Reason: tried: ', remainder)
    need(match is not None, 'complete referenced-image and tried header')
    tail = remainder[match.end():]
    rows = []
    while tail:
        item = re.match(r"'(/[^'\n]+)' \((no such file(?:, not in dyld cache)?)\)", tail)
        need(item is not None, 'unparsed dyld attempt or reason')
        path, reason = item.groups()
        need(str(Path(path)) == path and '..' not in Path(path).parts, 'canonical dyld attempted path')
        need(path in preobserved['absent_paths'], 'fresh dyld route lacks prior observation')
        rows.append({'path': path, 'reason': reason})
        tail = tail[item.end():]
        if tail:
            need(tail.startswith(', '), 'unparsed dyld suffix')
            tail = tail[2:]
            need(bool(tail), 'trailing dyld separator')
    need(bool(rows), 'empty dyld attempts')
    return rows


def profile_check(report, mode, snapshot):
    keys(report, ('schema', 'profile_before', 'profile_after', 'uname', 'startup', 'decimal', 'hashlib',
                  'modules', 'scientific_targets_imported_or_executed', 'boundary'), 'complete profile report')
    need(report['schema'] == 'ri121-installed-runtime-profile-observation-v1'
         and report['scientific_targets_imported_or_executed'] is False, 'nonscientific profile scope')
    same(report['boundary'], 'Installed-runtime observation under pinned supplier, cache-selection and host premises; no scientific qualification.', 'exact profile claim boundary')
    expected = {'version': '3.11.6 (main, Nov  2 2023, 04:39:43) [Clang 14.0.3 (clang-1403.0.22.14.1)]',
        'implementation': 'cpython', 'version_info': [3, 11, 6, 'final', 0], 'executable': M.VENV+'/bin/python',
        'prefix': M.VENV, 'exec_prefix': M.VENV,
        'base_prefix': '/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11',
        'base_exec_prefix': '/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11',
        'path': [M.ABSENCES[0], M.STDLIB, M.STDLIB+'/lib-dynload', M.ROOTS[1]],
        'byteorder': 'little', 'isolated': 1, 'dont_write_bytecode': 1, 'optimize': 0 if mode == 'normal' else 1}
    same(report['profile_before'], report['profile_after'], 'profile before/after changed')
    same(report['profile_after'], expected, 'exact accepted version/path/flags profile')
    same(report['uname'], snapshot['host_bootstrap']['uname'], 'profile host changed')
    same(report['startup'], {'enable_user_site': False, 'site_prefixes': [M.VENV], 'distutils_hook_loaded': True,
          'sitecustomize_loaded': True, 'usercustomize_loaded': False}, 'complete startup observation')
    d = report['decimal']
    keys(d, ('extension_loaded', 'fallback_loaded', 'decimal_class_is_fallback', 'extension_import_error', 'fraction_class_module'), 'complete decimal observation')
    need(d['extension_loaded'] is False and d['fallback_loaded'] is True and d['decimal_class_is_fallback'] is True,
         'accepted pure-python decimal fallback premise')
    same(d['fraction_class_module'], 'fractions', 'fraction supplier')
    keys(d['extension_import_error'], ('type', 'message'), 'complete decimal error')
    same(d['extension_import_error']['type'], 'ImportError', 'decimal import error type')
    attempts = dyld_attempts(d['extension_import_error']['message'], snapshot['preobserved_dyld_routes'])
    hashes = report['hashlib']
    keys(hashes, ('sha256_empty', 'openssl_sha256_empty', 'available_openssl_names'), 'complete hash observation')
    empty = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
    same([hashes['sha256_empty'], hashes['openssl_sha256_empty']], [empty, empty], 'observed empty hash usability')
    names = hashes['available_openssl_names']
    need(type(names) is list and all(type(x) is str for x in names) and names == sorted(set(names)), 'hash algorithm names retained')
    files = {row['path']: row for row in snapshot['runtime_inventory']['files']}
    descriptors = []
    need(type(report['modules']) is dict and bool(report['modules']), 'complete module descriptor object')
    forbidden = {'white_kernel', 'white_path', 'white_controls', 'white_fixtures', 'kernel_controls',
                 'white_validator', 'validator_controls', 'qualify_white_only'}
    need(not forbidden.intersection(report['modules']), 'scientific module in profile')
    for name, row in sorted(report['modules'].items()):
        keys(row, ('file', 'cached', 'origin', 'loader_type'), 'complete loaded module descriptor')
        need(type(row['loader_type']) is str, 'loader descriptor type')
        for field in ('file', 'cached', 'origin'):
            path = row[field]
            if path in (None, 'built-in', 'frozen'):
                descriptors.append({'module': name, 'field': field, 'value': path})
                continue
            need(type(path) is str and Path(path).is_absolute(), 'absolute module descriptor')
            if name == '__main__':
                need(field == 'file' and path == str(PACKET/'profile_observe.source-only.py'), 'only reviewed profile main file')
                descriptors.append({'module': name, 'field': field, 'identity': ref(path)})
                continue
            p = Path(path)
            if not p.exists():
                # Complete before/after tree enumeration, not this later lookup,
                # supplies the absence evidence for in-domain cache alternatives.
                need(field == 'cached' and not p.is_symlink() and path not in files
                     and any(str(p).startswith(root+'/') for root in M.ROOTS)
                     and p.resolve() == p, 'missing noncache/out-of-domain descriptor')
                descriptors.append({'module': name, 'field': field, 'path': path, 'absent_from_complete_inventory': True})
                continue
            resolved = str(p.resolve(strict=True))
            need(resolved in files, 'module descriptor outside complete runtime')
            same(ref(resolved), files[resolved], 'loaded descriptor current bytes')
            descriptors.append({'module': name, 'field': field, 'binding': M.binding(path)})
    need('__main__' in report['modules'], 'profile main descriptor absent')
    return {'status': 'SAVED_PROFILE_FIELDS_RECONCILED_NOT_RUNTIME_ACCEPTANCE', 'expected_runtime': expected,
            'all_descriptors': descriptors, 'ordered_actual_dyld_attempts': attempts,
            'full_dyld_error': d['extension_import_error'], 'preobserved_domain': snapshot['preobserved_dyld_routes'],
            'hash_algorithm_names': names, 'supplier_cache_and_stable_host_premises_retained': True,
            'full_import_trace_claim': False, 'scientific_qualification': False}


def guard_card(row, out):
    value = read(row)
    keys(value, ('schema', 'status', 'packet', 'harness', 'helpers', 'controls', 'output', 'source_review',
                 'genuine_outer_required'), 'complete separate 65-guard admission')
    need(value['schema'] == 'ri130-root-guard-admission-v1'
         and value['status'] == 'AUTHORIZE_RI130_NONSCIENTIFIC_CALLER_GUARDS_ONLY', 'separate caller guards authorized')
    same(value['packet'], str(PACKET), 'guard packet binding')
    same(value['harness'], pure(body(PACKET/'guard_controls.source-only.py')), 'exact guard harness')
    same(value['helpers'], {name: pure(body(PACKET/name)) for name in GUARD_HELPERS}, 'all seven captured guard helpers')
    same(value['controls'], list(GUARD_IDS), 'literal ordered 65 guards')
    same(value['output'], str(out/'GUARD_REPORT.json'), 'exact guard report output')
    need(value['genuine_outer_required'] is True, 'guard genuine custody premise')
    opaque(value['source_review'])
    return value


def guard_check(report, admission, out):
    keys(report, ('schema', 'status', 'packet', 'helpers_before', 'helpers_after', 'helpers_unchanged', 'controls',
        'control_order', 'counts', 'fixture_root', 'admission', 'target_or_scientific_helper_imported',
        'scientific_fixtures_or_controls_executed', 'runtime_observation_substitutions_explicit',
        'production_runtime_qualified', 'actual_data_admitted', 'full32_qualified', 'ret_paused'), 'complete caller guard report')
    need(report['schema'] == 'ri130-nonscientific-caller-guards-v1' and report['status'] == 'all_declared_guards_passed', 'actual65 report success')
    same(report['packet'], str(PACKET), 'reported guard packet')
    same(report['admission'], admission['guard_admission'], 'reported guard admission')
    expected_helpers = {name: pure(body(PACKET/name)) for name in GUARD_HELPERS}
    same(report['helpers_before'], expected_helpers, 'actual guard helper pre identities')
    same(report['helpers_after'], expected_helpers, 'actual guard helper post identities')
    same(report['control_order'], list(GUARD_IDS), 'actual guard ordered IDs')
    same(report['counts'], {'total': 65, 'passed': 65, 'failed': 0}, 'actual guard complete counts')
    need(type(report['controls']) is list, 'actual guard records type')
    same([row['id'] for row in report['controls']], list(GUARD_IDS), 'all actual guard records in order')
    for row in report['controls']:
        keys(row, ('id', 'passed', 'evidence', 'error'), 'complete guard evidence/error record')
        need(row['passed'] is True and row['error'] is None and row['evidence'] is not None, 'retained guard success evidence')
    for name in ('helpers_unchanged', 'runtime_observation_substitutions_explicit', 'ret_paused'):
        need(report[name] is True, 'guard true boundary '+name)
    for name in ('target_or_scientific_helper_imported', 'scientific_fixtures_or_controls_executed',
                 'production_runtime_qualified', 'actual_data_admitted', 'full32_qualified'):
        need(report[name] is False, 'guard false boundary '+name)
    root = M.literal_path(report['fixture_root'])
    need(root.parent == out and root.name.startswith('ri130-nonscientific-guards-'), 'owned complete guard fixture tree')
    return {'status': 'ALL65_SAVED_ENVELOPES_RECONCILED_NOT_ROOT_ACCEPTANCE', 'controls': report['controls'],
            'fixture_root': str(root), 'all_tree_entries': M.tree(root), 'scientific_controls_passed': 0,
            'runtime_substitutions_are_guard_doubles': True}


def run(path):
    admission, dependencies = authenticate(path)
    phase = admission['phase']; out = Path(admission['output']); env = environment(Path(admission['environment_root']))
    need(dict(os.environ) == env, 'root-controlled driver environment')
    need(not os.path.lexists(out), 'one fresh root-owned preparation output')
    # F01: a genuine initial reference and all safe tail state precede ownership.
    # Failure here is preownership refusal, with genuine outer evidence only.
    admission_ref = ref(path)
    same(read(admission_ref), admission, 'initial admission drift before ownership')
    started = time.monotonic()
    artifacts = {}; checks = {}; first = None; tails = []
    def remember(name, target):
        artifacts[name] = ref(target)
        return artifacts[name]
    def snapshot(label):
        need(time.monotonic()-started < 900, 'preparation parent soft deadline')
        command = [BOOTSTRAP, '-I', '-B', str(HERE/'prepare.py'), '--snapshot', str(path)]
        child = child_run(command, out, label, 180, env)
        remember(label, out/(label+'.stdout'))
        remember(label+'_completion', out/(label+'.COMPLETION.json'))
        return read(child['stdout'])
    baseline = None; before = None
    out.mkdir(mode=0o700)
    try:
        # Every fallible operation after successful mkdir is now protected.
        # A changed/unreadable admission cannot fabricate a new initial pin.
        same(ref(path), admission_ref, 'admission drift after ownership')
        save(out/'ATTEMPT.json', {'schema': 'ri133-preparation-attempt-v1', 'admission': admission_ref, 'sources': source_set(),
                                 'phase': phase, 'environment': env, 'scientific_execution': False})
        if phase == 'capture':
            need(all(admission[k] is None for k in ('baseline_acceptance', 'normal_acceptance', 'profiles_acceptance', 'guard_admission')), 'capture has no execution predecessor')
        else:
            base = acceptance(admission['baseline_acceptance'], 'baseline', admission)['capture']
            baseline = read(base['artifacts']['POST'])
        if phase in ('capture', 'profile_normal'):
            need(admission['normal_acceptance'] is None and admission['profiles_acceptance'] is None
                 and admission['guard_admission'] is None, 'no premature higher-stage admission')
        if phase == 'profile_optimized':
            need(admission['profiles_acceptance'] is None and admission['guard_admission'] is None, 'optimized is nonscientific profile only')
            normal = acceptance(admission['normal_acceptance'], 'normal', admission)['profile_normal']
        if phase == 'guards':
            need(admission['normal_acceptance'] is None, 'guards use complete both-mode review')
            profiles = acceptance(admission['profiles_acceptance'], 'profiles', admission)
            guard_card(admission['guard_admission'], out)
        before = snapshot('PRE')
        same(before['host_bootstrap']['bootstrap']['named'], admission['bootstrap'], 'snapshot bootstrap binding')
        same({'uname': before['host_bootstrap']['uname'], 'system_version': before['host_bootstrap']['system_version']}, admission['host'], 'snapshot root host binding')
        if baseline is not None:
            same(before, baseline, 'full current metadata differs from independently accepted baseline')
        if phase.startswith('profile_'):
            mode = phase[len('profile_'):]
            command = [M.VENV+'/bin/python', '-I', '-B']+(['-O'] if mode == 'optimized' else [])+[str(PACKET/'profile_observe.source-only.py')]
            result = child_run(command, out, 'PROFILE', 30, env)
            remember('PROFILE', out/'PROFILE.stdout'); remember('PROFILE_completion', out/'PROFILE.COMPLETION.json')
            checks['profile'] = profile_check(read(result['stdout']), mode, before)
            if mode == 'optimized':
                normal_report = read(normal['artifacts']['PROFILE'])
                normal_checks = profile_check(normal_report, 'normal', before)
                adjusted = dict(checks['profile']['expected_runtime']); adjusted['optimize'] = 0
                same(adjusted, normal_checks['expected_runtime'], 'normal/optimized complete runtime profile relation')
                same(checks['profile']['ordered_actual_dyld_attempts'], normal_checks['ordered_actual_dyld_attempts'], 'both complete ordered dyld attempts')
                same(checks['profile']['hash_algorithm_names'], normal_checks['hash_algorithm_names'], 'hash supplier names differ across modes')
        elif phase == 'guards':
            # Reconcile both genuine saved profiles now against the same full
            # current baseline before allowing the separately authorized guards.
            for mode in ('normal', 'optimized'):
                prior = profiles['profile_'+mode]
                checks['prior_'+mode] = profile_check(read(prior['artifacts']['PROFILE']), mode, before)
            command = [M.VENV+'/bin/python', '-I', '-B', str(PACKET/'guard_controls.source-only.py'),
                       '--packet', str(PACKET), '--admission', admission['guard_admission']['path'], '--output', str(out/'GUARD_REPORT.json')]
            guard_child = child_run(command, out, 'GUARDS', 180, env)
            need(guard_child['stdout']['bytes'] == 0, 'unexpected guard stdout')
            remember('GUARDS_completion', out/'GUARDS.COMPLETION.json'); remember('GUARD_REPORT', out/'GUARD_REPORT.json')
            checks['guards'] = guard_check(read(artifacts['GUARD_REPORT']), admission, out)
    except BaseException as exc:
        first = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        # Post-runtime, source/admission custody and namespace preservation are
        # independent tails. A failure in one never hides the first failure or
        # prevents attempting the remaining tails. Nothing is deleted or rerun.
        try:
            after = snapshot('POST')
            if before is not None: same(after, before, 'full before/after runtime/selection/native/routes/host/source changed')
            if baseline is not None: same(after, baseline, 'post metadata differs from accepted baseline')
            checks['post_metadata'] = 'PASS' if before is not None else 'CAPTURED_WITHOUT_SUCCESSFUL_PRE'
        except BaseException as exc:
            tails.append({'tail': 'post_metadata', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            same(source_set(), admission['sources'], 'preparation source postcheck')
            same(parse(body(path)), admission, 'root admission postcheck')
            M.source_observation(dependencies)
            checks['source_and_admission_postcheck'] = 'PASS'
        except BaseException as exc:
            tails.append({'tail': 'source_admission', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            save(out/'CHECKS.json', checks); remember('checks', out/'CHECKS.json')
        except BaseException as exc:
            tails.append({'tail': 'save_checks', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            save(out/'NAMESPACE.json', {'schema': 'ri133-retained-namespace-v1', 'root': str(out), 'entries': M.tree(out),
                                      'excluded_not_yet_written': ['NAMESPACE.json', 'COMPLETE.json']})
            remember('namespace', out/'NAMESPACE.json')
        except BaseException as exc:
            tails.append({'tail': 'retain_namespace', 'type': type(exc).__name__, 'message': str(exc)})
        elapsed = time.monotonic()-started
        if elapsed > 900:
            tails.append({'tail': 'soft_deadline', 'elapsed_seconds': elapsed})
        completion = {'schema': 'ri133-preparation-completion-v1', 'phase': phase,
            'status': 'CAPTURED_FOR_INDEPENDENT_REVIEW' if first is None and not tails else 'REFUSED_RETAIN_ALL_PARTIALS',
            'command': [BOOTSTRAP, '-I', '-B', str(HERE/'prepare.py'), '--admission', str(path)],
            'environment': env, 'admission': admission_ref, 'sources': admission['sources'], 'artifacts': artifacts,
            'first_error': first, 'independent_tail_errors': tails, 'elapsed_seconds': elapsed,
            'scientific_targets_executed': False, 'actual_data_admitted': False, 'full32_qualified': False,
            'ret_paused': True, 'runtime_acceptance_created': False, 'genuine_outer_created': False}
        save(out/'COMPLETE.json', completion)
    return 0 if completion['status'] == 'CAPTURED_FOR_INDEPENDENT_REVIEW' else 1


def main():
    parser = argparse.ArgumentParser()
    options = parser.add_mutually_exclusive_group(required=True)
    options.add_argument('--admission', type=Path)
    options.add_argument('--snapshot', type=Path)
    args = parser.parse_args()
    if args.snapshot is not None:
        admission, dependencies = authenticate(args.snapshot)
        need(dict(os.environ) == environment(Path(admission['environment_root'])), 'snapshot exact environment')
        sys.stdout.buffer.write(canonical(M.snapshot(dependencies)))
        return 0
    return run(args.admission)


if __name__ == '__main__':
    raise SystemExit(main())
