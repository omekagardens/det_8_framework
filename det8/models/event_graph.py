"""
DET 8 Causal Event Graph

Implements the event graph G = (V, ≺) from the formal core:
- V: locally finite set of events.
- ≺: causal partial order (irreflexive, transitive, antisymmetric).
- Spacelike separation: e1 ∥ e2 iff neither precedes the other.
- Causal past: J⁻(e) = {e' : e' ≺ e}.
- Causal future: J⁺(e) = {e' : e ≺ e'}.

Also implements event domains D_e (finite declared regions)
and causal-past record computation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Set


# ── Event ───────────────────────────────────────────────────────────────────


@dataclass(frozen=True)
class Event:
    """A local event in the causal graph.

    Each event has a unique ID and a declared domain D_e.
    """

    event_id: int
    domain_node_ids: tuple[int, ...]  # The nodes involved in this event.

    def __hash__(self) -> int:
        return hash(self.event_id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Event):
            return False
        return self.event_id == other.event_id


# ── Causal Graph ────────────────────────────────────────────────────────────


@dataclass
class CausalGraph:
    """A directed acyclic graph representing the causal partial order ≺.

    edges[a][b] = True means a ≺ b (a causally precedes b).

    Maintains:
    - Transitive closure for efficient causal-past queries.
    - Spacelike separation detection.
    """

    events: dict[int, Event] = field(default_factory=dict)
    _edges: dict[int, set[int]] = field(default_factory=dict)  # Direct edges.
    _transitive_closure: Optional[dict[int, set[int]]] = field(
        default=None, repr=False
    )

    def add_event(self, event: Event) -> None:
        """Add an event to the graph."""
        self.events[event.event_id] = event
        if event.event_id not in self._edges:
            self._edges[event.event_id] = set()
        self._transitive_closure = None  # Invalidate cache.

    def add_edge(self, from_id: int, to_id: int) -> None:
        """Declare that event from_id causally precedes event to_id.

        This must not create a cycle (will be checked).
        """
        if from_id not in self._edges:
            self._edges[from_id] = set()
        self._edges[from_id].add(to_id)

        if to_id not in self._edges:
            self._edges[to_id] = set()

        self._transitive_closure = None  # Invalidate cache.

        # Check for cycles.
        if self._has_cycle():
            self._edges[from_id].discard(to_id)
            self._transitive_closure = None
            raise ValueError(
                f"Adding edge {from_id} → {to_id} would create a cycle"
            )

    def _has_cycle(self) -> bool:
        """Check if the graph has a cycle using DFS."""
        closure = self._compute_closure()
        for v in self._edges:
            if v in closure.get(v, set()):
                return True
        return False

    def _compute_closure(self) -> dict[int, set[int]]:
        """Compute the transitive closure (Floyd-Warshall for small graphs)."""
        if self._transitive_closure is not None:
            return self._transitive_closure

        nodes = list(self._edges.keys())
        closure: dict[int, set[int]] = {n: set() for n in nodes}

        # Direct edges.
        for u in nodes:
            for v in self._edges.get(u, set()):
                closure[u].add(v)

        # Floyd-Warshall.
        for k in nodes:
            for i in nodes:
                if k in closure.get(i, set()):
                    for j in closure.get(k, set()):
                        closure[i].add(j)

        self._transitive_closure = closure
        return closure

    def precedes(self, a: int, b: int) -> bool:
        """Check if event a causally precedes event b (a ≺ b)."""
        closure = self._compute_closure()
        return b in closure.get(a, set())

    def causal_past(self, event_id: int) -> set[int]:
        """J⁻(e) = {e' : e' ≺ e}."""
        closure = self._compute_closure()
        result = set()
        for u, targets in closure.items():
            if event_id in targets:
                result.add(u)
        return result

    def causal_future(self, event_id: int) -> set[int]:
        """J⁺(e) = {e' : e ≺ e'}."""
        closure = self._compute_closure()
        return closure.get(event_id, set()).copy()

    def is_spacelike(self, a: int, b: int) -> bool:
        """Check if events a and b are spacelike-separated.

        a ∥ b iff neither a ≺ b nor b ≺ a, and a ≠ b.
        """
        if a == b:
            return False
        return not self.precedes(a, b) and not self.precedes(b, a)

    def spacelike_pairs(self) -> list[tuple[int, int]]:
        """List all spacelike-separated event pairs."""
        pairs = []
        event_ids = list(self.events.keys())
        for i in range(len(event_ids)):
            for j in range(i + 1, len(event_ids)):
                a, b = event_ids[i], event_ids[j]
                if self.is_spacelike(a, b):
                    pairs.append((a, b))
        return pairs

    def is_acyclic(self) -> bool:
        """Check that the graph has no cycles."""
        return not self._has_cycle()

    def topological_order(self) -> list[int]:
        """Return a topological ordering of events (any schedule that respects ≺)."""
        in_degree: dict[int, int] = {eid: 0 for eid in self._edges}
        for u in self._edges:
            for v in self._edges[u]:
                in_degree[v] = in_degree.get(v, 0) + 1

        queue = [eid for eid, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            u = queue.pop(0)
            order.append(u)
            for v in self._edges.get(u, set()):
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(order) != len(self._edges):
            raise ValueError("Graph has a cycle — no topological order exists")

        return order


# ── Causal-Past Record ──────────────────────────────────────────────────────


@dataclass
class CausalPastRecord:
    """The committed causal-past record for an event.

    R⁻_e = R|_{J⁻(D_e)} — the record restricted to the causal past
    of the event's domain.

    In a simulation, this is the snapshot of committed values
    for all nodes that can causally influence the event.
    """

    event_id: int
    node_records: dict[int, dict] = field(default_factory=dict)
    bond_records: dict[tuple[int, int], dict] = field(default_factory=dict)

    def get_node_value(self, node_id: int, key: str, default=0.0) -> float:
        """Get a specific record variable for a node."""
        return self.node_records.get(node_id, {}).get(key, default)

    def get_bond_value(
        self, i: int, j: int, key: str, default=0.0
    ) -> float:
        """Get a specific record variable for a bond."""
        k = (i, j) if i < j else (j, i)
        return self.bond_records.get(k, {}).get(key, default)


# ── Event Scheduler with Causal Order ───────────────────────────────────────


@dataclass
class CausalScheduler:
    """Schedules events respecting the causal partial order.

    Only executes events whose causal-past events have all been committed.
    This enforces: no event may consult an uncommitted future outcome.
    """

    graph: CausalGraph = field(default_factory=CausalGraph)
    committed: set[int] = field(default_factory=set)  # Events already executed.
    node_states: dict[int, dict] = field(default_factory=dict)

    def is_executable(self, event_id: int) -> bool:
        """An event is executable iff all its causal-past events are committed."""
        past = self.graph.causal_past(event_id)
        return past.issubset(self.committed)

    def executable_events(self) -> list[int]:
        """List all events that are currently executable."""
        return [
            eid
            for eid in self.graph.events
            if eid not in self.committed and self.is_executable(eid)
        ]

    def mark_committed(self, event_id: int) -> None:
        """Mark an event as committed (executed)."""
        self.committed.add(event_id)

    def is_complete(self) -> bool:
        """Check if all events have been committed."""
        return self.committed == set(self.graph.events.keys())

    def schedule_all(self) -> list[list[int]]:
        """Generate all valid topological schedules.

        At each step, any executable event may be chosen.
        Returns all possible linear extensions (complete orders).
        For large graphs, this may be exponential — use with caution.
        """
        all_schedules: list[list[int]] = []

        def backtrack(schedule: list[int]) -> None:
            if self.is_complete():
                all_schedules.append(schedule.copy())
                return

            executable = self.executable_events()
            for eid in executable:
                self.mark_committed(eid)
                schedule.append(eid)
                backtrack(schedule)
                schedule.pop()
                self.committed.discard(eid)

        backtrack([])
        return all_schedules
