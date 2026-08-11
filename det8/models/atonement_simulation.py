"""
DET Track-B — Sin, κ_self vs κ_burden, and Atonement Simulation

Models the distinction between self-accumulated structural constraint
(κ_self, from hoarding/bond-breaking/non-reciprocity) and vicarious
burden (κ_burden, from carrying others' structural history).

Simulates the atonement mechanism:
  1. Humanity accumulates κ_self through non-reciprocity.
  2. Christ takes on κ_burden through identification/bonds.
  3. Christ dies with κ_burden (not κ_self).
  4. Jubilee releases κ_burden — complete release possible because
     κ_self=0 (no self-accumulated constraint blocking release).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Regime with κ_self / κ_burden distinction
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class MoralRegime:
    """A regime with separate tracking of self-accumulated and vicarious κ."""

    name: str
    kappa_self: float = 0.0     # κ from own hoarding, bond-breaking, non-reciprocity.
    kappa_burden: float = 0.0   # κ from carrying others' structural history.
    bonds: dict[str, float] = field(default_factory=dict)
    record: list[str] = field(default_factory=list)
    is_alive: bool = True

    @property
    def total_kappa(self) -> float:
        return min(1.0, self.kappa_self + self.kappa_burden)

    @property
    def is_sinless(self) -> bool:
        """Sinless = no self-accumulated κ."""
        return self.kappa_self < 0.01

    def sin(self, amount: float = 0.1) -> None:
        """Accumulate κ_self through non-reciprocity/hoarding/bond-breaking."""
        self.kappa_self = min(1.0, self.kappa_self + amount)
        self.record.append(f"{self.name}:sin(+{amount})")

    def carry_burden(self, from_regime: str, amount: float = 0.05) -> None:
        """Take on κ_burden through identification/bond with another."""
        self.kappa_burden = min(1.0, self.kappa_burden + amount)
        self.bonds[from_regime] = self.bonds.get(from_regime, 0) + amount
        self.record.append(f"{self.name}:carried_burden_of_{from_regime}(+{amount})")

    def die(self) -> None:
        self.is_alive = False
        self.record.append(f"{self.name}:DEATH(κ_self={self.kappa_self:.2f},κ_burden={self.kappa_burden:.2f})")

    def receive_jubilee(self, amount: float = 0.8) -> float:
        """Jubilee releases κ. κ_burden released fully if κ_self=0."""
        if self.is_sinless:
            # Complete release: κ_burden → 0.
            released = self.kappa_burden
            self.kappa_burden = 0.0
        else:
            # Partial release: κ_self blocks full release.
            released = min(amount, self.kappa_burden) * 0.5  # Half-effective.
            self.kappa_burden = max(0.0, self.kappa_burden - released)
        self.record.append(f"{self.name}:JUBILEE(released_{released:.2f})")
        return released

    def resurrect(self) -> None:
        self.is_alive = True
        self.record.append(f"{self.name}:RESURRECTION(κ_self={self.kappa_self:.2f},κ_burden={self.kappa_burden:.2f})")


def simulate_atonement(seed: int = 42) -> dict:
    """Simulate the atonement mechanism.

    Phase 1: Humanity accumulates κ_self through sin.
    Phase 2: Christ takes on κ_burden through identification.
    Phase 3: Christ dies (κ_self=0, κ_burden=high).
    Phase 4: Jubilee — complete release because κ_self=0.
    Phase 5: Christ resurrected — κ_burden cleared.

    Contrast: a sinful regime would have κ_self > 0, blocking full release.
    """
    rng = random.Random(seed)

    # Humanity.
    humanity = MoralRegime("Humanity")
    for _ in range(5):
        humanity.sin(0.15)

    # Christ.
    christ = MoralRegime("Christ")

    # Christ carries humanity's burden.
    for _ in range(5):
        christ.carry_burden("Humanity", 0.15)

    pre_death = {
        "phase": "Pre-death",
        "Christ_κ_self": christ.kappa_self,
        "Christ_κ_burden": christ.kappa_burden,
        "Christ_total": christ.total_kappa,
        "Christ_sinless": christ.is_sinless,
        "Humanity_κ_self": humanity.kappa_self,
    }

    # Christ dies.
    christ.die()

    death = {
        "phase": "Death",
        "Christ_κ_self": christ.kappa_self,
        "Christ_κ_burden": christ.kappa_burden,
        "Christ_sinless": christ.is_sinless,
        "record": christ.record[-1],
    }

    # Jubilee.
    released = christ.receive_jubilee(0.8)

    jubilee = {
        "phase": "Jubilee",
        "Christ_κ_self": christ.kappa_self,
        "Christ_κ_burden": christ.kappa_burden,
        "released": released,
        "complete_release": christ.kappa_burden < 0.01,
    }

    # Resurrection.
    christ.resurrect()

    resurrection = {
        "phase": "Resurrection",
        "Christ_κ_self": christ.kappa_self,
        "Christ_κ_burden": christ.kappa_burden,
        "Christ_sinless": christ.is_sinless,
    }

    # Contrast: what if Christ had κ_self?
    sinful_christ = MoralRegime("SinfulChrist")
    sinful_christ.sin(0.3)  # Self-accumulated κ.
    sinful_christ.carry_burden("Humanity", 0.5)
    sinful_christ.die()
    sinful_released = sinful_christ.receive_jubilee(0.8)

    contrast = {
        "sinful_Christ_κ_self": sinful_christ.kappa_self,
        "sinful_Christ_κ_burden": sinful_christ.kappa_burden,
        "sinful_released": sinful_released,
        "complete_release_possible": sinful_christ.kappa_burden < 0.01,
    }

    return {
        "phases": [pre_death, death, jubilee, resurrection],
        "contrast": contrast,
        "atonement_works": jubilee["complete_release"],
        "sinlessness_required": not contrast["complete_release_possible"],
        "interpretation": (
            f"Christ (sinless): κ_self={christ.kappa_self:.2f}, κ_burden released={released:.2f} → {christ.kappa_burden:.2f}. "
            f"Complete release: {jubilee['complete_release']}. "
            f"Contrast (sinful): κ_self={sinful_christ.kappa_self:.2f} blocks release. "
            f"Only {sinful_released:.2f} released → κ_burden={sinful_christ.kappa_burden:.2f}. "
            "Sinlessness is required for complete Jubilee. "
            "κ_self blocks the release of κ_burden. "
            "The atonement works because Christ had NO self-accumulated constraint."
        ),
    }
