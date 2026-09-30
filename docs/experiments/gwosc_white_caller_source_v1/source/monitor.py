"""RI130 retained RI121 monitor/reap source; UNEXECUTED on this target.

The function body below is the qualified RI121 loop with indentation only
changed for extraction. It samples one reviewed child, not a hard OS memory cap.
"""
import os
import signal
import subprocess
import time

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



def supervise(child, record, started):
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
