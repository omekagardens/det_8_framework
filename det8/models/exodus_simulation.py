"""Exodus electrostatic-pressure equations translated into DET8.

This module is a governed research sandbox, not a DET8 force prediction.
It implements the equations asserted in US 11,511,891 B2 and then applies
DET8's existing conservation rule to the momentum ledger.

The translation is deliberately small:

* Electrode/surface regions are DET nodes/regimes.
* A momentum-carrying interaction is a DET bond with
  ``pi_ij = -pi_ji``.
* The patent's surface-pressure imbalance is an apparent force across a
  chosen apparatus cut.
* A possibility is DET-admissible only when the full relational regime has
  zero momentum residual.
* ``kappa`` is used only in an explicitly optional history-sensitivity ansatz;
  it is not a gravity or thrust source.

The central result is structural: an apparent Exodus force can be represented
as an internal stress (zero apparatus thrust) or as exchange with an external
boundary (nonzero apparatus thrust and an opposite environmental impulse).
An endpoint-free force is rejected by DET8 conservation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from enum import Enum

from det8.models.bonds import BondNetwork
from det8.models.det8_core import NodeRecord


EPSILON_0 = 8.854_187_812_8e-12  # F/m, exact enough for this sandbox.
PATENT_REFERENCE_VOLTAGE_V = 40_000.0
PATENT_REPORTED_FORCE_N = 237e-6


@dataclass(frozen=True)
class Equation11Geometry:
    """Effective two-patch geometry for patent equations (10)-(13).

    ``field_gain_i`` converts the parallel-plate estimate ``|V| / gap`` to
    the effective field on patch i. The model is one-dimensional along the
    claimed thrust axis and therefore does not replace a closed-surface
    Maxwell-stress calculation.
    """

    area_1_m2: float
    area_2_m2: float
    gap_m: float
    field_gain_1: float = 1.0
    field_gain_2: float = 1.0

    def __post_init__(self) -> None:
        if self.area_1_m2 <= 0.0 or self.area_2_m2 <= 0.0:
            raise ValueError("Surface areas must be positive")
        if self.gap_m <= 0.0:
            raise ValueError("Electrode gap must be positive")
        if self.field_gain_1 < 0.0 or self.field_gain_2 < 0.0:
            raise ValueError("Field gains must be non-negative")

    def field_amplitudes(self, voltage_v: float) -> tuple[float, float]:
        base_field = abs(voltage_v) / self.gap_m
        return (
            self.field_gain_1 * base_field,
            self.field_gain_2 * base_field,
        )


def calibrated_reference_geometry() -> Equation11Geometry:
    """Return a transparent effective geometry calibrated to 237 uN at 40 kV.

    The patent reports an average force near 237 uN and a supply up to 40 kV,
    but does not publish enough dimensions and field-map data to reconstruct
    that test article. This synthetic 1 cm gap / 1 cm^2 patch geometry chooses
    only ``field_gain_2`` to reproduce the reported point under equation (11).
    It must not be mistaken for a reconstruction of the physical article.
    """

    area = 1e-4
    gap = 1e-2
    base_field = PATENT_REFERENCE_VOLTAGE_V / gap
    gain_square_delta = PATENT_REPORTED_FORCE_N / (
        EPSILON_0 * area * base_field**2
    )
    return Equation11Geometry(
        area_1_m2=area,
        area_2_m2=area,
        gap_m=gap,
        field_gain_1=1.0,
        field_gain_2=math.sqrt(1.0 + gain_square_delta),
    )


def patent_equation_11_force(
    geometry: Equation11Geometry,
    voltage_v: float,
) -> float:
    """Patent equation (11): F = eps0 (E2^2 A2 - E1^2 A1).

    This reproduces the patent's asserted patch-sum force. It does not assert
    that the value is the force on a complete isolated apparatus.
    """

    e1, e2 = geometry.field_amplitudes(voltage_v)
    return EPSILON_0 * (
        e2**2 * geometry.area_2_m2 - e1**2 * geometry.area_1_m2
    )


def maxwell_patch_pressure_force(
    geometry: Equation11Geometry,
    voltage_v: float,
) -> float:
    """Scalar Maxwell-pressure comparison for the same two selected patches.

    A conductor surface in a normal electrostatic field has pressure
    ``eps0 E^2 / 2``. Even this comparison remains a patch calculation; the
    net force requires the Maxwell stress tensor over a closed boundary.
    """

    return 0.5 * patent_equation_11_force(geometry, voltage_v)


class MomentumChannel(str, Enum):
    """Candidate endpoint for the apparent surface-force impulse."""

    INTERNAL = "internal"
    BOUNDARY = "boundary"
    ORPHAN = "orphan"


@dataclass(frozen=True)
class MomentumLedger:
    """Committed one-dimensional momentum for a chosen DET regime cut."""

    channel: str
    patch_impulse_kg_m_s: float
    apparatus_remainder_impulse_kg_m_s: float
    environment_impulse_kg_m_s: float
    apparatus_impulse_kg_m_s: float
    global_residual_kg_m_s: float
    conserved: bool
    det_admissible: bool
    bond_endpoint: str | None
    n_relational_bonds: int


def commit_momentum_channel(
    apparent_force_n: float,
    duration_s: float,
    channel: MomentumChannel,
) -> MomentumLedger:
    """Commit the patent-force impulse to a DET momentum ledger.

    INTERNAL:
        The opposite endpoint is another part of the apparatus. Local stress
        is nonzero, but total apparatus impulse is zero.
    BOUNDARY:
        The opposite endpoint lies outside the apparatus. Apparatus momentum
        is nonzero while apparatus + environment remains conserved.
    ORPHAN:
        No opposite endpoint is recorded. This is retained as a diagnostic
        counterexample and rejected by the conservation gate.
    """

    if duration_s < 0.0:
        raise ValueError("Duration must be non-negative")

    impulse = apparent_force_n * duration_s
    network = BondNetwork()

    if channel is MomentumChannel.INTERNAL:
        remainder = -impulse
        environment = 0.0
        endpoint = "apparatus_remainder"
        network.add_bond(0, 1, pi=impulse)
    elif channel is MomentumChannel.BOUNDARY:
        remainder = 0.0
        environment = -impulse
        endpoint = "environment"
        network.add_bond(0, 2, pi=impulse)
    elif channel is MomentumChannel.ORPHAN:
        remainder = 0.0
        environment = 0.0
        endpoint = None
    else:  # pragma: no cover - Enum makes this unreachable for typed callers.
        raise ValueError(f"Unknown momentum channel: {channel}")

    apparatus = impulse + remainder
    residual = apparatus + environment
    conserved = abs(residual) <= 1e-15
    return MomentumLedger(
        channel=channel.value,
        patch_impulse_kg_m_s=impulse,
        apparatus_remainder_impulse_kg_m_s=remainder,
        environment_impulse_kg_m_s=environment,
        apparatus_impulse_kg_m_s=apparatus,
        global_residual_kg_m_s=residual,
        conserved=conserved,
        det_admissible=conserved and len(network) == 1,
        bond_endpoint=endpoint,
        n_relational_bonds=len(network),
    )


@dataclass(frozen=True)
class BoundaryCondition:
    """Phenomenological boundary relation used for discriminator sweeps.

    This is not derived from DET8 or the patent. It is a declared ansatz that
    turns the discussion's relational-boundary question into an executable
    sensitivity study.
    """

    distance_m: float
    relative_permittivity: float = 1.0
    shielding_fraction: float = 0.0
    coupling_length_m: float = 0.25
    channel_strength: float = 1.0

    def __post_init__(self) -> None:
        if self.distance_m < 0.0:
            raise ValueError("Boundary distance must be non-negative")
        if self.relative_permittivity <= 0.0:
            raise ValueError("Relative permittivity must be positive")
        if not 0.0 <= self.shielding_fraction <= 1.0:
            raise ValueError("Shielding fraction must lie in [0, 1]")
        if self.coupling_length_m <= 0.0:
            raise ValueError("Coupling length must be positive")
        if self.channel_strength < 0.0:
            raise ValueError("Channel strength must be non-negative")

    @property
    def relational_coupling(self) -> float:
        dielectric_boost = 1.0 + 0.5 * (
            (self.relative_permittivity - 1.0)
            / (self.relative_permittivity + 1.0)
        )
        distance_factor = 1.0 / (
            1.0 + (self.distance_m / self.coupling_length_m) ** 2
        )
        return (
            self.channel_strength
            * dielectric_boost
            * (1.0 - self.shielding_fraction)
            * distance_factor
        )

    def coupled_force(self, equation_11_force_n: float) -> float:
        return equation_11_force_n * self.relational_coupling


def boundary_sweep(
    equation_11_force_n: float,
    distances_m: tuple[float, ...] = (0.05, 0.10, 0.20, 0.50, 1.00),
    relative_permittivity: float = 1.0,
    shielding_fraction: float = 0.0,
) -> list[dict[str, float]]:
    """Evaluate the declared external-boundary ansatz over wall distance."""

    rows: list[dict[str, float]] = []
    for distance in distances_m:
        condition = BoundaryCondition(
            distance_m=distance,
            relative_permittivity=relative_permittivity,
            shielding_fraction=shielding_fraction,
        )
        rows.append(
            {
                "distance_m": distance,
                "relational_coupling": condition.relational_coupling,
                "apparent_force_n": condition.coupled_force(equation_11_force_n),
            }
        )
    return rows


@dataclass
class StructuralHistoryState:
    """Optional R-/kappa sensitivity model for matched-final-state tests."""

    record: NodeRecord = field(default_factory=NodeRecord)
    relaxation_time_s: float = 5.0
    normalization_voltage_v: float = 70_000.0

    def expose(self, voltage_v: float, dwell_s: float) -> float:
        if dwell_s < 0.0:
            raise ValueError("Dwell time must be non-negative")
        if self.relaxation_time_s <= 0.0:
            raise ValueError("Relaxation time must be positive")
        target = min(1.0, (abs(voltage_v) / self.normalization_voltage_v) ** 2)
        decay = math.exp(-dwell_s / self.relaxation_time_s)
        self.record.kappa = target + (self.record.kappa - target) * decay
        return self.record.kappa

    def target_at(self, voltage_v: float) -> float:
        return min(1.0, (abs(voltage_v) / self.normalization_voltage_v) ** 2)


def run_history_protocol(
    geometry: Equation11Geometry,
    voltages_v: tuple[float, ...],
    dwell_s: float = 1.0,
    lambda_history: float = 0.2,
) -> dict:
    """Run a voltage path and optionally couple kappa to the patch force.

    ``lambda_history`` is a declared sensitivity parameter. Zero recovers the
    patent equation with no DET history effect. A nonzero value is useful only
    for designing matched-final-state experiments; ordinary dielectric and
    mechanical hysteresis must be removed before assigning any DET meaning.
    """

    if not voltages_v:
        raise ValueError("A history protocol needs at least one voltage")

    history = StructuralHistoryState()
    trace = []
    for voltage in voltages_v:
        kappa = history.expose(voltage, dwell_s)
        base_force = patent_equation_11_force(geometry, voltage)
        target = history.target_at(voltage)
        multiplier = 1.0 + lambda_history * (kappa - target)
        trace.append(
            {
                "voltage_v": voltage,
                "kappa": kappa,
                "base_force_n": base_force,
                "history_multiplier": multiplier,
                "history_adjusted_force_n": base_force * multiplier,
            }
        )

    return {
        "lambda_history": lambda_history,
        "trace": trace,
        "final": trace[-1],
    }


def equation_13_force(
    geometry: Equation11Geometry,
    voltage_amplitude_v: float,
    angular_frequency_rad_s: float,
    phase_rad: float,
    time_s: float,
) -> float:
    """Differentiate patent equation (12) exactly to obtain equation (13).

    P(t) = eps0 t [E2(t)^2 A2 - E1(t)^2 A1]
    F(t) = eps0 [D(t) + t dD(t)/dt]

    Both effective fields share the waveform phase, as in the patent's simple
    sinusoidal example.
    """

    if angular_frequency_rad_s <= 0.0:
        raise ValueError("Angular frequency must be positive")

    amp1, amp2 = geometry.field_amplitudes(voltage_amplitude_v)
    angle = angular_frequency_rad_s * time_s + phase_rad
    sine = math.sin(angle)
    cosine = math.cos(angle)
    e1 = amp1 * sine
    e2 = amp2 * sine
    de1_dt = amp1 * angular_frequency_rad_s * cosine
    de2_dt = amp2 * angular_frequency_rad_s * cosine
    difference = e2**2 * geometry.area_2_m2 - e1**2 * geometry.area_1_m2
    difference_rate = (
        2.0 * e2 * de2_dt * geometry.area_2_m2
        - 2.0 * e1 * de1_dt * geometry.area_1_m2
    )
    return EPSILON_0 * (difference + time_s * difference_rate)


def equation_13_cycle_average(
    geometry: Equation11Geometry,
    voltage_amplitude_v: float,
    frequency_hz: float,
    phase_rad: float,
    start_time_s: float = 0.0,
    samples: int = 20_001,
) -> float:
    """Numerically average equation (13) over one complete cycle."""

    if frequency_hz <= 0.0:
        raise ValueError("Frequency must be positive")
    if samples < 3:
        raise ValueError("At least three samples are required")

    omega = 2.0 * math.pi * frequency_hz
    period = 1.0 / frequency_hz
    dt = period / (samples - 1)
    integral = 0.0
    previous = equation_13_force(
        geometry, voltage_amplitude_v, omega, phase_rad, start_time_s
    )
    for index in range(1, samples):
        time_s = start_time_s + index * dt
        current = equation_13_force(
            geometry, voltage_amplitude_v, omega, phase_rad, time_s
        )
        integral += 0.5 * (previous + current) * dt
        previous = current
    return integral / period


def patent_narrative_cycle_average(
    geometry: Equation11Geometry,
    voltage_amplitude_v: float,
    phase_rad: float,
) -> float:
    """Return the AC average stated in the patent prose after equation (15).

    The prose assigns ``C^2/2`` to the pressure term and ``+/- C^2/4``
    to the time-dependent term. Direct differentiation of equation (12)
    instead gives a ``+/- C^2/2`` time term. Keeping this separate makes the
    patent's internal factor-of-two mismatch executable and testable.
    """

    dc_amplitude_force = patent_equation_11_force(
        geometry, voltage_amplitude_v
    )
    factor = 0.5 - 0.25 * math.cos(2.0 * phase_rad)
    return dc_amplitude_force * factor


def time_translation_shift(
    geometry: Equation11Geometry,
    voltage_amplitude_v: float,
    frequency_hz: float,
    phase_rad: float = 0.0,
) -> dict[str, float]:
    """Compare equation (13) one period apart at identical field state."""

    omega = 2.0 * math.pi * frequency_hz
    period = 1.0 / frequency_hz
    first_time = period / 8.0
    first = equation_13_force(
        geometry, voltage_amplitude_v, omega, phase_rad, first_time
    )
    shifted = equation_13_force(
        geometry, voltage_amplitude_v, omega, phase_rad, first_time + period
    )
    return {
        "time_s": first_time,
        "shifted_time_s": first_time + period,
        "force_n": first,
        "shifted_force_n": shifted,
        "difference_n": shifted - first,
    }


def run_reference_suite() -> dict:
    """Run the reference voltage, closure, boundary, history, and AC sweeps."""

    geometry = calibrated_reference_geometry()
    reference_force = patent_equation_11_force(
        geometry, PATENT_REFERENCE_VOLTAGE_V
    )

    voltage_sweep = []
    for voltage in (10_000.0, 20_000.0, 30_000.0, 40_000.0):
        voltage_sweep.append(
            {
                "voltage_v": voltage,
                "force_n": patent_equation_11_force(geometry, voltage),
            }
        )

    ledgers = {
        channel.value: asdict(
            commit_momentum_channel(reference_force, 1.0, channel)
        )
        for channel in MomentumChannel
    }

    history_up = run_history_protocol(
        geometry, (0.0, 30_000.0, 50_000.0)
    )
    history_down = run_history_protocol(
        geometry, (70_000.0, 50_000.0)
    )

    frequency_hz = 1_000.0
    phase_zero_average = equation_13_cycle_average(
        geometry, PATENT_REFERENCE_VOLTAGE_V, frequency_hz, 0.0
    )
    phase_quadrature_average = equation_13_cycle_average(
        geometry,
        PATENT_REFERENCE_VOLTAGE_V,
        frequency_hz,
        math.pi / 2.0,
    )

    return {
        "status": "research sandbox; not a DET8 prediction",
        "patent": "US11511891B2",
        "reference": {
            "voltage_v": PATENT_REFERENCE_VOLTAGE_V,
            "reported_force_n": PATENT_REPORTED_FORCE_N,
            "equation_11_force_n": reference_force,
            "maxwell_selected_patch_comparison_n": maxwell_patch_pressure_force(
                geometry, PATENT_REFERENCE_VOLTAGE_V
            ),
            "geometry": asdict(geometry),
        },
        "voltage_sweep": voltage_sweep,
        "polarity_check": {
            "positive_n": patent_equation_11_force(
                geometry, PATENT_REFERENCE_VOLTAGE_V
            ),
            "negative_n": patent_equation_11_force(
                geometry, -PATENT_REFERENCE_VOLTAGE_V
            ),
        },
        "det_conservation_gate": ledgers,
        "boundary_sweep": boundary_sweep(reference_force),
        "history_matched_final_voltage": {
            "up_path": history_up,
            "down_path": history_down,
            "force_difference_n": (
                history_down["final"]["history_adjusted_force_n"]
                - history_up["final"]["history_adjusted_force_n"]
            ),
            "warning": "Declared sensitivity ansatz; standard hysteresis is not removed in code.",
        },
        "ac_equation_audit": {
            "frequency_hz": frequency_hz,
            "exact_phase_0_average_n": phase_zero_average,
            "patent_narrative_phase_0_average_n": patent_narrative_cycle_average(
                geometry, PATENT_REFERENCE_VOLTAGE_V, 0.0
            ),
            "exact_phase_90_average_n": phase_quadrature_average,
            "patent_narrative_phase_90_average_n": patent_narrative_cycle_average(
                geometry, PATENT_REFERENCE_VOLTAGE_V, math.pi / 2.0
            ),
            "time_translation_shift": time_translation_shift(
                geometry, PATENT_REFERENCE_VOLTAGE_V, frequency_hz
            ),
        },
    }


def main() -> None:
    print(json.dumps(run_reference_suite(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
