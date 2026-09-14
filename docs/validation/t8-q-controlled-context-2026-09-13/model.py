"""Exact chosen controlled-process witness, not a DET-selected physical law.

The four nonnegative coordinates form a classical cone. Its two embeddings are
coherent real pair kernels, not an enlargement to all positive kernels or a
reconstruction of quantum mechanics. All preparations, available actions, mode
control, and chain-append precursors below are supplied premises.

No random sampling, physical clock, RET interface, or implicit record production
is used. A silent branch leaves the committed history unchanged. Future-effect
closure concerns lawful finite controlled branch cylinders; their protocol
boundaries are supplied tests, not physical timestamps or additional records.
"""

from collections.abc import Iterable
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType

F = Fraction
Vector = tuple[F, F, F, F]
Matrix = tuple[Vector, Vector, Vector, Vector]
MODES = ("P", "Q")
UNIT: Vector = (F(1), F(1), F(1), F(1))
ZERO: Vector = (F(0), F(0), F(0), F(0))
PARTITIONS = MappingProxyType({"P": ((0, 1), (2, 3)), "Q": ((0, 2), (1, 3))})


def _rational(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Use exact integers or Fractions, not floats or booleans")
    return F(value)


def _mode(mode: str) -> str:
    if mode not in MODES:
        raise ValueError("The supplied controller mode must be P or Q")
    return mode


def row(values: Iterable[int | F]) -> Vector:
    converted = tuple(_rational(value) for value in values)
    if len(converted) != 4:
        raise ValueError("A coordinate/effect row must have exactly four entries")
    return converted


def coordinates(values: Iterable[int | F], *, normalized: bool = False) -> Vector:
    result = row(values)
    if any(value < 0 for value in result):
        raise ValueError("Coordinates must lie in the nonnegative cone")
    if normalized and mass(result) != 1:
        raise ValueError("A normalized residual must have coordinate mass one")
    return result


def matrix(rows: Iterable[Iterable[int | F]]) -> Matrix:
    result = tuple(row(values) for values in rows)
    if len(result) != 4:
        raise ValueError("A matrix must have exactly four rows")
    return result


def mass(x: Vector) -> F:
    return sum(x, F(0))


def kernel_mass(d: Matrix) -> F:
    """Total-entry pair-kernel mass, not matrix trace."""
    return sum((sum(values, F(0)) for values in d), F(0))


def dot(a: Vector, b: Vector) -> F:
    return sum((x * y for x, y in zip(a, b, strict=True)), F(0))


def matvec(a: Matrix, x: Vector) -> Vector:
    return tuple(dot(values, x) for values in a)


def rowmat(effect: Vector, a: Matrix) -> Vector:
    return tuple(sum((effect[i] * a[i][j] for i in range(4)), F(0)) for j in range(4))


def encode(mode: str, x: Iterable[int | F]) -> Matrix:
    """Embed the specified polyhedral cone, including its zero element."""
    _mode(mode)
    x = coordinates(x)
    output = [[F(0) for _ in range(4)] for _ in range(4)]
    for r, (i, j) in enumerate(PARTITIONS[mode]):
        diagonal = x[2 * r] / 3 + x[2 * r + 1]
        off_diagonal = x[2 * r] / 6 - x[2 * r + 1] / 2
        output[i][i] = output[j][j] = diagonal
        output[i][j] = output[j][i] = off_diagonal
    return matrix(output)


def decode(mode: str, d: Iterable[Iterable[int | F]]) -> Vector:
    """Invert only the declared image cone; reject, never repair, other kernels."""
    _mode(mode)
    d = matrix(d)
    values = []
    for i, j in PARTITIONS[mode]:
        diagonal, off_diagonal = d[i][i], d[i][j]
        values.extend((F(3, 2) * diagonal + 3 * off_diagonal, diagonal / 2 - off_diagonal))
    x = coordinates(values)
    if encode(mode, x) != d:
        raise ValueError("Kernel is not in the declared controller image cone")
    return x


def event_pair(d: Matrix, left: tuple[int, ...], right: tuple[int, ...]) -> F:
    return sum((d[i][j] for i in left for j in right), F(0))


def record_weights(mode: str, d: Iterable[Iterable[int | F]]) -> tuple[F, F]:
    """Weights of the mode's record partition, only on its declared cone."""
    d = matrix(d)
    decode(mode, d)
    return tuple(event_pair(d, block, block) for block in PARTITIONS[mode])


def _diagonal(values: Iterable[int | F]) -> Matrix:
    entries = row(values)
    return matrix(tuple(entries[i] if i == j else 0 for j in range(4)) for i in range(4))


@dataclass(frozen=True)
class Branch:
    """One registered branch of the explicitly supplied controlled law.

    Matrices act on unnormalized columns. ``epsilon`` means no new committed
    record, not a recorded null outcome. Constructing an arbitrary Branch does
    not make it available: apply/word evaluation require registry membership.
    """

    source: str
    action: str
    outcome: str
    target: str
    matrix: Matrix
    commits: bool

    def __post_init__(self) -> None:
        _mode(self.source)
        _mode(self.target)
        if type(self.commits) is not bool:
            raise TypeError("commits must be boolean")
        if not isinstance(self.action, str) or not self.action:
            raise ValueError("An action must be a nonempty string")
        if not isinstance(self.outcome, str) or not self.outcome:
            raise ValueError("An outcome must be a nonempty string")
        converted = matrix(self.matrix)
        if any(value < 0 for values in converted for value in values):
            raise ValueError("Branch matrices must preserve the coordinate cone")
        if any(value > 1 for value in rowmat(UNIT, converted)):
            raise ValueError("A branch cannot increase coordinate mass")
        object.__setattr__(self, "matrix", converted)


def actions(mode: str) -> tuple[str, ...]:
    _mode(mode)
    return ("read", "switch") if mode == "P" else ("read", "switch", "attempt")


def branches(mode: str, action: str) -> tuple[Branch, ...]:
    """Return the whole normalized supplied test, refusing unavailable contexts."""
    if action not in actions(mode):
        raise ValueError(f"Action {action!r} is not available in mode {mode}")
    if action == "read":
        return tuple(
            Branch(mode, action, str(r), mode, _diagonal(int(i // 2 == r) for i in range(4)), True)
            for r in range(2)
        )
    if action == "switch":
        # Input (r,s) moves to (r XOR s,s), while the kernel embedding also changes.
        permutation = (0, 3, 2, 1)
        operator = matrix(tuple(int(i == permutation[j]) for j in range(4)) for i in range(4))
        return (Branch(mode, action, "epsilon", "Q" if mode == "P" else "P", operator, False),)
    return (
        Branch("Q", action, "epsilon", "Q", _diagonal((F(1, 2), 1, F(1, 2), 1)), False),
        Branch("Q", action, "0", "Q", _diagonal((F(1, 2), 0, 0, 0)), True),
        Branch("Q", action, "1", "Q", _diagonal((0, 0, F(1, 2), 0)), True),
    )


def _registered(branch: Branch) -> None:
    if not isinstance(branch, Branch):
        raise TypeError("A controlled branch must be a Branch")
    if branch not in branches(branch.source, branch.action):
        raise ValueError("Branch is not part of the supplied available operation law")


@dataclass(frozen=True)
class Record:
    """A committed event; its precursor is the supplied whole-history ideal."""

    event_id: int
    past: frozenset[int]
    mode: str
    action: str
    outcome: str

    def __post_init__(self) -> None:
        if type(self.event_id) is not int or self.event_id < 0:
            raise ValueError("event_id must be a nonnegative integer")
        if not isinstance(self.past, frozenset) or any(
            type(i) is not int or i < 0 for i in self.past
        ):
            raise ValueError("past must be an immutable set of nonnegative event IDs")
        if not any(
            branch.outcome == self.outcome and branch.commits
            for branch in branches(self.mode, self.action)
        ):
            raise ValueError("A record must name a registered committing outcome")


def _history(records: tuple[Record, ...]) -> None:
    if not isinstance(records, tuple) or any(not isinstance(record, Record) for record in records):
        raise TypeError("Committed history must be an immutable tuple of Records")
    for index, record in enumerate(records):
        if record.event_id != index or record.past != frozenset(range(index)):
            raise ValueError(
                "This candidate uses contiguous IDs and whole-history chain precursors"
            )


def append_record(records: tuple[Record, ...], branch: Branch) -> tuple[Record, ...]:
    """Structural append for an already selected positive-probability branch.

    This helper has no residual and therefore cannot verify nonzero branch
    probability. Callers must establish that precondition. ``apply_branch`` is
    the state-aware transition that enforces it before invoking this helper.
    The supplied chain choice appends exactly once; silent branches are refused.
    """
    _history(records)
    _registered(branch)
    if not branch.commits:
        raise ValueError("A silent branch cannot append a committed record")
    index = len(records)
    record = Record(index, frozenset(range(index)), branch.source, branch.action, branch.outcome)
    return (*records, record)


@dataclass(frozen=True)
class State:
    """Committed history and normalized residual, with explicit apparatus mode."""

    mode: str
    coordinates: Vector
    records: tuple[Record, ...] = ()

    def __post_init__(self) -> None:
        _mode(self.mode)
        object.__setattr__(self, "coordinates", coordinates(self.coordinates, normalized=True))
        _history(self.records)


@dataclass(frozen=True)
class BranchResult:
    probability: F
    state: State


def apply_branch(state: State, branch: Branch) -> BranchResult:
    """Condition on a positive registered branch; do not sample or create time."""
    if not isinstance(state, State):
        raise TypeError("A transition requires an immutable State")
    _registered(branch)
    if state.mode != branch.source:
        raise ValueError("Branch source does not match the current apparatus mode")
    unnormalized = matvec(branch.matrix, state.coordinates)
    probability = mass(unnormalized)
    if probability <= 0:
        raise ValueError("A zero-probability branch has no conditional residual or record")
    updated = tuple(value / probability for value in unnormalized)
    records = append_record(state.records, branch) if branch.commits else state.records
    return BranchResult(probability, State(branch.target, updated, records))


def word_probability(mode: str, x: Iterable[int | F], word: tuple[Branch, ...]) -> F:
    """Exact mass of a legal controlled branch cylinder, including empty words."""
    _mode(mode)
    residual = coordinates(x, normalized=True)
    if not isinstance(word, tuple):
        raise TypeError("A branch-word witness must be an immutable tuple")
    for branch in word:
        _registered(branch)
        if branch.source != mode:
            raise ValueError("Branch word is not a lawful controller sequence")
        residual = matvec(branch.matrix, residual)
        mode = branch.target
    return mass(residual)


def rank(rows: Iterable[Iterable[int | F]]) -> int:
    """Exact rational row rank; this is algebra, not a numerical tolerance."""
    work = [list(row(values)) for values in rows]
    pivot_row = 0
    for column in range(4):
        pivot = next((i for i in range(pivot_row, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        divisor = work[pivot_row][column]
        work[pivot_row] = [value / divisor for value in work[pivot_row]]
        for i in range(len(work)):
            if i != pivot_row:
                factor = work[i][column]
                work[i] = [
                    value - factor * basis
                    for value, basis in zip(work[i], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


@dataclass(frozen=True)
class Effect:
    """A basis row with its legal branch-word certificate (not a new record)."""

    row: Vector
    word: tuple[Branch, ...]


def future_effects() -> dict[str, tuple[Effect, ...]]:
    """Backward typed closure, at most eight independent rows across both modes.

    Each retained row has a lawful word witness. Equality on the final row span
    is equivalent to equality of every finite controlled branch-cylinder law.
    The controller family is declared, not inferred from the committed record.
    """
    bases = {mode: [Effect(UNIT, ())] for mode in MODES}
    changed = True
    while changed:
        changed = False
        for source in MODES:
            for action in actions(source):
                for branch in branches(source, action):
                    for effect in tuple(bases[branch.target]):
                        pulled = rowmat(effect.row, branch.matrix)
                        current_rows = [known.row for known in bases[source]]
                        if rank((*current_rows, pulled)) > len(current_rows):
                            bases[source].append(Effect(pulled, (branch, *effect.word)))
                            changed = True
    return {mode: tuple(basis) for mode, basis in bases.items()}


@dataclass(frozen=True)
class EquivalenceResult:
    equivalent: bool
    word: tuple[Branch, ...] | None
    probabilities: tuple[F, F] | None


def equivalent(mode: str, x: Iterable[int | F], y: Iterable[int | F]) -> EquivalenceResult:
    """Compare residuals in one mode; return a legal separating word if needed."""
    _mode(mode)
    x, y = coordinates(x, normalized=True), coordinates(y, normalized=True)
    for effect in future_effects()[mode]:
        px, py = dot(effect.row, x), dot(effect.row, y)
        if px != py:
            return EquivalenceResult(False, effect.word, (px, py))
    return EquivalenceResult(True, None, None)
