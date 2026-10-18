"""QR-05AV independent reference: raw column probes and interval endpoints.

The source producer and receiver evaluate only explicitly supplied raw values.
No historical executor, geometry, stored answer or hidden file is consumed.
"""

from copy import deepcopy
from fractions import Fraction
from math import gcd

MAX_BITS = 4096
ZERO = Fraction(0)
ONE = Fraction(1)


def _need(condition, message):
    if not condition:
        raise ValueError(message)


def _native(value):
    """Native containers may share children, but may not contain cycles."""
    pending = [(value, False)]
    active, done = set(), set()
    while pending:
        current, leaving = pending.pop()
        kind = type(current)
        if kind in (dict, list):
            identity = id(current)
            if leaving:
                active.remove(identity)
                done.add(identity)
                continue
            _need(identity not in active, "cyclic native input")
            if identity in done:
                continue
            active.add(identity)
            pending.append((current, True))
            if kind is dict:
                _need(all(type(k) is str for k in current), "native object keys")
                pending.extend((v, False) for v in current.values())
            else:
                pending.extend((v, False) for v in current)
        else:
            _need(kind in (str, int, type(None)), "non-native mathematical input")
            if kind is int:
                _need(abs(current).bit_length() <= MAX_BITS, "integer bits")


def _keys(value, expected):
    _need(type(value) is dict and set(value) == set(expected), "object fields")


def _fraction(value):
    _need(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    _need(type(n) is int and type(d) is int and d > 0, "fraction integers")
    _need(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "fraction bits")
    _need(gcd(n, d) == 1, "reduced fraction")
    return Fraction(n, d)


def _wire(value):
    if type(value) is Fraction:
        _need(
            max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
            "retained rational bits",
        )
        return [value.numerator, value.denominator]
    if type(value) in (list, tuple):
        return [_wire(x) for x in value]
    if type(value) is dict:
        return {k: _wire(v) for k, v in value.items()}
    if type(value) is int:
        _need(abs(value).bit_length() <= MAX_BITS, "retained integer bits")
    _need(type(value) in (str, int, bool, type(None)), "internal output type")
    return value


def _dimensions(matrix, rows, columns):
    _need(type(matrix) is list and len(matrix) == rows, "matrix rows")
    _need(
        all(type(row) is list and len(row) == columns for row in matrix),
        "matrix width",
    )


def _matrix(matrix):
    return [[_fraction(x) for x in row] for row in matrix]


def _dot(row, vector):
    return sum((a * b for a, b in zip(row, vector) if a and b), ZERO)


def _pair_shapes(values):
    _need(all(type(x) is list and len(x) == 2 for x in values), "rational pair shapes")


def _matrix_pair_shapes(matrix):
    for row in matrix:
        _pair_shapes(row)


def _matvec(matrix, vector):
    return [_dot(row, vector) for row in matrix]


def _evaluate(matrix, values, row_cap, width_cap):
    _native(matrix)
    _native(values)
    _need(type(matrix) is list and len(matrix) <= row_cap, "raw evaluator row inventory")
    _need(type(values) is list and len(values) <= width_cap, "raw evaluator width")
    _dimensions(matrix, len(matrix), len(values))
    _matrix_pair_shapes(matrix)
    _pair_shapes(values)
    rows = _matrix(matrix)
    vector = [_fraction(x) for x in values]
    return _wire(_matvec(rows, vector))


def produce(matrix, values):
    """Raw linear production; no hidden source, geometry or calibration."""
    return _evaluate(matrix, values, 1024, 1024)


def apply(matrix, observed):
    """The supplied zero-intercept receiver on raw ordered input only."""
    return _evaluate(matrix, observed, 64, 320)


def _parse(problem):
    _native(problem)
    _keys(
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
    _need(type(problem["family"]) is str and bool(problem["family"]), "family label")
    B, G, D, W = (problem[k] for k in ("interface", "geometric", "decoder", "primitive_map"))
    sigma = problem["target_scales"]
    _need(type(G) is list and 1 <= len(G) <= 64, "target row inventory")
    _need(type(G[0]) is list and 1 <= len(G[0]) <= 1024, "bank inventory")
    q, r = len(G), len(G[0])
    _need(type(B) is list and len(B) <= 320, "receiver inventory")
    s = len(B)
    _need(type(W) is list and len(W) == r, "primitive bank inventory")
    _need(type(W[0]) is list and len(W[0]) <= 256, "primitive width")
    p = len(W[0])
    for matrix, rows, columns in ((B, s, r), (G, q, r), (D, q, s), (W, r, p)):
        _dimensions(matrix, rows, columns)
    _need(type(sigma) is list and len(sigma) == q, "target reference inventory")
    labels = problem["target_labels"]
    _need(type(labels) is list and len(labels) == q, "target label inventory")
    pairs = []
    for label in labels:
        _keys(label, ("first", "second"))
        _need(type(label["first"]) is int and type(label["second"]) is int, "native target IDs")
        pairs.append((label["first"], label["second"]))
    _need(pairs == sorted(set(pairs)), "sorted unique target labels")
    for matrix in (B, G, D, W):
        _matrix_pair_shapes(matrix)
    _pair_shapes(sigma)
    # Every dimension, label and pair shape precedes Fraction construction.
    B, G, D, W = (_matrix(matrix) for matrix in (B, G, D, W))
    sigma = [_fraction(value) for value in sigma]
    _need(all(value > ZERO for value in sigma), "positive target reference scales")
    return B, G, D, W, sigma, p


def _values(wire):
    return [_fraction(value) for value in wire]


def _columns(rows, columns):
    """Allocate the known shape, including positive rows with zero columns."""
    return [[ZERO] * columns for _ in range(rows)]


def _probe_maps(problem, B, G, D, W, p):
    """Recover every map through actual raw bank and primitive column calls."""
    q, r, s = len(G), len(G[0]), len(B)
    K = _columns(q, r)
    for j in range(r):
        bank_basis = [ZERO] * r
        bank_basis[j] = ONE
        receiver_column = produce(problem["interface"], _wire(bank_basis))
        decoded_column = _values(apply(problem["decoder"], receiver_column))
        for i, value in enumerate(decoded_column):
            K[i][j] = value
    bank_residual = [[K[i][j] - G[i][j] for j in range(r)] for i in range(q)]
    _need(not any(x for row in bank_residual for x in row), "full frozen bank identity")

    # Restriction begins only AFTER the full bank identity, even for p=0.
    H, J, L = _columns(s, p), _columns(q, p), _columns(q, p)
    for j in range(p):
        bank_column = _wire([row[j] for row in W])
        h_wire = produce(problem["interface"], bank_column)
        h = _values(h_wire)
        direct = _values(produce(problem["geometric"], bank_column))
        decoded = _values(apply(problem["decoder"], h_wire))
        for i, value in enumerate(h):
            H[i][j] = value
        for i in range(q):
            J[i][j], L[i][j] = direct[i], decoded[i]
    error_residual = [[L[i][j] - J[i][j] for j in range(p)] for i in range(q)]
    _need(not any(x for row in error_residual for x in row), "complete restricted error identity")
    return K, bank_residual, H, J, L, error_residual


def _interval_radius(row):
    """Sum independent lower/upper coordinate contributions, not a norm helper."""
    lower, upper = ZERO, ZERO
    for value in row:
        lower += min(-value, value)
        upper += max(-value, value)
    _need(lower == -upper and upper >= ZERO, "symmetric coordinate interval")
    return upper


def _sign(value):
    return int(value > ZERO) - int(value < ZERO)


def _maximum(values):
    largest = max(values)
    return largest, [i for i, value in enumerate(values) if value == largest]


def build_family(problem):
    """Certify sharp common-error and enclosing-box endpoints without refitting."""
    B, G, D, W, sigma, p = _parse(problem)
    q, r, s = len(G), len(G[0]), len(B)
    K, R_bank, H, J, L, R_error = _probe_maps(problem, B, G, D, W, p)
    A = [[value / sigma[i] for value in row] for i, row in enumerate(J)]
    beta = [_interval_radius(row) for row in H]
    E = [[D[i][j] * beta[j] / sigma[i] for j in range(s)] for i in range(q)]
    alpha = [_interval_radius(row) for row in A]
    gamma = [_interval_radius(row) for row in E]
    gap = [right - left for left, right in zip(alpha, gamma)]
    _need(all(value >= ZERO for value in gap), "conservative coordinate enclosure")
    shared_witnesses, enclosure_witnesses = [], []
    for target in range(q):
        signs = [_sign(value) for value in A[target]]
        endpoints = []
        for direction in (ONE, -ONE):
            primitive = [direction * value for value in signs]
            _need(all(-ONE <= value <= ONE for value in primitive), "primitive unit box")
            bank_wire = produce(problem["primitive_map"], _wire(primitive))
            observed_wire = produce(problem["interface"], bank_wire)
            direct_wire = produce(problem["geometric"], bank_wire)
            decoded_wire = apply(problem["decoder"], observed_wire)
            bank_error, observed, direct, decoded = (
                _values(values) for values in (bank_wire, observed_wire, direct_wire, decoded_wire)
            )
            normalized = [value / sigma[i] for i, value in enumerate(decoded)]
            _need(
                bank_error == _matvec(W, primitive)
                and observed == _matvec(H, primitive)
                and direct == decoded
                and normalized == _matvec(A, primitive),
                "complete common primitive pipeline",
            )
            _need(
                all(-radius <= value <= radius for value, radius in zip(normalized, alpha))
                and all(-radius <= value <= radius for value, radius in zip(observed, beta)),
                "complete common endpoint bounds",
            )
            _need(normalized[target] == direction * alpha[target], "shared signed attainment")
            endpoints.append(
                {
                    "primitive": primitive,
                    "bank_error": bank_error,
                    "observed_error": observed,
                    "direct_error": direct,
                    "decoded_error": decoded,
                    "normalized_error": normalized,
                    "attained": normalized[target],
                }
            )
        shared_witnesses.append(
            {
                "target_row": target,
                "signs": signs,
                "positive": endpoints[0],
                "negative": endpoints[1],
            }
        )

        enclosure_signs = [_sign(value) for value in E[target]]
        endpoints = []
        for direction in (ONE, -ONE):
            observed = [direction * radius * sign for radius, sign in zip(beta, enclosure_signs)]
            _need(
                all(-radius <= value <= radius for value, radius in zip(observed, beta)),
                "enclosure box",
            )
            decoded = _values(apply(problem["decoder"], _wire(observed)))
            normalized = [value / sigma[i] for i, value in enumerate(decoded)]
            _need(
                decoded == _matvec(D, observed)
                and all(-radius <= value <= radius for value, radius in zip(normalized, gamma)),
                "full enclosure endpoint response",
            )
            _need(normalized[target] == direction * gamma[target], "enclosure signed attainment")
            endpoints.append(
                {
                    "observed_error": observed,
                    "decoded_error": decoded,
                    "normalized_error": normalized,
                    "attained": normalized[target],
                }
            )
        enclosure_witnesses.append(
            {
                "target_row": target,
                "signs": enclosure_signs,
                "positive": endpoints[0],
                "negative": endpoints[1],
            }
        )
    shared_max, shared_rows = _maximum(alpha)
    enclosure_max, enclosure_rows = _maximum(gamma)
    max_gap, max_gap_rows = _maximum(gap)
    strict = [i for i, value in enumerate(gap) if value > ZERO]
    tied = [i for i, value in enumerate(gap) if value == ZERO]
    _need(sorted(strict + tied) == list(range(q)), "complete gain partition")
    return _wire(
        {
            "problem": deepcopy(problem),
            "maps": {
                "decoder_bank": K,
                "bank_residual": R_bank,
                "interface_error": H,
                "target_error": J,
                "decoded_error": L,
                "error_residual": R_error,
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
                "max_gap": max_gap,
                "max_gap_rows": max_gap_rows,
            },
            "checks": dict.fromkeys(
                (
                    "frozen_bank_identity",
                    "error_map_identity",
                    "normalized_error_identity",
                    "primitive_box",
                    "shared_pipeline",
                    "shared_attainment",
                    "enclosure_box",
                    "enclosure_attainment",
                    "complete_gain_partition",
                ),
                True,
            ),
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
                "gap_maximizers": len(max_gap_rows),
                "strict_rows": len(strict),
                "tied_rows": len(tied),
            },
        }
    )
