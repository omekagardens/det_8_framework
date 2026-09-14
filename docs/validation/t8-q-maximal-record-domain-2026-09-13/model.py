"""Exact helpers for the maximal fixed-partition recordability domain.

The construction uses supplied finite atoms and a supplied partition. It is a
linear-algebra witness, not a selection of physically available preparations,
apparatus operations, or a quantum/geometry reconstruction. Complex scalars
are Gaussian rationals: no floating-point tolerance enters the checks.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction

F = Fraction
ZERO_F = F(0)


def rational(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Use exact integers or Fractions, not floats or booleans")
    return F(value)


@dataclass(frozen=True, eq=False)
class G:
    """An immutable Gaussian rational with exact arithmetic."""

    real: F = ZERO_F
    imag: F = ZERO_F

    def __post_init__(self) -> None:
        object.__setattr__(self, "real", rational(self.real))
        object.__setattr__(self, "imag", rational(self.imag))

    def __add__(self, other: "G | int | F") -> "G":
        other = gaussian(other)
        return G(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self) -> "G":
        return G(-self.real, -self.imag)

    def __sub__(self, other: "G | int | F") -> "G":
        return self + -gaussian(other)

    def __rsub__(self, other: "G | int | F") -> "G":
        return gaussian(other) + -self

    def __mul__(self, other: "G | int | F") -> "G":
        other = gaussian(other)
        return G(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: "G | int | F") -> "G":
        other = gaussian(other)
        norm = other.norm_squared()
        if norm == 0:
            raise ZeroDivisionError("Cannot divide by the zero Gaussian rational")
        product = self * other.conjugate()
        return G(product.real / norm, product.imag / norm)

    def __rtruediv__(self, other: "G | int | F") -> "G":
        return gaussian(other) / self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, G):
            return self.real == other.real and self.imag == other.imag
        if not isinstance(other, bool) and isinstance(other, (int, F)):
            return self.imag == 0 and self.real == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.real) if self.imag == 0 else hash((self.real, self.imag))

    def conjugate(self) -> "G":
        return G(self.real, -self.imag)

    def norm_squared(self) -> F:
        return self.real * self.real + self.imag * self.imag


def gaussian(value: G | int | F) -> G:
    return value if isinstance(value, G) else G(rational(value))


Gaussian = G
Vector = tuple[G, ...]
Matrix = tuple[Vector, ...]
RealVector = tuple[F, ...]
RealMatrix = tuple[RealVector, ...]
I = G(0, 1)


def vector(values: Iterable[G | int | F]) -> Vector:
    result = tuple(gaussian(value) for value in values)
    if not result:
        raise ValueError("Vectors must be nonempty")
    return result


def matrix(rows: Iterable[Iterable[G | int | F]]) -> Matrix:
    result = tuple(vector(row) for row in rows)
    if not result or any(len(row) != len(result[0]) for row in result):
        raise ValueError("Matrices must be nonempty and rectangular")
    return result


def _dimension(n: int) -> int:
    if type(n) is not int or n <= 0:
        raise ValueError("Dimension must be a positive integer")
    return n


def zeros(rows: int, columns: int | None = None) -> Matrix:
    rows = _dimension(rows)
    columns = rows if columns is None else _dimension(columns)
    return matrix((0,) * columns for _ in range(rows))


def identity(n: int) -> Matrix:
    n = _dimension(n)
    return matrix(tuple(int(i == j) for j in range(n)) for i in range(n))


def dagger(d: Matrix) -> Matrix:
    d = matrix(d)
    return tuple(tuple(d[i][j].conjugate() for i in range(len(d))) for j in range(len(d[0])))


def add(*operators: Matrix) -> Matrix:
    if not operators:
        raise ValueError("Supply at least one matrix")
    operators = tuple(matrix(operator) for operator in operators)
    n, m = len(operators[0]), len(operators[0][0])
    if any(len(operator) != n or len(operator[0]) != m for operator in operators):
        raise ValueError("Matrix dimensions do not match")
    return tuple(
        tuple(sum((operator[i][j] for operator in operators), G()) for j in range(m))
        for i in range(n)
    )


def scale(coefficient: G | int | F, d: Matrix) -> Matrix:
    coefficient, d = gaussian(coefficient), matrix(d)
    return tuple(tuple(coefficient * entry for entry in row) for row in d)


def inner(left: Vector, right: Vector) -> G:
    left, right = vector(left), vector(right)
    return sum((a.conjugate() * b for a, b in zip(left, right, strict=True)), G())


def matvec(d: Matrix, x: Vector) -> Vector:
    d, x = matrix(d), vector(x)
    if len(d[0]) != len(x):
        raise ValueError("Matrix/vector dimensions do not match")
    return tuple(sum((a * b for a, b in zip(row, x, strict=True)), G()) for row in d)


def matmul(left: Matrix, right: Matrix) -> Matrix:
    left, right = matrix(left), matrix(right)
    if len(left[0]) != len(right):
        raise ValueError("Matrix dimensions do not match")
    return tuple(
        tuple(
            sum((left[i][k] * right[k][j] for k in range(len(right))), G())
            for j in range(len(right[0]))
        )
        for i in range(len(left))
    )


def outer(left: Vector, right: Vector | None = None) -> Matrix:
    left = vector(left)
    right = left if right is None else vector(right)
    return tuple(tuple(a * b.conjugate() for b in right) for a in left)


def is_hermitian(d: Matrix) -> bool:
    d = matrix(d)
    return len(d) == len(d[0]) and d == dagger(d)


def is_psd(d: Matrix) -> bool:
    """Exact Hermitian PSD decision by positive-pivot Schur complements.

    A negative diagonal excludes PSD. With no positive diagonal, a PSD matrix
    must be zero (its two-by-two principal minors force each off-diagonal to
    vanish). Otherwise a positive scalar pivot reduces PSD equivalently to
    PSD of its Schur complement. This terminates in the finite dimension.
    """
    d = matrix(d)
    if not is_hermitian(d):
        return False
    while d:
        if any(d[i][i].real < 0 for i in range(len(d))):
            return False
        pivots = tuple(i for i in range(len(d)) if d[i][i].real > 0)
        if not pivots:
            return all(entry == 0 for row in d for entry in row)
        pivot = pivots[0]
        remaining = tuple(i for i in range(len(d)) if i != pivot)
        d = tuple(
            tuple(d[i][j] - d[i][pivot] * d[pivot][j] / d[pivot][pivot] for j in remaining)
            for i in remaining
        )
    return True


@dataclass(frozen=True)
class Partition:
    cells: tuple[tuple[int, ...], ...]
    n: int | None = None

    def __post_init__(self) -> None:
        cells = tuple(tuple(cell) for cell in self.cells)
        if not cells or any(not cell for cell in cells):
            raise ValueError("A partition consists of nonempty cells")
        atoms = tuple(atom for cell in cells for atom in cell)
        if any(type(atom) is not int or atom < 0 for atom in atoms):
            raise ValueError("Atom labels must be nonnegative integers")
        n = max(atoms) + 1 if self.n is None else _dimension(self.n)
        if len(atoms) != n or set(atoms) != set(range(n)):
            raise ValueError("Cells must cover 0,...,n-1 exactly once")
        object.__setattr__(self, "cells", cells)
        object.__setattr__(self, "n", n)

    @property
    def k(self) -> int:
        return len(self.cells)


def _partition(partition: Partition) -> Partition:
    if not isinstance(partition, Partition):
        raise TypeError("Use a validated Partition")
    return partition


def indicator_vectors(partition: Partition) -> tuple[Vector, ...]:
    partition = _partition(partition)
    return tuple(vector(int(i in cell) for i in range(partition.n)) for cell in partition.cells)


def visible_vectors(partition: Partition) -> tuple[Vector, ...]:
    """Dual visible vectors v_r=b_r/|A_r| satisfy b_s^* v_r=delta_sr."""
    partition = _partition(partition)
    return tuple(
        tuple(value / len(cell) for value in b)
        for cell, b in zip(partition.cells, indicator_vectors(partition), strict=True)
    )


def dark_basis(partition: Partition) -> tuple[Vector, ...]:
    """A basis of the joint indicator annihilator, not an orthonormal basis."""
    partition = _partition(partition)
    return tuple(
        vector(int(i == atom) - int(i == cell[0]) for i in range(partition.n))
        for cell in partition.cells
        for atom in cell[1:]
    )


def _hermitian_pair(left: Vector, right: Vector) -> tuple[Matrix, Matrix]:
    forward, backward = outer(left, right), outer(right, left)
    return add(forward, backward), add(scale(I, forward), scale(-I, backward))


def span_basis(partition: Partition) -> tuple[Matrix, ...]:
    """Real basis: visible diagonal, dark Hermitian, and visible-dark cross terms."""
    visible, dark = visible_vectors(partition), dark_basis(partition)
    result = [outer(v) for v in visible]
    result.extend(outer(h) for h in dark)
    for i, h in enumerate(dark):
        for other in dark[i + 1 :]:
            result.extend(_hermitian_pair(h, other))
    for v in visible:
        for h in dark:
            result.extend(_hermitian_pair(v, h))
    return tuple(result)


def span_dimension(partition: Partition) -> int:
    partition = _partition(partition)
    return partition.n * partition.n - partition.k * (partition.k - 1)


def in_span(d: Matrix, partition: Partition) -> bool:
    """Membership in the real Hermitian span, without asserting positivity."""
    d, partition = matrix(d), _partition(partition)
    if len(d) != partition.n or len(d[0]) != partition.n or not is_hermitian(d):
        return False
    indicators = indicator_vectors(partition)
    return all(
        inner(b, matvec(d, other)) == 0
        for r, b in enumerate(indicators)
        for s, other in enumerate(indicators)
        if r != s
    )


def q(d: Matrix, partition: Partition) -> RealVector:
    """Cell weights, on the full Hermitian space; domain membership is separate."""
    d, partition = matrix(d), _partition(partition)
    if len(d) != partition.n or len(d[0]) != partition.n or not is_hermitian(d):
        raise ValueError("Use a Hermitian matrix on the supplied atom space")
    return tuple(inner(b, matvec(d, b)).real for b in indicator_vectors(partition))


def mass(d: Matrix) -> F:
    """Total-entry mass e^* d e, not trace; may be signed off the positive cone."""
    d = matrix(d)
    if not is_hermitian(d):
        raise ValueError("Mass here is defined on Hermitian matrices")
    e = vector(1 for _ in d)
    return inner(e, matvec(d, e)).real


def section(weights: Iterable[int | F], partition: Partition) -> Matrix:
    """Linear section sum_r weights_r v_r v_r^*, positive for nonnegative weights."""
    partition = _partition(partition)
    weights = tuple(rational(weight) for weight in weights)
    if len(weights) != partition.k:
        raise ValueError("Supply exactly one real weight per cell")
    return add(
        zeros(partition.n),
        *(
            scale(weight, outer(v))
            for weight, v in zip(weights, visible_vectors(partition), strict=True)
        ),
    )


def kernel(d: Matrix, partition: Partition, *, normalized: bool = False) -> Matrix:
    """Require the maximal PSD exact-recordability cone; reject, never repair."""
    d = matrix(d)
    if not in_span(d, partition) or not is_psd(d):
        raise ValueError("Kernel must be PSD and exactly recordable for the supplied partition")
    if normalized and mass(d) != 1:
        raise ValueError("Normalized kernels must have total-entry mass one")
    return d


def substochastic(
    rows: Iterable[Iterable[int | F]], source: Partition, target: Partition
) -> RealMatrix:
    """Validate a target-k by source-k nonnegative matrix with column sums <=1."""
    source, target = _partition(source), _partition(target)
    result = tuple(tuple(rational(value) for value in row) for row in rows)
    if len(result) != target.k or any(len(row) != source.k for row in result):
        raise ValueError("Transition dimensions must match target and source cell counts")
    if any(value < 0 for row in result for value in row):
        raise ValueError("Transition entries must be nonnegative")
    if any(sum((row[j] for row in result), F(0)) > 1 for j in range(source.k)):
        raise ValueError("Transition column sums cannot exceed one")
    return result


def measure_prepare(
    d: Matrix,
    source: Partition,
    target: Partition,
    transition: Iterable[Iterable[int | F]],
) -> Matrix:
    """T_A=section_target A q_source on the entire real recordability span.

    The linear extension accepts indefinite span elements. Positivity and mass
    nonincrease hold on its PSD cone, not on arbitrary signed inputs. The map
    is supplied, and its resetting of dark/cross residuals is not forced by DET.
    """
    d = matrix(d)
    if not in_span(d, source):
        raise ValueError("Input must belong to the source recordability span")
    transition = substochastic(transition, source, target)
    weights = q(d, source)
    output = tuple(
        sum((entry * weight for entry, weight in zip(row, weights, strict=True)), F(0))
        for row in transition
    )
    return section(output, target)


def bounded_effect(d: Matrix, partition: Partition, coefficients: Iterable[int | F]) -> F:
    """f_c(d)=c.q(d); 0<=f_c<=mass on the PSD cone when each 0<=c_r<=1."""
    d = matrix(d)
    if not in_span(d, partition):
        raise ValueError("Input must belong to the recordability span")
    coefficients = tuple(rational(coefficient) for coefficient in coefficients)
    if len(coefficients) != partition.k or any(c < 0 or c > 1 for c in coefficients):
        raise ValueError("Supply one coefficient in [0,1] per cell")
    return sum(
        (
            coefficient * weight
            for coefficient, weight in zip(coefficients, q(d, partition), strict=True)
        ),
        F(0),
    )
