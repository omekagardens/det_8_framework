"""Independent conditional-history signs and complete shared-policy partitions.

Generic controls do not load any producer artifacts. Fixed tests are separately
named and consume pinned JSON only after the coordinated release.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
WEIGHTS = [[0, 1], [1, 2], [1, 1]]


def native(value):
    if value is None or type(value) in (bool, int, str):
        if type(value) is int:
            assert abs(value).bit_length() <= 4096
        return
    if type(value) is list:
        for item in value:
            native(item)
        return
    if type(value) is dict:
        assert all(type(key) is str for key in value)
        for item in value.values():
            native(item)
        return
    raise AssertionError(f"non-native mathematical wire type: {type(value)}")


def wire(value):
    native(value)
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


def digest(value):
    return hashlib.sha256(wire(value)).hexdigest()


def fraction(value):
    assert type(value) is list and len(value) == 2
    n, d = value
    assert type(n) is int and type(d) is int and d > 0
    result = F(n, d)
    assert [result.numerator, result.denominator] == value
    assert max(abs(result.numerator).bit_length(), result.denominator.bit_length()) <= 4096
    return result


def fw(value):
    value = F(value)
    return [value.numerator, value.denominator]


def private_module(name, filename):
    if name in sys.modules:
        raise RuntimeError("private test module name already in use")
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError("required module unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def replaced(tree, path, value):
    if not path:
        return value
    answer = tree.copy()
    answer[path[0]] = value if len(path) == 1 else replaced(tree[path[0]], path[1:], value)
    return answer


GROUPS = ("positive", "negative", "zero")
CAPS = (
    "MAX_BITS",
    "MAX_DEPTH",
    "MAX_NODES",
    "MAX_BYTES",
    "MAX_HISTORIES",
    "MAX_PROFILES",
    "MAX_DECISIONS",
    "MAX_WORLD_CERTIFICATES",
    "MAX_ROOT_DIVISIONS",
    "MAX_STRATA",
    "MAX_MEMBERSHIPS",
    "MAX_POINT_EVALUATIONS",
    "MAX_TOTAL_WORK",
)
HOOKS = ("_root", "_profile_term", "_evaluate", "_open_sign", "_accumulate")
STRATUM_CHECKS = (
    "complete_sign_partition",
    "constant_sign_on_region",
    "original_weight_masses",
    "weighted_polynomial_decomposition",
    "point_or_parametric_decomposition",
)
WORLD_CHECKS = ("policy_domain_covered", "all_history_strata_preserved", "no_policy_reoptimization")
DECISION_CHECKS = (
    "declared_worlds_complete",
    "shared_policy_preserved",
    "no_historywise_selection",
)


def poly(a, b):
    return {"quadratic_coefficient": fw(a), "half_linear_coefficient": fw(b)}


def coefficients(row):
    return fraction(row["quadratic_coefficient"]), fraction(row["half_linear_coefficient"])


def point(a=F(1, 2)):
    return {"kind": "point", "weight": fw(a)}


def interval():
    return {"kind": "interval", "lower": [0, 1], "upper": [1, 1]}


def problem_of(rows=((2, F(1, 4)), (2, F(3, 4))), weights=None, policy=None):
    if weights is None:
        weights = [F(1, len(rows)) for _ in rows]
    if policy is None:
        policy = interval()
    return {
        "schema_version": "det8-qr05ae-problem-v1",
        "family": "qr05ae_history_safety",
        "levels": copy.deepcopy(LEVELS),
        "histories": [{"belief_id": i, "weight": fw(w)} for i, w in enumerate(weights)],
        "profiles": [
            {"assumed_index": s, "actual_index": t, "coefficients": [poly(a, b) for a, b in rows]}
            for s in range(4)
            for t in range(4)
        ],
        "decisions": [
            {"assumed_index": s, "bound_index": u, "policy": copy.deepcopy(policy)}
            for s in range(4)
            for u in range(4)
        ],
    }


def mixed_problem():
    p = problem_of(
        [(0, 0), (0, 1), (0, -1), (2, 0), (2, 1), (2, F(1, 4)), (2, F(3, 4))],
        [F(i, 28) for i in range(1, 8)],
    )
    for i, d in enumerate(p["decisions"]):
        if i % 3:
            d["policy"] = point(F(i % 4, 3))
    # Different worlds need different partitions, with the same supplied alpha.
    p["profiles"][1]["coefficients"][-1] = poly(2, F(1, 2))
    return p


def duplicate_problem():
    return problem_of([(2, F(1, 2))] * 4)


def reservations(problem):
    h = len(problem["histories"])
    points, used, occurrences = 0, set(), []
    for d in problem["decisions"]:
        for t in range(d["bound_index"] + 1):
            index = 4 * d["assumed_index"] + t
            if d["policy"]["kind"] == "point":
                points += 1
            else:
                used.add(index)
                occurrences.append(index)
    interior = {
        i: sum(0 < 2 * b < a for a, b in map(coefficients, problem["profiles"][i]["coefficients"]))
        for i in used
    }
    roots = sum(interior.values())
    sr = points + sum(2 * interior[i] + 3 for i in occurrences)
    tr = points + sum(interior[i] + 2 for i in occurrences)
    return {
        "histories": h,
        "profiles": 16,
        "decisions": 16,
        "world_certificates": 40,
        "point_world_certificates": points,
        "interval_world_certificates": 40 - points,
        "interval_profiles": len(used),
        "interior_root_candidates": roots,
        "reserved_strata": sr,
        "reserved_point_strata": tr,
        "reserved_open_strata": sr - tr,
        "reserved_history_memberships": h * sr,
        "reserved_point_evaluations": (h + 4) * tr,
        "reserved_total_work_terms": (16 + len(used)) * h + roots + 2 * h * sr + 4 * tr + sr + 40,
    }, used


def independent_analysis(problem):
    """Exact factorization, complete groups and direct weighted conditional values."""
    counts, used = reservations(problem)
    weights = [fraction(r["weight"]) for r in problem["histories"]]
    profiles, root_lists = [], {}
    for i, profile in enumerate(problem["profiles"]):
        rows = list(map(coefficients, profile["coefficients"]))
        aggregate = [sum(w * x[j] for w, x in zip(weights, rows, strict=True)) for j in (0, 1)]
        records = knots = None
        if i in used:
            records = [
                {"history_index": hi, "weight": fw(2 * b / a)}
                for hi, (a, b) in enumerate(rows)
                if 0 < 2 * b < a
            ]
            roots = sorted({fraction(r["weight"]) for r in records})
            root_lists[i] = roots
            knots = list(map(fw, [F(0), *roots, F(1)]))
        profiles.append(
            {
                "assumed_index": profile["assumed_index"],
                "actual_index": profile["actual_index"],
                "aggregate_polynomial": poly(*aggregate),
                "interval_root_records": records,
                "interval_knots": knots,
            }
        )
    decisions, ns, nt, no = [], 0, 0, 0
    for decision in problem["decisions"]:
        worlds = []
        for t in range(decision["bound_index"] + 1):
            pi = 4 * decision["assumed_index"] + t
            rows = list(map(coefficients, problem["profiles"][pi]["coefficients"]))
            aggregate = coefficients(profiles[pi]["aggregate_polynomial"])
            regions = [copy.deepcopy(decision["policy"])]
            if decision["policy"]["kind"] == "interval":
                knots = [F(0), *root_lists[pi], F(1)]
                regions = []
                for j, knot in enumerate(knots):
                    if j:
                        regions.append(
                            {"kind": "open_interval", "lower": fw(knots[j - 1]), "upper": fw(knot)}
                        )
                    regions.append(point(knot))
            strata, positive_union, negative_union = [], set(), set()
            for region in regions:
                is_point = region["kind"] == "point"
                ns += 1
                nt += is_point
                no += not is_point
                values, signs = [], []
                for a, b in rows:
                    if is_point:
                        x = fraction(region["weight"])
                        value = sum((a * x * x, -b * x, -b * x))
                        values.append(value)
                        sign = (value > 0) - (value < 0)
                    else:
                        lower, upper = fraction(region["lower"]), fraction(region["upper"])
                        if a == 0:
                            sign = (b < 0) - (b > 0)
                        else:
                            # Monotonic linear factor on a strictly positive open interval.
                            left, right = a * lower - 2 * b, a * upper - 2 * b
                            assert left >= 0 or right <= 0
                            sign = 1 if left >= 0 else -1
                    signs.append(sign)
                groups, scalars = {}, {}
                for name, sign in zip(GROUPS, (1, -1, 0), strict=True):
                    indices = [hi for hi, value in enumerate(signs) if value == sign]
                    subtotal = [sum(weights[hi] * rows[hi][j] for hi in indices) for j in (0, 1)]
                    groups[name] = {
                        "history_indices": indices,
                        "likelihood_mass": fw(sum(weights[hi] for hi in indices)),
                        "polynomial": poly(*subtotal),
                    }
                    if is_point:
                        scalars[name] = sum(weights[hi] * values[hi] for hi in indices)
                        x = fraction(region["weight"])
                        assert scalars[name] == subtotal[0] * x * x - 2 * subtotal[1] * x
                assert [
                    sum(coefficients(groups[name]["polynomial"])[j] for name in GROUPS)
                    for j in (0, 1)
                ] == list(aggregate)
                assert sum(fraction(groups[name]["likelihood_mass"]) for name in GROUPS) == 1
                positive_union.update(groups["positive"]["history_indices"])
                negative_union.update(groups["negative"]["history_indices"])
                point_values = None
                if is_point:
                    net = sum(w * v for w, v in zip(weights, values, strict=True))
                    assert (
                        scalars["positive"] >= 0
                        and scalars["negative"] <= 0
                        and scalars["zero"] == 0
                    )
                    point_values = {
                        "history_excesses": list(map(fw, values)),
                        "positive_contribution": fw(scalars["positive"]),
                        "negative_contribution": fw(scalars["negative"]),
                        "zero_contribution": fw(scalars["zero"]),
                        "aggregate_excess": fw(net),
                        "benefit_magnitude": fw(-scalars["negative"]),
                    }
                else:
                    assert groups["zero"]["polynomial"] == poly(0, 0)
                strata.append(
                    {
                        "region": region,
                        "groups": groups,
                        "point_values": point_values,
                        "checks": dict.fromkeys(STRATUM_CHECKS, True),
                    }
                )
            worlds.append(
                {
                    "actual_index": t,
                    "profile_index": pi,
                    "strata": strata,
                    "potentially_harmed_history_indices": sorted(positive_union),
                    "potentially_benefited_history_indices": sorted(negative_union),
                    "all_policy_weights_history_safe": not positive_union,
                    "checks": dict.fromkeys(WORLD_CHECKS, True),
                }
            )
        decisions.append(
            {
                **copy.deepcopy(decision),
                "worlds": worlds,
                "harm_possible_world_indices": [
                    w["actual_index"] for w in worlds if w["potentially_harmed_history_indices"]
                ],
                "checks": dict.fromkeys(DECISION_CHECKS, True),
            }
        )
    h, r, roots = (
        counts["histories"],
        counts["interval_profiles"],
        counts["interior_root_candidates"],
    )
    counts.update(
        distinct_interior_roots=sum(map(len, root_lists.values())),
        strata=ns,
        point_strata=nt,
        open_strata=no,
        history_memberships=h * ns,
        profile_aggregation_terms=16 * h,
        root_classification_terms=r * h,
        root_divisions=roots,
        history_point_evaluations=h * nt,
        group_point_evaluations=3 * nt,
        aggregate_point_evaluations=nt,
        open_sign_classifications=h * no,
        group_accumulation_terms=h * ns,
        stratum_certifications=ns,
        world_certifications=40,
        total_work_terms=(16 + r) * h + roots + 2 * h * ns + 4 * nt + ns + 40,
    )
    return {
        "input_sha256": digest(problem),
        "levels": copy.deepcopy(LEVELS),
        "histories": copy.deepcopy(problem["histories"]),
        "profiles": profiles,
        "decisions": decisions,
        "counts": counts,
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ae_test_primary", "safety.py"),
        private_module("_qr05ae_test_reference", "reference_qr05ae.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ae_test_runner", "study.py")


@pytest.mark.parametrize(
    "builder",
    [
        problem_of,
        mixed_problem,
        duplicate_problem,
        lambda: problem_of([(0, 0)]),
        lambda: problem_of([(0, 2), (0, -2)], policy=point(1)),
        lambda: problem_of([(0, 1), (0, -1)], [F(1, 3), F(2, 3)]),
        lambda: problem_of([(2, 1), (2, 0), (0, 0)]),
        lambda: problem_of([(2, F(1, 2)), (2, F(1, 2) + F(1, 2**128))]),
        lambda: problem_of([(2, F(1, 4)), (2, F(3, 4))], policy=point()),
        lambda: problem_of([(2, -2)], policy=point(1)),
    ],
)
def test_generic_complete_wire_sign_factorization_three_groups_and_work(executors, builder):
    p = builder()
    wanted = wire(independent_analysis(p))
    for module in executors:
        assert wire(module.analyze(p)) == wanted


def test_aggregate_zero_hides_harm_benefit_and_likelihood_is_not_contribution(executors):
    p = problem_of(policy=point())
    for module in executors:
        answer = module.analyze(p)
        s = answer["decisions"][0]["worlds"][0]["strata"][0]
        assert s["point_values"]["history_excesses"] == [[1, 4], [-1, 4]]
        assert s["point_values"]["aggregate_excess"] == [0, 1]
        assert s["point_values"]["positive_contribution"] == [1, 8]
        assert s["point_values"]["negative_contribution"] == [-1, 8]
        assert s["point_values"]["benefit_magnitude"] == [1, 8]
        assert s["groups"]["positive"]["likelihood_mass"] == [1, 2]
        assert answer["decisions"][0]["harm_possible_world_indices"] == [0]
    opposite = problem_of([(0, -1), (0, 1)])
    for module in executors:
        answer = module.analyze(opposite)
        assert answer["profiles"][0]["aggregate_polynomial"] == poly(0, 0)
        assert answer["decisions"][0]["worlds"][0]["all_policy_weights_history_safe"] is False


def test_complete_zero_roots_singleton_zero_group_polynomial_and_common_alpha(executors):
    p = problem_of()
    for module in executors:
        answer = module.analyze(p)
        assert answer["profiles"][0]["interval_knots"] == [[0, 1], [1, 4], [3, 4], [1, 1]]
        strata = answer["decisions"][0]["worlds"][0]["strata"]
        assert len(strata) == 7
        assert strata[2]["groups"]["zero"]["history_indices"] == [0]
        assert strata[2]["groups"]["zero"]["polynomial"] == poly(1, F(1, 8))
        assert strata[2]["point_values"]["zero_contribution"] == [0, 1]
        assert strata[0]["groups"]["zero"]["polynomial"] == poly(2, F(1, 2))
        assert [s["groups"]["positive"]["history_indices"] for s in strata[1::2]] == [
            [],
            [0],
            [0, 1],
        ]
        # Neither aggregate zero1/2 nor individual minimizing weights1/8,3/8 are knots.
        assert [1, 2] not in answer["profiles"][0]["interval_knots"]
        assert [1, 8] not in answer["profiles"][0]["interval_knots"]
        assert [3, 8] not in answer["profiles"][0]["interval_knots"]
        assert all(s["point_values"] is None for s in strata[1::2])


def test_duplicate_root_records_keep_every_history_but_only_knots_are_deduplicated(executors):
    for module in executors:
        a = module.analyze(duplicate_problem())
        assert a["profiles"][0]["interval_root_records"] == [
            {"history_index": i, "weight": [1, 2]} for i in range(4)
        ]
        assert a["profiles"][0]["interval_knots"] == [[0, 1], [1, 2], [1, 1]]
        assert a["counts"]["root_divisions"] == 64
        assert a["counts"]["distinct_interior_roots"] == 16
        assert a["counts"]["reserved_strata"] > a["counts"]["strata"]


def test_point_only_policies_never_form_even_unrepresentable_interior_roots(executors, monkeypatch):
    d = 1 << 4095
    p = problem_of([(F(3, d), F(1, d - 1))], policy=point(0))

    def forbidden(*_args):
        raise RuntimeError("irrelevant root division")

    for module in executors:
        with monkeypatch.context() as m:
            m.setattr(module, "_root", forbidden)
            assert wire(module.analyze(p)) == wire(independent_analysis(p))
        interval_p = problem_of([(F(3, d), F(1, d - 1))])
        with pytest.raises(ValueError):
            module.analyze(interval_p)


def test_retained_group_values_overflow_even_when_case_average_cancels(executors):
    d = (1 << 4095) - 1
    p = problem_of(
        [(0, -F(1, 6)), (0, -F(1, 2 * d)), (0, F(1, 6)), (0, F(1, 2 * d))], policy=point(1)
    )
    for r in p["profiles"][0]["coefficients"]:
        coefficients(r)
    assert ((F(1, 3) + F(1, d)) / 4).denominator.bit_length() == 4098
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)


def cancellation_problem():
    d = 1 << 4095
    return problem_of([(1, F(1, 2))] * 2, [F(1, d), F(d - 1, d)], point())


def test_oversized_unretained_weighted_products_cancel_without_rejecting(executors):
    p = cancellation_problem()
    assert (fraction(p["histories"][0]["weight"]) * F(-1, 4)).denominator.bit_length() == 4098
    wanted = independent_analysis(p)
    native(wanted)
    for module in executors:
        assert wire(module.analyze(p)) == wire(wanted)


def test_tiny_positive_history_mass_is_not_rounded_or_dropped(executors):
    d = 1 << 1024
    p = problem_of([(0, -F(1, 2)), (0, 0)], [F(1, d), F(d - 1, d)], point(1))
    for module in executors:
        a = module.analyze(p)
        stratum = a["decisions"][0]["worlds"][0]["strata"][0]
        assert stratum["groups"]["positive"]["likelihood_mass"] == [1, d]
        assert stratum["point_values"]["positive_contribution"] == [1, d]


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
    p = problem_of()
    bad = [None, [], (), DictChild(p), {**p, "extra": 0}, {**p, 1: 0}]
    for key in p:
        bad.append({k: v for k, v in p.items() if k != key})
    for key in ("schema_version", "family"):
        for value in (None, "wrong", StrChild(p[key]), True):
            bad.append(replaced(p, (key,), value))
    for key in ("levels", "histories", "profiles", "decisions"):
        for value in (
            None,
            tuple(p[key]),
            ListChild(p[key]),
            [],
            p[key][::-1],
            p[key] + p[key][:1],
        ):
            bad.append(replaced(p, (key,), value))
    for value in ([0, 2], [False, 1], (0, 1), [1, 0], [0.0, 1]):
        bad.append(replaced(p, ("levels", 0), value))
    for path in (
        ("histories", 0),
        ("profiles", 15),
        ("decisions", 15),
        ("profiles", 15, "coefficients", 1),
    ):
        row = p
        for key in path:
            row = row[key]
        for value in (None, [], DictChild(row), {**row, "extra": 0}):
            bad.append(replaced(p, path, value))
        for key in row:
            bad.append(replaced(p, path, {k: v for k, v in row.items() if k != key}))
    for path, correct in (
        (("histories", 1, "belief_id"), 1),
        (("profiles", 15, "assumed_index"), 3),
        (("profiles", 15, "actual_index"), 3),
        (("decisions", 15, "assumed_index"), 3),
        (("decisions", 15, "bound_index"), 3),
    ):
        for value in (True, float(correct), IntChild(correct), str(correct), -1, 4, 0):
            bad.append(replaced(p, path, value))
    for path in (
        ("histories", 0, "weight"),
        ("profiles", 15, "coefficients", 1, "quadratic_coefficient"),
        ("profiles", 15, "coefficients", 1, "half_linear_coefficient"),
    ):
        for value in (
            None,
            (0, 1),
            ListChild([0, 1]),
            [],
            [1],
            [0, 1, 2],
            [False, 1],
            [0, True],
            [IntChild(0), 1],
            [0, IntChild(1)],
            [0.0, 1],
            [0, 1.0],
            ["0", 1],
            [0, 0],
            [0, -1],
            [0, 2],
            [2, 4],
            [1, 1 << 4096],
            [1 << 4096, 1],
            [-(1 << 4096), 1],
        ):
            bad.append(replaced(p, path, value))
    for value in ([0, 1], [-1, 2], [2, 1], [1, 3]):
        bad.append(replaced(p, ("histories", 0, "weight"), value))
    for value in (
        None,
        (),
        ListChild(p["profiles"][15]["coefficients"]),
        [],
        p["profiles"][15]["coefficients"][:1],
        p["profiles"][15]["coefficients"] * 2,
    ):
        bad.append(replaced(p, ("profiles", 15, "coefficients"), value))
    for key, values in (
        ("quadratic_coefficient", ([-1, 1], [3, 1])),
        ("half_linear_coefficient", ([-3, 1], [3, 1])),
    ):
        for value in values:
            bad.append(replaced(p, ("profiles", 15, "coefficients", 1, key), value))
    for value in (
        None,
        [],
        DictChild(interval()),
        {**interval(), "extra": 0},
        {"kind": "unknown"},
        {"kind": StrChild("interval"), "lower": [0, 1], "upper": [1, 1]},
        {"kind": "interval", "lower": [0, 1]},
        {"kind": "interval", "lower": [1, 2], "upper": [1, 1]},
        {"kind": "interval", "lower": [0, 1], "upper": [1, 2]},
        {"kind": "interval", "lower": [0, 2], "upper": [1, 1]},
        {"kind": "point"},
        {**point(), "extra": 0},
    ):
        bad.append(replaced(p, ("decisions", 15, "policy"), value))
    for value in ([False, 1], [0.0, 1], [2, 4], (1, 2), [-1, 1], [2, 1], [1, 1 << 4096]):
        bad.append(replaced(p, ("decisions", 15, "policy"), {"kind": "point", "weight": value}))
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_schema_normalization_order_and_native_types_are_not_repaired(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def planned_caps(problem):
    c, _ = reservations(problem)
    return {
        "MAX_HISTORIES": c["histories"],
        "MAX_PROFILES": 16,
        "MAX_DECISIONS": 16,
        "MAX_WORLD_CERTIFICATES": 40,
        "MAX_ROOT_DIVISIONS": c["interior_root_candidates"],
        "MAX_STRATA": c["reserved_strata"],
        "MAX_MEMBERSHIPS": c["reserved_history_memberships"],
        "MAX_POINT_EVALUATIONS": c["reserved_point_evaluations"],
        "MAX_TOTAL_WORK": c["reserved_total_work_terms"],
    }


def test_complete_conservative_reservation_precedes_every_hook_and_executes_all_visits(
    executors, monkeypatch
):
    p = duplicate_problem()
    wanted = independent_analysis(p)
    c = wanted["counts"]
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as m:
            for name in HOOKS:
                original = getattr(module, name)

                def counted(*args, name=name, original=original, calls=calls):
                    calls[name] += 1
                    return original(*args)

                m.setattr(module, name, counted)
            assert wire(module.analyze(p)) == wire(wanted)
        assert calls == {
            "_root": c["root_divisions"],
            "_profile_term": c["profile_aggregation_terms"],
            "_evaluate": c["history_point_evaluations"]
            + c["group_point_evaluations"]
            + c["aggregate_point_evaluations"],
            "_open_sign": c["open_sign_classifications"],
            "_accumulate": c["group_accumulation_terms"],
        }

        def forbidden(*_args):
            raise RuntimeError("numeric work preceded complete reservations")

        for constant, limit in planned_caps(p).items():
            with monkeypatch.context() as m:
                m.setattr(module, constant, limit - 1)
                for name in HOOKS:
                    m.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        with monkeypatch.context() as m:
            for name in HOOKS:
                m.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(
                    replaced(
                        p, ("profiles", 15, "coefficients", 3, "half_linear_coefficient"), [2, 4]
                    )
                )
        # Deduplication would fit these execution-sized caps; reservation must still reject.
        for constant, actual in (
            ("MAX_STRATA", c["strata"]),
            ("MAX_MEMBERSHIPS", c["history_memberships"]),
            ("MAX_TOTAL_WORK", c["total_work_terms"]),
        ):
            with monkeypatch.context() as m:
                m.setattr(module, constant, actual)
                for name in HOOKS:
                    m.setattr(module, name, forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)


@pytest.mark.parametrize("constant", CAPS)
def test_every_live_cap_restores_without_cached_re_admission(executors, monkeypatch, constant):
    p = duplicate_problem()
    for module in executors:
        wanted = wire(module.analyze(p))
        with monkeypatch.context() as m:
            m.setattr(module, constant, 1)
            with pytest.raises(ValueError):
                module.analyze(p)
        assert wire(module.analyze(p)) == wanted


def mutable_ids(value):
    if type(value) not in (dict, list):
        return set()
    answer = {id(value)}
    for child in value.values() if type(value) is dict else value:
        answer |= mutable_ids(child)
    return answer


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def shared_problem():
    p = duplicate_problem()
    row = p["profiles"][0]["coefficients"][0]
    for profile in p["profiles"]:
        profile["coefficients"] = [row] * 4
    policy = interval()
    for decision in p["decisions"]:
        decision["policy"] = policy
    return p


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def test_complete_profiles_policies_groups_and_calls_are_detached(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        first, second = module.analyze(p), module.analyze(p)
        wanted = wire(second)
        assert not (mutable_ids(first) & (mutable_ids(p) | mutable_ids(second)))
        first["profiles"][0]["interval_knots"][0][0] = -1
        first["decisions"][0]["worlds"][0]["strata"][0]["groups"]["zero"]["history_indices"].clear()
        assert wire(p) == before and wire(second) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["profiles"][0]["coefficients"][0]["half_linear_coefficient"] = [0, 1]
        assert wire(detached) == wanted and wire(module.analyze(changed)) != wanted


def test_native_exact_scalar_empty_shared_depth_ascii_nodes_and_output_bytes(
    executors, monkeypatch
):
    value = {'"\\\b\f\n\r\t\x00\x1f é 🐈 \ud800': ["é", "🐈", "\udfff", -123, False, None]}
    for module in executors:
        for v in (nested(0, 128), nested([], 128)):
            module._native(v)
        for v in (nested(0, 129), nested([], 129)):
            with pytest.raises(ValueError):
                module._native(v)
        shared = [0]
        module._native([shared, nested(shared, 126)])
        with pytest.raises(ValueError):
            module._native([shared, nested(shared, 127)])
        for constant, limit in (
            ("MAX_NODES", 8),
            ("MAX_DEPTH", 2),
            ("MAX_BYTES", len(wire(value))),
        ):
            with monkeypatch.context() as m:
                m.setattr(module, constant, limit)
                module._native(value)
                m.setattr(module, constant, limit - 1)
                with pytest.raises(ValueError):
                    module._native(value)
        p = shared_problem()
        nodes, depth = tree_resources(p)
        for constant, limit in (
            ("MAX_NODES", nodes - 1),
            ("MAX_DEPTH", depth - 1),
            ("MAX_BYTES", len(wire(p)) - 1),
        ):

            def forbidden(*_args, **_kwargs):
                raise RuntimeError("unsafe tree serialized")

            with monkeypatch.context() as m:
                m.setattr(module, constant, limit)
                m.setattr(json, "dumps", forbidden)
                with pytest.raises(ValueError):
                    module.analyze(p)
        wanted = wire(module.analyze(p))
        assert len(wanted) > len(wire(p))
        with monkeypatch.context() as m:
            m.setattr(module, "MAX_BYTES", len(wanted) - 1)
            with pytest.raises(ValueError):
                module.analyze(p)
            m.setattr(module, "MAX_BYTES", len(wanted))
            assert wire(module.analyze(p)) == wanted


def graph_inputs(valid):
    cycle = []
    cycle.append(cycle)
    cycle_dict = {}
    cycle_dict["cycle"] = cycle_dict
    dag = []
    for _ in range(40):
        dag = [dag, dag]
    for value in (cycle, cycle_dict, nested([], 1500), dag):
        yield {**valid, "extra": value}
    for path in (
        ("levels",),
        ("histories",),
        ("histories", 0),
        ("histories", 0, "weight"),
        ("profiles",),
        ("profiles", 15),
        ("profiles", 15, "coefficients"),
        ("profiles", 15, "coefficients", 0, "half_linear_coefficient", 1),
        ("decisions",),
        ("decisions", 15, "policy"),
        ("decisions", 15, "policy", "lower"),
    ):
        yield replaced(valid, path, dag)


def test_generic_auditor_complete_wire_keeps_singleton_zero_polynomials_and_conservative_counts():
    audit = private_module("_qr05ae_test_generic_audit", "audit_json.py")
    for p in (mixed_problem(), duplicate_problem(), problem_of([(0, -1), (0, 1)])):
        assert wire(audit.expected_ae(p)) == wire(independent_analysis(p))


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_without_assertions(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05ae_guards",Path(sys.argv[1]))
if spec is None or spec.loader is None:raise RuntimeError("missing helpers")
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
rejections=pre=0
def require(value,message):
    if not value:raise RuntimeError(message)
def reject(call,value):
    global rejections
    try:call(value)
    except ValueError:rejections+=1
    else:raise RuntimeError("invalid input accepted")
def before_dump(call,value):
    global pre
    original=json.dumps
    def forbidden(*args,**kwargs):raise RuntimeError("unsafe tree serialized")
    json.dumps=forbidden
    try:reject(call,value);pre+=1
    finally:json.dumps=original
valid=h.shared_problem();invalid=h.invalid_problems()
for i,filename in enumerate(("safety.py","reference_qr05ae.py")):
    module=h.private_module("_qr05ae_guard_core"+str(i),filename)
    for p in (h.mixed_problem(),h.problem_of([(0,-1),(0,1)]),h.cancellation_problem()):
        require(h.wire(module.analyze(p))==h.wire(h.independent_analysis(p)),"complete generic wire")
    for bad in invalid:reject(module.analyze,bad)
    for bad in h.graph_inputs(valid):before_dump(module.analyze,bad)
    def forbidden(*args):raise RuntimeError("work preceded reservation")
    for constant,limit in h.planned_caps(valid).items():
        old=getattr(module,constant);hooks={n:getattr(module,n) for n in h.HOOKS}
        setattr(module,constant,limit-1)
        for n in hooks:setattr(module,n,forbidden)
        try:reject(module.analyze,valid)
        finally:
            setattr(module,constant,old)
            for n,v in hooks.items():setattr(module,n,v)
    for constant in h.CAPS:
        old=getattr(module,constant);setattr(module,constant,1)
        try:reject(module.analyze,valid)
        finally:setattr(module,constant,old)
    hooks={n:getattr(module,n) for n in h.HOOKS}
    for n in hooks:setattr(module,n,forbidden)
    try:reject(module.analyze,h.replaced(valid,("profiles",15,"coefficients",3,"half_linear_coefficient"),[2,4]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    d=1<<4095;p=h.problem_of([(h.F(3,d),h.F(1,d-1))],policy=h.point(0))
    require(module.analyze(p)==h.independent_analysis(p),"point0 must not form interval root")
    reject(module.analyze,h.problem_of([(h.F(3,d),h.F(1,d-1))]))
    d=(1<<4095)-1
    reject(module.analyze,h.problem_of([(0,-h.F(1,6)),(0,-h.F(1,2*d)),(0,h.F(1,6)),(0,h.F(1,2*d))],policy=h.point(1)))
    for v in (h.nested(0,128),h.nested([],128)):module._native(v)
    for v in (h.nested(0,129),h.nested([],129)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,126)]);reject(module._native,[shared,h.nested(shared,127)])
    result=module.analyze(valid);result["profiles"][0]["interval_knots"][0][0]=-1
    require(module.analyze(valid)==h.independent_analysis(valid),"ownership or restoration")
runner=h.private_module("_qr05ae_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==45,"pre-serialization inventory")
require(rejections==2*(len(invalid)+43)+19,"rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ae.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 43) + 19,
        "pre_serialization_rejections": 45,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


PINS = {
    "ad": (
        "qr-05ad-continuous-retention-2026-09-07",
        5003206,
        "099c9df18db91545fdd3a08a383e2e4ed96bf5734f6b80a9e492c3bc954c611a",
    ),
    "ac": (
        "qr-05ac-replacement-envelope-2026-09-07",
        1783649,
        "3fc5a502c214ba408e5f539133156b0ad81a2ef243545645dc980e7936932c18",
    ),
    "ab": (
        "qr-05ab-replacement-stress-2026-09-07",
        1805554,
        "7cbe2668d5b022f73207502bab214078b911e25d25a3826918b916e967643009",
    ),
    "aa": (
        "qr-05aa-uncertainty-decisions-2026-09-07",
        112206,
        "bf5661984f9df4cb111fbe97061035967de9f7516a26154abefc7d1d3a49c424",
    ),
    "z": (
        "qr-05z-fixed-attenuation-2026-09-07",
        31075315,
        "7828dafe766ae4cef9e2fd8dcc6181079fe936e8720a70367598aaf3bcbb8ccc",
    ),
    "w": (
        "qr-05w-noisy-readouts-2026-09-07",
        6756094,
        "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a",
    ),
}


def read_law(rows):
    return {tuple(atom["value"]): fraction(atom["probability"]) for atom in rows}


def law_wire(law):
    return [{"value": list(q), "probability": fw(p)} for q, p in sorted(law.items()) if p]


def outcome_risk(actual, forecast):
    assert sum(actual.values()) == sum(forecast.values()) == 1
    coordinates = actual.keys() | forecast.keys()
    return sum(
        probability * sum((forecast.get(q, F(0)) - (q == truth)) ** 2 for q in coordinates)
        for truth, probability in actual.items()
    )


def channel_joints(channel):
    return {
        (tuple(cell["value"]), tuple(atom["value"])): fraction(cell["probability"])
        * fraction(atom["probability"])
        for cell in channel["cells"]
        for atom in cell["prediction"]
    }


def marginal(joint):
    answer = {}
    for (report, future), mass in joint.items():
        key = report[:5], future
        answer[key] = answer.get(key, F(0)) + mass
    return answer


def alphabet(wsuite):
    groups = {}
    for label in wsuite["model"]["labels"]:
        q = tuple(label["question"])
        assert q[:5] == tuple(label["observation"])
        groups.setdefault(q[:5], set()).add(q)
    return [
        {"N": list(n), "values": [list(q) for q in sorted(values)]}
        for n, values in sorted(groups.items())
    ]


def frozen_maps(zcase):
    return [
        [
            {
                tuple(c["value"]): [read_law(b["forecast"]) for b in c["blends"]]
                for c in row["pairs"][12 + s]["cells"]
            }
            for s in range(4)
        ]
        for row in zcase["analysis"]["beliefs"]
    ]


def pointmass_channels(clean, letters, vector):
    """Apply one shared stochastic channel to each source outcome atom."""
    groups = {
        tuple(row["N"]): (row["values"], choice)
        for row, choice in zip(letters, vector, strict=True)
    }
    channels = []
    for level in LEVELS:
        t, joint = fraction(level), {}
        for (report, future), mass in channel_joints(clean).items():
            labels, choice = groups[report[:5]]
            for i, label in enumerate(labels):
                z = tuple(label)
                chance = (1 - t) * (z == report) + t * (i == choice)
                joint[z, future] = joint.get((z, future), F(0)) + chance * mass
        cells = []
        for z in sorted({z for (z, _), mass in joint.items() if mass}):
            law = {q: p for (r, q), p in joint.items() if r == z and p}
            mass = sum(law.values())
            cells.append(
                {
                    "value": list(z),
                    "probability": fw(mass),
                    "prediction": law_wire({q: p / mass for q, p in law.items()}),
                }
            )
        channels.append({"level": copy.deepcopy(level), "cells": cells})
    return channels


def mini_z_case():
    x, y = tuple([0] * 7), tuple([0] * 6 + [1])
    source, rows, base = [], [], []
    for bid, (weight, px) in enumerate(((F(1, 4), F(1, 4)), (F(3, 4), F(3, 4)))):
        g = {x: px, y: 1 - px}
        clean = {
            "level": [0, 1],
            "cells": [
                {"value": list(q), "probability": fw(p), "prediction": law_wire({q: F(1)})}
                for q, p in g.items()
            ],
        }
        source.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "channels": [clean],
                "fallbacks": [{"value": [0] * 5, "prediction": law_wire(g)}],
            }
        )
        cells, originals = [], []
        for q in (x, y):
            blends = [
                {
                    "retained_weight": fw(a),
                    "forecast": law_wire({r: (1 - a) * g[r] + a * (r == q) for r in g}),
                }
                for a in map(fraction, WEIGHTS)
            ]
            cells.append({"value": list(q), "blends": blends})
            originals.append(
                {"value": list(q), "coarse_forecast": law_wire(g), "forecast": law_wire({q: F(1)})}
            )
        rows.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "pairs": [copy.deepcopy({"cells": cells}) for _ in range(16)],
            }
        )
        base.append(
            {
                "belief_id": bid,
                "weight": fw(weight),
                "pairs": [copy.deepcopy({"cells": originals}) for _ in range(16)],
            }
        )
    return {
        "case_id": "generic-two-history",
        "problem": {"experiment": {"beliefs": source}},
        "analysis": {"beliefs": rows, "baseline": {"beliefs": base}},
    }


@pytest.fixture(scope="session")
def pinned():
    answer = {}
    for name, (directory, size, sha) in PINS.items():
        path = HERE.parent / directory / "results.json"
        assert path.is_file() and not path.is_symlink()
        raw = path.read_bytes()
        assert len(raw) == size and hashlib.sha256(raw).hexdigest() == sha
        envelope = json.loads(raw)
        assert (
            json.dumps(envelope, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
        ).encode() == raw
        native(envelope["suite"])
        answer[name] = envelope["suite"]
    return answer


PRODUCER_CONTROLS = dict.fromkeys(
    (
        "AD_baseline_preserved",
        "original_history_weights",
        "common_witness_and_policy_preserved",
        "complete_conditional_history_coefficients",
        "coefficients_aggregate_to_AD_world_polynomials",
        "literal_history_point_scores",
        "complete_history_sign_partitions",
        "interval_policies_not_point_selected",
        "harm_benefit_cancellation_visible",
        "case_average_certificates_recovered",
        "no_historywise_weight_or_mechanism_selection",
    ),
    True,
)
PRODUCER_CONTROLS.update(
    origin_authenticated_by_generic_API=False,
    all_replacement_mechanisms_audited=False,
    historywise_robustness_established=False,
    raw_history_reconstruction_performed_by_this_runner=False,
)


def conditional_profiles(adcase, zcase):
    """Expand literal indicator coordinates without multiplying original history weights."""
    sources = zcase["problem"]["experiment"]["beliefs"]
    maps = frozen_maps(zcase)
    histories = [
        {"belief_id": b["belief_id"], "weight": copy.deepcopy(b["weight"])} for b in sources
    ]
    assert [b["belief_id"] for b in histories] == list(range(len(histories)))
    profiles = []
    for s in range(4):
        links = adcase["witness_certificate_map"][4 * s : 4 * s + 4]
        wid = links[0]["witness_id"]
        assert all(row["witness_id"] == wid for row in links)
        actuals = adcase["witness_laws"][wid]["beliefs"]
        for t in range(4):
            rows = []
            for source, actual, models in zip(sources, actuals, maps, strict=True):
                assert (
                    source["belief_id"] == actual["belief_id"]
                    and source["weight"] == actual["weight"]
                )
                assert actual["channels"][t]["level"] == LEVELS[t]
                joint = channel_joints(actual["channels"][t])
                assert sum(joint.values()) == 1
                original = channel_joints(source["channels"][0])
                assert marginal(joint) == marginal(original)
                if t == 0:
                    assert joint == original
                a = b = F(0)
                for (report, truth), mass in joint.items():
                    g, _, f = models[s][report]
                    for q in g.keys() | f.keys() | {truth}:
                        delta = f.get(q, F(0)) - g.get(q, F(0))
                        a += mass * delta * delta
                        b += mass * ((q == truth) - g.get(q, F(0))) * delta
                rows.append(poly(a, b))
            profiles.append({"assumed_index": s, "actual_index": t, "coefficients": rows})
    return histories, profiles


def project_case(adcase, zcase):
    histories, profiles = conditional_profiles(adcase, zcase)
    assert adcase["case_id"] == zcase["case_id"]
    return {
        "case_id": adcase["case_id"],
        "baseline": copy.deepcopy(adcase),
        "problem": {
            "schema_version": "det8-qr05ae-problem-v1",
            "family": "qr05ae_history_safety",
            "levels": copy.deepcopy(LEVELS),
            "histories": histories,
            "profiles": profiles,
            "decisions": [
                {
                    "assumed_index": row["assumed_index"],
                    "bound_index": row["bound_index"],
                    "policy": copy.deepcopy(row["optimizer"]),
                }
                for row in adcase["analysis"]["decisions"]
            ],
        },
    }


def literal_history_scores(adcase, zcase, s, t, x):
    wid = adcase["witness_certificate_map"][4 * s]["witness_id"]
    values = []
    for actual, models in zip(
        adcase["witness_laws"][wid]["beliefs"], frozen_maps(zcase), strict=True
    ):
        total = F(0)
        for cell in actual["channels"][t]["cells"]:
            g, _, f = models[s][tuple(cell["value"])]
            h = {q: (1 - x) * g.get(q, F(0)) + x * f.get(q, F(0)) for q in g.keys() | f.keys()}
            truth = read_law(cell["prediction"])
            total += fraction(cell["probability"]) * (
                outcome_risk(truth, h) - outcome_risk(truth, g)
            )
        assert -2 <= total <= 2
        values.append(total)
    return values


def mini_ad_case(zcase, letters, vector=(1,)):
    sources = zcase["problem"]["experiment"]["beliefs"]
    return {
        "case_id": zcase["case_id"],
        "witness_certificate_map": [
            {"assumed_index": s, "bound_index": u, "witness_id": 0}
            for s in range(4)
            for u in range(4)
        ],
        "witness_laws": [
            {
                "witness_id": 0,
                "label_indices": list(vector),
                "beliefs": [
                    {
                        "belief_id": b["belief_id"],
                        "weight": copy.deepcopy(b["weight"]),
                        "channels": pointmass_channels(b["channels"][0], letters, vector),
                    }
                    for b in sources
                ],
            }
        ],
    }


def test_conditional_source_coefficients_do_not_double_weight_or_choose_historywise_mechanisms(
    runner,
):
    z = mini_z_case()
    letters = [{"N": [0] * 5, "values": [[0] * 7, [0] * 6 + [1]]}]
    ad = mini_ad_case(z, letters)
    histories, profiles = conditional_profiles(ad, z)
    assert runner.conditional_profiles(ad, z) == (histories, profiles)
    assert profiles[0]["coefficients"] == [poly(F(3, 8), F(3, 8))] * 2
    assert profiles[3]["coefficients"] == [poly(F(1, 8), 0), poly(F(9, 8), 0)]
    assert [h["weight"] for h in histories] == [[1, 4], [3, 4]]
    # The same global label has unequal conditional risks; neither max9/8 nor
    # a second factor of history weight may replace these profile rows.
    assert sum(
        fraction(h["weight"]) * coefficients(r)[0]
        for h, r in zip(histories, profiles[3]["coefficients"], strict=True)
    ) == F(7, 8)
    values = literal_history_scores(ad, z, 0, 1, F(3, 10))
    assert values == [-9 * F(1, 100), -9 * F(1, 200)]
    assert runner.literal_history_scores(ad, z, 0, 1, F(3, 10)) == values
    changed = copy.deepcopy(z)
    for b in changed["problem"]["experiment"]["beliefs"]:
        b["weight"] = [1, 2]
    changed_ad = mini_ad_case(changed, letters)
    new_histories, new_profiles = conditional_profiles(changed_ad, changed)
    assert new_profiles == profiles and new_histories != histories
    assert runner.conditional_profiles(changed_ad, changed) == (new_histories, profiles)


@pytest.fixture(scope="session")
def letters(pinned):
    return alphabet(pinned["w"])


@pytest.fixture(scope="session")
def projected(pinned):
    return [
        project_case(ad, z)
        for ad, z in zip(pinned["ad"]["cases"], pinned["z"]["cases"], strict=True)
    ]


@pytest.fixture(scope="session")
def expected(projected):
    return [independent_analysis(case["problem"]) for case in projected]


@pytest.mark.parametrize("case_index", range(6))
def test_fixed_complete_six_wires_and_unweighted_conditional_literal_source_coefficients(
    executors, runner, pinned, projected, expected, case_index
):
    i = case_index
    assert wire(runner.project_case(pinned["ad"]["cases"][i], pinned["z"]["cases"][i])) == wire(
        projected[i]
    )
    p = projected[i]["problem"]
    before = wire(p)
    for module in executors:
        assert wire(module.analyze(p)) == wire(expected[i])
        assert wire(p) == before
    assert wire(runner.expected_analysis(p)) == wire(expected[i])
    assert wire(projected[i]["baseline"]) == wire(pinned["ad"]["cases"][i])


def test_fixed_all_common_witness_laws_rebuilt_and_weighted_profiles_recover_every_AD_world(
    pinned, projected, expected, letters
):
    for ad, z, p, a in zip(
        pinned["ad"]["cases"], pinned["z"]["cases"], projected, expected, strict=True
    ):
        for witness in ad["witness_laws"]:
            for source, actual in zip(
                z["problem"]["experiment"]["beliefs"], witness["beliefs"], strict=True
            ):
                assert actual["channels"] == pointmass_channels(
                    source["channels"][0], letters, witness["label_indices"]
                )
        weights = [fraction(h["weight"]) for h in p["problem"]["histories"]]
        for pi, (profile, result) in enumerate(
            zip(p["problem"]["profiles"], a["profiles"], strict=True)
        ):
            rows = list(map(coefficients, profile["coefficients"]))
            total = poly(
                *(sum(w * r[j] for w, r in zip(weights, rows, strict=True)) for j in (0, 1))
            )
            s, t = divmod(pi, 4)
            old = ad["world_certificates"][4 * s + 3]["polynomials"][t]
            assert result["aggregate_polynomial"] == total == {k: old[k] for k in total}
        for decision, old in zip(a["decisions"], ad["world_certificates"], strict=True):
            assert decision["policy"] == old["optimizer"]
            if decision["policy"]["kind"] == "point":
                values = [
                    w["strata"][0]["point_values"]["aggregate_excess"] for w in decision["worlds"]
                ]
                assert values == old["point_world_excesses"]
                assert fw(max(map(fraction, values))) == old["upper_bound_value"]
            else:
                for world in decision["worlds"]:
                    qa, qb = coefficients(
                        a["profiles"][world["profile_index"]]["aggregate_polynomial"]
                    )
                    assert qa >= 0 and qa - 2 * qb <= 0
                    if world["actual_index"] == decision["bound_index"]:
                        assert qa == qb == 0


def test_fixed_every_unique_history_point_boundary_is_literally_scored_without_policy_selection(
    runner, pinned, projected, expected
):
    for ad, z, case, analysis in zip(
        pinned["ad"]["cases"], pinned["z"]["cases"], projected, expected, strict=True
    ):
        history_weights = [fraction(h["weight"]) for h in case["problem"]["histories"]]
        scored = {}
        for decision in analysis["decisions"]:
            s = decision["assumed_index"]
            for world in decision["worlds"]:
                t = world["actual_index"]
                for stratum in world["strata"]:
                    if stratum["region"]["kind"] == "open_interval":
                        assert stratum["point_values"] is None
                        continue
                    x = fraction(stratum["region"]["weight"])
                    key = s, t, x
                    if key not in scored:
                        scored[key] = literal_history_scores(ad, z, s, t, x)
                        assert runner.literal_history_scores(ad, z, s, t, x) == scored[key]
                    values = scored[key]
                    point_values = stratum["point_values"]
                    assert list(map(fw, values)) == point_values["history_excesses"]
                    assert (
                        fw(sum(w * v for w, v in zip(history_weights, values, strict=True)))
                        == point_values["aggregate_excess"]
                    )
                    for name, sign in zip(GROUPS, (1, -1, 0), strict=True):
                        indices = [
                            i for i, value in enumerate(values) if (value > 0) - (value < 0) == sign
                        ]
                        group = stratum["groups"][name]
                        assert group["history_indices"] == indices
                        assert group["likelihood_mass"] == fw(
                            sum(history_weights[i] for i in indices)
                        )
                        assert point_values[name + "_contribution"] == fw(
                            sum(history_weights[i] * values[i] for i in indices)
                        )


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_complete_suite_preserves_entire_AD_baseline_controls_case_links_and_nonpooled_inventory(
    aggregate, projected, expected
):
    totals = {"cases": 6, "analyze_calls": 12, "invalid_analyze_calls_rejected": 16}
    totals.update({key: sum(a["counts"][key] for a in expected) for key in expected[0]["counts"]})
    wanted = {
        "producer": {
            "artifact": PINS["ad"][0] + "/results.json",
            "bytes": PINS["ad"][1],
            "sha256": PINS["ad"][2],
        },
        "cases": [
            {**p, "analysis": a, "producer_controls": PRODUCER_CONTROLS}
            for p, a in zip(projected, expected, strict=True)
        ],
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 16,
            "raw_laws_or_prior_artifacts_given_to_core": False,
            "policy_reoptimized": False,
            "mechanism_reoptimized_per_history": False,
            "interval_representative_selected": False,
            "whole_replacement_class_audited": False,
        },
        "totals": totals,
    }
    assert wire(aggregate) == wire(wanted)


def test_max_history_boundary_and_default_duplicate_reservation_rejection(executors, monkeypatch):
    p = problem_of([(0, 0)] * 128, policy=point(0))
    wanted = wire(independent_analysis(p))
    duplicate = problem_of([(2, F(1, 2))] * 64)
    counts, _ = reservations(duplicate)
    assert counts["reserved_strata"] == 5240
    # The deduplicated execution would have200 strata; default4096 reservation rejects.
    for module in executors:
        assert wire(module.analyze(p)) == wanted
        with pytest.raises(ValueError):
            module.analyze(problem_of([(0, 0)] * 129, policy=point(0)))

        def forbidden(*_args):
            raise RuntimeError("default duplicate reservation bypassed")

        with monkeypatch.context() as m:
            for name in HOOKS:
                m.setattr(module, name, forbidden)
            with pytest.raises(ValueError):
                module.analyze(duplicate)


def test_oversized_string_key_and_width_fail_before_whole_serialization(executors, monkeypatch):
    p = problem_of()

    def forbidden(*_args, **_kwargs):
        raise RuntimeError("oversized native payload serialized")

    # Lower live caps keep this admission-boundary fixture small.
    for module in executors:
        with monkeypatch.context() as m:
            m.setattr(module, "MAX_BYTES", 4096)
            m.setattr(module, "MAX_NODES", 4096)
            m.setattr(json, "dumps", forbidden)
            for bad in (
                {**p, "extra": "é" * 4096},
                {**p, "x" * 4096: 0},
                {**p, "extra": [None] * 4096},
            ):
                with pytest.raises(ValueError):
                    module.analyze(bad)


def output_corruptions(analysis):
    ip = next(i for i, p in enumerate(analysis["profiles"]) if p["interval_knots"] is not None)
    di = next(i for i, d in enumerate(analysis["decisions"]) if d["policy"]["kind"] == "point")
    decision = analysis["decisions"][di]
    st = decision["worlds"][0]["strata"][0]
    point_path = ("decisions", di, "worlds", 0, "strata", 0)
    x = fraction(st["region"]["weight"])
    paths = [
        (("input_sha256",), "0" * 64),
        (("histories", 0, "belief_id"), False),
        (
            ("profiles", 0, "aggregate_polynomial", "quadratic_coefficient"),
            fw(coefficients(analysis["profiles"][0]["aggregate_polynomial"])[0] + 1),
        ),
        (("profiles", ip, "interval_root_records"), [{"history_index": 0, "weight": [1, 2]}]),
        (("profiles", ip, "interval_knots"), analysis["profiles"][ip]["interval_knots"][::-1]),
        (("decisions", di, "policy"), interval()),
        (
            ("decisions", di, "harm_possible_world_indices"),
            [0] if not decision["harm_possible_world_indices"] else [],
        ),
        (("decisions", di, "worlds"), []),
        ((*point_path, "region", "weight"), fw(1 - x) if x != F(1, 2) else [0, 1]),
        ((*point_path, "groups", "positive", "history_indices"), [len(analysis["histories"])]),
        (
            (*point_path, "groups", "positive", "likelihood_mass"),
            fw(fraction(st["groups"]["positive"]["likelihood_mass"]) + 1),
        ),
        (
            (*point_path, "groups", "zero", "polynomial", "half_linear_coefficient"),
            fw(coefficients(st["groups"]["zero"]["polynomial"])[1] + 1),
        ),
        (
            (*point_path, "point_values", "history_excesses", 0),
            fw(fraction(st["point_values"]["history_excesses"][0]) + 1),
        ),
        (
            (*point_path, "point_values", "negative_contribution"),
            fw(fraction(st["point_values"]["negative_contribution"]) - 1),
        ),
        ((*point_path, "checks", "weighted_polynomial_decomposition"), False),
        (
            ("counts", "reserved_total_work_terms"),
            analysis["counts"]["reserved_total_work_terms"] + 1,
        ),
    ]
    return [replaced(analysis, path, value) for path, value in paths]


def test_fixed_complete_output_mutations_are_nonvacuous_and_cannot_preserve_empty_harm_by_default(
    runner, pinned, expected, letters, monkeypatch
):
    i = next(
        i
        for i, a in enumerate(expected)
        if a["counts"]["point_world_certificates"] and a["counts"]["interval_world_certificates"]
    )
    ad, z, ac, aa, ab = (pinned[k]["cases"][i] for k in ("ad", "z", "ac", "aa", "ab"))
    # Full baseline authentication is exercised by the complete run_suite test.
    # Only that costly prior chain is bypassed for the bounded new-output mutations.
    monkeypatch.setattr(runner, "verify_ad_case", lambda *_args: None)
    for changed in output_corruptions(expected[i]):
        assert wire(changed) != wire(expected[i])
        with pytest.raises(ValueError):
            runner.check_analysis(changed, ad, z, ac, aa, ab, letters)


def case_corruptions(case):
    p = case["problem"]
    old = case["baseline"]["prior_certificates"][0]["candidates"][0]["worst_excess"]
    return [
        replaced(case, ("case_id",), case["case_id"] + "-corrupted"),
        replaced(case, ("problem", "histories", 0, "weight"), [0, 1]),
        replaced(
            case,
            ("problem", "profiles", 0, "coefficients", 0, "quadratic_coefficient"),
            fw(coefficients(p["profiles"][0]["coefficients"][0])[0] + 1),
        ),
        replaced(
            case,
            ("baseline", "prior_certificates", 0, "candidates", 0, "worst_excess"),
            fw(fraction(old) + 1),
        ),
        replaced(case, ("producer_controls", "historywise_robustness_established"), True),
    ]


def test_fixed_check_case_authenticates_complete_baseline_input_case_link_and_claim_boundary(
    runner, pinned, projected, expected, letters, monkeypatch
):
    i = 0
    case = {**projected[i], "analysis": expected[i], "producer_controls": PRODUCER_CONTROLS}
    ad, z, ac, aa, ab = (pinned[k]["cases"][i] for k in ("ad", "z", "ac", "aa", "ab"))
    monkeypatch.setattr(runner, "verify_ad_case", lambda *_args: None)
    for changed in case_corruptions(case):
        assert wire(changed) != wire(case)
        with pytest.raises(ValueError):
            runner.check_case(changed, ad, z, ac, aa, ab, letters)


def test_fixed_producer_weights_frozen_forecasts_witness_laws_policy_and_AD_coefficients_are_checked(
    runner, pinned, expected, letters, monkeypatch
):
    i = next(i for i, a in enumerate(expected) if a["counts"]["point_world_certificates"])
    ad, z, ac, aa, ab = (pinned[k]["cases"][i] for k in ("ad", "z", "ac", "aa", "ab"))
    di = next(
        i
        for i, row in enumerate(ad["analysis"]["decisions"])
        if row["optimizer"]["kind"] == "point"
    )
    monkeypatch.setattr(runner, "verify_ad_case", lambda *_args: None)
    changes = [
        (ad, replaced(ad, ("witness_laws", 0, "beliefs", 0, "weight"), [0, 1]), "ad"),
        (
            ad,
            replaced(
                ad,
                ("witness_laws", 0, "beliefs", 0, "channels", 0, "cells", 0, "probability"),
                [0, 1],
            ),
            "ad",
        ),
        (ad, replaced(ad, ("analysis", "decisions", di, "optimizer"), interval()), "ad"),
        (
            ad,
            replaced(
                ad,
                ("world_certificates", 3, "polynomials", 0, "quadratic_coefficient"),
                fw(
                    fraction(ad["world_certificates"][3]["polynomials"][0]["quadratic_coefficient"])
                    + 1
                ),
            ),
            "ad",
        ),
        (z, replaced(z, ("problem", "experiment", "beliefs", 0, "weight"), [0, 1]), "z"),
        (
            z,
            replaced(
                z,
                (
                    "analysis",
                    "beliefs",
                    0,
                    "pairs",
                    12,
                    "cells",
                    0,
                    "blends",
                    2,
                    "forecast",
                    0,
                    "probability",
                ),
                [0, 1],
            ),
            "z",
        ),
    ]
    for original, changed, kind in changes:
        assert wire(changed) != wire(original)
        with pytest.raises(ValueError):
            runner.check_analysis(
                expected[i],
                changed if kind == "ad" else ad,
                changed if kind == "z" else z,
                ac,
                aa,
                ab,
                letters,
            )
