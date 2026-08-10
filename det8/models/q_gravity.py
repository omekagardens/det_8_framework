"""
DET 8 q-Gravity Simulation

Models gravitational effects sourced through ρ = q - b (the contrast
between structural history and baseline). This is DET's proposed
gravitational mechanism, distinct from standard energy-momentum
sourcing.

Key predictions:
1. q-recovery reduces gravitational attraction without changing mass/energy.
2. Two objects with identical F (resource/energy) but different q
   exert different gravitational pulls.
3. This is distinguishable from mass loss (ΔF) vs structural recovery (Δq).

Toy model: Newtonian-style pairwise attraction with ρ as source.
F_ij = G_q · ρ_i · ρ_j / r_ij²

Where:
- G_q is the q-gravity coupling constant.
- r_ij is distance (graph distance or coordinate separation).
- ρ_i = q_i - b (may be negative if q_i < b).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional

from det8.models.det8_core import (
    GAMMA_B,
    LAMBDA_GAMMA,
    NodeRecord,
    apply_q_damage,
    apply_q_recovery,
    apply_q_jubilee,
)

# ── Gravitational Constant ──────────────────────────────────────────────────

G_Q = 1.0


# ── κ-Gravity Source ────────────────────────────────────────────────────────


def gravity_source(record: NodeRecord, baseline: float = GAMMA_B) -> float:
    """Compute the gravitational source ρ = γ - γ_b = λ_γ·κ - γ_b."""
    return LAMBDA_GAMMA * record.kappa - baseline


def effective_mass_proxy(record: NodeRecord, baseline: float = GAMMA_B) -> float:
    """The effective gravitational 'mass' from κ alone."""
    rho = gravity_source(record, baseline)
    return max(0.0, rho)


# ── Newtonian q-Gravity ────────────────────────────────────────────────────


@dataclass
class QGravitySystem:
    """A system of nodes with q-gravity interactions.

    Each node has a DET record (with q) and a position in 1D/2D/3D space.
    Gravity acts between all pairs with force ∝ ρ_i · ρ_j / r².
    """

    nodes: dict[int, NodeRecord] = field(default_factory=dict)
    positions: dict[int, tuple[float, ...]] = field(default_factory=dict)
    velocities: dict[int, tuple[float, ...]] = field(default_factory=dict)
    baseline: float = GAMMA_B
    G: float = G_Q
    softening: float = 0.1  # Softening length to avoid singularity at r=0.

    def add_node(
        self,
        node_id: int,
        record: NodeRecord,
        position: tuple[float, ...],
        velocity: Optional[tuple[float, ...]] = None,
    ) -> None:
        self.nodes[node_id] = record
        self.positions[node_id] = position
        dim = len(position)
        self.velocities[node_id] = velocity or tuple(0.0 for _ in range(dim))

    def distance(self, i: int, j: int) -> float:
        """Euclidean distance between nodes i and j."""
        pi = self.positions[i]
        pj = self.positions[j]
        sq = sum((a - b) ** 2 for a, b in zip(pi, pj))
        return math.sqrt(sq + self.softening**2)

    def force_on(self, target: int) -> tuple[float, ...]:
        """Compute the net q-gravitational force on a node.

        F_target = Σ_{j≠target} G · ρ_target · ρ_j / r² · û_{j→target}
        where û is the unit vector from target to j.
        """
        dim = len(self.positions[target])
        force = [0.0] * dim
        rho_target = gravity_source(self.nodes[target], self.baseline)

        for j in self.nodes:
            if j == target:
                continue
            rho_j = gravity_source(self.nodes[j], self.baseline)
            r = self.distance(target, j)

            if r < 1e-12:
                continue

            # Force magnitude: G · ρ_i · ρ_j / r².
            f_mag = self.G * rho_target * rho_j / (r * r)

            # Direction: unit vector from target to j.
            pt = self.positions[target]
            pj = self.positions[j]
            for d in range(dim):
                dir_d = (pj[d] - pt[d]) / r
                force[d] += f_mag * dir_d

        return tuple(force)

    def step(
        self,
        dt: float = 0.01,
    ) -> dict:
        """Evolve the system by one time step using simple Euler integration.

        Returns summary of the step.
        """
        dim = len(next(iter(self.positions.values())))

        # Compute forces.
        forces: dict[int, tuple[float, ...]] = {}
        for nid in self.nodes:
            forces[nid] = self.force_on(nid)

        # Update velocities and positions (Euler).
        for nid in self.nodes:
            vel = list(self.velocities[nid])
            pos = list(self.positions[nid])
            f = forces[nid]
            for d in range(dim):
                vel[d] += f[d] * dt
                pos[d] += vel[d] * dt
            self.velocities[nid] = tuple(vel)
            self.positions[nid] = tuple(pos)

        return {
            "dt": dt,
            "forces": {nid: forces[nid] for nid in forces},
        }

    def total_kinetic_energy(self) -> float:
        """Total kinetic energy (mass proxies = 1 for simplicity)."""
        ke = 0.0
        for nid, vel in self.velocities.items():
            ke += 0.5 * sum(v**2 for v in vel)
        return ke

    def total_potential_energy(self) -> float:
        """Total q-gravitational potential energy.

        U = -G · Σ_{i<j} ρ_i · ρ_j / r_ij
        """
        u = 0.0
        node_ids = list(self.nodes.keys())
        for a in range(len(node_ids)):
            for b in range(a + 1, len(node_ids)):
                i, j = node_ids[a], node_ids[b]
                rho_i = gravity_source(self.nodes[i], self.baseline)
                rho_j = gravity_source(self.nodes[j], self.baseline)
                r = self.distance(i, j)
                u -= self.G * rho_i * rho_j / r
        return u


# ── q-Gravity Decoupling Test ───────────────────────────────────────────────


def q_gravity_decoupling_test(
    q_damaged: float = 0.5,
    baseline: float = 0.0,
    separation: float = 10.0,
) -> dict:
    """Test the q-gravity decoupling prediction.

    Scenario:
    - Two identical objects (same F, σ, etc.) at fixed separation.
    - Object A: q = 0.3 (some structural history).
    - Object B: q = q_damaged (structurally constrained).

    DET predicts: gravitational attraction between A and B is
    proportional to ρ_A · ρ_B.

    After q-recovery on B (q_damaged → 0):
    - Standard physics (energy-momentum): no change in gravity.
    - DET: gravitational attraction WEAKENS (ρ_B → 0).

    This is the risky prediction: gravity changes without mass change.
    """
    sys = QGravitySystem(baseline=baseline, G=1.0)

    # Two nodes at fixed positions. Both have non-zero q for measurable force.
    sys.add_node(0, NodeRecord(kappa=0.3, F=10.0), position=(0.0,))
    sys.add_node(1, NodeRecord(kappa=q_damaged, F=10.0), position=(separation,))

    rho_a = gravity_source(sys.nodes[0], baseline)
    rho_b_before = gravity_source(sys.nodes[1], baseline)
    force_before = sys.force_on(0)[0]  # Force on A from B.

    # Recovery: reduce q on B.
    apply_q_recovery(sys.nodes[1], q_damaged)  # q_damaged → 0.
    rho_b_after = gravity_source(sys.nodes[1], baseline)
    force_after = sys.force_on(0)[0]

    # Standard mass proxy (F) unchanged.
    F_unchanged = sys.nodes[1].F == 10.0

    return {
        "rho_a": rho_a,
        "rho_b_before": rho_b_before,
        "rho_b_after": rho_b_after,
        "force_before": force_before,
        "force_after": force_after,
        "force_ratio": force_after / force_before if abs(force_before) > 1e-12 else float("inf"),
        "F_unchanged": F_unchanged,
        "gravity_weakened": abs(force_after) < abs(force_before) if abs(force_before) > 1e-12 else False,
        "decoupling_demonstrated": (
            F_unchanged
            and abs(force_after) < abs(force_before)
            if abs(force_before) > 1e-12
            else False
        ),
    }


# ── Two-Body Orbit Simulation ───────────────────────────────────────────────


def two_body_orbit(
    q_a: float = 0.1,
    q_b: float = 0.1,
    n_steps: int = 1000,
    dt: float = 0.01,
    separation: float = 10.0,
) -> dict:
    """Simulate a two-body q-gravity orbit.

    Two nodes with initial tangential velocities orbit each other
    under q-gravity. Tracks whether the orbit is stable.

    Returns orbital parameters.
    """
    sys = QGravitySystem(baseline=0.0, G=1.0, softening=0.5)

    # Place nodes symmetrically about origin with tangential velocities.
    half = separation / 2.0

    # For a circular orbit: v²/r = G·ρ_a·ρ_b/r² → v = sqrt(G·ρ_a·ρ_b/r).
    rho_a = q_a  # baseline = 0
    rho_b = q_b
    v_circular = math.sqrt(sys.G * rho_a * rho_b / separation)

    sys.add_node(
        0,
        NodeRecord(kappa=q_a, F=0.0),
        position=(-half, 0.0),
        velocity=(0.0, v_circular / 2.0),
    )
    sys.add_node(
        1,
        NodeRecord(kappa=q_b, F=0.0),
        position=(half, 0.0),
        velocity=(0.0, -v_circular / 2.0),
    )

    positions_history: list[dict[int, tuple[float, float]]] = []

    for _ in range(n_steps):
        sys.step(dt)
        positions_history.append(
            {nid: (sys.positions[nid][0], sys.positions[nid][1]) for nid in sys.nodes}
        )

    # Compute final separation.
    final_positions = positions_history[-1]
    final_sep = math.sqrt(
        (final_positions[0][0] - final_positions[1][0]) ** 2
        + (final_positions[0][1] - final_positions[1][1]) ** 2
    )

    # Check if orbit stayed bounded (didn't fly apart or collapse).
    initial_sep = separation
    sep_ratio = final_sep / initial_sep
    bounded = 0.5 < sep_ratio < 2.0

    return {
        "n_steps": n_steps,
        "dt": dt,
        "initial_separation": initial_sep,
        "final_separation": final_sep,
        "separation_ratio": sep_ratio,
        "bounded": bounded,
        "v_circular": v_circular,
        "total_energy": sys.total_kinetic_energy() + sys.total_potential_energy(),
    }


# ── q vs F Distinguishability Test ──────────────────────────────────────────


def q_vs_F_distinguishability() -> dict:
    """Demonstrate that q and F have different gravitational signatures.

    Scenario:
    - Pair 1: (q=0.5, F=0) — gravity from q only.
    - Pair 2: (q=0, F=10) — no q-gravity, but has resource/energy.

    In standard physics, pair 2 would have gravity (energy-momentum).
    In DET, pair 1 has q-gravity and pair 2 does not (ρ=0 for both).

    If standard gravity and q-gravity coexist, they must be distinguished.
    """
    baseline = 0.0
    sep = 10.0

    # Pair 1: q-gravity only.
    sys1 = QGravitySystem(baseline=baseline, G=1.0)
    sys1.add_node(0, NodeRecord(kappa=0.5, F=0.0), position=(0.0,))
    sys1.add_node(1, NodeRecord(kappa=0.5, F=0.0), position=(sep,))
    force_q = sys1.force_on(0)[0]

    # Pair 2: F only (no q-gravity since q=0 → ρ=0).
    sys2 = QGravitySystem(baseline=baseline, G=1.0)
    sys2.add_node(0, NodeRecord(kappa=0.0, F=10.0), position=(0.0,))
    sys2.add_node(1, NodeRecord(kappa=0.0, F=10.0), position=(sep,))
    force_F = sys2.force_on(0)[0]

    return {
        "force_q_gravity": force_q,
        "force_F_only": force_F,
        "q_gravity_active": abs(force_q) > 1e-12,
        "F_no_q_gravity": abs(force_F) < 1e-12,
        "distinguishable": abs(force_q - force_F) > 1e-12,
    }
