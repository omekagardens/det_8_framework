"""
DET Track-B — RC1 Research: Creation-as-Body + Fall-as-Distortion

Completes RC1 with the two remaining simulations:
  4. Creation-as-Body: Christ as personal unity of nested creation.
  5. Fall-as-Distortion: κ_self increases but bonds persist (damaged, not destroyed).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 4. Creation-as-Body: Christ as Personal Unity
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class BodyRegime:
    """A regime within Christ's body. Has κ_self, bonds, and body-identity."""

    name: str
    role: str  # "cell", "organ", "member", "firstfruits", "head"
    kappa_self: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    recognizes_body: bool = False  # Does this regime recognize it's part of the body?

    def damage(self, amount: float = 0.1) -> None:
        self.kappa_self = min(1.0, self.kappa_self + amount)

    def heal(self, amount: float = 0.1) -> None:
        self.kappa_self = max(0.0, self.kappa_self - amount)

    def awaken(self) -> None:
        """Recognize belonging to the body."""
        self.recognizes_body = True

    @property
    def state(self) -> str:
        if not self.recognizes_body and self.kappa_self > 0.5:
            return "lost (high κ, unaware)"
        elif not self.recognizes_body:
            return "unaware (low κ, not yet awakened)"
        elif self.kappa_self < 0.2:
            return "healed (low κ, aware)"
        else:
            return "healing (κ decreasing, aware)"


def simulate_creation_as_body(seed: int = 42) -> dict:
    """Simulate creation as Christ's body.

    All regimes already belong to the body (BC-4 hypothesis).
    Some recognize it (church as firstfruits). Some don't.
    The Fall distorted expression but didn't remove belonging.
    Redemption heals the body from within.
    """
    rng = random.Random(seed)

    # Creation as nested body.
    christ = BodyRegime("Christ", "head", kappa_self=0.0, recognizes_body=True)
    church = BodyRegime("Church", "firstfruits", kappa_self=0.2, recognizes_body=True)
    humanity = BodyRegime("Humanity", "member", kappa_self=0.5)
    animals = BodyRegime("Animals", "member", kappa_self=0.1)
    earth = BodyRegime("Earth", "member", kappa_self=0.4)

    # All already belong to Christ.
    all_members = [christ, church, humanity, animals, earth]

    # Bonds within the body.
    for a in all_members:
        for b in all_members:
            if a.name != b.name:
                a.bonds[b.name] = 0.5  # All connected.

    history = []

    # Phase 1: Fallen state — most don't recognize the body.
    history.append({
        "phase": "Fallen creation",
        "states": {m.name: {"κ": m.kappa_self, "state": m.state} for m in all_members},
        "recognizing": [m.name for m in all_members if m.recognizes_body],
    })

    # Phase 2: Church (firstfruits) begins healing work.
    # Church's low κ and recognition enables it to serve others.
    for m in all_members:
        if m.name != "Christ":
            m.heal(0.1)  # Church's presence brings healing.

    history.append({
        "phase": "Church as firstfruits begins healing",
        "states": {m.name: {"κ": m.kappa_self, "state": m.state} for m in all_members},
    })

    # Phase 3: Humanity awakens to belonging.
    humanity.awaken()
    humanity.heal(0.2)

    history.append({
        "phase": "Humanity awakens to body identity",
        "states": {m.name: {"κ": m.kappa_self, "state": m.state} for m in all_members},
        "recognizing": [m.name for m in all_members if m.recognizes_body],
    })

    # Phase 4: Ongoing healing — body moving toward wholeness.
    for m in all_members:
        m.heal(0.1)

    history.append({
        "phase": "Body healing toward wholeness",
        "states": {m.name: {"κ": m.kappa_self, "state": m.state} for m in all_members},
        "recognizing": [m.name for m in all_members if m.recognizes_body],
    })

    return {
        "history": history,
        "all_always_belong": True,  # None were ever outside Christ's body.
        "interpretation": (
            "All creation already belongs to Christ's body (BC-4). "
            "The Fall distorted expression but didn't remove belonging. "
            "The church (firstfruits) recognizes the body and serves its healing. "
            "As members awaken, κ decreases, bonds strengthen. "
            "None were ever outside. All are being healed from within."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 5. Fall-as-Distortion: Damaged Bonds Persist
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class FallenRegime:
    """A regime that has fallen — relation distorted, not destroyed."""

    name: str
    kappa_self: float = 0.0
    bonds: dict[str, float] = field(default_factory=dict)
    bond_history: list[dict] = field(default_factory=list)

    def fall(self, severity: float = 0.3) -> None:
        """The Fall: relation distorted, not lost."""
        self.kappa_self = min(1.0, self.kappa_self + severity)

        # Bonds are DAMAGED, not destroyed.
        for bond in self.bonds:
            damage = severity * random.uniform(0.3, 0.7)
            self.bonds[bond] = max(0.1, self.bonds[bond] - damage)

        self.bond_history.append({
            "event": "fall",
            "kappa_self": self.kappa_self,
            "n_bonds": len(self.bonds),
            "bond_strength": sum(self.bonds.values()),
        })

    def receive_grace(self, amount: float = 0.2) -> None:
        """Grace heals κ_self and begins bond restoration."""
        self.kappa_self = max(0.0, self.kappa_self - amount)
        for bond in self.bonds:
            self.bonds[bond] = min(1.0, self.bonds[bond] + amount * 0.5)

        self.bond_history.append({
            "event": "grace",
            "kappa_self": self.kappa_self,
            "n_bonds": len(self.bonds),
            "bond_strength": sum(self.bonds.values()),
        })


def simulate_fall_as_distortion(seed: int = 42) -> dict:
    """Simulate the Fall as relational distortion, not loss.

    Before Fall: κ_self=0, bonds strong.
    Fall: κ_self increases, bonds DAMAGED but PERSIST.
    Grace: κ_self decreases, bonds begin healing.
    Key: bonds were never destroyed — only damaged.
    """
    rng = random.Random(seed)

    # Pre-Fall state.
    adam = FallenRegime("Adam", kappa_self=0.0)
    adam.bonds = {
        "God": 1.0, "Eve": 1.0, "Animals": 0.8,
        "Earth": 0.9, "Self": 1.0,
    }

    history = []

    # Pre-Fall.
    history.append({
        "phase": "Eden (pre-Fall)",
        "kappa_self": adam.kappa_self,
        "n_bonds": len(adam.bonds),
        "bond_strength": sum(adam.bonds.values()),
        "bonds": dict(adam.bonds),
    })

    # Fall — relation distorted, bonds persist.
    adam.fall(0.5)

    history.append({
        "phase": "Fall (distorted, not destroyed)",
        "kappa_self": adam.kappa_self,
        "n_bonds": len(adam.bonds),
        "bond_strength": sum(adam.bonds.values()),
        "bonds": dict(adam.bonds),
    })

    # Continued fallen state.
    adam.fall(0.2)

    history.append({
        "phase": "Continued distortion",
        "kappa_self": adam.kappa_self,
        "n_bonds": len(adam.bonds),
        "bond_strength": sum(adam.bonds.values()),
        "bonds": dict(adam.bonds),
    })

    # Grace — healing begins.
    for _ in range(3):
        adam.receive_grace(0.15)

    history.append({
        "phase": "Grace (healing begins)",
        "kappa_self": adam.kappa_self,
        "n_bonds": len(adam.bonds),
        "bond_strength": sum(adam.bonds.values()),
        "bonds": dict(adam.bonds),
    })

    return {
        "history": history,
        "bonds_never_destroyed": all(h["n_bonds"] == 5 for h in history),
        "kappa_never_erased_identity": history[-1]["kappa_self"] < history[1]["kappa_self"],
        "interpretation": (
            f"Pre-Fall: κ=0.00, bonds=5, strength={history[0]['bond_strength']:.1f}. "
            f"Fall: κ→{history[1]['kappa_self']:.2f}, bonds STILL 5, strength→{history[1]['bond_strength']:.1f}. "
            f"Continued: κ→{history[2]['kappa_self']:.2f}, bonds STILL 5. "
            f"Grace: κ→{history[3]['kappa_self']:.2f}, bonds STILL 5, strength→{history[3]['bond_strength']:.1f}. "
            "The Fall distorted relation — it did not destroy it. "
            "Bonds persist through the Fall. Grace restores them. "
            "κ_self increases but identity remains. Healing is possible "
            "because the relational foundation was never lost."
        ),
    }
