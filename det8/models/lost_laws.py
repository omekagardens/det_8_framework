"""
DET Track-B — Lost Law Problem: κ-Obscured Discoverability

Simulates how κ can block access to previously-discovered law branches.
Demonstrates that laws are never deleted — only buried.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Library Model
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class LawLibrary:
    """A library of law branches. κ blocks access to shelves."""

    branches: dict[str, float] = field(default_factory=dict)  # branch → κ_threshold.
    kappa: float = 0.0

    def discover(self, branch_name: str) -> None:
        """Add a law branch to the library. Initially accessible."""
        self.branches[branch_name] = self.kappa  # Record κ at discovery.

    def is_accessible(self, branch_name: str) -> bool:
        """Check if a branch is accessible at current κ.

        A branch is accessible if current κ is below the threshold
        at which it was discovered PLUS the burial threshold.
        """
        if branch_name not in self.branches:
            return False
        discovery_kappa = self.branches[branch_name]
        burial_threshold = 3.0  # κ above discovery that buries the branch.
        return self.kappa < discovery_kappa + burial_threshold

    def accessible_branches(self) -> list[str]:
        """List all currently accessible branches."""
        return [b for b in self.branches if self.is_accessible(b)]

    def buried_branches(self) -> list[str]:
        """List all existing but inaccessible branches."""
        return [b for b in self.branches if not self.is_accessible(b)]

    def accumulate(self, delta: float = 0.5) -> None:
        """Accumulate κ — some branches may become buried."""
        self.kappa += delta

    def recover(self, delta: float = 0.5) -> None:
        """Reduce κ — buried branches may become accessible again."""
        self.kappa = max(0.0, self.kappa - delta)


def simulate_lost_laws(seed: int = 42) -> dict:
    """Simulate the lost law problem.

    Phase 1 (discovery): Discover several law branches at low κ.
    Phase 2 (catastrophe): κ spikes — most branches become buried.
    Phase 3 (recovery): κ reduces — some branches become accessible.
    Phase 4 (independent rediscovery): A buried branch is rediscovered
      through a different path (L extension).

    Shows: laws are never deleted. Only buried. Rediscovery is possible
    through κ-reduction OR independent L-extension.
    """
    library = LawLibrary()
    history = []

    # Phase 1: Discovery (κ=0).
    discoveries = ["mechanics", "electromagnetism", "thermodynamics",
                   "relativity", "quantum", "gravity_laws", "chemistry"]
    for branch in discoveries:
        library.discover(branch)

    history.append({
        "phase": "discovery", "kappa": library.kappa,
        "accessible": len(library.accessible_branches()),
        "buried": len(library.buried_branches()),
        "total": len(library.branches),
        "names": discoveries,
    })

    # Phase 2: Catastrophe (κ spike).
    for _ in range(8):
        library.accumulate(0.5)

    history.append({
        "phase": "catastrophe", "kappa": library.kappa,
        "accessible": len(library.accessible_branches()),
        "buried": len(library.buried_branches()),
        "total": len(library.branches),
        "buried_names": library.buried_branches(),
    })

    # Phase 3: Recovery (Jubilee / Grace).
    for _ in range(6):
        library.recover(0.5)

    history.append({
        "phase": "recovery", "kappa": library.kappa,
        "accessible": len(library.accessible_branches()),
        "buried": len(library.buried_branches()),
        "total": len(library.branches),
        "recovered": [b for b in library.accessible_branches()
                      if b in history[1].get("buried_names", [])],
    })

    # Phase 4: Independent rediscovery (L extension from different path).
    # Even buried branches can be rediscovered — added again to L.
    if library.buried_branches():
        rediscovered = library.buried_branches()[0]
        library.discover(rediscovered + "_v2")  # New path to same law.

    history.append({
        "phase": "rediscovery", "kappa": library.kappa,
        "accessible": len(library.accessible_branches()),
        "buried": len(library.buried_branches()),
        "total": len(library.branches),
    })

    return {
        "history": history,
        "interpretation": (
            f"Discovery: {history[0]['accessible']} accessible. "
            f"Catastrophe: κ={history[1]['kappa']:.0f}, only {history[1]['accessible']} accessible, "
            f"{history[1]['buried']} buried: {history[1].get('buried_names', [])}. "
            f"Recovery: κ={history[2]['kappa']:.0f}, {history[2]['accessible']} accessible again. "
            f"Rediscovery: added new path to buried law. Total branches: {history[3]['total']}. "
            "Laws are never deleted — only buried. κ-reduction restores access. "
            "Independent rediscovery adds new paths to the same truth."
        ),
    }
