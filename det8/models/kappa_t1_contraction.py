"""Pathway 1: T1 Kernel-Contraction + Reciprocal Aperture Gravity Model.

Implements the revived Pathway 1 formulation built on DET 8.1 T1 Markov
kernel contraction (``docs/record_kernel_physics.md`` §2.4):

    N_int(r) / N_rec = (Sigma_*(r) + Sigma_gas(r)) / Sigma_crit + w_SFR * Sigma_SFR(r)
    kappa(r)         = exp(-N_int(r) / N_rec) in (0, 1]
    G_eff(r)         = G / (1 - beta * kappa(r)),   beta in [0, 1)

This module is active (not in ``FULLY_RETIRED``), imports neutral empirical
fixtures from ``det8.models.galaxy_observables`` and only the literature bound
list ``PUBLISHED_EOTVOS`` from ``det8.models.experimental_constraints``, and
explicitly separates DET-native theorems (``TH-DET``), correspondences
(``CORR``), empirical closures/fits (``FIT``), and external anchors
(``EXTERNAL_ANCHOR``).
"""

from __future__ import annotations

import decimal
import math
import sys
from typing import Final, Sequence

from det8.models.experimental_constraints import PUBLISHED_EOTVOS
from det8.models.galaxy_observables import (
    C_SI,
    G_SI,
    KM_S_TO_M_S,
    KPC_TO_M,
    KNOWN_GALAXIES,
    M_SUN_KG,
    SAMPLE_GALAXIES,
    GalaxyObservables,
    GalaxyParams,
    load_sparc_subset_diagnostic,
    newton_rotation_velocity,
    sfr_surface_density,
    stellar_surface_density,
)


# ═══════════════════════════════════════════════════════════════════════════
# External Anchor Constants (Never imported from retired post_newtonian.py)
# ═══════════════════════════════════════════════════════════════════════════

AU_M: Final[float] = 1.495978707e11                    # IAU 2012 astronomical unit [m]
CASSINI_GAMMA_MINUS_1_BOUND: Final[float] = 2.3e-5     # Bertotti et al. 2003 Shapiro-delay bound
MOND_A0_M_S2: Final[float] = 1.2e-10                   # Milgrom acceleration scale [m/s^2]

DEFAULT_SIGMA_CRIT: Final[float] = 0.008               # [10^9 M_sun / kpc^2]
DEFAULT_BETA: Final[float] = 0.93                      # Dimensionless reciprocal-aperture coupling
DEFAULT_DISK_SCALE_HEIGHT_KPC: Final[float] = 0.3      # Nominal baryonic disk thickness [kpc]
DEFAULT_SOLAR_WIND_1AU_KG_M3: Final[float] = 1.0e-19   # Dense 1 AU solar-wind proxy [kg/m^3]
DEFAULT_LAB_WATER_DENSITY_KG_M3: Final[float] = 1.0e3  # Liquid water density [kg/m^3]
DEFAULT_LAB_SOLID_DENSITY_KG_M3: Final[float] = 1.0e4  # Typical laboratory solid density [kg/m^3]

_VALID_GAS_MODES: Final[frozenset[str]] = frozenset({"1d", "freeman_2d"})


# ═══════════════════════════════════════════════════════════════════════════
# Strict Domain & Type Validation Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _ensure_real_float(name: str, value: object) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a real number, got bool {value!r}")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    try:
        fval = float(value)
    except OverflowError as exc:
        raise ValueError(
            f"{name} must be finite and representable as float64, got {value!r}"
        ) from exc
    if not math.isfinite(fval):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return fval


def _validate_non_negative_finite(name: str, value: object) -> float:
    fval = _ensure_real_float(name, value)
    if fval < 0.0:
        raise ValueError(f"{name} must be >= 0, got {value!r}")
    return fval


def _validate_positive_finite(name: str, value: object) -> float:
    fval = _ensure_real_float(name, value)
    if fval <= 0.0:
        raise ValueError(f"{name} must be > 0, got {value!r}")
    return fval


def _validate_unit_closed(name: str, value: object) -> float:
    fval = _ensure_real_float(name, value)
    if fval < 0.0 or fval > 1.0:
        raise ValueError(f"{name} must satisfy 0.0 <= {name} <= 1.0, got {value!r}")
    return fval


def _validate_half_open_unit(name: str, value: object) -> float:
    fval = _ensure_real_float(name, value)
    if fval < 0.0 or fval >= 1.0:
        raise ValueError(f"{name} must satisfy 0.0 <= {name} < 1.0, got {value!r}")
    return fval


def _validate_positive_int(name: str, value: object, *, minimum: int = 1) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer >= {minimum}, got bool {value!r}")
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value!r}")
    return value


def _validate_gas_mode(gas_mode: object) -> str:
    if not isinstance(gas_mode, str) or gas_mode not in _VALID_GAS_MODES:
        raise ValueError(f"Invalid gas_mode {gas_mode!r}; expected '1d' or 'freeman_2d'")
    return gas_mode


def _validate_bool_flag(name: str, value: object) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _normalize_name(name: str) -> str:
    return "".join(name.split()).upper()


def _median(values: Sequence[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    if n == 0:
        raise ValueError("Cannot compute median of an empty sequence")
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return 0.5 * (ordered[mid - 1] + ordered[mid])


def _eotvos_bounds_by_name() -> dict[str, float]:
    bounds = {entry.name: float(entry.eta_upper_bound) for entry in PUBLISHED_EOTVOS}
    required = ("MICROSCOPE (2022)", "Eöt-Wash (2008)", "Lunar Laser Ranging")
    missing = [name for name in required if name not in bounds]
    if missing:
        raise RuntimeError(f"Missing expected PUBLISHED_EOTVOS entries: {missing}")
    return bounds


# ═══════════════════════════════════════════════════════════════════════════
# Core Pathway 1 Physics Functions
# ═══════════════════════════════════════════════════════════════════════════


def t1_contraction_kappa(
    r_kpc: float,
    M_star: float,
    r_d: float,
    M_gas: float = 0.0,
    r_gas: float = 0.0,
    *,
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    SFR: float = 0.0,
    r_SFR: float = 1.0,
    w_sfr: float = 0.0,
) -> float:
    """Compute Pathway 1 T1 Markov contraction ``kappa(r)`` in ``(0, 1]``.

    Formula:
        ``n_ratio = (Sigma_*(r) + Sigma_gas(r)) / sigma_crit + w_sfr * Sigma_SFR(r)``
        ``kappa(r) = exp(-n_ratio)``

    Mathematically ``kappa(r)`` lies in ``(0, 1]`` and in IEEE-754 float64
    lies in ``[0.0, 1.0]`` (underflowing cleanly to ``0.0`` when
    ``n_ratio >= 745.14``).
    """
    r_val = _validate_non_negative_finite("r_kpc", r_kpc)
    m_star_val = _validate_non_negative_finite("M_star", M_star)
    r_d_val = _validate_non_negative_finite("r_d", r_d)
    m_gas_val = _validate_non_negative_finite("M_gas", M_gas)
    r_gas_val = _validate_non_negative_finite("r_gas", r_gas)
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    sfr_val = _validate_non_negative_finite("SFR", SFR)
    r_sfr_val = _validate_positive_finite("r_SFR", r_SFR)
    w_sfr_val = _validate_non_negative_finite("w_sfr", w_sfr)

    s_star = stellar_surface_density(r_val, m_star_val, r_d_val)
    s_gas = stellar_surface_density(r_val, m_gas_val, r_gas_val)
    s_sfr = sfr_surface_density(r_val, sfr_val, r_sfr_val)

    # Guard 0.0 * inf = nan when w_sfr == 0.0 and s_sfr overflows.
    sfr_term = (w_sfr_val * s_sfr) if (w_sfr_val > 0.0 and s_sfr > 0.0) else 0.0
    n_ratio = (s_star + s_gas) / sigma_crit_val + sfr_term
    return math.exp(-n_ratio)


def reciprocal_aperture_g_eff(
    kappa: float,
    beta: float = DEFAULT_BETA,
    G: float = G_SI,
) -> float:
    """Compute effective gravitational coupling ``G_eff = G / (1 - beta * kappa)``."""
    kappa_val = _validate_unit_closed("kappa", kappa)
    beta_val = _validate_half_open_unit("beta", beta)
    g_val = _validate_positive_finite("G", G)
    return g_val / (1.0 - beta_val * kappa_val)


def pathway1_rotation_velocity(
    r_kpc: float,
    galaxy: GalaxyParams | GalaxyObservables,
    *,
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    w_sfr: float = 0.0,
    gas_mode: str = "1d",
) -> float:
    """Compute Pathway 1 circular rotation velocity [km/s] at radius ``r_kpc``."""
    if not isinstance(galaxy, (GalaxyParams, GalaxyObservables)):
        raise TypeError(
            "galaxy must be GalaxyParams or GalaxyObservables, "
            f"got {type(galaxy).__name__}"
        )
    r_val = _validate_positive_finite("r_kpc", r_kpc)
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    beta_val = _validate_half_open_unit("beta", beta)
    w_sfr_val = _validate_non_negative_finite("w_sfr", w_sfr)
    mode = _validate_gas_mode(gas_mode)

    if isinstance(galaxy, GalaxyObservables):
        sfr = galaxy.SFR
        r_sfr = galaxy.r_SFR
    else:
        sfr = 0.0
        r_sfr = 1.0

    v_newton = newton_rotation_velocity(
        r_val,
        galaxy.M_star,
        galaxy.r_d,
        galaxy.M_gas,
        galaxy.r_gas,
        gas_mode=mode,
    )
    kappa = t1_contraction_kappa(
        r_val,
        galaxy.M_star,
        galaxy.r_d,
        galaxy.M_gas,
        galaxy.r_gas,
        sigma_crit=sigma_crit_val,
        SFR=sfr,
        r_SFR=r_sfr,
        w_sfr=w_sfr_val,
    )
    g_eff = reciprocal_aperture_g_eff(kappa, beta=beta_val, G=G_SI)
    return v_newton * math.sqrt(g_eff / G_SI)


# ═══════════════════════════════════════════════════════════════════════════
# F6 Monotonicity Check
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_f6_sign_check(
    sigma_crit: float = 0.015,
    w_sfr: float = 0.5,
    *,
    r_core_kpc: float = 0.1,
    r_out_kpc: float = 30.0,
    n_points: int = 100,
) -> dict[str, object]:
    """Audit F6 radial sign behavior of ``t1_contraction_kappa`` across ``KNOWN_GALAXIES``."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    w_sfr_val = _validate_non_negative_finite("w_sfr", w_sfr)
    r_core_val = _validate_non_negative_finite("r_core_kpc", r_core_kpc)
    r_out_val = _validate_positive_finite("r_out_kpc", r_out_kpc)
    if r_out_val <= r_core_val:
        raise ValueError(
            f"r_out_kpc ({r_out_kpc!r}) must be > r_core_kpc ({r_core_kpc!r})"
        )
    n_pts = _validate_positive_int("n_points", n_points, minimum=2)

    step = (r_out_val - r_core_val) / (n_pts - 1)
    r_grid = [r_core_val + i * step for i in range(n_pts - 1)]
    r_grid.append(r_out_val)

    galaxies_out: list[dict[str, object]] = []
    n_increasing = 0
    n_monotonic = 0

    for g in KNOWN_GALAXIES:
        kappas = [
            t1_contraction_kappa(
                r,
                g.M_star,
                g.r_d,
                g.M_gas,
                g.r_gas,
                sigma_crit=sigma_crit_val,
                SFR=g.SFR,
                r_SFR=g.r_SFR,
                w_sfr=w_sfr_val,
            )
            for r in r_grid
        ]
        k_core = kappas[0]
        k_out = kappas[-1]
        dk = k_out - k_core
        increasing = dk > 0.0
        non_decreasing = all(
            kappas[idx + 1] >= kappas[idx] for idx in range(len(kappas) - 1)
        )
        monotonic = increasing and non_decreasing
        if increasing:
            n_increasing += 1
        if monotonic:
            n_monotonic += 1
        galaxies_out.append(
            {
                "name": g.name,
                "r_SFR_over_r_d": g.r_SFR / g.r_d,
                "kappa_core": k_core,
                "kappa_outskirts": k_out,
                "delta_kappa": dk,
                "increasing": increasing,
                "monotonic": monotonic,
            }
        )

    n_total = len(KNOWN_GALAXIES)
    return {
        "sigma_crit": sigma_crit_val,
        "w_sfr": w_sfr_val,
        "r_core_kpc": r_core_val,
        "r_out_kpc": r_out_val,
        "n_points": n_pts,
        "n_total": n_total,
        "n_increasing": n_increasing,
        "n_monotonic": n_monotonic,
        "all_increasing": n_increasing == n_total,
        "all_monotonic": n_monotonic == n_total,
        "galaxies": galaxies_out,
        "analytical_non_dip_proof": (
            "d/dr [(Sigma_*(r) + Sigma_gas(r))/Sigma_crit + w_SFR * Sigma_SFR(r)] = "
            "-Sigma_*(r)/(r_d * Sigma_crit) - Sigma_gas(r)/(r_gas * Sigma_crit) "
            "- w_SFR * Sigma_SFR(r)/r_SFR <= 0 for all r >= 0 and w_SFR >= 0. "
            "Because terms are summed with '+' rather than divided as Sigma_*/Sigma_SFR, "
            "d kappa / dr >= 0 everywhere regardless of r_SFR / r_d."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# SPARC 43-Galaxy Fit & Cross-Dataset Comparisons
# ═══════════════════════════════════════════════════════════════════════════


def _evaluate_sample_subset(
    sigma_crit: float,
    beta: float,
    gas_mode: str,
) -> dict[str, object]:
    fits: list[dict[str, object]] = []
    errors: list[float] = []
    bins: dict[str, list[float]] = {"dwarf": [], "mid": [], "high": []}
    within_20pct = 0
    within_50pct = 0

    for g in SAMPLE_GALAXIES:
        v_newton = newton_rotation_velocity(
            g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode=gas_mode
        )
        kappa = t1_contraction_kappa(
            g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, sigma_crit=sigma_crit
        )
        g_ratio = reciprocal_aperture_g_eff(kappa, beta=beta, G=G_SI) / G_SI
        v_pred = v_newton * math.sqrt(g_ratio)
        rel_err = abs(v_pred - g.v_flat) / g.v_flat
        signed_err = (v_pred - g.v_flat) / g.v_flat

        errors.append(rel_err)
        if rel_err < 0.20:
            within_20pct += 1
        if rel_err < 0.50:
            within_50pct += 1

        if g.M_star < 1.0:
            mass_bin = "dwarf"
        elif g.M_star < 10.0:
            mass_bin = "mid"
        else:
            mass_bin = "high"
        bins[mass_bin].append(rel_err)

        fits.append(
            {
                "name": g.name,
                "mass_bin": mass_bin,
                "M_star": g.M_star,
                "r_max": g.r_max,
                "kappa": kappa,
                "g_eff_over_G": g_ratio,
                "v_newton_kms": v_newton,
                "v_pred_kms": v_pred,
                "v_obs_kms": g.v_flat,
                "rel_error": rel_err,
                "signed_rel_error": signed_err,
            }
        )

    n_total = len(SAMPLE_GALAXIES)
    mean_err = sum(errors) / n_total
    mass_bins_summary = {
        key: {
            "count": len(vals),
            "mean_error": (sum(vals) / len(vals)) if vals else 0.0,
            "median_error": _median(vals) if vals else 0.0,
        }
        for key, vals in bins.items()
    }
    worst = sorted(fits, key=lambda item: float(item["rel_error"]), reverse=True)[:5]

    return {
        "gas_mode": gas_mode,
        "n_galaxies": n_total,
        "mean_error": mean_err,
        "median_error": _median(errors),
        "within_20pct": within_20pct,
        "within_50pct": within_50pct,
        "within_20_fraction": within_20pct / n_total,
        "within_50_fraction": within_50pct / n_total,
        "mass_bins": mass_bins_summary,
        "worst_fits": worst,
        "fits": fits,
    }


def _evaluate_known_galaxies_comparison(
    sigma_crit: float,
    beta: float,
    gas_mode: str,
) -> dict[str, object]:
    sample_by_name = {_normalize_name(g.name): g for g in SAMPLE_GALAXIES}
    at_5rd_8kpc: list[dict[str, object]] = []
    at_matched_rmax: list[dict[str, object]] = []

    for g in KNOWN_GALAXIES:
        r_fallback = max(5.0 * g.r_d, 8.0)
        v_pred_fb = pathway1_rotation_velocity(
            r_fallback, g, sigma_crit=sigma_crit, beta=beta, w_sfr=0.0, gas_mode=gas_mode
        )
        err_fb = abs(v_pred_fb - g.V_flat) / g.V_flat
        sample_match = sample_by_name.get(_normalize_name(g.name))
        m_star_ratio = (
            (sample_match.M_star / g.M_star) if sample_match is not None else None
        )
        at_5rd_8kpc.append(
            {
                "name": g.name,
                "r_kpc": r_fallback,
                "v_pred_kms": v_pred_fb,
                "v_obs_kms": g.V_flat,
                "rel_error": err_fb,
                "sample_over_known_M_star": m_star_ratio,
            }
        )

        if sample_match is not None:
            v_pred_m = pathway1_rotation_velocity(
                sample_match.r_max,
                g,
                sigma_crit=sigma_crit,
                beta=beta,
                w_sfr=0.0,
                gas_mode=gas_mode,
            )
            err_m = abs(v_pred_m - g.V_flat) / g.V_flat
            at_matched_rmax.append(
                {
                    "name": g.name,
                    "r_max_kpc": sample_match.r_max,
                    "v_pred_kms": v_pred_m,
                    "v_obs_kms": g.V_flat,
                    "rel_error": err_m,
                    "sample_over_known_M_star": m_star_ratio,
                }
            )

    mean_fb = (
        sum(float(item["rel_error"]) for item in at_5rd_8kpc) / len(at_5rd_8kpc)
        if at_5rd_8kpc
        else 0.0
    )
    mean_matched = (
        sum(float(item["rel_error"]) for item in at_matched_rmax) / len(at_matched_rmax)
        if at_matched_rmax
        else 0.0
    )
    max_m_ratio = max(
        (
            float(item["sample_over_known_M_star"])
            for item in at_5rd_8kpc
            if item["sample_over_known_M_star"] is not None
        ),
        default=None,
    )
    ratio_note = (
        f"SAMPLE_GALAXIES lists up to {max_m_ratio:.2f}x larger stellar masses for the "
        "same named massive spirals (e.g., NGC 2903: 30.0 vs 2.6 x 10^9 M_sun)."
        if max_m_ratio is not None
        else "no shared galaxy names exist between SAMPLE_GALAXIES and KNOWN_GALAXIES."
    )

    return {
        "n_galaxies": len(KNOWN_GALAXIES),
        "at_max_5rd_8kpc": {
            "mean_error": mean_fb,
            "galaxies": at_5rd_8kpc,
        },
        "at_matched_sample_rmax": {
            "count": len(at_matched_rmax),
            "mean_error": mean_matched,
            "galaxies": at_matched_rmax,
        },
        "max_sample_over_known_M_star_ratio": max_m_ratio,
        "discrepancy_note": (
            f"KNOWN_GALAXIES exhibits higher error ({mean_fb:.1%} at max(5*r_d, 8 kpc), "
            f"{mean_matched:.1%} at matched r_max) than SAMPLE_GALAXIES primarily because "
            + ratio_note
        ),
    }


def evaluate_sparc_fit(
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    *,
    gas_mode: str = "1d",
) -> dict[str, object]:
    """Evaluate Pathway 1 SPARC 43-galaxy fit, ceiling, 2D gas comparison, and fixture audits."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    beta_val = _validate_half_open_unit("beta", beta)
    mode = _validate_gas_mode(gas_mode)

    primary = _evaluate_sample_subset(sigma_crit_val, beta_val, mode)
    eval_1d = primary if mode == "1d" else _evaluate_sample_subset(sigma_crit_val, beta_val, "1d")
    eval_2d = (
        primary
        if mode == "freeman_2d"
        else _evaluate_sample_subset(sigma_crit_val, beta_val, "freeman_2d")
    )

    max_enhancement = 1.0 / (1.0 - beta_val)

    # Quantify the high-ceiling trade-off directly on SAMPLE_GALAXIES.
    tradeoff_evals: dict[str, dict[str, object]] = {}
    for candidate_beta in (0.97, 0.98):
        cand = _evaluate_sample_subset(sigma_crit_val, candidate_beta, mode)
        tradeoff_evals[f"beta_{candidate_beta:.2f}"] = {
            "beta": candidate_beta,
            "max_enhancement": 1.0 / (1.0 - candidate_beta),
            "mean_error": cand["mean_error"],
            "within_20pct": cand["within_20pct"],
            "within_50pct": cand["within_50pct"],
        }

    subset_diag = load_sparc_subset_diagnostic()
    anomalies = subset_diag.get("anomalies", {})
    cross = subset_diag.get("cross_comparison", {})
    sample_overlaps = cross.get("vs_sample_galaxies", {}).get("overlaps", [])
    max_subset_ratio = max(
        (
            float(item["M_star_ratio"])
            for item in sample_overlaps
            if item.get("M_star_ratio") is not None
        ),
        default=None,
    )

    return {
        "sigma_crit": sigma_crit_val,
        "beta": beta_val,
        "gas_mode": mode,
        "max_enhancement": max_enhancement,
        "beta_ceiling_note": (
            f"At beta={beta_val:.2f}, max enhancement 1/(1 - beta) = {max_enhancement:.4f}x "
            "(exceeding the retired alpha=16 9x ceiling, though below 30-50x). "
            "Reaching 33.3x-50.0x requires beta=0.97-0.98, which degrades SPARC mean error."
        ),
        "high_beta_tradeoff": tradeoff_evals,
        "n_galaxies": primary["n_galaxies"],
        "mean_error": primary["mean_error"],
        "median_error": primary["median_error"],
        "within_20pct": primary["within_20pct"],
        "within_50pct": primary["within_50pct"],
        "within_20_fraction": primary["within_20_fraction"],
        "within_50_fraction": primary["within_50_fraction"],
        "mass_bins": primary["mass_bins"],
        "worst_fits": primary["worst_fits"],
        "fits": primary["fits"],
        "freeman_2d_comparison": {
            "1d": {
                "mean_error": eval_1d["mean_error"],
                "median_error": eval_1d["median_error"],
                "within_20pct": eval_1d["within_20pct"],
                "within_50pct": eval_1d["within_50pct"],
                "mass_bins": eval_1d["mass_bins"],
            },
            "freeman_2d": {
                "mean_error": eval_2d["mean_error"],
                "median_error": eval_2d["median_error"],
                "within_20pct": eval_2d["within_20pct"],
                "within_50pct": eval_2d["within_50pct"],
                "mass_bins": eval_2d["mass_bins"],
            },
        },
        "known_galaxies_comparison": _evaluate_known_galaxies_comparison(
            sigma_crit_val, beta_val, mode
        ),
        "sparc_subset_audit": {
            "record_count": subset_diag.get("record_count", 0),
            "raw_json_valid": subset_diag.get("raw_json_valid", False),
            "m_gas_equals_m_star_count": anomalies.get("m_gas_equals_m_star_count", 0),
            "zero_v_flat_count": anomalies.get("zero_v_flat_count", 0),
            "missing_galaxy_params_fields": anomalies.get(
                "missing_galaxy_params_fields", []
            ),
            "vs_sample_overlap_count": cross.get("vs_sample_galaxies", {}).get(
                "overlap_count", 0
            ),
            "vs_known_overlap_count": cross.get("vs_known_galaxies", {}).get(
                "overlap_count", 0
            ),
            "max_sample_over_subset_M_star_ratio": max_subset_ratio,
            "audit_note": (
                "det8/data/sparc_subset.json cannot be directly fitted without inventing "
                "missing r_gas and r_max fields and replacing corrupted M_gas == M_star values."
            ),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# Radial Asymptotics (r >= 4 r_d and outer Keplerian turnover)
# ═══════════════════════════════════════════════════════════════════════════


def _summarize_slopes(slopes: Sequence[float], kappas: Sequence[float]) -> dict[str, object]:
    n = len(slopes)
    return {
        "count": n,
        "mean_slope": sum(slopes) / n,
        "min_slope": min(slopes),
        "max_slope": max(slopes),
        "mean_kappa": sum(kappas) / n if kappas else 0.0,
        "declining_lt_minus_0_1_count": sum(1 for s in slopes if s < -0.1),
        "steep_lt_minus_0_3_count": sum(1 for s in slopes if s < -0.3),
        "near_keplerian_lt_minus_0_45_count": sum(1 for s in slopes if s < -0.45),
    }


def evaluate_radial_asymptotics(
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    *,
    gas_mode: str = "1d",
    r_multipliers: tuple[float, ...] = (1.0, 2.0, 4.0, 6.0, 8.0, 10.0, 20.0, 50.0),
) -> dict[str, object]:
    """Evaluate radial rotation-curve asymptotics and Keplerian ``r^(-1/2)`` turnover."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    beta_val = _validate_half_open_unit("beta", beta)
    mode = _validate_gas_mode(gas_mode)

    if not isinstance(r_multipliers, (tuple, list)) or len(r_multipliers) == 0:
        raise ValueError("r_multipliers must be a non-empty sequence of positive numbers")
    validated_mults = tuple(
        _validate_positive_finite(f"r_multipliers[{idx}]", val)
        for idx, val in enumerate(r_multipliers)
    )
    if any(
        validated_mults[i + 1] <= validated_mults[i]
        for i in range(len(validated_mults) - 1)
    ):
        raise ValueError("r_multipliers must be strictly increasing")

    eps = 1e-4
    denom_log = math.log((1.0 + eps) / (1.0 - eps))

    def _central_log_slope(r_kpc: float, g: GalaxyParams) -> float:
        v_minus = pathway1_rotation_velocity(
            r_kpc * (1.0 - eps), g, sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
        )
        v_plus = pathway1_rotation_velocity(
            r_kpc * (1.0 + eps), g, sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
        )
        if v_minus <= 0.0 or v_plus <= 0.0:
            raise ValueError(
                f"Degenerate non-positive rotation velocity for {g.name!r} at "
                f"r_kpc={r_kpc!r}: v_minus={v_minus!r}, v_plus={v_plus!r}"
            )
        return math.log(v_plus / v_minus) / denom_log

    def _chord_log_slope(r1_kpc: float, r2_kpc: float, g: GalaxyParams) -> float:
        v1 = pathway1_rotation_velocity(
            r1_kpc, g, sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
        )
        v2 = pathway1_rotation_velocity(
            r2_kpc, g, sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
        )
        if v1 <= 0.0 or v2 <= 0.0:
            raise ValueError(
                f"Degenerate non-positive rotation velocity for {g.name!r} on chord "
                f"[{r1_kpc!r}, {r2_kpc!r}]: v1={v1!r}, v2={v2!r}"
            )
        return math.log(v2 / v1) / math.log(r2_kpc / r1_kpc)

    mult_slopes: dict[float, list[float]] = {m: [] for m in validated_mults}
    mult_kappas: dict[float, list[float]] = {m: [] for m in validated_mults}
    rmax_slopes: list[float] = []
    rmax_kappas: list[float] = []

    chord_4rd_rmax: list[float] = []
    chord_rmax_2rmax: list[float] = []
    chord_2rmax_4rmax: list[float] = []
    chord_10scale_20scale: list[float] = []

    galaxy_profiles: list[dict[str, object]] = []

    for g in SAMPLE_GALAXIES:
        profile_points: list[dict[str, object]] = []
        for m in validated_mults:
            r_eval = m * g.r_d
            v_eval = pathway1_rotation_velocity(
                r_eval, g, sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
            )
            k_eval = t1_contraction_kappa(
                r_eval, g.M_star, g.r_d, g.M_gas, g.r_gas, sigma_crit=sigma_crit_val
            )
            slope_eval = _central_log_slope(r_eval, g)
            mult_slopes[m].append(slope_eval)
            mult_kappas[m].append(k_eval)
            profile_points.append(
                {
                    "r_over_rd": m,
                    "r_kpc": r_eval,
                    "kappa": k_eval,
                    "v_kms": v_eval,
                    "dlnv_dlnr": slope_eval,
                }
            )

        slope_rmax = _central_log_slope(g.r_max, g)
        k_rmax = t1_contraction_kappa(
            g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, sigma_crit=sigma_crit_val
        )
        rmax_slopes.append(slope_rmax)
        rmax_kappas.append(k_rmax)

        r_4rd = 4.0 * g.r_d
        s_4rd_rmax = (
            _chord_log_slope(r_4rd, g.r_max, g)
            if g.r_max > r_4rd
            else _central_log_slope(g.r_max, g)
        )
        s_1_2 = _chord_log_slope(g.r_max, 2.0 * g.r_max, g)
        s_2_4 = _chord_log_slope(2.0 * g.r_max, 4.0 * g.r_max, g)
        r_scale = max(g.r_d, g.r_gas)
        s_10_20 = _chord_log_slope(10.0 * r_scale, 20.0 * r_scale, g)

        chord_4rd_rmax.append(s_4rd_rmax)
        chord_rmax_2rmax.append(s_1_2)
        chord_2rmax_4rmax.append(s_2_4)
        chord_10scale_20scale.append(s_10_20)

        galaxy_profiles.append(
            {
                "name": g.name,
                "r_d": g.r_d,
                "r_max": g.r_max,
                "r_max_over_rd": g.r_max / g.r_d,
                "slope_at_r_max": slope_rmax,
                "slope_4rd_to_rmax": s_4rd_rmax,
                "slope_rmax_to_2rmax": s_1_2,
                "slope_2rmax_to_4rmax": s_2_4,
                "slope_10scale_to_20scale": s_10_20,
                "profile": profile_points,
            }
        )

    multiplier_summaries = {
        str(m): {
            "r_over_rd": m,
            **_summarize_slopes(mult_slopes[m], mult_kappas[m]),
        }
        for m in validated_mults
    }

    regime_summaries = {
        "at_r_max": _summarize_slopes(rmax_slopes, rmax_kappas),
        "four_rd_to_rmax": _summarize_slopes(chord_4rd_rmax, rmax_kappas),
        "rmax_to_2rmax": _summarize_slopes(chord_rmax_2rmax, rmax_kappas),
        "outer_2_to_4_rmax": _summarize_slopes(chord_2rmax_4rmax, rmax_kappas),
        "outer_10_to_20_scale": _summarize_slopes(chord_10scale_20scale, rmax_kappas),
    }

    max_mult = validated_mults[-1]
    far_mult_mean = float(multiplier_summaries[str(max_mult)]["mean_slope"])
    far_outer_mean = float(regime_summaries["outer_2_to_4_rmax"]["mean_slope"])

    return {
        "sigma_crit": sigma_crit_val,
        "beta": beta_val,
        "gas_mode": mode,
        "r_multipliers": validated_mults,
        "n_galaxies": len(SAMPLE_GALAXIES),
        "multiplier_summaries": multiplier_summaries,
        "regime_summaries": regime_summaries,
        "galaxies": galaxy_profiles,
        "summary": {
            "far_outer_slope_mean": far_outer_mean,
            "max_multiplier_mean_slope": far_mult_mean,
            "keplerian_turnover_universal": (
                regime_summaries["outer_2_to_4_rmax"]["steep_lt_minus_0_3_count"]
                == len(SAMPLE_GALAXIES)
            ),
            "asymptotic_note": (
                "Once Sigma_*(r) + Sigma_gas(r) << Sigma_crit, kappa(r) saturates to 1 "
                "and G_eff(r) saturates to G/(1 - beta). Because M_bar(<r) also saturates, "
                "v(r) = sqrt(G_eff * M_bar / r) universally turns over to a Keplerian "
                "r^(-1/2) decline (d ln v / d ln r -> -0.5) rather than staying asymptotically flat."
            ),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# R6-A Screening, Experimental Bounds, and FL-1 Rank Separation
# ═══════════════════════════════════════════════════════════════════════════


def sigma_crit_to_rho_crit(
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    scale_height_kpc: float = DEFAULT_DISK_SCALE_HEIGHT_KPC,
    *,
    thickness_factor: float = 1.0,
) -> float:
    """Convert ``sigma_crit`` [10^9 M_sun/kpc^2] to 3D ``rho_crit`` [kg/m^3]."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    h_val = _validate_positive_finite("scale_height_kpc", scale_height_kpc)
    factor_val = _validate_positive_finite("thickness_factor", thickness_factor)

    # Fast path when no intermediate overflows or underflows to subnormal/zero.
    sigma_g = sigma_crit_val * 1e9
    sigma_kg = sigma_g * M_SUN_KG
    sigma_si = sigma_kg / (KPC_TO_M ** 2)
    fh = factor_val * h_val
    denom = fh * KPC_TO_M
    min_normal = sys.float_info.min
    intermediates_normal = all(
        math.isfinite(val) and val >= min_normal
        for val in (
            sigma_crit_val,
            h_val,
            factor_val,
            sigma_g,
            sigma_kg,
            sigma_si,
            fh,
            denom,
        )
    )
    rho_crit = (sigma_si / denom) if intermediates_normal else float("nan")

    if not math.isfinite(rho_crit) or rho_crit < min_normal:
        with decimal.localcontext() as ctx:
            ctx.prec = 80
            num = (
                decimal.Decimal.from_float(sigma_crit_val)
                * decimal.Decimal("1000000000")
                * decimal.Decimal.from_float(M_SUN_KG)
            )
            den = (
                (decimal.Decimal.from_float(KPC_TO_M) ** 3)
                * decimal.Decimal.from_float(factor_val)
                * decimal.Decimal.from_float(h_val)
            )
            rho_crit = float(num / den)

    if not math.isfinite(rho_crit) or rho_crit <= 0.0:
        raise ValueError(
            f"Effective rho_crit={rho_crit!r} must be finite and > 0 "
            f"(from sigma_crit={sigma_crit_val!r}, scale_height_kpc={h_val!r}, "
            f"thickness_factor={factor_val!r})"
        )
    return rho_crit


def _eval_screening_law(
    rho_kg_m3: float,
    rho_crit_kg_m3: float,
    beta: float,
    bound_value: float | None,
) -> dict[str, object]:
    ratio = rho_kg_m3 / rho_crit_kg_m3
    if not math.isfinite(ratio):
        raise ValueError(
            f"Non-finite density ratio rho/rho_crit={ratio!r} "
            f"(rho_kg_m3={rho_kg_m3!r}, rho_crit_kg_m3={rho_crit_kg_m3!r})"
        )

    kappa_exp = math.exp(-ratio) if ratio < 745.14 else 0.0
    log10_kappa_exp = -ratio / math.log(10.0)
    if not math.isfinite(log10_kappa_exp):
        raise ValueError(
            f"Non-finite log10_kappa={log10_kappa_exp!r} "
            f"(rho_kg_m3={rho_kg_m3!r}, rho_crit_kg_m3={rho_crit_kg_m3!r})"
        )
    dg_exp = (beta * kappa_exp) / (1.0 - beta * kappa_exp)

    kappa_pow = 1.0 / (1.0 + ratio)
    dg_pow = (beta * kappa_pow) / (1.0 - beta * kappa_pow)
    if not (math.isfinite(dg_exp) and math.isfinite(kappa_pow) and math.isfinite(dg_pow)):
        raise ValueError(
            "Non-finite screening law output "
            f"(rho_kg_m3={rho_kg_m3!r}, rho_crit_kg_m3={rho_crit_kg_m3!r}, beta={beta!r})"
        )

    exp_passes = (dg_exp < bound_value) if bound_value is not None else None
    pow_passes = (dg_pow < bound_value) if bound_value is not None else None

    return {
        "rho_kg_m3": rho_kg_m3,
        "rho_over_rho_crit": ratio,
        "exponential": {
            "kappa": kappa_exp,
            "log10_kappa": log10_kappa_exp,
            "delta_G_over_G": dg_exp,
            "passes_bound": exp_passes,
            "underflowed_to_zero": kappa_exp == 0.0,
        },
        "power_law": {
            "kappa": kappa_pow,
            "delta_G_over_G": dg_pow,
            "passes_bound": pow_passes,
        },
    }


def _eval_differential_eotvos(
    rho_a: float,
    rho_b: float,
    rho_crit: float,
    beta: float,
    eta_bound: float,
) -> dict[str, object]:
    ra = rho_a / rho_crit
    rb = rho_b / rho_crit
    if not math.isfinite(ra) or not math.isfinite(rb):
        raise ValueError(
            f"Non-finite differential Eotvos density ratio: ra={ra!r}, rb={rb!r} "
            f"(rho_crit={rho_crit!r})"
        )

    ka_exp = math.exp(-ra) if ra < 745.14 else 0.0
    kb_exp = math.exp(-rb) if rb < 745.14 else 0.0
    ga_exp = 1.0 / (1.0 - beta * ka_exp)
    gb_exp = 1.0 / (1.0 - beta * kb_exp)
    eta_exp = 2.0 * abs(ga_exp - gb_exp) / (ga_exp + gb_exp)

    ka_pow = 1.0 / (1.0 + ra)
    kb_pow = 1.0 / (1.0 + rb)
    ga_pow = 1.0 / (1.0 - beta * ka_pow)
    gb_pow = 1.0 / (1.0 - beta * kb_pow)
    eta_pow = 2.0 * abs(ga_pow - gb_pow) / (ga_pow + gb_pow)

    return {
        "rho_a_kg_m3": rho_a,
        "rho_b_kg_m3": rho_b,
        "eta_bound": eta_bound,
        "exponential": {
            "eta": eta_exp,
            "passes_bound": eta_exp < eta_bound,
        },
        "power_law": {
            "eta": eta_pow,
            "passes_bound": eta_pow < eta_bound,
        },
    }


def evaluate_screening_constraints(
    *,
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    scale_height_kpc: float = DEFAULT_DISK_SCALE_HEIGHT_KPC,
    thickness_factor: float = 1.0,
    solar_wind_1au_kg_m3: float = DEFAULT_SOLAR_WIND_1AU_KG_M3,
    lab_density_kg_m3: float = DEFAULT_LAB_SOLID_DENSITY_KG_M3,
    fl1_delta_kappa_proxy: float = 0.002,
    fl1_delta_kappa_clock: float = 0.5,
) -> dict[str, object]:
    """Audit R6-A screening (enclosed vs local 1 AU, lab, Eötvös) and FL-1 rank separation."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    beta_val = _validate_half_open_unit("beta", beta)
    h_val = _validate_positive_finite("scale_height_kpc", scale_height_kpc)
    factor_val = _validate_positive_finite("thickness_factor", thickness_factor)
    sw_1au_val = _validate_positive_finite("solar_wind_1au_kg_m3", solar_wind_1au_kg_m3)
    lab_rho_val = _validate_positive_finite("lab_density_kg_m3", lab_density_kg_m3)
    fl1_proxy_val = _validate_unit_closed("fl1_delta_kappa_proxy", fl1_delta_kappa_proxy)
    fl1_clock_val = _validate_unit_closed("fl1_delta_kappa_clock", fl1_delta_kappa_clock)
    if fl1_proxy_val == 0.0:
        raise ValueError("fl1_delta_kappa_proxy must be > 0")
    if fl1_clock_val == 0.0:
        raise ValueError("fl1_delta_kappa_clock must be > 0")

    rho_crit = sigma_crit_to_rho_crit(
        sigma_crit_val, h_val, thickness_factor=factor_val
    )
    eotvos_bounds = _eotvos_bounds_by_name()
    microscope_eta = eotvos_bounds["MICROSCOPE (2022)"]
    eot_wash_eta = eotvos_bounds["Eöt-Wash (2008)"]
    llr_eta = eotvos_bounds["Lunar Laser Ranging"]

    rho_roche_1au = M_SUN_KG / ((4.0 / 3.0) * math.pi * (AU_M ** 3))
    rho_roche_40au = M_SUN_KG / ((4.0 / 3.0) * math.pi * ((40.0 * AU_M) ** 3))
    rho_local_40au = sw_1au_val / (40.0 ** 2)
    pc_to_m = KPC_TO_M / 1000.0
    rho_solar_nbhd = 0.08 * M_SUN_KG / (pc_to_m ** 3)

    regime_specs: tuple[tuple[str, float, str | None, float | None], ...] = (
        ("enclosed_1au_roche", rho_roche_1au, "Cassini |gamma - 1|", CASSINI_GAMMA_MINUS_1_BOUND),
        ("local_1au_solar_wind", sw_1au_val, "Cassini |gamma - 1|", CASSINI_GAMMA_MINUS_1_BOUND),
        ("enclosed_40au_kuiper", rho_roche_40au, "Cassini |gamma - 1|", CASSINI_GAMMA_MINUS_1_BOUND),
        ("local_40au_solar_wind", rho_local_40au, "Cassini |gamma - 1|", CASSINI_GAMMA_MINUS_1_BOUND),
        ("solar_neighborhood_midplane", rho_solar_nbhd, None, None),
        ("lab_water", DEFAULT_LAB_WATER_DENSITY_KG_M3, "MICROSCOPE (2022)", microscope_eta),
        ("lab_solid", lab_rho_val, "MICROSCOPE (2022)", microscope_eta),
    )

    regimes: dict[str, dict[str, object]] = {}
    for key, rho_val, bound_name, bound_val in regime_specs:
        entry = _eval_screening_law(rho_val, rho_crit, beta_val, bound_val)
        entry["bound_name"] = bound_name
        entry["bound_value"] = bound_val
        regimes[key] = entry

    diff_eotvos = {
        "microscope_ti_pt": _eval_differential_eotvos(
            4500.0, 21450.0, rho_crit, beta_val, microscope_eta
        ),
        "eot_wash_be_ti": _eval_differential_eotvos(
            1850.0, 4500.0, rho_crit, beta_val, eot_wash_eta
        ),
    }

    dg_proxy = (beta_val * fl1_proxy_val) / (1.0 - beta_val * fl1_proxy_val)
    dg_clock = (beta_val * fl1_clock_val) / (1.0 - beta_val * fl1_clock_val)

    exp_passes_core = bool(
        regimes["enclosed_1au_roche"]["exponential"]["passes_bound"]
        and regimes["local_1au_solar_wind"]["exponential"]["passes_bound"]
        and regimes["lab_water"]["exponential"]["passes_bound"]
        and regimes["lab_solid"]["exponential"]["passes_bound"]
        and diff_eotvos["microscope_ti_pt"]["exponential"]["passes_bound"]
        and diff_eotvos["eot_wash_be_ti"]["exponential"]["passes_bound"]
    )
    pow_passes_roche_and_lab = bool(
        regimes["enclosed_1au_roche"]["power_law"]["passes_bound"]
        and regimes["lab_water"]["power_law"]["passes_bound"]
        and regimes["lab_solid"]["power_law"]["passes_bound"]
    )
    pow_fails_local_1au = not bool(
        regimes["local_1au_solar_wind"]["power_law"]["passes_bound"]
    )
    local_40au_fails_both = (
        not bool(regimes["local_40au_solar_wind"]["exponential"]["passes_bound"])
        and not bool(regimes["local_40au_solar_wind"]["power_law"]["passes_bound"])
    )

    return {
        "inputs": {
            "sigma_crit": sigma_crit_val,
            "beta": beta_val,
            "scale_height_kpc": h_val,
            "thickness_factor": factor_val,
            "solar_wind_1au_kg_m3": sw_1au_val,
            "lab_density_kg_m3": lab_rho_val,
        },
        "rho_crit_kg_m3": rho_crit,
        "bounds": {
            "cassini_gamma_minus_1": {
                "value": CASSINI_GAMMA_MINUS_1_BOUND,
                "tag": "EXTERNAL_ANCHOR",
                "source": "Bertotti et al. 2003 (local constant; post_newtonian.py is retired)",
            },
            "microscope_eta": {
                "value": microscope_eta,
                "tag": "EXTERNAL_ANCHOR",
                "source": "det8.models.experimental_constraints.PUBLISHED_EOTVOS",
            },
            "eot_wash_eta": {
                "value": eot_wash_eta,
                "tag": "EXTERNAL_ANCHOR",
                "source": "det8.models.experimental_constraints.PUBLISHED_EOTVOS",
            },
            "llr_nordtvedt_eta": {
                "value": llr_eta,
                "tag": "EXTERNAL_ANCHOR",
                "source": "det8.models.experimental_constraints.PUBLISHED_EOTVOS",
            },
        },
        "regimes": regimes,
        "differential_eotvos": diff_eotvos,
        "summary": {
            "exponential_passes_roche_and_local_1au_and_lab": exp_passes_core,
            "power_law_passes_roche_and_lab": pow_passes_roche_and_lab,
            "power_law_fails_local_1au_solar_wind": pow_fails_local_1au,
            "local_40au_solar_wind_fails_both_forms": local_40au_fails_both,
        },
        "fl1_rank_separation": {
            "fl1_delta_kappa_proxy": fl1_proxy_val,
            "fl1_delta_kappa_clock": fl1_clock_val,
            "conflated_scalar_delta_G_over_G_proxy": dg_proxy,
            "conflated_scalar_delta_G_over_G_clock": dg_clock,
            "proxy_violation_factor_vs_microscope": dg_proxy / microscope_eta,
            "clock_violation_factor_vs_microscope": dg_clock / microscope_eta,
            "requires_rank_r_gt_1_separation": True,
            "resolution_summary": (
                "Per docs/record_kernel_physics.md §2.1 & §2.4, a rank-1 scalar kappa "
                "cannot simultaneously retain lab FL-1 contrasts (Delta_kappa_dev ~ 0.002-0.5) "
                "and satisfy MICROSCOPE (eta < 1.5e-15). Resolving both requires rank r > 1 "
                "channel separation between coarse-grained ambient kappa_env (screened to ~0 "
                "for rho >> rho_crit) and isolated device micro-history kappa_dev."
            ),
        },
        "theoretical_caveats": [
            (
                "Missing covariant action: substituting G_eff(r) directly into circular-orbit "
                "kinematics lacks a field-theoretic Lagrangian/Poisson PDE and kappa stress-energy."
            ),
            (
                "Newton's 3rd law asymmetry: two bodies with unequal local G_eff exert unequal "
                "forces unless derived from a symmetric conservative potential."
            ),
            (
                "Roche density non-locality: M_enc(<r)/(4/3 pi r^3) depends on a chosen origin "
                "and radius rather than a covariant local field quantity."
            ),
            (
                "Unmodeled PPN gamma and lensing: scalar G_eff(r) provides no relativistic metric "
                "tensor g_munu, so Shapiro delay and gravitational lensing remain un-derived."
            ),
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# Two-Tier Refutation / Acceptance Criteria Evaluator
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_pathway1_criteria(
    *,
    sigma_crit: float = DEFAULT_SIGMA_CRIT,
    beta: float = DEFAULT_BETA,
    w_sfr: float = 0.0,
    gas_mode: str = "1d",
    scale_height_kpc: float = DEFAULT_DISK_SCALE_HEIGHT_KPC,
    has_covariant_lensing_action: bool = False,
    has_full_radial_sparc_profiles: bool = False,
) -> dict[str, object]:
    """Compute Pathway 1 viability verdict from two-tier non-hardcoded criteria."""
    sigma_crit_val = _validate_positive_finite("sigma_crit", sigma_crit)
    beta_val = _validate_half_open_unit("beta", beta)
    w_sfr_val = _validate_non_negative_finite("w_sfr", w_sfr)
    mode = _validate_gas_mode(gas_mode)
    h_val = _validate_positive_finite("scale_height_kpc", scale_height_kpc)
    has_lensing = _validate_bool_flag(
        "has_covariant_lensing_action", has_covariant_lensing_action
    )
    has_profiles = _validate_bool_flag(
        "has_full_radial_sparc_profiles", has_full_radial_sparc_profiles
    )

    f6_res = evaluate_f6_sign_check(sigma_crit=sigma_crit_val, w_sfr=w_sfr_val)
    sparc_res = evaluate_sparc_fit(
        sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
    )
    asym_res = evaluate_radial_asymptotics(
        sigma_crit=sigma_crit_val, beta=beta_val, gas_mode=mode
    )
    screen_res = evaluate_screening_constraints(
        sigma_crit=sigma_crit_val, beta=beta_val, scale_height_kpc=h_val
    )

    dwarf_mean_err = float(sparc_res["mass_bins"]["dwarf"]["mean_error"])
    max_enh = float(sparc_res["max_enhancement"])
    sparc_mean_err = float(sparc_res["mean_error"])
    sparc_w20_frac = float(sparc_res["within_20_fraction"])

    regimes = screen_res["regimes"]
    diff_eotvos = screen_res["differential_eotvos"]
    exp_screen_passed = bool(
        regimes["enclosed_1au_roche"]["exponential"]["passes_bound"]
        and regimes["local_1au_solar_wind"]["exponential"]["passes_bound"]
        and regimes["lab_solid"]["exponential"]["passes_bound"]
        and diff_eotvos["microscope_ti_pt"]["exponential"]["passes_bound"]
    )

    core_gates: dict[str, dict[str, object]] = {
        "f6_monotonicity": {
            "passed": bool(f6_res["all_increasing"] and f6_res["all_monotonic"]),
            "metric": f"{f6_res['n_increasing']}/{f6_res['n_total']} increasing",
            "threshold": "8/8 strictly monotonic increasing on KNOWN_GALAXIES",
        },
        "r6b_ceiling_and_dwarf": {
            "passed": (max_enh > 9.0) and (dwarf_mean_err <= 0.30),
            "max_enhancement": max_enh,
            "dwarf_mean_error": dwarf_mean_err,
            "threshold": "max_enhancement > 9.0x and dwarf_mean_error <= 0.30",
        },
        "sparc_outer_point_fit": {
            "passed": (sparc_mean_err <= 0.25) and (sparc_w20_frac >= 0.50),
            "mean_error": sparc_mean_err,
            "within_20_fraction": sparc_w20_frac,
            "threshold": "mean_error <= 0.25 and within_20_fraction >= 0.50",
        },
        "r6a_exponential_screening": {
            "passed": exp_screen_passed,
            "enclosed_1au_delta_G_over_G": regimes["enclosed_1au_roche"]["exponential"][
                "delta_G_over_G"
            ],
            "local_1au_delta_G_over_G": regimes["local_1au_solar_wind"]["exponential"][
                "delta_G_over_G"
            ],
            "lab_solid_delta_G_over_G": regimes["lab_solid"]["exponential"][
                "delta_G_over_G"
            ],
            "threshold": "exponential delta_G/G < Cassini (2.3e-5) and MICROSCOPE (1.5e-15)",
        },
    }

    far_outer_slope_mean = float(
        asym_res["regime_summaries"]["outer_2_to_4_rmax"]["mean_slope"]
    )
    known_mean_err = float(
        sparc_res["known_galaxies_comparison"]["at_max_5rd_8kpc"]["mean_error"]
    )
    pow_local_1au_passes = bool(
        regimes["local_1au_solar_wind"]["power_law"]["passes_bound"]
    )
    fl1_sep_documented = bool(
        screen_res["fl1_rank_separation"]["requires_rank_r_gt_1_separation"]
    )

    limitation_checks: dict[str, dict[str, object]] = {
        "asymptotic_flatness_maintained": {
            "passed": far_outer_slope_mean >= -0.15,
            "observed": far_outer_slope_mean,
            "threshold": "outer [2*r_max, 4*r_max] mean d ln v / d ln r >= -0.15",
            "note": "Pathway 1 turns over to Keplerian r^(-1/2) (slope ~ -0.5) once kappa -> 1.",
        },
        "known_galaxies_velocity_match": {
            "passed": known_mean_err <= 0.25,
            "observed": known_mean_err,
            "threshold": "KNOWN_GALAXIES mean_error <= 0.25 at max(5*r_d, 8.0)",
            "note": "Discrepancy driven by up to 11.54x M_star differences vs SAMPLE_GALAXIES.",
        },
        "power_law_local_1au_screening": {
            "passed": pow_local_1au_passes,
            "observed": regimes["local_1au_solar_wind"]["power_law"]["delta_G_over_G"],
            "threshold": "power-law delta_G/G < 2.3e-5 at local 1 AU solar wind",
            "note": "Power-law screening fails Cassini at local 1 AU (~729x over); exponential is required.",
        },
        "full_sparc_radial_profiles_tested": {
            "passed": has_profiles,
            "observed": has_profiles,
            "threshold": "Full radial rotation curves evaluated beyond single-point r_max",
        },
        "covariant_metric_and_lensing_closed": {
            "passed": has_lensing,
            "observed": has_lensing,
            "threshold": "Covariant action, momentum conservation, and PPN gamma = 1 lensing derived",
        },
        "fl1_rank_separation_documented": {
            "passed": fl1_sep_documented,
            "observed": fl1_sep_documented,
            "threshold": "Rank r > 1 separation (kappa_env vs kappa_dev) explicitly recorded",
        },
    }

    if not all(bool(gate["passed"]) for gate in core_gates.values()):
        status = "REFUTED"
    elif all(bool(check["passed"]) for check in limitation_checks.values()):
        status = "VIABLE_PROVISIONAL"
    else:
        status = "PARTIAL_LIMITATION"

    passing_checks = [
        *[f"core:{k}" for k, v in core_gates.items() if v["passed"]],
        *[f"limitation:{k}" for k, v in limitation_checks.items() if v["passed"]],
    ]
    failing_checks = [
        *[f"core:{k}" for k, v in core_gates.items() if not v["passed"]],
        *[f"limitation:{k}" for k, v in limitation_checks.items() if not v["passed"]],
    ]
    open_limitations = [
        k for k, v in limitation_checks.items() if not v["passed"]
    ]

    return {
        "status": status,
        "parameters": {
            "sigma_crit": sigma_crit_val,
            "beta": beta_val,
            "w_sfr": w_sfr_val,
            "gas_mode": mode,
            "scale_height_kpc": h_val,
        },
        "core_gates": core_gates,
        "limitation_checks": limitation_checks,
        "passing_checks": passing_checks,
        "failing_checks": failing_checks,
        "open_limitations": open_limitations,
        "summary": {
            "core_passed_count": sum(1 for v in core_gates.values() if v["passed"]),
            "core_total_count": len(core_gates),
            "limitation_passed_count": sum(
                1 for v in limitation_checks.values() if v["passed"]
            ),
            "limitation_total_count": len(limitation_checks),
        },
        "sub_evaluations": {
            "f6": f6_res,
            "sparc": sparc_res,
            "asymptotics": asym_res,
            "screening": screen_res,
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# Native vs. Fitted / Correspondence / External Anchor Manifest
# ═══════════════════════════════════════════════════════════════════════════


def closure_manifest() -> list[dict[str, object]]:
    """Return epistemic provenance manifest for all Pathway 1 equations and constants."""
    mond_sigma_kg_m2 = MOND_A0_M_S2 / (2.0 * math.pi * G_SI)
    mond_sigma_1e9_msun_kpc2 = mond_sigma_kg_m2 * (KPC_TO_M ** 2) / (1e9 * M_SUN_KG)
    mond_ratio = mond_sigma_1e9_msun_kpc2 / DEFAULT_SIGMA_CRIT

    return [
        {
            "id": "t1_markov_contraction",
            "symbol_or_equation": "kappa_n <= eta^n * kappa_0 = exp(-N_int / N_rec)",
            "tag": "TH-DET",
            "anchoring_level": "Level 3 (TH-DET)",
            "is_native_det": True,
            "value_or_domain": "kappa in (0, 1]",
            "units": "dimensionless",
            "calibration_dataset_or_source": "docs/record_kernel_physics.md §2.4 (T1 Fisher-Rao contraction)",
            "native_derivation_opportunity": (
                "Derive Dobrushin contraction coefficient eta < 1 directly from the discrete "
                "commit-channel transition kernel T without continuum surface-density fitting."
            ),
            "known_limitations_or_gaps": (
                "T1 guarantees exponential contraction in abstract interaction count N_int/N_rec, "
                "but does not itself determine how N_int maps to astrophysical baryonic mass."
            ),
        },
        {
            "id": "baryon_commit_bridge",
            "symbol_or_equation": "N_int(r)/N_rec := (Sigma_*(r) + Sigma_gas(r))/Sigma_crit + w_SFR * Sigma_SFR(r)",
            "tag": "CORR",
            "anchoring_level": "Level 3 (CORR)",
            "is_native_det": False,
            "value_or_domain": ">= 0",
            "units": "dimensionless",
            "calibration_dataset_or_source": "Coarse-grained correspondence over Freeman (1970) surface densities",
            "native_derivation_opportunity": (
                "Model local commit cross-section per dynamical/Hubble time from baryon scattering "
                "rates in a DET record lattice."
            ),
            "known_limitations_or_gaps": (
                "Postulated additive surface-density proxy; does not distinguish 3D volume density "
                "from 2D projected column density without a disk-thickness ansatz."
            ),
        },
        {
            "id": "sigma_crit",
            "symbol_or_equation": "Sigma_crit",
            "tag": "FIT",
            "anchoring_level": "Level 3 (FIT)",
            "is_native_det": False,
            "value_or_domain": DEFAULT_SIGMA_CRIT,
            "units": "10^9 M_sun / kpc^2",
            "calibration_dataset_or_source": "SAMPLE_GALAXIES (43 SPARC galaxies at r_max)",
            "native_derivation_opportunity": (
                f"Compare commit surface-density scale against MOND a_0/(2*pi*G) = "
                f"{mond_sigma_1e9_msun_kpc2:.5f} x 10^9 M_sun/kpc^2 ({mond_ratio:.2f}x larger than "
                f"Sigma_crit={DEFAULT_SIGMA_CRIT}); deriving Sigma_crit natively would require "
                "relating N_rec to G, c, and H_0."
            ),
            "known_limitations_or_gaps": (
                "Empirical fit parameter; differs by ~17.1x from MOND critical surface density "
                "because exponential Sigma(r) decays faster than Newtonian g_N(r) ~ 1/r^2."
            ),
        },
        {
            "id": "w_sfr",
            "symbol_or_equation": "w_SFR",
            "tag": "FIT",
            "anchoring_level": "Level 3 (FIT)",
            "is_native_det": False,
            "value_or_domain": "0.0 (SPARC default); 0.5 (exploratory F6 check)",
            "units": "yr * kpc^2 / M_sun",
            "calibration_dataset_or_source": "Exploratory setting on KNOWN_GALAXIES (uncalibrated on SAMPLE_GALAXIES)",
            "native_derivation_opportunity": (
                "Relate active star-formation reset rate to commit-event branching ratio in "
                "high-dissipation astrophysical environments."
            ),
            "known_limitations_or_gaps": (
                "SAMPLE_GALAXIES omits SFR and r_SFR; on KNOWN_GALAXIES w_SFR=0.5 changes "
                "rotation velocities by <0.1% at outer radii."
            ),
        },
        {
            "id": "reciprocal_aperture_coupling",
            "symbol_or_equation": "G_eff(r) = G / (1 - beta * kappa(r)) = G * sum_{m=0}^inf (beta * kappa(r))^m",
            "tag": "FIT",
            "anchoring_level": "Level 3 (FIT)",
            "is_native_det": False,
            "value_or_domain": "[G, G / (1 - beta))",
            "units": "m^3 / (kg * s^2)",
            "calibration_dataset_or_source": "Analogical inverse-aperture closure fitted to SAMPLE_GALAXIES",
            "native_derivation_opportunity": (
                "Admits a perturbative geometric-series interpretation sum_{m=0}^inf (beta*kappa)^m "
                "of unscreened participation feedback modes, contrasting det8_core.participation_aperture "
                "(1 + lambda_P * kappa)^(-1) which decreases with kappa."
            ),
            "known_limitations_or_gaps": (
                "Algebraic rotation-curve closure without a covariant action, Poisson PDE, "
                "momentum-conservation proof, or PPN gamma lensing metric."
            ),
        },
        {
            "id": "beta",
            "symbol_or_equation": "beta",
            "tag": "FIT",
            "anchoring_level": "Level 3 (FIT)",
            "is_native_det": False,
            "value_or_domain": f"{DEFAULT_BETA} (domain [0, 1))",
            "units": "dimensionless",
            "calibration_dataset_or_source": "SAMPLE_GALAXIES (43 SPARC galaxies at r_max)",
            "native_derivation_opportunity": (
                "Identify beta as an effective single-step susceptibility in the participation-aperture "
                "geometric series if derived from lattice Green's functions."
            ),
            "known_limitations_or_gaps": (
                f"Caps maximum enhancement at 1/(1 - beta) = {1.0/(1.0 - DEFAULT_BETA):.2f}x; "
                "pushing beta to 0.97-0.98 for 33-50x enhancement degrades SPARC mean error."
            ),
        },
        {
            "id": "disk_thickness_h_kpc",
            "symbol_or_equation": "rho_crit = Sigma_crit_SI / (thickness_factor * h_kpc * KPC_TO_M)",
            "tag": "CORR",
            "anchoring_level": "Level 3 (CORR)",
            "is_native_det": False,
            "value_or_domain": f"{DEFAULT_DISK_SCALE_HEIGHT_KPC} kpc (thickness_factor=1.0)",
            "units": "kpc",
            "calibration_dataset_or_source": "Nominal spiral-disk scale height bridging 2D Sigma_crit to 3D rho_crit",
            "native_derivation_opportunity": (
                "Replace 2D/3D slab bridge with an intrinsic 3D local commit-density or gravitational "
                "potential threshold."
            ),
            "known_limitations_or_gaps": (
                "Factor-of-2 convention ambiguity (slab h vs exponential 2h) and non-locality when "
                "comparing Roche enclosed density to local solar-wind density."
            ),
        },
        {
            "id": "external_anchors",
            "symbol_or_equation": "G_SI, C_SI, M_SUN_KG, KPC_TO_M, AU_M, Cassini, MICROSCOPE, Eot-Wash, LLR",
            "tag": "EXTERNAL_ANCHOR",
            "anchoring_level": "Level 2",
            "is_native_det": False,
            "value_or_domain": "SI constants & published experimental upper bounds",
            "units": "SI / dimensionless",
            "calibration_dataset_or_source": (
                "det8.models.galaxy_observables, det8.models.experimental_constraints.PUBLISHED_EOTVOS, "
                "and IAU/Bertotti et al. 2003 constants"
            ),
            "native_derivation_opportunity": "None — empirical external standards and null-experiment bounds.",
            "known_limitations_or_gaps": (
                "experimental_constraints.py strings are literature transcriptions rather than "
                "raw instrument data ingests."
            ),
        },
        {
            "id": "freeman_keplerian_kinematics",
            "symbol_or_equation": "v(r) = sqrt(G_eff(r) * M_bar(<r) / r)",
            "tag": "CORR",
            "anchoring_level": "Level 3 (CORR)",
            "is_native_det": False,
            "value_or_domain": "r > 0 kpc; gas_mode in {'1d', 'freeman_2d'}",
            "units": "km/s",
            "calibration_dataset_or_source": "Freeman (1970) exponential disk & Newtonian circular-orbit kinematics",
            "native_derivation_opportunity": (
                "Would require deriving the non-Keplerian outer potential from a dynamical field "
                "equation if asymptotic flatness is to be maintained beyond r_max."
            ),
            "known_limitations_or_gaps": (
                "Predicts universal Keplerian r^(-1/2) decline once kappa(r) -> 1 and M_bar(<r) "
                "saturates."
            ),
        },
    ]


__all__ = (
    "AU_M",
    "CASSINI_GAMMA_MINUS_1_BOUND",
    "C_SI",
    "DEFAULT_BETA",
    "DEFAULT_DISK_SCALE_HEIGHT_KPC",
    "DEFAULT_LAB_SOLID_DENSITY_KG_M3",
    "DEFAULT_LAB_WATER_DENSITY_KG_M3",
    "DEFAULT_SIGMA_CRIT",
    "DEFAULT_SOLAR_WIND_1AU_KG_M3",
    "G_SI",
    "KM_S_TO_M_S",
    "KPC_TO_M",
    "MOND_A0_M_S2",
    "M_SUN_KG",
    "closure_manifest",
    "evaluate_f6_sign_check",
    "evaluate_pathway1_criteria",
    "evaluate_radial_asymptotics",
    "evaluate_screening_constraints",
    "evaluate_sparc_fit",
    "pathway1_rotation_velocity",
    "reciprocal_aperture_g_eff",
    "sigma_crit_to_rho_crit",
    "t1_contraction_kappa",
)
