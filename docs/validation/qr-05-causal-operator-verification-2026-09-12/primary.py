"""Exact finite-power causal responses; independent, pure primary route.

Rows receive from columns.  The fixed study is assembled locally from the
prospective case specification, never from another implementation or a file.
"""

from fractions import Fraction


def _fraction(value, name):
    if type(value) is not Fraction:
        raise ValueError(f"{name} must be a plain Fraction")
    if abs(value.numerator).bit_length() > 128 or value.denominator.bit_length() > 128:
        raise ValueError(f"{name} exceeds the 128-bit input bound")


def _validate(world):
    if type(world) is not dict:
        raise ValueError("world must be a plain dict")
    if any(type(key) is not str for key in world) or set(world) != {"C", "A", "d"}:
        raise ValueError("world must have exactly the plain keys C, A, d")
    relation = world["C"]
    weights = world["A"]
    if type(relation) is not list or not 1 <= len(relation) <= 4:
        raise ValueError("C must be a plain list with 1 through 4 rows")
    n = len(relation)
    for name, matrix in (("C", relation), ("A", weights)):
        if type(matrix) is not list or len(matrix) != n:
            raise ValueError(f"{name} must be a matching plain square list")
        for row in matrix:
            if type(row) is not list or len(row) != n:
                raise ValueError(f"{name} must have plain square rows")
            for value in row:
                if name == "C":
                    if type(value) is not int or value not in (0, 1):
                        raise ValueError("C entries must be plain int 0 or 1")
                else:
                    _fraction(value, "A entry")
    _fraction(world["d"], "d")
    if world["d"] <= 0:
        raise ValueError("d must be strictly positive")
    for i in range(n):
        if relation[i][i] != 0:
            raise ValueError("C must be irreflexive")
        for j in range(n):
            if not relation[i][j] and weights[i][j] != 0:
                raise ValueError("A must vanish outside C")
            for k in range(n):
                if relation[i][k] and relation[k][j] and not relation[i][j]:
                    raise ValueError("C must be the complete transitive strict order")


def _copy(matrix):
    return [row[:] for row in matrix]


def _identity(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def _multiply(left, right):
    n = len(left)
    return [
        [sum((left[i][k] * right[k][j] for k in range(n)), Fraction(0)) for j in range(n)]
        for i in range(n)
    ]


def _support(matrix):
    n = len(matrix)
    return [[int(i != j and matrix[i][j] != 0) for j in range(n)] for i in range(n)]


def _closure(support):
    """Warshall closure of a support mask, without consulting target C."""
    reached = _copy(support)
    n = len(reached)
    for intermediate in range(n):
        for receiver in range(n):
            for sender in range(n):
                if reached[receiver][intermediate] and reached[intermediate][sender]:
                    reached[receiver][sender] = 1
    return reached


def _paths(relation, weights, diagonal):
    """Enumerate C-chains by extension, retaining even zero-weight paths."""
    n = len(relation)
    result = []

    def extend(nodes, edges, product):
        result.append(
            {
                "nodes": nodes[:],
                "weights": edges[:],
                "contribution": product / diagonal ** len(nodes),
            }
        )
        sender = nodes[-1]
        for receiver in range(n):
            if relation[receiver][sender]:
                weight = weights[receiver][sender]
                extend(nodes + [receiver], edges + [weight], product * weight)

    for start in range(n):
        extend([start], [], Fraction(1))
    result.sort(key=lambda path: (len(path["nodes"]), path["nodes"]))
    return result


def _differences(relation, candidate):
    n = len(relation)
    missing = []
    extra = []
    for i in range(n):
        for j in range(n):
            if relation[i][j] and not candidate[i][j]:
                missing.append([i, j])
            if candidate[i][j] and not relation[i][j]:
                extra.append([i, j])
    return missing, extra


def evaluate(world):
    """Return the complete exact row for one strictly validated finite world."""
    _validate(world)
    relation = world["C"]
    weights = world["A"]
    diagonal = world["d"]
    n = len(relation)

    powers = [_identity(n)]
    for _ in range(n):
        powers.append(_multiply(powers[-1], weights))
    response = [
        [
            sum(
                (powers[k][i][j] / diagonal ** (k + 1) for k in range(n)),
                Fraction(0),
            )
            for j in range(n)
        ]
        for i in range(n)
    ]
    operator = [
        [(diagonal if i == j else Fraction(0)) - weights[i][j] for j in range(n)] for i in range(n)
    ]
    antisymmetric = [[response[i][j] - response[j][i] for j in range(n)] for i in range(n)]
    links = [
        [
            int(relation[i][j] and not any(relation[i][k] and relation[k][j] for k in range(n)))
            for j in range(n)
        ]
        for i in range(n)
    ]
    covers = [
        {
            "pair": [i, j],
            "A": weights[i][j],
            "G": response[i][j],
            "expected": weights[i][j] / diagonal**2,
        }
        for i in range(n)
        for j in range(n)
        if links[i][j]
    ]
    support_a = _support(weights)
    support_g = _support(response)
    closure_a = _closure(support_a)
    closure_g = _closure(support_g)
    missing_direct, extra_direct = _differences(relation, support_g)
    missing_reachable, extra_reachable = _differences(relation, closure_g)
    flags = {
        "direct_equal": support_g == relation,
        "reachability_equal": closure_g == relation,
        "closures_equal": closure_a == closure_g,
        "covers_nonzero": all(cover["A"] != 0 for cover in covers),
        "covers_positive": all(cover["A"] > 0 for cover in covers),
        "A_nonnegative": all(value >= 0 for row in weights for value in row),
        "positive_sign_rule": all(
            ((antisymmetric[i][j] > 0) == (relation[i][j] == 1))
            and ((antisymmetric[i][j] < 0) == (relation[j][i] == 1))
            for i in range(n)
            for j in range(n)
        ),
    }
    return {
        "world": {"C": _copy(relation), "A": _copy(weights), "d": diagonal},
        "L": links,
        "powers": powers,
        "M": operator,
        "G": response,
        "Delta": antisymmetric,
        "MG": _multiply(operator, response),
        "GM": _multiply(response, operator),
        "paths": _paths(relation, weights, diagonal),
        "support_A": support_a,
        "support_G": support_g,
        "closure_A": closure_a,
        "closure_G": closure_g,
        "covers": covers,
        "missing_direct": missing_direct,
        "extra_direct": extra_direct,
        "missing_reachable": missing_reachable,
        "extra_reachable": extra_reachable,
        "flags": flags,
    }


def _cases():
    """Literal base data: name, size, full relation, weights, scalar diagonal."""
    return (
        ("singleton", 1, (), (), 1),
        ("antichain", 3, (), (), 1),
        ("chain", 3, ((1, 0), (2, 0), (2, 1)), ((1, 0, 1), (2, 1, 1)), 1),
        ("fork", 3, ((1, 0), (2, 0)), ((1, 0, 1), (2, 0, 1)), 1),
        (
            "diamond",
            4,
            ((1, 0), (2, 0), (3, 0), (3, 1), (3, 2)),
            ((1, 0, 1), (2, 0, 1), (3, 1, 1), (3, 2, 1)),
            1,
        ),
        ("missing_cover", 3, ((1, 0), (2, 0), (2, 1)), ((1, 0, 1),), 1),
        ("single_edge", 3, ((1, 0),), ((1, 0, 1),), 1),
        (
            "signed_diamond",
            4,
            ((1, 0), (2, 0), (3, 0), (3, 1), (3, 2)),
            ((1, 0, 1), (2, 0, 1), (3, 1, 1), (3, 2, -1)),
            1,
        ),
        (
            "toy_cancel",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 3), (2, 0, -3), (2, 1, 3)),
            3,
        ),
        (
            "toy_sign",
            3,
            ((1, 0), (2, 0), (2, 1)),
            ((1, 0, 3), (2, 0, -3), (2, 1, 3)),
            5,
        ),
        ("forward_pair", 2, ((1, 0),), ((1, 0, 1),), 1),
        ("reversed_signed_pair", 2, ((0, 1),), ((0, 1, -1),), 1),
        (
            "signed_relabelled_chain",
            3,
            ((0, 1), (2, 0), (2, 1)),
            ((0, 1, -1), (2, 0, 1), (2, 1, 1)),
            1,
        ),
    )


def _base_world(size, pairs, weights, diagonal):
    relation = [[0 for _ in range(size)] for _ in range(size)]
    matrix = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for receiver, sender in pairs:
        relation[receiver][sender] = 1
    for receiver, sender, value in weights:
        matrix[receiver][sender] = Fraction(value)
    return {"C": relation, "A": matrix, "d": Fraction(diagonal)}


def _variant(world, name):
    relation = world["C"]
    weights = world["A"]
    diagonal = world["d"]
    n = len(relation)
    if name == "identity":
        return {"C": _copy(relation), "A": _copy(weights), "d": diagonal}
    if name == "cyclic":
        moved_c = [[0 for _ in range(n)] for _ in range(n)]
        moved_a = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                moved_c[(i + 1) % n][(j + 1) % n] = relation[i][j]
                moved_a[(i + 1) % n][(j + 1) % n] = weights[i][j]
        return {"C": moved_c, "A": moved_a, "d": diagonal}
    if name == "reversal":
        return {
            "C": [[relation[j][i] for j in range(n)] for i in range(n)],
            "A": [[weights[j][i] for j in range(n)] for i in range(n)],
            "d": diagonal,
        }
    if name == "rescale":
        factor = Fraction(3, 2)
        return {
            "C": _copy(relation),
            "A": [[value * factor for value in row] for row in weights],
            "d": diagonal * factor,
        }
    raise ValueError("unknown fixed variant")


def analyze():
    """Return the fixed 52-row study and twelve explicit channel collisions."""
    variants = ("identity", "cyclic", "reversal", "rescale")
    rows = []
    for base, size, pairs, weights, diagonal in _cases():
        world = _base_world(size, pairs, weights, diagonal)
        for variant in variants:
            row = evaluate(_variant(world, variant))
            row.update({"id": base + ":" + variant, "base": base, "variant": variant})
            rows.append(row)

    by_id = {row["id"]: row for row in rows}
    witnesses = []
    pairs = (
        ("zero_cover_order", "G", "missing_cover", "single_edge"),
        ("signed_orientation", "Delta", "forward_pair", "reversed_signed_pair"),
        ("signed_nonisomorphic", "Delta", "fork", "signed_relabelled_chain"),
    )
    for kind, channel, left_base, right_base in pairs:
        for variant in variants:
            left_id = left_base + ":" + variant
            right_id = right_base + ":" + variant
            left = by_id[left_id]
            right = by_id[right_id]
            if left[channel] != right[channel]:
                raise ValueError("fixed collision channel values disagree")
            if left["world"]["C"] == right["world"]["C"]:
                raise ValueError("fixed collision target relations must differ")
            witnesses.append(
                {
                    "kind": kind,
                    "variant": variant,
                    "channel": channel,
                    "rows": [left_id, right_id],
                    "value": _copy(left[channel]),
                    "targets": [_copy(left["world"]["C"]), _copy(right["world"]["C"])],
                }
            )
    return {"schema": "qr05-causal-operator-report-v1", "rows": rows, "witnesses": witnesses}
