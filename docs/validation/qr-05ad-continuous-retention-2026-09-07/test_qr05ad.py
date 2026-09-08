"""Independent convex-quadratic and complete forecast-family verification.

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


CHECKS = (
    "convexity",
    "critical_candidates_complete",
    "optimizer_set_complete",
    "global_kkt_certificate",
    "finite_menu_complete",
    "finite_menu_argmin_complete",
    "finite_menu_gap_nonnegative",
    "menu_grid_error_bound",
    "coarse_option_available",
)
CAPS = (
    "MAX_BITS",
    "MAX_DEPTH",
    "MAX_NODES",
    "MAX_BYTES",
    "MAX_DECISIONS",
    "MAX_CRITICAL_POINTS",
    "MAX_VALUE_EVALUATIONS",
    "MAX_TOTAL_WORK",
)
HOOKS = ("_stationary", "_coefficients", "_gradient", "_evaluate", "_gap")


def problem_of(a=2, b=1):
    return {
        "schema_version": "det8-qr05ad-problem-v1",
        "family": "qr05ad_continuous_retention",
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "decisions": [
            {
                "assumed_index": s,
                "bound_index": u,
                "quadratic_coefficient": fw(a),
                "half_linear_coefficient": fw(b),
            }
            for s in range(4)
            for u in range(4)
        ],
    }


def mixed_problem():
    p = problem_of()
    values = [
        (0, 0),
        (0, 2),
        (0, -2),
        (2, 0),
        (2, 2),
        (1, 2),
        (1, -1),
        (2, F(1, 2)),
        (2, F(3, 2)),
        (2, 1),
        (F(2, 3), F(1, 5)),
        (F(1, 7), F(1, 7)),
        (0, F(1, 2**64)),
        (0, -F(1, 2**64)),
        (2, -2),
        (1, F(1, 4)),
    ]
    for row, (a, b) in zip(p["decisions"], values, strict=True):
        row["quadratic_coefficient"], row["half_linear_coefficient"] = fw(a), fw(b)
    return p


def work_counts(problem):
    pairs = [
        (fraction(r["quadratic_coefficient"]), fraction(r["half_linear_coefficient"]))
        for r in problem["decisions"]
    ]
    i = sum(0 < b < a for a, b in pairs)
    p = sum(a != 0 or b != 0 for a, b in pairs)
    c = 32 + i
    return {
        "optimizer_classifications": 16,
        "coefficient_visits": 16,
        "gradient_terms": p,
        "stationary_divisions": i,
        "critical_value_terms": c,
        "menu_value_terms": 48,
        "critical_selection_visits": c,
        "menu_selection_visits": 48,
        "gap_terms": 64,
        "total_work_terms": 192 + p + i + 2 * c,
    }


def independent_analysis(problem):
    """Finite critical-value enumeration, with polynomial/KKT set certificates."""
    answers = []
    lower = upper = ties = 0
    for row in problem["decisions"]:
        a, b = fraction(row["quadratic_coefficient"]), fraction(row["half_linear_coefficient"])
        candidates = [F(0), F(1)]
        if 0 < b < a:
            candidates.append(b / a)
        candidates.sort()
        # The oracle does not use the engines' clipped-ratio classification.
        values = [sum((a * x * x, -b * x, -b * x)) for x in candidates]
        minimum = min(values)
        minimizers = [x for x, value in zip(candidates, values, strict=True) if value == minimum]
        if a == b == 0:
            optimizer = {"kind": "interval", "lower": [0, 1], "upper": [1, 1]}
            proof = {
                "kind": "zero_polynomial",
                "anchor": None,
                "gradient": None,
                "second_derivative": [0, 1],
            }
        else:
            assert len(minimizers) == 1
            x = minimizers[0]
            lower += x == 0
            upper += x == 1
            gradient = 2 * a * x - 2 * b
            assert (x == 0 and gradient >= 0) or (x == 1 and gradient <= 0) or gradient == 0
            # Match all coefficients of Q(y)-Q(x), not merely sampled values.
            assert [a, -2 * b, -minimum] == [a, gradient - 2 * a * x, a * x * x - gradient * x]
            optimizer = {"kind": "point", "weight": fw(x)}
            proof = {
                "kind": "point_kkt",
                "anchor": fw(x),
                "gradient": fw(gradient),
                "second_derivative": fw(2 * a),
            }
        menu = [a * x * x - 2 * b * x for x in map(fraction, WEIGHTS)]
        menu_min = min(menu)
        indices = [i for i, value in enumerate(menu) if value == menu_min]
        ties += len(indices)
        gap = menu_min - minimum
        assert 0 <= gap <= F(1, 8) and 16 * gap <= a
        answers.append(
            {
                **copy.deepcopy(row),
                "linear_coefficient": fw(-2 * b),
                "critical_candidates": [
                    {"retained_weight": fw(x), "value": fw(v)}
                    for x, v in zip(candidates, values, strict=True)
                ],
                "optimizer": optimizer,
                "minimum": fw(minimum),
                "finite_menu": [
                    {
                        "retained_weight": copy.deepcopy(w),
                        "value": fw(v),
                        "excess_over_minimum": fw(v - minimum),
                    }
                    for w, v in zip(WEIGHTS, menu, strict=True)
                ],
                "finite_menu_minimum": fw(menu_min),
                "finite_menu_minimizer_indices": indices,
                "finite_menu_minimizer_weights": [copy.deepcopy(WEIGHTS[i]) for i in indices],
                "finite_menu_gap": fw(gap),
                "proof": proof,
                "checks": dict.fromkeys(CHECKS, True),
            }
        )
    work = work_counts(problem)
    return {
        "input_sha256": digest(problem),
        "levels": copy.deepcopy(LEVELS),
        "retained_weights": copy.deepcopy(WEIGHTS),
        "decisions": answers,
        "counts": {
            "decisions": 16,
            "critical_candidates": work["critical_value_terms"],
            "value_evaluations": work["critical_value_terms"] + 48,
            "point_optimizers": work["gradient_terms"],
            "interval_optimizers": 16 - work["gradient_terms"],
            "interior_point_optimizers": work["stationary_divisions"],
            "lower_endpoint_optimizers": lower,
            "upper_endpoint_optimizers": upper,
            "finite_menu_minimizer_occurrences": ties,
            **work,
        },
    }


@pytest.fixture(scope="session")
def executors():
    return (
        private_module("_qr05ad_test_primary", "retention.py"),
        private_module("_qr05ad_test_reference", "reference_qr05ad.py"),
    )


@pytest.fixture(scope="session")
def runner():
    return private_module("_qr05ad_test_runner", "study.py")


@pytest.mark.parametrize(
    "a,b",
    [
        (0, 0),
        (0, 2),
        (0, -2),
        (2, 0),
        (2, 2),
        (1, 2),
        (2, -2),
        (2, F(1, 2)),
        (2, F(3, 2)),
        (2, 1),
        (F(2, 3), F(1, 5)),
        (0, F(1, 2**64)),
        (0, -F(1, 2**64)),
    ],
)
def test_generic_complete_wire_and_convex_optimizer_sets(executors, a, b):
    p = problem_of(a, b)
    wanted = wire(independent_analysis(p))
    for module in executors:
        assert wire(module.analyze(p)) == wanted


def test_mixed_rows_preserve_order_and_global_not_per_world_or_menu_only_choices(executors):
    p = mixed_problem()
    for module in executors:
        answer = module.analyze(p)
        assert wire(answer) == wire(independent_analysis(p))
        assert answer["decisions"][0]["optimizer"]["kind"] == "interval"
        assert answer["decisions"][3]["optimizer"] == {"kind": "point", "weight": [0, 1]}
        assert answer["decisions"][4]["optimizer"] == {"kind": "point", "weight": [1, 1]}
        assert answer["decisions"][7]["finite_menu_minimizer_indices"] == [0, 1]
        assert answer["decisions"][8]["finite_menu_minimizer_indices"] == [1, 2]
        assert answer["decisions"][7]["finite_menu_gap"] == [1, 8]
        assert answer["decisions"][8]["finite_menu_gap"] == [1, 8]
        assert answer["decisions"][9]["critical_candidates"][0]["value"] == [0, 1]
        assert answer["decisions"][9]["critical_candidates"][-1]["value"] == [0, 1]
        assert answer["decisions"][9]["finite_menu_minimizer_indices"] == [1]
        assert answer["decisions"][14]["finite_menu"][-1]["value"] == [6, 1]


def test_only_isolated_interior_stationary_ratios_are_formed(executors, monkeypatch):
    p = mixed_problem()
    p["decisions"] = [
        dict(r, quadratic_coefficient=[0, 1], half_linear_coefficient=[2, 1])
        for r in p["decisions"]
    ]

    def forbidden(*_args):
        raise RuntimeError("outside stationary ratio was formed")

    for module in executors:
        with monkeypatch.context() as m:
            m.setattr(module, "_stationary", forbidden)
            assert wire(module.analyze(p)) == wire(independent_analysis(p))


def overflow_problem(kind):
    if kind == "stationary":
        d = 1 << 4095
        return problem_of(F(3, d), F(1, d - 1))
    if kind == "minimum_gap":
        d = 1 << 4094
        return problem_of(F(4, d), F(1, d))
    if kind == "linear_gradient":
        d = (1 << 4095) - 5
        return problem_of(F(8, d), -F(2 * d - 1, d))
    if kind == "curvature":
        d = (1 << 4095) - 1
        return problem_of(F(2 * d - 1, d), 0)
    raise AssertionError(kind)


@pytest.mark.parametrize("kind", ["stationary", "minimum_gap", "linear_gradient", "curvature"])
def test_retained_ratio_value_gap_and_coefficients_overflow_without_rounding(executors, kind):
    p = overflow_problem(kind)
    for row in p["decisions"]:
        a, b = fraction(row["quadratic_coefficient"]), fraction(row["half_linear_coefficient"])
        assert 0 <= a <= 2 and -2 <= b <= 2
    if kind == "minimum_gap":
        assert b / a == F(1, 4)
        for x in map(fraction, WEIGHTS):
            fraction(fw(a * x * x - 2 * b * x))
        assert (-b * b / a).denominator.bit_length() == 4097
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(p)


def test_unretained_large_products_cancel_and_all_retained_outputs_fit(executors):
    d = 1 << 4094
    p = problem_of(F(2, d), F(1, d))
    assert (F(1, d) ** 2).denominator.bit_length() > 4096
    wanted = independent_analysis(p)
    native(wanted)
    assert wanted["decisions"][0]["minimum"] == fw(-F(1, 2 * d))
    for module in executors:
        assert wire(module.analyze(p)) == wire(wanted)


def test_direct_retained_gap_guard_and_signed_gradient_extremes(executors):
    for module in executors:
        assert module._gradient(F(2), F(-2), F(1)) == 8
        assert module._gradient(F(0), F(2), F(1)) == -4
        with pytest.raises(ValueError):
            module._gap(F(1, 3), -F(1, 1 << 4095))


class IntChild(int):
    pass


class StrChild(str):
    pass


class ListChild(list):
    pass


class DictChild(dict):
    pass


def invalid_problems():
    p = mixed_problem()
    bad = [None, [], (), DictChild(p), {**p, "extra": 0}, {**p, 1: 0}]
    for key in p:
        bad.append({k: v for k, v in p.items() if k != key})
    for key in ("schema_version", "family"):
        for value in (None, "wrong", StrChild(p[key]), True):
            bad.append(replaced(p, (key,), value))
    for key in ("levels", "retained_weights"):
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
            bad.append(replaced(p, (key, 0), value))
    for value in (
        None,
        tuple(p["decisions"]),
        ListChild(p["decisions"]),
        [],
        p["decisions"][:-1],
        p["decisions"] + p["decisions"][:1],
        p["decisions"][::-1],
    ):
        bad.append(replaced(p, ("decisions",), value))
    row = p["decisions"][15]
    for value in (None, [], DictChild(row), {**row, "extra": 0}):
        bad.append(replaced(p, ("decisions", 15), value))
    for key in row:
        bad.append(replaced(p, ("decisions", 15), {k: v for k, v in row.items() if k != key}))
    for key in ("assumed_index", "bound_index"):
        for value in (True, 3.0, IntChild(3), "3", -1, 4, 0):
            bad.append(replaced(p, ("decisions", 15, key), value))
    for key in ("quadratic_coefficient", "half_linear_coefficient"):
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
            bad.append(replaced(p, ("decisions", 15, key), value))
    for value in ([-1, 1], [3, 1]):
        bad.append(replaced(p, ("decisions", 15, "quadratic_coefficient"), value))
    for value in ([-3, 1], [3, 1]):
        bad.append(replaced(p, ("decisions", 15, "half_linear_coefficient"), value))
    return bad


@pytest.mark.parametrize("index", range(len(invalid_problems())))
def test_exact_schema_rejects_without_coercion_reordering_defaults_or_reduction(executors, index):
    for module in executors:
        with pytest.raises(ValueError):
            module.analyze(invalid_problems()[index])


def planned_caps(problem):
    work = work_counts(problem)
    return {
        "MAX_DECISIONS": 16,
        "MAX_CRITICAL_POINTS": work["critical_value_terms"],
        "MAX_VALUE_EVALUATIONS": work["critical_value_terms"] + 48,
        "MAX_TOTAL_WORK": work["total_work_terms"],
    }


def test_every_declared_visit_and_hook_executes_after_complete_reservation(executors, monkeypatch):
    p = mixed_problem()
    work = work_counts(p)
    for module in executors:
        calls = dict.fromkeys(HOOKS, 0)
        with monkeypatch.context() as m:
            for name in HOOKS:
                original = getattr(module, name)

                def counted(*args, name=name, original=original, calls=calls):
                    calls[name] += 1
                    return original(*args)

                m.setattr(module, name, counted)
            answer = module.analyze(p)
        assert wire(answer) == wire(independent_analysis(p))
        assert calls == {
            "_stationary": work["stationary_divisions"],
            "_coefficients": 16,
            "_gradient": work["gradient_terms"],
            "_evaluate": work["critical_value_terms"] + 48,
            "_gap": 64,
        }

        def forbidden(*_args):
            raise RuntimeError("numeric work preceded complete planning")

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
                module.analyze(replaced(p, ("decisions", 15, "half_linear_coefficient"), [2, 4]))


@pytest.mark.parametrize("constant", CAPS)
def test_live_caps_restore_without_cross_call_cache(executors, monkeypatch, constant):
    p = mixed_problem()
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
    result = {id(value)}
    for child in value.values() if type(value) is dict else value:
        result |= mutable_ids(child)
    return result


def nested(value, wrappers):
    for _ in range(wrappers):
        value = [value]
    return value


def shared_problem():
    p = problem_of()
    for row in p["decisions"]:
        row["quadratic_coefficient"] = p["decisions"][0]["quadratic_coefficient"]
    return p


def tree_resources(value, depth=0):
    nodes, maximum = 1, depth
    if type(value) in (dict, list):
        for child in value.values() if type(value) is dict else value:
            count, height = tree_resources(child, depth + 1)
            nodes += count
            maximum = max(maximum, height)
    return nodes, maximum


def test_outputs_are_detached_across_input_aliases_calls_and_mutations(executors):
    p = shared_problem()
    before = wire(p)
    for module in executors:
        first, second = module.analyze(p), module.analyze(p)
        wanted = wire(second)
        assert not (mutable_ids(first) & (mutable_ids(p) | mutable_ids(second)))
        first["decisions"][0]["optimizer"]["weight"][0] = -1
        first["decisions"][0]["finite_menu"].clear()
        assert wire(p) == before and wire(second) == wanted
        assert wire(module.analyze(p)) == wanted
        changed = copy.deepcopy(p)
        detached = module.analyze(changed)
        changed["decisions"][0]["half_linear_coefficient"] = [0, 1]
        assert wire(detached) == wanted and wire(module.analyze(changed)) != wanted


def test_exact_native_depth_scalar_empty_shared_ascii_nodes_and_output_bytes(
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
                raise RuntimeError("unsafe tree reached whole serialization")

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
        ("levels", 0),
        ("levels", 0, 0),
        ("retained_weights",),
        ("decisions",),
        ("decisions", 15),
        ("decisions", 15, "assumed_index"),
        ("decisions", 15, "quadratic_coefficient"),
        ("decisions", 15, "half_linear_coefficient", 1),
    ):
        yield replaced(valid, path, dag)


def test_generic_auditor_complete_wire_includes_interval_ties_proofs_and_counts():
    audit = private_module("_qr05ad_test_generic_audit", "audit_json.py")
    for p in (mixed_problem(), problem_of(0, 0), problem_of(2, F(1, 2))):
        assert wire(audit.expected_ad(p)) == wire(independent_analysis(p))


@pytest.mark.parametrize("optimized", [False, True])
def test_explicit_guard_subprocess_checks_survive_optimized_python(tmp_path, optimized):
    program = r"""
import importlib.util,json,resource,sys
from pathlib import Path
resource.setrlimit(resource.RLIMIT_CPU,(20,20))
spec=importlib.util.spec_from_file_location("_qr05ad_guards",Path(sys.argv[1]))
if spec is None or spec.loader is None: raise RuntimeError("missing helpers")
h=importlib.util.module_from_spec(spec);sys.modules[spec.name]=h;spec.loader.exec_module(h)
rejections=pre=0
def require(value,message):
    if not value: raise RuntimeError(message)
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
for i,filename in enumerate(("retention.py","reference_qr05ad.py")):
    module=h.private_module("_qr05ad_guard_core"+str(i),filename)
    for p in (h.mixed_problem(),h.problem_of(0,0),h.problem_of(2,h.F(1,2))):
        require(h.wire(module.analyze(p))==h.wire(h.independent_analysis(p)),"complete generic wire")
    for bad in invalid:reject(module.analyze,bad)
    for bad in h.graph_inputs(valid):before_dump(module.analyze,bad)
    def forbidden(*args):raise RuntimeError("work preceded complete preflight")
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
    try:reject(module.analyze,h.replaced(valid,("decisions",15,"half_linear_coefficient"),[2,4]))
    finally:
        for n,v in hooks.items():setattr(module,n,v)
    for kind in ("stationary","minimum_gap","linear_gradient","curvature"):
        reject(module.analyze,h.overflow_problem(kind))
    for v in (h.nested(0,128),h.nested([],128)):module._native(v)
    for v in (h.nested(0,129),h.nested([],129)):reject(module._native,v)
    shared=[0];module._native([shared,h.nested(shared,126)]);reject(module._native,[shared,h.nested(shared,127)])
    result=module.analyze(valid);result["decisions"][0]["optimizer"]["weight"][0]=-1
    require(module.analyze(valid)==h.independent_analysis(valid),"ownership or cap restoration")
runner=h.private_module("_qr05ad_guard_runner","study.py")
for bad in h.graph_inputs(valid):before_dump(runner.require_wire,bad)
for v in (h.nested(0,129),h.nested([],129)):reject(runner.require_wire,v)
shared=[0];runner.require_wire([shared,h.nested(shared,126)]);reject(runner.require_wire,[shared,h.nested(shared,127)])
reject(lambda v:runner.require_same_wire({"x":0},v,"typed regression"),{"x":False})
require(pre==39,"pre-serialization inventory")
require(rejections==2*(len(invalid)+33)+17,"rejection inventory")
print(json.dumps({"rejections":rejections,"pre_serialization_rejections":pre,"invalid_fixture_cases":len(invalid),"optimized":bool(sys.flags.optimize)}))
"""
    arguments = [sys.executable, "-I", "-X", f"pycache_prefix={tmp_path / 'external-bytecode'}"]
    if optimized:
        arguments.append("-O")
    arguments.extend(["-c", program, str(HERE / "test_qr05ad.py")])
    result = subprocess.run(arguments, capture_output=True, text=True, timeout=30, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == {
        "rejections": 2 * (len(invalid_problems()) + 33) + 17,
        "pre_serialization_rejections": 39,
        "invalid_fixture_cases": len(invalid_problems()),
        "optimized": optimized,
    }


PINS = {
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
PRODUCER_CONTROLS = dict.fromkeys(
    (
        "frozen_AC_certificates_preserved",
        "original_weight_clean_coefficients",
        "clean_segment_premises",
        "full_replacement_envelope_preserved",
        "complete_quadratic_reduction",
        "all_AC_menu_values_recovered",
        "finite_menu_minimax_comparator",
        "complete_optimal_forecast_families",
        "interval_optima_not_point_selected",
        "global_common_mechanism_witnesses",
        "complete_witness_laws_and_marginals",
        "literal_point_forecast_scores",
        "literal_parametric_world_polynomials",
        "old_failures_preserved_without_relabeling",
        "no_per_history_weight_selection",
    ),
    True,
)
PRODUCER_CONTROLS.update(
    origin_authenticated_by_generic_API=False,
    raw_history_reconstruction_performed_by_this_runner=False,
)


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


def literal_coefficients(zcase, letters):
    """Direct indicator expansion on original unnormalized source atoms."""
    clean = [[F(0), F(0)] for _ in LEVELS]
    full = [[[F(0) for _ in row["values"]] for row in letters] for _ in LEVELS]
    for source, models in zip(
        zcase["problem"]["experiment"]["beliefs"], frozen_maps(zcase), strict=True
    ):
        weight = fraction(source["weight"])
        for (report, truth), mass in channel_joints(source["channels"][0]).items():
            ni = next(i for i, row in enumerate(letters) if tuple(row["N"]) == report[:5])
            for s, model in enumerate(models):
                g, _, f = model[report]
                for q in g.keys() | f.keys() | {truth}:
                    delta = f.get(q, F(0)) - g.get(q, F(0))
                    clean[s][0] += weight * mass * delta * delta
                    clean[s][1] += weight * mass * ((q == truth) - g.get(q, F(0))) * delta
                for zi, label in enumerate(letters[ni]["values"]):
                    g, _, f = model[tuple(label)]
                    full[s][ni][zi] += (
                        weight
                        * mass
                        * (outcome_risk({truth: F(1)}, f) - outcome_risk({truth: F(1)}, g))
                    )
    assert all(value >= 0 for model in full for fiber in model for value in fiber)
    return [
        {
            "assumed_index": s,
            "clean_distance": fw(d),
            "clean_cross": fw(c),
            "full_replacement_upper": fw(sum(max(fiber) for fiber in full[s])),
        }
        for s, (d, c) in enumerate(clean)
    ], full


def project_case(accase, zcase, letters):
    coefficients, full = literal_coefficients(zcase, letters)
    p = problem_of()
    for row in p["decisions"]:
        s, u = row["assumed_index"], row["bound_index"]
        d, c, upper = (
            fraction(coefficients[s][k])
            for k in ("clean_distance", "clean_cross", "full_replacement_upper")
        )
        t = fraction(LEVELS[u])
        row["quadratic_coefficient"], row["half_linear_coefficient"] = (
            fw((1 - t) * d + t * upper),
            fw((1 - t) * c),
        )
        assert 0 <= d <= c <= 2
    # All source-coordinate coefficients, including unused fibers, not merely S1.
    for s, model in enumerate(full):
        assert [[fw(v) for v in fiber] for fiber in model] == [
            [r[2] for r in fiber] for fiber in accase["problem"]["models"][s]["full_coefficients"]
        ]
    return {
        "case_id": accase["case_id"],
        "problem": p,
        "producer_coefficients": coefficients,
        "prior_certificates": copy.deepcopy(accase["analysis"]["certificates"]),
    }


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


def independent_evidence(zcase, accase, analysis, coefficients, letters):
    sources, maps = zcase["problem"]["experiment"]["beliefs"], frozen_maps(zcase)
    families, family_keys, links, mechanisms = [], [], [], []
    for decision in analysis["decisions"]:
        s, u, opt = decision["assumed_index"], decision["bound_index"], decision["optimizer"]
        key = (s, wire(opt))
        if key not in family_keys:
            family_keys.append(key)
            beliefs = []
            for source, models in zip(sources, maps, strict=True):
                cells = []
                for report, (g, _, f) in sorted(models[s].items()):
                    point = None
                    if opt["kind"] == "point":
                        x = fraction(opt["weight"])
                        point = law_wire(
                            {
                                q: (1 - x) * g.get(q, F(0)) + x * f.get(q, F(0))
                                for q in g.keys() | f.keys()
                            }
                        )
                    cells.append(
                        {
                            "value": list(report),
                            "coarse_forecast": law_wire(g),
                            "detailed_forecast": law_wire(f),
                            "point_forecast": point,
                        }
                    )
                beliefs.append(
                    {
                        "belief_id": source["belief_id"],
                        "weight": copy.deepcopy(source["weight"]),
                        "cells": cells,
                    }
                )
            families.append(
                {
                    "family_id": len(families),
                    "assumed_index": s,
                    "optimizer": copy.deepcopy(opt),
                    "beliefs": beliefs,
                }
            )
        links.append({"assumed_index": s, "bound_index": u, "family_id": family_keys.index(key)})
        faces = [
            fiber["maximizer_indices"][:]
            for fiber in accase["analysis"]["profiles"][3 * s + 2]["fibers"]
        ]
        all_faces = [list(range(len(row["values"]))) for row in letters]
        mechanisms.append(
            {
                "assumed_index": s,
                "bound_index": u,
                "full_retention_profile_index": 3 * s + 2,
                "positive_weight_face_indices": faces,
                "zero_weight_face_indices": all_faces,
                "zero_bound_face_indices": copy.deepcopy(all_faces),
                "common_witness_label_indices": [face[0] for face in faces],
                "common_witness_valid_for_entire_segment": True,
            }
        )
    vectors = sorted({tuple(row["common_witness_label_indices"]) for row in mechanisms})
    laws = [
        {
            "witness_id": i,
            "label_indices": list(vector),
            "beliefs": [
                {
                    "belief_id": source["belief_id"],
                    "weight": copy.deepcopy(source["weight"]),
                    "channels": pointmass_channels(source["channels"][0], letters, vector),
                }
                for source in sources
            ],
        }
        for i, vector in enumerate(vectors)
    ]
    witness_links = [
        {
            "assumed_index": row["assumed_index"],
            "bound_index": row["bound_index"],
            "witness_id": vectors.index(tuple(row["common_witness_label_indices"])),
        }
        for row in mechanisms
    ]
    worlds = []
    for row, link in zip(analysis["decisions"], witness_links, strict=True):
        s, u, opt = row["assumed_index"], row["bound_index"], row["optimizer"]
        d, c, full = (
            fraction(coefficients[s][k])
            for k in ("clean_distance", "clean_cross", "full_replacement_upper")
        )
        polys = [
            {
                "actual_index": i,
                "quadratic_coefficient": fw((1 - t) * d + t * full),
                "half_linear_coefficient": fw((1 - t) * c),
            }
            for i, t in enumerate(map(fraction, LEVELS[: u + 1]))
        ]
        values = worst = None
        if opt["kind"] == "point":
            x = fraction(opt["weight"])
            numbers = [
                fraction(p["quadratic_coefficient"]) * x * x
                - 2 * fraction(p["half_linear_coefficient"]) * x
                for p in polys
            ]
            values, worst = (
                list(map(fw, numbers)),
                [i for i, v in enumerate(numbers) if v == max(numbers)],
            )
        worlds.append(
            {
                "assumed_index": s,
                "bound_index": u,
                "world_indices": list(range(u + 1)),
                "polynomials": polys,
                "optimizer": copy.deepcopy(opt),
                "point_world_excesses": values,
                "point_worst_world_indices": worst,
                "whole_interval_minimax": opt["kind"] == "interval",
                "upper_bound_value": copy.deepcopy(row["minimum"]),
                "common_witness_id": link["witness_id"],
                "checks": dict.fromkeys(
                    (
                        "point_or_parametric_laws_complete",
                        "all_worlds_below_optimum_value",
                        "common_witness_attains_optimum",
                    ),
                    True,
                ),
            }
        )
    return {
        "forecast_families": families,
        "family_certificate_map": links,
        "mechanism_certificates": mechanisms,
        "witness_laws": laws,
        "witness_certificate_map": witness_links,
        "world_certificates": worlds,
    }


def witness_polynomials(zcase, witness, s):
    values = [[F(0), F(0)] for _ in LEVELS]
    for source, actual, models in zip(
        zcase["problem"]["experiment"]["beliefs"],
        witness["beliefs"],
        frozen_maps(zcase),
        strict=True,
    ):
        assert source["belief_id"] == actual["belief_id"] and source["weight"] == actual["weight"]
        original = channel_joints(source["channels"][0])
        weight = fraction(source["weight"])
        for t, channel in enumerate(actual["channels"]):
            joint = channel_joints(channel)
            assert marginal(joint) == marginal(original)
            if t == 0:
                assert joint == original
            for (report, truth), mass in joint.items():
                g, _, f = models[s][report]
                for q in g.keys() | f.keys() | {truth}:
                    direction = f.get(q, F(0)) - g.get(q, F(0))
                    values[t][0] += weight * mass * direction * direction
                    values[t][1] += weight * mass * ((truth == q) - g.get(q, F(0))) * direction
    return values


def literal_family_scores(family, witness):
    assert family["optimizer"]["kind"] == "point"
    values = [F(0) for _ in LEVELS]
    for belief, actual in zip(family["beliefs"], witness["beliefs"], strict=True):
        assert belief["weight"] == actual["weight"] and belief["belief_id"] == actual["belief_id"]
        policies = {tuple(c["value"]): c for c in belief["cells"]}
        for t, channel in enumerate(actual["channels"]):
            for cell in channel["cells"]:
                policy = policies[tuple(cell["value"])]
                values[t] += (
                    fraction(belief["weight"])
                    * fraction(cell["probability"])
                    * (
                        outcome_risk(
                            read_law(cell["prediction"]), read_law(policy["point_forecast"])
                        )
                        - outcome_risk(
                            read_law(cell["prediction"]), read_law(policy["coarse_forecast"])
                        )
                    )
                )
    return values


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


def test_original_weight_source_coefficients_global_mechanism_and_continuous_menu_gap(
    runner, executors
):
    z = mini_z_case()
    letters = [{"N": [0] * 5, "values": [[0] * 7, [0] * 6 + [1]]}]
    coeff, full = literal_coefficients(z, letters)
    assert full == [[[F(3, 8), F(7, 8)]] for _ in LEVELS]
    assert coeff == [
        {
            "assumed_index": s,
            "clean_distance": [3, 8],
            "clean_cross": [3, 8],
            "full_replacement_upper": [7, 8],
        }
        for s in range(4)
    ]
    # One historywise maximizer gives9/8; equal rather than original weighting gives5/8.
    assert fraction(coeff[0]["full_replacement_upper"]) not in (F(9, 8), F(5, 8))
    ac = {"analysis": {"profiles": [{"full_upper_excess": [7, 8]} for _ in range(12)]}}
    assert runner.clean_coefficients(z, ac) == coeff
    for module in executors:
        row = module.analyze(problem_of(F(5, 8), F(3, 16)))["decisions"][0]
        assert row["optimizer"] == {"kind": "point", "weight": [3, 10]}
        assert row["minimum"] == [-9, 160] and row["finite_menu_gap"] == [1, 40]
    # Global pointmass keeps the unchosen clean report until complete replacement.
    channels = pointmass_channels(
        z["problem"]["experiment"]["beliefs"][0]["channels"][0], letters, [1]
    )
    assert [len(c["cells"]) for c in channels] == [2, 2, 2, 1]


def test_flat_upper_parametric_boundary_does_not_assert_every_lower_polynomial_zero(runner):
    # Deliberately algebraic builder control, NOT a claim of realizable source coefficients.
    z = mini_z_case()
    letters = [{"N": [0] * 5, "values": [[0] * 7, [0] * 6 + [1]]}]
    ac = {
        "analysis": {"profiles": [{"fibers": [{"maximizer_indices": [0, 1]}]} for _ in range(12)]}
    }
    coefficients = [
        {
            "assumed_index": s,
            "clean_distance": [1, 1],
            "clean_cross": [1, 1],
            "full_replacement_upper": [0, 1],
        }
        for s in range(4)
    ]
    p = problem_of()
    for row in p["decisions"]:
        t = fraction(LEVELS[row["bound_index"]])
        row["quadratic_coefficient"] = row["half_linear_coefficient"] = fw(1 - t)
    analysis = independent_analysis(p)
    expected = independent_evidence(z, ac, analysis, coefficients, letters)
    assert wire(runner.build_evidence(z, ac, analysis, coefficients, letters)) == wire(expected)
    row = expected["world_certificates"][3]
    assert row["whole_interval_minimax"] is True and row["point_world_excesses"] is None
    assert row["polynomials"][0]["quadratic_coefficient"] == [1, 1]
    assert row["polynomials"][-1]["quadratic_coefficient"] == [0, 1]
    fid = expected["family_certificate_map"][3]["family_id"]
    family = expected["forecast_families"][fid]
    assert all(c["point_forecast"] is None for b in family["beliefs"] for c in b["cells"])
    assert any(
        c["coarse_forecast"] != c["detailed_forecast"]
        for b in family["beliefs"]
        for c in b["cells"]
    )


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


@pytest.fixture(scope="session")
def letters(pinned):
    return alphabet(pinned["w"])


@pytest.fixture(scope="session")
def projected(pinned, letters):
    return [
        project_case(ac, z, letters)
        for ac, z in zip(pinned["ac"]["cases"], pinned["z"]["cases"], strict=True)
    ]


@pytest.fixture(scope="session")
def expected(projected):
    return [independent_analysis(c["problem"]) for c in projected]


@pytest.fixture(scope="session")
def evidence(pinned, letters, projected, expected):
    return [
        independent_evidence(z, ac, a, c["producer_coefficients"], letters)
        for z, ac, a, c in zip(
            pinned["z"]["cases"], pinned["ac"]["cases"], expected, projected, strict=True
        )
    ]


@pytest.mark.parametrize("case_index", range(6))
def test_fixed_six_complete_optimizer_wires_and_literal_original_source_coefficients(
    executors, runner, pinned, letters, projected, expected, case_index
):
    i = case_index
    before = wire(projected[i]["problem"])
    assert wire(
        runner.project_case(pinned["ac"]["cases"][i], pinned["z"]["cases"][i], letters)
    ) == wire(projected[i])
    for module in executors:
        assert wire(module.analyze(projected[i]["problem"])) == wire(expected[i])
        assert wire(projected[i]["problem"]) == before
    assert wire(runner.expected_analysis(projected[i]["problem"])) == wire(expected[i])
    assert wire(projected[i]["prior_certificates"]) == wire(
        pinned["ac"]["cases"][i]["analysis"]["certificates"]
    )
    for row, old in zip(expected[i]["decisions"], projected[i]["prior_certificates"], strict=True):
        assert [v["value"] for v in row["finite_menu"]] == [
            c["worst_excess"] for c in old["candidates"]
        ]
        assert fraction(row["finite_menu_minimum"]) == min(
            fraction(c["worst_excess"]) for c in old["candidates"]
        )


def test_fixed_complete_point_and_interval_laws_global_witnesses_and_literal_world_polynomials(
    runner, pinned, letters, projected, expected, evidence
):
    for z, ac, case, analysis, e in zip(
        pinned["z"]["cases"], pinned["ac"]["cases"], projected, expected, evidence, strict=True
    ):
        assert wire(
            runner.build_evidence(z, ac, analysis, case["producer_coefficients"], letters)
        ) == wire(e)
        polynomials = {}
        for s in range(4):
            wid = e["witness_certificate_map"][4 * s]["witness_id"]
            polynomials[s] = witness_polynomials(z, e["witness_laws"][wid], s)
            assert runner.literal_polynomials(z, e["witness_laws"][wid], s) == polynomials[s]
            d, c, full = (
                fraction(case["producer_coefficients"][s][k])
                for k in ("clean_distance", "clean_cross", "full_replacement_upper")
            )
            assert polynomials[s] == [
                [(1 - t) * d + t * full, (1 - t) * c] for t in map(fraction, LEVELS)
            ]
        scores = {}
        for family in e["forecast_families"]:
            s = family["assumed_index"]
            if family["optimizer"]["kind"] == "interval":
                assert all(
                    c["point_forecast"] is None for b in family["beliefs"] for c in b["cells"]
                )
                continue
            wid = e["witness_certificate_map"][4 * s]["witness_id"]
            values = literal_family_scores(family, e["witness_laws"][wid])
            assert runner.literal_family_scores(family, e["witness_laws"][wid]) == values
            x = fraction(family["optimizer"]["weight"])
            assert values == [a * x * x - 2 * b * x for a, b in polynomials[s]]
            scores[family["family_id"]] = values
        for row, world, link in zip(
            analysis["decisions"], e["world_certificates"], e["family_certificate_map"], strict=True
        ):
            s, u = row["assumed_index"], row["bound_index"]
            assert [
                [fraction(p["quadratic_coefficient"]), fraction(p["half_linear_coefficient"])]
                for p in world["polynomials"]
            ] == polynomials[s][: u + 1]
            if row["optimizer"]["kind"] == "point":
                values = scores[link["family_id"]][: u + 1]
                assert world["point_world_excesses"] == list(map(fw, values))
                assert max(values) == fraction(row["minimum"])
                assert world["point_worst_world_indices"] == [
                    i for i, v in enumerate(values) if v == max(values)
                ]
            else:
                assert polynomials[s][u] == [0, 0]
                assert all(a >= 0 and a - 2 * b <= 0 for a, b in polynomials[s][: u + 1])
                assert world["point_world_excesses"] is world["point_worst_world_indices"] is None


@pytest.fixture(scope="session")
def aggregate(runner):
    return runner.run_suite()


def test_fixed_runner_whole_suite_nonpooled_inventory_complete_families_and_preserved_certificates(
    aggregate, letters, projected, expected, evidence
):
    cases = [
        {**p, "analysis": a, **e, "producer_controls": PRODUCER_CONTROLS}
        for p, a, e in zip(projected, expected, evidence, strict=True)
    ]
    totals = {"cases": 6, "analyze_calls": 12, "invalid_analyze_calls_rejected": 16}
    totals.update({k: sum(a["counts"][k] for a in expected) for k in expected[0]["counts"]})
    totals.update(
        forecast_families=sum(len(e["forecast_families"]) for e in evidence),
        witness_mechanisms=sum(len(e["witness_laws"]) for e in evidence),
    )
    wanted = {
        "producer": {
            "artifact": PINS["ac"][0] + "/results.json",
            "bytes": PINS["ac"][1],
            "sha256": PINS["ac"][2],
        },
        "alphabet": letters,
        "cases": cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": 16,
            "raw_laws_histories_or_artifacts_given_to_core": False,
            "weights_selected_per_history": False,
            "actual_world_used_to_select_weight": False,
            "forecasts_outside_frozen_segment_used": False,
            "prior_certificates_replaced": False,
        },
        "totals": totals,
    }
    assert wire(aggregate) == wire(wanted)


def test_oversized_native_strings_keys_and_width_fail_before_whole_serialization(
    executors, monkeypatch
):
    p = problem_of()
    bad = [
        {**p, "extra": "é" * (1048576 // 6 + 1)},
        {**p, "x" * 1048576: 0},
        {**p, "extra": [None] * 65536},
    ]

    def forbidden(*_args, **_kwargs):
        raise RuntimeError("oversized native structure reached serializer")

    for module in executors:
        with monkeypatch.context() as m:
            m.setattr(json, "dumps", forbidden)
            for value in bad:
                with pytest.raises(ValueError):
                    module.analyze(value)


def output_corruptions(analysis):
    point = next(
        i for i, r in enumerate(analysis["decisions"]) if r["optimizer"]["kind"] == "point"
    )
    row = analysis["decisions"][point]
    paths = [
        (("input_sha256",), "0" * 64),
        (("levels", 0, 0), False),
        (("decisions", point, "linear_coefficient"), fw(fraction(row["linear_coefficient"]) + 1)),
        (("decisions", point, "critical_candidates", 0, "value"), [1, 1]),
        (("decisions", point, "critical_candidates"), row["critical_candidates"][::-1]),
        (
            ("decisions", point, "optimizer", "weight"),
            fw(1 - fraction(row["optimizer"]["weight"]))
            if row["optimizer"]["weight"] != [1, 2]
            else [0, 1],
        ),
        (("decisions", point, "minimum"), fw(fraction(row["minimum"]) + 1)),
        (("decisions", point, "finite_menu", 0, "value"), [1, 1]),
        (
            ("decisions", point, "finite_menu", 0, "excess_over_minimum"),
            fw(fraction(row["finite_menu"][0]["excess_over_minimum"]) + 1),
        ),
        (("decisions", point, "finite_menu_minimizer_indices"), []),
        (("decisions", point, "finite_menu_minimizer_weights"), []),
        (("decisions", point, "finite_menu_gap"), fw(fraction(row["finite_menu_gap"]) + 1)),
        (("decisions", point, "proof", "gradient"), fw(fraction(row["proof"]["gradient"]) + 1)),
        (("decisions", point, "checks", "global_kkt_certificate"), False),
        (("counts", "total_work_terms"), analysis["counts"]["total_work_terms"] + 1),
    ]
    return [replaced(analysis, path, value) for path, value in paths]


def test_fixed_all_complete_optimizer_output_corruptions_are_nonvacuous(
    runner, pinned, letters, projected, expected, evidence, monkeypatch
):
    i = next(i for i, a in enumerate(expected) if a["counts"]["point_optimizers"])
    ac, z, aa, ab = (pinned[k]["cases"][i] for k in ("ac", "z", "aa", "ab"))
    # Prior AC/raw authentication and independent projection are covered separately.
    # These direct helper tests target its new complete AD output contract only.
    monkeypatch.setattr(runner, "ac_check_analysis", lambda *_args: None)
    monkeypatch.setattr(runner, "project_case", lambda *_args: projected[i])
    for changed in output_corruptions(expected[i]):
        assert wire(changed) != wire(expected[i])
        with pytest.raises(ValueError):
            runner.check_analysis(changed, ac, z, aa, ab, letters, evidence[i])


def evidence_corruptions(evidence):
    point = next(
        i for i, f in enumerate(evidence["forecast_families"]) if f["optimizer"]["kind"] == "point"
    )
    interval = next(
        i
        for i, f in enumerate(evidence["forecast_families"])
        if f["optimizer"]["kind"] == "interval"
    )
    interval_cell = evidence["forecast_families"][interval]["beliefs"][0]["cells"][0]
    world = evidence["world_certificates"][0]
    paths = [
        (
            (
                "forecast_families",
                point,
                "beliefs",
                0,
                "cells",
                0,
                "coarse_forecast",
                0,
                "probability",
            ),
            [0, 1],
        ),
        (
            (
                "forecast_families",
                point,
                "beliefs",
                0,
                "cells",
                0,
                "detailed_forecast",
                0,
                "probability",
            ),
            [0, 1],
        ),
        (
            (
                "forecast_families",
                point,
                "beliefs",
                0,
                "cells",
                0,
                "point_forecast",
                0,
                "probability",
            ),
            [0, 1],
        ),
        (
            ("forecast_families", interval, "beliefs", 0, "cells", 0, "point_forecast"),
            interval_cell["coarse_forecast"],
        ),
        (("forecast_families", point, "beliefs", 0, "weight"), [0, 1]),
        (("family_certificate_map", 0, "family_id"), -1),
        (("mechanism_certificates", 0, "common_witness_label_indices", 0), -1),
        (("mechanism_certificates", 0, "positive_weight_face_indices", 0), []),
        (("witness_laws", 0, "beliefs", 0, "channels", 0, "cells", 0, "probability"), [0, 1]),
        (("witness_laws", 0, "beliefs", 0, "channels"), []),
        (("witness_certificate_map", 0, "witness_id"), -1),
        (
            ("world_certificates", 0, "polynomials", 0, "quadratic_coefficient"),
            fw(fraction(world["polynomials"][0]["quadratic_coefficient"]) + 1),
        ),
        (("world_certificates", 0, "point_worst_world_indices"), []),
    ]
    return [replaced(evidence, path, value) for path, value in paths]


def test_fixed_complete_family_witness_and_world_corruptions_cannot_hide_behind_valid_minimum(
    runner, pinned, letters, expected, evidence, monkeypatch
):
    i = next(
        i
        for i, a in enumerate(expected)
        if a["counts"]["point_optimizers"] and a["counts"]["interval_optimizers"]
    )
    ac, z, aa, ab = (pinned[k]["cases"][i] for k in ("ac", "z", "aa", "ab"))
    monkeypatch.setattr(runner, "ac_check_analysis", lambda *_args: None)
    for changed in evidence_corruptions(evidence[i]):
        assert wire(changed) != wire(evidence[i])
        with pytest.raises(ValueError):
            runner.check_analysis(expected[i], ac, z, aa, ab, letters, changed)


def test_fixed_producer_original_weights_frozen_laws_coefficients_and_prior_menu_are_authenticated(
    runner, pinned, letters, expected, evidence, monkeypatch
):
    i = next(i for i, a in enumerate(expected) if a["counts"]["interior_point_optimizers"])
    ac, z, aa, ab = (pinned[k]["cases"][i] for k in ("ac", "z", "aa", "ab"))
    monkeypatch.setattr(runner, "ac_check_analysis", lambda *_args: None)
    z_changes = [
        replaced(z, ("problem", "experiment", "beliefs", 0, "weight"), [0, 1]),
        replaced(
            z,
            (
                "problem",
                "experiment",
                "beliefs",
                0,
                "channels",
                0,
                "cells",
                0,
                "prediction",
                0,
                "probability",
            ),
            [0, 1],
        ),
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
    ]
    ac_changes = [
        replaced(
            ac,
            ("analysis", "profiles", 2, "full_upper_excess"),
            fw(fraction(ac["analysis"]["profiles"][2]["full_upper_excess"]) + 1),
        ),
        replaced(
            ac,
            ("problem", "models", 0, "full_coefficients", 0, 0, 2),
            fw(fraction(ac["problem"]["models"][0]["full_coefficients"][0][0][2]) + 1),
        ),
        replaced(ac, ("analysis", "certificates", 0, "candidates", 0, "worst_excess"), [1, 1]),
    ]
    for original, changed, changed_ac, changed_z in [(z, bad, ac, bad) for bad in z_changes] + [
        (ac, bad, bad, z) for bad in ac_changes
    ]:
        assert wire(changed) != wire(original)
        with pytest.raises(ValueError):
            runner.check_analysis(expected[i], changed_ac, changed_z, aa, ab, letters, evidence[i])
