"""Pathway 2 (Π-Conformal Clock-Metric Bridge) implementation and quantitative refutation audit.

Evaluates the literal conformal bridge connecting DET8's participation aperture
``Π`` (``det8_core.participation_aperture``, ``Δτ = Π · ΔN``) to an effective
spacetime metric ``g_μν = Π²(x) η_μν`` and weak-field acceleration
``a = -c² ∇ ln Π(x)``, alongside the potential ``Φ_κ(x) = c² ln(1 + λ_P κ(x))``.

Epistemic & Quarantine Boundary
-------------------------------
- Imports ONLY Python stdlib and active/non-retired symbols from
  ``det8.models.det8_core``, ``det8.models.galaxy_observables``,
  ``det8.models.experimental_constraints`` (clock/Eötvös literature anchors only),
  and ``det8.models.bonds``.
- Imports ZERO ``FULLY_RETIRED`` modules (never ``post_newtonian``,
  ``kappa_derivation``, ``sparc_analysis``, ``o7_*``, or ``continuum_limit_*``)
  and ZERO quarantined gravity-source symbols (``LAMBDA_GAMMA``,
  ``effective_gravity_source``, ``constrain_lambda_gamma_from_eotvos``,
  ``KNOWN_ANOMALIES``, ``analyze_gravity_anomalies``).
- Preserves ``PARTIAL_QUARANTINE`` caveats: NIST/PTB/GPS clock bounds constrain
  the product ``λ_P · Δκ`` with an assumed (not directly measured) ``Δκ``.
"""

from __future__ import annotations

import math
from typing import Callable, Final, Sequence

from det8.models.bonds import BondNetwork, BondRecord
from det8.models.det8_core import (
    LAMBDA_P,
    NodeRecord,
    participation_aperture,
    proper_time_increment,
)
from det8.models.experimental_constraints import (
    PUBLISHED_CLOCK_COMPARISONS,
    PUBLISHED_EOTVOS,
    constrain_lambda_p_from_clocks,
)
from det8.models.galaxy_observables import (
    C_SI,
    G_SI,
    KM_S_TO_M_S,
    KNOWN_GALAXIES,
    KPC_TO_M,
    M_SUN_KG,
    SAMPLE_GALAXIES,
    GalaxyObservables,
    GalaxyParams,
    newton_rotation_velocity,
    sfr_surface_density,
    stellar_surface_density,
)


# ═══════════════════════════════════════════════════════════════════════════
# External Literature / Empirical Anchors (Declared Locally, Quarantine-Safe)
# ═══════════════════════════════════════════════════════════════════════════

# Bertotti, Iess & Tortora (2003), Nature 425, 374; Will (2014).
# Declared locally as an EXTERNAL_ANCHOR rather than importing retired post_newtonian.py.
CASSINI_GAMMA_PPN_BOUND: Final[float] = 2.3e-5

# Shapiro et al. (2004) / Will (2014) VLBI solar-limb deflection precision.
VLBI_DEFLECTION_PRECISION: Final[float] = 1.0e-4

# Solar radius [m] (IAU nominal, matches retired post_newtonian.R_SUN = 6.957e8).
SOLAR_RADIUS_M: Final[float] = 6.957e8

# Conditional GPS clock bound from illustrative 0.3 ns/day residual scale
# (0.3e-9 / 86400 ≈ 3.472e-15; rounded product bound 3.5e-15; gps_analysis.py).
GPS_CLOCK_RESIDUAL_NS: Final[float] = 0.3
SECONDS_PER_DAY: Final[float] = 86400.0
GPS_CLOCK_PRODUCT_BOUND: Final[float] = 3.5e-15
GPS_DELTA_KAPPA_ASSUMED: Final[float] = 1.0e-6

# Milgrom empirical MOND acceleration scale [m/s^2] for Variant (c) audit.
MOND_A0_SI: Final[float] = 1.2e-10

_ALLOWED_APERTURE_KWARGS: Final[frozenset[str]] = frozenset(
    {"sigma", "eta", "F", "H", "velocity_fraction"}
)


# ═══════════════════════════════════════════════════════════════════════════
# Strict Domain Validation Guards (Pre-det8_core)
# ═══════════════════════════════════════════════════════════════════════════


def _validate_finite_float(name: str, value: object) -> float:
    """Reject bools, non-real types, NaN, ±inf, and huge ints before touching det8_core."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite real number, got {value!r}")
    try:
        val = float(value)
    except OverflowError as exc:
        raise ValueError(
            f"{name} must be finite and representable as float64, got OverflowError from {type(value).__name__}"
        ) from exc
    if not math.isfinite(val):
        raise ValueError(f"{name} must be finite, got {value!r}")
    return val


def _validate_kappa(kappa: object, name: str = "kappa") -> float:
    val = _validate_finite_float(name, kappa)
    if val < 0.0 or val > 1.0:
        raise ValueError(f"{name} must satisfy 0.0 <= {name} <= 1.0, got {val!r}")
    return val


def _validate_lambda_p(lambda_p: object, *, positive_only: bool = False) -> float:
    val = _validate_finite_float("lambda_p", lambda_p)
    if positive_only:
        if val <= 0.0:
            raise ValueError(f"lambda_p must be > 0.0, got {val!r}")
    elif val < 0.0:
        raise ValueError(f"lambda_p must be >= 0.0, got {val!r}")
    return val


def _validate_aperture_kwargs(
    aperture_kwargs: dict[str, object],
    *,
    require_positive_eta: bool = False,
) -> tuple[float, float, float, float, float]:
    unknown = set(aperture_kwargs) - _ALLOWED_APERTURE_KWARGS
    if unknown:
        raise TypeError(
            f"Unexpected aperture keyword argument(s): {', '.join(sorted(unknown))}"
        )

    sigma = _validate_finite_float("sigma", aperture_kwargs.get("sigma", 1.0))
    if sigma <= 0.0:
        raise ValueError(f"sigma must be > 0.0, got {sigma!r}")

    eta = _validate_finite_float("eta", aperture_kwargs.get("eta", 1.0))
    if require_positive_eta:
        if eta <= 0.0 or eta > 1.0:
            raise ValueError(f"eta must satisfy 0.0 < eta <= 1.0, got {eta!r}")
    elif eta < 0.0 or eta > 1.0:
        raise ValueError(f"eta must satisfy 0.0 <= eta <= 1.0, got {eta!r}")

    f_val = _validate_finite_float("F", aperture_kwargs.get("F", 0.0))
    if f_val < 0.0:
        raise ValueError(f"F must be >= 0.0, got {f_val!r}")

    h_val = _validate_finite_float("H", aperture_kwargs.get("H", 0.0))
    if h_val < 0.0:
        raise ValueError(f"H must be >= 0.0, got {h_val!r}")

    vf = _validate_finite_float(
        "velocity_fraction", aperture_kwargs.get("velocity_fraction", 0.0)
    )
    if vf < 0.0 or vf >= 1.0:
        raise ValueError(
            f"velocity_fraction must satisfy 0.0 <= velocity_fraction < 1.0, got {vf!r}"
        )

    return sigma, eta, f_val, h_val, vf


# ═══════════════════════════════════════════════════════════════════════════
# Core Pathway 2 Functions
# ═══════════════════════════════════════════════════════════════════════════


def conformal_clock_lapse(
    kappa: float,
    lambda_p: float = LAMBDA_P,
    **aperture_kwargs: float,
) -> float:
    """Compute the DET8 participation aperture ``Π(κ)`` via ``det8_core``.

    Strictly pre-validates ``kappa``, ``eta``, ``F``, ``H``, ``velocity_fraction``,
    and ``lambda_p`` without silent clamping, preventing ``NaN``, ``bool``,
    out-of-range ``kappa``, negative ``velocity_fraction``, or zero-division.
    ``sigma > 0.0`` is likewise pre-validated while preserving ``det8_core.NodeRecord``'s
    ``1e-12`` conductivity floor (``max(1e-12, sigma)``).
    """
    k = _validate_kappa(kappa, "kappa")
    lp = _validate_lambda_p(lambda_p)
    sigma, eta, f_val, h_val, vf = _validate_aperture_kwargs(aperture_kwargs)

    record = NodeRecord(kappa=k, sigma=sigma, eta=eta, F=f_val, H=h_val)
    return participation_aperture(record, velocity_fraction=vf, lambda_p=lp)


def proper_time_step(
    kappa: float,
    delta_n: float = 1.0,
    lambda_p: float = LAMBDA_P,
    **aperture_kwargs: float,
) -> float:
    """Compute proper-time increment ``Δτ = Π(κ) · ΔN`` via ``det8_core.proper_time_increment``.

    Strictly pre-validates ``kappa``, ``delta_n``, ``eta``, ``F``, ``H``,
    ``velocity_fraction``, and ``lambda_p`` without clamping, while ``sigma > 0.0``
    preserves ``det8_core.NodeRecord``'s ``1e-12`` conductivity floor
    (``max(1e-12, sigma)``).
    """
    k = _validate_kappa(kappa, "kappa")
    dn = _validate_finite_float("delta_n", delta_n)
    if dn < 0.0:
        raise ValueError(f"delta_n must be >= 0.0, got {dn!r}")
    lp = _validate_lambda_p(lambda_p)
    sigma, eta, f_val, h_val, vf = _validate_aperture_kwargs(aperture_kwargs)

    record = NodeRecord(kappa=k, sigma=sigma, eta=eta, F=f_val, H=h_val)
    result = proper_time_increment(record, delta_N=dn, velocity_fraction=vf, lambda_p=lp)
    if not math.isfinite(result):
        raise ValueError(
            f"proper_time_step overflowed to non-finite result {result!r} "
            f"for delta_n={dn!r}, sigma={sigma!r}"
        )
    return result


def kappa_potential_phi(kappa: float, lambda_p: float = LAMBDA_P) -> float:
    """Compute the κ-bridge potential ``Φ_κ(κ) = c² ln(1 + λ_P κ)`` [m²/s²]."""
    k = _validate_kappa(kappa, "kappa")
    lp = _validate_lambda_p(lambda_p)
    return (C_SI**2) * math.log1p(lp * k)


def conformal_acceleration_1d(
    r_kpc: float,
    kappa_fn: Callable[[float], float],
    *,
    lambda_p: float = LAMBDA_P,
    dr_kpc: float = 1.0e-4,
    **aperture_kwargs: float,
) -> dict[str, object]:
    """Compute both literal conformal lapse acceleration and ``-∇Φ_κ`` in 1D.

    Evaluates:
      * ``a_conformal = -c² d(ln Π)/dr`` (literal Pathway 2 bridge)
      * ``a_phi       = -dΦ_κ/dr``       (attractive gradient of ``Φ_κ = c² ln(1 + λ_P κ)``)

    Uses the symmetric ``math.log1p``-stabilized identity for constant prefactor ``Π_0``:
      ``ln(Π_+ / Π_-) = -ln((1 + λ_P κ_+)/(1 + λ_P κ_-))``
    evaluating ``+log1p(λ_P (κ_+ - κ_-) / (1 + λ_P κ_-))`` for ``κ_+ >= κ_-`` and
    ``-log1p(λ_P (κ_- - κ_+) / (1 + λ_P κ_+))`` otherwise, preventing float64
    catastrophic cancellation when ``λ_P κ ≪ 1`` and ``log1p(-1.0)`` domain errors
    when ``λ_P >= 1e16`` on decreasing ``κ``.
    """
    r = _validate_finite_float("r_kpc", r_kpc)
    if r <= 0.0:
        raise ValueError(f"r_kpc must be > 0.0, got {r!r}")

    dr = _validate_finite_float("dr_kpc", dr_kpc)
    if dr <= 0.0 or dr >= r:
        raise ValueError(f"dr_kpc must satisfy 0.0 < dr_kpc < r_kpc ({r!r}), got {dr!r}")

    r_plus = r + dr
    r_minus = r - dr
    if not (math.isfinite(r_plus) and math.isfinite(r_minus)):
        raise ValueError(
            f"r_kpc +/- dr_kpc overflowed float64 for r_kpc={r!r}, dr_kpc={dr!r}"
        )
    if not (r_plus > r and r_minus < r):
        raise ValueError(
            f"dr_kpc={dr!r} is below float64 ULP resolution at r_kpc={r!r}"
        )

    if not callable(kappa_fn):
        raise TypeError(f"kappa_fn must be callable, got {type(kappa_fn).__name__}")

    lp = _validate_lambda_p(lambda_p)
    _validate_aperture_kwargs(aperture_kwargs, require_positive_eta=True)

    k_center = _validate_kappa(kappa_fn(r), "kappa_fn(r_kpc)")
    k_plus = _validate_kappa(kappa_fn(r_plus), "kappa_fn(r_kpc + dr_kpc)")
    k_minus = _validate_kappa(kappa_fn(r_minus), "kappa_fn(r_kpc - dr_kpc)")

    pi_center = conformal_clock_lapse(k_center, lambda_p=lp, **aperture_kwargs)
    pi_plus = conformal_clock_lapse(k_plus, lambda_p=lp, **aperture_kwargs)
    pi_minus = conformal_clock_lapse(k_minus, lambda_p=lp, **aperture_kwargs)

    dr_m = dr * KPC_TO_M
    if k_plus >= k_minus:
        delta_log = math.log1p(lp * (k_plus - k_minus) / (1.0 + lp * k_minus))
    else:
        delta_log = -math.log1p(lp * (k_minus - k_plus) / (1.0 + lp * k_plus))
    dln_pi_dr_m = -delta_log / (2.0 * dr_m)
    dphi_dr_m = (C_SI**2) * (delta_log / (2.0 * dr_m))

    a_conformal = -(C_SI**2) * dln_pi_dr_m
    a_phi = -dphi_dr_m
    if not (math.isfinite(a_conformal) and math.isfinite(a_phi)):
        raise ValueError(
            f"conformal_acceleration_1d overflowed to non-finite acceleration "
            f"(a_conformal={a_conformal!r}, a_phi={a_phi!r}) for r_kpc={r!r}, dr_kpc={dr!r}"
        )

    return {
        "r_kpc": r,
        "dr_kpc": dr,
        "lambda_p": lp,
        "kappa_center": k_center,
        "kappa_plus": k_plus,
        "kappa_minus": k_minus,
        "pi_center": pi_center,
        "pi_plus": pi_plus,
        "pi_minus": pi_minus,
        "phi_kappa": kappa_potential_phi(k_center, lambda_p=lp),
        "dln_pi_dr_m": dln_pi_dr_m,
        "dphi_dr_m": dphi_dr_m,
        "a_conformal": a_conformal,
        "a_phi": a_phi,
        "a_conformal_plus_a_phi": a_conformal + a_phi,
        "is_repulsive": a_conformal > 0.0,
        "is_attractive": a_conformal < 0.0,
        "sign_consistent_with_attractive_phi": (
            (a_conformal == 0.0 and a_phi == 0.0) or (a_conformal * a_phi > 0.0)
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Local Quarantine-Safe κ(r) Helpers (T1 Contraction vs Legacy F6 Parity)
# ═══════════════════════════════════════════════════════════════════════════


def _t1_contraction_kappa(
    r_kpc: float,
    *,
    M_star: float,
    r_d: float,
    M_gas: float,
    r_gas: float,
    sigma_crit: float,
    SFR: float = 0.0,
    r_SFR: float = 0.0,
    w_sfr: float = 0.0,
) -> float:
    """T1 Markov kernel contraction κ(r) = exp(-(Σ_* + Σ_gas)/Σ_crit - w_SFR Σ_SFR)."""
    s_star = stellar_surface_density(r_kpc, M_star, r_d)
    s_gas = stellar_surface_density(r_kpc, M_gas, r_gas)
    s_sfr = sfr_surface_density(r_kpc, SFR, r_SFR) if (SFR > 0.0 and r_SFR > 0.0) else 0.0
    exponent = (s_star + s_gas) / sigma_crit + w_sfr * s_sfr
    return math.exp(-exponent)


def _legacy_f6_kappa(
    r_kpc: float,
    galaxy: GalaxyObservables,
    *,
    t_reset: float = 0.01,
    kappa_min: float = 1.0e-6,
    q_sat: float = 1.0,
) -> float:
    """Local parity-exact replica of retired ``kappa_derivation.py:136-137`` (no retired import)."""
    s_star = stellar_surface_density(r_kpc, galaxy.M_star, galaxy.r_d)
    s_sfr = sfr_surface_density(r_kpc, galaxy.SFR, galaxy.r_SFR)
    q_val = s_star * galaxy.age / (s_sfr * t_reset + kappa_min)
    return q_val / (q_val + q_sat)


# ═══════════════════════════════════════════════════════════════════════════
# Quantitative Refutation & Viability Audits (1 through 4)
# ═══════════════════════════════════════════════════════════════════════════


def audit_sign_consistency(
    *,
    lambda_p: float = 2.0e-7,
    sigma_crit: float = 0.008,
    w_sfr: float = 0.0,
    dr_kpc: float = 1.0e-4,
) -> dict[str, object]:
    """Audit 1: Check sign of ``a_conformal = -c² ∇ ln Π`` under T1 vs legacy F6 ``κ(r)``.

    Algebraically:
      ``Π = (1 + λ_P κ)⁻¹ ⇒ ln Π = -ln(1 + λ_P κ) = -Φ_κ/c²``
      ``⇒ a_conformal = -c² d(ln Π)/dr = +dΦ_κ/dr = -a_phi``
    Therefore T1 contraction (``dκ/dr > 0``) makes ``a_conformal > 0`` (outward/repulsive),
    while inward ``a_conformal < 0`` forces ``dκ/dr < 0`` (the retired F6 failure).
    """
    lp = _validate_lambda_p(lambda_p, positive_only=True)
    sc = _validate_finite_float("sigma_crit", sigma_crit)
    if sc <= 0.0:
        raise ValueError(f"sigma_crit must be > 0.0, got {sc!r}")
    ws = _validate_finite_float("w_sfr", w_sfr)
    if ws < 0.0:
        raise ValueError(f"w_sfr must be >= 0.0, got {ws!r}")
    dr = _validate_finite_float("dr_kpc", dr_kpc)
    if dr <= 0.0:
        raise ValueError(f"dr_kpc must be > 0.0, got {dr!r}")

    radii_20 = [0.5 + i * (30.0 - 0.5) / 19.0 for i in range(20)]
    per_galaxy: list[dict[str, object]] = []
    t1_inc_count = 0
    t1_rep_count = 0
    f6_inc_count = 0
    f6_dec_count = 0
    f6_att_count = 0

    for g in KNOWN_GALAXIES:
        r_eval = max(2.0 * g.r_d, 5.0)

        def t1_fn(r: float, gal: GalaxyObservables = g) -> float:
            return _t1_contraction_kappa(
                r,
                M_star=gal.M_star,
                r_d=gal.r_d,
                M_gas=gal.M_gas,
                r_gas=gal.r_gas,
                sigma_crit=sc,
                SFR=gal.SFR,
                r_SFR=gal.r_SFR,
                w_sfr=ws,
            )

        def f6_fn(r: float, gal: GalaxyObservables = g) -> float:
            return _legacy_f6_kappa(r, gal)

        t1_vals = [t1_fn(r) for r in radii_20]
        f6_vals = [f6_fn(r) for r in radii_20]

        t1_increasing = all(t1_vals[i + 1] > t1_vals[i] for i in range(len(t1_vals) - 1))
        f6_increasing = all(f6_vals[i + 1] > f6_vals[i] for i in range(len(f6_vals) - 1))
        f6_decreasing = all(f6_vals[i + 1] < f6_vals[i] for i in range(len(f6_vals) - 1))

        t1_acc = conformal_acceleration_1d(r_eval, t1_fn, lambda_p=lp, dr_kpc=dr)
        f6_acc = conformal_acceleration_1d(r_eval, f6_fn, lambda_p=lp, dr_kpc=dr)

        if t1_increasing:
            t1_inc_count += 1
        if bool(t1_acc["is_repulsive"]):
            t1_rep_count += 1
        if f6_increasing:
            f6_inc_count += 1
        if f6_decreasing:
            f6_dec_count += 1
        if bool(f6_acc["is_attractive"]):
            f6_att_count += 1

        per_galaxy.append(
            {
                "name": g.name,
                "r_eval_kpc": r_eval,
                "t1_monotone_increasing": t1_increasing,
                "t1_delta_kappa_01_to_30": t1_fn(30.0) - t1_fn(0.1),
                "t1_a_conformal_m_s2": t1_acc["a_conformal"],
                "t1_a_phi_m_s2": t1_acc["a_phi"],
                "t1_repulsive": t1_acc["is_repulsive"],
                "f6_monotone_increasing": f6_increasing,
                "f6_monotone_decreasing": f6_decreasing,
                "f6_delta_kappa_01_to_30": f6_fn(30.0) - f6_fn(0.1),
                "f6_a_conformal_m_s2": f6_acc["a_conformal"],
                "f6_attractive": f6_acc["is_attractive"],
            }
        )

    n_total = len(KNOWN_GALAXIES)
    return {
        "audit": "sign_consistency",
        "lambda_p": lp,
        "sigma_crit": sc,
        "w_sfr": ws,
        "n_galaxies": n_total,
        "t1_monotone_increasing_count": t1_inc_count,
        "t1_repulsive_count": t1_rep_count,
        "f6_monotone_increasing_count": f6_inc_count,
        "f6_monotone_decreasing_count": f6_dec_count,
        "f6_attractive_count": f6_att_count,
        "f6_reintroduces_inside_out_failure": f6_inc_count == 0,
        "algebraic_identity": (
            "a_conformal = -c^2 d(ln Pi)/dr = +c^2 lambda_P (d kappa/dr) / (1 + lambda_P kappa) "
            "= +d Phi_kappa/dr = -a_phi"
        ),
        "galaxies": per_galaxy,
        "passed": t1_rep_count == 0 and f6_inc_count > 0,
        "reason": (
            f"Under T1 contraction, {t1_rep_count}/{n_total} galaxies yield outward repulsive "
            f"a_conformal > 0; inward a_conformal < 0 occurs in {f6_att_count}/{n_total} "
            "galaxies only by reintroducing retired F6 inside-out decreasing kappa (0/8 increasing)."
        ),
    }


def audit_conformal_ppn_lensing(
    *,
    cassini_bound: float = CASSINI_GAMMA_PPN_BOUND,
    vlbi_precision: float = VLBI_DEFLECTION_PRECISION,
) -> dict[str, object]:
    """Audit 2: Conformal null-geodesic invariance and PPN ``γ`` / Cassini / VLBI failure.

    For a purely conformal metric ``g_μν = Π²(x) η_μν`` (with ``Π(x) > 0``):
      1. Null intervals satisfy ``ds² = Π²(x) (-c² dt² + d𝐱²) = 0 ⇔ η_μν dx^μ dx^ν = 0``
         independently of ``Π(x)``, giving zero light deflection and zero Shapiro excess.
      2. Weak-field matching ``Π² ≈ 1 + 2 Φ_eff/c²`` against isotropic PPN
         ``g_00 = -(1 + 2 Φ/c²)``, ``g_ij = +(1 - 2 γ_PPN Φ/c²) δ_ij`` forces
         ``γ_PPN = -1.0`` and ``(1 + γ_PPN)/2 = 0.0``.
    """
    cb = _validate_finite_float("cassini_bound", cassini_bound)
    if cb <= 0.0:
        raise ValueError(f"cassini_bound must be > 0.0, got {cb!r}")
    vp = _validate_finite_float("vlbi_precision", vlbi_precision)
    if vp <= 0.0:
        raise ValueError(f"vlbi_precision must be > 0.0, got {vp!r}")

    # Numerical check of conformal null invariance ds^2 = Pi^2 * (-(c*dt)^2 + dx^2) = 0
    null_samples: list[dict[str, float]] = []
    lp_probe = 2.0e-7
    for k in (0.0, 0.25, 0.5, 1.0):
        pi_val = conformal_clock_lapse(k, lambda_p=lp_probe)
        c_dt = 1.0
        dx = 1.0
        ds_sq = (pi_val**2) * (-(c_dt**2) + dx**2)
        null_samples.append(
            {
                "kappa": k,
                "pi": pi_val,
                "conformal_null_ds_sq": ds_sq,
                "coord_light_speed_ratio": dx / c_dt,
            }
        )

    gamma_ppn = -1.0
    deflection_factor = 0.5 * (1.0 + gamma_ppn)
    abs_gamma_minus_one = abs(gamma_ppn - 1.0)
    cassini_violation_ratio = abs_gamma_minus_one / cb

    delta_theta_gr_rad = 4.0 * G_SI * M_SUN_KG / (SOLAR_RADIUS_M * (C_SI**2))
    delta_theta_gr_arcsec = delta_theta_gr_rad * (180.0 / math.pi) * 3600.0
    delta_theta_conformal_rad = deflection_factor * delta_theta_gr_rad
    vlbi_fractional_miss = abs(delta_theta_conformal_rad - delta_theta_gr_rad) / delta_theta_gr_rad
    vlbi_violation_ratio = vlbi_fractional_miss / vp

    return {
        "audit": "conformal_ppn_lensing",
        "metric_ansatz": "g_mu_nu = Pi(x)^2 * eta_mu_nu",
        "gamma_ppn": gamma_ppn,
        "gr_gamma_ppn": 1.0,
        "deflection_factor": deflection_factor,
        "abs_gamma_minus_one": abs_gamma_minus_one,
        "cassini_bound": cb,
        "cassini_violation_ratio": cassini_violation_ratio,
        "delta_theta_gr_rad": delta_theta_gr_rad,
        "delta_theta_gr_arcsec": delta_theta_gr_arcsec,
        "delta_theta_conformal_rad": delta_theta_conformal_rad,
        "vlbi_precision": vp,
        "vlbi_fractional_miss": vlbi_fractional_miss,
        "vlbi_violation_ratio": vlbi_violation_ratio,
        "null_invariance_samples": null_samples,
        "order_count_supersession_note": (
            "det8.models.order_count_geometry (T7, conformal_invariance_of_order) confirms "
            "conformal rescaling g -> Omega^2 g preserves light cones and supersedes the "
            "retired o7_*/continuum_limit_* Omega = Pi/c chain."
        ),
        "passed": abs_gamma_minus_one < cb and vlbi_fractional_miss < vp,
        "reason": (
            f"Purely conformal g_mu_nu = Pi^2 eta_mu_nu gives gamma_PPN = -1.0 (zero null "
            f"deflection), violating Cassini |gamma - 1| < {cb:.1e} by {cassini_violation_ratio:.1f}x "
            f"and missing GR solar-limb VLBI deflection by 100%."
        ),
    }


def _ols_and_btfr_stats(galaxies: Sequence[GalaxyParams]) -> dict[str, float]:
    xs = [math.log10((g.M_star + g.M_gas) * 1.0e9) for g in galaxies]
    ys = [math.log10(g.v_flat) for g in galaxies]
    n = float(len(xs))
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    s_xx = sum((x - mean_x) ** 2 for x in xs)
    s_yy = sum((y - mean_y) ** 2 for y in ys)
    s_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))

    slope = s_xy / s_xx
    intercept = mean_y - slope * mean_x
    pearson_r = s_xy / math.sqrt(s_xx * s_yy)

    residuals_btfr = [
        math.log10(((g.M_star + g.M_gas) * 1.0e9) / (g.v_flat**4)) for g in galaxies
    ]
    mean_res = sum(residuals_btfr) / n
    btfr_scatter_dex = math.sqrt(
        sum((res - mean_res) ** 2 for res in residuals_btfr) / n
    )
    return {
        "ols_slope": slope,
        "ols_intercept": intercept,
        "pearson_r": pearson_r,
        "btfr_canonical_slope": 0.25,
        "btfr_scatter_dex": btfr_scatter_dex,
    }


def audit_sparc_mass_scaling(
    *,
    gas_mode: str = "1d",
    lambda_p_grid: Sequence[float] | None = None,
    sigma_crit_grid: Sequence[float] | None = None,
) -> dict[str, object]:
    """Audit 3: Bounded ``κ ∈ [0, 1]`` mass-independent ``ΔΦ_κ`` vs SPARC 43 galaxies & BTFR."""
    if gas_mode not in {"1d", "freeman_2d"}:
        raise ValueError(f"Invalid gas_mode {gas_mode!r}; expected '1d' or 'freeman_2d'")

    lp_grid = (
        (5.0e-8, 1.0e-7, 2.0e-7, 3.0e-7, 5.0e-7, 1.0e-6)
        if lambda_p_grid is None
        else tuple(_validate_lambda_p(v, positive_only=True) for v in lambda_p_grid)
    )
    sc_grid = (
        (0.001, 0.002, 0.003, 0.005, 0.008, 0.01, 0.015, 0.02, 0.05)
        if sigma_crit_grid is None
        else tuple(_validate_finite_float("sigma_crit", v) for v in sigma_crit_grid)
    )
    if not lp_grid or not sc_grid:
        raise ValueError("lambda_p_grid and sigma_crit_grid must be non-empty")
    if any(sc <= 0.0 for sc in sc_grid):
        raise ValueError("All sigma_crit_grid entries must be > 0.0")

    v2_over_c2_list = [((g.v_flat * KM_S_TO_M_S) / C_SI) ** 2 for g in SAMPLE_GALAXIES]
    min_idx = min(range(len(SAMPLE_GALAXIES)), key=lambda i: v2_over_c2_list[i])
    max_idx = max(range(len(SAMPLE_GALAXIES)), key=lambda i: v2_over_c2_list[i])
    dynamic_range = v2_over_c2_list[max_idx] / v2_over_c2_list[min_idx]

    btfr_stats = _ols_and_btfr_stats(SAMPLE_GALAXIES)

    potential_ceilings: list[dict[str, float]] = []
    for lp_bench in (1.0e-7, 2.0e-7, 1.0e-6):
        delta_phi = kappa_potential_phi(1.0, lambda_p=lp_bench) - kappa_potential_phi(
            0.0, lambda_p=lp_bench
        )
        potential_ceilings.append(
            {
                "lambda_p": lp_bench,
                "delta_phi_max_m2_s2": delta_phi,
                "v_char_kms": math.sqrt(delta_phi) / KM_S_TO_M_S,
            }
        )

    # Precompute Newtonian baseline speeds and T1 derivative components at r_max
    v_newton_cache = {
        g.name: newton_rotation_velocity(
            g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode=gas_mode
        )
        for g in SAMPLE_GALAXIES
    }

    # Literal-sign test at benchmark (sigma_crit=0.002, lambda_p=2e-7) using conformal_acceleration_1d
    unbound_literal_count = 0
    for g in SAMPLE_GALAXIES:
        def t1_g(r: float, gal: GalaxyParams = g) -> float:
            return _t1_contraction_kappa(
                r,
                M_star=gal.M_star,
                r_d=gal.r_d,
                M_gas=gal.M_gas,
                r_gas=gal.r_gas,
                sigma_crit=0.002,
            )

        acc = conformal_acceleration_1d(g.r_max, t1_g, lambda_p=2.0e-7, dr_kpc=1.0e-4)
        v_n_ms = v_newton_cache[g.name] * KM_S_TO_M_S
        v_sq_lit = (v_n_ms**2) - (g.r_max * KPC_TO_M) * float(acc["a_conformal"])
        if v_sq_lit <= 0.0:
            unbound_literal_count += 1

    # Grid scan even with sign illegally flipped: v^2 = v_N^2 + r |dPhi_kappa/dr|
    best_mean_err = float("inf")
    best_fit: dict[str, object] = {}
    for sc in sc_grid:
        for lp in lp_grid:
            errs: list[float] = []
            dwarf_errs: list[float] = []
            mid_errs: list[float] = []
            high_errs: list[float] = []
            w20 = 0
            w50 = 0
            for g in SAMPLE_GALAXIES:
                def t1_scan(r: float, gal: GalaxyParams = g, sig_c: float = sc) -> float:
                    return _t1_contraction_kappa(
                        r,
                        M_star=gal.M_star,
                        r_d=gal.r_d,
                        M_gas=gal.M_gas,
                        r_gas=gal.r_gas,
                        sigma_crit=sig_c,
                    )

                acc = conformal_acceleration_1d(g.r_max, t1_scan, lambda_p=lp, dr_kpc=1.0e-4)
                a_mag = abs(float(acc["a_phi"]))
                v_n_ms = v_newton_cache[g.name] * KM_S_TO_M_S
                v_pred_kms = math.sqrt((v_n_ms**2) + (g.r_max * KPC_TO_M) * a_mag) / KM_S_TO_M_S
                err = abs(v_pred_kms - g.v_flat) / g.v_flat
                errs.append(err)
                if err < 0.20:
                    w20 += 1
                if err < 0.50:
                    w50 += 1
                if g.M_star < 1.0:
                    dwarf_errs.append(err)
                elif g.M_star < 10.0:
                    mid_errs.append(err)
                else:
                    high_errs.append(err)

            mean_err = sum(errs) / len(errs)
            if mean_err < best_mean_err:
                best_mean_err = mean_err
                best_fit = {
                    "sigma_crit": sc,
                    "lambda_p": lp,
                    "mean_error": mean_err,
                    "within_20_count": w20,
                    "within_50_count": w50,
                    "dwarf_mean_error": sum(dwarf_errs) / len(dwarf_errs),
                    "mid_mean_error": sum(mid_errs) / len(mid_errs),
                    "high_mean_error": sum(high_errs) / len(high_errs),
                }

    return {
        "audit": "sparc_mass_scaling",
        "gas_mode": gas_mode,
        "n_galaxies": len(SAMPLE_GALAXIES),
        "v2_over_c2_min": v2_over_c2_list[min_idx],
        "v2_over_c2_min_galaxy": SAMPLE_GALAXIES[min_idx].name,
        "v2_over_c2_max": v2_over_c2_list[max_idx],
        "v2_over_c2_max_galaxy": SAMPLE_GALAXIES[max_idx].name,
        "v2_over_c2_dynamic_range": dynamic_range,
        "btfr": btfr_stats,
        "mass_independent_potential_ceilings": potential_ceilings,
        "unbound_literal_count": unbound_literal_count,
        "literal_benchmark_params": {"sigma_crit": 0.002, "lambda_p": 2.0e-7},
        "best_sign_flipped_mean_error": best_mean_err,
        "best_sign_flipped_fit": best_fit,
        "passed": unbound_literal_count == 0 and best_mean_err < 0.25,
        "reason": (
            f"Bounded kappa in [0, 1] caps Delta Phi_kappa = c^2 ln(1 + lambda_P) independently of M_bar, "
            f"failing the {dynamic_range:.2f}x v_flat^2/c^2 dynamic range and BTFR scaling; "
            f"literal sign unbinds {unbound_literal_count}/{len(SAMPLE_GALAXIES)} galaxies, and even "
            f"sign-flipped best fit yields {best_mean_err * 100:.2f}% mean error."
        ),
    }


def audit_clock_scale_gap(
    *,
    galactic_lambda_p: float = 2.0e-7,
    max_kappa_diff: float = 0.5,
    lab_grad_kappa_per_m: float = 1.0e-12,
) -> dict[str, object]:
    """Audit 4: Compare galactic ``λ_P`` against NIST/PTB atomic-clock & GPS bounds.

    Uses ``experimental_constraints.constrain_lambda_p_from_clocks`` and
    ``det8_core.proper_time_increment`` (via ``proper_time_step``).
    """
    glp = _validate_lambda_p(galactic_lambda_p, positive_only=True)
    dk = _validate_finite_float("max_kappa_diff", max_kappa_diff)
    if dk <= 0.0 or dk > 1.0:
        raise ValueError(f"max_kappa_diff must satisfy 0.0 < max_kappa_diff <= 1.0, got {dk!r}")
    grad_k = _validate_finite_float("lab_grad_kappa_per_m", lab_grad_kappa_per_m)
    if grad_k < 0.0:
        raise ValueError(f"lab_grad_kappa_per_m must be >= 0.0, got {grad_k!r}")

    clock_bounds = constrain_lambda_p_from_clocks(max_kappa_difference=dk)
    nist_lambda_p_bound = float(clock_bounds["best_bound"])
    nist_product_bound = min(c.fractional_uncertainty for c in PUBLISHED_CLOCK_COMPARISONS)
    nist_gap_ratio = glp / nist_lambda_p_bound
    det8_core_default_gap_ratio = LAMBDA_P / nist_lambda_p_bound

    # Verify proper-time step ratio Δτ_0 / Δτ_1 = 1 + λ_P Δκ via det8_core.proper_time_increment
    dtau_pristine = proper_time_step(0.0, delta_n=1.0, lambda_p=glp)
    dtau_damaged = proper_time_step(dk, delta_n=1.0, lambda_p=glp)
    predicted_fractional_clock_shift = abs(dtau_pristine - dtau_damaged) / dtau_pristine

    gps_exact_product_bound = (GPS_CLOCK_RESIDUAL_NS * 1.0e-9) / SECONDS_PER_DAY
    gps_lambda_p_bound = GPS_CLOCK_PRODUCT_BOUND / GPS_DELTA_KAPPA_ASSUMED
    gps_gap_ratio = glp / gps_lambda_p_bound

    lab_acceleration_m_s2 = (C_SI**2) * glp * grad_k
    grad_benchmarks = [
        {
            "grad_kappa_per_m": gk,
            "acceleration_m_s2": (C_SI**2) * glp * gk,
            "acceleration_g": ((C_SI**2) * glp * gk) / 9.80665,
        }
        for gk in (1.0, 1.0e-6, 1.0e-12, 1.0e-18)
    ]

    return {
        "audit": "clock_scale_gap",
        "galactic_lambda_p": glp,
        "max_kappa_diff_assumed": dk,
        "nist_best_experiment": clock_bounds["best_experiment"],
        "nist_product_bound": nist_product_bound,
        "nist_clock_bound": nist_lambda_p_bound,
        "nist_gap_ratio": nist_gap_ratio,
        "det8_core_default_lambda_p": LAMBDA_P,
        "det8_core_default_gap_ratio": det8_core_default_gap_ratio,
        "predicted_fractional_clock_shift_at_galactic_lp": predicted_fractional_clock_shift,
        "gps_product_bound": GPS_CLOCK_PRODUCT_BOUND,
        "gps_exact_product_bound": gps_exact_product_bound,
        "gps_delta_kappa_assumed": GPS_DELTA_KAPPA_ASSUMED,
        "gps_clock_bound": gps_lambda_p_bound,
        "gps_gap_ratio": gps_gap_ratio,
        "lab_grad_kappa_per_m": grad_k,
        "lab_acceleration_m_s2": lab_acceleration_m_s2,
        "lab_gradient_benchmarks": grad_benchmarks,
        "eotvos_reference_count": len(PUBLISHED_EOTVOS),
        "partial_quarantine_caveat": (
            "experimental_constraints.py is PARTIALLY_QUARANTINED: NIST/PTB and GPS limits "
            "bound the product lambda_P * Delta_kappa, where Delta_kappa is assumed rather than measured."
        ),
        "passed": nist_gap_ratio <= 1.0 and gps_gap_ratio <= 1.0,
        "reason": (
            f"Galactic lambda_P = {glp:.1e} exceeds NIST Yb/Sr bound {nist_lambda_p_bound:.2e} "
            f"(at Delta_kappa = {dk}) by {nist_gap_ratio:.3e}x and conditional GPS bound "
            f"{gps_lambda_p_bound:.2e} (at delta_kappa = {GPS_DELTA_KAPPA_ASSUMED:.1e}) by "
            f"{gps_gap_ratio:.2f}x; implied lab accel at |grad kappa|={grad_k:.1e} m^-1 is "
            f"{lab_acceleration_m_s2:.3e} m/s^2."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Modified Variant Exploration (Variants a, b, c)
# ═══════════════════════════════════════════════════════════════════════════


def explore_modified_variants() -> dict[str, object]:
    """Evaluate whether natural Pathway 2 modifications overcome the 4 obstructions.

    Tests:
      (a) Decoupled ``Π_grav`` vs ``Π_clock``
      (b) Non-conformal spatial metric ``g_ij`` via ``BondNetwork`` conductivity ``σ_ij``
      (c) Mass-coupled ``λ_P(M_bar)`` and screened Poisson / MONDian ``κ`` PDE
    """
    # Variant (a): Decouple Pi_grav vs Pi_clock
    clock_lp = float(constrain_lambda_p_from_clocks(max_kappa_difference=0.5)["best_bound"])
    grav_lp = 2.0e-7
    clock_shift_at_05 = (
        proper_time_step(0.0, lambda_p=clock_lp) - proper_time_step(0.5, lambda_p=clock_lp)
    ) / proper_time_step(0.0, lambda_p=clock_lp)
    variant_a = {
        "name": "decoupled_pi_grav_vs_pi_clock",
        "clock_lambda_p": clock_lp,
        "grav_lambda_p": grav_lp,
        "clock_shift_delta_kappa_0_5": clock_shift_at_05,
        "resolves_clock_gap": True,
        "resolves_sign_if_inverted": True,
        "still_fails_conformal_lensing": True,
        "gamma_ppn_if_conformal": -1.0,
        "still_fails_sparc_mass_scaling": True,
        "native_vs_empirical_note": (
            "Empirical closure (FIT/CORR): requires introducing a second aperture Pi_grav "
            "outside det8_core.participation_aperture, breaking clock-gravity unification."
        ),
    }

    # Variant (b): Non-conformal spatial metric g_ij (BondNetwork sigma_ij check + PPN sweep)
    u_weak = -1.0e-6  # Phi_eff / c^2
    pi_t = math.exp(u_weak)

    # Construct explicit BondNetwork showing sigma_ij is only a flux cap in bonds.py
    net = BondNetwork()
    bond_01 = net.add_bond(0, 1, sigma=1.0 / (pi_t**2), C=1.0, pi=0.0)
    bond_12 = net.add_bond(1, 2, sigma=1.0, C=1.0, pi=0.0)

    metric_sweep: list[dict[str, float | bool]] = []
    for gamma_param in (-1.0, 0.0, 1.0):
        pi_s = math.exp(-gamma_param * u_weak)
        g_00 = -(pi_t**2)
        g_ij = pi_s**2
        gamma_eff = -(g_ij - 1.0) / (2.0 * u_weak)
        deflection_factor = 0.5 * (1.0 + gamma_eff)
        passes_cassini = abs(gamma_eff - 1.0) < CASSINI_GAMMA_PPN_BOUND
        metric_sweep.append(
            {
                "gamma_param": gamma_param,
                "pi_t": pi_t,
                "pi_s": pi_s,
                "g_00": g_00,
                "g_ij": g_ij,
                "gamma_eff": gamma_eff,
                "deflection_factor": deflection_factor,
                "passes_cassini": passes_cassini,
            }
        )

    variant_b = {
        "name": "non_conformal_spatial_metric_bond_sigma",
        "u_weak_field": u_weak,
        "bond_network_check": {
            "n_bonds": len(net),
            "bond_01_sigma": bond_01.sigma if isinstance(bond_01, BondRecord) else 0.0,
            "bond_12_sigma": bond_12.sigma,
            "bonds_py_has_mass_coupling": False,
        },
        "gamma_param_sweep": metric_sweep,
        "resolves_lensing_at_gamma_plus_1": True,
        "still_fails_sign_clock_and_mass_scaling": True,
        "native_vs_empirical_note": (
            "Borrowed GR / un-derived closure (CORR): setting Pi_s = Pi_t^(-1) passes "
            "Cassini kinematically, but det8/models/bonds.py only enforces |J| <= sigma_ij "
            "and lacks any native DET equation deriving sigma_ij -> Pi_t^(-2) from baryonic mass."
        ),
    }

    # Variant (c): Mass-coupled lambda_P(M_bar) and screened Poisson / MONDian PDE
    lp_m_values: list[float] = []
    lp_m_errs: list[float] = []
    deep_mond_errs: list[float] = []

    for g in SAMPLE_GALAXIES:
        m_bar_kg = (g.M_star + g.M_gas) * 1.0e9 * M_SUN_KG
        lp_m = math.sqrt(G_SI * m_bar_kg * MOND_A0_SI) / (C_SI**2)
        lp_m_values.append(lp_m)

        def t1_var_c(r: float, gal: GalaxyParams = g) -> float:
            return _t1_contraction_kappa(
                r,
                M_star=gal.M_star,
                r_d=gal.r_d,
                M_gas=gal.M_gas,
                r_gas=gal.r_gas,
                sigma_crit=0.002,
            )

        acc = conformal_acceleration_1d(g.r_max, t1_var_c, lambda_p=lp_m, dr_kpc=1.0e-4)
        v_n_ms = (
            newton_rotation_velocity(
                g.r_max, g.M_star, g.r_d, g.M_gas, g.r_gas, gas_mode="1d"
            )
            * KM_S_TO_M_S
        )
        v_pred_kms = (
            math.sqrt((v_n_ms**2) + (g.r_max * KPC_TO_M) * abs(float(acc["a_phi"])))
            / KM_S_TO_M_S
        )
        lp_m_errs.append(abs(v_pred_kms - g.v_flat) / g.v_flat)

        v_mond_kms = ((G_SI * m_bar_kg * MOND_A0_SI) ** 0.25) / KM_S_TO_M_S
        deep_mond_errs.append(abs(v_mond_kms - g.v_flat) / g.v_flat)

    # Logarithmic MONDian potential depth obstruction on NGC 2841 (v_flat = 290 km/s)
    ngc2841 = next(g for g in SAMPLE_GALAXIES if g.name == "NGC 2841")
    ngc2841_log_depth_over_c2 = (((ngc2841.v_flat * KM_S_TO_M_S) / C_SI) ** 2) * math.log(
        50.0 / 0.1
    )

    variant_c = {
        "name": "mass_coupled_lambda_p_and_screened_poisson",
        "lambda_p_mass_min": min(lp_m_values),
        "lambda_p_mass_max": max(lp_m_values),
        "t1_mass_coupled_mean_error": sum(lp_m_errs) / len(lp_m_errs),
        "deep_mond_btfr_mean_error": sum(deep_mond_errs) / len(deep_mond_errs),
        "ngc2841_log_potential_depth_over_c2_01_to_50kpc": ngc2841_log_depth_over_c2,
        "bounded_kappa_obstruction": (
            "Under Pi = (1 + lambda_P kappa)^(-1) with kappa in [0, 1] and fixed lambda_P, "
            "|Delta Phi_kappa| <= c^2 ln(1 + lambda_P) is strictly bounded and cannot represent "
            "an unbounded logarithmic MOND potential without dropping kappa in [0, 1] or replacing "
            "det8_core's clock ansatz with a nonlinear Poisson PDE importing MOND a_0."
        ),
        "native_vs_empirical_note": (
            "Non-local empirical closure (FIT/CORR): lambda_P(M_bar) depends on global integrated "
            "mass rather than local DET node variables, and still gives ~36.7% mean SPARC error "
            "with T1 kappa(r) because r |d kappa/dr| vanishes once kappa -> 1."
        ),
    }

    return {
        "variant_a_decoupled_pi": variant_a,
        "variant_b_non_conformal_metric": variant_b,
        "variant_c_mass_coupled_or_poisson": variant_c,
        "any_det_native_survivor": False,
        "combined_survivor_summary": (
            "No single local modification saves Pathway 2: a surviving theory must combine (b) "
            "anisotropic spatial metric Pi_s = Pi_t^(-1) with a native sigma_ij derivation, (a) "
            "clock-gravity decoupling or gradient screening, sign resolution without F6, and (c) "
            "an unbounded/screened potential scaling with M_bar — which abandons the literal "
            "Pi-conformal clock-metric bridge."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# Quantitative Refutation / Acceptance Verdict & Closure Manifest
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_pathway2_criteria() -> dict[str, object]:
    """Run all 4 Pathway 2 audits + variant exploration and return explicit verdict."""
    sign_audit = audit_sign_consistency()
    lensing_audit = audit_conformal_ppn_lensing()
    sparc_audit = audit_sparc_mass_scaling()
    clock_audit = audit_clock_scale_gap()
    variants = explore_modified_variants()

    criteria = {
        "C1_sign": {
            "criterion": "Inward acceleration (a_conformal <= 0) under T1 d kappa/dr > 0 without F6.",
            "threshold": "t1_repulsive_count == 0 and f6_reintroduces_inside_out_failure is False",
            "observed": {
                "t1_repulsive_count": sign_audit["t1_repulsive_count"],
                "f6_attractive_count": sign_audit["f6_attractive_count"],
                "f6_reintroduces_inside_out_failure": sign_audit["f6_reintroduces_inside_out_failure"],
            },
            "passed": bool(sign_audit["passed"]),
            "status": "PASS" if sign_audit["passed"] else "REFUTED",
        },
        "C2_lensing": {
            "criterion": "Match Cassini PPN gamma (|gamma - 1| < 2.3e-5) and VLBI light deflection (< 1e-4).",
            "threshold": f"|gamma_PPN - 1| < {CASSINI_GAMMA_PPN_BOUND:.1e} and miss < {VLBI_DEFLECTION_PRECISION:.1e}",
            "observed": {
                "gamma_ppn": lensing_audit["gamma_ppn"],
                "abs_gamma_minus_one": lensing_audit["abs_gamma_minus_one"],
                "cassini_violation_ratio": lensing_audit["cassini_violation_ratio"],
                "vlbi_fractional_miss": lensing_audit["vlbi_fractional_miss"],
            },
            "passed": bool(lensing_audit["passed"]),
            "status": "PASS" if lensing_audit["passed"] else "REFUTED",
        },
        "C3_sparc_btfr": {
            "criterion": "Reproduce SPARC 43-galaxy BTFR scaling (0 unbound literal, <25% mean error).",
            "threshold": "unbound_literal_count == 0 and best_sign_flipped_mean_error < 0.25",
            "observed": {
                "v2_over_c2_dynamic_range": sparc_audit["v2_over_c2_dynamic_range"],
                "unbound_literal_count": sparc_audit["unbound_literal_count"],
                "best_sign_flipped_mean_error": sparc_audit["best_sign_flipped_mean_error"],
            },
            "passed": bool(sparc_audit["passed"]),
            "status": "PASS" if sparc_audit["passed"] else "REFUTED",
        },
        "C4_clock_gap": {
            "criterion": "Reconcile galactic lambda_P with NIST/PTB optical-clock and GPS bounds.",
            "threshold": "nist_gap_ratio <= 1.0 and gps_gap_ratio <= 1.0",
            "observed": {
                "galactic_lambda_p": clock_audit["galactic_lambda_p"],
                "nist_clock_bound": clock_audit["nist_clock_bound"],
                "nist_gap_ratio": clock_audit["nist_gap_ratio"],
                "gps_gap_ratio": clock_audit["gps_gap_ratio"],
            },
            "passed": bool(clock_audit["passed"]),
            "status": "PASS" if clock_audit["passed"] else "REFUTED",
        },
    }

    refuted = [name for name, item in criteria.items() if not item["passed"]]
    passed = [name for name, item in criteria.items() if item["passed"]]
    overall_status = "VIABLE" if not refuted else "REFUTED"

    return {
        "pathway": "Pathway 2 (Pi-Conformal Clock-Metric Bridge)",
        "status": overall_status,
        "refuted_criteria": refuted,
        "passed_criteria": passed,
        "criteria": criteria,
        "audits": {
            "sign_consistency": sign_audit,
            "conformal_ppn_lensing": lensing_audit,
            "sparc_mass_scaling": sparc_audit,
            "clock_scale_gap": clock_audit,
        },
        "variants": variants,
        "survivor_conditions": [
            "Break conformal flatness g_mu_nu = Pi^2 eta_mu_nu by deriving spatial metric Psi(sigma_ij) = Pi_t^(-1) from DET bond conductivity.",
            "Resolve sign contradiction without reintroducing retired F6 inside-out decreasing kappa (r_SFR > r_d).",
            "Decouple gravitational lapse Pi_grav from atomic-clock Pi_clock (or screen local grad kappa) to satisfy NIST lambda_P*Delta_kappa < 2e-18.",
            "Replace bounded kappa in [0, 1] mass-independent Delta Phi_kappa with an unbounded or screened potential scaling with baryonic mass M_bar (BTFR).",
        ],
    }


def closure_manifest() -> list[dict[str, object]]:
    """Explicit Native (P/TH-DET) vs Borrowed GR (CORR) vs Fitted (FIT) vs External Anchor ledger."""
    return [
        {
            "symbol_or_relation": "M0 event-count monotonicity (Delta N != Delta kappa)",
            "epistemic_tag": "TH-DET",
            "evidence_level": "Level 3",
            "origin": "DET-native",
            "equation_or_value": "N_i monotone non-decreasing; kappa_i mutable in [0, 1]",
            "status_m_or_caveat": "Native DET8 M0 consistency invariant (det8_core.py:26-30).",
            "independent_discriminator": "Recovery (decreasing kappa) does not produce negative proper time.",
        },
        {
            "symbol_or_relation": "Delta tau = Pi * Delta N & Pi(kappa)",
            "epistemic_tag": "P",
            "evidence_level": "Level 3",
            "origin": "DET-native ansatz",
            "equation_or_value": "Pi_i = sigma_i * eta_i / ((1+F_i)(1+H_i) * gamma_v * (1 + lambda_P * kappa_i))",
            "status_m_or_caveat": "Proposed clock-drag ansatz in det8_core.py:136,166 (not uniquely derived from axioms).",
            "independent_discriminator": "Atomic-clock frequency shift Delta nu / nu = lambda_P * Delta kappa / (1 + lambda_P * kappa).",
        },
        {
            "symbol_or_relation": "a = -c^2 grad(ln Pi) & Phi_kappa = c^2 ln(1 + lambda_P kappa)",
            "epistemic_tag": "CORR",
            "evidence_level": "Level 3",
            "origin": "Borrowed GR",
            "equation_or_value": "Weak-field geodesic identification g_00 = -Pi^2 => a_conformal = -c^2 d(ln Pi)/dr = -a_phi",
            "status_m_or_caveat": "Imported from GR weak-field lapse; produces wrong repulsive sign under T1 d kappa/dr > 0.",
            "independent_discriminator": "Galactic sign consistency on KNOWN_GALAXIES (8/8 repulsive under T1).",
        },
        {
            "symbol_or_relation": "g_mu_nu = Pi(x)^2 * eta_mu_nu",
            "epistemic_tag": "CORR",
            "evidence_level": "Level 3",
            "origin": "Borrowed GR",
            "equation_or_value": "Conformal Minkowski metric => ds^2 = 0 invariant, gamma_PPN = -1.0",
            "status_m_or_caveat": "Refuted by solar-system null deflection; superseded by order_count_geometry.py (T7).",
            "independent_discriminator": "Cassini Shapiro delay |gamma - 1| < 2.3e-5 and VLBI solar-limb deflection.",
        },
        {
            "symbol_or_relation": "Non-conformal spatial metric Psi(sigma_ij) = Pi_t^(-1) (Variant b)",
            "epistemic_tag": "CORR",
            "evidence_level": "Level 3",
            "origin": "Borrowed GR / Un-derived",
            "equation_or_value": "ds^2 = -Pi_t^2 c^2 dt^2 + Pi_t^(-2) dx^2 => gamma_PPN = +1.0",
            "status_m_or_caveat": "det8/models/bonds.py only enforces |J| <= sigma_ij; no DET derivation links sigma_ij to M_bar or Pi_t.",
            "independent_discriminator": "Derivation of sigma_ij field equation reproducing Psi = Pi_t^(-1).",
        },
        {
            "symbol_or_relation": "lambda_P (galactic coupling vs det8_core.LAMBDA_P = 1.0)",
            "epistemic_tag": "FIT",
            "evidence_level": "Level 3",
            "origin": "Empirical closure",
            "equation_or_value": "Galactic ~1e-7..1e-6 vs NIST < 4.0e-18 (at Delta kappa = 0.5)",
            "status_m_or_caveat": "No native DET value; 5.0e10x scale clash between galactic fits and optical clocks.",
            "independent_discriminator": "NIST/PTB clock comparison and SPARC rotation curve amplitudes.",
        },
        {
            "symbol_or_relation": "T1 contraction parameters (Sigma_crit, w_SFR) & MOND/lambda_P(M_bar)",
            "epistemic_tag": "FIT",
            "evidence_level": "Level 3",
            "origin": "Empirical closure",
            "equation_or_value": "kappa(r) = exp(-(Sigma_* + Sigma_gas)/Sigma_crit - w_SFR Sigma_SFR), a_0 = 1.2e-10 m/s^2",
            "status_m_or_caveat": "Phenomenological mapping from baryonic surface densities to N_int/N_rec; bounded kappa fails BTFR.",
            "independent_discriminator": "SPARC 43-galaxy BTFR slope & scatter (0.3089 dex) vs sign-flipped fit (36.30% error).",
        },
        {
            "symbol_or_relation": "C_SI, G_SI, M_SUN_KG, KPC_TO_M, KNOWN_GALAXIES, SAMPLE_GALAXIES",
            "epistemic_tag": "EXTERNAL_ANCHOR",
            "evidence_level": "Level 2",
            "origin": "External empirical / SI",
            "equation_or_value": "c = 2.99792458e8 m/s, G = 6.67430e-11 m^3/(kg s^2), 8 + 43 galaxy fixtures",
            "status_m_or_caveat": "External SI constants and Level-2 SPARC/literature galaxy reductions (galaxy_observables.py).",
            "independent_discriminator": "Theory-independent Level-2 rotation velocities v_flat and disk photometry.",
        },
        {
            "symbol_or_relation": "CASSINI_GAMMA_PPN_BOUND & VLBI_DEFLECTION_PRECISION",
            "epistemic_tag": "EXTERNAL_ANCHOR",
            "evidence_level": "Level 2",
            "origin": "External literature",
            "equation_or_value": "|gamma_PPN - 1| < 2.3e-5 (Bertotti et al. 2003); VLBI 1.0e-4",
            "status_m_or_caveat": "Declared locally without importing retired post_newtonian.py.",
            "independent_discriminator": "Solar-conjunction Shapiro time delay and VLBI radio deflection.",
        },
        {
            "symbol_or_relation": "PUBLISHED_CLOCK_COMPARISONS (NIST/PTB) & GPS_CLOCK_PRODUCT_BOUND",
            "epistemic_tag": "EXTERNAL_ANCHOR",
            "evidence_level": "Level 2",
            "origin": "External literature",
            "equation_or_value": "NIST Yb/Sr 2.0e-18; GPS illustrative 0.3 ns/day => lambda_P * delta_kappa < 3.5e-15",
            "status_m_or_caveat": "PARTIAL_QUARANTINE: bounds product lambda_P * Delta kappa with assumed Delta kappa.",
            "independent_discriminator": "Optical lattice clock ratios under independently controlled structural history Delta kappa.",
        },
    ]


__all__ = (
    "CASSINI_GAMMA_PPN_BOUND",
    "GPS_CLOCK_PRODUCT_BOUND",
    "GPS_CLOCK_RESIDUAL_NS",
    "GPS_DELTA_KAPPA_ASSUMED",
    "MOND_A0_SI",
    "SECONDS_PER_DAY",
    "SOLAR_RADIUS_M",
    "VLBI_DEFLECTION_PRECISION",
    "audit_clock_scale_gap",
    "audit_conformal_ppn_lensing",
    "audit_sign_consistency",
    "audit_sparc_mass_scaling",
    "closure_manifest",
    "conformal_acceleration_1d",
    "conformal_clock_lapse",
    "evaluate_pathway2_criteria",
    "explore_modified_variants",
    "kappa_potential_phi",
    "proper_time_step",
)
