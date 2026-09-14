"""Exact conditional observation-stability audit on the fixed t=3/5 fixture.

The sole tilted terminal read, six named commands, literal cuts, full native
kernels and record grammar are copied independently without new availability.
A supplied positive normalized candidate may witness feasibility within exact
three-setting total-variation budgets. Failure of that candidate is only
inconclusive; no fitting, infeasibility decision or preparation is performed.
Certificates retain complete supplied data, current candidate payload and any
declared context/history/pending word as audit data, not available observations.
They are neither source states nor terminal outputs and admit no continuation.
The exact reconstruction contract remains strict even when noisy tables have
a budget-feasible witness. No time, unknown generator, full QM or gravity claim.
"""

from collections.abc import Iterable
from dataclasses import dataclass, field
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


def transpose(d: Matrix) -> Matrix:
    d = matrix(d)
    return tuple(tuple(d[i][j] for i in range(len(d))) for j in range(len(d[0])))


def _two(d: Matrix) -> Matrix:
    d = matrix(d)
    if len(d) != 2 or len(d[0]) != 2:
        raise ValueError("A qubit block must be two by two")
    return d


def _hermitian(d: Matrix, n: int) -> Matrix:
    d = matrix(d)
    if len(d) != n or len(d[0]) != n or not is_hermitian(d):
        raise ValueError("Matrix must be Hermitian with the declared full dimension")
    return d


def trace(d: Matrix) -> G:
    d = matrix(d)
    if len(d) != len(d[0]):
        raise ValueError("Trace requires a square matrix")
    return sum((d[i][i] for i in range(len(d))), G())


def tensor(left: Matrix, right: Matrix) -> Matrix:
    left, right = matrix(left), matrix(right)
    return tuple(
        tuple(a * b for a in left_row for b in right_row)
        for left_row in left
        for right_row in right
    )


def _bit(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError("A binary label must be a built-in integer 0 or 1")
    return value


def _t(value: int | F) -> F:
    value = rational(value)
    if abs(value) > 1:
        raise ValueError("The fixed reference polarization must lie in [-1,1]")
    return value


def _name(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("Retained names and labels must be nonempty strings")
    return value


def index_native(a: int, i: int, b: int, j: int) -> int:
    a, i, b, j = (_bit(value) for value in (a, i, b, j))
    return 8 * a + 4 * i + 2 * b + j


def index_joint(a: int, b: int, i: int, j: int) -> int:
    a, b, i, j = (_bit(value) for value in (a, b, i, j))
    return 8 * a + 4 * b + 2 * i + j


Z = matrix(((1, 0), (0, -1)))
H0 = matrix(((1, 1), (1, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
U0 = matmul(tensor(identity(2), H0), CNOT)
JOINT_CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))
CROSS_PAIRS = tuple(
    (left, right) for n, left in enumerate(JOINT_CELLS) for right in JOINT_CELLS[n + 1 :]
)
NATIVE_TO_GROUPED = tuple(
    index_joint(a, b, i, j) for a in (0, 1) for i in (0, 1) for b in (0, 1) for j in (0, 1)
)
SHARED_COUPLER = "shared_CNOT_H2"
FRAME = "fixed_shared_image"
CONTROLLER = "weighted_command_cut_terminal_read_controller"
NOMINAL_CUT = "literal_joint_cell_cut"
INTERIOR_DOMAIN = "interior_filtered_L_t_with_terminal_read"
FIXED_T = F(3, 5)
X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, -I), (I, 0)))
COMMANDS = ("A", "B", "AB", "A_inv", "B_inv", "AB_inv")


def _cell(outcome: tuple[int, int]) -> tuple[int, int]:
    if not isinstance(outcome, tuple) or len(outcome) != 2:
        raise ValueError("A fine joint outcome is the complete tuple (a,b)")
    return _bit(outcome[0]), _bit(outcome[1])


def cell_indices(outcome: tuple[int, int]) -> tuple[int, ...]:
    a, b = _cell(outcome)
    return tuple(index_native(a, i, b, j) for i in (0, 1) for j in (0, 1))


def to_untwisted(d: Matrix) -> Matrix:
    d = _hermitian(d, 16)
    inverse = tuple(NATIVE_TO_GROUPED.index(i) for i in range(16))
    signs = tuple(
        (-1) ** (a * i + b * j) for a in (0, 1) for i in (0, 1) for b in (0, 1) for j in (0, 1)
    )
    return matrix(tuple(signs[i] * d[i][j] * signs[j] for j in inverse) for i in inverse)


def from_untwisted(d: Matrix) -> Matrix:
    d = _hermitian(d, 16)
    signs = tuple(
        (-1) ** (a * i + b * j) for a in (0, 1) for i in (0, 1) for b in (0, 1) for j in (0, 1)
    )
    return matrix(
        tuple(
            signs[i] * d[NATIVE_TO_GROUPED[i]][NATIVE_TO_GROUPED[j]] * signs[j] for j in range(16)
        )
        for i in range(16)
    )


def local_from(rho: Matrix, c: G | int | F = 0, *, normalized: bool = False) -> Matrix:
    """Construct the full old local D(rho^T/2,c), without dropping complex c."""
    rho, c = _hermitian(rho, 2), gaussian(c)
    a = scale(F(1, 2), transpose(rho))
    f, b = scale(c, Z), matmul(matmul(Z, a), Z)
    adjoint = dagger(f)
    d = matrix(tuple(a[i]) + tuple(f[i]) for i in range(2)) + matrix(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )
    if not is_psd(d):
        raise ValueError("Full local kernel must be PSD, including its complex c blocks")
    if normalized and trace(rho) != 1:
        raise ValueError("Normalized local input requires trace(rho)=1")
    return d


def decompose_local(d: Matrix, *, normalized: bool = False) -> tuple[Matrix, G]:
    d = _hermitian(d, 4)
    a = matrix(row[:2] for row in d[:2])
    f = matrix(row[2:] for row in d[:2])
    b = matrix(row[2:] for row in d[2:])
    c = f[0][0]
    if f != scale(c, Z) or b != matmul(matmul(Z, a), Z) or not is_psd(d):
        raise ValueError("Input must retain a full PSD local D(A,c) kernel")
    rho = scale(2, transpose(a))
    if normalized and trace(rho) != 1:
        raise ValueError("Normalized local input requires total-entry mass one")
    return rho, c


def reference_rho(t: int | F) -> Matrix:
    return scale(F(1, 2), add(identity(2), scale(_t(t), Z)))


def raw_cross(d: Matrix, left: tuple[int, int], right: tuple[int, int]) -> G:
    d = _hermitian(d, 16)
    return sum((d[i][j] for i in cell_indices(left) for j in cell_indices(right)), G())


def raw_crossforms(d: Matrix) -> tuple[G, ...]:
    d = _hermitian(d, 16)
    return tuple(raw_cross(d, left, right) for left, right in CROSS_PAIRS)


def raw_cell_weights(d: Matrix) -> RealVector:
    d = _hermitian(d, 16)
    return tuple(raw_cross(d, cell, cell).real for cell in JOINT_CELLS)


def raw_mass(d: Matrix) -> F:
    """Native total-entry mass; generally NOT ordinary trace on the enlarged L_t."""
    d = _hermitian(d, 16)
    return sum((entry.real for row in d for entry in row), F(0))


def raw_cell_cut(d: Matrix, outcome: tuple[int, int]) -> Matrix:
    """Raw full-payload cut; reusable source typing requires explicit L_t validation."""
    d = _hermitian(d, 16)
    indices = cell_indices(outcome)
    return matrix(
        tuple(d[i][j] if i in indices and j in indices else 0 for j in range(16)) for i in range(16)
    )


def pulled_effect(t: int | F, outcome: tuple[int, int]) -> Matrix:
    _, b = _cell(outcome)
    return scale(F(1, 4), add(identity(2), scale((-1) ** b * _t(t), Z)))


def _rhos(rhos: Iterable[Matrix]) -> tuple[Matrix, ...]:
    rhos = tuple(_hermitian(rho, 2) for rho in rhos)
    if len(rhos) != 4:
        raise ValueError("L_t retains four independent Hermitian blocks in JOINT_CELLS order")
    return rhos


def _system_block(rho: Matrix, t: F) -> Matrix:
    a, b = scale(F(1, 2), transpose(rho)), scale(F(1, 2), reference_rho(t))
    return scale(F(1, 2), matmul(matmul(U0, tensor(a, b)), dagger(U0)))


def image_span(rhos: Iterable[Matrix], t: int | F) -> Matrix:
    """The signed L_t map: retwist diag(M_t(rho00),...,M_t(rho11))."""
    rhos, t = _rhos(rhos), _t(t)
    blocks = tuple(_system_block(rho, t) for rho in rhos)
    untwisted = matrix(
        tuple(blocks[i // 4][i % 4][j % 4] if i // 4 == j // 4 else 0 for j in range(16))
        for i in range(16)
    )
    return from_untwisted(untwisted)


def image(rhos: Iterable[Matrix], t: int | F, *, normalized: bool = False) -> Matrix:
    rhos = _rhos(rhos)
    if any(not is_psd(rho) for rho in rhos):
        raise ValueError("Each independent L_t block must be PSD")
    d = image_span(rhos, t)
    if normalized and raw_mass(d) != 1:
        raise ValueError("Normalize L_t by native cell-effect mass, not the sum of block traces")
    return d


def inverse_span(d: Matrix, t: int | F) -> tuple[Matrix, ...]:
    """Recover four blocks and reconstruct ALL raw entries, including off-cell zeros.

    Partial tracing uses trace(B_t)=1/2, so this inverse remains exact at t=0
    and t=+/-1. It is not a quotient projection that silently admits outsiders.
    """
    d, t = _hermitian(d, 16), _t(t)
    untwisted = to_untwisted(d)
    rhos = []
    for cell in range(4):
        start = 4 * cell
        block = matrix(row[start : start + 4] for row in untwisted[start : start + 4])
        before = scale(F(1, 2), matmul(matmul(dagger(U0), block), U0))
        partial = matrix(
            tuple(sum((before[2 * i + j][2 * k + j] for j in (0, 1)), G()) for k in (0, 1))
            for i in (0, 1)
        )
        rhos.append(scale(4, transpose(partial)))
    rhos = tuple(rhos)
    if image_span(rhos, t) != d:
        raise ValueError("Raw matrix is outside the exact full native L_t image")
    return rhos


def inverse_image(d: Matrix, t: int | F, *, normalized: bool = False) -> tuple[Matrix, ...]:
    d = matrix(d)
    rhos = inverse_span(d, t)
    if any(not is_psd(rho) for rho in rhos):
        raise ValueError("Every recovered L_t block must belong to its PSD cone")
    if normalized and raw_mass(d) != 1:
        raise ValueError("A normalized L_t source has native mass one, not raw trace one")
    return rhos


def image_kernel(d: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    d = matrix(d)
    inverse_image(d, t, normalized=normalized)
    return d


completion_span = image_span
completion_inverse = inverse_span


def k_image_span(rho: Matrix, t: int | F) -> Matrix:
    """Algebraic embedding of the earlier equal-block K_t subset, not a source adapter."""
    rho = _hermitian(rho, 2)
    return image_span((rho,) * 4, t)


def k_image(rho: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    rho = _hermitian(rho, 2)
    return image((rho,) * 4, t, normalized=normalized)


def inverse_k_span(d: Matrix, t: int | F) -> Matrix:
    """Diagnostic old-subset check; the new State requires the explicit enlarged L_t tag."""
    rhos = inverse_span(d, t)
    if any(rho != rhos[0] for rho in rhos[1:]):
        raise ValueError("Kernel is in the enlarged image but not its equal-block K_t subset")
    return rhos[0]


def k_from_local(d: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    rho, c = decompose_local(d, normalized=normalized)
    if c != 0:
        raise ValueError("The declared initial K_t subset requires c=0; nonzero c is not erased")
    return k_image(rho, t, normalized=normalized)


def quotient_on_span(d: Matrix, t: int | F) -> RealVector:
    """Old cut/command summary only; the new calibrated terminal read need not descend."""
    d = matrix(d)
    inverse_span(d, t)
    return raw_cell_weights(d)


def quotient(d: Matrix, t: int | F) -> RealVector:
    d = image_kernel(d, t)
    return quotient_on_span(d, t)


def _weights(weights: Iterable[int | F]) -> RealVector:
    weights = tuple(rational(weight) for weight in weights)
    if len(weights) != 4:
        raise ValueError("Retain exactly four weights in JOINT_CELLS order")
    return weights


def maximizing_rho(t: int | F, outcome: tuple[int, int]) -> Matrix:
    t, (_, b) = _t(t), _cell(outcome)
    if t == 0:
        return scale(F(1, 2), identity(2))
    alignment = 1 if (-1) ** b * t > 0 else -1
    return scale(F(1, 2), add(identity(2), scale(alignment, Z)))


def weight_section_span(weights: Iterable[int | F], t: int | F) -> Matrix:
    """Linear right inverse using maximal-effect states; not a physical reset operation."""
    weights, t = _weights(weights), _t(t)
    maximum = (1 + abs(t)) / 4
    rhos = tuple(
        scale(weight / maximum, maximizing_rho(t, outcome))
        for weight, outcome in zip(weights, JOINT_CELLS, strict=True)
    )
    return image_span(rhos, t)


def weight_section(weights: Iterable[int | F], t: int | F, *, normalized: bool = False) -> Matrix:
    """Positive algebraic section; existence does not authorize preparation or erasure."""
    weights = _weights(weights)
    if any(weight < 0 for weight in weights):
        raise ValueError("The positive weight section requires nonnegative weights")
    if normalized and sum(weights, F(0)) != 1:
        raise ValueError("Normalized record weights sum to one")
    return weight_section_span(weights, t)


def weight_cut(weights: Iterable[int | F], outcome: tuple[int, int]) -> RealVector:
    weights, outcome = _weights(weights), _cell(outcome)
    return tuple(
        weight if cell == outcome else F(0)
        for weight, cell in zip(weights, JOINT_CELLS, strict=True)
    )


def branch_on_span(d: Matrix, t: int | F, outcome: tuple[int, int]) -> Matrix:
    """Full literal cut, retaining nonzero zero-mass outputs for inspection."""
    d = matrix(d)
    inverse_span(d, t)
    return raw_cell_cut(d, _cell(outcome))


def branch(d: Matrix, t: int | F, outcome: tuple[int, int]) -> Matrix:
    d = image_kernel(d, t)
    return branch_on_span(d, t, outcome)


def fine_effect_on_span(d: Matrix, t: int | F, outcome: tuple[int, int]) -> F:
    d = matrix(d)
    inverse_span(d, t)
    outcome = _cell(outcome)
    return raw_cross(d, outcome, outcome).real


def b_effect_on_span(d: Matrix, t: int | F, b: int) -> F:
    d, b = matrix(d), _bit(b)
    inverse_span(d, t)
    return sum((raw_cross(d, (a, b), (a, b)).real for a in (0, 1)), F(0))


def dominated_effect_matrices(effects: Iterable[Matrix], t: int | F) -> tuple[Matrix, ...]:
    """Algebraic test of 0<=F_ab<=E_ab, not a catalogue of physical readouts."""
    effects, t = _rhos(effects), _t(t)
    for effect_matrix, outcome in zip(effects, JOINT_CELLS, strict=True):
        if not is_psd(effect_matrix) or not is_psd(
            add(pulled_effect(t, outcome), scale(-1, effect_matrix))
        ):
            raise ValueError("Each diagnostic effect must satisfy 0<=F_ab<=E_ab")
    return effects


def dominated_effect_on_span(d: Matrix, t: int | F, effects: Iterable[Matrix]) -> F:
    """Signed linear evaluation; the bound 0<=f<=mass applies on positive L_t."""
    rhos = inverse_span(d, t)
    effects = dominated_effect_matrices(effects, t)
    value = sum(
        (
            trace(matmul(effect_matrix, rho))
            for effect_matrix, rho in zip(effects, rhos, strict=True)
        ),
        G(),
    )
    if value.imag != 0:
        raise ValueError("Hermitian diagnostic effect evaluation must be real")
    return value.real


def dominated_effect(d: Matrix, t: int | F, effects: Iterable[Matrix]) -> F:
    d = image_kernel(d, t)
    return dominated_effect_on_span(d, t, effects)


def _fixture_t(t: int | F) -> F:
    t = _t(t)
    if t != FIXED_T:
        raise ValueError("The executable faithful-filter fixture is exactly the interior t=3/5")
    return t


def _unitary(unitary: Matrix) -> Matrix:
    unitary = _two(unitary)
    if matmul(dagger(unitary), unitary) != identity(2) or matmul(
        unitary, dagger(unitary)
    ) != identity(2):
        raise ValueError(
            "The algebraic unitary must satisfy both exact Gaussian-rational identities"
        )
    return unitary


def block_filter(outcome: tuple[int, int], t: int | F = FIXED_T) -> Matrix:
    """Rational D with E=D^2/10; no approximate square root or endpoint inverse."""
    _fixture_t(t)
    _, b = _cell(outcome)
    return matrix(((2, 0), (0, 1))) if b == 0 else matrix(((1, 0), (0, 2)))


def inverse_filter(outcome: tuple[int, int], t: int | F = FIXED_T) -> Matrix:
    _fixture_t(t)
    _, b = _cell(outcome)
    return matrix(((F(1, 2), 0), (0, 1))) if b == 0 else matrix(((1, 0), (0, F(1, 2))))


def weighted_unitary(unitary: Matrix, outcome: tuple[int, int], t: int | F = FIXED_T) -> Matrix:
    """Algebraic V=D^-1 U D; supplying U here does not register a physical command."""
    unitary = _unitary(unitary)
    return matmul(matmul(inverse_filter(outcome, t), unitary), block_filter(outcome, t))


def weighted_action_on_span(d: Matrix, t: int | F, unitaries: Iterable[Matrix]) -> Matrix:
    """Per-block algebraic congruence diagnostic on the entire signed image span."""
    t = _fixture_t(t)
    rhos = inverse_span(d, t)
    unitaries = tuple(_unitary(unitary) for unitary in unitaries)
    if len(unitaries) != 4:
        raise ValueError("Supply one exact algebraic unitary per retained cell")
    outputs = []
    for rho, unitary, outcome in zip(rhos, unitaries, JOINT_CELLS, strict=True):
        v = weighted_unitary(unitary, outcome, t)
        outputs.append(matmul(matmul(v, rho), dagger(v)))
    return image_span(outputs, t)


def weighted_action(d: Matrix, t: int | F, unitaries: Iterable[Matrix]) -> Matrix:
    """Positive diagnostic counterpart; not an enlargement of the named catalogue."""
    t = _fixture_t(t)
    d = image_kernel(d, t)
    return weighted_action_on_span(d, t, unitaries)


def command_unitary(name: str) -> Matrix:
    """Named group elements, not an elapsed-time parameterization."""
    parameters = {
        "A": (F(3, 5), F(4, 5)),
        "B": (F(5, 13), F(12, 13)),
        "AB": (F(-33, 65), F(56, 65)),
        "A_inv": (F(3, 5), F(-4, 5)),
        "B_inv": (F(5, 13), F(-12, 13)),
        "AB_inv": (F(-33, 65), F(-56, 65)),
    }
    if name not in COMMANDS:
        raise ValueError("Command is outside the fixed named rational group-element catalogue")
    c, s = parameters[name]
    return add(scale(c, identity(2)), scale(-I * s, X))


def command_on_span(d: Matrix, t: int | F, name: str) -> Matrix:
    unitary = command_unitary(name)
    return weighted_action_on_span(d, t, (unitary,) * 4)


def command(d: Matrix, t: int | F, name: str) -> Matrix:
    t = _fixture_t(t)
    d = image_kernel(d, t)
    return command_on_span(d, t, name)


def _command_word(names: Iterable[str]) -> tuple[str, ...]:
    if isinstance(names, str):
        raise TypeError("Supply an ordered sequence of complete nominal command labels")
    names = tuple(names)
    if any(name not in COMMANDS for name in names):
        raise ValueError("Pending word contains an unregistered primary command")
    return names


@dataclass(frozen=True)
class InputRecord:
    event_id: int
    action: str
    outcome: str
    settings: tuple[str, ...] = ()
    payload: tuple[tuple[str, str], ...] = ()
    precursor: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("Input event ids must be nonnegative built-in integers")
        _name(self.action)
        _name(self.outcome)
        if isinstance(self.settings, str):
            raise TypeError("Retain complete input setting labels, not a single string")
        settings = tuple(_name(setting) for setting in self.settings)
        payload = tuple(tuple(item) for item in self.payload)
        if any(
            len(item) != 2 or any(not isinstance(value, str) for value in item) for item in payload
        ):
            raise ValueError("Input payload consists of immutable string key/value pairs")
        precursor = tuple(self.precursor)
        if any(
            type(event) is not int or event < 0 or event >= self.event_id for event in precursor
        ):
            raise ValueError(
                "Input precursors must be built-in ids from the earlier same-origin prefix"
            )
        if len(set(precursor)) != len(precursor):
            raise ValueError("An input precursor cannot repeat an event")
        object.__setattr__(self, "settings", settings)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "precursor", precursor)


def input_history(records: Iterable[InputRecord]) -> tuple[InputRecord, ...]:
    records = tuple(records)
    for i, record in enumerate(records):
        if not isinstance(record, InputRecord) or record.event_id != i:
            raise ValueError(
                "Each separate input prefix uses complete records with contiguous local ids"
            )
    return records


@dataclass(frozen=True)
class LocalInput:
    residual: Matrix
    origin: str = "local"
    records: tuple[InputRecord, ...] = ()

    def __post_init__(self) -> None:
        _name(self.origin)
        d = matrix(self.residual)
        _, c = decompose_local(d, normalized=True)
        if c != 0:
            raise ValueError(
                "The declared initial K_t subset accepts only explicit c=0 local inputs"
            )
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", input_history(self.records))


@dataclass(frozen=True)
class ReferenceInput:
    t: F
    origin: str = "reference"
    records: tuple[InputRecord, ...] = ()
    orientation: str = "Z"
    residual: Matrix = field(init=False)

    def __post_init__(self) -> None:
        t = _t(self.t)
        _name(self.origin)
        if self.orientation != "Z":
            raise ValueError("The initial reference has the fixed declared Z orientation")
        object.__setattr__(self, "t", t)
        object.__setattr__(self, "records", input_history(self.records))
        object.__setattr__(self, "residual", local_from(reference_rho(t), normalized=True))


@dataclass(frozen=True)
class Independence:
    """Named initial-preparation premise; distinct labels do not prove independence."""

    origins: tuple[str, str]

    def __post_init__(self) -> None:
        if isinstance(self.origins, str):
            raise TypeError("Declare the two distinct initial preparation origins explicitly")
        origins = tuple(self.origins)
        if len(origins) != 2 or origins[0] == origins[1]:
            raise ValueError("Initial independence names exactly two distinct origins")
        for origin in origins:
            _name(origin)
        object.__setattr__(self, "origins", origins)


@dataclass(frozen=True)
class Context:
    """Initial origins and the explicitly enlarged command/cut/terminal-read context.

    Keeping the original reference/input objects is provenance, not a claim
    that each later cut prepares them again or applies the shared gate anew.
    """

    local: LocalInput
    reference: ReferenceInput
    independence: Independence
    terminal_read: "TerminalReadPremise"
    joint_origin: str = "joint"
    coupler: str = SHARED_COUPLER
    frame: str = FRAME
    controller: str = CONTROLLER
    setting_id: str = NOMINAL_CUT
    permutation: tuple[int, ...] = NATIVE_TO_GROUPED

    def __post_init__(self) -> None:
        if not isinstance(self.local, LocalInput) or not isinstance(self.reference, ReferenceInput):
            raise TypeError("Retain both complete separately typed initial inputs")
        _fixture_t(self.reference.t)
        if not isinstance(self.terminal_read, TerminalReadPremise):
            raise TypeError("Declare the additional calibrated available terminal read explicitly")
        if not isinstance(self.independence, Independence):
            raise TypeError("An explicit named initial-independence premise is required")
        if set(self.independence.origins) != {self.local.origin, self.reference.origin}:
            raise ValueError("Independence must name exactly the retained input origins")
        _name(self.joint_origin)
        _name(self.setting_id)
        if self.joint_origin in self.independence.origins:
            raise ValueError("The joint process uses a distinct origin")
        if self.coupler != SHARED_COUPLER or self.frame != FRAME or self.controller != CONTROLLER:
            raise ValueError(
                "Retain the actual fixed shared coupler, frame and nominal command/cut controller"
            )
        permutation = tuple(self.permutation)
        if any(type(label) is not int for label in permutation) or permutation != NATIVE_TO_GROUPED:
            raise ValueError("Permutation labels must be the exact built-in native-index integers")
        object.__setattr__(self, "permutation", permutation)

    @property
    def t(self) -> F:
        return self.reference.t


def _context(context: Context) -> Context:
    if not isinstance(context, Context):
        raise TypeError("Use a fully retained fixed-interior command/cut Context")
    return context


def complete_precursor(context: Context, count: int) -> tuple[tuple[str, int], ...]:
    """Tag all initial events and all previous joint records; infer no interinput order."""
    context = _context(context)
    if type(count) is not int or count < 0:
        raise ValueError("Previous joint record count must be a nonnegative built-in integer")
    inputs = tuple(
        (source.origin, record.event_id)
        for source in (context.local, context.reference)
        for record in source.records
    )
    return inputs + tuple((context.joint_origin, i) for i in range(count))


def _domain(domain: str) -> str:
    if domain != INTERIOR_DOMAIN:
        raise ValueError(
            "Primary commands require the explicit fixed-interior filtered L_t source-domain tag"
        )
    return domain


@dataclass(frozen=True)
class JointRecord:
    domain: str
    event_id: int
    outcome: tuple[int, int]
    precursor: tuple[tuple[str, int], ...]
    context: Context
    command_word: tuple[str, ...] = ()
    action: str = "literal_joint_cell_cut"

    def __post_init__(self) -> None:
        _domain(self.domain)
        context = _context(self.context)
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("Joint record ids must be nonnegative built-in integers")
        _cell(self.outcome)
        if self.action != "literal_joint_cell_cut":
            raise ValueError("Retain the actual fixed literal-cut action, not a reset label")
        precursor = tuple(tuple(item) for item in self.precursor)
        if any(
            len(item) != 2 or not isinstance(item[0], str) or type(item[1]) is not int
            for item in precursor
        ):
            raise ValueError("Each predecessor retains a named origin and a built-in event id")
        if precursor != complete_precursor(context, self.event_id):
            raise ValueError("Retain both initial prefixes and every previous joint record")
        object.__setattr__(self, "precursor", precursor)
        object.__setattr__(self, "command_word", _command_word(self.command_word))

    @property
    def origin(self) -> str:
        return self.context.joint_origin

    @property
    def reference_t(self) -> F:
        return self.context.t

    @property
    def reference_orientation(self) -> str:
        return self.context.reference.orientation

    @property
    def local_records(self) -> tuple[InputRecord, ...]:
        return self.context.local.records

    @property
    def reference_records(self) -> tuple[InputRecord, ...]:
        return self.context.reference.records

    @property
    def coupler(self) -> str:
        return self.context.coupler

    @property
    def frame(self) -> str:
        return self.context.frame

    @property
    def controller(self) -> str:
        return self.context.controller

    @property
    def setting_id(self) -> str:
        return self.context.setting_id


@dataclass(frozen=True)
class State:
    """Fixed-interior L_t snapshot retaining raw data and the pending nominal word.

    Cone/grammar validity is not physical preparation or global reachability.
    Silent commands append known labels, not records or physical time steps.
    Endpoint data belongs only to separate raw diagnostics, not this source type.
    """

    domain: str
    context: Context
    residual: Matrix
    records: tuple[JointRecord, ...] = ()
    pending: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _domain(self.domain)
        context = _context(self.context)
        d = image_kernel(self.residual, context.t, normalized=True)
        records = tuple(self.records)
        for i, record in enumerate(records):
            if (
                not isinstance(record, JointRecord)
                or record.event_id != i
                or record.context != context
                or record.domain != self.domain
            ):
                raise ValueError("Retain a complete L_t joint prefix in the unchanged context")
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "pending", _command_word(self.pending))

    @property
    def t(self) -> F:
        return self.context.t


def prepare_state(
    domain: str,
    local: LocalInput,
    reference: ReferenceInput,
    independence: Independence,
    *,
    terminal_read: "TerminalReadPremise",
    joint_origin: str = "joint",
    setting_id: str = NOMINAL_CUT,
) -> State:
    """Embed the declared K_t seed under the explicit fixed-interior command/cut contract."""
    _domain(domain)
    context = Context(
        local,
        reference,
        independence,
        terminal_read,
        joint_origin=joint_origin,
        setting_id=setting_id,
    )
    return State(domain, context, k_from_local(local.residual, reference.t, normalized=True))


def _source(state: State) -> State:
    if not isinstance(state, State):
        raise TypeError("Only this fixed-interior State admits the named commands and literal cuts")
    return state


def run_command(state: State, name: str) -> State:
    """Apply the actual named element silently and retain its nominal label once."""
    state = _source(state)
    output = command(state.residual, state.t, name)
    return State(state.domain, state.context, output, state.records, state.pending + (name,))


def run_word(state: State, names: Iterable[str]) -> State:
    state = _source(state)
    for name in _command_word(names):
        state = run_command(state, name)
    return state


def _question(question: str) -> str:
    if question not in ("fine", "b"):
        raise ValueError("Ask either the full retained fine outcome or its b component")
    return question


def record_answer(record: JointRecord, question: str = "fine") -> tuple[int, int] | int:
    """Read a question without erasing any actual fine record or raw residual."""
    if not isinstance(record, JointRecord):
        raise TypeError("A record question requires the complete typed JointRecord")
    return record.outcome if _question(question) == "fine" else record.outcome[1]


def next_question_probability(state: State, outcome: tuple[int, int], question: str = "fine") -> F:
    state, outcome, question = _source(state), _cell(outcome), _question(question)
    if question == "fine":
        return fine_effect_on_span(state.residual, state.t, outcome)
    return b_effect_on_span(state.residual, state.t, outcome[1])


def commit(state: State, outcome: tuple[int, int]) -> tuple[F, State]:
    """Cut the actual current residual and record its complete pending word once.

    Native mass supplies probability/normalization. Known command labels are
    never equated because their group elements or conditional cut weights agree.
    Clear only the pending word, preserving the complete immutable prior history.
    """
    state, outcome = _source(state), _cell(outcome)
    output = branch(state.residual, state.t, outcome)
    probability = raw_mass(output)
    if probability <= 0:
        raise ValueError("Cannot normalize or append a zero-probability literal cut")
    record = JointRecord(
        state.domain,
        len(state.records),
        outcome,
        complete_precursor(state.context, len(state.records)),
        state.context,
        state.pending,
    )
    return probability, State(
        state.domain, state.context, scale(1 / probability, output), state.records + (record,), ()
    )


commit_joint = commit


NOMINAL_TERMINAL_READ = "fixed_tilted_terminal_read"
READ_CALIBRATION = "filtered_tilt_3_0_4_over_5"
READ_Q_PLUS = scale(F(1, 10), matrix(((9, 3), (3, 1))))
READ_Q_MINUS = add(identity(2), scale(-1, READ_Q_PLUS))
TERMINAL_OUTCOMES = tuple((a, b, sign) for a, b in JOINT_CELLS for sign in ("+", "-"))
RECONSTRUCTION_WORDS = ((), ("A",), ("A", "A"))


def _sign(sign: str) -> str:
    if type(sign) is not str or sign not in ("+", "-"):
        raise ValueError("The internal terminal-read label is exactly '+' or '-'")
    return sign


def _terminal_outcome(outcome: tuple[int, int, str]) -> tuple[int, int, str]:
    if not isinstance(outcome, tuple) or len(outcome) != 3:
        raise ValueError("Retain the complete terminal outcome (a,b,sign)")
    return _bit(outcome[0]), _bit(outcome[1]), _sign(outcome[2])


def filtered_coordinates_on_span(d: Matrix, t: int | F = FIXED_T) -> tuple[Matrix, ...]:
    """Four sigma_ab=D_ab rho_ab D_ab/10, retaining each full complex block."""
    t = _fixture_t(t)
    rhos = inverse_span(d, t)
    return tuple(
        scale(F(1, 10), matmul(matmul(block_filter(cell, t), rho), block_filter(cell, t)))
        for rho, cell in zip(rhos, JOINT_CELLS, strict=True)
    )


def filtered_coordinates(d: Matrix, t: int | F = FIXED_T) -> tuple[Matrix, ...]:
    t = _fixture_t(t)
    return filtered_coordinates_on_span(image_kernel(d, t), t)


def from_filtered_coordinates_on_span(sigmas: Iterable[Matrix], t: int | F = FIXED_T) -> Matrix:
    """Algebraic full-image inverse, not a physical preparation or read output."""
    sigmas, t = _rhos(sigmas), _fixture_t(t)
    rhos = tuple(
        scale(10, matmul(matmul(inverse_filter(cell, t), sigma), inverse_filter(cell, t)))
        for sigma, cell in zip(sigmas, JOINT_CELLS, strict=True)
    )
    return image_span(rhos, t)


def from_filtered_coordinates(
    sigmas: Iterable[Matrix], t: int | F = FIXED_T, *, normalized: bool = False
) -> Matrix:
    sigmas, t = _rhos(sigmas), _fixture_t(t)
    if any(not is_psd(sigma) for sigma in sigmas):
        raise ValueError("Each filtered coordinate must be PSD")
    d = from_filtered_coordinates_on_span(sigmas, t)
    return image_kernel(d, t, normalized=normalized)


def terminal_projector(sign: str) -> Matrix:
    return READ_Q_PLUS if _sign(sign) == "+" else READ_Q_MINUS


def terminal_effect_matrix(outcome: tuple[int, int, str], t: int | F = FIXED_T) -> Matrix:
    """The declared cell-supported effect, expressed on its recovered rho_ab."""
    a, b, sign = _terminal_outcome(outcome)
    d_filter = block_filter((a, b), t)
    return scale(F(1, 10), matmul(matmul(d_filter, terminal_projector(sign)), d_filter))


def terminal_weights_on_span(d: Matrix, t: int | F = FIXED_T) -> RealVector:
    """Eight unconditioned cell/sign weights; differences are not divided by cell mass."""
    sigmas = filtered_coordinates_on_span(d, t)
    values = tuple(
        trace(matmul(terminal_projector(sign), sigma)) for sigma in sigmas for sign in ("+", "-")
    )
    if any(value.imag != 0 for value in values):
        raise ValueError("Hermitian terminal effects must have real evaluations")
    return tuple(value.real for value in values)


def terminal_weights(d: Matrix, t: int | F = FIXED_T) -> RealVector:
    t = _fixture_t(t)
    return terminal_weights_on_span(image_kernel(d, t), t)


read_weights = terminal_weights


def _bloch(sigma: Matrix) -> tuple[F, F, F, F]:
    sigma = _hermitian(sigma, 2)
    return (
        trace(sigma).real,
        2 * sigma[0][1].real,
        -2 * sigma[0][1].imag,
        sigma[0][0].real - sigma[1][1].real,
    )


def _sigma(q: F, x: F, y: F, z: F) -> Matrix:
    return scale(F(1, 2), add(scale(q, identity(2)), scale(x, X), scale(y, Y), scale(z, Z)))


def _diagnostic_axis(axis: str) -> str:
    if type(axis) is not str or axis not in ("Z", "X"):
        raise ValueError("Only the stated Z and X comparison summaries are defined")
    return axis


def diagnostic_summary_on_span(
    d: Matrix, t: int | F = FIXED_T, axis: str = "Z"
) -> tuple[tuple[F, ...], ...]:
    """Homogeneous comparison summary, not extra available terminal reads.

    Z returns (q,y,z) per cell, closed under the common-X commands; X returns
    (q,x). Their minimal ranks refer to mass-retaining full signed spans.
    """
    axis = _diagnostic_axis(axis)
    coordinates = tuple(_bloch(sigma) for sigma in filtered_coordinates_on_span(d, t))
    return tuple((q, y, z) if axis == "Z" else (q, x) for q, x, y, z in coordinates)


def diagnostic_summary(
    d: Matrix, t: int | F = FIXED_T, axis: str = "Z"
) -> tuple[tuple[F, ...], ...]:
    t = _fixture_t(t)
    return diagnostic_summary_on_span(image_kernel(d, t), t, axis)


def diagnostic_section(
    summary: Iterable[Iterable[int | F]],
    t: int | F = FIXED_T,
    axis: str = "Z",
    *,
    normalized: bool = False,
) -> Matrix:
    """Positive algebraic right inverse; no extra preparation/read/reset availability."""
    axis, t = _diagnostic_axis(axis), _fixture_t(t)
    summary = tuple(tuple(rational(value) for value in row) for row in summary)
    width = 3 if axis == "Z" else 2
    if len(summary) != 4 or any(len(row) != width for row in summary):
        raise ValueError("Retain four comparison coordinates in declared cell/axis order")
    sigmas = []
    for row in summary:
        q = row[0]
        x, y, z = (F(0), row[1], row[2]) if axis == "Z" else (row[1], F(0), F(0))
        if q < 0 or q * q < x * x + y * y + z * z:
            raise ValueError("Comparison summary is outside its exact positive cone")
        sigmas.append(_sigma(q, x, y, z))
    return from_filtered_coordinates(sigmas, t, normalized=normalized)


@dataclass(frozen=True)
class TerminalReadPremise:
    """Explicit additional availability/calibration assertion, not derived from DET."""

    setting_id: str = NOMINAL_TERMINAL_READ
    calibration: str = READ_CALIBRATION
    available: bool = True

    def __post_init__(self) -> None:
        _name(self.setting_id)
        if self.calibration != READ_CALIBRATION:
            raise ValueError("Only the one fixed tilted read has the declared exact calibration")
        if type(self.available) is not bool or not self.available:
            raise ValueError("The typed fixture requires an explicit available-read premise")


@dataclass(frozen=True)
class TerminalRecord:
    domain: str
    event_id: int
    outcome: tuple[int, int, str]
    precursor: tuple[tuple[str, int], ...]
    context: Context
    command_word: tuple[str, ...] = ()
    action: str = "terminal_tilted_read"

    def __post_init__(self) -> None:
        _domain(self.domain)
        context = _context(self.context)
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("Terminal event id must be a nonnegative built-in integer")
        _terminal_outcome(self.outcome)
        if self.action != "terminal_tilted_read":
            raise ValueError("The actual terminal-read action is not a literal cell commitment")
        precursor = tuple(tuple(item) for item in self.precursor)
        if any(
            len(item) != 2 or type(item[0]) is not str or type(item[1]) is not int
            for item in precursor
        ) or precursor != complete_precursor(context, self.event_id):
            raise ValueError("Retain all tagged input records and the whole preceding joint prefix")
        object.__setattr__(self, "precursor", precursor)
        object.__setattr__(self, "command_word", _command_word(self.command_word))

    @property
    def origin(self) -> str:
        return self.context.joint_origin

    @property
    def setting_id(self) -> str:
        return self.context.terminal_read.setting_id

    @property
    def calibration(self) -> str:
        return self.context.terminal_read.calibration


@dataclass(frozen=True)
class TerminalResult:
    """A selected terminal record and its exact pre-read source, not an output state.

    Probability is conditional on this normalized source snapshot only. Earlier
    input/reference selection probabilities are unspecified. Source retention
    is audit data, not an additional allowed read or policy input. No residual,
    normalization, reset or continuation after this result is provided.
    """

    source: State
    record: TerminalRecord
    effect: Matrix
    probability: F

    def __post_init__(self) -> None:
        source = _source(self.source)
        if not isinstance(self.record, TerminalRecord):
            raise TypeError("Retain the full typed terminal record")
        expected = TerminalRecord(
            source.domain,
            len(source.records),
            self.record.outcome,
            complete_precursor(source.context, len(source.records)),
            source.context,
            source.pending,
        )
        if self.record != expected:
            raise ValueError("Terminal record must retain the exact pre-read context and word")
        effect = matrix(self.effect)
        if effect != terminal_effect_matrix(self.record.outcome, source.t):
            raise ValueError("Retain the actual calibrated effect, not an inserted output kernel")
        probability = rational(self.probability)
        expected_probability = terminal_weights(source.residual, source.t)[
            TERMINAL_OUTCOMES.index(self.record.outcome)
        ]
        if expected_probability <= 0 or probability != expected_probability:
            raise ValueError("A selected terminal result requires its exact positive source weight")
        object.__setattr__(self, "effect", effect)
        object.__setattr__(self, "probability", probability)


def read_terminal(state: State, outcome: tuple[int, int, str]) -> TerminalResult:
    """Select one full cell/sign outcome without making a cell cut or an output state."""
    state, outcome = _source(state), _terminal_outcome(outcome)
    probability = terminal_weights(state.residual, state.t)[TERMINAL_OUTCOMES.index(outcome)]
    if probability <= 0:
        raise ValueError("Cannot select or append a zero-probability terminal result")
    record = TerminalRecord(
        state.domain,
        len(state.records),
        outcome,
        complete_precursor(state.context, len(state.records)),
        state.context,
        state.pending,
    )
    return TerminalResult(state, record, terminal_effect_matrix(outcome, state.t), probability)


@dataclass(frozen=True)
class ProbabilityTable:
    """Exact normalized full-outcome law at one separately resolved known word.

    These are supplied mathematical probabilities, not observed counts. Their
    comparison presumes the same snapshot under separate known settings; this
    constructor does not assert repeated-preparation availability.
    """

    word: tuple[str, ...]
    probabilities: tuple[tuple[tuple[int, int, str], F], ...]

    def __post_init__(self) -> None:
        word = _command_word(self.word)
        if word not in RECONSTRUCTION_WORDS:
            raise ValueError("This bounded table uses only (), ('A',), or ('A','A')")
        entries = tuple(tuple(entry) for entry in self.probabilities)
        if len(entries) != 8 or any(len(entry) != 2 for entry in entries):
            raise ValueError("Supply eight labeled full-outcome probabilities")
        probabilities = tuple(
            (_terminal_outcome(outcome), rational(value)) for outcome, value in entries
        )
        if tuple(outcome for outcome, _ in probabilities) != TERMINAL_OUTCOMES:
            raise ValueError("Full labels must remain in the fixed cell/sign order")
        values = tuple(value for _, value in probabilities)
        if any(value < 0 or value > 1 for value in values) or sum(values, F(0)) != 1:
            raise ValueError("Exact normalized terminal probabilities lie in [0,1] and sum to one")
        object.__setattr__(self, "word", word)
        object.__setattr__(self, "probabilities", probabilities)

    @property
    def weights(self) -> RealVector:
        return tuple(value for _, value in self.probabilities)


def probability_table(
    d: Matrix, t: int | F = FIXED_T, word: Iterable[str] = ()
) -> ProbabilityTable:
    """Algebraic separately resolved-setting law, not repeated physical execution."""
    t, word = _fixture_t(t), _command_word(word)
    if word not in RECONSTRUCTION_WORDS:
        raise ValueError("Only the three fixed reconstruction settings are specified")
    d = image_kernel(d, t, normalized=True)
    for name in word:
        d = command(d, t, name)
    return ProbabilityTable(
        word, tuple(zip(TERMINAL_OUTCOMES, terminal_weights(d, t), strict=True))
    )


def reconstruct_kernel(tables: Iterable[ProbabilityTable], t: int | F = FIXED_T) -> Matrix:
    """Exact conditional-state inverse, never a prepared state or terminal output.

    d_k is the complete unconditioned outcome difference, without division by
    q. Full raw entries, including zero-mass cells, are reconstructed and checked.
    """
    t, tables = _fixture_t(t), tuple(tables)
    if len(tables) != 3 or any(not isinstance(table, ProbabilityTable) for table in tables):
        raise TypeError("Supply exactly three complete typed probability tables")
    if tuple(table.word for table in tables) != RECONSTRUCTION_WORDS:
        raise ValueError("Retain the resolved setting order (), ('A',), ('A','A')")
    sigmas = []
    for cell in range(4):
        pairs = tuple(table.weights[2 * cell : 2 * cell + 2] for table in tables)
        masses = tuple(sum(pair, F(0)) for pair in pairs)
        if masses[1:] != masses[:1] * 2:
            raise ValueError("The known command settings must share every original cell mass")
        q = masses[0]
        d0, d1, d2 = (pair[0] - pair[1] for pair in pairs)
        x = (125 * d0 + 70 * d1 + 125 * d2) / 192
        y = (-55 * d0 + 180 * d1 - 125 * d2) / 192
        z = (195 * d0 - 70 * d1 - 125 * d2) / 256
        if q < 0 or q * q < x * x + y * y + z * z:
            raise ValueError("The reconstructed coordinates violate the exact PSD Bloch bound")
        sigmas.append(_sigma(q, x, y, z))
    d = from_filtered_coordinates(sigmas, t, normalized=True)
    if tuple(probability_table(d, t, word) for word in RECONSTRUCTION_WORDS) != tables:
        raise ValueError("The full reconstruction fails the supplied resolved-setting laws")
    return d


SQRT_UPPER_41 = F(640313, 100000)
SQRT_UPPER_6409 = F(1000703, 12500)
B_NORM_SQUARED = (F(640625, 589824), F(160225, 147456), F(640625, 589824))


def coefficient_upper_bounds() -> tuple[F, F, F]:
    """Rational upper enclosures of the three exact inverse-column norms.

    The exact coefficients are 125*sqrt(41)/768, 5*sqrt(6409)/384,
    and 125*sqrt(41)/768. These returned bounds are qualified upper
    enclosures, not exact radicals or statistically estimated constants.
    """
    if SQRT_UPPER_41 < 0 or SQRT_UPPER_41**2 < 41:
        raise ValueError("The first canonical rational root bound fails its exact square check")
    if SQRT_UPPER_6409 < 0 or SQRT_UPPER_6409**2 < 6409:
        raise ValueError("The second canonical rational root bound fails its exact square check")
    bounds = (
        125 * SQRT_UPPER_41 / 768,
        5 * SQRT_UPPER_6409 / 384,
        125 * SQRT_UPPER_41 / 768,
    )
    if any(
        upper < 1 or upper**2 < squared
        for upper, squared in zip(bounds, B_NORM_SQUARED, strict=True)
    ):
        raise ValueError("Every coefficient must certify its full exact norm and mass bound")
    return bounds


B_UPPER = coefficient_upper_bounds()


@dataclass(frozen=True)
class ErrorBudget:
    """Three supplied nonnegative exact TV budgets, not inferred sampling confidence."""

    etas: tuple[F, F, F]

    def __post_init__(self) -> None:
        etas = tuple(rational(eta) for eta in self.etas)
        if len(etas) != 3 or any(eta < 0 for eta in etas):
            raise ValueError("Supply exactly three nonnegative exact budgets in fixed word order")
        object.__setattr__(self, "etas", etas)


@dataclass(frozen=True)
class SnapshotMetadata:
    """Supplied common known metadata for a conditional snapshot comparison.

    This contains no unknown residual, preparation probability or terminal
    output. Different known contexts, complete prefixes or pending nominal
    words are not identified by matching numerical probability tables.
    """

    context: Context
    records: tuple[JointRecord, ...] = ()
    pending: tuple[str, ...] = ()
    domain: str = INTERIOR_DOMAIN

    def __post_init__(self) -> None:
        context = _context(self.context)
        _domain(self.domain)
        records = tuple(self.records)
        for i, record in enumerate(records):
            if (
                not isinstance(record, JointRecord)
                or record.event_id != i
                or record.context != context
                or record.domain != self.domain
            ):
                raise ValueError("Retain the complete known prefix in the unchanged context")
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "pending", _command_word(self.pending))


def metadata_from_state(state: State) -> SnapshotMetadata:
    """Read the supplied known prefix without making a new state or committed record."""
    state = _source(state)
    return SnapshotMetadata(state.context, state.records, state.pending, state.domain)


def _ordered_tables(tables: Iterable[ProbabilityTable]) -> tuple[ProbabilityTable, ...]:
    tables = tuple(tables)
    if len(tables) != 3 or any(not isinstance(table, ProbabilityTable) for table in tables):
        raise TypeError("Supply three complete normalized labeled ProbabilityTables")
    if tuple(table.word for table in tables) != RECONSTRUCTION_WORDS:
        raise ValueError("Preserve the separate resolved settings (), ('A',), ('A','A')")
    return tables


@dataclass(frozen=True)
class ObservationData:
    """Supplied normalized table centers y and exact per-setting error budgets.

    Each full eight-outcome table is normalized, but their cell masses may
    disagree across settings. No exact source is thereby asserted. A common
    metadata declaration is required and matched for typed source candidates.
    Raw candidate audits require metadata=None and have only fixed mathematical
    fixture scope; they cannot bind a declared context/history to a raw matrix.
    These are exact input values, not counts or demonstrated repeat preparations.
    """

    tables: tuple[ProbabilityTable, ...]
    budget: ErrorBudget
    metadata: SnapshotMetadata | None = None

    def __post_init__(self) -> None:
        tables = _ordered_tables(self.tables)
        if not isinstance(self.budget, ErrorBudget):
            raise TypeError("Use the explicitly supplied typed exact ErrorBudget")
        if self.metadata is not None and not isinstance(self.metadata, SnapshotMetadata):
            raise TypeError("Known comparison metadata must be complete SnapshotMetadata or None")
        object.__setattr__(self, "tables", tables)


def total_variation(left: ProbabilityTable, right: ProbabilityTable) -> F:
    """Exact full cell/sign TV at the SAME retained nominal setting."""
    if not isinstance(left, ProbabilityTable) or not isinstance(right, ProbabilityTable):
        raise TypeError("TV comparison requires two complete typed probability tables")
    if left.word != right.word:
        raise ValueError("Different known setting words cannot be silently identified")
    return sum((abs(a - b) for a, b in zip(left.weights, right.weights, strict=True)), F(0)) / 2


def _audit_inputs(
    candidate: State | Matrix, data: ObservationData
) -> tuple[State | Matrix, Matrix, tuple[ProbabilityTable, ...], tuple[F, ...]]:
    if not isinstance(data, ObservationData):
        raise TypeError("A candidate audit requires complete typed ObservationData")
    if isinstance(candidate, State):
        if data.metadata is None or data.metadata != metadata_from_state(candidate):
            raise ValueError(
                "Typed candidate must match all supplied context, records and pending word"
            )
        kernel = candidate.residual
    else:
        if isinstance(candidate, TerminalResult):
            raise TypeError(
                "A terminal result is not a source candidate or a postmeasurement kernel"
            )
        if data.metadata is not None:
            raise ValueError(
                "Raw candidates require metadata=None; use a typed State for matched metadata"
            )
        kernel = image_kernel(candidate, FIXED_T, normalized=True)
        candidate = kernel
    predicted = tuple(probability_table(kernel, FIXED_T, word) for word in RECONSTRUCTION_WORDS)
    errors = tuple(
        total_variation(prediction, supplied)
        for prediction, supplied in zip(predicted, data.tables, strict=True)
    )
    return candidate, kernel, predicted, errors


@dataclass(frozen=True)
class FeasibleWitness:
    """A supplied positive candidate proves nonemptiness and a qualified diameter bound.

    This is an immutable mathematical audit, not a fit, prepared State,
    terminal result or output residual. Any retained candidate State/context
    is pre-read audit data only. No additional availability is inferred.
    """

    candidate: State | Matrix
    data: ObservationData
    kernel: Matrix = field(init=False)
    predicted_tables: tuple[ProbabilityTable, ...] = field(init=False)
    actual_tv: tuple[F, ...] = field(init=False)
    filtered_diameter_upper: F = field(init=False)
    native_diameter_upper: F = field(init=False)

    def __post_init__(self) -> None:
        candidate, kernel, predicted, errors = _audit_inputs(self.candidate, self.data)
        if any(error > eta for error, eta in zip(errors, self.data.budget.etas, strict=True)):
            raise ValueError(
                "This candidate does not witness feasibility; that is not infeasibility"
            )
        filtered_upper = 2 * sum(
            (bound * eta for bound, eta in zip(B_UPPER, self.data.budget.etas, strict=True)),
            F(0),
        )
        object.__setattr__(self, "candidate", candidate)
        object.__setattr__(self, "kernel", kernel)
        object.__setattr__(self, "predicted_tables", predicted)
        object.__setattr__(self, "actual_tv", errors)
        object.__setattr__(self, "filtered_diameter_upper", filtered_upper)
        object.__setattr__(self, "native_diameter_upper", filtered_upper / (1 - abs(FIXED_T)))

    @property
    def feasible_nonempty(self) -> bool:
        return True

    @property
    def coefficient_upper(self) -> tuple[F, F, F]:
        return B_UPPER


@dataclass(frozen=True)
class CandidateFailure:
    """Failure of only this supplied candidate; existence of another remains open.

    No fitting search was made, and no infeasibility statement or certificate
    follows. The full candidate payload, tables, errors and metadata remain
    retained without preparation, commitment or terminal continuation.
    """

    candidate: State | Matrix
    data: ObservationData
    kernel: Matrix = field(init=False)
    predicted_tables: tuple[ProbabilityTable, ...] = field(init=False)
    actual_tv: tuple[F, ...] = field(init=False)
    failed_settings: tuple[tuple[str, ...], ...] = field(init=False)
    conclusion: str = field(init=False, default="inconclusive")

    def __post_init__(self) -> None:
        candidate, kernel, predicted, errors = _audit_inputs(self.candidate, self.data)
        failed = tuple(
            word
            for word, error, eta in zip(
                RECONSTRUCTION_WORDS, errors, self.data.budget.etas, strict=True
            )
            if error > eta
        )
        if not failed:
            raise ValueError("The supplied candidate is feasible and cannot be labeled a failure")
        object.__setattr__(self, "candidate", candidate)
        object.__setattr__(self, "kernel", kernel)
        object.__setattr__(self, "predicted_tables", predicted)
        object.__setattr__(self, "actual_tv", errors)
        object.__setattr__(self, "failed_settings", failed)


def candidate_witness(
    candidate: State | Matrix,
    tables: Iterable[ProbabilityTable],
    budget: ErrorBudget,
    *,
    metadata: SnapshotMetadata | None = None,
) -> FeasibleWitness | CandidateFailure:
    """Evaluate one explicitly supplied candidate; never solve or assert infeasibility."""
    data = ObservationData(tables, budget, metadata)
    candidate, _, _, errors = _audit_inputs(candidate, data)
    if all(error <= eta for error, eta in zip(errors, budget.etas, strict=True)):
        return FeasibleWitness(candidate, data)
    return CandidateFailure(candidate, data)


def filtered_difference_data(
    left: Matrix, right: Matrix, t: int | F = FIXED_T
) -> tuple[tuple[F, F], ...]:
    """Exact radical data for the filtered distance of two normalized candidates.

    Each pair is (abs(delta_q), delta_x^2+delta_y^2+delta_z^2). Therefore
    d_F = (1/2) sum max(pair[0], sqrt(pair[1])). No square root is approximated
    and no conditional division by possibly zero cell mass is performed.
    This diagnostic does not make either matrix available as an observation.
    """
    t = _fixture_t(t)
    left = filtered_coordinates(image_kernel(left, t, normalized=True), t)
    right = filtered_coordinates(image_kernel(right, t, normalized=True), t)
    result = []
    for a, b in zip(left, right, strict=True):
        q, x, y, z = _bloch(add(a, scale(-1, b)))
        result.append((abs(q), x * x + y * y + z * z))
    return tuple(result)
