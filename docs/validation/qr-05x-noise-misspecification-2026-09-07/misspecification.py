"""QR-05X exact actual-law scoring of supplied conditional experiments.

This module authenticates no channel origin. It accepts normalized exact
report/future laws, checks their shared future marginal, and scores all fixed
actual/assumed pairs with explicit unsupported-report accounting.
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
MAX_SCORING_TERMS = 16777216
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


def _symbol(value):
    _require(type(value) is list and len(value) == 7, "symbol must have seven native integers")
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


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "beliefs"))
    _require(
        problem["schema_version"] == "det8-qr05x-problem-v1"
        and problem["family"] == "qr05x_noise_misspecification",
        "unknown misspecification scoring schema",
    )
    supplied = problem["beliefs"]
    _require(
        type(supplied) is list and 1 <= len(supplied) <= MAX_BELIEFS,
        "belief count outside cap",
    )
    beliefs, input_cells, input_atoms = [], 0, 0
    weights = []
    for bid, row in enumerate(supplied):
        _fields(row, ("belief_id", "weight", "channels"))
        _integer(row["belief_id"], bid, bid)
        weight = _fraction(row["weight"], positive=True)
        weights.append(weight)
        _require(
            type(row["channels"]) is list and len(row["channels"]) == 4,
            "exactly four conditional experiments required",
        )
        channels, common_future = [], None
        for index, channel in enumerate(row["channels"]):
            _fields(channel, ("level", "cells"))
            _require(_fraction(channel["level"]) == LEVELS[index], "fixed level order differs")
            atoms = channel["cells"]
            _require(
                type(atoms) is list and 1 <= len(atoms) <= MAX_CELLS_PER_CHANNEL,
                "report cell count outside cap",
            )
            cells, previous, marginal = {}, None, {}
            input_cells += len(atoms)
            _require(input_cells <= MAX_INPUT_CELLS, "total input cell cap exceeded")
            for atom in atoms:
                _fields(atom, ("value", "probability", "prediction"))
                symbol = _symbol(atom["value"])
                _require(
                    previous is None or previous < symbol, "report values must be sorted unique"
                )
                previous = symbol
                probability = _fraction(atom["probability"], positive=True)
                law = _prediction(atom["prediction"])
                input_atoms += len(law)
                _require(
                    input_atoms <= MAX_INPUT_PREDICTION_ATOMS, "input prediction atom cap exceeded"
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
        beliefs.append({"belief_id": bid, "weight": weight, "channels": channels})
    _require(sum(weights, Fraction(0)) == 1, "history weights must have exact unit mass")
    # Plan all retained cells, including unsupported reports, and both sparse
    # support visits for every supported comparison before the score loops.
    planned_cells = input_cells * 4
    _require(planned_cells <= MAX_PAIR_CELLS, "planned pair cell cap exceeded")
    planned_terms = 0
    for row in beliefs:
        for actual in row["channels"]:
            for assumed in row["channels"]:
                for value, cell in actual.items():
                    forecast = assumed.get(value)
                    if forecast is not None:
                        planned_terms += len(cell["prediction"]) + len(forecast["prediction"])
                        _require(
                            planned_terms <= MAX_SCORING_TERMS, "planned scoring term cap exceeded"
                        )
    return beliefs, input_cells, input_atoms, planned_cells, planned_terms


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


def _pair_result(actual_index, assumed_index, actual, assumed):
    cells, coverage, unsupported, bayes = [], Fraction(0), Fraction(0), Fraction(0)
    supported_bayes, supported_risk, supported_regret = Fraction(0), Fraction(0), Fraction(0)
    equalities, terms = [], 0
    for value, cell in actual.items():
        probability, law = cell["probability"], cell["prediction"]
        bayes += probability * cell["bayes_risk"]
        forecast = assumed.get(value)
        if forecast is None:
            unsupported += probability
            cells.append(
                {
                    "value": list(value),
                    "actual_probability": _pair(probability, Fraction(1)),
                    "assumed_probability": [0, 1],
                    "actual_prediction": _law_wire(law),
                    "forecast": None,
                    "bayes_risk": _pair(cell["bayes_risk"], Fraction(1)),
                    "forecast_risk": None,
                    "regret": None,
                    "supported": False,
                    "predictions_equal": None,
                }
            )
            continue
        current_bayes, scored, regret, equal, visits = _score(law, forecast["prediction"])
        _require(current_bayes == cell["bayes_risk"], "conditional Bayes risk changed")
        terms += visits
        coverage += probability
        supported_bayes += probability * current_bayes
        supported_risk += probability * scored
        supported_regret += probability * regret
        equalities.append(equal)
        cells.append(
            {
                "value": list(value),
                "actual_probability": _pair(probability, Fraction(1)),
                "assumed_probability": _pair(forecast["probability"], Fraction(1)),
                "actual_prediction": _law_wire(law),
                "forecast": _law_wire(forecast["prediction"]),
                "bayes_risk": _pair(current_bayes, Fraction(1)),
                "forecast_risk": _pair(scored),
                "regret": _pair(regret),
                "supported": True,
                "predictions_equal": equal,
            }
        )
    _require(coverage + unsupported == 1, "supported and unsupported masses do not partition one")
    _require(
        supported_bayes <= coverage
        and supported_risk <= 2 * coverage
        and supported_regret <= 2 * coverage,
        "supported contributions exceed coverage-scaled bounds",
    )
    _require(
        supported_risk == supported_bayes + supported_regret, "supported decomposition differs"
    )
    _require(
        (supported_regret == 0) == all(equalities), "supported zero-regret characterization differs"
    )
    complete = coverage == 1
    if complete:
        _require(supported_bayes == bayes, "complete supported Bayes risk differs")
        _require(supported_risk == bayes + supported_regret, "full decomposition differs")
    if actual_index == assumed_index:
        _require(complete and supported_regret == 0, "diagonal scoring control failed")
    result = {
        "actual_index": actual_index,
        "assumed_index": assumed_index,
        "cells": cells,
        "bayes_risk": _pair(bayes, Fraction(1)),
        "coverage": _pair(coverage, Fraction(1)),
        "unsupported_mass": _pair(unsupported, Fraction(1)),
        "supported_bayes_risk": _pair(supported_bayes, coverage),
        "supported_forecast_risk": _pair(supported_risk, 2 * coverage),
        "supported_regret": _pair(supported_regret, 2 * coverage),
        "forecast_risk": _pair(supported_risk) if complete else None,
        "regret": _pair(supported_regret) if complete else None,
        "complete": complete,
        "checks": {
            "mass_partition": True,
            "supported_decomposition": True,
            "full_decomposition": True if complete else None,
            "zero_regret_iff_equal": True,
        },
    }
    return result, terms


def _read_pair(value):
    return Fraction(*value)


def _aggregate(rows):
    weights = [_read_pair(row["weight"]) for row in rows]
    pairs = []
    for index in range(16):
        parts = [row["pairs"][index] for row in rows]

        def weighted(name, parts=parts):
            return sum(
                (
                    weight * _read_pair(part[name])
                    for weight, part in zip(weights, parts, strict=True)
                ),
                Fraction(0),
            )

        coverage, unsupported = weighted("coverage"), weighted("unsupported_mass")
        bayes, supported_bayes = weighted("bayes_risk"), weighted("supported_bayes_risk")
        scored, regret = weighted("supported_forecast_risk"), weighted("supported_regret")
        complete_count = sum(part["complete"] for part in parts)
        complete = complete_count == len(rows)
        _require(
            complete == (coverage == 1), "case coverage disagrees with positive history weights"
        )
        _require(coverage + unsupported == 1, "aggregate mass partition differs")
        _require(
            supported_bayes <= coverage and scored <= 2 * coverage and regret <= 2 * coverage,
            "aggregate supported bounds differ",
        )
        _require(scored == supported_bayes + regret, "aggregate supported decomposition differs")
        equalities = [
            cell["predictions_equal"]
            for part in parts
            for cell in part["cells"]
            if cell["supported"]
        ]
        _require(
            (regret == 0) == all(equalities),
            "aggregate supported equality characterization differs",
        )
        if complete:
            _require(
                supported_bayes == bayes and scored == bayes + regret,
                "aggregate full decomposition differs",
            )
        pairs.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "bayes_risk": _pair(bayes, Fraction(1)),
                "coverage": _pair(coverage, Fraction(1)),
                "unsupported_mass": _pair(unsupported, Fraction(1)),
                "supported_bayes_risk": _pair(supported_bayes, coverage),
                "supported_forecast_risk": _pair(scored, 2 * coverage),
                "supported_regret": _pair(regret, 2 * coverage),
                "forecast_risk": _pair(scored) if complete else None,
                "regret": _pair(regret) if complete else None,
                "complete": complete,
                "checks": {
                    "mass_partition": True,
                    "supported_decomposition": True,
                    "full_decomposition": True if complete else None,
                    "zero_regret_iff_equal": True,
                },
                "complete_beliefs": complete_count,
                "incomplete_beliefs": len(rows) - complete_count,
            }
        )
    return {"total_weight": [1, 1], "pairs": pairs}


def analyze(problem):
    beliefs, input_cells, input_atoms, planned_cells, planned_terms = _prepare(problem)
    input_hash = hashlib.sha256(canonical(problem)).hexdigest()
    rows, terms = [], 0
    counts = {
        "beliefs": len(beliefs),
        "input_cells": input_cells,
        "input_prediction_atoms": input_atoms,
        "pair_cells": [0] * 16,
        "supported_pair_cells": [0] * 16,
        "unsupported_pair_cells": [0] * 16,
        "scoring_terms": 0,
        "complete_beliefs": [0] * 16,
        "incomplete_beliefs": [0] * 16,
        "positive_supported_regret_beliefs": [0] * 16,
        "positive_full_regret_beliefs": [0] * 16,
    }
    witnesses = {
        "first_incomplete": [None] * 16,
        "first_positive_supported_regret": [None] * 16,
        "first_positive_full_regret": [None] * 16,
    }
    for belief in beliefs:
        bid, pairs = belief["belief_id"], []
        for i, actual in enumerate(belief["channels"]):
            for j, assumed in enumerate(belief["channels"]):
                pair, visits = _pair_result(i, j, actual, assumed)
                terms += visits
                index = 4 * i + j
                pairs.append(pair)
                supported = sum(cell["supported"] for cell in pair["cells"])
                counts["pair_cells"][index] += len(pair["cells"])
                counts["supported_pair_cells"][index] += supported
                counts["unsupported_pair_cells"][index] += len(pair["cells"]) - supported
                counts["complete_beliefs"][index] += int(pair["complete"])
                counts["incomplete_beliefs"][index] += int(not pair["complete"])
                positive_supported = _read_pair(pair["supported_regret"]) > 0
                positive_full = pair["complete"] and _read_pair(pair["regret"]) > 0
                counts["positive_supported_regret_beliefs"][index] += int(positive_supported)
                counts["positive_full_regret_beliefs"][index] += int(positive_full)
                for field, condition in (
                    ("first_incomplete", not pair["complete"]),
                    ("first_positive_supported_regret", positive_supported),
                    ("first_positive_full_regret", positive_full),
                ):
                    if condition and witnesses[field][index] is None:
                        witnesses[field][index] = bid
        rows.append(
            {"belief_id": bid, "weight": _pair(belief["weight"], Fraction(1)), "pairs": pairs}
        )
    _require(sum(counts["pair_cells"]) == planned_cells, "planned and retained pair cells differ")
    _require(terms == planned_terms, "planned and executed support visits differ")
    counts["scoring_terms"] = terms
    result = {
        "input_sha256": input_hash,
        "levels": [_pair(level, Fraction(1)) for level in LEVELS],
        "beliefs": rows,
        "aggregate": _aggregate(rows),
        "witnesses": witnesses,
        "counts": counts,
    }
    # A fresh native JSON value detaches every repeated output occurrence from
    # inputs, sibling output cells, and all earlier or later analyze calls.
    return json.loads(canonical(result))
