"""RI135 focused F01/F02 control SOURCE; UNEXECUTED.

Separate root admission required. All preparation/runtime/process interfaces in
F01 and snapshot-entry F02 controls are explicit doubles. No candidate program,
profile, science, full runtime collection or production admission is performed.
Every control tree and failure remains retained. This does not run RI130's65.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
FILES = ('prepare.py', 'runtime_metadata.py', 'fault_controls.source-only.py', 'DEPENDENCIES.source-only.json')
F01 = ('positive', 'pre_admission_read', 'occupied', 'mkdir', 'post_admission_read', 'initial_source_read',
       'attempt_open', 'attempt_partial', 'secondary_post', 'secondary_source', 'secondary_namespace',
       'secondary_checks', 'three_secondary', 'final_partial')
F02 = ('positive', 'named_path', 'resolved_path', 'link_literal', 'link_order', 'link_omitted',
       'target_bytes', 'target_sha', 'provenance_missing', 'snapshot_alias', 'snapshot_target')
IDS = tuple('F01_'+x for x in F01)+tuple('F02_'+x for x in F02)
CAP = 67108864
BODIES = {}


def need(ok, message):
    if not ok: raise ValueError(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')


def pin(path):
    p = Path(path)
    need(p.is_absolute() and p.resolve(strict=True) == p and p.is_file() and not p.is_symlink(), 'literal control source/metadata')
    data = p.read_bytes()
    need(len(data) <= CAP, 'bounded control metadata')
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def file_ref(path):
    return {'path': str(path), **pin(path)}


def parse(data):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate control metadata key')
            result[key] = value
        return result
    def bad(_): raise ValueError('nonfinite control metadata')
    value = json.loads(data, object_pairs_hook=pairs, parse_constant=bad)
    need(canonical(value) == data, 'canonical control metadata')
    return value


def save(path, value):
    with Path(path).open('xb') as f:
        f.write(canonical(value)); f.flush(); os.fsync(f.fileno())
    return file_ref(path)


def module(name, role):
    body = BODIES[name]
    need(pin(HERE/name) == {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}, 'captured repair source drift')
    spec = importlib.util.spec_from_file_location('ri135_control_'+role, HERE/name)
    value = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = value
    exec(compile(body, str(HERE/name), 'exec'), value.__dict__)
    return value


def f01_case(base, kind):
    """Call the real repaired run; all runtime/launch authority is substituted."""
    root = base/('F01_'+kind); root.mkdir(); out = root/'owned-output'
    P = module('prepare.py', 'f01_'+kind); R = module('runtime_metadata.py', 'tree_'+kind)
    source_pins = P.source_set()
    envroot = root/'ENVIRONMENT_DOUBLE'; envroot.mkdir(); (envroot/'tmp').mkdir()
    admission = {'schema': 'ri135-FABRICATED_CONTROL_NOT_ADMISSION', 'phase': 'capture', 'output': str(out),
        'environment_root': str(envroot), 'sources': source_pins, 'baseline_acceptance': None, 'normal_acceptance': None,
        'profiles_acceptance': None, 'guard_admission': None,
        'bootstrap': {'CONTROL_DOUBLE_NOT_RUNTIME': True}, 'host': {'uname': ['CONTROL'], 'system_version': {'CONTROL': True}}}
    metadata_path = root/'FABRICATED_CONTROL_METADATA.json'; original_ref = save(metadata_path, admission)
    original_source = P.source_set; original_ref_fn = P.ref; original_save = P.save; original_mkdir = Path.mkdir
    events = []; calls = {'source_set': 0, 'post': 0, 'pre': 0, 'source_tail': 0, 'tree': 0, 'checks': 0, 'complete': 0}
    attempted_completion = []
    primary = {'post_admission_read': 'CONTROL_POST_ADMISSION_READ', 'initial_source_read': 'CONTROL_INITIAL_SOURCE_READ',
               'attempt_open': 'CONTROL_ATTEMPT_OPEN'}.get(kind, 'CONTROL_ATTEMPT_PARTIAL')
    partial_kinds = ('attempt_partial', 'secondary_post', 'secondary_source', 'secondary_namespace', 'secondary_checks', 'three_secondary', 'final_partial')
    def fake_auth(_):
        events.append('AUTHENTICATION_SUBSTITUTED'); return copy.deepcopy(admission), {'CONTROL_DEPENDENCIES': True}
    def fake_ref(path):
        if Path(path) == metadata_path:
            events.append('admission_ref_owned' if out.exists() else 'admission_ref_preownership')
            if kind == 'pre_admission_read' and not out.exists(): raise ValueError('CONTROL_PRE_ADMISSION_READ')
            if kind == 'post_admission_read' and out.exists(): raise ValueError(primary)
        return original_ref_fn(path)
    def fake_sources():
        calls['source_set'] += 1; events.append('sources_'+str(calls['source_set']))
        if kind == 'initial_source_read' and calls['source_set'] == 1: raise ValueError(primary)
        return original_source()
    def fake_save(path, value):
        name = Path(path).name; events.append('save_'+name)
        if name == 'ATTEMPT.json':
            if kind == 'attempt_open': raise ValueError(primary)
            if kind in partial_kinds:
                with Path(path).open('xb') as stream: stream.write(b'{"CONTROL_PARTIAL_ATTEMPT":')
                raise ValueError(primary)
        if name == 'CHECKS.json':
            calls['checks'] += 1
            if kind == 'secondary_checks': raise ValueError('CONTROL_SECONDARY_CHECKS')
        if name == 'COMPLETE.json':
            calls['complete'] += 1; attempted_completion.append(copy.deepcopy(value))
            if kind == 'final_partial':
                with Path(path).open('xb') as stream: stream.write(b'{"CONTROL_PARTIAL_COMPLETE":')
                raise ValueError('CONTROL_FINAL_RECEIPT_WRITE')
        return original_save(path, value)
    def fake_child(command, directory, label, seconds, environment):
        need(label in ('PRE', 'POST') and '--snapshot' in command, 'no candidate/guard/profile entry in F01 controls')
        calls[label.lower()] += 1; events.append('child_'+label+'_SUBSTITUTED')
        if label == 'POST' and kind in ('secondary_post', 'three_secondary'):
            raise ValueError('CONTROL_SECONDARY_POST')
        snapshot = {'CONTROL_METADATA_DOUBLE_ONLY': True,
                    'host_bootstrap': {'bootstrap': {'named': admission['bootstrap']}, **admission['host']}}
        stdout = original_save(directory/(label+'.stdout'), snapshot)
        original_save(directory/(label+'.COMPLETION.json'), {'CONTROL_CHILD_COMPLETION_DOUBLE_ONLY': True})
        return {'stdout': stdout}
    def source_tail(_):
        calls['source_tail'] += 1; events.append('source_tail_SUBSTITUTED')
        if kind in ('secondary_source', 'three_secondary'): raise ValueError('CONTROL_SECONDARY_SOURCE')
        return {'CONTROL_ONLY': True}
    def tree(path):
        calls['tree'] += 1; events.append('namespace_tail')
        if kind in ('secondary_namespace', 'three_secondary'): raise ValueError('CONTROL_SECONDARY_NAMESPACE')
        return R.tree(path)
    def mkdir(path, *args, **kwargs):
        if Path(path) == out and kind == 'mkdir': raise ValueError('CONTROL_MKDIR_FAILURE')
        return original_mkdir(path, *args, **kwargs)
    def forbidden(*args, **kwargs):
        raise ValueError('CONTROL_UNEXPECTED_REAL_PROCESS')
    if kind == 'occupied':
        out.mkdir(); (out/'UNRELATED_OCCUPIED').write_bytes(b'preserve me\n')
    returned = None; escaped = None
    with patch.object(P, 'authenticate', fake_auth), patch.object(P, 'ref', fake_ref), patch.object(P, 'source_set', fake_sources), \
         patch.object(P, 'save', fake_save), patch.object(P, 'child_run', fake_child), \
         patch.object(P, 'M', SimpleNamespace(tree=tree, source_observation=source_tail)), \
         patch.object(Path, 'mkdir', mkdir), patch.dict(os.environ, P.environment(envroot), clear=True), \
         patch.object(P.subprocess, 'Popen', forbidden), patch.object(P.subprocess, 'run', forbidden):
        try: returned = P.run(metadata_path)
        except BaseException as exc: escaped = {'type': type(exc).__name__, 'message': str(exc)}
    if kind in ('pre_admission_read', 'occupied', 'mkdir'):
        expected = {'pre_admission_read': 'CONTROL_PRE_ADMISSION_READ', 'occupied': 'one fresh root-owned preparation output', 'mkdir': 'CONTROL_MKDIR_FAILURE'}[kind]
        need(escaped == {'type': 'ValueError', 'message': expected}, 'exact preownership first refusal')
        need(calls == {'source_set': 0, 'post': 0, 'pre': 0, 'source_tail': 0, 'tree': 0, 'checks': 0, 'complete': 0}, 'preownership ran owned tails')
        if kind == 'occupied': need((out/'UNRELATED_OCCUPIED').read_bytes() == b'preserve me\n' and len(list(out.iterdir())) == 1, 'occupied output changed')
        else: need(not out.exists(), 'preownership refusal created output')
        first = escaped
    else:
        need(calls['post'] == calls['source_tail'] == calls['tree'] == calls['checks'] == calls['complete'] == 1,
             'every independent owned tail attempted exactly once')
        need(len(attempted_completion) == 1, 'one final completion attempt')
        record = attempted_completion[0]
        need(record['admission'] == original_ref, 'retained genuine initial fixture metadata reference')
        first = record['first_error']
        if kind == 'positive':
            need(returned == 0 and escaped is None and first is None and calls['pre'] == 1
                 and record['status'] == 'CAPTURED_FOR_INDEPENDENT_REVIEW', 'positive isolated run path')
        else:
            need(first == {'type': 'ValueError', 'message': primary} and calls['pre'] == 0,
                 'exact named early refusal reached before later work')
            need(record['status'] == 'REFUSED_RETAIN_ALL_PARTIALS', 'failed owned attempt promoted')
            if kind == 'final_partial':
                need(returned is None and escaped == {'type': 'ValueError', 'message': 'CONTROL_FINAL_RECEIPT_WRITE'}, 'actual final write failure must escape for genuine outer')
                need((out/'COMPLETE.json').read_bytes() == b'{"CONTROL_PARTIAL_COMPLETE":', 'partial final receipt changed')
            else: need(returned == 1 and escaped is None, 'owned refusal return')
        expected_tails = {'secondary_post': [('post_metadata', 'CONTROL_SECONDARY_POST')],
            'secondary_source': [('source_admission', 'CONTROL_SECONDARY_SOURCE')],
            'secondary_namespace': [('retain_namespace', 'CONTROL_SECONDARY_NAMESPACE')],
            'secondary_checks': [('save_checks', 'CONTROL_SECONDARY_CHECKS')],
            'three_secondary': [('post_metadata', 'CONTROL_SECONDARY_POST'), ('source_admission', 'CONTROL_SECONDARY_SOURCE'), ('retain_namespace', 'CONTROL_SECONDARY_NAMESPACE')]}.get(kind, [])
        need([(x['tail'], x['message']) for x in record['independent_tail_errors']] == expected_tails, 'exact independent secondary failures')
        if kind in partial_kinds:
            need((out/'ATTEMPT.json').read_bytes() == b'{"CONTROL_PARTIAL_ATTEMPT":', 'partial initial ATTEMPT overwritten')
            need(events.count('save_ATTEMPT.json') == 1, 'initial attempt retried')
        if kind in ('post_admission_read', 'initial_source_read', 'attempt_open'):
            need(not (out/'ATTEMPT.json').exists(), 'failed prewrite unexpectedly manufactured ATTEMPT')
    return {'substitutions': ['authentication', 'runtime snapshot/processes', 'source observation'], 'events': events,
            'calls': calls, 'first_error': first, 'escaped': escaped, 'returncode': returned,
            'attempted_completion': attempted_completion, 'retained_tree': R.tree(root),
            'actual_runtime_or_production_admission': False}


def f02_case(base, kind):
    R = module('runtime_metadata.py', 'f02_'+kind)
    dependencies = parse(BODIES['DEPENDENCIES.source-only.json'])
    expected = R.load_ref(dependencies['historical_interpreter'])
    current = copy.deepcopy(expected)
    if kind == 'named_path': current['named_path'] += '.changed'
    if kind == 'resolved_path': current['resolved_path'] += '.changed'
    if kind in ('link_literal', 'snapshot_alias'): current['symlink_chain'][0]['target'] = './python3.11'
    if kind == 'link_order': current['symlink_chain'] = list(reversed(current['symlink_chain']))
    if kind == 'link_omitted': current['symlink_chain'] = current['symlink_chain'][1:]
    if kind == 'target_bytes': current['target']['bytes'] += 1
    if kind in ('target_sha', 'snapshot_target'): current['target']['sha256'] = '0'*64
    reads = []; calls = {'host': 0, 'sources': 0, 'absences': 0, 'namespaces': 0, 'routes': 0, 'loaders': 0, 'interpreter': 0, 'walk': 0}
    original_load = R.load_ref
    def load(row):
        reads.append(row['path'])
        value = original_load(row)  # Actual parser/pin authentication of saved historical metadata only.
        if kind == 'provenance_missing' and row == dependencies['historical_interpreter_provenance']:
            value = copy.deepcopy(value)
            value['files'] = [x for x in value['files'] if x['path'] != dependencies['historical_interpreter']['path']]
        return value
    inventory = original_load(dependencies['historical_runtime'])
    namespaces = original_load(dependencies['historical_optional_namespaces'])['directories']
    def counted(name, value):
        calls[name] += 1; return copy.deepcopy(value)
    def binding(path):
        if path == R.VENV+'/bin/python': return counted('interpreter', current)
        calls['loaders'] += 1
        return copy.deepcopy(next(x for x in inventory['loader_bindings'] if x['named_path'] == path))
    def walk(_):
        calls['walk'] += 1; raise ValueError('CONTROL_UNEXPECTED_LATER_WALK')
    escaped = None; returned = None
    with patch.object(R, 'load_ref', load):
        try:
            if kind.startswith('snapshot_'):
                with patch.object(R, 'host_bootstrap', lambda: counted('host', {'CONTROL_ONLY': True})), \
                     patch.object(R, 'source_observation', lambda _: counted('sources', {'CONTROL_ONLY': True})), \
                     patch.object(R, 'absent_observations', lambda: counted('absences', [])), \
                     patch.object(R, 'directory_namespaces', lambda: counted('namespaces', namespaces)), \
                     patch.object(R, 'dyld_routes', lambda: counted('routes', {'CONTROL_ONLY': True})), \
                     patch.object(R, 'binding', binding), patch.object(R, 'walk_members', walk):
                    returned = R.snapshot(dependencies)
            else:
                returned = R.require_historical_interpreter(current, dependencies)
        except BaseException as exc: escaped = {'type': type(exc).__name__, 'message': str(exc)}
    if kind == 'positive':
        need(escaped is None and returned == expected, 'authentic full binding positive')
    else:
        expected_message = 'historical interpreter handoff identity' if kind == 'provenance_missing' else 'candidate interpreter differs from authentic historical binding'
        need(escaped == {'type': 'RuntimeError', 'message': expected_message}, 'exact new historical-binding refusal, not an earlier gate')
    need(reads.count(dependencies['historical_interpreter_provenance']['path']) == 1, 'authentic historical provenance reached')
    need(reads.count(dependencies['historical_interpreter']['path']) == (0 if kind == 'provenance_missing' else 1), 'binding read reached at intended gate')
    if kind.startswith('snapshot_'):
        need(calls == {'host': 1, 'sources': 1, 'absences': 1, 'namespaces': 1, 'routes': 1, 'loaders': 8, 'interpreter': 1, 'walk': 0}, 'real snapshot reached F02 before any later runtime walk')
    return {'current_binding_control_operand': current, 'genuine_historical_binding': dependencies['historical_interpreter'],
            'historical_provenance': dependencies['historical_interpreter_provenance'], 'reads': reads, 'calls': calls,
            'refusal': escaped, 'snapshot_observers_substituted': kind.startswith('snapshot_'),
            'provenance_after_authentication_mutated_in_memory': kind == 'provenance_missing', 'actual_current_interpreter_observed': False}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--admission', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True); args = parser.parse_args()
    need(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'normal isolated control bootstrap')
    card = parse(args.admission.read_bytes())
    need(set(card) == {'schema', 'status', 'sources', 'controls', 'output', 'independent_source_review', 'genuine_outer_required'}, 'closed separate control authorization')
    need(card['schema'] == 'ri135-root-fault-control-admission-v1' and card['status'] == 'AUTHORIZE_F01_F02_NONSCIENTIFIC_CONTROLS_ONLY'
         and card['controls'] == list(IDS) and card['output'] == str(args.output) and card['genuine_outer_required'] is True, 'separate exact fault-control authority')
    before = {name: pin(HERE/name) for name in FILES}; need(card['sources'] == before, 'exact focused-control source identities')
    need(file_ref(card['independent_source_review']['path']) == card['independent_source_review'], 'source-review binding')
    need(args.output.is_absolute() and args.output.resolve() == args.output and not os.path.lexists(args.output)
         and HERE not in args.output.parents and args.output != HERE, 'fresh external control output')
    global BODIES
    BODIES = {name: (HERE/name).read_bytes() for name in FILES}
    need({name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for name,data in BODIES.items()} == before, 'all source bodies captured before module load')
    args.output.mkdir(mode=0o700); rows = []
    def attempt(identifier, action):
        try: rows.append({'id': identifier, 'passed': True, 'evidence': action(), 'error': None})
        except BaseException as exc: rows.append({'id': identifier, 'passed': False, 'evidence': None, 'error': {'type': type(exc).__name__, 'message': str(exc)}})
    for kind in F01: attempt('F01_'+kind, lambda kind=kind: f01_case(args.output, kind))
    for kind in F02: attempt('F02_'+kind, lambda kind=kind: f02_case(args.output, kind))
    after = {name: pin(HERE/name) for name in FILES}
    report = {'schema': 'ri135-focused-fault-control-report-v1', 'controls': rows, 'order': list(IDS),
        'counts': {'total': len(rows), 'passed': sum(x['passed'] for x in rows), 'failed': sum(not x['passed'] for x in rows)},
        'sources_before': before, 'sources_after': after, 'sources_unchanged': before == after,
        'status': 'ALL25_FOCUSED_CONTROLS_PASSED' if before == after and all(x['passed'] for x in rows) else 'CONTROL_FAILURE',
        'admission': file_ref(args.admission), 'fixture_root': str(args.output), 'all_substitutions_explicit': True,
        'runtime_profiles_or_65_caller_guards_executed': False, 'scientific_execution': False,
        'production_admission_created': False, 'actual_current_runtime_qualified': False, 'ret_paused': True}
    save(args.output/'REPORT.json', report)
    R = module('runtime_metadata.py', 'final_control_namespace')
    save(args.output/'NAMESPACE.json', {'schema': 'ri135-focused-controls-retained-namespace-v1',
        'root': str(args.output), 'entries': R.tree(args.output), 'excluded_not_yet_written': ['NAMESPACE.json'],
        'partial_failure_artifacts_retained': True})
    return 0 if report['status'] == 'ALL25_FOCUSED_CONTROLS_PASSED' else 1


if __name__ == '__main__': raise SystemExit(main())
