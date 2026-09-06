"""Independent exact order/geometry reference for the bounded QR-05D fixtures.

Coordinates are compared directly in null coordinates.  Interval sets count
the second and third relation powers; independently propagated chain counts
give the full endpoint polynomial.  No primary geometry executor or other
QR/DET/RET implementation is imported.  The supplied scalar kernel is not a
quantum channel, a probability, or a reconstruction theorem for spacetime.
"""

from __future__ import annotations

from fractions import Fraction

F = Fraction
_CASES = (
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


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _guard(value):
    if type(value) is int:
        _require(abs(value).bit_length() <= 4096, "reference integer exceeds 4096-bit bound")
    elif type(value) is F:
        _require(
            abs(value.numerator).bit_length() <= 4096 and value.denominator.bit_length() <= 4096,
            "reference rational exceeds 4096-bit bound",
        )
    else:
        raise ValueError("reference exact arithmetic requires integers or Fractions")
    return value


def _validate_order(past, density):
    _require(
        type(past) is list and 1 <= len(past) <= 51,
        "reference order must be a list with one to fifty-one events",
    )
    _require(type(density) is F and density > 0, "reference density must be a positive Fraction")
    _guard(density)
    copied = []
    for event, row in enumerate(past):
        _require(type(row) is list, "reference strict-past rows must be lists")
        _require(
            all(type(node) is int and 0 <= node < event for node in row),
            "reference strict past must contain earlier integer event indices",
        )
        _require(row == sorted(set(row)), "reference strict past must be sorted and unique")
        copied.append(frozenset(row))
    _require(
        all(copied[ancestor].issubset(row) for event, row in enumerate(copied) for ancestor in row),
        "reference order must already contain its transitive relations",
    )
    return tuple(copied)


def _wire_fraction_matrix(matrix):
    return [[str(_guard(value)) for value in row] for row in matrix]


def order_analysis(past, density):
    """Analyze a validated naturally labeled order at a supplied algebraic scale.

    The helper allows general finite orders without unique boundary events.
    Endpoint output always refers to indices zero and n-1; for n=1 its finite
    chain and coefficient arrays are empty.  Noncausal longest-chain entries are
    zero, while summary height counts events rather than edges.
    """
    ancestors = _validate_order(past, density)
    n = len(ancestors)
    relation = [[int(i in ancestors[j]) for j in range(n)] for i in range(n)]
    links = [[0] * n for _ in range(n)]
    intervals = [[0] * n for _ in range(n)]
    pairs = [[0] * n for _ in range(n)]
    longest = [[0] * n for _ in range(n)]
    for source in range(n):
        best = {source: 0}
        for target in range(source + 1, n):
            if source not in ancestors[target]:
                continue
            between = {node for node in ancestors[target] if source in ancestors[node]}
            intervals[source][target] = len(between)
            pairs[source][target] = sum(len(ancestors[node] & between) for node in between)
            links[source][target] = int(not between)
            best[target] = 1 + max(best[node] for node in ancestors[target] if node in best)
            longest[source][target] = best[target]

    # Count chains by their terminal vertex and edge count, not by matrix powers.
    counts = [[0] * n for _ in range(n)]
    counts[0][0] = 1
    for target in range(1, n):
        for predecessor in ancestors[target]:
            for length in range(1, n):
                counts[target][length] = _guard(
                    counts[target][length] + counts[predecessor][length - 1]
                )
    endpoint_counts = counts[n - 1][1:]
    endpoint_coefficients = []
    for length, count in enumerate(endpoint_counts, start=1):
        coefficient = (
            F(0)
            if count == 0
            else F((-1) ** (length - 1) * count, 2**length) / density ** (length - 1)
        )
        endpoint_coefficients.append(str(_guard(coefficient)))
    coefficient_matrices = [
        [[F(relation[i][j], 2) for j in range(n)] for i in range(n)],
        [[-F(intervals[i][j], 4) / density for j in range(n)] for i in range(n)],
        [[F(pairs[i][j], 8) / density**2 for j in range(n)] for i in range(n)],
    ]
    relation_count = sum(len(row) for row in ancestors)
    summary = {
        "events": n,
        "relations": relation_count,
        "links": sum(sum(row) for row in links),
        "incomparable": n * (n - 1) // 2 - relation_count,
        "minimal": sum(not row for row in ancestors),
        "maximal": sum(not any(node in row for row in ancestors) for node in range(n)),
        "height": 1 + max(max(row) for row in longest),
    }
    return {
        "n": n,
        "relation": relation,
        "links": links,
        "interval_cardinality": intervals,
        "chain_pairs": pairs,
        "longest_chain_edges": longest,
        "kernel_coefficients": [_wire_fraction_matrix(matrix) for matrix in coefficient_matrices],
        "summary": summary,
        "endpoint": {"chain_counts": endpoint_counts, "coefficients": endpoint_coefficients},
    }


def _coordinates(case):
    if case == "standard_example3":
        return None, F(12), None
    if case == "ferrers6":
        interiors = ((2, 6), (4, 4), (6, 2), (3, 14), (5, 12), (14, 10))
        return (
            [(F(0), F(0)), *((F(u, 16), F(v, 16)) for u, v in interiors), (F(1), F(1))],
            F(12),
            None,
        )
    side = {"mesh3": 3, "mesh7": 7}.get(case, 5)
    epsilon = F(1, 4 * side)
    denominator = (side + 1) * (1 + epsilon)
    points = [(F(0), F(0))]
    points.extend(
        ((i + epsilon * j) / denominator, (j + epsilon * i) / denominator)
        for i in range(1, side + 1)
        for j in range(1, side + 1)
    )
    points.append((F(1), F(1)))
    density = F(2 * side * side)
    if case == "mesh5_boost":
        points = [(2 * u, v / 2) for u, v in points]
    elif case in ("mesh5_dilate", "mesh5_dilate_wrong_density"):
        points = [(2 * u, 2 * v) for u, v in points]
        if case == "mesh5_dilate":
            density /= 4
    elif case == "mesh5_warp":
        points = [(u * u, v * v) for u, v in points]
    return points, density, (side * side + 1) // 2


def _null_order(points):
    _require(
        len({u for u, _ in points}) == len(points) and len({v for _, v in points}) == len(points),
        "reference coordinate fixture contains null-coordinate ties",
    )
    past = []
    for target, (u, v) in enumerate(points):
        row = [source for source, (a, b) in enumerate(points) if a < u and b < v]
        _require(
            all(source < target for source in row),
            "reference coordinates are not naturally labeled",
        )
        past.append(row)
    return past


def _standard_order():
    past = [[]]
    past.extend([[0] for _ in range(3)])
    past.extend([[0, *(1 + i for i in range(3) if i != j)] for j in range(3)])
    past.append(list(range(7)))
    return past


def _two_orders(interior_past):
    """Enumerate linear orders and test their intersections on six interiors."""
    n = len(interior_past)
    _require(n == 6, "reference realizer enumeration is restricted to six interiors")
    extensions = []

    def extend(prefix, remaining):
        if not remaining:
            extensions.append(list(prefix))
            return
        for node in sorted(remaining):
            if all(ancestor in prefix for ancestor in interior_past[node]):
                extend((*prefix, node), remaining - {node})

    extend((), set(range(n)))
    positions = [tuple(extension.index(node) for node in range(n)) for extension in extensions]
    count = 0
    first = None
    for left, left_positions in enumerate(positions):
        for right, right_positions in enumerate(positions):
            if all(
                (
                    (left_positions[source] < left_positions[target])
                    and (right_positions[source] < right_positions[target])
                )
                == (source in interior_past[target])
                for source in range(n)
                for target in range(n)
            ):
                count += 1
                if first is None:
                    first = [extensions[left], extensions[right]]
    return {"linear_extensions": extensions, "realizer_count": count, "first_realizer": first}


def _geometry(points, density, order):
    rows = []
    for source in range(len(points)):
        for target in range(len(points)):
            if order["relation"][source][target] == 0:
                continue
            du = points[target][0] - points[source][0]
            dv = points[target][1] - points[source][1]
            tau_squared = _guard(du * dv)
            _require(
                du > 0 and dv > 0 and tau_squared > 0,
                "reference geometric comparison requires strict timelike separation",
            )
            volume = _guard(tau_squared / 2)
            count_volume = _guard(F(order["interval_cardinality"][source][target]) / density)
            continuum = (F(1, 2), -tau_squared / 8, tau_squared * tau_squared / 128)
            errors = [
                F(order["kernel_coefficients"][degree][source][target]) - continuum[degree]
                for degree in range(3)
            ]
            rows.append(
                {
                    "source": source,
                    "target": target,
                    "tau_squared": str(tau_squared),
                    "volume": str(volume),
                    "count_volume": str(count_volume),
                    "volume_error": str(_guard(count_volume - volume)),
                    "continuum_coefficients": [str(_guard(value)) for value in continuum],
                    "coefficient_errors": [str(_guard(value)) for value in errors],
                }
            )
    absolute_volume_errors = [abs(F(row["volume_error"])) for row in rows]
    metrics = {
        "timelike_pairs": len(rows),
        "exact_volume_pairs": sum(error == 0 for error in absolute_volume_errors),
        "max_abs_volume_error": str(max(absolute_volume_errors, default=F(0))),
        "mean_abs_volume_error": str(_guard(sum(absolute_volume_errors, F(0)) / len(rows)))
        if rows
        else "0",
        "max_abs_coefficient_errors": [
            str(max((abs(F(row["coefficient_errors"][degree])) for row in rows), default=F(0)))
            for degree in range(3)
        ],
    }
    return {"pairs": rows, "metrics": metrics}


def analyze(wire):
    """Return the specified JSON-compatible analysis of one fixed fixture."""
    _require(
        type(wire) is dict and set(wire) == {"schema_version", "case"},
        "reference problem must have exactly the specified keys",
    )
    _require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05d-problem-v1",
        "reference schema is unsupported",
    )
    _require(type(wire["case"]) is str and wire["case"] in _CASES, "reference case is unsupported")
    case = wire["case"]
    coordinates, density, middle = _coordinates(case)
    past = _standard_order() if coordinates is None else _null_order(coordinates)
    order = order_analysis(past, density)
    geometry = None if coordinates is None else _geometry(coordinates, density, order)
    two_order = None
    if case in ("ferrers6", "standard_example3"):
        interior_past = [[ancestor - 1 for ancestor in row if ancestor != 0] for row in past[1:-1]]
        two_order = _two_orders(interior_past)
    probes = [{"name": "whole", "source": 0, "target": len(past) - 1}]
    if middle is not None:
        probes.extend(
            (
                {"name": "bottom_to_middle", "source": 0, "target": middle},
                {"name": "middle_to_top", "source": middle, "target": len(past) - 1},
            )
        )
    return {
        "case": case,
        "density": str(density),
        "coordinates": None
        if coordinates is None
        else [[str(_guard(u)), str(_guard(v))] for u, v in coordinates],
        "order": order,
        "geometry": geometry,
        "two_order": two_order,
        "probes": probes,
    }
