#!/usr/bin/env python3
"""RI-41: exact single-layer height normalization for the fixed interior_a seed.

Standalone standard library only. No imports of project source, no writes,
no stochastic simulation, and no rows beyond the specified parent size four.
"""

from fractions import Fraction as F
from functools import cache
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


A, C, D = F(2, 3), F(1, 5), F(1, 4)
FS = (F(1, 6), F(1, 3))
G = (1 - A) * C / A
K = 1 - D - 2 * G
HS = tuple(1 - C - f for f in FS)
SEED_SCALE = 1 / (8 * max(F(1), G / D, K / D, K / G,
                         *(f / C for f in FS), *(h / C for h in HS),
                         *(h / f for h, f in zip(HS, FS))))


@cache
def subsets(n):
    return tuple(frozenset(v for v in range(n) if mask & (1 << v))
                 for mask in range(1 << n))


@cache
def marks(n):
    return tuple(product((0, 1), repeat=n))


@cache
def parents(n):
    require(0 <= n <= 4, "parent enumeration outside size-four bound")
    pairs = tuple(combinations(range(n), 2))
    result = set()
    for mask in range(1 << len(pairs)):
        edges = {pair for i, pair in enumerate(pairs) if mask & (1 << i)}
        for middle in range(n):
            for left in range(n):
                for right in range(n):
                    if (left, middle) in edges and (middle, right) in edges:
                        edges.add((left, right))
        result.add(frozenset(edges))
    return tuple(sorted(result, key=lambda edges: tuple(sorted(edges))))


@cache
def ideals(n, edges):
    return tuple(s for s in subsets(n)
                 if all(v not in s or u in s for u, v in edges))


@cache
def seed(n, edges, record):
    """Re-expressed RI-36 rows, for this one exact RI-38 fixture only."""
    require(0 <= n <= 3 and len(record) == n, "seed outside declared domain")
    empty, full = frozenset(), frozenset(range(n))
    if n == 0:
        return {empty: F(1)}
    if n == 1:
        return {empty: A, full: 1 - A}
    if n == 2:
        if not edges:
            return {empty: D, frozenset((0,)): G, frozenset((1,)): G, full: K}
        root = next(iter(edges))[0]
        return {empty: C, frozenset((root,)): FS[record[root]], full: HS[record[root]]}
    row = {s: SEED_SCALE for s in ideals(n, edges) if s != full}
    if not edges:
        for s in row:
            if len(s) == 1:
                row[s] *= G / D
            elif len(s) == 2:
                row[s] *= K / D
    elif len(edges) == 1:
        root, tip = next(iter(edges))
        isolated = next(v for v in range(n) if v not in (root, tip))
        row[frozenset((root,))] *= FS[record[root]] / C
        row[frozenset((root, tip))] *= HS[record[root]] / C
        row[frozenset((root, isolated))] *= K / G
    elif len(edges) == 2:
        roots = [v for v in range(n) if sum(u == v for u, _ in edges) == 2]
        if roots:
            for s in row:
                if len(s) == 2:
                    row[s] *= HS[record[roots[0]]] / FS[record[roots[0]]]
    row[full] = 1 - sum(row.values(), F(0))
    require(set(row) == set(ideals(n, edges)) and all(x > 0 for x in row.values()),
            "invalid transcribed seed row")
    return row


@cache
def local_key(edges, part, inside):
    """Quotient by whole-order isomorphism; forget only records outside S."""
    record = dict(zip(sorted(part), inside))
    return min((sum(1 << (4 * p[u] + p[v]) for u, v in edges),
                sum(1 << p[v] for v in part),
                sum(1 << p[v] for v in part if record[v]))
               for p in permutations(range(4)))


def node(edges, record, part):
    return local_key(edges, part, tuple(record[v] for v in sorted(part)))


@cache
def potential(edges, record, part):
    maxima = tuple(v for v in range(4)
                   if v not in part and not any(u == v for u, _ in edges))
    require(maxima, "proper ideal omitted no maximal vertex")
    value = F(1)
    for count in range(1, len(maxima) + 1):
        for removed in combinations(maxima, count):
            keep = tuple(v for v in range(4) if v not in removed)
            index = {v: i for i, v in enumerate(keep)}
            order = frozenset((index[u], index[v]) for u, v in edges
                              if u in index and v in index)
            smaller = frozenset(index[v] for v in part)
            q = seed(len(keep), order, tuple(record[v] for v in keep))[smaller]
            value = value * q if count % 2 else value / q
    require(value > 0, "nonpositive potential")
    return value


def height(edges, part):
    longest = {}
    for v in sorted(part):
        longest[v] = 1 + max((longest[u] for u in part if (u, v) in edges), default=0)
    return max(longest.values(), default=0)


def layer():
    require(SEED_SCALE == F(1, 44), "fixed RI-36 scale changed")
    require(tuple(len(parents(n)) for n in range(5)) == (1, 1, 2, 7, 40),
            "natural-parent envelope changed")
    nodes, raw_rows = {}, []
    proper_count = 0
    for edges in parents(4):
        for record in marks(4):
            entries = []
            h = height(edges, frozenset(range(4)))
            for part in ideals(4, edges):
                if len(part) == 4:
                    continue
                key, u = node(edges, record, part), potential(edges, record, part)
                child_edges = edges | frozenset((v, 4) for v in part)
                require(height(child_edges, frozenset(range(5))) ==
                        max(h, height(edges, part) + 1), "height increment identity failed")
                require(key not in nodes or nodes[key] == u, "quotient potential mismatch")
                nodes[key] = u
                entries.append((key, u, height(edges, part) < h))
                proper_count += 1
            raw_rows.append((edges, record, entries))
    adjacency = {key: set() for key in nodes}
    raw_links = []
    edge_count = zero_count = equal_count = loop_count = 0
    for base in parents(3):
        for record in marks(3):
            old = seed(3, base, record)
            for first, second in product(ideals(3, base), repeat=2):
                for b, h in product((0, 1), repeat=2):
                    left = base | frozenset((v, 3) for v in first)
                    right = base | frozenset((v, 3) for v in second)
                    i = node(left, record + (b,), second)
                    j = node(right, record + (h,), first)
                    require(old[first] * nodes[i] == old[second] * nodes[j],
                            "raw diamond ratio mismatch")
                    raw_links.append((i, j, old[first], old[second]))
                    adjacency[i].add(j)
                    adjacency[j].add(i)
                    edge_count += 1
                    zero_count += int(not any(record) and b == h == 0)
                    equal_count += int(first == second)
                    loop_count += int(i == j)
    component, roots = {}, []
    for root in sorted(nodes):
        if root in component:
            continue
        number = len(roots)
        roots.append(root)
        component[root] = number
        queue = [root]
        while queue:
            for neighbor in sorted(adjacency[queue.pop()]):
                if neighbor not in component:
                    component[neighbor] = number
                    queue.append(neighbor)
    rows = []
    for edges, record, entries in raw_rows:
        a, b = {}, {}
        for key, u, preserves in entries:
            c = component[key]
            a[c] = a.get(c, F(0)) + u
            if preserves:
                b[c] = b.get(c, F(0)) + u
        rows.append((edges, record, a, b))
    counts = (len(rows), proper_count, len(nodes), len(roots),
              edge_count, zero_count, equal_count, loop_count)
    require(counts == (640, 5072, 305, 109, 7616, 238, 1280, 1536),
            "fixed layer coverage changed")
    return rows, roots, counts, (nodes, component, raw_links)


def exact_fraction(value):
    require(type(value) is str, "certificate coefficient must be a rational string")
    return F(value)


def load_certificate(roots):
    path = Path(__file__).with_name("CERTIFICATE.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data["schema"] == "ri41-height-primal-v1" and data["seed"] == "interior_a"
            and data["parent_size"] == 4 and data["potential"] == "RI-38 maximal-deletion"
            and data["component_order"] == "increasing minimum canonical-local-key",
            "certificate domain changed")
    require(data["roots"] == [list(root) for root in roots], "certificate component roots mismatch")
    alpha = [exact_fraction(data["default_alpha"])] * len(roots)
    for key, value in data["overrides"].items():
        require(key == str(int(key)) and 0 <= int(key) < len(roots), "invalid component index")
        alpha[int(key)] = exact_fraction(value)
    return alpha


def masses(rows, alpha):
    require(all(x > 0 for x in alpha), "nonpositive component")
    proper, preserving = [], []
    for _, _, a, b in rows:
        proper.append(sum((u * alpha[c] for c, u in a.items()), F(0)))
        preserving.append(sum((u * alpha[c] for c, u in b.items()), F(0)))
    require(max(proper) < 1, "nonpositive full complement")
    require(min(preserving) >= F(1, 2), "height target failure")
    return proper, preserving


def rejected(call, expected):
    try:
        call()
    except RuntimeError as error:
        require(str(error) == expected, "negative control failed for an unexpected reason")
    else:
        raise RuntimeError("negative control was accepted")


def main():
    rows, roots, counts, graph = layer()
    totals = [sum(a.values(), F(0)) for _, _, a, _ in rows]
    preserves = [sum(b.values(), F(0)) for _, _, _, b in rows]
    maximum, minimum = max(totals), min(preserves)
    if sys.argv[1:] == ["--matrix"]:
        print(json.dumps({"roots": roots,
                          "rows": [{"order": sorted(e), "marks": r,
                                    "A": {str(k): str(v) for k, v in a.items()},
                                    "B": {str(k): str(v) for k, v in b.items()}}
                                   for e, r, a, b in rows]}))
        return
    require(not sys.argv[1:], "unknown arguments")
    print("fixed_seed=interior_a seed_scale=" + str(SEED_SCALE))
    print("rows,proper_summands,nodes,components,raw_edges,all_zero,equal,loops=" + str(counts))
    print(f"common: M={maximum} min_B={minimum} inf_worst_tau={1-minimum/maximum}")
    print("M_row=" + str(totals.index(maximum)) + " min_B_row=" + str(preserves.index(minimum)))
    require((maximum, minimum) == (F(7657469, 2371842), F(256, 1185921)),
            "common-scale extrema changed")
    require(1 - minimum / maximum > F(1, 2), "common-scale rejection changed")
    alpha = load_certificate(roots)
    proper, preserving = masses(rows, alpha)
    nodes, component, links = graph
    for i, j, old_first, old_second in links:
        left = old_first / 2 * (alpha[component[i]] * nodes[i] / 2)
        right = old_second / 2 * (alpha[component[j]] * nodes[j] / 2)
        require(left == right, "scaled full-kernel multiplier mismatch")
    minimum_slot = F(1)
    for row_index, (edges, record, _, _) in enumerate(rows):
        full = frozenset(range(4))
        probabilities = {s: alpha[component[node(edges, record, s)]] * potential(edges, record, s)
                         for s in ideals(4, edges) if s != full}
        probabilities[full] = 1 - sum(probabilities.values(), F(0))
        require(sum(probabilities.values(), F(0)) == 1 and all(q > 0 for q in probabilities.values()),
                "direct labeled row is not a strictly positive probability row")
        minimum_slot = min(minimum_slot, *probabilities.values())
        h = height(edges, full)
        direct_tau = sum((q for s, q in probabilities.items()
                          if height(edges | frozenset((v, 4) for v in s), frozenset(range(5))) > h), F(0))
        require(direct_tau == 1 - preserving[row_index] <= F(1, 2),
                "direct actual-height target failed")
    require(1-max(proper) == F(33901019, 474368400) and
            1-min(preserving) == F(14082809, 29648025), "exact certificate margins changed")
    print(f"component: min_alpha={min(alpha)} min_full={1-max(proper)} "
          f"max_tau={1-min(preserving)} min_ideal_probability={minimum_slot}; PASS")
    print(f"direct_rows={len(rows)} actual_height_slots={counts[1]+len(rows)} "
          f"full_kernel_multipliers={len(links)}; PASS")
    zero = list(alpha)
    zero[0] = F(0)
    rejected(lambda: masses(rows, zero), "nonpositive component")
    rejected(lambda: masses(rows, [1/maximum] * len(roots)), "nonpositive full complement")
    rejected(lambda: masses(rows, [F(1, 8)] * len(roots)), "height target failure")
    print("negative_controls=zero_component,zero_full_complement,positive_wrong_height; PASS")
    print("DONE: exact fixed-prefix parent-four witness; no optimality or asymptotic claim")


if __name__ == "__main__":
    main()
