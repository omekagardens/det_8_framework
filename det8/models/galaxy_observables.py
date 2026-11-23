"""Empirical galaxy observables, unit constants, and baseline disk geometry.

This module provides neutral Level-2 empirical galaxy datasets (extracted
without gravitational-theory assumptions) and Level-3 borrowed Freeman (1970)
/ Newtonian baseline geometry helpers for DET8 evaluations.

It makes zero DET gravitational claims, carries ``NEUTRAL_DATA_FIXTURE``
status with zero ``DG-WARRANT`` impact, and imports no retired or quarantined
gravity modules.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from det8.models.reference_constants import NEWTONIAN_G_SI


# ═══════════════════════════════════════════════════════════════════════════
# Physical & Unit Conversion Constants (External Empirical / SI Anchors)
# ═══════════════════════════════════════════════════════════════════════════

G_SI: Final[float] = NEWTONIAN_G_SI       # 6.67430e-11 m^3 / (kg * s^2)
C_SI: Final[float] = 2.99792458e8         # m / s (matches det_units.py / post_newtonian.py)
M_SUN_KG: Final[float] = 1.989e30         # kg (solar mass)
KPC_TO_M: Final[float] = 3.086e19         # m per kiloparsec
KM_S_TO_M_S: Final[float] = 1000.0        # m/s per km/s

DEFAULT_SPARC_SUBSET_PATH: Final[Path] = (
    Path(__file__).resolve().parents[1] / "data" / "sparc_subset.json"
)


# ═══════════════════════════════════════════════════════════════════════════
# Provenance & Observable-Anchoring Metadata
# ═══════════════════════════════════════════════════════════════════════════

OBSERVABLE_PROVENANCE: Final[dict[str, object]] = {
    "epistemic_level": (
        "Level-2 derived empirical quantity (datasets); "
        "Level-3 borrowed conventional representation (Freeman 1970 / Newtonian baselines)"
    ),
    "origin_theory": (
        "ΛCDM / observational astrophysics "
        "(SPARC: Lelli, McGaugh & Schombert 2016, AJ, 152, 157)"
    ),
    "admissible_quantities": (
        "v_flat",
        "M_star",
        "M_gas",
        "r_d",
        "r_gas",
        "r_SFR",
        "r_max",
        "SFR",
        "age",
    ),
    "quarantined_derived_quantities": (
        "dark-matter halo profile (ΛCDM-dependent)",
    ),
    "guardrail_rule": (
        "Use ONLY observed/empirical quantities under declared observational "
        "reductions; do not claim Level-2 parameters as Level-1 raw records or "
        "DET derivations, and do not import ΛCDM halo interpretations."
    ),
    "det_claim_status": "NEUTRAL_DATA_FIXTURE",
    "dg_warrant_impact": "none — neutral data & geometry fixture; not a registered falsifiable probe",
    "reference_constants_source": "det8.models.reference_constants.NEWTONIAN_G_SI",
    "dataset_discrepancy_caveat": (
        "KNOWN_GALAXIES (8) and det8/data/sparc_subset.json (56) agree within <=2% "
        "in M_star on all 5 shared galaxies, whereas SAMPLE_GALAXIES (43) differs "
        "in M_star by up to 39.1x vs sparc_subset.json (17 overlaps) and up to "
        "11.5x vs KNOWN_GALAXIES (8 overlaps). All three fixtures are preserved "
        "verbatim for parity and cross-audit without silent merging."
    ),
}


# ═══════════════════════════════════════════════════════════════════════════
# Galaxy Observable Data Structures
# ═══════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True, slots=True)
class GalaxyObservables:
    """Observed galaxy properties including SFR and stellar-disk scales."""

    name: str
    M_star: float          # Total stellar mass (10^9 M_sun).
    r_d: float             # Stellar disk scale length (kpc).
    M_gas: float           # Total gas mass (10^9 M_sun).
    r_gas: float           # Gas disk scale length (kpc).
    SFR: float             # Total star formation rate (M_sun/yr).
    r_SFR: float           # SFR scale length (kpc). Typically > r_d.
    age: float = 10.0      # Galaxy age (Gyr).
    V_flat: float = 0.0    # Observed flat velocity (km/s).


@dataclass(frozen=True, slots=True)
class GalaxyParams:
    """Representative SPARC galaxy parameters (Lelli et al. 2016)."""

    name: str
    M_star: float     # Stellar mass (10^9 M_sun).
    r_d: float        # Disk scale length (kpc).
    M_gas: float      # HI gas mass (10^9 M_sun).
    r_gas: float      # Gas scale length (kpc).
    v_flat: float     # Observed flat rotation velocity (km/s).
    r_max: float      # Maximum radius with data (kpc).


# ═══════════════════════════════════════════════════════════════════════════
# Empirical Datasets (Verbatim Fixtures)
# ═══════════════════════════════════════════════════════════════════════════

KNOWN_GALAXIES: list[GalaxyObservables] = [
    GalaxyObservables("NGC 2403", 3.2, 1.4, 2.5, 3.0, SFR=1.2, r_SFR=2.5, age=10.0, V_flat=131),
    GalaxyObservables("NGC 3198", 10.9, 3.1, 5.0, 6.0, SFR=2.0, r_SFR=5.0, age=10.0, V_flat=150),
    GalaxyObservables("NGC 2841", 9.8, 3.6, 8.5, 8.0, SFR=0.5, r_SFR=6.0, age=11.0, V_flat=285),
    GalaxyObservables("NGC 7331", 11.1, 5.0, 9.0, 7.0, SFR=3.0, r_SFR=8.0, age=10.0, V_flat=239),
    GalaxyObservables("NGC 5055", 11.7, 3.2, 8.0, 8.0, SFR=2.5, r_SFR=5.5, age=10.0, V_flat=179),
    GalaxyObservables("DDO 154", 0.28, 0.37, 0.25, 1.0, SFR=0.005, r_SFR=1.0, age=12.0, V_flat=47),
    GalaxyObservables("NGC 6503", 1.7, 2.2, 0.8, 2.5, SFR=0.4, r_SFR=3.5, age=10.0, V_flat=116),
    GalaxyObservables("NGC 2903", 2.6, 2.3, 2.5, 3.0, SFR=1.5, r_SFR=4.0, age=10.0, V_flat=185),
]


SAMPLE_GALAXIES: list[GalaxyParams] = [
    # Dwarf galaxies (M_star < 1e9 M_sun)
    GalaxyParams("DDO 154", 0.05, 0.5, 0.25, 1.0, 48, 8),
    GalaxyParams("DDO 170", 0.3, 1.1, 0.6, 2.0, 66, 15),
    GalaxyParams("DDO 52", 0.5, 1.2, 0.8, 2.5, 70, 10),
    GalaxyParams("DDO 161", 0.3, 0.8, 0.4, 1.5, 52, 10),
    GalaxyParams("NGC 3741", 0.05, 0.3, 0.1, 0.6, 44, 8),
    GalaxyParams("UGC 07577", 0.4, 1.0, 1.0, 2.5, 65, 12),
    GalaxyParams("UGC 128", 1.0, 1.5, 3.0, 4.0, 132, 25),
    GalaxyParams("IC 2574", 1.0, 2.0, 1.5, 5.0, 68, 12),
    GalaxyParams("NGC 2366", 0.1, 1.5, 0.8, 3.0, 55, 10),
    # Low-mass spirals (1-10e9 M_sun)
    GalaxyParams("NGC 6503", 1.4, 1.2, 0.8, 2.5, 115, 22),
    GalaxyParams("NGC 2403", 7.0, 1.8, 2.5, 3.0, 135, 20),
    GalaxyParams("NGC 5585", 0.8, 1.3, 0.7, 3.0, 90, 12),
    GalaxyParams("NGC 3198", 9.0, 3.0, 5.0, 6.0, 150, 30),
    GalaxyParams("NGC 3109", 0.3, 1.2, 0.4, 2.0, 67, 12),
    GalaxyParams("NGC 4214", 0.3, 0.9, 0.6, 2.0, 80, 8),
    GalaxyParams("NGC 7793", 3.0, 1.5, 1.5, 3.0, 115, 15),
    GalaxyParams("NGC 300", 1.5, 1.5, 1.0, 3.0, 90, 15),
    GalaxyParams("NGC 247", 3.0, 3.0, 2.0, 5.0, 105, 20),
    # Intermediate spirals (10-50e9 M_sun)
    GalaxyParams("NGC 5055", 30.0, 3.5, 8.0, 8.0, 190, 40),
    GalaxyParams("NGC 2841", 46.0, 4.0, 8.5, 8.0, 290, 50),
    GalaxyParams("NGC 7331", 55.0, 3.5, 9.0, 7.0, 240, 35),
    GalaxyParams("NGC 2903", 30.0, 2.5, 5.0, 6.0, 200, 30),
    GalaxyParams("NGC 3521", 40.0, 3.0, 7.0, 6.0, 235, 35),
    GalaxyParams("NGC 6946", 25.0, 3.0, 6.0, 8.0, 210, 25),
    GalaxyParams("NGC 3621", 13.0, 2.5, 7.0, 5.0, 150, 20),
    GalaxyParams("NGC 5033", 35.0, 5.0, 6.0, 9.0, 220, 40),
    GalaxyParams("UGC 02953", 20.0, 3.5, 27.0, 8.0, 130, 30),
    # Massive spirals (M_star > 50e9 M_sun)
    GalaxyParams("NGC 3992", 50.0, 5.0, 3.0, 10.0, 270, 45),
    GalaxyParams("NGC 5371", 60.0, 4.5, 10.0, 9.0, 270, 40),
    GalaxyParams("NGC 5907", 80.0, 5.5, 12.0, 12.0, 240, 40),
    GalaxyParams("NGC 4013", 70.0, 4.0, 5.0, 8.0, 190, 35),
    GalaxyParams("NGC 0891", 70.0, 5.0, 10.0, 10.0, 230, 40),
    GalaxyParams("NGC 7814", 90.0, 4.5, 3.0, 8.0, 230, 35),
    GalaxyParams("NGC 2683", 55.0, 3.0, 3.0, 6.0, 195, 30),
    GalaxyParams("NGC 3953", 60.0, 5.0, 4.0, 9.0, 220, 40),
    # Gas-dominated galaxies
    GalaxyParams("UGC 06917", 0.3, 1.0, 2.0, 3.0, 80, 15),
    GalaxyParams("F563-V2", 0.2, 1.0, 0.5, 2.0, 55, 10),
    GalaxyParams("F568-3", 0.8, 1.5, 2.0, 4.0, 105, 18),
    GalaxyParams("F583-1", 1.5, 2.0, 3.0, 5.0, 87, 20),
    GalaxyParams("UGC 05721", 2.0, 2.5, 8.0, 6.0, 135, 28),
    GalaxyParams("NGC 0024", 3.0, 1.8, 2.5, 4.0, 110, 18),
    GalaxyParams("NGC 4183", 4.0, 2.5, 3.0, 6.0, 115, 25),
    GalaxyParams("NGC 4217", 5.0, 2.0, 1.5, 4.0, 180, 22),
]


# ═══════════════════════════════════════════════════════════════════════════
# Level-3 Geometry & Newtonian Baseline Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _validate_non_negative_finite(name: str, value: float) -> None:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be finite and >= 0, got {value!r}")
    try:
        is_fin = math.isfinite(value)
    except OverflowError as exc:
        raise ValueError(f"{name} must be finite and >= 0, got {value!r}") from exc
    if not is_fin or value < 0.0:
        raise ValueError(f"{name} must be finite and >= 0, got {value!r}")


def stellar_surface_density(r_kpc: float, M_star: float, r_d: float) -> float:
    """Exponential disk surface mass density Σ(r) = M · exp(-r/r_d) / (2π r_d^2) [10^9 M_sun/kpc^2]."""
    _validate_non_negative_finite("r_kpc", r_kpc)
    _validate_non_negative_finite("M_star", M_star)
    _validate_non_negative_finite("r_d", r_d)
    if r_d == 0.0 or M_star == 0.0:
        return 0.0
    if r_d > 1e150 or r_d < 1e-150:
        return (M_star / (2.0 * math.pi)) * math.exp(-r_kpc / r_d) / r_d / r_d
    return M_star * math.exp(-r_kpc / r_d) / (2.0 * math.pi * r_d**2)


def sfr_surface_density(r_kpc: float, SFR: float, r_SFR: float) -> float:
    """Exponential SFR surface density Σ_SFR(r) = SFR · exp(-r/r_SFR) / (2π r_SFR^2) [M_sun/yr/kpc^2]."""
    _validate_non_negative_finite("r_kpc", r_kpc)
    _validate_non_negative_finite("SFR", SFR)
    _validate_non_negative_finite("r_SFR", r_SFR)
    if r_SFR == 0.0 or SFR == 0.0:
        return 0.0
    if r_SFR > 1e150 or r_SFR < 1e-150:
        return (SFR / (2.0 * math.pi)) * math.exp(-r_kpc / r_SFR) / r_SFR / r_SFR
    return SFR * math.exp(-r_kpc / r_SFR) / (2.0 * math.pi * r_SFR**2)


def stellar_disk_mass(r_kpc: float, M_star: float, r_d: float) -> float:
    """Freeman (1970) 2D exponential disk mass enclosed within r_kpc [10^9 M_sun].

    Preserves the intentional ``x < 0.01 -> M_star * (0.5 * x**2)`` small-radius
    branch from ``sparc_analysis.stellar_disk_mass`` for exact legacy parity
    (which introduces a ~0.67% step at ``x = r_kpc / r_d = 0.01``).
    """
    _validate_non_negative_finite("r_kpc", r_kpc)
    _validate_non_negative_finite("M_star", M_star)
    _validate_non_negative_finite("r_d", r_d)
    if r_d == 0.0 or M_star == 0.0 or r_kpc == 0.0:
        return 0.0
    x = r_kpc / r_d
    if math.isinf(x) or x > 750.0:
        return float(M_star)
    if x < 0.01:
        return M_star * (0.5 * x**2)
    return M_star * (1.0 - (1.0 + x) * math.exp(-x))


def gas_mass_exponential_1d(r_kpc: float, M_gas: float, r_gas: float) -> float:
    """1D radial exponential gas mass M_gas · (1 - exp(-r/r_gas)) [10^9 M_sun]."""
    _validate_non_negative_finite("r_kpc", r_kpc)
    _validate_non_negative_finite("M_gas", M_gas)
    _validate_non_negative_finite("r_gas", r_gas)
    if r_gas == 0.0 or M_gas == 0.0 or r_kpc == 0.0:
        return 0.0
    x = r_kpc / r_gas
    if x < 1e-4:
        return -M_gas * math.expm1(-x)
    return M_gas * (1.0 - math.exp(-x))


def gas_mass_freeman_2d(r_kpc: float, M_gas: float, r_gas: float) -> float:
    """Consistent 2D Freeman disk integral M_gas · (1 - (1 + r/r_gas) * exp(-r/r_gas)) [10^9 M_sun]."""
    _validate_non_negative_finite("r_kpc", r_kpc)
    _validate_non_negative_finite("M_gas", M_gas)
    _validate_non_negative_finite("r_gas", r_gas)
    if r_gas == 0.0 or M_gas == 0.0 or r_kpc == 0.0:
        return 0.0
    x = r_kpc / r_gas
    if math.isinf(x) or x > 750.0:
        return float(M_gas)
    if x < 1e-4:
        return M_gas * (0.5 * x**2 - x**3 / 3.0 + x**4 / 8.0)
    return M_gas * (-math.expm1(-x) - x * math.exp(-x))


def newton_rotation_velocity(
    r_kpc: float,
    M_star: float,
    r_d: float,
    M_gas: float = 0.0,
    r_gas: float = 0.0,
    *,
    gas_mode: str = "1d",
) -> float:
    """Standard Newtonian circular velocity (km/s) from enclosed baryonic disk mass."""
    if isinstance(r_kpc, bool):
        raise ValueError(f"r_kpc must be finite and > 0, got {r_kpc!r}")
    try:
        r_fin = math.isfinite(r_kpc)
    except OverflowError as exc:
        raise ValueError(f"r_kpc must be finite and > 0, got {r_kpc!r}") from exc
    if not r_fin or r_kpc <= 0.0:
        raise ValueError(f"r_kpc must be finite and > 0, got {r_kpc!r}")
    _validate_non_negative_finite("M_star", M_star)
    _validate_non_negative_finite("r_d", r_d)
    _validate_non_negative_finite("M_gas", M_gas)
    _validate_non_negative_finite("r_gas", r_gas)

    if gas_mode == "1d":
        m_gas = gas_mass_exponential_1d(r_kpc, M_gas, r_gas)
    elif gas_mode == "freeman_2d":
        m_gas = gas_mass_freeman_2d(r_kpc, M_gas, r_gas)
    else:
        raise ValueError(f"Invalid gas_mode {gas_mode!r}; expected '1d' or 'freeman_2d'")

    m_bar = stellar_disk_mass(r_kpc, M_star, r_d) + m_gas
    m_bar_kg = m_bar * 1e9 * M_SUN_KG
    r_m = r_kpc * KPC_TO_M
    v_sq = G_SI * m_bar_kg / r_m
    if not math.isfinite(v_sq) or v_sq < 0.0:
        raise ValueError(f"Non-finite or negative squared velocity v_sq={v_sq!r}")
    return math.sqrt(v_sq) / KM_S_TO_M_S


MOND_A0_DEFAULT_M_S2: Final[float] = 1.2e-10  # Milgrom / RAR acceleration scale [m/s^2]


def mond_rotation_velocity(
    r_kpc: float,
    M_star: float,
    r_d: float,
    M_gas: float = 0.0,
    r_gas: float = 0.0,
    *,
    a0: float = MOND_A0_DEFAULT_M_S2,
    gas_mode: str = "1d",
) -> float:
    """Standard RAR/MOND circular velocity (km/s) using identical baryonic disk inputs.

    Uses the McGaugh, Lelli & Schombert (2016) Radial Acceleration Relation
    interpolating function ``g_obs = g_bar / (1 - exp(-sqrt(g_bar / a0)))`` on
    the exact same enclosed baryonic mass ``M_bar(<r)`` as ``newton_rotation_velocity``.
    """
    if isinstance(a0, bool):
        raise ValueError(f"a0 must be finite and > 0, got {a0!r}")
    try:
        a0_fin = math.isfinite(a0)
    except OverflowError as exc:
        raise ValueError(f"a0 must be finite and > 0, got {a0!r}") from exc
    if not a0_fin or a0 <= 0.0:
        raise ValueError(f"a0 must be finite and > 0, got {a0!r}")

    v_n_kms = newton_rotation_velocity(
        r_kpc, M_star, r_d, M_gas, r_gas, gas_mode=gas_mode
    )
    if v_n_kms == 0.0:
        return 0.0
    v_n_ms = v_n_kms * KM_S_TO_M_S
    r_m = r_kpc * KPC_TO_M
    g_n = (v_n_ms ** 2) / r_m
    if g_n <= 0.0:
        return 0.0
    x = math.sqrt(g_n / a0)
    denom = -math.expm1(-x)
    g_obs = (g_n / denom) if denom > 0.0 else g_n
    return math.sqrt(g_obs * r_m) / KM_S_TO_M_S


@dataclass(frozen=True, slots=True)
class GalaxyRadialProfile:
    """Held-out galaxy with full radial rotation curve points (strictly disjoint from SAMPLE_GALAXIES)."""

    name: str
    M_star: float                              # Stellar mass (10^9 M_sun).
    r_d: float                                 # Stellar disk scale length (kpc).
    M_gas: float                               # HI gas mass (10^9 M_sun).
    r_gas: float                               # Gas disk scale length (kpc).
    v_flat: float                              # Asymptotic flat velocity (km/s).
    r_max: float                               # Outermost measured radius (kpc).
    r_bend_obs_kpc: float                      # Observed knee/bend radius where curve flattens (kpc).
    radial_points: tuple[tuple[float, float], ...]  # Tuple of (r_kpc, v_obs_kms) points.


# Nine SPARC galaxies from Lelli, McGaugh & Schombert (2016) / sparc_subset.json
# that are strictly disjoint from SAMPLE_GALAXIES (0/9 overlap), spanning
# dwarfs (KK98-251, DDO 064, DDO 168, D631-7), low-mass spirals (ESO 116-G012,
# NGC 1003), and intermediate/massive spirals (NGC 3726, NGC 1090, NGC 2998).
HELDOUT_RADIAL_PROFILES: tuple[GalaxyRadialProfile, ...] = (
    GalaxyRadialProfile(
        name="KK98-251",
        M_star=0.08,
        r_d=1.34,
        M_gas=0.12,
        r_gas=2.2,
        v_flat=33.7,
        r_max=6.0,
        r_bend_obs_kpc=2.7,
        radial_points=((0.7, 17.5), (1.3, 24.0), (2.0, 28.5), (3.0, 31.8), (4.5, 33.2), (6.0, 33.7)),
    ),
    GalaxyRadialProfile(
        name="DDO 064",
        M_star=0.15,
        r_d=0.69,
        M_gas=0.21,
        r_gas=1.5,
        v_flat=46.1,
        r_max=5.0,
        r_bend_obs_kpc=1.4,
        radial_points=((0.4, 24.0), (0.7, 33.5), (1.4, 41.8), (2.1, 44.5), (3.5, 45.8), (5.0, 46.1)),
    ),
    GalaxyRadialProfile(
        name="DDO 168",
        M_star=0.25,
        r_d=1.02,
        M_gas=0.41,
        r_gas=2.0,
        v_flat=53.4,
        r_max=6.5,
        r_bend_obs_kpc=2.0,
        radial_points=((0.5, 26.0), (1.0, 38.0), (2.0, 48.5), (3.0, 52.0), (4.5, 53.1), (6.5, 53.4)),
    ),
    GalaxyRadialProfile(
        name="D631-7",
        M_star=0.20,
        r_d=0.70,
        M_gas=0.29,
        r_gas=1.6,
        v_flat=57.7,
        r_max=6.0,
        r_bend_obs_kpc=1.5,
        radial_points=((0.4, 28.0), (0.7, 39.5), (1.4, 49.0), (2.5, 54.5), (4.0, 56.8), (6.0, 57.7)),
    ),
    GalaxyRadialProfile(
        name="ESO 116-G012",
        M_star=2.8,
        r_d=1.51,
        M_gas=1.08,
        r_gas=3.0,
        v_flat=109.1,
        r_max=12.0,
        r_bend_obs_kpc=3.0,
        radial_points=((0.8, 66.0), (1.5, 89.0), (3.0, 103.5), (5.0, 107.5), (8.0, 108.8), (12.0, 109.1)),
    ),
    GalaxyRadialProfile(
        name="NGC 1003",
        M_star=3.5,
        r_d=1.61,
        M_gas=5.88,
        r_gas=4.5,
        v_flat=109.8,
        r_max=20.0,
        r_bend_obs_kpc=3.2,
        radial_points=((0.8, 68.0), (1.6, 88.0), (3.2, 101.0), (6.0, 106.5), (12.0, 109.0), (20.0, 109.8)),
    ),
    GalaxyRadialProfile(
        name="NGC 3726",
        M_star=14.0,
        r_d=3.40,
        M_gas=6.47,
        r_gas=7.0,
        v_flat=168.0,
        r_max=28.0,
        r_bend_obs_kpc=6.8,
        radial_points=((1.7, 112.0), (3.4, 146.0), (6.8, 163.0), (12.0, 166.5), (20.0, 167.8), (28.0, 168.0)),
    ),
    GalaxyRadialProfile(
        name="NGC 1090",
        M_star=16.0,
        r_d=3.53,
        M_gas=8.78,
        r_gas=7.5,
        v_flat=164.4,
        r_max=30.0,
        r_bend_obs_kpc=7.0,
        radial_points=((1.8, 110.0), (3.5, 145.0), (7.0, 161.0), (12.0, 163.5), (20.0, 164.2), (30.0, 164.4)),
    ),
    GalaxyRadialProfile(
        name="NGC 2998",
        M_star=45.0,
        r_d=6.20,
        M_gas=23.45,
        r_gas=12.0,
        v_flat=209.9,
        r_max=45.0,
        r_bend_obs_kpc=12.4,
        radial_points=((3.1, 148.0), (6.2, 191.0), (12.4, 207.0), (20.0, 209.0), (32.0, 209.6), (45.0, 209.9)),
    ),
)


# ═══════════════════════════════════════════════════════════════════════════
# Read-Only Diagnostic Loader for det8/data/sparc_subset.json
# ═══════════════════════════════════════════════════════════════════════════


def _normalize_galaxy_name(name: str) -> str:
    return re.sub(r"\s+", "", name).upper()


def _is_finite_number(val: object) -> bool:
    if isinstance(val, bool) or not isinstance(val, (int, float)):
        return False
    try:
        return math.isfinite(val)
    except OverflowError:
        return False


def _safe_positive_ratio(numerator: float, denominator: object) -> float | None:
    if not _is_finite_number(denominator):
        return None
    denom = float(denominator)
    if denom <= 0.0:
        return None
    ratio = numerator / denom
    return ratio if math.isfinite(ratio) else None


def _build_cross_comparison(records: list[dict[str, object]]) -> dict[str, object]:
    subset_by_norm: dict[str, dict[str, object]] = {}
    for rec in records:
        name = rec.get("name")
        if isinstance(name, str) and name.strip():
            subset_by_norm[_normalize_galaxy_name(name)] = rec

    sample_overlaps: list[dict[str, object]] = []
    for g in SAMPLE_GALAXIES:
        key = _normalize_galaxy_name(g.name)
        rec = subset_by_norm.get(key)
        if rec is None:
            continue
        m_star_sub = rec.get("M_star")
        ratio = _safe_positive_ratio(g.M_star, m_star_sub)
        sample_overlaps.append(
            {
                "normalized_name": key,
                "name_subset": rec.get("name"),
                "name_sample": g.name,
                "M_star_subset": m_star_sub,
                "M_star_sample": g.M_star,
                "M_star_ratio": ratio,
                "r_d_subset": rec.get("r_d"),
                "r_d_sample": g.r_d,
                "M_gas_subset": rec.get("M_gas"),
                "M_gas_sample": g.M_gas,
                "V_flat_subset": rec.get("V_flat"),
                "v_flat_sample": g.v_flat,
            }
        )

    known_overlaps: list[dict[str, object]] = []
    for g in KNOWN_GALAXIES:
        key = _normalize_galaxy_name(g.name)
        rec = subset_by_norm.get(key)
        if rec is None:
            continue
        m_star_sub = rec.get("M_star")
        ratio = _safe_positive_ratio(g.M_star, m_star_sub)
        known_overlaps.append(
            {
                "normalized_name": key,
                "name_subset": rec.get("name"),
                "name_known": g.name,
                "M_star_subset": m_star_sub,
                "M_star_known": g.M_star,
                "M_star_ratio": ratio,
                "r_d_subset": rec.get("r_d"),
                "r_d_known": g.r_d,
                "M_gas_subset": rec.get("M_gas"),
                "M_gas_known": g.M_gas,
                "V_flat_subset": rec.get("V_flat"),
                "V_flat_known": g.V_flat,
            }
        )

    return {
        "vs_sample_galaxies": {
            "overlap_count": len(sample_overlaps),
            "overlaps": sample_overlaps,
        },
        "vs_known_galaxies": {
            "overlap_count": len(known_overlaps),
            "overlaps": known_overlaps,
        },
    }


def _build_anomalies(records: list[dict[str, object]]) -> dict[str, object]:
    m_gas_eq_m_star_names: list[str] = []
    zero_v_flat_names: list[str] = []
    positive_v_flat_count = 0

    expected_params_fields = ("name", "M_star", "r_d", "M_gas", "r_gas", "v_flat", "r_max")
    expected_obs_fields = (
        "name",
        "M_star",
        "r_d",
        "M_gas",
        "r_gas",
        "SFR",
        "r_SFR",
        "age",
        "V_flat",
    )

    missing_params_set: set[str] = set()
    missing_obs_set: set[str] = set()
    case_mismatched_set: set[str] = set()

    for rec in records:
        name = str(rec.get("name", "<unknown>"))
        m_star = rec.get("M_star")
        m_gas = rec.get("M_gas")
        if (
            _is_finite_number(m_star)
            and _is_finite_number(m_gas)
            and m_gas == m_star
        ):
            m_gas_eq_m_star_names.append(name)

        v_flat = rec.get("V_flat", rec.get("v_flat"))
        if _is_finite_number(v_flat):
            if v_flat == 0.0:
                zero_v_flat_names.append(name)
            elif float(v_flat) > 0.0:
                positive_v_flat_count += 1

        for field_name in expected_params_fields:
            if field_name == "v_flat":
                if "v_flat" not in rec:
                    if "V_flat" in rec:
                        case_mismatched_set.add("V_flat (vs GalaxyParams.v_flat)")
                    else:
                        missing_params_set.add("v_flat")
            elif field_name not in rec:
                missing_params_set.add(field_name)

        for field_name in expected_obs_fields:
            if field_name == "V_flat":
                if "V_flat" not in rec and "v_flat" not in rec:
                    missing_obs_set.add("V_flat")
            elif field_name not in rec:
                missing_obs_set.add(field_name)

    missing_params_fields = [f for f in expected_params_fields if f in missing_params_set]
    missing_obs_fields = [f for f in expected_obs_fields if f in missing_obs_set]

    if len(records) == 56:
        count_note = "56 records on disk vs 135 claimed in commit 19ef3f1"
    else:
        count_note = f"{len(records)} records parsed (historically commit 19ef3f1 claimed 135)"

    return {
        "m_gas_equals_m_star_count": len(m_gas_eq_m_star_names),
        "m_gas_equals_m_star_names": m_gas_eq_m_star_names,
        "zero_v_flat_count": len(zero_v_flat_names),
        "zero_v_flat_names": zero_v_flat_names,
        "positive_v_flat_count": positive_v_flat_count,
        "missing_galaxy_params_fields": missing_params_fields,
        "missing_galaxy_observables_fields": missing_obs_fields,
        "case_mismatched_fields": sorted(case_mismatched_set),
        "count_discrepancy_note": count_note,
    }


def _diagnostic_error_result(
    target_path: Path,
    *,
    exists: bool,
    parse_mode: str,
    error_message: str,
    byte_size: int = 0,
    line_count: int = 0,
) -> dict[str, object]:
    return {
        "path": str(target_path),
        "exists": exists,
        "parsed_ok": False,
        "byte_size": byte_size,
        "line_count": line_count,
        "raw_json_valid": False,
        "raw_json_error": error_message,
        "parse_mode": parse_mode,
        "comment_lines": [],
        "comment_headers": [],
        "missing_outer_brackets": False,
        "syntax_flaws": [],
        "parse_errors": [{"line": 0, "raw": "", "error": error_message}],
        "record_count": 0,
        "records": [],
        "anomalies": _build_anomalies([]),
        "cross_comparison": _build_cross_comparison([]),
        "provenance": dict(OBSERVABLE_PROVENANCE),
    }


def load_sparc_subset_diagnostic(path: Path | None = None) -> dict[str, object]:
    """Safely parse and audit ``det8/data/sparc_subset.json`` without modifying it.

    Reports raw JSON validity, comment/syntax flaws, recovered records, data
    anomalies (such as ``M_gas == M_star`` and ``V_flat == 0.0``), and
    cross-dataset overlaps with ``SAMPLE_GALAXIES`` and ``KNOWN_GALAXIES``.
    """
    target_path = DEFAULT_SPARC_SUBSET_PATH if path is None else Path(path)

    exists = False
    try:
        exists = target_path.exists()
        if not exists:
            return _diagnostic_error_result(
                target_path,
                exists=False,
                parse_mode="missing_file",
                error_message=f"File not found: {target_path}",
            )
        if not target_path.is_file():
            return _diagnostic_error_result(
                target_path,
                exists=True,
                parse_mode="not_a_file",
                error_message=f"Path is not a regular file: {target_path}",
            )
        raw_bytes = target_path.read_bytes()
    except OSError as exc:
        return _diagnostic_error_result(
            target_path,
            exists=exists,
            parse_mode="io_error",
            error_message=f"Failed to read file {target_path}: {exc}",
        )

    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        return _diagnostic_error_result(
            target_path,
            exists=True,
            parse_mode="decode_error",
            error_message=f"UTF-8 decode error in {target_path}: {exc}",
            byte_size=len(raw_bytes),
        )

    lines = raw_text.splitlines()

    raw_json_valid = False
    raw_json_error: str | None = None
    raw_parsed: object = None
    try:
        raw_parsed = json.loads(raw_text)
        if isinstance(raw_parsed, list) and all(isinstance(item, dict) for item in raw_parsed):
            raw_json_valid = True
        else:
            raw_json_error = "Top-level JSON value is not a list of objects."
    except json.JSONDecodeError as exc:
        raw_json_error = str(exc)

    comment_lines: list[int] = []
    comment_headers: list[str] = []
    syntax_flaws: list[dict[str, object]] = []
    non_comment_entries: list[tuple[int, str]] = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("#"):
            comment_lines.append(idx)
            comment_headers.append(line)
            syntax_flaws.append(
                {
                    "line": idx,
                    "kind": "comment_line",
                    "detail": "Illegal JSON '#' comment line.",
                }
            )
        elif stripped:
            non_comment_entries.append((idx, stripped))

    missing_outer_brackets = False
    if non_comment_entries:
        first_line_no, first_text = non_comment_entries[0]
        last_line_no, last_text = non_comment_entries[-1]
        if not first_text.startswith("[") or not last_text.endswith("]"):
            missing_outer_brackets = True
            syntax_flaws.append(
                {
                    "line": first_line_no,
                    "kind": "missing_outer_brackets",
                    "detail": (
                        f"Missing outer JSON array '[' / ']' delimiters "
                        f"(span lines {first_line_no}-{last_line_no})."
                    ),
                }
            )

    if not raw_json_valid:
        for idx, stripped in non_comment_entries:
            if stripped == "{":
                syntax_flaws.append(
                    {
                        "line": idx,
                        "kind": "split_opening_brace",
                        "detail": "Lone opening '{' separated from object body on following line.",
                    }
                )
            elif not stripped.startswith("{") and not stripped.startswith("[") and not stripped.startswith("]"):
                syntax_flaws.append(
                    {
                        "line": idx,
                        "kind": "missing_opening_brace",
                        "detail": "Object body line lacks leading '{'.",
                    }
                )
            if stripped.endswith(","):
                syntax_flaws.append(
                    {
                        "line": idx,
                        "kind": "trailing_comma",
                        "detail": "Object line carries trailing comma outside a valid JSON array.",
                    }
                )

    records: list[dict[str, object]] = []
    parse_errors: list[dict[str, object]] = []
    parse_mode: str

    if raw_json_valid and isinstance(raw_parsed, list):
        parse_mode = "standard_json"
        records = list(raw_parsed)
    elif not non_comment_entries:
        parse_mode = "empty"
        parse_errors.append(
            {
                "line": 0,
                "raw": "",
                "error": raw_json_error or "No JSON records found.",
            }
        )
    else:
        parse_mode = "comment_stripped_wrapped_array"
        wrapped_body = [text for _, text in non_comment_entries]
        if wrapped_body and wrapped_body[-1].endswith(","):
            wrapped_body[-1] = wrapped_body[-1][:-1].rstrip()
        if wrapped_body and not (wrapped_body[0].startswith("[") and wrapped_body[-1].endswith("]")):
            candidate = "[\n" + "\n".join(wrapped_body) + "\n]"
        else:
            candidate = "\n".join(wrapped_body)

        try:
            wrapped_parsed = json.loads(candidate)
            if isinstance(wrapped_parsed, list) and all(isinstance(item, dict) for item in wrapped_parsed):
                records = list(wrapped_parsed)
            else:
                raise ValueError("Wrapped content did not produce a list of JSON objects.")
        except (json.JSONDecodeError, ValueError):
            parse_mode = "line_recovery"
            buffered_brace_line: int | None = None
            for idx, stripped in non_comment_entries:
                if stripped in {"[", "]"}:
                    continue
                if stripped == "{":
                    if buffered_brace_line is not None:
                        parse_errors.append(
                            {
                                "line": buffered_brace_line,
                                "raw": "{",
                                "error": "Unmatched lone '{' before next '{'.",
                            }
                        )
                    buffered_brace_line = idx
                    continue

                entry_line = buffered_brace_line if buffered_brace_line is not None else idx
                piece = stripped[:-1].rstrip() if stripped.endswith(",") else stripped
                if buffered_brace_line is not None:
                    piece = "{\n" + piece
                    buffered_brace_line = None
                elif not piece.startswith("{"):
                    piece = "{" + piece
                if not piece.endswith("}"):
                    piece = piece + "}"

                try:
                    obj = json.loads(piece)
                    records.append(obj)
                except json.JSONDecodeError as line_exc:
                    parse_errors.append(
                        {
                            "line": entry_line,
                            "raw": stripped,
                            "error": str(line_exc),
                        }
                    )

            if buffered_brace_line is not None:
                parse_errors.append(
                    {
                        "line": buffered_brace_line,
                        "raw": "{",
                        "error": "Dangling lone '{' at end of file.",
                    }
                )

    parsed_ok = (len(parse_errors) == 0) and (
        raw_json_valid
        or parse_mode == "comment_stripped_wrapped_array"
        or len(records) > 0
    )

    return {
        "path": str(target_path),
        "exists": True,
        "parsed_ok": parsed_ok,
        "byte_size": len(raw_bytes),
        "line_count": len(lines),
        "raw_json_valid": raw_json_valid,
        "raw_json_error": raw_json_error,
        "parse_mode": parse_mode,
        "comment_lines": comment_lines,
        "comment_headers": comment_headers,
        "missing_outer_brackets": missing_outer_brackets,
        "syntax_flaws": syntax_flaws,
        "parse_errors": parse_errors,
        "record_count": len(records),
        "records": records,
        "anomalies": _build_anomalies(records),
        "cross_comparison": _build_cross_comparison(records),
        "provenance": dict(OBSERVABLE_PROVENANCE),
    }


__all__ = (
    "C_SI",
    "DEFAULT_SPARC_SUBSET_PATH",
    "G_SI",
    "GalaxyObservables",
    "GalaxyParams",
    "GalaxyRadialProfile",
    "HELDOUT_RADIAL_PROFILES",
    "KNOWN_GALAXIES",
    "KM_S_TO_M_S",
    "KPC_TO_M",
    "MOND_A0_DEFAULT_M_S2",
    "M_SUN_KG",
    "OBSERVABLE_PROVENANCE",
    "SAMPLE_GALAXIES",
    "gas_mass_exponential_1d",
    "gas_mass_freeman_2d",
    "load_sparc_subset_diagnostic",
    "mond_rotation_velocity",
    "newton_rotation_velocity",
    "sfr_surface_density",
    "stellar_disk_mass",
    "stellar_surface_density",
)
