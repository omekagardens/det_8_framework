"""Independent fixed RI100 saved arithmetic audit; no import-time I/O.

Source review and concrete root admission are required before any invocation.
This module imports no primary, validator, qualifier, runtime probe or helper.
Its integer numerator accumulation is separately written. Fixed protocol
vocabulary/provenance below is literal metadata, not an arithmetic oracle.
"""
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import math
import os
import re
import stat
import struct
import sys

BITS = 262144
Q = 1 << 256
M = 16384
D = 8
FS = 4096
ROWS = [0, 1, 27, 805, 1384, 2741, 2767, 2768]
SCENARIOS = ['H1:left', 'H1:right', 'L1:left', 'L1:right']
RI96 = {'bytes': 41673703, 'sha256': '5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580'}
HELD_METHOD = {'M': 16384, 'N': 2769, 'L': 4096, 'T': 10961,
 'output': 8, 'fs': 4096, 'precision_bits': 256, 'integer_bit_limit': 262144,
 'unitary_divisor': 128, 'transform_sign': 1, 'band_count': 14,
 'arithmetic': 'outward_Q256_integer_intervals',
 'normalization': 'exact_division_then_outward_Q256'}
HELD_GATES = ['admission:prior', 'admission:rows', 'transform:twiddles',
 'transform:midpoint_parseval', 'bands:responses', 'scenario:H1:left',
 'scenario:H1:right', 'scenario:L1:left', 'scenario:L1:right', 'completion:source_stable']
METHOD = {'L': 4096, 'M': 16384, 'N': 2769, 'T': 10961, 'arithmetic': 'exact_rational_scalar_aggregation_no_new_transform', 'band_count': 14, 'dc': 'true_action_zero_inherited_midpoint_unchanged', 'fs': 4096, 'integer_bit_limit': 262144, 'intersection': 'scalar_with_accepted_ri96_trace_only', 'nyquist_imaginary': 'center_tau_alpha_all_zero', 'output': 8, 'pair_weights': 'interior_2_nyquist_1', 'precision_bits': 256, 'psd_map': 'fs_p_at_endpoints_fs_p_over_2_at_interior', 'quantity': 'centered_discrepancy_energy_sum_of_eight_coordinates', 'rows': [0, 1, 27, 805, 1384, 2741, 2767, 2768], 'unitary_divisor': 128}
GATES = ['admission:phase', 'admission:input', 'admission:rows', 'admission:psds', 'mode:complete', 'endpoint:real', 'scenario:H1:left', 'scenario:H1:right', 'scenario:L1:left', 'scenario:L1:right', 'completion:input_stable']
PREMISES = ['RI96 completed independent transform validation and saved arithmetic/custody acceptance are inherited; no new FFT or coefficient reconstruction.', 'RI73 coefficient enclosures, constant annihilation and RI96 midpoint rectangles/alpha remain conditional accepted premises.', 'The four finite circulant covariance models and all original PSD bins are unchanged.']
LIMITATIONS = ['Exact bounds concern centered discrepancy energy summed over eight fixed selected coordinates, not all2769 outputs or uncentered energy without a mean premise.', 'Nonnegative deterministic enclosure terms and their split are not statistical estimation uncertainty or confidence intervals.', 'Negative raw endpoints and undefined ratios are retained; no useful width improvement is required.', 'The already accessed32-second inputs remain development/calibration evidence, not protected held-out validation.', 'Nominal V2/C02, blank literal Yunits, the clear L1 NO_CW_HW_INJ flag and unknown calibration meaning below10Hz remain inherited.', 'Finite four-second circulant wraparound, physical noise adequacy, stationarity, detector independence and empirical PSD error are not validated.', 'No native forward map, physical geometry/gravity result, SNR, p-value or RET work is supplied; RET remains paused.']
HELD_LIMITATIONS = ['The four inherited empirical PSDs define separate postulated finite four-second circulant proxies, not established physical noise covariance.', 'All input bins are retained; only true A DC action is omitted by the accepted constant-annihilation theorem.', 'RI73 row enclosure and custody are inherited premises; no adjoint or coefficient reconstruction is performed.', 'Q256 transform rounding and retained coefficient radii are enclosed without assuming independent errors.', 'Certified band endpoints need not dominate the prior global endpoints; indefinite lower endpoints are not clipped.', 'Loewner bounds concern quadratic forms; off-diagonal entries are not scalar variance intervals.', 'The already accessed 32-second inputs are development/calibration evidence, not independent held-out validation.', 'Nominal V2/C02, blank literal Yunits and the clear L1 NO_CW_HW_INJ flag remain inherited limitations.', 'No calibrated physical meaning below 10 Hz, stationarity, Gaussianity, detector independence or estimation-uncertainty law is established.', 'No colored covariance inverse, whitening, residual score, SNR, p-value, physical adequacy or native forward map is supplied; RET stays paused.']
FIXED_PROVENANCE = {'acceptance': {'custody': None, 'design': {'bytes': 2430, 'sha256': 'a2b76efbe5105c286c8b50d9183e407726c3404b36309d0ed9fb65c95b1b9539'}, 'qualification': {'bytes': 4283, 'sha256': '312e023d13618f3343cbbbdd042656cf56a329e44a9768ed278da0042080aee9'}, 'ri96': {'bytes': 6551, 'sha256': 'c7842d05fa0d34dddf60d5b3963abb0dbbcae6090ebfcc28af7ca525f61cc836'}}, 'input': {'bytes': 41673703, 'sha256': '5d0af7febecefd4db07bd93165b2fde7d887e7d3e7caf0243961638538db6580'}, 'runtime': {'fingerprint': {'bytes': 2302, 'sha256': '4e69452eb57244f0e9db42ffee662f8c1f2cf42ccd9db6bb747f9703efea61cd'}, 'interpreter': {'bytes': 52640, 'sha256': '033d83a12ab74b7bcade8248b1bca644f275d3965350b61fe485c2645e1f68e8'}, 'inventory': {'bytes': 1216343, 'sha256': '8b0329a83a1208b21dfb4771d2dd078aae6cb54a1741b7f20b4a4695c06e245c'}}, 'sources': {'consumer': {'bytes': 24861, 'sha256': 'f014394b2e5646b2810fa00f7449eabccea8487c3a0622520eb48416cdcea009'}, 'design': {'bytes': 23571, 'sha256': '65edcabef43e15cfa44299c19276c194aed717269fe17702877f76ca8af379e7'}, 'implementation': {'bytes': 13072, 'sha256': 'da2c12fa9265705b3d9310dc897d16ca13d7cda72e877e57137f40bda240a074'}, 'qualifier': {'bytes': 27707, 'sha256': '770834c35ac4c74655b1f5bc0ddab5e3ecb50cbb14d3801bbe77e7a1612f3150'}, 'validator': {'bytes': 34677, 'sha256': 'f5cf027b819199d6d3d75fc957c8e63cab404f1a825fbbf91a18ad4dd53ab4be'}}}

TOP_FIELDS = ('schema', 'phase', 'status', 'method', 'provenance', 'mode_terms',
              'scenarios', 'checks', 'inherited_premises', 'limitations')
HELD_TOP = ('schema', 'phase', 'status', 'model', 'method', 'provenance', 'prior',
            'rows', 'row_proofs', 'twiddles', 'bands', 'midpoint_parseval',
            'scenarios', 'gates', 'limitations')
HELD_SCENARIO = ('id', 'source_record', 'band_extrema', 'C_minus', 'H_minus',
                 'C_plus', 'H_plus', 'delta_minus', 'delta_plus', 'lower', 'upper',
                 'diagonal', 'trace', 'global_lower', 'global_upper', 'scalar_intersections')
PROJECT_SCENARIO = ('id', 'source_record', 'band_extrema', 'C_minus', 'C_plus',
                    'delta_minus', 'delta_plus', 'trace')
MODE_FIELDS = ('k', 'pair_weight', 'c', 'h_tau', 'h_alpha')
SCALAR_FIELDS = ('id', 'source_identity', 'center', 'error_tau', 'error_alpha',
                 'error', 'raw', 'ri96_raw_band', 'ri96_prior', 'final',
                 'band_spread', 'band_margin', 'band_width', 'widths',
                 'equalities', 'ratios', 'direct_upper_le_band_upper')


class AuditFailure(ValueError):
    pass


def demand(ok, message):
    if not ok:
        raise AuditFailure(message)


def fields(value, wanted, label):
    demand(type(value) is dict and all(type(k) is str for k in value)
           and set(value) == set(wanted), label + ': closed object')


def items(value, count, label):
    demand(type(value) is list and len(value) == count, label + ': exact list length')
    return value


def strict_equal(left, right, label):
    demand(type(left) is type(right), label + ': exact type')
    if type(left) is dict:
        demand(left.keys() == right.keys(), label + ': object keys')
        for name in left:
            strict_equal(left[name], right[name], label + '/' + name)
    elif type(left) in (list, tuple):
        demand(len(left) == len(right), label + ': sequence length')
        for index, (a, b) in enumerate(zip(left, right)):
            strict_equal(a, b, label + '/' + str(index))
    else:
        demand(left == right, label + ': unequal')


def parts(value):
    for piece in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True,
                                   allow_nan=False).iterencode(value):
        yield piece.encode('ascii')
    yield b'\n'


def body_pin(body):
    demand(type(body) is bytes, 'immutable byte body')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def value_pin(value):
    digest, length = hashlib.sha256(), 0
    for piece in parts(value):
        digest.update(piece)
        length += len(piece)
    return {'bytes': length, 'sha256': digest.hexdigest()}


def identity(value, label='identity'):
    fields(value, ('bytes', 'sha256'), label)
    demand(type(value['bytes']) is int and value['bytes'] > 0 and
           type(value['sha256']) is str and
           re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
           label + ': concrete nonempty identity')
    return value


def decode_json(body, *, scientific):
    def pairs(rows):
        result = {}
        for key, value in rows:
            demand(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def forbidden(token):
        raise AuditFailure('forbidden numeric JSON token: ' + token)
    opts = {'object_pairs_hook': pairs, 'parse_constant': forbidden}
    if scientific:
        opts['parse_float'] = forbidden
    try:
        return json.loads(body, **opts)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise AuditFailure('invalid JSON bytes') from error


def whole_json(body, *, scientific=True):
    value = decode_json(body, scientific=scientific)
    strict_equal(value_pin(value), body_pin(body), 'complete canonical JSON')
    return value


def integer(value):
    demand(type(value) is int and abs(value).bit_length() <= BITS,
           'plain integer within inherited bit ceiling')
    return value


def hex_number(text):
    demand(type(text) is str and len(text) <= (BITS + 3) // 4 + 1 and
           re.fullmatch(r'0|-?[1-9a-f][0-9a-f]*', text) is not None,
           'canonical signed hexadecimal integer')
    return integer(int(text, 16))


def bounded(value):
    demand(type(value) is Fraction, 'exact rational arithmetic')
    integer(value.numerator)
    integer(value.denominator)
    return value


def rational(pair):
    numerator, denominator = (hex_number(x) for x in items(pair, 2, 'rational'))
    demand(denominator > 0 and math.gcd(numerator, denominator) == 1,
           'positive denominator and reduced rational')
    return bounded(Fraction(numerator, denominator))


def plus(a, b):
    return bounded(bounded(a) + bounded(b))


def times(a, b):
    return bounded(bounded(a) * bounded(b))


def sum_exact(values):
    result = Fraction(0)
    for value in values:
        result = plus(result, value)
    return result


def encoded(value):
    if type(value) is Fraction:
        bounded(value)
        return [format(value.numerator, 'x'), format(value.denominator, 'x')]
    if type(value) in (tuple, list):
        return [encoded(x) for x in value]
    if type(value) is dict:
        return {k: encoded(v) for k, v in value.items()}
    return value


def rectangle(value):
    a, b, c, d = [hex_number(t) for t in items(value, 4, 'Q256 rectangle')]
    demand(a <= b and c <= d, 'ordered Q256 component endpoints')
    return a, b, c, d


def scalar_interval(value):
    lo, hi = [rational(x) for x in items(value, 2, 'scalar interval')]
    demand(lo <= hi, 'ordered scalar interval')
    return lo, hi


def gates(names):
    return {'inventory': names, 'counts': {'total': len(names), 'passed': len(names), 'failed': 0},
            'results': [{'id': name, 'passed': True} for name in names]}


def admit_projection(held):
    """Authenticate/select accepted fields, without re-proving the transform.

    The complete held body was pinned and canonically decoded before this call.
    Unselected scientific values remain authenticated inherited premises.
    """
    fields(held, HELD_TOP, 'RI96 top')
    for key, expected in {'schema': 'ri93-frequency-band-proxy-v1',
            'phase': 'fixed_saved_application', 'status': 'all_gates_passed',
            'model': 'postulated_finite_circulant_from_empirical_psd',
            'method': HELD_METHOD, 'rows': ROWS, 'limitations': HELD_LIMITATIONS,
            'gates': gates(HELD_GATES)}.items():
        strict_equal(held[key], expected, 'RI96/' + key)
    fields(held['prior'], ('context', 'G', 'rho', 'scenarios', 'held_provenance', 'held_limitations'), 'held prior')
    strict_equal(held['prior']['context'], 'accepted_ri90_saved_output', 'prior context')
    prior_scenarios = items(held['prior']['scenarios'], 4, 'prior scenario inventory')
    row_records = []
    for name, record in zip(ROWS, items(held['row_proofs'], D, 'RI96 rows')):
        fields(record, ('row', 'alpha', 'initial_q256', 'input_identity', 'midpoint_modes', 'mode_identity'), 'held row')
        strict_equal(record['row'], name, 'held row order')
        # These extra row fields are authenticated, not an alpha/FFT derivation.
        identity(record['input_identity'], 'held source row identity')
        for pair in items(record['initial_q256'], 10961, 'held input Q256 inventory'):
            lo, hi = [hex_number(x) for x in items(pair, 2, 'initial Q256 interval')]
            demand(lo <= hi, 'ordered retained initial Q256 interval')
        strict_equal(value_pin(record['initial_q256']), record['input_identity'], 'original retained Q256 input identity')
        row_records.append({key: record[key] for key in ('row', 'alpha', 'midpoint_modes', 'mode_identity')})
    scenarios = []
    for name, row, prior in zip(SCENARIOS, items(held['scenarios'], 4, 'RI96 scenarios'), prior_scenarios):
        fields(row, HELD_SCENARIO, 'held full scenario')
        fields(prior, ('id', 'source_record'), 'held prior scenario')
        strict_equal(row['id'], name, 'held scenario order')
        strict_equal(prior['id'], name, 'prior scenario order')
        strict_equal(prior['source_record'], row['source_record'], 'unchanged PSD source in prior and scenario')
        fields(row['scalar_intersections'], ('diagonal', 'trace', 'diagonal_ratios', 'trace_ratio'), 'held intersections')
        selected = {key: row[key] for key in PROJECT_SCENARIO}
        selected['prior_trace'] = row['scalar_intersections']['trace']
        scenarios.append(selected)
    # Authenticate the original fixed 14-band partition. Its matrices and the
    # full DC-inclusive Parseval proof are inherited, not recomputed here.
    for index, band in enumerate(items(held['bands'], 14, 'held bands')):
        fields(band, ('index', 'first', 'last_exclusive', 'C', 'H'), 'held band')
        first = 1 << index
        strict_equal([band['index'], band['first'], band['last_exclusive']],
                     [index, first, min(2 * first, 8193)], 'fixed band interval')
    fields(held['midpoint_parseval'], ('center', 'error', 'contains_G'), 'inherited Parseval')
    strict_equal(held['midpoint_parseval']['contains_G'], True, 'inherited Parseval declared gate')
    return {'context': 'accepted_ri96_saved_output', 'held_identity': RI96,
            'rows': ROWS, 'row_proofs': row_records, 'scenarios': scenarios,
            'held_provenance_identity': value_pin(held['provenance']), 'held_limitations': HELD_LIMITATIONS}


def mode_reconstruction(rows, actual):
    """Separately written integer-numerator route, not either RI98 routine.

    With m=l+u, n=u-l, d=2Q, the exact component contributions are
      c=m*m/d^2; h_tau=n*(2*abs(m)+n)/d^2;
      h_alpha=alpha*((2*abs(m)+2*n)/d+alpha).
    The numerator sums for c/h_tau are accumulated before the single common
    denominator division per mode. The alpha term retains every row radius.
    """
    alphas = []
    row_evidence = []
    for name, row in zip(ROWS, items(rows, D, 'selected rows')):
        strict_equal(row['row'], name, 'selected row')
        alpha = rational(row['alpha'])
        demand(alpha >= 0, 'nonnegative coefficient alpha')
        alphas.append(alpha)
        values = items(row['midpoint_modes'], 8193, 'complete row modes')
        identity(row['mode_identity'], 'complete row mode identity')
        strict_equal(value_pin(values), row['mode_identity'], 'original midpoint rectangle bytes')
        for endpoint in (0, 8192):
            a, b, c, d = rectangle(values[endpoint])
            demand(c <= 0 <= d, 'retained endpoint imaginary rectangle contains zero')
        row_evidence.append({'row': name, 'alpha': row['alpha'], 'mode_identity': row['mode_identity'],
                             'dc_rectangle': values[0], 'nyquist_rectangle': values[-1]})
    items(actual, 8192, 'RI100 complete mode inventory')
    numbers, rebuilt = [], []
    denominator = 2 * Q
    denominator2 = denominator * denominator
    for k in range(1, 8193):
        center_numerator = tau_numerator = 0
        alpha_sum = Fraction(0)
        for row, alpha in zip(rows, alphas):
            a, b, c, d = rectangle(row['midpoint_modes'][k])
            active = [(a, b)] if k == 8192 else [(a, b), (c, d)]
            for lo, hi in active:
                midpoint = integer(lo + hi)
                radius = integer(hi - lo)
                center_numerator = integer(center_numerator + integer(midpoint * midpoint))
                tau_piece = integer(radius * integer(2 * abs(midpoint) + radius))
                tau_numerator = integer(tau_numerator + tau_piece)
                linear_alpha = bounded(Fraction(integer(2 * abs(midpoint) + 2 * radius), denominator))
                alpha_sum = plus(alpha_sum, times(alpha, plus(linear_alpha, alpha)))
        weight = 1 if k == 8192 else 2
        cterm = bounded(Fraction(integer(weight * center_numerator), denominator2))
        tterm = bounded(Fraction(integer(weight * tau_numerator), denominator2))
        aterm = times(Fraction(weight), alpha_sum)
        demand(min(cterm, tterm, aterm) >= 0, 'all independently reconstructed mode terms nonnegative')
        expected = encoded({'k': k, 'pair_weight': weight, 'c': cterm, 'h_tau': tterm, 'h_alpha': aterm})
        fields(actual[k - 1], MODE_FIELDS, 'saved mode')
        for key in ('c', 'h_tau', 'h_alpha'):
            rational(actual[k - 1][key])
        strict_equal(actual[k - 1], expected, 'independent complete mode ' + str(k))
        rebuilt.append(expected)
        numbers.append((cterm, tterm, aterm))
    return numbers, rebuilt, row_evidence


def eigenvalues(record):
    fields(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'source PSD')
    strict_equal(record['dtype'], '<f8', 'PSD dtype')
    strict_equal(record['shape'], [8193], 'PSD shape')
    demand(type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None,
           'PSD original bit digest')
    h = hashlib.sha256()
    output = []
    for index, text in enumerate(items(record['values_hex'], 8193, 'complete PSD values')):
        demand(type(text) is str, 'binary64 hexadecimal string')
        try:
            value = float.fromhex(text)
        except (ValueError, OverflowError) as error:
            raise AuditFailure('invalid binary64 PSD') from error
        demand(math.isfinite(value) and value >= 0 and value.hex() == text,
               'canonical finite nonnegative PSD, including original signed zero')
        h.update(struct.pack('<d', value))
        # as_integer_ratio preserves the original finite dyadic value exactly.
        n, d = value.as_integer_ratio()
        output.append(bounded(Fraction(integer(n * (FS if index in (0, 8192) else FS // 2)), d)))
    strict_equal(h.hexdigest(), record['sha256'], 'original little-endian PSD bit identity')
    return output


def matrix_trace(value):
    matrix = [[rational(cell) for cell in items(row, D, 'matrix row')]
              for row in items(value, D, 'matrix')]
    demand(all(matrix[i][j] == matrix[j][i] for i in range(D) for j in range(i)),
           'inherited symmetric matrix')
    return sum_exact(matrix[i][i] for i in range(D))


def quotient(numerator, denominator, reason):
    if denominator > 0:
        return {'value': encoded(bounded(numerator / denominator)), 'undefined_reason': None}
    return {'value': None, 'undefined_reason': reason}


def scenario_reconstruction(held, terms):
    lam = eigenvalues(held['source_record'])
    sums = []
    for coordinate in range(3):
        sums.append(sum_exact(times(lam[k], terms[k - 1][coordinate]) for k in range(1, 8193)))
    center, etau, ealpha = sums
    error = plus(etau, ealpha)
    raw = (plus(center, -error), plus(center, error))
    trace_minus, trace_plus = matrix_trace(held['C_minus']), matrix_trace(held['C_plus'])
    dm, dp = rational(held['delta_minus']), rational(held['delta_plus'])
    demand(dm >= 0 and dp >= 0, 'nonnegative inherited matrix margins')
    band = scalar_interval(held['trace'])
    prior = scalar_interval(held['prior_trace'])
    strict_equal(band, (plus(trace_minus, -times(Fraction(D), dm)),
                        plus(trace_plus, times(Fraction(D), dp))), 'inherited raw band trace')
    demand(band[0] <= prior[0] <= prior[1] <= band[1], 'prior scalar intersection inside raw band')
    spread = Fraction(0)
    extrema_rebuilt = []
    for index, original in enumerate(items(held['band_extrema'], 14, 'complete extrema')):
        first, stop = 1 << index, min(1 << (index + 1), 8193)
        minimum, maximum = min(lam[first:stop]), max(lam[first:stop])
        extrema = encoded({'index': index, 'ell': minimum, 'u': maximum,
                  'minimum_indices': [k for k in range(first, stop) if lam[k] == minimum],
                  'maximum_indices': [k for k in range(first, stop) if lam[k] == maximum]})
        strict_equal(original, extrema, 'all extrema/ties in band ' + str(index))
        contribution = times(plus(maximum, -minimum), sum_exact(terms[k - 1][0] for k in range(first, stop)))
        spread = plus(spread, contribution)
        extrema_rebuilt.append(extrema)
    strict_equal(spread, plus(trace_plus, -trace_minus), 'spread equals trace Cplus minus Cminus')
    margin = times(Fraction(D), plus(dm, dp))
    band_width = plus(spread, margin)
    strict_equal(band_width, plus(band[1], -band[0]), 'raw band width decomposition')
    demand(raw[1] <= band[1], 'direct upper no larger than inherited band upper')
    final = (max(raw[0], prior[0]), min(raw[1], prior[1]))
    demand(final[0] <= final[1], 'nonempty scalar intersection')
    widths = {name: plus(pair[1], -pair[0]) for name, pair in (('raw', raw), ('ri96', prior), ('final', final))}
    ratios = {'ri96_over_final_width': quotient(widths['ri96'], widths['final'], 'zero_width_denominator'),
              'ri96_over_raw_width': quotient(widths['ri96'], widths['raw'], 'zero_width_denominator'),
              'raw_upper_over_lower': quotient(raw[1], raw[0], 'nonpositive_lower_endpoint'),
              'ri96_upper_over_lower': quotient(prior[1], prior[0], 'nonpositive_lower_endpoint'),
              'final_upper_over_lower': quotient(final[1], final[0], 'nonpositive_lower_endpoint')}
    result = encoded({'id': held['id'], 'source_identity': value_pin(held['source_record']),
                      'center': center, 'error_tau': etau, 'error_alpha': ealpha, 'error': error,
                      'raw': raw, 'ri96_raw_band': band, 'ri96_prior': prior, 'final': final,
                      'band_spread': spread, 'band_margin': margin, 'band_width': band_width,
                      'widths': widths, 'equalities': {'final_equals_ri96': final == prior,
                                                     'final_equals_raw': final == raw},
                      'ratios': ratios, 'direct_upper_le_band_upper': True})
    evidence = {'id': held['id'], 'eigenvalues': value_pin(encoded(lam)),
                'extrema': value_pin(extrema_rebuilt), 'mode_weighted_sums': encoded(sums),
                'twice_error_tau': encoded(times(Fraction(2), etau)),
                'twice_error_alpha': encoded(times(Fraction(2), ealpha)),
                'spread_from_matrices': encoded(plus(trace_plus, -trace_minus))}
    return result, evidence


def provenance_check(value):
    fields(value, ('sources', 'input', 'acceptance', 'runtime'), 'actual provenance')
    for key in ('sources', 'input', 'runtime'):
        strict_equal(value[key], FIXED_PROVENANCE[key], 'unchanged prospective provenance/' + key)
    fields(value['acceptance'], ('design', 'ri96', 'qualification', 'custody'), 'acceptance')
    for key in ('design', 'ri96', 'qualification'):
        strict_equal(value['acceptance'][key], FIXED_PROVENANCE['acceptance'][key], 'accepted predecessor/' + key)
    identity(value['acceptance']['custody'], 'genuine pre-execution input custody')


def reconstruct(ri96_body, result_body, result_identity, expected_provenance):
    """Fixed complete two-body interface; neither body decoded before both bind.

    This scientific function alone is not execution authorization. Main adds
    concrete source/descriptor/completed-custody gates before reaching it.
    """
    strict_equal(body_pin(ri96_body), RI96, 'whole fixed RI96 before either scientific parse')
    identity(result_identity, 'real completed result identity')
    strict_equal(body_pin(result_body), result_identity, 'whole actual RI100 before either scientific parse')
    provenance_check(expected_provenance)
    held = whole_json(ri96_body)
    projection = admit_projection(held)
    del held
    actual = whole_json(result_body)
    fields(actual, TOP_FIELDS, 'RI100 top')
    expected_metadata = {'schema': 'ri98-mode-weighted-trace-v1', 'phase': 'fixed_saved_application',
                         'status': 'all_declared_checks_passed', 'method': METHOD,
                         'provenance': expected_provenance, 'checks': gates(GATES),
                         'inherited_premises': {'labels': PREMISES, 'projection_identity': value_pin(projection),
                            'held_provenance_identity': projection['held_provenance_identity'],
                            'held_limitations': HELD_LIMITATIONS}, 'limitations': LIMITATIONS}
    for key, expected in expected_metadata.items():
        strict_equal(actual[key], expected, 'RI100 fixed metadata/' + key)
    terms, expected_modes, rows = mode_reconstruction(projection['row_proofs'], actual['mode_terms'])
    expected_scenarios, scalar_evidence = [], []
    for name, held_scenario, saved in zip(SCENARIOS, projection['scenarios'], items(actual['scenarios'], 4, 'RI100 scenarios')):
        strict_equal(held_scenario['id'], name, 'scenario order')
        fields(saved, SCALAR_FIELDS, 'saved scalar scenario')
        expected, evidence = scenario_reconstruction(held_scenario, terms)
        strict_equal(saved, expected, 'complete independently derived scenario ' + name)
        expected_scenarios.append(expected)
        scalar_evidence.append(evidence)
    expected = dict(expected_metadata, mode_terms=expected_modes, scenarios=expected_scenarios)
    strict_equal(value_pin(expected), result_identity, 'whole independently reconstructed RESULT identity')
    sections = {name: value_pin(expected[name]) for name in TOP_FIELDS}
    strict_equal(body_pin(ri96_body), RI96, 'held immutable bytes after arithmetic')
    strict_equal(body_pin(result_body), result_identity, 'actual immutable bytes after arithmetic')
    return {'status': 'all_saved_scalar_fields_independently_match',
            'reconstructed_result_identity': value_pin(expected), 'sections': sections,
            'counts': {'rows': 8, 'retained_rectangles': 65544, 'active_real_components': 131064,
                       'mode_records': 8192, 'mode_scalars': 24576, 'scenarios': 4,
                       'psd_bins': 32772, 'eigenvalues': 32772, 'band_extrema': 56,
                       'ratios': 20, 'top_sections': 10},
            'row_operand_identities': rows, 'scenario_evidence': scalar_evidence,
            'reconstructed_scenarios': expected_scenarios,
            'inherited_premises': PREMISES, 'limitations': LIMITATIONS,
            'scope': 'Exact scalar arithmetic and complete closed RI100 result; inherited RI96 transform, row, covariance and execution validity are not re-proved.'}

# Documentary execution admission is separate from the scientific arithmetic.
# It consumes a future genuine root bridge. No process is created here.
APPLICATION_ROOT = '/Volumes/AI_DATA/development/det-review-evidence/ri100-execution/application-preparation-uhq7i_49'
SOURCE_TEMPLATE = {'path': APPLICATION_ROOT + '/MANIFEST.source-only-template.json',
 'bytes': 65470, 'sha256': '3f0ea0d4953c5e52564dbe8637e12759d58d487c037dcc890356eddd3730b3b0'}
SOURCE_DECISION = {'path': '/Volumes/AI_DATA/development/det-review-evidence/ri99-root-review-osb8owly/RI100_ROOT_SOURCE_ADJUDICATION.json',
 'bytes': 3102, 'sha256': '5695a96d24db24e17df032670cf175b6e848c34dc60883b73600250e9285464c'}
LIMITS = {'wall_seconds': 180, 'rss_kib': 524288, 'target_poll_seconds': 0.025,
          'maximum_sample_gap_seconds': 0.1, 'ps_timeout_seconds': 0.05}
VALIDATION = {'status': 'all_fields_independently_match', 'rows': 8, 'modes': 8192, 'scenarios': 4}
BRIDGE_PREMISES = [
 'The original genuine normal and optimized outer completions, serial authorizations and complete raw monitor/custody review are accepted; arithmetic remains pending.',
 'RI96 full result, qualified recursive transform validation and completed independent arithmetic/custody acceptance remain inherited premises.',
 'Root owns the exact source/runtime closure and single later audit admission; this bridge does not itself authorize an auditor launch.'
]


def file_reference(value, *, empty=False):
    fields(value, ('path', 'bytes', 'sha256'), 'file reference')
    demand(type(value['path']) is str and Path(value['path']).is_absolute(), 'absolute file reference')
    size = value['bytes']
    demand(type(size) is int and (size >= 0 if empty else size > 0), 'concrete file size')
    demand(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
           'concrete file SHA256')
    return value


def short_pin(reference):
    return {'bytes': reference['bytes'], 'sha256': reference['sha256']}


class Custody:
    """Opaque stable-file reads and a final complete rehash, never execution."""
    def __init__(self):
        self.seen = {}

    def inspect(self, reference, *, capture=False):
        file_reference(reference, empty=True)
        path = Path(reference['path'])
        demand(path == path.resolve(), 'canonical nonsymlink dependency path')
        before = path.lstat()
        demand(stat.S_ISREG(before.st_mode), 'regular nonsymlink dependency')
        state = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
        digest, length, fragments = hashlib.sha256(), 0, []
        with path.open('rb') as stream:
            opened = os.fstat(stream.fileno())
            demand(state(opened) == state(before), 'dependency changed on open')
            while True:
                fragment = stream.read(1024 * 1024)
                if not fragment:
                    break
                digest.update(fragment)
                length += len(fragment)
                if capture:
                    fragments.append(fragment)
            after = os.fstat(stream.fileno())
        demand(state(before) == state(after) == state(path.lstat()), 'dependency changed during read')
        strict_equal({'bytes': length, 'sha256': digest.hexdigest()}, short_pin(reference), 'opaque file identity')
        item = {'reference': dict(reference), 'stat': list(state(before))}
        previous = self.seen.get(str(path))
        if previous is not None:
            strict_equal(previous, item, 'previously admitted dependency stability')
        self.seen[str(path)] = item
        return b''.join(fragments) if capture else short_pin(reference)

    def document(self, reference):
        return whole_json(self.inspect(reference, capture=True), scientific=False)

    def finish(self):
        saved = list(self.seen.values())
        for record in saved:
            self.inspect(record['reference'])
        return {'files': len(saved), 'identity': value_pin(sorted(saved, key=lambda x: x['reference']['path']))}


def literal_binding(named, custody):
    path = Path(named)
    demand(path.is_absolute(), 'absolute named interpreter')
    pending, current, links = list(path.parts[1:]), Path('/'), []
    while pending:
        part = pending.pop(0)
        if part in ('', '.'):
            continue
        if part == '..':
            current = current.parent
            continue
        candidate = current / part
        info = candidate.lstat()
        if stat.S_ISLNK(info.st_mode):
            demand(len(links) < 64, 'bounded interpreter link traversal')
            text = os.readlink(candidate)
            links.append({'path': str(candidate), 'target': text})
            target = Path(text)
            if target.is_absolute():
                current = Path('/')
                pending = list(target.parts[1:]) + pending
            else:
                pending = list(target.parts) + pending
        else:
            current = candidate
    return str(current), links


def complete_closure(freeze, custody):
    observed = []
    for row in items(freeze['sources'], 49, 'fixed source pairs'):
        fields(row, ('relative', 'original', 'copy', 'pin'), 'source pair')
        identity(row['pin'])
        for name in ('original', 'copy'):
            ref = {'path': row[name], **row['pin']}
            custody.inspect(ref)
            observed.append(ref)
    for row in items(freeze['helpers'], 3, 'fixed helpers'):
        fields(row, ('path', 'pin'), 'helper')
        ref = {'path': row['path'], **row['pin']}
        custody.inspect(ref)
        observed.append(ref)
    for ref in items(freeze['history'], 79, 'fixed historical records'):
        custody.inspect(ref)
    for ref in freeze['evidence'].values():
        custody.inspect(ref)
    runtime_ref = {'path': freeze['runtime_inventory']['path'], **freeze['runtime_inventory']['pin']}
    inventory = custody.document(runtime_ref)
    runtime_files = items(inventory['files'], 3925, 'complete qualified runtime files')
    discovered = set(inventory['extra_files'])
    for root in inventory['roots']:
        directory = Path(root)
        demand(directory == directory.resolve() and directory.is_dir(), 'runtime root identity')
        for parent, directories, names in os.walk(directory):
            for name in directories:
                demand(not (Path(parent) / name).is_symlink(), 'no extra runtime directory symlink')
            discovered.update(str(Path(parent) / name) for name in names)
    strict_equal(sorted(discovered), [row['path'] for row in runtime_files], 'complete runtime path inventory including pyc files')
    for ref in runtime_files:
        custody.inspect(ref)
    demand(sum(row['bytes'] for row in runtime_files) == 152961716, 'full qualified runtime byte count')
    binding = freeze['interpreter']
    resolved, links = literal_binding(binding['named_path'], custody)
    strict_equal(resolved, binding['resolved_path'], 'resolved interpreter')
    strict_equal(links, binding['symlink_chain'], 'every literal interpreter link')
    custody.inspect({'path': resolved, **binding['target']})
    runtime = {'interpreter': binding, 'runtime_files_count': 3925,
               'runtime_files_identity': value_pin(runtime_files),
               'inventory_pin': freeze['runtime_inventory']['pin']}
    return observed, runtime


def finite_time(value):
    demand(type(value) in (float, int) and math.isfinite(value) and value >= 0,
           'finite nonnegative elapsed time')
    return value


def reconcile_samples(receipt):
    """Read every real ps attempt; no monitor process or new measurement."""
    attempts, saved = receipt['monitor_attempts'], receipt['samples']
    demand(type(attempts) is list and attempts and type(saved) is list and saved, 'actual raw monitoring evidence')
    elapsed = finite_time(receipt['child_elapsed_seconds'])
    demand(elapsed <= 180, 'unchanged child wall limit')
    rebuilt, previous, last_attempt = [], 0, 0
    terminal = 0
    for index, record in enumerate(attempts):
        fields(record, ('elapsed_seconds', 'returncode', 'stdout', 'stderr'), 'successful-attempt record')
        stamp = finite_time(record['elapsed_seconds'])
        demand(last_attempt <= stamp <= elapsed, 'ordered raw attempt timestamps')
        last_attempt = stamp
        demand(type(record['returncode']) is int and type(record['stdout']) is str and
               type(record['stderr']) is str, 'raw ps types')
        text = record['stdout'].strip()
        if record['returncode'] != 0 or not text.isdigit():
            # The reviewed caller allows one terminal observation after poll
            # sees the child exit. Its genuine completion remains root-bound.
            demand(index == len(attempts) - 1, 'only final unavailable ps observation')
            terminal += 1
            continue
        rss = int(text)
        gap = stamp - previous
        demand(rss <= 524288 and 0 <= gap <= 0.1, 'unchanged RSS and sample-gap gates')
        rebuilt.append({'elapsed_seconds': stamp, 'rss_kib': rss, 'gap_seconds': gap})
        previous = stamp
    strict_equal(saved, rebuilt, 'every parsed sample and exact raw-derived gap')
    strict_equal(receipt['peak_sampled_rss_kib'], max(row['rss_kib'] for row in rebuilt), 'sampled peak')
    final_gap = elapsed - previous
    strict_equal(receipt['final_sample_to_reap_gap_seconds'], final_gap, 'final sample-to-reap gap')
    demand(0 <= final_gap <= 0.1 and receipt['final_sample_gap_passed'] is True, 'unchanged final gap gate')
    return {'raw_attempts': len(attempts), 'samples': len(rebuilt), 'terminal_attempts': terminal,
            'peak_sampled_rss_kib': receipt['peak_sampled_rss_kib'], 'child_seconds': elapsed,
            'maximum_gap_seconds': max(row['gap_seconds'] for row in rebuilt), 'final_gap_seconds': final_gap}


def completed_modes(bridge, freeze, freeze_pin, custody, sources, runtime):
    fields(bridge['modes'], ('normal', 'optimized'), 'both actual modes')
    summaries = {}
    expected_input = freeze['provenance_template']['input']
    input_states = []
    for operand in items(freeze['inputs'], 1, 'single fixed application input'):
        paths = []
        for field in ('original', 'copy'):
            ref = {'path': operand[field], **operand['pin']}
            custody.inspect(ref)
            info = Path(ref['path']).lstat()
            paths.append({'field': field, 'path': ref['path'], 'pin': operand['pin'],
                          'metadata': {'device': info.st_dev, 'inode': info.st_ino,
                          'size': info.st_size, 'mtime_ns': info.st_mtime_ns, 'ctime_ns': info.st_ctime_ns}})
        input_states.append({'role': operand['role'], 'paths': paths})
    expected_acceptance = {'evidence': freeze['evidence'], 'history': freeze['history'],
                          'source_count': 49, 'inputs': input_states,
                          'provenance_template': freeze['provenance_template'],
                          'boundary': 'Scalar exact aggregation on the accepted RI96 body; upstream transform and covariance premises inherited, actual application success not presumed.'}
    for mode in ('normal', 'optimized'):
        entry = bridge['modes'][mode]
        fields(entry, ('authorization', 'outer_completion', 'outer_exit_code', 'receipt',
                      'worker_receipt', 'custody', 'attempt', 'stdout', 'stderr'), 'mode bridge')
        strict_equal(entry['outer_exit_code'], 0, 'genuine root-attested outer exit')
        # Documentary outer records may preserve noncanonical historical format.
        # The exact root bridge authenticates their actual tool occurrence.
        custody.inspect(entry['authorization'])
        custody.inspect(entry['outer_completion'])
        run = freeze['runs'][mode]
        aliases = {'receipt': 'receipt', 'worker_receipt': 'worker_receipt', 'custody': 'custody',
                   'attempt': 'claim', 'stdout': 'stdout', 'stderr': 'stderr'}
        for name, key in aliases.items():
            strict_equal(entry[name]['path'], run[key], 'original actual mode path/' + name)
            custody.inspect(entry[name])
        receipt = custody.document(entry['receipt'])
        worker = custody.document(entry['worker_receipt'])
        saved_custody = custody.document(entry['custody'])
        attempt = custody.document(entry['attempt'])
        for record, schema in ((receipt, 'ri100-application-supervisor-receipt-v1'),
                               (worker, 'ri100-application-worker-receipt-v1'),
                               (saved_custody, 'ri100-application-custody-v1')):
            strict_equal(record['schema'], schema, 'actual receipt schema')
            strict_equal(record['phase'], 'fixed_saved_application', 'actual phase')
            strict_equal(record['mode'], mode, 'actual mode')
        command = [freeze['interpreter']['named_path'], '-I', '-B']
        if mode == 'optimized':
            command += ['-O']
        command += [APPLICATION_ROOT + '/worker.py', APPLICATION_ROOT + '/AUTHORIZED_FREEZE.json', mode]
        strict_equal(run['command'], command, 'fixed actual worker argv')
        strict_equal(receipt['command'], command, 'receipt command')
        strict_equal(receipt['environment'], freeze['environment'], 'receipt environment')
        strict_equal(receipt['limits'], LIMITS, 'receipt resource gates')
        strict_equal(attempt, {'freeze': freeze_pin, 'phase': 'fixed_saved_application', 'mode': mode, 'command': command}, 'exclusive genuine attempt')
        for record in (receipt, worker):
            strict_equal(record['freeze'], freeze_pin, 'actual freeze')
            strict_equal(record['source_before'], sources, 'complete source before')
            strict_equal(record['source_after'], sources, 'complete source after')
        strict_equal(receipt['success'], True, 'actual parent success')
        strict_equal(receipt['child_exit_code'], 0, 'actual child exit')
        strict_equal(receipt['stop_reason'], None, 'no supervisory stop')
        strict_equal(worker['exit_code'], 0, 'actual worker exit')
        strict_equal(worker['error'], None, 'actual worker error absent')
        demand(all(key not in record for record in (receipt, worker) for key in
                   ('postcheck_error', 'termination_error')), 'post-run failure absent')
        for key in ('runtime_before', 'runtime_after'):
            strict_equal(receipt[key], runtime, 'parent complete runtime bytes')
            strict_equal(worker[key], freeze['expected_runtime'], 'worker genuine full runtime')
        for key in ('runtime_bytes_before', 'runtime_bytes_after'):
            strict_equal(worker[key], runtime, 'worker complete runtime bytes')
        acceptance = receipt['acceptance_before']
        strict_equal(acceptance, expected_acceptance, 'complete acceptance and current original/copy stat binding')
        for value in (receipt['acceptance_after'], worker['acceptance_before'], worker['acceptance_after']):
            strict_equal(value, acceptance, 'all actual pre/post acceptance')
        strict_equal(worker['inputs_before'], acceptance['inputs'], 'actual original/copy input states')
        strict_equal(worker['inputs_after'], acceptance['inputs'], 'unchanged original/copy input states')
        for key in ('captured_ri96_before', 'captured_ri96_after'):
            strict_equal(worker[key], expected_input, 'complete captured scientific body')
        strict_equal(worker['saved_result_validation'], VALIDATION, 'genuine independent validator completion')
        strict_equal(worker['full_validator_passed'], True, 'full saved reload validator passed')
        fields(saved_custody, ('schema', 'phase', 'mode', 'context', 'report', 'provenance',
                              'genuine_runtime_fingerprint', 'inputs', 'captured_ri96',
                              'saved_result_validation', 'full_validator_passed', 'claim'), 'actual CUSTODY')
        strict_equal(saved_custody['report'], entry['stdout'], 'actual complete result binding')
        strict_equal(saved_custody['provenance'], bridge['expected_provenance'], 'actual saved provenance')
        strict_equal(saved_custody['genuine_runtime_fingerprint'], value_pin(freeze['expected_runtime']), 'genuine runtime fingerprint')
        strict_equal(saved_custody['inputs'], acceptance['inputs'], 'custody input states')
        strict_equal(saved_custody['captured_ri96'], RI96, 'custody whole RI96')
        strict_equal(saved_custody['saved_result_validation'], VALIDATION, 'custody validator completion')
        strict_equal(saved_custody['full_validator_passed'], True, 'custody full validator')
        strict_equal(saved_custody['context'], freeze['context'], 'actual fixed operation context')
        strict_equal(saved_custody['claim'], freeze['claim'], 'unchanged bounded scientific claim')
        strict_equal(worker['operation'], {'result': entry['stdout'], 'custody': entry['custody'], 'claim': freeze['claim']}, 'worker operation bindings')
        strict_equal(receipt['outputs'], {k: short_pin(entry[k]) for k in ('stdout', 'stderr', 'worker_receipt', 'custody')}, 'all actual outputs')
        strict_equal(short_pin(entry['stderr']), {'bytes': 0, 'sha256': hashlib.sha256(b'').hexdigest()}, 'empty stderr')
        expected_custody = {'custody_pin': short_pin(entry['custody']), 'report_pin': short_pin(entry['stdout']),
                            'provenance': bridge['expected_provenance'], 'inputs': acceptance['inputs'],
                            'captured_ri96': RI96, 'saved_result_validation': VALIDATION, 'full_validator_passed': True}
        strict_equal(receipt['verified_custody'], expected_custody, 'parent verified custody')
        summaries[mode] = reconcile_samples(receipt)
    return summaries


def admission(descriptor, custody):
    fields(descriptor, ('schema', 'status', 'auditor', 'contract', 'source_reviews',
                       'completed_custody', 'ri96', 'ri100', 'ri100_optimized',
                       'expected_provenance', 'output'), 'audit descriptor')
    strict_equal(descriptor['schema'], 'ri100-independent-scalar-audit-input-v1', 'descriptor schema')
    strict_equal(descriptor['status'], 'issued_for_separately_authorized_saved_audit', 'concrete descriptor status')
    demand(type(descriptor['source_reviews']) is list and len(descriptor['source_reviews']) >= 2, 'separate complete source reviews')
    for ref in descriptor['source_reviews']:
        custody.inspect(ref)
    for key in ('auditor', 'contract', 'completed_custody', 'ri96', 'ri100', 'ri100_optimized'):
        file_reference(descriptor[key])
    strict_equal(descriptor['auditor']['path'], str(Path(__file__).resolve()), 'executed captured auditor source')
    custody.inspect(descriptor['auditor'])
    custody.inspect(descriptor['contract'])
    bridge = custody.document(descriptor['completed_custody'])
    fields(bridge, ('schema', 'status', 'arithmetic_accepted', 'producer_freeze', 'source_acceptance',
                   'input_custody', 'qualification', 'normal_acceptance', 'independent_custody_review',
                   'raw_monitor_review', 'modes', 'full_result_equality', 'expected_provenance',
                   'inherited_premises'), 'completed root bridge')
    strict_equal(bridge['schema'], 'ri100-root-completed-custody-bridge-v1', 'root bridge schema')
    strict_equal(bridge['status'], 'accepted_both_mode_custody_pending_independent_arithmetic', 'custody only acceptance')
    strict_equal(bridge['arithmetic_accepted'], False, 'no invented prior arithmetic acceptance')
    strict_equal(bridge['inherited_premises'], BRIDGE_PREMISES, 'root inherited evidence boundary')
    strict_equal(bridge['source_acceptance'], SOURCE_DECISION, 'complete root source acceptance')
    for key in ('source_acceptance', 'input_custody', 'qualification', 'normal_acceptance',
                'independent_custody_review', 'raw_monitor_review'):
        custody.inspect(bridge[key])
    freeze = custody.document(bridge['producer_freeze'])
    template = custody.document(SOURCE_TEMPLATE)
    template['status'] = 'authorized_fixed_saved_application'
    template['evidence']['input_custody'] = bridge['input_custody']
    template['provenance_template']['acceptance']['custody'] = short_pin(bridge['input_custody'])
    strict_equal(freeze, template, 'only declared pre-execution custody and status substitutions')
    strict_equal(bridge['producer_freeze']['path'], APPLICATION_ROOT + '/AUTHORIZED_FREEZE.json', 'original application freeze')
    strict_equal(freeze['limits'], LIMITS, 'unchanged production resource envelope')
    strict_equal(bridge['qualification'], freeze['evidence']['qualification_adjudication'], 'genuine prior qualification')
    input_custody = custody.document(bridge['input_custody'])
    strict_equal(input_custody['schema'], 'ri100-root-input-custody-adjudication-v1', 'pre-execution input record schema')
    strict_equal(input_custody['status'], 'accepted_fixed_upstream_input_for_prospective_application', 'input admission scope')
    strict_equal(input_custody['actual_application_executed'], False, 'historical input admission not rewritten')
    strict_equal(input_custody['inputs'], freeze['inputs'], 'root admitted sole numerical input')
    strict_equal(bridge['expected_provenance'], freeze['provenance_template'], 'root provenance matches frozen caller')
    strict_equal(descriptor['expected_provenance'], bridge['expected_provenance'], 'descriptor exact actual provenance')
    provenance_check(descriptor['expected_provenance'])
    fields(bridge['full_result_equality'], ('byte_equal', 'common_identity'), 'whole mode equality')
    strict_equal(bridge['full_result_equality']['byte_equal'], True, 'root completed whole-byte equality')
    common = bridge['full_result_equality']['common_identity']
    identity(common)
    strict_equal(short_pin(descriptor['ri96']), RI96, 'sole original accepted scientific input')
    strict_equal(descriptor['ri96']['path'], freeze['inputs'][0]['copy'], 'original fixed captured RI96 path')
    strict_equal(short_pin(descriptor['ri100']), common, 'actual completed normal identity')
    strict_equal(short_pin(descriptor['ri100_optimized']), common, 'actual completed optimized identity')
    for key, mode in (('ri100', 'normal'), ('ri100_optimized', 'optimized')):
        strict_equal(descriptor[key], bridge['modes'][mode]['stdout'], 'exact genuine scientific output')
    sources, runtime = complete_closure(freeze, custody)
    mode_summary = completed_modes(bridge, freeze, short_pin(bridge['producer_freeze']), custody, sources, runtime)
    output = descriptor['output']
    demand(type(output) is str and Path(output).is_absolute(), 'exclusive absolute audit output')
    target = Path(output)
    demand(target.parent == target.parent.resolve() and target.parent.is_dir(), 'existing canonical audit output parent')
    demand(not target.exists() and not target.is_symlink(), 'audit output never overwrites prior evidence')
    demand(str(target) not in custody.seen, 'audit output cannot alias admitted input path')
    return mode_summary, freeze, common


def main():
    demand(len(sys.argv) == 2, 'one frozen descriptor argument')
    demand(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0,
           'one separately supervised isolated normal audit, no unasked optimized replay')
    descriptor_path = Path(sys.argv[1])
    demand(descriptor_path.is_absolute() and descriptor_path == descriptor_path.resolve(), 'canonical descriptor path')
    # The outer reviewed adapter pins the descriptor before loading these bytes.
    # Locally retain its immutable body and verify it again on completion.
    descriptor_body = descriptor_path.read_bytes()
    descriptor_ref = {'path': str(descriptor_path), **body_pin(descriptor_body)}
    custody = Custody()
    custody.inspect(descriptor_ref)
    descriptor = whole_json(descriptor_body, scientific=False)
    mode_summary, freeze, result_identity = admission(descriptor, custody)
    interpreter = freeze['interpreter']
    strict_equal(str(Path(sys.executable)), interpreter['named_path'], 'qualified named interpreter for audit')
    # BOTH complete numerical bodies are captured and byte-bound before either
    # scientific parse. Also compare the genuine optimized stream byte-for-byte.
    ri96_body = custody.inspect(descriptor['ri96'], capture=True)
    result_body = custody.inspect(descriptor['ri100'], capture=True)
    strict_equal(body_pin(ri96_body), RI96, 'complete fixed input captured')
    strict_equal(body_pin(result_body), result_identity, 'complete actual output captured')
    custody.inspect(descriptor['ri100_optimized'])
    with Path(descriptor['ri100_optimized']['path']).open('rb') as stream:
        offset = 0
        while True:
            chunk = stream.read(1024 * 1024)
            if not chunk:
                break
            demand(chunk == result_body[offset:offset + len(chunk)], 'complete normal/optimized bytes')
            offset += len(chunk)
    demand(offset == len(result_body), 'complete equal output stream length')
    custody.inspect(descriptor['ri100_optimized'])
    arithmetic = reconstruct(ri96_body, result_body, result_identity, descriptor['expected_provenance'])
    del ri96_body, result_body
    complete_closure(freeze, custody)
    resolved, links = literal_binding(interpreter['named_path'], custody)
    strict_equal(resolved, interpreter['resolved_path'], 'interpreter target stable after arithmetic')
    strict_equal(links, interpreter['symlink_chain'], 'literal runtime links stable after arithmetic')
    final_custody = custody.finish()
    result = {'schema': 'ri100-independent-saved-scalar-audit-v1',
              'status': 'all_saved_scalar_fields_independently_match',
              'descriptor': descriptor_ref, 'auditor': descriptor['auditor'], 'contract': descriptor['contract'],
              'inputs': {'ri96': descriptor['ri96'], 'normal': descriptor['ri100'], 'optimized': descriptor['ri100_optimized']},
              'completed_custody_bridge': descriptor['completed_custody'], 'mode_custody': mode_summary,
              'whole_output_byte_equality': True, 'arithmetic': arithmetic, 'final_custody': final_custody,
              'own_execution_custody': 'Not supplied by this report; separately reviewed supervisor receipt, genuine outer exit and post-run review remain required.'}
    with Path(descriptor['output']).open('xb') as stream:
        for piece in parts(result):
            stream.write(piece)
        stream.flush()
        os.fsync(stream.fileno())
    for piece in parts(result):
        sys.stdout.buffer.write(piece)
    sys.stdout.buffer.flush()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
