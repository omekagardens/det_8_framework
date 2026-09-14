"""Descriptive applied fit demonstrations with explicit comparison limitations.

Historical function names and generator aliases remain callable. Synthetic
curves are declared fit families, not physical identification experiments.
Grid/clipped fits have descriptive training RSS and no ordinary BIC claim.
The roughness example declares its different observation-noise levels; it is
not a diffusion-versus-defect mechanism discriminator. Real aging inputs keep
actual elapsed chronology and require a separate observation-noise analysis.
"""

from __future__ import annotations

import math
import random
from itertools import pairwise

from det8.applied_physics import adversarial as adv
from det8.applied_physics import discriminator as disc
from det8.applied_physics import kappa_ingest as ki
from det8.models.validation import require_nonnegative_finite, require_positive_finite

GRID_REASON = "finite search bank and possible clipping/degeneracy; ordinary BIC regularity not established"
AGING_REASON = "finite tau bank and unvalidated clock-error covariance; ordinary BIC unavailable"


def _times(t, y):
    t, y = adv.paired_series(t, y)
    if any(value < 0 for value in t):
        raise ValueError("elapsed times must be nonnegative")
    return t, y


def _det_drift(t, T_t, flux_t, kappa0, kappa_eq, tau0, E_a, damage_rate, dt, scale):
    """Supplied clipped Euler recovery family y=scale*kappa; time units must agree."""
    t, T_t = _times(t, T_t)
    _, flux_t = adv.paired_series(t, flux_t)
    dt = require_positive_finite(dt, "dt")
    if any(not math.isclose(b - a, dt, rel_tol=1e-12, abs_tol=0)
           for a, b in pairwise(t)):
        raise ValueError("fixed-dt kappa solver requires evenly spaced actual times")
    if any(value <= 0 for value in T_t) or any(value < 0 for value in flux_t):
        raise ValueError("temperature must be positive and flux nonnegative")
    kappa0 = require_nonnegative_finite(kappa0, "kappa0")
    kappa_eq = require_nonnegative_finite(kappa_eq, "kappa_eq")
    if max(kappa0, kappa_eq) > 1:
        raise ValueError("kappa0 and kappa_eq must lie in [0,1]")
    tau0 = require_positive_finite(tau0, "tau0")
    E_a = require_nonnegative_finite(E_a, "activation energy")
    damage_rate = require_nonnegative_finite(damage_rate, "damage_rate")
    scale = require_positive_finite(scale, "scale")
    tau = ki.temperature_to_tau_rec(T_t, tau0, E_a)
    damage = ki.flux_to_damage(flux_t, damage_rate)
    adv.finite_series(tau, "recovery time")
    adv.finite_series(damage, "damage")
    return adv.finite_series([scale * k for k in ki.solve_kappa(kappa0, kappa_eq, tau, damage, dt)], "predicted output")


def kappa_output_coordinates(kappa0, kappa_eq, damage_rate, scale, tau0):
    """Unclipped fixed-Ea equation depends on these products, not five independent scalars.

    This is an upper bound of four identifiable combinations, not a fitted
    rank certificate. Constant forcing may lower rank; clipping changes the
    symmetry and regularity. A scale calibration must be independent to fix it.
    """
    values = [require_nonnegative_finite(value, "parameter")
              for value in (kappa0, kappa_eq, damage_rate)]
    scale, tau0 = require_positive_finite(scale, "scale"), require_positive_finite(tau0, "tau0")
    products = adv.finite_series([scale * value for value in values], "output coordinate")
    return {"y0": products[0], "y_eq": products[1],
            "output_damage_rate": products[2], "tau0": tau0}


def _fit_det_grid(t, drift, T_t, flux_t, dt,
                  kappa0_grid=(0.05, 0.1, 0.2, 0.5),
                  kappa_eq_grid=(0.0, 0.02, 0.05, 0.1, 0.5),
                  tau0_grid=(0.1, 1.0, 10.0, 30.0, 100.0, 300.0),
                  damage_grid=(0.0, 1e-3, 1e-2, 1e-1, 0.5),
                  scale_grid=(0.5, 1.0), E_a=0.01):
    """Descriptive finite-grid RSS fit; no rank inferred from named search quantities."""
    t, drift = _times(t, drift)
    _, T_t = adv.paired_series(t, T_t)
    _, flux_t = adv.paired_series(t, flux_t)
    grids = [tuple(grid) for grid in (kappa0_grid, kappa_eq_grid, tau0_grid, damage_grid, scale_grid)]
    if any(not grid for grid in grids):
        raise ValueError("parameter grids must be nonempty")
    best = None
    for k0 in grids[0]:
        for ke in grids[1]:
            for tau0 in grids[2]:
                for dmg in grids[3]:
                    for sc in grids[4]:
                        pred = _det_drift(t, T_t, flux_t, k0, ke, tau0, E_a, dmg, dt, sc)
                        rss = adv.rss_between(pred, drift)
                        if best is None or rss < best["rss"]:
                            best = {"rss": rss, "params": {"kappa0": k0, "kappa_eq": ke,
                                    "tau0": tau0, "damage_rate": dmg, "scale": sc}}
    best.update({"fit_family": "clipped_forced_recovery_grid", "bic_available": False,
                 "bic_reason": GRID_REASON, "identifiable_mean_parameters": None,
                 "unclipped_fixed_Ea_identifiable_combinations_at_most": 4,
                 "identifiability_note": "scale confounding without clipping; forcing may lower rank"})
    return best


def _fit_design(columns, y, rank_tolerance=1e-12):
    """Scaled modified Gram-Schmidt fit; rank is a stated numerical design diagnostic."""
    y = adv.finite_series(y)
    columns = [adv.finite_series(column) for column in columns]
    if any(len(column) != len(y) for column in columns):
        raise ValueError("design and observation lengths must match")
    q, r, scales = [], [], []
    for column in columns:
        norm = math.sqrt(math.fsum(value * value for value in column))
        scales.append(norm)
        v = [value / norm for value in column] if norm else [0.0] * len(y)
        coefficients = []
        for basis in q:
            coefficient = math.fsum(a * b for a, b in zip(basis, v))
            coefficients.append(coefficient)
            v = [a - coefficient * b for a, b in zip(v, basis)]
        # Reorthogonalize to avoid pretending an ill-conditioned normal matrix is full rank.
        for i, basis in enumerate(q):
            correction = math.fsum(a * b for a, b in zip(basis, v))
            coefficients[i] += correction
            v = [a - correction * b for a, b in zip(v, basis)]
        residual_norm = math.sqrt(math.fsum(value * value for value in v))
        r.append(coefficients + [residual_norm])
        if residual_norm > rank_tolerance:
            q.append([value / residual_norm for value in v])
    rank = len(q)
    if rank != len(columns):
        return None, rank
    rhs = [math.fsum(a * b for a, b in zip(basis, y)) for basis in q]
    scaled = [0.0] * rank
    for i in reversed(range(rank)):
        scaled[i] = (rhs[i] - math.fsum(r[j][i] * scaled[j] for j in range(i + 1, rank))) / r[i][i]
    return [value / norm for value, norm in zip(scaled, scales)], rank


def _fit_ieee(t, drift):
    """Log-linear a log(1+t)+bt+c; three mean parameters only for rank-three design."""
    t, drift = _times(t, drift)
    columns = [[math.log1p(value) for value in t], t, [1.0] * len(t)]
    coefficient, rank = _fit_design(columns, drift)
    metadata = {"fit_family": "log_linear", "design_rank": rank,
                "rank_tolerance": 1e-12, "identifiable_mean_parameters": rank,
                "bic_available": False, "bic_reason": "observation-noise and sampling assumptions not declared",
                "monotonicity_assumed": False}
    if coefficient is None:
        return {**metadata, "rss": None, "params": None, "error": "rank-deficient log-linear design"}
    pred = [sum(coefficient[j] * columns[j][i] for j in range(3)) for i in range(len(t))]
    return {**metadata, "rss": adv.rss_between(pred, drift),
            "params": dict(zip(("a", "b", "c"), coefficient))}


def _solve3(M, v):
    """Retained small-system helper; solve with pivoting, reject singular systems."""
    rows = [list(row) + [value] for row, value in zip(M, v, strict=True)]
    if len(rows) != 3 or any(len(row) != 4 for row in rows):
        raise ValueError("expected a three-by-three system")
    for i in range(3):
        pivot = max(range(i, 3), key=lambda j: abs(rows[j][i]))
        rows[i], rows[pivot] = rows[pivot], rows[i]
        if rows[i][i] == 0:
            raise ZeroDivisionError("singular system")
        divisor = rows[i][i]
        rows[i] = [value / divisor for value in rows[i]]
        for j in range(3):
            if j != i:
                factor = rows[j][i]
                rows[j] = [a - factor * b for a, b in zip(rows[j], rows[i])]
    return [row[-1] for row in rows]


def descriptive_fit_report(fits, n_data, reason=GRID_REASON):
    """Same-data training errors only, with no BIC or causal winner."""
    if isinstance(n_data, bool) or not isinstance(n_data, int) or n_data <= 0:
        raise ValueError("n_data must be a positive integer")
    require_positive_finite(n_data, "n_data")
    output = {}
    for family, fit in fits.items():
        rss = fit.get("rss")
        if rss is not None:
            rss = require_nonnegative_finite(rss, "rss")
        output[family] = {**fit, "rss": rss, "rmse": math.sqrt(rss) / math.sqrt(n_data) if rss is not None else None}
    scores = {family: fit["rss"] for family, fit in output.items() if fit["rss"] is not None}
    minimum = min(scores.values()) if scores and len(scores) == len(output) else None
    tied = [family for family, rss in scores.items() if rss == minimum]
    reasons = [reason]
    if any(rss == 0 for rss in scores.values()):
        reasons.append("zero RSS: unknown-variance Gaussian likelihood is unbounded")
    return {"fits": output, "n_data": n_data, "score_type": "descriptive_training_rss",
            "lowest_rss_family": tied[0] if len(tied) == 1 else None,
            "bic_available": False, "bic_reason": "; ".join(reasons),
            "best": None, "det_wins": None, "physical_mechanism_identified": False}


def _generator(value, first, second):
    aliases = {"det": first, "standard": second, first: first, second: second}
    if value not in aliases:
        raise ValueError("unknown synthetic generator")
    return aliases[value]


def _result(name, generator, report, **extra):
    return {"test": name, "generating_model": generator, "data_kind": "synthetic",
            **report, "bic_det": None, "bic_std": None, "correct_identification": None, **extra}


def test_gnss_clock_aging(generating_model="det", seed=42):
    """Declared deterministic recovery-pulse and stepped log-linear generator examples."""
    generator = _generator(generating_model, "clipped_recovery_pulse", "stepped_log_linear")
    t, temperature, flux = list(range(200)), [300.0] * 200, [0.0] * 200
    flux[100] = 1.0
    if generator == "clipped_recovery_pulse":
        drift = _det_drift(t, temperature, flux, 0.5, 0.5, 30, 0.01, 0.5, 1, 1)
    else:
        drift = [adv.ieee_clock_aging(ti, 0.3, 0.001, 0.1) + (0.5 if i >= 100 else 0)
                 for i, ti in enumerate(t)]
    report = descriptive_fit_report({"clipped_forced_recovery_grid": _fit_det_grid(t, drift, temperature, flux, 1),
                                     "log_linear": _fit_ieee(t, drift)}, len(t))
    return _result("GNSS clock aging", generator, report)


def test_qubit_drift(generating_model="det", seed=42):
    """Descriptive spatial roughness; generator noise variances differ by 100-fold."""
    generator = _generator(generating_model, "smoothed_profile_low_noise", "constant_profile_high_noise")
    rng = random.Random(seed)
    n = 20
    if generator == "smoothed_profile_low_noise":
        kappa = [0.8 if i == 5 else 0.2 for i in range(n)]
        for _ in range(100):
            new = list(kappa)
            for i in range(1, n - 1):
                new[i] += 0.05 * (kappa[i - 1] - 2 * kappa[i] + kappa[i + 1]) - (kappa[i] - 0.1) / 1000
            kappa = [max(0.0, min(1.0, value)) for value in new]
        mean, sigma = [1 / (1 + value) for value in kappa], 0.01
    else:
        mean, sigma = [0.8] * n, 0.1
    values = [value + rng.gauss(0, sigma) for value in mean]
    report = {"score_type": "descriptive_path_roughness", "roughness": adv.roughness(values),
              "declared_generator_null": adv.iid_roughness_moments(n, sigma, mean),
              "constant_mean_sigma_0_1_null": adv.iid_roughness_moments(n, 0.1),
              "declared_sigma": sigma, "bic_available": False, "det_wins": None,
              "bic_reason": "roughness is not a fitted Gaussian likelihood or BIC score",
              "physical_mechanism_identified": False,
              "note": "Different noise variances confound the old mechanism classification; no classification threshold is used."}
    return _result("Qubit spatial roughness", generator, report)


def _relaxation_demo(name, generating_model, seed, times, amplitude, tau, stretch):
    generator = _generator(generating_model, "single_exponential", "stretched_exponential")
    rng = random.Random(seed)
    beta = 1 if generator == "single_exponential" else stretch
    drift = [amplitude * adv.kww_relaxation(ti, tau, beta) + rng.gauss(0, 0.005) for ti in times]
    full = disc.fit_kww(times, drift)
    single = disc.fit_kww(times, drift, beta_grid=(1.0,))
    report = descriptive_fit_report({"single_exponential_grid": single, "stretched_exponential_grid": full}, len(times))
    return _result(name, generator, report, fitted_beta=full["beta"], classification=full["classification"])


def test_cavity_creep(generating_model="det", seed=42):
    return _relaxation_demo("Cavity relaxation", generating_model, seed, list(range(0, 400, 4)), 1, 50, 0.5)


def test_space_degradation(generating_model="det", seed=42):
    generator = _generator(generating_model, "forced_recovery", "linear_cumulative_flux")
    t, flux = list(range(200)), [1.0] * 200
    temperature = [400.0 if i % 20 < 10 else 200.0 for i in t]
    if generator == "forced_recovery":
        drift = _det_drift(t, temperature, flux, 0.1, 0, 0.1, 0.1, 1e-3, 1, 1)
    else:
        drift = [adv.ddd_degradation(1e-5 * i, 1) for i in t]
    recovery = _fit_det_grid(t, drift, temperature, flux, 1, E_a=0.1)
    cumulative = [i + 1 for i in t]
    slope, intercept, rss = adv.least_squares_fit_linear(cumulative, drift)
    baseline = {"rss": rss, "params": {"slope": slope, "intercept": intercept},
                "identifiable_mean_parameters": 2, "fit_family": "linear_with_intercept"}
    return _result("Spacecraft degradation", generator,
                   descriptive_fit_report({"clipped_forced_recovery_grid": recovery, "linear_with_intercept": baseline}, len(t)))


def test_gauge_block(generating_model="det", seed=42):
    return _relaxation_demo("Gauge-block relaxation", generating_model, seed, list(range(0, 120, 2)), 0.5, 30, 0.6)


def run_all_applied_tests():
    functions = (test_gnss_clock_aging, test_qubit_drift, test_cavity_creep, test_space_degradation, test_gauge_block)
    rows = [function(generating_model=generator) for function in functions for generator in ("det", "standard")]
    return {"rows": rows, "n_tests": len(rows), "n_correct_identification": None,
            "fraction_correct": None, "physical_mechanism_identified": False,
            "interpretation": "Ten synthetic descriptive fit/roughness examples; no BIC winner or mechanism-identification success rate is established."}


TAU_GRID = (1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 100, 200, 300, 500, 700, 1000, 2000, 5000, 10000)


def _fit_exp_decay(t, y, tau_grid=TAU_GRID):
    """Finite tau bank for A exp(-t/tau)+C, a nominal three-mean-parameter family."""
    t, y = _times(t, y)
    taus = tuple(require_positive_finite(value, "tau") for value in tau_grid)
    if not taus:
        raise ValueError("tau grid must be nonempty")
    best = None
    for tau in taus:
        xs = [math.exp(-ti / tau) for ti in t]
        if len(set(xs)) < 2:
            continue
        amplitude, offset, rss = adv.least_squares_fit_linear(xs, y)
        if best is None or rss < best["rss"]:
            best = {"rss": rss, "tau": tau, "A": amplitude, "C": offset}
    metadata = {"fit_family": "exponential_offset_grid", "nominal_continuous_mean_parameters": 3,
                "identifiable_mean_parameters": None, "bic_available": False,
                "bic_reason": "finite tau bank; zero amplitude or long tau can be degenerate"}
    if best is None:
        return {**metadata, "rss": None, "tau": None, "A": None, "C": None,
                "error": "no identifiable amplitude/offset design in the tau bank"}
    if best["A"] == 0:
        best["grid_minimizer_tau"] = best["tau"]
        best["tau"] = None
        best["degeneracy"] = "zero amplitude: tau unidentified"
    return {**best, **metadata}


def clock_aging_coordinates(records):
    """Elapsed days from actual interval starts, preserving gaps and time-scale handling.

    Uses the existing ingestion elapsed-time contract (including leap seconds).
    Missing metadata, mixed systems, duplicate/overlapping daily intervals and
    multidate products are refused. Records are sorted without mutating inputs.
    """
    from det8.applied_physics.ingest import _elapsed_seconds, _epoch_coordinate

    records = list(records)
    if not records:
        raise ValueError("no dated clock records")
    if any(not record.get("start_epoch") or not record.get("end_epoch") for record in records):
        raise ValueError("unsupported chronology: daily start/end epochs are required")
    if len({record.get("time_system") for record in records}) != 1:
        raise ValueError("inconsistent clock time systems")
    records = sorted(records, key=lambda record: _epoch_coordinate(record["start_epoch"]))
    origin = {"epoch": records[0]["start_epoch"], "time_system": records[0].get("time_system")}
    times, values = [], []
    previous_end, previous_date = None, None
    for record in records:
        start, end = _epoch_coordinate(record["start_epoch"]), _epoch_coordinate(record["end_epoch"])
        first = {"epoch": record["start_epoch"], "time_system": record.get("time_system")}
        last = {"epoch": record["end_epoch"], "time_system": record.get("time_system")}
        if start.date() != end.date() or start.date() == previous_date:
            raise ValueError("daily clock intervals must occupy distinct single civil days")
        if _elapsed_seconds(first, last) <= 0 or (previous_end is not None and start <= previous_end):
            raise ValueError("clock intervals must be positive and nonoverlapping")
        times.append(_elapsed_seconds(origin, first) / 86400)
        values.append(record["drift_s_per_s"])
        previous_end, previous_date = end, start.date()
    return times, adv.finite_series(values, "clock drift"), records


def aging_fit_report(records, *, tau_grid=TAU_GRID, extra_fitters=None):
    """Shared descriptive clock comparison; no BIC until noise and fit assumptions are justified."""
    t, y, ordered = clock_aging_coordinates(records)
    fits = {"exponential_offset_grid": _fit_exp_decay(t, y, tau_grid), "log_linear": _fit_ieee(t, y)}
    for family, fitter in (extra_fitters or {}).items():
        if family in fits:
            raise ValueError("duplicate fit-family label")
        fits[family] = fitter(t, y)
    return {**descriptive_fit_report(fits, len(y), AGING_REASON), "elapsed_days": t,
            "span_days": t[-1] - t[0], "time_system": ordered[0].get("time_system"),
            "time_coordinate": "elapsed seconds between recorded interval starts / 86400",
            "source_records": ordered, "tau_best_days": fits["exponential_offset_grid"]["tau"],
            "interval_averaging_modeled": False}


def run_aging_adversarial(clk_dir, svn, tau_grid=TAU_GRID):
    from det8.applied_physics.ingest import run_clock_aging

    records = run_clock_aging(clk_dir, svn)
    if len(records) < 10:
        return {"svn": svn, "n_days": len(records), "error": "too few daily records (<10) for this descriptive comparison"}
    try:
        report = aging_fit_report(records, tau_grid=tau_grid)
    except ValueError as exc:
        return {"svn": svn, "n_days": len(records), "error": str(exc), "bic_available": False}
    return {"svn": svn, "n_days": len(records), **report, "bic_kappa": None, "bic_ieee": None,
            "delta_bic": None, "strength": None, "verdict": "descriptive fit errors only"}


def run_all_aging_adversarial(clk_dir, svns):
    rows = [run_aging_adversarial(clk_dir, svn) for svn in svns]
    return {"rows": rows, "n_satellites": sum("error" not in row for row in rows),
            "n_kappa_wins": None, "interpretation": "Dated descriptive fits; no causal winner count or calibrated BIC evidence."}
