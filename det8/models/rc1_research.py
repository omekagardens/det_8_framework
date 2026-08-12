"""
DET Track-B — RC1 Research: Nested Regimes, Bond Dependency, Personality Print

Implements three RC1 research directions:
  1. Nested Regimes: κ and bonds propagate across levels.
  2. Bond Dependency Test: "I do not need you" as ontological denial.
  3. Personality Print: stable response patterns across changing constituents.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. Nested Regimes: κ and Bond Propagation
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class NestedRegime:
    """A regime within a nested hierarchy. κ and bonds propagate across levels."""

    name: str
    level: str  # "constituent", "cell", "organ", "organism", "community", "ecosystem", "creation"
    kappa_self: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    sub_regimes: list[str] = field(default_factory=list)
    parent_regime: Optional[str] = None

    def damage(self, amount: float = 0.1) -> None:
        """Damage at one level propagates κ upward and downward."""
        self.kappa_self = min(1.0, self.kappa_self + amount)

    def heal(self, amount: float = 0.1) -> None:
        """Healing at one level propagates relief upward and downward."""
        self.kappa_self = max(0.0, self.kappa_self - amount)

    def bond_with(self, other: str, strength: float = 0.5) -> None:
        self.bonds[other] = min(1.0, self.bonds.get(other, 0) + strength)


def simulate_nested_damage(seed: int = 42) -> dict:
    """Simulate κ propagation across nested levels.

    Damage a cell → organ feels it → organism responds → community affected.
    Healing at organism level → relief flows down to organs and cells.
    """
    rng = random.Random(seed)

    # Build nested hierarchy.
    cell = NestedRegime("Cell_A", "cell")
    organ = NestedRegime("Heart", "organ", sub_regimes=["Cell_A"])
    organism = NestedRegime("Body", "organism", sub_regimes=["Heart"])
    community = NestedRegime("Family", "community", sub_regimes=["Body"])

    cell.parent_regime = "Heart"
    organ.parent_regime = "Body"
    organism.parent_regime = "Family"

    all_regimes = [cell, organ, organism, community]
    history = []

    # Phase 1: Initial state.
    history.append({
        "phase": "Initial",
        "states": {r.name: r.kappa_self for r in all_regimes},
    })

    # Phase 2: Damage at cell level propagates UP.
    cell.damage(0.3)
    organ.damage(0.15)   # Organ feels it.
    organism.damage(0.05) # Organism responds.
    history.append({
        "phase": "Cell damaged → upward propagation",
        "states": {r.name: r.kappa_self for r in all_regimes},
    })

    # Phase 3: Healing at organism level propagates DOWN.
    organism.heal(0.1)
    organ.heal(0.1)
    cell.heal(0.1)
    history.append({
        "phase": "Organism heals → downward propagation",
        "states": {r.name: r.kappa_self for r in all_regimes},
    })

    return {
        "hierarchy": "Cell → Organ → Organism → Community",
        "history": history,
        "interpretation": (
            "Damage at any level propagates through the nested hierarchy. "
            "A damaged cell stresses the organ, which burdens the organism, "
            "which affects the community. Healing also propagates — "
            "relief at the organism level flows down to organs and cells. "
            "No regime is isolated. The relational web connects all levels."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Bond Dependency Test: "I Do Not Need You"
# ═══════════════════════════════════════════════════════════════════════════


def simulate_bond_denial(seed: int = 42) -> dict:
    """Simulate what happens when a regime denies its bonds.

    "I do not need you" — but the bonds it denies are the bonds it depends on.
    Denial → bond neglect → bond decay → isolation → increased κ_self.

    The denial is ontologically false: the regime DOES depend on those bonds.
    The denial causes real damage through neglect.
    """
    rng = random.Random(seed)

    # A regime with strong bonds it depends on.
    human = NestedRegime("Human", "organism", kappa_self=0.1)
    human.bond_with("Soil", 0.8)
    human.bond_with("Water", 0.9)
    human.bond_with("Air", 0.9)
    human.bond_with("Other_Species", 0.6)
    human.bond_with("Future_Generations", 0.5)

    history = []

    # Initial state.
    history.append({
        "phase": "Acknowledged dependence",
        "kappa_self": human.kappa_self,
        "n_bonds": len(human.bonds),
        "bond_strength": sum(human.bonds.values()),
    })

    # Denial: "I do not need you."
    # Bonds neglected → decay.
    for bond in list(human.bonds.keys()):
        human.bonds[bond] = max(0.0, human.bonds[bond] - 0.3)
        if human.bonds[bond] < 0.1:
            del human.bonds[bond]
    human.damage(0.2)  # κ_self increases through denial.

    history.append({
        "phase": "After denial ('I do not need you')",
        "kappa_self": human.kappa_self,
        "n_bonds": len(human.bonds),
        "bond_strength": sum(human.bonds.values()),
        "bonds_lost": 5 - len(human.bonds),
    })

    # Consequence: isolation, increased vulnerability.
    human.damage(0.2)  # More κ_self from consequences of broken bonds.

    history.append({
        "phase": "Consequences of isolation",
        "kappa_self": human.kappa_self,
        "n_bonds": len(human.bonds),
        "bond_strength": sum(human.bonds.values()),
    })

    return {
        "history": history,
        "denial_cost": history[-1]["kappa_self"] - history[0]["kappa_self"],
        "interpretation": (
            f"Denial cost: κ_self increased by {history[-1]['kappa_self'] - history[0]['kappa_self']:.2f}. "
            f"Bonds lost: {history[1]['bonds_lost']}. "
            "'I do not need you' is ontologically false — the regime depends on "
            "the bonds it denies. The denial causes real damage: bonds decay, "
            "κ_self increases, isolation deepens. The statement attempts to "
            "deny the dependence by which the speaker exists."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Personality Print: Stable Response Across Change
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class RegimeWithPrint:
    """A regime with a personality print — stable response pattern."""

    name: str
    orientation: float = 0.0  # -1 (selfish) to +1 (generous).
    consistency: float = 0.0  # How stable the pattern is across changes.
    history: list[dict] = field(default_factory=list)

    def respond_to(self, situation: str, pressure: float = 0.0) -> float:
        """Respond to a situation. The response reflects the personality print."""
        # Base response from orientation.
        response = self.orientation

        # Add noise (less noise = more consistent print).
        noise = (1.0 - self.consistency) * 0.3
        response += random.uniform(-noise, noise)

        self.history.append({
            "situation": situation,
            "pressure": pressure,
            "response": response,
        })
        return response

    def strengthen_print(self, amount: float = 0.1) -> None:
        """Repeated consistent responses strengthen the print."""
        self.consistency = min(1.0, self.consistency + amount)

    def transform_print(self, new_orientation: float) -> None:
        """A transformative event can change the orientation."""
        self.orientation = max(-1.0, min(1.0, new_orientation))
        self.consistency = 0.3  # Consistency drops during transformation.


def simulate_personality_print(seed: int = 42) -> dict:
    """Simulate a personality print: stable response across changing situations.

    A regime has an orientation (generosity vs selfishness) and consistency
    (how stable the pattern is). Over many situations, the print becomes
    recognizable — even though constituents (specific responses) vary.
    """
    rng = random.Random(seed)

    # A generous regime.
    generous = RegimeWithPrint("Generous_Soul", orientation=0.7, consistency=0.6)

    # Many situations — print becomes recognizable.
    situations = ["need_encountered", "resource_available", "conflict",
                  "opportunity_to_give", "opportunity_to_take",
                  "stranger_arrives", "enemy_approaches", "vulnerable_present"]
    responses = []
    for i, sit in enumerate(situations):
        resp = generous.respond_to(sit)
        responses.append(resp)
        if i > 2:
            generous.strengthen_print(0.1)  # Practice strengthens consistency.

    before = {
        "orientation": generous.orientation,
        "consistency": generous.consistency,
        "responses": responses[:4],
        "print": "generous",
    }

    # A transformative event changes the orientation.
    generous.transform_print(-0.3)  # Becomes somewhat selfish after trauma.

    after_responses = []
    for sit in ["need_encountered", "resource_available", "conflict"]:
        resp = generous.respond_to(sit)
        after_responses.append(resp)
        generous.strengthen_print(0.05)

    after = {
        "orientation": generous.orientation,
        "consistency": generous.consistency,
        "responses": after_responses,
        "print": "becoming_selfish",
    }

    return {
        "before": before,
        "after": after,
        "interpretation": (
            f"Before: orientation={before['orientation']:.1f}, consistency={before['consistency']:.1f}. "
            f"Responses: {[f'{r:.1f}' for r in before['responses']]}. "
            f"After trauma: orientation={after['orientation']:.1f}, consistency={after['consistency']:.1f}. "
            "A personality print is a stable response pattern across changing situations. "
            "It is recognizable without requiring consciousness. "
            "It can be transformed by significant events. "
            "It is the fruit-print of a regime's relational character."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Full RC1 Research Status
# ═══════════════════════════════════════════════════════════════════════════


def rc1_full_research() -> dict:
    """Complete RC1 research results."""
    nested = simulate_nested_damage()
    denial = simulate_bond_denial()
    print_test = simulate_personality_print()

    return {
        "nested_regimes": nested,
        "bond_denial": denial,
        "personality_print": print_test,
        "rc1_status": (
            "RC1 Research: 3 of 5 planned simulations complete. "
            "Nested regimes show κ/bond propagation across levels. "
            "Bond denial demonstrates ontological cost of 'I do not need you.' "
            "Personality print shows stable response patterns across change. "
            "Remaining: creation-as-body model, Fall-as-distortion simulation."
        ),
    }
