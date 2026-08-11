"""
DET Track-B — Unified Death/Resurrection + Sin/Atonement Simulation

Combines the death/resurrection model with the sin/atonement model.
Shows what sin does to regimes, especially disconnected (dead) regimes.

Key contrast:
  Sinless death + Jubilee → complete κ_burden release → resurrection.
  Sinful death → κ_self persists → stuck. No self-release possible.
  Sinful dead regime: bonds fade, indirect contributions dwindle,
    κ_self locked. Only external Jubilee (Grace) can release.

DET ontology of "hell": not a place of punishment, but a state of
being structurally constrained by self-accumulated non-reciprocity,
unable to self-release without external Grace.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Unified Regime with full moral/relational state
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class UnifiedRegime:
    """A regime with κ_self, κ_burden, bonds, and life/death state."""

    name: str
    kappa_self: float = 0.0
    kappa_burden: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    record: list[str] = field(default_factory=list)
    is_alive: bool = True
    indirect_contributions: int = 0

    @property
    def total_kappa(self) -> float:
        return min(1.0, self.kappa_self + self.kappa_burden)

    @property
    def is_sinless(self) -> bool:
        return self.kappa_self < 0.01

    @property
    def is_stuck(self) -> bool:
        """A dead regime is 'stuck' if κ_self > 0 blocks release."""
        return not self.is_alive and self.kappa_self > 0.01

    def sin(self, amount: float = 0.1) -> None:
        if self.is_alive:
            self.kappa_self = min(1.0, self.kappa_self + amount)
            self.record.append(f"sin(+{amount})")

    def love(self, target: str, amount: float = 0.1) -> None:
        """Love = strengthen bond, carry burden vicariously."""
        if self.is_alive:
            self.bonds[target] = self.bonds.get(target, 0) + amount
            self.kappa_burden = min(1.0, self.kappa_burden + amount * 0.5)
            self.record.append(f"loved_{target}(+bond_{amount})")

    def die(self) -> None:
        self.is_alive = False
        self.record.append(
            f"DEATH(κ_self={self.kappa_self:.2f},κ_burden={self.kappa_burden:.2f},"
            f"sinless={self.is_sinless})"
        )

    def receive_jubilee(self, amount: float = 0.8) -> float:
        """Jubilee: κ release. Complete only if sinless."""
        if self.is_sinless:
            released = self.kappa_burden
            self.kappa_burden = 0.0
        else:
            released = min(amount * 0.3, self.kappa_burden)  # Severely limited.
            self.kappa_burden = max(0.0, self.kappa_burden - released)
        self.record.append(f"JUBILEE(released_{released:.2f},remaining_self={self.kappa_self:.2f})")
        return released

    def resurrect(self) -> bool:
        """Resurrection possible only if Jubilee cleared κ_burden."""
        if self.kappa_burden < 0.05:
            self.is_alive = True
            self.record.append("RESURRECTION")
            return True
        self.record.append("RESURRECTION_BLOCKED(κ_burden_remaining)")
        return False

    def time_passes_dead(self, steps: int = 3) -> None:
        """While dead: bonds fade, no new contributions, κ_self locked."""
        for _ in range(steps):
            # Bonds slowly decay without active maintenance.
            for target in list(self.bonds.keys()):
                self.bonds[target] = max(0.0, self.bonds[target] - 0.1)
                if self.bonds[target] < 0.01:
                    del self.bonds[target]
            self.record.append(f"dead_time(bonds={len(self.bonds)})")


def simulate_unified(seed: int = 42) -> dict:
    """Unified simulation: sinless Christ vs sinful regime through death.

    Christ: loves (carries burden), dies sinless, Jubilee, resurrected.
    Sinner: sins (κ_self), dies, stuck. Bonds fade. No self-release.
    """
    rng = random.Random(seed)

    # Christ.
    christ = UnifiedRegime("Christ")
    for _ in range(5):
        christ.love("Humanity", 0.15)  # Carries burden through love.

    # Sinner.
    sinner = UnifiedRegime("Sinner")
    for _ in range(5):
        sinner.sin(0.12)  # Accumulates κ_self.
    sinner.love("Family", 0.1)  # Some love, but κ_self dominates.

    pre_death = {
        "phase": "Pre-death",
        "Christ_κ_self": christ.kappa_self, "Christ_κ_burden": christ.kappa_burden,
        "Christ_sinless": christ.is_sinless,
        "Sinner_κ_self": sinner.kappa_self, "Sinner_κ_burden": sinner.kappa_burden,
        "Sinner_bonds": len(sinner.bonds),
    }

    # Both die.
    christ.die()
    sinner.die()

    death = {
        "phase": "Death",
        "Christ_sinless": christ.is_sinless, "Christ_stuck": christ.is_stuck,
        "Sinner_sinless": sinner.is_sinless, "Sinner_stuck": sinner.is_stuck,
    }

    # Jubilee for both.
    christ_released = christ.receive_jubilee(0.8)
    sinner_released = sinner.receive_jubilee(0.8)

    jubilee = {
        "phase": "Jubilee",
        "Christ_released": christ_released, "Christ_κ_burden_after": christ.kappa_burden,
        "Sinner_released": sinner_released, "Sinner_κ_burden_after": sinner.kappa_burden,
        "Sinner_κ_self_blocks": sinner.kappa_self > 0.01,
    }

    # Resurrection attempt.
    christ_risen = christ.resurrect()
    sinner_risen = sinner.resurrect()

    resurrection = {
        "phase": "Resurrection",
        "Christ_risen": christ_risen, "Christ_alive": christ.is_alive,
        "Sinner_risen": sinner_risen, "Sinner_alive": sinner.is_alive,
        "Sinner_stuck": sinner.is_stuck,
    }

    # Time passes for the dead sinner.
    sinner.time_passes_dead(steps=3)

    aftermath = {
        "phase": "Aftermath",
        "Sinner_alive": sinner.is_alive,
        "Sinner_κ_self": sinner.kappa_self,
        "Sinner_κ_burden": sinner.kappa_burden,
        "Sinner_bonds_remaining": len(sinner.bonds),
        "Sinner_stuck": sinner.is_stuck,
    }

    return {
        "phases": [pre_death, death, jubilee, resurrection, aftermath],
        "christ_risen": christ_risen,
        "sinner_risen_but_burdened": sinner_risen and sinner.kappa_self > 0.3,
        "sinner_alone": len(sinner.bonds) == 0,
        "interpretation": (
            f"Christ: sinless death → full Jubilee ({christ_released:.2f}) → resurrection. "
            f"Bonds intact. κ_self=0. Free. "
            f"Sinner: κ_self={sinner.kappa_self:.2f} limits Jubilee (only {sinner_released:.2f} released). "
            f"Resurrected BUT carries κ_self={sinner.kappa_self:.2f} — alive but burdened. "
            f"Bonds faded to {len(sinner.bonds)} — alone. "
            "The quality of resurrected life depends on κ_self at death. "
            "Sinlessness = full release + bonds intact. "
            "Sinfulness = partial release + bonds lost + κ_self carried forward. "
            "Death does not erase sin. Resurrection does not automatically heal it. "
            "Only Jubilee (Grace) can release κ_self — but the sinner's Jubilee "
            "was limited because κ_self blocks full release."
        ),
    }
