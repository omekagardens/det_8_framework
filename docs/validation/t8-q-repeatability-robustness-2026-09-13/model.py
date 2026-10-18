"""Exact finite approximate-repeatability witnesses with explicit source domains.

The primary domain is the declared composite-compatible c=0 cone. Approximate
ray targets are additional instrument-availability premises, not preparations
derived from the earlier finite control catalogue. The broader complex-c cone
is a separate local-only scope, with its own specified non-descending witness.
Ideal and approximate models may share the same full nominal record alphabet;
implementation parameters are not silently added as distinguishable outcomes.
All controls act on the current residual in the retained fixed frame.
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
    """Older control/read catalogue quotient rho=2 A^T, forgetting complex c.

    This is not a predictive quotient for every instrument in this bundle:
    LocalCounterInstrument can fail to descend through it.
    """
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


ideal_branch = branch
LOCAL_ONLY = "local_only"
COMPOSITE_C0 = "composite_C0"
DOMAINS = (LOCAL_ONLY, COMPOSITE_C0)
DEFAULT_EPSILON = F(1, 5)
COUNTER_K = F(2, 5)
NOMINAL_SETTING = "pauli_device"


def _domain(domain: str) -> str:
    if domain not in DOMAINS:
        raise ValueError("Declare either the local-only full C or composite-compatible C0 domain")
    return domain


def _label(label: str) -> str:
    if not isinstance(label, str) or not label:
        raise ValueError("Retained nominal settings and provenance labels must be nonempty strings")
    return label


def domain_span(d: Matrix, domain: str) -> Matrix:
    d, domain = matrix(d), _domain(domain)
    _, c = decompose_span(d)
    if domain == COMPOSITE_C0 and c != 0:
        raise ValueError("The composite-compatible span requires c=0, not discarded nonzero c")
    return d


def domain_kernel(d: Matrix, domain: str, *, normalized: bool = False) -> Matrix:
    d = domain_span(d, domain)
    decompose_candidate(d, normalized=normalized)
    return d


@dataclass(frozen=True)
class Instrument:
    """A positive calibrated ray-target instrument with a uniform deficit bound.

    On C0 the factorization is the conditional rank-one-effect theorem in the
    companion proof. Target availability is supplied separately. On full C,
    this class specifies a subclass only, not all admissible instruments.
    Epsilon, targets and provenance describe an implementation model, not extra
    record labels. setting_id is the actually retained nominal device setting.
    """

    axis: str
    epsilon: F
    targets: tuple[Matrix, Matrix]
    domain: str = COMPOSITE_C0
    provenance: str = "declared-ray-targets"
    setting_id: str = NOMINAL_SETTING

    def __post_init__(self) -> None:
        _axis(self.axis)
        _domain(self.domain)
        _label(self.provenance)
        _label(self.setting_id)
        epsilon = rational(self.epsilon)
        if epsilon < 0 or epsilon > F(1, 2):
            raise ValueError("The declared repeatability deficit must be in [0,1/2]")
        targets = tuple(
            domain_kernel(target, self.domain, normalized=True) for target in self.targets
        )
        if len(targets) != 2:
            raise ValueError("Retain one complete normalized target for each outcome")
        for outcome, target in enumerate(targets):
            if 1 - effect_on_span(target, self.axis, outcome) > epsilon:
                raise ValueError("A target exceeds the declared calibrated same-axis deficit")
        object.__setattr__(self, "epsilon", epsilon)
        object.__setattr__(self, "targets", targets)

    def effect(self, d: Matrix, outcome: int) -> F:
        d = domain_kernel(d, self.domain)
        return effect_on_span(d, self.axis, outcome)

    def branch_on_span(self, d: Matrix, outcome: int) -> Matrix:
        d, outcome = domain_span(d, self.domain), _outcome(outcome)
        return scale(effect_on_span(d, self.axis, outcome), self.targets[outcome])

    def branch(self, d: Matrix, outcome: int) -> Matrix:
        d = domain_kernel(d, self.domain)
        return domain_kernel(self.branch_on_span(d, outcome), self.domain)


def ideal_instrument(
    axis: str, domain: str = COMPOSITE_C0, *, setting_id: str = NOMINAL_SETTING
) -> Instrument:
    axis = _axis(axis)
    return Instrument(
        axis,
        F(0),
        tuple(section(projector(axis, outcome)) for outcome in (0, 1)),
        domain,
        "ideal conditional instrument",
        setting_id,
    )


def noisy_pauli_instrument(
    axis: str,
    epsilon: int | F = DEFAULT_EPSILON,
    domain: str = COMPOSITE_C0,
    *,
    setting_id: str = NOMINAL_SETTING,
) -> Instrument:
    """A supplied diagonal-error example; sharp coherent targets may be supplied directly."""
    axis, epsilon = _axis(axis), rational(epsilon)
    targets = tuple(
        section(
            add(
                scale(1 - epsilon, projector(axis, outcome)),
                scale(epsilon, projector(axis, 1 - outcome)),
            )
        )
        for outcome in (0, 1)
    )
    return Instrument(axis, epsilon, targets, domain, "declared diagonal-error targets", setting_id)


@dataclass(frozen=True)
class LocalCounterInstrument:
    """The single specified broader-C non-descent witness, not a C0 construction.

    Its Z+ branch keeps a k*c-dependent quotient off-diagonal while setting
    output c to zero. Positivity on full C follows from |c|<=p/2 and
    k^2=epsilon(1-epsilon), as proved separately. The complementary Z- branch
    is ideal. This class does not infer availability from the primary domain.
    """

    axis: str = "Z"
    epsilon: F = DEFAULT_EPSILON
    k: F = COUNTER_K
    domain: str = LOCAL_ONLY
    provenance: str = "specified local non-descent counterexample"
    setting_id: str = NOMINAL_SETTING

    def __post_init__(self) -> None:
        epsilon, k = rational(self.epsilon), rational(self.k)
        if (
            self.axis != "Z"
            or epsilon != DEFAULT_EPSILON
            or k != COUNTER_K
            or self.domain != LOCAL_ONLY
        ):
            raise ValueError("This local-only witness fixes axis Z, epsilon=1/5 and k=2/5")
        _label(self.provenance)
        _label(self.setting_id)
        object.__setattr__(self, "epsilon", epsilon)
        object.__setattr__(self, "k", k)

    def effect(self, d: Matrix, outcome: int) -> F:
        d = domain_kernel(d, self.domain)
        return effect_on_span(d, self.axis, outcome)

    def branch_on_span(self, d: Matrix, outcome: int) -> Matrix:
        d, outcome = domain_span(d, self.domain), _outcome(outcome)
        if outcome == 1:
            return branch_on_span(d, "Z", 1)
        _, c = decompose_span(d)
        p = effect_on_span(d, "Z", 0)
        a = matrix(
            (
                (p * (1 - self.epsilon) / 2, self.k * c),
                (self.k * c.conjugate(), p * self.epsilon / 2),
            )
        )
        return assemble(a, zeros(2), matmul(matmul(Z, a), Z))

    def branch(self, d: Matrix, outcome: int) -> Matrix:
        d = domain_kernel(d, self.domain)
        return domain_kernel(self.branch_on_span(d, outcome), self.domain)


def quotient_trace_distance_squared_to_ray(d: Matrix, axis: str, outcome: int) -> F:
    """Exact [one-half ||Phi(d)-Q||_1]^2 for a normalized qubit quotient.

    For a traceless Hermitian 2x2 difference this is delta_00^2+|delta_01|^2.
    This is a QUOTIENT distance, not a bound on forgotten complex-c raw data.
    On C0, the section duplicates half-scaled blocks and preserves trace norm.
    """
    d = matrix(d)
    decompose_candidate(d, normalized=True)
    delta = add(q_quantum(d), scale(-1, projector(axis, outcome)))
    return delta[0][0].real ** 2 + delta[0][1].norm_squared()


trace_distance_squared_to_ray = quotient_trace_distance_squared_to_ray


def quotient_trace_norm_squared_to_ray(d: Matrix, axis: str, outcome: int) -> F:
    return 4 * quotient_trace_distance_squared_to_ray(d, axis, outcome)


def _settings(names: Iterable[str]) -> tuple[str, ...]:
    if isinstance(names, str):
        raise TypeError("A control word contains complete setting names, not a single string")
    names = tuple(names)
    if any(name not in CONTROLS for name in names):
        raise ValueError("The pending word contains an unavailable control")
    return names


@dataclass(frozen=True)
class Record:
    event_id: int
    axis: str
    outcome: int
    settings: tuple[str, ...]
    precursor: tuple[int, ...]
    domain: str
    controller: str = CONTROLLER
    frame: str = FRAME
    setting_id: str = NOMINAL_SETTING
    action: str = "pauli_record"

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("A record id must be a nonnegative integer")
        _axis(self.axis)
        _outcome(self.outcome)
        _domain(self.domain)
        _label(self.setting_id)
        if self.controller != CONTROLLER or self.frame != FRAME or self.action != "pauli_record":
            raise ValueError("Retain the fixed controller/frame and the full nominal Pauli action")
        precursor = tuple(self.precursor)
        if any(type(event) is not int for event in precursor) or precursor != tuple(
            range(self.event_id)
        ):
            raise ValueError("The chosen record precursor is the complete committed prefix")
        object.__setattr__(self, "precursor", precursor)
        object.__setattr__(self, "settings", _settings(self.settings))


def history(records: Iterable[Record], domain: str) -> tuple[Record, ...]:
    records, domain = tuple(records), _domain(domain)
    for i, record in enumerate(records):
        if not isinstance(record, Record) or record.event_id != i or record.domain != domain:
            raise ValueError(
                "Retain a complete same-domain prefix with fresh consecutive record ids"
            )
    return records


@dataclass(frozen=True)
class State:
    """Full raw residual in one explicit domain, with immutable nominal records.

    The constructor checks finite grammar and cone membership, not global
    reachability from earlier preparation. Epsilon/targets/model provenance are
    absent from record labels; a physically known changed setting_id is retained.
    """

    domain: str
    residual: Matrix
    records: tuple[Record, ...] = ()
    settings: tuple[str, ...] = ()
    controller: str = CONTROLLER
    frame: str = FRAME

    def __post_init__(self) -> None:
        _domain(self.domain)
        if self.controller != CONTROLLER or self.frame != FRAME:
            raise ValueError("Source states retain the fixed declared controller and frame")
        object.__setattr__(
            self, "residual", domain_kernel(self.residual, self.domain, normalized=True)
        )
        object.__setattr__(self, "records", history(self.records, self.domain))
        object.__setattr__(self, "settings", _settings(self.settings))


def _source(state: State) -> State:
    if not isinstance(state, State):
        raise TypeError("Only an explicitly typed robustness State has these continuations")
    return state


def run_control(state: State, name: str) -> State:
    state = _source(state)
    return State(
        state.domain,
        controls(state.residual, name),
        state.records,
        state.settings + (name,),
        state.controller,
        state.frame,
    )


def run_word(state: State, names: Iterable[str]) -> State:
    state = _source(state)
    for name in _settings(names):
        state = run_control(state, name)
    return state


def commit(
    state: State, instrument: Instrument | LocalCounterInstrument, outcome: int
) -> tuple[F, State]:
    """Apply a fixed-frame instrument to the current residual, then append once.

    Bounds comparing ideal/approximate models require the same complete nominal
    settings and retained-history alphabet. Distinct recorded setting_ids are
    not silently identified; model parameters alone do not invent new labels.
    """
    state, outcome = _source(state), _outcome(outcome)
    if not isinstance(instrument, (Instrument, LocalCounterInstrument)):
        raise TypeError("Use one of this bounded witness's declared instrument types")
    if instrument.domain != state.domain:
        raise ValueError("Instrument availability must match the explicitly declared source domain")
    output = instrument.branch(state.residual, outcome)
    probability = mass(output)
    if probability <= 0:
        raise ValueError("Cannot select, normalize or append a zero-probability branch")
    normalized = scale(1 / probability, output)
    records = state.records + (
        Record(
            len(state.records),
            instrument.axis,
            outcome,
            state.settings,
            tuple(range(len(state.records))),
            state.domain,
            state.controller,
            state.frame,
            instrument.setting_id,
        ),
    )
    return probability, State(state.domain, normalized, records, (), state.controller, state.frame)
