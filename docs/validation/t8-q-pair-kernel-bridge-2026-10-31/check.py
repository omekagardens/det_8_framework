"""Exact standard-library witnesses for the upstream pair-kernel bridge.

Standard library only (fractions, itertools, unittest). Zero floating-point
arithmetic, external packages, or imports from existing DET/RET executors are
used. Universal statements rest on the proofs in BRIDGE_THEOREM.md; these eight
exact tests verify the linear-algebraic classifications, witness identities,
and countermodels in normal and -O modes.
"""

from __future__ import annotations

import itertools
import unittest
from fractions import Fraction

F = Fraction
ZERO_F = F(0)


def rational(value: int | F) -> F:
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise TypeError("Expected exact int or Fraction")
    return F(value)


class G:
    """Exact Gaussian rational a + b*i with a, b in Q."""

    __slots__ = ("real", "imag")
    real: F
    imag: F

    def __init__(self, real: int | F = ZERO_F, imag: int | F = ZERO_F) -> None:
        object.__setattr__(self, "real", rational(real))
        object.__setattr__(self, "imag", rational(imag))

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError("G is immutable")

    @classmethod
    def _raw(cls, real: F, imag: F) -> G:
        obj = object.__new__(cls)
        object.__setattr__(obj, "real", real)
        object.__setattr__(obj, "imag", imag)
        return obj

    def __repr__(self) -> str:
        return f"G({self.real!r}, {self.imag!r})"

    def __add__(self, other: G | int | F) -> G:
        other = g(other)
        return G._raw(self.real + other.real, self.imag + other.imag)

    __radd__ = __add__

    def __neg__(self) -> G:
        return G._raw(-self.real, -self.imag)

    def __sub__(self, other: G | int | F) -> G:
        other = g(other)
        return G._raw(self.real - other.real, self.imag - other.imag)

    def __rsub__(self, other: G | int | F) -> G:
        other = g(other)
        return G._raw(other.real - self.real, other.imag - self.imag)

    def __mul__(self, other: G | int | F) -> G:
        other = g(other)
        return G._raw(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: G | int | F) -> G:
        other = g(other)
        norm = other.norm_sq()
        if norm == 0:
            raise ZeroDivisionError("Gaussian division by zero")
        num = self * other.conj()
        return G._raw(num.real / norm, num.imag / norm)

    def __rtruediv__(self, other: G | int | F) -> G:
        return g(other) / self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, G):
            return self.real == other.real and self.imag == other.imag
        if not isinstance(other, bool) and isinstance(other, (int, F)):
            return self.imag == 0 and self.real == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.real) if self.imag == 0 else hash((self.real, self.imag))

    def conj(self) -> G:
        return G._raw(self.real, -self.imag)

    def norm_sq(self) -> F:
        return self.real * self.real + self.imag * self.imag


I_UNIT = G(0, 1)


def g(value: G | int | F) -> G:
    return value if isinstance(value, G) else G(rational(value))


Matrix = list[list[G]]
RealMatrix = list[list[F]]


def gmat(rows: list[list[G | int | F]]) -> Matrix:
    return [[g(v) for v in row] for row in rows]


def rmat(rows: list[list[int | F]]) -> RealMatrix:
    return [[rational(v) for v in row] for row in rows]


def mat_add(a: Matrix, b: Matrix) -> Matrix:
    if len(a) != len(b):
        raise ValueError("Row dimension mismatch")
    return [
        [x + y for x, y in zip(ra, rb)]
        for ra, rb in zip(a, b)
    ]


def mat_sub(a: Matrix, b: Matrix) -> Matrix:
    return mat_add(a, mat_scale(-1, b))


def mat_scale(scalar: G | int | F, a: Matrix) -> Matrix:
    s = g(scalar)
    return [[s * entry for entry in row] for row in a]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    m, k, n = len(a), len(b), len(b[0])
    if any(len(row) != k for row in a):
        raise ValueError("Incompatible matrix shapes")
    return [
        [sum((a[r][c] * b[c][col] for c in range(k)), G()) for col in range(n)]
        for r in range(m)
    ]


def mat_dagger(a: Matrix) -> Matrix:
    m, n = len(a), len(a[0])
    return [[a[r][c].conj() for r in range(m)] for c in range(n)]


def mat_transpose(a: Matrix) -> Matrix:
    m, n = len(a), len(a[0])
    return [[a[r][c] for r in range(m)] for c in range(n)]


def mat_kron(a: Matrix, b: Matrix) -> Matrix:
    r1, c1 = len(a), len(a[0])
    r2, c2 = len(b), len(b[0])
    return [
        [a[i1][j1] * b[i2][j2] for j1 in range(c1) for j2 in range(c2)]
        for i1 in range(r1)
        for i2 in range(r2)
    ]


def mat_apply(a: Matrix, vec: list[G]) -> list[G]:
    return [sum((entry * v for entry, v in zip(row, vec)), G()) for row in a]


def congruence(u: Matrix, d: Matrix, divisor: int | F = 1) -> Matrix:
    return mat_scale(F(1) / rational(divisor), mat_mul(mat_mul(u, d), mat_dagger(u)))


def is_hermitian(d: Matrix) -> bool:
    return d == mat_dagger(d)


def total_mass(d: Matrix) -> G:
    return sum((sum(row, G()) for row in d), G())


def trace(d: Matrix) -> G:
    return sum((d[i][i] for i in range(len(d))), G())


def pair_val(d: Matrix, a_set: set[int] | frozenset[int], b_set: set[int] | frozenset[int]) -> G:
    return sum((d[i][j] for i in a_set for j in b_set), G())


def mu_val(d: Matrix, a_set: set[int] | frozenset[int]) -> F:
    val = pair_val(d, a_set, a_set)
    if val.imag != 0:
        raise ValueError("Hermitian diagonal event weight must be real")
    return val.real


def split_real_imag(d: Matrix) -> tuple[Matrix, Matrix]:
    """Return (R, J) as Gaussian matrices with zero imag parts, where D = R + i J."""
    if not is_hermitian(d):
        raise ValueError("Expected Hermitian matrix")
    r_part = [[G(entry.real, 0) for entry in row] for row in d]
    j_part = [[G(entry.imag, 0) for entry in row] for row in d]
    return r_part, j_part


def compose_alpha(d: Matrix, e: Matrix, alpha: int | F) -> Matrix:
    """Classified 1-parameter product: R x S + alpha*(J x K) + i*(J x S + R x K)."""
    r_mat, j_mat = split_real_imag(d)
    s_mat, k_mat = split_real_imag(e)
    real_part = mat_add(mat_kron(r_mat, s_mat), mat_scale(rational(alpha), mat_kron(j_mat, k_mat)))
    imag_part = mat_add(mat_kron(j_mat, s_mat), mat_kron(r_mat, k_mat))
    return mat_add(real_part, mat_scale(I_UNIT, imag_part))


def exact_det(mat: Matrix) -> G:
    """Exact Gaussian-elimination determinant over Q(i) (independent of Leibniz sum)."""
    n = len(mat)
    if n == 0:
        return G(1)
    work = [[entry for entry in row] for row in mat]
    sign = 1
    det = G(1)
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if work[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            return G(0)
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            sign = -sign
        piv_val = work[col][col]
        det = det * piv_val
        for row in range(col + 1, n):
            if work[row][col] != 0:
                factor = work[row][col] / piv_val
                for k in range(col, n):
                    work[row][k] = work[row][k] - factor * work[col][k]
    return G(sign) * det


def rational_rref_nullity(rows: list[list[F]], num_cols: int) -> tuple[int, list[list[F]]]:
    """Return (rank, nullspace_basis) of a rational matrix over Q."""
    work = [list(r) for r in rows]
    m = len(work)
    pivot_cols: list[int] = []
    r_idx = 0
    for c_idx in range(num_cols):
        if r_idx >= m:
            break
        piv = None
        for cand in range(r_idx, m):
            if work[cand][c_idx] != 0:
                piv = cand
                break
        if piv is None:
            continue
        work[r_idx], work[piv] = work[piv], work[r_idx]
        inv = F(1) / work[r_idx][c_idx]
        work[r_idx] = [val * inv for val in work[r_idx]]
        for other in range(m):
            if other != r_idx and work[other][c_idx] != 0:
                fac = work[other][c_idx]
                work[other] = [
                    work[other][k] - fac * work[r_idx][k] for k in range(num_cols)
                ]
        pivot_cols.append(c_idx)
        r_idx += 1

    piv_set = set(pivot_cols)
    free_cols = [c for c in range(num_cols) if c not in piv_set]
    basis: list[list[F]] = []
    for free_c in free_cols:
        vec = [ZERO_F] * num_cols
        vec[free_c] = F(1)
        for row_i, piv_c in enumerate(pivot_cols):
            vec[piv_c] = -work[row_i][free_c]
        basis.append(vec)
    return len(pivot_cols), basis


# -- Reference RI-08b four-label lifted qubit objects -------------------------

Z2 = gmat([[1, 0], [0, -1]])
I2 = gmat([[1, 0], [0, 1]])
H0 = gmat([[1, 1], [1, -1]])  # H = H0 / sqrt(2), so congruence divides by 2
P2 = gmat([[1, 0], [0, I_UNIT]])


def lift_4(u2: Matrix) -> Matrix:
    """RI-08b block-twisted 4-atom lift W_U = diag(U, Z U Z)."""
    zuz = mat_mul(mat_mul(Z2, u2), Z2)
    return [
        [u2[0][0], u2[0][1], G(0), G(0)],
        [u2[1][0], u2[1][1], G(0), G(0)],
        [G(0), G(0), zuz[0][0], zuz[0][1]],
        [G(0), G(0), zuz[1][0], zuz[1][1]],
    ]


W_I = lift_4(I2)
W_Z = lift_4(Z2)
W_H0 = lift_4(H0)
W_P = lift_4(P2)

CELL_0 = frozenset({0, 1})
CELL_1 = frozenset({2, 3})


class PairKernelBridgeWitnesses(unittest.TestCase):
    def test_01_real_incidence_naturality_classifies_one_parameter_family(self) -> None:
        # Herm_2(C) real basis (dim 4): E00, E11, S01 = E01+E10, A01 = i(E01-E10).
        h2_basis = [
            gmat([[1, 0], [0, 0]]),
            gmat([[0, 0], [0, 1]]),
            gmat([[0, 1], [1, 0]]),
            gmat([[0, I_UNIT], [-I_UNIT, 0]]),
        ]
        # Herm_4(C) real basis (dim 16): 4 diagonals, 6 real sym pairs, 6 imag skew pairs.
        h4_basis: list[Matrix] = []
        for idx in range(4):
            m = [[G(0) for _ in range(4)] for _ in range(4)]
            m[idx][idx] = G(1)
            h4_basis.append(m)
        for p in range(4):
            for q in range(p + 1, 4):
                ms = [[G(0) for _ in range(4)] for _ in range(4)]
                ms[p][q] = G(1)
                ms[q][p] = G(1)
                h4_basis.append(ms)
                ma = [[G(0) for _ in range(4)] for _ in range(4)]
                ma[p][q] = I_UNIT
                ma[q][p] = -I_UNIT
                h4_basis.append(ma)
        self.assertEqual(len(h4_basis), 16)

        def h2_coords(mat: Matrix) -> list[F]:
            return [
                mat[0][0].real,
                mat[1][1].real,
                mat[0][1].real,
                mat[0][1].imag,
            ]

        def h4_coords(mat: Matrix) -> list[F]:
            out = [mat[idx][idx].real for idx in range(4)]
            for p in range(4):
                for q in range(p + 1, 4):
                    out.append(mat[p][q].real)
                    out.append(mat[p][q].imag)
            return out

        # Unknown real-bilinear map B: Herm_2 x Herm_2 -> Herm_4 has 4*4*16 = 256 coords.
        # Homogeneous equations on delta_B = B - B_{alpha=0}:
        # 1) Unit + real-incidence naturality fixes B on (R, S), (R, iK), (iJ, S) to 0 in delta_B:
        #    (u [1] u^T) (x) (v [1] v^T) and (U Omega_2 U^T) (x) (v [1] v^T).
        eq_rows: list[list[F]] = []
        for a_idx in range(4):
            for b_idx in range(4):
                if (a_idx, b_idx) == (3, 3):
                    continue
                # Unit + rectangular naturality from 1x1 and 2x1/1x2 embeddings
                # fixes all non-(3,3) pairs.
                for out_k in range(16):
                    row = [ZERO_F] * 256
                    row[(a_idx * 4 + b_idx) * 16 + out_k] = F(1)
                    eq_rows.append(row)

        # 2) On Herm_2 x Herm_2 itself, enforce 2x2 real-incidence naturality
        #    (U D U^T) (.) (V E V^T) = (U x V)(D (.) E)(U x V)^T for finite rational generators.
        real_gens = [
            gmat([[2, 0], [0, 1]]),
            gmat([[1, 1], [0, 1]]),
            gmat([[0, 1], [1, 0]]),
            gmat([[1, 0], [0, -1]]),
        ]
        pairs_uv = [(u, I2) for u in real_gens] + [(I2, v) for v in real_gens] + [
            (real_gens[2], real_gens[2])
        ]
        for u_mat, v_mat in pairs_uv:
            uv = mat_kron(u_mat, v_mat)
            uv_t = mat_transpose(uv)
            for a_idx, d_mat in enumerate(h2_basis):
                ud = mat_mul(mat_mul(u_mat, d_mat), mat_transpose(u_mat))
                c_ud = h2_coords(ud)
                for b_idx, e_mat in enumerate(h2_basis):
                    ve = mat_mul(mat_mul(v_mat, e_mat), mat_transpose(v_mat))
                    c_ve = h2_coords(ve)
                    # Precompute action of (U x V)(.)(U x V)^T on h4_basis.
                    mapped_h4 = [
                        h4_coords(mat_mul(mat_mul(uv, h4_b), uv_t)) for h4_b in h4_basis
                    ]
                    for out_k in range(16):
                        row = [ZERO_F] * 256
                        # LHS: sum_{p,q} c_ud[p] * c_ve[q] * B[p,q,out_k]
                        for p in range(4):
                            for q in range(4):
                                coeff = c_ud[p] * c_ve[q]
                                if coeff != 0:
                                    row[(p * 4 + q) * 16 + out_k] += coeff
                        # RHS: sum_m mapped_h4[m][out_k] * B[a_idx,b_idx,m]
                        for m_idx in range(16):
                            coeff_r = mapped_h4[m_idx][out_k]
                            if coeff_r != 0:
                                row[(a_idx * 4 + b_idx) * 16 + m_idx] -= coeff_r
                        if any(v != 0 for v in row):
                            eq_rows.append(row)

        rank, null_basis = rational_rref_nullity(eq_rows, 256)
        self.assertEqual(rank, 255)
        self.assertEqual(len(null_basis), 1)

        # Verify the unique surviving null vector is exactly proportional to J (x) K.
        omega_kron = compose_alpha(h2_basis[3], h2_basis[3], alpha=1)
        expected_vec = [ZERO_F] * 256
        for out_k, val in enumerate(h4_coords(omega_kron)):
            expected_vec[(3 * 4 + 3) * 16 + out_k] = val
        lone = null_basis[0]
        nonzero_indices = [idx for idx, val in enumerate(expected_vec) if val != 0]
        ratio = lone[nonzero_indices[0]] / expected_vec[nonzero_indices[0]]
        self.assertNotEqual(ratio, ZERO_F)
        self.assertEqual(lone, [ratio * v for v in expected_vec])

        # Verify associativity, swap covariance, unit, and complex marginals across alpha.
        d1 = gmat([[F(1, 3), G(F(1, 6), F(1, 5))], [G(F(1, 6), F(-1, 5)), F(1, 3)]])
        d2 = gmat([[F(1, 4), G(F(-1, 8), F(3, 10))], [G(F(-1, 8), F(-3, 10)), F(1, 2)]])
        d3 = gmat([[F(2, 5), G(F(1, 10), F(-1, 7))], [G(F(1, 10), F(1, 7)), F(2, 5)]])
        unit_1 = gmat([[1]])
        swap_2 = gmat([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
        for alpha in (F(-2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(2)):
            lhs = compose_alpha(compose_alpha(d1, d2, alpha), d3, alpha)
            rhs = compose_alpha(d1, compose_alpha(d2, d3, alpha), alpha)
            self.assertEqual(lhs, rhs)
            self.assertEqual(compose_alpha(unit_1, d1, alpha), d1)
            self.assertEqual(compose_alpha(d1, unit_1, alpha), d1)
            swapped = congruence(swap_2, compose_alpha(d1, d2, alpha))
            self.assertEqual(swapped, compose_alpha(d2, d1, alpha))
            comp12 = compose_alpha(d1, d2, alpha)
            marg_1 = [
                [
                    sum((comp12[2 * i + a][2 * j + b] for a in range(2) for b in range(2)), G())
                    for j in range(2)
                ]
                for i in range(2)
            ]
            self.assertEqual(marg_1, mat_scale(total_mass(d2), d1))

    def test_02_psd_weak_positivity_interval_and_eigenvalues_across_alpha(self) -> None:
        q_proj = gmat([[F(1, 2), G(0, F(1, 2))], [G(0, F(-1, 2)), F(1, 2)]])
        self.assertEqual(total_mass(q_proj), G(1))
        e_eq = {0, 3}
        e_diff = {1, 2}
        v1 = [G(1), G(0, -1), G(0, -1), G(-1)]
        v2 = [G(1), G(0, 1), G(0, 1), G(-1)]
        v3 = [G(1), G(0), G(0), G(1)]
        v4 = [G(0), G(1), G(-1), G(0)]

        for alpha in (F(-2), F(-3, 2), F(-1), F(-1, 2), F(0), F(1, 2), F(1), F(3, 2)):
            qq = compose_alpha(q_proj, q_proj, alpha)
            self.assertEqual(mu_val(qq, e_eq), F(1 + alpha, 2))
            self.assertEqual(mu_val(qq, e_diff), F(1 - alpha, 2))
            for vec, eig in (
                (v1, F(3 - alpha, 4)),
                (v2, F(-(1 + alpha), 4)),
                (v3, F(1 + alpha, 4)),
                (v4, F(1 + alpha, 4)),
            ):
                self.assertEqual(mat_apply(qq, vec), [g(eig) * c for c in vec])
            if alpha < -1:
                self.assertLess(mu_val(qq, e_eq), 0)
            elif alpha > 1:
                self.assertLess(mu_val(qq, e_diff), 0)
            else:
                # Convex decomposition of Re(D (.)_alpha E) for alpha in [-1, 1].
                q_conj = [[entry.conj() for entry in row] for row in q_proj]
                re_alpha, _ = split_real_imag(qq)
                re_minus, _ = split_real_imag(compose_alpha(q_proj, q_proj, -1))
                re_plus, _ = split_real_imag(compose_alpha(q_proj, q_conj, -1))
                rhs = mat_add(
                    mat_scale(F(1 - alpha, 2), re_minus),
                    mat_scale(F(1 + alpha, 2), re_plus),
                )
                self.assertEqual(re_alpha, rhs)
                for mask in range(1 << 4):
                    subset = {i for i in range(4) if (mask >> i) & 1}
                    self.assertGreaterEqual(mu_val(qq, subset), 0)

    def test_03_silent_control_interchange_uniquely_selects_ordinary_tensor_law(self) -> None:
        d_plus_z = gmat(
            [
                [F(1, 2), 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, F(1, 2), 0],
                [0, 0, 0, 0],
            ]
        )
        d_plus_x = congruence(W_H0, d_plus_z, divisor=2)
        d_plus_y = congruence(W_P, d_plus_x)
        d_minus_x = congruence(W_P, d_plus_y)

        for state in (d_plus_z, d_plus_x, d_plus_y, d_minus_x):
            self.assertTrue(is_hermitian(state))
            self.assertEqual(total_mass(state), G(1))
            self.assertEqual(trace(state), G(1))
            self.assertEqual(pair_val(state, CELL_0, CELL_1), G(0))

        # D_{+X} is purely real; single-system S_P^2 sends cell weights (1, 0) -> (0, 1).
        _, j_plus_x = split_real_imag(d_plus_x)
        self.assertEqual(j_plus_x, gmat([[0] * 4 for _ in range(4)]))
        self.assertEqual([mu_val(d_plus_x, CELL_0), mu_val(d_plus_x, CELL_1)], [F(1), F(0)])
        self.assertEqual([mu_val(d_plus_y, CELL_0), mu_val(d_plus_y, CELL_1)], [F(1, 2), F(1, 2)])
        self.assertEqual([mu_val(d_minus_x, CELL_0), mu_val(d_minus_x, CELL_1)], [F(0), F(1)])

        wp_wp = mat_kron(W_P, W_P)
        prod_cells = [
            (CELL_0, CELL_0),
            (CELL_0, CELL_1),
            (CELL_1, CELL_0),
            (CELL_1, CELL_1),
        ]
        prod_sets = [
            frozenset(4 * i + j for i in ca for j in cb) for ca, cb in prod_cells
        ]

        for alpha in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            # Path 1: compose D_{+X} first, then apply local silent S_P x S_P.
            path_1 = congruence(wp_wp, compose_alpha(d_plus_x, d_plus_x, alpha))
            # Path 2: apply silent S_P locally first, then compose D_{+Y} (.)_alpha D_{+Y}.
            path_2 = compose_alpha(d_plus_y, d_plus_y, alpha)

            self.assertEqual(path_1[0][5], G(F(-1, 16), 0))  # index (0,0) to (1,1)
            self.assertEqual(path_2[0][5], G(alpha * F(1, 16), 0))
            if alpha == -1:
                self.assertEqual(path_1, path_2)
            else:
                self.assertNotEqual(path_1, path_2)

            # Apply second local S_P x S_P to Path 2 and read local product cells.
            after_second_sp = congruence(wp_wp, path_2)
            self.assertEqual(total_mass(after_second_sp), G(1))
            for idx_a in range(4):
                for idx_b in range(4):
                    if idx_a != idx_b:
                        self.assertEqual(
                            pair_val(after_second_sp, prod_sets[idx_a], prod_sets[idx_b]), G(0)
                        )
            weights = [mu_val(after_second_sp, cell_set) for cell_set in prod_sets]
            expected = [
                F(-(1 + alpha), 4),
                F(1 + alpha, 4),
                F(1 + alpha, 4),
                F(3 - alpha, 4),
            ]
            self.assertEqual(weights, expected)
            if alpha == 0:
                # RI-22's star product yields negative cell probability -1/4!
                self.assertEqual(weights[0], F(-1, 4))

    def test_04_deletion_of_phase_control_leaves_ri22_and_interval_unexcluded(self) -> None:
        # Close the real silent-control group generated by S_H and S_Z on 2x2 and 4x4.
        # Signed matrices <Z, H> subset O(2) form D_8 of order 16; congruence S_U = W_U(.)W_U^T
        # quotients +-I_2 to 8 distinct real silent actions (matching RI-08b's "8 without P").
        gens_2 = [(F(1), Z2), (F(2), H0)]
        signed_matrices: dict[tuple[F, tuple[tuple[F, ...], ...]], tuple[F, Matrix]] = {}
        congruence_actions: dict[tuple[F, ...], tuple[F, Matrix]] = {}
        probe_e00 = gmat([[1, 0], [0, 0]])
        probe_s01 = gmat([[0, 1], [1, 0]])
        queue: list[tuple[F, Matrix]] = [(F(1), I2)]
        while queue:
            div_a, mat_a = queue.pop()
            key = (div_a, tuple(tuple(e.real for e in row) for row in mat_a))
            if key in signed_matrices:
                continue
            signed_matrices[key] = (div_a, mat_a)
            act_sig = tuple(
                x.real
                for row in (
                    congruence(mat_a, probe_e00, divisor=div_a)
                    + congruence(mat_a, probe_s01, divisor=div_a)
                )
                for x in row
            )
            congruence_actions.setdefault(act_sig, (div_a, mat_a))
            for div_g, mat_g in gens_2:
                nd = div_a * div_g
                nm = mat_mul(mat_g, mat_a)
                if nd == 4:
                    nd = F(1)
                    nm = mat_scale(F(1, 2), nm)
                queue.append((nd, nm))

        self.assertEqual(len(signed_matrices), 16)
        self.assertEqual(len(congruence_actions), 8)

        # Test complex PSD states across all 64 pairs of real silent controls and alphas in [-1, 1].
        d_a = congruence(
            W_P,
            congruence(
                W_H0,
                gmat([[F(1, 2), 0, 0, 0], [0, 0, 0, 0], [0, 0, F(1, 2), 0], [0, 0, 0, 0]]),
                divisor=2,
            ),
        )
        d_b = gmat(
            [
                [F(3, 8), G(F(1, 16), F(1, 8)), 0, 0],
                [G(F(1, 16), F(-1, 8)), F(1, 8), 0, 0],
                [0, 0, F(3, 8), G(F(-1, 16), F(-1, 8))],
                [0, 0, G(F(-1, 16), F(1, 8)), F(1, 8)],
            ]
        )
        for alpha in (F(-1), F(0), F(1)):
            base_comp = compose_alpha(d_a, d_b, alpha)
            for (div1, u1), (div2, u2) in itertools.product(
                congruence_actions.values(), repeat=2
            ):
                w1, w2 = lift_4(u1), lift_4(u2)
                lhs = congruence(mat_kron(w1, w2), base_comp, divisor=div1 * div2)
                rhs = compose_alpha(
                    congruence(w1, d_a, divisor=div1),
                    congruence(w2, d_b, divisor=div2),
                    alpha,
                )
                self.assertEqual(lhs, rhs)

    def test_05_composite_record_grouping_forces_exact_decoherence_iff_alpha_nonzero(self) -> None:
        # Strictly positive-definite 2-atom kernel with purely imaginary cross-relation t = 1/4.
        t_val = F(1, 4)
        d_imag = gmat([[F(1, 2), G(0, t_val)], [G(0, -t_val), F(1, 2)]])
        self.assertTrue(is_hermitian(d_imag))
        self.assertEqual(total_mass(d_imag), G(1))
        self.assertEqual(exact_det(d_imag), G(F(3, 16)))  # det = 1/4 - 1/16 = 3/16 > 0, so D > 0!
        self.assertEqual(mu_val(d_imag, {0}) + mu_val(d_imag, {1}), mu_val(d_imag, {0, 1}))
        self.assertEqual(pair_val(d_imag, {0}, {1}), G(0, t_val))

        c_same = {0, 3}  # (0,0) u (1,1)
        c_diff = {1, 2}  # (0,1) u (1,0)
        for alpha in (F(-1), F(-1, 2), F(0), F(1, 2), F(1)):
            dd = compose_alpha(d_imag, d_imag, alpha)
            discrepancy_same = mu_val(dd, c_same) - (mu_val(dd, {0}) + mu_val(dd, {3}))
            discrepancy_diff = mu_val(dd, c_diff) - (mu_val(dd, {1}) + mu_val(dd, {2}))
            self.assertEqual(discrepancy_same, 2 * alpha * t_val * t_val)
            self.assertEqual(discrepancy_diff, -2 * alpha * t_val * t_val)

        # Under RI-22's star product (alpha = 0), ALL 2^4 two-copy and 2^8 three-copy groupings add!
        dd_star = compose_alpha(d_imag, d_imag, 0)
        ddd_star = compose_alpha(dd_star, d_imag, 0)
        for mask in range(1 << 4):
            grp = {i for i in range(4) if (mask >> i) & 1}
            self.assertEqual(mu_val(dd_star, grp), sum((mu_val(dd_star, {i}) for i in grp), ZERO_F))
        for mask in range(1 << 8):
            grp = {i for i in range(8) if (mask >> i) & 1}
            self.assertEqual(
                mu_val(ddd_star, grp), sum((mu_val(ddd_star, {i}) for i in grp), ZERO_F)
            )

        # Boundary with RI-08d: zero-sum internal cross-block c*Z already has D(A_0, A_1) = 0
        # and therefore passes all uncoupled two-copy product-record groupings even at alpha = -1.
        c_internal = G(0, F(1, 8))
        d_c_nonzero = gmat(
            [
                [F(1, 4), 0, c_internal, 0],
                [0, F(1, 4), 0, -c_internal],
                [c_internal.conj(), 0, F(1, 4), 0],
                [0, -c_internal.conj(), 0, F(1, 4)],
            ]
        )
        self.assertEqual(total_mass(d_c_nonzero), G(1))
        self.assertEqual(pair_val(d_c_nonzero, CELL_0, CELL_1), G(0))
        d_c_sq = compose_alpha(d_c_nonzero, d_c_nonzero, -1)
        prod_cells = [
            frozenset(4 * i + j for i in ca for j in cb)
            for ca in (CELL_0, CELL_1)
            for cb in (CELL_0, CELL_1)
        ]
        for mask in range(1 << 4):
            union_cell: frozenset[int] = frozenset().union(
                *(prod_cells[k] for k in range(4) if (mask >> k) & 1)
            )
            self.assertEqual(
                mu_val(d_c_sq, union_cell),
                sum(
                    (mu_val(d_c_sq, prod_cells[k]) for k in range(4) if (mask >> k) & 1),
                    ZERO_F,
                ),
            )

    def test_06_classical_diagonal_plus_silent_hadamard_replaces_ri21_seed(self) -> None:
        d_plus_z = gmat(
            [
                [F(1, 2), 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, F(1, 2), 0],
                [0, 0, 0, 0],
            ]
        )
        seed_dx = congruence(W_H0, d_plus_z, divisor=2)
        self.assertEqual(total_mass(seed_dx), G(1))
        self.assertEqual(trace(seed_dx), G(1))
        self.assertEqual(pair_val(seed_dx, CELL_0, CELL_1), G(0))

        # All seven RI-21 benchmark candidates: (name, matrix, expected_psd).
        candidates: list[tuple[str, Matrix, bool]] = [
            (
                "D3=(J3-I3)/6",
                gmat([[0, F(1, 6), F(1, 6)], [F(1, 6), 0, F(1, 6)], [F(1, 6), F(1, 6), 0]]),
                False,
            ),
            (
                "diag(1/2,1/3,1/6)",
                gmat([[F(1, 2), 0, 0], [0, F(1, 3), 0], [0, 0, F(1, 6)]]),
                True,
            ),
            (
                "H_3rd_order",
                gmat(
                    [
                        [F(1, 5), F(1, 5), F(1, 5)],
                        [F(1, 5), F(1, 5), F(-1, 5)],
                        [F(1, 5), F(-1, 5), F(1, 5)],
                    ]
                ),
                False,
            ),
            (
                "Di_complex",
                gmat([[F(1, 2), I_UNIT], [-I_UNIT, F(1, 2)]]),
                False,
            ),
            (
                "J3/9_singular",
                gmat([[F(1, 9)] * 3 for _ in range(3)]),
                True,
            ),
            (
                "0_direct_sum_D3",
                gmat(
                    [
                        [0, 0, 0, 0],
                        [0, 0, F(1, 6), F(1, 6)],
                        [0, F(1, 6), 0, F(1, 6)],
                        [0, F(1, 6), F(1, 6), 0],
                    ]
                ),
                False,
            ),
            ("n=1_unit", gmat([[1]]), True),
        ]

        def perm_parity(perm: tuple[int, ...]) -> int:
            inv = sum(
                1
                for idx_a in range(len(perm))
                for idx_b in range(idx_a + 1, len(perm))
                if perm[idx_a] > perm[idx_b]
            )
            return inv % 2

        def factorial(k: int) -> int:
            out = 1
            for val in range(2, k + 1):
                out *= val
            return out

        for name, cand, expected_psd in candidates:
            n = len(cand)
            self.assertTrue(is_hermitian(cand), name)
            self.assertEqual(total_mass(cand), G(1), name)
            # Verify local weak Boolean positivity on all 2^n base events.
            for mask in range(1 << n):
                ev = {idx for idx in range(n) if (mask >> idx) & 1}
                self.assertGreaterEqual(mu_val(cand, ev), 0, name)

            # Build padded composite C_n(D) = D^(x n) (x) D_{+X} of size 4 * n^n.
            d_pow = cand
            for _ in range(n - 1):
                d_pow = mat_kron(d_pow, cand)
            comp_padded = mat_kron(d_pow, seed_dx)

            all_nonneg = True
            for m_ord in range(1, n + 1):
                # Also build unpadded D^(x m) (x) D_{+X}.
                d_m = cand
                for _ in range(m_ord - 1):
                    d_m = mat_kron(d_m, cand)
                comp_direct = mat_kron(d_m, seed_dx)

                for subset in itertools.combinations(range(n), m_ord):
                    submat = [[cand[r][c] for c in subset] for r in subset]
                    det_val = exact_det(submat)
                    self.assertEqual(det_val.imag, ZERO_F, name)
                    target_weight = F(factorial(m_ord), 4) * det_val.real

                    # Direct event in Omega^m x {0,1,2,3} using atoms {2, 3} of D_{+X}.
                    direct_atoms: set[int] = set()
                    padded_atoms: set[int] = set()
                    pad_tail = list(itertools.product(range(n), repeat=n - m_ord))
                    for perm in itertools.permutations(subset):
                        anc = 2 + perm_parity(perm)  # 2 for even, 3 for odd
                        h_code = 0
                        for coord in perm:
                            h_code = h_code * n + coord
                        direct_atoms.add(4 * h_code + anc)
                        for tail in pad_tail:
                            full_code = h_code
                            for t_coord in tail:
                                full_code = full_code * n + t_coord
                            padded_atoms.add(4 * full_code + anc)

                    w_direct = mu_val(comp_direct, direct_atoms)
                    w_padded = mu_val(comp_padded, padded_atoms)
                    self.assertEqual(w_direct, target_weight, name)
                    self.assertEqual(w_padded, target_weight, name)
                    if w_padded < 0:
                        all_nonneg = False

            self.assertEqual(all_nonneg, expected_psd, name)

    def test_07_single_system_classical_cone_automorphisms_and_mixed_counterexample(self) -> None:
        # 1) Exhaustively verify for d=2,3,4 that reversible stochastic matrices preserve extremes
        #    and map every basis state e_i to deterministic {0, 1} sharp-partition weights.
        for d_dim in (2, 3, 4):
            for perm in itertools.permutations(range(d_dim)):
                p_mat = [[F(1 if r == perm[c] else 0) for c in range(d_dim)] for r in range(d_dim)]
                # Inverse is transpose, also nonnegative column-stochastic.
                p_inv = [[p_mat[c][r] for c in range(d_dim)] for r in range(d_dim)]
                for col in range(d_dim):
                    self.assertEqual(sum((p_mat[r][col] for r in range(d_dim)), ZERO_F), F(1))
                    self.assertEqual(sum((p_inv[r][col] for r in range(d_dim)), ZERO_F), F(1))
                # On any sharp cell A_0 subseteq {0..d-1} and extreme state e_j, weight is 0 or 1.
                for mask in range(1 << d_dim):
                    a0 = {r for r in range(d_dim) if (mask >> r) & 1}
                    for j in range(d_dim):
                        w = sum((p_mat[r][j] for r in a0), ZERO_F)
                        self.assertIn(w, (F(0), F(1)))

        # 2) Anti-overclaiming countermodel: on d=6 with MIXED state rho = (e_0 + e_1)/2,
        #    reversible permutation pi = (0 -> 2 -> 3 -> 1 -> 4 -> 5 -> 0) gives (1, 1/2, 0)!
        pi = (2, 4, 3, 1, 5, 0)  # image of (0, 1, 2, 3, 4, 5)
        self.assertEqual(sorted(pi), [0, 1, 2, 3, 4, 5])
        rho = [F(1, 2), F(1, 2), F(0), F(0), F(0), F(0)]
        a0_6 = {0, 1, 2}

        def step_perm(vec: list[F]) -> list[F]:
            out = [ZERO_F] * 6
            for src, val in enumerate(vec):
                out[pi[src]] += val
            return out

        rho_1 = step_perm(rho)
        rho_2 = step_perm(rho_1)
        q0_seq = [sum((v[idx] for idx in a0_6), ZERO_F) for v in (rho, rho_1, rho_2)]
        self.assertEqual(q0_seq, [F(1), F(1, 2), F(0)])

        # 3) Check native_active_residual_v1 exact 2x2 matrices lie in the classical cone.
        r_full = F(-1, 4224)
        t_half = F(1, 2)
        m_zero = [[F(3, 4), F(1, 4)], [F(1, 4), F(3, 4)]]
        t_full = [
            [F(1 + r_full + t_half, 2) / (1 + r_full), F(1 - r_full - t_half, 2) / (1 - r_full)],
            [F(1 + r_full - t_half, 2) / (1 + r_full), F(1 - r_full + t_half, 2) / (1 - r_full)],
        ]
        for mat_2 in (m_zero, t_full):
            for col in range(2):
                self.assertEqual(mat_2[0][col] + mat_2[1][col], F(1))
                self.assertGreater(mat_2[0][col], 0)
                self.assertGreater(mat_2[1][col], 0)
        # Verify exact Delta_update = 1/25344 from native_active_residual_v1 eq. (10).
        q_base = F(1, 3)
        d_full = F(-1, 12672)
        p_delta0 = q_base + d_full * (F(1) - F(0))
        p_k_delta0 = q_base + d_full * (F(3, 4) - F(1, 4))
        self.assertEqual(p_k_delta0 - p_delta0, F(1, 25344))

    def test_08_exact_rational_16_label_bipartite_chsh_separates_all_classical_cones(self) -> None:
        # Universal classical conical CHSH bound |S| <= 2 checked on all 16 extreme strategies.
        for a0, a1, b0, b1 in itertools.product((-1, 1), repeat=4):
            s_cl = a0 * b0 + a0 * b1 + a1 * b0 - a1 * b1
            self.assertLessEqual(abs(s_cl), 2)

        # Build 16-label RI-08d signed permutation T and shared coupler U0 = (I x H0) CNOT.
        def q_idx(a: int, i: int, b: int, j: int) -> int:
            return 8 * a + 4 * i + 2 * b + j

        def p_idx(a: int, b: int, i: int, j: int) -> int:
            return 8 * a + 4 * b + 2 * i + j

        t_mat = [[G(0) for _ in range(16)] for _ in range(16)]
        for a, i, b, j in itertools.product((0, 1), repeat=4):
            sign = -1 if (a * i + b * j) % 2 == 1 else 1
            t_mat[p_idx(a, b, i, j)][q_idx(a, i, b, j)] = G(sign)
        i16 = gmat([[int(r == c) for c in range(16)] for r in range(16)])
        self.assertEqual(mat_mul(t_mat, mat_dagger(t_mat)), i16)

        cnot_4 = gmat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        u0_sys = mat_mul(mat_kron(I2, H0), cnot_4)  # U0 * U0^dagger = 2 * I_4
        i4_cells = gmat([[int(r == c) for c in range(4)] for r in range(4)])
        u0_raw = mat_mul(mat_mul(mat_dagger(t_mat), mat_kron(i4_cells, u0_sys)), t_mat)

        # Prepare local D_{+Z} (in C_0) and polarized reference R_{t=1} = D((I+Z)/4, 0) = D_{+Z}.
        # Wait: in RI-08d, D(A, 0) with A = (I + Z)/4 = diag(1/2, 0) is D_{+Z};
        # to prepare the maximally entangled Bell state under (I x H) CNOT, use local D_{+X}!
        d_plus_z = gmat(
            [[F(1, 2), 0, 0, 0], [0, 0, 0, 0], [0, 0, F(1, 2), 0], [0, 0, 0, 0]]
        )
        d_plus_x = congruence(W_H0, d_plus_z, divisor=2)
        r_ref = d_plus_z  # B_{t=1} = (I + Z)/4 = diag(1/2, 0), so R_1 = diag(1/2, 0, 1/2, 0).

        n_initial = mat_kron(d_plus_x, r_ref)
        n_coupled = congruence(u0_raw, n_initial, divisor=2)
        self.assertTrue(is_hermitian(n_coupled))
        self.assertEqual(total_mass(n_coupled), G(1))

        joint_cells = {
            (0, 0): frozenset({0, 1, 4, 5}),
            (0, 1): frozenset({2, 3, 6, 7}),
            (1, 0): frozenset({8, 9, 12, 13}),
            (1, 1): frozenset({10, 11, 14, 15}),
        }
        for k1, s1 in joint_cells.items():
            for k2, s2 in joint_cells.items():
                if k1 != k2:
                    self.assertEqual(pair_val(n_coupled, s1, s2), G(0))

        # Exact rational local silent controls (zero square roots!):
        # Alice: x=0 -> I2 (/1), x=1 -> H0 (/2)
        # Bob:   y=0 -> [[2, -1], [1, 2]] (/5), y=1 -> [[1, -2], [2, 1]] (/5)
        alice_ops = [(F(1), I2), (F(2), H0)]
        bob_ops = [
            (F(5), gmat([[2, -1], [1, 2]])),
            (F(5), gmat([[1, -2], [2, 1]])),
        ]

        correlators: dict[tuple[int, int], F] = {}
        for x_set, (div_a, op_a) in enumerate(alice_ops):
            for y_set, (div_b, op_b) in enumerate(bob_ops):
                local_16 = mat_kron(lift_4(op_a), lift_4(op_b))
                n_xy = congruence(local_16, n_coupled, divisor=div_a * div_b)
                self.assertTrue(is_hermitian(n_xy))
                self.assertEqual(total_mass(n_xy), G(1))
                # Verify exact 4-cell decoherence for every setting pair.
                for k1, s1 in joint_cells.items():
                    for k2, s2 in joint_cells.items():
                        if k1 != k2:
                            self.assertEqual(pair_val(n_xy, s1, s2), G(0))
                probs = {k: mu_val(n_xy, s) for k, s in joint_cells.items()}
                self.assertEqual(sum(probs.values(), ZERO_F), F(1))
                for p_val in probs.values():
                    self.assertGreaterEqual(p_val, 0)
                correlators[(x_set, y_set)] = (
                    probs[(0, 0)] + probs[(1, 1)] - probs[(0, 1)] - probs[(1, 0)]
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


if __name__ == "__main__":
    unittest.main()
