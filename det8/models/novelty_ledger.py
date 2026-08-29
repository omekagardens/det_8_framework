"""Instrument-productivity register for the DET lens.

The novelty ledger records every generated probe against its target theory,
its status, its outcome, and — crucially — what a null result costs the
*instrument*.  It is the falsification surface for DET as a lens: the ontology
is chosen, not evidenced, so the falsifiable quantity is whether the lens's
probes produce surviving novelties above the null rate.

The companion generative-warrant gate (DG-WARRANT) downgrades the lens after
``downgrade_after`` executed probes with zero surviving novelties.  It applies
the existing DG-gate pattern to the instrument rather than to a single claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


STATUSES = ("gated", "unexecuted", "executed", "active")
OUTCOMES = ("null", "surviving_novelty")
WARRANT_STATUSES = ("ACTIVE", "SUSTAINED", "DOWNGRADED")


@dataclass(frozen=True)
class NoveltyEntry:
    probe: str
    target_theory: str
    status: str
    cost_if_null: str
    outcome: str | None = None

    def __post_init__(self) -> None:
        if not self.probe or not self.target_theory or not self.cost_if_null:
            raise ValueError("probe, target theory, and cost-if-null are required")
        if self.status not in STATUSES:
            raise ValueError("status must be one of %s" % (STATUSES,))
        if self.status == "executed":
            if self.outcome not in OUTCOMES:
                raise ValueError(
                    "an executed probe must carry a null or surviving-novelty outcome"
                )
        elif self.outcome is not None:
            raise ValueError("only executed probes may carry an outcome")


@dataclass(frozen=True)
class NoveltyLedger:
    entries: Tuple[NoveltyEntry, ...]

    def __post_init__(self) -> None:
        probes = [entry.probe for entry in self.entries]
        if len(probes) != len(set(probes)):
            raise ValueError("ledger probe identifiers must be unique")

    def executed(self) -> Tuple[NoveltyEntry, ...]:
        return tuple(entry for entry in self.entries if entry.status == "executed")

    def surviving_novelties(self) -> int:
        return sum(
            1 for entry in self.executed() if entry.outcome == "surviving_novelty"
        )


@dataclass(frozen=True)
class GenerativeWarrant:
    executed_probes: int
    surviving_novelties: int
    downgrade_after: int = 5

    def __post_init__(self) -> None:
        if self.executed_probes < 0 or self.surviving_novelties < 0:
            raise ValueError("probe counts cannot be negative")
        if self.surviving_novelties > self.executed_probes:
            raise ValueError("surviving novelties cannot exceed executed probes")
        if self.downgrade_after < 1:
            raise ValueError("downgrade threshold must be positive")

    @property
    def status(self) -> str:
        if self.executed_probes < self.downgrade_after:
            return "ACTIVE"
        if self.surviving_novelties == 0:
            return "DOWNGRADED"
        return "SUSTAINED"


def warrant_from_ledger(
    ledger: NoveltyLedger, *, downgrade_after: int = 5
) -> GenerativeWarrant:
    """DG-WARRANT: derive the lens's generative warrant from executed probes."""

    return GenerativeWarrant(
        executed_probes=len(ledger.executed()),
        surviving_novelties=ledger.surviving_novelties(),
        downgrade_after=downgrade_after,
    )


def seed_novelty_ledger() -> NoveltyLedger:
    """The honest current contents of the lens's productivity register."""

    return NoveltyLedger(
        (
            NoveltyEntry(
                probe="clock anomaly (FL-1): Δν/ν = λ_P·κ/(1+λ_P·κ) common-mode universality",
                target_theory="standard physics (null clock universality)",
                status="gated",
                cost_if_null=(
                    "one logged miss; only a λ_P·Δκ product bound "
                    "(prerequisites F9 + independent κ missing)"
                ),
            ),
            NoveltyEntry(
                probe="recovery-rate discriminator (F9/FL-4): τ_rec(T) T-independent vs Arrhenius",
                target_theory="standard annealing / defect-density kinetics",
                status="unexecuted",
                cost_if_null=(
                    "cheapest probe; literature (densified silica, E_a = 2.64 eV) "
                    "already predicts the Arrhenius null, but no (T, τ) data is "
                    "ingested — F9 is not executed against real data"
                ),
            ),
            NoveltyEntry(
                probe="operational κ̂ + L0/L1/L2 ladder (metrology residual)",
                target_theory="standard materials metrology (f_std)",
                status="unexecuted",
                cost_if_null=(
                    "none — L0/L1 value is unconditional, publishable "
                    "even if DET is false"
                ),
            ),
            NoveltyEntry(
                probe="κ-dependent decoherence functional D_κ (three-slit I₃ = κ·r)",
                target_theory="grade-2 (quantum) decoherence functional (Sorkin)",
                status="executed",
                outcome="null",
                cost_if_null=(
                    "κ_DET·r < ε_exp·I₂_ref: κ_DET ≲ 1.5×10⁻⁵ (Kauten 2017, r=1); "
                    "consistent with standard QM — first logged miss"
                ),
            ),
            NoveltyEntry(
                probe="RET engine (discrepancy adjudication + engine validation)",
                target_theory="methodological — known-answer false-positive refusal",
                status="active",
                cost_if_null="none — methodological yield, not physics yield",
            ),
        )
    )
