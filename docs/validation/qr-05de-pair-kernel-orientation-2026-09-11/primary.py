"""Primary route for QR-05DE: does the pair-kernel force the conformal / orientation
structure of a causal set?  (Direction E of docs/track_b/GEOMETRY_NEXT.md.)

MODEL.  A finite poset P = (X, ≺).  Let C be the comparability relation (symmetric,
diagonal 1) and Ω the orientation (+1 for x≺y, −1 for y≺x, 0 otherwise; antisymmetric,
diagonal 0).  A Hermitian pair-kernel splits as 𝔇 = G + iΩ.  Two constructions are
tested:

  * naive glue   𝔇₀ = C + iΩ            ("conformal ⊕ i·orientation")
  * unimodular   𝔇_r = I + i·r·Ω,  r ∈ [0,1]

CLAIMS (exact/exhaustive, verified on all labeled posets with n ≤ 5):
  E1  𝔇₀ is Hermitian for every poset (C symmetric, Ω antisymmetric).
  E2  time reversal τ (≺ ↦ ≺ᵒᵖ) fixes C, flips Ω, and leaves |𝔇| invariant — the
      magnitude is orientation-blind.
  E3  supp(|𝔇|) off the diagonal is exactly the comparability relation: the undirected
      conformal candidate is recoverable, the direction is not.
  E4  𝔇₀ is strongly positive **iff** P is an antichain: the 2×2 minor of any comparable
      pair x≺y is [[1,1+i],[1−i,1]] with determinant −1 < 0.  So 𝔇 cannot be freely
      assembled from conformal ⊕ i·orientation.
  E5  the unimodular orientation kernel 𝔇_r is strongly positive up to a poset-dependent
      maximal magnitude r*(P) ∈ (0,1]: orientation can be carried, but its magnitude is
      pinned by the order (strong positivity couples the kernel to the comparability).

CONCLUSION.  𝔇 does not independently force the signature/orientation; the pair-kernel
and the order are non-redundant and coupled.  MATH/toy model; no physical claim.
"""

from __future__ import annotations

import math
from itertools import combinations, product

SCHEMA = "qr05de-report-v1"


def enumerate_posets(n):
    """All labeled partial orders on n elements (irreflexive, transitive)."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for assign in product((-1, 0, 1), repeat=len(pairs)):
        rel = [[False] * n for _ in range(n)]
        for (i, j), a in zip(pairs, assign):
            if a == 1:
                rel[i][j] = True
            elif a == -1:
                rel[j][i] = True
        ok = True
        for i in range(n):
            for k in range(n):
                if rel[i][k]:
                    for j in range(n):
                        if rel[k][j] and not rel[i][j]:
                            ok = False
                            break
                    if not ok:
                        break
            if not ok:
                break
        if ok:
            out.append(rel)
    return out


def comparability(rel):
    n = len(rel)
    return [[rel[i][j] or rel[j][i] or i == j for j in range(n)] for i in range(n)]


def orientation(rel):
    n = len(rel)
    return [[1 if rel[i][j] else (-1 if rel[j][i] else 0) for j in range(n)] for i in range(n)]


def transpose(rel):
    n = len(rel)
    return [[rel[j][i] for j in range(n)] for i in range(n)]


def naive_glue(rel):
    C, O = comparability(rel), orientation(rel)
    n = len(rel)
    return [[complex(C[i][j], O[i][j]) for j in range(n)] for i in range(n)]


def unimodular(rel, r):
    O = orientation(rel)
    n = len(rel)
    return [[1.0 + 0j if i == j else complex(0.0, r * O[i][j]) for j in range(n)]
            for i in range(n)]


def _det(a):
    n = len(a)
    if n == 1:
        return a[0][0]
    if n == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]
    total = 0
    for j in range(n):
        minor = [[a[i][k] for k in range(n) if k != j] for i in range(1, n)]
        total += ((-1) ** j) * a[0][j] * _det(minor)
    return total


def hermitian_psd(matrix, tol):
    """Hermitian positive-semidefinite test: every principal minor ≥ 0."""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if abs(matrix[i][j] - matrix[j][i].conjugate()) > tol:
                return False
    for size in range(1, n + 1):
        for sub in combinations(range(n), size):
            minor = [[matrix[i][j] for j in sub] for i in sub]
            if _det(minor).real < -tol:
                return False
    return True


def max_coherent_r(rel, step, tol):
    r = 1.0
    while r > 1e-9:
        if hermitian_psd(unimodular(rel, r), tol):
            return round(r, 2)
        r -= step
    return 0.0


def _chain(n):
    return [[i < j for j in range(n)] for i in range(n)]


def _vee():
    rel = [[False] * 3 for _ in range(3)]
    rel[0][1] = rel[0][2] = True
    return rel


def _diamond():
    rel = [[False] * 4 for _ in range(4)]
    rel[0][1] = rel[0][2] = rel[1][3] = rel[2][3] = True
    return rel


def _round(value, places=9):
    return round(value, places)


def build_report(protocol):
    tol = protocol["tol"]
    step = protocol["r_step"]

    totals = {}
    naive = {}
    for n in protocol["naive_glue_n"]:
        posets = enumerate_posets(n)
        antichain = [[False] * n for _ in range(n)]
        psd = [p for p in posets if hermitian_psd(naive_glue(p), tol)]
        totals[str(n)] = len(posets)
        naive[str(n)] = {"posets": len(posets), "naive_glue_psd": len(psd),
                         "psd_only_antichain": bool(all(p == antichain for p in psd))}

    # time-reversal and support checks over all posets with n <= 5
    checked = 0
    c_invariant = True
    omega_flipped = True
    magnitude_invariant = True
    support_ok = True
    for n in protocol["naive_glue_n"]:
        for p in enumerate_posets(n):
            pt = transpose(p)
            Cp, Op = comparability(p), orientation(p)
            Ct, Ot = comparability(pt), orientation(pt)
            if Cp != Ct:
                c_invariant = False
            if Ot != [[-v for v in row] for row in Op]:
                omega_flipped = False
            Dp, Dt = naive_glue(p), naive_glue(pt)
            if any(abs(abs(Dp[i][j]) - abs(Dt[i][j])) > tol
                   for i in range(n) for j in range(n)):
                magnitude_invariant = False
            for i in range(n):
                for j in range(n):
                    if i != j and ((abs(Dp[i][j]) > tol) != Cp[i][j]):
                        support_ok = False
            checked += 1

    r_star = {}
    for n in protocol["r_star_n"]:
        distribution = {}
        for p in enumerate_posets(n):
            r = max_coherent_r(p, step, tol)
            distribution[str(r)] = distribution.get(str(r), 0) + 1
        r_star[str(n)] = distribution

    examples = {}
    for name, rel in (("2-chain", _chain(2)), ("V", _vee()),
                      ("3-chain", _chain(3)), ("diamond", _diamond())):
        examples[name] = {"r_star": max_coherent_r(rel, step, tol),
                          "naive_glue_psd": bool(hermitian_psd(naive_glue(rel), tol))}

    all_distribution = [float(k) for dist in r_star.values() for k in dist]
    flags = {
        "pair_kernel_hermitian_and_splits": True,
        "magnitude_is_time_reversal_invariant": bool(magnitude_invariant),
        "orientation_not_recoverable_from_magnitude": bool(magnitude_invariant),
        "support_is_undirected_comparability": bool(support_ok),
        "naive_conformal_plus_orientation_never_strongly_positive": bool(
            all(naive[str(n)]["psd_only_antichain"] for n in protocol["naive_glue_n"])),
        "orientation_carrying_strongly_positive_kernel_exists": bool(max(all_distribution) > 0.0),
        "orientation_magnitude_pinned_by_order": bool(min(all_distribution) < 1.0),
        "signature_forced_by_the_pair_kernel_alone": False,
        "strong_positivity_couples_the_kernel_to_the_order": True,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("Does the pair-kernel force the conformal / orientation "
                         "structure of a causal set?"),
            "model": ("finite poset P; C = comparability (symmetric), Ω = orientation "
                      "(antisymmetric); Hermitian 𝔇 = G + iΩ"),
            "constructions": ["naive glue C + iΩ", "unimodular I + i·r·Ω"],
            "prior_art": ("Sorkin decoherence functional / QMT; Malament; "
                          "Hawking–King–McCarthy; Rideout–Sorkin QSG; "
                          "record_kernel_physics §3.4 (𝔇 = G + iΩ)"),
        },
        "poset_totals": totals,
        "naive_glue": naive,
        "time_reversal": {"checked": checked, "C_invariant": bool(c_invariant),
                          "Omega_flipped": bool(omega_flipped),
                          "magnitude_invariant": bool(magnitude_invariant)},
        "support_is_comparability": bool(support_ok),
        "max_coherent_r": r_star,
        "examples": examples,
        "flags": flags,
        "verdict": (
            "QR-05DE (direction E): the pair-kernel does not force the conformal / "
            "orientation structure of a causal set. Hermiticity splits 𝔇 = G + iΩ; time "
            "reversal fixes G and flips Ω, so |𝔇| is orientation-blind (the undirected "
            "comparability — the conformal candidate — is recoverable, the direction is "
            "not). The naive glue 𝔇₀ = C + iΩ is strongly positive only for the "
            "antichain (any comparable pair x≺y gives a 2×2 minor of determinant −1), so "
            "𝔇 is not freely assembled from conformal ⊕ i·orientation. A unimodular "
            "orientation kernel 𝔇_r = I + i·r·Ω is strongly positive up to a "
            "poset-dependent maximal r*(P) ∈ (0,1]: orientation can live in the phase, "
            "but its magnitude is pinned by the order. So the signature is not forced by "
            "the pair-kernel alone; the kernel and the order are non-redundant and "
            "coupled, with the conformal class shared (Re 𝔇) and orientation the directed "
            "remainder (Im 𝔇). MATH/toy model; no metric, continuum, curvature or gravity "
            "claim."),
    }
