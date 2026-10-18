"""Exact finite classical witness for first-commit elimination and quotient descent.

The supplied controller has two modes, each with bright and dark residual
coordinates. Global columns are (b0, d0, b1, d1); mixtures include classical
uncertainty about the unobserved controller. A silent step halves bright mass
and swaps dark modes. Commits retain their full source/action/outcome/target
label and residual. No silent-controller path is written into the record.

These are chosen finite maps, not a DET selection theorem, physical clock,
QM reconstruction, or general-purpose process SDK. All arithmetic is rational.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction

F = Fraction
Vector = tuple[F, ...]
Matrix = tuple[Vector, ...]


def _rational(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Use exact integers or Fractions, not floats or booleans")
    return F(value)


def _count(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("A count must be a nonnegative integer")
    return value


def _mode(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError("A controller mode must be exactly 0 or 1")
    return value


def vector(values: Iterable[int | F]) -> Vector:
    result = tuple(_rational(value) for value in values)
    if not result:
        raise ValueError("Empty vectors are not used in this finite witness")
    return result


def matrix(rows: Iterable[Iterable[int | F]]) -> Matrix:
    result = tuple(vector(row) for row in rows)
    if not result or any(len(row) != len(result[0]) for row in result):
        raise ValueError("A matrix must be nonempty and rectangular")
    return result


def dot(left: Vector, right: Vector) -> F:
    return sum((a * b for a, b in zip(left, right, strict=True)), F(0))


def mass(x: Vector) -> F:
    return sum(x, F(0))


def coordinates(values: Iterable[int | F], *, normalized: bool = False) -> Vector:
    result = vector(values)
    if len(result) != 4 or any(value < 0 for value in result):
        raise ValueError("Residuals must lie in the four-coordinate positive cone")
    if normalized and mass(result) != 1:
        raise ValueError("A normalized residual must have mass one")
    return result


def zero(rows: int, columns: int | None = None) -> Matrix:
    columns = rows if columns is None else columns
    if _count(rows) == 0 or _count(columns) == 0:
        raise ValueError("Matrix dimensions must be positive")
    return matrix((0,) * columns for _ in range(rows))


def identity(size: int) -> Matrix:
    if _count(size) == 0:
        raise ValueError("Matrix dimension must be positive")
    return matrix(tuple(int(i == j) for j in range(size)) for i in range(size))


def matvec(a: Matrix, x: Vector) -> Vector:
    a = matrix(a)
    x = vector(x)
    if len(a[0]) != len(x):
        raise ValueError("Matrix/vector dimensions do not match")
    return tuple(dot(row, x) for row in a)


def rowmat(effect: Vector, a: Matrix) -> Vector:
    a = matrix(a)
    effect = vector(effect)
    if len(effect) != len(a):
        raise ValueError("Effect/matrix dimensions do not match")
    return tuple(dot(effect, tuple(row[j] for row in a)) for j in range(len(a[0])))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    a, b = matrix(a), matrix(b)
    if len(a[0]) != len(b):
        raise ValueError("Matrix dimensions do not match")
    columns = tuple(zip(*b, strict=True))
    return tuple(tuple(dot(row, column) for column in columns) for row in a)


def matadd(*operators: Matrix) -> Matrix:
    if not operators:
        raise ValueError("Supply at least one matrix")
    operators = tuple(matrix(a) for a in operators)
    rows, columns = len(operators[0]), len(operators[0][0])
    if any(len(a) != rows or len(a[0]) != columns for a in operators):
        raise ValueError("Matrix dimensions do not match")
    return tuple(
        tuple(sum((a[i][j] for a in operators), F(0)) for j in range(columns)) for i in range(rows)
    )


def scale(coefficient: int | F, a: Matrix) -> Matrix:
    coefficient, a = _rational(coefficient), matrix(a)
    return tuple(tuple(coefficient * entry for entry in row) for row in a)


def matpow(a: Matrix, exponent: int) -> Matrix:
    a = matrix(a)
    exponent = _count(exponent)
    if len(a) != len(a[0]):
        raise ValueError("Only square matrices have powers here")
    output = identity(len(a))
    while exponent:
        if exponent % 2:
            output = matmul(output, a)
        a = matmul(a, a)
        exponent //= 2
    return output


UNIT = vector((1, 1, 1, 1))
S = matrix(((F(1, 2), 0, 0, 0), (0, 0, 0, 1), (0, 0, F(1, 2), 0), (0, 1, 0, 0)))
B0 = matrix(((F(1, 2), 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)))
B1 = matrix(((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, F(1, 2), 0), (0, 0, 0, 0)))
H0 = scale(2, B0)
H1 = scale(2, B1)


@dataclass(frozen=True)
class Label:
    """Full committing label before attaching the chosen actual precursor."""

    source: int
    action: str
    outcome: str
    target: int

    def __post_init__(self) -> None:
        _mode(self.source)
        _mode(self.target)
        if self.action != "attempt" or self.outcome != str(self.source):
            raise ValueError("This witness registers only attempt outcomes 0 and 1")
        if self.target != self.source:
            raise ValueError("The supplied commit branch retains its source mode")


LABELS = (Label(0, "attempt", "0", 0), Label(1, "attempt", "1", 1))


@dataclass(frozen=True)
class Branch:
    """A typed local 2-by-2 positive branch before direct-sum embedding.

    Silent entries have outcome epsilon, not a committed null outcome.
    These are internal paths, not individually observable/controllable tests.
    The aggregate S deliberately forgets which silent typed branch occurred;
    the quotient is invalid if the dark mode or a singled-out edge is read.
    """

    source: int
    target: int
    operator: Matrix
    commits: bool
    action: str = "attempt"
    outcome: str = "epsilon"

    def __post_init__(self) -> None:
        _mode(self.source)
        _mode(self.target)
        operator = matrix(self.operator)
        if len(operator) != 2 or len(operator[0]) != 2:
            raise ValueError("Each local mode has two coordinates")
        if any(entry < 0 for row in operator for entry in row):
            raise ValueError("Local branch maps must be positive")
        if any(value > 1 for value in rowmat(vector((1, 1)), operator)):
            raise ValueError("A local branch cannot increase mass")
        if type(self.commits) is not bool or self.action != "attempt":
            raise ValueError("Use the supplied attempt branch grammar")
        if self.commits:
            Label(self.source, self.action, self.outcome, self.target)
        elif self.outcome != "epsilon":
            raise ValueError("Silent branches cannot carry a recorded outcome")
        object.__setattr__(self, "operator", operator)

    @property
    def label(self) -> Label | None:
        if not self.commits:
            return None
        return Label(self.source, self.action, self.outcome, self.target)


BRANCHES = tuple(
    branch
    for mode in (0, 1)
    for branch in (
        Branch(mode, mode, matrix(((F(1, 2), 0), (0, 0))), False),
        Branch(mode, 1 - mode, matrix(((0, 0), (0, 1))), False),
        Branch(mode, mode, matrix(((F(1, 2), 0), (0, 0))), True, outcome=str(mode)),
    )
)


def embed(branch: Branch) -> Matrix:
    """Embed a typed local map; construction alone does not register a law."""
    output = [[F(0) for _ in range(4)] for _ in range(4)]
    for i in range(2):
        for j in range(2):
            output[2 * branch.target + i][2 * branch.source + j] = branch.operator[i][j]
    return matrix(output)


def aggregate_branches(branches: Iterable[Branch]) -> Matrix:
    return matadd(zero(4), *(embed(branch) for branch in branches))


def first_commit_at(n: int) -> tuple[Matrix, Matrix]:
    """Exactly n silent interactions followed by a labeled first commit."""
    power = matpow(S, n)
    return matmul(B0, power), matmul(B1, power)


def first_commit_prefix(count: int) -> tuple[Matrix, Matrix]:
    """Sum n=0,...,count-1, retaining both full committing labels separately."""
    count = _count(count)
    power, h0, h1 = identity(4), zero(4), zero(4)
    for _ in range(count):
        h0 = matadd(h0, matmul(B0, power))
        h1 = matadd(h1, matmul(B1, power))
        power = matmul(S, power)
    return h0, h1


def never_mass(x: Iterable[int | F]) -> F:
    x = coordinates(x)
    return x[1] + x[3]


@dataclass(frozen=True)
class Record:
    event_id: int
    label: Label
    precursor: tuple[int, ...]

    def __post_init__(self) -> None:
        _count(self.event_id)
        if not isinstance(self.label, Label):
            raise TypeError("A record retains a full committing Label")
        if not isinstance(self.precursor, tuple):
            raise TypeError("The immutable precursor must be a tuple")
        for event in self.precursor:
            _count(event)


def history(records: Iterable[Record]) -> tuple[Record, ...]:
    """Validate the chosen full-prefix chain grammar, not global reachability."""
    result = tuple(records)
    for i, record in enumerate(result):
        if not isinstance(record, Record):
            raise TypeError("Committed history consists of Record values")
        if record.event_id != i or record.precursor != tuple(range(i)):
            raise ValueError("Records use fresh consecutive ids and the entire earlier prefix")
    return result


@dataclass(frozen=True)
class State:
    residual: Vector
    records: tuple[Record, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "residual", coordinates(self.residual, normalized=True))
        object.__setattr__(self, "records", history(self.records))


def append_record(records: Iterable[Record], label: Label) -> tuple[Record, ...]:
    """Structural helper only: caller must have selected a positive-mass commit.

    apply_commit and apply_first_commit perform the residual-dependent guard.
    This helper cannot infer probability, physical availability, or the past
    residual trajectory.
    """
    records = history(records)
    if label not in LABELS:
        raise ValueError("Only registered complete labels may be appended")
    return records + (Record(len(records), label, tuple(range(len(records)))),)


def _selected(state: State, operator: Matrix) -> tuple[F, Vector]:
    if not isinstance(state, State):
        raise TypeError("Branch selection requires a validated State")
    output = matvec(operator, state.residual)
    probability = mass(output)
    if probability <= 0:
        raise ValueError("Cannot select or normalize a zero-probability branch")
    return probability, tuple(value / probability for value in output)


def apply_silent(state: State) -> tuple[F, State]:
    """Condition on no commit; retain dark-mode mixture, write no null record."""
    probability, residual = _selected(state, S)
    return probability, State(residual, state.records)


def apply_commit(state: State, mode: int) -> tuple[F, State]:
    mode = _mode(mode)
    probability, residual = _selected(state, (B0, B1)[mode])
    return probability, State(residual, append_record(state.records, LABELS[mode]))


def apply_first_commit(state: State, mode: int) -> tuple[F, State]:
    """Select an eventual labeled first commit, forgetting its silent prefix.

    H retains the committing residual and complete label. A never-commit mass
    is complementary probability, not a newly committed terminal record or a
    residual limit; no such terminal State is constructed here.
    """
    mode = _mode(mode)
    probability, residual = _selected(state, (H0, H1)[mode])
    return probability, State(residual, append_record(state.records, LABELS[mode]))


# Only the dark internal controller phase is forgotten. The observed interface
# comprises aggregate S, B0, B1 and terminal mass, not individual silent edges.
# This is not a quotient of distinct externally known apparatus settings.
Q = matrix(((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 1)))
S_BAR = matrix(((F(1, 2), 0, 0), (0, F(1, 2), 0), (0, 0, 1)))
B0_BAR = matrix(((F(1, 2), 0, 0), (0, 0, 0), (0, 0, 0)))
B1_BAR = matrix(((0, 0, 0), (0, F(1, 2), 0), (0, 0, 0)))
QUOTIENT_UNIT = vector((1, 1, 1))


def project(x: Iterable[int | F]) -> Vector:
    return matvec(Q, coordinates(x))


def descend_map(operator: Matrix) -> Matrix:
    """Return the unique induced map iff the dark-phase kernel is invariant.

    This exact linear test alone makes no positivity or physical-availability
    claim. If operator preserves the declared positive cone, the induced map
    preserves its image cone, which in this particular example is R_+^3.
    """
    operator = matrix(operator)
    if len(operator) != 4 or len(operator[0]) != 4:
        raise ValueError("This quotient helper accepts four-coordinate maps")
    q_operator = matmul(Q, operator)
    induced = matrix(tuple(row[j] for j in (0, 2, 1)) for row in q_operator)
    if matmul(induced, Q) != q_operator:
        raise ValueError("Map does not descend: a forgotten difference becomes predictive")
    return induced


def descend_effect(effect: Iterable[int | F]) -> Vector:
    effect = vector(effect)
    if len(effect) != 4 or effect[1] != effect[3]:
        raise ValueError("Terminal effect distinguishes the forgotten dark controller phase")
    return vector((effect[0], effect[2], effect[1]))
