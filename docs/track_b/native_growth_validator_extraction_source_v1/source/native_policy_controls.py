"""RI134 unexecuted direct tests of the four actual native policy functions.

No loader, CLI, file access, preparation, production admission or monkeypatch.
Every dictionary is an explicitly fabricated argument, not a custody record.
The future caller object must be authenticated by the separately admitted owner.
"""

from copy import deepcopy


E = '/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde'
ANCESTRY = '/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx'
RI128_DECISION = '/Volumes/AI_DATA/development/det-review-evidence/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json'


FUNCTIONS = {
    'dependency': 'validate_dependency_payload',
    'decision': 'validate_source_decision_payload',
    'review': 'validate_source_review_payload',
    'checks': 'validate_current_target_checks',
}


def _case(ident, family, mutation, code=None, message=None, declarations=()):
    return {'id': ident, 'family': family, 'boundary': FUNCTIONS[family],
            'mutation': mutation, 'input_kind': 'FABRICATED_IN_MEMORY_POLICY_ARGUMENTS_ONLY',
            'expected': {'outcome': 'RETURN' if code is None else 'REFUSED',
                         'exception_type': None if code is None else 'Stop',
                         'code': code, 'message': message,
                         'return_kind': ('new_list_of_same_validated_entry_objects' if family == 'dependency'
                                         else 'None') if code is None else None},
            'declared_controls': list(declarations),
            'whole_entry': False, 'executed_in_source_preparation': False}


CASES = (
    _case('D00-positive', 'dependency', 'none'),
    _case('D01-extra-root-key', 'dependency', 'extra-root-key', 'dependency', 'static source dependency manifest fields mismatch'),
    _case('D02-wrong-schema', 'dependency', 'schema', 'dependency', 'static source dependency manifest schema differs'),
    _case('D03-wrong-status', 'dependency', 'status', 'dependency', 'static source dependency manifest schema differs'),
    _case('D04-promoted-scope', 'dependency', 'scope', 'prerequisite', 'static source dependency scope differs'),
    _case('D05-empty-closure', 'dependency', 'empty', 'dependency', 'static source dependency closure is empty'),
    _case('D06-nonlist-closure', 'dependency', 'nonlist', 'dependency', 'static source dependency closure is empty'),
    _case('D07-extra-entry-key', 'dependency', 'extra-entry-key', 'dependency', 'static source dependency entry fields mismatch'),
    _case('D08-role-order', 'dependency', 'role', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('D09-relative-path', 'dependency', 'relative', 'dependency', 'static dependency role/order/path differs'),
    _case('D10-noncanonical-path', 'dependency', 'noncanonical', 'dependency', 'static dependency role/order/path differs'),
    _case('D11-nontext-path', 'dependency', 'nontext', 'dependency', 'static dependency role/order/path differs'),
    _case('D12-descending-paths', 'dependency', 'descending', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('D13-duplicate-path', 'dependency', 'duplicate', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('D14-identity-extra-key', 'dependency', 'identity-extra', 'configuration', 'file identity fields mismatch'),
    _case('D15-identity-path', 'dependency', 'identity-path', 'configuration', 'invalid file identity fields'),
    _case('D16-boolean-size', 'dependency', 'identity-bool-size', 'configuration', 'invalid file identity fields'),
    _case('D17-negative-size', 'dependency', 'identity-negative-size', 'configuration', 'invalid file identity fields'),
    _case('D18-invalid-digest', 'dependency', 'identity-digest', 'configuration', 'invalid file identity fields'),
    _case('D19-link-shape', 'dependency', 'link-shape', 'configuration', 'symlink identity fields mismatch'),
    _case('D20-resolved-alias', 'dependency', 'alias', 'dependency', 'static source dependency has a symlink or alias', ('dependency-link-or-alias',)),
    _case('D21-valid-link-record', 'dependency', 'link', 'dependency', 'static source dependency has a symlink or alias', ('dependency-link-or-alias',)),
    _case('D22-empty-classification', 'dependency', 'classification', 'dependency', 'static dependency provenance field types differ'),
    _case('D23-empty-access-policy', 'dependency', 'access-policy', 'dependency', 'static dependency provenance field types differ'),
    _case('D24-nonlist-provenance', 'dependency', 'provenance', 'dependency', 'static dependency provenance field types differ'),
    _case('S00-positive', 'decision', 'none'),
    _case('S01-extra-key', 'decision', 'extra-root-key', 'prerequisite', 'root source adjudication fields mismatch', ('wrong-source-card-extra-field',)),
    _case('S02-missing-key', 'decision', 'missing-root-key', 'prerequisite', 'root source adjudication fields mismatch'),
    _case('S03-wrong-schema', 'decision', 'schema', 'prerequisite', 'source adjudication scope differs'),
    _case('S04-wrong-status', 'decision', 'status', 'prerequisite', 'source adjudication scope differs'),
    _case('S05-execution-promotion', 'decision', 'execution', 'prerequisite', 'source adjudication scope differs', ('wrong-source-card-scope',)),
    _case('S06-execution-zero', 'decision', 'execution-zero', 'prerequisite', 'source adjudication scope differs'),
    _case('S07-inherited-qualification', 'decision', 'inherited', 'prerequisite', 'source adjudication scope differs', ('wrong-source-card-scope',)),
    _case('S08-source-role-omitted', 'decision', 'source-role', 'prerequisite', 'accepted caller sources fields mismatch'),
    _case('S09-early-scope-before-lookup', 'decision', 'scope-and-empty-index', 'prerequisite', 'source adjudication scope differs'),
    _case('S10-supervisor-binding', 'decision', 'binding:native_supervisor', 'prerequisite', 'complete metadata identity differs: '+E+'/supervise.py'),
    _case('S11-auditor-binding', 'decision', 'binding:audit_caller', 'prerequisite', 'complete metadata identity differs: '+E+'/launch_audit.py'),
    _case('S12-history-binding', 'decision', 'binding:history_manifest', 'prerequisite', 'complete metadata identity differs: '+ANCESTRY+'/HISTORY_RECONCILIATION.json'),
    _case('S13-runtime-binding', 'decision', 'binding:runtime_manifest', 'prerequisite', 'complete metadata identity differs: '+ANCESTRY+'/RUNTIME_CLOSURE.json'),
    _case('S14-contract-binding', 'decision', 'binding:caller_contract', 'prerequisite', 'complete metadata identity differs: '+E+'/CALLER_CONTRACT.md'),
    _case('S15-dependency-binding', 'decision', 'binding:dependency_manifest', 'prerequisite', 'complete metadata identity differs: '+E+'/SOURCE_DEPENDENCIES.json'),
    _case('S16-review-reference', 'decision', 'reference:independent_review', 'prerequisite', 'complete metadata identity differs: '+E+'/INDEPENDENT_SOURCE_REVIEW.json'),
    _case('S17-ri128-reference', 'decision', 'reference:ri128_source_adjudication', 'prerequisite', 'complete metadata identity differs: '+RI128_DECISION),
    _case('S18-history-reference', 'decision', 'reference:history_manifest', 'prerequisite', 'complete metadata identity differs: '+ANCESTRY+'/HISTORY_RECONCILIATION.json'),
    _case('S19-dependency-reference', 'decision', 'reference:dependency_manifest', 'prerequisite', 'complete metadata identity differs: '+E+'/SOURCE_DEPENDENCIES.json'),
    _case('S20-missing-index-role', 'decision', 'missing-index-role', 'identity', 'reference outside closed current inventory: '+E+'/supervise.py'),
    _case('R00-positive', 'review', 'none'),
    _case('R01-wrong-schema', 'review', 'schema', 'prerequisite', 'independent complete source review differs'),
    _case('R02-wrong-status', 'review', 'status', 'prerequisite', 'independent complete source review differs'),
    _case('R03-blocking-finding', 'review', 'blocking', 'prerequisite', 'independent complete source review differs'),
    _case('R04-scientific-execution', 'review', 'scientific', 'prerequisite', 'independent complete source review differs'),
    _case('R05-execution-promotion', 'review', 'execution', 'prerequisite', 'independent complete source review differs'),
    _case('R06-source-role-omitted', 'review', 'source-role', 'prerequisite', 'independently reviewed sources fields mismatch'),
    _case('R07-early-scope-before-lookup', 'review', 'scope-and-empty-index', 'prerequisite', 'independent complete source review differs'),
    _case('R08-supervisor-binding', 'review', 'binding:native_supervisor', 'prerequisite', 'complete metadata identity differs: '+E+'/supervise.py'),
    _case('R09-auditor-binding', 'review', 'binding:audit_caller', 'prerequisite', 'complete metadata identity differs: '+E+'/launch_audit.py'),
    _case('R10-history-binding', 'review', 'binding:history_manifest', 'prerequisite', 'complete metadata identity differs: '+ANCESTRY+'/HISTORY_RECONCILIATION.json'),
    _case('R11-runtime-binding', 'review', 'binding:runtime_manifest', 'prerequisite', 'complete metadata identity differs: '+ANCESTRY+'/RUNTIME_CLOSURE.json'),
    _case('R12-contract-binding', 'review', 'binding:caller_contract', 'prerequisite', 'complete metadata identity differs: '+E+'/CALLER_CONTRACT.md'),
    _case('R13-dependency-binding', 'review', 'binding:dependency_manifest', 'prerequisite', 'complete metadata identity differs: '+E+'/SOURCE_DEPENDENCIES.json'),
    _case('R14-missing-index-role', 'review', 'missing-index-role', 'identity', 'reference outside closed current inventory: '+E+'/supervise.py'),
    _case('T00-positive', 'checks', 'none'),
    _case('T01-missing-check-object', 'checks', 'missing-object', 'prerequisite', 'completed current-target check counts fields mismatch'),
    _case('T02-omitted-count', 'checks', 'omitted-count', 'prerequisite', 'completed current-target check counts fields mismatch'),
    _case('T03-extra-count', 'checks', 'extra-count', 'prerequisite', 'completed current-target check counts fields mismatch'),
    _case('T04-wrong-fixtures', 'checks', 'wrong-fixtures', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('T05-wrong-decisions', 'checks', 'wrong-decisions', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('T06-wrong-refusals', 'checks', 'wrong-refusals', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('T07-boolean-fixtures', 'checks', 'boolean-fixtures', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T08-boolean-decisions', 'checks', 'boolean-decisions', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T09-boolean-refusals', 'checks', 'boolean-refusals', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T10-float-integer', 'checks', 'float-fixtures', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T11-incomplete', 'checks', 'incomplete', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('T12-numeric-completion', 'checks', 'numeric-completion', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T13-inherited', 'checks', 'inherited', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('T14-numeric-inherited', 'checks', 'numeric-inherited', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
    _case('T15-omitted-inherited', 'checks', 'omitted-inherited', 'prerequisite', 'actual current-target checks absent or old qualification credited'),
)


def _identity(path):
    return {'path': str(path), 'resolved_path': str(path), 'bytes': 1,
            'sha256': '1'*64, 'symlinks': []}


def _index(caller):
    paths = list(caller.SOURCE_PATHS.values()) + [caller.E/'INDEPENDENT_SOURCE_REVIEW.json',
                                                caller.RI128_DECISION]
    return {str(path): _identity(path) for path in paths}


def _arguments(caller, family, mutation):
    # Values refer to fixed path strings but are never file observations/cards.
    if family == 'dependency':
        paths = ['/RI134-INERT-ARGUMENT-A', '/RI134-INERT-ARGUMENT-B']
        entries = [{'role': 'dep_'+str(i).zfill(4), 'path': path, 'identity': _identity(path),
                    'classification': 'synthetic argument', 'access_policy': 'not a file',
                    'reference_provenance': []} for i, path in enumerate(paths, 1)]
        value = {'schema': 'ri129-source-dependencies-v1', 'status': 'SOURCE_ONLY_CLOSED_DEPENDENCIES',
                 'scope': {'scientific_execution': False, 'runtime_inventory_created': False,
                           'active_execution_artifacts_created': False, 'old_history_and_runtime_preserved': True},
                 'protected_files': entries}
        first = entries[0]
        if mutation == 'extra-root-key': value['extra'] = None
        elif mutation in ('schema', 'status'): value[mutation] = 'wrong'
        elif mutation == 'scope': value['scope']['scientific_execution'] = True
        elif mutation == 'empty': value['protected_files'] = []
        elif mutation == 'nonlist': value['protected_files'] = ()
        elif mutation == 'extra-entry-key': first['extra'] = None
        elif mutation == 'role': first['role'] = 'dep_0002'
        elif mutation == 'relative': first['path'] = 'RI134-INERT-ARGUMENT-A'
        elif mutation == 'noncanonical': first['path'] = '/a/../RI134-INERT-ARGUMENT-A'
        elif mutation == 'nontext': first['path'] = 1
        elif mutation in ('descending', 'duplicate'):
            entries[1]['path'] = '/RI134-INERT-ARGUMENT-0' if mutation == 'descending' else paths[0]
            entries[1]['identity'] = _identity(entries[1]['path'])
        elif mutation == 'identity-extra': first['identity']['extra'] = None
        elif mutation == 'identity-path': first['identity']['path'] = '/RI134-INERT-WRONG'
        elif mutation == 'identity-bool-size': first['identity']['bytes'] = False
        elif mutation == 'identity-negative-size': first['identity']['bytes'] = -1
        elif mutation == 'identity-digest': first['identity']['sha256'] = 'not-a-digest'
        elif mutation == 'link-shape': first['identity']['symlinks'] = [{}]
        elif mutation == 'alias': first['identity']['resolved_path'] = '/RI134-INERT-ALIAS'
        elif mutation == 'link': first['identity']['symlinks'] = [{'path': paths[0], 'target': 'inert'}]
        elif mutation == 'classification': first['classification'] = ''
        elif mutation == 'access-policy': first['access_policy'] = ''
        elif mutation == 'provenance': first['reference_provenance'] = 'not-a-list'
        elif mutation != 'none': raise RuntimeError('unknown dependency mutation')
        return [value]
    if family in ('decision', 'review'):
        index = _index(caller)
        sources = {role: deepcopy(index[str(path)]) for role, path in caller.SOURCE_PATHS.items()}
        if family == 'decision':
            value = {'schema': 'ri129-root-caller-source-adjudication-v1',
                     'status': 'ACCEPT_EXACT_NATIVE_CALLER_SOURCE_ONLY', 'accepted_sources': sources,
                     'independent_review': deepcopy(index[str(caller.E/'INDEPENDENT_SOURCE_REVIEW.json')]),
                     'ri128_source_adjudication': deepcopy(index[str(caller.RI128_DECISION)]),
                     'history_manifest': deepcopy(index[str(caller.HISTORY)]),
                     'dependency_manifest': deepcopy(index[str(caller.DEPENDENCIES)]),
                     'execution_authorized': False, 'qualification_transferred_to_changed_targets': False}
        else:
            value = {'schema': 'ri129-independent-complete-caller-source-review-v1',
                     'status': 'PASS_COMPLETE_SOURCE_REVIEW_ONLY', 'blocking_findings': [],
                     'scientific_execution': False, 'execution_authorized': False, 'sources': sources}
        if mutation == 'extra-root-key': value['extra'] = None
        elif mutation == 'missing-root-key': del value['independent_review']
        elif mutation in ('schema', 'status'): value[mutation] = 'wrong'
        elif mutation == 'execution': value['execution_authorized'] = True
        elif mutation == 'execution-zero': value['execution_authorized'] = 0
        elif mutation == 'inherited': value['qualification_transferred_to_changed_targets'] = True
        elif mutation == 'source-role': del sources['native_supervisor']
        elif mutation == 'blocking': value['blocking_findings'] = ['synthetic blocking argument']
        elif mutation == 'scientific': value['scientific_execution'] = True
        elif mutation == 'scope-and-empty-index':
            value['execution_authorized'] = True
            index = {}
        elif mutation.startswith('binding:'):
            sources[mutation.split(':', 1)[1]]['sha256'] = '2'*64
        elif mutation.startswith('reference:'):
            value[mutation.split(':', 1)[1]]['sha256'] = '2'*64
        elif mutation == 'missing-index-role':
            del index[str(caller.SELF)]
        elif mutation != 'none': raise RuntimeError('unknown source policy mutation')
        return [value, index]
    if family == 'checks':
        value = {'current_target_checks': {'sign_fixtures': 15, 'internal_decision_cases': 4,
                                           'intended_first_refusals': 71},
                 'current_target_checks_completed': True, 'changed_target_qualification_inherited': False}
        checks = value['current_target_checks']
        if mutation == 'missing-object': del value['current_target_checks']
        elif mutation == 'omitted-count': del checks['sign_fixtures']
        elif mutation == 'extra-count': checks['extra'] = 1
        elif mutation == 'wrong-fixtures': checks['sign_fixtures'] = 14
        elif mutation == 'wrong-decisions': checks['internal_decision_cases'] = 3
        elif mutation == 'wrong-refusals': checks['intended_first_refusals'] = 70
        elif mutation == 'boolean-fixtures': checks['sign_fixtures'] = True
        elif mutation == 'boolean-decisions': checks['internal_decision_cases'] = True
        elif mutation == 'boolean-refusals': checks['intended_first_refusals'] = True
        elif mutation == 'float-fixtures': checks['sign_fixtures'] = 15.0
        elif mutation == 'incomplete': value['current_target_checks_completed'] = False
        elif mutation == 'numeric-completion': value['current_target_checks_completed'] = 1
        elif mutation == 'inherited': value['changed_target_qualification_inherited'] = True
        elif mutation == 'numeric-inherited': value['changed_target_qualification_inherited'] = 0
        elif mutation == 'omitted-inherited': del value['changed_target_qualification_inherited']
        elif mutation != 'none': raise RuntimeError('unknown current-target mutation')
        return [value]
    raise RuntimeError('unknown native policy family')


def _same_typed(left, right):
    """Compare only the supplied built-in value domain, including container types."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return len(left) == len(right) and all(
            _same_typed(ka, kb) and _same_typed(va, vb)
            for (ka, va), (kb, vb) in zip(left.items(), right.items()))
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(_same_typed(a, b) for a, b in zip(left, right))
    if type(left) is float:
        return left.hex() == right.hex()
    if type(left) in (str, int, bool, type(None)):
        return left == right
    raise RuntimeError('unsupported argument type in native policy purity check')


def run_case(authenticated_caller, case_id):
    """Call the real extracted policy; a return is never admission or history."""
    matches = [case for case in CASES if case['id'] == case_id]
    if len(matches) != 1:
        raise RuntimeError('native policy case must be uniquely declared')
    case = matches[0]
    caller = authenticated_caller
    arguments = _arguments(caller, case['family'], case['mutation'])
    before = deepcopy(arguments)
    function = getattr(caller, case['boundary'])
    expected = case['expected']
    try:
        result = function(*arguments)
    except BaseException as error:
        if (expected['outcome'] != 'REFUSED' or type(error) is not caller.Stop
                or error.code != expected['code'] or str(error) != expected['message']):
            raise RuntimeError('unexpected native policy first outcome: '+case_id) from error
        observation = {'exception_type': 'Stop', 'code': error.code, 'message': str(error), 'return_kind': None}
    else:
        if expected['outcome'] != 'RETURN':
            raise RuntimeError('native policy unexpectedly returned: '+case_id)
        if case['family'] == 'dependency':
            entries = arguments[0]['protected_files']
            if (type(result) is not list or result is entries or len(result) != len(entries)
                    or any(a is not b for a, b in zip(result, entries))):
                raise RuntimeError('dependency policy did not return the exact validated entry objects')
        elif result is not None:
            raise RuntimeError('native source/check policy must return exactly None')
        observation = {'exception_type': None, 'code': None, 'message': None,
                       'return_kind': expected['return_kind']}
    # Preserve dict order and list/tuple, bool/int/float distinctions recursively.
    if not _same_typed(arguments, before):
        raise RuntimeError('pure native policy mutated its arguments')
    return {'id': case_id, 'boundary': case['boundary'], 'outcome': expected['outcome'],
            'observed': observation, 'coverage_scope': 'DIRECT_ACTUAL_PURE_POLICY_ONLY',
            'whole_entry': False, 'active_acceptance_record_created': False,
            'complete_caller_qualification': False, 'scientific_execution': False}
