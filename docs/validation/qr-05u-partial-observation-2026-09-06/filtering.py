"""QR-05U summary-only exact filtering with sequential Bayes updates.

The class-local rank constructor is statically copied from this primary's
S/T lineage. No raw order, artifact, other executor or mutable application
module is read at runtime. Observation/question labels are explicit inputs;
their scientific authentication belongs to the separate producer bridge.
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
FIRST_CAP = 512
HISTORY_CAP = 16384
POSTERIOR_CAP = 262144
PREDICTION_CAP = 262144


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
        if depth > 128 or id(item) in active:
            raise ValueError("native JSON is cyclic or exceeds the bounded schema depth")
        if id(item) in completed:
            if depth + completed[id(item)][1] > 128:
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


def _fraction(value, positive=False):
    if type(value) is not list or len(value) != 2:
        raise ValueError("a probability must be a native numerator/denominator pair")
    numerator, denominator = value
    _integer(numerator, 1 if positive else 0, (1 << INPUT_BITS) - 1)
    _integer(denominator, 1, (1 << INPUT_BITS) - 1)
    if numerator > denominator or gcd(numerator, denominator) != 1:
        raise ValueError("probability is outside [0,1] or is not in reduced canonical form")
    return Fraction(numerator, denominator)


def _checked(value):
    if type(value) is not Fraction:
        raise ValueError("internal probability must remain exactly rational")
    if (
        value < 0
        or value > 1
        or value.numerator.bit_length() > BIT_LIMIT
        or value.denominator.bit_length() > BIT_LIMIT
    ):
        raise ValueError("probability exceeds its exact arithmetic bound")
    return value


def _pair(value):
    _checked(value)
    return [value.numerator, value.denominator]


def _sum(values):
    result = Fraction(0)
    for value in values:
        result = _checked(result + value)
    return result


def _add_mass(mapping, key, probability):
    _checked(probability)
    if probability:
        mapping[key] = _checked(mapping.get(key, Fraction(0)) + probability)


def _unit(mapping, message):
    if not mapping or _sum(mapping.values()) != 1:
        raise ValueError(message)
    if any(not value for value in mapping.values()):
        raise ValueError("positive distributions must omit zero atoms")


def _belief_wire(belief):
    return [
        {"class_id": class_id, "probability": _pair(probability)}
        for class_id, probability in sorted(belief.items())
        if probability
    ]


def _question_wire(law):
    return [
        {"value": list(value), "probability": _pair(probability)}
        for value, probability in sorted(law.items())
        if probability
    ]


def _kernel(profiles, rates):
    """Positive count-basis evaluation, not a fitted polynomial or raw oracle."""
    x, y = rates
    _checked(x)
    _checked(y)
    result, monomials = [], {}
    for profile in profiles:
        odd, even = profile["parent_color_sizes"]
        row = {}
        for atom in profile["transitions"]:
            m, n = atom["retained_color_sizes"]
            key = (odd, even, m, n)
            if key not in monomials:
                monomials[key] = _checked(
                    x**m * (1 - x) ** (odd - m) * y**n * (1 - y) ** (even - n)
                )
            probability = _checked(atom["multiplicity"] * monomials[key])
            _add_mass(row, atom["target_class"], probability)
        _unit(row, "reconstructed class kernel is not stochastic")
        result.append(row)
    return result


def _kernel_wire(kernel):
    return [
        {
            "class_id": class_id,
            "transitions": [
                {"target_class": target, "probability": _pair(probability)}
                for target, probability in sorted(row.items())
            ],
        }
        for class_id, row in enumerate(kernel)
    ]


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "model", "prior", "rates"))
    if (
        problem["schema_version"] != "det8-qr05u-problem-v1"
        or problem["family"] != "qr05u_partial_observation"
    ):
        raise ValueError("unknown partial-observation investigation")
    _fields(problem["model"], ("classes", "labels"))
    model = json.loads(canonical(problem["model"]))
    reconstructed = reconstruct_profiles(
        {"schema_version": "det8-qr05s-local-v1", "classes": model["classes"]}
    )
    classes, labels = model["classes"], model["labels"]
    if type(labels) is not list or len(labels) != len(classes):
        raise ValueError("labels must cover exactly the supplied local classes")
    values = []
    for class_id, label in enumerate(labels):
        _fields(label, ("class_id", "observation", "question"))
        _integer(label["class_id"], class_id, class_id)
        observation, question = label["observation"], label["question"]
        if (
            type(observation) is not list
            or len(observation) != 5
            or type(question) is not list
            or len(question) != 7
        ):
            raise ValueError("observation/question label dimensions are invalid")
        frame = classes[class_id]["frame_id"]
        odd, even = classes[class_id]["parent_color_sizes"]
        _integer(observation[0], frame, frame)
        _integer(observation[1], 1, 1)
        _integer(observation[2], odd + even + frame, odd + even + frame)
        _integer(observation[3], 0, _choose(observation[2], 2))
        _integer(observation[4], 0, _choose(observation[2], 3))
        for index, expected in enumerate(observation):
            _integer(question[index], expected, expected)
        limit = _choose(odd, 2) * _choose(even, 2)
        _integer(question[5], 0, limit)
        _integer(question[6], 0, limit)
        values.append((tuple(observation), tuple(question)))
    prior = problem["prior"]
    if type(prior) is not list or not 1 <= len(prior) <= 16:
        raise ValueError("prior support is outside its declared bound")
    belief, previous = {}, -1
    for atom in prior:
        _fields(atom, ("class_id", "probability"))
        _integer(atom["class_id"], previous + 1, len(classes) - 1)
        previous = atom["class_id"]
        belief[previous] = _fraction(atom["probability"], positive=True)
    _unit(belief, "prior must sum exactly to one without normalization")
    supplied_rates = problem["rates"]
    if type(supplied_rates) is not list or len(supplied_rates) != 3:
        raise ValueError("exactly three thinning rate pairs are required")
    rates = []
    for pair in supplied_rates:
        if type(pair) is not list or len(pair) != 2:
            raise ValueError("a thinning rate needs two native probability pairs")
        rates.append((_fraction(pair[0]), _fraction(pair[1])))
    profiles = reconstructed["profiles"]
    kernels = [_kernel(profiles, pair) for pair in rates]
    products = (
        _checked(rates[0][0] * rates[1][0] * rates[2][0]),
        _checked(rates[0][1] * rates[1][1] * rates[2][1]),
    )
    return {
        "model": model,
        "reconstructed": reconstructed,
        "labels": values,
        "alphabet": {label[0] for label in values},
        "prior": belief,
        "rates": rates,
        "kernels": kernels,
        "product_kernel": _kernel(profiles, products),
    }


def _propagate(belief, kernel):
    _unit(belief, "propagation requires a normalized positive class belief")
    result = {}
    for source, mass in belief.items():
        for target, probability in kernel[source].items():
            _add_mass(result, target, _checked(mass * probability))
    _unit(result, "class propagation lost probability mass")
    return result


def _question_pushforward(belief, labels):
    _unit(belief, "question pushforward requires a normalized belief")
    result = {}
    for class_id, mass in belief.items():
        _add_mass(result, labels[class_id][1], mass)
    _unit(result, "question pushforward lost probability mass")
    return result


def _predict(belief, kernel, labels):
    return _question_pushforward(_propagate(belief, kernel), labels)


def _observation_groups(belief, labels):
    _unit(belief, "conditioning requires a normalized predictive belief")
    groups = {}
    for class_id, mass in belief.items():
        groups.setdefault(labels[class_id][0], {})[class_id] = mass
    if len(groups) > FIRST_CAP:
        raise ValueError("received-observation support exceeds its declared bound")
    return groups


def _normalized_group(group):
    evidence = _sum(group.values())
    if not evidence:
        return evidence, None
    belief = {class_id: _checked(mass / evidence) for class_id, mass in group.items()}
    _unit(belief, "posterior normalization failed")
    return evidence, belief


def _condition(belief, observation, labels):
    group = {
        class_id: mass for class_id, mass in belief.items() if labels[class_id][0] == observation
    }
    return _normalized_group(group)


def _law_difference(left, right):
    for value in sorted(set(left) | set(right)):
        a, b = left.get(value, Fraction(0)), right.get(value, Fraction(0))
        if a != b:
            return {
                "question": list(value),
                "left_probability": _pair(a),
                "right_probability": _pair(b),
            }
    raise ValueError("different complete question laws have no separating value")


def _records(prepared, records):
    _native(records)
    if type(records) is not list or len(records) != 2:
        raise ValueError("conditioning requires exactly two received records")
    result = []
    for record in records:
        if type(record) is not list or len(record) != 5:
            raise ValueError("a received observation must be a native five-vector")
        if any(type(value) is not int for value in record):
            raise ValueError("received observation components must be native integers")
        value = tuple(record)
        if value not in prepared["alphabet"]:
            raise ValueError("unknown received observation")
        result.append(value)
    return result


def filter_history(problem, records):
    """Condition one received history; impossible evidence never gets a posterior."""
    prepared = _prepare(problem)
    observations = _records(prepared, records)
    belief, likelihood = prepared["prior"], Fraction(1)
    for index, observation in enumerate(observations):
        predictive = _propagate(belief, prepared["kernels"][index])
        evidence, posterior = _condition(predictive, observation, prepared["labels"])
        if not evidence:
            return {
                "status": "impossible",
                "failed_stage": index + 1,
                "likelihood": [0, 1],
                "posterior": None,
                "prediction": None,
            }
        likelihood = _checked(likelihood * evidence)
        belief = posterior
    result = {
        "status": "possible",
        "failed_stage": None,
        "likelihood": _pair(likelihood),
        "posterior": _belief_wire(belief),
        "prediction": _question_wire(_predict(belief, prepared["kernels"][2], prepared["labels"])),
    }
    return json.loads(canonical(result))


def _history_values(history):
    return [list(value) for value in history["observations"]]


def _witnesses(histories, latest, kernel, labels):
    by_latest = {}
    laws = []
    for index, row in enumerate(histories):
        by_latest.setdefault(row["observations"][1], []).append(index)
        laws.append(tuple(sorted(row["prediction"].items())))
    history_witness = forgetting_witness = map_witness = None
    pairs_compared = pairs_different = forgetting_differences = map_differences = 0
    map_predictions = {}
    for index, row in enumerate(histories):
        for other in by_latest[row["observations"][1]]:
            if other <= index:
                continue
            pairs_compared += 1
            different = laws[index] != laws[other]
            if different:
                pairs_different += 1
                if history_witness is None:
                    history_witness = {
                        "left": _history_values(row),
                        "right": _history_values(histories[other]),
                        **_law_difference(row["prediction"], histories[other]["prediction"]),
                    }
        latest_law = latest[row["observations"][1]]["prediction"]
        different = row["prediction"] != latest_law
        if different:
            forgetting_differences += 1
            if forgetting_witness is None:
                difference = _law_difference(row["prediction"], latest_law)
                forgetting_witness = {
                    "observations": _history_values(row),
                    "question": difference["question"],
                    "history_probability": difference["left_probability"],
                    "latest_only_probability": difference["right_probability"],
                }
        chosen = min(row["posterior"], key=lambda class_id: (-row["posterior"][class_id], class_id))
        if chosen not in map_predictions:
            map_predictions[chosen] = _predict({chosen: Fraction(1)}, kernel, labels)
        map_law = map_predictions[chosen]
        different = row["prediction"] != map_law
        if different:
            map_differences += 1
            if map_witness is None:
                difference = _law_difference(row["prediction"], map_law)
                map_witness = {
                    "observations": _history_values(row),
                    "map_class_id": chosen,
                    "question": difference["question"],
                    "mixture_probability": difference["left_probability"],
                    "map_probability": difference["right_probability"],
                }
    return (
        {
            "history_witness": history_witness,
            "forgetting_witness": forgetting_witness,
            "map_witness": map_witness,
        },
        {
            "history_pairs_compared": pairs_compared,
            "history_pairs_different": pairs_different,
            "forgetting_comparisons": len(histories),
            "forgetting_differences": forgetting_differences,
            "map_comparisons": len(histories),
            "map_differences": map_differences,
        },
    )


def _mixture(distributions):
    result = {}
    for weight, distribution in distributions:
        _checked(weight)
        for key, probability in distribution.items():
            _add_mass(result, key, _checked(weight * probability))
    return result


def _audit(first, histories, latest, unconditional, prepared):
    labels = prepared["labels"]
    after_first, after_second, after_third = unconditional
    if _sum(row["likelihood"] for row in first) != 1:
        raise ValueError("first-record evidence does not sum to one")
    if _sum(row["likelihood"] for row in histories) != 1:
        raise ValueError("joint two-record evidence does not sum to one")
    if _sum(row["likelihood"] for row in latest.values()) != 1:
        raise ValueError("latest-record evidence does not sum to one")
    first_index = {row["observation"]: row for row in first}
    by_first, by_latest = {}, {}
    for row in first:
        _unit(row["posterior"], "first posterior does not normalize")
        if any(
            labels[class_id][0] != row["observation"] or class_id not in after_first
            for class_id in row["posterior"]
        ):
            raise ValueError("first posterior has unsupported classes")
    for row in histories:
        y1, y2 = row["observations"]
        _unit(row["posterior"], "history posterior does not normalize")
        _unit(row["prediction"], "history question law does not normalize")
        if any(
            labels[class_id][0] != y2 or class_id not in first_index[y1]["after_second"]
            for class_id in row["posterior"]
        ):
            raise ValueError("history posterior has unsupported classes")
        if row["likelihood"] != _checked(
            first_index[y1]["likelihood"] * row["conditional_likelihood"]
        ):
            raise ValueError("joint and conditional history evidence disagree")
        by_first.setdefault(y1, []).append(row)
        by_latest.setdefault(y2, []).append(row)
    for observation, row in latest.items():
        _unit(row["posterior"], "latest-only posterior does not normalize")
        _unit(row["prediction"], "latest-only question law does not normalize")
        if any(
            labels[class_id][0] != observation or class_id not in after_second
            for class_id in row["posterior"]
        ):
            raise ValueError("latest-only posterior has unsupported classes")
    # Marginalizing posterior beliefs must recover the unconditioned current state.
    if _mixture((row["likelihood"], row["posterior"]) for row in first) != after_first:
        raise ValueError("first posterior marginal does not recover the first current law")
    if _mixture((row["likelihood"], row["posterior"]) for row in histories) != after_second:
        raise ValueError("history posterior marginal does not recover the second current law")
    if _mixture((row["likelihood"], row["posterior"]) for row in latest.values()) != after_second:
        raise ValueError("latest posterior marginal does not recover the second current law")
    for observation, rows in by_first.items():
        if _sum(row["conditional_likelihood"] for row in rows) != 1:
            raise ValueError("conditional second-record evidence does not normalize")
        actual = _mixture((row["conditional_likelihood"], row["prediction"]) for row in rows)
        expected = _predict(
            first_index[observation]["after_second"], prepared["kernels"][2], labels
        )
        if actual != expected:
            raise ValueError("first-record prediction tower identity failed")
    for observation, rows in by_latest.items():
        evidence = latest[observation]["likelihood"]
        if _sum(row["likelihood"] for row in rows) != evidence:
            raise ValueError("latest likelihood differs from the joint history marginal")
        weights = [_checked(row["likelihood"] / evidence) for row in rows]
        if _sum(weights) != 1:
            raise ValueError("earlier-record posterior probabilities do not normalize")
        actual = _mixture(
            (weight, row["prediction"]) for weight, row in zip(weights, rows, strict=True)
        )
        if actual != latest[observation]["prediction"]:
            raise ValueError("latest-record prediction tower identity failed")
        posterior = _mixture(
            (weight, row["posterior"]) for weight, row in zip(weights, rows, strict=True)
        )
        if posterior != latest[observation]["posterior"]:
            raise ValueError("latest current posterior is not the earlier-record mixture")
    if _propagate(prepared["prior"], prepared["product_kernel"]) != after_third:
        raise ValueError("unconditional three-stage law differs from product-rate thinning")
    if _mixture((row["likelihood"], row["prediction"]) for row in histories) != (
        _question_pushforward(after_third, labels)
    ):
        raise ValueError("history predictions do not marginalize to the third question law")
    return {
        "first_normalization": True,
        "joint_normalization": True,
        "posterior_normalization": True,
        "posterior_support": True,
        "tower_first": True,
        "tower_latest": True,
        "three_step_composition": True,
        "max_abs_residual": [0, 1],
    }


def analyze(problem):
    """Enumerate positive records using sequential normalized Bayes filtering."""
    prepared = _prepare(problem)
    labels, kernels = prepared["labels"], prepared["kernels"]
    after_first = _propagate(prepared["prior"], kernels[0])
    after_second = _propagate(after_first, kernels[1])
    after_third = _propagate(after_second, kernels[2])
    first, histories = [], []
    posterior_atoms = prediction_atoms = 0
    for observation, group in sorted(_observation_groups(after_first, labels).items()):
        likelihood, posterior = _normalized_group(group)
        second = _propagate(posterior, kernels[1])
        first.append(
            {
                "observation": observation,
                "likelihood": likelihood,
                "posterior": posterior,
                "after_second": second,
            }
        )
        if len(first) > FIRST_CAP:
            raise ValueError("first-observation count exceeds its declared bound")
        for next_observation, next_group in sorted(_observation_groups(second, labels).items()):
            conditional, current = _normalized_group(next_group)
            prediction = _predict(current, kernels[2], labels)
            histories.append(
                {
                    "observations": (observation, next_observation),
                    "likelihood": _checked(likelihood * conditional),
                    "conditional_likelihood": conditional,
                    "posterior": current,
                    "prediction": prediction,
                }
            )
            posterior_atoms += len(current)
            prediction_atoms += len(prediction)
            if len(histories) > HISTORY_CAP:
                raise ValueError("positive history count exceeds its declared bound")
            if posterior_atoms > POSTERIOR_CAP or prediction_atoms > PREDICTION_CAP:
                raise ValueError("history probability atoms exceed their declared bound")
    latest = {}
    for observation, group in sorted(_observation_groups(after_second, labels).items()):
        likelihood, posterior = _normalized_group(group)
        latest[observation] = {
            "likelihood": likelihood,
            "posterior": posterior,
            "prediction": _predict(posterior, kernels[2], labels),
        }
    checks = _audit(first, histories, latest, (after_first, after_second, after_third), prepared)
    controls, control_counts = _witnesses(histories, latest, kernels[2], labels)
    reconstruction = prepared["reconstructed"]
    kernel_rows = [_kernel_wire(kernel) for kernel in kernels]
    result = {
        "model_sha256": _digest(prepared["model"]),
        "reconstruction": {
            "profiles_sha256": _digest(reconstruction["profiles"]),
            "profile_atoms": sum(len(row["transitions"]) for row in reconstruction["profiles"]),
            "certificate": reconstruction["certificate"],
            "operator_checks": reconstruction["operator_checks"],
        },
        "prior": _belief_wire(prepared["prior"]),
        "rates": [[_pair(rate) for rate in pair] for pair in prepared["rates"]],
        "kernel_sha256": [_digest(rows) for rows in kernel_rows],
        "first": [
            {
                "observation": list(row["observation"]),
                "likelihood": _pair(row["likelihood"]),
                "posterior": _belief_wire(row["posterior"]),
            }
            for row in first
        ],
        "histories": [
            {
                "observations": _history_values(row),
                "likelihood": _pair(row["likelihood"]),
                "conditional_likelihood": _pair(row["conditional_likelihood"]),
                "posterior": _belief_wire(row["posterior"]),
                "prediction": _question_wire(row["prediction"]),
            }
            for row in histories
        ],
        "latest_only": [
            {
                "observation": list(observation),
                "likelihood": _pair(row["likelihood"]),
                "posterior": _belief_wire(row["posterior"]),
                "prediction": _question_wire(row["prediction"]),
            }
            for observation, row in sorted(latest.items())
        ],
        "unconditional": {
            "after_first": _belief_wire(after_first),
            "after_second": _belief_wire(after_second),
            "after_third": _belief_wire(after_third),
            "next_prediction": _question_wire(_question_pushforward(after_third, labels)),
        },
        "controls": controls,
        "checks": checks,
        "counts": {
            "classes": len(prepared["model"]["classes"]),
            "profile_atoms": sum(len(row["transitions"]) for row in reconstruction["profiles"]),
            "kernel_atoms": [sum(len(row) for row in kernel) for kernel in kernels],
            "first_histories": len(first),
            "histories": len(histories),
            "first_posterior_atoms": sum(len(row["posterior"]) for row in first),
            "history_posterior_atoms": posterior_atoms,
            "history_prediction_atoms": prediction_atoms,
            "latest_observations": len(latest),
            "latest_posterior_atoms": sum(len(row["posterior"]) for row in latest.values()),
            "latest_prediction_atoms": sum(len(row["prediction"]) for row in latest.values()),
            **control_counts,
        },
    }
    return json.loads(canonical(result))
