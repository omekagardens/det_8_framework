"""RI167 repaired fixed RI161 outer supervisor, UNEXECUTED SOURCE pending root admission.

This program reports observed cleanup, never complete fork coverage or case
acceptance. Root authenticates this source, its runtime and the exact command
before Python startup, and independently reviews genuine tool completion and
all unchanged RI161 receipts afterwards. There is no automatic retry.
"""
import hashlib
import json
import os
import selectors
import signal
import stat
import subprocess
import sys
import time

BASE = '/Volumes/AI_DATA/development/det-review-evidence'
VENDOR = '/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9'
CALLER = BASE + '/ri161-grid-qualification-source-679wwadg/caller.py'
REQUEST = BASE + '/ri163-native-qualification-request-0f632c815ef94824b7a160deb809c4ae.json'
REQUEST_SHA = 'bfb5cf54ff83af72cb20fbb82e855ba98d4fd458738cef4c3fcd71de80de7749'
PREFIX = BASE + '/ri163-native-qualification-outer-0f632c815ef94824b7a160deb809c4ae'
ARGV = [VENDOR, '-I', '-S', '-B', CALLER, '--request', REQUEST,
        '--request-sha256', REQUEST_SHA]
ENV = {'LANG': 'C', 'LC_ALL': 'C', 'PATH': '/usr/bin:/bin'}
PS = ['/bin/ps', '-axo', 'pid=,ppid=,pgid=,lstart=']
CAP = 8 * 1024 * 1024
JOURNAL_CAP = 64 * 1024 * 1024
PS_CAP = 262144
RECEIPT_CAP = 262144
OUTER_SECONDS, TERM_SECONDS, KILL_SECONDS = 315, 310, 312
PS_SECONDS, PS_CLEANUP_SECONDS, SCAN_PERIOD = 0.2, 0.2, 0.5
NS = 1000000000


class Refusal(Exception):
    pass


class HardStop(BaseException):
    pass


def need(value, message):
    if not value:
        raise Refusal(message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'),
                       ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')


def error(errors, stage, exc):
    if len(errors) < 32:
        errors.append({'stage': stage, 'type': type(exc).__name__, 'message': str(exc)[:240]})
    elif len(errors) == 32:
        errors.append({'stage': 'error_overflow', 'type': 'Refusal',
                       'message': 'Further errors omitted; acceptance is impossible.'})


def write_all(fd, raw):
    view = memoryview(raw)
    while view:
        n = os.write(fd, view)
        need(n > 0, 'short output write')
        view = view[n:]


def new_file(path):
    return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)


def sync_base():
    fd = os.open(BASE, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def readback(path, maximum):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'capture is not private regular file')
        need(0 <= before.st_size <= maximum, 'capture exceeds bound')
        digest, count = hashlib.sha256(), 0
        while True:
            chunk = os.read(fd, min(65536, maximum + 1 - count))
            if not chunk:
                break
            count += len(chunk)
            need(count <= maximum, 'capture grew beyond bound')
            digest.update(chunk)
        after = os.fstat(fd)
        signature = lambda st: (st.st_dev, st.st_ino, st.st_mode, st.st_nlink,
                                st.st_size, st.st_mtime_ns, st.st_ctime_ns)
        need(signature(before) == signature(after) == signature(os.lstat(path)), 'capture changed during readback')
        return {'path': path, 'bytes': count, 'sha256': digest.hexdigest(),
                'state': list(signature(after))}
    finally:
        os.close(fd)


def clear_child_timer():
    # This supervisor creates no threads. Do not import modules in preexec_fn.
    signal.setitimer(signal.ITIMER_REAL, 0.0)


def hard_stop(number, _frame):
    raise HardStop('outer signal ' + str(number))


def stop_pipe(name, pipes, active, closed, selector, issue):
    """Disable one pump; ownership survives failed registration/unregister/close."""
    if name in closed:
        return
    was_active = name in active
    active.discard(name)
    pipe = pipes[name]
    if selector is not None:
        try:
            selector.unregister(pipe)
        except KeyError as exc:
            if was_active:
                issue('unregister:' + name, exc)
        except Exception as exc:
            issue('unregister:' + name, exc)
    if name not in closed:
        try:
            pipe.close()
            closed.add(name)
        except Exception as exc:
            issue('pipe_close:' + name, exc)


def readable_names(selector, active, failed, deadline, interval, issue):
    if not active:
        return []
    if not failed:
        try:
            return [key.data for key, _ in selector.select(
                min(interval, max(0, (deadline - time.monotonic_ns()) / NS)))
                if key.data in active]
        except Exception as exc:
            issue('select', exc)
    # Ordinary failure never makes sibling drain depend on the damaged selector.
    time.sleep(min(0.005, max(0, (deadline - time.monotonic_ns()) / NS)))
    return sorted(active)


def process_snapshot(deadline, journal):
    """Bounded ps with independent healthy-stream drain after ordinary failure."""
    start = time.monotonic_ns()
    work_end = min(deadline, start + int(PS_SECONDS * NS))
    finish_end = min(deadline, work_end + int(PS_CLEANUP_SECONDS * NS))
    p, sel, buf, issues = None, None, {'stdout': bytearray(), 'stderr': bytearray()}, []
    rec = {'command': PS, 'start_monotonic_ns': start, 'pid': None, 'returncode': None,
           'reaped': False, 'eof': {'stdout': False, 'stderr': False}, 'overflow': {}}
    hard, rows = False, None
    pipes, active, closed = {}, set(), set()

    def issue(stage, exc):
        issues.append('ps ' + stage + ': ' + type(exc).__name__ + ': ' + str(exc)[:200])

    def drain(failed):
        for name in readable_names(sel, active, failed, finish_end, 0.01, issue):
            try:
                chunk = os.read(pipes[name].fileno(), min(65536, PS_CAP + 1 - len(buf[name])))
                if not chunk:
                    rec['eof'][name] = True
                    stop_pipe(name, pipes, active, closed, sel, issue)
                else:
                    buf[name].extend(chunk)
                    if len(buf[name]) > PS_CAP:
                        rec['overflow'][name] = buf[name][-1]
                        issues.append('ps ' + name + ' cap')
                        stop_pipe(name, pipes, active, closed, sel, issue)
            except BlockingIOError:
                continue
            except Exception as exc:
                issue('pump:' + name, exc)
                stop_pipe(name, pipes, active, closed, sel, issue)

    try:
        sel = selectors.DefaultSelector()
        p = subprocess.Popen(PS, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=ENV, cwd=BASE,
                             start_new_session=True, close_fds=True, preexec_fn=clear_child_timer)
        rec['pid'] = p.pid
        # Retain BOTH Popen handles before either registration can fail.
        pipes = {name: getattr(p, name) for name in buf}
        for name, pipe in pipes.items():
            try:
                os.set_blocking(pipe.fileno(), False)
                sel.register(pipe, selectors.EVENT_READ, name)
                active.add(name)
            except Exception as exc:
                issue('register:' + name, exc)
                stop_pipe(name, pipes, active, closed, sel, issue)
        while True:
            now = time.monotonic_ns()
            if now >= work_end or issues:
                if now >= work_end and not issues:
                    issues.append('ps work deadline')
                if p.returncode is None:
                    try:
                        os.killpg(p.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    except Exception as exc:
                        issue('kill', exc)
            code = p.poll()
            if code is not None:
                rec.update(returncode=code, reaped=True)
            if rec['reaped'] and not active:
                break
            need(now < finish_end, 'ps cleanup deadline')
            drain(bool(issues))
        need(not issues and rec['returncode'] == 0 and not buf['stderr'], 'ps observation failed')
        rows = {}
        for line in bytes(buf['stdout']).decode('ascii').splitlines():
            fields = line.split()
            need(len(fields) == 8 and all(x.isdigit() for x in fields[:3]), 'ps row shape')
            pid, ppid, pgid = (int(x) for x in fields[:3])
            need(pid > 0 and ppid >= 0 and pgid >= 0 and pid not in rows, 'ps identifiers')
            rows[pid] = {'pid': pid, 'ppid': ppid, 'pgid': pgid, 'birth': ' '.join(fields[3:])}
        need(rows, 'ps empty table')
    except Exception as exc:
        issues.append(type(exc).__name__ + ': ' + str(exc)[:200])
    except BaseException:
        hard = True
        raise
    finally:
        if p is not None and p.returncode is None:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            except Exception as exc:
                if not hard:
                    issues.append('ps kill: ' + str(exc)[:200])
        if p is not None and not hard:
            # Reap and healthy sibling drain share the original observer deadline.
            poll_unavailable = False
            while time.monotonic_ns() < finish_end:
                if not poll_unavailable:
                    try:
                        code = p.poll()
                        if code is not None:
                            rec.update(returncode=code, reaped=True)
                    except Exception as exc:
                        issue('reap', exc)
                        poll_unavailable = True
                drain(True)
                if not active and (rec['reaped'] or poll_unavailable):
                    break
                time.sleep(min(0.005, max(0, (finish_end - time.monotonic_ns()) / NS)))
        for name in pipes:
            if hard:
                try:
                    pipes[name].close()
                except Exception:
                    pass
            else:
                stop_pipe(name, pipes, active, closed, sel, issue)
        if sel is not None:
            try:
                sel.close()
            except Exception as exc:
                if not hard:
                    issue('selector_close', exc)
        if not hard:
            if not rec['reaped'] or not all(rec['eof'].values()):
                issues.append('observer tail incomplete')
            rec.update(end_monotonic_ns=time.monotonic_ns(), errors=list(issues),
                       stdout_hex=bytes(buf['stdout']).hex(), stderr_hex=bytes(buf['stderr']).hex())
            try:
                journal(rec)
            except Exception as exc:
                issues.append('ps journal: ' + str(exc)[:200])
    need(not issues and rows is not None, '; '.join(issues))
    return rows


def discover(table, caller_pid, known):
    """Only observed ancestry is claimed. Birth strings have one-second precision."""
    for pid, old in known.items():
        if pid in table:
            need(table[pid]['birth'] == old['birth'] and table[pid]['pgid'] == old['pgid'],
                 'observed PID identity/group changed')
    live = {pid for pid in known if pid in table}
    if not known:
        need(caller_pid in table and table[caller_pid]['pgid'] == caller_pid,
             'caller identity was not observed as owned leader')
        known[caller_pid] = dict(table[caller_pid])
        live.add(caller_pid)
    changed = True
    while changed:
        changed = False
        for pid, row in table.items():
            if pid not in known and row['ppid'] in live:
                need(len(known) < 64, 'observed descendant count cap')
                known[pid] = dict(row)
                live.add(pid)
                changed = True
    return live


def signal_observed(table, known, number):
    """No claim of atomic PID lifetime. Never signal a mismatched saved identity."""
    groups, failures = set(), []
    for pid, old in known.items():
        now = table.get(pid)
        if now is not None:
            if now['birth'] != old['birth'] or now['pgid'] != old['pgid'] or now['pgid'] <= 1:
                failures.append('signal identity/group mismatch for ' + str(pid))
                continue
            groups.add(now['pgid'])
    for pgid in sorted(groups):
        # All current members must match observed ancestry before group signalling.
        members = [row for row in table.values() if row['pgid'] == pgid]
        if not all(row['pid'] in known and row['birth'] == known[row['pid']]['birth']
                   and row['pgid'] == known[row['pid']]['pgid'] for row in members):
            failures.append('group contains unverified process: ' + str(pgid))
            continue
        try:
            os.killpg(pgid, number)
        except ProcessLookupError:
            pass
        except Exception as exc:
            failures.append('signal group ' + str(pgid) + ': ' + type(exc).__name__)
    need(not failures, '; '.join(failures))


def supervise():
    need(sys.argv == [os.path.abspath(__file__)], 'fixed invocation takes no arguments')
    need(sys.executable == VENDOR and sys.flags.isolated == 1 and sys.flags.no_site == 1
         and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'supervisor bootstrap flags/path')
    need(dict(os.environ) == ENV and os.getcwd() == BASE, 'supervisor environment/cwd')
    need(os.path.realpath(BASE) == BASE and not os.path.islink(BASE), 'base path alias')
    need(signal.getitimer(signal.ITIMER_REAL) == (0.0, 0.0), 'existing supervisor timer')
    start = time.monotonic_ns()
    deadline = start + OUTER_SECONDS * NS
    term_at, kill_at = start + TERM_SECONDS * NS, start + KILL_SECONDS * NS
    errors, known, table = [], {}, {}
    process, selector, hard = None, None, False
    fds, pipes, counts, digests, streams = {}, {}, {}, {}, {}
    active, closed = set(), set()
    receipt = {'schema': 'ri165-observed-outer-completion-v1', 'status': 'FAILED',
               'command': ARGV, 'environment': ENV, 'cwd': BASE,
               'start_monotonic_ns': start, 'deadline_monotonic_ns': deadline,
               'caller_pid': None, 'caller_reaped': False, 'caller_returncode': None,
               'observed_cleanup': False, 'complete_fork_coverage': False,
               'scientific_acceptance': False, 'errors': errors}
    handlers = {n: signal.getsignal(n) for n in (signal.SIGALRM, signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
    for n in handlers:
        signal.signal(n, hard_stop)
    signal.setitimer(signal.ITIMER_REAL, OUTER_SECONDS)

    def journal(value):
        raw = canonical(value)
        need(counts['processes'] + len(raw) <= JOURNAL_CAP, 'process journal cap')
        write_all(fds['processes'], raw)
        counts['processes'] += len(raw)
        digests['processes'].update(raw)

    def pump_issue(stage, exc):
        error(errors, stage, exc)

    def drain(failed):
        for name in readable_names(selector, active, failed, deadline, 0.05, pump_issue):
            try:
                read_fd = pipes[name].fileno()
                try:
                    chunk = os.read(read_fd, min(65536, CAP + 1 - counts[name]))
                except BlockingIOError:
                    continue
                if not chunk:
                    streams[name]['eof'] = True
                    stop_pipe(name, pipes, active, closed, selector, pump_issue)
                    continue
                room = CAP - counts[name]
                kept = chunk[:room]
                write_all(fds[name], kept)
                counts[name] += len(kept)
                digests[name].update(kept)
                if len(chunk) > room:
                    streams[name]['overflow_byte'] = chunk[room]
                    error(errors, 'capture:' + name, Refusal('8 MiB outer stream cap'))
                    stop_pipe(name, pipes, active, closed, selector, pump_issue)
            except Exception as exc:
                error(errors, 'pump:' + name, exc)
                stop_pipe(name, pipes, active, closed, selector, pump_issue)

    try:
        for name, suffix in (('stdout', '.stdout'), ('stderr', '.stderr'), ('processes', '.processes.jsonl')):
            path = PREFIX + suffix
            fds[name] = new_file(path)
            counts[name], digests[name] = 0, hashlib.sha256()
            streams[name] = {'path': path, 'eof': name == 'processes', 'overflow_byte': None,
                             'durable_close': False, 'readback': None}
        # Refuse a preexisting final receipt; exclusive creation is repeated at write.
        need(not os.path.lexists(PREFIX + '.completion.json'), 'completion already exists')
        sync_base()
        selector = selectors.DefaultSelector()
        process = subprocess.Popen(ARGV, cwd=BASE, env=ENV, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   start_new_session=True, close_fds=True, preexec_fn=clear_child_timer)
        receipt['caller_pid'] = process.pid
        # Acquisition is independent of successful registration for either pipe.
        pipes = {name: getattr(process, name) for name in ('stdout', 'stderr')}
        for name, pipe in pipes.items():
            try:
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
                active.add(name)
            except Exception as exc:
                error(errors, 'register:' + name, exc)
                stop_pipe(name, pipes, active, closed, selector, pump_issue)
        next_scan = 0
        while True:
            now = time.monotonic_ns()
            need(now < deadline, 'outer deadline')
            if now >= next_scan:
                table = process_snapshot(deadline, journal)
                live = discover(table, process.pid, known)
                next_scan = time.monotonic_ns() + int(SCAN_PERIOD * NS)
                if errors or now >= term_at:
                    if not errors:
                        error(errors, 'deadline', Refusal('310-second work cutoff'))
                    signal_observed(table, known, signal.SIGKILL if now >= kill_at else signal.SIGTERM)
            code = process.poll()
            if code is not None:
                receipt.update(caller_reaped=True, caller_returncode=code)
            if receipt['caller_reaped'] and not active:
                # A fresh complete observation after the actual wait, never stale live.
                table = process_snapshot(deadline, journal)
                live = discover(table, process.pid, known)
                remaining_groups = {row['pgid'] for row in known.values()}
                need(not live and not any(r['pgid'] in remaining_groups for r in table.values()),
                     'observed descendant/group remains after caller exit')
                receipt['observed_cleanup'] = True
                break
            drain(bool(errors))
            if errors:
                next_scan = 0
        need(receipt['caller_returncode'] == 0 and not errors, 'caller/outer failed')
        need(counts['stderr'] == 0, 'caller outer stderr nonempty')
    except Exception as exc:
        error(errors, 'supervision', exc)
    except BaseException:
        hard = True
        raise
    finally:
        if process is not None and not hard and (errors or not receipt['observed_cleanup']):
            # No new budget. Continue fresh observed-identity cleanup within original315s.
            while time.monotonic_ns() < deadline:
                try:
                    drain(True)
                    table = process_snapshot(deadline, journal)
                    try:
                        live = discover(table, process.pid, known)
                    except Exception as exc:
                        error(errors, 'cleanup_identity', exc)
                        live = {pid for pid in known if pid in table}
                    try:
                        signal_observed(table, known, signal.SIGKILL)
                    except Exception as exc:
                        error(errors, 'cleanup_signal', exc)
                    code = process.poll()
                    if code is not None:
                        receipt.update(caller_reaped=True, caller_returncode=code)
                    groups = {r['pgid'] for r in known.values()}
                    if known and receipt['caller_reaped'] and not live and not any(r['pgid'] in groups for r in table.values()):
                        receipt['observed_cleanup'] = True
                        break
                except Exception as exc:
                    error(errors, 'cleanup', exc)
                    break
        # This direct handle remains safe even when a failed observer/journal
        # prevents a fresh descendant snapshot. It never proves group cleanup.
        if process is not None and process.returncode is None and (hard or errors):
            try:
                process.kill()
            except Exception as exc:
                if not hard:
                    error(errors, 'direct_handle_kill', exc)
        if process is not None and not hard:
            # F02: owned waitpid does not depend on ps or its journal succeeding.
            # F01: independently readable siblings remain serviced during reap.
            poll_unavailable = False
            while time.monotonic_ns() < deadline:
                if not poll_unavailable:
                    try:
                        code = process.poll()
                        if code is not None:
                            receipt.update(caller_reaped=True, caller_returncode=code)
                    except Exception as exc:
                        error(errors, 'direct_handle_reap', exc)
                        poll_unavailable = True
                drain(True)
                if not active and (receipt['caller_reaped'] or poll_unavailable):
                    break
                time.sleep(min(0.005, max(0, (deadline - time.monotonic_ns()) / NS)))
            if not receipt['caller_reaped']:
                error(errors, 'direct_handle_reap', Refusal('owned caller reap incomplete within original deadline'))
        # Never signal escaped descendants from stale PIDs on hard abort.
        # Retain partials; no receipt, reap/cleanup credit or fresh recovery budget.
        for name, pipe in pipes.items():
            if hard:
                try:
                    pipe.close()
                except Exception:
                    pass
            else:
                stop_pipe(name, pipes, active, closed, selector, pump_issue)
        if selector is not None:
            try:
                selector.close()
            except Exception as exc:
                if not hard:
                    error(errors, 'selector_close', exc)
        for name, fd in fds.items():
            durable = not hard
            if not hard:
                try:
                    os.fsync(fd)
                except Exception as exc:
                    durable = False
                    error(errors, 'fsync:' + name, exc)
            final_fd_state = None
            if not hard:
                try:
                    st = os.fstat(fd)
                    final_fd_state = [st.st_dev, st.st_ino, st.st_mode, st.st_nlink,
                                      st.st_size, st.st_mtime_ns, st.st_ctime_ns]
                except Exception as exc:
                    durable = False
                    error(errors, 'fstat:' + name, exc)
            try:
                os.close(fd)
            except Exception as exc:
                durable = False
                if not hard:
                    error(errors, 'close:' + name, exc)
            if not hard:
                streams[name]['durable_close'] = durable
                try:
                    pin = readback(streams[name]['path'], JOURNAL_CAP if name == 'processes' else CAP)
                    streams[name]['readback'] = pin
                    need(pin['bytes'] == counts[name] and pin['sha256'] == digests[name].hexdigest()
                         and pin['state'] == final_fd_state,
                         'capture readback differs from drained bytes/final descriptor')
                except Exception as exc:
                    error(errors, 'readback:' + name, exc)
        if not hard:
            if not receipt['caller_reaped'] or not receipt['observed_cleanup']:
                error(errors, 'final_cleanup', Refusal('cleanup remains unverified'))
            if set(streams) != {'stdout', 'stderr', 'processes'} or not all(
                    s['eof'] and s['durable_close'] and s['readback'] is not None
                    and s['overflow_byte'] is None for s in streams.values()):
                error(errors, 'capture_tail', Refusal('capture tail incomplete'))
            receipt.update(streams=streams, observed_processes=list(known.values()),
                           end_before_receipt_monotonic_ns=time.monotonic_ns())
            if receipt['end_before_receipt_monotonic_ns'] >= deadline:
                error(errors, 'final_deadline', Refusal('outer tail exceeded315s'))
            receipt['status'] = 'CAPTURED_FOR_ROOT_REVIEW' if not errors else 'FAILED'
            raw = canonical(receipt)
            need(len(raw) <= RECEIPT_CAP, 'completion receipt cap')
            fd = new_file(PREFIX + '.completion.json')
            try:
                write_all(fd, raw)
                os.fsync(fd)
            finally:
                os.close(fd)
            sync_base()
            need(time.monotonic_ns() < deadline, 'completion durability exceeded315s')
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        for n, handler in handlers.items():
            signal.signal(n, handler)
    return 0 if not errors else 2


if __name__ == '__main__':
    sys.exit(supervise())
