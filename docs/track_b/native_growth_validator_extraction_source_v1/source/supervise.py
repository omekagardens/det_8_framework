#!/usr/bin/env python3
"""RI-134 source-only four-policy extraction from the accepted RI-129 supervisor.

Preparation grants no execution. The coordinator must review this adapter
and accept precise retained-engine applicability before use; changed validators
and scientific targets do not inherit qualification. Each mode consumes its one exclusive attempt
directory. There is no retry, target override, environment inheritance,
resource override, or successful admission without a byte-pinned explicit
authorization. A successful receipt also requires this supervisor to exit 0.
"""

from hashlib import sha256
from pathlib import Path
import datetime
import errno
import json
import os
import plistlib
import signal
import stat
import subprocess
import sys
import time


E = Path('/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde')
ANCESTRY = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx')
C = E/'closure'
B = C/'native_growth_connected_strict_sign_v1'
SOURCE = Path('/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv')
PYTHON = Path('/opt/homebrew/bin/python3')
PS = Path('/bin/ps')
SELF = E/'supervise.py'
TARGET = B/'check.py'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'sample_interval_ms': 50, 'ps_timeout_ms': 250}
MODES = ('witness', 'normal', 'optimized')
CLOSING, LAUNCHING, RECEIVED_SIGNALS = False, False, []
HISTORY = ANCESTRY/'HISTORY_RECONCILIATION.json'
RUNTIME = ANCESTRY/'RUNTIME_CLOSURE.json'
DEPENDENCIES = E/'SOURCE_DEPENDENCIES.json'
# Closed source/evidence metadata, not a runtime inventory or execution card.
DEPENDENCIES_BYTES = 624320
DEPENDENCIES_SHA256 = '80fb2a5a5f5a318208c9c6389bb7b59646ca18002b32bec01c632d33904cea9a'
DEPENDENCY_ENTRIES = None
RUNTIME_BYTES = 2862854
RUNTIME_SHA256 = '35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'
RUNTIME_VALUE, RUNTIME_IDENTITY, RUNTIME_ENTRIES = None, None, None
HISTORY_BYTES = 2170307
HISTORY_SHA256 = 'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'
HISTORY_IDENTITIES = None
RI128_DECISION = Path('/Volumes/AI_DATA/development/det-review-evidence/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json')
RI128_DECISION_PIN = (3230, '324644290d2d8eeb79a2af655bed476f02f7d0cc3ffb5fac1672f975f0a3ede1')
# Closed original/copy order shared with the independently authored audit caller.
PAIRS = (
    ('checker', SOURCE/'check.py', B/'check.py', 27288, '73bb32320be53c38cf85889ca108229d9c2ea2d79b27814ac258eb4b6f133e38'),
    ('auditor', SOURCE/'audit_saved.py', B/'audit_saved.py', 41355, '5c9494e78df31c726c973d2aa0188ca745a3532a351a5826dcb312fca3892ed7'),
    ('implementation', SOURCE/'IMPLEMENTATION.md', B/'IMPLEMENTATION.md', 9005, 'e9053c9b8e9f6d113febf4cc4b5597aca5e2238a25e67d14c5a3b743149aad26'),
    ('audit_notes', SOURCE/'AUDIT_NOTES.md', B/'AUDIT_NOTES.md', 13789, '89af7f6f7f4ea17e835770ff24ed71e181f5f6f28751f4f7fc8c57cdca77caf6'),
    ('ri88', ANCESTRY/'closure'/'native_growth_connected_sensitivity_v1'/'inputs'/'ri88.json', B/'inputs'/'ri88.json', 1828149, 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    ('ri88_root', Path('/Volumes/AI_DATA/development/det-review-evidence/ri87-ri88-results-checkpoint-3_kuqmvi/RI88_ROOT_RESULT_ADJUDICATION.json'), B/'inputs'/'ri88_root.json', 2783, '15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6'),
    ('ri122_root', Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json'), B/'inputs'/'ri122_root.json', 15477, '162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc'),
    ('ri124_root', Path('/Volumes/AI_DATA/development/det-review-evidence/ri124-root-proof-review-77jju1y6/ROOT_ADJUDICATION.json'), B/'inputs'/'ri124_root.json', 3645, '85b6d5c84139b05d5a18f89614a415ecde962efc429092b914e6f2da33ccde9c'),
    ('ri127_root', Path('/Volumes/AI_DATA/development/det-review-evidence/ri127-root-proof-review-tz7oyfkj/ROOT_ADJUDICATION.json'), B/'inputs'/'ri127_root.json', 4071, '66d274815c101015256ba506f3e6a125375797b1b7946831159d39692ffebd77'),
)
ACCEPTED = {role: pin for role, original, copy, size, pin in PAIRS}
SOURCE_PATHS = {
    'native_supervisor': SELF, 'audit_caller': E/'launch_audit.py',
    'history_manifest': HISTORY, 'runtime_manifest': RUNTIME,
    'caller_contract': E/'CALLER_CONTRACT.md', 'dependency_manifest': DEPENDENCIES,
}
EVIDENCE_NAMES = ('receipt.json', 'stdout.log', 'stderr.log', 'samples.jsonl', 'prepared.json', 'admission.json')
# Source-defined refusal coverage only. These declarations are NOT an executed
# qualification suite and production main never fabricates records or children.
# (name, validating function, required refusal code, intended invalid condition)
CONTROL_DECLARATIONS = (
    ('runtime-unbound-manifest', 'runtime_prepare', 'preparation', 'runtime metadata pin is missing or placeholder'),
    ('runtime-changed-manifest', 'runtime_prepare', 'runtime', 'runtime metadata bytes differ before parsing'),
    ('runtime-membership-change', 'run', 'prerequisite', 'directory names, kinds or link targets changed'),
    ('runtime-absence-invalid', 'run', 'prerequisite', 'declared absent import alternative now exists'),
    ('runtime-host-drift', 'run', 'prerequisite', 'uname, system version or visible system location differs'),
    ('runtime-file-changed', 'runtime_file_prerequisites', 'prerequisite', 'one captured runtime file changed'),
    ('runtime-late-namespace-change', 'run', 'runtime_namespace_change', 'namespace or host changes after launch'),
    ('unbound-dependency-pin', 'dependency_prepare', 'preparation', 'static source dependency pin is missing or placeholder'),
    ('changed-dependency-manifest', 'dependency_prepare', 'dependency', 'static source dependency metadata bytes changed before parsing'),
    ('dependency-order-or-duplicate', 'dependency_prepare', 'dependency', 'static dependency path order or role is not closed'),
    ('dependency-link-or-alias', 'dependency_prepare', 'dependency', 'static dependency identity is linked or resolved elsewhere'),
    ('changed-source-dependency', 'source_prerequisites', 'prerequisite', 'one complete static source/evidence identity changed'),
    ('unbound-history-pin', 'preparation_ready', 'preparation', 'None history pin before Attempt'),
    ('changed-history-manifest', 'preparation_ready', 'history', 'opaque manifest digest changed'),
    ('changed-historical-file', 'source_prerequisites', 'prerequisite', 'one complete historical identity changed'),
    ('history-order-or-duplicate', 'preparation_ready', 'history', 'unsorted or duplicate protected path'),
    ('history-zero-byte-log-valid', 'validate_identity', None, 'zero-byte regular historical log remains allowed'),
    ('missing-root-source-card', 'observed', 'identity', 'fixed current source decision unavailable'),
    ('missing-independent-review', 'observed', 'identity', 'fixed complete source review unavailable'),
    ('wrong-source-card-scope', 'source_prerequisites', 'prerequisite', 'source card claims execution or inherited target qualification'),
    ('wrong-source-card-extra-field', 'source_prerequisites', 'prerequisite', 'extra root source card field'),
    ('transient-current-admission-body', 'read_metadata', 'identity', 'parsed current freeze/auth bytes differ from observed pin'),
    ('transient-saved-witness-body', 'read_metadata', 'identity', 'parsed addendum/witness receipt bytes differ from observed pin'),
    ('changed-scientific-copy', 'source_prerequisites', 'identity', 'fixed source/input byte or size pin changed'),
    ('changed-runtime-bytes', 'runtime_file_prerequisites', 'prerequisite', 'interpreter or monitor captured identity differs'),
    ('changed-runtime-links', 'runtime_file_prerequisites', 'prerequisite', 'literal interpreter symlink traversal differs'),
    ('wrong-applicability-mode', 'applicability', 'prerequisite', 'stage applicability for another mode'),
    ('wrong-applicability-argv-env-limits', 'applicability', 'prerequisite', 'fixed command or envelope differs'),
    ('old-target-qualification-credit', 'completed_mode', 'prerequisite', 'completed review lacks current15/4/71 actual checks or credits old qualification'),
    ('missing-prerequisite-before-attempt', 'pre_attempt_prerequisites', 'identity', 'missing current card/input/prior custody refuses before exclusive Attempt allocation'),
    ('future-card-not-completed', 'completed_mode', 'prerequisite', 'prior root custody is not completed and accepted'),
    ('receipt-flag-only', 'completed_mode', 'prerequisite', 'receipt success without genuine completed outer zero exit'),
    ('outer-boolean-zero', 'completed_mode', 'prerequisite', 'outer exit_code false instead of integer zero'),
    ('outer-unfinished-session', 'completed_mode', 'prerequisite', 'outer result retains session_id'),
    ('outer-invocation-reconstruction', 'completed_mode', 'prerequisite', 'actual invocation differs from admitted literal'),
    ('wrong-completed-output-reference', 'bind', 'prerequisite', 'completed review references wrong current bytes'),
    ('supplemental-reference-outside-closure', 'current', 'identity', 'metadata narrative references unclosed path'),
    ('prior-snapshot-role-set', 'completed_mode', 'prerequisite', 'receipt has extra or omitted input role'),
    ('freeze-input-order', 'validate_freeze', 'configuration', 'ordered input array permuted or extended'),
    ('premature-normal', 'observed', 'identity', 'missing completed witness card/evidence'),
    ('premature-optimized', 'observed', 'identity', 'missing completed normal card/evidence'),
    ('partial-candidate', 'candidate_prerequisite', 'identity', 'candidate differs in any byte from complete witness'),
    ('candidate-math-promotion', 'candidate_prerequisite', 'prerequisite', 'candidate custody asserts scientific acceptance'),
    ('wrong-summary-whole-bytes', 'completed_mode', 'identity', 'optimized and normal complete summaries differ'),
    ('witness-existing-candidate', 'run', 'witness_certificate', 'any of the three candidate paths already exists'),
    ('attempt-output-reuse', 'Attempt.__init__', 'FileExistsError', 'exclusive attempt directory already exists'),
    ('wrong-outer-cwd-env-flags', 'run', 'configuration', 'outer cwd/environment/isolated flags or argv changed'),
    ('late-input-change', 'run', 'input_change', 'input identities change after admitted child'),
    ('inherited-monitor-failure', 'monitor', 'monitor', 'missing/malformed/nonzero/timed-out required census'),
    ('inherited-wall-limit', 'run', 'wall_limit', 'child exceeds the fixed 120-second deadline'),
    ('inherited-rss-limit', 'run', 'rss_limit', 'sampled owned group exceeds 512 MiB'),
    ('inherited-signal', 'stop_signal', 'signal', 'catchable interruption invalidates success'),
)


class Stop(RuntimeError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def need(condition, code, message):
    if not condition:
        raise Stop(code, message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def exact_keys(value, keys, code, context):
    need(type(value) is dict and set(value) == set(keys), code, context+' fields mismatch')


def hexhash(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def strict_json(raw, allow_floats=False):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'configuration', 'duplicate JSON key')
            result[key] = value
        return result
    def bad(value):
        raise Stop('configuration', 'JSON decimals and nonfinite constants are forbidden')
    def finite_float(value):
        result = float(value)
        need(-float('inf') < result < float('inf'), 'configuration', 'nonfinite receipt duration')
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_float=finite_float if allow_floats else bad, parse_constant=bad)


def argv_for(mode):
    argv = [str(PYTHON), '-I', '-S', '-B']
    if mode == 'optimized':
        argv.append('-O')
    argv.append(str(TARGET))
    if mode == 'witness':
        argv.append('--witness')
    return argv


def prior_paths(mode):
    prefix = mode.upper()
    attempt = E/(mode+'-01')
    result = {name: attempt/(name+'.json' if name in ('receipt', 'prepared', 'admission') else name+'.log')
              for name in ('receipt', 'stdout', 'stderr', 'samples', 'prepared', 'admission')}
    result['samples'] = attempt/'samples.jsonl'
    result.update({
        'freeze': E/(prefix+'_EXECUTION_FREEZE.json'),
        'authorization': E/(prefix+'_AUTHORIZATION.json'),
        'root_admission': E/(prefix+'_ROOT_ADMISSION.json'),
        'tool_completion': E/(prefix+'_OUTER_TOOL_RESULT.json'),
        'root_review': E/(prefix+'_ROOT_COMPLETE_REVIEW.json'),
        'independent_review': E/(prefix+'_INDEPENDENT_COMPLETE_REVIEW.json'),
        'custody': E/(prefix+'_ROOT_CUSTODY.json'),
        'applicability': E/(prefix+'_APPLICABILITY.json'),
    })
    return result


def input_paths(mode):
    need(type(mode) is str and mode in MODES, 'configuration', 'unknown fixed mode')
    need(type(HISTORY_IDENTITIES) is tuple, 'preparation', 'history preparation is not bound')
    result = {}
    for role, original, copy, size, pin in PAIRS:
        result[role+'_original'] = original
        result[role+'_copy'] = copy
    result.update(monitor=PS, history_manifest=HISTORY, runtime_manifest=RUNTIME,
                  dependency_manifest=DEPENDENCIES)
    for item in RUNTIME_ENTRIES:
        need(item['role'] not in result, 'runtime', 'runtime role collision')
        result[item['role']] = Path(item['path'])
    for entry in HISTORY_IDENTITIES:
        need(entry['role'] not in result, 'history', 'historical role collides with fixed role')
        result[entry['role']] = Path(entry['path'])
    for entry in DEPENDENCY_ENTRIES:
        need(entry['role'] not in result, 'dependency', 'source dependency role collides with fixed role')
        result[entry['role']] = Path(entry['path'])
    result.update(audit_caller=E/'launch_audit.py', caller_contract=E/'CALLER_CONTRACT.md',
                  source_adjudication=E/'ROOT_SOURCE_ADJUDICATION.json',
                  independent_source_review=E/'INDEPENDENT_SOURCE_REVIEW.json',
                  ri128_source_adjudication=RI128_DECISION,
                  mode_applicability=E/(mode.upper()+'_APPLICABILITY.json'))
    if mode != 'witness':
        result.update(certificate_original=E/'CERTIFICATE.json', certificate=B/'CERTIFICATE.json',
                      audit_candidate=E/'AUDIT_CANDIDATE.json',
                      certificate_addendum=E/'SAVED_CERTIFICATE_ADDENDUM.json',
                      candidate_custody=E/'CANDIDATE_CUSTODY.json')
    for previous in MODES[:MODES.index(mode)]:
        for role, path in prior_paths(previous).items():
            result[previous+'_'+role] = path
    return result


def complete_paths(mode):
    return dict(input_paths(mode), interpreter=PYTHON, supervisor=SELF,
                freeze=E/(mode.upper()+'_EXECUTION_FREEZE.json'),
                authorization=E/(mode.upper()+'_AUTHORIZATION.json'))


def certificate_absence():
    return {'original': not os.path.lexists(E/'CERTIFICATE.json'),
            'copy': not os.path.lexists(B/'CERTIFICATE.json'),
            'audit_copy': not os.path.lexists(E/'AUDIT_CANDIDATE.json')}


def resolve_links(path):
    """Resolve every component, retaining literal links in traversal order."""
    need(type(path) is Path or isinstance(path, Path), 'identity', 'identity path must be a Path')
    text = str(path)
    need(path.is_absolute() and os.path.normpath(text) == text, 'identity', 'noncanonical absolute path')
    links, seen = [], set()
    current = text
    for _ in range(64):
        need(current not in seen, 'identity', 'symlink resolution cycle')
        seen.add(current)
        parts = Path(current).parts
        prefix = Path(parts[0])
        for i, part in enumerate(parts[1:], 1):
            prefix = prefix/part
            status = prefix.lstat()
            if stat.S_ISLNK(status.st_mode):
                target = os.readlink(prefix)
                links.append({'path': str(prefix), 'target': target})
                replacement = Path(target) if os.path.isabs(target) else prefix.parent/target
                current = os.path.normpath(str(replacement.joinpath(*parts[i+1:])))
                break
        else:
            return Path(current), links
    raise Stop('identity', 'symlink resolution limit exceeded')


def file_identity(path):
    resolved, links = resolve_links(path)
    flags = os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0)
    descriptor = os.open(resolved, flags)
    try:
        before = os.fstat(descriptor)
        need(stat.S_ISREG(before.st_mode), 'identity', 'input is not a regular file')
        hasher, length = sha256(), 0
        while True:
            chunk = os.read(descriptor, 1024*1024)
            if not chunk:
                break
            hasher.update(chunk)
            length += len(chunk)
        after = os.fstat(descriptor)
        signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        need(signature(before) == signature(after) and length == after.st_size,
             'identity', 'input changed while hashing')
    finally:
        os.close(descriptor)
    again, again_links = resolve_links(path)
    need(again == resolved and again_links == links, 'identity', 'symlink chain changed while hashing')
    return {'path': str(path), 'resolved_path': str(resolved), 'bytes': length,
            'sha256': hasher.hexdigest(), 'symlinks': links}


def validate_identity(value, path):
    exact_keys(value, ('path', 'resolved_path', 'bytes', 'sha256', 'symlinks'), 'configuration', 'file identity')
    need(value['path'] == str(path) and type(value['resolved_path']) is str
         and Path(value['resolved_path']).is_absolute()
         and type(value['bytes']) is int and value['bytes'] >= 0
         and hexhash(value['sha256']) and type(value['symlinks']) is list,
         'configuration', 'invalid file identity fields')
    for link in value['symlinks']:
        exact_keys(link, ('path', 'target'), 'configuration', 'symlink identity')
        need(type(link['path']) is str and Path(link['path']).is_absolute()
             and type(link['target']) is str, 'configuration', 'invalid symlink identity fields')


def snapshot(paths):
    result = {}
    for role, path in paths.items():
        try:
            result[role] = {'ok': True, 'identity': file_identity(path)}
        except Exception as error:
            result[role] = {'ok': False, 'error': type(error).__name__+': '+str(error)}
    return result


def fsync_directory(path):
    descriptor = os.open(path, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def exclusive_json(path, value):
    with path.open('xb') as stream:
        stream.write((canonical(value)+'\n').encode())
        stream.flush()
        os.fsync(stream.fileno())
    fsync_directory(path.parent)


def observed(before, role):
    need(before[role]['ok'] is True, 'identity', 'unavailable input identity: '+role)
    return before[role]['identity']


def runtime_canonical_path(value):
    need(type(value) is str and Path(value).is_absolute()
         and os.path.normpath(value) == value, 'runtime', 'noncanonical runtime path')
    return value


def validate_dependency_payload(value):
    exact_keys(value, ('schema', 'status', 'protected_files', 'scope'),
               'dependency', 'static source dependency manifest')
    need(value['schema'] == 'ri129-source-dependencies-v1'
         and value['status'] == 'SOURCE_ONLY_CLOSED_DEPENDENCIES',
         'dependency', 'static source dependency manifest schema differs')
    same(value['scope'], {
        'scientific_execution': False, 'runtime_inventory_created': False,
        'active_execution_artifacts_created': False, 'old_history_and_runtime_preserved': True,
    }, 'static source dependency scope differs')
    need(type(value['protected_files']) is list and bool(value['protected_files']),
         'dependency', 'static source dependency closure is empty')
    entries, previous = [], None
    for index, entry in enumerate(value['protected_files'], 1):
        exact_keys(entry, ('role', 'path', 'identity', 'classification', 'access_policy',
                           'reference_provenance'), 'dependency', 'static source dependency entry')
        path = entry['path']
        need(entry['role'] == 'dep_'+str(index).zfill(4) and type(path) is str
             and Path(path).is_absolute() and os.path.normpath(path) == path
             and (previous is None or previous < path),
             'dependency', 'static dependency role/order/path differs')
        validate_identity(entry['identity'], Path(path))
        need(entry['identity']['resolved_path'] == path and entry['identity']['symlinks'] == [],
             'dependency', 'static source dependency has a symlink or alias')
        need(type(entry['classification']) is str and bool(entry['classification'])
             and type(entry['access_policy']) is str and bool(entry['access_policy'])
             and type(entry['reference_provenance']) is list,
             'dependency', 'static dependency provenance field types differ')
        previous = path
        entries.append(entry)
    return entries


def dependency_prepare():
    """Authenticate only the closed authored metadata; never discover new files."""
    global DEPENDENCY_ENTRIES
    if DEPENDENCY_ENTRIES is not None:
        return
    need(type(DEPENDENCIES_BYTES) is int and 0 < DEPENDENCIES_BYTES <= 64*1024*1024
         and hexhash(DEPENDENCIES_SHA256) and DEPENDENCIES_SHA256 != '0'*64,
         'preparation', 'reviewed source dependency manifest pin is unbound')
    identity = file_identity(DEPENDENCIES)
    need((identity['bytes'], identity['sha256']) == (DEPENDENCIES_BYTES, DEPENDENCIES_SHA256),
         'dependency', 'reviewed source dependency manifest changed')
    raw = DEPENDENCIES.read_bytes()
    need(len(raw) == DEPENDENCIES_BYTES and sha256(raw).hexdigest() == DEPENDENCIES_SHA256,
         'dependency', 'source dependency bytes changed before metadata parse')
    value = strict_json(raw)
    entries = validate_dependency_payload(value)
    same(file_identity(DEPENDENCIES), identity, 'source dependency manifest changed during preparation')
    DEPENDENCY_ENTRIES = tuple(entries)


def runtime_prepare():
    """Authenticate fixed source-time metadata; never discover a new input."""
    global RUNTIME_VALUE, RUNTIME_IDENTITY, RUNTIME_ENTRIES
    if RUNTIME_VALUE is not None:
        return
    need(type(RUNTIME_BYTES) is int and 0 < RUNTIME_BYTES <= 64*1024*1024
         and hexhash(RUNTIME_SHA256) and RUNTIME_SHA256 != '0'*64,
         'preparation', 'reviewed runtime manifest pin is unbound')
    identity = file_identity(RUNTIME)
    need((identity['bytes'], identity['sha256']) == (RUNTIME_BYTES, RUNTIME_SHA256),
         'runtime', 'reviewed runtime manifest changed')
    raw = RUNTIME.read_bytes()
    need(len(raw) == RUNTIME_BYTES and sha256(raw).hexdigest() == RUNTIME_SHA256,
         'runtime', 'runtime bytes changed before metadata parse')
    value = strict_json(raw)
    need(type(value) is dict
         and value.get('schema') == 'ri122-captured-application-runtime-v1'
         and value.get('status') == 'SOURCE_ONLY_CURRENT_RUNTIME_CANDIDATE'
         and all(key in value for key in ('files', 'directories', 'absences', 'host_platform')),
         'runtime', 'runtime manifest schema differs')
    need(type(value['files']) is list and bool(value['files']),
         'runtime', 'runtime file closure is empty')
    previous, by_path = None, {}
    for index, item in enumerate(value['files'], 1):
        exact_keys(item, ('role', 'path', 'identity', 'classification', 'reference_provenance'),
                   'runtime', 'runtime file entry')
        path = runtime_canonical_path(item['path'])
        need(item['role'] == 'runtime_'+str(index).zfill(4)
             and (previous is None or previous < path), 'runtime', 'runtime file order or role differs')
        validate_identity(item['identity'], Path(path))
        need(type(item['classification']) is str and bool(item['classification'])
             and type(item['reference_provenance']) is str and bool(item['reference_provenance']),
             'runtime', 'runtime file provenance differs')
        previous, by_path[path] = path, item['identity']
    for path in (PYTHON, PS):
        need(str(path) in by_path and by_path[str(path)]['bytes'] > 0,
             'runtime', 'fixed interpreter or monitor missing from runtime files')
    need(type(value['directories']) is list and bool(value['directories']),
         'runtime', 'runtime directory closure is empty')
    previous = None
    for item in value['directories']:
        exact_keys(item, ('path', 'resolved_path', 'symlinks', 'entries'), 'runtime', 'runtime directory')
        path = runtime_canonical_path(item['path'])
        runtime_canonical_path(item['resolved_path'])
        need(previous is None or previous < path, 'runtime', 'runtime directory order differs')
        previous = path
        need(type(item['symlinks']) is list and type(item['entries']) is list,
             'runtime', 'directory links or entries malformed')
        for link in item['symlinks']:
            exact_keys(link, ('path', 'target'), 'runtime', 'directory symlink')
            runtime_canonical_path(link['path'])
            need(type(link['target']) is str, 'runtime', 'directory symlink target malformed')
        names = []
        for child in item['entries']:
            need(type(child) is dict and child.get('kind') in ('file', 'dir', 'symlink'),
                 'runtime', 'unsupported directory member kind')
            exact_keys(child, ('name', 'kind', 'target') if child['kind'] == 'symlink' else ('name', 'kind'),
                       'runtime', 'directory member')
            name = child['name']
            need(type(name) is str and bool(name) and name not in ('.', '..') and '/' not in name
                 and chr(0) not in name, 'runtime', 'invalid directory member name')
            if child['kind'] == 'symlink':
                need(type(child['target']) is str, 'runtime', 'invalid directory member link')
            names.append(name)
        need(names == sorted(set(names)), 'runtime', 'directory members not uniquely sorted')
    need(type(value['absences']) is list, 'runtime', 'runtime absences malformed')
    absent = [runtime_canonical_path(path) for path in value['absences']]
    need(absent == sorted(set(absent)) and not set(absent).intersection(by_path)
         and not set(absent).intersection(item['path'] for item in value['directories']),
         'runtime', 'runtime absences unordered, duplicate or conflicting')
    host = value['host_platform']
    exact_keys(host, ('expected_uname', 'system_version_plist', 'system_dependencies',
                      'scope_decision', 'trust_boundary'), 'runtime', 'host-platform premises')
    exact_keys(host['expected_uname'], ('sysname', 'release', 'version', 'machine'),
               'runtime', 'host uname')
    need(all(type(item) is str and bool(item) for item in host['expected_uname'].values())
         and host['expected_uname']['sysname'] == 'Darwin', 'runtime', 'host uname premises malformed')
    plist = host['system_version_plist']
    exact_keys(plist, ('path', 'expected_values'), 'runtime', 'system version metadata')
    need(plist['path'] == '/System/Library/CoreServices/SystemVersion.plist'
         and plist['path'] in by_path, 'runtime', 'fixed system version plist unpinned')
    exact_keys(plist['expected_values'], ('ProductName', 'ProductVersion', 'ProductBuildVersion'),
               'runtime', 'system version fields')
    need(all(type(item) is str and bool(item) for item in plist['expected_values'].values()),
         'runtime', 'system version values malformed')
    need(type(host['system_dependencies']) is list, 'runtime', 'system dependencies malformed')
    seen = set()
    for item in host['system_dependencies']:
        exact_keys(item, ('install_name', 'source_images', 'location_status', 'shared_cache_status'),
                   'runtime', 'system dependency')
        path = runtime_canonical_path(item['install_name'])
        need((path.startswith('/usr/lib/') or path.startswith('/System/Library/'))
             and path not in seen and item['location_status'] in ('regular_file', 'symlink', 'absent', 'unavailable')
             and item['shared_cache_status'] == 'not_independently_inspected_trusted_host_premise'
             and type(item['source_images']) is list and bool(item['source_images'])
             and all(type(source) is str and source in by_path for source in item['source_images']),
             'runtime', 'system dependency outside fixed trusted-platform boundary')
        seen.add(path)
    scope_path = '/Volumes/AI_DATA/development/det-review-evidence/ri120-root-source-review-sksu97l1/RI122_HOST_PLATFORM_SCOPE_DECISION.json'
    validate_identity(host['scope_decision'], Path(scope_path))
    need(scope_path in by_path, 'runtime', 'owner host-platform scope decision unpinned')
    same(host['scope_decision'], by_path[scope_path], 'owner host-platform scope identity differs')
    need(type(host['trust_boundary']) is str and bool(host['trust_boundary']),
         'runtime', 'trusted host-platform boundary missing')
    same(file_identity(RUNTIME), identity, 'runtime metadata changed during preparation')
    RUNTIME_VALUE, RUNTIME_IDENTITY, RUNTIME_ENTRIES = value, identity, tuple(value['files'])


def runtime_file_identity(path):
    need(RUNTIME_ENTRIES is not None, 'runtime', 'runtime preparation missing')
    matches = [item['identity'] for item in RUNTIME_ENTRIES if item['path'] == str(path)]
    need(len(matches) == 1, 'runtime', 'fixed runtime path not uniquely captured')
    return matches[0]


def runtime_file_prerequisites(known):
    need(RUNTIME_VALUE is not None, 'runtime', 'runtime metadata missing')
    for item in RUNTIME_ENTRIES:
        same(known[item['path']], item['identity'], 'captured runtime file identity changed: '+item['path'])
    same(known[str(RUNTIME)], RUNTIME_IDENTITY, 'runtime manifest changed after preparation')


def runtime_expected_namespace():
    need(RUNTIME_VALUE is not None, 'runtime', 'runtime namespace metadata missing')
    host = RUNTIME_VALUE['host_platform']
    return {
        'directories': {item['path']: {'ok': True, 'identity': item}
                        for item in RUNTIME_VALUE['directories']},
        'absences': {path: {'ok': True, 'absent': True} for path in RUNTIME_VALUE['absences']},
        'host_platform': {
            'uname': {'ok': True, 'identity': host['expected_uname']},
            'system_version': {'ok': True, 'identity': host['system_version_plist']['expected_values']},
            'system_dependencies': [
                {'ok': True, 'identity': {key: item[key] for key in
                 ('install_name', 'location_status', 'shared_cache_status')}}
                for item in host['system_dependencies']],
            'trust_boundary': host['trust_boundary'],
        },
    }


def runtime_directory_identity(path):
    resolved, links = resolve_links(path)
    before = resolved.stat()
    need(stat.S_ISDIR(before.st_mode), 'runtime', 'runtime namespace path is not a directory')
    def members():
        result = []
        with os.scandir(resolved) as iterator:
            for entry in iterator:
                status = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(status.st_mode):
                    item = {'name': entry.name, 'kind': 'symlink', 'target': os.readlink(entry.path)}
                elif stat.S_ISREG(status.st_mode):
                    item = {'name': entry.name, 'kind': 'file'}
                elif stat.S_ISDIR(status.st_mode):
                    item = {'name': entry.name, 'kind': 'dir'}
                else:
                    raise Stop('runtime', 'unsupported runtime namespace object: '+entry.path)
                result.append(item)
        return sorted(result, key=lambda item: item['name'])
    entries = members()
    after = resolved.stat()
    signature = lambda value: (value.st_dev, value.st_ino, value.st_mode, value.st_mtime_ns, value.st_ctime_ns)
    again, again_links = resolve_links(path)
    need(signature(before) == signature(after) and entries == members()
         and again == resolved and again_links == links,
         'runtime', 'runtime directory changed during observation')
    return {'path': str(path), 'resolved_path': str(resolved), 'symlinks': links, 'entries': entries}


def runtime_system_location(path):
    try:
        status = Path(path).lstat()
    except FileNotFoundError as error:
        need(error.errno == errno.ENOENT, 'runtime', 'system location absence is not ENOENT')
        return 'absent'
    if stat.S_ISLNK(status.st_mode):
        return 'symlink'
    need(stat.S_ISREG(status.st_mode), 'runtime', 'system dependency is not a regular file or link')
    return 'regular_file'


def runtime_system_version():
    host = RUNTIME_VALUE['host_platform']['system_version_plist']
    path = Path(host['path'])
    expected = runtime_file_identity(path)
    before = file_identity(path)
    same(before, expected, 'system version plist identity changed')
    raw = path.read_bytes()
    need(len(raw) == expected['bytes'] and sha256(raw).hexdigest() == expected['sha256'],
         'runtime', 'system version metadata raw bytes changed')
    value = plistlib.loads(raw)
    need(type(value) is dict, 'runtime', 'system version metadata is not a dictionary')
    result = {key: value[key] for key in ('ProductName', 'ProductVersion', 'ProductBuildVersion')}
    need(all(type(item) is str for item in result.values()), 'runtime', 'system version metadata types differ')
    same(file_identity(path), expected, 'system version plist changed during metadata read')
    return result


def runtime_namespace_snapshot():
    """Every fixed path is attempted independently, including after any failure."""
    result = {'directories': {}, 'absences': {}, 'host_platform': {}}
    for item in RUNTIME_VALUE['directories']:
        try:
            observed = {'ok': True, 'identity': runtime_directory_identity(Path(item['path']))}
        except Exception as error:
            observed = {'ok': False, 'error': type(error).__name__+': '+str(error)}
        result['directories'][item['path']] = observed
    for path in RUNTIME_VALUE['absences']:
        try:
            try:
                Path(path).lstat()
                absent = False
            except FileNotFoundError as error:
                need(error.errno == errno.ENOENT, 'runtime', 'runtime absence is not ENOENT')
                absent = True
            observed = {'ok': True, 'absent': absent}
        except Exception as error:
            observed = {'ok': False, 'error': type(error).__name__+': '+str(error)}
        result['absences'][path] = observed
    host = result['host_platform']
    try:
        value = os.uname()
        host['uname'] = {'ok': True, 'identity': {key: getattr(value, key) for key in
                                                ('sysname', 'release', 'version', 'machine')}}
    except Exception as error:
        host['uname'] = {'ok': False, 'error': type(error).__name__+': '+str(error)}
    try:
        host['system_version'] = {'ok': True, 'identity': runtime_system_version()}
    except Exception as error:
        host['system_version'] = {'ok': False, 'error': type(error).__name__+': '+str(error)}
    host['system_dependencies'] = []
    for item in RUNTIME_VALUE['host_platform']['system_dependencies']:
        try:
            identity = {'install_name': item['install_name'],
                        'location_status': runtime_system_location(item['install_name']),
                        'shared_cache_status': item['shared_cache_status']}
            observed = {'ok': True, 'identity': identity}
        except Exception as error:
            observed = {'ok': False, 'install_name': item['install_name'],
                        'error': type(error).__name__+': '+str(error)}
        host['system_dependencies'].append(observed)
    host['trust_boundary'] = RUNTIME_VALUE['host_platform']['trust_boundary']
    return result


def preparation_ready():
    """Authenticate a closed source-time manifest before allocating an attempt."""
    global HISTORY_IDENTITIES
    dependency_prepare()
    runtime_prepare()
    need(type(HISTORY_BYTES) is int and HISTORY_BYTES > 0 and hexhash(HISTORY_SHA256)
         and HISTORY_SHA256 != '0'*64, 'preparation', 'reviewed history pin is not bound')
    identity = file_identity(HISTORY)
    need((identity['bytes'], identity['sha256']) == (HISTORY_BYTES, HISTORY_SHA256),
         'history', 'reviewed history manifest changed')
    raw = HISTORY.read_bytes()
    need(len(raw) == HISTORY_BYTES and sha256(raw).hexdigest() == HISTORY_SHA256,
         'history', 'history bytes changed before parse')
    manifest = strict_json(raw)
    need(type(manifest) is dict and manifest.get('schema') == 'ri122-native-history-reconciliation-v1'
         and manifest.get('status') == 'SOURCE_ONLY_CURRENT_CUSTODY_CANDIDATE'
         and type(manifest.get('protected_files')) is list and manifest['protected_files'],
         'history', 'closed history manifest schema differs')
    entries, previous = [], None
    for index, entry in enumerate(manifest['protected_files'], 1):
        exact_keys(entry, ('role', 'path', 'identity', 'classification', 'access_policy',
                           'reference_provenance'), 'history', 'protected history entry')
        need(entry['role'] == 'hist_'+str(index).zfill(4) and type(entry['path']) is str
             and Path(entry['path']).is_absolute() and os.path.normpath(entry['path']) == entry['path']
             and (previous is None or previous < entry['path']),
             'history', 'historical role/order/path differs')
        validate_identity(entry['identity'], Path(entry['path']))
        need(type(entry['classification']) is str and bool(entry['classification'])
             and type(entry['access_policy']) is str and bool(entry['access_policy'])
             and type(entry['reference_provenance']) is list,
             'history', 'historical provenance field types differ')
        previous = entry['path']
        entries.append(entry)
    need(canonical(file_identity(HISTORY)) == canonical(identity), 'history', 'history changed during preparation')
    HISTORY_IDENTITIES = tuple(entries)  # Cached once; no filesystem discovery or referenced-body traversal.


def same(left, right, context):
    need(canonical(left) == canonical(right), 'prerequisite', context)


def identity_index(before):
    result = {}
    for role in before:
        identity = observed(before, role)
        path = identity['path']
        if path in result:
            same(identity, result[path], 'aliased current identities differ')
        result[path] = identity
    return result


def current(index, path):
    need(str(path) in index, 'identity', 'reference outside closed current inventory: '+str(path))
    return index[str(path)]


def bind(value, path, index):
    validate_identity(value, path)
    same(value, current(index, path), 'complete metadata identity differs: '+str(path))


def bind_all_refs(value, index):
    # Only walk metadata explicitly read by these validators. Never follow a
    # reference to decode another body or inspect scientific stdout/candidates.
    if type(value) is list:
        for item in value:
            bind_all_refs(item, index)
    elif type(value) is dict:
        if all(key in value for key in ('path', 'bytes', 'sha256')):
            need(type(value['path']) is str, 'identity', 'reference path is not text')
            actual = current(index, value['path'])
            for key in ('path', 'bytes', 'sha256', 'resolved_path', 'symlinks'):
                if key in value:
                    same(value[key], actual[key], 'metadata reference differs: '+value['path'])
        for item in value.values():
            bind_all_refs(item, index)


def read_metadata(path, index, allow_floats=True):
    identity = current(index, path)
    need(identity['bytes'] > 0 and identity['bytes'] <= 64*1024*1024,
         'prerequisite', 'metadata is empty or exceeds fixed 64-MiB read ceiling')
    raw = path.read_bytes()
    need(len(raw) == identity['bytes'] and sha256(raw).hexdigest() == identity['sha256'],
         'identity', 'metadata changed before decoding: '+str(path))
    value = strict_json(raw, allow_floats=allow_floats)
    need(type(value) is dict, 'prerequisite', 'metadata must be a JSON object')
    bind_all_refs(value, index)
    return value


def validate_ri128_source_decision(value):
    """The exact RI128 decision accepts unexecuted sources, never actual signs."""
    need(value.get('schema') == 'ri128-root-proof-source-adjudication-v1'
         and value.get('status') == 'ACCEPT_ACTUAL_SCALE_CONTAINMENT_AND_BOUNDED_UNEXECUTED_SIGN_SOURCES'
         and value.get('actual_signs_decided') is False
         and value.get('full_H30_feasibility') is False
         and value.get('numerical_qualification_accepted') is False
         and value.get('physical_claim') is False
         and value.get('programme_complete') is False
         and value.get('resource_feasibility_demonstrated') is False
         and value.get('scientific_body_decode') is False
         and value.get('source_execution') is False
         and value.get('ret_paused') is True,
         'prerequisite', 'RI128 accepted source-only boundary differs')


def validate_source_decision_payload(decision, index):
    exact_keys(decision, ('schema', 'status', 'accepted_sources', 'independent_review', 'ri128_source_adjudication',
                          'history_manifest', 'dependency_manifest', 'execution_authorized', 'qualification_transferred_to_changed_targets'),
               'prerequisite', 'root source adjudication')
    need(decision['schema'] == 'ri129-root-caller-source-adjudication-v1'
         and decision['status'] == 'ACCEPT_EXACT_NATIVE_CALLER_SOURCE_ONLY'
         and decision['execution_authorized'] is False
         and decision['qualification_transferred_to_changed_targets'] is False,
         'prerequisite', 'source adjudication scope differs')
    exact_keys(decision['accepted_sources'], SOURCE_PATHS, 'prerequisite', 'accepted caller sources')
    for role, path in SOURCE_PATHS.items():
        bind(decision['accepted_sources'][role], path, index)
    for key, path in (('independent_review', E/'INDEPENDENT_SOURCE_REVIEW.json'),
                      ('ri128_source_adjudication', RI128_DECISION), ('history_manifest', HISTORY),
                      ('dependency_manifest', DEPENDENCIES)):
        bind(decision[key], path, index)


def validate_source_review_payload(review, index):
    need(review.get('schema') == 'ri129-independent-complete-caller-source-review-v1'
         and review.get('status') == 'PASS_COMPLETE_SOURCE_REVIEW_ONLY'
         and review.get('blocking_findings') == [] and review.get('scientific_execution') is False
         and review.get('execution_authorized') is False,
         'prerequisite', 'independent complete source review differs')
    exact_keys(review.get('sources'), SOURCE_PATHS, 'prerequisite', 'independently reviewed sources')
    for role, path in SOURCE_PATHS.items():
        bind(review['sources'][role], path, index)


def source_prerequisites(index):
    for role, original, copy, size, pin in PAIRS:
        for path in (original, copy):
            item = current(index, path)
            need((item['bytes'], item['sha256']) == (size, pin), 'identity', 'fixed scientific source/input changed')
    runtime_file_prerequisites(index)
    item = current(index, RI128_DECISION)
    need((item['bytes'], item['sha256']) == RI128_DECISION_PIN, 'identity', 'accepted RI128 source decision changed')
    for entry in HISTORY_IDENTITIES:
        same(current(index, entry['path']), entry['identity'], 'historical identity changed')
    item = current(index, HISTORY)
    need((item['bytes'], item['sha256']) == (HISTORY_BYTES, HISTORY_SHA256), 'history', 'history pin differs')
    for entry in DEPENDENCY_ENTRIES:
        same(current(index, entry['path']), entry['identity'], 'static source dependency identity changed')
    item = current(index, DEPENDENCIES)
    need((item['bytes'], item['sha256']) == (DEPENDENCIES_BYTES, DEPENDENCIES_SHA256),
         'dependency', 'static source dependency pin differs')
    decision = read_metadata(E/'ROOT_SOURCE_ADJUDICATION.json', index)
    validate_source_decision_payload(decision, index)
    review = read_metadata(E/'INDEPENDENT_SOURCE_REVIEW.json', index)
    validate_source_review_payload(review, index)
    inherited = read_metadata(RI128_DECISION, index)
    validate_ri128_source_decision(inherited)


def applicability(mode, index):
    card = read_metadata(E/(mode.upper()+'_APPLICABILITY.json'), index)
    exact_keys(card, ('schema', 'status', 'mode', 'source_adjudication', 'independent_review',
                      'ri128_source_adjudication', 'history_manifest', 'dependency_manifest', 'supervisor', 'target', 'interpreter',
                      'monitor', 'argv', 'cwd', 'environment', 'limits', 'retained_engine_only',
                      'changed_target_qualification_inherited', 'changed_validators_reviewed', 'execution_authorized'),
               'prerequisite', 'stage applicability')
    need(card['schema'] == 'ri129-stage-applicability-v1'
         and card['status'] == 'ACCEPT_PRECISE_FIXED_STAGE_APPLICABILITY_ONLY' and card['mode'] == mode
         and card['retained_engine_only'] is True and card['changed_target_qualification_inherited'] is False
         and card['changed_validators_reviewed'] is True and card['execution_authorized'] is False,
         'prerequisite', 'stage applicability scope differs')
    for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                      ('independent_review', E/'INDEPENDENT_SOURCE_REVIEW.json'),
                      ('ri128_source_adjudication', RI128_DECISION), ('history_manifest', HISTORY),
                      ('dependency_manifest', DEPENDENCIES), ('supervisor', SELF), ('target', TARGET), ('interpreter', PYTHON), ('monitor', PS)):
        bind(card[key], path, index)
    for key, expected in (('argv', argv_for(mode)), ('cwd', str(C)), ('environment', ENV), ('limits', LIMITS)):
        same(card[key], expected, 'stage applicability command/envelope differs')


def candidate_prerequisite(index):
    card = read_metadata(E/'CANDIDATE_CUSTODY.json', index)
    exact_keys(card, ('schema', 'whole_bytes_equal', 'scientific_math_accepted', 'replays_admitted',
                      'original', 'copy', 'audit_copy', 'source_stdout', 'saved_addendum', 'root_witness_acceptance'),
               'prerequisite', 'candidate custody')
    need(card['schema'] == 'ri129-exact-candidate-custody-v1' and card['whole_bytes_equal'] is True
         and card['scientific_math_accepted'] is False and card['replays_admitted'] is False,
         'prerequisite', 'candidate custody scope differs')
    for key, path in (('original', E/'CERTIFICATE.json'), ('copy', B/'CERTIFICATE.json'),
                      ('audit_copy', E/'AUDIT_CANDIDATE.json'), ('source_stdout', E/'witness-01'/'stdout.log'),
                      ('saved_addendum', E/'SAVED_CERTIFICATE_ADDENDUM.json'),
                      ('root_witness_acceptance', E/'WITNESS_ROOT_CUSTODY.json')):
        bind(card[key], path, index)
    witness = current(index, E/'witness-01'/'stdout.log')
    need(0 < witness['bytes'] <= 8*1024*1024, 'prerequisite', 'witness candidate size invalid')
    body = (E/'witness-01'/'stdout.log').read_bytes()  # Opaque complete bytes; no scientific JSON decode.
    need(len(body) == witness['bytes'] and sha256(body).hexdigest() == witness['sha256'],
         'identity', 'witness body changed during comparison')
    for path in (E/'CERTIFICATE.json', B/'CERTIFICATE.json', E/'AUDIT_CANDIDATE.json'):
        item = current(index, path)
        need((item['bytes'], item['sha256']) == (witness['bytes'], witness['sha256'])
             and path.read_bytes() == body, 'identity', 'whole candidate differs from genuine witness')


def validate_prerequisites(mode, before):
    index = identity_index(before)
    source_prerequisites(index)
    applicability(mode, index)
    for previous in MODES[:MODES.index(mode)]:
        completed_mode(previous, index)
    if mode != 'witness':
        candidate_prerequisite(index)


def validate_current_target_checks(review):
    checks = review.get('current_target_checks')
    exact_keys(checks, ('sign_fixtures', 'internal_decision_cases', 'intended_first_refusals'),
               'prerequisite', 'completed current-target check counts')
    need(all(type(checks[key]) is int for key in checks)
         and checks == {'sign_fixtures': 15, 'internal_decision_cases': 4,
                        'intended_first_refusals': 71}
         and review.get('current_target_checks_completed') is True
         and review.get('changed_target_qualification_inherited') is False,
         'prerequisite', 'actual current-target checks absent or old qualification credited')


def completed_mode(mode, index):
    """Validate prior *actual* custody; never infer outer success from a receipt."""
    paths = prior_paths(mode)
    receipt = read_metadata(paths['receipt'], index)
    freeze = read_metadata(paths['freeze'], index)
    authorization = read_metadata(paths['authorization'], index)
    applicability(mode, index)
    expected_paths = complete_paths(mode)
    expected_snapshot = {role: {'ok': True, 'identity': current(index, path)}
                         for role, path in expected_paths.items()}
    # Dictionary order is immaterial for receipt snapshots; ordered freeze
    # arrays are separately validated by the retained validator below.
    same(receipt.get('inputs_before'), expected_snapshot, 'prior before/current snapshots differ')
    same(receipt.get('inputs_after'), expected_snapshot, 'prior after/current snapshots differ')
    expected_namespace = runtime_expected_namespace()
    same(receipt.get('runtime_namespace_before'), expected_namespace, 'prior before runtime namespace differs')
    same(receipt.get('runtime_namespace_after'), expected_namespace, 'prior after runtime namespace differs')
    payload = validate_freeze(freeze, mode, expected_snapshot)
    validate_authorization(authorization, freeze, mode, payload, expected_snapshot)
    need(receipt.get('schema') == 'ri84-supervisor-receipt-v1' and receipt.get('mode') == mode
         and receipt.get('success') is True and type(receipt.get('exit_code')) is int
         and receipt['exit_code'] == 0 and receipt.get('input_stability') is True
         and receipt.get('error') is None and receipt.get('cleanup_errors') == []
         and receipt.get('received_signals') == [] and receipt.get('child_end_observed') is True
         and receipt.get('success_requires_supervisor_exit_zero') is True
         and receipt.get('freeze_payload_sha256') == payload,
         'prerequisite', 'prior native success/cleanup/payload differs')
    need(type(receipt.get('pid')) is int and receipt['pid'] > 0
         and type(receipt.get('pgid')) is int and receipt['pgid'] == receipt['pid']
         and type(receipt.get('monitor_attempts')) is int and receipt['monitor_attempts'] > 0
         and type(receipt.get('live_rss_samples')) is int
         and 0 < receipt['live_rss_samples'] <= receipt['monitor_attempts']
         and type(receipt.get('sampled_peak_rss_bytes')) is int
         and 0 < receipt['sampled_peak_rss_bytes'] <= LIMITS['rss_bytes']
         and type(receipt.get('child_elapsed_seconds')) in (int, float)
         and 0 <= receipt['child_elapsed_seconds'] < LIMITS['wall_seconds'],
         'prerequisite', 'prior live sampling, child identity or bounded resources differ')
    for key, expected in (('argv', argv_for(mode)), ('cwd', str(C)), ('environment', ENV), ('limits', LIMITS)):
        same(receipt.get(key), expected, 'prior native command/envelope differs')
    absence = {'original': True, 'copy': True, 'audit_copy': True} if mode == 'witness' else None
    same(receipt.get('witness_certificate_absence_before'), absence, 'prior witness pre-absence differs')
    same(receipt.get('witness_certificate_absence_after'), absence, 'prior witness post-absence differs')
    outputs = {role: current(index, paths[role]) for role in ('stdout', 'stderr', 'samples', 'prepared', 'admission')}
    same(receipt.get('outputs'), outputs, 'prior complete output identities differ')
    prepared = read_metadata(paths['prepared'], index)
    admitted = read_metadata(paths['admission'], index)
    need(prepared.get('schema') == 'ri84-supervisor-prepared-v1' and prepared.get('mode') == mode
         and prepared.get('authorization_granted') is False,
         'prerequisite', 'prior prepared metadata scope differs')
    same(prepared.get('supervisor_argv'), [str(SELF), mode], 'prior outer script argv differs')
    same(prepared.get('supervisor_cwd'), str(C), 'prior outer cwd differs')
    same(prepared.get('paths'), {role: str(path) for role, path in expected_paths.items()},
         'prior prepared role/path closure differs')
    same(prepared.get('observed_inputs'), expected_snapshot, 'prior prepared input identities differ')
    need(admitted.get('schema') == 'ri84-supervisor-admission-v1' and admitted.get('mode') == mode
         and admitted.get('admitted') is True and admitted.get('freeze_payload_sha256') == payload,
         'prerequisite', 'prior launcher admission differs')
    same(admitted.get('observed_inputs'), expected_snapshot, 'prior admission identities differ')
    bind(admitted.get('freeze_identity'), paths['freeze'], index)
    bind(admitted.get('authorization_identity'), paths['authorization'], index)
    for record in (prepared, admitted):
        same(record.get('observed_runtime_namespace'), expected_namespace,
             'prior prepared/admission runtime namespace differs')
        for key, expected in (('argv', argv_for(mode)), ('cwd', str(C)), ('environment', ENV), ('limits', LIMITS),
                              ('witness_certificate_absence', absence)):
            same(record.get(key), expected, 'prior prepared/admission command or absence differs')

    admission = read_metadata(paths['root_admission'], index)
    exact_keys(admission, ('schema', 'status', 'mode', 'source_adjudication', 'applicability', 'freeze',
                           'authorization', 'outer_argv', 'outer_cwd', 'outer_environment', 'outer_invocation',
                           'retry_or_limit_relaxation_authorized', 'history_manifest', 'dependency_manifest'),
               'prerequisite', 'prior root admission')
    need(admission['schema'] == 'ri129-root-stage-admission-v1'
         and admission['status'] == 'ADMITTED_ONE_FROZEN_'+mode.upper()+'_INVOCATION'
         and admission['mode'] == mode and admission['retry_or_limit_relaxation_authorized'] is False,
         'prerequisite', 'prior root admission scope differs')
    for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                      ('applicability', paths['applicability']), ('freeze', paths['freeze']),
                      ('authorization', paths['authorization']), ('history_manifest', HISTORY),
                      ('dependency_manifest', DEPENDENCIES)):
        bind(admission[key], path, index)
    same(admission['outer_argv'], [str(PYTHON), '-I', '-S', '-B', str(SELF), mode],
         'pre-admitted literal outer argv differs')
    same(admission['outer_cwd'], str(C), 'pre-admitted outer cwd differs')
    same(admission['outer_environment'], ENV, 'pre-admitted outer environment differs')
    invocation = admission['outer_invocation']
    need(type(invocation) is dict and invocation.get('workdir') == str(C)
         and type(invocation.get('cmd')) is str and bool(invocation['cmd']),
         'prerequisite', 'actual pre-admitted literal tool invocation absent')

    custody = read_metadata(paths['custody'], index)
    exact_keys(custody, ('schema', 'status', 'mode', 'source_adjudication', 'applicability', 'receipt', 'stdout',
                         'genuine_outer', 'root_complete_review', 'independent_complete_review', 'root_admission',
                         'before_after_current_identities_match', 'terminal_owned_group_absent', 'actual_outer_exit',
                         'actual_outer_chunk_id', 'scientific_math_accepted', 'programme_complete',
                         'root_witness_acceptance', 'root_normal_acceptance', 'candidate_custody',
                         'saved_summary_whole_bytes_equal'), 'prerequisite', 'prior root custody')
    need(custody['schema'] == 'ri129-root-completed-producer-custody-v1'
         and custody['status'] == 'ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY' and custody['mode'] == mode
         and custody['before_after_current_identities_match'] is True
         and custody['terminal_owned_group_absent'] is True
         and type(custody['actual_outer_exit']) is int and custody['actual_outer_exit'] == 0
         and type(custody['actual_outer_chunk_id']) is str and bool(custody['actual_outer_chunk_id'])
         and custody['scientific_math_accepted'] is False and custody['programme_complete'] is False,
         'prerequisite', 'prior root completed custody scope differs')
    for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                      ('applicability', paths['applicability']), ('receipt', paths['receipt']),
                      ('stdout', paths['stdout']), ('genuine_outer', paths['tool_completion']),
                      ('root_complete_review', paths['root_review']),
                      ('independent_complete_review', paths['independent_review']),
                      ('root_admission', paths['root_admission'])):
        bind(custody[key], path, index)
    if mode == 'witness':
        for key in ('root_witness_acceptance', 'root_normal_acceptance', 'candidate_custody',
                    'saved_summary_whole_bytes_equal'):
            need(custody[key] is None, 'prerequisite', 'witness has a premature later-stage dependency')
    else:
        bind(custody['root_witness_acceptance'], E/'WITNESS_ROOT_CUSTODY.json', index)
        bind(custody['candidate_custody'], E/'CANDIDATE_CUSTODY.json', index)
        if mode == 'normal':
            need(custody['root_normal_acceptance'] is None and custody['saved_summary_whole_bytes_equal'] is None,
                 'prerequisite', 'normal has a premature optimized prerequisite')
        else:
            bind(custody['root_normal_acceptance'], E/'NORMAL_ROOT_CUSTODY.json', index)
            need(custody['saved_summary_whole_bytes_equal'] is True,
                 'prerequisite', 'optimized whole-summary equality missing')
            need((E/'normal-01'/'stdout.log').read_bytes() == paths['stdout'].read_bytes(),
                 'identity', 'normal/optimized whole saved summaries differ')

    outer = read_metadata(paths['tool_completion'], index)
    exact_keys(outer, ('record_type', 'source', 'invocation', 'result'), 'prerequisite', 'genuine outer completion')
    need(outer['record_type'] == 'transcription_of_genuine_exec_command_result'
         and outer['source'] == 'Coordinator task tool history; actual invocation, not replay or reconstructed success',
         'prerequisite', 'genuine outer provenance labels differ')
    same(outer['invocation'], invocation, 'actual tool invocation differs from pre-admitted literal invocation')
    result = outer['result']
    need(type(result) is dict and type(result.get('exit_code')) is int and result['exit_code'] == 0
         and result.get('chunk_id') == custody['actual_outer_chunk_id'] and 'session_id' not in result
         and type(result.get('output')) is str, 'prerequisite', 'genuine completed outer zero exit absent')
    same(strict_json(result['output'].encode()), {
        'mode': mode, 'success': True, 'receipt': str(paths['receipt']),
        'receipt_sha256': current(index, paths['receipt'])['sha256']},
        'genuine outer message does not bind exact successful receipt')
    expected_outputs = {filename: current(index, E/(mode+'-01')/filename) for filename in EVIDENCE_NAMES}
    for role, schema, status in (
            ('root_review', 'ri129-root-completed-mode-review-v1',
             'PASS_COMPLETED_'+mode.upper()+'_CUSTODY_PENDING_INDEPENDENT_REVIEW'),
            ('independent_review', 'ri129-independent-completed-mode-review-v1',
             'PASS_COMPLETED_'+mode.upper()+'_CUSTODY_ONLY')):
        review = read_metadata(paths[role], index)
        need(review.get('schema') == schema and review.get('status') == status and review.get('mode') == mode
             and review.get('blocking_findings') == []
             and review.get('before_after_current_identities_match') is True
             and review.get('terminal_owned_group_absent') is True
             and review.get('native_arithmetic_recomputed') is False
             and review.get('native_mathematics_accepted') is False and review.get('programme_complete') is False,
             'prerequisite', 'completed independent/root review scope differs')
        validate_current_target_checks(review)
        for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                          ('applicability', paths['applicability']), ('genuine_outer', paths['tool_completion']),
                          ('root_admission', paths['root_admission']), ('freeze', paths['freeze']),
                          ('authorization', paths['authorization']), ('receipt', paths['receipt'])):
            bind(review.get(key), path, index)
        same(review.get('outputs'), expected_outputs, 'completed review output closure differs')


def validate_freeze(config, mode, before):
    exact_keys(config, ('schema', 'mode', 'supervisor_sha256', 'supervisor', 'argv', 'cwd', 'environment', 'limits',
                        'authorization', 'inputs', 'interpreter', 'attempt_dir'), 'configuration', 'freeze')
    need(config['schema'] == 'ri84-supervisor-freeze-v1' and config['mode'] == mode,
         'configuration', 'freeze schema or mode mismatch')
    need(canonical(config['argv']) == canonical(argv_for(mode)) and config['cwd'] == str(C)
         and canonical(config['environment']) == canonical(ENV)
         and canonical(config['limits']) == canonical(LIMITS)
         and config['attempt_dir'] == str(E/(mode+'-01')), 'configuration', 'fixed command or envelope changed')
    need(hexhash(config['supervisor_sha256'])
         and observed(before, 'supervisor')['sha256'] == config['supervisor_sha256'],
         'identity', 'supervisor byte pin mismatch')
    exact_keys(config['supervisor'], ('path', 'identity'), 'configuration', 'supervisor')
    need(config['supervisor']['path'] == str(SELF), 'configuration', 'supervisor path changed')
    validate_identity(config['supervisor']['identity'], SELF)
    need(canonical(observed(before, 'supervisor')) == canonical(config['supervisor']['identity']),
         'identity', 'supervisor byte or symlink identity mismatch')
    paths = input_paths(mode)
    need(type(config['inputs']) is list and len(config['inputs']) == len(paths), 'configuration', 'input inventory mismatch')
    need([item.get('role') for item in config['inputs'] if type(item) is dict] == list(paths),
         'configuration', 'input role order mismatch')
    for item, (role, path) in zip(config['inputs'], paths.items()):
        exact_keys(item, ('role', 'path', 'identity'), 'configuration', 'input')
        need(item['path'] == str(path), 'configuration', 'input path changed: '+role)
        validate_identity(item['identity'], path)
        actual = observed(before, role)
        need(canonical(actual) == canonical(item['identity']), 'identity', 'input pin mismatch: '+role)
    for role, expected in ACCEPTED.items():
        for suffix in ('_original', '_copy'):
            need(observed(before, role+suffix)['sha256'] == expected, 'identity', 'accepted source changed: '+role+suffix)
    exact_keys(config['interpreter'], ('path', 'identity'), 'configuration', 'interpreter')
    need(config['interpreter']['path'] == str(PYTHON), 'configuration', 'interpreter path changed')
    validate_identity(config['interpreter']['identity'], PYTHON)
    need(canonical(observed(before, 'interpreter')) == canonical(config['interpreter']['identity']),
         'identity', 'interpreter identity mismatch')
    auth = config['authorization']
    exact_keys(auth, ('path', 'sha256'), 'authorization', 'authorization reference')
    need(auth['path'] == str(E/(mode.upper()+'_AUTHORIZATION.json')) and hexhash(auth['sha256']),
         'authorization', 'explicit pinned authorization absent')
    need(observed(before, 'authorization')['sha256'] == auth['sha256'], 'authorization', 'authorization pin mismatch')
    return digest({key: value for key, value in config.items() if key != 'authorization'})


def validate_authorization(auth, config, mode, payload_hash, before):
    exact_keys(auth, ('schema', 'authorized', 'mode', 'freeze_payload_sha256', 'supervisor_sha256', 'addendum_sha256'),
               'authorization', 'authorization')
    need(auth['schema'] == 'ri84-execution-authorization-v1' and auth['authorized'] is True
         and auth['mode'] == mode and auth['freeze_payload_sha256'] == payload_hash
         and auth['supervisor_sha256'] == config['supervisor_sha256'], 'authorization', 'authorization does not bind this attempt')
    if mode == 'witness':
        need(auth['addendum_sha256'] is None, 'authorization', 'witness authorization has a saved-certificate addendum')
        return
    expected_addendum = observed(before, 'certificate_addendum')['sha256']
    need(auth['addendum_sha256'] == expected_addendum, 'authorization', 'saved-certificate addendum pin mismatch')
    addendum = read_metadata(E/'SAVED_CERTIFICATE_ADDENDUM.json', identity_index(before), allow_floats=False)
    exact_keys(addendum, ('schema', 'authorized_modes', 'supervisor_sha256', 'checker_sha256', 'certificate_sha256',
                         'witness_freeze_payload_sha256', 'witness_receipt_sha256'), 'authorization', 'saved-certificate addendum')
    need(addendum['schema'] == 'ri84-saved-certificate-addendum-v1'
         and canonical(addendum['authorized_modes']) == canonical(['normal', 'optimized'])
         and addendum['supervisor_sha256'] == config['supervisor_sha256']
         and addendum['checker_sha256'] == ACCEPTED['checker']
         and addendum['certificate_sha256'] == observed(before, 'certificate')['sha256']
         and hexhash(addendum['witness_freeze_payload_sha256'])
         and addendum['witness_receipt_sha256'] == observed(before, 'witness_receipt')['sha256'],
         'authorization', 'saved addendum does not bind source certificate and witness')
    receipt = read_metadata(E/'witness-01'/'receipt.json', identity_index(before))
    need(type(receipt) is dict and receipt.get('schema') == 'ri84-supervisor-receipt-v1'
         and receipt.get('mode') == 'witness' and receipt.get('success') is True
         and receipt.get('freeze_payload_sha256') == addendum['witness_freeze_payload_sha256']
         and receipt.get('outputs', {}).get('stdout', {}).get('sha256') == addendum['certificate_sha256'],
         'authorization', 'saved certificate is not the successful authorized witness stdout')


class Attempt:
    def __init__(self, mode):
        self.path = E/(mode+'-01')
        self.stdout = self.stderr = self.samples = None
        self.close_errors = []
        os.mkdir(self.path, 0o700)  # A pre-existing attempt is an unconditional refusal.

    def open_logs(self):
        # All fallible opening/fsync work occurs inside run's finalization guard.
        fsync_directory(E)
        self.stdout = (self.path/'stdout.log').open('xb')
        self.stderr = (self.path/'stderr.log').open('xb')
        self.samples = (self.path/'samples.jsonl').open('xb')
        fsync_directory(self.path)

    def event(self, value):
        self.samples.write((canonical(value)+'\n').encode())
        self.samples.flush()
        os.fsync(self.samples.fileno())

    def close(self):
        for label in ('stdout', 'stderr', 'samples'):
            stream = getattr(self, label)
            if stream is not None and not stream.closed:
                try:
                    stream.flush()
                    os.fsync(stream.fileno())
                except Exception as error:
                    self.close_errors.append(label+': '+repr(error))
                finally:
                    try:
                        stream.close()
                    except Exception as error:
                        self.close_errors.append(label+' close: '+repr(error))


def monitor(proc, attempt, launched, index):
    begin = time.monotonic()
    remaining = LIMITS['wall_seconds']-(begin-launched)
    timeout = min(LIMITS['ps_timeout_ms']/1000, max(0, remaining))
    event = {'event': 'monitor_attempt', 'index': index, 'elapsed_before': begin-launched,
             'argv': [str(PS), '-axo', 'pid=,pgid=,rss='], 'declared_timeout_ms': LIMITS['ps_timeout_ms'],
             'effective_timeout_seconds': timeout,
             'child_poll_before': proc.poll()}
    try:
        need(remaining > 0, 'wall_limit', 'no wall-time budget remains for RSS sampling')
        reply = subprocess.run(event['argv'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=str(C), env=ENV, timeout=timeout,
                               check=False, close_fds=True)
        event.update(returncode=reply.returncode, stdout=reply.stdout.decode('ascii', 'backslashreplace'),
                     stderr=reply.stderr.decode('ascii', 'backslashreplace'))
        need(reply.returncode == 0 and not reply.stderr, 'monitor', 'ps failed or emitted stderr')
        rows, seen = [], set()
        for line in reply.stdout.decode('ascii').splitlines():
            fields = line.split()
            need(len(fields) == 3 and all(field.isdecimal() for field in fields), 'monitor', 'malformed ps sample')
            pid, group, rss = map(int, fields)
            need(pid >= 0 and pid not in seen, 'monitor', 'invalid or duplicate ps pid')
            seen.add(pid)
            if pid == proc.pid:
                need(group == proc.pid, 'monitor', 'owned child escaped its process group')
            if group == proc.pid:
                rows.append({'pid': pid, 'pgid': group, 'rss_kib': rss})
        returncode = proc.poll()
        present = any(row['pid'] == proc.pid for row in rows)
        need(present or returncode is not None, 'monitor', 'live owned child missing from ps sample')
        event.update(owned_rows=rows, owned_rss_bytes=sum(row['rss_kib'] for row in rows)*1024,
                     child_poll=returncode, owned_leader_present=present,
                     terminal_absence=not present and returncode is not None)
        # A ps snapshot taken just before exit may legitimately contain the
        # leader even though the following poll reaps it. Obtain a fresh terminal
        # sample rather than calling that race a leaked process group.
        if event['child_poll_before'] is not None:
            need(not rows, 'monitor', 'owned process group survived its terminal leader')
        elif returncode is not None and not present:
            need(not rows, 'monitor', 'owned descendants survived their terminal leader')
        return event
    except BaseException as error:
        event.update(error=type(error).__name__+': '+str(error))
        if isinstance(error, subprocess.TimeoutExpired):
            event.update(stdout=(error.stdout or b'').decode('ascii', 'backslashreplace'),
                         stderr=(error.stderr or b'').decode('ascii', 'backslashreplace'))
        if isinstance(error, Stop):
            raise
        raise Stop('monitor', 'required RSS monitoring failed: '+str(error)) from error
    finally:
        event['elapsed_after'] = time.monotonic()-launched
        attempt.event(event)


def terminate_owned(proc, attempt, launched):
    event = {'event': 'owned_group_cleanup', 'pid': proc.pid, 'pgid': proc.pid,
             'elapsed': time.monotonic()-launched, 'signal': 'SIGKILL'}
    try:
        os.killpg(proc.pid, signal.SIGKILL)
        event['group_signal'] = 'sent'
    except ProcessLookupError:
        event['group_signal'] = 'already absent'
    except Exception as error:
        event['group_signal'] = type(error).__name__+': '+str(error)
    if proc.poll() is None:
        try:
            proc.kill()
            event['leader_signal'] = 'sent'
        except ProcessLookupError:
            event['leader_signal'] = 'already absent'
    try:
        event['reaped_returncode'] = proc.wait(timeout=1)
    except subprocess.TimeoutExpired:
        event['reap_error'] = 'owned child did not reap within one second'
    attempt.event(event)
    need('reap_error' not in event, 'cleanup', event.get('reap_error', 'cleanup failed'))


def pre_attempt_prerequisites(mode):
    """Read-only full admission preflight; refusal consumes no attempt directory.

    This is a new guard, not inherited qualification. The guarded run repeats
    every check freshly before admission and retains its failure postchecks.
    """
    need(sys.platform == 'darwin', 'configuration', 'this frozen supervisor requires Darwin RSS units')
    need(Path(__file__).absolute() == SELF, 'configuration', 'supervisor path changed')
    need(os.getcwd() == str(C) and dict(os.environ) == ENV, 'configuration', 'fixed outer cwd/environment required')
    need(sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.flags.dont_write_bytecode == 1
         and sys.flags.optimize == 0 and sys.argv == [str(SELF), mode],
         'configuration', 'fixed isolated outer interpreter flags/argv required')
    need(os.path.realpath(sys.executable) == runtime_file_identity(PYTHON)['resolved_path'],
         'configuration', 'actual outer interpreter differs from fixed resolved executable')
    before = snapshot(complete_paths(mode))
    same(runtime_namespace_snapshot(), runtime_expected_namespace(),
         'runtime namespace differs in read-only pre-attempt admission check')
    need(mode != 'witness' or all(certificate_absence().values()),
         'witness_certificate', 'witness mode requires all three new certificates absent')
    index = identity_index(before)
    config = read_metadata(E/(mode.upper()+'_EXECUTION_FREEZE.json'), index, allow_floats=False)
    payload_hash = validate_freeze(config, mode, before)
    validate_authorization(read_metadata(E/(mode.upper()+'_AUTHORIZATION.json'), index, allow_floats=False),
                           config, mode, payload_hash, before)
    validate_prerequisites(mode, before)
    same(snapshot(complete_paths(mode)), before,
         'inputs changed during read-only pre-attempt admission check')
    same(runtime_namespace_snapshot(), runtime_expected_namespace(),
         'runtime namespace changed during read-only pre-attempt admission check')
    need(mode != 'witness' or all(certificate_absence().values()),
         'witness_certificate', 'a new certificate appeared during pre-attempt admission check')


def run(mode):
    global CLOSING, LAUNCHING
    need(type(mode) is str and mode in MODES, 'configuration', 'require exactly one fixed mode: witness, normal, optimized')
    preparation_ready()
    CLOSING, LAUNCHING = False, False
    RECEIVED_SIGNALS.clear()
    pre_attempt_prerequisites(mode)
    attempt = Attempt(mode)
    freeze_path = E/(mode.upper()+'_EXECUTION_FREEZE.json')
    auth_path = E/(mode.upper()+'_AUTHORIZATION.json')
    paths = complete_paths(mode)
    started_at, started = timestamp(), time.monotonic()
    before, after, config, payload_hash = {}, {}, None, None
    namespace_before, namespace_after = {}, {}
    proc, launched, child_ended, exit_code, peak, valid_samples, monitor_attempts = None, None, None, None, 0, 0, 0
    absent_before, absent_after = None, None
    error, cleanup_errors, admission_written = None, [], False
    try:
        before = snapshot(paths)
        namespace_before = runtime_namespace_snapshot()
        absent_before = certificate_absence() if mode == 'witness' else None
        attempt.open_logs()
        need(sys.platform == 'darwin', 'configuration', 'this frozen supervisor requires Darwin RSS units')
        need(Path(__file__).absolute() == SELF, 'configuration', 'supervisor path changed')
        need(os.getcwd() == str(C) and dict(os.environ) == ENV, 'configuration', 'fixed outer cwd/environment required')
        need(sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.flags.dont_write_bytecode == 1
             and sys.flags.optimize == 0 and sys.argv == [str(SELF), mode],
             'configuration', 'fixed isolated outer interpreter flags/argv required')
        need(os.path.realpath(sys.executable) == runtime_file_identity(PYTHON)['resolved_path'],
             'configuration', 'actual outer interpreter differs from fixed resolved executable')
        exclusive_json(attempt.path/'prepared.json', {
            'schema': 'ri84-supervisor-prepared-v1', 'mode': mode, 'started_at': started_at,
            'supervisor_argv': sys.argv, 'supervisor_cwd': os.getcwd(),
            'argv': argv_for(mode), 'cwd': str(C), 'environment': ENV, 'limits': LIMITS,
            'paths': {key: str(path) for key, path in paths.items()}, 'observed_inputs': before,
            'observed_runtime_namespace': namespace_before,
            'witness_certificate_absence': absent_before,
            'authorization_granted': False,
        })
        same(namespace_before, runtime_expected_namespace(), 'runtime namespace differs before admission')
        need(mode != 'witness' or all(absent_before.values()), 'witness_certificate', 'witness mode requires all three new certificates absent')
        config = read_metadata(freeze_path, identity_index(before), allow_floats=False)
        payload_hash = validate_freeze(config, mode, before)
        validate_authorization(read_metadata(auth_path, identity_index(before), allow_floats=False),
                               config, mode, payload_hash, before)
        validate_prerequisites(mode, before)
        # Close read/validation races immediately before durable admission.
        admission_inputs = snapshot(paths)
        admission_namespace = runtime_namespace_snapshot()
        same(admission_namespace, runtime_expected_namespace(), 'runtime namespace changed before admission')
        same(admission_namespace, namespace_before, 'runtime namespace pre-admission observations differ')
        need(canonical(admission_inputs) == canonical(before), 'identity', 'inputs changed before admission')
        need(mode != 'witness' or all(certificate_absence().values()),
             'witness_certificate', 'a new certificate appeared before witness admission')
        exclusive_json(attempt.path/'admission.json', {
            'schema': 'ri84-supervisor-admission-v1', 'mode': mode, 'admitted': True,
            'timestamp': timestamp(), 'freeze_payload_sha256': payload_hash,
            'freeze_identity': observed(before, 'freeze'), 'authorization_identity': observed(before, 'authorization'),
            'argv': argv_for(mode), 'cwd': str(C), 'environment': ENV, 'limits': LIMITS,
            'observed_inputs': admission_inputs,
            'observed_runtime_namespace': admission_namespace,
            'witness_certificate_absence': absent_before,
        })
        admission_written = True
        launched = time.monotonic()
        try:
            # Deferral is only over the handle-assignment window. No signal mask
            # or preexec_fn is inherited by the child. A pending shutdown raises
            # immediately after proc becomes available to finally's cleanup.
            LAUNCHING = True
            try:
                proc = subprocess.Popen(argv_for(mode), cwd=str(C), env=ENV,
                                        stdin=subprocess.DEVNULL, stdout=attempt.stdout, stderr=attempt.stderr,
                                        start_new_session=True, close_fds=True)
            finally:
                LAUNCHING = False
            need(not RECEIVED_SIGNALS, 'signal', 'supervisor received a catchable signal during child launch')
        except Stop:
            raise
        except Exception as failure:
            raise Stop('launch', 'owned child launch failed: '+str(failure)) from failure
        attempt.event({'event': 'launch', 'pid': proc.pid, 'pgid': proc.pid,
                       'elapsed': time.monotonic()-launched, 'timestamp': timestamp()})
        while True:
            need(time.monotonic()-launched < LIMITS['wall_seconds'], 'wall_limit', '120-second child wall limit reached')
            monitor_attempts += 1
            sample = monitor(proc, attempt, launched, monitor_attempts)
            peak = max(peak, sample['owned_rss_bytes'])
            if sample['owned_leader_present']:
                valid_samples += 1
            need(time.monotonic()-launched < LIMITS['wall_seconds'], 'wall_limit', '120-second child wall limit reached')
            need(sample['owned_rss_bytes'] <= LIMITS['rss_bytes'], 'rss_limit', '512-MiB owned-group RSS limit exceeded')
            if sample['child_poll'] is not None:
                exit_code = sample['child_poll']
                attempt.event({'event': 'terminal_poll', 'returncode': exit_code,
                               'elapsed': time.monotonic()-launched, 'terminal_absence': sample['terminal_absence']})
                if sample['terminal_absence']:
                    child_ended = time.monotonic()
                    break
                continue  # Confirm disappearance after a pre-exit ps snapshot.
            remaining = LIMITS['wall_seconds']-(time.monotonic()-launched)
            time.sleep(min(LIMITS['sample_interval_ms']/1000, max(0, remaining)))
        need(valid_samples > 0, 'monitor', 'no live-child RSS sample was obtained')
        need(exit_code == 0, 'child_failure', 'owned child exited nonzero: '+str(exit_code))
    except BaseException as failure:
        error = {'code': failure.code if isinstance(failure, Stop) else 'supervisor_failure',
                 'type': type(failure).__name__, 'message': str(failure)}
    finally:
        cleanup_started = time.monotonic()
        CLOSING = True  # Catchable shutdown signals cannot interrupt durable cleanup.
        if error is not None and proc is not None:
            try:
                terminate_owned(proc, attempt, launched)
            except BaseException as failure:
                cleanup_errors.append(type(failure).__name__+': '+str(failure))
            exit_code = proc.poll()
            if exit_code is not None and child_ended is None:
                child_ended = time.monotonic()
        if not admission_written:
            try:
                exclusive_json(attempt.path/'admission.json', {
                    'schema': 'ri84-supervisor-admission-v1', 'mode': mode, 'admitted': False,
                    'timestamp': timestamp(), 'freeze_payload_sha256': payload_hash, 'error': error,
                })
            except BaseException as failure:
                cleanup_errors.append('admission receipt: '+type(failure).__name__+': '+str(failure))
        attempt.close()
        cleanup_errors.extend(attempt.close_errors)
        after = snapshot(paths)  # Always attempt every post-pin, including on failure.
        namespace_after = runtime_namespace_snapshot()  # Independent complete namespace/host postflight.
        namespace_stable = (canonical(namespace_before) == canonical(namespace_after)
                            and canonical(namespace_after) == canonical(runtime_expected_namespace()))
        if not namespace_stable and error is None:
            error = {'code': 'runtime_namespace_change', 'type': 'Stop',
                     'message': 'fixed runtime namespace or visible host identity changed'}
        absent_after = certificate_absence() if mode == 'witness' else None
        stable = canonical(before) == canonical(after)
        if not stable and error is None:
            error = {'code': 'input_change', 'type': 'Stop', 'message': 'frozen input identities changed during attempt'}
        if mode == 'witness' and not all(absent_after.values()) and error is None:
            error = {'code': 'witness_certificate', 'type': 'Stop', 'message': 'a new certificate appeared during witness attempt'}
        if cleanup_errors and error is None:
            error = {'code': 'cleanup', 'type': 'Stop', 'message': 'durable cleanup did not complete'}
        if RECEIVED_SIGNALS and error is None:
            error = {'code': 'signal', 'type': 'Stop', 'message': 'catchable shutdown signal received during cleanup'}
        output_paths = {'stdout': attempt.path/'stdout.log', 'stderr': attempt.path/'stderr.log',
                        'samples': attempt.path/'samples.jsonl', 'prepared': attempt.path/'prepared.json',
                        'admission': attempt.path/'admission.json'}
        output_snapshot = snapshot(output_paths)
        if not all(item['ok'] is True for item in output_snapshot.values()) and error is None:
            error = {'code': 'output_identity', 'type': 'Stop', 'message': 'an evidence output is unavailable'}
        success = error is None and exit_code == 0 and stable and valid_samples > 0 and not cleanup_errors
        receipt = {
            'schema': 'ri84-supervisor-receipt-v1', 'mode': mode, 'success': success,
            'started_at': started_at, 'completed_at': timestamp(), 'total_elapsed_seconds': time.monotonic()-started,
            'child_elapsed_seconds': None if launched is None or child_ended is None else child_ended-launched,
            'child_end_observed': child_ended is not None,
            'cleanup_elapsed_seconds': time.monotonic()-cleanup_started,
            'argv': argv_for(mode), 'cwd': str(C), 'environment': ENV, 'limits': LIMITS,
            'pid': None if proc is None else proc.pid, 'pgid': None if proc is None else proc.pid,
            'exit_code': exit_code, 'freeze_payload_sha256': payload_hash,
            'monitor_attempts': monitor_attempts, 'live_rss_samples': valid_samples,
            'sampled_peak_rss_bytes': peak, 'input_stability': stable,
            'inputs_before': before, 'inputs_after': after, 'error': error, 'cleanup_errors': cleanup_errors,
            'runtime_namespace_before': namespace_before, 'runtime_namespace_after': namespace_after,
            'witness_certificate_absence_before': absent_before, 'witness_certificate_absence_after': absent_after,
            'received_signals': list(RECEIVED_SIGNALS),
            'outputs': {role: item['identity'] if item['ok'] else item for role, item in output_snapshot.items()},
            'success_requires_supervisor_exit_zero': True,
        }
        exclusive_json(attempt.path/'receipt.json', receipt)
    print(canonical({'mode': mode, 'success': success, 'receipt': str(attempt.path/'receipt.json'),
                     'receipt_sha256': file_identity(attempt.path/'receipt.json')['sha256']}), flush=True)
    return 0 if success and not RECEIVED_SIGNALS else 1


def main():
    need(len(sys.argv) == 2 and sys.argv[1] in MODES, 'configuration', 'require exactly one fixed mode: witness, normal, optimized')
    for signum in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(signum, stop_signal)
    return run(sys.argv[1])


def stop_signal(signum, frame):
    RECEIVED_SIGNALS.append({'signal': signum, 'during_cleanup': CLOSING, 'during_launch': LAUNCHING})
    if not CLOSING and not LAUNCHING:
        raise Stop('signal', 'supervisor received catchable signal '+str(signum))


if __name__ == '__main__':
    try:
        sys.exit(main())
    except BaseException as failure:
        if isinstance(failure, SystemExit):
            raise
        print('SUPERVISOR REFUSAL: '+type(failure).__name__+': '+str(failure), file=sys.stderr, flush=True)
        sys.exit(2)
