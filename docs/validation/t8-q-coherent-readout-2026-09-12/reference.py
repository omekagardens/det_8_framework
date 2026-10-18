"""Independent downstream matrix representation of the candidate algebra.

This module is a comparison implementation, not an upstream Hilbert-space
assumption or a derivation of the candidate law.  It imports no primary
implementation.  All structural coefficients are exact ``Fraction`` values;
input coordinates may themselves be exact complex-like scalars.

The input coordinates are row-major phi(e_ij), NOT density-matrix entries:
rho[j][i] = phi(e_ij).  The index bits are big-endian (port a, port b).
"""

from fractions import Fraction

ZERO = Fraction(0)
ONE = Fraction(1)
HALF = Fraction(1, 2)
THIRD = Fraction(1, 3)

HISTORY_LABELS = tuple(
    (i, s, j, t) for i in (0, 1) for s in (1, -1) for j in (0, 1) for t in (1, -1)
)


def _density(values):
    """Convert functional coordinates using the trace-pairing transpose."""
    if len(values) != 16:
        raise ValueError("expected 16 row-major phi(e_ij) coordinates")
    return tuple(tuple(values[4 * j + i] for j in range(4)) for i in range(4))


def _linear_sum(terms, zero):
    """Only require scalar addition and right multiplication by Fraction."""
    result = zero
    for value, coefficient in terms:
        if coefficient:
            result = result + value * coefficient
    return result


def _projector(action, context, outcome):
    if action not in ("a", "b", "ab"):
        raise ValueError("action must be a, b or ab")
    if context not in (0, 1) or outcome not in (0, 1):
        raise ValueError("context and outcome must be binary")
    mask = {"a": 2, "b": 1, "ab": 3}[action]
    sign = ONE if outcome == 0 else -ONE
    rows = []
    for row in range(4):
        entries = []
        for column in range(4):
            identity = ONE if row == column else ZERO
            if context == 0:
                involution = ONE if row == (column ^ mask) else ZERO
            elif row == column:
                parity = (column & mask).bit_count() % 2
                involution = ONE if parity == 0 else -ONE
            else:
                involution = ZERO
            entries.append((identity + sign * involution) * HALF)
        rows.append(tuple(entries))
    return tuple(rows)


def branch_coordinates(values, action, context, outcome):
    """Return unnormalized phi' coordinates for P rho P / 3.

    The whole declared branch remains defined at zero probability.  This
    routine deliberately never normalizes a branch or samples a birth.
    """
    rho = _density(values)
    projector = _projector(action, context, outcome)
    zero = values[0] * ZERO
    output_density = tuple(
        tuple(
            _linear_sum(
                (
                    (
                        rho[k][ell],
                        projector[i][k] * projector[ell][j] * THIRD,
                    )
                    for k in range(4)
                    for ell in range(4)
                ),
                zero,
            )
            for j in range(4)
        )
        for i in range(4)
    )
    return tuple(output_density[j][i] for i in range(4) for j in range(4))


def _multiply(left, right):
    size = len(left)
    return tuple(
        tuple(sum((left[i][k] * right[k][j] for k in range(size)), ZERO) for j in range(size))
        for i in range(size)
    )


def _transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(len(matrix))) for i in range(len(matrix)))


def _local_history(i, sign):
    """The conventional real matrix for h_(i,sign) = q_sign z_i."""
    projector = ((HALF, sign * HALF), (sign * HALF, HALF))
    return tuple(
        tuple(projector[row][column] if column == i else ZERO for column in range(2))
        for row in range(2)
    )


def _tensor(left, right):
    return tuple(
        tuple(left[row // 2][column // 2] * right[row % 2][column % 2] for column in range(4))
        for row in range(4)
    )


def history_kernel(values):
    """Return D(z,w) = Tr(rho h_z^dagger h_w), in HISTORY_LABELS order.

    The histories have real coefficients, so their conjugate transpose is
    their transpose even when the functional coordinates are complex.
    """
    rho = _density(values)
    zero = values[0] * ZERO
    histories = tuple(
        _tensor(_local_history(i, sign), _local_history(j, other_sign))
        for i, sign, j, other_sign in HISTORY_LABELS
    )
    output = []
    for left in histories:
        row = []
        for right in histories:
            product = _multiply(_transpose(left), right)
            row.append(
                _linear_sum(
                    ((rho[i][j], product[j][i]) for i in range(4) for j in range(4)),
                    zero,
                )
            )
        output.append(tuple(row))
    return tuple(output)
