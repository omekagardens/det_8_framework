"""Primary route for the QR-05CC reference-calibration composition verification.

Exact rational arithmetic over declared norm triples, finite probability
spaces, selection regimes and the auditable-schema flag. No floats, no
randomness, no external data.
"""

from __future__ import annotations

from fractions import Fraction as F

SCHEMA = "qr05cc-report-v1"


def frac(pair):
    return F(int(pair[0]), int(pair[1]))


def point(pair):
    return (frac(pair[0]), frac(pair[1]))


def sup(left, right):
    return max(abs(left[0] - right[0]), abs(left[1] - right[1]))


def build_report(protocol):
    norms = []
    for item in protocol["norms"]:
        r, rr, q = point(item["r"]), point(item["r_ref"]), point(item["q"])
        a, d = frac(item["a"]), frac(item["d"])
        e, nrq, nrr = sup(r, q), sup(rr, q), sup(r, rr)
        norms.append({
            "id": item["id"], "e": e, "nrq": nrq, "nrr": nrr,
            "bound_ok": bool(nrq <= a and nrr <= d and e <= a + d),
            "tight": bool(e == a + d),
        })

    splits = []
    for item in protocol["splits"]:
        e_cal = (frac(item["a_sys"]) + frac(item["a_stat"])
                 + frac(item["d_sys"]) + frac(item["d_stat"]))
        splits.append({"id": item["id"], "e_cal": e_cal,
                       "matches_expected": bool(e_cal == frac(item["expected"]["e_cal"]))})

    spaces = []
    for item in protocol["spaces"]:
        weights = [frac(value) for value in item["weights"]]

        def probability(indices):
            return sum((weights[index] for index in indices), F(0))

        p_E = probability(item["E"])
        p_Ga = probability(item["Ga"])
        p_Gd = probability(item["Gd"])
        g = sorted(set(item["Ga"]) & set(item["Gd"]))
        both = sorted(set(item["E"]) & set(g))
        p_G = probability(g)
        p_EG = probability(both)
        alpha = F(1) - p_E
        beta_ref = F(1) - p_Ga
        beta_tr = F(1) - p_Gd
        beta = beta_ref + beta_tr
        union_ok = bool((F(1) - p_G) <= beta and p_EG >= (F(1) - alpha - beta))
        product = (F(1) - alpha) * (F(1) - beta)
        spaces.append({
            "id": item["id"], "alpha": alpha, "beta_ref": beta_ref, "beta_tr": beta_tr,
            "beta": beta, "p_G": p_G, "p_EcapG": p_EG, "union_ok": union_ok,
            "product": product, "product_refuted": bool(p_EG < product),
        })

    regimes = []
    for item in protocol["regimes"]:
        pH, alpha, beta = frac(item["pH"]), frac(item["alpha"]), frac(item["beta"])
        uncond = max(F(0), pH - alpha - beta)
        defined = pH > 0
        cond = (pH - alpha - beta) / pH if defined else None
        regimes.append({"id": item["id"], "uncond": uncond, "cond": cond, "defined": bool(defined)})

    repeats = []
    for item in protocol["repeats"]:
        budget = int(item["K"]) * frac(item["beta"])
        repeats.append({"id": item["id"], "budget": budget,
                        "matches_expected": bool(budget == frac(item["expected"]["budget"]))})

    schemas = []
    for item in protocol["schema_fixtures"]:
        conditional = any(premise["status"] != "supplied" for premise in item["premises"])
        schemas.append({"id": item["id"], "conditional_only": bool(conditional),
                        "matches_expected": bool(conditional == item["expected_conditional_only"])})

    return {"schema": SCHEMA, "norms": norms, "splits": splits, "spaces": spaces,
            "regimes": regimes, "repeats": repeats, "schemas": schemas}
