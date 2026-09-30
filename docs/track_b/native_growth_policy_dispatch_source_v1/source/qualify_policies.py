#!/usr/bin/env python3
"""RI136 version-bound one-case pure-policy dispatcher, source only.

Root owns external bootstrap authentication, real one-case admission, owned
process-group monitoring and complete source/runtime/evidence custody. This
script never calls production main/run or writes cards, copies or results.
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


BASE = Path('/Volumes/AI_DATA/development/det-review-evidence')
Q = BASE/'ri136-native-policy-dispatch-source-g_z472z7'
A = BASE/'ri134-native-validator-extraction-source-y8kwkcde'
SELF = Q/'qualify_policies.py'
MANIFEST = Q/'SOURCE_IDENTITIES.json'
HANDOFF = Q/'HANDOFF.json'
# Subject-only manifest excludes this dispatcher and its enclosing handoff.
MANIFEST_BYTES = 23216
MANIFEST_SHA256 = 'edb77d0f7edd2e79fd55d3f55b781286aceaf876e98fd1850e58a14281476a37'
PYTHON = Path('/opt/homebrew/bin/python3')
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'output_bytes': 8388608, 'auxiliary_metadata_bytes': 67108864,
          'sample_interval_ms': 50, 'ps_timeout_ms': 250}
SUBJECT_PINS = {
    'native': {
        'caller': {'path': str(A/'supervise.py'), 'bytes': 89283,
                   'sha256': 'e3e4b438dd169aa9f2ef815faec5d6f86766eb68da8a3da20412c90206e9f41d'},
        'controls': {'path': str(A/'native_policy_controls.py'), 'bytes': 22580,
                     'sha256': '8c50cb0ac29385265b89fa9d5b77ee766a74e84d49b0a354f9e7d7c0603e7f25'},
    },
    'audit': {
        'caller': {'path': str(A/'launch_audit.py'), 'bytes': 103969,
                   'sha256': '74f3ef59520a7d8d360a280bcf5d5389d0e3f6c456e8f02178fbc773c4e5d60b'},
        'controls': {'path': str(A/'audit_policy_controls.py'), 'bytes': 19923,
                     'sha256': 'e04a1014d91a49061ec8bde6a2b318209e12328d82d7633f076fcd77a2952548'},
    },
}
CASE_COUNTS = {'native': 77, 'audit': 62}
FINALIZING, RECEIVED_SIGNALS = False, []


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


def literal_path(value):
    require(type(value) is str and '\x00' not in value and Path(value).is_absolute()
            and os.path.normpath(value) == value, 'noncanonical literal path')
    return Path(value)


def validate_identity(value):
    exact(value, ('path', 'bytes', 'sha256'), 'source/evidence identity')
    literal_path(value['path'])
    require(type(value['bytes']) is int and 0 < value['bytes'] <= LIMITS['auxiliary_metadata_bytes']
            and digest_text(value['sha256']) and value['sha256'] != '0'*64, 'invalid positive identity')


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


def read_json(path, expected):
    validate_identity(expected)
    require(expected['path'] == str(path), 'metadata expected path differs')
    raw, identity = read_stable(path)
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


def register(protected, identity):
    validate_identity(identity)
    path = identity['path']
    require(path not in protected or canonical(protected[path]) == canonical(identity),
            'conflicting protected source identity')
    protected[path] = dict(identity)


def load_exact_module(path, expected, name):
    """Future whole-source loading, never edited or extracted validator snippets."""
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
    RECEIVED_SIGNALS.append({'signal': signum, 'during_finalization': FINALIZING})
    if not FINALIZING:
        raise Refused('qualification interrupted by signal '+str(signum))


def validate_manifest(value, protected):
    exact(value, ('schema', 'status', 'subjects', 'acceptance', 'runner_ancestry',
                  'dependency_manifest', 'scope'), 'fixed subject manifest')
    require(value['schema'] == 'ri136-policy-subject-identities-v1'
            and value['status'] == 'SOURCE_ONLY_VERSION_BOUND_POLICY_CASES', 'subject manifest schema differs')
    require(canonical(value['scope']) == canonical({
        'execution_authorized': False, 'scientific_execution': False,
        'old_cases_included': False, 'production_entry_authorized': False}), 'subject manifest scope differs')
    exact(value['subjects'], ('native', 'audit'), 'subject set')
    for which in ('native', 'audit'):
        subject = value['subjects'][which]
        exact(subject, ('caller', 'controls', 'case_count', 'ordered_cases', 'result_contract'), 'subject')
        for role in ('caller', 'controls'):
            require(canonical(subject[role]) == canonical(SUBJECT_PINS[which][role]), 'fixed RI134 subject changed')
            register(protected, subject[role])
        require(type(subject['case_count']) is int and subject['case_count'] == CASE_COUNTS[which]
                and type(subject['ordered_cases']) is list
                and len(subject['ordered_cases']) == subject['case_count'], 'exact RI134 case count differs')
        names = []
        for case in subject['ordered_cases']:
            exact(case, ('id', 'family', 'mutation'), 'static policy case')
            require(all(type(case[key]) is str and bool(case[key]) for key in case)
                    and case['family'] in ('dependency', 'decision', 'review', 'checks'), 'static case fields differ')
            names.append(case['id'])
        require(len(set(names)) == len(names), 'duplicate static policy case')
        contract = subject['result_contract']
        exact(contract, ('keys', 'observed_keys', 'coverage_scope', 'true_fields',
                         'false_fields', 'expected_keys'), 'result contract')
        for key in ('keys', 'observed_keys', 'true_fields', 'false_fields', 'expected_keys'):
            require(type(contract[key]) is list and all(type(item) is str for item in contract[key])
                    and len(contract[key]) == len(set(contract[key])), 'result contract list differs')
        require(type(contract['coverage_scope']) is str and bool(contract['coverage_scope']), 'result scope differs')
    for family in ('acceptance', 'runner_ancestry'):
        require(type(value[family]) is dict and bool(value[family]), 'manifest provenance group absent')
        for identity in value[family].values():
            register(protected, identity)
    register(protected, value['dependency_manifest'])


def validate_observation(observed, case, contract):
    exact(observed, contract['keys'], 'policy observation')
    require(observed['id'] == case['id'] and observed['boundary'] == case['boundary']
            and observed['outcome'] == case['expected']['outcome']
            and observed['coverage_scope'] == contract['coverage_scope'], 'policy observation identity/outcome differs')
    exact(case['expected'], contract['expected_keys'], 'policy expected outcome')
    exact(observed['observed'], contract['observed_keys'], 'policy actual outcome')
    require(canonical(observed['observed']) == canonical({key: case['expected'][key]
            for key in contract['observed_keys']}), 'policy actual first outcome differs')
    for field in contract['true_fields']:
        require(observed[field] is True, 'policy required true field differs: '+field)
    for field in contract['false_fields']:
        require(observed[field] is False, 'policy required false field differs: '+field)
    if 'expected' in observed:
        require(canonical(observed['expected']) == canonical(case['expected']), 'policy expected report differs')


def execute_one(which, case_id, evidence_directory, authorization_digest):
    global FINALIZING
    protected, first_error, result = {}, None, None
    helper, catalogue_before = None, None
    catalogue_postcheck = {'attempted': False, 'unchanged': False, 'reason': 'control module not loaded'}
    started = time.monotonic_ns()
    try:
        require(sys.platform == 'darwin' and Path(__file__).absolute() == SELF, 'fixed dispatcher/host differs')
        evidence = literal_path(evidence_directory)
        require(evidence.parent == BASE and evidence.name.startswith('ri136-policy-run-')
                and len(evidence.name) > len('ri136-policy-run-'), 'operational evidence directory outside fixed scope')
        require(Path.cwd() == evidence and dict(os.environ) == ENV, 'fixed operational cwd/environment differs')
        require(sys.flags.isolated == 1 and sys.flags.no_site == 1
                and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0,
                'fixed isolated normal interpreter flags required')
        require(sys.argv[0] == str(SELF), 'literal dispatcher argv path differs')
        require(os.path.realpath(sys.executable) == os.path.realpath(PYTHON), 'fixed interpreter differs')
        require(which in SUBJECT_PINS and type(case_id) is str and 0 < len(case_id) <= 100
                and all(c.isascii() and (c.isalnum() or c in '-_') for c in case_id), 'unknown caller/case syntax')
        require(digest_text(authorization_digest) and authorization_digest != '0'*64,
                'literal root one-case authorization hash required')
        auth_path = evidence/'AUTHORIZATION.json'
        _, auth_id = read_stable(auth_path)
        register(protected, auth_id)
        require(auth_id['sha256'] == authorization_digest, 'root authorization digest differs')
        auth, _ = read_json(auth_path, auth_id)
        exact(auth, ('schema', 'status', 'caller', 'case', 'source_manifest', 'source_handoff', 'external_preflight',
                     'dispatcher', 'caller_source', 'control_source', 'outer_argv_prefix', 'outer_cwd',
                     'outer_environment', 'limits', 'literal_dispatch_is_external', 'scientific_execution_authorized',
                     'production_entry_authorized', 'retry_or_limit_relaxation_authorized'), 'root policy-case authorization')
        require(auth['schema'] == 'ri136-root-policy-case-authorization-v1'
                and auth['status'] == 'ADMIT_ONE_VERSION_BOUND_PURE_POLICY_CASE'
                and auth['caller'] == which and auth['scientific_execution_authorized'] is False
                and auth['production_entry_authorized'] is False
                and auth['retry_or_limit_relaxation_authorized'] is False, 'root policy-case scope differs')
        exact(auth['case'], ('id', 'family', 'mutation'), 'authorized case')
        require(auth['case']['id'] == case_id, 'authorized literal case differs')
        require(canonical(auth['outer_argv_prefix']) == canonical(
                    [str(PYTHON), '-I', '-S', '-B', str(SELF), which, case_id, str(evidence)])
                and auth['outer_cwd'] == str(evidence) and canonical(auth['outer_environment']) == canonical(ENV)
                and canonical(auth['limits']) == canonical(LIMITS), 'root policy-case command/envelope differs')
        require(auth['literal_dispatch_is_external'] is True, 'external literal dispatch custody required')
        for field, path in (('source_manifest', MANIFEST), ('source_handoff', HANDOFF),
                            ('external_preflight', evidence/'PREFLIGHT.json'), ('dispatcher', SELF)):
            register(protected, auth[field])
            require(auth[field]['path'] == str(path), 'fixed authorization reference path differs: '+field)
        for field, role in (('caller_source', 'caller'), ('control_source', 'controls')):
            require(canonical(auth[field]) == canonical(SUBJECT_PINS[which][role]), 'authorized RI134 subject differs')
            register(protected, auth[field])
        preflight, preflight_id = read_json(evidence/'PREFLIGHT.json', auth['external_preflight'])
        exact(preflight, ('schema', 'status', 'caller', 'case', 'source_manifest', 'source_handoff', 'dispatcher',
                          'caller_source', 'control_source', 'all_runtime_files_match',
                          'all_runtime_namespace_and_host_match', 'all_source_history_dependencies_match',
                          'independent_external_observation', 'operational_directory', 'expected_interpreter', 'evidence'),
              'root external preflight')
        require(preflight['schema'] == 'ri136-root-external-policy-preflight-v1'
                and preflight['status'] == 'ACCEPT_COMPLETE_EXTERNAL_BOOTSTRAP_AND_POLICY_CUSTODY'
                and preflight['caller'] == which and preflight['operational_directory'] == str(evidence)
                and all(preflight[key] is True for key in ('all_runtime_files_match',
                    'all_runtime_namespace_and_host_match', 'all_source_history_dependencies_match',
                    'independent_external_observation'))
                and type(preflight['evidence']) is dict and bool(preflight['evidence']), 'external preflight assertions absent')
        for field in ('case', 'source_manifest', 'source_handoff', 'dispatcher', 'caller_source', 'control_source'):
            require(canonical(preflight[field]) == canonical(auth[field]), 'preflight binding differs: '+field)
        interpreter = preflight['expected_interpreter']
        exact(interpreter, ('path', 'resolved_path', 'bytes', 'sha256', 'symlinks'), 'external interpreter identity')
        validate_identity({key: interpreter[key] for key in ('path', 'bytes', 'sha256')})
        require(interpreter['path'] == str(PYTHON)
                and str(literal_path(interpreter['resolved_path'])) == os.path.realpath(sys.executable)
                and type(interpreter['symlinks']) is list, 'external expected interpreter differs')
        for link in interpreter['symlinks']:
            exact(link, ('path', 'target'), 'external interpreter link')
            literal_path(link['path'])
            require(type(link['target']) is str, 'external interpreter link target differs')
        handoff, handoff_id = read_json(HANDOFF, auth['source_handoff'])
        require(handoff.get('schema') == 'ri136-native-policy-dispatch-source-handoff-v1'
                and handoff.get('status') == 'SOURCE_ONLY_SEALED_FOR_NONAUTHOR_REVIEW'
                and handoff.get('execution_authorized') is False and handoff.get('scientific_execution') is False
                and type(handoff.get('files')) is list and bool(handoff['files']), 'wrong dispatcher source handoff')
        payloads, ordered = {}, []
        for identity in handoff['files']:
            validate_identity(identity)
            path = literal_path(identity['path'])
            require(path.parent == Q and path != HANDOFF and str(path) not in payloads,
                    'source handoff payload path differs')
            payloads[str(path)] = identity
            ordered.append(str(path))
            register(protected, identity)
        require(ordered == sorted(ordered) and str(SELF) in payloads and str(MANIFEST) in payloads,
                'dispatcher/manifest missing or unordered in handoff')
        require(canonical(payloads[str(SELF)]) == canonical(auth['dispatcher'])
                and canonical(payloads[str(MANIFEST)]) == canonical(auth['source_manifest']), 'handoff source bindings differ')
        require(type(MANIFEST_BYTES) is int and MANIFEST_BYTES > 0 and digest_text(MANIFEST_SHA256),
                'fixed subject manifest pin is unbound')
        fixed_manifest = {'path': str(MANIFEST), 'bytes': MANIFEST_BYTES, 'sha256': MANIFEST_SHA256}
        require(canonical(auth['source_manifest']) == canonical(fixed_manifest), 'fixed subject manifest identity differs')
        manifest, manifest_id = read_json(MANIFEST, fixed_manifest)
        validate_manifest(manifest, protected)
        subject = manifest['subjects'][which]
        matches = [case for case in subject['ordered_cases'] if case['id'] == case_id]
        require(len(matches) == 1, 'literal case outside fixed RI134 inventory')
        require(canonical(auth['case']) == canonical(matches[0]), 'authorized case triple differs')
        # All expected paths are registered before the first failure in this loop.
        for path, expected in protected.items():
            _, identity = read_stable(Path(path))
            require(canonical(identity) == canonical(expected), 'protected source/evidence changed before loading: '+path)
        helper, control_id = load_exact_module(Path(subject['controls']['path']), subject['controls'], 'ri134_'+which+'_policy_controls')
        catalogue_before = canonical(helper.CASES)
        require(type(helper.CASES) is tuple, 'loaded case catalogue must be a tuple')
        triples = [{key: item[key] for key in ('id', 'family', 'mutation')} for item in helper.CASES]
        require(canonical(triples) == canonical(subject['ordered_cases']), 'loaded full case catalogue differs')
        selected = [case for case in helper.CASES if case['id'] == case_id]
        require(len(selected) == 1, 'loaded case is not unique')
        case = json.loads(canonical(selected[0]))  # Snapshot metadata, never scientific operands.
        caller, caller_id = load_exact_module(Path(subject['caller']['path']), subject['caller'], 'ri134_'+which+'_policy_subject')
        observed = helper.run_case(caller, case_id)
        validate_observation(observed, case, subject['result_contract'])
        require(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss <= LIMITS['rss_bytes'], 'self RSS ceiling exceeded')
        result = {'schema': 'ri136-pure-policy-observation-v1', 'status': 'OBSERVED_EXACT_PURE_POLICY_CASE_ONLY',
                  'caller': which, 'case': auth['case'], 'expected': case['expected'], 'observation': observed,
                  'caller_source': caller_id, 'control_source': control_id, 'dispatcher': auth['dispatcher'],
                  'source_manifest': manifest_id, 'source_handoff': handoff_id, 'root_authorization': auth_id,
                  'external_preflight': preflight_id, 'external_preflight_assertions_checked_only': True,
                  'independent_outer_origin_and_custody_review_required': True, 'whole_entry': False,
                  'complete_caller_qualification': False, 'scientific_execution': False}
    except BaseException as error:
        FINALIZING = True
        first_error = {'error_type': type(error).__name__, 'error': str(error)[:4096]}
    finally:
        FINALIZING = True
        if helper is not None and catalogue_before is not None:
            try:
                catalogue_postcheck = {'attempted': True, 'unchanged': type(helper.CASES) is tuple
                                      and canonical(helper.CASES) == catalogue_before}
            except BaseException as error:
                catalogue_postcheck = {'attempted': True, 'unchanged': False,
                                      'error_type': type(error).__name__, 'error': str(error)[:2048]}
        final = postchecks(protected)
    elapsed = time.monotonic_ns()-started
    valid = (first_error is None and catalogue_postcheck['unchanged'] is True
             and all(item['unchanged'] is True for item in final)
             and elapsed <= 120000000000 and not RECEIVED_SIGNALS)
    envelope = {'result': result, 'first_error': first_error, 'postchecks': final,
                'catalogue_postcheck': catalogue_postcheck, 'received_signals': list(RECEIVED_SIGNALS),
                'elapsed_ns': elapsed, 'qualified_as_complete': False}
    raw = (canonical(envelope)+'\n').encode('ascii')
    require(len(raw) <= LIMITS['output_bytes'], 'qualification output exceeds fixed cap')
    stream = sys.stdout.buffer if valid else sys.stderr.buffer
    stream.write(raw)
    stream.flush()
    return 0 if valid and not RECEIVED_SIGNALS else 2


def main():
    require(len(sys.argv) == 5, 'require caller, case id, external evidence directory and root authorization digest')
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
        print('RI136 QUALIFICATION REFUSAL: '+type(error).__name__+': '+str(error)[:4096], file=sys.stderr)
        sys.exit(2)
