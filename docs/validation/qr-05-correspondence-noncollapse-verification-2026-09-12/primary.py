"""Exact finite comparisons by bitmasks and explicit strict-order paths.

This route is independent of the reference implementation. Importing this
module defines functions only; it constructs no fixtures or study results.
"""

from fractions import Fraction
from itertools import pairwise


def _container(value, name):
    if type(value) not in (list, tuple):
        raise TypeError(name + " must be a native list or tuple")


def _kernel(value, name):
    """Validate all bounded shapes before copying exact rational entries."""
    _container(value, name)
    size = len(value)
    if not 1 <= size <= 3:
        raise ValueError(name + " must have between one and three rows")
    for row in value:
        _container(row, name + " row")
        if len(row) != size:
            raise ValueError(name + " must be square")
    result = []
    for i, row in enumerate(value):
        copied = []
        for j, entry in enumerate(row):
            if type(entry) is not Fraction:
                raise TypeError(name + " entries must be native Fractions")
            if entry < 0:
                raise ValueError(name + " entries must be nonnegative")
            if entry.numerator.bit_length() > 128 or entry.denominator.bit_length() > 128:
                raise ValueError(name + " entries exceed the 128-bit input bound")
            if i == j and entry != 0:
                raise ValueError(name + " must have zero diagonal")
            copied.append(entry)
        result.append(copied)
    return result


def _strict(order):
    size = len(order)
    return not any(order[i][i] for i in range(size)) and all(
        not (order[i][j] and order[j][k]) or order[i][k]
        for i in range(size)
        for j in range(size)
        for k in range(size)
    )


def _inspect(kernel):
    size = len(kernel)
    support = [[entry > 0 for entry in row] for row in kernel]
    strict = _strict(support)
    conditional = [
        [i, j, k, kernel[i][k] - kernel[i][j] - kernel[j][k]]
        for i in range(size)
        for j in range(size)
        for k in range(size)
        if support[i][j] and support[j][k]
    ]
    gamma = [
        [
            max(
                max(abs(kernel[i][z] - kernel[j][z]), abs(kernel[z][i] - kernel[z][j]))
                for z in range(size)
            )
            for j in range(size)
        ]
        for i in range(size)
    ]
    twins = []
    visited = set()
    for i in range(size):
        if i not in visited:
            group = [j for j in range(size) if gamma[i][j] == 0]
            twins.append(group)
            visited.update(group)
    representatives = [group[0] for group in twins]
    return {
        "n": size,
        "kernel": [row[:] for row in kernel],
        "diameter": max(entry for row in kernel for entry in row),
        "support": support,
        "strict_support": strict,
        "conditional_residuals": conditional,
        "causal_valid": strict and all(row[3] >= 0 for row in conditional),
        "gamma": gamma,
        "gap": min(gamma[i][j] for i in range(size) for j in range(size) if i != j)
        if size > 1
        else None,
        "twins": twins,
        "quotient": [[kernel[i][j] for j in representatives] for i in representatives],
        "distinguishes": all(len(group) == 1 for group in twins),
    }


def inspect_kernel(d):
    """Inspect a supplied kernel without requiring causal admissibility."""
    return _inspect(_kernel(d, "kernel"))


def _members(value, nx, ny):
    _container(value, "relation")
    if not 1 <= len(value) <= nx * ny:
        raise ValueError("relation must be a nonempty bounded list of distinct pairs")
    pairs = []
    seen = set()
    for member in value:
        _container(member, "relation member")
        if len(member) != 2:
            raise ValueError("relation members must have two indices")
        i, j = member
        if type(i) is not int or type(j) is not int:
            raise TypeError("relation indices must be native ints")
        if not (0 <= i < nx and 0 <= j < ny):
            raise ValueError("relation index is out of range")
        pair = (i, j)
        if pair in seen:
            raise ValueError("relation members must be distinct")
        seen.add(pair)
        pairs.append([i, j])
    if len({pair[0] for pair in pairs}) != nx or len({pair[1] for pair in pairs}) != ny:
        raise ValueError("relation must be onto both inputs")
    pairs.sort()
    return pairs


def _normalized(kernel, diameter):
    if diameter == 0:
        return None
    return [[entry / diameter for entry in row] for row in kernel]


def _errors(left, right, members):
    errors = [[abs(left[i][ip] - right[j][jp]) for ip, jp in members] for i, j in members]
    maximum = max(entry for row in errors for entry in row)
    return {
        "errors": errors,
        "maximum": maximum,
        "argmax": [
            [row, column]
            for row in range(len(members))
            for column in range(len(members))
            if errors[row][column] == maximum
        ],
    }


def _record(left, right, normalized_left, normalized_right, members):
    return {
        "members": [member[:] for member in members],
        "raw": _errors(left, right, members),
        "normalized": _errors(normalized_left, normalized_right, members)
        if normalized_left is not None and normalized_right is not None
        else None,
    }


def relation_record(d, e, members):
    """Retain every ordered discrepancy cell of one supplied correspondence."""
    left, right = _kernel(d, "left kernel"), _kernel(e, "right kernel")
    pairs = _members(members, len(left), len(right))
    a = max(entry for row in left for entry in row)
    b = max(entry for row in right for entry in row)
    return _record(left, right, _normalized(left, a), _normalized(right, b), pairs)


def _minimum(records, indices, field):
    distance = min(records[i][field]["maximum"] for i in indices)
    return distance, [i for i in indices if records[i][field]["maximum"] == distance]


def compare(d, e):
    """Enumerate the entire bitmask universe, retaining every onto relation."""
    left, right = _kernel(d, "left kernel"), _kernel(e, "right kernel")
    nx, ny = len(left), len(right)
    x, y = _inspect(left), _inspect(right)
    normalized_left = _normalized(left, x["diameter"])
    normalized_right = _normalized(right, y["diameter"])
    universe = 1 << (nx * ny)
    relations = []
    for mask in range(universe):
        members = []
        rows, columns = 0, 0
        for i in range(nx):
            for j in range(ny):
                if mask & (1 << (i * ny + j)):
                    members.append([i, j])
                    rows |= 1 << i
                    columns |= 1 << j
        if rows == (1 << nx) - 1 and columns == (1 << ny) - 1:
            relations.append(_record(left, right, normalized_left, normalized_right, members))
    relations.sort(key=lambda item: tuple(tuple(member) for member in item["members"]))
    indices = list(range(len(relations)))
    raw_distance, raw_minimizers = _minimum(relations, indices, "raw")
    normalization_available = normalized_left is not None and normalized_right is not None
    normalized_distance, normalized_minimizers = (
        _minimum(relations, indices, "normalized") if normalization_available else (None, None)
    )
    bijections = [i for i in indices if len(relations[i]["members"]) == nx] if nx == ny else None
    raw_bijection_distance, raw_bijection_minimizers = (
        _minimum(relations, bijections, "raw") if bijections is not None else (None, None)
    )
    normalized_bijection_distance, normalized_bijection_minimizers = (
        _minimum(relations, bijections, "normalized")
        if bijections is not None and normalization_available
        else (None, None)
    )
    return {
        "x": x,
        "y": y,
        "relations": relations,
        "raw_distance": raw_distance,
        "normalized_distance": normalized_distance,
        "raw_minimizers": raw_minimizers,
        "normalized_minimizers": normalized_minimizers,
        "bijections": bijections,
        "raw_bijection_distance": raw_bijection_distance,
        "normalized_bijection_distance": normalized_bijection_distance,
        "raw_bijection_minimizers": raw_bijection_minimizers,
        "normalized_bijection_minimizers": normalized_bijection_minimizers,
        "bitmask_universe": universe,
        "safe_gap": all(gap is None or 2 * raw_distance < gap for gap in (x["gap"], y["gap"])),
    }


def _order(value, size):
    _container(value, "order")
    if len(value) != size:
        raise ValueError("order and weights must have the same size")
    for row in value:
        _container(row, "order row")
        if len(row) != size:
            raise ValueError("order must be square")
    copied = []
    for row in value:
        if any(type(entry) is not bool for entry in row):
            raise TypeError("order entries must be native bools")
        copied.append(list(row))
    if not _strict(copied):
        raise ValueError("order must be irreflexive and transitive")
    return copied


def _paths(order):
    """Explicitly visit every path, including every direct comparable edge."""
    paths = []

    def extend(nodes):
        for target in range(len(order)):
            if order[nodes[-1]][target]:
                following = nodes + [target]
                paths.append(following)
                extend(following)

    for source in range(len(order)):
        extend([source])
    paths.sort(key=tuple)
    return paths


def _residuals(order, weights):
    return [
        [i, j, k, weights[i][k] - weights[i][j] - weights[j][k]]
        for i in range(len(order))
        for j in range(len(order))
        for k in range(len(order))
        if order[i][j] and order[j][k]
    ]


def closure(order, w):
    """Close all supplied comparable weights using explicit path sums."""
    weights = _kernel(w, "weights")
    size = len(weights)
    relation = _order(order, size)
    if any(weights[i][j] > 0 and not relation[i][j] for i in range(size) for j in range(size)):
        raise ValueError("positive weights must be supported on the supplied order")
    covers = [
        [
            relation[i][j] and not any(relation[i][k] and relation[k][j] for k in range(size))
            for j in range(size)
        ]
        for i in range(size)
    ]
    paths = []
    for nodes in _paths(relation):
        path_weights = [weights[i][j] for i, j in pairwise(nodes)]
        paths.append(
            {
                "nodes": nodes,
                "weights": path_weights,
                "sum": sum(path_weights, Fraction(0)),
                "cover_only": all(covers[i][j] for i, j in pairwise(nodes)),
            }
        )
    closed = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    cover_closed = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    positive_reachability = [[False for _ in range(size)] for _ in range(size)]
    for path in paths:
        i, j = path["nodes"][0], path["nodes"][-1]
        closed[i][j] = max(closed[i][j], path["sum"])
        if path["cover_only"]:
            cover_closed[i][j] = max(cover_closed[i][j], path["sum"])
        if all(weight > 0 for weight in path["weights"]):
            positive_reachability[i][j] = True
    maximizers, cover_maximizers = [], []
    for i in range(size):
        for j in range(size):
            if relation[i][j]:
                connecting = [
                    index
                    for index, path in enumerate(paths)
                    if path["nodes"][0] == i and path["nodes"][-1] == j
                ]
                maximizers.append(
                    {
                        "pair": [i, j],
                        "paths": [
                            index for index in connecting if paths[index]["sum"] == closed[i][j]
                        ],
                    }
                )
                cover_maximizers.append(
                    {
                        "pair": [i, j],
                        "paths": [
                            index
                            for index in connecting
                            if paths[index]["cover_only"]
                            and paths[index]["sum"] == cover_closed[i][j]
                        ],
                    }
                )
    return {
        "order": relation,
        "weights": weights,
        "covers": covers,
        "paths": paths,
        "closure": closed,
        "cover_closure": cover_closed,
        "maximizers": maximizers,
        "cover_maximizers": cover_maximizers,
        "input_support": [[entry > 0 for entry in row] for row in weights],
        "closure_support": [[entry > 0 for entry in row] for row in closed],
        "positive_reachability": positive_reachability,
        "input_residuals": _residuals(relation, weights),
        "residuals": _residuals(relation, closed),
        "covers_positive": all(
            weights[i][j] > 0 for i in range(size) for j in range(size) if covers[i][j]
        ),
    }
