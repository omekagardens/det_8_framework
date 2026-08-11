"""
DET Track-B — Present Duration Paradox: Quantity of Fruit

The present moment has no duration in record-time. "How long does a
moment feel?" is unanswerable. But we can measure the QUANTITY OF FRUIT —
how much the record changes in a single commit event.

DET-native framing:
  The present is the act of participation that produces fruit (R changes).
  The "thickness" of the present = quantity of fruit produced per commit.
  κ constrains the possible fruit (Ω shrinks).
  Novelty = fruit that exceeds record-predicted expectation.

This connects to the Fruit-First Principle:
  "DET measures the fruit of becoming, not becoming itself."
  We cannot measure the present. We CAN measure its fruit.
  The quantity of fruit is our only window into the present's capacity.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════
# 1. Effect Size Measurement
# ═══════════════════════════════════════════════════════════════════════════


@dataclass
class PresentMoment:
    """A present moment characterized by the change it produces in the record."""

    prior_record: float       # R_n.
    committed_record: float   # R_{n+1}.
    possible_max: float       # Maximum possible change at this κ.
    possible_min: float       # Minimum possible change.

    @property
    def effect_size(self) -> float:
        """Absolute change: |R_{n+1} - R_n|."""
        return abs(self.committed_record - self.prior_record)

    @property
    def normalized_effect(self) -> float:
        """Effect as fraction of possible range.

        thickness = (actual change) / (max possible change).
        """
        span = self.possible_max - self.prior_record
        if abs(span) < 1e-10:
            return 0.0
        return self.effect_size / abs(span)

    @property
    def thickness_description(self) -> str:
        t = self.normalized_effect
        if t > 0.8:
            return "abundant fruit (near-maximum)"
        elif t > 0.5:
            return "substantial fruit"
        elif t > 0.2:
            return "sparse fruit"
        else:
            return "minimal fruit"


def simulate_present_thickness(
    n_moments: int = 50,
    kappa_start: float = 0.0,
    kappa_end: float = 5.0,
    seed: int = 42,
) -> dict:
    """Simulate present moments with varying κ.

    As κ increases, the possible change range shrinks (Ω constricts).
    The same "effort" of presence produces a smaller effect size
    because the possibility space is more constrained.

    This demonstrates that κ is a measure of how "thick" the present
    CAN be — not how thick it IS, but the ceiling on its capacity.
    """
    rng = random.Random(seed)
    record = 0.0
    history = []

    for i in range(n_moments):
        # κ increases linearly from kappa_start to kappa_end.
        kappa = kappa_start + (kappa_end - kappa_start) * i / (n_moments - 1)

        # Ω range shrinks with κ: possible change ∈ [−range, +range].
        omega_range = 1.0 / (1.0 + kappa)  # κ=0 → range=1, κ=5 → range≈0.17.

        # Present commits a random outcome within Ω.
        committed = record + rng.uniform(-omega_range, omega_range)

        # Max possible change from current record.
        possible_max = record + omega_range

        moment = PresentMoment(
            prior_record=record,
            committed_record=committed,
            possible_max=possible_max,
            possible_min=record - omega_range,
        )
        history.append({
            "moment": i,
            "kappa": kappa,
            "record_before": record,
            "record_after": committed,
            "effect_size": moment.effect_size,
            "normalized_effect": moment.normalized_effect,
            "omega_range": omega_range,
            "thickness": moment.thickness_description,
        })
        record = committed

    # Analyze: does κ correlate with effect size?
    kappas = [h["kappa"] for h in history]
    effects = [h["effect_size"] for h in history]
    ranges = [h["omega_range"] for h in history]

    # Correlation between κ and effect size (should be negative).
    n = len(history)
    mean_k = sum(kappas) / n
    mean_e = sum(effects) / n
    cov = sum((kappas[i] - mean_k) * (effects[i] - mean_e) for i in range(n)) / n
    std_k = math.sqrt(sum((k - mean_k)**2 for k in kappas) / n)
    std_e = math.sqrt(sum((e - mean_e)**2 for e in effects) / n)
    correlation = cov / (std_k * std_e) if std_k > 0 and std_e > 0 else 0.0

    mean_early_val = sum(h["effect_size"] for h in history[:10]) / 10
    mean_late_val = sum(h["effect_size"] for h in history[-10:]) / 10

    return {
        "n_moments": n_moments,
        "kappa_range": (kappa_start, kappa_end),
        "history": history,
        "kappa_effect_correlation": correlation,
        "early_effects": [h["effect_size"] for h in history[:5]],
        "late_effects": [h["effect_size"] for h in history[-5:]],
        "mean_early": mean_early_val,
        "mean_late": mean_late_val,
        "interpretation": (
            f"κ-effect correlation: {correlation:.2f}. "
            f"Mean fruit: {mean_early_val:.3f} (low κ) → {mean_late_val:.3f} (high κ). "
            f"As κ increases, the present's capacity to produce change "
            f"DECREASES. The present is 'thinner' when constrained by history. "
            f"This is observable: two systems with different κ will show "
            f"different typical commit magnitudes even with identical presence."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 2. Novelty Detection: Change Beyond Expectation
# ═══════════════════════════════════════════════════════════════════════════


def detect_novelty(
    n_moments: int = 50,
    novelty_at: list[int] = None,
    seed: int = 42,
) -> dict:
    """Detect novelty as change beyond record-predicted expectation.

    A "novel" present produces a commit that is larger than what the
    record history would predict. This is not proof of agency or
    creativity — but it IS an observable signature of a present that
    exceeded the constraints of its past.

    Novelty events are injected at specified moments by artificially
    increasing the commit magnitude beyond the Ω range.
    """
    if novelty_at is None:
        novelty_at = [20, 35]

    rng = random.Random(seed)
    record = 0.0
    kappa = 0.5
    history = []
    novelty_detected = []

    # Baseline statistics from first 10 moments.
    baseline_changes = []
    for i in range(10):
        omega_range = 1.0 / (1.0 + kappa)
        committed = record + rng.uniform(-omega_range, omega_range)
        baseline_changes.append(abs(committed - record))
        record = committed
        kappa += 0.02

    mean_baseline = sum(baseline_changes) / len(baseline_changes)
    std_baseline = (
        math.sqrt(sum((c - mean_baseline)**2 for c in baseline_changes) / (len(baseline_changes) - 1))
        if len(baseline_changes) > 1 else 0.01
    )

    for i in range(10, n_moments):
        omega_range = 1.0 / (1.0 + kappa)
        committed = record + rng.uniform(-omega_range, omega_range)

        # Inject novelty: artificial large change.
        if i in novelty_at:
            committed = record + rng.uniform(2 * omega_range, 4 * omega_range)
            if rng.random() > 0.5:
                committed = record + rng.uniform(2 * omega_range, 4 * omega_range)
            else:
                committed = record - rng.uniform(2 * omega_range, 4 * omega_range)

        change = abs(committed - record)
        sigma_deviation = (change - mean_baseline) / std_baseline

        moment_data = {
            "moment": i,
            "kappa": kappa,
            "change": change,
            "omega_range": omega_range,
            "sigma": sigma_deviation,
        }

        if sigma_deviation > 3.0:
            moment_data["novelty"] = "DETECTED (>3σ)"
            novelty_detected.append(i)
        elif sigma_deviation > 2.0:
            moment_data["novelty"] = "elevated (>2σ)"
        else:
            moment_data["novelty"] = "normal"

        history.append(moment_data)
        record = committed
        kappa += 0.02

    return {
        "baseline_mean": mean_baseline,
        "baseline_std": std_baseline,
        "novelty_injected_at": novelty_at,
        "novelty_detected_at": novelty_detected,
        "detection_rate": len(novelty_detected) / len(novelty_at) if novelty_at else 0.0,
        "history": history,
        "interpretation": (
            f"Novelty detection rate: {len(novelty_detected)}/{len(novelty_at)}. "
            "Changes beyond 3σ of baseline are flagged as potential novelty. "
            "This is NOT proof of agency or creativity — a stochastic process "
            "can also produce large deviations. It IS an observable signature "
            "that the present exceeded record-predicted expectations. "
            "Whether that excess is 'genuine novelty' or 'rare chance' is "
            "precisely the F8-OPEN question."
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# 3. Surprisal — Mathematical Trace of Faith
# ═══════════════════════════════════════════════════════════════════════════


def surprisal(outcome_probability: float) -> float:
    """Compute surprisal: S = -log K(X_e | R^-).

    High surprisal = outcome the past would not have predicted.
    Low surprisal = outcome the past fully expected.

    Faith is presence selecting the improbable from the lawful —
    not violating L, but choosing what the record-past would not
    have favored. Surprisal is the mathematical trace of that choice.
    """
    p = max(outcome_probability, 1e-15)
    return -math.log(p)


def simulate_surprisal_vs_kappa(n_moments: int = 50, seed: int = 42) -> dict:
    """Simulate surprisal as a function of kappa.

    At low kappa: Omega is large, kernel K spread over many options.
      Some outcomes have low probability -> high surprisal possible.
    At high kappa: Omega is small, kernel concentrated.
      All outcomes similar probability -> low surprisal ceiling.

    Faith (high surprisal) requires low kappa — structural freedom.
    """
    rng = random.Random(seed)
    history = []

    for i in range(n_moments):
        kappa = 0.0 + 5.0 * i / (n_moments - 1)
        n_options = max(2, int(10 * math.exp(-kappa * 0.5)))
        p_per_option = 1.0 / n_options
        chosen = rng.randint(0, n_options - 1)
        s = surprisal(p_per_option)
        history.append({
            "moment": i, "kappa": kappa,
            "n_options": n_options, "surprisal": s,
            "max_possible_surprisal": -math.log(1.0 / n_options),
            "faith_possible": s > 2.0,
        })

    return {
        "n_moments": n_moments, "history": history,
        "early_surprisal": [h["surprisal"] for h in history[:5]],
        "late_surprisal": [h["surprisal"] for h in history[-5:]],
        "interpretation": (
            f"Low kappa: {history[0]['n_options']} options, max surprisal {history[0]['max_possible_surprisal']:.1f}. "
            f"High kappa: {history[-1]['n_options']} options, max surprisal {history[-1]['max_possible_surprisal']:.1f}. "
            "kappa constrains not just fruit QUANTITY but fruit NOVELTY. "
            "A history-burdened present cannot produce surprising outcomes. "
            "Faith requires structural freedom."
        ),
    }
