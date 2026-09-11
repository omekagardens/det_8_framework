"""Independent reference route for QR-05DB.

Same report by different mechanics, so the two routes must agree before the gate
is published:

  - longest chains by a backward (intermediate-node) recurrence instead of the
    forward source dynamic program;
  - interval counts by integer bitmasks and ``int.bit_count`` instead of set
    intersections;
  - the axiom censuses recoded over a different loop nesting;
  - the report, spec and verdict recoded.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05db-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _round(value, places=9):
    return round(value, places)


def _spatial_sq(p, q):
    return sum((q[k] - p[k]) ** 2 for k in range(1, len(p)))


def _causality(points):
    n = len(points)
    out = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dt = points[j][0] - points[i][0]
                if dt > 0 and _spatial_sq(points[i], points[j]) < dt * dt:
                    out[i][j] = True
    return out


def _chains(prec, order):
    n = len(prec)
    ch = [[0] * n for _ in range(n)]
    for j in reversed(order):
        for i in reversed(order):
            if not prec[i][j]:
                continue
            best = 0
            for k in range(n):
                if prec[i][k] and prec[k][j] and ch[k][j] > best:
                    best = ch[k][j]
            ch[i][j] = 1 + best
    return ch


def _counts(prec, order):
    n = len(prec)
    desc = [0] * n
    for src in reversed(order):
        mask = 0
        for k in range(n):
            if prec[src][k]:
                mask |= (1 << k) | desc[k]
        desc[src] = mask
    anc = [0] * n
    for src in order:
        mask = 0
        for k in range(n):
            if prec[k][src]:
                mask |= (1 << k) | anc[k]
        anc[src] = mask
    return [[(desc[i] & anc[j]).bit_count() if prec[i][j] else 0 for j in range(n)]
            for i in range(n)]


def _chain_estimator(prec, order, ell=1.0):
    L = _chains(prec, order)
    return [[L[i][j] * ell for j in range(len(prec))] for i in range(len(prec))]


def _count_offset(prec, counts, ell=1.0):
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j] + 1) if prec[i][j] else 0.0
             for j in range(n)] for i in range(n)]


def _count_raw(prec, counts, ell=1.0):
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j]) if prec[i][j] and counts[i][j] > 0 else 0.0
             for j in range(n)] for i in range(n)]


def _support(D, prec, tol):
    n = len(prec)
    mism = 0
    causal = 0
    zero = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            pos = D[i][j] > tol
            if pos != bool(prec[i][j]):
                mism += 1
            if prec[i][j]:
                causal += 1
                if not pos:
                    zero += 1
    return mism, causal, zero


def _reverse(D, prec, tol):
    n = len(prec)
    viol = 0
    triples = 0
    worst = float("inf")
    witness = None
    for i in range(n):
        row_i = D[i]
        prec_i = prec[i]
        for j in range(n):
            if not prec_i[j]:
                continue
            mid = row_i[j]
            for k in range(n):
                if not prec[j][k]:
                    continue
                triples += 1
                gap = row_i[k] - mid - D[j][k]
                if gap < worst:
                    worst = gap
                    witness = [i, j, k]
                if gap < -tol:
                    viol += 1
    if worst == float("inf"):
        return viol, triples, 0.0, None
    return viol, triples, _round(worst), (witness if worst < -tol else None)


# Public wrappers (dict-returning) so the known-answer tests exercise both routes
# uniformly; build_report uses the tuple-returning internals directly.
chain_estimator = _chain_estimator
count_offset = _count_offset
count_raw = _count_raw


def support_census(D, prec, tol):
    mism, causal, zero = _support(D, prec, tol)
    return {"support_mismatches": mism, "causal_pairs": causal, "zero_on_causal": zero}


def reverse_triangle_census(D, prec, tol):
    viol, triples, worst, witness = _reverse(D, prec, tol)
    return {"reverse_triangle_violations": viol, "triples": triples,
            "worst_gap": worst, "witness": witness}


def _pure_chain(n):
    return {"name": f"pure_chain_n{n}", "kind": "chain", "n": n,
            "prec": [[j > i for j in range(n)] for i in range(n)], "order": list(range(n))}


def _antichain(n):
    return {"name": f"antichain_n{n}", "kind": "antichain", "n": n,
            "prec": [[False] * n for _ in range(n)], "order": list(range(n))}


def _random_poset(n, p, seed):
    rng = random.Random(seed)
    rank = list(range(n))
    rng.shuffle(rank)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if rank[i] < rank[j] and rng.random() < p:
                prec[i][j] = True
    for k in range(n):
        for i in range(n):
            if prec[i][k]:
                for j in range(n):
                    if prec[k][j]:
                        prec[i][j] = True
    return {"name": f"random_poset_n{n}", "kind": "poset", "n": n,
            "prec": prec, "order": sorted(range(n), key=lambda i: rank[i])}


def _sprinkle(module, dim, n, seed):
    points = module.sprinkle_diamond(dim, n, seed=seed)
    order = sorted(range(n), key=lambda i: points[i][0])
    return {"name": f"sprinkle_d{dim}_n{n}", "kind": "sprinkle", "n": n, "dim": dim,
            "prec": _causality(points), "order": order, "points": points}


def _objects(module, protocol):
    out = []
    for dim in protocol["sprinkle_dims"]:
        for n in protocol["sprinkle_n"]:
            out.append(_sprinkle(module, dim, n, protocol["seed"] + 100 * dim + n))
    out.append(_pure_chain(protocol["chain_len"]))
    out.append(_random_poset(protocol["poset_n"], protocol["poset_edge_prob"],
                             protocol["poset_seed"]))
    out.append(_antichain(protocol["antichain_len"]))
    return out


def _estimators(obj):
    prec, order = obj["prec"], obj["order"]
    counts = _counts(prec, order)
    return {"chain": _chain_estimator(prec, order),
            "count_offset": _count_offset(prec, counts),
            "count_raw": _count_raw(prec, counts)}, counts


def _three_chain():
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    prec = _causality(points)
    order = [0, 1, 2]
    counts = _counts(prec, order)
    offset = _count_offset(prec, counts)
    raw = _count_raw(prec, counts)
    chain = _chain_estimator(prec, order)
    return {
        "counts": {"m_ab": counts[0][1], "m_bc": counts[1][2], "m_ac": counts[0][2]},
        "count_offset": {"d_ab": offset[0][1], "d_bc": offset[1][2], "d_ac": offset[0][2],
                         "reverse_triangle_holds": bool(offset[0][2] >= offset[0][1] + offset[1][2])},
        "count_raw": {"d_ab": raw[0][1], "d_bc": raw[1][2], "d_ac": raw[0][2],
                      "reverse_triangle_holds": bool(raw[0][2] >= raw[0][1] + raw[1][2])},
        "chain": {"L_ab": chain[0][1], "L_bc": chain[1][2], "L_ac": chain[0][2],
                  "reverse_triangle_holds": bool(chain[0][2] >= chain[0][1] + chain[1][2])},
        "tau": {"tau_ac": 2.0, "reverse_triangle_holds": True},
    }


def _link_bound():
    ell = 1.0
    gaps = {m: _round(ell * (math.sqrt(1 + m) - 2.0)) for m in (1, 2, 3)}
    return {"gap_by_m_ac": {str(m): g for m, g in gaps.items()},
            "violating_for_m_ac_lt_3": True,
            "worst_lower_bound_on_unit_ell": _round(math.sqrt(2.0) - 2.0)}


def _structural(module, protocol):
    checked = 0
    total = 0
    viol = 0
    for obj in _objects(module, protocol):
        prec = obj["prec"]
        counts = _counts(prec, obj["order"])
        n = obj["n"]
        for i in range(n):
            for j in range(n):
                if not prec[i][j]:
                    continue
                for k in range(n):
                    if not prec[j][k]:
                        continue
                    total += 1
                    if counts[i][k] < counts[i][j] + counts[j][k] + 1:
                        viol += 1
        checked += 1
    return {"objects_checked": checked, "triples": total, "violations": viol}


def build_report(protocol):
    module = load_module("_qr05db_t7_ref", MODULE_PATH)
    tol = protocol["tol"]
    objs = _objects(module, protocol)

    rows = []
    for obj in objs:
        est, _counts_ = _estimators(obj)
        for name in ("chain", "count_offset", "count_raw"):
            D = est[name]
            mism, causal, zero = _support(D, obj["prec"], tol)
            viol, triples, worst, witness = _reverse(D, obj["prec"], tol)
            rows.append({
                "estimator": name, "object": obj["name"], "kind": obj["kind"], "n": obj["n"],
                "support_mismatches": mism, "causal_pairs": causal, "zero_on_causal": zero,
                "reverse_triangle_violations": viol, "triples": triples,
                "worst_gap": worst, "witness": witness,
            })

    def rows_for(name):
        return [r for r in rows if r["estimator"] == name]

    chain_rows = rows_for("chain")
    offset_rows = rows_for("count_offset")
    raw_rows = rows_for("count_raw")
    structural = _structural(module, protocol)

    flags = {
        "chain_satisfies_all_axioms": bool(all(
            r["support_mismatches"] == 0 and r["zero_on_causal"] == 0
            and r["reverse_triangle_violations"] == 0 for r in chain_rows)),
        "count_offset_support_exact": bool(all(
            r["support_mismatches"] == 0 for r in offset_rows)),
        "count_offset_violates_reverse_triangle": bool(any(
            r["reverse_triangle_violations"] > 0 for r in offset_rows)),
        "count_raw_fails_causal_support": bool(any(r["zero_on_causal"] > 0 for r in raw_rows)),
        "count_raw_reverse_triangle_fails_at_d2": bool(any(
            r["reverse_triangle_violations"] > 0 for r in raw_rows if r["kind"] == "sprinkle")),
        "structural_superadditivity_holds": bool(structural["violations"] == 0),
        "count_only_metric_established": False,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Can an order+count reconstruction be constructed with a "
                         "provable vanishing error bound while satisfying the required "
                         "Lorentzian metric-space properties?"),
            "admissible_class": ("fixed-count iid (Poisson) sprinklings into the unit causal "
                                 "diamond of d-dimensional Minkowski spacetime, d in "
                                 f"{protocol['sprinkle_dims']}; plus adversarial non-manifoldlike "
                                 "posets (pure chain, random poset, antichain)"),
            "density": "n iid points in the diamond; mean spacing ell = n^(-1/d)",
            "reconstruction": ("count-only d(i,j) = ell*(m_ij + s)^a, m_ij = #{k: i≺k≺j}; "
                               "tested: offset (s=1, a=1/2, QR-05DA) and raw (s=0, a=1/2); "
                               "order-only d = ell*L (longest chain)"),
            "scale": ("homothety only; absolute scale and reference are non-identifiable "
                      "from the order (QR-05CY)"),
            "axioms": ["A0 d(x,x)=0", "A1 d(x,y)>0 iff x≺y",
                       "A2 x≺y≺z => d(x,z) >= d(x,y)+d(y,z)"],
            "convergence": ("scale-free LGH distortion -> 0; pointwise d_ij -> c*tau_ij; the "
                            "count law m ~ rho*Vol(I) with the imported volume law "
                            "Vol(I(p,q)) = c_d*d(p,q)^d"),
            "bounds": ("constructive link-triple violation bound; structural "
                       "superadditivity m_ac >= m_ab+m_bc+1"),
            "controls": [o["name"] for o in objs if o["kind"] in ("chain", "poset", "antichain")],
        },
        "three_chain": _three_chain(),
        "link_triple_bound": _link_bound(),
        "structural_lemma": structural,
        "axiom_checks": rows,
        "flags": flags,
        "verdict": (
            "QR-05DB: the metric-axiom obstruction for count-only reconstructions. "
            "The order-only longest-chain estimator d = ell*L satisfies the Lorentzian "
            "distance axioms A0-A2 on every finite causal set tested (support exact, zero "
            "reverse-triangle violations), a Lorentzian premetric. The QR-05DA count "
            "estimator d = ell*sqrt(1+m) is positive exactly on the causal relation but "
            "violates the reverse-triangle inequality A2 on the sprinklings and controls "
            "(witness: the three-event chain gives ell*sqrt(2) < 2*ell). The offset-free "
            "count form ell*sqrt(m) satisfies A2 on chains in the continuum mean but assigns "
            "zero distance to links (fails A1). The count is structurally superadditive "
            "(m_ac >= m_ab+m_bc+1), and with the imported volume law Vol(I) = c_d*tau^d, "
            "convergence forces the exponent a = 1/d while positivity on links forces an "
            "offset s > 0 that breaks A2; so no count-only power reconstruction is both "
            "convergent and a Lorentzian metric with causal support. The axiom-compliant "
            "route is order-based; constructing a convergent order-based or mixed "
            "reconstruction remains open. No metric, continuum, curvature or gravity claim."),
    }
