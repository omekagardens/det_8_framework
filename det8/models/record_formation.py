"""
DET v8.1 — Record Stabilization Bound (historical T3 name retained)

Repeated weak commit events independently encode a target alternative with
reliability p > 1/2. A concentration bound forces the probability of a wrong
majority record to decay exponentially in the number N of redundant events:

    P_record_error(N) ≤ e^{−N·C(p)},   C(p) = D(1/2 ‖ p) = −ln(2√(p(1−p))).

This establishes conditional reliability of redundant classical copies. The
target alternative, independent copying events and their reliability are
assumed. It does not select the first outcome, derive record-production rates,
or prove decay of off-diagonal pair-kernel entries or physical irreversibility.

DERIVATION CERTIFICATE (honest provenance):

  Chernoff / relative-entropy bound   MATH   — standard concentration inequality
                                              (credited; not DET-specific).
  P_error(N) ≤ e^{−NC}                TH-DET — the theorem statement, applied to
                                              the commit channel with reliability p.
  redundancy → pointer stability     MODEL  — reliability under the stated
                                              independent-copying assumptions.

No standard-physics constants are used; the probability model is supplied.
"""

from __future__ import annotations

import math
import random


# ── Majority-vote error exponent ────────────────────────────────────────────


def chernoff_exponent(p: float) -> float:
    """C(p) = D(1/2 ‖ p) = −ln(2√(p(1−p))), the majority-vote error exponent.

    Positive for p > 1/2; zero at p = 1/2; → ∞ as p → 1.
    """
    if not (0.5 < p < 1.0):
        raise ValueError("reliability p must be in (0.5, 1)")
    return -math.log(2.0 * math.sqrt(p * (1.0 - p)))


def record_error_bound(N: int, p: float) -> float:
    """Upper bound on P(majority record is wrong) for N weak commits of reliability p.

    P_error(N) ≤ exp(−N·C(p)).
    """
    if N <= 0:
        raise ValueError("N must be positive")
    return math.exp(-N * chernoff_exponent(p))


def majority_vote_error(N: int, p: float, n_trials: int = 20000, seed: int = 42) -> float:
    """Monte Carlo estimate of the true majority-vote error (for checking the bound)."""
    if N % 2 == 0:
        N += 1  # avoid ties; majority is then unambiguous.
    rng = random.Random(seed)
    wrong = 0
    for _ in range(n_trials):
        successes = sum(1 for _ in range(N) if rng.random() < p)
        if successes < N / 2.0:  # strictly fewer than half correct → majority wrong.
            wrong += 1
    return wrong / n_trials


# ── Redundancy → pointer-record stability ───────────────────────────────────


def redundancy_decay(p: float, N_max: int = 101, step: int = 10) -> list[dict]:
    """Bound vs N, showing exponential decay of the record error."""
    rows = []
    for N in range(1, N_max + 1, step):
        rows.append({"N": N, "bound": record_error_bound(N, p),
                     "exponent": chernoff_exponent(p)})
    return rows


# ── Derivation certificate ──────────────────────────────────────────────────


def derivation_certificate() -> dict:
    return {
        "theorem": "T3 — Record Stabilization Bound",
        "deliverables": {
            "Chernoff / relative-entropy bound": "MATH — standard concentration inequality (credited)",
            "P_error(N) ≤ e^{−N·C(p)}": "TH-DET — applied to the commit channel with reliability p",
            "redundancy → pointer-record stability": (
                "MODEL — conditional reliability of independent classical copies"
            ),
        },
        "notes": [
            "C(p) = D(1/2 ‖ p) is the relative entropy between the coin-flip and p;",
            "the target alternative, independent copying events and reliability p are assumed;",
            "no first-outcome selection or pair-kernel decoherence rate is derived.",
        ],
        "exclusions": [
            "first_record_formation", "quantum_decoherence_rate",
            "physical_irreversibility", "record_production_rate",
        ],
        "status": "CONDITIONAL_CLASSICAL_STABILIZATION",
    }


# ── End-to-end T3 ───────────────────────────────────────────────────────────


def run_t3(p: float = 0.7, seed: int = 42) -> dict:
    """Demonstrate the conditional stabilization bound and compare a simulation."""
    rows = redundancy_decay(p, N_max=101, step=20)
    # Monte Carlo check at a few N.
    checks = []
    for N in (11, 51, 101):
        bound = record_error_bound(N, p)
        empirical = majority_vote_error(N, p, n_trials=50000, seed=seed + N)
        checks.append({"N": N, "bound": bound, "empirical": empirical,
                       "bound_holds": empirical <= bound * (1.0 + 1e-9)})

    bound_holds_all = all(c["bound_holds"] for c in checks)
    return {
        "p": p,
        "exponent_C": chernoff_exponent(p),
        "decay": rows,
        "checks": checks,
        "bound_holds_all": bound_holds_all,
        "certificate": derivation_certificate(),
        "interpretation": (
            f"p={p}, C(p)={chernoff_exponent(p):.4f}. Record error ≤ e^{{−N·C(p)}}; "
            f"Monte Carlo estimates lie below the bound at checked N ({bound_holds_all}); "
            f"this diagnostic is not a proof. Independent redundant copies stabilize "
            f"an assumed target; first-record formation is not derived."
        ),
    }
