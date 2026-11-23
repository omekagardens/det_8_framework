"""Opaque-box 4-tier E2E test suite for the DET8 kappa-gravity revival track.

Derived strictly from requirements and repository specifications:
- Tier 1: Isolated feature coverage (F1a, F1b, F2-F8, Quarantine & Snapshot)
- Tier 2: Boundary & corner cases (domain guards, numerical limits, malformed I/O)
- Tier 3: Cross-feature pairwise combinations
- Tier 4: Real-world astrophysical & repository governance scenarios

Runs purely on Python 3.13.5 stdlib ``unittest`` with lazy imports of M2-M4
modules and zero imports of ``FULLY_RETIRED`` quarantine modules.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import json
import math
import re
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
E2E_TEST_PATH = Path(__file__).resolve()
REVIVAL_BRANCH = "revival/kappa-gravity-pathways"
ORIGIN_URL = "https://github.com/omekagardens/det_8_framework.git"
MAIN_BASELINE_SHA = "f699622976c0ca770c60b3a6dc8980bdee7f02f7"
SNAPSHOT_MANIFEST_PATH = REPO_ROOT / "docs" / "coordination" / "review_snapshot.json"
RESEARCH_REGISTRY_PATH = REPO_ROOT / "docs" / "research" / "registry.json"

CASSINI_GAMMA_BOUND = 2.3e-5
NIST_YB_SR_UNCERTAINTY = 2.0e-18
MICROSCOPE_ETA_BOUND = 1.5e-15
EOT_WASH_ETA_BOUND = 1.8e-13

VALID_EPISTEMIC_TAGS = frozenset(
    {"TH-DET", "CORR", "FIT", "EXTERNAL_ANCHOR", "P", "PR", "AX-DET", "MATH", "M"}
)
PATHWAY1_STATUS_VALUES = frozenset(
    {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION", "REFUTED"}
)

EXPECTED_DOCS: tuple[str, ...] = (
    "PHYSICS.md",
    "MODEL_CARD.md",
    "README.md",
    "ROADMAP.md",
    "NEXT_STEPS.md",
    "GOVERNANCE.md",
    "FALSIFICATION_LEDGER.md",
    "NOVELTY_LEDGER.md",
    "archive/retired_kappa_gravity.md",
    "docs/CONTINUUM_LIMIT_FRAMEWORK.md",
    "docs/applied_physics.md",
    "docs/track_b/gravity.md",
    "docs/observable_anchoring.md",
)

EXPECTED_CORE_ALIGNED: tuple[str, ...] = (
    "det8/models/det_falsification.py",
    "det8/models/det_units.py",
    "det8/models/det8_core.py",
    "det8/models/legacy_gravity_quarantine.py",
)

EXPECTED_REVIVED_FILES: tuple[str, ...] = (
    "det8/models/galaxy_observables.py",
    "det8/models/kappa_t1_contraction.py",
    "det8/models/pi_conformal_bridge.py",
    "det8/models/kappa_gravity_revival.py",
    "det8/tests/test_kappa_gravity_revival.py",
    "det8/tests/test_kappa_gravity_e2e.py",
)


# ── Lazy Module Loaders & Subprocess Helpers ────────────────────────────────


def _import_observables():
    return importlib.import_module("det8.models.galaxy_observables")


def _import_reference_constants():
    return importlib.import_module("det8.models.reference_constants")


def _import_core():
    return importlib.import_module("det8.models.det8_core")


def _import_constraints():
    return importlib.import_module("det8.models.experimental_constraints")


def _import_quarantine():
    return importlib.import_module("det8.models.legacy_gravity_quarantine")


def _import_p1():
    return importlib.import_module("det8.models.kappa_t1_contraction")


def _import_p2():
    return importlib.import_module("det8.models.pi_conformal_bridge")


def _import_revival():
    return importlib.import_module("det8.models.kappa_gravity_revival")


def _run_cmd(args: list[str], *, cwd: Path = REPO_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return _run_cmd(["git", *args])


def _snapshot_pinned_relpaths() -> set[str]:
    data = json.loads(SNAPSHOT_MANIFEST_PATH.read_text(encoding="utf-8"))
    artifacts = data.get("artifacts", data.get("files", []))
    if isinstance(artifacts, dict):
        paths = set(artifacts.keys())
    else:
        paths = {entry["path"] for entry in artifacts}
    assert len(paths) == 71, f"Expected 71 snapshot paths, got {len(paths)}"
    return paths


# ── Opaque-Box Dict & Semantic Inspection Helpers ───────────────────────────


def _walk_items(obj: Any, prefix: str = ""):
    if isinstance(obj, dict):
        for key, val in obj.items():
            key_str = str(key)
            path = f"{prefix}.{key_str}" if prefix else key_str
            yield path.lower(), val
            yield from _walk_items(val, path)
    elif isinstance(obj, (list, tuple)):
        for idx, val in enumerate(obj):
            path = f"{prefix}[{idx}]"
            yield path.lower(), val
            yield from _walk_items(val, path)


def _all_numbers(obj: Any) -> list[float]:
    nums: list[float] = []
    if isinstance(obj, bool):
        return nums
    if isinstance(obj, (int, float)) and math.isfinite(float(obj)):
        nums.append(float(obj))
    elif isinstance(obj, dict):
        for val in obj.values():
            nums.extend(_all_numbers(val))
    elif isinstance(obj, (list, tuple)):
        for val in obj:
            nums.extend(_all_numbers(val))
    return nums


def _numbers_for_keys(obj: Any, substrings: tuple[str, ...]) -> list[float]:
    found: list[float] = []
    for path, val in _walk_items(obj):
        if isinstance(val, (int, float)) and not isinstance(val, bool):
            fval = float(val)
            if math.isfinite(fval) and any(sub in path for sub in substrings):
                found.append(fval)
    return found


def _serialized_lower(obj: Any) -> str:
    return json.dumps(obj, default=str, sort_keys=True).lower()


def _extract_manifest_tags(manifest: list[dict[str, Any]]) -> list[str]:
    tags: list[str] = []
    for entry in manifest:
        if not isinstance(entry, dict):
            continue
        tags.extend(sorted(_entry_tags(entry)))
    return tags


def _entry_tags(entry: dict[str, Any]) -> set[str]:
    found: set[str] = set()
    tag_key_tokens = (
        "tag",
        "status",
        "class",
        "layer",
        "epistemic",
        "label",
        "category",
        "provenance",
        "evidence",
    )
    for k, v in _walk_items(entry):
        if any(tok in k for tok in tag_key_tokens):
            if isinstance(v, str):
                for part in v.replace("/", " ").replace(",", " ").split():
                    cleaned = part.strip("()[] ")
                    if cleaned in VALID_EPISTEMIC_TAGS:
                        found.add(cleaned)
    if not found:
        for _, v in _walk_items(entry):
            if isinstance(v, str) and v.strip() in VALID_EPISTEMIC_TAGS:
                found.add(v.strip())
    return found


def _extract_conformal_and_phi_acc(res: dict[str, Any]) -> tuple[float, float]:
    lit_vals: list[float] = []
    att_vals: list[float] = []
    for path, val in _walk_items(res):
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            continue
        fval = float(val)
        if not math.isfinite(fval):
            continue
        leaf = path.rsplit(".", 1)[-1]
        if any(bad in leaf for bad in ("plus", "sum", "diff", "is_", "consistent")):
            continue
        if any(tok in leaf for tok in ("a_conformal", "a_literal", "literal_acc", "conformal_acc")):
            lit_vals.append(fval)
        elif any(tok in leaf for tok in ("a_phi", "a_attractive", "attractive_acc", "phi_acc", "minus_dphi")):
            att_vals.append(fval)
    if not lit_vals:
        lit_vals = _numbers_for_keys(res, ("literal", "conformal_acc", "ln_pi", "pi_acc"))
    if not att_vals:
        att_vals = _numbers_for_keys(res, ("attractive", "phi_acc", "minus_dphi"))
    if not lit_vals or not att_vals:
        raise AssertionError(f"Missing conformal/phi acceleration fields in {res}")
    return lit_vals[0], att_vals[0]


def _read_doc(relpath: str) -> str:
    return (REPO_ROOT / relpath).read_text(encoding="utf-8")


def _assert_f6_sign_check_8_of_8(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    for bkey in ("all_increasing", "all_monotonic", "passed", "all_passed", "f6_passed"):
        if bkey in res:
            case.assertIs(res[bkey], True, f"Expected {bkey}=True in {res}")
    case.assertNotIn("0/8", _serialized_lower(res), f"Unexpected 0/8 failure in {res}")

    inc_counts: list[float] = []
    positive_leaf_names = {
        "n_increasing",
        "increasing_count",
        "n_monotonic",
        "monotonic_count",
        "passed_count",
        "n_passed",
        "pass_count",
        "increasing",
    }
    neg_tokens = ("non", "not", "fail", "false", "dec", "frac", "ratio", "pct", "percent", "rate", "total")
    for path, val in _walk_items(res):
        if isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(float(val)):
            leaf = path.rsplit(".", 1)[-1]
            if "[" in leaf:
                continue
            if leaf in positive_leaf_names or (
                ("increasing" in leaf or "monotonic" in leaf)
                and not any(tok in leaf for tok in neg_tokens)
            ):
                inc_counts.append(float(val))

    galaxy_list_8_true = False
    for val in res.values():
        if isinstance(val, list) and len(val) == 8 and all(isinstance(item, dict) for item in val):
            true_count = 0
            for item in val:
                flag = None
                for k in ("increasing", "is_increasing", "monotonic", "passed"):
                    if k in item and isinstance(item[k], bool):
                        flag = item[k]
                        break
                if flag is False:
                    case.fail(f"Galaxy entry failed F6 sign check: {item}")
                if flag is True:
                    true_count += 1
            if true_count == 8:
                galaxy_list_8_true = True

    if inc_counts:
        case.assertIn(8.0, inc_counts, f"Expected increasing count == 8 in {res}; got {inc_counts}")
        case.assertNotIn(0.0, inc_counts, f"Unexpected 0 increasing count in {res}")
    else:
        case.assertTrue(
            galaxy_list_8_true,
            f"Expected increasing count keys == 8 or 8 True galaxy entries in {res}",
        )


def _assert_pathway2_refuted(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    verdict = res.get("status", res.get("verdict", res.get("outcome")))
    case.assertIsNotNone(verdict, f"Missing top-level status/verdict in {res}")
    case.assertEqual(str(verdict).strip().upper(), "REFUTED", f"Expected REFUTED verdict, got {res}")
    if "refuted_criteria" in res:
        case.assertIsInstance(res["refuted_criteria"], (list, tuple, set, dict))
        case.assertGreater(len(res["refuted_criteria"]), 0, f"Expected non-empty refuted_criteria in {res}")
    if "viable" in res:
        case.assertIs(res["viable"], False, f"Expected viable=False in {res}")
    if "passed" in res:
        case.assertIs(res["passed"], False, f"Expected passed=False in {res}")


def _assert_audit_failed(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    if "passed" in res:
        case.assertIs(res["passed"], False, f"Expected audit passed=False, got {res}")
    if "viable" in res:
        case.assertIs(res["viable"], False, f"Expected audit viable=False, got {res}")


def _assert_clock_scale_gap_failure(case: unittest.TestCase, res: dict[str, Any]) -> None:
    _assert_audit_failed(case, res)
    gap_vals: list[float] = []
    nist_vals: list[float] = []
    for path, val in _walk_items(res):
        if isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(float(val)):
            if "det8_core_default" in path or "core_default" in path:
                continue
            if any(tok in path for tok in ("nist_gap", "gap_ratio", "scale_gap", "clock_gap")):
                gap_vals.append(float(val))
            if "nist" in path and ("gap" in path or "ratio" in path or "excess" in path):
                nist_vals.append(float(val))
    case.assertTrue(
        any(x >= 1e10 for x in gap_vals),
        f"Expected >= 1e10 clock scale gap ratio (excluding det8_core_default) in {res}; got {gap_vals}",
    )
    if nist_vals:
        case.assertTrue(
            any(x >= 1e10 for x in nist_vals),
            f"Expected NIST clock gap >= 1e10 in {res}; got {nist_vals}",
        )


def _top_and_summary_scopes(res: dict[str, Any]) -> list[dict[str, Any]]:
    scopes: list[dict[str, Any]] = [res]
    summary = res.get("summary")
    if isinstance(summary, dict):
        scopes.append(summary)
    return scopes


def _top_scope_scalars(res: dict[str, Any]) -> list[float]:
    vals: list[float] = []
    for scope in _top_and_summary_scopes(res):
        for val in scope.values():
            if isinstance(val, (int, float)) and not isinstance(val, bool) and math.isfinite(float(val)):
                vals.append(float(val))
    return vals


def _sparc_overall_mean_and_rms_values(res: dict[str, Any]) -> tuple[list[float], list[float]]:
    mean_exact = {
        "mean_error",
        "mean_rel_error",
        "mean_relative_error",
        "mean_fractional_error",
        "mean_frac_error",
        "overall_mean_error",
    }
    rms_exact = {"rms_error", "rms_rel_error", "rms_relative_error"}
    exclude_tokens = (
        "newton",
        "baseline",
        "std",
        "max",
        "min",
        "median",
        "diff",
        "delta",
        "ratio",
        "improv",
    )
    mean_vals: list[float] = []
    rms_vals: list[float] = []
    for scope in _top_and_summary_scopes(res):
        for raw_k, val in scope.items():
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                continue
            fval = float(val)
            if not math.isfinite(fval):
                continue
            kl = str(raw_k).lower()
            if any(tok in kl for tok in exclude_tokens):
                continue
            if kl in mean_exact or ("mean" in kl and "err" in kl):
                mean_vals.append(fval)
            elif kl in rms_exact or ("rms" in kl and "err" in kl):
                rms_vals.append(fval)
    return mean_vals, rms_vals


def _sparc_overall_error_values(res: dict[str, Any]) -> list[float]:
    mean_vals, rms_vals = _sparc_overall_mean_and_rms_values(res)
    return mean_vals if mean_vals else rms_vals


def _assert_sparc_fit_overall_valid(
    case: unittest.TestCase,
    res: dict[str, Any],
    *,
    beta: float = 0.93,
    check_fit_quality: bool = True,
) -> None:
    case.assertIsInstance(res, dict)
    top_nums = _top_scope_scalars(res)
    case.assertIn(43.0, top_nums, f"Expected 43 galaxies in top-level/summary of {res}")

    mean_vals, rms_vals = _sparc_overall_mean_and_rms_values(res)
    errs = mean_vals if mean_vals else rms_vals
    case.assertTrue(errs, f"Missing top-level/summary overall SPARC error metrics in {res}")

    if check_fit_quality:
        for err in errs:
            case.assertGreater(err, 0.05, f"Unexpectedly tiny overall SPARC error {err} in {res}")
            case.assertLess(err, 0.30, f"Overall SPARC error {err} >= 0.30 in {res}")
        for rms in rms_vals:
            case.assertGreater(rms, 0.05, f"Unexpectedly tiny overall SPARC RMS error {rms} in {res}")
            case.assertLess(rms, 0.40, f"Overall SPARC RMS error {rms} >= 0.40 in {res}")

        w20_checked = False
        for scope in _top_and_summary_scopes(res):
            has_w20_frac = any(
                ("within_20" in str(k).lower() or "within20" in str(k).lower())
                and ("frac" in str(k).lower() or "ratio" in str(k).lower())
                for k in scope
            )
            has_w50_frac = any(
                ("within_50" in str(k).lower() or "within50" in str(k).lower())
                and ("frac" in str(k).lower() or "ratio" in str(k).lower())
                for k in scope
            )
            for raw_k, val in scope.items():
                if not isinstance(val, (int, float)) or isinstance(val, bool):
                    continue
                fval = float(val)
                if not math.isfinite(fval):
                    continue
                kl = str(raw_k).lower()
                if "within_20" in kl or "within20" in kl:
                    w20_checked = True
                    if "frac" in kl or "ratio" in kl:
                        case.assertGreaterEqual(fval, 0.58, f"Expected {raw_k} >= 0.58 in {res}")
                        case.assertLessEqual(fval, 1.0, f"Expected {raw_k} <= 1.0 in {res}")
                    elif kl in {"within_20pct", "within20pct"} or "count" in kl or kl.startswith("n_"):
                        case.assertTrue(
                            25.0 <= fval <= 43.0,
                            f"Overall {raw_k}={fval} out of passing galaxy count range [25, 43] in {res}",
                        )
                    elif "_pct" in kl or "percent" in kl:
                        if has_w20_frac and isinstance(val, int) and 25 <= val <= 43:
                            pass
                        else:
                            case.assertTrue(
                                58.0 <= fval <= 100.0,
                                f"Overall {raw_k}={fval} out of passing percentage range [58.0, 100.0] in {res}",
                            )
                    else:
                        valid_w20 = (25.0 <= fval <= 43.0) or (0.58 <= fval < 1.0)
                        case.assertTrue(valid_w20, f"Overall {raw_k}={fval} out of passing range in {res}")
                elif "within_50" in kl or "within50" in kl:
                    if "frac" in kl or "ratio" in kl:
                        case.assertGreaterEqual(fval, 0.80, f"Expected {raw_k} >= 0.80 in {res}")
                        case.assertLessEqual(fval, 1.0, f"Expected {raw_k} <= 1.0 in {res}")
                    elif kl in {"within_50pct", "within50pct"} or "count" in kl or kl.startswith("n_"):
                        case.assertTrue(
                            35.0 <= fval <= 43.0,
                            f"Overall {raw_k}={fval} out of passing galaxy count range [35, 43] in {res}",
                        )
                    elif "_pct" in kl or "percent" in kl:
                        if has_w50_frac and isinstance(val, int) and 35 <= val <= 43:
                            pass
                        else:
                            case.assertTrue(
                                80.0 <= fval <= 100.0,
                                f"Overall {raw_k}={fval} out of passing percentage range [80.0, 100.0] in {res}",
                            )
                    else:
                        valid_w50 = (35.0 <= fval <= 43.0) or (0.80 <= fval < 1.0)
                        case.assertTrue(valid_w50, f"Overall {raw_k}={fval} out of passing range in {res}")
        case.assertTrue(w20_checked, f"Missing top-level/summary within_20* metric in {res}")

    expected_ceiling = 1.0 / (1.0 - beta)
    ceiling_vals = [
        float(val)
        for scope in _top_and_summary_scopes(res)
        for raw_k, val in scope.items()
        if isinstance(val, (int, float))
        and not isinstance(val, bool)
        and math.isfinite(float(val))
        and any(tok in str(raw_k).lower() for tok in ("ceil", "max_enh", "enhancement", "factor"))
    ]
    case.assertTrue(
        any(abs(x - expected_ceiling) < 0.1 for x in (ceiling_vals or top_nums)),
        f"Expected dwarf ceiling ~{expected_ceiling:.2f} in top-level/summary of {res}",
    )


def _assert_radial_asymptotics_keplerian(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    for path, val in _walk_items(res):
        if path.rsplit(".", 1)[-1] == "keplerian_turnover_universal":
            case.assertIs(val, True, f"Expected {path}=True in {res}")

    outer_exact = {
        "far_outer_slope_mean",
        "max_multiplier_mean_slope",
        "outer_slope",
        "outer_log_slope",
        "asymptotic_slope",
        "mean_outer_slope",
        "outer_mean_slope",
    }
    outer_slopes: list[float] = []
    for scope in _top_and_summary_scopes(res):
        for raw_k, val in scope.items():
            if not isinstance(val, (int, float)) or isinstance(val, bool):
                continue
            fval = float(val)
            if not math.isfinite(fval):
                continue
            kl = str(raw_k).lower()
            if kl in outer_exact or (
                ("outer" in kl or "asymptot" in kl or "far_" in kl)
                and "slope" in kl
                and "min_" not in kl
                and "inner" not in kl
            ):
                outer_slopes.append(fval)

        reg_sum = scope.get("regime_summaries")
        if isinstance(reg_sum, dict):
            for rname, rval in reg_sum.items():
                rkl = str(rname).lower()
                if not isinstance(rval, dict):
                    continue
                if rkl.startswith("outer") or rkl in {"far_outer", "far_outer_regime"}:
                    for sk in ("mean_slope", "slope", "log_slope"):
                        sval = rval.get(sk)
                        if isinstance(sval, (int, float)) and not isinstance(sval, bool) and math.isfinite(float(sval)):
                            outer_slopes.append(float(sval))
                            break
                    steep_cnt = rval.get("steep_lt_minus_0_3_count")
                    if (
                        isinstance(steep_cnt, (int, float))
                        and not isinstance(steep_cnt, bool)
                        and math.isfinite(float(steep_cnt))
                    ):
                        denom = rval.get("count", rval.get("n_galaxies", scope.get("n_galaxies", res.get("n_galaxies"))))
                        if isinstance(denom, (int, float)) and not isinstance(denom, bool) and float(denom) > 0:
                            case.assertGreater(
                                float(steep_cnt),
                                0.8 * float(denom),
                                f"Expected {rname}.steep_lt_minus_0_3_count > 0.8 * {denom}, got {steep_cnt}",
                            )
                            case.assertLessEqual(
                                float(steep_cnt),
                                float(denom),
                                f"Expected {rname}.steep_lt_minus_0_3_count <= {denom}, got {steep_cnt}",
                            )

        mult_sum = scope.get("multiplier_summaries")
        if isinstance(mult_sum, dict):
            numeric_mults: list[tuple[float, dict[str, Any]]] = []
            for mk, mval in mult_sum.items():
                if not isinstance(mval, dict):
                    continue
                try:
                    mf = float(mk)
                except (TypeError, ValueError):
                    continue
                if math.isfinite(mf):
                    numeric_mults.append((mf, mval))
            if numeric_mults:
                _, max_mval = max(numeric_mults, key=lambda item: item[0])
                for sk in ("mean_slope", "slope", "log_slope"):
                    sval = max_mval.get(sk)
                    if isinstance(sval, (int, float)) and not isinstance(sval, bool) and math.isfinite(float(sval)):
                        outer_slopes.append(float(sval))
                        break

    case.assertTrue(outer_slopes, f"Missing outer-regime/summary slope metrics in {res}")
    for slope in outer_slopes:
        case.assertTrue(
            -0.6 <= slope <= -0.35,
            f"Expected outer Keplerian slope in [-0.6, -0.35], got {slope} in {res}",
        )


def _assert_exp_regime_passes(
    case: unittest.TestCase,
    path: str,
    val: dict[str, Any],
    *,
    bound: float,
) -> bool:
    exp_sub = val.get("exponential")
    if not isinstance(exp_sub, dict):
        return False
    found_pass_flag = False
    if "passes_bound" in exp_sub:
        case.assertIs(exp_sub["passes_bound"], True, f"Expected {path}.exponential.passes_bound=True")
        found_pass_flag = True
    if "passes" in exp_sub:
        case.assertIs(exp_sub["passes"], True, f"Expected {path}.exponential.passes=True")
        found_pass_flag = True
    for ek, ev in exp_sub.items():
        if not isinstance(ev, (int, float)) or isinstance(ev, bool) or not math.isfinite(float(ev)):
            continue
        ekl = str(ek).lower()
        if "bound" in ekl or "limit" in ekl:
            continue
        if ekl in {"delta_g_over_g", "eta", "delta_g", "delta_kappa", "gamma_dev", "cassini_dev"} or "delta_g" in ekl:
            case.assertLess(
                abs(float(ev)),
                bound,
                f"Expected |{path}.exponential.{ek}| < {bound}, got {ev}",
            )
    return found_pass_flag


def _assert_screening_constraints_valid(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    found_exp_summary = False
    found_pow_summary = False
    for scope in _top_and_summary_scopes(res):
        if "exponential_passes_roche_and_local_1au_and_lab" in scope:
            case.assertIs(
                scope["exponential_passes_roche_and_local_1au_and_lab"],
                True,
                f"Expected exponential_passes_roche_and_local_1au_and_lab=True in {res}",
            )
            found_exp_summary = True
        if "power_law_fails_local_1au_solar_wind" in scope:
            case.assertIs(
                scope["power_law_fails_local_1au_solar_wind"],
                True,
                f"Expected power_law_fails_local_1au_solar_wind=True in {res}",
            )
            found_pow_summary = True

    found_solar_exp = False
    found_solar_pow = False
    for path, val in _walk_items(res):
        if not isinstance(val, dict):
            continue
        leaf = path.rsplit(".", 1)[-1]
        if "roche" in leaf and not any(tok in leaf for tok in ("40au", "kuiper")):
            _assert_exp_regime_passes(case, path, val, bound=CASSINI_GAMMA_BOUND)
        elif (
            leaf in {"lab", "lab_solid", "lab_water"}
            or "lab_density" in leaf
            or "lab_water" in leaf
            or "lab_solid" in leaf
        ):
            _assert_exp_regime_passes(case, path, val, bound=MICROSCOPE_ETA_BOUND)
        elif "microscope" in leaf or "eot_wash" in leaf or "eotvos" in leaf:
            ebound = MICROSCOPE_ETA_BOUND if "microscope" in leaf else EOT_WASH_ETA_BOUND
            _assert_exp_regime_passes(case, path, val, bound=ebound)

        is_1au_solar_wind = (
            leaf == "local_1au_solar_wind"
            or ("1au" in leaf and ("wind" in leaf or "solar" in leaf) and "roche" not in leaf)
            or (
                "solar_wind" in leaf
                and not any(tok in leaf for tok in ("40au", "30au", "20au", "10au", "100au", "outer", "kuiper"))
            )
        )
        if is_1au_solar_wind:
            if _assert_exp_regime_passes(case, path, val, bound=CASSINI_GAMMA_BOUND):
                found_solar_exp = True
            pow_sub = val.get("power_law")
            if isinstance(pow_sub, dict):
                if "passes_bound" in pow_sub:
                    case.assertIs(pow_sub["passes_bound"], False, f"Expected {path}.power_law.passes_bound=False")
                    found_solar_pow = True
                if "passes" in pow_sub:
                    case.assertIs(pow_sub["passes"], False, f"Expected {path}.power_law.passes=False")
                    found_solar_pow = True
                for pk, pv in pow_sub.items():
                    if not isinstance(pv, (int, float)) or isinstance(pv, bool) or not math.isfinite(float(pv)):
                        continue
                    pkl = str(pk).lower()
                    if any(tok in pkl for tok in ("delta_kappa", "delta_g", "gamma_dev", "cassini_dev")) and "bound" not in pkl:
                        case.assertGreater(float(pv), CASSINI_GAMMA_BOUND, f"Expected {path}.power_law.{pk} > {CASSINI_GAMMA_BOUND}")
                    elif any(tok in pkl for tok in ("exceed", "violation", "ratio_to_bound")):
                        case.assertGreater(float(pv), 1.0, f"Expected {path}.power_law.{pk} > 1.0")

    case.assertTrue(
        (found_exp_summary and found_pow_summary) or (found_solar_exp and found_solar_pow),
        f"Missing exponential-pass / power-law-fail local 1 AU solar wind verification in {res}",
    )


def _assert_fl1_separation_required(case: unittest.TestCase, res: dict[str, Any]) -> None:
    case.assertIsInstance(res, dict)
    text = _serialized_lower(res)
    denial_patterns = (
        re.compile(r"\bno\s+(?:rank\s+)?separation\b"),
        re.compile(r"\b(?:rank\s+)?separation\s+(?:is\s+)?not\s+(?:needed|required)\b"),
        re.compile(r"\bnot\s+(?:need|requir)(?:e|ed|ing)?\s+(?:rank\s+)?separation\b"),
        re.compile(r"\bkappa\s*env\s*(?:=|==|equals)\s*kappa\s*dev\b"),
        re.compile(r"\bkappa\s*env\s+and\s+kappa\s*dev\s+(?:are|is)\s+(?:identical|equal|the\s+same)\b"),
    )

    checked_fl1_signal = False
    for path, val in _walk_items(res):
        leaf = path.rsplit(".", 1)[-1]
        if isinstance(val, str):
            norm_s = re.sub(r"[\s_-]+", " ", val.lower())
            for pat in denial_patterns:
                case.assertIsNone(
                    pat.search(norm_s),
                    f"Forbidden FL-1 denial pattern {pat.pattern!r} in {path}={val!r}",
                )
        elif isinstance(val, bool):
            leaf_norm = re.sub(r"[\s_-]+", " ", leaf)
            if "kappa_env" in leaf and "kappa_dev" in leaf and any(
                tok in leaf for tok in ("equal", "same", "identical", "conflat")
            ):
                case.assertIs(val, False, f"Forbidden FL-1 conflation flag {path}={val} in {res}")
            elif leaf == "requires_rank_r_gt_1_separation":
                case.assertIs(val, True, f"Expected {path}=True in {res}")
                checked_fl1_signal = True
            elif "separat" in leaf or (
                any(tok in leaf for tok in ("fl1", "fl-1", "rank"))
                and any(tok in leaf for tok in ("need", "requir"))
            ):
                if re.search(r"\b(?:no|not|without|unnecessary|skip)\b", leaf_norm):
                    case.assertIs(val, False, f"Forbidden FL-1 denial flag {path}={val} in {res}")
                else:
                    case.assertIs(val, True, f"Expected FL-1 {path}=True in {res}")
                    checked_fl1_signal = True
        elif isinstance(val, (int, float)) and math.isfinite(float(val)):
            if any(tok in path for tok in ("fl1", "fl-1", "rank_separation")) and (
                "violation" in leaf or "exceed" in leaf
            ):
                case.assertGreater(float(val), 1e10, f"Expected FL-1 {path} > 1e10 in {res}")
                checked_fl1_signal = True

    case.assertTrue(
        checked_fl1_signal,
        f"Missing positive FL-1 rank-separation signal in {res}",
    )
    case.assertTrue(
        ("kappa_env" in text and "kappa_dev" in text)
        or ("ambient" in text and "device" in text)
        or ("fl-1" in text and "separat" in text),
        f"Expected explicit FL-1 kappa_env vs kappa_dev separation in {res}",
    )


def _find_pathway_status(obj: Any, pathway_num: int) -> str | None:
    if not isinstance(obj, dict):
        return None
    if pathway_num == 1:
        pos_tokens = ("pathway_1", "pathway 1", "pathway1", "t1_contraction", "kappa_t1")
        neg_tokens = ("pathway_2", "pathway 2", "pathway2", "pi_conformal", "conformal", "p2")
        exact_p = {"p1", "p1_status", "p1_verdict", "p1_outcome", "p1_criteria"}
        prefix = "p1_"
    else:
        pos_tokens = ("pathway_2", "pathway 2", "pathway2", "pi_conformal", "conformal_bridge")
        neg_tokens = ("pathway_1", "pathway 1", "pathway1", "t1_contraction", "kappa_t1", "p1")
        exact_p = {"p2", "p2_status", "p2_verdict", "p2_outcome", "p2_criteria"}
        prefix = "p2_"

    for raw_k, val in obj.items():
        k = str(raw_k).lower()
        if any(neg in k for neg in neg_tokens):
            continue
        is_match = k in exact_p or k.startswith(prefix) or any(tok in k for tok in pos_tokens)
        if is_match:
            if isinstance(val, str) and val.strip():
                if any(st in k for st in ("status", "verdict", "outcome")) or val.strip().upper() in (
                    PATHWAY1_STATUS_VALUES | {"REFUTED"}
                ):
                    return val.strip().upper()
            elif isinstance(val, dict):
                for sk in ("status", "verdict", "outcome"):
                    if sk in val and isinstance(val[sk], str) and val[sk].strip():
                        return val[sk].strip().upper()
                for subk in ("criteria", "evaluation", "result"):
                    sub = val.get(subk)
                    if isinstance(sub, dict):
                        for sk in ("status", "verdict", "outcome"):
                            if sk in sub and isinstance(sub[sk], str) and sub[sk].strip():
                                return sub[sk].strip().upper()
    for val in obj.values():
        if isinstance(val, dict):
            found = _find_pathway_status(val, pathway_num)
            if found is not None:
                return found
    return None


def _assert_summary_matches_pathways(
    case: unittest.TestCase,
    summary: dict[str, Any],
    *,
    expected_p1: str | None,
    require_p2: bool = True,
) -> None:
    case.assertIsInstance(summary, dict)
    p1_stat = _find_pathway_status(summary, 1)
    p2_stat = _find_pathway_status(summary, 2)
    if expected_p1 is not None:
        case.assertIsNotNone(p1_stat, f"Missing Pathway 1 status in summary: {summary}")
        case.assertNotEqual(p1_stat, "REFUTED", f"Pathway 1 unexpectedly REFUTED in {summary}")
        case.assertEqual(
            p1_stat,
            expected_p1.strip().upper(),
            f"Pathway 1 status mismatch in {summary}: {p1_stat!r} != {expected_p1!r}",
        )
    if require_p2:
        case.assertIsNotNone(p2_stat, f"Missing Pathway 2 status in summary: {summary}")
        case.assertEqual(p2_stat, "REFUTED", f"Expected Pathway 2 REFUTED in {summary}, got {p2_stat!r}")


def _assert_cli_stdout_valid(case: unittest.TestCase, stdout: str, *, expected_p1: str) -> None:
    stripped = stdout.strip()
    case.assertGreater(len(stripped), 50)
    out = stdout.lower()
    case.assertTrue(
        ("th-det" in out or "native" in out) and ("fit" in out or "fitted" in out),
        f"Missing Native-vs-Fitted accounting in CLI stdout: {stdout[:300]}",
    )

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError:
        parsed = None

    if isinstance(parsed, dict):
        _assert_summary_matches_pathways(case, parsed, expected_p1=expected_p1, require_p2=True)
        return

    p1_id_pat = re.compile(r"\bpathway[\s_]*1(?:_[a-z0-9_]+)?\b")
    p2_id_pat = re.compile(r"\bpathway[\s_]*2(?:_[a-z0-9_]+)?\b")
    p12_split_pat = re.compile(r"(?=\bpathway[\s_]*[12](?:_[a-z0-9_]+)?\b)")
    neg_prefix_pat = r"\b(?:not|never|no|non|neither|nor|cannot|can't|fails|failed|rejected|refuted)\b"

    case.assertIsNotNone(
        p1_id_pat.search(out),
        f"Missing Pathway 1 identifier in CLI stdout: {stdout[:300]}",
    )
    case.assertIsNotNone(
        p2_id_pat.search(out),
        f"Missing Pathway 2 identifier in CLI stdout: {stdout[:300]}",
    )

    p1_low = expected_p1.strip().lower()
    case.assertTrue(
        p1_low in out or p1_low.replace("_", " ") in out,
        f"Missing Pathway 1 status {expected_p1!r} in CLI stdout: {stdout[:300]}",
    )
    case.assertIn("refuted", out)

    clauses: list[str] = []
    for raw_line in re.split(r"\r?\n|[;|]", out):
        parts = p12_split_pat.split(raw_line)
        clauses.extend(p.strip() for p in parts if p.strip())

    p1_has_expected = False
    p2_has_unnegated_refuted = False

    for cl in clauses:
        has_p1 = bool(p1_id_pat.search(cl))
        has_p2 = bool(p2_id_pat.search(cl))
        if has_p1 and not has_p2:
            if p1_low in cl or p1_low.replace("_", " ") in cl:
                p1_has_expected = True
            for m in re.finditer(r"\brefuted\b", cl):
                prefix = cl[max(0, m.start() - 30) : m.start()]
                if not re.search(r"\b(?:not|never|non|neither|nor)\b", prefix):
                    case.fail(f"Pathway 1 paired with unnegated 'refuted' in CLI output: {cl!r}")
        elif has_p2 and not has_p1:
            if re.search(r"\b(?:not|never|non)\s+refuted\b", cl):
                case.fail(f"Pathway 2 paired with negated refutation in CLI output: {cl!r}")
            for m in re.finditer(r"\brefuted\b", cl):
                prefix = cl[max(0, m.start() - 30) : m.start()]
                if not re.search(r"\b(?:not|never|non|neither|nor)\b", prefix):
                    p2_has_unnegated_refuted = True
            for bad_pat in (
                r"\bviable(?:_provisional)?\b",
                r"\bpartial[\s_]+limitation\b",
                r"\bpending\b",
            ):
                for m in re.finditer(bad_pat, cl):
                    prefix = cl[max(0, m.start() - 35) : m.start()]
                    if not re.search(neg_prefix_pat, prefix):
                        case.fail(f"Pathway 2 paired with unnegated {m.group(0)!r} in CLI output: {cl!r}")

    for block in p12_split_pat.split(out):
        if p1_id_pat.match(block.lstrip()) and not p2_id_pat.search(block):
            if p1_low in block or p1_low.replace("_", " ") in block:
                p1_has_expected = True
            if re.search(r"\b(?:status|verdict|outcome)\s*[:=]\s*refuted\b", block):
                case.fail(f"Pathway 1 block reports status=REFUTED: {block!r}")
        elif p2_id_pat.match(block.lstrip()) and not p1_id_pat.search(block):
            if re.search(r"\b(?:status|verdict|outcome)\s*[:=]\s*refuted\b", block):
                p2_has_unnegated_refuted = True
            if re.search(
                r"\b(?:status|verdict|outcome)\s*[:=]\s*(?:viable(?:_provisional)?|partial[\s_]+limitation|pending)\b",
                block,
            ):
                case.fail(f"Pathway 2 block reports non-refuted status: {block!r}")

    case.assertTrue(
        p1_has_expected,
        f"No Pathway 1 clause/block reports {expected_p1!r} in CLI output: {stdout[:300]}",
    )
    case.assertTrue(
        p2_has_unnegated_refuted,
        f"No Pathway 2 clause/block reports unnegated 'refuted' in CLI output: {stdout[:300]}",
    )


# ═══════════════════════════════════════════════════════════════════════════
# TIER 1: ISOLATED FEATURE COVERAGE (53 Tests across all 10 feature areas)
# ═══════════════════════════════════════════════════════════════════════════


class TestTier1F1aGitBranch(unittest.TestCase):
    """F1a: Git branch creation & isolation from main (5 tests)."""

    def test_f1a_current_branch_is_revival_branch(self) -> None:
        res = _git("rev-parse", "--abbrev-ref", "HEAD")
        self.assertEqual(res.returncode, 0, res.stderr)
        branch = res.stdout.strip()
        self.assertEqual(branch, REVIVAL_BRANCH)
        self.assertNotEqual(branch, "main")

    def test_f1a_branch_exists_and_descends_from_main(self) -> None:
        ref = _git("show-ref", "--verify", f"refs/heads/{REVIVAL_BRANCH}")
        self.assertEqual(ref.returncode, 0, ref.stderr)
        anc = _git("merge-base", "--is-ancestor", "main", REVIVAL_BRANCH)
        self.assertEqual(anc.returncode, 0, anc.stderr)
        cnt = _git("rev-list", "--count", f"main..{REVIVAL_BRANCH}")
        self.assertEqual(cnt.returncode, 0, cnt.stderr)
        self.assertGreaterEqual(int(cnt.stdout.strip()), 1)

    def test_f1a_main_pinned_at_baseline_commit(self) -> None:
        local_main = _git("rev-parse", "refs/heads/main")
        remote_main = _git("rev-parse", "refs/remotes/origin/main")
        self.assertEqual(local_main.returncode, 0)
        self.assertEqual(remote_main.returncode, 0)
        self.assertEqual(local_main.stdout.strip(), MAIN_BASELINE_SHA)
        self.assertEqual(remote_main.stdout.strip(), MAIN_BASELINE_SHA)
        div = _git("rev-list", "--count", "origin/main..main")
        self.assertEqual(int(div.stdout.strip()), 0)

    def test_f1a_m1_artifacts_committed_on_branch_not_main(self) -> None:
        on_revival = _git("ls-tree", "--name-only", REVIVAL_BRANCH, "--", "det8/models/galaxy_observables.py")
        on_main = _git("ls-tree", "--name-only", "main", "--", "det8/models/galaxy_observables.py")
        self.assertEqual(on_revival.returncode, 0)
        self.assertEqual(on_main.returncode, 0)
        self.assertEqual(on_revival.stdout.strip(), "det8/models/galaxy_observables.py")
        self.assertEqual(on_main.stdout.strip(), "")

    def test_f1a_branch_commit_history_excludes_merge_to_main(self) -> None:
        head_sha = _git("rev-parse", "HEAD").stdout.strip()
        self.assertNotEqual(head_sha, MAIN_BASELINE_SHA)
        branches = _git("branch", "--contains", "HEAD")
        self.assertEqual(branches.returncode, 0)
        names = [line.lstrip("* ").strip() for line in branches.stdout.splitlines() if line.strip()]
        self.assertIn(REVIVAL_BRANCH, names)
        self.assertNotIn("main", names)


class TestTier1F1bRemotePushAndHygiene(unittest.TestCase):
    """F1b: Offline-safe remote readiness, main integrity, and clean execution hygiene (5 tests)."""

    def test_f1b_origin_remote_configured_correctly(self) -> None:
        url = _git("remote", "get-url", "origin")
        self.assertEqual(url.returncode, 0, url.stderr)
        self.assertEqual(url.stdout.strip(), ORIGIN_URL)
        fetch = _git("config", "--get-all", "remote.origin.fetch")
        self.assertEqual(fetch.returncode, 0, fetch.stderr)
        self.assertIn("+refs/heads/*:refs/remotes/origin/*", fetch.stdout)

    def test_f1b_main_unchanged_and_equal_to_origin_main(self) -> None:
        ahead = _git("rev-list", "--count", "origin/main..main")
        behind = _git("rev-list", "--count", "main..origin/main")
        self.assertEqual(int(ahead.stdout.strip()), 0)
        self.assertEqual(int(behind.stdout.strip()), 0)
        self.assertEqual(_git("rev-parse", "main").stdout.strip(), MAIN_BASELINE_SHA)

    def test_f1b_branch_push_readiness_and_optional_remote_ref_parity(self) -> None:
        self.assertEqual(_git("merge-base", "--is-ancestor", "main", "HEAD").returncode, 0)
        self.assertGreaterEqual(int(_git("rev-list", "--count", "main..HEAD").stdout.strip()), 1)
        diff_files = set(_git("diff", "--name-only", "main...HEAD").stdout.splitlines())
        self.assertFalse(diff_files & _snapshot_pinned_relpaths())

        remote_ref = f"refs/remotes/origin/{REVIVAL_BRANCH}"
        exists = _git("show-ref", "--verify", "--quiet", remote_ref)
        if exists.returncode == 0:
            remote_sha = _git("rev-parse", remote_ref).stdout.strip()
            head_sha = _git("rev-parse", "HEAD").stdout.strip()
            self.assertEqual(remote_sha, head_sha)
            self.assertEqual(int(_git("rev-list", "--count", f"{remote_ref}..HEAD").stdout.strip()), 0)

    def test_f1b_clean_execution_idempotence(self) -> None:
        before = _git("status", "--porcelain").stdout
        go = _import_observables()
        report = go.load_sparc_subset_diagnostic()
        self.assertTrue(report["parsed_ok"])
        snap = _run_cmd([sys.executable, "-B", "scripts/check_review_snapshot.py"])
        self.assertEqual(snap.returncode, 0, snap.stdout + snap.stderr)
        after = _git("status", "--porcelain").stdout
        self.assertEqual(before, after)

    def test_f1b_no_tracked_or_diff_bytecode_artifacts(self) -> None:
        tracked = _git("ls-files").stdout.splitlines()
        diffed = _git("diff", "--name-only", "main...HEAD").stdout.splitlines()
        for path in tracked + diffed:
            self.assertFalse(path.endswith((".pyc", ".pyo")), f"Bytecode tracked: {path}")
            self.assertNotIn("__pycache__", path, f"Pycache tracked: {path}")


class TestTier1F2GalaxyObservables(unittest.TestCase):
    """F2: Neutral galaxy observables & SPARC diagnostic loader (6 tests)."""

    def test_f2_constants_and_provenance_contract(self) -> None:
        go = _import_observables()
        rc = _import_reference_constants()
        self.assertEqual(go.G_SI, rc.NEWTONIAN_G_SI)
        self.assertEqual(go.G_SI, 6.67430e-11)
        self.assertEqual(go.C_SI, 2.99792458e8)
        self.assertEqual(go.M_SUN_KG, 1.989e30)
        self.assertEqual(go.KPC_TO_M, 3.086e19)
        self.assertEqual(go.KM_S_TO_M_S, 1000.0)
        self.assertEqual(go.OBSERVABLE_PROVENANCE["det_claim_status"], "NEUTRAL_DATA_FIXTURE")
        self.assertIn("none", str(go.OBSERVABLE_PROVENANCE["dg_warrant_impact"]).lower())

    def test_f2_datasets_counts_types_and_immutability(self) -> None:
        go = _import_observables()
        self.assertEqual(len(go.KNOWN_GALAXIES), 8)
        self.assertEqual(len(go.SAMPLE_GALAXIES), 43)
        with self.assertRaises(FrozenInstanceError):
            setattr(go.KNOWN_GALAXIES[0], "M_star", 99.0)
        with self.assertRaises(FrozenInstanceError):
            setattr(go.SAMPLE_GALAXIES[0], "v_flat", 99.0)
        for g in go.KNOWN_GALAXIES:
            self.assertIsInstance(g, go.GalaxyObservables)
            self.assertGreater(g.r_SFR / g.r_d, 1.0)
            self.assertGreater(g.V_flat, 0.0)
        for g in go.SAMPLE_GALAXIES:
            self.assertIsInstance(g, go.GalaxyParams)
            self.assertGreater(g.v_flat, 0.0)
            self.assertGreater(g.r_max, 0.0)

    def test_f2_surface_density_exponential_profile(self) -> None:
        go = _import_observables()
        g = go.KNOWN_GALAXIES[0]
        s0 = go.stellar_surface_density(0.0, g.M_star, g.r_d)
        s1 = go.stellar_surface_density(g.r_d, g.M_star, g.r_d)
        s2 = go.stellar_surface_density(2.0 * g.r_d, g.M_star, g.r_d)
        expected_0 = g.M_star / (2.0 * math.pi * g.r_d ** 2)
        self.assertAlmostEqual(s0, expected_0, delta=1e-12)
        self.assertAlmostEqual(s1, expected_0 * math.exp(-1.0), delta=1e-12)
        self.assertGreater(s0, s1)
        self.assertGreater(s1, s2)
        sfr_0 = go.sfr_surface_density(0.0, g.SFR, g.r_SFR)
        self.assertAlmostEqual(sfr_0, g.SFR / (2.0 * math.pi * g.r_SFR ** 2), delta=1e-12)

    def test_f2_enclosed_disk_and_gas_mass_helpers(self) -> None:
        go = _import_observables()
        r_kpc, m_gas, r_gas = 6.0, 5.0, 3.0
        m_1d = go.gas_mass_exponential_1d(r_kpc, m_gas, r_gas)
        m_2d = go.gas_mass_freeman_2d(r_kpc, m_gas, r_gas)
        x = r_kpc / r_gas
        self.assertAlmostEqual(m_1d - m_2d, m_gas * x * math.exp(-x), delta=1e-12)
        self.assertAlmostEqual(go.stellar_disk_mass(100.0, 10.0, 1.0), 10.0, delta=1e-12)
        self.assertAlmostEqual(go.gas_mass_freeman_2d(100.0, 5.0, 1.0), 5.0, delta=1e-12)

    def test_f2_newton_rotation_velocity_modes(self) -> None:
        go = _import_observables()
        for g in go.SAMPLE_GALAXIES:
            v_1d = go.newton_rotation_velocity(g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="1d")
            v_2d = go.newton_rotation_velocity(g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="freeman_2d")
            self.assertTrue(math.isfinite(v_1d) and v_1d > 0.0)
            self.assertTrue(math.isfinite(v_2d) and v_2d > 0.0)
            self.assertLessEqual(v_2d, v_1d)
        v_a = go.newton_rotation_velocity(2.0, 10.0, 2.0, 0.0, 0.0, gas_mode="1d")
        v_b = go.newton_rotation_velocity(2.0, 10.0, 2.0, 0.0, 0.0, gas_mode="freeman_2d")
        self.assertEqual(v_a, v_b)

    def test_f2_sparc_subset_diagnostic_real_repo_file(self) -> None:
        go = _import_observables()
        report = go.load_sparc_subset_diagnostic()
        self.assertTrue(report["exists"])
        self.assertTrue(report["parsed_ok"])
        self.assertFalse(report["raw_json_valid"])
        self.assertEqual(report["parse_mode"], "comment_stripped_wrapped_array")
        self.assertEqual(report["record_count"], 56)
        self.assertEqual(report["anomalies"]["m_gas_equals_m_star_count"], 56)
        self.assertEqual(report["anomalies"]["zero_v_flat_count"], 12)
        self.assertEqual(report["anomalies"]["positive_v_flat_count"], 44)
        self.assertEqual(report["cross_comparison"]["vs_sample_galaxies"]["overlap_count"], 17)
        self.assertEqual(report["cross_comparison"]["vs_known_galaxies"]["overlap_count"], 5)


class TestTier1F3Pathway1Physics(unittest.TestCase):
    """F3: Pathway 1 T1 contraction + reciprocal aperture physics (7 tests)."""

    def test_f3_t1_contraction_kappa_exact_formula_and_range(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        g = go.KNOWN_GALAXIES[0]
        r = 2.5
        s_star = go.stellar_surface_density(r, g.M_star, g.r_d)
        s_gas = go.stellar_surface_density(r, g.M_gas, g.r_gas)
        s_sfr = go.sfr_surface_density(r, g.SFR, g.r_SFR)
        for w_sfr in (0.0, 0.5):
            k = p1.t1_contraction_kappa(
                r, g.M_star, g.r_d, g.M_gas, g.r_gas,
                sigma_crit=0.008, SFR=g.SFR, r_SFR=g.r_SFR, w_sfr=w_sfr,
            )
            expected = math.exp(-(s_star + s_gas) / 0.008 - w_sfr * s_sfr)
            self.assertAlmostEqual(k, expected, delta=1e-12)
            self.assertGreater(k, 0.0)
            self.assertLessEqual(k, 1.0)

    def test_f3_reciprocal_aperture_g_eff_exact_formula(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        g_eff = p1.reciprocal_aperture_g_eff(0.5, beta=0.93, G=go.G_SI)
        self.assertAlmostEqual(g_eff, go.G_SI / (1.0 - 0.93 * 0.5), delta=1e-18)
        self.assertGreater(g_eff, go.G_SI)
        self.assertGreater(
            p1.reciprocal_aperture_g_eff(0.8, beta=0.93),
            p1.reciprocal_aperture_g_eff(0.3, beta=0.93),
        )
        self.assertGreater(
            p1.reciprocal_aperture_g_eff(0.5, beta=0.95),
            p1.reciprocal_aperture_g_eff(0.5, beta=0.50),
        )

    def test_f3_pathway1_rotation_velocity_both_galaxy_types_and_modes(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        for gal in (go.KNOWN_GALAXIES[0], go.SAMPLE_GALAXIES[0]):
            for mode in ("1d", "freeman_2d"):
                r = 5.0
                v_n = go.newton_rotation_velocity(r, gal.M_star, gal.r_d, gal.M_gas, gal.r_gas, gas_mode=mode)
                k = p1.t1_contraction_kappa(r, gal.M_star, gal.r_d, gal.M_gas, gal.r_gas, sigma_crit=0.008, w_sfr=0.0)
                v_p1 = p1.pathway1_rotation_velocity(r, gal, sigma_crit=0.008, beta=0.93, w_sfr=0.0, gas_mode=mode)
                self.assertAlmostEqual(v_p1, v_n / math.sqrt(1.0 - 0.93 * k), delta=1e-9)
                self.assertGreater(v_p1, v_n)

    def test_f3_f6_sign_check_8_of_8_increasing(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        res = p1.evaluate_f6_sign_check()
        _assert_f6_sign_check_8_of_8(self, res)
        for g in go.KNOWN_GALAXIES:
            k_in = p1.t1_contraction_kappa(0.1, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR)
            k_out = p1.t1_contraction_kappa(30.0, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR)
            self.assertGreater(k_out, k_in, f"Expected increasing kappa for {g.name}")

    def test_f3_sparc_fit_metrics_and_r6b_ceiling_resolved(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.93)
        _assert_sparc_fit_overall_valid(self, res, beta=0.93, check_fit_quality=True)

    def test_f3_radial_asymptotics_outer_keplerian_slope(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        res = p1.evaluate_radial_asymptotics()
        _assert_radial_asymptotics_keplerian(self, res)
        g = go.SAMPLE_GALAXIES[0]
        r_scale = max(g.r_d, g.r_gas)
        r1 = 40.0 * r_scale
        r2 = 80.0 * r_scale
        v1 = p1.pathway1_rotation_velocity(r1, g)
        v2 = p1.pathway1_rotation_velocity(r2, g)
        slope = math.log(v2 / v1) / math.log(r2 / r1)
        self.assertLess(slope, -0.45)
        self.assertGreater(slope, -0.55)

    def test_f3_screening_constraints_1au_lab_and_fl1_separation(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_screening_constraints()
        _assert_screening_constraints_valid(self, res)
        _assert_fl1_separation_required(self, res)
        text = _serialized_lower(res)
        self.assertIn("roche", text)
        self.assertTrue("wind" in text or "1e-19" in text or any(abs(x - 1e-19) < 1e-20 for x in _all_numbers(res)))
        self.assertTrue("cassini" in text or "2.3e-05" in text or "2.3e-5" in text)
        self.assertTrue("microscope" in text or "eot" in text or "eöt" in text)


class TestTier1F4Pathway1CriteriaAndManifest(unittest.TestCase):
    """F4: Pathway 1 refutation/acceptance criteria & native-vs-fitted manifest (5 tests)."""

    def test_f4_evaluate_pathway1_criteria_structure_and_verdict(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_pathway1_criteria()
        self.assertIsInstance(res, dict)
        self.assertIn("status", res)
        self.assertIn(res["status"], PATHWAY1_STATUS_VALUES)
        self.assertIn(res["status"], {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION"})

    def test_f4_criteria_reproducibility_deterministic(self) -> None:
        p1 = _import_p1()
        r1 = p1.evaluate_pathway1_criteria()
        r2 = p1.evaluate_pathway1_criteria()
        self.assertEqual(json.dumps(r1, sort_keys=True, default=str), json.dumps(r2, sort_keys=True, default=str))

    def test_f4_closure_manifest_covers_all_p1_components(self) -> None:
        p1 = _import_p1()
        manifest = p1.closure_manifest()
        self.assertIsInstance(manifest, list)
        self.assertGreaterEqual(len(manifest), 4)
        text = _serialized_lower(manifest)
        self.assertTrue("t1" in text or "contraction" in text)
        self.assertTrue("sigma_crit" in text or "critical" in text)
        self.assertTrue("beta" in text or "reciprocal" in text or "aperture" in text)
        self.assertTrue("g_si" in text or "6.6743" in text or "sparc" in text or "external" in text)

    def test_f4_closure_manifest_epistemic_tags_and_honesty(self) -> None:
        p1 = _import_p1()
        manifest = p1.closure_manifest()
        all_tags: set[str] = set()
        for entry in manifest:
            self.assertIsInstance(entry, dict)
            tags = _entry_tags(entry)
            self.assertTrue(tags, f"Missing epistemic tag in manifest entry: {entry}")
            self.assertTrue(tags <= VALID_EPISTEMIC_TAGS, f"Invalid tags {tags} in {entry}")
            all_tags |= tags
            entry_text = _serialized_lower(entry)
            if any(param in entry_text for param in ("sigma_crit", "w_sfr", "beta")):
                self.assertNotIn("TH-DET", tags, f"Fitted parameter mislabeled TH-DET: {entry}")
        self.assertIn("TH-DET", all_tags)
        self.assertIn("FIT", all_tags)

    def test_f4_criteria_reflects_outer_slope_and_screening_tradeoffs(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_pathway1_criteria()
        text = _serialized_lower(res)
        self.assertTrue("f6" in text or "sign" in text)
        self.assertTrue("slope" in text or "kepler" in text or "-0.5" in text or "asymptot" in text or "r^(-1/2)" in text)
        self.assertTrue("screen" in text or "cassini" in text or "roche" in text or "solar" in text)


class TestTier1F5Pathway2Bridge(unittest.TestCase):
    """F5: Pathway 2 Pi-conformal clock-metric bridge & variants (5 tests)."""

    def test_f5_conformal_clock_lapse_wraps_det8_core(self) -> None:
        core = _import_core()
        p2 = _import_p2()
        pi_0 = p2.conformal_clock_lapse(0.5, lambda_p=1.0)
        core_0 = core.participation_aperture(core.NodeRecord(kappa=0.5), lambda_p=1.0)
        self.assertAlmostEqual(pi_0, core_0, delta=1e-12)
        self.assertAlmostEqual(pi_0, 2.0 / 3.0, delta=1e-12)

        pi_v = p2.conformal_clock_lapse(0.5, lambda_p=1.0, velocity_fraction=0.6)
        core_v = core.participation_aperture(core.NodeRecord(kappa=0.5), velocity_fraction=0.6, lambda_p=1.0)
        self.assertAlmostEqual(pi_v, core_v, delta=1e-12)
        self.assertAlmostEqual(pi_v, 0.8 * (2.0 / 3.0), delta=1e-12)

    def test_f5_kappa_potential_phi_exact_formula(self) -> None:
        go = _import_observables()
        p2 = _import_p2()
        for kappa, lam in ((0.0, 1.0), (0.5, 1e-7), (1.0, 2.0)):
            phi = p2.kappa_potential_phi(kappa, lambda_p=lam)
            expected = (go.C_SI ** 2) * math.log1p(lam * kappa)
            if expected == 0.0:
                self.assertEqual(phi, 0.0)
            else:
                self.assertLess(abs(phi - expected) / expected, 1e-12)

    def test_f5_conformal_acceleration_1d_exposes_sign_relation(self) -> None:
        p2 = _import_p2()
        lam = 1e-7
        kappa_inc = lambda r: 1.0 - math.exp(-r / 2.0)
        res = p2.conformal_acceleration_1d(5.0, kappa_inc, lambda_p=lam, dr_kpc=1e-4)
        self.assertIsInstance(res, dict)
        a_lit, a_att = _extract_conformal_and_phi_acc(res)
        self.assertGreater(a_lit, 0.0)
        self.assertLess(a_att, 0.0)
        self.assertAlmostEqual(a_lit, -a_att, delta=1e-9 * max(1e-30, abs(a_lit)))

    def test_f5_conformal_acceleration_decreasing_kappa_check(self) -> None:
        p2 = _import_p2()
        kappa_dec = lambda r: math.exp(-r / 2.0)
        res = p2.conformal_acceleration_1d(5.0, kappa_dec, lambda_p=1e-7, dr_kpc=1e-4)
        a_lit, a_att = _extract_conformal_and_phi_acc(res)
        self.assertLess(a_lit, 0.0)
        self.assertGreater(a_att, 0.0)
        self.assertAlmostEqual(a_lit, -a_att, delta=1e-9 * max(1e-30, abs(a_lit)))

    def test_f5_explore_modified_variants_runs_and_reports(self) -> None:
        p2 = _import_p2()
        res = p2.explore_modified_variants()
        self.assertIsInstance(res, dict)
        self.assertGreaterEqual(len(res), 1)
        text = _serialized_lower(res)
        self.assertTrue("non-conformal" in text or "non_conformal" in text or "spatial" in text or "screen" in text)
        self.assertTrue("mass" in text or "gamma" in text or "lensing" in text or "clock" in text)


class TestTier1F6Pathway2Audits(unittest.TestCase):
    """F6: Pathway 2 refutation/acceptance & 4-check audit (6 tests)."""

    def test_f6_audit_sign_consistency_exposes_t1_sign_clash(self) -> None:
        p2 = _import_p2()
        res = p2.audit_sign_consistency()
        _assert_audit_failed(self, res)
        text = _serialized_lower(res)
        self.assertTrue("sign" in text or "repulsive" in text or "outward" in text)
        self.assertTrue(
            res.get("passed") is False
            or "clash" in text
            or "inconsisten" in text
            or "refut" in text
            or "fail" in text
        )

    def test_f6_audit_conformal_ppn_lensing_cassini_failure(self) -> None:
        p2 = _import_p2()
        res = p2.audit_conformal_ppn_lensing()
        _assert_audit_failed(self, res)
        nums = _all_numbers(res)
        self.assertIn(-1.0, nums)
        self.assertTrue(any(abs(x - 2.0) < 1e-9 for x in nums) or any(abs(x - CASSINI_GAMMA_BOUND) < 1e-8 for x in nums))
        text = _serialized_lower(res)
        self.assertTrue("cassini" in text or "gamma" in text or "lensing" in text)
        self.assertTrue(
            res.get("passed") is False
            or "fail" in text
            or "refut" in text
            or "violat" in text
        )

    def test_f6_audit_sparc_mass_scaling_tully_fisher_failure(self) -> None:
        p2 = _import_p2()
        res = p2.audit_sparc_mass_scaling()
        _assert_audit_failed(self, res)
        text = _serialized_lower(res)
        self.assertTrue("tully" in text or "btfr" in text or "mass" in text or "sparc" in text)
        self.assertTrue(
            res.get("passed") is False
            or "fail" in text
            or "refut" in text
            or "independen" in text
        )

    def test_f6_audit_clock_scale_gap_nist_1e11_clash(self) -> None:
        p2 = _import_p2()
        res = p2.audit_clock_scale_gap()
        _assert_clock_scale_gap_failure(self, res)
        text = _serialized_lower(res)
        self.assertTrue("nist" in text or "clock" in text or "1e-18" in text or "2e-18" in text)

    def test_f6_evaluate_pathway2_criteria_verdict_refuted(self) -> None:
        p2 = _import_p2()
        res = p2.evaluate_pathway2_criteria()
        _assert_pathway2_refuted(self, res)

    def test_f6_pathway2_closure_manifest_tags(self) -> None:
        p2 = _import_p2()
        manifest = p2.closure_manifest()
        self.assertIsInstance(manifest, list)
        self.assertGreaterEqual(len(manifest), 3)
        for entry in manifest:
            self.assertIsInstance(entry, dict)
            tags = _entry_tags(entry)
            self.assertTrue(tags, f"Missing epistemic tag in P2 manifest: {entry}")
            self.assertTrue(tags <= VALID_EPISTEMIC_TAGS)
            etxt = _serialized_lower(entry)
            if "conformal" in etxt or "ppn" in etxt or "lambda_p" in etxt:
                self.assertNotIn("TH-DET", tags, f"P2 conformal/fitted assumption mislabeled TH-DET: {entry}")


class TestTier1F7DocsAndGates(unittest.TestCase):
    """F7: 13-doc alignment, re-entry gates & native-vs-fitted accounting (6 tests)."""

    def test_f7_all_13_required_docs_exist_and_nonempty(self) -> None:
        self.assertEqual(len(EXPECTED_DOCS), 13)
        for rel in EXPECTED_DOCS:
            p = REPO_ROOT / rel
            self.assertTrue(p.is_file(), f"Missing required doc: {rel}")
            txt = p.read_text(encoding="utf-8")
            self.assertGreater(len(txt.strip()), 200, f"Doc unexpectedly small: {rel}")

    def test_f7_physics_and_model_card_record_revival_and_pathways(self) -> None:
        for rel in ("PHYSICS.md", "MODEL_CARD.md"):
            txt = _read_doc(rel).lower()
            self.assertIn("pathway 1", txt, rel)
            self.assertIn("pathway 2", txt, rel)
            self.assertTrue("t1" in txt or "contraction" in txt, rel)
            self.assertTrue("conformal" in txt or "pi-conformal" in txt or "π-conformal" in txt, rel)
            self.assertIn("refut", txt, rel)

    def test_f7_reentry_gates_relaxed_vs_strict_explicit(self) -> None:
        for rel in ("GOVERNANCE.md", "docs/CONTINUUM_LIMIT_FRAMEWORK.md"):
            txt = _read_doc(rel).lower()
            self.assertIn("relax", txt, rel)
            self.assertIn("strict", txt, rel)
            self.assertTrue("fit" in txt or "calibrat" in txt, rel)
            self.assertTrue("quarantine" in txt or "anti-smuggling" in txt or "status m" in txt, rel)
        arch = _read_doc("archive/retired_kappa_gravity.md").lower()
        self.assertTrue("revival" in arch or "pathway 1" in arch)
        self.assertIn("quarantine", arch)

    def test_f7_ledgers_updated_with_revival_probes_and_falsifiers(self) -> None:
        fals = _read_doc("FALSIFICATION_LEDGER.md").lower()
        nov = _read_doc("NOVELTY_LEDGER.md").lower()
        self.assertIn("fl-1", fals)
        self.assertTrue("pathway 1" in fals or "t1" in fals)
        self.assertTrue("pathway 2" in fals or "conformal" in fals)
        self.assertIn("cost", nov)
        self.assertTrue("pathway 1" in nov or "pathway 2" in nov or "kappa" in nov)

    def test_f7_native_vs_fitted_documented_across_track_docs(self) -> None:
        for rel in ("docs/applied_physics.md", "docs/track_b/gravity.md", "docs/observable_anchoring.md"):
            txt = _read_doc(rel).lower()
            self.assertTrue("th-det" in txt or "native" in txt or "corr" in txt, rel)
            self.assertTrue("fit" in txt or "fitted" in txt or "calibrat" in txt, rel)
            self.assertTrue("pathway 1" in txt or "revival" in txt or "kappa" in txt, rel)
        anch = _read_doc("docs/observable_anchoring.md").lower()
        self.assertTrue(
            "galaxy_observables" in anch or ("known_galaxies" in anch and "sparc" in anch),
            "docs/observable_anchoring.md must document galaxy_observables or KNOWN_GALAXIES + SPARC",
        )

    def test_f7_readme_roadmap_next_steps_consistent_with_verdicts(self) -> None:
        for rel in ("README.md", "ROADMAP.md", "NEXT_STEPS.md"):
            txt = _read_doc(rel).lower()
            self.assertTrue("revival" in txt or "pathway 1" in txt, rel)
            self.assertTrue("pathway 2" in txt or "conformal" in txt, rel)


class TestTier1F8RunnerCoreAndQuarantine(unittest.TestCase):
    """F8 & Q&S: Unified runner, core alignment, unit suite, quarantine & snapshot (8 tests)."""

    def test_f8_unified_runner_api_parity(self) -> None:
        p1 = _import_p1()
        p2 = _import_p2()
        rev = _import_revival()
        summary = rev.run_all_pathway_evaluations()
        p1_status = p1.evaluate_pathway1_criteria()["status"]
        _assert_summary_matches_pathways(self, summary, expected_p1=p1_status, require_p2=True)
        txt = _serialized_lower(summary)
        self.assertTrue(("th-det" in txt or "native" in txt) and ("fit" in txt or "fitted" in txt))
        self.assertTrue({"TH-DET", "FIT"} <= set(_extract_manifest_tags(p1.closure_manifest())))
        self.assertGreaterEqual(len(p2.closure_manifest()), 3)

    def test_f8_unified_runner_cli_subprocess_exit_zero(self) -> None:
        proc = _run_cmd([sys.executable, "-B", "-m", "det8.models.kappa_gravity_revival"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        expected_p1 = _import_p1().evaluate_pathway1_criteria()["status"]
        _assert_cli_stdout_valid(self, proc.stdout, expected_p1=expected_p1)

    def test_f8_unit_test_suite_passes_via_unittest(self) -> None:
        test_file = REPO_ROOT / "det8" / "tests" / "test_kappa_gravity_revival.py"
        self.assertTrue(test_file.is_file(), f"Missing {test_file}")
        proc = _run_cmd([sys.executable, "-B", "-m", "unittest", "det8/tests/test_kappa_gravity_revival.py", "-v"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        combined = proc.stdout + proc.stderr
        self.assertIn("OK", combined)

    def test_f8_run_tests_py_registers_revival_section(self) -> None:
        rt_src = (REPO_ROOT / "run_tests.py").read_text(encoding="utf-8")
        self.assertIn("test_legacy_gravity_quarantine", rt_src)
        self.assertTrue(
            "kappa_gravity_revival" in rt_src or "test_kappa_gravity_revival" in rt_src,
            "run_tests.py must register kappa-gravity revival checks",
        )
        proc = _run_cmd(
            [
                sys.executable,
                "-B",
                "-c",
                "import run_tests; run_tests.test_legacy_gravity_quarantine(); "
                "assert run_tests.FAIL == 0 and run_tests.ERROR == 0",
            ]
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_f8_core_4_modules_alignment_notes_present(self) -> None:
        df = importlib.import_module("det8.models.det_falsification")
        du = importlib.import_module("det8.models.det_units")
        core = _import_core()
        lq = _import_quarantine()

        self.assertIsInstance(df.gravity_emergence_note(), dict)
        self.assertIsInstance(du.dimensional_analysis(), dict)
        self.assertGreater(core.participation_aperture(core.NodeRecord()), 0.0)
        self.assertEqual(lq.quarantine_summary()["active_empirical_claims_from_retired_modules"], 0)

        for rel in EXPECTED_CORE_ALIGNED:
            txt = (REPO_ROOT / rel).read_text(encoding="utf-8").lower()
            self.assertTrue(
                any(
                    tok in txt
                    for tok in (
                        "revival",
                        "kappa_t1_contraction",
                        "kappa_gravity_revival",
                        "pi_conformal_bridge",
                        "galaxy_observables",
                    )
                ),
                f"Expected revival alignment note in {rel}",
            )

    def test_f8_quarantine_28_retired_and_zero_active_imports(self) -> None:
        lq = _import_quarantine()
        self.assertEqual(len(lq.FULLY_RETIRED), 28)
        retired_set = set(lq.FULLY_RETIRED)
        models_dir = REPO_ROOT / "det8" / "models"
        for py_path in sorted(models_dir.glob("*.py")):
            mod_name = f"det8.models.{py_path.stem}"
            source = py_path.read_text(encoding="utf-8")
            if mod_name in retired_set:
                self.assertIn("QUARANTINE = quarantine_record(__name__)", source, mod_name)
                continue
            tree = ast.parse(source, filename=str(py_path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module)
                elif isinstance(node, ast.Import):
                    imported.update(alias.name for alias in node.names)
            self.assertFalse(imported & retired_set, f"{py_path.name} imports retired {imported & retired_set}")

    def test_f8_review_snapshot_71_files_unmodified(self) -> None:
        proc = _run_cmd([sys.executable, "-B", "scripts/check_review_snapshot.py"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "match")
        self.assertEqual(payload["declared_files"], 71)
        self.assertEqual(payload["matched_files"], 71)
        self.assertEqual(payload["executed_files"], 0)

    def test_f8_research_checks_manifest_intact(self) -> None:
        proc = _run_cmd([sys.executable, "-B", "scripts/run_research_checks.py", "--check"])
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertTrue(payload["successful"])
        self.assertEqual(payload["mode"], "check")


# ═══════════════════════════════════════════════════════════════════════════
# TIER 2: BOUNDARY & CORNER CASES (39 Tests >= 37)
# ═══════════════════════════════════════════════════════════════════════════


class TestTier2F1GitBoundaries(unittest.TestCase):
    """F1a/F1b boundary & corner cases (3 tests)."""

    def test_t2_f1a_merge_base_main_head_equals_baseline(self) -> None:
        mb = _git("merge-base", "main", "HEAD")
        self.assertEqual(mb.returncode, 0)
        self.assertEqual(mb.stdout.strip(), MAIN_BASELINE_SHA)
        behind = _git("rev-list", "--count", "HEAD..main")
        self.assertEqual(int(behind.stdout.strip()), 0)

    def test_t2_f1a_head_is_symbolic_branch_not_detached(self) -> None:
        sym = _git("symbolic-ref", "-q", "HEAD")
        self.assertEqual(sym.returncode, 0, sym.stderr)
        self.assertEqual(sym.stdout.strip(), f"refs/heads/{REVIVAL_BRANCH}")

    def test_t2_f1b_show_ref_heads_distinct_and_main_unmoved(self) -> None:
        main_sha = _git("rev-parse", "refs/heads/main").stdout.strip()
        rev_sha = _git("rev-parse", f"refs/heads/{REVIVAL_BRANCH}").stdout.strip()
        orig_main_sha = _git("rev-parse", "refs/remotes/origin/main").stdout.strip()
        self.assertEqual(main_sha, MAIN_BASELINE_SHA)
        self.assertEqual(orig_main_sha, MAIN_BASELINE_SHA)
        self.assertNotEqual(rev_sha, main_sha)


class TestTier2F2ObservablesBoundaries(unittest.TestCase):
    """F2 boundary & corner cases (6 tests)."""

    def test_t2_f2_zero_mass_and_zero_scale_length_identities(self) -> None:
        go = _import_observables()
        self.assertEqual(go.stellar_surface_density(1.0, 0.0, 2.0), 0.0)
        self.assertEqual(go.stellar_surface_density(1.0, 10.0, 0.0), 0.0)
        self.assertEqual(go.sfr_surface_density(1.0, 0.0, 2.0), 0.0)
        self.assertEqual(go.sfr_surface_density(1.0, 1.0, 0.0), 0.0)
        self.assertEqual(go.stellar_disk_mass(0.0, 10.0, 2.0), 0.0)
        self.assertEqual(go.gas_mass_exponential_1d(0.0, 5.0, 3.0), 0.0)
        self.assertEqual(go.gas_mass_freeman_2d(0.0, 5.0, 3.0), 0.0)
        self.assertEqual(go.newton_rotation_velocity(2.0, 0.0, 2.0, 0.0, 2.0), 0.0)

    def test_t2_f2_rejects_bool_negative_nan_inf_inputs(self) -> None:
        go = _import_observables()
        for bad in (True, False, -1e-9, float("nan"), float("inf"), float("-inf")):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    go.stellar_surface_density(bad, 10.0, 2.0)
                with self.assertRaises(ValueError):
                    go.sfr_surface_density(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.stellar_disk_mass(bad, 10.0, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_exponential_1d(1.0, bad, 2.0)
                with self.assertRaises(ValueError):
                    go.gas_mass_freeman_2d(1.0, 5.0, bad)
                with self.assertRaises(ValueError):
                    go.newton_rotation_velocity(bad, 10.0, 2.0, 5.0, 2.0)
        with self.assertRaises(ValueError):
            go.newton_rotation_velocity(0.0, 10.0, 2.0, 5.0, 2.0)

    def test_t2_f2_freeman_2d_continuity_across_taylor_thresholds(self) -> None:
        go = _import_observables()
        m_gas, r_gas = 5.0, 2.0
        for boundary in (1e-4, 0.01):
            g_left = go.gas_mass_freeman_2d(math.nextafter(boundary, 0.0) * r_gas, m_gas, r_gas)
            g_at = go.gas_mass_freeman_2d(boundary * r_gas, m_gas, r_gas)
            g_right = go.gas_mass_freeman_2d(math.nextafter(boundary, 1.0) * r_gas, m_gas, r_gas)
            self.assertLess(abs(g_at - g_left) / g_at, 1e-11)
            self.assertLess(abs(g_right - g_at) / g_at, 1e-11)

    def test_t2_f2_extreme_finite_float_stability(self) -> None:
        go = _import_observables()
        self.assertEqual(go.stellar_disk_mass(1e308, 10.0, 0.5), 10.0)
        self.assertEqual(go.gas_mass_freeman_2d(1e308, 5.0, 0.5), 5.0)
        v_ext = go.newton_rotation_velocity(1e308, 10.0, 0.5, 5.0, 0.5, gas_mode="freeman_2d")
        self.assertTrue(math.isfinite(v_ext) and v_ext >= 0.0)
        self.assertTrue(math.isfinite(go.stellar_surface_density(1.0, 10.0, 1e155)))
        self.assertEqual(go.stellar_surface_density(1.0, 10.0, 1e200), 0.0)

    def test_t2_f2_sparc_diagnostic_empty_missing_dir_binary_corrupt(self) -> None:
        go = _import_observables()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            self.assertEqual(go.load_sparc_subset_diagnostic(root / "missing.json")["parse_mode"], "missing_file")
            self.assertEqual(go.load_sparc_subset_diagnostic(root)["parse_mode"], "not_a_file")
            bad_bin = root / "bad.bin"
            bad_bin.write_bytes(b"\xff\xfe\x00\x00")
            self.assertEqual(go.load_sparc_subset_diagnostic(bad_bin)["parse_mode"], "decode_error")
            empty_p = root / "empty.json"
            empty_p.write_text("", encoding="utf-8")
            self.assertEqual(go.load_sparc_subset_diagnostic(empty_p)["parse_mode"], "empty")
            corrupt = root / "corrupt.json"
            corrupt.write_text('{"name": "DDO 154", "M_star": 0.28, "r_d": 0.37, "M_gas": 0.25, "V_flat": 47.0},\n{"broken": NaN_BAD}\n', encoding="utf-8")
            rep = go.load_sparc_subset_diagnostic(corrupt)
            self.assertFalse(rep["parsed_ok"])
            self.assertEqual(rep["parse_mode"], "line_recovery")
            self.assertEqual(rep["record_count"], 1)

    def test_t2_f2_sparc_diagnostic_bool_nan_inf_payload_sanitization(self) -> None:
        go = _import_observables()
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "bad_nums.json"
            p.write_text(
                json.dumps([
                    {"name": "DDO 154", "M_star": True, "M_gas": True, "V_flat": False},
                    {"name": "NGC 2403", "M_star": float("nan"), "M_gas": float("nan"), "V_flat": float("nan")},
                ]),
                encoding="utf-8",
            )
            rep = go.load_sparc_subset_diagnostic(p)
            self.assertTrue(rep["parsed_ok"])
            self.assertEqual(rep["anomalies"]["m_gas_equals_m_star_count"], 0)
            self.assertEqual(rep["anomalies"]["zero_v_flat_count"], 0)
            for ov in rep["cross_comparison"]["vs_sample_galaxies"]["overlaps"]:
                self.assertIsNone(ov["M_star_ratio"])


class TestTier2F3Pathway1Boundaries(unittest.TestCase):
    """F3 boundary & corner cases (7 tests)."""

    def test_t2_f3_kappa_limits_zero_mass_and_asymptotic_r(self) -> None:
        p1 = _import_p1()
        self.assertEqual(p1.t1_contraction_kappa(1.0, 0.0, 2.0, 0.0, 2.0), 1.0)
        self.assertAlmostEqual(p1.t1_contraction_kappa(1e6, 10.0, 2.0, 5.0, 3.0), 1.0, delta=1e-12)
        k_dense = p1.t1_contraction_kappa(0.0, 1e4, 0.1, 0.0, 1.0, sigma_crit=0.008)
        self.assertGreaterEqual(k_dense, 0.0)
        self.assertLess(k_dense, 1e-10)

    def test_t2_f3_reciprocal_aperture_beta_zero_and_near_one(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        self.assertEqual(p1.reciprocal_aperture_g_eff(0.0, beta=0.93), go.G_SI)
        self.assertEqual(p1.reciprocal_aperture_g_eff(1.0, beta=0.0), go.G_SI)
        self.assertAlmostEqual(p1.reciprocal_aperture_g_eff(1.0, beta=0.999), 1000.0 * go.G_SI, delta=1e-6)

    def test_t2_f3_reciprocal_aperture_rejects_beta_ge_1_and_out_of_domain(self) -> None:
        p1 = _import_p1()
        for bad_beta in (1.0, 1.01, -0.01, float("nan"), float("inf"), True):
            with self.subTest(bad_beta=bad_beta), self.assertRaises(ValueError):
                p1.reciprocal_aperture_g_eff(0.5, beta=bad_beta)
        for bad_kappa in (-0.01, 1.01, float("nan"), float("inf"), False):
            with self.subTest(bad_kappa=bad_kappa), self.assertRaises(ValueError):
                p1.reciprocal_aperture_g_eff(bad_kappa, beta=0.5)

    def test_t2_f3_t1_contraction_rejects_invalid_params(self) -> None:
        p1 = _import_p1()
        for bad in (-0.1, float("nan"), float("inf"), True):
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    p1.t1_contraction_kappa(bad, 10.0, 2.0, 1.0, 2.0)
                with self.assertRaises(ValueError):
                    p1.t1_contraction_kappa(1.0, bad, 2.0, 1.0, 2.0)
                with self.assertRaises(ValueError):
                    p1.t1_contraction_kappa(1.0, 10.0, 2.0, 1.0, 2.0, w_sfr=bad)
        for bad_sc in (0.0, -0.01, float("nan"), float("inf"), False):
            with self.subTest(bad_sc=bad_sc), self.assertRaises(ValueError):
                p1.t1_contraction_kappa(1.0, 10.0, 2.0, 1.0, 2.0, sigma_crit=bad_sc)

    def test_t2_f3_pathway1_velocity_invalid_r_and_gas_mode(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        gal = go.SAMPLE_GALAXIES[0]
        for bad_r in (0.0, -1.0, float("nan"), float("inf"), True):
            with self.subTest(bad_r=bad_r), self.assertRaises(ValueError):
                p1.pathway1_rotation_velocity(bad_r, gal)
        with self.assertRaises(ValueError):
            p1.pathway1_rotation_velocity(5.0, gal, gas_mode="invalid_mode")

    def test_t2_f3_radial_limits_near_zero_vs_large_r(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        _assert_radial_asymptotics_keplerian(self, p1.evaluate_radial_asymptotics())
        for gal in (go.SAMPLE_GALAXIES[0], go.SAMPLE_GALAXIES[28]):  # DDO 154 (LSB) & NGC 2841 (HSB)
            r_scale = max(gal.r_d, gal.r_gas)
            r_tiny = 1e-4 * gal.r_d
            r_far1 = 40.0 * r_scale
            r_far2 = 80.0 * r_scale
            v_tiny = p1.pathway1_rotation_velocity(r_tiny, gal, gas_mode="freeman_2d")
            v_far1 = p1.pathway1_rotation_velocity(r_far1, gal, gas_mode="freeman_2d")
            v_far2 = p1.pathway1_rotation_velocity(r_far2, gal, gas_mode="freeman_2d")
            self.assertLess(v_tiny, v_far1)
            k_far1 = p1.t1_contraction_kappa(r_far1, gal.M_star, gal.r_d, gal.M_gas, gal.r_gas)
            self.assertGreater(k_far1, 0.99)
            slope = math.log(v_far2 / v_far1) / math.log(r_far2 / r_far1)
            self.assertAlmostEqual(slope, -0.5, delta=0.05)

    def test_t2_f3_sfr_weight_sensitivity_boundary(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        g = go.KNOWN_GALAXIES[0]
        k_w0 = p1.t1_contraction_kappa(1.0, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR, w_sfr=0.0)
        k_w5 = p1.t1_contraction_kappa(1.0, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR, w_sfr=5.0)
        self.assertGreater(k_w0, k_w5)
        k_out = p1.t1_contraction_kappa(30.0, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR, w_sfr=0.5)
        k_in = p1.t1_contraction_kappa(0.1, g.M_star, g.r_d, g.M_gas, g.r_gas, SFR=g.SFR, r_SFR=g.r_SFR, w_sfr=0.5)
        self.assertGreater(k_out, k_in)


class TestTier2F4Pathway1CriteriaBoundaries(unittest.TestCase):
    """F4 boundary & corner cases (5 tests)."""

    def test_t2_f4_sparc_fit_beta_zero_matches_newtonian_baseline(self) -> None:
        p1 = _import_p1()
        res_n = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.0)
        res_p = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.93)
        _assert_sparc_fit_overall_valid(self, res_n, beta=0.0, check_fit_quality=False)
        _assert_sparc_fit_overall_valid(self, res_p, beta=0.93, check_fit_quality=True)
        errs_n = _sparc_overall_error_values(res_n)
        errs_p = _sparc_overall_error_values(res_p)
        self.assertTrue(any(abs(x - 0.6722566) < 0.02 for x in errs_n), f"Expected Newtonian mean error ~0.672 in {res_n}")
        self.assertGreater(min(errs_n), max(errs_p))

    def test_t2_f4_sparc_fit_high_beta_dwarf_ceiling_scaling(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.98)
        _assert_sparc_fit_overall_valid(self, res, beta=0.98, check_fit_quality=False)
        with self.assertRaises(ValueError):
            p1.evaluate_sparc_fit(sigma_crit=0.008, beta=1.0)

    def test_t2_f4_screening_constraints_extreme_density_regimes(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_screening_constraints()
        _assert_screening_constraints_valid(self, res)
        nums = _all_numbers(res)
        self.assertTrue(any(x >= 100.0 for x in nums))  # lab density ~1000
        self.assertTrue(any(1e-22 <= x <= 1e-18 for x in nums))  # rho_crit / solar wind scale
        self.assertTrue(any(1e-4 <= x <= 2e-4 for x in nums) or "roche" in _serialized_lower(res))

    def test_t2_f4_fl1_ambient_vs_device_kappa_separation(self) -> None:
        p1 = _import_p1()
        res = p1.evaluate_screening_constraints()
        _assert_fl1_separation_required(self, res)

    def test_t2_f4_criteria_and_manifest_schema_invariants(self) -> None:
        p1 = _import_p1()
        crit = p1.evaluate_pathway1_criteria()
        self.assertIn(crit["status"], PATHWAY1_STATUS_VALUES)
        manifest = p1.closure_manifest()
        self.assertGreater(len(manifest), 0)
        for entry in manifest:
            tags = _entry_tags(entry)
            self.assertTrue(tags <= VALID_EPISTEMIC_TAGS and len(tags) >= 1)


class TestTier2F5Pathway2Boundaries(unittest.TestCase):
    """F5 boundary & corner cases (6 tests)."""

    def test_t2_f5_clock_lapse_and_phi_at_kappa_zero_and_one(self) -> None:
        go = _import_observables()
        p2 = _import_p2()
        self.assertEqual(p2.conformal_clock_lapse(0.0, lambda_p=1.0), 1.0)
        self.assertEqual(p2.kappa_potential_phi(0.0, lambda_p=1.0), 0.0)
        self.assertAlmostEqual(p2.conformal_clock_lapse(1.0, lambda_p=3.0), 0.25, delta=1e-12)
        self.assertAlmostEqual(p2.kappa_potential_phi(1.0, lambda_p=3.0), (go.C_SI ** 2) * math.log(4.0), delta=1.0)

    def test_t2_f5_lambda_p_zero_and_extreme_scales(self) -> None:
        go = _import_observables()
        p2 = _import_p2()
        self.assertEqual(p2.conformal_clock_lapse(0.7, lambda_p=0.0), 1.0)
        self.assertEqual(p2.kappa_potential_phi(0.7, lambda_p=0.0), 0.0)
        acc0 = p2.conformal_acceleration_1d(5.0, lambda r: 1.0 - math.exp(-r / 2.0), lambda_p=0.0)
        for v in _all_numbers(acc0):
            if abs(v) < 1e-6:
                self.assertAlmostEqual(v, 0.0, delta=1e-12)
        for lam in (1e-18, 1e-7, 1.0, 1e6):
            phi = p2.kappa_potential_phi(0.5, lambda_p=lam)
            self.assertTrue(math.isfinite(phi))
            expected = (go.C_SI ** 2) * math.log1p(lam * 0.5)
            self.assertLess(abs(phi - expected) / expected, 1e-12)

    def test_t2_f5_conformal_acceleration_radial_and_step_stability(self) -> None:
        p2 = _import_p2()
        cases = (
            (1e-3, lambda r: 1.0 - math.exp(-r / 2.0)),
            (40.0, lambda r: 1.0 - math.exp(-r / 10.0)),
        )
        for r, kappa_fn in cases:
            a1 = p2.conformal_acceleration_1d(r, kappa_fn, lambda_p=1e-7, dr_kpc=1e-4)
            a2 = p2.conformal_acceleration_1d(r, kappa_fn, lambda_p=1e-7, dr_kpc=1e-5)
            v1, _ = _extract_conformal_and_phi_acc(a1)
            v2, _ = _extract_conformal_and_phi_acc(a2)
            self.assertLess(abs(v1 - v2) / max(1e-30, abs(v2)), 1e-4)

    def test_t2_f5_aperture_kwargs_velocity_fraction_guard(self) -> None:
        p2 = _import_p2()
        pi_fast = p2.conformal_clock_lapse(0.5, lambda_p=1.0, velocity_fraction=0.999)
        self.assertGreater(pi_fast, 0.0)
        self.assertLess(pi_fast, 0.05)
        with self.assertRaises(ValueError):
            p2.conformal_clock_lapse(0.5, velocity_fraction=1.0)
        with self.assertRaises(ValueError):
            p2.conformal_clock_lapse(0.5, velocity_fraction=1.1)

    def test_t2_f5_rejects_out_of_domain_kappa_lambda_and_bool(self) -> None:
        p2 = _import_p2()
        for bad_k in (-0.01, 1.01, float("nan"), float("inf"), True):
            with self.subTest(bad_k=bad_k):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(bad_k, lambda_p=1.0)
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(bad_k, lambda_p=1.0)
        for bad_l in (-1e-5, float("nan"), float("inf"), False):
            with self.subTest(bad_l=bad_l):
                with self.assertRaises(ValueError):
                    p2.conformal_clock_lapse(0.5, lambda_p=bad_l)
                with self.assertRaises(ValueError):
                    p2.kappa_potential_phi(0.5, lambda_p=bad_l)

    def test_t2_f5_conformal_acceleration_zero_gradient_profile(self) -> None:
        p2 = _import_p2()
        res = p2.conformal_acceleration_1d(5.0, lambda _r: 0.5, lambda_p=1e-7)
        lit, att = _extract_conformal_and_phi_acc(res)
        self.assertAlmostEqual(lit, 0.0, delta=1e-12)
        self.assertAlmostEqual(att, 0.0, delta=1e-12)


class TestTier2F6Pathway2AuditBoundaries(unittest.TestCase):
    """F6 boundary & corner cases (5 tests)."""

    def test_t2_f6_sign_consistency_positive_negative_zero_gradients(self) -> None:
        p2 = _import_p2()
        res = p2.audit_sign_consistency()
        _assert_audit_failed(self, res)
        text = _serialized_lower(res)
        self.assertTrue("t1" in text or "increasing" in text or "positive" in text)
        self.assertTrue("outward" in text or "repulsive" in text or "clash" in text)

    def test_t2_f6_conformal_ppn_gamma_invariant_across_lambda_p(self) -> None:
        p2 = _import_p2()
        res = p2.audit_conformal_ppn_lensing()
        _assert_audit_failed(self, res)
        nums = _all_numbers(res)
        self.assertIn(-1.0, nums)
        self.assertTrue(any(abs(x - 2.0) < 1e-9 for x in nums))

    def test_t2_f6_mass_scaling_dwarf_vs_massive_hsb_saturation(self) -> None:
        go = _import_observables()
        p2 = _import_p2()
        res = p2.audit_sparc_mass_scaling()
        _assert_audit_failed(self, res)
        text = _serialized_lower(res)
        self.assertTrue(
            res.get("passed") is False or "refut" in text or "fail" in text,
            f"Expected SPARC mass-scaling audit failure in {res}",
        )
        d_phi_max = p2.kappa_potential_phi(1.0, lambda_p=2.5e-7) - p2.kappa_potential_phi(0.0, lambda_p=2.5e-7)
        ddo = next(g for g in go.SAMPLE_GALAXIES if g.name == "DDO 154")
        ngc = next(g for g in go.SAMPLE_GALAXIES if g.name == "NGC 7814")
        self.assertGreater(ngc.M_star / ddo.M_star, 100.0)
        self.assertGreater((ngc.v_flat / ddo.v_flat) ** 2, 10.0)
        self.assertGreater(d_phi_max, 0.0)

    def test_t2_f6_clock_scale_gap_threshold_boundary(self) -> None:
        ec = _import_constraints()
        p2 = _import_p2()
        best = ec.constrain_lambda_p_from_clocks(0.5)["best_bound"]
        self.assertAlmostEqual(best, 4.0e-18, delta=1e-22)
        res = p2.audit_clock_scale_gap()
        _assert_clock_scale_gap_failure(self, res)

    def test_t2_f6_pathway2_criteria_and_manifest_valid_sets(self) -> None:
        p2 = _import_p2()
        crit = p2.evaluate_pathway2_criteria()
        _assert_pathway2_refuted(self, crit)
        for entry in p2.closure_manifest():
            tags = _entry_tags(entry)
            self.assertTrue(tags <= VALID_EPISTEMIC_TAGS and len(tags) >= 1)


class TestTier2F7DocsBoundaries(unittest.TestCase):
    """F7 boundary & consistency checks across all 13 docs (2 tests)."""

    def test_t2_f7_docs_no_false_pathway2_viability_or_tag_promotion(self) -> None:
        p2_pat = re.compile(r"\bpathway\s*2\b|pi[-\s]?conformal|π[-\s]?conformal")
        claim_pat = re.compile(r"\b(?:viable(?:_provisional)?|passed\s+all)\b")
        neg_prefix_pat = re.compile(
            r"\b(?:not|never|no|non|neither|nor|cannot|can't|fails|failed|rejected|refuted)\b"
        )
        for rel in EXPECTED_DOCS:
            txt = _read_doc(rel).lower()
            self.assertNotIn("pathway 2: viable", txt, rel)
            self.assertNotIn("pathway 2 passed", txt, rel)
            for raw_line in txt.splitlines():
                for seg in re.split(r"(?<=[.!?])\s+", raw_line):
                    if p2_pat.search(seg) and claim_pat.search(seg):
                        if (
                            re.search(r"\b(?:not|never|non)\s+refuted\b", seg)
                            or re.search(r"\brefut(?:ed|ation)\s+overturned\b", seg)
                            or "overturned" in seg
                        ):
                            self.fail(f"False Pathway 2 viability claim in {rel}: {seg.strip()!r}")
                        has_unnegated_refuted = bool(
                            re.search(r"\brefuted\b", seg)
                            and not re.search(r"\b(?:not|never|non)\s+refuted\b", seg)
                        )
                        for m_v in re.finditer(r"\bviable(?:_provisional)?\b", seg):
                            prefix = seg[max(0, m_v.start() - 35) : m_v.start()]
                            if not neg_prefix_pat.search(prefix) and not has_unnegated_refuted:
                                self.fail(f"Unnegated Pathway 2 viability claim in {rel}: {seg.strip()!r}")
                        for m_p in re.finditer(r"\bpassed\s+all\b", seg):
                            prefix = seg[max(0, m_p.start() - 35) : m_p.start()]
                            if not neg_prefix_pat.search(prefix) and not has_unnegated_refuted:
                                self.fail(f"Unnegated 'passed all' for Pathway 2 in {rel}: {seg.strip()!r}")
        phys = _read_doc("PHYSICS.md").lower()
        self.assertIn("fl-1", phys)
        self.assertIn("refut", phys)

    def test_t2_f7_docs_preserve_status_m_and_quarantine_boundary(self) -> None:
        gov = _read_doc("GOVERNANCE.md").lower()
        arch = _read_doc("archive/retired_kappa_gravity.md").lower()
        self.assertIn("status m", gov)
        self.assertIn("legacy_gravity_quarantine", arch)
        self.assertIn("quarantine", gov)


class TestTier2F8InfrastructureBoundaries(unittest.TestCase):
    """F8 / Quarantine / Snapshot / Core boundary cases (5 tests)."""

    def test_t2_f8_det8_core_m0_monotone_n_under_kappa_recovery(self) -> None:
        core = _import_core()
        rec = core.NodeRecord(kappa=0.1, N=2.0)
        n_vals = [rec.N]
        core.apply_q_damage(rec, 0.5)
        dt1 = core.accumulate_proper_time(rec, delta_N=1.0, lambda_p=1.0)
        n_vals.append(rec.N)
        core.apply_q_recovery(rec, 0.4)
        dt2 = core.accumulate_proper_time(rec, delta_N=1.5, lambda_p=1.0)
        n_vals.append(rec.N)
        self.assertGreater(dt1, 0.0)
        self.assertGreater(dt2, 0.0)
        self.assertLess(n_vals[0], n_vals[1])
        self.assertLess(n_vals[1], n_vals[2])

    def test_t2_f8_quarantine_record_rejects_unregistered_module(self) -> None:
        lq = _import_quarantine()
        self.assertFalse(lq.is_fully_retired("det8.models.galaxy_observables"))
        self.assertFalse(lq.is_fully_retired("det8.models.nonexistent"))
        with self.assertRaises(KeyError):
            lq.quarantine_record("det8.models.galaxy_observables")
        with self.assertRaises(KeyError):
            lq.quarantine_record("det8.models.nonexistent")

    def test_t2_f8_snapshot_checker_tamper_and_byte_limit_in_tempdir(self) -> None:
        script = REPO_ROOT / "scripts" / "check_review_snapshot.py"
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            target = root / "pinned.txt"
            target.write_text("original\n", encoding="utf-8")
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            manifest = root / "manifest.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "checkpoint": {"commit": "0" * 40, "tree": "0" * 40},
                        "artifacts": [{"path": "pinned.txt", "sha256": digest}],
                    }
                ),
                encoding="utf-8",
            )

            ok = _run_cmd([sys.executable, "-B", str(script), "--root", str(root), "--manifest", "manifest.json"])
            self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
            self.assertEqual(json.loads(ok.stdout)["status"], "match")

            target.write_text("tampered\n", encoding="utf-8")
            bad = _run_cmd([sys.executable, "-B", str(script), "--root", str(root), "--manifest", "manifest.json"])
            self.assertEqual(bad.returncode, 1)
            self.assertEqual(json.loads(bad.stdout)["status"], "mismatch")

            manifest.write_text('{"schema_version": 1, "schema_version": 1}', encoding="utf-8")
            inv = _run_cmd([sys.executable, "-B", str(script), "--root", str(root), "--manifest", "manifest.json"])
            self.assertEqual(inv.returncode, 2)
            self.assertEqual(json.loads(inv.stdout)["status"], "invalid")

    def test_t2_f8_e2e_test_file_itself_imports_zero_retired_modules(self) -> None:
        lq = _import_quarantine()
        retired = set(lq.FULLY_RETIRED)
        source = E2E_TEST_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(E2E_TEST_PATH))
        imported: set[str] = set()
        forbidden_decorators = {"skip", "skipIf", "skipUnless", "expectedFailure"}
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                if node.module == "unittest":
                    for alias in node.names:
                        if alias.name == "mock":
                            imported.add("unittest.mock")
            elif isinstance(node, ast.Import):
                imported.update(alias.name for alias in node.names)
            elif isinstance(node, ast.FunctionDef):
                for dec in node.decorator_list:
                    dname = dec.func.attr if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute) else (
                        dec.attr if isinstance(dec, ast.Attribute) else (dec.id if isinstance(dec, ast.Name) else "")
                    )
                    self.assertNotIn(dname, forbidden_decorators, f"Forbidden decorator @{dname} on {node.name}")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotEqual(node.func.attr, "skipTest")
        self.assertFalse(imported & retired, f"E2E suite imports retired: {imported & retired}")
        self.assertNotIn("pytest", imported)
        self.assertNotIn("unittest.mock", imported)

    def test_t2_f8_git_diff_against_main_touches_zero_snapshot_files(self) -> None:
        diff_files = set(_git("diff", "--name-only", "main...HEAD").stdout.splitlines())
        status_files = {line[3:].strip() for line in _git("status", "--porcelain").stdout.splitlines() if len(line) > 3}
        self.assertFalse((diff_files | status_files) & _snapshot_pinned_relpaths())


# ═══════════════════════════════════════════════════════════════════════════
# TIER 3: CROSS-FEATURE COMBINATIONS (15 Pairwise Tests)
# ═══════════════════════════════════════════════════════════════════════════


class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Pairwise cross-feature integration & consistency tests (15 tests)."""

    def test_t3_01_branch_contains_revived_modules_not_on_main(self) -> None:
        self.assertEqual(_git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), REVIVAL_BRANCH)
        for rel in EXPECTED_REVIVED_FILES:
            self.assertTrue((REPO_ROOT / rel).is_file(), f"Missing on revival branch: {rel}")
            on_main = _git("ls-tree", "--name-only", "main", "--", rel).stdout.strip()
            self.assertEqual(on_main, "", f"Unexpectedly present on main: {rel}")

    def test_t3_02_observables_to_pathway1_rotation_pipeline(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        f6 = p1.evaluate_f6_sign_check()
        sparc = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.93)
        _assert_f6_sign_check_8_of_8(self, f6)
        _assert_sparc_fit_overall_valid(self, sparc, beta=0.93, check_fit_quality=True)
        for g in go.SAMPLE_GALAXIES[:5]:
            for mode in ("1d", "freeman_2d"):
                vn = go.newton_rotation_velocity(g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode=mode)
                vp = p1.pathway1_rotation_velocity(g.r_max, g, sigma_crit=0.008, beta=0.93, gas_mode=mode)
                k = p1.t1_contraction_kappa(g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, sigma_crit=0.008)
                self.assertAlmostEqual(vp / vn, (1.0 - 0.93 * k) ** (-0.5), delta=1e-9)

    def test_t3_03_observables_and_core_to_pathway2_acceleration(self) -> None:
        go = _import_observables()
        core = _import_core()
        p2 = _import_p2()
        g = go.SAMPLE_GALAXIES[0]
        lam = 1e-7
        kappa_fn = lambda r: 1.0 - math.exp(-r / max(0.5, g.r_d))
        pi_fn = p2.conformal_clock_lapse(kappa_fn(g.r_max), lambda_p=lam)
        pi_core = core.participation_aperture(core.NodeRecord(kappa=kappa_fn(g.r_max)), lambda_p=lam)
        self.assertAlmostEqual(pi_fn, pi_core, delta=1e-12)
        acc = p2.conformal_acceleration_1d(g.r_max, kappa_fn, lambda_p=lam)
        lit, att = _extract_conformal_and_phi_acc(acc)
        self.assertAlmostEqual(lit, -att, delta=1e-9 * max(1e-30, abs(lit)))

    def test_t3_04_pathway1_physics_determines_criteria_and_manifest(self) -> None:
        p1 = _import_p1()
        f6 = p1.evaluate_f6_sign_check()
        sparc = p1.evaluate_sparc_fit()
        asym = p1.evaluate_radial_asymptotics()
        scr = p1.evaluate_screening_constraints()
        crit = p1.evaluate_pathway1_criteria()
        man = p1.closure_manifest()
        _assert_f6_sign_check_8_of_8(self, f6)
        _assert_sparc_fit_overall_valid(self, sparc, beta=0.93, check_fit_quality=True)
        _assert_radial_asymptotics_keplerian(self, asym)
        _assert_screening_constraints_valid(self, scr)
        _assert_fl1_separation_required(self, scr)
        self.assertIn(crit["status"], {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION"})
        self.assertIn("FIT", _extract_manifest_tags(man))
        self.assertIn("TH-DET", _extract_manifest_tags(man))

    def test_t3_05_pathway2_equations_determine_4check_refutation(self) -> None:
        p2 = _import_p2()
        self.assertGreater(p2.conformal_clock_lapse(0.5), 0.0)
        self.assertGreater(p2.kappa_potential_phi(0.5), 0.0)
        a_sign = p2.audit_sign_consistency()
        a_ppn = p2.audit_conformal_ppn_lensing()
        a_mass = p2.audit_sparc_mass_scaling()
        a_clk = p2.audit_clock_scale_gap()
        variants = p2.explore_modified_variants()
        crit = p2.evaluate_pathway2_criteria()
        for obj in (a_sign, a_ppn, a_mass, a_clk, variants, crit):
            self.assertIsInstance(obj, dict)
        _assert_audit_failed(self, a_sign)
        _assert_audit_failed(self, a_ppn)
        _assert_audit_failed(self, a_mass)
        _assert_clock_scale_gap_failure(self, a_clk)
        _assert_pathway2_refuted(self, crit)

    def test_t3_06_pathway1_vs_pathway2_contrast_on_shared_galaxies(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        p2 = _import_p2()
        g = go.KNOWN_GALAXIES[5]  # DDO 154
        k_in = p1.t1_contraction_kappa(0.1, g.M_star, g.r_d, g.M_gas, g.r_gas)
        k_out = p1.t1_contraction_kappa(30.0, g.M_star, g.r_d, g.M_gas, g.r_gas)
        self.assertGreater(k_out, k_in)
        acc = p2.conformal_acceleration_1d(
            1.5,
            lambda r: p1.t1_contraction_kappa(r, g.M_star, g.r_d, g.M_gas, g.r_gas),
            lambda_p=1e-7,
        )
        lit, _ = _extract_conformal_and_phi_acc(acc)
        self.assertGreater(lit, 0.0)  # outward repulsive under T1 d kappa/dr > 0
        self.assertIn(p1.evaluate_pathway1_criteria()["status"], {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION"})
        _assert_pathway2_refuted(self, p2.evaluate_pathway2_criteria())

    def test_t3_07_unified_runner_parity_with_pathway1(self) -> None:
        p1 = _import_p1()
        rev = _import_revival()
        crit1 = p1.evaluate_pathway1_criteria()
        summary = rev.run_all_pathway_evaluations()
        _assert_summary_matches_pathways(self, summary, expected_p1=crit1["status"], require_p2=False)

    def test_t3_08_unified_runner_parity_with_pathway2(self) -> None:
        p2 = _import_p2()
        rev = _import_revival()
        crit2 = p2.evaluate_pathway2_criteria()
        summary = rev.run_all_pathway_evaluations()
        _assert_pathway2_refuted(self, crit2)
        _assert_summary_matches_pathways(self, summary, expected_p1=None, require_p2=True)

    def test_t3_09_observables_provenance_and_core_constants_aligned(self) -> None:
        go = _import_observables()
        rc = _import_reference_constants()
        du = importlib.import_module("det8.models.det_units")
        rev = _import_revival()
        self.assertEqual(go.G_SI, rc.NEWTONIAN_G_SI)
        self.assertIn("2.99792458e8", du.natural_units()["dimensional_anchors"]["c"])
        self.assertEqual(go.OBSERVABLE_PROVENANCE["det_claim_status"], "NEUTRAL_DATA_FIXTURE")
        self.assertIsInstance(rev.run_all_pathway_evaluations(), dict)

    def test_t3_10_code_verdicts_and_manifests_match_docs_and_ledgers(self) -> None:
        p1 = _import_p1()
        p2 = _import_p2()
        p1_status = p1.evaluate_pathway1_criteria()["status"].lower()
        _assert_pathway2_refuted(self, p2.evaluate_pathway2_criteria())
        self.assertTrue({"TH-DET", "FIT"} <= set(_extract_manifest_tags(p1.closure_manifest())))
        self.assertGreaterEqual(len(p2.closure_manifest()), 3)
        phys = _read_doc("PHYSICS.md").lower()
        mc = _read_doc("MODEL_CARD.md").lower()
        fals = _read_doc("FALSIFICATION_LEDGER.md").lower()
        nov = _read_doc("NOVELTY_LEDGER.md").lower()
        arch = _read_doc("archive/retired_kappa_gravity.md").lower()
        self.assertIn("pathway 1", phys)
        self.assertIn("pathway 2", phys)
        self.assertTrue(
            p1_status in phys
            or p1_status.replace("_", " ") in phys
            or "partial_limitation" in phys
            or "partial limitation" in phys
            or "viable_provisional" in phys
            or "viable provisional" in phys
        )
        self.assertIn("pathway 1", mc)
        self.assertIn("pathway 2", mc)
        self.assertTrue("pathway 1" in fals or "pathway 2" in fals)
        self.assertTrue("pathway 1" in nov or "pathway 2" in nov or "kappa_t1_contraction" in nov)
        self.assertTrue("pathway 1" in arch or "revival" in arch)

    def test_t3_11_core_alignment_modules_match_governance_and_docs(self) -> None:
        rev = _import_revival()
        gov = _read_doc("GOVERNANCE.md").lower()
        clf = _read_doc("docs/CONTINUUM_LIMIT_FRAMEWORK.md").lower()
        self.assertIn("provisional", gov)
        self.assertIn("relax", clf)
        for rel in EXPECTED_CORE_ALIGNED:
            txt = (REPO_ROOT / rel).read_text(encoding="utf-8").lower()
            self.assertTrue(
                any(
                    tok in txt
                    for tok in (
                        "revival",
                        "kappa_gravity_revival",
                        "kappa_t1_contraction",
                        "pi_conformal_bridge",
                        "galaxy_observables",
                    )
                ),
                rel,
            )
        self.assertIsInstance(rev.run_all_pathway_evaluations(), dict)

    def test_t3_12_quarantine_snapshot_and_research_checks_simultaneous(self) -> None:
        lq = _import_quarantine()
        _import_observables()
        _import_p1()
        _import_p2()
        _import_revival()
        self.assertEqual(len(lq.FULLY_RETIRED), 28)
        snap = _run_cmd([sys.executable, "-B", "scripts/check_review_snapshot.py"])
        res = _run_cmd([sys.executable, "-B", "scripts/run_research_checks.py", "--check"])
        self.assertEqual(snap.returncode, 0, snap.stdout)
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertEqual(json.loads(snap.stdout)["matched_files"], 71)
        self.assertTrue(json.loads(res.stdout)["successful"])

    def test_t3_13_det8_core_m0_and_experimental_constraints_compose_with_p2(self) -> None:
        core = _import_core()
        ec = _import_constraints()
        p2 = _import_p2()
        rec = core.NodeRecord(kappa=0.5, N=1.0)
        dt = core.proper_time_increment(rec, delta_N=2.0, lambda_p=1.0)
        pi = p2.conformal_clock_lapse(0.5, lambda_p=1.0)
        self.assertAlmostEqual(dt, 2.0 * pi, delta=1e-12)
        best = ec.constrain_lambda_p_from_clocks(0.5)["best_bound"]
        clk_res = p2.audit_clock_scale_gap()
        self.assertAlmostEqual(best, 4.0e-18, delta=1e-22)
        _assert_clock_scale_gap_failure(self, clk_res)

    def test_t3_14_sparc_subset_discrepancies_documented_in_archive_and_anchoring(self) -> None:
        go = _import_observables()
        diag = go.load_sparc_subset_diagnostic()
        self.assertEqual(diag["record_count"], 56)
        self.assertEqual(diag["anomalies"]["m_gas_equals_m_star_count"], 56)
        self.assertEqual(diag["anomalies"]["zero_v_flat_count"], 12)
        arch = _read_doc("archive/retired_kappa_gravity.md").lower()
        anch = _read_doc("docs/observable_anchoring.md").lower()
        self.assertIn("sparc_subset.json", arch)
        self.assertIn("sparc", anch)

    def test_t3_15_all_13_docs_updated_on_revival_branch_only(self) -> None:
        self.assertEqual(_git("rev-parse", "main").stdout.strip(), MAIN_BASELINE_SHA)
        for rel in EXPECTED_DOCS:
            main_show = _git("show", f"main:{rel}")
            self.assertEqual(main_show.returncode, 0, rel)
            curr = _read_doc(rel)
            self.assertNotEqual(curr, main_show.stdout, f"Doc not updated relative to main: {rel}")


# ═══════════════════════════════════════════════════════════════════════════
# TIER 4: REAL-WORLD APPLICATION SCENARIOS (8 End-to-End Scenarios)
# ═══════════════════════════════════════════════════════════════════════════


class TestTier4RealWorldScenarios(unittest.TestCase):
    """End-to-end astrophysical & repository governance scenarios (8 tests)."""

    def test_t4_s1_full_sparc_43_and_known_8_astrophysical_pipeline(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        p2 = _import_p2()

        diag = go.load_sparc_subset_diagnostic()
        self.assertEqual(diag["record_count"], 56)
        self.assertEqual(len(go.KNOWN_GALAXIES), 8)
        self.assertEqual(len(go.SAMPLE_GALAXIES), 43)

        f6 = p1.evaluate_f6_sign_check()
        sparc = p1.evaluate_sparc_fit(sigma_crit=0.008, beta=0.93)
        mass_audit = p2.audit_sparc_mass_scaling()
        _assert_f6_sign_check_8_of_8(self, f6)
        _assert_sparc_fit_overall_valid(self, sparc, beta=0.93, check_fit_quality=True)
        _assert_audit_failed(self, mass_audit)
        self.assertTrue("fail" in _serialized_lower(mass_audit) or "refut" in _serialized_lower(mass_audit))

    def test_t4_s2_hsb_spiral_vs_lsb_dwarf_rotation_curve_regimes(self) -> None:
        go = _import_observables()
        p1 = _import_p1()
        ngc2841 = next(g for g in go.SAMPLE_GALAXIES if g.name == "NGC 2841")
        ddo154 = next(g for g in go.SAMPLE_GALAXIES if g.name == "DDO 154")

        for mult in (0.05, 0.5, 1.0, 2.0, 4.0, 8.0):
            k_hsb = p1.t1_contraction_kappa(mult * ngc2841.r_d, ngc2841.M_star, ngc2841.r_d, ngc2841.M_gas, ngc2841.r_gas)
            k_lsb = p1.t1_contraction_kappa(mult * ddo154.r_d, ddo154.M_star, ddo154.r_d, ddo154.M_gas, ddo154.r_gas)
            self.assertGreater(k_hsb, 0.0)
            self.assertLessEqual(k_lsb, 1.0)
        k_hsb_inner = p1.t1_contraction_kappa(ngc2841.r_d, ngc2841.M_star, ngc2841.r_d, ngc2841.M_gas, ngc2841.r_gas)
        k_lsb_inner = p1.t1_contraction_kappa(ddo154.r_d, ddo154.M_star, ddo154.r_d, ddo154.M_gas, ddo154.r_gas)
        self.assertGreater(k_lsb_inner, k_hsb_inner)
        g_lsb_out = p1.reciprocal_aperture_g_eff(
            p1.t1_contraction_kappa(ddo154.r_max, ddo154.M_star, ddo154.r_d, ddo154.M_gas, ddo154.r_gas),
            beta=0.93,
        )
        self.assertGreater(g_lsb_out / go.G_SI, 9.0)
        r_scale = max(ddo154.r_d, ddo154.r_gas)
        v40 = p1.pathway1_rotation_velocity(40.0 * r_scale, ddo154)
        v80 = p1.pathway1_rotation_velocity(80.0 * r_scale, ddo154)
        self.assertAlmostEqual(math.log(v80 / v40) / math.log(2.0), -0.5, delta=0.05)

    def test_t4_s3_multiscale_solar_nist_eotvos_fl1_constraint_suite(self) -> None:
        ec = _import_constraints()
        p1 = _import_p1()
        p2 = _import_p2()

        scr = p1.evaluate_screening_constraints()
        ppn = p2.audit_conformal_ppn_lensing()
        clk = p2.audit_clock_scale_gap()
        best_clk = ec.constrain_lambda_p_from_clocks(0.5)["best_bound"]
        self.assertAlmostEqual(best_clk, 4.0e-18, delta=1e-22)
        _assert_screening_constraints_valid(self, scr)
        _assert_fl1_separation_required(self, scr)
        self.assertIn("roche", _serialized_lower(scr))
        self.assertIn("fl-1", _serialized_lower(scr))
        _assert_audit_failed(self, ppn)
        self.assertIn(-1.0, _all_numbers(ppn))
        _assert_clock_scale_gap_failure(self, clk)

    def test_t4_s4_fresh_process_cli_revival_runner(self) -> None:
        before = _git("status", "--porcelain").stdout
        proc = _run_cmd([sys.executable, "-B", "-m", "det8.models.kappa_gravity_revival"])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stderr.strip(), "")
        expected_p1 = _import_p1().evaluate_pathway1_criteria()["status"]
        _assert_cli_stdout_valid(self, proc.stdout, expected_p1=expected_p1)
        self.assertEqual(_git("status", "--porcelain").stdout, before)

    def test_t4_s5_concurrent_pathway_adjudication_and_native_vs_fitted_audit(self) -> None:
        p1 = _import_p1()
        p2 = _import_p2()
        rev = _import_revival()

        c1 = p1.evaluate_pathway1_criteria()
        c2 = p2.evaluate_pathway2_criteria()
        m1 = p1.closure_manifest()
        m2 = p2.closure_manifest()
        summary = rev.run_all_pathway_evaluations()

        self.assertIn(c1["status"], {"VIABLE_PROVISIONAL", "PARTIAL_LIMITATION"})
        _assert_pathway2_refuted(self, c2)
        tags1 = set(_extract_manifest_tags(m1))
        tags2 = set(_extract_manifest_tags(m2))
        self.assertTrue({"TH-DET", "FIT"} <= tags1)
        self.assertTrue(len(tags2) >= 2)
        _assert_summary_matches_pathways(self, summary, expected_p1=c1["status"], require_p2=True)
        stxt = _serialized_lower(summary)
        self.assertTrue(("th-det" in stxt or "native" in stxt) and ("fit" in stxt or "fitted" in stxt))

    def test_t4_s6_repository_docs_gates_ledgers_crosscheck(self) -> None:
        for rel in EXPECTED_DOCS:
            self.assertTrue((REPO_ROOT / rel).is_file(), rel)
        for rel in EXPECTED_CORE_ALIGNED:
            txt = (REPO_ROOT / rel).read_text(encoding="utf-8").lower()
            self.assertTrue(
                any(
                    tok in txt
                    for tok in (
                        "revival",
                        "kappa_gravity_revival",
                        "kappa_t1_contraction",
                        "pi_conformal_bridge",
                        "galaxy_observables",
                    )
                ),
                rel,
            )
        gov = _read_doc("GOVERNANCE.md").lower()
        fals = _read_doc("FALSIFICATION_LEDGER.md").lower()
        nov = _read_doc("NOVELTY_LEDGER.md").lower()
        self.assertTrue("relax" in gov and "strict" in gov)
        self.assertTrue("fl-1" in fals and "falsifier" in fals)
        self.assertTrue("cost" in nov)

    def test_t4_s7_full_governance_quarantine_snapshot_research_verification(self) -> None:
        snap = _run_cmd([sys.executable, "-B", "scripts/check_review_snapshot.py"])
        res = _run_cmd([sys.executable, "-B", "scripts/run_research_checks.py", "--check"])
        unit = _run_cmd([sys.executable, "-B", "-m", "unittest", "det8/tests/test_kappa_gravity_revival.py", "-v"])
        quar = _run_cmd([
            sys.executable,
            "-B",
            "-c",
            "import run_tests; run_tests.test_legacy_gravity_quarantine(); "
            "assert run_tests.FAIL == 0 and run_tests.ERROR == 0",
        ])
        self.assertEqual(snap.returncode, 0, snap.stdout + snap.stderr)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual(unit.returncode, 0, unit.stdout + unit.stderr)
        self.assertEqual(quar.returncode, 0, quar.stdout + quar.stderr)

    def test_t4_s8_git_branch_isolation_push_and_clean_execution_hygiene(self) -> None:
        before_status = _git("status", "--porcelain").stdout
        before_head = _git("rev-parse", "HEAD").stdout.strip()

        _import_observables().load_sparc_subset_diagnostic()
        _run_cmd([sys.executable, "-B", "scripts/check_review_snapshot.py"])

        after_status = _git("status", "--porcelain").stdout
        after_head = _git("rev-parse", "HEAD").stdout.strip()
        self.assertEqual(before_status, after_status)
        self.assertEqual(before_head, after_head)
        self.assertEqual(_git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip(), REVIVAL_BRANCH)
        self.assertEqual(_git("rev-parse", "main").stdout.strip(), MAIN_BASELINE_SHA)
        self.assertEqual(_git("rev-parse", "origin/main").stdout.strip(), MAIN_BASELINE_SHA)
        remote_ref = f"refs/remotes/origin/{REVIVAL_BRANCH}"
        if _git("show-ref", "--verify", "--quiet", remote_ref).returncode == 0:
            self.assertEqual(_git("rev-parse", remote_ref).stdout.strip(), after_head)


if __name__ == "__main__":
    unittest.main()
