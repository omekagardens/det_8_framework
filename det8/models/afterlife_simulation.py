"""
DET Track-B — Heaven/Hell/Purgatory Simulation

Simulates three post-death trajectories based on κ_self at death:
  Saint (κ_self≈0): Heaven — free, connected, participatory.
  Sinner (κ_self≈0.5): Purgatory → eventual healing.
  Hardened (κ_self≈1.0): Hellish isolation → slow healing possible.

Key finding: All three are resurrected. The quality of resurrected life
depends on κ_self. Healing continues after resurrection. Hell is not absolute.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Soul:
    """A regime with afterlife trajectory determined by κ_self at death."""

    name: str
    kappa_self: float = 0.0
    kappa_burden: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    is_alive: bool = True
    healing_steps: int = 0
    trajectory: str = "unknown"

    @property
    def total_kappa(self) -> float:
        return min(1.0, self.kappa_self + self.kappa_burden)

    def die(self) -> None:
        self.is_alive = False

    def receive_grace(self, amount: float = 0.1) -> float:
        """Grace reduces κ_self. Effectiveness depends on current κ_self."""
        # Grace is more effective when κ_self is lower (receptivity).
        effectiveness = 1.0 - self.kappa_self * 0.8  # High κ_self resists.
        released = amount * effectiveness
        self.kappa_self = max(0.0, self.kappa_self - released)
        self.healing_steps += 1
        return released

    def resurrect(self) -> bool:
        """Resurrection when κ_self is sufficiently healed."""
        if self.kappa_self < 0.95:  # Even heavily burdened can resurrect.
            self.is_alive = True
            return True
        return False

    def assess_state(self) -> str:
        if not self.is_alive and self.kappa_self < 0.1:
            return "purgatory (nearly healed)"
        elif not self.is_alive and self.kappa_self > 0.7:
            return "hellish (heavily constrained)"
        elif not self.is_alive:
            return "purgatory (healing)"
        elif self.kappa_self < 0.1:
            return "heaven (free)"
        elif self.kappa_self < 0.5:
            return "resurrected (healing continues)"
        else:
            return "resurrected (burdened)"


def simulate_afterlife(seed: int = 42) -> dict:
    """Simulate three trajectories through death, purgatory, and resurrection.

    Saint: κ_self=0.05 → rapid healing → heaven.
    Sinner: κ_self=0.50 → purgatory → gradual healing → resurrected.
    Hardened: κ_self=0.95 → hellish → slow healing → eventual resurrection.
    """
    rng = random.Random(seed)

    souls = [
        Soul("Saint", kappa_self=0.05),
        Soul("Sinner", kappa_self=0.50),
        Soul("Hardened", kappa_self=0.95),
    ]

    # All die.
    for s in souls:
        s.die()

    trajectories = {s.name: [] for s in souls}

    # Purgatory: Grace applied over time.
    for step in range(20):
        for s in souls:
            if not s.is_alive:
                s.receive_grace(0.1)
            state = s.assess_state()
            if step % 5 == 0:
                trajectories[s.name].append({
                    "step": step,
                    "κ_self": s.kappa_self,
                    "alive": s.is_alive,
                    "state": state,
                })

        # Check for resurrection.
        for s in souls:
            if not s.is_alive and s.kappa_self < 0.5:
                s.resurrect()

    # Continue healing after resurrection.
    for step in range(10):
        for s in souls:
            if s.is_alive and s.kappa_self > 0.01:
                s.receive_grace(0.05)
            state = s.assess_state()
            if step % 3 == 0:
                trajectories[s.name].append({
                    "step": 20 + step,
                    "κ_self": s.kappa_self,
                    "alive": s.is_alive,
                    "state": state,
                })

    # Final state.
    final = {}
    for s in souls:
        final[s.name] = {
            "final_κ_self": s.kappa_self,
            "alive": s.is_alive,
            "healing_steps": s.healing_steps,
            "final_state": s.assess_state(),
        }

    return {
        "trajectories": trajectories,
        "final": final,
        "all_resurrected": all(s.is_alive for s in souls),
        "hell_not_absolute": final["Hardened"]["alive"],
        "interpretation": (
            f"Saint: κ_self {souls[0].kappa_self:.2f} → heaven (free). "
            f"Sinner: κ_self {souls[1].kappa_self:.2f} → purgatory → resurrected (healing). "
            f"Hardened: κ_self {souls[2].kappa_self:.2f} → hellish → slow healing → eventual resurrection. "
            f"All resurrected: {all(s.is_alive for s in souls)}. "
            "Hell is not absolute. Healing continues after resurrection. "
            "The quality of resurrected life depends on κ_self at death, "
            "but Grace reduces κ_self for ALL — no one is beyond reach. "
            "The fire of hell is real, but it is purifying, not eternal."
        ),
    }
