"""Independent exact history-diagnostic reference for QR-05AE.

Static own-lineage native guards. Conditional history polynomials remain
separate from original likelihood weights. Open signs use factorization,
not sampled alpha or history-specific policy choices.
"""

import hashlib
import json
from fractions import Fraction as F
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
LEVELS = (F(0), F(1, 2), F(3, 4), F(1))
STRATUM_CHECKS = (
    "complete_sign_partition",
    "constant_sign_on_region",
    "original_weight_masses",
    "weighted_polynomial_decomposition",
    "point_or_parametric_decomposition",
)
WORLD_CHECKS = (
    "policy_domain_covered",
    "all_history_strata_preserved",
    "no_policy_reoptimization",
)
DECISION_CHECKS = (
    "declared_worlds_complete",
    "shared_policy_preserved",
    "no_historywise_selection",
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


def _fraction(value, lower, upper):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    n, d = value
    _require(type(n) is int and type(d) is int and d > 0, "native rational components")
    _require(lower * d <= n <= upper * d and gcd(n, d) == 1, "reduced input rational interval")
    _require(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "input rational bit cap")
    return F(n, d)


def _wire(value, lower, upper):
    _require(type(value) is F and lower <= value <= upper, "retained rational interval")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained component bit cap",
    )
    return [value.numerator, value.denominator]


def _root(A, B):
    _require(type(A) is F and type(B) is F and 0 < 2 * B < A, "eligible interior sign root")
    value = 2 * B / A
    _wire(value, 0, 1)
    return value


def _profile_term(w, A, B):
    _require(all(type(v) is F for v in (w, A, B)), "exact internal profile product")
    return w * A, w * B


def _evaluate(A, B, alpha):
    _require(all(type(v) is F for v in (A, B, alpha)), "exact conditional polynomial operands")
    value = alpha * (A * alpha - 2 * B)
    _wire(value, -4, 6)
    return value


def _open_sign(A, B, lower, upper, root):
    _require(
        all(type(v) is F for v in (A, B, lower, upper)) and 0 <= lower < upper <= 1,
        "exact open region",
    )
    if root is not None:
        _require(
            type(root) is F and A * root == 2 * B and not lower < root < upper,
            "complete root-free open region",
        )
    if A == B == 0:
        return 0
    left, right = A * lower - 2 * B, A * upper - 2 * B
    if left >= 0 and right > 0:
        return 1
    if left < 0 and right <= 0:
        return -1
    raise ValueError("linear factor changes sign inside declared open region")


def _accumulate(group, w, A, B, value):
    _require(
        type(group) is tuple and len(group) == 4 and all(type(v) is F for v in (*group, w, A, B)),
        "exact internal group accumulator",
    )
    _require(value is None or type(value) is F, "point or parametric group contribution")
    mass, quadratic, cross, point = group
    return (
        mass + w,
        quadratic + w * A,
        cross + w * B,
        point + (F(0) if value is None else w * value),
    )


def _polynomial(A, B):
    return {"quadratic_coefficient": _wire(A, 0, 2), "half_linear_coefficient": _wire(B, -2, 2)}


def _prepare(problem):
    _native(problem)
    _fields(
        problem,
        ("schema_version", "family", "levels", "histories", "profiles", "decisions"),
        "exact AE problem fields",
    )
    _require(problem["schema_version"] == "det8-qr05ae-problem-v1", "AE schema")
    _require(problem["family"] == "qr05ae_history_safety", "AE family")
    _require(
        type(problem["levels"]) is list
        and len(problem["levels"]) == 4
        and tuple(_fraction(v, 0, 1) for v in problem["levels"]) == LEVELS,
        "fixed AE levels",
    )
    histories = problem["histories"]
    _require(type(histories) is list and 1 <= len(histories) <= MAX_HISTORIES, "history cap")
    weights = []
    for h, row in enumerate(histories):
        _fields(row, ("belief_id", "weight"), "exact history fields")
        _require(
            type(row["belief_id"]) is int and row["belief_id"] == h, "ordered native history id"
        )
        weight = _fraction(row["weight"], 0, 1)
        _require(weight > 0, "strictly positive original history likelihood")
        weights.append(weight)
    _require(sum(weights, F(0)) == 1, "original history likelihood normalization")
    profiles = problem["profiles"]
    _require(
        type(profiles) is list and len(profiles) == 16 and len(profiles) <= MAX_PROFILES,
        "sixteen ordered profile cap",
    )
    coefficients = []
    for index, row in enumerate(profiles):
        _fields(row, ("assumed_index", "actual_index", "coefficients"), "exact profile fields")
        _require(
            type(row["assumed_index"]) is int
            and row["assumed_index"] == index // 4
            and type(row["actual_index"]) is int
            and row["actual_index"] == index % 4,
            "ordered native profile indices",
        )
        values = row["coefficients"]
        _require(
            type(values) is list and len(values) == len(weights), "history coefficient dimension"
        )
        parsed = []
        for value in values:
            _fields(
                value,
                ("quadratic_coefficient", "half_linear_coefficient"),
                "exact history polynomial",
            )
            parsed.append(
                (
                    _fraction(value["quadratic_coefficient"], 0, 2),
                    _fraction(value["half_linear_coefficient"], -2, 2),
                )
            )
        coefficients.append(parsed)
    decisions = problem["decisions"]
    _require(
        type(decisions) is list and len(decisions) == 16 and len(decisions) <= MAX_DECISIONS,
        "sixteen ordered decision cap",
    )
    policies = []
    for index, row in enumerate(decisions):
        _fields(row, ("assumed_index", "bound_index", "policy"), "exact decision fields")
        _require(
            type(row["assumed_index"]) is int
            and row["assumed_index"] == index // 4
            and type(row["bound_index"]) is int
            and row["bound_index"] == index % 4,
            "ordered native decision indices",
        )
        policy = row["policy"]
        _require(type(policy) is dict and type(policy.get("kind")) is str, "native policy kind")
        if policy["kind"] == "point":
            _fields(policy, ("kind", "weight"), "exact point policy")
            policies.append(_fraction(policy["weight"], 0, 1))
        else:
            _fields(policy, ("kind", "lower", "upper"), "exact interval policy")
            _require(
                policy["kind"] == "interval"
                and _fraction(policy["lower"], 0, 1) == 0
                and _fraction(policy["upper"], 0, 1) == 1,
                "whole interval policy only",
            )
            policies.append(None)
    occurrences = [
        (4 * (index // 4) + t, policies[index]) for index in range(16) for t in range(index % 4 + 1)
    ]
    used = {p for p, policy in occurrences if policy is None}
    eligible = {p: [h for h, (A, B) in enumerate(coefficients[p]) if 0 < 2 * B < A] for p in used}
    H, R = len(weights), len(used)
    I = sum(len(ids) for ids in eligible.values())
    P = sum(policy is not None for _, policy in occurrences)
    Sr = P + sum(2 * len(eligible[p]) + 3 for p, policy in occurrences if policy is None)
    Tr = P + sum(len(eligible[p]) + 2 for p, policy in occurrences if policy is None)
    Or, Mr, Er = Sr - Tr, H * Sr, (H + 4) * Tr
    Wr = (16 + R) * H + I + 2 * H * Sr + 4 * Tr + Sr + 40
    _require(
        len(occurrences) == 40 and 40 <= MAX_WORLD_CERTIFICATES, "world-certificate reservation"
    )
    _require(I <= MAX_ROOT_DIVISIONS, "root division reservation")
    _require(Sr <= MAX_STRATA, "conservative stratum reservation")
    _require(Mr <= MAX_MEMBERSHIPS, "history membership reservation")
    _require(Er <= MAX_POINT_EVALUATIONS, "point evaluation reservation")
    _require(Wr <= MAX_TOTAL_WORK, "total work reservation")
    counts = {
        "histories": H,
        "profiles": 16,
        "decisions": 16,
        "world_certificates": 40,
        "point_world_certificates": P,
        "interval_world_certificates": 40 - P,
        "interval_profiles": R,
        "interior_root_candidates": I,
        "reserved_strata": Sr,
        "reserved_point_strata": Tr,
        "reserved_open_strata": Or,
        "reserved_history_memberships": Mr,
        "reserved_point_evaluations": Er,
        "reserved_total_work_terms": Wr,
    }
    return weights, coefficients, policies, used, eligible, counts


def analyze(problem):
    """Diagnose fixed shared policies without changing history weights or rules."""
    weights, coefficients, policies, used, eligible, counts = _prepare(problem)
    visited = dict.fromkeys(
        (
            "profile_aggregation_terms",
            "root_classification_terms",
            "root_divisions",
            "history_point_evaluations",
            "group_point_evaluations",
            "aggregate_point_evaluations",
            "open_sign_classifications",
            "group_accumulation_terms",
            "stratum_certifications",
            "world_certifications",
        ),
        0,
    )
    profiles, aggregates, roots, knots = [], [], {}, {}
    distinct = 0
    for index, rows in enumerate(coefficients):
        aggregate_A, aggregate_B = F(0), F(0)
        for weight, (A, B) in zip(weights, rows, strict=True):
            term_A, term_B = _profile_term(weight, A, B)
            aggregate_A += term_A
            aggregate_B += term_B
            visited["profile_aggregation_terms"] += 1
        aggregate = _polynomial(aggregate_A, aggregate_B)
        aggregates.append((aggregate_A, aggregate_B))
        records = knot_wire = None
        if index in used:
            roots[index] = {}
            records = []
            for h, (A, B) in enumerate(rows):
                is_eligible = 0 < 2 * B < A
                _require(is_eligible == (h in eligible[index]), "same planned root classification")
                visited["root_classification_terms"] += 1
                if is_eligible:
                    root = _root(A, B)
                    roots[index][h] = root
                    records.append({"history_index": h, "weight": _wire(root, 0, 1)})
                    visited["root_divisions"] += 1
            knots[index] = sorted({F(0), F(1), *roots[index].values()})
            distinct += len(knots[index]) - 2
            knot_wire = [_wire(v, 0, 1) for v in knots[index]]
        profiles.append(
            {
                "assumed_index": index // 4,
                "actual_index": index % 4,
                "aggregate_polynomial": aggregate,
                "interval_root_records": records,
                "interval_knots": knot_wire,
            }
        )
    decisions = []
    S = T = O = 0
    for index, alpha in enumerate(policies):
        assumed, bound = index // 4, index % 4
        worlds = []
        for actual in range(bound + 1):
            pid = 4 * assumed + actual
            regions = []
            if alpha is not None:
                regions.append(("point", alpha, alpha))
            else:
                values = knots[pid]
                _require(
                    values[0] == 0 and values[-1] == 1 and values == sorted(set(values)),
                    "whole interval knot domain",
                )
                for position, value in enumerate(values):
                    if position:
                        regions.append(("open_interval", values[position - 1], value))
                    regions.append(("point", value, value))
                _require(len(regions) == 2 * len(values) - 1, "all singleton and open strata")
            strata = []
            positive_union, negative_union = set(), set()
            for kind, lower, upper in regions:
                S += 1
                is_point = kind == "point"
                T += int(is_point)
                O += int(not is_point)
                groups = {
                    name: (F(0), F(0), F(0), F(0)) for name in ("positive", "negative", "zero")
                }
                ids = {name: [] for name in groups}
                history_values = []
                for h, (weight, (A, B)) in enumerate(zip(weights, coefficients[pid], strict=True)):
                    if is_point:
                        value = _evaluate(A, B, lower)
                        history_values.append(value)
                        sign = (value > 0) - (value < 0)
                        visited["history_point_evaluations"] += 1
                    else:
                        value = None
                        sign = _open_sign(A, B, lower, upper, roots[pid].get(h))
                        _require(type(sign) is int and sign in (-1, 0, 1), "native exact open sign")
                        visited["open_sign_classifications"] += 1
                    name = "positive" if sign > 0 else "negative" if sign < 0 else "zero"
                    ids[name].append(h)
                    groups[name] = _accumulate(groups[name], weight, A, B, value)
                    visited["group_accumulation_terms"] += 1
                _require(
                    sorted(h for group_ids in ids.values() for h in group_ids)
                    == list(range(len(weights))),
                    "complete disjoint sign partition",
                )
                _require(
                    sum((g[0] for g in groups.values()), F(0)) == 1, "all original group masses"
                )
                _require(
                    sum((g[1] for g in groups.values()), F(0)) == aggregates[pid][0]
                    and sum((g[2] for g in groups.values()), F(0)) == aggregates[pid][1],
                    "three-group coefficientwise decomposition",
                )
                group_wire = {}
                for name, values in groups.items():
                    mass, A, B, _point_sum = values
                    _require(
                        (mass > 0) == bool(ids[name]),
                        "positive weights preserve sign-group mass semantics",
                    )
                    if not ids[name]:
                        _require(mass == A == B == 0, "empty group zero polynomial")
                    group_wire[name] = {
                        "history_indices": ids[name],
                        "likelihood_mass": _wire(mass, 0, 1),
                        "polynomial": _polynomial(A, B),
                    }
                point_values = None
                if is_point:
                    group_values = {}
                    for name, (_, A, B, direct) in groups.items():
                        val = _evaluate(A, B, lower)
                        visited["group_point_evaluations"] += 1
                        _require(
                            val == direct,
                            "group polynomial equals direct weighted conditional risks",
                        )
                        group_values[name] = val
                    aggregate = _evaluate(*aggregates[pid], lower)
                    visited["aggregate_point_evaluations"] += 1
                    _require(
                        aggregate == sum(group_values.values(), F(0)) and group_values["zero"] == 0,
                        "point decomposition includes vanishing zero group",
                    )
                    _require(
                        group_values["positive"] >= 0 and group_values["negative"] <= 0,
                        "signed positive and negative contributions",
                    )
                    point_values = {
                        "history_excesses": [_wire(v, -4, 6) for v in history_values],
                        "positive_contribution": _wire(group_values["positive"], 0, 6),
                        "negative_contribution": _wire(group_values["negative"], -4, 0),
                        "zero_contribution": _wire(group_values["zero"], 0, 0),
                        "aggregate_excess": _wire(aggregate, -4, 6),
                        "benefit_magnitude": _wire(-group_values["negative"], 0, 4),
                    }
                    region = {"kind": "point", "weight": _wire(lower, 0, 1)}
                else:
                    _require(
                        groups["zero"][1] == groups["zero"][2] == 0,
                        "open zero group identically zero",
                    )
                    region = {
                        "kind": "open_interval",
                        "lower": _wire(lower, 0, 1),
                        "upper": _wire(upper, 0, 1),
                    }
                positive_union.update(ids["positive"])
                negative_union.update(ids["negative"])
                strata.append(
                    {
                        "region": region,
                        "groups": group_wire,
                        "point_values": point_values,
                        "checks": dict.fromkeys(STRATUM_CHECKS, True),
                    }
                )
                visited["stratum_certifications"] += 1
            worlds.append(
                {
                    "actual_index": actual,
                    "profile_index": pid,
                    "strata": strata,
                    "potentially_harmed_history_indices": sorted(positive_union),
                    "potentially_benefited_history_indices": sorted(negative_union),
                    "all_policy_weights_history_safe": not positive_union,
                    "checks": dict.fromkeys(WORLD_CHECKS, True),
                }
            )
            visited["world_certifications"] += 1
        _require(
            [row["actual_index"] for row in worlds] == list(range(bound + 1)),
            "complete declared world set",
        )
        decisions.append(
            {
                "assumed_index": assumed,
                "bound_index": bound,
                "policy": problem["decisions"][index]["policy"],
                "worlds": worlds,
                "harm_possible_world_indices": [
                    row["actual_index"]
                    for row in worlds
                    if not row["all_policy_weights_history_safe"]
                ],
                "checks": dict.fromkeys(DECISION_CHECKS, True),
            }
        )
    H, R, I = len(weights), len(used), counts["interior_root_candidates"]
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
    _require(visited == expected_visits, "exact executed visit inventory")
    total = (16 + R) * H + I + 2 * H * S + 4 * T + S + 40
    _require(
        sum(visited.values()) == total <= counts["reserved_total_work_terms"],
        "actual work bounded by prospective reservation",
    )
    _require(
        S <= counts["reserved_strata"]
        and T <= counts["reserved_point_strata"]
        and O <= counts["reserved_open_strata"]
        and H * S <= counts["reserved_history_memberships"]
        and (H + 4) * T <= counts["reserved_point_evaluations"],
        "all executed reservations",
    )
    counts.update(
        {
            "distinct_interior_roots": distinct,
            "strata": S,
            "point_strata": T,
            "open_strata": O,
            "history_memberships": H * S,
            **visited,
            "total_work_terms": total,
        }
    )
    result = {
        "input_sha256": hashlib.sha256(_canonical(problem)).hexdigest(),
        "levels": problem["levels"],
        "histories": problem["histories"],
        "profiles": profiles,
        "decisions": decisions,
        "counts": counts,
    }
    _native(result)
    encoded = _canonical(result)
    _require(len(encoded) <= MAX_BYTES, "complete detached AE output byte cap")
    return json.loads(encoded)
