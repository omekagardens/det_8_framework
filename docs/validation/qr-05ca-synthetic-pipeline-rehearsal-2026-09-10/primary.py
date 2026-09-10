"""Primary route for the QR-05CA synthetic pipeline rehearsal.

Exact rational arithmetic only: no floats, no randomness, no I/O, no old
mathematical engine. Definitions run at import; ``build_report`` is pure.

The report is a native Python structure whose rational values are
``fractions.Fraction``. The study driver encodes it and compares it with the
independent reference route.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction as F

SCHEMA = "qr05ca-report-v1"
EVENT_XY = {"00": (0, 0), "01": (0, 1), "10": (1, 0), "11": (1, 1)}
TARGET = {0: F(1, 4), 1: F(17, 80)}
DATASET_KEYS = ("id", "analysis_id", "marks_match", "attempts", "loss_bound", "stationarity_tol")


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def canonical_bytes(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def dataset_core(dataset):
    return {key: dataset[key] for key in DATASET_KEYS if key in dataset}


def seal_of(core):
    return hashlib.sha256(canonical_bytes(core)).hexdigest()


def q_point(eta, delta):
    """Ideal point via direct polynomial masses (Section 1 of the BU model)."""
    def mass(z):
        return z + (eta + delta) * z * z / 4 + eta * delta * z ** 3 / 9

    norm = mass(F(1))
    return (mass(F(1, 4)) / norm, mass(F(3, 8)) / norm)


def reduce_dataset(dataset, analysis_id):
    core = dataset_core(dataset)
    if "seal" in dataset and dataset["seal"] != seal_of(core):
        return {"id": dataset["id"], "status": "refused", "reason": "integrity"}
    if dataset.get("analysis_id") != analysis_id:
        return {"id": dataset["id"], "status": "refused", "reason": "analysis_id"}
    if not dataset.get("marks_match", True):
        return {"id": dataset["id"], "status": "refused", "reason": "mark"}

    attempts = list(dataset["attempts"])
    if any(attempt["event"] == "10" for attempt in attempts):
        return {"id": dataset["id"], "status": "refused", "reason": "support"}

    total = len(attempts)
    usable = [attempt for attempt in attempts if not attempt["loss"]]
    usable_count = len(usable)
    loss_count = total - usable_count
    loss_fraction = F(loss_count, total) if total else F(0)
    if loss_fraction > frac(dataset["loss_bound"]):
        return {"id": dataset["id"], "status": "refused", "reason": "loss"}
    if usable_count < 4:
        return {"id": dataset["id"], "status": "refused", "reason": "insufficient"}

    k1 = sum(1 for attempt in usable if EVENT_XY[attempt["event"]][0])
    k2 = sum(1 for attempt in usable if EVENT_XY[attempt["event"]][1])
    if not (0 <= k1 <= k2 <= usable_count):
        return {"id": dataset["id"], "status": "refused", "reason": "support"}

    half = usable_count // 2
    first = usable[:half]
    second = usable[usable_count - half:]
    f1 = F(sum(1 for attempt in first if EVENT_XY[attempt["event"]][0]), len(first))
    f2 = F(sum(1 for attempt in second if EVENT_XY[attempt["event"]][0]), len(second))
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
    for eta in (0, 1):
        for delta_pair in b_list:
            delta = frac(delta_pair)
            q = q_point(eta, delta)
            distance = max(abs(r_hat[0] - q[0]), abs(r_hat[1] - q[1]))
            if distance <= e and (eta not in admitted or delta < admitted[eta][0]):
                admitted[eta] = (delta, distance)
    return {
        "targets": sorted(TARGET[eta] for eta in admitted),
        "witness": [
            {"eta": eta, "delta": admitted[eta][0], "distance": admitted[eta][1]}
            for eta in sorted(admitted)
        ],
    }


def allowance_case(case):
    e_cal = frac(case["a_sys"]) + frac(case["a_stat"]) + frac(case["d_sys"]) + frac(case["d_stat"])
    beta = frac(case["beta_ref"]) + frac(case["beta_tr"]) + frac(case["beta_env"])
    e_max = frac(case["e_max"])
    return {"id": case["id"], "e_cal": e_cal, "beta": beta, "e_max": e_max, "within": e_cal <= e_max}


def feasibility_case(case):
    h = F(1, int(case["m"]))
    s = frac(case["D"]) - 2 * frac(case["e_max"]) - 2 * h
    score = int(case["n"]) * s * s
    return {"id": case["id"], "s": s, "score": score, "certified": bool(s > 0 and score >= 10)}


def by_case(case):
    dims = [F(int(value)) for value in case["dim_estimates"]]
    spread = max(dims) - min(dims)
    metric_tests = {
        "M1_dimension_stable": bool(spread <= frac(case["tol"])),
        "M2_causal_consistent": bool(case["causal_consistent"]),
        "M3_collision_declared": bool(case["collision_declared"]),
    }
    dynamics_tests = {
        "D1_well_defined_law": bool(case["normalized"] and not case["preferred_clock"]),
        "D2_stable_limit": bool(case["limit_stable"]),
    }
    return {
        "id": case["id"],
        "metric": "pass" if all(metric_tests.values()) else "refute",
        "dynamics": "pass" if all(dynamics_tests.values()) else "refute",
        "metric_tests": metric_tests,
        "dynamics_tests": dynamics_tests,
        "dim_spread": spread,
    }


def _by_lookup(by_cases, key):
    for case in by_cases:
        if case["id"] == key:
            return by_case(case)
    raise KeyError(key)


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
