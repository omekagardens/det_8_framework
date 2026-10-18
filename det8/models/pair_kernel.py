"""
DET v8.1 — Quadratic Commit Theorem (T2b)

The "given grade-2" half of T2: from a strongly-positive, Hermitian,
biadditive, normalized pair-kernel 𝔇 on the event algebra, derive

  - μ(A) = 𝔇(A,A) ≥ 0                     (nonnegativity)
  - I_3(A,B,C) = 0                         (no third-order interference)
  - 𝔇(A,B) = ⟨v_A, v_B⟩,  μ(A) = ‖v_A‖²     (Gram / norm-squared representation)
  - K_𝒫(i) = 𝔇(A_i,A_i)                    (commit kernel on a recordable partition)
  - additivity on decoherent partitions     (the classical limit)
  - composition closure                     (tensor product of pair-kernels)

DERIVATION CERTIFICATE (honest provenance):

  pair-kernel axioms            MATH   — decoherence functional, quantum measure
                                         theory (Sorkin et al.); credited, not new.
  μ ≥ 0                         TH-DET — from strong positivity + Hermiticity.
  I_3 = 0                       TH-DET — from biadditivity alone.
  Gram / norm-squared           MATH   — spectral theorem (Cholesky/LDL†).
  classical additivity          TH-DET — from the decoherence definition.
  composition closure           MATH   — Kronecker product of PSD matrices.

  T2b assumes pairwise structure and strong positivity separately. Vanishing
  third-order interference does not establish strong positivity. Under these
  supplied axioms the finite Gram and event-weight identities follow; this
  module does not select the pair-kernel premises, physically available
  operations, or the full quantum framework.

This is a DET-native module: it uses no standard-physics constants, only the
event algebra and the pair-kernel 𝔇.
"""

from __future__ import annotations

import math
import random
from numbers import Complex, Real


def _tolerance(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("tolerance must be a finite nonnegative real number")
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError("tolerance must be a finite nonnegative real number")
    return value


def _finite_complex(value) -> bool:
    try:
        return (isinstance(value, Complex) and not isinstance(value, bool)
                and math.isfinite(value.real) and math.isfinite(value.imag))
    except (OverflowError, ValueError):
        return False


# ── Pair kernel (decoherence functional) on a finite Ω ─────────────────────


class PairKernel:
    """A finite-dimensional pair-kernel 𝔇 on Ω = {0,…,n−1}.

    Represented by an n×n Hermitian positive-semidefinite matrix D with
    Σ_{ij} D_ij = 1, so that 𝔇(A,B) = Σ_{i∈A, j∈B} D_ij. Biadditivity is
    automatic from this linear form. Construction checks finite, nonempty square
    numeric data; ``validate`` separately diagnoses the kernel axioms. Numerical
    PSD validation is a tolerance-qualified Gram factorization, not an exact
    strong-positivity certificate. This remains an experimental research model.
    """

    def __init__(self, D: list[list[complex]]):
        n = len(D)
        if n == 0 or any(len(row) != n for row in D):
            raise ValueError("D must be nonempty and square")
        if any(not _finite_complex(value) for row in D for value in row):
            raise ValueError("D entries must be finite real or complex numbers")
        self.n = n
        self.D = [[complex(value) for value in row] for row in D]

    # -- event helpers ------------------------------------------------------
    @staticmethod
    def _as_set(event) -> frozenset:
        if isinstance(event, frozenset):
            return event
        return frozenset(event)

    def omega(self) -> frozenset:
        return frozenset(range(self.n))

    def _partition(self, partition) -> list[frozenset]:
        """Require nonempty, disjoint cells covering this carrier exactly."""
        cells = []
        seen = set()
        for cell in partition:
            values = list(cell)
            if not values or any(type(i) is not int or not 0 <= i < self.n
                                 for i in values):
                raise ValueError("partition cells must contain carrier indices")
            block = frozenset(values)
            if len(block) != len(values) or seen.intersection(block):
                raise ValueError("partition cells must be disjoint without duplicates")
            cells.append(block)
            seen.update(block)
        if not cells or seen != set(range(self.n)):
            raise ValueError("partition must cover the entire carrier")
        return cells

    def _finite_matrix(self) -> bool:
        return (len(self.D) == self.n
                and all(len(row) == self.n for row in self.D)
                and all(_finite_complex(value) for row in self.D for value in row))

    # -- the pair-kernel value ---------------------------------------------
    def D_value(self, A, B) -> complex:
        A = self._as_set(A)
        B = self._as_set(B)
        return sum(self.D[i][j] for i in A for j in B)

    def mu(self, A) -> float:
        """Quadratic possibility weight μ(A) = 𝔇(A,A)."""
        v = self.D_value(A, A)
        # μ is real and ≥ 0 for a valid pair-kernel; return the real part.
        return v.real

    # -- axiom validation ---------------------------------------------------
    def is_hermitian(self, tol: float = 1e-10) -> bool:
        """Check Hermiticity with absolute entrywise tolerance ``tol``."""
        tol = _tolerance(tol)
        return self._finite_matrix() and all(
            abs(self.D[i][j] - self.D[j][i].conjugate()) <= tol
            for i in range(self.n) for j in range(self.n))

    def is_normalized(self, tol: float = 1e-10) -> bool:
        """Check total-entry mass one with absolute tolerance ``tol``."""
        tol = _tolerance(tol)
        return self._finite_matrix() and abs(
            sum(self.D[i][j] for i in range(self.n) for j in range(self.n)) - 1.0
        ) <= tol

    def is_positive_semidefinite(self, tol: float = 1e-12) -> bool:
        """Numerical PSD check, including singular matrices; see ``cholesky``."""
        tol = _tolerance(tol)
        try:
            self.cholesky(tol=tol)
            return True
        except ValueError:
            return False

    def validate(self) -> dict:
        hermitian = self.is_hermitian()
        normalized = self.is_normalized()
        psd = self.is_positive_semidefinite()
        return {
            "hermitian": hermitian,
            "normalized": normalized,
            "psd": psd,
            "valid": hermitian and normalized and psd,
        }

    # -- third-order interference -------------------------------------------
    def interference_I3(self, A, B, C) -> float:
        """I_3(A,B,C) = μ(A∪B∪C) − μ(A∪B) − μ(A∪C) − μ(B∪C) + μ(A) + μ(B) + μ(C).

        Grade-2 ⇒ this vanishes identically.
        """
        A, B, C = map(self._as_set, (A, B, C))
        return (self.mu(A | B | C) - self.mu(A | B) - self.mu(A | C)
                - self.mu(B | C) + self.mu(A) + self.mu(B) + self.mu(C))

    # -- Gram representation (norm-squared as a theorem) --------------------
    def cholesky(self, tol: float = 1e-12) -> list[list[complex]]:
        """Return a pivoted Gram factor L with D approximately equal to L L†.

        Rows retain the original event order. Because of pivoting, L is not
        generally lower-triangular; callers may use its rows as Gram vectors,
        not as a triangular solver. Zero columns represent null directions.

        Finite Hermitian input is required up to ``tol * scale``, where scale
        is the largest absolute real or imaginary entry component. The same
        entrywise error bounds the reconstructed matrix: directions
        beneath that numerical resolution may be discarded. Thus acceptance
        certifies a nearby PSD matrix, not exact PSD of the supplied floats.
        No normalization or change to the stored D is performed.
        """
        tol = _tolerance(tol)
        if not self._finite_matrix():
            raise ValueError("D must remain a finite square matrix")
        n = self.n
        scale = max(max(abs(value.real), abs(value.imag))
                    for row in self.D for value in row)
        L = [[0j] * n for _ in range(n)]
        if scale == 0:
            return L
        A = [[value / scale for value in row] for row in self.D]
        if any(abs(A[i][j] - A[j][i].conjugate()) > tol
               for i in range(n) for j in range(n)):
            raise ValueError("D must be Hermitian within the factorization tolerance")
        remaining = list(range(n))
        for k in range(n):
            diagonal = {i: A[i][i].real - sum(abs(L[i][j]) ** 2 for j in range(k))
                        for i in remaining}
            if any(value < -tol for value in diagonal.values()):
                raise ValueError("D is not positive semidefinite within tolerance")
            pivot = max(remaining, key=diagonal.__getitem__)
            if diagonal[pivot] <= tol:
                break
            L[pivot][k] = math.sqrt(diagonal[pivot])
            remaining.remove(pivot)
            for i in remaining:
                residual = A[i][pivot] - sum(
                    L[i][j] * L[pivot][j].conjugate() for j in range(k))
                L[i][k] = residual / L[pivot][k]
        if any(abs(A[i][j] - sum(L[i][k] * L[j][k].conjugate()
                                 for k in range(n))) > tol
               for i in range(n) for j in range(n)):
            raise ValueError("D has no PSD factor within the entrywise tolerance")
        root_scale = math.sqrt(scale)
        return [[value * root_scale for value in row] for row in L]

    def gram_vectors(self) -> list[list[complex]]:
        """Rows of L give vectors v_i with 𝔇({i},{j}) = ⟨v_i, v_j⟩."""
        return self.cholesky()

    def gram_check(self, tol: float = 1e-9) -> dict:
        """Verify 𝔇(A,B) = ⟨v_A, v_B⟩ and μ(A) = ‖v_A‖² for all events."""
        L = self.cholesky()
        v = [L[i] for i in range(self.n)]  # v_i = row i of L

        def _vec(event) -> list[complex]:
            event = self._as_set(event)
            m = len(v[0])
            return [sum(v[i][k] for i in event) for k in range(m)]

        def _inner(u, w) -> complex:
            return sum(u[k] * w[k].conjugate() for k in range(len(u)))

        max_delta = 0.0
        # Check all pairs of events (n small: 2^n events).
        events = []
        for mask in range(1 << self.n):
            events.append(frozenset(i for i in range(self.n) if mask >> i & 1))
        for A in events:
            for B in events:
                true = self.D_value(A, B)
                est = _inner(_vec(A), _vec(B))
                max_delta = max(max_delta, abs(true - est))
        return {"max_abs_error": max_delta,
                "gram_holds": max_delta < tol,
                "mu_is_norm_squared": max_delta < tol}

    # -- commit kernel on a partition ---------------------------------------
    def commit_kernel(self, partition) -> list[float]:
        """Return weights only for a valid, exactly recordable full partition.

        Cross-cell values must be exactly zero in the supplied arithmetic;
        ``is_decoherent(tol=...)`` is only an approximate diagnostic. The
        matrix axioms and unit total are also checked numerically. Raw event
        weights remain available through ``mu``; they are never renormalized
        into probabilities here. Nonempty cells of zero weight are retained.
        """
        partition = self._partition(partition)
        if not self.validate()["valid"]:
            raise ValueError("commit requires a normalized Hermitian PSD pair-kernel")
        if not self.is_decoherent(partition, tol=0.0):
            raise ValueError("commit requires an exactly decoherent partition")
        weights = [self.mu(A) for A in partition]
        if (any(not math.isfinite(p) or not 0 <= p <= 1 for p in weights)
                or abs(math.fsum(weights) - 1.0) > 1e-10):
            raise ValueError("record weights must be nonnegative and sum to one")
        return weights

    def is_decoherent(self, partition, tol: float = 1e-9) -> bool:
        """Diagnose cross-cell decoherence; positive tol is approximate only."""
        tol = _tolerance(tol)
        partition = self._partition(partition)
        return all(abs(self.D_value(partition[i], partition[j])) <= tol
                   for i in range(len(partition))
                   for j in range(len(partition)) if i != j)

    def classical_additivity(self, partition, tol: float = 1e-9) -> dict:
        """Compare additivity and decoherence; decoherence suffices, not conversely.

        Scalar additivity can result from cancellation of cross terms, including
        purely imaginary ones. It does not license a record partition. Both
        booleans below are numerical diagnostics at the stated absolute tolerance.
        ``consistent`` allows the sum of all cross-cell tolerance contributions;
        approximate decoherence need not imply additivity at that same tolerance.
        """
        tol = _tolerance(tol)
        partition = self._partition(partition)
        union = frozenset().union(*partition) if partition else frozenset()
        lhs = self.mu(union)
        rhs = sum(self.mu(A) for A in partition)
        decoherent = self.is_decoherent(partition, tol)
        additive = abs(lhs - rhs) <= tol
        cross_budget = len(partition) * (len(partition) - 1) * tol
        return {"decoherent": decoherent, "additive": additive,
                "mu_union": lhs, "sum_mu": rhs,
                "consistent": (not decoherent) or abs(lhs - rhs) <= cross_budget + tol,
                "interpretation": (
                    f"μ(⊔A_i)={lhs:.6f} vs Σμ(A_i)={rhs:.6f}; partition "
                    f"{'decoherent' if decoherent else 'not decoherent'}; "
                    f"{'additive' if additive else 'nonadditive'}. "
                    "Additivity alone does not imply decoherence."
                )}

    # -- composition ---------------------------------------------------------
    def compose(self, other: PairKernel) -> PairKernel:
        """Tensor product 𝔇 = 𝔇_self ⊗ 𝔇_other over Ω_self × Ω_other."""
        n1, n2 = self.n, other.n
        N = n1 * n2
        D = [[0j] * N for _ in range(N)]
        for i1 in range(n1):
            for j1 in range(n1):
                for i2 in range(n2):
                    for j2 in range(n2):
                        D[i1 * n2 + i2][j1 * n2 + j2] = self.D[i1][j1] * other.D[i2][j2]
        return PairKernel(D)


# ── Constructors ────────────────────────────────────────────────────────────


def make_pair_kernel(n: int, seed: int = 42, coherent: bool = True) -> PairKernel:
    """Build a valid pair-kernel.

    coherent=True: D = M·M† / sum(M·M†) with M random full-rank complex
                   (general coherent pair-kernel, rank n).
    coherent=False: D = diagonal (fully decohered / classical), D_ii = p_i.
    """
    rng = random.Random(seed)
    if coherent:
        # Random full-rank complex M (n×n).
        M = [[complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
             for _ in range(n)]
        # D = M M† (Hermitian PSD, full rank), then normalize by the FULL sum.
        D = [[0j] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                D[i][j] = sum(M[i][k] * M[j][k].conjugate() for k in range(n))
        total = sum(D[i][j].real for i in range(n) for j in range(n))
        D = [[D[i][j] / total for j in range(n)] for i in range(n)]
    else:
        p = [rng.random() for _ in range(n)]
        tot = sum(p)
        p = [x / tot for x in p]
        D = [[(p[i] if i == j else 0j) for j in range(n)] for i in range(n)]
    return PairKernel(D)


def make_decoherent_partition(n: int) -> list[frozenset]:
    """A two-block partition that is decoherent for a block-diagonal D."""
    half = n // 2
    return [frozenset(range(half)), frozenset(range(half, n))]


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    """Provenance of each T2b deliverable (honest classification)."""
    return {
        "theorem": "T2b — Quadratic Commit Theorem (given grade-2)",
        "deliverables": {
            "pair-kernel axioms (Hermiticity, biadditivity, normalization, strong positivity)": "MATH — decoherence functional / quantum measure theory (Sorkin et al.), credited",
            "μ(A) = 𝔇(A,A) ≥ 0": "TH-DET — from strong positivity + Hermiticity",
            "I_3 = 0 (no third-order interference)": "TH-DET — from biadditivity alone",
            "Gram representation 𝔇(A,B)=⟨v_A,v_B⟩, μ(A)=‖v_A‖²": "MATH — spectral theorem / Cholesky",
            "classical additivity on decoherent partitions": "TH-DET — from the decoherence definition",
            "composition closure (tensor product)": "MATH — Kronecker product of PSD matrices",
        },
        "not_derived_here": [
            "the grade-2 (pairwise) restriction — that is T2a (a priori) or §7.2 (empirical I_3=0)",
            "the complex field ℂ (why not ℝ or ℍ) — open",
            "the full Born rule (event/projector structure, measurements, contexts)",
            "the quantum correlation set (T6) — strong positivity does not isolate it",
        ],
        "status": "MATH/TH-DET implemented; the DET-native forcing theorem (T2a) is still open.",
    }


# ── End-to-end T2b ──────────────────────────────────────────────────────────


def run_t2b(n: int = 4, seed: int = 42) -> dict:
    """Demonstrate T2b on a coherent pair-kernel and a classical (diagonal) one."""
    D = make_pair_kernel(n, seed=seed, coherent=True)
    valid = D.validate()

    # I_3 on two disjoint triples → 0 (I_3 is only defined for disjoint events).
    i3_disjoint = D.interference_I3({0}, {1}, {2})
    i3_disjoint2 = D.interference_I3({1}, {2}, {3})

    gram = D.gram_check()

    # Interference present on the (coherent) two-block partition.
    part = make_decoherent_partition(n)
    coherent_partition_check = D.classical_additivity(part)

    # Classical limit: diagonal pair-kernel → additive on every partition.
    Dc = make_pair_kernel(n, seed=seed, coherent=False)
    classical_check = Dc.classical_additivity(part)

    # Composition closure.
    D2 = make_pair_kernel(3, seed=seed + 1, coherent=True)
    composed = D.compose(D2)
    comp_valid = composed.validate()

    cert = derivation_certificate()

    return {
        "n": n,
        "axioms_valid": valid,
        "I3_disjoint": i3_disjoint,
        "I3_disjoint2": i3_disjoint2,
        "gram": gram,
        "coherent_partition": coherent_partition_check,
        "classical_partition": classical_check,
        "composition_valid": comp_valid,
        "certificate": cert,
        "interpretation": (
            f"Pair-kernel valid: {valid['valid']}. I_3 = {i3_disjoint:.1e} (grade-2). "
            f"Gram representation holds: {gram['gram_holds']}. "
            f"Coherent partition additive: {coherent_partition_check['additive']} "
            f"(interference present). Classical (diagonal) additive: {classical_check['additive']}. "
            f"Composition closed: {comp_valid['valid']}."
        ),
    }
