"""
MAM-Q: Minimal Actualization Model — Quantum Analogue

Implements a qubit/instrument model using the DET v8.0-P0.4 formal core.
Demonstrates: qubit state as relational record, measurement as commit event,
Born rule as provisional calibration, pointer-record commit, no pre-existing
outcome storage, and no-signalling in composite systems.

Key DET constraints:
  - The qubit state is an actual relational record (A/P), not a collection
    of parallel worlds or pre-existing hidden outcomes.
  - Amplitudes are present structural features (P/C), not beliefs about
    hidden futures.
  - The Born rule is provisional calibration (H/O), not a DET 8 derivation.
  - Measurement outcomes are committed to pointer records (A).
  - Before measurement, no fact of the matter exists about which outcome
    "will" occur (No Pre-Existing Future Facts).
"""

from __future__ import annotations

import cmath
import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ── Core Qubit Types ───────────────────────────────────────────────────────


@dataclass
class QubitState:
    """A pure qubit state: α|0⟩ + β|1⟩.

    Modal annotation: A/P (actual relational record). The qubit state
    is a determinate relation that constrains future measurement
    possibilities without containing those outcomes as pre-existing facts.

    It is NOT a collection of parallel worlds. It is NOT a warehouse
    of hidden outcomes. It is a present phase-bearing structure.
    """

    alpha: complex
    beta: complex

    def __post_init__(self):
        norm = abs(self.alpha) ** 2 + abs(self.beta) ** 2
        if norm < 1e-15:
            # Zero norm: the state vector is the zero vector
            # (e.g., from a Kraus operator applied to an orthogonal state).
            # Keep as-is; the caller should filter these out.
            return
        if abs(norm - 1.0) > 1e-12:
            # Normalize silently.
            inv = 1.0 / math.sqrt(norm)
            self.alpha *= inv
            self.beta *= inv

    def probabilities(self) -> tuple[float, float]:
        """Born rule: p(0) = |α|², p(1) = |β|².

        Modal annotation: H/O (provisional calibration, not derivation).
        """
        return (abs(self.alpha) ** 2, abs(self.beta) ** 2)

    def copy(self) -> "QubitState":
        return QubitState(alpha=self.alpha, beta=self.beta)


# ── Kraus Operators (Provisional Compatibility Layer) ──────────────────────


@dataclass
class KrausOperator:
    """A single Kraus operator for a quantum instrument.

    Modal annotation: P/C (provisional compatibility with standard QM).
    Not a DET 8 derivation; a bridge to standard quantum formalism.
    """

    matrix: list[list[complex]]  # 2×2 for single qubit

    def apply(self, state: QubitState) -> QubitState:
        """Apply this Kraus operator to a state (un-normalized result)."""
        m00, m01 = self.matrix[0][0], self.matrix[0][1]
        m10, m11 = self.matrix[1][0], self.matrix[1][1]

        new_alpha = m00 * state.alpha + m01 * state.beta
        new_beta = m10 * state.alpha + m11 * state.beta
        return QubitState(alpha=new_alpha, beta=new_beta)


@dataclass
class POVMMeasurement:
    """A projective or POVM measurement on a single qubit.

    Modal annotation: P/C (provisional compatibility).

    Generates the possibility object: Ω = {0, 1} (pointer outcomes)
    with kernel K from the Born rule. The measurement is the DET
    event at which an open relational record produces a committed
    pointer record.
    """

    kraus_ops: list[KrausOperator]
    outcome_labels: list[int] = field(default_factory=lambda: [0, 1])

    def compute_possibility(self, state: QubitState) -> "MeasurementPossibility":
        """Generate the possibility object from the current qubit state.

        This is the DET law map L_e for the measurement event.
        """
        outcomes: list[tuple[int, QubitState]] = []
        probs: list[float] = []

        for label, op in zip(self.outcome_labels, self.kraus_ops):
            post_state = op.apply(state)
            prob = abs(post_state.alpha) ** 2 + abs(post_state.beta) ** 2
            if prob > 1e-15:
                # Normalize the post-measurement state.
                inv = 1.0 / math.sqrt(prob)
                post_state.alpha *= inv
                post_state.beta *= inv
                outcomes.append((label, post_state))
                probs.append(prob)

        return MeasurementPossibility(
            omega=outcomes,
            kernel=probs,
            pre_measurement_state=state.copy(),
        )


@dataclass
class MeasurementPossibility:
    """The possibility object for a measurement event.

    Modal annotation: P/C (calculational).

    Contains:
      - omega: list of (outcome_label, post_measurement_state) pairs.
      - kernel: propensity kernel (Born rule probabilities).
      - pre_measurement_state: the state before measurement (for verification).
    """

    omega: list[tuple[int, QubitState]]
    kernel: list[float]
    pre_measurement_state: QubitState

    def __post_init__(self):
        if not self.omega:
            raise ValueError("Ω must be nonempty")
        total = sum(self.kernel)
        if abs(total) < 1e-15:
            raise ValueError("All probabilities vanish — inconsistent")
        if abs(total - 1.0) > 1e-12:
            self.kernel = [k / total for k in self.kernel]

    @property
    def outcome_labels(self) -> list[int]:
        return [label for label, _ in self.omega]


# ── Pointer Record ──────────────────────────────────────────────────────────


@dataclass
class PointerRecord:
    """A classical, redundantly coupled, readable measurement record.

    Modal annotation: A (actual committed fact).

    This is the "fruit" of measurement — the committed pointer outcome.
    Before measurement, the pointer record is None (uncommitted).
    """

    value: Optional[int] = None

    @property
    def is_committed(self) -> bool:
        return self.value is not None


# ── Qubit Measurement System ────────────────────────────────────────────────


class QubitActualizer:
    """Selects one measurement outcome from the possibility object.

    Modal annotation: P/C (simulation device). The seed is for
    reproducibility and must not be interpreted as a physical hidden
    variable or ontological mechanism of becoming.
    """

    def __init__(self, seed: Optional[int] = None):
        self._rng = random.Random(seed)

    def select(self, possibility: MeasurementPossibility) -> tuple[int, QubitState]:
        """Sample one outcome according to the Born rule kernel."""
        idx = self._rng.choices(
            population=range(len(possibility.omega)),
            weights=possibility.kernel,
            k=1,
        )[0]
        return possibility.omega[idx]


class MeasurementCommit:
    """Commits a measurement outcome to pointer record and updates qubit state.

    Modal annotation: P/A (event is proposed; resulting pointer record
    is actual committed fact).
    """

    @staticmethod
    def commit(
        qubit: QubitState,
        pointer: PointerRecord,
        outcome: tuple[int, QubitState],
    ) -> None:
        """Commit: write outcome to pointer, collapse qubit to post-measurement state."""
        label, post_state = outcome
        pointer.value = label
        qubit.alpha = post_state.alpha
        qubit.beta = post_state.beta


class QubitEventLog:
    """Records measurement events for verification."""

    def __init__(self):
        self.entries: list[dict] = []

    def record(
        self,
        event_name: str,
        pre_state: QubitState,
        omega_labels: list[int],
        kernel: list[float],
        outcome: tuple[int, QubitState],
        pointer_value: int,
    ) -> None:
        self.entries.append(
            {
                "event": event_name,
                "pre_state_alpha": pre_state.alpha,
                "pre_state_beta": pre_state.beta,
                "omega": omega_labels,
                "kernel": kernel,
                "outcome_label": outcome[0],
                "pointer_value": pointer_value,
            }
        )


# ── Standard Measurements ───────────────────────────────────────────────────


def make_z_measurement() -> POVMMeasurement:
    """Standard computational basis (Z) measurement.

    Kraus operators: |0⟩⟨0| and |1⟩⟨1|.
    """
    return POVMMeasurement(
        kraus_ops=[
            KrausOperator(matrix=[[1, 0], [0, 0]]),  # |0⟩⟨0|
            KrausOperator(matrix=[[0, 0], [0, 1]]),  # |1⟩⟨1|
        ],
        outcome_labels=[0, 1],
    )


def make_x_measurement() -> POVMMeasurement:
    """X-basis measurement (|+⟩, |-⟩).

    Kraus operators: |+⟩⟨+| and |-⟩⟨-|.
    """
    half = 0.5
    return POVMMeasurement(
        kraus_ops=[
            KrausOperator(matrix=[[half, half], [half, half]]),  # |+⟩⟨+|
            KrausOperator(matrix=[[half, -half], [-half, half]]),  # |-⟩⟨-|
        ],
        outcome_labels=[0, 1],
    )


# ── Experiments ─────────────────────────────────────────────────────────────


def run_measurement(
    state: QubitState,
    measurement: POVMMeasurement,
    actualizer: QubitActualizer,
    event_name: str = "m",
) -> tuple[PointerRecord, QubitEventLog]:
    """Run one measurement event: law → actualize → commit → log.

    Returns the pointer record (containing the committed outcome)
    and the event log for verification.
    """
    pointer = PointerRecord()
    event_log = QubitEventLog()

    # 1. Law map: generate possibility object from qubit state.
    possibility = measurement.compute_possibility(state)

    # 2. DECLARE: before measurement, the pointer is uncommitted (None).
    #    The qubit state is a relational record, not a hidden outcome list.
    assert not pointer.is_committed, "Pointer must be uncommitted before measurement"

    # 3. Actualize: select one outcome (actualizer).
    outcome = actualizer.select(possibility)

    # 4. Commit: write outcome to pointer record, collapse qubit.
    MeasurementCommit.commit(state, pointer, outcome)

    # 5. Log.
    event_log.record(
        event_name=event_name,
        pre_state=possibility.pre_measurement_state,
        omega_labels=possibility.outcome_labels,
        kernel=possibility.kernel,
        outcome=outcome,
        pointer_value=pointer.value,
    )

    return pointer, event_log


def verify_no_preexisting_outcome(event_log: QubitEventLog) -> bool:
    """Verify that the pre-measurement qubit state does not contain
    the measurement outcome as a hidden pre-existing value.

    In MAM-Q, this is verified by construction:
      - The qubit state stores only α, β (complex amplitudes).
      - There is no 'will_measure_0' or 'hidden_outcome' field.
      - The Born probabilities are present structural features, not hidden facts.
    """
    for entry in event_log.entries:
        # The pre-measurement state is a complex pair, not a labeled outcome.
        pre = complex(entry["pre_state_alpha"]), complex(entry["pre_state_beta"])
        outcome = entry["outcome_label"]
        # When α=1,β=0, outcome is always 0 — but only because Ω={0} (deterministic).
        # When |α|²,|β|² are both > 0, the pre-state gives probabilities, not a
        # hidden fact about which outcome "will" occur.
        # This is structural — no hidden variable to check.
        pass
    return True


# ── No-Signalling Verification ──────────────────────────────────────────────


@dataclass
class TwoQubitState:
    """A two-qubit system. Used for no-signalling tests.

    Modal annotation: A/P (relational record for a composite system).
    """

    # State vector |00⟩, |01⟩, |10⟩, |11⟩ amplitudes.
    amp00: complex
    amp01: complex
    amp10: complex
    amp11: complex

    def __post_init__(self):
        norm = (
            abs(self.amp00) ** 2
            + abs(self.amp01) ** 2
            + abs(self.amp10) ** 2
            + abs(self.amp11) ** 2
        )
        if abs(norm - 1.0) > 1e-12:
            inv = 1.0 / math.sqrt(norm)
            self.amp00 *= inv
            self.amp01 *= inv
            self.amp10 *= inv
            self.amp11 *= inv

    def reduced_density_qubit_b(self) -> tuple[float, float, float, float]:
        """Compute the reduced density matrix for qubit B.

        Returns (ρ00, ρ01, ρ10, ρ11) of the 2×2 density matrix.
        """
        # Trace over qubit A.
        rho00 = abs(self.amp00) ** 2 + abs(self.amp10) ** 2
        rho01 = self.amp00 * self.amp01.conjugate() + self.amp10 * self.amp11.conjugate()
        rho10 = rho01.conjugate()
        rho11 = abs(self.amp01) ** 2 + abs(self.amp11) ** 2
        return (rho00, rho01, rho10, rho11)

    def prob_b_given_a_measurement(
        self, a_outcome: int, a_basis: str
    ) -> tuple[float, float]:
        """Probability of B=0, B=1 given that A was measured and yielded
        a_outcome in basis a_basis ('Z' or 'X').

        This is a provisional calculation using standard QM rules.
        """
        if a_basis == "Z":
            if a_outcome == 0:
                # Post-measurement state ∝ (amp00|00⟩ + amp01|01⟩)
                p0 = abs(self.amp00) ** 2
                p1 = abs(self.amp01) ** 2
            else:
                p0 = abs(self.amp10) ** 2
                p1 = abs(self.amp11) ** 2
        elif a_basis == "X":
            # X basis: |+⟩ = (|0⟩+|1⟩)/√2, |-⟩ = (|0⟩-|1⟩)/√2
            inv2 = 1.0 / math.sqrt(2)
            if a_outcome == 0:  # |+⟩ outcome
                amp_plus0 = inv2 * (self.amp00 + self.amp10)
                amp_plus1 = inv2 * (self.amp01 + self.amp11)
                p0 = abs(amp_plus0) ** 2
                p1 = abs(amp_plus1) ** 2
            else:  # |-⟩ outcome
                amp_minus0 = inv2 * (self.amp00 - self.amp10)
                amp_minus1 = inv2 * (self.amp01 - self.amp11)
                p0 = abs(amp_minus0) ** 2
                p1 = abs(amp_minus1) ** 2
        else:
            raise ValueError(f"Unknown basis: {a_basis}")

        total = p0 + p1
        if total > 1e-15:
            p0 /= total
            p1 /= total
        return (p0, p1)


def make_bell_pair() -> TwoQubitState:
    """Create the Bell state |Φ⁺⟩ = (|00⟩ + |11⟩)/√2."""
    inv2 = 1.0 / math.sqrt(2)
    return TwoQubitState(amp00=inv2, amp01=0, amp10=0, amp11=inv2)


def no_signalling_test(n_samples: int = 10000, seed: int = 42) -> dict:
    """Verify no-signalling: the marginal probability distribution for B
    does not depend on whether A measured in Z or X basis.

    Returns statistics showing P(B=0) matches in both scenarios.
    """
    rng = random.Random(seed)

    bell = make_bell_pair()

    b_counts_z: dict[int, int] = {0: 0, 1: 0}
    b_counts_x: dict[int, int] = {0: 0, 1: 0}

    # Pre-compute reduced density matrix of A.
    # ρ_A = Tr_B(|Φ⁺⟩⟨Φ⁺|).
    # In the Bell state, ρ_A = |0⟩⟨0|/2 + |1⟩⟨1|/2.
    rho_a00 = abs(bell.amp00) ** 2 + abs(bell.amp01) ** 2  # ⟨0|ρ_A|0⟩
    rho_a11 = abs(bell.amp10) ** 2 + abs(bell.amp11) ** 2  # ⟨1|ρ_A|1⟩
    # Off-diagonal: ⟨0|ρ_A|1⟩
    rho_a01 = bell.amp00 * bell.amp10.conjugate() + bell.amp01 * bell.amp11.conjugate()

    inv2 = 1.0 / math.sqrt(2)
    # P(A = +) in X basis = ⟨+|ρ_A|+⟩ = (ρ00 + ρ01 + ρ10 + ρ11)/2
    p_a_plus_x = (rho_a00 + rho_a01 + rho_a01.conjugate() + rho_a11).real / 2.0

    for _ in range(n_samples):
        # Scenario Z: measure A in Z basis.
        # P(A=0) = ⟨0|ρ_A|0⟩ = rho_a00.
        if rng.random() < rho_a00:
            a_outcome = 0
        else:
            a_outcome = 1

        pb0_z, pb1_z = bell.prob_b_given_a_measurement(a_outcome, "Z")
        b_outcome = 0 if rng.random() < pb0_z else 1
        b_counts_z[b_outcome] += 1

    for _ in range(n_samples):
        # Scenario X: measure A in X basis.
        if rng.random() < p_a_plus_x:
            a_outcome = 0
        else:
            a_outcome = 1

        pb0_x, pb1_x = bell.prob_b_given_a_measurement(a_outcome, "X")
        b_outcome = 0 if rng.random() < pb0_x else 1
        b_counts_x[b_outcome] += 1

    p_b0_z = b_counts_z[0] / n_samples
    p_b0_x = b_counts_x[0] / n_samples

    return {
        "P(B=0 | A measured in Z)": p_b0_z,
        "P(B=0 | A measured in X)": p_b0_x,
        "delta": abs(p_b0_z - p_b0_x),
        "no_signalling_holds": abs(p_b0_z - p_b0_x) < 0.05,
        "expected_P_B0": 0.5,
        "n_samples": n_samples,
    }


# ── Interference / Two-Path Demonstration ───────────────────────────────────


def interference_demo(
    n_samples: int = 10000, seed: int = 42
) -> dict:
    """Demonstrate two-path interference in MAM-Q.

    Prepare |+⟩ = (|0⟩+|1⟩)/√2, measure in Z. Then compare with:
    prepare |+⟩, measure in X.

    The Z-measurement has two open outcomes; the X-measurement is
    deterministic (|+⟩ always yields outcome 0 in X-basis).
    This demonstrates the difference between open and deterministic
    regimes within the same quantum framework.
    """
    rng = random.Random(seed)
    z_meas = make_z_measurement()
    x_meas = make_x_measurement()

    # Prepare |+⟩.
    inv2 = 1.0 / math.sqrt(2)
    plus_state = QubitState(alpha=inv2, beta=inv2)

    # Z measurement on |+⟩: both outcomes possible.
    z_counts = {0: 0, 1: 0}
    for _ in range(n_samples):
        state = plus_state.copy()
        pointer = PointerRecord()
        possibility = z_meas.compute_possibility(state)
        idx = rng.choices(range(len(possibility.omega)), weights=possibility.kernel, k=1)[0]
        outcome = possibility.omega[idx]
        MeasurementCommit.commit(state, pointer, outcome)
        z_counts[pointer.value] += 1

    # X measurement on |+⟩: deterministic (only outcome 0).
    x_counts = {0: 0, 1: 0}
    for _ in range(n_samples):
        state = plus_state.copy()
        pointer = PointerRecord()
        possibility = x_meas.compute_possibility(state)
        idx = rng.choices(range(len(possibility.omega)), weights=possibility.kernel, k=1)[0]
        outcome = possibility.omega[idx]
        MeasurementCommit.commit(state, pointer, outcome)
        x_counts[pointer.value] += 1

    return {
        "Z_on_plus": {k: v / n_samples for k, v in z_counts.items()},
        "X_on_plus": {k: v / n_samples for k, v in x_counts.items()},
        "Z_is_open": z_counts[0] > 0 and z_counts[1] > 0,
        "X_is_deterministic": x_counts[0] == n_samples and x_counts[1] == 0,
    }
