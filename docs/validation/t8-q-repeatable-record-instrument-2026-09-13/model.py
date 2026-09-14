"""Exact conditional repeatable Pauli record instrument on the six-real source cone.

The finite atoms, invariant source cone, controls and preparation availability
are additional declared premises. Positivity, same-cone range, calibrated
effects and perfect repeatability derive the branch formula in the companion
proof; their physical availability is not derived. This is not a selection
theorem from DET. All complex arithmetic is Gaussian rational.
Source controls actually transform the current kernel. Record readout uses the
stated fixed Pauli frame; no unrecorded inverse control or old literal-cut reset
is hidden in a branch. Committed prefixes remain immutable.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType

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


def decompose_span(d: Matrix) -> tuple[Matrix, G]:
    """Full six-real-dimensional Hermitian span; indefinite inputs are allowed."""
    d = _four(d)
    a, f, b = blocks(d)
    c = f[0][0]
    if f != scale(c, Z) or b != matmul(matmul(Z, a), Z):
        raise ValueError("Kernel is outside the six-real-dimensional source span")
    return a, c


def decompose_candidate(d: Matrix, *, normalized: bool = False) -> tuple[Matrix, G]:
    """Require D(A,c)=[[A,cZ],[conj(c)Z,ZAZ]], retaining complex c.

    PSD is checked on the full four-by-four matrix. Equivalently A>=|c|I;
    checking the full matrix avoids approximating the potentially irrational
    absolute value. This is the stated candidate, not an assumed block-diagonal
    starting cone or a proof here that control viability selects it uniquely.
    """
    d = full_kernel(d, normalized=normalized)
    return decompose_span(d)


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


def trace(d: Matrix) -> G:
    d = matrix(d)
    if len(d) != len(d[0]):
        raise ValueError("Trace requires a square matrix")
    return sum((d[i][i] for i in range(len(d))), G())


def phi_on_span(d: Matrix) -> Matrix:
    a, _ = decompose_span(d)
    return scale(2, transpose(a))


phi = q_quantum
J2 = section
X = matrix(((0, 1), (1, 0)))
Y = matrix(((0, -I), (I, 0)))
AXES = ("X", "Y", "Z")
PAULI = MappingProxyType({"X": X, "Y": Y, "Z": Z})
CONTROLLER = "pauli_controller"
SOURCE_KIND = "repeatable_selected"
FRAME = "fixed_pauli"


def _axis(axis: str) -> str:
    if axis not in AXES:
        raise ValueError("The supplied instrument has only the fixed X, Y and Z axes")
    return axis


def _outcome(outcome: int) -> int:
    if type(outcome) is not int or outcome not in (0, 1):
        raise ValueError("A branch outcome must be exactly 0 or 1")
    return outcome


def projector(axis: str, outcome: int) -> Matrix:
    axis, outcome = _axis(axis), _outcome(outcome)
    return scale(F(1, 2), add(identity(2), scale((-1) ** outcome, PAULI[axis])))


def effect_on_span(d: Matrix, axis: str, outcome: int) -> F:
    """The signed real-linear extension Tr(Phi(d) Q_axis,outcome)."""
    value = trace(matmul(phi_on_span(d), projector(axis, outcome)))
    if value.imag != 0:
        raise ValueError("Hermitian effect evaluation must be real")
    return value.real


def branch_on_span(d: Matrix, axis: str, outcome: int) -> Matrix:
    """B(d)=effect(d) J2(Q), on every signed element of the full source span.

    In particular, each zero-probability positive input is mapped to the entire
    zero matrix, not to an unnormalized hidden remnant or a supplied reset.
    """
    probability = effect_on_span(d, axis, outcome)
    return scale(probability, section(projector(axis, outcome)))


def effect(d: Matrix, axis: str, outcome: int) -> F:
    d = matrix(d)
    decompose_candidate(d)
    return effect_on_span(d, axis, outcome)


def branch(d: Matrix, axis: str, outcome: int) -> Matrix:
    """The conditionally derived positive source-to-source branch, not a cell cut.

    The formula follows from the companion proof's calibrated-effect,
    positivity, same-cone range and repeatability premises; physical operation
    availability remains a separate supplied premise.
    """
    d = matrix(d)
    decompose_candidate(d)
    output = branch_on_span(d, axis, outcome)
    decompose_candidate(output)
    return output


def mix_residuals(weights: Iterable[int | F], residuals: Iterable[Matrix]) -> Matrix:
    """A declared preparation convex mixture of bare normalized kernels only.

    This helper neither establishes physical randomization/preparability nor
    accepts State/history values. It never erases differing committed prefixes,
    controller settings, or branch records by mixing recordful process states.
    """
    weights = tuple(rational(weight) for weight in weights)
    raw_residuals = tuple(residuals)
    if any(isinstance(residual, (State, TerminalState)) for residual in raw_residuals):
        raise TypeError("Preparation mixtures accept bare kernels, never recordful State values")
    residuals = tuple(matrix(residual) for residual in raw_residuals)
    if not weights or len(weights) != len(residuals):
        raise ValueError("Supply equally many nonempty weights and residuals")
    if any(weight < 0 for weight in weights) or sum(weights, F(0)) != 1:
        raise ValueError("Preparation weights must be nonnegative and sum exactly to one")
    for residual in residuals:
        decompose_candidate(residual, normalized=True)
    output = add(
        zeros(4),
        *(scale(weight, residual) for weight, residual in zip(weights, residuals, strict=True)),
    )
    decompose_candidate(output, normalized=True)
    return output


def _settings(names: Iterable[str]) -> tuple[str, ...]:
    if isinstance(names, str):
        raise TypeError("Supply an iterable of complete control names, not a string")
    result = tuple(names)
    if any(name not in CONTROLS for name in result):
        raise ValueError("Pending setting word contains an unavailable control")
    return result


@dataclass(frozen=True)
class Record:
    event_id: int
    axis: str
    outcome: int
    settings: tuple[str, ...]
    precursor: tuple[int, ...]
    action: str = "pauli_measure_prepare"
    controller: str = CONTROLLER
    source_kind: str = SOURCE_KIND
    frame: str = FRAME

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("A record id must be a nonnegative integer")
        _outcome(self.outcome)
        if self.controller != CONTROLLER or self.source_kind != SOURCE_KIND or self.frame != FRAME:
            raise ValueError(
                "A record retains the supplied controller, source kind and fixed frame"
            )
        if self.action == "pauli_measure_prepare":
            _axis(self.axis)
        elif self.action != "literal_cell_cut" or self.axis != "CELL":
            raise ValueError(
                "Use a supplied Pauli label or the separate literal-cut countermodel label"
            )
        object.__setattr__(self, "settings", _settings(self.settings))
        if not isinstance(self.precursor, tuple) or any(
            type(event) is not int or event < 0 for event in self.precursor
        ):
            raise ValueError("Precursor must be an immutable tuple of earlier event ids")


def history(records: Iterable[Record], *, terminal: bool = False) -> tuple[Record, ...]:
    """Check the chosen full-prefix chain grammar, not global reachability."""
    records = tuple(records)
    for i, record in enumerate(records):
        if not isinstance(record, Record):
            raise TypeError("Committed histories contain complete Record values")
        if record.event_id != i or record.precursor != tuple(range(i)):
            raise ValueError("Use fresh consecutive ids and the entire earlier committed prefix")
        if record.action == "literal_cell_cut" and (not terminal or i != len(records) - 1):
            raise ValueError("Literal-cut records cannot appear inside repeatable-source histories")
    if terminal and (not records or records[-1].action != "literal_cell_cut"):
        raise ValueError("The terminal countermodel must end in its distinct cell-cut record")
    return records


@dataclass(frozen=True)
class State:
    """Candidate snapshot with declared prefix and pending actually applied word.

    Construction validates grammar/cone membership, not global reachability
    from a prior preparation. Forward controls transform the current residual;
    a successful record stores the pending word, then clears it in the source.
    """

    residual: Matrix
    records: tuple[Record, ...] = ()
    settings: tuple[str, ...] = ()
    controller: str = CONTROLLER
    source_kind: str = SOURCE_KIND
    frame: str = FRAME

    def __post_init__(self) -> None:
        if self.controller != CONTROLLER or self.source_kind != SOURCE_KIND or self.frame != FRAME:
            raise ValueError(
                "State must retain the declared controller, source kind and fixed frame"
            )
        d = matrix(self.residual)
        decompose_candidate(d, normalized=True)
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", history(self.records))
        object.__setattr__(self, "settings", _settings(self.settings))


@dataclass(frozen=True)
class TerminalState:
    """Isolated literal-cut residual; no controls, repeatable records or reset API."""

    residual: Matrix
    records: tuple[Record, ...]
    controller: str = CONTROLLER
    source_kind: str = "literal_cell_cut"
    frame: str = FRAME

    def __post_init__(self) -> None:
        if (
            self.controller != CONTROLLER
            or self.source_kind != "literal_cell_cut"
            or self.frame != FRAME
        ):
            raise ValueError("Terminal countermodel retains its distinct source type")
        d = full_kernel(self.residual, normalized=True)
        records = history(self.records, terminal=True)
        projector = CELL_PROJECTORS[records[-1].outcome]
        if matmul(matmul(projector, d), projector) != d:
            raise ValueError("Literal-cut terminal residual must retain the selected cell support")
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", records)


def _source(state: State) -> State:
    if not isinstance(state, State):
        raise TypeError("Only a repeatable-selected State has these supplied source continuations")
    return state


def run_control(state: State, name: str) -> State:
    state = _source(state)
    return State(
        controls(state.residual, name),
        state.records,
        state.settings + (name,),
        state.controller,
        state.source_kind,
        state.frame,
    )


def run_word(state: State, names: Iterable[str]) -> State:
    state = _source(state)
    for name in _settings(names):
        state = run_control(state, name)
    return state


def commit_pauli(state: State, axis: str, outcome: int) -> tuple[F, State]:
    """Fixed-frame readout of the CURRENT residual, without a hidden inverse.

    The positive branch has the form derived from the declared structural and
    repeatability premises. It is not an old literal cell cut plus a silently
    authorized source reset, and the proof does not establish its availability.
    """
    state, axis, outcome = _source(state), _axis(axis), _outcome(outcome)
    output = branch(state.residual, axis, outcome)
    probability = mass(output)
    if probability <= 0:
        raise ValueError("Cannot select, normalize or append a zero-probability branch")
    normalized = scale(1 / probability, output)
    records = state.records + (
        Record(
            len(state.records),
            axis,
            outcome,
            state.settings,
            tuple(range(len(state.records))),
            controller=state.controller,
            source_kind=state.source_kind,
            frame=state.frame,
        ),
    )
    return probability, State(
        normalized, records, (), state.controller, state.source_kind, state.frame
    )


def literal_cut(state: State, outcome: int) -> tuple[F, TerminalState]:
    """Countermodel helper only: a full terminal cell cut, never a repeatable reset."""
    state, outcome = _source(state), _outcome(outcome)
    projector = CELL_PROJECTORS[outcome]
    output = matmul(matmul(projector, state.residual), projector)
    probability = mass(output)
    if probability <= 0:
        raise ValueError("Cannot select, normalize or append a zero-mass literal cut")
    records = state.records + (
        Record(
            len(state.records),
            "CELL",
            outcome,
            state.settings,
            tuple(range(len(state.records))),
            action="literal_cell_cut",
            controller=state.controller,
            source_kind=state.source_kind,
            frame=state.frame,
        ),
    )
    return probability, TerminalState(scale(1 / probability, output), records)
