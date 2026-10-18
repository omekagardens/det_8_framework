"""Exact fixed-reference joint-recordability witness, with full raw residuals.

The local preparation cone, reference orientation, declared independence and
single shared coupling are additional premises. Product preparation does not
derive physical independence. Native labels are (a,i,b,j), regrouped labels are
(a,b,i,j). Prospective PSD kernels retain every raw entry even when they fail
joint recordability; only validated composites may commit a literal joint cut.
No target terminal residual is silently reused as a lawful composite source.
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

    This is an isolated local diagnostic helper, not a typed local operation or
    a physical-availability claim. The raw fixture calculation only needs PSD.
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


def tensor(left: Matrix, right: Matrix) -> Matrix:
    left, right = matrix(left), matrix(right)
    return tuple(
        tuple(a * b for a in left_row for b in right_row)
        for left_row in left
        for right_row in right
    )


def _bit(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError("A binary label must be exactly 0 or 1")
    return value


def index_native(a: int, i: int, b: int, j: int) -> int:
    a, i, b, j = (_bit(value) for value in (a, i, b, j))
    return 8 * a + 4 * i + 2 * b + j


def index_joint(a: int, b: int, i: int, j: int) -> int:
    a, b, i, j = (_bit(value) for value in (a, b, i, j))
    return 8 * a + 4 * b + 2 * i + j


JOINT_CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))
CROSS_PAIRS = tuple(
    (left, right) for n, left in enumerate(JOINT_CELLS) for right in JOINT_CELLS[n + 1 :]
)
NATIVE_TO_GROUPED = tuple(
    index_joint(a, b, i, j) for a in (0, 1) for i in (0, 1) for b in (0, 1) for j in (0, 1)
)
UNTWIST_LOCAL = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, -1)))
CNOT = matrix(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0)))
SHARED_U0 = matmul(tensor(identity(2), H0), CNOT)
IDENTITY_COUPLER = "identity"
SHARED_COUPLER = "shared_CNOT_H2"
PRODUCT_COUPLER = "product_H2"
# Typed availability includes only the single shared coupler. The raw product
# congruence remains a countercontrol calculation in coupler_spec/couple.
COUPLERS = (IDENTITY_COUPLER, SHARED_COUPLER)


def _sixteen(d: Matrix) -> Matrix:
    d = matrix(d)
    if len(d) != 16 or len(d[0]) != 16 or not is_hermitian(d):
        raise ValueError("Use a Hermitian full sixteen-label kernel")
    return d


def joint_kernel(d: Matrix, *, normalized: bool = False) -> Matrix:
    """Validate prospective full PSD data; this does not require recordability."""
    d = _sixteen(d)
    if not is_psd(d):
        raise ValueError("The full joint kernel must be PSD")
    if normalized and joint_mass(d) != 1:
        raise ValueError("A normalized joint kernel must have native total-entry mass one")
    return d


def regroup(d: Matrix) -> Matrix:
    d = _sixteen(d)
    inverse = tuple(NATIVE_TO_GROUPED.index(i) for i in range(16))
    return matrix(tuple(d[i][j] for j in inverse) for i in inverse)


def unregroup(d: Matrix) -> Matrix:
    d = _sixteen(d)
    return matrix(tuple(d[i][j] for j in NATIVE_TO_GROUPED) for i in NATIVE_TO_GROUPED)


def _untwist_native(d: Matrix) -> Matrix:
    d = _sixteen(d)
    signs = tuple(
        (-1) ** (a * i + b * j) for a in (0, 1) for i in (0, 1) for b in (0, 1) for j in (0, 1)
    )
    return matrix(tuple(signs[i] * d[i][j] * signs[j] for j in range(16)) for i in range(16))


def to_untwisted(d: Matrix) -> Matrix:
    """Native (a,i,b,j) -> untwisted/regrouped (a,b,i,j)."""
    return regroup(_untwist_native(d))


def from_untwisted(d: Matrix) -> Matrix:
    return _untwist_native(unregroup(d))


def untwist_local(d: Matrix) -> Matrix:
    d = _four(d)
    return matmul(matmul(UNTWIST_LOCAL, d), UNTWIST_LOCAL)


def reference_kernel(t: int | F) -> Matrix:
    t = rational(t)
    if abs(t) > 1:
        raise ValueError("The reference parameter must lie in [-1,1]")
    b = scale(F(1, 4), add(identity(2), scale(t, Z)))
    return candidate_from(b, 0, normalized=True)


def product_kernel(local: Matrix, reference: Matrix) -> Matrix:
    """Algebraic product of two supplied kernels, not a proof of independence."""
    local, reference = matrix(local), matrix(reference)
    decompose_candidate(local, normalized=True)
    decompose_candidate(reference, normalized=True)
    return tensor(local, reference)


def coupler_spec(name: str) -> tuple[Matrix, F]:
    """Internal four-coordinate numerator and congruence factor; catalogue only."""
    if name == IDENTITY_COUPLER:
        return identity(4), F(1)
    if name == SHARED_COUPLER:
        return SHARED_U0, F(1, 2)
    if name == PRODUCT_COUPLER:
        return tensor(identity(2), H0), F(1, 2)
    raise ValueError("Coupler is outside this fixed witness catalogue")


def couple(d: Matrix, name: str) -> Matrix:
    """Prospective raw PSD congruence, not permission to read an invalid result."""
    d = joint_kernel(d)
    internal, factor = coupler_spec(name)
    lifted = tensor(identity(4), internal)
    output = scale(factor, matmul(matmul(lifted, to_untwisted(d)), dagger(lifted)))
    return from_untwisted(output)


def shared_couple(d: Matrix) -> Matrix:
    return couple(d, SHARED_COUPLER)


def _cell(outcome: tuple[int, int]) -> tuple[int, int]:
    if not isinstance(outcome, tuple) or len(outcome) != 2:
        raise ValueError("A joint outcome must be the tuple (a,b)")
    return _bit(outcome[0]), _bit(outcome[1])


def cell_indices(outcome: tuple[int, int]) -> tuple[int, ...]:
    a, b = _cell(outcome)
    return tuple(index_native(a, i, b, j) for i in (0, 1) for j in (0, 1))


def joint_cross(d: Matrix, left: tuple[int, int], right: tuple[int, int]) -> G:
    d = _sixteen(d)
    return sum((d[i][j] for i in cell_indices(left) for j in cell_indices(right)), G())


def joint_crossforms(d: Matrix) -> tuple[G, ...]:
    d = _sixteen(d)
    return tuple(joint_cross(d, left, right) for left, right in CROSS_PAIRS)


def joint_weights(d: Matrix) -> RealVector:
    d = _sixteen(d)
    return tuple(joint_cross(d, cell, cell).real for cell in JOINT_CELLS)


def joint_mass(d: Matrix) -> F:
    d = _sixteen(d)
    return sum((entry.real for row in d for entry in row), F(0))


def joint_recordable(d: Matrix, *, normalized: bool = False) -> bool:
    d = _sixteen(d)
    return (
        is_psd(d)
        and all(value == 0 for value in joint_crossforms(d))
        and (not normalized or joint_mass(d) == 1)
    )


def joint_cut(d: Matrix, outcome: tuple[int, int]) -> Matrix:
    """Raw literal cell-cut matrix; no normalization, commitment or availability."""
    d = _sixteen(d)
    indices = cell_indices(outcome)
    return matrix(
        tuple(d[i][j] if i in indices and j in indices else 0 for j in range(16)) for i in range(16)
    )


def _name(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("Names and retained labels must be nonempty strings")
    return value


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
            raise ValueError("A local event id must be a nonnegative integer")
        _name(self.action)
        _name(self.outcome)
        if isinstance(self.settings, str):
            raise TypeError("Settings must be an immutable sequence of complete labels")
        settings = tuple(_name(setting) for setting in self.settings)
        payload = tuple(tuple(item) for item in self.payload)
        if any(
            len(item) != 2 or any(not isinstance(value, str) for value in item) for item in payload
        ):
            raise ValueError("Retained payload consists of immutable string key/value pairs")
        precursor = tuple(self.precursor)
        if any(
            type(event) is not int or event < 0 or event >= self.event_id for event in precursor
        ):
            raise ValueError("Local precursor ids must belong to the earlier same-origin prefix")
        if len(set(precursor)) != len(precursor):
            raise ValueError("A local precursor cannot list an event twice")
        object.__setattr__(self, "settings", settings)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "precursor", precursor)


def input_history(records: Iterable[InputRecord]) -> tuple[InputRecord, ...]:
    """Check each local prefix independently; infer no ordering between origins."""
    records = tuple(records)
    for i, record in enumerate(records):
        if not isinstance(record, InputRecord) or record.event_id != i:
            raise ValueError(
                "Each input history retains complete records with contiguous local ids"
            )
    return records


@dataclass(frozen=True)
class LocalState:
    residual: Matrix
    origin: str = "local"
    records: tuple[InputRecord, ...] = ()

    def __post_init__(self) -> None:
        _name(self.origin)
        d = matrix(self.residual)
        decompose_candidate(d, normalized=True)
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", input_history(self.records))


@dataclass(frozen=True)
class ReferenceState:
    t: F
    origin: str = "reference"
    records: tuple[InputRecord, ...] = ()
    orientation: str = "Z"
    residual: Matrix = field(init=False)

    def __post_init__(self) -> None:
        _name(self.origin)
        t = rational(self.t)
        if self.orientation != "Z":
            raise ValueError("Only the explicitly supplied reference Z orientation is declared")
        object.__setattr__(self, "t", t)
        object.__setattr__(self, "residual", reference_kernel(t))
        object.__setattr__(self, "records", input_history(self.records))


@dataclass(frozen=True)
class Independence:
    """An explicit named premise, not something certified by matrices or names."""

    origins: tuple[str, str]

    def __post_init__(self) -> None:
        if isinstance(self.origins, str):
            raise TypeError("Independence must explicitly name both distinct origins")
        origins = tuple(self.origins)
        if len(origins) != 2 or origins[0] == origins[1]:
            raise ValueError("Independence must explicitly name two distinct origins")
        for origin in origins:
            _name(origin)
        object.__setattr__(self, "origins", origins)


@dataclass(frozen=True)
class ProspectiveState:
    """Full algebraic PSD snapshot, even when committing records would be illegal.

    Validation checks finite metadata/cone grammar, not global reachability of
    a hand-supplied snapshot or the empirical truth of declared independence.
    prepare_joint/couple_state construct the specified forward transformation.
    """

    residual: Matrix
    local: LocalState
    reference: ReferenceState
    independence: Independence
    coupler: str = IDENTITY_COUPLER
    joint_origin: str = "joint"
    permutation: tuple[int, ...] = NATIVE_TO_GROUPED

    def __post_init__(self) -> None:
        if not isinstance(self.local, LocalState) or not isinstance(self.reference, ReferenceState):
            raise TypeError("Both separately labeled local/reference inputs must be retained")
        if not isinstance(self.independence, Independence):
            raise TypeError("An explicit independence declaration is required")
        if set(self.independence.origins) != {self.local.origin, self.reference.origin}:
            raise ValueError("Independence must name exactly the two retained input origins")
        _name(self.joint_origin)
        if self.joint_origin in self.independence.origins:
            raise ValueError("The new joint record uses its own distinct origin")
        if self.coupler not in COUPLERS:
            raise ValueError("Retain the actual declared coupler name")
        permutation = tuple(self.permutation)
        if permutation != NATIVE_TO_GROUPED:
            raise ValueError("Retain the exact native-to-grouped label permutation")
        object.__setattr__(self, "residual", joint_kernel(self.residual))
        # Preserve compatible numeric input, but store canonical integer labels.
        object.__setattr__(self, "permutation", NATIVE_TO_GROUPED)


@dataclass(frozen=True)
class CompositeState(ProspectiveState):
    """Lawful source: full PSD, six complex cross forms zero, native mass one."""

    def __post_init__(self) -> None:
        super().__post_init__()
        if not joint_recordable(self.residual, normalized=True):
            raise ValueError("Composite source must be exactly jointly recordable and normalized")


def prepare_joint(
    local: LocalState,
    reference: ReferenceState,
    independence: Independence,
    *,
    joint_origin: str = "joint",
) -> ProspectiveState:
    if not isinstance(local, LocalState) or not isinstance(reference, ReferenceState):
        raise TypeError("Supply separately typed local and reference inputs")
    return ProspectiveState(
        product_kernel(local.residual, reference.residual),
        local,
        reference,
        independence,
        joint_origin=joint_origin,
    )


def promote_joint(prospective: ProspectiveState) -> CompositeState:
    if not isinstance(prospective, ProspectiveState):
        raise TypeError("Only a retained prospective snapshot can undergo source validation")
    return CompositeState(
        prospective.residual,
        prospective.local,
        prospective.reference,
        prospective.independence,
        prospective.coupler,
        prospective.joint_origin,
        prospective.permutation,
    )


def _source(state: CompositeState) -> CompositeState:
    if not isinstance(state, CompositeState):
        raise TypeError("Only an exactly recordable CompositeState is a lawful joint source")
    return state


def couple_state(state: CompositeState, name: str = SHARED_COUPLER) -> ProspectiveState:
    state = _source(state)
    if state.coupler != IDENTITY_COUPLER or name != SHARED_COUPLER:
        raise ValueError(
            "The typed witness permits exactly one shared coupler from the initial product source"
        )
    return ProspectiveState(
        couple(state.residual, name),
        state.local,
        state.reference,
        state.independence,
        name,
        state.joint_origin,
        state.permutation,
    )


def full_precursor(state: CompositeState) -> tuple[tuple[str, int], ...]:
    """List both full prefixes by origin; tuple order is not cross-origin causal order."""
    state = _source(state)
    return tuple(
        (input_state.origin, record.event_id)
        for input_state in (state.local, state.reference)
        for record in input_state.records
    )


@dataclass(frozen=True)
class JointRecord:
    event_id: int
    origin: str
    outcome: tuple[int, int]
    precursor: tuple[tuple[str, int], ...]
    coupler: str
    reference_t: F
    reference_orientation: str
    input_origins: tuple[str, str]
    local_records: tuple[InputRecord, ...]
    reference_records: tuple[InputRecord, ...]
    independence: Independence
    permutation: tuple[int, ...] = NATIVE_TO_GROUPED
    action: str = "terminal_joint_cell_cut"

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id != 0:
            raise ValueError(
                "The first joint commitment uses fresh event id zero in its new origin"
            )
        _name(self.origin)
        _cell(self.outcome)
        input_origins = tuple(self.input_origins)
        if len(input_origins) != 2 or len(set(input_origins)) != 2 or self.origin in input_origins:
            raise ValueError("Retain two distinct input origins and the new joint origin")
        for origin in input_origins:
            _name(origin)
        if not isinstance(self.independence, Independence) or set(self.independence.origins) != set(
            input_origins
        ):
            raise ValueError("Retain the matching explicit independence declaration")
        local_records = input_history(self.local_records)
        reference_records = input_history(self.reference_records)
        expected = tuple(
            (origin, record.event_id)
            for origin, records in zip(
                input_origins, (local_records, reference_records), strict=True
            )
            for record in records
        )
        if tuple(self.precursor) != expected:
            raise ValueError("The joint precursor must retain every input record with its origin")
        if self.coupler not in COUPLERS or self.reference_orientation != "Z":
            raise ValueError("Retain the actual coupler and fixed reference orientation")
        reference_t = rational(self.reference_t)
        if abs(reference_t) > 1 or self.action != "terminal_joint_cell_cut":
            raise ValueError("Retain the valid reference parameter and complete joint action")
        permutation = tuple(self.permutation)
        if permutation != NATIVE_TO_GROUPED:
            raise ValueError("Retain the exact label permutation")
        object.__setattr__(self, "reference_t", reference_t)
        object.__setattr__(self, "input_origins", input_origins)
        object.__setattr__(self, "local_records", local_records)
        object.__setattr__(self, "reference_records", reference_records)
        object.__setattr__(self, "precursor", expected)
        # Equality above validates the mapping; input scalar types are not kept.
        object.__setattr__(self, "permutation", NATIVE_TO_GROUPED)


def _record_for(state: CompositeState, outcome: tuple[int, int]) -> JointRecord:
    return JointRecord(
        0,
        state.joint_origin,
        outcome,
        full_precursor(state),
        state.coupler,
        state.reference.t,
        state.reference.orientation,
        (state.local.origin, state.reference.origin),
        state.local.records,
        state.reference.records,
        state.independence,
        state.permutation,
    )


@dataclass(frozen=True)
class TerminalState:
    residual: Matrix
    source: CompositeState
    record: JointRecord

    def __post_init__(self) -> None:
        source = _source(self.source)
        if not isinstance(self.record, JointRecord) or self.record != _record_for(
            source, self.record.outcome
        ):
            raise ValueError(
                "Terminal output must retain the full matching joint commitment record"
            )
        selected = joint_cut(source.residual, self.record.outcome)
        probability = joint_mass(selected)
        if probability <= 0:
            raise ValueError("Cannot construct a terminal state for a zero-probability source cut")
        d = joint_kernel(self.residual, normalized=True)
        if d != scale(1 / probability, selected):
            raise ValueError("Terminal residual must be the actual positive-probability source cut")
        object.__setattr__(self, "residual", d)

    @property
    def records(self) -> tuple[JointRecord, ...]:
        return (self.record,)


def commit_joint(state: CompositeState, outcome: tuple[int, int]) -> tuple[F, TerminalState]:
    """Commit only after exact source validation, then retain the full literal cut.

    The joint precursor joins both labeled prefixes without asserting an order
    between the independent inputs. Bad recordability cannot be repaired by
    renormalizing a selected outcome, and zero mass refuses before append.
    """
    state, outcome = _source(state), _cell(outcome)
    output = joint_cut(state.residual, outcome)
    probability = joint_mass(output)
    if probability <= 0:
        raise ValueError("Cannot select, normalize or append a zero-probability joint branch")
    normalized = scale(1 / probability, output)
    return probability, TerminalState(normalized, state, _record_for(state, outcome))
