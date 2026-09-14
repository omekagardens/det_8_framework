"""Descriptive fits and explicitly conditional Gaussian comparison arithmetic.

RSS needs a declared observation-noise model. Ordinary BIC additionally needs
an identifiable regular likelihood fit and suitable sampling asymptotics;
a clipped trajectory or finite search bank does not establish these premises.
No comparison identifies a DET mechanism. Regularity reference:
https://arxiv.org/abs/1309.0911. Gaussian/Cholesky identities:
https://www.cs.helsinki.fi/u/ahonkela/teaching/compstats1/book/multivariate-normal-distributions-and-numerical-linear-algebra.html
"""

from __future__ import annotations

import math
from itertools import pairwise

from det8.models.validation import (
    require_nonnegative_finite,
    require_positive_finite,
    require_real_finite,
)

K_B_EV = 8.617333262e-5


def finite_series(values, name="series") -> list[float]:
    result = [require_real_finite(value, name) for value in values]
    if not result:
        raise ValueError(f"{name} must be nonempty")
    return result


def paired_series(left, right) -> tuple[list[float], list[float]]:
    left, right = finite_series(left), finite_series(right)
    if len(left) != len(right):
        raise ValueError("series must have equal lengths")
    return left, right


def _count(value, name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    require_real_finite(value, name)
    return value


def _sum_squares(values, name):
    """Finite squared terms; refuse representational zeros from nonzero inputs."""
    squares = []
    for value in values:
        value = require_real_finite(value, name)
        square = value * value
        if value != 0 and square == 0:
            raise ValueError(f"{name}: positive squared term underflows float representation")
        squares.append(require_nonnegative_finite(square, name))
    try:
        return require_nonnegative_finite(math.fsum(squares), name)
    except OverflowError as exc:
        raise ValueError(f"{name} exceeds finite float representation") from exc


def gaussian_iid_unknown_variance(n_data: int, rss: float) -> dict:
    """Profile -2 log likelihood; zero RSS has unbounded likelihood, not a score."""
    n_data = _count(n_data, "n_data", 1)
    rss = require_nonnegative_finite(rss, "rss")
    if rss == 0:
        return {"available": False, "neg2_log_likelihood": None, "variance_mle": None,
                "reason": "zero RSS: unknown-variance Gaussian likelihood is unbounded"}
    score = require_real_finite(n_data * (math.log(2 * math.pi) + 1 + math.log(rss) - math.log(n_data)), "log likelihood")
    variance = rss / n_data
    return {"available": True, "neg2_log_likelihood": score,
            "variance_mle": variance if variance > 0 else None,
            "variance_mle_representable": variance > 0,
            "variance_mle_status": "positive" if variance > 0 else "positive MLE underflows float representation",
            "noise_model": "unknown common iid Gaussian variance"}


def _covariance_factor(covariance, n, *, allow_singular=False):
    """Finite symmetric covariance, with no jitter, clipping or hidden repair."""
    covariance = [finite_series(row, "covariance row") for row in covariance]
    if len(covariance) != n or any(len(row) != n for row in covariance):
        raise ValueError("covariance dimensions must match the observations")
    if any(covariance[i][j] != covariance[j][i] for i in range(n) for j in range(n)):
        raise ValueError("covariance must be symmetric")
    lower = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            residual = covariance[i][j] - math.fsum(lower[i][k] * lower[j][k] for k in range(j))
            require_real_finite(residual, "covariance factor residual")
            if i == j:
                if residual < 0 or (residual == 0 and not allow_singular):
                    raise ValueError("covariance must be positive semidefinite" if allow_singular
                                     else "covariance must be positive definite")
                lower[i][j] = math.sqrt(residual)
            elif lower[j][j] != 0:
                lower[i][j] = residual / lower[j][j]
            elif residual != 0:
                raise ValueError("zero covariance pivot has nonzero cross covariance")
    return covariance, lower


def gaussian_known_covariance(residuals, covariance) -> dict:
    """Gaussian -2 log density under fixed positive-definite R, including constants.

    Fixed independent calibration constants are not fitted parameters. Zero
    residual is permitted. Correct likelihood alone does not justify BIC.
    """
    residuals = finite_series(residuals, "residuals")
    n = len(residuals)
    _, lower = _covariance_factor(covariance, n)
    whitened = []
    for i, residual in enumerate(residuals):
        whitened.append((residual - math.fsum(lower[i][j] * whitened[j] for j in range(i)))
                        / lower[i][i])
    quadratic = _sum_squares(whitened, "Gaussian residual quadratic")
    if quadratic == 0 and any(value != 0 for value in residuals):
        raise ValueError("positive Gaussian residual quadratic underflows float representation")
    logdet = 2 * math.fsum(math.log(lower[i][i]) for i in range(n))
    score = require_real_finite(quadratic + logdet + n * math.log(2 * math.pi), "log likelihood")
    return {"available": True, "neg2_log_likelihood": score, "quadratic": quadratic,
            "log_determinant": logdet, "noise_model": "known Gaussian covariance",
            "fitted_noise_parameters": 0}


def bic(n_params: int, n_data: int, rss: float, *, regularity_confirmed=False) -> float | None:
    """Conditional iid BIC; n_params counts fitted identifiable mean parameters.

    Includes the estimated common variance and Gaussian constants. The caller
    must explicitly establish regularity, likelihood fitting and iid sampling.
    None means unavailable assumptions or an unbounded zero-RSS likelihood.
    """
    n_data, n_params = _count(n_data, "n_data", 1), _count(n_params, "n_params")
    if n_params >= n_data:
        raise ValueError("unknown-variance fitting needs n_data > n_params")
    if type(regularity_confirmed) is not bool:
        raise TypeError("regularity_confirmed must be a bool")
    likelihood = gaussian_iid_unknown_variance(n_data, rss)
    if not regularity_confirmed or not likelihood["available"]:
        return None
    return require_real_finite(likelihood["neg2_log_likelihood"] + (n_params + 1) * math.log(n_data), "BIC")


def bic_known_covariance(n_params, residuals, covariance, *, regularity_confirmed=False):
    """Conditional known-covariance BIC; no fixed calibration parameter counted."""
    n_params = _count(n_params, "n_params")
    residuals = finite_series(residuals, "residuals")
    if n_params > len(residuals):
        raise ValueError("n_params cannot exceed n_data")
    if type(regularity_confirmed) is not bool:
        raise TypeError("regularity_confirmed must be a bool")
    likelihood = gaussian_known_covariance(residuals, covariance)
    return (require_real_finite(likelihood["neg2_log_likelihood"] + n_params * math.log(len(residuals)), "BIC")
            if regularity_confirmed else None)


def compare_bic(det_n_params, det_rss, std_n_params, std_rss, n_data, *,
                regularity_confirmed=False, families=("candidate", "baseline")) -> dict:
    """Historical argument names; compare fit families, never causal DET identification."""
    if len(families) != 2 or families[0] == families[1]:
        raise ValueError("supply two distinct fit-family labels")
    first = bic(det_n_params, n_data, det_rss, regularity_confirmed=regularity_confirmed)
    second = bic(std_n_params, n_data, std_rss, regularity_confirmed=regularity_confirmed)
    available = first is not None and second is not None
    reason = ("zero RSS: unknown-variance Gaussian likelihood is unbounded"
              if det_rss == 0 or std_rss == 0 else
              "regular identifiable likelihood fit and sampling assumptions not confirmed")
    preferred = (families[0] if first < second else families[1] if second < first else None) if available else None
    delta = require_real_finite(first - second, "BIC difference") if available else None
    return {"comparison_available": available, "scores": dict(zip(families, (first, second))),
            "preferred_family": preferred, "delta_bic": delta,
            "reason": None if available else reason, "bic_det": first, "bic_std": second,
            "det_wins": None, "physical_mechanism_identified": False,
            "verdict": "conditional fit-family comparison" if available else "BIC unavailable"}


def roughness(series) -> float:
    values = finite_series(series)
    return _sum_squares((b - a for a, b in pairwise(values)), "roughness")


def gaussian_roughness_moments(mean, covariance) -> dict:
    """Path roughness moments under a declared Gaussian mean/covariance.

    For delta=D mean and V=D covariance D^T: E Q=delta^T delta+tr V;
    Var Q=2tr(V²)+4delta^T V delta. Shared difference errors are retained.
    These are null moments, not a diffusion likelihood or a significance test.
    """
    mean = finite_series(mean, "mean")
    covariance, _ = _covariance_factor(covariance, len(mean), allow_singular=True)
    delta = [b - a for a, b in pairwise(mean)]
    v = [[covariance[i + 1][j + 1] - covariance[i + 1][j]
          - covariance[i][j + 1] + covariance[i][j]
          for j in range(len(delta))] for i in range(len(delta))]
    deterministic = _sum_squares(delta, "deterministic roughness")
    noise = math.fsum(v[i][i] for i in range(len(delta)))
    variance = 2 * _sum_squares((value for row in v for value in row), "roughness covariance square")
    variance += 4 * math.fsum(delta[i] * v[i][j] * delta[j]
                              for i in range(len(delta)) for j in range(len(delta)))
    if variance == 0 and any(value != 0 for row in v for value in row):
        raise ValueError("positive Gaussian roughness variance is not representable")
    for name, value in (("roughness mean", deterministic + noise), ("roughness variance", variance),
                        ("deterministic roughness", deterministic), ("noise contribution", noise)):
        require_nonnegative_finite(value, name)
    return {"mean": deterministic + noise, "variance": variance,
            "deterministic_roughness": deterministic, "noise_contribution": noise,
            "difference_covariance": v, "p_value": None,
            "physical_mechanism_identified": False}


def iid_roughness_moments(n_data, sigma, mean=None):
    n_data = _count(n_data, "n_data", 1)
    sigma = require_nonnegative_finite(sigma, "sigma")
    noise_variance = _sum_squares([sigma], "noise variance")
    mean = [0.0] * n_data if mean is None else finite_series(mean, "mean")
    if len(mean) != n_data:
        raise ValueError("mean length must equal n_data")
    return gaussian_roughness_moments(mean, [[noise_variance if i == j else 0.0
                                           for j in range(n_data)] for i in range(n_data)])


def ieee_clock_aging(t, a, b, c):
    """Log-linear family; derivative a/(1+t)+b may change sign."""
    t = require_real_finite(t, "time")
    if t <= -1:
        raise ValueError("log-linear time must exceed -1")
    a, b, c = (require_real_finite(value, "coefficient") for value in (a, b, c))
    return a * math.log1p(t) + b * t + c


def kww_relaxation(t, tau, beta):
    """Exp(-(t/tau)^beta), a descriptive shape rather than a unique mechanism."""
    t = require_nonnegative_finite(t, "time")
    tau, beta = require_positive_finite(tau, "tau"), require_positive_finite(beta, "beta")
    return math.exp(-((t / tau) ** beta))


def arrhenius_rate(T_K, tau0_s, E_a_eV):
    T_K = require_positive_finite(T_K, "temperature")
    tau0_s = require_positive_finite(tau0_s, "tau0")
    E_a_eV = require_nonnegative_finite(E_a_eV, "activation energy")
    return math.exp(-E_a_eV / (K_B_EV * T_K)) / tau0_s


def ddd_degradation(cumulative_flux, k):
    return require_nonnegative_finite(cumulative_flux, "cumulative flux") * require_real_finite(k, "slope")


def least_squares_fit_linear(xs, ys):
    """Fit BOTH slope and intercept; refuse an unidentifiable constant design."""
    xs, ys = paired_series(xs, ys)
    xbar, ybar = math.fsum(xs) / len(xs), math.fsum(ys) / len(ys)
    centered = [x - xbar for x in xs]
    denominator = math.fsum(x * x for x in centered)
    if denominator == 0:
        raise ValueError("slope is unidentifiable for a constant design")
    slope = math.fsum(x * (y - ybar) for x, y in zip(centered, ys)) / denominator
    intercept = ybar - slope * xbar
    return slope, intercept, rss_between([slope * x + intercept for x in xs], ys)


def rss_between(predicted, observed) -> float:
    predicted, observed = paired_series(predicted, observed)
    return _sum_squares((p - o for p, o in zip(predicted, observed)), "RSS")
