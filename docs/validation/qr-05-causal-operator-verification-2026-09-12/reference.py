"""Independent exact elimination and explicit-chain reference; no I/O."""

from fractions import Fraction
from itertools import permutations


def _copy_matrix(matrix):
    return [row[:] for row in matrix]


def _zeros(n):
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def _identity(n):
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def _rational(value):
    if type(value) is not Fraction:
        raise ValueError("A and d require plain Fractions")
    if abs(value.numerator).bit_length() > 128 or value.denominator.bit_length() > 128:
        raise ValueError("input rational exceeds the inclusive 128-bit bound")


def _validated_copy(world):
    if type(world) is not dict:
        raise ValueError("world must be a plain dict")
    if any(type(key) is not str for key in world) or set(world) != {"C", "A", "d"}:
        raise ValueError("world must have exactly C, A and d")
    relation = world["C"]
    weights = world["A"]
    if type(relation) is not list or not 1 <= len(relation) <= 4:
        raise ValueError("C must be a plain square list with one to four nodes")
    n = len(relation)
    if type(weights) is not list or len(weights) != n:
        raise ValueError("A must have the same square shape as C")
    for matrix in (relation, weights):
        if any(type(row) is not list or len(row) != n for row in matrix):
            raise ValueError("matrix rows must be plain lists of the common dimension")
    for row in relation:
        if any(type(entry) is not int or entry not in (0, 1) for entry in row):
            raise ValueError("C entries must be plain ints zero or one")
    for row in weights:
        for entry in row:
            _rational(entry)
    _rational(world["d"])
    if world["d"] <= 0:
        raise ValueError("d must be positive")
    if any(relation[i][i] for i in range(n)):
        raise ValueError("C must be irreflexive")
    for i in range(n):
        for j in range(n):
            if not relation[i][j] and weights[i][j] != 0:
                raise ValueError("A must vanish outside C")
            for k in range(n):
                if relation[i][k] and relation[k][j] and not relation[i][j]:
                    raise ValueError("C must already be transitive")
    return {"C": _copy_matrix(relation), "A": _copy_matrix(weights), "d": world["d"]}


def _inverse(matrix):
    """Gauss–Jordan elimination without causal or triangular shortcuts."""
    n = len(matrix)
    identity = _identity(n)
    augmented = [matrix[i][:] + identity[i][:] for i in range(n)]
    for column in range(n):
        pivot_row = next((i for i in range(column, n) if augmented[i][column] != 0), None)
        if pivot_row is None:
            raise ValueError("singular matrix cannot supply an inverse")
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[column],
        )
        pivot = augmented[column][column]
        augmented[column] = [entry / pivot for entry in augmented[column]]
        for row in range(n):
            if row != column:
                multiplier = augmented[row][column]
                augmented[row] = [
                    augmented[row][j] - multiplier * augmented[column][j] for j in range(2 * n)
                ]
    return [row[n:] for row in augmented]


def _product(left, right):
    n = len(left)
    result = _zeros(n)
    for receiving in range(n):
        for sending in range(n):
            for middle in range(n):
                result[receiving][sending] += left[receiving][middle] * right[middle][sending]
    return result


def _chains_and_powers(relation, weights, diagonal):
    """Enumerate permutations, then sum raw chain products for each A power."""
    n = len(relation)
    powers = [_identity(n)] + [_zeros(n) for _ in range(n)]
    paths = []
    for node_count in range(1, n + 1):
        for nodes in permutations(range(n), node_count):
            if not all(relation[nodes[k + 1]][nodes[k]] for k in range(node_count - 1)):
                continue
            edge_weights = [weights[nodes[k + 1]][nodes[k]] for k in range(node_count - 1)]
            raw_product = Fraction(1)
            for weight in edge_weights:
                raw_product *= weight
            paths.append(
                {
                    "nodes": list(nodes),
                    "weights": edge_weights,
                    "contribution": raw_product / diagonal**node_count,
                }
            )
            if node_count > 1:
                powers[node_count - 1][nodes[-1]][nodes[0]] += raw_product
    return paths, powers


def _support(matrix):
    return [
        [int(i != j and matrix[i][j] != 0) for j in range(len(matrix))] for i in range(len(matrix))
    ]


def _reachability(support):
    """Traverse each source separately, using only the actual support mask."""
    n = len(support)
    closure = [[0 for _ in range(n)] for _ in range(n)]
    for source in range(n):
        pending = [source]
        visited = {source}
        while pending:
            current = pending.pop()
            for destination in range(n):
                if support[destination][current] and destination not in visited:
                    visited.add(destination)
                    pending.append(destination)
                    closure[destination][source] = 1
    return closure


def _differences(relation, observed):
    missing = []
    extra = []
    for i in range(len(relation)):
        for j in range(len(relation)):
            if relation[i][j] and not observed[i][j]:
                missing.append([i, j])
            if not relation[i][j] and observed[i][j]:
                extra.append([i, j])
    return missing, extra


def evaluate(world):
    """Return the exact native report for one strictly validated finite world."""
    copied = _validated_copy(world)
    relation, weights, diagonal = copied["C"], copied["A"], copied["d"]
    n = len(relation)
    cover_matrix = [
        [
            int(
                bool(relation[i][j])
                and not any(relation[i][k] and relation[k][j] for k in range(n))
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    matrix = [[diagonal * int(i == j) - weights[i][j] for j in range(n)] for i in range(n)]
    inverse = _inverse(matrix)
    antisymmetric = [[inverse[i][j] - inverse[j][i] for j in range(n)] for i in range(n)]
    paths, powers = _chains_and_powers(relation, weights, diagonal)
    support_a, support_g = _support(weights), _support(inverse)
    closure_a, closure_g = _reachability(support_a), _reachability(support_g)
    covers = [
        {
            "pair": [i, j],
            "A": weights[i][j],
            "G": inverse[i][j],
            "expected": weights[i][j] / diagonal**2,
        }
        for i in range(n)
        for j in range(n)
        if cover_matrix[i][j]
    ]
    missing_direct, extra_direct = _differences(relation, support_g)
    missing_reachable, extra_reachable = _differences(relation, closure_g)
    return {
        "world": copied,
        "L": cover_matrix,
        "powers": powers,
        "M": matrix,
        "G": inverse,
        "Delta": antisymmetric,
        "MG": _product(matrix, inverse),
        "GM": _product(inverse, matrix),
        "paths": paths,
        "support_A": support_a,
        "support_G": support_g,
        "closure_A": closure_a,
        "closure_G": closure_g,
        "covers": covers,
        "missing_direct": missing_direct,
        "extra_direct": extra_direct,
        "missing_reachable": missing_reachable,
        "extra_reachable": extra_reachable,
        "flags": {
            "direct_equal": support_g == relation,
            "reachability_equal": closure_g == relation,
            "closures_equal": closure_a == closure_g,
            "covers_nonzero": all(cover["A"] != 0 for cover in covers),
            "covers_positive": all(cover["A"] > 0 for cover in covers),
            "A_nonnegative": all(entry >= 0 for row in weights for entry in row),
            "positive_sign_rule": all(
                ((antisymmetric[i][j] > 0) == (relation[i][j] == 1))
                and ((antisymmetric[i][j] < 0) == (relation[j][i] == 1))
                for i in range(n)
                for j in range(n)
            ),
        },
    }


def _base_worlds():
    """Literal independent construction of the thirteen prospective cases."""
    cases = (
        ("singleton", 1, (), (), (1, 1)),
        ("antichain", 3, (), (), (1, 1)),
        (
            "chain",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 1, 1), (2, 1, 1, 1)),
            (1, 1),
        ),
        (
            "fork",
            3,
            ((1, 0), (2, 0)),
            ((1, 0, 1, 1), (2, 0, 1, 1)),
            (1, 1),
        ),
        (
            "diamond",
            4,
            ((1, 0), (2, 0), (3, 0), (3, 1), (3, 2)),
            ((1, 0, 1, 1), (2, 0, 1, 1), (3, 1, 1, 1), (3, 2, 1, 1)),
            (1, 1),
        ),
        (
            "missing_cover",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 1, 1),),
            (1, 1),
        ),
        ("single_edge", 3, ((1, 0),), ((1, 0, 1, 1),), (1, 1)),
        (
            "signed_diamond",
            4,
            ((1, 0), (2, 0), (3, 0), (3, 1), (3, 2)),
            ((1, 0, 1, 1), (2, 0, 1, 1), (3, 1, 1, 1), (3, 2, -1, 1)),
            (1, 1),
        ),
        (
            "toy_cancel",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 3, 1), (2, 0, -3, 1), (2, 1, 3, 1)),
            (3, 1),
        ),
        (
            "toy_sign",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 3, 1), (2, 0, -3, 1), (2, 1, 3, 1)),
            (5, 1),
        ),
        ("forward_pair", 2, ((1, 0),), ((1, 0, 1, 1),), (1, 1)),
        ("reversed_signed_pair", 2, ((0, 1),), ((0, 1, -1, 1),), (1, 1)),
        (
            "signed_relabelled_chain",
            3,
            ((0, 1), (2, 0), (2, 1)),
            ((0, 1, -1, 1), (2, 0, 1, 1), (2, 1, 1, 1)),
            (1, 1),
        ),
    )
    worlds = []
    for name, n, pairs, weighted_pairs, diagonal in cases:
        relation = [[0 for _ in range(n)] for _ in range(n)]
        weights = _zeros(n)
        for receiver, sender in pairs:
            relation[receiver][sender] = 1
        for receiver, sender, numerator, denominator in weighted_pairs:
            weights[receiver][sender] = Fraction(numerator, denominator)
        worlds.append((name, {"C": relation, "A": weights, "d": Fraction(*diagonal)}))
    return worlds


def _transform(world, variant):
    relation, weights, diagonal = world["C"], world["A"], world["d"]
    n = len(relation)
    if variant == "identity":
        return {"C": _copy_matrix(relation), "A": _copy_matrix(weights), "d": diagonal}
    if variant == "cyclic":
        new_relation = [[0 for _ in range(n)] for _ in range(n)]
        new_weights = _zeros(n)
        for i in range(n):
            for j in range(n):
                new_relation[(i + 1) % n][(j + 1) % n] = relation[i][j]
                new_weights[(i + 1) % n][(j + 1) % n] = weights[i][j]
        return {"C": new_relation, "A": new_weights, "d": diagonal}
    if variant == "reversal":
        return {
            "C": [[relation[j][i] for j in range(n)] for i in range(n)],
            "A": [[weights[j][i] for j in range(n)] for i in range(n)],
            "d": diagonal,
        }
    if variant == "rescale":
        multiplier = Fraction(3, 2)
        return {
            "C": _copy_matrix(relation),
            "A": [[multiplier * entry for entry in row] for row in weights],
            "d": multiplier * diagonal,
        }
    raise ValueError("unknown fixed variant")


def analyze():
    """Return only the independently constructed fixed rows and collisions."""
    variants = ("identity", "cyclic", "reversal", "rescale")
    rows = []
    by_id = {}
    for base, world in _base_worlds():
        for variant in variants:
            row = evaluate(_transform(world, variant))
            identifier = base + ":" + variant
            row.update({"id": identifier, "base": base, "variant": variant})
            rows.append(row)
            by_id[identifier] = row
    witnesses = []
    pairs = (
        ("zero_cover_order", "G", "missing_cover", "single_edge"),
        ("signed_orientation", "Delta", "forward_pair", "reversed_signed_pair"),
        ("signed_nonisomorphic", "Delta", "fork", "signed_relabelled_chain"),
    )
    for kind, channel, left_base, right_base in pairs:
        for variant in variants:
            identifiers = [left_base + ":" + variant, right_base + ":" + variant]
            left, right = (by_id[identifier] for identifier in identifiers)
            if left[channel] != right[channel]:
                raise ValueError("declared collision has different channel values")
            if left["world"]["C"] == right["world"]["C"]:
                raise ValueError("declared collision has equal target relations")
            witnesses.append(
                {
                    "kind": kind,
                    "variant": variant,
                    "channel": channel,
                    "rows": identifiers,
                    "value": _copy_matrix(left[channel]),
                    "targets": [
                        _copy_matrix(left["world"]["C"]),
                        _copy_matrix(right["world"]["C"]),
                    ],
                }
            )
    return {"schema": "qr05-causal-operator-report-v1", "rows": rows, "witnesses": witnesses}
