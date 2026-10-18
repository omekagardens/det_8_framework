"""QR-05Y scoring-layer capture and read-only replay.

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
SCHEMA = "det8-qr05y-results-v1"
BASE_COMMIT = "de4bfb06a2f0d6715d0ff6f4cd7a4cd7c514bbb0"
SOURCES = (
    "README.md",
    "fallback.py",
    "reference_qr05y.py",
    "study.py",
    "test_qr05y.py",
    "test_capture.py",
    "audit_json.py",
)
X_PRIOR = "qr-05x-noise-misspecification-2026-09-07/results.json"
X_BYTES = 8842933
X_SHA = "1bf12e668ccaaeb20da78d849ae138ffcce2cc32e14be57f286169c74a4734c4"
W_PRIOR = "qr-05w-noisy-readouts-2026-09-07/results.json"
W_BYTES = 6756094
W_SHA = "05b20faf7feae7327113ace9168540d61db0e0e6bebae268819b2b84847cce8a"
LEVELS = [[0, 1], [1, 2], [3, 4], [1, 1]]
MAX_CAPTURE_BYTES = 64 * 1024 * 1024
MAX_WORKING_BYTES = 128 * 1024 * 1024

PRIORS = {
    X_PRIOR: X_SHA,
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


X_FIELDS = (
    "coverage",
    "unsupported_mass",
    "bayes_risk",
    "supported_bayes_risk",
    "supported_forecast_risk",
    "supported_regret",
    "forecast_risk",
    "regret",
    "complete",
)
X_LINEAR = X_FIELDS[:6]
Y_LINEAR = (
    "fallback_bayes_risk",
    "fallback_forecast_risk",
    "fallback_regret",
    "completed_forecast_risk",
    "completed_regret",
    "coarse_forecast_risk",
    "coarse_regret",
    "gain_over_coarse",
)
CHECK_FIELDS = (
    "policy_total",
    "mass_partition",
    "split_decomposition",
    "completed_decomposition",
    "coarse_decomposition",
    "gain_identity",
    "supported_forecasts_preserved",
    "zero_regret_iff_equal",
)


def fraction(value):
    require(type(value) is list and len(value) == 2, "fraction pair")
    n, d = value
    require(type(n) is int and type(d) is int and d > 0 and -2 * d <= n <= 2 * d, "fraction range")
    f = F(n, d)
    require([f.numerator, f.denominator] == value, "reduced fraction")
    require(max(abs(n).bit_length(), d.bit_length()) <= 4096, "fraction bit bound")
    return f


def fq(value, signed=False):
    require((-2 if signed else 0) <= value <= 2, "retained score interval")
    answer = [value.numerator, value.denominator]
    require(max(abs(v).bit_length() for v in answer) <= 4096, "retained score bits")
    return answer


def law(rows):
    return {tuple(r["value"]): fraction(r["probability"]) for r in rows}


def fixtures():
    raw = plain_bytes(HERE.parent / X_PRIOR)
    require(len(raw) == X_BYTES and digest(raw) == X_SHA, "pinned X artifact")
    doc = json.loads(raw)
    require(canonical(doc) == raw, "canonical X envelope")
    require_wire(doc["suite"])
    expected = {**doc["prior_artifacts"], X_PRIOR: {"bytes": X_BYTES, "sha256": X_SHA}}
    require_same_wire(expected, priors(), "exact inherited 29-artifact inventory")
    require(len(doc["suite"]["cases"]) == 6, "six fixed X cases")
    return doc["suite"]


def w_case(case_id):
    candidates = [c for c in prior_json(W_PRIOR)["suite"]["cases"] if c["case_id"] == case_id]
    require(len(candidates) == 1, "unknown W case")
    return candidates[0]


def case_problem(case):
    old = w_case(case["case_id"])
    require(len(case["problem"]["beliefs"]) == len(old["analysis"]["beliefs"]), "W/X history count")
    beliefs = []
    for xrow, wrow in zip(case["problem"]["beliefs"], old["analysis"]["beliefs"], strict=True):
        require_same_wire(xrow["belief_id"], wrow["belief_id"], "W/X history ID")
        require_same_wire(xrow["weight"], wrow["weight"], "W/X likelihood")
        projected = [
            {
                "level": c["level"],
                "cells": [
                    {k: s[k] for k in ("value", "probability", "prediction")} for s in c["cells"]
                ],
            }
            for c in wrow["channels"]
        ]
        require_same_wire(xrow["channels"], projected, "W/X complete noisy law projection")
        beliefs.append(
            {
                **copy.deepcopy(xrow),
                "fallbacks": [
                    {k: copy.deepcopy(c[k]) for k in ("value", "prediction")}
                    for c in wrow["controls"]["N"]["cells"]
                ],
            }
        )
    return {
        "schema_version": "det8-qr05y-problem-v1",
        "family": "qr05y_explicit_fallback",
        "beliefs": beliefs,
    }


def coordinate_score(p, f):
    """Coordinate-wise Bernoulli loss; independent of either core."""
    support = sorted(p.keys() | f.keys())
    score = sum(
        (
            p.get(q, F(0)) * (1 - f.get(q, F(0))) ** 2 + (1 - p.get(q, F(0))) * f.get(q, F(0)) ** 2
            for q in support
        ),
        F(0),
    )
    distance = sum(((p.get(q, F(0)) - f.get(q, F(0))) ** 2 for q in support), F(0))
    bayes = sum((u * (1 - u) for u in p.values()), F(0))
    require(
        score == bayes + distance and (distance == 0) == (p == f),
        "complete cell law/score identity",
    )
    require(0 <= score <= 2 and 0 <= distance <= 2, "conditional score range")
    return bayes, score, distance


def check_totals(x, y, equal_policy, equal_coarse, supported_gain):
    require(x["coverage"] + x["unsupported_mass"] == 1, "original support/fallback mass")
    require(x["bayes_risk"] == x["supported_bayes_risk"] + y["fallback_bayes_risk"], "split Bayes")
    require(
        x["supported_forecast_risk"] == x["supported_bayes_risk"] + x["supported_regret"],
        "supported decomposition",
    )
    require(
        y["fallback_forecast_risk"] == y["fallback_bayes_risk"] + y["fallback_regret"],
        "fallback decomposition",
    )
    require(
        y["completed_forecast_risk"] == x["supported_forecast_risk"] + y["fallback_forecast_risk"],
        "split policy risk",
    )
    require(
        y["completed_regret"] == x["supported_regret"] + y["fallback_regret"], "split policy regret"
    )
    require(
        y["completed_forecast_risk"] == x["bayes_risk"] + y["completed_regret"],
        "completed identity",
    )
    require(y["coarse_forecast_risk"] == x["bayes_risk"] + y["coarse_regret"], "coarse identity")
    require(
        y["gain_over_coarse"]
        == y["coarse_forecast_risk"] - y["completed_forecast_risk"]
        == y["coarse_regret"] - y["completed_regret"]
        == supported_gain,
        "signed gain identity",
    )
    require(abs(y["gain_over_coarse"]) <= 2 * x["coverage"], "support-scaled signed gain bound")
    require(
        (y["completed_regret"] == 0) == equal_policy, "completed zero regret iff full laws equal"
    )
    require((y["coarse_regret"] == 0) == equal_coarse, "coarse zero regret iff full laws equal")
    for mass, bayes, risk, regret in (
        (
            x["coverage"],
            x["supported_bayes_risk"],
            x["supported_forecast_risk"],
            x["supported_regret"],
        ),
        (
            x["unsupported_mass"],
            y["fallback_bayes_risk"],
            y["fallback_forecast_risk"],
            y["fallback_regret"],
        ),
    ):
        require(
            0 <= bayes <= mass and 0 <= risk <= 2 * mass and 0 <= regret <= 2 * mass,
            "split mass-scaled bounds",
        )


def expected_analysis(problem):
    rows = []
    completed_terms = coarse_terms = 0
    for entry in problem["beliefs"]:
        channels = [{tuple(c["value"]): c for c in ch["cells"]} for ch in entry["channels"]]
        fallback = {tuple(r["value"]): r["prediction"] for r in entry["fallbacks"]}
        pairs = []
        for i in range(4):
            for j in range(4):
                x = {key: F(0) for key in X_LINEAR}
                y = {key: F(0) for key in Y_LINEAR}
                cells = []
                supported_gain = F(0)
                for z, actual in sorted(channels[i].items()):
                    w = fraction(actual["probability"])
                    p = law(actual["prediction"])
                    assumed = channels[j].get(z)
                    supported = assumed is not None
                    coarse_wire = fallback[z[:5]]
                    chosen_wire = assumed["prediction"] if supported else coarse_wire
                    f, g = law(chosen_wire), law(coarse_wire)
                    bayes, score, regret = coordinate_score(p, f)
                    coarse_bayes, coarse_score, coarse_regret = coordinate_score(p, g)
                    require(coarse_bayes == bayes, "common actual conditional law")
                    completed_terms += len(p) + len(f)
                    coarse_terms += len(p) + len(g)
                    gain = coarse_score - score
                    if not supported:
                        require(f == g and gain == 0, "fallback branch equals coarse comparator")
                    else:
                        require_same_wire(
                            chosen_wire, assumed["prediction"], "unchanged supported forecast"
                        )
                        supported_gain += w * gain
                    x["bayes_risk"] += w * bayes
                    x["coverage" if supported else "unsupported_mass"] += w
                    if supported:
                        x["supported_bayes_risk"] += w * bayes
                        x["supported_forecast_risk"] += w * score
                        x["supported_regret"] += w * regret
                    else:
                        y["fallback_bayes_risk"] += w * bayes
                        y["fallback_forecast_risk"] += w * score
                        y["fallback_regret"] += w * regret
                    y["completed_forecast_risk"] += w * score
                    y["completed_regret"] += w * regret
                    y["coarse_forecast_risk"] += w * coarse_score
                    y["coarse_regret"] += w * coarse_regret
                    y["gain_over_coarse"] += w * gain
                    cells.append(
                        {
                            "value": list(z),
                            "actual_probability": fq(w),
                            "assumed_probability": copy.deepcopy(assumed["probability"])
                            if supported
                            else [0, 1],
                            "actual_prediction": copy.deepcopy(actual["prediction"]),
                            "assumed_forecast": copy.deepcopy(assumed["prediction"])
                            if supported
                            else None,
                            "coarse_forecast": copy.deepcopy(coarse_wire),
                            "forecast": copy.deepcopy(chosen_wire),
                            "supported": supported,
                            "used_fallback": not supported,
                            "bayes_risk": fq(bayes),
                            "forecast_risk": fq(score),
                            "regret": fq(regret),
                            "coarse_risk": fq(coarse_score),
                            "coarse_regret": fq(coarse_regret),
                            "gain_over_coarse": fq(gain, True),
                            "predictions_equal": p == f,
                            "coarse_predictions_equal": p == g,
                        }
                    )
                check_totals(
                    x,
                    y,
                    all(c["predictions_equal"] for c in cells),
                    all(c["coarse_predictions_equal"] for c in cells),
                    supported_gain,
                )
                complete = x["coverage"] == 1
                x_scores = {
                    **{k: fq(v) for k, v in x.items()},
                    "forecast_risk": fq(x["supported_forecast_risk"]) if complete else None,
                    "regret": fq(x["supported_regret"]) if complete else None,
                    "complete": complete,
                }
                pairs.append(
                    {
                        "actual_index": i,
                        "assumed_index": j,
                        "cells": cells,
                        "x_scores": x_scores,
                        **{k: fq(v, k == "gain_over_coarse") for k, v in y.items()},
                        "checks": {k: True for k in CHECK_FIELDS},
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
    require(sum(weights) == 1, "unchanged original likelihood weights")
    aggregate = []
    for k in range(16):
        x = {
            name: sum(
                (
                    w * fraction(r["pairs"][k]["x_scores"][name])
                    for w, r in zip(weights, rows, strict=True)
                ),
                F(0),
            )
            for name in X_LINEAR
        }
        y = {
            name: sum(
                (w * fraction(r["pairs"][k][name]) for w, r in zip(weights, rows, strict=True)),
                F(0),
            )
            for name in Y_LINEAR
        }
        supported_gain = sum(
            (
                w * fraction(c["actual_probability"]) * fraction(c["gain_over_coarse"])
                for w, r in zip(weights, rows, strict=True)
                for c in r["pairs"][k]["cells"]
                if c["supported"]
            ),
            F(0),
        )
        check_totals(
            x,
            y,
            all(c["predictions_equal"] for r in rows for c in r["pairs"][k]["cells"]),
            all(c["coarse_predictions_equal"] for r in rows for c in r["pairs"][k]["cells"]),
            supported_gain,
        )
        count = sum(r["pairs"][k]["x_scores"]["complete"] for r in rows)
        complete = count == len(rows)
        require(complete == (x["coverage"] == 1), "positive-weight aggregate completeness")
        aggregate.append(
            {
                "actual_index": k // 4,
                "assumed_index": k % 4,
                "x_scores": {
                    **{key: fq(v) for key, v in x.items()},
                    "forecast_risk": fq(x["supported_forecast_risk"]) if complete else None,
                    "regret": fq(x["supported_regret"]) if complete else None,
                    "complete": complete,
                },
                **{name: fq(v, name == "gain_over_coarse") for name, v in y.items()},
                "checks": {key: True for key in CHECK_FIELDS},
                "complete_before_beliefs": count,
                "incomplete_before_beliefs": len(rows) - count,
            }
        )

    def first(k, predicate):
        return next((r["belief_id"] for r in rows if predicate(r["pairs"][k])), None)

    witnesses = {
        "first_fallback": [
            first(k, lambda p: fraction(p["x_scores"]["unsupported_mass"]) > 0) for k in range(16)
        ],
        "first_positive_fallback_regret": [
            first(k, lambda p: fraction(p["fallback_regret"]) > 0) for k in range(16)
        ],
        "first_positive_completed_regret": [
            first(k, lambda p: fraction(p["completed_regret"]) > 0) for k in range(16)
        ],
        "first_better_than_coarse": [
            first(k, lambda p: fraction(p["gain_over_coarse"]) > 0) for k in range(16)
        ],
        "first_equal_to_coarse": [
            first(k, lambda p: fraction(p["gain_over_coarse"]) == 0) for k in range(16)
        ],
        "first_worse_than_coarse": [
            first(k, lambda p: fraction(p["gain_over_coarse"]) < 0) for k in range(16)
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
        "input_fallbacks": sum(len(b["fallbacks"]) for b in problem["beliefs"]),
        "input_fallback_atoms": sum(
            len(f["prediction"]) for b in problem["beliefs"] for f in b["fallbacks"]
        ),
        "pair_cells": [sum(len(r["pairs"][k]["cells"]) for r in rows) for k in range(16)],
        "supported_pair_cells": [
            sum(c["supported"] for r in rows for c in r["pairs"][k]["cells"]) for k in range(16)
        ],
        "fallback_pair_cells": [
            sum(c["used_fallback"] for r in rows for c in r["pairs"][k]["cells"]) for k in range(16)
        ],
        "completed_scoring_terms": completed_terms,
        "coarse_scoring_terms": coarse_terms,
        "complete_before_beliefs": [p["complete_before_beliefs"] for p in aggregate],
        "incomplete_before_beliefs": [p["incomplete_before_beliefs"] for p in aggregate],
        "positive_fallback_regret_beliefs": [
            sum(fraction(r["pairs"][k]["fallback_regret"]) > 0 for r in rows) for k in range(16)
        ],
        "positive_completed_regret_beliefs": [
            sum(fraction(r["pairs"][k]["completed_regret"]) > 0 for r in rows) for k in range(16)
        ],
        "better_than_coarse_beliefs": [
            sum(fraction(r["pairs"][k]["gain_over_coarse"]) > 0 for r in rows) for k in range(16)
        ],
        "equal_to_coarse_beliefs": [
            sum(fraction(r["pairs"][k]["gain_over_coarse"]) == 0 for r in rows) for k in range(16)
        ],
        "worse_than_coarse_beliefs": [
            sum(fraction(r["pairs"][k]["gain_over_coarse"]) < 0 for r in rows) for k in range(16)
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


def producer_controls(analysis, case):
    old = w_case(case["case_id"])
    for row, xrow, wrow in zip(
        analysis["beliefs"], case["analysis"]["beliefs"], old["analysis"]["beliefs"], strict=True
    ):
        require_same_wire(row["belief_id"], xrow["belief_id"], "unchanged X belief ID")
        require_same_wire(row["weight"], xrow["weight"], "unchanged X likelihood")
        n_cells = {tuple(c["value"]): c for c in wrow["controls"]["N"]["cells"]}
        w_noisy = [{tuple(c["value"]): c for c in channel["cells"]} for channel in wrow["channels"]]
        for k, (p, xp) in enumerate(zip(row["pairs"], xrow["pairs"], strict=True)):
            require_same_wire(
                p["x_scores"],
                {key: xp[key] for key in X_FIELDS},
                "complete original X scores preserved",
            )
            require_same_wire(
                p["coarse_forecast_risk"], wrow["controls"]["N"]["expected_risk"], "W N comparator"
            )
            require(p["fallback_regret"] == [0, 1], "predicted W fallback zero regret")
            require_same_wire(
                p["completed_regret"], xp["supported_regret"], "W completed equals supported regret"
            )
            require(
                fraction(p["completed_forecast_risk"])
                == fraction(xp["supported_forecast_risk"])
                + fraction(xp["bayes_risk"])
                - fraction(xp["supported_bayes_risk"]),
                "W predicted completion identity",
            )
            require(len(p["cells"]) == len(xp["cells"]), "all actual cells retained")
            for cell, xcell in zip(p["cells"], xp["cells"], strict=True):
                for key in (
                    "value",
                    "actual_probability",
                    "assumed_probability",
                    "actual_prediction",
                    "supported",
                ):
                    require_same_wire(cell[key], xcell[key], "X actual/report law preserved")
                require_same_wire(
                    cell["assumed_forecast"], xcell["forecast"], "X assumed forecast preserved"
                )
                n = n_cells[tuple(cell["value"][:5])]
                require_same_wire(cell["coarse_forecast"], n["prediction"], "N fallback source")
                if cell["used_fallback"]:
                    require_same_wire(
                        w_noisy[k // 4][tuple(cell["value"])]["posterior"],
                        n["posterior"],
                        "predicted W complete fallback current posterior equals N",
                    )
                    require_same_wire(
                        cell["actual_prediction"],
                        cell["forecast"],
                        "predicted W full fallback future law",
                    )
                    require(
                        cell["regret"] == [0, 1] and cell["gain_over_coarse"] == [0, 1],
                        "W fallback identities",
                    )
                else:
                    require_same_wire(
                        cell["forecast"], xcell["forecast"], "supported X forecast unchanged"
                    )
                    require_same_wire(
                        cell["forecast_risk"], xcell["forecast_risk"], "supported X risk unchanged"
                    )
                    require_same_wire(
                        cell["regret"], xcell["regret"], "supported X regret unchanged"
                    )
            if k // 4 == k % 4:
                require(p["completed_regret"] == [0, 1], "unchanged Bayes-correct diagonal")
    for p, xp in zip(
        analysis["aggregate"]["pairs"], case["analysis"]["aggregate"]["pairs"], strict=True
    ):
        require_same_wire(
            p["x_scores"],
            {key: xp[key] for key in X_FIELDS},
            "aggregate original X scores preserved",
        )
        require_same_wire(
            p["coarse_forecast_risk"],
            old["analysis"]["aggregate"]["N_risk"],
            "weighted W N comparator",
        )
        require(p["fallback_regret"] == [0, 1], "weighted W fallback zero regret")
        require_same_wire(
            p["completed_regret"], xp["supported_regret"], "weighted W completion regret"
        )
    return {
        "X_laws_and_W_N_fallbacks_are_declared_dependencies": True,
        "complete_original_X_scores_and_nulls_preserved": True,
        "supported_forecasts_and_scores_preserved": True,
        "W_fallback_future_laws_equal_actual": True,
        "W_fallback_regret_zero": True,
        "W_completion_identity": True,
        "coarse_only_W_N_risk_equal": True,
        "channel_or_fallback_origin_authenticated_by_generic_API": False,
        "raw_history_reconstruction_performed_by_this_runner": False,
    }


def check_analysis(analysis, case):
    require_wire(analysis)
    require_wire(case)
    candidates = [c for c in fixtures()["cases"] if c["case_id"] == case["case_id"]]
    require(len(candidates) == 1, "unknown X case")
    require_same_wire(case, candidates[0], "X producer case differs")
    expected = expected_analysis(case_problem(case))
    require_same_wire(analysis, expected, "complete independent Y scoring audit differs")
    producer_controls(analysis, case)
    return {"analysis_sha256": digest(canonical(expected)), "complete_native_output_equal": True}


def run_suite():
    primary = load("_qr05y_primary", "fallback.py")
    reference = load("_qr05y_reference", "reference_qr05y.py")
    data = fixtures()
    cases = []
    for case in data["cases"]:
        problem = case_problem(case)
        before = canonical(problem)
        a = primary.analyze(problem)
        require(canonical(problem) == before, "primary input mutation")
        b = reference.analyze(problem)
        require(canonical(problem) == before, "reference input mutation")
        require_same_wire(a, b, "independent Y routes differ")
        require_same_wire(a, expected_analysis(problem), "independent Y runner score differs")
        controls = producer_controls(a, case)
        cases.append(
            {
                "case_id": case["case_id"],
                "problem": problem,
                "analysis": a,
                "producer_controls": controls,
            }
        )
    invalid = 0
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
                invalid += 1
            else:
                raise ValueError("malformed Y input accepted")
    require(invalid == 14, "public malformed control inventory")
    totals = {
        "cases": len(cases),
        "analyze_calls": 2 * len(cases),
        "invalid_analyze_calls_rejected": invalid,
    }
    for key, value in cases[0]["analysis"]["counts"].items():
        totals[key] = (
            [sum(c["analysis"]["counts"][key][k] for c in cases) for k in range(16)]
            if type(value) is list
            else sum(c["analysis"]["counts"][key] for c in cases)
        )
    return {
        "producer": {"artifact": X_PRIOR, "bytes": X_BYTES, "sha256": X_SHA},
        "cases": cases,
        "independent_route_equal": True,
        "public_controls": {
            "analyze_calls": 12,
            "invalid_analyze_calls_rejected": invalid,
            "raw_orders_histories_or_artifacts_given_to_core": False,
            "fallback_rule_explicit": True,
            "fallback_optimized": False,
            "actual_level_used_to_select_forecast": False,
        },
        "totals": totals,
    }


if __name__ == "__main__":
    main()
