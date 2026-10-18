"""Version-two QR-05D capture: JSON-native suite guard and exact read-only replay."""

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
RESULT = HERE / "results-v2.json"
SCHEMA = "det8-qr05d-results-v2"
BASE_COMMIT = "34483a602987369f52c41179daf1dd63e06aa0ed"
SOURCES = (
    "README.md",
    "REVISION_V2.md",
    "geometry.py",
    "reference_qr05d.py",
    "study.py",
    "study_v2.py",
    "test_qr05d.py",
    "test_capture.py",
    "test_capture_v2.py",
)
PRIORS = {
    "qr-01-quantum-records-2026-09-05": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
}
CASES = (
    "mesh3",
    "mesh5",
    "mesh7",
    "mesh5_boost",
    "mesh5_dilate",
    "mesh5_dilate_wrong_density",
    "mesh5_warp",
    "ferrers6",
    "standard_example3",
)


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
        raw = plain_bytes(HERE.parent / name / "results.json")
        require(digest(raw) == sha, "prior artifact changed")
        result[name] = {"bytes": len(raw), "sha256": sha}
    return result


def prior_json(name):
    raw = plain_bytes(HERE.parent / name / "results.json")
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


def fixtures():
    return [{"schema_version": "det8-qr05d-problem-v1", "case": name} for name in CASES]


def invalid_fixtures():
    base = fixtures()[0]
    return [
        None,
        [],
        True,
        {},
        {"case": "mesh3"},
        {"schema_version": base["schema_version"]},
        {**base, "extra": 1},
        {**base, "case": "mesh9"},
        {**base, "case": True},
        {**base, "case": ["mesh3"]},
        {**base, "case": None},
        {**base, "schema_version": "other"},
        {**base, "schema_version": 1},
        {**base, "schema_version": [base["schema_version"]]},
    ]


def check_analysis(a):
    o = a["order"]
    n, rho = o["n"], F(a["density"])
    c, c2, c3 = (o[k] for k in ("relation", "interval_cardinality", "chain_pairs"))
    require(1 <= n <= 51 and rho > 0, "analysis bound")
    for i in range(n):
        for j in range(n):
            between = [k for k in range(n) if c[i][k] and c[k][j]]
            require(c2[i][j] == len(between), "interval count differs")
            require(
                c3[i][j] == sum(c[k][l] for k in between for l in between), "pair count differs"
            )
            require(
                [F(matrix[i][j]) for matrix in o["kernel_coefficients"]]
                == [F(c[i][j], 2), -F(c2[i][j]) / (4 * rho), F(c3[i][j]) / (8 * rho**2)],
                "kernel coefficient differs",
            )
    require(len(o["endpoint"]["chain_counts"]) == n - 1, "endpoint zero padding differs")
    if a["coordinates"] is None:
        require(
            a["case"] == "standard_example3" and a["geometry"] is None, "abstract control geometry"
        )
        return
    points = [[F(v) for v in p] for p in a["coordinates"]]
    require(
        c == [[int(u < s and v < t) for s, t in points] for u, v in points],
        "causal support does not match supplied geometry",
    )
    require(len(a["geometry"]["pairs"]) == sum(map(sum, c)), "timelike pair inventory")
    for p in a["geometry"]["pairs"]:
        i, j = p["source"], p["target"]
        tau = (points[j][0] - points[i][0]) * (points[j][1] - points[i][1])
        require(F(p["tau_squared"]) == tau > 0, "coordinate interval differs")
        require(F(p["volume"]) == tau / 2, "coordinate volume differs")
        require(F(p["count_volume"]) == F(c2[i][j]) / rho, "count volume differs")
        require(
            F(p["volume_error"]) == F(p["count_volume"]) - tau / 2, "signed volume error differs"
        )
        expected = [F(1, 2), -tau / 8, tau**2 / 128]
        require(
            list(map(F, p["continuum_coefficients"])) == expected, "continuum coefficient differs"
        )
        require(
            list(map(F, p["coefficient_errors"]))
            == [F(o["kernel_coefficients"][k][i][j]) - expected[k] for k in range(3)],
            "signed coefficient error differs",
        )


def pair(a, source, target):
    return next(
        p for p in a["geometry"]["pairs"] if p["source"] == source and p["target"] == target
    )


def probe_table(a):
    result = []
    for probe in a["probes"]:
        i, j = probe["source"], probe["target"]
        result.append(
            {
                **probe,
                "comparison": None if a["geometry"] is None else pair(a, i, j),
                "kernel_coefficients": [m[i][j] for m in a["order"]["kernel_coefficients"]],
            }
        )
    return result


def cross_controls(analyses, direct, reference):
    by_name = {a["case"]: a for a in analyses}
    base = by_name["mesh5"]
    sequence = []
    for m in (3, 5, 7):
        a = by_name[f"mesh{m}"]
        require(
            a["order"]["endpoint"]["chain_counts"][:3]
            == [1, m * m, m * m * (m * m + 2 * m - 3) // 4],
            "mesh analytical chain count differs",
        )
        require(
            a["order"]["endpoint"]["coefficients"][:3]
            == ["1/2", "-1/8", str(F(m * m + 2 * m - 3, 128 * m * m))],
            "mesh analytical endpoint coefficient differs",
        )
        sequence.append({"case": a["case"], "probes": probe_table(a)})
    transforms = []
    for name, coefficient_scale, geometric_scale in (
        ("mesh5_boost", F(1), F(1)),
        ("mesh5_dilate", F(4), F(4)),
        ("mesh5_dilate_wrong_density", F(1), F(4)),
        ("mesh5_warp", F(1), None),
    ):
        other = by_name[name]
        require(
            base["order"]["relation"] == other["order"]["relation"], "transformed order changed"
        )
        require(
            all(
                F(other["order"]["kernel_coefficients"][k][i][j])
                == coefficient_scale**k * F(base["order"]["kernel_coefficients"][k][i][j])
                for k in range(3)
                for i in range(27)
                for j in range(27)
            ),
            "order coefficient scaling differs",
        )
        if geometric_scale is not None:
            require(
                all(
                    F(q["tau_squared"]) == geometric_scale * F(p["tau_squared"])
                    for p, q in zip(
                        base["geometry"]["pairs"], other["geometry"]["pairs"], strict=True
                    )
                ),
                "coordinate scaling differs",
            )
        transforms.append(
            {
                "case": name,
                "order_equal": other["order"] == base["order"],
                "geometry_equal": other["geometry"] == base["geometry"],
                "coefficient_scale": str(coefficient_scale),
                "geometric_scale": None if geometric_scale is None else str(geometric_scale),
                "whole_volume_matches": pair(other, 0, 26)["volume_error"] == "0",
                "probes": probe_table(other),
            }
        )
    require(transforms[0]["order_equal"] and transforms[0]["geometry_equal"], "boost control")
    require(not transforms[2]["whole_volume_matches"], "wrong density was hidden")
    warp = by_name["mesh5_warp"]
    require(
        [pair(warp, 0, 13)["tau_squared"], pair(warp, 13, 26)["tau_squared"]] == ["1/16", "9/16"],
        "warp local proper times differ",
    )
    for a in (base, warp):
        require(
            [a["order"]["kernel_coefficients"][k][0][13] for k in range(3)]
            == [a["order"]["kernel_coefficients"][k][13][26] for k in range(3)]
            == ["1/2", "-1/25", "19/20000"],
            "equal local kernel witness differs",
        )
    ferrers, s3 = by_name["ferrers6"], by_name["standard_example3"]
    interiors = [[[], [], [], [0], [0, 1], [0, 1, 2]], [[], [], [], [1, 2], [0, 2], [0, 1]]]
    interior_analyses = []
    for past in interiors:
        a, b = direct.order_analysis(past, F(12)), reference.order_analysis(past, F(12))
        require_same_wire(a, b, "independent interior collision analysis differs")
        interior_analyses.append(a)
    require(
        interior_analyses[0]["summary"] == interior_analyses[1]["summary"],
        "interior count collision",
    )
    require(
        ferrers["order"]["endpoint"] == s3["order"]["endpoint"]
        and ferrers["order"]["endpoint"]["chain_counts"] == [1, 6, 6, 0, 0, 0, 0],
        "endpoint polynomial collision differs",
    )
    require(
        ferrers["order"]["interval_cardinality"] != s3["order"]["interval_cardinality"],
        "local collision lost",
    )
    require(
        len(ferrers["two_order"]["linear_extensions"]) == 57
        and ferrers["two_order"]["realizer_count"] == 2
        and len(s3["two_order"]["linear_extensions"]) == 48
        and s3["two_order"]["realizer_count"] == 0
        and s3["two_order"]["first_realizer"] is None,
        "two-order obstruction differs",
    )
    return {
        "mesh_sequence": sequence,
        "transformations": transforms,
        "base_probes": probe_table(base),
        "collision": {
            "interior_orders": interiors,
            "interior_analyses": interior_analyses,
            "interior_summaries_equal": True,
            "endpoint_polynomials_equal": True,
            "full_interval_tables_equal": False,
            "scope": "INDUCED_1_PLUS_1_FLAT_ORDER_EMBEDDING_ONLY",
        },
    }


def prior_bridge(direct, reference):
    prior = prior_json("qr-05c-coarse-dynamics-2026-09-05")
    old = next(c["analysis"] for c in prior["suite"]["cases"] if c["input"]["case"] == "weak_phase")
    comparisons = []
    for name in ("fork_join", "chain_record", "record_location"):
        control = old["controls"][name]
        histories, outputs = [], []
        for index in control["histories"]:
            h = old["levels"][control["births"]]["histories"][index]
            past = [
                [],
                *[[0, *(i + 1 for i in row)] for row in h["order"]],
                list(range(len(h["order"]) + 1)),
            ]
            a, b = (
                direct.order_analysis(past, F(2 * len(h["order"]))),
                reference.order_analysis(past, F(2 * len(h["order"]))),
            )
            require_same_wire(a, b, "independent prior-order diagnostic differs")
            histories.append({"index": index, **h})
            outputs.append(a)
        require(
            outputs[0]["endpoint"] == outputs[1]["endpoint"], "prior endpoint collision differs"
        )
        require(
            (outputs[0] == outputs[1]) == (name != "fork_join"), "prior full order question differs"
        )
        if "kernels" in control:
            maps = [old["map_bank"][i] for i in control["kernels"]]
            require(maps[0] != maps[1], "prior quantum discrepancy missing")
        else:
            maps = []
            require(control["probabilities"] == ["4/25", "2/5"], "prior count discrepancy missing")
        comparisons.append(
            {
                "control": name,
                "histories": histories,
                "order_analyses": outputs,
                "endpoint_polynomials_equal": True,
                "full_order_analyses_equal": outputs[0] == outputs[1],
                "prior_control": control,
                "resolved_prior_kernel_diagonals": maps,
            }
        )
    delayed = old["controls"]["delayed"]
    require(
        delayed["one_step_exact"] and delayed["probabilities_Px"] == ["147/78125", "1011/78125"],
        "prior delayed witness",
    )
    return {
        "scope": "REANALYZED_PARENT_ORDERS_AND_PINNED_PRIOR_QUANTUM_WITNESSES_NOT_A_NEW_COUPLING",
        "comparisons": comparisons,
        "delayed_prior_control": delayed,
        "delayed_prior_diagonals": [old["map_bank"][delayed[k]] for k in ("actual", "proposed")],
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
    direct = load("qr05d_v2_capture_direct", "geometry.py")
    reference = load("qr05d_v2_capture_reference", "reference_qr05d.py")
    cases = []
    for wire in fixtures():
        a, b = direct.analyze(wire), reference.analyze(wire)
        require_same_wire(a, b, "independent complete analysis differs")
        check_analysis(a)
        cases.append({"input": wire, "analysis": a})
    rejections = []
    for wire in invalid_fixtures():
        for module in (direct, reference):
            try:
                module.analyze(wire)
            except (ValueError, TypeError):
                pass
            else:
                raise ValueError("invalid fixed input accepted")
        rejections.append({"input": wire, "both_rejected": True})
    analyses = [c["analysis"] for c in cases]
    controls = cross_controls(analyses, direct, reference)
    bridge = prior_bridge(direct, reference)
    bits = retained_bits([cases, controls, bridge])
    require(bits <= 4096, "retained arithmetic bound")
    suite = {
        "cases": cases,
        "rejections": rejections,
        "controls": controls,
        "prior_bridge": bridge,
        "research_base_commit": BASE_COMMIT,
        "claim": "FINITE_SUPPLIED_GEOMETRY_AND_ORDER_KERNEL_DIAGNOSTIC",
        "manifold_emergence_established": False,
        "continuum_limit_established": False,
        "poisson_ensemble_validated": False,
        "quantum_field_theory_derived": False,
        "gravity_derived": False,
        "empirical_data_used": False,
        "ret_integration_tested": False,
        "bounds": {
            "maximum_events": 51,
            "all_pair_mass_squared_degree": 2,
            "maximum_realizer_interior_events": 6,
            "arithmetic_guard_bits": 4096,
        },
        "totals": {
            "fixtures": len(cases),
            "rejected_fixtures": len(rejections),
            "events_across_cases": sum(a["order"]["n"] for a in analyses),
            "matrix_positions": sum(a["order"]["n"] ** 2 for a in analyses),
            "kernel_coefficient_cells": 3 * sum(a["order"]["n"] ** 2 for a in analyses),
            "geometric_pair_comparisons": sum(
                len(a["geometry"]["pairs"]) for a in analyses if a["geometry"] is not None
            ),
            "linear_extension_pairs": sum(
                len(a["two_order"]["linear_extensions"]) ** 2
                for a in analyses
                if a["two_order"] is not None
            ),
            "independent_collision_interior_checks": 2,
            "independent_prior_parent_order_checks": 6,
            "retained_component_bits": bits,
        },
    }

    require_wire(suite)
    require_same_wire(
        prior_json("qr-05d-geometric-correspondence-2026-09-05")["suite"],
        suite,
        "version-one mathematical wire data changed",
    )
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
        require(
            existing["source_ledger"] == frozen and existing["prior_artifacts"] == previous,
            "source/prior identity changed",
        )
    started = time.perf_counter()
    suite = run_suite()
    require_wire(suite)
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
