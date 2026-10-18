"""Independent finite correspondence and masked max-plus reference calculus."""

from fractions import Fraction
from itertools import combinations, pairwise, product


def _square_rows(value):
    if type(value) not in (list, tuple):
        raise TypeError("matrix must be an exact list or tuple")
    n = len(value)
    if not 1 <= n <= 3:
        raise ValueError("matrix dimension must be between one and three")
    for row in value:
        if type(row) not in (list, tuple):
            raise TypeError("matrix rows must be exact lists or tuples")
        if len(row) != n:
            raise ValueError("matrix must be square")
    return [list(row) for row in value]


def _kernel(value):
    copied = _square_rows(value)
    for i, row in enumerate(copied):
        for j, entry in enumerate(row):
            if type(entry) is not Fraction:
                raise TypeError("kernel entries must be exact Fractions")
            if entry < 0:
                raise ValueError("kernel entries must be nonnegative")
            if entry.numerator.bit_length() > 128 or entry.denominator.bit_length() > 128:
                raise ValueError("input rational exceeds the inclusive 128-bit bound")
            if i == j and entry != 0:
                raise ValueError("kernel diagonal must be zero")
    return copied


def _is_strict(relation):
    n = len(relation)
    return not any(relation[i][i] for i in range(n)) and all(
        not (relation[i][j] and relation[j][k]) or relation[i][k]
        for i in range(n)
        for j in range(n)
        for k in range(n)
    )


def _support(kernel):
    return [[value > 0 for value in row] for row in kernel]


def _residuals(relation, kernel):
    n = len(relation)
    return [
        [i, j, k, kernel[i][k] - kernel[i][j] - kernel[j][k]]
        for i in range(n)
        for j in range(n)
        for k in range(n)
        if relation[i][j] and relation[j][k]
    ]


def _inspection(kernel):
    n = len(kernel)
    support = _support(kernel)
    strict = _is_strict(support)
    residuals = _residuals(support, kernel)
    gamma = [
        [
            max(
                max(abs(kernel[i][z] - kernel[j][z]), abs(kernel[z][i] - kernel[z][j]))
                for z in range(n)
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    profiles = {}
    for node in range(n):
        profile = tuple(kernel[node]) + tuple(kernel[other][node] for other in range(n))
        profiles.setdefault(profile, []).append(node)
    twins = list(profiles.values())
    representatives = [group[0] for group in twins]
    return {
        "n": n,
        "kernel": [row[:] for row in kernel],
        "diameter": max(value for row in kernel for value in row),
        "support": support,
        "strict_support": strict,
        "conditional_residuals": residuals,
        "causal_valid": strict and all(row[3] >= 0 for row in residuals),
        "gamma": gamma,
        "gap": None if n == 1 else min(gamma[i][j] for i in range(n) for j in range(n) if i != j),
        "twins": twins,
        "quotient": [[kernel[i][j] for j in representatives] for i in representatives],
        "distinguishes": all(len(group) == 1 for group in twins),
    }


def inspect_kernel(d):
    """Inspect a supplied nonnegative kernel without assuming causal validity."""
    return _inspection(_kernel(d))


def _members(value, m, n):
    if type(value) not in (list, tuple):
        raise TypeError("relation must be an exact list or tuple")
    if not 1 <= len(value) <= m * n:
        raise ValueError("relation size is outside the finite pair universe")
    pairs = []
    for member in value:
        if type(member) not in (list, tuple):
            raise TypeError("relation members must be exact lists or tuples")
        if len(member) != 2:
            raise ValueError("relation members must have two indices")
        if any(type(index) is not int for index in member):
            raise TypeError("relation indices must be exact ints")
        i, j = member
        if not 0 <= i < m or not 0 <= j < n:
            raise ValueError("relation index is out of range")
        pairs.append((i, j))
    if len(set(pairs)) != len(pairs):
        raise ValueError("relation members must be distinct")
    if {i for i, _ in pairs} != set(range(m)) or {j for _, j in pairs} != set(range(n)):
        raise ValueError("relation projections must both be onto")
    return [list(pair) for pair in sorted(pairs)]


def _normalized_pair(left, right):
    left_diameter = max(value for row in left for value in row)
    right_diameter = max(value for row in right for value in row)
    if left_diameter == 0 or right_diameter == 0:
        return None
    return (
        [[value / left_diameter for value in row] for row in left],
        [[value / right_diameter for value in row] for row in right],
    )


def _error_record(left, right, members):
    errors = [
        [abs(left[i][other_i] - right[j][other_j]) for other_i, other_j in members]
        for i, j in members
    ]
    maximum = max(value for row in errors for value in row)
    return {
        "errors": errors,
        "maximum": maximum,
        "argmax": [
            [i, j]
            for i, row in enumerate(errors)
            for j, value in enumerate(row)
            if value == maximum
        ],
    }


def _record(left, right, members, normalized):
    return {
        "members": [member[:] for member in members],
        "raw": _error_record(left, right, members),
        "normalized": None
        if normalized is None
        else _error_record(normalized[0], normalized[1], members),
    }


def relation_record(d, e, members):
    """Retain every ordered discrepancy for one explicitly supplied correspondence."""
    left, right = _kernel(d), _kernel(e)
    ordered = _members(members, len(left), len(right))
    return _record(left, right, ordered, _normalized_pair(left, right))


def _onto_members(m, n):
    """Choose nonempty neighborhoods independently for each source row."""
    neighborhoods = [subset for size in range(1, n + 1) for subset in combinations(range(n), size)]
    relations = []
    for selection in product(neighborhoods, repeat=m):
        if set().union(*selection) != set(range(n)):
            continue
        relations.append([[i, j] for i, neighborhood in enumerate(selection) for j in neighborhood])
    relations.sort(key=lambda members: tuple(tuple(member) for member in members))
    return relations


def _minimum(records, indices, kind):
    best = min(records[index][kind]["maximum"] for index in indices)
    attaining = [index for index in indices if records[index][kind]["maximum"] == best]
    return best, attaining


def compare(d, e):
    """Compare the complete onto-neighborhood relation family, including bijections."""
    left, right = _kernel(d), _kernel(e)
    m, n = len(left), len(right)
    normalized = _normalized_pair(left, right)
    records = [_record(left, right, members, normalized) for members in _onto_members(m, n)]
    indices = list(range(len(records)))
    raw_distance, raw_minimizers = _minimum(records, indices, "raw")
    normalized_distance = normalized_minimizers = None
    if normalized is not None:
        normalized_distance, normalized_minimizers = _minimum(records, indices, "normalized")
    bijections = raw_bijection_distance = raw_bijection_minimizers = None
    normalized_bijection_distance = normalized_bijection_minimizers = None
    if m == n:
        bijections = [index for index, record in enumerate(records) if len(record["members"]) == n]
        raw_bijection_distance, raw_bijection_minimizers = _minimum(records, bijections, "raw")
        if normalized is not None:
            normalized_bijection_distance, normalized_bijection_minimizers = _minimum(
                records, bijections, "normalized"
            )
    x, y = _inspection(left), _inspection(right)
    return {
        "x": x,
        "y": y,
        "relations": records,
        "raw_distance": raw_distance,
        "normalized_distance": normalized_distance,
        "raw_minimizers": raw_minimizers,
        "normalized_minimizers": normalized_minimizers,
        "bijections": bijections,
        "raw_bijection_distance": raw_bijection_distance,
        "normalized_bijection_distance": normalized_bijection_distance,
        "raw_bijection_minimizers": raw_bijection_minimizers,
        "normalized_bijection_minimizers": normalized_bijection_minimizers,
        "bitmask_universe": 2 ** (m * n),
        "safe_gap": all(
            space["gap"] is None or 2 * raw_distance < space["gap"] for space in (x, y)
        ),
    }


def _validated_order(order, weights):
    copied = _square_rows(order)
    if len(copied) != len(weights):
        raise ValueError("order and weights must have equal dimensions")
    if any(type(value) is not bool for row in copied for value in row):
        raise TypeError("order entries must be exact bools")
    if not _is_strict(copied):
        raise ValueError("order must be irreflexive and already transitive")
    if any(
        weights[i][j] > 0 and not value
        for i, row in enumerate(copied)
        for j, value in enumerate(row)
    ):
        raise ValueError("positive weights cannot occur outside the supplied order")
    return copied


def _topology(order):
    remaining = set(range(len(order)))
    topology = []
    while remaining:
        candidates = [
            node for node in sorted(remaining) if not any(order[other][node] for other in remaining)
        ]
        if not candidates:
            raise ValueError("a cyclic order has no topological traversal")
        node = candidates[0]
        topology.append(node)
        remaining.remove(node)
    return topology


def _max_plus(mask, weights, topology):
    """DAG dynamic programming; absent edges never acquire numeric-zero access."""
    n = len(mask)
    result = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for source in range(n):
        best = [None for _ in range(n)]
        best[source] = Fraction(0)
        for current in topology:
            if best[current] is None:
                continue
            for destination in range(n):
                if mask[current][destination]:
                    candidate = best[current] + weights[current][destination]
                    if best[destination] is None or candidate > best[destination]:
                        best[destination] = candidate
        for destination in range(n):
            if destination != source and best[destination] is not None:
                result[source][destination] = best[destination]
    return result


def _paths(order, weights, covers, topology):
    """Propagate full path lists separately from the max-plus value recurrence."""
    n = len(order)
    records = []
    for source in range(n):
        ending = [[] for _ in range(n)]
        ending[source].append([source])
        for current in topology:
            for prefix in ending[current]:
                for destination in range(n):
                    if not order[current][destination]:
                        continue
                    nodes = prefix + [destination]
                    ending[destination].append(nodes)
                    values = [weights[a][b] for a, b in pairwise(nodes)]
                    records.append(
                        {
                            "nodes": nodes,
                            "weights": values,
                            "sum": sum(values, Fraction(0)),
                            "cover_only": all(covers[a][b] for a, b in pairwise(nodes)),
                        }
                    )
    records.sort(key=lambda record: tuple(record["nodes"]))
    return records


def _positive_reachability(support):
    n = len(support)
    result = [[False for _ in range(n)] for _ in range(n)]
    for source in range(n):
        seen = {source}
        pending = [source]
        while pending:
            current = pending.pop()
            for destination in range(n):
                if support[current][destination] and destination not in seen:
                    seen.add(destination)
                    pending.append(destination)
                    result[source][destination] = True
    return result


def closure(order, w):
    """Close all comparable weights, retaining the distinct cover-only comparison."""
    weights = _kernel(w)
    relation = _validated_order(order, weights)
    n = len(relation)
    covers = [
        [
            relation[i][j] and not any(relation[i][k] and relation[k][j] for k in range(n))
            for j in range(n)
        ]
        for i in range(n)
    ]
    topology = _topology(relation)
    closed = _max_plus(relation, weights, topology)
    cover_closed = _max_plus(covers, weights, topology)
    paths = _paths(relation, weights, covers, topology)
    maximizers, cover_maximizers = [], []
    for i in range(n):
        for j in range(n):
            if not relation[i][j]:
                continue
            matching = [
                index
                for index, path in enumerate(paths)
                if path["nodes"][0] == i and path["nodes"][-1] == j
            ]
            maximizers.append(
                {
                    "pair": [i, j],
                    "paths": [index for index in matching if paths[index]["sum"] == closed[i][j]],
                }
            )
            cover_maximizers.append(
                {
                    "pair": [i, j],
                    "paths": [
                        index
                        for index in matching
                        if paths[index]["cover_only"] and paths[index]["sum"] == cover_closed[i][j]
                    ],
                }
            )
    input_support = _support(weights)
    return {
        "order": relation,
        "weights": weights,
        "covers": covers,
        "paths": paths,
        "closure": closed,
        "cover_closure": cover_closed,
        "maximizers": maximizers,
        "cover_maximizers": cover_maximizers,
        "input_support": input_support,
        "closure_support": _support(closed),
        "positive_reachability": _positive_reachability(input_support),
        "input_residuals": _residuals(relation, weights),
        "residuals": _residuals(relation, closed),
        "covers_positive": all(
            weights[i][j] > 0 for i in range(n) for j in range(n) if covers[i][j]
        ),
    }
