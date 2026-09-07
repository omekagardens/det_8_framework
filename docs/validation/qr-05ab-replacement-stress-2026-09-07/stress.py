"""Exact replacement stress with a statically carried nominal AA baseline.

The risk-table API authenticates no forecast law or mechanism origin. Every
nominal minimizing rule is preserved, without a stressed reoptimization.
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


MAX_STRESS_RISK_CELLS = 96
MAX_TOTAL_WORK = 840
MECHANISMS = ("forward", "reverse")


def _shift(left, right):
    """Retain a new excess/bound difference without bounding intermediates."""
    value = left - right
    _require(
        type(value) is Fraction
        and -4 <= value <= 4
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift outside score or bit bounds",
    )
    return value


def _shift_pair(value):
    _require(
        type(value) is Fraction
        and -4 <= value <= 4
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained shift outside score or bit bounds",
    )
    return [value.numerator, value.denominator]


def _prepare_ab(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "nominal", "mechanisms"))
    _require(
        problem["schema_version"] == "det8-qr05ab-problem-v1"
        and problem["family"] == "qr05ab_replacement_stress",
        "unknown replacement-stress schema",
    )
    nominal = problem["nominal"]
    _, _, nominal_counts = _prepare(nominal)
    supplied = problem["mechanisms"]
    _require(type(supplied) is list and len(supplied) == 2, "exactly two mechanisms required")
    mechanisms = []
    for expected, mechanism in zip(MECHANISMS, supplied):
        _fields(mechanism, ("mechanism_id", "worlds"))
        _require(mechanism["mechanism_id"] == expected, "mechanism order differs")
        # Reuse only this source's own AA input parser, never its decision scan.
        validation_problem = {
            "schema_version": nominal["schema_version"],
            "family": nominal["family"],
            "levels": nominal["levels"],
            "retained_weights": nominal["retained_weights"],
            "worlds": mechanism["worlds"],
        }
        coarse, risks, _ = _prepare(validation_problem)
        mechanisms.append((expected, coarse, risks))

    risk_cells = sum(len(row) for _, _, risks in mechanisms for world in risks for row in world)
    certificate_count = sum(len(risks) * len(risks[0]) for _, _, risks in mechanisms)
    candidate_count = sum(
        len(risks) * len(risks[0]) * len(risks[0][0]) for _, _, risks in mechanisms
    )
    world_visits = sum(
        len(risks[0]) * len(risks[0][0]) * sum(range(1, len(risks) + 1))
        for _, _, risks in mechanisms
    )
    planned = {
        "mechanisms": len(mechanisms),
        "worlds": sum(len(risks) for _, _, risks in mechanisms),
        "assumed_models": sum(len(risks[0]) for _, _, risks in mechanisms),
        "rules": sum(len(risks[0][0]) for _, _, risks in mechanisms),
        "certificates": certificate_count,
        "candidate_certificates": candidate_count,
        "stress_risk_cells": risk_cells,
        "baseline_decision_work": nominal_counts["total_decision_work"],
        "stress_excess_terms": risk_cells,
        "candidate_world_visits": world_visits,
        "shift_terms": 2 * candidate_count,
        "candidate_classification_visits": candidate_count,
        "total_work_terms": nominal_counts["total_decision_work"]
        + risk_cells
        + world_visits
        + 2 * candidate_count
        + candidate_count,
    }
    _require(risk_cells <= MAX_STRESS_RISK_CELLS, "stress risk-cell cap exceeded")
    _require(planned["total_work_terms"] <= MAX_TOTAL_WORK, "total decision-work cap exceeded")
    return mechanisms, planned


def _stress_worlds(coarse, risks):
    worlds, excess, terms = [], [], 0
    for actual, supplied_models in enumerate(risks):
        models, excess_rows = [], []
        for assumed, risk_row in enumerate(supplied_models):
            values = []
            for risk in risk_row:
                values.append(_difference(risk, coarse[actual]))
                terms += 1
            excess_rows.append(values)
            models.append(
                {
                    "assumed_index": assumed,
                    "forecast_risks": [_pair(risk) for risk in risk_row],
                    "excess_risks": [_pair(value) for value in values],
                }
            )
        worlds.append(
            {"actual_index": actual, "coarse_risk": _pair(coarse[actual]), "models": models}
        )
        excess.append(excess_rows)
    return worlds, excess, terms


def _stress_certificates(excess, baseline):
    certificates = []
    world_visits = shift_terms = classifications = old_slots = 0
    for assumed in range(len(excess[0])):
        previous_worlds = []
        for bound in range(len(excess)):
            nominal = baseline["decisions"][assumed * len(excess) + bound]
            _require(
                nominal["assumed_index"] == assumed and nominal["bound_index"] == bound,
                "nominal certificate alignment differs",
            )
            nominal_value = _checked(Fraction(*nominal["minimax_excess"]))
            old_indices = nominal["minimizer_indices"][:]
            old_weights = [weight[:] for weight in nominal["minimizer_weights"]]
            _require(
                old_indices and len(old_indices) == len(old_weights), "empty nominal selection"
            )
            world_indices = list(range(bound + 1))
            candidates, maxima = [], []
            complete_argmax = signed_bound_comparison = witnesses_complete = True
            for rule, weight in enumerate(RETAINED_WEIGHTS):
                values, maximizers, unsafe_worlds, breaking_worlds, worst = [], [], [], [], None
                for actual in world_indices:
                    value = excess[actual][assumed][rule]
                    world_visits += 1
                    values.append(value)
                    if worst is None or value > worst:
                        worst, maximizers = value, [actual]
                    elif value == worst:
                        maximizers.append(actual)
                    if value > 0:
                        unsafe_worlds.append(actual)
                    if value > nominal_value:
                        breaking_worlds.append(actual)

                nominal_worst = _checked(Fraction(*nominal["candidates"][rule]["worst_excess"]))
                worst_shift = _shift(worst, nominal_worst)
                shift_terms += 1
                bound_excess = _shift(worst, nominal_value)
                shift_terms += 1
                classifications += 1
                old_choice = rule in old_indices
                if old_choice:
                    old_slots += 1
                safe, strict, preserved = worst <= 0, worst < 0, worst <= nominal_value
                complete_argmax = complete_argmax and (
                    worst is not None
                    and all(value <= worst for value in values)
                    and maximizers
                    == [actual for actual, value in zip(world_indices, values) if value == worst]
                )
                witnesses_complete = witnesses_complete and (
                    unsafe_worlds
                    == [actual for actual, value in zip(world_indices, values) if value > 0]
                    and breaking_worlds
                    == [
                        actual
                        for actual, value in zip(world_indices, values)
                        if value > nominal_value
                    ]
                )
                signed_bound_comparison = signed_bound_comparison and (
                    worst_shift + nominal_worst == worst
                    and bound_excess + nominal_value == worst
                    and safe == (not unsafe_worlds)
                    and strict == all(value < 0 for value in values)
                    and preserved == (not breaking_worlds)
                    and preserved == (bound_excess <= 0)
                )
                candidates.append(
                    {
                        "retained_weight": _pair(weight),
                        "world_excesses": [_pair(value) for value in values],
                        "worst_excess": _pair(worst),
                        "worst_world_indices": maximizers,
                        "nominal_worst_excess": _pair(nominal_worst),
                        "worst_shift": _shift_pair(worst_shift),
                        "bound_excess": _shift_pair(bound_excess),
                        "nominal_minimizer": old_choice,
                        "coarse_safe": safe,
                        "strict_benefit": strict,
                        "original_bound_preserved": preserved,
                        "unsafe_world_indices": unsafe_worlds,
                        "bound_breaking_world_indices": breaking_worlds,
                    }
                )
                maxima.append(worst)

            safe_old = [rule for rule in old_indices if candidates[rule]["coarse_safe"]]
            strict_old = [rule for rule in old_indices if candidates[rule]["strict_benefit"]]
            preserving_old = [
                rule for rule in old_indices if candidates[rule]["original_bound_preserved"]
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
                "all_old_bound_preserved": len(preserving_old) == len(old_indices),
                "any_old_bound_preserved": bool(preserving_old),
            }
            quantified = (
                quantifiers["all_old_safe"] == all(maxima[rule] <= 0 for rule in old_indices)
                and quantifiers["any_old_safe"] == any(maxima[rule] <= 0 for rule in old_indices)
                and quantifiers["all_old_strict"] == all(maxima[rule] < 0 for rule in old_indices)
                and quantifiers["any_old_strict"] == any(maxima[rule] < 0 for rule in old_indices)
                and quantifiers["all_old_bound_preserved"]
                == all(maxima[rule] <= nominal_value for rule in old_indices)
                and quantifiers["any_old_bound_preserved"]
                == any(maxima[rule] <= nominal_value for rule in old_indices)
                and safe_old == [rule for rule in old_indices if rule not in unsafe_old]
                and preserving_old == [rule for rule in old_indices if rule not in breaking_old]
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
                "complete_argmax": complete_argmax,
                "all_any_quantifiers": quantified,
                "signed_bound_comparison": signed_bound_comparison,
                "coarse_zero": all(
                    value == 0 for value in excess_row(excess, world_indices, assumed, 0)
                ),
                "nested_worlds": world_indices == [*previous_worlds, bound],
                "world_witnesses_complete": witnesses_complete,
            }
            _require(
                all(value is True for value in checks.values()),
                "stress certificate identity failed",
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
                    "bound_preserving_old_indices": preserving_old,
                    "unsafe_old_indices": unsafe_old,
                    "bound_breaking_old_indices": breaking_old,
                    **quantifiers,
                    "checks": checks,
                }
            )
            previous_worlds = world_indices
    return certificates, world_visits, shift_terms, classifications, old_slots


def excess_row(excess, world_indices, assumed, rule):
    return [excess[actual][assumed][rule] for actual in world_indices]


def analyze(problem):
    """Stress the nominal minimizer sets without computing a stressed argmin."""
    mechanisms, planned = _prepare_ab(problem)
    input_sha256 = hashlib.sha256(canonical(problem)).hexdigest()
    baseline = _analyze_nominal(problem["nominal"])
    baseline_snapshot = canonical(baseline)
    _require(
        baseline["counts"]["total_decision_work"] == planned["baseline_decision_work"],
        "nominal executed work differs from plan",
    )
    expected_old_slots = len(mechanisms) * sum(
        len(decision["minimizer_indices"]) for decision in baseline["decisions"]
    )
    output_mechanisms = []
    stress_excess_terms = candidate_world_visits = shift_terms = classification_visits = (
        old_slots
    ) = 0
    for mechanism_id, coarse, risks in mechanisms:
        worlds, excess, terms = _stress_worlds(coarse, risks)
        certificates, visits, shifts, classifications, old = _stress_certificates(excess, baseline)
        output_mechanisms.append(
            {"mechanism_id": mechanism_id, "worlds": worlds, "certificates": certificates}
        )
        stress_excess_terms += terms
        candidate_world_visits += visits
        shift_terms += shifts
        classification_visits += classifications
        old_slots += old

    counts = {
        "mechanisms": len(output_mechanisms),
        "worlds": sum(len(mechanism["worlds"]) for mechanism in output_mechanisms),
        "assumed_models": sum(
            len(mechanism["worlds"][0]["models"]) for mechanism in output_mechanisms
        ),
        "rules": sum(
            len(mechanism["worlds"][0]["models"][0]["forecast_risks"])
            for mechanism in output_mechanisms
        ),
        "certificates": sum(len(mechanism["certificates"]) for mechanism in output_mechanisms),
        "candidate_certificates": sum(
            len(certificate["candidates"])
            for mechanism in output_mechanisms
            for certificate in mechanism["certificates"]
        ),
        "old_rule_evaluations": old_slots,
        "stress_risk_cells": sum(
            len(model["forecast_risks"])
            for mechanism in output_mechanisms
            for world in mechanism["worlds"]
            for model in world["models"]
        ),
        "baseline_decision_work": baseline["counts"]["total_decision_work"],
        "stress_excess_terms": stress_excess_terms,
        "candidate_world_visits": candidate_world_visits,
        "shift_terms": shift_terms,
        "candidate_classification_visits": classification_visits,
        "total_work_terms": baseline["counts"]["total_decision_work"]
        + stress_excess_terms
        + candidate_world_visits
        + shift_terms
        + classification_visits,
    }
    _require(
        {name: value for name, value in counts.items() if name != "old_rule_evaluations"}
        == planned,
        "executed stress work differs from preflight",
    )
    _require(
        old_slots == expected_old_slots and old_slots <= counts["candidate_certificates"],
        "old-rule inventory differs from original selections",
    )
    _require(canonical(baseline) == baseline_snapshot, "nominal AA baseline changed during stress")
    result = {
        "input_sha256": input_sha256,
        "baseline": baseline,
        "mechanisms": output_mechanisms,
        "counts": counts,
    }
    return json.loads(canonical(result))
