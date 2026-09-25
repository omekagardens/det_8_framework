"""RI87 source-only exact finite colored-proxy consumer.

Pure stdlib APIs; no files or scientific predecessors are opened/imported here.
run_saved binds both published byte bodies before parsing either. A separately
reviewed captured-source caller must admit source/runtime/acceptance/path custody.
No function authorizes an execution, estimates true noise, or computes a score.
"""
from fractions import Fraction as F
import hashlib
import json
import math
import re
import struct

BITS = 262144
M, FS, N, L, T, DIM = 16384, 4096, 2769, 4096, 10961, 8
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
SCENARIOS = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
RHO_LIMIT = F(1, 10**12)
DESIGN_PIN = {'bytes': 32470, 'sha256': '2a00cac0017f0b749ed958efef4d623143c97e33ba36c60454a65ef9069dc04e'}
RI83_PIN = {'bytes': 38952074, 'sha256': 'e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f'}
RI73_PIN = {'bytes': 11180937, 'sha256': '3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe'}
RI73_SOURCE_PIN = {'bytes': 68018, 'sha256': '574f5f1b8900221a47bc30ea62e6bed378a8fd1c8b4aa904e0549ade8ceb2887'}
RI78_PIN = {'bytes': 24390, 'sha256': '3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce'}
RI37_PIN = {'bytes': 31096, 'sha256': 'a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80'}
RECOVERY_PIN = {'bytes': 16293, 'sha256': 'be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0'}
RI80_PIN = {'bytes': 63464716, 'sha256': 'f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d'}
INPUTS = (
    ('H1', 'H-H1_LOSC_4_V2-1126259446-32.hdf5', 1040592, '50441a42c13fc1f14e5c4ea5527f1515', '6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6'),
    ('L1', 'L-L1_LOSC_4_V2-1126259446-32.hdf5', 1007420, '361ae6a040a9fef7897b1e0124d5b0a1', '56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189'),
)
CERT_CHECKS = ('G_symmetry', 'H_symmetry_nonnegative', 'positive_LDL', 'LDL_reconstruction',
               'two_sided_inverse', 'delta_identity', 'gamma_identity', 'rho_identity',
               'rho_mathematical', 'rho_accuracy')
GATE_IDS = ('admission:metadata', 'admission:certificate', 'scenario:H1:left',
            'scenario:H1:right', 'scenario:L1:left', 'scenario:L1:right', 'completion:algebra')
LIMITATIONS = [
    'The four saved Welch PSDs are empirical finite statistics, not established physical noise covariance.',
    'Each finite four-second circulant covariance is an explicit separate proxy postulate with long-lag wraparound.',
    'Public prior-access development inputs are not blind or protected validation; off-event names an exclusion only.',
    'Nominal V2/C02 strain has blank literal Yunits; L1 NO_CW_HW_INJ is clear throughout all 32 seconds.',
    'No stationarity, signal-free interval, Gaussianity, detector independence or calibrated covariance is established.',
    'Loewner endpoints bound quadratic forms; only diagonal and trace pairs are scalar variance intervals.',
    'A zero non-DC lower eigenvalue need not make output covariance singular; unresolved ranks remain unresolved.',
    'Held RI73 operator proof is prior accepted evidence; no adjoint reconstruction or predecessor rerun is claimed.',
    'No colored covariance entries, inverse, whitening, residual score, SNR, p-value or chi-square law is computed.',
    'Calibration, mean/template, detector response, timing, noise-estimation uncertainty and a native forward map remain open; RET stays paused.',
]
RI83_LIMITATIONS = [
    'Known public development inputs with prior display and context access; not blind/protected validation.',
    'Nominal released V2/C02 strain; literal Yunits is empty; no extra calibration correction or uncertainty band.',
    'L1 NO_CW_HW_INJ is clear throughout; continuous-wave injection absence/effect is not established.',
    'Off-event names the fixed exclusion only; short overlapping sides have unequal seven/six segment counts.',
    'Finite descriptive spectra do not establish signal-free data, stationarity, Gaussianity or detector independence.',
    'Estimated spectra are not known covariance, unit-white covariance, whitening, a chi-square law or significance.',
    'Calibration/timing/mean-response/noise-estimation premises and a native forward map remain separate prerequisites.',
    'Retained bins below 10 Hz have no added calibrated physical interpretation; no RET work is implied.',
]


class ProxyError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def need(condition, code, message):
    if not condition:
        raise ProxyError(code, message)


def rat(value):
    need(type(value) is F, 'EXACT', 'Fraction required')
    need(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= BITS,
         'RESOURCE', 'exact numerator/denominator cap')
    return value


def add(a, b):
    return rat(rat(a) + rat(b))


def mul(a, b):
    return rat(rat(a) * rat(b))


def total(values):
    result = F(0)
    for value in values:
        result = add(result, value)
    return result


def scalar(value):
    value = rat(value)
    return [format(value.numerator, 'x'), format(value.denominator, 'x')]


def decode_scalar(value):
    need(type(value) is list and len(value) == 2, 'EXACT', 'hex rational pair required')
    for i, text in enumerate(value):
        need(type(text) is str and len(text) <= (BITS + 3) // 4 + (i == 0), 'RESOURCE', 'rational encoding size')
        pattern = r'(?:0|-?[1-9a-f][0-9a-f]*)' if i == 0 else r'[1-9a-f][0-9a-f]*'
        need(re.fullmatch(pattern, text) is not None, 'EXACT', 'canonical hex rational required')
    numerator, denominator = int(value[0], 16), int(value[1], 16)
    need(max(abs(numerator).bit_length(), denominator.bit_length()) <= BITS, 'RESOURCE', 'encoded integer cap')
    result = rat(F(numerator, denominator))
    need(scalar(result) == value, 'EXACT', 'unreduced hex rational')
    return result


def encoded(value):
    if type(value) is F:
        return scalar(value)
    if type(value) in (tuple, list):
        return [encoded(item) for item in value]
    if type(value) is dict:
        return {key: encoded(item) for key, item in value.items()}
    return value


def canonical(value):
    try:
        return (json.dumps(encoded(value), sort_keys=True, indent=2, ensure_ascii=True,
                           allow_nan=False) + '\n').encode('ascii')
    except (ValueError, TypeError, OverflowError) as error:
        raise ProxyError('JSON', 'finite serializable JSON required') from error


def exact(actual, expected, code, message):
    need(canonical(actual) == canonical(expected), code, message)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'JSON', 'duplicate JSON key')
        result[key] = value
    return result


def _json_float(text):
    result = float(text)
    need(math.isfinite(result), 'NONFINITE', 'nonfinite JSON number')
    return result


def parse_json(body):
    need(type(body) is bytes, 'JSON', 'retained bytes required')
    try:
        return json.loads(body.decode('utf-8'), object_pairs_hook=_pairs, parse_float=_json_float,
                          parse_constant=lambda value: (_ for _ in ()).throw(ProxyError('NONFINITE', 'nonfinite JSON constant')))
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ProxyError('JSON', 'invalid UTF-8 JSON') from error


def obj(value, keys, code, label):
    need(type(value) is dict and set(value) == set(keys), code, label + ' keys')
    return value


def seq(value, length, code, label):
    need(type(value) in (list, tuple) and len(value) == length, code, label + ' length')
    return value


def identity(body):
    need(type(body) is bytes, 'INPUT', 'bytes required')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def pin(value, code='INPUT'):
    obj(value, ('bytes', 'sha256'), code, 'pin')
    need(type(value['bytes']) is int and value['bytes'] > 0, code, 'positive integer byte count')
    need(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
         code, 'SHA-256 syntax')
    return value


def verify_body(body, expected, code='INPUT'):
    pin(expected, code)
    exact(identity(body), expected, code, 'retained body identity differs')
    return body


def verify_binding(actual, expected, kind):
    need(kind in ('SOURCE', 'RUNTIME', 'CUSTODY'), 'CUSTODY', 'binding kind')
    exact(actual, expected, kind, 'frozen ' + kind.lower() + ' binding differs')
    return True


def number(text):
    need(type(text) is str, 'HEX', 'float hex string required')
    try:
        value = float.fromhex(text)
    except OverflowError as error:
        raise ProxyError('NONFINITE', 'overflowing binary64 literal') from error
    except ValueError as error:
        raise ProxyError('HEX', 'invalid float hex') from error
    need(math.isfinite(value), 'NONFINITE', 'finite binary64 required')
    need(value.hex() == text, 'HEX', 'canonical binary64 hex required')
    return value


def decode_psd(record, bins=8193):
    need(type(bins) is int and bins in (3, 8193), 'BINS', 'fixed bin count')
    obj(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'SPECTRA_SCHEMA', 'PSD record')
    exact(record['dtype'], '<f8', 'DTYPE', 'PSD dtype')
    exact(record['shape'], [bins], 'BINS', 'PSD shape')
    seq(record['values_hex'], bins, 'BINS', 'PSD')
    need(type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']) is not None,
         'IDENTITY', 'array SHA-256 syntax')
    digest = hashlib.sha256()
    result = []
    for text in record['values_hex']:
        value = number(text)
        need(value >= 0, 'NEGATIVE_PSD', 'negative PSD bin')
        digest.update(struct.pack('<d', value))
        result.append(rat(F.from_float(value)))
    need(digest.hexdigest() == record['sha256'], 'IDENTITY', 'array byte identity differs')
    return tuple(result)


def matrix(value, dimension, *, decode=False, code='DOMAIN'):
    seq(value, dimension, code, 'matrix rows')
    return tuple(tuple(decode_scalar(x) if decode else rat(x)
                       for x in seq(row, dimension, code, 'matrix columns')) for row in value)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    return tuple(tuple(total(mul(x, y) for x, y in zip(row, col, strict=True))
                       for col in transpose(b)) for row in a)


def eye(dimension):
    return tuple(tuple(F(int(i == j)) for j in range(dimension)) for i in range(dimension))


def symmetric(a, code):
    need(a == transpose(a), code, 'matrix must be exactly symmetric')
    return a


def positive_ldl(g):
    n = len(g)
    lower = [list(row) for row in eye(n)]
    pivots = []
    for j in range(n):
        pivot = add(g[j][j], -total(mul(mul(lower[j][k], lower[j][k]), pivots[k]) for k in range(j)))
        need(pivot > 0, 'LDL_PIVOT', 'strictly positive exact pivot required')
        pivots.append(pivot)
        for i in range(j + 1, n):
            numerator = add(g[i][j], -total(mul(mul(lower[i][k], lower[j][k]), pivots[k]) for k in range(j)))
            lower[i][j] = rat(numerator / pivot)
    return tuple(map(tuple, lower)), tuple(pivots)


def build_scenario(psd, fs, G, rho, *, application=False):
    need(type(psd) in (list, tuple) and len(psd) in (3, 8193), 'DOMAIN', 'fixed PSD domain')
    need(type(application) is bool, 'DOMAIN', 'boolean application control required')
    m = 2 * (len(psd) - 1)
    n = len(G) if type(G) in (list, tuple) else 0
    need((m == 4 and n in (1, 2)) or (m == M and n == DIM), 'DOMAIN', 'fixed matrix/domain combination')
    fs, rho = rat(fs), rat(rho)
    need(fs == F(4 if m == 4 else FS), 'DOMAIN', 'fixed sampling frequency')
    need(F(0) <= rho < F(1), 'RHO', '0<=rho<1 required')
    if application:
        need(m == M and n == DIM, 'DOMAIN', 'application dimensions')
        need(rho <= RHO_LIMIT, 'RHO_ACCURACY', 'inherited rho usefulness gate')
    g = symmetric(matrix(G, n), 'GRAM_SYMMETRY')
    positive_ldl(g)
    values = tuple(rat(x) for x in psd)
    need(all(x >= 0 for x in values), 'NEGATIVE_PSD', 'negative PSD bin')
    dc = mul(fs, values[0])
    non_dc = tuple(mul(fs, value) if k == m // 2 else rat(mul(fs, value) / 2)
                   for k, value in enumerate(values[1:], 1))
    ell, upper_eigenvalue = min(non_dc), max(non_dc)
    lower_scale = mul(ell, add(F(1), -rho))
    upper_scale = mul(upper_eigenvalue, add(F(1), rho))
    lower = tuple(tuple(mul(lower_scale, x) for x in row) for row in g)
    upper = tuple(tuple(mul(upper_scale, x) for x in row) for row in g)
    positive = sum(value > 0 for value in values[1:-1])
    non_dc_rank = 2 * positive + int(values[-1] > 0)
    rank_upper = min(n, non_dc_rank)
    return {'lambda_dc': dc, 'lambda_nyquist': non_dc[-1], 'non_dc_eigenvalues': non_dc,
            'q_proxy': mul(rat(fs / m), total(values)), 'ell': ell, 'u': upper_eigenvalue,
            'minimum_indices': tuple(k for k, value in enumerate(non_dc, 1) if value == ell),
            'maximum_indices': tuple(k for k, value in enumerate(non_dc, 1) if value == upper_eigenvalue),
            'zero_interior_count': m // 2 - 1 - positive, 'positive_interior_count': positive,
            'spectral_rank': non_dc_rank + int(values[0] > 0), 'non_dc_rank': non_dc_rank,
            'rank_upper': rank_upper,
            'rank_status': ('positive_definite_rank' + str(n) if ell > 0 else
                            'zero_rank0' if upper_eigenvalue == 0 else 'unresolved_by_envelope'),
            'singularity_proved': rank_upper < n,
            'lower': lower, 'upper': upper, 'diagonal': tuple((lower[i][i], upper[i][i]) for i in range(n)),
            'trace': (total(lower[i][i] for i in range(n)), total(upper[i][i] for i in range(n)))}


def validate_certificate(certificate, dimension=8, application=True):
    need(type(dimension) is int and dimension in (1, 2, 8) and type(application) is bool,
         'CERT_SCHEMA', 'certificate domain control')
    if application:
        need(dimension == DIM, 'DIMENSIONS', 'application certificate dimension')
    obj(certificate, ('source_gate', 'source_model', 'G', 'H', 'V', 'ldl', 'delta', 'gamma', 'rho', 'checks'),
        'CERT_SCHEMA', 'projected certificate')
    exact(certificate['source_gate'], 'integration:gram', 'CERT_SCHEMA', 'certificate gate')
    exact(certificate['source_model'], 'known_synthetic_unit_white', 'PRIOR_MODEL', 'held model label')
    exact(certificate['checks'], list(CERT_CHECKS), 'CERT_SCHEMA', 'certificate check labels')
    g = symmetric(matrix(certificate['G'], dimension, decode=True, code='CERT_SCHEMA'), 'GRAM_SYMMETRY')
    h = symmetric(matrix(certificate['H'], dimension, decode=True, code='CERT_SCHEMA'), 'ERROR_SYMMETRY')
    need(all(x >= 0 for row in h for x in row), 'ERROR_NEGATIVE', 'negative error entry')
    factor = obj(certificate['ldl'], ('lower', 'pivots', 'reconstruction'), 'CERT_SCHEMA', 'LDL')
    lower = matrix(factor['lower'], dimension, decode=True, code='CERT_SCHEMA')
    pivots = tuple(decode_scalar(x) for x in seq(factor['pivots'], dimension, 'CERT_SCHEMA', 'pivots'))
    need(all(x > 0 for x in pivots), 'LDL_PIVOT', 'strictly positive stored pivots required')
    expected_lower, expected_pivots = positive_ldl(g)
    need(lower == expected_lower and pivots == expected_pivots, 'LDL_RECONSTRUCTION', 'stored LDL factors differ')
    reconstruction = matrix(factor['reconstruction'], dimension, decode=True, code='CERT_SCHEMA')
    diagonal = tuple(tuple(pivots[i] if i == j else F(0) for j in range(dimension)) for i in range(dimension))
    need(matmul(matmul(lower, diagonal), transpose(lower)) == reconstruction == g,
         'LDL_RECONSTRUCTION', 'exact LDL reconstruction differs')
    inverse = symmetric(matrix(certificate['V'], dimension, decode=True, code='CERT_SCHEMA'), 'INVERSE')
    need(matmul(g, inverse) == eye(dimension) and matmul(inverse, g) == eye(dimension), 'INVERSE', 'two-sided inverse identity')
    delta, gamma, rho = (decode_scalar(certificate[key]) for key in ('delta', 'gamma', 'rho'))
    need(delta == max(total(row) for row in h), 'DELTA', 'delta identity')
    need(gamma == max(total(abs(x) for x in row) for row in inverse), 'GAMMA', 'gamma identity')
    need(F(0) <= rho < F(1), 'RHO', '0<=rho<1 required')
    need(rho == mul(delta, gamma), 'RHO_IDENTITY', 'rho identity')
    if application:
        need(rho <= RHO_LIMIT, 'RHO_ACCURACY', 'inherited rho usefulness gate')
    return {'source_gate': certificate['source_gate'], 'source_model': certificate['source_model'],
            'G': g, 'H': h, 'V': inverse, 'ldl': {'lower': lower, 'pivots': pivots, 'reconstruction': reconstruction},
            'delta': delta, 'gamma': gamma, 'rho': rho, 'checks': list(CERT_CHECKS)}


# Exact published inventory transcribed from RI73 checker source, not observed values.
RI73_GATE_IDS = ('fixture:fir',
 'fixture:cancellation',
 'fixture:singleton',
 'fixture:offdiagonal_small',
 'fixture:offdiagonal_large',
 'fixture:failed_gate',
 'fixture:midpoint',
 'fixture:rank_ambiguity',
 'fixture:singular',
 'fixture:output_law',
 'refusal:float_endpoint',
 'refusal:bool_endpoint',
 'refusal:nonfinite_endpoint',
 'refusal:reversed_interval',
 'refusal:negative_radius',
 'refusal:matrix_rows',
 'refusal:bool_dimension',
 'refusal:bool_row_dimension',
 'refusal:matrix_columns',
 'refusal:ragged_box',
 'refusal:asymmetric_gram',
 'refusal:asymmetric_error',
 'refusal:negative_error',
 'refusal:negative_pivot',
 'refusal:wrong_ldl',
 'refusal:wrong_inverse',
 'refusal:wrong_delta',
 'refusal:wrong_gamma',
 'refusal:incorrect_rank',
 'refusal:bool_rank',
 'refusal:wrong_mp1',
 'refusal:wrong_mp2',
 'refusal:wrong_mp3',
 'refusal:off_support',
 'refusal:negative_rho',
 'refusal:rho_at_one',
 'refusal:negative_output_error',
 'refusal:unqualified_cdf',
 'refusal:cdf_series_domain',
 'refusal:negative_cdf_argument',
 'refusal:estimated_covariance',
 'refusal:colored_covariance',
 'refusal:fraction_numerator_cap',
 'refusal:fraction_denominator_cap',
 'refusal:operation_result_cap',
 'refusal:hex_length',
 'refusal:hex_plus',
 'refusal:hex_negative_zero',
 'refusal:hex_leading_zero',
 'refusal:hex_denominator_zero',
 'refusal:hex_unreduced',
 'refusal:work_cap',
 'refusal:work_bool',
 'refusal:output_cap',
 'refusal:duplicate_json',
 'refusal:nonfinite_json',
 'refusal:overflow_json',
 'refusal:changed_snapshot',
 'refusal:bool_pin',
 'refusal:changed_runtime',
 'refusal:changed_runtime_build',
 'refusal:failed_receipt',
 'refusal:incomplete_receipt',
 'refusal:changed_receipt_engine',
 'refusal:changed_arithmetic',
 'refusal:wrong_padding',
 'refusal:bool_padding',
 'refusal:changed_manifest_coefficient',
 'refusal:changed_manifest_stage_order',
 'refusal:changed_manifest_padding',
 'refusal:missing_rows',
 'refusal:wrong_rows',
 'refusal:wrong_snapshot_shape',
 'refusal:missing_expected_summaries',
 'integration:reconstruction',
 'integration:gram',
 'integration:mathematical',
 'integration:accuracy',
 'integration:cross',
 'probe:zero',
 'probe:constant',
 'probe:0',
 'probe:1',
 'probe:27',
 'probe:805',
 'probe:1384',
 'probe:2741',
 'probe:2767',
 'probe:2768',
 'integration:law',
 'integration:final_custody',
 'completion:custody')

RI73_DEPENDENCIES = {'design': {'path': 'gwosc_noise_operator_covariance_v1/DESIGN.md',
            'bytes': 29545,
            'sha256': '08e6e99d0f884e26b9b4a2422789431d6d6acf077dbb751dd73144b5c6409cd6'},
 'check60': {'path': 'gwosc_context_operator_v2/check.py',
             'bytes': 38088,
             'sha256': 'a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02'},
 'engine': {'path': 'gwosc_context_operator_v2/operator.py',
            'bytes': 30531,
            'sha256': 'ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af'},
 'oracle': {'path': 'gwosc_context_operator_v1/oracle.py',
            'bytes': 9484,
            'sha256': '37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651'},
 'qualification60': {'path': 'gwosc_context_operator_v2/QUALIFICATION_REPORT.json',
                     'bytes': 9413345,
                     'sha256': '1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f'},
 'failed_predecessor': {'path': 'gwosc_context_operator_v1/QUALIFICATION_REPORT.json',
                        'bytes': 161816,
                        'sha256': '7dfbc8cac7e631a9c3663bca2b288b134d6cea03f1d0ca14c8334746761a808a'},
 'filtering': {'path': 'gwosc_nominal_processing_v1/filtering.py',
               'bytes': 8805,
               'sha256': '9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be'},
 'reference': {'path': 'gwosc_nominal_processing_v1/reference.py',
               'bytes': 7253,
               'sha256': 'c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305'},
 'coefficients': {'path': 'gwosc_nominal_processing_v1/COEFFICIENTS.json',
                  'bytes': 7698,
                  'sha256': '700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0'},
 'prior_qualification': {'path': 'gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json',
                         'bytes': 107468,
                         'sha256': '2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3'},
 'recipe': {'path': 'gwosc_nominal_display_v1/RECIPE.md',
            'bytes': 14014,
            'sha256': '872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a'},
 'prior_design': {'path': 'gwosc_context_sensitivity_v1/DESIGN.md',
                  'bytes': 21702,
                  'sha256': 'e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45'},
 'window_design': {'path': 'gwosc_observed_context_v1/DESIGN.md',
                   'bytes': 19255,
                   'sha256': '636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2'},
 'noise_design': {'path': 'gwosc_context_noise_v1/DESIGN.md',
                  'bytes': 24027,
                  'sha256': '74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921'}}

RI73_TOP_KEYS = ('schema_version', 'mode', 'status', 'full_integration_qualified', 'source_identity',
                  'dependencies', 'runtime', 'inherited_arithmetic_contract', 'resource_contract', 'model',
                  'dimensions', 'rows', 'sample_spacing', 'gate_inventory', 'gate_counts', 'gates',
                  'deterministic_fixture_admission_passed', 'sampling_performed',
                  'admitted_coefficient_design_requested', 'reconstructed_rows_admitted',
                  'exact_scalar_encoding', 'scope')
RI73_CERT_KEYS = ('mathematical_gate', 'accuracy_gate', 'rho_limit', 'G', 'H', 'delta', 'eta2', 'ldl',
                  'inverse', 'left_inverse_product', 'right_inverse_product', 'gamma', 'rho', 'status',
                  'rank', 'inverse_error_norm_bound', 'inverse_lower', 'inverse_upper')
RI73_MODEL = {'kind': 'known_synthetic_unit_white', 'mean': 'zero', 'covariance': 'I_T',
              'input_dimension': T, 'output_dimension': DIM}
RUNTIME_KEYS = ('versions', 'python_implementation', 'python_build', 'operating_system', 'os_release',
                'os_version', 'machine', 'byte_order', 'hdf5_version', 'numpy_configuration')
VERSIONS = {'python': '3.11.6', 'numpy': '2.1.3', 'scipy': '1.14.1', 'h5py': '3.12.1'}


def admit_ri73(report):
    obj(report, RI73_TOP_KEYS, 'PRIOR_SCHEMA', 'RI73 report')
    exact(report['schema_version'], 'ri73-unit-white-operator-covariance-v1', 'PRIOR_SCHEMA', 'RI73 schema')
    for key, expected in (('mode', 'fixed_operator_covariance'), ('status', 'fixed_operator_covariance_passed'),
                          ('full_integration_qualified', True), ('deterministic_fixture_admission_passed', True),
                          ('sampling_performed', False), ('admitted_coefficient_design_requested', True),
                          ('reconstructed_rows_admitted', True)):
        exact(report[key], expected, 'PRIOR_STATUS', 'RI73 ' + key)
    exact(report['model'], RI73_MODEL, 'PRIOR_MODEL', 'unit-white prior model required unchanged')
    exact(report['dimensions'], {'N': N, 'L': L, 'T': T}, 'DIMENSIONS', 'held lengths')
    exact(report['rows'], list(ROWS), 'ROWS', 'held row order')
    exact(report['sample_spacing'], scalar(F(1, FS)), 'DIMENSIONS', 'sample spacing')
    exact(report['source_identity'], RI73_SOURCE_PIN, 'SOURCE', 'held checker pin')
    exact(report['dependencies'], RI73_DEPENDENCIES, 'SOURCE', 'complete held dependency pins')
    obj(report['runtime'], RUNTIME_KEYS, 'RUNTIME', 'held runtime fingerprint')
    exact(report['runtime']['versions'], VERSIONS, 'RUNTIME', 'held runtime versions')
    exact(report['runtime']['hdf5_version'], '1.12.2', 'RUNTIME', 'held HDF5 build')
    exact(report['runtime']['python_implementation'], 'CPython', 'RUNTIME', 'held Python implementation')
    # The future caller binds the full fingerprint, not just these version keys.
    exact(report['gate_inventory'], list(RI73_GATE_IDS), 'GATE_INVENTORY', '92 ordered gate IDs')
    exact(report['gate_counts'], {'total': 92, 'passed': 92, 'failed': 0}, 'GATE_STATUS', '92 passed gates')
    gates = seq(report['gates'], 92, 'GATE_INVENTORY', 'RI73 gates')
    selected = None
    for row, expected in zip(gates, RI73_GATE_IDS, strict=True):
        obj(row, ('id', 'passed', 'detail'), 'GATE_INVENTORY', 'RI73 gate')
        exact(row['id'], expected, 'GATE_INVENTORY', 'ordered unique gate')
        exact(row['passed'], True, 'GATE_STATUS', 'RI73 gate failed')
        need(type(row['detail']) is dict, 'PRIOR_SCHEMA', 'gate detail object required')
        if expected == 'integration:gram':
            obj(row['detail'], ('certificate', 'M_identity', 'R_identity'), 'PRIOR_SCHEMA', 'Gram detail')
            selected = row['detail']['certificate']
    need(selected is not None, 'GATE_INVENTORY', 'unique Gram gate required')
    obj(selected, RI73_CERT_KEYS, 'CERT_SCHEMA', 'complete prior certificate')
    for key, expected in (('mathematical_gate', True), ('accuracy_gate', True),
                          ('status', 'certified'), ('rank', DIM), ('rho_limit', scalar(RHO_LIMIT))):
        exact(selected[key], expected, 'PRIOR_STATUS', 'prior certificate ' + key)
    ldl = obj(selected['ldl'], ('positive', 'lower', 'pivots', 'reconstruction'), 'CERT_SCHEMA', 'prior LDL')
    exact(ldl['positive'], True, 'LDL_PIVOT', 'held positive LDL gate')
    projected = {'source_gate': 'integration:gram', 'source_model': report['model']['kind'],
                 'G': selected['G'], 'H': selected['H'], 'V': selected['inverse'],
                 'ldl': {key: ldl[key] for key in ('lower', 'pivots', 'reconstruction')},
                 'delta': selected['delta'], 'gamma': selected['gamma'], 'rho': selected['rho'],
                 'checks': list(CERT_CHECKS)}
    certificate = validate_certificate(projected)
    exact(selected['left_inverse_product'], encoded(eye(DIM)), 'INVERSE', 'held left inverse product')
    exact(selected['right_inverse_product'], encoded(eye(DIM)), 'INVERSE', 'held right inverse product')
    # These are prior auxiliary assertions, not newly reconstructed coefficient data.
    need(decode_scalar(selected['eta2']) >= 0, 'CERT_SCHEMA', 'negative squared coefficient radius')
    rho, gamma, v = certificate['rho'], certificate['gamma'], certificate['V']
    exact(selected['inverse_error_norm_bound'], scalar(rat(mul(rho, gamma) / (1 - rho))),
          'CERT_SCHEMA', 'held inverse-error bound')
    for field, denominator in (('inverse_lower', 1 + rho), ('inverse_upper', 1 - rho)):
        expected = tuple(tuple(rat(x / denominator) for x in row) for row in v)
        exact(selected[field], encoded(expected), 'CERT_SCHEMA', 'held inverse interval')
    return encoded(certificate)


def indices():
    return {'left': {'interval': [0, 65536], 'starts': [0, 8192, 16384, 24576, 32768, 40960, 49152],
                     'count': 7, 'used_interval': [0, 65536], 'unused_intervals': []},
            'right': {'interval': [69632, 131072], 'starts': [69632, 77824, 86016, 94208, 102400, 110592],
                      'count': 6, 'used_interval': [69632, 126976], 'unused_intervals': [[126976, 131072]]}}


def spectra_method():
    return {'design_pin': RI78_PIN.copy(), 'fs': FS, 'segment_length': M, 'stride': 8192, 'nfft': M,
            'exclusion': [65536, 69632], 'sides': indices(), 'bins': 8193, 'endpoint_weights': [1, 1],
            'interior_weight': 2, 'delta_f_hex': '0x1.0000000000000p-2',
            'detrend': 'arithmetic_per_segment_mean_before_window', 'window': 'periodic_hann_sym_false',
            'fft': 'numpy_rfft_backward', 'scaling': 'density_fs_times_actual_window_energy',
            'average': 'arithmetic_mean_periodograms', 'asd': 'sqrt_mean_psd',
            'eps_hex': '0x1.0000000000000p-52', 'tau_hex': '0x1.0000000000000p-40',
            'sqrt_relative_budget_hex': '0x1.0000000000000p-49'}


def input_metadata_report(detectors):
    """Same closed RI37 report reconstruction as the accepted RI83 validator."""
    return {'schema_version': 'gwosc-fixed-pair-qualification-v1', 'status': 'identity_and_structure_verified',
            'event': 'GW150914', 'strain_product_version': 'V2', 'detectors': detectors,
            'interpretation_boundary': {
                'dimensionless_strain': 'publisher interpretation; the literal strain Yunits attribute is empty',
                'C02_calibration': 'external publisher release identification, not a literal calibration header',
                'calibration_uncertainty': 'applicable artifact values, interpolation and correlations remain unqualified',
                'scientific_fit_readiness': 'not established by identity, structure, finite samples or quality flags',
                'prior_access': 'known public reference event; not blind evaluation data',
                'native_gravity_comparison': 'no native forward law or DET-versus-GR inference supplied'}}


def select_psd(side, field='mean_psd'):
    need(field == 'mean_psd', 'PSD_SELECTION', 'only original side mean_psd is admitted')
    need(type(side) is dict and field in side, 'PSD_SELECTION', 'mean_psd record missing')
    return side[field]


def admit_spectra(report):
    obj(report, ('schema', 'method', 'inputs', 'frequency_hz', 'window', 'detectors', 'checks', 'limitations'),
        'SPECTRA_SCHEMA', 'RI83 report')
    exact(report['schema'], 'ri78-off-event-spectra-v1', 'SPECTRA_SCHEMA', 'RI83 schema')
    exact(report['method'], spectra_method(), 'METHOD', 'complete held spectral method')
    exact(report['limitations'], RI83_LIMITATIONS, 'METADATA', 'held prior-access/calibration limitations')
    frequency = decode_psd(report['frequency_hz'])
    need(all(x == F(k, 4) for k, x in enumerate(frequency)), 'BINS', 'complete frequency grid')
    metadata = []
    for row, (detector, filename, size, md5, sha) in zip(seq(report['inputs'], 2, 'METADATA', 'inputs'), INPUTS, strict=True):
        obj(row, ('detector', 'filename', 'bytes', 'md5', 'sha256', 'url', 'ri37_detector',
                  'inspector_report_pin', 'recovery_handoff_pin'), 'METADATA', 'input')
        for key, expected in (('detector', detector), ('filename', filename), ('bytes', size), ('md5', md5),
                              ('sha256', sha), ('url', 'https://gwosc.org/GW150914data/' + filename),
                              ('inspector_report_pin', RI37_PIN), ('recovery_handoff_pin', RECOVERY_PIN)):
            exact(row[key], expected, 'METADATA', 'fixed input ' + key)
        metadata.append(row['ri37_detector'])
    # This hash closes every nested flag/Yunits/metadata field without HDF access.
    verify_body(canonical(input_metadata_report(metadata)), RI37_PIN, 'METADATA')
    checks = obj(report['checks'], ('identity', 'detectors'), 'SPECTRA_SCHEMA', 'RI83 checks')
    identity_checks = obj(checks['identity'], ('inspector_report_pin', 'recovery_handoff_pin',
                         'qualification_report_pin', 'fixed_dimensions_indices_and_flags'), 'METADATA', 'RI83 identity')
    exact(identity_checks, {'inspector_report_pin': RI37_PIN, 'recovery_handoff_pin': RECOVERY_PIN,
                           'qualification_report_pin': RI80_PIN, 'fixed_dimensions_indices_and_flags': True},
          'METADATA', 'complete identity checks')
    result = []
    for d, detector in enumerate(seq(report['detectors'], 2, 'DETECTOR_ORDER', 'detectors')):
        name = ('H1', 'L1')[d]
        obj(detector, ('detector', 'sides'), 'SPECTRA_SCHEMA', 'detector')
        exact(detector['detector'], name, 'DETECTOR_ORDER', 'detector order')
        for s, side in enumerate(seq(detector['sides'], 2, 'SIDE', 'sides')):
            label = ('left', 'right')[s]
            obj(side, ('side', 'interval', 'starts', 'count', 'used_interval', 'unused_intervals', 'segments',
                       'mean_psd', 'asd', 'q', 'psd_unit', 'asd_unit'), 'SPECTRA_SCHEMA', 'side')
            exact(side['side'], label, 'SIDE', 'side order')
            spec = indices()[label]
            for key, expected in spec.items():
                exact(side[key], expected, 'SIDE', 'fixed side ' + key)
            exact(side['psd_unit'], 'nominal_strain_squared_per_Hz', 'UNITS', 'PSD unit')
            exact(side['asd_unit'], 'nominal_strain_per_sqrt_Hz', 'UNITS', 'ASD unit')
            for segment, start in zip(seq(side['segments'], spec['count'], 'SIDE', 'segments'), spec['starts'], strict=True):
                obj(segment, ('start', 'end', 'gps_offset_numerators', 'gps_offset_denominator', 'flag_rows',
                              'dq_masks', 'injection_masks', 'mean', 'q', 'raw_sha256', 'demeaned_sha256',
                              'windowed_sha256', 'psd'), 'SPECTRA_SCHEMA', 'segment metadata')
                expected = {'start': start, 'end': start + M, 'gps_offset_numerators': [start, start + M],
                            'gps_offset_denominator': FS, 'flag_rows': list(range(start // FS, (start + M) // FS)),
                            'dq_masks': [127] * 4, 'injection_masks': [(31, 23)[d]] * 4}
                for key, value in expected.items():
                    exact(segment[key], value, 'METADATA', 'segment flags/indices ' + key)
            record = select_psd(side)
            decode_psd(record)
            q = number(side['q'])
            need(q >= 0, 'NEGATIVE_PSD', 'negative saved power')
            context = {**spec, 'psd_unit': side['psd_unit'], 'asd_unit': side['asd_unit'],
                       'prior_access': 'known_public_development', 'Yunits': '', 'injection_mask': (31, 23)[d],
                       'dq_mask': 127, 'NO_CW_HW_INJ': d == 0}
            result.append({'id': SCENARIOS[2 * d + s], 'detector': name, 'side': label,
                           'source_pointer': f'/detectors/{d}/sides/{s}/mean_psd',
                           'source_record': record, 'saved_q_hex': side['q'], 'context': context})
    return result


def validate_provenance(provenance, phase):
    need(phase in ('fabricated_qualification', 'fixed_saved_application'), 'PHASE', 'explicit phase required')
    obj(provenance, ('sources', 'inputs', 'acceptance', 'runtime'), 'CUSTODY', 'provenance')
    source = obj(provenance['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation'), 'SOURCE', 'source pins')
    for value in source.values():
        pin(value, 'SOURCE')
    exact(source['design'], DESIGN_PIN, 'SOURCE', 'accepted design pin')
    inputs = obj(provenance['inputs'], ('ri83', 'ri73'), 'INPUT', 'input pins')
    for name, expected in (('ri83', RI83_PIN), ('ri73', RI73_PIN)):
        pin(inputs[name], 'INPUT')
        if phase == 'fixed_saved_application':
            exact(inputs[name], expected, 'INPUT', 'published input identity')
        else:
            need(inputs[name] != expected, 'PHASE', 'fabricated input must not claim actual identity')
    acceptance = obj(provenance['acceptance'], ('ri83', 'ri73', 'ri86', 'qualification'), 'CUSTODY', 'acceptance pins')
    for name in ('ri83', 'ri73', 'ri86'):
        pin(acceptance[name], 'CUSTODY')
    if phase == 'fabricated_qualification':
        need(acceptance['qualification'] is None, 'PHASE', 'qualification is not yet accepted')
    else:
        pin(acceptance['qualification'], 'CUSTODY')
    runtime = obj(provenance['runtime'], ('inventory', 'fingerprint', 'interpreter'), 'RUNTIME', 'runtime pins')
    for value in runtime.values():
        pin(value, 'RUNTIME')
    return provenance


def build_result(ri83obj, ri73obj, provenance, *, phase='fabricated_qualification'):
    """Pure assembler; phase/schema do not independently establish byte custody."""
    validate_provenance(provenance, phase)
    sources = admit_spectra(ri83obj)
    projected = admit_ri73(ri73obj)
    certificate = validate_certificate(projected)
    # The frozen caller's runtime probe must supply this complete fingerprint pin.
    exact(identity(canonical(ri73obj['runtime'])), provenance['runtime']['fingerprint'],
          'RUNTIME', 'complete held/current runtime fingerprint pin')
    scenarios = []
    for source in sources:
        psd = decode_psd(source['source_record'])
        derived = build_scenario(psd, F(FS), certificate['G'], certificate['rho'], application=True)
        q_difference = add(derived['q_proxy'], -F.from_float(number(source['saved_q_hex'])))
        scenarios.append({**source, 'q_difference': q_difference, 'derived': derived})
    return encoded({'schema': 'ri86-colored-proxy-envelope-v1', 'phase': phase, 'status': 'all_gates_passed',
                    'model': 'postulated_finite_circulant_from_empirical_psd',
                    'dimensions': {'M': M, 'N': N, 'L': L, 'T': T, 'output': DIM}, 'fs': F(FS), 'df': F(1, 4),
                    'scenario_order': list(SCENARIOS), 'rows': list(ROWS), 'provenance': provenance,
                    'certificate': projected, 'scenarios': scenarios,
                    'gates': {'inventory': list(GATE_IDS), 'counts': {'total': 7, 'passed': 7, 'failed': 0},
                              'results': [{'id': label, 'passed': True} for label in GATE_IDS]},
                    'limitations': list(LIMITATIONS)})


def run_saved(ri83body, ri73body, provenance):
    """Only actual scientific entry point: bind both complete bodies before parse.

    The separately frozen caller supplies already admitted immutable byte snapshots
    and rechecks files/runtime after completion. This API does no filesystem access.
    """
    verify_body(ri83body, RI83_PIN)
    verify_body(ri73body, RI73_PIN)
    validate_provenance(provenance, 'fixed_saved_application')
    ri83 = parse_json(ri83body)
    ri73 = parse_json(ri73body)
    result = build_result(ri83, ri73, provenance, phase='fixed_saved_application')
    # Byte objects remain immutable; checking them again closes in-memory identity.
    verify_body(ri83body, RI83_PIN)
    verify_body(ri73body, RI73_PIN)
    return result


if __name__ == '__main__':
    raise SystemExit('RI87 source-only library: use the separately reviewed frozen caller; no direct execution.')
