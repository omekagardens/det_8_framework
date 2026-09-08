"""Exact replacement envelopes with a statically carried nominal AA baseline.

This coefficient-model API does not authenticate forecast or channel origin.
It preserves every nominal minimizing rule without a replacement argmin.
No prior or alternative executor is imported.
"""

import hashlib
import json
from fractions import Fraction
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 262144
MAX_BYTES = 4194304
MAX_RISK_CELLS = 48
MAX_DECISION_WORK = 216

LEVELS = (Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1))
RETAINED_WEIGHTS = (Fraction(0), Fraction(1, 2), Fraction(1))


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _string_size(value):
    _require(len(value) <= MAX_BYTES, "native string exceeds its byte cap")
    size = 2
    _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    for character in value:
        code = ord(character)
        if character in ('"', "\\") or code in (8, 9, 10, 12, 13):
            size += 2
        elif 32 <= code <= 126:
            size += 1
        elif code <= 65535:
            size += 6
        else:
            size += 12
        _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    return size


def _scalar_info(value):
    kind = type(value)
    if value is None:
        return 1, 0, 4
    if kind is bool:
        return 1, 0, 4 if value else 5
    if kind is str:
        return 1, 0, _string_size(value)
    if kind is int:
        _require(value.bit_length() <= MAX_BITS, "native integer exceeds its bit cap")
        return 1, 0, len(str(value))
    raise ValueError("expected exact native JSON value")


def _native(value):
    """Preflight expanded JSON value nodes, root-zero depth and exact bytes."""
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        _require(depth <= MAX_DEPTH, "native value exceeds depth cap")
        kind = type(item)
        if kind not in (list, dict):
            nodes, height, size = _scalar_info(item)
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native scalar exceeds cap")
            continue
        if leaving:
            active.remove(id(item))
            nodes, height, size = 1, 0, 2 + max(0, len(item) - 1)
            values = item if kind is list else item.values()
            if kind is dict:
                size += sum(_string_size(key) + 1 for key in item)
            for child in values:
                info = completed[id(child)] if type(child) in (list, dict) else _scalar_info(child)
                child_nodes, child_height, child_size = info
                nodes += child_nodes
                height = max(height, child_height + 1)
                size += child_size
                _require(nodes <= MAX_NODES, "expanded native node cap exceeded")
                _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native container exceeds cap")
            completed[id(item)] = nodes, height, size
            continue
        _require(id(item) not in active, "cyclic native JSON is invalid")
        if id(item) in completed:
            nodes, height, size = completed[id(item)]
            _require(depth + height <= MAX_DEPTH, "shared subtree exceeds depth cap")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "shared subtree exceeds cap")
            continue
        if kind is dict:
            _require(all(type(key) is str for key in item), "object keys must be native strings")
        _require(1 + len(item) <= MAX_NODES, "expanded native node cap exceeded")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if kind is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))
    if type(value) in (list, dict):
        nodes, height, size = completed[id(value)]
    else:
        nodes, height, size = _scalar_info(value)
    _require(height <= MAX_DEPTH and nodes <= MAX_NODES, "expanded native tree cap exceeded")
    _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
    return size + 1


def canonical(value):
    expected_bytes = _native(value)
    data = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    _require(len(data) == expected_bytes, "canonical size preflight disagrees with serialization")
    _require(len(data) <= MAX_BYTES, "canonical byte cap exceeded")
    return data


def _fields(value, names):
    _require(type(value) is dict and set(value) == set(names), "unexpected object fields")


def _integer(value, minimum, maximum):
    _require(
        type(value) is int and minimum <= value <= maximum and value.bit_length() <= MAX_BITS,
        "native integer outside declared bounds",
    )


def _risk(value):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0
        and 0 <= numerator <= 2 * denominator
        and max(numerator.bit_length(), denominator.bit_length()) <= MAX_BITS,
        "risk outside native fraction, score or bit bounds",
    )
    _require(gcd(numerator, denominator) == 1, "fraction is not reduced")
    return Fraction(numerator, denominator)


def _checked(value):
    _require(
        type(value) is Fraction
        and -2 <= value <= 2
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational outside score or bit bounds",
    )
    return value


def _pair(value):
    _checked(value)
    return [value.numerator, value.denominator]


def _difference(risk, coarse):
    """One retained subtraction; unretained cross-products may exceed MAX_BITS."""
    return _checked(risk - coarse)


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "levels", "retained_weights", "worlds"))
    _require(
        problem["schema_version"] == "det8-qr05aa-problem-v1"
        and problem["family"] == "qr05aa_uncertainty_decision",
        "unknown uncertainty-decision schema",
    )
    for name, expected in (("levels", LEVELS), ("retained_weights", RETAINED_WEIGHTS)):
        supplied = problem[name]
        _require(type(supplied) is list and len(supplied) == len(expected), "wrong fixed menu size")
        _require(tuple(_risk(value) for value in supplied) == expected, "fixed menu order differs")
    supplied_worlds = problem["worlds"]
    _require(type(supplied_worlds) is list and len(supplied_worlds) == 4, "four worlds required")
    coarse, risks = [], []
    for actual, world in enumerate(supplied_worlds):
        _fields(world, ("actual_index", "coarse_risk", "models"))
        _integer(world["actual_index"], actual, actual)
        coarse_risk = _risk(world["coarse_risk"])
        supplied_models = world["models"]
        _require(
            type(supplied_models) is list and len(supplied_models) == 4, "four models required"
        )
        model_risks = []
        for assumed, model in enumerate(supplied_models):
            _fields(model, ("assumed_index", "forecast_risks"))
            _integer(model["assumed_index"], assumed, assumed)
            supplied_risks = model["forecast_risks"]
            _require(
                type(supplied_risks) is list and len(supplied_risks) == 3, "three rules required"
            )
            row = tuple(_risk(value) for value in supplied_risks)
            _require(row[0] == coarse_risk, "zero-retention risk must equal the coarse risk")
            model_risks.append(row)
        coarse.append(coarse_risk)
        risks.append(model_risks)

    world_count = len(risks)
    model_count, rule_count = len(risks[0]), len(risks[0][0])
    risk_cells = sum(len(row) for world in risks for row in world)
    candidate_visits = model_count * rule_count * sum(range(1, world_count + 1))
    selection_visits = model_count * world_count * rule_count
    planned = {
        "worlds": world_count,
        "assumed_models": model_count,
        "rules": rule_count,
        "decisions": world_count * model_count,
        "world_rule_cells": risk_cells,
        "excess_terms": risk_cells,
        "candidate_world_visits": candidate_visits,
        "candidate_selection_visits": selection_visits,
        "total_decision_work": risk_cells + candidate_visits + selection_visits,
    }
    _require(risk_cells <= MAX_RISK_CELLS, "risk-cell work cap exceeded")
    _require(planned["total_decision_work"] <= MAX_DECISION_WORK, "decision-work cap exceeded")
    return coarse, risks, planned


def _analyze_nominal(problem):
    """Return all finite signed-excess certificates, including every exact tie."""
    coarse, risks, planned = _prepare(problem)
    input_sha256 = hashlib.sha256(canonical(problem)).hexdigest()
    worlds, excess = [], []
    excess_terms = candidate_world_visits = candidate_selection_visits = 0
    for actual, supplied_models in enumerate(risks):
        models, excess_rows = [], []
        for assumed, risk_row in enumerate(supplied_models):
            values = []
            for risk in risk_row:
                values.append(_difference(risk, coarse[actual]))
                excess_terms += 1
            excess_rows.append(values)
            models.append(
                {
                    "assumed_index": assumed,
                    "forecast_risks": [_pair(risk) for risk in risk_row],
                    "excess_risks": [_pair(value) for value in values],
                }
            )
        excess.append(excess_rows)
        worlds.append(
            {"actual_index": actual, "coarse_risk": _pair(coarse[actual]), "models": models}
        )

    decisions = []
    for assumed in range(len(risks[0])):
        previous_worlds, previous_worst, previous_minimum = [], None, None
        for bound in range(len(risks)):
            world_indices = list(range(bound + 1))
            candidates, candidate_values, maxima = [], [], []
            complete_argmax = True
            for rule, weight in enumerate(RETAINED_WEIGHTS):
                values, maximizers, worst = [], [], None
                for actual in world_indices:
                    value = excess[actual][assumed][rule]
                    candidate_world_visits += 1
                    values.append(value)
                    if worst is None or value > worst:
                        worst, maximizers = value, [actual]
                    elif value == worst:
                        maximizers.append(actual)
                complete_argmax = complete_argmax and (
                    worst is not None
                    and all(value <= worst for value in values)
                    and maximizers
                    == [actual for actual, value in zip(world_indices, values) if value == worst]
                )
                candidates.append(
                    {
                        "retained_weight": _pair(weight),
                        "world_excesses": [_pair(value) for value in values],
                        "worst_excess": _pair(worst),
                        "worst_world_indices": maximizers,
                    }
                )
                candidate_values.append(values)
                maxima.append(worst)

            minimizers, minimum = [], None
            for rule, value in enumerate(maxima):
                candidate_selection_visits += 1
                if minimum is None or value < minimum:
                    minimum, minimizers = value, [rule]
                elif value == minimum:
                    minimizers.append(rule)
            checks = {
                "coarse_zero": all(value == 0 for value in candidate_values[0]),
                "nested_uncertainty": world_indices == [*previous_worlds, bound],
                "complete_argmax": complete_argmax,
                "complete_argmin": minimum is not None
                and all(value >= minimum for value in maxima)
                and minimizers == [rule for rule, value in enumerate(maxima) if value == minimum],
                "minimax_nonpositive": minimum <= 0,
                "bound_extension_non_decrease": previous_worst is None
                or (
                    all(value >= old for value, old in zip(maxima, previous_worst))
                    and minimum >= previous_minimum
                ),
            }
            _require(all(value is True for value in checks.values()), "decision identity failed")
            decisions.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": world_indices,
                    "candidates": candidates,
                    "minimax_excess": _pair(minimum),
                    "minimizer_indices": minimizers,
                    "minimizer_weights": [_pair(RETAINED_WEIGHTS[rule]) for rule in minimizers],
                    "checks": checks,
                }
            )
            previous_worlds, previous_worst, previous_minimum = world_indices, maxima, minimum

    counts = {
        "worlds": len(worlds),
        "assumed_models": len(worlds[0]["models"]),
        "rules": len(worlds[0]["models"][0]["forecast_risks"]),
        "decisions": len(decisions),
        "world_rule_cells": sum(len(row) for world in excess for row in world),
        "excess_terms": excess_terms,
        "candidate_world_visits": candidate_world_visits,
        "candidate_selection_visits": candidate_selection_visits,
        "total_decision_work": excess_terms + candidate_world_visits + candidate_selection_visits,
    }
    _require(counts == planned, "executed decision work differs from its preflight plan")
    result = {
        "input_sha256": input_sha256,
        "levels": [_pair(level) for level in LEVELS],
        "retained_weights": [_pair(weight) for weight in RETAINED_WEIGHTS],
        "worlds": worlds,
        "decisions": decisions,
        "counts": counts,
    }
    return json.loads(canonical(result))


MAX_FIBERS = 72
MAX_LABELS = 93
MAX_COEFFICIENT_CELLS = 1116
MAX_TOTAL_WORK = 10548


def _nonnegative(value):
    _checked(value)
    _require(value >= 0, "retained nonnegative rational is negative")
    return value


def _profile_coefficient(value):
    return _nonnegative(value)


def _witness_term(value):
    return _nonnegative(value)


def _envelope(clean, full, rate):
    return _checked((1 - rate) * clean + rate * full)


def _shift(left, right):
    value = left - right
    _require(
        type(value) is Fraction
        and -4 <= value <= 4
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift outside range or bit bounds",
    )
    return value


def _wide_pair(value):
    _require(
        type(value) is Fraction
        and -4 <= value <= 4
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift outside range or bit bounds",
    )
    return [value.numerator, value.denominator]


def _coordinates(value, length):
    _require(type(value) is list and len(value) == length, "wrong native coordinate dimension")
    for coordinate in value:
        _integer(coordinate, 0, (1 << MAX_BITS) - 1)
    return tuple(value)


def _prepare_ac(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "nominal", "alphabet", "models"))
    _require(
        problem["schema_version"] == "det8-qr05ac-problem-v1"
        and problem["family"] == "qr05ac_replacement_envelope",
        "unknown replacement-envelope schema",
    )
    _, _, nominal_counts = _prepare(problem["nominal"])
    supplied = problem["alphabet"]
    _require(
        type(supplied) is list and 1 <= len(supplied) <= MAX_FIBERS,
        "fiber count outside cap",
    )
    alphabet, previous_prefix, labels = [], None, 0
    for fiber in supplied:
        _fields(fiber, ("N", "values"))
        prefix = _coordinates(fiber["N"], 5)
        _require(
            previous_prefix is None or previous_prefix < prefix, "fibers must be sorted unique"
        )
        previous_prefix = prefix
        supplied_values = fiber["values"]
        _require(type(supplied_values) is list and supplied_values, "fiber must have native labels")
        labels += len(supplied_values)
        _require(labels <= MAX_LABELS, "whole alphabet label cap exceeded")
        values, previous_label = [], None
        for supplied_value in supplied_values:
            value = _coordinates(supplied_value, 7)
            _require(value[:5] == prefix, "label has a different N prefix")
            _require(
                previous_label is None or previous_label < value, "labels must be sorted unique"
            )
            previous_label = value
            values.append(value)
        alphabet.append((prefix, values))

    models = problem["models"]
    _require(type(models) is list and len(models) == 4, "four ordered coefficient models required")
    coefficients, cells = [], 0
    for assumed, model in enumerate(models):
        _fields(model, ("assumed_index", "full_coefficients"))
        _integer(model["assumed_index"], assumed, assumed)
        rows = model["full_coefficients"]
        _require(
            type(rows) is list and len(rows) == len(alphabet),
            "coefficient fiber dimension differs",
        )
        fibers = []
        for supplied_rows, (_, values) in zip(rows, alphabet):
            _require(
                type(supplied_rows) is list and len(supplied_rows) == len(values),
                "coefficient label dimension differs",
            )
            parsed_rows = []
            for row in supplied_rows:
                _require(type(row) is list and len(row) == 3, "three coefficient rules required")
                parsed = tuple(_risk(value) for value in row)
                _require(parsed[0] == 0, "coarse coefficient must be zero")
                parsed_rows.append(parsed)
                cells += len(parsed)
            fibers.append(parsed_rows)
        coefficients.append(fibers)

    fibers = len(alphabet)
    planned = {
        "fibers": fibers,
        "labels": labels,
        "assumed_models": 4,
        "rules": 3,
        "certificates": 16,
        "candidate_certificates": 48,
        "nominal_risk_cells": nominal_counts["world_rule_cells"],
        "coefficient_cells": cells,
        "baseline_decision_work": nominal_counts["total_decision_work"],
        "profile_coefficient_visits": 12 * labels,
        "profile_fiber_terms": 12 * fibers,
        "world_envelope_terms": 48,
        "candidate_world_visits": 120,
        "face_label_visits": 48 * labels,
        "witness_coefficient_terms": 48 * fibers,
        "witness_world_terms": 120,
        "shift_terms": 96,
        "candidate_classifications": 48,
        "total_work_terms": nominal_counts["total_decision_work"]
        + 48
        + 120
        + 120
        + 96
        + 48
        + 60 * labels
        + 60 * fibers,
    }
    _require(cells <= MAX_COEFFICIENT_CELLS, "coefficient-cell cap exceeded")
    _require(cells == planned["profile_coefficient_visits"], "coefficient inventory differs")
    _require(planned["total_work_terms"] <= MAX_TOTAL_WORK, "envelope work cap exceeded")
    return alphabet, coefficients, planned


def _profiles(alphabet, coefficients, baseline):
    profiles, internals, curves = [], [], []
    coefficient_visits = fiber_terms = envelope_terms = 0
    for assumed, model in enumerate(coefficients):
        for rule, weight in enumerate(RETAINED_WEIGHTS):
            clean = _checked(
                Fraction(*baseline["worlds"][0]["models"][assumed]["excess_risks"][rule])
            )
            total, rows, maxima, maximizers = Fraction(0), [], [], []
            flat = True
            for (prefix, labels), fiber in zip(alphabet, model):
                values, best, indices = [], None, []
                for index, row in enumerate(fiber):
                    value = _profile_coefficient(row[rule])
                    coefficient_visits += 1
                    values.append(value)
                    if best is None or value > best:
                        best, indices = value, [index]
                    elif value == best:
                        indices.append(index)
                _require(
                    best is not None
                    and all(value <= best for value in values)
                    and indices == [index for index, value in enumerate(values) if value == best],
                    "profile maximum or complete face differs",
                )
                fiber_terms += 1
                total += best
                rows.append(
                    {"N": list(prefix), "maximum": _pair(best), "maximizer_indices": indices}
                )
                maxima.append(best)
                maximizers.append(indices)
                flat = flat and len(indices) == len(labels)
            # This sum is newly retained; partial exact sums are not bit capped.
            full = _nonnegative(total)
            profiles.append(
                {
                    "assumed_index": assumed,
                    "retained_weight": _pair(weight),
                    "clean_excess": _pair(clean),
                    "full_upper_excess": _pair(full),
                    "fibers": rows,
                    "all_fibers_flat": flat,
                }
            )
            internals.append((clean, full, maxima, maximizers, flat))
            curve = []
            for rate in LEVELS:
                curve.append(_envelope(clean, full, rate))
                envelope_terms += 1
            curves.append(curve)
    return profiles, internals, curves, coefficient_visits, fiber_terms, envelope_terms


def _certificates(alphabet, coefficients, baseline, internals, curves):
    certificates = []
    visits = face_visits = witness_terms = witness_world_terms = shifts = classifications = (
        old_slots
    ) = 0
    for assumed in range(4):
        previous_worlds = []
        for bound in range(4):
            nominal = baseline["decisions"][4 * assumed + bound]
            _require(
                nominal["assumed_index"] == assumed and nominal["bound_index"] == bound,
                "nominal decision order differs",
            )
            nominal_value = _checked(Fraction(*nominal["minimax_excess"]))
            old_indices = nominal["minimizer_indices"][:]
            old_weights = [weight[:] for weight in nominal["minimizer_weights"]]
            _require(
                old_indices and len(old_indices) == len(old_weights), "nominal selection empty"
            )
            world_indices = list(range(bound + 1))
            candidates, candidate_maxima, interiors = [], [], []
            complete_maxima = complete_faces = witness_attains = witness_maxima_complete = True
            attainment_checked = signed_comparison = True
            for rule, weight in enumerate(RETAINED_WEIGHTS):
                profile_index = 3 * assumed + rule
                clean, full, _maxima, maximizers, flat = internals[profile_index]
                upper_values, worst, worst_worlds = [], None, []
                for actual in world_indices:
                    value = curves[profile_index][actual]
                    visits += 1
                    upper_values.append(value)
                    if worst is None or value > worst:
                        worst, worst_worlds = value, [actual]
                    elif value == worst:
                        worst_worlds.append(actual)
                complete_maxima = complete_maxima and (
                    worst is not None
                    and all(value <= worst for value in upper_values)
                    and worst_worlds
                    == [
                        actual
                        for actual, value in zip(world_indices, upper_values)
                        if value == worst
                    ]
                )

                clean_worst = 0 in worst_worlds
                faces, witness_labels, witness_sum = [], [], Fraction(0)
                for fiber_index, (_, labels) in enumerate(alphabet):
                    face = []
                    for label in range(len(labels)):
                        face_visits += 1
                        if clean_worst or label in maximizers[fiber_index]:
                            face.append(label)
                    _require(face, "empty global mechanism face")
                    complete_faces = complete_faces and face == (
                        list(range(len(labels))) if clean_worst else maximizers[fiber_index]
                    )
                    selected = face[0]
                    term = _witness_term(coefficients[assumed][fiber_index][selected][rule])
                    witness_terms += 1
                    witness_sum += term
                    faces.append(face)
                    witness_labels.append(selected)
                witness_full = _nonnegative(witness_sum)
                _require(witness_full <= full, "witness full coefficient exceeds the envelope")
                witness_values, witness_worst, witness_worlds = [], None, []
                for actual in world_indices:
                    value = _envelope(clean, witness_full, LEVELS[actual])
                    witness_world_terms += 1
                    witness_values.append(value)
                    if witness_worst is None or value > witness_worst:
                        witness_worst, witness_worlds = value, [actual]
                    elif value == witness_worst:
                        witness_worlds.append(actual)
                witness_attains = witness_attains and (
                    witness_worst == worst
                    and all(value <= upper for value, upper in zip(witness_values, upper_values))
                    and witness_labels == [face[0] for face in faces]
                )
                witness_maxima_complete = witness_maxima_complete and (
                    witness_worst is not None
                    and all(value <= witness_worst for value in witness_values)
                    and witness_worlds
                    == [
                        actual
                        for actual, value in zip(world_indices, witness_values)
                        if value == witness_worst
                    ]
                )
                attained = clean_worst or flat
                interior_strict = worst < 0 or (worst == 0 and not attained)
                attainment_checked = attainment_checked and (
                    attained
                    == (
                        clean_worst
                        or all(
                            len(face) == len(labels) for face, (_, labels) in zip(faces, alphabet)
                        )
                    )
                    and interior_strict == (worst < 0 or (worst == 0 and not attained))
                )
                nominal_worst = _checked(Fraction(*nominal["candidates"][rule]["worst_excess"]))
                worst_shift = _shift(worst, nominal_worst)
                shifts += 1
                bound_excess = _shift(worst, nominal_value)
                shifts += 1
                classifications += 1
                old = rule in old_indices
                if old:
                    old_slots += 1
                safe, strict, preserved = worst <= 0, worst < 0, worst <= nominal_value
                unsafe = [actual for actual, value in zip(world_indices, upper_values) if value > 0]
                breaking = [
                    actual
                    for actual, value in zip(world_indices, upper_values)
                    if value > nominal_value
                ]
                witness_unsafe = [
                    actual for actual, value in zip(world_indices, witness_values) if value > 0
                ]
                witness_breaking = [
                    actual
                    for actual, value in zip(world_indices, witness_values)
                    if value > nominal_value
                ]
                signed_comparison = signed_comparison and (
                    worst_shift + nominal_worst == worst
                    and bound_excess + nominal_value == worst
                    and safe == (not unsafe)
                    and strict == all(value < 0 for value in upper_values)
                    and preserved == (not breaking)
                    and preserved == (bound_excess <= 0)
                )
                candidates.append(
                    {
                        "retained_weight": _pair(weight),
                        "profile_index": profile_index,
                        "world_upper_excesses": [_pair(value) for value in upper_values],
                        "worst_excess": _pair(worst),
                        "worst_world_indices": worst_worlds,
                        "nominal_worst_excess": _pair(nominal_worst),
                        "worst_shift": _wide_pair(worst_shift),
                        "bound_excess": _wide_pair(bound_excess),
                        "nominal_minimizer": old,
                        "coarse_safe": safe,
                        "strict_benefit": strict,
                        "original_bound_preserved": preserved,
                        "full_support_maximum_attained": attained,
                        "every_full_support_mechanism_strict": interior_strict,
                        "maximizing_face_indices": faces,
                        "witness_label_indices": witness_labels,
                        "witness_full_excess": _pair(witness_full),
                        "witness_world_excesses": [_pair(value) for value in witness_values],
                        "witness_worst_world_indices": witness_worlds,
                        "potentially_unsafe_world_indices": unsafe,
                        "potentially_bound_breaking_world_indices": breaking,
                        "witness_unsafe_world_indices": witness_unsafe,
                        "witness_bound_breaking_world_indices": witness_breaking,
                    }
                )
                candidate_maxima.append(worst)
                interiors.append(interior_strict)

            safe_old = [rule for rule in old_indices if candidates[rule]["coarse_safe"]]
            strict_old = [rule for rule in old_indices if candidates[rule]["strict_benefit"]]
            preserved_old = [
                rule for rule in old_indices if candidates[rule]["original_bound_preserved"]
            ]
            interior_old = [
                rule
                for rule in old_indices
                if candidates[rule]["every_full_support_mechanism_strict"]
            ]
            unsafe_old = [rule for rule in old_indices if not candidates[rule]["coarse_safe"]]
            breaking_old = [
                rule for rule in old_indices if not candidates[rule]["original_bound_preserved"]
            ]
            quantifiers = {
                "all_old_safe": len(safe_old) == len(old_indices),
                "any_old_safe": bool(safe_old),
                "all_old_strict": len(strict_old) == len(old_indices),
                "any_old_strict": bool(strict_old),
                "all_old_bound_preserved": len(preserved_old) == len(old_indices),
                "any_old_bound_preserved": bool(preserved_old),
                "all_old_interior_strict": len(interior_old) == len(old_indices),
                "any_old_interior_strict": bool(interior_old),
            }
            quantifiers_checked = (
                quantifiers["all_old_safe"]
                == all(candidate_maxima[rule] <= 0 for rule in old_indices)
                and quantifiers["any_old_safe"]
                == any(candidate_maxima[rule] <= 0 for rule in old_indices)
                and quantifiers["all_old_strict"]
                == all(candidate_maxima[rule] < 0 for rule in old_indices)
                and quantifiers["any_old_strict"]
                == any(candidate_maxima[rule] < 0 for rule in old_indices)
                and quantifiers["all_old_bound_preserved"]
                == all(candidate_maxima[rule] <= nominal_value for rule in old_indices)
                and quantifiers["any_old_bound_preserved"]
                == any(candidate_maxima[rule] <= nominal_value for rule in old_indices)
                and quantifiers["all_old_interior_strict"]
                == all(interiors[rule] for rule in old_indices)
                and quantifiers["any_old_interior_strict"]
                == any(interiors[rule] for rule in old_indices)
                and safe_old == [rule for rule in old_indices if rule not in unsafe_old]
                and preserved_old == [rule for rule in old_indices if rule not in breaking_old]
            )
            checks = {
                "nominal_selection_preserved": old_indices == nominal["minimizer_indices"]
                and old_weights == nominal["minimizer_weights"]
                and old_indices
                == [
                    rule
                    for rule, candidate in enumerate(candidates)
                    if candidate["nominal_minimizer"]
                ]
                and old_weights == [_pair(RETAINED_WEIGHTS[rule]) for rule in old_indices],
                "complete_envelope_argmax": complete_maxima,
                "complete_mechanism_faces": complete_faces,
                "global_witness_attains_envelope": witness_attains,
                "witness_argmax_complete": witness_maxima_complete,
                "full_support_attainment": attainment_checked,
                "all_any_quantifiers": quantifiers_checked,
                "signed_bound_comparison": signed_comparison,
                "coarse_zero": all(
                    value == [0, 1] for value in candidates[0]["world_upper_excesses"]
                ),
                "nested_worlds": world_indices == [*previous_worlds, bound],
            }
            _require(
                all(value is True for value in checks.values()),
                "envelope certificate identity failed",
            )
            certificates.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": world_indices,
                    "nominal_minimax_excess": _pair(nominal_value),
                    "old_minimizer_indices": old_indices,
                    "old_minimizer_weights": old_weights,
                    "candidates": candidates,
                    "safe_old_indices": safe_old,
                    "strictly_beneficial_old_indices": strict_old,
                    "bound_preserving_old_indices": preserved_old,
                    "interior_strict_old_indices": interior_old,
                    "unsafe_old_indices": unsafe_old,
                    "bound_breaking_old_indices": breaking_old,
                    **quantifiers,
                    "checks": checks,
                }
            )
            previous_worlds = world_indices
    metrics = {
        "candidate_world_visits": visits,
        "face_label_visits": face_visits,
        "witness_coefficient_terms": witness_terms,
        "witness_world_terms": witness_world_terms,
        "shift_terms": shifts,
        "candidate_classifications": classifications,
    }
    return certificates, metrics, old_slots


def analyze(problem):
    """Certify all frozen nominal choices over the supplied replacement product."""
    alphabet, coefficients, planned = _prepare_ac(problem)
    input_sha256 = hashlib.sha256(canonical(problem)).hexdigest()
    baseline = _analyze_nominal(problem["nominal"])
    baseline_snapshot = canonical(baseline)
    _require(
        baseline["counts"]["total_decision_work"] == planned["baseline_decision_work"],
        "nominal work differs from plan",
    )
    profiles, internals, curves, coefficient_visits, fiber_terms, envelope_terms = _profiles(
        alphabet, coefficients, baseline
    )
    certificates, metrics, old_slots = _certificates(
        alphabet, coefficients, baseline, internals, curves
    )
    counts = {
        "fibers": len(alphabet),
        "labels": sum(len(labels) for _, labels in alphabet),
        "assumed_models": len(coefficients),
        "rules": len(RETAINED_WEIGHTS),
        "certificates": len(certificates),
        "candidate_certificates": sum(
            len(certificate["candidates"]) for certificate in certificates
        ),
        "old_rule_evaluations": old_slots,
        "nominal_risk_cells": baseline["counts"]["world_rule_cells"],
        "coefficient_cells": sum(
            len(row) for model in coefficients for fiber in model for row in fiber
        ),
        "baseline_decision_work": baseline["counts"]["total_decision_work"],
        "profile_coefficient_visits": coefficient_visits,
        "profile_fiber_terms": fiber_terms,
        "world_envelope_terms": envelope_terms,
        **metrics,
        "total_work_terms": baseline["counts"]["total_decision_work"]
        + coefficient_visits
        + fiber_terms
        + envelope_terms
        + sum(metrics.values()),
    }
    _require(
        {name: value for name, value in counts.items() if name != "old_rule_evaluations"}
        == planned,
        "executed envelope work differs from plan",
    )
    _require(
        old_slots == sum(len(decision["minimizer_indices"]) for decision in baseline["decisions"])
        and old_slots <= counts["candidate_certificates"],
        "old minimizing-slot count differs",
    )
    _require(canonical(baseline) == baseline_snapshot, "nominal baseline changed")
    result = {
        "input_sha256": input_sha256,
        "baseline": baseline,
        "alphabet": [
            {"N": list(prefix), "values": [list(value) for value in labels]}
            for prefix, labels in alphabet
        ],
        "profiles": profiles,
        "certificates": certificates,
        "counts": counts,
    }
    return json.loads(canonical(result))
