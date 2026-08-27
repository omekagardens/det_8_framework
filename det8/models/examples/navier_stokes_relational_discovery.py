"""DET/RET discovery diagnostics for bounded Navier--Stokes trajectories.

This layer observes the Fourier solver in
``navier_stokes_near_singularity`` without changing its frozen phase-one
result schema.  It adds four deliberately separated products:

* Ladyzhenskaya--Prodi--Serrin (LPS) velocity-norm diagnostics;
* spatial records for intense-vorticity components and temporal associations;
* a train/held-out-segment comparison of predeclared growth-law families; and
* provenance-protected RET evidence bundles.

Every output remains a bounded floating-point diagnostic.  Component bonds
are temporal associations, not material-vortex identity or physical causal
edges.  A within-trajectory held-out segment is not an independent
replication, and no output authorizes a singularity or regularity claim.
"""

from __future__ import annotations

import math
import hashlib
from dataclasses import asdict, replace
from pathlib import Path
from typing import Mapping, Optional, Sequence

from det8.models.event_graph import CausalGraph, Event
from det8.models.relational_evidence import (
    EvidenceAction,
    EvidenceLedger,
    EvidenceRecord,
    StudentT,
    evidence_payload_digest,
)
from det8.models.examples.navier_stokes_near_singularity import (
    DOMAIN_LENGTH,
    PROOF_WARNING,
    SpectralNavierStokes3D,
    SpectralRunConfig,
    compare_resolution_pair,
    compare_timestep_pair,
    prepare_navier_stokes_protocol,
)


DISCOVERY_SCHEMA_VERSION = "navier-stokes-det-ret-discovery-v1"
INTENSE_SET_FRACTIONS = (0.01, 0.001)
PRIMARY_COMPONENT_FRACTION = 0.01
MAX_DISPLAYED_COMPONENTS = 12
GROWTH_TRAINING_FRACTION = 0.70
GROWTH_STUDENT_T_DF = 5.0

DISCOVERY_WARNING = (
    "DET component bonds are grid-based temporal associations, not proof of "
    "material vortex identity, reconnection, or dynamical causation. RET "
    "scores use a temporally dependent development holdout and are neither "
    "an independent replication nor a Navier--Stokes singularity test."
)


# Checked against arXiv v1 on 2026-08-26.  The unavailable-data fields are a
# required provenance barrier: published scalar settings are not enough to
# reconstruct or claim reproduction of an optimized initial condition.
LATEST_LPS_REFERENCE = {
    "checked_on": "2026-08-26",
    "arxiv_id": "2604.13338v1",
    "submitted_on": "2026-04-14",
    "title": (
        "The Ladyzhenskaya-Prodi-Serrin Conditions and the Search for "
        "Extreme Behavior in 3D Navier-Stokes Flows"
    ),
    "authors": ("Elkin Ramirez", "Bartosz Protas"),
    "url": "https://arxiv.org/abs/2604.13338",
    "published_domain": "unit torus R^3/Z^3",
    "published_viscosity": 1.0,
    "published_q_values": (3, 4, 5, 9),
    "lps_relation": "2/p + 3/q = 1 for q > 3",
    "q9": {
        "p": 3.0,
        "sobolev_proxy_s": 7.0 / 6.0,
        "constraint_levels_B": (500.0, 800.0, 1200.0),
        "explicit_example_B": 800.0,
        "explicit_example_final_time": 2.0e-4,
        "objective": "(1/T) * integral_0^T ||u(t)||_9^3 dt",
        "reference_norm_growth_powers": (2.5, 4.0),
        "reference_enstrophy_growth_powers": (2.0, 3.0),
    },
    "published_nominal_resolution": 256,
    "published_time_integrator": (
        "Crank-Nicolson for linear terms and third-order Runge-Kutta for "
        "nonlinear terms"
    ),
    "optimized_coefficients_publicly_downloadable": False,
    "data_availability_statement": "available upon request",
    "optimized_field_imported_here": False,
    "direct_reproduction_claim_authorized": False,
    "normalization_caution": (
        "Published B values use a unit torus and must not be copied into this "
        "[0,2*pi)^3 mean-norm code without an explicit PDE/domain rescaling."
    ),
}
LATEST_LPS_REFERENCE_SHA256 = evidence_payload_digest(LATEST_LPS_REFERENCE)


GROWTH_MODEL_PROTOCOL = {
    "schema_version": "navier-stokes-growth-model-protocol-v1",
    "response": "log fixed-2x-interpolated maximum vorticity",
    "training_fraction": GROWTH_TRAINING_FRACTION,
    "holdout": "last 30 percent of stored samples",
    "families": (
        "exponential",
        "saturating_exponential",
        "double_exponential",
        "finite_time_power",
        "M_bottom",
    ),
    "saturating_and_double_rate_grid_times_horizon": (0.25, 8.0, 32),
    "finite_time_offset_grid_times_horizon": (0.02, 8.0, 48),
    "declared_student_t_df": GROWTH_STUDENT_T_DF,
    "minimum_residual_scale": 0.01,
    "open_model_df": 3.0,
    "open_model_minimum_scale": 0.25,
    "parameter_rule": "least squares on training samples only",
    "hyperparameter_rule": "minimum training mean squared residual on fixed grid",
    "no_refit_after_holdout": True,
    "holdout_is_temporally_dependent": True,
    "independent_replication": False,
}
GROWTH_MODEL_PROTOCOL_SHA256 = evidence_payload_digest(GROWTH_MODEL_PROTOCOL)


def phase_two_scout_actions() -> tuple[SpectralRunConfig, ...]:
    """Return two fixed scouts that change one physical axis at a time."""

    common = {
        "initial_condition": "random_low_mode",
        "resolution": 40,
        "amplitude": 1.0,
        "maximum_dt": 0.00375,
        "sample_interval": 0.025,
        "seed": 20260826,
    }
    return (
        SpectralRunConfig(
            viscosity=0.007,
            final_time=0.75,
            role="phase_two_viscosity_scout",
            **common,
        ),
        SpectralRunConfig(
            viscosity=0.01,
            final_time=1.25,
            role="phase_two_horizon_scout",
            **common,
        ),
    )


def prepare_discovery_protocol(
    actions: Optional[Sequence[SpectralRunConfig]] = None,
) -> dict[str, object]:
    """Freeze actions and diagnostic/scoring rules before evolving the PDE."""

    configs = tuple(actions or phase_two_scout_actions())
    base = prepare_navier_stokes_protocol(configs)
    manifest: dict[str, object] = {
        "schema_version": DISCOVERY_SCHEMA_VERSION,
        "actions": tuple(asdict(config) for config in configs),
        "action_digests": tuple(config.digest for config in configs),
        "base_protocol_digest": base["manifest_digest"],
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "latest_lps_reference_sha256": LATEST_LPS_REFERENCE_SHA256,
        "growth_model_protocol_sha256": GROWTH_MODEL_PROTOCOL_SHA256,
        "intense_set_fractions": INTENSE_SET_FRACTIONS,
        "primary_component_fraction": PRIMARY_COMPONENT_FRACTION,
        "maximum_displayed_components_per_snapshot": MAX_DISPLAYED_COMPONENTS,
        "feature_graph_component_scope": "all selected-set components",
        "spatial_norm_convention": "volume mean: mean(|u|^q)^(1/q)",
        "optimized_reference_field_available": False,
        "historically_fresh_confirmation": False,
        "rg2_evaluation_authorized": False,
        "formal_singularity_claim": False,
        "proof_language_allowed": False,
        "warning": DISCOVERY_WARNING,
    }
    manifest["manifest_digest"] = evidence_payload_digest(manifest)
    return manifest


def _periodic_distance(left: Sequence[float], right: Sequence[float]) -> float:
    squared = 0.0
    for a, b in zip(left, right):
        delta = math.atan2(math.sin(float(a) - float(b)), math.cos(float(a) - float(b)))
        squared += delta * delta
    return math.sqrt(squared)


def _circular_centroid(
    np, coordinates, resolution: int, weights=None
) -> tuple[float, float, float]:
    result = []
    if weights is None:
        weights = np.ones(len(coordinates), dtype=float)
    weights = np.asarray(weights, dtype=float)
    weight_sum = max(float(np.sum(weights)), 1.0e-300)
    for axis in range(3):
        angles = coordinates[:, axis].astype(float) * DOMAIN_LENGTH / resolution
        sine = float(np.sum(weights * np.sin(angles)) / weight_sum)
        cosine = float(np.sum(weights * np.cos(angles)) / weight_sum)
        if abs(sine) + abs(cosine) < 1.0e-14:
            angle = float(np.mean(angles)) % DOMAIN_LENGTH
        else:
            angle = math.atan2(sine, cosine) % DOMAIN_LENGTH
        result.append(angle)
    return tuple(result)  # type: ignore[return-value]


def _component_radius(np, coordinates, centroid, resolution: int, weights=None) -> float:
    angles = coordinates.astype(float) * DOMAIN_LENGTH / resolution
    squared = np.zeros(len(coordinates), dtype=float)
    for axis in range(3):
        delta = np.arctan2(
            np.sin(angles[:, axis] - centroid[axis]),
            np.cos(angles[:, axis] - centroid[axis]),
        )
        squared += delta * delta
    if not len(coordinates):
        return 0.0
    if weights is None:
        return math.sqrt(float(np.mean(squared)))
    weights = np.asarray(weights, dtype=float)
    return math.sqrt(
        float(np.sum(weights * squared)) / max(float(np.sum(weights)), 1.0e-300)
    )


def _connected_components(
    np,
    mask,
    vorticity_magnitude,
    stretching_density,
    *,
    maximum_components: int = MAX_DISPLAYED_COMPONENTS,
) -> tuple[int, tuple[dict[str, object], ...], tuple[dict[str, object], ...]]:
    """Return periodic six-neighbor components and a compact tracked subset."""

    resolution = int(mask.shape[0])
    unvisited = set(int(value) for value in np.flatnonzero(mask))
    components = []
    total_omega_squared = max(float(np.sum(vorticity_magnitude**2)), 1.0e-300)
    while unvisited:
        start = min(unvisited)
        unvisited.remove(start)
        stack = [start]
        cells = []
        while stack:
            flat = stack.pop()
            cells.append(flat)
            i, remainder = divmod(flat, resolution * resolution)
            j, k = divmod(remainder, resolution)
            for neighbor in (
                ((i - 1) % resolution, j, k),
                ((i + 1) % resolution, j, k),
                (i, (j - 1) % resolution, k),
                (i, (j + 1) % resolution, k),
                (i, j, (k - 1) % resolution),
                (i, j, (k + 1) % resolution),
            ):
                neighbor_flat = int(np.ravel_multi_index(neighbor, mask.shape))
                if neighbor_flat in unvisited:
                    unvisited.remove(neighbor_flat)
                    stack.append(neighbor_flat)
        cell_ids = tuple(sorted(cells))
        coordinates = np.asarray(np.unravel_index(cell_ids, mask.shape)).T
        magnitudes = vorticity_magnitude.reshape(-1)[list(cell_ids)]
        stretching = stretching_density.reshape(-1)[list(cell_ids)]
        weights = magnitudes**2
        centroid = _circular_centroid(np, coordinates, resolution, weights)
        omega_squared = float(np.sum(magnitudes**2))
        summary = {
            "cell_count": len(cell_ids),
            "volume_fraction": len(cell_ids) / float(resolution**3),
            "centroid": centroid,
            "rms_periodic_radius": _component_radius(
                np, coordinates, centroid, resolution, weights
            ),
            "mean_vorticity": float(np.mean(magnitudes)),
            "maximum_vorticity": float(np.max(magnitudes)),
            "mean_vortex_stretching_density": float(np.mean(stretching)),
            "enstrophy_fraction": omega_squared / total_omega_squared,
        }
        components.append((omega_squared, cell_ids, summary))
    components.sort(key=lambda row: (-row[0], row[1][0]))
    public = []
    internal = []
    for rank, (_, cell_ids, summary) in enumerate(components):
        record = {"rank": rank, **summary}
        internal.append({**record, "cell_ids": cell_ids})
        if rank < maximum_components:
            public.append(record)
    return len(components), tuple(public), tuple(internal)


def _direction_coherence(np, unit_vorticity, mask):
    values = []
    edge_count = 0
    for axis in range(3):
        paired = mask & np.roll(mask, -1, axis=axis)
        count = int(np.count_nonzero(paired))
        if not count:
            continue
        shifted = np.roll(unit_vorticity, -1, axis=axis + 1)
        dot = np.abs(np.sum(unit_vorticity * shifted, axis=0))
        values.append(float(np.sum(dot[paired])))
        edge_count += count
    if not edge_count:
        return None, 0
    return sum(values) / edge_count, edge_count


def _intense_set_record(
    np,
    fraction: float,
    speed,
    vorticity_magnitude,
    unit_vorticity,
    strain,
    stretching_density,
) -> tuple[dict[str, object], tuple[dict[str, object], ...]]:
    total_cells = int(vorticity_magnitude.size)
    if float(np.max(vorticity_magnitude)) <= 1.0e-14:
        return (
            {
                "declared_volume_fraction": float(fraction),
                "selected_cell_count": 0,
                "effectively_zero_vorticity": True,
                "threshold_vorticity": None,
                "mean_vorticity": None,
                "maximum_vorticity": None,
                "enstrophy_fraction": None,
                "velocity_l3_mass_fraction": None,
                "mean_vortex_stretching_density": None,
                "mean_normalized_vortex_stretching_rate": None,
                "positive_vortex_stretching_fraction": None,
                "mean_absolute_alignment_with_strain_eigendirections": None,
                "mean_absolute_alignment_with_most_extensional_strain": None,
                "mean_relative_extensional_eigengap": None,
                "neighbor_direction_coherence": None,
                "neighbor_pair_count": 0,
                "periodic_six_neighbor_component_count": 0,
                "displayed_components": (),
            },
            (),
        )
    selected_count = max(1, int(math.ceil(fraction * total_cells)))
    flat_magnitude = vorticity_magnitude.reshape(-1)
    order = np.argsort(-flat_magnitude, kind="stable")[:selected_count]
    mask = np.zeros(total_cells, dtype=bool)
    mask[order] = True
    mask = mask.reshape(vorticity_magnitude.shape)
    coordinates = np.asarray(np.unravel_index(order, mask.shape))
    selected_strain = strain[
        :, :, coordinates[0], coordinates[1], coordinates[2]
    ].transpose(2, 0, 1)
    eigenvalues, eigenvectors = np.linalg.eigh(selected_strain)
    most_extensional = eigenvectors[:, :, -1]
    selected_directions = unit_vorticity[
        :, coordinates[0], coordinates[1], coordinates[2]
    ].T
    alignment = np.abs(np.sum(selected_directions * most_extensional, axis=1))
    all_alignment = np.abs(
        np.einsum("ni,nij->nj", selected_directions, eigenvectors, optimize=True)
    )
    extensional_gap = eigenvalues[:, 2] - eigenvalues[:, 1]
    relative_gap = extensional_gap / np.maximum(
        np.maximum(np.abs(eigenvalues[:, 2]), np.abs(eigenvalues[:, 1])),
        1.0e-12,
    )
    nondegenerate = relative_gap > 1.0e-6
    coherence, coherence_edges = _direction_coherence(np, unit_vorticity, mask)
    component_count, components, internal = _connected_components(
        np, mask, vorticity_magnitude, stretching_density
    )
    total_enstrophy_weight = max(float(np.sum(vorticity_magnitude**2)), 1.0e-300)
    total_velocity_l3_weight = max(float(np.sum(speed**3)), 1.0e-300)
    selected_vorticity = vorticity_magnitude[mask]
    selected_stretching = stretching_density[mask]
    normalized_stretching = selected_stretching / np.maximum(
        selected_vorticity**2, 1.0e-300
    )
    record = {
        "declared_volume_fraction": float(fraction),
        "selected_cell_count": selected_count,
        "effectively_zero_vorticity": False,
        "threshold_vorticity": float(np.min(selected_vorticity)),
        "mean_vorticity": float(np.mean(selected_vorticity)),
        "maximum_vorticity": float(np.max(selected_vorticity)),
        "enstrophy_fraction": float(
            np.sum(vorticity_magnitude[mask] ** 2) / total_enstrophy_weight
        ),
        "velocity_l3_mass_fraction": float(
            np.sum(speed[mask] ** 3) / total_velocity_l3_weight
        ),
        "mean_vortex_stretching_density": float(np.mean(selected_stretching)),
        "mean_normalized_vortex_stretching_rate": float(
            np.mean(normalized_stretching)
        ),
        "positive_vortex_stretching_fraction": float(
            np.mean(selected_stretching > 0.0)
        ),
        "mean_absolute_alignment_with_strain_eigendirections": tuple(
            float(value) for value in np.mean(all_alignment, axis=0)
        ),
        "mean_absolute_alignment_with_most_extensional_strain": (
            float(np.mean(alignment[nondegenerate]))
            if bool(np.any(nondegenerate))
            else None
        ),
        "mean_relative_extensional_eigengap": float(np.mean(relative_gap)),
        "neighbor_direction_coherence": (
            float(coherence) if coherence is not None else None
        ),
        "neighbor_pair_count": coherence_edges,
        "periodic_six_neighbor_component_count": component_count,
        "displayed_components": components,
    }
    return record, internal


def _field_snapshot(solver, velocity_hat, base_sample):
    np = solver.np
    velocity = np.fft.ifftn(velocity_hat, axes=(1, 2, 3)).real
    vorticity_hat = solver.vorticity_hat(velocity_hat)
    vorticity = np.fft.ifftn(vorticity_hat, axes=(1, 2, 3)).real
    speed = np.sqrt(np.sum(velocity * velocity, axis=0))
    vorticity_magnitude = np.sqrt(np.sum(vorticity * vorticity, axis=0))
    gradient = np.empty((3, 3) + speed.shape, dtype=float)
    for component in range(3):
        for derivative in range(3):
            gradient[component, derivative] = np.fft.ifftn(
                1j * solver.wavevectors[derivative] * velocity_hat[component]
            ).real
    strain = 0.5 * (gradient + np.swapaxes(gradient, 0, 1))
    stretching_density = np.einsum(
        "i...,ij...,j...->...", vorticity, strain, vorticity, optimize=True
    )
    unit_vorticity = vorticity / np.maximum(vorticity_magnitude, 1.0e-300)[None]
    maximum_speed = float(np.max(speed))
    if maximum_speed <= 0.0:
        lq_norms = {str(q): 0.0 for q in (3, 4, 5, 9)}
    else:
        scaled_speed = speed / maximum_speed
        lq_norms = {
            str(q): maximum_speed
            * float(np.mean(scaled_speed**q) ** (1.0 / q))
            for q in (3, 4, 5, 9)
        }
    integral_lq_norms = {
        str(q): lq_norms[str(q)] * (DOMAIN_LENGTH ** (3.0 / q))
        for q in (3, 4, 5, 9)
    }
    intense_sets = {}
    internal_sets = {}
    for fraction in INTENSE_SET_FRACTIONS:
        label = "top_1_percent" if fraction == 0.01 else "top_0_1_percent"
        intense_sets[label], internal_sets[label] = _intense_set_record(
            np,
            fraction,
            speed,
            vorticity_magnitude,
            unit_vorticity,
            strain,
            stretching_density,
        )
    return (
        {
            "time": float(base_sample["time"]),
            "maximum_velocity": float(base_sample["maximum_velocity"]),
            "velocity_lq_norms": lq_norms,
            "velocity_integral_lq_norms": integral_lq_norms,
            "lps_integrands": {
                "q4_p8": lq_norms["4"] ** 8,
                "q5_p5": lq_norms["5"] ** 5,
                "q9_p3": lq_norms["9"] ** 3,
            },
            "intense_sets": intense_sets,
        },
        internal_sets,
    )


class RelationalDiagnosticsCollector:
    """Sample observer used by :class:`SpectralNavierStokes3D`."""

    def __init__(self) -> None:
        self.snapshots: list[dict[str, object]] = []
        self.primary_component_frames: list[tuple[dict[str, object], ...]] = []

    def __call__(self, solver, velocity_hat, base_sample) -> None:
        snapshot, internal_sets = _field_snapshot(solver, velocity_hat, base_sample)
        self.snapshots.append(snapshot)
        self.primary_component_frames.append(internal_sets["top_1_percent"])


def reference_scale_bridge(code_viscosity: float) -> dict[str, object]:
    """Map published unit-torus scalar scales into this solver's convention.

    With ``x = 2*pi*y``, the exact PDE scaling is
    ``u_code = nu_code/(2*pi*nu_paper) * u_paper`` and
    ``t_code = (2*pi)^2*nu_paper/nu_code * t_paper``.  This maps scalar
    norms and horizons only; it cannot reconstruct unavailable coefficients.
    """

    if not math.isfinite(code_viscosity) or code_viscosity <= 0.0:
        raise ValueError("code viscosity must be finite and positive")
    paper_viscosity = float(LATEST_LPS_REFERENCE["published_viscosity"])
    velocity_factor = code_viscosity / (DOMAIN_LENGTH * paper_viscosity)
    time_factor = DOMAIN_LENGTH**2 * paper_viscosity / code_viscosity
    q9 = LATEST_LPS_REFERENCE["q9"]
    assert isinstance(q9, Mapping)
    levels = tuple(float(value) for value in q9["constraint_levels_B"])
    return {
        "derivation": (
            "x_code=2*pi*y_paper; u_code=nu_code/(2*pi*nu_paper)*u_paper; "
            "t_code=(2*pi)^2*nu_paper/nu_code*t_paper"
        ),
        "derived_here_not_quoted_from_reference": True,
        "code_viscosity": float(code_viscosity),
        "paper_viscosity": paper_viscosity,
        "velocity_and_normalized_mean_lq_factor": velocity_factor,
        "time_factor": time_factor,
        "q9_constraint_levels_in_code_mean_norm": tuple(
            velocity_factor * value for value in levels
        ),
        "example_final_time_in_code_units": (
            time_factor * float(q9["explicit_example_final_time"])
        ),
        "coefficients_available_after_scale_change": False,
        "reproduction_claim_authorized": False,
    }


def _trapezoid(times: Sequence[float], values: Sequence[float]) -> float:
    return sum(
        0.5 * (float(left_value) + float(right_value))
        * (float(right_time) - float(left_time))
        for left_time, right_time, left_value, right_value in zip(
            times[:-1], times[1:], values[:-1], values[1:]
        )
    )


def _loglog_slope(x_values: Sequence[float], y_values: Sequence[float]):
    pairs = [
        (float(x), float(y))
        for x, y in zip(x_values, y_values)
        if float(x) > 0.0 and float(y) > 0.0
    ]
    if len(pairs) < 4:
        return None
    np = __import__("numpy")
    x = np.log(np.asarray([pair[0] for pair in pairs], dtype=float))
    y = np.log(np.asarray([pair[1] for pair in pairs], dtype=float))
    design = np.stack((np.ones_like(x), x), axis=1)
    coefficients = np.linalg.lstsq(design, y, rcond=None)[0]
    prediction = design @ coefficients
    residual = float(np.sum((y - prediction) ** 2))
    total = float(np.sum((y - float(np.mean(y))) ** 2))
    return {
        "slope": float(coefficients[1]),
        "intercept": float(coefficients[0]),
        "r_squared": 1.0 - residual / total if total > 0.0 else 1.0,
        "positive_derivative_point_count": len(pairs),
    }


def summarize_lps_diagnostics(
    snapshots: Sequence[Mapping[str, object]],
    numerical_result: Mapping[str, object],
) -> dict[str, object]:
    """Integrate LPS quantities and align them with published diagnostics."""

    if len(snapshots) < 2:
        raise ValueError("LPS summary requires at least two samples")
    times = [float(row["time"]) for row in snapshots]
    duration = times[-1] - times[0]
    if duration <= 0.0:
        raise ValueError("LPS sample times must span a positive duration")
    norms = {
        str(q): [float(row["velocity_lq_norms"][str(q)]) for row in snapshots]
        for q in (3, 4, 5, 9)
    }
    integral_norms = {
        str(q): [
            float(row["velocity_integral_lq_norms"][str(q)]) for row in snapshots
        ]
        for q in (3, 4, 5, 9)
    }
    exponents = {"4": 8.0, "5": 5.0, "9": 3.0}
    integrated = {}
    for q, exponent in exponents.items():
        mean_values = [value**exponent for value in norms[q]]
        standard_values = [value**exponent for value in integral_norms[q]]
        mean_integral = _trapezoid(times, mean_values)
        standard_integral = _trapezoid(times, standard_values)
        integrated[q] = {
            "q": int(q),
            "p": exponent,
            "normalized_mean_norm_integral": mean_integral,
            "normalized_mean_norm_time_average_phi": mean_integral / duration,
            "standard_integral_norm_integral": standard_integral,
            "standard_integral_norm_time_average_phi": standard_integral / duration,
            "maximum_normalized_mean_lq_norm": max(norms[q]),
            "terminal_normalized_mean_lq_norm": norms[q][-1],
            "maximum_standard_integral_lq_norm": max(integral_norms[q]),
            "terminal_standard_integral_lq_norm": integral_norms[q][-1],
        }
    base_samples = numerical_result["samples"]
    enstrophy = [float(row["enstrophy"]) for row in base_samples]
    minimum_index = min(range(len(enstrophy)), key=enstrophy.__getitem__)
    rebound = max(enstrophy[minimum_index:]) - enstrophy[minimum_index]

    def centered_derivative(values):
        derivative = []
        centers = []
        for index in range(1, len(values) - 1):
            dt = times[index + 1] - times[index - 1]
            if dt <= 0.0:
                continue
            centers.append(float(values[index]))
            derivative.append((float(values[index + 1]) - float(values[index - 1])) / dt)
        return centers, derivative

    q9_centers, q9_derivative = centered_derivative(norms["9"])
    enstrophy_centers, enstrophy_derivative = centered_derivative(enstrophy)
    config = numerical_result["configuration"]
    bridge = reference_scale_bridge(float(config["viscosity"]))
    return {
        "norm_convention": (
            "normalized spatial mean mean(|u|^q)^(1/q); equal to the standard "
            "integral norm only on a unit-volume domain"
        ),
        "q3_endpoint": {
            "criterion_proxy": "sampled sup_t ||u||_3",
            "sampled_supremum_normalized_mean_l3": max(norms["3"]),
            "sampled_supremum_standard_integral_l3": max(integral_norms["3"]),
            "terminal_normalized_mean_l3": norms["3"][-1],
            "terminal_standard_integral_l3": integral_norms["3"][-1],
            "terminal_standard_integral_l3_cubed_objective": (
                integral_norms["3"][-1] ** 3
            ),
        },
        "q_greater_than_3": integrated,
        "q9_phase_plane_growth_slope": _loglog_slope(q9_centers, q9_derivative),
        "q9_reference_slopes": {
            "regularity_safe_comparison": 2.5,
            "singularity_compatible_comparison": 4.0,
            "comparison_is_descriptive_not_a_proof_test": True,
        },
        "enstrophy_phase_plane_growth_slope": _loglog_slope(
            enstrophy_centers, enstrophy_derivative
        ),
        "enstrophy_reference_slopes": {
            "regularity_safe_comparison": 2.0,
            "singularity_compatible_comparison": 3.0,
            "comparison_is_descriptive_not_a_proof_test": True,
        },
        "enstrophy_rebound": {
            "minimum": enstrophy[minimum_index],
            "minimum_time": float(base_samples[minimum_index]["time"]),
            "postminimum_rebound": rebound,
            "postminimum_rebound_relative_to_initial": rebound
            / max(enstrophy[0], 1.0e-300),
        },
        "published_scalar_scale_bridge": bridge,
        "published_optimized_field_imported": False,
        "direct_published_field_reproduction": False,
    }


def build_vortex_event_graph(
    snapshots: Sequence[Mapping[str, object]],
    component_frames: Sequence[Sequence[Mapping[str, object]]],
    *,
    resolution: int,
) -> dict[str, object]:
    """Associate intense-set components across adjacent stored samples."""

    if len(snapshots) != len(component_frames):
        raise ValueError("component frames must align one-to-one with snapshots")
    if resolution < 1:
        raise ValueError("resolution must be positive")
    grid_spacing = DOMAIN_LENGTH / resolution
    nodes = []
    frame_nodes = []
    node_lookup = {}
    next_node_id = 0
    for sample_index, (snapshot, components) in enumerate(
        zip(snapshots, component_frames)
    ):
        identifiers = []
        ordered_components = sorted(
            components,
            key=lambda component: (
                int(component.get("rank", 0)),
                -float(component.get("enstrophy_fraction", 0.0)),
                min(
                    (int(value) for value in component.get("cell_ids", ())),
                    default=0,
                ),
            ),
        )
        for component in ordered_components:
            node_id = next_node_id
            next_node_id += 1
            identifiers.append(node_id)
            public_component = {
                key: value for key, value in component.items() if key != "cell_ids"
            }
            node = {
                "node_id": node_id,
                "sample_index": sample_index,
                "time": float(snapshot["time"]),
                **public_component,
            }
            nodes.append(node)
            node_lookup[node_id] = component
        frame_nodes.append(tuple(identifiers))
    bonds = []
    def dilated(cell_ids):
        expanded = set(int(value) for value in cell_ids)
        for flat in tuple(expanded):
            i, remainder = divmod(flat, resolution * resolution)
            j, k = divmod(remainder, resolution)
            for neighbor in (
                ((i - 1) % resolution, j, k),
                ((i + 1) % resolution, j, k),
                (i, (j - 1) % resolution, k),
                (i, (j + 1) % resolution, k),
                (i, j, (k - 1) % resolution),
                (i, j, (k + 1) % resolution),
            ):
                expanded.add(int(neighbor[0] * resolution * resolution + neighbor[1] * resolution + neighbor[2]))
        return expanded

    dilated_cache = {
        node_id: dilated(node_lookup[node_id].get("cell_ids", ()))
        for node_id in node_lookup
    }
    for frame_index, (left_ids, right_ids) in enumerate(
        zip(frame_nodes[:-1], frame_nodes[1:])
    ):
        delta_time = float(snapshots[frame_index + 1]["time"]) - float(
            snapshots[frame_index]["time"]
        )
        advective_allowance = max(
            float(snapshots[frame_index].get("maximum_velocity", 0.0)),
            float(snapshots[frame_index + 1].get("maximum_velocity", 0.0)),
        ) * max(delta_time, 0.0)
        for left_id in left_ids:
            left = node_lookup[left_id]
            left_cells = set(int(value) for value in left.get("cell_ids", ()))
            for right_id in right_ids:
                right = node_lookup[right_id]
                right_cells = set(int(value) for value in right.get("cell_ids", ()))
                union = left_cells | right_cells
                intersection = left_cells & right_cells
                jaccard = len(intersection) / len(union) if union else 0.0
                dilated_intersection = dilated_cache[left_id] & right_cells
                dilated_overlap = (
                    len(dilated_intersection)
                    / max(len(dilated_cache[left_id] | right_cells), 1)
                )
                distance = _periodic_distance(left["centroid"], right["centroid"])
                size_similarity = min(
                    float(left["cell_count"]), float(right["cell_count"])
                ) / max(float(left["cell_count"]), float(right["cell_count"]), 1.0)
                length_scale = max(
                    grid_spacing,
                    float(left["rms_periodic_radius"])
                    + float(right["rms_periodic_radius"]),
                )
                proximity = math.exp(-((distance / length_scale) ** 2))
                displacement_gate = (
                    advective_allowance
                    + float(left["rms_periodic_radius"])
                    + float(right["rms_periodic_radius"])
                    + 2.0 * grid_spacing
                )
                if distance > displacement_gate and not dilated_intersection:
                    continue
                strength = max(jaccard, dilated_overlap, proximity * size_similarity)
                if strength < 0.20:
                    continue
                bonds.append(
                    {
                        "from_node": left_id,
                        "to_node": right_id,
                        "strength": strength,
                        "cell_jaccard": jaccard,
                        "one_cell_dilated_overlap": dilated_overlap,
                        "periodic_centroid_distance": distance,
                        "advective_displacement_gate": displacement_gate,
                        "size_similarity": size_similarity,
                        "relation": "candidate_temporal_association",
                    }
                )
    incoming = {node["node_id"]: [] for node in nodes}
    outgoing = {node["node_id"]: [] for node in nodes}
    for bond in bonds:
        outgoing[bond["from_node"]].append(bond["to_node"])
        incoming[bond["to_node"]].append(bond["from_node"])
    events = []
    last_sample = len(frame_nodes) - 1
    for node in nodes:
        node_id = node["node_id"]
        sample_index = int(node["sample_index"])
        if sample_index > 0 and not incoming[node_id]:
            events.append({"type": "birth", "node_ids": (node_id,)})
        if len(incoming[node_id]) > 1:
            events.append(
                {"type": "merge_candidate", "node_ids": tuple(incoming[node_id]) + (node_id,)}
            )
        if len(outgoing[node_id]) > 1:
            events.append(
                {"type": "split_candidate", "node_ids": (node_id,) + tuple(outgoing[node_id])}
            )
        if sample_index < last_sample and not outgoing[node_id]:
            events.append({"type": "death", "node_ids": (node_id,)})
    counts = {
        name: sum(1 for event in events if event["type"] == name)
        for name in ("birth", "death", "merge_candidate", "split_candidate")
    }
    graph: dict[str, object] = {
        "intense_set_fraction": PRIMARY_COMPONENT_FRACTION,
        "node_semantics": "periodic six-neighbor intense-vorticity component",
        "bond_semantics": (
            "adjacent-sample spatial association from overlap, centroid "
            "proximity, and size; not material identity or causation"
        ),
        "nodes": tuple(nodes),
        "bonds": tuple(bonds),
        "candidate_events": tuple(events),
        "event_counts": counts,
        "time_direction_acyclic_by_construction": all(
            int(nodes[bond["from_node"]]["sample_index"])
            < int(nodes[bond["to_node"]]["sample_index"])
            for bond in bonds
        ),
    }
    graph["graph_digest"] = evidence_payload_digest(graph)
    return graph


def build_diagnostic_event_chain(
    numerical_result: Mapping[str, object],
    snapshots: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    """Commit predeclared chronological diagnostic events to a DET graph."""

    samples = numerical_result["samples"]
    initial_vorticity = max(float(samples[0]["maximum_vorticity"]), 1.0e-300)
    events = [
        {
            "kind": "run_start",
            "time": float(samples[0]["time"]),
            "value": initial_vorticity,
        }
    ]
    for threshold in (1.2, 2.0, 4.0):
        crossing = next(
            (
                sample
                for sample in samples
                if float(sample["maximum_vorticity"]) / initial_vorticity >= threshold
            ),
            None,
        )
        if crossing is not None:
            events.append(
                {
                    "kind": "first_vorticity_amplification_crossing",
                    "time": float(crossing["time"]),
                    "value": threshold,
                }
            )
    tail_threshold = 2.0e-3
    tail_crossing = next(
        (
            sample
            for sample in samples
            if float(sample["high_wavenumber_energy_fraction"]) > tail_threshold
        ),
        None,
    )
    if tail_crossing is not None:
        events.append(
            {
                "kind": "spectral_tail_admission_threshold_exceeded",
                "time": float(tail_crossing["time"]),
                "value": float(tail_crossing["high_wavenumber_energy_fraction"]),
            }
        )
    peak_index = max(
        range(len(samples)), key=lambda index: float(samples[index]["maximum_vorticity"])
    )
    q9_peak_index = max(
        range(len(snapshots)),
        key=lambda index: float(snapshots[index]["velocity_lq_norms"]["9"]),
    )
    events.extend(
        (
            {
                "kind": "sampled_vorticity_peak",
                "time": float(samples[peak_index]["time"]),
                "value": float(samples[peak_index]["maximum_vorticity"]),
            },
            {
                "kind": "sampled_l9_peak",
                "time": float(snapshots[q9_peak_index]["time"]),
                "value": float(snapshots[q9_peak_index]["velocity_lq_norms"]["9"]),
            },
            {
                "kind": "run_end",
                "time": float(samples[-1]["time"]),
                "value": float(samples[-1]["maximum_vorticity"]),
            },
        )
    )
    priority = {
        "run_start": 0,
        "first_vorticity_amplification_crossing": 1,
        "spectral_tail_admission_threshold_exceeded": 2,
        "sampled_vorticity_peak": 3,
        "sampled_l9_peak": 4,
        "run_end": 5,
    }
    events.sort(key=lambda row: (float(row["time"]), priority[row["kind"]]))
    causal = CausalGraph()
    for event_id, _ in enumerate(events):
        causal.add_event(Event(event_id, ()))
    for event_id in range(len(events) - 1):
        causal.add_edge(event_id, event_id + 1)
    records = tuple({"event_id": index, **event} for index, event in enumerate(events))
    chain: dict[str, object] = {
        "events": records,
        "direct_edges": tuple((index, index + 1) for index in range(len(events) - 1)),
        "topological_order": tuple(causal.topological_order()),
        "is_acyclic": causal.is_acyclic(),
        "edge_semantics": "chronological committed-record order, not physical causation",
    }
    chain["chain_digest"] = evidence_payload_digest(chain)
    return chain


def _geometric_grid(lower: float, upper: float, count: int) -> tuple[float, ...]:
    if lower <= 0.0 or upper <= lower or count < 2:
        raise ValueError("invalid geometric grid")
    ratio = (upper / lower) ** (1.0 / (count - 1))
    return tuple(lower * ratio**index for index in range(count))


def _linear_growth_fit(
    feature: Sequence[float],
    response: Sequence[float],
    *,
    nonnegative_coefficient: bool = True,
) -> tuple[float, float, tuple[float, ...], float]:
    if len(feature) != len(response) or not feature:
        raise ValueError("growth feature and response must have equal nonzero length")
    mean_x = sum(float(value) for value in feature) / len(feature)
    mean_y = sum(float(value) for value in response) / len(response)
    variance = sum((float(value) - mean_x) ** 2 for value in feature)
    if variance <= 1.0e-24:
        coefficient = 0.0
    else:
        coefficient = sum(
            (float(x) - mean_x) * (float(y) - mean_y)
            for x, y in zip(feature, response)
        ) / variance
    if nonnegative_coefficient:
        coefficient = max(0.0, coefficient)
    intercept = mean_y - coefficient * mean_x
    prediction = tuple(intercept + coefficient * float(value) for value in feature)
    mse = sum(
        (float(actual) - predicted) ** 2
        for actual, predicted in zip(response, prediction)
    ) / len(response)
    return intercept, coefficient, prediction, mse


def _fit_growth_candidates(
    times: Sequence[float], response: Sequence[float], train_count: int
) -> tuple[dict[str, object], ...]:
    centered = tuple(float(value) - float(times[0]) for value in times)
    training_response = tuple(float(value) for value in response[:train_count])
    horizon = centered[-1]
    if horizon <= 0.0:
        raise ValueError("growth horizon must be positive")

    def fit_one(name, feature, parameters):
        intercept, coefficient, training_prediction, mse = _linear_growth_fit(
            feature[:train_count], training_response
        )
        prediction = tuple(intercept + coefficient * float(value) for value in feature)
        return {
            "name": name,
            "parameters": {
                "intercept": intercept,
                "growth_coefficient": coefficient,
                **parameters,
            },
            "prediction": prediction,
            "training_prediction": training_prediction,
            "training_mse": mse,
        }

    candidates = [fit_one("exponential", centered, {})]
    dimensionless_rates = _geometric_grid(0.25, 8.0, 32)
    for name in ("saturating_exponential", "double_exponential"):
        best = None
        for dimensionless_rate in dimensionless_rates:
            rate = dimensionless_rate / horizon
            if name == "saturating_exponential":
                feature = tuple(1.0 - math.exp(-rate * time) for time in centered)
            else:
                feature = tuple(math.expm1(rate * time) for time in centered)
            fitted = fit_one(
                name,
                feature,
                {
                    "rate": rate,
                    "dimensionless_rate_times_horizon": dimensionless_rate,
                },
            )
            key = (float(fitted["training_mse"]), dimensionless_rate)
            if best is None or key < best[0]:
                best = (key, fitted)
        assert best is not None
        candidates.append(best[1])
    best_power = None
    for relative_offset in _geometric_grid(0.02, 8.0, 48):
        singular_time = centered[-1] + relative_offset * horizon
        feature = tuple(
            math.log(singular_time / (singular_time - time)) for time in centered
        )
        fitted = fit_one(
            "finite_time_power",
            feature,
            {
                "fitted_singular_time_relative_to_initial": singular_time,
                "singular_time_offset_beyond_declared_horizon": (
                    singular_time - centered[-1]
                ),
                "vorticity_power_exponent_gamma": None,
            },
        )
        fitted["parameters"]["vorticity_power_exponent_gamma"] = fitted[
            "parameters"
        ]["growth_coefficient"]
        key = (float(fitted["training_mse"]), relative_offset)
        if best_power is None or key < best_power[0]:
            best_power = (key, fitted)
    assert best_power is not None
    candidates.append(best_power[1])
    return tuple(candidates)


def compare_growth_models(
    times: Sequence[float],
    vorticity_values: Sequence[float],
    *,
    training_fraction: float = GROWTH_TRAINING_FRACTION,
) -> dict[str, object]:
    """Fit on an early segment and score fixed predictions on the final segment."""

    if len(times) != len(vorticity_values) or len(times) < 12:
        raise ValueError("growth scoring requires at least twelve aligned samples")
    if not 0.5 <= training_fraction <= 0.8:
        raise ValueError("training fraction must lie in [0.5, 0.8]")
    clean_times = tuple(float(value) for value in times)
    clean_values = tuple(float(value) for value in vorticity_values)
    if any(not math.isfinite(value) for value in clean_times + clean_values):
        raise ValueError("growth series must be finite")
    if any(value <= 0.0 for value in clean_values):
        raise ValueError("vorticity values must be positive")
    if any(right <= left for left, right in zip(clean_times[:-1], clean_times[1:])):
        raise ValueError("growth sample times must be strictly increasing")
    train_count = max(8, min(len(clean_times) - 4, int(len(clean_times) * training_fraction)))
    response = tuple(math.log(value) for value in clean_values)
    fitted = _fit_growth_candidates(clean_times, response, train_count)
    rows = []
    for model in fitted:
        training_rmse = math.sqrt(float(model["training_mse"]))
        scale = max(0.01, training_rmse)
        predictions = model["prediction"]
        point_scores = tuple(
            StudentT(float(predicted), scale, GROWTH_STUDENT_T_DF).log_prob(actual)
            for predicted, actual in zip(
                predictions[train_count:], response[train_count:]
            )
        )
        row = {
            "name": model["name"],
            "parameters": model["parameters"],
            "training_sample_count": train_count,
            "training_rmse_log_vorticity": training_rmse,
            "predictive_scale": scale,
            "holdout_prediction_log_vorticity": tuple(
                float(value) for value in predictions[train_count:]
            ),
            "holdout_point_log_scores": point_scores,
            "holdout_composite_log_score": sum(point_scores),
            "holdout_mean_log_score": sum(point_scores) / len(point_scores),
        }
        rows.append(row)
    minimum_declared_scale = min(float(row["predictive_scale"]) for row in rows)
    open_scale = max(0.25, 5.0 * minimum_declared_scale)
    open_center = response[train_count - 1]
    open_scores = tuple(
        StudentT(open_center, open_scale, 3.0).log_prob(actual)
        for actual in response[train_count:]
    )
    open_row = {
        "name": "M_bottom",
        "parameters": {"persistence_center": open_center},
        "training_sample_count": train_count,
        "training_rmse_log_vorticity": None,
        "predictive_scale": open_scale,
        "holdout_prediction_log_vorticity": tuple(
            open_center for _ in response[train_count:]
        ),
        "holdout_point_log_scores": open_scores,
        "holdout_composite_log_score": sum(open_scores),
        "holdout_mean_log_score": sum(open_scores) / len(open_scores),
    }
    declared = sorted(
        rows,
        key=lambda row: (-float(row["holdout_mean_log_score"]), str(row["name"])),
    )
    including_open = sorted(
        rows + [open_row],
        key=lambda row: (-float(row["holdout_mean_log_score"]), str(row["name"])),
    )
    declared_margin = (
        float(declared[0]["holdout_mean_log_score"])
        - float(declared[1]["holdout_mean_log_score"])
    )
    result: dict[str, object] = {
        "state": "WITHIN_TRAJECTORY_DEVELOPMENT_HOLDOUT",
        "protocol_sha256": GROWTH_MODEL_PROTOCOL_SHA256,
        "training_fraction": training_fraction,
        "training_sample_count": train_count,
        "holdout_sample_count": len(clean_times) - train_count,
        "training_time_stop": clean_times[train_count - 1],
        "holdout_time_start": clean_times[train_count],
        "declared_model_scores": tuple(declared),
        "open_model_score": open_row,
        "best_declared_model": declared[0]["name"],
        "best_model_including_open": including_open[0]["name"],
        "best_declared_mean_score_margin": declared_margin,
        "finite_time_power_descriptively_preferred": (
            declared[0]["name"] == "finite_time_power" and declared_margin > 0.0
        ),
        "finite_time_power_preference_is_not_singularity_evidence": True,
        "parameters_fit_on_training_only": True,
        "predictions_frozen_before_holdout_values": True,
        "pointwise_sum_is_composite_score_not_joint_likelihood": True,
        "holdout_temporally_correlated": True,
        "counts_as_independent_replication": False,
        "posterior_model_probabilities_authorized": False,
    }
    result["score_digest"] = evidence_payload_digest(result)
    return result


def run_relational_discovery(
    config: SpectralRunConfig,
    *,
    protocol: Optional[Mapping[str, object]] = None,
) -> dict[str, object]:
    """Run one trajectory with LPS, DET, and development RET diagnostics."""

    frozen_protocol = dict(protocol or prepare_discovery_protocol((config,)))
    if config.digest not in tuple(frozen_protocol["action_digests"]):
        raise ValueError("configuration is absent from the frozen discovery protocol")
    collector = RelationalDiagnosticsCollector()
    numerical_result = SpectralNavierStokes3D(config).run(observer=collector)
    snapshots = tuple(collector.snapshots)
    if len(snapshots) != int(numerical_result["sample_count"]):
        raise RuntimeError("relational observer lost alignment with numerical samples")
    numerical_times = tuple(
        float(sample["time"]) for sample in numerical_result["samples"]
    )
    snapshot_times = tuple(float(sample["time"]) for sample in snapshots)
    if numerical_times != snapshot_times:
        raise RuntimeError("relational observer sample times do not match the solver")
    lps = summarize_lps_diagnostics(snapshots, numerical_result)
    feature_graph = build_vortex_event_graph(
        snapshots,
        collector.primary_component_frames,
        resolution=config.resolution,
    )
    diagnostic_chain = build_diagnostic_event_chain(numerical_result, snapshots)
    growth = compare_growth_models(
        numerical_times,
        tuple(
            float(sample["maximum_vorticity"])
            for sample in numerical_result["samples"]
        ),
    )
    ret_action = EvidenceAction(
        name=f"ns-{config.initial_condition}-nu-{config.viscosity}-T-{config.final_time}",
        family="navier_stokes_log_peak_vorticity_amplification",
        coordinate=None,
        metadata={
            "configuration_digest": config.digest,
            "protocol_digest": frozen_protocol["manifest_digest"],
            "counts_as_replication": False,
        },
        cost=(config.resolution / 16.0) ** 4 * config.final_time,
    )
    discovery: dict[str, object] = {
        "schema_version": DISCOVERY_SCHEMA_VERSION,
        "configuration": asdict(config),
        "configuration_digest": config.digest,
        "protocol_digest": frozen_protocol["manifest_digest"],
        "numerical_result": numerical_result,
        "relational_snapshots": snapshots,
        "lps_diagnostics": lps,
        "det_layer": {
            "diagnostic_event_chain": diagnostic_chain,
            "intense_vorticity_feature_graph": feature_graph,
        },
        "ret_layer": {
            "prospective_action": {
                "name": ret_action.name,
                "family": ret_action.family,
                "coordinate": ret_action.coordinate,
                "cost": ret_action.cost,
                "metadata": dict(ret_action.metadata),
            },
            "growth_model_comparison": growth,
            "evidence_commit_state": "PROVISIONAL_PENDING_NUMERICAL_TRANSPORT",
            "ret_model_calibration_required": True,
            "posterior_model_probabilities_authorized": False,
        },
        "latest_lps_reference_sha256": LATEST_LPS_REFERENCE_SHA256,
        "optimized_reference_field_imported": False,
        "counts_as_independent_replication": False,
        "historically_fresh_confirmation": False,
        "rg2_state": "NOT_EVALUATED_NO_SOURCE_DISJOINT_REPLICATION",
        "formal_singularity_claim": False,
        "global_regularity_claim": False,
        "proof_language_allowed": False,
        "proof_warning": PROOF_WARNING,
        "discovery_warning": DISCOVERY_WARNING,
    }
    discovery["discovery_digest"] = evidence_payload_digest(discovery)
    return discovery


def _physical_bundle_key(discovery: Mapping[str, object]) -> tuple[object, ...]:
    config = discovery["configuration"]
    return (
        config["initial_condition"],
        config["viscosity"],
        config["final_time"],
        config["amplitude"],
        config["seed"],
        config["sample_interval"],
    )


def _bundle_transport_report(
    discoveries: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    numerical_results = tuple(item["numerical_result"] for item in discoveries)
    by_resolution = {}
    for result in numerical_results:
        resolution = int(result["configuration"]["resolution"])
        by_resolution.setdefault(resolution, []).append(result)
    resolution_comparisons = []
    ordered_resolutions = sorted(by_resolution)
    for lower_resolution, higher_resolution in zip(
        ordered_resolutions[:-1], ordered_resolutions[1:]
    ):
        lower_by_dt = {
            float(row["configuration"]["maximum_dt"]): row
            for row in by_resolution[lower_resolution]
        }
        higher_by_dt = {
            float(row["configuration"]["maximum_dt"]): row
            for row in by_resolution[higher_resolution]
        }
        common_timesteps = sorted(set(lower_by_dt) & set(higher_by_dt))
        if not common_timesteps:
            continue
        matched_dt = common_timesteps[0]
        resolution_comparisons.append(
            {
                "matched_maximum_dt": matched_dt,
                **compare_resolution_pair(
                lower_by_dt[matched_dt],
                higher_by_dt[matched_dt],
                ),
            }
        )
    timestep_comparisons = []
    for resolution, rows in sorted(by_resolution.items()):
        ordered = sorted(
            rows,
            key=lambda row: float(row["configuration"]["maximum_dt"]),
            reverse=True,
        )
        for coarser, finer in zip(ordered[:-1], ordered[1:]):
            if float(coarser["configuration"]["maximum_dt"]) == float(
                finer["configuration"]["maximum_dt"]
            ):
                continue
            timestep_comparisons.append(compare_timestep_pair(coarser, finer))
    resolution_passed = any(
        bool(row["transport_passed"]) for row in resolution_comparisons
    )
    timestep_passed = any(
        bool(row["transport_passed"]) for row in timestep_comparisons
    )
    return {
        "resolution_comparisons": tuple(resolution_comparisons),
        "timestep_comparisons": tuple(timestep_comparisons),
        "resolution_transport_passed": resolution_passed,
        "timestep_transport_passed": timestep_passed,
        "bundle_transport_passed": resolution_passed and timestep_passed,
        "transport_counts_as_replication": False,
    }


def ret_bundle_reports(
    discoveries: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    """Group numerical variants into physical-action evidence bundles."""

    grouped = {}
    for discovery in discoveries:
        grouped.setdefault(_physical_bundle_key(discovery), []).append(discovery)
    reports = []
    for physical_key, group in sorted(grouped.items(), key=lambda item: repr(item[0])):
        transport = _bundle_transport_report(group)
        selected = max(
            group,
            key=lambda item: (
                int(item["configuration"]["resolution"]),
                -float(item["configuration"]["maximum_dt"]),
            ),
        )
        selected_result = selected["numerical_result"]
        log_amplifications = tuple(
            math.log(max(float(item["numerical_result"]["vorticity_amplification"]), 1.0e-300))
            for item in group
        )
        selected_observation = math.log(
            max(float(selected_result["vorticity_amplification"]), 1.0e-300)
        )
        numerical_uncertainty = (
            max(abs(value - selected_observation) for value in log_amplifications)
            if len(log_amplifications) > 1
            else None
        )
        admitted = bool(
            selected_result["numerical_admission"]["numerical_gates_passed"]
        )
        complete = bool(transport["bundle_transport_passed"] and admitted)
        lineage_digest = evidence_payload_digest(physical_key)
        reports.append(
            {
                "physical_action": {
                    "initial_condition": physical_key[0],
                    "viscosity": physical_key[1],
                    "final_time": physical_key[2],
                    "amplitude": physical_key[3],
                    "seed": physical_key[4],
                    "sample_interval": physical_key[5],
                },
                "lineage_digest": lineage_digest,
                "source_run_digests": tuple(
                    str(item["numerical_result"]["run_digest"])
                    for item in sorted(
                        group, key=lambda row: row["configuration_digest"]
                    )
                ),
                "selected_discovery_digest": selected["discovery_digest"],
                "selected_configuration_digest": selected["configuration_digest"],
                "observation_log_peak_vorticity_amplification": selected_observation,
                "numerical_uncertainty_log_scale": numerical_uncertainty,
                "selected_numerically_admitted": admitted,
                "transport": transport,
                "evidence_commit_state": (
                    "TRANSPORTED_DEVELOPMENT_BUNDLE"
                    if complete
                    else "PROVISIONAL_PENDING_NUMERICAL_TRANSPORT"
                ),
                "eligible_for_ret_ledger": complete,
                "counts_as_replication": False,
                "historically_fresh": False,
            }
        )
    return tuple(reports)


def build_discovery_evidence_ledger(
    discoveries: Sequence[Mapping[str, object]],
) -> EvidenceLedger:
    """Commit only numerically transported physical-action bundles."""

    reports = ret_bundle_reports(discoveries)
    by_digest = {item["discovery_digest"]: item for item in discoveries}
    ledger = EvidenceLedger()
    for report in reports:
        if not report["eligible_for_ret_ledger"]:
            continue
        selected = by_digest[report["selected_discovery_digest"]]
        observation = float(report["observation_log_peak_vorticity_amplification"])
        source_ids = tuple(
            f"ns-run-{digest}" for digest in report["source_run_digests"]
        )
        ledger = ledger.append(
            EvidenceRecord(
                record_id=f"ns-det-ret-{str(report['lineage_digest'])[:16]}",
                source_ids=source_ids,
                action="navier_stokes_physical_action_bundle",
                coordinate=None,
                digest=evidence_payload_digest(observation),
                family="navier_stokes_log_peak_vorticity_amplification",
                scope="transported_bounded_floating_point_pde_development",
                observation=observation,
                metadata={
                    "physical_action": report["physical_action"],
                    "configuration_digest": selected["configuration_digest"],
                    "protocol_digest": selected["protocol_digest"],
                    "numerical_admission_state": selected["numerical_result"][
                        "numerical_admission"
                    ]["state"],
                    "numerical_uncertainty_log_scale": report[
                        "numerical_uncertainty_log_scale"
                    ],
                    "lps_summary_digest": evidence_payload_digest(
                        selected["lps_diagnostics"]
                    ),
                    "feature_graph_digest": selected["det_layer"][
                        "intense_vorticity_feature_graph"
                    ]["graph_digest"],
                    "growth_score_digest": selected["ret_layer"][
                        "growth_model_comparison"
                    ]["score_digest"],
                    "lineage_group": report["lineage_digest"],
                    "counts_as_replication": False,
                    "historically_fresh": False,
                    "formal_singularity_claim": False,
                    "ret_model_calibration_required": True,
                },
                joint=True,
            )
        )
    return ledger


def rank_discovery_runs(
    discoveries: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    """Rank branches for numerical refinement, not physical truth."""

    rows = []
    for discovery in discoveries:
        result = discovery["numerical_result"]
        snapshots = discovery["relational_snapshots"]
        initial_l9 = max(
            float(snapshots[0]["velocity_lq_norms"]["9"]), 1.0e-300
        )
        l9_amplification = max(
            float(snapshot["velocity_lq_norms"]["9"]) for snapshot in snapshots
        ) / initial_l9
        coherence_values = [
            snapshot["intense_sets"]["top_1_percent"][
                "neighbor_direction_coherence"
            ]
            for snapshot in snapshots
            if snapshot["intense_sets"]["top_1_percent"][
                "neighbor_direction_coherence"
            ]
            is not None
        ]
        coherence = max(float(value) for value in coherence_values) if coherence_values else 0.0
        signal = (
            math.log(max(float(result["vorticity_amplification"]), 1.0e-300))
            + 0.5 * math.log(max(l9_amplification, 1.0e-300))
            + 0.15 * coherence
        )
        admitted = bool(result["numerical_admission"]["numerical_gates_passed"])
        cost = (
            (int(discovery["configuration"]["resolution"]) / 16.0) ** 4
            * float(discovery["configuration"]["final_time"])
        )
        rows.append(
            {
                "configuration_digest": discovery["configuration_digest"],
                "discovery_digest": discovery["discovery_digest"],
                "numerically_admitted": admitted,
                "vorticity_amplification": result["vorticity_amplification"],
                "l9_norm_amplification": l9_amplification,
                "peak_intense_set_direction_coherence": coherence,
                "diagnostic_signal_proxy": signal,
                "relative_cost_proxy": cost,
                "refinement_priority": signal / max(cost, 1.0e-12),
                "ranking_is_deterministic_proxy_not_posterior": True,
            }
        )
    rows.sort(
        key=lambda row: (
            not bool(row["numerically_admitted"]),
            -float(row["diagnostic_signal_proxy"]),
            str(row["configuration_digest"]),
        )
    )
    return tuple(rows)


def phase_two_refinement_actions(
    scout_discoveries: Sequence[Mapping[str, object]],
) -> tuple[SpectralRunConfig, ...]:
    """Promote admitted signal and recover underresolved branches spatially."""

    ranked = rank_discovery_runs(scout_discoveries)
    admitted = [row for row in ranked if row["numerically_admitted"]]
    actions = []
    if admitted:
        selected_digest = admitted[0]["configuration_digest"]
        selected = next(
            item
            for item in scout_discoveries
            if item["configuration_digest"] == selected_digest
        )
        config = SpectralRunConfig(**dict(selected["configuration"]))
        actions.extend(
            (
                replace(
                    config,
                    resolution=config.resolution + 8,
                    role="phase_two_resolution_transport",
                ),
                replace(
                    config,
                    maximum_dt=config.maximum_dt / 2.0,
                    role="phase_two_timestep_transport",
                ),
            )
        )
    for row in ranked:
        if row["numerically_admitted"]:
            continue
        discovery = next(
            item
            for item in scout_discoveries
            if item["configuration_digest"] == row["configuration_digest"]
        )
        gates = discovery["numerical_result"]["numerical_admission"][
            "numerical_gates"
        ]
        if bool(gates.get("spectral_tail_occupancy", True)):
            continue
        config = SpectralRunConfig(**dict(discovery["configuration"]))
        actions.append(
            replace(
                config,
                resolution=config.resolution + 8,
                role="phase_two_underresolved_spatial_recovery",
            )
        )
    unique = {action.digest: action for action in actions}
    return tuple(unique[digest] for digest in sorted(unique))


def run_phase_two_discovery_suite(*, include_refinements: bool = False) -> dict[str, object]:
    """Run fixed scouts and optionally their outcome-selected transport bundle."""

    scouts = phase_two_scout_actions()
    scout_protocol = prepare_discovery_protocol(scouts)
    scout_results = tuple(
        run_relational_discovery(config, protocol=scout_protocol) for config in scouts
    )
    refinements = phase_two_refinement_actions(scout_results) if include_refinements else ()
    refinement_results = ()
    refinement_protocol = None
    if refinements:
        refinement_protocol = prepare_discovery_protocol(refinements)
        refinement_results = tuple(
            run_relational_discovery(config, protocol=refinement_protocol)
            for config in refinements
        )
    all_results = scout_results + refinement_results
    ledger = build_discovery_evidence_ledger(all_results)
    reports = ret_bundle_reports(all_results)
    admitted_count = sum(
        bool(result["numerical_result"]["numerical_admission"]["numerical_gates_passed"])
        for result in all_results
    )
    if ledger.records:
        state = "TRANSPORTED_DEVELOPMENT_RELATION_REQUIRES_INDEPENDENT_REPLICATION"
    elif admitted_count:
        state = "ADMITTED_SCOUT_PENDING_NUMERICAL_TRANSPORT"
    else:
        state = "NUMERICAL_MODEL_REVISION"
    suite: dict[str, object] = {
        "schema_version": DISCOVERY_SCHEMA_VERSION,
        "scientific_state": state,
        "scout_protocol_digest": scout_protocol["manifest_digest"],
        "refinement_protocol_digest": (
            refinement_protocol["manifest_digest"] if refinement_protocol else None
        ),
        "adaptive_refinement_selection_consumed_scout_outcomes": bool(refinements),
        "latest_lps_reference": LATEST_LPS_REFERENCE,
        "latest_lps_reference_sha256": LATEST_LPS_REFERENCE_SHA256,
        "results": all_results,
        "ranked_scouts": rank_discovery_runs(scout_results),
        "refinement_actions": tuple(asdict(config) for config in refinements),
        "ret_bundle_reports": reports,
        "ret_evidence_ledger": {
            "record_ids": ledger.record_ids,
            "source_ids": ledger.source_ids,
            "record_count": len(ledger.records),
            "historically_fresh": False,
            "counts_as_replication": False,
            "posterior_model_probabilities_authorized": False,
        },
        "rg2_state": "NOT_EVALUATED_NO_SOURCE_DISJOINT_REPLICATION",
        "formal_singularity_claim": False,
        "global_regularity_claim": False,
        "proof_language_allowed": False,
        "proof_warning": PROOF_WARNING,
        "discovery_warning": DISCOVERY_WARNING,
    }
    suite["suite_digest"] = evidence_payload_digest(suite)
    return suite


def compact_phase_two_summary(suite: Mapping[str, object]) -> dict[str, object]:
    """Return a JSON-sized summary of a phase-two suite."""

    runs = []
    for discovery in suite["results"]:
        result = discovery["numerical_result"]
        lps = discovery["lps_diagnostics"]
        graph = discovery["det_layer"]["intense_vorticity_feature_graph"]
        growth = discovery["ret_layer"]["growth_model_comparison"]
        q9_series = tuple(
            float(snapshot["velocity_lq_norms"]["9"])
            for snapshot in discovery["relational_snapshots"]
        )
        runs.append(
            {
                "role": discovery["configuration"]["role"],
                "resolution": discovery["configuration"]["resolution"],
                "viscosity": discovery["configuration"]["viscosity"],
                "final_time": discovery["configuration"]["final_time"],
                "maximum_dt": discovery["configuration"]["maximum_dt"],
                "state": result["numerical_admission"]["state"],
                "vorticity_amplification": result["vorticity_amplification"],
                "enstrophy_amplification": result["enstrophy_amplification"],
                "palinstrophy_amplification": result["palinstrophy_amplification"],
                "peak_high_wavenumber_energy_fraction": result["maxima"][
                    "high_wavenumber_energy_fraction"
                ],
                "q9_phi_mean_norm": lps["q_greater_than_3"]["9"][
                    "normalized_mean_norm_time_average_phi"
                ],
                "initial_normalized_mean_l9": q9_series[0],
                "final_to_initial_l9_ratio": q9_series[-1]
                / max(q9_series[0], 1.0e-300),
                "maximum_to_initial_l9_ratio": max(q9_series)
                / max(q9_series[0], 1.0e-300),
                "q9_phase_plane_growth_slope": lps["q9_phase_plane_growth_slope"],
                "feature_graph_event_counts": graph["event_counts"],
                "best_growth_model": growth["best_declared_model"],
                "best_model_including_open": growth["best_model_including_open"],
                "growth_score_margin": growth["best_declared_mean_score_margin"],
                "run_digest": result["run_digest"],
                "discovery_digest": discovery["discovery_digest"],
            }
        )
    return {
        "scientific_state": suite["scientific_state"],
        "runs": tuple(runs),
        "ranked_scouts": suite["ranked_scouts"],
        "ret_bundle_reports": suite["ret_bundle_reports"],
        "ret_evidence_ledger": suite["ret_evidence_ledger"],
        "rg2_state": suite["rg2_state"],
        "formal_singularity_claim": suite["formal_singularity_claim"],
        "proof_language_allowed": suite["proof_language_allowed"],
        "suite_digest": suite["suite_digest"],
        "discovery_warning": suite["discovery_warning"],
    }


if __name__ == "__main__":
    import json

    try:
        print(json.dumps(compact_phase_two_summary(run_phase_two_discovery_suite()), indent=2))
    except RuntimeError as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, indent=2))
