"""RI171 one-case fixture controller; source-only preparation, no native invocation.
Root authenticates this program/runtime and separately authorizes one exact request.
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import types


def load_protocol(path, digest):
    with open(path, 'rb') as f:
        raw = f.read(262145)
    if len(raw) > 262144 or hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError('driver request digest/cap')
    req = json.loads(raw)
    p = req['sources']['protocol']
    with open(p['path'], 'rb') as f:
        body = f.read(1048577)
    if len(body) != p['bytes'] or hashlib.sha256(body).hexdigest() != p['sha256']:
        raise ValueError('driver protocol pin')
    m = types.ModuleType('ri171_protocol')
    m.__file__ = p['path']
    exec(compile(body, p['path'], 'exec'), m.__dict__)
    return m


def main():
    if len(sys.argv) != 5 or sys.argv[1] != '--request' or sys.argv[3] != '--request-sha256':
        raise ValueError('fixed driver invocation')
    path, digest = sys.argv[2], sys.argv[4]
    P = load_protocol(path, digest)
    request, case, _, before = P.request(path, digest)
    P.need(sys.executable == P.VENDOR and sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'driver bootstrap')
    P.need(os.getcwd() == P.BASE and dict(os.environ) == P.ENV, 'driver environment/cwd')
    P.need(os.path.abspath(__file__) == request['sources']['driver']['path'], 'driver source selection')
    operation = request['operation']
    os.mkdir(operation, 0o700)  # exclusive; no retry/removal/reuse
    result = {'schema': 'ri171-one-case-collection-v1', 'case_id': case['id'], 'status': 'FAILED',
              'before': before, 'after': None, 'command': [P.VENDOR, '-I', '-S', '-B', request['sources']['worker']['path'], path, digest],
              'environment': P.ENV, 'cwd': P.BASE, 'worker_pid': None, 'worker_returncode': None,
              'worker_reaped': False, 'errors': [], 'body_tree': None,
              'subject_deadline_seconds': 315, 'controller_collection_timeout_seconds': 335,
              'new_subject_cleanup_budget': False, 'start_monotonic_ns': time.monotonic_ns()}
    handles, proc = {}, None
    def error(stage, exc):
        result['errors'].append({'stage': stage, 'type': type(exc).__name__, 'message': str(exc)})
    try:
        P.put(os.path.join(operation, 'REQUEST_CAPTURE.json'), request)
        for name in ('stdout', 'stderr'):
            handles[name] = open(os.path.join(operation, 'worker.'+name), 'xb', buffering=0)
        proc = subprocess.Popen(result['command'], stdin=subprocess.DEVNULL,
                                stdout=handles['stdout'], stderr=handles['stderr'],
                                env=P.ENV, cwd=P.BASE, close_fds=True, start_new_session=True)
        result['worker_pid'] = proc.pid
        try:
            result['worker_returncode'] = proc.wait(timeout=335)
            result['worker_reaped'] = True
        except subprocess.TimeoutExpired as exc:
            error('worker_collection_deadline', exc)
            # Do not claim subject/descendant cleanup; direct worker handle only.
            proc.kill()
            result['worker_returncode'] = proc.poll()
            result['worker_reaped'] = result['worker_returncode'] is not None
            result['external_recovery_required'] = True
        P.need(result['worker_returncode'] == 0 and result['worker_reaped'], 'worker genuine completion missing/nonzero')
    except BaseException as exc:
        error('collection', exc)
    finally:
        for name, f in handles.items():
            try:
                os.fsync(f.fileno())
            except BaseException as exc:
                error('fsync:'+name, exc)
            try:
                f.close()
            except BaseException as exc:
                error('close:'+name, exc)
            try:
                raw, pin, state = P.capture(os.path.join(operation, 'worker.'+name), 1048576)
                result['worker_'+name] = {'pin': pin, 'state': state}
                P.need(not raw, 'worker administrative stream nonempty')
            except BaseException as exc:
                error('readback:'+name, exc)
        try:
            after, failures = P.postcheck(request, path, digest)
            result['after'] = after
            result['errors'].extend({'stage':'complete_custody_tail/'+e['stage'],'type':e['type'],'message':e['message']} for e in failures)
            P.need(after == before, 'complete request/source custody changed')
        except BaseException as exc:
            error('source_request_tail', exc)
        value = None
        try:
            raw, pin, _ = P.capture(os.path.join(operation, 'CASE.json'), 33554432)
            result['case_report'] = pin
            value = P.decode(raw)
            P.need(value['case_id'] == case['id'] and not value['worker_errors'], 'case worker failed/selection changed')
        except BaseException as exc:
            error('case_report_tail', exc)
        try:
            _, pin, _ = P.capture(os.path.join(operation, 'TRACE.json'), 33554432)
            result['trace'] = pin
        except BaseException as exc:
            error('trace_tail', exc)
        try:
            result['body_tree'] = P.tree(os.path.join(operation, 'body'))
            P.need(value is not None and result['body_tree'] == value['body_tree'], 'post-exit complete body tree differs or earlier report unavailable')
        except BaseException as exc:
            error('complete_body_tail', exc)
        if not result['errors']:
            result['status'] = 'CAPTURED_FOR_INDEPENDENT_SAVED_REVIEW'
        result['end_before_final_record_monotonic_ns'] = time.monotonic_ns()
        # This write/close is covered only by genuine root outer completion, not the
        # saved pre-write timestamp or the child's self-reported success label.
        P.put(os.path.join(operation, 'COLLECTION.json'), result)
    return 0 if not result['errors'] else 2


if __name__ == '__main__':
    sys.exit(main())
