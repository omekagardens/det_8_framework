"""RI119 fixed synthetic primary: exact complete sign enumeration.

Source only until separately admitted. No I/O, target imports or import-time
calculation. The retained-report comparator requires a freshly enumerated
reference owned by the admitted caller, not an externally supplied oracle.
"""
from fractions import Fraction
from itertools import product
import json
import re

BITS = 8192
DECIMAL_COMPONENT_LIMIT = 2467
BODY_LIMIT = 2 * 1024 * 1024
CASE_IDS = ('Q02_white_two', 'Q03_periodic_two', 'Q05_white_three',
            'Q06_constant_mean', 'Q07_quadratic_mean', 'Q08_scale_minus_one',
            'Q08_scale_two', 'Q09_oriented_matrix', 'Q10_zero_map')
BOUND_IDS = ('Q12_calibrated_constant', 'Q12_covariance_error', 'Q12_calibration_error')
GROUPS = tuple('Q' + str(i).zfill(2) for i in range(1, 13))
METHOD = {'rational_encoding': 'reduced_decimal_strings', 'arithmetic': 'exact_rational',
          'primary_route': 'complete_sign_enumeration',
          'validator_route': 'independent_moment_selector_factor_algebra',
          'inputs': 'fixed_synthetic_only', 'divisor': 'n',
          'real_operator_evaluated': False, 'empirical_inputs_evaluated': False,
          'physical_model_validated': False}
LIMITATIONS = (
    'Synthetic joint-window arithmetic only; no empirical data or actual coefficient capture.',
    'Shared sample and covariance refusals concern the declared fixed model, not every alternative model.',
    'Finite circulant marginals do not select a physical joint window law.',
    'Mean, calibration and model-error premises are explicit and not estimated here.',
    'No significance, physical calibration, protected validation or native forward claim; RET remains paused.',
)
RATIONAL = re.compile(r'(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z')


class PrimaryError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def require(condition, code, message):
    if not condition:
        raise PrimaryError(code, message)


def bounded(x):
    require(type(x) is Fraction, 'EXACT', 'internal Fraction required')
    require(max(abs(x.numerator).bit_length(), x.denominator.bit_length()) <= BITS,
            'RESOURCE', 'reduced rational bit limit')
    return x


def plus(a, b): return bounded(a + b)
def minus(a, b): return bounded(a - b)
def times(a, b): return bounded(a * b)
def divide(a, b):
    require(b != 0, 'EXACT', 'zero divisor')
    return bounded(a / b)


def total(xs):
    value = Fraction(0)
    for x in xs:
        value = plus(value, x)
    return value


def scalar(text):
    require(type(text) is str and len(text) <= 2 * DECIMAL_COMPONENT_LIMIT + 2,
            'RESOURCE' if type(text) is str else 'EXACT', 'bounded scalar string required')
    pieces = text.split('/')
    require(all(len(p.lstrip('-')) <= DECIMAL_COMPONENT_LIMIT for p in pieces),
            'RESOURCE', 'decimal component limit')
    require(RATIONAL.fullmatch(text) is not None, 'EXACT', 'decimal rational syntax')
    numerator = int(pieces[0])
    denominator = int(pieces[1]) if len(pieces) == 2 else 1
    require(max(abs(numerator).bit_length(), denominator.bit_length()) <= BITS,
            'RESOURCE', 'parsed rational component bit limit')
    number = bounded(Fraction(numerator, denominator))
    require(str(number) == text, 'EXACT', 'canonical reduced rational')
    return number


def encode(value):
    if type(value) is Fraction:
        return str(bounded(value))
    if type(value) is list:
        return [encode(v) for v in value]
    if type(value) is dict:
        return {key: encode(v) for key, v in value.items()}
    require(type(value) in (str, int, bool), 'SCHEMA', 'unsupported output value')
    return value


def canonical(value):
    try:
        body = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                           allow_nan=False) + '\n').encode('ascii')
    except (TypeError, ValueError, OverflowError, RecursionError) as error:
        raise PrimaryError('CANONICAL', 'cannot encode canonical report') from error
    require(len(body) <= BODY_LIMIT, 'RESOURCE', 'report byte limit')
    return body


def parse_result(body):
    require(type(body) is bytes, 'CANONICAL', 'bytes required')
    require(len(body) <= BODY_LIMIT, 'RESOURCE', 'report byte limit')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'CANONICAL', 'duplicate JSON key')
            result[key] = value
        return result
    def bad(_): raise PrimaryError('CANONICAL', 'nonfinite JSON')
    try:
        value = json.loads(body, object_pairs_hook=pairs, parse_constant=bad)
    except (UnicodeError, ValueError, RecursionError) as error:
        if isinstance(error, PrimaryError): raise
        raise PrimaryError('CANONICAL', 'invalid JSON') from error
    require(canonical(value) == body, 'CANONICAL', 'whole canonical bytes required')
    return value


def zeros(rows, cols):
    return [[Fraction(0) for _ in range(cols)] for _ in range(rows)]


def selector(start, length, raw_length):
    return [[int(j == start + i) for j in range(raw_length)] for i in range(length)]


def dot(row, vector):
    require(len(row) == len(vector), 'DIMENSION', 'dot dimensions')
    return total(times(a, b) for a, b in zip(row, vector))


def outer_accumulate(matrix, vector):
    for i, a in enumerate(vector):
        for j, b in enumerate(vector):
            matrix[i][j] = plus(matrix[i][j], times(a, b))


def covariance(second, mean, count):
    return [[minus(divide(second[i][j], Fraction(count)), times(mean[i], mean[j]))
             for j in range(len(mean))] for i in range(len(mean))]


def fixed_model(case_id):
    require(case_id in CASE_IDS, 'INVENTORY', 'fixed case')
    n = 3 if case_id in ('Q05_white_three', 'Q07_quadratic_mean') else 2
    starts = [2 * i for i in range(n)]
    raw_length = starts[-1] + 4
    periodic = case_id == 'Q03_periodic_two'
    latent = 4 if periodic else raw_length
    factor = [[Fraction(int(j == (i % 4 if periodic else i))) for j in range(latent)]
              for i in range(raw_length)]
    mean = [Fraction(3 if case_id == 'Q06_constant_mean' else
                     i * i if case_id == 'Q07_quadratic_mean' else 0)
            for i in range(raw_length)]
    a = [[Fraction(1), Fraction(0), Fraction(-1)]]
    if case_id == 'Q09_oriented_matrix':
        a.append([Fraction(0), Fraction(1), Fraction(-1)])
    if case_id == 'Q10_zero_map':
        a = [[Fraction(0), Fraction(0), Fraction(0)]]
    scale = Fraction(-1 if case_id == 'Q08_scale_minus_one' else
                     2 if case_id == 'Q08_scale_two' else 1)
    return {'kind': 'shared_periodic' if periodic else 'shared_raw_white',
            'M': 4, 'T': 3, 'stride': 2, 'n': n, 'starts': starts,
            'raw_length': raw_length, 'latent_dimension': latent,
            'output_dimension': len(a), 'A': a, 'raw_factor': factor,
            'raw_mean': mean, 'scale': scale}


def enumerate_case(case_id):
    model = fixed_model(case_id)
    n, q, size, latent = (model[k] for k in ('n', 'output_dimension', 'raw_length', 'latent_dimension'))
    require(n <= 3 and q <= 2 and size <= 8 and latent <= 8, 'RESOURCE', 'fixed tiny dimensions')
    starts, a = model['starts'], model['A']
    raw_sum = [Fraction(0)] * size
    output_sum = [Fraction(0)] * (n * q)
    bar_sum = [Fraction(0)] * q
    raw_outer, output_outer, bar_outer = zeros(size, size), zeros(n * q, n * q), zeros(q, q)
    centered_outer = zeros(q, q)
    sum_v = sum_u = sum_bar_energy = Fraction(0)
    count = 0
    for signs in product((-1, 1), repeat=latent):
        latent_values = [Fraction(x) for x in signs]
        raw = [times(model['scale'], plus(m, dot(f, latent_values)))
               for m, f in zip(model['raw_mean'], model['raw_factor'])]
        outputs = [[dot(row, raw[start:start + 3]) for row in a] for start in starts]
        # Mandatory pointwise properties: second moments alone cannot tell a
        # scale of -1 from +1. These guards run on every vector in these cubes.
        if case_id in ('Q06_constant_mean', 'Q08_scale_minus_one', 'Q08_scale_two'):
            base_raw = [dot(f, latent_values) for f in model['raw_factor']]
            base_outputs = [[dot(row, base_raw[start:start + 3]) for row in a] for start in starts]
            if case_id == 'Q06_constant_mean':
                require(all(total(row) == 0 for row in a), 'MEAN_TERM', 'actual operator row sums')
                require(outputs == base_outputs, 'MEAN_TERM', 'pointwise constant mean cancellation')
            else:
                signed_outputs = [[times(model['scale'], x) for x in values] for values in base_outputs]
                require(outputs == signed_outputs, 'ENERGY', 'pointwise signed output scaling')
        flat = [x for values in outputs for x in values]
        bar = [divide(total(values[i] for values in outputs), Fraction(n)) for i in range(q)]
        centered = [[minus(x, b) for x, b in zip(values, bar)] for values in outputs]
        v = divide(total(times(x, x) for values in centered for x in values), Fraction(n))
        u = divide(total(times(x, x) for values in outputs for x in values), Fraction(n))
        mean_energy = total(times(x, x) for x in bar)
        require(u == plus(v, mean_energy), 'ENERGY', 'pointwise U=V+mean energy')
        sum_v, sum_u = plus(sum_v, v), plus(sum_u, u)
        sum_bar_energy = plus(sum_bar_energy, mean_energy)
        raw_sum = [plus(x, y) for x, y in zip(raw_sum, raw)]
        output_sum = [plus(x, y) for x, y in zip(output_sum, flat)]
        bar_sum = [plus(x, y) for x, y in zip(bar_sum, bar)]
        outer_accumulate(raw_outer, raw)
        outer_accumulate(output_outer, flat)
        outer_accumulate(bar_outer, bar)
        for values in centered:
            outer_accumulate(centered_outer, values)
        count += 1
    require(count == 2 ** latent, 'ENUMERATION', 'entire fixed sign cube')
    raw_mean = [divide(x, Fraction(count)) for x in raw_sum]
    output_mean = [divide(x, Fraction(count)) for x in output_sum]
    bar_mean = [divide(x, Fraction(count)) for x in bar_sum]
    centered_mean = [[minus(output_mean[j * q + i], bar_mean[i]) for i in range(q)]
                     for j in range(n)]
    mean_dispersion_matrix = zeros(q, q)
    for values in centered_mean:
        outer_accumulate(mean_dispersion_matrix, values)
    mean_dispersion_matrix = [[divide(x, Fraction(n)) for x in row] for row in mean_dispersion_matrix]
    centered_cov = [[minus(divide(centered_outer[i][j], Fraction(count * n)),
                           mean_dispersion_matrix[i][j]) for j in range(q)] for i in range(q)]
    raw_cov = covariance(raw_outer, raw_mean, count)
    stack_cov = covariance(output_outer, output_mean, count)
    bar_cov = covariance(bar_outer, bar_mean, count)
    covariance_contribution = total(centered_cov[i][i] for i in range(q))
    mean_dispersion = total(mean_dispersion_matrix[i][i] for i in range(q))
    expected_v = plus(covariance_contribution, mean_dispersion)
    direct_v = divide(sum_v, Fraction(count))
    require(direct_v == expected_v, 'ENERGY', 'complete centered moment identity')
    output_map = []
    for start in starts:
        for row in a:
            output_map.append([row[j - start] if start <= j < start + 3 else Fraction(0)
                               for j in range(size)])
    result = {'id': case_id, 'model': encode(model),
              'selectors_M': [selector(s, 4, size) for s in starts],
              'selectors_T': [selector(s, 3, size) for s in starts],
              'output_map': encode(output_map), 'raw_mean': encode(raw_mean),
              'raw_covariance': encode(raw_cov),
              'window_marginal_covariances': encode([[[raw_cov[s + i][s + j] for j in range(4)]
                                                     for i in range(4)] for s in starts]),
              'stacked_output_mean': encode(output_mean), 'stacked_output_covariance': encode(stack_cov),
              'cross_blocks': encode([[[[stack_cov[aa * q + i][bb * q + j] for j in range(q)]
                                       for i in range(q)] for bb in range(n)] for aa in range(n)]),
              'mean_output_covariance': encode(bar_cov), 'centered_covariance_average': encode(centered_cov),
              'mean_dispersion': str(mean_dispersion), 'covariance_contribution': str(covariance_contribution),
              'expected_V': str(expected_v), 'direct_average_V': str(direct_v),
              'expected_U': str(divide(sum_u, Fraction(count))),
              'mean_output_energy': str(divide(sum_bar_energy, Fraction(count))), 'sign_count': count}
    if case_id in ('Q02_white_two', 'Q03_periodic_two'):
        require_psd_2x2(result['stacked_output_covariance'])
    return result


def factor_contribution(factor):
    # Standalone Q12 one-output-per-window D=(1,-1)^T, Pi=H2.
    total_v = Fraction(0)
    count = 0
    for values in product((-1, 1), repeat=len(factor)):
        x = dot(factor, [Fraction(v) for v in values])
        total_v = plus(total_v, times(x, x))
        count += 1
    return divide(total_v, Fraction(count))


def fixed_bounds():
    d = [[Fraction(1)], [Fraction(-1)]]
    pi = [[Fraction(1, 2), Fraction(-1, 2)], [Fraction(-1, 2), Fraction(1, 2)]]
    base = factor_contribution([Fraction(1)])
    true = factor_contribution([Fraction(1), Fraction(1)])
    changed = factor_contribution([Fraction(2)])
    norm_sq = total(times(row[0], row[0]) for row in d)
    model_bound = divide(norm_sq, Fraction(2))
    calibration_bound = divide(plus(times(Fraction(2), norm_sq), norm_sq), Fraction(2))
    constant = dot([Fraction(1), Fraction(0), Fraction(-1)], [Fraction(1), Fraction(1), Fraction(2)])
    return encode([
        {'id': 'Q12_calibrated_constant', 'output_dimension': 1,
         'A': [[Fraction(1), Fraction(0), Fraction(-1)]],
         'C_cal': [[Fraction(1), Fraction(0), Fraction(0)],
                   [Fraction(0), Fraction(1), Fraction(0)],
                   [Fraction(0), Fraction(0), Fraction(2)]],
         'input': [Fraction(1), Fraction(1), Fraction(1)], 'output': [constant],
         'constant_annihilation_claim': False},
        {'id': 'Q12_covariance_error', 'n': 2, 'output_dimension': 1, 'D': d, 'Pi': pi,
         'Sigma_model': [[Fraction(1)]], 'Sigma_true': [[Fraction(2)]], 'eta': Fraction(1),
         'model_contribution': base, 'true_contribution': true,
         'absolute_difference': abs(minus(true, base)), 'bound': model_bound},
        {'id': 'Q12_calibration_error', 'n': 2, 'output_dimension': 1, 'D': d, 'Pi': pi,
         'C0': [[Fraction(1)]], 'DeltaC': [[Fraction(1)]], 'F': [[Fraction(1)]],
         'model_contribution': base, 'true_contribution': changed,
         'absolute_difference': abs(minus(changed, base)), 'bound': calibration_bound},
    ])


def build_result():
    return {'schema': 'ri119-joint-window-synthetic-v1',
            'phase': 'fabricated_joint_window_qualification', 'status': 'all_declared_checks_passed',
            'method': dict(METHOD), 'cases': [enumerate_case(name) for name in CASE_IDS],
            'bounds': fixed_bounds(), 'groups': list(GROUPS), 'limitations': list(LIMITATIONS)}


def typed_equal(a, b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in b)
    if type(a) is list:
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def compare(a, b, code, message):
    require(typed_equal(a, b), code, message)


def shape_and_scalars(actual, expected):
    if type(expected) is dict:
        require(type(actual) is dict and actual.keys() == expected.keys(), 'SCHEMA', 'closed record keys')
        for key in expected: shape_and_scalars(actual[key], expected[key])
    elif type(expected) is list:
        require(type(actual) is list and len(actual) == len(expected), 'DIMENSION', 'complete list dimension')
        for a, b in zip(actual, expected): shape_and_scalars(a, b)
    elif type(expected) is int:
        require(type(actual) is int, 'DIMENSION', 'plain structural integer')
    elif type(expected) is bool:
        require(type(actual) is bool, 'DIMENSION', 'plain boolean')
    elif type(expected) is str:
        require(type(actual) is str, 'EXACT', 'plain string')
        if RATIONAL.fullmatch(expected): scalar(actual)
    else:
        raise PrimaryError('SCHEMA', 'unsupported expected type')


def require_psd_2x2(matrix):
    require(type(matrix) is list and len(matrix) == 2 and
            all(type(row) is list and len(row) == 2 for row in matrix), 'DIMENSION', 'two by two matrix')
    a, b, c, d = [scalar(x) for row in matrix for x in row]
    require(b == c and a >= 0 and d >= 0 and minus(times(a, d), times(b, c)) >= 0,
            'PSD', 'symmetric PSD two by two covariance')
    return None


def compare_result(given, expected):
    # expected is exclusively the caller's fresh enumeration, never a user oracle.
    require(type(given) is dict and given.keys() == expected.keys(), 'SCHEMA', 'closed scientific root')
    for key, code in (('schema', 'SCHEMA'), ('phase', 'PHASE'), ('status', 'RESULT'), ('method', 'SCOPE')):
        compare(given[key], expected[key], code, 'scientific ' + key)
    compare(given['groups'], expected['groups'], 'INVENTORY', 'complete group order')
    for key in ('cases', 'bounds'):
        require(type(given[key]) is list and all(type(x) is dict for x in given[key]), 'INVENTORY', 'record inventory')
        compare([x.get('id') for x in given[key]], [x['id'] for x in expected[key]], 'INVENTORY', 'complete ' + key)
    compare(given['limitations'], expected['limitations'], 'SCOPE', 'scientific limitations')
    shape_and_scalars(given['cases'], expected['cases'])
    shape_and_scalars(given['bounds'], expected['bounds'])
    covariance_fields = ('raw_covariance', 'window_marginal_covariances', 'stacked_output_covariance',
                         'cross_blocks', 'mean_output_covariance', 'centered_covariance_average')
    for current, reference in zip(given['cases'], expected['cases']):
        for dim in ('M', 'T', 'stride', 'n', 'raw_length', 'latent_dimension', 'output_dimension'):
            compare(current['model'][dim], reference['model'][dim], 'DIMENSION', 'fixed model dimension')
        if current['id'] in ('Q02_white_two', 'Q03_periodic_two'):
            require_psd_2x2(current['stacked_output_covariance'])
        compare(current['model'], reference['model'], 'MODEL', 'declared complete model')
        compare(current['selectors_M'], reference['selectors_M'], 'SHARED_INDEX', 'fixed shared raw M selectors')
        compare(current['selectors_T'], reference['selectors_T'], 'CROP', 'first T crop')
        compare(current['output_map'], reference['output_map'], 'OPERATOR', 'fixed output map')
        compare(current['raw_mean'], reference['raw_mean'], 'MEAN_TERM', 'complete raw mean')
        for key in covariance_fields:
            compare(current[key], reference[key], 'COVARIANCE_MODEL', 'declared model ' + key)
        for key in ('stacked_output_mean', 'mean_dispersion'):
            compare(current[key], reference[key], 'MEAN_TERM', 'declared mean ' + key)
        compare(current['sign_count'], reference['sign_count'], 'ENUMERATION', 'complete sign cube count')
        for key in ('covariance_contribution', 'expected_V', 'direct_average_V', 'expected_U', 'mean_output_energy'):
            compare(current[key], reference[key], 'ENERGY', 'complete exact energy ' + key)
    for current, reference in zip(given['bounds'], expected['bounds']):
        for dim in ('n', 'output_dimension'):
            if dim in reference: compare(current[dim], reference[dim], 'DIMENSION', 'standalone nuisance dimension')
        if current['id'] == 'Q12_calibrated_constant':
            compare(current['constant_annihilation_claim'], False, 'CALIBRATION', 'calibrated constant claim')
        if current['id'] == 'Q12_covariance_error':
            require(scalar(current['eta']) >= 0, 'BOUND', 'eta must be nonnegative')
        compare(current, reference, 'BOUND', 'full exact nuisance bound')
    return {'status': 'all_fields_primary_match', 'cases': 9, 'bounds': 3, 'groups': 12}
