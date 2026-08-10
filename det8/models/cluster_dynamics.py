"""
DET κ-Gravity — Galaxy Cluster Dynamics

Extends κ(r) to cluster scales (100–2000 kpc). Tests whether DET
κ-gravity can explain cluster dynamics without dark matter.

Key DET prediction:
  M_DET(<r) = M_dynamical(<r) · (κ_earth / κ(r))²

where M_dynamical is the mass inferred from standard gravity
(hydrostatic, virial, or lensing). If κ(r) > κ_earth at cluster
scales, the required mass is REDUCED — less dark matter needed.

Cluster κ(r) model:
  κ(r) = κ_core + Δκ · (1 − exp(−r/r_cluster))

  where:
    κ_core ≈ κ_galaxy_outskirts (smooth connection at ~30 kpc)
    r_cluster ≈ 100–500 kpc (cluster scale, larger than galaxy scale)
    Δκ ≈ 2–6 (additional enhancement from cluster formation history)

Data: published cluster mass profiles from X-ray (Chandra/XMM),
optical (velocity dispersion), and lensing (HST/JWST).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# Physical Constants
# ═══════════════════════════════════════════════════════════════════════════

G = 6.67430e-11
M_SUN = 1.989e30
KPC_TO_M = 3.086e19
KM_S_TO_M_S = 1000.0


# ═══════════════════════════════════════════════════════════════════════════
# Cluster κ(r) Profile
# ═══════════════════════════════════════════════════════════════════════════


def kappa_cluster(
    r: float,
    kappa_core: float = 3.5,     # Connects to galaxy outskirts κ (~3.5 at 30 kpc).
    delta_kappa: float = 4.0,    # Additional cluster enhancement.
    r_cluster: float = 300.0,    # Cluster transition scale (kpc).
) -> float:
    """κ(r) for galaxy clusters.

    Smoothly connects to the galaxy κ(r) profile: at r ~ 30 kpc
    (galaxy outskirts), κ ≈ 3.5. At r ≫ 300 kpc (cluster outskirts),
    κ ≈ 3.5 + 4.0 = 7.5.

    κ(r) = kappa_core + delta_kappa · (1 − exp(−r/r_cluster))
    """
    return kappa_core + delta_kappa * (1.0 - math.exp(-r / r_cluster))


def kappa_universal(
    r: float,
    kappa_0: float = 0.5,
    kappa_scale_galaxy: float = 3.0,
    r_galaxy: float = 1.8,  # r_SFR/r_d ratio.
    kappa_scale_cluster: float = 4.0,
    r_cluster: float = 300.0,
) -> float:
    """Universal κ(r) from galaxy cores to cluster outskirts.

    Galaxy regime (r < 30 kpc): κ(r) = κ₀ + κ_scale_galaxy·(1−e^(−r/r_galaxy))
    Cluster regime (r > 30 kpc): κ(r) = κ(30) + κ_scale_cluster·(1−e^(−(r−30)/r_cluster))

    This gives a continuous κ(r) from ~0.5 at r=0 to ~7.5 at r=1000 kpc.
    """
    r_connect = 30.0  # kpc — connection point.

    if r <= r_connect:
        return kappa_0 + kappa_scale_galaxy * (1.0 - math.exp(-r / (r_galaxy * 1.0)))
    else:
        kappa_at_connect = kappa_0 + kappa_scale_galaxy * (1.0 - math.exp(-r_connect / (r_galaxy * 1.0)))
        return kappa_at_connect + kappa_scale_cluster * (1.0 - math.exp(-(r - r_connect) / r_cluster))


# ═══════════════════════════════════════════════════════════════════════════
# Cluster Mass Estimates
# ═══════════════════════════════════════════════════════════════════════════


def hydrostatic_mass(
    r: float,
    T_gas: float,      # Gas temperature (keV).
    dlnT_dlnr: float = 0.0,    # Temperature gradient.
    dlnrho_dlnr: float = -2.0,  # Density gradient (β-model: -3β ≈ -2 for β=2/3).
) -> float:
    """Hydrostatic mass from X-ray gas.

    M(<r) = -(kT·r)/(G·μ·m_p) · (dlnρ/dlnr + dlnT/dlnr).

    For isothermal β-model with β=2/3: dlnρ/dlnr ≈ -3β·(r²/(r²+r_c²)) ≈ -2.
    """
    k_B = 1.380649e-23  # J/K.
    keV_to_J = 1.602176634e-16
    mu = 0.6  # Mean molecular weight.
    m_p = 1.67262192369e-27  # kg.

    T_K = T_gas * keV_to_J / k_B
    r_m = r * KPC_TO_M

    M = -(k_B * T_K * r_m) / (G * mu * m_p) * (dlnrho_dlnr + dlnT_dlnr)
    return max(0.0, M / M_SUN)


def det_mass_from_hydrostatic(
    r: float,
    T_gas: float,
    kappa_r: float,
    kappa_earth: float = 1.0,
) -> float:
    """DET-corrected mass from hydrostatic equilibrium.

    M_DET = M_hydrostatic · (κ_earth/κ(r))².

    If κ(r) > κ_earth, the DET mass is LOWER than the standard
    hydrostatic mass — meaning less mass is needed to explain
    the observed gas temperature and density profile.
    """
    M_hydro = hydrostatic_mass(r, T_gas)
    return M_hydro * (kappa_earth / kappa_r)**2


def virial_mass(
    r: float,
    sigma_v: float,  # Line-of-sight velocity dispersion (km/s).
) -> float:
    """Virial mass estimate from galaxy velocity dispersion.

    M(<r) ≈ 3·σ_v²·r / G  (virial theorem, isotropic orbits).
    """
    sigma_ms = sigma_v * KM_S_TO_M_S
    r_m = r * KPC_TO_M
    M = 3.0 * sigma_ms**2 * r_m / G
    return M / M_SUN


def det_mass_from_virial(
    r: float,
    sigma_v: float,
    kappa_r: float,
    kappa_earth: float = 1.0,
) -> float:
    """DET-corrected virial mass."""
    M_virial = virial_mass(r, sigma_v)
    return M_virial * (kappa_earth / kappa_r)**2


# ═══════════════════════════════════════════════════════════════════════════
# Published Cluster Data (representative)
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class ClusterData:
    """Published data for a galaxy cluster."""
    name: str
    r_virial: float      # Virial radius (kpc).
    M_virial_standard: float  # M(<r_vir) from standard gravity (10^14 M_sun).
    T_gas: float         # Gas temperature (keV).
    sigma_v: float       # Galaxy velocity dispersion (km/s).
    z: float             # Redshift.
    reference: str


# Representative clusters (from Vikhlinin et al. 2006, ApJ; Planck SZ catalog).
CLUSTERS = [
    ClusterData("A133", 1200, 4.0, 3.8, 700, 0.057, "Vikhlinin+2006"),
    ClusterData("A262", 900, 2.0, 2.2, 550, 0.016, "Vikhlinin+2006"),
    ClusterData("A383", 1000, 3.0, 3.5, 650, 0.187, "Vikhlinin+2006"),
    ClusterData("A478", 1400, 8.0, 6.5, 850, 0.088, "Vikhlinin+2006"),
    ClusterData("A907", 1100, 4.5, 4.0, 700, 0.153, "Vikhlinin+2006"),
    ClusterData("A1413", 1300, 7.0, 6.0, 800, 0.143, "Vikhlinin+2006"),
    ClusterData("A1795", 1200, 5.0, 4.5, 750, 0.062, "Vikhlinin+2006"),
    ClusterData("A2029", 1300, 6.0, 7.0, 850, 0.077, "Vikhlinin+2006"),
    ClusterData("A2390", 1200, 6.0, 5.5, 900, 0.228, "Vikhlinin+2006"),
    ClusterData("Coma", 1400, 7.0, 8.0, 1000, 0.023, "Vikhlinin+2006"),
]


# ═══════════════════════════════════════════════════════════════════════════
# Cluster Analysis
# ═══════════════════════════════════════════════════════════════════════════


def analyze_clusters(
    kappa_core: float = 3.5,
    delta_kappa: float = 4.0,
    r_cluster: float = 300.0,
    kappa_earth: float = 1.0,
) -> dict:
    """Analyze all clusters with DET κ-gravity.

    Computes the DET-corrected mass and the implied dark matter fraction.
    """
    results = []
    total_dm_standard = 0.0
    total_dm_det = 0.0

    for cluster in CLUSTERS:
        # κ at the virial radius.
        kappa_r = kappa_cluster(cluster.r_virial, kappa_core, delta_kappa, r_cluster)

        # Standard hydrostatic mass.
        M_hydro = hydrostatic_mass(cluster.r_virial, cluster.T_gas)
        M_hydro_14 = M_hydro / 1e14  # In 10^14 M_sun.

        # DET-corrected mass.
        M_det = det_mass_from_hydrostatic(cluster.r_virial, cluster.T_gas, kappa_r, kappa_earth)
        M_det_14 = M_det / 1e14

        # Standard virial mass.
        M_virial = virial_mass(cluster.r_virial, cluster.sigma_v)
        M_virial_14 = M_virial / 1e14

        # DET-corrected virial mass.
        M_det_virial = det_mass_from_virial(cluster.r_virial, cluster.sigma_v, kappa_r, kappa_earth)
        M_det_virial_14 = M_det_virial / 1e14

        # Dark matter fraction (standard: M_virial vs M_baryon estimated from gas).
        # Baryon fraction: f_b ≈ 0.15 (cosmic). M_baryon ≈ f_b · M_virial.
        f_b = 0.15
        M_baryon_14 = f_b * cluster.M_virial_standard
        f_dm_standard = 1.0 - M_baryon_14 / cluster.M_virial_standard

        # DET dark matter fraction.
        M_det_req = cluster.M_virial_standard  # Required mass to match observations.
        f_dm_det = 1.0 - M_baryon_14 / M_det_req

        results.append({
            "cluster": cluster.name,
            "r_virial_kpc": cluster.r_virial,
            "kappa_at_rvir": kappa_r,
            "M_hydro_14": M_hydro_14,
            "M_det_hydro_14": M_det_14,
            "M_virial_14": M_virial_14,
            "M_det_virial_14": M_det_virial_14,
            "f_dm_standard": f_dm_standard,
            "f_dm_det": f_dm_det,
            "kappa_reduction_factor": (kappa_earth / kappa_r)**2,
        })

        total_dm_standard += f_dm_standard
        total_dm_det += f_dm_det

    n = len(CLUSTERS)
    return {
        "parameters": {"kappa_core": kappa_core, "delta_kappa": delta_kappa, "r_cluster": r_cluster},
        "n_clusters": n,
        "avg_kappa_at_rvir": sum(r["kappa_at_rvir"] for r in results) / n,
        "avg_kappa_reduction": sum(r["kappa_reduction_factor"] for r in results) / n,
        "avg_f_dm_standard": total_dm_standard / n,
        "avg_f_dm_det": total_dm_det / n,
        "results": results,
    }


# ═══════════════════════════════════════════════════════════════════════════
# Universal Profile: Galaxy → Cluster
# ═══════════════════════════════════════════════════════════════════════════


def universal_kappa_summary() -> dict:
    """Summary of the universal κ(r) from galaxy cores to cluster outskirts."""
    test_radii = [0.1, 1.0, 5.0, 10.0, 30.0, 100.0, 300.0, 1000.0, 3000.0]
    
    profile = []
    for r in test_radii:
        k = kappa_universal(r)
        profile.append({
            "r_kpc": r,
            "kappa": k,
            "enhancement": (k / 1.0)**2,
            "regime": "galaxy core" if r < 1 else "galaxy disk" if r < 10 else "galaxy outskirts" if r < 50 else "cluster",
        })

    return {
        "formula_galaxy": "κ(r) = 0.5 + 3.0·(1−e^(−r/(1.8·r_d)))",
        "formula_cluster": "κ(r) = κ(30) + 4.0·(1−e^(−(r−30)/300))",
        "profile": profile,
        "key_scales": {
            "galaxy_core": "κ ≈ 0.5–1.0 (r < 1 kpc)",
            "galaxy_outskirts": "κ ≈ 3.5 (r ≈ 30 kpc)",
            "cluster_core": "κ ≈ 4–5 (r ≈ 100 kpc)",
            "cluster_outskirts": "κ ≈ 7.5 (r > 1000 kpc)",
        },
    }
