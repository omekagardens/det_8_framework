"""RI113 fabricated header-interface qualification, source-only until admitted.

No observed path, input, numerical module, primary or validator is imported.
The future admitted caller supplies captured module objects and binds this
returned report to the complete reviewed source/runtime/custody closure.
Only the production header helpers are called: 2 positives and 20 refusals.
"""

import copy
import json


SCHEMA = 'ri113-fabricated-interface-qualification-v1'
PHASE = 'fabricated_interface_qualification'
HEADER = {'schema': 'ri98-mode-weighted-trace-v1',
          'phase': 'fixed_saved_application',
          'status': 'all_declared_checks_passed'}
CASE_IDS = ('H00:accepted_header_contract', 'H01:legacy_status',
            'H02:unknown_status', 'H03:fabricated_prior_phase',
            'H04:receiving_phase_substitution', 'H05:older_predecessor_schema',
            'H06:missing_status', 'H07:missing_phase', 'H08:missing_schema',
            'H09:nonstring_status', 'H10:nonmapping_header')
PRIMARY_CODES = (None, 'TRACE', 'TRACE', 'PHASE', 'PHASE', 'INPUT',
                 'TRACE', 'PHASE', 'INPUT', 'TRACE', 'INPUT')
VALIDATOR_CODES = (None,) + ('INPUT',) * 10
LIMITATIONS = [
    'Every test is fabricated source-known header metadata, not an observed result body or numerical input.',
    'Recognizing the fixed RI100 header does not establish whole-body identity, scenario validity, provenance, execution custody or arithmetic.',
    'No observed adapter, HDF5 extraction, coefficient capture, interval contraction or scientific fixture is executed by this qualifier.',
    'This report qualifies only the two production header helpers; historical RI108 qualification and the failed RI110 attempt remain distinct evidence.',
    'A passing interface report does not admit a new observed attempt or establish physical calibration, protected validation, noise covariance, a native forward map or geometry/gravity; RET remains paused.',
]


class InterfaceQualificationError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InterfaceQualificationError('RI113 interface qualification: ' + message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       allow_nan=False) + '\n').encode('ascii')


def vectors():
    """Return the closed 11-vector inventory, with no actual body impersonation."""
    cases = [copy.deepcopy(HEADER)]
    for field, value in (('status', 'all_gates_passed'),
                         ('status', 'success_unchecked'),
                         ('phase', 'fabricated_qualification'),
                         ('phase', 'fixed_observed_application'),
                         ('schema', 'ri93-frequency-band-proxy-v1')):
        item = copy.deepcopy(HEADER)
        item[field] = value
        cases.append(item)
    for field in ('status', 'phase', 'schema'):
        item = copy.deepcopy(HEADER)
        del item[field]
        cases.append(item)
    item = copy.deepcopy(HEADER)
    item['status'] = True
    cases.extend((item, None))
    require(len(cases) == 11, 'fixed vector inventory')
    return cases


def qualify_interface(primary, validator):
    """Exercise exactly 22 production-helper calls; no I/O or actual adapters.

    Source acceptance, captured loading, runtime identity and external custody
    belong to the separately admitted caller, not this narrow metadata report.
    On any unexpected result the qualifier raises; it never relabels a failure.
    """
    implementations = (
        ('primary', 'check_ri100_header', primary, 'ContextError', PRIMARY_CODES),
        ('validator', 'verify_ri100_header', validator, 'ValidationError', VALIDATOR_CODES),
    )
    records = []
    for implementation, helper_name, module, error_name, codes in implementations:
        helper = getattr(module, helper_name, None)
        error_type = getattr(module, error_name, None)
        require(callable(helper), implementation + ' production helper missing')
        require(type(error_type) is type and issubclass(error_type, Exception),
                implementation + ' expected typed error missing')
        cases = vectors()
        require(len(cases) == len(CASE_IDS) == len(codes) == 11,
                implementation + ' complete case/code inventory')
        for case_id, value, expected_code in zip(CASE_IDS, cases, codes):
            before = canonical(value)
            actual_code = None
            actual_error = None
            try:
                result = helper(value)
            except Exception as error:
                require(expected_code is not None, implementation + ':' + case_id + ' unexpected refusal')
                require(type(error) is error_type, implementation + ':' + case_id + ' wrong exception class')
                actual_code = getattr(error, 'code', None)
                require(type(actual_code) is str and actual_code == expected_code,
                        implementation + ':' + case_id + ' wrong refusal code')
                actual_error = error_name
            else:
                require(expected_code is None, implementation + ':' + case_id + ' missing refusal')
                require(result is None, implementation + ':' + case_id + ' header helper must return None')
            require(canonical(value) == before, implementation + ':' + case_id + ' input mutation')
            records.append({'id': implementation + ':' + case_id,
                            'implementation': implementation, 'helper': helper_name,
                            'input': copy.deepcopy(value),
                            'expected': {'outcome': 'header_only_pass' if expected_code is None else 'refusal',
                                         'code': expected_code},
                            'actual': {'outcome': 'header_only_pass' if actual_error is None else 'refusal',
                                       'code': actual_code, 'error_class': actual_error},
                            'passed': True})
    inventory = [implementation + ':' + case_id
                 for implementation in ('primary', 'validator') for case_id in CASE_IDS]
    require([record['id'] for record in records] == inventory, 'exact complete ordered helper-call inventory')
    return {'schema': SCHEMA, 'phase': PHASE, 'status': 'all_header_contract_checks_passed',
            'scope': 'fixed_RI100_header_contract_only_no_observed_or_scientific_execution',
            'counts': {'implementations': 2, 'positive': 2, 'refusals': 20, 'helper_calls': 22},
            'inventory': inventory, 'results': records, 'limitations': list(LIMITATIONS)}
