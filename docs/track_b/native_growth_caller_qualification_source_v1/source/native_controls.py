"""RI132 native caller controls: unexecuted, direct boundaries only.

The driver authenticates the immutable RI129 module and the current runtime
before loading this source. Nothing here imports that module, writes cards,
changes its globals, or creates copies/attempts. Synthetic dictionaries below
are function arguments, never observations or historical acceptance evidence.
Genuine preparation_ready() populates the caller's own normal metadata cache
only for the five cases explicitly identified as requiring preparation.
"""

from copy import deepcopy


E = '/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0'
R = '/Volumes/AI_DATA/development/det-review-evidence/ri129-native-caller-independent-review-Z0SqaY10'
PYTHON = '/opt/homebrew/bin/python3'
BODY = '/Volumes/AI_DATA/development/det-review-evidence/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json'

# Literal accepted declaration namespace; order and wording are not a result.
DECLARATIONS = (
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


def _case(ident, boundary, code, message, declarations=(), scope='', prepared=False):
    return {
        'id': ident, 'boundary': boundary,
        'expected': {'outcome': 'RETURN' if code is None else 'REFUSED',
                     'exception_type': None if code is None else 'Stop',
                     'code': code, 'message': message},
        'input_kind': ('SYNTHETIC_ARGUMENTS_WITH_GENUINE_PINNED_METADATA_PREPARATION'
                       if prepared else 'SYNTHETIC_ARGUMENTS'),
        'prerequisite_dependent': prepared,
        'declared_controls': list(declarations), 'coverage_scope': scope,
    }


CASES = (
    _case('N01-zero-byte-identity', 'validate_identity', None, None,
          ('history-zero-byte-log-valid',), 'Identity shape permits zero bytes; no historical file is observed.'),
    _case('N02-unavailable-root-identity', 'observed', 'identity',
          'unavailable input identity: source_adjudication', ('missing-root-source-card',),
          'The observed() unavailable-role guard only; no root card or whole entry is exercised.'),
    _case('N03-unavailable-review-identity', 'observed', 'identity',
          'unavailable input identity: independent_source_review', ('missing-independent-review',),
          'The observed() unavailable-role guard only; no review file or whole entry is exercised.'),
    _case('N04-fixed-source-pin', 'source_prerequisites', 'identity',
          'fixed scientific source/input changed', ('changed-scientific-copy',),
          'Correct first original pin and wrong first copy pin reach the copy-size/hash guard; no file exists by implication.'),
    _case('N05-runtime-file-identity', 'runtime_file_prerequisites', 'prerequisite',
          'captured runtime file identity changed: '+PYTHON,
          ('runtime-file-changed', 'changed-runtime-bytes'),
          'Pinned interpreter identity versus a changed synthetic hash, not actual host drift.', True),
    _case('N06-runtime-link-identity', 'runtime_file_prerequisites', 'prerequisite',
          'captured runtime file identity changed: '+PYTHON, ('changed-runtime-links',),
          'Pinned interpreter identity versus a changed synthetic link record, not an actual link replacement.', True),
    _case('N07-historical-identity', 'source_prerequisites', 'prerequisite',
          'historical identity changed', ('changed-historical-file',),
          'A synthetic index agrees with all earlier checks and differs at one historical identity; no current custody claim.', True),
    _case('N08-source-dependency-identity', 'source_prerequisites', 'prerequisite',
          'static source dependency identity changed', ('changed-source-dependency',),
          'One synthetic static dependency identity differs after earlier checks; manifest schema/card parsing is not covered.', True),
    _case('N09-authenticated-metadata-body', 'read_metadata', 'identity',
          'metadata changed before decoding: '+BODY,
          ('transient-current-admission-body', 'transient-saved-witness-body'),
          'Exact raw-body authentication guard on an existing administrative source decision; not transient freeze/addendum races.'),
    _case('N10-bound-current-identity', 'bind', 'prerequisite',
          'complete metadata identity differs: '+E+'/supervise.py', ('wrong-completed-output-reference',),
          'Exact binding equality boundary with inert identities, not completed-review provenance.'),
    _case('N11-unclosed-reference', 'current', 'identity',
          'reference outside closed current inventory: '+E+'/supervise.py',
          ('supplemental-reference-outside-closure',), 'Closed-index lookup only; not traversal of an actual narrative.'),
    _case('N12-freeze-role-order', 'validate_freeze', 'configuration', 'input role order mismatch',
          ('freeze-input-order',),
          'Inert freeze argument passes earlier field/command/supervisor checks then swaps first two role entries; no freeze issued.', True),
    _case('N13-unavailable-witness-identity', 'observed', 'identity',
          'unavailable input identity: witness_receipt', ('premature-normal',),
          'Missing-role argument at observed(); not serial normal entry or genuine witness custody.'),
    _case('N14-unavailable-normal-identity', 'observed', 'identity',
          'unavailable input identity: normal_receipt', ('premature-optimized',),
          'Missing-role argument at observed(); not serial optimized entry or genuine normal custody.'),
    _case('N15-source-only-decision-scope', 'validate_ri128_source_decision', 'prerequisite',
          'RI128 accepted source-only boundary differs', (),
          'Direct RI128 premise-scope validator rejects source_execution=True; this is not the RI129 root-source-card guard.'),
    _case('N16-boolean-byte-count', 'validate_identity', 'configuration',
          'invalid file identity fields', (), 'Identity integer-type guard rejects false-as-zero; no file observation.'),
    _case('N17-authorization-binding', 'validate_authorization', 'authorization',
          'authorization does not bind this attempt', (),
          'First native authorization predicate rejects authorized=False; no deeper addendum guard credited.'),
)


def _identity(path, length=1, digest='1'*64):
    return {'path': str(path), 'resolved_path': str(path), 'bytes': length,
            'sha256': digest, 'symlinks': []}


def _changed_hash(value):
    value['sha256'] = ('0' if value['sha256'][0] != '0' else '1')+value['sha256'][1:]


def _prepared_index(caller):
    # This genuine method reads only the accepted fixed administrative manifests.
    # No caller constant/cache is assigned by this harness.
    caller.preparation_ready()
    index = {}
    def put(identity):
        path = identity['path']
        if path in index and caller.canonical(index[path]) != caller.canonical(identity):
            raise RuntimeError('setup: pinned synthetic identity namespace conflict: '+path)
        index[path] = deepcopy(identity)
    for collection in (caller.RUNTIME_ENTRIES, caller.HISTORY_IDENTITIES, caller.DEPENDENCY_ENTRIES):
        for entry in collection:
            put(entry['identity'])
    for role, original, copy, size, digest in caller.PAIRS:
        put(_identity(original, size, digest))
        put(_identity(copy, size, digest))
    put(caller.RUNTIME_IDENTITY)
    put(_identity(caller.HISTORY, caller.HISTORY_BYTES, caller.HISTORY_SHA256))
    put(_identity(caller.DEPENDENCIES, caller.DEPENDENCIES_BYTES, caller.DEPENDENCIES_SHA256))
    put(_identity(caller.RI128_DECISION, *caller.RI128_DECISION_PIN))
    return index


def _choose_distinct(entries, excluded):
    for item in entries:
        if item['path'] not in excluded:
            return item['path']
    raise RuntimeError('setup: no pinned identity can reach requested boundary without an earlier refusal')


def _action(caller, ident):
    """Return a zero-argument actual boundary call; setup failure is not a pass."""
    path = caller.SELF
    if ident == 'N01-zero-byte-identity':
        value = _identity(path, 0)
        return lambda: caller.validate_identity(value, path)
    roles = {'N02-unavailable-root-identity': 'source_adjudication',
             'N03-unavailable-review-identity': 'independent_source_review',
             'N13-unavailable-witness-identity': 'witness_receipt',
             'N14-unavailable-normal-identity': 'normal_receipt'}
    if ident in roles:
        role = roles[ident]
        before = {role: {'ok': False, 'error': 'RI132 synthetic unavailable-role argument, not a file observation'}}
        return lambda: caller.observed(before, role)
    if ident == 'N04-fixed-source-pin':
        role, original, copy, size, digest = caller.PAIRS[0]
        index = {str(original): _identity(original, size, digest),
                 str(copy): _identity(copy, size, digest)}
        _changed_hash(index[str(copy)])
        return lambda: caller.source_prerequisites(index)
    if ident in ('N05-runtime-file-identity', 'N06-runtime-link-identity',
                 'N07-historical-identity', 'N08-source-dependency-identity'):
        index = _prepared_index(caller)
        if ident == 'N05-runtime-file-identity':
            _changed_hash(index[str(caller.PYTHON)])
            return lambda: caller.runtime_file_prerequisites(index)
        if ident == 'N06-runtime-link-identity':
            index[str(caller.PYTHON)]['symlinks'].append(
                {'path': str(caller.PYTHON), 'target': 'RI132-inert-nonexistent-link-target'})
            return lambda: caller.runtime_file_prerequisites(index)
        earlier = {str(path) for _, original, copy, _, _ in caller.PAIRS for path in (original, copy)}
        earlier.update(item['path'] for item in caller.RUNTIME_ENTRIES)
        earlier.update(str(path) for path in (caller.RUNTIME, caller.RI128_DECISION))
        if ident == 'N07-historical-identity':
            selected = _choose_distinct(caller.HISTORY_IDENTITIES, earlier)
        else:
            earlier.update(item['path'] for item in caller.HISTORY_IDENTITIES)
            earlier.add(str(caller.HISTORY))
            selected = _choose_distinct(caller.DEPENDENCY_ENTRIES, earlier)
        _changed_hash(index[selected])
        return lambda: caller.source_prerequisites(index)
    if ident == 'N09-authenticated-metadata-body':
        path = caller.RI128_DECISION
        value = _identity(path, *caller.RI128_DECISION_PIN)
        _changed_hash(value)
        return lambda: caller.read_metadata(path, {str(path): value})
    if ident == 'N10-bound-current-identity':
        value = _identity(path)
        other = deepcopy(value)
        _changed_hash(other)
        return lambda: caller.bind(value, path, {str(path): other})
    if ident == 'N11-unclosed-reference':
        return lambda: caller.current({}, path)
    if ident == 'N12-freeze-role-order':
        caller.preparation_ready()
        paths = caller.input_paths('witness')
        inputs = [{'role': role, 'path': str(item), 'identity': _identity(item)}
                  for role, item in paths.items()]
        if len(inputs) < 2:
            raise RuntimeError('setup: insufficient fixed roles for order control')
        inputs[0], inputs[1] = inputs[1], inputs[0]
        identity = _identity(caller.SELF)
        before = {'supervisor': {'ok': True, 'identity': identity}}
        config = {'schema': 'ri84-supervisor-freeze-v1', 'mode': 'witness',
                  'supervisor_sha256': identity['sha256'],
                  'supervisor': {'path': str(caller.SELF), 'identity': identity},
                  'argv': caller.argv_for('witness'), 'cwd': str(caller.C),
                  'environment': deepcopy(caller.ENV), 'limits': deepcopy(caller.LIMITS),
                  'authorization': None, 'inputs': inputs, 'interpreter': None,
                  'attempt_dir': str(caller.E/'witness-01')}
        return lambda: caller.validate_freeze(config, 'witness', before)
    if ident == 'N15-source-only-decision-scope':
        value = {'schema': 'ri128-root-proof-source-adjudication-v1',
                 'status': 'ACCEPT_ACTUAL_SCALE_CONTAINMENT_AND_BOUNDED_UNEXECUTED_SIGN_SOURCES',
                 'actual_signs_decided': False, 'full_H30_feasibility': False,
                 'numerical_qualification_accepted': False, 'physical_claim': False,
                 'programme_complete': False, 'resource_feasibility_demonstrated': False,
                 'scientific_body_decode': False, 'source_execution': True, 'ret_paused': True}
        return lambda: caller.validate_ri128_source_decision(value)
    if ident == 'N16-boolean-byte-count':
        value = _identity(path, False)
        return lambda: caller.validate_identity(value, path)
    if ident == 'N17-authorization-binding':
        value = {'schema': 'ri84-execution-authorization-v1', 'authorized': False,
                 'mode': 'witness', 'freeze_payload_sha256': '1'*64,
                 'supervisor_sha256': '1'*64, 'addendum_sha256': None}
        return lambda: caller.validate_authorization(value, {'supervisor_sha256': '1'*64},
                                                    'witness', '1'*64, {})
    raise RuntimeError('unknown native boundary case: '+str(ident))


def run_case(caller, case_id):
    """A narrow result, never a claim that all 52 declarations were exercised."""
    matches = [case for case in CASES if case['id'] == case_id]
    if len(matches) != 1:
        raise RuntimeError('native case must identify exactly one declared boundary')
    case = matches[0]
    action = _action(caller, case_id)  # Outside catch: failed preparation is not qualification.
    expected = case['expected']
    try:
        value = action()
    except BaseException as error:
        if (expected['outcome'] != 'REFUSED' or type(error) is not caller.Stop
                or error.code != expected['code'] or str(error) != expected['message']):
            raise RuntimeError('unexpected native boundary result for '+case_id+': '+
                               type(error).__name__+': '+str(error)) from error
        observed = {'exception_type': type(error).__name__, 'code': error.code, 'message': str(error)}
    else:
        if expected['outcome'] != 'RETURN' or value is not None:
            raise RuntimeError('unexpected native boundary return for '+case_id)
        observed = {'exception_type': None, 'code': None, 'message': None}
    return {'id': case_id, 'boundary': case['boundary'], 'outcome': expected['outcome'],
            'observed': observed, 'coverage_scope': case['coverage_scope'], 'whole_entry': False}


_RETAINED = {
    'runtime-membership-change': ('run -> same(namespace_before, runtime_expected_namespace())',
        'runtime namespace differs before admission',
        'Representative Stop/prerequisite at the retained in-attempt comparison only, after a successful changed preflight. This is not the changed preflight first full-entry refusal or actual directory-mutation coverage.'),
    'runtime-absence-invalid': ('run -> same(namespace_before, runtime_expected_namespace())',
        'runtime namespace differs before admission',
        'Representative Stop/prerequisite at the retained in-attempt comparison only, after a successful changed preflight. The preflight and actual creation of an absent import alternative remain unqualified.'),
    'runtime-host-drift': ('run -> same(namespace_before, runtime_expected_namespace())',
        'runtime namespace differs before admission',
        'Representative Stop/prerequisite at the retained in-attempt aggregate comparison only, after successful changed preflight. The changed preflight and specific earlier host/system-version observation failures are not covered.'),
    'runtime-late-namespace-change': ('run finally -> error record when namespace_stable is false and error is None',
        'fixed runtime namespace or visible host identity changed',
        'Representative error record type Stop/code runtime_namespace_change, not a raised exception. Requires no earlier error; no late namespace or host mutation is executed.'),
    'attempt-output-reuse': ('Attempt.__init__(witness) -> os.mkdir',
        "[Errno 17] File exists: '"+E+"/witness-01'",
        'Representative FileExistsError/errno 17 with no Stop.code for an already existing witness-01 directory. No directory is created; other modes and filesystem failures are untested. Full run requires successful preflight before this constructor.'),
    'late-input-change': ('run finally -> error record when stable is false and error is None',
        'frozen input identities changed during attempt',
        'Representative error record type Stop/code input_change, not a raised exception. Requires no earlier error; no protected file is changed.'),
    'inherited-monitor-failure': ('monitor -> need(reply.returncode == 0 and not reply.stderr)',
        'ps failed or emitted stderr',
        'Representative raised Stop/monitor for a census with nonzero return code and otherwise well-formed subprocess completion. Malformed rows, timeout, absent live child and other monitoring branches remain untested.'),
    'inherited-wall-limit': ('run monitor loop -> first elapsed-time need',
        '120-second child wall limit reached',
        'Representative raised Stop/wall_limit at the first loop deadline guard. The post-sample deadline and monitor remaining-budget guard are different boundaries and are untested; no child is launched.'),
    'inherited-rss-limit': ('run monitor loop -> owned_rss_bytes limit need',
        '512-MiB owned-group RSS limit exceeded',
        'Representative raised Stop/rss_limit after a successful census and deadline check. No allocation fault or child is executed; this remains sampled-group source reasoning only.'),
    'inherited-signal': ('run finally -> error record when RECEIVED_SIGNALS is nonempty and error is None',
        'catchable shutdown signal received during cleanup',
        'Representative error record type Stop/code signal, not an exception raised by stop_signal. With CLOSING=True the handler only records the signal; this later finalization guard invalidates success. Immediate body and deferred launch signal exceptions are different and untested.'),
}
_BLOCKED = {
    'runtime-unbound-manifest': ('reviewed runtime manifest pin is unbound', 'Changing fixed module constants is forbidden.'),
    'runtime-changed-manifest': ('reviewed runtime manifest changed', 'Changing immutable manifest bytes is forbidden.'),
    'unbound-dependency-pin': ('reviewed source dependency manifest pin is unbound', 'Changing fixed module constants is forbidden.'),
    'changed-dependency-manifest': ('reviewed source dependency manifest changed', 'Changing the fixed dependency manifest is forbidden.'),
    'dependency-order-or-duplicate': ('static dependency role/order/path differs', 'Malformed metadata cannot pass the earlier immutable whole-byte pin without a forbidden replacement/rebinding.'),
    'dependency-link-or-alias': ('static source dependency has a symlink or alias', 'Malformed metadata cannot pass the earlier immutable whole-byte pin without a forbidden replacement/rebinding.'),
    'unbound-history-pin': ('reviewed history pin is not bound', 'Changing fixed module constants is forbidden.'),
    'changed-history-manifest': ('reviewed history manifest changed', 'Changing immutable historical manifest bytes is forbidden.'),
    'history-order-or-duplicate': ('historical role/order/path differs', 'Malformed metadata cannot pass the earlier immutable whole-byte pin without a forbidden replacement/rebinding.'),
    'wrong-source-card-scope': ('source adjudication scope differs', 'Inline validator reads an authenticated fixed-path active source card; no argument API exists.'),
    'wrong-source-card-extra-field': ('root source adjudication fields mismatch', 'Inline validator reads an authenticated fixed-path active source card; no argument API exists.'),
    'wrong-applicability-mode': ('stage applicability scope differs', 'Inline validator reads an authenticated fixed-path active applicability card.'),
    'wrong-applicability-argv-env-limits': ('stage applicability command/envelope differs', 'Inline validator first requires genuine authenticated card identities and scope.'),
    'old-target-qualification-credit': ('actual current-target checks absent or old qualification credited', 'Inline completed_mode guard follows genuine receipt/freeze/auth/applicability/source/custody/completion reads; no direct count-validator API.'),
    'future-card-not-completed': ('prior root completed custody scope differs', 'Requires preceding authentic current files/custody; a missing receipt refusal is earlier and does not count.'),
    'receipt-flag-only': ('genuine completed outer zero exit absent', 'Requires preceding authentic current files/custody; a missing receipt refusal is earlier and does not count.'),
    'outer-boolean-zero': ('genuine completed outer zero exit absent', 'Requires preceding authentic current files/custody; no forged outer completion allowed.'),
    'outer-unfinished-session': ('genuine completed outer zero exit absent', 'Requires preceding authentic current files/custody; no forged outer completion allowed.'),
    'outer-invocation-reconstruction': ('actual tool invocation differs from pre-admitted literal invocation', 'Requires preceding authentic current files/custody; no forged outer completion allowed.'),
    'prior-snapshot-role-set': ('prior before/current snapshots differ', 'Requires authenticated fixed-path receipt/freeze/authorization/applicability before snapshot comparison.'),
    'partial-candidate': ('whole candidate differs from genuine witness', 'Requires authenticated candidate custody and genuine witness stdout; no scientific body/copy mutation allowed.'),
    'candidate-math-promotion': ('candidate custody scope differs', 'Requires authenticated fixed-path candidate custody; no fabricated active acceptance card allowed.'),
    'wrong-summary-whole-bytes': ('normal/optimized whole saved summaries differ', 'Requires genuine normal/optimized custody before opaque complete-byte comparison.'),
    'witness-existing-candidate': ('witness mode requires all three new certificates absent', 'Requires fixed-entry environment, interpreter and namespace checks first; no candidate file creation here.'),
    'wrong-outer-cwd-env-flags': ('fixed outer cwd/environment required', 'Representative raised Stop/configuration for incorrect cwd at the changed pre_attempt_prerequisites guard, with platform/source path and earlier preparation valid. No such whole-entry invocation is provided; environment, flags, argv and retained in-attempt alternatives remain untested.'),
}


def _coverage():
    result = []
    for name, function, code, condition in DECLARATIONS:
        first_code = code
        cases = [case for case in CASES if name in case['declared_controls']]
        case_ids = [case['id'] for case in cases]
        if cases:
            classification = 'DIRECT_VALIDATOR_BOUNDARY'
            boundary = [case['boundary'] for case in cases]
            messages = [case['expected']['message'] for case in cases]
            prerequisites = [case['input_kind'] for case in cases]
            gap = 'Only the stated argument boundary is callable; full fixed entry, actual custody and condition-specific filesystem effects remain unqualified.'
            evidence = []
        elif name == 'missing-prerequisite-before-attempt':
            classification = 'WHOLE_UNCHANGED_ENTRY'
            case_ids = ['native-witness-missing-copy']
            boundary = ['pre_attempt_prerequisites -> identity_index -> observed']
            messages = ['unavailable input identity: checker_copy']
            prerequisites = [
                'Prospective entry_evidence.py ENTRY_CASES contract only; no execution observed.',
                'Root-authenticated complete runtime/source/history/dependency closure, exact witness argv/environment/flags, existing empty closure cwd and first checker copy absent.',
                'Real root-owned outer process completion and external complete before/after custody; all attempt paths remain absent.',
            ]
            evidence = []
            gap = ('Only the first missing checker-copy identity guard before Attempt allocation is addressed by the future unchanged entry. '
                   'No source-card, later custody, 15/4/71, admission or in-attempt finally guard is thereby qualified. '
                   'Actual execution and independent external custody review remain pending.')
        elif name in _RETAINED:
            classification = 'RETAINED_ENGINE_APPLICABILITY'
            actual, message, residual = _RETAINED[name]
            boundary, messages = [actual], [message]
            if name == 'attempt-output-reuse':
                first_code = None  # FileExistsError has errno, not Stop.code.
            prerequisites = ['Root adjudication of exact retained text and caller conditions; no current fault execution is supplied.']
            gap = ('Exact retained source reasoning only. No historical count, successful stage or code equality is promoted to fresh executed RI129 fault coverage. '+residual)
            evidence = [{'path': R+'/CORRECTED_METADATA_SUMMARY.json',
                         'bytes': 18478,
                         'sha256': '2d69442db44cea379812c5b4907818b05e0c7008ab6d65061cc84a0a7bc65c04',
                         'selector': 'retained',
                         'scope': 'Independent exact RI122/RI129 block comparisons and single preflight-call insertion; not a whole-program qualification result.'}]
        elif name in _BLOCKED:
            classification = 'BLOCKED_DEEPER'
            message, gap = _BLOCKED[name]
            boundary, messages = [function], [message]
            if name == 'wrong-outer-cwd-env-flags':
                boundary = ['pre_attempt_prerequisites -> fixed outer cwd/environment need']
            prerequisites, evidence = ['The earlier genuine accepted caller prerequisites, without bypass.'], []
        else:
            raise RuntimeError('missing native declaration coverage design: '+name)
        result.append({'declaration': {'name': name, 'function': function, 'code': code, 'condition': condition},
                       'classification': classification, 'case_ids': case_ids,
                       'actual_boundary': boundary, 'intended_first_code': first_code,
                       'intended_first_message': messages, 'prerequisites': prerequisites,
                       'retained_evidence': evidence, 'remaining_gap': gap})
    return tuple(result)


DECLARATION_COVERAGE = _coverage()
