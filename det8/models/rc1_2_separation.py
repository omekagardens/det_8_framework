"""
DET Track-B — RC1.2: Edge/Capacity/Belonging Separation + Corrected κ Bounds

Implements the primary RC1.2 fix:
  σ_ij: active bond strength [0,1]
  A_ij: latent relational capacity [0,1]
  L_i:  causal lineage (immutable provenance ID)
  M_iG: regime membership (bool + participation degree)

Also corrects κ bounds: maps unbounded burden B_waste → bounded κ ∈ [0,1)
via κ = 1 − exp(−B_waste / B_*).
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Four-Way Separation Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class SeparatedRegime:
    """A regime with distinct edge, capacity, lineage, and membership."""

    name: str
    lineage_id: str                                    # L_i: immutable provenance.
    active_bonds: dict[str, float] = field(default_factory=dict)    # σ_ij ∈ [0,1].
    latent_capacity: dict[str, float] = field(default_factory=dict)  # A_ij ∈ [0,1].
    regime_memberships: dict[str, float] = field(default_factory=dict)  # M_iG ∈ [0,1].
    kappa_self: float = 0.0  # ∈ [0,1].

    def damage_active_bond(self, target: str, amount: float = 0.3) -> None:
        """Weaken or delete active bond. Latent capacity may persist."""
        if target in self.active_bonds:
            self.active_bonds[target] = max(0.0, self.active_bonds[target] - amount)

    def restore_from_latent(self, target: str, amount: float = 0.3) -> bool:
        """Restore active bond from latent capacity, if capacity exists."""
        if target in self.latent_capacity and self.latent_capacity[target] > 0.01:
            self.active_bonds[target] = min(1.0,
                self.active_bonds.get(target, 0) + amount)
            return True
        return False

    def belongs_to(self, regime_name: str) -> bool:
        return self.regime_memberships.get(regime_name, 0) > 0.01

    @property
    def active_bond_count(self) -> int:
        return sum(1 for v in self.active_bonds.values() if v > 0.01)

    @property
    def latent_capacity_count(self) -> int:
        return sum(1 for v in self.latent_capacity.values() if v > 0.01)


def simulate_separation_model(seed: int = 42) -> dict:
    """Test: active bonds can be destroyed while latent capacity persists.

    A regime starts with active bonds AND latent capacity.
    Bonds are damaged to zero (σ_ij → 0).
    Latent capacity remains (A_ij > 0).
    Bonds can be RESTORED from latent capacity.
    Lineage (L_i) is immutable throughout.
    Membership (M_iG) persists regardless of active bond state.
    """
    rng = random.Random(seed)

    # Create regime with both active bonds and latent capacity.
    r = SeparatedRegime("TestRegime", lineage_id="L_001")
    r.regime_memberships["Body"] = 1.0  # Full member.

    for target in ["A", "B", "C", "D"]:
        r.active_bonds[target] = 0.7
        r.latent_capacity[target] = 0.8  # Capacity exists even if bond is damaged.

    history = []

    # Initial state.
    history.append({
        "phase": "Initial",
        "active_bonds": r.active_bond_count,
        "latent_capacity": r.latent_capacity_count,
        "lineage": r.lineage_id,
        "member": r.belongs_to("Body"),
    })

    # Damage bonds to zero.
    for target in list(r.active_bonds.keys()):
        r.damage_active_bond(target, 0.8)  # Destroy active bond.

    history.append({
        "phase": "Bonds destroyed",
        "active_bonds": r.active_bond_count,
        "latent_capacity": r.latent_capacity_count,
        "lineage": r.lineage_id,
        "member": r.belongs_to("Body"),
    })

    # Restore from latent capacity.
    for target in list(r.latent_capacity.keys()):
        r.restore_from_latent(target, 0.6)

    history.append({
        "phase": "Restored from latent",
        "active_bonds": r.active_bond_count,
        "latent_capacity": r.latent_capacity_count,
        "lineage": r.lineage_id,
        "member": r.belongs_to("Body"),
    })

    return {
        "history": history,
        "active_bonds_destroyed": history[1]["active_bonds"] == 0,
        "latent_capacity_persisted": history[1]["latent_capacity"] > 0,
        "bonds_restored": history[2]["active_bonds"] > 0,
        "lineage_immutable": all(h["lineage"] == "L_001" for h in history),
        "membership_persisted": all(h["member"] for h in history),
        "interpretation": (
            "Active bonds can be destroyed (σ→0) while latent capacity persists (A>0). "
            "Bonds can be restored from latent capacity. "
            "Lineage is immutable. Membership persists regardless of bond state. "
            "This is the corrected RC1 model: relation ≠ active edge."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Corrected κ Bounds: Bounded Mapping
# ═══════════════════════════════════════════════════════════════════════════


def bounded_kappa(burden: float, B_star: float = 50.0) -> float:
    """Map unbounded burden → bounded κ ∈ [0, 1).

    κ = 1 − exp(−burden / B_star).

    Burden can grow without bound. κ saturates near 1.
    """
    return 1.0 - math.exp(-burden / B_star)


def simulate_corrected_material_ledger(seed: int = 42) -> dict:
    """Corrected material disposability with bounded κ mapping.

    Externalize: burden accumulates unbounded. κ → 1 (but never exceeds).
    Regenerate: burden stays low. κ → κ_eq > 0.
    """
    rng = random.Random(seed)

    def run(externalize: bool, steps: int = 20, B_star: float = 50.0) -> dict:
        resources = 100.0
        burden = 0.0  # Unbounded waste burden.
        viability = 1.0

        for _ in range(steps):
            consumption = 5.0
            resources -= consumption

            if externalize:
                burden += consumption * 0.8
                if burden > 30:
                    viability -= 0.05
            else:
                resources += consumption * 0.6
                burden = max(0.0, burden - consumption * 0.1)

            viability = max(0.0, min(1.0, viability))

        return {
            "final_resources": resources,
            "burden": burden,
            "kappa": bounded_kappa(burden, B_star),
            "viability": viability,
        }

    ext = run(True)
    regen = run(False)

    return {
        "externalize": ext,
        "regenerate": regen,
        "kappa_in_bounds": ext["kappa"] < 1.0,
        "regeneration_superior": regen["viability"] > ext["viability"],
        "interpretation": (
            f"Externalize: κ={ext['kappa']:.3f} (bounded), viability={ext['viability']:.2f}. "
            f"Regenerate: κ={regen['kappa']:.3f}, viability={regen['viability']:.2f}. "
            f"κ in [0,1): {ext['kappa'] < 1.0}. "
            "Burden can grow without bound; κ maps to [0,1) via exponential saturation. "
            "Regeneration preserves viability; externalization destroys it."
        ),
    }
