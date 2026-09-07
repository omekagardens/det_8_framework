"""QR-05V exact predictive value of non-disturbing current-state readouts.

The local constructor is statically carried from this primary's S/U lineage.
All predictions condition explicit current beliefs before the fixed future
kernel. No raw order, artifact or other executor is imported or read.
"""

import hashlib
import json
from fractions import Fraction
from math import comb, gcd

BIT_LIMIT = 4096
INPUT_BITS = 64
CLASS_CAP = 512
CLASS_LOCAL_CAP = 3072
PROFILE_ATOM_CAP = 32768
WORKING_CAP = 512 * 1024 * 1024
DEPTH_LIMIT = 128
BELIEF_CAP = 512
POSTERIOR_CAP = 262144
CELL_CAP = 32768
READOUT_POSTERIOR_CAP = 786432
PREDICTION_CAP = 1048576


def _native(value):
    """Validate the object graph and bound its expanded JSON value tree.

    Completed containers are memoized, while an active-path check still
    rejects cycles. Repeated child references contribute repeatedly to the
    tree-node count: deduplicating validation must not hide exponential JSON
    expansion. Each native value node occupies at least one serialized byte,
    so this preflight only rejects values already above the working byte cap.
    """
    active, completed, pending = set(), {}, [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 0
            for child in children:
                if type(child) in (list, dict):
                    child_nodes, child_height = completed[id(child)]
                    nodes += child_nodes
                    height = max(height, child_height + 1)
                else:
                    nodes += 1
                if nodes > WORKING_CAP:
                    raise ValueError("expanded native value tree exceeds the working-output cap")
            active.remove(id(item))
            completed[id(item)] = (nodes, height)
            continue
        if item is None or type(item) in (str, bool):
            if WORKING_CAP < 1:
                raise ValueError("native value exceeds the working-output cap")
            continue
        if type(item) is int:
            if item.bit_length() > BIT_LIMIT:
                raise ValueError("integer exceeds the exact arithmetic bound")
            if WORKING_CAP < 1:
                raise ValueError("native value exceeds the working-output cap")
            continue
        if type(item) not in (list, dict):
            raise ValueError("expected native exact JSON")
        if depth > DEPTH_LIMIT or id(item) in active:
            raise ValueError("native JSON is cyclic or exceeds the bounded schema depth")
        if id(item) in completed:
            if depth + completed[id(item)][1] > DEPTH_LIMIT:
                raise ValueError("native JSON exceeds the bounded schema depth")
            continue
        if type(item) is dict and any(type(key) is not str for key in item):
            raise ValueError("wire dictionary keys must be native strings")
        if 1 + len(item) > WORKING_CAP:
            raise ValueError("native value tree exceeds the working-output cap")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if type(item) is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))


def canonical(value):
    _native(value)
    encoded = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    if len(encoded) > WORKING_CAP:
        raise ValueError("retained exact JSON exceeds the working-output cap")
    return encoded


def _digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _fields(value, keys):
    if (
        type(value) is not dict
        or any(type(key) is not str for key in value)
        or set(value) != set(keys)
    ):
        raise ValueError("unexpected native object fields")


def _integer(value, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum or value.bit_length() > BIT_LIMIT:
        raise ValueError("native integer outside the declared bound")


def _choose(total, selected):
    return comb(total, selected) if total >= 0 and 0 <= selected <= total else 0


def _colors(value):
    if type(value) is not list or len(value) != 2:
        raise ValueError("color sizes must be two native integers")
    for size in value:
        _integer(size, 0, 3)
    return tuple(value)


def _validated_local(local_model):
    _native(local_model)
    _fields(local_model, ("schema_version", "classes"))
    if local_model["schema_version"] != "det8-qr05s-local-v1":
        raise ValueError("unknown local-model schema")
    classes = local_model["classes"]
    if type(classes) is not list or not 1 <= len(classes) <= CLASS_CAP:
        raise ValueError("local class count outside its resource bound")
    atoms = 0
    for class_id, row in enumerate(classes):
        _fields(row, ("class_id", "frame_id", "parent_color_sizes", "odd", "even"))
        _integer(row["class_id"], class_id, class_id)
        _integer(row["frame_id"], 0, 1)
        sizes = _colors(row["parent_color_sizes"])
        for color, name in enumerate(("odd", "even")):
            edges = row[name]
            if type(edges) is not list or len(edges) > 3:
                raise ValueError("each local color row has at most three atoms")
            previous, total = -1, 0
            for edge in edges:
                _fields(edge, ("target_class", "multiplicity"))
                _integer(edge["target_class"], previous + 1, len(classes) - 1)
                previous = edge["target_class"]
                _integer(edge["multiplicity"], 1, 3)
                total += edge["multiplicity"]
            if total != sizes[color]:
                raise ValueError("local row total differs from its parent color population")
            atoms += len(edges)
    if atoms > CLASS_LOCAL_CAP:
        raise ValueError("class-local atom resource cap exceeded")
    for row in classes:
        for color, name in enumerate(("odd", "even")):
            for edge in row[name]:
                target = classes[edge["target_class"]]
                expected = list(row["parent_color_sizes"])
                expected[color] -= 1
                if (
                    target["frame_id"] != row["frame_id"]
                    or target["parent_color_sizes"] != expected
                ):
                    raise ValueError(
                        "a local deletion must preserve frame and lower exactly one color"
                    )
    return json.loads(canonical(classes))


def _operator_product(classes, source, first, second):
    result = {}
    for edge in classes[source][first]:
        for following in classes[edge["target_class"]][second]:
            target = following["target_class"]
            result[target] = (
                result.get(target, 0) + edge["multiplicity"] * following["multiplicity"]
            )
    return result


def _operator_checks(classes, profiles):
    rows = []
    fields = (
        "odd_odd_targets",
        "even_even_targets",
        "mixed_targets",
        "coefficient_cells",
        "odd_odd_pairs",
        "even_even_pairs",
        "mixed_pairs",
        "max_abs_residual",
    )
    totals = {name: 0 for name in fields}
    for row, profile in zip(classes, profiles, strict=True):
        source = row["class_id"]
        odd, even = row["parent_color_sizes"]
        oo = _operator_product(classes, source, "odd", "odd")
        ee = _operator_product(classes, source, "even", "even")
        oe = _operator_product(classes, source, "odd", "even")
        eo = _operator_product(classes, source, "even", "odd")
        expected_oo, expected_ee, expected_mixed = {}, {}, {}
        for atom in profile["transitions"]:
            target, rank, count = (
                atom["target_class"],
                atom["retained_color_sizes"],
                atom["multiplicity"],
            )
            if rank == [odd - 2, even]:
                expected_oo[target] = 2 * count
            if rank == [odd, even - 2]:
                expected_ee[target] = 2 * count
            if rank == [odd - 1, even - 1]:
                expected_mixed[target] = count
        if oo != expected_oo or ee != expected_ee:
            raise ValueError("same-color deletion words disagree with the factor-two subset count")
        if oe != eo or oe != expected_mixed:
            raise ValueError("mixed deletion orders disagree with each other or the subset count")
        pairs = [sum(oo.values()), sum(ee.values()), sum(oe.values())]
        if pairs != [odd * (odd - 1), even * (even - 1), odd * even]:
            raise ValueError("local two-deletion row masses are incorrect")
        counts = {
            "class_id": source,
            "odd_odd_targets": len(oo),
            "even_even_targets": len(ee),
            "mixed_targets": len(oe),
            "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
            "odd_odd_pairs": pairs[0],
            "even_even_pairs": pairs[1],
            "mixed_pairs": pairs[2],
            "max_abs_residual": 0,
        }
        rows.append(counts)
        for name in fields:
            totals[name] += counts[name]
    return {"verified": True, "rows": rows, "totals": totals}


def reconstruct_profiles(local_model):
    """Reconstruct all subset counts from local rows alone, by rank induction.

    No raw observations or full-profile oracle are received or consulted.
    This is structural and algebraic validation, not an authentication of the
    class names or a guarantee of realization in an observed-order domain.
    """
    classes = _validated_local(local_model)
    size = len(classes)
    dense = [None] * size
    profiles = [None] * size
    base_cells, recurrence_cells, atoms = 0, 0, 0
    order = sorted(range(size), key=lambda i: (sum(classes[i]["parent_color_sizes"]), i))
    for source in order:
        row = classes[source]
        odd, even = row["parent_color_sizes"]
        values = [0] * size
        for target, following in enumerate(classes):
            m, n = following["parent_color_sizes"]
            if row["frame_id"] != following["frame_id"] or m > odd or n > even:
                continue
            if m == odd and n == even:
                values[target] = int(source == target)
                base_cells += 1
                continue
            odd_sum, even_sum = None, None
            if odd > m:
                odd_sum = 0
                for edge in row["odd"]:
                    child = dense[edge["target_class"]]
                    if child is None:
                        raise ValueError("smaller-parent induction used an unprocessed class")
                    odd_sum += edge["multiplicity"] * child[target]
                if odd_sum < 0 or odd_sum % (odd - m):
                    raise ValueError("odd recurrence is not exactly nonnegative integer divisible")
                recurrence_cells += 1
            if even > n:
                even_sum = 0
                for edge in row["even"]:
                    child = dense[edge["target_class"]]
                    if child is None:
                        raise ValueError("smaller-parent induction used an unprocessed class")
                    even_sum += edge["multiplicity"] * child[target]
                if even_sum < 0 or even_sum % (even - n):
                    raise ValueError("even recurrence is not exactly nonnegative integer divisible")
                recurrence_cells += 1
            count = odd_sum // (odd - m) if odd_sum is not None else even_sum // (even - n)
            if odd_sum is not None and even_sum is not None and even_sum != (even - n) * count:
                raise ValueError("odd and even reconstruction recurrences disagree")
            _integer(count, 0, min(9, _choose(odd, m) * _choose(even, n)))
            values[target] = count
        totals = [[0] * 4 for _ in range(4)]
        transitions = []
        for target, count in enumerate(values):
            m, n = classes[target]["parent_color_sizes"]
            totals[m][n] += count
            if count:
                transitions.append(
                    {
                        "target_class": target,
                        "retained_color_sizes": [m, n],
                        "multiplicity": count,
                    }
                )
        if totals != [[_choose(odd, m) * _choose(even, n) for n in range(4)] for m in range(4)]:
            raise ValueError("reconstructed counts do not satisfy rankwise binomial normalization")
        if len(transitions) > 64:
            raise ValueError("one class profile exceeds its subset atom bound")
        atoms += len(transitions)
        if atoms > PROFILE_ATOM_CAP:
            raise ValueError("reconstructed profile atom resource cap exceeded")
        dense[source] = values
        profiles[source] = {
            "class_id": source,
            "parent_color_sizes": [odd, even],
            "transitions": transitions,
        }
    if any(row is None for row in profiles):
        raise ValueError("class induction did not fill the full domain")
    result = {
        "profiles": profiles,
        "certificate": {
            "target_cells": size * size,
            "base_cells": base_cells,
            "recurrence_cells": recurrence_cells,
            "normalization_cells": 16 * size,
            "max_abs_residual": 0,
        },
        "operator_checks": _operator_checks(classes, profiles),
    }
    canonical(result)
    return result


READOUTS = ("N", "NMT", "H")
REFINEMENTS = (("baseline", "N"), ("N", "NMT"), ("NMT", "H"))


def _fraction(value, *, positive=False, rate=False):
    if type(value) is not list or len(value) != 2:
        raise ValueError("a probability must be a native fraction pair")
    numerator, denominator = value
    bits = INPUT_BITS if rate else BIT_LIMIT
    _integer(numerator, int(positive), (1 << bits) - 1)
    _integer(denominator, 1, (1 << bits) - 1)
    if numerator > denominator or gcd(numerator, denominator) != 1:
        raise ValueError("probability must be reduced and within the unit interval")
    return Fraction(numerator, denominator)


def _checked(value):
    if (
        type(value) is not Fraction
        or not 0 <= value <= 1
        or max(value.numerator.bit_length(), value.denominator.bit_length()) > BIT_LIMIT
    ):
        raise ValueError("derived probability/risk exceeds its exact bound")
    return value


def _pair(value):
    _checked(value)
    return [value.numerator, value.denominator]


def _sum(values):
    result = Fraction(0)
    for value in values:
        result = _checked(result + value)
    return result


def _add_mass(mapping, key, mass):
    _checked(mass)
    if mass:
        mapping[key] = _checked(mapping.get(key, Fraction(0)) + mass)


def _unit(mapping, message):
    if not mapping or any(not p for p in mapping.values()) or _sum(mapping.values()) != 1:
        raise ValueError(message)


def _belief_wire(belief):
    return [{"class_id": h, "probability": _pair(p)} for h, p in sorted(belief.items()) if p]


def _question_wire(law):
    return [{"value": list(q), "probability": _pair(p)} for q, p in sorted(law.items()) if p]


def _kernel(profiles, rate):
    x, y = rate
    rows, monomials = [], {}
    for profile in profiles:
        odd, even = profile["parent_color_sizes"]
        row = {}
        for atom in profile["transitions"]:
            m, n = atom["retained_color_sizes"]
            key = odd, even, m, n
            if key not in monomials:
                monomials[key] = _checked(
                    x**m * (1 - x) ** (odd - m) * y**n * (1 - y) ** (even - n)
                )
            _add_mass(row, atom["target_class"], _checked(atom["multiplicity"] * monomials[key]))
        _unit(row, "reconstructed class kernel is not stochastic")
        rows.append(row)
    return rows


def _kernel_wire(rows):
    return [
        {
            "class_id": h,
            "transitions": [
                {"target_class": g, "probability": _pair(p)} for g, p in sorted(row.items())
            ],
        }
        for h, row in enumerate(rows)
    ]


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "model", "rate", "beliefs"))
    if (
        problem["schema_version"] != "det8-qr05v-problem-v1"
        or problem["family"] != "qr05v_readout_value"
    ):
        raise ValueError("unknown readout-value investigation")
    _fields(problem["model"], ("classes", "labels"))
    model = json.loads(canonical(problem["model"]))
    reconstructed = reconstruct_profiles(
        {"schema_version": "det8-qr05s-local-v1", "classes": model["classes"]}
    )
    classes, labels = model["classes"], model["labels"]
    if type(labels) is not list or len(labels) != len(classes):
        raise ValueError("labels must cover exactly the supplied local classes")
    values = []
    for h, label in enumerate(labels):
        _fields(label, ("class_id", "observation", "question"))
        _integer(label["class_id"], h, h)
        observation, question = label["observation"], label["question"]
        if (
            type(observation) is not list
            or len(observation) != 5
            or type(question) is not list
            or len(question) != 7
        ):
            raise ValueError("observation/question label dimensions are invalid")
        frame = classes[h]["frame_id"]
        odd, even = classes[h]["parent_color_sizes"]
        _integer(observation[0], frame, frame)
        _integer(observation[1], 1, 1)
        _integer(observation[2], odd + even + frame, odd + even + frame)
        _integer(observation[3], 0, _choose(observation[2], 2))
        _integer(observation[4], 0, _choose(observation[2], 3))
        for index, expected in enumerate(observation):
            _integer(question[index], expected, expected)
        bound = _choose(odd, 2) * _choose(even, 2)
        _integer(question[5], 0, bound)
        _integer(question[6], 0, bound)
        values.append((tuple(observation), tuple(question)))
    supplied_rate = problem["rate"]
    if type(supplied_rate) is not list or len(supplied_rate) != 2:
        raise ValueError("one fixed two-color rate is required")
    rate = tuple(_fraction(pair, rate=True) for pair in supplied_rate)
    supplied_beliefs = problem["beliefs"]
    if type(supplied_beliefs) is not list or not 1 <= len(supplied_beliefs) <= BELIEF_CAP:
        raise ValueError("belief count exceeds the fixed bound")
    beliefs, weights, atoms = [], {}, 0
    for bid, supplied in enumerate(supplied_beliefs):
        _fields(supplied, ("belief_id", "weight", "posterior"))
        _integer(supplied["belief_id"], bid, bid)
        weight = _fraction(supplied["weight"], positive=True)
        posterior = supplied["posterior"]
        if type(posterior) is not list or not 1 <= len(posterior) <= CLASS_CAP:
            raise ValueError("posterior support is outside the declared bound")
        belief, previous = {}, -1
        for atom in posterior:
            _fields(atom, ("class_id", "probability"))
            _integer(atom["class_id"], previous + 1, len(classes) - 1)
            previous = atom["class_id"]
            belief[previous] = _fraction(atom["probability"], positive=True)
        _unit(belief, "current posterior must have exact unit mass")
        atoms += len(belief)
        if atoms > POSTERIOR_CAP:
            raise ValueError("total input posterior atom cap exceeded")
        weights[bid] = weight
        beliefs.append({"belief_id": bid, "weight": weight, "posterior": belief})
    _unit(weights, "supplied case weights must sum exactly to one")
    # Construct all-class maps, including zero-posterior classes.
    nmt_to_n = {}
    for n, nmt in values:
        if nmt in nmt_to_n and nmt_to_n[nmt] != n:
            raise ValueError("global readout nesting is inconsistent")
        if nmt[:5] != n:
            raise ValueError("current NMT does not refine current N")
        nmt_to_n[nmt] = n
    maps = {
        "NMT_to_N": [{"fine": list(v), "coarse": list(nmt_to_n[v])} for v in sorted(nmt_to_n)],
        "H_to_NMT": [{"fine": [h], "coarse": list(value[1])} for h, value in enumerate(values)],
    }
    K = _kernel(reconstructed["profiles"], rate)
    class_laws = []
    for row in K:
        law = {}
        for g, probability in row.items():
            _add_mass(law, values[g][1], probability)
        _unit(law, "fixed future-question pushforward is not normalized")
        class_laws.append(law)
    return {
        "model": model,
        "reconstructed": reconstructed,
        "labels": values,
        "readout_maps": maps,
        "beliefs": beliefs,
        "rate": rate,
        "kernel": K,
        "class_laws": class_laws,
        "posterior_atoms": atoms,
    }


def _mixture(weighted_laws):
    result, weights = {}, []
    for weight, law in weighted_laws:
        _checked(weight)
        weights.append(weight)
        _unit(law, "mixture component must be a positive unit law")
        for value, probability in law.items():
            _add_mass(result, value, _checked(weight * probability))
    if _sum(weights) != 1:
        raise ValueError("mixture weights must sum exactly to one")
    _unit(result, "mixture failed to preserve probability mass")
    return result


def _prediction(belief, class_laws):
    _unit(belief, "prediction requires a normalized current posterior")
    return _mixture((p, class_laws[h]) for h, p in belief.items())


def _risk(law):
    _unit(law, "Brier Bayes risk requires its true normalized law")
    return _checked(1 - sum((p * p for p in law.values()), Fraction(0)))


def _distance(left, right):
    """Unweighted squared distance is not a probability; it can exceed one."""
    return sum(
        (
            (left.get(q, Fraction(0)) - right.get(q, Fraction(0))) ** 2
            for q in left.keys() | right.keys()
        ),
        Fraction(0),
    )


def _weighted_distance(weight, left, right):
    # These terms compare a child law with its weighted-mixture parent.
    return _checked(weight * _distance(left, right))


def _readout_value(name, h, labels):
    if name == "N":
        return labels[h][0]
    if name == "NMT":
        return labels[h][1]
    if name == "H":
        return (h,)
    raise ValueError("unknown fixed readout")


def _readout_cells(belief, name, labels, class_laws):
    groups = {}
    for h, mass in belief.items():
        value = _readout_value(name, h, labels)
        groups.setdefault(value, {})[h] = mass
    cells = []
    for value, joint in sorted(groups.items()):
        weight = _sum(joint.values())
        if not weight:
            continue
        posterior = {h: _checked(mass / weight) for h, mass in joint.items()}
        _unit(posterior, "positive readout cell failed normalization")
        prediction = _prediction(posterior, class_laws)
        cells.append(
            {
                "value": value,
                "probability": weight,
                "posterior": posterior,
                "prediction": prediction,
                "risk": _risk(prediction),
            }
        )
    if _sum(cell["probability"] for cell in cells) != 1:
        raise ValueError("readout probabilities must sum to one")
    return cells


def _cell_wire(cell):
    return {
        "value": list(cell["value"]),
        "probability": _pair(cell["probability"]),
        "posterior": _belief_wire(cell["posterior"]),
        "prediction": _question_wire(cell["prediction"]),
        "risk": _pair(cell["risk"]),
    }


def _readout_score(cells, baseline):
    posterior = _mixture((c["probability"], c["posterior"]) for c in cells)
    prediction = _mixture((c["probability"], c["prediction"]) for c in cells)
    if posterior != baseline["posterior"] or prediction != baseline["prediction"]:
        raise ValueError("readout marginal changed the current belief or future target")
    expected = _sum(_checked(c["probability"] * c["risk"]) for c in cells)
    gain = _checked(baseline["risk"] - expected)
    variance = _sum(
        _weighted_distance(c["probability"], c["prediction"], baseline["prediction"]) for c in cells
    )
    if variance != gain:
        raise ValueError("readout gain differs from its squared-law variance")
    return {
        "cells": [_cell_wire(c) for c in cells],
        "expected_risk": _pair(expected),
        "gain": _pair(gain),
        "variance_gain": _pair(variance),
    }


def _parent_value(coarse, fine_cell, labels):
    if coarse == "baseline":
        return ()
    if coarse == "N":
        return fine_cell["value"][:5]
    if coarse == "NMT":
        return labels[fine_cell["value"][0]][1]
    raise ValueError("unknown adjacent readout refinement")


def _refinement(coarse, fine, parents, children, labels):
    parent_index = {cell["value"]: cell for cell in parents}
    grouped = {}
    for child in children:
        value = _parent_value(coarse, child, labels)
        if value not in parent_index:
            raise ValueError("positive child has no declared coarse readout parent")
        grouped.setdefault(value, []).append(child)
    if grouped.keys() != parent_index.keys():
        raise ValueError("positive coarse cell is missing its children")
    checks, conditional_drops, conditional_variances = [], [], []
    all_equal = True
    for parent in parents:
        siblings = grouped[parent["value"]]
        if _sum(c["probability"] for c in siblings) != parent["probability"]:
            raise ValueError("child masses do not sum to their coarse parent")
        alphas = [_checked(c["probability"] / parent["probability"]) for c in siblings]
        posterior = _mixture((a, c["posterior"]) for a, c in zip(alphas, siblings, strict=True))
        prediction = _mixture((a, c["prediction"]) for a, c in zip(alphas, siblings, strict=True))
        if posterior != parent["posterior"] or prediction != parent["prediction"]:
            raise ValueError("nested posterior or complete future mixture differs")
        risk = _sum(_checked(a * c["risk"]) for a, c in zip(alphas, siblings, strict=True))
        drop = _checked(parent["risk"] - risk)
        variance = _sum(
            _weighted_distance(a, c["prediction"], parent["prediction"])
            for a, c in zip(alphas, siblings, strict=True)
        )
        equal = all(c["prediction"] == parent["prediction"] for c in siblings)
        if drop != variance or (drop == 0) != equal:
            raise ValueError("conditional refinement gain or zero-gain characterization failed")
        all_equal = equal and all_equal
        conditional_drops.append(_checked(parent["probability"] * drop))
        conditional_variances.append(_checked(parent["probability"] * variance))
        checks.append(
            {
                "value": list(parent["value"]),
                "probability": _pair(parent["probability"]),
                "fine_values": [list(c["value"]) for c in siblings],
                "mixture_sha256": _digest(_question_wire(prediction)),
                "conditional_risk_drop": _pair(drop),
                "conditional_variance_gain": _pair(variance),
                "predictions_equal": equal,
            }
        )
    coarse_risk = _sum(_checked(c["probability"] * c["risk"]) for c in parents)
    fine_risk = _sum(_checked(c["probability"] * c["risk"]) for c in children)
    drop, variance = _sum(conditional_drops), _sum(conditional_variances)
    if drop != coarse_risk - fine_risk or variance != drop or (drop == 0) != all_equal:
        raise ValueError("global refinement risk identity failed")
    return {
        "coarse": coarse,
        "fine": fine,
        "risk_drop": _pair(drop),
        "variance_gain": _pair(variance),
        "parent_checks": checks,
        "zero_gain_iff_equal": True,
    }


def _belief_result(row, prepared, class_risks):
    belief = row["posterior"]
    prediction = _prediction(belief, prepared["class_laws"])
    baseline = {
        "value": (),
        "probability": Fraction(1),
        "posterior": belief,
        "prediction": prediction,
        "risk": _risk(prediction),
    }
    cells = {"baseline": [baseline]}
    readouts = {}
    for name in READOUTS:
        cells[name] = _readout_cells(belief, name, prepared["labels"], prepared["class_laws"])
        readouts[name] = _readout_score(cells[name], baseline)
    refinements = [
        _refinement(coarse, fine, cells[coarse], cells[fine], prepared["labels"])
        for coarse, fine in REFINEMENTS
    ]
    oracle = _sum(_checked(p * class_risks[h]) for h, p in belief.items())
    if oracle != _fraction(readouts["H"]["expected_risk"]):
        raise ValueError("H residual differs from the independent class-wise future risk")
    gains = [_fraction(item["risk_drop"]) for item in refinements]
    if _sum(gains) != _fraction(readouts["H"]["gain"]):
        raise ValueError("adjacent gains do not telescope to the oracle gain")
    previous = baseline["risk"]
    for name in READOUTS:
        risk = _fraction(readouts[name]["expected_risk"])
        if risk > previous:
            raise ValueError("nested readout risks are not ordered")
        previous = risk
    return {
        "belief_id": row["belief_id"],
        "weight": _pair(row["weight"]),
        "posterior": _belief_wire(belief),
        "baseline": {"prediction": _question_wire(prediction), "risk": _pair(baseline["risk"])},
        "readouts": readouts,
        "refinements": refinements,
        "oracle_residual": _pair(oracle),
        "checks": {
            "probabilities_normalized": True,
            "marginal_future_preserved": True,
            "nested_mixtures": True,
            "nested_risks": True,
            "oracle_residual_identity": True,
            "gains_telescope": True,
            "N_already_known": len(cells["N"]) == 1,
        },
    }


def _law_from_wire(atoms):
    return {tuple(atom["value"]): _fraction(atom["probability"], positive=True) for atom in atoms}


def _aggregate(rows):
    weights = [_fraction(row["weight"], positive=True) for row in rows]
    total = _sum(weights)
    if total != 1:
        raise ValueError("case aggregation requires exact normalized history weights")
    prediction = _mixture(
        (weight, _law_from_wire(row["baseline"]["prediction"]))
        for weight, row in zip(weights, rows, strict=True)
    )
    # History has already been received: average conditional risks, not the
    # Bayes risk of the mixture that would forget which history occurred.
    baseline = _sum(
        _checked(weight * _fraction(row["baseline"]["risk"]))
        for weight, row in zip(weights, rows, strict=True)
    )
    expected, gains = {}, {}
    for name in READOUTS:
        risk = _sum(
            _checked(weight * _fraction(row["readouts"][name]["expected_risk"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        gain = _sum(
            _checked(weight * _fraction(row["readouts"][name]["gain"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        if baseline - risk != gain:
            raise ValueError("weighted aggregate risk/gain identity failed")
        expected[name], gains[name] = _pair(risk), _pair(gain)
    adjacent = [
        _sum(
            _checked(weight * _fraction(row["refinements"][index]["risk_drop"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        for index in range(len(REFINEMENTS))
    ]
    oracle = _sum(
        _checked(weight * _fraction(row["oracle_residual"]))
        for weight, row in zip(weights, rows, strict=True)
    )
    previous = baseline
    for name, gain in zip(READOUTS, adjacent, strict=True):
        risk = _fraction(expected[name])
        if risk > previous or previous - risk != gain:
            raise ValueError("case-weighted nesting failed")
        previous = risk
    if oracle != _fraction(expected["H"]) or _sum(adjacent) != _fraction(gains["H"]):
        raise ValueError("case-weighted oracle or telescope identity failed")
    return {
        "total_weight": _pair(total),
        "prediction": _question_wire(prediction),
        "baseline_risk": _pair(baseline),
        "expected_risk": expected,
        "gain": gains,
        "adjacent_gain": [_pair(gain) for gain in adjacent],
        "oracle_residual": _pair(oracle),
    }


def analyze(problem):
    prepared = _prepare(problem)
    class_risks = [_risk(law) for law in prepared["class_laws"]]
    rows = []
    cells = {name: 0 for name in READOUTS}
    posterior_atoms = {name: 0 for name in READOUTS}
    prediction_atoms = {name: 0 for name in READOUTS}
    parents = [0] * len(REFINEMENTS)
    strict = {name: 0 for name in READOUTS}
    no_gain = {name: 0 for name in READOUTS}
    witnesses = {
        "first_strict": [None] * len(REFINEMENTS),
        "first_zero": [None] * len(REFINEMENTS),
        "first_positive_oracle_residual": None,
        "first_zero_oracle_residual": None,
    }
    positive_oracle, known_n = 0, 0
    for belief in prepared["beliefs"]:
        row = _belief_result(belief, prepared, class_risks)
        bid = row["belief_id"]
        rows.append(row)
        for name in READOUTS:
            current = row["readouts"][name]
            cells[name] += len(current["cells"])
            posterior_atoms[name] += sum(len(c["posterior"]) for c in current["cells"])
            prediction_atoms[name] += sum(len(c["prediction"]) for c in current["cells"])
            gain = _fraction(current["gain"])
            strict[name] += int(gain > 0)
            no_gain[name] += int(gain == 0)
        if sum(cells.values()) > CELL_CAP:
            raise ValueError("retained readout cell cap exceeded")
        if sum(posterior_atoms.values()) > READOUT_POSTERIOR_CAP:
            raise ValueError("retained readout posterior atom cap exceeded")
        if sum(prediction_atoms.values()) > PREDICTION_CAP:
            raise ValueError("retained readout prediction atom cap exceeded")
        for index, refinement in enumerate(row["refinements"]):
            parents[index] += len(refinement["parent_checks"])
            field = "first_strict" if _fraction(refinement["risk_drop"]) > 0 else "first_zero"
            if witnesses[field][index] is None:
                witnesses[field][index] = bid
        residual = _fraction(row["oracle_residual"])
        field = "first_positive_oracle_residual" if residual > 0 else "first_zero_oracle_residual"
        if witnesses[field] is None:
            witnesses[field] = bid
        positive_oracle += int(residual > 0)
        known_n += int(row["checks"]["N_already_known"])
    reconstructed = prepared["reconstructed"]
    profile_atoms = sum(len(row["transitions"]) for row in reconstructed["profiles"])
    result = {
        "model_sha256": _digest(prepared["model"]),
        "reconstruction": {
            "profiles_sha256": _digest(reconstructed["profiles"]),
            "profile_atoms": profile_atoms,
            "certificate": reconstructed["certificate"],
            "operator_checks": reconstructed["operator_checks"],
        },
        "rate": [_pair(p) for p in prepared["rate"]],
        "kernel_sha256": _digest(_kernel_wire(prepared["kernel"])),
        "readout_maps": prepared["readout_maps"],
        "beliefs": rows,
        "aggregate": _aggregate(rows),
        "witnesses": witnesses,
        "counts": {
            "classes": len(prepared["labels"]),
            "beliefs": len(rows),
            "profile_atoms": profile_atoms,
            "kernel_atoms": sum(len(row) for row in prepared["kernel"]),
            "posterior_atoms": prepared["posterior_atoms"],
            "readout_cells": cells,
            "readout_posterior_atoms": posterior_atoms,
            "readout_prediction_atoms": prediction_atoms,
            "refinement_parents": parents,
            "strict_gain_beliefs": strict,
            "no_gain_beliefs": no_gain,
            "positive_oracle_residual_beliefs": positive_oracle,
            "known_N_beliefs": known_n,
        },
    }
    return json.loads(canonical(result))
