"""DET v8.1 — bare kernel extension and operator-word consistency.

A normalized pair-kernel extends by tensoring with any normalized pair-kernel;
coarse-graining recovers the old kernel. This algebraic fact does not constrain
the new marginal or enforce a physical measurement algebra. A Gram sum rule
holds for the declared strongly positive kernels, including singular ones.

The supplied Bell construction has compatible Q_{1+AB} and Q2 moment matrices.
This is one finite example. It does not show that an arbitrary almost-quantum
point fails at Q2, nor derive all-level NPA relations from bare D marginals.
The full NPA hierarchy with its measurement-word relations targets commuting
correlations C_qc; it does not generally select finite tensor-product C_q or
its closure C_qa. Sources: https://arxiv.org/abs/0803.4290 and
https://arxiv.org/abs/2001.04383. These are imported results, not a resolved
DET forcing theorem. Historical function names and numeric examples remain.
"""

from __future__ import annotations

from det8.models.correlation_class import correlation_set_scope
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
            "Summing exact fine Gram vectors realizes the coarse kernel in the "
            "same Hilbert space. This numerical diagnostic uses a "
            "tolerance-qualified factorization; max_abs_error reports its "
            "reconstruction error and sum_rule_holds tests that error < 1e-9."
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
    """Compare the supplied Bell Q_{1+AB} and Q2 matrices, not arbitrary data."""
    from det8.models.correlation_class import (
        bell_state_npa_level1,
        global_record_extendability,
    )
    first = bell_state_npa_level1()
    extension = global_record_extendability()
    return {
        "bell_level1_psd": first["psd"],
        "bell_level2_psd": extension["level2_psd"],
        "bell_level1_is_principal_submatrix": extension["level1_is_principal_submatrix"],
        "bell_extends": extension["extends"],
        "tested_levels": ("Q_1+AB", "Q_2"),
        "arbitrary_almost_quantum_rejection_established": False,
        "all_level_extension_tested": False,
        "why_this_is_non_trivial": (
            "NPA imposes measurement-word identities in addition to positivity. "
            "The supplied Bell realization satisfies them; this check does not "
            "find the exclusion level of an arbitrary nonquantum behavior."
        ),
    }


# ── The resolution ──────────────────────────────────────────────────────────


def resolution() -> dict:
    return {
        "question": "Does bare D marginal extension imply NPA operator-word extendability?",
        "answer": (
            "No such implication follows from bare marginal consistency. Tensoring "
            "with any normalized kernel already supplies a bare extension. NPA "
            "additionally requires a specified measurement algebra and its word identities."
        ),
        "status": "BARE_EXTENSION_TRIVIAL; OPERATOR_RELATIONS_ADDITIONAL; DET_FORCING_OPEN",
        "scope": correlation_set_scope(),
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T6 residual — bare extension versus operational moment consistency",
        "deliverables": {
            "kernel coarse-graining": "MATH — finite biadditive marginal identity",
            "Gram sum rule under strong positivity": "MATH — finite Gram construction; numerical examples",
            "bare normalized tensor extension": "MATH — elementary construction",
            "Bell Q_1+AB to Q2 extension": "CORR — one supplied quantum realization",
            "all-level NPA target C_qc": "MATH — cited theorem with operator-word premises",
        },
        "scope": correlation_set_scope(),
        "not_derived_here": [
            "NPA convergence or the general C_qa/C_qc separation (both cited)",
            "an implication from bare record marginals to the NPA word relations",
            "a selected tensor-product quantum theory or a physical update law",
        ],
        "status": "BARE_EXTENSION_PROVED; DET_OPERATIONAL_SELECTION_OPEN",
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
            f"Bare tensor extension recovers the old kernel (error {trivial['max_abs_error']:.1e}); "
            f"the Gram sum rule holds ({srule['sum_rule_holds']}). The supplied Bell "
            f"example extends to Q2 ({op['bell_extends']}). Neither result derives "
            "NPA operator-word relations from records or selects tensor-product QM."
        ),
    }
