"""Independent expected-per-outcome Brier scoring for QR-05X.

The four supplied conditional experiments are mathematical data. This core
checks their shared future marginal, not their origin, a replacement model,
empirical calibration, or a physical measurement interpretation.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F
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
MAX_BYTES = 128 * 1024 * 1024
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))


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
    pending, active, complete = [(value, False)], set(), {}

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
        current, leaving = pending.pop()
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
            continue
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native object key")
        active.add(identity)
        pending.append((current, True))
        children = current.values() if type(current) is dict else current
        pending.extend((child, False) for child in children)
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


def _bound(value):
    _require(type(value) is F, "exact rational arithmetic required")
    # Internal products/partial sums may exceed the retained component cap
    # and subsequently cancel. The contract bounds inputs and emitted values.
    return value


def _fraction(pair, positive=False):
    _require(type(pair) is list and len(pair) == 2, "fraction must be a native pair")
    numerator, denominator = pair
    _require(
        type(numerator) is int and type(denominator) is int,
        "fraction components must be native integers",
    )
    _require(0 <= numerator <= denominator and denominator > 0, "probability interval")
    _require(
        numerator.bit_length() <= MAX_BITS and denominator.bit_length() <= MAX_BITS,
        "input rational component bit cap",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must be reduced")
    value = _bound(F(numerator, denominator))
    _require(not positive or value > 0, "zero sparse probability")
    return value


def _wire(value, maximum=2):
    value = _bound(value)
    _require(
        abs(value.numerator).bit_length() <= MAX_BITS
        and value.denominator.bit_length() <= MAX_BITS,
        "retained rational component bit cap",
    )
    _require(0 <= value <= maximum, "retained rational range")
    return [value.numerator, value.denominator]


def _sum(values):
    result = F(0)
    for value in values:
        result = _bound(result + value)
    return result


def _add(target, key, value):
    value = _bound(value)
    _require(value >= 0, "negative probability contribution")
    if value:
        target[key] = _bound(target.get(key, F(0)) + value)


def _symbol(value):
    _require(
        type(value) is list and len(value) == 7,
        "opaque symbol must be a seven-component native list",
    )
    _require(
        all(type(x) is int and x >= 0 and x.bit_length() <= 64 for x in value),
        "opaque symbol component bound",
    )
    return tuple(value)


def _law_wire(law):
    return [{"value": list(value), "probability": _wire(p, 1)} for value, p in sorted(law.items())]


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "beliefs"), "X problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05x-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05x_noise_misspecification",
        "X schema/family",
    )
    supplied = problem["beliefs"]
    _require(type(supplied) is list and 1 <= len(supplied) <= MAX_BELIEFS, "belief count cap")
    beliefs, input_cells, input_atoms = [], 0, 0
    for bid, belief in enumerate(supplied):
        _fields(belief, ("belief_id", "weight", "channels"), "belief fields")
        _require(
            type(belief["belief_id"]) is int and belief["belief_id"] == bid,
            "contiguous native belief ID",
        )
        weight = _fraction(belief["weight"], positive=True)
        channels = belief["channels"]
        _require(
            type(channels) is list and len(channels) == 4, "exactly four conditional experiments"
        )
        parsed, shared = [], None
        for i, channel in enumerate(channels):
            _fields(channel, ("level", "cells"), "channel fields")
            _require(_fraction(channel["level"]) == LEVELS[i], "fixed level order")
            cells = channel["cells"]
            _require(
                type(cells) is list and 1 <= len(cells) <= MAX_CELLS_PER_CHANNEL,
                "per-channel cell cap",
            )
            input_cells += len(cells)
            _require(input_cells <= MAX_INPUT_CELLS, "total input cell cap")
            rows, marginal, previous = {}, {}, None
            for cell in cells:
                _fields(cell, ("value", "probability", "prediction"), "input cell fields")
                value = _symbol(cell["value"])
                _require(previous is None or previous < value, "report values sorted unique")
                previous = value
                mass = _fraction(cell["probability"], positive=True)
                prediction = cell["prediction"]
                _require(
                    type(prediction) is list and 1 <= len(prediction) <= MAX_ATOMS_PER_PREDICTION,
                    "prediction atom cap",
                )
                input_atoms += len(prediction)
                _require(
                    input_atoms <= MAX_INPUT_PREDICTION_ATOMS, "total input prediction atom cap"
                )
                law, last = {}, None
                for atom in prediction:
                    _fields(atom, ("value", "probability"), "future atom fields")
                    q = _symbol(atom["value"])
                    _require(last is None or last < q, "future atoms sorted unique")
                    last = q
                    p = _fraction(atom["probability"], positive=True)
                    law[q] = p
                    _add(marginal, q, _bound(mass * p))
                _require(_sum(law.values()) == 1, "future prediction already normalized")
                bayes = _sum(_bound(p * (1 - p)) for p in law.values())
                _require(0 <= bayes <= 1, "Bayes risk range")
                rows[value] = {"mass": mass, "law": law, "bayes": bayes}
            _require(
                _sum(c["mass"] for c in rows.values()) == 1, "report masses already normalized"
            )
            _require(_sum(marginal.values()) == 1, "future marginal mass")
            if shared is None:
                shared = marginal
            _require(marginal == shared, "four experiments must share their full future marginal")
            parsed.append(rows)
        beliefs.append((weight, parsed))
    _require(_sum(weight for weight, _ in beliefs) == 1, "history weights already normalized")
    pair_cells, scoring_terms = [0] * 16, 0
    for _, channels in beliefs:
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                pair_cells[4 * i + j] += len(actual)
                for value, cell in actual.items():
                    if value in assumed:
                        scoring_terms += len(cell["law"]) + len(assumed[value]["law"])
    _require(sum(pair_cells) <= MAX_PAIR_CELLS, "planned retained pair-cell cap")
    _require(scoring_terms <= MAX_SCORING_TERMS, "planned scoring support-visit cap")
    data = _canonical(problem)
    _require(len(data) <= MAX_BYTES, "canonical input byte cap")
    return (
        beliefs,
        input_cells,
        input_atoms,
        pair_cells,
        scoring_terms,
        hashlib.sha256(data).hexdigest(),
    )


def _score_supported(actual, forecast):
    """Expected loss conditional on each actual future outcome, with no assumed weighting."""
    truth, guessed = actual["law"], forecast["law"]
    forecast_square, regret, visits = F(0), F(0), 0
    for q, f in guessed.items():
        square = _bound(f * f)
        forecast_square = _bound(forecast_square + square)
        if q not in truth:
            regret = _bound(regret + square)
        visits += 1
    expected = F(0)
    for q, p in truth.items():
        f = guessed.get(q, F(0))
        # Loss at actual outcome q: its coordinate error plus every other
        # forecast coordinate's square. This is not the assumed Bayes risk.
        at_outcome = _bound(_bound((1 - f) ** 2) + forecast_square - _bound(f * f))
        _require(0 <= at_outcome <= 2, "per-outcome Brier loss range")
        expected = _bound(expected + _bound(p * at_outcome))
        regret = _bound(regret + _bound((p - f) ** 2))
        visits += 1
    equal = truth == guessed
    _require(0 <= expected <= 2 and 0 <= regret <= 2, "misspecified score/regret range")
    _require(expected == actual["bayes"] + regret, "independent expected-loss decomposition")
    _require((regret == 0) == equal, "zero conditional regret iff complete-law equality")
    return expected, regret, equal, visits


def _pair(i, j, actual, assumed):
    cells, coverage, supported_bayes, supported_forecast, supported_regret = (
        [],
        F(0),
        F(0),
        F(0),
        F(0),
    )
    bayes, equalities, terms, supported_count = F(0), [], 0, 0
    for value, cell in actual.items():
        w = cell["mass"]
        bayes = _bound(bayes + _bound(w * cell["bayes"]))
        supported = value in assumed
        forecast_risk = regret = equal = None
        if supported:
            forecast = assumed[value]
            forecast_risk, regret, equal, visits = _score_supported(cell, forecast)
            terms += visits
            supported_count += 1
            coverage = _bound(coverage + w)
            supported_bayes = _bound(supported_bayes + _bound(w * cell["bayes"]))
            supported_forecast = _bound(supported_forecast + _bound(w * forecast_risk))
            supported_regret = _bound(supported_regret + _bound(w * regret))
            equalities.append(equal)
        cells.append(
            {
                "value": list(value),
                "actual_probability": _wire(w, 1),
                "assumed_probability": _wire(assumed[value]["mass"], 1) if supported else [0, 1],
                "actual_prediction": _law_wire(cell["law"]),
                "forecast": _law_wire(assumed[value]["law"]) if supported else None,
                "bayes_risk": _wire(cell["bayes"], 1),
                "forecast_risk": _wire(forecast_risk) if supported else None,
                "regret": _wire(regret) if supported else None,
                "supported": supported,
                "predictions_equal": equal,
            }
        )
    unsupported = _sum(cell["mass"] for value, cell in actual.items() if value not in assumed)
    _require(coverage + unsupported == 1, "pair coverage mass partition")
    _require(
        supported_forecast == supported_bayes + supported_regret,
        "supported unnormalized decomposition",
    )
    _require(
        0 <= supported_bayes <= coverage
        and 0 <= supported_forecast <= 2 * coverage
        and 0 <= supported_regret <= 2 * coverage,
        "supported bounds scale with coverage",
    )
    _require(
        (supported_regret == 0) == all(equalities),
        "zero supported regret iff all defined forecasts agree",
    )
    complete = coverage == 1
    if complete:
        _require(
            supported_bayes == bayes and supported_forecast == bayes + supported_regret,
            "full-coverage decomposition",
        )
    return (
        {
            "actual_index": i,
            "assumed_index": j,
            "cells": cells,
            "bayes_risk": _wire(bayes, 1),
            "coverage": _wire(coverage, 1),
            "unsupported_mass": _wire(unsupported, 1),
            "supported_bayes_risk": _wire(supported_bayes, 1),
            "supported_forecast_risk": _wire(supported_forecast),
            "supported_regret": _wire(supported_regret),
            "forecast_risk": _wire(supported_forecast) if complete else None,
            "regret": _wire(supported_regret) if complete else None,
            "complete": complete,
            "checks": {
                "mass_partition": True,
                "supported_decomposition": True,
                "full_decomposition": True if complete else None,
                "zero_regret_iff_equal": True,
            },
        },
        terms,
        supported_count,
        all(equalities),
    )


def analyze(problem):
    """Score all actual/assumed pairs without inventing unsupported forecasts."""
    parsed, input_cells, input_atoms, planned_cells, planned_terms, input_digest = _prepare(problem)
    rows, score_terms = [], 0
    supported_count, unsupported_count = [0] * 16, [0] * 16
    complete_count, incomplete_count = [0] * 16, [0] * 16
    positive_supported, positive_full = [0] * 16, [0] * 16
    first_incomplete, first_supported, first_full = [None] * 16, [None] * 16, [None] * 16
    aggregate_fields = (
        "bayes_risk",
        "coverage",
        "unsupported_mass",
        "supported_bayes_risk",
        "supported_forecast_risk",
        "supported_regret",
    )
    sums = [{field: F(0) for field in aggregate_fields} for _ in range(16)]
    equality_flags = [[] for _ in range(16)]
    for bid, (weight, channels) in enumerate(parsed):
        pairs = []
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                index = 4 * i + j
                pair, visits, supported, equal = _pair(i, j, actual, assumed)
                pairs.append(pair)
                score_terms += visits
                supported_count[index] += supported
                unsupported_count[index] += len(actual) - supported
                complete_count[index] += int(pair["complete"])
                incomplete_count[index] += int(not pair["complete"])
                positive = pair["supported_regret"][0] > 0
                positive_supported[index] += int(positive)
                positive_full[index] += int(positive and pair["complete"])
                if not pair["complete"] and first_incomplete[index] is None:
                    first_incomplete[index] = bid
                if positive and first_supported[index] is None:
                    first_supported[index] = bid
                if positive and pair["complete"] and first_full[index] is None:
                    first_full[index] = bid
                for field in aggregate_fields:
                    value = F(*pair[field])
                    sums[index][field] = _bound(sums[index][field] + _bound(weight * value))
                equality_flags[index].append(equal)
        rows.append({"belief_id": bid, "weight": _wire(weight, 1), "pairs": pairs})
    _require(score_terms == planned_terms, "planned/executed scoring support visits")
    pair_counts = [supported_count[k] + unsupported_count[k] for k in range(16)]
    _require(pair_counts == planned_cells, "planned/retained pair-cell counts")
    aggregate = []
    for index, values in enumerate(sums):
        coverage = values["coverage"]
        complete = incomplete_count[index] == 0
        _require((coverage == 1) == complete, "positive-history aggregate coverage")
        _require(coverage + values["unsupported_mass"] == 1, "aggregate coverage partition")
        _require(
            values["supported_forecast_risk"]
            == values["supported_bayes_risk"] + values["supported_regret"],
            "aggregate supported decomposition",
        )
        _require(
            0 <= values["supported_bayes_risk"] <= coverage
            and 0 <= values["supported_forecast_risk"] <= 2 * coverage
            and 0 <= values["supported_regret"] <= 2 * coverage,
            "aggregate coverage-scaled score bounds",
        )
        _require(
            (values["supported_regret"] == 0) == all(equality_flags[index]),
            "aggregate supported zero regret law equivalence",
        )
        if complete:
            _require(
                values["supported_bayes_risk"] == values["bayes_risk"]
                and values["supported_forecast_risk"]
                == values["bayes_risk"] + values["supported_regret"],
                "aggregate full decomposition",
            )
        aggregate.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                **{
                    field: _wire(
                        value,
                        1
                        if field
                        in ("bayes_risk", "coverage", "unsupported_mass", "supported_bayes_risk")
                        else 2,
                    )
                    for field, value in values.items()
                },
                "forecast_risk": _wire(values["supported_forecast_risk"]) if complete else None,
                "regret": _wire(values["supported_regret"]) if complete else None,
                "complete": complete,
                "checks": {
                    "mass_partition": True,
                    "supported_decomposition": True,
                    "full_decomposition": True if complete else None,
                    "zero_regret_iff_equal": True,
                },
                "complete_beliefs": complete_count[index],
                "incomplete_beliefs": incomplete_count[index],
            }
        )
    result = {
        "input_sha256": input_digest,
        "levels": [_wire(level, 1) for level in LEVELS],
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": {
            "first_incomplete": first_incomplete,
            "first_positive_supported_regret": first_supported,
            "first_positive_full_regret": first_full,
        },
        "counts": {
            "beliefs": len(rows),
            "input_cells": input_cells,
            "input_prediction_atoms": input_atoms,
            "pair_cells": pair_counts,
            "supported_pair_cells": supported_count,
            "unsupported_pair_cells": unsupported_count,
            "scoring_terms": score_terms,
            "complete_beliefs": complete_count,
            "incomplete_beliefs": incomplete_count,
            "positive_supported_regret_beliefs": positive_supported,
            "positive_full_regret_beliefs": positive_full,
        },
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "canonical output byte cap")
    return json.loads(encoded)
