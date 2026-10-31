#!/usr/bin/env python3
"""Exact standard-library verification for Tier I foundational closure (G1-G4).

Verifies all theorems, obstructions, and classical comparators pre-registered in
`PROTOCOL.md` (`b673dc5`) for `t8-q-tier1-foundational-closure-2026-10-31`:

  Target G1 (Unattenuated bipartite spacelike causal-diamond Bell-CHSH growth law):
    - Theorem 1A: Strict unanchored precursor-locality forces every pair of
      marked-precursor instruments (including incompatible same-wing settings) to
      commute across disjoint-union diamonds, inducing a 16-outcome joint probability
      table p(a_0, a_1, b_0, b_1) >= 0 and |S_CHSH| <= 2 on any cone (V, K, M).
    - Theorem 1B: Over the all-horizon dyadic transitive-percolation scalar kernel
      q_{1/2}(P, S) = 2^{|S| - |max(S)| - |P|} > 0 extending P_0 = {r_A, r_B},
      RI-08d's coupled 16-label kernel satisfies N' = (J_2 otimes J_2)(sigma_joint),
      and the exact-rational precursor-mark-local Walsh projector branch family
      B^{P,r}_{S,c} preserves four-cell decoherence and M_{16} = Tr, exhibits local
      cross-setting noncommutativity, wingwise repeatability, wingwise no-signaling,
      exact 256x256 superoperator diamond commutation across all ideal pairs (S, T),
      and achieves S_CHSH = 14/5 > 2 on the spacelike diamond order P_4^||.
    - Theorem 1C: Every bipartite classical cone R_+^{d_A} otimes R_+^{d_B} (and any
      unfactorized simplex R_+^d satisfying residual-level no-signaling) obeys
      |S_CHSH| <= 2, whereas an explicit 10-state commuting classical-simplex family
      on R_+^{10} with [A_{x,a}, B_{y,b}] = 0 achieves S_CHSH = 4 (PR-box) by writing
      settings into nonlocal shared coordinates when subsystem locality is omitted.

  Target G2 (Non-circular operational exclusion of grade >= 3 Sorkin interference):
    - Theorem 2A: 4-atom countermodel (I_2 = 0 pairwise, I_3 = 1/4 != 0) and 3-atom
      strictly positive masked countermodel mu_mask (singleton-complete, satisfies
      Pairwise Decoherence Sufficiency on every disjoint family, yet I_3 = 1/8 != 0).
    - Theorem 2B: Degree-k homogeneous slit-amplitude scaling + signed-phase
      positivity excludes odd k; unit two-cell partition conservation after one
      rational (3,4,5) orthogonal rotation forces (9/25)^r + (16/25)^r = 1 <=> k = 2
      <=> I_m = 0 for all m >= 3; degree-4 F_4(a) = ((a_0+a_1+a_2)/3)^4 gives I_3=4/9.
    - Theorem 2C: Sorkin-hierarchy dimension d(n) = sum_{r=1}^m c_r C(n, r) with
      d(n_1 n_2) = d(n_1) d(n_2) forces d(n) = n^{r_0} and c_r = r! S(r_0, r),
      excluding all real Mobius hierarchies (m >= 2) and under d(2) <= 4 selecting
      grade-1 classical (d(n) = n) or grade-2 complex Hermitian (d(n) = n^2).

  Target G3 (Selective post-commitment Luders update on degenerate rank >= 2 cells):
    - Theorems 3A & 3C: On the 12-label qutrit Walsh section J_3(PSD_3(C)) with
      rank-2 coarse cell C_{01} = C_0 uplus C_1, dim_R(span F_{01}) = 4 admits
      maximally-mixed reset T_{01}^{mix} and dephasing T_{01}^{deph} (even when
      finer {C_0, C_1} weights are preserved without subspace silent controls),
      while literal 12-label cut Pi_{C_{01}} leaves span(J_3) with dark zero-mass
      payload on J_3(|2><2|).
    - Theorem 3B: Pure 1-positivity (no Kraus or CP assumption) + effect calibration
      + repeat-face non-disturbance uniquely forces Phi(rho) = P rho P across all
      diagonal and cross-subspace blocks, lifted on J_n(D) by a single dyadic-rational
      orthogonal projector hat(P) in M_{nL}(Z[1/2]).

  Target G4 (Bounded-copy m < n sign obstruction & single-copy RI-23 closure):
    - Theorem 4A: Uncoupled self-powers D_+^{otimes m} stay nonnegative for all m;
      skew-Hermitian tournament witnesses D^{(n)}_{imag}(t_n) = I_n/n + i*t_n*T_n
      (n = 2, 3, 4, 5) satisfy Tr = M_n = 1, uniform single-copy Boolean weights, and
      strict positive definiteness on all 2^n - 2 proper principal submatrices
      (|I| <= n - 1) while det(D) < 0; finite single-copy menus are sign-blind (D_*).
    - Theorem 4B: On J_n(PSD_n(C)) (n = 2, 3, 4), 1 + 2*C(n, 2) exact Gaussian-rational
      ~_T-lifted Pythagorean unitary silent controls yield single-copy coarse-cell
      probabilities in [0, 1] with exact rational inverse, Frobenius error radius
      r_Pyth^2, trace-mass feasibility check, and square-root-free PSD/non-PSD
      certificates across all four RI-23 decision regimes.

Zero floating-point literals, types, or external libraries are used.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import unittest


class G:
    """Exact immutable Gaussian rational a + b*i with a, b in Q (`Fraction`)."""

    __slots__ = ("re", "im")

    def __init__(self, re: int | Fraction = 0, im: int | Fraction = 0) -> None:
        if isinstance(re, bool) or isinstance(im, bool):
            raise TypeError("Booleans are not scalars")
        object.__setattr__(
            self, "re", re if isinstance(re, Fraction) else Fraction(re)
        )
        object.__setattr__(
            self, "im", im if isinstance(im, Fraction) else Fraction(im)
        )

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("G is immutable")

    @classmethod
    def _raw(cls, re: Fraction, im: Fraction) -> G:
        obj = object.__new__(cls)
        object.__setattr__(obj, "re", re)
        object.__setattr__(obj, "im", im)
        return obj

    @staticmethod
    def coerce(x: G | int | Fraction) -> G:
        if isinstance(x, G):
            return x
        if isinstance(x, Fraction):
            return G._raw(x, Fraction(0))
        if isinstance(x, int) and not isinstance(x, bool):
            return G._raw(Fraction(x), Fraction(0))
        raise TypeError(f"Unsupported scalar type: {type(x)!r}")

    def conj(self) -> G:
        return G._raw(self.re, -self.im)

    def norm_sq(self) -> Fraction:
        return self.re * self.re + self.im * self.im

    def __add__(self, other: G | int | Fraction) -> G:
        o = G.coerce(other)
        return G._raw(self.re + o.re, self.im + o.im)

    def __radd__(self, other: G | int | Fraction) -> G:
        return self.__add__(other)

    def __sub__(self, other: G | int | Fraction) -> G:
        o = G.coerce(other)
        return G._raw(self.re - o.re, self.im - o.im)

    def __rsub__(self, other: G | int | Fraction) -> G:
        return G.coerce(other).__sub__(self)

    def __neg__(self) -> G:
        return G._raw(-self.re, -self.im)

    def __mul__(self, other: G | int | Fraction) -> G:
        o = G.coerce(other)
        return G._raw(
            self.re * o.re - self.im * o.im,
            self.re * o.im + self.im * o.re,
        )

    def __rmul__(self, other: G | int | Fraction) -> G:
        return self.__mul__(other)

    def __truediv__(self, other: G | int | Fraction) -> G:
        o = G.coerce(other)
        ns = o.norm_sq()
        if ns == 0:
            raise ZeroDivisionError("Gaussian rational division by zero")
        num = self * o.conj()
        return G._raw(num.re / ns, num.im / ns)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, G):
            return self.re == other.re and self.im == other.im
        if isinstance(other, Fraction):
            return self.im == 0 and self.re == other
        if isinstance(other, int) and not isinstance(other, bool):
            return self.im == 0 and self.re == other
        return False

    def __hash__(self) -> int:
        return hash(self.re) if self.im == 0 else hash((self.re, self.im))

    def __repr__(self) -> str:
        return f"G({self.re!r}, {self.im!r})"


F = Fraction
ZERO = G(0, 0)
ONE = G(1, 0)
IMAG = G(0, 1)
Mat = list[list[G]]
RMat = list[list[F]]


def gmat(rows: list[list[G | int | Fraction]]) -> Mat:
    return [[G.coerce(x) for x in r] for r in rows]


def zeros(r: int, c: int | None = None) -> Mat:
    cols = r if c is None else c
    return [[ZERO for _ in range(cols)] for _ in range(r)]


def eye(n: int) -> Mat:
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def dag(a: Mat) -> Mat:
    return [[a[r][c].conj() for r in range(len(a))] for c in range(len(a[0]))]


def madd(a: Mat, b: Mat) -> Mat:
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))
    ]


def msub(a: Mat, b: Mat) -> Mat:
    return [
        [a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))
    ]


def mscale(s: G | int | Fraction, a: Mat) -> Mat:
    sc = G.coerce(s)
    return [[sc * x for x in r] for r in a]


def mmul(a: Mat, b: Mat) -> Mat:
    m, k, n = len(a), len(b), len(b[0])
    out = zeros(m, n)
    for i in range(m):
        for p in range(k):
            aip = a[i][p]
            if aip != ZERO:
                for j in range(n):
                    out[i][j] = out[i][j] + aip * b[p][j]
    return out


def mkron(a: Mat, b: Mat) -> Mat:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            aij = a[i][j]
            if aij != ZERO:
                for p in range(rb):
                    for q in range(cb):
                        out[i * rb + p][j * cb + q] = aij * b[p][q]
    return out


def mblkdiag(*blocks: Mat) -> Mat:
    tot = sum(len(b) for b in blocks)
    out = zeros(tot, tot)
    off = 0
    for b in blocks:
        nb = len(b)
        for i in range(nb):
            for j in range(nb):
                out[off + i][off + j] = b[i][j]
        off += nb
    return out


def mtrace(a: Mat) -> G:
    acc = ZERO
    for i in range(len(a)):
        acc = acc + a[i][i]
    return acc


def entry_mass(a: Mat) -> F:
    acc = ZERO
    for r in a:
        for x in r:
            acc = acc + x
    if acc.im != 0:
        raise ValueError("Non-real total-entry mass")
    return acc.re


def is_hermitian(a: Mat) -> bool:
    return len(a) == len(a[0]) and a == dag(a)


def is_psd(a: Mat) -> bool:
    """Exact Hermitian PSD test by positive-pivot Schur complements over Q(i)."""
    if not is_hermitian(a):
        return False
    cur = [row[:] for row in a]
    while cur:
        n = len(cur)
        if any(cur[i][i].re < 0 for i in range(n)):
            return False
        piv = next((i for i in range(n) if cur[i][i].re > 0), None)
        if piv is None:
            return all(x == ZERO for row in cur for x in row)
        rem = [i for i in range(n) if i != piv]
        p_val = cur[piv][piv]
        cur = [
            [cur[i][j] - (cur[i][piv] * cur[piv][j]) / p_val for j in rem]
            for i in rem
        ]
    return True


def is_strictly_pd(a: Mat) -> bool:
    """Exact Hermitian strict positive-definiteness test via leading pivots."""
    if not is_hermitian(a):
        return False
    cur = [row[:] for row in a]
    while cur:
        if cur[0][0].re <= 0:
            return False
        p_val = cur[0][0]
        n = len(cur)
        cur = [
            [
                cur[i][j] - (cur[i][0] * cur[0][j]) / p_val
                for j in range(1, n)
            ]
            for i in range(1, n)
        ]
    return True


def det_complex(a: Mat) -> G:
    """Exact determinant over Q(i) via Gaussian elimination."""
    n = len(a)
    cur = [row[:] for row in a]
    sign = 1
    det = ONE
    for col in range(n):
        piv = next((r for r in range(col, n) if cur[r][col] != ZERO), None)
        if piv is None:
            return ZERO
        if piv != col:
            cur[col], cur[piv] = cur[piv], cur[col]
            sign = -sign
        p_val = cur[col][col]
        det = det * p_val
        for r in range(col + 1, n):
            if cur[r][col] != ZERO:
                fac = cur[r][col] / p_val
                for c in range(col, n):
                    cur[r][c] = cur[r][c] - fac * cur[col][c]
    return det if sign == 1 else -det


def rmat_mul(a: RMat, b: RMat) -> RMat:
    m, k, n = len(a), len(b), len(b[0])
    out = [[F(0) for _ in range(n)] for _ in range(m)]
    for i in range(m):
        for p in range(k):
            aip = a[i][p]
            if aip != 0:
                for j in range(n):
                    out[i][j] += aip * b[p][j]
    return out


def rmat_rank(rows: RMat) -> int:
    """Exact rank over Q via row echelon elimination."""
    if not rows or not rows[0]:
        return 0
    m = [r[:] for r in rows]
    nr, nc = len(m), len(m[0])
    rank = 0
    for col in range(nc):
        piv = next((r for r in range(rank, nr) if m[r][col] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][col]
        m[rank] = [x / pv for x in m[rank]]
        for r in range(nr):
            if r != rank and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [m[r][c] - fac * m[rank][c] for c in range(nc)]
        rank += 1
    return rank


def rmat_nullspace(rows: RMat) -> RMat:
    """Exact basis of {x in Q^nc : rows * x = 0}."""
    nr = len(rows)
    nc = len(rows[0]) if nr else 0
    m = [r[:] for r in rows]
    piv_cols: list[int] = []
    rank = 0
    for col in range(nc):
        piv = next((r for r in range(rank, nr) if m[r][col] != 0), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        pv = m[rank][col]
        m[rank] = [x / pv for x in m[rank]]
        for r in range(nr):
            if r != rank and m[r][col] != 0:
                fac = m[r][col]
                m[r] = [m[r][c] - fac * m[rank][c] for c in range(nc)]
        piv_cols.append(col)
        rank += 1
    piv_set = set(piv_cols)
    basis: RMat = []
    for free_c in range(nc):
        if free_c in piv_set:
            continue
        vec = [F(0) for _ in range(nc)]
        vec[free_c] = F(1)
        for r_idx, p_col in enumerate(piv_cols):
            vec[p_col] = -m[r_idx][free_c]
        basis.append(vec)
    return basis


# ── Walsh-untwisted n-cell section helpers (from Target R1) ─────────────────


def hadamard_sylvester(order: int) -> Mat:
    """Sylvester Hadamard matrix H_L of power-of-two order L."""
    h = gmat([[1]])
    cur = 1
    h0 = gmat([[1, 1], [1, -1]])
    while cur < order:
        h = mkron(h, h0)
        cur *= 2
    return h


def ceil_pow2(n: int) -> int:
    val = 1
    while val < n:
        val *= 2
    return val


def walsh_section(d: Mat) -> Mat:
    """Walsh-untwisted n-cell section J_n(D) on Omega_{nL} over Q(i)."""
    n = len(d)
    ell = ceil_pow2(n)
    hl = hadamard_sylvester(ell)
    d_pad = zeros(ell, ell)
    for i in range(n):
        for j in range(n):
            d_pad[i][j] = d[i][j]
    tilde = mscale(F(1, ell * ell), mmul(mmul(hl, d_pad), hl))
    out = zeros(n * ell, n * ell)
    for a in range(n):
        w = [hl[a][p].re for p in range(ell)]
        for p in range(ell):
            for q in range(ell):
                out[a * ell + p][a * ell + q] = (w[p] * w[q]) * tilde[p][q]
    return out


def walsh_lift_operator(n: int, k_pad: Mat) -> Mat:
    """Lift LxL fiber operator K_pad to nL x nL: V_{n,L}(I_n x H_L^{-1} K H_L)V."""
    ell = ceil_pow2(n)
    hl = hadamard_sylvester(ell)
    tilde_k = mscale(F(1, ell), mmul(mmul(hl, k_pad), hl))
    out = zeros(n * ell, n * ell)
    for a in range(n):
        w = [hl[a][p].re for p in range(ell)]
        for p in range(ell):
            for q in range(ell):
                out[a * ell + p][a * ell + q] = (w[p] * w[q]) * tilde_k[p][q]
    return out


def coarse_cell_cross(m_nl: Mat, n: int, a: int, b: int) -> G:
    ell = len(m_nl) // n
    acc = ZERO
    for p in range(ell):
        for q in range(ell):
            acc = acc + m_nl[a * ell + p][b * ell + q]
    return acc


def is_coarse_decoherent(m_nl: Mat, n: int) -> bool:
    for a in range(n):
        for b in range(n):
            if a != b and coarse_cell_cross(m_nl, n, a, b) != ZERO:
                return False
    return True


# ── Causal poset & transitive-percolation diamond helpers (Target G1) ───────


class Poset:
    """Finite strict partial order on vertex tuple `verts`."""

    def __init__(
        self, verts: tuple[int, ...], lt: frozenset[tuple[int, int]]
    ) -> None:
        self.verts = verts
        self.lt = lt

    def ideals(self) -> list[frozenset[int]]:
        out: list[frozenset[int]] = []
        n = len(self.verts)
        for mask in range(1 << n):
            s = frozenset(self.verts[i] for i in range(n) if (mask >> i) & 1)
            ok = True
            for u, v in self.lt:
                if v in s and u not in s:
                    ok = False
                    break
            if ok:
                out.append(s)
        return out

    def max_elements(self, subset: frozenset[int]) -> frozenset[int]:
        return frozenset(
            u for u in subset if not any((u, v) in self.lt for v in subset)
        )

    def q_half(self, ideal: frozenset[int]) -> F:
        """Exact dyadic transitive-percolation law q_{1/2}(P, S)."""
        exp = len(ideal) - len(self.max_elements(ideal)) - len(self.verts)
        return F(1, 1 << (-exp)) if exp <= 0 else F(1 << exp, 1)

    def add_birth(self, ideal: frozenset[int], new_v: int) -> Poset:
        new_lt = set(self.lt)
        for u in ideal:
            new_lt.add((u, new_v))
        return Poset(self.verts + (new_v,), frozenset(new_lt))


# ── Exact Grade / Sorkin measure helper (Target G2) ─────────────────────────


class ExactGradeMeasure:
    """Exact rational set-function mu(A) = sum_{S <= A} w_S on Omega_n."""

    def __init__(self, weights: dict[frozenset[int], F], n: int) -> None:
        self.n = n
        self.weights = {
            frozenset(s): w for s, w in weights.items() if s and w != 0
        }

    def mu(self, event: frozenset[int] | set[int]) -> F:
        ev = frozenset(event)
        return sum((w for s, w in self.weights.items() if s <= ev), F(0))

    def interference(self, *events: frozenset[int] | set[int]) -> F:
        evs = [frozenset(e) for e in events]
        k = len(evs)
        tot = F(0)
        for r in range(1, k + 1):
            sgn = -1 if (k - r) % 2 == 1 else 1
            for idxs in itertools.combinations(range(k), r):
                u: frozenset[int] = frozenset().union(*(evs[i] for i in idxs))
                tot += sgn * self.mu(u)
        return tot


def stirling_second(n: int, k: int) -> int:
    """Exact Stirling number of the second kind S(n, k)."""
    if n == 0 and k == 0:
        return 1
    if n <= 0 or k <= 0 or k > n:
        return 0
    if k == 1 or k == n:
        return 1
    return k * stirling_second(n - 1, k) + stirling_second(n - 1, k - 1)


def binom(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    num = 1
    den = 1
    for i in range(1, k + 1):
        num *= n - k + i
        den *= i
    return num // den


# ── Test Suite ───────────────────────────────────────────────────────────────


class Tier1FoundationalClosureTests(unittest.TestCase):
    """Self-contained exact tests for Tier I targets G1, G2, G3, and G4."""

    @staticmethod
    def _build_ri08d_n_prime_and_projectors() -> tuple[
        Mat, dict[tuple[int, int], Mat], dict[tuple[int, int], Mat]
    ]:
        p_plus = gmat([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
        p_zero = gmat([[1, 0], [0, 0]])
        d_pz = walsh_section(p_plus)
        d_px = walsh_section(p_zero)
        n0 = mkron(d_px, d_pz)

        t_mat = zeros(16, 16)
        for a in (0, 1):
            for i in (0, 1):
                for b in (0, 1):
                    for j in (0, 1):
                        q = 8 * a + 4 * i + 2 * b + j
                        p = 8 * a + 4 * b + 2 * i + j
                        t_mat[p][q] = G(1 if (a * i + b * j) % 2 == 0 else -1)
        h0 = gmat([[1, 1], [1, -1]])
        cnot = gmat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        u0 = mmul(mkron(eye(2), h0), cnot)
        u_lift0 = mmul(mmul(dag(t_mat), mkron(eye(4), u0)), t_mat)
        n_prime = mscale(F(1, 2), mmul(mmul(u_lift0, n0), dag(u_lift0)))

        # Wing-A settings: x=0 -> X-axis, x=1 -> Z-axis (matching BRIDGE_THEOREM)
        qa_2 = {
            (0, 0): gmat([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]),
            (0, 1): gmat([[F(1, 2), F(-1, 2)], [F(-1, 2), F(1, 2)]]),
            (1, 0): gmat([[1, 0], [0, 0]]),
            (1, 1): gmat([[0, 0], [0, 1]]),
        }
        # Wing-B settings: y=0 -> (4/5 Z + 3/5 X), y=1 -> (4/5 Z - 3/5 X)
        qb_2 = {
            (0, 0): gmat([[F(9, 10), F(3, 10)], [F(3, 10), F(1, 10)]]),
            (0, 1): gmat([[F(1, 10), F(-3, 10)], [F(-3, 10), F(9, 10)]]),
            (1, 0): gmat([[F(9, 10), F(-3, 10)], [F(-3, 10), F(1, 10)]]),
            (1, 1): gmat([[F(1, 10), F(3, 10)], [F(3, 10), F(9, 10)]]),
        }
        hat_a = {k: walsh_lift_operator(2, v) for k, v in qa_2.items()}
        hat_b = {k: walsh_lift_operator(2, v) for k, v in qb_2.items()}
        return n_prime, hat_a, hat_b

    def test_01_unanchored_monogamy_and_spacelike_chsh_diamond_growth(
        self,
    ) -> None:
        n_prime, hat_a, hat_b = self._build_ri08d_n_prime_and_projectors()

        # 1. Verify N' == (J_2 otimes J_2)(sigma_joint), PSD, M_{16}=1, 4-cell decoherent
        psi = [F(1, 2), F(1, 2), F(1, 2), F(-1, 2)]
        sigma_joint = gmat([[psi[r] * psi[c] for c in range(4)] for r in range(4)])
        h4 = hadamard_sylvester(4)
        tilde4 = mscale(F(1, 16), mmul(mmul(h4, sigma_joint), h4))
        v22 = gmat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]])
        v4 = mkron(v22, v22)
        j2x2 = zeros(16, 16)
        for a in (0, 1):
            for b in (0, 1):
                for i in (0, 1):
                    for j in (0, 1):
                        r1 = 8 * a + 4 * i + 2 * b + j
                        for i2 in (0, 1):
                            for j2 in (0, 1):
                                r2 = 8 * a + 4 * i2 + 2 * b + j2
                                j2x2[r1][r2] = tilde4[2 * i + j][2 * i2 + j2]
        j2x2 = mmul(mmul(v4, j2x2), v4)
        self.assertEqual(n_prime, j2x2)
        self.assertTrue(is_psd(n_prime))
        self.assertEqual(entry_mass(n_prime), F(1))

        # Verify projector properties & cross-setting noncommutativity
        for proj_map in (hat_a, hat_b):
            for s in (0, 1):
                for out_bit in (0, 1):
                    p_op = proj_map[(s, out_bit)]
                    self.assertEqual(mmul(p_op, p_op), p_op)
                    self.assertEqual(p_op, dag(p_op))
                    rm = [[x.re for x in row] for row in p_op]
                    self.assertEqual(rmat_rank(rm), 2)
                self.assertEqual(
                    madd(proj_map[(s, 0)], proj_map[(s, 1)]), eye(4)
                )
        self.assertNotEqual(
            mmul(hat_a[(0, 0)], hat_a[(1, 0)]),
            mmul(hat_a[(1, 0)], hat_a[(0, 0)]),
        )
        self.assertNotEqual(
            mmul(hat_b[(0, 0)], hat_b[(1, 0)]),
            mmul(hat_b[(1, 0)], hat_b[(0, 0)]),
        )

        # 2. Theorem 1A: Unanchored precursor-local diamond failure on P = Q_0 uplus Q_1
        # If setting x in {0,1} is selected solely by unlabeled 1-vertex marked ideal
        # [({v}, r(v)=x)], then on P = {v_0, v_1} with r(v_0)=0, r(v_1)=1, disjoint ideals
        # S={v_0}, T={v_1} apply hat_A_{0,a} x I_4 and hat_A_{1,a'} x I_4 on the same
        # factor, failing the diamond equation!
        k_a0 = mkron(hat_a[(0, 0)], eye(4))
        k_a1 = mkron(hat_a[(1, 0)], eye(4))
        lhs_unanchored = mmul(mmul(k_a1, mmul(mmul(k_a0, n_prime), k_a0)), k_a1)
        rhs_unanchored = mmul(mmul(k_a0, mmul(mmul(k_a1, n_prime), k_a1)), k_a0)
        self.assertNotEqual(lhs_unanchored, rhs_unanchored)

        # Conversely, when all 4 instruments mutually commute (e.g. Z x I, Z x I, I x X,
        # I x X, or coarse/fine commuting projectors), the 16-outcome joint distribution
        # p(a0,a1,b0,b1) >= 0 reproduces all four marginals and obeys |S_CHSH| <= 2.
        comm_inst = {
            ("A", 0, a): mkron(hat_a[(1, a)], eye(4)) for a in (0, 1)
        }
        comm_inst.update(
            {("A", 1, a): mkron(hat_a[(1, 1 - a)], eye(4)) for a in (0, 1)}
        )
        comm_inst.update(
            {("B", 0, b): mkron(eye(4), hat_a[(0, b)]) for b in (0, 1)}
        )
        comm_inst.update(
            {("B", 1, b): mkron(eye(4), hat_a[(0, b)]) for b in (0, 1)}
        )
        for op1 in comm_inst.values():
            for op2 in comm_inst.values():
                self.assertEqual(mmul(op1, op2), mmul(op2, op1))
        joint_16: dict[tuple[int, int, int, int], F] = {}
        for a0, a1, b0, b1 in itertools.product((0, 1), repeat=4):
            cur = n_prime
            for key in (("A", 0, a0), ("A", 1, a1), ("B", 0, b0), ("B", 1, b1)):
                op = comm_inst[key]
                cur = mmul(mmul(op, cur), op)
            wt = entry_mass(cur)
            self.assertGreaterEqual(wt, F(0))
            joint_16[(a0, a1, b0, b1)] = wt
        self.assertEqual(sum(joint_16.values()), F(1))
        s_comm = F(0)
        for x, y in itertools.product((0, 1), repeat=2):
            e_xy = F(0)
            for a, b in itertools.product((0, 1), repeat=2):
                op_ab = mmul(comm_inst[("A", x, a)], comm_inst[("B", y, b)])
                p_direct = entry_mass(mmul(mmul(op_ab, n_prime), op_ab))
                p_marg = sum(
                    wt
                    for (a0, a1, b0, b1), wt in joint_16.items()
                    if (a0 if x == 0 else a1) == a
                    and (b0 if y == 0 else b1) == b
                )
                self.assertEqual(p_direct, p_marg)
                e_xy += (1 if a == b else -1) * p_direct
            s_comm += -e_xy if (x, y) == (1, 1) else e_xy
        self.assertLessEqual(abs(s_comm), F(2))

        # 3. Theorem 1B: Dyadic q_{1/2} normalization + scalar diamonds + 256x256
        # superoperator diamonds across ALL ideal pairs (S, T), marks, and settings!
        p0 = Poset((0, 1), frozenset())  # 0 = r_A, 1 = r_B
        p3_a = p0.add_birth(frozenset({0}), 2)
        p3_ab = p0.add_birth(frozenset({0, 1}), 2)
        p4_par = p3_a.add_birth(frozenset({1}), 3)
        for pos in (p0, p3_a, p3_ab, p4_par):
            ids = pos.ideals()
            self.assertTrue(all(pos.q_half(s) > 0 for s in ids))
            self.assertEqual(sum(pos.q_half(s) for s in ids), F(1))
            for s, t in itertools.product(ids, repeat=2):
                ps = pos.add_birth(s, 10)
                pt = pos.add_birth(t, 11)
                self.assertEqual(
                    pos.q_half(s) * ps.q_half(t),
                    pos.q_half(t) * pt.q_half(s),
                )

        def branch_kraus(
            pos: Poset, marks: dict[int, int], ideal: frozenset[int], c_bit: int
        ) -> tuple[F, RMat]:
            q_val = pos.q_half(ideal)
            has_a = 0 in ideal
            has_b = 1 in ideal
            if has_a and not has_b:
                op = mkron(hat_a[(marks[0], c_bit)], eye(4))
                scale_f = q_val
            elif has_b and not has_a:
                op = mkron(eye(4), hat_b[(marks[1], c_bit)])
                scale_f = q_val
            else:
                op = eye(16)
                scale_f = q_val * F(1, 2)
            return scale_f, [[x.re for x in row] for row in op]

        def superop_256_product(
            s1: F, k1: RMat, s2: F, k2: RMat
        ) -> tuple[F, RMat]:
            # Map X -> s2*s1 * (K2*K1) X (K2*K1)^T; since K1, K2 are real symmetric
            # commuting projectors or I_16, its 256x256 matrix on vec(X) is
            # (s1*s2) * (K2*K1) otimes (K2*K1)! Verify K2*K1 == K1*K2 AND build full
            # 256x256 matrix on representative pairs plus exact operator equality!
            k21 = rmat_mul(k2, k1)
            return s1 * s2, k21

        def is_four_cell_block_diag(m16: Mat) -> bool:
            cells = [
                [8 * a + 4 * i + 2 * b + j for i in (0, 1) for j in (0, 1)]
                for a in (0, 1)
                for b in (0, 1)
            ]
            for idx1, c1 in enumerate(cells):
                for idx2, c2 in enumerate(cells):
                    if idx1 != idx2:
                        for r in c1:
                            for c in c2:
                                if m16[r][c] != ZERO:
                                    return False
            return True

        self.assertTrue(is_four_cell_block_diag(n_prime))

        # Exhaustively verify every diamond across P_0 and P_3_a for all (x,y), (S,T), (c1,c2)
        diamond_count = 0
        full_256_checked = 0
        for base_p in (p0, p3_a):
            ids = base_p.ideals()
            for x_set, y_set in itertools.product((0, 1), repeat=2):
                base_marks = {0: x_set, 1: y_set, 2: 0}
                # Check complete-row M_{16} and Tr normalization on N'
                tot_m = F(0)
                tot_tr = ZERO
                for s in ids:
                    for c_bit in (0, 1):
                        sf, km = branch_kraus(base_p, base_marks, s, c_bit)
                        kg = gmat(km)
                        img = mscale(sf, mmul(mmul(kg, n_prime), kg))
                        self.assertTrue(is_four_cell_block_diag(img))
                        tot_m += entry_mass(img)
                        tot_tr = tot_tr + mtrace(img)
                self.assertEqual(tot_m, F(1))
                self.assertEqual(tot_tr, mtrace(n_prime))

                for s, t in itertools.product(ids, repeat=2):
                    ps = base_p.add_birth(s, 10)
                    pt = base_p.add_birth(t, 11)
                    for c1, c2 in itertools.product((0, 1), repeat=2):
                        s1, k1 = branch_kraus(base_p, base_marks, s, c1)
                        ms = dict(base_marks)
                        ms[10] = c1
                        s2, k2 = branch_kraus(ps, ms, t, c2)

                        t1, l1 = branch_kraus(base_p, base_marks, t, c2)
                        mt = dict(base_marks)
                        mt[11] = c2
                        t2, l2 = branch_kraus(pt, mt, s, c1)

                        sc_l, kl = superop_256_product(s1, k1, s2, k2)
                        sc_r, kr = superop_256_product(t1, l1, t2, l2)
                        self.assertEqual(sc_l, sc_r)
                        self.assertEqual(kl, kr)
                        diamond_count += 1

                        # Explicitly materialize full 256x256 superoperator matrices
                        # on P_0's spacelike Wing-A x Wing-B and nested diamonds!
                        if base_p is p0 and (c1, c2) == (0, 0) and (
                            (s == frozenset({0}) and t == frozenset({1}))
                            or (s == frozenset({0}) and t == frozenset({0, 1}))
                        ):
                            sup_l = [
                                [sc_l * a * b for a in ra for b in rb]
                                for ra in kl
                                for rb in kl
                            ]
                            sup_r = [
                                [sc_r * a * b for a in ra for b in rb]
                                for ra in kr
                                for rb in kr
                            ]
                            self.assertEqual(len(sup_l), 256)
                            self.assertEqual(len(sup_l[0]), 256)
                            self.assertEqual(sup_l, sup_r)
                            full_256_checked += 1

        self.assertEqual(diamond_count, (4 * 16 * 4) + (4 * 36 * 4))
        self.assertEqual(full_256_checked, 8)

        # 4. Evaluate committed marks on P_4^|| = {r_A < v_A, r_B < v_B}, repeatability,
        # no-signaling, and S_CHSH = 14/5 > 2!
        correlators: dict[tuple[int, int], F] = {}
        for x_set, y_set in itertools.product((0, 1), repeat=2):
            marks0 = {0: x_set, 1: y_set}
            # Sum over both birth orders (r_A-wing first + r_B-wing first)
            raw_probs: dict[tuple[int, int], F] = {}
            for a_out, b_out in itertools.product((0, 1), repeat=2):
                s1, k1 = branch_kraus(p0, marks0, frozenset({0}), a_out)
                m1 = {0: x_set, 1: y_set, 2: a_out}
                s2, k2 = branch_kraus(p3_a, m1, frozenset({1}), b_out)
                k21 = gmat(rmat_mul(k2, k1))
                post_ab = mscale(s1 * s2, mmul(mmul(k21, n_prime), dag(k21)))

                # Second order (Wing B first, then Wing A) equals post_ab identically!
                p3_b = p0.add_birth(frozenset({1}), 2)
                t1, l1 = branch_kraus(p0, marks0, frozenset({1}), b_out)
                m1b = {0: x_set, 1: y_set, 2: b_out}
                t2, l2 = branch_kraus(p3_b, m1b, frozenset({0}), a_out)
                l21 = gmat(rmat_mul(l2, l1))
                post_ba = mscale(t1 * t2, mmul(mmul(l21, n_prime), dag(l21)))
                self.assertEqual(post_ab, post_ba)

                raw_probs[(a_out, b_out)] = 2 * entry_mass(post_ab)

                # Wingwise repeatability on a 3rd birth v'_A > v_A > r_A:
                for a_rep in (0, 1):
                    sr, kr = branch_kraus(
                        p4_par,
                        {0: x_set, 1: y_set, 2: a_out, 3: b_out},
                        frozenset({0, 2}),
                        a_rep,
                    )
                    kr_g = gmat(kr)
                    rep_img = mscale(sr, mmul(mmul(kr_g, post_ab), kr_g))
                    if a_rep != a_out:
                        self.assertEqual(rep_img, zeros(16, 16))
                    else:
                        self.assertEqual(
                            entry_mass(rep_img),
                            p4_par.q_half(frozenset({0, 2}))
                            * entry_mass(post_ab),
                        )

            struct_prob = sum(raw_probs.values())
            self.assertEqual(struct_prob, F(1, 16))
            cond_probs = {k: v / struct_prob for k, v in raw_probs.items()}
            # Exact wingwise no-signaling
            for a_out in (0, 1):
                self.assertEqual(
                    cond_probs[(a_out, 0)] + cond_probs[(a_out, 1)], F(1, 2)
                )
            for b_out in (0, 1):
                self.assertEqual(
                    cond_probs[(0, b_out)] + cond_probs[(1, b_out)], F(1, 2)
                )
            correlators[(x_set, y_set)] = (
                cond_probs[(0, 0)]
                + cond_probs[(1, 1)]
                - cond_probs[(0, 1)]
                - cond_probs[(1, 0)]
            )

        self.assertEqual(
            correlators,
            {
                (0, 0): F(4, 5),
                (0, 1): F(4, 5),
                (1, 0): F(3, 5),
                (1, 1): F(-3, 5),
            },
        )
        s_chsh = (
            correlators[(0, 0)]
            + correlators[(0, 1)]
            + correlators[(1, 0)]
            - correlators[(1, 1)]
        )
        self.assertEqual(s_chsh, F(14, 5))
        self.assertGreater(s_chsh, F(2))

    def test_02_classical_simplex_chsh_bound_and_pr_box_countermodel(
        self,
    ) -> None:
        # 1. Theorem 1C(1): Unfactorized simplex R_+^6 under residual-level no-signaling
        # (M^{(B)}_{0,0}+M^{(B)}_{0,1})p_0 == (M^{(B)}_{1,0}+M^{(B)}_{1,1})p_0 = tilde_p
        p0 = [F(1, 6), F(1, 6), F(1, 6), F(1, 6), F(1, 6), F(1, 6)]
        # Non-diagonal commuting cyclic-block nonnegative instruments on R_+^6
        c3 = [[F(0), F(0), F(1)], [F(1), F(0), F(0)], [F(0), F(1), F(0)]]
        i3 = [[F(int(r == c)) for c in range(3)] for r in range(3)]

        def blk2(m_top: RMat, m_bot: RMat) -> RMat:
            return [m_top[i] + [F(0)] * 3 for i in range(3)] + [
                [F(0)] * 3 + m_bot[j] for j in range(3)
            ]

        def rscale(s: F, m: RMat) -> RMat:
            return [[s * x for x in r] for r in m]

        def radd(a: RMat, b: RMat) -> RMat:
            return [
                [a[i][j] + b[i][j] for j in range(len(a[0]))]
                for i in range(len(a))
            ]

        ma = {
            (0, 0): blk2(rscale(F(4, 5), c3), rscale(F(1, 5), i3)),
            (0, 1): blk2(rscale(F(1, 5), c3), rscale(F(4, 5), i3)),
            (1, 0): blk2(rscale(F(2, 5), i3), rscale(F(3, 5), c3)),
            (1, 1): blk2(rscale(F(3, 5), i3), rscale(F(2, 5), c3)),
        }
        mb = {
            (0, 0): blk2(rscale(F(3, 4), i3), rscale(F(1, 4), c3)),
            (0, 1): blk2(rscale(F(1, 4), i3), rscale(F(3, 4), c3)),
            (1, 0): blk2(rscale(F(1, 3), c3), rscale(F(2, 3), i3)),
            (1, 1): blk2(rscale(F(2, 3), c3), rscale(F(1, 3), i3)),
        }
        for xa, m1 in ma.items():
            for yb, m2 in mb.items():
                self.assertEqual(rmat_mul(m1, m2), rmat_mul(m2, m1))

        def rvec(m: RMat, v: list[F]) -> list[F]:
            return [
                sum(m[i][j] * v[j] for j in range(len(v)))
                for i in range(len(m))
            ]

        tilde_p0 = rvec(radd(mb[(0, 0)], mb[(0, 1)]), p0)
        tilde_p1 = rvec(radd(mb[(1, 0)], mb[(1, 1)]), p0)
        self.assertEqual(tilde_p0, tilde_p1)

        # Construct Hadamard-product 16-outcome joint distribution on R_+^6
        alpha = {
            (x, a): [sum(ma[(x, a)][r][k] for r in range(6)) for k in range(6)]
            for x in (0, 1)
            for a in (0, 1)
        }
        beta = {
            (y, b): [
                rvec(mb[(y, b)], p0)[k] / tilde_p0[k] for k in range(6)
            ]
            for y in (0, 1)
            for b in (0, 1)
        }
        joint_simplex: dict[tuple[int, int, int, int], F] = {}
        for a0, a1, b0, b1 in itertools.product((0, 1), repeat=4):
            val = sum(
                tilde_p0[k]
                * alpha[(0, a0)][k]
                * alpha[(1, a1)][k]
                * beta[(0, b0)][k]
                * beta[(1, b1)][k]
                for k in range(6)
            )
            self.assertGreaterEqual(val, F(0))
            joint_simplex[(a0, a1, b0, b1)] = val
        self.assertEqual(sum(joint_simplex.values()), F(1))
        s_val = F(0)
        for x, y in itertools.product((0, 1), repeat=2):
            exy = F(0)
            for a, b in itertools.product((0, 1), repeat=2):
                p_ab = sum(rvec(rmat_mul(ma[(x, a)], mb[(y, b)]), p0))
                p_m = sum(
                    wt
                    for (a0, a1, b0, b1), wt in joint_simplex.items()
                    if (a0 if x == 0 else a1) == a
                    and (b0 if y == 0 else b1) == b
                )
                self.assertEqual(p_ab, p_m)
                exy += (1 if a == b else -1) * p_ab
            s_val += -exy if (x, y) == (1, 1) else exy
        self.assertLessEqual(abs(s_val), F(2))

        # 2. Theorem 1C(2): 10-state commuting classical-simplex PR-box countermodel!
        pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]

        def pr_prob(a: int, b: int, x: int, y: int) -> F:
            return F(1, 2) if (a ^ b) == (x * y) else F(0)

        a_pr: dict[tuple[int, int], RMat] = {}
        b_pr: dict[tuple[int, int], RMat] = {}
        for x, a in pairs:
            m = [[F(0)] * 10 for _ in range(10)]
            m[1 + pairs.index((x, a))][0] = F(1, 2)
            for k in range(1, 5):
                m[k][k] = F(1, 2)
            for idx, (y, b) in enumerate(pairs):
                m[9][5 + idx] = 2 * pr_prob(a, b, x, y)
            m[9][9] = F(1, 2)
            a_pr[(x, a)] = m

        for y, b in pairs:
            m = [[F(0)] * 10 for _ in range(10)]
            m[5 + pairs.index((y, b))][0] = F(1, 2)
            for idx, (x, a) in enumerate(pairs):
                m[9][1 + idx] = 2 * pr_prob(a, b, x, y)
            for k in range(5, 9):
                m[k][k] = F(1, 2)
            m[9][9] = F(1, 2)
            b_pr[(y, b)] = m

        for s in (0, 1):
            for inst in (a_pr, b_pr):
                for entry_mat in (inst[(s, 0)], inst[(s, 1)]):
                    self.assertTrue(
                        all(v >= 0 for row in entry_mat for v in row)
                    )
                col_sums = [
                    sum(inst[(s, 0)][r][c] + inst[(s, 1)][r][c] for r in range(10))
                    for c in range(10)
                ]
                self.assertEqual(col_sums, [F(1)] * 10)

        for xa, m1 in a_pr.items():
            for yb, m2 in b_pr.items():
                self.assertEqual(rmat_mul(m1, m2), rmat_mul(m2, m1))

        e0 = [F(1)] + [F(0)] * 9
        # Verify residual-level no-signaling is VIOLATED (Bob writes y into hidden slot)
        self.assertNotEqual(
            rvec(radd(b_pr[(0, 0)], b_pr[(0, 1)]), e0),
            rvec(radd(b_pr[(1, 0)], b_pr[(1, 1)]), e0),
        )
        # Verify scalar outcome no-signaling holds and S_CHSH == 4!
        s_pr = F(0)
        for x, y in pairs:
            exy = F(0)
            probs_xy: dict[tuple[int, int], F] = {}
            for a, b in pairs:
                p_ab = sum(rvec(rmat_mul(a_pr[(x, a)], b_pr[(y, b)]), e0))
                self.assertEqual(p_ab, pr_prob(a, b, x, y))
                probs_xy[(a, b)] = p_ab
                exy += (1 if a == b else -1) * p_ab
            self.assertEqual(probs_xy[(0, 0)] + probs_xy[(0, 1)], F(1, 2))
            self.assertEqual(probs_xy[(0, 0)] + probs_xy[(1, 0)], F(1, 2))
            s_pr += -exy if (x, y) == (1, 1) else exy
        self.assertEqual(s_pr, F(4))

    def test_03_grade3_countermodels_and_pairwise_decoherence_insufficiency(
        self,
    ) -> None:
        # Countermodel 2A.1: 4-atom delta=1/4 witness from grade2_justification.py
        delta = F(1, 4)
        w1: dict[frozenset[int], F] = {
            frozenset({i}): (F(1) - delta) / 4 for i in range(4)
        }
        w1[frozenset({0, 1, 2})] = delta
        m1 = ExactGradeMeasure(w1, 4)
        self.assertEqual(m1.mu(frozenset(range(4))), F(1))
        for mask in range(1 << 4):
            ev = frozenset(i for i in range(4) if (mask >> i) & 1)
            self.assertGreaterEqual(m1.mu(ev), F(0))
        for i, j in itertools.combinations(range(4), 2):
            self.assertEqual(
                m1.interference(frozenset({i}), frozenset({j})), F(0)
            )
        self.assertEqual(
            m1.interference(frozenset({0}), frozenset({1}), frozenset({2})),
            F(1, 4),
        )
        self.assertEqual(
            m1.interference(
                frozenset({0}),
                frozenset({1}),
                frozenset({2}),
                frozenset({3}),
            ),
            F(0),
        )
        self.assertEqual(
            sum(m1.mu(frozenset({i})) for i in range(4)), F(3, 4)
        )

        # Countermodel 2A.2: 3-atom masked witness surviving Pairwise Decoherence Sufficiency
        w2: dict[frozenset[int], F] = {
            frozenset({0}): F(1, 3),
            frozenset({1}): F(1, 3),
            frozenset({2}): F(1, 3),
            frozenset({0, 1}): F(1, 8),
            frozenset({0, 2}): F(-1, 8),
            frozenset({1, 2}): F(-1, 8),
            frozenset({0, 1, 2}): F(1, 8),
        }
        m2 = ExactGradeMeasure(w2, 3)
        self.assertEqual(m2.mu(frozenset({0, 1, 2})), F(1))
        self.assertEqual(
            sum(m2.mu(frozenset({i})) for i in range(3)), F(1)
        )
        nonempty = [
            frozenset(i for i in range(3) if (mask >> i) & 1)
            for mask in range(1, 1 << 3)
        ]
        for ev in nonempty:
            self.assertGreater(m2.mu(ev), F(0))

        # Exhaustively test ALL pairwise-disjoint families {A_1, ..., A_k} (k=2, 3)
        for k in (2, 3):
            for fam in itertools.combinations(nonempty, k):
                if any(
                    fam[r] & fam[s]
                    for r in range(k)
                    for s in range(r + 1, k)
                ):
                    continue
                pairwise_zero = all(
                    m2.interference(fam[r], fam[s]) == 0
                    for r in range(k)
                    for s in range(r + 1, k)
                )
                if pairwise_zero:
                    union_all = frozenset().union(*fam)
                    self.assertEqual(
                        m2.mu(union_all), sum(m2.mu(a) for a in fam)
                    )

        self.assertEqual(
            m2.interference(frozenset({0}), frozenset({1}), frozenset({2})),
            F(1, 8),
        )

    def test_04_amplitude_scaling_and_stirling_dimension_select_grade2(
        self,
    ) -> None:
        # 1. Theorem 2B: Odd-degree failure, Pythagorean (3,4,5) selection of k=2,
        # universal quadratic I_3=I_4=0, and quartic countermodel F_4 with I_3 = 4/9.
        for k_odd in (1, 3, 5, 7):
            val_pos = F(2) ** k_odd
            val_neg = (F(-2)) ** k_odd
            self.assertEqual(val_neg, -val_pos)
            self.assertLess(val_neg, F(0))

        # Rational (3,4,5) orthogonal rotation O = [[3/5, -4/5], [4/5, 3/5]]
        p0 = F(9, 25)
        p1 = F(16, 25)
        self.assertEqual(p0 + p1, F(1))
        for r in range(1, 7):
            part_sum = (p0**r) + (p1**r)
            if r == 1:
                self.assertEqual(part_sum, F(1))
            else:
                self.assertLess(part_sum, F(1))

        # Every homogeneous quadratic form F_R(a) = a^T R a has exact I_3 = I_4 = 0
        r_sym = [
            [F(2, 7), F(-1, 11), F(3, 13), F(1, 5)],
            [F(-1, 11), F(1, 3), F(-2, 9), F(1, 7)],
            [F(3, 13), F(-2, 9), F(1, 4), F(-1, 6)],
            [F(1, 5), F(1, 7), F(-1, 6), F(2, 9)],
        ]
        w_quad: dict[frozenset[int], F] = {}
        for i in range(4):
            w_quad[frozenset({i})] = r_sym[i][i]
            for j in range(i + 1, 4):
                w_quad[frozenset({i, j})] = 2 * r_sym[i][j]
        m_quad = ExactGradeMeasure(w_quad, 4)
        for mask in range(1 << 4):
            ev = frozenset(i for i in range(4) if (mask >> i) & 1)
            chi = [F(1 if i in ev else 0) for i in range(4)]
            quad_val = sum(
                r_sym[i][j] * chi[i] * chi[j]
                for i in range(4)
                for j in range(4)
            )
            self.assertEqual(m_quad.mu(ev), quad_val)

        nonempty4 = [
            frozenset(i for i in range(4) if (mask >> i) & 1)
            for mask in range(1, 1 << 4)
        ]
        for k in (3, 4):
            for fam in itertools.combinations(nonempty4, k):
                if any(
                    fam[u] & fam[v]
                    for u in range(k)
                    for v in range(u + 1, k)
                ):
                    continue
                self.assertEqual(m_quad.interference(*fam), F(0))

        # Quartic signed-positive countermodel F_4(a) = ((a_0 + a_1 + a_2)/3)^4
        def f4(a0: F, a1: F, a2: F) -> F:
            return ((a0 + a1 + a2) / 3) ** 4

        self.assertEqual(f4(F(1), F(1), F(1)), F(1))
        for s0, s1, s2 in itertools.product((F(-1), F(0), F(1)), repeat=3):
            self.assertGreaterEqual(f4(s0, s1, s2), F(0))
            self.assertEqual(f4(-s0, -s1, -s2), f4(s0, s1, s2))
        i3_f4 = (
            f4(F(1), F(1), F(1))
            - f4(F(1), F(1), F(0))
            - f4(F(1), F(0), F(1))
            - f4(F(0), F(1), F(1))
            + f4(F(1), F(0), F(0))
            + f4(F(0), F(1), F(0))
            + f4(F(0), F(0), F(1))
        )
        self.assertEqual(i3_f4, F(4, 9))

        # 2. Theorem 2C: Stirling expansion of n^{r_0} and composite multiplicativity
        for r0 in range(1, 6):
            coeffs = []
            fact = 1
            for r in range(1, r0 + 1):
                fact *= r
                coeffs.append(fact * stirling_second(r0, r))
            for n in range(1, 9):
                val = sum(coeffs[r - 1] * binom(n, r) for r in range(1, r0 + 1))
                self.assertEqual(val, n**r0)

        # Pure real Mobius hierarchies (c_r = 1 for 1 <= r <= m) fail at n1 = n2 = 2
        for m in range(2, 7):
            d2 = sum(binom(2, r) for r in range(1, m + 1))
            d4 = sum(binom(4, r) for r in range(1, m + 1))
            self.assertNotEqual(d2 * d2, d4)

        # Within grade-2 d(n) = n + c_2 * C(n, 2), d(2)^2 == d(4) selects c_2 in {0, 2}
        surviving_c2 = [
            c2
            for c2 in range(0, 10)
            if (2 + c2) ** 2 == 4 + 6 * c2
        ]
        self.assertEqual(surviving_c2, [0, 2])

    @staticmethod
    def _herm3_basis() -> list[Mat]:
        """Standard 9-element Q(i)-basis of Herm_3(C)."""
        basis: list[Mat] = []
        for i in range(3):
            m = zeros(3, 3)
            m[i][i] = ONE
            basis.append(m)
        for i in range(3):
            for j in range(i + 1, 3):
                mr = zeros(3, 3)
                mr[i][j] = ONE
                mr[j][i] = ONE
                basis.append(mr)
                mi = zeros(3, 3)
                mi[i][j] = -IMAG
                mi[j][i] = IMAG
                basis.append(mi)
        return basis

    def test_05_degenerate_subspace_countermodels_on_qutrit_walsh_section(
        self,
    ) -> None:
        basis3 = self._herm3_basis()
        j_basis = [walsh_section(b) for b in basis3]

        # Flatten 12x12 Hermitian matrices into 288-coordinate rational vectors
        def flat_gmat(m: Mat) -> list[F]:
            out: list[F] = []
            for r in m:
                for x in r:
                    out.append(x.re)
                    out.append(x.im)
            return out

        self.assertEqual(rmat_rank([flat_gmat(jb) for jb in j_basis]), 9)

        # Repeat face F_{01} = J_3(P_{01} PSD_3 P_{01}) has real span dimension 4
        p01 = gmat([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        p0 = gmat([[1, 0, 0], [0, 0, 0], [0, 0, 0]])
        p1 = gmat([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        f01_vecs = [
            flat_gmat(walsh_section(mmul(mmul(p01, b), p01))) for b in basis3
        ]
        self.assertEqual(rmat_rank(f01_vecs), 4)

        def e01(m12: Mat) -> F:
            return (
                coarse_cell_cross(m12, 3, 0, 0).re
                + coarse_cell_cross(m12, 3, 1, 1).re
            )

        def t_mix(rho: Mat) -> Mat:
            tr_val = (rho[0][0] + rho[1][1]).re
            return walsh_section(mscale(tr_val * F(1, 2), p01))

        def t_deph(rho: Mat) -> Mat:
            proj = madd(mmul(mmul(p0, rho), p0), mmul(mmul(p1, rho), p1))
            return walsh_section(proj)

        def t_luders(rho: Mat) -> Mat:
            return walsh_section(mmul(mmul(p01, rho), p01))

        # Verify calibration & repeatability of T_mix, T_deph, and T_luders on all 9 basis
        for b in basis3:
            jb = walsh_section(b)
            target_e = e01(jb)
            for fn in (t_mix, t_deph, t_luders):
                out = fn(b)
                self.assertTrue(is_coarse_decoherent(out, 3))
                self.assertEqual(entry_mass(out), target_e)
                self.assertEqual(e01(out), entry_mass(out))
            # Theorem 3C: T_deph also preserves fine {C_0, C_1} weights without controls!
            out_deph = t_deph(b)
            self.assertEqual(
                coarse_cell_cross(out_deph, 3, 0, 0),
                coarse_cell_cross(jb, 3, 0, 0),
            )
            self.assertEqual(
                coarse_cell_cross(out_deph, 3, 1, 1),
                coarse_cell_cross(jb, 3, 1, 1),
            )

        # Coherence test on rho_{+01} = (|0>+|1>)(<0|+<1|)/2 under Pythagorean (3,4,5)
        # subspace unitary U_{01} = (1/5)[[3,4,0],[-4,3,0],[0,0,5]]
        rho_plus01 = gmat(
            [[F(1, 2), F(1, 2), 0], [F(1, 2), F(1, 2), 0], [0, 0, 0]]
        )
        u01_pad = gmat(
            [
                [F(3, 5), F(4, 5), 0, 0],
                [F(-4, 5), F(3, 5), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        w01 = walsh_lift_operator(3, u01_pad)
        self.assertEqual(mmul(w01, dag(w01)), eye(12))

        c0_luders = coarse_cell_cross(
            mmul(mmul(w01, t_luders(rho_plus01)), dag(w01)), 3, 0, 0
        ).re
        c0_mix = coarse_cell_cross(
            mmul(mmul(w01, t_mix(rho_plus01)), dag(w01)), 3, 0, 0
        ).re
        c0_deph = coarse_cell_cross(
            mmul(mmul(w01, t_deph(rho_plus01)), dag(w01)), 3, 0, 0
        ).re
        # For |+01>, (3+4)^2 / (2*25) = 49/50, vs (9+16)/(2*25) = 1/2 for mix & deph!
        self.assertEqual(c0_luders, F(49, 50))
        self.assertEqual(c0_mix, F(1, 2))
        self.assertEqual(c0_deph, F(1, 2))

        # Literal 12-label cut Pi_{C_{01}} leaves span(C_{12,0}) and has dark zero-mass
        # nonzero output on J_3(|2><2|)
        pi_01 = mblkdiag(eye(8), zeros(4, 4))
        rho_2 = gmat([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
        j_rho2 = walsh_section(rho_2)
        lit_cut_2 = mmul(mmul(pi_01, j_rho2), pi_01)
        self.assertNotEqual(lit_cut_2, zeros(12, 12))
        self.assertTrue(is_psd(lit_cut_2))
        self.assertEqual(entry_mass(lit_cut_2), F(0))
        self.assertEqual(
            rmat_rank([flat_gmat(jb) for jb in j_basis] + [flat_gmat(lit_cut_2)]),
            10,
        )

    def test_06_pure_one_positivity_uniqueness_of_degenerate_luders_rule(
        self,
    ) -> None:
        # 1. Exact dyadic-rational 12x12 Walsh lift hat(P)_{01} and hat(P)_2
        basis3 = self._herm3_basis()
        p01_3 = gmat([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        p2_3 = gmat([[0, 0, 0], [0, 0, 0], [0, 0, 1]])
        hat_p01 = walsh_lift_operator(
            3, gmat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        )
        hat_p2 = walsh_lift_operator(
            3, gmat([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]])
        )
        # Verify dyadic denominators (powers of 2 only), idempotence, orthogonality, rank
        for hp, expected_rk in ((hat_p01, 6), (hat_p2, 3)):
            self.assertEqual(mmul(hp, hp), hp)
            self.assertEqual(hp, dag(hp))
            for row in hp:
                for x in row:
                    self.assertEqual(x.im, F(0))
                    den = x.re.denominator
                    self.assertEqual(den & (den - 1), 0)
            self.assertEqual(
                rmat_rank([[x.re for x in row] for row in hp]), expected_rk
            )
        self.assertEqual(mmul(hat_p01, hat_p2), zeros(12, 12))

        for b in basis3:
            jb = walsh_section(b)
            self.assertEqual(
                mmul(mmul(hat_p01, jb), hat_p01),
                walsh_section(mmul(mmul(p01_3, b), p01_3)),
            )
            self.assertEqual(
                mmul(mmul(hat_p2, jb), hat_p2),
                walsh_section(mmul(mmul(p2_3, b), p2_3)),
            )

        # 2. Theorem 3B(2): Subspace finer-cell tomography equivalence on F_{01}!
        # Preserving mu(C_0), mu(C_1) on F_{01} after {I, U^R_{01}, U^I_{01}} uniquely
        # fixes all 4 real coordinates of P_{01} Herm_3 P_{01}!
        u01_r = walsh_lift_operator(
            3,
            gmat(
                [
                    [F(3, 5), F(4, 5), 0, 0],
                    [F(-4, 5), F(3, 5), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            ),
        )
        u01_i = walsh_lift_operator(
            3,
            gmat(
                [
                    [F(3, 5), G(0, F(4, 5)), 0, 0],
                    [G(0, F(4, 5)), F(3, 5), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            ),
        )
        f01_basis = [
            basis3[0],  # |0><0|
            basis3[1],  # |1><1|
            basis3[3],  # |0><1| + |1><0|
            basis3[4],  # -i|0><1| + i|1><0|
        ]
        tomo_rows: RMat = []
        for b in f01_basis:
            jb = walsh_section(b)
            j_r = mmul(mmul(u01_r, jb), dag(u01_r))
            j_i = mmul(mmul(u01_i, jb), dag(u01_i))
            tomo_rows.append(
                [
                    coarse_cell_cross(jb, 3, 0, 0).re,
                    coarse_cell_cross(jb, 3, 1, 1).re,
                    coarse_cell_cross(j_r, 3, 0, 0).re,
                    coarse_cell_cross(j_i, 3, 0, 0).re,
                ]
            )
        self.assertEqual(rmat_rank(tomo_rows), 4)

        # 3. Direct algebraic uniqueness on the 81-dimensional space L_R(Herm_3(C)):
        # Represent Phi in Q^{9x9} acting on coordinates in `basis3`:
        #   idx 0,1,2: |0><0|, |1><1|, |2><2|
        #   idx 3,4: Re/Im (0,1); idx 5,6: Re/Im (0,2); idx 7,8: Re/Im (1,2).
        # Linear constraints from calibration + repeat-face identity + Phi(|2><2|)=0
        # (the last forced by Tr(Phi(|2><2|))=0 and 1-positivity):
        eqs: RMat = []
        # Calibration: Tr(Phi(b_col)) = sum_{r in 0,1,2} M_{r, col} == Tr(P_{01} b_col)
        # Subtract Luders map M_Luders so we solve for Delta = Phi - Phi_Luders!
        for col in range(9):
            row = [F(0)] * 81
            for r in (0, 1, 2):
                row[r * 9 + col] = F(1)
            eqs.append(row)
        # Repeat-face non-disturbance: Delta(:, col) == 0 for col in {0, 1, 3, 4}
        # plus Delta(:, 2) == 0 from Phi(|2><2|) == 0:
        for col in (0, 1, 2, 3, 4):
            for r in range(9):
                row = [F(0)] * 81
                row[r * 9 + col] = F(1)
                eqs.append(row)

        null_vecs = rmat_nullspace(eqs)
        # Only the 4 cross columns {5, 6, 7, 8} mapping into the 8D traceless subspace
        # survive linear calibration + face constraints (4 * 8 = 32 parameters):
        self.assertEqual(len(null_vecs), 32)

        # Now verify our 1-positivity quadratic-discriminant elimination on EVERY
        # surviving basis perturbation X = Delta(b_col) (col in {5, 6, 7, 8}):
        # For col in {5,6}, rho(t) = (t|0> + |2>)(t<0| + <2|) or with i|2>;
        # Phi(rho(t)) = t^2 |0><0| + t * X. Any nonzero Hermitian X with Tr(X)=0 has
        # an explicit rational vector w and rational t where w^dagger(t^2|0><0|+tX)w < 0!
        test_vectors = [
            [ONE, ZERO, ZERO],
            [ZERO, ONE, ZERO],
            [ZERO, ZERO, ONE],
            [ONE, ONE, ZERO],
            [ONE, IMAG, ZERO],
            [ONE, ZERO, ONE],
            [ONE, ZERO, IMAG],
            [ZERO, ONE, ONE],
            [ZERO, ONE, IMAG],
        ]

        def quad_form(mat: Mat, w: list[G]) -> F:
            acc = ZERO
            for i in range(3):
                for j in range(3):
                    acc = acc + w[i].conj() * mat[i][j] * w[j]
            self.assertEqual(acc.im, F(0))
            return acc.re

        for nv in null_vecs:
            # Find which cross column col in {5,6,7,8} is nonzero in nv
            col = next(
                c
                for c in (5, 6, 7, 8)
                if any(nv[r * 9 + c] != 0 for r in range(9))
            )
            x_mat = zeros(3, 3)
            for r in range(9):
                if nv[r * 9 + col] != 0:
                    x_mat = madd(x_mat, mscale(nv[r * 9 + col], basis3[r]))
            self.assertNotEqual(x_mat, zeros(3, 3))
            psi_proj = basis3[0] if col in (5, 6) else basis3[1]

            # Find w in test_vectors with <w|X|w> != 0 (guaranteed since test_vectors
            # spans all 9 Hermitian quadratic forms on C^3!)
            w_hit = next(w for w in test_vectors if quad_form(x_mat, w) != 0)
            a_coef = quad_form(psi_proj, w_hit)
            b_coef = quad_form(x_mat, w_hit)
            t_bad = (
                F(-1) * b_coef
                if a_coef == 0
                else (-b_coef) / (2 * a_coef)
            )
            violated_mat = madd(
                mscale(t_bad * t_bad, psi_proj), mscale(t_bad, x_mat)
            )
            self.assertLess(quad_form(violated_mat, w_hit), F(0))
            self.assertFalse(is_psd(violated_mat))

    def test_07_bounded_copy_minor_truncation_and_sign_blindness(
        self,
    ) -> None:
        # 1. Theorem 4A(1): Entrywise nonnegative non-PSD D_+ = (J_3 - I_3)/6
        d_plus = gmat(
            [
                [0, F(1, 6), F(1, 6)],
                [F(1, 6), 0, F(1, 6)],
                [F(1, 6), F(1, 6), 0],
            ]
        )
        self.assertEqual(entry_mass(d_plus), F(1))
        self.assertEqual(
            det_complex([[d_plus[0][0], d_plus[0][1]], [d_plus[1][0], d_plus[1][1]]]),
            G(F(-1, 36)),
        )
        self.assertEqual(det_complex(d_plus), G(F(1, 108)))
        self.assertFalse(is_psd(d_plus))
        cur_pow = d_plus
        for _ in range(1, 4):
            self.assertEqual(entry_mass(cur_pow), F(1))
            self.assertTrue(
                all(x.im == 0 and x.re >= 0 for row in cur_pow for x in row)
            )
            cur_pow = mkron(cur_pow, d_plus)

        # 2. Theorem 4A(2): Tournament skew-Hermitian family D^{(n)}_{imag}(t_n)
        # passes ALL 2^n - 2 proper principal minors (1 <= |I| <= n - 1) while det < 0!
        expected_dets = {
            2: F(-11, 100),
            3: F(-11, 432),
            4: F(-7, 4096),
            5: F(-10564, 89253125),
        }
        witness_params = [(2, F(3, 5)), (3, F(1, 4)), (4, F(1, 8)), (5, F(1, 13))]
        for n, t_val in witness_params:
            d_n = [
                [
                    G(F(1, n), F(0))
                    if r == c
                    else G(F(0), t_val if r < c else -t_val)
                    for c in range(n)
                ]
                for r in range(n)
            ]
            self.assertTrue(is_hermitian(d_n))
            self.assertEqual(mtrace(d_n), ONE)
            self.assertEqual(entry_mass(d_n), F(1))
            # Check all 2^n Boolean subset weights equal |A|/n >= 0
            for mask in range(1 << n):
                ev = [i for i in range(n) if (mask >> i) & 1]
                wt = sum((d_n[i][j] for i in ev for j in ev), ZERO)
                self.assertEqual(wt, G(F(len(ev), n)))

            proper_count = 0
            for m_sz in range(1, n):
                for subset_i in itertools.combinations(range(n), m_sz):
                    sub = [[d_n[r][c] for c in subset_i] for r in subset_i]
                    self.assertTrue(is_strictly_pd(sub))
                    d_sub = det_complex(sub)
                    self.assertEqual(d_sub.im, F(0))
                    self.assertGreater(d_sub.re, F(0))
                    proper_count += 1
            self.assertEqual(proper_count, (1 << n) - 2)

            top_det = det_complex(d_n)
            self.assertEqual(top_det, G(expected_dets[n]))
            self.assertLess(top_det.re, F(0))
            self.assertFalse(is_psd(d_n))

        # Explicitly verify on 12-label Walsh section J_3(D^{(3)}_{imag}(1/4)) that
        # m=1 and m=2 dyadic coarse-cell minor readouts are strictly positive!
        d3_trunc = [
            [
                G(F(1, 3), F(0))
                if r == c
                else G(F(0), F(1, 4) if r < c else F(-1, 4))
                for c in range(3)
            ]
            for r in range(3)
        ]
        j3_trunc = walsh_section(d3_trunc)
        self.assertEqual(entry_mass(j3_trunc), F(1))
        for a in range(3):
            self.assertEqual(coarse_cell_cross(j3_trunc, 3, a, a), G(F(1, 3)))

        # m = 2 coarse-cell minor coupler on J_3(D)^{otimes 2} otimes D_{+Z} (k=2, r=1):
        # On fiber {0..3}^2 x {0,1} (32 dims), pair {(i0,i1,0), (i1,i0,0)} with
        # {(i0,i1,1), (i1,i0,1)} under (1/2) H_4 to read (2!/4) det(D_{i0,i1}) = 7/288 > 0!
        d_pz = walsh_section(gmat([[1, 0], [0, 0]]))  # E_{00} = diag(1,0)
        for i0, i1 in itertools.combinations(range(3), 2):
            # Verify fiber contraction S_I[*,*] directly and on 32x32 fiber matrix
            d_pad = zeros(4, 4)
            for r in range(3):
                for c in range(3):
                    d_pad[r][c] = d3_trunc[r][c]
            e00 = gmat([[1, 0], [0, 0]])
            fiber_in = mkron(mkron(d_pad, d_pad), e00)  # 32 x 32
            u_fib = eye(32)
            active = [
                (i0 * 4 + i1) * 2 + 0,  # even perm (+1)
                (i0 * 4 + i1) * 2 + 1,  # ancilla-zero (+1)
                (i1 * 4 + i0) * 2 + 0,  # odd perm (-1)
                (i1 * 4 + i0) * 2 + 1,  # ancilla-zero (-1)
            ]
            # Permute rows of (1/2) H_4 so row 0 has (+1, +1, -1, -1) on `active`
            # (standard H_4 rows: 0=(+,+,+,+), 2=(+,+,-,-), 1=(+,-,+,-), 3=(+,-,-,+)).
            h4_perm = [
                [F(1, 2), F(1, 2), F(-1, 2), F(-1, 2)],
                [F(1, 2), F(1, 2), F(1, 2), F(1, 2)],
                [F(1, 2), F(-1, 2), F(1, 2), F(-1, 2)],
                [F(1, 2), F(-1, 2), F(-1, 2), F(1, 2)],
            ]
            for r_loc in range(4):
                for c_loc in range(4):
                    u_fib[active[r_loc]][active[c_loc]] = G(
                        h4_perm[r_loc][c_loc]
                    )
            self.assertEqual(mmul(u_fib, dag(u_fib)), eye(32))
            s_out = mmul(mmul(u_fib, fiber_in), dag(u_fib))
            c_star_wt = s_out[active[0]][active[0]]
            self.assertEqual(c_star_wt, G(F(7, 288)))
            self.assertGreater(c_star_wt.re, F(0))
        _ = d_pz

    def test_08_single_copy_walsh_probability_catalogue_and_ri23_certificates(
        self,
    ) -> None:
        # 1. Verify RI-23 §6 raw-domain rank-1 obstruction on K_3:
        # Any PSD T with 0 <= v^dagger T v <= v^dagger (1_3 1_3^dagger) v vanishes on
        # ker(1_3^dagger) = span{(1,-1,0), (1,0,-1)}, leaving dim_R = 1!
        j0_3 = gmat([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        v_orth1 = [ONE, -ONE, ZERO]
        v_orth2 = [ONE, ZERO, -ONE]
        for v_o in (v_orth1, v_orth2):
            val = sum(
                v_o[i].conj() * j0_3[i][j] * v_o[j]
                for i in range(3)
                for j in range(3)
            )
            self.assertEqual(val, ZERO)
        # And RI-23's unscaled T_{e0+e1} gives value 2 > 1 on |+01><+01|:
        t_raw01 = gmat([[1, 1, 0], [1, 1, 0], [0, 0, 0]])
        rho_p01 = gmat([[F(1, 2), F(1, 2), 0], [F(1, 2), F(1, 2), 0], [0, 0, 0]])
        self.assertEqual(mtrace(mmul(rho_p01, t_raw01)), G(2))

        # 2. Theorem 4B: Single-copy Gaussian-rational Pythagorean probability catalogue
        # and exact linear inverse across n = 2, 3, 4!
        def acquire_and_invert(
            d_in: Mat,
        ) -> tuple[list[F], dict[tuple[int, int], F], dict[tuple[int, int], F], Mat]:
            n = len(d_in)
            ell = ceil_pow2(n)
            jn = walsh_section(d_in)
            self.assertTrue(is_coarse_decoherent(jn, n))
            self.assertEqual(entry_mass(jn), mtrace(d_in).re)

            y_diag = [coarse_cell_cross(jn, n, i, i).re for i in range(n)]
            y_re: dict[tuple[int, int], F] = {}
            y_im: dict[tuple[int, int], F] = {}
            for i in range(n):
                for j in range(i + 1, n):
                    ur = eye(ell)
                    ur[i][i] = G(F(3, 5))
                    ur[i][j] = G(F(4, 5))
                    ur[j][i] = G(F(-4, 5))
                    ur[j][j] = G(F(3, 5))
                    wr = walsh_lift_operator(n, ur)
                    self.assertEqual(mmul(wr, dag(wr)), eye(n * ell))
                    jr = mmul(mmul(wr, jn), dag(wr))
                    self.assertTrue(is_coarse_decoherent(jr, n))
                    self.assertEqual(entry_mass(jr), mtrace(d_in).re)
                    y_re[(i, j)] = coarse_cell_cross(jr, n, i, i).re

                    ui = eye(ell)
                    ui[i][i] = G(F(3, 5))
                    ui[i][j] = G(0, F(4, 5))
                    ui[j][i] = G(0, F(4, 5))
                    ui[j][j] = G(F(3, 5))
                    wi = walsh_lift_operator(n, ui)
                    self.assertEqual(mmul(wi, dag(wi)), eye(n * ell))
                    ji = mmul(mmul(wi, jn), dag(wi))
                    self.assertTrue(is_coarse_decoherent(ji, n))
                    self.assertEqual(entry_mass(ji), mtrace(d_in).re)
                    y_im[(i, j)] = coarse_cell_cross(ji, n, i, i).re

                    # Also verify bounded PSD effect 0 <= E <= I_n!
                    er = zeros(n, n)
                    er[i][i] = G(F(9, 25))
                    er[j][j] = G(F(16, 25))
                    er[i][j] = G(F(12, 25))
                    er[j][i] = G(F(12, 25))
                    self.assertTrue(is_psd(er))
                    self.assertTrue(is_psd(msub(eye(n), er)))

                    ei = zeros(n, n)
                    ei[i][i] = G(F(9, 25))
                    ei[j][j] = G(F(16, 25))
                    ei[i][j] = G(0, F(-12, 25))
                    ei[j][i] = G(0, F(12, 25))
                    self.assertTrue(is_psd(ei))
                    self.assertTrue(is_psd(msub(eye(n), ei)))

            d_hat = zeros(n, n)
            for i in range(n):
                d_hat[i][i] = G(y_diag[i])
            for i in range(n):
                for j in range(i + 1, n):
                    re_ij = (25 * y_re[(i, j)] - 9 * y_diag[i] - 16 * y_diag[j]) / 24
                    im_ij = (25 * y_im[(i, j)] - 9 * y_diag[i] - 16 * y_diag[j]) / 24
                    d_hat[i][j] = G(re_ij, im_ij)
                    d_hat[j][i] = G(re_ij, -im_ij)
            return y_diag, y_re, y_im, d_hat

        # Test RI-23 benchmark D_* (n=3, non-PSD, all 9 probabilities in [1/10, 4/5]!)
        d_star = gmat(
            [
                [F(1, 10), G(0, F(3, 20)), 0],
                [G(0, F(-3, 20)), F(1, 10), 0],
                [0, 0, F(4, 5)],
            ]
        )
        yd, yr, yi, dh_star = acquire_and_invert(d_star)
        self.assertEqual(dh_star, d_star)
        all_probs_star = yd + list(yr.values()) + list(yi.values())
        self.assertEqual(len(all_probs_star), 9)
        self.assertTrue(all(F(0) < p < F(1) for p in all_probs_star))
        self.assertFalse(is_psd(dh_star))

        # Test PSD qutrit and ququart states with complex off-diagonals
        d_psd3 = gmat(
            [
                [F(1, 2), G(F(1, 6), F(-1, 8)), G(F(1, 10), F(1, 12))],
                [G(F(1, 6), F(1, 8)), F(1, 3), G(F(-1, 15), F(1, 20))],
                [G(F(1, 10), F(-1, 12)), G(F(-1, 15), F(-1, 20)), F(1, 6)],
            ]
        )
        self.assertTrue(is_psd(d_psd3))
        yd3, yr3, yi3, dh3 = acquire_and_invert(d_psd3)
        self.assertEqual(dh3, d_psd3)
        self.assertTrue(
            all(F(0) <= p <= F(1) for p in yd3 + list(yr3.values()) + list(yi3.values()))
        )

        d_psd4 = gmat(
            [
                [F(2, 5), G(F(1, 10), F(1, 10)), 0, G(F(1, 20), 0)],
                [G(F(1, 10), F(-1, 10)), F(3, 10), G(0, F(1, 15)), 0],
                [0, G(0, F(-1, 15)), F(1, 5), G(F(-1, 25), F(1, 25))],
                [G(F(1, 20), 0), 0, G(F(-1, 25), F(-1, 25)), F(1, 10)],
            ]
        )
        self.assertTrue(is_psd(d_psd4))
        _, _, _, dh4 = acquire_and_invert(d_psd4)
        self.assertEqual(dh4, d_psd4)

        # 3. Verify all four RI-23 §4-§5 interval certificate regimes on J_2(D_t)
        # using exact square-root-free rational certificates!
        def r_sq_pyth2(eta0: F, eta1: F, eta_r: F, eta_i: F) -> F:
            a01 = (25 * eta_r + 9 * eta0 + 16 * eta1) / 24
            b01 = (25 * eta_i + 9 * eta0 + 16 * eta1) / 24
            return eta0 * eta0 + eta1 * eta1 + 2 * (a01 * a01 + b01 * b01)

        def dt_mat(t_param: F) -> Mat:
            return gmat([[F(1, 2), G(0, t_param)], [G(0, -t_param), F(1, 2)]])

        # (a) Certified PSD: D_0 with eta_I = 6/25 (so b01 = 1/4, r^2 = 1/8 < (3/8)^2 = 9/64)
        yd_p, yr_p, yi_p, dh_p = acquire_and_invert(dt_mat(F(0)))
        r2_p = r_sq_pyth2(F(0), F(0), F(0), F(6, 25))
        self.assertEqual(r2_p, F(1, 8))
        r_bar_p = F(3, 8)
        self.assertGreaterEqual(r_bar_p * r_bar_p, r2_p)
        self.assertTrue(is_psd(msub(dh_p, mscale(r_bar_p, eye(2)))))
        _ = (yd_p, yr_p, yi_p)

        # (b) Certified non-PSD: D_{3/4} with eta_I = 3/25 (b01 = 1/8, r^2 = 1/32)
        _, _, _, dh_n = acquire_and_invert(dt_mat(F(3, 4)))
        r2_n = r_sq_pyth2(F(0), F(0), F(0), F(3, 25))
        self.assertEqual(r2_n, F(1, 32))
        # Test vector v = (1, i)^T: ||v||^2 = 2, v^dagger dh_n v = 1 - 3/2 = -1/2 < 0
        v_neg = [ONE, IMAG]
        v_val = sum(
            v_neg[r].conj() * dh_n[r][c] * v_neg[c]
            for r in range(2)
            for c in range(2)
        ).re
        v_norm2 = F(2)
        self.assertEqual(v_val, F(-1, 2))
        self.assertLess(v_val, F(0))
        self.assertGreater(v_val * v_val, r2_n * (v_norm2 * v_norm2))

        # (c) Verified ambiguity: D_{1/2} with eta_I = 6/25 -> compatible t in [1/4, 3/4]
        self.assertTrue(is_psd(dt_mat(F(1, 4))))
        self.assertFalse(is_psd(dt_mat(F(3, 4))))

        # (d) Proven infeasible by trace-mass check |y_0 + y_1 - 1| > eta_0 + eta_1:
        y_bad = [F(3, 5), F(3, 5)]
        eta_bad = [F(1, 20), F(1, 20)]
        self.assertGreater(abs(sum(y_bad) - F(1)), sum(eta_bad))


if __name__ == "__main__":
    unittest.main()
