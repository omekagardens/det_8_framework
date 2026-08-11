"""
DET Track-B — Law Discovery Through Multiple Independent Paths

Demonstrates that the same law branch can be discovered through
different record-paths. Laws are discovered, not created. Burial
doesn't destroy — it only blocks one path while others may remain.

Simulation:
  1. Civilization A discovers laws through a specific record-path.
  2. Catastrophe buries Civilization A's discoveries under high κ.
  3. Civilization B independently discovers the SAME laws through
     a different record-path (different history, same truth).
  4. Later, κ-reduction (Jubilee) restores Civilization A's path —
     the same laws are now accessible through TWO independent paths.

Key DET insight:
  L contains the law branch. It was added when A discovered it.
  κ blocked A's path, but B found a different path to the same branch.
  The branch was never deleted — only one path was buried.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Law Discovery Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class LawBranch:
    """A law branch in L. Can be discovered through multiple paths."""

    name: str
    discovery_paths: list[str] = field(default_factory=list)  # Who discovered it.
    accessible_paths: set[str] = field(default_factory=set)    # Currently accessible.

    @property
    def is_accessible(self) -> bool:
        return len(self.accessible_paths) > 0

    @property
    def n_paths(self) -> int:
        return len(self.discovery_paths)


@dataclass
class Civilization:
    """A civilization with its own record-path and κ level."""

    name: str
    kappa: float = 0.0
    discovered: set[str] = field(default_factory=set)

    def can_discover(self, burial_threshold: float = 3.0) -> bool:
        """Can this civilization discover new laws at current κ?"""
        return self.kappa < burial_threshold

    def discover(self, branch_name: str) -> None:
        """Discover a law branch."""
        self.discovered.add(branch_name)

    def accumulate_kappa(self, delta: float = 0.5) -> None:
        self.kappa += delta

    def recover_kappa(self, delta: float = 0.5) -> None:
        self.kappa = max(0.0, self.kappa - delta)


def simulate_independent_discovery(seed: int = 42) -> dict:
    """Simulate independent discovery of the same laws.

    Phase 1: Civilization A discovers laws at low κ.
    Phase 2: Catastrophe — A's κ spikes, burying discoveries.
    Phase 3: Civilization B independently discovers same laws.
    Phase 4: A recovers (Jubilee) — laws now accessible through 2 paths.
    """
    rng = random.Random(seed)

    # The law branches that exist in L (waiting to be discovered).
    law_branches = {
        "mechanics": LawBranch("mechanics"),
        "electromagnetism": LawBranch("electromagnetism"),
        "thermodynamics": LawBranch("thermodynamics"),
        "relativity": LawBranch("relativity"),
        "quantum": LawBranch("quantum"),
    }

    # Phase 1: Civilization A discovers.
    civ_a = Civilization("Civilization A", kappa=0.0)
    for branch_name in law_branches:
        civ_a.discover(branch_name)
        law_branches[branch_name].discovery_paths.append("A")
        law_branches[branch_name].accessible_paths.add("A")

    phase1 = {
        "phase": "Discovery (A)",
        "A_kappa": civ_a.kappa,
        "A_discoveries": list(civ_a.discovered),
        "accessible_branches": sum(1 for b in law_branches.values() if b.is_accessible),
        "total_branches": len(law_branches),
    }

    # Phase 2: Catastrophe buries A's discoveries.
    for _ in range(8):
        civ_a.accumulate_kappa(0.5)

    # At high κ, A's path is blocked — but branches still exist.
    for branch_name in law_branches:
        if civ_a.kappa >= 3.0:
            law_branches[branch_name].accessible_paths.discard("A")

    phase2 = {
        "phase": "Catastrophe (A buried)",
        "A_kappa": civ_a.kappa,
        "A_can_discover": civ_a.can_discover(),
        "accessible_branches": sum(1 for b in law_branches.values() if b.is_accessible),
        "total_branches": len(law_branches),
        "buried_names": [n for n, b in law_branches.items() if not b.is_accessible],
    }

    # Phase 3: Civilization B independently discovers same laws.
    civ_b = Civilization("Civilization B", kappa=0.0)
    for branch_name in law_branches:
        civ_b.discover(branch_name)
        law_branches[branch_name].discovery_paths.append("B")
        law_branches[branch_name].accessible_paths.add("B")

    phase3 = {
        "phase": "Rediscovery (B)",
        "B_kappa": civ_b.kappa,
        "B_discoveries": list(civ_b.discovered),
        "accessible_branches": sum(1 for b in law_branches.values() if b.is_accessible),
        "total_branches": len(law_branches),
        "paths_per_branch": {n: b.n_paths for n, b in law_branches.items()},
    }

    # Phase 4: A recovers (Jubilee) — laws now accessible through 2 paths.
    for _ in range(6):
        civ_a.recover_kappa(0.5)

    for branch_name in law_branches:
        if civ_a.kappa < 3.0:
            law_branches[branch_name].accessible_paths.add("A")

    phase4 = {
        "phase": "Recovery (A + B)",
        "A_kappa": civ_a.kappa,
        "B_kappa": civ_b.kappa,
        "accessible_branches": sum(1 for b in law_branches.values() if b.is_accessible),
        "total_branches": len(law_branches),
        "paths_per_branch": {n: b.n_paths for n, b in law_branches.items()},
        "accessible_via": {
            n: list(b.accessible_paths) for n, b in law_branches.items()
        },
    }

    return {
        "phases": [phase1, phase2, phase3, phase4],
        "interpretation": (
            f"Discovery: {phase1['total_branches']} laws known through 1 path (A). "
            f"Catastrophe: κ={civ_a.kappa:.0f} blocks A's path — 0 accessible. "
            f"Rediscovery: B finds ALL {phase3['total_branches']} independently — 2 paths now. "
            f"Recovery: A's path restored — ALL laws accessible through 2 independent paths. "
            "Laws are NEVER deleted. Only paths are buried. "
            "The same truth can be reached through different histories. "
            "Independent discovery IS the evidence that laws exist independently of any one knower."
        ),
    }
