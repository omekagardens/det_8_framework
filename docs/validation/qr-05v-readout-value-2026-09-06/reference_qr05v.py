"""Independent joint-readout/future-law Brier-risk reference for QR-05V.

Only the supplied local class counts, explicit labels, current beliefs and
one thinning rate are used. Ordered deletion words reconstruct complete
profiles; readout-by-future joint masses precede all conditioning and scores.
This finite classical information calculation does not authenticate sensors,
empirical priors, physical realization or an ontology.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from math import comb, factorial, gcd

F = Fraction
BIT_LIMIT = 4096
INPUT_BITS = 64
DEPTH_LIMIT = 128
WORKING_CAP = 512 * 1024 * 1024
CLASS_CAP = 512
CLASS_LOCAL_CAP = 3072
PROFILE_ATOM_CAP = 32768
BELIEF_CAP = 512
POSTERIOR_CAP = 262144
CELL_CAP = 32768
READOUT_POSTERIOR_CAP = 786432
PREDICTION_CAP = 1048576
READOUTS = ("N", "NMT", "H")
EDGES = (("baseline", "N"), ("N", "NMT"), ("NMT", "H"))


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (RecursionError, TypeError, OverflowError) as error:
        raise ValueError("native JSON serialization failed") from error


def _digest(value):
    return hashlib.sha256(_canonical(value)).hexdigest()


def _fields(value, names, message):
    _require(
        type(value) is dict and all(type(key) is str for key in value) and set(value) == set(names),
        message,
    )


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _bounded(value):
    _require(type(value) is F, "reference arithmetic must remain rational")
    _require(
        abs(value.numerator).bit_length() <= BIT_LIMIT
        and value.denominator.bit_length() <= BIT_LIMIT,
        "reference rational exceeds the 4096-bit bound",
    )
    return value


def _native_json(value):
    # Active-path detection distinguishes cycles from valid repeated inputs.
    # Completed memoization retains repeated occurrences in expanded size.
    pending = [(value, False)]
    active = set()
    completed = {}
    while pending:
        current, leaving = pending.pop()
        if leaving:
            children = current.values() if type(current) is dict else current
            nodes, height = 1, 1
            for child in children:
                count, child_height = (
                    completed[id(child)] if type(child) in (list, dict) else (1, 0)
                )
                nodes += count
                height = max(height, child_height + 1)
                _require(nodes <= WORKING_CAP, "expanded JSON exceeds working cap")
                _require(height <= DEPTH_LIMIT, "native JSON exceeds depth cap")
            _require(
                nodes <= WORKING_CAP and height <= DEPTH_LIMIT, "native container resource cap"
            )
            completed[id(current)] = (nodes, height)
            active.remove(id(current))
            continue
        if current is None or type(current) in (str, bool):
            continue
        if type(current) is int:
            _require(abs(current).bit_length() <= BIT_LIMIT, "integer component bound")
            continue
        _require(type(current) in (list, dict), "non-native JSON value")
        identity = id(current)
        _require(identity not in active, "cyclic native container")
        if identity in completed:
            continue
        active.add(identity)
        pending.append((current, True))
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native JSON key")
            children = current.values()
        else:
            children = current
        pending.extend((child, False) for child in children)


def _zero_table():
    return [[0] * 4 for _ in range(4)]


def _integer(value, low=0, high=None):
    _require(
        type(value) is int
        and value >= low
        and (high is None or value <= high)
        and abs(value).bit_length() <= BIT_LIMIT,
        "native integer outside bound",
    )


def _colors(value):
    _require(type(value) is list and len(value) == 2, "colors must be a native pair")
    for color in value:
        _integer(color, 0, 3)


def _choose(n, k):
    return comb(n, k) if n >= 0 and 0 <= k <= n else 0


def _copy(value):
    return json.loads(_canonical(value))


def _validate_color_row(atoms, parent, color, classes):
    _require(type(atoms) is list and len(atoms) <= 3, "local color row bound")
    previous = -1
    total = 0
    for atom in atoms:
        _fields(atom, ("target_class", "multiplicity"), "local atom fields")
        target = atom["target_class"]
        _integer(target, 0, len(classes) - 1)
        _require(target > previous, "local targets must be sorted unique")
        previous = target
        _integer(atom["multiplicity"], 1, 3)
        total += atom["multiplicity"]
        child = classes[target]
        expected = list(parent["parent_color_sizes"])
        expected[color] -= 1
        _require(
            child["frame_id"] == parent["frame_id"] and child["parent_color_sizes"] == expected,
            "local target must preserve frame and lower exactly one color",
        )
    _require(total == parent["parent_color_sizes"][color], "local color row mass")


def _validate_local_model(local_model):
    _native_json(local_model)
    _fields(local_model, ("schema_version", "classes"), "local-only model fields")
    _require(
        type(local_model["schema_version"]) is str
        and local_model["schema_version"] == "det8-qr05s-local-v1",
        "local-only model schema",
    )
    classes = local_model["classes"]
    _require(type(classes) is list and 1 <= len(classes) <= CLASS_CAP, "local class resource bound")
    for cid, row in enumerate(classes):
        _fields(
            row,
            ("class_id", "frame_id", "parent_color_sizes", "odd", "even"),
            "local class fields",
        )
        _integer(row["class_id"], cid, cid)
        _integer(row["frame_id"], 0, 1)
        _colors(row["parent_color_sizes"])
    for row in classes:
        for color, name in enumerate(("odd", "even")):
            _validate_color_row(row[name], row, color, classes)
    _require(
        sum(len(row[name]) for row in classes for name in ("odd", "even")) <= CLASS_LOCAL_CAP,
        "local atom resource bound",
    )
    _require(len(_canonical(local_model)) <= WORKING_CAP, "local input byte cap")
    return classes


def _advance(vector, rows):
    result = {}
    for source, paths in vector.items():
        for target, multiplicity in rows[source].items():
            result[target] = result.get(target, 0) + paths * multiplicity
            _integer(result[target])
    return result


def _word_profiles(classes):
    """One fixed color word: odd deletion powers followed by even powers."""
    operators = [
        [{edge["target_class"]: edge["multiplicity"] for edge in row[name]} for row in classes]
        for name in ("odd", "even")
    ]
    profiles = []
    atoms = 0
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        counts = {}
        odds = {source: 1}  # An empty word is identity, not a zero-color deletion.
        for a in range(O + 1):
            word = dict(odds)
            for b in range(E + 1):
                divisor = factorial(a) * factorial(b)
                for target, paths in word.items():
                    _require(paths % divisor == 0, "ordered-word count is not factorial divisible")
                    count = paths // divisor
                    _integer(count, 1)
                    wanted = [O - a, E - b]
                    _require(
                        classes[target]["frame_id"] == parent["frame_id"]
                        and classes[target]["parent_color_sizes"] == wanted,
                        "word target rank/frame",
                    )
                    _require(target not in counts, "one target reached at inconsistent word rank")
                    counts[target] = count
                word = _advance(word, operators[1])
            _require(not word, "even deletion beyond its boundary is not zero")
            odds = _advance(odds, operators[0])
        _require(not odds, "odd deletion beyond its boundary is not zero")
        transitions = []
        for target, count in sorted(counts.items()):
            o, e = classes[target]["parent_color_sizes"]
            _integer(count, 1, min(9, _choose(O, o) * _choose(E, e)))
            transitions.append(
                {"target_class": target, "retained_color_sizes": [o, e], "multiplicity": count}
            )
        atoms += len(transitions)
        _require(atoms <= PROFILE_ATOM_CAP, "reconstructed profile atom resource bound")
        profiles.append(
            {"class_id": source, "parent_color_sizes": [O, E], "transitions": transitions}
        )
    return profiles, operators


def _recurrence_certificate(classes, profiles, operators):
    maps = [
        {edge["target_class"]: edge["multiplicity"] for edge in row["transitions"]}
        for row in profiles
    ]
    base_cells = 0
    recurrence_cells = 0
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        ranks = _zero_table()
        for target, child in enumerate(classes):
            value = maps[source].get(target, 0)
            m, n = child["parent_color_sizes"]
            compatible = child["frame_id"] == parent["frame_id"] and m <= O and n <= E
            if not compatible:
                _require(value == 0, "other-frame or impossible target is nonzero")
                continue
            ranks[m][n] += value
            if (O, E) == (m, n):
                base_cells += 1
                _require(value == int(source == target), "zero-deletion identity/base delta")
            for color, difference in enumerate((O - m, E - n)):
                if difference == 0:
                    continue
                recurrence_cells += 1
                total = sum(
                    multiplicity * maps[middle].get(target, 0)
                    for middle, multiplicity in operators[color][source].items()
                )
                _integer(total)
                _require(
                    total % difference == 0 and total // difference == value,
                    "independent local recurrence or exact division failed",
                )
        for o, e in product(range(4), repeat=2):
            _require(ranks[o][e] == _choose(O, o) * _choose(E, e), "full rank normalization")
        _require(sum(map(sum, ranks)) == 2 ** (O + E), "full subset mass")
    return {
        "target_cells": len(classes) ** 2,
        "base_cells": base_cells,
        "recurrence_cells": recurrence_cells,
        "normalization_cells": 16 * len(classes),
        "max_abs_residual": 0,
    }


def _operator_checks(classes, profiles, operators):
    rows = []
    for source, parent in enumerate(classes):
        O, E = parent["parent_color_sizes"]
        oo = _advance(operators[0][source], operators[0])
        ee = _advance(operators[1][source], operators[1])
        oe = _advance(operators[0][source], operators[1])
        eo = _advance(operators[1][source], operators[0])
        _require(oe == eo, "odd/even deletion words do not commute")
        targets = {}
        for grade, scale in (((O - 2, E), 2), ((O, E - 2), 2), ((O - 1, E - 1), 1)):
            targets[grade] = {
                edge["target_class"]: scale * edge["multiplicity"]
                for edge in profiles[source]["transitions"]
                if tuple(edge["retained_color_sizes"]) == grade
            }
        _require(oo == targets[(O - 2, E)], "odd-odd paths lack the 2! profile factor")
        _require(ee == targets[(O, E - 2)], "even-even paths lack the 2! profile factor")
        _require(oe == targets[(O - 1, E - 1)], "mixed words differ from the full profile")
        masses = (sum(oo.values()), sum(ee.values()), sum(oe.values()))
        _require(masses == (O * (O - 1), E * (E - 1), O * E), "two-deletion word masses")
        rows.append(
            {
                "class_id": source,
                "odd_odd_targets": len(oo),
                "even_even_targets": len(ee),
                "mixed_targets": len(oe),
                "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
                "odd_odd_pairs": masses[0],
                "even_even_pairs": masses[1],
                "mixed_pairs": masses[2],
                "max_abs_residual": 0,
            }
        )
    return {
        "verified": True,
        "rows": rows,
        "totals": {
            field: sum(row[field] for row in rows)
            for field in (
                "odd_odd_targets",
                "even_even_targets",
                "mixed_targets",
                "coefficient_cells",
                "odd_odd_pairs",
                "even_even_pairs",
                "mixed_pairs",
                "max_abs_residual",
            )
        },
    }


def reconstruct_profiles(local_model):
    """Construct complete profiles using only validated local class counts.

    Structural/algebraic validity does not authenticate H labels, raw-domain
    membership, or realization by an observed partial order.
    """
    classes = _validate_local_model(local_model)
    profiles, operators = _word_profiles(classes)
    certificate = _recurrence_certificate(classes, profiles, operators)
    checks = _operator_checks(classes, profiles, operators)
    result = {"profiles": profiles, "certificate": certificate, "operator_checks": checks}
    _native_json(result)
    _require(len(_canonical(result)) <= WORKING_CAP, "local output byte cap")
    return _copy(result)


def _input_fraction(pair, positive=False, bits=None):
    if bits is None:
        bits = BIT_LIMIT
    _require(type(pair) is list and len(pair) == 2, "fraction must be a native pair")
    numerator, denominator = pair
    _require(
        type(numerator) is int
        and type(denominator) is int
        and numerator >= 0
        and denominator > 0
        and numerator.bit_length() <= bits
        and denominator.bit_length() <= bits,
        "input fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must be reduced")
    value = _bounded(F(numerator, denominator))
    _require(0 <= value <= 1 and (not positive or value > 0), "probability interval/support")
    return value


def _wire_fraction(value):
    value = _bounded(value)
    _require(0 <= value <= 1, "probability/risk outside unit interval")
    return [value.numerator, value.denominator]


def _sum(values):
    result = F(0)
    for value in values:
        result = _bounded(result + value)
    return result


def _add(target, key, value):
    value = _bounded(value)
    _require(value >= 0, "negative path mass")
    if value:
        target[key] = _bounded(target.get(key, F(0)) + value)


def _normalise(masses):
    total = _sum(masses.values())
    _require(total > 0, "cannot normalize impossible event")
    result = {key: _bounded(value / total) for key, value in masses.items() if value}
    _require(_sum(result.values()) == 1, "posterior/law normalization")
    return result


def _belief(masses):
    return [
        {"class_id": cid, "probability": _wire_fraction(value)}
        for cid, value in sorted(masses.items())
        if value
    ]


def _question_law(masses):
    return [
        {"value": list(value), "probability": _wire_fraction(probability)}
        for value, probability in sorted(masses.items())
        if probability
    ]


def _propagate(masses, kernel):
    result = {}
    for source, mass in masses.items():
        for target, probability in kernel[source].items():
            _add(result, target, _bounded(mass * probability))
    return result


def _push_questions(masses, questions):
    result = {}
    for cid, probability in masses.items():
        _add(result, questions[cid], probability)
    return result


def _kernel(profiles, rates):
    x, y = rates
    factors = {}
    rows = []
    for profile in profiles:
        O, E = profile["parent_color_sizes"]
        row = {}
        for edge in profile["transitions"]:
            m, n = edge["retained_color_sizes"]
            key = (O, E, m, n)
            if key not in factors:
                factors[key] = _bounded(x**m * (1 - x) ** (O - m) * y**n * (1 - y) ** (E - n))
            probability = _bounded(edge["multiplicity"] * factors[key])
            if probability:
                row[edge["target_class"]] = probability
        _require(_sum(row.values()) == 1, "class kernel normalization")
        rows.append(row)
    return rows


def _kernel_wire(kernel):
    return [
        {
            "class_id": source,
            "transitions": [
                {"target_class": target, "probability": _wire_fraction(value)}
                for target, value in sorted(row.items())
                if value
            ],
        }
        for source, row in enumerate(kernel)
    ]


def _prepare(problem):
    _native_json(problem)
    _fields(problem, ("schema_version", "family", "model", "rate", "beliefs"), "V problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05v-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05v_readout_value",
        "V schema/family",
    )
    model = problem["model"]
    _fields(model, ("classes", "labels"), "summary-only model fields")
    local_model = {"schema_version": "det8-qr05s-local-v1", "classes": model["classes"]}
    classes = _validate_local_model(local_model)
    labels = model["labels"]
    _require(type(labels) is list and len(labels) == len(classes), "class label table")
    observations, questions = [], []
    for cid, (row, label) in enumerate(zip(classes, labels, strict=True)):
        _fields(label, ("class_id", "observation", "question"), "label fields")
        _integer(label["class_id"], cid, cid)
        observation, question = label["observation"], label["question"]
        _require(type(observation) is list and len(observation) == 5, "observation label shape")
        _require(type(question) is list and len(question) == 7, "question label shape")
        for value in observation + question:
            _integer(value, 0)
        O, E = row["parent_color_sizes"]
        frame, N0, N1, N2, N3 = observation
        _require(
            frame == row["frame_id"]
            and N0 == 1
            and N1 == O + E + frame
            and N2 <= _choose(N1, 2)
            and N3 <= _choose(N1, 3),
            "observation label structure",
        )
        _require(
            question[:5] == observation
            and question[5] <= _choose(O, 2) * _choose(E, 2)
            and question[6] <= _choose(O, 2) * _choose(E, 2),
            "question label structure/prefix",
        )
        observations.append(tuple(observation))
        questions.append(tuple(question))

    rate = problem["rate"]
    _require(type(rate) is list and len(rate) == 2, "two-color rate pair")
    rates = tuple(_input_fraction(value, bits=INPUT_BITS) for value in rate)
    beliefs = problem["beliefs"]
    _require(type(beliefs) is list and 1 <= len(beliefs) <= BELIEF_CAP, "belief count bound")
    parsed = []
    atoms = 0
    for bid, row in enumerate(beliefs):
        _fields(row, ("belief_id", "weight", "posterior"), "current belief fields")
        _integer(row["belief_id"], bid, bid)
        weight = _input_fraction(row["weight"], positive=True)
        posterior = row["posterior"]
        _require(
            type(posterior) is list and 1 <= len(posterior) <= CLASS_CAP, "posterior support cap"
        )
        mass = {}
        previous = -1
        for atom in posterior:
            _fields(atom, ("class_id", "probability"), "posterior atom fields")
            cid = atom["class_id"]
            _integer(cid, 0, len(classes) - 1)
            _require(cid > previous, "posterior must be sorted unique")
            previous = cid
            mass[cid] = _input_fraction(atom["probability"], positive=True)
        _require(_sum(mass.values()) == 1, "supplied posterior must have mass one")
        atoms += len(mass)
        _require(atoms <= POSTERIOR_CAP, "total input posterior atom cap")
        parsed.append((weight, mass))
    _require(_sum(weight for weight, _ in parsed) == 1, "belief weights must already normalize")
    _require(len(_canonical(problem)) <= WORKING_CAP, "problem working cap")
    built = reconstruct_profiles(local_model)
    kernel = _kernel(built["profiles"], rates)
    qrows = [_push_questions(row, questions) for row in kernel]
    for row in qrows:
        _require(_sum(row.values()) == 1, "full Q3 kernel normalization")
    selectors = {
        "N": observations,
        "NMT": questions,
        "H": [(cid,) for cid in range(len(classes))],
    }
    nmt_to_n = {}
    for nmt, n in zip(questions, observations, strict=True):
        _require(nmt[:5] == n, "global NMT-to-N nesting")
        if nmt in nmt_to_n:
            _require(nmt_to_n[nmt] == n, "global readout map is not a function")
        nmt_to_n[nmt] = n
    h_to_nmt = {(cid,): q for cid, q in enumerate(questions)}
    maps = {
        "NMT_to_N": [
            {"fine": list(fine), "coarse": list(coarse)}
            for fine, coarse in sorted(nmt_to_n.items())
        ],
        "H_to_NMT": [
            {"fine": list(fine), "coarse": list(coarse)}
            for fine, coarse in sorted(h_to_nmt.items())
        ],
    }
    return {
        "model_sha256": _digest(model),
        "built": built,
        "rate": _copy(rate),
        "kernel": kernel,
        "qrows": qrows,
        "selectors": selectors,
        "maps": maps,
        "parents": ({}, nmt_to_n, h_to_nmt),
        "beliefs": parsed,
        "posterior_atoms": atoms,
    }


def _risk_from_joint(joint, weight):
    """Conditional risk using raw joint cell masses, without posterior scoring."""
    _require(weight > 0 and _sum(joint.values()) == weight, "joint future row mass")
    collision = _sum(_bounded(value * value / (weight * weight)) for value in joint.values())
    risk = _bounded(1 - collision)
    _require(0 <= risk <= 1, "conditional Brier risk range")
    return risk


def _joint_cells(belief, selector, qrows):
    joint, class_joint, weights = {}, {}, {}
    for cid, mass in belief.items():
        value = selector[cid]
        _add(weights, value, mass)
        _add(class_joint.setdefault(value, {}), cid, mass)
        for question, probability in qrows[cid].items():
            _add(joint.setdefault(value, {}), question, _bounded(mass * probability))
    cells = {}
    for value, weight in sorted(weights.items()):
        law = {q: _bounded(mass / weight) for q, mass in joint[value].items()}
        posterior = {cid: _bounded(mass / weight) for cid, mass in class_joint[value].items()}
        _require(_sum(law.values()) == _sum(posterior.values()) == 1, "cell normalized laws")
        cells[value] = {
            "value": value,
            "weight": weight,
            "joint": joint[value],
            "posterior": posterior,
            "law": law,
            "risk": _risk_from_joint(joint[value], weight),
        }
    _require(_sum(weights.values()) == 1, "readout weights normalize")
    return cells


def _cell_wire(cell):
    return {
        "value": list(cell["value"]),
        "probability": _wire_fraction(cell["weight"]),
        "posterior": _belief(cell["posterior"]),
        "prediction": _question_law(cell["law"]),
        "risk": _wire_fraction(cell["risk"]),
    }


def _joint_expected_risk(cells):
    # Summing squared JOINT masses divided by their readout masses is the
    # collision probability after that readout. No extra thinning is applied.
    collision = _sum(
        _bounded(value * value / cell["weight"])
        for cell in cells.values()
        for value in cell["joint"].values()
    )
    risk = _bounded(1 - collision)
    _require(0 <= risk <= 1, "expected readout risk range")
    _require(
        risk == _sum(_bounded(cell["weight"] * cell["risk"]) for cell in cells.values()),
        "joint-risk / weighted conditional-risk identity",
    )
    return risk


def _weighted_distance(left, right, weight):
    # The unweighted distance may exceed one. Only the weighted variance term
    # is subsequently emitted as a probability/risk quantity.
    distance = _sum(
        _bounded((left.get(q, F(0)) - right.get(q, F(0))) ** 2) for q in left.keys() | right.keys()
    )
    term = _bounded(weight * distance)
    _require(term >= 0, "negative squared-law term")
    return term


def _refinement(coarse_name, fine_name, coarse, fine, mapping):
    parents = []
    total_drop = F(0)
    total_variance = F(0)
    all_equal = True
    covered = set()
    for parent_value, parent in sorted(coarse.items()):
        children = [
            cell
            for value, cell in sorted(fine.items())
            if (() if coarse_name == "baseline" else mapping[value]) == parent_value
        ]
        _require(children, "positive parent has no positive children")
        covered.update(cell["value"] for cell in children)
        _require(
            _sum(cell["weight"] for cell in children) == parent["weight"],
            "nested readout cell weights",
        )
        posterior, law = {}, {}
        conditional_risk = F(0)
        conditional_variance = F(0)
        predictions_equal = True
        for child in children:
            weight = _bounded(child["weight"] / parent["weight"])
            for cid, p in child["posterior"].items():
                _add(posterior, cid, _bounded(weight * p))
            for question, p in child["law"].items():
                _add(law, question, _bounded(weight * p))
            conditional_risk = _bounded(conditional_risk + weight * child["risk"])
            conditional_variance = _bounded(
                conditional_variance + _weighted_distance(child["law"], parent["law"], weight)
            )
            predictions_equal = predictions_equal and child["law"] == parent["law"]
        _require(posterior == parent["posterior"] and law == parent["law"], "whole nested mixtures")
        drop = _bounded(parent["risk"] - conditional_risk)
        _require(drop == conditional_variance and 0 <= drop <= 1, "conditional risk / variance")
        _require((drop == 0) == predictions_equal, "conditional zero gain iff equal laws")
        total_drop = _bounded(total_drop + parent["weight"] * drop)
        total_variance = _bounded(total_variance + parent["weight"] * conditional_variance)
        all_equal = all_equal and predictions_equal
        parents.append(
            {
                "value": list(parent_value),
                "probability": _wire_fraction(parent["weight"]),
                "fine_values": [list(child["value"]) for child in children],
                "mixture_sha256": _digest(_question_law(law)),
                "conditional_risk_drop": _wire_fraction(drop),
                "conditional_variance_gain": _wire_fraction(conditional_variance),
                "predictions_equal": predictions_equal,
            }
        )
    _require(covered == set(fine), "every positive fine cell has a checked parent")
    coarse_risk, fine_risk = _joint_expected_risk(coarse), _joint_expected_risk(fine)
    _require(total_drop == total_variance == coarse_risk - fine_risk, "global refinement risk")
    _require((total_drop == 0) == all_equal, "global zero gain iff equal laws")
    return {
        "coarse": coarse_name,
        "fine": fine_name,
        "risk_drop": _wire_fraction(total_drop),
        "variance_gain": _wire_fraction(total_variance),
        "parent_checks": parents,
        "zero_gain_iff_equal": True,
    }, total_drop


def _score_belief(bid, weight, belief, prepared):
    selectors, qrows = prepared["selectors"], prepared["qrows"]
    baseline_cells = _joint_cells(belief, [()] * len(qrows), qrows)
    baseline = baseline_cells[()]
    readout_cells = {name: _joint_cells(belief, selectors[name], qrows) for name in READOUTS}
    readouts = {}
    risks, gains = {}, {}
    for name in READOUTS:
        cells = readout_cells[name]
        marginal = {}
        for cell in cells.values():
            for question, mass in cell["joint"].items():
                _add(marginal, question, mass)
        _require(marginal == baseline["law"], "complete marginal future unchanged")
        risk = _joint_expected_risk(cells)
        gain = _bounded(baseline["risk"] - risk)
        variance = _sum(
            _weighted_distance(cell["law"], baseline["law"], cell["weight"])
            for cell in cells.values()
        )
        _require(gain == variance and gain >= 0, "readout gain identity")
        risks[name], gains[name] = risk, gain
        readouts[name] = {
            "cells": [_cell_wire(cell) for cell in cells.values()],
            "expected_risk": _wire_fraction(risk),
            "gain": _wire_fraction(gain),
            "variance_gain": _wire_fraction(variance),
        }
    hierarchy = {"baseline": baseline_cells, **readout_cells}
    refinements, adjacent = [], []
    for index, (coarse, fine) in enumerate(EDGES):
        row, drop = _refinement(
            coarse, fine, hierarchy[coarse], hierarchy[fine], prepared["parents"][index]
        )
        refinements.append(row)
        adjacent.append(drop)
    oracle = _sum(
        _bounded(mass * _risk_from_joint(qrows[cid], F(1))) for cid, mass in belief.items()
    )
    _require(oracle == risks["H"], "independent class-wise oracle residual")
    _require(_sum(adjacent) == gains["H"], "adjacent gains telescope")
    _require(
        gains["N"] == adjacent[0] and gains["NMT"] == _sum(adjacent[:2]),
        "nested baseline gains",
    )
    row = {
        "belief_id": bid,
        "weight": _wire_fraction(weight),
        "posterior": _belief(belief),
        "baseline": {
            "prediction": _question_law(baseline["law"]),
            "risk": _wire_fraction(baseline["risk"]),
        },
        "readouts": readouts,
        "refinements": refinements,
        "oracle_residual": _wire_fraction(oracle),
        "checks": {
            "probabilities_normalized": True,
            "marginal_future_preserved": True,
            "nested_mixtures": True,
            "nested_risks": True,
            "oracle_residual_identity": True,
            "gains_telescope": True,
            "N_already_known": len(readout_cells["N"]) == 1,
        },
    }
    return row, baseline, risks, gains, adjacent, oracle


def analyze(problem):
    prepared = _prepare(problem)
    rows = []
    aggregate_prediction = {}
    baseline_risk, oracle_residual = F(0), F(0)
    expected_risks = {name: F(0) for name in READOUTS}
    gains = {name: F(0) for name in READOUTS}
    adjacent_gains = [F(0)] * len(EDGES)
    first_strict, first_zero = [None] * len(EDGES), [None] * len(EDGES)
    first_positive_residual = first_zero_residual = None
    cells_count = {name: 0 for name in READOUTS}
    posterior_count = {name: 0 for name in READOUTS}
    prediction_count = {name: 0 for name in READOUTS}
    parent_count = [0] * len(EDGES)
    strict_count, zero_count = {name: 0 for name in READOUTS}, {name: 0 for name in READOUTS}
    positive_residual = known_n = 0
    for bid, (weight, belief) in enumerate(prepared["beliefs"]):
        row, baseline, risks, row_gains, adjacent, oracle = _score_belief(
            bid, weight, belief, prepared
        )
        rows.append(row)
        baseline_risk = _bounded(baseline_risk + weight * baseline["risk"])
        oracle_residual = _bounded(oracle_residual + weight * oracle)
        for q, p in baseline["law"].items():
            _add(aggregate_prediction, q, _bounded(weight * p))
        for name in READOUTS:
            expected_risks[name] = _bounded(expected_risks[name] + weight * risks[name])
            gains[name] = _bounded(gains[name] + weight * row_gains[name])
            cells = row["readouts"][name]["cells"]
            cells_count[name] += len(cells)
            posterior_count[name] += sum(len(cell["posterior"]) for cell in cells)
            prediction_count[name] += sum(len(cell["prediction"]) for cell in cells)
            strict_count[name] += int(row_gains[name] > 0)
            zero_count[name] += int(row_gains[name] == 0)
        _require(sum(cells_count.values()) <= CELL_CAP, "readout cell cap")
        _require(
            sum(posterior_count.values()) <= READOUT_POSTERIOR_CAP, "readout posterior atom cap"
        )
        _require(sum(prediction_count.values()) <= PREDICTION_CAP, "readout prediction atom cap")
        for index, drop in enumerate(adjacent):
            adjacent_gains[index] = _bounded(adjacent_gains[index] + weight * drop)
            parent_count[index] += len(row["refinements"][index]["parent_checks"])
            if drop > 0 and first_strict[index] is None:
                first_strict[index] = bid
            if drop == 0 and first_zero[index] is None:
                first_zero[index] = bid
        positive_residual += int(oracle > 0)
        known_n += int(row["checks"]["N_already_known"])
        if oracle > 0 and first_positive_residual is None:
            first_positive_residual = bid
        if oracle == 0 and first_zero_residual is None:
            first_zero_residual = bid
    _require(_sum(aggregate_prediction.values()) == 1, "case-weighted prediction normalization")
    _require(
        0 <= expected_risks["H"] <= expected_risks["NMT"] <= expected_risks["N"] <= baseline_risk,
        "aggregate nested risk",
    )
    for name in READOUTS:
        _require(gains[name] == baseline_risk - expected_risks[name], "aggregate gain identity")
    _require(
        _sum(adjacent_gains) == gains["H"]
        and oracle_residual == expected_risks["H"]
        and adjacent_gains[0] == gains["N"]
        and _sum(adjacent_gains[:2]) == gains["NMT"],
        "aggregate telescoping and oracle identity",
    )
    built = prepared["built"]
    profile_atoms = sum(len(row["transitions"]) for row in built["profiles"])
    result = {
        "model_sha256": prepared["model_sha256"],
        "reconstruction": {
            "profiles_sha256": _digest(built["profiles"]),
            "profile_atoms": profile_atoms,
            "certificate": built["certificate"],
            "operator_checks": built["operator_checks"],
        },
        "rate": prepared["rate"],
        "kernel_sha256": _digest(_kernel_wire(prepared["kernel"])),
        "readout_maps": prepared["maps"],
        "beliefs": rows,
        "aggregate": {
            "total_weight": [1, 1],
            "prediction": _question_law(aggregate_prediction),
            "baseline_risk": _wire_fraction(baseline_risk),
            "expected_risk": {name: _wire_fraction(expected_risks[name]) for name in READOUTS},
            "gain": {name: _wire_fraction(gains[name]) for name in READOUTS},
            "adjacent_gain": [_wire_fraction(value) for value in adjacent_gains],
            "oracle_residual": _wire_fraction(oracle_residual),
        },
        "witnesses": {
            "first_strict": first_strict,
            "first_zero": first_zero,
            "first_positive_oracle_residual": first_positive_residual,
            "first_zero_oracle_residual": first_zero_residual,
        },
        "counts": {
            "classes": len(prepared["qrows"]),
            "beliefs": len(rows),
            "profile_atoms": profile_atoms,
            "kernel_atoms": sum(map(len, prepared["kernel"])),
            "posterior_atoms": prepared["posterior_atoms"],
            "readout_cells": cells_count,
            "readout_posterior_atoms": posterior_count,
            "readout_prediction_atoms": prediction_count,
            "refinement_parents": parent_count,
            "strict_gain_beliefs": strict_count,
            "no_gain_beliefs": zero_count,
            "positive_oracle_residual_beliefs": positive_residual,
            "known_N_beliefs": known_n,
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= WORKING_CAP, "V output working cap")
    return _copy(result)
