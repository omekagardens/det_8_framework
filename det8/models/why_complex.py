"""DET v8.1 — compatible complex structures: conditional correspondence.

For the supplied compatible pair G=I, Ω=J0, J=G^{-1}Ω squares to -I,
and simultaneous form preservation gives O(2m) ∩ Sp(2m,R)=U(m).
Compatibility is an input, not a consequence of reversibility or positivity.
The normalized positive family D_t=(I+i tJ0)/2, 0<t<1, is a counterexample
to the unrestricted implication: planar rotations preserve both forms while
(G^{-1}Ω)^2=-t^2 I. A real positive kernel can also have interference.

These finite calculations do not select complex over real or quaternionic
operational quantum theories. Real-theory network exclusions depend on the
specified composition/source/experimental premises; they do not establish
an imaginary kernel entry as a direct observation. A real vector realization
of Bell correlators is not a complete real quantum theory or the almost-
quantum set. No empirical dataset is analyzed by this module.

See the explicit local counterexample and premise audit in
 docs/validation/t8-q-strict-derivation-2026-09-12/DERIVATION.md, sections 6–7,
and the qualified operational comparison in
 docs/validation/t8-q-principle-selection-research-2026-09-13/RESEARCH.md.
Historical callable names are retained; they do not confer derivation status.
"""

from __future__ import annotations

import math
import random

# ── Small real-matrix helpers ───────────────────────────────────────────────


def _matmul(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    return [[sum(A[i][r] * B[r][j] for r in range(k)) for j in range(m)]
            for i in range(n)]


def _transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def _scale(s, A):
    return [[s * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _inverse(A):
    """Real matrix inverse via Gauss–Jordan (A assumed invertible)."""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(A)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        for j in range(2 * n):
            M[col][j] /= pv
        for r in range(n):
            if r != col and M[r][col] != 0.0:
                f = M[r][col]
                for j in range(2 * n):
                    M[r][j] -= f * M[col][j]
    return [row[n:] for row in M]


def _frob(A):
    return math.sqrt(sum(abs(A[i][j]) ** 2 for i in range(len(A)) for j in range(len(A[0]))))


# ── 𝔇 = G + iΩ decomposition ───────────────────────────────────────────────


def decompose(D: list[list[complex]]) -> tuple:
    """Split a Hermitian D into G (real symmetric) and Ω (real antisymmetric)."""
    n = len(D)
    G = [[D[i][j].real for j in range(n)] for i in range(n)]
    Om = [[D[i][j].imag for j in range(n)] for i in range(n)]
    return G, Om


def is_symmetric(A, tol=1e-9):
    return max(abs(A[i][j] - A[j][i]) for i in range(len(A)) for j in range(len(A))) < tol


def is_antisymmetric(A, tol=1e-9):
    return max(abs(A[i][j] + A[j][i]) for i in range(len(A)) for j in range(len(A))) < tol


# ── Real positive kernels can interfere ────────────────────────────────────


def real_part_gives_real_qm() -> dict:
    """Historical name: exhibit real-kernel interference, not a full real theory."""
    D = [[1 / 3, 1 / 6], [1 / 6, 1 / 3]]
    i2 = sum(sum(row) for row in D) - D[0][0] - D[1][1]
    return {
        "I2": i2,
        "kernel": D,
        "real_QM_not_classical": abs(i2) > 1e-9,
        "conclusion": "A normalized real positive kernel CAN interfere; real entries do not imply classical additivity.",
        "real_qm_ruled_out_empirically": (
            "Exclusions of specified real quantum network models require composition, "
            "source and experimental premises. This calculation supplies no empirical exclusion."
        ),
        "scope": {"full_real_qm_reconstructed": False, "empirical_exclusion_performed": False},
    }


# ── The complex structure J = G^{-1}Ω ───────────────────────────────────────


def standard_symplectic(m: int) -> list[list[float]]:
    """The standard 2m×2m symplectic structure J₀ (block [[0,1],[-1,0]])."""
    n = 2 * m
    J = [[0.0] * n for _ in range(n)]
    for k in range(m):
        J[2 * k][2 * k + 1] = 1.0
        J[2 * k + 1][2 * k] = -1.0
    return J


def complex_structure(m: int = 2) -> dict:
    """Build J = G^{-1}Ω for the maximally-coherent pair-kernel and check J²=−I.

    Take G = I (identity metric) and Ω = J₀ (unit symplectic form); then
    D = G + iΩ = I + iJ₀ is Hermitian PSD (rank m), and J = G^{-1}Ω = J₀
    satisfies J² = −I — the complex structure that identifies ℝ^{2m} with ℂ^m.
    """
    n = 2 * m
    G = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    Om = standard_symplectic(m)
    J = _matmul(_inverse(G), Om)
    J2 = _matmul(J, J)
    neg_I = [[-1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    err = max(abs(J2[i][j] - neg_I[i][j]) for i in range(n) for j in range(n))
    # also confirm D = G + iΩ is Hermitian PSD (rank m) — eigenvalues are 0 (m×) and 2 (m×).
    return {
        "dim": n,
        "compatibility_assumed": True,
        "complex_field_selected": False,
        "J_squared_equals_minus_I": err < 1e-9,
        "max_abs_error": err,
        "conclusion": (
            f"J = G^{-1}Ω satisfies J² = −I (error {err:.1e}) — a complex "
            "structure for the supplied compatible forms; the physical scalar field is not selected."
        ),
    }


# ── Reversible dynamics: O(2m) ∩ Sp(2m,ℝ) = U(m) ────────────────────────────


def reversible_dynamics_require_complex(m: int = 2, n_trials: int = 50,
                                        seed: int = 42) -> dict:
    """Check the generator identity conditional on supplied compatible forms.

    For G = I and Ω = J₀, a generator X preserves G iff X is antisymmetric
    (X^T = −X). The symplectic (Ω-preserving) condition X^T Ω + Ω X = 0 is then
    exactly X^T Ω + Ω X = J₀ X − X J₀ = 0, i.e. X commutes with J₀ — which is
    the definition of a COMPLEX-LINEAR (u(m)) generator. Verified numerically:
    for random antisymmetric X, "X preserves Ω" ⟺ "X commutes with J".
    """
    rng = random.Random(seed)
    n = 2 * m
    Om = standard_symplectic(m)

    def symp_violation(X):
        Xt = _transpose(X)
        return max(abs(sum(Xt[i][k] * Om[k][j] + Om[i][k] * X[k][j] for k in range(n)))
                   for i in range(n) for j in range(n))

    def commutes_violation(X):
        return max(abs(sum(X[i][k] * Om[k][j] - Om[i][k] * X[k][j] for k in range(n)))
                   for i in range(n) for j in range(n))

    mismatch = 0
    for _ in range(n_trials):
        M = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        X = [[(M[i][j] - M[j][i]) / 2 for j in range(n)] for i in range(n)]  # antisymmetric
        sv = symp_violation(X)
        cj = commutes_violation(X)
        if (sv < 1e-9) != (cj < 1e-9):
            mismatch += 1
    return {
        "n_trials": n_trials,
        "compatibility_assumed": True,
        "complex_field_selected": False,
        "symplectic_iff_commutes_with_J": mismatch == 0,
        "mismatches": mismatch,
        "conclusion": (
            "A generator that preserves both G (metric) and Ω (phase) is exactly "
            "the set {X antisymmetric, X J = J X} = u(m), the unitary Lie "
            "algebra for the supplied G=I, Ω=J0. This conditional identity "
            "does not derive compatibility or select a physical scalar field."
        ),
    }


# ── Why ℂ and not ℍ ─────────────────────────────────────────────────────────


def why_not_quaternions() -> dict:
    return {
        "quaternionic_would_need_three_phases": (
            "Quaternion algebra has three imaginary units. Relating them to physical "
            "forms or dynamics requires an independently specified operational theory."
        ),
        "one_phase_gives_C": (
            "The one imaginary part of an already complex-valued D does not select "
            "complex scalars or exclude quaternionic operational completions."
        ),
        "honest_caveat": "Neither one causal order nor one written antisymmetric part proves scalar-field selection.",
        "selects_complex_over_quaternionic": False,
    }


# ── Relation to almost-quantum / what is actually observed ──────────────────


def connection_to_observation() -> dict:
    """Keep correlator representations, operational theories and observations distinct."""
    return {
        "no_superquantum_observed": "This module analyzes no empirical dataset and makes no exhaustive observation claim.",
        "but_everything_observed_is_in_Qtilde": "Quantum correlations are contained in the almost-quantum relaxation; set inclusion is not evidence selecting that relaxation.",
        "kinematics_are_real": "The (2,2,2) quantum correlator projection is real-realizable by unit vectors; this is not a full real operational theory.",
        "complex_is_dynamical": "Compatible forms describe a complex-linear dynamical family; reversibility alone does not select the complex field.",
        "verdict": "Real correlator coordinates, real quantum theory and almost-quantum correlations are different claims; these examples select none as physical reality.",
        "scope": {
            "empirical_data_analyzed": False,
            "real_correlators_equal_almost_quantum": False,
            "complex_field_selected": False,
        },
    }


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "Conditional compatible-form identity and field-selection counterexample",
        "deliverables": {
            "D=G+iΩ": "MATH — Hermitian decomposition of an admitted complex matrix",
            "real positive kernels can interfere": "MATH — explicit normalized example",
            "O(2m) ∩ Sp(2m,R)=U(m) for compatible forms": "MATH — supplied G=I, Ω=J0",
            "reversibility does not force J²=-I": "MATH — D_t counterexample",
        },
        "scope": {"compatibility_assumed": True, "complex_field_selected": False,
                  "empirical_exclusion_performed": False},
        "not_derived_here": [
            "physical availability and compatibility of G and Ω",
            "selection of complex rather than real or quaternionic operational theory",
            "the realized dynamics or a physical reversible generator",
        ],
        "status": "CONDITIONAL_COMPATIBLE_FAMILY; FIELD_SELECTION_NOT_DERIVED",
    }


# ── End-to-end ──────────────────────────────────────────────────────────────


def run_why_complex() -> dict:
    return {
        "real_part_gives_real_qm": real_part_gives_real_qm(),
        "complex_structure": complex_structure(m=2),
        "reversible_dynamics_require_complex": reversible_dynamics_require_complex(m=2),
        "why_not_quaternions": why_not_quaternions(),
        "connection_to_observation": connection_to_observation(),
        "counterexample": reversible_form_counterexample(),
        "certificate": derivation_certificate(),
        "interpretation": (
            "Real positive kernels can interfere. The chosen compatible forms give "
            "J²=-I and U(m); a positive reversible counterexample violates J²=-I. "
            "Compatibility, scalar-field selection and physical dynamics remain additional obligations."
        ),
    }


def reversible_form_counterexample(t: float = 0.5) -> dict:
    """Normalized positive D_t with form-preserving rotations but J² != -I."""
    if isinstance(t, bool) or not math.isfinite(t) or not 0 < t < 1:
        raise ValueError("t must be finite and strictly between zero and one")
    J0 = standard_symplectic(1)
    G = [[0.5, 0.0], [0.0, 0.5]]
    omega = _scale(t / 2, J0)
    D = [[complex(G[i][j], omega[i][j]) for j in range(2)] for i in range(2)]
    J = _matmul(_inverse(G), omega)
    squared = _matmul(J, J)
    rotation = J0
    preserved = all(
        _frob([[actual[i][j] - form[i][j] for j in range(2)] for i in range(2)]) < 1e-12
        for form in (G, omega)
        for actual in [_matmul(_matmul(_transpose(rotation), form), rotation)]
    )
    return {
        "kernel": D, "eigenvalues": ((1 - t) / 2, (1 + t) / 2),
        "J": J, "J_squared": squared, "rotation_preserves_both_forms": preserved,
        "J_squared_equals_minus_I": all(
            abs(squared[i][j] + (1 if i == j else 0)) < 1e-12
            for i in range(2) for j in range(2)),
        "complex_field_selected": False,
    }
