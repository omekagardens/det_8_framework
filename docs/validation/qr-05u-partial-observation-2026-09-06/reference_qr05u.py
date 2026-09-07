"""Independent unnormalized joint-class-path filtering reference for QR-05U.

The only producer inputs are local class deletion rows and explicit labels.
Complete subset profiles are reconstructed by the locally carried ordered
word/factorial route. Joint path masses are accumulated before conditioning.
No raw order, prior artifact, other executor, or mutable core is accessed.
This is exact prior/design-relative finite classical filtering.
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
FIRST_CAP = 512
HISTORY_CAP = 16384
POSTERIOR_CAP = 262144
PREDICTION_CAP = 262144


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
    _require(type(classes) is list and 1 <= len(classes) <= 512, "local class resource bound")
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
        sum(len(row[name]) for row in classes for name in ("odd", "even")) <= 3072,
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
        _require(atoms <= 32768, "reconstructed profile atom resource bound")
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


def _input_fraction(pair, positive=False):
    _require(type(pair) is list and len(pair) == 2, "fraction must be a native pair")
    numerator, denominator = pair
    _require(
        type(numerator) is int
        and type(denominator) is int
        and numerator >= 0
        and denominator > 0
        and numerator.bit_length() <= INPUT_BITS
        and denominator.bit_length() <= INPUT_BITS,
        "input fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must be reduced")
    value = _bounded(F(numerator, denominator))
    _require(0 <= value <= 1 and (not positive or value > 0), "probability interval/support")
    return value


def _wire_fraction(value):
    value = _bounded(value)
    _require(value >= 0, "negative probability")
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
    _fields(problem, ("schema_version", "family", "model", "prior", "rates"), "U problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05u-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05u_partial_observation",
        "U schema/family",
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
    prior_atoms = problem["prior"]
    _require(type(prior_atoms) is list and 1 <= len(prior_atoms) <= 16, "prior support bound")
    prior = {}
    previous = -1
    for atom in prior_atoms:
        _fields(atom, ("class_id", "probability"), "prior atom fields")
        cid = atom["class_id"]
        _integer(cid, 0, len(classes) - 1)
        _require(cid > previous, "prior labels must be sorted unique")
        previous = cid
        prior[cid] = _input_fraction(atom["probability"], positive=True)
    _require(_sum(prior.values()) == 1, "prior must already normalize")
    rate_wire = problem["rates"]
    _require(type(rate_wire) is list and len(rate_wire) == 3, "exactly three rate pairs")
    rates = []
    for pair in rate_wire:
        _require(type(pair) is list and len(pair) == 2, "two-color rate pair")
        rates.append(tuple(_input_fraction(value) for value in pair))
    _require(len(_canonical(problem)) <= WORKING_CAP, "problem working cap")
    built = reconstruct_profiles(local_model)
    cache = {}
    kernels = []
    for pair in rates:
        if pair not in cache:
            cache[pair] = _kernel(built["profiles"], pair)
        kernels.append(cache[pair])
    return {
        "model_sha256": _digest(model),
        "built": built,
        "prior": prior,
        "rates": rates,
        "rate_wire": _copy(rate_wire),
        "observations": observations,
        "questions": questions,
        "kernels": kernels,
    }


def _records(records, observations):
    _native_json(records)
    _require(type(records) is list and len(records) == 2, "exactly two observations required")
    known = set(observations)
    result = []
    for observation in records:
        _require(type(observation) is list and len(observation) == 5, "received record shape")
        for value in observation:
            _integer(value, 0)
        key = tuple(observation)
        _require(key in known, "unknown observation label")
        result.append(key)
    return result


def _first_difference(left, right):
    for question in sorted(left.keys() | right.keys()):
        l, r = left.get(question, F(0)), right.get(question, F(0))
        if l != r:
            return question, l, r
    raise ValueError("different question laws have no differing atom")


def _controls(keys, joint, predictions, latest_predictions, kernel3, questions):
    grouped = {}
    for key in keys:
        grouped.setdefault(key[1], []).append(key)
    positions = {key: i for group in grouped.values() for i, key in enumerate(group)}
    history_witness = forgetting_witness = map_witness = None
    pair_count = pair_differences = forgetting_differences = map_differences = 0
    for left in keys:
        for right in grouped[left[1]][positions[left] + 1 :]:
            pair_count += 1
            lhs, rhs = predictions[left], predictions[right]
            if lhs != rhs:
                pair_differences += 1
                if history_witness is None:
                    question, l, r = _first_difference(lhs, rhs)
                    history_witness = {
                        "left": [list(v) for v in left],
                        "right": [list(v) for v in right],
                        "question": list(question),
                        "left_probability": _wire_fraction(l),
                        "right_probability": _wire_fraction(r),
                    }
        prediction = predictions[left]
        forgotten = latest_predictions[left[1]]
        if prediction != forgotten:
            forgetting_differences += 1
            if forgetting_witness is None:
                question, l, r = _first_difference(prediction, forgotten)
                forgetting_witness = {
                    "observations": [list(v) for v in left],
                    "question": list(question),
                    "history_probability": _wire_fraction(l),
                    "latest_only_probability": _wire_fraction(r),
                }
        map_class = min(joint[left], key=lambda cid: (-joint[left][cid], cid))
        point_prediction = _push_questions(kernel3[map_class], questions)
        if prediction != point_prediction:
            map_differences += 1
            if map_witness is None:
                question, l, r = _first_difference(prediction, point_prediction)
                map_witness = {
                    "observations": [list(v) for v in left],
                    "map_class_id": map_class,
                    "question": list(question),
                    "mixture_probability": _wire_fraction(l),
                    "map_probability": _wire_fraction(r),
                }
    return (
        {
            "history_witness": history_witness,
            "forgetting_witness": forgetting_witness,
            "map_witness": map_witness,
        },
        {
            "history_pairs_compared": pair_count,
            "history_pairs_different": pair_differences,
            "forgetting_comparisons": len(keys),
            "forgetting_differences": forgetting_differences,
            "map_comparisons": len(keys),
            "map_differences": map_differences,
        },
    )


def _analyze(prepared):
    prior = prepared["prior"]
    observations, questions = prepared["observations"], prepared["questions"]
    kernel1, kernel2, kernel3 = prepared["kernels"]
    first, joint = {}, {}
    after_first, after_second = {}, {}
    # Joint class paths are summed before any posterior is normalized.
    for source, prior_mass in prior.items():
        for middle, p1 in kernel1[source].items():
            mass1 = _bounded(prior_mass * p1)
            y1 = observations[middle]
            _add(first.setdefault(y1, {}), middle, mass1)
            _add(after_first, middle, mass1)
            _require(len(first) <= FIRST_CAP, "first observation resource bound")
            for current, p2 in kernel2[middle].items():
                mass2 = _bounded(mass1 * p2)
                key = (y1, observations[current])
                _add(joint.setdefault(key, {}), current, mass2)
                _add(after_second, current, mass2)
                _require(len(joint) <= HISTORY_CAP, "received history resource bound")
    _require(
        sum(len(masses) for masses in joint.values()) <= POSTERIOR_CAP,
        "history posterior atom resource bound",
    )
    first_keys, history_keys = sorted(first), sorted(joint)
    first_likelihood = {key: _sum(first[key].values()) for key in first_keys}
    joint_likelihood = {key: _sum(joint[key].values()) for key in history_keys}
    first_posterior = {key: _normalise(first[key]) for key in first_keys}
    posterior = {key: _normalise(joint[key]) for key in history_keys}
    prediction = {}
    latest = {}
    for key in history_keys:
        next_joint = _push_questions(_propagate(joint[key], kernel3), questions)
        prediction[key] = _normalise(next_joint)
        for current, mass in joint[key].items():
            _add(latest.setdefault(key[1], {}), current, mass)
    _require(
        sum(len(law) for law in prediction.values()) <= PREDICTION_CAP,
        "history prediction atom resource bound",
    )
    latest_keys = sorted(latest)
    latest_likelihood = {key: _sum(latest[key].values()) for key in latest_keys}
    latest_posterior = {key: _normalise(latest[key]) for key in latest_keys}
    latest_prediction = {
        key: _normalise(_push_questions(_propagate(latest[key], kernel3), questions))
        for key in latest_keys
    }
    after_third = _propagate(after_second, kernel3)
    unconditional_question = _push_questions(after_third, questions)
    _require(_sum(first_likelihood.values()) == 1, "first evidence normalization")
    _require(_sum(joint_likelihood.values()) == 1, "joint evidence normalization")
    for masses in (after_first, after_second, after_third, unconditional_question):
        _require(_sum(masses.values()) == 1, "unconditional normalization")
    for key, masses in first_posterior.items():
        _require(
            _sum(masses.values()) == 1 and all(observations[cid] == key for cid in masses),
            "first posterior support",
        )
    for key, masses in posterior.items():
        _require(
            _sum(masses.values()) == 1 and all(observations[cid] == key[1] for cid in masses),
            "current H2 posterior support",
        )
    for key, masses in latest_posterior.items():
        _require(
            _sum(masses.values()) == 1 and all(observations[cid] == key for cid in masses),
            "latest posterior support",
        )
    marginal_first, marginal_second, marginal_latest = {}, {}, {}
    for key, masses in first_posterior.items():
        for cid, probability in masses.items():
            _add(marginal_first, cid, _bounded(first_likelihood[key] * probability))
    for key, masses in posterior.items():
        for cid, probability in masses.items():
            _add(marginal_second, cid, _bounded(joint_likelihood[key] * probability))
    for key, masses in latest_posterior.items():
        for cid, probability in masses.items():
            _add(marginal_latest, cid, _bounded(latest_likelihood[key] * probability))
    _require(
        marginal_first == after_first
        and marginal_second == after_second
        and marginal_latest == after_second,
        "posterior marginalization",
    )
    for y1 in first_keys:
        average = {}
        conditional_total = F(0)
        for key in history_keys:
            if key[0] != y1:
                continue
            conditional = _bounded(joint_likelihood[key] / first_likelihood[y1])
            conditional_total = _bounded(conditional_total + conditional)
            for question, probability in prediction[key].items():
                _add(average, question, _bounded(conditional * probability))
        expected = _push_questions(
            _propagate(_propagate(first_posterior[y1], kernel2), kernel3), questions
        )
        _require(
            conditional_total == 1 and average == expected, "first-observation prediction tower"
        )
    for y2 in latest_keys:
        average = {}
        conditional_total = F(0)
        for key in history_keys:
            if key[1] != y2:
                continue
            conditional = _bounded(joint_likelihood[key] / latest_likelihood[y2])
            conditional_total = _bounded(conditional_total + conditional)
            for question, probability in prediction[key].items():
                _add(average, question, _bounded(conditional * probability))
        _require(
            conditional_total == 1 and average == latest_prediction[y2],
            "latest-observation prediction tower",
        )
    product_rates = tuple(
        _bounded(prepared["rates"][0][c] * prepared["rates"][1][c] * prepared["rates"][2][c])
        for c in range(2)
    )
    direct_kernel = _kernel(prepared["built"]["profiles"], product_rates)
    _require(
        _propagate(prior, direct_kernel) == after_third, "unconditional three-stage composition"
    )
    controls, control_counts = _controls(
        history_keys, joint, prediction, latest_prediction, kernel3, questions
    )
    first_rows = [
        {
            "observation": list(key),
            "likelihood": _wire_fraction(first_likelihood[key]),
            "posterior": _belief(first_posterior[key]),
        }
        for key in first_keys
    ]
    history_rows = [
        {
            "observations": [list(value) for value in key],
            "likelihood": _wire_fraction(joint_likelihood[key]),
            "conditional_likelihood": _wire_fraction(
                _bounded(joint_likelihood[key] / first_likelihood[key[0]])
            ),
            "posterior": _belief(posterior[key]),
            "prediction": _question_law(prediction[key]),
        }
        for key in history_keys
    ]
    latest_rows = [
        {
            "observation": list(key),
            "likelihood": _wire_fraction(latest_likelihood[key]),
            "posterior": _belief(latest_posterior[key]),
            "prediction": _question_law(latest_prediction[key]),
        }
        for key in latest_keys
    ]
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
        "prior": _belief(prior),
        "rates": prepared["rate_wire"],
        "kernel_sha256": [_digest(_kernel_wire(kernel)) for kernel in prepared["kernels"]],
        "first": first_rows,
        "histories": history_rows,
        "latest_only": latest_rows,
        "unconditional": {
            "after_first": _belief(after_first),
            "after_second": _belief(after_second),
            "after_third": _belief(after_third),
            "next_prediction": _question_law(unconditional_question),
        },
        "controls": controls,
        "checks": {
            "first_normalization": True,
            "joint_normalization": True,
            "posterior_normalization": True,
            "posterior_support": True,
            "tower_first": True,
            "tower_latest": True,
            "three_step_composition": True,
            "max_abs_residual": [0, 1],
        },
        "counts": {
            "classes": len(built["profiles"]),
            "profile_atoms": profile_atoms,
            "kernel_atoms": [sum(len(row) for row in kernel) for kernel in prepared["kernels"]],
            "first_histories": len(first_rows),
            "histories": len(history_rows),
            "first_posterior_atoms": sum(len(row["posterior"]) for row in first_rows),
            "history_posterior_atoms": sum(len(row["posterior"]) for row in history_rows),
            "history_prediction_atoms": sum(len(row["prediction"]) for row in history_rows),
            "latest_observations": len(latest_rows),
            "latest_posterior_atoms": sum(len(row["posterior"]) for row in latest_rows),
            "latest_prediction_atoms": sum(len(row["prediction"]) for row in latest_rows),
            **control_counts,
        },
    }
    _native_json(result)
    _require(len(_canonical(result)) <= WORKING_CAP, "filtering output working cap")
    return _copy(result)


def analyze(problem):
    return _analyze(_prepare(problem))


def filter_history(problem, records):
    prepared = _prepare(problem)
    # Validate BOTH known records before either impossible-evidence branch.
    y1, y2 = _records(records, prepared["observations"])
    kernel1, kernel2, kernel3 = prepared["kernels"]
    first_joint = {}
    for source, mass in prepared["prior"].items():
        for target, probability in kernel1[source].items():
            if prepared["observations"][target] == y1:
                _add(first_joint, target, _bounded(mass * probability))
    impossible = {
        "status": "impossible",
        "failed_stage": 1,
        "likelihood": [0, 1],
        "posterior": None,
        "prediction": None,
    }
    if not first_joint:
        return impossible
    second_joint = {}
    for middle, mass in first_joint.items():
        for current, probability in kernel2[middle].items():
            if prepared["observations"][current] == y2:
                _add(second_joint, current, _bounded(mass * probability))
    if not second_joint:
        impossible["failed_stage"] = 2
        return impossible
    prediction = _normalise(
        _push_questions(_propagate(second_joint, kernel3), prepared["questions"])
    )
    result = {
        "status": "possible",
        "failed_stage": None,
        "likelihood": _wire_fraction(_sum(second_joint.values())),
        "posterior": _belief(_normalise(second_joint)),
        "prediction": _question_law(prediction),
    }
    _native_json(result)
    _require(len(_canonical(result)) <= WORKING_CAP, "conditional output working cap")
    return _copy(result)
