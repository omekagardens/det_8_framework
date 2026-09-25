"""Independent RI98 saved-result validation from the accepted RI97 contract.

Only standard-library definitions; no import-time I/O, producer import, FFT,
CLI or filesystem access. Product-form errors are independently reconstructed.
The actual saved entry authenticates RI96 bytes before decoding. Upstream
transform validity and completed custody remain explicitly inherited premises.
"""
from fractions import Fraction
import hashlib
import json
import math
import re
import struct

BIT_LIMIT = 262144
GRID = 1 << 256
SIZE = 16384
RATE = 4096
DIMENSION = 8
ROW_IDS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
SCENARIO_IDS = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
DESIGN_PIN = {'bytes': 23571, 'sha256': '65edcabef43e15cfa44299c19276c194aed717269fe17702877f76ca8af379e7'}
RI96_PIN = {'bytes': 41673703, 'sha256': '5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580'}
DESIGN_DECISION = {'bytes': 2430, 'sha256': 'a2b76efbe5105c286c8b50d9183e407726c3404b36309d0ed9fb65c95b1b9539'}
RI96_DECISION = {'bytes': 6551, 'sha256': 'c7842d05fa0d34dddf60d5b3963abb0dbbcae6090ebfcc28af7ca525f61cc836'}
METHOD = {
    'M': 16384, 'N': 2769, 'L': 4096, 'T': 10961, 'output': 8,
    'fs': 4096, 'rows': [0, 1, 27, 805, 1384, 2741, 2767, 2768],
    'precision_bits': 256, 'integer_bit_limit': 262144,
    'unitary_divisor': 128, 'band_count': 14,
    'psd_map': 'fs_p_at_endpoints_fs_p_over_2_at_interior',
    'pair_weights': 'interior_2_nyquist_1',
    'dc': 'true_action_zero_inherited_midpoint_unchanged',
    'nyquist_imaginary': 'center_tau_alpha_all_zero',
    'arithmetic': 'exact_rational_scalar_aggregation_no_new_transform',
    'intersection': 'scalar_with_accepted_ri96_trace_only',
    'quantity': 'centered_discrepancy_energy_sum_of_eight_coordinates',
}
HELD_METHOD = {
    'M': 16384, 'N': 2769, 'L': 4096, 'T': 10961, 'output': 8,
    'fs': 4096, 'precision_bits': 256, 'integer_bit_limit': 262144,
    'unitary_divisor': 128, 'transform_sign': 1, 'band_count': 14,
    'arithmetic': 'outward_Q256_integer_intervals',
    'normalization': 'exact_division_then_outward_Q256',
}

# Literal protocol vocabulary copied from the reviewed source contract,
# not numerical functions or an arithmetic oracle.
HELD_LIMITATIONS = ['The four inherited empirical PSDs define separate postulated finite four-second circulant proxies, not established physical noise covariance.', 'All input bins are retained; only true A DC action is omitted by the accepted constant-annihilation theorem.', 'RI73 row enclosure and custody are inherited premises; no adjoint or coefficient reconstruction is performed.', 'Q256 transform rounding and retained coefficient radii are enclosed without assuming independent errors.', 'Certified band endpoints need not dominate the prior global endpoints; indefinite lower endpoints are not clipped.', 'Loewner bounds concern quadratic forms; off-diagonal entries are not scalar variance intervals.', 'The already accessed 32-second inputs are development/calibration evidence, not independent held-out validation.', 'Nominal V2/C02, blank literal Yunits and the clear L1 NO_CW_HW_INJ flag remain inherited limitations.', 'No calibrated physical meaning below 10 Hz, stationarity, Gaussianity, detector independence or estimation-uncertainty law is established.', 'No colored covariance inverse, whitening, residual score, SNR, p-value, physical adequacy or native forward map is supplied; RET stays paused.']
FABRICATED_LIMITATIONS = ['Fabricated RI98 projection; no observed input or predecessor execution.']
PREMISES = ['RI96 completed independent transform validation and saved arithmetic/custody acceptance are inherited; no new FFT or coefficient reconstruction.', 'RI73 coefficient enclosures, constant annihilation and RI96 midpoint rectangles/alpha remain conditional accepted premises.', 'The four finite circulant covariance models and all original PSD bins are unchanged.']
LIMITATIONS = ['Exact bounds concern centered discrepancy energy summed over eight fixed selected coordinates, not all2769 outputs or uncentered energy without a mean premise.', 'Nonnegative deterministic enclosure terms and their split are not statistical estimation uncertainty or confidence intervals.', 'Negative raw endpoints and undefined ratios are retained; no useful width improvement is required.', 'The already accessed32-second inputs remain development/calibration evidence, not protected held-out validation.', 'Nominal V2/C02, blank literal Yunits, the clear L1 NO_CW_HW_INJ flag and unknown calibration meaning below10Hz remain inherited.', 'Finite four-second circulant wraparound, physical noise adequacy, stationarity, detector independence and empirical PSD error are not validated.', 'No native forward map, physical geometry/gravity result, SNR, p-value or RET work is supplied; RET remains paused.']
GATES = ('admission:phase', 'admission:input', 'admission:rows', 'admission:psds', 'mode:complete', 'endpoint:real', 'scenario:H1:left', 'scenario:H1:right', 'scenario:L1:left', 'scenario:L1:right', 'completion:input_stable')

PROJECTION_FIELDS = ('context', 'held_identity', 'rows', 'row_proofs', 'scenarios',
                     'held_provenance_identity', 'held_limitations')
ROW_FIELDS = ('row', 'alpha', 'midpoint_modes', 'mode_identity')
INPUT_SCENARIO_FIELDS = ('id', 'source_record', 'band_extrema', 'C_minus', 'C_plus',
                         'delta_minus', 'delta_plus', 'trace', 'prior_trace')
RESULT_FIELDS = ('schema', 'phase', 'status', 'method', 'provenance', 'mode_terms',
                 'scenarios', 'checks', 'inherited_premises', 'limitations')
MODE_FIELDS = ('k', 'pair_weight', 'c', 'h_tau', 'h_alpha')
SCENARIO_FIELDS = ('id', 'source_identity', 'center', 'error_tau', 'error_alpha',
                   'error', 'raw', 'ri96_raw_band', 'ri96_prior', 'final',
                   'band_spread', 'band_margin', 'band_width', 'widths',
                   'equalities', 'ratios', 'direct_upper_le_band_upper')
RATIO_NAMES = ('ri96_over_final_width', 'ri96_over_raw_width',
               'raw_upper_over_lower', 'ri96_upper_over_lower', 'final_upper_over_lower')


class ValidationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def _require(condition, code, message):
    if not condition:
        raise ValidationError(code, message)


def _object(value, fields, code='SCHEMA'):
    _require(type(value) is dict and all(type(k) is str for k in value)
             and set(value) == set(fields), code, 'closed object fields')


def _array(value, length, code='SCHEMA'):
    _require(type(value) is list and len(value) == length, code, 'complete ordered list')
    return value


def _same(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(_same(left[k], right[k]) for k in left)
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(_same(a, b) for a, b in zip(left, right))
    return left == right


def _equal(left, right, code, message):
    _require(_same(left, right), code, message)


def _integer(value):
    _require(type(value) is int, 'EXACT', 'plain integer required')
    _require(abs(value).bit_length() <= BIT_LIMIT, 'RESOURCE', 'integer bit ceiling')
    return value


def _fraction(value):
    _require(type(value) is Fraction, 'EXACT', 'Fraction required')
    _integer(value.numerator)
    _integer(value.denominator)
    return value


def _plus(left, right):
    return _fraction(_fraction(left) + _fraction(right))


def _minus(left, right):
    return _fraction(_fraction(left) - _fraction(right))


def _times(left, right):
    return _fraction(_fraction(left) * _fraction(right))


def _sum(values):
    result = Fraction(0)
    for value in values:
        result = _plus(result, value)
    return result


def _hex(value):
    _require(type(value) is str, 'EXACT', 'canonical hexadecimal string')
    _require(len(value) <= (BIT_LIMIT + 3) // 4 + 1, 'RESOURCE', 'hexadecimal length ceiling')
    _require(re.fullmatch(r'0|-?[1-9a-f][0-9a-f]*', value) is not None,
             'EXACT', 'canonical lowercase signed hexadecimal')
    return _integer(int(value, 16))


def _decode(value):
    numerator, denominator = (_hex(v) for v in _array(value, 2, 'EXACT'))
    _require(denominator > 0 and math.gcd(numerator, denominator) == 1,
             'EXACT', 'positive denominator and reduced rational')
    return _fraction(Fraction(numerator, denominator))


def _encode(value):
    value = _fraction(value)
    return [format(value.numerator, 'x'), format(value.denominator, 'x')]


def _interval(value):
    endpoints = tuple(_decode(v) for v in _array(value, 2, 'ENVELOPE'))
    _require(endpoints[0] <= endpoints[1], 'ENVELOPE', 'ordered interval')
    return endpoints


def _encoded_interval(pair):
    return [_encode(pair[0]), _encode(pair[1])]


def _pin(value):
    _object(value, ('bytes', 'sha256'), 'PROVENANCE')
    _require(type(value['bytes']) is int and value['bytes'] >= 0
             and type(value['sha256']) is str
             and re.fullmatch(r'[0-9a-f]{64}', value['sha256']) is not None,
             'PROVENANCE', 'complete byte identity')


def _body_pin(body):
    _require(type(body) is bytes, 'INPUT', 'immutable bytes required')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def _canonical_parts(value):
    encoder = json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)
    for part in encoder.iterencode(value):
        yield part.encode('ascii')
    yield b'\n'


def _canonical_pin(value):
    digest, length = hashlib.sha256(), 0
    for part in _canonical_parts(value):
        digest.update(part)
        length += len(part)
    return {'bytes': length, 'sha256': digest.hexdigest()}


def _parse(body):
    _require(type(body) is bytes, 'INPUT', 'immutable JSON bytes required')
    def pairs(items):
        result = {}
        for key, value in items:
            _require(key not in result, 'SCHEMA', 'duplicate JSON key')
            result[key] = value
        return result
    def nonfinite(_):
        raise ValidationError('EXACT', 'nonfinite JSON literal')
    try:
        return json.loads(body, object_pairs_hook=pairs, parse_constant=nonfinite)
    except ValidationError:
        raise
    except (UnicodeError, ValueError) as error:
        raise ValidationError('SCHEMA', 'invalid JSON encoding') from error


def _phase(value):
    _require(type(value) is str and value in ('fabricated_qualification', 'fixed_saved_application'),
             'PHASE', 'fixed qualification/application phase')


def _projection(projection, phase):
    _phase(phase)
    _object(projection, PROJECTION_FIELDS, 'INPUT')
    _pin(projection['held_identity'])
    _pin(projection['held_provenance_identity'])
    if phase == 'fixed_saved_application':
        _equal(projection['context'], 'accepted_ri96_saved_output', 'PHASE', 'actual context')
        _equal(projection['held_identity'], RI96_PIN, 'INPUT', 'accepted complete RI96 identity')
        _equal(projection['held_limitations'], HELD_LIMITATIONS, 'INPUT', 'inherited actual limitations')
    else:
        _equal(projection['context'], 'fabricated_projection_not_observed', 'PHASE', 'fabricated context')
        _require(not _same(projection['held_identity'], RI96_PIN), 'PHASE', 'fabricated operand tag cannot claim actual identity')
        _equal(projection['held_limitations'], FABRICATED_LIMITATIONS, 'PHASE', 'explicit fabricated limitations')
        _equal(projection['held_provenance_identity'], _canonical_pin({'context': 'fabricated_not_observed'}),
               'PHASE', 'explicit fabricated upstream provenance marker')
    _equal(projection['rows'], list(ROW_IDS), 'ROW', 'fixed selected row order')
    for row_id, row in zip(ROW_IDS, _array(projection['row_proofs'], DIMENSION, 'ROW')):
        _object(row, ROW_FIELDS, 'ROW')
        _equal(row['row'], row_id, 'ROW', 'complete row order')
    for scenario_id, scenario in zip(SCENARIO_IDS, _array(projection['scenarios'], 4, 'PSD')):
        _object(scenario, INPUT_SCENARIO_FIELDS, 'PSD')
        _equal(scenario['id'], scenario_id, 'PSD', 'complete separate scenario order')


def _provenance(provenance, phase, input_pin):
    _object(provenance, ('sources', 'input', 'acceptance', 'runtime'), 'PROVENANCE')
    _object(provenance['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation'), 'PROVENANCE')
    for value in provenance['sources'].values():
        _pin(value)
    _equal(provenance['sources']['design'], DESIGN_PIN, 'SOURCE', 'accepted design identity')
    _pin(provenance['input'])
    _equal(provenance['input'], input_pin, 'INPUT', 'complete phase-specific numerical operand')
    _object(provenance['acceptance'], ('design', 'ri96', 'qualification', 'custody'), 'PROVENANCE')
    _equal(provenance['acceptance']['design'], DESIGN_DECISION, 'PROVENANCE', 'accepted root design record')
    _equal(provenance['acceptance']['ri96'], RI96_DECISION, 'PROVENANCE', 'accepted root RI96 record')
    for name in ('qualification', 'custody'):
        if phase == 'fabricated_qualification':
            _require(provenance['acceptance'][name] is None, 'PHASE', 'fabricated phase cannot claim completed admission')
        else:
            _pin(provenance['acceptance'][name])
    _object(provenance['runtime'], ('fingerprint', 'inventory', 'interpreter'), 'PROVENANCE')
    for value in provenance['runtime'].values():
        _pin(value)


def verify_result_fields(report, projection, expected_provenance, expected_phase):
    """Actual metadata guard used by full validation, with no arithmetic shortcut.

    This guard alone does not validate mode/scenario arithmetic or transform
    validity. The qualifier may use it for bounded metadata refusal cases.
    """
    _projection(projection, expected_phase)
    projection_pin = _canonical_pin(projection)
    _provenance(expected_provenance, expected_phase,
                RI96_PIN if expected_phase == 'fixed_saved_application' else projection_pin)
    _object(report, RESULT_FIELDS)
    _equal(report['schema'], 'ri98-mode-weighted-trace-v1', 'SCHEMA', 'RI98 result schema')
    _equal(report['phase'], expected_phase, 'PHASE', 'required phase')
    _equal(report['status'], 'all_declared_checks_passed', 'RESULT', 'completed fixed computation')
    _equal(report['method'], METHOD, 'DOMAIN', 'complete unchanged method')
    _equal(report['provenance'], expected_provenance, 'PROVENANCE', 'caller supplied exact provenance')
    _array(report['mode_terms'], SIZE // 2, 'MODE')
    _array(report['scenarios'], 4, 'PSD')
    checks = {'inventory': list(GATES), 'counts': {'total': 11, 'passed': 11, 'failed': 0},
              'results': [{'id': name, 'passed': True} for name in GATES]}
    _equal(report['checks'], checks, 'SCHEMA', 'closed gate inventory and typed results')
    premises = {'labels': list(PREMISES), 'projection_identity': projection_pin,
                'held_provenance_identity': projection['held_provenance_identity'],
                'held_limitations': projection['held_limitations']}
    _object(report['inherited_premises'], tuple(premises), 'SCHEMA')
    _equal(report['inherited_premises']['projection_identity'], projection_pin, 'INPUT', 'complete admitted projection identity')
    _equal(report['inherited_premises'], premises, 'SCHEMA', 'exact inherited premises')
    _equal(report['limitations'], LIMITATIONS, 'SCHEMA', 'complete scientific limitations')
    return True


def verify_mode_term(record, expected_term):
    """Actual per-mode guard; expected_term must be separately reconstructed."""
    _object(record, MODE_FIELDS, 'MODE')
    _require(type(record['k']) is int and 1 <= record['k'] <= SIZE // 2,
             'MODE', 'plain non-DC mode index')
    _require(type(record['pair_weight']) is int and record['pair_weight'] in (1, 2),
             'MODE', 'plain pair multiplicity')
    for name in ('c', 'h_tau', 'h_alpha'):
        _require(_decode(record[name]) >= 0, 'MODE', 'nonnegative exact mode term')
    _equal(record, expected_term, 'RESULT', 'independent product-form mode reconstruction')
    return True


def verify_scenario(record, expected_scenario):
    """Actual scalar-record guard; full validation supplies independent values."""
    _object(record, SCENARIO_FIELDS, 'PSD')
    _require(type(record['id']) is str and record['id'] in SCENARIO_IDS, 'PSD', 'fixed scenario id')
    _pin(record['source_identity'])
    for name in ('center', 'error_tau', 'error_alpha', 'error', 'band_spread', 'band_margin', 'band_width'):
        _require(_decode(record[name]) >= 0, 'ENVELOPE', 'nonnegative scalar diagnostic')
    for name in ('raw', 'ri96_raw_band', 'ri96_prior', 'final'):
        _interval(record[name])
    _object(record['widths'], ('raw', 'ri96', 'final'), 'ENVELOPE')
    for value in record['widths'].values():
        _require(_decode(value) >= 0, 'ENVELOPE', 'nonnegative interval width')
    _object(record['equalities'], ('final_equals_ri96', 'final_equals_raw'), 'SCHEMA')
    _require(all(type(v) is bool for v in record['equalities'].values()), 'SCHEMA', 'plain equality flags')
    _require(type(record['direct_upper_le_band_upper']) is bool, 'SCHEMA', 'plain upper-consistency flag')
    _object(record['ratios'], RATIO_NAMES, 'SCHEMA')
    for name, ratio in record['ratios'].items():
        _object(ratio, ('value', 'undefined_reason'), 'SCHEMA')
        if ratio['value'] is None:
            reason = 'zero_width_denominator' if name.startswith('ri96_over_') else 'nonpositive_lower_endpoint'
            _equal(ratio['undefined_reason'], reason, 'RESULT', 'undefined ratio reason')
        else:
            _decode(ratio['value'])
            _require(ratio['undefined_reason'] is None, 'RESULT', 'defined ratio has null reason')
    _equal(record, expected_scenario, 'RESULT', 'complete independently reconstructed scalar record')
    return True


def _domain(size, dimension):
    _require(type(size) is int and type(dimension) is int and
             (size, dimension) in ((4, 1), (4, 2), (8, 1), (8, 8), (16384, 8)),
             'DOMAIN', 'fixed analytic or production dimensions')


def _rectangle(encoded):
    real_low, real_high, imag_low, imag_high = (_hex(v) for v in _array(encoded, 4, 'MODE'))
    _require(real_low <= real_high and imag_low <= imag_high, 'INTERVAL', 'ordered Q256 rectangle')
    return real_low, real_high, imag_low, imag_high


def _mode_triplets(rows, size):
    """Independent magnitude-product route, without the producer expansion.

    For each active component: base=X^2, transform=(|X|+tau)^2,
    enlarged=(|X|+tau+alpha)^2. The two errors are consecutive
    differences. Their nonnegativity and sum are checked exactly.
    """
    _require(type(rows) is list, 'ROW', 'complete row list')
    _domain(size, len(rows))
    expected_ids = ROW_IDS if size == SIZE else tuple(range(len(rows)))
    radii = []
    for row_id, row in zip(expected_ids, rows):
        _object(row, ROW_FIELDS, 'ROW')
        _equal(row['row'], row_id, 'ROW', 'declared row order')
        alpha = _decode(row['alpha'])
        _require(alpha >= 0, 'ALPHA', 'nonnegative coefficient radius')
        radii.append(alpha)
        _array(row['midpoint_modes'], size // 2 + 1, 'MODE')
        _pin(row['mode_identity'])
        _equal(_canonical_pin(row['midpoint_modes']), row['mode_identity'], 'MODE', 'complete mode record identity')
        for endpoint in (0, size // 2):
            _, _, low, high = _rectangle(row['midpoint_modes'][endpoint])
            _require(low <= 0 <= high, 'INTERVAL', 'real endpoint compatible with zero imaginary part')
    output = []
    for mode in range(1, size // 2 + 1):
        central = transform_error = coefficient_error = Fraction(0)
        for row, alpha in zip(rows, radii):
            left, right, bottom, top = _rectangle(row['midpoint_modes'][mode])
            # At Nyquist only the real component is active. In particular,
            # neither imaginary tau nor imaginary alpha is added there.
            active = ((left, right),) if mode == size // 2 else ((left, right), (bottom, top))
            for lower, upper in active:
                midpoint = _fraction(Fraction(_integer(lower + upper), 2 * GRID))
                radius = _fraction(Fraction(_integer(upper - lower), 2 * GRID))
                base = _times(midpoint, midpoint)
                magnitude_with_tau = _plus(abs(midpoint), radius)
                magnitude_with_all = _plus(magnitude_with_tau, alpha)
                transform_square = _times(magnitude_with_tau, magnitude_with_tau)
                outer_square = _times(magnitude_with_all, magnitude_with_all)
                tau_error = _minus(transform_square, base)
                alpha_error = _minus(outer_square, transform_square)
                total_error = _minus(outer_square, base)
                _require(tau_error >= 0 and alpha_error >= 0
                         and _plus(tau_error, alpha_error) == total_error,
                         'EXACT', 'nonnegative product-form error decomposition')
                central = _plus(central, base)
                transform_error = _plus(transform_error, tau_error)
                coefficient_error = _plus(coefficient_error, alpha_error)
        multiplicity = Fraction(1 if mode == size // 2 else 2)
        output.append((_times(multiplicity, central), _times(multiplicity, transform_error),
                       _times(multiplicity, coefficient_error)))
    return output


def _expected_mode(mode, triple, size):
    return {'k': mode, 'pair_weight': 1 if mode == size // 2 else 2,
            'c': _encode(triple[0]), 'h_tau': _encode(triple[1]), 'h_alpha': _encode(triple[2])}


def _psd_values(record, size):
    _object(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'PSD')
    _equal(record['dtype'], '<f8', 'PSD', 'original little-endian binary64 dtype')
    _equal(record['shape'], [size // 2 + 1], 'PSD', 'complete PSD shape')
    _array(record['values_hex'], size // 2 + 1, 'PSD')
    _require(type(record['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}', record['sha256']) is not None,
             'PSD', 'original array SHA256')
    digest = hashlib.sha256()
    eigenvalues = []
    for index, text in enumerate(record['values_hex']):
        _require(type(text) is str, 'PSD', 'binary64 hexadecimal string')
        try:
            value = float.fromhex(text)
        except (ValueError, OverflowError) as error:
            raise ValidationError('PSD', 'invalid binary64 value') from error
        _require(math.isfinite(value) and value >= 0 and value.hex() == text,
                 'PSD', 'finite nonnegative canonical binary64')
        # Signed zero remains in the original byte digest even though the
        # corresponding exact rational is zero. DC is read and hashed too.
        digest.update(struct.pack('<d', value))
        numerator, denominator = value.as_integer_ratio()
        factor = RATE if index == 0 or index == size // 2 else RATE // 2
        eigenvalues.append(_times(Fraction(factor), _fraction(Fraction(numerator, denominator))))
    _equal(digest.hexdigest(), record['sha256'], 'PSD', 'original PSD bytes')
    return eigenvalues


def _trace(encoded_matrix, dimension):
    _array(encoded_matrix, dimension, 'BAND')
    decoded = [tuple(_decode(v) for v in _array(row, dimension, 'BAND')) for row in encoded_matrix]
    _require(all(decoded[r][c] == decoded[c][r] for r in range(dimension) for c in range(r)),
             'BAND', 'symmetric inherited center matrix')
    return _sum(decoded[i][i] for i in range(dimension))


def _ratio(numerator, denominator, reason):
    if denominator <= 0:
        return {'value': None, 'undefined_reason': reason}
    return {'value': _encode(_fraction(numerator / denominator)), 'undefined_reason': None}


def _scenario_expectation(held, terms, size, dimension):
    _domain(size, dimension)
    _object(held, INPUT_SCENARIO_FIELDS, 'PSD')
    _require(type(held['id']) is str and held['id'] in SCENARIO_IDS, 'PSD', 'scenario id')
    eigenvalues = _psd_values(held['source_record'], size)
    _require(len(terms) == size // 2, 'MODE', 'complete independently derived modes')
    sums = [Fraction(0), Fraction(0), Fraction(0)]
    # Each scenario has its own exact dot products. DC is retained as an
    # authenticated input but omitted from true operator action alone.
    for index, triple in enumerate(terms, 1):
        for column in range(3):
            sums[column] = _plus(sums[column], _times(eigenvalues[index], triple[column]))
    center, tau_error, alpha_error = sums
    error = _plus(tau_error, alpha_error)
    raw = (_minus(center, error), _plus(center, error))
    lower_trace = _trace(held['C_minus'], dimension)
    upper_trace = _trace(held['C_plus'], dimension)
    delta_lower, delta_upper = _decode(held['delta_minus']), _decode(held['delta_plus'])
    _require(delta_lower >= 0 and delta_upper >= 0, 'BAND', 'nonnegative inherited margins')
    old_band = _interval(held['trace'])
    prior = _interval(held['prior_trace'])
    expected_band = (_minus(lower_trace, _times(Fraction(dimension), delta_lower)),
                     _plus(upper_trace, _times(Fraction(dimension), delta_upper)))
    _require(old_band == expected_band, 'BAND', 'inherited raw trace from complete matrices and margins')
    _require(old_band[0] <= prior[0] <= prior[1] <= old_band[1],
             'ENVELOPE', 'prior intersection contained in inherited raw band')
    count = size.bit_length() - 1
    _array(held['band_extrema'], count, 'BAND')
    spectral_spread = Fraction(0)
    first = 1
    for band_index, bound in enumerate(held['band_extrema']):
        stop = min(2 * first, size // 2 + 1)
        _object(bound, ('index', 'ell', 'u', 'minimum_indices', 'maximum_indices'), 'BAND')
        low = min(eigenvalues[k] for k in range(first, stop))
        high = max(eigenvalues[k] for k in range(first, stop))
        expected = {'index': band_index, 'ell': _encode(low), 'u': _encode(high),
                    'minimum_indices': [k for k in range(first, stop) if eigenvalues[k] == low],
                    'maximum_indices': [k for k in range(first, stop) if eigenvalues[k] == high]}
        _equal(bound, expected, 'BAND', 'complete exact extrema including all ties')
        band_center = _sum(terms[k - 1][0] for k in range(first, stop))
        spectral_spread = _plus(spectral_spread, _times(_minus(high, low), band_center))
        first *= 2
    _require(spectral_spread == _minus(upper_trace, lower_trace),
             'BAND', 'independent fixed-band spectral-spread identity')
    margin = _times(Fraction(dimension), _plus(delta_lower, delta_upper))
    band_width = _plus(spectral_spread, margin)
    _require(band_width == _minus(old_band[1], old_band[0]), 'BAND', 'raw band width decomposition')
    _require(raw[1] <= old_band[1], 'BAND', 'direct upper bounded by inherited band upper')
    final = (max(raw[0], prior[0]), min(raw[1], prior[1]))
    _require(final[0] <= final[1], 'ENVELOPE', 'nonempty exact scalar intersection')
    widths = {'raw': _minus(raw[1], raw[0]), 'ri96': _minus(prior[1], prior[0]),
              'final': _minus(final[1], final[0])}
    ratios = {
        'ri96_over_final_width': _ratio(widths['ri96'], widths['final'], 'zero_width_denominator'),
        'ri96_over_raw_width': _ratio(widths['ri96'], widths['raw'], 'zero_width_denominator'),
        'raw_upper_over_lower': _ratio(raw[1], raw[0], 'nonpositive_lower_endpoint'),
        'ri96_upper_over_lower': _ratio(prior[1], prior[0], 'nonpositive_lower_endpoint'),
        'final_upper_over_lower': _ratio(final[1], final[0], 'nonpositive_lower_endpoint'),
    }
    return {
        'id': held['id'], 'source_identity': _canonical_pin(held['source_record']),
        'center': _encode(center), 'error_tau': _encode(tau_error), 'error_alpha': _encode(alpha_error),
        'error': _encode(error), 'raw': _encoded_interval(raw), 'ri96_raw_band': _encoded_interval(old_band),
        'ri96_prior': _encoded_interval(prior), 'final': _encoded_interval(final),
        'band_spread': _encode(spectral_spread), 'band_margin': _encode(margin), 'band_width': _encode(band_width),
        'widths': {key: _encode(value) for key, value in widths.items()},
        'equalities': {'final_equals_ri96': final == prior, 'final_equals_raw': final == raw},
        'ratios': ratios, 'direct_upper_le_band_upper': True,
    }


def validate_case(row_proofs, held_scenario, mode_terms, result_scenario, *, size):
    """Same arithmetic in exactly the accepted tiny qualification domains.

    No actual RI96 or production provenance is claimed by this pure fixture
    API. It is not an alternative saved-application admission path.
    """
    _require(type(row_proofs) is list, 'ROW', 'tiny row list')
    _require(type(size) is int and (size, len(row_proofs)) in ((4, 1), (4, 2), (8, 1), (8, 8)),
             'DOMAIN', 'only frozen RI97 tiny qualification domains')
    _array(mode_terms, size // 2, 'MODE')
    triples = _mode_triplets(row_proofs, size)
    for mode, (record, triple) in enumerate(zip(mode_terms, triples), 1):
        verify_mode_term(record, _expected_mode(mode, triple, size))
    expected_scenario = _scenario_expectation(held_scenario, triples, size, len(row_proofs))
    verify_scenario(result_scenario, expected_scenario)
    return {'status': 'all_fields_independently_match', 'rows': len(row_proofs),
            'modes': size // 2, 'scenarios': 1}


def validate_result(report, projection, expected_provenance, *, expected_phase):
    """Reconstruct every output; validation of a projection is not body custody."""
    verify_result_fields(report, projection, expected_provenance, expected_phase)
    before_projection, before_provenance = _canonical_pin(projection), _canonical_pin(expected_provenance)
    triples = _mode_triplets(projection['row_proofs'], SIZE)
    for mode, (record, triple) in enumerate(zip(report['mode_terms'], triples), 1):
        verify_mode_term(record, _expected_mode(mode, triple, SIZE))
    for held, actual in zip(projection['scenarios'], report['scenarios']):
        expected = _scenario_expectation(held, triples, SIZE, DIMENSION)
        verify_scenario(actual, expected)
    _equal(_canonical_pin(projection), before_projection, 'INPUT', 'projection remained unchanged')
    _equal(_canonical_pin(expected_provenance), before_provenance, 'PROVENANCE', 'caller provenance remained unchanged')
    return {'status': 'all_fields_independently_match', 'rows': DIMENSION,
            'modes': SIZE // 2, 'scenarios': 4}


def load_result(body, projection, expected_provenance, *, expected_phase):
    report = _parse(body)
    _equal(_body_pin(body), _canonical_pin(report), 'CANONICAL', 'complete canonical result bytes')
    validate_result(report, projection, expected_provenance, expected_phase=expected_phase)
    return report


def _saved_projection(body):
    # The fixed complete byte identity is checked before the first scientific
    # parse. Hash equality does not establish the inherited transform proof.
    _equal(_body_pin(body), RI96_PIN, 'INPUT', 'fixed RI96 body before any decode')
    held = _parse(body)
    _object(held, ('schema', 'phase', 'status', 'model', 'method', 'provenance', 'prior', 'rows',
                   'row_proofs', 'twiddles', 'bands', 'midpoint_parseval', 'scenarios', 'gates', 'limitations'), 'INPUT')
    _equal(held['schema'], 'ri93-frequency-band-proxy-v1', 'INPUT', 'accepted RI96 schema')
    _equal(held['phase'], 'fixed_saved_application', 'PHASE', 'held actual phase')
    _equal(held['status'], 'all_gates_passed', 'INPUT', 'accepted predecessor status')
    _equal(held['method'], HELD_METHOD, 'DOMAIN', 'complete inherited method')
    _equal(held['rows'], list(ROW_IDS), 'ROW', 'exact inherited row selection')
    _equal(held['limitations'], HELD_LIMITATIONS, 'INPUT', 'complete inherited limitations')
    rows = []
    for entry in _array(held['row_proofs'], DIMENSION, 'ROW'):
        _object(entry, ('row', 'alpha', 'initial_q256', 'input_identity', 'midpoint_modes', 'mode_identity'), 'ROW')
        rows.append({'row': entry['row'], 'alpha': entry['alpha'],
                     'midpoint_modes': entry['midpoint_modes'], 'mode_identity': entry['mode_identity']})
    scenarios = []
    for entry in _array(held['scenarios'], 4, 'PSD'):
        _require(type(entry) is dict and all(key in entry for key in INPUT_SCENARIO_FIELDS if key != 'prior_trace'),
                 'PSD', 'all inherited scenario operands retained')
        _require(type(entry.get('scalar_intersections')) is dict and 'trace' in entry['scalar_intersections'],
                 'ENVELOPE', 'inherited scalar trace intersection')
        scenarios.append({
            'id': entry['id'], 'source_record': entry['source_record'], 'band_extrema': entry['band_extrema'],
            'C_minus': entry['C_minus'], 'C_plus': entry['C_plus'],
            'delta_minus': entry['delta_minus'], 'delta_plus': entry['delta_plus'],
            'trace': entry['trace'], 'prior_trace': entry['scalar_intersections']['trace'],
        })
    projection = {'context': 'accepted_ri96_saved_output', 'held_identity': dict(RI96_PIN),
                  'rows': list(ROW_IDS), 'row_proofs': rows, 'scenarios': scenarios,
                  'held_provenance_identity': _canonical_pin(held['provenance']),
                  'held_limitations': list(held['limitations'])}
    # The unprojected accepted fields may now be released; their exact byte
    # identity and completed upstream validation stay named premises.
    del held
    _projection(projection, 'fixed_saved_application')
    _equal(_body_pin(body), RI96_PIN, 'INPUT', 'unchanged admitted RI96 bytes')
    return projection


def validate_saved(report, ri96_body, expected_provenance):
    """Actual fixed saved-body validation with independent byte admission.

    The external caller must first admit source/runtime/upstream custody.
    This API never opens paths or recreates that custody from result flags.
    """
    _equal(_body_pin(ri96_body), RI96_PIN, 'INPUT', 'whole RI96 bytes before decoding')
    _provenance(expected_provenance, 'fixed_saved_application', RI96_PIN)
    projection = _saved_projection(ri96_body)
    summary = validate_result(report, projection, expected_provenance, expected_phase='fixed_saved_application')
    _equal(_body_pin(ri96_body), RI96_PIN, 'INPUT', 'whole RI96 bytes after reconstruction')
    return summary
