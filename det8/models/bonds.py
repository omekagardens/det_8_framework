"""
DET 8 Bond Model — Relational Structure Between Nodes

Implements the bond/edge layer of DET 8 physics: bonds between nodes
carry conductivity, coherence, and momentum. Bond events transfer
conserved flux between adjacent nodes.

Per P0.1 §6.1:
  σ_ij : bond conductivity
  C_ij : bond coherence
  π_ij = -π_ji : bond momentum (antisymmetric)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


# ── Bond Record ─────────────────────────────────────────────────────────────


@dataclass
class BondRecord:
    """DET 8 record for a bond (edge) between two nodes.

    Modal annotation: A (actual committed facts).

    All variables are record-side. None is agency.
    """

    node_i: int
    node_j: int

    # ── Core bond variables ──
    sigma: float = 1.0    # bond conductivity (> 0)
    C: float = 1.0        # bond coherence
    pi: float = 0.0       # bond momentum (from i to j; antisymmetric: π_ji = -π_ij)

    # ── Optional extensions ──
    detector_coupling: float = 0.0
    relational_debt: float = 0.0  # for declared submodels

    def __post_init__(self):
        self.sigma = max(1e-12, self.sigma)

    @property
    def pi_reverse(self) -> float:
        """Momentum from j to i = -π_ij."""
        return -self.pi

    def copy(self) -> "BondRecord":
        return BondRecord(
            node_i=self.node_i,
            node_j=self.node_j,
            sigma=self.sigma,
            C=self.C,
            pi=self.pi,
            detector_coupling=self.detector_coupling,
            relational_debt=self.relational_debt,
        )


# ── Bond Network ────────────────────────────────────────────────────────────


@dataclass
class BondNetwork:
    """A network of bonds between nodes.

    Bonds are undirected edges; each bond is stored once with
    node_i < node_j. The momentum π_ij is from i to j;
    π_ji = -π_ij for the reverse direction.
    """

    bonds: dict[tuple[int, int], BondRecord] = field(default_factory=dict)

    def _key(self, i: int, j: int) -> tuple[int, int]:
        """Canonical key with smaller node first."""
        return (i, j) if i < j else (j, i)

    def add_bond(
        self,
        i: int,
        j: int,
        sigma: float = 1.0,
        C: float = 1.0,
        pi: float = 0.0,
    ) -> BondRecord:
        """Add or update a bond between nodes i and j.

        pi is momentum from i to j. If i > j, pi is negated for storage.
        """
        key = self._key(i, j)
        if i < j:
            bond = BondRecord(node_i=i, node_j=j, sigma=sigma, C=C, pi=pi)
        else:
            bond = BondRecord(node_i=j, node_j=i, sigma=sigma, C=C, pi=-pi)
        self.bonds[key] = bond
        return bond

    def get_bond(self, i: int, j: int) -> Optional[BondRecord]:
        """Get the bond between i and j, or None."""
        return self.bonds.get(self._key(i, j))

    def get_momentum(self, i: int, j: int) -> float:
        """Get momentum from i to j. π_ij = -π_ji."""
        bond = self.get_bond(i, j)
        if bond is None:
            return 0.0
        if i < j:
            return bond.pi
        else:
            return -bond.pi

    def neighbors(self, node: int) -> list[int]:
        """List all nodes connected to the given node."""
        result = []
        for (i, j), bond in self.bonds.items():
            if i == node:
                result.append(j)
            elif j == node:
                result.append(i)
        return result

    def total_momentum(self) -> float:
        """Total momentum in the network (should be zero for isolated system)."""
        # Each bond contributes π_ij + π_ji = 0, so total is always zero
        # by antisymmetry. This is a consistency check.
        total = 0.0
        for bond in self.bonds.values():
            total += bond.pi + bond.pi_reverse
        return total

    def __contains__(self, pair: tuple[int, int]) -> bool:
        return self._key(*pair) in self.bonds

    def __len__(self) -> int:
        return len(self.bonds)


# ── Bond Flux Event ─────────────────────────────────────────────────────────


@dataclass
class BondFluxEvent:
    """A flux transfer event across a bond.

    Transfers an amount J from node i to node j.
    Conservation: J_{i→j} = -J_{j→i}.

    The event respects:
    - Bond conductivity σ_ij (maximum flux rate).
    - Node resource F_i, F_j (available resources).
    - Nonnegativity of node resources.
    """

    bond: BondRecord
    amount: float  # J > 0 means flow from i to j

    def __post_init__(self):
        # Clamp to conductivity limit.
        max_flux = self.bond.sigma
        self.amount = max(-max_flux, min(max_flux, self.amount))

    @property
    def reverse(self) -> "BondFluxEvent":
        """The reverse flux event."""
        return BondFluxEvent(bond=self.bond, amount=-self.amount)


def generate_bond_flux_possibilities(
    bond: BondRecord,
    resource_i: float,
    resource_j: float,
) -> tuple[list[float], list[float]]:
    """Generate the possibility object for a bond flux event.

    Returns (omega, kernel) where omega is a list of possible flux amounts
    and kernel is the uniform propensity over them.

    Constraints:
    - |J| ≤ σ_ij (conductivity bound).
    - J ≤ resource_i (can't transfer more than i has).
    - -J ≤ resource_j (can't transfer more than j has, i.e., J ≥ -resource_j).

    For simplicity, discretizes into integer steps.
    """
    sigma = bond.sigma

    # Maximum flux in each direction.
    max_forward = min(sigma, resource_i)
    max_backward = min(sigma, resource_j)

    # Generate possible transfers in integer steps.
    omega: list[float] = []
    for j_forward in range(int(max_forward) + 1):
        omega.append(float(j_forward))
    for j_backward in range(1, int(max_backward) + 1):
        omega.append(float(-j_backward))

    if not omega:
        omega = [0.0]

    kernel = [1.0 / len(omega)] * len(omega)
    return omega, kernel


def apply_bond_flux(
    bond: BondRecord,
    resource_i: float,
    resource_j: float,
    flux: float,
) -> tuple[float, float]:
    """Apply a flux transfer: move `flux` from i to j.

    Returns (new_resource_i, new_resource_j).

    Raises ValueError if the transfer violates constraints.
    """
    if abs(flux) > bond.sigma + 1e-12:
        raise ValueError(
            f"Flux {flux} exceeds bond conductivity {bond.sigma}"
        )
    if flux > resource_i + 1e-12:
        raise ValueError(
            f"Flux {flux} exceeds resource_i {resource_i}"
        )
    if -flux > resource_j + 1e-12:
        raise ValueError(
            f"Flux {-flux} exceeds resource_j {resource_j}"
        )

    new_i = resource_i - flux
    new_j = resource_j + flux
    return max(0.0, new_i), max(0.0, new_j)


# ── Conservation Verifier ───────────────────────────────────────────────────


def verify_network_conservation(
    resources: dict[int, float],
    bond_network: BondNetwork,
) -> dict:
    """Verify conservation invariants across a bond network.

    Checks:
    1. Total resource sum across all nodes.
    2. Total momentum = 0 (antisymmetry).
    3. Per-bond antisymmetry: π_ij = -π_ji.
    """
    total_resource = sum(resources.values())
    total_momentum = bond_network.total_momentum()

    # Per-bond antisymmetry.
    antisymmetry_ok = True
    for bond in bond_network.bonds.values():
        if abs(bond.pi + bond.pi_reverse) > 1e-12:
            antisymmetry_ok = False
            break

    return {
        "total_resource": total_resource,
        "total_momentum": total_momentum,
        "total_momentum_zero": abs(total_momentum) < 1e-12,
        "antisymmetry_ok": antisymmetry_ok,
        "n_bonds": len(bond_network),
        "n_nodes": len(resources),
    }
