"""QR-05Z fixed attenuation with this primary's statically carried Y policy.

This module authenticates no channel origin. It accepts normalized exact
report/future laws, checks their shared future marginal, and scores all fixed
actual/assumed pairs with explicit forecast completion and original X scores.
"""

import hashlib
import json
from fractions import Fraction
from math import gcd

MAX_BELIEFS = 512
MAX_CELLS_PER_CHANNEL = 4096
MAX_ATOMS_PER_PREDICTION = 4096
MAX_INPUT_CELLS = 32768
MAX_INPUT_PREDICTION_ATOMS = 2097152
MAX_PAIR_CELLS = 131072
MAX_SCORING_TERMS = 33554432
MAX_FALLBACKS_PER_BELIEF = 16384
MAX_INPUT_FALLBACKS = 32768
MAX_INPUT_FALLBACK_ATOMS = 2097152
MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 8388608
MAX_BYTES = 134217728

LEVELS = (Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1))


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _string_size(value):
    size = 2
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
    """Bound the expanded value tree and canonical bytes before serialization."""
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


def _fraction(value, *, positive=False):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _integer(numerator, int(positive), (1 << MAX_BITS) - 1)
    _integer(denominator, 1, (1 << MAX_BITS) - 1)
    _require(numerator <= denominator and gcd(numerator, denominator) == 1, "invalid probability")
    return Fraction(numerator, denominator)


def _checked(value, upper=Fraction(2)):
    _require(
        type(value) is Fraction
        and 0 <= value <= upper
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained exact rational outside score or bit bound",
    )
    return value


def _pair(value, upper=Fraction(2)):
    _checked(value, upper)
    return [value.numerator, value.denominator]


def _symbol(value, length=7):
    _require(type(value) is list and len(value) == length, "symbol has wrong native dimension")
    for coordinate in value:
        _integer(coordinate, 0, (1 << 64) - 1)
    return tuple(value)


def _prediction(atoms):
    _require(
        type(atoms) is list and 1 <= len(atoms) <= MAX_ATOMS_PER_PREDICTION,
        "prediction support exceeds its cap",
    )
    law, previous = {}, None
    for atom in atoms:
        _fields(atom, ("value", "probability"))
        value = _symbol(atom["value"])
        _require(previous is None or previous < value, "future symbols must be sorted unique")
        previous = value
        law[value] = _fraction(atom["probability"], positive=True)
    _require(sum(law.values(), Fraction(0)) == 1, "prediction must have exact unit mass")
    return law


def _law_wire(law):
    return [
        {"value": list(value), "probability": _pair(probability, Fraction(1))}
        for value, probability in sorted(law.items())
    ]


def _risk(law):
    return _checked(1 - sum((p * p for p in law.values()), Fraction(0)), Fraction(1))


def _signed_pair(value):
    _require(
        type(value) is Fraction
        and -2 <= value <= 2
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained signed gain outside score or bit bound",
    )
    return [value.numerator, value.denominator]


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "beliefs"))
    _require(
        problem["schema_version"] == "det8-qr05y-problem-v1"
        and problem["family"] == "qr05y_explicit_fallback",
        "unknown explicit-fallback scoring schema",
    )
    supplied = problem["beliefs"]
    _require(
        type(supplied) is list and 1 <= len(supplied) <= MAX_BELIEFS,
        "belief count outside cap",
    )
    beliefs, weights = [], []
    counts = {
        "input_cells": 0,
        "input_prediction_atoms": 0,
        "input_fallbacks": 0,
        "input_fallback_atoms": 0,
    }
    for bid, row in enumerate(supplied):
        _fields(row, ("belief_id", "weight", "channels", "fallbacks"))
        _integer(row["belief_id"], bid, bid)
        weight = _fraction(row["weight"], positive=True)
        weights.append(weight)
        _require(
            type(row["channels"]) is list and len(row["channels"]) == 4,
            "exactly four conditional experiments required",
        )
        channels, common_future, prefixes = [], None, set()
        for index, channel in enumerate(row["channels"]):
            _fields(channel, ("level", "cells"))
            _require(_fraction(channel["level"]) == LEVELS[index], "fixed level order differs")
            atoms = channel["cells"]
            _require(
                type(atoms) is list and 1 <= len(atoms) <= MAX_CELLS_PER_CHANNEL,
                "report cell count outside cap",
            )
            cells, previous, marginal = {}, None, {}
            counts["input_cells"] += len(atoms)
            _require(counts["input_cells"] <= MAX_INPUT_CELLS, "total input cell cap exceeded")
            for atom in atoms:
                _fields(atom, ("value", "probability", "prediction"))
                symbol = _symbol(atom["value"])
                _require(
                    previous is None or previous < symbol, "report values must be sorted unique"
                )
                previous = symbol
                prefixes.add(symbol[:5])
                probability = _fraction(atom["probability"], positive=True)
                law = _prediction(atom["prediction"])
                counts["input_prediction_atoms"] += len(law)
                _require(
                    counts["input_prediction_atoms"] <= MAX_INPUT_PREDICTION_ATOMS,
                    "input channel prediction atom cap exceeded",
                )
                for q, p in law.items():
                    marginal[q] = marginal.get(q, Fraction(0)) + probability * p
                cells[symbol] = {
                    "value": symbol,
                    "probability": probability,
                    "prediction": law,
                    "bayes_risk": _risk(law),
                }
            _require(
                sum((cell["probability"] for cell in cells.values()), Fraction(0)) == 1,
                "report cells must have exact unit mass",
            )
            if common_future is None:
                common_future = marginal
            else:
                _require(
                    marginal == common_future, "conditional experiments change future marginal"
                )
            channels.append(cells)
        supplied_fallbacks = row["fallbacks"]
        _require(
            type(supplied_fallbacks) is list
            and 1 <= len(supplied_fallbacks) <= MAX_FALLBACKS_PER_BELIEF,
            "fallback table count outside cap",
        )
        counts["input_fallbacks"] += len(supplied_fallbacks)
        _require(
            counts["input_fallbacks"] <= MAX_INPUT_FALLBACKS, "total fallback count cap exceeded"
        )
        fallbacks, previous = {}, None
        for atom in supplied_fallbacks:
            _fields(atom, ("value", "prediction"))
            prefix = _symbol(atom["value"], 5)
            _require(
                previous is None or previous < prefix, "fallback prefixes must be sorted unique"
            )
            previous = prefix
            law = _prediction(atom["prediction"])
            counts["input_fallback_atoms"] += len(law)
            _require(
                counts["input_fallback_atoms"] <= MAX_INPUT_FALLBACK_ATOMS,
                "input fallback prediction atom cap exceeded",
            )
            fallbacks[prefix] = law
        _require(
            fallbacks.keys() == prefixes, "fallback keys must exactly cover all report prefixes"
        )
        beliefs.append(
            {"belief_id": bid, "weight": weight, "channels": channels, "fallbacks": fallbacks}
        )
    _require(sum(weights, Fraction(0)) == 1, "history weights must have exact unit mass")
    planned_cells = counts["input_cells"] * 4
    _require(planned_cells <= MAX_PAIR_CELLS, "planned pair cell cap exceeded")
    completed_terms, coarse_terms = 0, 0
    for row in beliefs:
        for actual in row["channels"]:
            for assumed in row["channels"]:
                for value, cell in actual.items():
                    old = assumed.get(value)
                    coarse = row["fallbacks"][value[:5]]
                    chosen = old["prediction"] if old is not None else coarse
                    completed_terms += len(cell["prediction"]) + len(chosen)
                    coarse_terms += len(cell["prediction"]) + len(coarse)
                    _require(
                        completed_terms + coarse_terms <= MAX_SCORING_TERMS,
                        "planned chosen and coarse scoring term cap exceeded",
                    )
    return beliefs, counts, planned_cells, completed_terms, coarse_terms


def _score(actual, forecast):
    """Direct quadratic risk and independent squared-distance regret.

    The two sparse support traversals match the declared scoring-work metric.
    Signed dot-product intermediates are not treated as probabilities.
    """
    actual_square, forecast_square, dot, regret = (Fraction(0) for _ in range(4))
    visits = 0
    for q, p in actual.items():
        f = forecast.get(q, Fraction(0))
        actual_square += p * p
        dot += p * f
        regret += (p - f) ** 2
        visits += 1
    for q, f in forecast.items():
        forecast_square += f * f
        if q not in actual:
            regret += f * f
        visits += 1
    bayes = _checked(1 - actual_square, Fraction(1))
    scored = _checked(1 - 2 * dot + forecast_square)
    regret = _checked(regret)
    equal = actual == forecast
    _require(scored == bayes + regret, "quadratic Brier decomposition differs")
    _require((regret == 0) == equal, "zero regret does not characterize complete law equality")
    return bayes, scored, regret, equal, visits


X_SCALARS = (
    "coverage",
    "unsupported_mass",
    "bayes_risk",
    "supported_bayes_risk",
    "supported_forecast_risk",
    "supported_regret",
)
NEW_SCALARS = (
    "fallback_bayes_risk",
    "fallback_forecast_risk",
    "fallback_regret",
    "completed_forecast_risk",
    "completed_regret",
    "coarse_forecast_risk",
    "coarse_regret",
    "gain_over_coarse",
)
CHECKS = (
    "policy_total",
    "mass_partition",
    "split_decomposition",
    "completed_decomposition",
    "coarse_decomposition",
    "gain_identity",
    "supported_forecasts_preserved",
    "zero_regret_iff_equal",
)


def _verify_totals(totals, supported_gain, completed_equal, coarse_equal):
    coverage = totals["coverage"]
    missing = totals["unsupported_mass"]
    _require(coverage + missing == 1, "supported and fallback masses do not partition one")
    _checked(coverage, Fraction(1))
    _checked(missing, Fraction(1))
    _checked(totals["bayes_risk"], Fraction(1))
    for branch, mass in (("supported", coverage), ("fallback", missing)):
        bayes, risk, regret = (
            totals[branch + suffix] for suffix in ("_bayes_risk", "_forecast_risk", "_regret")
        )
        _checked(bayes, mass)
        _checked(risk, 2 * mass)
        _checked(regret, 2 * mass)
        _require(risk == bayes + regret, "branch Bayes/risk/regret decomposition differs")
    _require(
        totals["bayes_risk"] == totals["supported_bayes_risk"] + totals["fallback_bayes_risk"],
        "split Bayes contributions differ from full Bayes risk",
    )
    _require(
        totals["completed_forecast_risk"]
        == totals["supported_forecast_risk"] + totals["fallback_forecast_risk"],
        "completed risk differs from original-weight branch contributions",
    )
    _require(
        totals["completed_regret"] == totals["supported_regret"] + totals["fallback_regret"],
        "completed regret differs from branch contributions",
    )
    for name in ("completed", "coarse"):
        risk, regret = totals[name + "_forecast_risk"], totals[name + "_regret"]
        _checked(risk)
        _checked(regret)
        _require(risk == totals["bayes_risk"] + regret, name + " full decomposition differs")
    gain = totals["gain_over_coarse"]
    _signed_pair(gain)
    _require(
        gain
        == totals["coarse_forecast_risk"] - totals["completed_forecast_risk"]
        == totals["coarse_regret"] - totals["completed_regret"]
        == supported_gain,
        "gain differs from risk/regret difference or supported-only contribution",
    )
    _require(abs(gain) <= 2 * coverage, "signed gain exceeds its supported-mass bound")
    _require(
        (totals["completed_regret"] == 0) == all(completed_equal),
        "zero completed regret does not characterize full future-law equality",
    )
    _require(
        (totals["coarse_regret"] == 0) == all(coarse_equal),
        "zero coarse regret does not characterize full future-law equality",
    )


def _x_scores(totals):
    complete = totals["coverage"] == 1
    if complete:
        _require(
            totals["fallback_forecast_risk"] == totals["fallback_regret"] == 0,
            "complete X pair used fallback mass",
        )
        _require(
            totals["supported_forecast_risk"] == totals["bayes_risk"] + totals["supported_regret"],
            "original complete X decomposition differs",
        )
    return {
        **{name: _pair(totals[name]) for name in X_SCALARS},
        "forecast_risk": _pair(totals["supported_forecast_risk"]) if complete else None,
        "regret": _pair(totals["supported_regret"]) if complete else None,
        "complete": complete,
    }


def _new_scores(totals):
    return {
        name: _signed_pair(totals[name]) if name == "gain_over_coarse" else _pair(totals[name])
        for name in NEW_SCALARS
    }


def _pair_result(actual_index, assumed_index, actual, assumed, fallbacks):
    totals = {name: Fraction(0) for name in X_SCALARS + NEW_SCALARS}
    cells, completed_equal, coarse_equal = [], [], []
    completed_terms, coarse_terms, supported_gain = 0, 0, Fraction(0)
    for value, cell in actual.items():
        probability, law = cell["probability"], cell["prediction"]
        old = assumed.get(value)
        supported = old is not None
        coarse = fallbacks[value[:5]]
        chosen = old["prediction"] if supported else coarse
        bayes, risk, regret, equal, visits = _score(law, chosen)
        other_bayes, coarse_risk, coarse_regret, other_equal, other_visits = _score(law, coarse)
        completed_terms += visits
        coarse_terms += other_visits
        _require(
            bayes == other_bayes == cell["bayes_risk"],
            "actual Bayes risk changed between comparators",
        )
        gain = coarse_risk - risk
        _require(gain == coarse_regret - regret, "conditional signed gain identity differs")
        if supported:
            _require(chosen == old["prediction"], "supported assumed forecast was replaced")
            branch = "supported"
            totals["coverage"] += probability
            supported_gain += probability * gain
        else:
            _require(
                chosen == coarse and gain == 0, "fallback-used cell differs from coarse policy"
            )
            branch = "fallback"
            totals["unsupported_mass"] += probability
        totals["bayes_risk"] += probability * bayes
        totals[branch + "_bayes_risk"] += probability * bayes
        totals[branch + "_forecast_risk"] += probability * risk
        totals[branch + "_regret"] += probability * regret
        totals["completed_forecast_risk"] += probability * risk
        totals["completed_regret"] += probability * regret
        totals["coarse_forecast_risk"] += probability * coarse_risk
        totals["coarse_regret"] += probability * coarse_regret
        totals["gain_over_coarse"] += probability * gain
        completed_equal.append(equal)
        coarse_equal.append(other_equal)
        cells.append(
            {
                "value": list(value),
                "actual_probability": _pair(probability, Fraction(1)),
                "assumed_probability": _pair(old["probability"], Fraction(1))
                if supported
                else [0, 1],
                "actual_prediction": _law_wire(law),
                "assumed_forecast": _law_wire(old["prediction"]) if supported else None,
                "coarse_forecast": _law_wire(coarse),
                "forecast": _law_wire(chosen),
                "supported": supported,
                "used_fallback": not supported,
                "bayes_risk": _pair(bayes, Fraction(1)),
                "forecast_risk": _pair(risk),
                "regret": _pair(regret),
                "coarse_risk": _pair(coarse_risk),
                "coarse_regret": _pair(coarse_regret),
                "gain_over_coarse": _signed_pair(gain),
                "predictions_equal": equal,
                "coarse_predictions_equal": other_equal,
            }
        )
    _verify_totals(totals, supported_gain, completed_equal, coarse_equal)
    original = _x_scores(totals)
    if actual_index == assumed_index:
        _require(
            original["complete"] and totals["completed_regret"] == 0,
            "diagonal Bayes control differs",
        )
    result = {
        "actual_index": actual_index,
        "assumed_index": assumed_index,
        "cells": cells,
        "x_scores": original,
        **_new_scores(totals),
        "checks": {name: True for name in CHECKS},
    }
    return result, completed_terms, coarse_terms


def _read_pair(value):
    return Fraction(*value)


def _aggregate(rows):
    weights = [_read_pair(row["weight"]) for row in rows]
    pairs = []
    for index in range(16):
        parts = [row["pairs"][index] for row in rows]
        totals = {
            name: sum(
                (
                    weight * _read_pair(part["x_scores"][name] if name in X_SCALARS else part[name])
                    for weight, part in zip(weights, parts, strict=True)
                ),
                Fraction(0),
            )
            for name in X_SCALARS + NEW_SCALARS
        }
        complete_count = sum(part["x_scores"]["complete"] for part in parts)
        _require(
            (complete_count == len(rows)) == (totals["coverage"] == 1),
            "aggregate coverage disagrees with positive-weight history completeness",
        )
        completed_equal = [cell["predictions_equal"] for part in parts for cell in part["cells"]]
        coarse_equal = [
            cell["coarse_predictions_equal"] for part in parts for cell in part["cells"]
        ]
        supported_gain = sum(
            (
                weight
                * sum(
                    (
                        _read_pair(cell["actual_probability"])
                        * _read_pair(cell["gain_over_coarse"])
                        for cell in part["cells"]
                        if cell["supported"]
                    ),
                    Fraction(0),
                )
                for weight, part in zip(weights, parts, strict=True)
            ),
            Fraction(0),
        )
        _verify_totals(totals, supported_gain, completed_equal, coarse_equal)
        pairs.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "x_scores": _x_scores(totals),
                **_new_scores(totals),
                "checks": {name: True for name in CHECKS},
                "complete_before_beliefs": complete_count,
                "incomplete_before_beliefs": len(rows) - complete_count,
            }
        )
    return {"total_weight": [1, 1], "pairs": pairs}


def _analyze_y(problem):
    beliefs, input_counts, planned_cells, planned_completed, planned_coarse = _prepare(problem)
    input_hash = hashlib.sha256(canonical(problem)).hexdigest()
    rows, completed_terms, coarse_terms = [], 0, 0
    counts = {
        "beliefs": len(beliefs),
        **input_counts,
        "pair_cells": [0] * 16,
        "supported_pair_cells": [0] * 16,
        "fallback_pair_cells": [0] * 16,
        "completed_scoring_terms": 0,
        "coarse_scoring_terms": 0,
        "complete_before_beliefs": [0] * 16,
        "incomplete_before_beliefs": [0] * 16,
        "positive_fallback_regret_beliefs": [0] * 16,
        "positive_completed_regret_beliefs": [0] * 16,
        "better_than_coarse_beliefs": [0] * 16,
        "equal_to_coarse_beliefs": [0] * 16,
        "worse_than_coarse_beliefs": [0] * 16,
    }
    witnesses = {
        "first_fallback": [None] * 16,
        "first_positive_fallback_regret": [None] * 16,
        "first_positive_completed_regret": [None] * 16,
        "first_better_than_coarse": [None] * 16,
        "first_equal_to_coarse": [None] * 16,
        "first_worse_than_coarse": [None] * 16,
    }
    for belief in beliefs:
        bid, pairs = belief["belief_id"], []
        for i, actual in enumerate(belief["channels"]):
            for j, assumed in enumerate(belief["channels"]):
                pair, visits, other_visits = _pair_result(
                    i, j, actual, assumed, belief["fallbacks"]
                )
                completed_terms += visits
                coarse_terms += other_visits
                index = 4 * i + j
                pairs.append(pair)
                supported = sum(cell["supported"] for cell in pair["cells"])
                counts["pair_cells"][index] += len(pair["cells"])
                counts["supported_pair_cells"][index] += supported
                counts["fallback_pair_cells"][index] += len(pair["cells"]) - supported
                complete = pair["x_scores"]["complete"]
                counts["complete_before_beliefs"][index] += int(complete)
                counts["incomplete_before_beliefs"][index] += int(not complete)
                positive_fallback = _read_pair(pair["fallback_regret"]) > 0
                positive_completed = _read_pair(pair["completed_regret"]) > 0
                gain = _read_pair(pair["gain_over_coarse"])
                counts["positive_fallback_regret_beliefs"][index] += int(positive_fallback)
                counts["positive_completed_regret_beliefs"][index] += int(positive_completed)
                counts["better_than_coarse_beliefs"][index] += int(gain > 0)
                counts["equal_to_coarse_beliefs"][index] += int(gain == 0)
                counts["worse_than_coarse_beliefs"][index] += int(gain < 0)
                for name, condition in (
                    ("first_fallback", _read_pair(pair["x_scores"]["unsupported_mass"]) > 0),
                    ("first_positive_fallback_regret", positive_fallback),
                    ("first_positive_completed_regret", positive_completed),
                    ("first_better_than_coarse", gain > 0),
                    ("first_equal_to_coarse", gain == 0),
                    ("first_worse_than_coarse", gain < 0),
                ):
                    if condition and witnesses[name][index] is None:
                        witnesses[name][index] = bid
        rows.append(
            {"belief_id": bid, "weight": _pair(belief["weight"], Fraction(1)), "pairs": pairs}
        )
    _require(sum(counts["pair_cells"]) == planned_cells, "planned and retained pair cells differ")
    _require(
        completed_terms == planned_completed, "planned and executed chosen support visits differ"
    )
    _require(coarse_terms == planned_coarse, "planned and executed coarse support visits differ")
    counts["completed_scoring_terms"] = completed_terms
    counts["coarse_scoring_terms"] = coarse_terms
    result = {
        "input_sha256": input_hash,
        "levels": [_pair(level, Fraction(1)) for level in LEVELS],
        "beliefs": rows,
        "aggregate": _aggregate(rows),
        "witnesses": witnesses,
        "counts": counts,
    }
    return json.loads(canonical(result))


# Z adds no imported executor: the entire Y policy above belongs to this
# primary's static source lineage and is recomputed only after all plans pass.
MAX_BLEND_CELLS = 393216
MAX_BLEND_ATOMS = 8388608
MAX_TOTAL_WORK_TERMS = 167772160
RETAINED_WEIGHTS = (Fraction(0), Fraction(1, 2), Fraction(1))
Z_CHECKS = (
    "normalization",
    "score_decomposition",
    "quadratic_risk_identity",
    "quadratic_gain_identity",
    "endpoint_recovery",
    "fallback_preserved",
    "zero_regret_iff_equal",
    "jensen_bound",
)


def _prepare_z(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "experiment"))
    _require(
        problem["schema_version"] == "det8-qr05z-problem-v1"
        and problem["family"] == "qr05z_fixed_attenuation",
        "unknown fixed-attenuation wrapper",
    )
    beliefs, _, pair_cells, completed, coarse = _prepare(problem["experiment"])
    plan = {
        "pair_cells": pair_cells,
        "blend_cells": 3 * pair_cells,
        "blend_atoms": 0,
        "mixture_terms": 0,
        "distance_terms": 0,
        "blend_scoring_terms": 0,
        "baseline_scoring_terms": completed + coarse,
        "total_work_terms": 0,
    }
    _require(plan["blend_cells"] <= MAX_BLEND_CELLS, "planned blend cell cap exceeded")
    for row in beliefs:
        for actual in row["channels"]:
            for assumed in row["channels"]:
                for value, cell in actual.items():
                    g = row["fallbacks"][value[:5]]
                    old = assumed.get(value)
                    f = old["prediction"] if old is not None else g
                    endpoint_visits = len(f) + len(g)
                    sizes = (len(g), len(f.keys() | g.keys()), len(f))
                    plan["blend_atoms"] += sum(sizes)
                    plan["mixture_terms"] += 3 * endpoint_visits
                    plan["distance_terms"] += endpoint_visits
                    plan["blend_scoring_terms"] += 3 * len(cell["prediction"]) + sum(sizes)
                    plan["total_work_terms"] = sum(
                        plan[key]
                        for key in (
                            "baseline_scoring_terms",
                            "mixture_terms",
                            "distance_terms",
                            "blend_scoring_terms",
                        )
                    )
                    _require(
                        plan["blend_atoms"] <= MAX_BLEND_ATOMS,
                        "planned mixed-law atom cap exceeded",
                    )
                    _require(
                        plan["total_work_terms"] <= MAX_TOTAL_WORK_TERMS,
                        "planned total Y/Z work cap exceeded before forecast scoring",
                    )
    return beliefs, plan


def _z_distance(f, g):
    value, visits = Fraction(0), 0
    for q, p in f.items():
        value += (p - g.get(q, Fraction(0))) ** 2
        visits += 1
    for q, p in g.items():
        if q not in f:
            value += p * p
        visits += 1
    _checked(value)
    _require((value == 0) == (f == g), "zero forecast deviation differs from full law equality")
    return value, visits


def _z_mix(f, g, retained):
    result, visits = {}, 0
    for law, coefficient in ((f, retained), (g, 1 - retained)):
        for q, p in law.items():
            result[q] = result.get(q, Fraction(0)) + coefficient * p
            visits += 1
    result = {q: p for q, p in result.items() if p}
    _require(result and sum(result.values(), Fraction(0)) == 1, "mixed forecast is not normalized")
    expected_support = (
        g.keys() if retained == 0 else f.keys() if retained == 1 else f.keys() | g.keys()
    )
    _require(
        result.keys() == expected_support, "mixed support was pruned or endpoint zero retained"
    )
    for p in result.values():
        _checked(p, Fraction(1))
    return result, visits


def _z_check_scores(blends, distance, base, equalities):
    _checked(distance)
    for index, retained in enumerate(RETAINED_WEIGHTS):
        row = blends[index]
        risk, regret = row["forecast_risk"], row["regret"]
        coarse_gain, base_gain = row["gain_over_coarse"], row["gain_over_base"]
        _checked(risk)
        _checked(regret)
        _signed_pair(coarse_gain)
        _signed_pair(base_gain)
        _require(risk == base["bayes_risk"] + regret, "blend Bayes decomposition differs")
        average = (1 - retained) * base["coarse_risk"] + retained * base["policy_risk"]
        _require(
            risk == average - retained * (1 - retained) * distance,
            "exact quadratic mixed-risk identity differs",
        )
        _require(
            coarse_gain
            == base["coarse_risk"] - risk
            == retained * base["gain"] + retained * (1 - retained) * distance,
            "exact quadratic coarse-gain identity differs",
        )
        _require(
            base_gain == base["policy_risk"] - risk == coarse_gain - base["gain"],
            "gain over completed Y policy differs",
        )
        _require(risk <= average, "Jensen risk upper bound failed")
        _require(
            (regret == 0) == all(equalities[index]),
            "zero blend regret requires complete actual-law equality",
        )
    _require(
        blends[0]["forecast_risk"] == base["coarse_risk"]
        and blends[0]["regret"] == base["coarse_regret"]
        and blends[0]["gain_over_coarse"] == 0,
        "coarse endpoint scores differ",
    )
    _require(
        blends[2]["forecast_risk"] == base["policy_risk"]
        and blends[2]["regret"] == base["policy_regret"]
        and blends[2]["gain_over_base"] == 0,
        "completed-Y endpoint scores differ",
    )


def _z_blend_wire(row):
    return {
        "retained_weight": _pair(row["retained_weight"], Fraction(1)),
        "forecast_risk": _pair(row["forecast_risk"]),
        "regret": _pair(row["regret"]),
        "gain_over_coarse": _signed_pair(row["gain_over_coarse"]),
        "gain_over_base": _signed_pair(row["gain_over_base"]),
    }


def _z_pair_base(row):
    return {
        "bayes_risk": _read_pair(row["x_scores"]["bayes_risk"]),
        "coarse_risk": _read_pair(row["coarse_forecast_risk"]),
        "coarse_regret": _read_pair(row["coarse_regret"]),
        "policy_risk": _read_pair(row["completed_forecast_risk"]),
        "policy_regret": _read_pair(row["completed_regret"]),
        "gain": _read_pair(row["gain_over_coarse"]),
    }


def _z_cell_base(cell):
    return {
        "bayes_risk": _read_pair(cell["bayes_risk"]),
        "coarse_risk": _read_pair(cell["coarse_risk"]),
        "coarse_regret": _read_pair(cell["coarse_regret"]),
        "policy_risk": _read_pair(cell["forecast_risk"]),
        "policy_regret": _read_pair(cell["regret"]),
        "gain": _read_pair(cell["gain_over_coarse"]),
    }


def _z_pair(i, j, supplied, baseline_pair):
    actual, assumed = supplied["channels"][i], supplied["channels"][j]
    _require(
        [list(v) for v in actual] == [c["value"] for c in baseline_pair["cells"]],
        "baseline report order or coverage differs",
    )
    totals = [
        {
            "retained_weight": retained,
            "forecast_risk": Fraction(0),
            "regret": Fraction(0),
            "gain_over_coarse": Fraction(0),
            "gain_over_base": Fraction(0),
        }
        for retained in RETAINED_WEIGHTS
    ]
    cells, distance_total = [], Fraction(0)
    equalities = [[], [], []]
    work = {"blend_atoms": 0, "mixture_terms": 0, "distance_terms": 0, "blend_scoring_terms": 0}
    for old_cell in baseline_pair["cells"]:
        value = tuple(old_cell["value"])
        current = actual[value]
        p, w = current["prediction"], current["probability"]
        old = assumed.get(value)
        g = supplied["fallbacks"][value[:5]]
        f = old["prediction"] if old is not None else g
        _require(
            old_cell["actual_prediction"] == _law_wire(p)
            and old_cell["actual_probability"] == _pair(w, Fraction(1))
            and old_cell["forecast"] == _law_wire(f)
            and old_cell["coarse_forecast"] == _law_wire(g)
            and old_cell["used_fallback"] == (old is None),
            "baseline actual law, policy or branch differs from declared input",
        )
        base = _z_cell_base(old_cell)
        distance, visits = _z_distance(f, g)
        work["distance_terms"] += visits
        distance_total += w * distance
        raw_blends, cell_blends = [], []
        for index, retained in enumerate(RETAINED_WEIGHTS):
            h, visits = _z_mix(f, g, retained)
            work["mixture_terms"] += visits
            work["blend_atoms"] += len(h)
            bayes, risk, regret, equal, visits = _score(p, h)
            work["blend_scoring_terms"] += visits
            _require(bayes == base["bayes_risk"], "rescored actual Bayes risk differs")
            coarse_gain, base_gain = base["coarse_risk"] - risk, base["policy_risk"] - risk
            score = {
                "retained_weight": retained,
                "forecast_risk": risk,
                "regret": regret,
                "gain_over_coarse": coarse_gain,
                "gain_over_base": base_gain,
            }
            raw_blends.append(score)
            equalities[index].append(equal)
            for name in ("forecast_risk", "regret", "gain_over_coarse", "gain_over_base"):
                totals[index][name] += w * score[name]
            cell_blends.append(
                {
                    **_z_blend_wire(score),
                    "forecast": _law_wire(h),
                    "predictions_equal": equal,
                }
            )
            if retained in (0, 1):
                _require(h == (g if retained == 0 else f), "complete endpoint forecast law differs")
            if old_cell["used_fallback"]:
                _require(
                    distance == 0
                    and h == f == g
                    and risk == base["policy_risk"]
                    and regret == base["policy_regret"],
                    "fallback law or positive generic fallback regret changed by blending",
                )
        _z_check_scores(raw_blends, distance, base, [[c["predictions_equal"]] for c in cell_blends])
        cells.append(
            {"value": list(value), "forecast_distance": _pair(distance), "blends": cell_blends}
        )
    _z_check_scores(totals, distance_total, _z_pair_base(baseline_pair), equalities)
    return {
        "actual_index": i,
        "assumed_index": j,
        "cells": cells,
        "forecast_distance": _pair(distance_total),
        "blends": [_z_blend_wire(row) for row in totals],
        "checks": {name: True for name in Z_CHECKS},
    }, work


def _z_aggregate(rows, baseline):
    weights = [_read_pair(row["weight"]) for row in rows]
    _require(sum(weights, Fraction(0)) == 1, "history weights lost normalization")
    pairs = []
    for index in range(16):
        parts = [row["pairs"][index] for row in rows]
        distance = sum(
            (
                w * _read_pair(part["forecast_distance"])
                for w, part in zip(weights, parts, strict=True)
            ),
            Fraction(0),
        )
        blends, equalities = [], []
        for blend_index, retained in enumerate(RETAINED_WEIGHTS):
            blends.append(
                {
                    "retained_weight": retained,
                    **{
                        name: sum(
                            (
                                w * _read_pair(part["blends"][blend_index][name])
                                for w, part in zip(weights, parts, strict=True)
                            ),
                            Fraction(0),
                        )
                        for name in (
                            "forecast_risk",
                            "regret",
                            "gain_over_coarse",
                            "gain_over_base",
                        )
                    },
                }
            )
            equalities.append(
                [
                    cell["blends"][blend_index]["predictions_equal"]
                    for part in parts
                    for cell in part["cells"]
                ]
            )
        _z_check_scores(
            blends, distance, _z_pair_base(baseline["aggregate"]["pairs"][index]), equalities
        )
        pairs.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "forecast_distance": _pair(distance),
                "blends": [_z_blend_wire(row) for row in blends],
                "checks": {name: True for name in Z_CHECKS},
            }
        )
    return {"total_weight": [1, 1], "pairs": pairs}


def analyze(problem):
    prepared, plan = _prepare_z(problem)
    input_hash = hashlib.sha256(canonical(problem)).hexdigest()
    baseline = _analyze_y(problem["experiment"])
    baseline_bytes = canonical(baseline)
    baseline_terms = (
        baseline["counts"]["completed_scoring_terms"] + baseline["counts"]["coarse_scoring_terms"]
    )
    _require(
        baseline_terms == plan["baseline_scoring_terms"],
        "planned and executed baseline work differs",
    )
    counts = {
        "beliefs": len(prepared),
        "pair_cells": [0] * 16,
        "blend_cells": [0] * 48,
        "blend_atoms": 0,
        "mixture_terms": 0,
        "distance_terms": 0,
        "blend_scoring_terms": 0,
        "baseline_scoring_terms": baseline_terms,
        "total_work_terms": 0,
        "positive_deviation_beliefs": [0] * 16,
        "positive_regret_beliefs": [0] * 48,
        "better_than_coarse_beliefs": [0] * 48,
        "equal_to_coarse_beliefs": [0] * 48,
        "worse_than_coarse_beliefs": [0] * 48,
        "better_than_base_beliefs": [0] * 48,
        "equal_to_base_beliefs": [0] * 48,
        "worse_than_base_beliefs": [0] * 48,
    }
    witnesses = {
        "first_positive_deviation": [None] * 16,
        **{
            name: [None] * 48
            for name in (
                "first_positive_regret",
                "first_better_than_coarse",
                "first_equal_to_coarse",
                "first_worse_than_coarse",
                "first_better_than_base",
                "first_equal_to_base",
                "first_worse_than_base",
            )
        },
    }
    rows = []
    for supplied, original in zip(prepared, baseline["beliefs"], strict=True):
        bid = supplied["belief_id"]
        _require(
            original["belief_id"] == bid
            and original["weight"] == _pair(supplied["weight"], Fraction(1)),
            "baseline history identity or likelihood changed",
        )
        pairs = []
        for i in range(4):
            for j in range(4):
                pair_index = 4 * i + j
                pair, work = _z_pair(i, j, supplied, original["pairs"][pair_index])
                pairs.append(pair)
                counts["pair_cells"][pair_index] += len(pair["cells"])
                for name, value in work.items():
                    counts[name] += value
                positive = _read_pair(pair["forecast_distance"]) > 0
                counts["positive_deviation_beliefs"][pair_index] += int(positive)
                if positive and witnesses["first_positive_deviation"][pair_index] is None:
                    witnesses["first_positive_deviation"][pair_index] = bid
                for blend_index, blend in enumerate(pair["blends"]):
                    index = 3 * pair_index + blend_index
                    counts["blend_cells"][index] += len(pair["cells"])
                    positive_regret = _read_pair(blend["regret"]) > 0
                    coarse_gain = _read_pair(blend["gain_over_coarse"])
                    base_gain = _read_pair(blend["gain_over_base"])
                    for count_name, witness_name, condition in (
                        ("positive_regret_beliefs", "first_positive_regret", positive_regret),
                        ("better_than_coarse_beliefs", "first_better_than_coarse", coarse_gain > 0),
                        ("equal_to_coarse_beliefs", "first_equal_to_coarse", coarse_gain == 0),
                        ("worse_than_coarse_beliefs", "first_worse_than_coarse", coarse_gain < 0),
                        ("better_than_base_beliefs", "first_better_than_base", base_gain > 0),
                        ("equal_to_base_beliefs", "first_equal_to_base", base_gain == 0),
                        ("worse_than_base_beliefs", "first_worse_than_base", base_gain < 0),
                    ):
                        counts[count_name][index] += int(condition)
                        if condition and witnesses[witness_name][index] is None:
                            witnesses[witness_name][index] = bid
        rows.append(
            {"belief_id": bid, "weight": _pair(supplied["weight"], Fraction(1)), "pairs": pairs}
        )
    counts["total_work_terms"] = sum(
        counts[name]
        for name in (
            "baseline_scoring_terms",
            "mixture_terms",
            "distance_terms",
            "blend_scoring_terms",
        )
    )
    _require(
        sum(counts["pair_cells"]) == plan["pair_cells"], "planned and retained Z pair cells differ"
    )
    _require(
        sum(counts["blend_cells"]) == plan["blend_cells"], "planned and retained blend cells differ"
    )
    for name in (
        "blend_atoms",
        "mixture_terms",
        "distance_terms",
        "blend_scoring_terms",
        "baseline_scoring_terms",
        "total_work_terms",
    ):
        _require(counts[name] == plan[name], "planned and executed work differs: " + name)
    result = {
        "input_sha256": input_hash,
        "levels": [_pair(level, Fraction(1)) for level in LEVELS],
        "retained_weights": [_pair(retained, Fraction(1)) for retained in RETAINED_WEIGHTS],
        "baseline": baseline,
        "beliefs": rows,
        "aggregate": _z_aggregate(rows, baseline),
        "witnesses": witnesses,
        "counts": counts,
    }
    _require(
        canonical(baseline) == baseline_bytes, "Z construction mutated its complete Y baseline"
    )
    return json.loads(canonical(result))
