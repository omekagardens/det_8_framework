#!/usr/bin/env python3
"""Independent, stdlib-only closed RI86 result validator.

Validation rederives the exact proxy algebra from retained PSD records and the
selected prior certificate. It does not prove external source/data custody,
reconstruct the held operator, execute an FFT, or read any scientific file.
No computation is run on import. A separately admitted caller supplies bytes.
"""

from fractions import Fraction
import hashlib
import json
import math
import re
import struct


BITS = 262144
DESIGN = {"bytes": 32470, "sha256": "2a00cac0017f0b749ed958efef4d623143c97e33ba36c60454a65ef9069dc04e"}
INPUTS = {
    "ri83": {"bytes": 38952074, "sha256": "e7aad05d912401b9b65c54579b46456bd8077afdc60079d0414fd2043844ed2f"},
    "ri73": {"bytes": 11180937, "sha256": "3a69e1f30042d3dcfed4a7fa95b59b7a8984de1e0ec4059a26f4ca25604b39fe"},
}
ORDER = ["H1:left", "H1:right", "L1:left", "L1:right"]
ROWS = [0, 1, 27, 805, 1384, 2741, 2767, 2768]
CERT_CHECKS = ["G_symmetry", "H_symmetry_nonnegative", "positive_LDL",
               "LDL_reconstruction", "two_sided_inverse", "delta_identity",
               "gamma_identity", "rho_identity", "rho_mathematical", "rho_accuracy"]
GATE_IDS = ["admission:metadata", "admission:certificate", "scenario:H1:left",
            "scenario:H1:right", "scenario:L1:left", "scenario:L1:right", "completion:algebra"]
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
    if type(expected) is list:
        return len(actual) == len(expected) and all(same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def equal(actual, expected, code, message):
    require(same(actual, expected), code, message)


def bounded(value):
    require(type(value) is Fraction, "EXACT", "exact Fraction required")
    require(max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= BITS,
            "RESOURCE", "exact rational exceeds the fixed bit cap")
    return value


def add(a, b):
    return bounded(bounded(a) + bounded(b))


def subtract(a, b):
    return bounded(bounded(a) - bounded(b))


def multiply(a, b):
    return bounded(bounded(a) * bounded(b))


def total(values):
    result = Fraction(0)
    for value in values:
        result = add(result, value)
    return result


def decode_scalar(pair):
    require(type(pair) is list and len(pair) == 2, "EXACT", "rational pair required")
    for i, value in enumerate(pair):
        require(type(value) is str and len(value) <= (BITS + 3) // 4 + (i == 0),
                "RESOURCE", "rational hexadecimal text exceeds cap")
        pattern = r"(?:0|-?[1-9a-f][0-9a-f]*)" if i == 0 else r"[1-9a-f][0-9a-f]*"
        require(re.fullmatch(pattern, value) is not None, "EXACT", "noncanonical rational hexadecimal text")
    numerator, denominator = int(pair[0], 16), int(pair[1], 16)
    require(max(abs(numerator).bit_length(), denominator.bit_length()) <= BITS,
            "RESOURCE", "parsed rational exceeds cap")
    value = bounded(Fraction(numerator, denominator))
    equal(pair, [format(value.numerator, "x"), format(value.denominator, "x")],
          "EXACT", "unreduced rational pair")
    return value


def encoded(value):
    if type(value) is Fraction:
        value = bounded(value)
        return [format(value.numerator, "x"), format(value.denominator, "x")]
    if type(value) is list:
        return [encoded(x) for x in value]
    if type(value) is dict:
        return {k: encoded(v) for k, v in value.items()}
    return value


def float_hex(value, nonnegative=True):
    require(type(value) is str, "HEX", "float hexadecimal string required")
    # Every canonical finite binary64 hex fits comfortably within this bound.
    require(len(value) <= 32, "HEX", "noncanonical binary64 hexadecimal length")
    try:
        number = float.fromhex(value)
    except OverflowError as error:
        raise ValidationError("NONFINITE", "overflowing binary64 literal") from error
    except ValueError as error:
        raise ValidationError("HEX", "invalid binary64 literal") from error
    require(math.isfinite(number), "NONFINITE", "nonfinite binary64 value")
    require(number.hex() == value, "HEX", "noncanonical binary64 hexadecimal string")
    if nonnegative:
        require(number >= 0, "NEGATIVE_PSD", "negative finite power")
    return number, bounded(Fraction.from_float(number))


def decode_psd(record):
    keys(record, ("dtype", "shape", "values_hex", "sha256"), "SCHEMA")
    equal(record["dtype"], "<f8", "DTYPE", "PSD dtype differs")
    equal(record["shape"], [8193], "BINS", "PSD shape differs")
    require(type(record["values_hex"]) is list and len(record["values_hex"]) == 8193,
            "BINS", "PSD must retain all 8193 bins")
    require(type(record["sha256"]) is str and re.fullmatch(r"[0-9a-f]{64}", record["sha256"]) is not None,
            "IDENTITY", "invalid PSD byte identity")
    hasher, result = hashlib.sha256(), []
    for text in record["values_hex"]:
        value, rational = float_hex(text)
        hasher.update(struct.pack("<d", value))
        result.append(rational)
    equal(hasher.hexdigest(), record["sha256"], "IDENTITY", "PSD bytes differ from retained identity")
    return result


def matrix(value, size, code="CERT_SCHEMA"):
    require(type(value) is list and len(value) == size, code, "matrix row count differs")
    result = []
    for row in value:
        require(type(row) is list and len(row) == size, code, "matrix column count differs")
        result.append([decode_scalar(x) for x in row])
    return result


def product(a, b):
    size = len(a)
    return [[total(multiply(a[i][k], b[k][j]) for k in range(size))
             for j in range(size)] for i in range(size)]


def certificate(value):
    keys(value, ("source_gate", "source_model", "G", "H", "V", "ldl", "delta", "gamma", "rho", "checks"),
         "CERT_SCHEMA")
    equal(value["source_gate"], "integration:gram", "CERT_SCHEMA", "selected prior gate differs")
    equal(value["source_model"], "known_synthetic_unit_white", "PRIOR_MODEL", "inherited model changed")
    equal(value["checks"], CERT_CHECKS, "CERT_SCHEMA", "prior exact check labels differ")
    size = 8
    g, h, inverse = (matrix(value[k], size) for k in ("G", "H", "V"))
    require(all(g[i][j] == g[j][i] for i in range(size) for j in range(size)),
            "GRAM_SYMMETRY", "G is not symmetric")
    require(all(h[i][j] == h[j][i] for i in range(size) for j in range(size)),
            "ERROR_SYMMETRY", "H is not symmetric")
    require(all(x >= 0 for row in h for x in row), "ERROR_NEGATIVE", "H has a negative entry")
    keys(value["ldl"], ("lower", "pivots", "reconstruction"), "CERT_SCHEMA")
    lower = matrix(value["ldl"]["lower"], size)
    reconstruction = matrix(value["ldl"]["reconstruction"], size)
    require(type(value["ldl"]["pivots"]) is list and len(value["ldl"]["pivots"]) == size,
            "CERT_SCHEMA", "LDL pivot count differs")
    pivots = [decode_scalar(x) for x in value["ldl"]["pivots"]]
    require(all(p > 0 for p in pivots), "LDL_PIVOT", "nonpositive LDL pivot")
    require(all(lower[i][j] == (1 if i == j else 0) for i in range(size) for j in range(i, size)),
            "LDL_RECONSTRUCTION", "LDL lower factor is not unit lower triangular")
    reconstructed = [[total(multiply(multiply(lower[i][k], pivots[k]), lower[j][k]) for k in range(size))
                      for j in range(size)] for i in range(size)]
    require(reconstruction == g and reconstructed == g, "LDL_RECONSTRUCTION", "LDL does not reconstruct G")
    eye = [[Fraction(int(i == j)) for j in range(size)] for i in range(size)]
    require(product(g, inverse) == eye and product(inverse, g) == eye, "INVERSE", "two-sided inverse check failed")
    delta, gamma, rho = (decode_scalar(value[k]) for k in ("delta", "gamma", "rho"))
    require(delta == max(total(row) for row in h), "DELTA", "delta is not the maximum H row sum")
    require(gamma == max(total(bounded(abs(x)) for x in row) for row in inverse),
            "GAMMA", "gamma is not the maximum absolute inverse row sum")
    require(rho >= 0 and rho < 1, "RHO", "rho is outside its mathematical domain")
    require(rho == multiply(delta, gamma), "RHO_IDENTITY", "rho differs from delta times gamma")
    require(rho <= Fraction(1, 10**12), "RHO_ACCURACY", "application rho exceeds the held usefulness gate")
    return g, rho


def pin(value, code):
    keys(value, ("bytes", "sha256"), code)
    require(type(value["bytes"]) is int and value["bytes"] > 0
            and type(value["sha256"]) is str
            and re.fullmatch(r"[0-9a-f]{64}", value["sha256"]) is not None,
            code, "invalid positive-length byte/SHA256 pin")


def provenance(value, phase):
    keys(value, ("sources", "inputs", "acceptance", "runtime"), "PROVENANCE")
    keys(value["sources"], ("design", "consumer", "validator", "qualifier", "implementation"), "SOURCE")
    for item in value["sources"].values():
        pin(item, "SOURCE")
    equal(value["sources"]["design"], DESIGN, "SOURCE", "accepted RI86 design identity changed")
    keys(value["inputs"], ("ri83", "ri73"), "INPUT")
    for name, item in value["inputs"].items():
        pin(item, "INPUT")
        if phase == "fixed_saved_application":
            equal(item, INPUTS[name], "INPUT", "actual predecessor identity changed")
        else:
            require(not same(item, INPUTS[name]), "PHASE", "fabricated input masquerades as actual predecessor")
    keys(value["acceptance"], ("ri83", "ri73", "ri86", "qualification"), "CUSTODY")
    for name, item in value["acceptance"].items():
        if name == "qualification" and phase == "fabricated_qualification":
            require(item is None, "PHASE", "fabricated qualification is not already accepted")
            continue
        pin(item, "CUSTODY")
    keys(value["runtime"], ("inventory", "fingerprint", "interpreter"), "RUNTIME")
    for item in value["runtime"].values():
        pin(item, "RUNTIME")


def context(detector, side):
    left = side == "left"
    return {"interval": [0, 65536] if left else [69632, 131072],
            "starts": [0, 8192, 16384, 24576, 32768, 40960, 49152] if left
                      else [69632, 77824, 86016, 94208, 102400, 110592],
            "count": 7 if left else 6,
            "used_interval": [0, 65536] if left else [69632, 126976],
            "unused_intervals": [] if left else [[126976, 131072]],
            "psd_unit": "nominal_strain_squared_per_Hz", "asd_unit": "nominal_strain_per_sqrt_Hz",
            "prior_access": "known_public_development", "Yunits": "", "injection_mask": 31 if detector == "H1" else 23,
            "dq_mask": 127, "NO_CW_HW_INJ": detector == "H1"}


def scenario(value, detector, side, detector_index, side_index, g, rho):
    keys(value, ("id", "detector", "side", "source_pointer", "source_record", "saved_q_hex", "context",
                 "q_difference", "derived"))
    equal(value["id"], detector + ":" + side, "DETECTOR_ORDER", "scenario identifier differs")
    equal(value["detector"], detector, "DETECTOR_ORDER", "scenario detector differs")
    equal(value["side"], side, "SIDE", "scenario side differs")
    equal(value["source_pointer"], "/detectors/{}/sides/{}/mean_psd".format(detector_index, side_index),
          "PSD_SELECTION", "original mean PSD pointer differs")
    equal(value["context"], context(detector, side), "METADATA", "side, flag or unit context differs")
    psd = decode_psd(value["source_record"])
    _, saved_q = float_hex(value["saved_q_hex"])
    # Derive each spectral coordinate independently from the complete input.
    dc = multiply(Fraction(4096), psd[0])
    nyquist = multiply(Fraction(4096), psd[-1])
    non_dc = [multiply(Fraction(2048), psd[k]) for k in range(1, 8192)] + [nyquist]
    q_proxy = multiply(Fraction(1, 4), total(psd))
    ell, upper_eigenvalue = min(non_dc), max(non_dc)
    minimum_indices = [k for k, x in enumerate(non_dc, 1) if x == ell]
    maximum_indices = [k for k, x in enumerate(non_dc, 1) if x == upper_eigenvalue]
    positives = sum(x > 0 for x in psd[1:-1])
    non_dc_rank = 2 * positives + int(psd[-1] > 0)
    rank_upper = min(8, non_dc_rank)
    rank_status = "positive_definite_rank8" if ell > 0 else "zero_rank0" if upper_eigenvalue == 0 else "unresolved_by_envelope"
    low_factor = multiply(ell, subtract(Fraction(1), rho))
    high_factor = multiply(upper_eigenvalue, add(Fraction(1), rho))
    lower = [[multiply(low_factor, x) for x in row] for row in g]
    upper = [[multiply(high_factor, x) for x in row] for row in g]
    expected = {"lambda_dc": dc, "lambda_nyquist": nyquist, "non_dc_eigenvalues": non_dc,
                "q_proxy": q_proxy, "ell": ell, "u": upper_eigenvalue,
                "minimum_indices": minimum_indices, "maximum_indices": maximum_indices,
                "zero_interior_count": 8191 - positives, "positive_interior_count": positives,
                "spectral_rank": non_dc_rank + int(psd[0] > 0), "non_dc_rank": non_dc_rank,
                "rank_upper": rank_upper, "rank_status": rank_status, "singularity_proved": rank_upper < 8,
                "lower": lower, "upper": upper, "diagonal": [[lower[i][i], upper[i][i]] for i in range(8)],
                "trace": [total(lower[i][i] for i in range(8)), total(upper[i][i] for i in range(8))]}
    keys(value["derived"], expected)
    codes = {"lambda_dc": "PSD_MAPPING", "lambda_nyquist": "PSD_MAPPING", "non_dc_eigenvalues": "PSD_MAPPING",
             "q_proxy": "Q_PROXY", "ell": "EXTREMA", "u": "EXTREMA", "minimum_indices": "EXTREMA",
             "maximum_indices": "EXTREMA", "zero_interior_count": "RANK", "positive_interior_count": "RANK",
             "spectral_rank": "RANK", "non_dc_rank": "RANK", "rank_upper": "RANK", "rank_status": "RANK",
             "singularity_proved": "RANK", "lower": "ENVELOPE", "upper": "ENVELOPE", "diagonal": "ENVELOPE", "trace": "ENVELOPE"}
    for field, calculated in expected.items():
        equal(value["derived"][field], encoded(calculated), codes[field], "derived field differs: " + field)
    equal(value["q_difference"], encoded(subtract(q_proxy, saved_q)), "Q_DIFFERENCE", "saved q difference differs")


def validate_result(report, *, expected_phase=None):
    keys(report, ("schema", "phase", "status", "model", "dimensions", "fs", "df", "scenario_order", "rows",
                  "provenance", "certificate", "scenarios", "gates", "limitations"))
    equal(report["schema"], "ri86-colored-proxy-envelope-v1", "SCHEMA", "result schema differs")
    require(type(report["phase"]) is str and report["phase"] in ("fabricated_qualification", "fixed_saved_application"),
            "PHASE", "unknown result phase")
    if expected_phase is not None:
        require(type(expected_phase) is str and expected_phase in ("fabricated_qualification", "fixed_saved_application"),
                "PHASE", "unknown expected phase")
        equal(report["phase"], expected_phase, "PHASE", "fabricated/actual phase does not match admission")
    equal(report["status"], "all_gates_passed", "STATUS", "incomplete result status")
    equal(report["model"], "postulated_finite_circulant_from_empirical_psd", "MODEL", "proxy model changed")
    equal(report["dimensions"], {"M": 16384, "N": 2769, "L": 4096, "T": 10961, "output": 8},
          "DIMENSIONS", "fixed dimensions changed")
    equal(report["fs"], encoded(Fraction(4096)), "METHOD", "sample rate changed")
    equal(report["df"], encoded(Fraction(1, 4)), "BINS", "frequency spacing changed")
    equal(report["scenario_order"], ORDER, "DETECTOR_ORDER", "scenario order changed")
    equal(report["rows"], ROWS, "ROWS", "operator row order changed")
    provenance(report["provenance"], report["phase"])
    g, rho = certificate(report["certificate"])
    require(type(report["scenarios"]) is list and len(report["scenarios"]) == 4,
            "SCHEMA", "complete four-scenario list required")
    for index, (detector, side) in enumerate((("H1", "left"), ("H1", "right"), ("L1", "left"), ("L1", "right"))):
        scenario(report["scenarios"][index], detector, side, index // 2, index % 2, g, rho)
    equal(report["gates"], {"inventory": GATE_IDS, "counts": {"total": 7, "passed": 7, "failed": 0},
                           "results": [{"id": name, "passed": True} for name in GATE_IDS]},
          "GATE_INVENTORY", "complete passed gate inventory differs")
    equal(report["limitations"], LIMITATIONS, "LIMITATIONS", "claim boundary literals changed")
    return True


def load_result(payload, *, expected_phase=None):
    require(type(payload) is bytes, "SCHEMA", "retained result bytes required")
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "DUPLICATE_JSON", "duplicate JSON key")
            result[key] = value
        return result
    def reject(token):
        raise ValidationError("NONFINITE", "JSON decimal/nonfinite literal forbidden: " + token)
    try:
        report = json.loads(payload, object_pairs_hook=pairs, parse_float=reject, parse_constant=reject)
    except ValidationError:
        raise
    except (UnicodeDecodeError, ValueError, RecursionError) as error:
        raise ValidationError("SCHEMA", "invalid scientific JSON") from error
    try:
        canonical = (json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")
    except (ValueError, TypeError, RecursionError) as error:
        raise ValidationError("SCHEMA", "scientific JSON cannot be canonicalized") from error
    require(payload == canonical, "CANONICAL_JSON", "scientific JSON is not exact canonical indent-two bytes")
    validate_result(report, expected_phase=expected_phase)
    return report
