"""Exact history-level sign diagnostics for supplied convex polynomials.

Only the strict native guard is statically carried from this primary's
own lineage. No prior executor, policy optimization or physical-origin
authentication occurs here.
"""

import hashlib
import json
from fractions import Fraction
from itertools import pairwise
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 128
MAX_NODES = 2097152
MAX_BYTES = 33554432
MAX_HISTORIES = 128
MAX_PROFILES = 16
MAX_DECISIONS = 16
MAX_WORLD_CERTIFICATES = 40
MAX_ROOT_DIVISIONS = 2048
MAX_STRATA = 4096
MAX_MEMBERSHIPS = 524288
MAX_POINT_EVALUATIONS = 600000
MAX_TOTAL_WORK = 2000000

LEVELS = (Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1))
GROUP_NAMES = ("positive", "negative", "zero")
STRATUM_CHECKS = (
    "complete_sign_partition",
    "constant_sign_on_region",
    "original_weight_masses",
    "weighted_polynomial_decomposition",
    "point_or_parametric_decomposition",
)


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


def _fraction(value, lower, upper):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0
        and max(numerator.bit_length(), denominator.bit_length()) <= MAX_BITS,
        "invalid native fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must already be reduced")
    result = Fraction(numerator, denominator)
    _require(lower <= result <= upper, "fraction outside declared coefficient range")
    return result


def _retained(value, lower, upper):
    _require(
        type(value) is Fraction
        and lower <= value <= upper
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational outside range or bit bounds",
    )
    return value


def _pair(value, lower, upper):
    _retained(value, lower, upper)
    return [value.numerator, value.denominator]


def _root(A, B):
    _require(0 < 2 * B < A, "root division is restricted to strict interior zeros")
    return _retained(2 * B / A, 0, 1)


def _profile_term(w, A, B):
    # Products are internal, not retained scalars; cancellation is permitted.
    return w * A, w * B


def _evaluate(A, B, a):
    return _retained(A * a * a - 2 * B * a, -4, 6)


def _open_sign(A, B, lower, upper, root):
    """Prove the sign by a*(A*a-2*B), never by a sampled alpha."""
    _require(0 <= lower < upper <= 1, "invalid open interval")
    if A == B == 0:
        _require(root is None, "flat polynomial has no isolated interior root")
        return 0
    if A == 0:
        _require(root is None, "linear polynomial has no interior root")
        return 1 if B < 0 else -1
    if B <= 0:
        _require(root is None, "nonpositive B has no interior root")
        return 1
    if 2 * B >= A:
        _require(root is None, "endpoint or outside root must not be formed")
        return -1
    _require(
        root is not None and 0 < root < 1 and A * root == 2 * B,
        "complete interior root is required",
    )
    if upper <= root:
        return -1
    _require(lower >= root, "open stratum crosses an unrecorded root")
    return 1


def _accumulate(group, w, A, B, value):
    # No intermediate component bound: only the completed group is retained.
    mass, quadratic, half_linear, point_sum = group
    return (
        mass + w,
        quadratic + w * A,
        half_linear + w * B,
        point_sum if value is None else point_sum + w * value,
    )


def _polynomial(A, B):
    return {
        "quadratic_coefficient": _pair(A, 0, 2),
        "half_linear_coefficient": _pair(B, -2, 2),
    }


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "levels", "histories", "profiles", "decisions"))
    _require(
        problem["schema_version"] == "det8-qr05ae-problem-v1"
        and problem["family"] == "qr05ae_history_safety",
        "unknown history-safety schema",
    )
    _require(type(problem["levels"]) is list and len(problem["levels"]) == 4, "four fixed levels")
    _require(
        tuple(_fraction(v, 0, 1) for v in problem["levels"]) == LEVELS,
        "fixed levels differ",
    )
    histories = problem["histories"]
    _require(
        type(histories) is list and 1 <= len(histories) <= min(128, MAX_HISTORIES),
        "history inventory outside live bound",
    )
    H = len(histories)
    weights = []
    for i, row in enumerate(histories):
        _fields(row, ("belief_id", "weight"))
        _integer(row["belief_id"], i, i)
        weight = _fraction(row["weight"], 0, 1)
        _require(weight > 0, "history weights must be strictly positive")
        weights.append(weight)
    _require(sum(weights, Fraction(0)) == 1, "history weights must sum to one")
    supplied = problem["profiles"]
    _require(
        type(supplied) is list and len(supplied) == 16 and len(supplied) <= MAX_PROFILES,
        "sixteen profiles within the live cap are required",
    )
    profiles = []
    for i, row in enumerate(supplied):
        _fields(row, ("assumed_index", "actual_index", "coefficients"))
        _integer(row["assumed_index"], i // 4, i // 4)
        _integer(row["actual_index"], i % 4, i % 4)
        _require(
            type(row["coefficients"]) is list and len(row["coefficients"]) == H,
            "coefficient rows must align with every history",
        )
        coefficients = []
        for coefficient in row["coefficients"]:
            _fields(coefficient, ("quadratic_coefficient", "half_linear_coefficient"))
            coefficients.append(
                (
                    _fraction(coefficient["quadratic_coefficient"], 0, 2),
                    _fraction(coefficient["half_linear_coefficient"], -2, 2),
                )
            )
        profiles.append(coefficients)
    supplied = problem["decisions"]
    _require(
        type(supplied) is list and len(supplied) == 16 and len(supplied) <= MAX_DECISIONS,
        "sixteen decisions within the live cap are required",
    )
    policies = []
    for i, row in enumerate(supplied):
        _fields(row, ("assumed_index", "bound_index", "policy"))
        _integer(row["assumed_index"], i // 4, i // 4)
        _integer(row["bound_index"], i % 4, i % 4)
        policy = row["policy"]
        _require(type(policy) is dict, "policy must be a native object")
        if policy.get("kind") == "point":
            _fields(policy, ("kind", "weight"))
            policies.append(("point", _fraction(policy["weight"], 0, 1)))
        else:
            _fields(policy, ("kind", "lower", "upper"))
            _require(policy["kind"] == "interval", "unknown policy kind")
            _require(
                _fraction(policy["lower"], 0, 1) == 0 and _fraction(policy["upper"], 0, 1) == 1,
                "only the complete unit interval is admitted",
            )
            policies.append(("interval", None))

    # All schemas and normalization precede planning. Root multiplicity is
    # deliberately reserved without any division, deduplication or scoring.
    point_worlds = 0
    interval_occurrences = []
    for i, (kind, _) in enumerate(policies):
        if kind == "point":
            point_worlds += i % 4 + 1
        else:
            interval_occurrences.extend(4 * (i // 4) + t for t in range(i % 4 + 1))
    used = sorted(set(interval_occurrences))
    eligible = {p: [h for h, (A, B) in enumerate(profiles[p]) if 0 < 2 * B < A] for p in used}
    root_count = sum(len(eligible[p]) for p in used)
    reserved_strata = point_worlds + sum(2 * len(eligible[p]) + 3 for p in interval_occurrences)
    reserved_points = point_worlds + sum(len(eligible[p]) + 2 for p in interval_occurrences)
    reserved_memberships = H * reserved_strata
    reserved_evaluations = (H + 4) * reserved_points
    reserved_work = (
        (16 + len(used)) * H
        + root_count
        + 2 * H * reserved_strata
        + 4 * reserved_points
        + reserved_strata
        + 40
    )
    for actual, cap, name in (
        (40, MAX_WORLD_CERTIFICATES, "world certificates"),
        (root_count, MAX_ROOT_DIVISIONS, "root divisions"),
        (reserved_strata, MAX_STRATA, "conservatively reserved strata"),
        (reserved_memberships, MAX_MEMBERSHIPS, "conservatively reserved memberships"),
        (reserved_evaluations, MAX_POINT_EVALUATIONS, "conservatively reserved point evaluations"),
        (reserved_work, MAX_TOTAL_WORK, "conservatively reserved total work"),
    ):
        _require(actual <= cap, name + " exceed live cap")
    reservations = {
        "point_world_certificates": point_worlds,
        "interval_world_certificates": 40 - point_worlds,
        "interval_profiles": len(used),
        "interior_root_candidates": root_count,
        "reserved_strata": reserved_strata,
        "reserved_point_strata": reserved_points,
        "reserved_open_strata": reserved_strata - reserved_points,
        "reserved_history_memberships": reserved_memberships,
        "reserved_point_evaluations": reserved_evaluations,
        "reserved_total_work_terms": reserved_work,
    }
    return weights, profiles, policies, eligible, reservations


def _stratum(coefficients, weights, aggregate, roots, region, counts):
    point = region[0] == "point"
    alpha = region[1] if point else None
    indices = {name: [] for name in GROUP_NAMES}
    sums = {name: (Fraction(0),) * 4 for name in GROUP_NAMES}
    history_values = []
    for h, ((A, B), weight) in enumerate(zip(coefficients, weights, strict=True)):
        if point:
            value = _evaluate(A, B, alpha)
            counts["history_point_evaluations"] += 1
            history_values.append(value)
            sign = (value > 0) - (value < 0)
        else:
            value = None
            sign = _open_sign(A, B, region[1], region[2], roots.get(h))
            counts["open_sign_classifications"] += 1
            _require(type(sign) is int and sign in (-1, 0, 1), "sign classifier must be exact")
        name = "positive" if sign > 0 else "negative" if sign < 0 else "zero"
        indices[name].append(h)
        sums[name] = _accumulate(sums[name], weight, A, B, value)
        counts["group_accumulation_terms"] += 1

    _require(
        sorted(h for name in GROUP_NAMES for h in indices[name]) == list(range(len(weights))),
        "sign partition does not contain each history exactly once",
    )
    _require(sum(sums[name][0] for name in GROUP_NAMES) == 1, "group masses must sum to one")
    _require(
        tuple(sum(sums[name][k] for name in GROUP_NAMES) for k in (1, 2)) == aggregate,
        "three-group coefficient decomposition failed",
    )
    groups = {}
    for name in GROUP_NAMES:
        mass, A, B, _ = sums[name]
        _require(
            bool(indices[name]) == (mass > 0), "positive original weights and sign sets disagree"
        )
        if not indices[name]:
            _require(mass == A == B == 0, "empty group must have zero coefficients and mass")
        groups[name] = {
            "history_indices": indices[name],
            "likelihood_mass": _pair(mass, 0, 1),
            "polynomial": _polynomial(A, B),
        }
    point_values = None
    if point:
        values = {}
        for name in GROUP_NAMES:
            _, A, B, direct = sums[name]
            values[name] = _evaluate(A, B, alpha)
            counts["group_point_evaluations"] += 1
            _require(
                values[name] == direct, "group polynomial and weighted conditional values differ"
            )
        total = _evaluate(*aggregate, alpha)
        counts["aggregate_point_evaluations"] += 1
        _require(
            total == sum(values.values(), Fraction(0))
            and total
            == sum(
                (weight * value for weight, value in zip(weights, history_values, strict=True)),
                Fraction(0),
            ),
            "point decomposition differs from direct original-weight risk",
        )
        _require(values["zero"] == 0, "zero group must vanish at this singleton")
        _require(values["positive"] >= 0 and values["negative"] <= 0, "point group sign mismatch")
        _require(
            total == values["positive"] + values["negative"], "point risk cancellation differs"
        )
        point_values = {
            "history_excesses": [_pair(value, -4, 6) for value in history_values],
            "positive_contribution": _pair(values["positive"], 0, 6),
            "negative_contribution": _pair(values["negative"], -4, 0),
            "zero_contribution": _pair(values["zero"], 0, 0),
            "aggregate_excess": _pair(total, -4, 6),
            "benefit_magnitude": _pair(-values["negative"], 0, 4),
        }
        region_wire = {"kind": "point", "weight": _pair(alpha, 0, 1)}
    else:
        _require(
            sums["zero"][1] == sums["zero"][2] == 0, "open zero group must be identically zero"
        )
        region_wire = {
            "kind": "open_interval",
            "lower": _pair(region[1], 0, 1),
            "upper": _pair(region[2], 0, 1),
        }
    counts["stratum_certifications"] += 1
    return {
        "region": region_wire,
        "groups": groups,
        "point_values": point_values,
        "checks": dict.fromkeys(STRATUM_CHECKS, True),
    }


def analyze(problem):
    weights, profiles, policies, eligible, reservations = _prepare(problem)
    input_sha = hashlib.sha256(canonical(problem)).hexdigest()
    H = len(weights)
    counts = {
        "profile_aggregation_terms": 0,
        "root_classification_terms": reservations["interval_profiles"] * H,
        "root_divisions": 0,
        "history_point_evaluations": 0,
        "group_point_evaluations": 0,
        "aggregate_point_evaluations": 0,
        "open_sign_classifications": 0,
        "group_accumulation_terms": 0,
        "stratum_certifications": 0,
        "world_certifications": 0,
    }
    aggregates, root_maps, knot_lists, output_profiles = [], {}, {}, []
    distinct_roots = 0
    for p, coefficients in enumerate(profiles):
        A_total, B_total = Fraction(0), Fraction(0)
        for weight, (A, B) in zip(weights, coefficients, strict=True):
            term_A, term_B = _profile_term(weight, A, B)
            counts["profile_aggregation_terms"] += 1
            A_total += term_A
            B_total += term_B
        aggregate = (A_total, B_total)
        aggregates.append(aggregate)
        polynomial = _polynomial(*aggregate)
        records, knots_wire = None, None
        if p in eligible:
            records, roots = [], {}
            for h in eligible[p]:
                root = _root(*coefficients[h])
                counts["root_divisions"] += 1
                roots[h] = root
                records.append({"history_index": h, "weight": _pair(root, 0, 1)})
            knots = sorted({Fraction(0), Fraction(1), *roots.values()})
            _require(knots[0] == 0 and knots[-1] == 1, "complete endpoint knots required")
            _require(all(a < b for a, b in pairwise(knots)), "distinct knots must be sorted")
            distinct_roots += len(knots) - 2
            root_maps[p], knot_lists[p] = roots, knots
            knots_wire = [_pair(a, 0, 1) for a in knots]
        output_profiles.append(
            {
                "assumed_index": p // 4,
                "actual_index": p % 4,
                "aggregate_polynomial": polynomial,
                "interval_root_records": records,
                "interval_knots": knots_wire,
            }
        )

    decisions = []
    total_points = total_opens = 0
    for i, (kind, alpha) in enumerate(policies):
        s, bound = i // 4, i % 4
        worlds, harmed_worlds = [], []
        for t in range(bound + 1):
            p = 4 * s + t
            if kind == "point":
                regions = [("point", alpha)]
            else:
                knots = knot_lists[p]
                regions = []
                for j, knot in enumerate(knots):
                    regions.append(("point", knot))
                    if j + 1 < len(knots):
                        regions.append(("open_interval", knot, knots[j + 1]))
                _require(
                    len(regions) == 2 * len(knots) - 1, "whole policy domain must be partitioned"
                )
            strata, positive, negative = [], set(), set()
            for region in regions:
                point = region[0] == "point"
                total_points += int(point)
                total_opens += int(not point)
                stratum = _stratum(
                    profiles[p], weights, aggregates[p], root_maps.get(p, {}), region, counts
                )
                positive.update(stratum["groups"]["positive"]["history_indices"])
                negative.update(stratum["groups"]["negative"]["history_indices"])
                strata.append(stratum)
            if positive:
                harmed_worlds.append(t)
            worlds.append(
                {
                    "actual_index": t,
                    "profile_index": p,
                    "strata": strata,
                    "potentially_harmed_history_indices": sorted(positive),
                    "potentially_benefited_history_indices": sorted(negative),
                    "all_policy_weights_history_safe": not positive,
                    "checks": {
                        "policy_domain_covered": True,
                        "all_history_strata_preserved": True,
                        "no_policy_reoptimization": True,
                    },
                }
            )
            counts["world_certifications"] += 1
        _require(
            [w["actual_index"] for w in worlds] == list(range(bound + 1)),
            "all declared worlds required",
        )
        _require(
            harmed_worlds
            == [w["actual_index"] for w in worlds if w["potentially_harmed_history_indices"]],
            "world harm inventory differs",
        )
        decisions.append(
            {
                "assumed_index": s,
                "bound_index": bound,
                "policy": problem["decisions"][i]["policy"],
                "worlds": worlds,
                "harm_possible_world_indices": harmed_worlds,
                "checks": {
                    "declared_worlds_complete": True,
                    "shared_policy_preserved": True,
                    "no_historywise_selection": True,
                },
            }
        )

    S, T, O, R, I = (
        total_points + total_opens,
        total_points,
        total_opens,
        reservations["interval_profiles"],
        reservations["interior_root_candidates"],
    )
    expected_visits = {
        "profile_aggregation_terms": 16 * H,
        "root_classification_terms": R * H,
        "root_divisions": I,
        "history_point_evaluations": H * T,
        "group_point_evaluations": 3 * T,
        "aggregate_point_evaluations": T,
        "open_sign_classifications": H * O,
        "group_accumulation_terms": H * S,
        "stratum_certifications": S,
        "world_certifications": 40,
    }
    _require(
        counts == expected_visits, "executed visit inventory differs from the declared contract"
    )
    total_work = sum(counts.values())
    _require(
        total_work == (16 + R) * H + I + 2 * H * S + 4 * T + S + 40, "total work identity failed"
    )
    for actual, reserved, name in (
        (S, reservations["reserved_strata"], "strata"),
        (T, reservations["reserved_point_strata"], "point strata"),
        (O, reservations["reserved_open_strata"], "open strata"),
        (H * S, reservations["reserved_history_memberships"], "memberships"),
        ((H + 4) * T, reservations["reserved_point_evaluations"], "point evaluations"),
        (total_work, reservations["reserved_total_work_terms"], "total work"),
    ):
        _require(actual <= reserved, "execution exceeds conservative " + name + " reservation")
    counts = {
        "histories": H,
        "profiles": 16,
        "decisions": 16,
        "world_certificates": 40,
        **reservations,
        "distinct_interior_roots": distinct_roots,
        "strata": S,
        "point_strata": T,
        "open_strata": O,
        "history_memberships": H * S,
        **counts,
        "total_work_terms": total_work,
    }
    result = {
        "input_sha256": input_sha,
        "levels": problem["levels"],
        "histories": problem["histories"],
        "profiles": output_profiles,
        "decisions": decisions,
        "counts": counts,
    }
    # Serialization also validates the complete output against live native
    # bounds. The final load severs input, sibling and cross-call aliases.
    return json.loads(canonical(result))
