"""Exact supplied-geometry diagnostics via Lorentzian intervals and matrix powers."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

CASES = (
    "mesh3",
    "mesh5",
    "mesh7",
    "mesh5_boost",
    "mesh5_dilate",
    "mesh5_dilate_wrong_density",
    "mesh5_warp",
    "ferrers6",
    "standard_example3",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(value):
    value = F(value)
    require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= 4096,
        "rational component guard",
    )
    return str(value)


def validate(past, density):
    require(type(past) is list and 1 <= len(past) <= 51, "bounded strict-past list required")
    require(type(density) is F and density > 0, "positive Fraction density required")
    rational(density)
    for j, row in enumerate(past):
        require(type(row) is list, "past rows must be lists")
        require(all(type(i) is int and 0 <= i < j for i in row), "natural integer labels required")
        require(row == sorted(set(row)), "past row must be sorted and unique")
        require(all(set(past[i]) <= set(row) for i in row), "past is not transitive")


def matrix_product(left, right):
    columns = list(zip(*right, strict=True))
    return [[sum(a * b for a, b in zip(row, col, strict=True)) for col in columns] for row in left]


def order_analysis(past, density):
    validate(past, density)
    n = len(past)
    c = [[int(i in past[j]) for j in range(n)] for i in range(n)]
    c2 = matrix_product(c, c)
    c3 = matrix_product(c2, c)
    links = [[int(c[i][j] and not c2[i][j]) for j in range(n)] for i in range(n)]
    longest = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if c[i][j]:
                longest[i][j] = 1 + max(
                    (longest[i][k] for k in range(i + 1, j) if c[i][k] and c[k][j]),
                    default=0,
                )
    power, chain_counts = c, []
    for k in range(1, n):
        chain_counts.append(power[0][-1])
        power = matrix_product(power, c)
    require(not any(any(row) for row in power), "strict order failed nilpotence")
    relations = sum(map(sum, c))
    return {
        "n": n,
        "relation": c,
        "links": links,
        "interval_cardinality": c2,
        "chain_pairs": c3,
        "longest_chain_edges": longest,
        "kernel_coefficients": [
            [[rational(F(v, 2)) for v in row] for row in c],
            [[rational(-F(v) / (4 * density)) for v in row] for row in c2],
            [[rational(F(v) / (8 * density**2)) for v in row] for row in c3],
        ],
        "summary": {
            "events": n,
            "relations": relations,
            "links": sum(map(sum, links)),
            "incomparable": n * (n - 1) // 2 - relations,
            "minimal": sum(not row for row in past),
            "maximal": sum(not any(row) for row in c),
            "height": 1 + max(map(max, longest)),
        },
        "endpoint": {
            "chain_counts": chain_counts,
            "coefficients": [
                rational(F((-1) ** k * count, 2 ** (k + 1)) / density**k)
                for k, count in enumerate(chain_counts)
            ],
        },
    }


def two_order(past):
    require(len(past) == 6, "realizer check is bounded to six interiors")
    extensions, masks = [], []
    desired = sum(1 << (6 * i + j) for j, row in enumerate(past) for i in row)
    for permutation in permutations(range(6)):
        rank = {event: k for k, event in enumerate(permutation)}
        if all(rank[i] < rank[j] for j, row in enumerate(past) for i in row):
            extensions.append(list(permutation))
            masks.append(
                sum(1 << (6 * i + j) for i in range(6) for j in range(6) if rank[i] < rank[j])
            )
    count, first = 0, None
    for i, left in enumerate(masks):
        for j, right in enumerate(masks):
            if left & right == desired:
                count += 1
                if first is None:
                    first = [extensions[i], extensions[j]]
    return {"linear_extensions": extensions, "realizer_count": count, "first_realizer": first}


def augment(past):
    return [[], *[[0, *(i + 1 for i in row)] for row in past], list(range(len(past) + 1))]


def fixture(name):
    if name == "standard_example3":
        interior = [[], [], [], *[[i for i in range(3) if i != j] for j in range(3)]]
        return None, augment(interior), F(12), None
    if name == "ferrers6":
        points = [
            (F(u, 16), F(v, 16)) for u, v in ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
        ]
        points = [(F(0), F(0)), *points, (F(1), F(1))]
        density, middle = F(12), None
    else:
        m = 3 if name == "mesh3" else 7 if name == "mesh7" else 5
        epsilon = F(1, 4 * m)
        denominator = (m + 1) * (1 + epsilon)
        points = [(F(0), F(0))]
        points += [
            ((i + epsilon * j) / denominator, (j + epsilon * i) / denominator)
            for i in range(1, m + 1)
            for j in range(1, m + 1)
        ]
        points.append((F(1), F(1)))
        density, middle = F(2 * m * m), (m * m + 1) // 2
        if name == "mesh5_boost":
            points = [(2 * u, v / 2) for u, v in points]
        if name in ("mesh5_dilate", "mesh5_dilate_wrong_density"):
            points = [(2 * u, 2 * v) for u, v in points]
            if name == "mesh5_dilate":
                density /= 4
        if name == "mesh5_warp":
            points = [(u * u, v * v) for u, v in points]
    # The independent reference uses direct null-coordinate inequalities instead.
    tx = [((u + v) / 2, (u - v) / 2) for u, v in points]
    past = []
    for j, (tj, xj) in enumerate(tx):
        predecessors = []
        for i, (ti, xi) in enumerate(tx):
            if tj > ti and (tj - ti) ** 2 > (xj - xi) ** 2:
                require(i < j, "coordinate fixture not naturally labeled")
                predecessors.append(i)
        past.append(predecessors)
    require(len({u for u, _ in points}) == len(points), "unexpected equal u coordinates")
    require(len({v for _, v in points}) == len(points), "unexpected equal v coordinates")
    return points, past, density, middle


def compare_geometry(points, result, density):
    pairs = []
    for i, row in enumerate(result["relation"]):
        for j, related in enumerate(row):
            if not related:
                continue
            du, dv = points[j][0] - points[i][0], points[j][1] - points[i][1]
            dt, dx = (du + dv) / 2, (du - dv) / 2
            tau_squared = dt**2 - dx**2
            require(dt > 0 and tau_squared > 0, "non-timelike comparison")
            volume = tau_squared / 2
            count_volume = F(result["interval_cardinality"][i][j]) / density
            continuum = [F(1, 2), -tau_squared / 8, tau_squared**2 / 128]
            pairs.append(
                {
                    "source": i,
                    "target": j,
                    "tau_squared": rational(tau_squared),
                    "volume": rational(volume),
                    "count_volume": rational(count_volume),
                    "volume_error": rational(count_volume - volume),
                    "continuum_coefficients": list(map(rational, continuum)),
                    "coefficient_errors": [
                        rational(F(result["kernel_coefficients"][k][i][j]) - continuum[k])
                        for k in range(3)
                    ],
                }
            )
    errors = [abs(F(p["volume_error"])) for p in pairs]
    return {
        "pairs": pairs,
        "metrics": {
            "timelike_pairs": len(pairs),
            "exact_volume_pairs": sum(not e for e in errors),
            "max_abs_volume_error": rational(max(errors, default=F(0))),
            "mean_abs_volume_error": rational(sum(errors, F(0)) / len(errors) if errors else F(0)),
            "max_abs_coefficient_errors": [
                rational(max((abs(F(p["coefficient_errors"][k])) for p in pairs), default=F(0)))
                for k in range(3)
            ],
        },
    }


def analyze(wire):
    require(
        type(wire) is dict and set(wire) == {"schema_version", "case"},
        "exact fixture fields required",
    )
    require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05d-problem-v1",
        "unknown schema",
    )
    require(type(wire["case"]) is str and wire["case"] in CASES, "unknown fixed case")
    name = wire["case"]
    points, past, density, middle = fixture(name)
    result = order_analysis(past, density)
    interior = [[i - 1 for i in row if i != 0] for row in past[1:-1]]
    probes = [{"name": "whole", "source": 0, "target": len(past) - 1}]
    if middle is not None:
        probes += [
            {"name": "bottom_to_middle", "source": 0, "target": middle},
            {"name": "middle_to_top", "source": middle, "target": len(past) - 1},
        ]
    return {
        "case": name,
        "density": rational(density),
        "coordinates": None if points is None else [[rational(u), rational(v)] for u, v in points],
        "order": result,
        "geometry": None if points is None else compare_geometry(points, result, density),
        "two_order": two_order(interior) if name in ("ferrers6", "standard_example3") else None,
        "probes": probes,
    }
