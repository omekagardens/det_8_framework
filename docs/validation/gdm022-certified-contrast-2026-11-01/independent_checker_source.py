#!/usr/bin/env python3
"""UNEXECUTED source candidate: fixed GDM022 distinct exact reconstruction.
No evaluator import, subprocess, network, arguments, or file writes.
Execution requires a separate root-reviewed exact-source admission.
"""
import hashlib
import json
import os
import stat
import sys

ARTIFACT = '/Volumes/AI_DATA/development/det-review-evidence/followthrough-1851-20261101/calculation-GDM022/endpoints.json'
ARTIFACT_BYTES = 1106044
ARTIFACT_SHA = '683f76a23c9e8f32c89a8c76d503718b698ab5c8f0cec46d9a645ccaaeb48658'
METHOD_SHA = '0721ef3682bab838ed11c8c119fc4825261fab18c07b57111f26a08688d2c87c'
BITS = 200000
CHARGE_CAP = 10000000
Q = 1 << 128
charge = 200000
primitive_calls = 0
largest_bits = 0


class Reject(Exception):
    pass


def need(ok, label):
    if not ok:
        raise Reject(label)


def integer(a):
    global largest_bits
    need(type(a) is int, 'integer type')
    n = a.bit_length()
    need(n <= BITS, 'integer bit cap')
    largest_bits = max(largest_bits, n)
    return a


def begin(a, b):
    global charge, primitive_calls
    charge += 32
    primitive_calls += 1
    need(charge <= CHARGE_CAP, 'checker arithmetic charge cap')
    integer(a)
    integer(b)


def plus(a, b):
    begin(a, b)
    need(max(a.bit_length(), b.bit_length()) < BITS, 'sum pre-cap')
    return integer(a + b)


def minus(a, b):
    begin(a, b)
    need(max(a.bit_length(), b.bit_length()) < BITS, 'difference pre-cap')
    return integer(a - b)


def times(a, b):
    begin(a, b)
    need(a.bit_length() + b.bit_length() <= BITS, 'product pre-cap')
    return integer(a * b)


def compare(a, b):
    begin(a, b)
    return (a > b) - (a < b)


def divide(a, b):
    begin(a, b)
    need(b > 0, 'positive integer divisor')
    q, r = divmod(a, b)
    return integer(q), integer(r)


def quotient(a, b):
    q, r = divide(a, b)
    need(r == 0, 'prescribed exact division')
    return q


def power(a, n):
    need(type(n) is int and 0 <= n <= 800, 'bounded exponent')
    # Exponentiation by squaring, unlike the producer's power tables.
    value = 1
    while n:
        if n & 1:
            value = times(value, a)
        n //= 2
        if n:
            a = times(a, a)
    return value


def radd(a, b):
    if a[1] == b[1]:
        return plus(a[0], b[0]), a[1]
    return plus(times(a[0], b[1]), times(b[0], a[1])), times(a[1], b[1])


def rsub(a, b):
    if a[1] == b[1]:
        return minus(a[0], b[0]), a[1]
    return minus(times(a[0], b[1]), times(b[0], a[1])), times(a[1], b[1])


def rtimes(a, b):
    return times(a[0], b[0]), times(a[1], b[1])


def scale(a, n):
    return times(a[0], n), a[1]


def order(a, b):
    return compare(times(a[0], b[1]), times(b[0], a[1]))


def slack(a, b):
    # Exact numerator of b-a with the deliberately unreduced positive product denominator.
    s = minus(times(b[0], a[1]), times(a[0], b[1]))
    need(s >= 0, 'negative certified inequality')
    return s


def interval(a):
    need(a[0][1] > 0 and a[1][1] > 0 and order(a[0], a[1]) <= 0,
         'ordered positive-denominator interval')
    return a


def isum(a, b):
    return interval((radd(a[0], b[0]), radd(a[1], b[1])))


def iproduct(a, b):
    # Four-corner enclosure; strict comparisons retain the first representative on ties.
    corners = [rtimes(x, y) for x in a for y in b]
    lo = hi = corners[0]
    for c in corners[1:]:
        if order(c, lo) < 0:
            lo = c
        if order(c, hi) > 0:
            hi = c
    return interval((lo, hi))


def keys(obj, expected):
    need(type(obj) is dict and set(obj) == set(expected), 'exact object schema')


def hi(s):
    need(type(s) is str and 3 <= len(s) <= 50004, 'bounded hexadecimal token')
    body = s[1:] if s.startswith('-') else s
    need(body.startswith('0x') and len(body) > 2, 'hexadecimal prefix')
    need(len(body) - 2 <= BITS // 4, 'hexadecimal pre-allocation bit cap')
    need(all(c in '0123456789abcdef' for c in body[2:]), 'hexadecimal alphabet')
    a = integer(int(s, 16))
    need(hex(a) == s, 'canonical hexadecimal representation')
    return a


def rational(obj):
    keys(obj, ['n', 'd'])
    a = hi(obj['n']), hi(obj['d'])
    need(a[1] > 0, 'positive rational denominator')
    return a


def encoded_interval(obj):
    keys(obj, ['lo', 'hi'])
    return interval((rational(obj['lo']), rational(obj['hi'])))


def same_r(obj, expected):
    need(rational(obj) == expected, 'exact raw rational encoding mismatch')


def same_i(obj, expected):
    need(encoded_interval(obj) == expected, 'exact interval encoding mismatch')


def width(a):
    need(a[0][1] == Q and a[1][1] == Q, 'fixed dyadic grid')
    return minus(a[1][0], a[0][0])


def rounding(raw, record, endpoint, domain):
    interval(raw)
    keys(record, ['unclipped', 'lower_residual', 'upper_residual', 'domain_clip'])
    low, _ = divide(times(Q, raw[0][0]), raw[0][1])
    high, rem = divide(times(Q, raw[1][0]), raw[1][1])
    high = plus(high, 1) if rem else high
    uncut = ((low, Q), (high, Q))
    same_i(record['unclipped'], uncut)
    need(hi(record['lower_residual']) == slack(uncut[0], raw[0]), 'lower rounding residual')
    need(hi(record['upper_residual']) == slack(raw[1], uncut[1]), 'upper rounding residual')
    need(record['domain_clip'] == list(domain), 'fixed domain clipping')
    if domain[0] is not None:
        low = max(low, times(domain[0], Q))
    if domain[1] is not None:
        high = min(high, times(domain[1], Q))
    result = interval(((low, Q), (high, Q)))
    same_i(endpoint, result)
    return result


def homogeneous_exp(u, v, f):
    # Horner homogeneous numerator, not the author's sum of power-table terms.
    h, coefficient, v_power = 1, 1, 1
    for k in range(127, -1, -1):
        coefficient = times(coefficient, k + 1)
        v_power = times(v_power, v)
        h = plus(times(h, u), times(coefficient, v_power))
    return h, times(v_power, f[128])


def exponential(rec, u, v, f, normalization=False):
    common = ['argument', 'endpoint'] + (['k'] if normalization else [])
    keys(rec, common + (['exact_zero'] if u == 0 else ['polynomial', 'tail_upper', 'rounding']))
    same_r(rec['argument'], (u, v))
    need(0 <= u <= 2 * v, 'exponential domain')
    if u == 0:
        need(rec['exact_zero'] is True, 'exact zero declaration')
        result = ((Q, Q), (Q, Q))
        same_i(rec['endpoint'], result)
        return result
    poly = homogeneous_exp(u, v, f)
    same_r(rec['polynomial'], poly)
    need(order(poly, (1, 1)) >= 0, 'positive exponential partial sum')
    tail = (1, 1 << 266)
    same_r(rec['tail_upper'], tail)
    enlarged = radd(poly, tail)
    raw = ((enlarged[1], enlarged[0]), (poly[1], poly[0]))
    result = rounding(raw, rec['rounding'], rec['endpoint'], (0, 1))
    need(width(result) < 3, 'exponential width')
    return result


def atan_interval(v, f):
    # Horner in v^2 for the common-denominator alternating polynomial.
    square = times(v, v)
    numerator = f[255]
    for j in range(1, 128):
        c = quotient(f[255], 2 * j + 1)
        numerator = times(numerator, square)
        numerator = minus(numerator, c) if j & 1 else plus(numerator, c)
    low = (numerator, times(power(v, 255), f[255]))
    return interval((low, radd(low, (1, 1 << 514))))


def trigonometric(theta, records, f):
    need(type(records) is list and len(records) == 2, 'two trigonometric records')
    need(theta[0][1] == theta[1][1], 'phase common denominator')
    need(order(theta[0], (0, 1)) >= 0 and order(theta[1], (4, 1)) <= 0, 'phase domain')
    u, v = plus(theta[0][0], theta[1][0]), times(2, theta[0][1])
    h = (minus(theta[1][0], theta[0][0]), v)
    # Two homogeneous Horner accumulators at common degree255.
    hc, hs, coefficient, v_power = 0, -1, 1, 1
    for k in range(254, -1, -1):
        coefficient = times(coefficient, k + 1)
        v_power = times(v_power, v)
        term = times(coefficient, v_power)
        hc, hs = times(hc, u), times(hs, u)
        if k & 1:
            hs = plus(hs, term) if k % 4 == 1 else minus(hs, term)
        else:
            hc = plus(hc, term) if k % 4 == 0 else minus(hc, term)
    den = times(v_power, f[255])
    error = radd((1, 1 << 380), h)
    results = []
    for label, num, rec in zip(('cos', 'sin'), (hc, hs), records):
        keys(rec, ['function', 'midpoint', 'halfwidth', 'endpoint', 'rounding'])
        need(rec['function'] == label, 'trigonometric label/order')
        same_r(rec['midpoint'], (u, v))
        same_r(rec['halfwidth'], h)
        poly = num, den
        result = rounding((rsub(poly, error), radd(poly, error)), rec['rounding'], rec['endpoint'], (-1, 1))
        need(width(result) < 6, 'trigonometric width')
        results.append(result)
    return results


def check(a):
    keys(a, ['schema', 'status', 'method_sha256', 'normalization', 'pairs', 'pi', 'aggregates', 'norm', 'final', 'resources', 'limits'])
    need(a['schema'] == 'GDM022-fixed-endpoints-v1', 'artifact schema')
    need(a['status'] == 'conditional_arithmetic_pending_distinct_reconstruction', 'pending artifact status')
    need(a['method_sha256'] == METHOD_SHA, 'accepted arithmetic version')
    need(a['limits'] == 'No individual laws, P0/P1/P2/P3 clearance, physical tolerance or gravity/DET derivation.', 'claim boundary')
    f = [1]
    for k in range(1, 321):
        f.append(times(f[-1], k))
    # Independent exact sufficient inequalities for the declared Taylor remainders.
    need(compare(times(130, 1 << 395), times(128, f[129])) < 0, 'exponential tail bound')
    need(compare(1 << 892, f[256]) < 0, 'trigonometric Taylor tail bound')
    for v in (5, 239):
        need(compare(1 << 514, times(257, power(v, 257))) < 0, 'arctangent alternating tail bound')
    norm = a['normalization']
    need(type(norm) is list and len(norm) == 21, 'normalization count')
    z = ((0, Q), (0, Q))
    for k, rec in zip(range(140, 161), norm):
        need(rec['k'] == k, 'normalization label/order')
        ei = exponential(rec, (k - 150) ** 2, 50, f, True)
        z = isum(z, ei)
    need(order(z[0], (1, 1)) >= 0 and order(z[1], (21, 1)) <= 0, 'positive Z enclosure')
    need(width(z) <= 5376, 'Z width')
    pi_record = a['pi']
    keys(pi_record, ['atan_5', 'atan_239', 'atan_tail_upper', 'endpoint', 'rounding'])
    at5, at239 = atan_interval(5, f), atan_interval(239, f)
    same_i(pi_record['atan_5'], at5)
    same_i(pi_record['atan_239'], at239)
    same_r(pi_record['atan_tail_upper'], (1, 1 << 514))
    raw_pi = (rsub(scale(at5[0], 16), scale(at239[1], 4)), rsub(scale(at5[1], 16), scale(at239[0], 4)))
    pi = rounding(raw_pi, pi_record['rounding'], pi_record['endpoint'], (2, 4))
    need(width(pi) < 3, 'pi width')
    pairs = a['pairs']
    need(type(pairs) is list and len(pairs) == 19, 'pair count')
    ac = ass = ((0, 1), (0, 1))
    for n, rec in zip(range(140, 159), pairs):
        keys(rec, ['n', 'b', 'r', 'theta', 'exponential', 'trig'])
        need(rec['n'] == n, 'pair label/order')
        # Original GDM020 positive radical cancellation, squared without radicals.
        radical = 4 * n * (n + 1) * (n + 2)
        lhs = times(times(f[2 * n + 4], f[2 * n + 4]), n * (n + 1))
        rhs = times(times(times(radical, radical), (2 * n + 1) * (2 * n + 3)), times(f[2 * n - 1], f[2 * n + 3]))
        need(compare(lhs, rhs) == 0, 'original positive matrix-factor cancellation')
        # Raw expression for witness identity, independently checked against factorized form.
        b = (times(power(n, n + 5), power(n + 2, n + 3)), times(4 * 150 ** 4, power(n + 1, 2 * n + 4)))
        factorized_b = (times(n * n, power((n + 1) ** 2 - 1, n + 3)), times(4 * 150 ** 4, power(n + 1, 2 * n + 4)))
        need(order(b, factorized_b) == 0, 'equivalent matrix coefficient forms')
        r = (150 ** 3 * (n + 1), 2 * n * n * (n + 2) ** 2)
        same_r(rec['b'], b)
        same_r(rec['r'], r)
        need(order((0, 1), b) < 0 and order(b, (1, 1)) < 0, 'b domain')
        need(order((0, 1), r) < 0 and order(r, (1, 1)) < 0, 'r domain')
        # Independently verify the dimensionless Coulomb n-to-n+2 gap.
        gap = rtimes((150 ** 3, 8), rsub((1, n * n), (1, (n + 2) ** 2)))
        need(order(r, gap) == 0, 'original phase-gap scaling')
        theta_den = times(Q, r[1])
        theta = ((times(pi[0][0], r[0]), theta_den), (times(pi[1][0], r[0]), theta_den))
        same_i(rec['theta'], theta)
        ci, si = trigonometric(theta, rec['trig'], f)
        ui = exponential(rec['exponential'], (n - 150) ** 2 + (n - 148) ** 2, 100, f)
        difference = ((minus(Q, ci[1][0]), Q), (minus(Q, ci[0][0]), Q))
        ac = isum(ac, iproduct((b, b), iproduct(ui, difference)))
        ass = isum(ass, iproduct((b, b), iproduct(ui, si)))
    keys(a['aggregates'], ['Z', 'A_c', 'A_s'])
    for key, value in (('Z', z), ('A_c', ac), ('A_s', ass)):
        same_i(a['aggregates'][key], value)
    need(order(ac[0], (0, 1)) >= 0 and order(ac[1], (38, 1)) <= 0, 'cosine aggregate domain')
    need(order(ass[0], (-19, 1)) >= 0 and order(ass[1], (19, 1)) <= 0, 'sine aggregate domain')
    keys(a['final'], ['d_c', 'd_s', 'D'])
    inverse = ((z[1][1], z[1][0]), (z[0][1], z[0][0]))
    results = {}
    for label, agg, domain in (('d_c', ac, (0, 152)), ('d_s', ass, (-76, 76))):
        rec = a['final'][label]
        raw = iproduct((scale(agg[0], 4), scale(agg[1], 4)), inverse)
        results[label] = rounding(raw, rec['rounding'], rec['endpoint'], domain)
    dc, ds = results['d_c'], results['d_s']
    wc, ws = width(dc), width(ds)
    need(wc < 1 << 20 and ws < 1 << 19, 'component analytic widths')
    tq = times(2, Q)
    xc = minus(plus(dc[0][0], dc[1][0]), tq)
    xs = minus(plus(ds[0][0], ds[1][0]), tq)
    y = (plus(times(xc, xc), times(xs, xs)), times(tq, tq))
    keys(a['norm'], ['radius', 'root'])
    root = a['norm']['root']
    keys(root, ['Y', 'endpoint', 'steps', 'lower_square_residual', 'upper_square_residual'])
    same_r(root['Y'], y)
    need(root['steps'] == 128, 'recorded bisection count')
    bracket = encoded_interval(root['endpoint'])
    need(width(bracket) <= 256 and bracket[0][0] >= 0 and bracket[1][0] <= times(256, Q), 'nonnegative narrow root bracket')
    # This is an independent certificate check, not reproduction of128 bisection steps.
    q2 = times(Q, Q)
    low_square = (times(bracket[0][0], bracket[0][0]), q2)
    high_square = (times(bracket[1][0], bracket[1][0]), q2)
    need(hi(root['lower_square_residual']) == slack(low_square, y), 'root lower square residual')
    need(hi(root['upper_square_residual']) == slack(y, high_square), 'root upper square residual')
    total_width = plus(wc, ws)
    same_r(a['norm']['radius'], (total_width, tq))
    raw_d = ((max(0, minus(times(2, bracket[0][0]), total_width)), tq), (plus(times(2, bracket[1][0]), total_width), tq))
    results['D'] = rounding(raw_d, a['final']['D']['rounding'], a['final']['D']['endpoint'], (0, None))
    for label, value in results.items():
        rec = a['final'][label]
        keys(rec, ['endpoint', 'width', 'resolution_residual', 'rounding'] + ([] if label == 'D' else ['contains_one_not_equality']))
        w = width(value)
        need(w < 1 << 22, 'uniform analytic width')
        same_r(rec['width'], (w, Q))
        resolution_slack = minus(Q, times(1000000, w))
        need(resolution_slack >= 0 and hi(rec['resolution_residual']) == resolution_slack, 'exact millionth resolution')
        if label != 'D':
            contains = value[0][0] <= Q <= value[1][0]
            need(type(rec['contains_one_not_equality']) is bool and rec['contains_one_not_equality'] == contains, 'containment classification')
    # Resource flags are provenance only; our guards and external observations are separate.
    keys(a['resources'], ['all_arithmetic_guards_passed', 'base_charge_per_call', 'charged_integer_operations', 'division_charge_per_call', 'fixed_bookkeeping_reserve', 'metered_calls', 'operation_cap', 'per_integer_bit_cap', 'wall_time_and_RSS'])
    return results


def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d


def small_decimal(s):
    need(len(s) <= 10, 'bounded JSON integer token')
    n = int(s)
    need(abs(n) <= 10000000, 'bounded metadata integer')
    return n


def forbidden_number(s):
    raise Reject('noninteger JSON number')


def bounded_tree(a):
    todo, nodes, text_bytes = [(a, 0)], 0, 0
    while todo:
        value, depth = todo.pop()
        nodes += 1
        need(nodes <= 20000 and depth <= 20, 'JSON structure bounds')
        if type(value) is dict:
            need(len(value) <= 32, 'object width')
            for k, v in value.items():
                need(type(k) is str and len(k) <= 80, 'JSON key bound')
                todo.append((v, depth + 1))
        elif type(value) is list:
            need(len(value) <= 40, 'array width')
            todo.extend((v, depth + 1) for v in value)
        elif type(value) is str:
            need(len(value) <= 50004, 'JSON string bound')
            text_bytes += len(value)
            need(text_bytes <= ARTIFACT_BYTES, 'JSON total text bound')
        else:
            need(value is None or type(value) in (bool, int), 'JSON primitive type')
    return nodes, text_bytes


def snapshot():
    fd = os.open(ARTIFACT, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        s = os.fstat(fd)
        need(stat.S_ISREG(s.st_mode) and s.st_size == ARTIFACT_BYTES, 'fixed regular artifact size')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            data = stream.read(ARTIFACT_BYTES + 1)
        need(len(data) == ARTIFACT_BYTES and hashlib.sha256(data).hexdigest() == ARTIFACT_SHA, 'artifact exact identity')
        return data
    finally:
        os.close(fd)


def main():
    need(len(sys.argv) == 1, 'no arguments')
    first = snapshot()
    a = json.loads(first.decode('ascii'), object_pairs_hook=unique, parse_int=small_decimal,
                   parse_float=forbidden_number, parse_constant=forbidden_number)
    nodes, text_bytes = bounded_tree(a)
    results = check(a)
    need(snapshot() == first, 'artifact changed during reconstruction')
    report = {
        'status': 'EXACT_FIXED_ARTIFACT_CHECKS_PASSED_PENDING_COORDINATOR_DISPOSITION',
        'artifact_sha256': ARTIFACT_SHA,
        'method_sha256': METHOD_SHA,
        'coverage': {'exponentials': 40, 'pairs': 19, 'trigonometric_functions': 38, 'root': 'direct nonnegative square-bracket certificate'},
        'endpoints': {label: {'lo': [hex(v[0][0]), hex(v[0][1])], 'hi': [hex(v[1][0]), hex(v[1][1])]} for label, v in results.items()},
        'checker_resources': {'charged_units': charge, 'unit_cap': CHARGE_CAP, 'primitive_calls': primitive_calls,
                              'largest_integer_bits': largest_bits, 'integer_bit_cap': BITS, 'json_nodes': nodes,
                              'json_text_bytes': text_bytes, 'wall_time_and_RSS': 'external measurement required'},
        'limits': 'Fixed conditional model only. No physical acceptance, individual laws, benchmark, M38 qualification, or programme gate release.'
    }
    payload = (json.dumps(report, sort_keys=True) + '\n').encode('ascii')
    need(len(payload) <= 8192, 'stdout cap')
    sys.stdout.buffer.write(payload)
    sys.stdout.buffer.flush()


if __name__ == '__main__':
    try:
        main()
    except Reject as exc:
        sys.stderr.write('GDM022 independent checker stopped: ' + str(exc)[:200] + '. No acceptance.\n')
        sys.exit(1)
    except Exception:
        sys.stderr.write('GDM022 independent checker failed. No acceptance; preserve external capture.\n')
        sys.exit(1)
