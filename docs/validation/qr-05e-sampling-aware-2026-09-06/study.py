"""QR-05E exact finite sampling capture and read-only replay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULT = HERE / "results.json"
SCHEMA = "det8-qr05e-results-v1"
BASE_COMMIT = "07703e939c4b2932bb6bd87d914b756fa3a42a1d"
SOURCES = (
    "README.md",
    "thinning.py",
    "reference_qr05e.py",
    "study.py",
    "test_qr05e.py",
    "test_capture.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05/results.json": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05/results.json": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05/results.json": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05/results.json": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05/results.json": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05/results.json": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05/results.json": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05/results.json": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    "qr-05d-geometric-correspondence-2026-09-05/results-v2.json": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def plain_bytes(path):
    require(path.is_file() and not path.is_symlink(), "input must be a plain file")
    return path.read_bytes()


def ledger():
    result = {}
    for name in SOURCES:
        raw = plain_bytes(HERE / name)
        result[name] = {"bytes": len(raw), "sha256": digest(raw)}
    return result


def priors():
    result = {}
    for name, sha in PRIORS.items():
        raw = plain_bytes(HERE.parent / name)
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name)
    require(digest(raw) == PRIORS[name], "prior artifact changed")
    return json.loads(raw)


def load(name, filename):
    require(name not in sys.modules, "private study module collision")
    path = HERE / filename
    raw = plain_bytes(path)
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "cannot load executor")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


ORDERS = ("ferrers6", "standard_example3", "mesh3_center")
DESIGNS = ("identity", "iid_half", "heterogeneous", "all_or_none", "fixed_size2")
METHODS = ("raw", "marginal_product", "uniform_rate", "joint_supported")
PAIRS = tuple((o, d) for o in ORDERS for d in DESIGNS) + (
    ("ferrers6", "singleton"),
    ("chain6", "singleton"),
)
GEOMETRY_PRIOR = "qr-05d-geometric-correspondence-2026-09-05/results-v2.json"


def fixtures():
    return [{"schema_version": "det8-qr05e-problem-v1", "order": o, "design": d} for o, d in PAIRS]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"order": "ferrers6"},
        {k: v for k, v in base.items() if k != "design"},
        {**base, "extra": 1},
        *({**base, "order": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "design": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "schema_version": v} for v in (True, None, 1, [], "other")),
        {**base, "order": "chain6", "design": "iid_half"},
        {**base, "order": "standard_example3", "design": "singleton"},
        {**base, "order": "mesh3_center", "design": "singleton"},
    ]


def check_analysis(a):
    require_wire(a)
    samples, questions = a["samples"], a["questions"]
    n, m, qn = len(a["past"]), len(a["eligible"]), len(questions)
    require(n <= 11 and m <= 8 and qn in (4, 12), "analysis bound")
    require([s["mask"] for s in samples] == list(range(1 << m)), "mask coverage")
    probabilities = [F(s["probability"]) for s in samples]
    require(sum(probabilities) == 1 and min(probabilities) >= 0, "sampling normalization")
    inclusion = [F(p) for p in a["inclusion_probabilities"]]
    require(
        inclusion
        == [
            sum((p for s, p in enumerate(probabilities) if s & t == t), F(0)) for t in range(1 << m)
        ],
        "joint inclusion table differs",
    )
    require(all(inclusion[1 << j] > 0 for j in range(m)), "positive marginal contract")
    supported = [str(q["supported_count"]) for q in questions]
    require_same_wire(
        a["moments"]["joint_supported"]["mean_counts"], supported, "supported mean identity"
    )
    require_same_wire(
        a["joint_covariance_formula"],
        a["moments"]["joint_supported"]["covariance_counts"],
        "covariance identity",
    )
    for q in questions:
        require(q["target_count"] == len(q["chains"]), "source chain inventory")
        zero = [c["vertices"] for c in q["chains"] if F(c["inclusion"]) == 0]
        require_same_wire(q["zero_inclusion_chains"], zero, "zero support inventory")
        require(q["supported_count"] == q["target_count"] - len(zero), "supported target")
        require(q["full_target_supported"] is (not zero), "support flag")
        alpha = F((-1) ** q["degree"], 2 ** (q["degree"] + 1) * F(a["density"]) ** q["degree"])
        require(
            F(q["scale"]) == alpha and F(q["target_coefficient"]) == alpha * q["target_count"],
            "target coefficient",
        )
    for s, p in zip(samples, probabilities, strict=True):
        require(
            len(s["chain_counts"]) == qn
            and all(len(s["estimates"][method]) == qn for method in METHODS),
            "sample width",
        )
        if p > 0:
            require(not any(s["unsupported_observed_terms"]), "impossible supported row")
    require(
        a["counts"]
        == {
            "events": n,
            "eligible_events": m,
            "mask_rows": 1 << m,
            "positive_rows": sum(p > 0 for p in probabilities),
            "questions": qn,
            "chain_terms": sum(q["target_count"] for q in questions),
            "estimator_cells": (1 << m) * qn * 4,
        },
        "retained counts",
    )


def cross_controls(analyses):
    by = {(a["order_name"], a["design"]): a for a in analyses}
    controls = {
        "iid_collision": [],
        "heterogeneous": [],
        "correlated": [],
        "fixed_size2": [],
        "hasse_only": [],
    }
    for order, variance, hetero_mean in (
        ("ferrers6", "34", "52/9"),
        ("standard_example3", "30", "56/9"),
    ):
        iid = by[order, "iid_half"]
        h = iid["moments"]["joint_supported"]
        require(h["mean_counts"] == ["1", "6", "6", "0"], "IID mean")
        require(
            h["covariance_counts"][1][1] == "6"
            and h["covariance_counts"][1][2] == "12"
            and h["covariance_counts"][2][2] == variance,
            "IID covariance",
        )
        require(h["exact_target_probabilities"][2] == "0", "IID single-sample non-equality")
        controls["iid_collision"].append(
            {
                "order": order,
                "mean_counts": h["mean_counts"],
                "variance_N": "6",
                "covariance_N_R": "12",
                "variance_R": variance,
                "exact_R_target_probability": "0",
            }
        )
        ht = by[order, "heterogeneous"]["moments"]
        require(ht["uniform_rate"]["mean_counts"][2] == hetero_mean, "heterogeneous bias")
        require(
            all(
                ht[k]["mean_counts"][1:3] == ["6", "6"]
                for k in ("joint_supported", "marginal_product")
            ),
            "independent correction",
        )
        controls["heterogeneous"].append(
            {
                "order": order,
                "raw_mean_R": ht["raw"]["mean_counts"][2],
                "uniform_mean_R": hetero_mean,
                "uniform_bias_R": ht["uniform_rate"]["bias_counts"][2],
                "corrected_mean_R": "6",
            }
        )
        correlated = by[order, "all_or_none"]["moments"]
        require(
            correlated["joint_supported"]["mean_counts"][1:3] == ["6", "6"]
            and correlated["marginal_product"]["mean_counts"][1:3] == ["6", "12"],
            "correlated inclusion counterexample",
        )
        require(
            correlated["joint_supported"]["mean_coefficients"][2] == "1/192"
            and correlated["marginal_product"]["mean_coefficients"][2] == "1/96",
            "correlated coefficient counterexample",
        )
        controls["correlated"].append(
            {
                "order": order,
                "joint_mean_N_R": ["6", "6"],
                "product_mean_N_R": ["6", "12"],
                "joint_mean_z2": "1/192",
                "product_mean_z2": "1/96",
                "one_density_rescaling_fixes_all_degrees": False,
            }
        )
        fixed = by[order, "fixed_size2"]
        require(all(q["full_target_supported"] for q in fixed["questions"]), "pair support")
        covariance = fixed["moments"]["joint_supported"]["covariance_counts"]
        require(
            covariance[1][1] == "0" and covariance[1][2] == "0" and covariance[2][2] == "54",
            "fixed-size cancellation",
        )
        controls["fixed_size2"].append(
            {
                "order": order,
                "full_targets_supported": True,
                "variance_N": "0",
                "covariance_N_R": "0",
                "variance_R": "54",
            }
        )
    mesh = by["mesh3_center", "fixed_size2"]
    require(
        [q["target_count"] for q in mesh["questions"][:4]] == [1, 9, 27, 37]
        and [q["supported_count"] for q in mesh["questions"][:4]] == [1, 9, 27, 13],
        "fixed-center support counts",
    )
    require(
        len(mesh["questions"][3]["zero_inclusion_chains"]) == 24
        and all(q["full_target_supported"] for q in mesh["questions"][4:]),
        "fixed-center omitted chains",
    )
    require(
        mesh["moments"]["joint_supported"]["covariance_counts"][3][3] == "195",
        "supported degree-three variance",
    )
    controls["fixed_center_support"] = {
        "whole_targets": [1, 9, 27, 37],
        "whole_supported_targets": [1, 9, 27, 13],
        "missing_degree3_chains": 24,
        "supported_degree3_variance": "195",
        "local_targets_supported": True,
        "universal_nonidentifiability_claimed": False,
    }
    left, right = by["ferrers6", "singleton"], by["chain6", "singleton"]
    require_same_wire(
        left["observation_law"], right["observation_law"], "singleton channel collision differs"
    )
    require(
        [q["target_count"] for q in left["questions"]] == [1, 6, 6, 0]
        and [q["target_count"] for q in right["questions"]] == [1, 6, 15, 20],
        "singleton distinct targets",
    )
    controls["singleton_identification"] = {
        "orders": ["ferrers6", "chain6"],
        "observation_laws_equal": True,
        "source_name_disclosed_to_observer": False,
        "targets": [[1, 6, 6, 0], [1, 6, 15, 20]],
        "supported_targets": [1, 6, 0, 0],
        "one_unbiased_estimator_for_both_full_targets_exists": False,
        "obstruction_persists_for_any_fixed_number_of_iid_repetitions": True,
        "observation_law": left["observation_law"],
    }
    for a in analyses:
        h = a["hasse_control"]
        require(
            (h["first_mismatch"] is None) == (F(h["mismatch_probability"]) == 0),
            "positive Hasse mismatch witness",
        )
        if a["design"] == "identity":
            require(h["first_mismatch"] is None, "identity Hasse loss")
            for moment in a["moments"].values():
                require(
                    not any(map(F, moment["bias_counts"]))
                    and not any(F(v) for row in moment["covariance_counts"] for v in row),
                    "identity exactness",
                )
        controls["hasse_only"].append({"order": a["order_name"], "design": a["design"], **h})
    require(
        F(by["chain6", "singleton"]["hasse_control"]["mismatch_probability"]) == 1,
        "Hasse positive-channel failure",
    )
    return controls


def prior_bridge(analyses):
    prior = prior_json(GEOMETRY_PRIOR)["suite"]
    old = {c["input"]["case"]: c["analysis"] for c in prior["cases"]}
    current = {a["order_name"]: a for a in analyses if a["design"] == "identity"}
    checks = []
    for new_name, old_name in (
        ("ferrers6", "ferrers6"),
        ("standard_example3", "standard_example3"),
        ("mesh3_center", "mesh3"),
    ):
        a, previous = current[new_name], old[old_name]
        relation = previous["order"]["relation"]
        past = [[i for i in range(len(relation)) if relation[i][j]] for j in range(len(relation))]
        require_same_wire(a["past"], past, "QR-05D source order bridge")
        require(a["density"] == previous["density"], "QR-05D supplied density bridge")
        questions = a["questions"][:4]
        require_same_wire(
            [q["target_count"] for q in questions],
            previous["order"]["endpoint"]["chain_counts"][:4],
            "QR-05D endpoint chain bridge",
        )
        require_same_wire(
            [q["target_coefficient"] for q in questions],
            previous["order"]["endpoint"]["coefficients"][:4],
            "QR-05D endpoint coefficient bridge",
        )
        local = []
        for p in a["probes"][1:]:
            coefficients = [
                q["target_coefficient"] for q in a["questions"] if q["probe"] == p["name"]
            ][:3]
            require_same_wire(
                coefficients,
                [m[p["source"]][p["target"]] for m in previous["order"]["kernel_coefficients"]],
                "QR-05D local coefficient bridge",
            )
            local.append({"probe": p["name"], "coefficients": coefficients})
        checks.append(
            {
                "order": new_name,
                "prior_case": old_name,
                "past": past,
                "density": a["density"],
                "endpoint_counts": [q["target_count"] for q in questions],
                "endpoint_coefficients": [q["target_coefficient"] for q in questions],
                "local_checks": local,
            }
        )
    return {
        "scope": "PINNED_GEOMETRY_TARGET_REPRODUCTION_AND_RETAINED_PRIOR_COUNTEREXAMPLES",
        "order_checks": checks,
        "endpoint_question_checks": 12,
        "local_coefficient_checks": 6,
        "prior_collision": prior["controls"]["collision"],
        "prior_base_probes": prior["controls"]["base_probes"],
        "prior_transformations": prior["controls"]["transformations"],
        "prior_quantum_bridge": prior["prior_bridge"],
        "previous_executors_imported": False,
        "new_quantum_or_geometry_coupling_claimed": False,
    }


def retained_bits(value):
    if type(value) is dict:
        return max((retained_bits(v) for v in value.values()), default=0)
    if type(value) is list:
        return max((retained_bits(v) for v in value), default=0)
    if type(value) is int:
        return abs(value).bit_length()
    if type(value) is str and re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value):
        v = F(value)
        return max(abs(v.numerator).bit_length(), v.denominator.bit_length())
    return 0


def run_suite():
    direct = load("qr05e_capture_direct", "thinning.py")
    reference = load("qr05e_capture_reference", "reference_qr05e.py")
    cases = []
    for problem in fixtures():
        a, b = direct.analyze(problem), reference.analyze(problem)
        require_same_wire(a, b, "independent complete analysis differs")
        check_analysis(a)
        cases.append({"input": problem, "analysis": a})
    rejections = []
    for problem in invalid_fixtures():
        for module in (direct, reference):
            try:
                module.analyze(problem)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError("invalid fixed input accepted")
        rejections.append({"input": problem, "both_rejected": True})
    analyses = [c["analysis"] for c in cases]
    controls, bridge = cross_controls(analyses), prior_bridge(analyses)
    bits = retained_bits([cases, controls, bridge])
    require(bits <= 4096, "retained arithmetic bound")
    totals = {
        key: sum(a["counts"][key] for a in analyses)
        for key in (
            "events",
            "eligible_events",
            "mask_rows",
            "positive_rows",
            "questions",
            "chain_terms",
            "estimator_cells",
        )
    }
    totals.update(
        {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejections),
            "zero_probability_rows": totals["mask_rows"] - totals["positive_rows"],
            "count_covariance_cells": 4 * sum(len(a["questions"]) ** 2 for a in analyses),
            "coefficient_covariance_cells": 4 * sum(len(a["questions"]) ** 2 for a in analyses),
            "retained_component_bits": bits,
        }
    )
    require(
        [totals[k] for k in ("fixtures", "mask_rows", "positive_rows", "questions")]
        == [17, 2048, 847, 108],
        "prespecified coverage",
    )
    suite = {
        "cases": cases,
        "controls": controls,
        "prior_bridge": bridge,
        "rejections": rejections,
        "research_base_commit": BASE_COMMIT,
        "claim": "EXACT_FINITE_DESIGN_MEANS_COVARIANCES_AND_OBSERVER_RELATIVE_LIMITS",
        "unknown_sampling_law_inferred": False,
        "unknown_geometry_reconstructed": False,
        "poisson_ensemble_validated": False,
        "continuum_limit_established": False,
        "quantum_channel_constructed": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "bounds": {
            "maximum_events": 11,
            "maximum_eligible_events": 8,
            "maximum_internal_chain_degree": 3,
            "estimation_methods": 4,
            "arithmetic_guard_bits": 4096,
        },
        "totals": totals,
    }
    require_wire(suite)
    require_same_wire(suite, json.loads(canonical(suite)), "aggregate wire round trip differs")
    return suite


def require_wire(value):
    """Reject implicit JSON coercions in the mathematical evidence tree."""
    if value is None or type(value) in (bool, int, str):
        return
    if type(value) is list:
        for item in value:
            require_wire(item)
        return
    if type(value) is dict:
        require(all(type(key) is str for key in value), "wire keys must be strings")
        for item in value.values():
            require_wire(item)
        return
    raise ValueError("mathematical suite must use native exact JSON types")


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()


def require_same_wire(left, right, message):
    require_wire(left)
    require_wire(right)
    require(canonical(left) == canonical(right), message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    require(
        sys.flags.isolated and sys.pycache_prefix, "run isolated with an external bytecode cache"
    )
    cache = Path(sys.pycache_prefix).resolve()
    require(
        cache != Path(cache.anchor) and not cache.is_relative_to(ROOT),
        "invalid bytecode cache boundary",
    )
    if not args.verify and (RESULT.exists() or RESULT.is_symlink()):
        raise FileExistsError("result exists; use --verify, never overwrite")
    frozen, previous = ledger(), priors()
    if args.verify:
        before = plain_bytes(RESULT)
        existing = json.loads(before)
        require(
            type(existing) is dict
            and set(existing)
            == {"schema_version", "source_ledger", "prior_artifacts", "suite", "runtime"}
            and existing["schema_version"] == SCHEMA,
            "unrecognized result schema",
        )
        require(canonical(existing) == before, "result is not canonical")
        require_same_wire(existing["source_ledger"], frozen, "source identity changed")
        require_same_wire(existing["prior_artifacts"], previous, "prior identity changed")
    started = time.perf_counter()
    suite = run_suite()
    require_wire(suite)
    require_same_wire(suite, json.loads(canonical(suite)), "aggregate wire round trip differs")
    elapsed = time.perf_counter() - started
    require(ledger() == frozen and priors() == previous, "source/prior changed during execution")
    if args.verify:
        require_same_wire(existing["suite"], suite, "exact replay differs")
        require(plain_bytes(RESULT) == before, "result changed during replay")
        print(
            json.dumps(
                {
                    "status": "VERIFIED_EXACT_REPLAY",
                    "sha256": digest(before),
                    "seconds": elapsed,
                    "totals": suite["totals"],
                }
            )
        )
        return
    report = {
        "schema_version": SCHEMA,
        "source_ledger": frozen,
        "prior_artifacts": previous,
        "suite": suite,
        "runtime": {
            "python": sys.version,
            "executable": sys.executable,
            "platform": platform.platform(),
            "isolated": bool(sys.flags.isolated),
            "optimized": sys.flags.optimize,
            "bytecode_cache": str(cache),
            "suite_seconds": elapsed,
            "rss_high_water_at_suite_end": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "rss_units": "bytes" if sys.platform == "darwin" else "KiB",
            "scope": "suite only; excludes serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    with RESULT.open("xb") as output:
        output.write(raw)
    require(plain_bytes(RESULT) == raw, "capture readback differs")
    print(
        json.dumps(
            {
                "status": "CREATED_EXACT_FINITE_RESULT",
                "path": str(RESULT),
                "bytes": len(raw),
                "sha256": digest(raw),
                "seconds": elapsed,
                "totals": suite["totals"],
            }
        )
    )


if __name__ == "__main__":
    main()
