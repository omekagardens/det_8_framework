"""RI171 inert process/observer payload; never a native caller. UNEXECUTED."""
import json
import os
import signal
import subprocess
import sys
import time

PATTERN = b'R' * 64  # literal synthetic payload; independently reconstructed by saved oracle
CAP = 8 * 1024 * 1024


def save(path, value):
    with open(path, 'xb') as f:
        f.write((json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii'))
        f.flush()
        os.fsync(f.fileno())


def emit(fd, n):
    block = (PATTERN * 1024)[:65536]
    while n:
        raw = block[:min(n, len(block))]
        view = memoryview(raw)
        while view:
            k = os.write(fd, view)
            if k <= 0:
                raise OSError('payload zero write')
            view = view[k:]
        n -= len(raw)


def observer(fault, directory):
    line = b'123 1 123 Wed Sep 30 00:00:00 2026\n'
    if fault in ('ps_real', 'ps_nonzero', 'ps_stderr', 'ps_timeout'):
        raw = line
    elif fault == 'ps_duplicate':
        raw = line + line
    elif fault == 'ps_malformed':
        raw = b'123 1 123 Wed Sep\n'
    elif fault == 'ps_nonascii':
        raw = b'\xff\n'
    elif fault == 'ps_empty':
        raw = b''
    elif fault == 'ps_overflow':
        raw = b'x' * 262145
    elif fault == 'ps_max':
        prefix, suffix = b'123 1 123 ', b' Sep 30 00:00:00 2026\n'
        raw = prefix + b'x' * (262144 - len(prefix) - len(suffix)) + suffix
    else:
        raw = line
    # Fault-isolation recipes use tiny ready buffers on both streams.
    if fault.startswith('S05.ps.') or fault.startswith('S10.ps.'):
        os.write(1, line)
        os.write(2, b'ps-inert-stderr\n')
        save(os.path.join(directory, 'OBSERVER_READY.json'), {'ready': True})
        time.sleep(0.05)
    else:
        if raw:
            view = memoryview(raw)
            while view:
                view = view[os.write(1, view):]
        if fault == 'ps_stderr':
            os.write(2, b'ps-inert-stderr\n')
        if fault == 'ps_timeout':
            time.sleep(2)
    return 9 if fault == 'ps_nonzero' else 0


def main():
    mode, fault, directory = sys.argv[1:]
    if mode == 'observer':
        return observer(fault, directory)
    if mode == 'leaf':
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        save(os.path.join(directory, 'LEAF.json'), {'pid': os.getpid(), 'ppid': os.getppid(), 'pgid': os.getpgrp()})
        while True:
            time.sleep(1)
    meta = {'pid': os.getpid(), 'ppid': os.getppid(), 'pgid': os.getpgrp(),
            'timer': list(signal.getitimer(signal.ITIMER_REAL)), 'environment': dict(os.environ),
            'executable': sys.executable, 'flags': {'isolated': sys.flags.isolated, 'no_site': sys.flags.no_site,
            'dont_write_bytecode': sys.flags.dont_write_bytecode, 'optimize': sys.flags.optimize}}
    save(os.path.join(directory, 'PAYLOAD_START.json'), meta)
    if fault in ('observed_descendant', 'fast_reparent'):
        child = subprocess.Popen([sys.executable, '-I', '-S', '-B', os.path.abspath(__file__), 'leaf', fault, directory],
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 start_new_session=True, close_fds=True, env=dict(os.environ))
        end = time.monotonic() + 2
        while not os.path.exists(os.path.join(directory, 'LEAF.json')):
            if time.monotonic() >= end:
                raise RuntimeError('leaf startup not observed')
            time.sleep(0.002)
        save(os.path.join(directory, 'READY.json'), {'ready': True, 'leaf': child.pid})
        if fault == 'fast_reparent':
            return 0
        while not os.path.exists(os.path.join(directory, 'DESCENDANT_OBSERVED.json')):
            time.sleep(0.002)
        return 0
    if fault.startswith('cap_'):
        save(os.path.join(directory, 'READY.json'), {'ready': True})
        if fault == 'cap_dual_excess':
            # Interleave both streams so both overflow predicates are reachable.
            for _ in range(CAP // 65536):
                emit(1, 65536)
                emit(2, 65536)
            os.write(1, PATTERN[:1])
            os.write(2, PATTERN[:1])
        else:
            stream = 1 if 'stdout' in fault else 2
            emit(stream, CAP + (1 if fault.endswith('excess') else 0))
    elif fault in ('real_cutoffs', 'real_expiry'):
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        save(os.path.join(directory, 'READY.json'), {'ready': True})
        while True:
            time.sleep(1)
    else:
        both = fault.startswith(('S04.', 'S05.fallback.', 'S05.caller.', 'S10.caller.', 'S10.journal.', 'S13.'))
        emit(1, 64)
        if both or fault == 'stderr':
            emit(2, 64)
        save(os.path.join(directory, 'READY.json'), {'ready': True})
    if fault.endswith('already_exited'):
        return 0
    time.sleep(1)
    return 7 if fault == 'nonzero' or fault.startswith('late_') else 0


if __name__ == '__main__':
    sys.exit(main())
