"""RI73 fixed eight-row covariance under explicitly synthetic unit-white noise.

--fixtures never designs admitted coefficients or reconstructs their adjoints.
The default integration requires prior independent source review and root freeze.
No observations, PRNG, filtering of samples, file writes or fitted covariance.
All new derived rational operations check the frozen 262144-bit result cap.
"""
import argparse
import copy
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
import math
from pathlib import Path
import platform
import re
import stat
import sys


N, L, T = 2769, 4096, 10961
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
DIM, BITS, MAX_RESULT = 8, 262144, 64 * 1024 * 1024
RHO_LIMIT = F(1, 10**12)
CDF_LIMIT, ORACLE_LIMIT = F(1, 10**10), F(1, 2**100)
VERSIONS = {'python': '3.11.6', 'numpy': '2.1.3', 'scipy': '1.14.1', 'h5py': '3.12.1'}
DEPENDENCIES = {
    'design': {'path': 'gwosc_noise_operator_covariance_v1/DESIGN.md', 'bytes': 29545,
        'sha256': '08e6e99d0f884e26b9b4a2422789431d6d6acf077dbb751dd73144b5c6409cd6'},
    'check60': {'path': 'gwosc_context_operator_v2/check.py', 'bytes': 38088,
        'sha256': 'a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02'},
    'engine': {'path': 'gwosc_context_operator_v2/operator.py', 'bytes': 30531,
        'sha256': 'ef8169986977c533f549f2ca59b5f72224464db616d8303c451d6a29f22df6af'},
    'oracle': {'path': 'gwosc_context_operator_v1/oracle.py', 'bytes': 9484,
        'sha256': '37f3dea8ccbc495e90123b51e35150c8e5324c18c598954182e76943a285a651'},
    'qualification60': {'path': 'gwosc_context_operator_v2/QUALIFICATION_REPORT.json', 'bytes': 9413345,
        'sha256': '1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f'},
    'failed_predecessor': {'path': 'gwosc_context_operator_v1/QUALIFICATION_REPORT.json', 'bytes': 161816,
        'sha256': '7dfbc8cac7e631a9c3663bca2b288b134d6cea03f1d0ca14c8334746761a808a'},
    'filtering': {'path': 'gwosc_nominal_processing_v1/filtering.py', 'bytes': 8805,
        'sha256': '9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be'},
    'reference': {'path': 'gwosc_nominal_processing_v1/reference.py', 'bytes': 7253,
        'sha256': 'c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305'},
    'coefficients': {'path': 'gwosc_nominal_processing_v1/COEFFICIENTS.json', 'bytes': 7698,
        'sha256': '700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0'},
    'prior_qualification': {'path': 'gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json', 'bytes': 107468,
        'sha256': '2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3'},
    'recipe': {'path': 'gwosc_nominal_display_v1/RECIPE.md', 'bytes': 14014,
        'sha256': '872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a'},
    'prior_design': {'path': 'gwosc_context_sensitivity_v1/DESIGN.md', 'bytes': 21702,
        'sha256': 'e672cea6c5f06c5927b54b0021636793c14b01e8efe57aa8e719fd464a527e45'},
    'window_design': {'path': 'gwosc_observed_context_v1/DESIGN.md', 'bytes': 19255,
        'sha256': '636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2'},
    'noise_design': {'path': 'gwosc_context_noise_v1/DESIGN.md', 'bytes': 24027,
        'sha256': '74581df2266277b5ff12c9d45d110baf191f99dfbc7db8ea4b3810affa914921'},
}
ERRORS = (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rat(value):
    require(type(value) is F, 'exact Fraction required')
    require(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= BITS,
            'Fraction resource limit')
    return value


def add(a, b): return rat(rat(a) + rat(b))
def sub(a, b): return rat(rat(a) - rat(b))
def mul(a, b): return rat(rat(a) * rat(b))
def div(a, b):
    require(rat(b) != 0, 'division by zero')
    return rat(rat(a) / b)
def neg(a): return rat(-rat(a))
def absolute(a): return rat(abs(rat(a)))


def total(values):
    result = F(0)
    for value in values:
        result = add(result, value)
    return result


def scalar(value):
    value = rat(value)
    return [format(value.numerator, 'x'), format(value.denominator, 'x')]


def decode_scalar(value):
    require(type(value) is list and len(value) == 2, 'exact scalar pair required')
    for index, item in enumerate(value):
        require(type(item) is str and len(item) <= (BITS + 3) // 4 + (index == 0),
                'hex scalar length limit')
        pattern = r'(?:0|-?[1-9a-f][0-9a-f]*)' if index == 0 else r'[1-9a-f][0-9a-f]*'
        require(re.fullmatch(pattern, item) is not None, 'noncanonical hexadecimal scalar')
    n, d = int(value[0], 16), int(value[1], 16)
    require(max(abs(n).bit_length(), d.bit_length()) <= BITS, 'Fraction resource limit')
    result = rat(F(n, d))
    require(scalar(result) == value, 'unreduced hexadecimal scalar')
    return result


def encoded(value):
    if type(value) is F:
        return scalar(value)
    if type(value) in (list, tuple):
        return [encoded(v) for v in value]
    if type(value) is dict:
        return {k: encoded(v) for k, v in value.items()}
    return value


def canonical(value):
    return json.dumps(encoded(value), sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False).encode('ascii')


def identity(body):
    require(type(body) is bytes, 'identity requires retained bytes')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def equal(actual, expected, label):
    require(canonical(actual) == canonical(expected), label)


def array_identity(values, label, domain):
    return {'schema': 'ri73-exact-array-v1', 'label': label, 'domain': domain,
            **identity(canonical({'schema': 'ri73-exact-array-v1', 'label': label,
                                  'domain': domain, 'values': values}))}


def interval(value):
    require(type(value) in (list, tuple) and len(value) == 2, 'interval pair required')
    lo, hi = map(rat, value)
    require(lo <= hi, 'reversed interval')
    return lo, hi


def iadd(a, b):
    a, b = interval(a), interval(b)
    return add(a[0], b[0]), add(a[1], b[1])


def isub(a, b):
    a, b = interval(a), interval(b)
    return sub(a[0], b[1]), sub(a[1], b[0])


def imul(a, b):
    a, b = interval(a), interval(b)
    values = tuple(mul(x, y) for x in a for y in b)
    return min(values), max(values)


def isquare(a):
    lo, hi = interval(a)
    values = mul(lo, lo), mul(hi, hi)
    return F(0) if lo <= 0 <= hi else min(values), max(values)


def isum(values):
    result = F(0), F(0)
    for value in values:
        result = iadd(result, value)
    return result


def vector(values, length=None, maximum=T):
    require(type(maximum) is int and 0 < maximum <= T and
            (length is None or type(length) is int and 0 < length <= maximum), 'invalid vector dimension control')
    require(type(values) in (tuple, list) and 0 < len(values) <= maximum and
            (length is None or len(values) == length), 'vector dimensions differ')
    return tuple(rat(v) for v in values)


def matrix(values, rows=None, columns=None, maximum_columns=T):
    require(rows is None or type(rows) is int and 0 < rows <= DIM, 'invalid matrix row control')
    require(type(values) in (tuple, list) and 0 < len(values) <= DIM and
            (rows is None or len(values) == rows), 'matrix row dimensions differ')
    first = vector(values[0], columns, maximum_columns)
    return (first,) + tuple(vector(row, len(first), maximum_columns) for row in values[1:])


def box_matrix(values, rows=None, columns=None):
    require(rows is None or type(rows) is int and 0 < rows <= DIM, 'invalid interval row control')
    require(columns is None or type(columns) is int and 0 < columns <= T, 'invalid interval column control')
    require(type(values) in (tuple, list) and 0 < len(values) <= DIM and
            (rows is None or len(values) == rows), 'interval matrix row dimensions differ')
    result = []
    width = columns
    for row in values:
        require(type(row) in (tuple, list) and 0 < len(row) <= T and
                (width is None or len(row) == width), 'interval matrix column dimensions differ')
        width = len(row)
        result.append(tuple(interval(v) for v in row))
    return tuple(result)


def transpose(a): return tuple(zip(*a, strict=True))
def eye(n): return tuple(tuple(F(int(i == j)) for j in range(n)) for i in range(n))
def zeros(n, m): return tuple(tuple(F(0) for _ in range(m)) for _ in range(n))
def singleton(a): return tuple(tuple((v, v) for v in row) for row in matrix(a))


def dot(a, b):
    require(len(a) == len(b), 'dot dimensions differ')
    return total(mul(x, y) for x, y in zip(a, b, strict=True))


def matmul(a, b):
    a, b = matrix(a), matrix(b, maximum_columns=DIM)
    require(len(a[0]) == len(b), 'matrix product dimensions differ')
    return tuple(tuple(dot(row, col) for col in transpose(b)) for row in a)


def matrix_sub(a, b):
    a, b = matrix(a), matrix(b, len(a), len(a[0]))
    return tuple(tuple(sub(x, y) for x, y in zip(u, v, strict=True)) for u, v in zip(a, b, strict=True))


def matrix_scale(a, scale):
    return tuple(tuple(mul(v, scale) for v in row) for row in matrix(a))


def symmetric(a, label='matrix'):
    a = matrix(a, columns=len(a), maximum_columns=DIM)
    require(a == transpose(a), label + ' is asymmetric')
    return a


def midpoint_radii(bounds):
    bounds = box_matrix(bounds)
    return (tuple(tuple(div(add(lo, hi), F(2)) for lo, hi in row) for row in bounds),
            tuple(tuple(div(sub(hi, lo), F(2)) for lo, hi in row) for row in bounds))


def midpoint_gram(m):
    m = matrix(m)
    result = [list(row) for row in zeros(len(m), len(m))]
    for i in range(len(m)):
        for j in range(i, len(m)):
            result[i][j] = result[j][i] = dot(m[i], m[j])
    return tuple(map(tuple, result))


def error_matrix(m, radii):
    m = matrix(m)
    radii = matrix(radii, len(m), len(m[0]))
    require(all(v >= 0 for row in radii for v in row), 'negative coefficient radius')
    h = [list(row) for row in zeros(len(m), len(m))]
    for i in range(len(m)):
        for j in range(i, len(m)):
            h[i][j] = h[j][i] = total(add(add(mul(absolute(x), s), mul(r, absolute(y))), mul(r, s))
                for x, r, y, s in zip(m[i], radii[i], m[j], radii[j], strict=True))
    return tuple(map(tuple, h))


def gram_interval(a, b=None):
    a = box_matrix(a)
    same = b is None
    b = a if same else box_matrix(b, columns=len(a[0]))
    require(len(a) == len(b), 'cross covariance row dimensions differ')
    zero = F(0), F(0)
    result = [[zero for _ in b] for _ in a]
    for i in range(len(a)):
        for j in range(i if same else 0, len(b)):
            if same and i == j:
                value = isum(isquare(x) for x in a[i])
            else:
                value = isum(imul(x, y) for x, y in zip(a[i], b[j], strict=True))
            result[i][j] = value
            if same:
                result[j][i] = value
    return tuple(map(tuple, result))


def matrix_rank(a):
    a = [list(row) for row in matrix(a, maximum_columns=DIM)]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [div(x, scale) for x in a[rank]]
        for i in range(rank + 1, len(a)):
            scale = a[i][col]
            a[i] = [sub(x, mul(scale, y)) for x, y in zip(a[i], a[rank], strict=True)]
        rank += 1
        if rank == len(a):
            break
    return rank


def psd(a):
    a = [list(row) for row in symmetric(a)]
    rank = 0
    for k in range(len(a)):
        require(a[k][k] >= 0, 'negative PSD pivot')
        if a[k][k] == 0:
            require(all(a[j][k] == 0 for j in range(k, len(a))), 'zero PSD pivot has nonzero column')
            continue
        rank += 1
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[i][j] = a[j][i] = sub(a[i][j], div(mul(a[i][k], a[j][k]), a[k][k]))
    return rank


def ldl(a):
    a = symmetric(a, 'Gram')
    n = len(a)
    lower = [list(row) for row in eye(n)]
    pivots = []
    for j in range(n):
        pivot = sub(a[j][j], total(mul(mul(lower[j][k], lower[j][k]), pivots[k]) for k in range(j)))
        require(pivot >= 0, 'negative Gram pivot after positive predecessors')
        if pivot == 0:
            return {'positive': False, 'stopped_index': j, 'stopped_pivot': pivot,
                    'pivots': tuple(pivots), 'lower_partial': tuple(map(tuple, lower))}
        pivots.append(pivot)
        for i in range(j + 1, n):
            lower[i][j] = div(sub(a[i][j], total(mul(mul(lower[i][k], lower[j][k]), pivots[k])
                                                 for k in range(j))), pivot)
    lower = tuple(map(tuple, lower))
    diagonal = tuple(tuple(pivots[i] if i == j else F(0) for j in range(n)) for i in range(n))
    reconstructed = matmul(matmul(lower, diagonal), transpose(lower))
    equal(reconstructed, a, 'LDL reconstruction differs')
    return {'positive': True, 'lower': lower, 'pivots': tuple(pivots), 'reconstruction': reconstructed}


def inverse_from_ldl(a, factor):
    a = symmetric(a, 'Gram')
    require(factor.get('positive') is True, 'positive LDL required')
    lower, pivots = matrix(factor['lower'], len(a), len(a)), vector(factor['pivots'], len(a), DIM)
    require(all(v > 0 for v in pivots), 'positive LDL pivots required')
    d = tuple(tuple(pivots[i] if i == j else F(0) for j in range(len(a))) for i in range(len(a)))
    equal(matmul(matmul(lower, d), transpose(lower)), a, 'LDL reconstruction differs')
    equal(tuple(lower[i][i] for i in range(len(a))), tuple(F(1) for _ in a), 'unit lower diagonal required')
    require(all(lower[i][j] == 0 for i in range(len(a)) for j in range(i + 1, len(a))), 'lower triangular factor required')
    columns = []
    for selected in range(len(a)):
        y = []
        for i in range(len(a)):
            y.append(sub(F(int(i == selected)), total(mul(lower[i][j], y[j]) for j in range(i))))
        z = [div(v, pivot) for v, pivot in zip(y, pivots, strict=True)]
        x = [F(0) for _ in a]
        for i in range(len(a) - 1, -1, -1):
            x[i] = sub(z[i], total(mul(lower[j][i], x[j]) for j in range(i + 1, len(a))))
        columns.append(tuple(x))
    inverse = symmetric(transpose(columns), 'inverse')
    left, right = matmul(a, inverse), matmul(inverse, a)
    equal(left, eye(len(a)), 'left inverse identity failed')
    equal(right, eye(len(a)), 'right inverse identity failed')
    return inverse, left, right


def norm_infinity(a): return max(total(absolute(v) for v in row) for row in matrix(a))


class CovarianceComputationError(ValueError):
    """Retain completed exact fields when a later bounded calculation fails."""
    def __init__(self, stage, completed, error):
        super().__init__('covariance calculation failed at ' + stage + ': ' + str(error))
        self.stage = stage
        self.completed = completed
        self.original_error_type = type(error).__name__
        self.original_error = str(error)


def covariance_certificate(bounds):
    bounds = box_matrix(bounds)
    result = {'mathematical_gate': False, 'accuracy_gate': False, 'rho_limit': RHO_LIMIT}
    stage = 'coefficient_midpoints'
    try:
        m, radii = midpoint_radii(bounds)
        stage = 'midpoint_Gram'
        g = midpoint_gram(m)
        result['G'] = g
        stage = 'coefficient_error_matrix'
        h = error_matrix(m, radii)
        result['H'] = h
        stage = 'error_norm_and_mean_square'
        delta = max(total(row) for row in h)
        result['delta'] = delta
        result['eta2'] = total(mul(v, v) for row in radii for v in row)
        stage = 'exact_LDL'
        factor = ldl(g)
        result['ldl'] = factor
        if not factor['positive']:
            result['status'] = 'unresolved_by_fixed_gate'
            result['reason'] = 'midpoint Gram positive pivots not proved; true covariance rank not inferred'
            return m, radii, result
        stage = 'exact_inverse'
        inverse, left, right = inverse_from_ldl(g, factor)
        result.update(inverse=inverse, left_inverse_product=left, right_inverse_product=right)
        stage = 'relative_error_norm'
        gamma = norm_infinity(inverse)
        result['gamma'] = gamma
        rho = mul(delta, gamma)
        result.update(rho=rho, mathematical_gate=rho < 1, accuracy_gate=rho <= RHO_LIMIT)
        if rho >= 1:
            result.update(status='unresolved_by_fixed_gate', reason='relative error sufficient gate did not prove rho<1')
        else:
            stage = 'inverse_error_bounds'
            result.update(status='certified' if rho <= RHO_LIMIT else 'accuracy_failed', rank=len(g))
            result['inverse_error_norm_bound'] = div(mul(rho, gamma), sub(F(1), rho))
            result['inverse_lower'] = matrix_scale(inverse, div(F(1), add(F(1), rho)))
            result['inverse_upper'] = matrix_scale(inverse, div(F(1), sub(F(1), rho)))
        return m, radii, result
    except ERRORS as error:
        result['status'] = 'calculation_failed'
        result['complete_certificate'] = False
        raise CovarianceComputationError(stage, result, error) from error


def quadratic(y, inverse):
    inverse = symmetric(inverse, 'inverse')
    y = vector(y, len(inverse), DIM)
    result = dot(y, tuple(dot(row, y) for row in inverse))
    require(result >= 0, 'negative quadratic')
    return result


def output_score(y, error, inverse, rho, gamma):
    inverse = symmetric(inverse, 'inverse')
    y, error = vector(y, len(inverse), DIM), vector(error, len(inverse), DIM)
    require(all(v >= 0 for v in error), 'negative output error')
    require(F(0) <= rat(rho) < 1, 'score requires 0<=rho<1')
    require(rat(gamma) == norm_infinity(inverse), 'incorrect inverse norm bound')
    q = quadratic(y, inverse)
    e1, y1 = total(error), total(absolute(v) for v in y)
    bound = div(mul(gamma, add(mul(mul(F(2), y1), e1), mul(e1, e1))), sub(F(1), rho))
    lower, upper = div(q, add(F(1), rho)), div(q, sub(F(1), rho))
    result = max(F(0), sub(lower, bound)), add(upper, bound)
    require(F(0) <= result[0] <= result[1], 'invalid score enclosure')
    return {'point_output': y, 'component_error_bounds': error, 'point_quadratic': q,
            'unperturbed_quadratic_interval': (lower, upper), 'E1': e1, 'Y1': y1,
            'score_error_bound': bound, 'score_interval': result}


def coefficient_probe(z, m, radii, certificate):
    m = matrix(m)
    radii, z = matrix(radii, len(m), len(m[0])), vector(z, len(m[0]))
    require(all(v >= 0 for row in radii for v in row), 'negative coefficient radius')
    require(certificate['mathematical_gate'] is True, 'proved covariance inverse required')
    y, error = [], []
    # One shared row-coordinate visit accumulates both sums from design (8).
    for row, radius in zip(m, radii, strict=True):
        point, bound = F(0), F(0)
        for coefficient, width, value in zip(row, radius, z, strict=True):
            point = add(point, mul(coefficient, value))
            bound = add(bound, mul(width, absolute(value)))
        y.append(point)
        error.append(bound)
    return output_score(y, error, certificate['inverse'], certificate['rho'], certificate['gamma'])


def cdf8(argument):
    argument = rat(argument)
    require(argument >= 0, 'negative CDF argument')
    u = div(argument, F(2))
    require(u < 130, 'exponential series argument out of range')
    term, series = F(1), F(1)
    for j in range(1, 129):
        term = div(mul(term, u), F(j))
        series = add(series, term)
    first = div(mul(term, u), F(129))
    remainder = div(first, sub(F(1), div(u, F(130))))
    exp_bounds = div(F(1), add(series, remainder)), div(F(1), series)
    term, polynomial = F(1), F(1)
    for j in range(1, 4):
        term = div(mul(term, u), F(j))
        polynomial = add(polynomial, term)
    bounds = sub(F(1), mul(polynomial, exp_bounds[1])), sub(F(1), mul(polynomial, exp_bounds[0]))
    require(F(0) <= bounds[0] <= bounds[1] <= 1, 'CDF interval outside unit range')
    require(sub(bounds[1], bounds[0]) <= ORACLE_LIMIT, 'CDF oracle width failed')
    return {'argument': argument, 'exponential_argument': u, 'series_degree': 128,
            'summand_count': 129, 'remainder_first_degree': 129, 'series': series,
            'remainder_bound': remainder, 'negative_exponential_interval': exp_bounds,
            'tail_polynomial': polynomial, 'interval': bounds, 'width_limit': ORACLE_LIMIT}


def law_comparison(rho):
    require(F(0) <= rat(rho) <= RHO_LIMIT, 'CDF comparison requires admitted rho')
    lower = cdf8(div(F(16), add(F(1), RHO_LIMIT)))
    upper = cdf8(div(F(16), sub(F(1), RHO_LIMIT)))
    bounds = lower['interval'][0], upper['interval'][1]
    width = sub(bounds[1], bounds[0])
    proof_width = add(div(mul(F(32), RHO_LIMIT), sub(F(1), mul(RHO_LIMIT, RHO_LIMIT))), mul(F(2), ORACLE_LIMIT))
    require(F(0) <= width <= proof_width < CDF_LIMIT, 'probability comparison width failed')
    return {'threshold': F(16), 'rho_bar': RHO_LIMIT, 'actual_rho': rho,
            'lower_CDF': lower, 'upper_CDF': upper, 'probability_interval': bounds,
            'width': width, 'width_limit': CDF_LIMIT, 'density_based_width_bound': proof_width,
            'sampling_performed': False, 'interpretation': 'Conditional ideal Gaussian law only; no detector noise or finite sampler qualification.'}


def validate_pseudoinverse(a, inverse, rank):
    a, inverse = symmetric(a), symmetric(inverse, 'pseudoinverse')
    require(len(a) == len(inverse), 'pseudoinverse dimensions differ')
    require(type(rank) is int and 0 <= rank <= len(a), 'invalid exact rank')
    require(psd(a) == matrix_rank(a) == rank, 'incorrect exact rank')
    av, va = matmul(a, inverse), matmul(inverse, a)
    equal(matmul(av, a), a, 'Moore-Penrose identity 1 failed')
    equal(matmul(va, inverse), inverse, 'Moore-Penrose identity 2 failed')
    equal(av, transpose(av), 'Moore-Penrose identity 3 failed')
    equal(va, transpose(va), 'Moore-Penrose identity 4 failed')
    return av


def support_score(y, a, inverse, rank):
    projector = validate_pseudoinverse(a, inverse, rank)
    y = vector(y, len(projector), DIM)
    require(tuple(dot(row, y) for row in projector) == y, 'residual outside covariance support')
    return quadratic(y, inverse)


def cross_consistency(a, p, q, certificate):
    a = box_matrix(a)
    p, q = box_matrix(p, len(a), len(a[0])), box_matrix(q, len(a), len(a[0]))
    completed = {}
    stage = 'direct_interval_Gram'
    try:
        direct = gram_interval(a)
        completed['direct_A_Gram'] = direct
        stage = 'interval_QQ'
        qq = gram_interval(q)
        completed['QQ'] = qq
        stage = 'interval_PP'
        pp = gram_interval(p)
        completed['PP'] = pp
        stage = 'interval_QP'
        qp = gram_interval(q, p)
        completed.update(QP=qp, PQ=transpose(qp))
        stage = 'cross_expansion'
        expansion = tuple(tuple(isub(isub(iadd(qq[i][j], pp[i][j]), qp[i][j]), qp[j][i])
                                for j in range(len(a))) for i in range(len(a)))
        require(expansion == transpose(expansion), 'cross expansion is asymmetric')
        completed['cross_expansion'] = expansion
        stage = 'covariance_intersections'
        g, h = certificate['G'], certificate['H']
        intersections = []
        for i in range(len(a)):
            row = []
            for j in range(len(a)):
                gh = sub(g[i][j], h[i][j]), add(g[i][j], h[i][j])
                bounds = max(direct[i][j][0], expansion[i][j][0], gh[0]), min(direct[i][j][1], expansion[i][j][1], gh[1])
                require(bounds[0] <= bounds[1], 'covariance enclosure routes disagree')
                row.append(bounds)
            intersections.append(tuple(row))
        completed['consistency_intersection'] = tuple(intersections)
        return completed
    except ERRORS as error:
        raise CovarianceComputationError(stage, completed, error) from error


def pin_only(pin):
    require(type(pin) is dict and type(pin.get('bytes')) is int and 0 < pin['bytes'] <= MAX_RESULT and
            type(pin.get('sha256')) is str and re.fullmatch(r'[0-9a-f]{64}', pin['sha256']), 'invalid frozen pin')
    return {key: pin[key] for key in ('bytes', 'sha256')}


def verify_bytes(body, pin, label):
    equal(identity(body), pin_only(pin), label + ': snapshot identity differs')
    return body


def bound_bytes(path, pin, label):
    expected = pin_only(pin)
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == expected['bytes'], label + ': pinned regular file required')
        with path.open('rb') as stream:
            body = stream.read(expected['bytes'] + 1)
    except OSError as error:
        raise ValueError(label + ': cannot read pinned file') from error
    return verify_bytes(body, expected, label)


def parse_json(body):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise ValueError('nonfinite JSON constant')
    def finite_number(value):
        number = float(value)
        require(math.isfinite(number), 'nonfinite JSON number')
        return number
    return json.loads(body, object_pairs_hook=pairs, parse_constant=invalid, parse_float=finite_number)


def load_module(name, path, body):
    spec = importlib.util.spec_from_file_location('ri73_bound_' + name, path)
    require(spec is not None and spec.loader is not None, 'cannot load bound helper')
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(body, str(path), 'exec'), module.__dict__)
    return module


def runtime():
    import numpy as np
    import scipy
    import h5py
    return {'versions': {'python': platform.python_version(), 'numpy': np.__version__,
                         'scipy': scipy.__version__, 'h5py': h5py.__version__},
            'python_implementation': platform.python_implementation(), 'python_build': sys.version,
            'operating_system': platform.system(), 'os_release': platform.release(),
            'os_version': platform.version(), 'machine': platform.machine(), 'byte_order': sys.byteorder,
            'hdf5_version': h5py.version.hdf5_version, 'numpy_configuration': np.show_config(mode='dicts')}


def validate_runtime(current, qualified):
    equal(current.get('versions'), VERSIONS, 'runtime versions differ')
    equal(current, qualified, 'full qualified runtime differs')


def validate_prior(prior, bodies):
    require(prior.get('schema_version') == 'ri44-synthetic-qualification-v1' and
            prior.get('status') == 'all_synthetic_gates_passed', 'RI44 status differs')
    equal(prior.get('gate_counts'), {'total': 105, 'passed': 105, 'failed': 0}, 'RI44 gate count differs')
    # RI44 uses the same compact JSON conventions for this manifest.
    require(canonical(prior['coefficient_manifest']) == bodies['coefficients'], 'RI44 manifest differs')
    require(prior['coefficient_manifest_sha256'] == DEPENDENCIES['coefficients']['sha256'], 'RI44 manifest pin differs')
    for key in ('filtering', 'reference'):
        require(prior['source_identity'][key]['sha256'] == DEPENDENCIES[key]['sha256'], 'RI44 source identity differs')
    require(prior['source_identity']['accepted_recipe_sha256'] == DEPENDENCIES['recipe']['sha256'], 'RI44 recipe identity differs')


def admission():
    """Bind the complete closure and metadata; no admitted coefficient design."""
    base = Path(__file__).resolve().parent.parent
    bodies = {name: bound_bytes(base / pin['path'], pin, name) for name, pin in DEPENDENCIES.items()}
    own = Path(__file__).read_bytes()
    qualification = parse_json(bodies['qualification60'])
    prior, predecessor = parse_json(bodies['prior_qualification']), parse_json(bodies['failed_predecessor'])
    current = runtime()
    validate_runtime(current, qualification.get('runtime'))
    # All dependency bodies and runtime are bound before any helper execution.
    modules = {name: load_module(name, base / DEPENDENCIES[name]['path'], bodies[name])
               for name in ('check60', 'engine', 'oracle')}
    check, engine = modules['check60'], modules['engine']
    inherited = {pin['path']: pin_only(pin) for pin in check.DEPENDENCIES.values()}
    inherited[DEPENDENCIES['engine']['path']] = pin_only(check.ENGINE_PIN)
    inherited[check.REUSED_ORACLE_PATH] = pin_only(check.ORACLE_PIN)
    current_pins = {pin['path']: pin_only(pin) for pin in DEPENDENCIES.values()}
    require(all(current_pins.get(path) == pin for path, pin in inherited.items()), 'transitive source closure differs')
    check.validate_predecessor(predecessor)
    validate_prior(prior, bodies)
    arithmetic = engine.arithmetic_contract()
    check.validate_qualification(qualification, {'runtime': current, 'arithmetic': arithmetic})
    return {'base': base, 'bodies': bodies, 'own': own, 'runtime': current,
            'modules': modules, 'qualification': qualification, 'arithmetic': arithmetic,
            'numeric': None, 'rows': None}


def recheck(admitted):
    require(Path(__file__).read_bytes() == admitted['own'], 'checker source changed')
    for name, pin in DEPENDENCIES.items():
        require(bound_bytes(admitted['base'] / pin['path'], pin, name) == admitted['bodies'][name], 'source snapshot changed')
    validate_runtime(runtime(), admitted['runtime'])
    check = admitted['modules']['check60']
    check.validate_qualification(admitted['qualification'], {'runtime': admitted['runtime'], 'arithmetic': admitted['arithmetic']})
    if admitted['numeric'] is not None:
        numeric = admitted['numeric']
        check.check_coefficients(numeric)
        validate_manifest(numeric['production'].coefficient_manifest(numeric['stages']), admitted['bodies']['coefficients'])
        actual_fractions = tuple(tuple(tuple(rat(F.from_float(float(v))) for v in section)
                                       for section in stage['sos'].tolist()) for stage in numeric['stages'])
        equal(numeric['fraction_stages'], actual_fractions, 'exact coefficient state changed')
        validate_padding(numeric['padlens'])
        equal(numeric['padlens'], tuple(stage['padlen'] for stage in numeric['stages']), 'padding state changed')
        equal(numeric['arithmetic'], admitted['arithmetic'], 'arithmetic state changed')


def validate_manifest(manifest, body):
    require(canonical(manifest) == body, 'coefficient manifest, stage order or padding differs')


def validate_padding(padlens):
    require(type(padlens) is tuple and all(type(value) is int for value in padlens) and
            padlens == (27,) + (9,) * 16, 'fixed padding differs')


def prepare_numeric(admitted):
    """Full integration only; never called by fixtures-only execution."""
    recheck(admitted)
    base, bodies, modules = admitted['base'], admitted['bodies'], admitted['modules']
    production = load_module('filtering', base / DEPENDENCIES['filtering']['path'], bodies['filtering'])
    reference = load_module('reference', base / DEPENDENCIES['reference']['path'], bodies['reference'])
    stages = production.design_stages()
    numeric = {'production': production, 'reference': reference, 'engine': modules['engine'],
               'oracle': modules['oracle'], 'stages': stages, 'coefficient_bytes': bodies['coefficients'],
               'runtime': admitted['runtime'], 'arithmetic': admitted['arithmetic']}
    modules['check60'].check_coefficients(numeric)
    validate_manifest(production.coefficient_manifest(stages), bodies['coefficients'])
    numeric['fraction_stages'] = tuple(tuple(tuple(rat(F.from_float(float(v))) for v in section)
                                             for section in stage['sos'].tolist()) for stage in stages)
    numeric['padlens'] = tuple(stage['padlen'] for stage in stages)
    validate_padding(numeric['padlens'])
    admitted['numeric'] = numeric
    recheck(admitted)
    return numeric


def row_inventory(rows):
    require(type(rows) is tuple and tuple(row.get('row') for row in rows) == ROWS,
            'complete fixed row inventory required')
    require(all(type(row['row']) is int for row in rows), 'integer row identity required')


def immutable_rows(rows):
    row_inventory(rows)
    return tuple((row['row'], tuple(interval(pair) for pair in row['short']['intervals']),
                  tuple(interval(pair) for pair in row['long']['intervals'])) for row in rows)


def snapshot_record(snapshot):
    require(type(snapshot) is tuple and len(snapshot) == len(ROWS), 'immutable complete snapshot required')
    records = []
    for expected, entry in zip(ROWS, snapshot, strict=True):
        require(type(entry) is tuple and len(entry) == 3 and type(entry[0]) is int and entry[0] == expected,
                'immutable snapshot row order differs')
        _, short, long = entry
        require(type(short) is tuple and type(long) is tuple and len(short) == N and len(long) == T,
                'immutable snapshot vector dimensions differ')
        require(all(type(pair) is tuple for pair in (*short, *long)), 'immutable snapshot endpoints required')
        records.append({'row': expected, 'short': tuple(interval(v) for v in short),
                        'long': tuple(interval(v) for v in long)})
    return {'schema': 'ri73-reconstructed-intervals-v1', 'dimensions': {'N': N, 'L': L, 'T': T},
            'row_order': list(ROWS), 'rows': records}


def row_state(rows, check):
    snapshot = snapshot_record(immutable_rows(rows))
    return identity(canonical({'snapshot': snapshot, 'summaries': [check.row_summary(row) for row in rows]}))


def reconcile_rows(rows, expected, check):
    row_inventory(rows)
    require(type(expected) is dict and set(expected) == set(ROWS), 'qualification certificate row inventory differs')
    for row in rows:
        require(len(row['short']['intervals']) == N and len(row['long']['intervals']) == T,
                'reconstructed interval lengths differ')
        equal(check.row_summary(row), expected[row['row']], 'recomputed certificate differs from qualification')
        check.require_width(row['gain'], div(max(F(1), rat(row['gain'][1])), F(10**12)), 'gain')
        check.validate_row_status(row['operator_status'], row['b'])
    return True


def reconstruct(admitted, row_observer=None):
    numeric = prepare_numeric(admitted)
    check = admitted['modules']['check60']
    rows = check.build_rows(numeric)
    previous = {gate['detail']['row']['row']: gate['detail']['row']
                for gate in admitted['qualification']['gates'] if gate['id'].startswith('enclosure:')}
    reconcile_rows(rows, previous, check)
    before = row_state(rows, check)
    recheck(admitted)
    if row_observer is not None:
        require(callable(row_observer), 'row observer must be callable')
        require(row_observer(immutable_rows(rows)) is None, 'row observer must return None')
    equal(row_state(rows, check), before, 'reconciled row state changed')
    recheck(admitted)
    admitted['rows'] = rows
    return rows, before


def operators_from_rows(rows):
    row_inventory(rows)
    p, q, a, sums = [], [], [], []
    for row in rows:
        short = tuple(interval(v) for v in row['short']['intervals'])
        long = tuple(interval(v) for v in row['long']['intervals'])
        require(len(short) == N and len(long) == T, 'reconstructed interval lengths differ')
        center = tuple(isub(v, s) for v, s in zip(long[L:L + N], short, strict=True))
        outside = long[:L] + long[L + N:]
        equal(center, row['a'], 'central A enclosure differs')
        equal(outside, row['b'], 'outside A enclosure order differs')
        p.append(((F(0), F(0)),) * L + short + ((F(0), F(0)),) * L)
        q.append(long)
        full = long[:L] + center + long[L + N:]
        bounds = isum(full)
        require(bounds[0] <= 0 <= bounds[1], 'constant-annihilation enclosure excludes zero')
        a.append(full)
        sums.append(bounds)
    return tuple(a), tuple(p), tuple(q), tuple(sums)


def expect_refusal(work, message):
    try:
        work()
    except ValueError as error:
        require(str(error) == message, 'refusal reason differs: ' + str(error))
        return {'refused': True, 'reason': message}
    raise ValueError('controlled invalid request was accepted')


def fir_fixture(oracle, identity_filter=False):
    coeff = (F(1), F(0) if identity_filter else F(1, 2), F(0), F(1), F(0), F(0))
    stages, pads = ((coeff,),), (0,)
    short = matrix(oracle.matrix_fraction(2, stages, pads))
    long = matrix(oracle.matrix_fraction(4, stages, pads))
    p = tuple((F(0), *row, F(0)) for row in short)
    q = long[1:3]
    a = matrix_sub(q, p)
    m, radii, cert = covariance_certificate(singleton(a))
    cross = cross_consistency(singleton(a), singleton(p), singleton(q), cert)
    if identity_filter:
        equal(p, ((F(0), F(1), F(0), F(0)), (F(0), F(0), F(1), F(0))), 'identity P differs')
        equal(q, p, 'identity shared Q differs')
        equal(a, zeros(2, 4), 'identity cancellation failed')
        equal(cert['G'], zeros(2, 2), 'identity covariance differs')
        support_score((F(0), F(0)), cert['G'], zeros(2, 2), 0)
        support_failure = expect_refusal(lambda: support_score((F(0), F(1)), cert['G'], zeros(2, 2), 0),
                                         'residual outside covariance support')
        wrong = matrix_scale(eye(2), F(2))
    else:
        equal(short, ((F(7, 4), F(1, 2)), (F(3, 4), F(3, 2))), 'FIR short oracle differs')
        equal(long, ((F(7, 4), F(1, 2), F(0), F(0)), (F(1, 2), F(5, 4), F(1, 2), F(0)),
                     (F(0), F(1, 2), F(5, 4), F(1, 2)), (F(0), F(0), F(3, 4), F(3, 2))), 'FIR long oracle differs')
        equal(p, ((F(0), F(7, 4), F(1, 2), F(0)), (F(0), F(3, 4), F(3, 2), F(0))), 'FIR P differs')
        equal(a, ((F(1, 2), F(-1, 2), F(0), F(0)), (F(0), F(-1, 4), F(-1, 4), F(1, 2))), 'FIR A differs')
        expected = ((F(1, 2), F(1, 8)), (F(1, 8), F(3, 8)))
        equal(cert['G'], expected, 'FIR covariance differs')
        equal(cert['inverse'], ((F(24, 11), F(-8, 11)), (F(-8, 11), F(32, 11))), 'FIR inverse differs')
        equal(cross['QP'], singleton(((F(39, 16), F(27, 16)), (F(3, 2), F(9, 4)))), 'FIR cross orientation differs')
        equal(sub(mul(expected[0][0], expected[1][1]), mul(expected[0][1], expected[1][0])), F(11, 64), 'FIR determinant differs')
        equal(quadratic((F(1, 2), F(0)), cert['inverse']), F(6, 11), 'FIR impulse quadratic differs')
        wrong = ((F(43, 8), F(53, 16)), (F(53, 16), F(39, 8)))
        support_failure = None
    wrong_refusal = expect_refusal(lambda: equal(wrong, cert['G'], 'omitted shared cross covariance'), 'omitted shared cross covariance')
    return {'short': short, 'long': long, 'P': p, 'Q': q, 'A': a, 'certificate': cert,
            'cross': cross, 'wrong_covariance': wrong, 'wrong_covariance_refusal': wrong_refusal,
            'off_support_refusal': support_failure}


def singleton_fixture():
    a = ((F(1), F(0)), (F(0), F(2)))
    _, _, cert = covariance_certificate(singleton(a))
    equal(cert['G'], ((F(1), F(0)), (F(0), F(4))), 'singleton Gram differs')
    equal(cert['ldl']['pivots'], (F(1), F(4)), 'singleton pivots differ')
    equal(cert['inverse'], ((F(1), F(0)), (F(0), F(1, 4))), 'singleton inverse differs')
    equal((cert['gamma'], cert['delta'], cert['rho'], cert['eta2']), (F(1), F(0), F(0), F(0)), 'singleton bounds differ')
    equal(quadratic((F(2), F(2)), cert['inverse']), F(5), 'singleton quadratic differs')
    return cert


def offdiagonal_fixture(e):
    bounds = (((F(1), F(1)), (neg(e), e)), ((neg(e), e), (F(1), F(1))))
    m, radii, cert = covariance_certificate(bounds)
    expected_h = ((mul(e, e), mul(F(2), e)), (mul(F(2), e), mul(e, e)))
    equal(cert['G'], eye(2), 'off-diagonal midpoint Gram differs')
    equal(cert['H'], expected_h, 'off-diagonal error matrix differs')
    equal(cert['rho'], add(mul(F(2), e), mul(e, e)), 'off-diagonal rho differs')
    equal(cert['eta2'], mul(F(2), mul(e, e)), 'off-diagonal eta2 differs')
    require(cert['accuracy_gate'] is (e == F(1, 10**15)), 'off-diagonal usefulness status differs')
    corner_records = []
    probes = ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1)), (F(1), F(-1)))
    direct = gram_interval(bounds)
    for s, t in product((-1, 1), repeat=2):
        a = ((F(1), mul(F(s), e)), (mul(F(t), e), F(1)))
        omega = midpoint_gram(a)
        for i in range(2):
            for j in range(2):
                require(direct[i][j][0] <= omega[i][j] <= direct[i][j][1], 'corner direct Gram excludes value')
                require(absolute(sub(omega[i][j], cert['G'][i][j])) <= cert['H'][i][j], 'corner H bound failed')
        psd(matrix_sub(omega, matrix_scale(cert['G'], sub(F(1), cert['rho']))))
        psd(matrix_sub(matrix_scale(cert['G'], add(F(1), cert['rho'])), omega))
        inverse, _, _ = inverse_from_ldl(omega, ldl(omega))
        psd(matrix_sub(inverse, cert['inverse_lower']))
        psd(matrix_sub(cert['inverse_upper'], inverse))
        score_records = []
        for z in probes:
            y = tuple(dot(row, z) for row in a)
            true = quadratic(y, inverse)
            qg = quadratic(y, cert['inverse'])
            require(div(qg, add(F(1), cert['rho'])) <= true <= div(qg, sub(F(1), cert['rho'])), 'corner inverse quadratic bound failed')
            score = coefficient_probe(z, m, radii, cert)
            require(score['score_interval'][0] <= true <= score['score_interval'][1], 'corner output-error bound failed')
            score_records.append({'z': z, 'exact_output': y, 'exact_quadratic': true, 'enclosure': score})
        corner_records.append({'signs': [s, t], 'A': a, 'Omega': omega, 'inverse': inverse, 'scores': score_records})
    # On the positive corner, Delta*(1,1)=(2e+e^2)*(1,1).
    delta = matrix_sub(midpoint_gram(((F(1), e), (e, F(1)))), eye(2))
    equal(tuple(total(row) for row in delta), (cert['rho'], cert['rho']), 'attaining spectral error differs')
    bad = expect_refusal(lambda: require(cert['rho'] <= mul(e, e), 'diagonal-only error bound is false'), 'diagonal-only error bound is false')
    return {'e': e, 'bounds': bounds, 'certificate': cert, 'corners': corner_records,
            'corner_count': 4, 'output_score_count': 20, 'diagonal_only_refusal': bad}


def failed_gate_fixture():
    bounds = (((F(1, 2), F(3, 2)), (F(0), F(0))), ((F(0), F(0)), (F(1, 2), F(3, 2))))
    _, _, cert = covariance_certificate(bounds)
    equal(cert['rho'], F(5, 4), 'sufficient-gate rho differs')
    require(cert['status'] == 'unresolved_by_fixed_gate' and 'rank' not in cert, 'sufficient failure misstates rank')
    return {'bounds': bounds, 'certificate': cert, 'all_compatible_diagonal_entries_strictly_positive': True}


def midpoint_fixture():
    bounds = (((F(1), F(3)),),)
    m, _, cert = covariance_certificate(bounds)
    direct = gram_interval(bounds)
    equal((m, cert['G'], direct, cert['H'], cert['rho']),
          (((F(2),),), ((F(4),),), (((F(1), F(9)),),), ((F(5),),), F(5, 4)), 'midpoint distinction differs')
    wrong = expect_refusal(lambda: equal(cert['G'][0][0], F(5), 'coefficient and covariance midpoints differ'), 'coefficient and covariance midpoints differ')
    return {'certificate': cert, 'direct_Gram': direct, 'wrong_midpoint_refusal': wrong}


def rank_ambiguity_fixture():
    bounds = (((F(1), F(1)), (F(0), F(0))), ((F(1), F(1)), (F(-1, 100), F(1, 100))))
    _, _, cert = covariance_certificate(bounds)
    require(cert['status'] == 'unresolved_by_fixed_gate' and 'rank' not in cert, 'rank ambiguity was not retained')
    matrices = (((F(1), F(0)), (F(1), F(0))), ((F(1), F(0)), (F(1), F(1, 100))))
    equal(tuple(matrix_rank(midpoint_gram(a)) for a in matrices), (1, 2), 'rank ambiguity examples differ')
    return {'bounds': bounds, 'certificate': cert, 'compatible_matrices': matrices, 'compatible_ranks': [1, 2]}


def singular_fixture():
    w = ((F(1), F(1)), (F(1), F(1)))
    inverse = matrix_scale(w, F(1, 4))
    equal(support_score((F(2), F(2)), w, inverse, 1), F(4), 'rank-one quadratic differs')
    refusal = expect_refusal(lambda: support_score((F(1), F(-1)), w, inverse, 1), 'residual outside covariance support')
    zero = zeros(2, 2)
    equal(support_score((F(0), F(0)), zero, zero, 0), F(0), 'zero-support quadratic differs')
    zero_refusal = expect_refusal(lambda: support_score((F(1), F(0)), zero, zero, 0), 'residual outside covariance support')
    return {'Omega': w, 'pseudoinverse': inverse, 'projector': validate_pseudoinverse(w, inverse, 1),
            'rank': 1, 'null_vector': (F(1), F(-1)), 'support_refusal': refusal,
            'zero_covariance': zero, 'zero_support_refusal': zero_refusal}


def error_law_fixture():
    score = output_score((F(1), F(0)), (F(1, 10), F(0)), eye(2), F(0), F(1))
    equal(score['score_error_bound'], F(21, 100), 'generic output error bound differs')
    equal(score['score_interval'], (F(79, 100), F(121, 100)), 'generic output interval differs')
    endpoints = F(81, 100), F(121, 100)
    require(all(score['score_interval'][0] <= x <= score['score_interval'][1] for x in endpoints), 'generic endpoint not enclosed')
    zero = output_score((F(0), F(0)), (F(0), F(0)), eye(2), F(0), F(1))
    equal(zero['score_interval'], (F(0), F(0)), 'zero score not exact zero')
    cdf_zero = cdf8(F(16))
    laws = (law_comparison(F(0)), law_comparison(RHO_LIMIT))
    equal(laws[0]['probability_interval'], laws[1]['probability_interval'], 'frozen rho_bar display changed')
    wrong = expect_refusal(lambda: require(laws[0]['upper_CDF']['argument'] <= laws[0]['lower_CDF']['argument'], 'reversed CDF arguments'), 'reversed CDF arguments')
    return {'generic_output_error': score, 'endpoint_quadratics': endpoints, 'exact_zero': zero,
            'CDF_at_rho_zero': cdf_zero, 'law_comparisons': laws, 'wrong_orientation_refusal': wrong}


def validate_model(model):
    equal(model, {'kind': 'known_synthetic_unit_white', 'mean': 'zero', 'covariance': 'I_T',
                  'input_dimension': T, 'output_dimension': DIM}, 'only fixed known unit-white model admitted')


def validate_derived(g, h, delta, inverse=None, gamma=None):
    g, h = symmetric(g, 'Gram'), symmetric(h, 'error matrix')
    require(len(g) == len(h), 'error matrix dimensions differ')
    require(all(v >= 0 for row in h for v in row), 'negative error matrix entry')
    equal(rat(delta), max(total(row) for row in h), 'incorrect covariance error norm bound')
    if inverse is not None:
        inverse = symmetric(inverse, 'inverse')
        equal(matmul(g, inverse), eye(len(g)), 'left inverse identity failed')
        equal(matmul(inverse, g), eye(len(g)), 'right inverse identity failed')
        equal(rat(gamma), norm_infinity(inverse), 'incorrect inverse norm bound')


def guard_work(count):
    require(type(count) is int and 0 <= count <= 244 * T, 'covariance work limit')


def guard_output(count):
    require(type(count) is int and 0 <= count <= MAX_RESULT, 'result byte limit')


def resource_contract():
    return {'derived_fraction_bits': BITS, 'maximum_matrix_dimension': DIM, 'maximum_input_length': T,
            'covariance_pair_coordinate_visit_limit': 244 * T, 'probe_coordinate_visit_limit': 10 * DIM * T,
            'required_reconstructed_adjoint_count': 16, 'required_reconciled_row_count': DIM, 'one_worker': True,
            'external_seconds_per_execution': 1800, 'external_sampled_resident_byte_limit': 2147483648,
            'external_snapshot_byte_limit': 268435456, 'canonical_result_byte_limit': MAX_RESULT,
            'watchdog_is_not_hard_allocator_cap': True, 'no_new_adjoint_precision': True}


def refusal_actions(admitted):
    f, zero, unit = F, zeros(2, 2), eye(2)
    actions = {}
    def case(name, expected, work):
        actions[name] = (expected, work)
    case('float_endpoint', 'exact Fraction required', lambda: interval((0.0, f(1))))
    case('bool_endpoint', 'exact Fraction required', lambda: interval((False, f(1))))
    case('nonfinite_endpoint', 'exact Fraction required', lambda: interval((float('inf'), f(1))))
    case('reversed_interval', 'reversed interval', lambda: interval((f(1), f(0))))
    case('negative_radius', 'negative coefficient radius', lambda: error_matrix(unit, ((f(-1), f(0)), (f(0), f(0)))))
    case('matrix_rows', 'matrix row dimensions differ', lambda: matrix([[f(0)]] * 9))
    case('bool_dimension', 'invalid vector dimension control', lambda: vector([f(0)], True))
    case('bool_row_dimension', 'invalid matrix row control', lambda: matrix([[f(0)]], True))
    case('matrix_columns', 'vector dimensions differ', lambda: matrix([[f(0)] * (T + 1)]))
    case('ragged_box', 'interval matrix column dimensions differ', lambda: box_matrix([[(f(0), f(0))], []]))
    case('asymmetric_gram', 'Gram is asymmetric', lambda: ldl(((f(1), f(1)), (f(0), f(1)))))
    case('asymmetric_error', 'error matrix is asymmetric', lambda: validate_derived(unit, ((f(1), f(1)), (f(0), f(1))), f(2)))
    case('negative_error', 'negative error matrix entry', lambda: validate_derived(unit, ((f(-1), f(0)), (f(0), f(0))), f(0)))
    case('negative_pivot', 'negative Gram pivot after positive predecessors', lambda: ldl(((f(1), f(0)), (f(0), f(-1)))))
    factor = ldl(unit)
    wrong_factor = {**factor, 'pivots': (f(1), f(2))}
    case('wrong_ldl', 'LDL reconstruction differs', lambda: inverse_from_ldl(unit, wrong_factor))
    case('wrong_inverse', 'left inverse identity failed', lambda: validate_derived(unit, zero, f(0), zero, f(0)))
    case('wrong_delta', 'incorrect covariance error norm bound', lambda: validate_derived(unit, zero, f(1)))
    case('wrong_gamma', 'incorrect inverse norm bound', lambda: validate_derived(unit, zero, f(0), unit, f(2)))
    case('incorrect_rank', 'incorrect exact rank', lambda: validate_pseudoinverse(unit, unit, 1))
    case('bool_rank', 'invalid exact rank', lambda: validate_pseudoinverse(unit, unit, True))
    case('wrong_mp1', 'Moore-Penrose identity 1 failed', lambda: validate_pseudoinverse(unit, zero, 2))
    case('wrong_mp2', 'Moore-Penrose identity 2 failed', lambda: validate_pseudoinverse(zero, unit, 0))
    case('wrong_mp3', 'Moore-Penrose identity 3 failed', lambda: validate_pseudoinverse(((f(1), f(0)), (f(0), f(0))), ((f(1), f(1)), (f(1), f(1))), 1))
    case('off_support', 'residual outside covariance support', lambda: support_score((f(1), f(0)), zero, zero, 0))
    case('negative_rho', 'score requires 0<=rho<1', lambda: output_score((f(0), f(0)), (f(0), f(0)), unit, f(-1), f(1)))
    case('rho_at_one', 'score requires 0<=rho<1', lambda: output_score((f(0), f(0)), (f(0), f(0)), unit, f(1), f(1)))
    case('negative_output_error', 'negative output error', lambda: output_score((f(0), f(0)), (f(-1), f(0)), unit, f(0), f(1)))
    case('unqualified_cdf', 'CDF comparison requires admitted rho', lambda: law_comparison(f(1, 10)))
    case('cdf_series_domain', 'exponential series argument out of range', lambda: cdf8(f(260)))
    case('negative_cdf_argument', 'negative CDF argument', lambda: cdf8(f(-1)))
    model = {'kind': 'known_synthetic_unit_white', 'mean': 'zero', 'covariance': 'I_T', 'input_dimension': T, 'output_dimension': DIM}
    case('estimated_covariance', 'only fixed known unit-white model admitted', lambda: validate_model({**model, 'kind': 'estimated'}))
    case('colored_covariance', 'only fixed known unit-white model admitted', lambda: validate_model({**model, 'covariance': 'colored'}))
    case('fraction_numerator_cap', 'Fraction resource limit', lambda: rat(f(1 << BITS)))
    case('fraction_denominator_cap', 'Fraction resource limit', lambda: rat(f(1, 1 << BITS)))
    case('operation_result_cap', 'Fraction resource limit', lambda: mul(f(1 << (BITS - 1)), f(2)))
    case('hex_length', 'hex scalar length limit', lambda: decode_scalar(['1' * ((BITS + 3) // 4 + 2), '1']))
    case('hex_plus', 'noncanonical hexadecimal scalar', lambda: decode_scalar(['+1', '1']))
    case('hex_negative_zero', 'noncanonical hexadecimal scalar', lambda: decode_scalar(['-0', '1']))
    case('hex_leading_zero', 'noncanonical hexadecimal scalar', lambda: decode_scalar(['01', '1']))
    case('hex_denominator_zero', 'noncanonical hexadecimal scalar', lambda: decode_scalar(['1', '0']))
    case('hex_unreduced', 'unreduced hexadecimal scalar', lambda: decode_scalar(['2', '2']))
    case('work_cap', 'covariance work limit', lambda: guard_work(244 * T + 1))
    case('work_bool', 'covariance work limit', lambda: guard_work(True))
    case('output_cap', 'result byte limit', lambda: guard_output(MAX_RESULT + 1))
    case('duplicate_json', 'duplicate JSON key', lambda: parse_json(b'{"x":1,"x":2}'))
    case('nonfinite_json', 'nonfinite JSON constant', lambda: parse_json(b'{"x":NaN}'))
    case('overflow_json', 'nonfinite JSON number', lambda: parse_json(b'{"x":1e999}'))
    case('changed_snapshot', 'test: snapshot identity differs', lambda: verify_bytes(b'b', identity(b'a'), 'test'))
    case('bool_pin', 'invalid frozen pin', lambda: pin_only({'bytes': True, 'sha256': '0' * 64}))
    case('changed_runtime', 'runtime versions differ', lambda: validate_runtime({'versions': {}}, admitted['runtime']))
    wrong_runtime = copy.deepcopy(admitted['runtime'])
    wrong_runtime['byte_order'] = 'wrong'
    case('changed_runtime_build', 'full qualified runtime differs', lambda: validate_runtime(wrong_runtime, admitted['runtime']))
    check = admitted['modules']['check60']
    metadata = {'runtime': admitted['runtime'], 'arithmetic': admitted['arithmetic']}
    def receipt_change(field, value):
        candidate = copy.deepcopy(admitted['qualification'])
        candidate[field] = value
        return check.validate_qualification(candidate, metadata)
    case('failed_receipt', 'qualification failed or incomplete', lambda: receipt_change('status', 'failed'))
    case('incomplete_receipt', 'qualification gate coverage changed', lambda: receipt_change('gates', []))
    case('changed_receipt_engine', 'qualification mismatch: engine_identity', lambda: receipt_change('engine_identity', {}))
    case('changed_arithmetic', 'qualification mismatch: arithmetic_contract', lambda: receipt_change('arithmetic_contract', {}))
    case('wrong_padding', 'fixed padding differs', lambda: validate_padding((28,) + (9,) * 16))
    case('bool_padding', 'fixed padding differs', lambda: validate_padding((True,) + (9,) * 16))
    def changed_manifest(kind):
        manifest = parse_json(admitted['bodies']['coefficients'])
        if kind == 'coefficient':
            manifest['stages'][0]['coefficient_hex'][0][0] = '0x0.0p+0'
        elif kind == 'stage_order':
            manifest['stages'][0], manifest['stages'][1] = manifest['stages'][1], manifest['stages'][0]
        else:
            manifest['stages'][0]['padlen'] += 1
        validate_manifest(manifest, admitted['bodies']['coefficients'])
    for kind in ('coefficient', 'stage_order', 'padding'):
        case('changed_manifest_' + kind, 'coefficient manifest, stage order or padding differs',
             lambda k=kind: changed_manifest(k))
    case('missing_rows', 'complete fixed row inventory required', lambda: row_inventory(()))
    case('wrong_rows', 'complete fixed row inventory required', lambda: row_inventory(tuple({'row': v} for v in reversed(ROWS))))
    case('wrong_snapshot_shape', 'immutable complete snapshot required', lambda: snapshot_record([]))
    # Empty expected inventory must reject before asking a check helper for a summary.
    case('missing_expected_summaries', 'qualification certificate row inventory differs',
         lambda: reconcile_rows(tuple({'row': v} for v in ROWS), {}, None))
    return actions


def fixture_inventory(admitted):
    return ['fixture:' + name for name in ('fir', 'cancellation', 'singleton', 'offdiagonal_small',
        'offdiagonal_large', 'failed_gate', 'midpoint', 'rank_ambiguity', 'singular', 'output_law')] + [
        'refusal:' + name for name in refusal_actions(admitted)]


def record(gates, identifier, work):
    try:
        detail = work()
        passed = detail.get('acceptance', {}).get('passed', True) is True
        gates.append({'id': identifier, 'passed': passed, 'detail': detail})
        return detail
    except ERRORS as error:
        detail = {'error_type': type(error).__name__, 'error': str(error)}
        if isinstance(error, CovarianceComputationError):
            detail.update(failed_stage=error.stage, completed_fields=error.completed,
                          original_error_type=error.original_error_type, original_error=error.original_error)
        gates.append({'id': identifier, 'passed': False,
                      'detail': detail})
        return None


def not_run(gates, identifier, reason):
    gates.append({'id': identifier, 'passed': False, 'detail': {'not_run': True, 'reason': reason}})


def run_fixtures(admitted, gates):
    oracle = admitted['modules']['oracle']
    functions = (
        ('fir', lambda: fir_fixture(oracle)), ('cancellation', lambda: fir_fixture(oracle, True)),
        ('singleton', singleton_fixture), ('offdiagonal_small', lambda: offdiagonal_fixture(F(1, 10**15))),
        ('offdiagonal_large', lambda: offdiagonal_fixture(F(1, 10))), ('failed_gate', failed_gate_fixture),
        ('midpoint', midpoint_fixture), ('rank_ambiguity', rank_ambiguity_fixture),
        ('singular', singular_fixture), ('output_law', error_law_fixture))
    for name, work in functions:
        record(gates, 'fixture:' + name, work)
    for name, (message, work) in refusal_actions(admitted).items():
        record(gates, 'refusal:' + name, lambda action=work, expected=message: expect_refusal(action, expected))
    equal([g['id'] for g in gates], fixture_inventory(admitted), 'fixture inventory differs')


def integration_ids():
    return ['integration:' + name for name in ('reconstruction', 'gram', 'mathematical', 'accuracy', 'cross')] + [
        'probe:' + name for name in ('zero', 'constant', *(str(i) for i in ROWS))] + ['integration:law', 'integration:final_custody']


def run_integration(admitted, gates, row_observer):
    state = {}
    def build():
        rows, before = reconstruct(admitted, row_observer)
        a, p, q, sums = operators_from_rows(rows)
        check = admitted['modules']['check60']
        domain = {'row_order': list(ROWS), 'coordinate_order': 'left,center,right', 'shape': [DIM, T]}
        state.update(rows=rows, row_state=before, a=a, p=p, q=q, domain=domain)
        return {'adjoints_reconstructed': 16, 'summaries_reconciled': 8,
                'row_state_identity': before, 'row_summaries': [check.row_summary(row) for row in rows],
                'vector_identities': [{'row': row['row'],
                    'short': array_identity(row['short']['intervals'], 'short', {'length': N, 'row': row['row']}),
                    'long': array_identity(row['long']['intervals'], 'long', {'length': T, 'row': row['row'], 'seed': L + row['row']})} for row in rows],
                'A_identity': array_identity(a, 'A', domain), 'P_identity': array_identity(p, 'P', domain),
                'Q_identity': array_identity(q, 'Q', domain), 'constant_row_sum_intervals': sums,
                'coefficient_arrays_stored_in_result': False}
    reconstruction = record(gates, 'integration:reconstruction', build)
    if reconstruction is None:
        for identifier in integration_ids()[1:]:
            not_run(gates, identifier, 'complete coefficient reconstruction/reconciliation failed')
        return
    def gram():
        m, radii, cert = covariance_certificate(state['a'])
        validate_derived(cert['G'], cert['H'], cert['delta'], cert.get('inverse'), cert.get('gamma'))
        state.update(m=m, radii=radii, certificate=cert)
        return {'certificate': cert, 'M_identity': array_identity(m, 'M', state['domain']),
                'R_identity': array_identity(radii, 'R', state['domain'])}
    gram_result = record(gates, 'integration:gram', gram)
    if gram_result is None:
        for identifier in integration_ids()[2:]:
            not_run(gates, identifier, 'Gram/certificate computation failed')
        return
    cert = state['certificate']
    record(gates, 'integration:mathematical', lambda: {'status': cert['status'],
        'acceptance': {'passed': cert['mathematical_gate']}, 'rho': cert.get('rho'), 'strict_limit': F(1)})
    record(gates, 'integration:accuracy', lambda: {'status': cert['status'],
        'acceptance': {'passed': cert['accuracy_gate']}, 'rho': cert.get('rho'), 'inclusive_limit': RHO_LIMIT})
    record(gates, 'integration:cross', lambda: cross_consistency(state['a'], state['p'], state['q'], cert))
    for name in ('zero', 'constant', *(str(i) for i in ROWS)):
        identifier = 'probe:' + name
        if cert['mathematical_gate']:
            def probe(label=name):
                z = tuple(F(int(label == 'constant' or (label not in ('zero', 'constant') and j == L + int(label)))) for j in range(T))
                result = coefficient_probe(z, state['m'], state['radii'], cert)
                if label == 'zero':
                    equal(result['score_interval'], (F(0), F(0)), 'zero probe quadratic not exact zero')
                if label == 'constant':
                    require(result['score_interval'][0] <= 0 <= result['score_interval'][1], 'constant probe score excludes zero')
                return {'probe': label, 'raw_index': None if label in ('zero', 'constant') else L + int(label),
                        'input_identity': array_identity(z, 'synthetic_probe', {'length': T, 'probe': label}), **result}
            record(gates, identifier, probe)
        else:
            not_run(gates, identifier, 'mathematical covariance/inverse gate unresolved')
    if cert['accuracy_gate']:
        record(gates, 'integration:law', lambda: law_comparison(cert['rho']))
    else:
        not_run(gates, 'integration:law', 'fixed rho usefulness gate failed')
    def final_custody():
        equal(row_state(state['rows'], admitted['modules']['check60']), state['row_state'], 'reconciled row state changed')
        recheck(admitted)
        visits = 244 * T
        guard_work(visits)
        return {'row_state_identity': state['row_state'], 'covariance_pair_coordinate_visit_limit': visits,
                'probe_coordinate_visit_limit': 10 * DIM * T, 'sources_runtime_coefficients_unchanged': True}
    record(gates, 'integration:final_custody', final_custody)


def run_checks(admitted, fixtures_only, row_observer=None):
    require(type(fixtures_only) is bool, 'explicit execution mode required')
    require(row_observer is None or callable(row_observer), 'row observer must be callable')
    require(not fixtures_only or row_observer is None, 'fixtures cannot capture admitted rows')
    gates = []
    run_fixtures(admitted, gates)
    ready = all(g['passed'] is True for g in gates)
    recheck(admitted)
    if not fixtures_only:
        if ready:
            run_integration(admitted, gates, row_observer)
        else:
            for identifier in integration_ids():
                not_run(gates, identifier, 'exact deterministic fixtures failed before admitted coefficient design')
    def final_custody():
        recheck(admitted)
        return {'complete_source_runtime_receipt_state_unchanged': True}
    record(gates, 'completion:custody', final_custody)
    inventory = fixture_inventory(admitted) + ([] if fixtures_only else integration_ids()) + ['completion:custody']
    equal([g['id'] for g in gates], inventory, 'complete gate inventory differs')
    failed = sum(g['passed'] is not True for g in gates)
    mode = 'fixtures_only' if fixtures_only else 'fixed_operator_covariance'
    return {'schema_version': 'ri73-unit-white-operator-covariance-v1', 'mode': mode,
            'status': mode + ('_passed' if failed == 0 else '_failed'),
            'full_integration_qualified': not fixtures_only and failed == 0,
            'source_identity': identity(admitted['own']),
            'dependencies': {name: {'path': DEPENDENCIES[name]['path'], **identity(body)} for name, body in admitted['bodies'].items()},
            'runtime': admitted['runtime'], 'inherited_arithmetic_contract': admitted['arithmetic'],
            'resource_contract': resource_contract(), 'model': {'kind': 'known_synthetic_unit_white', 'mean': 'zero',
                'covariance': 'I_T', 'input_dimension': T, 'output_dimension': DIM},
            'dimensions': {'N': N, 'L': L, 'T': T}, 'rows': list(ROWS), 'sample_spacing': F(1, 4096),
            'gate_inventory': inventory, 'gate_counts': {'total': len(gates), 'passed': len(gates) - failed, 'failed': failed},
            'gates': gates, 'deterministic_fixture_admission_passed': ready, 'sampling_performed': False,
            'admitted_coefficient_design_requested': not fixtures_only,
            'reconstructed_rows_admitted': admitted['rows'] is not None,
            'exact_scalar_encoding': '[reduced lowercase hexadecimal numerator, positive hexadecimal denominator]; no +, no leading zeros, zero=[0,1] strings',
            'scope': {'covariance': 'Conditional on fixed synthetic unit-white input covariance; no detector-noise estimate.',
                'rank': 'Actual rank8/inverse claims require exact positive Gram pivots and rho<1; usefulness also requires rho<=10^-12.',
                'law': 'Deterministic ideal-Gaussian CDF sandwich; no approximate sampler is assigned exact chi-square.',
                'prior_evidence': 'RI60 196 gates are validated pinned prior evidence, not rerun; full mode requires 16 reconstructed adjoints before Gram work.',
                'observations': 'No raw strain, CROP, REFERENCE, OBSERVED_CONTEXT, observed score or new data accessed.',
                'physics': 'No calibrated confidence, source/response/timing resolution, native forward map or physical gravity claim.'}}


def report_bytes(result):
    encoder = json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)
    body = bytearray()
    for chunk in encoder.iterencode(encoded(result)):
        piece = chunk.encode('ascii')
        guard_output(len(body) + len(piece))
        body.extend(piece)
    guard_output(len(body) + 1)
    body.extend(b'\n')
    return bytes(body)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fixtures', action='store_true', help='Only exact tiny fixtures; no admitted coefficient design/reconstruction.')
    args = parser.parse_args(argv)
    admitted = None
    try:
        admitted = admission()
        result = run_checks(admitted, args.fixtures)
        sys.stdout.buffer.write(report_bytes(result))
        return 0 if result['gate_counts']['failed'] == 0 else 1
    except ERRORS as error:
        failure = {'schema_version': 'ri73-unit-white-operator-failure-v1', 'status': 'execution_refused',
                   'mode': 'fixtures_only' if args.fixtures else 'fixed_operator_covariance',
                   'full_integration_qualified': False, 'error_type': type(error).__name__, 'error': str(error)}
        if admitted is not None:
            failure['source_identity'] = identity(admitted['own'])
        sys.stdout.buffer.write(report_bytes(failure))
        print('RI73 refused: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
