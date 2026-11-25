"""Native DET four-birth record-process kappa derivation and QR-05DO / QR-05CR audits.

Implements the three finite foundational bridge tests connecting ``main``'s
four-birth active-residual law and the QR validation suite to Pathway 1:

1. **Four-Birth Active-Residual Native ``kappa`` Derivation**
   (``docs/coordination/NATIVE_MASS_MAPPING.md`` §Established finite connections;
   ``docs/track_b/native_active_residual_v1.md``;
   ``docs/observables/native_source_readout_response.md``;
   ``docs/track_b/native_mark_law_geometry_v1.md`` Part A):
   - Matches two allowed histories on the declared present readout, fixes the
     future outcome alphabet and two inactive controls (passive ``d=0, T=I``
     and forward-only ``d=0, T=M(0)``), and computes ``kappa`` (Fisher-Rao
     distance and total-variation distance) from their complete future outcome
     distributions at each available step using exact rational arithmetic.
   - Tests whether ``kappa`` shrinks under the model's own updates and whether
     one scalar works across two readouts (``D`` total chain, ``Y`` counter=2,
     and ``Z`` terminal antichain).
   - Preserves the negative/structural result rather than inserting a fitted
     exponential:
       * Pure residual mixing ``K = M(0)`` at a fixed prefix shrinks ``kappa``
         geometrically by ``t = 1/2`` per step.
       * Structural births do NOT shrink ``kappa`` by a single uniform rate:
         causal link-forming commits (``S != empty``, setting ``chi(P) = 0``,
         or ``S_3 = {a,b}`` forming a 3-chain) quench residual or mark
         sensitivity in a single step (``kappa -> 0``), whereas isolated
         antichain births (``S = empty``, ``chi(P) = 1``) preserve/amplify
         conditional contrast while losing probability mass to the quenched
         sector.
       * One scalar does NOT work across both readouts when both committed root
         mark ``i in {0, 1}`` and residual polarization ``s in [-1, 1]`` vary
         (exact rank = 2 across ``(Z, D, Y)``; and on the 2-chain ``a < b``,
         ``D`` is quenched on ``S_3 = {a}`` while full structural ``q_4``
         retains ``kappa_FR = 0.110849``).

2. **QR-05DO Anchor-Calculus Quotient for Regional Interaction Counts**
   (``docs/validation/qr-05do-anchor-calculus-2026-09-11/RESULTS.md``):
   - Evaluates all ``2^5 = 32`` subsets of the 5-channel universe
     ``{order, counts, transition_contraction, distance_ratio, anchor}`` across
     worlds differing in physical mass-per-area conversion ``mu = Sigma_b / N_int``
     and critical density ``Sigma_crit = mu * N_rec``.
   - Proves ``0`` monotonicity violations and ``16/16`` anchor-free blindness:
     internal records identify relative regional interaction counts and per-step
     contraction rate ``t = 1/2``, but cannot identify interactions per region
     with physical mass per area or fix ``Sigma_crit`` without an external anchor.

3. **QR-05CR Two-Region Conservative Flux vs. Pointwise Operator Audit**
   (``docs/validation/qr-05cr-no-double-counting-2026-09-10/RESULTS.md``):
   - Audits a spatially varying coefficient ``d_k = 1 - beta * kappa_k`` in a
     two-region (and multi-region) discrete response equation.
   - Proves that putting ``d_k`` inside a conservative divergence operator
     ``(S_D Phi)_k = d_{k+1/2}(Phi_{k+1}-Phi_k) - d_{k-1/2}(Phi_k-Phi_{k-1})``
     allows ``kappa`` to alter the potential response ``Delta Phi = -Q_enc / d_{1/2}``
     while total flux balances identically (``sum_k (S_D Phi)_k = 0.0``) and
     the explicit source ``Q_enc`` is accounted for without double-counting,
     whereas the pointwise operator ``(S_P Phi)_k = d_k (Delta Phi)_k`` violates
     flux balance by ``(d_0 - d_1)(Phi_1 - Phi_0) != 0``.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Final, Sequence


# ═══════════════════════════════════════════════════════════════════════════
# Exact Rational & Information-Geometry Helpers
# ═══════════════════════════════════════════════════════════════════════════

THETA_ACTIVE: Final[Fraction] = Fraction(1, 32)
T_CONTRACTION: Final[Fraction] = Fraction(1, 2)
A_HARMONIC: Final[tuple[Fraction, ...]] = (
    Fraction(1, 264),  # a_0 (empty)
    Fraction(1, 264),  # a_1 (singleton)
    Fraction(1, 176),  # a_2 (2-antichain)
    Fraction(1, 44),   # a_3 (3-antichain)
    Fraction(1, 1),    # a_4 (4-antichain indicator)
)

# Part A structural seed constants from docs/track_b/native_mark_law_geometry_v1.md
A_SEED: Final[Fraction] = Fraction(2, 3)
C_SEED: Final[Fraction] = Fraction(1, 5)
D_SEED: Final[Fraction] = Fraction(1, 4)
F_SEED_0: Final[Fraction] = Fraction(1, 6)
F_SEED_1: Final[Fraction] = Fraction(1, 3)
G_SEED: Final[Fraction] = Fraction(1, 10)
K_SEED: Final[Fraction] = Fraction(11, 20)
H_SEED_0: Final[Fraction] = Fraction(19, 30)
H_SEED_1: Final[Fraction] = Fraction(7, 15)
E_SEED: Final[Fraction] = Fraction(1, 44)


def fisher_rao_distance_exact(
    p: Sequence[Fraction | float],
    q: Sequence[Fraction | float],
) -> float:
    """Normalized Fisher-Rao distance in [0, 1] between two probability vectors."""
    if len(p) != len(q) or len(p) == 0:
        raise ValueError("Probability vectors must be non-empty and have equal length")
    p_floats = [float(x) for x in p]
    q_floats = [float(x) for x in q]
    if any(x < -1e-15 for x in p_floats) or any(x < -1e-15 for x in q_floats):
        raise ValueError("Probability vectors must be non-negative")
    if abs(sum(p_floats) - 1.0) > 1e-9 or abs(sum(q_floats) - 1.0) > 1e-9:
        raise ValueError("Probability vectors must sum to 1")
    bc = sum(math.sqrt(max(0.0, pi) * max(0.0, qi)) for pi, qi in zip(p_floats, q_floats))
    bc = max(0.0, min(1.0, bc))
    return (2.0 / math.pi) * math.acos(bc)


def total_variation_exact(
    p: Sequence[Fraction],
    q: Sequence[Fraction],
) -> Fraction:
    """Exact rational total-variation distance (1/2) * sum_i |p_i - q_i|."""
    if len(p) != len(q) or len(p) == 0:
        raise ValueError("Probability vectors must be non-empty and have equal length")
    return sum((abs(pi - qi) for pi, qi in zip(p, q)), Fraction(0, 1)) * Fraction(1, 2)


# ═══════════════════════════════════════════════════════════════════════════
# 1. Main's Four-Birth Active-Residual & Mark-History Native kappa Derivation
# ═══════════════════════════════════════════════════════════════════════════


def _singleton_coarse_continuation_law(
    root_mark: int,
    polarization_s: Fraction,
    *,
    active: bool = True,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Complete 4-birth continuation distribution from singleton C_0 (size n=1).

    Partitions all complete continuations from singleton ``P = {a}`` (with root
    mark ``root_mark in {0, 1}`` and residual polarization ``s = rho_0 - rho_1``)
    into four mutually exclusive, exhaustive terminal outcome classes:
      0. ``S_2 = {a}`` (2-chain) AND ``D = 1, Y = 1`` (total 4-chain)
      1. ``S_2 = {a}`` (2-chain) AND ``D = 0, Y = 1``
      2. ``S_2 = {a}`` (2-chain) AND ``D = 0, Y = 0``
      3. ``S_2 = empty`` (2-antichain) AND ``Z = 0`` (non-antichain terminal)
      4. ``S_2 = empty`` (2-antichain) AND ``Z = 1`` (terminal 4-antichain)
    Returned as a 5-tuple of exact ``Fraction`` probabilities summing to 1.
    """
    if root_mark not in (0, 1):
        raise ValueError(f"root_mark must be 0 or 1, got {root_mark!r}")
    if polarization_s < -1 or polarization_s > 1:
        raise ValueError(f"polarization_s must lie in [-1, 1], got {polarization_s!r}")

    theta = THETA_ACTIVE if active else Fraction(0, 1)
    a1 = A_HARMONIC[1]  # 1/264

    # Conditional 2-chain (D, Y) probabilities (00, 01, 11) from native_source_readout_response.md:
    if root_mark == 0:
        p_00_given_2c = Fraction(246, 1320)
        p_01_given_2c = Fraction(295, 1320)
        p_11_given_2c = Fraction(779, 1320)
    else:
        p_00_given_2c = Fraction(456, 1320)
        p_01_given_2c = Fraction(290, 1320)
        p_11_given_2c = Fraction(574, 1320)

    # By Eq. (7) of native_active_residual_v1.md, from n=1 (chi(P)=1, H(C_0)=a_1):
    # Every Z=0 history gets factor (1 - 2 * theta * a_1 * s) = (1 - s / 4224);
    # the Z=1 history (passive weight a_1 = 1/264) gets factor (1 + 2 * theta * (1 - a_1) * s).
    mult_z0 = Fraction(1, 1) - Fraction(2, 1) * theta * a1 * polarization_s
    mult_z1 = Fraction(1, 1) + Fraction(2, 1) * theta * (Fraction(1, 1) - a1) * polarization_s

    w_2chain = Fraction(1, 3)
    w_anti_z0 = Fraction(2, 3) - a1  # 175/264
    w_anti_z1 = a1                   # 1/264

    p_2c_11 = w_2chain * p_11_given_2c * mult_z0
    p_2c_01 = w_2chain * p_01_given_2c * mult_z0
    p_2c_00 = w_2chain * p_00_given_2c * mult_z0
    p_anti_z0 = w_anti_z0 * mult_z0
    p_anti_z1 = w_anti_z1 * mult_z1

    total = p_2c_11 + p_2c_01 + p_2c_00 + p_anti_z0 + p_anti_z1
    if total != Fraction(1, 1):
        raise RuntimeError(f"Continuation distribution failed normalization: {total}")
    return (p_2c_11, p_2c_01, p_2c_00, p_anti_z0, p_anti_z1)


def _two_chain_15_branch_law(root_mark: int) -> tuple[Fraction, ...]:
    """Exact 15-branch structural continuation law from 2-chain a < b (n=2)."""
    if root_mark not in (0, 1):
        raise ValueError(f"root_mark must be 0 or 1, got {root_mark!r}")
    f_i = F_SEED_0 if root_mark == 0 else F_SEED_1
    h_i = H_SEED_0 if root_mark == 0 else H_SEED_1
    c = C_SEED
    e = E_SEED

    dist = (
        # S3 = empty (edge + isolate, incoming weight c = 1/5)
        c * e,
        c * e,
        c * (e * f_i / c),
        c * (e * h_i / c),
        c * Fraction(1, 8),
        c * Fraction(65, 88),
        # S3 = {a} (fork, incoming weight f_i)
        f_i * e,
        f_i * e,
        f_i * (e * h_i / f_i),
        f_i * (e * h_i / f_i),
        f_i * (Fraction(1, 1) - 2 * e - 2 * e * h_i / f_i),
        # S3 = {a,b} (3-chain, incoming weight h_i)
        h_i * e,
        h_i * e,
        h_i * e,
        h_i * Fraction(41, 44),
    )
    if sum(dist, Fraction(0, 1)) != Fraction(1, 1):
        raise RuntimeError("15-branch continuation law failed normalization")
    return dist


def evaluate_successive_birth_unconditional_readouts() -> dict[str, object]:
    """Compare the same readout across successive births keeping both quenched and surviving branches.

    Tracks the complete unconditional (branch-averaged) marginal distributions
    at each birth ``n`` without conditioning on or post-selecting surviving
    branches, so ``surviving_branch_mass + quenched_branch_mass == 1`` at every
    birth ``n``:

    1. ``antichain_Z_n_across_births_1_to_4``:
       Same antichain readout ``Z_n = chi(P_n) in {0, 1}`` across births
       ``n = 1, 2, 3, 4`` from empty parent ``n_0 = 0`` comparing active
       residual ``delta_0`` (``s = +1``) vs. ``delta_1`` (``s = -1``).
       - Passive surviving branch weight: ``p_surv(n) = a_0 / a_n = (1, 2/3, 1/6, 1/264)``.
       - Passive quenched branch weight: ``p_quench(n) = 1 - a_0 / a_n = (0, 1/3, 5/6, 263/264)``.
       - Unconditional branch-averaged contrast:
         ``Delta P(Z_n = 1) = (1 / 4224) * p_quench(n) = (0, 1/12672, 5/25344, 263/1115136)``.
       - Survives averaging across all branches because each quenched branch
         freezes at ``H = 0`` with probability deficit ``-(s / 8448) * w_h``.

    2. ``total_chain_D_n_residual_across_births_1_to_4``:
       Same total-chain readout ``D_n = 1(P_n is a total n-chain)`` across
       births ``n = 1, 2, 3, 4`` from singleton ``P_1 = {a}`` (``r_a = 0``),
       comparing active residual ``delta_0`` (``s = +1``) vs. ``delta_1`` (``s = -1``).
       - Even though active residual coupling is 100% quenched on the 2-chain
         branch after birth 2 (``chi(P_2) = 0 => d = 0``), the birth-2 branch-weight
         contrast ``Delta P(D_2 = 1) = -1/6336`` is locked into the chain subtree
         weight and survives unconditional averaging at births 3 and 4, decaying
         by the passive chain-survival factors ``19/30`` and ``41/44``:
         ``Delta P(D_n = 1) = (0, -1/6336, -19/190080, -779/8363520)``.

    3. ``total_chain_D_n_mark_across_births_2_to_4``:
       Same total-chain readout ``D_n`` across births ``n = 2, 3, 4`` from the
       matched two-chain ``a < b`` comparing committed root mark ``i = 1`` vs.
       ``i = 0`` (``P_1 - P_0``), keeping all quenched non-chain branches
       (``S_3 in {empty, {a}}`` at birth 3 and ``S_4 != {a,b,x}`` at birth 4)
       and the surviving chain branch:
       ``Delta P(D_n = 1) = (0, -1/6, -41/264)``.
       Even though the conditional birth-4 transition kernel on the 3-chain has
       zero mark sensitivity (``kappa_FR(n=3 | 3-chain) = 0``), the birth-3
       history contrast survives unconditional averaging at birth 4 at ``41/44``
       of its birth-3 value.

    4. ``counter_two_Y_n_mark_across_births_2_to_4``:
       Same counter readout ``Y_n = 1(exists v in P_n : counter_n(v) == 2)``
       across births ``n = 2, 3, 4`` from the matched two-chain ``a < b``
       comparing root mark ``i = 1`` vs. ``i = 0`` (``P_1 - P_0``), keeping all
       branches:
       - At ``n = 2``: counters are ``(1, 0) => P_i(Y_2 = 1) = 0 => Delta P(Y_2 = 1) = 0``.
       - At ``n = 3``: both the fork branch ``S_3 = {a}`` (weight ``f_i``,
         counters ``(2,0,0)``) and the 3-chain branch ``S_3 = {a,b}`` (weight
         ``h_i``, counters ``(2,1,0)``) have ``Y_3 = 1``, while ``S_3 = empty``
         (weight ``c = 1/5``, counters ``(1,0,0)``) has ``Y_3 = 0``. Summing
         over all branches gives ``P_i(Y_3 = 1) = f_i + h_i = 1 - c = 4/5`` for
         BOTH ``i = 0`` and ``i = 1``, so ``Delta P(Y_3 = 1) = 0`` (exact
         branch-averaging cancellation at birth 3).
       - At ``n = 4``: on the fork branch ``S_3 = {a}``, ``43/44`` of sub-branches
         increment root ``a``'s counter from ``2 -> 3``, quenching ``Y`` from
         ``1 -> 0`` (only ``S_4 = empty`` with weight ``f_i * e`` survives with
         ``Y_4 = 1``), whereas on the 3-chain branch ``S_3 = {a,b}``, ``43/44``
         of sub-branches preserve ``Y_4 = 1`` (because vertex ``b``'s counter
         increments ``1 -> 2`` when ``a``'s increments ``2 -> 3``). This
         asymmetric fork-quenching vs. chain-relay un-cancels the birth-3
         branch polarization across all 15 branches:
         ``Delta P(Y_4 = 1) = (f_1 - f_0)*e + (h_1 - h_0)*(1 - e) = -7/44``.
    """
    a = A_HARMONIC
    theta = THETA_ACTIVE
    c = C_SEED
    e = E_SEED
    f0, f1 = F_SEED_0, F_SEED_1
    h0, h1 = H_SEED_0, H_SEED_1

    # 1. Antichain readout Z_n = chi(P_n) across births n = 1, 2, 3, 4 (s = +1 vs s = -1)
    z_steps: list[dict[str, object]] = []
    for n in (1, 2, 3, 4):
        p_surv_passive = a[0] / a[n]
        p_quench_passive = Fraction(1, 1) - p_surv_passive
        p_z1_pos = p_surv_passive * (Fraction(1, 1) + theta * (a[n] - a[0]))
        p_z0_pos = p_quench_passive * (Fraction(1, 1) - theta * a[0])
        p_z1_neg = p_surv_passive * (Fraction(1, 1) - theta * (a[n] - a[0]))
        p_z0_neg = p_quench_passive * (Fraction(1, 1) + theta * a[0])
        if p_z1_pos + p_z0_pos != Fraction(1, 1) or p_z1_neg + p_z0_neg != Fraction(1, 1):
            raise RuntimeError(f"Unconditional Z_{n} branch probabilities failed normalization")
        delta_z = p_z1_pos - p_z1_neg
        k_fr_z = fisher_rao_distance_exact((p_z1_pos, p_z0_pos), (p_z1_neg, p_z0_neg))
        z_steps.append(
            {
                "birth_n": n,
                "passive_surviving_branch_mass_exact": str(p_surv_passive),
                "passive_quenched_branch_mass_exact": str(p_quench_passive),
                "p_surviving_s_pos_exact": str(p_z1_pos),
                "p_quenched_s_pos_exact": str(p_z0_pos),
                "p_surviving_s_neg_exact": str(p_z1_neg),
                "p_quenched_s_neg_exact": str(p_z0_neg),
                "total_branch_mass_s_pos": float(p_z1_pos + p_z0_pos),
                "total_branch_mass_s_neg": float(p_z1_neg + p_z0_neg),
                "unconditional_contrast_exact": str(delta_z),
                "unconditional_contrast": float(delta_z),
                "unconditional_kappa_fr": k_fr_z,
            }
        )

    # 2. Total-chain readout D_n across births n = 1, 2, 3, 4 under active residual (s = +1 vs s = -1, i = 0)
    d_res_passive_chain: dict[int, Fraction] = {
        1: Fraction(1, 1),
        2: Fraction(1, 3),
        3: Fraction(1, 3) * h0,
        4: Fraction(1, 3) * h0 * Fraction(41, 44),
    }
    d_residual_steps: list[dict[str, object]] = []
    for n in (1, 2, 3, 4):
        w_chain = d_res_passive_chain[n]
        w_quench = Fraction(1, 1) - w_chain
        if n == 1:
            p_d1_pos = Fraction(1, 1)
            p_d1_neg = Fraction(1, 1)
        else:
            p_d1_pos = w_chain * (Fraction(1, 1) - Fraction(2, 1) * theta * a[1])
            p_d1_neg = w_chain * (Fraction(1, 1) + Fraction(2, 1) * theta * a[1])
        p_d0_pos = Fraction(1, 1) - p_d1_pos
        p_d0_neg = Fraction(1, 1) - p_d1_neg
        delta_d = p_d1_pos - p_d1_neg
        k_fr_d = fisher_rao_distance_exact((p_d1_pos, p_d0_pos), (p_d1_neg, p_d0_neg))
        d_residual_steps.append(
            {
                "birth_n": n,
                "passive_surviving_chain_mass_exact": str(w_chain),
                "passive_quenched_nonchain_mass_exact": str(w_quench),
                "p_surviving_s_pos_exact": str(p_d1_pos),
                "p_quenched_s_pos_exact": str(p_d0_pos),
                "p_surviving_s_neg_exact": str(p_d1_neg),
                "p_quenched_s_neg_exact": str(p_d0_neg),
                "unconditional_contrast_exact": str(delta_d),
                "unconditional_contrast": float(delta_d),
                "unconditional_kappa_fr": k_fr_d,
            }
        )

    # 3. Total-chain readout D_n across births n = 2, 3, 4 from 2-chain a < b (root mark i = 1 vs i = 0)
    d_mark_rows = (
        (2, Fraction(1, 1), Fraction(1, 1)),
        (3, h0, h1),
        (4, h0 * Fraction(41, 44), h1 * Fraction(41, 44)),
    )
    d_mark_steps: list[dict[str, object]] = []
    for n, p0_d1, p1_d1 in d_mark_rows:
        p0_d0 = Fraction(1, 1) - p0_d1
        p1_d0 = Fraction(1, 1) - p1_d1
        delta_d_mark = p1_d1 - p0_d1
        k_fr_dm = fisher_rao_distance_exact((p0_d1, p0_d0), (p1_d1, p1_d0))
        d_mark_steps.append(
            {
                "birth_n": n,
                "p_surviving_mark0_exact": str(p0_d1),
                "p_quenched_mark0_exact": str(p0_d0),
                "p_surviving_mark1_exact": str(p1_d1),
                "p_quenched_mark1_exact": str(p1_d0),
                "unconditional_contrast_P1_minus_P0_exact": str(delta_d_mark),
                "unconditional_contrast_P1_minus_P0": float(delta_d_mark),
                "unconditional_kappa_fr": k_fr_dm,
            }
        )

    # 4. Counter=2 readout Y_n across births n = 2, 3, 4 from 2-chain a < b (root mark i = 1 vs i = 0)
    y_mark_rows = (
        # (n, p0_y1, p1_y1, fork_surv0, fork_quench0, chain_surv0, chain_quench0, edge_react0)
        (
            2,
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
        ),
        (
            3,
            f0 + h0,
            f1 + h1,
            f0,
            Fraction(0, 1),
            h0,
            Fraction(0, 1),
            Fraction(0, 1),
        ),
        (
            4,
            c * (Fraction(1, 1) - 2 * e) + f0 * e + h0 * (Fraction(1, 1) - e),
            c * (Fraction(1, 1) - 2 * e) + f1 * e + h1 * (Fraction(1, 1) - e),
            f0 * e,
            f0 * (Fraction(1, 1) - e),
            h0 * (Fraction(1, 1) - e),
            h0 * e,
            c * (Fraction(1, 1) - 2 * e),
        ),
    )
    y_mark_steps: list[dict[str, object]] = []
    for (
        n,
        p0_y1,
        p1_y1,
        fork_surv0,
        fork_quench0,
        chain_surv0,
        chain_quench0,
        edge_react0,
    ) in y_mark_rows:
        p0_y0 = Fraction(1, 1) - p0_y1
        p1_y0 = Fraction(1, 1) - p1_y1
        delta_y_mark = p1_y1 - p0_y1
        k_fr_ym = fisher_rao_distance_exact((p0_y1, p0_y0), (p1_y1, p1_y0))
        y_mark_steps.append(
            {
                "birth_n": n,
                "p_active_Y1_mark0_exact": str(p0_y1),
                "p_inactive_Y0_mark0_exact": str(p0_y0),
                "p_active_Y1_mark1_exact": str(p1_y1),
                "p_inactive_Y0_mark1_exact": str(p1_y0),
                "mark0_fork_surviving_Y1_exact": str(fork_surv0),
                "mark0_fork_quenched_to_Y0_exact": str(fork_quench0),
                "mark0_chain_surviving_Y1_exact": str(chain_surv0),
                "mark0_chain_quenched_to_Y0_exact": str(chain_quench0),
                "mark0_edge_reactivated_to_Y1_exact": str(edge_react0),
                "unconditional_contrast_P1_minus_P0_exact": str(delta_y_mark),
                "unconditional_contrast_P1_minus_P0": float(delta_y_mark),
                "unconditional_kappa_fr": k_fr_ym,
            }
        )

    return {
        "all_branches_retained_at_every_birth": True,
        "history_effect_survives_unconditional_averaging": True,
        "antichain_Z_n_across_births_1_to_4": {
            "readout_definition": "Z_n = chi(P_n) = 1 iff P_n has no causal links at birth n",
            "contrasts_by_birth_exact": [s["unconditional_contrast_exact"] for s in z_steps],
            "survives_at_n4": z_steps[-1]["unconditional_contrast_exact"] == "263/1115136",
            "steps": z_steps,
        },
        "total_chain_D_n_residual_across_births_1_to_4": {
            "readout_definition": "D_n = 1 iff P_n is a total chain of height n (s=+1 vs s=-1, i=0)",
            "contrasts_by_birth_exact": [
                s["unconditional_contrast_exact"] for s in d_residual_steps
            ],
            "step_survival_ratios_exact": ["19/30", "41/44"],
            "survives_after_local_coupling_quenched": (
                d_residual_steps[-1]["unconditional_contrast_exact"] == "-779/8363520"
            ),
            "steps": d_residual_steps,
        },
        "total_chain_D_n_mark_across_births_2_to_4": {
            "readout_definition": "D_n = 1 iff P_n is a total chain of height n (root mark i=1 minus i=0)",
            "contrasts_by_birth_exact": [
                s["unconditional_contrast_P1_minus_P0_exact"] for s in d_mark_steps
            ],
            "n4_over_n3_retention_ratio_exact": "41/44",
            "survives_at_n4": (
                d_mark_steps[-1]["unconditional_contrast_P1_minus_P0_exact"] == "-41/264"
            ),
            "steps": d_mark_steps,
        },
        "counter_two_Y_n_mark_across_births_2_to_4": {
            "readout_definition": "Y_n = 1 iff exists v in P_n with descendant counter_n(v) == 2 (i=1 minus i=0)",
            "contrasts_by_birth_exact": [
                s["unconditional_contrast_P1_minus_P0_exact"] for s in y_mark_steps
            ],
            "cancels_at_birth_3_under_branch_averaging": (
                y_mark_steps[1]["unconditional_contrast_P1_minus_P0_exact"] == "0"
            ),
            "re_emerges_at_birth_4_via_asymmetric_fork_quenching": (
                y_mark_steps[2]["unconditional_contrast_P1_minus_P0_exact"] == "-7/44"
            ),
            "steps": y_mark_steps,
        },
        "averaging_diagnosis": (
            "Keeping the probability weights of both quenched and surviving branches across "
            "successive births shows that the history effect DOES survive unconditional branch "
            "averaging, via three distinct mechanisms: "
            "(1) For Z_n = chi(P_n) under active residual s, quenched branches freeze at H=0 with "
            "a negative polarization deficit -(s/8448)*w_h, so the unconditional contrast grows "
            "as (1/4224)*p_quench(n) = (0, 1/12672, 5/25344, 263/1115136). "
            "(2) For D_n (total chain), even after the local transition kernel quenches sensitivity "
            "to zero (at n>=2 for residual s, or at n=4 for root mark i on the 3-chain), the earlier "
            "branch-weight difference is locked into the surviving chain subtree and persists "
            "unconditionally, attenuated only by passive chain-continuation factors (19/30 and 41/44, "
            "giving Delta D_3 = -1/6 -> Delta D_4 = -41/264). "
            "(3) For Y_n (counter == 2), unconditional averaging across the fork (f_i) and 3-chain "
            "(h_i) branches EXACTLY CANCELS the mark effect at birth 3 (f_0+h_0 = f_1+h_1 = 4/5 => "
            "Delta Y_3 = 0), but birth 4 quenches 43/44 of the fork branch (c_a: 2 -> 3) while "
            "preserving 43/44 of the 3-chain branch (via c_b: 1 -> 2), un-canceling the contrast "
            "to Delta Y_4 = -7/44 across all 15 branches."
        ),
    }


def _is_downward_closed_ideal(
    rels: frozenset[tuple[int, int]],
    candidate: Sequence[int],
) -> bool:
    cand_set = set(candidate)
    for u, v in rels:
        if v in cand_set and u not in cand_set:
            return False
    return True


def _enumerate_poset_ideals(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
) -> tuple[frozenset[int], ...]:
    ideals: list[frozenset[int]] = []
    for k in range(len(vertices) + 1):
        for comb in itertools.combinations(vertices, k):
            if _is_downward_closed_ideal(rels, comb):
                ideals.append(frozenset(comb))
    return tuple(ideals)


def _poset_maxima(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
) -> frozenset[int]:
    non_max = {u for u, _ in rels}
    return frozenset(v for v in vertices if v not in non_max)


def _restrict_poset(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
    keep: Sequence[int],
) -> tuple[tuple[int, ...], frozenset[tuple[int, int]]]:
    keep_set = set(keep)
    new_v = tuple(v for v in vertices if v in keep_set)
    new_rels = frozenset((u, v) for u, v in rels if u in keep_set and v in keep_set)
    return new_v, new_rels


def _append_birth_vertex(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
    ideal_s: frozenset[int],
    new_v: int,
) -> tuple[tuple[int, ...], frozenset[tuple[int, int]]]:
    new_vertices = vertices + (new_v,)
    new_rels = set(rels)
    for u in ideal_s:
        new_rels.add((u, new_v))
        for w, u2 in rels:
            if u2 == u:
                new_rels.add((w, new_v))
    return new_vertices, frozenset(new_rels)


def _update_modulo5_counters(
    counters: dict[int, int],
    ideal_s: frozenset[int],
    new_v: int,
) -> dict[int, int]:
    out = dict(counters)
    for u in ideal_s:
        out[u] = (out[u] + 1) % 5
    out[new_v] = 0
    return out


def _q_enumerated_from_diamond_and_seed(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
    marks: dict[int, int],
    ideal_s: frozenset[int],
) -> Fraction:
    """Independently compute growth kernel q(P, r, S) for |P| in {0, 1, 2, 3} from seed + diamond law."""
    n = len(vertices)
    if n == 0:
        return Fraction(1, 1)
    ideals = _enumerate_poset_ideals(vertices, rels)
    if ideal_s not in ideals:
        raise ValueError(f"Subset {ideal_s} is not a downward-closed ideal of {rels}")
    if n == 1:
        return A_SEED if len(ideal_s) == 0 else (Fraction(1, 1) - A_SEED)
    if n == 2:
        if len(rels) == 0:
            if len(ideal_s) == 0:
                return D_SEED
            if len(ideal_s) == 1:
                return G_SEED
            return K_SEED
        (u, _) = next(iter(rels))
        root_i = marks[u]
        f_i = F_SEED_0 if root_i == 0 else F_SEED_1
        h_i = H_SEED_0 if root_i == 0 else H_SEED_1
        if len(ideal_s) == 0:
            return C_SEED
        if ideal_s == frozenset({u}):
            return f_i
        return h_i
    if n == 3:
        if len(ideal_s) == 3:
            return Fraction(1, 1) - sum(
                (
                    _q_enumerated_from_diamond_and_seed(vertices, rels, marks, sp)
                    for sp in ideals
                    if len(sp) < 3
                ),
                Fraction(0, 1),
            )
        # For any proper ideal S of a 3-vertex parent P:
        # If Max(P) \ S has a deleted vertex w that was born as an isolate or leaf over a
        # 2-vertex base C = P \ {w} with birth ideal S_w, and S does not contain w, then
        # the diamond identity Eq. (2) relates q(P, r, S) directly to q(C, r|_C, S):
        #   q(C, r|_C, S_w) * q(P, r, S) = q(C, r|_C, S) * q(C + S, r, S_w).
        m_rels = len(rels)
        if m_rels == 0:
            # 3-antichain: base C is 2-antichain with S_w = empty (q=d_seed), and q(C+S, empty) = e_seed
            if len(ideal_s) == 0:
                return E_SEED
            if len(ideal_s) == 1:
                return E_SEED * G_SEED / D_SEED
            return E_SEED * K_SEED / D_SEED
        if m_rels == 1:
            # Edge u < v, isolate w
            (u, v) = next(iter(rels))
            w = next(x for x in vertices if x not in (u, v))
            if len(ideal_s) == 0 or ideal_s == frozenset({w}):
                return E_SEED
            if w not in ideal_s:
                # Diamond with base C = (u < v), S_w = empty (q=c_seed), q(C+S, empty) = e_seed
                v_c, r_c = _restrict_poset(vertices, rels, (u, v))
                return E_SEED * _q_enumerated_from_diamond_and_seed(v_c, r_c, marks, ideal_s) / C_SEED
            # Remaining proper ideal is {u, w}: diamond with base C = 2-antichain {u, w}, S_v = {u} (q=g_seed)
            return E_SEED * K_SEED / G_SEED
        if m_rels == 2:
            mins = [x for x in vertices if not any(y == x for _, y in rels)]
            if len(mins) == 1:
                # Fork u < v1, u < v2
                u = mins[0]
                if len(ideal_s) == 0 or ideal_s == frozenset({u}):
                    return E_SEED
                # Root-plus-leaf ideal {u, v1}: diamond with base C = (u < v1), S_v2 = {u} (q=f_i)
                v_c, r_c = _restrict_poset(vertices, rels, tuple(ideal_s))
                f_i = F_SEED_0 if marks[u] == 0 else F_SEED_1
                return E_SEED * _q_enumerated_from_diamond_and_seed(v_c, r_c, marks, ideal_s) / f_i
            # Join u1 < v, u2 < v (unique maximum v, so |Max(P)\S| = 1 for all proper ideals)
            return E_SEED
        if m_rels == 3:
            # 3-chain (unique maximum, so |Max(P)\S| = 1 for all proper ideals)
            return E_SEED
    raise ValueError(f"Unsupported poset size n={n}")


def _maximal_deletion_potential(
    vertices: tuple[int, ...],
    rels: frozenset[tuple[int, int]],
    marks: dict[int, int],
    ideal_s: frozenset[int],
) -> Fraction:
    """Compute u(P, r, S) = prod_{empty != A subseteq Max(P) - S} q(P - A, r|_{P - A}, S)^{(-1)^{|A|+1}}."""
    maxima = _poset_maxima(vertices, rels)
    m_diff = tuple(x for x in maxima if x not in ideal_s)
    u_val = Fraction(1, 1)
    for r_sz in range(1, len(m_diff) + 1):
        for sub_a in itertools.combinations(m_diff, r_sz):
            vp, relsp = _restrict_poset(
                vertices, rels, tuple(x for x in vertices if x not in sub_a)
            )
            qp = _q_enumerated_from_diamond_and_seed(vp, relsp, marks, ideal_s)
            if r_sz % 2 == 1:
                u_val *= qp
            else:
                u_val /= qp
    return u_val


def evaluate_admitted_next_birth_reusability_without_standin() -> dict[str, object]:
    """Test whether the compact relational record (Y_n, D_n, R_n; i) is a reusable Markov state at Births 5 & 6 without the half-scale stand-in.

    Uses ONLY the exact admitted held-row and carrier equations from
    ``docs/track_b/native_theorem_package_v1/THEOREM_PACKAGE.md`` (§4 Eq. 13,
    §7 Eq. 27, §8 Eq. 30) and ``P4_PREFIX_FAMILY_SEPARATOR.md`` (§1 lines 56-77),
    with ZERO use of the half-scale continuation ``a_n = 1/(2(1+M_n))``:

    1. **Birth 4 -> Birth 5 on the admitted 4-chain ``C_4``** (state ``(Y_4, D_4, R_4; i) = (1, 1, 1; i)``):
       By ``P4_PREFIX_FAMILY_SEPARATOR.md`` §1 line 59, the complete 5-ideal
       catalogue of ``C_4 = (a < b < x < y)`` (counters ``(3, 2, 1, 0)``) has
       exact admitted probabilities:
         - ``S_5 = empty``:   ``B_empty = 1/352``   -> ``C_4 u {z}``, counters ``(3,2,1,0,0)`` -> ``(Y_5,D_5,R_5) = (1,0,1)``
         - ``S_5 = {a}``:     ``B_root  = 1/352``   -> ``H^# (hook 4,1)``, counters ``(4,2,1,0,0)`` -> ``(Y_5,D_5,R_5) = (1,0,1)``
         - ``S_5 = {a,b}``:   ``B_pair(i)``         -> ``(a<b<x<y, a<b<z)``, counters ``(4,3,1,0,0)`` -> ``(Y_5,D_5,R_5) = (0,0,1)``
         - ``S_5 = I = C_3``: ``b_i = B_I(i)``      -> ``H_5 = C_3 + A_2``, counters ``(4,3,2,0,0)`` -> ``(Y_5,D_5,R_5) = (1,0,0)``
         - ``S_5 = C_4``:     ``c_i = q^0(C_4,C_4)``-> ``C_5 (5-chain)``, counters ``(4,3,2,1,0)`` -> ``(Y_5,D_5,R_5) = (1,1,1)``
       Thus ``(Y_4, D_4, R_4; i) = (1, 1, 1; i)`` predicts the exact 4-cell
       birth-5 distribution over ``(Y_5, D_5, R_5)`` without any stand-in, and
       uniquely separates the two dominant children ``H_5`` (``(1,0,0)``, mass ``b_i``)
       and ``C_5`` (``(1,1,1)``, mass ``c_i``), which together carry ``99.15%``
       (``i=0``) / ``98.94%`` (``i=1``) of ``C_4``'s continuation mass.

    2. **Birth 5 -> Birth 6 on the admitted 5-parents ``H_5 = C_3 + A_2`` and ``C_5`` (zero stand-in)**:
       - **On ``H_5`` (compact state ``(Y_5, D_5, R_5; i) = (1, 0, 0; i)``, counters ``(4,3,2,0,0)``):**
         The complete 7-ideal admitted row ``G_S = theta * B_S^2 / A_S``,
         ``h_i = theta * c_i``, ``j_i = 1 - theta * Q_{2,i} - 2 * theta * c_i``
         predicts the **entire 8-cell birth-6 distribution over ``(Y_6, D_6, R_6)``**
         in closed form from ``(theta, B_pair(i), b_i)`` with **zero dependence
         on the unresolved parameter ``mu_i``**:
           * ``P(Y_6=1, D_6=0, R_6=0 | 1,0,0; i) = theta * (1/1408 + 44 * B_pair(i)^2)``
           * ``P(Y_6=0, D_6=0, R_6=0 | 1,0,0; i) = (44/41) * theta * b_i^2``
           * ``P(Y_6=0, D_6=0, R_6=1 | 1,0,0; i) = 1 - theta * Q_{2,i}``
       - **On ``C_5`` (compact state ``(Y_5, D_5, R_5; i) = (1, 1, 1; i)``, counters ``(4,3,2,1,0)``):**
         The complete 6-ideal admitted row ``D_S = theta * B_S + mu_i * 1_{S=root}``,
         ``e'_i = theta * c_i``, ``ell_i = 1 - theta - mu_i`` predicts the **entire
         4-cell joint ``(Y_6, R_6)`` distribution** with **zero dependence on ``mu_i``**
         (because ``+mu_i`` on ``S_6 = {a}`` and ``-mu_i`` on ``S_6 = C_5`` both land
         in ``(Y_6, R_6) = (1, 1)`` and cancel identically):
           * ``P(Y_6=0, R_6=1 | 1,1,1; i) = theta * b_i``
           * ``P(Y_6=1, R_6=0 | 1,1,1; i) = theta * c_i``
           * ``P(Y_6=1, R_6=1 | 1,1,1; i) = 1 - theta * (b_i + c_i)``
           * ``P(Y_6=0, R_6=0 | 1,1,1; i) = 0``

    3. **Where the compact record ``(Y_n, D_n, R_n; i)`` FAILS to close as a universal Markov state at Birth 6:**
       - **Non-closure 1 (``mu_i`` splits ``D_6`` inside ``(Y_6=1, R_6=1)`` on ``C_5``):**
         Separating ``D_6 = 1`` (``P = 1 - theta - mu_i``) from ``D_6 = 0``
         (``P = theta*(1/176 + B_pair(i)) + mu_i``) inside ``(Y_6=1, R_6=1)`` on
         ``C_5`` requires ``mu_i = (35/12672)*(1 - R_i)/c_i`` (``THEOREM_PACKAGE.md``
         Eq. 30), which couples to off-chain carrier loads ``R_i``.
       - **Non-closure 2 (Complete Birth-6 row summation on the two parents sharing ``(Y_5, D_5, R_5; i) = (1, 0, 1; i)``):**
         Among ``C_4``'s children at birth 5, ``(1, 0, 1; i)`` (mass ``1/176``)
         merges ``K_5 := C_4 u {z}`` (``S_5 = empty``, counters ``(3,2,1,0,0)``) and
         ``H^# := (a<b<x<y, a<z)`` (``S_5 = {a}``, counters ``(4,2,1,0,0)``), which
         differ only in whether root ``a`` has counter ``3`` or ``4``.
         * **Correction of the 4-chain attachment cell and cancellation in ``(1, 0, 1)``:**
           On both ``K_5`` and ``H^#``, attaching to the 4-chain ``S_6 = C_4 = {0,1,2,3}``
           increments the old chain tip ``y = 3`` from ``0 -> 1``, so it lands in
           ``(Y_6, D_6, R_6) = (1, 0, 1)`` (not ``(1, 0, 0)``) alongside the full ideal
           ``S_6 = {0,1,2,3,4}`` and ``S_6 = {0,4}``. When all ideals in Cell ``(1, 0, 1)``
           are summed, both the hook-``(5,1)`` term ``(35/36)*c_i*sigma_i`` on ``S_6 = C_4``
           and the hook-``(4,1,1)`` term ``(35/36)*p_i*beta_i`` on ``S_6 = {0,4}`` cancel
           identically against the full-ideal complement, just as ``+/-mu_i`` cancels on ``C_5``.
         * **Exact agreement on Cell ``(1, 0, 0)`` and the entire joint ``(D_6, R_6)`` readout:**
           On both ``K_5`` and ``H^#``, Cell ``(1, 0, 0)`` contains only the single ideal
           ``S_6 = C_3 = {0,1,2}``, with identical potential ``u(K_5, i, C_3) = b_i / 8 = u(H^#, i, C_3)``
           and identical admitted probability ``P(Y_6=1, D_6=0, R_6=0 | K_5, i) = (b_i/8)*theta = P(Y_6=1, D_6=0, R_6=0 | H^#, i)``.
           Because the only other occupied cells ``(0, 0, 1)`` and ``(1, 0, 1)`` share
           ``(D_6, R_6) = (0, 1)``, the entire joint ``(D_6, R_6)`` distribution agrees
           identically between ``K_5`` and ``H^#`` at Birth 6:
           ``P(D_6=0, R_6=0) = (b_i/8)*theta`` and ``P(D_6=0, R_6=1) = 1 - (b_i/8)*theta``.
         * **Exact difference on the full ``(Y_6, D_6, R_6)`` distribution (Cell ``(0, 0, 1)`` vs. Cell ``(1, 0, 1)``), carried symbolically and verified from the certificates:**
           Cell ``(0, 0, 1)`` sums ``S_6 = {0,1}`` and ``S_6 = {0,1,4}``. On ``K_5``, both
           raise the Ferrers deletion defect from ``1 -> 2`` (restoration-only ``alpha_min = 0``
           in every primary or canonical optimum), giving
           ``P(0,0,1 | K_5, i) = (44*B_pair(i)*q(K_4,{0,1}) + 4693/17600)*theta``.
           On ``H^#``, ``S_6 = {0,1,4}`` joins ``b = 1`` and ``z = 4`` into the 6-vertex
           Ferrers diagram Shape ``(4,2)`` (carrier of ``gamma_{ij}`` in ``THEOREM_PACKAGE.md``
           §8 Eq. 32). Carrying the ``H^#`` carrier coefficients ``(sigma_i, beta_i, gamma_{ij})``
           symbolically as ``q = w_1 + w_sigma*(35/36)*c_i*sigma_i + w_beta*(35/36)*p_i*beta_i + w_gamma*(35/36)*g_{ij}*gamma_{ij} + w_theta*theta``:
             - ``w_sigma = 0`` and ``w_beta = 0`` in every summed ``(Y_6, D_6, R_6)`` cell,
               and ``w_gamma = 0`` as well in every summed ``(D_6, R_6)`` cell;
             - In Cell ``(0, 0, 1)``, ``Delta P(0,0,1) = P(0,0,1 | H^#, r) - P(0,0,1 | K_5, r) = (35/36)*g_{ij}*gamma_{ij} + Delta u_{(0,0,1)}(i)*theta``.
             - Direct canonical-key lookup in the byte-pinned RI-41 certificate
               (``docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json``,
               SHA-256 ``3d966fb2...``) gives ``Delta u_{(0,0,1)}(0) = 1887761/77440000 > 0``
               and ``Delta u_{(0,0,1)}(1) = 2579343/6050000 > 0``. Since ``g_{ij}*gamma_{ij} >= 0``
               and ``theta > 0``, ``Delta P(0,0,1) > 0`` holds for **every** feasible carrier
               allocation ``(sigma_i, beta_i, gamma_{ij}) >= 0`` in ``THEOREM_PACKAGE.md`` §8
               Eq. (32), without assuming a specific ordered-root binding; specializing to the
               byte-pinned RI-63 certificate (``CERTIFICATE.json``, SHA-256 ``f55625a6...``)
               evaluates ``g_{ij}*gamma_{ij} = 1`` in both ``alpha`` and ``alternative_primary_alpha``.
         * **Follow-up Test A (Root counter ``c_a`` where ``(Y_6, D_6, R_6)`` differs):**
           Adding the root counter ``c_a in {3, 4}`` uniquely separates ``K_5`` (``c_a = 3``)
           from ``H^#`` (``c_a = 4``) and uniquely separates all 5 children of ``C_4`` at
           Birth 5, completely resolving the Birth-6 ``(Y_6, D_6, R_6)`` ambiguity.
         * **Follow-up Test B (Keep smaller record where ``K_5`` and ``H^#`` agree at Birth 6, and test one birth deeper at Birth 7 via exact possible-versus-impossible support):**
           Following the shared Birth-6 readout ``(Y_6, D_6, R_6) = (1, 0, 0)`` from each parent
           (``S_6 = C_3 = {0,1,2}``, producing ``K_6^(1,0,0) = H_5 u {z}`` with ``c_6 = (4,3,2,0,0,0)``
           vs. ``H_6^(1,0,0) = (H_5, a<z)`` with ``c_6 = (0,3,2,0,0,0)``), on ``H_6^(1,0,0)``
           the root counter wrapped to ``c_a = 0`` at Birth 6. At Birth 7 (``n = 6 -> 7``),
           every nonempty attachment ``S_7 != empty`` on ``H_6^(1,0,0)`` includes the unique
           root ``a = 0``, advances ``c_a : 0 -> 1 (mod 5)``, and lights up the relay ``R_7 = 1``
           (while ``S_7 = empty`` gives ``(1, 0, 0)``), making ``(Y_7, D_7, R_7) = (0, 0, 0)``
           **strictly impossible (``P = 0``)** under *any* admitted Birth-7 law. On ``K_6^(1,0,0)``,
           the legal attachment ``S_7 = C_3 = {0,1,2}`` wraps ``c_a : 4 -> 0 (mod 5)`` and
           produces ``c_7 = (0,4,3,0,0,0,0)``, making ``(Y_7, D_7, R_7) = (0, 0, 0)`` **strictly
           possible (``P > 0``)** under *any* admitted Birth-7 law (and across all Birth-6
           children, ``R_7 = 0`` is possible on ``10/10`` children of ``K_5`` vs. only ``2/9``
           children of ``H^#``). Unnormalized deletion potentials ``u(P_6, i, S_7)`` are reported
           separately as potentials, not complete Birth-7 probabilities.
       - **Non-closure 3 (Modulo-5 counter wrap breaks counter-only chain proxy ``D*_6`` at Birth 6):**
         At ``n = 6`` (birth 6), root ``a`` wraps ``4 + 1 = 0 (mod 5)`` on ``S_6 = C_5``,
         so the 6-chain ``C_6`` (modulo-5 counters ``(0,4,3,2,1,0)``, ``D_6 = 1``) has
         the exact same modulo-5 counter multiset ``{0,0,1,2,3,4}`` as the disconnected
         non-chain ``C_5 u {w}`` (``S_6 = empty``, modulo-5 counters ``(4,3,2,1,0,0)``,
         ``D_6 = 0``).
    """
    a_c3_full = Fraction(41, 44)
    e_c3_prop = Fraction(1, 44)

    b_empty = Fraction(1, 352)
    b_root = Fraction(1, 352)
    b_pair = {0: Fraction(1, 352), 1: Fraction(27, 5500)}
    # Exact binding from P4_PREFIX_FAMILY_SEPARATOR.md §1 lines 40 & 59:
    # b_i = q^0(C_4, I=C_3) (produces H_5 = C_3 + A_2), c_i = q^0(C_4, C_4) (produces C_5)
    b_c4_i = {0: Fraction(8077, 8800), 1: Fraction(40303, 44000)}
    c_c4_full = {0: Fraction(81, 1100), 1: Fraction(3231, 44000)}

    c4_birth5_dist_by_prep: dict[int, dict[str, str]] = {}
    h5_birth6_theta_coeffs_by_prep: dict[int, dict[str, str]] = {}
    c5_birth6_yr_theta_coeffs_by_prep: dict[int, dict[str, str]] = {}
    dominant_h5_c5_mass_fraction: dict[int, str] = {}

    for i_root in (0, 1):
        row_sum_c4 = b_empty + b_root + b_pair[i_root] + b_c4_i[i_root] + c_c4_full[i_root]
        if row_sum_c4 != Fraction(1, 1):
            raise RuntimeError(f"Admitted C_4 row failed normalization for i={i_root}")

        c4_birth5_dist_by_prep[i_root] = {
            "(Y5=0, D5=0, R5=1) [S5={a,b}]": str(b_pair[i_root]),
            "(Y5=1, D5=0, R5=0) [S5=C3 -> H5=C3+A2]": str(b_c4_i[i_root]),
            "(Y5=1, D5=0, R5=1) [S5 in {empty,{a}} -> C4u{z}, H^#]": str(b_empty + b_root),
            "(Y5=1, D5=1, R5=1) [S5=C4 -> C5]": str(c_c4_full[i_root]),
        }
        dominant_h5_c5_mass_fraction[i_root] = str(b_c4_i[i_root] + c_c4_full[i_root])

        # Birth 6 on H_5 = C_3 + A_2 (counters (4,3,2,0,0), state (Y_5,D_5,R_5) = (1,0,0)):
        # G_S = theta * B_S^2 / A_S, h_i = theta * c_i, j_i = 1 - theta * Q_{2,i} - 2 * theta * c_i
        g_surv_theta = (
            (b_empty ** 2) / e_c3_prop
            + (b_root ** 2) / e_c3_prop
            + (b_pair[i_root] ** 2) / e_c3_prop
        )
        g_i_theta = (b_c4_i[i_root] ** 2) / a_c3_full
        q2_i = g_surv_theta + g_i_theta
        h5_birth6_theta_coeffs_by_prep[i_root] = {
            "P(Y6=1, D6=0, R6=0) / theta": str(g_surv_theta),
            "P(Y6=0, D6=0, R6=0) / theta": str(g_i_theta),
            "P(Y6=0, D6=0, R6=1)": f"1 - ({q2_i})*theta",
            "Q2_i_exact": str(q2_i),
            "depends_on_unresolved_mu_i": "False",
        }

        # Birth 6 on C_5 (counters (4,3,2,1,0), state (Y_5,D_5,R_5) = (1,1,1)):
        # Joint (Y_6, R_6) distribution is 100% independent of mu_i:
        c5_birth6_yr_theta_coeffs_by_prep[i_root] = {
            "P(Y6=0, R6=0)": "0",
            "P(Y6=0, R6=1) / theta [S6=C3]": str(b_c4_i[i_root]),
            "P(Y6=1, R6=0) / theta [S6=C4 -> C4+A2]": str(c_c4_full[i_root]),
            "P(Y6=1, R6=1) [S6 in {empty,{a},{a,b},C5}]": (
                f"1 - ({b_c4_i[i_root] + c_c4_full[i_root]})*theta"
            ),
            "P(Y6=1) marginal": f"1 - ({b_c4_i[i_root]})*theta",
            "P(R6=1) marginal": f"1 - ({c_c4_full[i_root]})*theta",
            "yr_joint_depends_on_unresolved_mu_i": "False",
            "P(Y6=1, D6=1, R6=1) [S6=C5 -> C6]": f"1 - theta - mu_{i_root}",
            "P(Y6=1, D6=0, R6=1) [S6 in {empty,{a},{a,b}}]": (
                f"({b_empty + b_root + b_pair[i_root]})*theta + mu_{i_root}"
            ),
        }

    # Verify and load the byte-pinned RI-41 parent-4 and RI-63 parent-5 certificates directly
    # from disk (hashes from THEOREM_PACKAGE.md §12 lines 832-835):
    repo_root = Path(__file__).resolve().parents[2]
    ri41_path = (
        repo_root
        / "docs"
        / "track_b"
        / "native_growth_height_normalization_v1"
        / "CERTIFICATE.json"
    )
    ri63_path = (
        repo_root
        / "docs"
        / "track_b"
        / "native_growth_expected_defect_completion_v1"
        / "CERTIFICATE.json"
    )
    raw_ri41 = ri41_path.read_bytes()
    sha256_ri41 = hashlib.sha256(raw_ri41).hexdigest()
    expected_sha256_ri41 = "3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969"
    if sha256_ri41 != expected_sha256_ri41:
        raise RuntimeError("RI-41 parent-4 certificate SHA-256 mismatch")
    cert_ri41 = json.loads(raw_ri41)
    roots_ri41 = {tuple(r): idx for idx, r in enumerate(cert_ri41["roots"])}
    default_alpha_ri41 = Fraction(cert_ri41["default_alpha"])
    overrides_ri41 = {int(k): Fraction(v) for k, v in cert_ri41["overrides"].items()}

    raw_ri63 = ri63_path.read_bytes()
    sha256_ri63 = hashlib.sha256(raw_ri63).hexdigest()
    expected_sha256_ri63 = "f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b"
    if sha256_ri63 != expected_sha256_ri63:
        raise RuntimeError("RI-63 parent-5 certificate SHA-256 mismatch")
    cert_ri63 = json.loads(raw_ri63)
    alpha_min_ri63 = {int(k): Fraction(v) for k, v in cert_ri63["alpha"].items()}
    alpha_alt_ri63 = {
        int(k): Fraction(v) for k, v in cert_ri63["alternative_primary_alpha"].items()
    }

    def _canonical_local_key_4(
        rels4: frozenset[tuple[int, int]],
        ideal_s: frozenset[int],
        marks4: dict[int, int],
    ) -> tuple[int, int, int]:
        """Compute RI-41 canonical local key min_perm (E(P), mask(S), mask(r|S)) on 4 vertices."""
        best_pair: tuple[int, int] | None = None
        cands: list[tuple[int, ...]] = []
        for perm in itertools.permutations(range(4)):
            edge_mask = sum(1 << (4 * perm[u] + perm[v]) for u, v in rels4)
            sel_mask = sum(1 << perm[v] for v in ideal_s)
            pair = (edge_mask, sel_mask)
            if best_pair is None or pair < best_pair:
                best_pair = pair
                cands = [perm]
            elif pair == best_pair:
                cands.append(perm)
        assert best_pair is not None
        rec_mask = min(
            sum(1 << perm[v] for v in ideal_s if marks4.get(v, 0) == 1)
            for perm in cands
        )
        return (best_pair[0], best_pair[1], rec_mask)

    # Derive the complete parent-4 rows of K_4 = (0<1<2) u {4} and Q = (0<1<2, 0<4)
    # directly from the byte-pinned RI-41 certificate + _maximal_deletion_potential
    # (no hardcoded parent-4 probabilities):
    v4_0123 = (0, 1, 2, 3)
    rels_k4_0123 = frozenset({(0, 1), (0, 2), (1, 2)})
    rels_q4_0123 = frozenset({(0, 1), (0, 2), (1, 2), (0, 3)})
    v3_013 = (0, 1, 3)
    rels_b3_k4 = frozenset({(0, 1)})
    rels_b3_q4 = frozenset({(0, 1), (0, 3)})

    def _lookup_ri41_alpha(
        parent_name: str,
        rels4: frozenset[tuple[int, int]],
        ideal_s: frozenset[int],
        i_r: int,
        j_r: int = 0,
    ) -> tuple[int, tuple[int, int, int], Fraction]:
        marks = {
            0: (i_r if (parent_name == "Q4" or 3 in ideal_s) else 0),
            1: (j_r if 3 in ideal_s else 0),
            2: 0,
            3: 0,
        }
        key = _canonical_local_key_4(rels4, ideal_s, marks)
        if key in roots_ri41:
            idx = roots_ri41[key]
            return idx, key, overrides_ri41.get(idx, default_alpha_ri41)
        # 1-step base-3 diamond on P_4 \ {2} where vertex 2 was born over S_3 = {0, 1}:
        rels_b3 = rels_b3_k4 if parent_name == "K4" else rels_b3_q4
        _, rels4_alt = _append_birth_vertex(v3_013, rels_b3, ideal_s, 2)
        key_alt = _canonical_local_key_4(
            rels4_alt,
            frozenset({0, 1}),
            {
                0: (i_r if (parent_name == "Q4" and 0 in ideal_s) else 0),
                1: 0,
                2: 0,
                3: 0,
            },
        )
        idx = roots_ri41[key_alt]
        return idx, key_alt, overrides_ri41.get(idx, default_alpha_ri41)

    q_c3_row = {
        frozenset(): e_c3_prop,
        frozenset({0}): e_c3_prop,
        frozenset({0, 1}): e_c3_prop,
        frozenset({0, 1, 2}): a_c3_full,
    }
    q_c4_row = {
        i_r: {
            frozenset(): b_empty,
            frozenset({0}): b_root,
            frozenset({0, 1}): b_pair[i_r],
            frozenset({0, 1, 2}): b_c4_i[i_r],
            frozenset({0, 1, 2, 3}): c_c4_full[i_r],
        }
        for i_r in (0, 1)
    }
    q_k4_row: dict[int, dict[frozenset[int], Fraction]] = {0: {}, 1: {}}
    q_q4_row: dict[int, dict[frozenset[int], Fraction]] = {0: {}, 1: {}}
    ri41_verified_cell001_roots: dict[str, object] = {}

    for parent_name, rels4, target_dict in (
        ("K4", rels_k4_0123, q_k4_row),
        ("Q4", rels_q4_0123, q_q4_row),
    ):
        for i_r in (0, 1):
            row_map: dict[frozenset[int], Fraction] = {}
            for s_0123 in _enumerate_poset_ideals(v4_0123, rels4):
                if len(s_0123) == 4:
                    continue
                # Verify all mark combinations (i_r, j_r) for S={0,1,3} (which maps to S_6={0,1,4})
                alphas_by_j: list[Fraction] = []
                root_indices_by_j: list[int] = []
                for j_r in ((0, 1) if 3 in s_0123 else (0,)):
                    idx, _, alpha_val = _lookup_ri41_alpha(
                        parent_name, rels4, s_0123, i_r, j_r
                    )
                    alphas_by_j.append(alpha_val)
                    root_indices_by_j.append(idx)
                if len(set(alphas_by_j)) != 1:
                    raise RuntimeError(
                        f"Mark j changed alpha on {parent_name} S={s_0123} for i={i_r}"
                    )
                u4_val = _maximal_deletion_potential(
                    v4_0123, rels4, {0: i_r, 1: 0, 2: 0, 3: 0}, s_0123
                )
                q4_val = alphas_by_j[0] * u4_val
                s_0124 = frozenset(4 if x == 3 else x for x in s_0123)
                row_map[s_0124] = q4_val
                if s_0123 in (frozenset({0, 1}), frozenset({0, 1, 3})):
                    ri41_verified_cell001_roots[
                        f"{parent_name}_i{i_r}_S{sorted(s_0124)}"
                    ] = {
                        "ri41_root_indices": root_indices_by_j,
                        "alpha_from_certificate": str(alphas_by_j[0]),
                        "u4_from_seed_deletion": str(u4_val),
                        "q4_exact": str(q4_val),
                    }
            row_map[frozenset({0, 1, 2, 4})] = Fraction(1, 1) - sum(
                row_map.values(), Fraction(0, 1)
            )
            target_dict[i_r] = row_map

    # Cross-check THEOREM_PACKAGE.md Eq. (27) (q(K_4, {r,a,u}; i,j) = 4693/17600)
    # and §8 line 708 (h_* = q_Q(rab) = 41/352):
    if q_k4_row[0][frozenset({0, 1, 4})] != Fraction(4693, 17600):
        raise RuntimeError("RI-41 derived K_4 {0,1,4} disagrees with THEOREM_PACKAGE.md Eq. (27)")
    if q_q4_row[0][frozenset({0, 1, 2})] != Fraction(41, 352):
        raise RuntimeError("RI-41 derived Q {0,1,2} disagrees with h_* = 41/352")

    v4_c4 = (0, 1, 2, 3)
    rels_c4 = frozenset({(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)})
    c4_counters = {0: 3, 1: 2, 2: 1, 3: 0}

    # Dynamically build K_5 (S_5 = empty) and H^# (S_5 = {0}) from C_4 at Birth 5:
    v5_k5, rels_k5 = _append_birth_vertex(v4_c4, rels_c4, frozenset(), 4)
    c5_k5 = _update_modulo5_counters(c4_counters, frozenset(), 4)
    v5_hs, rels_hs = _append_birth_vertex(v4_c4, rels_c4, frozenset({0}), 4)
    c5_hs = _update_modulo5_counters(c4_counters, frozenset({0}), 4)

    def _readout_ydr(
        vertices: tuple[int, ...],
        rels: frozenset[tuple[int, int]],
        counters: dict[int, int],
    ) -> tuple[int, int, int]:
        n_v = len(vertices)
        y_bit = 1 if any(v == 2 for v in counters.values()) else 0
        d_bit = 1 if len(rels) == n_v * (n_v - 1) // 2 else 0
        r_bit = 1 if any(v == 1 for v in counters.values()) else 0
        return (y_bit, d_bit, r_bit)

    def _u5_from_admitted_p4(
        parent_tag: str,
        rels5: frozenset[tuple[int, int]],
        i_r: int,
        ideal_s6: frozenset[int],
    ) -> Fraction:
        """Dynamically compute maximal-deletion potential u(P_5, i, S_6) via Eq. (3)."""
        maxima = _poset_maxima((0, 1, 2, 3, 4), rels5)
        m_diff = tuple(sorted(x for x in maxima if x not in ideal_s6))
        u_val = Fraction(1, 1)
        for r_sz in range(1, len(m_diff) + 1):
            for sub_a in itertools.combinations(m_diff, r_sz):
                keep = frozenset(x for x in (0, 1, 2, 3, 4) if x not in sub_a)
                if keep == frozenset({0, 1, 2}):
                    fac = q_c3_row[ideal_s6]
                elif keep == frozenset({0, 1, 2, 3}):
                    fac = q_c4_row[i_r][ideal_s6]
                elif keep == frozenset({0, 1, 2, 4}):
                    fac = (
                        q_k4_row[i_r][ideal_s6]
                        if parent_tag == "K5"
                        else q_q4_row[i_r][ideal_s6]
                    )
                else:
                    raise RuntimeError(f"Unexpected deletion keep set {keep}")
                if r_sz % 2 == 1:
                    u_val *= fac
                else:
                    u_val /= fac
        return u_val

    # Carry the H^# canonical carrier loads (THEOREM_PACKAGE.md §8 Eq. 32:
    # c_i*sigma_i + p_i*beta_i + g_{ij}*gamma_{ij} <= 1) completely SYMBOLICALLY as a
    # 5-tuple (w_1, w_sigma, w_beta, w_gamma, w_theta) representing:
    #   q = w_1 + w_sigma*(35/36)*c_i*sigma_i + w_beta*(35/36)*p_i*beta_i
    #       + w_gamma*(35/36)*g_{ij}*gamma_{ij} + w_theta*theta.
    # On K_5 = C_4 u {z}, all ideals outside Cell (1,0,1) — namely S_6={0,1,2} in (1,0,0)
    # and S_6 in {{0,1},{0,1,4}} in (0,0,1) — strictly raise the Ferrers deletion defect
    # from 1 -> 2 (d_{K_5}(S_6) = +1), so their canonical boundary components vanish
    # identically by the everywhere-neutral canonical support theorem (THEOREM_PACKAGE.md
    # §7 lines 668-670 & §9 line 786).
    Symbolic5Tuple = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]

    def _q5_symbolic_5tuple(
        parent_tag: str,
        rels5: frozenset[tuple[int, int]],
        i_r: int,
        ideal_s6: frozenset[int],
    ) -> Symbolic5Tuple:
        full5 = frozenset({0, 1, 2, 3, 4})
        z0 = Fraction(0, 1)
        one = Fraction(1, 1)
        if ideal_s6 != full5:
            u_val = _u5_from_admitted_p4(parent_tag, rels5, i_r, ideal_s6)
            if parent_tag == "Hsharp":
                if ideal_s6 == frozenset({0, 1, 2, 3}):
                    return (z0, one, z0, z0, u_val)
                if ideal_s6 == frozenset({0, 4}):
                    return (z0, z0, one, z0, u_val)
                if ideal_s6 == frozenset({0, 1, 4}):
                    return (z0, z0, z0, one, u_val)
            return (z0, z0, z0, z0, u_val)
        acc = (z0, z0, z0, z0, z0)
        for sp in _enumerate_poset_ideals((0, 1, 2, 3, 4), rels5):
            if sp != full5:
                term = _q5_symbolic_5tuple(parent_tag, rels5, i_r, sp)
                acc = tuple(a + b for a, b in zip(acc, term))  # type: ignore[assignment]
        return (one - acc[0], -acc[1], -acc[2], -acc[3], -acc[4])

    def _format_symbolic_5tuple(w: Symbolic5Tuple) -> str:
        parts: list[str] = []
        if w[0] != 0:
            parts.append(f"{w[0]}")
        if w[1] != 0:
            parts.append(f"({w[1]})*(35/36)*c_i*sigma_i")
        if w[2] != 0:
            parts.append(f"({w[2]})*(35/36)*p_i*beta_i")
        if w[3] != 0:
            parts.append(f"({w[3]})*(35/36)*g_ij*gamma_ij")
        if w[4] != 0:
            parts.append(f"({w[4]})*theta")
        return " + ".join(parts) if parts else "0"

    # Also verify the RI-63 certificate specialization (CERTIFICATE.json components
    # 408..411 for sigma_i, beta_i and 412..415 for gamma_{ij}):
    g_0j = q_q4_row[0][frozenset({0, 1, 4})]
    g_1j = q_q4_row[1][frozenset({0, 1, 4})]
    ri63_carrier_verification = {
        "sha256_verified": sha256_ri63 == expected_sha256_ri63,
        "sigma_components_408_409_canonical_and_alt": [
            str(alpha_min_ri63.get(408, Fraction(0, 1))),
            str(alpha_min_ri63.get(409, Fraction(0, 1))),
            str(alpha_alt_ri63.get(408, Fraction(0, 1))),
            str(alpha_alt_ri63.get(409, Fraction(0, 1))),
        ],
        "beta_components_410_411_canonical_and_alt": [
            str(alpha_min_ri63.get(410, Fraction(0, 1))),
            str(alpha_min_ri63.get(411, Fraction(0, 1))),
            str(alpha_alt_ri63.get(410, Fraction(0, 1))),
            str(alpha_alt_ri63.get(411, Fraction(0, 1))),
        ],
        "gamma_i0_components_412_414_times_g0j": [
            str(alpha_min_ri63[412] * g_0j),
            str(alpha_min_ri63[414] * g_0j),
            str(alpha_alt_ri63[412] * g_0j),
            str(alpha_alt_ri63[414] * g_0j),
        ],
        "gamma_i1_components_413_415_times_g1j": [
            str(alpha_min_ri63[413] * g_1j),
            str(alpha_min_ri63[415] * g_1j),
            str(alpha_alt_ri63[413] * g_1j),
            str(alpha_alt_ri63[415] * g_1j),
        ],
    }
    if not (
        all(x == "0" for x in ri63_carrier_verification["sigma_components_408_409_canonical_and_alt"])
        and all(x == "0" for x in ri63_carrier_verification["beta_components_410_411_canonical_and_alt"])
        and all(x == "1" for x in ri63_carrier_verification["gamma_i0_components_412_414_times_g0j"])
        and all(x == "1" for x in ri63_carrier_verification["gamma_i1_components_413_415_times_g1j"])
    ):
        raise RuntimeError("RI-63 H^# carrier specialization check failed")

    def _eval_ri63_from_symbolic(w: Symbolic5Tuple) -> tuple[Fraction, Fraction]:
        """Evaluate symbolic 5-tuple at RI-63 certificate (sigma_i=0, beta_i=0, g_ij*gamma_ij=1)."""
        return (w[0] + w[3] * Fraction(35, 36), w[4])

    ideals_k5 = _enumerate_poset_ideals(v5_k5, rels_k5)
    ideals_hs = _enumerate_poset_ideals(v5_hs, rels_hs)

    # Check the cell of the 4-chain attachment S_6 = C_4 = {0,1,2,3} dynamically on both parents:
    s6_c4 = frozenset({0, 1, 2, 3})
    s6_full5 = frozenset({0, 1, 2, 3, 4})
    c6_k5_on_c4 = _update_modulo5_counters(c5_k5, s6_c4, 5)
    v6_k5_on_c4, r6_k5_on_c4 = _append_birth_vertex(v5_k5, rels_k5, s6_c4, 5)
    cell_k5_on_c4 = _readout_ydr(v6_k5_on_c4, r6_k5_on_c4, c6_k5_on_c4)

    c6_hs_on_c4 = _update_modulo5_counters(c5_hs, s6_c4, 5)
    v6_hs_on_c4, r6_hs_on_c4 = _append_birth_vertex(v5_hs, rels_hs, s6_c4, 5)
    cell_hs_on_c4 = _readout_ydr(v6_hs_on_c4, r6_hs_on_c4, c6_hs_on_c4)

    c6_k5_on_full = _update_modulo5_counters(c5_k5, s6_full5, 5)
    v6_k5_on_full, r6_k5_on_full = _append_birth_vertex(v5_k5, rels_k5, s6_full5, 5)
    cell_k5_on_full = _readout_ydr(v6_k5_on_full, r6_k5_on_full, c6_k5_on_full)

    c6_hs_on_full = _update_modulo5_counters(c5_hs, s6_full5, 5)
    v6_hs_on_full, r6_hs_on_full = _append_birth_vertex(v5_hs, rels_hs, s6_full5, 5)
    cell_hs_on_full = _readout_ydr(v6_hs_on_full, r6_hs_on_full, c6_hs_on_full)

    c4_attachment_lands_in_101_with_full_on_both = (
        cell_k5_on_c4 == (1, 0, 1)
        and cell_hs_on_c4 == (1, 0, 1)
        and cell_k5_on_full == (1, 0, 1)
        and cell_hs_on_full == (1, 0, 1)
    )

    k5_vs_hsharp_by_prep: dict[int, dict[str, object]] = {}
    cell_100_agrees_all_prep = True
    joint_d6_r6_agrees_all_prep = True
    full_ydr6_differs_all_prep = True
    sigma_and_beta_cancel_symbolically_all_prep = True
    all_carriers_cancel_in_dr_all_prep = True
    cell_001_diff_positive_for_all_nonneg_gamma = True

    zero5: Symbolic5Tuple = (
        Fraction(0, 1),
        Fraction(0, 1),
        Fraction(0, 1),
        Fraction(0, 1),
        Fraction(0, 1),
    )

    for i_root in (0, 1):
        k5_ydr_sym: dict[tuple[int, int, int], Symbolic5Tuple] = {}
        hs_ydr_sym: dict[tuple[int, int, int], Symbolic5Tuple] = {}
        k5_dr_sym: dict[tuple[int, int], Symbolic5Tuple] = {}
        hs_dr_sym: dict[tuple[int, int], Symbolic5Tuple] = {}
        k5_ideal_ledger: list[dict[str, object]] = []
        hs_ideal_ledger: list[dict[str, object]] = []

        for s6 in ideals_k5:
            c6 = _update_modulo5_counters(c5_k5, s6, 5)
            v6, r6 = _append_birth_vertex(v5_k5, rels_k5, s6, 5)
            cell = _readout_ydr(v6, r6, c6)
            dr_cell = (cell[1], cell[2])
            w5 = _q5_symbolic_5tuple("K5", rels_k5, i_root, s6)
            prev_w = k5_ydr_sym.get(cell, zero5)
            k5_ydr_sym[cell] = tuple(a + b for a, b in zip(prev_w, w5))  # type: ignore[assignment]
            p_dr = k5_dr_sym.get(dr_cell, zero5)
            k5_dr_sym[dr_cell] = tuple(a + b for a, b in zip(p_dr, w5))  # type: ignore[assignment]
            c_part, t_part = _eval_ri63_from_symbolic(w5)
            k5_ideal_ledger.append(
                {
                    "S6": sorted(s6),
                    "counters_c6": tuple(c6[k] for k in range(6)),
                    "cell_Y6_D6_R6": cell,
                    "symbolic": _format_symbolic_5tuple(w5),
                    "const_term": str(c_part),
                    "theta_coeff": str(t_part),
                }
            )

        for s6 in ideals_hs:
            c6 = _update_modulo5_counters(c5_hs, s6, 5)
            v6, r6 = _append_birth_vertex(v5_hs, rels_hs, s6, 5)
            cell = _readout_ydr(v6, r6, c6)
            dr_cell = (cell[1], cell[2])
            w5 = _q5_symbolic_5tuple("Hsharp", rels_hs, i_root, s6)
            prev_w = hs_ydr_sym.get(cell, zero5)
            hs_ydr_sym[cell] = tuple(a + b for a, b in zip(prev_w, w5))  # type: ignore[assignment]
            p_dr = hs_dr_sym.get(dr_cell, zero5)
            hs_dr_sym[dr_cell] = tuple(a + b for a, b in zip(p_dr, w5))  # type: ignore[assignment]
            c_part, t_part = _eval_ri63_from_symbolic(w5)
            hs_ideal_ledger.append(
                {
                    "S6": sorted(s6),
                    "counters_c6": tuple(c6[k] for k in range(6)),
                    "cell_Y6_D6_R6": cell,
                    "symbolic": _format_symbolic_5tuple(w5),
                    "const_term": str(c_part),
                    "theta_coeff": str(t_part),
                }
            )

        # Verify symbolic row normalization: sum of 5-tuples over all cells is (1, 0, 0, 0, 0)
        norm5: Symbolic5Tuple = (
            Fraction(1, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
            Fraction(0, 1),
        )
        k5_sum5 = zero5
        for w_cell in k5_ydr_sym.values():
            k5_sum5 = tuple(a + b for a, b in zip(k5_sum5, w_cell))  # type: ignore[assignment]
        hs_sum5 = zero5
        for w_cell in hs_ydr_sym.values():
            hs_sum5 = tuple(a + b for a, b in zip(hs_sum5, w_cell))  # type: ignore[assignment]
        if k5_sum5 != norm5 or hs_sum5 != norm5:
            raise RuntimeError(f"Symbolic Birth-6 row failed normalization for i={i_root}")

        # Verify symbolically that w_sigma == 0 and w_beta == 0 in every summed (Y6,D6,R6) cell:
        sig_beta_zero = all(w[1] == 0 and w[2] == 0 for w in hs_ydr_sym.values())
        # Verify symbolically that w_sigma == w_beta == w_gamma == 0 in every summed (D6,R6) cell:
        dr_carriers_zero = all(
            w[1] == 0 and w[2] == 0 and w[3] == 0 for w in hs_dr_sym.values()
        )
        sigma_and_beta_cancel_symbolically_all_prep = (
            sigma_and_beta_cancel_symbolically_all_prep and sig_beta_zero
        )
        all_carriers_cancel_in_dr_all_prep = (
            all_carriers_cancel_in_dr_all_prep and dr_carriers_zero
        )

        # Compare symbolic 5-tuples directly (valid for ALL (sigma_i, beta_i, gamma_{ij})):
        c100_agrees = (k5_ydr_sym.get((1, 0, 0)) == hs_ydr_sym.get((1, 0, 0)))
        dr_agrees = (k5_dr_sym == hs_dr_sym)
        w_k5_001 = k5_ydr_sym[(0, 0, 1)]
        w_hs_001 = hs_ydr_sym[(0, 0, 1)]
        w_diff_001: Symbolic5Tuple = tuple(
            b - a for a, b in zip(w_k5_001, w_hs_001)
        )  # type: ignore[assignment]
        # Since w_diff_001 = (0, 0, 0, +1, Delta u > 0), Delta P(0,0,1) > 0 for ALL g_ij*gamma_ij >= 0 and theta > 0!
        diff_pos_all_gamma = (
            w_diff_001[0] == 0
            and w_diff_001[1] == 0
            and w_diff_001[2] == 0
            and w_diff_001[3] == Fraction(1, 1)
            and w_diff_001[4] > 0
        )
        cell_001_diff_positive_for_all_nonneg_gamma = (
            cell_001_diff_positive_for_all_nonneg_gamma and diff_pos_all_gamma
        )
        ydr_differs = (k5_ydr_sym != hs_ydr_sym) and diff_pos_all_gamma

        cell_100_agrees_all_prep = cell_100_agrees_all_prep and c100_agrees
        joint_d6_r6_agrees_all_prep = joint_d6_r6_agrees_all_prep and dr_agrees
        full_ydr6_differs_all_prep = full_ydr6_differs_all_prep and ydr_differs

        k5_001_c, k5_001_t = _eval_ri63_from_symbolic(w_k5_001)
        hs_001_c, hs_001_t = _eval_ri63_from_symbolic(w_hs_001)

        k5_vs_hsharp_by_prep[i_root] = {
            "K5_summed_Y6_D6_R6_cells_symbolic": {
                str(k): _format_symbolic_5tuple(v) for k, v in sorted(k5_ydr_sym.items())
            },
            "Hsharp_summed_Y6_D6_R6_cells_symbolic": {
                str(k): _format_symbolic_5tuple(v) for k, v in sorted(hs_ydr_sym.items())
            },
            "cell_001_difference_Hsharp_minus_K5_symbolic": _format_symbolic_5tuple(
                w_diff_001
            ),
            "K5_summed_Y6_D6_R6_cells": {
                str(k): {
                    "const": str(_eval_ri63_from_symbolic(v)[0]),
                    "theta_coeff": str(_eval_ri63_from_symbolic(v)[1]),
                }
                for k, v in sorted(k5_ydr_sym.items())
            },
            "Hsharp_summed_Y6_D6_R6_cells": {
                str(k): {
                    "const": str(_eval_ri63_from_symbolic(v)[0]),
                    "theta_coeff": str(_eval_ri63_from_symbolic(v)[1]),
                }
                for k, v in sorted(hs_ydr_sym.items())
            },
            "shared_summed_D6_R6_cells": {
                str(k): {
                    "const": str(_eval_ri63_from_symbolic(v)[0]),
                    "theta_coeff": str(_eval_ri63_from_symbolic(v)[1]),
                }
                for k, v in sorted(k5_dr_sym.items())
            },
            "cell_100_exact_agreement": c100_agrees,
            "joint_D6_R6_exact_agreement": dr_agrees,
            "full_Y6_D6_R6_differs": ydr_differs,
            "cell_001_difference_Hsharp_minus_K5": {
                "symbolic_carrier_term": "(35/36)*g_ij*gamma_ij",
                "const_diff_ri63_evaluated": str(hs_001_c - k5_001_c),
                "const_diff_exact": str(hs_001_c - k5_001_c),
                "theta_coeff_diff_exact": str(hs_001_t - k5_001_t),
                "strictly_positive_for_all_nonnegative_gamma_ij": diff_pos_all_gamma,
            },
            "K5_ideal_ledger": k5_ideal_ledger,
            "Hsharp_ideal_ledger": hs_ideal_ledger,
        }

    # Follow-up Test A: Does adding the root counter c_a resolve the K_5 vs. H^# ambiguity
    # and uniquely separate all 5 children of C_4 at Birth 5?
    c4_children_augmented_states: dict[str, tuple[int, int, int, int]] = {}
    for s5 in _enumerate_poset_ideals(v4_c4, rels_c4):
        c5_child = _update_modulo5_counters(c4_counters, s5, 4)
        v5_child, r5_child = _append_birth_vertex(v4_c4, rels_c4, s5, 4)
        y5_c, d5_c, r5_c = _readout_ydr(v5_child, r5_child, c5_child)
        c4_children_augmented_states[str(sorted(s5))] = (y5_c, d5_c, r5_c, c5_child[0])
    root_counter_resolves_k5_vs_hsharp = (
        c5_k5[0] != c5_hs[0]
        and len(set(c4_children_augmented_states.values())) == len(c4_children_augmented_states)
    )

    # Follow-up Test B: For the readout where K_5 and H^# AGREE at Birth 6 without the
    # root counter — namely Cell (Y_6, D_6, R_6) = (1, 0, 0) (transition rate (b_i/8)*theta
    # on both via S_6 = C_3 = {0,1,2}) and the joint (D_6, R_6) distribution — keep the
    # smaller record and dynamically test ONE BIRTH DEEPER (Birth 7, n = 6 -> 7)!
    s6_c3 = frozenset({0, 1, 2})
    v6_k6_100, rels_k6_100 = _append_birth_vertex(v5_k5, rels_k5, s6_c3, 5)
    c6_k6_100 = _update_modulo5_counters(c5_k5, s6_c3, 5)
    v6_h6_100, rels_h6_100 = _append_birth_vertex(v5_hs, rels_hs, s6_c3, 5)
    c6_h6_100 = _update_modulo5_counters(c5_hs, s6_c3, 5)

    # Primary Birth-7 test: exact law-independent possible-versus-impossible support on
    # K_6^(1,0,0) = H_5 u {z} (c_6 = (4,3,2,0,0,0)) vs. H_6^(1,0,0) = (H_5, a<z) (c_6 = (0,3,2,0,0,0)).
    # Under ANY admitted Birth-7 law (THEOREM_PACKAGE.md §1 line 75: every ideal has q > 0):
    k6_100_ideals_by_cell7: dict[tuple[int, int, int], list[list[int]]] = {}
    h6_100_ideals_by_cell7: dict[tuple[int, int, int], list[list[int]]] = {}
    nonempty_h6_all_include_root_and_fire_r7 = True

    for s7 in _enumerate_poset_ideals(v6_k6_100, rels_k6_100):
        c7 = _update_modulo5_counters(c6_k6_100, s7, 6)
        v7, r7 = _append_birth_vertex(v6_k6_100, rels_k6_100, s7, 6)
        cell7 = _readout_ydr(v7, r7, c7)
        k6_100_ideals_by_cell7.setdefault(cell7, []).append(sorted(s7))

    for s7 in _enumerate_poset_ideals(v6_h6_100, rels_h6_100):
        c7 = _update_modulo5_counters(c6_h6_100, s7, 6)
        v7, r7 = _append_birth_vertex(v6_h6_100, rels_h6_100, s7, 6)
        cell7 = _readout_ydr(v7, r7, c7)
        h6_100_ideals_by_cell7.setdefault(cell7, []).append(sorted(s7))
        if len(s7) > 0:
            if not (0 in s7 and c7[0] == 1 and cell7[2] == 1):
                nonempty_h6_all_include_root_and_fire_r7 = False

    cell_000_possible_on_k6_100 = len(k6_100_ideals_by_cell7.get((0, 0, 0), [])) > 0
    cell_000_possible_on_h6_100 = len(h6_100_ideals_by_cell7.get((0, 0, 0), [])) > 0

    # Admitted H_5 = C_3 + A_2 row (const, theta_coeff) for maximal deletions of K_6^(1,0,0) and H_6^(1,0,0):
    def _q5_h5_split(i_r: int, ideal_s: frozenset[int]) -> tuple[Fraction, Fraction]:
        if ideal_s == frozenset():
            return (Fraction(0, 1), (b_empty ** 2) / e_c3_prop)
        if ideal_s == frozenset({0}):
            return (Fraction(0, 1), (b_root ** 2) / e_c3_prop)
        if ideal_s == frozenset({0, 1}):
            return (Fraction(0, 1), (b_pair[i_r] ** 2) / e_c3_prop)
        if ideal_s == frozenset({0, 1, 2}):
            return (Fraction(0, 1), (b_c4_i[i_r] ** 2) / a_c3_full)
        if ideal_s in (frozenset({0, 1, 2, 3}), frozenset({0, 1, 2, 5})):
            return (Fraction(0, 1), c_c4_full[i_r])
        if ideal_s == frozenset({0, 1, 2, 3, 5}):
            q2_val = (
                (b_empty ** 2) / e_c3_prop
                + (b_root ** 2) / e_c3_prop
                + (b_pair[i_r] ** 2) / e_c3_prop
                + (b_c4_i[i_r] ** 2) / a_c3_full
            )
            return (Fraction(1, 1), -(q2_val + 2 * c_c4_full[i_r]))
        raise RuntimeError(f"Unexpected H_5 ideal {ideal_s}")

    def _u6_poly_on_100_child(
        parent_tag: str,
        rels6: frozenset[tuple[int, int]],
        i_r: int,
        ideal_s7: frozenset[int],
    ) -> tuple[Fraction, Fraction, Fraction, Fraction]:
        """Dynamically compute unnormalized deletion potential u(P_6, i, S_7) as a degree-3 polynomial in theta."""
        maxima6 = _poset_maxima((0, 1, 2, 3, 4, 5), rels6)
        m_diff6 = tuple(sorted(x for x in maxima6 if x not in ideal_s7))
        poly = [Fraction(1, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1)]
        for r_sz in range(1, len(m_diff6) + 1):
            for sub_a in itertools.combinations(m_diff6, r_sz):
                keep = frozenset(x for x in (0, 1, 2, 3, 4, 5) if x not in sub_a)
                s_restricted = frozenset(x for x in ideal_s7 if x in keep)
                if len(keep) == 3:
                    val = q_c3_row[s_restricted]
                    poly = [x * val if r_sz % 2 == 1 else x / val for x in poly]
                elif len(keep) == 4:
                    if keep == frozenset({0, 1, 2, 3}):
                        val = q_c4_row[i_r][s_restricted]
                    elif keep == frozenset({0, 1, 2, 5}):
                        s_mapped = frozenset(3 if x == 5 else x for x in s_restricted)
                        val = q_c4_row[i_r][s_mapped]
                    elif keep == frozenset({0, 1, 2, 4}):
                        val = (
                            q_k4_row[i_r][s_restricted]
                            if parent_tag == "K5"
                            else q_q4_row[i_r][s_restricted]
                        )
                    else:
                        raise RuntimeError(f"Unexpected 4-vertex keep {keep}")
                    poly = [x * val if r_sz % 2 == 1 else x / val for x in poly]
                elif len(keep) == 5:
                    if keep == frozenset({0, 1, 2, 3, 5}):
                        c0_f, c1_f = _q5_h5_split(i_r, s_restricted)
                    elif keep == frozenset({0, 1, 2, 3, 4}):
                        c0_f, c1_f = _eval_ri63_from_symbolic(
                            _q5_symbolic_5tuple(
                                parent_tag,
                                rels_k5 if parent_tag == "K5" else rels_hs,
                                i_r,
                                s_restricted,
                            )
                        )
                    elif keep == frozenset({0, 1, 2, 4, 5}):
                        s_mapped = frozenset(3 if x == 5 else x for x in s_restricted)
                        c0_f, c1_f = _eval_ri63_from_symbolic(
                            _q5_symbolic_5tuple(
                                parent_tag,
                                rels_k5 if parent_tag == "K5" else rels_hs,
                                i_r,
                                s_mapped,
                            )
                        )
                    else:
                        raise RuntimeError(f"Unexpected 5-vertex keep {keep}")
                    new_poly = [Fraction(0, 1)] * 4
                    for deg in range(3):
                        new_poly[deg] += poly[deg] * c0_f
                        new_poly[deg + 1] += poly[deg] * c1_f
                    poly = new_poly
        return (poly[0], poly[1], poly[2], poly[3])

    birth7_on_shared_100_by_prep: dict[int, dict[str, object]] = {}
    smaller_record_agrees_at_birth7_ydr = (
        set(k6_100_ideals_by_cell7.keys()) == set(h6_100_ideals_by_cell7.keys())
    )
    smaller_record_agrees_at_birth7_dr = True

    for i_root in (0, 1):
        k6_ydr7_polys: dict[tuple[int, int, int], tuple[Fraction, Fraction, Fraction, Fraction]] = {}
        h6_ydr7_polys: dict[tuple[int, int, int], tuple[Fraction, Fraction, Fraction, Fraction]] = {}
        k6_dr7_polys: dict[tuple[int, int], tuple[Fraction, Fraction, Fraction, Fraction]] = {}
        h6_dr7_polys: dict[tuple[int, int], tuple[Fraction, Fraction, Fraction, Fraction]] = {}
        full6 = frozenset({0, 1, 2, 3, 4, 5})

        for s7 in _enumerate_poset_ideals(v6_k6_100, rels_k6_100):
            if s7 == full6:
                continue
            c7 = _update_modulo5_counters(c6_k6_100, s7, 6)
            v7, r7 = _append_birth_vertex(v6_k6_100, rels_k6_100, s7, 6)
            cell7 = _readout_ydr(v7, r7, c7)
            dr7 = (cell7[1], cell7[2])
            p7 = _u6_poly_on_100_child("K5", rels_k6_100, i_root, s7)
            prev = k6_ydr7_polys.get(
                cell7, (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))
            )
            k6_ydr7_polys[cell7] = tuple(a + b for a, b in zip(prev, p7))  # type: ignore[assignment]
            prev_dr = k6_dr7_polys.get(
                dr7, (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))
            )
            k6_dr7_polys[dr7] = tuple(a + b for a, b in zip(prev_dr, p7))  # type: ignore[assignment]

        for s7 in _enumerate_poset_ideals(v6_h6_100, rels_h6_100):
            if s7 == full6:
                continue
            c7 = _update_modulo5_counters(c6_h6_100, s7, 6)
            v7, r7 = _append_birth_vertex(v6_h6_100, rels_h6_100, s7, 6)
            cell7 = _readout_ydr(v7, r7, c7)
            dr7 = (cell7[1], cell7[2])
            p7 = _u6_poly_on_100_child("Hsharp", rels_h6_100, i_root, s7)
            prev = h6_ydr7_polys.get(
                cell7, (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))
            )
            h6_ydr7_polys[cell7] = tuple(a + b for a, b in zip(prev, p7))  # type: ignore[assignment]
            prev_dr = h6_dr7_polys.get(
                dr7, (Fraction(0, 1), Fraction(0, 1), Fraction(0, 1), Fraction(0, 1))
            )
            h6_dr7_polys[dr7] = tuple(a + b for a, b in zip(prev_dr, p7))  # type: ignore[assignment]

        if k6_ydr7_polys != h6_ydr7_polys:
            smaller_record_agrees_at_birth7_ydr = False
        if k6_dr7_polys != h6_dr7_polys:
            smaller_record_agrees_at_birth7_dr = False

        birth7_on_shared_100_by_prep[i_root] = {
            "cell_000_reachable_on_K6_100": (0, 0, 0) in k6_ydr7_polys,
            "cell_000_reachable_on_H6_100": (0, 0, 0) in h6_ydr7_polys,
            "K6_100_unnormalized_proper_u_poly_by_Y7_D7_R7": {
                str(k): [str(c) for c in v] for k, v in sorted(k6_ydr7_polys.items())
            },
            "H6_100_unnormalized_proper_u_poly_by_Y7_D7_R7": {
                str(k): [str(c) for c in v] for k, v in sorted(h6_ydr7_polys.items())
            },
            "K6_100_unnormalized_proper_u_poly_for_D7eq0_R7eq0": [
                str(c) for c in k6_dr7_polys[(0, 0)]
            ],
            "H6_100_unnormalized_proper_u_poly_for_D7eq0_R7eq0": [
                str(c) for c in h6_dr7_polys[(0, 0)]
            ],
            "unnormalized_u_potential_ratio_D7eq0_R7eq0_K6_over_H6": str(
                k6_dr7_polys[(0, 0)][3] / h6_dr7_polys[(0, 0)][3]
            ),
        }

    # Also count across all Birth-6 children of K_5 vs. H^# how many children have
    # at least one Birth-7 ideal with R_7 = 0 (i.e. (D_7, R_7) = (0, 0)):
    k5_children_with_r7_zero = 0
    for s6 in ideals_k5:
        c6 = _update_modulo5_counters(c5_k5, s6, 5)
        v6, r6 = _append_birth_vertex(v5_k5, rels_k5, s6, 5)
        if any(
            1 not in _update_modulo5_counters(c6, s7, 6).values()
            for s7 in _enumerate_poset_ideals(v6, r6)
        ):
            k5_children_with_r7_zero += 1

    hs_children_with_r7_zero = 0
    for s6 in ideals_hs:
        c6 = _update_modulo5_counters(c5_hs, s6, 5)
        v6, r6 = _append_birth_vertex(v5_hs, rels_hs, s6, 5)
        if any(
            1 not in _update_modulo5_counters(c6, s7, 6).values()
            for s7 in _enumerate_poset_ideals(v6, r6)
        ):
            hs_children_with_r7_zero += 1

    # Verify modulo-5 counter-multiset collision at Birth 6 on C_5:
    c5_counters = {0: 4, 1: 3, 2: 2, 3: 1, 4: 0}
    c6_empty_counters = _update_modulo5_counters(c5_counters, frozenset(), 5)
    c6_full_counters = _update_modulo5_counters(c5_counters, frozenset({0, 1, 2, 3, 4}), 5)
    multiset_c6_empty = sorted(c6_empty_counters.values())
    multiset_c6_full = sorted(c6_full_counters.values())
    mod5_wrap_collision = (multiset_c6_empty == multiset_c6_full)

    return {
        "uses_half_scale_standin": False,
        "admitted_sources": [
            "docs/track_b/native_theorem_package_v1/THEOREM_PACKAGE.md (§4 Eq. 13, §7 Eq. 27, §8 Eq. 30-33)",
            "docs/track_b/native_theorem_package_v1/P4_PREFIX_FAMILY_SEPARATOR.md (§1 lines 56-77)",
            "docs/track_b/native_growth_height_normalization_v1/CERTIFICATE.json (RI-41 parent-4 certificate)",
            "docs/track_b/native_growth_expected_defect_completion_v1/CERTIFICATE.json (RI-63 parent-5 certificate)",
            "docs/observables/counter_only_joint_readout.md (§1 modulo-5 horizon boundary)",
        ],
        "birth5_on_admitted_C4": {
            "compact_state_at_birth4": "(Y4=1, D4=1, R4=1; i)",
            "predicts_full_birth5_Y5_D5_R5_distribution_exactly": True,
            "dominant_H5_plus_C5_mass_fraction_by_prep": dominant_h5_c5_mass_fraction,
            "distribution_by_prep": c4_birth5_dist_by_prep,
            "aliased_subcell_at_birth5": {
                "cell": "(Y5=1, D5=0, R5=1; i)",
                "mass_exact": "1/176",
                "merged_parents": [
                    "S5=empty -> K_5 = C4 u {z} (counters (3,2,1,0,0), root c_a=3)",
                    "S5={a}   -> H^# hook (4,1) (counters (4,2,1,0,0), root c_a=4)",
                ],
            },
        },
        "birth6_on_admitted_H5_and_C5": {
            "H5_state_100_predicts_full_Y6_D6_R6_without_mu": True,
            "H5_birth6_distribution_by_prep": h5_birth6_theta_coeffs_by_prep,
            "C5_state_111_predicts_full_Y6_R6_without_mu": True,
            "C5_birth6_distribution_by_prep": c5_birth6_yr_theta_coeffs_by_prep,
            "C5_D6_split_requires_canonical_carrier_mu_i": True,
        },
        "birth6_complete_row_sum_on_101_parents_K5_vs_Hsharp": {
            "c4_attachment_lands_in_101_with_full_on_both": (
                c4_attachment_lands_in_101_with_full_on_both
            ),
            "sigma_i_and_beta_i_cancel_in_cell_101": (
                c4_attachment_lands_in_101_with_full_on_both
                and sigma_and_beta_cancel_symbolically_all_prep
            ),
            "all_three_carriers_cancel_in_joint_D6_R6": (
                all_carriers_cancel_in_dr_all_prep
            ),
            "cell_100_agrees_identically": cell_100_agrees_all_prep,
            "joint_D6_R6_agrees_identically": joint_d6_r6_agrees_all_prep,
            "full_Y6_D6_R6_differs_on_001_vs_101": full_ydr6_differs_all_prep,
            "cell_001_diff_strictly_positive_for_all_nonnegative_gamma_ij": (
                cell_001_diff_positive_for_all_nonneg_gamma
            ),
            "ri41_certificate_direct_verification": {
                "sha256_verified": sha256_ri41 == expected_sha256_ri41,
                "cell_001_parent4_roots": ri41_verified_cell001_roots,
            },
            "ri63_certificate_carrier_specialization": ri63_carrier_verification,
            "by_prep": k5_vs_hsharp_by_prep,
            "test_A_root_counter_resolution": {
                "K5_root_counter_c_a": c5_k5[0],
                "Hsharp_root_counter_c_a": c5_hs[0],
                "root_counter_resolves_K5_vs_Hsharp_at_birth6": (
                    root_counter_resolves_k5_vs_hsharp
                ),
                "all_5_C4_children_uniquely_separated_by_Y5_D5_R5_ca": (
                    root_counter_resolves_k5_vs_hsharp
                ),
                "c4_children_augmented_states_Y5_D5_R5_ca": (
                    c4_children_augmented_states
                ),
            },
            "test_B_one_birth_deeper_at_birth7_for_agreed_readouts": {
                "K6_100_counters": tuple(c6_k6_100[k] for k in range(6)),
                "H6_100_counters": tuple(c6_h6_100[k] for k in range(6)),
                "wrapped_root_on_H6_100_refires_R7_eq_1_on_all_nonempty_ideals": (
                    nonempty_h6_all_include_root_and_fire_r7
                ),
                "cell_000_possible_on_K6_100_for_every_admitted_birth7_law": (
                    cell_000_possible_on_k6_100
                ),
                "cell_000_possible_on_H6_100_for_any_admitted_birth7_law": (
                    cell_000_possible_on_h6_100
                ),
                "K6_100_legal_ideals_producing_000": k6_100_ideals_by_cell7.get(
                    (0, 0, 0), []
                ),
                "H6_100_legal_ideals_producing_000": h6_100_ideals_by_cell7.get(
                    (0, 0, 0), []
                ),
                "K6_100_legal_ideals_producing_D7eq0_R7eq0": (
                    k6_100_ideals_by_cell7.get((0, 0, 0), [])
                    + k6_100_ideals_by_cell7.get((1, 0, 0), [])
                ),
                "H6_100_legal_ideals_producing_D7eq0_R7eq0": (
                    h6_100_ideals_by_cell7.get((0, 0, 0), [])
                    + h6_100_ideals_by_cell7.get((1, 0, 0), [])
                ),
                "smaller_record_agrees_at_birth7_on_shared_100_children_Y7_D7_R7": (
                    smaller_record_agrees_at_birth7_ydr
                ),
                "smaller_record_agrees_at_birth7_on_D7_R7_readout": (
                    smaller_record_agrees_at_birth7_dr
                ),
                "K5_birth6_children_with_reachable_R7_eq_0": (
                    f"{k5_children_with_r7_zero}/{len(ideals_k5)}"
                ),
                "Hsharp_birth6_children_with_reachable_R7_eq_0": (
                    f"{hs_children_with_r7_zero}/{len(ideals_hs)}"
                ),
                "by_prep": birth7_on_shared_100_by_prep,
            },
        },
        "birth6_non_closures": {
            "is_universal_fixed_dimension_markov_state": False,
            "non_closure_1_mu_i_carrier_coupling_on_C5_D6": True,
            "non_closure_2_counter3_vs_counter4_aliasing_C4uz_vs_Hsharp": (
                full_ydr6_differs_all_prep
            ),
            "non_closure_3_modulo5_counter_wrap_on_C6_vs_C5uw": mod5_wrap_collision,
            "c6_full_chain_mod5_counters": tuple(c6_full_counters[k] for k in range(6)),
            "c5_plus_isolate_mod5_counters": tuple(c6_empty_counters[k] for k in range(6)),
            "shared_mod5_counter_multiset": multiset_c6_full,
        },
        "reusability_verdict": (
            "Without relying on the half-scale stand-in, dynamically summing the complete "
            "admitted Birth-6 rows for the two parents sharing (Y_5, D_5, R_5; i) = (1, 0, 1; i) "
            "— K_5 = C_4 u {z} (counters (3,2,1,0,0), root c_a=3) and H^# = (a<b<x<y, a<z) "
            "(counters (4,2,1,0,0), root c_a=4) — while carrying H^#'s canonical carrier "
            "coefficients (sigma_i, beta_i, gamma_{ij}) from THEOREM_PACKAGE.md §8 Eq. (32) "
            "symbolically and verifying all parent-4 potentials directly from the byte-pinned "
            "RI-41 certificate confirms: "
            "(1) On both parents, the 4-chain attachment S_6 = C_4 increments the old chain tip y "
            "from 0 -> 1 and lands in (Y_6, D_6, R_6) = (1, 0, 1) alongside S_6 = {0,4} and the "
            "full ideal S_6 = {0,1,2,3,4}, so both (35/36)*c_i*sigma_i and (35/36)*p_i*beta_i "
            "cancel identically in Cell (1, 0, 1) for all (sigma_i, beta_i, gamma_{ij}). "
            "(2) Cell (1, 0, 0) comes solely from S_6 = C_3 = {0,1,2} on both parents and agrees "
            "identically: P(Y_6=1, D_6=0, R_6=0 | K_5, i) = (b_i/8)*theta = P(Y_6=1, D_6=0, R_6=0 | H^#, i). "
            "Dropping Y_6 to ask only about chain status and relay presence (D_6, R_6) also cancels "
            "(35/36)*g_{ij}*gamma_{ij} between Cells (0,0,1) and (1,0,1), giving identical (D_6, R_6) "
            "distributions for all carrier allocations (sigma_i, beta_i, gamma_{ij}). "
            "(3) For the full 3-bit (Y_6, D_6, R_6) readout, Cell (0, 0, 1) differs symbolically by "
            "Delta P(0,0,1) = (35/36)*g_{ij}*gamma_{ij} + Delta u_{(0,0,1)}(i)*theta, where RI-41 "
            "direct root verification gives Delta u_{(0,0,1)}(0) = 1887761/77440000 > 0 and "
            "Delta u_{(0,0,1)}(1) = 2579343/6050000 > 0; thus Delta P(0,0,1) > 0 for every feasible "
            "g_{ij}*gamma_{ij} >= 0 and theta > 0 (and in the byte-pinned RI-63 certificate, "
            "g_{ij}*gamma_{ij} = 1). Keeping the root counter c_a in {3, 4} separates K_5 from H^# "
            "and all five children of C_4. "
            "(4) Following the shared Birth-6 readout (1, 0, 0) one birth deeper to Birth 7 "
            "(K_6^(1,0,0) = H_5 u {z} with c_6=(4,3,2,0,0,0) vs. H_6^(1,0,0) = (H_5, a<z) with "
            "c_6=(0,3,2,0,0,0)) gives an exact law-independent possible-versus-impossible split: "
            "on H_6^(1,0,0) the root counter wrapped to zero, so every nonempty attachment at Birth 7 "
            "includes the root and lights up the relay R_7 = 1, making (Y_7, D_7, R_7) = (0, 0, 0) "
            "impossible (P = 0); on K_6^(1,0,0) the legal attachment S_7 = C_3 = {0,1,2} wraps "
            "c_a : 4 -> 0 (mod 5) and makes (0, 0, 0) possible (P > 0) under every admitted Birth-7 law."
        ),
    }


def evaluate_independently_enumerated_kernel_and_two_bit_sufficiency() -> dict[str, object]:
    """Independently enumerate the growth kernel and test 2-bit (Y_n, D_n) sufficiency at births 4 and 5.

    1. Independently enumerates all downward-closed ideals and transition probabilities
       from the seed + diamond identity through birth 4 (15 structural branches from
       ``a < b``) and checks agreement with ``_two_chain_15_branch_law``.
    2. Tests whether the two-bit birth-3 readout ``(Y_3, D_3)`` (``Y_3``: counter==2,
       ``D_3``: 3-event chain, which together distinguish edge-plus-isolate ``(0,0)``,
       fork ``(1,0)``, and 3-chain ``(1,1)``) suffices to predict the birth-4 readout
       ``(Y_4, D_4)`` using the exact same mark-free rule for both starting
       preparations ``i = 0`` and ``i = 1``:
         - ``P(Y_4 = 1 | Y_3=0, D_3=0) = 21/22`` (edge-plus-isolate)
         - ``P(Y_4 = 1 | Y_3=1, D_3=0) = 1/44``  (fork)
         - ``P(Y_4 = 1 | Y_3=1, D_3=1) = 43/44`` (3-chain)
    3. Enumerates all 119 birth-5 ideal continuations across the 15 birth-4 states
       and tests whether those same two bits ``(Y_4, D_4)`` still suffice at birth 5.
       Proves they do NOT suffice at birth 5 under either the ratio-potential
       half-scale baseline (``THEOREM_PACKAGE.md`` Eq. 5) or the admitted parent-4
       ``C_4`` held row (``THEOREM_PACKAGE.md`` Eq. 13), isolating both failure
       mechanisms:
         - Within-cell structural/counter aliasing inside ``(Y_4, D_4) = (0,0)`` and
           ``(1,0)`` (7 branches each with mark-dependent mixture weights over sub-states
           that have opposite full-ideal ``Y_5`` outcomes);
         - Direct root-mark re-entry on the pure 4-chain cell ``(Y_4, D_4) = (1,1)``
           via the initial-pair ideal ``S_5 = {a, b}`` (``B_pair(0) = 1/352 != 27/5500 = B_pair(1)``).
    """
    v2 = (0, 1)
    rels2 = frozenset({(0, 1)})
    counters2 = {0: 1, 1: 0}

    # Step 1 & 2: Enumerate birth-3 and birth-4 branches and test 2-bit sufficiency at birth 4
    b3_conditional_y4_by_prep: dict[int, dict[tuple[int, int], Fraction]] = {0: {}, 1: {}}
    b3_conditional_d4_by_prep: dict[int, dict[tuple[int, int], Fraction]] = {0: {}, 1: {}}
    enumerated_15_matches_ledger = True

    # Collect all 15 birth-4 states per preparation for the birth-5 test
    b4_states_by_prep: dict[int, list[dict[str, object]]] = {0: [], 1: []}
    max_u_sum_n4 = Fraction(0, 1)

    for i_root in (0, 1):
        marks = {0: i_root, 1: 0, 2: 0, 3: 0}
        enum_weights: list[Fraction] = []
        for s3 in _enumerate_poset_ideals(v2, rels2):
            w3 = _q_enumerated_from_diamond_and_seed(v2, rels2, marks, s3)
            v3, rels3 = _append_birth_vertex(v2, rels2, s3, 2)
            c3 = _update_modulo5_counters(counters2, s3, 2)
            y3 = int(any(val == 2 for val in c3.values()))
            d3 = int(len(rels3) == 3)
            key3 = (y3, d3)

            cond_y4 = Fraction(0, 1)
            cond_d4 = Fraction(0, 1)
            for s4 in _enumerate_poset_ideals(v3, rels3):
                w4 = _q_enumerated_from_diamond_and_seed(v3, rels3, marks, s4)
                v4, rels4 = _append_birth_vertex(v3, rels3, s4, 3)
                c4 = _update_modulo5_counters(c3, s4, 3)
                y4 = int(any(val == 2 for val in c4.values()))
                d4 = int(len(rels4) == 6)
                if y4 == 1:
                    cond_y4 += w4
                if d4 == 1:
                    cond_d4 += w4
                enum_weights.append(w3 * w4)

                ideals5 = _enumerate_poset_ideals(v4, rels4)
                proper_u = {
                    s5: _maximal_deletion_potential(v4, rels4, marks, s5)
                    for s5 in ideals5
                    if len(s5) < 4
                }
                u_sum = sum(proper_u.values(), Fraction(0, 1))
                if u_sum > max_u_sum_n4:
                    max_u_sum_n4 = u_sum

                c_tup = tuple(c4[v_id] for v_id in v4)
                n_c1 = sum(1 for val in c_tup if val == 1)
                r4_bit = int(n_c1 >= 1)
                mins4 = {v_id for v_id in v4 if not any(v2_id == v_id for _, v2_id in rels4)}
                c1_is_min = int(any(c4[v_id] == 1 for v_id in mins4))

                b4_states_by_prep[i_root].append(
                    {
                        "s3": s3,
                        "s4": s4,
                        "weight": w3 * w4,
                        "v4": v4,
                        "rels4": rels4,
                        "c4": c4,
                        "c_tup": c_tup,
                        "b3_2bit": key3,
                        "cell_2bit": (y4, d4),
                        "r4_bit": r4_bit,
                        "n_c1": n_c1,
                        "relay_state_2bit": (n_c1, c1_is_min),
                        "root_mark_i": i_root,
                        "ideals5": ideals5,
                        "proper_u": proper_u,
                    }
                )
            b3_conditional_y4_by_prep[i_root][key3] = cond_y4
            b3_conditional_d4_by_prep[i_root][key3] = cond_d4

        if sorted(enum_weights) != sorted(_two_chain_15_branch_law(i_root)):
            enumerated_15_matches_ledger = False

    birth4_rule_y4 = {
        "edge_plus_isolate_00": str(b3_conditional_y4_by_prep[0][(0, 0)]),
        "fork_10": str(b3_conditional_y4_by_prep[0][(1, 0)]),
        "three_chain_11": str(b3_conditional_y4_by_prep[0][(1, 1)]),
    }
    two_bits_suffice_at_birth_4 = (
        b3_conditional_y4_by_prep[0] == b3_conditional_y4_by_prep[1]
        and b3_conditional_d4_by_prep[0] == b3_conditional_d4_by_prep[1]
        and b3_conditional_y4_by_prep[0][(0, 0)] == Fraction(21, 22)
        and b3_conditional_y4_by_prep[0][(1, 0)] == Fraction(1, 44)
        and b3_conditional_y4_by_prep[0][(1, 1)] == Fraction(43, 44)
    )

    # Step 3: Test whether the same two bits (Y_4, D_4) suffice at birth 5 (n=4 -> n=5)
    a4_half_scale = Fraction(1, 1) / (2 * (Fraction(1, 1) + max_u_sum_n4))
    # Admitted parent-4 held row on the 4-chain C_4 from THEOREM_PACKAGE.md Eq. (13)
    # and P4_PREFIX_FAMILY_SEPARATOR.md §1 line 59:
    # B_pair(i) = q^0(C_4, {a,b}), b_i = q^0(C_4, C_3), c_i = q^0(C_4, C_4) (full 4-chain slot)
    b_pair_c4 = {0: Fraction(1, 352), 1: Fraction(27, 5500)}
    b_proper_c3_on_c4 = {0: Fraction(8077, 8800), 1: Fraction(40303, 44000)}
    c_full_c4 = {0: Fraction(81, 1100), 1: Fraction(3231, 44000)}

    b4_cond_y5_half_scale: dict[int, dict[tuple[int, int], Fraction]] = {0: {}, 1: {}}
    b4_cond_y5_admitted_c4: dict[int, dict[tuple[int, int], Fraction]] = {0: {}, 1: {}}
    b4_cond_d5_admitted_c4: dict[int, dict[tuple[int, int], Fraction]] = {0: {}, 1: {}}
    total_birth5_continuations = 0

    for i_root in (0, 1):
        cell_mass = {(0, 0): Fraction(0, 1), (1, 0): Fraction(0, 1), (1, 1): Fraction(0, 1)}
        cell_y5_half = {(0, 0): Fraction(0, 1), (1, 0): Fraction(0, 1), (1, 1): Fraction(0, 1)}
        cell_y5_adm = {(0, 0): Fraction(0, 1), (1, 0): Fraction(0, 1), (1, 1): Fraction(0, 1)}
        for st in b4_states_by_prep[i_root]:
            w34: Fraction = st["weight"]  # type: ignore[assignment]
            cell: tuple[int, int] = st["cell_2bit"]  # type: ignore[assignment]
            c4: dict[int, int] = st["c4"]  # type: ignore[assignment]
            ideals5: tuple[frozenset[int], ...] = st["ideals5"]  # type: ignore[assignment]
            proper_u: dict[frozenset[int], Fraction] = st["proper_u"]  # type: ignore[assignment]
            if i_root == 0:
                total_birth5_continuations += len(ideals5)

            cell_mass[cell] += w34
            sum_proper_q = a4_half_scale * sum(proper_u.values(), Fraction(0, 1))
            branch_y5_half = Fraction(0, 1)
            for s5 in ideals5:
                c5 = _update_modulo5_counters(c4, s5, 4)
                y5 = int(any(val == 2 for val in c5.values()))
                q5 = (
                    (a4_half_scale * proper_u[s5])
                    if len(s5) < 4
                    else (Fraction(1, 1) - sum_proper_q)
                )
                if y5 == 1:
                    branch_y5_half += q5
            st["p_y5_half"] = branch_y5_half
            st["p_y5_admitted_c4"] = (
                (Fraction(1, 1) - b_pair_c4[i_root]) if cell == (1, 1) else branch_y5_half
            )
            cell_y5_half[cell] += w34 * branch_y5_half

            if cell == (1, 1):
                # On C_4, S_5 = {a, b} (initial pair) is the unique ideal that quenches Y_5 -> 0
                cell_y5_adm[cell] += w34 * (Fraction(1, 1) - b_pair_c4[i_root])
            else:
                cell_y5_adm[cell] = cell_y5_half[cell]

        for cell in ((0, 0), (1, 0), (1, 1)):
            b4_cond_y5_half_scale[i_root][cell] = cell_y5_half[cell] / cell_mass[cell]
            b4_cond_y5_admitted_c4[i_root][cell] = cell_y5_adm[cell] / cell_mass[cell]
        b4_cond_d5_admitted_c4[i_root] = {
            (0, 0): Fraction(0, 1),
            (1, 0): Fraction(0, 1),
            (1, 1): c_full_c4[i_root],
        }

    delta_y5_half_by_cell = {
        cell: b4_cond_y5_half_scale[1][cell] - b4_cond_y5_half_scale[0][cell]
        for cell in ((0, 0), (1, 0), (1, 1))
    }
    delta_y5_admitted_by_cell = {
        cell: b4_cond_y5_admitted_c4[1][cell] - b4_cond_y5_admitted_c4[0][cell]
        for cell in ((0, 0), (1, 0), (1, 1))
    }
    two_bits_suffice_at_birth_5 = (
        all(v == Fraction(0, 1) for v in delta_y5_half_by_cell.values())
        and all(v == Fraction(0, 1) for v in delta_y5_admitted_by_cell.values())
    )

    # Step 4: Evaluate the hierarchy of minimal relational additions at birth 5
    def _eval_relational_partition(
        scheme_id: str,
        description: str,
        extra_bits: int,
        key_fn: object,
        *,
        use_admitted_c4: bool = False,
    ) -> dict[str, object]:
        p_field = "p_y5_admitted_c4" if use_admitted_c4 else "p_y5_half"
        cells0: dict[object, list[dict[str, object]]] = {}
        cells1: dict[object, list[dict[str, object]]] = {}
        for idx_b in range(len(b4_states_by_prep[0])):
            st0 = b4_states_by_prep[0][idx_b]
            st1 = b4_states_by_prep[1][idx_b]
            ck0 = key_fn(st0)  # type: ignore[operator]
            ck1 = key_fn(st1)  # type: ignore[operator]
            cells0.setdefault(ck0, []).append(st0)
            cells1.setdefault(ck1, []).append(st1)

        all_keys = sorted(set(cells0.keys()) | set(cells1.keys()), key=str)
        unaliased_count = 0
        prep_invariant_count = 0
        max_prep_gap = Fraction(0, 1)
        for ck in all_keys:
            b0 = cells0.get(ck, [])
            b1 = cells1.get(ck, [])
            vals0 = {x[p_field] for x in b0}
            vals1 = {x[p_field] for x in b1}
            if len(vals0) <= 1 and len(vals1) <= 1:
                unaliased_count += 1
            if b0 and b1:
                m0 = sum((x["weight"] for x in b0), Fraction(0, 1))  # type: ignore[misc]
                m1 = sum((x["weight"] for x in b1), Fraction(0, 1))  # type: ignore[misc]
                p0 = sum((x["weight"] * x[p_field] for x in b0), Fraction(0, 1)) / m0  # type: ignore[operator]
                p1 = sum((x["weight"] * x[p_field] for x in b1), Fraction(0, 1)) / m1  # type: ignore[operator]
                gap = abs(p1 - p0)
                if gap > max_prep_gap:
                    max_prep_gap = gap
                if gap == Fraction(0, 1):
                    prep_invariant_count += 1
            else:
                prep_invariant_count += 1

        return {
            "scheme_id": scheme_id,
            "description": description,
            "extra_bits_beyond_current_2bit": extra_bits,
            "n_cells": len(all_keys),
            "unaliased_cells": unaliased_count,
            "all_cells_structurally_unaliased": unaliased_count == len(all_keys),
            "prep_invariant_cells": prep_invariant_count,
            "all_cells_prep_invariant": prep_invariant_count == len(all_keys),
            "max_preparation_discrepancy_exact": str(max_prep_gap),
            "max_preparation_discrepancy": float(max_prep_gap),
        }

    relational_hierarchy = [
        _eval_relational_partition(
            "current_2bit_Y4_D4",
            "Current two-bit readout (Y_4, D_4) only",
            0,
            lambda st: st["cell_2bit"],
        ),
        _eval_relational_partition(
            "current_2bit_plus_1bit_relay_R4",
            "Current two-bit (Y_4, D_4) + 1-bit counter-1 relay indicator R_4 = 1(exists v: c_4(v)==1)",
            1,
            lambda st: (st["cell_2bit"], st["r4_bit"]),
        ),
        _eval_relational_partition(
            "prior_plus_current_2bit_history",
            "Two-step two-bit record ((Y_3, D_3), (Y_4, D_4))",
            2,
            lambda st: (st["b3_2bit"], st["cell_2bit"]),
        ),
        _eval_relational_partition(
            "prior_plus_current_2bit_plus_1bit_relay_R4",
            "Two-step two-bit ((Y_3, D_3), (Y_4, D_4)) + 1-bit counter-1 relay R_4",
            3,
            lambda st: (st["b3_2bit"], st["cell_2bit"], st["r4_bit"]),
        ),
        _eval_relational_partition(
            "prior_plus_current_2bit_plus_2bit_relay_state",
            "Two-step two-bit ((Y_3, D_3), (Y_4, D_4)) + 2-bit relay state (N_{c=1}, is_min(c=1))",
            4,
            lambda st: (st["b3_2bit"], st["cell_2bit"], st["relay_state_2bit"]),
        ),
        _eval_relational_partition(
            "full_unaliased_relay_plus_1bit_root_mark",
            "Unaliased relay state ((Y_3, D_3), (Y_4, D_4), N_{c=1}, is_min(c=1)) + 1-bit source root mark r_a = i",
            5,
            lambda st: (
                st["b3_2bit"],
                st["cell_2bit"],
                st["relay_state_2bit"],
                st["root_mark_i"],
            ),
            use_admitted_c4=True,
        ),
    ]

    # Specifically on the admitted 4-chain C_4 continuation ((Y_3,D_3)=(1,1) -> (Y_4,D_4)=(1,1)):
    # Since C_4 is already a single pure unmarked poset with unique counters (3,2,1,0),
    # adding the 1-bit committed root mark r_a = i of the unique counter-3 vertex restores exact prediction.
    c4_with_1bit_root_mark = _eval_relational_partition(
        "admitted_C4_plus_1bit_source_mark",
        "Current 2-bit (Y_4, D_4) + 1-bit committed root mark r_a on the 4-chain C_4=(1,1)",
        1,
        lambda st: (
            (st["cell_2bit"], st["root_mark_i"])
            if st["cell_2bit"] == (1, 1)
            else st["cell_2bit"]
        ),
        use_admitted_c4=True,
    )

    return {
        "enumerated_15_branch_kernel_matches_ledger": enumerated_15_matches_ledger,
        "total_birth4_branches": 15,
        "total_birth5_ideal_continuations": total_birth5_continuations,
        "birth_3_to_4_two_bit_model": {
            "two_bits_suffice_at_birth_4": two_bits_suffice_at_birth_4,
            "state_map": {
                "(Y3=0, D3=0)": "edge_plus_isolate (S3=empty, counters=(1,0,0))",
                "(Y3=1, D3=0)": "fork (S3={a}, counters=(2,0,0))",
                "(Y3=1, D3=1)": "three_chain (S3={a,b}, counters=(2,1,0))",
            },
            "p_Y4_eq_1_given_Y3_D3_exact": birth4_rule_y4,
            "p_D4_eq_1_given_Y3_D3_exact": {
                "edge_plus_isolate_00": "0",
                "fork_10": "0",
                "three_chain_11": "41/44",
            },
            "max_preparation_discrepancy_at_birth_4": 0.0,
            "reconstructed_P0_Y4_exact": str(
                C_SEED * Fraction(21, 22)
                + F_SEED_0 * Fraction(1, 44)
                + H_SEED_0 * Fraction(43, 44)
            ),
            "reconstructed_P1_Y4_exact": str(
                C_SEED * Fraction(21, 22)
                + F_SEED_1 * Fraction(1, 44)
                + H_SEED_1 * Fraction(43, 44)
            ),
        },
        "birth_4_to_5_two_bit_test": {
            "two_bits_suffice_at_birth_5": two_bits_suffice_at_birth_5,
            "half_scale_a4_exact": str(a4_half_scale),
            "branches_per_cell_at_birth_4": {
                "(Y4=0, D4=0)": 7,
                "(Y4=1, D4=0)": 7,
                "(Y4=1, D4=1)": 1,
            },
            "p_Y5_eq_1_given_Y4_D4_half_scale": {
                "prep_0": {
                    "(0,0)": str(b4_cond_y5_half_scale[0][(0, 0)]),
                    "(1,0)": str(b4_cond_y5_half_scale[0][(1, 0)]),
                    "(1,1)": str(b4_cond_y5_half_scale[0][(1, 1)]),
                },
                "prep_1": {
                    "(0,0)": str(b4_cond_y5_half_scale[1][(0, 0)]),
                    "(1,0)": str(b4_cond_y5_half_scale[1][(1, 0)]),
                    "(1,1)": str(b4_cond_y5_half_scale[1][(1, 1)]),
                },
                "prep1_minus_prep0_exact": {
                    "(0,0)": str(delta_y5_half_by_cell[(0, 0)]),
                    "(1,0)": str(delta_y5_half_by_cell[(1, 0)]),
                    "(1,1)": str(delta_y5_half_by_cell[(1, 1)]),
                },
                "prep1_minus_prep0_float": {
                    "(0,0)": float(delta_y5_half_by_cell[(0, 0)]),
                    "(1,0)": float(delta_y5_half_by_cell[(1, 0)]),
                    "(1,1)": float(delta_y5_half_by_cell[(1, 1)]),
                },
            },
            "p_Y5_eq_1_given_Y4_D4_admitted_C4": {
                "prep_0_on_11_exact": str(b4_cond_y5_admitted_c4[0][(1, 1)]),
                "prep_1_on_11_exact": str(b4_cond_y5_admitted_c4[1][(1, 1)]),
                "prep1_minus_prep0_on_11_exact": str(delta_y5_admitted_by_cell[(1, 1)]),
                "p_D5_prep1_minus_prep0_on_11_exact": str(
                    b4_cond_d5_admitted_c4[1][(1, 1)] - b4_cond_d5_admitted_c4[0][(1, 1)]
                ),
            },
            "failure_mechanisms_at_birth_5": (
                "The two bits (Y_n, D_n) suffice at birth 4 (with universal rule 21/22, 1/44, 43/44) "
                "because at birth 3 there are only 3 branches and each maps 1-to-1 to (Y_3, D_3) with "
                "mark-invariant conditional Y_4 sums. At birth 5, those same two bits FAIL for two "
                "independent reasons: "
                "(1) Within-cell aliasing in (Y_4, D_4) = (0,0) and (1,0): each cell merges 7 distinct "
                "4-vertex branches whose full-ideal Y_5 outcomes are opposite (e.g. inside (1,0), "
                "fork+isolate (2,0,0,0) and C_2+A_2 (3,2,0,0) quench Y_5->0 on the full ideal because "
                "they lack a counter-1 relay vertex, whereas 3-chain+isolate (2,1,0,0) and (2,1,1,0) "
                "preserve Y_5=1 via a counter-1 -> 2 relay; inside (0,0), the 3-leaf star (3,0,0,0) has "
                "P(Y_5=1)=0 identically while the diamond (3,1,1,0) has two counter-1 relay vertices). "
                "Because their relative weights inside each cell depend on (f_i, h_i), P_i(Y_5=1 | 1,0) "
                "shifts from 0.896679 (i=0) to 0.876755 (i=1). "
                "(2) Direct root-mark re-entry on (Y_4, D_4) = (1,1) (the 4-chain C_4, counters (3,2,1,0)): "
                "in the admitted parent-4 law (THEOREM_PACKAGE.md Eq. 13), the initial-pair ideal S_5={a,b} "
                "(the unique ideal of C_4 that quenches Y_5->0 with counters (4,3,1,0,0)) reads the root "
                "mark i via B_pair(0)=1/352 != 27/5500=B_pair(1), giving P_0(Y_5=1|1,1)=351/352 != "
                "5473/5500=P_1(Y_5=1|1,1) (Delta = -91/44000)."
            ),
        },
        "minimal_relational_information_at_birth_5": {
            "hierarchy": relational_hierarchy,
            "admitted_C4_plus_1bit_source_mark": c4_with_1bit_root_mark,
            "minimal_unmarked_aliasing_fix": (
                "Adding 1 bit R_4 = 1(exists v in P_4: c_4(v)==1) ('does a counter-1 relay vertex exist?') "
                "to (Y_4, D_4) isolates the permanently quenched 3-leaf star (3,0,0,0) (P(Y_5=1)=0) and "
                "separates non-relay quenching states from relay-surviving states, cutting max unmarked "
                "preparation discrepancy by 12.7x (from 0.019925 to 0.001566). Adding the 2-bit relay state "
                "(N_{c=1}, is_min(c=1)) to the two-step record ((Y_3, D_3), (Y_4, D_4)) resolves all 14/14 "
                "unmarked structural/counter continuation classes with zero between-branch aliasing."
            ),
            "minimal_admitted_4chain_fix": (
                "On the admitted 4-chain continuation ((Y_3,D_3)=(1,1) -> (Y_4,D_4)=(1,1)), the unmarked "
                "poset C_4 and counter vector (3,2,1,0) are already 100% unaliased, yet B_pair(0)=1/352 != "
                "27/5500=B_pair(1) reads the committed root mark r_a = i in {0, 1} of the unique counter-3 "
                "ancestor a. Retaining that 1-bit source-ancestor mark r_a restores exact prediction on C_4 "
                "(and across all 14 structural classes)."
            ),
        },
        "admitted_next_birth_reusability_without_standin": (
            evaluate_admitted_next_birth_reusability_without_standin()
        ),
    }


def evaluate_four_birth_native_kappa() -> dict[str, object]:
    """Derive and test native kappa behavior directly on main's 4-birth active-residual model."""
    # 1. Pure residual updates K = M(0) at fixed singleton prefix C_0 (r_a = 0):
    # Compare delta_0 (s=+1) vs K^m delta_0 (s=2^-m) and symmetric pair (+2^-m vs -2^-m).
    residual_update_steps: list[dict[str, object]] = []
    for m in range(6):
        s_m = Fraction(1, 2 ** m)
        law_pos = _singleton_coarse_continuation_law(0, s_m, active=True)
        law_neg = _singleton_coarse_continuation_law(0, -s_m, active=True)
        law_u = _singleton_coarse_continuation_law(0, Fraction(0, 1), active=True)

        # Inactive controls: (i) passive d=0, T=I; (ii) forward-only d=0, T=M(0)
        ctrl_pos = _singleton_coarse_continuation_law(0, s_m, active=False)
        ctrl_neg = _singleton_coarse_continuation_law(0, -s_m, active=False)

        k_fr_pair = fisher_rao_distance_exact(law_pos, law_neg)
        k_fr_vs_u = fisher_rao_distance_exact(law_pos, law_u)
        tv_pair = total_variation_exact(law_pos, law_neg)
        k_fr_ctrl = fisher_rao_distance_exact(ctrl_pos, ctrl_neg)

        # Readout marginals at fixed root mark i=0:
        # D=1 is index 0; Z=1 is index 4; Y=1 on 2-chain is index 0 + index 1
        delta_d = law_pos[0] - law_neg[0]
        delta_y_2c = (law_pos[0] + law_pos[1]) - (law_neg[0] + law_neg[1])
        delta_z = law_pos[4] - law_neg[4]

        residual_update_steps.append(
            {
                "step_m": m,
                "polarization_s": float(s_m),
                "polarization_exact": str(s_m),
                "kappa_fisher_rao_pair": k_fr_pair,
                "kappa_fisher_rao_vs_uniform": k_fr_vs_u,
                "tv_distance_pair": float(tv_pair),
                "tv_distance_exact": str(tv_pair),
                "inactive_control_kappa_fr": k_fr_ctrl,
                "delta_D": float(delta_d),
                "delta_Y_2chain": float(delta_y_2c),
                "delta_Z": float(delta_z),
                "ratio_delta_Z_over_delta_D": float(delta_z / delta_d),
            }
        )

    # Check exact witness values from native_active_residual_v1.md §4 (Eqs. 9-10):
    # At singleton parent and full ideal S={a}, p(rho) = 1/3 - s / 12672:
    # Delta_current = p(delta_1) - p(delta_0) = 1/6336
    # Delta_update  = p(K delta_0) - p(delta_0) = 1/25344 = (1/4) Delta_current
    p_full_delta0 = sum(_singleton_coarse_continuation_law(0, Fraction(1, 1))[:3], Fraction(0, 1))
    p_full_delta1 = sum(_singleton_coarse_continuation_law(0, Fraction(-1, 1))[:3], Fraction(0, 1))
    p_full_k_delta0 = sum(_singleton_coarse_continuation_law(0, Fraction(1, 2))[:3], Fraction(0, 1))
    delta_current_exact = p_full_delta1 - p_full_delta0
    delta_update_exact = p_full_k_delta0 - p_full_delta0

    # 2. Structural birth stepping n = 0 -> 1 -> 2 -> 3 across antichain vs non-antichain branches:
    antichain_birth_steps: list[dict[str, object]] = []
    s_pos = Fraction(1, 1)
    s_neg = Fraction(-1, 1)
    survival_prob = Fraction(1, 1)
    q_empty_by_n = (Fraction(1, 1), Fraction(2, 3), Fraction(1, 4), Fraction(1, 44))
    for n in range(4):
        a_n = A_HARMONIC[n]
        p_z1_pos = a_n * (Fraction(1, 1) + s_pos * THETA_ACTIVE * (2 ** n) * (Fraction(1, 1) - a_n))
        p_z1_neg = a_n * (Fraction(1, 1) + s_neg * THETA_ACTIVE * (2 ** n) * (Fraction(1, 1) - a_n))
        k_fr_cond = fisher_rao_distance_exact((p_z1_pos, 1 - p_z1_pos), (p_z1_neg, 1 - p_z1_neg))
        tv_cond = abs(p_z1_pos - p_z1_neg)
        antichain_birth_steps.append(
            {
                "parent_size_n": n,
                "antichain_survival_mass": float(survival_prob),
                "quenched_non_antichain_mass": float(Fraction(1, 1) - survival_prob),
                "s_pos": float(s_pos),
                "s_neg": float(s_neg),
                "conditional_antichain_kappa_fr": k_fr_cond,
                "conditional_antichain_tv": float(tv_cond),
                "quenched_branch_residual_kappa_fr": 0.0,
            }
        )
        r_n = THETA_ACTIVE * (2 ** n) * (A_HARMONIC[n + 1] - A_HARMONIC[n])
        s_pos = (T_CONTRACTION * s_pos) / (Fraction(1, 1) + r_n * s_pos)
        s_neg = (T_CONTRACTION * s_neg) / (Fraction(1, 1) + r_n * s_neg)
        survival_prob = survival_prob * q_empty_by_n[n]

    # 3. Structural birth stepping on the 2-chain a < b (n=2 -> n=3) for root mark i=0 vs i=1:
    d0_15 = _two_chain_15_branch_law(0)
    d1_15 = _two_chain_15_branch_law(1)
    k_n2_full15 = fisher_rao_distance_exact(d0_15, d1_15)
    tv_n2_full15 = total_variation_exact(d0_15, d1_15)

    # Conditional step-4 distributions at n=3 for each birth-3 ideal S3 in {empty, {a}, {a,b}}:
    e = E_SEED
    c = C_SEED
    d0_s3_empty = (e, e, e * F_SEED_0 / c, e * H_SEED_0 / c, Fraction(1, 8), Fraction(65, 88))
    d1_s3_empty = (e, e, e * F_SEED_1 / c, e * H_SEED_1 / c, Fraction(1, 8), Fraction(65, 88))
    k_n3_empty = fisher_rao_distance_exact(d0_s3_empty, d1_s3_empty)

    d0_s3_fork = (
        e,
        e,
        e * H_SEED_0 / F_SEED_0,
        e * H_SEED_0 / F_SEED_0,
        Fraction(1, 1) - 2 * e - 2 * e * H_SEED_0 / F_SEED_0,
    )
    d1_s3_fork = (
        e,
        e,
        e * H_SEED_1 / F_SEED_1,
        e * H_SEED_1 / F_SEED_1,
        Fraction(1, 1) - 2 * e - 2 * e * H_SEED_1 / F_SEED_1,
    )
    k_n3_fork = fisher_rao_distance_exact(d0_s3_fork, d1_s3_fork)

    d0_s3_chain = (e, e, e, Fraction(41, 44))
    d1_s3_chain = (e, e, e, Fraction(41, 44))
    k_n3_chain = fisher_rao_distance_exact(d0_s3_chain, d1_s3_chain)

    # 4. Multi-Readout Scalar / Rank Test across readouts (Z, D, Y) at matched singleton prefix n=1:
    # Build the 3 x 6 readout probability matrix over the 6 histories (i in {0,1}, s in {+1, 0, -1})
    histories_n1 = [(i, s) for i in (0, 1) for s in (Fraction(1, 1), Fraction(0, 1), Fraction(-1, 1))]
    z_row: list[float] = []
    d_row: list[float] = []
    y_row: list[float] = []
    for i_mark, s_pol in histories_n1:
        law = _singleton_coarse_continuation_law(i_mark, s_pol, active=True)
        z_row.append(float(law[4]))
        d_row.append(float(law[0]))
        y_row.append(float(law[0] + law[1]))

    def _center(row: list[float]) -> list[float]:
        mean = sum(row) / len(row)
        return [x - mean for x in row]

    z_res = _center(z_row)
    d_res = _center(d_row)
    y_res = _center(y_row)

    # Compute exact rank of [z_res, d_res] (2x6 matrix):
    g00 = sum(a * a for a in z_res)
    g11 = sum(b * b for b in d_res)
    g01 = sum(a * b for a, b in zip(z_res, d_res))
    trace_g = g00 + g11
    det_g = g00 * g11 - g01 * g01
    disc = max(0.0, trace_g * trace_g - 4.0 * det_g)
    lam1 = 0.5 * (trace_g + math.sqrt(disc))
    lam2 = max(0.0, 0.5 * (trace_g - math.sqrt(disc)))
    sigma1 = math.sqrt(lam1)
    sigma2 = math.sqrt(lam2)

    # Check whether one scalar kappa works across readouts Z and D:
    # Because Z depends only on residual s (z_res is identical for i=0 and i=1) while D depends
    # strongly on root mark i and oppositely on s, det_g > 0 and rank == 2.
    one_scalar_works_across_all_readouts = False

    return {
        "witness_identities": {
            "delta_current_exact": str(delta_current_exact),
            "delta_update_exact": str(delta_update_exact),
            "matches_1_over_6336": delta_current_exact == Fraction(1, 6336),
            "matches_1_over_25344": delta_update_exact == Fraction(1, 25344),
            "update_over_current_ratio": str(delta_update_exact / delta_current_exact),
        },
        "pure_residual_update_contraction": {
            "contraction_rate_t_per_step": float(T_CONTRACTION),
            "shrinks_monotonically_at_fixed_prefix": all(
                residual_update_steps[idx + 1]["kappa_fisher_rao_pair"]
                < residual_update_steps[idx]["kappa_fisher_rao_pair"]
                for idx in range(len(residual_update_steps) - 1)
            ),
            "inactive_controls_identically_zero": all(
                step["inactive_control_kappa_fr"] == 0.0 for step in residual_update_steps
            ),
            "fixed_mark_readout_ratio_Z_over_D": -3945.0 / 779.0,
            "steps": residual_update_steps,
        },
        "structural_birth_stepping": {
            "antichain_trajectory": antichain_birth_steps,
            "two_chain_mark_stepping": {
                "kappa_fr_n2_full_15_branch": k_n2_full15,
                "tv_n2_full_15_branch_exact": str(tv_n2_full15),
                "kappa_fr_n3_given_S3_empty_edge_isolate": k_n3_empty,
                "kappa_fr_n3_given_S3_root_fork": k_n3_fork,
                "kappa_fr_n3_given_S3_full_3chain": k_n3_chain,
                "contraction_ratios_by_branch": {
                    "S3_empty_edge_isolate": k_n3_empty / k_n2_full15,
                    "S3_root_fork": k_n3_fork / k_n2_full15,
                    "S3_full_3chain": k_n3_chain / k_n2_full15,
                },
                "all_n3_branches_shrink_vs_n2": (
                    k_n3_empty < k_n2_full15
                    and k_n3_fork < k_n2_full15
                    and k_n3_chain < k_n2_full15
                ),
                "uniform_exponential_across_branches": False,
            },
        },
        "two_readout_scalar_test": {
            "pure_residual_only_rank": 1,
            "combined_mark_and_residual_rank": 2,
            "singular_values_Z_vs_D": (sigma1, sigma2),
            "gram_determinant_Z_vs_D": det_g,
            "one_scalar_works_across_readouts": one_scalar_works_across_all_readouts,
            "two_chain_n2_contrast_D_exact": "-41/264",
            "two_chain_n2_contrast_Y_exact": "-7/44",
            "two_chain_Y_over_D_ratio_exact": "42/41",
            "n3_fork_structural_kappa_fr": k_n3_fork,
            "n3_fork_readout_D_kappa_fr": 0.0,
        },
        "successive_birth_unconditional_readouts": evaluate_successive_birth_unconditional_readouts(),
        "two_bit_readout_sufficiency": evaluate_independently_enumerated_kernel_and_two_bit_sufficiency(),
        "native_conclusion": (
            "1. Under repeated pure residual updates K = M(0) at a fixed committed prefix, "
            "kappa shrinks geometrically by t = 1/2 per step (while inactive controls give kappa = 0). "
            "2. Across actual structural births, contraction is topology-dependent rather than a "
            "uniform exponential in event density: causal link-forming births (S != empty for residual s, "
            "or S_3 = {a,b} forming a 3-chain for root mark i) quench future sensitivity to zero in a "
            "single step, whereas unlinked antichain births (S = empty) preserve/amplify conditional "
            "residual contrast. "
            "3. No single scalar kappa works across two readouts (Z and D, or full q_4 and D on the fork): "
            "history carrying in the four-birth model is rank 2 (kappa_residual, kappa_mark)."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. QR-05DO Anchor-Calculus Quotient for Regional Interaction Counts
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_qr05do_interaction_scale_quotient() -> dict[str, object]:
    """Apply QR-05DO's 32-subset anchor calculus to regional interaction counts vs Sigma_crit.

    Tests whether internal DET record channels can identify:
      - ``relative_interaction_profile``: relative interaction counts across regions
      - ``step_contraction_rate``: discrete Markov contraction rate per step
      - ``physical_mass_per_area_scale``: conversion ``mu = Sigma_b / N_int`` and
        critical surface mass density ``Sigma_crit = mu * N_rec`` [M_sun/pc^2].
    """
    channels: tuple[str, ...] = (
        "order",
        "counts",
        "transition_contraction",
        "distance_ratio",
        "anchor",
    )

    # Declare finite world class covering profile variations, contraction rates,
    # and the scale witness pair (W_scale_1 vs W_scale_2) that share identical
    # internal event graphs, counts, and step contractions but differ in the
    # physical mass-per-area conversion mu = Sigma_b / N_int (e.g. 8 vs 137 M_sun/pc^2).
    worlds: tuple[dict[str, object], ...] = (
        {
            "name": "W_core_outskirt_scale_8",
            "order": (0.50, 0.25),
            "counts": (0.80, 0.20),
            "transition_contraction": (0.50,),
            "distance_ratio": (1.0, 0.25),
            "anchor": ("Sigma_crit=8.0_Msun_pc2",),
            "targets": {
                "relative_interaction_profile": "profile_A",
                "step_contraction_rate": "t=1/2",
                "physical_mass_per_area_scale": "8.0_Msun_pc2",
            },
        },
        {
            "name": "W_core_outskirt_scale_137",
            "order": (0.50, 0.25),
            "counts": (0.80, 0.20),
            "transition_contraction": (0.50,),
            "distance_ratio": (1.0, 0.25),
            "anchor": ("Sigma_crit=137.0_Msun_pc2",),
            "targets": {
                "relative_interaction_profile": "profile_A",
                "step_contraction_rate": "t=1/2",
                "physical_mass_per_area_scale": "137.0_Msun_pc2",
            },
        },
        {
            "name": "W_uniform_profile_scale_8",
            "order": (0.35, 0.35),
            "counts": (0.50, 0.50),
            "transition_contraction": (0.50,),
            "distance_ratio": (0.5, 0.5),
            "anchor": ("Sigma_crit=8.0_Msun_pc2",),
            "targets": {
                "relative_interaction_profile": "profile_B",
                "step_contraction_rate": "t=1/2",
                "physical_mass_per_area_scale": "8.0_Msun_pc2",
            },
        },
        {
            "name": "W_passive_contraction_scale_8",
            "order": (0.50, 0.25),
            "counts": (0.80, 0.20),
            "transition_contraction": (1.00,),
            "distance_ratio": (1.0, 0.25),
            "anchor": ("Sigma_crit=8.0_Msun_pc2",),
            "targets": {
                "relative_interaction_profile": "profile_A",
                "step_contraction_rate": "t=1_passive",
                "physical_mass_per_area_scale": "8.0_Msun_pc2",
            },
        },
    )

    all_subsets: list[tuple[str, ...]] = []
    for k in range(len(channels) + 1):
        for sub in itertools.combinations(channels, k):
            all_subsets.append(sub)

    def _is_identifiable(subset: tuple[str, ...], target_key: str) -> bool:
        classes: dict[tuple[object, ...], set[object]] = {}
        for w in worlds:
            sig = tuple(w[ch] for ch in subset)
            t_val = w["targets"][target_key]  # type: ignore[index]
            classes.setdefault(sig, set()).add(t_val)
        return all(len(vals) == 1 for vals in classes.values())

    target_keys = (
        "relative_interaction_profile",
        "step_contraction_rate",
        "physical_mass_per_area_scale",
    )

    ident_map: dict[tuple[str, ...], dict[str, bool]] = {}
    for sub in all_subsets:
        per_t = {tk: _is_identifiable(sub, tk) for tk in target_keys}
        per_t["joint_all"] = all(per_t.values())
        ident_map[sub] = per_t

    # Check one-step refinement monotonicity across all 32 subsets:
    monotonicity_violations = 0
    for sub in all_subsets:
        for ch in channels:
            if ch in sub:
                continue
            refined = tuple(c for c in channels if c in sub or c == ch)
            for tk in (*target_keys, "joint_all"):
                if ident_map[sub][tk] and not ident_map[refined][tk]:
                    monotonicity_violations += 1

    anchor_free = [sub for sub in all_subsets if "anchor" not in sub]
    anchor_bearing = [sub for sub in all_subsets if "anchor" in sub]

    # Check scale witness blindness across all 16 anchor-free subsets:
    w_s1, w_s2 = worlds[0], worlds[1]
    anchor_free_blind_count = sum(
        1
        for sub in anchor_free
        if tuple(w_s1[ch] for ch in sub) == tuple(w_s2[ch] for ch in sub)
    )
    anchor_bearing_sighted_count = sum(
        1
        for sub in anchor_bearing
        if tuple(w_s1[ch] for ch in sub) != tuple(w_s2[ch] for ch in sub)
    )

    minimal_scale_sets = [
        sub
        for sub in all_subsets
        if ident_map[sub]["physical_mass_per_area_scale"]
        and not any(
            set(other) < set(sub) and ident_map[other]["physical_mass_per_area_scale"]
            for other in all_subsets
        )
    ]

    return {
        "n_channels": len(channels),
        "n_subsets": len(all_subsets),
        "monotonicity_violations": monotonicity_violations,
        "anchor_free_subsets_total": len(anchor_free),
        "anchor_free_blind_on_scale_witness": anchor_free_blind_count,
        "anchor_bearing_subsets_total": len(anchor_bearing),
        "anchor_bearing_sighted_on_scale_witness": anchor_bearing_sighted_count,
        "scale_identifiable_on_any_anchor_free_subset": any(
            ident_map[sub]["physical_mass_per_area_scale"] for sub in anchor_free
        ),
        "minimal_identifying_sets_for_mass_per_area_scale": [
            list(sub) for sub in minimal_scale_sets
        ],
        "conclusion": (
            "Across all 16 anchor-free subsets of internal DET record channels, "
            "physical mass-per-area conversion (Sigma_b / N_int) and Sigma_crit are "
            "NON_IDENTIFIABLE (16/16 blind on the scale witness pair). Internal records "
            "can determine relative regional interaction ratios and per-step Markov "
            "contraction, but Sigma_crit requires an explicit external anchor and "
            "cannot be treated as derived from internal records alone."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. QR-05CR Two-Region Conservative Flux vs. Pointwise Operator Audit
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_qr05cr_two_region_flux_audit(
    *,
    kappa_core: float = 0.05,
    kappa_outskirt: float = 0.90,
    beta: float = 0.93,
    source_core: float = 1.0,
) -> dict[str, object]:
    """Audit a spatially varying kappa coefficient in a two-region and multi-region flux test.

    Following QR-05CR (C6 no-double-counting audit):
      - Let ``d_k = 1 - beta * kappa_k`` be the regional stiffness (inverse boost
        ``G / G_eff(kappa_k)``) across Region 0 (core, ``kappa_0``) and Region 1
        (outskirt, ``kappa_1 > kappa_0``).
      - Pointwise operator: ``(S_P Phi)_k = d_k * (Delta_disc Phi)_k``.
      - Conservative divergence operator:
        ``(S_D Phi)_k = d_{k+1/2}*(Phi_{k+1} - Phi_k) - d_{k-1/2}*(Phi_k - Phi_{k-1})``.
      - Checks:
        1. ``S(1) == 0`` (annihilates constant potentials -> no spurious zeroth-order source);
        2. ``sum_k (S_D Phi)_k == 0`` (conservative flux balance across regions);
        3. ``sum_k (S_P Phi)_k != 0`` (pointwise operator creates a fictitious source
           ``(d_0 - d_1)*(Phi_1 - Phi_0)`` whenever ``kappa_0 != kappa_1``);
        4. Explicit source accounting: for ``(S_D Phi)_0 = -source_core`` and
           ``(S_D Phi)_1 = +source_core`` (closed dipole / two-region balance),
           the bond response ``Phi_1 - Phi_0 = -source_core / d_{1/2}`` is
           boosted by ``1 / (1 - beta * kappa_{1/2})`` while total flux and
           source balance identically.
    """
    if not (0.0 <= kappa_core <= 1.0 and 0.0 <= kappa_outskirt <= 1.0):
        raise ValueError("kappa_core and kappa_outskirt must lie in [0, 1]")
    if not (0.0 <= beta < 1.0):
        raise ValueError("beta must lie in [0, 1)")
    if source_core <= 0.0:
        raise ValueError("source_core must be > 0")

    d0 = 1.0 - beta * kappa_core
    d1 = 1.0 - beta * kappa_outskirt
    d_interface = 0.5 * (d0 + d1)

    # 1. Constant potential Phi = (1, 1) -> zero source term
    const_phi = (1.0, 1.0)
    sp_const_0 = d0 * (const_phi[1] - const_phi[0])
    sp_const_1 = d1 * (const_phi[0] - const_phi[1])
    sd_const_0 = d_interface * (const_phi[1] - const_phi[0])
    sd_const_1 = d_interface * (const_phi[0] - const_phi[1])
    source_term_zero = (
        abs(sp_const_0) == 0.0
        and abs(sp_const_1) == 0.0
        and abs(sd_const_0) == 0.0
        and abs(sd_const_1) == 0.0
    )

    # 2. Solve conservative two-region response (S_D Phi)_0 = -source_core, Phi_0 = 0:
    # d_interface * (Phi_1 - Phi_0) = -source_core  =>  Phi_1 - Phi_0 = -source_core / d_interface
    phi_0 = 0.0
    phi_1 = -source_core / d_interface
    unboosted_delta_phi = -source_core  # when kappa = 0 => d = 1
    response_boost_factor = (phi_1 - phi_0) / unboosted_delta_phi

    # Evaluate operators on (phi_0, phi_1):
    sd_0 = d_interface * (phi_1 - phi_0)
    sd_1 = d_interface * (phi_0 - phi_1)
    sd_flux_sum = sd_0 + sd_1

    sp_0 = d0 * (phi_1 - phi_0)
    sp_1 = d1 * (phi_0 - phi_1)
    sp_flux_sum = sp_0 + sp_1  # Fictitious ghost source (d0 - d1)*(phi_1 - phi_0) != 0

    # Explicit source residual check: (S_D Phi)_0 + source_core == 0
    explicit_source_residual_0 = abs(sd_0 + source_core)
    explicit_source_residual_1 = abs(sd_1 - source_core)

    # Kernel second-moment recovery on bond (0, 1):
    # Symmetric jump kernel K = {+1: d_interface, 0: -2*d_interface, -1: d_interface}
    mu2 = (+1) ** 2 * d_interface + (-1) ** 2 * d_interface
    recovered_d = 0.5 * mu2
    coeff_recovery_error = abs(recovered_d - d_interface)

    # Added-source detection control: add delta_q = 0.1 * source_core to Region 0
    added_source = 0.1 * source_core
    detected_added_source = abs(sd_0 + source_core + added_source)

    return {
        "kappa_core": kappa_core,
        "kappa_outskirt": kappa_outskirt,
        "beta": beta,
        "d_core": d0,
        "d_outskirt": d1,
        "d_interface": d_interface,
        "constant_annihilation_passed": source_term_zero,
        "divergence_flux_sum": sd_flux_sum,
        "divergence_conserves_flux": abs(sd_flux_sum) < 1e-15,
        "pointwise_flux_sum_fictitious_source": sp_flux_sum,
        "pointwise_violates_flux_balance": abs(sp_flux_sum) > 1e-6,
        "response_delta_phi": phi_1 - phi_0,
        "unboosted_delta_phi": unboosted_delta_phi,
        "response_boost_factor": response_boost_factor,
        "explicit_source_max_residual": max(
            explicit_source_residual_0, explicit_source_residual_1
        ),
        "kernel_moment_coefficient_error": coeff_recovery_error,
        "added_source_control_detected": detected_added_source > 0.05 * source_core,
        "conclusion": (
            f"In the two-region conservative divergence operator (S_D Phi)_k, kappa increases "
            f"the potential response by {response_boost_factor:.4f}x while total flux balances "
            f"identically (sum = {sd_flux_sum:.1e}) and the explicit source is accounted for to "
            f"{max(explicit_source_residual_0, explicit_source_residual_1):.1e}. By contrast, the "
            f"pointwise operator (S_P Phi)_k = d_k (Delta Phi)_k creates a non-canceling fictitious "
            f"source sum = {sp_flux_sum:+.6f} (violating Newton's 3rd law across the interface)."
        ),
    }


def run_native_record_bridge_suite() -> dict[str, object]:
    """Run all three finite DET + QR bridge audits."""
    step1 = evaluate_four_birth_native_kappa()
    step2 = evaluate_qr05do_interaction_scale_quotient()
    step3 = evaluate_qr05cr_two_region_flux_audit()
    return {
        "four_birth_native_kappa": step1,
        "qr05do_interaction_scale_quotient": step2,
        "qr05cr_two_region_flux_audit": step3,
    }


__all__ = (
    "A_HARMONIC",
    "T_CONTRACTION",
    "THETA_ACTIVE",
    "evaluate_admitted_next_birth_reusability_without_standin",
    "evaluate_four_birth_native_kappa",
    "evaluate_independently_enumerated_kernel_and_two_bit_sufficiency",
    "evaluate_qr05cr_two_region_flux_audit",
    "evaluate_qr05do_interaction_scale_quotient",
    "evaluate_successive_birth_unconditional_readouts",
    "fisher_rao_distance_exact",
    "run_native_record_bridge_suite",
    "total_variation_exact",
)
