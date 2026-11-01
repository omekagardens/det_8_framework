"""T5: finite supplied-kernel transport and local jump moments.

Q[i][j] = P(next=j | current=i) has outgoing rows. M=(Q-I)/eps
has zero row sums. Column probabilities evolve by Q.T p, not Q p.
Symmetric M is the negative of a weighted graph Laplacian; detailed balance
with a nonuniform stationary law does not itself imply matrix symmetry.

Coordinates, rates and eps are supplied dimensionless model parameters.
Local first/half-second jump moments do not prove a continuum PDE, physical
diffusion scale, arbitrary finite-time variance law or native-growth limit.
The public historical names and accurate result keys remain for compatibility.
"""
from __future__ import annotations

import math
from numbers import Real

_TOL = 1e-12  # Dimensionless probability/balance tolerance, never a rate floor.


def _scalar(value, name):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{name} must be representable") from error
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _count(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def _vector(values, name, n=None):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError(f"{name} must be a nonempty list or tuple")
    if n is not None and len(values) != n:
        raise ValueError(f"{name} dimension mismatch")
    return [_scalar(v, name) for v in values]


def _matrix(values, name):
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError(f"{name} must be a nonempty square matrix")
    return [_vector(row, name, len(values)) for row in values]


def _sum(values):
    try:
        result = math.fsum(values)
    except (OverflowError, ValueError) as error:
        raise ValueError("sum is not representable") from error
    if not math.isfinite(result):
        raise ValueError("sum is not finite")
    return result


def _kernel(values):
    q = _matrix(values, "Q")
    for row in q:
        if any(v < 0.0 or v > 1.0 for v in row):
            raise ValueError("Q entries must be probabilities")
        if not math.isclose(_sum(row), 1.0, rel_tol=0.0, abs_tol=_TOL):
            raise ValueError("Q outgoing rows must sum to one")
    return q


def _balanced(diagonal_magnitude, outgoing):
    # Both arguments are finite/nonnegative after the generator sign checks.
    # No dimensionful absolute tolerance: even a tiny sink/leak is not zero.
    scale = max(diagonal_magnitude, outgoing)
    if scale == 0.0:
        return True
    return abs(diagonal_magnitude / scale - outgoing / scale) <= _TOL


def _is_symmetric(m):
    # Exact equality of represented off-diagonal rates, including explicit zero.
    # Never silently symmetrize or admit a one-way edge by absolute magnitude.
    return all(m[i][j] == m[j][i] for i in range(len(m)) for j in range(i + 1, len(m)))


def _generator(values, symmetric=False):
    m = _matrix(values, "M")
    for i, row in enumerate(m):
        if row[i] > 0.0 or any(v < 0.0 for j, v in enumerate(row) if j != i):
            raise ValueError("M requires nonnegative off-diagonals and nonpositive diagonal")
        outgoing = _sum(v for j, v in enumerate(row) if j != i)
        if not _balanced(-row[i], outgoing):
            raise ValueError("M outgoing rows must sum to zero")
    if symmetric and not _is_symmetric(m):
        raise ValueError("spectral/relaxation helper requires exactly symmetric off-diagonal rates")
    return m


def _step_kernel(m, eps):
    step = _scalar(eps, "eps")
    if step < 0.0:
        raise ValueError("eps must be nonnegative")
    return _kernel([[step * v + (1.0 if i == j else 0.0)
                     for j, v in enumerate(row)] for i, row in enumerate(m)])


def _probability(values, n):
    p = _vector(values, "p", n)
    if any(v < 0.0 for v in p) or not math.isclose(_sum(p), 1.0, rel_tol=0.0, abs_tol=_TOL):
        raise ValueError("p must have nonnegative entries and mass one")
    return p


def _advance(p, q):
    # q[j][i] = eps*M[j][i] off diagonal: outgoing rows, column state.
    # Combining the diagonal first avoids subtractive cancellation at zero.
    return [_sum(q[j][i] * p[j] for j in range(len(p))) for i in range(len(p))]


def _connected(m):
    seen, pending = {0}, [0]
    while pending:
        i = pending.pop()
        for j, value in enumerate(m[i]):
            if j != i and value > 0.0 and j not in seen:
                seen.add(j)
                pending.append(j)
    return len(seen) == len(m)


def graph_laplacian_generator(Q: list[list[float]], eps: float) -> dict:
    """Extract the outgoing-row generator from a valid row-stochastic Q.

    eps must be positive: eps=0 does not identify a generator. A valid biased
    generator is not symmetric and has is_laplacian=False. Symmetry means exact
    represented off-diagonal equality, also used by both helpers. Nonnegative entries
    alone supply no geometric-locality or continuum certificate.
    """
    q = _kernel(Q)
    step = _scalar(eps, "eps")
    if step <= 0.0:
        raise ValueError("generator extraction requires eps > 0")
    m = _generator([[(v - (1.0 if i == j else 0.0)) / step
                     for j, v in enumerate(row)] for i, row in enumerate(q)])
    zero = all(_balanced(-row[i], _sum(v for j, v in enumerate(row) if j != i))
               for i, row in enumerate(m))
    symmetric = _is_symmetric(m)
    return {"M": m, "zero_row_sums": zero, "symmetric": symmetric,
            "nonneg_offdiag": True, "neg_diag": True,
            "is_laplacian": zero and symmetric}


def make_nearest_neighbor_kernel(n: int, w: float, eps: float,
                                 drift: float = 0.0) -> list[list[float]]:
    """Reflecting finite path, outgoing right/left rates w+drift,w-drift.

    n>=1; finite w>=abs(drift), eps>=0; the actual step must be stochastic.
    One state, zero rates and eps=0 give identity kernels. Positive drift
    favours increasing coordinates. One-way rates are admitted, without the
    positive-rate stationary theorem being extended to them.
    """
    n = _count(n, "n", 1)
    w, drift = _scalar(w, "w"), _scalar(drift, "drift")
    if w < abs(drift):
        raise ValueError("rates require w >= abs(drift)")
    right, left = _scalar(w + drift, "right rate"), _scalar(w - drift, "left rate")
    m = [[0.0] * n for _ in range(n)]
    for i in range(n):
        if i > 0:
            m[i][i - 1] = left
        if i + 1 < n:
            m[i][i + 1] = right
        m[i][i] = -_sum(m[i])
    return _step_kernel(m, eps)


def continuum_coefficients(M: list[list[float]], positions: list[float]) -> dict:
    """Local outgoing first and half-second generator moments at site n//2.

    Historical name/key diffusion retained; no PDE or physical coefficient is
    derived. At n=2 the reference is the right endpoint; at n=1 both moments
    vanish. Endpoint contributions are retained, not an assumed O(1/n) error.
    """
    m = _generator(M)
    x = _vector(positions, "positions", len(m))
    i = len(m) // 2
    v = _sum((x[j] - x[i]) * m[i][j] for j in range(len(m)) if j != i)
    try:
        d = 0.5 * _sum((x[j] - x[i]) ** 2 * m[i][j] for j in range(len(m)) if j != i)
    except OverflowError as error:
        raise ValueError("local second moment is not representable") from error
    return {"drift": v, "diffusion": d, "reference_site": i}


def _jacobi_eigh(A: list[list[float]], tol: float = 1e-12, max_iter: int = 500) -> list[float]:
    n = len(A)
    a = [row[:] for row in A]
    for _ in range(max_iter):
        p, q, mx = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > mx:
                    mx, p, q = abs(a[i][j]), i, j
        if mx < tol:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        theta = 0.5 * math.atan2(2.0 * apq, aqq - app)
        c, s = math.cos(theta), math.sin(theta)
        for k in range(n):
            if k == p or k == q:
                continue
            akp, akq = a[k][p], a[k][q]
            a[k][p] = a[p][k] = c * akp - s * akq
            a[k][q] = a[q][k] = s * akp + c * akq
        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0
    return sorted((a[i][i] for i in range(n)), reverse=True)


def spectral_gap(M: list[list[float]]) -> float:
    """Numerical exactly symmetric-generator gap; zero for n=1/disconnected graph.

    This is a generator eigenvalue, not a finite-step fitted decay rate.
    The existing finite Jacobi iteration is a numerical approximation.
    """
    m = _generator(M, symmetric=True)
    if not _connected(m) or len(m) == 1:
        return 0.0
    scale = max(abs(v) for row in m for v in row)
    values = sorted(_jacobi_eigh([[-v / scale for v in row] for row in m]))
    return _scalar(max(0.0, values[1]) * scale, "spectral gap")


def diffuse(p0: list[float], M: list[list[float]], eps: float, n_steps: int) -> list[float]:
    """Column p evolves by (I+eps*M).T, with outgoing-row M.

    Accept valid nonempty generators, simplex p0, stochastic eps>=0 and
    integer n_steps>=0. Degenerate/zero-step chains are valid. No normalization
    or orientation detection is performed, including at zero iterations.
    """
    m = _generator(M)
    q = _step_kernel(m, eps)
    p = _probability(p0, len(m))
    steps = _count(n_steps, "n_steps")
    for _ in range(steps):
        p = _advance(p, q)
    return p


def _moments(p: list[float], positions: list[float]) -> dict:
    """Normalized moments of a finite nonnegative vector with positive mass.

    run_t5 reports/checks full mass first; this normalization is not a repair.
    """
    p = _vector(p, "p")
    x = _vector(positions, "positions", len(p))
    total = _sum(p)
    if any(v < 0.0 for v in p) or total <= 0.0:
        raise ValueError("moments require nonnegative positive mass")
    mean = _sum(xi * pi for xi, pi in zip(x, p)) / total
    variance = _sum((xi - mean) ** 2 * pi for xi, pi in zip(x, p)) / total
    return {"mean": mean, "variance": variance}


def measure_relaxation_rate(M: list[list[float]], eps: float,
                            n_steps: int = 300) -> float:
    """Finite discrete late-window fit, exactly symmetric off-diagonal input only.

    eps>0, n_steps>=3, stochastic step. A nonzero generator must be connected;
    n=1 and the all-zero generator return 0 (no decay). Vanished late-window
    deviations are refused rather than hidden by a log floor. For one mode
    the discrete rate is -log(abs(1-eps*lambda))/eps when it decays; a mixture
    fit/roundoff need not equal this or the generator gap.
    """
    m = _generator(M, symmetric=True)
    step = _scalar(eps, "eps")
    if step <= 0.0:
        raise ValueError("relaxation rate requires eps > 0")
    steps = _count(n_steps, "n_steps", 3)
    q = _step_kernel(m, step)
    n = len(m)
    if n == 1 or all(v == 0.0 for row in m for v in row):
        return 0.0
    if not _connected(m):
        raise ValueError("nonzero relaxation experiment requires a connected generator")
    uniform = [1.0 / n] * n
    p = [1.0] + [0.0] * (n - 1)
    norms = []
    for _ in range(steps):
        p = _advance(p, q)
        norms.append(_sum((p[i] - uniform[i]) ** 2 for i in range(n)))
    start = int(0.6 * steps)
    xs = list(range(start, steps))
    if any(norms[i] <= 0.0 for i in xs):
        raise ValueError("late deviation vanished; no finite logarithmic fit")
    ys = [math.log(norms[i]) for i in xs]
    xbar, ybar = _sum(xs) / len(xs), _sum(ys) / len(ys)
    slope = _sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / _sum((x - xbar) ** 2 for x in xs)
    return _scalar(-slope / (2.0 * step), "finite relaxation fit")


def derivation_certificate() -> dict:
    return {
        "theorem": "T5 — finite supplied-kernel transport and local moments",
        "deliverables": {
            "Q = I + eps*M": "supplied finite weak-update model",
            "row normalization implies zero generator row sums": "finite algebra",
            "column p evolves by Q transpose": "finite probability transport",
            "symmetric valid M is a negative weighted graph Laplacian": "conditional finite classification",
            "outgoing first and half-second moments": "local jump statistics, including endpoints",
        },
        "not_derived_here": ["generic continuum or heat-equation limit",
                             "physical time/distance/diffusion scale or empirical validation",
                             "native growth correspondence or reversible wave-like limit"],
        "status": "Synthetic finite-model calculation; no general continuum or physical theorem.",
    }


def run_t5(n: int = 61, w: float = 1.0, eps: float = 0.05,
           drift: float = 0.0, n_steps: int = 200, seed: int = 42) -> dict:
    """Synthetic finite transport plus a separately symmetric relaxation fit.

    seed is retained but unused (no random sampling). eps>0 because extraction
    and rate fitting need it; both transport and the separate21-site symmetric
    step must be stochastic. Legacy empirical_* keys mean synthetic finite-law
    moments, and predicted_* mean the homogeneous unbounded-increment reference
    frozen at the reference site's moments, not exact bounded-chain predictions.
    """
    n, steps = _count(n, "n", 1), _count(n_steps, "n_steps")
    w, eps, drift = _scalar(w, "w"), _scalar(eps, "eps"), _scalar(drift, "drift")
    q = make_nearest_neighbor_kernel(n, w, eps, drift)
    gen = graph_laplacian_generator(q, eps)
    positions = [float(i - n // 2) for i in range(n)]
    coef = continuum_coefficients(gen["M"], positions)
    p0 = [0.0] * n
    p0[n // 2] = 1.0
    p_end = diffuse(p0, gen["M"], eps, steps)
    mass, minimum = _sum(p_end), min(p_end)
    if minimum < 0.0 or not math.isclose(mass, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ArithmeticError("finite transport lost probability mass/nonnegativity")
    # Complete law and mass are checked before any normalized summary.
    finite = _moments(p_end, positions)
    displacement = eps * coef["drift"]
    reference_variance = 2.0 * eps * coef["diffusion"] - displacement ** 2
    predicted_mean = _scalar(steps * displacement, "reference mean")
    predicted_variance = _scalar(steps * reference_variance, "reference variance")
    n_small = 21
    qs = make_nearest_neighbor_kernel(n_small, w, eps, 0.0)
    ms = graph_laplacian_generator(qs, eps)["M"]
    gap = 2.0 * w * (1.0 - math.cos(math.pi / n_small))
    fitted = measure_relaxation_rate(ms, eps, n_steps=4000)
    multiplier = abs(1.0 - eps * gap)
    discrete_rate = -math.log(multiplier) / eps if 0.0 < multiplier < 1.0 else (0.0 if multiplier == 1.0 else None)
    return {
        "n": n, "eps": eps, "n_steps": steps, "w": w, "drift": drift,
        "is_laplacian": gen["is_laplacian"], "continuum_coefficients": coef,
        "final_probabilities": p_end, "final_probability_mass": mass,
        "final_nonnegative": minimum >= 0.0, "minimum_probability": minimum,
        "empirical_mean": finite["mean"], "empirical_variance": finite["variance"],
        "predicted_mean": predicted_mean,
        "predicted_variance": predicted_variance,
        "comparison_model": "homogeneous unbounded increments frozen at reference; endpoint changes not modeled",
        "quantity_labels": {"empirical": "synthetic finite-law moment", "predicted": "homogeneous finite-step reference"},
        "spectral_gap_analytic": gap, "spectral_gap_measured": fitted,
        "relaxation_experiment": {"n": n_small, "drift": 0.0, "eps": eps, "n_steps": 4000,
                                  "generator_gap_analytic": gap, "discrete_mode_rate_analytic": discrete_rate,
                                  "finite_discrete_fit": fitted, "separate_from_transport": True},
        "certificate": derivation_certificate(),
        "interpretation": "Synthetic finite supplied-kernel transport; local moments and homogeneous reference are not a continuum proof. Relaxation is a separate symmetric finite experiment.",
    }
