"""One exact finite conditional protocol, using four unchanged accepted sources.

Every physical availability/independence assertion is supplied, not derived.
The executable starts at a normalized, empty-history local snapshot with root
weight one. It retains earlier audit anchors but never exposes them to the
outcome-only command decision. All stage outputs are derived by actual forward
calls: callers cannot insert a target, weight, record, or post-read residual.
No general loader, process SDK, preparation theorem, or terminal reuse is here.
"""

from dataclasses import dataclass, field
from fractions import Fraction

import joint_source as d
import local_joint_adapter as bridge
import local_source as c
import terminal_read_source as i

F = Fraction
ONE = F(1)
FIXED_T = F(3, 5)
ORIGINS = ("signal", "reference")
JOINT_ORIGIN = "joint"
STOP_ORIGIN = "protocol-stop"
POLICY_ID = "finite_Y_Z_ready_cut_a_tilt"
WORD_BY_A = ((), ("A",))
AVAILABILITY = (
    "local_repeatable_Y",
    "local_Z",
    "independent_reference_selection_preparation",
    "shared_CNOT_H2",
    "fixed_interior_L_t_return",
    "literal_joint_cell_cut",
    "known_A",
)
CHOICES = ("ready", "unavailable")
CELLS = ((0, 0), (0, 1), (1, 0), (1, 1))


def validate_aliases() -> None:
    """Identity, not matching source text, is required by RI-15's class guards."""
    if bridge.c is not c or bridge.d is not d:
        raise ValueError("RI-15 must bind these same local_source and joint_source modules")
    if len({id(c), id(d), id(bridge), id(i)}) != 4:
        raise ValueError("The four accepted dependencies require distinct module instances")


validate_aliases()


def _exact(value, kind):
    if type(value) is not kind:
        raise TypeError(f"Use the exact bound {kind.__name__}, not a terminal or lookalike")
    return value


def _rational(value: int | F) -> F:
    if type(value) not in (int, F):
        raise TypeError("Supply exact built-in integers or Fractions, not floats or booleans")
    return F(value)


def _name(value: str) -> str:
    if type(value) is not str or not value or value != value.strip():
        raise ValueError("Supply a nonempty canonical built-in string identifier")
    return value


def _bit(value: int) -> int:
    if type(value) is not int or value not in (0, 1):
        raise ValueError("An outcome bit is a built-in 0 or 1")
    return value


def _cell(value) -> tuple[int, int]:
    if isinstance(value, str):
        raise TypeError("Retain both cell bits, not a string")
    value = tuple(value)
    if len(value) != 2:
        raise ValueError("A cell has exactly two bits")
    return (_bit(value[0]), _bit(value[1]))


def _terminal(value) -> tuple[int, int, str]:
    if isinstance(value, str):
        raise TypeError("Retain both cell bits and the terminal sign")
    value = tuple(value)
    if len(value) != 3 or type(value[2]) is not str or value[2] not in ("+", "-"):
        raise ValueError("The terminal outcome is the complete (a,b,sign) label")
    return (_bit(value[0]), _bit(value[1]), value[2])


def _choice(value: str) -> str:
    if type(value) is not str or value not in CHOICES:
        raise ValueError("Retain the actual ready or unavailable selector outcome")
    return value


def _read_premise(value: i.TerminalReadPremise) -> i.TerminalReadPremise:
    value = _exact(value, i.TerminalReadPremise)
    _name(value.setting_id)
    _name(value.calibration)
    if i.TerminalReadPremise(value.setting_id, value.calibration, value.available) != value:
        raise ValueError("Retain the exact declared available/calibrated terminal-read premise")
    return value


def policy_word(outcome: tuple[int, int]) -> tuple[str, ...]:
    """The ONLY adaptive decision: two bits in, immutable registered word out.

    Do not pass a full record/context/source to this function. Retained raw
    kernels are audit data, not an additional read available to the controller.
    """
    a, _ = _cell(outcome)
    return WORD_BY_A[a]


@dataclass(frozen=True)
class Boundary:
    """An expressly supplied conditional boundary, not an earlier preparation law."""

    source: c.State
    root_weight: F = ONE
    availability: tuple[str, ...] = AVAILABILITY

    def __post_init__(self) -> None:
        validate_aliases()
        source = _exact(self.source, c.State)
        checked = c.State(
            source.residual,
            source.records,
            source.settings,
            source.controller,
            source.source_kind,
            source.frame,
        )
        if checked != source or source.records or source.settings:
            raise ValueError("This boundary requires a valid empty record and pending prefix")
        if (source.controller, source.source_kind, source.frame) != (
            c.CONTROLLER,
            c.SOURCE_KIND,
            c.FRAME,
        ):
            raise ValueError("Retain the fixed local controller, source type and Pauli frame")
        if any(type(value) is not c.G for row in source.residual for value in row):
            raise TypeError("Local entries must use the exact bound Gaussian representation")
        weight = _rational(self.root_weight)
        if weight != 1:
            raise ValueError("The executable starts with supplied root weight one only")
        availability = tuple(self.availability)
        if availability != AVAILABILITY or any(type(x) is not str for x in availability):
            raise ValueError("Declare this fixed operational availability contract completely")
        object.__setattr__(self, "root_weight", weight)
        object.__setattr__(self, "availability", availability)


@dataclass(frozen=True)
class ReferenceLaw:
    """A supplied complete independent selector/preparer law, not inferred metadata."""

    ready: F
    unavailable: F
    independence: d.Independence
    preparation_id: str
    law_id: str
    preparation_available: bool

    def __post_init__(self) -> None:
        ready, unavailable = _rational(self.ready), _rational(self.unavailable)
        if min(ready, unavailable) < 0 or max(ready, unavailable) > 1:
            raise ValueError("Both selector weights lie in [0,1]")
        if ready + unavailable != 1:
            raise ValueError("Supply both complementary weights of the complete selector law")
        independence = _exact(self.independence, d.Independence)
        if independence.origins != ORIGINS:
            raise ValueError("The declared independent origins are exactly signal/reference")
        if any(type(origin) is not str for origin in independence.origins):
            raise TypeError("Origin names must use built-in strings")
        _name(self.preparation_id)
        _name(self.law_id)
        if type(self.preparation_available) is not bool or not self.preparation_available:
            raise ValueError("Declare the conditional fixed reference preparation available")
        object.__setattr__(self, "ready", ready)
        object.__setattr__(self, "unavailable", unavailable)

    @property
    def provenance(self) -> tuple[tuple[str, str], ...]:
        return (
            ("preparation_id", self.preparation_id),
            ("selector_law_id", self.law_id),
            ("protocol_id", POLICY_ID),
        )

    def probability(self, outcome: str) -> F:
        return self.ready if _choice(outcome) == "ready" else self.unavailable


@dataclass(frozen=True)
class WeightedLocal:
    """A positive Y commitment followed by the actual weight-one local Z control."""

    boundary: Boundary
    outcome: int
    probability: F = field(init=False)
    committed: c.State = field(init=False)
    state: c.State = field(init=False)
    weight: F = field(init=False)
    unnormalized: c.Matrix = field(init=False)

    def __post_init__(self) -> None:
        boundary, outcome = _exact(self.boundary, Boundary), _bit(self.outcome)
        raw = c.branch(boundary.source.residual, "Y", outcome)
        probability = c.mass(raw)
        if probability <= 0:
            raise ValueError("A zero local branch has no selected state or appended record")
        returned, committed = c.commit_pauli(boundary.source, "Y", outcome)
        if returned != probability or c.scale(probability, committed.residual) != raw:
            raise ValueError("The local conditional API must equal its full unnormalized branch")
        state = c.run_control(committed, "Z")
        transformed = c.controls(raw, "Z")
        if c.scale(probability, state.residual) != transformed:
            raise ValueError("The local Z control must act exactly once on the selected branch")
        if c.decompose_candidate(state.residual, normalized=True)[1] != 0:
            raise ValueError("This actual branch must establish C0 eligibility")
        object.__setattr__(self, "probability", probability)
        object.__setattr__(self, "committed", committed)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "weight", boundary.root_weight * probability)
        object.__setattr__(self, "unnormalized", transformed)


@dataclass(frozen=True)
class ReferenceDecision:
    """One selected record, retaining the whole law; unavailable has no source."""

    law: ReferenceLaw
    outcome: str
    origin: str = field(init=False, default=ORIGINS[1])
    probability: F = field(init=False)
    record: d.InputRecord = field(init=False)
    reference: d.ReferenceState | None = field(init=False)

    def __post_init__(self) -> None:
        law, outcome = _exact(self.law, ReferenceLaw), _choice(self.outcome)
        probability = law.probability(outcome)
        if probability <= 0:
            raise ValueError("A zero selector coordinate supplies no actual selection record")
        record = d.InputRecord(
            0,
            "reference_select_prepare",
            outcome,
            (law.preparation_id, law.law_id),
            law.provenance + (("reference_t", "3/5"), ("orientation", "Z")),
            (),
        )
        reference = (
            d.ReferenceState(FIXED_T, ORIGINS[1], (record,), "Z") if outcome == "ready" else None
        )
        object.__setattr__(self, "probability", probability)
        object.__setattr__(self, "record", record)
        object.__setattr__(self, "reference", reference)


@dataclass(frozen=True)
class WeightedJoint:
    """Actual RI-15 forward route, stopping BEFORE its terminal commitment."""

    local: WeightedLocal
    decision: ReferenceDecision
    source: bridge.JointSource = field(init=False)
    weight: F = field(init=False)

    def __post_init__(self) -> None:
        validate_aliases()
        local = _exact(self.local, WeightedLocal)
        decision = _exact(self.decision, ReferenceDecision)
        if decision.outcome != "ready" or type(decision.reference) is not d.ReferenceState:
            raise ValueError("Only a positive ready selection supplies the joint reference")
        prospective = bridge.prepare(
            local.state,
            decision.reference,
            decision.law.independence,
            local_origin=ORIGINS[0],
            joint_origin=JOINT_ORIGIN,
            reference_provenance=decision.law.provenance,
        )
        source = bridge.promote(bridge.couple(bridge.promote(prospective)))
        if source.target.coupler != d.SHARED_COUPLER:
            raise ValueError("The new arrow requires the already coupled preterminal source")
        if source.context.local_source is not local.state:
            raise ValueError("RI-15 must retain the original local state and pending Z")
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "weight", local.weight * decision.probability)


def _to_i_kernel(kernel: d.Matrix) -> i.Matrix:
    return i.matrix(tuple(tuple(i.G(z.real, z.imag) for z in row) for row in kernel))


def _to_i_record(record: d.InputRecord) -> i.InputRecord:
    _exact(record, d.InputRecord)
    return i.InputRecord(
        record.event_id,
        record.action,
        record.outcome,
        record.settings,
        record.payload,
        record.precursor,
    )


@dataclass(frozen=True)
class LtEnvelope:
    """Lossless same-kernel inclusion under an explicitly adopted return/read contract."""

    joint: WeightedJoint
    terminal_read: i.TerminalReadPremise
    state: i.State = field(init=False)
    weight: F = field(init=False)

    def __post_init__(self) -> None:
        joint = _exact(self.joint, WeightedJoint)
        premise = _read_premise(self.terminal_read)
        source = _exact(joint.source, bridge.JointSource)
        context = source.context
        decision = joint.decision
        if source.target.coupler != d.SHARED_COUPLER:
            raise ValueError("Do not adapt a product, prospective or terminal target")
        if (
            context.reference != decision.reference
            or context.reference_provenance != decision.law.provenance
        ):
            raise ValueError("Retain the ready decision's exact reference and provenance")
        local = i.LocalInput(
            _to_i_kernel(context.local_input.residual),
            context.local_input.origin,
            tuple(_to_i_record(record) for record in context.local_input.records),
        )
        reference = i.ReferenceInput(
            context.reference.t,
            context.reference.origin,
            tuple(_to_i_record(record) for record in context.reference.records),
            context.reference.orientation,
        )
        if reference.residual != _to_i_kernel(context.reference.residual):
            raise ValueError("The complete reference kernel must survive conversion unchanged")
        new_context = i.Context(
            local,
            reference,
            i.Independence(context.independence.origins),
            premise,
            joint_origin=context.joint_origin,
            coupler=source.target.coupler,
            frame=i.FRAME,
            controller=i.CONTROLLER,
            setting_id=i.NOMINAL_CUT,
            permutation=source.target.permutation,
        )
        kernel = _to_i_kernel(source.target.residual)
        expected = i.k_from_local(local.residual, FIXED_T, normalized=True)
        if kernel != expected:
            raise ValueError("The ENTIRE existing native kernel must equal its fixed K_t image")
        i.inverse_k_span(kernel, FIXED_T)
        i.image_kernel(kernel, FIXED_T, normalized=True)
        if i.raw_mass(kernel) != 1:
            raise ValueError("Native entry mass, not a substituted trace, normalizes this source")
        state = i.State(i.INTERIOR_DOMAIN, new_context, kernel, (), ())
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "weight", joint.weight)


def convert_preterminal(
    source: bridge.JointSource,
    anchor: WeightedJoint,
    terminal_read: i.TerminalReadPremise,
) -> LtEnvelope:
    """Bind one supplied preterminal source to its whole weighted audit anchor.

    This is a representation/interface conversion, not another preparation or
    coupling. In particular neither bare terminals nor an equal quotient can
    substitute for the complete source and original local pending word.
    """
    validate_aliases()
    source = _exact(source, bridge.JointSource)
    anchor = _exact(anchor, WeightedJoint)
    if source.target.coupler != d.SHARED_COUPLER:
        raise ValueError("The conversion point is after the one actual shared coupling")
    verified = bridge.JointSource(source.context, source.target)
    if verified != source or source != anchor.source:
        raise ValueError("The whole forward-verified source must match its exact weighted anchor")
    return LtEnvelope(anchor, terminal_read)


@dataclass(frozen=True)
class CutEnvelope:
    """The existing reusable L_t literal cut, retaining all source anchors."""

    source: LtEnvelope
    outcome: tuple[int, int]
    probability: F = field(init=False)
    state: i.State = field(init=False)
    weight: F = field(init=False)
    unnormalized: i.Matrix = field(init=False)

    def __post_init__(self) -> None:
        source, outcome = _exact(self.source, LtEnvelope), _cell(self.outcome)
        raw = i.branch(source.state.residual, FIXED_T, outcome)
        probability = i.raw_mass(raw)
        if probability <= 0:
            raise ValueError("A zero literal cut cannot normalize or append an event")
        returned, state = i.commit(source.state, outcome)
        if returned != probability or i.scale(probability, state.residual) != raw:
            raise ValueError("The full cut residual must equal probability times conditional state")
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "probability", probability)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "weight", source.weight * probability)
        object.__setattr__(self, "unnormalized", raw)


@dataclass(frozen=True)
class CommandEnvelope:
    """A fixed record-outcome policy, not a caller-supplied raw-state callback."""

    cut: CutEnvelope
    word: tuple[str, ...] = field(init=False)
    state: i.State = field(init=False)
    weight: F = field(init=False)

    def __post_init__(self) -> None:
        cut = _exact(self.cut, CutEnvelope)
        # Only these two bits cross the controller boundary. In particular the
        # full JointRecord carries raw Context data and must not be passed.
        word = policy_word(cut.state.records[-1].outcome)
        state = i.run_word(cut.state, word)
        if state.records != cut.state.records or state.pending != word:
            raise ValueError("Apply the actual new word once and retain the committed cut")
        if i.raw_mass(state.residual) != 1:
            raise ValueError("The accepted command must preserve normalized native mass")
        object.__setattr__(self, "word", word)
        object.__setattr__(self, "state", state)
        object.__setattr__(self, "weight", cut.weight)


@dataclass(frozen=True)
class PathLabel:
    """A prospective coordinate with the planned read ID, including stopped paths.

    Planned-setting metadata is not a claim that a stopped or zero event read
    occurred. Actual records and their full audit anchors remain separate.
    """

    local_outcome: int
    reference_outcome: str
    preparation_id: str
    law_id: str
    cut_outcome: tuple[int, int] | None = None
    command_word: tuple[str, ...] = ()
    terminal_outcome: tuple[int, int, str] | None = None
    policy_id: str = POLICY_ID
    terminal_setting_id: str = i.NOMINAL_TERMINAL_READ

    def __post_init__(self) -> None:
        _bit(self.local_outcome)
        choice = _choice(self.reference_outcome)
        _name(self.preparation_id)
        _name(self.law_id)
        _name(self.terminal_setting_id)
        if type(self.policy_id) is not str or self.policy_id != POLICY_ID:
            raise ValueError("Retain the fixed complete nominal policy identifier")
        if isinstance(self.command_word, str):
            raise TypeError("The actual command word is a sequence of complete labels")
        word = tuple(self.command_word)
        if choice == "unavailable":
            if self.cut_outcome is not None or self.terminal_outcome is not None or word:
                raise ValueError("Unavailable stops have no invented cut, command or read")
        else:
            cell = _cell(self.cut_outcome)
            terminal = _terminal(self.terminal_outcome)
            if word != policy_word(cell) or any(type(x) is not str for x in word):
                raise ValueError("The coordinate must retain the actual fixed-policy command word")
            object.__setattr__(self, "cut_outcome", cell)
            object.__setattr__(self, "terminal_outcome", terminal)
        object.__setattr__(self, "command_word", word)


@dataclass(frozen=True)
class WeightedTerminal:
    """Scalar-only terminal output; exact pre-read sources remain audit data only."""

    commands: CommandEnvelope
    outcome: tuple[int, int, str]
    result: i.TerminalResult = field(init=False)
    probability: F = field(init=False)
    weight: F = field(init=False)
    label: PathLabel = field(init=False)

    def __post_init__(self) -> None:
        commands = _exact(self.commands, CommandEnvelope)
        outcome = _terminal(self.outcome)
        result = i.read_terminal(commands.state, outcome)
        joint = commands.cut.source.joint
        law = joint.decision.law
        label = PathLabel(
            joint.local.outcome,
            "ready",
            law.preparation_id,
            law.law_id,
            commands.cut.outcome,
            commands.word,
            outcome,
            terminal_setting_id=commands.cut.source.terminal_read.setting_id,
        )
        object.__setattr__(self, "outcome", outcome)
        object.__setattr__(self, "result", result)
        object.__setattr__(self, "probability", result.probability)
        object.__setattr__(self, "weight", commands.weight * result.probability)
        object.__setattr__(self, "label", label)


@dataclass(frozen=True)
class StopReport:
    """A scalar report; its declared planned read setting is NOT a performed read."""

    local: WeightedLocal
    decision: ReferenceDecision
    terminal_read: i.TerminalReadPremise
    origin: str = field(init=False, default=STOP_ORIGIN)
    event_id: int = field(init=False, default=0)
    action: str = field(init=False, default="protocol_stop")
    outcome: str = field(init=False, default="reference_unavailable")
    policy_id: str = field(init=False, default=POLICY_ID)
    precursor: tuple[tuple[str, int], ...] = field(init=False)

    def __post_init__(self) -> None:
        local = _exact(self.local, WeightedLocal)
        decision = _exact(self.decision, ReferenceDecision)
        _read_premise(self.terminal_read)
        if decision.outcome != "unavailable" or decision.reference is not None:
            raise ValueError("Only an unavailable decision produces this scalar stop report")
        precursor = tuple((ORIGINS[0], record.event_id) for record in local.state.records)
        precursor += ((decision.origin, decision.record.event_id),)
        object.__setattr__(self, "precursor", precursor)


@dataclass(frozen=True)
class StoppedBranch:
    """A scalar stopped path, retaining the existing local state without a new residual."""

    local: WeightedLocal
    decision: ReferenceDecision
    terminal_read: i.TerminalReadPremise
    report: StopReport = field(init=False)
    weight: F = field(init=False)
    label: PathLabel = field(init=False)

    def __post_init__(self) -> None:
        report = StopReport(self.local, self.decision, self.terminal_read)
        law = self.decision.law
        label = PathLabel(
            self.local.outcome,
            "unavailable",
            law.preparation_id,
            law.law_id,
            terminal_setting_id=self.terminal_read.setting_id,
        )
        object.__setattr__(self, "report", report)
        object.__setattr__(self, "weight", self.local.weight * self.decision.probability)
        object.__setattr__(self, "label", label)


@dataclass(frozen=True)
class LawEntry:
    """One labeled scalar coordinate; only a positive coordinate has a selected leaf."""

    label: PathLabel
    weight: F
    selected: WeightedTerminal | StoppedBranch | None

    def __post_init__(self) -> None:
        _exact(self.label, PathLabel)
        weight = _rational(self.weight)
        if weight < 0:
            raise ValueError("A scalar law coordinate cannot have negative mass")
        if weight == 0:
            if self.selected is not None:
                raise ValueError("Zero coordinates must not fabricate selected states or records")
        elif type(self.selected) not in (WeightedTerminal, StoppedBranch):
            raise TypeError("A positive coordinate retains its actual terminal or stopped trace")
        elif self.selected.label != self.label or self.selected.weight != weight:
            raise ValueError("Scalar weight and full label must match the actual selected trace")
        object.__setattr__(self, "weight", weight)


@dataclass(frozen=True)
class ProtocolRun:
    """Complete 66-coordinate law for this finite policy, not a selectable source.

    Zeros are inspected before each selected constructor. Unexpected validation
    exceptions propagate and reject the whole contract; none becomes a zero.
    """

    boundary: Boundary
    law: ReferenceLaw
    terminal_read: i.TerminalReadPremise
    coordinates: tuple[LawEntry, ...] = field(init=False)

    def __post_init__(self) -> None:
        boundary = _exact(self.boundary, Boundary)
        law = _exact(self.law, ReferenceLaw)
        premise = _read_premise(self.terminal_read)
        # Validate even when ready weight is zero: invalid declarations are not
        # additional physical outcomes that an implementation may skip.
        validate_aliases()
        entries = []
        for r in (0, 1):
            probability = c.mass(c.branch(boundary.source.residual, "Y", r))
            local = WeightedLocal(boundary, r) if probability > 0 else None
            lt = None
            if local is not None and law.ready > 0:
                decision = ReferenceDecision(law, "ready")
                joint = WeightedJoint(local, decision)
                lt = convert_preterminal(joint.source, joint, premise)
            for cell in CELLS:
                commands = None
                if lt is not None:
                    raw = i.branch(lt.state.residual, FIXED_T, cell)
                    if i.raw_mass(raw) > 0:
                        commands = CommandEnvelope(CutEnvelope(lt, cell))
                weights = (
                    i.terminal_weights(commands.state.residual, FIXED_T)
                    if commands is not None
                    else (F(0),) * 8
                )
                for outcome, conditional in zip(i.TERMINAL_OUTCOMES, weights):
                    label = PathLabel(
                        r,
                        "ready",
                        law.preparation_id,
                        law.law_id,
                        cell,
                        policy_word(cell),
                        outcome,
                        terminal_setting_id=premise.setting_id,
                    )
                    leaf = (
                        WeightedTerminal(commands, outcome)
                        if commands is not None and conditional > 0
                        else None
                    )
                    entries.append(LawEntry(label, leaf.weight if leaf is not None else F(0), leaf))
            stop = (
                StoppedBranch(local, ReferenceDecision(law, "unavailable"), premise)
                if local is not None and law.unavailable > 0
                else None
            )
            label = PathLabel(
                r,
                "unavailable",
                law.preparation_id,
                law.law_id,
                terminal_setting_id=premise.setting_id,
            )
            entries.append(LawEntry(label, stop.weight if stop is not None else F(0), stop))
        if len(entries) != 66 or sum((entry.weight for entry in entries), F(0)) != 1:
            raise ValueError(
                "The complete finite conditional law must have 66 entries and mass one"
            )
        if len({entry.label for entry in entries}) != 66:
            raise ValueError("Distinct complete path labels must not be merged")
        object.__setattr__(self, "coordinates", tuple(entries))

    @property
    def probabilities(self) -> tuple[tuple[PathLabel, F], ...]:
        return tuple((entry.label, entry.weight) for entry in self.coordinates)

    @property
    def leaves(self) -> tuple[WeightedTerminal | StoppedBranch, ...]:
        return tuple(entry.selected for entry in self.coordinates if entry.selected is not None)

    @property
    def total(self) -> F:
        return sum((entry.weight for entry in self.coordinates), F(0))


def run_protocol(
    boundary: Boundary,
    law: ReferenceLaw,
    terminal_read: i.TerminalReadPremise,
) -> ProtocolRun:
    return ProtocolRun(boundary, law, terminal_read)


def primary_boundary() -> Boundary:
    """Declare the exact nonzero-c starting fixture; this is not preparation evidence."""
    rho = c.scale(F(1, 2), c.add(c.identity(2), c.scale(F(3, 5), c.Y)))
    kernel = c.candidate_from(c.scale(F(1, 2), c.transpose(rho)), F(1, 20), normalized=True)
    return Boundary(c.State(kernel), F(1))


def zero_local_boundary() -> Boundary:
    """A separate normalized Y+ fixture, whose Y-minus coordinate is zero."""
    return Boundary(c.State(c.section(c.projector("Y", 0), normalized=True)), F(1))


def primary_law() -> ReferenceLaw:
    """Explicit fixture premises, not a probability inferred from provenance."""
    return ReferenceLaw(
        F(2, 3),
        F(1, 3),
        d.Independence(ORIGINS),
        "fixed_R_3_5_Z",
        "independent_ready_unavailable",
        True,
    )
