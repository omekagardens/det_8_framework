"""
DET v8.0 — κ vs. Defect-Density Discriminator (F9)

The gating experiment for Track A: is κ anything more than ordinary
defect density?

Standard defect density ρ_d relaxes by thermal annealing with an Arrhenius
timescale that is a STRONG function of temperature:

    τ_anneal(T) = τ_0 · exp(E_a / k_B T)

DET κ relaxes by the recovery law (det8_core / kappa_diffusion):

    dκ/dt = −(κ − κ_eq)/τ_rec

with a recovery timescale τ_rec that is, by hypothesis, a DET-native
structural quantity — NOT the thermal annealing time.

The discriminator: if κ-recovery tracks τ_anneal(T) across temperature,
then κ = defect density (relabeling; the clock anomaly is just the known
defect-induced shift). If κ-recovery follows τ_rec independently of T,
then κ is distinct from ordinary materials history — the first evidence
for a novel field.

This module simulates both hypotheses and computes the discriminating
statistic: the temperature dependence of the measured recovery time.

Status: P (proposed) — this simulates the protocol that must be run on
real samples (see red-team review §6, items 1–3).
"""

from __future__ import annotations

import math
import random


K_B_EV = 8.617333262e-5  # Boltzmann constant, eV/K.


# ── Recovery timescales ─────────────────────────────────────────────────────


def annealing_timescale(
    T_K: float,
    E_a_eV: float,
    tau0_s: float,
) -> float:
    """τ_anneal(T) = τ_0·exp(E_a/(k_B·T)). Strong Arrhenius T-dependence.

    Higher T → shorter τ (faster annealing).
    """
    if T_K <= 0.0:
        raise ValueError("temperature must be > 0 K")
    return tau0_s * math.exp(E_a_eV / (K_B_EV * T_K))


def kappa_recovery_timescale(tau_rec_s: float) -> float:
    """κ recovery timescale τ_rec — by hypothesis T-independent."""
    return tau_rec_s


# ── Trajectories ────────────────────────────────────────────────────────────


def defect_density(
    t: float,
    rho0: float,
    T_K: float,
    E_a_eV: float,
    tau0_s: float,
) -> float:
    """ρ_d(t) = ρ_0·exp(−t/τ_anneal(T)) — thermal annealing."""
    tau = annealing_timescale(T_K, E_a_eV, tau0_s)
    return rho0 * math.exp(-t / tau)


def kappa_trajectory(
    t: float,
    kappa0: float,
    kappa_eq: float,
    tau_rec_s: float,
) -> float:
    """κ(t) = κ_eq + (κ_0 − κ_eq)·exp(−t/τ_rec) — DET recovery."""
    return kappa_eq + (kappa0 - kappa_eq) * math.exp(-t / tau_rec_s)


def clock_shift(
    kappa: float,
    lambda_p: float,
) -> float:
    """Δν/ν = λ_P·κ/(1 + λ_P·κ) — the DET clock signal (F10 convention)."""
    return lambda_p * kappa / (1.0 + lambda_p * kappa)


# ── The discriminator ───────────────────────────────────────────────────────


def discriminator_signature(
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    tau_rec_s: float = 1e4,
) -> dict:
    """The temperature dependence that separates κ from defect density.

    Defect model: recovery time changes by τ_anneal(T_low)/τ_anneal(T_high)
                  ≈ exp(E_a/k_B·(1/T_low − 1/T_high))  (≫ 1 over a sweep).
    κ model:       recovery time is T-independent (ratio = 1).

    If a measured recovery time is constant across the sweep, κ ≠ defect
    density; if it tracks the Arrhenius law, κ = defect density.
    """
    tau_a_low = annealing_timescale(T_low_K, E_a_eV, tau0_s)
    tau_a_high = annealing_timescale(T_high_K, E_a_eV, tau0_s)
    tau_k_low = kappa_recovery_timescale(tau_rec_s)
    tau_k_high = kappa_recovery_timescale(tau_rec_s)

    defect_ratio = tau_a_high / tau_a_low          # < 1 (faster at high T).
    kappa_ratio = tau_k_high / tau_k_low           # = 1 (T-independent).
    sweep_factor = tau_a_low / tau_a_high if tau_a_high > 0 else float("inf")

    distinguishable = (
        abs(kappa_ratio - 1.0) < 1e-12
        and abs(sweep_factor - 1.0) > 1e-3
    )

    return {
        "T_low_K": T_low_K,
        "T_high_K": T_high_K,
        "tau_anneal_low_s": tau_a_low,
        "tau_anneal_high_s": tau_a_high,
        "tau_rec_s": tau_rec_s,
        "defect_T_ratio": defect_ratio,
        "kappa_T_ratio": kappa_ratio,
        "annealing_sweep_factor": sweep_factor,
        "distinguishable": distinguishable,
        "verdict": (
            f"Thermal annealing changes the recovery time by ×{sweep_factor:.1e} "
            f"over {T_low_K:.0f}→{T_high_K:.0f} K (Arrhenius); κ-recovery is "
            f"T-independent (×{kappa_ratio:.3f}). A measured recovery time that "
            f"does NOT track the Arrhenius law is the discriminator: κ ≠ defect "
            f"density. If it DOES track it, κ = defect density (no novelty)."
        ),
    }


# ── Simulated clock-signal decay under each hypothesis ─────────────────────


def simulate_signal_decay(
    t_values: list[float],
    kappa0: float = 0.5,
    kappa_eq: float = 0.0,
    tau_rec_s: float = 1e4,
    rho0: float = 0.5,
    T_K: float = 600.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    lambda_p: float = 1.0,
) -> dict:
    """Clock-shift decay under the κ model vs a defect-driven model.

    The κ-driven shift decays with τ_rec; the defect-driven shift decays
    with τ_anneal(T). The two decay constants differ, which is the temporal
    signature separating the hypotheses.
    """
    kappa_series = [kappa_trajectory(t, kappa0, kappa_eq, tau_rec_s) for t in t_values]
    shift_kappa = [clock_shift(k, lambda_p) for k in kappa_series]

    tau_anneal = annealing_timescale(T_K, E_a_eV, tau0_s)
    defect_series = [defect_density(t, rho0, T_K, E_a_eV, tau0_s) for t in t_values]
    shift_defect = [lambda_p * d / (1.0 + lambda_p * d) for d in defect_series]

    return {
        "t_values": t_values,
        "kappa_series": kappa_series,
        "defect_series": defect_series,
        "shift_kappa": shift_kappa,
        "shift_defect": shift_defect,
        "tau_rec_s": tau_rec_s,
        "tau_anneal_s": tau_anneal,
        "interpretation": (
            f"κ-driven clock shift decays with τ_rec = {tau_rec_s:.1e} s; "
            f"defect-driven shift decays with τ_anneal = {tau_anneal:.1e} s at "
            f"{T_K:.0f} K. The decay constants differ by ×{tau_rec_s/tau_anneal:.1e} "
            f"— the temporal signature that separates the two hypotheses."
        ),
    }


# ── Quantitative F9 specification (τ_rec, annealing model, power) ───────────


def power_analysis(
    n_samples: int = 10,
    sigma_log_tau: float = 0.5,   # per-sample log-noise on the recovery time.
    arrhenius_log_ratio: float = 25.0,  # ln(τ_low/τ_high) from the Arrhenius law.
) -> dict:
    """Statistical power to reject "κ = defect density" from a T-sweep.

    Statistic: log(recovery_ratio) = log(τ_rec(T_low)/τ_rec(T_high)).
      κ (distinct):  log(ratio) = 0.
      defect (Arrhenius): log(ratio) = arrhenius_log_ratio (≫ 0).

    With n_samples per temperature and per-sample log-noise sigma_log_tau, the
    standard error on the mean ratio is sigma_log_tau/√n_samples; the SNR for
    distinguishing the two is arrhenius_log_ratio / SE.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be > 0")
    se = sigma_log_tau / math.sqrt(n_samples)
    snr = arrhenius_log_ratio / se if se > 0 else float("inf")
    return {
        "n_samples": n_samples,
        "sigma_log_tau": sigma_log_tau,
        "standard_error_log_ratio": se,
        "arrhenius_log_ratio": arrhenius_log_ratio,
        "snr": snr,
        "detectable_5sigma": snr >= 5.0,
        "interpretation": (
            f"With N={n_samples} samples per temperature and log-noise "
            f"σ_logτ={sigma_log_tau}, the standard error on the recovery-ratio is "
            f"{se:.3f} and the SNR against the Arrhenius prediction is {snr:.1f}. "
            f"The discriminator is {'resolvable at ≥5σ' if snr >= 5 else 'UNDERPOWERED'}."
        ),
    }


def f9_specification(
    n_samples: int = 10,
    sigma_log_tau: float = 0.5,
    E_a_eV_range: tuple[float, float] = (0.5, 2.0),
    tau0_s: float = 1e-13,
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
) -> dict:
    """The quantitative F9 discriminator specification.

    States the τ_rec range to test, the competing annealing model (Arrhenius
    with defect-type-specific activation energies), the temperature sweep, the
    sample count, and the resulting power.
    """
    # Arrhenius log-ratio over the sweep, at the LOWEST activation energy
    # (worst case: smallest separation to resolve).
    arrhenius_log_ratio_min = (
        E_a_eV_range[0] / (K_B_EV * (1.0 / T_low_K - 1.0 / T_high_K))
    ) if (1.0 / T_low_K - 1.0 / T_high_K) > 0 else 0.0
    arrhenius_log_ratio_min = abs(arrhenius_log_ratio_min)

    power = power_analysis(n_samples, sigma_log_tau, arrhenius_log_ratio_min)

    return {
        "tau_rec_range_to_test": "τ_rec ∈ [10², 10⁷] s — must NOT track the Arrhenius law",
        "competing_annealing_model": (
            f"τ_anneal(T) = τ_0·exp(E_a/k_B T), τ_0 ≈ {tau0_s:.0e} s, "
            f"E_a ∈ {E_a_eV_range} eV (defect-type-specific activation energies)"
        ),
        "temperature_sweep": f"T ∈ [{T_low_K:.0f}, {T_high_K:.0f}] K",
        "sample_count": f"N ≥ {n_samples} per temperature",
        "worst_case_arrhenius_log_ratio": arrhenius_log_ratio_min,
        "power": power,
        "decision": (
            "recovery ratio ≈ 1 (T-independent) ⇒ κ distinct from defect density; "
            "recovery ratio ≈ Arrhenius ⇒ κ = defect density ⇒ DET is a relabeling."
        ),
    }


def power_curve(
    n_samples_range: tuple[int, ...] = (1, 2, 5, 10, 20, 50, 100),
    sigma_log_tau: float = 0.5,
    arrhenius_log_ratio: float = 25.0,
    n_trials: int = 2000,
    seed: int = 42,
) -> dict:
    """Monte Carlo power curve: detection probability vs sample count.

    The discriminator statistic is log(recovery_ratio). Under κ (distinct),
    log(ratio) ~ N(0, σ_logτ²/N); under defect (Arrhenius), log(ratio) ~
    N(arrhenius_log_ratio, σ_logτ²/N). The decision boundary is the midpoint
    arrhenius_log_ratio/2.

    `power` = probability of correctly classifying "distinct" when κ IS
    distinct (sensitivity), i.e. P(|measured| < boundary | mean = 0).

    Returns the power at each sample count, so the minimum N for ≥95% power
    can be read off.
    """
    rng = random.Random(seed)
    boundary = arrhenius_log_ratio / 2.0
    results = []
    for n in n_samples_range:
        se = sigma_log_tau / math.sqrt(n)
        correct = 0
        for _ in range(n_trials):
            measured = rng.gauss(0.0, se)  # κ distinct → true mean 0.
            if abs(measured) < boundary:
                correct += 1
        power = correct / n_trials
        results.append(
            {
                "n_samples": n,
                "standard_error": se,
                "power": power,
                "achieved_95pct": power >= 0.95,
            }
        )

    # Minimum N for 95% power (from the analytic requirement |1.96·σ/√N| < boundary/2).
    min_n_95 = (
        math.ceil((1.96 * sigma_log_tau / (boundary / 2.0)) ** 2)
        if boundary > 0
        else float("inf")
    )

    return {
        "sigma_log_tau": sigma_log_tau,
        "arrhenius_log_ratio": arrhenius_log_ratio,
        "boundary": boundary,
        "results": results,
        "min_n_for_95pct": min_n_95,
        "interpretation": (
            f"Power rises from {results[0]['power']:.2f} at N=1 to "
            f"{results[-1]['power']:.2f} at N={n_samples_range[-1]}. "
            f"Analytic 95% power requires N ≥ {min_n_95}. Because the Arrhenius "
            f"separation ({arrhenius_log_ratio}) is huge, the discriminator is "
            f"decisive even with a handful of samples."
        ),
    }


def discriminator_reduction(
    T_high_K: float = 900.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
) -> dict:
    """The cleaner statement of the F9 discriminator (R7-C).

    At T_high = 900 K, defect annealing gives
        τ_anneal = τ_0·exp(E_a/k_B T) ≈ 10⁻¹³·exp(12.9) ≈ 40 ns
    — unobservably fast. So the ratio test REDUCES to a single question:

        "Can κ ≠ κ_eq be prepared and HELD at 900 K at all?"

    - Yes (κ survives at 900 K for a measurable time) → κ is NOT ordinary
      annealing (a distinct field).
    - No (κ vanishes in ~ns) → κ = defect density (relabeling).

    The difficulty is PHYSICAL preparation, not statistics (power ≈ 1 at N ≈ 1).
    """
    tau_anneal = annealing_timescale(T_high_K, E_a_eV, tau0_s)
    return {
        "T_high_K": T_high_K,
        "E_a_eV": E_a_eV,
        "tau_anneal_at_high_T_s": tau_anneal,
        "reduced_test": (
            f"At {T_high_K:.0f} K, defect annealing is τ_anneal ≈ "
            f"{tau_anneal:.2e} s — unobservably fast. The discriminator reduces to: "
            f"'can κ ≠ κ_eq be prepared and HELD at {T_high_K:.0f} K at all?' "
            f"Yes ⇒ κ distinct; No ⇒ κ = defect density."
        ),
        "caveat": (
            "The 'power ≈ 1 at N ≈ 1' result is statistically true, but the "
            "difficulty is PHYSICAL preparation (holding κ ≠ κ_eq at high T long "
            "enough to measure τ_rec), not statistics."
        ),
    }
