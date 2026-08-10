"""
DET κ-Diffusion on Bond Networks

Models how structural history (κ) propagates through a connected
system via bonds. Damage to one node spreads to neighbors through
conductive bonds. Recovery acts locally.

DET primitives:
  - Bond network with conductivity σ_ij.
  - κ as per-node structural history density.
  - Diffusion: dκ_i/dt = D · Σ_j σ_ij · (κ_j - κ_i).
  - Local recovery: dκ_i/dt = -(κ_i - κ_eq)/τ_rec.
  - Local damage: dκ_i/dt = +α · (event rate) · (1-κ_i).

Combined dynamics:
  dκ_i/dt = D·Σ_j σ_ij·(κ_j-κ_i) - (κ_i-κ_eq)/τ_rec + damage_rate

This is the DET-native heat/diffusion equation on the event graph.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ── Diffusion Parameters ────────────────────────────────────────────────────


@dataclass
class DiffusionParams:
    """Parameters for κ-diffusion on a bond network."""

    D: float = 0.1          # Diffusion coefficient.
    tau_rec: float = 10.0   # Recovery time scale.
    kappa_eq: float = 0.0   # Equilibrium κ (fully recovered).
    alpha_damage: float = 0.01  # Damage coefficient per event.


# ── κ-Diffusion on Graph ────────────────────────────────────────────────────


def kappa_diffusion_step(
    kappa: dict[int, float],
    bonds: dict[tuple[int, int], float],  # (i,j) → σ_ij.
    params: DiffusionParams,
    dt: float = 0.01,
    damage_nodes: Optional[set[int]] = None,
) -> dict[int, float]:
    """Evolve κ by one time step using graph diffusion + recovery + damage.

    Args:
        kappa: Current κ values per node.
        bonds: Bond conductivities σ_ij.
        params: Diffusion parameters.
        dt: Time step.
        damage_nodes: Set of nodes receiving damage this step.

    Returns:
        Updated κ values.
    """
    new_kappa = {}
    damage_set = damage_nodes or set()

    for i in kappa:
        # Diffusion: sum over neighbors.
        diffusion = 0.0
        for (a, b), sigma in bonds.items():
            if a == i and b in kappa:
                diffusion += sigma * (kappa[b] - kappa[i])
            elif b == i and a in kappa:
                diffusion += sigma * (kappa[a] - kappa[i])

        # Recovery: relax toward equilibrium.
        recovery = -(kappa[i] - params.kappa_eq) / params.tau_rec

        # Damage: apply if this node is being damaged.
        damage = 0.0
        if i in damage_set:
            damage = params.alpha_damage * (1.0 - kappa[i])

        # Update.
        dk = (params.D * diffusion + recovery + damage) * dt
        new_kappa[i] = max(0.0, min(1.0, kappa[i] + dk))

    return new_kappa


def simulate_diffusion(
    initial_kappa: dict[int, float],
    bonds: dict[tuple[int, int], float],
    params: Optional[DiffusionParams] = None,
    n_steps: int = 100,
    dt: float = 0.1,
    damage_schedule: Optional[dict[int, list[int]]] = None,
) -> list[dict[int, float]]:
    """Simulate κ-diffusion over multiple time steps.

    Args:
        initial_kappa: Starting κ values.
        bonds: Bond conductivities.
        params: Diffusion parameters.
        n_steps: Number of time steps.
        dt: Time step size.
        damage_schedule: {step: [node_ids]} — which nodes get damaged at which step.

    Returns:
        History of κ values at each step.
    """
    if params is None:
        params = DiffusionParams()

    kappa = dict(initial_kappa)
    history = [dict(kappa)]

    for step in range(n_steps):
        damage_nodes = set()
        if damage_schedule and step in damage_schedule:
            damage_nodes = set(damage_schedule[step])

        kappa = kappa_diffusion_step(kappa, bonds, params, dt, damage_nodes)
        history.append(dict(kappa))

    return history


# ── Demonstration: Damage Propagation ───────────────────────────────────────


def demonstrate_damage_propagation() -> dict:
    """Demonstrate how damage propagates through a bond network.

    Three nodes in a line: 0 — 1 — 2.
    Node 0 receives damage at t=0.
    The damage diffuses to nodes 1 and 2 over time.
    Recovery gradually reduces κ everywhere.
    """
    bonds = {(0, 1): 1.0, (1, 2): 0.5}  # σ_01=1.0, σ_12=0.5.
    kappa = {0: 0.0, 1: 0.0, 2: 0.0}

    params = DiffusionParams(D=0.1, tau_rec=20.0, kappa_eq=0.0, alpha_damage=0.5)
    damage_schedule = {0: [0]}  # Damage node 0 at step 0.

    history = simulate_diffusion(
        kappa, bonds, params, n_steps=200, dt=0.1, damage_schedule=damage_schedule
    )

    # Extract key time points.
    snapshots = {}
    for t in [0, 10, 50, 100, 200]:
        if t < len(history):
            snapshots[f"t={t}"] = history[t]

    return {
        "topology": "0 — 1 — 2 (σ_01=1.0, σ_12=0.5)",
        "damage": "Node 0 at t=0",
        "snapshots": snapshots,
        "final": history[-1],
        "interpretation": (
            "Damage at node 0 diffuses to node 1 (high conductivity) "
            "and weakly to node 2 (lower conductivity). Recovery "
            "gradually reduces κ everywhere. This is the DET-native "
            "model of how structural history spreads through connected systems."
        ),
    }
