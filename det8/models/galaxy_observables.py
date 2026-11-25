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
DEFAULT_SPARC_ROTMOD_PATH: Final[Path] = (
    Path(__file__).resolve().parents[1] / "data" / "sparc_heldout_rotmod.json"
)
SPARC_UPSILON_DISK_DEFAULT: Final[float] = 0.5  # Fiducial 3.6 um disk M/L [M_sun/L_sun]
SPARC_UPSILON_BUL_DEFAULT: Final[float] = 0.7   # Fiducial 3.6 um bulge M/L [M_sun/L_sun]


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
class SparcRotmodPoint:
    """Single radial measurement row from a SPARC ``*_rotmod.dat`` table (Lelli et al. 2016)."""

    Rad_kpc: float       # Galactocentric radius [kpc]
    Vobs_kms: float      # Observed circular velocity [km/s]
    errV_kms: float      # Velocity uncertainty [km/s]
    Vgas_kms: float      # Gas contribution to circular velocity [km/s]
    Vdisk_kms: float     # Stellar disk velocity contribution for M/L = 1 [km/s]
    Vbul_kms: float      # Stellar bulge velocity contribution for M/L = 1 [km/s]
    SBdisk_L_pc2: float  # Stellar disk 3.6 um surface brightness [L_sun/pc^2]
    SBbul_L_pc2: float   # Stellar bulge 3.6 um surface brightness [L_sun/pc^2]
    Sigma_gas_from_Vgas_1e9_Msun_kpc2: float = 0.0  # Gas surface density inferred from Vgas(r) [10^9 M_sun/kpc^2]


def sparc_baryonic_newton_velocity(
    v_gas_kms: float,
    v_disk_kms: float,
    v_bul_kms: float,
    *,
    upsilon_disk: float = SPARC_UPSILON_DISK_DEFAULT,
    upsilon_bul: float = SPARC_UPSILON_BUL_DEFAULT,
) -> float:
    """Compute Newtonian baryonic circular speed V_bar [km/s] from SPARC rotmod components."""
    v_bar_sq = (
        v_gas_kms * abs(v_gas_kms)
        + upsilon_disk * (v_disk_kms ** 2)
        + upsilon_bul * (v_bul_kms ** 2)
    )
    return math.sqrt(max(0.0, v_bar_sq))


def load_sparc_heldout_rotmod(path: Path | None = None) -> dict[str, dict[str, object]]:
    """Load verbatim held-out SPARC ``*_rotmod.dat`` radial tables from disk."""
    target = DEFAULT_SPARC_ROTMOD_PATH if path is None else Path(path)
    if not target.exists() or not target.is_file():
        return {}
    raw = json.loads(target.read_text(encoding="utf-8"))
    return raw if isinstance(raw, dict) else {}


@dataclass(frozen=True, slots=True)
class GalaxyRadialProfile:
    """Held-out SPARC galaxy row traceable verbatim to sparc_subset.json, Table1.mrt, and *_rotmod.dat."""

    name: str
    M_star: float                              # Verbatim stellar mass column from sparc_subset.json (10^9 M_sun).
    r_d: float                                 # Verbatim disk scale length from sparc_subset.json (kpc).
    M_gas: float                               # Verbatim gas column from sparc_subset.json (10^9 M_sun).
    r_gas: float                               # HI disk scale length calibrated from Table1 RHI (or 2.0 * r_d) (kpc).
    v_flat: float                              # Verbatim V_flat from sparc_subset.json (km/s).
    r_max: float                               # Outermost measured SPARC Rad_kpc (or 8.0 * r_d fallback) (kpc).
    r_bend_obs_kpc: float                      # Empirically measured bend radius from observed rotation curve (kpc).
    radial_points: tuple[tuple[float, float], ...]  # Actual SPARC ((Rad_kpc, Vobs_kms)) points from *_rotmod.dat.
    sparc_subset_line: int = 0                 # Verbatim 1-based line number in det8/data/sparc_subset.json.
    rotmod_points: tuple[SparcRotmodPoint, ...] = ()  # Complete SPARC *_rotmod.dat rows.
    rotmod_sha256: str = ""                    # SHA-256 digest of the verbatim *_rotmod.dat file.
    plateau_grid_points: tuple[tuple[float, float], ...] = ()  # Standardized ((m * r_d, V_flat)) grid.
    M_star_true_table1: float = 0.0            # True SPARC Table1 stellar mass 0.5 * L[3.6] (10^9 M_sun).
    MHI_table1: float = 0.0                    # True SPARC Table1 HI gas mass MHI (10^9 M_sun).
    M_gas_true_table1: float = 0.0             # True SPARC Table1 total gas mass 1.33 * MHI (10^9 M_sun).
    RHI_kpc: float = 0.0                       # True SPARC Table1 HI radius at 1 M_sun/pc^2 (kpc).
    r_bend_measured_idx: int = 0               # Index in rotmod_points of empirically measured curve bend.
    r_bend_measured_method: str = ""           # Empirical bend detection method on observed rotation curve.


HELDOUT_PLATEAU_MULTIPLIERS: tuple[float, ...] = (2.2, 3.0, 4.0, 5.0, 6.0, 8.0)
_CACHED_ROTMOD_TABLES: Final[dict[str, dict[str, object]]] = load_sparc_heldout_rotmod()


def _make_traceable_sparc_profile(
    *,
    name: str,
    M_star: float,
    r_d: float,
    M_gas: float,
    v_flat: float,
    sparc_subset_line: int,
) -> GalaxyRadialProfile:
    """Build a GalaxyRadialProfile from verbatim sparc_subset.json, Table1.mrt, and *_rotmod.dat rows."""
    plateau_grid = tuple((round(m * r_d, 6), v_flat) for m in HELDOUT_PLATEAU_MULTIPLIERS)
    entry = _CACHED_ROTMOD_TABLES.get(name)
    rot_pts: tuple[SparcRotmodPoint, ...] = ()
    sha = ""
    ms_true = M_star
    mhi_t1 = M_gas
    mg_true = round(1.33 * M_gas, 6)
    rhi_val = 0.0
    rg_val = round(2.0 * r_d, 6)
    b_idx = 0
    b_method = "rule_2p2_rd"
    r_bend_val = round(2.2 * r_d, 6)

    if isinstance(entry, dict):
        sha = str(entry.get("sha256", ""))
        ms_true = float(entry.get("M_star_true_1e9Msun", M_star))
        mhi_t1 = float(entry.get("MHI_1e9Msun", M_gas))
        mg_true = float(entry.get("M_gas_true_1e9Msun", round(1.33 * M_gas, 6)))
        rhi_val = float(entry.get("RHI_kpc", 0.0))
        rg_val = float(entry.get("r_gas_from_RHI_kpc", round(2.0 * r_d, 6)))
        b_idx = int(entry.get("r_bend_measured_idx", 0))
        b_method = str(entry.get("r_bend_measured_method", "first_ge_0p85_vflat"))
        raw_pts = entry.get("points", [])
        if isinstance(raw_pts, list):
            rot_pts = tuple(
                SparcRotmodPoint(
                    Rad_kpc=float(p["Rad_kpc"]),
                    Vobs_kms=float(p["Vobs_kms"]),
                    errV_kms=float(p["errV_kms"]),
                    Vgas_kms=float(p["Vgas_kms"]),
                    Vdisk_kms=float(p["Vdisk_kms"]),
                    Vbul_kms=float(p["Vbul_kms"]),
                    SBdisk_L_pc2=float(p["SBdisk_L_pc2"]),
                    SBbul_L_pc2=float(p["SBbul_L_pc2"]),
                    Sigma_gas_from_Vgas_1e9_Msun_kpc2=float(
                        p.get("Sigma_gas_from_Vgas_1e9_Msun_kpc2", 0.0)
                    ),
                )
                for p in raw_pts
            )
    if rot_pts:
        rad_pts = tuple((p.Rad_kpc, p.Vobs_kms) for p in rot_pts)
        r_max_val = rot_pts[-1].Rad_kpc
        r_bend_val = float(
            entry.get("r_bend_measured_kpc", rot_pts[min(b_idx, len(rot_pts) - 1)].Rad_kpc)
            if isinstance(entry, dict)
            else rot_pts[min(b_idx, len(rot_pts) - 1)].Rad_kpc
        )
    else:
        rad_pts = plateau_grid
        r_max_val = round(8.0 * r_d, 6)

    return GalaxyRadialProfile(
        name=name,
        M_star=M_star,
        r_d=r_d,
        M_gas=M_gas,
        r_gas=rg_val,
        v_flat=v_flat,
        r_max=r_max_val,
        r_bend_obs_kpc=r_bend_val,
        radial_points=rad_pts,
        sparc_subset_line=sparc_subset_line,
        rotmod_points=rot_pts,
        rotmod_sha256=sha,
        plateau_grid_points=plateau_grid,
        M_star_true_table1=ms_true,
        MHI_table1=mhi_t1,
        M_gas_true_table1=mg_true,
        RHI_kpc=rhi_val,
        r_bend_measured_idx=b_idx,
        r_bend_measured_method=b_method,
    )


def canonicalize_sparc_catalog_name(name: str) -> str:
    """Normalize SPARC galaxy identifier, stripping whitespace and leading zeros after prefix."""
    compact = re.sub(r"[\s_-]+", "", name).upper()
    match = re.match(r"^([A-Z]+)0+(\d+.*)$", compact)
    return f"{match.group(1)}{match.group(2)}" if match else compact


# Nine traceable SPARC rows verbatim from det8/data/sparc_subset.json
# (Lelli, McGaugh & Schombert 2016, AJ, 152, 157; commit 19ef3f1), strictly
# disjoint from SAMPLE_GALAXIES (0/9 overlap under canonical catalog IDs),
# spanning dwarfs (KK98-251, DDO064, DDO168, D631-7), low-mass spirals
# (ESO116-G012, NGC1003), and intermediate/massive spirals (NGC3726, NGC1090, NGC2998).
HELDOUT_RADIAL_PROFILES: tuple[GalaxyRadialProfile, ...] = (
    _make_traceable_sparc_profile(
        name="KK98-251",
        M_star=0.115,
        r_d=1.34,
        M_gas=0.115,
        v_flat=33.7,
        sparc_subset_line=38,
    ),
    _make_traceable_sparc_profile(
        name="DDO064",
        M_star=0.211,
        r_d=0.69,
        M_gas=0.211,
        v_flat=46.1,
        sparc_subset_line=11,
    ),
    _make_traceable_sparc_profile(
        name="DDO168",
        M_star=0.413,
        r_d=1.02,
        M_gas=0.413,
        v_flat=53.4,
        sparc_subset_line=14,
    ),
    _make_traceable_sparc_profile(
        name="D631-7",
        M_star=0.290,
        r_d=0.70,
        M_gas=0.290,
        v_flat=57.7,
        sparc_subset_line=10,
    ),
    _make_traceable_sparc_profile(
        name="ESO116-G012",
        M_star=1.083,
        r_d=1.51,
        M_gas=1.083,
        v_flat=109.1,
        sparc_subset_line=17,
    ),
    _make_traceable_sparc_profile(
        name="NGC1003",
        M_star=5.880,
        r_d=1.61,
        M_gas=5.880,
        v_flat=109.8,
        sparc_subset_line=47,
    ),
    _make_traceable_sparc_profile(
        name="NGC3726",
        M_star=6.473,
        r_d=3.40,
        M_gas=6.473,
        v_flat=168.0,
        sparc_subset_line=62,
    ),
    _make_traceable_sparc_profile(
        name="NGC1090",
        M_star=8.783,
        r_d=3.53,
        M_gas=8.783,
        v_flat=164.4,
        sparc_subset_line=48,
    ),
    _make_traceable_sparc_profile(
        name="NGC2998",
        M_star=23.451,
        r_d=6.20,
        M_gas=23.451,
        v_flat=209.9,
        sparc_subset_line=58,
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
    "DEFAULT_SPARC_ROTMOD_PATH",
    "DEFAULT_SPARC_SUBSET_PATH",
    "G_SI",
    "GalaxyObservables",
    "GalaxyParams",
    "GalaxyRadialProfile",
    "HELDOUT_PLATEAU_MULTIPLIERS",
    "HELDOUT_RADIAL_PROFILES",
    "KNOWN_GALAXIES",
    "KM_S_TO_M_S",
    "KPC_TO_M",
    "MOND_A0_DEFAULT_M_S2",
    "M_SUN_KG",
    "OBSERVABLE_PROVENANCE",
    "SAMPLE_GALAXIES",
    "SPARC_UPSILON_BUL_DEFAULT",
    "SPARC_UPSILON_DISK_DEFAULT",
    "SparcRotmodPoint",
    "canonicalize_sparc_catalog_name",
    "gas_mass_exponential_1d",
    "gas_mass_freeman_2d",
    "load_sparc_heldout_rotmod",
    "load_sparc_subset_diagnostic",
    "mond_rotation_velocity",
    "newton_rotation_velocity",
    "sfr_surface_density",
    "sparc_baryonic_newton_velocity",
    "stellar_disk_mass",
    "stellar_surface_density",
)
