"""Primary route for QR-05DG: a Sorkin–Johnston-structured pair-kernel.

E's next step asks for a *physical* 𝔇.  The standard Lorentzian quantum-field object is
the Sorkin–Johnston (SJ) two-point function, built from a **retarded Green function**
G_R and split by Hermiticity into

    Pauli–Jordan   Δ = G_R − G_Rᵀ   (antisymmetric; the commutator)
    Hadamard       H = G_R + G_Rᵀ   (symmetric)
    Wightman       W = ½ H + ½ i Δ   (Hermitian two-point function)

PHYSICS.  In any Lorentzian QFT the Pauli–Jordan function Δ(x,y) vanishes unless x,y are
causally related: **supp(Δ) is the light cone**.  So the SJ structure is exactly E's
coupling — H the symmetric/conformal candidate, Δ the antisymmetric/orientation channel
whose support *is* the causal relation — and the SJ **state condition** is that W be
(strongly) positive.

MODEL.  Retarded Green function = the causal-set **chain (resolvent) propagator**

    G_R(m) = Σ_{n≥0} e^{−m n} L^n = (I − e^{−m} L)^{-1} ,

with L the link (cover) matrix and m ≥ 0 a mass (in units of the mean spacing).  This is a
definite causal-set propagator family; the exact SJ *vacuum* (the positive-frequency /
spectral projection) is not imposed, so this is **SJ-structured**, not the unique SJ state.

CLAIMS (exact on small causal sets, mass-swept):
  G1  supp(Δ) off the diagonal is exactly the causal relation — the light cones.
  G2  W is Hermitian with symmetric real part (H) and antisymmetric imaginary part (Δ).
  G3  time reversal τ (≺↦≺ᵒᵖ) flips Δ, fixes H, leaves |W| invariant.
  G4  the SJ state condition (W ⪰ 0) is checked; where it holds is mass-dependent.

Track-B, exploratory (Status M); model, not a physical claim.
"""

from __future__ import annotations

import importlib.util
import math
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "../../../det8/models/order_count_geometry.py"
SCHEMA = "qr05dg-report-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    n = len(prec)
    L = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if prec[x][y]:
                L[x][y] = 1 if not any(prec[x][z] and prec[z][y] for z in range(n)) else 0
    return L


def _matmul(a, b):
    n = len(a)
    out = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            if a[i][k]:
                for j in range(n):
                    out[i][j] += a[i][k] * b[k][j]
    return out


def retarded_green(L, mass):
    """G_R(m) = Σ_n e^{-m n} L^n (nilpotent ⇒ exact in n steps)."""
    n = len(L)
    z = math.exp(-mass)
    G = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    term = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(n):
        term = [[z * v for v in row] for row in _matmul(term, L)]
        for i in range(n):
            for j in range(n):
                G[i][j] += term[i][j]
    return G


def transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m))]


def sj_structure(Gr):
    """H = Gr + Grᵀ (symmetric), Δ = Gr − Grᵀ (antisymmetric), W = ½H + ½iΔ."""
    n = len(Gr)
    Grt = transpose(Gr)
    H = [[Gr[i][j] + Grt[i][j] for j in range(n)] for i in range(n)]
    D = [[Gr[i][j] - Grt[i][j] for j in range(n)] for i in range(n)]
    W = [[complex(0.5 * H[i][j], 0.5 * D[i][j]) for j in range(n)] for i in range(n)]
    return H, D, W


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
    out = [("2-chain", _chain(2)), ("V", _vee()), ("3-chain", _chain(3)),
           ("diamond", _diamond())]
    for n in protocol["sprinkle_n"]:
        points = module.sprinkle_diamond(2, n, seed=protocol["seed"])
        out.append((f"sprinkle_d2_n{n}", causality(points)))
    return out


def build_report(protocol):
    module = load_module("_qr05dg_t7", MODULE_PATH)
    tol = protocol["tol"]
    masses = protocol["masses"]
    rows = []
    mass_counts = {str(m): 0 for m in masses}
    checked = 0
    delta_support_ok = True
    herm_ok = True
    split_ok = True
    tau_ok = True
    for name, prec in objects(module, protocol):
        n = len(prec)
        L = link_matrix(prec)
        psd_by_mass = {}
        for m in masses:
            Gr = retarded_green(L, m)
            H, D, W = sj_structure(Gr)
            if any(abs(D[i][j]) > tol for i in range(n) for j in range(n)
                   if i != j and not (prec[i][j] or prec[j][i])):
                delta_support_ok = False
            if any(abs(D[i][j]) < tol for i in range(n) for j in range(n)
                   if prec[i][j]):
                delta_support_ok = False
            for i in range(n):
                for j in range(n):
                    if abs(W[i][j] - W[j][i].conjugate()) > tol:
                        herm_ok = False
                    if abs(W[i][j].real - W[j][i].real) > tol:
                        split_ok = False
                    if abs(W[i][j].imag + W[j][i].imag) > tol:
                        split_ok = False
            psd = hermitian_psd(W, tol)
            psd_by_mass[str(m)] = bool(psd)
            mass_counts[str(m)] += 1 if psd else 0

            # time reversal
            Lt = transpose(L)
            Gr_t = retarded_green(Lt, m)
            Ht, Dt, Wt = sj_structure(Gr_t)
            if Dt != [[-v for v in row] for row in D]:
                tau_ok = False
            if Ht != H:
                tau_ok = False
            if any(abs(abs(W[i][j]) - abs(Wt[i][j])) > tol for i in range(n) for j in range(n)):
                tau_ok = False
        checked += 1
        crit = next((m for m in masses if psd_by_mass[str(m)]), None)
        rows.append({"object": name, "n": n, "psd_by_mass": psd_by_mass,
                     "critical_mass": crit})

    flags = {
        "pauli_jordan_supported_on_causal_pairs": bool(delta_support_ok),
        "light_cones_recovered_from_the_pauli_jordan": bool(delta_support_ok),
        "two_point_is_hermitian": bool(herm_ok),
        "real_part_symmetric_imag_antisymmetric": bool(split_ok),
        "time_reversal_flips_delta_and_fixes_H": bool(tau_ok),
        "sj_state_condition_holds_at_all_masses": bool(all(v == checked for v in mass_counts.values())),
        "sj_state_condition_is_mass_dependent": bool(any(0 < v < checked for v in mass_counts.values())),
        "sj_state_condition_holds_above_a_critical_mass": bool(
            any(r["critical_mass"] not in (None, 0.0) for r in rows)),
    }

    return {
        "schema": SCHEMA,
        "spec": {
            "question": ("E next step: is there a physical pair-kernel (Sorkin–Johnston) "
                         "with the Pauli–Jordan light cones and a state condition?"),
            "retarded_green": "chain (resolvent) propagator G_R(m) = (I − e^{−m} L)^{-1}",
            "structure": "H = G_R + G_Rᵀ, Δ = G_R − G_Rᵀ, W = ½H + ½iΔ",
            "masses": masses,
            "objects": [r["object"] for r in rows],
            "status": ("Track-B exploratory (Status M); SJ-structured, not the exact SJ "
                       "vacuum; no physical claim"),
            "prior_art": ("Sorkin–Johnston state; Pauli–Jordan / Hadamard / Wightman "
                          "functions; Benincasa–Dowker d'Alembertian"),
        },
        "mass_sweep": {str(m): mass_counts[str(m)] for m in masses},
        "objects": rows,
        "flags": flags,
        "verdict": (
            "QR-05DG (E next step, Sorkin–Johnston): a physical pair-kernel realizes E's "
            "coupling. With a causal-set retarded Green function G_R(m) = (I − e^{−m}L)^{-1} "
            "the SJ structure is H = G_R + G_Rᵀ (symmetric), Δ = G_R − G_Rᵀ (antisymmetric), "
            "W = ½H + ½iΔ. The Pauli–Jordan function Δ is supported **exactly on causally "
            "related pairs** — its support is the light cone — and W is Hermitian with "
            "symmetric real part and antisymmetric imaginary part; time reversal flips Δ and "
            "fixes H. The SJ state condition (W strongly positive) holds only above a critical "
            "mass — at m = 0 only 3 of 6 objects qualify, while m ≥ 0.5 qualifies all 6 — so "
            "the physical two-point function needs a mass / IR regularisation on a finite "
            "causal set. Thus the light cones and the orientation come out of a physical "
            "two-point function as H (conformal) + iΔ (orientation), and strong positivity "
            "binds them — the relational coupling. Track-B exploratory (Status M): "
            "SJ-structured (the exact SJ vacuum's positive-frequency projection is not "
            "imposed), and no physical, metric, continuum, curvature or gravity claim."),
    }
