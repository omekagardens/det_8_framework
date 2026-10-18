"""RI134 unexecuted direct tests of the four real audit policy functions.

The owner supplies an authenticated new caller module. This module has no
loader, command line, filesystem observation, accepted-file writer or global
patch. All input values are fabricated argument data, never cards/history.
"""

from copy import deepcopy


E_PATH = '/Volumes/AI_DATA/development/det-review-evidence/ri134-native-validator-extraction-source-y8kwkcde'
RI128_PATH = '/Volumes/AI_DATA/development/det-review-evidence/ri128-root-adjudication-tb3fbol5/RI128_ROOT_ADJUDICATION.json'
HISTORY_PATH = '/Volumes/AI_DATA/development/det-review-evidence/ri122-native-caller-source-jgehvvxx/HISTORY_RECONCILIATION.json'


def _case(identifier, family, mutation, code=None, message=None, declarations=()):
    return {
        'id': identifier, 'family': family, 'mutation': mutation,
        'boundary': {
            'dependency': 'validate_dependency_payload',
            'decision': 'validate_source_decision_payload',
            'review': 'validate_source_review_payload',
            'checks': 'validate_current_target_checks',
        }[family],
        'expected': {'outcome': 'RETURN' if message is None else 'REFUSED',
                     'exception_type': None if message is None else 'Stop',
                     'code': code, 'message': message},
        'input_kind': 'FABRICATED_ARGUMENT_ONLY',
        'coverage_scope': 'DIRECT_EXTRACTED_POLICY_ONLY',
        'declared_controls': list(declarations), 'prerequisite_dependent': False,
    }


CASES = (
    _case('AD01', 'dependency', 'positive'),
    _case('AD02', 'dependency', 'root-extra', 'dependency', 'static source dependency manifest fields mismatch'),
    _case('AD03', 'dependency', 'schema', 'dependency', 'static source dependency manifest schema differs'),
    _case('AD04', 'dependency', 'status', 'dependency', 'static source dependency manifest schema differs'),
    _case('AD05', 'dependency', 'scope', 'identity', 'static source dependency scope differs'),
    _case('AD06', 'dependency', 'empty', 'dependency', 'static source dependency closure is empty'),
    _case('AD07', 'dependency', 'entry-extra', 'dependency', 'static source dependency entry fields mismatch'),
    _case('AD08', 'dependency', 'role', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('AD09', 'dependency', 'duplicate', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('AD10', 'dependency', 'path', 'dependency', 'static dependency role/order/path differs', ('dependency-order-or-duplicate',)),
    _case('AD11', 'dependency', 'identity-extra', 'configuration', 'file identity fields mismatch'),
    _case('AD12', 'dependency', 'identity-bool-size', 'configuration', 'invalid file identity fields'),
    _case('AD13', 'dependency', 'alias', 'dependency', 'static source dependency has a symlink or alias', ('dependency-link-or-alias',)),
    _case('AD14', 'dependency', 'link', 'dependency', 'static source dependency has a symlink or alias', ('dependency-link-or-alias',)),
    _case('AD15', 'dependency', 'classification', 'dependency', 'static dependency provenance field types differ'),
    _case('AD16', 'dependency', 'access', 'dependency', 'static dependency provenance field types differ'),
    _case('AD17', 'dependency', 'provenance', 'dependency', 'static dependency provenance field types differ'),
    _case('AD18', 'dependency', 'not-list', 'dependency', 'static source dependency closure is empty'),
    _case('AD19', 'dependency', 'not-object', 'dependency', 'static source dependency manifest fields mismatch'),
    _case('AS01', 'decision', 'positive'),
    _case('AS02', 'decision', 'extra', 'prerequisite', 'RI129 source decision fields mismatch', ('source-decision-extra-field',)),
    _case('AS03', 'decision', 'missing', 'prerequisite', 'RI129 source decision fields mismatch'),
    _case('AS04', 'decision', 'schema', 'prerequisite', 'RI129 source decision is not exact source-only acceptance'),
    _case('AS05', 'decision', 'status', 'prerequisite', 'RI129 source decision is not exact source-only acceptance'),
    _case('AS06', 'decision', 'execution-true', 'prerequisite', 'RI129 source decision is not exact source-only acceptance', ('source-decision-promotion',)),
    _case('AS07', 'decision', 'execution-zero', 'prerequisite', 'RI129 source decision is not exact source-only acceptance', ('source-decision-promotion',)),
    _case('AS08', 'decision', 'transfer-true', 'prerequisite', 'RI129 source decision is not exact source-only acceptance', ('source-decision-promotion',)),
    _case('AS09', 'decision', 'transfer-zero', 'prerequisite', 'RI129 source decision is not exact source-only acceptance', ('source-decision-promotion',)),
    _case('AS10', 'decision', 'sources', 'identity', 'RI129 accepted source set differs'),
    _case('AS11', 'decision', 'unclosed-review', 'identity', 'required path outside frozen inventory'),
    _case('AS12', 'decision', 'zero-review', 'preparation', 'nonpositive or placeholder identity: '+E_PATH+'/INDEPENDENT_SOURCE_REVIEW.json'),
    _case('AS13', 'decision', 'changed-review', 'identity', 'full current reference differs: '+E_PATH+'/INDEPENDENT_SOURCE_REVIEW.json'),
    _case('AS14', 'decision', 'changed-ri128', 'identity', 'full current reference differs: '+RI128_PATH),
    _case('AS15', 'decision', 'changed-history', 'identity', 'full current reference differs: '+HISTORY_PATH),
    _case('AS16', 'decision', 'changed-dependency', 'identity', 'full current reference differs: '+E_PATH+'/SOURCE_DEPENDENCIES.json'),
    _case('AS17', 'decision', 'null-review', 'configuration', 'file identity fields mismatch'),
    _case('AR01', 'review', 'positive'),
    _case('AR02', 'review', 'schema', 'prerequisite', 'complete independent source review absent'),
    _case('AR03', 'review', 'status', 'prerequisite', 'complete independent source review absent'),
    _case('AR04', 'review', 'blockers', 'prerequisite', 'complete independent source review absent', ('source-review-incomplete',)),
    _case('AR05', 'review', 'science-true', 'prerequisite', 'complete independent source review absent'),
    _case('AR06', 'review', 'science-zero', 'prerequisite', 'complete independent source review absent'),
    _case('AR07', 'review', 'execution-true', 'prerequisite', 'complete independent source review absent'),
    _case('AR08', 'review', 'execution-zero', 'prerequisite', 'complete independent source review absent'),
    _case('AR09', 'review', 'sources', 'identity', 'independent source set differs'),
    _case('AT01', 'checks', 'positive'),
    _case('AT02', 'checks', 'missing-checks', 'prerequisite', 'completed current-target check counts fields mismatch', ('old-target-qualification-credit',)),
    _case('AT03', 'checks', 'extra-count', 'prerequisite', 'completed current-target check counts fields mismatch', ('old-target-qualification-credit',)),
    _case('AT04', 'checks', 'missing-count', 'prerequisite', 'completed current-target check counts fields mismatch', ('old-target-qualification-credit',)),
    _case('AT05', 'checks', 'bool-sign', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT06', 'checks', 'string-decision', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT07', 'checks', 'float-refusal', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT08', 'checks', 'wrong-sign', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT09', 'checks', 'wrong-decision', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT10', 'checks', 'wrong-refusal', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT11', 'checks', 'completed-false', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT12', 'checks', 'completed-one', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT13', 'checks', 'inherited-true', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT14', 'checks', 'inherited-zero', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT15', 'checks', 'missing-completed', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT16', 'checks', 'missing-inherited', 'prerequisite', 'actual current-target checks absent or old qualification credited', ('old-target-qualification-credit',)),
    _case('AT17', 'checks', 'null-counts', 'prerequisite', 'completed current-target check counts fields mismatch', ('old-target-qualification-credit',)),
)


def _identity(path):
    return {'path': str(path), 'resolved_path': str(path), 'bytes': 1,
            'sha256': '1'*64, 'symlinks': []}


def _dependency(mutation):
    entries = []
    for index, suffix in enumerate(('a', 'b'), 1):
        path = '/__ri134_argument_only__/'+suffix
        entries.append({'role': 'dep_'+str(index).zfill(4), 'path': path,
                        'identity': _identity(path), 'classification': 'fabricated-argument',
                        'access_policy': 'not-a-file-observation', 'reference_provenance': []})
    value = {'schema': 'ri129-source-dependencies-v1', 'status': 'SOURCE_ONLY_CLOSED_DEPENDENCIES',
             'protected_files': entries,
             'scope': {'scientific_execution': False, 'runtime_inventory_created': False,
                       'active_execution_artifacts_created': False, 'old_history_and_runtime_preserved': True}}
    first = entries[0]
    if mutation == 'root-extra':
        value['extra'] = None
    elif mutation == 'schema':
        value['schema'] = 'wrong'
    elif mutation == 'status':
        value['status'] = 'wrong'
    elif mutation == 'scope':
        value['scope']['scientific_execution'] = 0
    elif mutation == 'empty':
        value['protected_files'] = []
    elif mutation == 'entry-extra':
        first['extra'] = None
    elif mutation == 'role':
        first['role'] = 'dep_0002'
    elif mutation == 'duplicate':
        entries[1]['path'] = first['path']
        entries[1]['identity'] = deepcopy(first['identity'])
    elif mutation == 'path':
        first['path'] = '/__ri134_argument_only__/./a'
        first['identity'] = _identity(first['path'])
    elif mutation == 'identity-extra':
        first['identity']['extra'] = None
    elif mutation == 'identity-bool-size':
        first['identity']['bytes'] = True
    elif mutation == 'alias':
        first['identity']['resolved_path'] = '/__ri134_argument_only__/elsewhere'
    elif mutation == 'link':
        first['identity']['symlinks'] = [{'path': first['path'], 'target': 'inert-target'}]
    elif mutation == 'classification':
        first['classification'] = ''
    elif mutation == 'access':
        first['access_policy'] = ''
    elif mutation == 'provenance':
        first['reference_provenance'] = 'not-a-list'
    elif mutation == 'not-list':
        value['protected_files'] = {}
    elif mutation == 'not-object':
        value = None
    elif mutation != 'positive':
        raise RuntimeError('unknown closed dependency mutation')
    return [value]


def _source_context(caller):
    # Constants determine inert path strings only; no filesystem lookup occurs.
    paths = {'native_supervisor': caller.E/'supervise.py', 'audit_caller': caller.SELF,
             'history_manifest': caller.HISTORY, 'runtime_manifest': caller.RUNTIME,
             'caller_contract': caller.E/'CALLER_CONTRACT.md',
             'dependency_manifest': caller.DEPENDENCIES}
    sources = {role: _identity(path) for role, path in paths.items()}
    known = {str(path): _identity(path) for path in paths.values()}
    refs = {'independent_review': caller.E/'INDEPENDENT_SOURCE_REVIEW.json',
            'ri128_source_adjudication': caller.RI128_DECISION,
            'history_manifest': caller.HISTORY, 'dependency_manifest': caller.DEPENDENCIES}
    for path in refs.values():
        known[str(path)] = _identity(path)
    decision = {'schema': 'ri129-root-caller-source-adjudication-v1',
                'status': 'ACCEPT_EXACT_NATIVE_CALLER_SOURCE_ONLY',
                'accepted_sources': deepcopy(sources), 'execution_authorized': False,
                'qualification_transferred_to_changed_targets': False}
    decision.update({key: _identity(path) for key, path in refs.items()})
    review = {'schema': 'ri129-independent-complete-caller-source-review-v1',
              'status': 'PASS_COMPLETE_SOURCE_REVIEW_ONLY', 'blocking_findings': [],
              'scientific_execution': False, 'execution_authorized': False,
              'sources': deepcopy(sources)}
    return decision, review, sources, known


def _decision(caller, mutation):
    decision, _, sources, known = _source_context(caller)
    if mutation == 'extra':
        decision['extra'] = None
    elif mutation == 'missing':
        del decision['status']
    elif mutation == 'schema':
        decision['schema'] = 'wrong'
    elif mutation == 'status':
        decision['status'] = 'wrong'
    elif mutation in ('execution-true', 'execution-zero'):
        decision['execution_authorized'] = True if mutation == 'execution-true' else 0
    elif mutation in ('transfer-true', 'transfer-zero'):
        decision['qualification_transferred_to_changed_targets'] = True if mutation == 'transfer-true' else 0
    elif mutation == 'sources':
        decision['accepted_sources']['audit_caller']['sha256'] = '2'*64
    elif mutation == 'unclosed-review':
        del known[str(caller.E/'INDEPENDENT_SOURCE_REVIEW.json')]
    elif mutation == 'zero-review':
        decision['independent_review']['bytes'] = 0
    elif mutation in ('changed-review', 'changed-ri128', 'changed-history', 'changed-dependency'):
        key = {'changed-review': 'independent_review', 'changed-ri128': 'ri128_source_adjudication',
               'changed-history': 'history_manifest', 'changed-dependency': 'dependency_manifest'}[mutation]
        decision[key]['sha256'] = '2'*64
    elif mutation == 'null-review':
        decision['independent_review'] = None
    elif mutation != 'positive':
        raise RuntimeError('unknown closed source-decision mutation')
    return [decision, sources, known]


def _review(caller, mutation):
    _, review, sources, _ = _source_context(caller)
    if mutation == 'schema':
        review['schema'] = 'wrong'
    elif mutation == 'status':
        review['status'] = 'wrong'
    elif mutation == 'blockers':
        review['blocking_findings'] = ['inert-blocker']
    elif mutation in ('science-true', 'science-zero'):
        review['scientific_execution'] = True if mutation == 'science-true' else 0
    elif mutation in ('execution-true', 'execution-zero'):
        review['execution_authorized'] = True if mutation == 'execution-true' else 0
    elif mutation == 'sources':
        review['sources']['audit_caller']['sha256'] = '2'*64
    elif mutation != 'positive':
        raise RuntimeError('unknown closed source-review mutation')
    return [review, sources]


def _checks(mutation):
    value = {'current_target_checks': {'sign_fixtures': 15, 'internal_decision_cases': 4,
                                       'intended_first_refusals': 71},
             'current_target_checks_completed': True, 'changed_target_qualification_inherited': False}
    counts = value['current_target_checks']
    if mutation == 'missing-checks':
        del value['current_target_checks']
    elif mutation == 'extra-count':
        counts['extra'] = 0
    elif mutation == 'missing-count':
        del counts['sign_fixtures']
    elif mutation == 'bool-sign':
        counts['sign_fixtures'] = True
    elif mutation == 'string-decision':
        counts['internal_decision_cases'] = '4'
    elif mutation == 'float-refusal':
        counts['intended_first_refusals'] = 71.0
    elif mutation == 'wrong-sign':
        counts['sign_fixtures'] = 14
    elif mutation == 'wrong-decision':
        counts['internal_decision_cases'] = 5
    elif mutation == 'wrong-refusal':
        counts['intended_first_refusals'] = 70
    elif mutation == 'completed-false':
        value['current_target_checks_completed'] = False
    elif mutation == 'completed-one':
        value['current_target_checks_completed'] = 1
    elif mutation == 'inherited-true':
        value['changed_target_qualification_inherited'] = True
    elif mutation == 'inherited-zero':
        value['changed_target_qualification_inherited'] = 0
    elif mutation == 'missing-completed':
        del value['current_target_checks_completed']
    elif mutation == 'missing-inherited':
        del value['changed_target_qualification_inherited']
    elif mutation == 'null-counts':
        value['current_target_checks'] = None
    elif mutation != 'positive':
        raise RuntimeError('unknown closed current-check mutation')
    return [value]


def run_case(caller, case_id):
    """Observe one exact real-function outcome, not whole-entry acceptance."""
    matches = [item for item in CASES if item['id'] == case_id]
    if len(matches) != 1:
        raise RuntimeError('unknown or duplicate audit policy case')
    case = matches[0]
    family, mutation = case['family'], case['mutation']
    builders = {'dependency': lambda: _dependency(mutation),
                'decision': lambda: _decision(caller, mutation),
                'review': lambda: _review(caller, mutation),
                'checks': lambda: _checks(mutation)}
    args = builders[family]()
    unchanged = deepcopy(args)
    expected = dict(case['expected'])
    function = getattr(caller, case['boundary'])
    outcome, result = 'RETURN', None
    observed = {'exception_type': None, 'code': None, 'message': None}
    try:
        result = function(*args)
    except Exception as error:
        if type(error) is not caller.Stop:
            raise RuntimeError('unexpected exception type at '+case['boundary']) from error
        outcome = 'REFUSED'
        observed = {'exception_type': type(error).__name__, 'code': error.code, 'message': str(error)}
    if caller.canonical(args) != caller.canonical(unchanged):
        raise RuntimeError('pure audit policy mutated its arguments')
    if outcome != expected['outcome'] or observed != {
            key: expected[key] for key in ('exception_type', 'code', 'message')}:
        raise RuntimeError('audit policy first outcome differs: '+case_id+'; '+repr(observed))
    if outcome == 'RETURN':
        if family == 'dependency':
            if type(result) is not list or caller.canonical(result) != caller.canonical(args[0]['protected_files']):
                raise RuntimeError('dependency positive result is not the exact ordered entries list')
        elif result is not None:
            raise RuntimeError('audit policy positive result must be None')
    return {'id': case_id, 'boundary': case['boundary'], 'outcome': outcome,
            'observed': observed, 'expected': expected, 'arguments_unchanged': True,
            'coverage_scope': case['coverage_scope'], 'whole_entry': False,
            'actual_target_checks_executed': False, 'complete_caller_qualification': False,
            'fabricated_arguments_are_history': False}
