"""QR-05X scoring-layer capture and read-only replay.

W conditional laws are pinned inputs, not recomputed by this runner.
The separately frozen JSON-only audit authenticates the raw-history bridge.
Lifecycle helpers are carried locally from the O/W lineage.
"""

from __future__ import annotations

import argparse
import copy
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
SCHEMA = "det8-qr05x-results-v1"
BASE_COMMIT = "f2fb58047a86b513d8a032980bc49c316bd6d84b"
SOURCES = (
    "README.md",
    "misspecification.py",
    "reference_qr05x.py",
    "study.py",
    "test_qr05x.py",
    "test_capture.py",
    "audit_json.py",
)
W_PRIOR = "qr-05w-noisy-readouts-2026-09-07/results.json"
W_BYTES = 6756094
W_SHA = "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a"
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 128 * 1024 * 1024

PRIORS = {
    W_PRIOR: W_SHA,
    "qr-05v-readout-value-2026-09-06/results.json": "eceb01f49624f3d5ebb5dc8041074aa04b62d8408d4a7117979fb1c6b9823ff7",
    "qr-05u-partial-observation-2026-09-06/results.json": "a2cf4ae0bb31934c3c1aeab7071fb6f675d90d9f0b1a5c2776282e926e3e5eee",
    "qr-05t-local-refinement-2026-09-06/results.json": "f7bf6db5dd822c27a3087c6ad48af3ae76fdce653536cff8d381bfae905a5fe8",
    "qr-05s-local-deletion-2026-09-06/results.json": "8caa59a1921dc7fb46a38e44058bfe9f2ac5608c1f2ed05e5dc8ff063ab7e3b3",
    "qr-05r-deletion-profile-2026-09-06/results.json": "cfec27d60d605ec142af96f8931e0e90b3c5ca92c72389ce8e0d84ef8b444001",
    "qr-05q-three-layer-portability-2026-09-06/results.json": "1e9b9443ee5d55cd888d5ea62e594fad197ca0baeecfee1f1efac34ada8125aa",
    "qr-05p-minimal-summary-2026-09-06/results.json": "c43435c4916e5c15efb373ff70795ed733d7c4e360ebec4e9a1b32f4e050b048",
    "qr-05o-path-observable-2026-09-06/results.json": "3364b36813f745a645d78d6d30caa292778da986cb6d1140f108a0fd4b945eb1",
    "qr-05n-domain-portability-2026-09-06/results.json": "f2d666285afef41cd8a7f977399d3626a620da39174967a38047714f5f26f93e",
    "qr-05m-observable-realization-2026-09-06/results.json": "79cb515022fdb3bb2c918a469c1ac5ffdf98a6dd18cdd289f8030fc7a38f1543",
    "qr-05l-adversarial-refinement-2026-09-06/results.json": "0df1b47e1219191783a9ec229540fd433e2129121ce2c5f6e5262e5f3c00e0ff",
    "qr-05k-recursive-closure-2026-09-06/results.json": "46d93f643c443b75ef425349cff11d7f3c437a79921e7e1ee94610998bd1a501",
    "qr-05j-uncertainty-contract-2026-09-06/results.json": "dc8f80f40861107dd7a5ee378c9813a90c1981a3c2e7e14ee343163e9d88c333",
    "qr-05i-analytic-portability-2026-09-06/results.json": "9742e602b037ce74611e7801256f86752f584438a80f9dac6c823acef671e798",
    "qr-05h-law-portability-2026-09-06/results.json": "e6d5f06d765ccca7a1da1cef15d12bc15a3287463ec3cce3732aab75af613b3a",
    "qr-05g-predictive-compression-2026-09-06/results.json": "62b13d1c46efcd5552596f37ba9ec5ab00f8e9708bab19f811cc0a0a357ffb74",
    "qr-01-quantum-records-2026-09-05/results.json": "e9af97dab27777775ad37db1f03a85abc9ca3b45b11a7ba79b7e92c0bd1c2c9b",
    "qr-02-record-coarse-graining-2026-09-05/results.json": "b7f18f32a3b5552b77c0933343e707da400c095758c1065e477eb8ada580af1c",
    "qr-03-predictive-histories-2026-09-05/results.json": "2b92b7bd42aa9cde29722269c1a31f339e37b217d1256e50d8ea0ee34d8188c2",
    "qr-04-adaptive-causal-records-2026-09-05/results.json": "a5dc5f5e96a189ae8fd5648334e630fd4c24f6cee2fa805a45d32522bc0bcd70",
    "qr-05a-quantum-births-2026-09-05/results.json": "e0c2676ae33b36dde3edb2697ac252330ad801006fe8420acd8cfb94b87c9479",
    "qr-05b-order-summaries-2026-09-05/results.json": "2fe3fd939dcc242ee2a6b8c4abc9d6904e32bf5072cf638f7d880daaeaf2e03b",
    "qr-05c-coarse-dynamics-2026-09-05/results.json": "4f7bb191e64db6bb24886cc1211cb83186d7e24f77599e56e25539c100f4dde1",
    "qr-05d-geometric-correspondence-2026-09-05/results.json": "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238",
    "qr-05d-geometric-correspondence-2026-09-05/results-v2.json": "18499d8a126a3677fb0f0e54a98659df7934c7429c39cc0f531adfc063d40b32",
    "qr-05f-two-stage-2026-09-06/results.json": "0fffba7f9d8549b2e12d90551c82dc72e0ead7f4010923578af610e055683917",
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


def require_wire(value):
    """Native validation with per-call DAG accounting before serialization.

    Expanded value nodes lower-bound JSON bytes. Repeated references count
    each occurrence, but completed subtrees are walked only once. Depth is
    safely above every valid S schema, including evidence envelopes.
    """
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        identity = id(item)
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 1
            for child in children:
                count, child_height = (
                    completed[id(child)] if type(child) in (list, dict) else (1, 0)
                )
                nodes += count
                height = max(height, child_height + 1)
                require(nodes <= MAX_WORKING_BYTES, "expanded wire exceeds working byte cap")
            completed[identity] = nodes, height
            active.remove(identity)
            continue
        if item is None or type(item) in (bool, int, str):
            continue
        require(type(item) in (list, dict), "mathematical suite must use native exact JSON types")
        require(identity not in active, "cyclic wire container")
        require(depth <= 128, "wire exceeds bounded schema depth")
        if identity in completed:
            require(depth + completed[identity][1] - 1 <= 128, "wire exceeds bounded schema depth")
            continue
        if type(item) is dict:
            require(all(type(key) is str for key in item), "wire keys must be strings")
        active.add(identity)
        pending.append((item, depth, True))
        children = item if type(item) is list else item.values()
        pending.extend((child, depth + 1, False) for child in children)


def canonical(value):
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode()


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
        require(len(before) <= MAX_CAPTURE_BYTES, "artifact byte cap")
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
    require(retained_bits(suite) <= 4096, "retained suite component bit bound")
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
            "scope": "suite and internal exact JSON checks; excludes final report serialization; no application performance claim",
        },
    }
    raw = canonical(report)
    require(len(raw) <= MAX_CAPTURE_BYTES, "artifact byte cap")
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


def fraction(value):
    require(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    require(type(n) is int and type(d) is int and 0 <= n <= 2 * d and d > 0, "fraction range")
    f = F(n, d)
    require([f.numerator, f.denominator] == value, "reduced fraction")
    require(max(n.bit_length(), d.bit_length()) <= 4096, "rational bit bound")
    return f


def fq(value):
    require(0 <= value <= 2, "retained score range")
    answer = [value.numerator, value.denominator]
    require(max(abs(v).bit_length() for v in answer) <= 4096, "retained score bits")
    return answer


def law(rows):
    return {tuple(r["value"]): fraction(r["probability"]) for r in rows}


def fixtures():
    raw = plain_bytes(HERE.parent / W_PRIOR)
    require(len(raw) == W_BYTES and digest(raw) == W_SHA, "pinned W artifact")
    doc = json.loads(raw)
    require(canonical(doc) == raw, "W envelope canonical bytes")
    require_wire(doc["suite"])
    expected = {**doc["prior_artifacts"], W_PRIOR: {"bytes": W_BYTES, "sha256": W_SHA}}
    require_same_wire(expected, priors(), "exact inherited 28-artifact inventory")
    require(len(doc["suite"]["cases"]) == 6, "six fixed W cases")
    return doc["suite"]


def case_problem(case):
    return {
        "schema_version": "det8-qr05x-problem-v1",
        "family": "qr05x_noise_misspecification",
        "beliefs": [
            {
                "belief_id": b["belief_id"],
                "weight": copy.deepcopy(b["weight"]),
                "channels": [
                    {
                        "level": copy.deepcopy(ch["level"]),
                        "cells": [
                            {k: copy.deepcopy(c[k]) for k in ("value", "probability", "prediction")}
                            for c in ch["cells"]
                        ],
                    }
                    for ch in b["channels"]
                ],
            }
            for b in case["analysis"]["beliefs"]
        ],
    }


def expected_analysis(problem):
    """Independent scorer on pinned conditional laws; not an origin authenticator."""
    rows = []
    scoring_terms = 0
    for entry in problem["beliefs"]:
        channels = [{tuple(c["value"]): c for c in ch["cells"]} for ch in entry["channels"]]
        pairs = []
        for i in range(4):
            for j in range(4):
                cells = []
                coverage = bayes = supported_bayes = forecast_total = regret_total = F(0)
                equalities = []
                for z, actual in sorted(channels[i].items()):
                    p = law(actual["prediction"])
                    w = fraction(actual["probability"])
                    # Replica disagreement, rather than 1 minus a squared norm.
                    r = sum((u * (1 - u) for u in p.values()), F(0))
                    bayes += w * r
                    assumed = channels[j].get(z)
                    supported = assumed is not None
                    output = {
                        "value": list(z),
                        "actual_probability": fq(w),
                        "assumed_probability": assumed["probability"] if supported else [0, 1],
                        "actual_prediction": copy.deepcopy(actual["prediction"]),
                        "forecast": copy.deepcopy(assumed["prediction"]) if supported else None,
                        "bayes_risk": fq(r),
                        "forecast_risk": None,
                        "regret": None,
                        "supported": supported,
                        "predictions_equal": None,
                    }
                    if supported:
                        f = law(assumed["prediction"])
                        scoring_terms += len(p) + len(f)
                        support = sorted(p.keys() | f.keys())
                        # Coordinate-wise expected squared error. This counts
                        # both outcomes of each indicator without generating
                        # extra physical or forecast observations.
                        score = sum(
                            (
                                p.get(q, F(0)) * (1 - f.get(q, F(0))) ** 2
                                + (1 - p.get(q, F(0))) * f.get(q, F(0)) ** 2
                                for q in support
                            ),
                            F(0),
                        )
                        distance = sum(
                            ((p.get(q, F(0)) - f.get(q, F(0))) ** 2 for q in support), F(0)
                        )
                        equal = p == f
                        require(
                            score == r + distance and (distance == 0) == equal,
                            "cell actual-law Brier decomposition",
                        )
                        require(0 <= score <= 2 and 0 <= distance <= 2, "cell score range")
                        output.update(
                            forecast_risk=fq(score), regret=fq(distance), predictions_equal=equal
                        )
                        coverage += w
                        supported_bayes += w * r
                        forecast_total += w * score
                        regret_total += w * distance
                        equalities.append(equal)
                    cells.append(output)
                require(
                    forecast_total == supported_bayes + regret_total,
                    "supported actual-weight decomposition",
                )
                require((regret_total == 0) == all(equalities), "supported zero regret iff equal")
                complete = coverage == 1
                unsupported = sum(
                    (fraction(c["actual_probability"]) for c in cells if not c["supported"]),
                    F(0),
                )
                require(coverage + unsupported == 1, "explicit support mass partition")
                require(
                    sum(fraction(c["actual_probability"]) for c in cells) == 1, "actual report mass"
                )
                require(
                    0 <= supported_bayes <= coverage and 0 <= forecast_total <= 2 * coverage,
                    "coverage-scaled supported risk bounds",
                )
                require(0 <= regret_total <= 2 * coverage, "coverage-scaled regret bound")
                if complete:
                    require(forecast_total == bayes + regret_total, "full decomposition")
                pairs.append(
                    {
                        "actual_index": i,
                        "assumed_index": j,
                        "cells": cells,
                        "bayes_risk": fq(bayes),
                        "coverage": fq(coverage),
                        "unsupported_mass": fq(1 - coverage),
                        "supported_bayes_risk": fq(supported_bayes),
                        "supported_forecast_risk": fq(forecast_total),
                        "supported_regret": fq(regret_total),
                        "forecast_risk": fq(forecast_total) if complete else None,
                        "regret": fq(regret_total) if complete else None,
                        "complete": complete,
                        "checks": {
                            "mass_partition": True,
                            "supported_decomposition": True,
                            "full_decomposition": True if complete else None,
                            "zero_regret_iff_equal": True,
                        },
                    }
                )
        rows.append(
            {
                "belief_id": entry["belief_id"],
                "weight": copy.deepcopy(entry["weight"]),
                "pairs": pairs,
            }
        )
    weights = [fraction(r["weight"]) for r in rows]
    require(sum(weights) == 1, "original history weights")
    aggregate = []
    scalar_fields = (
        "bayes_risk",
        "coverage",
        "unsupported_mass",
        "supported_bayes_risk",
        "supported_forecast_risk",
        "supported_regret",
    )
    for index in range(16):
        values = {
            key: sum(
                (
                    weight * fraction(r["pairs"][index][key])
                    for weight, r in zip(weights, rows, strict=True)
                ),
                F(0),
            )
            for key in scalar_fields
        }
        complete_count = sum(r["pairs"][index]["complete"] for r in rows)
        complete = complete_count == len(rows)
        require(complete == (values["coverage"] == 1), "aggregate complete iff full coverage")
        require(values["coverage"] + values["unsupported_mass"] == 1, "case mass partition")
        require(
            values["supported_forecast_risk"]
            == values["supported_bayes_risk"] + values["supported_regret"],
            "case supported identity",
        )
        require(
            (values["supported_regret"] == 0)
            == all(
                c["predictions_equal"]
                for r in rows
                for c in r["pairs"][index]["cells"]
                if c["supported"]
            ),
            "case zero supported regret iff all supported laws agree",
        )
        if complete:
            require(
                values["supported_forecast_risk"]
                == values["bayes_risk"] + values["supported_regret"],
                "case full identity",
            )
        aggregate.append(
            {
                "actual_index": index // 4,
                "assumed_index": index % 4,
                **{key: fq(value) for key, value in values.items()},
                "forecast_risk": fq(values["supported_forecast_risk"]) if complete else None,
                "regret": fq(values["supported_regret"]) if complete else None,
                "complete": complete,
                "checks": {
                    "mass_partition": True,
                    "supported_decomposition": True,
                    "full_decomposition": True if complete else None,
                    "zero_regret_iff_equal": True,
                },
                "complete_beliefs": complete_count,
                "incomplete_beliefs": len(rows) - complete_count,
            }
        )

    def first(index, predicate):
        return next((r["belief_id"] for r in rows if predicate(r["pairs"][index])), None)

    witnesses = {
        "first_incomplete": [first(i, lambda p: not p["complete"]) for i in range(16)],
        "first_positive_supported_regret": [
            first(i, lambda p: fraction(p["supported_regret"]) > 0) for i in range(16)
        ],
        "first_positive_full_regret": [
            first(i, lambda p: p["complete"] and fraction(p["regret"]) > 0) for i in range(16)
        ],
    }
    counts = {
        "beliefs": len(rows),
        "input_cells": sum(len(c["cells"]) for b in problem["beliefs"] for c in b["channels"]),
        "input_prediction_atoms": sum(
            len(cell["prediction"])
            for b in problem["beliefs"]
            for c in b["channels"]
            for cell in c["cells"]
        ),
        "pair_cells": [sum(len(r["pairs"][i]["cells"]) for r in rows) for i in range(16)],
        "supported_pair_cells": [
            sum(c["supported"] for r in rows for c in r["pairs"][i]["cells"]) for i in range(16)
        ],
        "unsupported_pair_cells": [
            sum(not c["supported"] for r in rows for c in r["pairs"][i]["cells"]) for i in range(16)
        ],
        "scoring_terms": scoring_terms,
        "complete_beliefs": [a["complete_beliefs"] for a in aggregate],
        "incomplete_beliefs": [a["incomplete_beliefs"] for a in aggregate],
        "positive_supported_regret_beliefs": [
            sum(fraction(r["pairs"][i]["supported_regret"]) > 0 for r in rows) for i in range(16)
        ],
        "positive_full_regret_beliefs": [
            sum(r["pairs"][i]["complete"] and fraction(r["pairs"][i]["regret"]) > 0 for r in rows)
            for i in range(16)
        ],
    }
    return {
        "input_sha256": digest(canonical(problem)),
        "levels": copy.deepcopy(LEVELS),
        "beliefs": rows,
        "aggregate": {"total_weight": [1, 1], "pairs": aggregate},
        "witnesses": witnesses,
        "counts": counts,
    }


def check_analysis(analysis, case):
    require_wire(analysis)
    require_wire(case)
    data = fixtures()
    candidates = [c for c in data["cases"] if c["case_id"] == case["case_id"]]
    require(len(candidates) == 1, "unknown W case")
    require_same_wire(case, candidates[0], "W producer case differs")
    expected = expected_analysis(case_problem(case))
    require_same_wire(analysis, expected, "complete independent X scoring audit differs")
    return {"analysis_sha256": digest(canonical(expected)), "complete_native_output_equal": True}


def producer_controls(analysis, case):
    for out, old in zip(analysis["beliefs"], case["analysis"]["beliefs"], strict=True):
        require(
            out["belief_id"] == old["belief_id"] and out["weight"] == old["weight"],
            "unchanged W histories and weights",
        )
        for i in range(4):
            diagonal = out["pairs"][4 * i + i]
            require(diagonal["complete"] and diagonal["regret"] == [0, 1], "diagonal calibration")
            require_same_wire(
                diagonal["forecast_risk"], old["channels"][i]["expected_risk"], "W diagonal risk"
            )
            for j in (1, 2, 3):
                require(
                    out["pairs"][4 * i + j]["complete"],
                    "positive W noise model covers actual reports",
                )
            full = out["pairs"][4 * i + 3]
            require_same_wire(
                full["forecast_risk"],
                old["controls"]["N"]["expected_risk"],
                "assumed full replacement is N forecast for every actual law",
            )
    for i in range(4):
        diagonal = analysis["aggregate"]["pairs"][4 * i + i]
        require_same_wire(
            diagonal["forecast_risk"],
            case["analysis"]["aggregate"]["channels"][i]["expected_risk"],
            "weighted diagonal W risk",
        )
        require_same_wire(
            analysis["aggregate"]["pairs"][4 * i + 3]["forecast_risk"],
            case["analysis"]["aggregate"]["N_risk"],
            "weighted N control",
        )
    return {
        "W_laws_are_declared_pinned_dependencies": True,
        "complete_projection_checked": True,
        "diagonal_W_risks_equal": True,
        "positive_assumed_noise_covers_actual_reports": True,
        "assumed_full_replacement_N_risk_equal": True,
        "W_channel_origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


def run_suite():
    primary = load("_qr05x_primary", "misspecification.py")
    reference = load("_qr05x_reference", "reference_qr05x.py")
    data = fixtures()
    cases = []
    for case in data["cases"]:
        problem = case_problem(case)
        before = canonical(problem)
        a = primary.analyze(problem)
        require(canonical(problem) == before, "primary input mutation")
        b = reference.analyze(problem)
        require(canonical(problem) == before, "reference input mutation")
        require_same_wire(a, b, "independent X scoring routes differ")
        require_same_wire(a, expected_analysis(problem), "independent runner scoring differs")
        controls = producer_controls(a, case)
        cases.append(
            {
                "case_id": case["case_id"],
                "problem": problem,
                "analysis": a,
                "producer_controls": controls,
            }
        )
    bad_calls = 0
    first = cases[0]["problem"]
    for module in (primary, reference):
        for bad in (
            None,
            {},
            [],
            {**first, "extra": 0},
            {**first, "schema_version": "bad"},
            {**first, "family": "bad"},
            {**first, "beliefs": []},
        ):
            try:
                module.analyze(bad)
            except ValueError:
                bad_calls += 1
            else:
                raise ValueError("malformed X input accepted")
    totals = {
        "cases": len(cases),
        "analyze_calls": 2 * len(cases),
        "invalid_analyze_calls_rejected": bad_calls,
    }
    scalar_counts = ("beliefs", "input_cells", "input_prediction_atoms", "scoring_terms")
    for key in scalar_counts:
        totals[key] = sum(c["analysis"]["counts"][key] for c in cases)
    for key in cases[0]["analysis"]["counts"]:
        if key not in scalar_counts:
            totals[key] = [sum(c["analysis"]["counts"][key][i] for c in cases) for i in range(16)]
    require(bad_calls == 14, "malformed control inventory")
    return {
        "producer": {"artifact": W_PRIOR, "bytes": W_BYTES, "sha256": W_SHA},
        "cases": cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": bad_calls,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "noise_parameters_fitted": False,
            "fallback_forecasts_invented": False,
        },
        "totals": totals,
    }


if __name__ == "__main__":
    main()
