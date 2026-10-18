"""RI132 pure validation of root-owned genuine early-refusal evidence.

SOURCE ONLY. Nothing here launches/imports a caller, reads a file, creates an
artifact, patches a target or authenticates evidence origin. Root must admit
and monitor each actual invocation, preserve its external custody and obtain
independent origin review. Matching this structural contract is not admission.
"""

from hashlib import sha256
import json
from pathlib import PurePosixPath


BASE = '/Volumes/AI_DATA/development/det-review-evidence'
E = BASE + '/ri129-native-sign-caller-source-8TksBLo0'
C = E + '/closure'
B = C + '/native_growth_connected_strict_sign_v1'
Q = BASE + '/ri132-native-caller-qualification-source-0ZmB3R5I'
A = BASE + '/ri122-native-caller-source-jgehvvxx'
S = BASE + '/ri128-connected-sign-dvgWLqqv'
REVIEW = BASE + '/ri129-native-caller-independent-review-Z0SqaY10'
PYTHON = '/opt/homebrew/bin/python3'
ENV = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC',
       '__CF_USER_TEXT_ENCODING': '0x1F5:0x0:0x0'}
LIMITS = {'wall_seconds': 120, 'rss_bytes': 536870912,
          'sample_interval_ms': 50, 'ps_timeout_ms': 250}
AUX_BYTES = 64 * 1024 * 1024
BODY_BYTES = 8 * 1024 * 1024
MANIFEST_PINS = {
    'history': (A + '/HISTORY_RECONCILIATION.json', 2170307,
                'b00d94f5d81f22e6c18715bed9519eb17f8252d12871e3254a9f3e5dac92435c'),
    'runtime': (A + '/RUNTIME_CLOSURE.json', 2862854,
                '35a58d48fce8e00e87d61034b13ef4fba2571d68630d55616ea27e3b786a7920'),
    'dependencies': (E + '/SOURCE_DEPENDENCIES.json', 583262,
                     'a2ef77a9827ceafaf8e94296ec01389d686f3ce2f68064b23d7a1626343c3d1c'),
}
FIXED_PINS = (
    ('native_supervisor', E + '/supervise.py', 88890,
     '34707ca1bd6e245ca9ec469adeb4c3da8cf0ed303be945036708554073b39650'),
    ('audit_caller', E + '/launch_audit.py', 103287,
     '5263099d45d9ed021a80d65029da511ad9019d30892278b1b412cb1794465ae5'),
    ('caller_contract', E + '/CALLER_CONTRACT.md', 24196,
     'dc2d798e3e95957ddcc397f94155f3c2ca493bc500eec2086aa2147a53a11dd6'),
    ('ri129_handoff', E + '/HANDOFF.json', 10184,
     'b3839ba2f81e791321e2549107ce5f1b84ffdbbcc635396ab4e72002386feac0'),
    ('ri129_root', BASE + '/ri129-root-source-adjudication-7cuvjhh5/RI129_ROOT_ADJUDICATION.json', 6126,
     '4b3139b7595e3f9c94c9bda3725dc7b6e329b7b100b1493124199064a4743266'),
    ('ri129_review_narrative', REVIEW + '/INDEPENDENT_SOURCE_REVIEW.md', 16214,
     '19d74caf5807a4d781bfac97959c2f791d9c181914496e0504145a321132f7eb'),
    ('ri129_review_machine', REVIEW + '/INDEPENDENT_SOURCE_REVIEW.json', 6670,
     'd0e81254694db9c145c3760b08e86f02a8e2a1edadccfe10776842e4455710de'),
    ('ri129_review_handoff', REVIEW + '/HANDOFF.json', 3082,
     '6cd215563c660948188a73c6d3d0ccc6fe6f583b4d1bc2cc981654abcc223ac0'),
    ('ri129_retained_comparisons', REVIEW + '/CORRECTED_METADATA_SUMMARY.json', 18478,
     '2d69442db44cea379812c5b4907818b05e0c7008ab6d65061cc84a0a7bc65c04'),
    ('ri128_root', BASE + '/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json', 3230,
     '324644290d2d8eeb79a2af655bed476f02f7d0cc3ffb5fac1672f975f0a3ede1'),
)
ORIGINAL_PINS = (
    ('checker', S + '/check.py', 'check.py', 27288,
     '73bb32320be53c38cf85889ca108229d9c2ea2d79b27814ac258eb4b6f133e38'),
    ('auditor', S + '/audit_saved.py', 'audit_saved.py', 41355,
     '5c9494e78df31c726c973d2aa0188ca745a3532a351a5826dcb312fca3892ed7'),
    ('implementation', S + '/IMPLEMENTATION.md', 'IMPLEMENTATION.md', 9005,
     'e9053c9b8e9f6d113febf4cc4b5597aca5e2238a25e67d14c5a3b743149aad26'),
    ('audit_notes', S + '/AUDIT_NOTES.md', 'AUDIT_NOTES.md', 13789,
     '89af7f6f7f4ea17e835770ff24ed71e181f5f6f28751f4f7fc8c57cdca77caf6'),
    ('ri88', A + '/closure/native_growth_connected_sensitivity_v1/inputs/ri88.json',
     'inputs/ri88.json', 1828149,
     'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    ('ri88_root', BASE + '/ri87-ri88-results-checkpoint-3_kuqmvi/RI88_ROOT_RESULT_ADJUDICATION.json',
     'inputs/ri88_root.json', 2783,
     '15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6'),
    ('ri122_root', BASE + '/ri122-root-execution-review-6whn_vky/RI122_ROOT_FINAL_ADJUDICATION.json',
     'inputs/ri122_root.json', 15477,
     '162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc'),
    ('ri124_root', BASE + '/ri124-root-proof-review-77jju1y6/ROOT_ADJUDICATION.json',
     'inputs/ri124_root.json', 3645,
     '85b6d5c84139b05d5a18f89614a415ecde962efc429092b914e6f2da33ccde9c'),
    ('ri127_root', BASE + '/ri127-root-proof-review-tz7oyfkj/ROOT_ADJUDICATION.json',
     'inputs/ri127_root.json', 4071,
     '66d274815c101015256ba506f3e6a125375797b1b7946831159d39692ffebd77'),
)
ENTRY_CASES = {
    'native-invalid-mode': {
        'caller_role': 'native_supervisor', 'mode': 'ri132-invalid-mode', 'cwd': E,
        'function': 'main', 'exception_type': 'Stop', 'source_attributed_code': 'configuration',
        'message': 'require exactly one fixed mode: witness, normal, optimized',
        'coverage': 'WHOLE_UNCHANGED_ENTRY_CONFIGURATION_ONLY',
    },
    'native-witness-missing-copy': {
        'caller_role': 'native_supervisor', 'mode': 'witness', 'cwd': C,
        'function': 'pre_attempt_prerequisites -> identity_index -> observed',
        'exception_type': 'Stop', 'source_attributed_code': 'identity',
        'message': 'unavailable input identity: checker_copy',
        'coverage': 'WHOLE_UNCHANGED_ENTRY_FIRST_MISSING_COPY_ONLY',
    },
    'audit-missing-binding': {
        'caller_role': 'audit_caller', 'mode': 'audit', 'cwd': C,
        'function': 'main -> preparation_ready -> file_identity',
        'exception_type': 'FileNotFoundError', 'source_attributed_code': None,
        'message': "[Errno 2] No such file or directory: '" + E + "/AUDIT_BINDING.json'",
        'coverage': 'WHOLE_UNCHANGED_ENTRY_PREPARATION_MISSING_BINDING_ONLY',
    },
}


class EvidenceError(ValueError):
    pass


def _need(condition, message):
    if not condition:
        raise EvidenceError(message)


def _keys(value, expected, context):
    _need(type(value) is dict and set(value) == set(expected), context + ': keys differ')


def _same(left, right, context):
    # JSON spelling preserves bool/int and all nested types, unlike Python ==.
    _need(json.dumps(left, sort_keys=True, separators=(',', ':'), allow_nan=False) ==
          json.dumps(right, sort_keys=True, separators=(',', ':'), allow_nan=False), context)


def _path(value):
    _need(type(value) is str and value.startswith('/') and '\x00' not in value
          and str(PurePosixPath(value)) == value and '..' not in PurePosixPath(value).parts,
          'noncanonical literal path')
    return value


def _hash(value):
    return type(value) is str and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _identity(path, size, checksum):
    return {'path': path, 'resolved_path': path, 'bytes': size,
            'sha256': checksum, 'symlinks': []}


def _validate_identity(value):
    _keys(value, ('path', 'resolved_path', 'bytes', 'sha256', 'symlinks'), 'identity')
    _path(value['path'])
    _path(value['resolved_path'])
    _need(type(value['bytes']) is int and value['bytes'] >= 0
          and _hash(value['sha256']) and type(value['symlinks']) is list, 'identity fields')
    for link in value['symlinks']:
        _keys(link, ('path', 'target'), 'symlink')
        _path(link['path'])
        _need(type(link['target']) is str, 'symlink target')


def _text(value, maximum, context):
    _need(type(value) is str, context + ': text required')
    raw = value.encode('utf-8')
    _need(len(raw) <= maximum, context + ': byte ceiling')
    return raw


def _decode(text):
    def pairs(items):
        result = {}
        for key, value in items:
            _need(key not in result, 'duplicate administrative JSON key')
            result[key] = value
        return result
    def reject(value):
        raise EvidenceError('noninteger administrative JSON number: ' + value)
    return json.loads(text, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)


def _bound_body(value, identity, maximum=AUX_BYTES):
    _validate_identity(identity)
    raw = _text(value, maximum, 'administrative body')
    _need(identity['bytes'] == len(raw) and identity['sha256'] == sha256(raw).hexdigest(),
          'body differs from complete recorded identity')
    return _decode(value)


def _namespace(runtime):
    host = runtime['host_platform']
    return {
        'directories': {item['path']: {'ok': True, 'identity': item} for item in runtime['directories']},
        'absences': {path: {'ok': True, 'absent': True} for path in runtime['absences']},
        'host_platform': {
            'uname': {'ok': True, 'identity': host['expected_uname']},
            'system_version': {'ok': True, 'identity': host['system_version_plist']['expected_values']},
            'system_dependencies': [{'ok': True, 'identity': {key: item[key] for key in
                ('install_name', 'location_status', 'shared_cache_status')}}
                for item in host['system_dependencies']],
            'trust_boundary': host['trust_boundary'],
        },
    }


def _absent_paths():
    paths = {B, E + '/ROOT_SOURCE_ADJUDICATION.json', E + '/INDEPENDENT_SOURCE_REVIEW.json',
             E + '/CERTIFICATE.json', B + '/CERTIFICATE.json', E + '/AUDIT_CANDIDATE.json',
             E + '/CANDIDATE_CUSTODY.json', E + '/SAVED_CERTIFICATE_ADDENDUM.json',
             E + '/AUDIT_BINDING.json', E + '/AUDIT_INPUT.json', E + '/REPORT.json'}
    paths.update(B + '/' + relative for role, original, relative, count, checksum in ORIGINAL_PINS)
    for mode in ('witness', 'normal', 'optimized', 'audit'):
        attempt = E + '/' + mode + '-01'
        paths.add(attempt)
        paths.update(attempt + '/' + name for name in
                     ('receipt.json', 'stdout.log', 'stderr.log', 'samples.jsonl', 'prepared.json', 'admission.json'))
        suffixes = ('APPLICABILITY.json', 'EXECUTION_FREEZE.json', 'AUTHORIZATION.json', 'ROOT_ADMISSION.json')
        if mode != 'audit':
            suffixes += ('OUTER_TOOL_RESULT.json', 'ROOT_COMPLETE_REVIEW.json',
                         'INDEPENDENT_COMPLETE_REVIEW.json', 'ROOT_CUSTODY.json')
        paths.update(E + '/' + mode.upper() + '_' + suffix for suffix in suffixes)
    return sorted(paths)


def _closure(record, admission):
    _keys(record['manifest_bodies'], MANIFEST_PINS, 'manifest bodies')
    files, manifests = [], {}
    for role, (path, count, checksum) in MANIFEST_PINS.items():
        identity = _identity(path, count, checksum)
        # Whole accepted manifest bytes authenticate its complete role arrays.
        manifests[role] = _bound_body(record['manifest_bodies'][role], identity)
        files.append({'role': 'manifest_' + role, 'identity': identity})
    for role, path, count, checksum in FIXED_PINS:
        files.append({'role': role, 'identity': _identity(path, count, checksum)})
    for role, original, relative, count, checksum in ORIGINAL_PINS:
        files.append({'role': role + '_original', 'identity': _identity(original, count, checksum)})
    for group, key, count in (('runtime', 'files', 2988), ('history', 'protected_files', 699),
                              ('dependencies', 'protected_files', 299)):
        entries = manifests[group][key]
        _need(type(entries) is list and len(entries) == count, 'pinned manifest role count changed')
        for entry in entries:
            _validate_identity(entry['identity'])
            _need(entry['path'] == entry['identity']['path'], 'manifest entry path mismatch')
            files.append({'role': group + ':' + entry['role'], 'identity': entry['identity']})
    handoff_id = admission['qualification_handoff']
    _validate_identity(handoff_id)
    _need(handoff_id['path'] == Q + '/HANDOFF.json' and handoff_id['resolved_path'] == handoff_id['path']
          and handoff_id['symlinks'] == [], 'qualification handoff path changed')
    handoff = _bound_body(record['qualification_handoff_body'], handoff_id)
    _need(handoff.get('schema') == 'ri132-native-caller-qualification-source-handoff-v1'
          and handoff.get('status') == 'SOURCE_ONLY_SEALED_FOR_NONAUTHOR_REVIEW'
          and handoff.get('execution_authorized') is False and handoff.get('scientific_execution') is False,
          'qualification source handoff scope changed')
    entries = handoff.get('files')
    _need(type(entries) is list and bool(entries), 'qualification source closure missing')
    paths = []
    for index, entry in enumerate(entries):
        _keys(entry, ('path', 'bytes', 'sha256'), 'qualification source entry')
        _path(entry['path'])
        _need(str(PurePosixPath(entry['path']).parent) == Q and entry['path'] != Q + '/HANDOFF.json',
              'qualification source file outside fixed packet or circular handoff')
        identity = _identity(entry['path'], entry['bytes'], entry['sha256'])
        _validate_identity(identity)
        _need(identity['bytes'] > 0, 'empty qualification source entry')
        paths.append(entry['path'])
        files.append({'role': 'qualification:' + str(index + 1).zfill(4), 'identity': identity})
    _need(paths == sorted(set(paths)), 'qualification files unordered or duplicate')
    _need(all(Q + '/' + name in paths for name in
              ('entry_evidence.py', 'qualify_callers.py', 'native_controls.py', 'audit_controls.py', 'EVIDENCE_CONTRACT.md')),
          'qualification executable or contract omitted')
    files.append({'role': 'qualification_handoff', 'identity': handoff_id})
    by_path = {}
    for entry in files:
        path = entry['identity']['path']
        if path in by_path:
            _same(by_path[path], entry['identity'], 'conflicting aliased closure identity')
        by_path[path] = entry['identity']
    _need(len({item['role'] for item in files}) == len(files), 'duplicate external custody role')
    _need(not set(by_path).intersection(_absent_paths()), 'present and absent closure conflict')
    return files, _namespace(manifests['runtime']), by_path


def _external(record, field, expected_files, namespace, case, directory):
    envelope = record[field]
    _keys(envelope, ('identity', 'body'), field)
    identity = envelope['identity']
    _validate_identity(identity)
    expected_path = directory + '/' + field + '.json'
    _need(identity['path'] == expected_path and identity['resolved_path'] == expected_path
          and identity['symlinks'] == [], field + ': literal path differs')
    value = _bound_body(envelope['body'], identity)
    _keys(value, ('schema', 'phase', 'case_id', 'files', 'runtime_namespace', 'absences',
                  'cwd_directory', 'complete', 'errors', 'observed_at_ns'), field)
    _need(value['schema'] == 'ri132-external-entry-custody-v1' and value['phase'] == field
          and value['case_id'] == record['case_id'] and value['complete'] is True and value['errors'] == [],
          field + ': incomplete or failed external custody')
    _need(type(value['observed_at_ns']) is int and value['observed_at_ns'] > 0, field + ': observation time')
    _same(value['files'], expected_files, field + ': complete ordered file roles/identities differ')
    _same(value['runtime_namespace'], namespace, field + ': complete runtime namespace/host differs')
    _same(value['absences'], [{'path': path, 'errno': 2} for path in _absent_paths()],
          field + ': required lstat ENOENT observations differ')
    _same(value['cwd_directory'], {'path': case['cwd'], 'resolved_path': case['cwd'],
                                  'symlinks': [], 'kind': 'directory'}, field + ': actual cwd observation differs')
    return value


def _process(value):
    _keys(value, ('schema', 'leader_pid', 'owned_pgid', 'started_at_ns', 'completed_at_ns',
                  'active_elapsed_ns', 'samples', 'terminal_owned_group_absent', 'errors', 'signals'), 'process custody')
    _need(value['schema'] == 'ri132-root-owned-entry-process-custody-v1', 'process custody schema')
    for key in ('leader_pid', 'owned_pgid', 'started_at_ns', 'completed_at_ns', 'active_elapsed_ns'):
        _need(type(value[key]) is int and value[key] > 0, 'process integer field: ' + key)
    _need(value['leader_pid'] == value['owned_pgid'] and value['started_at_ns'] < value['completed_at_ns']
          and value['active_elapsed_ns'] <= 120000000000, 'owned group or wall bound differs')
    _need(value['terminal_owned_group_absent'] is True and value['errors'] == [] and value['signals'] == [],
          'process monitoring/cleanup failed')
    samples = value['samples']
    _need(type(samples) is list and len(samples) >= 2, 'live and terminal external samples required')
    previous, live = 0, False
    for item in samples:
        _keys(item, ('elapsed_ns', 'census_elapsed_ns', 'members', 'raw_stdout', 'raw_stderr', 'exit_code'), 'process sample')
        _need(type(item['elapsed_ns']) is int and previous <= item['elapsed_ns'] <= value['active_elapsed_ns'],
              'sample timing differs')
        _need(type(item['census_elapsed_ns']) is int and 0 <= item['census_elapsed_ns'] <= 250000000
              and item['elapsed_ns'] + item['census_elapsed_ns'] <= 120000000000, 'census deadline differs')
        _need(type(item['exit_code']) is int and item['exit_code'] == 0 and item['raw_stderr'] == '', 'census failed')
        _text(item['raw_stdout'], BODY_BYTES, 'raw census output')
        _need(type(item['members']) is list, 'process sample members')
        seen, total = set(), 0
        for member in item['members']:
            _keys(member, ('pid', 'pgid', 'rss_bytes'), 'owned process')
            _need(type(member['pid']) is int and member['pid'] > 0 and member['pid'] not in seen
                  and type(member['pgid']) is int and member['pgid'] == value['owned_pgid']
                  and type(member['rss_bytes']) is int and member['rss_bytes'] >= 0, 'owned process fields')
            seen.add(member['pid'])
            total += member['rss_bytes']
        _need(total <= 536870912, 'sampled owned-group RSS bound exceeded')
        live = live or value['leader_pid'] in seen
        previous = item['elapsed_ns']
    _need(live and samples[-1]['members'] == [], 'no live leader or final owned group not empty')
    # Raw census/member correspondence and real PID ownership need root's actual
    # independent capture review; this pure record checker cannot prove origin.


def validate_entry_record(record, case_id):
    """Check structural consistency only; never launch, admit, or authenticate origin."""
    _need(type(case_id) is str and case_id in ENTRY_CASES, 'unknown fixed entry case')
    _keys(record, ('schema', 'case_id', 'evidence_directory', 'manifest_bodies',
                   'qualification_handoff_body', 'root_admission_identity', 'root_admission_body',
                   'genuine_outer', 'stdout', 'stderr', 'external_before', 'external_after', 'process_custody'), 'entry record')
    _need(len(json.dumps(record, ensure_ascii=False, allow_nan=False).encode('utf-8')) <= AUX_BYTES,
          'complete administrative evidence exceeds 64 MiB')
    _need(record['schema'] == 'ri132-genuine-early-refusal-record-v1' and record['case_id'] == case_id,
          'entry record schema/case changed')
    case = ENTRY_CASES[case_id]
    directory = _path(record['evidence_directory'])
    _need(str(PurePosixPath(directory).parent) == BASE and directory not in (E, Q, A, S, REVIEW)
          and PurePosixPath(directory).name.startswith('ri132-entry-evidence-'), 'evidence directory outside root-owned reservation')
    admission_id = record['root_admission_identity']
    _validate_identity(admission_id)
    _need(admission_id['path'] == directory + '/ROOT_ADMISSION.json'
          and admission_id['resolved_path'] == admission_id['path'] and admission_id['symlinks'] == [], 'root admission path')
    admission = _bound_body(record['root_admission_body'], admission_id)
    _keys(admission, ('schema', 'status', 'case_id', 'qualification_handoff', 'caller', 'entry_verifier',
                      'outer_argv', 'outer_cwd', 'outer_environment', 'outer_invocation', 'limits',
                      'external_before', 'execution_scope', 'scientific_execution_authorized', 'retry_authorized'), 'root entry admission')
    _need(admission['schema'] == 'ri132-root-one-entry-qualification-admission-v1'
          and admission['status'] == 'ADMITTED_ONE_FIXED_EARLY_REFUSAL_INVOCATION'
          and admission['case_id'] == case_id and admission['execution_scope'] == 'caller_early_refusal_only'
          and admission['scientific_execution_authorized'] is False and admission['retry_authorized'] is False,
          'root admission scope')
    expected_files, namespace, by_path = _closure(record, admission)
    caller_path = E + ('/supervise.py' if case['caller_role'] == 'native_supervisor' else '/launch_audit.py')
    _same(admission['caller'], by_path[caller_path], 'admitted caller differs')
    _same(admission['entry_verifier'], by_path[Q + '/entry_evidence.py'], 'admitted entry verifier differs')
    _same(admission['outer_argv'], [PYTHON, '-I', '-S', '-B', caller_path, case['mode']], 'admitted actual entry argv differs')
    _same(admission['outer_cwd'], case['cwd'], 'admitted actual entry cwd differs')
    _same(admission['outer_environment'], ENV, 'admitted actual entry environment differs')
    _same(admission['limits'], LIMITS, 'admitted entry resource envelope differs')
    before = _external(record, 'external_before', expected_files, namespace, case, directory)
    after = _external(record, 'external_after', expected_files, namespace, case, directory)
    _same(admission['external_before'], record['external_before']['identity'], 'admitted external preflight differs')
    outer = record['genuine_outer']
    _keys(outer, ('record_type', 'source', 'invocation', 'result'), 'genuine outer transcription')
    _need(outer['record_type'] == 'transcription_of_genuine_exec_command_result'
          and outer['source'] == 'Coordinator task tool history; actual invocation, not replay or reconstructed success',
          'outer transcription labels differ')
    _same(outer['invocation'], admission['outer_invocation'], 'actual invocation differs from pre-admitted literal invocation')
    _need(type(outer['invocation']) is dict and type(outer['invocation'].get('cmd')) is str
          and bool(outer['invocation']['cmd']) and outer['invocation'].get('workdir') == case['cwd'],
          'actual literal invocation incomplete')
    result = outer['result']
    _need(type(result) is dict and type(result.get('exit_code')) is int and result['exit_code'] == 2
          and 'session_id' not in result and type(result.get('chunk_id')) is str and bool(result['chunk_id']),
          'actual outer process not genuinely completed with integer exit 2')
    _text(result.get('output'), BODY_BYTES, 'outer tool output')
    expected_stderr = 'SUPERVISOR REFUSAL: ' + case['exception_type'] + ': ' + case['message'] + '\n'
    for role, expected in (('stdout', ''), ('stderr', expected_stderr)):
        stream = record[role]
        _keys(stream, ('identity', 'text'), role)
        identity = stream['identity']
        _validate_identity(identity)
        raw = _text(stream['text'], BODY_BYTES, role)
        _need(identity['path'] == directory + '/' + role + '.log' and identity['resolved_path'] == identity['path']
              and identity['symlinks'] == [] and identity['bytes'] == len(raw)
              and identity['sha256'] == sha256(raw).hexdigest() and stream['text'] == expected,
              role + ': exact captured first-refusal output differs')
    _process(record['process_custody'])
    process = record['process_custody']
    _need(before['observed_at_ns'] < process['started_at_ns'] < process['completed_at_ns'] < after['observed_at_ns'],
          'external custody does not bracket genuine process')
    return {
        'schema': 'ri132-entry-evidence-structural-check-v1',
        'status': 'EVIDENCE_CONSISTENCY_ONLY',
        'case_id': case_id, 'coverage': case['coverage'], 'actual_call_boundary': case['function'],
        'exception_type': case['exception_type'], 'message': case['message'],
        'source_attributed_code': case['source_attributed_code'], 'code_observed_in_outer_output': False,
        'genuine_origin_authenticated_by_this_checker': False,
        'independent_origin_review_required': True,
        'deep_source_card_or_scientific_or_eight_object_qualification': False,
        'allocated_attempt_evidence': None, 'complete_changed_caller_qualification': False,
        'scientific_execution_authorized': False, 'full_H30_feasibility': False,
        'external_custody_role_count': len(expected_files),
    }
