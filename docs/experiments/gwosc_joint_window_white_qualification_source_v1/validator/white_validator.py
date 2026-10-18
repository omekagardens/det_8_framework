"""UNEXECUTED RI125 independent WHITE reconstruction source.

This module is a different author's implementation. It imports no primary
parser, kernel, controls, arithmetic or expected dictionaries. No import-time
I/O occurs. A future root-admitted caller must establish loaded-source and
runtime custody before using any actual-input entry point.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

BITS = 262144
FILE_CAP = 64 * 1024 * 1024
ROW_CAP = 8 * 1024 * 1024
ROW_IDS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
N, L, T, D = 2769, 4096, 10961, 8192
CONTEXT = 'RI125_FABRICATED_ONLY_NOT_HISTORICAL'
ZERO, ONE = (0, 1), (1, 1)
SHIFT_FIELDS = ('orientation', 'center', 'error', 'direct', 'midpoint_polarization', 'trace_center', 'trace_error')
GRAM_FIELDS = ('G', 'H', 'delta', 'inverse', 'gamma', 'rho')


class Refusal(ValueError):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(code + ': ' + message)


def demand(test, code, text):
    if not test:
        raise Refusal(code, text)


def bounded_integer(x):
    demand(type(x) is int, 'EXACT', 'plain integer required')
    demand(x.bit_length() <= BITS, 'RESOURCE', 'integer bit ceiling')
    return x


def Q(n, d=1):
    demand(type(n) is int and type(d) is int, 'EXACT', 'plain integer required')
    demand(d != 0, 'ZERO_DIVISOR', 'division by zero')
    if d < 0:
        n, d = -n, -d
    common = math.gcd(n, d)
    return bounded_integer(n // common), bounded_integer(d // common)


def checked_q(x):
    demand(type(x) is tuple and len(x) == 2, 'EXACT', 'reduced integer pair required')
    a, b = x
    bounded_integer(a); bounded_integer(b)
    demand(b > 0 and math.gcd(a, b) == 1, 'EXACT', 'reduced positive denominator')
    return x


def plus(x, y):
    a, b = checked_q(x); c, d = checked_q(y)
    common = math.gcd(b, d)
    return Q(a * (d // common) + c * (b // common), (b // common) * d)


def neg(x):
    a, b = checked_q(x)
    return -a, b


def minus(x, y):
    return plus(x, neg(y))


def times(x, y):
    a, b = checked_q(x); c, d = checked_q(y)
    left, right = math.gcd(abs(a), d), math.gcd(abs(c), b)
    return Q((a // left) * (c // right), (b // right) * (d // left))


def quotient(x, y):
    c, d = checked_q(y)
    demand(c != 0, 'ZERO_DIVISOR', 'division by zero')
    return times(x, Q(d, c))


def absolute(x):
    a, b = checked_q(x)
    return abs(a), b


def cmp(x, y):
    a, b = checked_q(x); c, d = checked_q(y)
    # Cross products are internal comparison temporaries, not retained operands.
    left, right = a * d, c * b
    return (left > right) - (left < right)


def sum_q(items):
    out = ZERO
    for x in items:
        out = plus(out, x)
    return out


def smallest(items):
    iterator = iter(items); out = next(iterator)
    for x in iterator:
        if cmp(x, out) < 0:
            out = x
    return out


def largest(items):
    iterator = iter(items); out = next(iterator)
    for x in iterator:
        if cmp(x, out) > 0:
            out = x
    return out


def exact_keys(value, names, code='SCHEMA'):
    demand(type(value) is dict and all(type(k) is str for k in value)
           and set(value) == set(names), code, 'closed object keys')


def items(value, size):
    demand(type(value) is list and len(value) == size, 'SHAPE', 'exact list length')
    return value


def equal_types(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return set(a) == set(b) and all(equal_types(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(equal_types(a[i], b[i]) for i in range(len(a)))
    return a == b


def match(a, b, code, message):
    demand(equal_types(a, b), code, message)


def scalar(x):
    a, b = checked_q(x)
    return [format(a, 'x'), format(b, 'x')]


def decode_scalar(x):
    pair = items(x, 2)
    nums = []
    for text in pair:
        demand(type(text) is str, 'EXACT', 'hex string required')
        demand(len(text) <= 65537, 'RESOURCE', 'integer text ceiling')
        demand(re.fullmatch(r'(0|-?[1-9a-f][0-9a-f]*)', text) is not None,
               'EXACT', 'canonical signed hex')
        nums.append(bounded_integer(int(text, 16)))
    a, b = nums
    demand(b > 0 and math.gcd(a, b) == 1, 'EXACT', 'reduced positive denominator')
    return a, b


def decode_interval(value):
    a, b = items(value, 2)
    low, high = decode_scalar(a), decode_scalar(b)
    demand(cmp(low, high) <= 0, 'INTERVAL', 'ordered endpoints')
    return low, high


def interval(low, high):
    demand(cmp(low, high) <= 0, 'INTERVAL', 'ordered endpoints')
    return [scalar(low), scalar(high)]


def packed(value):
    if type(value) is tuple and len(value) == 2 and all(type(v) is int for v in value):
        return scalar(value)
    if type(value) in (tuple, list):
        return [packed(x) for x in value]
    if type(value) is dict:
        return {k: packed(v) for k, v in value.items()}
    demand(type(value) in (str, bool, int) or value is None, 'EXACT', 'encoded type')
    return value


def parse_json(body):
    demand(type(body) is bytes and len(body) <= FILE_CAP, 'RESOURCE', 'JSON byte ceiling')
    def collect(pairs):
        obj = {}
        for key, value in pairs:
            demand(key not in obj, 'SCHEMA', 'duplicate JSON key')
            obj[key] = value
        return obj
    def decimal(_):
        raise Refusal('EXACT', 'decimal or nonfinite JSON token')
    def integer(token):
        demand(len(token) <= 65537, 'RESOURCE', 'JSON integer text ceiling')
        return bounded_integer(int(token))
    try:
        return json.loads(body.decode('utf-8'), object_pairs_hook=collect,
                          parse_float=decimal, parse_int=integer, parse_constant=decimal)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Refusal('SCHEMA', 'invalid bounded JSON') from exc


def serialized_parts(value, compact=False):
    options = {'sort_keys': True, 'ensure_ascii': True, 'allow_nan': False}
    options.update({'separators': (',', ':')} if compact else {'indent': 2})
    produced = 0
    for token in json.JSONEncoder(**options).iterencode(value):
        chunk = token.encode('ascii')
        produced += len(chunk)
        demand(produced <= FILE_CAP, 'RESOURCE', 'serialized byte ceiling')
        yield chunk
    if not compact:
        demand(produced < FILE_CAP, 'RESOURCE', 'terminal newline ceiling')
        yield b'\n'


def serialize(value, compact=False):
    return b''.join(serialized_parts(value, compact))


def content_pin(body):
    demand(type(body) is bytes and len(body) <= FILE_CAP, 'RESOURCE', 'bounded immutable body')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def object_pin(value, compact=False):
    hasher, count = hashlib.sha256(), 0
    for chunk in serialized_parts(value, compact):
        hasher.update(chunk); count += len(chunk)
    return {'bytes': count, 'sha256': hasher.hexdigest()}


def matrix_decode(value, dimension):
    return [[decode_scalar(x) for x in items(row, dimension)] for row in items(value, dimension)]


def trace_q(matrix):
    return sum_q(matrix[i][i] for i in range(len(matrix)))


def dot_q(a, b):
    demand(len(a) == len(b), 'SHAPE', 'dot lengths')
    return sum_q(times(a[i], b[i]) for i in range(len(a)))


def check_gram(encoded, size):
    exact_keys(encoded, GRAM_FIELDS)
    g = matrix_decode(encoded['G'], size)
    h = matrix_decode(encoded['H'], size)
    inv = matrix_decode(encoded['inverse'], size)
    delta, gamma, rho = (decode_scalar(encoded[k]) for k in ('delta', 'gamma', 'rho'))
    for i in range(size):
        for j in range(size):
            demand(g[i][j] == g[j][i] and h[i][j] == h[j][i]
                   and inv[i][j] == inv[j][i] and cmp(h[i][j], ZERO) >= 0,
                   'GRAM', 'symmetric Gram/inverse and nonnegative bound')
            target = ONE if i == j else ZERO
            demand(dot_q(g[i], [inv[k][j] for k in range(size)]) == target
                   and dot_q(inv[i], [g[k][j] for k in range(size)]) == target,
                   'GRAM', 'both inverse products')
    # Independent symmetric Schur reduction, rather than the primary's LDL factors.
    schur = [list(row) for row in g]
    for pivot in range(size):
        d = schur[pivot][pivot]
        demand(cmp(d, ZERO) > 0, 'GRAM', 'nonpositive inherited Gram pivot')
        for i in range(pivot + 1, size):
            for j in range(pivot + 1, size):
                schur[i][j] = minus(schur[i][j], quotient(times(schur[i][pivot], schur[pivot][j]), d))
    demand(delta == largest(sum_q(row) for row in h), 'GRAM', 'delta row-sum bound')
    demand(gamma == largest(sum_q(absolute(v) for v in row) for row in inv)
           and cmp(gamma, ZERO) > 0, 'GRAM', 'gamma inverse row-sum bound')
    demand(rho == times(delta, gamma) and cmp(rho, ZERO) >= 0 and cmp(rho, Q(1, 10**12)) <= 0,
           'GRAM', 'unchanged inherited rho gate')
    return g, h, gamma, rho


def build_shift(rows, *, length, stride):
    demand(type(rows) is list, 'SHAPE', 'strip rows list')
    dimension = len(rows)
    demand(type(length) is int and type(stride) is int
           and (dimension, length, stride) in ((1, 3, 2), (2, 3, 2), (8, T, D)),
           'DOMAIN', 'fixed primitive domain')
    labels = list(ROW_IDS) if dimension == 8 else list(range(dimension))
    width = length - stride
    h, u = [], []
    for index in range(dimension):
        row = rows[index]
        exact_keys(row, ('row', 'head', 'tail'))
        demand(type(row['row']) is int and row['row'] == labels[index], 'ROW', 'row order')
        h.append([decode_interval(v) for v in items(row['head'], width)])
        u.append([decode_interval(v) for v in items(row['tail'], width)])
    centers, errors, direct, polarization = [], [], [], []
    for i in range(dimension):
        kr, er, dr, pr = [], [], [], []
        for j in range(dimension):
            k = e = lower = upper = pol = ZERO
            for coordinate in range(width):
                ulo, uhi = u[i][coordinate]; hlo, hhi = h[j][coordinate]
                um = quotient(plus(ulo, uhi), Q(2)); ur = quotient(minus(uhi, ulo), Q(2))
                hm = quotient(plus(hlo, hhi), Q(2)); hr = quotient(minus(hhi, hlo), Q(2))
                k = plus(k, times(um, hm))
                e = sum_q((e, times(absolute(um), hr), times(ur, absolute(hm)), times(ur, hr)))
                products = [times(x, y) for x in (ulo, uhi) for y in (hlo, hhi)]
                lower = plus(lower, smallest(products)); upper = plus(upper, largest(products))
                added, subtracted = plus(um, hm), minus(um, hm)
                pol = plus(pol, quotient(minus(times(added, added), times(subtracted, subtracted)), Q(4)))
            demand(k == pol, 'POLARIZATION', 'midpoint identity differs')
            demand(cmp(largest((lower, minus(k, e))), smallest((upper, plus(k, e)))) <= 0,
                   'DIRECT', 'direct and midpoint-radius boxes disjoint')
            kr.append(k); er.append(e); dr.append((lower, upper)); pr.append(pol)
        centers.append(kr); errors.append(er); direct.append(dr); polarization.append(pr)
    return packed({'orientation': 'earlier_tail_times_later_head_transpose',
                   'center': centers, 'error': errors, 'direct': direct,
                   'midpoint_polarization': polarization,
                   'trace_center': trace_q(centers), 'trace_error': trace_q(errors)})


def usefulness(error, lower):
    checked_q(error); checked_q(lower)
    demand(cmp(error, ZERO) >= 0 and cmp(lower, ZERO) > 0,
           'BOUND', 'nonnegative error, positive lower bound')
    eps = quotient(error, lower)
    return eps, ('usefulness_passed' if cmp(eps, Q(1, 10**12)) <= 0 else 'accuracy_failed')


def make_response(gram, shift, *, n):
    demand(type(n) is int and n in (2, 3, 6, 7), 'DOMAIN', 'fixed window count')
    exact_keys(shift, SHIFT_FIELDS)
    demand(shift['orientation'] == 'earlier_tail_times_later_head_transpose',
           'ORIENTATION', 'directed shift label')
    demand(type(shift['center']) is list and len(shift['center']) in (1, 2, 8), 'SHAPE', 'fixed matrix size')
    size = len(shift['center'])
    k, e, pol = (matrix_decode(shift[name], size) for name in ('center', 'error', 'midpoint_polarization'))
    boxes = [[decode_interval(v) for v in items(row, size)] for row in items(shift['direct'], size)]
    for i in range(size):
        for j in range(size):
            demand(cmp(e[i][j], ZERO) >= 0, 'BOUND', 'nonnegative shift radius')
            demand(k[i][j] == pol[i][j], 'POLARIZATION', 'saved polarization')
            lo, hi = boxes[i][j]
            demand(cmp(largest((lo, minus(k[i][j], e[i][j]))), smallest((hi, plus(k[i][j], e[i][j])))) <= 0,
                   'DIRECT', 'saved direct enclosure intersection')
    demand(decode_scalar(shift['trace_center']) == trace_q(k) and decode_scalar(shift['trace_error']) == trace_q(e),
           'TRACE', 'complete shift trace')
    g, h, gamma, rho = check_gram(gram, size)
    a, b = Q(n - 1, n), Q(n - 1, n * n)
    z, f, enclosure = [], [], []
    for i in range(size):
        zr, fr, ir = [], [], []
        for j in range(size):
            middle = minus(minus(times(a, g[i][j]), times(b, k[i][j])), times(b, k[j][i]))
            error = sum_q((times(a, h[i][j]), times(b, e[i][j]), times(b, e[j][i])))
            zr.append(middle); fr.append(error); ir.append((minus(middle, error), plus(middle, error)))
        z.append(zr); f.append(fr); enclosure.append(ir)
    entry_trace = (sum_q(enclosure[i][i][0] for i in range(size)), sum_q(enclosure[i][i][1] for i in range(size)))
    gtrace, htrace, ktrace, etrace = map(trace_q, (g, h, k, e))
    low = minus(times(a, minus(gtrace, htrace)), times(times(Q(2), b), plus(ktrace, etrace)))
    high = minus(times(a, plus(gtrace, htrace)), times(times(Q(2), b), minus(ktrace, etrace)))
    trace_two = low, high
    demand(entry_trace == trace_two, 'TRACE', 'entry and g/c trace equality')
    lo_factor, hi_factor = Q((n - 1)**2, n*n), Q(n*n - 1, n*n)
    structural = (times(times(lo_factor, minus(ONE, rho)), gtrace), times(times(hi_factor, plus(ONE, rho)), gtrace))
    demand(cmp(largest((entry_trace[0], structural[0])), smallest((entry_trace[1], structural[1]))) <= 0,
           'STRUCTURAL', 'trace structural interval intersection')
    delta = largest(sum_q(row) for row in f)
    ell = quotient(times(lo_factor, minus(ONE, rho)), gamma)
    eps, status = usefulness(delta, ell)
    return packed({'n': n, 'a': a, 'b': b, 'center': z, 'error': f, 'entry_intervals': enclosure,
                   'trace_interval': entry_trace, 'trace_from_g_c': trace_two,
                   'structural_trace_interval': structural, 'delta': delta, 'ell': ell, 'eps': eps,
                   'enclosure_state': 'valid_conditional_enclosure', 'usefulness_state': status})

WHITE_CASES = (
    'W01_single_white_two', 'W02_single_white_three', 'W03_oriented_two',
    'W04_negative_scale', 'W05_double_scale', 'W06_interval_mixed',
    'W07_interval_crosses_zero', 'W08_zero_shift', 'W09_production_boundary_sparse',
    'W10_usefulness_boundaries', 'W11_asymmetric_rational_radii',
    'W12_sparse_lifted_denominators', 'W13_full_response_below',
    'W14_full_response_equal', 'W15_full_response_above')


def blank_full_rows():
    return [{'row': label, 'short': [interval(ZERO, ZERO) for _ in range(N)],
             'long': [interval(ZERO, ZERO) for _ in range(T)]} for label in ROW_IDS]


def prescribed_full_rows(case_id):
    rows = blank_full_rows()
    if case_id in ('W09_production_boundary_sparse', 'J01_four_rows_exact'):
        positions = [{0: 1, 8192: 2, 3000: -3}, {2768: 3, 10960: -1, 3001: -2}]
        positions.extend({3000 + 2*i: 1, 3001 + 2*i: -1} for i in range(2, 8))
    else:
        demand(case_id in WHITE_CASES[12:] or case_id == 'J02_precision_inconclusive', 'DOMAIN', 'fixed fabricated assembly case')
        positions = [{3000 + 2*i: 1, 3001 + 2*i: -1} for i in range(8)]
    for row, changes in zip(rows, positions):
        for coordinate, number in changes.items():
            row['long'][coordinate] = interval(Q(number), Q(number))
    return rows


def exact_vectors(full_rows):
    vectors = []
    for ordinal, row in enumerate(items(full_rows, 8)):
        exact_keys(row, ('row', 'short', 'long'), 'ROW')
        match(row['row'], ROW_IDS[ordinal], 'ROW', 'fixed row order')
        sparse = {}
        for j, box in enumerate(items(row['long'], T)):
            low, high = decode_interval(box)
            demand(low == high, 'BINDING', 'fabricated exact full-row singleton')
            if low != ZERO:
                sparse[j] = low
        for j, box in enumerate(items(row['short'], N)):
            low, high = decode_interval(box)
            demand(low == high, 'BINDING', 'fabricated exact full-row singleton')
            old = sparse.get(L+j, ZERO)
            value = minus(old, low)
            if value != ZERO:
                sparse[L+j] = value
            else:
                sparse.pop(L+j, None)
        demand(sum_q(sparse.values()) == ZERO, 'BINDING', 'fabricated exact constant annihilation')
        vectors.append(sparse)
    return vectors


def inverse_of(g):
    size = len(g)
    augmented = [list(g[i]) + [ONE if i == j else ZERO for j in range(size)] for i in range(size)]
    for column in range(size):
        pivot = augmented[column][column]
        demand(cmp(pivot, ZERO) > 0, 'GRAM', 'nonpositive inherited Gram pivot')
        augmented[column] = [quotient(v, pivot) for v in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [minus(augmented[row][j], times(factor, augmented[column][j])) for j in range(2*size)]
    return [row[size:] for row in augmented]


def gram_of_vectors(vectors, radius=ZERO):
    size = len(vectors)
    g = [[sum_q(times(vectors[i][k], vectors[j][k]) for k in sorted(set(vectors[i]) & set(vectors[j])))
          for j in range(size)] for i in range(size)]
    inv = inverse_of(g)
    h = [[radius if i == j else ZERO for j in range(size)] for i in range(size)]
    delta = largest(sum_q(row) for row in h)
    gamma = largest(sum_q(absolute(v) for v in row) for row in inv)
    return packed({'G': g, 'H': h, 'inverse': inv, 'delta': delta, 'gamma': gamma, 'rho': times(delta, gamma)})


def rows_to_strips(full_rows):
    return [{'row': row['row'], 'head': row['long'][:N], 'tail': row['long'][D:]} for row in full_rows]


def expected_fixture(case_id):
    """Independent transcription of immutable recipes, never primary outputs."""
    demand(type(case_id) is str and case_id in WHITE_CASES, 'DOMAIN', 'fixed white fixture case')
    if case_id == WHITE_CASES[9]:
        q = Q(1, 10**12); offset = Q(1, 10**24)
        pairs = [{'delta': scalar(v), 'ell': scalar(ONE)} for v in (minus(q, offset), q, plus(q, offset), ONE)]
        return {'schema': 'ri125-fabricated-bound-operands-v1', 'context': CONTEXT, 'case_id': case_id, 'pairs': pairs}
    size, length, stride = 1, 3, 2
    rows, gram, full, order = [], None, None, []
    if case_id in WHITE_CASES[:5]:
        if case_id in WHITE_CASES[:2]:
            dense = [[1, 0, -1]]
        else:
            size = 2
            scale = -1 if case_id == WHITE_CASES[3] else (2 if case_id == WHITE_CASES[4] else 1)
            dense = [[scale, 0, -scale], [0, scale, -scale]]
        vectors = [{j: Q(v) for j, v in enumerate(row) if v} for row in dense]
        rows = [{'row': i, 'head': [interval(Q(row[0]), Q(row[0]))],
                 'tail': [interval(Q(row[2]), Q(row[2]))]} for i, row in enumerate(dense)]
        gram = gram_of_vectors(vectors)
        order = [3 if case_id == WHITE_CASES[1] else 2]
    elif case_id in WHITE_CASES[5:8]:
        endpoints = {
            WHITE_CASES[5]: ((Q(1), Q(2)), (Q(-2), Q(-1))),
            WHITE_CASES[6]: ((Q(-1), Q(1)), (Q(-2), Q(2))),
            WHITE_CASES[7]: ((ZERO, ZERO), (ZERO, ZERO))}[case_id]
        rows = [{'row': 0, 'head': [interval(*endpoints[0])], 'tail': [interval(*endpoints[1])]}]
    elif case_id == WHITE_CASES[10]:
        size = 2
        rows = [
            {'row': 0, 'head': [interval(Q(1,3), Q(2,3))], 'tail': [interval(Q(-3,7), Q(-1,7))]},
            {'row': 1, 'head': [interval(Q(-2,5), Q(1,5))], 'tail': [interval(Q(2,11), Q(2,11))]}]
    elif case_id == WHITE_CASES[11]:
        size, length, stride = 8, T, D
        rows = [{'row': label, 'head': [interval(ZERO, ZERO) for _ in range(N)],
                 'tail': [interval(ZERO, ZERO) for _ in range(N)]} for label in ROW_IDS]
        specification = [
            (0,'head',0,Q(1,3),Q(2,3)), (0,'head',2768,Q(-1,5),Q(-1,5)),
            (0,'tail',0,Q(-3,7),Q(-1,7)), (0,'tail',2768,Q(2,11),Q(3,11)),
            (1,'head',0,Q(-2,5),Q(1,5)), (1,'head',2768,Q(1,13),Q(2,17)),
            (1,'tail',0,Q(2,11),Q(2,11)), (1,'tail',2768,Q(-1,19),Q(1,23)),
            (2,'head',1,Q(1,13),Q(1,13)), (2,'tail',1,Q(-1,17),Q(1,19))]
        for ordinal, strip, coordinate, low, high in specification:
            rows[ordinal][strip][coordinate] = interval(low, high)
    else:
        size, length, stride = 8, T, D
        full = prescribed_full_rows(case_id)
        vectors = exact_vectors(full)
        radius = ZERO
        if case_id in WHITE_CASES[12:]:
            q = Q(1,10**12)
            if case_id == WHITE_CASES[12]: q = minus(q, Q(1,10**24))
            if case_id == WHITE_CASES[14]: q = plus(q, Q(1,10**24))
            radius = quotient(times(Q(12), q), plus(Q(7), times(Q(6), q)))
        gram = gram_of_vectors(vectors, radius)
        rows = rows_to_strips(full)
        order = [7,6] if case_id == WHITE_CASES[8] else [7]
    return {'schema': 'ri125-fabricated-white-operands-v1', 'context': CONTEXT,
            'case_id': case_id, 'domain': {'r': size, 'T': length, 'd': stride},
            'strips': rows, 'gram': gram, 'n_order': order, 'full_rows': full}


def validate_fixture_bytes(body):
    operand = parse_json(body)
    demand(type(operand) is dict, 'SCHEMA', 'closed object keys')
    match(serialize(operand), body, 'CANONICAL', 'canonical fixture operand bytes')
    demand(type(operand.get('case_id')) is str, 'DOMAIN', 'fixed white fixture case')
    expected = expected_fixture(operand['case_id'])
    match(operand, expected, 'BINDING', 'complete independently prescribed white operand')
    if operand['schema'] == 'ri125-fabricated-bound-operands-v1':
        outputs = []
        for pair in operand['pairs']:
            delta, ell = decode_scalar(pair['delta']), decode_scalar(pair['ell'])
            eps, disposition = usefulness(delta, ell)
            outputs.append({'delta': scalar(delta), 'ell': scalar(ell), 'eps': scalar(eps), 'usefulness_state': disposition})
        return {'schema': 'ri125-fabricated-bound-result-v1', 'phase': 'fabricated_qualification',
                'context': CONTEXT, 'case_id': operand['case_id'], 'results': outputs,
                'historical_acceptance': None, 'physical_claim': False}
    domain = operand['domain']
    if operand['full_rows'] is not None:
        match(rows_to_strips(operand['full_rows']), operand['strips'], 'BINDING', 'full rows and strip endpoints')
        # Own prescribed Gram was recomputed from all exact rows, never input G alone.
        exact_vectors(operand['full_rows'])
    shift = build_shift(operand['strips'], length=domain['T'], stride=domain['d'])
    responses = [make_response(operand['gram'], shift, n=n) for n in operand['n_order']]
    check_recipe_anchors(operand, shift, responses)
    return {'schema': 'ri125-fabricated-white-primitive-v1', 'phase': 'fabricated_qualification',
            'context': CONTEXT, 'case_id': operand['case_id'], 'domain': domain,
            'gram': operand['gram'], 'shift': shift, 'responses': responses,
            'historical_acceptance': None, 'physical_claim': False}


def validate_pin(value):
    exact_keys(value, ('bytes', 'sha256'), 'INPUT')
    demand(type(value['bytes']) is int and 0 < value['bytes'] <= FILE_CAP, 'INPUT', 'positive bounded pin length')
    demand(type(value['sha256']) is str and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None,
           'INPUT', 'lowercase sha256')


def resolved_path(value):
    demand(type(value) is str, 'INPUT', 'path string')
    path = Path(value)
    demand(path.is_absolute() and str(path) == value and str(path.resolve()) == value,
           'INPUT', 'literal absolute nonsymlink path')
    return path


def reference_path(ref):
    exact_keys(ref, ('path', 'pin'), 'INPUT'); validate_pin(ref['pin'])
    return resolved_path(ref['path'])


def file_state(s):
    return s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size, s.st_mtime_ns, s.st_ctime_ns


def inspect_file(ref, remember=None, retain=False):
    path = reference_path(ref)
    begin = path.lstat()
    demand(stat.S_ISREG(begin.st_mode) and begin.st_nlink == 1, 'INPUT', 'regular single-link source or input')
    demand(0 < begin.st_size <= FILE_CAP, 'RESOURCE', 'file byte ceiling')
    stamp = file_state(begin)
    if remember is not None:
        demand(stamp == remember, 'CUSTODY', 'path state changed')
    collected = bytearray() if retain else None
    hasher, size = hashlib.sha256(), 0
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as file:
        demand(file_state(os.fstat(file.fileno())) == stamp, 'CUSTODY', 'opened file differs')
        while True:
            chunk = file.read(131072)
            if not chunk: break
            size += len(chunk)
            demand(size <= FILE_CAP, 'RESOURCE', 'stream byte ceiling')
            hasher.update(chunk)
            if retain: collected.extend(chunk)
        demand(file_state(os.fstat(file.fileno())) == stamp, 'CUSTODY', 'descriptor changed')
    demand(file_state(path.lstat()) == stamp, 'CUSTODY', 'closed path changed')
    match({'bytes': size, 'sha256': hasher.hexdigest()}, ref['pin'], 'INPUT', 'whole body pin')
    demand(size == begin.st_size, 'CUSTODY', 'complete file length')
    return (bytes(collected) if retain else None), stamp


class ReadSet:
    def __init__(self):
        self.members = []

    def add(self, role, ref):
        reference_path(ref)
        self.members.append({'role': role, 'reference': ref, 'initial': None})

    def begin(self):
        for member in self.members:
            _, member['initial'] = inspect_file(member['reference'])

    def final(self):
        results = []
        for member in self.members:
            try:
                inspect_file(member['reference'], remember=member['initial'])
                demand(member['initial'] is not None, 'CUSTODY', 'initial custody incomplete')
                results.append({'role': member['role'], 'pin': member['reference']['pin'], 'unchanged': True, 'error': None})
            except Exception as exc:
                results.append({'role': member['role'], 'pin': None, 'unchanged': False,
                                'error': (type(exc).__name__ + ': ' + str(exc))[:1024]})
        return results


class CaptureReader:
    """Independent streaming bracket/string framer, including array nesting."""
    def __init__(self, file):
        self.file = file; self.block = b''; self.at = 0
        self.hasher = hashlib.sha256(); self.size = 0

    def replenish(self):
        self.block = self.file.read(32768); self.at = 0
        self.hasher.update(self.block); self.size += len(self.block)
        demand(self.size <= FILE_CAP, 'RESOURCE', 'capture byte ceiling')

    def byte(self):
        if self.at == len(self.block):
            self.replenish()
        demand(bool(self.block), 'ROW', 'truncated capture')
        value = self.block[self.at]; self.at += 1
        return value

    def literal(self, token, message):
        for expected in token:
            demand(self.byte() == expected, 'ROW', message)

    def object_body(self):
        demand(self.byte() == 123, 'ROW', 'row start')
        body = bytearray(b'{'); stack = [125]
        quoted, escaped = False, False
        while stack:
            value = self.byte(); body.append(value)
            demand(len(body) <= ROW_CAP, 'RESOURCE', 'capture row byte ceiling')
            if quoted:
                if escaped: escaped = False
                elif value == 92: escaped = True
                elif value == 34: quoted = False
            elif value == 34:
                quoted = True
            elif value in (91,123):
                stack.append(93 if value == 91 else 125)
            elif value in (93,125):
                demand(value == stack[-1], 'ROW', 'balanced capture delimiters')
                stack.pop()
        return bytes(body)

    def exhausted(self):
        if self.at != len(self.block): return False
        self.replenish()
        return self.block == b''


def array_pin(values, name, domain):
    value = {'schema': 'ri73-exact-array-v1', 'label': name, 'domain': domain, 'values': values}
    return {'schema': value['schema'], 'label': name, 'domain': domain, **object_pin(value, compact=True)}


def row_summary(row, body, label):
    exact_keys(row, ('row', 'short', 'long'), 'ROW')
    match(row['row'], label, 'ROW', 'fixed row order')
    totals = {}
    for name, length in (('short', N), ('long', T)):
        lower, upper = ZERO, ZERO
        for box in items(row[name], length):
            a, b = decode_interval(box)
            lower, upper = plus(lower, a), plus(upper, b)
        totals[name] = lower, upper
    lower = minus(totals['long'][0], totals['short'][1])
    upper = minus(totals['long'][1], totals['short'][0])
    demand(cmp(lower, ZERO) <= 0 and cmp(upper, ZERO) >= 0, 'ROW', 'constant sum enclosure')
    head, tail = row['long'][:N], row['long'][D:]
    return {'strip': {'row': label, 'head': head, 'tail': tail},
            'vectors': {'row': label, 'short': array_pin(row['short'], 'short', {'length': N, 'row': label}),
                        'long': array_pin(row['long'], 'long', {'length': T, 'row': label, 'seed': L+label})},
            'row_identity': {'row': label, 'source_row_pin': content_pin(body), 'short_count': N,
                'long_count': T, 'head_pin': object_pin(head), 'tail_pin': object_pin(tail),
                'a_row_sum_interval': interval(lower, upper), 'contains_zero': True}}


def stream_capture(ref, fabricated=False):
    demand(type(fabricated) is bool, 'PHASE', 'explicit capture phase')
    if fabricated:
        demand(not equal_types(ref.get('pin'), FIXED['capture']), 'PHASE', 'actual capture forbidden in fabrication')
    _, before = inspect_file(ref)
    path = reference_path(ref)
    header = b'{"dimensions":' + serialize({'N':N,'L':L,'T':T}, True) + b',"row_order":' + serialize(list(ROW_IDS), True) + b',"rows":['
    with os.fdopen(os.open(path, os.O_RDONLY | os.O_NOFOLLOW), 'rb') as file:
        demand(file_state(os.fstat(file.fileno())) == before, 'CUSTODY', 'capture descriptor initial')
        reader = CaptureReader(file)
        reader.literal(header, 'literal capture header')
        for index, label in enumerate(ROW_IDS):
            if index: reader.literal(b',', 'row separator')
            body = reader.object_body(); row = parse_json(body)
            match(serialize(row, True), body, 'CANONICAL', 'compact row encoding')
            result = row_summary(row, body, label)
            del row, body
            yield result
            del result
        schema = 'ri125-fabricated-capture-v1' if fabricated else 'ri73-reconstructed-intervals-v1'
        reader.literal(b'],"schema":' + serialize(schema, True) + b'}', 'capture footer and ninth-row exhaustion')
        demand(reader.exhausted(), 'ROW', 'trailing capture bytes')
        match({'bytes':reader.size,'sha256':reader.hasher.hexdigest()}, ref['pin'], 'INPUT', 'complete consumed capture pin')
        demand(file_state(os.fstat(file.fileno())) == before, 'CUSTODY', 'capture descriptor final')
    inspect_file(ref, remember=before)


def match_row(item, reconstruction, index):
    match(item['vectors'], reconstruction['vector_identities'][index], 'BINDING', 'capture vector identity tied to accepted RI73 result')
    match(item['row_identity']['a_row_sum_interval'], reconstruction['constant_row_sum_intervals'][index],
          'BINDING', 'complete row sum tied to accepted RI73 result')


def rebuild_from_capture(ref, gram, reconstruction=None, fabricated=False):
    generator = stream_capture(ref, fabricated)
    strips, identities = [], []
    try:
        for index, label in enumerate(ROW_IDS):
            try: item = next(generator)
            except StopIteration as exc: raise Refusal('ROW','missing full row') from exc
            match(item['strip']['row'], label, 'ROW', 'assembly row order')
            if not fabricated: match_row(item, reconstruction, index)
            strips.append(item['strip']); identities.append(item['row_identity'])
        sentinel = object()
        demand(next(generator, sentinel) is sentinel, 'ROW', 'extra ninth row')
    finally:
        generator.close()
    shift = build_shift(strips, length=T, stride=D)
    responses = [make_response(gram, shift, n=n) for n in (7,6)]
    return identities, shift, responses


def validate_fabricated_assembly(capture_ref, gram, case_id, context):
    match(context, CONTEXT, 'PHASE', 'fabricated context')
    demand(type(case_id) is str and case_id in ('W09_production_boundary_sparse','J01_four_rows_exact','J02_precision_inconclusive'),
           'DOMAIN', 'fixed fabricated assembly case')
    full = prescribed_full_rows(case_id)
    radius = Q(2,10**12) if case_id == 'J02_precision_inconclusive' else ZERO
    expected_gram = gram_of_vectors(exact_vectors(full), radius)
    match(gram, expected_gram, 'BINDING', 'complete fabricated Gram from exact full rows')
    expected_capture = {'dimensions':{'N':N,'L':L,'T':T},'row_order':list(ROW_IDS),
                        'rows':full,'schema':'ri125-fabricated-capture-v1'}
    match(capture_ref.get('pin'), object_pin(expected_capture, True), 'BINDING', 'independently prescribed full fabricated capture')
    del expected_capture, full
    identities, shift, responses = rebuild_from_capture(capture_ref, gram, fabricated=True)
    return {'schema':'ri125-fabricated-white-assembly-v1','phase':'fabricated_qualification',
            'case_id':case_id,'context':CONTEXT,'capture':capture_ref['pin'],'gram':gram,
            'row_identities':identities,'shift':shift,'white_responses':responses,
            'historical_acceptance':None,'physical_claim':False}

INPUT_NAMES = ('capture','ri73_result','ri73_source','ri73_reconciliation','ri73_final_review','ri73_audit_freeze')
SOURCE_NAMES = ('design','contract','primary','white_kernel','validator','qualifier','cases','kernel_refusals','white_refusals','fabricated_interfaces')
RUNTIME_NAMES = ('fingerprint','inventory','interpreter')
FIXED = {
 'capture': {'bytes':51891508,'sha256':'fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba'},
 'ri73_result': {'bytes':11180937,'sha256':'3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe'},
 'ri73_source': {'bytes':68018,'sha256':'574f5f1b8900221a47bc30ea62e6bed378a8fd1c8b4aa904e0549ade8ceb2887'},
 'ri73_reconciliation': {'bytes':2098,'sha256':'5263ab139542d6591af03300ded7f2d7c9fba5fd3585347b4f7b4bfb7605f232'},
 'ri73_final_review': {'bytes':5479,'sha256':'c4ac724cbde99d98b3b95f51fcf030a9ac00e48fd7aafa8998356e0f3a9eea1e'},
 'ri73_audit_freeze': {'bytes':31442,'sha256':'a10dd521e72e6cecbc55a5c35720a4d6755daebc9f1d07ecd5553af220402581'}}
DESIGN = {'bytes':31586,'sha256':'4e725c42d77097e66b5b5cf5c3cc014f97b2a42663b0ef0ee3f78d8b4161699b'}
DESIGN_ACCEPTANCE = {'bytes':2948,'sha256':'2963dbd483539f90ef52b744e93b52451265975cbd041ff2d59df26f0d94936a'}
# Literal historical protocol data, not imported primary code or new executions.
HISTORICAL_GATES = (
 'fixture:fir','fixture:cancellation','fixture:singleton','fixture:offdiagonal_small',
 'fixture:offdiagonal_large','fixture:failed_gate','fixture:midpoint','fixture:rank_ambiguity','fixture:singular','fixture:output_law',
 'refusal:float_endpoint','refusal:bool_endpoint','refusal:nonfinite_endpoint','refusal:reversed_interval','refusal:negative_radius',
 'refusal:matrix_rows','refusal:bool_dimension','refusal:bool_row_dimension','refusal:matrix_columns','refusal:ragged_box',
 'refusal:asymmetric_gram','refusal:asymmetric_error','refusal:negative_error','refusal:negative_pivot','refusal:wrong_ldl',
 'refusal:wrong_inverse','refusal:wrong_delta','refusal:wrong_gamma','refusal:incorrect_rank','refusal:bool_rank',
 'refusal:wrong_mp1','refusal:wrong_mp2','refusal:wrong_mp3','refusal:off_support','refusal:negative_rho','refusal:rho_at_one',
 'refusal:negative_output_error','refusal:unqualified_cdf','refusal:cdf_series_domain','refusal:negative_cdf_argument',
 'refusal:estimated_covariance','refusal:colored_covariance','refusal:fraction_numerator_cap','refusal:fraction_denominator_cap',
 'refusal:operation_result_cap','refusal:hex_length','refusal:hex_plus','refusal:hex_negative_zero','refusal:hex_leading_zero',
 'refusal:hex_denominator_zero','refusal:hex_unreduced','refusal:work_cap','refusal:work_bool','refusal:output_cap',
 'refusal:duplicate_json','refusal:nonfinite_json','refusal:overflow_json','refusal:changed_snapshot','refusal:bool_pin',
 'refusal:changed_runtime','refusal:changed_runtime_build','refusal:failed_receipt','refusal:incomplete_receipt',
 'refusal:changed_receipt_engine','refusal:changed_arithmetic','refusal:wrong_padding','refusal:bool_padding',
 'refusal:changed_manifest_coefficient','refusal:changed_manifest_stage_order','refusal:changed_manifest_padding',
 'refusal:missing_rows','refusal:wrong_rows','refusal:wrong_snapshot_shape','refusal:missing_expected_summaries',
 'integration:reconstruction','integration:gram','integration:mathematical','integration:accuracy','integration:cross',
 'probe:zero','probe:constant','probe:0','probe:1','probe:27','probe:805','probe:1384','probe:2741','probe:2767','probe:2768',
 'integration:law','integration:final_custody','completion:custody')
CHECK_IDS = ('admission:phase','admission:inputs','admission:source','operator:gram','operator:capture','operator:rows',
             'shift:direct','shift:polarization','response:7','trace:7','structural:7','accuracy:7',
             'response:6','trace:6','structural:6','accuracy:6','completion:stable')
LIMITATIONS = [
 'Conditional conventional moments of fixed operators and explicitly postulated joint laws only.',
 'Numerical enclosure and usefulness bounds are not statistical or physical model error.',
 'All four public development/calibration scenarios remain unchanged and are not protected validation.',
 'Shared-white amplitude and population mean are unresolved; sample centering does not establish zero population mean.',
 'Exact periodic repetition is a hypothetical completion, not established detector noise.',
 'Nominal V2/C02, blank Yunits, clear L1 NO_CW_HW_INJ, possible injection effects and below-10-Hz calibration remain unresolved.',
 'No significance, fitted model, calibrated measurement, native forward map or geometry/gravity result is established; RET remains paused.']
LIMITS = {'seconds':180,'sampled_rss_kib':524288,'poll_ms':25,'max_gap_ms':100,'ps_timeout_ms':50}


def historical_gram(report):
    exact_keys(report, ('schema_version','mode','status','full_integration_qualified','source_identity','dependencies','runtime',
        'inherited_arithmetic_contract','resource_contract','model','dimensions','rows','sample_spacing','gate_inventory','gate_counts','gates',
        'deterministic_fixture_admission_passed','sampling_performed','admitted_coefficient_design_requested',
        'reconstructed_rows_admitted','exact_scalar_encoding','scope'), 'RI73')
    headers = [
        ('schema_version','ri73-unit-white-operator-covariance-v1'),('mode','fixed_operator_covariance'),
        ('status','fixed_operator_covariance_passed'),('full_integration_qualified',True),('source_identity',FIXED['ri73_source']),
        ('dimensions',{'N':N,'L':L,'T':T}),('rows',list(ROW_IDS)),('sample_spacing',scalar(Q(1,4096))),
        ('model',{'kind':'known_synthetic_unit_white','mean':'zero','covariance':'I_T','input_dimension':T,'output_dimension':8}),
        ('gate_inventory',list(HISTORICAL_GATES)),('gate_counts',{'total':92,'passed':92,'failed':0}),
        ('deterministic_fixture_admission_passed',True),('sampling_performed',False),
        ('admitted_coefficient_design_requested',True),('reconstructed_rows_admitted',True)]
    for name, value in headers:
        match(report[name], value, 'RI73', 'full inherited header ' + name)
    details = {}
    gate_rows = items(report['gates'], 92)
    for index, identifier in enumerate(HISTORICAL_GATES):
        gate = gate_rows[index]
        exact_keys(gate, ('id','passed','detail'), 'RI73')
        match(gate['id'], identifier, 'RI73', 'literal 92-gate order')
        demand(gate['passed'] is True and type(gate['detail']) is dict,
               'RI73', 'all inherited gates passed with details')
        details[identifier] = gate['detail']
    reconstruction = details['integration:reconstruction']
    exact_keys(reconstruction, ('adjoints_reconstructed','summaries_reconciled','row_state_identity','row_summaries',
        'vector_identities','A_identity','P_identity','Q_identity','constant_row_sum_intervals','coefficient_arrays_stored_in_result'), 'RI73')
    match(reconstruction['adjoints_reconstructed'],16,'RI73','all reconstructed adjoints')
    match(reconstruction['summaries_reconciled'],8,'RI73','all row summaries')
    match(reconstruction['coefficient_arrays_stored_in_result'],False,'RI73','external complete capture')
    items(reconstruction['vector_identities'],8); items(reconstruction['constant_row_sum_intervals'],8)
    detail = details['integration:gram']
    exact_keys(detail, ('certificate','M_identity','R_identity'), 'RI73')
    cert = detail['certificate']
    exact_keys(cert, ('mathematical_gate','accuracy_gate','rho_limit','G','H','delta','eta2','ldl','inverse',
        'left_inverse_product','right_inverse_product','gamma','rho','status','rank','inverse_error_norm_bound','inverse_lower','inverse_upper'), 'RI73')
    for name, value in [('status','certified'),('rank',8),('mathematical_gate',True),('accuracy_gate',True),('rho_limit',scalar(Q(1,10**12)))]:
        match(cert[name],value,'RI73','accepted inherited certificate '+name)
    for suffix, key, value in [('mathematical','strict_limit',ONE),('accuracy','inclusive_limit',Q(1,10**12))]:
        match(details['integration:'+suffix], {'status':'certified','acceptance':{'passed':True},'rho':cert['rho'],key:scalar(value)},
              'RI73','inherited acceptance details')
    gram = {name:cert[name] for name in GRAM_FIELDS}
    check_gram(gram,8)
    return gram, object_pin(detail), reconstruction


def request_references(request, selection, candidate=False):
    exact_keys(request, ('schema','phase','inputs','sources','design_acceptance','qualification','custody','runtime','admission','output'))
    match(request['phase'],'fixed_saved_application','PHASE','actual phase before body decoding')
    match(request['schema'],'ri125-white-request-v1','SCHEMA','white request schema')
    exact_keys(request['inputs'],INPUT_NAMES,'INPUT'); exact_keys(request['sources'],SOURCE_NAMES,'SOURCE')
    exact_keys(request['runtime'],RUNTIME_NAMES,'SOURCE')
    for name in INPUT_NAMES:
        reference_path(request['inputs'][name]); match(request['inputs'][name]['pin'],FIXED[name],'INPUT','fixed historical pin '+name)
    for name in SOURCE_NAMES: reference_path(request['sources'][name])
    match(request['sources']['design']['pin'],DESIGN,'SOURCE','accepted RI123 design')
    for name in ('design_acceptance','qualification','custody','admission'): reference_path(request[name])
    match(request['design_acceptance']['pin'],DESIGN_ACCEPTANCE,'SOURCE','RI123 root acceptance')
    for name in RUNTIME_NAMES: reference_path(request['runtime'][name])
    exact_keys(selection,('primary','white_kernel','validator'),'SOURCE')
    for name in selection: resolved_path(selection[name])
    match(request['sources']['primary']['path'],selection['primary'],'SOURCE','loaded primary path')
    match(request['sources']['white_kernel']['path'],selection['white_kernel'],'SOURCE','loaded kernel path')
    match(request['sources']['validator']['path'],selection['validator'],'SOURCE','loaded validator path')
    output = resolved_path(request['output'])
    demand(output.parent.is_dir() and (candidate or not os.path.lexists(output)), 'OUTPUT','exclusive absent output')
    refs = [('input:'+name,request['inputs'][name]) for name in INPUT_NAMES]
    refs.extend(('source:'+name,request['sources'][name]) for name in SOURCE_NAMES)
    refs.extend((name,request[name]) for name in ('design_acceptance','qualification','custody','admission'))
    refs.extend(('runtime:'+name,request['runtime'][name]) for name in RUNTIME_NAMES)
    demand(len({x['path'] for _,x in refs}) == len(refs),'INPUT','distinct required file paths')
    demand(request['output'] not in {x['path'] for _,x in refs},'OUTPUT','output/input alias')
    return refs


def primary_admission(card, request):
    expected = {'schema':'ri125-white-admission-v1','phase':'fixed_saved_application','status':'ROOT_ADMITS_ONE_WHITE_RUN',
        'inputs':{name:ref['pin'] for name,ref in request['inputs'].items()},
        'sources':{name:ref['pin'] for name,ref in request['sources'].items()},
        'design_acceptance':request['design_acceptance']['pin'],'qualification':request['qualification']['pin'],
        'custody':request['custody']['pin'],'runtime':{name:ref['pin'] for name,ref in request['runtime'].items()},
        'output':request['output'],'limits':dict(LIMITS),'history_and_runtime_adjudicated_by_root':True,
        'protected_validation':False,'physical_covariance_accepted':False,'ret_paused':True}
    match(card,expected,'ADMISSION','exact root-bound card')


def expected_actual(request, gram, detail_pin, identities, shift, responses):
    state = 'enclosure_and_usefulness_passed' if all(r['usefulness_state']=='usefulness_passed' for r in responses) else 'enclosure_valid_accuracy_failed'
    accuracy = {'accuracy:'+str(r['n']):r['usefulness_state']=='usefulness_passed' for r in responses}
    checks = [{'id':name,'passed':accuracy.get(name,True)} for name in CHECK_IDS]
    passed = sum(1 for row in checks if row['passed'])
    return {'schema':'ri125-white-coupling-v1','phase':'fixed_saved_application','status':state,
        'method':{'model':'shared_raw_white_unit_response','dimensions':{'r':8,'N':N,'L':L,'T':T,'M':16384,'d':D,'raw_samples':131072,'fs':4096},
            'rows':list(ROW_IDS),'n_order':[7,6],'crop':'first_T','integer_bit_limit':BITS,'precision_limit':scalar(Q(1,10**12)),
            'centering':'divisor_n_shared_samples'},
        'provenance':{'sources':{name:ref['pin'] for name,ref in request['sources'].items()},
            'inputs':[{'role':name,'pin':request['inputs'][name]['pin']} for name in INPUT_NAMES],
            'acceptance':{'design':request['design_acceptance']['pin'],'qualification':request['qualification']['pin'],
                'custody':request['custody']['pin'],'dependencies':[{'role':name,'pin':request['inputs'][name]['pin']}
                    for name in ('ri73_reconciliation','ri73_final_review','ri73_audit_freeze')]
                    +[{'role':'one_run_admission','pin':request['admission']['pin']}]},
            'runtime':{name:ref['pin'] for name,ref in request['runtime'].items()}},
        'operator':{'capture':request['inputs']['capture']['pin'],'ri73_result':request['inputs']['ri73_result']['pin'],
            'ri73_gram_detail':detail_pin,'shape':[8,T],'row_identities':identities,'gram':gram,
            'inherited_gate_inventory':list(HISTORICAL_GATES),'inherited_gates_all_passed':True},
        'shift':shift,'white_responses':responses,
        'checks':{'inventory':list(CHECK_IDS),'counts':{'total':len(checks),'passed':passed,'failed':len(checks)-passed},'results':checks},
        'limitations':list(LIMITATIONS)}


def write_new_output(path_value, value):
    path = resolved_path(path_value)
    parent_before = path.parent.lstat()
    demand(path.parent.is_dir() and not os.path.lexists(path), 'OUTPUT', 'output absent before exclusive open')
    hasher, count = hashlib.sha256(), 0
    with os.fdopen(os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600),'wb') as file:
        for chunk in serialized_parts(value):
            demand(file.write(chunk)==len(chunk),'OUTPUT','complete output write')
            hasher.update(chunk); count += len(chunk)
        file.flush(); os.fsync(file.fileno()); observed = file_state(os.fstat(file.fileno()))
    demand(file_state(path.lstat())==observed,'CUSTODY','output descriptor/path binding')
    parent_after = path.parent.lstat()
    demand((parent_before.st_dev,parent_before.st_ino)==(parent_after.st_dev,parent_after.st_ino),'CUSTODY','output parent identity')
    pin = {'bytes':count,'sha256':hasher.hexdigest()}
    inspect_file({'path':path_value,'pin':pin},remember=observed)
    return pin


def finish_validation(first, result, output_pin, postchecks):
    if first is None and any(row['unchanged'] is not True for row in postchecks):
        first = Refusal('CUSTODY','one or more final source/input postchecks failed')
    if first is None:
        return {'result':result,'output_pin':output_pin,'refusal':None,'postchecks':postchecks}
    refusal = {'schema':'ri125-application-refusal-v1','status':'REFUSED','phase':'fixed_saved_application','stage':'white',
        'code':first.code if isinstance(first,Refusal) else 'FAILURE',
        'message':(type(first).__name__+': '+str(first))[:1024],
        'scientific_disposition_emitted':False,'postchecks':postchecks}
    return {'result':None,'output_pin':output_pin,'refusal':refusal,'postchecks':postchecks}


def request_bytes_check(body, frozen_pin):
    validate_pin(frozen_pin)
    match(content_pin(body),frozen_pin,'INPUT','externally frozen request bytes')
    return parse_json(body)


def validate_saved_white(request_body, request_pin, candidate_ref, binding_body, binding_pin):
    """Prospective separately admitted actual validation; never self-authorizing.

    The binding is supplied as exact externally frozen bytes by the root caller.
    It contains no executable instruction. No actual call is authorized here.
    Success reconstructs every field and preserves the whole independent result.
    """
    readset, first, report, output_pin = ReadSet(), None, None, None
    try:
        request = request_bytes_check(request_body,request_pin)
        validate_pin(binding_pin)
        match(content_pin(binding_body),binding_pin,'INPUT','externally frozen validation binding')
        binding = parse_json(binding_body)
        exact_keys(binding,('schema','phase','status','primary_request','candidate','sources','inputs','qualification','custody',
            'runtime','selection','output','limits','history_and_runtime_adjudicated_by_root','protected_validation','ret_paused'),'ADMISSION')
        selection = binding['selection']
        refs = request_references(request,selection,candidate=True)
        reference_path(candidate_ref)
        match(candidate_ref['path'],request['output'],'BINDING','candidate is the primary exclusive output')
        match(selection['validator'],str(Path(__file__).resolve()),'SOURCE','loaded validator path')
        expected_binding = {'schema':'ri125-white-independent-validation-admission-v1','phase':'fixed_saved_application',
            'status':'ROOT_ADMITS_ONE_WHITE_VALIDATION','primary_request':request_pin,'candidate':candidate_ref,
            'sources':{k:v['pin'] for k,v in request['sources'].items()},'inputs':{k:v['pin'] for k,v in request['inputs'].items()},
            'qualification':request['qualification']['pin'],'custody':request['custody']['pin'],
            'runtime':{k:v['pin'] for k,v in request['runtime'].items()},'selection':selection,
            'output':binding['output'],'limits':dict(LIMITS),'history_and_runtime_adjudicated_by_root':True,
            'protected_validation':False,'ret_paused':True}
        match(binding,expected_binding,'ADMISSION','exact independent root-bound validation card')
        output = resolved_path(binding['output'])
        demand(output.parent.is_dir() and not os.path.lexists(output),'OUTPUT','exclusive absent output')
        refs.append(('candidate',candidate_ref))
        demand(len({r['path'] for _,r in refs})==len(refs) and str(output) not in {r['path'] for _,r in refs},
               'INPUT','distinct validation input and output paths')
        for role, ref in refs: readset.add(role,ref)
        readset.begin()
        admission,_ = inspect_file(request['admission'],retain=True)
        primary_admission(parse_json(admission),request); del admission
        source,_ = inspect_file(request['inputs']['ri73_result'],retain=True)
        gram,detail_pin,reconstruction = historical_gram(parse_json(source)); del source
        identities,shift,responses = rebuild_from_capture(request['inputs']['capture'],gram,reconstruction)
        del reconstruction
        independent = expected_actual(request,gram,detail_pin,identities,shift,responses)
        candidate_body,_ = inspect_file(candidate_ref,retain=True)
        candidate = parse_json(candidate_body)
        match(serialize(candidate),candidate_body,'CANONICAL','canonical actual candidate')
        match(candidate,independent,'COMPARISON','complete independently reconstructed white result')
        # Complete independent output retained, rather than an uninspectable success bit.
        report = {'schema':'ri125-independent-white-validation-v1','status':'complete_white_result_independently_matches',
            'phase':'fixed_saved_application','candidate':candidate_ref['pin'],'primary_request':request_pin,
            'validation_binding':binding_pin,'reconstructed_result':independent,
            'reconstructed_canonical_identity':object_pin(independent),
            'independent_arithmetic':'reduced_integer_pairs_per_coordinate_endpoint_products',
            'actual_physical_claim':False,'programme_complete':False,'ret_paused':True}
        output_pin = write_new_output(str(output),report)
        readset.add('independent_output',{'path':str(output),'pin':output_pin})
        _,readset.members[-1]['initial'] = inspect_file(readset.members[-1]['reference'])
    except Exception as exc:
        first = exc
    return finish_validation(first,report,output_pin,readset.final())


def check_recipe_anchors(operand, shift, responses):
    """Manual recipe consequences supplement full independent reconstruction."""
    case = operand['case_id']
    if case == WHITE_CASES[10]:
        match(shift['error'][0][1],scalar(Q(1,7)),'FIXTURE','W11 asymmetric forward error')
        match(shift['error'][1][0],scalar(Q(1,33)),'FIXTURE','W11 asymmetric reverse error')
    if case == WHITE_CASES[5]:
        match(shift['center'],[[scalar(Q(-9,4))]],'FIXTURE','W06 center')
        match(shift['error'],[[scalar(Q(7,4))]],'FIXTURE','W06 all three errors')
        match(shift['direct'],[[interval(Q(-4),Q(-1))]],'FIXTURE','W06 retained direct box')
    if case == WHITE_CASES[8]:
        match(shift['trace_center'],scalar(Q(-1)),'FIXTURE','W09 complete overlap trace')
        match(shift['center'][0][0],scalar(Q(2)),'FIXTURE','W09 first overlap coordinate')
        match(shift['center'][1][1],scalar(Q(-3)),'FIXTURE','W09 last overlap coordinate')
    if case in WHITE_CASES[12:]:
        target = Q(1,10**12)
        if case == WHITE_CASES[12]: target = minus(target,Q(1,10**24))
        if case == WHITE_CASES[14]: target = plus(target,Q(1,10**24))
        match(responses[0]['eps'],scalar(target),'FIXTURE','full response boundary derived eps')
        expected = 'accuracy_failed' if case == WHITE_CASES[14] else 'usefulness_passed'
        match(responses[0]['usefulness_state'],expected,'FIXTURE','full response inclusive boundary')
        demand(cmp(decode_scalar(operand['gram']['rho']),Q(1,10**12))<0,
               'FIXTURE','full response keeps inherited rho strictly below threshold')
