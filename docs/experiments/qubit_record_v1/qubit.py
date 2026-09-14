"""Exact ordinary-qubit fixture, with an explicit normalized C0 embedding.

Trace-one qubit states, Born probabilities, selective/nonselective Lüders
updates, and calibrated X/Y/Z/W measurement availability are ADOPTED model
premises. They are not derived from DET. W=(0,3/5,4/5) is fixed, not fitted.
The J2 bridge is a mathematical representation; it supplies no four-cell L_t
apparatus, physical preparation, or conversion of a terminal record to a state.

All numerical inputs are integers or fractions.Fraction, never floats. G is
an exact Gaussian rational with separate real/imaginary Fraction components.
Matrices are immutable row tuples. This module owns no records or randomness.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType

F = Fraction
ZERO = F(0)


def _rational(value: int | F) -> F:
    if type(value) is int:
        return F(value)
    if type(value) is F:
        return value
    raise TypeError("Use exact built-in integers or Fraction values, not booleans or floats")


@dataclass(frozen=True)
class Bloch:
    """One normalized qubit snapshot, not proof of preparation or reachability."""

    r: tuple[F, F, F]

    def __post_init__(self) -> None:
        if isinstance(self.r, (str, bytes)):
            raise TypeError("A Bloch vector must contain three exact real coordinates")
        values = tuple(_rational(value) for value in self.r)
        if len(values) != 3:
            raise ValueError("A Bloch vector has exactly three coordinates")
        if sum((value * value for value in values), F(0)) > 1:
            raise ValueError("A physical Bloch vector has squared norm at most one")
        object.__setattr__(self, "r", values)


AXES = MappingProxyType(
    {
        "X": (F(1), F(0), F(0)),
        "Y": (F(0), F(1), F(0)),
        "Z": (F(0), F(0), F(1)),
        "W": (F(0), F(3, 5), F(4, 5)),
    }
)


def _state(state: Bloch) -> Bloch:
    if type(state) is not Bloch:
        raise TypeError("Supply this fixture's exact Bloch state")
    return state


def _axis(setting: str) -> tuple[F, F, F]:
    if type(setting) is not str:
        raise TypeError("A setting must be a built-in string")
    if setting not in AXES:
        raise ValueError("Only the declared X, Y, Z and W settings are available")
    return AXES[setting]


def _outcome(outcome: int) -> int:
    if type(outcome) is not int:
        raise TypeError("An outcome must be the built-in integer +1 or -1")
    if outcome not in (-1, 1):
        raise ValueError("An outcome must be +1 or -1")
    return outcome


def _dot(left: tuple[F, F, F], right: tuple[F, F, F]) -> F:
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def plus_probability(state: Bloch, setting: str) -> F:
    """Adopted calibrated Born law for the +1 outcome, conditional on this state."""
    return (1 + _dot(_state(state).r, _axis(setting))) / 2


def outcome_probability(state: Bloch, setting: str, outcome: int) -> F:
    outcome = _outcome(outcome)
    probability = plus_probability(state, setting)
    return probability if outcome == 1 else 1 - probability


class ModelMismatch(ValueError):
    """An observed zero-probability outcome has no update in this model.

    The caller must retain the actual attempted acquisition and its outcome;
    this exception neither erases that record nor fabricates a new state.
    """


def selective_update(state: Bloch, setting: str, outcome: int) -> Bloch:
    """Adopted rank-one Lüders update, only on a selected positive branch."""
    probability = outcome_probability(state, setting, outcome)
    if probability == 0:
        raise ModelMismatch(
            f"Observed outcome {outcome:+d} at {setting} has probability zero; retain its record"
        )
    return Bloch(tuple(outcome * value for value in _axis(setting)))


def nonselective_update(state: Bloch, setting: str) -> Bloch:
    """Adopted unconditioned Lüders channel; never a rule for a missing outcome."""
    state, axis = _state(state), _axis(setting)
    expectation = _dot(state.r, axis)
    return Bloch(tuple(expectation * value for value in axis))


def trace_distance_squared(left: Bloch, right: Bloch) -> F:
    """Square of (1/2)||rho-left - rho-right||_1 = ||r-left - r-right||_2/2."""
    left, right = _state(left), _state(right)
    return sum(((a - b) ** 2 for a, b in zip(left.r, right.r, strict=True)), F(0)) / 4


@dataclass(frozen=True)
class G:
    """An exact Gaussian rational; neither binary complex nor float arithmetic."""

    real: F = ZERO
    imag: F = ZERO

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", _rational(self.real))
        object.__setattr__(self, "imag", _rational(self.imag))

    def conjugate(self) -> "G":
        return G(self.real, -self.imag)

    def __neg__(self) -> "G":
        return G(-self.real, -self.imag)

    def __add__(self, other: "G | int | F") -> "G":
        other = _gaussian(other)
        return G(self.real + other.real, self.imag + other.imag)

    def __radd__(self, other: "G | int | F") -> "G":
        return self + other

    def __sub__(self, other: "G | int | F") -> "G":
        return self + (-_gaussian(other))

    def __mul__(self, other: "G | int | F") -> "G":
        other = _gaussian(other)
        return G(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    def __rmul__(self, other: "G | int | F") -> "G":
        return self * other


Matrix = tuple[tuple[G, ...], ...]


def _gaussian(value: G | int | F) -> G:
    return value if type(value) is G else G(_rational(value))


def _matrix(rows: Iterable[Iterable[G | int | F]], size: int) -> Matrix:
    if isinstance(rows, (str, bytes)):
        raise TypeError("Supply exact matrix rows, not text")
    result = tuple(tuple(_gaussian(value) for value in row) for row in rows)
    if len(result) != size or any(len(row) != size for row in result):
        raise ValueError(f"The matrix must be exactly {size} by {size}")
    return result


def density(state: Bloch) -> Matrix:
    """rho=(I+r.sigma)/2, trace one; the upper Y entry is -i*r_y/2."""
    x, y, z = _state(state).r
    return (
        (G((1 + z) / 2), G(x / 2, -y / 2)),
        (G(x / 2, y / 2), G((1 - z) / 2)),
    )


def _density_bloch(rho: Matrix) -> Bloch:
    rho = _matrix(rho, 2)
    if rho[0][0].imag or rho[1][1].imag or rho[1][0] != rho[0][1].conjugate():
        raise ValueError("A density matrix must be Hermitian")
    if rho[0][0].real + rho[1][1].real != 1:
        raise ValueError("A density matrix must have trace one")
    return Bloch((2 * rho[0][1].real, -2 * rho[0][1].imag, rho[0][0].real - rho[1][1].real))


def J2(state: Bloch) -> Matrix:
    """J2(rho)=diag(rho^T/2, Z*rho^T*Z/2), with full four-label payload."""
    rho = density(state)
    zero = G()
    a = tuple(tuple(F(1, 2) * rho[j][i] for j in range(2)) for i in range(2))
    return (
        (a[0][0], a[0][1], zero, zero),
        (a[1][0], a[1][1], zero, zero),
        (zero, zero, a[0][0], -a[0][1]),
        (zero, zero, -a[1][0], a[1][1]),
    )


def phi(kernel: Iterable[Iterable[G | int | F]]) -> Matrix:
    """Inverse only on the entire normalized J2 image, never a silent projection.

    Every supplied entry is checked against the C0 image, including zero cross
    blocks and the Z-conjugate lower block. This does not certify preparation.
    """
    d = _matrix(kernel, 4)
    rho = tuple(tuple(2 * d[j][i] for j in range(2)) for i in range(2))
    state = _density_bloch(rho)
    if d != J2(state):
        raise ValueError(
            "The full kernel must equal a normalized J2 image; no payload is discarded"
        )
    return density(state)
