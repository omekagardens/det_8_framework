"""Exact shared-bank error propagation through a frozen linear receiver."""

import json
from fractions import Fraction as F
from math import gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind is int:
        _require(value.bit_length() <= 4096, "integer exceeds retained component bound")
    elif value is None or kind in (str, bool):
        return
    elif kind in (list, dict):
        identity = id(value)
        _require(identity not in active, "cyclic native containers are not supported")
        if kind is dict:
            _require(all(type(key) is str for key in value), "native string keys required")
        active.add(identity)
        try:
            for child in value if kind is list else value.values():
                _native(child, active)
        finally:
            active.remove(identity)
    else:
        raise ValueError("exact native mathematical wire required")


def _encode(value):
    if type(value) is F:
        _require(
            max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096,
            "retained fraction exceeds component bound",
        )
        return [value.numerator, value.denominator]
    if type(value) is list:
        return [_encode(x) for x in value]
    if type(value) is dict:
        return {key: _encode(child) for key, child in value.items()}
    return value


def canonical(value):
    _native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
        + "\n"
    ).encode("ascii")


def _detach(value):
    return json.loads(canonical(_encode(value)))


def _fields(value, keys):
    _require(type(value) is dict and set(value) == set(keys), "unexpected fixture fields")


def _fraction(pair):
    _require(type(pair) is list and len(pair) == 2, "native fraction pair required")
    n, d = pair
    _require(
        type(n) is int
        and type(d) is int
        and d > 0
        and max(n.bit_length(), d.bit_length()) <= 4096
        and gcd(n, d) == 1,
        "reduced bounded fraction required",
    )
    return F(n, d)


def _pair_shape(value):
    _require(type(value) is list and len(value) == 2, "native rational-pair shape required")


def _vector_shape(value, width):
    _require(type(value) is list and len(value) == width, "vector width differs")
    for pair in value:
        _pair_shape(pair)


def _matrix_shape(value, rows, columns):
    _require(type(value) is list and len(value) == rows, "matrix row inventory differs")
    for row in value:
        _vector_shape(row, columns)


def _matrix(value):
    return [list(map(_fraction, row)) for row in value]


def _dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True) if x and y), F(0))


def _mm(left, right, columns=None):
    if not right:
        _require(columns is not None, "empty product requires its column dimension")
        return [[F(0)] * columns for _ in left]
    transposed = list(zip(*right, strict=True))
    return [[_dot(row, column) for column in transposed] for row in left]


def _raw_product(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _require(type(matrix) is list and len(matrix) <= row_cap, "matrix row cap")
    _require(type(values) is list and len(values) <= width_cap, "raw value width cap")
    width = len(values)
    _matrix_shape(matrix, len(matrix), width)
    _vector_shape(values, width)
    parsed = _matrix(matrix)
    vector = list(map(_fraction, values))
    return _detach([_dot(row, vector) for row in parsed])


def produce(matrix, values):
    """Apply a raw bank/readout matrix, with no source or file access."""
    return _raw_product(matrix, values, 1024, 1024)


def apply(matrix, observed):
    """Apply a frozen zero-intercept receiver to raw observed values."""
    return _raw_product(matrix, observed, 64, 320)


def _problem(problem):
    _native(problem)
    _fields(
        problem,
        (
            "family",
            "target_labels",
            "interface",
            "geometric",
            "decoder",
            "primitive_map",
            "target_scales",
        ),
    )
    _require(type(problem["family"]) is str and problem["family"], "family label required")
    geometric = problem["geometric"]
    _require(type(geometric) is list and 1 <= len(geometric) <= 64, "target row cap")
    q = len(geometric)
    _require(type(geometric[0]) is list and 1 <= len(geometric[0]) <= 1024, "bank width cap")
    r = len(geometric[0])
    interface = problem["interface"]
    _require(type(interface) is list and len(interface) <= 320, "receiver row cap")
    s = len(interface)
    primitive = problem["primitive_map"]
    _require(type(primitive) is list and len(primitive) == r, "primitive row inventory")
    _require(type(primitive[0]) is list and len(primitive[0]) <= 256, "primitive width cap")
    p = len(primitive[0])
    labels = problem["target_labels"]
    _require(type(labels) is list and len(labels) == q, "target label inventory")
    label_order = []
    for label in labels:
        _fields(label, ("first", "second"))
        _require(
            type(label["first"]) is int and type(label["second"]) is int,
            "native integer target labels required",
        )
        label_order.append((label["first"], label["second"]))
    _require(label_order == sorted(set(label_order)), "sorted unique target labels required")
    _matrix_shape(interface, s, r)
    _matrix_shape(geometric, q, r)
    _matrix_shape(problem["decoder"], q, s)
    _matrix_shape(primitive, r, p)
    _vector_shape(problem["target_scales"], q)
    # Every shape above is complete before any Fraction is constructed.
    B = _matrix(interface)
    G = _matrix(geometric)
    D = _matrix(problem["decoder"])
    W = _matrix(primitive)
    scales = list(map(_fraction, problem["target_scales"]))
    _require(all(scale > 0 for scale in scales), "strictly positive target scales required")
    # Every scalar is admitted before the first mathematical product.
    return B, G, D, W, scales, q, r, s, p


def _subtract(left, right):
    return [[x - y for x, y in zip(a, b, strict=True)] for a, b in zip(left, right, strict=True)]


def _zero(matrix):
    return all(value == 0 for row in matrix for value in row)


def _sign(value):
    return int(value > 0) - int(value < 0)


def _linear(matrix, values):
    return [_dot(row, values) for row in matrix]


def _vector(value):
    return list(map(_fraction, value))


def _maximum(values):
    maximum = max(values)
    return maximum, [index for index, value in enumerate(values) if value == maximum]


def _shared_endpoint(index, direction, signs, wires, H, A, scales, alpha, beta):
    primitive = [F(direction * sign) for sign in signs]
    _require(all(abs(value) <= 1 for value in primitive), "primitive error outside unit box")
    bank_wire = produce(wires["W"], _encode(primitive))
    observed_wire = produce(wires["B"], bank_wire)
    direct_wire = produce(wires["G"], bank_wire)
    decoded_wire = apply(wires["D"], observed_wire)
    bank = _vector(bank_wire)
    observed = _vector(observed_wire)
    direct = _vector(direct_wire)
    decoded = _vector(decoded_wire)
    normalized = [value / scale for value, scale in zip(decoded, scales, strict=True)]
    _require(direct == decoded, "shared endpoint decoder differs from direct target")
    _require(observed == _linear(H, primitive), "shared endpoint interface map differs")
    _require(normalized == _linear(A, primitive), "shared normalized map differs")
    _require(
        all(abs(value) <= gain for value, gain in zip(normalized, alpha, strict=True)),
        "shared endpoint exceeds a target bound",
    )
    _require(
        all(abs(value) <= radius for value, radius in zip(observed, beta, strict=True)),
        "shared endpoint exceeds a receiver radius",
    )
    attained = normalized[index]
    _require(attained == direction * alpha[index], "shared endpoint does not attain bound")
    return {
        "primitive": primitive,
        "bank_error": bank,
        "observed_error": observed,
        "direct_error": direct,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "attained": attained,
    }


def _enclosure_endpoint(index, direction, signs, decoder_wire, scales, beta, gamma, E):
    observed = [direction * radius * sign for radius, sign in zip(beta, signs, strict=True)]
    decoded = _vector(apply(decoder_wire, _encode(observed)))
    normalized = [value / scale for value, scale in zip(decoded, scales, strict=True)]
    _require(
        normalized == _linear(E, [F(direction * sign) for sign in signs]),
        "enclosure normalized map differs",
    )
    _require(
        all(abs(value) <= radius for value, radius in zip(observed, beta, strict=True)),
        "enclosure endpoint outside receiver box",
    )
    _require(
        all(abs(value) <= gain for value, gain in zip(normalized, gamma, strict=True)),
        "enclosure endpoint exceeds a target bound",
    )
    attained = normalized[index]
    _require(attained == direction * gamma[index], "enclosure endpoint does not attain bound")
    return {
        "observed_error": observed,
        "decoded_error": decoded,
        "normalized_error": normalized,
        "attained": attained,
    }


def build_family(problem):
    """Certify common-bank and independent receiver-box error bounds exactly."""
    B, G, D, W, scales, q, r, s, p = _problem(problem)
    K = _mm(D, B, r)
    bank_residual = _subtract(K, G)
    _require(_zero(bank_residual), "frozen decoder-bank identity is false")
    H = _mm(B, W, p)
    J = _mm(G, W, p)
    L = _mm(D, H, p)
    error_residual = _subtract(L, J)
    _require(_zero(error_residual), "frozen error-map identity is false")
    A = [[value / scales[i] for value in row] for i, row in enumerate(J)]
    beta = [sum(map(abs, row), F(0)) for row in H]
    E = [
        [value * radius / scales[i] for value, radius in zip(row, beta, strict=True)]
        for i, row in enumerate(D)
    ]
    alpha = [sum(map(abs, row), F(0)) for row in A]
    gamma = [sum(map(abs, row), F(0)) for row in E]
    gap = [upper - lower for lower, upper in zip(alpha, gamma, strict=True)]
    _require(all(value >= 0 for value in gap), "receiver box fails to enclose shared errors")
    strict = [index for index, value in enumerate(gap) if value > 0]
    tied = [index for index, value in enumerate(gap) if value == 0]
    _require(sorted(strict + tied) == list(range(q)), "incomplete gain partition")
    shared_max, shared_rows = _maximum(alpha)
    enclosure_max, enclosure_rows = _maximum(gamma)
    gap_max, gap_rows = _maximum(gap)
    wires = {"B": _encode(B), "G": _encode(G), "D": _encode(D), "W": _encode(W)}
    shared_witnesses = []
    enclosure_witnesses = []
    for index in range(q):
        signs = list(map(_sign, A[index]))
        shared_witnesses.append(
            {
                "target_row": index,
                "signs": signs,
                "positive": _shared_endpoint(index, 1, signs, wires, H, A, scales, alpha, beta),
                "negative": _shared_endpoint(index, -1, signs, wires, H, A, scales, alpha, beta),
            }
        )
        enclosure_signs = list(map(_sign, E[index]))
        enclosure_witnesses.append(
            {
                "target_row": index,
                "signs": enclosure_signs,
                "positive": _enclosure_endpoint(
                    index, 1, enclosure_signs, wires["D"], scales, beta, gamma, E
                ),
                "negative": _enclosure_endpoint(
                    index, -1, enclosure_signs, wires["D"], scales, beta, gamma, E
                ),
            }
        )
    return _detach(
        {
            "problem": problem,
            "maps": {
                "decoder_bank": K,
                "bank_residual": bank_residual,
                "interface_error": H,
                "target_error": J,
                "decoded_error": L,
                "error_residual": error_residual,
                "normalized_target": A,
                "enclosure_target": E,
            },
            "shared": {
                "row_gains": alpha,
                "witnesses": shared_witnesses,
                "max_gain": shared_max,
                "max_rows": shared_rows,
            },
            "enclosure": {
                "receiver_radii": beta,
                "row_gains": gamma,
                "witnesses": enclosure_witnesses,
                "max_gain": enclosure_max,
                "max_rows": enclosure_rows,
                "common_bank_feasibility_tested": False,
            },
            "comparison": {
                "gain_gap": gap,
                "strict_rows": strict,
                "tied_rows": tied,
                "max_gap": gap_max,
                "max_gap_rows": gap_rows,
            },
            "checks": {
                "frozen_bank_identity": True,
                "error_map_identity": True,
                "normalized_error_identity": True,
                "primitive_box": True,
                "shared_pipeline": True,
                "shared_attainment": True,
                "enclosure_box": True,
                "enclosure_attainment": True,
                "complete_gain_partition": True,
            },
            "counts": {
                "bank_values": r,
                "receiver_values": s,
                "primitive_values": p,
                "target_rows": q,
                "input_matrix_entries": s * r + q * r + q * s + r * p + q,
                "map_entries": 2 * q * r + s * p + 4 * q * p + q * s,
                "gain_entries": s + 3 * q + 3,
                "shared_witnesses": 2 * q,
                "shared_sign_entries": q * p,
                "shared_witness_entries": 2 * q * (p + r + s + 3 * q + 1),
                "enclosure_witnesses": 2 * q,
                "enclosure_sign_entries": q * s,
                "enclosure_witness_entries": 2 * q * (s + 2 * q + 1),
                "shared_maximizers": len(shared_rows),
                "enclosure_maximizers": len(enclosure_rows),
                "gap_maximizers": len(gap_rows),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )
