"""Fixed RI97 scalar aggregation. Source-only until separately frozen admission.

No import-time I/O, FFT, scientific library, subprocess or CLI. Transform and
upstream covariance premises are inherited from the exactly admitted RI96.
"""
from fractions import Fraction as F
import hashlib
import json
import math
import re
import struct

BITS, Q, M, FS, D = 262144, 1 << 256, 16384, 4096, 8
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
ORDER = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
DESIGN = {'bytes': 23571, 'sha256': '65edcabef43e15cfa44299c19276c194aed717269fe17702877f76ca8af379e7'}
INPUT = {'bytes': 41673703, 'sha256': '5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580'}
DESIGN_ACCEPTANCE = {'bytes': 2430, 'sha256': 'a2b76efbe5105c286c8b50d9183e407726c3404b36309d0ed9fb65c95b1b9539'}
RI96_ACCEPTANCE = {'bytes': 6551, 'sha256': 'c7842d05fa0d34dddf60d5b3963abb0dbbcae6090ebfcc28af7ca525f61cc836'}
METHOD = {'M': M, 'N': 2769, 'L': 4096, 'T': 10961, 'output': D, 'fs': FS,
          'rows': list(ROWS), 'precision_bits': 256, 'integer_bit_limit': BITS,
          'unitary_divisor': 128, 'band_count': 14,
          'psd_map': 'fs_p_at_endpoints_fs_p_over_2_at_interior',
          'pair_weights': 'interior_2_nyquist_1',
          'dc': 'true_action_zero_inherited_midpoint_unchanged',
          'nyquist_imaginary': 'center_tau_alpha_all_zero',
          'arithmetic': 'exact_rational_scalar_aggregation_no_new_transform',
          'intersection': 'scalar_with_accepted_ri96_trace_only',
          'quantity': 'centered_discrepancy_energy_sum_of_eight_coordinates'}
HELD_METHOD = {'M': M, 'N': 2769, 'L': 4096, 'T': 10961, 'output': D, 'fs': FS,
               'precision_bits': 256, 'integer_bit_limit': BITS, 'unitary_divisor': 128,
               'transform_sign': 1, 'band_count': 14, 'arithmetic': 'outward_Q256_integer_intervals',
               'normalization': 'exact_division_then_outward_Q256'}
HELD_LIMITATIONS = [
    'The four inherited empirical PSDs define separate postulated finite four-second circulant proxies, not established physical noise covariance.',
    'All input bins are retained; only true A DC action is omitted by the accepted constant-annihilation theorem.',
    'RI73 row enclosure and custody are inherited premises; no adjoint or coefficient reconstruction is performed.',
    'Q256 transform rounding and retained coefficient radii are enclosed without assuming independent errors.',
    'Certified band endpoints need not dominate the prior global endpoints; indefinite lower endpoints are not clipped.',
    'Loewner bounds concern quadratic forms; off-diagonal entries are not scalar variance intervals.',
    'The already accessed 32-second inputs are development/calibration evidence, not independent held-out validation.',
    'Nominal V2/C02, blank literal Yunits and the clear L1 NO_CW_HW_INJ flag remain inherited limitations.',
    'No calibrated physical meaning below 10 Hz, stationarity, Gaussianity, detector independence or estimation-uncertainty law is established.',
    'No colored covariance inverse, whitening, residual score, SNR, p-value, physical adequacy or native forward map is supplied; RET stays paused.',
]
FAKE_LIMITATIONS = ['Fabricated RI98 projection; no observed input or predecessor execution.']
PREMISES = [
    'RI96 completed independent transform validation and saved arithmetic/custody acceptance are inherited; no new FFT or coefficient reconstruction.',
    'RI73 coefficient enclosures, constant annihilation and RI96 midpoint rectangles/alpha remain conditional accepted premises.',
    'The four finite circulant covariance models and all original PSD bins are unchanged.',
]
LIMITATIONS = [
    'Exact bounds concern centered discrepancy energy summed over eight fixed selected coordinates, not all2769 outputs or uncentered energy without a mean premise.',
    'Nonnegative deterministic enclosure terms and their split are not statistical estimation uncertainty or confidence intervals.',
    'Negative raw endpoints and undefined ratios are retained; no useful width improvement is required.',
    'The already accessed32-second inputs remain development/calibration evidence, not protected held-out validation.',
    'Nominal V2/C02, blank literal Yunits, the clear L1 NO_CW_HW_INJ flag and unknown calibration meaning below10Hz remain inherited.',
    'Finite four-second circulant wraparound, physical noise adequacy, stationarity, detector independence and empirical PSD error are not validated.',
    'No native forward map, physical geometry/gravity result, SNR, p-value or RET work is supplied; RET remains paused.',
]
GATES = ('admission:phase', 'admission:input', 'admission:rows', 'admission:psds',
         'mode:complete', 'endpoint:real', 'scenario:H1:left', 'scenario:H1:right',
         'scenario:L1:left', 'scenario:L1:right', 'completion:input_stable')
SCENARIO_KEYS = ('id', 'source_record', 'band_extrema', 'C_minus', 'C_plus',
                 'delta_minus', 'delta_plus', 'trace', 'prior_trace')


class TraceError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def require(ok, code, message):
    if not ok:
        raise TraceError(code, message)


def keys(value, fields, code='SCHEMA'):
    require(type(value) is dict and all(type(k) is str for k in value)
            and set(value) == set(fields), code, 'closed object fields')


def same(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) in (list, tuple):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


def equal(a, b, code, message):
    require(same(a, b), code, message)


def sequence(value, length, code='SCHEMA'):
    require(type(value) is list and len(value) == length, code, 'complete list length')
    return value


def integer(value):
    require(type(value) is int, 'EXACT', 'plain integer')
    require(abs(value).bit_length() <= BITS, 'RESOURCE', 'integer bit ceiling')
    return value


def rational(value):
    require(type(value) is F, 'EXACT', 'exact Fraction')
    integer(value.numerator); integer(value.denominator)
    return value


def add(a, b):
    return rational(rational(a) + rational(b))


def mul(a, b):
    return rational(rational(a) * rational(b))


def total(values):
    answer = F(0)
    for x in values:
        answer = add(answer, x)
    return answer


def hex_integer(value):
    require(type(value) is str, 'EXACT', 'hexadecimal integer string')
    require(len(value) <= (BITS + 3) // 4 + 1, 'RESOURCE', 'integer string ceiling')
    require(re.fullmatch(r'(?:0|-?[1-9a-f][0-9a-f]*)', value) is not None,
            'EXACT', 'canonical signed hexadecimal integer')
    return integer(int(value, 16))


def scalar(value):
    value = rational(value)
    return [format(value.numerator, 'x'), format(value.denominator, 'x')]


def decode_scalar(value):
    sequence(value, 2, 'EXACT')
    a, b = map(hex_integer, value)
    require(b > 0, 'EXACT', 'positive rational denominator')
    result = rational(F(a, b))
    equal(scalar(result), value, 'EXACT', 'reduced rational encoding')
    return result


def encode(value):
    if type(value) is F:
        return scalar(value)
    if type(value) in (list, tuple):
        return [encode(x) for x in value]
    if type(value) is dict:
        return {k: encode(v) for k, v in value.items()}
    return value


def canonical_parts(value):
    for chunk in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True,
                                  allow_nan=False).iterencode(value):
        yield chunk.encode('ascii')
    yield b'\n'


def canonical(value):
    return b''.join(canonical_parts(value))


def identity(body):
    require(type(body) is bytes, 'INPUT', 'immutable bytes')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def canonical_pin(value):
    h, n = hashlib.sha256(), 0
    for chunk in canonical_parts(value):
        h.update(chunk); n += len(chunk)
    return {'bytes': n, 'sha256': h.hexdigest()}


def pin(value):
    keys(value, ('bytes', 'sha256'), 'PROVENANCE')
    require(type(value['bytes']) is int and value['bytes'] >= 0 and
            type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']),
            'PROVENANCE', 'byte identity fields')


def _pairs(items):
    value = {}
    for key, item in items:
        require(key not in value, 'SCHEMA', 'duplicate JSON key')
        value[key] = item
    return value


def parse_json(body):
    require(type(body) is bytes, 'INPUT', 'immutable JSON body')
    def bad(text):
        raise TraceError('EXACT', 'nonfinite JSON literal')
    try:
        return json.loads(body, object_pairs_hook=_pairs, parse_constant=bad)
    except TraceError:
        raise
    except (UnicodeError, ValueError) as error:
        raise TraceError('SCHEMA', 'invalid UTF8 JSON') from error


def domain(size, dimension):
    require(type(size) is int and type(dimension) is int and
            (size, dimension) in ((4, 1), (4, 2), (8, 1), (8, 8), (M, D)),
            'DOMAIN', 'fixed analytic/production domain')


def bands(size):
    require(type(size) is int and size in (4, 8, M), 'DOMAIN', 'fixed sizes')
    starts = [1 << p for p in range(size.bit_length() - 1)]
    return [(start, min(2 * start, size // 2 + 1)) for start in starts]


def rectangle(value):
    a, b, c, d = map(hex_integer, sequence(value, 4, 'MODE'))
    require(a <= b and c <= d, 'INTERVAL', 'ordered component intervals')
    return a, b, c, d


def derive_modes(row_proofs, *, size=M):
    require(type(row_proofs) is list, 'ROW', 'row records list')
    dimension = len(row_proofs); domain(size, dimension)
    expected = list(ROWS) if size == M else list(range(dimension))
    alphas = []
    for name, record in zip(expected, row_proofs):
        keys(record, ('row', 'alpha', 'midpoint_modes', 'mode_identity'), 'ROW')
        equal(record['row'], name, 'ROW', 'fixed row order')
        alpha = decode_scalar(record['alpha'])
        require(alpha >= 0, 'ALPHA', 'nonnegative coefficient radius')
        alphas.append(alpha)
        sequence(record['midpoint_modes'], size // 2 + 1, 'MODE')
        pin(record['mode_identity'])
        equal(canonical_pin(record['midpoint_modes']), record['mode_identity'], 'MODE', 'complete mode byte identity')
        for k in (0, size // 2):
            a, b, c, d = rectangle(record['midpoint_modes'][k])
            require(c <= 0 <= d, 'INTERVAL', 'real endpoint imaginary compatibility')
    terms = []
    den = 2 * Q
    for k in range(1, size // 2 + 1):
        weight = 1 if k == size // 2 else 2
        csum, tsum, asum = F(0), F(0), F(0)
        for record, alpha in zip(row_proofs, alphas):
            a, b, c, d = rectangle(record['midpoint_modes'][k])
            pairs = [(F(integer(a+b), den), F(integer(b-a), den))]
            if k != size // 2:
                pairs.append((F(integer(c+d), den), F(integer(d-c), den)))
            for center, tau in pairs:
                center, tau = rational(center), rational(tau)
                csum = add(csum, mul(center, center))
                tsum = add(tsum, add(mul(mul(F(2), abs(center)), tau), mul(tau, tau)))
                extra = add(mul(mul(F(2), abs(center)), alpha),
                            add(mul(mul(F(2), tau), alpha), mul(alpha, alpha)))
                asum = add(asum, extra)
        terms.append({'k': k, 'pair_weight': weight, 'c': scalar(mul(F(weight), csum)),
                      'h_tau': scalar(mul(F(weight), tsum)), 'h_alpha': scalar(mul(F(weight), asum))})
    return terms


def decode_psd(record, size):
    keys(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'PSD')
    equal(record['dtype'], '<f8', 'PSD', 'little-endian binary64')
    equal(record['shape'], [size // 2 + 1], 'PSD', 'complete PSD shape')
    sequence(record['values_hex'], size // 2 + 1, 'PSD')
    require(type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']), 'PSD', 'PSD digest')
    digest = hashlib.sha256(); result = []
    for text in record['values_hex']:
        require(type(text) is str, 'PSD', 'binary64 hex string')
        try: value = float.fromhex(text)
        except (ValueError, OverflowError) as error: raise TraceError('PSD', 'invalid binary64 hex') from error
        require(math.isfinite(value) and value >= 0 and value.hex() == text,
                'PSD', 'finite nonnegative canonical binary64')
        digest.update(struct.pack('<d', value)); result.append(rational(F.from_float(value)))
    equal(digest.hexdigest(), record['sha256'], 'PSD', 'original PSD array identity')
    return result


def matrix(value, dimension):
    result = [[decode_scalar(x) for x in sequence(row, dimension, 'BAND')]
              for row in sequence(value, dimension, 'BAND')]
    require(all(result[i][j] == result[j][i] for i in range(dimension) for j in range(dimension)),
            'BAND', 'symmetric inherited matrix')
    return result


def interval(value):
    lo, hi = map(decode_scalar, sequence(value, 2, 'ENVELOPE'))
    require(lo <= hi, 'ENVELOPE', 'ordered scalar interval')
    return lo, hi


def ratio(num, den, reason):
    rational(num); rational(den)
    return {'value': scalar(rational(num / den)) if den > 0 else None,
            'undefined_reason': None if den > 0 else reason}


def derive_scenario(record, mode_terms, *, size=M, dimension=D):
    domain(size, dimension)
    keys(record, SCENARIO_KEYS, 'PSD')
    require(type(record['id']) is str and record['id'] in ORDER, 'PSD', 'scenario name')
    values = decode_psd(record['source_record'], size)
    lambdas = [mul(F(FS if k in (0, size//2) else FS//2), value) for k, value in enumerate(values)]
    sequence(mode_terms, size // 2, 'MODE')
    cs, ht, ha = [], [], []
    for k, term in enumerate(mode_terms, 1):
        keys(term, ('k', 'pair_weight', 'c', 'h_tau', 'h_alpha'), 'MODE')
        equal(term['k'], k, 'MODE', 'complete mode order')
        equal(term['pair_weight'], 1 if k == size//2 else 2, 'MODE', 'pair weight')
        scalars = [decode_scalar(term[name]) for name in ('c', 'h_tau', 'h_alpha')]
        require(all(x >= 0 for x in scalars), 'MODE', 'nonnegative mode terms')
        cs.append(scalars[0]); ht.append(scalars[1]); ha.append(scalars[2])
    center = total(mul(lambdas[k], cs[k-1]) for k in range(1, size//2+1))
    et = total(mul(lambdas[k], ht[k-1]) for k in range(1, size//2+1))
    ea = total(mul(lambdas[k], ha[k-1]) for k in range(1, size//2+1))
    error = add(et, ea); raw = (add(center, -error), add(center, error))
    cm, cp = matrix(record['C_minus'], dimension), matrix(record['C_plus'], dimension)
    dm, dp = decode_scalar(record['delta_minus']), decode_scalar(record['delta_plus'])
    require(dm >= 0 and dp >= 0, 'BAND', 'nonnegative inherited error margins')
    tm, tp = total(cm[i][i] for i in range(dimension)), total(cp[i][i] for i in range(dimension))
    old_raw, prior = interval(record['trace']), interval(record['prior_trace'])
    equal(list(old_raw), [add(tm, -mul(F(dimension), dm)), add(tp, mul(F(dimension), dp))],
          'BAND', 'raw band trace identity')
    require(old_raw[0] <= prior[0] <= prior[1] <= old_raw[1], 'ENVELOPE', 'prior is scalar band intersection')
    partitions = bands(size); sequence(record['band_extrema'], len(partitions), 'BAND')
    spread = F(0)
    for index, ((first, stop), held) in enumerate(zip(partitions, record['band_extrema'])):
        keys(held, ('index', 'ell', 'u', 'minimum_indices', 'maximum_indices'), 'BAND')
        lo, hi = min(lambdas[first:stop]), max(lambdas[first:stop])
        expected = {'index': index, 'ell': scalar(lo), 'u': scalar(hi),
                    'minimum_indices': [k for k in range(first, stop) if lambdas[k] == lo],
                    'maximum_indices': [k for k in range(first, stop) if lambdas[k] == hi]}
        equal(held, expected, 'BAND', 'complete original extrema and ties')
        spread = add(spread, mul(add(hi, -lo), total(cs[first-1:stop-1])))
    equal(spread, add(tp, -tm), 'BAND', 'spectral spread identity')
    margin = mul(F(dimension), add(dm, dp)); width = add(spread, margin)
    equal(width, add(old_raw[1], -old_raw[0]), 'BAND', 'raw band width decomposition')
    require(raw[1] <= old_raw[1], 'BAND', 'direct upper exceeds inherited band upper')
    final = (max(raw[0], prior[0]), min(raw[1], prior[1]))
    require(final[0] <= final[1], 'ENVELOPE', 'empty scalar intersection')
    widths = {'raw': add(raw[1], -raw[0]), 'ri96': add(prior[1], -prior[0]),
              'final': add(final[1], -final[0])}
    ratios = {'ri96_over_final_width': ratio(widths['ri96'], widths['final'], 'zero_width_denominator'),
              'ri96_over_raw_width': ratio(widths['ri96'], widths['raw'], 'zero_width_denominator'),
              'raw_upper_over_lower': ratio(raw[1], raw[0], 'nonpositive_lower_endpoint'),
              'ri96_upper_over_lower': ratio(prior[1], prior[0], 'nonpositive_lower_endpoint'),
              'final_upper_over_lower': ratio(final[1], final[0], 'nonpositive_lower_endpoint')}
    return encode({'id': record['id'], 'source_identity': canonical_pin(record['source_record']),
                   'center': center, 'error_tau': et, 'error_alpha': ea, 'error': error,
                   'raw': raw, 'ri96_raw_band': old_raw, 'ri96_prior': prior, 'final': final,
                   'band_spread': spread, 'band_margin': margin, 'band_width': width,
                   'widths': widths, 'equalities': {'final_equals_ri96': final == prior, 'final_equals_raw': final == raw},
                   'ratios': ratios, 'direct_upper_le_band_upper': True})


def provenance_check(provenance, phase, input_identity):
    require(type(phase) is str and phase in ('fabricated_qualification', 'fixed_saved_application'), 'PHASE', 'fixed phase')
    keys(provenance, ('sources', 'input', 'acceptance', 'runtime'), 'PROVENANCE')
    keys(provenance['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation'), 'PROVENANCE')
    for item in provenance['sources'].values(): pin(item)
    equal(provenance['sources']['design'], DESIGN, 'SOURCE', 'accepted RI97 design')
    pin(provenance['input']); equal(provenance['input'], input_identity, 'INPUT', 'complete operand identity')
    keys(provenance['acceptance'], ('design', 'ri96', 'qualification', 'custody'), 'PROVENANCE')
    equal(provenance['acceptance']['design'], DESIGN_ACCEPTANCE, 'PROVENANCE', 'root design acceptance')
    equal(provenance['acceptance']['ri96'], RI96_ACCEPTANCE, 'PROVENANCE', 'root prior result acceptance')
    for name in ('qualification', 'custody'):
        if phase == 'fabricated_qualification':
            require(provenance['acceptance'][name] is None, 'PHASE', 'fabrication cannot claim completed admission')
        else: pin(provenance['acceptance'][name])
    keys(provenance['runtime'], ('fingerprint', 'inventory', 'interpreter'), 'PROVENANCE')
    for value in provenance['runtime'].values(): pin(value)


def projection_check(projection, phase):
    keys(projection, ('context', 'held_identity', 'rows', 'row_proofs', 'scenarios',
                      'held_provenance_identity', 'held_limitations'), 'INPUT')
    pin(projection['held_identity']); pin(projection['held_provenance_identity'])
    if phase == 'fixed_saved_application':
        equal(projection['context'], 'accepted_ri96_saved_output', 'PHASE', 'actual projection context')
        equal(projection['held_identity'], INPUT, 'INPUT', 'exact complete held result')
        equal(projection['held_limitations'], HELD_LIMITATIONS, 'INPUT', 'held scientific limitations')
    elif phase == 'fabricated_qualification':
        equal(projection['context'], 'fabricated_projection_not_observed', 'PHASE', 'fabricated projection context')
        require(projection['held_identity'] != INPUT, 'PHASE', 'fabricated held tag differs from actual identity')
        equal(projection['held_limitations'], FAKE_LIMITATIONS, 'PHASE', 'fabricated predecessor label')
        equal(projection['held_provenance_identity'], canonical_pin({'context': 'fabricated_not_observed'}),
              'PHASE', 'fabricated held provenance label')
    else: raise TraceError('PHASE', 'fixed phase')
    equal(projection['rows'], list(ROWS), 'ROW', 'complete production rows')
    sequence(projection['row_proofs'], D, 'ROW'); sequence(projection['scenarios'], 4, 'PSD')
    for name, record in zip(ORDER, projection['scenarios']):
        keys(record, SCENARIO_KEYS, 'PSD'); equal(record['id'], name, 'PSD', 'four scenario order')


def build_result(projection, provenance, *, phase='fabricated_qualification'):
    projection_check(projection, phase)
    projection_before, provenance_before = canonical_pin(projection), canonical_pin(provenance)
    input_identity = INPUT if phase == 'fixed_saved_application' else projection_before
    provenance_check(provenance, phase, input_identity)
    terms = derive_modes(projection['row_proofs'])
    scenarios = [derive_scenario(record, terms) for record in projection['scenarios']]
    equal(canonical_pin(projection), projection_before, 'INPUT', 'projection changed during arithmetic')
    equal(canonical_pin(provenance), provenance_before, 'PROVENANCE', 'caller provenance changed')
    return {'schema': 'ri98-mode-weighted-trace-v1', 'phase': phase,
            'status': 'all_declared_checks_passed', 'method': encode(METHOD), 'provenance': encode(provenance),
            'mode_terms': terms, 'scenarios': scenarios,
            'checks': {'inventory': list(GATES), 'counts': {'total': 11, 'passed': 11, 'failed': 0},
                       'results': [{'id': name, 'passed': True} for name in GATES]},
            'inherited_premises': {'labels': list(PREMISES), 'projection_identity': projection_before,
                                   'held_provenance_identity': dict(projection['held_provenance_identity']),
                                   'held_limitations': list(projection['held_limitations'])},
            'limitations': list(LIMITATIONS)}


def project_saved(body):
    equal(identity(body), INPUT, 'INPUT', 'complete RI96 body before scientific parse')
    held = parse_json(body)
    keys(held, ('schema', 'phase', 'status', 'model', 'method', 'provenance', 'prior', 'rows',
                'row_proofs', 'twiddles', 'bands', 'midpoint_parseval', 'scenarios', 'gates', 'limitations'), 'INPUT')
    equal(held['schema'], 'ri93-frequency-band-proxy-v1', 'INPUT', 'held schema')
    equal(held['phase'], 'fixed_saved_application', 'PHASE', 'held actual phase')
    equal(held['status'], 'all_gates_passed', 'INPUT', 'held completion')
    equal(held['method'], HELD_METHOD, 'DOMAIN', 'unchanged upstream method')
    equal(held['limitations'], HELD_LIMITATIONS, 'INPUT', 'held limitations')
    row_proofs = []
    for record in sequence(held['row_proofs'], D, 'ROW'):
        keys(record, ('row', 'alpha', 'initial_q256', 'input_identity', 'midpoint_modes', 'mode_identity'), 'ROW')
        row_proofs.append({k: record[k] for k in ('row', 'alpha', 'midpoint_modes', 'mode_identity')})
    scenarios = []
    for record in sequence(held['scenarios'], 4, 'PSD'):
        require(type(record) is dict and all(k in record for k in SCENARIO_KEYS if k != 'prior_trace')
                and type(record.get('scalar_intersections')) is dict and 'trace' in record['scalar_intersections'],
                'PSD', 'held complete scenario projection')
        scenario = {k: record[k] for k in SCENARIO_KEYS if k != 'prior_trace'}
        scenario['prior_trace'] = record['scalar_intersections']['trace']; scenarios.append(scenario)
    projection = {'context': 'accepted_ri96_saved_output', 'held_identity': dict(INPUT),
                  'rows': held['rows'], 'row_proofs': row_proofs, 'scenarios': scenarios,
                  'held_provenance_identity': canonical_pin(held['provenance']),
                  'held_limitations': held['limitations']}
    projection_check(projection, 'fixed_saved_application')
    return projection


def run_saved(ri96_body, provenance):
    """Actual fixed-body projection; callers independently admit custody/runtime.

    This function neither opens a path nor represents the inherited transform
    proof as a fresh execution. Qualification must not call it with real data.
    """
    equal(identity(ri96_body), INPUT, 'INPUT', 'fixed input before any decode')
    provenance_check(provenance, 'fixed_saved_application', INPUT)
    projection = project_saved(ri96_body)
    result = build_result(projection, provenance, phase='fixed_saved_application')
    equal(identity(ri96_body), INPUT, 'INPUT', 'fixed input after arithmetic')
    return result
