"""RI119 source-defined synthetic qualification; requires later caller admission.

Only run() and audit() perform work. Module objects are supplied by a caller
which captures and independently admits their exact source bytes. No imports
of those targets, paths, data, random sampling, subprocesses or ambient I/O.
Control expectations below are declarations until genuinely executed.
"""
from copy import deepcopy
import json

BODY_LIMIT = 2 * 1024 * 1024
SCHEMA = 'ri119-joint-window-qualification-v1'
PHASE = 'fabricated_joint_window_qualification'
LIMITATIONS = [
    'Complete finite synthetic arithmetic qualification only.',
    'Expected control labels are source declarations until this qualifier actually runs.',
    'Saved-field reconstruction does not independently witness historical control execution.',
    'Actual normal and optimized caller custody remains separate from this report.',
    'No empirical, calibration, significance or native validation; RET remains paused.',
]
# A path is traversed through a fresh copy. All ordinals are fixed by CONTRACT.
MUTATIONS = (
    ('M01_missing_root_key', 'delete', ('limitations',), None, 'SCHEMA'),
    ('M02_wrong_phase', 'set', ('phase',), 'empirical_validation', 'PHASE'),
    ('M03_wrong_result_status', 'set', ('status',), 'pending', 'RESULT'),
    ('M04_physical_scope', 'set', ('method', 'physical_model_validated'), True, 'SCOPE'),
    ('M05_missing_case', 'delete', ('cases', 8), None, 'INVENTORY'),
    ('M06_shared_coordinate', 'set', ('cases', 0, 'selectors_M', 1, 0, 2), 0, 'SHARED_INDEX'),
    ('M07_first_T_crop', 'set', ('cases', 0, 'selectors_T', 0, 2, 2), 0, 'CROP'),
    ('M08_output_map', 'set', ('cases', 0, 'output_map', 0, 0), '0', 'OPERATOR'),
    ('M09_declared_factor', 'set', ('cases', 0, 'model', 'raw_factor', 0, 0), '0', 'MODEL'),
    ('M10_nonPSD_covariance', 'set', ('cases', 0, 'stacked_output_covariance'),
     [['2', '3'], ['3', '2']], 'PSD'),
    ('M11_dropped_cross_term', 'set', ('cases', 0, 'stacked_output_covariance'),
     [['2', '0'], ['0', '2']], 'COVARIANCE_MODEL'),
    ('M12_transposed_cross_block', 'transpose', ('cases', 7, 'cross_blocks', 0, 1), None, 'COVARIANCE_MODEL'),
    ('M13_omitted_mean_dispersion', 'set', ('cases', 4, 'mean_dispersion'), '0', 'MEAN_TERM'),
    ('M14_wrong_n_divisor', 'set', ('cases', 0, 'expected_V'), '3', 'ENERGY'),
    ('M15_wrong_direct_energy', 'set', ('cases', 0, 'direct_average_V'), '0', 'ENERGY'),
    ('M16_rational_boolean', 'set', ('cases', 0, 'expected_V'), True, 'EXACT'),
    ('M17_unreduced_rational', 'set', ('cases', 0, 'expected_V'), '2/2', 'EXACT'),
    ('M18_scientific_float', 'set', ('cases', 0, 'expected_V'), 1.5, 'EXACT'),
    ('M19_wrong_sign_count', 'set', ('cases', 0, 'sign_count'), 63, 'ENUMERATION'),
    ('M20_boolean_sign_count', 'set', ('cases', 0, 'sign_count'), True, 'DIMENSION'),
    ('M21_calibrated_constant_claim', 'set', ('bounds', 0, 'constant_annihilation_claim'), True, 'CALIBRATION'),
    ('M22_negative_eta', 'set', ('bounds', 1, 'eta'), '-1', 'BOUND'),
    ('M23_understated_covariance_bound', 'set', ('bounds', 1, 'bound'), '0', 'BOUND'),
    ('M24_understated_calibration_bound', 'set', ('bounds', 2, 'bound'), '2', 'BOUND'),
    ('M25_wrong_nuisance_dimension', 'set', ('bounds', 1, 'output_dimension'), 8, 'DIMENSION'),
    ('M26_missing_case_field', 'delete', ('cases', 0, 'raw_mean'), None, 'SCHEMA'),
    ('M27_incomplete_covariance_row', 'delete', ('cases', 7, 'stacked_output_covariance', 0, 3), None, 'DIMENSION'),
    ('M28_boolean_selector', 'set', ('cases', 0, 'selectors_M', 0, 0, 0), True, 'DIMENSION'),
    ('M29_oversized_rational_component', 'oversized_scalar', ('cases', 0, 'expected_V'), None, 'RESOURCE'),
    ('M30_boolean_model_kind', 'set', ('cases', 0, 'model', 'kind'), True, 'EXACT'),
    ('M31_wrong_group_inventory', 'delete', ('groups', 0), None, 'INVENTORY'),
    ('M32_zeroed_oriented_covariance', 'set', ('cases', 7, 'centered_covariance_average', 0, 1), '0', 'COVARIANCE_MODEL'),
    ('M33_oversized_malformed_scalar', 'oversized_malformed', ('cases', 0, 'expected_V'), None, 'RESOURCE'),
)
PARSERS = (
    ('P01_duplicate_keys', 'CANONICAL'),
    ('P02_nonfinite', 'CANONICAL'),
    ('P03_missing_terminal_newline', 'CANONICAL'),
    ('P04_body_over_limit', 'RESOURCE'),
    ('P05_nonbytes', 'CANONICAL'),
)
PSD_CONTROLS = (('G01_nonsymmetric', 'PSD'), ('G02_negative_diagonal', 'PSD'),
                ('G03_oversized_cancelled_products', 'RESOURCE'))
PRIMARY_OK = {'status': 'all_fields_primary_match', 'cases': 9, 'bounds': 3, 'groups': 12}
VALIDATOR_OK = {'status': 'all_fields_independently_match', 'cases': 9, 'bounds': 3, 'groups': 12}
COVERAGE = [
    {'group': 'Q01', 'evidence': ['all_full_selectors_and_output_maps', 'M06_shared_coordinate', 'M07_first_T_crop']},
    {'group': 'Q02', 'evidence': ['Q02_white_two']},
    {'group': 'Q03', 'evidence': ['Q03_periodic_two']},
    {'group': 'Q04', 'evidence': ['M11_dropped_cross_term']},
    {'group': 'Q05', 'evidence': ['Q05_white_three']},
    {'group': 'Q06', 'evidence': ['Q06_constant_mean']},
    {'group': 'Q07', 'evidence': ['Q07_quadratic_mean', 'M13_omitted_mean_dispersion']},
    {'group': 'Q08', 'evidence': ['Q08_scale_minus_one', 'Q08_scale_two']},
    {'group': 'Q09', 'evidence': ['Q09_oriented_matrix', 'M12_transposed_cross_block', 'M32_zeroed_oriented_covariance']},
    {'group': 'Q10', 'evidence': ['Q10_zero_map', 'Q03_periodic_two']},
    {'group': 'Q11', 'evidence': ['all_full_factor_covariances', 'M10_nonPSD_covariance', 'G01_nonsymmetric', 'G02_negative_diagonal']},
    {'group': 'Q12', 'evidence': ['Q12_calibrated_constant', 'Q12_covariance_error', 'Q12_calibration_error',
                                'M21_calibrated_constant_claim', 'M22_negative_eta',
                                'M23_understated_covariance_bound', 'M24_understated_calibration_bound',
                                'M25_wrong_nuisance_dimension']},
]


class QualificationError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def require(ok, code, message):
    if not ok:
        raise QualificationError(code, message)


def equal(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in b)
    if type(a) is list: return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b


def canonical(value):
    try:
        body = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    except (TypeError, ValueError, OverflowError, RecursionError) as error:
        raise QualificationError('CANONICAL', 'canonical qualification encoding') from error
    require(len(body) <= BODY_LIMIT, 'RESOURCE', 'qualification byte limit')
    return body


def parse_report(body):
    require(type(body) is bytes, 'CANONICAL', 'qualification bytes required')
    require(len(body) <= BODY_LIMIT, 'RESOURCE', 'qualification byte limit')
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'CANONICAL', 'duplicate qualification JSON key')
            out[k] = v
        return out
    def bad(_): raise QualificationError('CANONICAL', 'nonfinite qualification JSON')
    try:
        out = json.loads(body.decode('ascii'), object_pairs_hook=pairs, parse_constant=bad)
    except QualificationError: raise
    except (ValueError, TypeError, UnicodeError, OverflowError, RecursionError) as error:
        raise QualificationError('CANONICAL', 'invalid qualification JSON') from error
    require(canonical(out) == body, 'CANONICAL', 'entire canonical qualification body')
    return out


def changed(reference, specification):
    _name, action, path, value, _code = specification
    candidate = deepcopy(reference)
    owner = candidate
    for key in path[:-1]: owner = owner[key]
    key = path[-1]
    if action == 'set': owner[key] = deepcopy(value)
    elif action == 'delete': del owner[key]
    elif action == 'transpose': owner[key] = [list(row) for row in zip(*owner[key])]
    elif action == 'oversized_scalar': owner[key] = '1' * 2468
    elif action == 'oversized_malformed': owner[key] = 'x' * 2468
    else: raise QualificationError('INVENTORY', 'unknown fixed mutation')
    require(not equal(candidate, reference), 'CONTROL', 'mutation must actually change the complete input')
    return candidate


def refused(call, exception_class, wanted):
    try:
        call()
    except exception_class as error:
        require(type(error.code) is str and error.code == wanted, 'CONTROL', 'wrong deliberate first-refusal code')
        return error.code
    except Exception as error:
        raise QualificationError('CONTROL', 'unexpected exception is not a successful refusal') from error
    raise QualificationError('CONTROL', 'mutation unexpectedly accepted')


def expected_rows(inventory):
    return [{'id': name, 'expected': code, 'primary': code, 'validator': code}
            for name, code in inventory]


def audit(report, primary, validator, reference):
    """Reconstruct all saved fields; custody separately witnesses run() history.

    reference is the caller-owned fresh primary enumeration, never read from
    the saved report. This function does not re-execute mutation controls.
    """
    wanted = {
        'schema': SCHEMA, 'phase': PHASE, 'status': 'all_qualification_checks_passed',
        'scientific_result': reference,
        'baseline': {'primary': PRIMARY_OK, 'validator': VALIDATOR_OK},
        'mutation_refusals': expected_rows([(row[0], row[4]) for row in MUTATIONS]),
        'parser_refusals': expected_rows(PARSERS), 'psd_refusals': expected_rows(PSD_CONTROLS),
        'coverage': COVERAGE, 'control_count_per_implementation': 41,
        'scientific_case_count': 9, 'bound_count': 3, 'group_count': 12,
        'input_and_reference_unchanged': True, 'limitations': LIMITATIONS,
    }
    require(equal(report, wanted), 'REPORT', 'complete qualification record mismatch')
    before = canonical(report)
    reference_before = primary.canonical(reference)
    require(equal(primary.compare_result(report['scientific_result'], reference), PRIMARY_OK), 'REPORT', 'primary result audit')
    require(equal(validator.validate_result(report['scientific_result']), VALIDATOR_OK), 'REPORT', 'full independent result audit')
    require(canonical(report) == before and primary.canonical(reference) == reference_before,
            'MUTATION', 'audit changed input or reference')
    return {'status': 'all_saved_fields_match', 'historical_controls_reexecuted': False,
            'scientific_independent_reconstruction': True}


def run(primary, validator):
    reference = primary.build_result()
    original = primary.canonical(reference)
    require(validator.canonical(reference) == original, 'CANONICAL', 'canonical scientific disagreement')
    scientific = primary.parse_result(original)
    require(equal(validator.parse_result(original), scientific), 'CANONICAL', 'complete parser disagreement')
    baseline = {'primary': primary.compare_result(scientific, reference),
                'validator': validator.validate_result(scientific)}
    require(equal(baseline, {'primary': PRIMARY_OK, 'validator': VALIDATOR_OK}), 'BASELINE', 'both complete baselines')
    require(primary.canonical(reference) == original and primary.canonical(scientific) == original,
            'MUTATION', 'baseline changed input/reference')
    mutations = []
    for spec in MUTATIONS:
        given = changed(reference, spec)
        input_before = primary.canonical(given)
        p_code = refused(lambda: primary.compare_result(given, reference), primary.PrimaryError, spec[4])
        require(primary.canonical(given) == input_before and primary.canonical(reference) == original,
                'MUTATION', 'primary changed malformed input/reference')
        v_code = refused(lambda: validator.validate_result(given), validator.ValidationError, spec[4])
        require(primary.canonical(given) == input_before and primary.canonical(reference) == original,
                'MUTATION', 'validator changed malformed input/reference')
        mutations.append({'id': spec[0], 'expected': spec[4], 'primary': p_code, 'validator': v_code})
    bodies = (
        b'{"x": 1, "x": 2}\n', b'{"x": NaN}\n', original[:-1],
        b' ' * (BODY_LIMIT + 1), original.decode('ascii'),
    )
    parsers = []
    for (name, code), body in zip(PARSERS, bodies):
        p_code = refused(lambda: primary.parse_result(body), primary.PrimaryError, code)
        v_code = refused(lambda: validator.parse_result(body), validator.ValidationError, code)
        parsers.append({'id': name, 'expected': code, 'primary': p_code, 'validator': v_code})
    psd_rows = []
    large = str(1 << 4096)
    for (name, code), matrix in zip(PSD_CONTROLS,
                                  ([['2', '0'], ['1', '2']], [['-1', '0'], ['0', '1']],
                                   [[large, large], [large, large]])):
        before = canonical(matrix)
        p_code = refused(lambda: primary.require_psd_2x2(matrix), primary.PrimaryError, code)
        v_code = refused(lambda: validator.require_psd_2x2(matrix), validator.ValidationError, code)
        require(canonical(matrix) == before, 'MUTATION', 'PSD guard changed input')
        psd_rows.append({'id': name, 'expected': code, 'primary': p_code, 'validator': v_code})
    require(primary.canonical(reference) == original and primary.canonical(scientific) == original,
            'MUTATION', 'control sequence changed baseline/reference')
    report = {
        'schema': SCHEMA, 'phase': PHASE, 'status': 'all_qualification_checks_passed',
        'scientific_result': scientific, 'baseline': baseline,
        'mutation_refusals': mutations, 'parser_refusals': parsers, 'psd_refusals': psd_rows,
        'coverage': deepcopy(COVERAGE), 'control_count_per_implementation': 41,
        'scientific_case_count': 9, 'bound_count': 3, 'group_count': 12,
        'input_and_reference_unchanged': True, 'limitations': list(LIMITATIONS),
    }
    # Saved-report path: serialize/parse and reconstruct all fields, retaining
    # the full independent scientific validator inside this genuine child call.
    saved = parse_report(canonical(report))
    audit(saved, primary, validator, reference)
    return saved
