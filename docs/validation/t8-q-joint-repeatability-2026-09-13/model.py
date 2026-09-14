"""Exact same-image joint-return witnesses on the fixed c=0 sixteen-label family.

The fixed reference, initial independent product and shared-coupler frame are
declared premises. Reusable return maps below are additional algebraic
availability, not RI08d terminal cuts, re-preparing a reference, or reapplying a
coupler after each record. Every current kernel retains all native raw entries.
Exact inverse validation rejects outsiders instead of silently projecting them.
Fine (a,b) records remain complete when a later question asks only about b.
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
CONTROLLER = "joint_return_controller"
NOMINAL_RETURN = "same_image_joint_return"


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


def image_span(rho: Matrix, t: int | F) -> Matrix:
    """The real-linear K_t image map on arbitrary signed Hermitian rho."""
    rho, t = _hermitian(rho, 2), _t(t)
    a, b = scale(F(1, 2), transpose(rho)), scale(F(1, 2), reference_rho(t))
    block = scale(F(1, 2), matmul(matmul(U0, tensor(a, b)), dagger(U0)))
    return from_untwisted(tensor(identity(4), block))


def image(rho: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    rho = _hermitian(rho, 2)
    if not is_psd(rho):
        raise ValueError("Positive image input must be PSD")
    if normalized and trace(rho) != 1:
        raise ValueError("Normalized image input requires trace(rho)=1")
    return image_span(rho, t)


def inverse_span(d: Matrix, t: int | F) -> Matrix:
    """Recover rho and compare ALL sixteen-label entries with its fixed-t image.

    This is an inverse-domain test, not a partial-trace projection that admits
    arbitrary outsiders. The trace of the reference block is always 1/2, so
    the recovery works at t=0 and both pure-reference endpoints without division
    by 1+t or 1-t.
    """
    d, t = _hermitian(d, 16), _t(t)
    untwisted = to_untwisted(d)
    first = matrix(row[:4] for row in untwisted[:4])
    before = scale(F(1, 2), matmul(matmul(dagger(U0), first), U0))
    partial = matrix(
        tuple(sum((before[2 * i + j][2 * k + j] for j in (0, 1)), G()) for k in (0, 1))
        for i in (0, 1)
    )
    rho = scale(4, transpose(partial))
    if image_span(rho, t) != d:
        raise ValueError("Raw kernel is outside the exact fixed-reference sixteen-label image")
    return rho


def inverse_image(d: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    rho = inverse_span(d, t)
    if not is_psd(rho):
        raise ValueError("The exact image inverse must lie in the positive cone")
    if normalized and trace(rho) != 1:
        raise ValueError("Normalized image states require input mass one")
    return rho


def image_kernel(d: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    """Exact full-image validation; positivity follows from the reconstructed PSD input."""
    d = matrix(d)
    inverse_image(d, t, normalized=normalized)
    return d


def from_local(d: Matrix, t: int | F, *, normalized: bool = False) -> Matrix:
    rho, c = decompose_local(d, normalized=normalized)
    if c != 0:
        raise ValueError("This fixed image starts at c=0; nonzero c is rejected, never erased")
    return image(rho, t, normalized=normalized)


def quotient_on_span(d: Matrix, t: int | F) -> Matrix:
    rho = inverse_span(d, t)
    # U is real here. This is conjugate(U) (rho tensor rho_t) transpose(U).
    return scale(F(1, 2), matmul(matmul(U0, tensor(rho, reference_rho(t))), transpose(U0)))


def quotient(d: Matrix, t: int | F) -> Matrix:
    d = image_kernel(d, t)
    return quotient_on_span(d, t)


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
    """Native total-entry mass; equality with trace is guaranteed on the stated image."""
    d = _hermitian(d, 16)
    return sum((entry.real for row in d for entry in row), F(0))


def raw_cell_cut(d: Matrix, outcome: tuple[int, int]) -> Matrix:
    """A diagnostic literal cut, with no return-map or reusable-state authorization."""
    d = _hermitian(d, 16)
    indices = cell_indices(outcome)
    return matrix(
        tuple(d[i][j] if i in indices and j in indices else 0 for j in range(16)) for i in range(16)
    )


def pulled_effect(t: int | F, outcome: tuple[int, int]) -> Matrix:
    _, b = _cell(outcome)
    return scale(F(1, 4), add(identity(2), scale((-1) ** b * _t(t), Z)))


def pulled_b_effect(t: int | F, b: int) -> Matrix:
    return scale(2, pulled_effect(t, (0, _bit(b))))


def effect_on_span(d: Matrix, t: int | F, outcome: tuple[int, int]) -> F:
    d = matrix(d)
    inverse_span(d, t)
    return raw_cross(d, _cell(outcome), outcome).real


def b_effect_on_span(d: Matrix, t: int | F, b: int) -> F:
    d, b = matrix(d), _bit(b)
    inverse_span(d, t)
    return sum((raw_cross(d, (a, b), (a, b)).real for a in (0, 1)), F(0))


def fine_relative_floor(t: int | F) -> F:
    return (3 - abs(_t(t))) / 4


def b_relative_floor(t: int | F) -> F:
    return (1 - abs(_t(t))) / 2


def fine_input_mass_floor(t: int | F) -> F:
    p_f = (1 + abs(_t(t))) / 4
    return p_f * (1 - p_f)


def b_after_fine_input_mass_floor(t: int | F) -> F:
    """Next-b failure following ONE retained fine (a,b) first branch."""
    t = _t(t)
    return (1 - t * t) / 8


def b_after_summed_b_input_mass_floor(t: int | F) -> F:
    """Algebraically summed first-b branch; not erasure of an actual first a record."""
    t = _t(t)
    return (1 - t * t) / 4


def optimal_target_rho(t: int | F, outcome: tuple[int, int]) -> Matrix:
    t, (_, b) = _t(t), _cell(outcome)
    if t == 0:
        # A chosen witness, not a claim that every optimal branch resets at t=0.
        return scale(F(1, 2), identity(2))
    alignment = 1 if (-1) ** b * t > 0 else -1
    return scale(F(1, 2), add(identity(2), scale(alignment, Z)))


@dataclass(frozen=True)
class ReturnInstrument:
    """Four supplied same-image algebraic return maps q_ab(N)*h_ab.

    This witnesses optimal targets when requested; it does not classify every
    calibrated positive instrument as a reset. In particular t=0 has other
    optimal maps. Availability is additional, not inferred from terminal cuts.
    """

    t: F
    targets: tuple[Matrix, ...]
    setting_id: str = NOMINAL_RETURN
    provenance: str = "declared same-image return targets"
    orientation: str = "Z"
    coupler: str = SHARED_COUPLER
    frame: str = FRAME

    def __post_init__(self) -> None:
        t = _t(self.t)
        _name(self.setting_id)
        _name(self.provenance)
        if self.orientation != "Z" or self.coupler != SHARED_COUPLER or self.frame != FRAME:
            raise ValueError("Return instrument must retain the fixed reference/coupler frame")
        targets = tuple(image_kernel(target, t, normalized=True) for target in self.targets)
        if len(targets) != 4:
            raise ValueError("Retain one full normalized same-image target per fine outcome")
        object.__setattr__(self, "t", t)
        object.__setattr__(self, "targets", targets)

    def branch_on_span(self, d: Matrix, outcome: tuple[int, int]) -> Matrix:
        d, outcome = matrix(d), _cell(outcome)
        weight = effect_on_span(d, self.t, outcome)
        return scale(weight, self.targets[JOINT_CELLS.index(outcome)])

    def branch(self, d: Matrix, outcome: tuple[int, int]) -> Matrix:
        d = image_kernel(d, self.t)
        return self.branch_on_span(d, outcome)


def optimal_instrument(t: int | F, *, setting_id: str = NOMINAL_RETURN) -> ReturnInstrument:
    t = _t(t)
    return ReturnInstrument(
        t,
        tuple(image(optimal_target_rho(t, outcome), t, normalized=True) for outcome in JOINT_CELLS),
        setting_id,
        "aligned Z-ray optimal witnesses; center explicitly chosen at t=0",
    )


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
            raise ValueError("The fixed joint image accepts only explicit c=0 local inputs")
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
    """Immutable initial origins and the fixed image/return-setting contract.

    Keeping the original reference/input objects is provenance, not a claim
    that each later return prepares them again or applies the shared gate anew.
    """

    local: LocalInput
    reference: ReferenceInput
    independence: Independence
    joint_origin: str = "joint"
    coupler: str = SHARED_COUPLER
    frame: str = FRAME
    controller: str = CONTROLLER
    setting_id: str = NOMINAL_RETURN
    permutation: tuple[int, ...] = NATIVE_TO_GROUPED

    def __post_init__(self) -> None:
        if not isinstance(self.local, LocalInput) or not isinstance(self.reference, ReferenceInput):
            raise TypeError("Retain both complete separately typed initial inputs")
        if not isinstance(self.independence, Independence):
            raise TypeError("An explicit named initial-independence premise is required")
        if set(self.independence.origins) != {self.local.origin, self.reference.origin}:
            raise ValueError("Independence must name exactly the retained input origins")
        _name(self.joint_origin)
        _name(self.setting_id)
        if self.joint_origin in self.independence.origins:
            raise ValueError("The joint process uses a distinct origin")
        if self.coupler != SHARED_COUPLER or self.frame != FRAME or self.controller != CONTROLLER:
            raise ValueError("Retain the actual fixed shared coupler, frame and return controller")
        permutation = tuple(self.permutation)
        if any(type(label) is not int for label in permutation) or permutation != NATIVE_TO_GROUPED:
            raise ValueError("Permutation labels must be the exact built-in native-index integers")
        object.__setattr__(self, "permutation", permutation)

    @property
    def t(self) -> F:
        return self.reference.t


def _context(context: Context) -> Context:
    if not isinstance(context, Context):
        raise TypeError("Use a fully retained fixed-image Context")
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


@dataclass(frozen=True)
class JointRecord:
    event_id: int
    outcome: tuple[int, int]
    precursor: tuple[tuple[str, int], ...]
    context: Context
    action: str = "same_image_joint_return"

    def __post_init__(self) -> None:
        context = _context(self.context)
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("Joint record ids must be nonnegative built-in integers")
        _cell(self.outcome)
        if self.action != "same_image_joint_return":
            raise ValueError("Retain the actual same-image nominal return action")
        precursor = tuple(tuple(item) for item in self.precursor)
        if any(
            len(item) != 2 or not isinstance(item[0], str) or type(item[1]) is not int
            for item in precursor
        ):
            raise ValueError("Every predecessor retains an origin and a built-in event id")
        if precursor != complete_precursor(context, self.event_id):
            raise ValueError("Retain both complete input prefixes and every previous joint record")
        object.__setattr__(self, "precursor", precursor)

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
    """Full current raw image with immutable complete initial and joint histories.

    Snapshot validation checks grammar and exact image membership, not global
    reachability. No factor or history is replaced by its coarse question value.
    """

    context: Context
    residual: Matrix
    records: tuple[JointRecord, ...] = ()

    def __post_init__(self) -> None:
        context = _context(self.context)
        d = image_kernel(self.residual, context.t, normalized=True)
        records = tuple(self.records)
        for i, record in enumerate(records):
            if (
                not isinstance(record, JointRecord)
                or record.event_id != i
                or record.context != context
            ):
                raise ValueError(
                    "Retain a complete sequential joint prefix in this unchanged context"
                )
        object.__setattr__(self, "residual", d)
        object.__setattr__(self, "records", records)

    @property
    def t(self) -> F:
        return self.context.t


def prepare_state(
    local: LocalInput,
    reference: ReferenceInput,
    independence: Independence,
    *,
    joint_origin: str = "joint",
    setting_id: str = NOMINAL_RETURN,
) -> State:
    context = Context(
        local, reference, independence, joint_origin=joint_origin, setting_id=setting_id
    )
    return State(context, from_local(local.residual, reference.t, normalized=True))


def _source(state: State) -> State:
    if not isinstance(state, State):
        raise TypeError("Only a complete same-image State has these declared return operations")
    return state


def _question(question: str) -> str:
    if question not in ("fine", "b"):
        raise ValueError("Ask either the full fine outcome or only its b component")
    return question


def record_answer(record: JointRecord, question: str = "fine") -> tuple[int, int] | int:
    """Read-only question about a full retained record; never rewrite that record."""
    if not isinstance(record, JointRecord):
        raise TypeError("A record question requires the complete JointRecord")
    return record.outcome if _question(question) == "fine" else record.outcome[1]


def next_question_probability(state: State, outcome: tuple[int, int], question: str = "fine") -> F:
    """Probability of a question about the NEXT full record in the fixed context."""
    state, outcome, question = _source(state), _cell(outcome), _question(question)
    if question == "fine":
        return effect_on_span(state.residual, state.t, outcome)
    return b_effect_on_span(state.residual, state.t, outcome[1])


def commit(state: State, instrument: ReturnInstrument, outcome: tuple[int, int]) -> tuple[F, State]:
    """Apply an additional same-image return directly; retain the full fine record.

    This operation is not a terminal cell cut plus an inferred reference reset
    or repeated coupler. Fine/b questions change no branch label or prior record.
    """
    state, outcome = _source(state), _cell(outcome)
    if not isinstance(instrument, ReturnInstrument):
        raise TypeError("Use this bounded witness's declared same-image return instrument")
    context = state.context
    if (
        instrument.t != context.t
        or instrument.orientation != context.reference.orientation
        or instrument.coupler != context.coupler
        or instrument.frame != context.frame
        or instrument.setting_id != context.setting_id
    ):
        raise ValueError("Instrument must match the entire fixed reference/frame/nominal context")
    output = instrument.branch(state.residual, outcome)
    probability = raw_mass(output)
    if probability <= 0:
        raise ValueError("Cannot normalize or append a zero-probability return branch")
    record = JointRecord(
        len(state.records), outcome, complete_precursor(context, len(state.records)), context
    )
    return probability, State(context, scale(1 / probability, output), state.records + (record,))


commit_joint = commit
