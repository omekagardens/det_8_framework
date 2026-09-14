"""Exact, conditional RI-08c to RI-08d bridge under fixed source aliases.

The separate coordinator launcher binds local_source and joint_source to the
reviewed original model bytes. This module neither loads files nor supplies a
new physical operation. Original local snapshots survive in every envelope;
the accepted joint model performs all product, coupler and terminal-cut algebra.
"""

from dataclasses import dataclass, field

import joint_source as d
import local_source as c


def _name(value: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise ValueError("Supply a nonempty canonical provenance label")
    return value


def _local(state: c.State) -> c.State:
    if type(state) is not c.State:
        raise TypeError("Use the exact bound RI-08c State, never a terminal or foreign state")
    validated = c.State(
        state.residual,
        state.records,
        state.settings,
        state.controller,
        state.source_kind,
        state.frame,
    )
    if state != validated:
        raise ValueError("Retain a complete valid RI-08c snapshot")
    return state


def convert_local_state(state: c.State, *, origin: str) -> d.LocalState:
    """Change exact Python representations; preserve the entire current kernel.

    The returned legacy LocalState cannot hold pending word/frame/controller.
    It must travel inside a bridge envelope to preserve the full local context.
    This conversion applies no control, quotient, section, reset or new record.
    """
    state, origin = _local(state), _name(origin)
    residual = d.matrix(
        tuple(tuple(d.G(value.real, value.imag) for value in row) for row in state.residual)
    )
    records = tuple(
        d.InputRecord(
            record.event_id,
            record.action,
            str(record.outcome),
            record.settings,
            (
                ("ri08c.axis", record.axis),
                ("ri08c.controller", record.controller),
                ("ri08c.source_kind", record.source_kind),
                ("ri08c.frame", record.frame),
            ),
            record.precursor,
        )
        for record in state.records
    )
    return d.LocalState(residual, origin, records)


def _provenance(values: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    if isinstance(values, str):
        raise TypeError("Reference provenance is a nonempty sequence of key/value pairs")
    result = []
    for item in values:
        if isinstance(item, str):
            raise TypeError("A provenance item must be a key/value pair, not a string")
        pair = tuple(item)
        if len(pair) != 2:
            raise ValueError("Reference provenance items contain exactly two strings")
        result.append((_name(pair[0]), _name(pair[1])))
    if not result or len({key for key, _ in result}) != len(result):
        raise ValueError("Reference provenance requires nonempty, distinct keys")
    return tuple(result)


@dataclass(frozen=True)
class BridgeContext:
    """Retained supplied preparations and provenance, not a preparation proof.

    local_source contains its pending actual control word and original local
    frame/controller/source kind even when no earlier record exists. The named
    independence premise and reference provenance are supplied, not inferred.
    No cumulative local-history or reference-selection probability is available.
    """

    local_source: c.State
    reference: d.ReferenceState
    independence: d.Independence
    local_origin: str
    joint_origin: str
    reference_provenance: tuple[tuple[str, str], ...]
    local_input: d.LocalState = field(init=False)

    def __post_init__(self) -> None:
        _local(self.local_source)
        if type(self.reference) is not d.ReferenceState:
            raise TypeError("Retain the exact bound RI-08d reference preparation")
        if type(self.independence) is not d.Independence:
            raise TypeError("Supply the exact bound RI-08d independence declaration")
        _name(self.local_origin)
        _name(self.joint_origin)
        reference = d.ReferenceState(
            self.reference.t,
            self.reference.origin,
            self.reference.records,
            self.reference.orientation,
        )
        if self.reference != reference:
            raise ValueError("Reference residual must match its retained preparation")
        local = convert_local_state(self.local_source, origin=self.local_origin)
        # Existing joint construction validates all three distinct origins and
        # the declared independence pair; it does not certify independence.
        d.prepare_joint(local, reference, self.independence, joint_origin=self.joint_origin)
        object.__setattr__(self, "local_input", local)
        object.__setattr__(self, "reference_provenance", _provenance(self.reference_provenance))


def _context(context: BridgeContext) -> BridgeContext:
    if type(context) is not BridgeContext:
        raise TypeError("Retain the complete immutable BridgeContext")
    return context


def _expected_prospective(context: BridgeContext, coupler: str) -> d.ProspectiveState:
    context = _context(context)
    product = d.prepare_joint(
        context.local_input,
        context.reference,
        context.independence,
        joint_origin=context.joint_origin,
    )
    if coupler == d.IDENTITY_COUPLER:
        return product
    if coupler == d.SHARED_COUPLER:
        return d.couple_state(d.promote_joint(product))
    raise ValueError("The bridge retains exactly the product or one accepted shared coupling")


@dataclass(frozen=True)
class ProspectiveJoint:
    context: BridgeContext
    target: d.ProspectiveState

    def __post_init__(self) -> None:
        if type(self.target) is not d.ProspectiveState:
            raise TypeError("Use the exact prospective RI-08d target type")
        expected = _expected_prospective(self.context, self.target.coupler)
        if self.target != expected:
            raise ValueError("Prospective target must equal the full retained forward construction")


@dataclass(frozen=True)
class JointSource:
    context: BridgeContext
    target: d.CompositeState

    def __post_init__(self) -> None:
        if type(self.target) is not d.CompositeState:
            raise TypeError("Use the exact jointly recordable RI-08d source type")
        expected = d.promote_joint(_expected_prospective(self.context, self.target.coupler))
        if self.target != expected:
            raise ValueError("Joint source must equal the validated retained forward construction")


@dataclass(frozen=True)
class JointTerminal:
    context: BridgeContext
    target: d.TerminalState

    def __post_init__(self) -> None:
        if type(self.target) is not d.TerminalState:
            raise TypeError("Use the exact terminal RI-08d cut type")
        JointSource(self.context, self.target.source)
        _, expected = d.commit_joint(self.target.source, self.target.record.outcome)
        if self.target != expected:
            raise ValueError("Terminal target must equal the actual retained positive-weight cut")

    @property
    def conditional_probability(self) -> d.F:
        return d.joint_mass(d.joint_cut(self.target.source.residual, self.target.record.outcome))


def prepare(
    state: c.State,
    reference: d.ReferenceState,
    independence: d.Independence,
    *,
    local_origin: str,
    joint_origin: str,
    reference_provenance: tuple[tuple[str, str], ...],
) -> ProspectiveJoint:
    """Compose supplied normalized preparations, preserving their full context."""
    context = BridgeContext(
        state, reference, independence, local_origin, joint_origin, reference_provenance
    )
    return ProspectiveJoint(context, _expected_prospective(context, d.IDENTITY_COUPLER))


def promote(state: ProspectiveJoint) -> JointSource:
    """Validate the exact joint source; never repair it by projection or reset."""
    if type(state) is not ProspectiveJoint:
        raise TypeError("Only a retained prospective bridge can undergo source validation")
    return JointSource(state.context, d.promote_joint(state.target))


def couple(state: JointSource) -> ProspectiveJoint:
    """Apply the one accepted shared coupler; do not replay pending local controls."""
    if type(state) is not JointSource:
        raise TypeError("Only a validated bridge source can undergo the shared coupling")
    return ProspectiveJoint(state.context, d.couple_state(state.target))


def commit(state: JointSource, outcome: tuple[int, int]) -> tuple[d.F, JointTerminal]:
    """Return conditional weight and full terminal cut; supply no further reuse."""
    if type(state) is not JointSource:
        raise TypeError("Only a validated bridge source can form a terminal joint record")
    probability, target = d.commit_joint(state.target, outcome)
    return probability, JointTerminal(state.context, target)
