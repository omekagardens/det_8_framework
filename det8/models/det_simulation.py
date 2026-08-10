"""
DET 8 Integrated Simulation — Multi-Node System with Bonds and Proper Time

Unifies the DET 8 physical core (node records, Π, q-dynamics),
bond network (flux, conductivity, momentum), and causal event graph
into a single simulation framework.

The simulation cycle:
  1. Causal scheduler determines which events are executable.
  2. For each event, the law map generates Ω from the causal-past record.
  3. An actualizer selects one successor.
  4. The commit map writes the outcome to node/bond records.
  5. Proper time is accumulated via Π for each participating node.
  6. Conservation invariants are verified.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Optional

from det8.models.det8_core import (
    LAMBDA_P,
    NodeRecord,
    accumulate_proper_time,
    apply_q_damage,
    participation_aperture,
)
from det8.models.bonds import (
    BondNetwork,
    BondRecord,
    apply_bond_flux,
    generate_bond_flux_possibilities,
    verify_network_conservation,
)
from det8.models.event_graph import CausalGraph, CausalScheduler, Event


# ── Integrated DET System ──────────────────────────────────────────────────


@dataclass
class DetUniverse:
    """A complete DET 8 simulation universe.

    Contains:
    - Node records with full DET physics (q, Π, proper time).
    - A bond network connecting nodes.
    - A causal event graph defining allowed event sequences.
    - A resource field per node (for flux conservation).
    - An event log for post-hoc analysis.
    """

    nodes: dict[int, NodeRecord] = field(default_factory=dict)
    resources: dict[int, float] = field(default_factory=dict)
    bonds: BondNetwork = field(default_factory=BondNetwork)
    causal_graph: CausalGraph = field(default_factory=CausalGraph)
    scheduler: Optional[CausalScheduler] = None

    # Simulation state.
    current_time_kappa: float = 0.0
    event_log: list[dict] = field(default_factory=list)
    _rng: random.Random = field(default_factory=lambda: random.Random(42))

    def __post_init__(self):
        self.scheduler = CausalScheduler(graph=self.causal_graph)

    def add_node(
        self,
        node_id: int,
        q: float = 0.0,
        sigma: float = 1.0,
        F: float = 0.0,
        H: float = 0.0,
        resource: float = 10.0,
    ) -> None:
        """Add a node with initial DET record."""
        record = NodeRecord(kappa=q, sigma=sigma, F=F, H=H, eta=1.0)
        self.nodes[node_id] = record
        self.resources[node_id] = resource

    def add_bond(
        self,
        i: int,
        j: int,
        sigma: float = 1.0,
        C: float = 1.0,
        pi: float = 0.0,
    ) -> BondRecord:
        """Add a bond between nodes."""
        return self.bonds.add_bond(i, j, sigma=sigma, C=C, pi=pi)

    def add_event(
        self,
        event_id: int,
        domain_nodes: tuple[int, ...],
        predecessors: Optional[list[int]] = None,
    ) -> Event:
        """Add an event to the causal graph."""
        event = Event(event_id=event_id, domain_node_ids=domain_nodes)
        self.causal_graph.add_event(event)

        if predecessors:
            for pred_id in predecessors:
                if pred_id in self.causal_graph.events:
                    self.causal_graph.add_edge(pred_id, event_id)

        return event

    def step(
        self,
        delta_N: float = 1.0,
        lambda_p: float = LAMBDA_P,
        damage_per_event: float = 0.0,
    ) -> list[dict]:
        """Execute one simulation step.

        Finds all executable events, executes them in causal order,
        accumulates proper time, and applies optional q-damage.

        Returns the event log entries for this step.
        """
        if not self.scheduler:
            raise RuntimeError("Scheduler not initialized")

        executable = self.scheduler.executable_events()
        step_log: list[dict] = []

        for eid in executable:
            event = self.causal_graph.events[eid]
            entry = self._execute_event(event, delta_N, lambda_p, damage_per_event)
            step_log.append(entry)
            self.scheduler.mark_committed(eid)

        self.current_time_kappa += delta_N
        self.event_log.extend(step_log)
        return step_log

    def _execute_event(
        self,
        event: Event,
        delta_N: float,
        lambda_p: float,
        damage: float,
    ) -> dict:
        """Execute a single event.

        Currently supports two event types:
        - Single-node: accumulate proper time.
        - Two-node (bond): transfer flux across a bond.
        """
        domain = event.domain_node_ids

        if len(domain) == 1:
            # Single-node event: just accumulate proper time.
            node_id = domain[0]
            record = self.nodes[node_id]
            dtau = accumulate_proper_time(record, delta_N, lambda_p=lambda_p)

            if damage > 0:
                apply_q_damage(record, damage)

            return {
                "event_id": event.event_id,
                "type": "proper_time",
                "node": node_id,
                "delta_tau": dtau,
                "total_tau": record._proper_time,
                "kappa": record.kappa,
                "pi": participation_aperture(record, lambda_p=lambda_p),
            }

        elif len(domain) == 2:
            # Two-node event: bond flux transfer.
            i, j = domain
            bond = self.bonds.get_bond(i, j)
            resource_i = self.resources.get(i, 0.0)
            resource_j = self.resources.get(j, 0.0)

            # Generate flux possibilities.
            if bond is None:
                # No bond — create a virtual one for the transfer.
                omega = [0.0]
                kernel = [1.0]
            else:
                omega, kernel = generate_bond_flux_possibilities(
                    bond, resource_i, resource_j
                )

            # Actualize: select a flux amount.
            idx = self._rng.choices(range(len(omega)), weights=kernel, k=1)[0]
            flux = omega[idx]

            # Commit: apply the flux.
            new_i, new_j = apply_bond_flux(
                bond or BondRecord(node_i=i, node_j=j),
                resource_i,
                resource_j,
                flux,
            )
            self.resources[i] = new_i
            self.resources[j] = new_j

            # Accumulate proper time for both nodes.
            dtau_i = accumulate_proper_time(
                self.nodes[i], delta_N, lambda_p=lambda_p
            )
            dtau_j = accumulate_proper_time(
                self.nodes[j], delta_N, lambda_p=lambda_p
            )

            # Apply damage.
            if damage > 0:
                apply_q_damage(self.nodes[i], damage)
                apply_q_damage(self.nodes[j], damage)

            return {
                "event_id": event.event_id,
                "type": "bond_flux",
                "nodes": (i, j),
                "flux": flux,
                "omega_size": len(omega),
                "resources_before": (resource_i, resource_j),
                "resources_after": (new_i, new_j),
                "delta_tau": (dtau_i, dtau_j),
                "kappa": (self.nodes[i].kappa, self.nodes[j].kappa),
            }

        else:
            raise ValueError(f"Unsupported event domain size: {len(domain)}")

    def run(
        self,
        n_steps: int = 10,
        delta_N: float = 1.0,
        lambda_p: float = LAMBDA_P,
        damage_per_event: float = 0.0,
    ) -> dict:
        """Run the simulation for n_steps.

        Returns summary statistics.
        """
        for _ in range(n_steps):
            self.step(delta_N, lambda_p, damage_per_event)

        return self.summary()

    def summary(self) -> dict:
        """Generate a summary of the simulation state."""
        total_proper_time = sum(
            r._proper_time for r in self.nodes.values()
        )
        conservation = verify_network_conservation(
            self.resources, self.bonds
        )

        node_summaries = {}
        for nid, record in self.nodes.items():
            node_summaries[nid] = {
                "kappa": record.kappa,
                "pi": participation_aperture(record),
                "proper_time": record._proper_time,
                "resource": self.resources.get(nid, 0.0),
            }

        return {
            "n_steps": self.current_time_kappa,
            "n_events_committed": len(self.scheduler.committed)
            if self.scheduler
            else 0,
            "n_events_total": len(self.causal_graph.events),
            "total_proper_time": total_proper_time,
            "conservation": conservation,
            "nodes": node_summaries,
            "bonds": len(self.bonds),
        }


# ── Pre-Built Example ──────────────────────────────────────────────────────


def build_triangle_universe(
    seed: int = 42,
) -> DetUniverse:
    """Build a 3-node triangle universe with bonds and causal events.

    Topology:
      Node 0 ←→ Node 1 ←→ Node 2 ←→ Node 0

    Causal order (linear chain for simplicity):
      Event 0 (node 0) → Event 1 (bond 0-1) → Event 2 (bond 1-2) → Event 3 (bond 2-0)
    """
    u = DetUniverse()
    u._rng = random.Random(seed)

    # Nodes with different q values.
    u.add_node(0, q=0.0, sigma=1.0, resource=10.0)  # Pristine
    u.add_node(1, q=0.3, sigma=1.0, resource=7.0)   # Damaged
    u.add_node(2, q=0.0, sigma=1.5, resource=3.0)   # High conductivity

    # Bonds.
    u.add_bond(0, 1, sigma=3.0, C=0.9, pi=0.0)
    u.add_bond(1, 2, sigma=2.0, C=0.8, pi=0.0)
    u.add_bond(2, 0, sigma=1.0, C=0.7, pi=0.0)

    # Events: single-node time ticks and bond flux events.
    u.add_event(0, (0,))       # Node 0 proper time tick.
    u.add_event(1, (1,))       # Node 1 proper time tick.
    u.add_event(2, (2,))       # Node 2 proper time tick.
    u.add_event(3, (0, 1))     # Bond flux 0↔1.
    u.add_event(4, (1, 2))     # Bond flux 1↔2.
    u.add_event(5, (2, 0))     # Bond flux 2↔0.

    return u
