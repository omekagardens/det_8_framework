"""Independent fixed-certificate stress reference for QR-05AB.

Native DAG guards are statically carried own lineage; the decision engine
works solely with supplied risks. It authenticates no forecast laws or origin.
"""

import hashlib
import json
from fractions import Fraction as F
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 262144
MAX_BYTES = 4194304
MAX_RISK_CELLS = 48
MAX_DECISION_WORK = 216
MAX_STRESS_RISK_CELLS = 96
MAX_TOTAL_WORK = 840
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


STRESS_CHECKS = (
    "nominal_selection_preserved",
    "complete_argmax",
    "all_any_quantifiers",
    "signed_bound_comparison",
    "coarse_zero",
    "nested_worlds",
    "world_witnesses_complete",
)


def _shift_wire(value):
    _require(type(value) is F and -4 <= value <= 4, "retained signed shift interval")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift component cap",
    )
    return [value.numerator, value.denominator]


def _shift(left, right):
    _require(type(left) is F and type(right) is F, "exact shift inputs")
    result = left - right
    _shift_wire(result)
    return result


def _prepare_ab(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "nominal", "mechanisms"), "AB wrapper fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05ab-problem-v1",
        "AB problem schema",
    )
    _require(
        type(problem["family"]) is str and problem["family"] == "qr05ab_replacement_stress",
        "AB problem family",
    )
    nominal = _prepare(problem["nominal"])
    mechanisms = problem["mechanisms"]
    _require(type(mechanisms) is list and len(mechanisms) == 2, "two declared stress mechanisms")
    parsed = []
    for mechanism, name in zip(mechanisms, ("forward", "reverse"), strict=True):
        _fields(mechanism, ("mechanism_id", "worlds"), "AB mechanism fields")
        _require(
            type(mechanism["mechanism_id"]) is str and mechanism["mechanism_id"] == name,
            "AB mechanism order",
        )
        projected = {**problem["nominal"], "worlds": mechanism["worlds"]}
        parsed.append(_prepare(projected))
    nominal_risks = sum(len(risks) for _, models in nominal for risks in models)
    nominal_visits = 4 * 3 * sum(range(1, 5))
    nominal_selections = 4 * 4 * 3
    nominal_work = nominal_risks + nominal_visits + nominal_selections
    stress_risks = sum(
        len(risks) for mechanism in parsed for _, models in mechanism for risks in models
    )
    world_visits = len(parsed) * 4 * 3 * sum(range(1, 5))
    classification_visits = len(parsed) * 4 * 4 * 3
    shift_terms = 2 * classification_visits
    total = nominal_work + stress_risks + world_visits + shift_terms + classification_visits
    _require(nominal_risks <= MAX_RISK_CELLS, "planned nominal risk-cell cap")
    _require(nominal_work <= MAX_DECISION_WORK, "planned nominal decision-work cap")
    _require(stress_risks <= MAX_STRESS_RISK_CELLS, "planned stressed risk-cell cap")
    _require(total <= MAX_TOTAL_WORK, "planned complete nominal/stress work cap")
    return parsed, (
        nominal_work,
        stress_risks,
        world_visits,
        shift_terms,
        classification_visits,
        total,
    )


def analyze(problem):
    """Stress every frozen nominal candidate/tie without a stressed argmin."""
    parsed, plan = _prepare_ab(problem)
    # All wrapper/nominal/stress schemas and work caps precede every AA/AB
    # retained subtraction and every nominal minimax or stressed maximum scan.
    baseline = _analyze_nominal(problem["nominal"])
    _require(baseline["counts"]["total_decision_work"] == plan[0], "planned baseline work")
    mechanisms = []
    excess_terms = world_visits = shift_terms = classifications = old_evaluations = 0
    for mid, data in enumerate(parsed):
        worlds, excesses = [], []
        for actual, (coarse, models) in enumerate(data):
            model_wires, model_values = [], []
            for assumed, risks in enumerate(models):
                signed = []
                for risk in risks:
                    signed.append(_difference(risk, coarse))
                    excess_terms += 1
                model_values.append(signed)
                model_wires.append(
                    {
                        "assumed_index": assumed,
                        "forecast_risks": [_wire(value) for value in risks],
                        "excess_risks": [_wire(value) for value in signed],
                    }
                )
            worlds.append(
                {"actual_index": actual, "coarse_risk": _wire(coarse), "models": model_wires}
            )
            excesses.append(model_values)
        certificates = []
        for nominal in baseline["decisions"]:
            assumed, bound = nominal["assumed_index"], nominal["bound_index"]
            actuals = list(range(bound + 1))
            _require(actuals == nominal["world_indices"], "unchanged nested uncertainty set")
            old_indices = list(nominal["minimizer_indices"])
            old_weights = [list(value) for value in nominal["minimizer_weights"]]
            minimum = F(*nominal["minimax_excess"])
            old_evaluations += len(old_indices)
            candidates = []
            for rule, weight in enumerate(RETAINED_WEIGHTS):
                vector = []
                for actual in actuals:
                    vector.append(excesses[actual][assumed][rule])
                    world_visits += 1
                worst = max(vector)
                maxima = [i for i in actuals if excesses[i][assumed][rule] == worst]
                previous = F(*nominal["candidates"][rule]["worst_excess"])
                delta = _shift(worst, previous)
                margin = _shift(worst, minimum)
                shift_terms += 2
                is_old = rule in old_indices
                safe, strict, preserved = worst <= 0, worst < 0, worst <= minimum
                unsafe_worlds = [i for i in actuals if excesses[i][assumed][rule] > 0]
                breaking_worlds = [i for i in actuals if excesses[i][assumed][rule] > minimum]
                _require(
                    bool(maxima) and all(value <= worst for value in vector),
                    "complete stressed maximum",
                )
                _require(
                    safe == (not unsafe_worlds) and preserved == (not breaking_worlds),
                    "complete actual-world adverse witnesses",
                )
                _require(
                    preserved == (margin <= 0) and strict == (worst < 0),
                    "signed original-bound comparison",
                )
                _require(is_old == (previous == minimum), "unchanged nominal selection membership")
                if rule == 0:
                    _require(
                        vector == [F(0)] * len(actuals) and worst == 0,
                        "same-law coarse zero stress excess",
                    )
                candidates.append(
                    {
                        "retained_weight": _wire(weight),
                        "world_excesses": [_wire(value) for value in vector],
                        "worst_excess": _wire(worst),
                        "worst_world_indices": maxima,
                        "nominal_worst_excess": _wire(previous),
                        "worst_shift": _shift_wire(delta),
                        "bound_excess": _shift_wire(margin),
                        "nominal_minimizer": is_old,
                        "coarse_safe": safe,
                        "strict_benefit": strict,
                        "original_bound_preserved": preserved,
                        "unsafe_world_indices": unsafe_worlds,
                        "bound_breaking_world_indices": breaking_worlds,
                    }
                )
                classifications += 1
            safe_old = [k for k in old_indices if candidates[k]["coarse_safe"]]
            strict_old = [k for k in old_indices if candidates[k]["strict_benefit"]]
            preserving_old = [k for k in old_indices if candidates[k]["original_bound_preserved"]]
            unsafe_old = [k for k in old_indices if not candidates[k]["coarse_safe"]]
            breaking_old = [k for k in old_indices if not candidates[k]["original_bound_preserved"]]
            _require(bool(old_indices), "nominal minimizing set nonempty")
            _require(
                sorted(safe_old + unsafe_old) == old_indices
                and sorted(preserving_old + breaking_old) == old_indices,
                "old-set classifications complete and disjoint",
            )
            quantifiers = {
                "all_old_safe": len(safe_old) == len(old_indices),
                "any_old_safe": bool(safe_old),
                "all_old_strict": len(strict_old) == len(old_indices),
                "any_old_strict": bool(strict_old),
                "all_old_bound_preserved": len(preserving_old) == len(old_indices),
                "any_old_bound_preserved": bool(preserving_old),
            }
            for short, flag in (
                ("safe", "coarse_safe"),
                ("strict", "strict_benefit"),
                ("bound_preserved", "original_bound_preserved"),
            ):
                _require(
                    quantifiers["all_old_" + short] == all(candidates[k][flag] for k in old_indices)
                    and quantifiers["any_old_" + short]
                    == any(candidates[k][flag] for k in old_indices),
                    "exact old-set all/any quantifiers",
                )
            certificates.append(
                {
                    "assumed_index": assumed,
                    "bound_index": bound,
                    "world_indices": actuals,
                    "nominal_minimax_excess": _wire(minimum),
                    "old_minimizer_indices": old_indices,
                    "old_minimizer_weights": old_weights,
                    "candidates": candidates,
                    "safe_old_indices": safe_old,
                    "strictly_beneficial_old_indices": strict_old,
                    "bound_preserving_old_indices": preserving_old,
                    "unsafe_old_indices": unsafe_old,
                    "bound_breaking_old_indices": breaking_old,
                    **quantifiers,
                    "checks": dict.fromkeys(STRESS_CHECKS, True),
                }
            )
        mechanisms.append(
            {
                "mechanism_id": ("forward", "reverse")[mid],
                "worlds": worlds,
                "certificates": certificates,
            }
        )
    executed = (
        baseline["counts"]["total_decision_work"],
        excess_terms,
        world_visits,
        shift_terms,
        classifications,
        baseline["counts"]["total_decision_work"]
        + excess_terms
        + world_visits
        + shift_terms
        + classifications,
    )
    _require(executed == plan, "planned/executed AB work accounting")
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "baseline": baseline,
        "mechanisms": mechanisms,
        "counts": {
            "mechanisms": 2,
            "worlds": 8,
            "assumed_models": 8,
            "rules": 6,
            "certificates": 32,
            "candidate_certificates": 96,
            "old_rule_evaluations": old_evaluations,
            "stress_risk_cells": excess_terms,
            "baseline_decision_work": executed[0],
            "stress_excess_terms": excess_terms,
            "candidate_world_visits": world_visits,
            "shift_terms": shift_terms,
            "candidate_classification_visits": classifications,
            "total_work_terms": executed[-1],
        },
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "AB canonical output byte cap")
    return json.loads(encoded)
