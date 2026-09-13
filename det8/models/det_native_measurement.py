"""
Classical Pointer-Record Copying — Historical DET-Native API

The model assumes a pre-existing binary target and a supplied noisy copying
kernel. Repeated copies can stabilize a majority pointer. It uses no Hilbert
space or Born rule because it models this classical readout task, not a full
quantum measurement. The historical function names are retained for callers.

No first-outcome selection, quantum decoherence rate, quantum Darwinism,
cross-context Born statistics or uniquely DET-derived law is established.
Current apparatus storage is mutable; it is not an immutable event history.
See record_process.py for the separate activity/commit/access contracts.
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

        Returns None when no bits are committed or their vote is tied.
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

    This classical model assumes that the target value already exists.
    Copying it is not a derivation that every quantum observable has a
    determinate pre-measurement value, nor a first-record formation mechanism.
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

    This is a noisy classical copy, not a derived quantum weak instrument.
    Each event writes a binary output; its mutual information about the
    target need not equal one bit.

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
    """Perform a full classical copying sequence (historical API name).

    Repeatedly applies det_native_measurement_event until all
    apparatus bits are committed. Returns the final pointer record
    and measurement statistics.

    A majority pointer is computed from N noisy copies of an assumed
    binary target. This does not construct a general projective measurement,
    resolve collapse, or prove that pointer strength grows monotonically.
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
    """Test the supplied classical copying model at low fidelity.

    At fidelity = 0.6, each individual bit is only 60% reliable.
    But with N=100 bits, the consensus should be correct with
    very high probability (law of large numbers).

    This demonstrates that pointer records can be reliable even
    when individual commit events are noisy — a key feature of
    this classical record-stabilization model.
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
    """State the limits of a classical copying/QM comparison.

    Matching a declared readout distribution does not match all instruments,
    incompatible settings, entangled composites or sequential experiments.
    The quantum formalism alone does not select an interpretation of collapse.
    """
    return {
        "det_native": {
            "target_ontology": "A pre-existing binary target is assumed in this classical model.",
            "measurement_process": "Sequence of commit events copying target → apparatus.",
            "pointer_origin": "Consensus of N noisy apparatus bits.",
            "collapse": "Outside this model; classical copying does not resolve quantum collapse.",
            "preferred_basis": "The copied binary property is supplied, not derived.",
        },
        "standard_qm": {
            "target_ontology": "Quantum state; an ontological interpretation is not fixed here.",
            "measurement_process": "Quantum instrument; projective measurement is a special case.",
            "pointer_origin": "Outcome probabilities and updates require a specified instrument.",
            "collapse": "Interpretation-dependent; not settled by this comparison.",
            "preferred_basis": "Requires a specified apparatus interaction and readout model.",
        },
        "convergence": {
            "statistics": (
                "A chosen classical readout distribution can be matched; no full QM "
                "reconstruction or cross-context equivalence follows."
            ),
            "ontology": "This model's binary-target assumption is not a universal DET ontology.",
        },
        "status": "CLASSICAL_RECORD_COPYING_ONLY",
    }
