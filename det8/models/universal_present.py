"""
DET Track-B — Universal Selfhood: Spectrum of Consciousness Simulation

Models different selfhood-bearing regimes (human, animal, hypothetical
extraterrestrial) participating in the SAME present moment, distinguished
only by their records, κ, bonds, and Ω — not by separate "presents."
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SelfhoodRegime:
    """A selfhood-bearing regime at any level of the spectrum."""

    name: str
    species: str
    level: int            # 0-4 on the selfhood spectrum.
    kappa_self: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    record: list[str] = field(default_factory=list)
    present_moment: int = 0  # ALL regimes share the same present counter.

    @property
    def can_accumulate_kappa_self(self) -> bool:
        return self.level >= 3  # Self-aware.

    @property
    def omega_description(self) -> str:
        if self.level == 0:
            return "none (no choices)"
        elif self.level == 1:
            return "stimulus-response only"
        elif self.level == 2:
            return "present-moment awareness"
        elif self.level == 3:
            return "future/past, moral choice"
        else:
            return "full relational, Grace-capable"

    def participate(self, event: str) -> None:
        """Participate in the present moment. All regimes do this together."""
        self.present_moment += 1
        self.record.append(event)

    def accumulate_kappa(self, amount: float = 0.1) -> None:
        if self.can_accumulate_kappa_self:
            self.kappa_self = min(1.0, self.kappa_self + amount)


def simulate_universal_present(seed: int = 42) -> dict:
    """Simulate multiple selfhood regimes sharing the same present."""
    rng = random.Random(seed)

    regimes = [
        SelfhoodRegime("Human", "Homo sapiens", level=3),
        SelfhoodRegime("Chimpanzee", "Pan troglodytes", level=3, kappa_self=0.1),
        SelfhoodRegime("Dolphin", "Tursiops truncatus", level=3, kappa_self=0.05),
        SelfhoodRegime("Dog", "Canis familiaris", level=2),  # Sentient but not self-aware.
        SelfhoodRegime("Oak", "Quercus robur", level=1),     # Reactive.
        SelfhoodRegime("ET_Alpha", "Unknown", level=4, kappa_self=0.01),  # Hypothetical.
    ]

    # Bond formation: extensive relational webs across all levels.
    regimes[0].bonds["Chimpanzee"] = 0.5
    regimes[0].bonds["Dog"] = 0.8
    regimes[1].bonds["Human"] = 0.5
    regimes[3].bonds["Human"] = 0.8
    regimes[4].bonds["Soil_Mycorrhizae"] = 0.9   # Oak: vast underground fungal network.
    regimes[4].bonds["Forest_Community"] = 0.7    # Oak: connected to entire forest.
    regimes[4].bonds["Squirrels_Birds_Insects"] = 0.6  # Oak: hosts countless species.
    regimes[5].bonds["Human"] = 0.0  # ET: no contact yet.

    # All participate in the SAME present moments.
    shared_events = [
        "sunrise", "rain", "earthquake", "season_change", "cosmic_event"
    ]
    for event in shared_events:
        for r in regimes:
            r.participate(event)

    # Some accumulate κ_self (only L3+).
    for _ in range(3):
        regimes[0].accumulate_kappa(0.1)  # Human sins.
        regimes[1].accumulate_kappa(0.05) # Chimp sins (deception).

    # All participate in more shared events.
    for event in ["predator_appears", "food_discovery", "death_nearby"]:
        for r in regimes:
            r.participate(event)

    summary = []
    for r in regimes:
        summary.append({
            "name": r.name,
            "species": r.species,
            "level": r.level,
            "Ω": r.omega_description,
            "κ_self": r.kappa_self,
            "bonds": len(r.bonds),
            "present_moments": r.present_moment,  # Should be identical.
            "can_sin": r.can_accumulate_kappa_self,
            "record_sample": r.record[:3],
        })

    all_same_present = len(set(r.present_moment for r in regimes)) == 1

    return {
        "regimes": summary,
        "all_same_present": all_same_present,
        "total_present_moments": regimes[0].present_moment,
        "interpretation": (
            f"All {len(regimes)} regimes share {regimes[0].present_moment} present moments. "
            f"Same present: {all_same_present}. "
            "What differs: κ_self, bonds, Ω complexity, level of selfhood. "
            "The present is ONE. Only the records differ. "
            "We are not alone — we share the present with every selfhood-bearing "
            "regime on Earth and across the universe. The relational web connects all."
        ),
    }
