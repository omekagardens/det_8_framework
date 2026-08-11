"""
DET Track-B — Death as Relational Transition: Indirect Contribution Model

Simulates how the dead continue to contribute INDIRECTLY to the record
through bonds (σ_ij, C_ij) with the living, through κ left behind,
and through influence on the living's commit events.

Key metrics:
  - Direct commits: events the regime committed while alive.
  - Indirect commits: events committed by the living that reference
    or are shaped by the dead regime's influence.
  - Bond strength: σ_ij between dead and living persists.
  - κ persistence: the dead regime's κ remains in the world.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Relational Regime Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class RelationalRegime:
    """A regime with bonds to others. Can be alive, dead, or resurrected."""

    name: str
    kappa: float = 0.0
    record: list[str] = field(default_factory=list)
    bonds: dict[str, float] = field(default_factory=dict)  # other_name → bond_strength.
    is_alive: bool = True
    mode: str = "direct"  # "direct" or "indirect".

    def commit(self, event: str) -> bool:
        if not self.is_alive:
            return False
        self.record.append(f"{self.name}:{event}")
        self.kappa = min(1.0, self.kappa + 0.03)
        return True

    def commit_influenced_by(self, event: str, influencer: str) -> bool:
        """Commit an event that carries the influence of another regime."""
        if not self.is_alive:
            return False
        self.record.append(f"{self.name}:{event}(influenced_by_{influencer})")
        self.kappa = min(1.0, self.kappa + 0.03)
        return True

    def bond_with(self, other_name: str, strength: float = 1.0) -> None:
        self.bonds[other_name] = strength

    def die(self) -> None:
        self.kappa = 1.0
        self.record.append(f"{self.name}:DEATH")
        self.is_alive = False
        self.mode = "indirect"

    def receive_jubilee(self, amount: float = 0.7) -> None:
        self.kappa = max(0.0, self.kappa - amount)
        self.record.append(f"{self.name}:JUBILEE")

    def resurrect(self) -> None:
        self.is_alive = True
        self.mode = "direct"
        self.record.append(f"{self.name}:RESURRECTION")


def simulate_indirect_contribution(seed: int = 42) -> dict:
    """Simulate indirect contribution through bonds after death.

    Setup:
      Regime A: lives, dies, is resurrected.
      Regime B: lives throughout, bonded to A.

    Key question: does A continue to contribute INDIRECTLY to the
    record through B's actions after A's death?
    """
    rng = random.Random(seed)

    # Create regimes with mutual bonds.
    a = RelationalRegime("A")
    b = RelationalRegime("B")
    a.bond_with("B", 1.0)
    b.bond_with("A", 1.0)

    # Phase 1: Both alive. Both commit directly.
    a.commit("discovery")
    b.commit("learning")
    a.commit("teaching")
    b.commit_influenced_by("applying_teaching", "A")  # B's act shaped by A.

    phase1 = {
        "phase": "Both alive (direct)",
        "A_mode": a.mode, "B_mode": b.mode,
        "A_record": a.record.copy(),
        "B_record": b.record.copy(),
        "A_direct": sum(1 for e in a.record if "influenced" not in e),
        "B_influenced_by_A": sum(1 for e in b.record if "influenced_by_A" in e),
    }

    # Phase 2: A dies. B continues to live.
    a.die()
    b.commit("mourning")
    b.commit_influenced_by("carrying_legacy", "A")  # B's act shaped by A.
    b.commit_influenced_by("teaching_others", "A")  # Another act shaped by A.

    phase2 = {
        "phase": "A dead (indirect), B alive",
        "A_mode": a.mode, "B_mode": b.mode,
        "A_kappa": a.kappa, "B_kappa": b.kappa,
        "A_bond_to_B": a.bonds.get("B", 0),
        "B_bond_to_A": b.bonds.get("A", 0),
        "A_record": a.record.copy(),
        "B_record": b.record.copy(),
        "B_influenced_by_A": sum(1 for e in b.record if "influenced_by_A" in e),
        "A_contributes_indirectly": True,  # Through B's influenced acts.
    }

    # Phase 3: Jubilee. A's κ reduced but still dead.
    a.receive_jubilee(0.7)
    b.commit("hoping")
    b.commit_influenced_by("preparing_for_return", "A")

    phase3 = {
        "phase": "Jubilee (A still indirect)",
        "A_mode": a.mode, "B_mode": b.mode,
        "A_kappa": a.kappa, "B_kappa": b.kappa,
        "B_record": b.record.copy(),
        "B_influenced_by_A": sum(1 for e in b.record if "influenced_by_A" in e),
    }

    # Phase 4: A resurrected. Both alive again.
    a.resurrect()
    a.commit("gratitude")
    b.commit_influenced_by("reunion", "A")
    a.commit("new_teaching")

    phase4 = {
        "phase": "Resurrection (both direct)",
        "A_mode": a.mode, "B_mode": b.mode,
        "A_kappa": a.kappa, "B_kappa": b.kappa,
        "A_record": a.record.copy(),
        "B_record": b.record.copy(),
        "A_direct_after": sum(1 for e in a.record if "influenced" not in e and a.record.index(e) > a.record.index("A:RESURRECTION")),
        "B_influenced_by_A_total": sum(1 for e in b.record if "influenced_by_A" in e),
    }

    return {
        "phases": [phase1, phase2, phase3, phase4],
        "total_A_contributions": (
            sum(1 for e in a.record if "influenced" not in e) +
            sum(1 for e in b.record if "influenced_by_A" in e)
        ),
        "A_direct": sum(1 for e in a.record if "influenced" not in e),
        "A_indirect_through_B": sum(1 for e in b.record if "influenced_by_A" in e),
        "interpretation": (
            f"A's direct contributions: {sum(1 for e in a.record if 'influenced' not in e)}. "
            f"A's indirect contributions (through B): {sum(1 for e in b.record if 'influenced_by_A' in e)}. "
            "A contributes to the record even while DEAD — through B's acts shaped by A. "
            "Death does not end contribution. It transitions from direct to indirect. "
            "Bonds persist. Influence persists. The dead remain present in the relational web."
        ),
    }
