"""Exact QR-05BM monomial integration and sparse projective instruments.

This standalone module has no file access and computes no fixture at import.
Only analyze(protocol) performs the prospectively fixed mathematical study.
"""

from fractions import Fraction as F
from itertools import product
from math import comb, gcd


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _native_input(value, active=None):
    if active is None:
        active = set()
    kind = type(value)
    if kind in (str, int):
        return
    _require(kind in (dict, list), "native protocol objects, strings and integers required")
    identity = id(value)
    _require(identity not in active, "cyclic protocol")
    if kind is dict:
        _require(all(type(key) is str for key in value), "native string protocol keys")
    active.add(identity)
    try:
        for child in value.values() if kind is dict else value:
            _native_input(child, active)
    finally:
        active.remove(identity)


def _validate(protocol):
    _native_input(protocol)
    expected = {
        "schema": "qr05bm-protocol-v1",
        "quota": 4,
        "worlds": [
            {"id": "A", "eta": 0, "scale": 1, "density_uv": 0},
            {"id": "B", "eta": 1, "scale": 1, "density_uv": 0},
            {"id": "C", "eta": 0, "scale": 1, "density_uv": 1},
            {"id": "D", "eta": 0, "scale": 4, "density_uv": 0},
            {"id": "E", "eta": 1, "scale": 4, "density_uv": 0},
        ],
        "regions": {
            "Q": [[0, 1], [1, 1], [0, 1], [1, 1]],
            "I": [[0, 1], [1, 2], [0, 1], [1, 2]],
        },
        "chart": {"U_scale": 2, "U_offset": 1, "V_scale": 3, "V_offset": -1},
        "menus": [
            {"id": "positive", "worlds": ["A", "B"]},
            {"id": "expanded", "worlds": ["A", "B", "C", "D", "E"]},
        ],
        "observer": {
            "protocol": "qr05bm-v1",
            "query": "o-m-t",
            "variants": ["membership", "membership-z"],
        },
        "coverage": {"membership": 80, "cq": 1280, "histogram": 25},
        "limits": {
            "source_bytes": 262144,
            "artifact_bytes": 16777216,
            "analysis_seconds": 30,
            "suite_seconds": 120,
            "alternate_reference_runs": 1,
        },
    }
    _require(type(protocol) is dict and protocol == expected, "complete fixed protocol required")


def _rational_pair(pair):
    _require(
        type(pair) is list and len(pair) == 2 and all(type(value) is int for value in pair),
        "native rational pair",
    )
    numerator, denominator = pair
    _require(denominator > 0 and gcd(numerator, denominator) == 1, "canonical rational pair")
    return F(numerator, denominator)


def _clean(poly):
    return {powers: value for powers, value in poly.items() if value != 0}


def _scale(poly, scalar):
    return _clean({powers: scalar * value for powers, value in poly.items()})


def _multiply_poly(left, right):
    result = {}
    for (i, j), first in left.items():
        for (k, ell), second in right.items():
            powers = (i + k, j + ell)
            result[powers] = result.get(powers, F(0)) + first * second
    return _clean(result)


def _integrate(poly, bounds):
    lower_u, upper_u, lower_v, upper_v = bounds
    _require(lower_u < upper_u and lower_v < upper_v, "positive integration rectangle")
    return sum(
        (
            coefficient
            * (upper_u ** (i + 1) - lower_u ** (i + 1))
            * (upper_v ** (j + 1) - lower_v ** (j + 1))
            / ((i + 1) * (j + 1))
            for (i, j), coefficient in poly.items()
        ),
        F(0),
    )


def _pullback(poly, u_scale, u_offset, v_scale, v_offset):
    """Substitute u=u_scale*U+u_offset and v=v_scale*V+v_offset."""
    result = {}
    for (i, j), coefficient in poly.items():
        for p in range(i + 1):
            for q in range(j + 1):
                value = (
                    coefficient
                    * comb(i, p)
                    * u_scale**p
                    * u_offset ** (i - p)
                    * comb(j, q)
                    * v_scale**q
                    * v_offset ** (j - q)
                )
                result[p, q] = result.get((p, q), F(0)) + value
    return _clean(result)


def _polynomial_wire(poly):
    return [[i, j, coefficient] for (i, j), coefficient in sorted(poly.items()) if coefficient]


def _measure_scalars(proper, weighted, regions):
    volume_q = _integrate(proper, regions["Q"])
    volume_i = _integrate(proper, regions["I"])
    mass_q = _integrate(weighted, regions["Q"])
    mass_i = _integrate(weighted, regions["I"])
    _require(
        0 < volume_i < volume_q and 0 < mass_i < mass_q,
        "strictly positive region and complement masses",
    )
    return {
        "volume_Q": volume_q,
        "volume_I": volume_i,
        "mass_Q": mass_q,
        "mass_I": mass_i,
        "target": volume_i / volume_q,
        "q": mass_i / mass_q,
    }


def _geometry(world, regions, chart):
    eta, scale, delta = (F(world[key]) for key in ("eta", "scale", "density_uv"))
    metric = _clean({(0, 0): scale, (1, 1): scale * eta})
    proper = _scale(metric, F(1, 2))
    density = _clean({(0, 0): F(1), (1, 1): delta})
    weighted = _multiply_poly(proper, density)
    original = _measure_scalars(proper, weighted, regions)
    normalized = _scale(weighted, 1 / original["mass_Q"])
    _require(_integrate(normalized, regions["Q"]) == 1, "normalized point law")
    _require(_integrate(normalized, regions["I"]) == original["q"], "membership marginal")

    a, b, c, d = [F(chart[key]) for key in ("U_scale", "U_offset", "V_scale", "V_offset")]
    _require(a > 0 and c > 0, "orientation-preserving passive axes")
    inverse = (1 / a, -b / a, 1 / c, -d / c)
    jacobian = 1 / (a * c)

    def transported_point(point):
        u, v = point
        return [a * u + b, c * v + d]

    source_marks = [
        [regions["Q"][0], regions["Q"][2]],
        [regions["I"][1], regions["I"][3]],
        [regions["Q"][1], regions["Q"][3]],
    ]
    origin, middle, top = [transported_point(point) for point in source_marks]
    transported_regions = {
        "Q": [origin[0], top[0], origin[1], top[1]],
        "I": [origin[0], middle[0], origin[1], middle[1]],
    }
    for name, (u0, u1, v0, v1) in regions.items():
        _require(
            transported_regions[name] == [a * u0 + b, a * u1 + b, c * v0 + d, c * v1 + d],
            "marked regions and direct coordinate transport agree",
        )
    new_metric = _scale(_pullback(metric, *inverse), jacobian)
    new_proper = _scale(new_metric, F(1, 2))
    new_density = _pullback(density, *inverse)
    new_weighted = _multiply_poly(new_proper, new_density)
    _require(
        new_proper == _scale(_pullback(proper, *inverse), jacobian),
        "volume transport has exactly one Jacobian",
    )
    _require(
        new_weighted == _scale(_pullback(weighted, *inverse), jacobian),
        "sampling density is a scalar, not a second volume Jacobian",
    )
    transported = _measure_scalars(new_proper, new_weighted, transported_regions)
    _require(transported == original, "all six original and passive scalar quantities agree")
    new_normalized = _scale(new_weighted, 1 / transported["mass_Q"])
    _require(
        new_normalized == _scale(_pullback(normalized, *inverse), jacobian),
        "complete normalized point measure transports",
    )
    _require(
        _integrate(new_normalized, transported_regions["Q"]) == 1
        and _integrate(new_normalized, transported_regions["I"]) == transported["q"],
        "transported normalized law and membership",
    )
    return {
        "metric_uv": _polynomial_wire(metric),
        "density_uv": _polynomial_wire(density),
        "proper_uv": _polynomial_wire(proper),
        "weighted_uv": _polynomial_wire(weighted),
        "normalized_uv": _polynomial_wire(normalized),
        **original,
        "chart": {
            "metric_UV": _polynomial_wire(new_metric),
            "density_UV": _polynomial_wire(new_density),
            "proper_UV": _polynomial_wire(new_proper),
            "weighted_UV": _polynomial_wire(new_weighted),
            "normalized_UV": _polynomial_wire(new_normalized),
            **transported,
        },
    }


def _identity(size):
    return {(i, i): F(1) for i in range(size)}


def _matrix_scale(matrix, scale):
    return {position: scale * value for position, value in matrix.items() if scale * value != 0}


def _matrix_add(left, right):
    result = dict(left)
    for position, value in right.items():
        result[position] = result.get(position, F(0)) + value
    return {position: value for position, value in result.items() if value != 0}


def _matrix_multiply(left, right):
    by_row = {}
    for (i, j), value in right.items():
        by_row.setdefault(i, []).append((j, value))
    result = {}
    for (i, k), first in left.items():
        for j, second in by_row.get(k, ()):
            position = (i, j)
            result[position] = result.get(position, F(0)) + first * second
    return {position: value for position, value in result.items() if value != 0}


def _adjoint(matrix):
    return {(j, i): value for (i, j), value in matrix.items()}


def _tensor(left, left_size, right, right_size):
    _require(
        all(0 <= i < left_size and 0 <= j < left_size for i, j in left)
        and all(0 <= i < right_size and 0 <= j < right_size for i, j in right),
        "tensor factor dimensions",
    )
    result = {
        (i * right_size + k, j * right_size + ell): first * second
        for (i, j), first in left.items()
        for (k, ell), second in right.items()
        if first * second != 0
    }
    return result, left_size * right_size


def _diagonal(matrix, size):
    _require(
        all(
            0 <= i < size and 0 <= j < size and (i == j or value == 0)
            for (i, j), value in matrix.items()
        ),
        "full retained state has no nonzero off-diagonal or out-of-range entry",
    )
    return [matrix.get((i, i), F(0)) for i in range(size)]


def _trace(matrix, size):
    return sum(_diagonal(matrix, size), F(0))


def _projector(outcome):
    _require(type(outcome) is int and outcome in (-1, 1), "projective outcome")
    z = {(0, 0): F(1), (1, 1): F(-1)}
    result = _matrix_scale(_matrix_add(_identity(2), _matrix_scale(z, F(outcome))), F(1, 2))
    _require(_matrix_multiply(result, result) == result, "idempotent local projector")
    _require(_adjoint(result) == result, "self-adjoint local projector")
    return result


def _local_projector(slot, outcome, quota):
    result, size = _identity(1), 1
    for index in range(quota):
        factor = _projector(outcome) if index == slot else _identity(2)
        result, size = _tensor(result, size, factor, 2)
    return result, size


def _quantum_instrument(quota):
    """Derive every branch by actual sparse K rho K-adjoint products."""
    preparation, size = _identity(1), 1
    mixed_qubit = _matrix_scale(_identity(2), F(1, 2))
    for _ in range(quota):
        preparation, size = _tensor(preparation, size, mixed_qubit, 2)
    mixed_diagonal = _diagonal(preparation, size)
    _require(_trace(preparation, size) == 1, "normalized full product preparation")
    branches = []
    aggregate = {}
    for outcomes in product((-1, 1), repeat=quota):
        kraus = _identity(size)
        for slot, outcome in enumerate(outcomes):
            factor, factor_size = _local_projector(slot, outcome, quota)
            _require(factor_size == size, "local projector full dimension")
            kraus = _matrix_multiply(factor, kraus)
        branch = _matrix_multiply(_matrix_multiply(kraus, preparation), _adjoint(kraus))
        diagonal = _diagonal(branch, size)
        probability = _trace(branch, size)
        _require(probability > 0 and all(value >= 0 for value in diagonal), "positive branch")
        conditional = [value / probability for value in diagonal]
        _require(sum(conditional, F(0)) == 1, "full normalized conditional state")
        aggregate = _matrix_add(aggregate, branch)
        branches.append(
            {
                "z": list(outcomes),
                "p": probability,
                "diagonal": diagonal,
                "conditional_diagonal": conditional,
            }
        )
    _require(aggregate == preparation, "nonselective projective output for this preparation")
    _require(sum((row["p"] for row in branches), F(0)) == 1, "complete quantum outcome law")
    return branches, mixed_diagonal


def _membership(geometry, quota):
    q = geometry["q"]
    rows = []
    for y in product((0, 1), repeat=quota):
        k = sum(y)
        probability = q**k * (1 - q) ** (quota - k)
        _require(probability > 0, "complete finite membership support")
        rows.append({"y": list(y), "k": k, "p": probability, "estimate": F(k, quota)})
    histogram = []
    for k in range(quota + 1):
        group = [row for row in rows if row["k"] == k]
        probability = sum((row["p"] for row in group), F(0))
        multiplicity = len(group)
        _require(multiplicity == comb(quota, k), "binomial word multiplicity")
        _require(
            probability == multiplicity * q**k * (1 - q) ** (quota - k),
            "histogram is not an individual-word law",
        )
        histogram.append({"k": k, "multiplicity": multiplicity, "p": probability})
    _require(sum((row["p"] for row in rows), F(0)) == 1, "normalized membership law")
    _require(sum((row["p"] for row in histogram), F(0)) == 1, "normalized histogram")
    mean = sum((row["p"] * row["estimate"] for row in rows), F(0))
    variance = sum((row["p"] * (row["estimate"] - mean) ** 2 for row in rows), F(0))
    _require(mean == q and variance == q * (1 - q) / quota, "enumerated iid moments")
    return (
        rows,
        histogram,
        {
            "mean": mean,
            "variance": variance,
            "bias": mean - geometry["target"],
        },
    )


def _cq_rows(membership, instrument):
    result = []
    for member in membership:
        for quantum in instrument:
            diagonal = [member["p"] * value for value in quantum["diagonal"]]
            probability = member["p"] * quantum["p"]
            trace = sum(diagonal, F(0))
            _require(trace == probability and trace > 0, "joint branch trace equals joint law")
            conditional = [value / trace for value in diagonal]
            _require(
                conditional == quantum["conditional_diagonal"],
                "world and membership do not alter the recorded-z conditional",
            )
            result.append(
                {
                    "y": list(member["y"]),
                    "z": list(quantum["z"]),
                    "p": probability,
                    "trace": trace,
                    "diagonal": diagonal,
                    "conditional_diagonal": conditional,
                }
            )
    _require(sum((row["p"] for row in result), F(0)) == 1, "complete joint CQ law")
    return result


def _classes(names, worlds, field):
    groups = []
    signatures = []
    for name in names:
        signature = tuple(row["p"] for row in worlds[name][field])
        if signature in signatures:
            groups[signatures.index(signature)].append(name)
        else:
            signatures.append(signature)
            groups.append([name])
    result = []
    for group in groups:
        targets = sorted({worlds[name]["geometry"]["target"] for name in group})
        result.append({"worlds": list(group), "targets": targets, "identified": len(targets) == 1})
    return result


def _menu(supplied, worlds):
    names = supplied["worlds"]
    classes = _classes(names, worlds, "membership")
    cq_classes = _classes(names, worlds, "cq")
    _require(classes == cq_classes, "inert qubits do not split complete-law classes")
    first = worlds[names[0]]["membership"]
    support = []
    for index, row in enumerate(first):
        compatible = [name for name in names if worlds[name]["membership"][index]["p"] > 0]
        _require(compatible == names, "all finite words retain every menu hypothesis")
        support.append({"y": list(row["y"]), "worlds": compatible})
    return {
        "id": supplied["id"],
        "worlds": list(names),
        "classes": classes,
        "cq_classes": cq_classes,
        "identified": all(group["identified"] for group in classes),
        "support": support,
    }


def _controls(worlds, instrument, mixed_diagonal, protocol):
    by_id = {world["id"]: world for world in worlds}
    scalar_fields = ("volume_Q", "volume_I", "mass_Q", "mass_I", "target", "q")
    chart_invariant = [
        world["id"]
        for world in worlds
        if all(world["geometry"][key] == world["geometry"]["chart"][key] for key in scalar_fields)
    ]
    _require(
        chart_invariant == [world["id"] for world in worlds],
        "complete passive-coordinate scalar invariance",
    )
    b, c = by_id["B"]["geometry"], by_id["C"]["geometry"]
    density_equal = b["weighted_uv"] == c["weighted_uv"] and b["mass_Q"] == c["mass_Q"]
    density_gap = c["target"] - b["target"]
    _require(density_equal and density_gap != 0, "whole-point-law density obstruction")
    _require(
        by_id["B"]["membership"] == by_id["C"]["membership"]
        and by_id["B"]["cq"] == by_id["C"]["cq"],
        "density compensation preserves the complete accessible experiment",
    )
    a = by_id["A"]
    _require(
        a["geometry"]["target"] != b["target"]
        and a["membership"] != by_id["B"]["membership"]
        and a["moments"]["bias"] == by_id["B"]["moments"]["bias"] == 0,
        "positive-family law distinction and sampler-conditional unbiasedness",
    )
    scales = {world["id"]: F(world["scale"]) for world in protocol["worlds"]}
    scale_pairs = []
    for first, second in (("A", "D"), ("B", "E")):
        left, right = by_id[first], by_id[second]
        left_geometry, right_geometry = left["geometry"], right["geometry"]
        factor = right_geometry["volume_Q"] / left_geometry["volume_Q"]
        normalized_equal = left_geometry["normalized_uv"] == right_geometry["normalized_uv"]
        target_equal = left_geometry["target"] == right_geometry["target"]
        law_equal = left["membership"] == right["membership"]
        cq_equal = left["cq"] == right["cq"]
        _require(
            factor == scales[second] / scales[first]
            and factor != 1
            and right_geometry["volume_I"] == factor * left_geometry["volume_I"]
            and normalized_equal
            and target_equal
            and law_equal
            and cq_equal,
            "absolute-scale change leaves the normalized experiment invariant",
        )
        scale_pairs.append(
            {
                "worlds": [first, second],
                "volume_factor": factor,
                "normalized_equal": normalized_equal,
                "target_equal": target_equal,
                "law_equal": law_equal,
                "cq_equal": cq_equal,
            }
        )
    conditional_by_z = {tuple(row["z"]): row["conditional_diagonal"] for row in instrument}
    marginals_match = True
    conditionals_common = True
    for world in worlds:
        grouped = {}
        for row in world["cq"]:
            grouped.setdefault(tuple(row["y"]), []).append(row)
            conditionals_common = (
                conditionals_common
                and row["conditional_diagonal"] == conditional_by_z[tuple(row["z"])]
            )
        for member in world["membership"]:
            group = grouped[tuple(member["y"])]
            marginal = sum((row["p"] for row in group), F(0))
            marginal_diagonal = [
                sum((row["diagonal"][index] for row in group), F(0))
                for index in range(len(mixed_diagonal))
            ]
            marginals_match = marginals_match and marginal == member["p"]
            _require(
                marginal_diagonal == [member["p"] * value for value in mixed_diagonal],
                "complete pre-Z conditional quantum payload remains common",
            )
    _require(
        marginals_match and conditionals_common, "complete CQ marginal and conditional controls"
    )
    return {
        "density_equal": density_equal,
        "density_target_gap": density_gap,
        "scale_pairs": scale_pairs,
        "chart_invariant": chart_invariant,
        "cq_marginals_match": marginals_match,
        "cq_conditionals_common": conditionals_common,
    }


def _native_report(value):
    if type(value) in (F, int, bool, str):
        return
    _require(type(value) in (list, dict), "unsupported report type")
    if type(value) is dict:
        _require(all(type(key) is str for key in value), "native report keys")
    for child in value.values() if type(value) is dict else value:
        _native_report(child)


def analyze(protocol):
    """Verify precisely the declared five-world experiment, without external access."""
    _validate(protocol)
    quota = protocol["quota"]
    regions = {
        name: [_rational_pair(pair) for pair in region]
        for name, region in protocol["regions"].items()
    }
    instrument, mixed_diagonal = _quantum_instrument(quota)
    worlds = []
    for supplied in protocol["worlds"]:
        geometry = _geometry(supplied, regions, protocol["chart"])
        membership, histogram, moments = _membership(geometry, quota)
        worlds.append(
            {
                "id": supplied["id"],
                "geometry": geometry,
                "membership": membership,
                "histogram": histogram,
                "moments": moments,
                "cq": _cq_rows(membership, instrument),
            }
        )
    _require(
        {key: sum(len(world[key]) for world in worlds) for key in ("membership", "cq", "histogram")}
        == protocol["coverage"],
        "complete prescribed mathematical coverage",
    )
    menus = [
        _menu(supplied, {world["id"]: world for world in worlds}) for supplied in protocol["menus"]
    ]
    controls = _controls(worlds, instrument, mixed_diagonal, protocol)
    report = {
        "schema": "qr05bm-report-v1",
        "quota": quota,
        "worlds": worlds,
        "menus": menus,
        "controls": controls,
    }
    _native_report(report)
    return report
