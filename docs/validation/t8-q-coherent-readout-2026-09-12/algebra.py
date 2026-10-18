"""Symbolic directed-pair composition; no matrix/instrument input.

This small internal checker implements the assumed algebra in CANDIDATE.md.
Coefficients of the specific history/branch elements are rational and real;
functional values may be exact complex numbers. It is not a public validator
of arbitrary positive kernels. Positivity remains an explicit domain premise.
"""

from fractions import Fraction as F
from itertools import product

LABELS = tuple(product((0, 1), (1, -1), (0, 1), (1, -1)))
UNITS = tuple(product(range(4), repeat=2))


def clean(a):
    return {ij: value for ij, value in a.items() if value != 0}


def add(*terms):
    out = {}
    for a in terms:
        for ij, value in a.items():
            out[ij] = out.get(ij, F(0)) + value
    return clean(out)


def scale(a, factor):
    return clean({ij: factor * value for ij, value in a.items()})


def mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if j == k:
                out[i, l] = out.get((i, l), F(0)) + x * y
    return clean(out)


def star(a):
    # All element coefficients used here are real rationals.
    return {(j, i): value for (i, j), value in a.items()}


ONE = {(i, i): F(1) for i in range(4)}


def lift(local, port):
    """Tensor a local directed-pair element with the other identity."""
    out = {}
    for (i, j), value in local.items():
        for other in (0, 1):
            ij = (2 * i + other, 2 * j + other) if port == "a" else (2 * other + i, 2 * other + j)
            out[ij] = value
    return out


def involution(port, context):
    local = {(0, 1): F(1), (1, 0): F(1)} if context == 0 else {(0, 0): F(1), (1, 1): F(-1)}
    return lift(local, port)


def projector(action, context, outcome):
    if action not in ("a", "b", "ab") or context not in (0, 1) or outcome not in (0, 1):
        raise ValueError("Expected declared action, context and binary outcome")
    t = ONE
    for port in action:
        t = mul(t, involution(port, context))
    return scale(add(ONE, scale(t, (-1) ** outcome)), F(1, 2))


def history(label):
    i, s, j, t = label
    qa = scale(add(ONE, scale(involution("a", 0), s)), F(1, 2))
    qb = scale(add(ONE, scale(involution("b", 0), t)), F(1, 2))
    za = lift({(i, i): F(1)}, "a")
    zb = lift({(j, j): F(1)}, "b")
    return mul(mul(qa, za), mul(qb, zb))


HISTORIES = tuple(history(z) for z in LABELS)
GRAM_ELEMENTS = tuple(tuple(mul(star(h), k) for k in HISTORIES) for h in HISTORIES)


def evaluate(values, a):
    if len(values) != 16:
        raise ValueError("Expected 16 functional coordinates")
    return sum((values[4 * i + j] * coefficient for (i, j), coefficient in a.items()), F(0))


def history_kernel(values):
    return tuple(tuple(evaluate(values, a) for a in row) for row in GRAM_ELEMENTS)


def coordinates_from_kernel(kernel):
    """Derive phi_D using the history-basis expansion and column sums."""
    if len(kernel) != 16 or any(len(row) != 16 for row in kernel):
        raise ValueError("Expected a 16 by 16 history kernel")
    columns = tuple(sum((row[z] for row in kernel), F(0)) for z in range(16))
    values = []
    for row, col in UNITS:
        ra, rb = divmod(row, 2)
        ca, cb = divmod(col, 2)
        values.append(
            sum(
                (
                    columns[n] * (s if ra != ca else 1) * (t if rb != cb else 1)
                    for n, (i, s, j, t) in enumerate(LABELS)
                    if i == ca and j == cb
                ),
                F(0),
            )
        )
    return tuple(values)


def compatible(kernel):
    """Check linear algebra compatibility only; NOT a positivity test."""
    return history_kernel(coordinates_from_kernel(kernel)) == tuple(tuple(r) for r in kernel)


def branch_coordinates(values, action, context, outcome):
    if outcome is None:
        # Formal impossible outcome: no normalization or committed successor.
        if action not in ("a", "b", "ab"):
            raise ValueError("Unknown action")
        return (F(0),) * 16
    p = projector(action, context, outcome)
    return tuple(evaluate(values, mul(mul(p, {ij: F(1)}), p)) / 3 for ij in UNITS)


def branch_kernel(kernel, action, context, outcome):
    if not compatible(kernel):
        raise ValueError("Outside the declared compatible linear domain")
    return history_kernel(
        branch_coordinates(coordinates_from_kernel(kernel), action, context, outcome)
    )


def mass(kernel):
    return sum((sum(row, F(0)) for row in kernel), F(0))


def trace(kernel):
    return sum((kernel[i][i] for i in range(len(kernel))), F(0))


def normalized_or_none(kernel):
    weight = mass(kernel)
    if weight == 0:
        # Reject, do not silently erase a nonzero zero-mass raw restriction.
        if any(value != 0 for row in kernel for value in row):
            raise ValueError("Nonzero zero-mass kernel is not a compression residual")
        return None
    return tuple(tuple(value / weight for value in row) for row in kernel)
