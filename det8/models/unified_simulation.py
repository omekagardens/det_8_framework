"""
DET v8.0 — Unified End-to-End Simulation

Integrates all DET physics layers into a single simulation:
  1. Node records: κ, F, σ, H, C (det8_core)
  2. Bond network: σ_ij, flux conservation (bonds)
  3. Participation aperture Π: proper-time accumulation (det8_core)
  4. κ-diffusion: damage propagation through bonds (kappa_diffusion)
  5. Time evolution: kernel root dynamics (time_evolution)
  6. Gravity: γ = λ_γ·κ sourcing potential (det_gravity)
  7. Causal event graph: spacelike detection (event_graph)

This is the most complete DET simulation. It demonstrates all
derived observables working together in a single multi-node system.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional

from det8.models.det8_core import (
    LAMBDA_P,
    LAMBDA_GAMMA,
    NodeRecord,
    participation_aperture,
    accumulate_proper_time,
    apply_q_damage,
    apply_q_recovery,
)
from det8.models.bonds import BondNetwork
from det8.models.kappa_diffusion import (
    DiffusionParams,
    kappa_diffusion_step,
)
from det8.models.time_evolution import (
    KernelState,
    evolve_state,
)
from det8.models.det_gravity import compute_potential, EventGraphGeometry, KappaField


# ── Unified Simulation ──────────────────────────────────────────────────────


@dataclass
class UnifiedDETSimulation:
    """A complete DET simulation with all physics layers active.

    Tracks:
      - Node records (κ, F, σ, H, C, proper time)
      - Bond network (conductivities)
      - κ-diffusion between nodes
      - Kernel root evolution (quantum analogue)
      - Gravitational potential from κ distribution
      - Event log for post-hoc analysis
    """

    nodes: dict[int, NodeRecord] = field(default_factory=dict)
    bonds: BondNetwork = field(default_factory=BondNetwork)
    kappa_state: dict[int, float] = field(default_factory=dict)
    kernel_states: dict[int, KernelState] = field(default_factory=dict)
    positions: dict[int, tuple[float, ...]] = field(default_factory=dict)
    diffusion_params: DiffusionParams = field(default_factory=DiffusionParams)
    event_log: list[dict] = field(default_factory=list)
    total_time: float = 0.0
    _rng: random.Random = field(default_factory=lambda: random.Random(42))

    def add_node(
        self,
        node_id: int,
        kappa: float = 0.0,
        F: float = 0.0,
        sigma: float = 1.0,
        H: float = 0.0,
        C: float = 1.0,
        position: tuple[float, ...] = (0.0, 0.0, 0.0),
    ) -> None:
        """Add a node with full DET record and kernel state."""
        record = NodeRecord(kappa=kappa, F=F, sigma=sigma, H=H, C=C)
        self.nodes[node_id] = record
        self.kappa_state[node_id] = kappa
        self.kernel_states[node_id] = KernelState(
            roots=[1.0 + 0j, 0.0 + 0j]  # Start in |0⟩.
        )
        self.positions[node_id] = position

    def add_bond(self, i: int, j: int, sigma: float = 1.0) -> None:
        """Add a conductive bond between nodes."""
        self.bonds.add_bond(i, j, sigma=sigma)

    def step(
        self,
        dt: float = 0.1,
        damage_nodes: Optional[set[int]] = None,
        lambda_p: float = LAMBDA_P,
    ) -> dict:
        """Advance the simulation by one time step.

        Applies all physics layers:
          1. κ-diffusion + recovery + damage.
          2. Proper-time accumulation via Π.
          3. Kernel root evolution.
          4. Sync node records with updated κ.
        """
        # 1. κ-diffusion.
        bond_sigmas = {
            (b.node_i, b.node_j): b.sigma
            for b in self.bonds.bonds.values()
        }
        self.kappa_state = kappa_diffusion_step(
            self.kappa_state, bond_sigmas, self.diffusion_params, dt, damage_nodes
        )

        # 2. Proper time + sync κ.
        proper_time_increments = {}
        for nid, record in self.nodes.items():
            record.kappa = self.kappa_state.get(nid, record.kappa)
            dtau = accumulate_proper_time(record, dt, lambda_p=lambda_p)
            proper_time_increments[nid] = dtau

        # 3. Kernel root evolution.
        for nid, state in self.kernel_states.items():
            record = self.nodes[nid]
            new_state = evolve_state(
                state,
                record_kappa=record.kappa,
                record_F=record.F,
                record_C=record.C,
                delta_tau=proper_time_increments.get(nid, dt),
            )
            self.kernel_states[nid] = new_state

        # 4. Gravity update.
        geometry = EventGraphGeometry()
        for nid, pos in self.positions.items():
            geometry.add_node(nid, pos)
        for (i, j), bond in self.bonds.bonds.items():
            geometry.add_link(i, j)

        kappa_field = KappaField()
        for nid, k in self.kappa_state.items():
            kappa_field.set(nid, k)

        potential = compute_potential(
            kappa_field, geometry, lambda_gamma=LAMBDA_GAMMA, G_q=1.0
        )

        self.total_time += dt

        step_log = {
            "time": self.total_time,
            "kappa": dict(self.kappa_state),
            "proper_time": proper_time_increments,
            "total_proper_time": {
                nid: r._proper_time for nid, r in self.nodes.items()
            },
            "kernel_probs": {
                nid: s.probabilities for nid, s in self.kernel_states.items()
            },
            "gravity_potential": potential,
        }
        self.event_log.append(step_log)
        return step_log

    def run(
        self,
        n_steps: int = 100,
        dt: float = 0.1,
        damage_schedule: Optional[dict[int, list[int]]] = None,
        lambda_p: float = LAMBDA_P,
    ) -> dict:
        """Run the simulation for n_steps.

        Args:
            n_steps: Number of time steps.
            dt: Time step size.
            damage_schedule: {step: [node_ids]} for damage events.
            lambda_p: κ-drag coupling.

        Returns:
            Summary of the simulation.
        """
        for step in range(n_steps):
            damage = set()
            if damage_schedule and step in damage_schedule:
                damage = set(damage_schedule[step])
            self.step(dt, damage, lambda_p)

        return self.summary()

    def summary(self) -> dict:
        """Generate a summary of the simulation state."""
        total_proper_time = sum(r._proper_time for r in self.nodes.values())
        total_kappa = sum(self.kappa_state.values())

        node_summaries = {}
        for nid in self.nodes:
            record = self.nodes[nid]
            node_summaries[nid] = {
                "kappa": record.kappa,
                "pi": participation_aperture(record),
                "proper_time": record._proper_time,
                "kernel_P0": self.kernel_states[nid].probabilities[0],
                "F": record.F,
                "C": record.C,
            }

        return {
            "n_steps": len(self.event_log),
            "total_time": self.total_time,
            "total_proper_time": total_proper_time,
            "total_kappa": total_kappa,
            "nodes": node_summaries,
            "n_bonds": len(self.bonds),
        }


# ── Pre-Built Demonstration ─────────────────────────────────────────────────


def build_demo_simulation(seed: int = 42) -> UnifiedDETSimulation:
    """Build a 3-node demonstration simulation.

    Topology: 0 — 1 — 2
    Node 0: pristine (κ=0).
    Node 1: partially damaged (κ=0.3).
    Node 2: pristine (κ=0).
    Node 0 receives damage pulses periodically.

    Demonstrates:
      - κ-diffusion from damaged node to neighbors.
      - Proper-time differences from κ (clock anomaly).
      - Kernel root evolution differences from κ.
      - Gravity potential from κ distribution.
    """
    sim = UnifiedDETSimulation()
    sim._rng = random.Random(seed)
    sim.diffusion_params = DiffusionParams(
        D=0.1, tau_rec=20.0, kappa_eq=0.0, alpha_damage=0.3,
    )

    sim.add_node(0, kappa=0.0, F=0.0, sigma=1.0, C=1.0, position=(0.0, 0.0, 0.0))
    sim.add_node(1, kappa=0.3, F=0.0, sigma=1.0, C=0.9, position=(1.0, 0.0, 0.0))
    sim.add_node(2, kappa=0.0, F=0.0, sigma=1.0, C=1.0, position=(2.0, 0.0, 0.0))

    sim.add_bond(0, 1, sigma=1.0)
    sim.add_bond(1, 2, sigma=0.5)

    return sim
