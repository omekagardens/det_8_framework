"""QR-05W exact predictive value of imperfect current-state reports.

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
READOUT_POSTERIOR_CAP = 1048576
PREDICTION_CAP = 2097152


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
LEVELS = (Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1))
GARBLING_LEVELS = (Fraction(1, 2), Fraction(1, 2), Fraction(1))
CHANNEL_ATOM_CAP = 1048576
COMPOSITION_TERM_CAP = 4194304
COUPLING_CAP = 1048576
RECEIVING_CAP = 32768


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
        problem["schema_version"] != "det8-qr05w-problem-v1"
        or problem["family"] != "qr05w_noisy_readouts"
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


def _channel_rows(fibers, level):
    rows = {}
    for values in fibers.values():
        m = len(values)
        for source in values:
            row = {}
            for target in values:
                probability = _checked((1 - level) * int(source == target) + level / m)
                _add_mass(row, target, probability)
            _unit(row, "replacement channel row is not stochastic")
            rows[source] = row
    return rows


def _channel_wire(rows):
    return [
        {"source": list(source), "transitions": _question_wire(row)}
        for source, row in sorted(rows.items())
    ]


def _channel_model(labels):
    fibers = {}
    for n, a in labels:
        fibers.setdefault(n, set()).add(a)
    fibers = {n: tuple(sorted(values)) for n, values in sorted(fibers.items())}
    expected_atoms = sum(len(values) + 3 * len(values) ** 2 for values in fibers.values())
    expected_terms = sum(len(values) ** 2 + 2 * len(values) ** 3 for values in fibers.values())
    if expected_atoms > CHANNEL_ATOM_CAP:
        raise ValueError("global channel atom cap exceeded")
    if expected_terms > COMPOSITION_TERM_CAP:
        raise ValueError("planned composition product term cap exceeded")
    channels = [_channel_rows(fibers, level) for level in LEVELS]
    garblers = [_channel_rows(fibers, level) for level in GARBLING_LEVELS]
    channel_wires = [_channel_wire(rows) for rows in channels]
    checks, checked_terms = [], 0
    for index, garbler in enumerate(garblers):
        composed, product_terms = {}, 0
        for source, row in sorted(channels[index].items()):
            result = {}
            for middle, earlier_probability in row.items():
                for target, conditional_probability in garbler[middle].items():
                    product_terms += 1
                    _add_mass(
                        result, target, _checked(earlier_probability * conditional_probability)
                    )
            _unit(result, "composed replacement row is not stochastic")
            composed[source] = result
        checked_terms += product_terms
        wire = _channel_wire(composed)
        if wire != channel_wires[index + 1]:
            raise ValueError("full-model replacement composition is incorrect")
        checks.append(
            {
                "from_index": index,
                "to_index": index + 1,
                "garbling_level": _pair(GARBLING_LEVELS[index]),
                "row_comparisons": len(composed),
                "product_terms": product_terms,
                "positive_composed_atoms": sum(len(row) for row in composed.values()),
                "composed_sha256": _digest(wire),
                "exact": True,
            }
        )
    if checked_terms != expected_terms:
        raise ValueError("planned and actual composition work differs")
    counts = [sum(len(row) for row in channel.values()) for channel in channels]
    if sum(counts) != expected_atoms:
        raise ValueError("planned and actual channel atom counts differ")
    return {
        "wire": {
            "alphabet": [
                {"N": list(n), "values": [list(a) for a in values]} for n, values in fibers.items()
            ],
            "channels": [
                {"level": _pair(level), "rows": wire}
                for level, wire in zip(LEVELS, channel_wires, strict=True)
            ],
            "composition_checks": checks,
        },
        "fibers": fibers,
        "channels": channels,
        "garblers": garblers,
        "atom_counts": counts,
    }


def _noisy_cells(belief, channel, labels, class_laws):
    groups = {}
    for h, probability in belief.items():
        for value, conditional in channel[labels[h][1]].items():
            _add_mass(groups.setdefault(value, {}), h, _checked(probability * conditional))
    cells = []
    for value, joint in sorted(groups.items()):
        weight = _sum(joint.values())
        if not weight:
            continue
        posterior = {h: _checked(mass / weight) for h, mass in joint.items()}
        _unit(posterior, "noisy-report posterior is not normalized")
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
        raise ValueError("noisy report probabilities do not sum to one")
    return cells


def _garbling(index, earlier, later, garbler):
    earlier_index = {cell["value"]: cell for cell in earlier}
    later_index = {cell["value"]: cell for cell in later}
    incoming = {value: [] for value in later_index}
    source_marginal, target_marginal, pairs = {}, {}, []
    for source, cell in sorted(earlier_index.items()):
        for target, conditional in sorted(garbler[source].items()):
            probability = _checked(cell["probability"] * conditional)
            if not probability:
                continue
            if target not in later_index:
                raise ValueError("positive coupling has no receiving report")
            pairs.append(
                {"earlier": list(source), "later": list(target), "probability": _pair(probability)}
            )
            if len(pairs) > COUPLING_CAP:
                raise ValueError("report-pair coupling atom cap exceeded")
            _add_mass(source_marginal, source, probability)
            _add_mass(target_marginal, target, probability)
            incoming[target].append((source, probability))
    _unit(source_marginal, "coupling earlier marginal is not normalized")
    _unit(target_marginal, "coupling later marginal is not normalized")
    if source_marginal != {
        value: cell["probability"] for value, cell in earlier_index.items()
    } or target_marginal != {value: cell["probability"] for value, cell in later_index.items()}:
        raise ValueError("coupling report marginal differs from the directly computed channel")
    checks, losses, variances, equalities = [], [], [], []
    for target, cell in sorted(later_index.items()):
        components = incoming[target]
        alphas = [_checked(probability / cell["probability"]) for _, probability in components]
        if _sum(alphas) != 1:
            raise ValueError("reverse-Bayes incoming weights are not normalized")
        posterior = _mixture(
            (alpha, earlier_index[source]["posterior"])
            for alpha, (source, _) in zip(alphas, components, strict=True)
        )
        prediction = _mixture(
            (alpha, earlier_index[source]["prediction"])
            for alpha, (source, _) in zip(alphas, components, strict=True)
        )
        if posterior != cell["posterior"] or prediction != cell["prediction"]:
            raise ValueError(
                "garbling changed its complete conditional posterior or future mixture"
            )
        old_risk = _sum(
            _checked(alpha * earlier_index[source]["risk"])
            for alpha, (source, _) in zip(alphas, components, strict=True)
        )
        loss = _checked(cell["risk"] - old_risk)
        variance = _sum(
            _weighted_distance(alpha, earlier_index[source]["prediction"], prediction)
            for alpha, (source, _) in zip(alphas, components, strict=True)
        )
        compared = [earlier_index[source]["prediction"] == prediction for source, _ in components]
        equal = all(compared)
        if loss != variance or (loss == 0) != equal:
            raise ValueError("conditional garbling loss or zero-loss characterization failed")
        losses.append(_checked(cell["probability"] * loss))
        variances.append(_checked(cell["probability"] * variance))
        equalities.append(equal)
        checks.append(
            {
                "value": list(target),
                "probability": _pair(cell["probability"]),
                "earlier_values": [list(source) for source, _ in components],
                "posterior_mixture_sha256": _digest(_belief_wire(posterior)),
                "prediction_mixture_sha256": _digest(_question_wire(prediction)),
                "conditional_risk_increase": _pair(loss),
                "conditional_variance_loss": _pair(variance),
                "predictions_equal": equal,
            }
        )
        if len(checks) > RECEIVING_CAP:
            raise ValueError("receiving-cell check cap exceeded")
    risk_earlier = _sum(_checked(cell["probability"] * cell["risk"]) for cell in earlier)
    risk_later = _sum(_checked(cell["probability"] * cell["risk"]) for cell in later)
    loss, variance = _sum(losses), _sum(variances)
    if loss != risk_later - risk_earlier or variance != loss or (loss == 0) != all(equalities):
        raise ValueError("expected garbling data-processing identity failed")
    return {
        "from_index": index,
        "to_index": index + 1,
        "garbling_level": _pair(GARBLING_LEVELS[index]),
        "risk_increase": _pair(loss),
        "variance_loss": _pair(variance),
        "couplings": pairs,
        "receiving_checks": checks,
        "zero_loss_iff_equal": True,
    }


def _belief_result(row, prepared, channel_model, class_risks):
    belief = row["posterior"]
    prediction = _prediction(belief, prepared["class_laws"])
    baseline = {
        "value": (),
        "probability": Fraction(1),
        "posterior": belief,
        "prediction": prediction,
        "risk": _risk(prediction),
    }
    n_cells = _readout_cells(belief, "N", prepared["labels"], prepared["class_laws"])
    n_score = _readout_score(n_cells, baseline)
    n_risk = _fraction(n_score["expected_risk"])
    h_risk = _sum(_checked(p * class_risks[h]) for h, p in belief.items())
    if h_risk > n_risk:
        raise ValueError("class-wise oracle risk exceeds current-N risk")
    channel_cells = [
        _noisy_cells(belief, channel, prepared["labels"], prepared["class_laws"])
        for channel in channel_model["channels"]
    ]
    clean_cells = _readout_cells(belief, "NMT", prepared["labels"], prepared["class_laws"])
    if channel_cells[0] != clean_cells:
        raise ValueError("zero replacement differs from the clean NMT experiment")
    n_index = {cell["value"]: cell for cell in n_cells}
    expected_end_values = {value for n in n_index for value in channel_model["fibers"][n]}
    if {cell["value"] for cell in channel_cells[-1]} != expected_end_values:
        raise ValueError("complete replacement omits a positive-fiber output symbol")
    for cell in channel_cells[-1]:
        n = cell["value"][:5]
        parent = n_index[n]
        if (
            cell["probability"] != parent["probability"] / len(channel_model["fibers"][n])
            or cell["posterior"] != parent["posterior"]
            or cell["prediction"] != parent["prediction"]
            or cell["risk"] != parent["risk"]
        ):
            raise ValueError("complete replacement is not information-equivalent to N")
    channels = []
    clean_gain = None
    previous = h_risk
    for index, (level, cells) in enumerate(zip(LEVELS, channel_cells, strict=True)):
        score = _readout_score(cells, baseline)
        risk = _fraction(score["expected_risk"])
        if risk < previous or risk > n_risk or risk > baseline["risk"]:
            raise ValueError("replacement risks violate the declared expected-risk order")
        previous = risk
        added_gain = _checked(n_risk - risk)
        if index == 0:
            clean_gain = added_gain
        retention = _checked(added_gain / clean_gain) if clean_gain else None
        if (added_gain > 0) != (bool(clean_gain) and level < 1):
            raise ValueError("replacement-family strict-gain characterization failed")
        channels.append(
            {
                "level": _pair(level),
                **score,
                "gain_over_N": _pair(added_gain),
                "retained_gain_fraction": None if retention is None else _pair(retention),
            }
        )
    if previous != n_risk:
        raise ValueError("complete-replacement risk differs from N-control risk")
    garblings = [
        _garbling(index, channel_cells[index], channel_cells[index + 1], garbler)
        for index, garbler in enumerate(channel_model["garblers"])
    ]
    losses = [_fraction(edge["risk_increase"]) for edge in garblings]
    if _sum(losses) != clean_gain:
        raise ValueError("adjacent replacement losses do not telescope to clean added gain")
    return {
        "belief_id": row["belief_id"],
        "weight": _pair(row["weight"]),
        "posterior": _belief_wire(belief),
        "baseline": {"prediction": _question_wire(prediction), "risk": _pair(baseline["risk"])},
        "controls": {
            "N": {key: n_score[key] for key in ("cells", "expected_risk", "gain")},
            "H": {
                "expected_risk": _pair(h_risk),
                "gain": _pair(_checked(baseline["risk"] - h_risk)),
            },
        },
        "channels": channels,
        "garblings": garblings,
        "checks": {
            "probabilities_normalized": True,
            "marginal_current_preserved": True,
            "marginal_future_preserved": True,
            "garbling_marginals": True,
            "conditional_mixtures": True,
            "risk_order": True,
            "endpoint_information_equivalence": True,
            "losses_telescope": True,
            "N_already_known": len(n_cells) == 1,
        },
    }


def _law_from_wire(atoms):
    return {tuple(atom["value"]): _fraction(atom["probability"], positive=True) for atom in atoms}


def _aggregate(rows):
    weights = [_fraction(row["weight"], positive=True) for row in rows]
    total = _sum(weights)
    if total != 1:
        raise ValueError("case aggregation needs exactly normalized history weights")
    prediction = _mixture(
        (weight, _law_from_wire(row["baseline"]["prediction"]))
        for weight, row in zip(weights, rows, strict=True)
    )
    baseline = _sum(
        _checked(weight * _fraction(row["baseline"]["risk"]))
        for weight, row in zip(weights, rows, strict=True)
    )
    controls = {
        name: _sum(
            _checked(weight * _fraction(row["controls"][name]["expected_risk"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        for name in ("N", "H")
    }
    channels, clean_gain, previous = [], None, controls["H"]
    for index, level in enumerate(LEVELS):
        risk = _sum(
            _checked(weight * _fraction(row["channels"][index]["expected_risk"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        gain = _sum(
            _checked(weight * _fraction(row["channels"][index]["gain"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        added = _sum(
            _checked(weight * _fraction(row["channels"][index]["gain_over_N"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        if (
            gain != baseline - risk
            or added != controls["N"] - risk
            or risk < previous
            or risk > controls["N"]
            or controls["N"] > baseline
        ):
            raise ValueError("likelihood-weighted risk/gain order or identity failed")
        previous = risk
        if index == 0:
            clean_gain = added
        retention = _checked(added / clean_gain) if clean_gain else None
        channels.append(
            {
                "level": _pair(level),
                "expected_risk": _pair(risk),
                "gain": _pair(gain),
                "gain_over_N": _pair(added),
                "retained_gain_fraction": None if retention is None else _pair(retention),
            }
        )
    losses = [
        _sum(
            _checked(weight * _fraction(row["garblings"][index]["risk_increase"]))
            for weight, row in zip(weights, rows, strict=True)
        )
        for index in range(len(GARBLING_LEVELS))
    ]
    for index, loss in enumerate(losses):
        if loss != _fraction(channels[index + 1]["expected_risk"]) - _fraction(
            channels[index]["expected_risk"]
        ):
            raise ValueError("aggregate garbling loss differs from adjacent risk change")
    if previous != controls["N"] or _sum(losses) != clean_gain:
        raise ValueError("aggregate complete-replacement endpoint or telescope failed")
    return {
        "total_weight": _pair(total),
        "prediction": _question_wire(prediction),
        "baseline_risk": _pair(baseline),
        "N_risk": _pair(controls["N"]),
        "H_risk": _pair(controls["H"]),
        "channels": channels,
        "adjacent_risk_increase": [_pair(loss) for loss in losses],
    }


def analyze(problem):
    prepared = _prepare(problem)
    channel_model = _channel_model(prepared["labels"])
    class_risks = [_risk(law) for law in prepared["class_laws"]]
    rows = []
    cells, posteriors, predictions = [0] * 4, [0] * 4, [0] * 4
    pairs, receivers = [0] * 3, [0] * 3
    strict_gain, no_gain, strict_loss, no_loss = [0] * 4, [0] * 4, [0] * 3, [0] * 3
    n_cells, n_posteriors, n_predictions, positive_oracle, known_n = 0, 0, 0, 0, 0
    witnesses = {
        "first_strict_gain": [None] * 4,
        "first_zero_gain": [None] * 4,
        "first_strict_loss": [None] * 3,
        "first_zero_loss": [None] * 3,
        "first_positive_oracle_residual": None,
        "first_zero_oracle_residual": None,
    }
    for supplied in prepared["beliefs"]:
        row = _belief_result(supplied, prepared, channel_model, class_risks)
        rows.append(row)
        bid = row["belief_id"]
        control_cells = row["controls"]["N"]["cells"]
        n_cells += len(control_cells)
        n_posteriors += sum(len(cell["posterior"]) for cell in control_cells)
        n_predictions += sum(len(cell["prediction"]) for cell in control_cells)
        for index, channel in enumerate(row["channels"]):
            cells[index] += len(channel["cells"])
            posteriors[index] += sum(len(cell["posterior"]) for cell in channel["cells"])
            predictions[index] += sum(len(cell["prediction"]) for cell in channel["cells"])
            added = _fraction(channel["gain_over_N"])
            strict_gain[index] += int(added > 0)
            no_gain[index] += int(added == 0)
            field = "first_strict_gain" if added > 0 else "first_zero_gain"
            if witnesses[field][index] is None:
                witnesses[field][index] = bid
        for index, edge in enumerate(row["garblings"]):
            pairs[index] += len(edge["couplings"])
            receivers[index] += len(edge["receiving_checks"])
            loss = _fraction(edge["risk_increase"])
            strict_loss[index] += int(loss > 0)
            no_loss[index] += int(loss == 0)
            field = "first_strict_loss" if loss > 0 else "first_zero_loss"
            if witnesses[field][index] is None:
                witnesses[field][index] = bid
        if n_cells + sum(cells) > CELL_CAP:
            raise ValueError("retained N and channel cell cap exceeded")
        if n_posteriors + sum(posteriors) > READOUT_POSTERIOR_CAP:
            raise ValueError("retained N and channel posterior atom cap exceeded")
        if n_predictions + sum(predictions) > PREDICTION_CAP:
            raise ValueError("retained N and channel prediction atom cap exceeded")
        if sum(pairs) > COUPLING_CAP:
            raise ValueError("total report-pair coupling atom cap exceeded")
        if sum(receivers) > RECEIVING_CAP:
            raise ValueError("total receiving-cell check cap exceeded")
        residual = _fraction(row["controls"]["H"]["expected_risk"])
        field = "first_positive_oracle_residual" if residual else "first_zero_oracle_residual"
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
        "rate": [_pair(rate) for rate in prepared["rate"]],
        "kernel_sha256": _digest(_kernel_wire(prepared["kernel"])),
        "channel_model": channel_model["wire"],
        "beliefs": rows,
        "aggregate": _aggregate(rows),
        "witnesses": witnesses,
        "counts": {
            "classes": len(prepared["labels"]),
            "beliefs": len(rows),
            "profile_atoms": profile_atoms,
            "kernel_atoms": sum(len(row) for row in prepared["kernel"]),
            "alphabet_fibers": len(channel_model["fibers"]),
            "alphabet_values": sum(len(values) for values in channel_model["fibers"].values()),
            "global_channel_atoms": channel_model["atom_counts"],
            "posterior_atoms": prepared["posterior_atoms"],
            "channel_cells": cells,
            "channel_posterior_atoms": posteriors,
            "channel_prediction_atoms": predictions,
            "N_cells": n_cells,
            "N_posterior_atoms": n_posteriors,
            "N_prediction_atoms": n_predictions,
            "coupling_atoms": pairs,
            "receiving_checks": receivers,
            "strict_gain_beliefs": strict_gain,
            "no_gain_beliefs": no_gain,
            "strict_loss_beliefs": strict_loss,
            "no_loss_beliefs": no_loss,
            "positive_oracle_residual_beliefs": positive_oracle,
            "known_N_beliefs": known_n,
        },
    }
    return json.loads(canonical(result))
