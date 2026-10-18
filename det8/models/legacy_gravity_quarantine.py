"""Executable quarantine ledger for DET8's retired gravity program.

The entries in this module are governance metadata, not physical results.  A
module in :data:`FULLY_RETIRED` may be imported to reproduce historical
arithmetic, but it must not supply assumptions, constants, or conclusions to
an active DET model.  This boundary exists because those modules identify
``kappa`` or ``Pi`` with gravitational sources or metric data without an
independent derivation or observational bridge.

Mixed modules are listed separately so that their surviving non-gravity
utilities are not silently promoted into evidence for the retired mechanism.
Synthetic correspondence modules reproduce results after standard geometric
structure has been inserted; they are checks of implementation, not DET
derivations.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Final, Mapping


RETIRED: Final[str] = "RETIRED"
PARTIAL: Final[str] = "PARTIAL_QUARANTINE"
SYNTHETIC_CORRESPONDENCE: Final[str] = "SYNTHETIC_CORRESPONDENCE"


@dataclass(frozen=True)
class QuarantineRecord:
    """Machine-readable status for a legacy or salvaged module."""

    module: str
    status: str
    reason: str
    permitted_use: str
    empirical_claim: bool = False


def _record(module: str, reason: str) -> QuarantineRecord:
    return QuarantineRecord(
        module=module,
        status=RETIRED,
        reason=reason,
        permitted_use="historical reproduction and regression tests only",
        empirical_claim=False,
    )


_FULLY_RETIRED = {
    # Direct kappa-gravity laws and their simulations.
    "det8.models.q_gravity": _record(
        "det8.models.q_gravity", "Treats structural history as gravitational charge."
    ),
    "det8.models.det_gravity": _record(
        "det8.models.det_gravity", "Maps kappa conservation to a gravitational Poisson equation."
    ),
    "det8.models.gravity_v2": _record(
        "det8.models.gravity_v2", "Adds an underived kappa response to Newtonian gravity."
    ),
    "det8.models.gravity_experiment": _record(
        "det8.models.gravity_experiment", "Simulates an experiment for the withdrawn kappa-force law."
    ),
    "det8.models.newton_correspondence": _record(
        "det8.models.newton_correspondence", "Calibrates the withdrawn kappa source to Newtonian mass."
    ),
    "det8.models.unified_simulation": _record(
        "det8.models.unified_simulation", "Integrates the withdrawn kappa-gravity sector as active physics."
    ),
    # Retired phenomenology built on those laws.
    "det8.models.kappa_derivation": _record(
        "det8.models.kappa_derivation", "Constructs a galactic kappa profile for the withdrawn force law."
    ),
    "det8.models.sparc_analysis": _record(
        "det8.models.sparc_analysis", "Fits rotation curves with the withdrawn force law."
    ),
    "det8.models.cluster_dynamics": _record(
        "det8.models.cluster_dynamics", "Reinterprets inferred cluster masses through kappa-gravity."
    ),
    "det8.models.post_newtonian": _record(
        "det8.models.post_newtonian", "Inserts a kappa-dependent G into standard PPN formulas."
    ),
    "det8.models.flyby_anomaly": _record(
        "det8.models.flyby_anomaly", "Attributes flyby residuals to the withdrawn force law."
    ),
    "det8.models.remaining_items": _record(
        "det8.models.remaining_items", "Bundles retired galaxy, cluster, and BAO gravity claims."
    ),
    # Superseded Pi/kappa continuum and O7 chains.
    **{
        f"det8.models.{name}": _record(
            f"det8.models.{name}",
            "Uses inserted continuum geometry and/or the retired Pi/kappa gravity identification.",
        )
        for name in (
            "continuum_limit_proof",
            "continuum_limit_l234",
            "continuum_limit_step1",
            "continuum_limit_step2",
            "continuum_limit_step3",
            "continuum_limit_step4",
            "continuum_limit_step4p",
            "continuum_limit_concentration",
            "continuum_limit_lgh",
            "continuum_limit_bianchi",
            "continuum_limit_curvature",
            "continuum_limit_einstein",
            "continuum_limit_geometric",
            "o7_causal_spacetime",
            "o7_continuum_limit",
            "o7_derivation",
        )
    },
}

FULLY_RETIRED: Final[Mapping[str, QuarantineRecord]] = MappingProxyType(_FULLY_RETIRED)


PARTIALLY_QUARANTINED: Final[Mapping[str, tuple[str, ...]]] = MappingProxyType(
    {
        "det8.models.det8_core": ("LAMBDA_GAMMA and gravitational_charge",),
        "det8.models.det_units": (
            "gravity_shift_from_alpha",
            "alpha_from_gravity_shift",
            "gravity entries in coupling_implications and fit_lab_example",
        ),
        "det8.models.experimental_constraints": ("gravity and orbital-anomaly sections",),
        "det8.models.gps_analysis": ("kappa-gravity interpretation; clock-ratio arithmetic may survive",),
        "det8.models.track_a": ("legacy lambda_gamma bookkeeping",),
    }
)


SALVAGED_CORRESPONDENCE: Final[Mapping[str, QuarantineRecord]] = MappingProxyType(
    {
        "det8.models.lorentz_derivation": QuarantineRecord(
            module="det8.models.lorentz_derivation",
            status=SYNTHETIC_CORRESPONDENCE,
            reason=(
                "Uses supplied Minkowski coordinates, interval, light cone, and Lorentz boosts; "
                "it checks standard special-relativistic identities."
            ),
            permitted_use="known-answer synthetic correspondence tests",
            empirical_claim=False,
        ),
        "det8.models.order_count_geometry": QuarantineRecord(
            module="det8.models.order_count_geometry",
            status=SYNTHETIC_CORRESPONDENCE,
            reason=(
                "Tests order-and-count estimators on samples generated from a supplied "
                "Minkowski embedding."
            ),
            permitted_use="synthetic estimator validation with explicit generating geometry",
            empirical_claim=False,
        ),
    }
)


def quarantine_record(module_name: str) -> QuarantineRecord:
    """Return a retired module's record, rejecting unregistered use."""

    try:
        return FULLY_RETIRED[module_name]
    except KeyError as exc:
        raise KeyError(f"{module_name!r} is not registered as fully retired") from exc


def is_fully_retired(module_name: str) -> bool:
    """Whether *module_name* belongs to the historical gravity quarantine."""

    return module_name in FULLY_RETIRED


def quarantine_summary() -> dict[str, object]:
    """Return the policy in a serialization-friendly form."""

    return {
        "policy": (
            "Fully retired modules cannot provide dependencies or evidence to active DET models."
        ),
        "fully_retired": tuple(sorted(FULLY_RETIRED)),
        "partially_quarantined": tuple(sorted(PARTIALLY_QUARANTINED)),
        "salvaged_correspondence": tuple(sorted(SALVAGED_CORRESPONDENCE)),
        "active_empirical_claims_from_retired_modules": 0,
    }
