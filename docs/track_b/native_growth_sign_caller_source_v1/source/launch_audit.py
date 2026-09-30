#!/usr/bin/env python3
"""RI129 prospective fixed saved-audit caller; source is not admission.

The immutable RI128 target and five premises are never evaluated here. Future
root-created binding, genuine serial custody, source applicability, freeze
and authorization must all be present and coherent before any child launch.
Missing preparation pins or actual future evidence refuse before Attempt.
Retained supervision mechanics are not qualification of changed validators.
No retry, arbitrary target/path discovery, environment or resource override.
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


E = Path('/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0')
C = E/'closure'
B = C/'native_growth_connected_strict_sign_v1'
SOURCE = Path('/Volumes/AI_DATA/development/det-review-evidence/ri128-connected-sign-dvgWLqqv')
ANCESTRY = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx')
PYTHON = Path('/opt/homebrew/bin/python3')
PS = Path('/bin/ps')
SELF = E/'launch_audit.py'
TARGET = B/'audit_saved.py'
AUDIT_BINDING = E/'AUDIT_BINDING.json'
CERTIFICATE = E/'AUDIT_CANDIDATE.json'
CERTIFICATE_ORIGINAL = E/'CERTIFICATE.json'
NATIVE_CANDIDATE = B/'CERTIFICATE.json'
OLD_E = Path('/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx')
HISTORY = OLD_E/'HISTORY_RECONCILIATION.json'
RUNTIME = OLD_E/'RUNTIME_CLOSURE.json'
DEPENDENCIES = E/'SOURCE_DEPENDENCIES.json'
# Authored closed source metadata; this identity confers no execution authority.
DEPENDENCIES_BYTES = 583262
DEPENDENCIES_SHA256 = 'a2ef77a9827ceafaf8e94296ec01389d686f3ce2f68064b23d7a1626343c3d1c'
DEPENDENCY_ENTRIES = None
RUNTIME_BYTES = 2862854
RUNTIME_SHA256 = '35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'
RUNTIME_VALUE, RUNTIME_IDENTITY, RUNTIME_ENTRIES = None, None, None
# Immutable reviewed metadata; an absent or changed manifest refuses preparation.
HISTORY_BYTES = 2170307
HISTORY_SHA256 = 'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'
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
PRODUCER_MODES = ('witness', 'normal', 'optimized')
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'sample_interval_ms': 50, 'ps_timeout_ms': 250}
MODES = ('audit',)
CLOSING, LAUNCHING, RECEIVED_SIGNALS = False, False, []
CANDIDATE_BYTES, CANDIDATE_SHA256 = None, None
BINDING_VALUE, BINDING_IDENTITY, HISTORY_VALUE, HISTORY_IDENTITY = None, None, None, None
HISTORY_ENTRIES = None
METADATA_IDENTITIES = None
ACCEPTED = {role+'_'+suffix: checksum for role, original, copy, count, checksum in PAIRS
            for suffix in ('original', 'copy')}
ACCEPTED['ri128_source_adjudication'] = RI128_DECISION_PIN[1]
# Static review inventory, not an executed suite or a qualification claim.
# Each tuple names the rejecting path and intended invalid condition.
CONTROL_DECLARATIONS = (
    ('runtime-unbound-manifest', 'runtime_prepare', 'preparation', 'runtime metadata pin is missing or placeholder'),
    ('runtime-changed-manifest', 'runtime_prepare', 'runtime', 'runtime metadata bytes differ before parsing'),
    ('runtime-membership-change', 'run', 'identity', 'directory names, kinds or link targets changed'),
    ('runtime-absence-invalid', 'run', 'identity', 'declared absent import alternative now exists'),
    ('runtime-host-drift', 'run', 'identity', 'uname, system version or visible system location differs'),
    ('runtime-file-changed', 'runtime_file_prerequisites', 'identity', 'one captured runtime file changed'),
    ('runtime-late-namespace-change', 'run', 'runtime_namespace_change', 'namespace or host changes after launch'),
    ('unbound-dependency-pin', 'dependency_prepare', 'preparation', 'source dependency manifest pin is missing or placeholder'),
    ('changed-dependency-manifest', 'dependency_prepare', 'dependency', 'source dependency metadata bytes changed before parsing'),
    ('dependency-order-or-duplicate', 'dependency_prepare', 'dependency', 'source dependency order or role is not closed'),
    ('dependency-link-or-alias', 'dependency_prepare', 'dependency', 'source dependency identity is linked or resolved elsewhere'),
    ('changed-source-dependency', 'verify_source_cards', 'identity', 'one complete static source/evidence identity changed'),
    ('old-target-qualification-credit', 'validate_mode_custodies', 'prerequisite', 'completed review lacks current15/4/71 checks or credits old qualification'),
    ('pre-attempt-missing-or-invalid-prerequisite', 'pre_attempt_prerequisites', 'varies-by-failed-prerequisite', 'current freeze/auth or full fixed prerequisite fails before allocation'),
    ('unbound-history', 'preparation_ready', 'preparation', 'history pin is None or placeholder'),
    ('changed-history', 'preparation_ready', 'identity', 'manifest bytes no longer match literal pin'),
    ('missing-binding', 'preparation_ready', 'FileNotFoundError', 'future actual binding does not exist'),
    ('binding-extra-key', 'preparation_ready', 'preparation', 'actual binding has an extra field'),
    ('binding-null-identity', 'positive_identity', 'configuration', 'future identity is null'),
    ('binding-zero-size', 'positive_identity', 'preparation', 'future actual identity has zero size'),
    ('binding-zero-digest', 'positive_identity', 'preparation', 'future actual identity has zero digest'),
    ('binding-arbitrary-path', 'positive_identity', 'configuration', 'a fixed future path is substituted'),
    ('binding-missing-mode', 'preparation_ready', 'preparation', 'one actual custody is omitted'),
    ('binding-changed-after-cache', 'validate_authorization', 'identity', 'binding changes before freeze validation'),
    ('missing-custody', 'preparation_ready', 'FileNotFoundError', 'required genuine completed custody absent'),
    ('history-order', 'preparation_ready', 'configuration', 'protected roles or paths reordered'),
    ('history-duplicate', 'preparation_ready', 'configuration', 'protected literal path repeated'),
    ('history-zero-log-valid', 'validate_identity', None, 'empty historical stderr remains permitted'),
    ('changed-protected-file', 'verify_source_cards', 'identity', 'one historical full identity changes'),
    ('changed-copy', 'verify_source_cards', 'identity', 'one exact scientific source/input copy changes'),
    ('source-decision-extra-field', 'verify_source_cards', 'prerequisite', 'root source decision contains extra key'),
    ('source-decision-promotion', 'verify_source_cards', 'prerequisite', 'source decision grants execution or target qualification'),
    ('source-review-incomplete', 'verify_source_cards', 'prerequisite', 'independent source review has blockers'),
    ('stage-wrong-mode', 'verify_applicability', 'prerequisite', 'applicability names another mode'),
    ('stage-wrong-argv', 'verify_applicability', 'identity', 'applicability changes literal child argv'),
    ('stage-wrong-env-limits', 'verify_applicability', 'identity', 'applicability changes environment or envelope'),
    ('freeze-input-order', 'validate_freeze', 'configuration', 'frozen array differs in order or length'),
    ('freeze-raw-body-mismatch', 'metadata', 'identity', 'parsed freeze bytes differ from snapshot identity'),
    ('authorization-raw-body-mismatch', 'metadata', 'identity', 'parsed authorization bytes differ from snapshot identity'),
    ('runtime-link-change', 'validate_freeze', 'identity', 'runtime literal symlink or bytes differs from freeze'),
    ('missing-explicit-auth', 'validate_authorization', 'authorization', 'root authorization is not exact positive admission'),
    ('target-path-alias', 'validate_authorization', 'identity', 'one of eight fixed target paths is substituted'),
    ('target-physical-alias', 'validate_authorization', 'identity', 'any two of eight target objects share device/inode'),
    ('target-symlink', 'validate_authorization', 'identity', 'a target file or ancestor is a symlink'),
    ('target-oversize', 'validate_authorization', 'identity', 'one target object exceeds eight MiB'),
    ('target-certificate-binding', 'validate_authorization', 'authorization', 'native saved certificate differs from actual binding'),
    ('serial-receipt-only', 'validate_mode_custodies', 'prerequisite', 'receipt claims success without root custody'),
    ('serial-omitted-prior', 'validate_mode_custodies', 'identity', 'optimized omits genuine normal acceptance'),
    ('native-false-zero', 'validate_producer_receipts', 'prerequisite', 'child exit false replaces integer zero'),
    ('native-role-trailer', 'validate_producer_receipts', 'configuration', 'native input array has trailing non-dict'),
    ('native-before-after-change', 'validate_producer_receipts', 'identity', 'retained native snapshots differ from current'),
    ('native-empty-live-samples', 'validate_producer_receipts', 'prerequisite', 'no positive live sample exists'),
    ('native-no-terminal-absence', 'validate_producer_receipts', 'prerequisite', 'last census retains owned processes'),
    ('native-candidate-during-witness', 'validate_producer_receipts', 'identity', 'witness did not preserve candidate absence'),
    ('candidate-partial', 'validate_mode_custodies', 'identity', 'one saved candidate differs in any byte'),
    ('saved-summary-difference', 'validate_mode_custodies', 'identity', 'normal and optimized complete bytes differ'),
    ('outer-wrong-literal-invocation', 'validate_mode_custodies', 'identity', 'actual command differs from pre-admission'),
    ('outer-false-zero', 'validate_mode_custodies', 'prerequisite', 'false replaces genuine integer outer exit zero'),
    ('outer-unfinished-session', 'validate_mode_custodies', 'prerequisite', 'outer completion still has a session id'),
    ('outer-receipt-mismatch', 'validate_mode_custodies', 'identity', 'actual outer message binds a different receipt'),
    ('review-missing-output', 'validate_mode_custodies', 'identity', 'completed review omits one of six outputs'),
    ('metadata-unclosed-reference', 'bind_refs', 'identity', 'decoded metadata names an unclosed identity'),
    ('attempt-reuse', 'Attempt.__init__', 'FileExistsError', 'exclusive audit-01 already exists'),
    ('wrong-launch-environment', 'run', 'configuration', 'outer flags, argv, cwd or exact environment differs'),
    ('monitor-failure', 'monitor', 'monitor', 'required census is malformed, nonzero or timed out'),
    ('wall-limit', 'run', 'wall_limit', 'owned child reaches 120-second bound'),
    ('rss-limit', 'run', 'rss_limit', 'sampled owned group exceeds 512 MiB'),
    ('late-input-change', 'run', 'input_change', 'post-admission input byte or link identity changes'),
    ('late-signal', 'run', 'signal', 'catchable interruption invalidates apparent completion'),
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



def metadata(path, expected=None, allow_floats=True):
    """Read only fixed custody JSON, never a scientific payload body."""
    if expected is None:
        if METADATA_IDENTITIES is not None:
            need(str(path) in METADATA_IDENTITIES, 'identity', 'metadata outside frozen input closure')
            expected = METADATA_IDENTITIES[str(path)]
        else:
            expected = file_identity(path)
    need(type(expected.get('bytes')) is int and 0 < expected['bytes'] <= 64*1024*1024,
         'configuration', 'expected metadata size outside fixed domain')
    raw = path.read_bytes()
    need(0 < len(raw) <= 64*1024*1024, 'configuration', 'metadata size outside fixed domain')
    need(len(raw) == expected['bytes'] and sha256(raw).hexdigest() == expected['sha256'],
         'identity', 'metadata raw bytes differ from authenticated identity')
    same(file_identity(path), expected, 'metadata literal links or identity changed during read')
    value = strict_json(raw, allow_floats=allow_floats)
    need(type(value) is dict, 'configuration', 'metadata must be a JSON object')
    return value


def same(left, right, context):
    need(canonical(left) == canonical(right), 'identity', context)


def positive_identity(value, path):
    validate_identity(value, path)
    need(value['bytes'] > 0 and value['sha256'] != '0'*64,
         'preparation', 'nonpositive or placeholder identity: '+str(path))


def mode_paths(name):
    need(name in PRODUCER_MODES, 'configuration', 'unknown fixed producer mode')
    result = {}
    for role, filename in (('receipt', 'receipt.json'), ('stdout', 'stdout.log'),
                           ('stderr', 'stderr.log'), ('samples', 'samples.jsonl'),
                           ('prepared', 'prepared.json'), ('admission', 'admission.json')):
        result[name+'_'+role] = E/(name+'-01')/filename
    for role, suffix in (('freeze', 'EXECUTION_FREEZE.json'), ('authorization', 'AUTHORIZATION.json'),
                         ('root_admission', 'ROOT_ADMISSION.json'), ('tool_completion', 'OUTER_TOOL_RESULT.json'),
                         ('root_review', 'ROOT_COMPLETE_REVIEW.json'), ('independent_review', 'INDEPENDENT_COMPLETE_REVIEW.json'),
                         ('custody', 'ROOT_CUSTODY.json'), ('applicability', 'APPLICABILITY.json')):
        result[name+'_'+role] = E/(name.upper()+'_'+suffix)
    return result


def base_paths(mode):
    need(mode in (*PRODUCER_MODES, 'audit') and HISTORY_ENTRIES is not None,
         'preparation', 'fixed stage or authenticated history unavailable')
    result = {}
    for role, original, copy, count, checksum in PAIRS:
        result[role+'_original'] = original
        result[role+'_copy'] = copy
    result.update(monitor=PS, history_manifest=HISTORY, runtime_manifest=RUNTIME,
                  dependency_manifest=DEPENDENCIES)
    for item in RUNTIME_ENTRIES:
        need(item['role'] not in result, 'runtime', 'runtime role collision')
        result[item['role']] = Path(item['path'])
    for item in HISTORY_ENTRIES:
        need(item['role'] not in result, 'configuration', 'historical role collision')
        result[item['role']] = Path(item['path'])
    for item in DEPENDENCY_ENTRIES:
        need(item['role'] not in result, 'dependency', 'source dependency role collision')
        result[item['role']] = Path(item['path'])
    result.update(audit_caller=SELF, caller_contract=E/'CALLER_CONTRACT.md',
                  source_adjudication=E/'ROOT_SOURCE_ADJUDICATION.json',
                  independent_source_review=E/'INDEPENDENT_SOURCE_REVIEW.json',
                  ri128_source_adjudication=RI128_DECISION,
                  mode_applicability=E/(mode.upper()+'_APPLICABILITY.json'))
    return result


def native_paths(mode):
    result = base_paths(mode)
    if mode != 'witness':
        result.update(certificate_original=CERTIFICATE_ORIGINAL, certificate=NATIVE_CANDIDATE,
                      audit_candidate=CERTIFICATE, certificate_addendum=E/'SAVED_CERTIFICATE_ADDENDUM.json',
                      candidate_custody=E/'CANDIDATE_CUSTODY.json')
    for name in PRODUCER_MODES[:PRODUCER_MODES.index(mode)]:
        result.update(mode_paths(name))
    return result


def input_paths(mode):
    need(mode == 'audit', 'configuration', 'fixed audit input mode changed')
    result = base_paths(mode)
    result.update(certificate_original=CERTIFICATE_ORIGINAL, certificate=NATIVE_CANDIDATE,
                  audit_candidate=CERTIFICATE, certificate_addendum=E/'SAVED_CERTIFICATE_ADDENDUM.json',
                  candidate_custody=E/'CANDIDATE_CUSTODY.json')
    for name in PRODUCER_MODES:
        result.update(mode_paths(name))
    result.update(audit_binding=AUDIT_BINDING, native_supervisor=E/'supervise.py')
    return result


def runtime_canonical_path(value):
    need(type(value) is str and Path(value).is_absolute()
         and os.path.normpath(value) == value, 'runtime', 'noncanonical runtime path')
    return value


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
    same(file_identity(DEPENDENCIES), identity, 'source dependency manifest changed during preparation')
    DEPENDENCY_ENTRIES = tuple(entries)


def preparation_ready():
    """Authenticate and cache genuine future bindings before Attempt allocation."""
    global CANDIDATE_BYTES, CANDIDATE_SHA256
    global BINDING_VALUE, BINDING_IDENTITY, HISTORY_VALUE, HISTORY_IDENTITY, HISTORY_ENTRIES
    dependency_prepare()
    runtime_prepare()
    if BINDING_VALUE is not None:
        return  # The launch and cleanup argv never follow a subsequently changed card.
    need(type(HISTORY_BYTES) is int and HISTORY_BYTES > 0 and hexhash(HISTORY_SHA256)
         and HISTORY_SHA256 != '0'*64, 'preparation', 'reviewed historical manifest pin is unbound')
    manifest_id = file_identity(HISTORY)
    need(manifest_id['bytes'] == HISTORY_BYTES and manifest_id['sha256'] == HISTORY_SHA256,
         'identity', 'reviewed historical manifest changed')
    history = metadata(HISTORY, manifest_id)
    need(history.get('schema') == 'ri122-native-history-reconciliation-v1'
         and history.get('status') == 'SOURCE_ONLY_CURRENT_CUSTODY_CANDIDATE'
         and type(history.get('protected_files')) is list and bool(history['protected_files']),
         'configuration', 'closed historical manifest schema changed')
    entries, seen = history['protected_files'], set()
    for index, item in enumerate(entries, 1):
        exact_keys(item, ('role', 'path', 'identity', 'classification', 'access_policy', 'reference_provenance'),
                   'configuration', 'protected historical entry')
        need(item['role'] == 'hist_'+str(index).zfill(4)
             and type(item['path']) is str and item['path'] not in seen,
             'configuration', 'historical ordered role or path changed')
        validate_identity(item['identity'], Path(item['path']))
        need(Path(item['path']).is_absolute() and os.path.normpath(item['path']) == item['path']
             and type(item['classification']) is str and bool(item['classification'])
             and type(item['access_policy']) is str and bool(item['access_policy'])
             and type(item['reference_provenance']) is list,
             'configuration', 'historical entry provenance or canonical path differs')
        seen.add(item['path'])
    need([item['path'] for item in entries] == sorted(seen),
         'configuration', 'historical literal path order changed')
    HISTORY_VALUE, HISTORY_IDENTITY, HISTORY_ENTRIES = history, manifest_id, entries
    binding_id = file_identity(AUDIT_BINDING)
    positive_identity(binding_id, AUDIT_BINDING)
    binding = metadata(AUDIT_BINDING, binding_id)
    exact_keys(binding, ('schema', 'status', 'audit_admitted', 'candidates', 'custodies',
                        'outer_completions', 'candidate_custody', 'source_adjudication',
                        'ri128_source_adjudication', 'history_manifest', 'dependency_manifest'), 'preparation', 'actual audit binding')
    need(binding['schema'] == 'ri129-actual-three-mode-audit-binding-v1'
         and binding['status'] == 'ACCEPT_COMPLETED_THREE_MODE_CUSTODY_FOR_SOURCE_BINDING_ONLY'
         and binding['audit_admitted'] is False, 'preparation', 'actual audit binding scope differs')
    refs = [(binding['candidate_custody'], E/'CANDIDATE_CUSTODY.json'),
            (binding['source_adjudication'], E/'ROOT_SOURCE_ADJUDICATION.json'),
            (binding['ri128_source_adjudication'], RI128_DECISION),
            (binding['history_manifest'], HISTORY), (binding['dependency_manifest'], DEPENDENCIES)]
    exact_keys(binding['candidates'], ('original', 'native', 'audit'), 'preparation', 'candidate binding')
    for key, path in (('original', CERTIFICATE_ORIGINAL), ('native', NATIVE_CANDIDATE), ('audit', CERTIFICATE)):
        refs.append((binding['candidates'][key], path))
    for group, suffix in (('custodies', 'ROOT_CUSTODY.json'), ('outer_completions', 'OUTER_TOOL_RESULT.json')):
        exact_keys(binding[group], PRODUCER_MODES, 'preparation', group)
        for name in PRODUCER_MODES:
            refs.append((binding[group][name], E/(name.upper()+'_'+suffix)))
    for item, path in refs:
        positive_identity(item, path)
        same(item, file_identity(path), 'actual future binding reference changed: '+str(path))
    for role, path in input_paths('audit').items():
        resolved, links = resolve_links(path)
        need(stat.S_ISREG(resolved.stat().st_mode), 'preparation', 'required actual input unavailable: '+role)
    CANDIDATE_BYTES = binding['candidates']['native']['bytes']
    CANDIDATE_SHA256 = binding['candidates']['native']['sha256']
    need(CANDIDATE_BYTES <= 8388608,
         'preparation', 'native saved candidate outside accepted byte ceiling')
    BINDING_IDENTITY, BINDING_VALUE = binding_id, binding


def argv_for(mode):
    preparation_ready()
    need(mode == 'audit', 'configuration', 'fixed no-argument audit mode changed')
    return [str(PYTHON), '-I', '-S', '-B', str(TARGET)]


def native_argv(mode):
    need(mode in PRODUCER_MODES, 'configuration', 'native mode changed')
    result = [str(PYTHON), '-I', '-S', '-B']
    if mode == 'optimized':
        result.append('-O')
    result.append(str(B/'check.py'))
    if mode == 'witness':
        result.append('--witness')
    return result

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


def validate_freeze(config, mode, before):
    exact_keys(config, ('schema', 'mode', 'supervisor_sha256', 'supervisor', 'argv', 'cwd', 'environment', 'limits',
                        'authorization', 'inputs', 'interpreter', 'attempt_dir'), 'configuration', 'freeze')
    need(config['schema'] == 'ri95-certificate-audit-freeze-v1' and config['mode'] == mode,
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
        need(observed(before, role)['sha256'] == expected, 'identity', 'accepted source changed: '+role)
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



def refmap(before):
    result = {}
    for role in before:
        item = observed(before, role)
        if item['path'] in result:
            same(item, result[item['path']], 'aliased frozen identities disagree')
        result[item['path']] = item
    return result


def bind_refs(value, known):
    """Check references in already selected metadata; never follow files."""
    if type(value) is list:
        for item in value:
            bind_refs(item, known)
    elif type(value) is dict:
        if all(key in value for key in ('path', 'bytes', 'sha256')):
            need(type(value['path']) is str and value['path'] in known,
                 'identity', 'metadata reference outside closed frozen inventory')
            actual = known[value['path']]
            for key in ('path', 'bytes', 'sha256', 'resolved_path', 'symlinks'):
                if key in value:
                    same(value[key], actual[key], 'metadata reference changed: '+value['path'])
        for item in value.values():
            bind_refs(item, known)


def require_ref(value, path, known, positive=True):
    need(str(path) in known, 'identity', 'required path outside frozen inventory')
    if positive:
        positive_identity(value, path)
    else:
        validate_identity(value, path)
    same(value, known[str(path)], 'full current reference differs: '+str(path))


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


def verify_source_cards(before, known):
    runtime_file_prerequisites(known)
    for role, original, copy, count, checksum in PAIRS:
        for suffix in ('original', 'copy'):
            item = observed(before, role+'_'+suffix)
            need(item['bytes'] == count and item['sha256'] == checksum,
                 'identity', 'accepted RI128 pair changed: '+role+'/'+suffix)
        need(original.read_bytes() == copy.read_bytes(), 'identity', 'whole source copy differs: '+role)
    item = observed(before, 'ri128_source_adjudication')
    need((item['bytes'], item['sha256']) == RI128_DECISION_PIN, 'identity', 'accepted RI128 source decision changed')
    accepted = metadata(RI128_DECISION)
    validate_ri128_source_decision(accepted)
    bind_refs(accepted, known)
    for item in HISTORY_ENTRIES:
        same(observed(before, item['role']), item['identity'], 'historical protected identity changed')
    same(observed(before, 'history_manifest'), HISTORY_IDENTITY, 'historical manifest changed after caching')
    for item in DEPENDENCY_ENTRIES:
        same(observed(before, item['role']), item['identity'], 'static source dependency identity changed')
    dependency_id = observed(before, 'dependency_manifest')
    need((dependency_id['bytes'], dependency_id['sha256']) == (DEPENDENCIES_BYTES, DEPENDENCIES_SHA256),
         'dependency', 'source dependency manifest pin differs')
    sources = {'native_supervisor': known[str(E/'supervise.py')],
               'audit_caller': known[str(SELF)], 'history_manifest': known[str(HISTORY)],
               'runtime_manifest': known[str(RUNTIME)],
               'caller_contract': known[str(E/'CALLER_CONTRACT.md')],
               'dependency_manifest': known[str(DEPENDENCIES)]}
    decision = metadata(E/'ROOT_SOURCE_ADJUDICATION.json')
    exact_keys(decision, ('schema', 'status', 'accepted_sources', 'independent_review',
                         'ri128_source_adjudication', 'history_manifest', 'dependency_manifest', 'execution_authorized',
                         'qualification_transferred_to_changed_targets'), 'prerequisite', 'RI129 source decision')
    need(decision['schema'] == 'ri129-root-caller-source-adjudication-v1'
         and decision['status'] == 'ACCEPT_EXACT_NATIVE_CALLER_SOURCE_ONLY'
         and decision['execution_authorized'] is False
         and decision['qualification_transferred_to_changed_targets'] is False,
         'prerequisite', 'RI129 source decision is not exact source-only acceptance')
    same(decision['accepted_sources'], sources, 'RI129 accepted source set differs')
    for key, path in (('independent_review', E/'INDEPENDENT_SOURCE_REVIEW.json'),
                      ('ri128_source_adjudication', RI128_DECISION), ('history_manifest', HISTORY),
                      ('dependency_manifest', DEPENDENCIES)):
        require_ref(decision[key], path, known)
    review = metadata(E/'INDEPENDENT_SOURCE_REVIEW.json')
    need(review.get('schema') == 'ri129-independent-complete-caller-source-review-v1'
         and review.get('status') == 'PASS_COMPLETE_SOURCE_REVIEW_ONLY'
         and review.get('blocking_findings') == [] and review.get('scientific_execution') is False
         and review.get('execution_authorized') is False,
         'prerequisite', 'complete independent source review absent')
    same(review.get('sources'), sources, 'independent source set differs')
    for doc in (decision, review):
        bind_refs(doc, known)


def verify_applicability(name, known):
    path = E/(name.upper()+'_APPLICABILITY.json')
    card = metadata(path)
    exact_keys(card, ('schema', 'status', 'mode', 'source_adjudication', 'independent_review',
                     'ri128_source_adjudication', 'history_manifest', 'dependency_manifest', 'supervisor', 'target',
                     'interpreter', 'monitor', 'argv', 'cwd', 'environment', 'limits',
                     'retained_engine_only', 'changed_target_qualification_inherited',
                     'changed_validators_reviewed', 'execution_authorized'),
               'prerequisite', 'stage applicability')
    need(card['schema'] == 'ri129-stage-applicability-v1'
         and card['status'] == 'ACCEPT_PRECISE_FIXED_STAGE_APPLICABILITY_ONLY'
         and card['mode'] == name and card['retained_engine_only'] is True
         and card['changed_target_qualification_inherited'] is False
         and card['changed_validators_reviewed'] is True and card['execution_authorized'] is False,
         'prerequisite', 'fixed stage applicability scope differs: '+name)
    for key, target in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                        ('independent_review', E/'INDEPENDENT_SOURCE_REVIEW.json'),
                        ('ri128_source_adjudication', RI128_DECISION), ('history_manifest', HISTORY),
                        ('dependency_manifest', DEPENDENCIES), ('supervisor', SELF if name == 'audit' else E/'supervise.py'),
                        ('target', TARGET if name == 'audit' else B/'check.py'),
                        ('interpreter', PYTHON), ('monitor', PS)):
        require_ref(card[key], target, known)
    same(card['argv'], argv_for('audit') if name == 'audit' else native_argv(name), 'stage argv differs')
    need(card['cwd'] == str(C), 'prerequisite', 'stage cwd differs')
    same(card['environment'], ENV, 'stage environment differs')
    same(card['limits'], LIMITS, 'stage resource envelope differs')
    bind_refs(card, known)


def validate_authorization(auth, config, mode, payload_hash, before):
    global METADATA_IDENTITIES
    exact_keys(auth, ('schema', 'authorized', 'mode', 'freeze_payload_sha256', 'supervisor_sha256'),
               'authorization', 'authorization')
    need(auth['schema'] == 'ri95-certificate-audit-authorization-v1' and auth['authorized'] is True
         and auth['mode'] == mode and auth['freeze_payload_sha256'] == payload_hash
         and auth['supervisor_sha256'] == config['supervisor_sha256'],
         'authorization', 'authorization does not bind this one audit attempt')
    known = refmap(before)
    METADATA_IDENTITIES = known
    same(observed(before, 'audit_binding'), BINDING_IDENTITY, 'actual binding changed after preparation')
    same(metadata(AUDIT_BINDING), BINDING_VALUE, 'actual binding body changed after preparation')
    bind_refs(BINDING_VALUE, known)
    # The accepted RI128 consumer takes no descriptor or operands. Protect its
    # exact eight sibling objects, independently of the larger outer inventory.
    target_roles = ('auditor_copy', 'checker_copy', 'ri88_copy', 'ri88_root_copy',
                    'ri122_root_copy', 'ri124_root_copy', 'ri127_root_copy', 'certificate')
    target_paths = (TARGET, B/'check.py', B/'inputs'/'ri88.json',
                    B/'inputs'/'ri88_root.json', B/'inputs'/'ri122_root.json',
                    B/'inputs'/'ri124_root.json', B/'inputs'/'ri127_root.json', NATIVE_CANDIDATE)
    need(len(set(target_paths)) == 8, 'configuration', 'eight target paths must be distinct')
    physical = set()
    for role, path in zip(target_roles, target_paths):
        item = observed(before, role)
        need(item['path'] == str(path) and type(item['bytes']) is int
             and 0 < item['bytes'] <= 8388608 and item['sha256'] != '0'*64
             and not item['symlinks'] and item['path'] == item['resolved_path'],
             'identity', 'target object must be positive bounded literal nonsymlink file: '+role)
        # Full component traversal is authenticated by file_identity; the lstat
        # device/inode guard additionally rejects same-physical-file aliases.
        identity = os.stat(item['path'], follow_symlinks=False)
        need(stat.S_ISREG(identity.st_mode), 'identity', 'target object is not regular: '+role)
        key = (identity.st_dev, identity.st_ino)
        need(key not in physical, 'identity', 'target objects share a physical identity: '+role)
        physical.add(key)
        same(file_identity(path), item, 'target object changed during physical alias guard')
    need(observed(before, 'certificate')['bytes'] == CANDIDATE_BYTES
         and observed(before, 'certificate')['sha256'] == CANDIDATE_SHA256,
         'authorization', 'actual native saved certificate differs from audit binding')
    verify_source_cards(before, known)
    verify_applicability('audit', known)
    validate_producer_receipts(before)
    validate_mode_custodies(before)


def validate_producer_receipts(before):
    """Reconcile all native evidence; outer-tool truth is checked separately."""
    known = refmap(before)
    supervisor_id = known[str(E/'supervise.py')]
    for name in PRODUCER_MODES:
        paths = mode_paths(name)
        read = lambda suffix: metadata(paths[name+'_'+suffix])
        receipt, freeze, auth = read('receipt'), read('freeze'), read('authorization')
        need(receipt.get('schema') == 'ri84-supervisor-receipt-v1'
             and receipt.get('mode') == name and receipt.get('success') is True
             and type(receipt.get('exit_code')) is int and receipt['exit_code'] == 0
             and receipt.get('input_stability') is True and receipt.get('error') is None
             and receipt.get('cleanup_errors') == [] and receipt.get('received_signals') == []
             and receipt.get('child_end_observed') is True
             and receipt.get('success_requires_supervisor_exit_zero') is True
             and type(receipt.get('live_rss_samples')) is int and receipt['live_rss_samples'] > 0,
             'prerequisite', 'successful native completion absent: '+name)
        need(type(receipt.get('pid')) is int and receipt['pid'] > 0
             and type(receipt.get('pgid')) is int and receipt['pgid'] == receipt['pid']
             and type(receipt.get('monitor_attempts')) is int and receipt['monitor_attempts'] > 0
             and type(receipt.get('sampled_peak_rss_bytes')) is int
             and 0 < receipt['sampled_peak_rss_bytes'] <= LIMITS['rss_bytes']
             and type(receipt.get('child_elapsed_seconds')) in (int, float)
             and 0 <= receipt['child_elapsed_seconds'] < LIMITS['wall_seconds'],
             'prerequisite', 'native runtime completion evidence differs')
        exact_keys(freeze, ('schema', 'mode', 'supervisor_sha256', 'supervisor', 'argv', 'cwd', 'environment', 'limits',
                            'authorization', 'inputs', 'interpreter', 'attempt_dir'), 'configuration', 'native freeze')
        need(freeze['schema'] == 'ri84-supervisor-freeze-v1' and freeze['mode'] == name
             and freeze['attempt_dir'] == str(E/(name+'-01'))
             and freeze['supervisor_sha256'] == supervisor_id['sha256'],
             'prerequisite', 'native freeze source/mode differs')
        for value in (freeze, receipt):
            same(value.get('argv'), native_argv(name), 'native fixed argv differs')
            need(value.get('cwd') == str(C), 'prerequisite', 'native cwd differs')
            same(value.get('environment'), ENV, 'native exact environment differs')
            same(value.get('limits'), LIMITS, 'native envelope differs')
        for key, path in (('supervisor', E/'supervise.py'), ('interpreter', PYTHON)):
            exact_keys(freeze[key], ('path', 'identity'), 'configuration', 'native '+key)
            need(freeze[key]['path'] == str(path), 'identity', 'native runtime path differs')
            require_ref(freeze[key]['identity'], path, known)
        payload = digest({key: value for key, value in freeze.items() if key != 'authorization'})
        exact_keys(auth, ('schema', 'authorized', 'mode', 'freeze_payload_sha256', 'supervisor_sha256', 'addendum_sha256'),
                   'authorization', 'native authorization')
        need(auth['schema'] == 'ri84-execution-authorization-v1' and auth['authorized'] is True
             and auth['mode'] == name and auth['supervisor_sha256'] == supervisor_id['sha256']
             and auth['freeze_payload_sha256'] == payload and receipt.get('freeze_payload_sha256') == payload
             and auth['addendum_sha256'] == (None if name == 'witness' else known[str(E/'SAVED_CERTIFICATE_ADDENDUM.json')]['sha256']),
             'authorization', 'native explicit authorization/payload differs')
        same(freeze['authorization'], {'path': str(paths[name+'_authorization']),
                                      'sha256': known[str(paths[name+'_authorization'])]['sha256']},
             'native authorization identity differs')
        expected_paths = native_paths(name)
        need(type(freeze['inputs']) is list and len(freeze['inputs']) == len(expected_paths)
             and [item.get('role') for item in freeze['inputs'] if type(item) is dict] == list(expected_paths),
             'configuration', 'native complete ordered input list differs')
        complete_paths = dict(expected_paths, interpreter=PYTHON, supervisor=E/'supervise.py',
                              freeze=paths[name+'_freeze'], authorization=paths[name+'_authorization'])
        expected_snapshot = {role: {'ok': True, 'identity': known[str(path)]} for role, path in complete_paths.items()}
        same(receipt.get('inputs_before'), expected_snapshot, 'native before/current identity map differs')
        same(receipt.get('inputs_after'), expected_snapshot, 'native after/current identity map differs')
        expected_namespace = runtime_expected_namespace()
        same(receipt.get('runtime_namespace_before'), expected_namespace, 'native before runtime namespace differs')
        same(receipt.get('runtime_namespace_after'), expected_namespace, 'native after runtime namespace differs')
        for item, (role, path) in zip(freeze['inputs'], expected_paths.items()):
            exact_keys(item, ('role', 'path', 'identity'), 'configuration', 'native input entry')
            need(item['role'] == role and item['path'] == str(path), 'configuration', 'native ordered role/path differs')
            require_ref(item['identity'], path, known, positive=False)
        output_paths = {role: paths[name+'_'+role] for role in ('stdout', 'stderr', 'samples', 'prepared', 'admission')}
        same(receipt.get('outputs'), {role: known[str(path)] for role, path in output_paths.items()},
             'native complete output identity set differs')
        prepared, admitted = read('prepared'), read('admission')
        need(prepared.get('schema') == 'ri84-supervisor-prepared-v1' and prepared.get('mode') == name
             and prepared.get('authorization_granted') is False
             and prepared.get('supervisor_argv') == [str(E/'supervise.py'), name]
             and prepared.get('supervisor_cwd') == str(C),
             'prerequisite', 'native prepared evidence differs')
        same(prepared.get('paths'), {role: str(path) for role, path in complete_paths.items()}, 'native prepared paths differ')
        need(admitted.get('schema') == 'ri84-supervisor-admission-v1' and admitted.get('mode') == name
             and admitted.get('admitted') is True and admitted.get('freeze_payload_sha256') == payload,
             'prerequisite', 'native admission was not successful')
        require_ref(admitted.get('freeze_identity'), paths[name+'_freeze'], known)
        require_ref(admitted.get('authorization_identity'), paths[name+'_authorization'], known)
        for value in (prepared, admitted):
            same(value.get('observed_inputs'), expected_snapshot, 'native prepared/admitted identities differ')
            same(value.get('observed_runtime_namespace'), expected_namespace,
                 'native prepared/admitted runtime namespace differs')
            same(value.get('argv'), native_argv(name), 'native prepared/admitted argv differs')
            need(value.get('cwd') == str(C), 'prerequisite', 'native prepared/admitted cwd differs')
            same(value.get('environment'), ENV, 'native prepared/admitted environment differs')
            same(value.get('limits'), LIMITS, 'native prepared/admitted envelope differs')
        absence = {'original': True, 'copy': True, 'audit_copy': True} if name == 'witness' else None
        for value in (prepared, admitted):
            same(value.get('witness_certificate_absence'), absence, 'native candidate absence at admission differs')
        same(receipt.get('witness_certificate_absence_before'), absence, 'native candidate absence before differs')
        same(receipt.get('witness_certificate_absence_after'), absence, 'native candidate absence after differs')
        # Sample records are custody metadata, not target stdout or mathematics.
        sample_identity = known[str(paths[name+'_samples'])]
        need(type(sample_identity['bytes']) is int and 0 < sample_identity['bytes'] <= 64*1024*1024,
             'prerequisite', 'expected native sample evidence outside bound')
        samples_raw = paths[name+'_samples'].read_bytes()
        need(0 < len(samples_raw) <= 64*1024*1024, 'prerequisite', 'native sample evidence outside bound')
        need(len(samples_raw) == sample_identity['bytes']
             and sha256(samples_raw).hexdigest() == sample_identity['sha256'],
             'identity', 'native samples raw bytes differ from frozen identity')
        same(file_identity(paths[name+'_samples']), sample_identity, 'native samples path identity changed during read')
        samples = [strict_json(line, allow_floats=True) for line in samples_raw.splitlines()]
        need(all(type(row) is dict for row in samples), 'prerequisite', 'malformed native sample row')
        census = [row for row in samples if row.get('event') == 'monitor_attempt']
        launches = [row for row in samples if row.get('event') == 'launch']
        terminal = [row for row in samples if row.get('event') == 'terminal_poll']
        need(len(launches) == 1 and type(launches[0].get('pid')) is int and launches[0]['pid'] == receipt['pid']
             and type(launches[0].get('pgid')) is int and launches[0]['pgid'] == receipt['pid']
             and bool(census) and bool(terminal)
             and len(census) == receipt.get('monitor_attempts')
             and type(terminal[-1].get('returncode')) is int and terminal[-1]['returncode'] == 0
             and terminal[-1].get('terminal_absence') is True
             and census[-1].get('terminal_absence') is True and census[-1].get('owned_rows') == []
             and type(census[-1].get('child_poll')) is int and census[-1]['child_poll'] == 0
             and not any(row.get('event') == 'owned_group_cleanup' for row in samples),
             'prerequisite', 'native live/terminal sampled custody is incomplete')
        for index, row in enumerate(census, 1):
            need(type(row.get('index')) is int and row['index'] == index and 'error' not in row
                 and type(row.get('returncode')) is int and row['returncode'] == 0
                 and row.get('stderr') == '' and type(row.get('declared_timeout_ms')) is int
                 and row['declared_timeout_ms'] == LIMITS['ps_timeout_ms']
                 and (row.get('child_poll') is None or type(row['child_poll']) is int)
                 and (row.get('child_poll_before') is None or type(row['child_poll_before']) is int)
                 and type(row.get('owned_rss_bytes')) is int and 0 <= row['owned_rss_bytes'] <= LIMITS['rss_bytes'],
                 'prerequisite', 'native monitor attempt failed or exceeded envelope')
            same(row.get('argv'), [str(PS), '-axo', 'pid=,pgid=,rss='], 'native census argv differs')
        need(sum(row.get('owned_leader_present') is True for row in census) == receipt['live_rss_samples']
             and max(row['owned_rss_bytes'] for row in census) == receipt['sampled_peak_rss_bytes'],
             'prerequisite', 'native sample totals disagree with receipt')
        for value in (freeze, auth, receipt, prepared, admitted):
            bind_refs(value, known)


def validate_mode_custodies(before):
    """Require actual serial root/independent custody and genuine tool records."""
    known = refmap(before)
    witness_body = (E/'witness-01'/'stdout.log').read_bytes()
    need(len(witness_body) == CANDIDATE_BYTES and sha256(witness_body).hexdigest() == CANDIDATE_SHA256,
         'identity', 'whole witness body differs from bound candidate')
    for path in (CERTIFICATE_ORIGINAL, NATIVE_CANDIDATE, CERTIFICATE):
        need(path.read_bytes() == witness_body, 'identity', 'candidate copy differs from whole witness bytes')
    need((E/'normal-01'/'stdout.log').read_bytes() == (E/'optimized-01'/'stdout.log').read_bytes(),
         'identity', 'whole normal/optimized summaries differ')
    candidate = metadata(E/'CANDIDATE_CUSTODY.json')
    exact_keys(candidate, ('schema', 'whole_bytes_equal', 'scientific_math_accepted', 'replays_admitted',
                           'original', 'copy', 'audit_copy', 'source_stdout', 'saved_addendum', 'root_witness_acceptance'),
               'prerequisite', 'candidate custody')
    need(candidate['schema'] == 'ri129-exact-candidate-custody-v1' and candidate['whole_bytes_equal'] is True
         and candidate['scientific_math_accepted'] is False and candidate['replays_admitted'] is False,
         'prerequisite', 'candidate creation custody scope differs')
    for key, path in (('original', CERTIFICATE_ORIGINAL), ('copy', NATIVE_CANDIDATE), ('audit_copy', CERTIFICATE),
                      ('source_stdout', E/'witness-01'/'stdout.log'), ('saved_addendum', E/'SAVED_CERTIFICATE_ADDENDUM.json'),
                      ('root_witness_acceptance', E/'WITNESS_ROOT_CUSTODY.json')):
        require_ref(candidate[key], path, known)
    addendum = metadata(E/'SAVED_CERTIFICATE_ADDENDUM.json')
    witness_receipt = metadata(E/'witness-01'/'receipt.json')
    exact_keys(addendum, ('schema', 'authorized_modes', 'supervisor_sha256', 'checker_sha256', 'certificate_sha256',
                          'witness_receipt_sha256', 'witness_freeze_payload_sha256'), 'prerequisite', 'saved addendum')
    need(addendum['schema'] == 'ri84-saved-certificate-addendum-v1'
         and addendum['authorized_modes'] == ['normal', 'optimized']
         and addendum['supervisor_sha256'] == known[str(E/'supervise.py')]['sha256']
         and addendum['checker_sha256'] == ACCEPTED['checker_copy']
         and addendum['certificate_sha256'] == CANDIDATE_SHA256
         and addendum['witness_receipt_sha256'] == known[str(E/'witness-01'/'receipt.json')]['sha256']
         and addendum['witness_freeze_payload_sha256'] == witness_receipt.get('freeze_payload_sha256'),
         'prerequisite', 'saved addendum source/witness bindings differ')
    bind_refs(candidate, known)
    for name in PRODUCER_MODES:
        verify_applicability(name, known)
        paths = mode_paths(name)
        read = lambda suffix: metadata(paths[name+'_'+suffix])
        custody, root, independent = read('custody'), read('root_review'), read('independent_review')
        admission, outer = read('root_admission'), read('tool_completion')
        exact_keys(custody, ('schema', 'status', 'mode', 'source_adjudication', 'applicability', 'receipt', 'stdout',
                             'genuine_outer', 'root_complete_review', 'independent_complete_review', 'root_admission',
                             'before_after_current_identities_match', 'terminal_owned_group_absent', 'actual_outer_exit',
                             'actual_outer_chunk_id', 'scientific_math_accepted', 'programme_complete',
                             'root_witness_acceptance', 'root_normal_acceptance', 'candidate_custody',
                             'saved_summary_whole_bytes_equal'), 'prerequisite', 'completed root custody')
        need(custody['schema'] == 'ri129-root-completed-producer-custody-v1'
             and custody['status'] == 'ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY' and custody['mode'] == name
             and custody['before_after_current_identities_match'] is True and custody['terminal_owned_group_absent'] is True
             and type(custody['actual_outer_exit']) is int and custody['actual_outer_exit'] == 0
             and type(custody['actual_outer_chunk_id']) is str and bool(custody['actual_outer_chunk_id'])
             and custody['scientific_math_accepted'] is False and custody['programme_complete'] is False,
             'prerequisite', 'completed producer custody scope differs')
        for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                          ('applicability', paths[name+'_applicability']), ('receipt', paths[name+'_receipt']),
                          ('stdout', paths[name+'_stdout']), ('genuine_outer', paths[name+'_tool_completion']),
                          ('root_complete_review', paths[name+'_root_review']),
                          ('independent_complete_review', paths[name+'_independent_review']),
                          ('root_admission', paths[name+'_root_admission'])):
            require_ref(custody[key], path, known)
        expected_prior = {
            'root_witness_acceptance': None if name == 'witness' else known[str(E/'WITNESS_ROOT_CUSTODY.json')],
            'root_normal_acceptance': known[str(E/'NORMAL_ROOT_CUSTODY.json')] if name == 'optimized' else None,
            'candidate_custody': None if name == 'witness' else known[str(E/'CANDIDATE_CUSTODY.json')],
            'saved_summary_whole_bytes_equal': True if name == 'optimized' else None,
        }
        for key, value in expected_prior.items():
            same(custody[key], value, 'completed serial custody dependency differs')
        exact_keys(admission, ('schema', 'status', 'mode', 'source_adjudication', 'applicability', 'freeze',
                               'authorization', 'outer_argv', 'outer_cwd', 'outer_environment', 'outer_invocation',
                               'retry_or_limit_relaxation_authorized', 'history_manifest', 'dependency_manifest'),
                   'prerequisite', 'root stage admission')
        need(admission['schema'] == 'ri129-root-stage-admission-v1'
             and admission['status'] == 'ADMITTED_ONE_FROZEN_'+name.upper()+'_INVOCATION'
             and admission['mode'] == name and admission['retry_or_limit_relaxation_authorized'] is False,
             'prerequisite', 'actual root producer admission differs')
        for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                          ('applicability', paths[name+'_applicability']), ('freeze', paths[name+'_freeze']),
                          ('authorization', paths[name+'_authorization']), ('history_manifest', HISTORY),
                          ('dependency_manifest', DEPENDENCIES)):
            require_ref(admission[key], path, known)
        same(admission['outer_argv'], [str(PYTHON), '-I', '-S', '-B', str(E/'supervise.py'), name],
             'root admitted outer argv differs')
        need(admission['outer_cwd'] == str(C), 'prerequisite', 'root admitted outer cwd differs')
        same(admission['outer_environment'], ENV, 'root admitted literal outer environment differs')
        invocation = admission['outer_invocation']
        need(type(invocation) is dict and invocation.get('workdir') == str(C)
             and type(invocation.get('cmd')) is str and bool(invocation['cmd']),
             'prerequisite', 'pre-admitted literal tool invocation missing')
        exact_keys(outer, ('record_type', 'source', 'invocation', 'result'), 'prerequisite', 'genuine outer record')
        need(outer['record_type'] == 'transcription_of_genuine_exec_command_result'
             and outer['source'] == 'Coordinator task tool history; actual invocation, not replay or reconstructed success',
             'prerequisite', 'genuine outer provenance labels differ')
        same(outer['invocation'], invocation, 'genuine invocation differs from pre-admitted literal command')
        completion = outer['result']
        need(type(completion) is dict and type(completion.get('exit_code')) is int and completion['exit_code'] == 0
             and completion.get('chunk_id') == custody['actual_outer_chunk_id'] and 'session_id' not in completion
             and type(completion.get('output')) is str, 'prerequisite', 'actual outer exit/chunk incomplete')
        same(strict_json(completion['output'].encode()), {'mode': name, 'success': True,
             'receipt': str(paths[name+'_receipt']), 'receipt_sha256': known[str(paths[name+'_receipt'])]['sha256']},
             'genuine outer success does not bind exact receipt')
        for value, schema, status in ((root, 'ri129-root-completed-mode-review-v1',
                                      'PASS_COMPLETED_'+name.upper()+'_CUSTODY_PENDING_INDEPENDENT_REVIEW'),
                                     (independent, 'ri129-independent-completed-mode-review-v1',
                                      'PASS_COMPLETED_'+name.upper()+'_CUSTODY_ONLY')):
            need(value.get('schema') == schema and value.get('status') == status and value.get('mode') == name
                 and value.get('blocking_findings') == [] and value.get('before_after_current_identities_match') is True
                 and value.get('terminal_owned_group_absent') is True and value.get('native_arithmetic_recomputed') is False
                 and value.get('native_mathematics_accepted') is False and value.get('programme_complete') is False,
                 'prerequisite', 'root or independent completed-mode review differs')
            checks = value.get('current_target_checks')
            exact_keys(checks, ('sign_fixtures', 'internal_decision_cases', 'intended_first_refusals'),
                       'prerequisite', 'completed current-target check counts')
            need(all(type(checks[key]) is int for key in checks)
                 and checks == {'sign_fixtures': 15, 'internal_decision_cases': 4,
                                'intended_first_refusals': 71}
                 and value.get('current_target_checks_completed') is True
                 and value.get('changed_target_qualification_inherited') is False,
                 'prerequisite', 'actual current-target checks absent or old qualification credited')
            for key, path in (('source_adjudication', E/'ROOT_SOURCE_ADJUDICATION.json'),
                              ('applicability', paths[name+'_applicability']), ('genuine_outer', paths[name+'_tool_completion']),
                              ('root_admission', paths[name+'_root_admission']), ('freeze', paths[name+'_freeze']),
                              ('authorization', paths[name+'_authorization']), ('receipt', paths[name+'_receipt'])):
                require_ref(value.get(key), path, known)
            expected_outputs = {filename: known[str(paths[name+'_'+role])] for role, filename in
                                (('receipt', 'receipt.json'), ('stdout', 'stdout.log'), ('stderr', 'stderr.log'),
                                 ('samples', 'samples.jsonl'), ('prepared', 'prepared.json'), ('admission', 'admission.json'))}
            same(value.get('outputs'), expected_outputs, 'completed review must bind all six evidence files')
        for value in (custody, root, independent, admission, outer):
            bind_refs(value, known)


def pre_attempt_prerequisites(mode):
    """Read-only complete admission validation before allocating audit-01.

    The guarded run repeats every check against fresh observations. This new
    preflight grants nothing, writes nothing, and inherits no qualification.
    Its refusal remains an outer failure that root must preserve genuinely.
    """
    need(type(mode) is str and mode == 'audit', 'configuration', 'fixed preflight mode changed')
    preparation_ready()
    paths = dict(input_paths(mode), interpreter=PYTHON, supervisor=SELF,
                 freeze=E/'AUDIT_EXECUTION_FREEZE.json', authorization=E/'AUDIT_AUTHORIZATION.json')
    before = snapshot(paths)
    namespace_before = runtime_namespace_snapshot()
    for role in paths:
        observed(before, role)
    need(sys.platform == 'darwin' and Path(__file__).absolute() == SELF,
         'configuration', 'fixed preflight platform or caller path changed')
    need(dict(os.environ) == ENV and sys.flags.isolated == 1 and sys.flags.no_site == 1
         and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0
         and sys.argv == [str(SELF), 'audit'] and Path.cwd() == C,
         'configuration', 'preflight environment, flags, argv or cwd changed')
    need(os.path.realpath(sys.executable) == runtime_file_identity(PYTHON)['resolved_path'],
         'configuration', 'preflight interpreter differs from frozen runtime')
    same(namespace_before, runtime_expected_namespace(), 'preflight runtime namespace differs')
    config = metadata(paths['freeze'], observed(before, 'freeze'), allow_floats=False)
    payload_hash = validate_freeze(config, mode, before)
    auth = metadata(paths['authorization'], observed(before, 'authorization'), allow_floats=False)
    validate_authorization(auth, config, mode, payload_hash, before)
    # Independently finish all physical/namespace observations even when one
    # path changed. No externally visible admission or attempt exists yet.
    after = snapshot(paths)
    namespace_after = runtime_namespace_snapshot()
    same(after, before, 'preflight inputs changed during full prerequisite validation')
    same(namespace_after, namespace_before, 'preflight runtime namespace changed')
    same(namespace_after, runtime_expected_namespace(), 'preflight final runtime namespace differs')


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


def run(mode):
    global CLOSING, LAUNCHING
    preparation_ready()
    need(type(mode) is str and mode in MODES, 'configuration', 'require exactly one fixed mode: audit')
    CLOSING, LAUNCHING = False, False
    RECEIVED_SIGNALS.clear()
    pre_attempt_prerequisites(mode)
    attempt = Attempt(mode)
    freeze_path = E/(mode.upper()+'_EXECUTION_FREEZE.json')
    auth_path = E/(mode.upper()+'_AUTHORIZATION.json')
    paths = dict(input_paths(mode), interpreter=PYTHON, supervisor=SELF,
                 freeze=freeze_path, authorization=auth_path)
    started_at, started = timestamp(), time.monotonic()
    before, after, config, payload_hash = {}, {}, None, None
    namespace_before, namespace_after = {}, {}
    proc, launched, child_ended, exit_code, peak, valid_samples, monitor_attempts = None, None, None, None, 0, 0, 0
    absent_before, absent_after = None, None
    error, cleanup_errors, admission_written = None, [], False
    try:
        before = snapshot(paths)
        namespace_before = runtime_namespace_snapshot()
        attempt.open_logs()
        need(sys.platform == 'darwin', 'configuration', 'this frozen supervisor requires Darwin RSS units')
        need(Path(__file__).absolute() == SELF, 'configuration', 'supervisor path changed')
        need(dict(os.environ) == ENV and sys.flags.isolated == 1 and sys.flags.no_site == 1
             and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0
             and sys.argv == [str(SELF), 'audit'] and Path.cwd() == C,
             'configuration', 'frozen launcher environment, flags, argv or cwd changed')
        need(os.path.realpath(sys.executable) == runtime_file_identity(PYTHON)['resolved_path'],
             'configuration', 'executing launcher interpreter differs from frozen runtime')
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
        config = metadata(freeze_path, observed(before, 'freeze'), allow_floats=False)
        payload_hash = validate_freeze(config, mode, before)
        validate_authorization(metadata(auth_path, observed(before, 'authorization'), allow_floats=False),
                               config, mode, payload_hash, before)
        # Close read/validation races immediately before durable admission.
        admission_inputs = snapshot(paths)
        admission_namespace = runtime_namespace_snapshot()
        same(admission_namespace, runtime_expected_namespace(), 'runtime namespace changed before admission')
        same(admission_namespace, namespace_before, 'runtime namespace pre-admission observations differ')
        need(canonical(admission_inputs) == canonical(before), 'identity', 'inputs changed before admission')
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
        # This consumer emits its complete report only to stdout. Preserve raw
        # stdout, then make one exclusive byte-identical report after child exit.
        attempt.stdout.flush()
        os.fsync(attempt.stdout.fileno())
        with (attempt.path/'stdout.log').open('rb') as source_stream, (attempt.path/'REPORT.json').open('xb') as report_stream:
            for chunk in iter(lambda: source_stream.read(1024*1024), b''):
                report_stream.write(chunk)
            report_stream.flush()
            os.fsync(report_stream.fileno())
        fsync_directory(attempt.path)
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
        stable = canonical(before) == canonical(after)
        if not stable and error is None:
            error = {'code': 'input_change', 'type': 'Stop', 'message': 'frozen input identities changed during attempt'}
        if cleanup_errors and error is None:
            error = {'code': 'cleanup', 'type': 'Stop', 'message': 'durable cleanup did not complete'}
        if RECEIVED_SIGNALS and error is None:
            error = {'code': 'signal', 'type': 'Stop', 'message': 'catchable shutdown signal received during cleanup'}
        output_paths = {'stdout': attempt.path/'stdout.log', 'stderr': attempt.path/'stderr.log',
                        'samples': attempt.path/'samples.jsonl', 'prepared': attempt.path/'prepared.json',
                        'admission': attempt.path/'admission.json', 'audit_report': attempt.path/'REPORT.json'}
        output_snapshot = snapshot(output_paths)
        if not all(item['ok'] is True for item in output_snapshot.values()) and error is None:
            error = {'code': 'output_identity', 'type': 'Stop', 'message': 'an evidence output is unavailable'}
        if error is None:
            raw_identity = output_snapshot['stdout']['identity']
            report_identity = output_snapshot['audit_report']['identity']
            if any(raw_identity[key] != report_identity[key] for key in ('bytes', 'sha256')):
                error = {'code': 'output_identity', 'type': 'Stop', 'message': 'exclusive report differs from retained raw stdout'}
        success = error is None and exit_code == 0 and stable and valid_samples > 0 and not cleanup_errors
        receipt = {
            'schema': 'ri95-certificate-audit-receipt-v1', 'mode': mode, 'success': success,
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
    preparation_ready()
    need(len(sys.argv) == 2 and sys.argv[1] in MODES, 'configuration', 'require exactly one fixed mode: audit')
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
