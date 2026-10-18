"""Independent QR-05BM Simpson, interpolation and classical-record route.

This module performs no fixed computation on import and reads no files.
The metric and sampling formulas are shared model data, not answer tables.
"""

from fractions import Fraction
from itertools import product


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _validate_protocol(protocol):
    """Admit precisely the native, prospectively fixed finite experiment."""
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
    # Parallel traversal of a finite expected tree bounds work and cannot
    # follow an attacker-supplied cycle indefinitely. Shared native input
    # containers are harmless when their complete values match this tree.
    pending = [(protocol, expected)]
    while pending:
        actual, wanted = pending.pop()
        _require(type(actual) is type(wanted), "protocol native type differs")
        if type(wanted) is dict:
            _require(
                all(type(key) is str for key in actual) and set(actual) == set(wanted),
                "protocol fields differ",
            )
            pending.extend((actual[key], value) for key, value in wanted.items())
        elif type(wanted) is list:
            _require(len(actual) == len(wanted), "protocol list length differs")
            pending.extend(zip(actual, wanted))
        else:
            _require(actual == wanted, "fixed protocol value differs")


def _rectangle(encoded):
    values = [Fraction(pair[0], pair[1]) for pair in encoded]
    _require(len(values) == 4, "rectangle width")
    _require(values[0] < values[1] and values[2] < values[3], "positive rectangle")
    return values


def _quadrature_axis(lower, upper):
    _require(type(lower) is Fraction and type(upper) is Fraction, "rational quadrature bounds")
    _require(lower < upper, "positive quadrature interval")
    return ((lower, 1), ((lower + upper) / 2, 4), (upper, 1))


def _integrate(function, rectangle):
    """Tensor Simpson: each coordinate degree is at most two here."""
    left, right, bottom, top = rectangle
    total = Fraction(0)
    for x, wx in _quadrature_axis(left, right):
        for y, wy in _quadrature_axis(bottom, top):
            value = function(x, y)
            _require(type(value) is Fraction, "exact quadrature value")
            total += wx * wy * value
    return (right - left) * (top - bottom) * total / 36


def _quadratic_coefficients(values):
    """Recover power coefficients from values at zero, one and two."""
    zero, one, two = values
    quadratic = (two - 2 * one + zero) / 2
    linear = one - zero - quadratic
    return [zero, linear, quadratic]


def _polynomial(function):
    """Independent tensor interpolation; no monomial-product construction."""
    nodes = [Fraction(0), Fraction(1), Fraction(2)]
    first_axis = [_quadratic_coefficients([function(x, y) for x in nodes]) for y in nodes]
    result = []
    for i in range(3):
        column = _quadratic_coefficients([row[i] for row in first_axis])
        for j, coefficient in enumerate(column):
            _require(type(coefficient) is Fraction, "exact interpolated coefficient")
            if coefficient:
                result.append([i, j, coefficient])
    return result


def _at(polynomial, x, y):
    return sum((value * x**i * y**j for i, j, value in polynomial), Fraction(0))


def _density_functions(world, scales, offsets):
    scale, eta, delta = (Fraction(world[name]) for name in ("scale", "eta", "density_uv"))
    a, b = scales
    c, d = offsets
    _require(a > 0 and b > 0, "orientation-preserving chart")

    def metric(x, y):
        u, v = (x - c) / a, (y - d) / b
        return scale * (1 + eta * u * v) / (a * b)

    def density(x, y):
        u, v = (x - c) / a, (y - d) / b
        return 1 + delta * u * v

    def proper(x, y):
        return metric(x, y) / 2

    def weighted(x, y):
        return proper(x, y) * density(x, y)

    return {"metric": metric, "density": density, "proper": proper, "weighted": weighted}


def _chart_rectangle(rectangle, scales, offsets):
    a, b = scales
    c, d = offsets
    return [a * rectangle[0] + c, a * rectangle[1] + c, b * rectangle[2] + d, b * rectangle[3] + d]


def _coordinate_geometry(world, regions, scales, offsets, suffix):
    functions = _density_functions(world, scales, offsets)
    transported = {
        key: _chart_rectangle(rectangle, scales, offsets) for key, rectangle in regions.items()
    }
    volume_q = _integrate(functions["proper"], transported["Q"])
    volume_i = _integrate(functions["proper"], transported["I"])
    mass_q = _integrate(functions["weighted"], transported["Q"])
    mass_i = _integrate(functions["weighted"], transported["I"])
    _require(0 < volume_i < volume_q and 0 < mass_i < mass_q, "proper subinterval measures")

    def normalized(x, y):
        return functions["weighted"](x, y) / mass_q

    functions["normalized"] = normalized
    result = {}
    for name, function in functions.items():
        polynomial = _polynomial(function)
        # These checks use physical quadrature nodes, distinct from the
        # coefficient-recovery nodes. Integrals still use the direct formula.
        for rectangle in transported.values():
            for x, _ in _quadrature_axis(rectangle[0], rectangle[1]):
                for y, _ in _quadrature_axis(rectangle[2], rectangle[3]):
                    _require(_at(polynomial, x, y) == function(x, y), "density interpolation")
        result[name + "_" + suffix] = polynomial
    _require(_integrate(normalized, transported["Q"]) == 1, "normalized point measure")
    result.update(
        {
            "volume_Q": volume_q,
            "volume_I": volume_i,
            "mass_Q": mass_q,
            "mass_I": mass_i,
            "target": volume_i / volume_q,
            "q": mass_i / mass_q,
        }
    )
    return result


def _geometry(world, regions, chart):
    result = _coordinate_geometry(
        world, regions, [Fraction(1), Fraction(1)], [Fraction(0), Fraction(0)], "uv"
    )
    scales = [Fraction(chart["U_scale"]), Fraction(chart["V_scale"])]
    offsets = [Fraction(chart["U_offset"]), Fraction(chart["V_offset"])]
    result["chart"] = _coordinate_geometry(world, regions, scales, offsets, "UV")
    return result


def _product(values):
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def _membership(q, quota):
    rows = []
    for word in product((0, 1), repeat=quota):
        probability = _product(q if bit else 1 - q for bit in word)
        count = sum(word)
        rows.append(
            {"y": list(word), "k": count, "p": probability, "estimate": Fraction(count, quota)}
        )
    _require(sum((row["p"] for row in rows), Fraction(0)) == 1, "membership normalization")
    _require(all(row["p"] > 0 for row in rows), "common positive finite-word support")
    return rows


def _histogram(membership, quota):
    histogram = []
    for k in range(quota + 1):
        members = [row for row in membership if row["k"] == k]
        histogram.append(
            {
                "k": k,
                "multiplicity": len(members),
                "p": sum((row["p"] for row in members), Fraction(0)),
            }
        )
        _require(
            all(row["p"] == members[0]["p"] for row in members),
            "equal probability within each count fiber",
        )
    _require(sum(row["multiplicity"] for row in histogram) == len(membership), "count census")
    _require(sum((row["p"] for row in histogram), Fraction(0)) == 1, "count normalization")
    return histogram


def _moments(membership, q, target, quota):
    mean = sum((row["p"] * row["estimate"] for row in membership), Fraction(0))
    variance = sum((row["p"] * (row["estimate"] - mean) ** 2 for row in membership), Fraction(0))
    _require(mean == q and variance == q * (1 - q) / quota, "iid moment identity")
    return {"mean": mean, "variance": variance, "bias": mean - target}


def _cq(membership, quota):
    basis = list(product((0, 1), repeat=quota))
    templates = []
    for signs in product((-1, 1), repeat=quota):
        selected_bits = tuple((1 - sign) // 2 for sign in signs)
        # A computational-basis ket is built directly from bit indicators;
        # its outer-product diagonal specifies the full rank-one state.
        amplitudes = [Fraction(int(bits == selected_bits)) for bits in basis]
        conditional = [amplitude * amplitude for amplitude in amplitudes]
        _require(sum(conditional, Fraction(0)) == 1, "normalized basis outer product")
        fair_probability = _product(Fraction(1, 2) for _ in signs)
        templates.append((list(signs), fair_probability, conditional))
    rows = []
    for member in membership:
        for signs, fair_probability, conditional in templates:
            probability = member["p"] * fair_probability
            diagonal = [probability * value for value in conditional]
            trace = sum(diagonal, Fraction(0))
            _require(probability == trace and probability > 0, "classical/branch trace agreement")
            _require([value / trace for value in diagonal] == conditional, "conditional branch")
            rows.append(
                {
                    "y": list(member["y"]),
                    "z": list(signs),
                    "p": probability,
                    "trace": trace,
                    "diagonal": diagonal,
                    "conditional_diagonal": list(conditional),
                }
            )
    _require(sum((row["p"] for row in rows), Fraction(0)) == 1, "joint CQ normalization")
    return rows


def _law(world, field):
    return [row["p"] for row in world[field]]


def _classes(worlds, field):
    classes = []
    representatives = []
    for world in worlds:
        law = _law(world, field)
        destination = next((j for j, old in enumerate(representatives) if old == law), None)
        if destination is None:
            representatives.append(law)
            classes.append({"worlds": [], "targets": [], "identified": False})
            destination = len(classes) - 1
        group = classes[destination]
        group["worlds"].append(world["id"])
        target = world["geometry"]["target"]
        if target not in group["targets"]:
            group["targets"].append(target)
    for group in classes:
        group["targets"].sort()
        group["identified"] = len(group["targets"]) == 1
    return classes


def _menus(descriptors, worlds):
    index = {world["id"]: world for world in worlds}
    menus = []
    for descriptor in descriptors:
        selected = [index[identifier] for identifier in descriptor["worlds"]]
        classes = _classes(selected, "membership")
        cq_classes = _classes(selected, "cq")
        _require(classes == cq_classes, "inert CQ law classification")
        support = []
        for row_index, row in enumerate(selected[0]["membership"]):
            compatible = [
                world["id"] for world in selected if world["membership"][row_index]["p"] > 0
            ]
            support.append({"y": list(row["y"]), "worlds": compatible})
            _require(compatible == descriptor["worlds"], "finite words do not eliminate worlds")
        menus.append(
            {
                "id": descriptor["id"],
                "worlds": list(descriptor["worlds"]),
                "classes": classes,
                "cq_classes": cq_classes,
                "identified": all(group["identified"] for group in classes),
                "support": support,
            }
        )
    return menus


def _controls(worlds):
    index = {world["id"]: world for world in worlds}
    a, b, c = (index[key] for key in ("A", "B", "C"))
    density_equal = (
        b["geometry"]["weighted_uv"] == c["geometry"]["weighted_uv"]
        and b["geometry"]["mass_Q"] == c["geometry"]["mass_Q"]
    )
    target_gap = c["geometry"]["target"] - b["geometry"]["target"]
    _require(density_equal and target_gap != 0, "whole-point-law geometric-target collision")
    _require(
        b["geometry"]["normalized_uv"] == c["geometry"]["normalized_uv"],
        "density collision normalized point law",
    )
    _require(_law(b, "membership") == _law(c, "membership"), "density collision record law")
    _require(
        a["geometry"]["target"] != b["geometry"]["target"]
        and _law(a, "membership") != _law(b, "membership"),
        "positive-menu distinction",
    )
    _require(a["moments"]["bias"] == b["moments"]["bias"] == 0, "uniform sampler unbiasedness")
    scale_pairs = []
    for first, second in (("A", "D"), ("B", "E")):
        old, new = index[first], index[second]
        g0, g1 = old["geometry"], new["geometry"]
        factor = g1["volume_Q"] / g0["volume_Q"]
        _require(
            factor == 4 and g1["volume_I"] == factor * g0["volume_I"],
            "declared metric-volume scale",
        )
        row = {
            "worlds": [first, second],
            "volume_factor": factor,
            "normalized_equal": g0["normalized_uv"] == g1["normalized_uv"],
            "target_equal": g0["target"] == g1["target"],
            "law_equal": _law(old, "membership") == _law(new, "membership"),
            "cq_equal": old["cq"] == new["cq"],
        }
        _require(
            all(row[key] for key in ("normalized_equal", "target_equal", "law_equal", "cq_equal")),
            "normalized scale invariance",
        )
        scale_pairs.append(row)
    scalar_fields = ("volume_Q", "volume_I", "mass_Q", "mass_I", "target", "q")
    chart_invariant = []
    conditionals = {}
    marginals_match = True
    conditionals_common = True
    for world in worlds:
        geometry = world["geometry"]
        agrees = all(geometry[key] == geometry["chart"][key] for key in scalar_fields)
        _require(agrees, "passive chart preserves every volume and mass")
        chart_invariant.append(world["id"])
        marginal = {tuple(row["y"]): Fraction(0) for row in world["membership"]}
        for row in world["cq"]:
            marginal[tuple(row["y"])] += row["p"]
            key = tuple(row["z"])
            if key not in conditionals:
                conditionals[key] = row["conditional_diagonal"]
            conditionals_common = (
                conditionals_common and conditionals[key] == row["conditional_diagonal"]
            )
        marginals_match = marginals_match and all(
            marginal[tuple(row["y"])] == row["p"] for row in world["membership"]
        )
    _require(marginals_match and conditionals_common, "complete inert quantum extension")
    return {
        "density_equal": density_equal,
        "density_target_gap": target_gap,
        "scale_pairs": scale_pairs,
        "chart_invariant": chart_invariant,
        "cq_marginals_match": marginals_match,
        "cq_conditionals_common": conditionals_common,
    }


def _native_report(report):
    pending = [report]
    while pending:
        value = pending.pop()
        if type(value) is dict:
            _require(all(type(key) is str for key in value), "native report key")
            pending.extend(value.values())
        elif type(value) is list:
            pending.extend(value)
        else:
            _require(type(value) in (Fraction, int, bool, str), "native report scalar")


def analyze(protocol: dict) -> dict:
    """Compute the complete frozen five-world report without observer access."""
    _validate_protocol(protocol)
    quota = protocol["quota"]
    regions = {name: _rectangle(value) for name, value in protocol["regions"].items()}
    worlds = []
    for descriptor in protocol["worlds"]:
        geometry = _geometry(descriptor, regions, protocol["chart"])
        membership = _membership(geometry["q"], quota)
        worlds.append(
            {
                "id": descriptor["id"],
                "geometry": geometry,
                "membership": membership,
                "histogram": _histogram(membership, quota),
                "moments": _moments(membership, geometry["q"], geometry["target"], quota),
                "cq": _cq(membership, quota),
            }
        )
    for field, expected in protocol["coverage"].items():
        _require(sum(len(world[field]) for world in worlds) == expected, "fixed coverage")
    controls = _controls(worlds)
    menus = _menus(protocol["menus"], worlds)
    report = {
        "schema": "qr05bm-report-v1",
        "quota": quota,
        "worlds": worlds,
        "menus": menus,
        "controls": controls,
    }
    _native_report(report)
    return report
