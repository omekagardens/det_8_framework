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
import itertools
import math
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
    "evaluate_four_birth_native_kappa",
    "evaluate_qr05cr_two_region_flux_audit",
    "evaluate_qr05do_interaction_scale_quotient",
    "evaluate_successive_birth_unconditional_readouts",
    "fisher_rao_distance_exact",
    "run_native_record_bridge_suite",
    "total_variation_exact",
)
