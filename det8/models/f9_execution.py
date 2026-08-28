"""Execute the F9 τ_rec-vs-annealing discriminator (matched-generator dry run).

The F9 probe asks whether the κ recovery time τ_rec is temperature-independent
(a DET-native structural quantity) or tracks thermal annealing — i.e. whether
κ is anything more than ordinary defect density.

    defect density:  τ_anneal(T) = τ_0·exp(E_a / k_B T)   (strong T-dependence)
    κ (distinct):    τ_rec        = constant                (T-independent)

This module runs the full decision pipeline — generate a raw recovery record
R(t), fit τ_rec(T) from it, and apply the T-ratio discriminator — on
matched-generator data only.  There are no real raw recovery records in this
repository, so this is a *protocol dry run*, not a physics result.  The
Novelty Ledger entry for F9 therefore remains ``unexecuted`` against real
samples.

See `kappa_discriminator.py` for the discriminator specification and power
analysis, and `det8_core.py` / `kappa_diffusion.py` for the recovery law.
"""

from __future__ import annotations

import math
import random

from det8.models.kappa_discriminator import annealing_timescale


# ── Measurement: fit τ from a raw recovery record ──────────────────────────


def fit_recovery_time(
    t_values,
    signal_values,
    baseline: float = 0.0,
) -> float:
    """Fit τ from R(t) = baseline + A·exp(−t/τ) by log-linear regression.

    Uses only points above the baseline, then regresses log(R − baseline) on t
    (slope = −1/τ).  Returns the fitted decay constant in the same units as t.
    """

    xs = []
    ys = []
    for t, s in zip(t_values, signal_values):
        delta = s - baseline
        if delta <= 0.0:
            continue
        xs.append(t)
        ys.append(math.log(delta))
    if len(xs) < 2:
        return float("inf")
    n = len(xs)
    sx = sum(xs)
    sy = sum(ys)
    sxx = sum(x * x for x in xs)
    sxy = sum(x * y for x, y in zip(xs, ys))
    denom = n * sxx - sx * sx
    if abs(denom) < 1e-18:
        return float("inf")
    slope = (n * sxy - sx * sy) / denom
    if slope >= 0.0:
        return float("inf")
    return -1.0 / slope


def measure_recovery_time_at_T(
    hypothesis: str,
    T_K: float,
    *,
    tau_rec_s: float = 1e4,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    noise_sigma: float = 0.02,
    n_time_points: int = 15,
    seed: int = 0,
) -> float:
    """One simulated measurement of τ_rec at temperature T_K.

    Generates a raw normalized recovery record R(t) = exp(−t/τ_true) on a
    timescale matched to the true decay constant, adds Gaussian noise, and fits
    τ.  Returns the fitted τ (seconds).  ``hypothesis`` is ``"kappa_distinct"``
    or ``"defect"``.
    """

    if hypothesis == "kappa_distinct":
        tau_true = tau_rec_s
    elif hypothesis == "defect":
        tau_true = annealing_timescale(T_K, E_a_eV, tau0_s)
    else:
        raise ValueError("unknown hypothesis: %s" % (hypothesis,))

    rng = random.Random(seed)
    t_values = [
        2.0 * tau_true * (i + 1) / n_time_points for i in range(n_time_points)
    ]
    signal = [math.exp(-t / tau_true) for t in t_values]
    noisy = [s + rng.gauss(0.0, noise_sigma) for s in signal]
    return fit_recovery_time(t_values, noisy, baseline=0.0)


# ── The execution ──────────────────────────────────────────────────────────


def execute_f9_probe(
    *,
    T_low_K: float = 300.0,
    T_high_K: float = 900.0,
    E_a_eV: float = 1.0,
    tau0_s: float = 1e-13,
    tau_rec_s: float = 1e4,
    n_samples_per_T: int = 8,
    noise_sigma: float = 0.02,
    n_time_points: int = 15,
    decision_ratio_threshold: float = 2.0,
    seed: int = 20260827,
) -> dict:
    """Execute the F9 τ_rec-vs-annealing discriminator end-to-end.

    For each hypothesis and each temperature, measure τ_rec from simulated raw
    records, average in log space, and apply the T-ratio decision: ratio ≈ 1
    ⇒ T-independent (κ distinct); ratio ≫ 1 ⇒ Arrhenius (κ = defect density).
    """

    hypotheses = ("kappa_distinct", "defect")
    fitted = {}
    for hypothesis in hypotheses:
        for T_K in (T_low_K, T_high_K):
            samples = []
            for k in range(n_samples_per_T):
                tau = measure_recovery_time_at_T(
                    hypothesis,
                    T_K,
                    tau_rec_s=tau_rec_s,
                    E_a_eV=E_a_eV,
                    tau0_s=tau0_s,
                    noise_sigma=noise_sigma,
                    n_time_points=n_time_points,
                    seed=seed + k,
                )
                if math.isfinite(tau) and tau > 0.0:
                    samples.append(tau)
            log_mean = sum(math.log(s) for s in samples) / len(samples)
            fitted[(hypothesis, T_K)] = {
                "tau_mean_s": math.exp(log_mean),
                "n_measurements": len(samples),
            }

    verdicts = {}
    for hypothesis in hypotheses:
        tau_low = fitted[(hypothesis, T_low_K)]["tau_mean_s"]
        tau_high = fitted[(hypothesis, T_high_K)]["tau_mean_s"]
        ratio = tau_low / tau_high
        decision = (
            "T-INDEPENDENT (κ distinct from defect density)"
            if ratio < decision_ratio_threshold
            else "ARRHENIUS (κ = defect density; no novelty)"
        )
        verdicts[hypothesis] = {
            "tau_low_s": tau_low,
            "tau_high_s": tau_high,
            "T_ratio": ratio,
            "decision": decision,
            "ground_truth": (
                "T-INDEPENDENT" if hypothesis == "kappa_distinct" else "ARRHENIUS"
            ),
            "correct": (ratio < decision_ratio_threshold)
            == (hypothesis == "kappa_distinct"),
        }

    discriminator_works = all(v["correct"] for v in verdicts.values())
    return {
        "probe": "F9 τ_rec-vs-annealing discriminator",
        "execution": "matched-generator dry run (protocol validation)",
        "temperature_sweep_K": [T_low_K, T_high_K],
        "decision_ratio_threshold": decision_ratio_threshold,
        "verdicts": verdicts,
        "discriminator_works": discriminator_works,
        "physics_outcome": (
            "NOT DETERMINED — no real raw R(t) recovery records in this repository"
        ),
        "ledger_status": "remains unexecuted against real samples",
        "practical_reduction": (
            f"At {T_high_K:.0f} K, defect annealing is τ_anneal ≈ "
            f"{annealing_timescale(T_high_K, E_a_eV, tau0_s):.2e} s — so the "
            f"ratio test reduces to: can κ ≠ κ_eq be prepared and HELD at "
            f"{T_high_K:.0f} K at all?  Yes ⇒ κ distinct; No ⇒ κ = defect density."
        ),
        "next_physical_step": (
            f"measure recovery rate τ_rec(T) on a real sample across a "
            f"[{T_low_K:.0f}, {T_high_K:.0f}] K sweep; the discriminator is cheap "
            f"in practice (power ≈ 1 at N ≈ 1)."
        ),
    }
