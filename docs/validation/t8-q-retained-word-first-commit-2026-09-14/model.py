"""Small exact supplement for retained-word first commitment, not an SDK.

One supplied stationary policy has mutually exclusive A/B silent outcomes and
a K commitment. They are not summed alternative choices of the experimenter.
The infinite output is a symbolic geometric family queried by finite words,
never a finite dictionary advertised as the whole countable direct sum.
Words, initial pending metadata, complete prior records and output types stay
intact. Uniformly contractive word-dependent effects are mathematical
continuations, not newly established physical availability.

The optional Bloch example is the exact filtered representation of the already
declared t=3/5 L_t cell00 face. Its native image is I_t with other blocks zero,
rho00=10 D00^-1 sigma D00^-1 and D00=diag(2,1). This injective correspondence
retains the full cell payload; it is not a new quantum-state classification.
Only the existing common-X A and literal cell cut are used there. Terminal
tilted reads have scalar outputs only, not a manufactured post-read residual.
"""

from dataclasses import dataclass, field
from fractions import Fraction
from itertools import product

F = Fraction
ZERO_F = F(0)
ONE_F = F(1)
CLASSICAL_POLICY = "fixed_ABK_mutually_exclusive_policy"
LT_POLICY = "fixed_half_A_half_literal_C00_policy"
INPUT_TYPE = "positive_orthant_3"
BRIGHT_TYPE = "positive_orthant_2"
LT_TYPE = "filtered_Lt_3_5_cell00_face"
SCALAR_TYPE = "positive_scalar_weight"
LETTERS = ("A", "B")


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Use exact integers or Fractions")
    return F(value)


def _vector(values, dimension, *, positive=False):
    values = tuple(rational(value) for value in values)
    if len(values) != dimension or (positive and any(value < 0 for value in values)):
        raise ValueError("Vector must have the declared dimension and positivity")
    return values


def _natural(value):
    if type(value) is not int or value < 0:
        raise ValueError("A length/event id must be a nonnegative built-in integer")
    return value


def _name(value):
    if type(value) is not str or not value:
        raise ValueError("Use a complete nonempty built-in string label")
    return value


def word(values):
    if isinstance(values, str):
        raise TypeError("Supply a sequence of full retained letters, not one string")
    values = tuple(values)
    if any(type(value) is not str or value not in LETTERS for value in values):
        raise ValueError("Only actual retained A/B letters are in this fixed interface")
    return values


def prepend_word(prefix, suffix):
    """Chronological prefix shift; neither order nor nominal labels are erased."""
    return word(prefix) + word(suffix)


def silent_map(x, letter):
    """Signed linear map of one mutually exclusive outcome of the fixed policy."""
    x0, x1, dark = _vector(x, 3)
    if type(letter) is not str or letter not in LETTERS:
        raise ValueError("No hidden branch id, epsilon step or alternative policy is exposed")
    return (x1 / 4, x0 / 4, dark / 2) if letter == "A" else (x0 / 4, x1 / 4, dark / 2)


def hidden_A_parts(x):
    """Two internal identical half-branches; no extra retained path labels exist."""
    half = tuple(value / 2 for value in silent_map(x, "A"))
    return half, half


def commit_map(x):
    x0, x1, _ = _vector(x, 3)
    return x0 / 2, x1 / 2


def word_map(x, retained_word):
    x = _vector(x, 3)
    for letter in word(retained_word):
        x = silent_map(x, letter)
    return x


def first_commit_residual(x, retained_word):
    """K S_last ... S_first x, with unnormalized branches summed before selection."""
    x0, x1, _ = _vector(x, 3)
    retained_word = word(retained_word)
    if retained_word.count("A") % 2:
        x0, x1 = x1, x0
    factor = F(1, 2 * 4 ** len(retained_word))
    return factor * x0, factor * x1


def coordinate_matrix(retained_word):
    retained_word = word(retained_word)
    columns = tuple(
        first_commit_residual(tuple(int(i == j) for i in range(3)), retained_word) for j in range(3)
    )
    return tuple(tuple(columns[j][i] for j in range(3)) for i in range(2))


@dataclass(frozen=True)
class PriorRecord:
    event_id: int
    action: str
    outcome: str
    settings: tuple = ()
    payload: tuple = ()
    precursor: tuple = ()

    def __post_init__(self):
        _natural(self.event_id)
        _name(self.action)
        _name(self.outcome)
        if isinstance(self.settings, str):
            raise TypeError("Retain full prior setting labels")
        settings = tuple(_name(value) for value in self.settings)
        payload = tuple(tuple(pair) for pair in self.payload)
        if any(len(pair) != 2 or any(type(v) is not str for v in pair) for pair in payload):
            raise ValueError("Prior payload must retain immutable string key/value pairs")
        precursor = tuple(self.precursor)
        if any(type(i) is not int or not 0 <= i < self.event_id for i in precursor):
            raise ValueError("Prior precursor ids must come from the earlier same-origin prefix")
        if len(set(precursor)) != len(precursor):
            raise ValueError("Do not duplicate a prior event")
        object.__setattr__(self, "settings", settings)
        object.__setattr__(self, "payload", payload)
        object.__setattr__(self, "precursor", precursor)


@dataclass(frozen=True)
class Context:
    policy: str = CLASSICAL_POLICY
    prior: tuple = ()
    initial_pending: tuple = ()
    origin: str = "record_origin"
    controller: str = "fixed_stationary_controller"
    source_type: str = field(init=False)
    output_type: str = field(init=False)
    frame: str = field(init=False)

    def __post_init__(self):
        if self.policy not in (CLASSICAL_POLICY, LT_POLICY):
            raise ValueError("Declare one of the two fixed complete policy fixtures")
        _name(self.origin)
        _name(self.controller)
        prior = tuple(self.prior)
        if any(
            type(record) is not PriorRecord or record.event_id != i
            for i, record in enumerate(prior)
        ):
            raise ValueError("Retain the complete contiguous prior record prefix")
        classical = self.policy == CLASSICAL_POLICY
        object.__setattr__(self, "prior", prior)
        object.__setattr__(self, "initial_pending", word(self.initial_pending))
        object.__setattr__(self, "source_type", INPUT_TYPE if classical else LT_TYPE)
        object.__setattr__(self, "output_type", BRIGHT_TYPE if classical else LT_TYPE)
        object.__setattr__(self, "frame", "fixed_orthant_coordinates" if classical else LT_TYPE)

    @property
    def precursor(self):
        return tuple((self.origin, record.event_id) for record in self.prior)


@dataclass(frozen=True)
class State:
    context: Context
    residual: tuple

    def __post_init__(self):
        if type(self.context) is not Context or self.context.policy != CLASSICAL_POLICY:
            raise TypeError("The classical input requires its fixed complete-policy context")
        residual = _vector(self.residual, 3, positive=True)
        if sum(residual, F(0)) != 1:
            raise ValueError("Source snapshot must have faithful mass one")
        object.__setattr__(self, "residual", residual)


@dataclass(frozen=True)
class CommitLabel:
    context: Context
    new_word: tuple
    outcome: object
    output_type: str

    def __post_init__(self):
        if type(self.context) is not Context:
            raise TypeError("Retain the complete declared context")
        new_word = word(self.new_word)
        expected = "K" if self.context.policy == CLASSICAL_POLICY else (0, 0)
        if self.context.policy == LT_POLICY and any(letter != "A" for letter in new_word):
            raise ValueError("The one-cell policy retains only its actual A outcomes")
        if self.outcome != expected or self.output_type != self.context.output_type:
            raise ValueError("Do not merge different committing outcomes or residual types")
        if isinstance(self.outcome, tuple) and any(type(bit) is not int for bit in self.outcome):
            raise ValueError("Cell labels use built-in integer bits")
        object.__setattr__(self, "new_word", new_word)

    @property
    def actual_word(self):
        return self.context.initial_pending + self.new_word

    @property
    def event_id(self):
        return len(self.context.prior)

    @property
    def precursor(self):
        return self.context.precursor


@dataclass(frozen=True)
class CommitCoordinate:
    source: State
    new_word: tuple
    residual: tuple = field(init=False)
    label: CommitLabel = field(init=False)

    def __post_init__(self):
        if type(self.source) is not State:
            raise TypeError(
                "A coordinate requires the retained normalized source, not a terminal audit"
            )
        new_word = word(self.new_word)
        object.__setattr__(self, "new_word", new_word)
        object.__setattr__(self, "residual", first_commit_residual(self.source.residual, new_word))
        object.__setattr__(
            self, "label", CommitLabel(self.source.context, new_word, "K", BRIGHT_TYPE)
        )

    @property
    def mass(self):
        return sum(self.residual, F(0))


@dataclass(frozen=True)
class GeometricFirstCommit:
    """Symbolic countable output; methods are exact queries, not an infinite enumeration."""

    source: State

    def __post_init__(self):
        if type(self.source) is not State:
            raise TypeError("The symbolic law requires the fixed positive input State")

    def coordinate(self, retained_word):
        return CommitCoordinate(self.source, retained_word)

    def truncation(self, horizon):
        horizon = _natural(horizon)
        if horizon > 12:
            raise ValueError(
                "Only bounded explicit supplements are enumerated; query symbolic tails instead"
            )
        return tuple(self.coordinate(w) for n in range(horizon) for w in product(LETTERS, repeat=n))

    def level_mass(self, length):
        return sum(self.source.residual[:2], F(0)) / 2 ** (_natural(length) + 1)

    def tail_mass(self, horizon):
        """Remaining EVER-commit output mass, not the full survival functional."""
        return sum(self.source.residual[:2], F(0)) / 2 ** _natural(horizon)

    def partial_mass(self, horizon):
        return self.total_mass - self.tail_mass(horizon)

    def survival_mass(self, horizon):
        return self.never_mass + self.tail_mass(horizon)

    @property
    def total_mass(self):
        """Explicit word-forgetting scalar question, not an equality of full outputs."""
        return sum(self.source.residual[:2], F(0))

    @property
    def never_mass(self):
        """A scalar limit only: there is no never-commit residual or appended event."""
        return self.source.residual[2]


@dataclass(frozen=True)
class UniformEffectCertificate:
    input_type: str = BRIGHT_TYPE
    output_type: str = SCALAR_TYPE
    bound: F = ONE_F
    proof_rule: str = "three_rows_in_unit_coefficient_box"

    def __post_init__(self):
        bound = rational(self.bound)
        if (self.input_type, self.output_type, bound, self.proof_rule) != (
            BRIGHT_TYPE,
            SCALAR_TYPE,
            F(1),
            "three_rows_in_unit_coefficient_box",
        ):
            raise ValueError("Supply the stated uniform positive-contraction certificate")
        object.__setattr__(self, "bound", bound)


@dataclass(frozen=True)
class WordEffect:
    """A last-NEW-letter family, with a separate empty-new-suffix row.

    The fixed initial pending word remains in the retained context; it is
    neither replayed nor substituted for an empty new suffix. Finite
    coefficient checks prove this family's uniform contraction bound.
    """

    empty: tuple
    after_A: tuple
    after_B: tuple
    certificate: UniformEffectCertificate

    def __post_init__(self):
        if type(self.certificate) is not UniformEffectCertificate:
            raise TypeError(
                "No word-dependent continuation without its checked uniform certificate"
            )
        for name in ("empty", "after_A", "after_B"):
            row = _vector(getattr(self, name), 2, positive=True)
            if any(value > 1 for value in row):
                raise ValueError("Unbounded/noncontractive coefficients are outside this interface")
            object.__setattr__(self, name, row)

    def apply(self, coordinate):
        if type(coordinate) is not CommitCoordinate or coordinate.label.output_type != BRIGHT_TYPE:
            raise TypeError("Use the matching full bright-pair committing coordinate")
        w = coordinate.new_word
        row = self.empty if not w else self.after_A if w[-1] == "A" else self.after_B
        value = sum((a * b for a, b in zip(row, coordinate.residual, strict=True)), F(0))
        return ScalarCoordinate(coordinate, value)


@dataclass(frozen=True)
class ScalarCoordinate:
    original: CommitCoordinate
    weight: F
    output_type: str = SCALAR_TYPE

    def __post_init__(self):
        if type(self.original) is not CommitCoordinate or self.output_type != SCALAR_TYPE:
            raise TypeError("Retain the exact original label and the separate scalar output type")
        weight = rational(self.weight)
        if weight < 0 or weight > self.original.mass:
            raise ValueError("A positive contraction cannot enlarge branch mass")
        object.__setattr__(self, "weight", weight)

    @property
    def label(self):
        return self.original.label


@dataclass(frozen=True)
class ContinuedSeries:
    series: GeometricFirstCommit
    effect: WordEffect

    def __post_init__(self):
        if type(self.series) is not GeometricFirstCommit or type(self.effect) is not WordEffect:
            raise TypeError("Use a declared symbolic series and uniformly certified effect family")

    def coordinate(self, retained_word):
        return self.effect.apply(self.series.coordinate(retained_word))

    def level_weight(self, length):
        length = _natural(length)
        if length == 0:
            return self.coordinate(()).weight
        if length == 1:
            return self.coordinate(("A",)).weight + self.coordinate(("B",)).weight
        coefficient_sum = sum(self.effect.after_A + self.effect.after_B, F(0))
        return self.series.total_mass * coefficient_sum / 2 ** (length + 3)

    def tail_weight(self, horizon):
        horizon = _natural(horizon)
        if horizon == 0:
            return self.level_weight(0) + self.tail_weight(1)
        if horizon == 1:
            return self.level_weight(1) + self.tail_weight(2)
        coefficient_sum = sum(self.effect.after_A + self.effect.after_B, F(0))
        return self.series.total_mass * coefficient_sum / 2 ** (horizon + 2)

    @property
    def total_weight(self):
        return self.tail_weight(0)


@dataclass(frozen=True)
class Bloch:
    """Positive filtered Hermitian2 coordinate sigma=(qI+xX+yY+zZ)/2."""

    q: F
    x: F = ZERO_F
    y: F = ZERO_F
    z: F = ZERO_F

    def __post_init__(self):
        q, x, y, z = tuple(rational(getattr(self, name)) for name in ("q", "x", "y", "z"))
        if q < 0 or q * q < x * x + y * y + z * z:
            raise ValueError("The exact filtered block must be positive semidefinite")
        for name, value in zip(("q", "x", "y", "z"), (q, x, y, z), strict=True):
            object.__setattr__(self, name, value)

    def scaled(self, coefficient):
        coefficient = rational(coefficient)
        if coefficient < 0:
            raise ValueError("Only positive cone scaling is used by this finite supplement")
        return Bloch(*(coefficient * getattr(self, name) for name in ("q", "x", "y", "z")))


def lt_control_A(block):
    """Existing common-X congruence on the accepted filtered cell00 face."""
    if type(block) is not Bloch:
        raise TypeError("Use the exact filtered representation of the accepted L_t face")
    return Bloch(
        block.q, block.x, (-7 * block.y - 24 * block.z) / 25, (24 * block.y - 7 * block.z) / 25
    )


@dataclass(frozen=True)
class LtFaceState:
    context: Context
    residual: Bloch

    def __post_init__(self):
        if type(self.context) is not Context or self.context.policy != LT_POLICY:
            raise TypeError(
                "Declare the fixed half-silent/half-literal-cut policy on this old face"
            )
        if type(self.residual) is not Bloch or self.residual.q != 1:
            raise ValueError("The supplied face snapshot must have filtered/native mass one")


@dataclass(frozen=True)
class LtCoordinate:
    source: LtFaceState
    length: int
    residual: Bloch = field(init=False)
    label: CommitLabel = field(init=False)

    def __post_init__(self):
        if type(self.source) is not LtFaceState:
            raise TypeError("Use the retained existing-face source, not a terminal output")
        length = _natural(self.length)
        block = self.source.residual
        for _ in range(length):
            block = lt_control_A(block)
        object.__setattr__(self, "residual", block.scaled(F(1, 2 ** (length + 1))))
        object.__setattr__(
            self, "label", CommitLabel(self.source.context, ("A",) * length, (0, 0), LT_TYPE)
        )

    @property
    def mass(self):
        return self.residual.q


@dataclass(frozen=True)
class LtFaceSeries:
    source: LtFaceState

    def __post_init__(self):
        if type(self.source) is not LtFaceState:
            raise TypeError("Use the explicitly declared existing-face fixed-policy source")

    def coordinate(self, length):
        return LtCoordinate(self.source, length)

    def tail_mass(self, horizon):
        return F(1, 2 ** _natural(horizon))

    @property
    def never_mass(self):
        return F(0)


@dataclass(frozen=True)
class SelectedCommit:
    coordinate: object
    record: CommitLabel = field(init=False)
    probability: F = field(init=False)
    residual: object = field(init=False)

    def __post_init__(self):
        if type(self.coordinate) not in (CommitCoordinate, LtCoordinate):
            raise TypeError(
                "Only a linear residual coordinate can supply a selected committing output"
            )
        probability = self.coordinate.mass
        if probability <= 0:
            raise ValueError("Never normalize or append a zero-weight committing branch")
        residual = self.coordinate.residual
        normalized = (
            residual.scaled(1 / probability)
            if type(residual) is Bloch
            else tuple(value / probability for value in residual)
        )
        object.__setattr__(self, "record", self.coordinate.label)
        object.__setattr__(self, "probability", probability)
        object.__setattr__(self, "residual", normalized)

    @property
    def records(self):
        return self.record.context.prior + (self.record,)


def select_commit(coordinate):
    return SelectedCommit(coordinate)


@dataclass(frozen=True)
class TerminalScalar:
    """A scalar mathematical continuation on a lawful literal-cut coordinate.

    It retains that coordinate's full label and adds the fixed cell/sign
    question. It is not a replacement terminal-first-commit instrument,
    a post-read residual or an additional physical-availability claim.
    """

    coordinate: LtCoordinate
    sign: str
    weight: F = field(init=False)
    output_type: str = field(init=False, default=SCALAR_TYPE)

    def __post_init__(self):
        if (
            type(self.coordinate) is not LtCoordinate
            or type(self.sign) is not str
            or self.sign not in ("+", "-")
        ):
            raise TypeError("Retain the full existing-face coordinate and fixed tilted sign label")
        block = self.coordinate.residual
        difference = (3 * block.x + 4 * block.z) / 5
        object.__setattr__(
            self, "weight", (block.q + (1 if self.sign == "+" else -1) * difference) / 2
        )

    @property
    def full_label(self):
        return self.coordinate.label, (0, 0, self.sign)


def epsilon_candidate(bright, dark, coefficient):
    """Separate scalar fixed-point diagnostic, not an epsilon branch of the A/B policy.

    For S_epsilon=diag(1/2,1), B=(1/2,0), bright+c*dark solves T=B+TS.
    Only c=0 is the least series solution; c>0 invents a never-commit output.
    """
    bright, dark, coefficient = (rational(value) for value in (bright, dark, coefficient))
    if min(bright, dark, coefficient) < 0:
        raise ValueError("This diagnostic compares positive scalar candidates")
    return bright + coefficient * dark
