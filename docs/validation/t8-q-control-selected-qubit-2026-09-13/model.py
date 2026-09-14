"""Exact chosen-control witness for a qubit-shaped predictive quotient.

All atoms, controls, preparations and terminal readouts are supplied candidate
premises. Full four-atom kernels, including complex cross-block residuals, are
retained. Gaussian rational arithmetic implements Hadamard congruence exactly,
without inserting approximate square roots. This is neither a DET selection
theorem nor a native derivation of physically available quantum operations.
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


def transpose(d: Matrix) -> Matrix:
    d = matrix(d)
    return tuple(tuple(d[i][j] for i in range(len(d))) for j in range(len(d[0])))


def _two(d: Matrix) -> Matrix:
    d = matrix(d)
    if len(d) != 2 or len(d[0]) != 2:
        raise ValueError("A qubit block must be two by two")
    return d


def _four(d: Matrix) -> Matrix:
    d = matrix(d)
    if len(d) != 4 or len(d[0]) != 4 or not is_hermitian(d):
        raise ValueError("Use a Hermitian four-atom kernel")
    return d


def full_kernel(d: Matrix, *, normalized: bool = False) -> Matrix:
    d = _four(d)
    if not is_psd(d):
        raise ValueError("The full four-atom kernel must be PSD")
    if normalized and mass(d) != 1:
        raise ValueError("Normalized kernels must have total-entry mass one")
    return d


Z = matrix(((1, 0), (0, -1)))
H0 = matrix(((1, 1), (1, -1)))
P = matrix(((1, 0), (0, I)))
P_INV = dagger(P)
CONTROLS = ("H", "P", "P_inv", "Z")
CELL_INDICATORS = (vector((1, 1, 0, 0)), vector((0, 0, 1, 1)))
CELL_PROJECTORS = (
    matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))),
    matrix(((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))),
)


def blocks(d: Matrix) -> tuple[Matrix, Matrix, Matrix]:
    """Return A,F,B for the full Hermitian block array [[A,F],[F*,B]]."""
    d = _four(d)
    return (
        matrix(row[:2] for row in d[:2]),
        matrix(row[2:] for row in d[:2]),
        matrix(row[2:] for row in d[2:]),
    )


def assemble(a: Matrix, f: Matrix, b: Matrix) -> Matrix:
    """Assemble full blocks without claiming positivity or recordability."""
    a, f, b = _two(a), _two(f), _two(b)
    adjoint = dagger(f)
    return matrix(tuple(a[i]) + tuple(f[i]) for i in range(2)) + matrix(
        tuple(adjoint[i]) + tuple(b[i]) for i in range(2)
    )


def qcell(d: Matrix) -> RealVector:
    d = _four(d)
    return tuple(inner(b, matvec(d, b)).real for b in CELL_INDICATORS)


def mass(d: Matrix) -> F:
    """Total-entry mass e* D e; not trace and not necessarily preserved off-domain."""
    d = _four(d)
    e = vector((1, 1, 1, 1))
    return inner(e, matvec(d, e)).real


m = mass


def recordable(d: Matrix) -> bool:
    """Initial exact cell-recordability on the full PSD four-atom cone."""
    d = _four(d)
    return is_psd(d) and inner(CELL_INDICATORS[0], matvec(d, CELL_INDICATORS[1])) == 0


def control_spec(name: str) -> tuple[Matrix, F]:
    """Return W numerator and its congruence factor, not an approximate unitary.

    H uses W0=diag(H0,Z H0 Z), so W D W* is W0 D W0*/2.
    Other controls have factor one and exactly Gaussian-rational entries.
    """
    if name not in CONTROLS:
        raise ValueError("Control is not in the supplied fixed catalogue")
    numerator = {"H": H0, "P": P, "P_inv": P_INV, "Z": Z}[name]
    other = matmul(matmul(Z, numerator), Z)
    zero = zeros(2)
    return assemble(numerator, zero, other), F(1, 2) if name == "H" else F(1)


def controls(d: Matrix, name: str) -> Matrix:
    """Raw full-kernel congruence; no off-candidate domain or mass claim.

    Lawful source-State application is run_control, which independently
    validates the invariant candidate. This raw fixture helper only needs PSD.
    """
    d = full_kernel(d)
    numerator, factor = control_spec(name)
    return scale(factor, matmul(matmul(numerator, d), dagger(numerator)))


def word(d: Matrix, names: Iterable[str]) -> Matrix:
    d = full_kernel(d)
    if isinstance(names, str):
        raise TypeError("A control word is an iterable of control names, not a string")
    for name in names:
        d = controls(d, name)
    return d


def decompose_candidate(d: Matrix, *, normalized: bool = False) -> tuple[Matrix, G]:
    """Require D(A,c)=[[A,cZ],[conj(c)Z,ZAZ]], retaining complex c.

    PSD is checked on the full four-by-four matrix. Equivalently A>=|c|I;
    checking the full matrix avoids approximating the potentially irrational
    absolute value. This is the stated candidate, not an assumed block-diagonal
    starting cone or a proof here that control viability selects it uniquely.
    """
    d = full_kernel(d, normalized=normalized)
    a, f, b = blocks(d)
    c = f[0][0]
    if f != scale(c, Z) or b != matmul(matmul(Z, a), Z):
        raise ValueError("Kernel is outside the supplied control-selected candidate")
    return a, c


def candidate_from(a: Matrix, c: G | int | F = 0, *, normalized: bool = False) -> Matrix:
    a, c = _two(a), gaussian(c)
    d = assemble(a, scale(c, Z), matmul(matmul(Z, a), Z))
    decompose_candidate(d, normalized=normalized)
    return d


def q_quantum(d: Matrix) -> Matrix:
    """The chosen predictive quotient rho=2 A^T; complex residual c is forgotten."""
    a, _ = decompose_candidate(d)
    return scale(2, transpose(a))


def section(rho: Matrix, *, normalized: bool = False) -> Matrix:
    """Positive c=0 section of the candidate quotient, not an inverse on full D."""
    rho = _two(rho)
    if not is_psd(rho):
        raise ValueError("The quotient preparation must be a PSD two-by-two matrix")
    if normalized and sum((rho[i][i].real for i in range(2)), F(0)) != 1:
        raise ValueError("A normalized quotient preparation must have trace one")
    return candidate_from(scale(F(1, 2), transpose(rho)), normalized=normalized)


def _outcome(outcome: int) -> int:
    if type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("A cell outcome must be exactly 0 or 1")
    return outcome


def _settings(names: Iterable[str]) -> tuple[str, ...]:
    if isinstance(names, str):
        raise TypeError("Supply a tuple or iterable of complete control names")
    result = tuple(names)
    if any(name not in CONTROLS for name in result):
        raise ValueError("Setting word contains an unavailable control")
    return result


@dataclass(frozen=True)
class Record:
    event_id: int
    outcome: int
    settings: tuple[str, ...]
    precursor: tuple[int, ...]
    action: str = "terminal_cell_read"
    source_kind: str = "control_selected"

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("A committed event id must be a nonnegative integer")
        _outcome(self.outcome)
        if self.action != "terminal_cell_read" or self.source_kind != "control_selected":
            raise ValueError("Record must retain this supplied action and source kind")
        object.__setattr__(self, "settings", _settings(self.settings))
        if not isinstance(self.precursor, tuple) or any(
            type(event) is not int or event < 0 for event in self.precursor
        ):
            raise ValueError("Precursor must be an immutable tuple of earlier event ids")


def history(records: Iterable[Record]) -> tuple[Record, ...]:
    """Validate full-prefix chain grammar, not a global preparation trajectory."""
    result = tuple(records)
    for i, record in enumerate(result):
        if not isinstance(record, Record):
            raise TypeError("Committed history contains full Record values")
        if record.event_id != i or record.precursor != tuple(range(i)):
            raise ValueError("Use consecutive fresh ids and the entire earlier committed prefix")
    return result


@dataclass(frozen=True)
class State:
    """Validated candidate snapshot with declared prior record/setting grammar.

    Construction does not prove global reachability from an earlier supplied
    preparation. run_control/run_word retain the actual forward-applied word.
    """

    residual: Matrix
    records: tuple[Record, ...] = ()
    settings: tuple[str, ...] = ()
    source_kind: str = "control_selected"

    def __post_init__(self) -> None:
        if self.source_kind != "control_selected":
            raise ValueError("This source State belongs only to the selected candidate")
        d = matrix(self.residual)
        decompose_candidate(d, normalized=True)
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", history(self.records))
        object.__setattr__(self, "settings", _settings(self.settings))


@dataclass(frozen=True)
class TerminalState:
    """Full normalized post-cut residual; no source controls are registered here."""

    residual: Matrix
    records: tuple[Record, ...]
    source_kind: str = "terminal_cell_cut"

    def __post_init__(self) -> None:
        if self.source_kind != "terminal_cell_cut":
            raise ValueError("Terminal residual keeps its distinct source kind")
        d = full_kernel(self.residual, normalized=True)
        records = history(self.records)
        if not records:
            raise ValueError("A terminal cell cut must retain its committed record")
        projector = CELL_PROJECTORS[records[-1].outcome]
        if matmul(matmul(projector, d), projector) != d:
            raise ValueError("Terminal residual must retain the selected cell support")
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", records)


def _source(state: State) -> State:
    if not isinstance(state, State):
        raise TypeError("Only a control-selected source State has these lawful continuations")
    return state


def run_control(state: State, name: str) -> State:
    state = _source(state)
    return State(controls(state.residual, name), state.records, state.settings + (name,))


def run_word(state: State, names: Iterable[str]) -> State:
    state = _source(state)
    for name in _settings(names):
        state = run_control(state, name)
    return state


def commit_cell(state: State, outcome: int) -> tuple[F, TerminalState]:
    """Select a positive branch of the terminal literal cell-cut instrument.

    Preserve the full four-atom residual and actual supplied setting word. The
    whole committed prefix is a chosen precursor; no clock, erased record, or
    quantum reset is introduced. Zero mass refuses before normalization/append.
    """
    state, outcome = _source(state), _outcome(outcome)
    projector = CELL_PROJECTORS[outcome]
    output = matmul(matmul(projector, state.residual), projector)
    probability = mass(output)
    if probability <= 0:
        raise ValueError("Cannot select, normalize, or append a zero-probability branch")
    normalized = scale(1 / probability, output)
    records = state.records + (
        Record(len(state.records), outcome, state.settings, tuple(range(len(state.records)))),
    )
    return probability, TerminalState(normalized, records)
