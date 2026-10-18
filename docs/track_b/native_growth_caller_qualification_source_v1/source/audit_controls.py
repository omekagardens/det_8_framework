"""RI132 unexecuted qualification actions for the exact RI129 audit caller.

This module neither imports the caller nor dispatches its main/run entry. The
externally admitted driver supplies the byte-authenticated unchanged module.
Only direct function arguments are fabricated. No source, global or file is
patched. Deferred cases require genuine root-owned three-mode prerequisites;
failure to obtain those prerequisites is NOT the intended refusal or a pass.
"""

from copy import deepcopy


CALLER_PATH = '/Volumes/AI_DATA/development/det-review-evidence/ri129-native-sign-caller-source-8TksBLo0/launch_audit.py'
CALLER_BYTES = 103287
CALLER_SHA256 = '5263099d45d9ed021a80d65029da511ad9019d30892278b1b412cb1794465ae5'
REVIEW_PATH = '/Volumes/AI_DATA/development/det-review-evidence/ri129-native-caller-independent-review-Z0SqaY10/INDEPENDENT_SOURCE_REVIEW.md'
REVIEW_SHA256 = '19d74caf5807a4d781bfac97959c2f791d9c181914496e0504145a321132f7eb'
FIRST_RUNTIME_PATH = '/System/Library/CoreServices/SystemVersion.plist'
ZERO_LOG_SHA256 = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

# Exact ordered source declarations, not executed outcomes.
DECLARATIONS = (
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


def _case(identifier, boundary, message=None, code=None, declarations=(),
          input_kind='FABRICATED_ARGUMENT_ONLY', scope='DIRECT_VALIDATOR_BOUNDARY'):
    return {
        'id': identifier, 'boundary': boundary,
        'expected': {'outcome': 'RETURN' if message is None else 'REFUSED',
                     'exception_type': None if message is None else 'Stop',
                     'code': code, 'message': message},
        'input_kind': input_kind, 'declared_controls': list(declarations),
        'coverage_scope': scope,
        'prerequisite_dependent': scope == 'PREREQUISITE_DEPENDENT_DIRECT',
    }


CASES = (
    _case('audit-binding-null', 'positive_identity', 'file identity fields mismatch',
          'configuration', ('binding-null-identity',)),
    _case('audit-binding-zero-size', 'positive_identity',
          'nonpositive or placeholder identity: '+CALLER_PATH.rsplit('/', 1)[0]+'/AUDIT_BINDING.json',
          'preparation', ('binding-zero-size',)),
    _case('audit-binding-zero-digest', 'positive_identity',
          'nonpositive or placeholder identity: '+CALLER_PATH.rsplit('/', 1)[0]+'/AUDIT_BINDING.json',
          'preparation', ('binding-zero-digest',)),
    _case('audit-binding-arbitrary-path', 'positive_identity', 'invalid file identity fields',
          'configuration', ('binding-arbitrary-path',)),
    _case('audit-history-empty-log-identity', 'validate_identity',
          declarations=('history-zero-log-valid',)),
    _case('audit-auth-false', 'validate_authorization',
          'authorization does not bind this one audit attempt', 'authorization',
          ('missing-explicit-auth',)),
    _case('audit-unclosed-reference', 'bind_refs',
          'metadata reference outside closed frozen inventory', 'identity',
          ('metadata-unclosed-reference',)),
    _case('audit-runtime-file-argument-change', 'runtime_file_prerequisites',
          'captured runtime file identity changed: '+FIRST_RUNTIME_PATH, 'identity',
          ('runtime-file-changed',), 'AUTHENTIC_RUNTIME_MANIFEST_PLUS_FABRICATED_ARGUMENT'),
    _case('audit-runtime-index-positive', 'runtime_file_prerequisites',
          input_kind='AUTHENTIC_RUNTIME_MANIFEST_PLUS_DECLARED_IDENTITY_ARGUMENT',
          scope='SUPPLEMENTAL_COMPONENT_ONLY'),
    _case('audit-dependency-prepare-positive', 'dependency_prepare',
          input_kind='AUTHENTIC_IMMUTABLE_DEPENDENCY_MANIFEST',
          scope='SUPPLEMENTAL_COMPONENT_ONLY'),
    _case('audit-preflight-wrong-mode', 'pre_attempt_prerequisites',
          'fixed preflight mode changed', 'configuration', scope='SUPPLEMENTAL_COMPONENT_ONLY'),
    _case('audit-ri128-promotion', 'validate_ri128_source_decision',
          'RI128 accepted source-only boundary differs', 'prerequisite',
          scope='SUPPLEMENTAL_COMPONENT_ONLY'),
    _case('audit-no-argument-argv', 'argv_for',
          input_kind='AUTHENTIC_FUTURE_THREE_MODE_PREREQUISITES',
          scope='PREREQUISITE_DEPENDENT_DIRECT'),
    _case('audit-target-path-argument', 'validate_authorization',
          'target object must be positive bounded literal nonsymlink file: auditor_copy',
          'identity', ('target-path-alias',), 'AUTHENTIC_FUTURE_CONTEXT_PLUS_FABRICATED_ARGUMENT',
          'PREREQUISITE_DEPENDENT_DIRECT'),
    _case('audit-target-symlink-argument', 'validate_authorization',
          'target object must be positive bounded literal nonsymlink file: auditor_copy',
          'identity', ('target-symlink',), 'AUTHENTIC_FUTURE_CONTEXT_PLUS_FABRICATED_ARGUMENT',
          'PREREQUISITE_DEPENDENT_DIRECT'),
    _case('audit-target-oversize-argument', 'validate_authorization',
          'target object must be positive bounded literal nonsymlink file: auditor_copy',
          'identity', ('target-oversize',), 'AUTHENTIC_FUTURE_CONTEXT_PLUS_FABRICATED_ARGUMENT',
          'PREREQUISITE_DEPENDENT_DIRECT'),
)


def _identity(path, count=1, checksum='1'*64):
    """An argument only: never a file observation, accepted card or custody."""
    return {'path': str(path), 'resolved_path': str(path), 'bytes': count,
            'sha256': checksum, 'symlinks': []}


def _runtime_index(caller):
    caller.runtime_prepare()  # The real loader authenticates the immutable pin.
    entries = caller.RUNTIME_ENTRIES
    if not entries or entries[0]['path'] != FIRST_RUNTIME_PATH:
        raise RuntimeError('unexpected authenticated runtime first role')
    known = {item['path']: deepcopy(item['identity']) for item in entries}
    known[str(caller.RUNTIME)] = deepcopy(caller.RUNTIME_IDENTITY)
    return known


def _future_audit_context(caller):
    """Read authentic future artifacts; neither manufacture nor authorize them.

    Failures here escape the intended-control catcher. A qualification driver
    must mark the case blocked/error, never the requested deeper guard passed.
    Root independently owns authenticity and eligibility of actual prior runs.
    """
    caller.preparation_ready()
    paths = dict(caller.input_paths('audit'), interpreter=caller.PYTHON,
                 supervisor=caller.SELF,
                 freeze=caller.E/'AUDIT_EXECUTION_FREEZE.json',
                 authorization=caller.E/'AUDIT_AUTHORIZATION.json')
    before = caller.snapshot(paths)
    for role in paths:
        caller.observed(before, role)
    config = caller.metadata(paths['freeze'], caller.observed(before, 'freeze'),
                             allow_floats=False)
    payload = caller.validate_freeze(config, 'audit', before)
    auth = caller.metadata(paths['authorization'], caller.observed(before, 'authorization'),
                           allow_floats=False)
    return auth, config, payload, before


def _action(caller, identifier):
    """Prepare arguments outside the outcome catcher; return the exact call."""
    if identifier == 'audit-binding-null':
        return lambda: caller.positive_identity(None, caller.AUDIT_BINDING)
    if identifier == 'audit-binding-zero-size':
        value = _identity(caller.AUDIT_BINDING, 0)
        return lambda: caller.positive_identity(value, caller.AUDIT_BINDING)
    if identifier == 'audit-binding-zero-digest':
        value = _identity(caller.AUDIT_BINDING, checksum='0'*64)
        return lambda: caller.positive_identity(value, caller.AUDIT_BINDING)
    if identifier == 'audit-binding-arbitrary-path':
        value = _identity(caller.E/'NOT_AN_ACTUAL_BINDING.json')
        return lambda: caller.positive_identity(value, caller.AUDIT_BINDING)
    if identifier == 'audit-history-empty-log-identity':
        value = _identity(caller.E/'NOT_AN_ACTUAL_HISTORICAL_LOG', 0, ZERO_LOG_SHA256)
        path = caller.E/'NOT_AN_ACTUAL_HISTORICAL_LOG'
        return lambda: caller.validate_identity(value, path)
    if identifier == 'audit-auth-false':
        value = {'schema': 'ri95-certificate-audit-authorization-v1', 'authorized': False,
                 'mode': 'audit', 'freeze_payload_sha256': '1'*64, 'supervisor_sha256': '1'*64}
        return lambda: caller.validate_authorization(value, {'supervisor_sha256': '1'*64},
                                                       'audit', '1'*64, {})
    if identifier == 'audit-unclosed-reference':
        value = _identity(caller.E/'NOT_A_CLOSED_REFERENCE')
        return lambda: caller.bind_refs(value, {})
    if identifier in ('audit-runtime-file-argument-change', 'audit-runtime-index-positive'):
        known = _runtime_index(caller)
        if identifier == 'audit-runtime-file-argument-change':
            known[FIRST_RUNTIME_PATH]['sha256'] = '0'*64
        return lambda: caller.runtime_file_prerequisites(known)
    if identifier == 'audit-dependency-prepare-positive':
        if caller.DEPENDENCY_ENTRIES is not None:
            raise RuntimeError('fresh module required; cached dependency preparation is not coverage')
        return caller.dependency_prepare
    if identifier == 'audit-preflight-wrong-mode':
        return lambda: caller.pre_attempt_prerequisites('not-audit')
    if identifier == 'audit-ri128-promotion':
        value = {
            'schema': 'ri128-root-proof-source-adjudication-v1',
            'status': 'ACCEPT_ACTUAL_SCALE_CONTAINMENT_AND_BOUNDED_UNEXECUTED_SIGN_SOURCES',
            'actual_signs_decided': False, 'full_H30_feasibility': False,
            'numerical_qualification_accepted': False, 'physical_claim': False,
            'programme_complete': False, 'resource_feasibility_demonstrated': False,
            'scientific_body_decode': False, 'source_execution': True, 'ret_paused': True,
        }
        return lambda: caller.validate_ri128_source_decision(value)
    if identifier == 'audit-no-argument-argv':
        caller.preparation_ready()  # A missing binding is not no-argument coverage.
        def no_argument():
            result = caller.argv_for('audit')
            expected = [str(caller.PYTHON), '-I', '-S', '-B', str(caller.TARGET)]
            if type(result) is not list or result != expected or len(result) != 5:
                raise RuntimeError('actual argv_for did not return the exact no-argument target vector')
        return no_argument
    if identifier in ('audit-target-path-argument', 'audit-target-symlink-argument',
                      'audit-target-oversize-argument'):
        auth, config, payload, before = _future_audit_context(caller)
        changed = deepcopy(before)
        item = changed['auditor_copy']['identity']
        if identifier == 'audit-target-path-argument':
            item['path'] = str(caller.B/'NOT_AN_ACTUAL_AUDITOR.py')
            item['resolved_path'] = item['path']
        elif identifier == 'audit-target-symlink-argument':
            item['symlinks'] = [{'path': str(caller.TARGET), 'target': 'NOT_AN_ACTUAL_SYMLINK'}]
        else:
            item['bytes'] = 8388609
        return lambda: caller.validate_authorization(auth, config, 'audit', payload, changed)
    raise RuntimeError('unknown closed audit qualification case: '+str(identifier))


def run_case(caller, case_id):
    """One fresh imported module per case; genuine external admission required.

    Returning means only this direct boundary met its exact expectation. The
    result cannot establish whole-entry custody, actual target qualification,
    prior-run truth, physical alias handling or scientific acceptance.
    """
    choices = [item for item in CASES if item['id'] == case_id]
    if len(choices) != 1:
        raise RuntimeError('unknown or duplicate closed audit case')
    if tuple(caller.CONTROL_DECLARATIONS) != DECLARATIONS:
        raise RuntimeError('audit declaration inventory differs from accepted source')
    case = choices[0]
    action = _action(caller, case_id)  # Prerequisite failure is never case success.
    observed = {'exception_type': None, 'code': None, 'message': None}
    outcome = 'RETURN'
    try:
        value = action()
    except Exception as error:
        outcome = 'REFUSED'
        observed = {'exception_type': type(error).__name__,
                    'code': getattr(error, 'code', None), 'message': str(error)}
        if type(error) is not caller.Stop:
            raise RuntimeError('unexpected non-Stop exception at '+case['boundary']) from error
    else:
        if value is not None:
            raise RuntimeError('direct audit validator unexpectedly returned a non-None result')
    expected = case['expected']
    if outcome != expected['outcome'] or observed != {
            key: expected[key] for key in ('exception_type', 'code', 'message')}:
        raise RuntimeError('audit qualification first outcome differs: '+case_id+'; '+repr(observed))
    return {'id': case_id, 'boundary': case['boundary'], 'outcome': outcome,
            'observed': observed, 'coverage_scope': case['coverage_scope'], 'whole_entry': False}


# A retained source comparison is evidence of implementation applicability,
# never evidence that this changed entry or these fault cases were executed.
_RETAINED = {
    'kind': 'EXACT_RETAINED_CODE_APPLICABILITY_ONLY', 'path': REVIEW_PATH,
    'sha256': REVIEW_SHA256,
    'scope': 'Complete accepted nonauthor review: runtime helpers, identity/metadata helpers and Attempt/monitor/termination retained; run/main retained after removing only new preflight call.',
    'changed_entry_qualification_transferred': False,
    'individual_historical_fault_outcome_claimed': False,
}
_RUNTIME_PREREQUISITE = 'External pre-bootstrap runtime authentication; fresh immutable caller import; authentic fixed runtime manifest.'
_DEEP_PREREQUISITE = 'Genuine root-owned current source/applicability/freezes/authorization, exact copies, runtime/history/dependency closure and all required serial custody; no fabricated cards.'

# Every message below names a concrete intended guard. Where a declaration
# covers alternatives, one named representative is selected and the remaining
# alternatives are explicitly not claimed covered.
_DETAILS = {
    'runtime-unbound-manifest': ('runtime_prepare', 'preparation', 'reviewed runtime manifest pin is unbound', 'Pinned globals cannot be altered; unchanged helper applicability only.'),
    'runtime-changed-manifest': ('runtime_prepare', 'runtime', 'reviewed runtime manifest changed', 'No immutable manifest is changed; raw-read race alternative is not exercised.'),
    'runtime-membership-change': ('pre_attempt_prerequisites -> same', 'identity', 'preflight runtime namespace differs', 'Full-entry now rejects at preflight; no namespace mutation or new-entry coverage.'),
    'runtime-absence-invalid': ('pre_attempt_prerequisites -> same', 'identity', 'preflight runtime namespace differs', 'No forbidden import alternative is created; preflight path is new.'),
    'runtime-host-drift': ('pre_attempt_prerequisites -> same', 'identity', 'preflight runtime namespace differs', 'No host premise is altered; specific earlier system-version identity refusal may precede this aggregate guard.'),
    'runtime-file-changed': ('runtime_file_prerequisites', 'identity', 'captured runtime file identity changed: '+FIRST_RUNTIME_PATH, 'Direct synthetic identity-map argument only; no actual runtime file mutation or full-entry claim.'),
    'runtime-late-namespace-change': ('run finally', 'runtime_namespace_change', 'fixed runtime namespace or visible host identity changed', 'No late host/namespace mutation; retained finalizer only, conditional on no earlier error.'),
    'unbound-dependency-pin': ('dependency_prepare', 'preparation', 'reviewed source dependency manifest pin is unbound', 'Requires forbidden mutation of accepted globals; positive authentic preparation does not cover this.'),
    'changed-dependency-manifest': ('dependency_prepare', 'dependency', 'reviewed source dependency manifest changed', 'No immutable dependency file mutation; positive preparation is not this fault.'),
    'dependency-order-or-duplicate': ('dependency_prepare', 'dependency', 'static dependency role/order/path differs', 'Authenticated whole-file pin precedes parsing; changing order first changes the pin.'),
    'dependency-link-or-alias': ('dependency_prepare', 'dependency', 'static source dependency has a symlink or alias', 'Whole-file authentication precedes entry checks; cannot manufacture an accepted changed manifest.'),
    'changed-source-dependency': ('verify_source_cards', 'identity', 'static source dependency identity changed', 'Runtime and exact nine source/copy pairs precede dependency loop; not called with missing physical prerequisites.'),
    'old-target-qualification-credit': ('validate_mode_custodies', 'prerequisite', 'actual current-target checks absent or old qualification credited', 'Current15/4/71 checks are inline after genuine serial metadata; an earlier binding/auth failure is not coverage.'),
    'pre-attempt-missing-or-invalid-prerequisite': ('main -> preparation_ready -> file_identity(AUDIT_BINDING)', None, "[Errno 2] No such file or directory: '"+CALLER_PATH.rsplit('/', 1)[0]+"/AUDIT_BINDING.json'", 'Root whole-entry missing-binding case is separately specified; it does not reach full pre_attempt_prerequisites or prove every gate.'),
    'unbound-history': ('preparation_ready', 'preparation', 'reviewed historical manifest pin is unbound', 'Requires forbidden accepted-global mutation.'),
    'changed-history': ('preparation_ready', 'identity', 'reviewed historical manifest changed', 'Requires forbidden immutable historical manifest change; raw authentication must remain first.'),
    'missing-binding': ('main -> preparation_ready -> file_identity(AUDIT_BINDING)', None, "[Errno 2] No such file or directory: '"+CALLER_PATH.rsplit('/', 1)[0]+"/AUDIT_BINDING.json'", 'Root-owned whole-entry specification/evidence validator only; no run or current outer result in this module.'),
    'binding-extra-key': ('preparation_ready', 'preparation', 'actual audit binding fields mismatch', 'Needs changed physical current binding; no fake actual binding card is created.'),
    'binding-null-identity': ('positive_identity -> validate_identity -> exact_keys', 'configuration', 'file identity fields mismatch', 'Only direct argument shape; no loaded binding-card coverage.'),
    'binding-zero-size': ('positive_identity', 'preparation', 'nonpositive or placeholder identity: '+CALLER_PATH.rsplit('/', 1)[0]+'/AUDIT_BINDING.json', 'Only direct argument identity; no physical zero-byte binding file.'),
    'binding-zero-digest': ('positive_identity', 'preparation', 'nonpositive or placeholder identity: '+CALLER_PATH.rsplit('/', 1)[0]+'/AUDIT_BINDING.json', 'Only direct argument identity; no physical placeholder binding file.'),
    'binding-arbitrary-path': ('positive_identity -> validate_identity', 'configuration', 'invalid file identity fields', 'Only direct argument identity; no actual path substitution.'),
    'binding-missing-mode': ('preparation_ready -> exact_keys', 'preparation', 'custodies fields mismatch', 'Representative missing custodies.optimized requires a fabricated/changed binding; outer_completions alternative not tested.'),
    'binding-changed-after-cache': ('validate_authorization -> same', 'identity', 'actual binding changed after preparation', 'No actual binding mutation after cache; needs genuine prepared state.'),
    'missing-custody': ('preparation_ready -> file_identity(E/WITNESS_ROOT_CUSTODY.json)', None, "[Errno 2] No such file or directory: '"+CALLER_PATH.rsplit('/', 1)[0]+"/WITNESS_ROOT_CUSTODY.json'", 'Selected missing first producer custody presumes all preceding genuine binding references; none is manufactured.'),
    'history-order': ('preparation_ready', 'configuration', 'historical ordered role or path changed', 'Selected role-order violation is behind immutable history pin; sorted-path alternative also unexecuted.'),
    'history-duplicate': ('preparation_ready', 'configuration', 'historical ordered role or path changed', 'Duplicate path occurs behind immutable history pin; no bypass.'),
    'history-zero-log-valid': ('validate_identity', None, None, 'Direct identity-shape acceptance only; argument is not an observed historical output.'),
    'changed-protected-file': ('verify_source_cards -> same', 'identity', 'historical protected identity changed', 'Genuine runtime/source-copy prerequisites required; no historical file mutation.'),
    'changed-copy': ('verify_source_cards', 'identity', 'accepted RI128 pair changed: checker/copy', 'Representative changed checker-copy pin; no copy created/changed; whole-byte mismatch subguard is distinct.'),
    'source-decision-extra-field': ('verify_source_cards -> exact_keys', 'prerequisite', 'RI129 source decision fields mismatch', 'Physical metadata is authenticated before inline shape check; no fake current decision.'),
    'source-decision-promotion': ('verify_source_cards', 'prerequisite', 'RI129 source decision is not exact source-only acceptance', 'RI128 direct promotion case is different and receives no credit for this RI129 card guard.'),
    'source-review-incomplete': ('verify_source_cards', 'prerequisite', 'complete independent source review absent', 'No changed physical independent source review or card is supplied.'),
    'stage-wrong-mode': ('verify_applicability', 'prerequisite', 'fixed stage applicability scope differs: audit', 'Current authenticated physical stage card required; no fabricated historical admission.'),
    'stage-wrong-argv': ('verify_applicability -> same', 'identity', 'stage argv differs', 'Current actual binding/preparation and stage card required; noarg vector positive case is narrower.'),
    'stage-wrong-env-limits': ('verify_applicability -> same', 'identity', 'stage environment differs', 'Representative environment guard; resource-envelope alternative remains separately untested.'),
    'freeze-input-order': ('validate_freeze', 'configuration', 'input role order mismatch', 'Same-length reordered inputs selected; argv_for first requires real audit preparation.'),
    'freeze-raw-body-mismatch': ('metadata', 'identity', 'metadata raw bytes differ from authenticated identity', 'Exact retained metadata helper only; current freeze path not fabricated or changed.'),
    'authorization-raw-body-mismatch': ('metadata', 'identity', 'metadata raw bytes differ from authenticated identity', 'Exact retained metadata helper only; current authorization path not fabricated or changed.'),
    'runtime-link-change': ('validate_freeze', 'identity', 'interpreter identity mismatch', 'Selected interpreter identity field mismatch; earlier frozen runtime-role mismatch may be first in other mutations.'),
    'missing-explicit-auth': ('validate_authorization', 'authorization', 'authorization does not bind this one audit attempt', 'Only false authorized argument at first guard; no binding/eight-object/custody coverage.'),
    'target-path-alias': ('validate_authorization eight-object value guard', 'identity', 'target object must be positive bounded literal nonsymlink file: auditor_copy', 'Deferred genuine context plus wrong-path argument only; no actual filesystem path alias created.'),
    'target-physical-alias': ('validate_authorization device/inode guard', 'identity', 'target objects share a physical identity: checker_copy', 'Requires real hardlink/physical fault among protected files; none authorized or fabricated.'),
    'target-symlink': ('validate_authorization eight-object value guard', 'identity', 'target object must be positive bounded literal nonsymlink file: auditor_copy', 'Deferred nonempty symlinks argument only; actual component traversal/fault remains untested.'),
    'target-oversize': ('validate_authorization eight-object value guard', 'identity', 'target object must be positive bounded literal nonsymlink file: auditor_copy', 'Deferred oversized identity argument only; no oversized scientific body created/read.'),
    'target-certificate-binding': ('validate_authorization certificate guard', 'authorization', 'actual native saved certificate differs from audit binding', 'Earlier bind_refs(BINDING_VALUE,known) catches an inconsistent certificate argument; cannot credit that as reaching this guard.'),
    'serial-receipt-only': ('validate_mode_custodies -> exact_keys', 'prerequisite', 'completed root custody fields mismatch', 'Representative receipt-shaped dict in custody position requires fabricated current custody file; real missing file fails earlier.'),
    'serial-omitted-prior': ('validate_mode_custodies -> same', 'identity', 'completed serial custody dependency differs', 'Representative optimized root_normal_acceptance=null after valid keys; genuine prior cards remain necessary.'),
    'native-false-zero': ('validate_producer_receipts', 'prerequisite', 'successful native completion absent: witness', 'Inline actual receipt validator, not a separable argument callback; no fabricated receipt file.'),
    'native-role-trailer': ('validate_producer_receipts', 'configuration', 'native complete ordered input list differs', 'Inline current freeze with malformed trailer cannot be substituted as history.'),
    'native-before-after-change': ('validate_producer_receipts -> same', 'identity', 'native before/current identity map differs', 'Representative before map; after map has a different first message and is also untested.'),
    'native-empty-live-samples': ('validate_producer_receipts', 'prerequisite', 'successful native completion absent: witness', 'Zero live_rss_samples fails first receipt guard, not later census totals.'),
    'native-no-terminal-absence': ('validate_producer_receipts', 'prerequisite', 'native live/terminal sampled custody is incomplete', 'Actual authenticated sample file is required; no synthetic process history.'),
    'native-candidate-during-witness': ('validate_producer_receipts -> same', 'identity', 'native candidate absence at admission differs', 'Representative prepared absence mismatch after prior guards; no actual witness history alteration.'),
    'candidate-partial': ('validate_mode_custodies', 'identity', 'candidate copy differs from whole witness bytes', 'Requires altered candidate bytes and genuine earlier stages; no candidate is created/changed.'),
    'saved-summary-difference': ('validate_mode_custodies', 'identity', 'whole normal/optimized summaries differ', 'Requires changed real summary bytes; no scientific body is decoded/altered.'),
    'outer-wrong-literal-invocation': ('validate_mode_custodies -> same', 'identity', 'genuine invocation differs from pre-admitted literal command', 'No fabricated tool-completion record; root actual output truth is separately external.'),
    'outer-false-zero': ('validate_mode_custodies', 'prerequisite', 'actual outer exit/chunk incomplete', 'Representative completion.result.exit_code=false; custody.actual_outer_exit=false fails earlier scope guard.'),
    'outer-unfinished-session': ('validate_mode_custodies', 'prerequisite', 'actual outer exit/chunk incomplete', 'Presence of session_id is rejected even if null; no fabricated completion supplied.'),
    'outer-receipt-mismatch': ('validate_mode_custodies -> same', 'identity', 'genuine outer success does not bind exact receipt', 'Requires different raw genuine output binding; not inferred from receipt status.'),
    'review-missing-output': ('validate_mode_custodies -> same', 'identity', 'completed review must bind all six evidence files', 'Authenticated actual completed-review file required; no fake review.'),
    'metadata-unclosed-reference': ('bind_refs', 'identity', 'metadata reference outside closed frozen inventory', 'Direct argument reference only; no metadata file discovery or accepted card.'),
    'attempt-reuse': ('Attempt.__init__ -> os.mkdir', None, "[Errno 17] File exists: '"+CALLER_PATH.rsplit('/', 1)[0]+"/audit-01'", 'No actual attempt directory is created; full entry additionally needs successful fresh preflight.'),
    'wrong-launch-environment': ('pre_attempt_prerequisites', 'configuration', 'preflight environment, flags, argv or cwd changed', 'New preflight precedes retained run guard; all genuine earlier prerequisites required to reach it.'),
    'monitor-failure': ('monitor', 'monitor', 'ps failed or emitted stderr', 'Representative nonzero/stderr census; malformed/timeout alternative has distinct messages and no current execution.'),
    'wall-limit': ('run monitor loop', 'wall_limit', '120-second child wall limit reached', 'No owned process launched; monitor remaining-budget guard has distinct first message.'),
    'rss-limit': ('run monitor loop', 'rss_limit', '512-MiB owned-group RSS limit exceeded', 'No memory-allocation fault or child run; applicability is retained sampled-group code only.'),
    'late-input-change': ('run finally', 'input_change', 'frozen input identities changed during attempt', 'Conditional on no earlier error; no late protected-file mutation.'),
    'late-signal': ('run finally', 'signal', 'catchable shutdown signal received during cleanup', 'Representative cleanup signal; launch/body signal paths have different messages and remain unexecuted.'),
}

_RETAINED_NAMES = frozenset((
    'runtime-unbound-manifest', 'runtime-changed-manifest',
    'runtime-late-namespace-change', 'freeze-raw-body-mismatch',
    'authorization-raw-body-mismatch', 'runtime-link-change', 'attempt-reuse',
    'monitor-failure', 'wall-limit', 'rss-limit', 'late-input-change', 'late-signal',
))
_WHOLE_ENTRY_NAMES = frozenset(('missing-binding',))


def _coverage(declaration):
    name, function, code, condition = declaration
    actual, first_code, message, gap = _DETAILS[name]
    cases = [item for item in CASES if name in item['declared_controls']]
    direct = [item for item in cases if item['coverage_scope'] == 'DIRECT_VALIDATOR_BOUNDARY']
    if direct:
        classification = 'DIRECT_VALIDATOR_BOUNDARY'
    elif name in _WHOLE_ENTRY_NAMES:
        classification = 'WHOLE_UNCHANGED_ENTRY'
    elif name in _RETAINED_NAMES:
        classification = 'RETAINED_ENGINE_APPLICABILITY'
    else:
        classification = 'BLOCKED_DEEPER'
    return {
        'declaration': {'name': name, 'function': function, 'code': code, 'condition': condition},
        'classification': classification,
        'case_ids': (['audit-missing-binding'] if name in _WHOLE_ENTRY_NAMES else
                     [item['id'] for item in cases]),
        'actual_boundary': actual, 'intended_first_code': first_code,
        'intended_first_message': message,
        'prerequisites': (_RUNTIME_PREREQUISITE if name == 'runtime-file-changed' else
                          'External authenticated fresh module; direct arguments are not evidence.' if direct else
                          'Root actual unchanged entry dispatch under closed before/after external custody; authentic manifests; AUDIT_BINDING.json absent.' if name in _WHOLE_ENTRY_NAMES else
                          _DEEP_PREREQUISITE),
        'retained_evidence': [dict(_RETAINED)] if name in _RETAINED_NAMES else [],
        'remaining_gap': gap,
    }


DECLARATION_COVERAGE = tuple(_coverage(item) for item in DECLARATIONS)
