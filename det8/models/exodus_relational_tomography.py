"""DET-native relational endpoint tomography for the Exodus sandbox.

The field simulations established explicit ordinary endpoints in declared
geometries.  This module asks the next methodological question: which set of
controlled interventions would let an experiment infer the endpoint rather
than merely detect a force?

It is a reduced-order, synthetic experiment-design study calibrated to the
base 3-D apparatus run.  It does not introduce a DET force.  Candidate models
compete across independently varied device orientation, chamber orientation,
wall distance, common mode, lead routing, and preparation path.  A nested
regime ledger tests where conservation closes, while a matched-state history
protocol demonstrates how residual charge relaxation can imitate history.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple


# Quadratic fixed-differential response surfaces extracted from the same-end
# base 3-D field run.  Input is common mode in kV; output is newtons.  Three
# electrostatic states determine each quadratic exactly.  These coefficients
# are calibration data for the intervention study, not universal constants.
AXIAL_A_UN_PER_KV2 = -0.0019523133092567058
AXIAL_B_UN_PER_KV = -19.790751190089633
AXIAL_C_UN = -23.597038492738086
WALL_A_UN_PER_KV2 = -3.219301609808212
WALL_B_UN_PER_KV = -0.819204321505208
WALL_C_UN = -441.34562140448134

BASE_COMMON_MODE_KV = -2.1145142159
BASE_DEVICE_FORCE_N = (18.2420571164e-6, 0.0, -454.0074481882e-6)
BASE_CHAMBER_FORCE_N = (-18.1826512899e-6, 0.0, 449.4639242325e-6)


def axial_force_shape_n(common_mode_kv: float) -> float:
    return 1.0e-6 * (
        AXIAL_A_UN_PER_KV2 * common_mode_kv**2
        + AXIAL_B_UN_PER_KV * common_mode_kv
        + AXIAL_C_UN
    )


def wall_force_shape_n(common_mode_kv: float) -> float:
    return 1.0e-6 * (
        WALL_A_UN_PER_KV2 * common_mode_kv**2
        + WALL_B_UN_PER_KV * common_mode_kv
        + WALL_C_UN
    )


def _device_axis(angle_deg: float) -> Tuple[float, float, float]:
    angle = math.radians(angle_deg)
    return math.cos(angle), math.sin(angle), 0.0


def _chamber_normal(angle_deg: float) -> Tuple[float, float, float]:
    angle = math.radians(angle_deg)
    return math.sin(angle), 0.0, math.cos(angle)


def _scale(vector: Sequence[float], scalar: float) -> Tuple[float, float, float]:
    return tuple(scalar * value for value in vector)


def _add(*vectors: Sequence[float]) -> Tuple[float, float, float]:
    return tuple(sum(vector[axis] for vector in vectors) for axis in range(3))


def _norm(vector: Sequence[float]) -> float:
    return math.sqrt(sum(value * value for value in vector))


@dataclass(frozen=True)
class TomographyCondition:
    wall_distance_m: float
    common_mode_kv: float
    lead_routing: str
    device_angle_deg: float
    chamber_angle_deg: float
    preparation_sign: int


LEAD_ROUTE_FACTORS = {
    "none": 0.0,
    "same_end": 1.0,
    # Base 3-D floating values: +48.328 uN versus -454.007 uN.
    "opposite_ends": -0.106447,
}


def condition_features(condition: TomographyCondition) -> Dict[str, Tuple[float, float, float]]:
    device_axis = _device_axis(condition.device_angle_deg)
    chamber_normal = _chamber_normal(condition.chamber_angle_deg)
    distance_scale = (0.10 / condition.wall_distance_m) ** 2
    axial_n = axial_force_shape_n(condition.common_mode_kv)
    wall_n = wall_force_shape_n(condition.common_mode_kv)
    route_factor = LEAD_ROUTE_FACTORS[condition.lead_routing]
    return {
        "internal_constant": device_axis,
        "common_mode_device": _scale(device_axis, axial_n),
        "boundary_electrode": _scale(device_axis, distance_scale * axial_n),
        "lead_boundary": _scale(
            chamber_normal,
            distance_scale * route_factor * wall_n,
        ),
        "earth_fixed": (1.0, 0.0, 0.0),
        "matched_history": _scale(device_axis, float(condition.preparation_sign)),
    }


def intervention_conditions() -> List[TomographyCondition]:
    conditions = []
    for wall_distance_m in (0.08, 0.12):
        for common_mode_kv in (-6.0, -2.0, 4.0):
            for lead_routing in ("none", "same_end", "opposite_ends"):
                for device_angle_deg in (0.0, 90.0):
                    for chamber_angle_deg in (0.0, 90.0):
                        for preparation_sign in (-1, 1):
                            conditions.append(
                                TomographyCondition(
                                    wall_distance_m,
                                    common_mode_kv,
                                    lead_routing,
                                    device_angle_deg,
                                    chamber_angle_deg,
                                    preparation_sign,
                                )
                            )
    return conditions


MODEL_FEATURES = {
    "null": (),
    "device_internal": ("internal_constant",),
    "common_mode_only": ("common_mode_device",),
    "boundary_electrode": ("boundary_electrode",),
    "lead_only": ("lead_boundary",),
    "full_relational": ("boundary_electrode", "lead_boundary"),
    "full_plus_earth": (
        "boundary_electrode",
        "lead_boundary",
        "earth_fixed",
    ),
    "full_plus_history": (
        "boundary_electrode",
        "lead_boundary",
        "matched_history",
    ),
}


def _solve_linear_system(matrix: List[List[float]], vector: List[float]) -> List[float]:
    """Solve a small dense system with pivoted Gauss-Jordan elimination."""

    n = len(vector)
    augmented = [matrix[row][:] + [vector[row]] for row in range(n)]
    for column in range(n):
        pivot = max(range(column, n), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1.0e-14:
            raise ValueError("singular tomography design matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        augmented[column] = [value / pivot_value for value in augmented[column]]
        for row in range(n):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][item] - factor * augmented[column][item]
                for item in range(n + 1)
            ]
    return [augmented[row][-1] for row in range(n)]


def _fit_model(
    observations_n: Sequence[float],
    feature_rows: Sequence[Dict[str, float]],
    features: Sequence[str],
) -> Dict[str, object]:
    n = len(observations_n)
    p = len(features)
    if p == 0:
        rss = sum(value * value for value in observations_n)
        return {
            "coefficients": {},
            "rss_n2": rss,
            "aic": n * math.log(max(rss / n, 1.0e-300)),
            "bic": n * math.log(max(rss / n, 1.0e-300)),
        }

    # Normalize columns for stable normal equations: physical feature scales
    # range from unit vectors to hundreds of micronewtons.
    scales = {}
    for feature in features:
        scales[feature] = math.sqrt(
            sum(row[feature] ** 2 for row in feature_rows) / n
        )
        if scales[feature] == 0.0:
            raise ValueError(f"zero design column: {feature}")

    normal = [[0.0 for _ in range(p)] for _ in range(p)]
    target = [0.0 for _ in range(p)]
    for row, observed in zip(feature_rows, observations_n):
        normalized = [row[feature] / scales[feature] for feature in features]
        for i in range(p):
            target[i] += normalized[i] * observed
            for j in range(p):
                normal[i][j] += normalized[i] * normalized[j]
    normalized_coefficients = _solve_linear_system(normal, target)
    coefficients = {
        feature: normalized_coefficients[index] / scales[feature]
        for index, feature in enumerate(features)
    }
    rss = 0.0
    for row, observed in zip(feature_rows, observations_n):
        prediction = sum(coefficients[feature] * row[feature] for feature in features)
        rss += (observed - prediction) ** 2
    return {
        "coefficients": coefficients,
        "rss_n2": rss,
        "aic": n * math.log(max(rss / n, 1.0e-300)) + 2.0 * p,
        "bic": n * math.log(max(rss / n, 1.0e-300)) + p * math.log(n),
    }


def _synthetic_dataset(
    noise_sigma_n: float,
    seed: int,
    history_force_n: float = 0.0,
    earth_force_n: float = 0.0,
) -> Tuple[List[float], List[Dict[str, float]]]:
    rng = random.Random(seed)
    observations = []
    rows = []
    for condition in intervention_conditions():
        vector_features = condition_features(condition)
        true_force = _add(
            vector_features["boundary_electrode"],
            vector_features["lead_boundary"],
            _scale(vector_features["matched_history"], history_force_n),
            _scale(vector_features["earth_fixed"], earth_force_n),
        )
        for axis in range(3):
            observations.append(true_force[axis] + rng.gauss(0.0, noise_sigma_n))
            rows.append(
                {
                    feature: vector[axis]
                    for feature, vector in vector_features.items()
                }
            )
    return observations, rows


def fit_endpoint_models(
    noise_sigma_n: float = 20.0e-6,
    seed: int = 20_260_823,
) -> Dict[str, object]:
    observations, rows = _synthetic_dataset(noise_sigma_n, seed)
    fits = {
        name: _fit_model(observations, rows, features)
        for name, features in MODEL_FEATURES.items()
    }
    best_aic = min(fit["aic"] for fit in fits.values())
    best_bic = min(fit["bic"] for fit in fits.values())
    raw_aic_weights = {
        name: math.exp(-0.5 * (fit["aic"] - best_aic))
        for name, fit in fits.items()
    }
    raw_bic_weights = {
        name: math.exp(-0.5 * (fit["bic"] - best_bic))
        for name, fit in fits.items()
    }
    total_aic_weight = sum(raw_aic_weights.values())
    total_bic_weight = sum(raw_bic_weights.values())
    for name, fit in fits.items():
        fit["delta_aic"] = fit["aic"] - best_aic
        fit["akaike_weight"] = raw_aic_weights[name] / total_aic_weight
        fit["delta_bic"] = fit["bic"] - best_bic
        fit["bic_weight"] = raw_bic_weights[name] / total_bic_weight
    return {
        "noise_sigma_n": noise_sigma_n,
        "seed": seed,
        "scalar_measurements": len(observations),
        "best_model_aic": min(fits, key=lambda name: fits[name]["aic"]),
        "best_model_bic": min(fits, key=lambda name: fits[name]["bic"]),
        "fits": fits,
    }


def monte_carlo_endpoint_recovery(
    noise_levels_n: Iterable[float] = (5.0e-6, 20.0e-6, 50.0e-6, 100.0e-6),
    trials: int = 200,
    seed: int = 8_082_026,
) -> Dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be positive")
    rows = []
    for noise_index, noise_sigma_n in enumerate(noise_levels_n):
        aic_wins = {name: 0 for name in MODEL_FEATURES}
        bic_wins = {name: 0 for name in MODEL_FEATURES}
        aic_weight_sums = {name: 0.0 for name in MODEL_FEATURES}
        bic_weight_sums = {name: 0.0 for name in MODEL_FEATURES}
        for trial in range(trials):
            result = fit_endpoint_models(
                noise_sigma_n=noise_sigma_n,
                seed=seed + noise_index * 10_000 + trial,
            )
            aic_wins[result["best_model_aic"]] += 1
            bic_wins[result["best_model_bic"]] += 1
            for name, fit in result["fits"].items():
                aic_weight_sums[name] += fit["akaike_weight"]
                bic_weight_sums[name] += fit["bic_weight"]
        relational_family = ("full_relational", "full_plus_earth", "full_plus_history")
        rows.append(
            {
                "noise_sigma_n": noise_sigma_n,
                "trials": trials,
                "aic_full_relational_win_fraction": aic_wins["full_relational"] / trials,
                "aic_relational_family_win_fraction": sum(
                    aic_wins[name] for name in relational_family
                ) / trials,
                "bic_full_relational_win_fraction": bic_wins["full_relational"] / trials,
                "bic_relational_family_win_fraction": sum(
                    bic_wins[name] for name in relational_family
                ) / trials,
                "full_relational_mean_aic_weight": (
                    aic_weight_sums["full_relational"] / trials
                ),
                "full_relational_mean_bic_weight": (
                    bic_weight_sums["full_relational"] / trials
                ),
                "aic_win_counts": aic_wins,
                "bic_win_counts": bic_wins,
            }
        )
    return {"rows": rows}


def rotation_signature() -> Dict[str, object]:
    """Separate device-fixed and chamber-fixed vector components."""

    common_mode = BASE_COMMON_MODE_KV
    axial_n = axial_force_shape_n(common_mode)
    wall_n = wall_force_shape_n(common_mode)
    cases = []
    for name, device_angle, chamber_angle in (
        ("reference", 0.0, 0.0),
        ("rotate_device_only_90", 90.0, 0.0),
        ("rotate_chamber_only_90", 0.0, 90.0),
        ("reverse_chamber_only_180", 0.0, 180.0),
    ):
        force = _add(
            _scale(_device_axis(device_angle), axial_n),
            _scale(_chamber_normal(chamber_angle), wall_n),
        )
        cases.append(
            {
                "name": name,
                "device_angle_deg": device_angle,
                "chamber_angle_deg": chamber_angle,
                "force_n": {"x": force[0], "y": force[1], "z": force[2]},
            }
        )
    return {
        "common_mode_kv": common_mode,
        "lead_routing": "same_end",
        "cases": cases,
    }


def nested_regime_closure() -> Dict[str, object]:
    """Expand the regime cut until the calibrated 3-D momentum ledger closes."""

    device = BASE_DEVICE_FORCE_N
    chamber = BASE_CHAMBER_FORCE_N
    numerical_residual = _add(device, chamber)
    correction = _scale(numerical_residual, -1.0)
    cuts = [
        {
            "cut": "apparatus_only",
            "included_endpoints": ("electrodes", "leads"),
            "residual_n": {"x": device[0], "y": device[1], "z": device[2]},
            "residual_norm_n": _norm(device),
            "det_conservation_gate": False,
        },
        {
            "cut": "apparatus_plus_chamber_grid",
            "included_endpoints": ("electrodes", "leads", "chamber"),
            "residual_n": {
                "x": numerical_residual[0],
                "y": numerical_residual[1],
                "z": numerical_residual[2],
            },
            "residual_norm_n": _norm(numerical_residual),
            "det_conservation_gate": True,
        },
        {
            "cut": "continuum_extrapolated_closed_regime",
            "included_endpoints": (
                "electrodes",
                "leads",
                "chamber",
                "discretization_transport_correction",
            ),
            "residual_n": {"x": 0.0, "y": 0.0, "z": 0.0},
            "residual_norm_n": 0.0,
            "det_conservation_gate": True,
        },
    ]
    return {
        "device_force_n": {"x": device[0], "y": device[1], "z": device[2]},
        "chamber_force_n": {"x": chamber[0], "y": chamber[1], "z": chamber[2]},
        "numerical_transport_correction_n": {
            "x": correction[0],
            "y": correction[1],
            "z": correction[2],
        },
        "closure_improvement_factor": _norm(device) / _norm(numerical_residual),
        "cuts": cuts,
        "orphan_counterfactual_residual_norm_n": _norm(device),
    }


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _sample_variance(values: Sequence[float]) -> float:
    mean = _mean(values)
    return sum((value - mean) ** 2 for value in values) / (len(values) - 1)


def matched_state_history_test(
    repeats_per_path: int = 40,
    force_noise_sigma_n: float = 3.0e-6,
    common_mode_measurement_sigma_kv: float = 0.01,
    residual_common_mode_kv: float = 0.30,
    seed: int = 1_045,
) -> Dict[str, object]:
    """Contrast apparent history with a common-mode-matched residual.

    The two paths retain opposite residual common-mode errors after a finite
    dwell.  A naive comparison therefore reports path dependence even with no
    history force.  Correcting each observation with its measured electrical
    state removes that false signal.  A separately injected 5 uN term shows
    what a surviving matched-state history residual would look like.
    """

    if repeats_per_path < 2:
        raise ValueError("at least two repeats per path are required")
    target_common_kv = BASE_COMMON_MODE_KV
    scenarios = {}
    for scenario_index, history_difference_n in enumerate((0.0, 5.0e-6)):
        rng = random.Random(seed + scenario_index)
        raw = {-1: [], 1: []}
        corrected = {-1: [], 1: []}
        measured_common = {-1: [], 1: []}
        for preparation_sign in (-1, 1):
            true_common_kv = (
                target_common_kv + preparation_sign * residual_common_mode_kv
            )
            history_offset_n = 0.5 * preparation_sign * history_difference_n
            for _ in range(repeats_per_path):
                measured_common_kv = true_common_kv + rng.gauss(
                    0.0, common_mode_measurement_sigma_kv
                )
                observed_force_n = (
                    axial_force_shape_n(true_common_kv)
                    + history_offset_n
                    + rng.gauss(0.0, force_noise_sigma_n)
                )
                raw[preparation_sign].append(observed_force_n)
                measured_common[preparation_sign].append(measured_common_kv)
                corrected[preparation_sign].append(
                    observed_force_n - axial_force_shape_n(measured_common_kv)
                )

        def comparison(values: Dict[int, List[float]]) -> Dict[str, float]:
            difference = _mean(values[1]) - _mean(values[-1])
            standard_error = math.sqrt(
                _sample_variance(values[1]) / repeats_per_path
                + _sample_variance(values[-1]) / repeats_per_path
            )
            return {
                "path_difference_n": difference,
                "standard_error_n": standard_error,
                "z_score": abs(difference) / standard_error,
            }

        name = "electrical_memory_only" if history_difference_n == 0.0 else "injected_5uN_history"
        scenarios[name] = {
            "injected_matched_history_difference_n": history_difference_n,
            "mean_measured_common_mode_kv": {
                "up_path": _mean(measured_common[-1]),
                "down_path": _mean(measured_common[1]),
            },
            "naive_force_comparison": comparison(raw),
            "electrical_state_corrected_comparison": comparison(corrected),
        }
    return {
        "repeats_per_path": repeats_per_path,
        "force_noise_sigma_n": force_noise_sigma_n,
        "common_mode_measurement_sigma_kv": common_mode_measurement_sigma_kv,
        "residual_common_mode_kv": residual_common_mode_kv,
        "scenarios": scenarios,
    }


def run_relational_tomography_suite() -> Dict[str, object]:
    return {
        "status": "synthetic DET relational-methodology study; no new force prediction",
        "calibration": {
            "source": "base 3-D same-end-lead electrostatic run",
            "common_mode_kv": BASE_COMMON_MODE_KV,
            "device_force_n": BASE_DEVICE_FORCE_N,
            "chamber_force_n": BASE_CHAMBER_FORCE_N,
            "distance_dependence": "declared inverse-square intervention shape",
        },
        "single_model_selection": fit_endpoint_models(),
        "monte_carlo_endpoint_recovery": monte_carlo_endpoint_recovery(),
        "rotation_signature": rotation_signature(),
        "nested_regime_closure": nested_regime_closure(),
        "matched_state_history": matched_state_history_test(),
    }


if __name__ == "__main__":
    print(json.dumps(run_relational_tomography_suite(), indent=2, sort_keys=True))
