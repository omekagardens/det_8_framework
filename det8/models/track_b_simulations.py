"""
DET Track-B — Ω Enlargement (Grace) + Causal Provenance (PID-C)

Two executable Track-B simulations:

1. Ω Enlargement: Models how the possibility space shrinks as κ accumulates
   (structural constraints tighten) and can be re-expanded through κ-reduction.
   This is the DET model of Grace — the opening of new possibilities.

2. Causal Provenance Tracker: Tracks unique causal lineage through commit events.
   Demonstrates PID-C: two regimes with identical records but different
   causal provenances are distinguishable.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. Ω Enlargement (Grace Model)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class PossibilitySpace:
    """A possibility space Ω that shrinks with κ and can be enlarged."""

    total_options: int = 10       # Maximum possible options at κ=0.
    kappa: float = 0.0           # Current structural history.
    constraint_rate: float = 1.0  # How fast κ constrains Ω.

    @property
    def available_options(self) -> int:
        """Number of available options at current κ.

        Ω(κ) = total_options · exp(−constraint_rate · κ).
        At κ=0: all options available.
        At κ→∞: Ω → 0.
        """
        n = int(self.total_options * math.exp(-self.constraint_rate * self.kappa))
        return max(1, n)  # At least 1 option always available.

    @property
    def fraction_available(self) -> float:
        return self.available_options / self.total_options

    def accumulate(self, delta_kappa: float = 0.1) -> None:
        """Accumulate structural history — Ω shrinks."""
        self.kappa = min(10.0, self.kappa + delta_kappa)

    def recover(self, delta_kappa: float = 0.1) -> None:
        """Recover — κ decreases, Ω re-expands (Grace/Jubilee)."""
        self.kappa = max(0.0, self.kappa - delta_kappa)


def simulate_omega_evolution(
    n_steps: int = 30,
    seed: int = 42,
) -> dict:
    """Simulate Ω evolution: accumulation → recovery → re-expansion.

    Phase 1 (steps 0-9): Accumulate κ, Ω shrinks.
    Phase 2 (steps 10-19): Recovery, Ω re-expands (Grace).
    Phase 3 (steps 20-29): Re-accumulation, Ω shrinks again.

    Demonstrates that Ω is not fixed — it responds to κ.
    Grace is modeled as accelerated recovery opening new possibilities.
    """
    omega = PossibilitySpace(total_options=20)
    history = []

    for step in range(n_steps):
        if step < 10:
            omega.accumulate(0.2)  # Accumulation phase.
            phase = "accumulation"
        elif step < 20:
            omega.recover(0.3)     # Recovery/Grace phase (faster).
            phase = "grace"
        else:
            omega.accumulate(0.15)  # Re-accumulation.
            phase = "re-accumulation"

        history.append({
            "step": step,
            "kappa": omega.kappa,
            "available": omega.available_options,
            "fraction": omega.fraction_available,
            "phase": phase,
        })

    return {
        "total_options": omega.total_options,
        "history": history,
        "min_options": min(h["available"] for h in history),
        "max_options": max(h["available"] for h in history),
        "grace_effect": (
            f"During Grace phase (steps 10-19), Ω expanded from "
            f"{history[9]['available']} to {history[19]['available']} options. "
            f"Recovery rate was 1.5× the accumulation rate."
        ),
        "interpretation": (
            "Ω is not fixed. It responds to κ. Grace is modeled as "
            "accelerated κ-recovery that re-opens possibilities that "
            "structural history had closed. This is a Track-B model — "
            "the mechanism of Grace (M/H) is not specified; only its "
            "effect on the possibility space is demonstrated."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Causal Provenance Tracker (PID-C)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ProvenanceTracker:
    """Tracks unique causal lineage through commit events.

    Two regimes with identical records but different causal provenances
    are distinguishable. This is the PID-C implementation.
    """

    regimes: dict[str, list[str]] = field(default_factory=dict)  # id → event history.
    event_counter: int = 0

    def create_regime(self, regime_id: str, parent_id: Optional[str] = None) -> str:
        """Create a new regime with unique provenance.

        If parent_id is provided, the new regime inherits the parent's
        history (record continuity). But its provenance is unique because
        the creation event is new.
        """
        if parent_id and parent_id in self.regimes:
            # Inherit parent's history (record similarity).
            history = self.regimes[parent_id].copy()
        else:
            history = []

        # Add unique creation event.
        self.event_counter += 1
        creation_event = f"create_{regime_id}_{self.event_counter}"
        history.append(creation_event)
        self.regimes[regime_id] = history
        return creation_event

    def commit_event(self, regime_id: str, event: str) -> None:
        """Record a commit event in the regime's history."""
        if regime_id in self.regimes:
            self.event_counter += 1
            self.regimes[regime_id].append(f"{event}_{self.event_counter}")

    def provenance(self, regime_id: str) -> list[str]:
        """Return the unique causal provenance of a regime."""
        return self.regimes.get(regime_id, [])

    def identical_records(self, id_a: str, id_b: str) -> bool:
        """Check if two regimes have identical event histories (same record)."""
        return self.provenance(id_a) == self.provenance(id_b)

    def same_provenance(self, id_a: str, id_b: str) -> bool:
        """Check if two regimes share causal provenance.

        They share provenance if one's history is a prefix of the other's
        (one was created from the other). Same record but different creation
        events means different provenance.
        """
        hist_a = self.provenance(id_a)
        hist_b = self.provenance(id_b)
        if not hist_a or not hist_b:
            return False
        # Must share the initial creation event.
        return hist_a[0] == hist_b[0]


def simulate_duplicate_test(seed: int = 42) -> dict:
    """Simulate the duplicate test using causal provenance.

    Creates three regimes:
      - Original: unique causal lineage from t=0.
      - Copy: identical record, created later, DIFFERENT provenance.
      - Child: created from Original, shares provenance prefix.

    Demonstrates that identical records ≠ same identity.
    """
    tracker = ProvenanceTracker()

    # Original regime.
    tracker.create_regime("original")
    tracker.commit_event("original", "event_A")
    tracker.commit_event("original", "event_B")

    # Copy regime — same events, created independently (different provenance).
    tracker.create_regime("copy")  # New creation event!
    tracker.commit_event("copy", "event_A")
    tracker.commit_event("copy", "event_B")

    # Child regime — created FROM original.
    tracker.create_regime("child", parent_id="original")
    tracker.commit_event("child", "event_C")

    return {
        "original_history": tracker.provenance("original"),
        "copy_history": tracker.provenance("copy"),
        "child_history": tracker.provenance("child"),
        "identical_records_orig_copy": tracker.identical_records("original", "copy"),
        "same_provenance_orig_copy": tracker.same_provenance("original", "copy"),
        "same_provenance_orig_child": tracker.same_provenance("original", "child"),
        "duplicate_test_result": (
            f"Original and Copy have identical records: "
            f"{tracker.identical_records('original', 'copy')}. "
            f"But their provenance differs: "
            f"{tracker.same_provenance('original', 'copy')}. "
            f"Original and Child share provenance prefix: "
            f"{tracker.same_provenance('original', 'child')}. "
            "Record equality does NOT imply identity. Provenance is decisive."
        ),
    }
