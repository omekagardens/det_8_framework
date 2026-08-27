"""Phase-2 discriminator runs for the DET8 Exodus research sandbox.

The reference translation in :mod:`det8.models.exodus_simulation` establishes
the conservation choices. This module asks which measurements distinguish
those choices:

1. A conventional image-charge surrogate for coupling to a grounded wall.
2. Noisy model selection across wall-distance sweeps.
3. Simultaneous momentum inventories for internal, boundary, and orphan cuts.
4. Detectability estimates for the declared kappa/history sensitivity ansatz.
5. Phase and frequency sweeps of the patent's time-varying equations.

None of these runs promotes Exodus thrust, the boundary ansatz, or the history
ansatz to a DET8 prediction.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass

from det8.models.exodus_simulation import (
    EPSILON_0,
    PATENT_REFERENCE_VOLTAGE_V,
    PATENT_REPORTED_FORCE_N,
    Equation11Geometry,
    calibrated_reference_geometry,
    equation_13_cycle_average,
    patent_equation_11_force,
    patent_narrative_cycle_average,
    run_history_protocol,
    time_translation_shift,
)


COULOMB_K = 1.0 / (4.0 * math.pi * EPSILON_0)


def _force_between_point_charges(
    charge_i_c: float,
    position_i_m: float,
    charge_j_c: float,
    position_j_m: float,
) -> float:
    """One-dimensional Coulomb force on i due to j."""

    displacement = position_i_m - position_j_m
    if displacement == 0.0:
        raise ValueError("Point charges cannot occupy the same position")
    return (
        COULOMB_K
        * charge_i_c
        * charge_j_c
        * displacement
        / abs(displacement) ** 3
    )


def grounded_plane_dipole_ledger(
    center_distance_m: float,
    separation_m: float,
    charge_c: float,
) -> dict[str, float]:
    """Compute a neutral dipole's force near an infinite grounded plane.

    The grounded plane lies at x=0. Real charges +q and -q lie at
    ``center_distance - separation/2`` and ``center_distance + separation/2``.
    The method of images replaces the plane by image charges of opposite sign.

    This is a conventional electrostatic boundary surrogate, not a geometric
    reconstruction of the Exodus device. It is useful because it has an
    explicit external endpoint and an exactly closed momentum ledger.
    """

    if separation_m <= 0.0:
        raise ValueError("Dipole separation must be positive")
    if center_distance_m <= separation_m / 2.0:
        raise ValueError("Both charges must lie in front of the grounded plane")

    real = (
        (center_distance_m - separation_m / 2.0, charge_c),
        (center_distance_m + separation_m / 2.0, -charge_c),
    )
    images = tuple((-position, -charge) for position, charge in real)

    internal_forces = []
    boundary_forces = []
    for index, (position_i, charge_i) in enumerate(real):
        internal = 0.0
        for other_index, (position_j, charge_j) in enumerate(real):
            if index != other_index:
                internal += _force_between_point_charges(
                    charge_i, position_i, charge_j, position_j
                )
        boundary = sum(
            _force_between_point_charges(
                charge_i, position_i, image_charge, image_position
            )
            for image_position, image_charge in images
        )
        internal_forces.append(internal)
        boundary_forces.append(boundary)

    internal_sum = sum(internal_forces)
    device_boundary_force = sum(boundary_forces)
    wall_reaction = -device_boundary_force
    return {
        "internal_force_sum_n": internal_sum,
        "device_boundary_force_n": device_boundary_force,
        "wall_reaction_force_n": wall_reaction,
        "global_residual_n": device_boundary_force + wall_reaction,
    }


def calibrate_image_dipole_charge(
    target_force_n: float = PATENT_REPORTED_FORCE_N,
    reference_distance_m: float = 0.10,
    separation_m: float = 0.01,
) -> float:
    """Choose q so the wall-coupled dipole matches a reference force."""

    if target_force_n <= 0.0:
        raise ValueError("Target force must be positive")
    unit = abs(
        grounded_plane_dipole_ledger(
            reference_distance_m, separation_m, 1.0
        )["device_boundary_force_n"]
    )
    return math.sqrt(target_force_n / unit)


def image_charge_boundary_sweep(
    distances_m: tuple[float, ...] = (0.03, 0.05, 0.10, 0.20, 0.50),
    reference_distance_m: float = 0.10,
    separation_m: float = 0.01,
) -> dict:
    """Run the conventional grounded-wall surrogate over distance."""

    charge = calibrate_image_dipole_charge(
        reference_distance_m=reference_distance_m,
        separation_m=separation_m,
    )
    rows = []
    for distance in distances_m:
        ledger = grounded_plane_dipole_ledger(distance, separation_m, charge)
        rows.append(
            {
                "distance_m": distance,
                "force_magnitude_n": abs(ledger["device_boundary_force_n"]),
                "device_force_n": ledger["device_boundary_force_n"],
                "wall_reaction_n": ledger["wall_reaction_force_n"],
                "global_residual_n": ledger["global_residual_n"],
            }
        )
    return {
        "status": "conventional image-charge surrogate; not an Exodus geometry model",
        "reference_distance_m": reference_distance_m,
        "separation_m": separation_m,
        "calibrated_charge_c": charge,
        "rows": rows,
    }


def _fit_scaled_shape(
    observations: list[tuple[float, float]],
    shape: dict[float, float],
    parameter_count: int = 1,
) -> dict[str, float]:
    numerator = sum(shape[distance] * force for distance, force in observations)
    denominator = sum(shape[distance] ** 2 for distance, _ in observations)
    scale = numerator / denominator if denominator > 0.0 else 0.0
    residual_sum_squares = sum(
        (force - scale * shape[distance]) ** 2
        for distance, force in observations
    )
    n = len(observations)
    mean_square = max(residual_sum_squares / n, 1e-300)
    aic = n * math.log(mean_square) + 2.0 * parameter_count
    return {
        "scale_n": scale,
        "rss_n2": residual_sum_squares,
        "aic": aic,
    }


def noisy_boundary_model_selection(
    noise_sigma_n: float = 5e-6,
    replicates_per_distance: int = 5,
    seed: int = 20_260_823,
) -> dict:
    """Test whether a wall-attached signal is distinguishable from constants.

    Synthetic observations are generated from the image-charge dipole model.
    Four models are compared: null, constant, inverse-square, and the correct
    image-dipole shape. This quantifies the value of changing the boundary
    rather than repeating a single geometry.
    """

    if noise_sigma_n <= 0.0:
        raise ValueError("Noise sigma must be positive")
    if replicates_per_distance < 1:
        raise ValueError("At least one replicate is required")

    distances = (0.08, 0.10, 0.12, 0.15, 0.20)
    reference_distance = 0.10
    separation = 0.01
    charge = calibrate_image_dipole_charge(
        reference_distance_m=reference_distance,
        separation_m=separation,
    )

    true_force = {
        distance: abs(
            grounded_plane_dipole_ledger(distance, separation, charge)[
                "device_boundary_force_n"
            ]
        )
        for distance in distances
    }
    image_shape = {
        distance: true_force[distance] / true_force[reference_distance]
        for distance in distances
    }
    shapes = {
        "constant": {distance: 1.0 for distance in distances},
        "inverse_square": {
            distance: (reference_distance / distance) ** 2
            for distance in distances
        },
        "image_dipole": image_shape,
    }

    rng = random.Random(seed)
    observations = []
    aggregates = []
    for distance in distances:
        values = [
            true_force[distance] + rng.gauss(0.0, noise_sigma_n)
            for _ in range(replicates_per_distance)
        ]
        observations.extend((distance, value) for value in values)
        aggregates.append(
            {
                "distance_m": distance,
                "true_force_n": true_force[distance],
                "observed_mean_n": sum(values) / len(values),
            }
        )

    null_rss = sum(force**2 for _, force in observations)
    n = len(observations)
    fits = {
        "null": {
            "scale_n": 0.0,
            "rss_n2": null_rss,
            "aic": n * math.log(max(null_rss / n, 1e-300)),
        }
    }
    for name, shape in shapes.items():
        fits[name] = _fit_scaled_shape(observations, shape)

    best_aic = min(fit["aic"] for fit in fits.values())
    raw_weights = {
        name: math.exp(-0.5 * (fit["aic"] - best_aic))
        for name, fit in fits.items()
    }
    weight_total = sum(raw_weights.values())
    for name, fit in fits.items():
        fit["delta_aic"] = fit["aic"] - best_aic
        fit["akaike_weight"] = raw_weights[name] / weight_total

    best_model = min(fits, key=lambda name: fits[name]["aic"])
    return {
        "seed": seed,
        "noise_sigma_n": noise_sigma_n,
        "replicates_per_distance": replicates_per_distance,
        "best_model": best_model,
        "aggregates": aggregates,
        "fits": fits,
    }


@dataclass(frozen=True)
class MomentumScenario:
    patch_force_n: float
    apparatus_remainder_force_n: float
    environment_force_n: float
    field_momentum_rate_n: float = 0.0


def noisy_momentum_inventory(
    noise_sigma_per_channel_n: float = 5e-6,
    samples: int = 25,
    seed: int = 8_023,
) -> dict:
    """Measure all candidate endpoints and test global closure."""

    if noise_sigma_per_channel_n <= 0.0:
        raise ValueError("Noise sigma must be positive")
    if samples < 1:
        raise ValueError("At least one sample is required")

    force = PATENT_REPORTED_FORCE_N
    scenarios = {
        "internal": MomentumScenario(force, -force, 0.0),
        "external_boundary": MomentumScenario(force, 0.0, -force),
        "orphan": MomentumScenario(force, 0.0, 0.0),
    }

    results = {}
    for scenario_index, (name, scenario) in enumerate(scenarios.items()):
        rng = random.Random(seed + scenario_index)
        component_names = (
            "patch_force_n",
            "apparatus_remainder_force_n",
            "environment_force_n",
            "field_momentum_rate_n",
        )
        measured = {component: [] for component in component_names}
        for _ in range(samples):
            for component in component_names:
                true_value = getattr(scenario, component)
                measured[component].append(
                    true_value + rng.gauss(0.0, noise_sigma_per_channel_n)
                )

        means = {
            component: sum(values) / len(values)
            for component, values in measured.items()
        }
        apparatus_mean = (
            means["patch_force_n"] + means["apparatus_remainder_force_n"]
        )
        residual_mean = sum(means.values())
        apparatus_standard_error = (
            math.sqrt(2.0) * noise_sigma_per_channel_n / math.sqrt(samples)
        )
        closure_standard_error = (
            2.0 * noise_sigma_per_channel_n / math.sqrt(samples)
        )
        results[name] = {
            "measured_component_means_n": means,
            "apparatus_force_mean_n": apparatus_mean,
            "apparatus_signal_z": abs(apparatus_mean) / apparatus_standard_error,
            "closure_residual_mean_n": residual_mean,
            "closure_residual_z": abs(residual_mean) / closure_standard_error,
            "closure_passes_5sigma": abs(residual_mean) < 5.0 * closure_standard_error,
        }

    return {
        "noise_sigma_per_channel_n": noise_sigma_per_channel_n,
        "samples": samples,
        "scenarios": results,
    }


def history_detectability_grid(
    geometry: Equation11Geometry | None = None,
    noise_sigma_n: float = 5e-6,
    target_sigma: float = 5.0,
) -> dict:
    """Estimate repeats per voltage path needed to resolve history coupling."""

    if noise_sigma_n <= 0.0:
        raise ValueError("Noise sigma must be positive")
    if target_sigma <= 0.0:
        raise ValueError("Target sigma must be positive")

    geometry = geometry or calibrated_reference_geometry()
    rows = []
    for dwell_s in (0.2, 1.0, 5.0, 20.0):
        for coupling in (0.0, 0.02, 0.05, 0.10, 0.20):
            up = run_history_protocol(
                geometry,
                (0.0, 30_000.0, 50_000.0),
                dwell_s=dwell_s,
                lambda_history=coupling,
            )
            down = run_history_protocol(
                geometry,
                (70_000.0, 50_000.0),
                dwell_s=dwell_s,
                lambda_history=coupling,
            )
            difference = abs(
                down["final"]["history_adjusted_force_n"]
                - up["final"]["history_adjusted_force_n"]
            )
            if difference <= 1e-18:
                repeats = None
            else:
                repeats = math.ceil(
                    (
                        target_sigma
                        * math.sqrt(2.0)
                        * noise_sigma_n
                        / difference
                    )
                    ** 2
                )
            rows.append(
                {
                    "dwell_s": dwell_s,
                    "lambda_history": coupling,
                    "force_difference_n": difference,
                    "repeats_per_path_for_target": repeats,
                }
            )

    finite_rows = [row for row in rows if row["repeats_per_path_for_target"]]
    best = min(
        finite_rows,
        key=lambda row: row["repeats_per_path_for_target"],
    )
    return {
        "noise_sigma_n": noise_sigma_n,
        "target_sigma": target_sigma,
        "warning": "Sensitivity ansatz only; nuisance hysteresis is not modeled.",
        "best_case": best,
        "rows": rows,
    }


def ac_phase_frequency_grid(
    geometry: Equation11Geometry | None = None,
) -> dict:
    """Sweep phase and frequency through patent equations (12)-(15)."""

    geometry = geometry or calibrated_reference_geometry()
    frequencies_hz = (100.0, 1_000.0, 10_000.0)
    phases_deg = (0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0)
    rows = []
    for frequency in frequencies_hz:
        for phase_deg in phases_deg:
            phase_rad = math.radians(phase_deg)
            exact = equation_13_cycle_average(
                geometry,
                PATENT_REFERENCE_VOLTAGE_V,
                frequency,
                phase_rad,
                samples=5_001,
            )
            narrative = patent_narrative_cycle_average(
                geometry, PATENT_REFERENCE_VOLTAGE_V, phase_rad
            )
            rows.append(
                {
                    "frequency_hz": frequency,
                    "phase_deg": phase_deg,
                    "exact_average_n": exact,
                    "patent_narrative_average_n": narrative,
                    "difference_n": exact - narrative,
                }
            )

    per_phase_spread = {}
    for phase_deg in phases_deg:
        values = [
            row["exact_average_n"]
            for row in rows
            if row["phase_deg"] == phase_deg
        ]
        per_phase_spread[str(int(phase_deg))] = max(values) - min(values)

    shifts = {
        str(int(frequency)): time_translation_shift(
            geometry, PATENT_REFERENCE_VOLTAGE_V, frequency
        )
        for frequency in frequencies_hz
    }
    return {
        "rows": rows,
        "exact_frequency_spread_by_phase_n": per_phase_spread,
        "time_translation_shifts": shifts,
    }


def run_next_suite() -> dict:
    """Execute all phase-2 Exodus/DET discriminator runs."""

    geometry = calibrated_reference_geometry()
    return {
        "status": "phase-2 research sandbox; no new DET8 force prediction",
        "reference_equation_11_force_n": patent_equation_11_force(
            geometry, PATENT_REFERENCE_VOLTAGE_V
        ),
        "image_charge_boundary": image_charge_boundary_sweep(),
        "boundary_model_selection": noisy_boundary_model_selection(),
        "momentum_inventory": noisy_momentum_inventory(),
        "history_detectability": history_detectability_grid(geometry),
        "ac_phase_frequency": ac_phase_frequency_grid(geometry),
    }


def main() -> None:
    print(json.dumps(run_next_suite(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
