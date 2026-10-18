#!/usr/bin/env python3
"""RI132 future one-case direct-boundary runner; not execution permission.

No caller main/run is invoked and no accepted source or global is patched.
Root owns external bootstrap authentication, one-case admission, owned-group
monitoring, actual process completion and independent before/after custody.
All sources in this packet are unexecuted at author handoff.
"""

from hashlib import sha256
from pathlib import Path
import json
import os
import resource
import signal
import stat
import sys
import time
import types


Q = Path('/Volumes/AI_DATA/development/det-review-evidence/ri132-native-caller-qualification-source-0ZmB3R5I')
A = Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0')
SELF = Q/'qualify_callers.py'
PYTHON = Path('/opt/homebrew/bin/python3')
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'output_bytes': 8388608, 'auxiliary_metadata_bytes': 67108864}
CALLERS = {
    'native': (A/'supervise.py', 88890,
               '34707ca1bd6e245ca9ec469adeb4c3da8cf0ed303be945036708554073b39650'),
    'audit': (A/'launch_audit.py', 103287,
              '5263099d45d9ed021a80d65029da511ad9019d30892278b1b412cb1794465ae5'),
}
REQUIRED_SOURCE_FILES = ('qualify_callers.py', 'native_controls.py',
                         'audit_controls.py', 'entry_evidence.py')


class Refused(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Refused(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def exact(value, names, where):
    require(type(value) is dict and set(value) == set(names), where+' fields differ')


def digest_text(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def read_stable(path, cap=67108864):
    require(path.is_absolute() and os.path.normpath(str(path)) == str(path), 'noncanonical path')
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current/part
        require(not stat.S_ISLNK(current.lstat().st_mode), 'source/evidence path contains symlink')
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= cap, 'file size/type refused')
        blocks, count = [], 0
        while True:
            block = os.read(fd, min(1024*1024, cap+1-count))
            if not block:
                break
            count += len(block)
            require(count <= cap, 'file grew beyond read cap')
            blocks.append(block)
        after = os.fstat(fd)
        sig = lambda x: (x.st_dev, x.st_ino, x.st_mode, x.st_size, x.st_mtime_ns, x.st_ctime_ns)
        require(sig(before) == sig(after) and count == after.st_size, 'file changed during read')
    finally:
        os.close(fd)
    require(sig(path.lstat()) == sig(after), 'file replaced after read')
    raw = b''.join(blocks)
    return raw, {'path': str(path), 'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def read_json(path, expected=None):
    raw, identity = read_stable(path)
    if expected is not None:
        exact(expected, ('path', 'bytes', 'sha256'), 'metadata identity')
        require(canonical(identity) == canonical(expected), 'metadata bytes differ from admitted identity')
    def pairs(items):
        value = {}
        for key, item in items:
            require(key not in value, 'duplicate metadata key')
            value[key] = item
        return value
    def bad(_):
        raise Refused('noninteger metadata number refused')
    value = json.loads(raw, object_pairs_hook=pairs, parse_float=bad, parse_constant=bad)
    require(type(value) is dict, 'metadata root is not an object')
    return value, identity


def load_exact_module(path, expected, name):
    """Future execution of complete authenticated source, not edited slices.

    Compile exact bytes under a non-main name, avoiding ambient pyc suppliers.
    There is no name/path/global replacement in the accepted caller module.
    This function is not invoked during source preparation.
    """
    raw, identity = read_stable(path)
    require(canonical(identity) == canonical(expected), 'module differs from admitted source')
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ''
    code = compile(raw, str(path), 'exec', dont_inherit=True, optimize=0)
    exec(code, module.__dict__)
    return module, identity


def postchecks(protected):
    result = []
    for path, expected in protected.items():
        try:
            _, identity = read_stable(Path(path))
            result.append({'path': path, 'unchanged': canonical(identity) == canonical(expected),
                           'identity': identity})
        except BaseException as error:
            result.append({'path': path, 'unchanged': False,
                           'error_type': type(error).__name__, 'error': str(error)[:2048]})
    return result


def interrupted(signum, _frame):
    raise Refused('qualification interrupted by signal '+str(signum))


def execute_one(which, case_id, authorization_digest):
    protected, failure, result = {}, None, None
    started = time.monotonic_ns()
    try:
        require(sys.platform == 'darwin' and Path(__file__).absolute() == SELF, 'fixed runner/host differs')
        require(Path.cwd() == Q and dict(os.environ) == ENV, 'fixed cwd/environment differs')
        require(sys.flags.isolated == 1 and sys.flags.no_site == 1
                and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0,
                'fixed isolated normal interpreter flags required')
        require(sys.argv[0] == str(SELF), 'literal runner argv path differs')
        require(os.path.realpath(sys.executable) == os.path.realpath(PYTHON), 'fixed interpreter differs')
        require(which in CALLERS and type(case_id) is str and 0 < len(case_id) <= 100
                and all(c.isascii() and (c.isalnum() or c in '-_') for c in case_id), 'unknown caller/case syntax')
        require(digest_text(authorization_digest) and authorization_digest != '0'*64,
                'literal root one-case authorization hash required')
        auth_path = Q/'admissions'/(which+'-'+case_id+'.json')
        auth_raw, auth_id = read_stable(auth_path)
        protected[str(auth_path)] = auth_id
        require(auth_id['sha256'] == authorization_digest, 'root authorization digest differs')
        auth, _ = read_json(auth_path, auth_id)
        exact(auth, ('schema', 'status', 'caller', 'case_id', 'source_manifest', 'external_preflight',
                     'outer_argv_prefix', 'outer_cwd', 'outer_environment', 'limits', 'literal_dispatch_is_external',
                     'deferred_prerequisites_accepted', 'scientific_execution_authorized',
                     'retry_or_limit_relaxation_authorized'), 'root direct-case authorization')
        require(auth['schema'] == 'ri132-root-direct-case-authorization-v1'
                and auth['status'] == 'ADMIT_ONE_SPECIFIED_DIRECT_BOUNDARY_OBSERVATION'
                and auth['caller'] == which and auth['case_id'] == case_id
                and type(auth['deferred_prerequisites_accepted']) is bool
                and auth['scientific_execution_authorized'] is False
                and auth['retry_or_limit_relaxation_authorized'] is False, 'root direct-case scope differs')
        # The card must not contain a command carrying its own digest. Root
        # records/authenticates that literal dispatch separately after hashing.
        require(auth['outer_argv_prefix'] == [str(PYTHON), '-I', '-S', '-B', str(SELF), which, case_id]
                and auth['outer_cwd'] == str(Q)
                and canonical(auth['outer_environment']) == canonical(ENV)
                and canonical(auth['limits']) == canonical(LIMITS), 'root direct-case command/envelope differs')
        require(auth['literal_dispatch_is_external'] is True, 'external literal dispatch custody required')
        preflight_path = Q/'admissions'/(which+'-'+case_id+'.preflight.json')
        require(auth['external_preflight'].get('path') == str(preflight_path), 'fixed preflight path differs')
        preflight, preflight_id = read_json(preflight_path, auth['external_preflight'])
        protected[str(preflight_path)] = preflight_id
        require(preflight.get('schema') == 'ri132-root-external-direct-preflight-v1'
                and preflight.get('status') == 'ACCEPT_COMPLETE_EXTERNAL_BOOTSTRAP_AND_CASE_CUSTODY'
                and preflight.get('caller') == which and preflight.get('case_id') == case_id
                and preflight.get('all_runtime_files_match') is True
                and preflight.get('all_runtime_namespace_and_host_match') is True
                and preflight.get('all_source_history_dependencies_match') is True
                and preflight.get('independent_external_observation') is True
                and canonical(preflight.get('source_manifest')) == canonical(auth['source_manifest'])
                and type(preflight.get('evidence')) is dict and bool(preflight['evidence']),
                'complete external preflight not accepted; runner cannot establish bootstrap itself')
        require(auth['source_manifest'].get('path') == str(Q/'HANDOFF.json'), 'fixed source manifest differs')
        handoff, handoff_id = read_json(Q/'HANDOFF.json', auth['source_manifest'])
        protected[str(Q/'HANDOFF.json')] = handoff_id
        require(handoff.get('schema') == 'ri132-native-caller-qualification-source-handoff-v1'
                and handoff.get('status') == 'SOURCE_ONLY_SEALED_FOR_NONAUTHOR_REVIEW'
                and handoff.get('execution_authorized') is False
                and handoff.get('scientific_execution') is False
                and type(handoff.get('files')) is list, 'wrong sealed qualification source manifest')
        source_ids = {}
        for item in handoff['files']:
            exact(item, ('path', 'bytes', 'sha256'), 'sealed source identity')
            require(type(item['path']) is str and item['path'] not in source_ids, 'duplicate source identity')
            source_ids[item['path']] = item
        for name in REQUIRED_SOURCE_FILES:
            path = Q/name
            require(str(path) in source_ids, 'required source absent from admitted closure')
            _, identity = read_stable(path)
            require(canonical(identity) == canonical(source_ids[str(path)]), 'qualification source changed')
            protected[str(path)] = identity
        helper_path = Q/(which+'_controls.py')
        helper, helper_id = load_exact_module(helper_path, source_ids[str(helper_path)], 'ri132_'+which+'_controls')
        require(type(helper.CASES) is tuple, 'closed case catalogue must be a tuple')
        matches = [case for case in helper.CASES if case['id'] == case_id]
        require(len(matches) == 1, 'unknown or duplicate direct case')
        case = matches[0]
        if case.get('prerequisite_dependent') is True:
            require(auth['deferred_prerequisites_accepted'] is True, 'deferred genuine prerequisites not admitted')
        path, count, checksum = CALLERS[which]
        caller_id = {'path': str(path), 'bytes': count, 'sha256': checksum}
        protected[str(path)] = caller_id
        caller, _ = load_exact_module(path, caller_id, 'ri129_'+which+'_qualification_subject')
        observed = helper.run_case(caller, case_id)
        require(type(observed) is dict and observed.get('id') == case_id
                and observed.get('whole_entry') is False, 'unscoped direct observation refused')
        require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= LIMITS['rss_bytes'], 'self RSS ceiling exceeded')
        result = {'schema': 'ri132-direct-boundary-observation-v1',
                  'status': 'OBSERVED_DECLARED_BOUNDARY_ONLY', 'caller': which, 'case_id': case_id,
                  'expected': case['expected'], 'observation': observed,
                  'caller_source': caller_id, 'control_source': helper_id,
                  'source_manifest': handoff_id, 'root_authorization': auth_id,
                  'external_preflight': preflight_id, 'whole_entry': False,
                  'complete_caller_qualification': False, 'historical_acceptance_created': False,
                  'independent_outer_origin_and_custody_review_required': True,
                  'scientific_execution': False}
    except BaseException as error:
        failure = {'error_type': type(error).__name__, 'error': str(error)[:4096]}
    finally:
        final = postchecks(protected)
    elapsed = time.monotonic_ns()-started
    valid = failure is None and all(item['unchanged'] is True for item in final) and elapsed <= 120000000000
    envelope = {'result': result, 'error': failure, 'postchecks': final,
                'elapsed_ns': elapsed, 'qualified_as_complete': False}
    raw = (canonical(envelope)+'\n').encode('ascii')
    require(len(raw) <= LIMITS['output_bytes'], 'qualification output exceeds fixed cap')
    stream = sys.stdout.buffer if valid else sys.stderr.buffer
    stream.write(raw)
    stream.flush()
    return 0 if valid else 2


def main():
    require(len(sys.argv) == 4, 'require caller, case id and genuine root authorization digest')
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGALRM):
        signal.signal(signum, interrupted)
    signal.alarm(120)
    try:
        return execute_one(*sys.argv[1:])
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BaseException as error:
        if isinstance(error, SystemExit):
            raise
        print('RI132 QUALIFICATION REFUSAL: '+type(error).__name__+': '+str(error)[:4096], file=sys.stderr)
        sys.exit(2)
