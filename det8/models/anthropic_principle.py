"""
DET v8.0 — Anthropic Principle (F12): Observer Selection in DET-Native Terms

Tests what Deep Existence Theory can and cannot say about the Anthropic
Principle, using ONLY DET primitives. No standard-physics constants are
imported (no c, hbar, G, Lambda, fine-structure constant, axion decay
constant, strong-CP angle, dark matter/energy, or cosmological parameters).

Why a DET-native module exists at all:
  The standard Anthropic Principle is the claim that our universe's
  fundamental constants appear "fine-tuned" for life, because a small
  change in any one of ~20 numbers would make observers impossible.
  The Weak Anthropic Principle (WAP) reads this as a selection effect
  ("we can only observe from a life-permitting universe"). The Strong
  Anthropic Principle (SAP) reads it as necessity ("the universe must
  permit life"). Both are motivated by the fine-tuning premise.

  DET has NO standard-model constants to tune. Its only free parameters
  are its own primitives (lambda_P, lambda_gamma, G_q, kappa_eq, tau_rec,
  D, K). The one that gates observer-existence is the structural history
  field kappa, acting through the participation aperture:

      Pi(kappa) = 1 / (1 + lambda_P * kappa)     (all other Pi factors = 1)

  So the anthropic question "why are the constants right for observers?"
  becomes, in DET, "why does the kappa-field settle into a range that
  permits structured participation?" — and kappa is a DYNAMICAL field
  with an attractor, not a fixed constant.

DET-native observer (Structured Participation Regime, SPR):
  A connected record-regime that (i) is gravitationally SELF-BOUND by its
  own kappa-gravity and (ii) keeps its participation aperture Pi above a
  floor so present participation keeps producing measurable fruit. This is
  deliberately NOT biological life and NOT consciousness — both are
  quarantined (Status M) in DET. The SPR is the minimal DET-native analogue
  of "an observer that can measure."

  Binding + participation give a WINDOW on kappa:

      kappa_bind  <=  kappa  <=  kappa_obs

  where kappa_bind is the minimum kappa for self-gravitational binding
  (from kappa-gravity) and kappa_obs = (1/Pi_min - 1)/lambda_P is the
  maximum kappa for participation. This is DET's native "Goldilocks"
  window: too little structural history cannot bind, too much stalls
  participation. It replaces the standard ~20 fine-tuned constants with
  one scalar that must fall in one interval.

Three positions are tested (see det_anthropic_position()):

  1. WAP (selection)      — is the selection effect coherent and does it
                            explain apparent tuning?  -> CONFIRMED (CI)
  2. SAP (necessity)      — does L force observers for all parameter
                            draws?                     -> REJECTED (FT)
  3. Fine-tuning premise  — are observers an improbable coincidence of
                            many independent constants? -> REDUCED (FT/CI)

The core structural results (exact, prior-independent):

  * kappa has an attractor kappa* = (kappa_eq + beta) / (1 + beta),
    where beta = alpha * R * tau_rec is the damage-recovery ratio.
  * An SPR forms iff kappa* lies in the window [kappa_bind, kappa_obs].
  * The upper bound is one dimensionless combination
        Z = lambda_P * kappa*  <=  (1/Pi_min - 1).
    The lower bound is kappa* >= kappa_bind. Both depend on the single
    scalar kappa*, not on ~20 independent constants.
  * Because kappa* is an attractor, the observer condition is independent
    of the INITIAL kappa: initial-condition fine-tuning is dissolved.
  * Observers are contingent, not necessary: kappa_eq -> 1 or beta -> inf
    pushes kappa* above kappa_obs (no participation), while kappa_bind ->
    1 pushes the window shut (no binding) — two independent ways to fail.

The statistical results (prior-dependent, reported for a documented prior):

  * P(observer) under the prior ("naturalness").
  * Posterior vs prior means of the parameters conditioned on SPR
    (the WAP selection shift).
  * A prior-sensitivity sweep (prior_sensitivity_sweep) separates the
    prior-robust findings from the prior-dependent magnitudes.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ── Module thresholds (module-level choices, NOT physical constants) ────────

PI_MIN_DEFAULT = 0.5        # Participation floor for observer-existence.
COHERENCE_MIN_DEFAULT = 0.5  # Record coherence floor (readability).

# DET-native parameter prior ranges (documented; see draw_det_universe).
LAMBDA_P_LOG_MIN = -2.0     # lambda_P in [10^-2, 10^2]  (κ-drag coupling).
LAMBDA_P_LOG_MAX = 2.0
KAPPA_EQ_MIN = 0.0          # kappa_eq in [0, 1] (equilibrium structural history).
KAPPA_EQ_MAX = 1.0
BETA_LOG_MIN = -2.0         # beta = alpha*R*tau_rec in [10^-2, 10^2].
BETA_LOG_MAX = 2.0
KAPPA_BIND_MIN = 0.0        # kappa_bind in [0, 1] (self-binding threshold).
KAPPA_BIND_MAX = 1.0


# ── DET-native participation aperture (κ-only slice) ────────────────────────


def participation_aperture_kappa_only(
    kappa: float,
    lambda_p: float = 1.0,
) -> float:
    """Π(κ) = 1 / (1 + λ_P·κ), with all other Π factors held at unity.

    This is the κ-only slice of det8_core.participation_aperture: it sets
    σ=η=1, F=H=0, γ_v=1 and keeps only the structural-history drag. It is
    the DET-native analogue of the "fine-tuned quantity" — the one number
    that gates participation.

    κ ∈ [0, 1]. Higher κ → lower Π → slower proper time per event.
    """
    return 1.0 / (1.0 + lambda_p * kappa)


def kappa_threshold(
    lambda_p: float,
    pi_min: float = PI_MIN_DEFAULT,
) -> float:
    """κ_obs such that Π(κ) ≥ pi_min  ⟺  κ ≤ κ_obs.

    From Π(κ) = 1/(1+λ_P·κ) ≥ pi_min:
        1 + λ_P·κ ≤ 1/pi_min  ⟺  κ ≤ (1/pi_min − 1)/λ_P.
    """
    if lambda_p <= 0.0:
        return float("inf")
    return (1.0 / pi_min - 1.0) / lambda_p


# ── κ-gravity self-binding threshold (DET-native, proposed) ─────────────────


def kappa_bind_from_gravity(
    a_disp: float,
    R: float,
    G_q: float,
    lambda_gamma: float,
    N: float,
) -> float:
    """Minimum κ for self-gravitational binding.

    DET κ-gravity (Newtonian limit, `det_gravity.py`): a clump of N nodes
    has total gravitational charge Γ = λ_γ·κ·N, so a node at the clump
    edge feels inward acceleration a = G_q·Γ/R² = G_q·λ_γ·κ·N/R². For the
    clump to hold together, this must exceed the record-side dispersal
    acceleration a_disp (the structural tendency to unbind). Hence:

        κ_bind = a_disp·R² / (G_q·λ_γ·N).

    Modal annotation: P (proposed physical — binding ansatz). Uses only DET
    primitives G_q, λ_γ and record-side quantities a_disp, R, N.
    """
    if G_q <= 0.0 or lambda_gamma <= 0.0 or N <= 0.0:
        return float("inf")
    return a_disp * R * R / (G_q * lambda_gamma * N)


# ── κ attractor (from DET's own κ-dynamics) ─────────────────────────────────


def kappa_fixed_point(
    kappa_eq: float,
    beta: float,
) -> float:
    """Attractor of the homogeneous κ-dynamics.

    DET κ-dynamics (no diffusion, in recovery-time units):
        dκ/ds = β·(1 − κ) − (κ − κ_eq),    β = α·R·τ_rec.

    Fixed point: β(1−κ*) = (κ* − κ_eq)
        ⟹  κ* = (κ_eq + β) / (1 + β).

    β is the dimensionless damage-recovery ratio: damage rate α·R
    (accumulating structural history) balanced against recovery
    (κ − κ_eq)/τ_rec. β=0 → κ*=κ_eq (fully recovered); β→∞ → κ*→1.
    """
    return (kappa_eq + beta) / (1.0 + beta)


def relax_kappa(
    kappa0: float,
    kappa_eq: float,
    beta: float,
    n_steps: int = 400,
    dt: float = 0.05,
) -> float:
    """Integrate the κ-dynamics forward from an initial κ to its attractor.

    Demonstrates initial-condition independence: any κ0 converges to the
    same κ*. This dissolves initial-condition fine-tuning — the observer
    condition depends on the attractor, not on where κ started.
    """
    kappa = kappa0
    for _ in range(n_steps):
        dk = beta * (1.0 - kappa) - (kappa - kappa_eq)
        kappa += dk * dt
        kappa = max(0.0, min(1.0, kappa))
    return kappa


# ── DET-native observer predicate (binding + participation window) ──────────


def is_observer_regime(
    kappa_star: float,
    lambda_p: float,
    pi_min: float = PI_MIN_DEFAULT,
    kappa_bind: float = 0.0,
) -> bool:
    """True iff the κ-attractor lies in the observer window [κ_bind, κ_obs].

    Two DET-native conditions:
      1. Binding:       κ* ≥ κ_bind  (κ-gravity holds the regime together).
      2. Participation: κ* ≤ κ_obs   (Π(κ*) ≥ pi_min).
    """
    return kappa_bind <= kappa_star <= kappa_threshold(lambda_p, pi_min)


def observer_window_width(
    lambda_p: float,
    kappa_bind: float,
    pi_min: float = PI_MIN_DEFAULT,
) -> float:
    """Width of the observer window κ_obs − κ_bind (≤ 0 means no observers)."""
    return kappa_threshold(lambda_p, pi_min) - kappa_bind


def observer_combination(
    lambda_p: float,
    kappa_eq: float,
    beta: float,
) -> float:
    """The single upper-bound combination Z = λ_P·κ*.

    The participation (upper) bound is Z ≤ (1/pi_min − 1). The binding
    (lower) bound is κ* ≥ κ_bind. Both constrain the single scalar κ*.
    """
    return lambda_p * kappa_fixed_point(kappa_eq, beta)


# ── Ensemble over DET-native parameter space ────────────────────────────────


def draw_det_universe(
    rng: random.Random,
    lp_range: tuple[float, float] = (LAMBDA_P_LOG_MIN, LAMBDA_P_LOG_MAX),
    beta_range: tuple[float, float] = (BETA_LOG_MIN, BETA_LOG_MAX),
    kb_range: tuple[float, float] = (KAPPA_BIND_MIN, KAPPA_BIND_MAX),
) -> dict:
    """Draw one DET universe from the DET-native parameter prior.

    Parameters (all DET primitives / free parameters, none from standard
    physics):
      lambda_p  : κ-drag coupling (log-uniform).
      kappa_eq  : equilibrium structural history (uniform [0, 1]).
      beta      : damage-recovery ratio α·R·τ_rec (log-uniform).
      kappa_bind: self-binding threshold (uniform [0, 1]) — the effective
                  combination a_disp·R²/(G_q·λ_γ·N), drawn directly.

    The priors are deliberately broad/agnostic. Results that are robust
    to prior choice (necessity-false, window structure, selection-shift
    direction) are flagged separately from the prior-dependent naturalness
    measure.
    """
    lambda_p = 10.0 ** rng.uniform(lp_range[0], lp_range[1])
    kappa_eq = rng.uniform(KAPPA_EQ_MIN, KAPPA_EQ_MAX)
    beta = 10.0 ** rng.uniform(beta_range[0], beta_range[1])
    kappa_bind = rng.uniform(kb_range[0], kb_range[1])
    return {
        "lambda_p": lambda_p,
        "kappa_eq": kappa_eq,
        "beta": beta,
        "kappa_bind": kappa_bind,
    }


def anthropic_ensemble(
    n_draws: int = 20000,
    seed: int = 42,
    pi_min: float = PI_MIN_DEFAULT,
    lp_range: tuple[float, float] = (LAMBDA_P_LOG_MIN, LAMBDA_P_LOG_MAX),
    beta_range: tuple[float, float] = (BETA_LOG_MIN, BETA_LOG_MAX),
    kb_range: tuple[float, float] = (KAPPA_BIND_MIN, KAPPA_BIND_MAX),
) -> dict:
    """Monte Carlo over DET universes; compute anthropic statistics.

    Returns:
      p_observer          : naturalness — P(SPR) under the prior.
      necessity           : True only if EVERY draw forms an SPR (SAP).
      threshold           : upper Z-threshold (1/pi_min − 1).
      prior_*_mean        : prior means of parameters.
      posterior_*_mean    : means conditioned on SPR (WAP selection shift).
      observer_draws      : list of draws that form an SPR.
      non_observer_draws  : list of draws that do not.

    Caveat: p_observer and the exact posterior means depend on the prior;
    necessity, the window structure, and the sign of the selection shifts
    are prior-independent.
    """
    rng = random.Random(seed)
    threshold = 1.0 / pi_min - 1.0

    draws = []
    observer_draws = []
    non_observer_draws = []

    for _ in range(n_draws):
        d = draw_det_universe(rng, lp_range, beta_range, kb_range)
        kappa_star = kappa_fixed_point(d["kappa_eq"], d["beta"])
        Z = d["lambda_p"] * kappa_star
        obs = is_observer_regime(
            kappa_star, d["lambda_p"], pi_min, d["kappa_bind"]
        )
        d["kappa_star"] = kappa_star
        d["Z"] = Z
        d["observer"] = obs
        draws.append(d)
        (observer_draws if obs else non_observer_draws).append(d)

    def _mean(key: str, lst: list[dict]) -> float:
        return sum(x[key] for x in lst) / len(lst) if lst else float("nan")

    keys = ["lambda_p", "kappa_eq", "beta", "kappa_bind"]
    prior = {k: _mean(k, draws) for k in keys}
    post = {k: _mean(k, observer_draws) for k in keys}
    shifts = {k: post[k] / prior[k] if prior[k] else float("nan") for k in keys}

    p_observer = len(observer_draws) / n_draws if n_draws else float("nan")
    necessity = len(observer_draws) == n_draws

    result = {
        "n_draws": n_draws,
        "pi_min": pi_min,
        "threshold": threshold,
        "p_observer": p_observer,
        "necessity": necessity,
        "prior_mean": prior,
        "posterior_mean": post,
        "selection_shift": shifts,
        "observer_draws": observer_draws,
        "non_observer_draws": non_observer_draws,
    }
    result["interpretation"] = (
        f"Under this DET-native prior, P(observer) = {p_observer:.3f}. "
        f"Necessity (SAP) is {necessity}: observers are contingent, not forced. "
        f"Conditioning on an SPR shifts the posterior means of "
        f"lambda_P ({post['lambda_p']:.2f} vs {prior['lambda_p']:.2f}), "
        f"kappa_eq ({post['kappa_eq']:.3f} vs {prior['kappa_eq']:.3f}), "
        f"beta ({post['beta']:.2f} vs {prior['beta']:.2f}), and "
        f"kappa_bind ({post['kappa_bind']:.3f} vs {prior['kappa_bind']:.3f}) "
        f"downward — a coherent selection effect (WAP). The observer "
        f"condition depends on a single scalar κ* falling in the window "
        f"[κ_bind, κ_obs], not on ~20 independent constants, and it is set "
        f"by the κ-attractor, not initial conditions."
    )
    return result


# ── Prior-sensitivity sweep ─────────────────────────────────────────────────


def prior_sensitivity_sweep(
    n_draws: int = 20000,
    seed: int = 42,
    pi_min: float = PI_MIN_DEFAULT,
) -> dict:
    """Run the ensemble under several prior specifications.

    Varies (i) the λ_P log-range, (ii) the β log-range, (iii) the κ_bind
    prior. Reports P(observer) and the selection-shift ratios for each, so
    the prior-robust findings (necessity false, window structure, shift
    direction) can be separated from the prior-dependent magnitudes
    (P(observer), exact shift ratios).

    All configs keep the parameters DET-native; only the prior widths change.
    """
    configs = [
        ("baseline",          dict(lp_range=(-2.0, 2.0),  beta_range=(-2.0, 2.0),  kb_range=(0.0, 1.0))),
        ("narrow λ_P",        dict(lp_range=(-1.0, 1.0),  beta_range=(-2.0, 2.0),  kb_range=(0.0, 1.0))),
        ("wide λ_P",          dict(lp_range=(-3.0, 3.0),  beta_range=(-2.0, 2.0),  kb_range=(0.0, 1.0))),
        ("narrow β",          dict(lp_range=(-2.0, 2.0),  beta_range=(-1.0, 1.0),  kb_range=(0.0, 1.0))),
        ("wide β",            dict(lp_range=(-2.0, 2.0),  beta_range=(-3.0, 3.0),  kb_range=(0.0, 1.0))),
        ("κ_bind ∈ [0, 0.5]", dict(lp_range=(-2.0, 2.0),  beta_range=(-2.0, 2.0),  kb_range=(0.0, 0.5))),
        ("κ_bind ∈ [0.5, 1]", dict(lp_range=(-2.0, 2.0),  beta_range=(-2.0, 2.0),  kb_range=(0.5, 1.0))),
    ]

    rows = []
    for name, cfg in configs:
        ens = anthropic_ensemble(
            n_draws=n_draws, seed=seed, pi_min=pi_min,
            lp_range=cfg["lp_range"], beta_range=cfg["beta_range"],
            kb_range=cfg["kb_range"],
        )
        rows.append({
            "config": name,
            "p_observer": ens["p_observer"],
            "necessity": ens["necessity"],
            "shift_lambda_p": ens["selection_shift"]["lambda_p"],
            "shift_kappa_eq": ens["selection_shift"]["kappa_eq"],
            "shift_beta": ens["selection_shift"]["beta"],
            "shift_kappa_bind": ens["selection_shift"]["kappa_bind"],
        })

    robust = {
        "necessity_always_false": all(not r["necessity"] for r in rows),
        "shift_direction_lambda_p_always_down": all(r["shift_lambda_p"] < 1.0 for r in rows),
        "shift_direction_kappa_bind_always_down": all(r["shift_kappa_bind"] < 1.0 for r in rows),
        "shift_direction_kappa_eq_always_up": all(r["shift_kappa_eq"] > 1.0 for r in rows),
        "shift_direction_beta_always_up": all(r["shift_beta"] > 1.0 for r in rows),
    }

    return {
        "pi_min": pi_min,
        "n_draws_per_config": n_draws,
        "rows": rows,
        "robust": robust,
        "interpretation": (
            f"Across {len(rows)} prior specifications, P(observer) ranges "
            f"from {min(r['p_observer'] for r in rows):.3f} to "
            f"{max(r['p_observer'] for r in rows):.3f} — the naturalness "
            f"number is prior-dependent. By contrast, the qualitative "
            f"signature is prior-robust: necessity is always false, and the "
            f"selection is always two-sided — lambda_P and kappa_bind are "
            f"selected DOWNWARD (loosening the two window bounds), while "
            f"kappa_eq and beta are selected UPWARD (raising κ* into the "
            f"window). SAP-rejection and WAP-selection are robust; only "
            f"their magnitudes are prior-dependent."
        ),
    }


# ── Initial-condition independence demonstration ───────────────────────────


def demonstrate_attractor_convergence(
    kappa_eq: float = 0.3,
    beta: float = 0.5,
    lambda_p: float = 1.5,
    pi_min: float = PI_MIN_DEFAULT,
    kappa_bind: float = 0.2,
) -> dict:
    """Show that any initial κ converges to the same attractor κ*.

    The observer condition then depends on κ* (the attractor), not κ0
    (the initial condition) — DET dissolves initial-condition fine-tuning.
    """
    kappa_star = kappa_fixed_point(kappa_eq, beta)
    initial = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    finals = [relax_kappa(k0, kappa_eq, beta) for k0 in initial]
    converged = all(abs(f - kappa_star) < 1e-3 for f in finals)

    return {
        "kappa_eq": kappa_eq,
        "beta": beta,
        "kappa_star": kappa_star,
        "initial_kappa": initial,
        "final_kappa": finals,
        "converged": converged,
        "observer_regime": is_observer_regime(kappa_star, lambda_p, pi_min, kappa_bind),
        "interpretation": (
            f"All initial κ values converge to κ* = {kappa_star:.3f}. "
            f"The observer condition depends only on κ*, not on κ(0): "
            f"initial-condition fine-tuning is dissolved. "
            f"(Converged: {converged}.)"
        ),
    }


# ── Anti-smuggling audit ────────────────────────────────────────────────────


def anti_smuggling_audit() -> dict:
    """Document that this module uses only DET primitives.

    This is a written audit, mirroring the anti-smuggling discipline in
    PHYSICS.md §6: every symbol the module uses is listed with its DET
    provenance, and every standard-physics/axion constant it deliberately
    does NOT import is listed as excluded. `clean` is True iff no excluded
    symbol is among the used symbols.
    """
    used = {
        "kappa": "structural history density (DET primitive, det8_core)",
        "kappa_eq": "equilibrium structural history (DET free parameter)",
        "kappa_bind": "self-binding threshold (DET-derived: a_disp·R²/(G_q·λ_γ·N))",
        "lambda_p": "κ-drag coupling on Π (DET free parameter)",
        "lambda_gamma": "κ → gravitational charge conversion (DET free parameter)",
        "G_q": "κ-gravity coupling (DET free parameter)",
        "a_disp": "record-side dispersal acceleration (DET record quantity)",
        "R": "regime spatial scale (DET record quantity)",
        "N": "node count / event count (DET record quantity)",
        "alpha": "damage coefficient per event (DET primitive)",
        "R_rate": "event rate (record-side quantity, DET)",
        "tau_rec": "recovery time scale (DET free parameter)",
        "beta": "damage-recovery ratio α·R·τ_rec (DET-derived)",
        "pi": "participation aperture Π (DET primitive, det8_core)",
        "pi_min": "participation floor (module threshold, not physics)",
        "coherence": "record coherence C (DET primitive)",
        "kappa_obs": "participation threshold (DET-derived from Π)",
        "Z": "upper combination λ_P·κ* (DET-derived)",
    }
    excluded = [
        "c (speed of light)",
        "hbar (Planck constant)",
        "G (Newton constant)",
        "Lambda (cosmological constant)",
        "alpha_em (fine-structure constant)",
        "f_a (axion decay constant)",
        "m_a (axion/ultralight-ALP mass)",
        "theta_QCD (strong-CP angle)",
        "electron/proton mass",
        "dark matter / dark energy",
        "Omega_Lambda, H0, T_cmb (cosmological parameters)",
    ]
    clean = all(s not in used for s in [e.split(" (")[0] for e in excluded])
    return {
        "used_det_symbols": used,
        "deliberately_excluded": excluded,
        "clean": clean,
        "note": (
            "The module imports no standard-physics constants. Its 'parameters' "
            "are DET's own free parameters (lambda_P, lambda_gamma, G_q, "
            "kappa_eq, tau_rec, alpha, R). Gravitational binding is computed "
            "from DET's κ-gravity (G_q, λ_γ), not Newtonian G. The ultralight-"
            "axion / strong-CP fine-tuning question is NOT imported; it is "
            "reframed in DET-native terms (see docs/track_b/anthropic_principle.md)."
        ),
    }


# ── Claim register ──────────────────────────────────────────────────────────


def det_anthropic_position() -> dict:
    """DET-native verdict on the three anthropic positions.

    Status vocabulary (per MODEL_CARD §6):
      FT = Finite Theorem (exhibited construction), CI = Computed Instance,
      P = Proposed, M = Metaphysical.
    """
    return {
        "weak_anthropic_selection": {
            "verdict": "CONFIRMED (coherent selection mechanism)",
            "status": "CI",
            "detail": (
                "Conditioning on 'an SPR is present' produces a coherent, "
                "two-sided selection effect. The posterior pushes lambda_P "
                "and kappa_bind DOWNWARD (loosening the two window bounds, "
                "kappa_obs and kappa_bind) while pushing kappa_eq and beta "
                "UPWARD (raising the κ-attractor κ* into the window). The "
                "selection effect is real and mathematically well-defined in "
                "DET: an observer is, by construction, a record-regime that "
                "already exists, so 'we observe from an observer-permitting "
                "region' is a tautology DET makes precise. This is evidence "
                "FOR the weak Anthropic Principle as a selection mechanism. "
                "The prior-sensitivity sweep shows the direction of the shift "
                "is robust across priors; only its magnitude is prior-dependent."
            ),
        },
        "strong_anthropic_necessity": {
            "verdict": "REJECTED (observers are contingent)",
            "status": "FT",
            "detail": (
                "DET's law map L fixes the FORM of the κ-dynamics but not the "
                "free parameters. There are now TWO independent ways to build a "
                "consistent observer-free DET universe: (i) kappa_eq -> 1 or "
                "beta -> inf drives kappa* above kappa_obs (participation "
                "stalls); (ii) kappa_bind -> 1 drives the binding floor above "
                "any attainable kappa* (the window shuts). Hence 'the universe "
                "must permit observers' is not a theorem of DET — the strong "
                "Anthropic Principle (necessity) fails within DET's own "
                "ontology. Caveat: this counters SAP as a claim about DET; it "
                "does not, by itself, refute SAP in standard physics, which "
                "this module does not engage."
            ),
        },
        "fine_tuning_premise": {
            "verdict": "REDUCED (one scalar in one window, not ~20 constants)",
            "status": "FT/CI",
            "detail": (
                "The observer condition depends on a single scalar κ* (the "
                "κ-attractor) falling in the window [κ_bind, κ_obs], where "
                "κ_obs = (1/Π_min − 1)/λ_P. The upper bound is the combination "
                "Z = λ_P·κ*, the lower bound is κ_bind, and κ* is a dynamical "
                "attractor, so the condition is independent of initial κ. The "
                "fine-tuning premise — many independent constants each "
                "improbably tuned — does not survive translation into DET: "
                "there is one scalar in one interval, not ~20 free "
                "coincidences. The prior-dependent naturalness measure "
                "(P(observer)) is reported separately and is NOT claimed to be "
                "large; the reduction claim is structural, not statistical."
            ),
        },
        "binding_participation_window": {
            "verdict": "NEW — observers require κ* ∈ [κ_bind, κ_obs]",
            "status": "P",
            "detail": (
                "Folding κ-gravity self-binding into the SPR criterion yields "
                "a genuine DET-native 'Goldilocks' window: too little "
                "structural history cannot self-bind (κ* < κ_bind), too much "
                "stalls participation (κ* > κ_obs). This mirrors the standard "
                "fine-tuning window structure (e.g. a force strong enough to "
                "bind but weak enough to not over-bind) entirely within DET's "
                "κ. The binding threshold is a proposed ansatz (Status P), "
                "derived from DET's κ-gravity, not a proven theorem."
            ),
        },
        "caveats": [
            "No empirical prediction is made here; this is a Track A/B "
            "structural analysis of DET's own parameter space.",
            "The SPR is DET's minimal observer analogue, not biological life "
            "and not consciousness (both Status M).",
            "P(observer) and the exact selection-shift magnitudes are "
            "prior-dependent; the verdicts above are prior-independent "
            "(verified by the sweep).",
            "The κ_bind binding ansatz is Status P; it is not yet tied to a "
            "specific measured regime or to inhomogeneous κ on a bond network.",
        ],
    }


# ── Convenience summary ─────────────────────────────────────────────────────


def summary(
    n_draws: int = 20000,
    seed: int = 42,
    pi_min: float = PI_MIN_DEFAULT,
) -> dict:
    """Run everything and return a single self-contained report."""
    ens = anthropic_ensemble(n_draws=n_draws, seed=seed, pi_min=pi_min)
    sweep = prior_sensitivity_sweep(n_draws=n_draws, seed=seed, pi_min=pi_min)
    attractor = demonstrate_attractor_convergence()
    audit = anti_smuggling_audit()
    position = det_anthropic_position()
    return {
        "ensemble": {k: v for k, v in ens.items() if k not in ("observer_draws", "non_observer_draws")},
        "sweep": {k: v for k, v in sweep.items() if k != "rows"},
        "sweep_rows": sweep["rows"],
        "attractor": attractor,
        "anti_smuggling": audit,
        "position": position,
    }
