"""Exact finite uncertainty decisions on supplied risks, without origin claims.

The native preflight is statically carried from this primary's prior guard
lineage. Decision validation and single-pass extrema are implemented here;
no prior or alternative executor is imported.
"""

import hashlib
import json
from fractions import Fraction
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 65536
MAX_BYTES = 1048576
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


def analyze(problem):
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
