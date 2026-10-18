#!/usr/bin/env python3
"""RI140 repaired two-phase policy launcher; source only until genuine root admission.

Root authenticates this interpreter before startup and owns actual tool history.
This program implements finite custody/collection, never external provenance.
"""

from hashlib import sha256
from pathlib import Path
import json
import math
import os
import shlex
import signal
import stat
import sys
import time
import types


BASE = Path('/Volumes/AI_DATA/development/det-review-evidence')
Q = BASE/'ri140-native-failure-repair-source-l_a4mna0'
SELF = Q/'launch_policy_case.py'
MANIFEST = Q/'SOURCE_IDENTITIES.json'
MANIFEST_PIN = {'path': str(MANIFEST), 'bytes': 26029,
                'sha256': '25a694353f782aa3d6c50f925981b5403a5da28308676930256b420c110f192c'}
PYTHON = '/opt/homebrew/bin/python3'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912, 'output_bytes': 8388608,
          'auxiliary_metadata_bytes': 67108864, 'sample_interval_ms': 50, 'ps_timeout_ms': 250}
BUDGETS = {'metadata_seconds': 60, 'before_seconds': 300, 'after_seconds': 300,
           'final_seconds': 60, 'overall_seconds': 840}
CAP = 67108864
NS = 1000000000
TOOL_SOURCE = 'Coordinator task tool history; actual invocation, not replay or reconstructed success'
ROOT_NAMES = {'ROOT_PLAN.json', 'ROOT_PREPARE_DISPATCH.json'}
PREPARE_NAMES = {'PREPARE_STARTED.json', 'PREPARE_EXPECTATIONS.json',
                 'PREPARE_BEFORE.jsonl', 'PREPARE_BEFORE_SUMMARY.json',
                 'PREPARE_AFTER.jsonl', 'PREPARE_AFTER_SUMMARY.json',
                 'PREFLIGHT.json', 'AUTHORIZATION.json', 'PREPARE_RESULT.json'}
RUN_INPUT_NAMES = {'ROOT_DISPATCH.json', 'PREPARE_TOOL_RESULT.json'}
RUN_NAMES = {'RUN_STARTED.json', 'RUN_EXPECTATIONS.json', 'RUN_BEFORE.jsonl',
             'RUN_BEFORE_SUMMARY.json', 'RUN_AFTER.jsonl', 'RUN_AFTER_SUMMARY.json',
             'RUN_RESULT.json'}
PROCESS_NAMES = {'stdout.log', 'stderr.log', 'process-events.jsonl',
                 'process-errors.jsonl', 'PROCESS_REPORT.json', 'PROCESS_CLOSE.json'}
SIGNALS = []
OVERALL_DEADLINE = None
ACQUISITION_SIGNALS = None
ACQUISITION_PRIMARY = None


class Refused(RuntimeError):
    pass


class HardDeadline(BaseException):
    ri138_hard_deadline = True


def require(condition, message):
    if not condition:
        raise Refused(message)


def propagate_hard(error):
    if getattr(error, 'ri138_hard_deadline', False) is True:
        raise error


def hard_unwinding():
    error = sys.exc_info()[1]
    return error is not None and not isinstance(error, Exception)


def close_on_abort(sink):
    # No persistence or completed-close claim while unwinding a hard abort.
    if sink is not None and sink.fd is not None and not sink.closed:
        try:
            os.close(sink.fd)
        except Exception:
            pass


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def raw_json(value):
    return (canonical(value)+'\n').encode('ascii')


def exact(value, keys, context):
    require(type(value) is dict and set(value) == set(keys), context+' fields differ')


def same(left, right, context):
    require(canonical(left) == canonical(right), context)


def strict_json(raw, tool_record=False):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate administrative JSON key')
            result[key] = value
        return result
    def number(value):
        require(tool_record, 'administrative decimals forbidden outside genuine tool transcription')
        result = float(value)
        require(math.isfinite(result), 'nonfinite tool transcription number')
        return result
    def bad(value):
        raise Refused('nonfinite JSON number forbidden')
    value = json.loads(raw, object_pairs_hook=pairs, parse_float=number, parse_constant=bad)
    require(type(value) is dict, 'administrative root must be an object')
    return value


def check_time(deadline):
    now = time.monotonic_ns()
    if OVERALL_DEADLINE is not None and now >= OVERALL_DEADLINE:
        raise HardDeadline('overall 840-second launcher budget exhausted')
    require(type(deadline) is int and now <= deadline, 'bounded phase deadline exhausted')


def signal_received(signum, frame):
    SIGNALS.append({'signal': signum, 'monotonic_ns': time.monotonic_ns()})
    if signum == signal.SIGALRM:
        raise HardDeadline('overall launcher watchdog fired')
    acquisition = ACQUISITION_SIGNALS
    if acquisition is not None:
        if acquisition.pending is None:
            acquisition.pending = Refused('launcher interrupted by signal '+str(signum))
        if acquisition.deferring or sys.exc_info()[1] is not None:
            return
        acquisition.interrupt()
    # Protect only this acquisition's exact primary exception across context
    # clearing, not unrelated exception handlers elsewhere in the launcher.
    active_error = sys.exc_info()[1]
    if active_error is not None and active_error is ACQUISITION_PRIMARY:
        return
    raise Refused('launcher interrupted by signal '+str(signum))


def literal_path(value):
    require(type(value) is str and '\x00' not in value and os.path.isabs(value)
            and os.path.normpath(value) == value, 'noncanonical literal absolute path')
    return Path(value)


def nonsymlink(path):
    part = Path(path.anchor)
    for name in path.parts[1:]:
        part /= name
        require(not stat.S_ISLNK(part.lstat().st_mode), 'symlink in source/operational path')


def identity_shape(value, positive=True):
    exact(value, ('path', 'bytes', 'sha256'), 'ordinary identity')
    literal_path(value['path'])
    require(type(value['bytes']) is int and (value['bytes'] > 0 if positive else value['bytes'] >= 0)
            and value['bytes'] <= CAP and type(value['sha256']) is str
            and len(value['sha256']) == 64 and all(c in '0123456789abcdef' for c in value['sha256'])
            and value['sha256'] != '0'*64, 'invalid bounded ordinary identity')


def read_file(path, deadline, expected=None, cap=CAP):
    check_time(deadline)
    path = literal_path(str(path))
    nonsymlink(path)
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= cap, 'file type/size refused')
        chunks, count = [], 0
        while True:
            check_time(deadline)
            block = os.read(fd, min(1048576, cap+1-count))
            if not block:
                break
            chunks.append(block)
            count += len(block)
            require(count <= cap, 'file grew beyond bounded read')
        after = os.fstat(fd)
    finally:
        os.close(fd)
    signature = lambda x: (x.st_dev, x.st_ino, x.st_mode, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
    require(signature(before) == signature(after) == signature(path.lstat()) and count == after.st_size,
            'file identity changed while reading')
    raw = b''.join(chunks)
    identity = {'path': str(path), 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}
    if expected is not None:
        identity_shape(expected, positive=False)
        same(identity, expected, 'whole-file identity differs before decoding')
    check_time(deadline)
    return raw, identity


def read_json(path, deadline, expected=None, tool_record=False):
    raw, identity = read_file(path, deadline, expected)
    return strict_json(raw, tool_record), identity


def error_value(stage, error):
    return {'stage': stage, 'type': type(error).__name__, 'message': str(error)[:4096]}


def directory_sync(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class AcquisitionSignals:
    """Protect fd/owner registration only, never writes, fsyncs or the watchdog."""
    def __init__(self):
        self.pending, self.deferring = None, True

    def __enter__(self):
        global ACQUISITION_SIGNALS
        require(ACQUISITION_SIGNALS is None, 'nested evidence sink acquisition')
        ACQUISITION_SIGNALS = self
        return self

    def __exit__(self, error_type, error, traceback):
        global ACQUISITION_SIGNALS, ACQUISITION_PRIMARY
        ACQUISITION_PRIMARY = error
        try:
            # A new signal here raises the same first pending signal, but never
            # replaces the original exception supplied by the protected body.
            self.deferring = False
            if error_type is None and self.pending is not None:
                self.interrupt()
        finally:
            ACQUISITION_SIGNALS = None
        return False

    def interrupt(self):
        global ACQUISITION_PRIMARY
        ACQUISITION_PRIMARY = self.pending
        raise self.pending


class DurableSink:
    """One exclusive bounded file; synchronous records never claim unwritten bytes."""
    def __init__(self, path, deadline):
        self.path, self.deadline = Path(path), deadline
        self.fd = None
        self.length, self.digest, self.closed = 0, sha256(), False
        check_time(deadline)
        nonsymlink(self.path.parent)

    def acquire(self, owner=None):
        # The caller already holds this fully initialized sink. Only this short
        # transition defers ordinary signals; the hard watchdog is never deferred.
        check_time(self.deadline)
        require(self.fd is None and not self.closed, 'evidence sink already acquired or closed')
        with AcquisitionSignals():
            try:
                self.fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            finally:
                if self.fd is not None and owner is not None:
                    owner.owned = True

    def append_bytes(self, raw):
        check_time(self.deadline)
        require(type(raw) is bytes and self.length+len(raw) <= CAP, '64-MiB evidence sink bound exceeded')
        require(self.fd is not None and not self.closed, 'write to closed evidence sink')
        offset, view = self.length, memoryview(raw)
        while view:
            check_time(self.deadline)
            count = os.write(self.fd, view)
            require(count > 0, 'nonpositive evidence write')
            self.digest.update(view[:count])
            self.length += count
            view = view[count:]
        os.fsync(self.fd)
        check_time(self.deadline)
        return {'path': str(self.path), 'offset': offset, 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}

    def __call__(self, value):
        return self.append_bytes(raw_json(value))

    def close(self):
        expected = {'path': str(self.path), 'bytes': self.length, 'sha256': self.digest.hexdigest()}
        receipt = {'path': str(self.path), 'identity': expected, 'fsync_ok': False,
                   'closed': False, 'readback_ok': False, 'directory_fsync_ok': False, 'errors': []}
        for stage, operation in (('fsync', lambda: os.fsync(self.fd)),
                                 ('close', lambda: os.close(self.fd)),
                                 ('readback', lambda: read_file(self.path, self.deadline, expected)),
                                 ('directory_fsync', lambda: directory_sync(self.path.parent))):
            try:
                operation()
                receipt[{'fsync': 'fsync_ok', 'close': 'closed', 'readback': 'readback_ok',
                         'directory_fsync': 'directory_fsync_ok'}[stage]] = True
                if stage == 'close':
                    self.closed = True
                check_time(self.deadline)
            except Exception as error:
                receipt['errors'].append(error_value('sink-'+stage, error))
        return receipt


def write_new(path, raw, deadline, owner=None):
    sink, receipt = None, {'path': str(path), 'identity': None, 'errors': [], 'close': None}
    try:
        sink = DurableSink(path, deadline)
        sink.acquire(owner)
        sink.append_bytes(raw)
    except Exception as error:
        receipt['errors'].append(error_value('exclusive-write', error))
    finally:
        if hard_unwinding():
            close_on_abort(sink)
        elif sink is not None and sink.fd is not None:
            receipt['close'] = sink.close()
            receipt['identity'] = receipt['close']['identity']
            receipt['errors'].extend(receipt['close']['errors'])
    return receipt


def invocation(phase, plan_sha, directory):
    argv = [PYTHON, '-I', '-S', '-B', str(SELF), phase, plan_sha]
    command = ['exec', '/usr/bin/env', '-i'] + [key+'='+ENV[key] for key in ENV] + argv
    return argv, {'cmd': ' '.join(shlex.quote(word) for word in command), 'workdir': str(directory),
                  'login': False, 'yield_time_ms': 1000, 'max_output_tokens': 2000}


def namespace(directory, expected_names, deadline):
    check_time(deadline)
    nonsymlink(directory)
    before = directory.stat()
    actual = []
    for entry in directory.iterdir():
        check_time(deadline)
        require(len(actual) < 64, 'operational namespace exceeded fixed bound')
        require(stat.S_ISREG(entry.lstat().st_mode), 'nonregular operational namespace member')
        actual.append(entry.name)
    after = directory.stat()
    require((before.st_dev, before.st_ino, before.st_mtime_ns, before.st_ctime_ns)
            == (after.st_dev, after.st_ino, after.st_mtime_ns, after.st_ctime_ns),
            'operational namespace changed during observation')
    require(set(actual) == set(expected_names), 'operational namespace has absent/unexpected artifacts')
    return {'path': str(directory), 'names': sorted(actual), 'complete': True}


def load_module(identity, name, deadline):
    raw, _ = read_file(Path(identity['path']), deadline, identity)
    module = types.ModuleType(name)
    module.__file__, module.__package__ = identity['path'], ''
    exec(compile(raw, identity['path'], 'exec', dont_inherit=True, optimize=0), module.__dict__)
    return module


def authenticate(phase, plan_sha, deadline):
    require(phase in ('prepare', 'run') and type(plan_sha) is str and len(plan_sha) == 64
            and all(c in '0123456789abcdef' for c in plan_sha) and plan_sha != '0'*64,
            'require prepare/run and literal root-plan SHA256')
    directory = Path.cwd()
    require(directory.parent == BASE and directory.name.startswith('ri136-policy-run-')
            and len(directory.name) > len('ri136-policy-run-'), 'wrong operational reservation')
    nonsymlink(directory)
    require(sys.platform == 'darwin' and Path(__file__).absolute() == SELF and sys.argv[0] == str(SELF)
            and os.path.realpath(sys.executable) == os.path.realpath(PYTHON)
            and dict(os.environ) == ENV and sys.flags.isolated == 1 and sys.flags.no_site == 1
            and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0,
            'fixed launcher/interpreter/host/environment/flags differ')
    raw, plan_id = read_file(directory/'ROOT_PLAN.json', deadline)
    require(plan_id['sha256'] == plan_sha, 'root plan complete-byte digest differs')
    plan = strict_json(raw)
    exact(plan, ('schema', 'status', 'caller', 'case', 'operational_directory', 'source_manifest',
                 'source_handoff', 'launcher', 'independent_review', 'root_adjudication', 'external_bootstrap',
                 'outer_environment', 'limits', 'phase_budgets', 'acceptance_assertions',
                 'prepare_authorized', 'one_run_authorized',
                 'scientific_execution_authorized', 'production_entry_authorized',
                 'retry_or_limit_relaxation_authorized'), 'root plan')
    require(plan['schema'] == 'ri138-root-one-case-plan-v1'
            and plan['status'] == 'ADMIT_PREPARE_AND_ONE_CONDITIONAL_POLICY_RUN'
            and plan['caller'] in ('native', 'audit') and plan['operational_directory'] == str(directory)
            and plan['prepare_authorized'] is True and plan['one_run_authorized'] is True
            and all(plan[k] is False for k in ('scientific_execution_authorized',
                'production_entry_authorized', 'retry_or_limit_relaxation_authorized')), 'root plan scope differs')
    same(plan['outer_environment'], ENV, 'plan environment differs')
    same(plan['limits'], LIMITS, 'plan child limits differ')
    same(plan['phase_budgets'], BUDGETS, 'plan phase budgets differ')
    same(plan['source_manifest'], MANIFEST_PIN, 'fixed launcher subject manifest differs')
    manifest, manifest_id = read_json(MANIFEST, deadline, MANIFEST_PIN)
    require(manifest['schema'] == 'ri138-external-launch-subject-identities-v1', 'subject manifest schema differs')
    subject = manifest['subjects'][plan['caller']]
    dispatcher_handoff, _ = read_json(Path(manifest['dispatcher_source_handoff']['path']), deadline,
                                     manifest['dispatcher_source_handoff'])
    dispatcher_subjects, _ = read_json(Path(manifest['dispatcher_subject_manifest']['path']), deadline,
                                      manifest['dispatcher_subject_manifest'])
    matches = [case for case in subject['ordered_cases'] if canonical(case) == canonical(plan['case'])]
    require(len(matches) == 1, 'root case is not one exact accepted triple')
    require(plan['source_handoff']['path'] == str(Q/'HANDOFF.json'), 'wrong current source handoff path')
    handoff, handoff_id = read_json(Q/'HANDOFF.json', deadline, plan['source_handoff'])
    exact(handoff, ('schema', 'status', 'source_directory', 'files', 'predecessor', 'author_checks',
                    'scope', 'remaining_obligations'), 'current source handoff')
    require(handoff.get('schema') == 'ri140-native-failure-repair-source-handoff-v1'
            and handoff.get('status') == 'SOURCE_ONLY_REQUIRES_INDEPENDENT_REVIEW'
            and handoff['source_directory'] == str(Q)
            and type(handoff.get('files')) is list and 0 < len(handoff['files']) <= 64,
            'current source handoff scope differs')
    same(handoff['scope'], {'execution_authorized': False, 'current_runtime_observed': False,
                           'controls_executed': 0, 'scientific_execution': False,
                           'complete_caller_qualification': False, 'repository_modified': False},
         'source-only handoff scope differs')
    same(handoff['predecessor'], manifest['repair_ancestry']['predecessor_source_handoff'],
         'handoff predecessor differs')
    require(type(handoff['remaining_obligations']) is list
            and all(type(item) is str for item in handoff['remaining_obligations']), 'handoff obligations differ')
    payloads = {}
    for identity in handoff['files']:
        identity_shape(identity)
        path = literal_path(identity['path'])
        require(path.parent == Q and path.name != 'HANDOFF.json' and str(path) not in payloads,
                'current payload path duplicated or outside packet')
        payloads[str(path)] = identity
    require(list(payloads) == sorted(payloads), 'handoff payloads not sorted')
    for name in ('launch_policy_case.py', 'custody.py', 'owned_process.py', 'SOURCE_IDENTITIES.json',
                 'SOURCE_DEPENDENCIES.json'):
        require(str(Q/name) in payloads, 'required current source payload missing')
    same(payloads[str(SELF)], plan['launcher'], 'launcher pin differs from complete handoff')
    same(payloads[str(MANIFEST)], MANIFEST_PIN, 'subject manifest pin differs from handoff')
    same(payloads[str(Q/'SOURCE_DEPENDENCIES.json')], manifest['dependency_manifest'], 'dependency pin differs')
    require(str(Q/'AUTHOR_STATIC_CHECKS.json') in payloads, 'author metadata identity missing')
    same(handoff['author_checks'], payloads[str(Q/'AUTHOR_STATIC_CHECKS.json')], 'author metadata binding differs')
    namespace(Q, {Path(path).name for path in payloads}|{'HANDOFF.json'}, deadline)
    inputs = [plan_id, handoff_id, manifest_id]
    for identity in payloads.values():
        read_file(Path(identity['path']), deadline, identity)
        inputs.append(identity)
    for name in ('independent_review', 'root_adjudication', 'external_bootstrap'):
        identity_shape(plan[name])
        require(Path(plan[name]['path']).parent != directory, 'root authority must be outside writable reservation')
        read_file(Path(plan[name]['path']), deadline, plan[name])
        inputs.append(plan[name])
    # These exact bindings/assertions are root input, not fabricated review
    # authority or a guessed schema for the future independent review.
    same(plan['acceptance_assertions'], {'source_handoff': handoff_id, 'source_accepted': True,
        'blocking_findings': [], 'complete_caller_qualification': False, 'scientific_result_claimed': False},
        'root acceptance assertions differ')
    prepare_dispatch, prepare_dispatch_id = read_json(directory/'ROOT_PREPARE_DISPATCH.json', deadline)
    exact(prepare_dispatch, ('schema', 'root_plan', 'prepare_argv', 'outer_cwd', 'outer_environment',
                            'limits', 'phase_budgets', 'literal_tool_invocation'), 'root prepare dispatch')
    expected_argv, expected_tool = invocation('prepare', plan_sha, directory)
    same(prepare_dispatch, {'schema': 'ri138-root-prepare-dispatch-v1', 'root_plan': plan_id,
                           'prepare_argv': expected_argv, 'outer_cwd': str(directory), 'outer_environment': ENV,
                           'limits': LIMITS, 'phase_budgets': BUDGETS, 'literal_tool_invocation': expected_tool},
         'root prepare literal invocation binding differs')
    inputs.append(prepare_dispatch_id)
    dependencies, dependency_id = read_json(Q/'SOURCE_DEPENDENCIES.json', deadline, manifest['dependency_manifest'])
    require(dependencies.get('schema') == 'ri129-source-dependencies-v1'
            and dependencies.get('status') == 'SOURCE_ONLY_CLOSED_DEPENDENCIES'
            and type(dependencies.get('protected_files')) is list
            and len(dependencies['protected_files']) == 423, 'complete 423 source closure absent')
    for index, entry in enumerate(dependencies['protected_files'], 1):
        require(entry['role'] == 'dep_'+str(index).zfill(4)
                and entry['path'] == entry['identity']['path'], 'dependency role/path differs')
        inputs.append(entry['identity'])
    # Authenticate the entire packet above before either complete helper is loaded.
    custody = load_module(payloads[str(Q/'custody.py')], 'ri138_external_custody', deadline)
    monitor = load_module(payloads[str(Q/'owned_process.py')], 'ri138_external_process', deadline)
    same(monitor.LIMITS, LIMITS, 'owned-process fixed limits differ')
    same(custody.MANIFEST_PINS['runtime'], manifest['expected_runtime'], 'expected runtime pin differs')
    same(custody.MANIFEST_PINS['history'], manifest['expected_history'], 'expected history pin differs')
    return {'phase': phase, 'directory': directory, 'plan': plan, 'plan_id': plan_id,
            'manifest': manifest, 'manifest_id': manifest_id, 'handoff_id': handoff_id,
            'subject': subject, 'inputs': inputs, 'custody': custody, 'monitor': monitor,
            'prepare_dispatch': prepare_dispatch, 'prepare_dispatch_id': prepare_dispatch_id,
            'source_names': {Path(path).name for path in payloads}|{'HANDOFF.json'},
            'dispatcher_handoff': dispatcher_handoff, 'dispatcher_subjects': dispatcher_subjects,
            'metadata_deadline': deadline}


class Phase:
    def __init__(self, context, spec):
        self.context, self.spec = context, spec
        self.name, self.directory = context['phase'].upper(), context['directory']
        self.first_error, self.later_errors, self.created = None, [], {}
        self.owned = False
        self.before, self.after, self.process, self.child_validation = None, None, None, None
        self.cards, self.final_checks, self.namespaces = {}, [], []
        self.process_attempted = False
        self.final_spent_ns = 0
        self.process_artifacts = []

    def fail(self, stage, error):
        propagate_hard(error)
        item = error_value(stage, error)
        if self.first_error is None:
            self.first_error = item
        else:
            self.later_errors.append(item)

    def add_receipt(self, receipt):
        if receipt['identity'] is not None:
            self.created[receipt['identity']['path']] = receipt['identity']
        for error in receipt['errors']:
            self.fail('durability', Refused(canonical(error)))
        return receipt

    def save(self, name, value, deadline, raw=False):
        receipt = write_new(self.directory/name, value if raw else raw_json(value), deadline)
        return self.add_receipt(receipt)

    def claim(self, deadline):
        marker = {'schema': 'ri138-phase-started-v1', 'phase': self.context['phase'],
                  'root_plan': self.context['plan_id'], 'started_ns': time.monotonic_ns(),
                  'automatic_retry_authorized': False}
        receipt = write_new(self.directory/(self.name+'_STARTED.json'), raw_json(marker), deadline, self)
        if not self.owned:
            raise Refused('phase was not claimed: '+canonical(receipt['errors']))
        self.add_receipt(receipt)
        require(not receipt['errors'], 'phase claim could not be durably completed')

    def observe(self, before, spec, deadline):
        label = self.name+('_BEFORE' if before else '_AFTER')
        sink, summary, close, sink_failure = None, None, None, None
        try:
            sink = DurableSink(self.directory/(label+'.jsonl'), deadline)
            sink.acquire()
        except Exception as error:
            sink_failure = error_value(label+'-open', error)
            self.fail(label+'-open', error)
        finally:
            if hard_unwinding():
                close_on_abort(sink)
        def failed_sink(record):
            raise Refused('journal unavailable: '+canonical(sink_failure))
        try:
            # A failed journal does not skip any independent object observation.
            summary = self.context['custody'].observe_all(spec, 'before' if before else 'after',
                                                         sink if sink_failure is None else failed_sink, deadline)
            require(summary['complete'] is True, label+' complete custody did not match')
        except Exception as error:
            self.fail(label, error)
        finally:
            if hard_unwinding():
                close_on_abort(sink)
            elif sink is not None and sink.fd is not None:
                close = sink.close()
                self.created[close['identity']['path']] = close['identity']
                for error in close['errors']:
                    self.fail(label+'-close', Refused(canonical(error)))
        result = {'summary': summary, 'log_close': close, 'summary_write': None}
        # Preserve even an incomplete summary and independent close errors.
        result['summary_write'] = self.save(label+'_SUMMARY.json', {'summary': summary, 'log_close': close},
                                            deadline)
        return result

    def namespace_check(self, expected, deadline, stage):
        try:
            self.namespaces.append(dict(namespace(self.directory, expected, deadline), stage=stage))
        except Exception as error:
            self.fail(stage, error)

    def source_namespace_check(self, deadline, stage):
        try:
            self.namespaces.append(dict(namespace(Q, self.context['source_names'], deadline), stage=stage))
        except Exception as error:
            self.fail(stage, error)

    def finish(self, input_names):
        # Never reload metadata as a new expectation after the body.
        remaining_final = max(0, 60*NS-self.final_spent_ns)
        after_deadline = min(time.monotonic_ns()+300*NS, OVERALL_DEADLINE-remaining_final)
        extended = self.spec
        try:
            extended = self.context['custody'].extend_spec(self.spec, list(self.created.values()))
        except Exception as error:
            self.fail('after-spec-extension', error)
        # Extension failure must not suppress the original complete inventory.
        self.after = self.observe(False, extended, after_deadline)
        self.source_namespace_check(after_deadline, 'after-source-namespace')
        final_started = time.monotonic_ns()
        deadline = min(final_started+remaining_final, OVERALL_DEADLINE)
        for identity in list(self.created.values()):
            row = {'expected': identity, 'matched': False}
            try:
                _, row['observed'] = read_file(Path(identity['path']), deadline, identity)
                row['matched'] = True
            except Exception as error:
                self.fail('final-artifact-check', error)
                row['error'] = error_value('final-artifact-check', error)
            self.final_checks.append(row)
        expected_names = set(input_names)|{Path(path).name for path in self.created}
        self.namespace_check(expected_names, deadline, 'final-operational-namespace')
        self.source_namespace_check(deadline, 'final-source-namespace')
        if SIGNALS:
            self.fail('signals', Refused('launcher interruption was recorded'))
        check_time(deadline)
        value = {'schema': 'ri138-'+self.context['phase']+'-result-v1', 'phase': self.context['phase'],
                 'success_before_result_close': self.first_error is None and not self.later_errors,
                 'root_plan': self.context['plan_id'], 'source_manifest': self.context['manifest_id'],
                 'root_prepare_dispatch': self.context['prepare_dispatch_id'],
                 'root_dispatch': self.context.get('run_dispatch_id'),
                 'source_handoff': self.context['handoff_id'], 'caller': self.context['plan']['caller'],
                 'case': self.context['plan']['case'], 'frozen_spec': self.created.get(str(self.directory/(self.name+'_EXPECTATIONS.json'))),
                 'before': self.before, 'after': self.after, 'cards': self.cards,
                 'process': self.process, 'child_validation': self.child_validation,
                 'process_artifact_checks': self.process_artifacts,
                 'first_error': self.first_error, 'later_errors': self.later_errors,
                 'received_signals': list(SIGNALS), 'created_files': list(self.created.values()),
                 'final_checks': self.final_checks, 'namespaces': self.namespaces,
                 'final_budget_spent_before_after_ns': self.final_spent_ns,
                 'final_budget_remaining_at_finalization_ns': remaining_final,
                 'phase_budgets': BUDGETS, 'child_limits': LIMITS,
                 'outer_tool_origin_established': False, 'root_acceptance': False,
                 'complete_caller_qualification': False, 'scientific_execution': False}
        receipt = self.save(self.name+'_RESULT.json', value, deadline)
        try:
            check_time(deadline)
        except Exception as error:
            receipt['errors'].append(error_value('result-close-deadline', error))
        success = value['success_before_result_close'] and not receipt['errors'] and not SIGNALS
        terminal = {'schema': 'ri138-phase-terminal-v1', 'phase': self.context['phase'],
                    'success': success, 'result': receipt['identity'], 'result_close_errors': receipt['errors']}
        stream = sys.stdout.buffer if success else sys.stderr.buffer
        stream.write(raw_json(terminal))
        stream.flush()
        # A late flush can leave stdout success text with a genuine nonzero exit;
        # outer completion, not that earlier text, is authoritative.
        check_time(deadline)
        return 0 if success else 2


def create_cards(state, deadline):
    context, directory, plan = state.context, state.directory, state.context['plan']
    require(state.first_error is None and state.before['summary']['complete'] is True
            and state.before['log_close']['errors'] == []
            and state.before['summary_write']['errors'] == [], 'no complete durable before evidence for cards')
    spec = context['custody'].validate_spec(state.spec)
    manifest = context['manifest']
    preflight = {'schema': 'ri136-root-external-policy-preflight-v1',
                 'status': 'ACCEPT_COMPLETE_EXTERNAL_BOOTSTRAP_AND_POLICY_CUSTODY',
                 'caller': plan['caller'], 'case': plan['case'],
                 'source_manifest': manifest['dispatcher_subject_manifest'],
                 'source_handoff': manifest['dispatcher_source_handoff'], 'dispatcher': manifest['dispatcher'],
                 'caller_source': context['subject']['caller'], 'control_source': context['subject']['controls'],
                 'all_runtime_files_match': True, 'all_runtime_namespace_and_host_match': True,
                 'all_source_history_dependencies_match': True, 'independent_external_observation': True,
                 'operational_directory': str(directory), 'expected_interpreter': spec['expected_interpreter'],
                 'evidence': {'root_plan': context['plan_id'], 'external_launcher_bootstrap': plan['external_bootstrap'],
                             'prepared_spec': state.created[str(directory/'PREPARE_EXPECTATIONS.json')],
                             'before_summary': state.before['summary_write']['identity'],
                             'before_log': state.before['log_close']['identity'],
                             'current_launcher_handoff': context['handoff_id']}}
    receipt = state.save('PREFLIGHT.json', preflight, deadline)
    require(not receipt['errors'], 'preflight durability failed')
    state.cards['preflight'] = receipt['identity']
    argv = [PYTHON, '-I', '-S', '-B', manifest['dispatcher']['path'], plan['caller'], plan['case']['id'], str(directory)]
    auth = {'schema': 'ri136-root-policy-case-authorization-v1', 'status': 'ADMIT_ONE_VERSION_BOUND_PURE_POLICY_CASE',
            'caller': plan['caller'], 'case': plan['case'],
            'source_manifest': manifest['dispatcher_subject_manifest'], 'source_handoff': manifest['dispatcher_source_handoff'],
            'external_preflight': receipt['identity'], 'dispatcher': manifest['dispatcher'],
            'caller_source': context['subject']['caller'], 'control_source': context['subject']['controls'],
            'outer_argv_prefix': argv, 'outer_cwd': str(directory), 'outer_environment': ENV, 'limits': LIMITS,
            'literal_dispatch_is_external': True, 'scientific_execution_authorized': False,
            'production_entry_authorized': False, 'retry_or_limit_relaxation_authorized': False}
    receipt = state.save('AUTHORIZATION.json', auth, deadline)
    require(not receipt['errors'], 'authorization durability failed')
    state.cards['authorization'] = receipt['identity']


def validate_prepare(context, plan_sha, deadline):
    directory, plan = context['directory'], context['plan']
    dispatch, dispatch_id = read_json(directory/'ROOT_DISPATCH.json', deadline)
    context['run_dispatch_id'] = dispatch_id
    exact(dispatch, ('schema', 'caller', 'case', 'authorization', 'outer_argv', 'outer_cwd', 'outer_environment',
                     'limits', 'literal_tool_invocation', 'root_plan', 'prepared_result', 'prepare_tool_result'),
          'root run dispatch')
    expected_argv, expected_tool = invocation('run', plan_sha, directory)
    require(dispatch['schema'] == 'ri136-literal-policy-dispatch-v1', 'root run dispatch schema differs')
    for field, expected in (('caller', plan['caller']), ('case', plan['case']), ('outer_cwd', str(directory)),
                            ('outer_environment', ENV), ('limits', LIMITS), ('literal_tool_invocation', expected_tool),
                            ('root_plan', context['plan_id'])):
        same(dispatch[field], expected, 'root run dispatch binding differs: '+field)
    require(dispatch['prepared_result']['path'] == str(directory/'PREPARE_RESULT.json')
            and dispatch['prepare_tool_result']['path'] == str(directory/'PREPARE_TOOL_RESULT.json')
            and dispatch['authorization']['path'] == str(directory/'AUTHORIZATION.json'), 'prepared reference path differs')
    prepared, prepared_id = read_json(directory/'PREPARE_RESULT.json', deadline, dispatch['prepared_result'])
    require(prepared.get('schema') == 'ri138-prepare-result-v1'
            and prepared.get('success_before_result_close') is True
            and prepared.get('first_error') is None and prepared.get('later_errors') == []
            and prepared.get('received_signals') == [] and prepared.get('phase') == 'prepare', 'prepare did not complete successfully')
    for field, expected in (('root_plan', context['plan_id']), ('source_manifest', context['manifest_id']),
                            ('source_handoff', context['handoff_id']), ('caller', plan['caller']), ('case', plan['case'])):
        same(prepared[field], expected, 'prepare result binding differs: '+field)
    for phase in ('before', 'after'):
        require(prepared[phase]['summary']['complete'] is True
                and prepared[phase]['log_close']['errors'] == []
                and prepared[phase]['summary_write']['errors'] == [], 'prepare custody or close was incomplete')
    require(type(prepared['created_files']) is list and len(prepared['created_files']) <= 32
            and all(row['matched'] is True for row in prepared['final_checks']), 'prepare final custody invalid')
    inputs, names = [dispatch_id, prepared_id], set()
    for identity in prepared['created_files']:
        identity_shape(identity, positive=False)
        path = Path(identity['path'])
        require(path.parent == directory and path.name in PREPARE_NAMES and path.name not in names,
                'invalid or repeated prepared file')
        names.add(path.name)
        read_file(path, deadline, identity)
        inputs.append(identity)
    require(names == PREPARE_NAMES-{'PREPARE_RESULT.json'}, 'complete prepare artifact inventory absent')
    auth, auth_id = read_json(directory/'AUTHORIZATION.json', deadline, prepared['cards']['authorization'])
    preflight, preflight_id = read_json(directory/'PREFLIGHT.json', deadline, prepared['cards']['preflight'])
    same(auth_id, dispatch['authorization'], 'root dispatch authorization differs')
    same(auth['external_preflight'], preflight_id, 'authorization preflight differs')
    child_argv = [PYTHON, '-I', '-S', '-B', context['manifest']['dispatcher']['path'],
                  plan['caller'], plan['case']['id'], str(directory), auth_id['sha256']]
    same(dispatch['outer_argv'], child_argv, 'digest-bearing child argv differs')
    same(auth['outer_argv_prefix'], child_argv[:-1], 'prepared child prefix differs')
    spec_raw, _ = read_file(directory/'PREPARE_EXPECTATIONS.json', deadline, prepared['frozen_spec'])
    saved_spec = context['custody'].validate_spec(spec_raw)
    common = {'caller': plan['caller'], 'case': plan['case'],
              'source_manifest': context['manifest']['dispatcher_subject_manifest'],
              'source_handoff': context['manifest']['dispatcher_source_handoff'],
              'dispatcher': context['manifest']['dispatcher'],
              'caller_source': context['subject']['caller'], 'control_source': context['subject']['controls']}
    same(preflight, dict(common, schema='ri136-root-external-policy-preflight-v1',
        status='ACCEPT_COMPLETE_EXTERNAL_BOOTSTRAP_AND_POLICY_CUSTODY',
        all_runtime_files_match=True, all_runtime_namespace_and_host_match=True,
        all_source_history_dependencies_match=True, independent_external_observation=True,
        operational_directory=str(directory), expected_interpreter=saved_spec['expected_interpreter'],
        evidence={'root_plan': context['plan_id'], 'external_launcher_bootstrap': plan['external_bootstrap'],
                  'prepared_spec': prepared['frozen_spec'],
                  'before_summary': prepared['before']['summary_write']['identity'],
                  'before_log': prepared['before']['log_close']['identity'],
                  'current_launcher_handoff': context['handoff_id']}), 'exact prepared preflight differs')
    same(auth, dict(common, schema='ri136-root-policy-case-authorization-v1',
        status='ADMIT_ONE_VERSION_BOUND_PURE_POLICY_CASE', external_preflight=preflight_id,
        outer_argv_prefix=child_argv[:-1], outer_cwd=str(directory), outer_environment=ENV, limits=LIMITS,
        literal_dispatch_is_external=True, scientific_execution_authorized=False,
        production_entry_authorized=False, retry_or_limit_relaxation_authorized=False),
        'exact prepared authorization differs')
    transcript, transcript_id = read_json(directory/'PREPARE_TOOL_RESULT.json', deadline,
                                         dispatch['prepare_tool_result'], tool_record=True)
    exact(transcript, ('record_type', 'source', 'invocation', 'result'), 'actual prepare tool transcription')
    require(transcript['record_type'] == 'transcription_of_genuine_exec_command_result'
            and transcript['source'] == TOOL_SOURCE, 'prepare tool record provenance labels differ')
    same(transcript['invocation'], context['prepare_dispatch']['literal_tool_invocation'], 'actual prepare invocation differs')
    actual = transcript['result']
    require(type(actual) is dict and type(actual.get('exit_code')) is int and actual['exit_code'] == 0
            and type(actual.get('chunk_id')) is str and bool(actual['chunk_id'])
            and 'session_id' not in actual and type(actual.get('output')) is str,
            'prepare tool completion is not a genuine terminal zero-exit structure')
    require(set(actual) <= {'exit_code', 'chunk_id', 'output', 'wall_time_seconds', 'original_token_count'}
            and type(actual.get('wall_time_seconds')) in (int, float)
            and math.isfinite(actual['wall_time_seconds']) and actual['wall_time_seconds'] >= 0,
            'actual tool result fields/timing differ')
    if 'original_token_count' in actual:
        require(type(actual['original_token_count']) is int and actual['original_token_count'] >= 0,
                'tool output-count metadata differs')
    expected_terminal = {'schema': 'ri138-phase-terminal-v1', 'phase': 'prepare', 'success': True,
                         'result': prepared_id, 'result_close_errors': []}
    require(actual['output'] == raw_json(expected_terminal).decode('ascii'), 'actual prepare terminal output differs')
    inputs.append(transcript_id)
    return inputs, child_argv, {'authorization': auth_id, 'preflight': preflight_id}


def validate_child(context, cards, process, deadline):
    require(type(process) is dict and process.get('success') is True
            and process.get('first_error') is None and process.get('later_errors') == []
            and process.get('received_signals') == [] and process.get('signal_overflow') == 0,
            'owned process did not independently succeed')
    require(process.get('omitted_error_count') == 0 and type(process.get('omitted_error_count')) is int
            and process.get('error_journal_unavailable') is False, 'owned-process error detail incomplete')
    report = process['report']
    require(type(report['returncode']) is int and report['returncode'] == 0
            and type(report['live_leader_samples']) is int and report['live_leader_samples'] > 0
            and report['terminal_empty'] is True and report['peak_owned_rss_bytes'] <= LIMITS['rss_bytes']
            and all(row['eof'] is True and row['complete'] is True for row in report['streams'].values()),
            'process lifecycle/resource/capture checks incomplete')
    stdout, stdout_id = read_file(context['directory']/'stdout.log', deadline, cap=LIMITS['output_bytes'])
    stderr, stderr_id = read_file(context['directory']/'stderr.log', deadline, cap=LIMITS['output_bytes'])
    require(stderr == b'', 'successful child emitted stderr')
    envelope = strict_json(stdout)
    require(raw_json(envelope) == stdout, 'child envelope is not one canonical complete JSON line')
    exact(envelope, ('result', 'first_error', 'postchecks', 'catalogue_postcheck', 'received_signals',
                     'elapsed_ns', 'qualified_as_complete'), 'child outer envelope')
    require(envelope['first_error'] is None and envelope['received_signals'] == []
            and envelope['qualified_as_complete'] is False and type(envelope['elapsed_ns']) is int
            and 0 <= envelope['elapsed_ns'] <= 120*NS
            and envelope['catalogue_postcheck'] == {'attempted': True, 'unchanged': True}
            and type(envelope['postchecks']) is list and bool(envelope['postchecks'])
            and all(row.get('unchanged') is True for row in envelope['postchecks']), 'child final envelope failed')
    protected = {}
    def register(identity):
        identity_shape(identity)
        path = identity['path']
        if path in protected:
            same(protected[path], identity, 'conflicting reconstructed dispatcher postcheck pin')
        protected[path] = identity
    register(cards['authorization'])
    for identity in (context['manifest']['dispatcher_subject_manifest'], context['manifest']['dispatcher_source_handoff'],
                     cards['preflight'], context['manifest']['dispatcher'], context['subject']['caller'],
                     context['subject']['controls']):
        register(identity)
    for identity in context['dispatcher_handoff']['files']:
        register(identity)
    for which in ('native', 'audit'):
        for role in ('caller', 'controls'):
            register(context['dispatcher_subjects']['subjects'][which][role])
    for family in ('acceptance', 'runner_ancestry'):
        for identity in context['dispatcher_subjects'][family].values():
            register(identity)
    register(context['dispatcher_subjects']['dependency_manifest'])
    expected_postchecks = [{'path': path, 'unchanged': True, 'identity': identity}
                           for path, identity in protected.items()]
    same(envelope['postchecks'], expected_postchecks, 'complete ordered dispatcher postcheck set/identities differ')
    result = envelope['result']
    exact(result, ('schema', 'status', 'caller', 'case', 'expected', 'observation', 'caller_source',
                   'control_source', 'dispatcher', 'source_manifest', 'source_handoff', 'root_authorization',
                   'external_preflight', 'external_preflight_assertions_checked_only',
                   'independent_outer_origin_and_custody_review_required', 'whole_entry',
                   'complete_caller_qualification', 'scientific_execution'), 'child exact result')
    manifest, plan, subject = context['manifest'], context['plan'], context['subject']
    bindings = {'schema': 'ri136-pure-policy-observation-v1', 'status': 'OBSERVED_EXACT_PURE_POLICY_CASE_ONLY',
                'caller': plan['caller'], 'case': plan['case'], 'caller_source': subject['caller'],
                'control_source': subject['controls'], 'dispatcher': manifest['dispatcher'],
                'source_manifest': manifest['dispatcher_subject_manifest'],
                'source_handoff': manifest['dispatcher_source_handoff'],
                'root_authorization': cards['authorization'], 'external_preflight': cards['preflight'],
                'external_preflight_assertions_checked_only': True,
                'independent_outer_origin_and_custody_review_required': True,
                'whole_entry': False, 'complete_caller_qualification': False, 'scientific_execution': False}
    for field, expected in bindings.items():
        same(result[field], expected, 'child result binding differs: '+field)
    contract, observation = subject['result_contract'], result['observation']
    exact(observation, contract['keys'], 'native/audit observation')
    exact(result['expected'], contract['expected_keys'], 'selected expected outcome')
    exact(observation['observed'], contract['observed_keys'], 'actual policy outcome')
    require(observation['id'] == plan['case']['id']
            and observation['coverage_scope'] == contract['coverage_scope']
            and observation['outcome'] == result['expected']['outcome']
            and observation['outcome'] in ('RETURN', 'REFUSED')
            and observation['boundary'] == {'dependency': 'validate_dependency_payload',
                'decision': 'validate_source_decision_payload', 'review': 'validate_source_review_payload',
                'checks': 'validate_current_target_checks'}[plan['case']['family']],
            'policy observation selection/scope differs')
    same(observation['observed'], {key: result['expected'][key] for key in contract['observed_keys']},
         'reported first policy outcome differs')
    for field in contract['true_fields']:
        require(observation[field] is True, 'required observation true field differs')
    for field in contract['false_fields']:
        require(observation[field] is False, 'required observation false field differs')
    if 'expected' in observation:
        same(observation['expected'], result['expected'], 'audit expected outcome report differs')
    # Exact pinned dispatcher/control execution, not a second extracted evaluator,
    # supplies the selected expected exception/message/boundary semantics.
    for name, identity in (('stdout', stdout_id), ('stderr', stderr_id)):
        same(report['sink_closes'][name]['identity'], identity, 'independent capture identity differs')
    return {'schema': 'ri138-child-envelope-check-v1', 'matched': True, 'stdout': stdout_id,
            'stderr': stderr_id, 'accepted_case': plan['case'], 'root_acceptance': False}


def collect_process_artifacts(state, deadline):
    """Keep original writer pins even after mismatch; never rebaseline a capture."""
    expected, process = {}, state.process
    if type(process) is dict:
        try:
            same(process['files'], {name: str(state.directory/name) for name in PROCESS_NAMES},
                 'owned-process file inventory differs')
        except Exception as error:
            state.fail('process-file-inventory', error)
        for key, name in (('report_file', 'PROCESS_REPORT.json'), ('close_receipt', 'PROCESS_CLOSE.json')):
            try:
                receipt = process[key]
                identity_shape(receipt['identity'], positive=False)
                require(receipt['identity']['path'] == str(state.directory/name), 'process receipt path differs')
                expected[name] = receipt['identity']
                require(receipt['errors'] == [] and receipt['directory_fsync_ok'] is True
                        and receipt['close']['errors'] == [] and receipt['close']['fsync_ok'] is True
                        and receipt['close']['closed'] is True, 'process final receipt did not close durably')
                same(receipt['close']['identity'], receipt['identity'], 'process receipt close identity differs')
            except Exception as error:
                state.fail('process-receipt-'+name, error)
        close_body = None
        if 'PROCESS_CLOSE.json' in expected:
            try:
                close_body, _ = read_json(state.directory/'PROCESS_CLOSE.json', deadline, expected['PROCESS_CLOSE.json'])
                same(close_body['report_write'], process['report_file'], 'saved process report receipt differs')
                require(close_body['schema'] == 'ri138-owned-process-close-v1'
                        and close_body['success_so_far'] is True and close_body['first_error'] is None
                        and close_body['later_errors'] == [] and close_body['omitted_error_count'] == 0
                        and close_body['error_journal_unavailable'] is False
                        and close_body['received_signals'] == [] and close_body['signal_overflow'] == 0,
                        'process close body contains failure')
            except Exception as error:
                state.fail('process-close-body', error)
        # Provisional returned report pins the first three logs; the authenticated
        # final CLOSE additionally pins the error journal after its actual close.
        try:
            sink_closes = dict(process.get('report', {}).get('sink_closes', {}))
        except Exception as error:
            state.fail('process-returned-sink-closes', error)
            sink_closes = {}
        if close_body is not None:
            try:
                final_closes = dict(close_body.get('sink_closes', {}))
            except Exception as error:
                state.fail('process-final-sink-closes', error)
                final_closes = {}
            for key, receipt in final_closes.items():
                if key in sink_closes:
                    try:
                        same(sink_closes[key], receipt, 'original/final process sink close differs')
                    except Exception as error:
                        state.fail('process-close-consistency-'+key, error)
                else:
                    sink_closes[key] = receipt
        for key, name in (('stdout', 'stdout.log'), ('stderr', 'stderr.log'),
                          ('events', 'process-events.jsonl'), ('errors', 'process-errors.jsonl')):
            try:
                receipt = sink_closes[key]
                identity_shape(receipt['identity'], positive=False)
                require(receipt['identity']['path'] == str(state.directory/name), 'original process log path differs')
                expected[name] = receipt['identity']
                require(receipt['errors'] == [] and receipt['closed'] is True and receipt['fsync_ok'] is True,
                        'process log close failed')
            except Exception as error:
                state.fail('process-original-log-'+name, error)
    for name in sorted(PROCESS_NAMES):
        pin = expected.get(name)
        row = {'path': str(state.directory/name), 'expected': pin, 'observed': None, 'matched': False}
        if pin is not None:
            # Preserve the original expected pin even if this reread now fails.
            state.created[pin['path']] = pin
        else:
            state.fail('process-original-pin-'+name, Refused('original writer identity unavailable'))
        try:
            raw, observed = read_file(state.directory/name, deadline)
            row['observed'] = observed
            require(pin is not None, 'partial process file has no authenticated original writer identity')
            same(observed, pin, 'process file differs from original writer identity')
            if name == 'PROCESS_REPORT.json':
                same(strict_json(raw), process['report'], 'saved process report differs from returned report')
            row['matched'] = True
        except Exception as error:
            row['error'] = error_value('process-file-'+name, error)
            state.fail('process-file-'+name, error)
        state.process_artifacts.append(row)


def run_phase(phase, plan_sha):
    started = time.monotonic_ns()
    metadata_deadline = min(started+60*NS, OVERALL_DEADLINE)
    context = authenticate(phase, plan_sha, metadata_deadline)
    input_names = set(ROOT_NAMES)
    command, cards = None, None
    if phase == 'run':
        extra, command, cards = validate_prepare(context, plan_sha, metadata_deadline)
        context['inputs'].extend(extra)
        input_names |= PREPARE_NAMES|RUN_INPUT_NAMES
    namespace(context['directory'], input_names, metadata_deadline)
    spec = context['custody'].load_expected(context['inputs'], metadata_deadline)
    state = Phase(context, spec)
    try:
        state.claim(metadata_deadline)
        receipt = state.save(state.name+'_EXPECTATIONS.json', spec, metadata_deadline, raw=True)
        require(not receipt['errors'], 'frozen expectation persistence failed')
        before_deadline = min(time.monotonic_ns()+300*NS, OVERALL_DEADLINE-(480 if phase == 'run' else 360)*NS)
        state.before = state.observe(True, context['custody'].extend_spec(spec, list(state.created.values())), before_deadline)
        require(state.first_error is None and not SIGNALS, 'complete before custody required')
        state.namespace_check(input_names|{Path(path).name for path in state.created}, before_deadline, 'before-body-namespace')
        state.source_namespace_check(before_deadline, 'before-source-namespace')
        require(state.first_error is None, 'operational namespace changed before body')
        if phase == 'prepare':
            create_cards(state, before_deadline)
        else:
            state.cards = cards
            # Original ROOT_DISPATCH identity is rechecked immediately before launch.
            original_dispatch = next(i for i in context['inputs'] if i['path'] == str(context['directory']/'ROOT_DISPATCH.json'))
            read_file(context['directory']/'ROOT_DISPATCH.json', before_deadline, original_dispatch)
            state.process_attempted = True
            state.process = context['monitor'].run_child(command, str(context['directory']), ENV,
                str(context['directory']), outer_deadline_ns=min(time.monotonic_ns()+120*NS, OVERALL_DEADLINE-360*NS))
            if not state.process.get('success'):
                state.fail('owned-process', Refused(canonical({'first_error': state.process.get('first_error'),
                                                             'later_errors': state.process.get('later_errors')})))
    except Exception as error:
        if not state.owned:
            raise
        state.fail('phase-body', error)
    finally:
        if not hard_unwinding() and state.owned and state.process_attempted:
            # Monitor final receipt persistence after collection_end, these
            # checks, and later finalization all share the same total60s budget.
            verification_started = time.monotonic_ns()
            if type(state.process) is dict:
                ended = state.process.get('report', {}).get('collection_end_ns')
                if type(ended) is int and started <= ended <= verification_started:
                    verification_started = ended
            verification_deadline = min(verification_started+60*NS, OVERALL_DEADLINE-300*NS)
            try:
                try:
                    collect_process_artifacts(state, verification_deadline)
                except Exception as error:
                    state.fail('process-artifacts', error)
                try:
                    state.child_validation = validate_child(context, cards, state.process, verification_deadline)
                except Exception as error:
                    state.fail('child-envelope', error)
                try:
                    check_time(verification_deadline)
                except Exception as error:
                    state.fail('shared-final-budget', error)
            finally:
                state.final_spent_ns = time.monotonic_ns()-verification_started
    require(state.owned, 'no phase ownership; no result or postchecks claimed')
    return state.finish(input_names)


def main():
    global OVERALL_DEADLINE
    require(len(sys.argv) == 3, 'require prepare/run and root plan SHA256')
    OVERALL_DEADLINE = time.monotonic_ns()+840*NS
    for number in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM):
        signal.signal(number, signal_received)
    signal.setitimer(signal.ITIMER_REAL, 840)
    try:
        return run_phase(sys.argv[1], sys.argv[2])
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BaseException as error:
        if isinstance(error, SystemExit):
            raise
        print('RI138 LAUNCH REFUSAL: '+type(error).__name__+': '+str(error)[:4096], file=sys.stderr)
        sys.exit(2)
