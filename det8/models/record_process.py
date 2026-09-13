"""Experimental contracts separating residual activity, commit, and record access.

These immutable finite objects are research scaffolding, not a new DET law or
an exported core/RET interface. Callers supply residual operations and realized
commit branches. No dynamics, scheduling parameter, Born rule, physical cone,
record-selection mechanism, or eventual-commit guarantee is derived here.

The record tuple is one append order, not a universal physical clock. Each
``past`` contains the full strict predecessor ideal, not merely cover edges.
Immutability follows the public immutable-value API; it rejects mutable
containers and custom payload aliases. It is not a security boundary against
``object.__setattr__`` or tampering with private ``Fraction`` internals.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import TypeAlias

ImmutableValue: TypeAlias = (
    None | bool | int | str | float | complex | Fraction | tuple["ImmutableValue", ...]
)
Probability: TypeAlias = int | float | Fraction
_KINDS = frozenset({"outcome", "null", "receipt"})


def _immutable(value: ImmutableValue) -> None:
    """Reject mutable containers, custom subclasses, and nonfinite scalars."""
    value_type = type(value)
    if value_type in (type(None), bool, int, str, Fraction):
        return
    if value_type is float:
        if not isfinite(value):
            raise ValueError("immutable float values must be finite")
        return
    if value_type is complex:
        if not (isfinite(value.real) and isfinite(value.imag)):
            raise ValueError("immutable complex values must be finite")
        return
    if value_type is tuple:
        for item in value:
            _immutable(item)
        return
    raise TypeError("values must use exact immutable scalar types or tuples thereof")


def _event_id(value: int) -> None:
    if type(value) is not int:
        raise TypeError("event IDs must be exact integers, not booleans or subclasses")


def _record_fields(
    event_id: int, kind: str, label: str, payload: ImmutableValue, source_event_id: int | None
) -> None:
    _event_id(event_id)
    if type(kind) is not str or kind not in _KINDS:
        raise ValueError("record kind must be outcome, null, or receipt")
    if type(label) is not str:
        raise TypeError("record labels must be exact strings")
    _immutable(payload)
    if kind == "receipt":
        _event_id(source_event_id)
    elif source_event_id is not None:
        raise ValueError("only a receipt can carry source_event_id")


@dataclass(frozen=True, slots=True)
class CommittedRecord:
    """One immutable fact; a logged null is a fact, not a silent transition.

    A receipt references a distinct already-committed event in its causal past.
    Existence and downward closure of all predecessors are checked by the
    enclosing snapshot. Nothing here derives when a physical fact forms.
    """

    event_id: int
    past: frozenset[int]
    kind: str = "outcome"
    label: str = ""
    payload: ImmutableValue = None
    source_event_id: int | None = None

    def __post_init__(self) -> None:
        _record_fields(self.event_id, self.kind, self.label, self.payload, self.source_event_id)
        if type(self.past) is not frozenset:
            raise TypeError("past must be an exact frozenset of predecessor IDs")
        for predecessor in self.past:
            _event_id(predecessor)
        if self.event_id in self.past:
            raise ValueError("an event cannot precede itself")
        if self.kind == "receipt" and self.source_event_id not in self.past:
            raise ValueError("a receipt source must be in its strict causal past")


@dataclass(frozen=True, slots=True)
class CommittedSnapshot:
    """Finite append-only record poset represented in a valid append order."""

    records: tuple[CommittedRecord, ...] = ()

    def __post_init__(self) -> None:
        if type(self.records) is not tuple:
            raise TypeError("records must be an exact tuple")
        seen: dict[int, CommittedRecord] = {}
        for record in self.records:
            if type(record) is not CommittedRecord:
                raise TypeError("snapshot entries must be exact CommittedRecord objects")
            if record.event_id in seen:
                raise ValueError("each committed event ID must be fresh")
            if not record.past <= seen.keys():
                raise ValueError("all predecessors must already be committed")
            if any(not seen[ancestor].past <= record.past for ancestor in record.past):
                raise ValueError("past must be a downward-closed full predecessor ideal")
            seen[record.event_id] = record

    @property
    def count(self) -> int:
        """Committed-event count only; not a count of all residual operations."""
        return len(self.records)

    def precedes(self, earlier: int, later: int) -> bool:
        """Return the strict order, raising KeyError for uncommitted IDs."""
        _event_id(earlier)
        _event_id(later)
        records = {record.event_id: record for record in self.records}
        if earlier not in records:
            raise KeyError(earlier)
        if later not in records:
            raise KeyError(later)
        return earlier in records[later].past


@dataclass(frozen=True, slots=True)
class ResidualState:
    """A declared residual-system type and immutable encoded value.

    ``type_id`` is a caller-supplied identifier, not proof that the values form
    a physical state space or that all encodings of the type are admissible.
    A pair-kernel can be encoded as a tuple of tuples; its positivity and
    total-entry normalization require separate model-specific validation.
    """

    type_id: str
    value: ImmutableValue

    def __post_init__(self) -> None:
        if type(self.type_id) is not str:
            raise TypeError("type_id must be an exact string")
        if not self.type_id.strip():
            raise ValueError("type_id must be nonempty and non-whitespace")
        _immutable(self.value)


@dataclass(frozen=True, slots=True)
class ProcessState:
    """Committed history and residual state are distinct components."""

    committed: CommittedSnapshot
    residual: ResidualState

    def __post_init__(self) -> None:
        if type(self.committed) is not CommittedSnapshot:
            raise TypeError("committed must be an exact CommittedSnapshot")
        if type(self.residual) is not ResidualState:
            raise TypeError("residual must be an exact ResidualState")


@dataclass(frozen=True, slots=True)
class AccessibleRecord:
    """Exact selected record content, without unselected ancestor metadata.

    A receipt's literal source reference may name an inaccessible event. This
    does not create an accessible vertex or an inferred causal edge.
    """

    event_id: int
    kind: str = "outcome"
    label: str = ""
    payload: ImmutableValue = None
    source_event_id: int | None = None

    def __post_init__(self) -> None:
        _record_fields(self.event_id, self.kind, self.label, self.payload, self.source_event_id)
        if self.source_event_id == self.event_id:
            raise ValueError("a receipt cannot reference itself")


@dataclass(frozen=True, slots=True)
class RecordView:
    """An exact projection, not a past-closed snapshot or a physical receipt.

    ``order`` is the induced strict transitive relation, not a retained-edge
    cover graph. The constructor checks a finite strict partial order; only
    ``access_records`` establishes its provenance in a particular snapshot.
    """

    records: tuple[AccessibleRecord, ...] = ()
    order: frozenset[tuple[int, int]] = frozenset()

    def __post_init__(self) -> None:
        if type(self.records) is not tuple:
            raise TypeError("view records must be an exact tuple")
        if any(type(record) is not AccessibleRecord for record in self.records):
            raise TypeError("view entries must be exact AccessibleRecord objects")
        ids = {record.event_id for record in self.records}
        if len(ids) != len(self.records):
            raise ValueError("view event IDs must be unique")
        if type(self.order) is not frozenset:
            raise TypeError("view order must be an exact frozenset")
        for pair in self.order:
            if type(pair) is not tuple or len(pair) != 2:
                raise TypeError("order entries must be exact pairs of event IDs")
            earlier, later = pair
            _event_id(earlier)
            _event_id(later)
            if earlier not in ids or later not in ids:
                raise ValueError("view order may only refer to accessible vertices")
            if earlier == later:
                raise ValueError("view order must be irreflexive")
        for earlier, middle in self.order:
            for left, later in self.order:
                if left == middle and (earlier, later) not in self.order:
                    raise ValueError("view order must be transitive")

    @property
    def count(self) -> int:
        return len(self.records)

    def precedes(self, earlier: int, later: int) -> bool:
        """Return the induced order, raising KeyError for inaccessible IDs."""
        _event_id(earlier)
        _event_id(later)
        ids = {record.event_id for record in self.records}
        if earlier not in ids:
            raise KeyError(earlier)
        if later not in ids:
            raise KeyError(later)
        return (earlier, later) in self.order


def _process_state(state: ProcessState) -> None:
    if type(state) is not ProcessState:
        raise TypeError("state must be an exact ProcessState")


def evolve_residual(
    state: ProcessState, operation: Callable[[ResidualState], ResidualState]
) -> ProcessState:
    """Apply one supplied same-type operation without a committed event.

    The result shares the original committed snapshot object. Calling order
    only composes functions; it does not supply a physical scheduler, duration,
    preferred foliation, or guarantee that any subsequent commit occurs.
    """
    _process_state(state)
    if not callable(operation):
        raise TypeError("operation must be callable")
    residual = operation(state.residual)
    if type(residual) is not ResidualState:
        raise TypeError("operation must return an exact ResidualState")
    if residual.type_id != state.residual.type_id:
        raise ValueError("a silent residual operation must preserve its declared type")
    return ProcessState(state.committed, residual)


def commit_record(
    state: ProcessState,
    record: CommittedRecord,
    residual: ResidualState,
    branch_probability: Probability,
) -> ProcessState:
    """Append exactly one supplied positive-probability realized branch.

    The supplied branch may change residual-system type. This checks neither
    a complete instrument's normalization nor its physical admissibility and
    does not sample, derive probabilities, or select an outcome. Zero-weight
    bookkeeping branches cannot be committed. A positive-probability ``null``
    outcome is an ordinary new record and increases the committed count.
    """
    _process_state(state)
    if type(record) is not CommittedRecord:
        raise TypeError("record must be an exact CommittedRecord")
    if type(residual) is not ResidualState:
        raise TypeError("residual must be an exact ResidualState")
    if type(branch_probability) not in (int, float, Fraction):
        raise TypeError("branch probability must be an exact int, float, or Fraction")
    if type(branch_probability) is float and not isfinite(branch_probability):
        raise ValueError("branch probability must be finite")
    if not 0 < branch_probability <= 1:
        raise ValueError("only a branch with probability in (0, 1] can be committed")
    committed = CommittedSnapshot(state.committed.records + (record,))
    return ProcessState(committed, residual)


def access_records(state: ProcessState, event_ids: Iterable[int]) -> RecordView:
    """Passively expose selected records and their exact induced order.

    Selection may omit ancestors and may be empty. It does not change the
    process state, add a receipt, invent ancestors, model noisy detection, or
    infer missing order. Reordering requested IDs never changes the source
    snapshot's append order in the returned tuple. Duplicate/unknown IDs are
    rejected instead of being silently repaired.
    """
    _process_state(state)
    requested = tuple(event_ids)
    for event_id in requested:
        _event_id(event_id)
    selected = frozenset(requested)
    if len(selected) != len(requested):
        raise ValueError("requested event IDs must be unique")
    existing = {record.event_id for record in state.committed.records}
    for event_id in requested:
        if event_id not in existing:
            raise KeyError(event_id)
    records = tuple(record for record in state.committed.records if record.event_id in selected)
    accessible = tuple(
        AccessibleRecord(
            record.event_id, record.kind, record.label, record.payload, record.source_event_id
        )
        for record in records
    )
    order = frozenset(
        (predecessor, record.event_id)
        for record in records
        for predecessor in record.past & selected
    )
    return RecordView(accessible, order)
