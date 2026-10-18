"""QR-05F exact finite sampling capture and read-only replay."""

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
SCHEMA = "det8-qr05f-results-v1"
BASE_COMMIT = "90d40a6a430271298c5141246c5632c97a4a2d58"
SOURCES = (
    "README.md",
    "sequential.py",
    "reference_qr05f.py",
    "study.py",
    "test_qr05f.py",
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
    "qr-05e-sampling-aware-2026-09-06/results.json": "362e7f0c00f00491cd3820fd840faca63b244ed4a0c2156bcb3d0924baa52f41",
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


DESIGNS = ("independent", "parity_adaptive", "common_coin", "parity_hole", "first_pair")
PAIRS = tuple(("ferrers6", d) for d in DESIGNS) + (
    ("standard_example3", "independent"),
    ("chain6", "parity_adaptive"),
    ("chain6", "parity_hole"),
    ("chain6", "first_pair"),
    ("ferrers6_fixed", "independent"),
)
METHODS = ("final_joint", "sequential_supported", "naive_quarter", "rb_sequential")
SAMPLING_PRIOR = "qr-05e-sampling-aware-2026-09-06/results.json"


def fixtures():
    return [
        {"schema_version": "det8-qr05f-problem-v1", "profile": p, "design": d} for p, d in PAIRS
    ]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"profile": "ferrers6"},
        {k: v for k, v in base.items() if k != "design"},
        {**base, "extra": 1},
        *({**base, "profile": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "design": v} for v in (True, None, 1, [], "unknown")),
        *({**base, "schema_version": v} for v in (True, None, 1, [], "other")),
        {**base, "profile": "chain6", "design": "independent"},
        {**base, "profile": "standard_example3", "design": "common_coin"},
        {**base, "profile": "ferrers6_fixed", "design": "parity_hole"},
    ]


def check_analysis(a):
    require_wire(a)
    m = len(a["eligible"])
    require(len(a["past"]) == 8 and m in (5, 6) and len(a["questions"]) == 4, "analysis bounds")
    first, final, paths = a["first_rows"], a["final_rows"], a["transcripts"]
    require([r["mask"] for r in first] == list(range(1 << m)), "first mask coverage")
    require([r["mask"] for r in final] == list(range(1 << m)), "final mask coverage")
    require(
        [[r["stage1_mask"], r["final_mask"]] for r in paths]
        == [[s, t] for s in range(1 << m) for t in range(1 << m) if s & t == t],
        "nested transcript coverage",
    )
    p1, pf = list(map(F, a["stage1_probabilities"])), list(map(F, a["final_probabilities"]))
    require(sum(p1) == sum(pf) == 1 and min(p1 + pf) >= 0, "probability normalization")
    conditional = [F(0) for _ in first]
    composed = [F(0) for _ in final]
    for path in paths:
        s, t = path["stage1_mask"], path["final_mask"]
        k, joint = F(path["conditional_probability"]), F(path["joint_probability"])
        require(k >= 0 and joint == p1[s] * k, "joint composition")
        conditional[s] += k
        composed[t] += joint
        if joint > 0:
            require(
                not any(path["omitted_terms"]["final_joint"])
                and not any(path["omitted_terms"]["sequential_supported"]),
                "unsupported term on positive transcript",
            )
    require(conditional == [1] * len(first) and composed == pf, "law composition normalization")
    for field, probabilities in (("stage1_inclusions", p1), ("final_inclusions", pf)):
        expected = [
            str(sum((p for s, p in enumerate(probabilities) if s & mask == mask), F(0)))
            for mask in range(1 << m)
        ]
        require_same_wire(a[field], expected, "inclusion table differs")
    require_same_wire(
        a["moments"]["final_joint"]["mean_counts"],
        [str(q["final_supported_count"]) for q in a["questions"]],
        "final supported expectation",
    )
    require_same_wire(
        a["moments"]["sequential_supported"]["mean_counts"],
        [q["sequential_coverage_target"] for q in a["questions"]],
        "sequential coverage expectation",
    )
    require_same_wire(
        a["moments"]["rb_sequential"]["mean_counts"],
        a["moments"]["sequential_supported"]["mean_counts"],
        "RB mean",
    )
    for t, row in enumerate(final):
        require(F(row["probability"]) == pf[t], "final row probability")
        require(
            (row["conditional_sequential_mean"] is None) == (pf[t] == 0)
            and (row["conditional_sequential_covariance"] is None) == (pf[t] == 0),
            "null-event conditional boundary",
        )
    for s, row in enumerate(first):
        require(F(row["probability"]) == p1[s], "first row probability")
        require(
            [
                F(v) - F(w)
                for v, w in zip(
                    row["sequential_conditional_mean"], row["first_estimates"], strict=True
                )
            ]
            == list(map(F, row["conditional_defect"])),
            "conditional defect",
        )
    decomp = a["variance_decomposition"]
    require_same_wire(
        decomp["sequential_covariance"],
        a["moments"]["sequential_supported"]["covariance_counts"],
        "total covariance",
    )
    require_same_wire(
        decomp["rb_covariance"], a["moments"]["rb_sequential"]["covariance_counts"], "RB covariance"
    )
    require_same_wire(
        decomp["residual"], [["0"] * 4 for _ in range(4)], "total covariance residual"
    )
    require(
        all(
            F(decomp["sequential_covariance"][i][j])
            == F(decomp["rb_covariance"][i][j]) + F(decomp["mean_conditional_covariance"][i][j])
            for i in range(4)
            for j in range(4)
        ),
        "variance decomposition",
    )
    counts = {
        "events": 8,
        "eligible_events": m,
        "first_rows": 1 << m,
        "positive_first_rows": sum(p > 0 for p in p1),
        "final_rows": 1 << m,
        "positive_final_rows": sum(p > 0 for p in pf),
        "transcript_rows": 3**m,
        "positive_transcript_rows": sum(F(r["joint_probability"]) > 0 for r in paths),
        "questions": 4,
        "chain_terms": sum(q["target_count"] for q in a["questions"]),
        "estimator_cells": 3**m * 12,
    }
    require_same_wire(a["counts"], counts, "retained counts")


def find_path(a, s, t):
    return next(r for r in a["transcripts"] if r["stage1_mask"] == s and r["final_mask"] == t)


def cross_controls(analyses):
    by = {(a["profile"], a["design"]): a for a in analyses}
    independent = []
    for profile, vr in (("ferrers6", "138"), ("standard_example3", "126")):
        a = by[profile, "independent"]
        for row in a["transcripts"]:
            require_same_wire(
                row["estimates"]["final_joint"],
                row["estimates"]["sequential_supported"],
                "independent pointwise",
            )
            require_same_wire(
                row["estimates"]["final_joint"],
                row["estimates"]["naive_quarter"],
                "independent naive control",
            )
        h = a["moments"]["final_joint"]
        require(
            h["mean_counts"] == ["1", "6", "6", "0"]
            and h["covariance_counts"][1][1] == "18"
            and h["covariance_counts"][1][2] == "36"
            and h["covariance_counts"][2][2] == vr,
            "independent covariance control",
        )
        independent.append(
            {
                "profile": profile,
                "mean_N_R": ["6", "6"],
                "variance_N": "18",
                "covariance_N_R": "36",
                "variance_R": vr,
            }
        )
    a = by["ferrers6", "parity_adaptive"]
    pi = ["1", "1/4", "5/72", "1/48", "17/2592", "11/5184", "1/46656"]
    require(a["final_inclusions"] == [pi[s.bit_count()] for s in range(64)], "adaptive inclusions")
    left, right = find_path(a, 1, 1), find_path(a, 3, 1)
    require(
        left["joint_probability"] == "1/96" and right["joint_probability"] == "1/288",
        "adaptive supported collision paths",
    )
    require(
        left["estimates"]["sequential_supported"][1] == "3"
        and right["estimates"]["sequential_supported"][1] == "6"
        and left["estimates"]["final_joint"][1] == right["estimates"]["final_joint"][1] == "4",
        "adaptive estimator collision",
    )
    require(
        a["final_rows"][1]["conditional_sequential_mean"][1] == "570/119"
        and a["final_rows"][1]["probability"] == "1309/23328",
        "RB differs from final HT",
    )
    require(
        a["moments"]["sequential_supported"]["covariance_counts"][1][1] == "21"
        and a["moments"]["final_joint"]["covariance_counts"][1][1] == "64/3",
        "no uniform final variance dominance",
    )
    adaptive = {
        "inclusions_by_size": pi,
        "left": left,
        "right": right,
        "final_mask": 1,
        "final_mask_probability": "1309/23328",
        "conditional_sequential_N": "570/119",
        "direct_final_N": "4",
        "sequential_variance_N": "21",
        "final_variance_N": "64/3",
        "access": a["access"],
    }
    common = by["ferrers6", "common_coin"]
    require(
        common["moments"]["final_joint"]["mean_counts"] == ["1", "6", "6", "0"]
        and common["moments"]["naive_quarter"]["mean_counts"] == ["1", "6", "12", "0"],
        "common-coin marginal-product failure",
    )
    c = common["moments"]["final_joint"]["covariance_counts"]
    require(c[1][1] == "48" and c[1][2] == "60" and c[2][2] == "104", "common-coin covariance")
    for row in common["transcripts"]:
        require_same_wire(
            row["estimates"]["final_joint"],
            row["estimates"]["sequential_supported"],
            "common-coin pointwise joint correction",
        )
    holes = []
    for profile, seq, full in (
        ("ferrers6", ["1", "3", "3", "0"], ["1", "6", "6", "0"]),
        ("chain6", ["1", "3", "15/2", "10"], ["1", "6", "15", "20"]),
    ):
        case = by[profile, "parity_hole"]
        require(
            case["moments"]["sequential_supported"]["mean_counts"] == seq
            and case["moments"]["final_joint"]["mean_counts"] == full
            and all(q["full_final_support"] for q in case["questions"]),
            "final vs conditional support",
        )
        holes.append(
            {
                "profile": profile,
                "sequential_mean": seq,
                "final_mean": full,
                "final_support_complete": True,
            }
        )
    pair = by["chain6", "first_pair"]["questions"][3]
    require(
        pair["target_count"] == 20
        and pair["first_supported_count"] == pair["final_supported_count"] == 0
        and pair["sequential_coverage_target"] == "0",
        "first-stage chain support hole",
    )
    fixed = by["ferrers6_fixed", "independent"]
    require(
        fixed["final_rows"][0]["chain_counts"][1] == 1
        and fixed["final_rows"][0]["final_estimate"][1] == "1"
        and fixed["moments"]["final_joint"]["mean_counts"][1] == "6",
        "fixed vertex weight",
    )
    access = []
    for case in analyses:
        require(
            case["access"]["policy_token"]["estimator"]["measurable"]
            and all(
                case["access"]["full_stage1"][k]["measurable"]
                for k in ("estimator", "repeat_prediction")
            ),
            "access positive control",
        )
        access.append(
            {"profile": case["profile"], "design": case["design"], "access": case["access"]}
        )
    require(
        not a["access"]["final_only"]["estimator"]["measurable"]
        and not a["access"]["policy_token"]["repeat_prediction"]["measurable"],
        "access separation",
    )
    require(
        a["first_rows"][0]["policy_token"] == a["first_rows"][3]["policy_token"] == "1/3"
        and a["first_rows"][0]["repeat_probability"] == "0"
        and a["first_rows"][3]["repeat_probability"] == "1/3"
        and F(find_path(a, 0, 0)["joint_probability"]) > 0
        and F(find_path(a, 3, 0)["joint_probability"]) > 0,
        "partial-provenance repeat witness",
    )
    return {
        "independent": independent,
        "adaptive": adaptive,
        "common_coin": {
            "corrected_mean_N_R": ["6", "6"],
            "naive_mean_N_R": ["6", "12"],
            "variance_N": "48",
            "covariance_N_R": "60",
            "variance_R": "104",
        },
        "conditional_holes": holes,
        "first_pair_unsupported_degree3": pair,
        "fixed_vertex": {"final_empty_count_N": 1, "final_empty_estimate_N": "1", "mean_N": "6"},
        "access": access,
    }


def prior_bridge(analyses):
    old = prior_json(SAMPLING_PRIOR)["suite"]
    by = {(c["input"]["order"], c["input"]["design"]): c["analysis"] for c in old["cases"]}
    checks = []
    for a in analyses:
        profile, design = a["profile"], a["design"]
        source = "ferrers6" if profile == "ferrers6_fixed" else profile
        target_prior = by[source, "singleton" if source == "chain6" else "identity"]
        require_same_wire(a["past"], target_prior["past"], "QR-05E full source bridge")
        require(a["density"] == target_prior["density"], "QR-05E density bridge")
        require_same_wire(
            [q["target_count"] for q in a["questions"]],
            [q["target_count"] for q in target_prior["questions"]],
            "QR-05E target bridge",
        )
        require_same_wire(
            [q["target_coefficient"] for q in a["questions"]],
            [q["target_coefficient"] for q in target_prior["questions"]],
            "QR-05E coefficient bridge",
        )
        stage_checks = 0
        prior_design = "fixed_size2" if design == "first_pair" else "iid_half"
        if (source, prior_design) in by:
            earlier = by[source, prior_design]
            for row in a["first_rows"]:
                mask = sum(1 << j for j, v in enumerate(earlier["eligible"]) if v in row["kept"])
                old_row = earlier["samples"][mask]
                require_same_wire(row["kept"], old_row["kept"], "QR-05E first kept bridge")
                require_same_wire(
                    row["past"], old_row["observed_past"], "QR-05E first order bridge"
                )
                expected_probability = F(old_row["probability"])
                if profile == "ferrers6_fixed":
                    expected_probability /= F(earlier["inclusion_probabilities"][1 << 2])
                require(
                    F(row["probability"]) == expected_probability, "QR-05E first probability bridge"
                )
                stage_checks += 1
        checks.append(
            {
                "profile": profile,
                "design": design,
                "source_prior": [source, target_prior["design"]],
                "target_counts": [q["target_count"] for q in a["questions"]],
                "target_coefficients": [q["target_coefficient"] for q in a["questions"]],
                "first_stage_prior": None if stage_checks == 0 else [source, prior_design],
                "condition_on_fixed_vertex": 3 if profile == "ferrers6_fixed" else None,
                "first_mask_rows_checked": stage_checks,
            }
        )
    return {
        "scope": "PINNED_SOURCE_TARGETS_FIRST_OBSERVATION_LAWS_AND_RETAINED_COUNTEREXAMPLES",
        "checks": checks,
        "source_checks": len(checks),
        "target_question_checks": 4 * len(checks),
        "first_mask_rows_checked": sum(c["first_mask_rows_checked"] for c in checks),
        "prior_iid_variance_collision": old["controls"]["iid_collision"],
        "prior_singleton_identification": old["controls"]["singleton_identification"],
        "prior_geometric_and_quantum_bridge": old["prior_bridge"],
        "prior_executors_imported": False,
        "new_physical_coupling_claimed": False,
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
    direct = load("qr05f_capture_direct", "sequential.py")
    reference = load("qr05f_capture_reference", "reference_qr05f.py")
    cases = []
    for problem in fixtures():
        a, b = direct.analyze(problem), reference.analyze(problem)
        require_same_wire(a, b, "independent complete analysis differs")
        check_analysis(a)
        cases.append({"input": problem, "analysis": a})
    rejected = []
    for problem in invalid_fixtures():
        for module in (direct, reference):
            try:
                module.analyze(problem)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError("invalid fixed input accepted")
        rejected.append({"input": problem, "both_rejected": True})
    analyses = [c["analysis"] for c in cases]
    controls, bridge = cross_controls(analyses), prior_bridge(analyses)
    bits = retained_bits([cases, controls, bridge])
    require(bits <= 4096, "retained arithmetic bound")
    totals = {k: sum(a["counts"][k] for a in analyses) for k in analyses[0]["counts"]}
    totals.update(
        {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejected),
            "zero_joint_rows": totals["transcript_rows"] - totals["positive_transcript_rows"],
            "count_covariance_cells": len(cases) * 4 * 16,
            "coefficient_covariance_cells": len(cases) * 4 * 16,
            "retained_component_bits": bits,
        }
    )
    require(
        [
            totals[k]
            for k in (
                "fixtures",
                "transcript_rows",
                "positive_transcript_rows",
                "first_rows",
                "final_rows",
                "questions",
                "estimator_cells",
            )
        ]
        == [10, 6804, 3534, 608, 608, 40, 81648],
        "prespecified coverage",
    )
    suite = {
        "cases": cases,
        "rejections": rejected,
        "controls": controls,
        "prior_bridge": bridge,
        "research_base_commit": BASE_COMMIT,
        "claim": "FINITE_TWO_STAGE_LAW_ESTIMATION_CONDITIONING_AND_ACCESS_SEPARATION",
        "unknown_sampling_law_inferred": False,
        "unknown_geometry_reconstructed": False,
        "quantum_channel_constructed": False,
        "continuum_limit_established": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "full_conditional_law_preserved_by_token_claimed": False,
        "bounds": {
            "maximum_events": 8,
            "maximum_eligible_events": 6,
            "maximum_chain_degree": 3,
            "operational_methods": 3,
            "conditional_average_methods": 1,
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
