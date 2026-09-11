"""Primary route for QR-05DB: the metric-axiom obstruction for count-only
reconstructions on a causal set.

PRE-SPECIFIED QUESTION. Can an order+count reconstruction be constructed with a
provable vanishing error bound while satisfying the required Lorentzian
metric-space properties?

AXIOMS (a Lorentzian distance/premetric on a finite causal set (X, ≺)):
  A0 (irreflexive zero)   d(x,x) = 0.
  A1 (causal support)     d(x,y) > 0  <=>  x ≺ y   (x != y).
  A2 (reverse triangle)   x ≺ y ≺ z  =>  d(x,z) >= d(x,y) + d(y,z).

RESULTS (proofs in RESULTS.md; the executable core verifies the finite witnesses):
  R1  The QR-05DA count estimator d = ell*sqrt(1+m_ij) violates A2 on actual
      Poisson sprinklings of Minkowski spacetime (census + explicit witness).  It
      is a distance ESTIMATOR, not a metric.
  R2  Count-only trade-off / impossibility.  For the count-only power family
      d(i,j) = ell*(m_ij + s)^a with m ~ rho*c_d*tau^d:
        - A2 on geodesic chains forces a >= 1/d (a < 1/d is subadditive);
        - convergence forces a = 1/d;
        - A1 on links (m = 0) forces s > 0, and s > 0 strictly breaks A2 at a = 1/d.
      So no count-only power reconstruction has convergence, positivity (A1) and
      A2 together.  The raw form ell*sqrt(m) (s = 0, a = 1/2) keeps A2 in the
      continuum-mean at d = 2 and fails A1; the DA offset restores A1 and fails A2.
  R3  The order-only longest-chain estimator d = ell*L satisfies A0-A2 on EVERY
      finite causal set (superadditivity of longest chains): it is a Lorentzian
      premetric.  QR-05DA shows its scale-free ceiling still does not vanish.
  R4  The interval count is superadditive: I(a,b) ⊔ I(b,c) ⊔ {b} ⊆ I(a,c), so
      m_ac >= m_ab + m_bc + 1 for every a ≺ b ≺ c (verified exactly here); with the
      imported volume law Vol(I(p,q)) = c_d d(p,q)^d this is the structural fact
      behind R2.

Supplied geometry; no metric, continuum, curvature or gravity claim.
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


def causality(points):
    n = len(points)
    prec = [[False] * n for _ in range(n)]
    for i in range(n):
        pi = points[i]
        for j in range(n):
            if i == j:
                continue
            dt = points[j][0] - pi[0]
            spatial = sum((points[j][k] - pi[k]) ** 2 for k in range(1, len(pi)))
            if dt > 0 and spatial < dt * dt:
                prec[i][j] = True
    return prec


def chain_matrix(prec, order):
    """Longest-chain length L(i,j) (in links); 0 when not causally related."""
    n = len(prec)
    chain = [[0] * n for _ in range(n)]
    for src in order:
        dist = [-1] * n
        dist[src] = 0
        for j in order:
            best = -1
            for i in range(n):
                if prec[i][j] and dist[i] >= 0 and dist[i] + 1 > best:
                    best = dist[i] + 1
            if best > dist[j]:
                dist[j] = best
        chain[src] = [value if value > 0 else 0 for value in dist]
    return chain


def interval_counts(prec, order):
    """m_ij = #{k : i ≺ k ≺ j}, the points strictly between i and j."""
    n = len(prec)
    desc = [set() for _ in range(n)]
    for src in reversed(order):
        acc = set()
        for k in range(n):
            if prec[src][k]:
                acc.add(k)
                acc |= desc[k]
        desc[src] = acc
    anc = [set() for _ in range(n)]
    for src in order:
        acc = set()
        for k in range(n):
            if prec[k][src]:
                acc.add(k)
                acc |= anc[k]
        anc[src] = acc
    return [[len(desc[i] & anc[j]) if prec[i][j] else 0 for j in range(n)] for i in range(n)]


def chain_estimator(prec, order, ell=1.0):
    L = chain_matrix(prec, order)
    return [[L[i][j] * ell for j in range(len(prec))] for i in range(len(prec))]


def count_offset(prec, counts, ell=1.0):
    """QR-05DA count form: ell*sqrt(1 + m_ij)."""
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j] + 1) if prec[i][j] else 0.0
             for j in range(n)] for i in range(n)]


def count_raw(prec, counts, ell=1.0):
    """Offset-free count form: ell*sqrt(m_ij); zero on links (m = 0)."""
    n = len(prec)
    return [[ell * math.sqrt(counts[i][j]) if prec[i][j] and counts[i][j] > 0 else 0.0
             for j in range(n)] for i in range(n)]


def support_census(D, prec, tol):
    """A1: positive exactly on the causal relation; count causal pairs at zero."""
    n = len(prec)
    mismatches = 0
    causal_pairs = 0
    zero_on_causal = 0
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            positive = D[i][j] > tol
            if positive != bool(prec[i][j]):
                mismatches += 1
            if prec[i][j]:
                causal_pairs += 1
                if not positive:
                    zero_on_causal += 1
    return {"support_mismatches": mismatches, "causal_pairs": causal_pairs,
            "zero_on_causal": zero_on_causal}


def reverse_triangle_census(D, prec, tol):
    """A2 over all triples i ≺ j ≺ k; witness is the first of the minimal gap."""
    n = len(prec)
    violations = 0
    triples = 0
    worst = float("inf")
    witness = None
    for i in range(n):
        for j in range(n):
            if not prec[i][j]:
                continue
            for k in range(n):
                if not prec[j][k]:
                    continue
                triples += 1
                gap = D[i][k] - D[i][j] - D[j][k]
                if gap < worst:
                    worst = gap
                    witness = [i, j, k]
                if gap < -tol:
                    violations += 1
    if worst == float("inf"):
        worst = 0.0
        witness = None
    elif worst >= -tol:
        witness = None
    return {"reverse_triangle_violations": violations, "triples": triples,
            "worst_gap": _round(worst), "witness": witness}


def pure_chain(n):
    prec = [[j > i for j in range(n)] for i in range(n)]
    return {"name": f"pure_chain_n{n}", "kind": "chain", "n": n,
            "prec": prec, "order": list(range(n))}


def antichain(n):
    prec = [[False] * n for _ in range(n)]
    return {"name": f"antichain_n{n}", "kind": "antichain", "n": n,
            "prec": prec, "order": list(range(n))}


def random_poset(n, p, seed):
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


def sprinkle_object(module, dim, n, seed):
    points = module.sprinkle_diamond(dim, n, seed=seed)
    order = sorted(range(n), key=lambda i: points[i][0])
    return {"name": f"sprinkle_d{dim}_n{n}", "kind": "sprinkle", "n": n, "dim": dim,
            "prec": causality(points), "order": order, "points": points}


def objects(module, protocol):
    out = []
    for dim in protocol["sprinkle_dims"]:
        for n in protocol["sprinkle_n"]:
            out.append(sprinkle_object(module, dim, n, protocol["seed"] + 100 * dim + n))
    out.append(pure_chain(protocol["chain_len"]))
    out.append(random_poset(protocol["poset_n"], protocol["poset_edge_prob"],
                            protocol["poset_seed"]))
    out.append(antichain(protocol["antichain_len"]))
    return out


def estimators(obj):
    prec, order = obj["prec"], obj["order"]
    counts = interval_counts(prec, order)
    return {
        "chain": chain_estimator(prec, order),
        "count_offset": count_offset(prec, counts),
        "count_raw": count_raw(prec, counts),
    }, counts


def three_chain_witness():
    """a ≺ b ≺ c with consecutive links: m_ab = m_bc = 0, m_ac = 1, tau_ac = 2."""
    points = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]
    prec = causality(points)
    order = [0, 1, 2]
    counts = interval_counts(prec, order)
    offset = count_offset(prec, counts)
    raw = count_raw(prec, counts)
    chain = chain_estimator(prec, order)
    tau_ac = 2.0  # directed Lorentzian distance: sqrt(2^2 - 0)
    return {
        "counts": {"m_ab": counts[0][1], "m_bc": counts[1][2], "m_ac": counts[0][2]},
        "count_offset": {"d_ab": offset[0][1], "d_bc": offset[1][2], "d_ac": offset[0][2],
                         "reverse_triangle_holds": bool(offset[0][2] >= offset[0][1] + offset[1][2])},
        "count_raw": {"d_ab": raw[0][1], "d_bc": raw[1][2], "d_ac": raw[0][2],
                      "reverse_triangle_holds": bool(raw[0][2] >= raw[0][1] + raw[1][2])},
        "chain": {"L_ab": chain[0][1], "L_bc": chain[1][2], "L_ac": chain[0][2],
                  "reverse_triangle_holds": bool(chain[0][2] >= chain[0][1] + chain[1][2])},
        "tau": {"tau_ac": tau_ac, "reverse_triangle_holds": bool(tau_ac >= 1.0 + 1.0)},
    }


def link_triple_bound():
    """Guaranteed A2 violation on a link triple in the offset count form.

    For a≺b≺c links, m_ab=m_bc=0, so d_ab=d_bc=ell and the reverse-triangle gap is
    ell*(sqrt(1+m_ac) - 2).  A violation needs m_ac < 3; the smallest nonempty
    interval (m_ac = 1) gives the constructive lower bound ell*(sqrt(2) - 2).
    """
    ell = 1.0
    gaps = {m: _round(ell * (math.sqrt(1 + m) - 2.0)) for m in (1, 2, 3)}
    return {"gap_by_m_ac": {str(m): g for m, g in gaps.items()},
            "violating_for_m_ac_lt_3": True,
            "worst_lower_bound_on_unit_ell": _round(math.sqrt(2.0) - 2.0)}


def structural_lemma(module, protocol):
    """Verify m_ac >= m_ab + m_bc + 1 for every a ≺ b ≺ c (R4)."""
    checked = 0
    violations = 0
    total_triples = 0
    for obj in objects(module, protocol):
        prec = obj["prec"]
        counts = interval_counts(prec, obj["order"])
        n = obj["n"]
        for i in range(n):
            for j in range(n):
                if not prec[i][j]:
                    continue
                for k in range(n):
                    if not prec[j][k]:
                        continue
                    total_triples += 1
                    if counts[i][k] < counts[i][j] + counts[j][k] + 1:
                        violations += 1
        checked += 1
    return {"objects_checked": checked, "triples": total_triples, "violations": violations}


def build_report(protocol):
    module = load_module("_qr05db_t7", MODULE_PATH)
    tol = protocol["tol"]
    objs = objects(module, protocol)

    rows = []
    for obj in objs:
        est, _counts = estimators(obj)
        for name in ("chain", "count_offset", "count_raw"):
            D = est[name]
            support = support_census(D, obj["prec"], tol)
            reverse = reverse_triangle_census(D, obj["prec"], tol)
            rows.append({
                "estimator": name, "object": obj["name"], "kind": obj["kind"], "n": obj["n"],
                "support_mismatches": support["support_mismatches"],
                "causal_pairs": support["causal_pairs"],
                "zero_on_causal": support["zero_on_causal"],
                "reverse_triangle_violations": reverse["reverse_triangle_violations"],
                "triples": reverse["triples"],
                "worst_gap": reverse["worst_gap"],
                "witness": reverse["witness"],
            })

    def rows_for(estimator):
        return [r for r in rows if r["estimator"] == estimator]

    chain_rows = rows_for("chain")
    offset_rows = rows_for("count_offset")
    raw_rows = rows_for("count_raw")

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
        "structural_superadditivity_holds": bool(
            structural_lemma(module, protocol)["violations"] == 0),
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
        "three_chain": three_chain_witness(),
        "link_triple_bound": link_triple_bound(),
        "structural_lemma": structural_lemma(module, protocol),
        "axiom_checks": rows,
        "flags": flags,
        "verdict": (
            "QR-05DB: the metric-axiom obstruction for count-only reconstructions. "
            "The order-only longest-chain estimator d = ell*L satisfies the Lorentzian "
            "distance axioms A0-A2 on every finite causal set tested (support exact, zero "
            "reverse-triangle violations), a Lorentzian premetric. The QR-05DA count "
            "estimator d = ell*sqrt(1+m) is positive exactly on the causal relation but "
            f"violates the reverse-triangle inequality A2 on the sprinklings and controls "
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
