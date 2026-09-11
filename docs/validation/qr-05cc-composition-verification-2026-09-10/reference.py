"""Independent reference route for the QR-05CC composition verification.

Explicit coordinate comparisons instead of max(), and probability by summing
indicator functions over atoms in a different order. Must match the primary
report exactly.
"""

from __future__ import annotations

from fractions import Fraction as F

SCHEMA = "qr05cc-report-v1"


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def build_report(protocol):
    norms = []
    for item in protocol["norms"]:
        r = (frac(item["r"][0]), frac(item["r"][1]))
        rr = (frac(item["r_ref"][0]), frac(item["r_ref"][1]))
        q = (frac(item["q"][0]), frac(item["q"][1]))
        a, d = frac(item["a"]), frac(item["d"])
        dx = abs(r[0] - q[0])
        dy = abs(r[1] - q[1])
        e = dx if dx > dy else dy
        ax = abs(rr[0] - q[0])
        ay = abs(rr[1] - q[1])
        nrq = ax if ax > ay else ay
        bx = abs(r[0] - rr[0])
        by = abs(r[1] - rr[1])
        nrr = bx if bx > by else by
        norms.append({
            "id": item["id"], "e": e, "nrq": nrq, "nrr": nrr,
            "bound_ok": nrq <= a and nrr <= d and e <= a + d,
            "tight": e == a + d,
        })

    splits = []
    for item in protocol["splits"]:
        parts = [frac(item[key]) for key in ("a_sys", "a_stat", "d_sys", "d_stat")]
        total = F(0)
        for part in parts:
            total += part
        splits.append({"id": item["id"], "e_cal": total,
                       "matches_expected": total == frac(item["expected"]["e_cal"])})

    spaces = []
    for item in protocol["spaces"]:
        weights = [frac(value) for value in item["weights"]]

        def mass(members):
            members = set(members)
            total = F(0)
            for index, weight in enumerate(weights):
                if index in members:
                    total += weight
            return total

        alpha = mass([i for i in range(len(weights)) if i not in set(item["E"])])
        beta_ref = mass([i for i in range(len(weights)) if i not in set(item["Ga"])])
        beta_tr = mass([i for i in range(len(weights)) if i not in set(item["Gd"])])
        beta = beta_ref + beta_tr
        p_G = mass(set(item["Ga"]) & set(item["Gd"]))
        p_EG = mass(set(item["Ga"]) & set(item["Gd"]) & set(item["E"]))
        union_ok = (F(1) - p_G) <= beta and p_EG >= (F(1) - alpha - beta)
        product = (F(1) - alpha) * (F(1) - beta)
        spaces.append({
            "id": item["id"], "alpha": alpha, "beta_ref": beta_ref, "beta_tr": beta_tr,
            "beta": beta, "p_G": p_G, "p_EcapG": p_EG, "union_ok": union_ok,
            "product": product, "product_refuted": p_EG < product,
        })

    regimes = []
    for item in protocol["regimes"]:
        pH, alpha, beta = frac(item["pH"]), frac(item["alpha"]), frac(item["beta"])
        slack = pH - alpha - beta
        uncond = slack if slack > 0 else F(0)
        if pH > 0:
            regimes.append({"id": item["id"], "uncond": uncond, "cond": slack / pH, "defined": True})
        else:
            regimes.append({"id": item["id"], "uncond": uncond, "cond": None, "defined": False})

    repeats = []
    for item in protocol["repeats"]:
        budget = frac(item["beta"]) * int(item["K"])
        repeats.append({"id": item["id"], "budget": budget,
                        "matches_expected": budget == frac(item["expected"]["budget"])})

    schemas = []
    for item in protocol["schema_fixtures"]:
        statuses = [premise["status"] for premise in item["premises"]]
        conditional = len([s for s in statuses if s != "supplied"]) > 0
        schemas.append({"id": item["id"], "conditional_only": conditional,
                        "matches_expected": conditional == item["expected_conditional_only"]})

    return {"schema": SCHEMA, "norms": norms, "splits": splits, "spaces": spaces,
            "regimes": regimes, "repeats": repeats, "schemas": schemas}
