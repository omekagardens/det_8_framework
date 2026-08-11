"""
DET Track-B — Record Extension Through Death (Resurrection Model)

Simulates a regime that dies, undergoes Jubilee (κ-reduction),
and resumes committing — with death remaining a committed fact
and identity tracked through PID-C provenance.

DET claim: Resurrection is not undoing death. It is extending the
record beyond death. d ≺ r. R_r ⊃ R_d. κ transforms without erasing.

Simulation phases:
  1. Life: Regime accumulates history through commit events.
  2. Death: κ→1, Ω→{0}. No more possibilities. Record stops.
  3. Jubilee: Grace/κ-reduction. Ω re-expands. New possibilities.
  4. Resurrection: New commit events. Record extends beyond death.
     Death remains in R. κ is reduced but not erased.
  5. Provenance check: PID-C confirms same identity before/after death.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Regime Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class Regime:
    """A selfhood-bearing regime with record, κ, and provenance."""

    name: str
    kappa: float = 0.0
    record: list[str] = field(default_factory=list)  # Committed events.
    provenance_id: str = ""  # Unique identifier for PID-C.
    is_alive: bool = True
    omega_options: int = 10  # Size of Ω.

    def commit(self, event: str) -> bool:
        """Commit an event. Only possible if alive (Ω non-empty)."""
        if not self.is_alive:
            return False
        self.record.append(event)
        self.kappa = min(1.0, self.kappa + 0.05)  # Slow accumulation.
        return True

    def die(self) -> None:
        """Death: κ→1, Ω→{0}. No more possibilities."""
        self.kappa = 1.0
        self.omega_options = 1  # Only the "null" option.
        self.record.append("DEATH_EVENT")
        self.is_alive = False

    def receive_jubilee(self, amount: float = 0.8) -> None:
        """Jubilee: κ-reduction. Ω re-expands."""
        self.kappa = max(0.0, self.kappa - amount)
        self.omega_options = max(2, int(10 * math.exp(-self.kappa * 0.5)))
        self.record.append("JUBILEE_EVENT")

    def resurrect(self) -> None:
        """Resurrection: life resumes. Record extends beyond death."""
        self.is_alive = True
        self.record.append("RESURRECTION_EVENT")

    @property
    def has_died(self) -> bool:
        return "DEATH_EVENT" in self.record

    @property
    def is_resurrected(self) -> bool:
        return "RESURRECTION_EVENT" in self.record


def simulate_resurrection(seed: int = 42) -> dict:
    """Simulate record extension through death.

    Phase 1 (Life): Regime commits events, accumulates history.
    Phase 2 (Death): κ→1, Ω→{0}. Record includes DEATH_EVENT.
    Phase 3 (Jubilee): κ-reduction, Ω re-expands. JUBILEE_EVENT.
    Phase 4 (Resurrection): Life resumes. RESURRECTION_EVENT.
      More events committed. Record extends beyond death.
    """
    rng = random.Random(seed)

    # Phase 1: Life.
    regime = Regime("TestRegime", provenance_id="PID_001")
    life_events = ["birth", "learning", "relationship", "achievement", "suffering"]
    for event in life_events:
        regime.commit(event)

    life_state = {
        "phase": "Life",
        "kappa": regime.kappa,
        "alive": regime.is_alive,
        "omega": regime.omega_options,
        "record_length": len(regime.record),
        "record_sample": regime.record.copy(),
    }

    # Phase 2: Death.
    regime.die()
    death_state = {
        "phase": "Death",
        "kappa": regime.kappa,
        "alive": regime.is_alive,
        "omega": regime.omega_options,
        "record_length": len(regime.record),
        "death_committed": regime.has_died,
    }

    # Phase 3: Jubilee (κ-reduction, not resurrection yet).
    regime.receive_jubilee(amount=0.8)
    jubilee_state = {
        "phase": "Jubilee",
        "kappa": regime.kappa,
        "alive": regime.is_alive,  # Still dead — only κ reduced.
        "omega": regime.omega_options,
        "record_length": len(regime.record),
    }

    # Phase 4: Resurrection. Life resumes.
    regime.resurrect()
    resurrection_events = ["restored_relationship", "new_creation", "eternal_participation"]
    for event in resurrection_events:
        regime.commit(event)

    resurrection_state = {
        "phase": "Resurrection",
        "kappa": regime.kappa,
        "alive": regime.is_alive,
        "omega": regime.omega_options,
        "record_length": len(regime.record),
        "record_sample": regime.record.copy(),
    }

    # Key checks.
    death_index = regime.record.index("DEATH_EVENT")
    resurrection_index = regime.record.index("RESURRECTION_EVENT")

    return {
        "phases": [life_state, death_state, jubilee_state, resurrection_state],
        "death_before_resurrection": death_index < resurrection_index,
        "death_remains_committed": "DEATH_EVENT" in regime.record,
        "record_grows_through_death": len(regime.record) > death_index + 1,
        "kappa_transformed_not_erased": regime.kappa < 1.0 and regime.kappa > 0.0,
        "provenance_preserved": regime.provenance_id == "PID_001",
        "interpretation": (
            f"Death committed at record index {death_index}. "
            f"Resurrection at record index {resurrection_index}. "
            f"d ≺ r: {death_index < resurrection_index}. "
            f"Death remains in R: {regime.has_died}. "
            f"Record grows through death: {len(regime.record)} events total. "
            f"κ transformed: {life_state['kappa']:.2f} → {regime.kappa:.2f} "
            f"(death κ={death_state['kappa']:.1f}, jubilee κ={jubilee_state['kappa']:.1f}). "
            "Resurrection is NOT undoing death. It is extending the record beyond it. "
            "d ≺ r. R_r ⊃ R_d. κ transformed without erasing."
        ),
    }
