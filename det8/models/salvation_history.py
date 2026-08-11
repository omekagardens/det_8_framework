"""
DET Track-B — Complete Salvation History: Eden → Fall → Law → Christ → Kingdom

Simulates the full arc of κ_self across cosmic history:
  Eden: κ_self=0, Ω open, bonds intact.
  Fall: κ_self emerges with moral self-awareness.
  Law: κ_self revealed but not removed. Partial Jubilee.
  Christ: Complete κ_burden carrier. Full Jubilee.
  Kingdom: Ongoing κ-reduction through Spirit.

Shows the collective κ_self of humanity across epochs.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CollectiveRegime:
    """A collective regime (humanity) with aggregate κ_self and κ_burden."""

    name: str
    kappa_self: float = 0.0
    kappa_burden: float = 0.0
    epoch: str = "Eden"
    omega_openness: float = 1.0  # Fraction of Ω available.
    bonds_intact: float = 1.0    # Fraction of bonds intact.

    @property
    def total_kappa(self) -> float:
        return min(1.0, self.kappa_self + self.kappa_burden)

    def accumulate_sin(self, amount: float = 0.05) -> None:
        self.kappa_self = min(1.0, self.kappa_self + amount)
        self.omega_openness = 1.0 / (1.0 + self.kappa_self)
        self.bonds_intact = max(0.0, 1.0 - self.kappa_self * 0.8)

    def receive_law(self) -> None:
        """The Law reveals κ_self but doesn't remove it."""
        self.epoch = "Law"
        # Law makes κ_self visible — no change to κ itself.
        # But provides partial Jubilee mechanism (sacrifice).

    def partial_jubilee(self, amount: float = 0.1) -> float:
        """Sacrificial system: partial temporary κ_burden release."""
        released = min(amount, self.kappa_burden) * 0.3  # Limited effectiveness.
        self.kappa_burden = max(0.0, self.kappa_burden - released)
        return released

    def receive_christ(self) -> None:
        """Christ arrives: complete κ_burden carrier available."""
        self.epoch = "Christ"

    def full_jubilee(self) -> float:
        """Christ's Jubilee: complete κ_burden release."""
        released = self.kappa_burden
        self.kappa_burden = 0.0
        return released

    def spirit_work(self, amount: float = 0.05) -> float:
        """Ongoing κ_self reduction through Spirit in the Kingdom."""
        released = min(amount, self.kappa_self)
        self.kappa_self = max(0.0, self.kappa_self - released)
        self.omega_openness = 1.0 / (1.0 + self.kappa_self)
        self.bonds_intact = max(0.0, 1.0 - self.kappa_self * 0.8)
        return released

    def state_summary(self) -> dict:
        return {
            "epoch": self.epoch,
            "κ_self": self.kappa_self,
            "κ_burden": self.kappa_burden,
            "Ω": self.omega_openness,
            "bonds": self.bonds_intact,
        }


def simulate_salvation_history(seed: int = 42) -> dict:
    """Simulate the complete arc from Eden to Kingdom."""
    rng = random.Random(seed)
    humanity = CollectiveRegime("Humanity")
    history = []

    # 1. EDEN: κ_self=0.
    history.append({"phase": "Eden", **humanity.state_summary()})

    # 2. FALL: κ_self emerges through repeated non-reciprocity.
    humanity.epoch = "Fall"
    for _ in range(8):
        humanity.accumulate_sin(0.08)
    history.append({"phase": "Fall (post)", **humanity.state_summary()})

    # Load collective burden from fallen state.
    humanity.kappa_burden = humanity.kappa_self * 0.5

    # 3. LAW: Reveals κ_self. Provides partial Jubilee.
    humanity.receive_law()
    for _ in range(4):
        humanity.partial_jubilee(0.1)
    # But κ_self continues to accumulate.
    for _ in range(2):
        humanity.accumulate_sin(0.03)
    history.append({"phase": "Law (post)", **humanity.state_summary()})

    # 4. CHRIST: Complete κ_burden release.
    humanity.receive_christ()
    released = humanity.full_jubilee()
    history.append({
        "phase": "Christ (Jubilee)",
        "released": released,
        **humanity.state_summary(),
    })

    # 5. KINGDOM: Ongoing κ_self reduction through Spirit.
    humanity.epoch = "Kingdom"
    for _ in range(10):
        humanity.spirit_work(0.04)
    history.append({"phase": "Kingdom (post)", **humanity.state_summary()})

    return {
        "history": history,
        "final_κ_self": humanity.kappa_self,
        "eden_restored": humanity.kappa_self < 0.1 and humanity.omega_openness > 0.9,
        "interpretation": (
            f"Eden: κ_self={history[0]['κ_self']:.2f}, Ω={history[0]['Ω']:.2f}. "
            f"Fall: κ_self→{history[1]['κ_self']:.2f}, Ω→{history[1]['Ω']:.2f}. "
            f"Law: partial Jubilee, κ_self→{history[2]['κ_self']:.2f}. "
            f"Christ: κ_burden released ({released:.2f}). "
            f"Kingdom: Spirit reduces κ_self→{humanity.kappa_self:.2f}, Ω→{humanity.omega_openness:.2f}. "
            f"Eden restored: {humanity.kappa_self < 0.1 and humanity.omega_openness > 0.9}. "
            "The arc is complete: from κ_self=0, through accumulation, "
            "to ongoing release. The Kingdom is NOW — κ_self decreasing, "
            "Ω expanding, bonds healing. Not yet complete, but underway."
        ),
    }
