"""Independent reference route for the QR-05CA synthetic pipeline rehearsal.

Exact rational arithmetic only. This route uses a different reduction
(Counter over usable events), the BU segment-parameter ideal-point formula,
an inverted loop nesting for the inverse, and differently written
feasibility/dynamics predicates. It must reproduce the primary report
exactly.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction as F

SCHEMA = "qr05ca-report-v1"
Y1 = ("10", "11")
TARGET = {0: F(1, 4), 1: F(17, 80)}
DATASET_KEYS = ("id", "analysis_id", "marks_match", "attempts", "loss_bound", "stationarity_tol")


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def q_point(eta, delta):
    """Ideal point via the BU segment-parameter formulas."""
    if eta == 0:
        t = delta / (4 + delta)
        return ((1 - t) * F(1, 4) + t * F(1, 16), (1 - t) * F(3, 8) + t * F(9, 64))
    t = 13 * delta / (45 + 13 * delta)

    def component(z):
        return (1 - t) * (4 * z + z * z) / 5 + t * (9 * z * z + 4 * z * z * z) / 13

    return (component(F(1, 4)), component(F(3, 8)))


def reduce_dataset(dataset, analysis_id):
    core = {key: dataset[key] for key in DATASET_KEYS if key in dataset}
    seal = dataset.get("seal")
    if seal is not None and seal != hashlib.sha256(canonical_bytes(core)).hexdigest():
        return {"id": dataset["id"], "status": "refused", "reason": "integrity"}
    if dataset.get("analysis_id", "") != analysis_id:
        return {"id": dataset["id"], "status": "refused", "reason": "analysis_id"}
    if dataset.get("marks_match", True) is not True:
        return {"id": dataset["id"], "status": "refused", "reason": "mark"}

    events = [attempt["event"] for attempt in dataset["attempts"]]
    if "10" in events:
        return {"id": dataset["id"], "status": "refused", "reason": "support"}

    total = len(events)
    losses = [attempt["loss"] for attempt in dataset["attempts"]]
    loss_count = sum(1 for flag in losses if flag)
    usable_events = [event for event, flag in zip(events, losses) if not flag]
    usable_count = len(usable_events)
    loss_fraction = F(loss_count, total) if total else F(0)
    if loss_fraction > frac(dataset["loss_bound"]):
        return {"id": dataset["id"], "status": "refused", "reason": "loss"}
    if usable_count < 4:
        return {"id": dataset["id"], "status": "refused", "reason": "insufficient"}

    counts = Counter(usable_events)
    k1 = counts["10"] + counts["11"]
    k2 = counts["01"] + counts["11"]
    if k1 < 0 or k1 > k2 or k2 > usable_count:
        return {"id": dataset["id"], "status": "refused", "reason": "support"}

    half = usable_count // 2
    left = usable_events[:half]
    right = usable_events[usable_count - half:]
    f1 = F(sum(1 for event in left if event in Y1), len(left))
    f2 = F(sum(1 for event in right if event in Y1), len(right))
    diff = abs(f1 - f2)
    tol = frac(dataset["stationarity_tol"])
    if diff > tol:
        return {"id": dataset["id"], "status": "refused", "reason": "stationarity"}

    return {
        "id": dataset["id"],
        "status": "accepted",
        "K1": k1,
        "K2": k2,
        "n_eff": usable_count,
        "r_hat": [F(k1, usable_count), F(k2, usable_count)],
        "loss": {"count": loss_count, "fraction": loss_fraction, "bound": frac(dataset["loss_bound"])},
        "stationarity": {"f1": f1, "f2": f2, "diff": diff, "tol": tol},
    }


def inverse_case(r_hat, b_list, e):
    admitted = {}
    for delta_pair in b_list:
        delta = frac(delta_pair)
        for eta in (0, 1):
            q = q_point(eta, delta)
            distance = max(abs(r_hat[0] - q[0]), abs(r_hat[1] - q[1]))
            if distance <= e:
                current = admitted.get(eta)
                if current is None or delta < current[0]:
                    admitted[eta] = (delta, distance)
    return {
        "targets": sorted(TARGET[eta] for eta in admitted),
        "witness": [
            {"eta": eta, "delta": admitted[eta][0], "distance": admitted[eta][1]}
            for eta in sorted(admitted)
        ],
    }


def allowance_case(case):
    parts = [frac(case["a_sys"]), frac(case["a_stat"]), frac(case["d_sys"]), frac(case["d_stat"])]
    e_cal = sum(parts, F(0))
    beta = sum((frac(case[key]) for key in ("beta_ref", "beta_tr", "beta_env")), F(0))
    e_max = frac(case["e_max"])
    return {"id": case["id"], "e_cal": e_cal, "beta": beta, "e_max": e_max, "within": not (e_cal > e_max)}


def feasibility_case(case):
    h = F(1, int(case["m"]))
    s = frac(case["D"]) - 2 * (frac(case["e_max"]) + h)
    score = int(case["n"]) * s ** 2
    certified = s > 0 and score >= 10
    return {"id": case["id"], "s": s, "score": score, "certified": certified}


def by_case(case):
    dims = [F(int(value)) for value in case["dim_estimates"]]
    spread = dims[-1] - dims[0] if len(dims) == 1 else max(dims) - min(dims)
    metric_tests = {
        "M1_dimension_stable": spread <= frac(case["tol"]),
        "M2_causal_consistent": case["causal_consistent"],
        "M3_collision_declared": case["collision_declared"],
    }
    dynamics_tests = {
        "D1_well_defined_law": case["normalized"] and not case["preferred_clock"],
        "D2_stable_limit": case["limit_stable"],
    }
    metric = "refute"
    if all(metric_tests.values()):
        metric = "pass"
    dynamics = "refute"
    if all(dynamics_tests.values()):
        dynamics = "pass"
    return {
        "id": case["id"],
        "metric": metric,
        "dynamics": dynamics,
        "metric_tests": metric_tests,
        "dynamics_tests": dynamics_tests,
        "dim_spread": spread,
    }


def _by_lookup(by_cases, key):
    match = [case for case in by_cases if case["id"] == key]
    if not match:
        raise KeyError(key)
    return by_case(match[0])


def pipeline(dataset, analysis_id, by_cases):
    result = reduce_dataset(dataset, analysis_id)
    if result["status"] == "refused":
        return result
    case = dataset["case"]
    result["inverse"] = inverse_case(result["r_hat"], case["B"], frac(case["e"]))
    result["by"] = _by_lookup(by_cases, case["by"])
    return result


def build_report(protocol):
    analysis_id = protocol["analysis_id"]
    by_cases = protocol["by_cases"]
    return {
        "schema": SCHEMA,
        "analysis_id": analysis_id,
        "datasets": [pipeline(ds, analysis_id, by_cases) for ds in protocol["datasets"]],
        "refusals": [pipeline(ds, analysis_id, by_cases) for ds in protocol["refusals"]],
        "allowances": [allowance_case(item) for item in protocol["allowances"]],
        "inverses": [
            {"id": item["id"], **inverse_case([frac(item["r_hat"][0]), frac(item["r_hat"][1])],
                                              item["B"], frac(item["e"]))}
            for item in protocol["inverses"]
        ],
        "feasibility": [feasibility_case(item) for item in protocol["feasibility"]],
        "by_tests": [by_case(item) for item in by_cases],
    }
