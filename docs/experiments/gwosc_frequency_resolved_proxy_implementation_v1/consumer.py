"""RI93 certified Q256 frequency-band consumer; source-only until frozen admission.

No target inputs are read at import. Actual entry admits the unchanged RI90
body and RI73 row snapshot before decoding. It creates no files or subprocesses.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import math
import os
import re
import stat
import struct

BITS, PRECISION, Q = 262144, 256, 1 << 256
M, N, L, T, DIM, FS = 16384, 2769, 4096, 10961, 8, 4096
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
SCENARIOS = ('H1:left', 'H1:right', 'L1:left', 'L1:right')
RHO_LIMIT = F(1, 10**12)
DESIGN_PIN = {'bytes': 23384, 'sha256': '1176d5bb3ebab7fd7ba59cc33da494ffeab7a0f0981652734e65714ad873c811'}
RI90_PIN = {'bytes': 6994965, 'sha256': 'c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf'}
SNAPSHOT_PIN = {'bytes': 51891508, 'sha256': 'fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba'}
RI83_PIN = {'bytes': 38952074, 'sha256': 'e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f'}
RI73_PIN = {'bytes': 11180937, 'sha256': '3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe'}
RI90_ACCEPTANCE = {'bytes': 5773, 'sha256': 'ac1cc18491dfd9a9f1bd1bf546f0d0ecea3427eb287238f6c4783f6a3b34cd50'}
RI92_ACCEPTANCE = {'bytes': 1873, 'sha256': '2a08c8d69cb3910918152e3f17394142df096c5ca4ee7428e3e57018cd004114'}
METHOD = {'M': M, 'N': N, 'L': L, 'T': T, 'output': DIM, 'fs': FS,
          'precision_bits': PRECISION, 'integer_bit_limit': BITS, 'unitary_divisor': 128,
          'transform_sign': 1, 'band_count': 14, 'arithmetic': 'outward_Q256_integer_intervals',
          'normalization': 'exact_division_then_outward_Q256'}
GATES = ('admission:prior', 'admission:rows', 'transform:twiddles', 'transform:midpoint_parseval',
         'bands:responses', 'scenario:H1:left', 'scenario:H1:right', 'scenario:L1:left',
         'scenario:L1:right', 'completion:source_stable')
LIMITATIONS = [
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
FAKE_LIMITATIONS = ['Fabricated prior for RI93 qualification; no observed values or predecessor execution.']


class BandError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ': ' + message)


def need(ok, code, message):
    if not ok:
        raise BandError(code, message)


def integer(v):
    need(type(v) is int, 'EXACT', 'integer required')
    need(abs(v).bit_length() <= BITS, 'RESOURCE', 'integer bit ceiling')
    return v


def rat(v):
    need(type(v) is F, 'EXACT', 'Fraction required')
    integer(v.numerator); integer(v.denominator)
    return v


def scalar(v):
    v = rat(v)
    return [format(v.numerator, 'x'), format(v.denominator, 'x')]


def hexint(v):
    return format(integer(v), 'x')


def decode_int(v):
    need(type(v) is str, 'EXACT', 'hex integer string required')
    need(len(v) <= (BITS + 3) // 4 + 1, 'RESOURCE', 'hex integer length')
    need(re.fullmatch(r'(?:0|-?[1-9a-f][0-9a-f]*)', v) is not None, 'EXACT', 'canonical hex integer')
    return integer(int(v, 16))


def decode_scalar(v):
    need(type(v) is list and len(v) == 2, 'EXACT', 'rational pair required')
    a, b = map(decode_int, v)
    need(b > 0, 'EXACT', 'positive denominator')
    x = rat(F(a, b))
    need(scalar(x) == v, 'EXACT', 'reduced rational required')
    return x


def encoded(v):
    if type(v) is F:
        return scalar(v)
    if type(v) in (list, tuple):
        return [encoded(x) for x in v]
    if type(v) is dict:
        return {k: encoded(x) for k, x in v.items()}
    return v


def canonical_parts(v):
    for part in json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False).iterencode(v):
        yield part.encode('ascii')
    yield b'\n'


def canonical(v):
    return b''.join(canonical_parts(encoded(v)))


def identity(body):
    need(type(body) is bytes, 'INPUT', 'immutable bytes required')
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def canonical_pin(v):
    h, n = hashlib.sha256(), 0
    for piece in canonical_parts(v):
        h.update(piece); n += len(piece)
    return {'bytes': n, 'sha256': h.hexdigest()}


def obj(v, keys, code='SCHEMA'):
    need(type(v) is dict and set(v) == set(keys), code, 'closed keys: ' + ','.join(keys))
    return v


def seq(v, length, code='SCHEMA'):
    need(type(v) in (list, tuple) and len(v) == length, code, 'fixed sequence length')
    return v


def _pairs(rows):
    out = {}
    for k, v in rows:
        need(k not in out, 'SCHEMA', 'duplicate JSON key')
        out[k] = v
    return out


def parse_json(body):
    need(type(body) is bytes, 'INPUT', 'immutable JSON bytes')
    def bad(text):
        raise BandError('EXACT', 'nonfinite JSON constant ' + text)
    try:
        return json.loads(body.decode('ascii'), object_pairs_hook=_pairs, parse_constant=bad)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise BandError('SCHEMA', 'canonical ASCII JSON required') from exc


def pin(v):
    obj(v, ('bytes', 'sha256'), 'PROVENANCE')
    need(type(v['bytes']) is int and 0 < v['bytes'] <= 1 << 40, 'PROVENANCE', 'positive bounded byte count')
    need(type(v['sha256']) is str and re.fullmatch('[0-9a-f]{64}', v['sha256']) is not None,
         'PROVENANCE', 'SHA256 required')
    return v


def addf(a, b):
    return rat(rat(a) + rat(b))


def mulf(a, b):
    return rat(rat(a) * rat(b))


def sumf(values):
    out = F(0)
    for v in values:
        out = addf(out, v)
    return out


def qinterval(v):
    rat(v)
    a = integer(v.numerator * Q)
    return (a // v.denominator, -((-a) // v.denominator))


def interval(v):
    seq(v, 2, 'INTERVAL')
    a, b = map(integer, v)
    need(a <= b, 'INTERVAL', 'ordered grid endpoints')
    return a, b


def iadd(a, b):
    a, b = interval(a), interval(b)
    return integer(a[0] + b[0]), integer(a[1] + b[1])


def isub(a, b):
    a, b = interval(a), interval(b)
    return integer(a[0] - b[1]), integer(a[1] - b[0])


def imul(a, b):
    a, b = interval(a), interval(b)
    vals = [integer(x * y) for x in a for y in b]
    return min(vals) // Q, -((-max(vals)) // Q)


def rectangle(v):
    seq(v, 4, 'INTERVAL')
    return (*interval(v[:2]), *interval(v[2:]))


def cadd(a, b):
    return (*iadd(a[:2], b[:2]), *iadd(a[2:], b[2:]))


def csub(a, b):
    return (*isub(a[:2], b[:2]), *isub(a[2:], b[2:]))


def cmul(a, b):
    a, b = rectangle(a), rectangle(b)
    ac, bd = imul(a[:2], b[:2]), imul(a[2:], b[2:])
    ad, bc = imul(a[:2], b[2:]), imul(a[2:], b[:2])
    return (*isub(ac, bd), *iadd(ad, bc))


def sqrt_grid(q):
    rat(q)
    need(q >= 0, 'INTERVAL', 'nonnegative square-root argument')
    scaled = integer(q.numerator * (Q * Q))
    a = integer(math.isqrt(scaled // q.denominator))
    exact = integer(integer(a * a) * q.denominator) == scaled
    b = a if exact else integer(a + 1)
    need(F(a * a, Q * Q) <= q <= F(b * b, Q * Q), 'INTERVAL', 'sqrt isolation')
    return a, b


def transform_size(n):
    need(type(n) is int and n in (4, 16, M), 'DOMAIN', 'fixed transform sizes')
    return n


@lru_cache(maxsize=3)
def twiddles(size):
    size = transform_size(size)
    stages = []
    cosine = (0, 0)
    n = 2
    while n <= size:
        if n == 2:
            base = (-Q, -Q, 0, 0)
        elif n == 4:
            base = (0, 0, Q, Q)
        else:
            clo = sqrt_grid(F(Q + cosine[0], 2 * Q))[0]
            chi = sqrt_grid(F(Q + cosine[1], 2 * Q))[1]
            slo = sqrt_grid(F(Q - cosine[1], 2 * Q))[0]
            shi = sqrt_grid(F(Q - cosine[0], 2 * Q))[1]
            base = (max(0, clo), min(Q, chi), max(0, slo), min(Q, shi))
            rectangle(base)
            cosine = base[:2]
        powers, current = [], (Q, Q, 0, 0)
        for j in range(n // 2):
            powers.append(current)
            if j + 1 < n // 2:
                current = cmul(current, base)
        stages.append((n, base, tuple(powers)))
        n *= 2
    return tuple(stages)


def twiddle_record(size):
    return {'size': transform_size(size), 'precision_bits': PRECISION,
            'stages': [{'length': n, 'base': list(map(hexint, base)),
                        'powers_identity': canonical_pin([list(map(hexint, p)) for p in powers])}
                       for n, base, powers in twiddles(size)]}


def transform(midpoints, size):
    size = transform_size(size)
    seq(midpoints, size, 'DOMAIN')
    values = [(*qinterval(rat(x)), 0, 0) for x in midpoints]
    j = 0
    for i in range(1, size):
        bit = size >> 1
        while j & bit:
            j ^= bit; bit >>= 1
        j ^= bit
        if i < j:
            values[i], values[j] = values[j], values[i]
    for n, _, powers in twiddles(size):
        half = n // 2
        for start in range(0, size, n):
            for j, power in enumerate(powers):
                u = values[start + j]
                t = cmul(power, values[start + j + half])
                values[start + j] = cadd(u, t)
                values[start + j + half] = csub(u, t)
    divisor = math.isqrt(size)
    need(divisor * divisor == size, 'DOMAIN', 'exact unitary divisor')
    return tuple((a // divisor, -((-b) // divisor), c // divisor, -((-d) // divisor))
                 for a, b, c, d in values)


def row_certificate(row, midpoints, radii, *, size=M):
    size = transform_size(size)
    need(size in (4, M), 'DOMAIN', 'fixed row certificate sizes')
    length = T if size == M else 3
    need(type(row) is int and row >= 0, 'ROW', 'integer row id')
    seq(midpoints, length, 'ROW'); seq(radii, length, 'ROW')
    midpoints, radii = tuple(map(rat, midpoints)), tuple(map(rat, radii))
    need(all(x >= 0 for x in radii), 'INTERVAL', 'nonnegative radii')
    radius_sum, center_sum = sumf(radii), sumf(midpoints)
    need(-radius_sum <= center_sum <= radius_sum, 'DC', 'constant-annihilation box excludes zero')
    divisor = math.isqrt(size)
    alpha = rat(radius_sum / divisor)
    initial = [list(map(hexint, qinterval(x))) for x in midpoints]
    modes = transform(midpoints + (F(0),) * (size - length), size)[:size // 2 + 1]
    for a, b in (modes[0][:2], modes[0][2:]):
        need(F(a, Q) - alpha <= 0 <= F(b, Q) + alpha, 'DC', 'true DC incompatible with enclosure')
    need(modes[-1][2] <= 0 <= modes[-1][3], 'DC', 'Nyquist imaginary enclosure excludes zero')
    recorded = [list(map(hexint, p)) for p in modes]
    return ({'row': row, 'alpha': scalar(alpha), 'initial_q256': initial,
             'input_identity': canonical_pin(initial), 'midpoint_modes': recorded,
             'mode_identity': canonical_pin(recorded)}, modes)


def band_partition(size):
    need(type(size) is int and size in (4, M), 'DOMAIN', 'fixed band domain')
    out, first, index = [], 1, 0
    while first < size // 2:
        out.append({'index': index, 'first': first, 'last_exclusive': 2 * first})
        first *= 2; index += 1
    out.append({'index': index, 'first': first, 'last_exclusive': first + 1})
    return out


def _accumulate(mode_rows, alphas, first, last, size):
    """Exact factorization of (10); no Fraction multiplication inside mode loops."""
    d = len(mode_rows)
    cnum = [[0] * d for _ in range(d)]
    hnum = [[0] * d for _ in range(d)]
    linear = [0] * d
    acount = 0
    for k in range(first, last):
        endpoint = k in (0, size // 2)
        weight = 1 if endpoint else 2
        parts = []
        for i in range(d):
            a, b, c, e = rectangle(mode_rows[i][k])
            need(not endpoint or c <= 0 <= e, 'DC', 'real endpoint imaginary mismatch')
            x, tx = integer(a + b), integer(b - a)
            y, ty = (0, 0) if endpoint else (integer(c + e), integer(e - c))
            parts.append((x, tx, y, ty))
            linear[i] = integer(linear[i] + weight * (abs(x) + tx + abs(y) + ty))
        acount += weight * (1 if endpoint else 2)
        for i in range(d):
            x, tx, y, ty = parts[i]
            for j in range(i, d):
                xx, txx, yy, tyy = parts[j]
                cnum[i][j] = integer(cnum[i][j] + weight * integer(integer(x * xx) + integer(y * yy)))
                terms = (integer(abs(x) * txx), integer(tx * abs(xx)), integer(tx * txx),
                         integer(abs(y) * tyy), integer(ty * abs(yy)), integer(ty * tyy))
                hnum[i][j] = integer(hnum[i][j] + weight * integer(sum(terms)))
    den = 2 * Q
    cmat = [[F(0)] * d for _ in range(d)]
    hmat = [[F(0)] * d for _ in range(d)]
    htau = [[F(0)] * d for _ in range(d)]
    for i in range(d):
        for j in range(i, d):
            c = rat(F(cnum[i][j], den * den))
            ht = rat(F(hnum[i][j], den * den))
            h = sumf((ht, mulf(alphas[j], rat(F(linear[i], den))),
                      mulf(alphas[i], rat(F(linear[j], den))),
                      mulf(mulf(alphas[i], alphas[j]), F(acount))))
            cmat[i][j] = cmat[j][i] = c
            hmat[i][j] = hmat[j][i] = h
            htau[i][j] = htau[j][i] = ht
    return cmat, hmat, htau


def _matrix_sum(matrices, dimension):
    return [[sumf(m[i][j] for m in matrices) for j in range(dimension)] for i in range(dimension)]


def band_matrices(mode_rows, alphas, *, size=M):
    need(type(size) is int and size in (4, M), 'DOMAIN', 'matrix size domain')
    dimension = len(mode_rows) if type(mode_rows) in (tuple, list) else 0
    need((size == 4 and dimension in (1, 2)) or (size == M and dimension == DIM), 'DOMAIN', 'matrix dimension domain')
    seq(alphas, dimension, 'ALPHA')
    alphas = tuple(map(rat, alphas))
    need(all(x >= 0 for x in alphas), 'ALPHA', 'nonnegative alpha')
    for row in mode_rows:
        seq(row, size // 2 + 1, 'TRANSFORM')
        for rect in row:
            rectangle(rect)
    bands, centers, errors = [], [], []
    for part in band_partition(size):
        c, h, ht = _accumulate(mode_rows, alphas, part['first'], part['last_exclusive'], size)
        bands.append({**part, 'C': encoded(c), 'H': encoded(h)})
        centers.append(c); errors.append(ht)
    dc, _, dc_error = _accumulate(mode_rows, (F(0),) * dimension, 0, 1, size)
    centers.append(dc); errors.append(dc_error)
    return {'bands': bands, 'midpoint_parseval': {'center': encoded(_matrix_sum(centers, dimension)),
                                                'error': encoded(_matrix_sum(errors, dimension))}}


def decode_matrix(value, dimension):
    seq(value, dimension)
    result = [[decode_scalar(v) for v in seq(row, dimension)] for row in value]
    need(all(result[i][j] == result[j][i] for i in range(dimension) for j in range(dimension)), 'BAND', 'symmetric matrix')
    return result


def positive_gram(g):
    d = len(g); work = [row[:] for row in g]
    for k in range(d):
        pivot = work[k][k]
        need(pivot > 0, 'GLOBAL', 'positive Gram pivots required')
        for i in range(k + 1, d):
            for j in range(i, d):
                entry = addf(work[i][j], -rat(mulf(work[i][k], work[j][k]) / pivot))
                work[i][j] = work[j][i] = entry


def decode_psd(record, size):
    obj(record, ('dtype', 'shape', 'values_hex', 'sha256'), 'PSD')
    need(record['dtype'] == '<f8' and type(record['shape']) is list and
         all(type(x) is int for x in record['shape']) and record['shape'] == [size // 2 + 1], 'PSD', 'PSD dtype/shape')
    seq(record['values_hex'], size // 2 + 1, 'PSD')
    values, digest = [], hashlib.sha256()
    for text in record['values_hex']:
        need(type(text) is str and len(text) <= 32, 'PSD', 'float hex string')
        try:
            x = float.fromhex(text)
        except (ValueError, OverflowError) as exc:
            raise BandError('PSD', 'invalid binary64') from exc
        need(math.isfinite(x) and x >= 0 and x.hex() == text, 'PSD', 'canonical finite nonnegative binary64')
        digest.update(struct.pack('<d', x)); values.append(rat(F.from_float(x)))
    need(digest.hexdigest() == record['sha256'], 'PSD', 'PSD raw byte identity')
    return tuple(values)


def scenario_bounds(psd_record, G, rho, bands, *, size=M, fs=FS):
    need(type(size) is int and type(fs) is int and ((size == 4 and fs == 4) or (size == M and fs == FS)),
         'DOMAIN', 'fixed scenario domain')
    dimension = len(G)
    need((size == 4 and dimension in (1, 2)) or (size == M and dimension == DIM), 'DOMAIN', 'scenario dimension')
    g = [[rat(x) for x in seq(row, dimension)] for row in seq(G, dimension)]
    need(all(g[i][j] == g[j][i] for i in range(dimension) for j in range(dimension)), 'GLOBAL', 'symmetric Gram')
    positive_gram(g); rho = rat(rho)
    need(F(0) <= rho <= RHO_LIMIT, 'GLOBAL', 'unchanged rho gate')
    values = decode_psd(psd_record, size)
    eigen = [mulf(F(fs if k in (0, size // 2) else fs, 1 if k in (0, size // 2) else 2), p)
             for k, p in enumerate(values)]
    parts = band_partition(size); seq(bands, len(parts), 'BAND')
    cm = [[F(0)] * dimension for _ in range(dimension)]
    cp = [[F(0)] * dimension for _ in range(dimension)]
    hm = [[F(0)] * dimension for _ in range(dimension)]
    hp = [[F(0)] * dimension for _ in range(dimension)]
    extrema = []
    for b, part in zip(bands, parts, strict=True):
        obj(b, ('index', 'first', 'last_exclusive', 'C', 'H'), 'BAND')
        need({k: b[k] for k in part} == part and all(type(b[k]) is int for k in part), 'BAND', 'fixed band partition')
        c, h = decode_matrix(b['C'], dimension), decode_matrix(b['H'], dimension)
        need(all(x >= 0 for row in h for x in row), 'BAND', 'nonnegative error matrix')
        indices = range(part['first'], part['last_exclusive'])
        lo, hi = min(eigen[k] for k in indices), max(eigen[k] for k in indices)
        extrema.append({'index': part['index'], 'ell': scalar(lo), 'u': scalar(hi),
                        'minimum_indices': [k for k in indices if eigen[k] == lo],
                        'maximum_indices': [k for k in indices if eigen[k] == hi]})
        for i in range(dimension):
            for j in range(dimension):
                cm[i][j] = addf(cm[i][j], mulf(lo, c[i][j])); cp[i][j] = addf(cp[i][j], mulf(hi, c[i][j]))
                hm[i][j] = addf(hm[i][j], mulf(lo, h[i][j])); hp[i][j] = addf(hp[i][j], mulf(hi, h[i][j]))
    dm, dp = max(map(sumf, hm)), max(map(sumf, hp))
    lower = [[addf(cm[i][j], -dm if i == j else F(0)) for j in range(dimension)] for i in range(dimension)]
    upper = [[addf(cp[i][j], dp if i == j else F(0)) for j in range(dimension)] for i in range(dimension)]
    ell, u = min(eigen[1:]), max(eigen[1:])
    gl = [[mulf(mulf(ell, F(1) - rho), x) for x in row] for row in g]
    gu = [[mulf(mulf(u, F(1) + rho), x) for x in row] for row in g]
    diagonal = [[lower[i][i], upper[i][i]] for i in range(dimension)]
    trace = [sumf(lower[i][i] for i in range(dimension)), sumf(upper[i][i] for i in range(dimension))]
    inter = [[max(lower[i][i], gl[i][i]), min(upper[i][i], gu[i][i])] for i in range(dimension)]
    itrace = [max(trace[0], sumf(gl[i][i] for i in range(dimension))),
              min(trace[1], sumf(gu[i][i] for i in range(dimension)))]
    need(all(a <= b for a, b in [*inter, itrace]), 'ENVELOPE', 'disjoint valid scalar enclosures')
    return encoded({'band_extrema': extrema, 'C_minus': cm, 'H_minus': hm, 'C_plus': cp, 'H_plus': hp,
                    'delta_minus': dm, 'delta_plus': dp, 'lower': lower, 'upper': upper,
                    'diagonal': diagonal, 'trace': trace, 'global_lower': gl, 'global_upper': gu,
                    'scalar_intersections': {'diagonal': inter, 'trace': itrace,
                         'diagonal_ratios': [rat(b / a) if a > 0 else None for a, b in inter],
                         'trace_ratio': rat(itrace[1] / itrace[0]) if itrace[0] > 0 else None}})


def validate_provenance(value, phase):
    need(phase in ('fabricated_qualification', 'fixed_saved_application'), 'PHASE', 'fixed phase')
    obj(value, ('sources', 'inputs', 'acceptance', 'runtime'), 'PROVENANCE')
    obj(value['sources'], ('design', 'consumer', 'validator', 'qualifier', 'implementation'), 'PROVENANCE')
    for v in value['sources'].values(): pin(v)
    need(value['sources']['design'] == DESIGN_PIN, 'SOURCE', 'accepted RI92 design')
    obj(value['inputs'], ('ri90', 'snapshot', 'ri83', 'ri73'), 'PROVENANCE')
    for v in value['inputs'].values(): pin(v)
    actual = {'ri90': RI90_PIN, 'snapshot': SNAPSHOT_PIN, 'ri83': RI83_PIN, 'ri73': RI73_PIN}
    if phase == 'fixed_saved_application':
        need(value['inputs'] == actual, 'INPUT', 'fixed actual input identities')
    else:
        need(all(value['inputs'][k] != p for k, p in actual.items()), 'PHASE', 'fabricated operands must not claim actual identities')
    obj(value['acceptance'], ('ri90', 'ri92', 'qualification'), 'PROVENANCE')
    need(value['acceptance']['ri90'] == RI90_ACCEPTANCE and value['acceptance']['ri92'] == RI92_ACCEPTANCE,
         'PROVENANCE', 'prior root acceptances')
    if phase == 'fabricated_qualification':
        need(value['acceptance']['qualification'] is None, 'PHASE', 'qualification not yet accepted')
    else:
        pin(value['acceptance']['qualification'])
    obj(value['runtime'], ('fingerprint', 'inventory', 'interpreter'), 'PROVENANCE')
    for v in value['runtime'].values(): pin(v)


def validate_prior(prior, phase):
    obj(prior, ('context', 'G', 'rho', 'scenarios', 'held_provenance', 'held_limitations'))
    context = 'accepted_ri90_saved_output' if phase == 'fixed_saved_application' else 'fabricated_prior_not_observed'
    need(prior['context'] == context, 'PHASE', 'prior context')
    g = decode_matrix(prior['G'], DIM); positive_gram(g)
    rho = decode_scalar(prior['rho']); need(F(0) <= rho <= RHO_LIMIT, 'GLOBAL', 'inherited rho gate')
    seq(prior['scenarios'], 4)
    for name, scenario in zip(SCENARIOS, prior['scenarios'], strict=True):
        obj(scenario, ('id', 'source_record'))
        need(scenario['id'] == name, 'PSD', 'fixed scenario order')
        decode_psd(scenario['source_record'], M)
    if phase == 'fabricated_qualification':
        need(prior['held_provenance'] == {'context': 'fabricated_not_observed'} and prior['held_limitations'] == FAKE_LIMITATIONS,
             'PHASE', 'fabricated prior labels')
    else:
        need(type(prior['held_provenance']) is dict and type(prior['held_limitations']) is list and prior['held_limitations'],
             'PROVENANCE', 'retained actual prior metadata')
    return g, rho


def require_exhausted(iterator):
    exhausted = object()
    need(next(iterator, exhausted) is exhausted, 'ROW', 'extra source row')


def build_result(source_rows, prior, provenance, *, phase='fabricated_qualification'):
    validate_provenance(provenance, phase)
    g, rho = validate_prior(prior, phase)
    prior_identity, provenance_identity = canonical_pin(prior), canonical_pin(provenance)
    records, modes, alphas = [], [], []
    iterator = iter(source_rows)
    for expected in ROWS:
        try: row = next(iterator)
        except StopIteration as exc: raise BandError('ROW', 'missing source row') from exc
        obj(row, ('row', 'midpoints', 'radii'), 'ROW')
        need(type(row['row']) is int and row['row'] == expected, 'ROW', 'fixed row order')
        record, values = row_certificate(expected, row['midpoints'], row['radii'])
        records.append(record); modes.append(values); alphas.append(decode_scalar(record['alpha']))
        del row
    require_exhausted(iterator)
    response = band_matrices(modes, alphas)
    center = decode_matrix(response['midpoint_parseval']['center'], DIM)
    error = decode_matrix(response['midpoint_parseval']['error'], DIM)
    need(all(abs(g[i][j] - center[i][j]) <= error[i][j] for i in range(DIM) for j in range(DIM)),
         'PARSEVAL', 'midpoint transform does not enclose retained G')
    response['midpoint_parseval']['contains_G'] = True
    scenarios = [{'id': s['id'], 'source_record': s['source_record'],
                  **scenario_bounds(s['source_record'], g, rho, response['bands'])} for s in prior['scenarios']]
    need(canonical_pin(prior) == prior_identity and canonical_pin(provenance) == provenance_identity,
         'SOURCE', 'admitted prior/provenance changed during calculation')
    return {'schema': 'ri93-frequency-band-proxy-v1', 'phase': phase, 'status': 'all_gates_passed',
            'model': 'postulated_finite_circulant_from_empirical_psd', 'method': dict(METHOD), 'provenance': provenance,
            'prior': prior, 'rows': list(ROWS), 'row_proofs': records, 'twiddles': twiddle_record(M),
            'bands': response['bands'], 'midpoint_parseval': response['midpoint_parseval'], 'scenarios': scenarios,
            'gates': {'inventory': list(GATES), 'counts': {'total': 10, 'passed': 10, 'failed': 0},
                      'results': [{'id': name, 'passed': True} for name in GATES]}, 'limitations': list(LIMITATIONS)}


def file_identity(path):
    path = Path(path)
    need(path.is_absolute() and path == path.resolve(), 'INPUT', 'absolute unsubstituted input path')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'INPUT', 'regular nonsymlink input')
    h, n = hashlib.sha256(), 0
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        need((opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), 'INPUT', 'file changed at open')
        while chunk := stream.read(1024 * 1024): h.update(chunk); n += len(chunk)
        after = os.fstat(stream.fileno())
    final = path.lstat()
    key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    need(key(before) == key(after) == key(final) and n == before.st_size, 'INPUT', 'input changed during hashing')
    return {'bytes': n, 'sha256': h.hexdigest()}


class _RowReader:
    def __init__(self, stream):
        self.stream, self.buffer, self.position = stream, b'', 0
        self.digest, self.count = hashlib.sha256(), 0
    def refill(self):
        self.buffer, self.position = self.stream.read(65536), 0
        self.digest.update(self.buffer); self.count += len(self.buffer)
        need(self.count <= 64 * 1024 * 1024, 'RESOURCE', 'streamed snapshot byte ceiling')
    def take(self, n):
        out = bytearray()
        while len(out) < n:
            if self.position == len(self.buffer):
                self.refill()
                need(bool(self.buffer), 'INPUT', 'truncated snapshot')
            count = min(n - len(out), len(self.buffer) - self.position)
            out += self.buffer[self.position:self.position + count]; self.position += count
        return bytes(out)
    def row(self):
        need(self.take(1) == b'{', 'SCHEMA', 'snapshot row object')
        chunks, length, depth, string, escape = [b'{'], 1, 1, False, False
        while depth:
            if self.position == len(self.buffer):
                self.refill()
                need(bool(self.buffer), 'INPUT', 'truncated snapshot row')
            start = self.position
            while self.position < len(self.buffer):
                value = self.buffer[self.position]; self.position += 1
                if string:
                    if escape: escape = False
                    elif value == 92: escape = True
                    elif value == 34: string = False
                elif value == 34: string = True
                elif value == 123: depth += 1
                elif value == 125:
                    depth -= 1
                    if not depth: break
            chunk = self.buffer[start:self.position]; chunks.append(chunk); length += len(chunk)
            need(length <= 8 * 1024 * 1024, 'RESOURCE', 'snapshot row byte ceiling')
        return b''.join(chunks)
    def eof(self):
        if self.position != len(self.buffer):
            return False
        self.refill()
        return self.buffer == b''


def source_rows(path, expected_pin):
    """Full fixed capture grammar, one decoded row at a time; no whole JSON tree."""
    pin(expected_pin)
    need(expected_pin['bytes'] <= 64 * 1024 * 1024, 'RESOURCE', 'snapshot byte ceiling')
    need(file_identity(path) == expected_pin, 'INPUT', 'snapshot identity before decoding')
    compact = lambda v: json.dumps(v, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')
    header = b'{"dimensions":' + compact({'N': N, 'L': L, 'T': T}) + b',"row_order":' + compact(list(ROWS)) + b',"rows":['
    footer = b'],"schema":"ri73-reconstructed-intervals-v1"}'
    before = Path(path).lstat()
    key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    with Path(path).open('rb') as stream:
        need(key(os.fstat(stream.fileno())) == key(before), 'INPUT', 'snapshot parse descriptor changed')
        reader = _RowReader(stream)
        need(reader.take(len(header)) == header, 'SCHEMA', 'fixed snapshot header')
        for position, expected in enumerate(ROWS):
            if position: need(reader.take(1) == b',', 'SCHEMA', 'snapshot row separator')
            body = reader.row(); row = parse_json(body)
            need(compact(row) == body, 'CANONICAL', 'canonical compact row')
            obj(row, ('long', 'row', 'short'), 'ROW')
            need(type(row['row']) is int and row['row'] == expected, 'ROW', 'snapshot row order')
            seq(row['short'], N, 'ROW'); seq(row['long'], T, 'ROW')
            short, long = [], []
            for target, values in ((short, row['short']), (long, row['long'])):
                for pair in values:
                    seq(pair, 2, 'INTERVAL'); lo, hi = map(decode_scalar, pair)
                    need(lo <= hi, 'INTERVAL', 'ordered coefficient interval')
                    target.append((lo, hi))
            del row, body, target, values, pair
            mids, radii = [], []
            for j, (lo, hi) in enumerate(long):
                if L <= j < L + N:
                    sl, sh = short[j - L]
                    lo, hi = addf(lo, -sh), addf(hi, -sl)
                mids.append(rat(addf(lo, hi) / 2)); radii.append(rat(addf(hi, -lo) / 2))
            del short, long
            yield {'row': expected, 'midpoints': tuple(mids), 'radii': tuple(radii)}
            del mids, radii
        need(reader.take(len(footer)) == footer and reader.eof(), 'SCHEMA', 'fixed snapshot footer and EOF')
        need({'bytes': reader.count, 'sha256': reader.digest.hexdigest()} == expected_pin,
             'INPUT', 'parsed snapshot stream identity')
        need(key(os.fstat(stream.fileno())) == key(before) == key(Path(path).lstat()),
             'INPUT', 'snapshot changed during parsing')
    need(file_identity(path) == expected_pin, 'INPUT', 'snapshot identity after decoding')


def extract_prior(ri90_body):
    need(identity(ri90_body) == RI90_PIN, 'INPUT', 'accepted RI90 body identity')
    value = parse_json(ri90_body)
    need(value['schema'] == 'ri86-colored-proxy-envelope-v1' and value['phase'] == 'fixed_saved_application'
         and value['status'] == 'all_gates_passed' and value['rows'] == list(ROWS)
         and value['scenario_order'] == list(SCENARIOS), 'INPUT', 'accepted RI90 context')
    return {'context': 'accepted_ri90_saved_output', 'G': value['certificate']['G'], 'rho': value['certificate']['rho'],
            'scenarios': [{'id': s['id'], 'source_record': s['source_record']} for s in value['scenarios']],
            'held_provenance': value['provenance'], 'held_limitations': value['limitations']}


def run_saved(snapshot_path, ri90_body, provenance):
    """Root-authorized caller only: both byte identities precede scientific parse."""
    need(identity(ri90_body) == RI90_PIN, 'INPUT', 'accepted RI90 body identity')
    need(file_identity(snapshot_path) == SNAPSHOT_PIN, 'INPUT', 'accepted RI73 capture identity')
    validate_provenance(provenance, 'fixed_saved_application')
    prior = extract_prior(ri90_body)
    result = build_result(source_rows(snapshot_path, SNAPSHOT_PIN), prior, provenance, phase='fixed_saved_application')
    need(identity(ri90_body) == RI90_PIN and file_identity(snapshot_path) == SNAPSHOT_PIN,
         'INPUT', 'saved operand identity after calculation')
    return result


if __name__ == '__main__':
    raise SystemExit('RI93 library requires a separately admitted captured-source caller; no direct launch.')
