"""Declared rational inputs only; no mathematical engine imports."""

from fractions import Fraction as F

VARIANTS = ("identity", "cyclic", "reversal", "rescale")
EXPECTED_CENSUS = {
    "comparison_rows": 28,
    "input_nodes": 132,
    "input_cells": 332,
    "bitmask_universe": 4752,
    "relations": 2380,
    "relation_members": 12576,
    "raw_cells": 69976,
    "normalized_cells": 69960,
    "bijections": 64,
    "closure_rows": 16,
    "closure_nodes": 40,
    "closure_cells": 112,
    "comparable_slots": 36,
}


def matrix(n, entries=()):
    result = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, value in entries:
        result[i][j] = F(value)
    return result


def chain(value):
    return matrix(2, [(0, 1, value)])


def transform(a, variant, boolean=False):
    n = len(a)
    mapping = [(i + 1) % n if variant == "cyclic" else i for i in range(n)]
    factor = F(3, 2) if variant == "rescale" and not boolean else F(1)
    result = [[False if boolean else F(0) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            u, v = (j, i) if variant == "reversal" else (i, j)
            result[mapping[u]][mapping[v]] = a[i][j] if boolean else factor * a[i][j]
    return result, mapping


def comparison_cases():
    fork = matrix(3, [(0, 2, 1), (1, 2, F(11, 10))])
    excess = matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)])
    bases = [
        ("zero_multiplicity", matrix(1), matrix(2)),
        ("scale_pair", chain(1), chain(F(3, 2))),
        ("fork_correspondence", fork, matrix(3, [(0, 1, 1), (0, 2, F(11, 10))])),
        ("duplicate_fork", chain(1), matrix(3, [(0, 2, 1), (1, 2, 1)])),
        ("near_twins", fork, chain(1)),
        ("endpoint_excess", excess, matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 2)])),
        ("orientation_mismatch", chain(1), matrix(2, [(0, 1, 1), (1, 0, 1)])),
    ]
    rows = []
    for name, x, y in bases:
        for variant in VARIANTS:
            tx, xm = transform(x, variant)
            ty, ym = transform(y, variant)
            rows.append(
                {
                    "id": name + "/" + variant,
                    "base": name,
                    "variant": variant,
                    "x": tx,
                    "y": ty,
                    "x_map": xm,
                    "y_map": ym,
                    "scale": F(3, 2) if variant == "rescale" else F(1),
                }
            )
    return rows


def closure_cases():
    bases = [
        ("singleton", matrix(1)),
        ("endpoint_excess", matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)])),
        ("zero_cover", matrix(3, [(1, 2, 1)])),
        ("unit_all_pairs", matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)])),
    ]
    rows = []
    for name, weights in bases:
        n = len(weights)
        order = [[i < j for j in range(n)] for i in range(n)]
        for variant in VARIANTS:
            tw, mapping = transform(weights, variant)
            to, _ = transform(order, variant, boolean=True)
            rows.append(
                {
                    "id": name + "/" + variant,
                    "base": name,
                    "variant": variant,
                    "order": to,
                    "weights": tw,
                    "map": mapping,
                    "scale": F(3, 2) if variant == "rescale" else F(1),
                }
            )
    return rows


def controls():
    ident = [[0, 0], [1, 1]]
    order = [[i < j for j in range(3)] for i in range(3)]
    return {
        "triangle": {"chains": [chain(1), chain(F(3, 2)), chain(2)], "members": ident},
        "gap_boundary": {
            "x": matrix(3, [(0, 2, 1), (1, 2, 3)]),
            "y": chain(2),
            "members": [[0, 0], [1, 0], [2, 1]],
        },
        "fit_asymmetry": {
            "a": chain(1),
            "b": matrix(2, [(0, 1, 1), (1, 0, 1)]),
            "scale": F(1, 2),
            "members": ident,
        },
        "paired_list": {
            "L": [F(1), F(1), F(2)],
            "tau": [F(1), F(1), F(3)],
            "ell": F(1, 2),
            "c": F(3, 4),
        },
        "endpoint_trim": {
            "x": matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 3)]),
            "y": matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 2)]),
            "members": [[0, 0], [1, 1], [2, 2]],
            "included": [[0, 1], [1, 2]],
        },
        "lipschitz": {
            "order": order,
            "zero": matrix(3),
            "unit": matrix(3, [(0, 1, 1), (1, 2, 1), (0, 2, 1)]),
        },
    }
