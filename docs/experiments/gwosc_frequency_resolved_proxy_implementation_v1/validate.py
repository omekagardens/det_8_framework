#!/usr/bin/env python3
"""Independent exact saved-certificate validation for the fixed RI92 design.

This module performs no computation on import and imports no producer.  Its
arithmetic verifies finite interval certificates; external source, input and
execution custody remains the separately admitted caller's responsibility.
"""

from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import struct


BITS = 262144
Q = 1 << 256
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
T = 10961
M = 16384
ORDER = ("H1:left", "H1:right", "L1:left", "L1:right")
METHOD = {"M": M, "N": 2769, "L": 4096, "T": T, "output": 8, "fs": 4096,
          "precision_bits": 256, "integer_bit_limit": BITS, "unitary_divisor": 128,
          "transform_sign": 1, "band_count": 14,
          "arithmetic": "outward_Q256_integer_intervals",
          "normalization": "exact_division_then_outward_Q256"}
DESIGN = {"bytes": 23384, "sha256": "1176d5bb3ebab7fd7ba59cc33da494ffeab7a0f0981652734e65714ad873c811"}
INPUTS = {
    "ri90": {"bytes": 6994965, "sha256": "c3a90d4d4516cce5309e47ec0b276455a515dcd3a67c749fa6c2500a2d9af3bf"},
    "snapshot": {"bytes": 51891508, "sha256": "fe24ce8b35d97a9073eff8c8002ce733e4f81be3e2d9167453a640f7f2c21aba"},
    "ri83": {"bytes": 38952074, "sha256": "e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f"},
    "ri73": {"bytes": 11180937, "sha256": "3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe"},
}
GATES = ["admission:prior", "admission:rows", "transform:twiddles",
         "transform:midpoint_parseval", "bands:responses", "scenario:H1:left",
         "scenario:H1:right", "scenario:L1:left", "scenario:L1:right",
         "completion:source_stable"]
ACCEPTANCE = {
    "ri90": {"bytes": 5773, "sha256": "ac1cc18491dfd9a9f1bd1bf546f0d0ecea3427eb287238f6c4783f6a3b34cd50"},
    "ri92": {"bytes": 1873, "sha256": "2a08c8d69cb3910918152e3f17394142df096c5ca4ee7428e3e57018cd004114"},
}
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


class ValidationError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, code, message):
    if not condition:
        raise ValidationError(code, message)


def keys(value, expected, code="SCHEMA"):
    require(type(value) is dict and all(type(k) is str for k in value)
            and set(value) == set(expected), code, "closed object fields differ")


def same(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return actual.keys() == expected.keys() and all(same(actual[k], v) for k, v in expected.items())
    if type(expected) in (list, tuple):
        return len(actual) == len(expected) and all(same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def equal(actual, expected, code, message):
    require(same(actual, expected), code, message)


def bounded_integer(value):
    require(type(value) is int, "EXACT", "integer required")
    require(abs(value).bit_length() <= BITS, "RESOURCE", "exact integer exceeds fixed bit cap")
    return value


def bounded(value):
    require(type(value) is Fraction, "EXACT", "Fraction required")
    bounded_integer(value.numerator)
    bounded_integer(value.denominator)
    return value


def add(a, b):
    return bounded(bounded(a) + bounded(b))


def mul(a, b):
    return bounded(bounded(a) * bounded(b))


def total(values):
    result = Fraction(0)
    for value in values:
        result = add(result, value)
    return result


def integer(text):
    require(type(text) is str, "EXACT", "hexadecimal integer text required")
    require(len(text) <= (BITS + 3) // 4 + 1, "RESOURCE", "hexadecimal integer text exceeds cap")
    require(re.fullmatch(r"(?:0|-?[1-9a-f][0-9a-f]*)", text) is not None,
            "EXACT", "noncanonical signed hexadecimal integer")
    return bounded_integer(int(text, 16))


def rational(value):
    require(type(value) is list and len(value) == 2, "EXACT", "rational pair required")
    numerator, denominator = (integer(x) for x in value)
    require(denominator > 0, "EXACT", "positive rational denominator required")
    result = bounded(Fraction(numerator, denominator))
    require(result.numerator == numerator and result.denominator == denominator,
            "EXACT", "rational pair is not reduced")
    return result


def encode(value):
    if type(value) is Fraction:
        value = bounded(value)
        return [format(value.numerator, "x"), format(value.denominator, "x")]
    if type(value) in (list, tuple):
        return [encode(x) for x in value]
    if type(value) is dict:
        return {k: encode(v) for k, v in value.items()}
    return value


def grid_pair(value):
    require(type(value) is list and len(value) == 2, "INTERVAL", "grid endpoint pair required")
    result = tuple(integer(x) for x in value)
    require(result[0] <= result[1], "INTERVAL", "reversed grid endpoints")
    return result


def pin(value, code="PROVENANCE"):
    keys(value, ("bytes", "sha256"), code)
    require(type(value["bytes"]) is int and value["bytes"] > 0
            and type(value["sha256"]) is str
            and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]) is not None,
            code, "invalid positive-length byte identity")


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def identity(payload):
    require(type(payload) is bytes, "INPUT", "immutable input bytes required")
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def decode_json(payload):
    require(type(payload) is bytes, "INPUT", "immutable JSON bytes required")
    def object_pairs(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "SCHEMA", "duplicate object key")
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValidationError("SCHEMA", "nonfinite JSON constant")
    try:
        return json.loads(payload, object_pairs_hook=object_pairs, parse_constant=invalid_constant)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValidationError("SCHEMA", "invalid JSON payload") from error


def canonical_identity(value):
    digest, length = hashlib.sha256(), 0
    encoder = json.JSONEncoder(sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)
    for text in encoder.iterencode(value):
        chunk = text.encode("ascii")
        digest.update(chunk)
        length += len(chunk)
    digest.update(b"\n")
    return {"bytes": length + 1, "sha256": digest.hexdigest()}


def interval_add(a, b):
    return (bounded_integer(a[0] + b[0]), bounded_integer(a[1] + b[1]))


def interval_sub(a, b):
    return (bounded_integer(a[0] - b[1]), bounded_integer(a[1] - b[0]))


def interval_product(a, b):
    products = [bounded_integer(x * y) for x in a for y in b]
    return (bounded_integer(min(products) // Q), bounded_integer(-((-max(products)) // Q)))


def complex_product(a, b):
    ac = interval_product(a[:2], b[:2])
    bd = interval_product(a[2:], b[2:])
    ad = interval_product(a[:2], b[2:])
    bc = interval_product(a[2:], b[:2])
    return interval_sub(ac, bd) + interval_add(ad, bc)


def complex_add(a, b):
    return interval_add(a[:2], b[:2]) + interval_add(a[2:], b[2:])


def complex_sub(a, b):
    return interval_sub(a[:2], b[:2]) + interval_sub(a[2:], b[2:])


def quantize(value):
    value = bounded(value)
    numerator = bounded_integer(value.numerator * Q)
    return (bounded_integer(numerator // value.denominator),
            bounded_integer(-((-numerator) // value.denominator)))


def sqrt_endpoint(value):
    value = bounded(value)
    require(value >= 0, "TWIDDLE", "negative square-root argument")
    numerator = bounded_integer(value.numerator * Q * Q)
    lower = bounded_integer(math.isqrt(numerator // value.denominator))
    lo = bounded(Fraction(lower, Q))
    upper = lower if mul(lo, lo) == value else bounded_integer(lower + 1)
    hi = bounded(Fraction(upper, Q))
    require(mul(lo, lo) <= value <= mul(hi, hi), "TWIDDLE", "square-root isolation failed")
    return lower, upper


def grid_sqrt(low, high):
    require(Fraction(0) <= low <= high, "TWIDDLE", "invalid square-root interval")
    return sqrt_endpoint(low)[0], sqrt_endpoint(high)[1]


def twiddle_evidence(size):
    require(type(size) is int and size in (4, 16, M), "DOMAIN", "unsupported transform size")
    stages, powers_by_size = [], {}
    previous_cos = None
    length = 2
    while length <= size:
        if length == 2:
            base = (-Q, -Q, 0, 0)
        elif length == 4:
            base = (0, 0, Q, Q)
        else:
            cosine = grid_sqrt(Fraction(Q + previous_cos[0], 2 * Q),
                               Fraction(Q + previous_cos[1], 2 * Q))
            sine = grid_sqrt(Fraction(Q - previous_cos[1], 2 * Q),
                             Fraction(Q - previous_cos[0], 2 * Q))
            base = (max(0, cosine[0]), min(Q, cosine[1]),
                    max(0, sine[0]), min(Q, sine[1]))
            require(base[0] <= base[1] and base[2] <= base[3],
                    "TWIDDLE", "first-quadrant intersection is empty")
        previous_cos = base[:2]
        powers, current = [], (Q, Q, 0, 0)
        for j in range(length // 2):
            powers.append(current)
            if j + 1 < length // 2:
                current = complex_product(current, base)
        encoded_powers = [[format(x, "x") for x in item] for item in powers]
        stages.append({"length": length, "base": [format(x, "x") for x in base],
                       "powers_identity": canonical_identity(encoded_powers)})
        powers_by_size[length] = tuple(powers)
        length *= 2
    return {"size": size, "precision_bits": 256, "stages": stages}, powers_by_size


def recursive_transform(initial, size, powers):
    """Recursive even/odd DIT: independent indexing from bit-reversed iteration."""
    require(len(initial) == size, "TRANSFORM", "transform input length differs")
    def visit(first, step, length):
        if length == 1:
            return [initial[first]]
        half = length // 2
        even = visit(first, step * 2, half)
        odd = visit(first + step, step * 2, half)
        low, high = [], []
        for k in range(half):
            term = complex_product(powers[length][k], odd[k])
            low.append(complex_add(even[k], term))
            high.append(complex_sub(even[k], term))
        return low + high
    divisor = {4: 2, 16: 4, M: 128}[size]
    output = visit(0, 1, size)
    return tuple((a // divisor, -((-b) // divisor),
                  c // divisor, -((-d) // divisor)) for a, b, c, d in output)


def rectangle(value):
    require(type(value) is list and len(value) == 4, "INTERVAL", "complex grid rectangle required")
    out = tuple(integer(x) for x in value)
    require(out[0] <= out[1] and out[2] <= out[3], "INTERVAL", "reversed complex rectangle")
    return out


def verify_row(record, source, expected_row, powers):
    keys(source, ("row", "midpoints", "radii"), "ROW")
    equal(source["row"], expected_row, "ROW", "source row order differs")
    midpoints, radii = source["midpoints"], source["radii"]
    require(type(midpoints) is tuple and type(radii) is tuple
            and len(midpoints) == T and len(radii) == T, "ROW", "exact source-row shapes differ")
    radius_sum = total(bounded(x) for x in radii)
    require(all(x >= 0 for x in radii), "INTERVAL", "negative source radius")
    midpoint_sum = total(bounded(x) for x in midpoints)
    require(abs(midpoint_sum) <= radius_sum, "DC", "source intervals exclude exact constant annihilation")
    alpha = bounded(radius_sum / 128)
    keys(record, ("row", "alpha", "initial_q256", "input_identity", "midpoint_modes", "mode_identity"), "ROW")
    equal(record["row"], expected_row, "ROW", "reported row order differs")
    equal(record["alpha"], encode(alpha), "ALPHA", "alpha differs from exact sum of source radii")
    initial = [quantize(x) for x in midpoints]
    encoded_initial = [[format(a, "x"), format(b, "x")] for a, b in initial]
    equal(record["initial_q256"], encoded_initial, "TRANSFORM", "initial midpoint enclosure differs")
    equal(record["input_identity"], canonical_identity(encoded_initial), "TRANSFORM", "initial midpoint identity differs")
    padded = [x + (0, 0) for x in initial] + [(0, 0, 0, 0)] * (M - T)
    del initial, encoded_initial
    replayed = recursive_transform(padded, M, powers)
    del padded
    require(type(record["midpoint_modes"]) is list and len(record["midpoint_modes"]) == M // 2 + 1,
            "TRANSFORM", "midpoint mode count differs")
    modes = []
    for k, item in enumerate(record["midpoint_modes"]):
        actual = rectangle(item)
        require(actual == replayed[k], "TRANSFORM", "recursive transform enclosure differs")
        modes.append(actual)
    equal(record["mode_identity"], canonical_identity(record["midpoint_modes"]),
          "TRANSFORM", "midpoint mode identity differs")
    require(Fraction(modes[0][0], Q) - alpha <= 0 <= Fraction(modes[0][1], Q) + alpha
            and Fraction(modes[0][2], Q) - alpha <= 0 <= Fraction(modes[0][3], Q) + alpha,
            "DC", "mode enclosure is incompatible with true zero DC")
    require(modes[-1][2] <= 0 <= modes[-1][3], "TRANSFORM", "Nyquist imaginary enclosure excludes zero")
    return tuple(modes), alpha


def matrix(value, dimension=8, code="SCHEMA"):
    require(type(value) is list and len(value) == dimension, code, "matrix row count differs")
    result = []
    for row in value:
        require(type(row) is list and len(row) == dimension, code, "matrix column count differs")
        result.append([rational(x) for x in row])
    return result


def check_gram(value):
    g = matrix(value, code="GLOBAL")
    require(all(g[i][j] == g[j][i] for i in range(8) for j in range(8)),
            "GLOBAL", "held midpoint Gram is not symmetric")
    # Independent Schur elimination, rather than trusting a stored LDL label.
    schur = [row[:] for row in g]
    for k in range(8):
        pivot = schur[k][k]
        require(pivot > 0, "GLOBAL", "held midpoint Gram is not positive definite")
        for i in range(k + 1, 8):
            for j in range(i, 8):
                correction = bounded(mul(schur[i][k], schur[k][j]) / pivot)
                schur[i][j] = add(schur[i][j], -correction)
                schur[j][i] = schur[i][j]
    return g


def decode_psd(record):
    keys(record, ("dtype", "shape", "values_hex", "sha256"), "PSD")
    equal(record["dtype"], "<f8", "PSD", "PSD dtype differs")
    equal(record["shape"], [8193], "PSD", "PSD shape differs")
    require(type(record["values_hex"]) is list and len(record["values_hex"]) == 8193,
            "PSD", "complete one-sided PSD required")
    digest, out = hashlib.sha256(), []
    for text in record["values_hex"]:
        require(type(text) is str and len(text) <= 32, "PSD", "invalid binary64 literal length")
        try:
            value = float.fromhex(text)
        except (OverflowError, ValueError) as error:
            raise ValidationError("PSD", "invalid finite binary64 literal") from error
        require(math.isfinite(value) and value.hex() == text and value >= 0,
                "PSD", "noncanonical, negative or nonfinite PSD")
        digest.update(struct.pack("<d", value))
        out.append(bounded(Fraction.from_float(value)))
    equal(record["sha256"], digest.hexdigest(), "PSD", "PSD binary64 byte identity differs")
    return tuple(out)


def band_partition():
    return [(index, 1 << index, 1 << (index + 1)) for index in range(13)] + [(13, 8192, 8193)]


def response_sum(mode_rows, alphas, first, last, *, midpoint_only=False):
    """Exact integer sufficient statistics; no per-mode Fraction matrices.

    A grid rectangle has center s/(2Q) and radius d/(2Q).  The two
    alpha-linear sums and alpha-quadratic count are kept separately from
    the transform-only integer errors, then combined exactly once.
    """
    centers = [[0] * 8 for _ in range(8)]
    errors = [[0] * 8 for _ in range(8)]
    linear, multiplicity = [0] * 8, 0
    for k in range(first, last):
        weight = 1 if k in (0, M // 2) else 2
        component_rows = []
        for modes in mode_rows:
            lo, hi, ilo, ihi = modes[k]
            components = (bounded_integer(lo + hi), bounded_integer(hi - lo),
                          bounded_integer(ilo + ihi), bounded_integer(ihi - ilo))
            # Both endpoint midpoint images are analytically real.  In the
            # Parseval check DC's real center/radius remain untouched; only
            # its identically zero imaginary part is removed.
            if k in (0, M // 2):
                require(ilo <= 0 <= ihi, "TRANSFORM", "real endpoint imaginary enclosure excludes zero")
                components = components[:2] + (0, 0)
            component_rows.append(components)
        axes = (0,) if k in (0, M // 2) else (0, 2)
        multiplicity = bounded_integer(multiplicity + weight * len(axes))
        for i in range(8):
            linear[i] = bounded_integer(linear[i] + weight * sum(
                abs(component_rows[i][axis]) + component_rows[i][axis + 1] for axis in axes))
            for j in range(i, 8):
                c, h = 0, 0
                for axis in axes:
                    si, di = component_rows[i][axis:axis + 2]
                    sj, dj = component_rows[j][axis:axis + 2]
                    c = bounded_integer(c + bounded_integer(si * sj))
                    h = bounded_integer(h + bounded_integer(abs(si) * dj)
                                        + bounded_integer(di * abs(sj)) + bounded_integer(di * dj))
                centers[i][j] = bounded_integer(centers[i][j] + bounded_integer(weight * c))
                errors[i][j] = bounded_integer(errors[i][j] + bounded_integer(weight * h))
    cmat, hmat = [[Fraction(0)] * 8 for _ in range(8)], [[Fraction(0)] * 8 for _ in range(8)]
    for i in range(8):
        for j in range(i, 8):
            c = bounded(Fraction(centers[i][j], 4 * Q * Q))
            h = bounded(Fraction(errors[i][j], 4 * Q * Q))
            if not midpoint_only:
                h = total((h, mul(alphas[j], Fraction(linear[i], 2 * Q)),
                           mul(alphas[i], Fraction(linear[j], 2 * Q)),
                           mul(mul(alphas[i], alphas[j]), Fraction(multiplicity))))
            cmat[i][j] = cmat[j][i] = c
            hmat[i][j] = hmat[j][i] = h
    return cmat, hmat


def verify_band(record, modes, alphas, index):
    require(type(index) is int and 0 <= index < 14, "BAND", "fixed band index required")
    expected_index, first, last = band_partition()[index]
    keys(record, ("index", "first", "last_exclusive", "C", "H"), "BAND")
    equal([record["index"], record["first"], record["last_exclusive"]],
          [expected_index, first, last], "BAND", "fixed band indices differ")
    c, h = response_sum(modes, alphas, first, last)
    equal(record["C"], encode(c), "BAND", "band center matrix differs")
    equal(record["H"], encode(h), "BAND", "band error matrix differs")
    return c, h


def verify_parseval(parseval, modes, alphas, g):
    keys(parseval, ("center", "error", "contains_G"), "PARSEVAL")
    pc, ph = response_sum(modes, alphas, 0, M // 2 + 1, midpoint_only=True)
    equal(parseval["center"], encode(pc), "PARSEVAL", "midpoint Parseval center differs")
    equal(parseval["error"], encode(ph), "PARSEVAL", "midpoint Parseval error differs")
    require(all(abs(g[i][j] - pc[i][j]) <= ph[i][j] for i in range(8) for j in range(8)),
            "PARSEVAL", "midpoint transform does not enclose held Gram")
    equal(parseval["contains_G"], True, "PARSEVAL", "invalid Parseval status")


def verify_bands(records, parseval, modes, alphas, g):
    require(type(records) is list and len(records) == 14, "BAND", "fourteen fixed bands required")
    computed = [verify_band(record, modes, alphas, index) for index, record in enumerate(records)]
    verify_parseval(parseval, modes, alphas, g)
    return computed


def scaled(matrix_value, coefficient):
    return [[mul(x, coefficient) for x in row] for row in matrix_value]


def weighted_matrices(bands, coefficients, slot):
    return [[total(mul(coefficient, band[slot][i][j]) for band, coefficient in zip(bands, coefficients))
             for j in range(8)] for i in range(8)]


def endpoints(lower, upper):
    diagonal = [[lower[i][i], upper[i][i]] for i in range(8)]
    trace = [total(lower[i][i] for i in range(8)), total(upper[i][i] for i in range(8))]
    return diagonal, trace


def verify_scenario(record, held, bands, g, rho):
    fields = ("id", "source_record", "band_extrema", "C_minus", "H_minus", "C_plus", "H_plus",
              "delta_minus", "delta_plus", "lower", "upper", "diagonal", "trace",
              "global_lower", "global_upper", "scalar_intersections")
    keys(record, fields, "ENVELOPE")
    equal(record["id"], held["id"], "PSD", "scenario order differs")
    equal(record["source_record"], held["source_record"], "PSD", "scenario source PSD differs from admitted prior")
    psd = decode_psd(held["source_record"])
    lambdas = tuple(mul(p, Fraction(4096 if k in (0, M // 2) else 2048)) for k, p in enumerate(psd))
    minima, maxima, extrema = [], [], []
    for index, first, last in band_partition():
        low, high = min(lambdas[first:last]), max(lambdas[first:last])
        minima.append(low)
        maxima.append(high)
        extrema.append({"index": index, "ell": encode(low), "u": encode(high),
                        "minimum_indices": [k for k in range(first, last) if lambdas[k] == low],
                        "maximum_indices": [k for k in range(first, last) if lambdas[k] == high]})
    equal(record["band_extrema"], extrema, "ENVELOPE", "band extrema or complete ties differ")
    cm = weighted_matrices(bands, minima, 0)
    hm = weighted_matrices(bands, minima, 1)
    cp = weighted_matrices(bands, maxima, 0)
    hp = weighted_matrices(bands, maxima, 1)
    dm, dp = max(total(row) for row in hm), max(total(row) for row in hp)
    lower = [[add(cm[i][j], -dm if i == j else Fraction(0)) for j in range(8)] for i in range(8)]
    upper = [[add(cp[i][j], dp if i == j else Fraction(0)) for j in range(8)] for i in range(8)]
    diagonal, trace = endpoints(lower, upper)
    gl = scaled(g, mul(min(lambdas[1:]), add(Fraction(1), -rho)))
    gu = scaled(g, mul(max(lambdas[1:]), add(Fraction(1), rho)))
    gd, gt = endpoints(gl, gu)
    intersection_diagonal = [[max(a[0], b[0]), min(a[1], b[1])] for a, b in zip(diagonal, gd)]
    intersection_trace = [max(trace[0], gt[0]), min(trace[1], gt[1])]
    require(all(low <= high for low, high in intersection_diagonal + [intersection_trace]),
            "ENVELOPE", "scalar intersection is empty")
    intersections = {"diagonal": intersection_diagonal, "trace": intersection_trace,
                     "diagonal_ratios": [bounded(high / low) if low > 0 else None
                                         for low, high in intersection_diagonal],
                     "trace_ratio": bounded(intersection_trace[1] / intersection_trace[0])
                     if intersection_trace[0] > 0 else None}
    expected = {"C_minus": cm, "H_minus": hm, "C_plus": cp, "H_plus": hp,
                "delta_minus": dm, "delta_plus": dp, "lower": lower, "upper": upper,
                "diagonal": diagonal, "trace": trace, "global_lower": gl, "global_upper": gu,
                "scalar_intersections": intersections}
    for key, value in expected.items():
        equal(record[key], encode(value), "GLOBAL" if key.startswith("global_") else "ENVELOPE",
              "independent scenario field differs: " + key)


def verify_provenance(value, expected, phase):
    keys(value, ("sources", "inputs", "acceptance", "runtime"), "PROVENANCE")
    keys(value["sources"], ("design", "consumer", "validator", "qualifier", "implementation"), "SOURCE")
    for record in value["sources"].values():
        pin(record, "SOURCE")
    equal(value["sources"]["design"], DESIGN, "SOURCE", "accepted RI92 design identity differs")
    keys(value["inputs"], INPUTS, "INPUT")
    for name, record in value["inputs"].items():
        pin(record, "INPUT")
        if phase == "fixed_saved_application":
            equal(record, INPUTS[name], "INPUT", "actual fixed input identity differs")
        else:
            require(not same(record, INPUTS[name]), "PHASE", "fabricated input claims an actual identity")
    keys(value["acceptance"], ("ri90", "ri92", "qualification"), "PROVENANCE")
    for name, expected_pin in ACCEPTANCE.items():
        equal(value["acceptance"][name], expected_pin, "PROVENANCE", "held root acceptance differs")
    for name, record in value["acceptance"].items():
        if name == "qualification" and phase == "fabricated_qualification":
            require(record is None, "PHASE", "fabricated qualification cannot already be accepted")
        else:
            pin(record, "PROVENANCE")
    keys(value["runtime"], ("fingerprint", "inventory", "interpreter"), "PROVENANCE")
    for record in value["runtime"].values():
        pin(record, "PROVENANCE")
    equal(value, expected, "PROVENANCE", "provenance differs from admitted caller metadata")


def verify_prior(prior, phase):
    keys(prior, ("context", "G", "rho", "scenarios", "held_provenance", "held_limitations"), "GLOBAL")
    expected_context = "accepted_ri90_saved_output" if phase == "fixed_saved_application" else "fabricated_prior_not_observed"
    equal(prior["context"], expected_context, "PHASE", "prior context differs from phase")
    g = check_gram(prior["G"])
    rho = rational(prior["rho"])
    require(Fraction(0) <= rho <= Fraction(1, 10**12), "GLOBAL", "held rho exceeds fixed accuracy domain")
    require(type(prior["scenarios"]) is list and len(prior["scenarios"]) == 4,
            "PSD", "four prior scenarios required")
    for record, name in zip(prior["scenarios"], ORDER):
        keys(record, ("id", "source_record"), "PSD")
        equal(record["id"], name, "PSD", "prior scenario order differs")
        # Full values and byte identity are checked again when deriving each scenario.
        keys(record["source_record"], ("dtype", "shape", "values_hex", "sha256"), "PSD")
    if phase == "fabricated_qualification":
        equal(prior["held_provenance"], {"context": "fabricated_not_observed"},
              "PHASE", "fabricated prior claims held observed provenance")
        equal(prior["held_limitations"],
              ["Fabricated prior for RI93 qualification; no observed values or predecessor execution."],
              "PHASE", "fabricated prior limitations differ")
    else:
        # Full prior identities and values are bound independently by validate_saved.
        require(type(prior["held_provenance"]) is dict and type(prior["held_limitations"]) is list
                and bool(prior["held_limitations"])
                and all(type(x) is str for x in prior["held_limitations"]),
                "GLOBAL", "retained prior provenance/limitations have invalid types")
    return g, rho


class SnapshotReader:
    """Structural one-row JSON reader with bounded buffers and exact syntax."""
    def __init__(self, stream, expected_identity):
        self.stream = stream
        self.buffer = b""
        self.offset = 0
        self.expected_identity = expected_identity
        self.digest = hashlib.sha256()
        self.length = 0

    def available(self):
        if self.offset == len(self.buffer):
            self.buffer = self.stream.read(65536)
            self.offset = 0
            self.digest.update(self.buffer)
            self.length += len(self.buffer)
            require(self.length <= 64 * 1024 * 1024, "RESOURCE", "consumed snapshot exceeds fixed byte ceiling")
        return bool(self.buffer)

    def take(self, count):
        parts = []
        while count:
            require(self.available(), "INPUT", "truncated snapshot")
            width = min(count, len(self.buffer) - self.offset)
            parts.append(self.buffer[self.offset:self.offset + width])
            self.offset += width
            count -= width
        return b"".join(parts)

    def expect(self, expected):
        equal(self.take(len(expected)), expected, "INPUT", "snapshot canonical structure differs")

    def row_body(self):
        self.expect(b"{")
        pieces, length, depth = [b"{"], 1, 1
        quoted, escaped = False, False
        while depth:
            require(self.available(), "INPUT", "truncated snapshot row")
            begin = self.offset
            while self.offset < len(self.buffer) and depth:
                byte = self.buffer[self.offset]
                self.offset += 1
                if quoted:
                    if escaped:
                        escaped = False
                    elif byte == 92:
                        escaped = True
                    elif byte == 34:
                        quoted = False
                elif byte == 34:
                    quoted = True
                elif byte == 123:
                    depth += 1
                elif byte == 125:
                    depth -= 1
            piece = self.buffer[begin:self.offset]
            length += len(piece)
            require(length <= 8 * 1024 * 1024, "RESOURCE", "snapshot row exceeds fixed byte ceiling")
            pieces.append(piece)
        return b"".join(pieces)

    def rows(self):
        self.expect(b'{"dimensions":{"L":4096,"N":2769,"T":10961},"row_order":[0,1,27,805,1384,2741,2767,2768],"rows":[')
        for index, expected_row in enumerate(ROWS):
            if index:
                self.expect(b",")
            body = self.row_body()
            row = decode_json(body)
            keys(row, ("long", "row", "short"), "ROW")
            equal(row["row"], expected_row, "ROW", "snapshot row order differs")
            compact = json.dumps(row, sort_keys=True, separators=(",", ":"),
                                 ensure_ascii=True, allow_nan=False).encode("ascii")
            require(body == compact, "CANONICAL", "snapshot row is not exact compact canonical JSON")
            del body, compact
            require(type(row["long"]) is list and len(row["long"]) == T
                    and type(row["short"]) is list and len(row["short"]) == 2769,
                    "ROW", "snapshot vector shapes differ")
            midpoints, radii = [], []
            for coordinate, long_interval in enumerate(row["long"]):
                require(type(long_interval) is list and len(long_interval) == 2,
                        "INTERVAL", "snapshot interval pair required")
                low, high = (rational(x) for x in long_interval)
                require(low <= high, "INTERVAL", "reversed long coefficient interval")
                if 4096 <= coordinate < 4096 + 2769:
                    short_interval = row["short"][coordinate - 4096]
                    require(type(short_interval) is list and len(short_interval) == 2,
                            "INTERVAL", "short coefficient interval pair required")
                    slow, shigh = (rational(x) for x in short_interval)
                    require(slow <= shigh, "INTERVAL", "reversed short coefficient interval")
                    low, high = add(low, -shigh), add(high, -slow)
                midpoints.append(bounded(add(low, high) / 2))
                radii.append(bounded(add(high, -low) / 2))
            del row
            output = {"row": expected_row, "midpoints": tuple(midpoints), "radii": tuple(radii)}
            del midpoints, radii
            yield output
            del output
        self.expect(b'],"schema":"ri73-reconstructed-intervals-v1"}')
        require(not self.available(), "INPUT", "trailing bytes after snapshot")
        equal({"bytes": self.length, "sha256": self.digest.hexdigest()}, self.expected_identity,
              "INPUT", "actually parsed snapshot bytes differ from admitted identity")


def stat_identity(info):
    return info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def regular_snapshot(path):
    require(isinstance(path, (str, Path)), "INPUT", "snapshot path required")
    path = Path(path)
    require(path.is_absolute() and path.resolve(strict=True) == path, "INPUT", "canonical snapshot path required")
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and not path.is_symlink(), "INPUT", "regular nonsymlink snapshot required")
    require(info.st_size <= 64 * 1024 * 1024, "RESOURCE", "snapshot exceeds fixed file byte ceiling")
    return path, stat_identity(info)


def hash_open_snapshot(stream):
    digest, length = hashlib.sha256(), 0
    stream.seek(0)
    while True:
        block = stream.read(1024 * 1024)
        if not block:
            break
        length += len(block)
        require(length <= 64 * 1024 * 1024, "RESOURCE", "snapshot exceeds fixed file byte ceiling")
        digest.update(block)
    return {"bytes": length, "sha256": digest.hexdigest()}


def extract_prior(body):
    # This function is a projection of one exactly pinned, previously accepted
    # whole report, not a new independent validation of all RI90 fields.
    equal(identity(body), INPUTS["ri90"], "INPUT", "held RI90 body differs")
    report = decode_json(body)
    require(type(report) is dict and report.get("schema") == "ri86-colored-proxy-envelope-v1"
            and report.get("phase") == "fixed_saved_application"
            and report.get("status") == "all_gates_passed", "GLOBAL", "held RI90 report status differs")
    equal(report["rows"], list(ROWS), "ROW", "held RI90 row order differs")
    equal(report["scenario_order"], list(ORDER), "PSD", "held RI90 scenario order differs")
    result = {"context": "accepted_ri90_saved_output", "G": report["certificate"]["G"],
              "rho": report["certificate"]["rho"],
              "scenarios": [{"id": x["id"], "source_record": x["source_record"]} for x in report["scenarios"]],
              "held_provenance": report["provenance"], "held_limitations": report["limitations"]}
    return result


def validate_result(report, source_rows, prior, expected_provenance, *, expected_phase):
    """Verify every result field using independently supplied exact operands.

    This pure entry does not establish custody of the supplied operands.
    validate_saved binds the fixed actual snapshot and held prior first;
    qualification supplies explicitly fabricated, independently made rows.
    """
    require(type(expected_phase) is str and expected_phase in
            ("fabricated_qualification", "fixed_saved_application"), "PHASE", "unsupported phase")
    keys(report, ("schema", "phase", "status", "model", "method", "provenance", "prior", "rows",
                  "row_proofs", "twiddles", "bands", "midpoint_parseval", "scenarios", "gates", "limitations"))
    equal(report["schema"], "ri93-frequency-band-proxy-v1", "SCHEMA", "result schema differs")
    equal(report["phase"], expected_phase, "PHASE", "result phase differs")
    equal(report["status"], "all_gates_passed", "SCHEMA", "result status differs")
    equal(report["model"], "postulated_finite_circulant_from_empirical_psd", "SCHEMA", "model label differs")
    equal(report["method"], METHOD, "DOMAIN", "fixed method differs")
    equal(report["rows"], list(ROWS), "ROW", "fixed row inventory differs")
    equal(report["limitations"], LIMITATIONS, "SCHEMA", "scientific limitations differ")
    expected_gates = {"inventory": GATES, "counts": {"total": 10, "passed": 10, "failed": 0},
                      "results": [{"id": name, "passed": True} for name in GATES]}
    equal(report["gates"], expected_gates, "SCHEMA", "complete gate inventory differs")
    verify_provenance(report["provenance"], expected_provenance, expected_phase)
    equal(report["prior"], prior, "GLOBAL", "reported prior differs from independently supplied prior")
    g, rho = verify_prior(prior, expected_phase)
    before_prior = canonical_identity(prior)
    before_provenance = canonical_identity(expected_provenance)
    require(type(report["row_proofs"]) is list and len(report["row_proofs"]) == 8,
            "ROW", "complete eight-row proof inventory required")
    twiddle_record, powers = twiddle_evidence(M)
    equal(report["twiddles"], twiddle_record, "TWIDDLE", "independent twiddle evidence differs")
    try:
        iterator = iter(source_rows)
    except TypeError as error:
        raise ValidationError("ROW", "independent source rows are not iterable") from error
    mode_rows, alphas = [], []
    for record, expected_row in zip(report["row_proofs"], ROWS):
        try:
            source = next(iterator)
        except StopIteration as error:
            raise ValidationError("ROW", "missing independent source row") from error
        modes, alpha = verify_row(record, source, expected_row, powers)
        mode_rows.append(modes)
        alphas.append(alpha)
        del source
    sentinel = object()
    require(next(iterator, sentinel) is sentinel, "ROW", "extra independent source row")
    del powers
    bands = verify_bands(report["bands"], report["midpoint_parseval"], mode_rows, alphas, g)
    del mode_rows
    require(type(report["scenarios"]) is list and len(report["scenarios"]) == 4,
            "PSD", "four complete result scenarios required")
    for record, held in zip(report["scenarios"], prior["scenarios"]):
        verify_scenario(record, held, bands, g, rho)
    equal(canonical_identity(prior), before_prior, "SOURCE", "admitted prior changed during verification")
    equal(canonical_identity(expected_provenance), before_provenance, "SOURCE", "caller metadata changed during verification")
    return {"status": "all_fields_independently_match", "rows": 8, "modes": 65544, "bands": 14, "scenarios": 4}


def load_result(body, source_rows, prior, expected_provenance, *, expected_phase):
    report = decode_json(body)
    equal(identity(body), canonical_identity(report), "CANONICAL", "result is not exact canonical JSON")
    validate_result(report, source_rows, prior, expected_provenance, expected_phase=expected_phase)
    return report


def validate_saved(report, snapshot_path, ri90_body, expected_provenance):
    """Fixed-body admission and independent bounded source-row streaming.

    Both complete body identities precede any scientific decode.  The open
    descriptor, regular path metadata and complete file bytes are rechecked
    after arithmetic.  Root's full prior/source/runtime custody is additional.
    """
    equal(identity(ri90_body), INPUTS["ri90"], "INPUT", "held RI90 body differs before decode")
    require(type(report) is dict and "provenance" in report and "phase" in report,
            "SCHEMA", "saved result admission fields are missing")
    equal(report["phase"], "fixed_saved_application", "PHASE", "saved validation requires actual phase")
    verify_provenance(report["provenance"], expected_provenance, "fixed_saved_application")
    try:
        path, before = regular_snapshot(snapshot_path)
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(descriptor, "rb") as stream:
            require(stat_identity(os.fstat(stream.fileno())) == before, "INPUT", "snapshot descriptor identity differs")
            equal(hash_open_snapshot(stream), INPUTS["snapshot"], "INPUT", "snapshot body differs before decode")
            require(regular_snapshot(path)[1] == before, "INPUT", "snapshot path changed during admission")
            prior = extract_prior(ri90_body)
            stream.seek(0)
            result = validate_result(report, SnapshotReader(stream, INPUTS["snapshot"]).rows(), prior, expected_provenance,
                                     expected_phase="fixed_saved_application")
            equal(identity(ri90_body), INPUTS["ri90"], "INPUT", "held RI90 body differs after verification")
            equal(hash_open_snapshot(stream), INPUTS["snapshot"], "INPUT", "snapshot body differs after verification")
            require(stat_identity(os.fstat(stream.fileno())) == before
                    and regular_snapshot(path)[1] == before, "INPUT", "snapshot metadata changed after verification")
            return result
    except OSError as error:
        raise ValidationError("INPUT", "snapshot filesystem admission failed") from error


if __name__ == "__main__":
    raise SystemExit("RI93 validator requires a separately admitted captured-source caller; no direct launch.")
