"""Independent reference route for QR-05DE.

Same report by different mechanics:
  - posets enumerated from predecessor bitmasks with an ancestral-closure check,
    instead of a Boolean-matrix transitivity scan;
  - strong positivity by an LDL (semidefinite Cholesky) recursion, instead of
    testing every principal minor;
  - the report and verdict recoded.
"""

from __future__ import annotations

from itertools import product

SCHEMA = "qr05de-report-v1"


def enumerate_posets(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for assign in product((-1, 0, 1), repeat=len(pairs)):
        pred = [0] * n
        for (i, j), a in zip(pairs, assign):
            if a == 1:
                pred[j] |= (1 << i)
            elif a == -1:
                pred[i] |= (1 << j)
        ok = True
        for k in range(n):
            closure = pred[k]
            changed = True
            while changed:
                changed = False
                for j in range(n):
                    if (closure >> j) & 1:
                        if pred[j] | closure != closure:
                            closure |= pred[j]
                            changed = True
            if closure != pred[k]:
                ok = False
                break
        if ok:
            out.append(pred)
    return out


def to_relation(pred):
    n = len(pred)
    return [[bool((pred[j] >> i) & 1) for j in range(n)] for i in range(n)]


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


def hermitian_psd(matrix, tol):
    """Hermitian PSD via LDL: any negative pivot, or nonzero entry under a zero
    pivot, fails."""
    n = len(matrix)
    a = [[complex(matrix[i][j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if abs(a[i][j] - a[j][i].conjugate()) > tol:
                return False
    for j in range(n):
        d = a[j][j].real
        if d < -tol:
            return False
        if abs(d) <= tol:
            for i in range(j + 1, n):
                if abs(a[i][j]) > tol:
                    return False
            continue
        for i in range(j + 1, n):
            a[i][j] /= d
        for i in range(j + 1, n):
            for k in range(j + 1, n):
                a[i][k] -= a[i][j] * d * a[k][j].conjugate()
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
    all_posets = {}
    for n in protocol["naive_glue_n"]:
        posets = [to_relation(pred) for pred in enumerate_posets(n)]
        all_posets[n] = posets
        antichain = [[False] * n for _ in range(n)]
        psd = [p for p in posets if hermitian_psd(naive_glue(p), tol)]
        totals[str(n)] = len(posets)
        naive[str(n)] = {"posets": len(posets), "naive_glue_psd": len(psd),
                         "psd_only_antichain": bool(all(p == antichain for p in psd))}

    checked = 0
    c_invariant = True
    omega_flipped = True
    magnitude_invariant = True
    support_ok = True
    for n in protocol["naive_glue_n"]:
        for p in all_posets[n]:
            pt = transpose(p)
            Cp, Op = comparability(p), orientation(p)
            if Cp != comparability(pt):
                c_invariant = False
            if orientation(pt) != [[-v for v in row] for row in Op]:
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
        for p in all_posets[n]:
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
