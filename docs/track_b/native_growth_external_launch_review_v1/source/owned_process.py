"""RI138 source-only external owned-process collection, not execution authority.

The root orchestrator authenticates this complete module and the exact command,
runtime, cards and reservation before calling run_child once. No source loads,
policy calls, root cards or tool-origin assertions are implemented here.
"""

import base64
from hashlib import sha256
import json
import os
from pathlib import Path
import selectors
import signal
import stat
import subprocess
import sys
import time


LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'output_bytes': 8388608, 'auxiliary_metadata_bytes': 67108864,
          'sample_interval_ms': 50, 'ps_timeout_ms': 250}
PS_ARGV = ['/bin/ps', '-axo', 'pid=,pgid=,rss=']
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
FILES = ('stdout.log', 'stderr.log', 'process-events.jsonl',
         'process-errors.jsonl', 'PROCESS_REPORT.json', 'PROCESS_CLOSE.json')
NS = 1000000000
TAIL_NS = 2 * NS
META_RESERVE = 1048576
ERROR_LIMIT = 524288
FINAL_LIMIT = 262144
MAX_LATER_ERRORS = 64
MAX_ERROR_MESSAGE = 1024
USED = False


class CollectionFailure(RuntimeError):
    pass


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def error_value(phase, error):
    message = str(error)
    return {'phase': phase, 'type': type(error).__name__,
            'message': message[:MAX_ERROR_MESSAGE],
            'message_truncated': len(message) > MAX_ERROR_MESSAGE,
            'original_message_characters': len(message),
            'monotonic_ns': time.monotonic_ns()}


def hard_abort_active():
    error = sys.exc_info()[1]
    return error is not None and not isinstance(error, Exception)


def abort_owned(owner, extra_process=None):
    """No durable-tail claim: only best-effort immediate signals and closes."""
    if owner.hard_abort_attempted:
        return
    owner.hard_abort_attempted = True
    processes = [extra_process, owner.census_process]
    processes.extend(p for p in owner.ps_handles if p.returncode is None)
    if owner.child is not None and not owner.terminal_empty:
        processes.append(owner.child)
    pids = set()
    for process in processes:
        if process is None or process.pid in pids:
            continue
        pids.add(process.pid)
        for action in (lambda: os.killpg(process.pid, signal.SIGKILL),
                       lambda: os.kill(process.pid, signal.SIGKILL)):
            try:
                action()
            except Exception:
                pass  # No invented successful cleanup; root retains hard abort.
    for process in [owner.child, extra_process, owner.census_process]+owner.ps_handles:
        if process is not None:
            for name in ('stdout', 'stderr'):
                try:
                    stream = getattr(process, name)
                    if stream is not None and not stream.closed:
                        stream.close()
                except Exception:
                    pass
    for sink in owner.sinks.values():
        if sink.fd is not None and not sink.closed:
            try:
                os.close(sink.fd)
                sink.fd, sink.closed = None, True
            except Exception:
                pass
    if owner.selector is not None:
        try:
            owner.selector.close()
        except Exception:
            pass
    for signum, handler in owner.old_handlers.items():
        try:
            signal.signal(signum, handler)
        except Exception:
            pass


def directory_sync(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class Sink:
    """Exclusive bounded byte sink; a short/failed write is never success."""

    def __init__(self, path, limit):
        self.path, self.limit = str(path), limit
        self.fd, self.written, self.hash = None, 0, sha256()
        self.identity, self.closed = None, False
        self.fd = os.open(self.path, os.O_RDWR | os.O_CREAT | os.O_EXCL |
                          os.O_NOFOLLOW, 0o600)

    def append(self, data, durable=False):
        if self.fd is None or self.closed:
            raise CollectionFailure('write to unavailable evidence sink: '+self.path)
        if self.written + len(data) > self.limit:
            raise CollectionFailure('evidence sink byte ceiling: '+self.path)
        view = memoryview(data)
        while view:
            count = os.write(self.fd, view)
            if count <= 0:
                raise CollectionFailure('nonpositive evidence write: '+self.path)
            self.hash.update(view[:count])
            self.written += count
            view = view[count:]
        if durable:
            os.fsync(self.fd)

    def close(self):
        receipt = {'path': self.path, 'written_bytes': self.written,
                   'flush_attempted': False, 'fsync_ok': False,
                   'identity': None, 'closed': self.closed, 'errors': []}
        if self.fd is None or self.closed:
            return receipt
        try:
            receipt['flush_attempted'] = True  # os.write has no userspace buffer.
            os.fsync(self.fd)
            receipt['fsync_ok'] = True
        except Exception as error:
            receipt['errors'].append(error_value('sink-fsync', error))
        try:
            before = os.fstat(self.fd)
            if not stat.S_ISREG(before.st_mode) or before.st_size != self.written:
                raise CollectionFailure('capture size/type changed: '+self.path)
            actual, offset = sha256(), 0
            while offset < self.written:
                chunk = os.pread(self.fd, min(65536, self.written-offset), offset)
                if not chunk:
                    raise CollectionFailure('short evidence reread: '+self.path)
                actual.update(chunk)
                offset += len(chunk)
            after, named = os.fstat(self.fd), os.lstat(self.path)
            for key in ('st_dev', 'st_ino', 'st_mode', 'st_size', 'st_mtime_ns', 'st_ctime_ns'):
                if getattr(before, key) != getattr(after, key) or getattr(after, key) != getattr(named, key):
                    raise CollectionFailure('evidence identity changed: '+self.path)
            if stat.S_ISLNK(named.st_mode) or actual.hexdigest() != self.hash.hexdigest():
                raise CollectionFailure('evidence bytes or path changed: '+self.path)
            self.identity = {'path': self.path, 'bytes': self.written,
                             'sha256': actual.hexdigest()}
            receipt['identity'] = self.identity
        except Exception as error:
            receipt['errors'].append(error_value('sink-identity', error))
        finally:
            if hard_abort_active():
                # A parent watchdog must not enter another fsync/readback tail.
                try:
                    os.close(self.fd)
                    self.fd, self.closed = None, True
                except Exception:
                    pass
                raise
            try:
                os.close(self.fd)
                self.closed = True
                receipt['closed'] = True
            except Exception as error:
                receipt['errors'].append(error_value('sink-close', error))
        return receipt


class Owner:
    def __init__(self, command, cwd, env, outputdir, outer_deadline_ns):
        self.command, self.cwd, self.env = command, cwd, env
        self.directory, self.outer_deadline = Path(outputdir), outer_deadline_ns
        self.sinks, self.close_receipts = {}, {}
        self.selector, self.child, self.census_process = None, None, None
        self.ps_handles = []
        self.first_error, self.later_errors = None, []
        self.omitted_error_count, self.error_journal_unavailable = 0, False
        self.received_signals, self.signal_overflow = [], 0
        self.old_handlers = {}
        self.launched, self.deadline, self.child_reaped_at = None, None, None
        self.collection_end = None
        self.returncode, self.ownership = None, None
        self.live_samples, self.peak, self.samples = 0, 0, 0
        self.terminal_empty, self.terminal_sample = False, None
        self.streams = {n: {'observed_bytes': 0, 'eof': False, 'complete': True,
                            'overflow_first_byte_b64': None} for n in ('stdout', 'stderr')}
        self.pipe_objects = {}
        self.ps_buffers, self.ps_eof, self.ps_limit = {}, {}, 0
        self.stopping = False
        self.hard_abort_attempted = False

    def remember_error(self, item):
        if self.first_error is None:
            self.first_error = item
        elif len(self.later_errors) < MAX_LATER_ERRORS:
            self.later_errors.append(item)
        else:
            self.omitted_error_count += 1

    def failure(self, phase, error):
        item = error if type(error) is dict else error_value(phase, error)
        self.remember_error(item)
        sink = self.sinks.get('errors')
        if sink is not None and not sink.closed and not self.error_journal_unavailable:
            try:
                sink.append(canonical(item), durable=True)
            except Exception as failed:
                # Do not recurse into the failed error sink. The root preserves
                # this returned error independently of local storage success.
                self.error_journal_unavailable = True
                self.remember_error(error_value('error-journal-write', failed))

    def event(self, value):
        value = dict(value, monotonic_ns=time.monotonic_ns())
        self.sinks['events'].append(canonical(value), durable=True)

    def signal_received(self, signum, frame):
        if len(self.received_signals) < 1024:
            self.received_signals.append({'signal': signum,
                                         'monotonic_ns': time.monotonic_ns(),
                                         'stopping': self.stopping})
        else:
            self.signal_overflow += 1

    def poll_child(self):
        if self.child is not None:
            value = self.child.poll()  # waitpid WNOHANG, not an unbounded wait.
            if value is not None and self.returncode is None:
                self.returncode, self.child_reaped_at = value, time.monotonic_ns()
                self.event({'event': 'child_reaped', 'pid': self.child.pid,
                            'returncode': value})
        return self.returncode

    def register_pipe(self, stream, kind, name):
        os.set_blocking(stream.fileno(), False)
        self.selector.register(stream, selectors.EVENT_READ, (kind, name))
        self.pipe_objects[(kind, name)] = stream

    def close_pipe(self, kind, name):
        stream = self.pipe_objects.pop((kind, name), None)
        if stream is None:
            return
        try:
            self.selector.unregister(stream)
        except Exception as error:
            self.failure('pipe-unregister-'+kind+'-'+name, error)
        try:
            stream.close()
        except Exception as error:
            self.failure('pipe-close-'+kind+'-'+name, error)

    def pump(self, timeout):
        if not self.stopping and (self.received_signals or self.signal_overflow):
            raise CollectionFailure('catchable interruption ends active stream/census work')
        if self.deadline is not None and time.monotonic_ns() >= self.deadline:
            raise CollectionFailure('original process/outer deadline exhausted before selector wait')
        for key, _ in self.selector.select(max(0.0, min(timeout, 0.05))):
            kind, name = key.data
            if kind == 'child':
                state, sink = self.streams[name], self.sinks[name]
                amount = min(65536, LIMITS['output_bytes']-state['observed_bytes']+1)
            else:
                amount = min(65536, self.ps_limit-sum(map(len, self.ps_buffers.values()))+1)
            try:
                data = os.read(key.fd, max(1, amount))
            except BlockingIOError:
                continue
            except Exception:
                if kind == 'child':
                    self.streams[name]['complete'] = False
                self.close_pipe(kind, name)
                raise
            if not data:
                if kind == 'child':
                    self.streams[name]['eof'] = True
                else:
                    self.ps_eof[name] = True
                self.close_pipe(kind, name)
                continue
            if kind == 'child':
                state['observed_bytes'] += len(data)
                room = LIMITS['output_bytes']-sink.written
                try:
                    sink.append(data[:room])
                except Exception:
                    state['complete'] = False
                    self.close_pipe(kind, name)
                    raise
                if len(data) > room:
                    state['complete'] = False
                    state['overflow_first_byte_b64'] = base64.b64encode(data[room:room+1]).decode('ascii')
                    self.close_pipe(kind, name)
                    raise CollectionFailure(name+' exceeded independent 8-MiB capture ceiling')
            else:
                room = self.ps_limit-sum(map(len, self.ps_buffers.values()))
                self.ps_buffers[name].extend(data[:room])
                if len(data) > room:
                    self.close_pipe(kind, name)
                    raise CollectionFailure('census raw metadata capacity exceeded; partial bytes retained')

    def kill(self, process, label):
        result = {'event': 'termination', 'label': label, 'pid': process.pid,
                  'pgid': process.pid, 'signal': int(signal.SIGKILL), 'attempts': []}
        for name, action in (('owned_group', lambda: os.killpg(process.pid, signal.SIGKILL)),
                             ('leader', process.kill)):
            try:
                action()
                result['attempts'].append({'target': name, 'outcome': 'signal_sent'})
            except ProcessLookupError:
                result['attempts'].append({'target': name, 'outcome': 'already_absent'})
            except Exception as error:
                result['attempts'].append({'target': name, 'outcome': 'error',
                                           'error': error_value('termination', error)})
                self.failure('terminate-'+label+'-'+name, error)
        try:
            self.event(result)
        except Exception as error:
            self.failure('termination-event', error)

    def census(self, deadline):
        begin = time.monotonic_ns()
        remaining = min(250000000, deadline-begin)
        if remaining <= 0:
            raise CollectionFailure('no remaining deadline for required census')
        end = begin+remaining
        # Reserve up to 50ms inside the 250ms census budget for helper kill/reap.
        running_end = end-min(50000000, remaining//2)
        event = {'event': 'census', 'index': self.samples+1, 'argv': PS_ARGV,
                 'begin_ns': begin, 'deadline_ns': end, 'effective_timeout_ns': remaining,
                 'child_poll_before': self.poll_child(), 'ps_pid': None,
                 'ps_returncode': None, 'ps_reaped': False, 'errors': []}
        self.samples += 1
        self.ps_buffers = {'stdout': bytearray(), 'stderr': bytearray()}
        self.ps_eof = {'stdout': False, 'stderr': False}
        # Reserve conservative room for base64, parsed row dictionaries and
        # framing within the journal's fixed quota, not just the raw bytes.
        # Capacity exhaustion is a refusal, never silent truncation.
        self.ps_limit = max(0, (self.sinks['events'].limit-self.sinks['events'].written-65536)//16)
        process, failure = None, None
        try:
            if self.ps_limit <= 0:
                raise CollectionFailure('no metadata capacity for census')
            if time.monotonic_ns() >= running_end:
                raise CollectionFailure('census preparation consumed its remaining deadline')
            if not self.stopping and (self.received_signals or self.signal_overflow):
                raise CollectionFailure('catchable interruption before census launch')
            process = subprocess.Popen(PS_ARGV, cwd=self.cwd, env=self.env,
                                       stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True,
                                       close_fds=True, shell=False)
            self.census_process = process
            self.ps_handles.append(process)
            event['ps_pid'] = process.pid
            for name in ('stdout', 'stderr'):
                self.register_pipe(getattr(process, name), 'ps', name)
            while True:
                code = process.poll()
                if code is not None and all(self.ps_eof.values()):
                    break
                if time.monotonic_ns() >= running_end:
                    raise CollectionFailure('required census timed out within bounded helper budget')
                self.pump(min(0.01, max(0, running_end-time.monotonic_ns())/NS))
            event['ps_returncode'], event['ps_reaped'] = code, True
            if code != 0 or self.ps_buffers['stderr']:
                raise CollectionFailure('ps failed or emitted stderr')
            rows, seen = [], set()
            for line in bytes(self.ps_buffers['stdout']).decode('ascii').splitlines():
                fields = line.split()
                if len(fields) != 3 or not all(field.isdecimal() for field in fields):
                    raise CollectionFailure('malformed ps sample')
                pid, group, rss = map(int, fields)
                if pid in seen:
                    raise CollectionFailure('duplicate ps pid')
                seen.add(pid)
                if pid == self.child.pid and group != self.child.pid:
                    raise CollectionFailure('owned child escaped its process group')
                if group == self.child.pid:
                    rows.append({'pid': pid, 'pgid': group, 'rss_kib': rss})
            after = self.poll_child()
            leader = next((row for row in rows if row['pid'] == self.child.pid), None)
            if leader is None and after is None:
                raise CollectionFailure('live owned child missing from ps sample')
            total = sum(row['rss_kib'] for row in rows)*1024
            live = event['child_poll_before'] is None and leader is not None and leader['rss_kib'] > 0
            terminal = event['child_poll_before'] is not None and not rows
            event.update(owned_rows=rows, owned_rss_bytes=total, child_poll_after=after,
                         live_leader_sample=live, terminal_empty=terminal)
            self.peak = max(self.peak, total)
            if live:
                self.live_samples += 1
            if terminal:
                self.terminal_empty, self.terminal_sample = True, self.samples
            if total > LIMITS['rss_bytes']:
                raise CollectionFailure('512-MiB sampled owned-group RSS ceiling exceeded')
            if event['child_poll_before'] is not None and rows:
                raise CollectionFailure('owned process group survived reaped leader')
        except Exception as error:
            failure = error
            event['errors'].append(error_value('census', error))
            self.failure('census', error)  # Retain first cause before cleanup failures.
        finally:
            if hard_abort_active():
                abort_owned(self, process)
                raise
            if process is not None:
                if process.poll() is None or not all(self.ps_eof.values()):
                    self.kill(process, 'census-helper')
                    while time.monotonic_ns() < end:
                        if process.poll() is not None and all(self.ps_eof.values()):
                            break
                        try:
                            self.pump(min(0.005, max(0, end-time.monotonic_ns())/NS))
                        except Exception as error:
                            event['errors'].append(error_value('census-tail-pump', error))
                            self.failure('census-tail-pump', error)
                            break
                event['ps_returncode'] = process.poll()
                event['ps_reaped'] = event['ps_returncode'] is not None
                if not event['ps_reaped']:
                    error = CollectionFailure('census helper not reaped within its deadline')
                    event['errors'].append(error_value('census-reap', error))
                    self.failure('census-reap', error)
                    failure = failure or error
            for name in ('stdout', 'stderr'):
                self.close_pipe('ps', name)
                if process is not None:
                    try:
                        stream = getattr(process, name)
                        if stream is not None and not stream.closed:
                            stream.close()
                    except Exception as error:
                        self.failure('unregistered-census-pipe-close-'+name, error)
                        event['errors'].append(error_value('census-pipe-close', error))
                        failure = failure or error
            event.update(end_ns=time.monotonic_ns(), stdout_b64=base64.b64encode(self.ps_buffers['stdout']).decode('ascii'),
                         stderr_b64=base64.b64encode(self.ps_buffers['stderr']).decode('ascii'),
                         stdout_eof=self.ps_eof['stdout'], stderr_eof=self.ps_eof['stderr'],
                         raw_capture_limit=self.ps_limit)
            self.census_process = None
            try:
                self.event(event)
                if time.monotonic_ns() > end:
                    raise CollectionFailure('census collection/persistence exceeded its bounded deadline')
            except Exception as error:
                self.failure('census-event-persistence', error)
                failure = failure or error
        if failure is not None:
            raise failure
        return event

    def drive(self):
        work_end = self.deadline-TAIL_NS
        next_sample = self.launched
        while True:
            now = time.monotonic_ns()
            if self.received_signals or self.signal_overflow:
                raise CollectionFailure('catchable interruption recorded during owned process')
            if self.first_error is not None:
                raise CollectionFailure('independent collection error recorded')
            if now >= work_end:
                raise CollectionFailure('bounded work deadline exhausted; two-second cleanup reserve retained')
            if now >= next_sample:
                self.census(work_end)
                next_sample = now+50000000
            if time.monotonic_ns() >= work_end:
                raise CollectionFailure('work deadline reached during census or stream collection')
            if self.poll_child() is not None and self.terminal_empty and all(x['eof'] for x in self.streams.values()):
                break
            self.pump(min(0.05, max(0, min(next_sample, work_end)-time.monotonic_ns())/NS))
        if not self.live_samples:
            raise CollectionFailure('no actual live-leader RSS sample; fast case is not qualified')
        if self.returncode != 0:
            raise CollectionFailure('owned child exited nonzero: '+str(self.returncode))

    def cleanup(self):
        self.stopping = True
        if self.child is None:
            return
        # Popen may have succeeded before an ownership/event/register failure.
        # Still attempt both original raw drains; no replacement child is made.
        for name in ('stdout', 'stderr'):
            stream = getattr(self.child, name)
            if (stream is not None and not stream.closed and
                    ('child', name) not in self.pipe_objects):
                try:
                    self.register_pipe(stream, 'child', name)
                except Exception as error:
                    self.streams[name]['complete'] = False
                    self.failure('cleanup-register-'+name, error)
        if self.first_error is not None or self.returncode is None or not self.terminal_empty:
            self.kill(self.child, 'dispatcher')
        # Earlier body failure receives at most the reserved two-second tail;
        # late failure receives only what remains inside the original120s.
        end = min(self.deadline, time.monotonic_ns()+TAIL_NS)
        next_census, remaining_censuses = 0, 8
        while time.monotonic_ns() < end:
            try:
                self.poll_child()
                if (not self.terminal_empty and remaining_censuses and
                        time.monotonic_ns() >= next_census and
                        end-time.monotonic_ns() > 1000000):
                    remaining_censuses -= 1
                    next_census = time.monotonic_ns()+50000000
                    self.census(end)
                if self.returncode is not None and self.terminal_empty and all(x['eof'] for x in self.streams.values()):
                    break
                self.pump(min(0.01, max(0, end-time.monotonic_ns())/NS))
            except Exception as error:
                self.failure('independent-cleanup', error)
                self.kill(self.child, 'dispatcher-cleanup')
                # No relaunch or held-child handshake. These are cleanup-only
                # bounded observations of the original owned group.
                # A faulty selector/census is not retried in a CPU-speed loop.
                # The independent reap/helper/close attempts below still run.
                break
        try:
            self.poll_child()
        except Exception as error:
            self.failure('final-child-reap', error)
        if self.returncode is None:
            self.kill(self.child, 'dispatcher-final-deadline')
            self.failure('child-reap', CollectionFailure('owned child not reaped within deadline'))
        if not self.terminal_empty:
            self.failure('terminal-group', CollectionFailure('no successful empty-group census after child reap'))
        for process in self.ps_handles:
            try:
                code = process.poll()
                if code is None:
                    self.kill(process, 'unreaped-census-helper')
                    self.failure('helper-reap', CollectionFailure('census helper remains unreaped'))
                self.event({'event': 'final_helper_reap', 'pid': process.pid,
                            'returncode': code, 'reaped': code is not None})
            except Exception as error:
                self.failure('final-helper-reap', error)
        for name, state in self.streams.items():
            if not state['eof']:
                state['complete'] = False
                self.failure('stream-eof-'+name, CollectionFailure('stream EOF not observed before close'))

    def close_sink(self, name):
        sink = self.sinks.get(name)
        if sink is None:
            self.close_receipts[name] = {'attempted': False, 'reason': 'sink never opened'}
            return
        receipt = sink.close()
        self.close_receipts[name] = receipt
        for item in receipt['errors']:
            self.failure('sink-close-'+name, item)

    def save(self, name, value):
        sink, receipt = None, {'path': str(self.directory/name), 'identity': None, 'errors': []}
        try:
            raw = canonical(value)
            if len(raw) > FINAL_LIMIT:
                raise CollectionFailure('final receipt exceeds reserved metadata capacity')
            sink = Sink(self.directory/name, FINAL_LIMIT)
            sink.append(raw, durable=True)
        except Exception as error:
            receipt['errors'].append(error_value('exclusive-receipt-write', error))
        finally:
            if hard_abort_active():
                if sink is not None and sink.fd is not None and not sink.closed:
                    try:
                        os.close(sink.fd)
                        sink.fd, sink.closed = None, True
                    except Exception:
                        pass
                abort_owned(self)
                raise
            if sink is not None:
                closed = sink.close()
                receipt['identity'] = closed['identity']
                receipt['close'] = closed
                receipt['errors'].extend(closed['errors'])
            try:
                directory_sync(self.directory)
                receipt['directory_fsync_ok'] = True
            except Exception as error:
                receipt['directory_fsync_ok'] = False
                receipt['errors'].append(error_value('receipt-directory-fsync', error))
        for item in receipt['errors']:
            self.failure('receipt-'+name, item)
        return receipt

    def success(self):
        return (self.child is not None and self.first_error is None and not self.later_errors
                and not self.omitted_error_count and not self.error_journal_unavailable
                and not self.received_signals and not self.signal_overflow
                and self.returncode == 0 and self.live_samples > 0 and self.terminal_empty
                and all(s['eof'] and s['complete'] for s in self.streams.values())
                and self.peak <= LIMITS['rss_bytes'] and self.collection_end is not None
                and self.deadline is not None and self.collection_end <= self.deadline)


def run_child(command, cwd, env, outputdir, *, outer_deadline_ns):
    """Collect one genuinely owned child; return evidence, never tool authority.

    Precondition refusal raises before ownership. After setup begins, independent
    errors are retained through cleanup and returned even if a local receipt
    cannot be written. The external root must preserve this return/raw failure.
    """
    global USED
    if USED:
        raise CollectionFailure('one run_child call per fresh authenticated launcher process')
    USED = True
    if (sys.platform != 'darwin' or type(command) is not list or not command
            or any(type(x) is not str or not x or '\x00' in x for x in command)
            or not os.path.isabs(command[0]) or type(cwd) is not str
            or type(outputdir) is not str or type(env) is not dict or env != ENV
            or type(outer_deadline_ns) is not int
            or outer_deadline_ns-time.monotonic_ns() <= TAIL_NS):
        raise CollectionFailure('invalid exact process arguments, host, environment or remaining deadline')
    for path in (cwd, outputdir):
        if not os.path.isabs(path) or os.path.normpath(path) != path or os.path.realpath(path) != path:
            raise CollectionFailure('noncanonical cwd/output directory')
        prefix = Path('/')
        for part in Path(path).parts[1:]:
            prefix /= part
            if stat.S_ISLNK(os.lstat(prefix).st_mode):
                raise CollectionFailure('symlink directory component')
        if not stat.S_ISDIR(os.lstat(path).st_mode):
            raise CollectionFailure('cwd/output is not an existing directory')
    owner = Owner(list(command), cwd, dict(env), outputdir, outer_deadline_ns)
    try:
        report, report_file, close_receipt = None, None, None
        try:
            owner.sinks['errors'] = Sink(Path(outputdir)/'process-errors.jsonl', ERROR_LIMIT)
            owner.sinks['events'] = Sink(Path(outputdir)/'process-events.jsonl', LIMITS['auxiliary_metadata_bytes']-META_RESERVE)
            for name in ('stdout', 'stderr'):
                owner.sinks[name] = Sink(Path(outputdir)/(name+'.log'), LIMITS['output_bytes'])
            directory_sync(outputdir)
            owner.selector = selectors.DefaultSelector()
            for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
                owner.old_handlers[signum] = signal.getsignal(signum)
                signal.signal(signum, owner.signal_received)
            if owner.received_signals or owner.signal_overflow:
                raise CollectionFailure('catchable interruption before dispatcher launch')
            if outer_deadline_ns-time.monotonic_ns() <= TAIL_NS:
                raise CollectionFailure('setup exhausted remaining outer process budget')
            owner.launched = time.monotonic_ns()
            owner.deadline = min(owner.launched+120*NS, outer_deadline_ns)
            owner.child = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                           start_new_session=True, close_fds=True, shell=False)
            owner.ownership = {'pid': owner.child.pid, 'observed_pgid': None,
                               'start_new_session': True, 'observed_ns': None}
            actual_pgid = os.getpgid(owner.child.pid)
            owner.ownership.update(observed_pgid=actual_pgid, observed_ns=time.monotonic_ns())
            owner.event({'event': 'launch', 'ownership': owner.ownership,
                         'argv': command, 'cwd': cwd, 'environment': env,
                         'launched_ns': owner.launched, 'deadline_ns': owner.deadline})
            if actual_pgid != owner.child.pid:
                raise CollectionFailure('fresh child did not establish its owned leader process group')
            for name in ('stdout', 'stderr'):
                owner.register_pipe(getattr(owner.child, name), 'child', name)
            owner.drive()
        except Exception as error:
            owner.failure('owned-body', error)
        finally:
            if hard_abort_active():
                abort_owned(owner)
                raise
            try:
                owner.cleanup()
            except Exception as error:
                owner.failure('cleanup-tail', error)
                if owner.child is not None:
                    owner.kill(owner.child, 'independent-finally')
            for kind, name in tuple(owner.pipe_objects):
                owner.close_pipe(kind, name)
            # Also attempt pipe closes when failure preceded selector registration.
            if owner.child is not None:
                for name in ('stdout', 'stderr'):
                    try:
                        stream = getattr(owner.child, name)
                        if stream is not None and not stream.closed:
                            stream.close()
                    except Exception as error:
                        owner.failure('unregistered-child-pipe-close-'+name, error)
            if owner.selector is not None:
                try:
                    owner.selector.close()
                except Exception as error:
                    owner.failure('selector-close', error)
            for name in ('stdout', 'stderr', 'events'):
                owner.close_sink(name)
            owner.collection_end = time.monotonic_ns()
            if owner.deadline is not None and owner.collection_end > owner.deadline:
                owner.failure('collection-deadline', CollectionFailure('raw capture/cleanup exceeded original process deadline'))
            report = {'schema': 'ri138-owned-process-report-v1',
                      'status': 'OBSERVATION_REQUIRES_FINAL_CLOSE_AND_EXTERNAL_ROOT_REVIEW',
                      'success_provisional': owner.success(), 'command': command,
                      'cwd': cwd, 'environment': env, 'limits': LIMITS,
                      'work_reserve_ns': TAIL_NS, 'launched_ns': owner.launched,
                      'deadline_ns': owner.deadline, 'child_reaped_at_ns': owner.child_reaped_at,
                      'collection_end_ns': owner.collection_end,
                      'ownership': owner.ownership, 'returncode': owner.returncode,
                      'live_leader_samples': owner.live_samples, 'census_attempts': owner.samples,
                      'peak_owned_rss_bytes': owner.peak, 'terminal_empty': owner.terminal_empty,
                      'terminal_sample': owner.terminal_sample, 'streams': owner.streams,
                      'first_error': owner.first_error, 'later_errors': list(owner.later_errors),
                      'omitted_error_count': owner.omitted_error_count,
                      'error_journal_unavailable': owner.error_journal_unavailable,
                      'received_signals': list(owner.received_signals),
                      'signal_overflow': owner.signal_overflow, 'sink_closes': dict(owner.close_receipts),
                      'outer_tool_origin_established': False, 'root_acceptance': False}
            report_file = owner.save('PROCESS_REPORT.json', report)
            owner.close_sink('errors')
            close_value = {'schema': 'ri138-owned-process-close-v1',
                           'success_so_far': owner.success(), 'report_write': report_file,
                           'sink_closes': dict(owner.close_receipts), 'first_error': owner.first_error,
                           'later_errors': list(owner.later_errors),
                           'omitted_error_count': owner.omitted_error_count,
                           'error_journal_unavailable': owner.error_journal_unavailable,
                           'received_signals': list(owner.received_signals),
                           'signal_overflow': owner.signal_overflow,
                           'own_final_close_requires_external_observation': True}
            close_receipt = owner.save('PROCESS_CLOSE.json', close_value)
            for signum, handler in owner.old_handlers.items():
                try:
                    signal.signal(signum, handler)
                except Exception as error:
                    owner.failure('signal-handler-restore', error)
        return {'schema': 'ri138-owned-process-return-v1',
                'status': 'COLLECTED_NOT_EXTERNALLY_ACCEPTED', 'success': owner.success(),
                'report': report, 'report_file': report_file, 'close_receipt': close_receipt,
                'files': {name: str(Path(outputdir)/name) for name in FILES},
                'first_error': owner.first_error, 'later_errors': list(owner.later_errors),
                'omitted_error_count': owner.omitted_error_count,
                'error_journal_unavailable': owner.error_journal_unavailable,
                'received_signals': list(owner.received_signals), 'signal_overflow': owner.signal_overflow,
                'outer_tool_origin_established': False, 'root_acceptance': False}
    finally:
        # Also covers a hard alarm arriving during ordinary finalization,
        # after the inner finally-entry guard has already been evaluated.
        if hard_abort_active():
            abort_owned(owner)
            raise
