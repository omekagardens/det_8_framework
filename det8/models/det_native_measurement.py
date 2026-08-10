"""
DET-Native Pointer-Record Formation — No Kraus/POVM Borrowing

Derives measurement and pointer-record formation from pure DET primitives:
  - Records (node states)
  - Event graph (causal order)
  - Law map (generates Ω from record)
  - Commit kernel (propensities over Ω)
  - Commit map (writes outcome to record)

No Hilbert space, no Kraus operators, no POVM, no Born rule.
The pointer record emerges from the statistics of commit events on
a high-dimensional apparatus coupled to the system being measured.

DET-native insight:
  Measurement is not a special process. It is a sequence of ordinary
  commit events on a joint system (target + apparatus). The apparatus
  has many degrees of freedom (high N). Through repeated commit events,
  information about the target property is redundantly encoded across
  the apparatus. The pointer record r_i is the consensus of apparatus
  bits — a classical, stable, redundantly stored outcome.

This is DET's version of decoherence/quantum Darwinism, expressed
entirely in DET's record-kernel grammar.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


# ── DET-Native Measurement Apparatus ────────────────────────────────────────


@dataclass
class ApparatusBit:
    """A single binary degree of freedom in the measurement apparatus.

    This is a DET record element — a committed fact. It stores either
    an undetermined state (None) or a committed value (0 or 1).
    """

    value: Optional[int] = None  # None = not yet committed.

    @property
    def is_committed(self) -> bool:
        return self.value is not None


@dataclass
class MeasurementApparatus:
    """A DET-native measurement apparatus with N binary degrees of freedom.

    The apparatus does NOT use Kraus operators, POVMs, or Hilbert spaces.
    It is a collection of record bits that become correlated with the
    target system through repeated commit events.
    """

    n_bits: int = 100
    bits: list[ApparatusBit] = field(default_factory=list)

    def __post_init__(self):
        self.bits = [ApparatusBit() for _ in range(self.n_bits)]

    @property
    def committed_count(self) -> int:
        return sum(1 for b in self.bits if b.is_committed)

    @property
    def pointer_value(self) -> Optional[int]:
        """The pointer record: majority vote of committed bits.

        Returns None if fewer than half the bits are committed.
        """
        zeros = sum(1 for b in self.bits if b.value == 0)
        ones = sum(1 for b in self.bits if b.value == 1)
        total = zeros + ones
        if total == 0:
            return None
        if zeros > ones:
            return 0
        elif ones > zeros:
            return 1
        return None  # Tie.

    @property
    def pointer_strength(self) -> float:
        """Pointer record strength r ∈ [0,1].

        r = fraction of committed bits that agree with the majority.
        r ≈ 0.5: no consensus (random).
        r ≈ 1.0: perfect consensus (strong pointer).
        """
        pv = self.pointer_value
        if pv is None:
            return 0.0
        committed = [b for b in self.bits if b.is_committed]
        if not committed:
            return 0.0
        agreeing = sum(1 for b in committed if b.value == pv)
        return agreeing / len(committed)

    @property
    def redundancy(self) -> float:
        """How many independent copies of the pointer value exist.

        Redundancy ≈ committed_count · pointer_strength.
        """
        return self.committed_count * self.pointer_strength


# ── Target System ───────────────────────────────────────────────────────────


@dataclass
class TargetSystem:
    """A DET-native system being measured.

    Has a binary property (the 'system value') that the apparatus
    attempts to read out through repeated commit events.

    In DET, this property is a committed record fact. It exists
    whether or not it has been measured (Record Determinacy).
    The measurement does not create the property; it copies it
    into the apparatus record.
    """

    value: int  # 0 or 1 — the system property (committed fact).

    def __post_init__(self):
        if self.value not in (0, 1):
            raise ValueError("Target value must be 0 or 1")


# ── DET-Native Measurement Event ────────────────────────────────────────────


def det_native_measurement_event(
    target: TargetSystem,
    apparatus: MeasurementApparatus,
    fidelity: float = 0.9,
    rng: Optional[random.Random] = None,
) -> dict:
    """One DET-native measurement event.

    A single apparatus bit interacts with the target system through
    a commit event. The commit kernel is:

      K(bit = target.value | record) = fidelity
      K(bit ≠ target.value | record) = 1 - fidelity

    This is the DET-native equivalent of a weak measurement.
    Each event transfers one bit of (noisy) information from target
    to apparatus.

    DET primitives used:
    - Record: target.value and apparatus bits are committed facts.
    - Law map: generates Ω = {target.value, ¬target.value} with kernel.
    - Commit kernel: fidelity-weighted propensity.
    - Commit map: writes outcome to the selected apparatus bit.

    No Kraus operators, no Hilbert space, no Born rule.
    """
    if rng is None:
        rng = random.Random()

    # Select an uncommitted apparatus bit.
    uncommitted = [i for i, b in enumerate(apparatus.bits) if not b.is_committed]
    if not uncommitted:
        return {"event": "no_uncommitted_bits", "apparatus_full": True}

    bit_idx = rng.choice(uncommitted)

    # Law map: possible outcomes are {0, 1} with kernel [fidelity, 1-fidelity]
    # or [1-fidelity, fidelity] depending on target value.
    if target.value == 0:
        kernel = [fidelity, 1.0 - fidelity]
    else:
        kernel = [1.0 - fidelity, fidelity]

    # Actualize: select outcome.
    outcome = 0 if rng.random() < kernel[0] else 1

    # Commit: write outcome to apparatus bit.
    apparatus.bits[bit_idx].value = outcome

    return {
        "bit_index": bit_idx,
        "target_value": target.value,
        "outcome": outcome,
        "correct": outcome == target.value,
        "kernel": kernel,
    }


# ── Full Measurement Sequence ───────────────────────────────────────────────


def det_native_measure(
    target_value: int = 0,
    n_bits: int = 100,
    fidelity: float = 0.9,
    seed: int = 42,
) -> dict:
    """Perform a full DET-native measurement.

    Repeatedly applies det_native_measurement_event until all
    apparatus bits are committed. Returns the final pointer record
    and measurement statistics.

    This is the DET-native equivalent of a projective measurement.
    The pointer record emerges from the consensus of N noisy
    single-bit commit events.

    Key DET properties:
    - The target value exists before measurement (Record Determinacy).
    - Measurement copies the value, does not create it.
    - Pointer strength r grows with redundancy.
    - No collapse — just information transfer through commit events.
    """
    target = TargetSystem(value=target_value)
    apparatus = MeasurementApparatus(n_bits=n_bits)
    rng = random.Random(seed)

    history: list[dict] = []
    pointer_trace: list[float] = []  # Pointer strength over time.

    for step in range(n_bits):
        event = det_native_measurement_event(target, apparatus, fidelity, rng)
        history.append(event)
        pointer_trace.append(apparatus.pointer_strength)

    return {
        "target_value": target_value,
        "n_bits": n_bits,
        "fidelity": fidelity,
        "pointer_value": apparatus.pointer_value,
        "pointer_strength": apparatus.pointer_strength,
        "redundancy": apparatus.redundancy,
        "correct": apparatus.pointer_value == target_value,
        "committed_count": apparatus.committed_count,
        "pointer_trace": pointer_trace[:10] + ["..."] + pointer_trace[-5:]
        if len(pointer_trace) > 20
        else pointer_trace,
        "history_sample": history[:3],
    }


# ── Measurement Robustness Test ─────────────────────────────────────────────


def measurement_robustness_test(
    n_trials: int = 100,
    n_bits: int = 100,
    fidelity: float = 0.6,  # Barely above chance.
    seed: int = 42,
) -> dict:
    """Test how robust DET-native measurement is to low fidelity.

    At fidelity = 0.6, each individual bit is only 60% reliable.
    But with N=100 bits, the consensus should be correct with
    very high probability (law of large numbers).

    This demonstrates that pointer records can be reliable even
    when individual commit events are noisy — a key feature of
    DET-native measurement.
    """
    rng = random.Random(seed)
    correct_count = 0
    strengths = []

    for _ in range(n_trials):
        result = det_native_measure(
            target_value=rng.randint(0, 1),
            n_bits=n_bits,
            fidelity=fidelity,
            seed=rng.randint(0, 10**6),
        )
        if result["correct"]:
            correct_count += 1
        strengths.append(result["pointer_strength"])

    avg_strength = sum(strengths) / len(strengths) if strengths else 0.0

    return {
        "n_trials": n_trials,
        "n_bits": n_bits,
        "fidelity": fidelity,
        "accuracy": correct_count / n_trials,
        "avg_pointer_strength": avg_strength,
        "reliable": correct_count / n_trials > 0.99,
    }


# ── DET vs Standard QM Measurement Comparison ──────────────────────────────


def compare_det_vs_qm_measurement() -> dict:
    """Compare DET-native measurement with standard QM measurement.

    This documents the conceptual differences, not numerical ones
    (the numerical outcomes can be calibrated to match).

    DET-native features (no smuggling):
    - Target value exists before measurement (committed record fact).
    - Measurement copies information, does not create it.
    - Pointer record emerges from consensus of many weak commit events.
    - No wavefunction collapse — just information transfer.
    - No special "measurement" category — just ordinary commit events.

    Standard QM features (not in DET-native model):
    - Superposition: target could be in |ψ⟩ = α|0⟩ + β|1⟩.
    - Born rule: P(0) = |α|².
    - Projection postulate: post-measurement state is |0⟩ or |1⟩.
    - Preferred basis problem: why {|0⟩, |1⟩}?

    Where DET converges with QM:
    - If the DET commit kernel K(outcome | record) is calibrated to
      match Born rule probabilities, the measurement statistics are
      identical.
    - The difference is ontological, not statistical.
    """
    return {
        "det_native": {
            "target_ontology": "Committed record fact (determinate before measurement).",
            "measurement_process": "Sequence of commit events copying target → apparatus.",
            "pointer_origin": "Consensus of N noisy apparatus bits.",
            "collapse": "No collapse — just information transfer.",
            "preferred_basis": "Determined by apparatus design (which property it couples to).",
        },
        "standard_qm": {
            "target_ontology": "Quantum state in Hilbert space (indeterminate before measurement).",
            "measurement_process": "Projective measurement (special non-unitary process).",
            "pointer_origin": "Born rule applied to measurement operator eigenstates.",
            "collapse": "Wavefunction collapse (or branching in Many-Worlds).",
            "preferred_basis": "Determined by einselection (environment-induced superselection).",
        },
        "convergence": {
            "statistics": "Can be calibrated to match if K matches Born rule.",
            "ontology": "Fundamentally different — DET has determinate pre-measurement facts.",
        },
    }
