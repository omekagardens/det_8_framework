"""
DET v8.1 — T6 Residual: what "global record extendability" must mean

The last open question of the correlation-class program: is DET's
"global record extendability" (𝔇_n = Marginal(𝔇_{n+1}) for every lawful future
refinement) EQUAL to NPA-extendability, or a distinct condition?

THE RESOLUTION (honest and precise). The answer is: it depends on what 𝔇
carries, and being precise about this SETTLES the question.

  1. BARE pair-kernel extendability is TRIVIAL. A single decoherence functional
     𝔇 on a finite algebra is always Gram-representable (𝔇(A,B)=⟨v_A,v_B⟩),
     and it always extends — tensor with any normalized kernel and take the
     marginal: marginal(𝔇 ⊗ 𝔇_new) = 𝔇 exactly. So "𝔇_n = marginal of SOME
     𝔇_{n+1}" is satisfiable by EVERY pair-kernel, quantum or almost-quantum.
     It therefore CANNOT isolate the quantum set.

  2. NPA-extendability (moment-matrix / operator-algebra consistency) is the
     NON-trivial condition. The level-1 moment matrix must extend to level 2, 3, …
     while obeying the operator relations A_x² = I, [A_x,B_y] = 0 and the word
     reductions. This is exactly what NPA convergence proves to be equivalent to
     quantum realizability (Navascués–Pironio–Acín 2008).

  3. Therefore: DET's "global record extendability" collapses Q̃ → Q IF AND ONLY
     IF it is read as the operator-algebra (moment-matrix) consistency, NOT as the
     bare decoherence-functional marginal. The collapse is then a SETTLED theorem
     (NPA convergence), and DET's contribution is the precise identification of
     what "record extendability" must mean — consistency of the full measurement
     algebra under lawful refinement, not mere marginal consistency of 𝔇.

What is implemented (pure stdlib):

  - coarse-graining (marginal) of a pair-kernel over a refinement partition;
  - the Gram SUM RULE: the coarse Gram vector is the sum of the fine Gram
    vectors (v_coarse_a = Σ_i v_fine_(a,i)), verified numerically — this is the
    constructive content of "a single Hilbert space realizes the refinement";
  - the TRIVIALITY of bare extendability: marginal(𝔇 ⊗ 𝔇_new) = 𝔇 for any
    normalized 𝔇_new, verified exactly;
  - the CONTRAST with the non-trivial operator-algebra condition, reusing the
    Bell-state level-1/level-2 moment matrices (correlation_class.py).

DERIVATION CERTIFICATE (honest provenance):

  Gram representation of 𝔇           MATH — spectral theorem / Cholesky (T2b).
  coarse-graining + sum rule         MATH — decoherent histories (Gell-Mann–
                                          Hartle; Griffiths; Omnès), credited.
  bare extendability is trivial      TH-DET — verified construction.
  NPA-extendability ⟺ quantum        MATH — Navascués–Pironio–Acín (2008), cited.
  resolution (collapse iff operator
    algebra consistency)             TH-DET — the sharpening of the DET condition.

  NOT done: re-deriving NPA convergence, or the infinite inductive-limit
  construction (standard, cited).
"""

from __future__ import annotations

from det8.models.pair_kernel import PairKernel


# ── Coarse-graining (marginal) of a pair-kernel ─────────────────────────────


def marginal(pk: PairKernel, blocks: list[frozenset]) -> PairKernel:
    """Coarse-grain a pair-kernel over a partition `blocks` of the fine indices.

    𝔇_coarse(a,b) = Σ_{i∈block_a, j∈block_b} 𝔇_fine(i,j). If blocks partition
    the fine set, the coarse kernel stays normalized.
    """
    nb = len(blocks)
    D = [[0j] * nb for _ in range(nb)]
    for a in range(nb):
        for b in range(nb):
            D[a][b] = sum(pk.D[i][j] for i in blocks[a] for j in blocks[b])
    return PairKernel(D)


def product_blocks(n_old: int, n_new: int) -> list[frozenset]:
    """The refinement blocks for a tensor refinement old×new.

    block_a = {a·n_new + i : i ∈ [0,n_new)} — the 'new slot' is summed out.
    """
    return [frozenset(a * n_new + i for i in range(n_new)) for a in range(n_old)]


# ── The Gram sum rule (single Hilbert space realizes a refinement) ──────────


def gram_sum_rule(pk_fine: PairKernel, blocks: list[frozenset]) -> dict:
    """Verify v_coarse_a = Σ_{i∈block_a} v_fine_i reproduces the marginal.

    This is the constructive half of "a consistent refinement is realized by a
    single Hilbert space": the coarse Gram vectors are sums of the fine ones,
    so the top (fine) Hilbert space carries the whole family.
    """
    L = pk_fine.cholesky()
    v = [L[i] for i in range(pk_fine.n)]
    dim = len(v[0])
    v_coarse = [[sum(v[i][k] for i in blocks[a]) for k in range(dim)]
                for a in range(len(blocks))]
    marg = marginal(pk_fine, blocks)
    max_diff = 0.0
    for a in range(len(blocks)):
        for b in range(len(blocks)):
            inner = sum(v_coarse[a][k] * v_coarse[b][k].conjugate() for k in range(dim))
            max_diff = max(max_diff, abs(inner - marg.D[a][b]))
    return {
        "max_abs_error": max_diff,
        "sum_rule_holds": max_diff < 1e-9,
        "interpretation": (
            "The coarse Gram vectors are the sums of the fine Gram vectors, so "
            "one Hilbert space (the fine one) realizes the coarse kernel exactly."
        ),
    }


# ── Triviality of bare extendability ────────────────────────────────────────


def trivial_extendability(pk: PairKernel, pk_new: PairKernel) -> dict:
    """Show marginal(𝔇 ⊗ 𝔇_new) = 𝔇 exactly, for any normalized 𝔇_new.

    Hence EVERY pair-kernel is 'bare-extendable'; bare 𝔇_n = Marginal(𝔇_{n+1})
    cannot separate quantum from almost-quantum.
    """
    refined = pk.compose(pk_new)
    blocks = product_blocks(pk.n, pk_new.n)
    marg = marginal(refined, blocks)
    max_diff = max(abs(marg.D[a][b] - pk.D[a][b])
                   for a in range(pk.n) for b in range(pk.n))
    return {
        "max_abs_error": max_diff,
        "always_extends": max_diff < 1e-9,
        "conclusion": (
            "marginal(𝔇 ⊗ 𝔇_new) = 𝔇 for ANY normalized 𝔇_new — bare "
            "extendability is trivial and does NOT isolate the quantum set."
        ),
    }


# ── The non-trivial condition (operator algebra / NPA) ──────────────────────


def operator_algebra_consistency() -> dict:
    """The genuinely non-trivial condition: moment-matrix extendability.

    Reuses the Bell-state level-1/level-2 NPA moment matrices. The Bell state
    (quantum) extends: its level-1 Γ is a principal submatrix of a PSD level-2
    Γ². An almost-quantum-but-not-quantum correlation fails exactly this step —
    which is why it is not quantum (NPA convergence).
    """
    from det8.models.correlation_class import (
        bell_state_npa_level1, global_record_extendability,
    )
    l1 = bell_state_npa_level1()
    ext = global_record_extendability()
    return {
        "bell_level1_psd": l1["psd"],
        "bell_level2_psd": ext["level2_psd"],
        "bell_level1_is_principal_submatrix": ext["level1_is_principal_submatrix"],
        "bell_extends": ext["extends"],
        "why_this_is_non_trivial": (
            "The level-2 matrix must obey A_x²=I, [A_x,B_y]=0 and the word "
            "reductions (e.g. A₀·(A₀B₀)=B₀). These operator-algebra relations — "
            "not the bare 𝔇 marginal — are what an almost-quantum-but-not-quantum "
            "correlation fails to extend."
        ),
    }


# ── The resolution ──────────────────────────────────────────────────────────


def resolution() -> dict:
    return {
        "question": "is 𝔇_n = Marginal(𝔇_{n+1}) equal to NPA-extendability?",
        "answer": (
            "Not as stated. As a BARE decoherence-functional marginal it is "
            "trivial (every 𝔇 extends) and cannot isolate quantum. It collapses "
            "Q̃ → Q if and only if 'record extendability' means consistency of the "
            "full measurement algebra (the moment-matrix / operator relations), "
            "which IS NPA-extendability — and that is the borrowed NPA-convergence "
            "theorem, not a DET-specific result."
        ),
        "status": (
            "The collapse is a SETTLED theorem (NPA convergence) under the "
            "operator-algebra reading. DET's contribution is the sharpened "
            "definition: 'global record extendability' must be the operator-"
            "algebra consistency, not the bare pair-kernel marginal."
        ),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T6 residual — what global record extendability must mean",
        "deliverables": {
            "coarse-graining (marginal) of 𝔇": "MATH — decoherent histories (Gell-Mann–Hartle, Griffiths, Omnès), credited",
            "Gram sum rule (single Hilbert space realizes a refinement)": "TH-DET — verified numerically",
            "bare extendability is trivial": "TH-DET — verified construction",
            "NPA-extendability ⟺ quantum": "MATH — Navascués–Pironio–Acín (2008), cited",
            "resolution (collapse iff operator-algebra consistency)": "TH-DET — sharpened DET condition",
        },
        "not_derived_here": [
            "NPA convergence itself (cited)",
            "the infinite inductive-limit construction (standard, cited)",
        ],
        "status": (
            "Resolved: the bare 𝔇-marginal condition is trivial; the collapse "
            "Q̃ → Q is the NPA theorem applied to the operator algebra. DET's "
            "'global record extendability' is equivalent to NPA-extendability "
            "when (and only when) it is read as the operator-algebra consistency."
        ),
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_t6_residual() -> dict:
    from det8.models.pair_kernel import make_pair_kernel

    pk = make_pair_kernel(4, seed=42, coherent=True)
    pk_new = make_pair_kernel(3, seed=7, coherent=True)

    # 1. Triviality of bare extendability.
    trivial = trivial_extendability(pk, pk_new)

    # 2. Sum rule: the fine kernel realizes the coarse kernel in one Hilbert space.
    refined = pk.compose(pk_new)
    blocks = product_blocks(pk.n, pk_new.n)
    srule = gram_sum_rule(refined, blocks)

    # 3. The non-trivial operator-algebra condition.
    op = operator_algebra_consistency()

    return {
        "trivial_bare_extendability": trivial,
        "gram_sum_rule": srule,
        "operator_algebra_consistency": op,
        "resolution": resolution(),
        "certificate": derivation_certificate(),
        "interpretation": (
            "Bare 𝔇-extendability is trivial (marginal(𝔇⊗𝔇_new)=𝔇, error "
            f"{trivial['max_abs_error']:.1e}). The Gram sum rule holds "
            f"({srule['sum_rule_holds']}), so one Hilbert space realizes any "
            "refinement. The genuinely non-trivial condition is the operator-"
            f"algebra (moment-matrix) consistency — Bell extends to level 2 "
            f"({op['bell_extends']}), and an almost-quantum-but-not-quantum "
            "correlation fails exactly this. Hence 'global record extendability' "
            "collapses Q̃→Q iff read as the operator-algebra consistency (= NPA "
            "extendability), settling the residual."
        ),
    }
