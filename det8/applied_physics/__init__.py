"""
DET v8.0 — Applied Physics Program

A suite of applied, adversarial tests that turn operational κ into a
precision-materials engineering tool, using publicly-available real-world
datasets (GNSS clock logs, qubit calibration logs, cavity drift, space
telemetry, gauge-block archives).

Methodology (three steps):
  1. ADVERSARIAL BASELINE — implement the industry-standard model for each
     domain (IEEE clock aging, KWW creep, Arrhenius recovery, DDD radiation
     damage). DET claims a "win" only if the κ-model yields a LOWER Bayesian
     Information Criterion (BIC) than the standard model.
  2. κ-PROXY INGEST — map external variables to DET inputs:
       T(t)  → τ_rec(T)      (temperature modulates recovery)
       Φ(t)  → κ̇_damage       (radiation drives damage)
       Δf/f or ΔL/L → κ(t)   (the observable proxy)
  3. DISCRIMINATOR — look for the DET signature: a relaxation that tracks the
     free-energy gradient ∂ψ/∂κ (single exponential) rather than a fixed
     Arrhenius spectrum (stretched exponential).

The real datasets are external; the modules below generate SYNTHETIC data
mimicking their structure, so the full machinery — generate → fit standard →
fit DET → compare BIC → discriminate — is runnable and testable now, and the
ingest stubs are ready for the real datasets when supplied.

Layer mapping (operational_kappa):
  L0 (engineering descriptor)  — κ as a compact drift model.
  L1 (independent residual)    — the discriminator: does κ beat the standard model?
  L2 (clock anomaly via λ_P)   — NOT claimed here; λ_P is a separate, riskier test.
"""
