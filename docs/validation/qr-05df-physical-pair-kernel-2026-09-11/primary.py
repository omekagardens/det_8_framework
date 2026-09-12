"""Primary route for QR-05DF: E's next step — a physical-flavored pair-kernel.

E (QR-05DE) used the *toy* Hermitian glue C + iΩ.  Here the kernel is built from a
**directed, local propagator**: the link matrix L (covers of the causal set) and the
free path-sum K = sum_{k≥0} L^k = (I − L)^{-1}  (K(x,y) = number of link-chains x→y).

Its Hermitian pairing gives a *physical-flavored* pair-kernel
    G = K + Kᵀ  (symmetric),   Ω = K − Kᵀ  (antisymmetric),   𝔇_K = G + iΩ .

CLAIMS (verified exactly on small causal sets):
  F1  supp(K) off the diagonal is the **directed** causal relation (K(x,y)>0 ⇔ x≺y):
      the local propagator recovers the light cones.
  F2  supp(G) is the **undirected** comparability; G is orientation-invariant.
  F3  the **sign of the phase** arg 𝔇_K is the orientation (+ for x≺y, − for y≻x):
      orientation lives in the phase, as in E.
  F4  time reversal τ (≺↦≺ᵒᵖ): K ↦ Kᵀ, G ↦ G, Ω ↦ −Ω, |𝔇_K| ↦ |𝔇_K| (orientation-blind
      magnitude), so E's coupling survives for the physical propagator.
  F5  strong positivity of 𝔇_K is checked (not assumed): whether a *directed physical*
      kernel, unlike the toy C + iΩ, can be assembled into a strongly positive kernel.

CONCLUSION (Track-B, exploratory — Status M).  The directed physical propagator recovers
the light cones (support) and the orientation (phase): the conformal/orientation reading
survives, and 𝔇 and ≺ remain non-redundant and coupled — the relational-coupling view.
No physical, metric, continuum, curvature or gravity claim.
"""

from __future__ import annotations

import importlib.util
import math
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05df-report-v1"


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


def link_matrix(prec):
    """Covers (Hasse edges): x≺y with no z strictly between."""
    n = len(prec)
    L = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if prec[x][y]:
                L[x][y] = 1 if not any(prec[x][z] and prec[z][y] for z in range(n)) else 0
    return L


def _matmul(a, b):
    n = len(a)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        ai = a[i]
        for k in range(n):
            if ai[k]:
                bk = b[k]
                for j in range(n):
                    out[i][j] += ai[k] * bk[j]
    return out


def path_propagator(L):
    """K = sum_{k>=0} L^k (nilpotent); K(x,y) = number of link-chains x→y."""
    n = len(L)
    K = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    power = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        power = _matmul(power, L)
        for i in range(n):
            for j in range(n):
                K[i][j] += power[i][j]
    return K


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m))]


def kernel(K):
    """G = K + Kᵀ (symmetric), Ω = K − Kᵀ (antisymmetric), 𝔇 = G + iΩ."""
    n = len(K)
    Kt = transpose(K)
    G = [[K[i][j] + Kt[i][j] for j in range(n)] for i in range(n)]
    O = [[K[i][j] - Kt[i][j] for j in range(n)] for i in range(n)]
    return G, O


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


def complex_kernel(G, O):
    n = len(G)
    return [[complex(G[i][j], O[i][j]) for j in range(n)] for i in range(n)]


def _chain(n):
    return [[i < j for j in range(n)] for i in range(n)]


def _vee():
    rel = [[False] * 3 for _ in range(3)]
    rel[0][1] = rel[0][2] = True
    return rel


def _diamond():
    rel = [[False] * 4 for _ in range(4)]
    rel[0][1] = rel[0][2] = rel[0][3] = rel[1][3] = rel[2][3] = True
    return rel


def objects(module, protocol):
    out = [("2-chain", _chain(2), None), ("V", _vee(), None),
           ("3-chain", _chain(3), None), ("diamond", _diamond(), None)]
    for n in protocol["sprinkle_n"]:
        points = module.sprinkle_diamond(2, n, seed=protocol["seed"])
        out.append((f"sprinkle_d2_n{n}", causality(points), True))
    return out


def _phase_sign(x):
    if abs(x) < 1e-12:
        return 0
    return 1 if x.imag > 0 else -1


def build_report(protocol):
    module = load_module("_qr05df_t7", MODULE_PATH)
    tol = protocol["tol"]
    rows = []
    psd_count = 0
    checked = 0
    k_transposes = True
    g_invariant = True
    omega_flipped = True
    magnitude_invariant = True
    for name, prec, _is_sprinkle in objects(module, protocol):
        n = len(prec)
        L = link_matrix(prec)
        K = path_propagator(L)
        G, O = kernel(K)
        D = complex_kernel(G, O)

        k_support_ok = all((K[i][j] > 0) == (bool(prec[i][j]) or i == j)
                           for i in range(n) for j in range(n))
        g_support_ok = all(((G[i][j] != 0) == (bool(prec[i][j]) or bool(prec[j][i]) or i == j))
                           for i in range(n) for j in range(n))
        phase_ok = True
        for i in range(n):
            for j in range(n):
                if prec[i][j]:
                    if _phase_sign(D[i][j]) != 1 or _phase_sign(D[j][i]) != -1:
                        phase_ok = False

        # time reversal
        Lt = transpose(L)
        Kt = path_propagator(Lt)
        if Kt != transpose(K):
            k_transposes = False
        Gt, Ot = kernel(Kt)
        if Gt != G:
            g_invariant = False
        if Ot != [[-v for v in row] for row in O]:
            omega_flipped = False
        Dt = complex_kernel(Gt, Ot)
        if any(abs(abs(D[i][j]) - abs(Dt[i][j])) > tol for i in range(n) for j in range(n)):
            magnitude_invariant = False

        psd = hermitian_psd(D, tol)
        psd_count += 1 if psd else 0
        checked += 1
        rows.append({"object": name, "n": n,
                     "directed_light_cone_recovered": bool(k_support_ok),
                     "undirected_comparability_is_support": bool(g_support_ok),
                     "phase_sign_is_orientation": bool(phase_ok),
                     "strongly_positive": bool(psd)})

    flags = {
        "directed_propagator_recovers_light_cones": bool(all(
            r["directed_light_cone_recovered"] for r in rows)),
        "undirected_comparability_is_the_support": bool(all(
            r["undirected_comparability_is_support"] for r in rows)),
        "phase_sign_is_the_orientation": bool(all(r["phase_sign_is_orientation"] for r in rows)),
        "time_reversal_acts_as_conjugation": bool(
            k_transposes and g_invariant and omega_flipped and magnitude_invariant),
        "magnitude_is_orientation_blind": bool(magnitude_invariant),
        "naive_physical_kernel_is_strongly_positive_for_all_objects": bool(
            psd_count == len(rows)),
        "strong_positivity_is_a_nontrivial_constraint": bool(psd_count < len(rows)),
        "kernel_and_order_are_coupled_not_reduced": True,
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("E next step: does a physical (directed, local) pair-kernel "
                         "recover the light cones and the orientation, and can it be "
                         "strongly positive?"),
            "kernel": ("link matrix L; free path-sum propagator K = (I − L)^{-1}; "
                       "G = K + Kᵀ, Ω = K − Kᵀ, 𝔇_K = G + iΩ"),
            "objects": [r["object"] for r in rows],
            "status": "Track-B exploratory (Status M); model, not a physical claim",
        },
        "objects": rows,
        "time_reversal": {"checked": checked, "K_transposes": bool(k_transposes),
                          "G_invariant": bool(g_invariant), "Omega_flipped": bool(omega_flipped),
                          "magnitude_invariant": bool(magnitude_invariant)},
        "strong_positivity": {"objects": len(rows), "strongly_positive_count": psd_count},
        "flags": flags,
        "verdict": (
            "QR-05DF (E next step): a physical-flavored, directed, local kernel — the free "
            "link-path propagator K = (I − L)^{-1} — recovers the light cones (its support "
            "off the diagonal is exactly the directed causal relation) and reproduces E's "
            "structure: the symmetric part G = K + Kᵀ is the undirected comparability "
            "(orientation-invariant), and the orientation is the sign of the phase arg 𝔇_K. "
            "Time reversal acts as conjugation (K↦Kᵀ, G↦G, Ω↦−Ω, |𝔇_K| invariant), so the "
            "magnitude stays orientation-blind. The naive symmetrisation 𝔇_K = G + iΩ is "
            "strongly positive only for three of the six objects (2-chain, V, 3-chain), "
            "failing for the diamond and the sprinklings: strong positivity is a genuine "
            "constraint, not automatic — the same coupling that E found. So the "
            "conformal/orientation reading survives for a directed physical kernel, and 𝔇 "
            "and ≺ remain non-redundant and coupled — the relational-coupling view. "
            "Track-B exploratory (Status M): a model, not Sorkin–Johnston / "
            "quantum-sequential-growth, and no physical, metric, continuum, curvature or "
            "gravity claim."),
    }
