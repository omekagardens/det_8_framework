"""RI125 primary exact white-strip kernels: unexecuted source preparation.

No import-time I/O, actual operand admission, historical result parsing or
qualification is implemented here. Complete fixed wrappers and an independently
authored validator remain mandatory. These pure kernels accept explicit declared
operands; they never claim their provenance or physical adequacy.
"""
from fractions import Fraction as F
import math
import re

BITS = 262144
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
HEX = re.compile(r'(?:0|-?[1-9a-f][0-9a-f]*)\Z')
SHIFT_KEYS = ('orientation', 'center', 'error', 'direct',
              'midpoint_polarization', 'trace_center', 'trace_error')
GRAM_KEYS = ('G', 'H', 'delta', 'inverse', 'gamma', 'rho')


class ApplicationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def need(value, code, message):
    if not value:
        raise ApplicationError(code, message)


def keys(value, expected):
    need(type(value) is dict and all(type(k) is str for k in value)
         and set(value) == set(expected), 'SCHEMA', 'closed object keys')


def sequence(value, length):
    need(type(value) is list and len(value) == length, 'SHAPE', 'exact list length')
    return value


def integer(value):
    need(type(value) is int, 'EXACT', 'plain integer required')
    need(abs(value).bit_length() <= BITS, 'RESOURCE', 'integer bit ceiling')
    return value


def rational(value):
    need(type(value) is F, 'EXACT', 'Fraction required')
    integer(value.numerator)
    integer(value.denominator)
    return value


def add(a, b):
    return rational(rational(a) + rational(b))


def sub(a, b):
    return rational(rational(a) - rational(b))


def mul(a, b):
    return rational(rational(a) * rational(b))


def div(a, b):
    rational(a)
    rational(b)
    need(b != 0, 'ZERO_DIVISOR', 'division by zero')
    return rational(a / b)


def total(values):
    answer = F(0)
    for value in values:
        answer = add(answer, value)
    return answer


def hex_integer(value):
    need(type(value) is str, 'EXACT', 'hex string required')
    need(len(value) <= 65537, 'RESOURCE', 'integer text ceiling')
    need(HEX.fullmatch(value) is not None, 'EXACT', 'canonical signed hex')
    return integer(int(value, 16))


def scalar(value):
    rational(value)
    return [format(value.numerator, 'x'), format(value.denominator, 'x')]


def unscalar(value):
    sequence(value, 2)
    n, d = map(hex_integer, value)
    need(d > 0 and math.gcd(n, d) == 1, 'EXACT', 'reduced positive denominator')
    return rational(F(n, d))


def interval(low, high):
    rational(low)
    rational(high)
    need(low <= high, 'INTERVAL', 'ordered endpoints')
    return [scalar(low), scalar(high)]


def uninterval(value):
    low, high = map(unscalar, sequence(value, 2))
    need(low <= high, 'INTERVAL', 'ordered endpoints')
    return low, high


def encode(value):
    if type(value) is F:
        return scalar(value)
    if type(value) in (list, tuple):
        return [encode(v) for v in value]
    if type(value) is dict:
        return {k: encode(v) for k, v in value.items()}
    need(type(value) in (str, int, bool) or value is None, 'EXACT', 'encoded type')
    return value


def matrix(value, size):
    return [[unscalar(v) for v in sequence(row, size)]
            for row in sequence(value, size)]


def zero_matrix(size):
    return [[F(0) for _ in range(size)] for _ in range(size)]


def trace(value):
    return total(value[i][i] for i in range(len(value)))


def dot(left, right):
    need(len(left) == len(right), 'SHAPE', 'dot lengths')
    return total(mul(a, b) for a, b in zip(left, right))


def lifted(intervals):
    """Checked common denominator, preserving every endpoint independently."""
    denominator = 1
    for low, high in intervals:
        rational(low)
        rational(high)
        need(low <= high, 'INTERVAL', 'ordered endpoints')
        denominator = integer(math.lcm(denominator, low.denominator,
                                       high.denominator))
    lo = [integer(v[0].numerator * (denominator // v[0].denominator))
          for v in intervals]
    hi = [integer(v[1].numerator * (denominator // v[1].denominator))
          for v in intervals]
    return lo, hi, denominator


def product_entry(u, h):
    """Ordered tail/head midpoint, deterministic error, direct box, polarization."""
    ul, uh, ud = u
    hl, hh, hd = h
    need(len(ul) == len(uh) == len(hl) == len(hh) and len(ul) > 0,
         'SHAPE', 'strip product lengths')
    den = integer(ud * hd)
    four_den = integer(4 * den)
    common = integer(math.lcm(ud, hd))
    pol_den = integer(16 * integer(common * common))
    center_num = error_num = lower_num = upper_num = polarization_num = 0
    for a, b, c, d in zip(ul, uh, hl, hh):
        um, ur = integer(a + b), integer(b - a)
        hm, hr = integer(c + d), integer(d - c)
        need(ur >= 0 and hr >= 0, 'INTERVAL', 'negative lifted radius')
        center_num = integer(center_num + integer(um * hm))
        first = integer(abs(um) * hr)
        second = integer(ur * abs(hm))
        third = integer(ur * hr)
        error_num = integer(error_num + integer(integer(first + second) + third))
        products = [integer(a * c), integer(a * d), integer(b * c), integer(b * d)]
        lower_num = integer(lower_num + min(products))
        upper_num = integer(upper_num + max(products))
        pu = integer(um * (common // ud))
        ph = integer(hm * (common // hd))
        plus, minus = integer(pu + ph), integer(pu - ph)
        term = integer(integer(plus * plus) - integer(minus * minus))
        polarization_num = integer(polarization_num + term)
    center = rational(F(center_num, four_den))
    error = rational(F(error_num, four_den))
    low, high = rational(F(lower_num, den)), rational(F(upper_num, den))
    polarization = rational(F(polarization_num, pol_den))
    need(center == polarization, 'POLARIZATION', 'midpoint identity differs')
    need(max(low, sub(center, error)) <= min(high, add(center, error)),
         'DIRECT', 'direct and midpoint-radius boxes disjoint')
    return center, error, (low, high), polarization


def derive_shift(rows, *, length, stride):
    """Pure explicit-strip operation, not full-capture or phase admission."""
    need(type(rows) is list, 'SHAPE', 'strip rows list')
    size = len(rows)
    need(type(length) is int and type(stride) is int
         and (size, length, stride) in ((1, 3, 2), (2, 3, 2), (8, 10961, 8192)),
         'DOMAIN', 'fixed primitive domain')
    labels = list(ROWS) if size == 8 else list(range(size))
    width = length - stride
    heads, tails = [], []
    for label, row in zip(labels, rows):
        keys(row, ('row', 'head', 'tail'))
        need(type(row['row']) is int and row['row'] == label, 'ROW', 'row order')
        head = [uninterval(v) for v in sequence(row['head'], width)]
        tail = [uninterval(v) for v in sequence(row['tail'], width)]
        heads.append(lifted(head))
        tails.append(lifted(tail))
    center, error, polarization = (zero_matrix(size) for _ in range(3))
    direct = [[None for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for k in range(size):
            center[i][k], error[i][k], direct[i][k], polarization[i][k] = (
                product_entry(tails[i], heads[k]))
    return encode({'orientation': 'earlier_tail_times_later_head_transpose',
                   'center': center, 'error': error, 'direct': direct,
                   'midpoint_polarization': polarization,
                   'trace_center': trace(center), 'trace_error': trace(error)})


def positive_ldl(g):
    """Small recorded-Gram consistency check, not a coefficient reconstruction."""
    size = len(g)
    lower = zero_matrix(size)
    diagonal = [F(0) for _ in range(size)]
    for i in range(size):
        lower[i][i] = F(1)
        for j in range(i):
            held = total(mul(mul(lower[i][k], lower[j][k]), diagonal[k])
                         for k in range(j))
            lower[i][j] = div(sub(g[i][j], held), diagonal[j])
        diagonal[i] = sub(g[i][i], total(mul(mul(lower[i][k], lower[i][k]),
                                            diagonal[k]) for k in range(i)))
        need(diagonal[i] > 0, 'GRAM', 'nonpositive inherited Gram pivot')


def inherited_gram(value, size):
    keys(value, GRAM_KEYS)
    g, h, inverse = (matrix(value[key], size) for key in ('G', 'H', 'inverse'))
    delta, gamma, rho = (unscalar(value[key]) for key in ('delta', 'gamma', 'rho'))
    for i in range(size):
        for j in range(size):
            need(g[i][j] == g[j][i] and h[i][j] == h[j][i]
                 and inverse[i][j] == inverse[j][i] and h[i][j] >= 0,
                 'GRAM', 'symmetric Gram/inverse and nonnegative bound')
            left = total(mul(g[i][k], inverse[k][j]) for k in range(size))
            right = total(mul(inverse[i][k], g[k][j]) for k in range(size))
            need(left == right == F(int(i == j)), 'GRAM', 'both inverse products')
    positive_ldl(g)
    need(delta == max(total(row) for row in h), 'GRAM', 'delta row-sum bound')
    need(gamma == max(total(abs(v) for v in row) for row in inverse)
         and gamma > 0, 'GRAM', 'gamma inverse row-sum bound')
    need(rho == mul(delta, gamma) and F(0) <= rho <= F(1, 10**12),
         'GRAM', 'unchanged inherited rho gate')
    return g, h, gamma, rho


def usefulness(delta, ell):
    rational(delta)
    rational(ell)
    need(delta >= 0 and ell > 0, 'BOUND', 'nonnegative error, positive lower bound')
    eps = div(delta, ell)
    return eps, ('usefulness_passed' if eps <= F(1, 10**12) else 'accuracy_failed')


def derive_response(gram, shift, *, n):
    """Conditional response from a separately authenticated Gram and own shift."""
    need(type(n) is int and n in (2, 3, 6, 7), 'DOMAIN', 'fixed window count')
    keys(shift, SHIFT_KEYS)
    need(shift['orientation'] == 'earlier_tail_times_later_head_transpose',
         'ORIENTATION', 'directed shift label')
    need(type(shift['center']) is list and len(shift['center']) in (1, 2, 8),
         'SHAPE', 'fixed matrix size')
    size = len(shift['center'])
    k, e, pol = (matrix(shift[key], size)
                 for key in ('center', 'error', 'midpoint_polarization'))
    direct = [[uninterval(v) for v in sequence(row, size)]
              for row in sequence(shift['direct'], size)]
    for i in range(size):
        for j in range(size):
            need(e[i][j] >= 0, 'BOUND', 'nonnegative shift radius')
            need(k[i][j] == pol[i][j], 'POLARIZATION', 'saved polarization')
            low, high = direct[i][j]
            need(max(low, sub(k[i][j], e[i][j])) <= min(high, add(k[i][j], e[i][j])),
                 'DIRECT', 'saved direct enclosure intersection')
    need(unscalar(shift['trace_center']) == trace(k)
         and unscalar(shift['trace_error']) == trace(e), 'TRACE', 'complete shift trace')
    g, h, gamma, rho = inherited_gram(gram, size)
    a, b = F(n - 1, n), F(n - 1, n * n)
    z, f = zero_matrix(size), zero_matrix(size)
    boxes = [[None for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            z[i][j] = sub(mul(a, g[i][j]), mul(b, add(k[i][j], k[j][i])))
            f[i][j] = add(mul(a, h[i][j]), mul(b, add(e[i][j], e[j][i])))
            boxes[i][j] = (sub(z[i][j], f[i][j]), add(z[i][j], f[i][j]))
    from_entries = (total(boxes[i][i][0] for i in range(size)),
                    total(boxes[i][i][1] for i in range(size)))
    gc_center = sub(mul(a, trace(g)), mul(mul(F(2), b), trace(k)))
    gc_radius = add(mul(a, trace(h)), mul(mul(F(2), b), trace(e)))
    from_gc = (sub(gc_center, gc_radius), add(gc_center, gc_radius))
    need(from_entries == from_gc, 'TRACE', 'entry and g/c trace equality')
    low_factor, high_factor = F((n-1)**2, n*n), F(n*n-1, n*n)
    structural = (mul(mul(low_factor, sub(F(1), rho)), trace(g)),
                  mul(mul(high_factor, add(F(1), rho)), trace(g)))
    need(max(from_entries[0], structural[0]) <= min(from_entries[1], structural[1]),
         'STRUCTURAL', 'trace structural interval intersection')
    delta = max(total(row) for row in f)
    ell = div(mul(low_factor, sub(F(1), rho)), gamma)
    eps, state = usefulness(delta, ell)
    return encode({'n': n, 'a': a, 'b': b, 'center': z, 'error': f,
                   'entry_intervals': boxes, 'trace_interval': from_entries,
                   'trace_from_g_c': from_gc, 'structural_trace_interval': structural,
                   'delta': delta, 'ell': ell, 'eps': eps,
                   'enclosure_state': 'valid_conditional_enclosure',
                   'usefulness_state': state})
