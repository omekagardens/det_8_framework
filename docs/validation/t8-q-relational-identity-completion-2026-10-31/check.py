#!/usr/bin/env python3
"""Exact standard-library verification for relational-identity pair-kernel completion.

Verifies all theorems, obstructions, and classical comparators pre-registered in
`PROTOCOL.md` for `t8-q-relational-identity-completion-2026-10-31`:

  Target R1 (Coarse-cell dyadic-rational determinant witness via ~_T quotienting):
    - Theorem 1A: Walsh-untwisted n-cell section J_n(D) over Z[1/2, i] (tested on
      n=2 and n=3) is exactly decoherent on coarse cells, preserves Tr(D) as total
      mass M(J_n(D)), and via ~_T-lifted Sylvester-Hadamard couplers U_I yields
      mu(C_*) = (|I|! / 2^k) det(D_I) on a single coarse product cell using zero
      sub-cell addressing (verified on full 16x16 raw matrices for n=2 and all 7
      principal minors for n=3, m=1,2,3).
    - Theorem 1B: On raw unencoded D^{otimes m} otimes D_anc with one 4-label
      ancilla D_anc in RI-08b's cone C_4, any mass-preserving controlled unitary
      (V_x 1_4 = 1_4) satisfies |1_4^dagger y| <= sqrt(2)||y||_2 on ker(D_anc),
      forcing v_+ = v_- and zero pure-determinant sensitivity on coarse cell A_r.

  Target R2 (~_T-quotient escape, identity-atomicity, generator observability, J^2=-I):
    - Theorem 2A: Quotienting C_4 by ~_T replaces rank-1 Gamma_4 = 1_4 1_4^dagger
      with full-rank Tr on PSD_2(C); mass preservation across {I, S_H}-reachable
      states forces lambda = 1 in M_lambda = P_+ + lambda P_-.
    - Theorem 2B: Reference-complete identity-atomicity fails on Diag_+(Omega_d)
      for d >= 2 via coordinate projections T_i(D) = E_i D E_i, and holds on both
      PSD_2(R) and PSD_2(C) via pure faithful entangled probes.
    - Theorem 2C: On Sym_2(R), im(D_{J_0}) = span{X, Z} forces every self-conserved
      linear observable into R*Tr (excluding the rebit without local tomography),
      whereas phi(D_{-iH})(rho) = Tr(H rho) is injective and non-constant on Herm_2(C).
    - Theorem 2D: For D = G + i*Omega in Herm_{2m}(C) with G > 0, D >= 0 iff
      G + Omega G^{-1} Omega >= 0, rank_C(D) >= m, and rank_C(D) = m iff
      (G^{-1} Omega)^2 = -I_{2m} (resolving why_complex.py's mixed-rank D_t).

  Target R3 (Active pair-kernel-to-growth four-birth causal diamond law):
    - Theorem 3A: Over unchanged Part A four-birth marked q_C(S), branch maps
      B^{P,r}_{S,b} on C_4 subset M_4(C) have strictly positive-definite Choi
      matrices and explicit Gaussian-rational Kraus decompositions, normalize both
      total-entry mass M on C_4 and Tr on M_4(C), satisfy relabeling covariance,
      exhibit timelike sequential noncommutativity [B_2, B_1] != 0, and satisfy
      every incomparable-birth diamond as exact 16x16 superoperators on M_4(C).
    - Theorem 3B: Purely imaginary phase difference between D_{+Y} and D_{-Y}
      (which share Re(D_{+Y}) = Re(D_{-Y}) = I_4 / 4, hence identical weights
      mu(A) = |A|/4 on all 16 Boolean subsets) drives four-birth antichain contrast
      Delta_Z = 263 / 1115136, with cyclic S_P^k quadrature rotation and an explicit
      d=4 classical cyclic-simplex comparator (Delta_4, C_4) on mixed states.

Zero floating-point operations or external libraries are used.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import unittest


class G:
    """Exact Gaussian rational a + b*i with a, b in Q (`fractions.Fraction`)."""

    __slots__ = ("re", "im")

    def __init__(self, re: int | Fraction = 0, im: int | Fraction = 0) -> None:
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
        denom = o.norm_sq()
        if denom == 0:
            raise ZeroDivisionError("Gaussian rational division by zero")
        num = self * o.conj()
        return G._raw(num.re / denom, num.im / denom)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (G, int, Fraction)) and not isinstance(other, bool):
            o = G.coerce(other)
            return self.re == o.re and self.im == o.im
        return False

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    def __repr__(self) -> str:
        return f"G({self.re!r}, {self.im!r})"


ZERO = G(0, 0)
ONE = G(1, 0)
IMAG = G(0, 1)
Matrix = list[list[G]]


# ── Exact Gaussian-rational matrix linear algebra ───────────────────────────


def zeros(rows: int, cols: int) -> Matrix:
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def eye(n: int) -> Matrix:
    out = zeros(n, n)
    for i in range(n):
        out[i][i] = ONE
    return out


def diag_mat(entries: list[G | int | Fraction]) -> Matrix:
    n = len(entries)
    out = zeros(n, n)
    for i, val in enumerate(entries):
        out[i][i] = G.coerce(val)
    return out


def block_diag(*blocks: Matrix) -> Matrix:
    total_r = sum(len(b) for b in blocks)
    total_c = sum(len(b[0]) for b in blocks)
    out = zeros(total_r, total_c)
    r_off = 0
    c_off = 0
    for b in blocks:
        for i, row in enumerate(b):
            for j, val in enumerate(row):
                out[r_off + i][c_off + j] = val
        r_off += len(b)
        c_off += len(b[0])
    return out


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return [
        [a[i][j] - b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def mat_scale(c: G | int | Fraction, a: Matrix) -> Matrix:
    cc = G.coerce(c)
    return [[cc * val for val in row] for row in a]


def mat_dag(a: Matrix) -> Matrix:
    return [
        [a[i][j].conj() for i in range(len(a))]
        for j in range(len(a[0]))
    ]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    m, k, n = len(a), len(a[0]), len(b[0])
    if len(b) != k:
        raise ValueError("Incompatible dimensions")
    out = zeros(m, n)
    for i in range(m):
        for r in range(k):
            air = a[i][r]
            if air != ZERO:
                brow = b[r]
                out_row = out[i]
                for j in range(n):
                    if brow[j] != ZERO:
                        out_row[j] = out_row[j] + air * brow[j]
    return out


def kron(a: Matrix, b: Matrix) -> Matrix:
    ra, ca = len(a), len(a[0])
    rb, cb = len(b), len(b[0])
    out = zeros(ra * rb, ca * cb)
    for i in range(ra):
        for j in range(ca):
            aij = a[i][j]
            if aij != ZERO:
                for p in range(rb):
                    for q in range(cb):
                        bpq = b[p][q]
                        if bpq != ZERO:
                            out[i * rb + p][j * cb + q] = aij * bpq
    return out


def mat_trace(a: Matrix) -> G:
    acc = ZERO
    for i in range(len(a)):
        acc = acc + a[i][i]
    return acc


def total_mass(d: Matrix) -> G:
    acc = ZERO
    for row in d:
        for val in row:
            acc = acc + val
    return acc


def sesquilinear(d: Matrix, a_set: set[int] | tuple[int, ...],
                 b_set: set[int] | tuple[int, ...]) -> G:
    acc = ZERO
    for i in a_set:
        for j in b_set:
            acc = acc + d[i][j]
    return acc


def is_hermitian(d: Matrix) -> bool:
    n = len(d)
    return all(
        len(row) == n and all(d[i][j] == d[j][i].conj() for j in range(n))
        for i, row in enumerate(d)
    )


def det_gaussian(m: Matrix) -> G:
    """Exact Gaussian-elimination determinant over Q(i)."""
    n = len(m)
    if n == 0:
        return ONE
    a = [row[:] for row in m]
    sign = ONE
    for col in range(n):
        pivot = None
        for r in range(col, n):
            if a[r][col] != ZERO:
                pivot = r
                break
        if pivot is None:
            return ZERO
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        piv = a[col][col]
        for r in range(col + 1, n):
            if a[r][col] != ZERO:
                factor = a[r][col] / piv
                for c in range(col, n):
                    a[r][c] = a[r][c] - factor * a[col][c]
    prod = sign
    for i in range(n):
        prod = prod * a[i][i]
    return prod


def rank_gaussian(m: Matrix) -> int:
    """Exact rank over Q(i) via row reduction."""
    if not m or not m[0]:
        return 0
    rows, cols = len(m), len(m[0])
    a = [row[:] for row in m]
    r = 0
    for col in range(cols):
        pivot = None
        for i in range(r, rows):
            if a[i][col] != ZERO:
                pivot = i
                break
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        piv = a[r][col]
        for c in range(col, cols):
            a[r][c] = a[r][c] / piv
        for i in range(rows):
            if i != r and a[i][col] != ZERO:
                factor = a[i][col]
                for c in range(col, cols):
                    a[i][c] = a[i][c] - factor * a[r][c]
        r += 1
        if r == rows:
            break
    return r


def principal_submatrix(d: Matrix, indices: tuple[int, ...]) -> Matrix:
    return [[d[i][j] for j in indices] for i in indices]


def is_psd(d: Matrix) -> bool:
    """Exact PSD check: Hermitian and all 2^n - 1 principal minors >= 0."""
    if not is_hermitian(d):
        return False
    n = len(d)
    for k in range(1, n + 1):
        for subset in itertools.combinations(range(n), k):
            minor = det_gaussian(principal_submatrix(d, subset))
            if minor.im != 0 or minor.re < 0:
                return False
    return True


def is_strictly_pd(d: Matrix) -> bool:
    """Exact strict positive-definiteness via Sylvester leading principal minors."""
    if not is_hermitian(d):
        return False
    for k in range(1, len(d) + 1):
        minor = det_gaussian(principal_submatrix(d, tuple(range(k))))
        if minor.im != 0 or minor.re <= 0:
            return False
    return True


def perm_parity(perm: tuple[int, ...]) -> int:
    inv = 0
    m = len(perm)
    for i in range(m):
        for j in range(i + 1, m):
            if perm[i] > perm[j]:
                inv += 1
    return -1 if (inv % 2) else 1


# ── Standard Pauli / RI-08b 4-label qubit pair-kernel helpers ───────────────

I2: Matrix = eye(2)
X2: Matrix = [[ZERO, ONE], [ONE, ZERO]]
Y2: Matrix = [[ZERO, -IMAG], [IMAG, ZERO]]
Z2: Matrix = [[ONE, ZERO], [ZERO, -ONE]]
P2: Matrix = [[ONE, ZERO], [ZERO, IMAG]]
H0_2: Matrix = [[ONE, ONE], [ONE, -ONE]]

WP4: Matrix = block_diag(P2, mat_mul(Z2, mat_mul(P2, Z2)))
WZ4: Matrix = block_diag(Z2, Z2)
WH0_4: Matrix = block_diag(H0_2, mat_mul(Z2, mat_mul(H0_2, Z2)))


def apply_SH(d4: Matrix) -> Matrix:
    return mat_scale(Fraction(1, 2), mat_mul(WH0_4, mat_mul(d4, mat_dag(WH0_4))))


def apply_SP(d4: Matrix) -> Matrix:
    return mat_mul(WP4, mat_mul(d4, mat_dag(WP4)))


def apply_SZ(d4: Matrix) -> Matrix:
    return mat_mul(WZ4, mat_mul(d4, mat_dag(WZ4)))


def make_C4(a2: Matrix, c_val: G | int | Fraction = 0) -> Matrix:
    """RI-08b 4-label kernel D(A, c) = [[A, cZ], [conj(c)Z, ZAZ]]."""
    cc = G.coerce(c_val)
    zaz = mat_mul(Z2, mat_mul(a2, Z2))
    top_r = mat_scale(cc, Z2)
    bot_l = mat_scale(cc.conj(), Z2)
    out = zeros(4, 4)
    for i in range(2):
        for j in range(2):
            out[i][j] = a2[i][j]
            out[i][j + 2] = top_r[i][j]
            out[i + 2][j] = bot_l[i][j]
            out[i + 2][j + 2] = zaz[i][j]
    return out


D_PLUS_Z: Matrix = diag_mat([Fraction(1, 2), 0, Fraction(1, 2), 0])
D_MINUS_Z: Matrix = diag_mat([0, Fraction(1, 2), 0, Fraction(1, 2)])
D_PLUS_X: Matrix = apply_SH(D_PLUS_Z)
D_MINUS_X: Matrix = apply_SZ(D_PLUS_X)
D_PLUS_Y: Matrix = apply_SP(D_PLUS_X)
D_MINUS_Y: Matrix = apply_SZ(D_PLUS_Y)


# ── Target R1 helpers: Walsh n-cell section J_n(D) and Sylvester coupler ────


def sylvester_hadamard(p: int) -> Matrix:
    """Unnormalized 2^p x 2^p Walsh-Hadamard matrix H_0^{otimes p} in {+1,-1}."""
    h = [[ONE]]
    for _ in range(p):
        h = kron(h, H0_2)
    return h


def walsh_power(n: int) -> tuple[int, int]:
    p = 0
    size = 1
    while size < n:
        p += 1
        size *= 2
    return p, size


def walsh_section_Jn(d: Matrix) -> Matrix:
    """Dyadic-rational n-cell coarse-decoherent section J_n(D) on n*L labels."""
    n = len(d)
    p, l_size = walsh_power(n)
    h_l = sylvester_hadamard(p)
    d_pad = zeros(l_size, l_size)
    for i in range(n):
        for j in range(n):
            d_pad[i][j] = d[i][j]
    # d_tilde = (1 / L^2) * H_L * D_pad * H_L; then J_n(D) = (1 / L)?
    # Check: w_a^T (H_L D_pad H_L) w_a = L^2 D_{aa}, and beta_a^T V_a = w_a^T,
    # so (1 / L^2) V_{n,L} (I_n otimes (H_L D_pad H_L)) V_{n,L} gives mu(C_a) = D_{aa}!
    d_tilde = mat_scale(
        Fraction(1, l_size * l_size), mat_mul(h_l, mat_mul(d_pad, h_l))
    )
    blocks = []
    for a in range(n):
        omega_a = diag_mat(h_l[a])
        blocks.append(mat_mul(omega_a, mat_mul(d_tilde, omega_a)))
    return block_diag(*blocks)


def build_dyadic_antisym_hadamard(
    dim_total: int,
    even_indices: list[int],
    odd_indices: list[int],
    zero_anc_indices: list[int],
) -> tuple[Matrix, int]:
    """Construct integer U_0 on C^{dim_total} with U_0 U_0^T = 2^k I on active block.

    Returns (U_0_active_rows_or_full_op, k) where U = 2^{-k/2} U_sub on the 2^k-dim
    active subspace (and identity outside), so congruence U M U^dagger uses exact
    rational scaling on the 2^k subspace and cross-blocks? Wait: cross-blocks between
    the 2^k subspace and its complement would pick up 2^{-k/2} if k is odd!
    To keep EVERY entry of U M U^dagger 100% dyadic-rational even on cross-blocks,
    make k EVEN (so 2^{k/2} is an exact integer 2^{k//2}, hence U itself is an
    EXACT DYADIC-RATIONAL UNITARY MATRIX in Q^{dim_total x dim_total}!!).
    """
    m_fact = len(even_indices) + len(odd_indices)
    k = 0
    while (1 << k) < m_fact or (k % 2) != 0:
        k += 1
    sub_size = 1 << k
    needed_anc = sub_size - m_fact
    if len(zero_anc_indices) < needed_anc:
        raise ValueError("Not enough zero-amplitude ancilla basis indices")
    h_sub = sylvester_hadamard(k)
    # Row 1 of H_0^{otimes k} (since k >= 2 is even) has 2^{k-1} (+1)s and 2^{k-1} (-1)s.
    row1 = h_sub[1]
    plus_cols = [c for c in range(sub_size) if row1[c] == ONE]
    minus_cols = [c for c in range(sub_size) if row1[c] == -ONE]

    active_Plus = list(even_indices)
    active_Minus = list(odd_indices)
    extra = needed_anc // 2
    active_Plus.extend(zero_anc_indices[:extra])
    active_Minus.extend(zero_anc_indices[extra:2 * extra])

    col_to_basis = [0] * sub_size
    for c, b_idx in zip(plus_cols, active_Plus):
        col_to_basis[c] = b_idx
    for c, b_idx in zip(minus_cols, active_Minus):
        col_to_basis[c] = b_idx

    # Permute rows of h_sub so row 0 is the antisymmetric row (row 1 of h_sub)
    # placed at target basis index even_indices[0].
    row_order = [1, 0] + list(range(2, sub_size))
    active_basis_ordered = (
        [even_indices[0]]
        + [b for b in col_to_basis if b != even_indices[0]]
    )
    scale = Fraction(1, 1 << (k // 2))
    u_full = eye(dim_total)
    for b_idx in active_basis_ordered:
        u_full[b_idx][b_idx] = ZERO
    for r_pos, out_b in enumerate(active_basis_ordered):
        h_row = h_sub[row_order[r_pos]]
        for c_pos, in_b in enumerate(col_to_basis):
            u_full[out_b][in_b] = G.coerce(scale) * h_row[c_pos]
    return u_full, k


# ── Target R3 helpers: Part A four-birth marked growth law and active CP law ─


class Poset:
    """Immutable finite strict partial order on {0, ..., n-1} with binary marks."""

    __slots__ = ("n", "lt", "marks")

    def __init__(
        self, n: int, lt: frozenset[tuple[int, int]], marks: tuple[int, ...]
    ) -> None:
        self.n = n
        self.lt = lt
        self.marks = marks

    def is_antichain(self) -> bool:
        return len(self.lt) == 0

    def is_chain(self) -> bool:
        return len(self.lt) == self.n * (self.n - 1) // 2

    def ideals(self) -> list[frozenset[int]]:
        out: list[frozenset[int]] = []
        for mask in range(1 << self.n):
            s = frozenset(v for v in range(self.n) if (mask >> v) & 1)
            if all(u in s for (u, v) in self.lt if v in s):
                out.append(s)
        return out

    def append_birth(self, ideal: frozenset[int], bit: int) -> Poset:
        x = self.n
        new_lt = set(self.lt)
        for u in ideal:
            new_lt.add((u, x))
        return Poset(self.n + 1, frozenset(new_lt), self.marks + (bit,))

    def relabel(self, perm: tuple[int, ...]) -> Poset:
        new_lt = frozenset((perm[u], perm[v]) for (u, v) in self.lt)
        inv = [0] * self.n
        for old_v, new_v in enumerate(perm):
            inv[new_v] = old_v
        new_marks = tuple(self.marks[inv[new_v]] for new_v in range(self.n))
        return Poset(self.n, new_lt, new_marks)


Q_A = Fraction(2, 3)
Q_C = Fraction(1, 5)
Q_D = Fraction(1, 4)
Q_F = {0: Fraction(1, 6), 1: Fraction(1, 3)}
Q_G = Fraction(1, 10)
Q_K = Fraction(11, 20)
Q_H = {0: Fraction(19, 30), 1: Fraction(7, 15)}
Q_E = Fraction(1, 44)


def q_part_a(p: Poset, s: frozenset[int]) -> Fraction:
    """Exact Part A structural probability q(P, r, S) for parent sizes 0..3."""
    n = p.n
    if n == 0:
        assert len(s) == 0
        return Fraction(1, 1)
    if n == 1:
        return Q_A if len(s) == 0 else (Fraction(1, 1) - Q_A)
    if n == 2:
        if len(p.lt) == 0:  # 2-antichain
            if len(s) == 0:
                return Q_D
            if len(s) == 1:
                return Q_G
            return Q_K
        # 2-chain u < v
        (u, _v) = next(iter(p.lt))
        i = p.marks[u]
        if len(s) == 0:
            return Q_C
        if s == frozenset({u}):
            return Q_F[i]
        if len(s) == 2:
            return Q_H[i]
        raise ValueError("Invalid ideal in 2-chain")
    if n == 3:
        all_ideals = p.ideals()
        full = frozenset(range(3))
        if s == full:
            proper_sum = sum(q_part_a(p, t) for t in all_ideals if t != full)
            return Fraction(1, 1) - proper_sum
        m = len(p.lt)
        if m == 0:  # 3-antichain
            if len(s) == 0:
                return Q_E
            if len(s) == 1:
                return Q_E * Q_G / Q_D
            if len(s) == 2:
                return Q_E * Q_K / Q_D
        if m == 1:  # edge u < v, isolate w
            (u, v) = next(iter(p.lt))
            w = next(x for x in range(3) if x not in (u, v))
            if len(s) == 0 or s == frozenset({w}):
                return Q_E
            if s == frozenset({u}):
                return Q_E * Q_F[p.marks[u]] / Q_C
            if s == frozenset({u, v}):
                return Q_E * Q_H[p.marks[u]] / Q_C
            if s == frozenset({u, w}):
                return Q_E * Q_K / Q_G
        if m == 2:
            mins = [x for x in range(3) if not any(y != x and (y, x) in p.lt for y in range(3))]
            if len(mins) == 1:  # Fork: root u < leaf1, u < leaf2
                u = mins[0]
                i = p.marks[u]
                if len(s) == 0 or s == frozenset({u}):
                    return Q_E
                if len(s) == 2 and u in s:
                    return Q_E * Q_H[i] / Q_F[i]
            else:  # Join: min1 < top, min2 < top
                if len(s) in (0, 1, 2):
                    return Q_E
        if m == 3:  # 3-chain
            return Q_E
        raise ValueError(f"Unhandled 3-parent ideal: lt={p.lt}, s={s}")
    raise ValueError(f"Unsupported parent size: {n}")


ACTIVE_THETA = Fraction(1, 32)
ACTIVE_T = Fraction(1, 2)
ACTIVE_A = (
    Fraction(1, 264),
    Fraction(1, 264),
    Fraction(1, 176),
    Fraction(1, 44),
    Fraction(1, 1),
)
# O_P on Bloch (X, Y, Z): P X P^dagger = Y, P Y P^dagger = -X, P Z P^dagger = Z
# So s' = O_P s has O_P = [[0, -1, 0], [1, 0, 0], [0, 0, 1]].
O_P_BLOCH: list[list[Fraction]] = [
    [Fraction(0), Fraction(-1), Fraction(0)],
    [Fraction(1), Fraction(0), Fraction(0)],
    [Fraction(0), Fraction(0), Fraction(1)],
]
O_P_INV_BLOCH: list[list[Fraction]] = [
    [Fraction(0), Fraction(1), Fraction(0)],
    [Fraction(-1), Fraction(0), Fraction(0)],
    [Fraction(0), Fraction(0), Fraction(1)],
]


def bloch_pow_inv(n: int) -> list[list[Fraction]]:
    res = [
        [Fraction(1 if i == j else 0) for j in range(3)]
        for i in range(3)
    ]
    for _ in range(n):
        nxt = [[Fraction(0) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for k in range(3):
                for j in range(3):
                    nxt[i][j] += res[i][k] * O_P_INV_BLOCH[k][j]
        res = nxt
    return res


def active_r_vec(p: Poset, s: frozenset[int]) -> tuple[Fraction, Fraction, Fraction]:
    """Current-prefix Bloch vector r_C(S) = theta * 2^n * [H(P+S)-H(P)] * w_0^T O_P^{-n}."""
    n = p.n
    h_curr = ACTIVE_A[n] if p.is_antichain() else Fraction(0)
    next_antichain = p.is_antichain() and (len(s) == 0)
    h_next = ACTIVE_A[n + 1] if next_antichain else Fraction(0)
    scalar = ACTIVE_THETA * (1 << n) * (h_next - h_curr)
    # w_0 = (0, 1, 0)^T (initial Y-phase axis!)
    w0 = [Fraction(0), Fraction(1), Fraction(0)]
    op_inv_n = bloch_pow_inv(n)
    vec = [
        scalar * sum(w0[k] * op_inv_n[k][j] for k in range(3))
        for j in range(3)
    ]
    return (vec[0], vec[1], vec[2])


def active_G_matrix(r_vec: tuple[Fraction, Fraction, Fraction]) -> Matrix:
    """Strictly PD 4x4 effect matrix G_r = diag(F_r, Z F_r Z), F_r = (1-t)I_2 + r . sigma."""
    rx, ry, rz = r_vec
    one_minus_t = Fraction(1, 1) - ACTIVE_T
    f_r = mat_add(
        mat_scale(one_minus_t, I2),
        mat_add(
            mat_scale(rx, X2),
            mat_add(mat_scale(ry, Y2), mat_scale(rz, Z2)),
        ),
    )
    zfz = mat_mul(Z2, mat_mul(f_r, Z2))
    return block_diag(f_r, zfz)


def active_branch_map(p: Poset, s: frozenset[int], _bit: int, d4: Matrix) -> Matrix:
    """Active pair-kernel branch map B^{P,r}_{S,b}(D) on M_4(C) preserving C_4."""
    q_val = q_part_a(p, s)
    r_vec = active_r_vec(p, s)
    g_mat = active_G_matrix(r_vec)
    tr_gd = mat_trace(mat_mul(g_mat, d4))
    coherent = mat_scale(ACTIVE_T, mat_mul(WP4, mat_mul(d4, mat_dag(WP4))))
    repl = mat_scale(tr_gd * G.coerce(Fraction(1, 4)), eye(4))
    return mat_scale(q_val * Fraction(1, 2), mat_add(coherent, repl))


def superop_16x16(map_fn) -> Matrix:
    """Exact 16x16 superoperator matrix of a C-linear map M_4(C) -> M_4(C)."""
    sup = zeros(16, 16)
    for r in range(4):
        for c in range(4):
            col_idx = 4 * r + c
            e_rc = zeros(4, 4)
            e_rc[r][c] = ONE
            out = map_fn(e_rc)
            for i in range(4):
                for j in range(4):
                    sup[4 * i + j][col_idx] = out[i][j]
    return sup


def choi_16x16(map_fn) -> Matrix:
    """Exact 16x16 Choi matrix sum_{r,c} E_{rc} otimes map_fn(E_{rc})."""
    ch = zeros(16, 16)
    for r in range(4):
        for c in range(4):
            e_rc = zeros(4, 4)
            e_rc[r][c] = ONE
            out = map_fn(e_rc)
            for i in range(4):
                for j in range(4):
                    ch[4 * r + i][4 * c + j] = out[i][j]
    return ch


# ── Verification Test Suite ─────────────────────────────────────────────────


class RelationalIdentityCompletionTests(unittest.TestCase):
    """Self-contained exact tests for Targets R1, R2, and R3."""

    # ── Target R1 ───────────────────────────────────────────────────────────

    def test_01_walsh_section_and_dyadic_coarse_cell_minors(self) -> None:
        """Theorem 1A: Walsh section J_n(D) + ~_T-lifted dyadic coupler gives all minors."""
        # 1. Explicit full 16x16 raw verification for n=2 (both PSD and non-PSD D).
        d2_psd: Matrix = [
            [G(Fraction(3, 5)), G(Fraction(1, 5), Fraction(-1, 5))],
            [G(Fraction(1, 5), Fraction(1, 5)), G(Fraction(2, 5))],
        ]
        d2_bad: Matrix = [
            [G(Fraction(1, 2)), G(Fraction(3, 5), Fraction(2, 5))],
            [G(Fraction(3, 5), Fraction(-2, 5)), G(Fraction(1, 2))],
        ]
        for d2, expect_psd in ((d2_psd, True), (d2_bad, False)):
            j2_d = walsh_section_Jn(d2)
            self.assertEqual(len(j2_d), 4)
            self.assertEqual(is_psd(j2_d), expect_psd)
            self.assertEqual(total_mass(j2_d), mat_trace(d2))
            c0, c1 = {0, 1}, {2, 3}
            self.assertEqual(sesquilinear(j2_d, c0, c1), ZERO)
            self.assertEqual(sesquilinear(j2_d, c0, c0), d2[0][0])
            self.assertEqual(sesquilinear(j2_d, c1, c1), d2[1][1])

            # 2-copy composite J_2(D) otimes J_2(D) on 16 raw labels.
            raw_16 = kron(j2_d, j2_d)
            # Untwist T = Pi * (V_2 otimes V_2), identical to RI-08d!
            # Regrouped index p(a0, a1, j0, j1) = 4*(2*a0 + a1) + (2*j0 + j1),
            # tensor index q(a0, j0, a1, j1) = 4*(2*a0 + j0) + (2*a1 + j1).
            t_mat = zeros(16, 16)
            for a0 in range(2):
                for a1 in range(2):
                    for j0 in range(2):
                        for j1 in range(2):
                            p_idx = 4 * (2 * a0 + a1) + (2 * j0 + j1)
                            q_idx = 4 * (2 * a0 + j0) + (2 * a1 + j1)
                            sgn = -1 if ((a0 * j0 + a1 * j1) % 2) else 1
                            t_mat[p_idx][q_idx] = G(sgn)
            self.assertEqual(mat_mul(t_mat, mat_dag(t_mat)), eye(16))

            # Build exact dyadic coupler on C^2 otimes C^2 (k=2 => scale 1/2, 1 ancilla?
            # Even simpler for m=2: 2x2 exchange block with H_0 has scale 1/sqrt(2), or
            # with 1 ancilla D_{+Z} (k=2, scale 1/2!) U_full itself is 100% rational!
            # And on m=2 without ancilla, U_0 congruence (1/2) U_0 (.) U_0^T on the
            # exchange subspace {01, 10} + identity outside: wait, cross terms with
            # {00, 11} would need sqrt(2) unless {00, 11} ALSO undergo H_0!
            # APPLYING H_0 ON {01, 10} AND H_0 ON {00, 11} GIVES A 4x4 INTEGER MATRIX
            # U_0 WITH U_0 U_0^T = 2 I_4, SO (1/2) U_0 (.) U_0^T IS 100% RATIONAL
            # ON ALL 4x4 BLOCKS WITH ZERO ANCILLAS!!
            u0_sys = [
                [ONE, ZERO, ZERO, ONE],
                [ZERO, ONE, -ONE, ZERO],
                [ZERO, ONE, ONE, ZERO],
                [ONE, ZERO, ZERO, -ONE],
            ]
            self.assertEqual(mat_mul(u0_sys, mat_dag(u0_sys)), mat_scale(2, eye(4)))
            # Conjugate into Walsh-transformed internal basis: H_4 = H_0 otimes H_0
            h4 = sylvester_hadamard(2)
            # H_4^{-1} = (1/4) H_4
            u0_tilde = mat_scale(
                Fraction(1, 4), mat_mul(h4, mat_mul(u0_sys, h4))
            )
            big_u0 = mat_mul(
                mat_dag(t_mat),
                mat_mul(kron(eye(4), u0_tilde), t_mat),
            )
            coupled_16 = mat_scale(
                Fraction(1, 2), mat_mul(big_u0, mat_mul(raw_16, mat_dag(big_u0)))
            )
            self.assertTrue(is_hermitian(coupled_16))
            self.assertEqual(total_mass(coupled_16), ONE)

            # Coarse product cells in tensor order:
            coarse_cells = []
            for a0 in range(2):
                for a1 in range(2):
                    cell = {
                        4 * (2 * a0 + j0) + (2 * a1 + j1)
                        for j0 in range(2)
                        for j1 in range(2)
                    }
                    coarse_cells.append(cell)
            # Check exact coarse-cell decoherence across ALL 4 coarse product cells!
            for idx_a in range(4):
                for idx_b in range(4):
                    if idx_a != idx_b:
                        self.assertEqual(
                            sesquilinear(
                                coupled_16, coarse_cells[idx_a], coarse_cells[idx_b]
                            ),
                            ZERO,
                        )
            # Coarse cell (0, 1) (index 1) has exact weight det(D)!
            det_d2 = det_gaussian(d2)
            self.assertEqual(
                sesquilinear(coupled_16, coarse_cells[1], coarse_cells[1]),
                det_d2,
            )

        # 2. n=3 (12-label Walsh section) and all 7 principal minors (m=1, 2, 3)
        # using exact dyadic-rational unitary U_full (k=2 for m=2,3 with 1 ancilla D_{+Z}).
        d3_psd: Matrix = [
            [G(Fraction(2, 5)), G(Fraction(1, 10), Fraction(1, 10)), G(Fraction(1, 10))],
            [G(Fraction(1, 10), Fraction(-1, 10)), G(Fraction(3, 10)), G(0, Fraction(1, 10))],
            [G(Fraction(1, 10)), G(0, Fraction(-1, 10)), G(Fraction(3, 10))],
        ]
        # Non-PSD 3x3 Hermitian with Tr=1, all 1x1 and 2x2 minors > 0, det(D) < 0!
        d3_neg3: Matrix = [
            [G(Fraction(1, 3)), G(Fraction(1, 4)), G(Fraction(1, 4))],
            [G(Fraction(1, 4)), G(Fraction(1, 3)), G(Fraction(-1, 4))],
            [G(Fraction(1, 4)), G(Fraction(-1, 4)), G(Fraction(1, 3))],
        ]
        self.assertTrue(is_psd(d3_psd))
        self.assertFalse(is_psd(d3_neg3))
        for pair in ((0, 1), (0, 2), (1, 2)):
            self.assertGreater(
                det_gaussian(principal_submatrix(d3_neg3, pair)).re, 0
            )
        self.assertLess(det_gaussian(d3_neg3).re, 0)

        for d3, expect_psd in ((d3_psd, True), (d3_neg3, False)):
            j3 = walsh_section_Jn(d3)
            self.assertEqual(len(j3), 12)
            self.assertEqual(total_mass(j3), ONE)
            self.assertEqual(is_psd(j3), expect_psd)
            cells_3 = [set(range(4 * a, 4 * (a + 1))) for a in range(3)]
            for a in range(3):
                for b in range(3):
                    if a != b:
                        self.assertEqual(sesquilinear(j3, cells_3[a], cells_3[b]), ZERO)
                    else:
                        self.assertEqual(sesquilinear(j3, cells_3[a], cells_3[a]), d3[a][a])

            # Test all 2x2 minors (m=2) and 3x3 minor (m=3) via dyadic rational U_I
            # with a single ancilla D_{+Z} (n_anc = 1, dim_anc = 2):
            # for m=2, k=2 (2! = 2 <= 4, 9 >= 2 zero states);
            # for m=3, k=4 (3! = 6 <= 16, 27 >= 10 zero states, 2^{k/2} = 4 exact!).
            for m_size, n_anc in ((2, 1), (3, 1)):
                dim_cand = 3 ** m_size
                dim_anc = 1 << n_anc
                dim_tot = dim_cand * dim_anc
                zero_anc = [
                    c_idx * dim_anc + a_idx
                    for c_idx in range(dim_cand)
                    for a_idx in range(1, dim_anc)
                ]
                # Build input state D^{otimes m} otimes |0...0><0...0| in untwisted cell basis
                d_power = d3
                for _ in range(m_size - 1):
                    d_power = kron(d_power, d3)
                anc_proj = zeros(dim_anc, dim_anc)
                anc_proj[0][0] = ONE
                state_in = kron(d_power, anc_proj)

                for subset in itertools.combinations(range(3), m_size):
                    even_idx: list[int] = []
                    odd_idx: list[int] = []
                    for perm in itertools.permutations(range(m_size)):
                        tup = tuple(subset[p] for p in perm)
                        lin = 0
                        for x in tup:
                            lin = 3 * lin + x
                        full_idx = lin * dim_anc + 0
                        if perm_parity(perm) == 1:
                            even_idx.append(full_idx)
                        else:
                            odd_idx.append(full_idx)
                    u_dyadic, k_exp = build_dyadic_antisym_hadamard(
                        dim_tot, even_idx, odd_idx, zero_anc
                    )
                    # Verify exact rational unitarity U * U^dagger = I!
                    self.assertEqual(
                        mat_mul(u_dyadic, mat_dag(u_dyadic)), eye(dim_tot)
                    )
                    state_out = mat_mul(u_dyadic, mat_mul(state_in, mat_dag(u_dyadic)))
                    # In the ~_T-untwisted product section, coarse product cell idx `idx`
                    # has exact weight state_out[idx][idx] and total mass Tr(state_out) = 1,
                    # with ALL off-diagonal coarse-cell cross-forms identically 0!
                    self.assertEqual(mat_trace(state_out), ONE)
                    target_cell = even_idx[0]
                    m_fact = 2 if m_size == 2 else 6
                    expected = (
                        G.coerce(Fraction(m_fact, 1 << k_exp))
                        * det_gaussian(principal_submatrix(d3, subset))
                    )
                    self.assertEqual(state_out[target_cell][target_cell], expected)

    def test_02_single_ancilla_raw_mass_preserving_obstruction(self) -> None:
        """Theorem 1B: Single 4-label ancilla in C_4 with V_x 1_4 = 1_4 cannot isolate det."""
        # Verify the kernel norm bound |1_4^dagger y|^2 <= 2 ||y||_2^2 across all three
        # strata of RI-08b's cone C_4:
        #   (A) c = 0, rank-1 pure state A = (1/2)|psi><psi| (tested on +Z, +X, +Y, and (3,4)/5)
        #   (B) |c| > 0 boundary A = (1/4)I_2, c = (1/4)e^{i phi} (tested on c=1/4, i/4, (3+4i)/20)
        #   (C) interior A > |c|I_2 => ker(D) = {0}.
        psi_34 = [
            [G(Fraction(9, 50)), G(Fraction(12, 50))],
            [G(Fraction(12, 50)), G(Fraction(16, 50))],
        ]
        boundary_states = [
            D_PLUS_Z,
            D_PLUS_X,
            D_PLUS_Y,
            make_C4(psi_34, 0),
            make_C4(mat_scale(Fraction(1, 4), I2), Fraction(1, 4)),
            make_C4(mat_scale(Fraction(1, 4), I2), G(0, Fraction(1, 4))),
            make_C4(
                mat_scale(Fraction(1, 4), I2),
                G(Fraction(3, 20), Fraction(4, 20)),
            ),
        ]
        interior_state = make_C4(
            [[G(Fraction(3, 10)), ZERO], [ZERO, G(Fraction(2, 10))]],
            Fraction(1, 10),
        )
        self.assertEqual(rank_gaussian(interior_state), 4)

        for d_anc in boundary_states:
            self.assertTrue(is_psd(d_anc))
            self.assertEqual(total_mass(d_anc), ONE)
            self.assertEqual(sesquilinear(d_anc, {0, 1}, {2, 3}), ZERO)
            self.assertLess(rank_gaussian(d_anc), 4)
            # For every permutation matrix V on Omega_4 (all 24 satisfy V 1_4 = 1_4),
            # check that v = V^T beta_1 gives (v_+ + v_-)^dagger D_anc (v_+ + v_-) > 0
            # whenever v_+ != v_-, so D = (1/2) 1_2 1_2^T (det = 0) gets nonzero weight!
            perms_v = set()
            for perm in itertools.permutations(range(4)):
                v = tuple(1 if perm[i] in (2, 3) else 0 for i in range(4))
                perms_v.add(v)
            self.assertEqual(len(perms_v), 6)
            for vp in perms_v:
                for vm in perms_v:
                    u = [G(vp[i] + vm[i]) for i in range(4)]
                    quad = ZERO
                    for i in range(4):
                        for j in range(4):
                            quad = quad + u[i].conj() * d_anc[i][j] * u[j]
                    self.assertEqual(quad.im, 0)
                    if vp != vm:
                        # quad > 0 (contaminating det=0 state with permanent); quad == 0 is
                        # impossible by Cauchy-Schwarz since ||vp||^2=||vm||^2=2, 1^T(vp+vm)=4.
                        self.assertGreater(quad.re, 0)

    # ── Target R2 ───────────────────────────────────────────────────────────

    def test_03_quotient_escape_and_noncompact_scaling_exclusion(self) -> None:
        """Theorem 2A: ~_T quotient escapes rank-1 Gamma_4 and excludes M_lambda."""
        # 1. Rank-1 Gamma_4 on raw K_4 vs full-rank Tr on C_4 / ~_T:
        gamma_4 = [[ONE for _ in range(4)] for _ in range(4)]
        self.assertEqual(rank_gaussian(gamma_4), 1)
        # Generic asymmetric Bloch state (Tr=1/2, a00-a11=1/5, Re(a01)=1/10, Im(a01)=-1/20)
        # generates all 24 octahedral Clifford images; D(A, 0) and D(A, c) match on every word!
        a_asym = [
            [G(Fraction(7, 20)), G(Fraction(1, 10), Fraction(-1, 20))],
            [G(Fraction(1, 10), Fraction(1, 20)), G(Fraction(3, 20))],
        ]
        d_asym0 = make_C4(a_asym, 0)
        d_asym1 = make_C4(a_asym, G(Fraction(1, 30), Fraction(-1, 40)))
        self.assertTrue(is_psd(d_asym0))
        self.assertTrue(is_psd(d_asym1))
        seen_asym = [d_asym0]
        pairs_asym = [(d_asym0, d_asym1)]
        q_asym = [d_asym0]
        while q_asym:
            c0 = q_asym.pop(0)
            c1 = pairs_asym[seen_asym.index(c0)][1]
            for fn in (apply_SH, apply_SP, apply_SZ):
                n0, n1 = fn(c0), fn(c1)
                if n0 not in seen_asym:
                    seen_asym.append(n0)
                    pairs_asym.append((n0, n1))
                    q_asym.append(n0)
        self.assertEqual(len(seen_asym), 24)
        for k0, k1 in pairs_asym:
            self.assertEqual(
                sesquilinear(k0, {0, 1}, {0, 1}), sesquilinear(k1, {0, 1}, {0, 1})
            )
            self.assertEqual(
                sesquilinear(k0, {2, 3}, {2, 3}), sesquilinear(k1, {2, 3}, {2, 3})
            )

        # 2. Exclusion of OPERATION_DOMAIN.md's noncompact scaling M_lambda = P_+ + lambda P_-:
        # On raw K_2, M_lambda preserves M_2(D) = 1_2^dagger D 1_2 because Gamma_2 = 2 P_+ has
        # nullspace span{|->}. Lifted to C_4 via tilde_M_lambda = diag(M_lambda, Z M_lambda Z),
        # M_4 on {I, S_H}-reachable preparations {D_{+Z}, D_{-Z}, D_{+X}, D_{-X}} gives
        # M_4(tilde_M_lambda D_{+X} tilde_M_lambda^dagger) = 1,
        # M_4(tilde_M_lambda D_{+Z} tilde_M_lambda^dagger) = (1 + lambda^2) / 2, and
        # M_4(tilde_M_lambda D_{-X} tilde_M_lambda^dagger) = lambda^2, forcing lambda = 1!
        d_minus_x = apply_SH(D_MINUS_Z)
        for lam in (Fraction(1, 2), Fraction(2, 1), Fraction(3, 2)):
            p_plus = mat_scale(Fraction(1, 2), [[ONE, ONE], [ONE, ONE]])
            p_minus = mat_scale(Fraction(1, 2), [[ONE, -ONE], [-ONE, ONE]])
            m_lam = mat_add(p_plus, mat_scale(lam, p_minus))
            # Raw 2-label mass preservation holds even for lam != 1:
            d_z0_raw = [[ONE, ZERO], [ZERO, ZERO]]
            self.assertEqual(
                total_mass(mat_mul(m_lam, mat_mul(d_z0_raw, mat_dag(m_lam)))), ONE
            )
            # Lifted to C_4, M_4 preservation fails on D_{+Z} and D_{-X} = S_H(D_{-Z}):
            zmz = mat_mul(Z2, mat_mul(m_lam, Z2))
            tilde_m = block_diag(m_lam, zmz)
            out_px = mat_mul(tilde_m, mat_mul(D_PLUS_X, mat_dag(tilde_m)))
            out_pz = mat_mul(tilde_m, mat_mul(D_PLUS_Z, mat_dag(tilde_m)))
            out_mx = mat_mul(tilde_m, mat_mul(d_minus_x, mat_dag(tilde_m)))
            self.assertEqual(total_mass(out_px), ONE)
            self.assertEqual(
                total_mass(out_pz), G(Fraction(1, 2) + Fraction(1, 2) * lam * lam)
            )
            self.assertEqual(total_mass(out_mx), G(lam * lam))
            self.assertNotEqual(total_mass(out_pz), ONE)
            self.assertNotEqual(total_mass(out_mx), ONE)

    def test_04_identity_atomicity_and_generator_observability(self) -> None:
        """Theorems 2B & 2C: Identity-atomicity vs classical; generator observability vs rebit."""
        # 1. Theorem 2B: Classical Diag_+(Omega_d) fails identity-atomicity for d=2, 3, 4.
        for d in (2, 3, 4):
            # Instrument T_i(diag(p)) = p_i E_{ii} sums to id_{Diag_d}, yet T_0 is not p_0 * id.
            e0 = diag_mat([1 if k == 0 else 0 for k in range(d)])
            e1 = diag_mat([1 if k == 1 else 0 for k in range(d)])
            # T_0(e0) = e0 != c * e0 and T_0(e1) = 0 => proportionality impossible!
            t0_e0 = mat_mul(e0, mat_mul(e0, e0))
            t0_e1 = mat_mul(e0, mat_mul(e1, e0))
            self.assertEqual(t0_e0, e0)
            self.assertEqual(t0_e1, zeros(d, d))

        # Faithful pure entangled probe verification on PSD_2(R) and PSD_2(C):
        # Bell vector |Phi+> = (1, 0, 0, 1)^T / sqrt(2) => Psi = (1/2) |v><v|, v = (1,0,0,1)^T.
        # Map T -> (T otimes I_2)(Psi) is proportional to the Choi matrix (1/2) Choi(T),
        # which is rank-1 on Psi and injective on ALL linear maps (both real 3x3->3x3 CP maps
        # and complex 4x4->4x4 CP maps), and any decomposition Psi = B_0 + B_1 with B_x >= 0
        # forces B_x = p_x Psi since rank(Psi) = 1!
        v_bell = [ONE, ZERO, ZERO, ONE]
        psi_bell = [[v_bell[i] * v_bell[j] for j in range(4)] for i in range(4)]
        psi_bell = mat_scale(Fraction(1, 2), psi_bell)
        self.assertTrue(is_psd(psi_bell))
        self.assertEqual(mat_trace(psi_bell), ONE)
        self.assertEqual(rank_gaussian(psi_bell), 1)
        # Verify Choi injectivity on the 16-dimensional complex space L(M_2(C))
        basis_images: list[list[G]] = []
        for a in range(2):
            for b in range(2):
                for c in range(2):
                    for d_idx in range(2):
                        # Basis map X -> E_{ab} X_{cd}
                        def basis_map(
                            x: Matrix, a: int = a, b: int = b, c: int = c, d_idx: int = d_idx
                        ) -> Matrix:
                            out = zeros(2, 2)
                            out[a][b] = x[c][d_idx]
                            return out

                        img = zeros(4, 4)
                        for r_blk in range(2):
                            for c_blk in range(2):
                                sub = [[psi_bell[2 * r_blk + i][2 * c_blk + j] for j in range(2)]
                                       for i in range(2)]
                                m_sub = basis_map(sub)
                                for i in range(2):
                                    for j in range(2):
                                        img[2 * r_blk + i][2 * c_blk + j] = m_sub[i][j]
                        basis_images.append([img[i][j] for i in range(4) for j in range(4)])
        self.assertEqual(rank_gaussian(basis_images), 16)

        # 2. Theorem 2C: Generator observability on Rebit Sym_2(R) vs Qubit Herm_2(C).
        # Rebit basis {I_2, X_2, Z_2} (dim 3), generator D_{J_0}(rho) = [J_0, rho],
        # J_0 = [[0, -1], [1, 0]].
        j0: Matrix = [[ZERO, -ONE], [ONE, ZERO]]
        rebit_basis = [I2, X2, Z2]

        def comm(a: Matrix, b: Matrix) -> Matrix:
            return mat_sub(mat_mul(a, b), mat_mul(b, a))

        # Express D_{J_0}(B_k) in rebit_basis via trace inner product (1/2) Tr(B_j * .):
        d_j0_rebit = zeros(3, 3)
        for col, bk in enumerate(rebit_basis):
            img = comm(j0, bk)
            for row, bj in enumerate(rebit_basis):
                d_j0_rebit[row][col] = G.coerce(Fraction(1, 2)) * mat_trace(mat_mul(bj, img))
        # Rank of D_{J_0} on Sym_2(R) is 2! Its left nullspace {ell : ell D_{J_0} = 0} has
        # dimension 3 - 2 = 1, spanned solely by ell = (1, 0, 0) = Tr!
        self.assertEqual(rank_gaussian(d_j0_rebit), 2)
        self.assertEqual(comm(j0, I2), zeros(2, 2))
        self.assertEqual(comm(j0, Z2), mat_scale(2, X2))
        self.assertEqual(comm(j0, X2), mat_scale(-2, Z2))

        # On Herm_2(C) (basis {I_2, X_2, Y_2, Z_2}, dim 4), su(2) generators D_{-i sigma_a / 2}
        # map injectively via phi(D_{-i H})(rho) = Tr(H rho) onto traceless observables
        # span{X_2, Y_2, Z_2}: self-conserved, non-constant, and NOT conserved by all su(2)!
        pauli_traceless = [X2, Y2, Z2]
        qubit_basis = [I2, X2, Y2, Z2]
        phi_matrix = zeros(3, 4)
        for gen_idx, h_gen in enumerate(pauli_traceless):
            # Self-conservation: Tr(h_gen * [-i h_gen, B_k]) == 0 for all B_k in qubit_basis
            for col, bk in enumerate(qubit_basis):
                flow = comm(mat_scale(-IMAG, h_gen), bk)
                self.assertEqual(mat_trace(mat_mul(h_gen, flow)), ZERO)
                phi_matrix[gen_idx][col] = mat_trace(mat_mul(h_gen, bk))
            # Non-constancy & non-conservation under another su(2) generator:
            other_h = pauli_traceless[(gen_idx + 1) % 3]
            found_nonconserved = any(
                mat_trace(mat_mul(h_gen, comm(mat_scale(-IMAG, other_h), bk))) != ZERO
                for bk in qubit_basis
            )
            self.assertTrue(found_nonconserved)
        # Injectivity of phi: rank(phi_matrix) == 3, and column 0 (on I_2) is zero (traceless).
        self.assertEqual(rank_gaussian(phi_matrix), 3)
        for gen_idx in range(3):
            self.assertEqual(phi_matrix[gen_idx][0], ZERO)

    def test_05_minimal_rank_characterizes_compatible_complex_structure(self) -> None:
        """Theorem 2D: For D = G + i*Omega >= 0 (G > 0), rank_C(D) >= m with '=' iff J^2 = -I."""
        # 1. why_complex.py family D_t = (I_{2m} + i * t * J_0) / 2 for m=1 and m=2:
        for m_pairs in (1, 2):
            dim = 2 * m_pairs
            j_std = zeros(dim, dim)
            for k in range(m_pairs):
                j_std[2 * k][2 * k + 1] = ONE
                j_std[2 * k + 1][2 * k] = -ONE
            neg_eye = mat_scale(-1, eye(dim))

            for t_val in (
                Fraction(0, 1),
                Fraction(1, 3),
                Fraction(4, 5),
                Fraction(1, 1),
                Fraction(-1, 1),
                Fraction(6, 5),
            ):
                d_t = mat_scale(
                    Fraction(1, 2),
                    mat_add(eye(dim), mat_scale(G(0, t_val), j_std)),
                )
                # G = (1/2) I, Omega = (t/2) J_std => J = G^{-1} Omega = t * J_std
                j_op = mat_scale(t_val, j_std)
                j_sq = mat_mul(j_op, j_op)
                # Schur complement G + Omega G^{-1} Omega = (1/2)(1 - t^2) I
                schur = mat_scale(Fraction(1, 2) * (1 - t_val * t_val), eye(dim))

                if abs(t_val) <= 1:
                    self.assertTrue(is_psd(d_t))
                    self.assertTrue(is_psd(schur))
                    rk = rank_gaussian(d_t)
                    self.assertGreaterEqual(rk, m_pairs)
                    self.assertEqual(rk == m_pairs, j_sq == neg_eye)
                else:
                    self.assertFalse(is_psd(d_t))
                    self.assertFalse(is_psd(schur))

        # 2. Non-identity metric G != I_{2m} (anisotropic G > 0 on dim = 4, m = 2):
        # Take G = diag(1, 4, 9, 1) > 0. For J^2 = -I_4 with Omega = G J skew-symmetric:
        # G_00 J_01 = -G_11 J_10 and J_01 J_10 = -1 => J_01 = 2, J_10 = -1/2 => Omega_01 = 2;
        # G_22 J_23 = -G_33 J_32 and J_23 J_32 = -1 => J_23 = 1/3, J_32 = -3 => Omega_23 = 3!
        g_aniso = diag_mat([1, 4, 9, 1])
        g_inv = diag_mat([1, Fraction(1, 4), Fraction(1, 9), 1])
        om_compat = [
            [ZERO, G(2), ZERO, ZERO],
            [G(-2), ZERO, ZERO, ZERO],
            [ZERO, ZERO, ZERO, G(3)],
            [ZERO, ZERO, G(-3), ZERO],
        ]
        d_compat = mat_add(g_aniso, mat_scale(IMAG, om_compat))
        j_compat = mat_mul(g_inv, om_compat)
        self.assertTrue(is_psd(d_compat))
        self.assertEqual(rank_gaussian(d_compat), 2)
        self.assertEqual(mat_mul(j_compat, j_compat), mat_scale(-1, eye(4)))

        # Perturb one symplectic block (Omega_23 = 2 instead of 3): still PSD, rank jumps to 3,
        # and J^2 != -I_4!
        om_mixed = [row[:] for row in om_compat]
        om_mixed[2][3] = G(2)
        om_mixed[3][2] = G(-2)
        d_mixed = mat_add(g_aniso, mat_scale(IMAG, om_mixed))
        j_mixed = mat_mul(g_inv, om_mixed)
        self.assertTrue(is_psd(d_mixed))
        self.assertEqual(rank_gaussian(d_mixed), 3)
        self.assertNotEqual(mat_mul(j_mixed, j_mixed), mat_scale(-1, eye(4)))

    # ── Target R3 ───────────────────────────────────────────────────────────

    def test_06_active_pair_kernel_cp_normalization_and_superoperator_diamonds(self) -> None:
        """Theorem 3A: Complete positivity, normalization, noncommutativity, and 16x16 diamonds."""
        empty = Poset(0, frozenset(), ())
        by_size: dict[int, list[Poset]] = {0: [empty], 1: [], 2: [], 3: []}
        seen_keys: set[tuple[int, frozenset[tuple[int, int]], tuple[int, ...]]] = {
            (0, empty.lt, empty.marks)
        }
        for sz in range(3):
            for p in by_size[sz]:
                for s in p.ideals():
                    for b in (0, 1):
                        child = p.append_birth(s, b)
                        key = (child.n, child.lt, child.marks)
                        if key not in seen_keys:
                            seen_keys.add(key)
                            by_size[sz + 1].append(child)

        test_c4_states = [
            D_PLUS_Z,
            D_MINUS_Z,
            D_PLUS_X,
            D_PLUS_Y,
            D_MINUS_Y,
            make_C4(
                [[G(Fraction(3, 10)), G(Fraction(1, 20), Fraction(1, 20))],
                 [G(Fraction(1, 20), Fraction(-1, 20)), G(Fraction(2, 10))]],
                G(Fraction(1, 20), Fraction(-1, 20)),
            ),
        ]

        # Cache unscaled 16x16 superoperators by r_vec, and verify strict PD of both
        # the 4x4 effect G_r, the 4x4 qubit Choi matrix, and the full 16x16 Choi matrix!
        unit_sup_by_r: dict[tuple[Fraction, Fraction, Fraction], Matrix] = {}

        def get_branch_sup(p: Poset, s: frozenset[int]) -> Matrix:
            r_vec = active_r_vec(p, s)
            if r_vec not in unit_sup_by_r:
                g_mat = active_G_matrix(r_vec)
                self.assertTrue(is_strictly_pd(g_mat))

                def unit_map(d4: Matrix, g_mat: Matrix = g_mat) -> Matrix:
                    tr_gd = mat_trace(mat_mul(g_mat, d4))
                    coh = mat_scale(ACTIVE_T, mat_mul(WP4, mat_mul(d4, mat_dag(WP4))))
                    rep = mat_scale(tr_gd * G.coerce(Fraction(1, 4)), eye(4))
                    return mat_add(coh, rep)

                # Verify full 16x16 Choi matrix on M_4(C) is strictly positive-definite!
                self.assertTrue(is_strictly_pd(choi_16x16(unit_map)))
                # Verify cone preservation C_4 -> C_4 on all 6 test states:
                for d_in in test_c4_states:
                    d_out = unit_map(d_in)
                    self.assertTrue(is_psd(d_out))
                    self.assertEqual(sesquilinear(d_out, {0, 1}, {2, 3}), ZERO)
                unit_sup_by_r[r_vec] = superop_16x16(unit_map)
            q_half = q_part_a(p, s) * Fraction(1, 2)
            return mat_scale(q_half, unit_sup_by_r[r_vec])

        def eval_sup_on(sup: Matrix, d4: Matrix) -> Matrix:
            vec = [d4[i][j] for i in range(4) for j in range(4)]
            out_v = [
                sum((sup[row][col] * vec[col] for col in range(16)), ZERO)
                for row in range(16)
            ]
            return [[out_v[4 * i + j] for j in range(4)] for i in range(4)]

        # 1. Verify harmonic identity, complete-row Tr preservation on M_4(C),
        # and complete-row total-entry mass normalization on C_4 at EVERY reachable parent!
        for sz in range(4):
            for p in by_size[sz]:
                ideals = p.ideals()
                self.assertEqual(sum(q_part_a(p, s) for s in ideals), Fraction(1, 1))
                sum_rx = sum(q_part_a(p, s) * active_r_vec(p, s)[0] for s in ideals)
                sum_ry = sum(q_part_a(p, s) * active_r_vec(p, s)[1] for s in ideals)
                sum_rz = sum(q_part_a(p, s) * active_r_vec(p, s)[2] for s in ideals)
                self.assertEqual((sum_rx, sum_ry, sum_rz), (0, 0, 0))

                row_sup = zeros(16, 16)
                for s in ideals:
                    b_sup = get_branch_sup(p, s)
                    row_sup = mat_add(row_sup, mat_scale(2, b_sup))

                for r in range(4):
                    for c in range(4):
                        tr_coeff = sum(
                            (row_sup[4 * i + i][4 * r + c] for i in range(4)), ZERO
                        )
                        self.assertEqual(tr_coeff, ONE if r == c else ZERO)

                for d_in in test_c4_states:
                    d_sum = eval_sup_on(row_sup, d_in)
                    self.assertEqual(total_mass(d_sum), total_mass(d_in))

        # 2. Relabeling covariance check across all permutations of size-2 and size-3 parents:
        for sz in (2, 3):
            for p in by_size[sz][:4]:
                for perm in itertools.permutations(range(sz)):
                    p_rel = p.relabel(perm)
                    for s in p.ideals():
                        s_rel = frozenset(perm[v] for v in s)
                        self.assertEqual(get_branch_sup(p, s), get_branch_sup(p_rel, s_rel))

        # 3. Timelike causal-chain NONCOMMUTATIVITY:
        c1 = empty.append_birth(frozenset(), 0)
        sup_step1 = get_branch_sup(empty, frozenset())
        sup_step2 = get_branch_sup(c1, frozenset({0}))
        self.assertNotEqual(
            mat_mul(sup_step2, sup_step1), mat_mul(sup_step1, sup_step2)
        )

        # 4. All exact 16x16 superoperator causal diamonds across every labeled marked
        # poset of size |C| <= 2 (including non-canonical 1 < 0 relabelings:
        # 4 at |C|=0 + 32 at |C|=1 + (4*64 + 8*36) at |C|=2 = 580 diamonds):
        all_labeled_bases: list[Poset] = list(by_size[0]) + list(by_size[1])
        seen_sz2: set[tuple[int, frozenset[tuple[int, int]], tuple[int, ...]]] = set()
        for p2 in by_size[2]:
            for perm in ((0, 1), (1, 0)):
                pr = p2.relabel(perm)
                k2 = (pr.n, pr.lt, pr.marks)
                if k2 not in seen_sz2:
                    seen_sz2.add(k2)
                    all_labeled_bases.append(pr)
        self.assertEqual(len(all_labeled_bases), 15)

        diamond_count = 0
        for base in all_labeled_bases:
            ideals = base.ideals()
            for s in ideals:
                sup_x1 = get_branch_sup(base, s)
                for t_ideal in ideals:
                    sup_y1 = get_branch_sup(base, t_ideal)
                    rhs_by_c = [
                        mat_mul(get_branch_sup(base.append_birth(t_ideal, c_bit), s), sup_y1)
                        for c_bit in (0, 1)
                    ]
                    for b in (0, 1):
                        px = base.append_birth(s, b)
                        sup_x2 = get_branch_sup(px, t_ideal)
                        lhs = mat_mul(sup_x2, sup_x1)
                        for c_bit in (0, 1):
                            self.assertEqual(lhs, rhs_by_c[c_bit])
                            diamond_count += 1
        self.assertEqual(diamond_count, 580)

    def test_07_purely_imaginary_phase_drives_four_birth_causal_order(self) -> None:
        """Theorem 3B: Complete 4-birth enumeration proves Re-identical D_{+-Y} shift Z(E)."""
        # 1. Verify D_{+Y} and D_{-Y} have IDENTICAL real part (1/4) I_4, hence identical
        # initial weights mu(A) = |A|/4 on ALL 2^4 = 16 Boolean subsets A subseteq Omega_4!
        quarter_i4 = mat_scale(Fraction(1, 4), eye(4))
        for i in range(4):
            for j in range(4):
                self.assertEqual(G(D_PLUS_Y[i][j].re, 0), quarter_i4[i][j])
                self.assertEqual(G(D_MINUS_Y[i][j].re, 0), quarter_i4[i][j])
        self.assertNotEqual(D_PLUS_Y, D_MINUS_Y)
        for mask in range(16):
            subset = {i for i in range(4) if (mask >> i) & 1}
            w_plus = sesquilinear(D_PLUS_Y, subset, subset)
            w_minus = sesquilinear(D_MINUS_Y, subset, subset)
            self.assertEqual(w_plus, G(Fraction(len(subset), 4)))
            self.assertEqual(w_minus, G(Fraction(len(subset), 4)))

        # 2. Enumerate ALL 640 complete 4-birth marked histories as 16x16 superoperators!
        empty = Poset(0, frozenset(), ())
        sup_antichain = zeros(16, 16)
        sup_non_antichain = zeros(16, 16)
        history_count = 0
        unit_cache: dict[tuple[Fraction, Fraction, Fraction], Matrix] = {}

        def cached_step_sup(p: Poset, s: frozenset[int]) -> Matrix:
            rv = active_r_vec(p, s)
            if rv not in unit_cache:
                g_m = active_G_matrix(rv)
                unit_cache[rv] = superop_16x16(
                    lambda d4, g_m=g_m: mat_add(
                        mat_scale(ACTIVE_T, mat_mul(WP4, mat_mul(d4, mat_dag(WP4)))),
                        mat_scale(
                            mat_trace(mat_mul(g_m, d4)) * G.coerce(Fraction(1, 4)),
                            eye(4),
                        ),
                    )
                )
            return mat_scale(q_part_a(p, s) * Fraction(1, 2), unit_cache[rv])

        def dfs(p: Poset, acc_sup: Matrix) -> None:
            nonlocal sup_antichain, sup_non_antichain, history_count
            if p.n == 4:
                history_count += 1
                if p.is_antichain():
                    sup_antichain = mat_add(sup_antichain, acc_sup)
                else:
                    sup_non_antichain = mat_add(sup_non_antichain, acc_sup)
                return
            for s in p.ideals():
                nxt_sup = mat_mul(cached_step_sup(p, s), acc_sup)
                for bit in (0, 1):
                    dfs(p.append_birth(s, bit), nxt_sup)

        dfs(empty, eye(16))
        self.assertEqual(history_count, 640)

        def eval_sup(sup: Matrix, d4: Matrix) -> Matrix:
            vec = [d4[i][j] for i in range(4) for j in range(4)]
            out_vec = [
                sum((sup[row][col] * vec[col] for col in range(16)), ZERO)
                for row in range(16)
            ]
            return [[out_vec[4 * i + j] for j in range(4)] for i in range(4)]

        # Evaluate exact endpoint probabilities on D_{+-Y}, D_{+-X}, D_{+-Z}:
        p_plus_y_z1 = total_mass(eval_sup(sup_antichain, D_PLUS_Y))
        p_plus_y_z0 = total_mass(eval_sup(sup_non_antichain, D_PLUS_Y))
        p_minus_y_z1 = total_mass(eval_sup(sup_antichain, D_MINUS_Y))
        p_minus_y_z0 = total_mass(eval_sup(sup_non_antichain, D_MINUS_Y))

        self.assertEqual(p_plus_y_z1, G(Fraction(8711, 2230272)))
        self.assertEqual(p_plus_y_z0, G(Fraction(2221561, 2230272)))
        self.assertEqual(p_plus_y_z0 + p_plus_y_z1, ONE)
        self.assertEqual(p_minus_y_z1, G(Fraction(8185, 2230272)))
        self.assertEqual(p_minus_y_z0, G(Fraction(2222087, 2230272)))
        self.assertEqual(p_minus_y_z0 + p_minus_y_z1, ONE)

        delta_star = Fraction(263, 1115136)
        self.assertEqual(p_plus_y_z1 - p_minus_y_z1, G(delta_star))

        # Orthogonal Bloch axes X and Z have exact ZERO contrast!
        self.assertEqual(
            total_mass(eval_sup(sup_antichain, D_PLUS_X)),
            total_mass(eval_sup(sup_antichain, D_MINUS_X)),
        )
        self.assertEqual(
            total_mass(eval_sup(sup_antichain, D_PLUS_Z)),
            total_mass(eval_sup(sup_antichain, D_MINUS_Z)),
        )

        # Pre-trial quarter-phase pulses S_P^k (k = 0, 1, 2, 3) rotate contrast
        # cyclic-quadrature-wise on D_{+-X} = S_H(D_{+-Z}) and D_{+-Y}:
        cur_px, cur_mx = D_PLUS_X, D_MINUS_X
        cur_py, cur_my = D_PLUS_Y, D_MINUS_Y
        expected_x_cycle = [Fraction(0), delta_star, Fraction(0), -delta_star]
        expected_y_cycle = [delta_star, Fraction(0), -delta_star, Fraction(0)]
        for step in range(4):
            cx = (
                total_mass(eval_sup(sup_antichain, cur_px))
                - total_mass(eval_sup(sup_antichain, cur_mx))
            )
            cy = (
                total_mass(eval_sup(sup_antichain, cur_py))
                - total_mass(eval_sup(sup_antichain, cur_my))
            )
            self.assertEqual(cx, G(expected_x_cycle[step]))
            self.assertEqual(cy, G(expected_y_cycle[step]))
            cur_px, cur_mx = apply_SP(cur_px), apply_SP(cur_mx)
            cur_py, cur_my = apply_SP(cur_py), apply_SP(cur_my)

        # 3. Required d=4 classical cyclic-simplex comparator (Delta_4, C_4) on mixed states:
        # Genuinely mixed states in Delta_4 (each supported on 3 vertices) rotated by C_4:
        a0 = ACTIVE_A[0]
        vis = ACTIVE_THETA * a0 * (1 - a0)
        e_z1_mix = [a0, a0 + 2 * vis, a0, a0 - 2 * vis]
        self.assertTrue(all(Fraction(0) < val < Fraction(1) for val in e_z1_mix))

        c_px = [Fraction(1, 2), Fraction(1, 4), Fraction(0), Fraction(1, 4)]
        c_mx = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]
        c_py = [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4), Fraction(0)]
        c_my = [Fraction(1, 4), Fraction(0), Fraction(1, 4), Fraction(1, 2)]

        def c4_shift(vec: list[Fraction]) -> list[Fraction]:
            return [vec[3], vec[0], vec[1], vec[2]]

        def dot4(a_v: list[Fraction], b_v: list[Fraction]) -> Fraction:
            return sum((x * y for x, y in zip(a_v, b_v)), Fraction(0))

        self.assertEqual(c4_shift(c_px), c_py)
        self.assertEqual(c4_shift(c_mx), c_my)
        self.assertEqual(dot4(e_z1_mix, c_py), Fraction(8711, 2230272))
        self.assertEqual(dot4(e_z1_mix, c_my), Fraction(8185, 2230272))
        self.assertEqual(dot4(e_z1_mix, c_px), a0)
        self.assertEqual(dot4(e_z1_mix, c_mx), a0)

        for step in range(4):
            self.assertEqual(
                dot4(e_z1_mix, c_px) - dot4(e_z1_mix, c_mx), expected_x_cycle[step]
            )
            self.assertEqual(
                dot4(e_z1_mix, c_py) - dot4(e_z1_mix, c_my), expected_y_cycle[step]
            )
            c_px, c_mx = c4_shift(c_px), c4_shift(c_mx)
            c_py, c_my = c4_shift(c_py), c4_shift(c_my)


if __name__ == "__main__":
    unittest.main()
