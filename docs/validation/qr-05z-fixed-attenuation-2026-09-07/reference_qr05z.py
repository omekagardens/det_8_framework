"""Independent expected-loss reference for fixed attenuation, QR-05Z.

The Y validator and baseline scorer below are statically carried own lineage.

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
MAX_SCORING_TERMS = 33554432
MAX_FALLBACKS_PER_BELIEF = 16384
MAX_INPUT_FALLBACKS = 32768
MAX_INPUT_FALLBACK_ATOMS = 2097152
MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 8388608
MAX_BYTES = 128 * 1024 * 1024
MAX_BLEND_CELLS = 393216
MAX_BLEND_ATOMS = 8388608
MAX_TOTAL_WORK_TERMS = 167772160
RETAINED_WEIGHTS = (F(0), F(1, 2), F(1))
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


def _signed_wire(value):
    value = _bound(value)
    _require(
        abs(value.numerator).bit_length() <= MAX_BITS
        and value.denominator.bit_length() <= MAX_BITS,
        "retained signed component bit cap",
    )
    _require(-2 <= value <= 2, "signed gain range")
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


def _symbol(value, length=7):
    _require(
        type(value) is list and len(value) == length,
        "opaque symbol native list shape",
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
    _fields(problem, ("schema_version", "family", "beliefs"), "Y problem fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05y-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05y_explicit_fallback",
        "Y schema/family",
    )
    supplied = problem["beliefs"]
    _require(type(supplied) is list and 1 <= len(supplied) <= MAX_BELIEFS, "belief count cap")
    beliefs, input_cells, input_atoms = [], 0, 0
    input_fallbacks = input_fallback_atoms = 0
    for bid, belief in enumerate(supplied):
        _fields(belief, ("belief_id", "weight", "channels", "fallbacks"), "belief fields")
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
        fallback_rows = belief["fallbacks"]
        _require(
            type(fallback_rows) is list and 1 <= len(fallback_rows) <= MAX_FALLBACKS_PER_BELIEF,
            "per-belief fallback count cap",
        )
        input_fallbacks += len(fallback_rows)
        _require(input_fallbacks <= MAX_INPUT_FALLBACKS, "total input fallback cap")
        fallbacks, last_prefix = {}, None
        for fallback in fallback_rows:
            _fields(fallback, ("value", "prediction"), "fallback fields")
            prefix = _symbol(fallback["value"], 5)
            _require(last_prefix is None or last_prefix < prefix, "fallback prefixes sorted unique")
            last_prefix = prefix
            prediction = fallback["prediction"]
            _require(
                type(prediction) is list and 1 <= len(prediction) <= MAX_ATOMS_PER_PREDICTION,
                "fallback prediction atom cap",
            )
            input_fallback_atoms += len(prediction)
            _require(
                input_fallback_atoms <= MAX_INPUT_FALLBACK_ATOMS,
                "total fallback prediction atom cap",
            )
            law, previous = {}, None
            for atom in prediction:
                _fields(atom, ("value", "probability"), "fallback future atom fields")
                q = _symbol(atom["value"])
                _require(previous is None or previous < q, "fallback future atoms sorted unique")
                previous = q
                law[q] = _fraction(atom["probability"], positive=True)
            _require(_sum(law.values()) == 1, "fallback prediction already normalized")
            fallbacks[prefix] = {"law": law}
        prefixes = {value[:5] for channel in parsed for value in channel}
        _require(
            set(fallbacks) == prefixes,
            "fallback keys must exactly cover the full report-prefix union",
        )
        beliefs.append((weight, parsed, fallbacks))
    _require(_sum(weight for weight, _, _ in beliefs) == 1, "history weights already normalized")
    pair_cells, completed_terms, coarse_terms = [0] * 16, 0, 0
    for _, channels, fallbacks in beliefs:
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                pair_cells[4 * i + j] += len(actual)
                for value, cell in actual.items():
                    coarse = fallbacks[value[:5]]
                    chosen = assumed.get(value, coarse)
                    completed_terms += len(cell["law"]) + len(chosen["law"])
                    coarse_terms += len(cell["law"]) + len(coarse["law"])
    _require(sum(pair_cells) <= MAX_PAIR_CELLS, "planned retained pair-cell cap")
    _require(
        completed_terms + coarse_terms <= MAX_SCORING_TERMS,
        "planned total scoring support-visit cap",
    )
    data = _canonical(problem)
    _require(len(data) <= MAX_BYTES, "canonical input byte cap")
    return (
        beliefs,
        input_cells,
        input_atoms,
        input_fallbacks,
        input_fallback_atoms,
        pair_cells,
        completed_terms,
        coarse_terms,
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
X_NUMERIC = (
    "coverage",
    "unsupported_mass",
    "bayes_risk",
    "supported_bayes_risk",
    "supported_forecast_risk",
    "supported_regret",
)
Y_NUMERIC = (
    "fallback_bayes_risk",
    "fallback_forecast_risk",
    "fallback_regret",
    "completed_forecast_risk",
    "completed_regret",
    "coarse_forecast_risk",
    "coarse_regret",
    "gain_over_coarse",
)


def _check_totals(x, y, completed_equal, coarse_equal, supported_gain):
    _require(x["coverage"] + x["unsupported_mass"] == 1, "policy branch mass partition")
    _require(
        x["supported_forecast_risk"] == x["supported_bayes_risk"] + x["supported_regret"],
        "original supported decomposition",
    )
    _require(
        y["fallback_forecast_risk"] == y["fallback_bayes_risk"] + y["fallback_regret"],
        "fallback decomposition",
    )
    _require(
        x["bayes_risk"] == x["supported_bayes_risk"] + y["fallback_bayes_risk"],
        "Bayes branch split",
    )
    _require(
        y["completed_forecast_risk"]
        == x["supported_forecast_risk"] + y["fallback_forecast_risk"]
        == x["bayes_risk"] + y["completed_regret"],
        "completed risk decomposition",
    )
    _require(
        y["completed_regret"] == x["supported_regret"] + y["fallback_regret"],
        "completed regret split",
    )
    _require(
        y["coarse_forecast_risk"] == x["bayes_risk"] + y["coarse_regret"],
        "coarse risk decomposition",
    )
    _require(
        y["gain_over_coarse"]
        == y["coarse_forecast_risk"] - y["completed_forecast_risk"]
        == y["coarse_regret"] - y["completed_regret"]
        == supported_gain,
        "signed gain only from supported cells",
    )
    _require(abs(y["gain_over_coarse"]) <= 2 * x["coverage"], "signed gain coverage bound")
    for branch, mass in (("supported", x["coverage"]), ("fallback", x["unsupported_mass"])):
        table = x if branch == "supported" else y
        _require(
            0 <= table[branch + "_bayes_risk"] <= mass
            and 0 <= table[branch + "_forecast_risk"] <= 2 * mass
            and 0 <= table[branch + "_regret"] <= 2 * mass,
            "branch contributions keep original mass",
        )
    _require(
        (y["completed_regret"] == 0) == completed_equal
        and (y["coarse_regret"] == 0) == coarse_equal,
        "zero completed/coarse regret iff complete-law equality",
    )


def _x_wire(x):
    complete = x["coverage"] == 1
    if complete:
        _require(
            x["supported_bayes_risk"] == x["bayes_risk"], "complete original Bayes contribution"
        )
    return {
        **{
            key: _wire(value, 2 if key in ("supported_forecast_risk", "supported_regret") else 1)
            for key, value in x.items()
        },
        "forecast_risk": _wire(x["supported_forecast_risk"]) if complete else None,
        "regret": _wire(x["supported_regret"]) if complete else None,
        "complete": complete,
    }


def _y_wire(y):
    return {
        key: _signed_wire(value)
        if key == "gain_over_coarse"
        else _wire(value, 1 if key == "fallback_bayes_risk" else 2)
        for key, value in y.items()
    }


def _pair(i, j, actual, assumed, fallbacks):
    x = {key: F(0) for key in X_NUMERIC}
    y = {key: F(0) for key in Y_NUMERIC}
    cells, completed_flags, coarse_flags = [], [], []
    completed_terms = coarse_terms = supported_count = 0
    supported_gain = F(0)
    for value, cell in actual.items():
        mass, bayes = cell["mass"], cell["bayes"]
        supported = value in assumed
        coarse = fallbacks[value[:5]]
        chosen = assumed[value] if supported else coarse
        # Both full comparisons are evaluated, even on fallback-used cells.
        loss, regret, equal, visits = _score_supported(cell, chosen)
        coarse_loss, coarse_regret, coarse_equal, coarse_visits = _score_supported(cell, coarse)
        completed_terms += visits
        coarse_terms += coarse_visits
        completed_flags.append(equal)
        coarse_flags.append(coarse_equal)
        gain = coarse_loss - loss
        _require(gain == coarse_regret - regret, "conditional gain identity")
        x["bayes_risk"] += mass * bayes
        if supported:
            supported_count += 1
            x["coverage"] += mass
            x["supported_bayes_risk"] += mass * bayes
            x["supported_forecast_risk"] += mass * loss
            x["supported_regret"] += mass * regret
            supported_gain += mass * gain
            _require(chosen["law"] == assumed[value]["law"], "original supported forecast retained")
        else:
            x["unsupported_mass"] += mass
            y["fallback_bayes_risk"] += mass * bayes
            y["fallback_forecast_risk"] += mass * loss
            y["fallback_regret"] += mass * regret
            _require(
                chosen["law"] == coarse["law"] and gain == 0,
                "fallback branch equals coarse forecast",
            )
        y["completed_forecast_risk"] += mass * loss
        y["completed_regret"] += mass * regret
        y["coarse_forecast_risk"] += mass * coarse_loss
        y["coarse_regret"] += mass * coarse_regret
        y["gain_over_coarse"] += mass * gain
        cells.append(
            {
                "value": list(value),
                "actual_probability": _wire(mass, 1),
                "assumed_probability": _wire(assumed[value]["mass"], 1) if supported else [0, 1],
                "actual_prediction": _law_wire(cell["law"]),
                "assumed_forecast": _law_wire(assumed[value]["law"]) if supported else None,
                "coarse_forecast": _law_wire(coarse["law"]),
                "forecast": _law_wire(chosen["law"]),
                "supported": supported,
                "used_fallback": not supported,
                "bayes_risk": _wire(bayes, 1),
                "forecast_risk": _wire(loss),
                "regret": _wire(regret),
                "coarse_risk": _wire(coarse_loss),
                "coarse_regret": _wire(coarse_regret),
                "gain_over_coarse": _signed_wire(gain),
                "predictions_equal": equal,
                "coarse_predictions_equal": coarse_equal,
            }
        )
    completed_equal, coarse_equal = all(completed_flags), all(coarse_flags)
    _check_totals(x, y, completed_equal, coarse_equal, supported_gain)
    return (
        {
            "actual_index": i,
            "assumed_index": j,
            "cells": cells,
            "x_scores": _x_wire(x),
            **_y_wire(y),
            "checks": dict.fromkeys(CHECKS, True),
        },
        completed_terms,
        coarse_terms,
        supported_count,
        completed_equal,
        coarse_equal,
        supported_gain,
    )


def _analyze_y(problem):
    """Apply the declared total rule without repairing the original X scores."""
    (
        parsed,
        input_cells,
        input_atoms,
        input_fallbacks,
        input_fallback_atoms,
        planned_cells,
        planned_completed,
        planned_coarse,
        input_digest,
    ) = _prepare(problem)
    rows = []
    completed_terms = coarse_terms = 0
    x_sums = [{key: F(0) for key in X_NUMERIC} for _ in range(16)]
    y_sums = [{key: F(0) for key in Y_NUMERIC} for _ in range(16)]
    supported_gains = [F(0)] * 16
    complete_flags, coarse_flags = [[] for _ in range(16)], [[] for _ in range(16)]
    count_names = (
        "pair_cells",
        "supported_pair_cells",
        "fallback_pair_cells",
        "complete_before_beliefs",
        "incomplete_before_beliefs",
        "positive_fallback_regret_beliefs",
        "positive_completed_regret_beliefs",
        "better_than_coarse_beliefs",
        "equal_to_coarse_beliefs",
        "worse_than_coarse_beliefs",
    )
    counts = {name: [0] * 16 for name in count_names}
    witness_names = (
        "first_fallback",
        "first_positive_fallback_regret",
        "first_positive_completed_regret",
        "first_better_than_coarse",
        "first_equal_to_coarse",
        "first_worse_than_coarse",
    )
    witnesses = {name: [None] * 16 for name in witness_names}
    for bid, (weight, channels, fallbacks) in enumerate(parsed):
        pairs = []
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                index = 4 * i + j
                pair, used, coarse_used, supported, eq_complete, eq_coarse, supported_gain = _pair(
                    i, j, actual, assumed, fallbacks
                )
                pairs.append(pair)
                completed_terms += used
                coarse_terms += coarse_used
                complete_flags[index].append(eq_complete)
                coarse_flags[index].append(eq_coarse)
                supported_gains[index] += weight * supported_gain
                for key in X_NUMERIC:
                    x_sums[index][key] += weight * F(*pair["x_scores"][key])
                for key in Y_NUMERIC:
                    y_sums[index][key] += weight * F(*pair[key])
                counts["pair_cells"][index] += len(actual)
                counts["supported_pair_cells"][index] += supported
                counts["fallback_pair_cells"][index] += len(actual) - supported
                complete_before = pair["x_scores"]["complete"]
                counts["complete_before_beliefs"][index] += int(complete_before)
                counts["incomplete_before_beliefs"][index] += int(not complete_before)
                gain = F(*pair["gain_over_coarse"])
                conditions = (
                    pair["x_scores"]["unsupported_mass"][0] > 0,
                    pair["fallback_regret"][0] > 0,
                    pair["completed_regret"][0] > 0,
                    gain > 0,
                    gain == 0,
                    gain < 0,
                )
                for name, condition in zip(witness_names, conditions, strict=True):
                    if condition and witnesses[name][index] is None:
                        witnesses[name][index] = bid
                for name, condition in zip(
                    (
                        "positive_fallback_regret_beliefs",
                        "positive_completed_regret_beliefs",
                        "better_than_coarse_beliefs",
                        "equal_to_coarse_beliefs",
                        "worse_than_coarse_beliefs",
                    ),
                    conditions[1:],
                    strict=True,
                ):
                    counts[name][index] += int(condition)
        rows.append({"belief_id": bid, "weight": _wire(weight, 1), "pairs": pairs})
    _require(counts["pair_cells"] == planned_cells, "planned/retained pair-cell counts")
    _require(
        completed_terms == planned_completed and coarse_terms == planned_coarse,
        "planned/executed two-comparison support visits",
    )
    aggregate = []
    for index, (x, y) in enumerate(zip(x_sums, y_sums, strict=True)):
        _check_totals(
            x, y, all(complete_flags[index]), all(coarse_flags[index]), supported_gains[index]
        )
        _require(
            (x["coverage"] == 1) == (counts["incomplete_before_beliefs"][index] == 0),
            "positive-history original completeness",
        )
        aggregate.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "x_scores": _x_wire(x),
                **_y_wire(y),
                "checks": dict.fromkeys(CHECKS, True),
                "complete_before_beliefs": counts["complete_before_beliefs"][index],
                "incomplete_before_beliefs": counts["incomplete_before_beliefs"][index],
            }
        )
    result = {
        "input_sha256": input_digest,
        "levels": [_wire(level, 1) for level in LEVELS],
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": witnesses,
        "counts": {
            "beliefs": len(rows),
            "input_cells": input_cells,
            "input_prediction_atoms": input_atoms,
            "input_fallbacks": input_fallbacks,
            "input_fallback_atoms": input_fallback_atoms,
            "completed_scoring_terms": completed_terms,
            "coarse_scoring_terms": coarse_terms,
            **counts,
        },
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "canonical output byte cap")
    return json.loads(encoded)


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
Z_SCORES = ("forecast_risk", "regret", "gain_over_coarse", "gain_over_base")


def _plan_z(prepared):
    parsed = prepared[0]
    pair_cells, blend_cells = [0] * 16, [0] * 48
    atoms = mixture_terms = distance_terms = blend_scoring = 0
    baseline_scoring = prepared[6] + prepared[7]
    for _, channels, fallbacks in parsed:
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                index = 4 * i + j
                pair_cells[index] += len(actual)
                for value, cell in actual.items():
                    coarse = fallbacks[value[:5]]["law"]
                    chosen = assumed.get(value, fallbacks[value[:5]])["law"]
                    source_visits = len(chosen) + len(coarse)
                    distance_terms += source_visits
                    sizes = (len(coarse), len(chosen.keys() | coarse.keys()), len(chosen))
                    for k, size in enumerate(sizes):
                        blend_cells[3 * index + k] += 1
                        atoms += size
                        mixture_terms += source_visits
                        blend_scoring += len(cell["law"]) + size
    total = baseline_scoring + mixture_terms + distance_terms + blend_scoring
    _require(sum(blend_cells) <= MAX_BLEND_CELLS, "planned blend cell cap")
    _require(atoms <= MAX_BLEND_ATOMS, "planned retained blend atom cap")
    _require(total <= MAX_TOTAL_WORK_TERMS, "planned combined Y/Z work cap")
    return {
        "pair_cells": pair_cells,
        "blend_cells": blend_cells,
        "blend_atoms": atoms,
        "mixture_terms": mixture_terms,
        "distance_terms": distance_terms,
        "blend_scoring_terms": blend_scoring,
        "baseline_scoring_terms": baseline_scoring,
        "total_work_terms": total,
    }


def _distance(chosen, coarse):
    # One visit of each source support, with missing sparse atoms equal zero.
    value, visits = F(0), 0
    for q, f in chosen.items():
        value += (f - coarse.get(q, F(0))) ** 2
        visits += 1
    for q, g in coarse.items():
        if q not in chosen:
            value += g * g
        visits += 1
    _require(0 <= value <= 2, "endpoint forecast distance range")
    _require((value == 0) == (chosen == coarse), "zero endpoint distance iff complete laws equal")
    return value, visits


def _mixed_law(chosen, coarse, retained):
    law, visits = {}, 0
    # Both source supports are traversed at every weight, including endpoints.
    for q, f in chosen.items():
        _add(law, q, retained * f)
        visits += 1
    for q, g in coarse.items():
        _add(law, q, (1 - retained) * g)
        visits += 1
    _require(_sum(law.values()) == 1, "mixed forecast normalized")
    _require(
        all(value > 0 for value in law.values()), "mixed forecast contains only positive atoms"
    )
    if retained == 0:
        _require(law == coarse, "zero retention coarse endpoint law")
    elif retained == 1:
        _require(law == chosen, "full retention Y endpoint law")
    else:
        _require(set(law) == chosen.keys() | coarse.keys(), "positive midpoint union support")
    return law, visits


def _blend_wire(retained, score):
    return {
        "retained_weight": _wire(retained, 1),
        **{
            name: _signed_wire(score[name]) if name.startswith("gain_") else _wire(score[name])
            for name in Z_SCORES
        },
    }


def _check_quadratic(
    retained,
    score,
    distance,
    coarse_risk,
    base_risk,
    coarse_regret,
    base_regret,
    bayes_risk,
    predictions_equal,
):
    average = (1 - retained) * coarse_risk + retained * base_risk
    gap = retained * (1 - retained) * distance
    base_gain = coarse_risk - base_risk
    _require(score["forecast_risk"] == bayes_risk + score["regret"], "blend score decomposition")
    _require(score["forecast_risk"] == average - gap, "exact quadratic attenuation risk identity")
    _require(
        score["gain_over_coarse"]
        == coarse_risk - score["forecast_risk"]
        == retained * base_gain + gap,
        "exact quadratic attenuation gain",
    )
    _require(
        score["gain_over_base"]
        == base_risk - score["forecast_risk"]
        == score["gain_over_coarse"] - base_gain,
        "gain relative to completed Y",
    )
    _require(score["forecast_risk"] <= average, "Jensen endpoint-average upper bound")
    _require(
        (score["regret"] == 0) == predictions_equal,
        "zero mixed regret iff all complete actual laws equal",
    )
    if retained == 0:
        _require(
            score["forecast_risk"] == coarse_risk
            and score["regret"] == coarse_regret
            and score["gain_over_coarse"] == 0,
            "zero-retention endpoint scores",
        )
    if retained == 1:
        _require(
            score["forecast_risk"] == base_risk
            and score["regret"] == base_regret
            and score["gain_over_base"] == 0,
            "full-retention endpoint scores",
        )


def _z_pair(i, j, actual, assumed, fallbacks, baseline_pair):
    cells, flags = [], [[], [], []]
    scores = [{name: F(0) for name in Z_SCORES} for _ in range(3)]
    forecast_distance = F(0)
    work = {"blend_atoms": 0, "mixture_terms": 0, "distance_terms": 0, "blend_scoring_terms": 0}
    _require(len(actual) == len(baseline_pair["cells"]), "same Y/Z report cell count")
    for (value, truth), base_cell in zip(actual.items(), baseline_pair["cells"], strict=True):
        _require(list(value) == base_cell["value"], "same Y/Z report order")
        coarse = fallbacks[value[:5]]["law"]
        chosen = assumed.get(value, fallbacks[value[:5]])["law"]
        distance, visits = _distance(chosen, coarse)
        work["distance_terms"] += visits
        forecast_distance += truth["mass"] * distance
        base_risk, coarse_risk = F(*base_cell["forecast_risk"]), F(*base_cell["coarse_risk"])
        base_regret, coarse_regret = F(*base_cell["regret"]), F(*base_cell["coarse_regret"])
        blend_rows = []
        for k, retained in enumerate(RETAINED_WEIGHTS):
            law, construction_visits = _mixed_law(chosen, coarse, retained)
            work["mixture_terms"] += construction_visits
            work["blend_atoms"] += len(law)
            risk, regret, equal, scoring_visits = _score_supported(truth, {"law": law})
            work["blend_scoring_terms"] += scoring_visits
            score = {
                "forecast_risk": risk,
                "regret": regret,
                "gain_over_coarse": coarse_risk - risk,
                "gain_over_base": base_risk - risk,
            }
            _check_quadratic(
                retained,
                score,
                distance,
                coarse_risk,
                base_risk,
                coarse_regret,
                base_regret,
                truth["bayes"],
                equal,
            )
            if value not in assumed:
                _require(
                    chosen == coarse
                    and distance == 0
                    and law == chosen
                    and risk == base_risk
                    and regret == base_regret,
                    "unchanged fallback law and scores at every retention",
                )
            flags[k].append(equal)
            for name in Z_SCORES:
                scores[k][name] += truth["mass"] * score[name]
            blend_rows.append(
                {
                    **_blend_wire(retained, score),
                    "forecast": _law_wire(law),
                    "predictions_equal": equal,
                }
            )
        cells.append(
            {"value": list(value), "forecast_distance": _wire(distance), "blends": blend_rows}
        )
    _require(
        _sum(cell["mass"] for cell in actual.values()) == 1, "original actual report normalization"
    )
    equalities = [all(values) for values in flags]
    for k, retained in enumerate(RETAINED_WEIGHTS):
        _check_quadratic(
            retained,
            scores[k],
            forecast_distance,
            F(*baseline_pair["coarse_forecast_risk"]),
            F(*baseline_pair["completed_forecast_risk"]),
            F(*baseline_pair["coarse_regret"]),
            F(*baseline_pair["completed_regret"]),
            F(*baseline_pair["x_scores"]["bayes_risk"]),
            equalities[k],
        )
    pair = {
        "actual_index": i,
        "assumed_index": j,
        "cells": cells,
        "forecast_distance": _wire(forecast_distance),
        "blends": [
            _blend_wire(retained, score)
            for retained, score in zip(RETAINED_WEIGHTS, scores, strict=True)
        ],
        "checks": dict.fromkeys(Z_CHECKS, True),
    }
    return pair, work, forecast_distance, scores, equalities


def analyze(problem):
    """Recompute Y and score all fixed blends after combined work preplanning."""
    _native(problem)
    _fields(problem, ("schema_version", "family", "experiment"), "Z wrapper fields")
    _require(
        type(problem["schema_version"]) is str
        and problem["schema_version"] == "det8-qr05z-problem-v1"
        and type(problem["family"]) is str
        and problem["family"] == "qr05z_fixed_attenuation",
        "Z wrapper schema/family",
    )
    prepared = _prepare(problem["experiment"])
    planned = _plan_z(prepared)
    # No Y or Z forecast scorer has run above this point.
    baseline = _analyze_y(problem["experiment"])
    parsed = prepared[0]
    baseline_work = (
        baseline["counts"]["completed_scoring_terms"] + baseline["counts"]["coarse_scoring_terms"]
    )
    _require(
        baseline_work == planned["baseline_scoring_terms"],
        "planned/executed inherited Y scoring terms",
    )
    work = {
        name: 0
        for name in ("blend_atoms", "mixture_terms", "distance_terms", "blend_scoring_terms")
    }
    pair_cells, blend_cells = [0] * 16, [0] * 48
    rows = []
    distances = [F(0)] * 16
    aggregate_scores = [[{name: F(0) for name in Z_SCORES} for _ in range(3)] for _ in range(16)]
    aggregate_flags = [[[] for _ in range(3)] for _ in range(16)]
    counts = {
        name: [0] * (16 if name == "positive_deviation_beliefs" else 48)
        for name in (
            "positive_deviation_beliefs",
            "positive_regret_beliefs",
            "better_than_coarse_beliefs",
            "equal_to_coarse_beliefs",
            "worse_than_coarse_beliefs",
            "better_than_base_beliefs",
            "equal_to_base_beliefs",
            "worse_than_base_beliefs",
        )
    }
    witnesses = {
        name: [None] * (16 if name == "first_positive_deviation" else 48)
        for name in (
            "first_positive_deviation",
            "first_positive_regret",
            "first_better_than_coarse",
            "first_equal_to_coarse",
            "first_worse_than_coarse",
            "first_better_than_base",
            "first_equal_to_base",
            "first_worse_than_base",
        )
    }
    for bid, (weight, channels, fallbacks) in enumerate(parsed):
        pairs = []
        for i, actual in enumerate(channels):
            for j, assumed in enumerate(channels):
                index = 4 * i + j
                pair, used, distance, scores, flags = _z_pair(
                    i, j, actual, assumed, fallbacks, baseline["beliefs"][bid]["pairs"][index]
                )
                pairs.append(pair)
                pair_cells[index] += len(pair["cells"])
                for name in work:
                    work[name] += used[name]
                distances[index] += weight * distance
                if distance > 0:
                    counts["positive_deviation_beliefs"][index] += 1
                    if witnesses["first_positive_deviation"][index] is None:
                        witnesses["first_positive_deviation"][index] = bid
                for k, score in enumerate(scores):
                    position = 3 * index + k
                    blend_cells[position] += len(pair["cells"])
                    aggregate_flags[index][k].append(flags[k])
                    for name in Z_SCORES:
                        aggregate_scores[index][k][name] += weight * score[name]
                    outcomes = {
                        "positive_regret": score["regret"] > 0,
                        "better_than_coarse": score["gain_over_coarse"] > 0,
                        "equal_to_coarse": score["gain_over_coarse"] == 0,
                        "worse_than_coarse": score["gain_over_coarse"] < 0,
                        "better_than_base": score["gain_over_base"] > 0,
                        "equal_to_base": score["gain_over_base"] == 0,
                        "worse_than_base": score["gain_over_base"] < 0,
                    }
                    for name, condition in outcomes.items():
                        if condition:
                            counts[name + "_beliefs"][position] += 1
                            if witnesses["first_" + name][position] is None:
                                witnesses["first_" + name][position] = bid
        rows.append({"belief_id": bid, "weight": _wire(weight, 1), "pairs": pairs})
    actual_work = {
        "pair_cells": pair_cells,
        "blend_cells": blend_cells,
        **work,
        "baseline_scoring_terms": baseline_work,
        "total_work_terms": baseline_work
        + work["mixture_terms"]
        + work["distance_terms"]
        + work["blend_scoring_terms"],
    }
    _require(actual_work == planned, "all planned/executed Z structure and work counts")
    aggregate = []
    for index, scores in enumerate(aggregate_scores):
        y = baseline["aggregate"]["pairs"][index]
        for k, retained in enumerate(RETAINED_WEIGHTS):
            _check_quadratic(
                retained,
                scores[k],
                distances[index],
                F(*y["coarse_forecast_risk"]),
                F(*y["completed_forecast_risk"]),
                F(*y["coarse_regret"]),
                F(*y["completed_regret"]),
                F(*y["x_scores"]["bayes_risk"]),
                all(aggregate_flags[index][k]),
            )
        aggregate.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                "forecast_distance": _wire(distances[index]),
                "blends": [
                    _blend_wire(retained, score)
                    for retained, score in zip(RETAINED_WEIGHTS, scores, strict=True)
                ],
                "checks": dict.fromkeys(Z_CHECKS, True),
            }
        )
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "levels": [_wire(level, 1) for level in LEVELS],
        "retained_weights": [_wire(weight, 1) for weight in RETAINED_WEIGHTS],
        "baseline": baseline,
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": witnesses,
        "counts": {"beliefs": len(rows), **actual_work, **counts},
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "canonical full Y/Z output byte cap")
    return json.loads(encoded)
