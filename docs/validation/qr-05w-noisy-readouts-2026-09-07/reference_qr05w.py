"""Independent joint-channel/current/future Brier-risk reference for QR-05W.

Only the supplied local class counts, explicit labels, current beliefs and
one thinning rate are used. Ordered deletion words reconstruct complete
profiles; noisy report/current/future joint masses precede conditioning and scores.
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
READOUT_POSTERIOR_CAP = 1048576
PREDICTION_CAP = 2097152
CHANNEL_ATOM_CAP = 1048576
COMPOSITION_TERM_CAP = 4194304
COUPLING_CAP = 1048576
RECEIVING_CAP = 32768
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
GARBLINGS = (F(1, 2), F(1, 2), F(1))


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
    _fields(problem, ("schema_version", "family", "model", "rate", "beliefs"), "W problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05w-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05w_noisy_readouts",
        "W schema/family",
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


def _channel_rows_wire(rows):
    return [
        {
            "source": list(source),
            "transitions": [
                {"value": list(value), "probability": _wire_fraction(probability)}
                for value, probability in sorted(row.items())
                if probability
            ],
        }
        for source, row in sorted(rows.items())
    ]


def _channel_family(prepared):
    alphabet = {}
    for value in prepared["selectors"]["NMT"]:
        alphabet.setdefault(value[:5], set()).add(value)
    alphabet = {n: sorted(values) for n, values in sorted(alphabet.items())}
    planned_atoms = [
        sum(len(values) if level == 0 else len(values) ** 2 for values in alphabet.values())
        for level in LEVELS
    ]
    _require(sum(planned_atoms) <= CHANNEL_ATOM_CAP, "global channel atom cap")
    channels = []
    for level in LEVELS:
        rows = {}
        for values in alphabet.values():
            uniform = _bounded(level / len(values))
            for source in values:
                row = {}
                for value in values:
                    probability = _bounded(uniform + (1 - level) * int(source == value))
                    if probability:
                        row[value] = probability
                _require(_sum(row.values()) == 1, "global channel row mass")
                rows[source] = row
        channels.append(rows)
    global_atoms = [sum(map(len, rows.values())) for rows in channels]
    _require(global_atoms == planned_atoms, "planned/actual channel atoms")
    garbling_rows = [channels[1], channels[1], channels[3]]
    planned_terms = [
        sum(len(garbling[middle]) for row in channels[i].values() for middle in row)
        for i, garbling in enumerate(garbling_rows)
    ]
    # Bound all three positive-product loops before multiplying any of them.
    _require(sum(planned_terms) <= COMPOSITION_TERM_CAP, "composition product term cap")
    checks = []
    for i, garbling in enumerate(garbling_rows):
        composed, terms = {}, 0
        for source, row in channels[i].items():
            result = {}
            for middle, first in row.items():
                for target, second in garbling[middle].items():
                    terms += 1
                    _add(result, target, _bounded(first * second))
            _require(_sum(result.values()) == 1, "composed row mass")
            composed[source] = result
        _require(terms == planned_terms[i], "composition planned work")
        _require(composed == channels[i + 1], "complete channel composition")
        checks.append(
            {
                "from_index": i,
                "to_index": i + 1,
                "garbling_level": _wire_fraction(GARBLINGS[i]),
                "row_comparisons": len(composed),
                "product_terms": terms,
                "positive_composed_atoms": sum(map(len, composed.values())),
                "composed_sha256": _digest(_channel_rows_wire(composed)),
                "exact": True,
            }
        )
    wire = {
        "alphabet": [
            {"N": list(n), "values": [list(a) for a in values]} for n, values in alphabet.items()
        ],
        "channels": [
            {"level": _wire_fraction(level), "rows": _channel_rows_wire(rows)}
            for level, rows in zip(LEVELS, channels, strict=True)
        ],
        "composition_checks": checks,
    }
    return alphabet, channels, garbling_rows, wire, global_atoms


def _risk_from_joint(joint, weight):
    _require(weight > 0 and _sum(joint.values()) == weight, "joint future row mass")
    collision = _sum(_bounded(value * value / (weight * weight)) for value in joint.values())
    risk = _bounded(1 - collision)
    _require(0 <= risk <= 1, "conditional Brier risk range")
    return risk


def _joint_cells(belief, report_rows, qrows):
    # Build J(z,h) and J(z,q) from b(h)C(z|a(h))k_h(q), before conditioning.
    class_joint, future_joint, weights = {}, {}, {}
    for cid, prior in belief.items():
        for report, likelihood in report_rows[cid].items():
            joint_h = _bounded(prior * likelihood)
            _add(weights, report, joint_h)
            _add(class_joint.setdefault(report, {}), cid, joint_h)
            for question, transition in qrows[cid].items():
                _add(future_joint.setdefault(report, {}), question, _bounded(joint_h * transition))
    cells = {}
    for value, weight in sorted(weights.items()):
        posterior = {cid: _bounded(mass / weight) for cid, mass in class_joint[value].items()}
        law = {q: _bounded(mass / weight) for q, mass in future_joint[value].items()}
        _require(_sum(posterior.values()) == _sum(law.values()) == 1, "cell normalized laws")
        cells[value] = {
            "value": value,
            "weight": weight,
            "class_joint": class_joint[value],
            "joint": future_joint[value],
            "posterior": posterior,
            "law": law,
            "risk": _risk_from_joint(future_joint[value], weight),
        }
    _require(_sum(weights.values()) == 1, "report weights normalize")
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
    collision = _sum(
        _bounded(value * value / cell["weight"])
        for cell in cells.values()
        for value in cell["joint"].values()
    )
    risk = _bounded(1 - collision)
    _require(
        0 <= risk <= 1
        and risk == _sum(_bounded(cell["weight"] * cell["risk"]) for cell in cells.values()),
        "joint collision / weighted risk identity",
    )
    return risk


def _weighted_distance(left, right, weight):
    distance = _sum(
        _bounded((left.get(q, F(0)) - right.get(q, F(0))) ** 2) for q in left.keys() | right.keys()
    )
    result = _bounded(weight * distance)
    _require(result >= 0, "negative weighted square")
    return result


def _check_marginals(cells, belief, prediction):
    current, future = {}, {}
    for cell in cells.values():
        for cid, mass in cell["class_joint"].items():
            _add(current, cid, mass)
        for q, mass in cell["joint"].items():
            _add(future, q, mass)
    _require(current == belief and future == prediction, "complete current/future marginals")


def _garbling(i, earlier, later, channel):
    coupling, first_marginal, last_marginal = {}, {}, {}
    for source, cell in sorted(earlier.items()):
        for target, likelihood in sorted(channel[source].items()):
            mass = _bounded(cell["weight"] * likelihood)
            if mass:
                coupling[(source, target)] = mass
                _add(first_marginal, source, mass)
                _add(last_marginal, target, mass)
    _require(
        first_marginal == {v: c["weight"] for v, c in earlier.items()}, "first coupling marginal"
    )
    _require(last_marginal == {v: c["weight"] for v, c in later.items()}, "last coupling marginal")
    _require(_sum(coupling.values()) == 1, "coupling normalization")
    receiving, total_risk, total_variance = [], F(0), F(0)
    equalities = []
    for target, final in sorted(later.items()):
        incoming = [
            (source, mass) for (source, dest), mass in sorted(coupling.items()) if dest == target
        ]
        _require(
            incoming and _sum(mass for _, mass in incoming) == final["weight"], "receiving mass"
        )
        posterior, law, conditional_risk, variance = {}, {}, F(0), F(0)
        predicates = []
        for source, mass in incoming:
            cell = earlier[source]
            reverse = _bounded(mass / final["weight"])
            for cid, value in cell["posterior"].items():
                _add(posterior, cid, _bounded(reverse * value))
            for q, value in cell["law"].items():
                _add(law, q, _bounded(reverse * value))
            conditional_risk = _bounded(conditional_risk + reverse * cell["risk"])
            variance = _bounded(variance + _weighted_distance(cell["law"], final["law"], reverse))
            predicates.append(cell["law"] == final["law"])
        _require(
            posterior == final["posterior"] and law == final["law"],
            "complete reverse-Bayes mixtures",
        )
        increase = _bounded(final["risk"] - conditional_risk)
        equal = all(predicates)
        _require(0 <= increase <= 1 and increase == variance, "conditional risk increase identity")
        _require((increase == 0) == equal, "conditional zero loss iff predictive equality")
        equalities.append(equal)
        total_risk = _bounded(total_risk + final["weight"] * increase)
        total_variance = _bounded(total_variance + final["weight"] * variance)
        receiving.append(
            {
                "value": list(target),
                "probability": _wire_fraction(final["weight"]),
                "earlier_values": [list(source) for source, _ in incoming],
                "posterior_mixture_sha256": _digest(_belief(posterior)),
                "prediction_mixture_sha256": _digest(_question_law(law)),
                "conditional_risk_increase": _wire_fraction(increase),
                "conditional_variance_loss": _wire_fraction(variance),
                "predictions_equal": equal,
            }
        )
    _require(
        total_risk == total_variance == _joint_expected_risk(later) - _joint_expected_risk(earlier),
        "global garbling identity",
    )
    _require((total_risk == 0) == all(equalities), "global zero loss iff equal laws")
    return {
        "from_index": i,
        "to_index": i + 1,
        "garbling_level": _wire_fraction(GARBLINGS[i]),
        "risk_increase": _wire_fraction(total_risk),
        "variance_loss": _wire_fraction(total_variance),
        "couplings": [
            {"earlier": list(source), "later": list(target), "probability": _wire_fraction(mass)}
            for (source, target), mass in sorted(coupling.items())
        ],
        "receiving_checks": receiving,
        "zero_loss_iff_equal": True,
    }, total_risk


def _score_belief(bid, weight, belief, prepared, family):
    alphabet, channels, garbling_rows, _, _ = family
    qrows, selectors = prepared["qrows"], prepared["selectors"]
    baseline = _joint_cells(belief, [{(): F(1)} for _ in qrows], qrows)[()]
    n_cells = _joint_cells(belief, [{n: F(1)} for n in selectors["N"]], qrows)
    n_risk = _joint_expected_risk(n_cells)
    h_risk = _sum(
        _bounded(mass * _risk_from_joint(qrows[cid], F(1))) for cid, mass in belief.items()
    )
    _check_marginals(n_cells, belief, baseline["law"])
    level_cells = [
        _joint_cells(belief, [channel[value] for value in selectors["NMT"]], qrows)
        for channel in channels
    ]
    clean = _joint_cells(belief, [{a: F(1)} for a in selectors["NMT"]], qrows)
    _require(clean == level_cells[0], "zero-noise deterministic NMT endpoint")
    for value, cell in level_cells[-1].items():
        parent = n_cells[value[:5]]
        _require(
            cell["weight"] == parent["weight"] / len(alphabet[value[:5]])
            and cell["posterior"] == parent["posterior"]
            and cell["law"] == parent["law"],
            "complete replacement N-information endpoint",
        )
    _require(
        set(level_cells[-1]) == {a for n in n_cells for a in alphabet[n]},
        "complete replacement covers every positive N alphabet",
    )
    risks = [_joint_expected_risk(cells) for cells in level_cells]
    _require(
        h_risk <= risks[0] <= risks[1] <= risks[2] <= risks[3] == n_risk <= baseline["risk"],
        "expected risk order and endpoints",
    )
    extra_gains = [_bounded(n_risk - risk) for risk in risks]
    records = []
    for i, cells in enumerate(level_cells):
        _check_marginals(cells, belief, baseline["law"])
        gain = _bounded(baseline["risk"] - risks[i])
        variance = _sum(
            _weighted_distance(cell["law"], baseline["law"], cell["weight"])
            for cell in cells.values()
        )
        _require(gain == variance, "noisy channel gain / squared-law identity")
        records.append(
            {
                "level": _wire_fraction(LEVELS[i]),
                "cells": [_cell_wire(cell) for cell in cells.values()],
                "expected_risk": _wire_fraction(risks[i]),
                "gain": _wire_fraction(gain),
                "variance_gain": _wire_fraction(variance),
                "gain_over_N": _wire_fraction(extra_gains[i]),
                "retained_gain_fraction": _wire_fraction(extra_gains[i] / extra_gains[0])
                if extra_gains[0]
                else None,
            }
        )
    garblings, losses = [], []
    for i, garbling in enumerate(garbling_rows):
        row, loss = _garbling(i, level_cells[i], level_cells[i + 1], garbling)
        garblings.append(row)
        losses.append(loss)
    _require(_sum(losses) == n_risk - risks[0] == extra_gains[0], "losses telescope")
    row = {
        "belief_id": bid,
        "weight": _wire_fraction(weight),
        "posterior": _belief(belief),
        "baseline": {
            "prediction": _question_law(baseline["law"]),
            "risk": _wire_fraction(baseline["risk"]),
        },
        "controls": {
            "N": {
                "cells": [_cell_wire(c) for c in n_cells.values()],
                "expected_risk": _wire_fraction(n_risk),
                "gain": _wire_fraction(baseline["risk"] - n_risk),
            },
            "H": {
                "expected_risk": _wire_fraction(h_risk),
                "gain": _wire_fraction(baseline["risk"] - h_risk),
            },
        },
        "channels": records,
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
    return row, baseline, n_risk, h_risk, risks, extra_gains, losses


def analyze(problem):
    """Exact noisy-current-report laws from a structurally checked local model."""
    prepared = _prepare(problem)
    family = _channel_family(prepared)
    rows, prediction = [], {}
    baseline_risk = n_risk = h_risk = F(0)
    risks, gains, extra_gains, adjacent = [F(0)] * 4, [F(0)] * 4, [F(0)] * 4, [F(0)] * 3
    first_strict_gain, first_zero_gain = [None] * 4, [None] * 4
    first_strict_loss, first_zero_loss = [None] * 3, [None] * 3
    first_positive_residual = first_zero_residual = None
    channel_cells, channel_posterior, channel_prediction = [0] * 4, [0] * 4, [0] * 4
    n_cells = n_posterior = n_prediction = 0
    couplings, receiving = [0] * 3, [0] * 3
    strict_gain, zero_gain, strict_loss, zero_loss = [0] * 4, [0] * 4, [0] * 3, [0] * 3
    positive_residual = known_n = 0
    for bid, (weight, belief) in enumerate(prepared["beliefs"]):
        row, baseline, n, h, row_risks, row_extras, losses = _score_belief(
            bid, weight, belief, prepared, family
        )
        rows.append(row)
        baseline_risk = _bounded(baseline_risk + weight * baseline["risk"])
        n_risk = _bounded(n_risk + weight * n)
        h_risk = _bounded(h_risk + weight * h)
        for q, value in baseline["law"].items():
            _add(prediction, q, _bounded(weight * value))
        n_control = row["controls"]["N"]["cells"]
        n_cells += len(n_control)
        n_posterior += sum(len(cell["posterior"]) for cell in n_control)
        n_prediction += sum(len(cell["prediction"]) for cell in n_control)
        for i, risk in enumerate(row_risks):
            risks[i] = _bounded(risks[i] + weight * risk)
            gains[i] = _bounded(gains[i] + weight * (baseline["risk"] - risk))
            extra_gains[i] = _bounded(extra_gains[i] + weight * row_extras[i])
            cells = row["channels"][i]["cells"]
            channel_cells[i] += len(cells)
            channel_posterior[i] += sum(len(cell["posterior"]) for cell in cells)
            channel_prediction[i] += sum(len(cell["prediction"]) for cell in cells)
            strict_gain[i] += int(row_extras[i] > 0)
            zero_gain[i] += int(row_extras[i] == 0)
            if row_extras[i] > 0 and first_strict_gain[i] is None:
                first_strict_gain[i] = bid
            if row_extras[i] == 0 and first_zero_gain[i] is None:
                first_zero_gain[i] = bid
        _require(n_cells + sum(channel_cells) <= CELL_CAP, "all retained cell cap")
        _require(
            n_posterior + sum(channel_posterior) <= READOUT_POSTERIOR_CAP, "readout posterior cap"
        )
        _require(n_prediction + sum(channel_prediction) <= PREDICTION_CAP, "readout prediction cap")
        for i, loss in enumerate(losses):
            adjacent[i] = _bounded(adjacent[i] + weight * loss)
            couplings[i] += len(row["garblings"][i]["couplings"])
            receiving[i] += len(row["garblings"][i]["receiving_checks"])
            strict_loss[i] += int(loss > 0)
            zero_loss[i] += int(loss == 0)
            if loss > 0 and first_strict_loss[i] is None:
                first_strict_loss[i] = bid
            if loss == 0 and first_zero_loss[i] is None:
                first_zero_loss[i] = bid
        _require(sum(couplings) <= COUPLING_CAP, "retained coupling atom cap")
        _require(sum(receiving) <= RECEIVING_CAP, "retained receiving check cap")
        positive_residual += int(h > 0)
        known_n += int(row["checks"]["N_already_known"])
        if h > 0 and first_positive_residual is None:
            first_positive_residual = bid
        if h == 0 and first_zero_residual is None:
            first_zero_residual = bid
    _require(_sum(prediction.values()) == 1, "weighted prediction normalization")
    _require(
        h_risk <= risks[0] <= risks[1] <= risks[2] <= risks[3] == n_risk <= baseline_risk,
        "aggregate risk order/endpoints",
    )
    for i in range(4):
        _require(
            gains[i] == baseline_risk - risks[i] and extra_gains[i] == n_risk - risks[i],
            "aggregate total/additional gains",
        )
    for i in range(3):
        _require(adjacent[i] == risks[i + 1] - risks[i], "aggregate adjacent losses")
    _require(_sum(adjacent) == extra_gains[0], "aggregate telescoping")
    built = prepared["built"]
    profile_atoms = sum(len(row["transitions"]) for row in built["profiles"])
    alphabet, _, _, channel_model, global_atoms = family
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
        "channel_model": channel_model,
        "beliefs": rows,
        "aggregate": {
            "total_weight": [1, 1],
            "prediction": _question_law(prediction),
            "baseline_risk": _wire_fraction(baseline_risk),
            "N_risk": _wire_fraction(n_risk),
            "H_risk": _wire_fraction(h_risk),
            "channels": [
                {
                    "level": _wire_fraction(LEVELS[i]),
                    "expected_risk": _wire_fraction(risks[i]),
                    "gain": _wire_fraction(gains[i]),
                    "gain_over_N": _wire_fraction(extra_gains[i]),
                    "retained_gain_fraction": _wire_fraction(extra_gains[i] / extra_gains[0])
                    if extra_gains[0]
                    else None,
                }
                for i in range(4)
            ],
            "adjacent_risk_increase": [_wire_fraction(loss) for loss in adjacent],
        },
        "witnesses": {
            "first_strict_gain": first_strict_gain,
            "first_zero_gain": first_zero_gain,
            "first_strict_loss": first_strict_loss,
            "first_zero_loss": first_zero_loss,
            "first_positive_oracle_residual": first_positive_residual,
            "first_zero_oracle_residual": first_zero_residual,
        },
        "counts": {
            "classes": len(prepared["qrows"]),
            "beliefs": len(rows),
            "profile_atoms": profile_atoms,
            "kernel_atoms": sum(map(len, prepared["kernel"])),
            "alphabet_fibers": len(alphabet),
            "alphabet_values": sum(map(len, alphabet.values())),
            "global_channel_atoms": global_atoms,
            "posterior_atoms": prepared["posterior_atoms"],
            "channel_cells": channel_cells,
            "channel_posterior_atoms": channel_posterior,
            "channel_prediction_atoms": channel_prediction,
            "N_cells": n_cells,
            "N_posterior_atoms": n_posterior,
            "N_prediction_atoms": n_prediction,
            "coupling_atoms": couplings,
            "receiving_checks": receiving,
            "strict_gain_beliefs": strict_gain,
            "no_gain_beliefs": zero_gain,
            "strict_loss_beliefs": strict_loss,
            "no_loss_beliefs": zero_loss,
            "positive_oracle_residual_beliefs": positive_residual,
            "known_N_beliefs": known_n,
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= WORKING_CAP, "W output working cap")
    return _copy(result)
