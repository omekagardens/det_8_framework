"""RI171 one-case worker. All target operations are prospective, not executed in authoring.
Loads the entire exact subject once; substitutions are named per manifest and logged.
"""
import hashlib
import json
import os
import selectors
import signal
import subprocess
import sys
import time
import types


def bootstrap(path, digest):
    with open(path, 'rb') as f:
        raw = f.read(262145)
    if len(raw) > 262144 or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('worker request digest/cap')
    request = json.loads(raw)
    pin = request['sources']['protocol']
    with open(pin['path'], 'rb') as f:
        body = f.read(1048577)
    if len(body) != pin['bytes'] or hashlib.sha256(body).hexdigest() != pin['sha256']:
        raise ValueError('worker protocol pin')
    module = types.ModuleType('ri171_protocol')
    module.__file__ = pin['path']
    exec(compile(body, pin['path'], 'exec'), module.__dict__)
    return module


class Proxy:
    def __init__(self, base, **changes):
        self.base, self.changes = base, changes
    def __getattr__(self, name):
        return self.changes[name] if name in self.changes else getattr(self.base, name)


class Instrument:
    def __init__(self, protocol, target, case, request, directory):
        self.P, self.T, self.C, self.R, self.D = protocol, target, case, request, directory
        self.fault = case['fault']
        self.events, self.handles, self.input_fds, self.output_fds = [], [], {}, {}
        self.once, self.write_steps, self.ps_calls = set(), {}, 0
        self.killed, self.clock_shift, self.last_table = False, 0, None
        self.start, self.deadline = time.monotonic_ns(), time.monotonic_ns() + 315000000000
        self.leaf_identity = None
        self.original = {k: getattr(target, k) for k in ('process_snapshot', 'discover', 'canonical', 'sync_base', 'new_file', 'error')}
        self.target_stream = case.get('stream') or ('stderr' if '.stderr.' in self.fault else 'stdout')
        self.target_input_tag = ('ps' if case['kind'] == 'observer' else 'caller') + ':' + self.target_stream

    def event(self, name, **fields):
        if len(self.events) >= 131072:
            raise RuntimeError('RI171 trace event cap')
        self.events.append({'event': name, 'monotonic_ns': time.monotonic_ns(), **json.loads(json.dumps(fields, allow_nan=False))})

    def once_at(self, key):
        if key in self.once:
            return False
        self.once.add(key)
        return True

    def io_error(self, event, tag, message, would_block=False):
        self.event(event, tag=tag, type='BlockingIOError' if would_block else 'OSError', message=message)
        if would_block:
            raise BlockingIOError(message)
        raise OSError(message)

    def monotonic(self):
        return time.monotonic_ns() + self.clock_shift

    def read(self, fd, n):
        tag = self.input_fds.get(fd)
        selected = tag == self.target_input_tag
        if selected and '.read_would_block.' in self.fault and self.once_at('read_transient'):
            self.io_error('read_error', tag, 'RI169_READ_TRANSIENT', True)
        if selected and (self.fault.endswith('.read') or self.fault.endswith('.unregister_close')) and self.once_at('read_fault'):
            self.io_error('read_error', tag, 'RI167_F01_READ')
        if tag == 'caller:stdout' and self.fault == 'hard_drain' and self.once_at('hard_drain'):
            self.event('hard_injection', phase='drain')
            raise self.T.HardStop('RI171_HARD_DRAIN')
        raw = os.read(fd, n)
        if tag:
            self.event('read', tag=tag, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
        return raw

    def write(self, fd, raw):
        tag = self.output_fds.get(fd)
        selected = tag == self.target_stream
        phase = self.write_steps.get(tag, 0)
        partial = self.fault.endswith('.partial_write') or '.write_would_block.after_prefix' in self.fault
        if selected and partial:
            if phase == 0:
                n = os.write(fd, raw[:17])
                self.write_steps[tag] = 1
                self.event('write', tag=tag, requested=len(raw), written=n, injection='real-prefix')
                return n
            if phase == 1:
                self.write_steps[tag] = 2
                wb = '.write_would_block.' in self.fault
                self.io_error('write_error', tag, 'RI169_WRITE_AFTER_PREFIX' if wb else 'RI167_F01_PARTIAL_WRITE', wb)
        if selected and (self.fault.endswith('.write') or '.write_would_block.zero_progress' in self.fault) and self.once_at('write_fault'):
            wb = '.write_would_block.' in self.fault
            self.io_error('write_error', tag, 'RI169_WRITE_ZERO_PROGRESS' if wb else 'RI167_F01_WRITE', wb)
        if tag == 'processes' and self.fault.startswith(('S10.journal.', 'S13.journal.')):
            if phase == 0:
                n = os.write(fd, raw[:17])
                self.write_steps[tag] = 1
                self.event('write', tag=tag, requested=len(raw), written=n, injection='real-prefix')
                return n
            self.io_error('write_error', tag, 'RI171_JOURNAL_WRITE')
        if tag == 'completion' and self.fault == 'receipt_partial':
            if phase == 0:
                n = os.write(fd, raw[:17])
                self.write_steps[tag] = 1
                self.event('write', tag=tag, requested=len(raw), written=n, injection='real-prefix')
                return n
            self.io_error('write_error', tag, 'RI171_RECEIPT_WRITE')
        if selected and self.fault.endswith('.short_write'):
            n = os.write(fd, raw[:7])
        else:
            n = os.write(fd, raw)
        if tag:
            self.event('write', tag=tag, requested=len(raw), written=n)
        return n

    def fsync(self, fd):
        tag = self.output_fds.get(fd)
        if tag:
            self.event('fsync_attempt', tag=tag)
        if tag == self.target_stream and self.fault == 'late_fsync' and self.once_at('late_fsync'):
            self.io_error('fsync_error', tag, 'RI171_LATE_FSYNC')
        if tag == 'completion' and self.fault == 'receipt_fsync':
            self.io_error('fsync_error', tag, 'RI171_RECEIPT_FSYNC')
        if tag == 'stdout' and self.fault == 'hard_finalization' and self.once_at('hard_finalization'):
            self.event('hard_injection', phase='finalization')
            raise self.T.HardStop('RI171_HARD_FINALIZATION')
        if tag == self.target_stream and self.fault in ('late_replacement', 'late_descriptor', 'late_drift', 'late_size') and self.once_at('late_mutation'):
            path = self.T.PREFIX + ('.processes.jsonl' if tag == 'processes' else '.'+tag)
            before_raw, before_pin, _ = self.P.capture(path, 67108864)
            if self.fault == 'late_replacement':
                os.rename(path, path+'.original')
                self.P.put(path, b'RI171 replacement\n')
            elif self.fault == 'late_descriptor':
                replacement = path + '.fd_replacement'
                self.P.put(replacement, b'RI171 descriptor replacement\n')
                other = os.open(replacement, os.O_WRONLY | os.O_NOFOLLOW)
                try:
                    os.dup2(other, fd)
                finally:
                    os.close(other)
            elif self.fault == 'late_size':
                os.write(fd, b'Q')
            else:
                os.pwrite(fd, b'Q', 0)
            after_raw, after_pin, _ = self.P.capture(path, 67108864)
            self.event('file_mutation', tag=tag, fault=self.fault, before=before_pin, after=after_pin,
                       before_first_byte=before_raw[0] if before_raw else None)
        result = os.fsync(fd)
        if tag:
            self.event('fsync_complete', tag=tag)
        return result

    def close(self, fd):
        tag = self.output_fds.pop(fd, None)
        if tag:
            self.event('close_attempt', tag=tag)
        result = os.close(fd)
        if tag:
            self.event('close_complete', tag=tag)
        if tag == self.target_stream and self.fault == 'late_close' and self.once_at('late_close'):
            self.io_error('close_error', tag, 'RI171_LATE_CLOSE_AFTER_REAL_CLOSE')
        return result

    def new_file(self, path):
        fd = self.original['new_file'](path)
        tag = 'completion' if path.endswith('.completion.json') else 'processes' if path.endswith('.processes.jsonl') else 'stderr' if path.endswith('.stderr') else 'stdout'
        self.output_fds[fd] = tag
        self.event('file_acquired', tag=tag, path=path, fd=fd)
        return fd

    def sync_base(self):
        n = sum(x['event'] == 'sync_base_attempt' for x in self.events) + 1
        self.event('sync_base_attempt', ordinal=n)
        if n == 2 and self.fault == 'receipt_base_sync':
            raise OSError('RI171_RECEIPT_BASE_SYNC')
        result = self.original['sync_base']()
        # PREFIX is the declared nested fixture substitution. Keep the actual
        # production BASE fsync, then separately durably sync the fixture owner.
        fd = os.open(self.D, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)
        self.event('fixture_directory_sync', path=self.D)
        self.event('sync_base_complete', ordinal=n)
        if n == 2 and self.fault == 'receipt_post_receipt':
            raise OSError('RI171_POST_RECEIPT')
        return result

    def target_error(self, errors, stage, exc):
        self.event('source_error', stage=stage, type=type(exc).__name__, message=str(exc)[:240])
        return self.original['error'](errors, stage, exc)

    def canonical(self, value):
        if type(value) is dict and value.get('schema') == 'ri165-observed-outer-completion-v1':
            self.event('receipt_candidate', value=value)
        if self.fault == 'journal_cap' and type(value) is dict and 'stdout_hex' in value:
            self.event('canonical_double', bytes=67108865, value=value)
            return b'x' * 67108865
        if self.fault.startswith(('S10.journal.', 'S13.journal.')) and type(value) is dict and 'stdout_hex' in value:
            self.event('journal_candidate', value=value)
        return self.original['canonical'](value)

    def wait_ready(self, path, process, cap_seconds):
        end = min(self.deadline, time.monotonic_ns()+int(cap_seconds*1000000000))
        while not os.path.exists(path):
            if process.poll() is not None or time.monotonic_ns() >= end:
                raise RuntimeError('RI171 inert ready barrier not reached')
            time.sleep(0.001)
        self.event('ready_barrier', path=path)

    def identity(self, pid):
        # Independent fixture recovery observation; not a subject snapshot/qualification credit.
        p = subprocess.run(['/bin/ps', '-p', str(pid), '-o', 'pid=,ppid=,pgid=,lstart='],
                           stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           env=self.P.ENV, cwd=self.P.BASE, timeout=0.2, check=False)
        fields = p.stdout.decode('ascii').split()
        self.event('recovery_identity_observation', pid=pid, returncode=p.returncode,
                   stdout_hex=p.stdout.hex(), stderr_hex=p.stderr.hex())
        if p.returncode != 0 or p.stderr or len(fields) != 8:
            raise RuntimeError('RI171 fixture recovery identity unavailable')
        return {'pid': int(fields[0]), 'ppid': int(fields[1]), 'pgid': int(fields[2]), 'birth': ' '.join(fields[3:])}

    def popen(self, argv, **kwargs):
        kind = 'ps' if argv == self.T.PS else 'caller'
        actual = argv
        if kind == 'ps' and self.C['kind'] == 'observer' and self.fault != 'ps_real':
            actual = [self.P.VENDOR, '-I', '-S', '-B', self.R['sources']['payload']['path'], 'observer', self.fault, self.D]
        self.event('popen_attempt', kind=kind, subject_argv=argv, actual_argv=actual,
                   parent_timer=list(signal.getitimer(signal.ITIMER_REAL)))
        p = subprocess.Popen(actual, **kwargs)
        handle_id = len(self.handles) + 1
        self.handles.append((handle_id, kind, p))
        self.event('popen_acquired', handle_id=handle_id, kind=kind, pid=p.pid)
        wrapped = Process(self, kind, p)
        if kind == 'caller':
            self.wait_ready(os.path.join(self.D, 'READY.json'), p, 2)
            if self.fault in ('observed_descendant', 'fast_reparent'):
                raw, _, _ = self.P.capture(os.path.join(self.D, 'LEAF.json'), 4096)
                leaf = self.P.decode(raw)
                self.leaf_identity = self.identity(leaf['pid'])
                self.P.need(self.leaf_identity['pgid'] == leaf['pid'], 'fixture leaf session leader')
                self.P.put(os.path.join(self.D, 'RECOVERY_IDENTITY.json'), self.leaf_identity)
            if self.fault.endswith('already_exited') or self.fault == 'fast_reparent':
                p.wait(timeout=2)
                self.event('inert_pre_observer_exit', pid=p.pid, returncode=p.returncode)
            if self.fault == 'hard_ownership':
                self.event('hard_injection', phase='ownership')
                raise self.T.HardStop('RI171_HARD_OWNERSHIP')
        elif '.ps.' in self.fault:
            self.wait_ready(os.path.join(self.D, 'OBSERVER_READY.json'), p, 0.1)
        return wrapped

    def snapshot(self, deadline, journal):
        self.ps_calls += 1
        early = self.fault.startswith('S05.fallback.') or self.fault.startswith('S13.observer.') or self.fault in ('S13.poll_unavailable', 'S13.deadline_exhausted')
        if early or (self.fault == 'late_observer' and self.ps_calls > 1):
            message = 'RI171_OBSERVER_FAILURE'
            self.event('observer_double', ordinal=self.ps_calls, message=message)
            if self.fault == 'S13.deadline_exhausted':
                self.clock_shift = 316000000000
                self.event('clock_double', nanoseconds=self.clock_shift, genuine_timing_credit=False)
            raise self.T.Refusal(message)
        if self.fault == 'real_expiry' and self.last_table is not None:
            # Declared stale observer has bounded real latency; do not spin the
            # fixture trace into its own cap before the actual315-second timer.
            time.sleep(min(0.005, max(0, (self.deadline-time.monotonic_ns())/1000000000)))
            self.event('stale_table_double', ordinal=self.ps_calls)
            return {k: dict(v) for k, v in self.last_table.items()}
        table = self.original['process_snapshot'](deadline, journal)
        self.last_table = table
        return table

    def discover(self, table, pid, known):
        live = self.original['discover'](table, pid, known)
        self.event('discover', caller=pid, live=sorted(live), known=sorted(known))
        if self.fault == 'observed_descendant' and self.leaf_identity and self.leaf_identity['pid'] in known:
            marker = os.path.join(self.D, 'DESCENDANT_OBSERVED.json')
            if not os.path.exists(marker):
                self.P.put(marker, {'pid': self.leaf_identity['pid'], 'observed': True})
        return live

    def killpg(self, pgid, number):
        self.event('signal_group', pgid=pgid, signal=int(number))
        return os.killpg(pgid, number)

    def install(self):
        t = self.T
        t.os = Proxy(os, read=self.read, write=self.write, fsync=self.fsync, close=self.close, killpg=self.killpg)
        t.time = Proxy(time, monotonic_ns=self.monotonic)
        t.subprocess = Proxy(subprocess, Popen=self.popen)
        t.selectors = Proxy(selectors, DefaultSelector=lambda: Selector(self))
        t.sys = Proxy(sys, argv=[os.path.abspath(t.__file__)])
        t.ARGV = [self.P.VENDOR, '-I', '-S', '-B', self.R['sources']['payload']['path'], 'caller', self.fault, self.D]
        t.PREFIX = os.path.join(self.D, 'outer')
        t.new_file, t.sync_base, t.canonical = self.new_file, self.sync_base, self.canonical
        t.error = self.target_error
        t.process_snapshot, t.discover = self.snapshot, self.discover

    def recovery(self):
        result = []
        # Direct owned handles and the separately observed leaf only. This phase grants
        # no subject cleanup credit and creates no new ordinary315-second wait budget.
        for handle_id, kind, p in self.handles:
            try:
                if p.poll() is None:
                    p.kill()
                end = self.deadline
                while p.poll() is None and time.monotonic_ns() < end:
                    time.sleep(0.002)
                result.append({'handle_id': handle_id, 'kind': kind, 'pid': p.pid, 'returncode': p.returncode,
                               'reaped': p.returncode is not None})
            except BaseException as exc:
                result.append({'handle_id': handle_id, 'kind': kind, 'pid': p.pid, 'error': type(exc).__name__+': '+str(exc)})
        if self.fault in ('observed_descendant', 'fast_reparent') and self.leaf_identity is None:
            result.append({'kind':'leaf', 'identity_unavailable':True, 'requires_external_recovery_review':True})
        if self.leaf_identity:
            try:
                now = self.identity(self.leaf_identity['pid'])
                same = all(now[k] == self.leaf_identity[k] for k in ('pid', 'pgid', 'birth'))
                if not same:
                    raise RuntimeError('fixture leaf identity changed; refuse signal')
                os.killpg(now['pgid'], signal.SIGKILL)
                self.event('leaf_recovery_signal', identity=now, signal=int(signal.SIGKILL))
                result.append({'kind': 'leaf', 'identity': now, 'kill_sent': True,
                               'absence_proven': False, 'requires_external_recovery_review': True})
            except BaseException as exc:
                result.append({'kind': 'leaf', 'identity': self.leaf_identity,
                               'error': type(exc).__name__+': '+str(exc), 'requires_external_recovery_review': True})
        return result


class Pipe:
    def __init__(self, inst, tag, raw):
        self.i, self.tag, self.raw = inst, tag, raw
        inst.input_fds[raw.fileno()] = tag
    def fileno(self):
        return self.raw.fileno()
    def close(self):
        self.i.event('pipe_close_attempt', tag=self.tag)
        if self.i.fault.endswith('.unregister_close') and self.tag == self.i.target_input_tag and self.i.once_at('pipe_close_fault'):
            self.i.io_error('pipe_close_error', self.tag, 'RI171_PIPE_CLOSE')
        fd = self.raw.fileno()
        value = self.raw.close()
        self.i.input_fds.pop(fd, None)
        self.i.event('pipe_closed', tag=self.tag)
        return value


class Process:
    def __init__(self, inst, kind, raw):
        self.i, self.kind, self.raw = inst, kind, raw
        self.stdout, self.stderr = Pipe(inst, kind+':stdout', raw.stdout), Pipe(inst, kind+':stderr', raw.stderr)
    def __getattr__(self, name):
        return getattr(self.raw, name)
    @property
    def returncode(self):
        if self.kind == 'caller' and self.i.fault.endswith('.nonreap'):
            return None
        return self.raw.returncode
    def poll(self):
        if self.kind == 'caller' and self.i.killed and self.i.fault == 'S13.poll_unavailable':
            self.i.io_error('poll_error', 'caller', 'RI171_POLL_UNAVAILABLE')
        if self.kind == 'caller' and self.i.killed and self.i.fault.endswith('.nonreap'):
            self.i.clock_shift = 316000000000
            self.i.event('poll_double', kind=self.kind, observed_returncode=None, genuine_reap=False)
            return None
        code = self.raw.poll()
        self.i.event('poll', kind=self.kind, pid=self.raw.pid, returncode=code)
        return code
    def kill(self):
        self.i.killed = True
        self.i.event('direct_kill_attempt', kind=self.kind, pid=self.raw.pid)
        if self.kind == 'caller' and self.i.fault.endswith('.kill_failure') and self.i.once_at('kill_fault'):
            self.i.io_error('direct_kill_error', 'caller', 'RI171_KILL_FAILURE')
        return self.raw.kill()


class Selector:
    def __init__(self, inst):
        self.i, self.raw = inst, selectors.DefaultSelector()
    def register(self, pipe, events, data):
        result = self.raw.register(pipe, events, data)
        self.i.event('register_installed', tag=pipe.tag)
        if self.i.fault.endswith('.registration') and pipe.tag == self.i.target_input_tag and self.i.once_at('register_fault'):
            self.i.io_error('register_error', pipe.tag, 'RI167_F01_REGISTER')
        return result
    def unregister(self, pipe):
        self.i.event('unregister_attempt', tag=pipe.tag)
        if self.i.fault.endswith('.unregister_close') and pipe.tag == self.i.target_input_tag and self.i.once_at('unregister_fault'):
            self.i.io_error('unregister_error', pipe.tag, 'RI171_UNREGISTER')
        return self.raw.unregister(pipe)
    def select(self, timeout):
        return self.raw.select(timeout)
    def close(self):
        self.i.event('selector_close_attempt')
        return self.raw.close()


def direct(inst):
    t, f = inst.T, inst.fault
    a = {'pid': 12001, 'ppid': 1, 'pgid': 12001, 'birth': 'Wed Sep 30 00:00:00 2026'}
    table, known = {a['pid']: dict(a)}, {a['pid']: dict(a)}
    if f == 'descendant_cap':
        for n in range(1, 65):
            table[12001+n] = {'pid': 12001+n, 'ppid': 12001, 'pgid': 12001+n, 'birth': a['birth']}
        inst.event('direct_operand', target='discover', table=table, known=known)
        return t.discover(table, 12001, known)
    if f in ('identity_birth', 'identity_pgid', 'identity_signal_birth', 'identity_signal_pgid'):
        table[12001]['birth' if f.endswith('birth') else 'pgid'] = 'changed' if f.endswith('birth') else 12002
        target = 'signal_observed' if '_signal_' in f else 'discover'
        inst.event('direct_operand', target=target, table=table, known=known)
        if target == 'signal_observed':
            t.os = Proxy(t.os, killpg=lambda pgid, sig: inst.event('signal_double', pgid=pgid, signal=int(sig)))
            return t.signal_observed(table, known, signal.SIGKILL)
        return t.discover(table, 12001, known)
    table[12002] = {'pid': 12002, 'ppid': 1, 'pgid': 12001, 'birth': a['birth']}
    if f == 'identity_safe_second':
        b = {'pid': 13001, 'ppid': 1, 'pgid': 13001, 'birth': a['birth']}
        table[13001], known[13001] = b, dict(b)
    t.os = Proxy(t.os, killpg=lambda pgid, sig: inst.event('signal_double', pgid=pgid, signal=int(sig)))
    inst.event('direct_operand', target='signal_observed', table=table, known=known)
    return t.signal_observed(table, known, signal.SIGKILL)


def main():
    path, digest = sys.argv[1:]
    P = bootstrap(path, digest)
    request, case, bodies, before = P.request(path, digest)
    P.need(sys.executable == P.VENDOR and sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'worker bootstrap')
    P.need(dict(os.environ) == P.ENV and os.getcwd() == P.BASE, 'worker environment')
    directory = os.path.join(request['operation'], 'body')
    P.need(not os.path.lexists(directory), 'no repeat body')
    os.mkdir(directory, 0o700)
    target = types.ModuleType('ri171_exact_subject')
    target.__file__ = P.SUBJECT
    exec(compile(bodies['subject'], P.SUBJECT, 'exec'), target.__dict__)
    inst = Instrument(P, target, case, request, directory)
    inst.install()
    report = {'schema': 'ri171-case-observation-v1', 'case_id': case['id'], 'before': before,
              'source_subject': request['sources']['subject'], 'entry': case['kind'], 'fault': case['fault'],
              'return': None, 'exception': None, 'worker_errors': [], 'journal': [], 'recovery': None}
    if case['fault'] == 'receipt_preexists':
        P.put(target.PREFIX+'.completion.json', b'RI171 preexisting\n')
    began = time.monotonic_ns()
    try:
        if case['kind'] == 'observer':
            # Call the real exported function; no whole-supervisor credit.
            observer_deadline = time.monotonic_ns()+400000000
            inst.event('observer_entry', deadline_monotonic_ns=observer_deadline)
            report['return'] = inst.original['process_snapshot'](observer_deadline, report['journal'].append)
        elif case['kind'] == 'direct':
            report['return'] = direct(inst)
        else:
            report['return'] = target.supervise()
    except BaseException as exc:
        report['exception'] = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        ended = time.monotonic_ns()
        # Exact subject HardStop may leave its timer installed. Test-controller cleanup
        # is recorded separately and grants no success to a failed/incomplete subject.
        signal.setitimer(signal.ITIMER_REAL, 0)
        report['entry_start_monotonic_ns'], report['entry_end_monotonic_ns'] = began, ended
        try:
            report['recovery'] = inst.recovery()
        except BaseException as exc:
            report['worker_errors'].append({'stage': 'fixture_recovery', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            after, failures = P.postcheck(request, path, digest)
            report['after_sources'] = after['sources']
            report['worker_errors'].extend({'stage':'complete_custody_tail/'+e['stage'],'type':e['type'],'message':e['message']} for e in failures)
            P.need(after == before, 'whole input/source/prerequisite state changed')
        except BaseException as exc:
            report['worker_errors'].append({'stage': 'source_tail', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            P.put(os.path.join(request['operation'], 'TRACE.json'), inst.events)
        except BaseException as exc:
            report['worker_errors'].append({'stage': 'trace_tail', 'type': type(exc).__name__, 'message': str(exc)})
        try:
            report['body_tree'] = P.tree(directory)
        except BaseException as exc:
            report['worker_errors'].append({'stage': 'tree_tail', 'type': type(exc).__name__, 'message': str(exc)})
        P.put(os.path.join(request['operation'], 'CASE.json'), report)
    return 0 if not report['worker_errors'] else 2


if __name__ == '__main__':
    sys.exit(main())
