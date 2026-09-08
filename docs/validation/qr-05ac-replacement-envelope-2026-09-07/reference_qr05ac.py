"""Independent exact product-simplex envelope reference for QR-05AC.

The nominal decision engine is statically carried own AA lineage.

Native DAG guards are statically carried own lineage; the decision engine
works solely with supplied risks. It authenticates no forecast laws or origin.
"""

import hashlib
import json
from fractions import Fraction as F
from itertools import pairwise
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 262144
MAX_BYTES = 4194304
MAX_RISK_CELLS = 48
MAX_DECISION_WORK = 216
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
RETAINED_WEIGHTS = (F(0), F(1, 2), F(1))
CHECKS = (
    "coarse_zero",
    "nested_uncertainty",
    "complete_argmax",
    "complete_argmin",
    "minimax_nonpositive",
    "bound_extension_non_decrease",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _fields(obj, names, message):
    _require(
        type(obj) is dict and all(type(k) is str for k in obj) and set(obj) == set(names), message
    )


def _string_bytes(value):
    # Exact ensure_ascii=True JSON size without serializing an unbounded tree.
    _require(type(value) is str, "native object key or string")
    _require(len(value) <= MAX_BYTES, "string byte cap")
    count = 2
    for char in value:
        code = ord(char)
        if char in ('"', "\\", "\b", "\t", "\n", "\f", "\r"):
            count += 2
        elif code < 32 or code >= 127:
            count += 6 if code <= 65535 else 12
        else:
            count += 1
        _require(count <= MAX_BYTES, "escaped string byte cap")
    return count


def _native(value):
    # Nodes are JSON values, not object keys. A scalar/empty container has
    # height zero: root depth is zero and deepest scalar leaves count.
    pending, active, complete = [(value, False, 0)], set(), {}

    def scalar(v):
        if v is None:
            return (1, 0, 4)
        if type(v) is bool:
            return (1, 0, 4 if v else 5)
        if type(v) is str:
            return (1, 0, _string_bytes(v))
        if type(v) is int:
            _require(abs(v).bit_length() <= MAX_BITS, "native integer component bit cap")
            return (1, 0, len(str(v)))
        _require(type(v) in (list, dict), "non-native JSON value")
        return None

    while pending:
        current, leaving, depth = pending.pop()
        _require(depth <= MAX_DEPTH, "early native traversal depth cap")
        simple = scalar(current)
        if simple is not None:
            continue
        identity = id(current)
        if leaving:
            children = list(current.values()) if type(current) is dict else current
            nodes, height = 1, 0
            size = 2 + max(0, len(children) - 1)
            if type(current) is dict:
                for key in current:
                    size += _string_bytes(key) + 1
                    _require(size <= MAX_BYTES, "object-key expanded byte cap")
            for child in children:
                info = complete[id(child)] if type(child) in (list, dict) else scalar(child)
                nodes += info[0]
                height = max(height, info[1] + 1)
                size += info[2]
                _require(nodes <= MAX_NODES, "expanded value-node cap")
                _require(height <= MAX_DEPTH, "native depth cap")
                _require(size <= MAX_BYTES, "expanded canonical byte cap")
            _require(
                nodes <= MAX_NODES and height <= MAX_DEPTH and size <= MAX_BYTES,
                "native tree resource cap",
            )
            complete[identity] = (nodes, height, size)
            active.remove(identity)
            continue
        _require(identity not in active, "cyclic JSON container")
        if identity in complete:
            _require(depth + complete[identity][1] <= MAX_DEPTH, "cached subtree depth cap")
            continue
        _require(len(current) + 1 <= MAX_NODES, "container width value-node lower bound")
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native object key")
        active.add(identity)
        pending.append((current, True, depth))
        children = current.values() if type(current) is dict else current
        pending.extend((child, False, depth + 1) for child in children)
    info = complete[id(value)] if type(value) in (list, dict) else scalar(value)
    _require(
        info[0] <= MAX_NODES and info[1] <= MAX_DEPTH and info[2] + 1 <= MAX_BYTES,
        "complete expanded native wire cap",
    )


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, OverflowError, RecursionError, ValueError) as error:
        raise ValueError("canonical JSON serialization failed") from error


def _fraction(value):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    n, d = value
    _require(type(n) is int and type(d) is int, "native rational components")
    _require(d > 0 and 0 <= n <= 2 * d, "risk interval")
    _require(max(n.bit_length(), d.bit_length()) <= MAX_BITS, "input rational bit cap")
    _require(gcd(n, d) == 1, "reduced rational")
    return F(n, d)


def _wire(value):
    _require(type(value) is F and -2 <= value <= 2, "retained exact signed risk interval")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational bit cap",
    )
    return [value.numerator, value.denominator]


def _prepare(problem):
    _native(problem)
    _fields(
        problem,
        ("schema_version", "family", "levels", "retained_weights", "worlds"),
        "exact problem fields",
    )
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05aa-problem-v1",
        "problem schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05aa_uncertainty_decision",
        "problem family",
    )
    for key, expected in (("levels", LEVELS), ("retained_weights", RETAINED_WEIGHTS)):
        _require(
            type(problem[key]) is list and len(problem[key]) == len(expected), "fixed label count"
        )
        _require(
            tuple(_fraction(value) for value in problem[key]) == expected,
            "fixed reduced label order",
        )
    worlds = problem["worlds"]
    _require(type(worlds) is list and len(worlds) == 4, "four actual worlds")
    parsed = []
    for i, world in enumerate(worlds):
        _fields(world, ("actual_index", "coarse_risk", "models"), "exact world fields")
        _require(
            type(world["actual_index"]) is int and world["actual_index"] == i,
            "actual index native and ordered",
        )
        coarse = _fraction(world["coarse_risk"])
        models = world["models"]
        _require(type(models) is list and len(models) == 4, "four assumed models")
        forecasts = []
        for j, model in enumerate(models):
            _fields(model, ("assumed_index", "forecast_risks"), "exact model fields")
            _require(
                type(model["assumed_index"]) is int and model["assumed_index"] == j,
                "assumed index native and ordered",
            )
            risks = model["forecast_risks"]
            _require(type(risks) is list and len(risks) == 3, "three fixed rules")
            values = tuple(_fraction(value) for value in risks)
            _require(values[0] == coarse, "zero retention is same-world coarse risk")
            forecasts.append(values)
        parsed.append((coarse, forecasts))
    return parsed


def _difference(risk, coarse):
    # Fraction may form large intermediate cross-products before reduction.
    # Only the retained reduced difference, not those intermediates, is capped.
    _require(type(risk) is F and type(coarse) is F, "exact subtraction inputs")
    result = risk - coarse
    _wire(result)
    return result


def _analyze_nominal(problem):
    """Compare all declared experiment-wide rules over each finite upper set."""
    parsed = _prepare(problem)
    planned_risks = sum(len(risks) for _, models in parsed for risks in models)
    planned_world_visits = sum(len(parsed[: u + 1]) for u in range(4)) * 4 * 3
    planned_selections = 4 * 4 * 3
    planned_work = planned_risks + planned_world_visits + planned_selections
    _require(planned_risks <= MAX_RISK_CELLS, "planned risk-cell cap")
    _require(planned_work <= MAX_DECISION_WORK, "planned decision-work cap")
    # No subtraction or minimax scan has occurred above this point.
    input_digest = hashlib.sha256(_canonical(problem)).hexdigest()
    excesses, worlds = [], []
    excess_terms = candidate_world_visits = candidate_selection_visits = 0
    for i, (coarse, models) in enumerate(parsed):
        row, wire_models = [], []
        for j, risks in enumerate(models):
            differences = []
            for risk in risks:
                differences.append(_difference(risk, coarse))
                excess_terms += 1
            row.append(differences)
            wire_models.append(
                {
                    "assumed_index": j,
                    "forecast_risks": [_wire(risk) for risk in risks],
                    "excess_risks": [_wire(value) for value in differences],
                }
            )
        excesses.append(row)
        worlds.append({"actual_index": i, "coarse_risk": _wire(coarse), "models": wire_models})
    decisions = []
    for assumed in range(4):
        previous_worlds, previous_worst, previous_minimum = [], None, None
        for bound in range(4):
            actual_indices = list(range(bound + 1))
            _require(actual_indices[:-1] == previous_worlds, "nested uncertainty sets")
            candidates, selection_values = [], []
            for rule, retained in enumerate(RETAINED_WEIGHTS):
                values = []
                for actual in actual_indices:
                    values.append(excesses[actual][assumed][rule])
                    candidate_world_visits += 1
                worst = max(values)
                maximizers = [
                    actual
                    for actual, value in zip(actual_indices, values, strict=True)
                    if value == worst
                ]
                _require(
                    bool(maximizers) and all(value <= worst for value in values),
                    "complete candidate maximum",
                )
                _require(
                    maximizers
                    == [
                        actual
                        for actual in actual_indices
                        if excesses[actual][assumed][rule] == worst
                    ],
                    "all exact maximizing worlds",
                )
                if rule == 0:
                    _require(all(value == 0 for value in values), "coarse zero excess")
                if previous_worst is not None:
                    _require(worst >= previous_worst[rule], "candidate bound extension")
                candidates.append(
                    {
                        "retained_weight": _wire(retained),
                        "world_excesses": [_wire(value) for value in values],
                        "worst_excess": _wire(worst),
                        "worst_world_indices": maximizers,
                    }
                )
                selection_values.append(worst)
                candidate_selection_visits += 1
            minimum = min(selection_values)
            minimizers = [rule for rule, value in enumerate(selection_values) if value == minimum]
            _require(
                bool(minimizers) and all(value >= minimum for value in selection_values),
                "complete candidate minimum",
            )
            _require(
                minimizers == [rule for rule in range(3) if selection_values[rule] == minimum],
                "all exact minimizing rules",
            )
            _require(minimum <= 0, "coarse choice makes minimax nonpositive")
            if previous_minimum is not None:
                _require(minimum >= previous_minimum, "minimax bound extension")
            decisions.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": actual_indices,
                    "candidates": candidates,
                    "minimax_excess": _wire(minimum),
                    "minimizer_indices": minimizers,
                    "minimizer_weights": [_wire(RETAINED_WEIGHTS[k]) for k in minimizers],
                    "checks": dict.fromkeys(CHECKS, True),
                }
            )
            previous_worlds, previous_worst, previous_minimum = (
                actual_indices,
                selection_values,
                minimum,
            )
    _require(
        (excess_terms, candidate_world_visits, candidate_selection_visits)
        == (planned_risks, planned_world_visits, planned_selections),
        "planned/executed visits",
    )
    result = {
        "input_sha256": input_digest,
        "levels": [_wire(level) for level in LEVELS],
        "retained_weights": [_wire(weight) for weight in RETAINED_WEIGHTS],
        "worlds": worlds,
        "decisions": decisions,
        "counts": {
            "worlds": 4,
            "assumed_models": 4,
            "rules": 3,
            "decisions": 16,
            "world_rule_cells": planned_risks,
            "excess_terms": excess_terms,
            "candidate_world_visits": candidate_world_visits,
            "candidate_selection_visits": candidate_selection_visits,
            "total_decision_work": excess_terms
            + candidate_world_visits
            + candidate_selection_visits,
        },
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "canonical output byte cap")
    return json.loads(encoded)


MAX_FIBERS = 72
MAX_LABELS = 93
MAX_COEFFICIENT_CELLS = 1116
MAX_TOTAL_WORK = 10548
AC_CHECKS = (
    "nominal_selection_preserved",
    "complete_envelope_argmax",
    "complete_mechanism_faces",
    "global_witness_attains_envelope",
    "witness_argmax_complete",
    "full_support_attainment",
    "all_any_quantifiers",
    "signed_bound_comparison",
    "coarse_zero",
    "nested_worlds",
)


def _profile_coefficient(value):
    _require(type(value) is F and 0 <= value <= 2, "exact full coefficient")
    _wire(value)
    return value


def _envelope(c, upper, level):
    _require(all(type(x) is F for x in (c, upper, level)), "exact envelope operands")
    value = (1 - level) * c + level * upper
    _wire(value)
    return value


def _witness_term(value):
    _require(type(value) is F and 0 <= value <= 2, "exact witness coefficient")
    _wire(value)
    return value


def _shift(left, right):
    _require(type(left) is F and type(right) is F, "exact shift operands")
    value = left - right
    _shift_wire(value)
    return value


def _shift_wire(value):
    _require(type(value) is F and -4 <= value <= 4, "retained shift interval")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift rational bit cap",
    )
    return [value.numerator, value.denominator]


def _coordinate(value, width):
    _require(type(value) is list and len(value) == width, "coordinate width")
    _require(all(type(x) is int and x >= 0 for x in value), "native nonnegative coordinates")
    return tuple(value)


def _prepare_ac(problem):
    _native(problem)
    _fields(
        problem,
        ("schema_version", "family", "nominal", "alphabet", "models"),
        "exact AC input fields",
    )
    _require(problem["schema_version"] == "det8-qr05ac-problem-v1", "AC input schema")
    _require(problem["family"] == "qr05ac_replacement_envelope", "AC input family")
    nominal = _prepare(problem["nominal"])
    alphabet = problem["alphabet"]
    _require(type(alphabet) is list and 1 <= len(alphabet) <= MAX_FIBERS, "fiber cap")
    labels = []
    previous = None
    for fiber in alphabet:
        _fields(fiber, ("N", "values"), "exact alphabet fiber")
        prefix = _coordinate(fiber["N"], 5)
        _require(previous is None or previous < prefix, "strict sorted distinct N fibers")
        previous = prefix
        _require(type(fiber["values"]) is list and bool(fiber["values"]), "nonempty fiber labels")
        values = [_coordinate(value, 7) for value in fiber["values"]]
        _require(all(value[:5] == prefix for value in values), "labels in their declared N fiber")
        _require(all(a < b for a, b in pairwise(values)), "strict sorted distinct labels")
        labels.append(values)
    fibers, label_count = len(labels), sum(map(len, labels))
    _require(label_count <= MAX_LABELS, "total label cap")
    models = problem["models"]
    _require(type(models) is list and len(models) == 4, "four ordered AC models")
    coefficients = []
    for assumed, model in enumerate(models):
        _fields(model, ("assumed_index", "full_coefficients"), "exact coefficient model")
        _require(
            type(model["assumed_index"]) is int and model["assumed_index"] == assumed,
            "native ordered assumed model",
        )
        rows = model["full_coefficients"]
        _require(type(rows) is list and len(rows) == fibers, "coefficient fiber dimension")
        parsed_rows = []
        for values, row in zip(labels, rows, strict=True):
            _require(type(row) is list and len(row) == len(values), "coefficient label dimension")
            parsed_row = []
            for triple in row:
                _require(type(triple) is list and len(triple) == 3, "three coefficient rules")
                parsed = tuple(_fraction(value) for value in triple)
                _require(parsed[0] == 0, "coarse coefficients exactly zero")
                parsed_row.append(parsed)
            parsed_rows.append(parsed_row)
        coefficients.append(parsed_rows)
    counts = {
        "fibers": fibers,
        "labels": label_count,
        "assumed_models": 4,
        "rules": 3,
        "certificates": 16,
        "candidate_certificates": 48,
        "nominal_risk_cells": 48,
        "coefficient_cells": 12 * label_count,
        "baseline_decision_work": 216,
        "profile_coefficient_visits": 12 * label_count,
        "profile_fiber_terms": 12 * fibers,
        "world_envelope_terms": 48,
        "candidate_world_visits": 120,
        "face_label_visits": 48 * label_count,
        "witness_coefficient_terms": 48 * fibers,
        "witness_world_terms": 120,
        "shift_terms": 96,
        "candidate_classifications": 48,
        "total_work_terms": 648 + 60 * label_count + 60 * fibers,
    }
    _require(counts["nominal_risk_cells"] <= MAX_RISK_CELLS, "planned nominal risk cells")
    _require(counts["baseline_decision_work"] <= MAX_DECISION_WORK, "planned baseline work")
    _require(counts["coefficient_cells"] <= MAX_COEFFICIENT_CELLS, "planned coefficient cells")
    _require(counts["total_work_terms"] <= MAX_TOTAL_WORK, "planned total work")
    return nominal, labels, coefficients, counts


def analyze(problem):
    """Envelope every fixed rule without selecting a new forecasting rule."""
    _nominal, labels, coefficients, counts = _prepare_ac(problem)
    baseline = _analyze_nominal(problem["nominal"])
    profiles, profile_values, envelopes = [], [], []
    visited_coefficients = visited_fibers = 0
    for assumed in range(4):
        for rule, weight in enumerate(RETAINED_WEIGHTS):
            clean = F(*baseline["worlds"][0]["models"][assumed]["excess_risks"][rule])
            fibers, maxima = [], []
            for index, values in enumerate(labels):
                terms = []
                for label in range(len(values)):
                    terms.append(_profile_coefficient(coefficients[assumed][index][label][rule]))
                    visited_coefficients += 1
                maximum = max(terms)
                face = [i for i, value in enumerate(terms) if value == maximum]
                _require(
                    bool(face) and all(value <= maximum for value in terms),
                    "complete coefficient maximum",
                )
                maxima.append(maximum)
                fibers.append(
                    {
                        "N": problem["alphabet"][index]["N"],
                        "maximum": _wire(maximum),
                        "maximizer_indices": face,
                    }
                )
                visited_fibers += 1
            upper = sum(maxima, F(0))
            _require(0 <= upper <= 2, "full envelope sum interval")
            _wire(upper)
            flat = all(
                len(fiber["maximizer_indices"]) == len(values)
                for fiber, values in zip(fibers, labels, strict=True)
            )
            profile_values.append((clean, upper))
            profiles.append(
                {
                    "assumed_index": assumed,
                    "retained_weight": _wire(weight),
                    "clean_excess": _wire(clean),
                    "full_upper_excess": _wire(upper),
                    "fibers": fibers,
                    "all_fibers_flat": flat,
                }
            )
            envelopes.append([_envelope(clean, upper, level) for level in LEVELS])
    _require(
        visited_coefficients == counts["profile_coefficient_visits"]
        and visited_fibers == counts["profile_fiber_terms"],
        "profile work inventory",
    )
    certificates = []
    actual_visits = face_visits = witness_terms = witness_worlds = shifts = classifications = 0
    old_evaluations = 0
    for assumed in range(4):
        previous_worlds = []
        for bound in range(4):
            old = baseline["decisions"][4 * assumed + bound]
            worlds = list(range(bound + 1))
            _require(worlds[:-1] == previous_worlds, "nested envelope worlds")
            previous_worlds = worlds
            optimum = F(*old["minimax_excess"])
            candidates = []
            for rule, weight in enumerate(RETAINED_WEIGHTS):
                index = 3 * assumed + rule
                clean, upper = profile_values[index]
                profile = profiles[index]
                values = []
                for world in worlds:
                    values.append(envelopes[index][world])
                    actual_visits += 1
                worst = max(values)
                maximizers = [i for i in worlds if envelopes[index][i] == worst]
                _require(
                    bool(maximizers) and all(v <= worst for v in values), "complete envelope argmax"
                )
                faces, selected = [], []
                for fiber, label_values in zip(profile["fibers"], labels, strict=True):
                    face = []
                    for label in range(len(label_values)):
                        if 0 in maximizers or label in fiber["maximizer_indices"]:
                            face.append(label)
                        face_visits += 1
                    _require(bool(face), "nonempty complete global maximizing face")
                    faces.append(face)
                    selected.append(face[0])
                selected_terms = []
                for fiber, label in enumerate(selected):
                    selected_terms.append(_witness_term(coefficients[assumed][fiber][label][rule]))
                    witness_terms += 1
                witness_full = sum(selected_terms, F(0))
                _require(0 <= witness_full <= 2, "witness full sum interval")
                _wire(witness_full)
                witness_values = []
                for world in worlds:
                    witness_values.append(_envelope(clean, witness_full, LEVELS[world]))
                    witness_worlds += 1
                witness_maximum = max(witness_values)
                witness_argmax = [
                    i
                    for i, value in zip(worlds, witness_values, strict=True)
                    if value == witness_maximum
                ]
                _require(witness_maximum == worst, "global witness attains envelope")
                _require(
                    witness_argmax == [i for i in worlds if witness_values[i] == worst],
                    "own complete witness argmax",
                )
                attained = 0 in maximizers or profile["all_fibers_flat"]
                interior_strict = worst < 0 or (worst == 0 and not attained)
                _require(
                    attained
                    == (
                        0 in maximizers
                        or all(
                            len(face) == len(value)
                            for face, value in zip(faces, labels, strict=True)
                        )
                    ),
                    "full support maximum attainment",
                )
                nominal_worst = F(*old["candidates"][rule]["worst_excess"])
                difference, excess = _shift(worst, nominal_worst), _shift(worst, optimum)
                shifts += 2
                if rule == 0:
                    _require(
                        worst == witness_full == clean == upper == 0 and attained,
                        "coarse zero envelope",
                    )
                candidates.append(
                    {
                        "retained_weight": _wire(weight),
                        "profile_index": index,
                        "world_upper_excesses": [_wire(v) for v in values],
                        "worst_excess": _wire(worst),
                        "worst_world_indices": maximizers,
                        "nominal_worst_excess": _wire(nominal_worst),
                        "worst_shift": _shift_wire(difference),
                        "bound_excess": _shift_wire(excess),
                        "nominal_minimizer": rule in old["minimizer_indices"],
                        "coarse_safe": worst <= 0,
                        "strict_benefit": worst < 0,
                        "original_bound_preserved": worst <= optimum,
                        "full_support_maximum_attained": attained,
                        "every_full_support_mechanism_strict": interior_strict,
                        "maximizing_face_indices": faces,
                        "witness_label_indices": selected,
                        "witness_full_excess": _wire(witness_full),
                        "witness_world_excesses": [_wire(v) for v in witness_values],
                        "witness_worst_world_indices": witness_argmax,
                        "potentially_unsafe_world_indices": [
                            i for i, v in zip(worlds, values, strict=True) if v > 0
                        ],
                        "potentially_bound_breaking_world_indices": [
                            i for i, v in zip(worlds, values, strict=True) if v > optimum
                        ],
                        "witness_unsafe_world_indices": [
                            i for i, v in zip(worlds, witness_values, strict=True) if v > 0
                        ],
                        "witness_bound_breaking_world_indices": [
                            i for i, v in zip(worlds, witness_values, strict=True) if v > optimum
                        ],
                    }
                )
                classifications += 1
            old_indices = old["minimizer_indices"]
            old_evaluations += len(old_indices)
            subset = {
                "safe_old_indices": [i for i in old_indices if candidates[i]["coarse_safe"]],
                "strictly_beneficial_old_indices": [
                    i for i in old_indices if candidates[i]["strict_benefit"]
                ],
                "bound_preserving_old_indices": [
                    i for i in old_indices if candidates[i]["original_bound_preserved"]
                ],
                "interior_strict_old_indices": [
                    i for i in old_indices if candidates[i]["every_full_support_mechanism_strict"]
                ],
                "unsafe_old_indices": [i for i in old_indices if not candidates[i]["coarse_safe"]],
                "bound_breaking_old_indices": [
                    i for i in old_indices if not candidates[i]["original_bound_preserved"]
                ],
            }
            quantifiers = {}
            for suffix, key in (
                ("safe", "safe_old_indices"),
                ("strict", "strictly_beneficial_old_indices"),
                ("bound_preserved", "bound_preserving_old_indices"),
                ("interior_strict", "interior_strict_old_indices"),
            ):
                quantifiers["all_old_" + suffix] = len(subset[key]) == len(old_indices)
                quantifiers["any_old_" + suffix] = bool(subset[key])
                _require(
                    quantifiers["all_old_" + suffix] == all(i in subset[key] for i in old_indices)
                    and quantifiers["any_old_" + suffix]
                    == any(i in subset[key] for i in old_indices),
                    "all/any exact old-set quantifiers",
                )
            _require(
                sorted(subset["safe_old_indices"] + subset["unsafe_old_indices"]) == old_indices
                and sorted(
                    subset["bound_preserving_old_indices"] + subset["bound_breaking_old_indices"]
                )
                == old_indices,
                "signed old-set partitions",
            )
            certificates.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": worlds,
                    "nominal_minimax_excess": old["minimax_excess"],
                    "old_minimizer_indices": old_indices,
                    "old_minimizer_weights": old["minimizer_weights"],
                    "candidates": candidates,
                    **subset,
                    **quantifiers,
                    "checks": dict.fromkeys(AC_CHECKS, True),
                }
            )
    _require(
        (actual_visits, face_visits, witness_terms, witness_worlds, shifts, classifications)
        == (
            counts["candidate_world_visits"],
            counts["face_label_visits"],
            counts["witness_coefficient_terms"],
            counts["witness_world_terms"],
            counts["shift_terms"],
            counts["candidate_classifications"],
        ),
        "complete AC work inventory",
    )
    counts["old_rule_evaluations"] = old_evaluations
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "baseline": baseline,
        "alphabet": problem["alphabet"],
        "profiles": profiles,
        "certificates": certificates,
        "counts": counts,
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "full AC output byte cap")
    return json.loads(encoded)
