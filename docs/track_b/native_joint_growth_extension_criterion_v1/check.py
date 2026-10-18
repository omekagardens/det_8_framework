#!/usr/bin/env python3
"""RI-38: exact proper-slot ratio graph for extending the RI-36 prefix.

Standalone standard-library corroboration, bounded to new parent size four.
The prefix formulas and small enumeration helpers are re-expressed from the
accepted RI-36 EXTENSION.md/check.py; neither source is imported or modified.
Numerical fixtures are not an all-parameter or all-size theorem.
"""

from collections import deque
from dataclasses import dataclass
from fractions import Fraction as F
from functools import cache
from itertools import combinations, permutations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Parameters:
    name: str
    a: F
    c: F
    d: F
    f0: F
    f1: F

    def __post_init__(self):
        require(all(type(x) is F for x in (self.a, self.c, self.d, self.f0, self.f1)),
                "nonexact parameter")
        require(0 < self.a < 1 and self.c > 0 and self.d > 0 and self.k > 0,
                "inadmissible strict parameters")
        require(all(0 < x < 1 - self.c for x in (self.f0, self.f1)),
                "inadmissible chain parameters")

    def f(self, bit):
        return (self.f0, self.f1)[bit]

    def h(self, bit):
        return 1 - self.c - self.f(bit)

    @property
    def g(self):
        return (1 - self.a) * self.c / self.a

    @property
    def k(self):
        return 1 - self.d - 2 * self.g

    @property
    def epsilon(self):
        bound = max(F(1), self.g / self.d, self.k / self.d, self.k / self.g,
                    self.f0 / self.c, self.f1 / self.c,
                    self.h(0) / self.c, self.h(1) / self.c,
                    self.h(0) / self.f0, self.h(1) / self.f1)
        return 1 / (8 * bound)


@cache
def subsets(n):
    return tuple(frozenset(v for v in range(n) if mask & (1 << v))
                 for mask in range(1 << n))


@cache
def records(n):
    return tuple(product((0, 1), repeat=n))


def closure(n, edges):
    result = set(edges)
    for middle in range(n):
        for left in range(n):
            for right in range(n):
                if (left, middle) in result and (middle, right) in result:
                    result.add((left, right))
    return frozenset(result)


@cache
def parents(n):
    require(0 <= n <= 4, "explicit size-four enumeration cap")
    possible = tuple(combinations(range(n), 2))
    result = {closure(n, (possible[i] for i in range(len(possible))
                          if mask & (1 << i)))
              for mask in range(1 << len(possible))}
    return tuple(sorted(result, key=lambda edges: tuple(sorted(edges))))


@cache
def ideals(n, edges):
    return tuple(part for part in subsets(n)
                 if all(v not in part or u in part for u, v in edges))


@cache
def prefix_row(p, n, edges, record):
    require(n <= 3 and len(record) == n, "prefix row outside declared domain")
    empty, full = frozenset(), frozenset(range(n))
    if n == 0:
        return {empty: F(1)}
    if n == 1:
        return {empty: p.a, full: 1 - p.a}
    if n == 2:
        if edges:
            root = next(iter(edges))[0]
            return {empty: p.c, frozenset((root,)): p.f(record[root]),
                    full: p.h(record[root])}
        return {empty: p.d, frozenset((0,)): p.g,
                frozenset((1,)): p.g, full: p.k}
    e = p.epsilon
    row = {part: e for part in ideals(n, edges) if part != full}
    if not edges:
        for part in row:
            if len(part) == 1:
                row[part] = e * p.g / p.d
            elif len(part) == 2:
                row[part] = e * p.k / p.d
    elif len(edges) == 1:
        root, tip = next(iter(edges))
        isolated = next(v for v in range(n) if v not in (root, tip))
        row[frozenset((root,))] = e * p.f(record[root]) / p.c
        row[frozenset((root, tip))] = e * p.h(record[root]) / p.c
        row[frozenset((root, isolated))] = e * p.k / p.g
    elif len(edges) == 2:
        roots = [v for v in range(n) if sum(u == v for u, _ in edges) == 2]
        if roots:
            for part in row:
                if len(part) == 2:
                    row[part] = e * p.h(record[roots[0]]) / p.f(record[roots[0]])
    row[full] = 1 - sum(row.values(), F(0))
    require(set(row) == set(ideals(n, edges)), "prefix slot envelope changed")
    return row


def moved(n, edges, record, part, permutation):
    output_record = [None] * n
    for old, new in enumerate(permutation):
        output_record[new] = record[old]
    return (frozenset((permutation[u], permutation[v]) for u, v in edges),
            tuple(output_record), frozenset(permutation[v] for v in part))


def append(n, edges, record, part, bit):
    require(part in ideals(n, edges), "precursor not an old-parent ideal")
    return edges | frozenset((v, n) for v in part), record + (bit,)


@cache
def canonical_local_key(n, edges, part, inside_record):
    """Preserve ALL order; erase only marks outside this proper precursor."""
    require(len(part) < n and part in ideals(n, edges), "not a proper-ideal node")
    require(len(inside_record) == len(part), "incomplete precursor record")
    marked = dict(zip(sorted(part), inside_record))
    keys = []
    for permutation in permutations(range(n)):
        edge_mask = sum(1 << (n * permutation[u] + permutation[v]) for u, v in edges)
        ideal_mask = sum(1 << permutation[v] for v in part)
        record_mask = sum(1 << permutation[v] for v in part if marked[v])
        keys.append((edge_mask, ideal_mask, record_mask))
    return min(keys)


def node(n, edges, record, part):
    return canonical_local_key(n, edges, part, tuple(record[v] for v in sorted(part)))


def node_universe(n):
    nodes = set()
    raw_local_slots = 0
    for edges in parents(n):
        for part in ideals(n, edges):
            if len(part) == n:
                continue
            for inside_record in records(len(part)):
                raw_local_slots += 1
                nodes.add(canonical_local_key(n, edges, part, inside_record))
    return nodes, raw_local_slots


@dataclass(frozen=True)
class RawEdge:
    base: frozenset
    record: tuple
    first: frozenset
    second: frozenset
    first_bit: int
    second_bit: int
    source: tuple
    target: tuple
    gain: F


def raw_edges(p, n):
    result = []
    for base in parents(n - 1):
        for record in records(n - 1):
            old_row = prefix_row(p, n - 1, base, record)
            for first, second in product(ideals(n - 1, base), repeat=2):
                for first_bit, second_bit in product((0, 1), repeat=2):
                    left = append(n - 1, base, record, first, first_bit)
                    right = append(n - 1, base, record, second, second_bit)
                    left_terminal = append(n, *left, second, second_bit)
                    right_terminal = append(n, *right, first, first_bit)
                    exchange = tuple(range(n - 1)) + (n, n - 1)
                    transported = moved(n + 1, *right_terminal, frozenset(), exchange)
                    require(left_terminal == transported[:2],
                            "complete terminal order/record transport failed")
                    result.append(RawEdge(base, record, first, second, first_bit,
                                          second_bit, node(n, *left, second),
                                          node(n, *right, first),
                                          old_row[first] / old_row[second]))
    return result


PAYLOAD = ((F(1, 2), F(0)), (F(0), F(1, 4)),
           (F(0), F(-1, 4)), (F(1, 2), F(0)))


def scale(coefficient, payload):
    return tuple((coefficient * real, coefficient * imaginary)
                 for real, imaginary in payload)


@cache
def deletion_potential(p, n, edges, record, part):
    """Alternating product over nonempty deletions from Max(P) outside S."""
    require(n == 4 and len(part) < n, "potential check is capped at new size four")
    outside_maxima = tuple(v for v in range(n)
                          if v not in part and not any(u == v for u, _ in edges))
    require(outside_maxima, "a proper finite ideal must omit a maximal vertex")
    value = F(1)
    for deletion_size in range(1, len(outside_maxima) + 1):
        for deleted in combinations(outside_maxima, deletion_size):
            surviving = tuple(v for v in range(n) if v not in deleted)
            new_index = {old: new for new, old in enumerate(surviving)}
            induced_order = frozenset((new_index[u], new_index[v])
                                      for u, v in edges
                                      if u in new_index and v in new_index)
            induced_record = tuple(record[v] for v in surviving)
            induced_part = frozenset(new_index[v] for v in part)
            factor = prefix_row(p, len(surviving), induced_order,
                                induced_record)[induced_part]
            require(factor > 0, "deletion potential divided by a nonpositive prefix slot")
            value = value * factor if deletion_size % 2 else value / factor
    return value


@cache
def potential_row(p, n, edges, record):
    return {part: deletion_potential(p, n, edges, record, part)
            for part in ideals(n, edges) if len(part) < n}


@cache
def extension_row(p, n, edges, record, fixed_scale):
    row = {part: fixed_scale * value
           for part, value in potential_row(p, n, edges, record).items()}
    row[frozenset(range(n))] = 1 - sum(row.values(), F(0))
    return row


def validate_extension(p, nodes, edges):
    n = 4
    quotient_values = {}
    max_row_sum = F(0)
    proper_occurrences = 0
    for relation in parents(n):
        for record in records(n):
            unscaled = potential_row(p, n, relation, record)
            # Sum DISTINCT LABELED ideals, not distinct quotient nodes.
            max_row_sum = max(max_row_sum, sum(unscaled.values(), F(0)))
            for part, value in unscaled.items():
                proper_occurrences += 1
                require(value > 0, "potential is not strictly positive")
                key = node(n, relation, record, part)
                if key in quotient_values:
                    require(value == quotient_values[key],
                            "potential does not descend to the strict-local/equivariant quotient")
                else:
                    quotient_values[key] = value
    require(set(quotient_values) == nodes, "candidate potential omitted a proper-slot class")
    # This constant is chosen from the entire fixed layer table in advance.
    # It is never re-estimated from a current parent's records.
    fixed_scale = 1 / (2 * (1 + max_row_sum))
    rows = slots = locality = equivariance = full_payload = 0
    for relation in parents(n):
        for record in records(n):
            row = extension_row(p, n, relation, record, fixed_scale)
            rows += 1
            require(sum(row.values(), F(0)) == 1 and all(q > 0 for q in row.values()),
                    "new row normalization/strict positivity failed")
            require(row[frozenset(range(n))] > F(1, 2), "full-ideal half-mass bound failed")
            for part, q in row.items():
                slots += 1
                for other in records(n):
                    if all(record[v] == other[v] for v in part):
                        locality += 1
                        require(q == extension_row(p, n, relation, other, fixed_scale)[part],
                                "new strict precursor-record locality failed")
                for permutation in permutations(range(n)):
                    pe, pr, ps = moved(n, relation, record, part, permutation)
                    equivariance += 1
                    require(q == extension_row(p, n, pe, pr, fixed_scale)[ps],
                            "new full marked-parent equivariance failed")
    for edge in edges:
        left_u, right_u = quotient_values[edge.source], quotient_values[edge.target]
        require(right_u == edge.gain * left_u, "maximal-deletion potential fails a raw ratio edge")
        old_row = prefix_row(p, n - 1, edge.base, edge.record)
        left_first, right_first = old_row[edge.first] / 2, old_row[edge.second] / 2
        left_second, right_second = fixed_scale * left_u / 2, fixed_scale * right_u / 2
        require(left_first * left_second == right_first * right_second,
                "new scalar full-map diamond failed")
        require(scale(left_second, scale(left_first, PAYLOAD)) ==
                scale(right_second, scale(right_first, PAYLOAD)),
                "new exact complex-payload diamond failed")
        full_payload += 1
    require(rows == 640 and full_payload == 7616, "new layer coverage changed")
    return (rows, slots, locality, equivariance, proper_occurrences,
            full_payload, fixed_scale)


def validate_prefix(p):
    rows = slots = locality = equivariance = diamonds = all_zero = 0
    for n in range(4):
        for edges in parents(n):
            for record in records(n):
                row = prefix_row(p, n, edges, record)
                rows += 1
                require(sum(row.values(), F(0)) == 1 and all(q > 0 for q in row.values()),
                        "prefix strict row failure")
                for part, q in row.items():
                    slots += 1
                    for other in records(n):
                        if all(record[v] == other[v] for v in part):
                            locality += 1
                            require(q == prefix_row(p, n, edges, other)[part],
                                    "prefix locality failure")
                    for permutation in permutations(range(n)):
                        pe, pr, ps = moved(n, edges, record, part, permutation)
                        equivariance += 1
                        require(q == prefix_row(p, n, pe, pr)[ps],
                                "prefix equivariance failure")
    for n in range(1, 4):
        for edge in raw_edges(p, n):
            old = prefix_row(p, n - 1, edge.base, edge.record)
            left = append(n - 1, edge.base, edge.record, edge.first, edge.first_bit)
            right = append(n - 1, edge.base, edge.record, edge.second, edge.second_bit)
            l1, r1 = old[edge.first] / 2, old[edge.second] / 2
            l2 = prefix_row(p, n, *left)[edge.second] / 2
            r2 = prefix_row(p, n, *right)[edge.first] / 2
            require(l1 * l2 == r1 * r2, "prefix scalar/full-map diamond failure")
            require(scale(l2, scale(l1, PAYLOAD)) == scale(r2, scale(r1, PAYLOAD)),
                    "prefix complex payload failure")
            diamonds += 1
            all_zero += int(not any(edge.record) and edge.first_bit == edge.second_bit == 0)
    require((rows, slots, locality, equivariance, diamonds, all_zero) ==
            (67, 353, 1199, 1981, 436, 30), "prefix coverage changed")
    return rows, slots, locality, equivariance, diamonds, all_zero


def cycle_from_conflict(source, target, edge_index, direction, tree):
    def path(vertex):
        reversed_path = []
        while tree[vertex] is not None:
            previous, index, orientation = tree[vertex]
            reversed_path.append((previous, vertex, index, orientation))
            vertex = previous
        return list(reversed(reversed_path))

    left, right = path(source), path(target)
    common = 0
    while common < min(len(left), len(right)) and left[common] == right[common]:
        common += 1
    return (left[common:] + [(source, target, edge_index, direction)] +
            [(v, u, index, -orientation)
             for u, v, index, orientation in reversed(right[common:])])


def ratio_graph(nodes, edges):
    adjacency = {key: [] for key in nodes}  # Retain even isolated proper-slot classes.
    for index, edge in enumerate(edges):
        require(edge.source in nodes and edge.target in nodes, "edge node missing from universe")
        adjacency[edge.source].append((edge.target, edge.gain, index, 1))
        adjacency[edge.target].append((edge.source, 1 / edge.gain, index, -1))
    potential, tree = {}, {}
    components = conflicts = 0
    witness = None
    for root in sorted(nodes):
        if root in potential:
            continue
        components += 1
        potential[root], tree[root] = F(1), None
        queue = deque((root,))
        while queue:
            source = queue.popleft()
            for target, gain, index, direction in adjacency[source]:
                proposed = gain * potential[source]
                if target not in potential:
                    potential[target] = proposed
                    tree[target] = (source, index, direction)
                    queue.append(target)
                elif potential[target] != proposed:
                    conflicts += 1
                    if witness is None:
                        witness = cycle_from_conflict(source, target, index, direction, tree)
    require(len(potential) == len(nodes), "isolated node was omitted")
    if witness is not None:
        require(witness[0][0] == witness[-1][1], "witness is not closed")
        gain_product = F(1)
        for step, (source, target, index, direction) in enumerate(witness):
            edge = edges[index]
            if direction == 1:
                require((source, target) == (edge.source, edge.target), "forward witness mismatch")
                gain_product *= edge.gain
            else:
                require((source, target) == (edge.target, edge.source), "reverse witness mismatch")
                gain_product /= edge.gain
            require(target == witness[(step + 1) % len(witness)][0], "disconnected witness")
        require(gain_product != 1, "reported cycle is consistent")
    else:
        gain_product = F(1)
    return components, sum(not neighbors for neighbors in adjacency.values()), conflicts, witness, gain_product


def print_witness(edges, witness, gain_product):
    print(f"  cycle_length={len(witness)} cycle_gain={gain_product} (required 1)")
    for number, (source, target, index, direction) in enumerate(witness, 1):
        edge = edges[index]
        gain = edge.gain if direction == 1 else 1 / edge.gain
        print(f"  step={number} raw_edge={index} orientation={direction:+d} gain={gain} "
              f"node={source}->{target}")
        print(f"    C={tuple(sorted(edge.base))} R={edge.record} "
              f"S={tuple(sorted(edge.first))} T={tuple(sorted(edge.second))} "
              f"b={edge.first_bit} h={edge.second_bit}")


def check_detector_controls():
    # Pure graph tests, not purported valid stochastic prefixes or countermodels.
    v0, v1, v2, isolated = ((0, i, 0) for i in range(4))

    def edge(source, target, gain):
        return RawEdge(frozenset(), (), frozenset(), frozenset(),
                       0, 0, source, target, gain)

    vertices = {v0, v1, v2, isolated}
    consistent = [edge(v0, v1, F(2)), edge(v1, v2, F(3)),
                  edge(v2, v0, F(1, 6)), edge(v0, v0, F(1)),
                  edge(v0, v1, F(2))]  # Keep both a loop and a parallel edge.
    result = ratio_graph(vertices, consistent)
    require(result[:3] == (2, 1, 0) and result[3] is None,
            "consistent graph/isolated-node control failed")
    inconsistent = consistent[:]
    inconsistent[2] = edge(v2, v0, F(1, 5))
    result = ratio_graph(vertices, inconsistent)
    require(result[2] > 0 and len(result[3]) == 3 and result[4] != 1,
            "nontrivial cycle detector failed")
    loop_result = ratio_graph({v0}, [edge(v0, v0, F(2))])
    require(loop_result[2] > 0 and len(loop_result[3]) == 1,
            "inconsistent self-loop detector failed")
    parallel_result = ratio_graph({v0, v1}, [edge(v0, v1, F(2)), edge(v0, v1, F(3))])
    require(parallel_result[2] > 0 and len(parallel_result[3]) == 2,
            "inconsistent parallel-edge/reverse-traversal detector failed")

    relation = frozenset(((0, 1),))
    precursor = frozenset((0,))
    reference = node(4, relation, (0, 0, 0, 0), precursor)
    require(reference == node(4, relation, (0, 1, 1, 1), precursor),
            "outside-precursor records were not erased")
    require(reference != node(4, relation, (1, 0, 0, 0), precursor),
            "inside-precursor record was erased")
    require(reference != node(4, relation, (0, 0, 0, 0), frozenset((2,))),
            "distinct structural precursor roles were erased")
    extra_order = frozenset(((0, 1), (0, 2), (1, 2)))
    require(node(4, relation, (0, 0, 0, 0), frozenset()) !=
            node(4, extra_order, (0, 0, 0, 0), frozenset()),
            "order outside an empty precursor was erased")
    for permutation in permutations(range(4)):
        moved_edges, moved_record, moved_part = moved(
            4, relation, (1, 0, 1, 0), precursor, permutation)
        require(node(4, relation, (1, 0, 1, 0), precursor) ==
                node(4, moved_edges, moved_record, moved_part),
                "canonical quotient is not equivariant")
    print("controls: isolated node, parallel edges, consistent cycle, inconsistent "
          "cycle/self-loop, and exact locality/equivariance quotient; PASS")


def main():
    require(tuple(len(parents(n)) for n in range(5)) == (1, 1, 2, 7, 40),
            "independent natural-poset closure enumeration failed")
    check_detector_controls()
    fixtures = (
        Parameters("interior_a", F(2, 3), F(1, 5), F(1, 4), F(1, 6), F(1, 3)),
        Parameters("interior_b", F(1, 2), F(1, 5), F(1, 5), F(1, 5), F(2, 5)),
        Parameters("small_a_f0", F(1, 10), F(1, 100), F(1, 100), F(1, 1000), F(49, 50)),
        Parameters("large_a_small_h1", F(99, 100), F(1, 4), F(1, 3), F(1, 100), F(37, 50)),
    )
    nodes, raw_slots = node_universe(4)
    print(f"n=4 natural_parents=40 raw_local_proper_slots={raw_slots} quotient_nodes={len(nodes)}")
    for p in fixtures:
        counts = validate_prefix(p)
        print(f"{p.name}: valid_prefix rows={counts[0]} slots={counts[1]} "
              f"locality={counts[2]} equivariance={counts[3]} "
              f"diamonds={counts[4]} all_zero={counts[5]}")
        edges = raw_edges(p, 4)
        zero_count = sum(not any(e.record) and e.first_bit == e.second_bit == 0 for e in edges)
        equal_count = sum(e.first == e.second for e in edges)
        require((len(edges), zero_count, equal_count) == (7616, 238, 1280),
                "new raw diamond coverage changed")
        components, isolates, conflicts, witness, gain_product = ratio_graph(nodes, edges)
        print(f"  raw_edges={len(edges)} all_zero={zero_count} equal_precursor={equal_count} "
              f"loops={sum(e.source == e.target for e in edges)} "
              f"components={components} isolates={isolates} "
              f"directed_potential_conflicts={conflicts}")
        if witness is not None:
            print_witness(edges, witness, gain_product)
            print("  RESULT: this fixed valid prefix has no strictly positive n=4 extension")
        else:
            print("  RESULT: n=4 ratio constraints consistent for this fixture only")
        extension = validate_extension(p, nodes, edges)
        print(f"  deletion_potential: rows={extension[0]} slots={extension[1]} "
              f"locality={extension[2]} equivariance={extension[3]} "
              f"proper_occurrences={extension[4]} full_payload={extension[5]} "
              f"fixed_scale={extension[6]}; PASS")
    print("DONE: finite exact fixture results only; no all-size or physical claim")


if __name__ == "__main__":
    main()
