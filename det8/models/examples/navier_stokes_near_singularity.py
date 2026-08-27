"""Governed 3-D incompressible Navier--Stokes near-singularity scout.

The numerical domain is the periodic cube ``[0, 2*pi)^3``.  A rotational-form
Fourier pseudo-spectral discretization evolves

    du/dt = P(u x omega) - nu |k|^2 u,   div(u) = 0,

where ``P`` is the Leray projector and the nonlinear term is filtered with the
standard component-wise 2/3 rule.  Time integration uses adaptive-step RK4.

This is a bounded numerical search, not a regularity proof.  A large vorticity
value is never promoted by itself.  The admission gate also checks divergence,
the unforced energy identity, spectral-tail occupancy, analyticity-strip
proxies, time-window stability, and transport across resolutions.  Even a run
that clears every numerical gate is called only a numerical scaling candidate;
RG2 and proof language remain unavailable until a predictive relation is
frozen and independently tested.

NumPy is imported lazily so the rest of DET8 and its pure-Python test suite do
not acquire a mandatory numerical dependency.
"""

from __future__ import annotations

import copy
import math
import hashlib
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Mapping, Optional, Sequence

from det8.models.relational_evidence import (
    EvidenceLedger,
    EvidenceRecord,
    evidence_payload_digest,
)


SCHEMA_VERSION = "navier-stokes-near-singularity-v1"
DOMAIN_LENGTH = 2.0 * math.pi
NUMERICAL_STATES = (
    "NUMERICAL_MODEL_FAILURE",
    "UNDERRESOLVED",
    "NO_NEAR_SINGULAR_SCALING",
    "RESOLVED_TRANSIENT_AMPLIFICATION",
    "SINGLE_RUN_SCALING_TRIGGER",
)
PROOF_WARNING = (
    "A finite floating-point trajectory cannot prove finite-time blow-up or "
    "global regularity for the three-dimensional Navier--Stokes equations."
)
INTERPRETATION_WARNING = (
    "Vorticity, enstrophy, palinstrophy, BKM-style integrals, fitted blow-up "
    "times, and analyticity-strip widths are numerical diagnostics. Apparent "
    "growth that does not transport across resolution and timestep refinement "
    "is classified as numerical model failure or under-resolution."
)
LOCKED_GROWTH_MODEL_HOLDOUT_AVAILABLE = False
PRIMARY_REFERENCES = (
    {
        "role": "official problem scope",
        "title": "Existence and Smoothness of the Navier--Stokes Equation",
        "url": "https://www.claymath.org/library/monographs/MPPc.pdf",
    },
    {
        "role": "vorticity continuation criterion",
        "title": "Remarks on the breakdown of smooth solutions for the 3-D Euler equations",
        "doi": "10.1007/BF01212349",
    },
    {
        "role": "analyticity-strip diagnostic",
        "title": "Tracing complex singularities with spectral methods",
        "doi": "10.1016/0021-9991(83)90045-1",
    },
    {
        "role": "near-singular spectral numerics",
        "title": "Computing nearly singular solutions using pseudo-spectral methods",
        "doi": "10.1016/j.jcp.2007.04.014",
    },
    {
        "role": "3-D Navier--Stokes worst-case enstrophy search",
        "title": "Maximum Amplification of Enstrophy in 3D Navier-Stokes Flows",
        "url": "https://arxiv.org/abs/1909.00041",
    },
)

# Machine-readable record of the completed, consumed development ladder.  It
# is not a locked confirmation manifest and cannot authorize proof language.
PHASE_ONE_REFERENCE_FINDINGS = {
    "schema_version": "navier-stokes-phase-one-reference-v1",
    "run_date": "2026-08-26",
    "physical_action": {
        "initial_condition": "random_low_mode",
        "initial_condition_definition": (
            "seeded resolution-invariant divergence-free Fourier polynomial"
        ),
        "seed": 20260826,
        "viscosity": 0.01,
        "final_time": 0.75,
        "amplitude": 1.0,
        "maximum_dt": 0.00375,
        "sample_interval": 0.05,
    },
    "resolution_ladder": (
        {
            "resolution": 16,
            "state": "UNDERRESOLVED",
            "vorticity_amplification": 1.38236399846368,
            "enstrophy_amplification": 1.2483197080839832,
            "palinstrophy_amplification": 2.5889951615555766,
            "peak_high_wavenumber_energy_fraction": 0.08762885381460177,
            "energy_balance_relative_defect": 9.529109590289409e-08,
            "analyticity_margin_delta_kmax": 3.362141479184491,
            "run_digest": (
                "67cb6d5fe2c4c5a63b7aa2578c8db950b18da3b02d2d9f8c49abcc7b022f9a8d"
            ),
        },
        {
            "resolution": 24,
            "state": "UNDERRESOLVED",
            "vorticity_amplification": 1.6380310264317524,
            "enstrophy_amplification": 1.2747266158887869,
            "palinstrophy_amplification": 3.03526257964552,
            "peak_high_wavenumber_energy_fraction": 0.0119367141970767,
            "energy_balance_relative_defect": 1.0906707870184104e-07,
            "analyticity_margin_delta_kmax": 2.4069561129610086,
            "run_digest": (
                "3ae2d28a1f62fbfa5f98fe5fa06bfb629124c590db60afeb4c17ca585efb4fd6"
            ),
        },
        {
            "resolution": 32,
            "state": "UNDERRESOLVED",
            "vorticity_amplification": 1.763186303705291,
            "enstrophy_amplification": 1.281835733398124,
            "palinstrophy_amplification": 3.275240950259043,
            "peak_high_wavenumber_energy_fraction": 0.0021947293756642366,
            "energy_balance_relative_defect": 1.1462786309035523e-07,
            "analyticity_margin_delta_kmax": 0.7196876233184147,
            "run_digest": (
                "1bd0997d165c0252a061a6ca42e59b303a246a83cf76345ad2ada6a5d5d9e7dc"
            ),
        },
        {
            "resolution": 40,
            "state": "RESOLVED_TRANSIENT_AMPLIFICATION",
            "vorticity_amplification": 1.748110969716919,
            "enstrophy_amplification": 1.2828471935308605,
            "palinstrophy_amplification": 3.3444085512874,
            "peak_high_wavenumber_energy_fraction": 0.0002523188473400888,
            "energy_balance_relative_defect": 1.15679326784246e-07,
            "analyticity_margin_delta_kmax": 1.7789579875496258,
            "run_digest": (
                "cadfced4aa6436548a5a79d8ed6edd6c22a32ac65cbd41bdbe01c629e63070a2"
            ),
        },
        {
            "resolution": 48,
            "state": "RESOLVED_TRANSIENT_AMPLIFICATION",
            "vorticity_amplification": 1.7333735273287931,
            "enstrophy_amplification": 1.2829878643766484,
            "palinstrophy_amplification": 3.360812309946021,
            "peak_high_wavenumber_energy_fraction": 0.00013112391384556966,
            "energy_balance_relative_defect": 1.1585485126808229e-07,
            "analyticity_margin_delta_kmax": 1.8815364280462745,
            "run_digest": (
                "234f14543f33da08f58cb61ef3c7aea1a1acae1f915b3e3175c1bdc7884e934f"
            ),
        },
    ),
    "admitted_spatial_transport": {
        "lower_resolution": 40,
        "higher_resolution": 48,
        "vorticity_amplification_relative_gap": 0.008502173452964275,
        "enstrophy_amplification_relative_gap": 0.00010964316163363269,
        "palinstrophy_amplification_relative_gap": 0.004880891030443835,
        "initial_spectrum_relative_l2_gap": 9.261446204494652e-16,
        "final_spectrum_relative_l2_gap": 3.7480722105672654e-05,
        "maximum_vorticity_time_absolute_gap": 0.0,
        "all_gates_passed": True,
        "counts_as_replication": False,
    },
    "admitted_timestep_transport_at_resolution_40": {
        "coarse_maximum_dt": 0.0075,
        "fine_maximum_dt": 0.00375,
        "vorticity_amplification_relative_gap": 5.810628619730429e-10,
        "enstrophy_amplification_relative_gap": 8.925224317013805e-10,
        "palinstrophy_amplification_relative_gap": 1.7167530195031832e-08,
        "final_spectrum_relative_l2_gap": 4.981925096380622e-10,
        "all_gates_passed": True,
        "counts_as_replication": False,
    },
    "late_window_fitted_time_relative_instability": 0.2539682539682539,
    "scientific_state": (
        "RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING"
    ),
    "growth_model_holdout_available": False,
    "historically_fresh_replication": False,
    "formal_singularity_claim": False,
    "global_regularity_claim": False,
    "proof_language_allowed": False,
}
PHASE_ONE_REFERENCE_FINDINGS_SHA256 = (
    "df280ae1e3f43569acba45b31c967197f964a1398d386d8ed9297dd7e13ada8a"
)


def _numpy():
    try:
        import numpy as np
    except ModuleNotFoundError as error:
        raise RuntimeError(
            "the Navier--Stokes numerical adapter requires NumPy; install NumPy "
            "or use the bundled Codex workspace Python runtime"
        ) from error
    return np


@dataclass(frozen=True)
class SpectralRunConfig:
    """One immutable numerical action on the periodic cube."""

    initial_condition: str
    resolution: int
    viscosity: float
    final_time: float
    amplitude: float = 1.0
    cfl: float = 0.35
    maximum_dt: float = 0.01
    sample_interval: float = 0.025
    maximum_steps: int = 100_000
    seed: int = 0
    role: str = "development"

    def __post_init__(self) -> None:
        if self.initial_condition not in {
            "abc",
            "taylor_green",
            "kida_pelz",
            "vortex_tubes",
            "random_low_mode",
        }:
            raise ValueError("unknown Navier--Stokes initial-condition family")
        if self.resolution < 8 or self.resolution % 2:
            raise ValueError("spectral resolution must be an even integer at least 8")
        if self.initial_condition in {"kida_pelz", "random_low_mode"} and (
            self.resolution < 10
        ):
            raise ValueError(
                "kida_pelz and random_low_mode require resolution at least 10 "
                "so the strict 2/3 mask retains their mode-3 content"
            )
        for name in (
            "viscosity",
            "final_time",
            "amplitude",
            "cfl",
            "maximum_dt",
            "sample_interval",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be finite and positive")
        if self.maximum_steps < 1:
            raise ValueError("maximum_steps must be positive")
        if not self.role:
            raise ValueError("numerical action role is required")

    @property
    def digest(self) -> str:
        return evidence_payload_digest(asdict(self))


@dataclass(frozen=True)
class NumericalAdmissionThresholds:
    maximum_relative_energy_balance_defect: float = 5.0e-3
    maximum_relative_enstrophy_balance_defect: float = 5.0e-2
    maximum_relative_energy_increase: float = 5.0e-3
    maximum_relative_step_energy_increase: float = 5.0e-5
    maximum_divergence_l2: float = 1.0e-10
    maximum_high_wavenumber_energy_fraction: float = 2.0e-3
    minimum_analyticity_margin_for_candidate: float = 2.0
    minimum_vorticity_amplification_for_candidate: float = 4.0
    minimum_enstrophy_amplification_for_candidate: float = 2.0
    minimum_vorticity_amplification_for_transient: float = 1.20
    minimum_power_law_exponent: float = 1.0
    minimum_power_law_r_squared: float = 0.98
    maximum_relative_fitted_time_instability: float = 0.10
    maximum_resolution_amplification_gap: float = 0.15
    maximum_resolution_enstrophy_gap: float = 0.15
    maximum_resolution_palinstrophy_gap: float = 0.20
    maximum_resolution_initial_spectrum_gap: float = 0.02
    maximum_resolution_final_spectrum_gap: float = 0.15
    maximum_resolution_peak_time_gap: float = 0.075
    maximum_timestep_diagnostic_gap: float = 0.02


def _periodic_offset(np, coordinate, center: float):
    return np.arctan2(np.sin(coordinate - center), np.cos(coordinate - center))


class SpectralNavierStokes3D:
    """Dealiased rotational-form Fourier solver with numerical audits."""

    def __init__(self, config: SpectralRunConfig) -> None:
        self.config = config
        self.np = _numpy()
        np = self.np
        n = config.resolution
        modes = np.fft.fftfreq(n, d=1.0 / n)
        kx, ky, kz = np.meshgrid(modes, modes, modes, indexing="ij")
        self.wavevectors = np.stack((kx, ky, kz), axis=0)
        self.k_squared = kx * kx + ky * ky + kz * kz
        self.safe_k_squared = self.k_squared.copy()
        self.safe_k_squared[0, 0, 0] = 1.0
        self.retained_axis_wavenumber = int(math.ceil(n / 3.0) - 1)
        self.dealias_mask = (
            (np.abs(kx) < n / 3.0)
            & (np.abs(ky) < n / 3.0)
            & (np.abs(kz) < n / 3.0)
        )
        self.maximum_retained_k_squared = float(
            np.max(self.k_squared[self.dealias_mask])
        )
        coordinates = np.arange(n, dtype=float) * DOMAIN_LENGTH / n
        self.x, self.y, self.z = np.meshgrid(
            coordinates, coordinates, coordinates, indexing="ij"
        )

    def project(self, vector_hat):
        np = self.np
        projected = np.array(vector_hat, dtype=complex, copy=True)
        dot = np.sum(self.wavevectors * projected, axis=0)
        projected -= self.wavevectors * (dot / self.safe_k_squared)
        projected *= self.dealias_mask[None, :, :, :]
        projected[:, 0, 0, 0] = 0.0
        return projected

    def initial_velocity(self):
        np = self.np
        family = self.config.initial_condition
        if family == "taylor_green":
            velocity = np.stack(
                (
                    np.sin(self.x) * np.cos(self.y) * np.cos(self.z),
                    -np.cos(self.x) * np.sin(self.y) * np.cos(self.z),
                    np.zeros_like(self.x),
                ),
                axis=0,
            )
        elif family == "abc":
            velocity = np.stack(
                (
                    np.sin(self.z) + np.cos(self.y),
                    np.sin(self.x) + np.cos(self.z),
                    np.sin(self.y) + np.cos(self.x),
                ),
                axis=0,
            )
        elif family == "kida_pelz":
            velocity = np.stack(
                (
                    np.sin(self.x)
                    * (
                        np.cos(3.0 * self.y) * np.cos(self.z)
                        - np.cos(self.y) * np.cos(3.0 * self.z)
                    ),
                    np.sin(self.y)
                    * (
                        np.cos(3.0 * self.z) * np.cos(self.x)
                        - np.cos(self.z) * np.cos(3.0 * self.x)
                    ),
                    np.sin(self.z)
                    * (
                        np.cos(3.0 * self.x) * np.cos(self.y)
                        - np.cos(self.x) * np.cos(3.0 * self.y)
                    ),
                ),
                axis=0,
            )
        elif family == "vortex_tubes":
            sigma = 0.55
            dy_left = _periodic_offset(np, self.y, math.pi - 0.75)
            dy_right = _periodic_offset(np, self.y, math.pi + 0.75)
            dz = _periodic_offset(np, self.z, math.pi)
            left = np.exp(-(dy_left * dy_left + dz * dz) / (sigma * sigma))
            right = np.exp(-(dy_right * dy_right + dz * dz) / (sigma * sigma))
            modulation = 1.0 + 0.10 * np.cos(self.x)
            dpsi_dz = (
                (-2.0 * dz / (sigma * sigma)) * (left - right) * modulation
            )
            dpsi_dy = (
                (
                    (-2.0 * dy_left / (sigma * sigma)) * left
                    - (-2.0 * dy_right / (sigma * sigma)) * right
                )
                * modulation
            )
            velocity = np.stack(
                (np.zeros_like(self.x), dpsi_dz, -dpsi_dy), axis=0
            )
        else:
            # Generate a continuum Fourier polynomial rather than grid-space
            # noise.  The ordered mode list and seeded coefficients are
            # therefore identical at every admissible resolution, which is
            # essential for a genuine resolution-transport check.
            rng = np.random.default_rng(self.config.seed)
            velocity = np.zeros((3,) + self.x.shape, dtype=float)
            for mode_x in range(-3, 4):
                for mode_y in range(-3, 4):
                    for mode_z in range(-3, 4):
                        mode = (mode_x, mode_y, mode_z)
                        squared_norm = sum(component * component for component in mode)
                        canonical_half = (
                            mode_x > 0
                            or (mode_x == 0 and mode_y > 0)
                            or (mode_x == 0 and mode_y == 0 and mode_z > 0)
                        )
                        if not canonical_half or not (1 <= squared_norm <= 9):
                            continue
                        wavevector = np.asarray(mode, dtype=float)
                        cosine_vector = rng.normal(size=3)
                        sine_vector = rng.normal(size=3)
                        cosine_vector -= wavevector * (
                            float(np.dot(wavevector, cosine_vector)) / squared_norm
                        )
                        sine_vector -= wavevector * (
                            float(np.dot(wavevector, sine_vector)) / squared_norm
                        )
                        phase = mode_x * self.x + mode_y * self.y + mode_z * self.z
                        velocity += (
                            cosine_vector[:, None, None, None] * np.cos(phase)
                            + sine_vector[:, None, None, None] * np.sin(phase)
                        )
        return velocity

    def initial_velocity_hat(self):
        velocity = self.initial_velocity()
        velocity_hat = self.np.fft.fftn(velocity, axes=(1, 2, 3))
        velocity_hat = self.project(velocity_hat)
        retained_velocity = self.np.fft.ifftn(
            velocity_hat, axes=(1, 2, 3)
        ).real
        retained_rms = float(
            self.np.sqrt(
                self.np.mean(self.np.sum(retained_velocity * retained_velocity, axis=0))
            )
        )
        if (
            not math.isfinite(retained_rms)
            or retained_rms <= max(1.0e-14, self.config.amplitude * 1.0e-12)
        ):
            raise RuntimeError(
                "initial condition vanished under projection/dealiasing at this "
                "resolution"
            )
        return velocity_hat * (self.config.amplitude / retained_rms)

    def vorticity_hat(self, velocity_hat):
        kx, ky, kz = self.wavevectors
        ux, uy, uz = velocity_hat
        return 1j * self.np.stack(
            (ky * uz - kz * uy, kz * ux - kx * uz, kx * uy - ky * ux),
            axis=0,
        )

    def right_hand_side(self, velocity_hat):
        np = self.np
        velocity_hat = self.project(velocity_hat)
        vorticity_hat = self.vorticity_hat(velocity_hat)
        velocity = np.fft.ifftn(velocity_hat, axes=(1, 2, 3)).real
        vorticity = np.fft.ifftn(vorticity_hat, axes=(1, 2, 3)).real
        ux, uy, uz = velocity
        wx, wy, wz = vorticity
        cross = np.stack(
            (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx),
            axis=0,
        )
        nonlinear_hat = np.fft.fftn(cross, axes=(1, 2, 3))
        return self.project(nonlinear_hat) - (
            self.config.viscosity * self.k_squared[None, :, :, :] * velocity_hat
        )

    def rk4_step(self, velocity_hat, dt: float):
        k1 = self.right_hand_side(velocity_hat)
        k2 = self.right_hand_side(velocity_hat + 0.5 * dt * k1)
        k3 = self.right_hand_side(velocity_hat + 0.5 * dt * k2)
        k4 = self.right_hand_side(velocity_hat + dt * k3)
        return self.project(
            velocity_hat + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        )

    def stable_timestep(self, velocity_hat) -> float:
        np = self.np
        velocity = np.fft.ifftn(velocity_hat, axes=(1, 2, 3)).real
        maximum_speed = float(np.max(np.sqrt(np.sum(velocity * velocity, axis=0))))
        grid_spacing = DOMAIN_LENGTH / self.config.resolution
        advective = (
            self.config.cfl * grid_spacing / maximum_speed
            if maximum_speed > 0.0
            else self.config.maximum_dt
        )
        diffusive = 2.0 / (
            self.config.viscosity * self.maximum_retained_k_squared
        )
        return min(self.config.maximum_dt, advective, diffusive)

    def _spectral_scalars(self, velocity_hat) -> tuple[float, float, float, float]:
        np = self.np
        normalization = float(self.config.resolution**6)
        vorticity_hat = self.vorticity_hat(velocity_hat)
        velocity_power = np.sum(np.abs(velocity_hat) ** 2, axis=0)
        vorticity_power = np.sum(np.abs(vorticity_hat) ** 2, axis=0)
        energy = 0.5 * float(np.sum(velocity_power)) / normalization
        enstrophy = 0.5 * float(np.sum(vorticity_power)) / normalization
        palinstrophy = (
            0.5 * float(np.sum(self.k_squared * vorticity_power)) / normalization
        )
        helicity = float(
            np.sum(np.real(np.sum(np.conjugate(velocity_hat) * vorticity_hat, axis=0)))
        ) / normalization
        return energy, enstrophy, palinstrophy, helicity

    def _energy_spectrum(self, velocity_hat) -> tuple[float, ...]:
        np = self.np
        normalization = float(self.config.resolution**6)
        shell = np.rint(np.sqrt(self.k_squared)).astype(int)
        weights = 0.5 * np.sum(np.abs(velocity_hat) ** 2, axis=0) / normalization
        spectrum = np.bincount(shell.ravel(), weights=weights.ravel())
        return tuple(float(value) for value in spectrum)

    def _oversampled_vorticity_maximum(self, vorticity_hat) -> float:
        """Evaluate max |omega| on a fixed two-times zero-padded grid."""

        np = self.np
        n = self.config.resolution
        doubled = 2 * n
        shifted = np.fft.fftshift(vorticity_hat, axes=(1, 2, 3))
        padded = np.zeros((3, doubled, doubled, doubled), dtype=complex)
        offset = (doubled - n) // 2
        padded[
            :,
            offset : offset + n,
            offset : offset + n,
            offset : offset + n,
        ] = shifted
        padded = np.fft.ifftshift(padded, axes=(1, 2, 3))
        vorticity = (
            np.fft.ifftn(padded, axes=(1, 2, 3)).real
            * (float(doubled) / n) ** 3
        )
        return float(np.max(np.sqrt(np.sum(vorticity * vorticity, axis=0))))

    def _stretching_diagnostics(self, velocity_hat, vorticity):
        np = self.np
        gradient = np.empty((3, 3) + self.x.shape, dtype=float)
        for component in range(3):
            for direction in range(3):
                derivative_hat = (
                    1j * self.wavevectors[direction] * velocity_hat[component]
                )
                gradient[component, direction] = np.fft.ifftn(
                    derivative_hat, axes=(0, 1, 2)
                ).real
        strain = 0.5 * (gradient + np.swapaxes(gradient, 0, 1))
        strain_vorticity = np.einsum("ijxyz,jxyz->ixyz", strain, vorticity)
        stretching = float(np.mean(np.sum(vorticity * strain_vorticity, axis=0)))
        maximum_strain_frobenius = float(
            np.max(np.sqrt(np.sum(strain * strain, axis=(0, 1))))
        )
        return stretching, maximum_strain_frobenius

    def _analyticity_strip(self, spectrum: Sequence[float]) -> dict[str, object]:
        np = self.np
        cutoff = self.retained_axis_wavenumber
        points = [
            (k, float(spectrum[k]))
            for k in range(max(2, cutoff // 2), min(cutoff, len(spectrum) - 1) + 1)
            if float(spectrum[k]) > 1.0e-28
        ]
        if len(points) < 3:
            return {
                "width": None,
                "algebraic_exponent": None,
                "r_squared": None,
                "fit_shells": tuple(k for k, _ in points),
                "candidate_eligible": False,
                "method": "C*k^(-p)*exp(-2*delta*k); insufficient shells",
            }
        x = np.asarray([float(k) for k, _ in points])
        y = np.log(np.asarray([value for _, value in points]))
        if len(points) < 4:
            return {
                "width": None,
                "algebraic_exponent": None,
                "r_squared": None,
                "fit_shells": tuple(k for k, _ in points),
                "candidate_eligible": False,
                "method": "C*k^(-p)*exp(-2*delta*k); insufficient shells",
            }
        design = np.stack((np.ones_like(x), np.log(x), x), axis=1)
        coefficients = np.linalg.lstsq(design, y, rcond=None)[0]
        prediction = design @ coefficients
        residual = float(np.sum((y - prediction) ** 2))
        total = float(np.sum((y - float(np.mean(y))) ** 2))
        r_squared = 1.0 - residual / total if total > 0.0 else 1.0
        width = max(0.0, -0.5 * float(coefficients[2]))
        return {
            "width": width,
            "algebraic_exponent": -float(coefficients[1]),
            "r_squared": r_squared,
            "fit_shells": tuple(k for k, _ in points),
            "candidate_eligible": len(points) >= 5 and r_squared >= 0.95,
            "method": "E(k) proportional to k^(-p)*exp(-2*delta*k) tail proxy",
        }

    def diagnostics(self, velocity_hat, time: float) -> dict[str, object]:
        np = self.np
        energy, enstrophy, palinstrophy, helicity = self._spectral_scalars(
            velocity_hat
        )
        velocity = np.fft.ifftn(velocity_hat, axes=(1, 2, 3)).real
        vorticity_hat = self.vorticity_hat(velocity_hat)
        vorticity = np.fft.ifftn(vorticity_hat, axes=(1, 2, 3)).real
        stretching, maximum_strain = self._stretching_diagnostics(
            velocity_hat, vorticity
        )
        divergence_hat = 1j * np.sum(self.wavevectors * velocity_hat, axis=0)
        normalization = float(self.config.resolution**6)
        divergence_l2 = math.sqrt(
            float(np.sum(np.abs(divergence_hat) ** 2)) / normalization
        )
        spectrum = self._energy_spectrum(velocity_hat)
        analyticity = self._analyticity_strip(spectrum)
        axis_high = np.max(np.abs(self.wavevectors), axis=0) >= (
            0.80 * self.retained_axis_wavenumber
        )
        velocity_power = np.sum(np.abs(velocity_hat) ** 2, axis=0)
        high_fraction = float(np.sum(velocity_power[axis_high])) / max(
            float(np.sum(velocity_power)), 1.0e-300
        )
        speed = np.sqrt(np.sum(velocity * velocity, axis=0))
        grid_vorticity = float(
            np.max(np.sqrt(np.sum(vorticity * vorticity, axis=0)))
        )
        return {
            "time": float(time),
            "energy": energy,
            "enstrophy": enstrophy,
            "palinstrophy": palinstrophy,
            "vortex_stretching": stretching,
            "helicity": helicity,
            "velocity_l3_norm": float(np.mean(speed**3) ** (1.0 / 3.0)),
            "maximum_velocity": float(np.max(speed)),
            "grid_maximum_vorticity": grid_vorticity,
            "maximum_vorticity": self._oversampled_vorticity_maximum(
                vorticity_hat
            ),
            "maximum_strain_frobenius": maximum_strain,
            "divergence_l2": divergence_l2,
            "high_wavenumber_energy_fraction": high_fraction,
            "analyticity_strip": analyticity,
            "energy_spectrum": spectrum,
        }

    def run(self, observer=None) -> dict[str, object]:
        """Evolve one trajectory and optionally observe each stored sample.

        ``observer`` is called as ``observer(solver, velocity_hat, sample)``
        after the sample diagnostics are complete.  It must treat the Fourier
        state as read-only.  Keeping observer products outside the base result
        preserves the frozen phase-one numerical record while allowing richer
        DET/RET diagnostics to be layered over the same integration.
        """
        velocity_hat = self.initial_velocity_hat()
        initial = self.diagnostics(velocity_hat, 0.0)
        initial["approximate_bkm_integral"] = 0.0
        samples = [initial]
        if observer is not None:
            observer_state = self.np.array(velocity_hat, copy=True)
            observer_state.flags.writeable = False
            observer(self, observer_state, copy.deepcopy(initial))
        time = 0.0
        step_count = 0
        next_sample = min(self.config.sample_interval, self.config.final_time)
        previous_enstrophy = float(initial["enstrophy"])
        previous_energy = float(initial["energy"])
        dissipation_enstrophy_integral = 0.0
        approximate_bkm_integral = 0.0
        previous_sample_time = 0.0
        previous_sample_vorticity = float(initial["maximum_vorticity"])
        maximum_relative_energy_increase = 0.0
        maximum_relative_step_energy_increase = 0.0
        maximum_positive_step_energy_balance_residual = 0.0

        while time < self.config.final_time - 1.0e-14:
            if step_count >= self.config.maximum_steps:
                raise RuntimeError("Navier--Stokes run exhausted its step limit")
            dt = min(
                self.stable_timestep(velocity_hat),
                self.config.final_time - time,
                max(next_sample - time, 0.0) or self.config.maximum_dt,
            )
            if not math.isfinite(dt) or dt <= 0.0:
                raise RuntimeError("Navier--Stokes timestep became invalid")
            velocity_hat = self.rk4_step(velocity_hat, dt)
            if not bool(self.np.all(self.np.isfinite(velocity_hat))):
                raise RuntimeError("Navier--Stokes state became nonfinite")
            new_time = time + dt
            new_energy, new_enstrophy, _, _ = self._spectral_scalars(velocity_hat)
            step_dissipation = (
                2.0
                * self.config.viscosity
                * 0.5
                * (previous_enstrophy + new_enstrophy)
                * dt
            )
            maximum_relative_step_energy_increase = max(
                maximum_relative_step_energy_increase,
                (new_energy - previous_energy)
                / max(float(initial["energy"]), 1.0e-300),
            )
            maximum_positive_step_energy_balance_residual = max(
                maximum_positive_step_energy_balance_residual,
                (new_energy - previous_energy + step_dissipation)
                / max(float(initial["energy"]), 1.0e-300),
            )
            dissipation_enstrophy_integral += (
                0.5 * (previous_enstrophy + new_enstrophy) * dt
            )
            previous_enstrophy = new_enstrophy
            previous_energy = new_energy
            maximum_relative_energy_increase = max(
                maximum_relative_energy_increase,
                (new_energy - float(initial["energy"]))
                / max(float(initial["energy"]), 1.0e-300),
            )
            time = new_time
            step_count += 1

            if time >= next_sample - 1.0e-12 or time >= self.config.final_time - 1.0e-12:
                sample = self.diagnostics(velocity_hat, time)
                sample_dt = time - previous_sample_time
                approximate_bkm_integral += 0.5 * (
                    previous_sample_vorticity + float(sample["maximum_vorticity"])
                ) * sample_dt
                previous_sample_time = time
                previous_sample_vorticity = float(sample["maximum_vorticity"])
                sample["approximate_bkm_integral"] = approximate_bkm_integral
                samples.append(sample)
                if observer is not None:
                    observer_state = self.np.array(velocity_hat, copy=True)
                    observer_state.flags.writeable = False
                    observer(self, observer_state, copy.deepcopy(sample))
                next_sample = min(
                    next_sample + self.config.sample_interval,
                    self.config.final_time,
                )

        final = samples[-1]
        energy_balance_defect = abs(
            float(final["energy"])
            + 2.0 * self.config.viscosity * dissipation_enstrophy_integral
            - float(initial["energy"])
        ) / max(float(initial["energy"]), 1.0e-300)
        enstrophy_rhs_integral = 0.0
        for left, right in zip(samples[:-1], samples[1:]):
            left_rate = float(left["vortex_stretching"]) - (
                2.0 * self.config.viscosity * float(left["palinstrophy"])
            )
            right_rate = float(right["vortex_stretching"]) - (
                2.0 * self.config.viscosity * float(right["palinstrophy"])
            )
            enstrophy_rhs_integral += 0.5 * (left_rate + right_rate) * (
                float(right["time"]) - float(left["time"])
            )
        enstrophy_balance_defect = abs(
            float(final["enstrophy"])
            - float(initial["enstrophy"])
            - enstrophy_rhs_integral
        ) / max(
            float(initial["enstrophy"]),
            max(float(sample["enstrophy"]) for sample in samples),
            1.0e-300,
        )
        maxima = {
            key: max(float(sample[key]) for sample in samples)
            for key in (
                "enstrophy",
                "palinstrophy",
                "maximum_velocity",
                "maximum_vorticity",
                "divergence_l2",
                "high_wavenumber_energy_fraction",
            )
        }
        maximum_vorticity_sample = max(
            samples, key=lambda row: float(row["maximum_vorticity"])
        )
        result: dict[str, object] = {
            "schema_version": SCHEMA_VERSION,
            "configuration": asdict(self.config),
            "configuration_digest": self.config.digest,
            "dealiasing": {
                "rule": "component-wise 2/3 truncation",
                "retained_axis_wavenumber": self.retained_axis_wavenumber,
                "maximum_retained_k_squared": self.maximum_retained_k_squared,
            },
            "time_integrator": "classical RK4 with advective/diffusive adaptive cap",
            "step_count": step_count,
            "sample_count": len(samples),
            "initial": initial,
            "final": final,
            "maxima": maxima,
            "maximum_vorticity_time": float(maximum_vorticity_sample["time"]),
            "vorticity_amplification": maxima["maximum_vorticity"]
            / max(float(initial["maximum_vorticity"]), 1.0e-300),
            "enstrophy_amplification": maxima["enstrophy"]
            / max(float(initial["enstrophy"]), 1.0e-300),
            "palinstrophy_amplification": maxima["palinstrophy"]
            / max(float(initial["palinstrophy"]), 1.0e-300),
            "energy_balance": {
                "identity": "E(t) + 2*nu*integral(enstrophy dt) = E(0)",
                "relative_defect": energy_balance_defect,
                "maximum_relative_energy_increase": maximum_relative_energy_increase,
                "maximum_relative_step_energy_increase": (
                    maximum_relative_step_energy_increase
                ),
                "maximum_positive_step_balance_residual": (
                    maximum_positive_step_energy_balance_residual
                ),
            },
            "enstrophy_balance": {
                "identity": (
                    "Omega(t)-Omega(0) = integral(stretching-2*nu*palinstrophy dt)"
                ),
                "sample_trapezoid_relative_defect": enstrophy_balance_defect,
            },
            "approximate_bkm_integral": approximate_bkm_integral,
            "samples": tuple(samples),
            "bounded_numerical_computation": True,
            "proof_warning": PROOF_WARNING,
            "interpretation_warning": INTERPRETATION_WARNING,
        }
        result["late_window_power_law_fits"] = _late_window_fits(samples)
        result["numerical_admission"] = classify_numerical_run(result)
        result["run_digest"] = evidence_payload_digest(result)
        return result


def _power_law_fit(
    samples: Sequence[Mapping[str, object]], tail_fraction: float
) -> Optional[dict[str, float]]:
    np = _numpy()
    count = max(5, int(math.ceil(len(samples) * tail_fraction)))
    selected = samples[-count:]
    times = np.asarray([float(row["time"]) for row in selected])
    values = np.asarray([float(row["maximum_vorticity"]) for row in selected])
    if len(times) < 5 or not bool(np.all(values > 0.0)) or values[-1] <= values[0]:
        return None
    span = max(float(times[-1] - times[0]), 1.0e-6)
    offsets = np.geomspace(max(span * 0.02, 1.0e-6), span * 8.0, 240)
    response = np.log(values)
    total = float(np.sum((response - float(np.mean(response))) ** 2))
    best = None
    for offset in offsets:
        singular_time = float(times[-1] + offset)
        predictor = np.log(singular_time - times)
        design = np.stack((np.ones_like(predictor), predictor), axis=1)
        coefficients = np.linalg.lstsq(design, response, rcond=None)[0]
        prediction = design @ coefficients
        residual = float(np.sum((response - prediction) ** 2))
        if best is None or residual < best[0]:
            r_squared = 1.0 - residual / total if total > 0.0 else 1.0
            best = (
                residual,
                {
                    "tail_fraction": float(tail_fraction),
                    "fitted_singular_time": singular_time,
                    "exponent": -float(coefficients[1]),
                    "r_squared": r_squared,
                    "window_start": float(times[0]),
                    "window_stop": float(times[-1]),
                },
            )
    return best[1] if best is not None else None


def _late_window_fits(
    samples: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    broad = _power_law_fit(samples, 0.40)
    narrow = _power_law_fit(samples, 0.30)
    instability = None
    if broad is not None and narrow is not None:
        denominator = max(
            abs(float(broad["fitted_singular_time"])),
            abs(float(narrow["fitted_singular_time"])),
            1.0e-12,
        )
        instability = abs(
            float(broad["fitted_singular_time"])
            - float(narrow["fitted_singular_time"])
        ) / denominator
    return {
        "last_40_percent": broad,
        "last_30_percent": narrow,
        "relative_fitted_time_instability": instability,
        "model": "omega_max approximately C*(T_star-t)^(-gamma)",
        "fit_is_numerical_diagnostic_not_singularity_evidence": True,
    }


def classify_numerical_run(
    result: Mapping[str, object],
    thresholds: NumericalAdmissionThresholds = NumericalAdmissionThresholds(),
) -> dict[str, object]:
    maxima = result["maxima"]
    balance = result["energy_balance"]
    enstrophy_balance = result["enstrophy_balance"]
    final = result["final"]
    fits = result["late_window_power_law_fits"]
    strip = final["analyticity_strip"]
    strip_width = strip["width"]
    cutoff = int(result["dealiasing"]["retained_axis_wavenumber"])
    analyticity_margin = (
        float(strip_width) * cutoff if strip_width is not None else None
    )
    numerical_gates = {
        "finite_energy_balance_defect": float(balance["relative_defect"])
        <= thresholds.maximum_relative_energy_balance_defect,
        "finite_enstrophy_balance_defect": float(
            enstrophy_balance["sample_trapezoid_relative_defect"]
        )
        <= thresholds.maximum_relative_enstrophy_balance_defect,
        "unforced_energy_nonincrease": float(balance["maximum_relative_energy_increase"])
        <= thresholds.maximum_relative_energy_increase,
        "stepwise_energy_nonincrease": float(
            balance["maximum_relative_step_energy_increase"]
        )
        <= thresholds.maximum_relative_step_energy_increase,
        "stepwise_energy_balance": float(
            balance["maximum_positive_step_balance_residual"]
        )
        <= thresholds.maximum_relative_energy_balance_defect,
        "divergence_control": float(maxima["divergence_l2"])
        <= thresholds.maximum_divergence_l2,
        "spectral_tail_occupancy": float(maxima["high_wavenumber_energy_fraction"])
        <= thresholds.maximum_high_wavenumber_energy_fraction,
    }
    broad = fits["last_40_percent"]
    narrow = fits["last_30_percent"]
    instability = fits["relative_fitted_time_instability"]
    scaling_gates = {
        "vorticity_amplification": float(result["vorticity_amplification"])
        >= thresholds.minimum_vorticity_amplification_for_candidate,
        "enstrophy_amplification": float(result["enstrophy_amplification"])
        >= thresholds.minimum_enstrophy_amplification_for_candidate,
        "analyticity_margin": analyticity_margin is not None
        and bool(strip.get("candidate_eligible", False))
        and analyticity_margin
        >= thresholds.minimum_analyticity_margin_for_candidate,
        "two_late_window_fits": broad is not None and narrow is not None,
        "power_law_exponent": broad is not None
        and narrow is not None
        and min(float(broad["exponent"]), float(narrow["exponent"]))
        >= thresholds.minimum_power_law_exponent,
        "power_law_fit_quality": broad is not None
        and narrow is not None
        and min(float(broad["r_squared"]), float(narrow["r_squared"]))
        >= thresholds.minimum_power_law_r_squared,
        "fitted_time_window_stability": instability is not None
        and float(instability)
        <= thresholds.maximum_relative_fitted_time_instability,
        "locked_growth_model_holdout": LOCKED_GROWTH_MODEL_HOLDOUT_AVAILABLE,
    }
    if not all(numerical_gates.values()):
        state = "UNDERRESOLVED"
        reason = "one or more numerical-admission gates failed"
    elif all(scaling_gates.values()):
        state = "SINGLE_RUN_SCALING_TRIGGER"
        reason = (
            "the bounded run clears single-resolution numerical and scaling "
            "gates; independent resolution and timestep transport remain required"
        )
    elif float(result["vorticity_amplification"]) >= (
        thresholds.minimum_vorticity_amplification_for_transient
    ):
        state = "RESOLVED_TRANSIENT_AMPLIFICATION"
        reason = "resolved vorticity amplification does not clear the scaling gates"
    else:
        state = "NO_NEAR_SINGULAR_SCALING"
        reason = "no admitted near-singular scaling appears on this bounded run"
    return {
        "state": state,
        "reason": reason,
        "numerical_gates": numerical_gates,
        "numerical_gates_passed": all(numerical_gates.values()),
        "scaling_gates": scaling_gates,
        "scaling_gates_passed": all(scaling_gates.values()),
        "analyticity_margin_delta_kmax": analyticity_margin,
        "formal_singularity_claim": False,
        "proof_language_allowed": False,
    }


def _relative_gap(lower: float, higher: float) -> float:
    return abs(float(lower) - float(higher)) / max(abs(float(higher)), 1.0e-12)


def _spectrum_relative_gap(
    lower: Sequence[float], higher: Sequence[float]
) -> float:
    common = min(len(lower), len(higher))
    if common < 1:
        return math.inf
    squared_difference = sum(
        (float(lower[index]) - float(higher[index])) ** 2
        for index in range(common)
    )
    squared_reference = sum(float(higher[index]) ** 2 for index in range(common))
    return math.sqrt(squared_difference) / max(math.sqrt(squared_reference), 1.0e-12)


def compare_resolution_pair(
    lower: Mapping[str, object],
    higher: Mapping[str, object],
    thresholds: NumericalAdmissionThresholds = NumericalAdmissionThresholds(),
) -> dict[str, object]:
    lower_config = lower["configuration"]
    higher_config = higher["configuration"]
    physical_fields = (
        "initial_condition",
        "viscosity",
        "final_time",
        "amplitude",
        "seed",
    )
    if any(lower_config[field] != higher_config[field] for field in physical_fields):
        raise ValueError("resolution transport requires the same physical action")
    if int(lower_config["resolution"]) >= int(higher_config["resolution"]):
        raise ValueError("resolution pair must be ordered from lower to higher")
    amplification_gap = _relative_gap(
        lower["vorticity_amplification"], higher["vorticity_amplification"]
    )
    enstrophy_gap = _relative_gap(
        lower["enstrophy_amplification"], higher["enstrophy_amplification"]
    )
    palinstrophy_gap = _relative_gap(
        lower["palinstrophy_amplification"], higher["palinstrophy_amplification"]
    )
    initial_spectrum_gap = _spectrum_relative_gap(
        lower["initial"]["energy_spectrum"],
        higher["initial"]["energy_spectrum"],
    )
    final_spectrum_gap = _spectrum_relative_gap(
        lower["final"]["energy_spectrum"],
        higher["final"]["energy_spectrum"],
    )
    peak_time_gap = abs(
        float(lower["maximum_vorticity_time"])
        - float(higher["maximum_vorticity_time"])
    )
    gates = {
        "both_numerically_admitted": bool(
            lower["numerical_admission"]["numerical_gates_passed"]
            and higher["numerical_admission"]["numerical_gates_passed"]
        ),
        "vorticity_amplification_transport": amplification_gap
        <= thresholds.maximum_resolution_amplification_gap,
        "enstrophy_amplification_transport": enstrophy_gap
        <= thresholds.maximum_resolution_enstrophy_gap,
        "palinstrophy_amplification_transport": palinstrophy_gap
        <= thresholds.maximum_resolution_palinstrophy_gap,
        "initial_spectrum_transport": initial_spectrum_gap
        <= thresholds.maximum_resolution_initial_spectrum_gap,
        "final_spectrum_transport": final_spectrum_gap
        <= thresholds.maximum_resolution_final_spectrum_gap,
        "peak_time_transport": peak_time_gap
        <= thresholds.maximum_resolution_peak_time_gap,
    }
    return {
        "lower_resolution": lower_config["resolution"],
        "higher_resolution": higher_config["resolution"],
        "lower_configuration_digest": lower["configuration_digest"],
        "higher_configuration_digest": higher["configuration_digest"],
        "vorticity_amplification_relative_gap": amplification_gap,
        "enstrophy_amplification_relative_gap": enstrophy_gap,
        "palinstrophy_amplification_relative_gap": palinstrophy_gap,
        "initial_spectrum_relative_l2_gap": initial_spectrum_gap,
        "final_spectrum_relative_l2_gap": final_spectrum_gap,
        "maximum_vorticity_time_absolute_gap": peak_time_gap,
        "gates": gates,
        "transport_passed": all(gates.values()),
        "transport_is_numerical_not_replication": True,
    }


def compare_timestep_pair(
    coarser: Mapping[str, object],
    finer: Mapping[str, object],
    thresholds: NumericalAdmissionThresholds = NumericalAdmissionThresholds(),
) -> dict[str, object]:
    """Audit a maximum-timestep halving without counting it as replication."""

    coarse_config = coarser["configuration"]
    fine_config = finer["configuration"]
    fixed_fields = (
        "initial_condition",
        "resolution",
        "viscosity",
        "final_time",
        "amplitude",
        "cfl",
        "sample_interval",
        "seed",
    )
    if any(coarse_config[field] != fine_config[field] for field in fixed_fields):
        raise ValueError("timestep transport requires the same spatial/physical action")
    if float(coarse_config["maximum_dt"]) <= float(fine_config["maximum_dt"]):
        raise ValueError("timestep pair must be ordered from coarser to finer")
    gaps = {
        "vorticity_amplification": _relative_gap(
            coarser["vorticity_amplification"], finer["vorticity_amplification"]
        ),
        "enstrophy_amplification": _relative_gap(
            coarser["enstrophy_amplification"], finer["enstrophy_amplification"]
        ),
        "palinstrophy_amplification": _relative_gap(
            coarser["palinstrophy_amplification"], finer["palinstrophy_amplification"]
        ),
        "final_spectrum": _spectrum_relative_gap(
            coarser["final"]["energy_spectrum"],
            finer["final"]["energy_spectrum"],
        ),
    }
    peak_time_gap = abs(
        float(coarser["maximum_vorticity_time"])
        - float(finer["maximum_vorticity_time"])
    )
    gates = {
        "both_numerically_admitted": bool(
            coarser["numerical_admission"]["numerical_gates_passed"]
            and finer["numerical_admission"]["numerical_gates_passed"]
        ),
        **{
            f"{name}_transport": value
            <= thresholds.maximum_timestep_diagnostic_gap
            for name, value in gaps.items()
        },
        "peak_time_transport": peak_time_gap
        <= thresholds.maximum_resolution_peak_time_gap,
    }
    return {
        "resolution": coarse_config["resolution"],
        "coarse_maximum_dt": coarse_config["maximum_dt"],
        "fine_maximum_dt": fine_config["maximum_dt"],
        "coarse_configuration_digest": coarser["configuration_digest"],
        "fine_configuration_digest": finer["configuration_digest"],
        "relative_gaps": gaps,
        "maximum_vorticity_time_absolute_gap": peak_time_gap,
        "gates": gates,
        "transport_passed": all(gates.values()),
        "transport_is_numerical_not_replication": True,
    }


def development_actions() -> tuple[SpectralRunConfig, ...]:
    """Return the fixed first bounded scout; no action is historically unique."""

    return (
        SpectralRunConfig("abc", 16, 0.02, 0.50, role="calibration"),
        SpectralRunConfig("taylor_green", 16, 0.01, 1.00),
        SpectralRunConfig("taylor_green", 24, 0.01, 1.00),
        SpectralRunConfig("kida_pelz", 16, 0.01, 0.75),
        SpectralRunConfig("kida_pelz", 24, 0.01, 0.75),
        SpectralRunConfig("vortex_tubes", 16, 0.01, 0.50),
        SpectralRunConfig("random_low_mode", 16, 0.01, 0.75, seed=20260826),
    )


def phase_one_resolution_ladder_actions() -> tuple[SpectralRunConfig, ...]:
    """Return the consumed, reproducible random-low-mode refinement ladder."""

    return tuple(
        SpectralRunConfig(
            "random_low_mode",
            resolution,
            0.01,
            0.75,
            maximum_dt=0.00375,
            sample_interval=0.05,
            seed=20260826,
            role="resolution_calibration",
        )
        for resolution in (16, 24, 32, 40, 48)
    )


def phase_one_timestep_actions() -> tuple[SpectralRunConfig, ...]:
    """Return the consumed maximum-timestep pair at the admitted 40^3 grid."""

    return tuple(
        SpectralRunConfig(
            "random_low_mode",
            40,
            0.01,
            0.75,
            maximum_dt=maximum_dt,
            sample_interval=0.05,
            seed=20260826,
            role="timestep_calibration",
        )
        for maximum_dt in (0.0075, 0.00375)
    )


def prepare_navier_stokes_protocol(
    actions: Optional[Sequence[SpectralRunConfig]] = None,
) -> dict[str, object]:
    """Freeze the reproducible development protocol without running the PDE."""

    configs = tuple(actions or development_actions())
    if len({config.digest for config in configs}) != len(configs):
        raise ValueError("protocol actions must have unique configurations")
    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "experiment": "3-D periodic incompressible Navier--Stokes near-singularity scout",
        "equation": "du/dt = P(u cross curl(u)) + nu*Delta(u)",
        "domain": "[0, 2*pi)^3",
        "boundary_condition": "periodic",
        "forcing": "none",
        "precision": "NumPy complex128/float64",
        "spatial_discretization": (
            "Fourier pseudo-spectral, Leray projected, strict component-wise "
            "2/3 retained band"
        ),
        "time_discretization": "classical RK4 with adaptive stability cap",
        "diagnostics": (
            "energy",
            "enstrophy",
            "palinstrophy",
            "vortex stretching",
            "grid and fixed-2x-interpolated maximum vorticity",
            "BKM-style vorticity integral",
            "velocity L3 norm",
            "spectral-tail occupancy",
            "analyticity-strip proxy",
            "energy and enstrophy balance defects",
            "divergence",
        ),
        "development_actions": tuple(asdict(config) for config in configs),
        "development_source_ids": tuple(
            f"ns-config-{config.digest}" for config in configs
        ),
        "numerical_admission_thresholds": asdict(NumericalAdmissionThresholds()),
        "growth_model_holdout_available": LOCKED_GROWTH_MODEL_HOLDOUT_AVAILABLE,
        "locked_confirmation_available": False,
        "rg2_evaluation_authorized": False,
        "rg2_exact_certificate_branch_authorized": False,
        "rg2_bounded_exact_computation_branch_authorized": False,
        "finite_time_singularity_claim_authorized": False,
        "global_regularity_claim_authorized": False,
        "consumed_phase_one_reference_findings_sha256": (
            PHASE_ONE_REFERENCE_FINDINGS_SHA256
        ),
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "primary_references": PRIMARY_REFERENCES,
        "proof_warning": PROOF_WARNING,
        "interpretation_warning": INTERPRETATION_WARNING,
    }
    manifest["manifest_digest"] = evidence_payload_digest(manifest)
    return manifest


def _result_evidence_observation(result: Mapping[str, object]) -> dict[str, object]:
    return {
        "configuration_digest": result["configuration_digest"],
        "run_digest": result["run_digest"],
        "configuration": result["configuration"],
        "step_count": result["step_count"],
        "vorticity_amplification": result["vorticity_amplification"],
        "enstrophy_amplification": result["enstrophy_amplification"],
        "palinstrophy_amplification": result["palinstrophy_amplification"],
        "maximum_vorticity_time": result["maximum_vorticity_time"],
        "energy_balance": result["energy_balance"],
        "enstrophy_balance": result["enstrophy_balance"],
        "numerical_admission": result["numerical_admission"],
    }


def build_numerical_evidence_ledger(
    results: Sequence[Mapping[str, object]],
) -> EvidenceLedger:
    ledger = EvidenceLedger()
    for index, result in enumerate(results, 1):
        observation = _result_evidence_observation(result)
        config = result["configuration"]
        ledger = ledger.append(
            EvidenceRecord(
                record_id=f"navier_stokes_numerical_run_{index}",
                source_ids=(f"ns-config-{result['configuration_digest']}",),
                action=str(config["initial_condition"]),
                coordinate=float(config["viscosity"]),
                digest=evidence_payload_digest(observation),
                family="navier_stokes_numerical_trajectory",
                scope="bounded_floating_point_pde",
                observation=observation,
                metadata={
                    "resolution": config["resolution"],
                    "role": config["role"],
                    "historically_unique_evidence": False,
                },
                joint=True,
            )
        )
    return ledger


def _physical_action_key(result: Mapping[str, object]) -> tuple[object, ...]:
    config = result["configuration"]
    return (
        config["initial_condition"],
        config["viscosity"],
        config["final_time"],
        config["amplitude"],
        config["seed"],
    )


def _finest_results_by_resolution(
    results: Sequence[Mapping[str, object]],
) -> tuple[Mapping[str, object], ...]:
    selected: dict[int, Mapping[str, object]] = {}
    for result in results:
        config = result["configuration"]
        resolution = int(config["resolution"])
        current = selected.get(resolution)
        if current is None or float(config["maximum_dt"]) < float(
            current["configuration"]["maximum_dt"]
        ):
            selected[resolution] = result
    return tuple(selected[resolution] for resolution in sorted(selected))


def rank_followup_actions(
    results: Sequence[Mapping[str, object]],
) -> tuple[dict[str, object], ...]:
    """Rank deterministic calibration/search actions from admitted diagnostics."""

    proposals = []
    seen = {str(result["configuration_digest"]) for result in results}
    grouped = {}
    for result in results:
        key = _physical_action_key(result)
        grouped.setdefault(key, []).append(result)
    transported_keys = set()
    selected_highest_digest = {}
    for key, group in grouped.items():
        ordered = _finest_results_by_resolution(group)
        selected_highest_digest[key] = ordered[-1]["configuration_digest"]
        if any(
            compare_resolution_pair(lower, higher)["transport_passed"]
            for lower, higher in zip(ordered[:-1], ordered[1:])
        ):
            transported_keys.add(key)
    for result in results:
        config = SpectralRunConfig(**dict(result["configuration"]))
        admission = result["numerical_admission"]
        action_key = _physical_action_key(result)
        if result["configuration_digest"] != selected_highest_digest[action_key]:
            continue
        if config.role == "calibration" and admission["numerical_gates_passed"]:
            continue
        signal = math.log1p(max(float(result["vorticity_amplification"]) - 1.0, 0.0))
        high_tail = float(result["maxima"]["high_wavenumber_energy_fraction"])
        balance = float(result["energy_balance"]["relative_defect"])
        uncertainty = min(4.0, 200.0 * high_tail + 50.0 * balance)
        if action_key in transported_keys and admission["numerical_gates_passed"]:
            proposed = replace(
                config,
                resolution=max(16, config.resolution - 8),
                viscosity=max(config.viscosity * 0.70, 1.0e-4),
                role="stress_test",
            )
            reason = (
                "increase Reynolds stress from the cheaper member after "
                "adjacent-grid transport"
            )
            information = 2.5 + signal
        elif admission["state"] == "UNDERRESOLVED" or signal > 0.15:
            proposed = replace(
                config,
                resolution=config.resolution + 8,
                maximum_dt=config.maximum_dt * 0.75,
                role="resolution_calibration",
            )
            reason = "resolve spectral/numerical uncertainty around the strongest signal"
            information = 2.0 + signal + uncertainty
        else:
            proposed = replace(
                config,
                viscosity=max(config.viscosity * 0.70, 1.0e-4),
                role="stress_test",
            )
            reason = "increase Reynolds stress after an admitted bounded run"
            information = 1.0 + signal
        if proposed.digest in seen:
            continue
        relative_cost = (proposed.resolution / 16.0) ** 4 * proposed.final_time
        utility = information / max(relative_cost, 1.0e-12)
        proposals.append(
            {
                "configuration": asdict(proposed),
                "configuration_digest": proposed.digest,
                "reason": reason,
                "diagnostic_information_proxy": information,
                "relative_cost_proxy": relative_cost,
                "utility": utility,
                "scheduler_is_deterministic_proxy_not_bayesian_posterior": True,
            }
        )
    proposals.sort(key=lambda row: (-float(row["utility"]), row["configuration_digest"]))
    return tuple(proposals)


def run_development_suite(
    actions: Optional[Sequence[SpectralRunConfig]] = None,
) -> dict[str, object]:
    configs = tuple(actions or development_actions())
    if len({config.digest for config in configs}) != len(configs):
        raise ValueError("development actions must have unique configurations")
    results = tuple(SpectralNavierStokes3D(config).run() for config in configs)
    protocol = prepare_navier_stokes_protocol(configs)
    ledger = build_numerical_evidence_ledger(results)
    grouped_results: dict[tuple[object, ...], list[Mapping[str, object]]] = {}
    for result in results:
        grouped_results.setdefault(_physical_action_key(result), []).append(result)
    comparisons = []
    for physical_key, group in sorted(
        grouped_results.items(), key=lambda item: repr(item[0])
    ):
        ordered = _finest_results_by_resolution(group)
        for lower, higher in zip(ordered[:-1], ordered[1:]):
            comparisons.append(
                {
                    "initial_condition": physical_key[0],
                    **compare_resolution_pair(lower, higher),
                }
            )
    timestep_comparisons = []
    for physical_key, group in sorted(
        grouped_results.items(), key=lambda item: repr(item[0])
    ):
        by_resolution: dict[int, list[Mapping[str, object]]] = {}
        for result in group:
            by_resolution.setdefault(
                int(result["configuration"]["resolution"]), []
            ).append(result)
        for resolution, same_grid in sorted(by_resolution.items()):
            ordered = sorted(
                same_grid,
                key=lambda row: float(row["configuration"]["maximum_dt"]),
                reverse=True,
            )
            for coarser, finer in zip(ordered[:-1], ordered[1:]):
                if float(coarser["configuration"]["maximum_dt"]) == float(
                    finer["configuration"]["maximum_dt"]
                ):
                    continue
                timestep_comparisons.append(
                    {
                        "initial_condition": physical_key[0],
                        **compare_timestep_pair(coarser, finer),
                    }
                )
    scaling_candidates = tuple(
        result["configuration_digest"]
        for result in results
        if result["numerical_admission"]["state"]
        == "SINGLE_RUN_SCALING_TRIGGER"
    )
    unresolved = tuple(
        result["configuration_digest"]
        for result in results
        if result["numerical_admission"]["state"] == "UNDERRESOLVED"
    )
    transported_scaling_candidates = tuple(
        str(candidate_digest)
        for candidate_digest in scaling_candidates
        if any(
            row["transport_passed"]
            and row["higher_configuration_digest"] == candidate_digest
            for row in comparisons
        )
        and any(
            row["transport_passed"]
            and candidate_digest
            in {
                row["coarse_configuration_digest"],
                row["fine_configuration_digest"],
            }
            for row in timestep_comparisons
        )
    )
    if transported_scaling_candidates:
        state = "RESOLVED_NEAR_SINGULAR_CANDIDATE_REQUIRES_INDEPENDENT_SOLVER"
    elif unresolved:
        state = "NUMERICAL_MODEL_REVISION"
    elif any(
        result["numerical_admission"]["state"]
        == "RESOLVED_TRANSIENT_AMPLIFICATION"
        for result in results
    ):
        state = "RESOLVED_TRANSIENT_AMPLIFICATION_NO_NEAR_SINGULAR_SCALING"
    else:
        state = "NO_NEAR_SINGULAR_SCALING_ON_COMPUTED_SUITE"
    suite: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "experiment": "3-D periodic incompressible Navier--Stokes near-singularity scout",
        "domain": "[0, 2*pi)^3",
        "equation": "du/dt = P(u cross curl(u)) + nu*Delta(u)",
        "actions_fixed_before_suite": tuple(asdict(config) for config in configs),
        "protocol_manifest_digest": protocol["manifest_digest"],
        "protocol_manifest": protocol,
        "results": results,
        "resolution_transport": tuple(comparisons),
        "timestep_transport": tuple(timestep_comparisons),
        "scaling_candidate_configuration_digests": scaling_candidates,
        "transported_scaling_candidate_configuration_digests": (
            transported_scaling_candidates
        ),
        "underresolved_configuration_digests": unresolved,
        "scientific_state": state,
        "rg2_state": "NOT_EVALUATED_NO_FROZEN_PREDICTIVE_RELATION",
        "formal_singularity_claim": False,
        "proof_language_allowed": False,
        "evidence_ledger": {
            "record_ids": ledger.record_ids,
            "source_ids": ledger.source_ids,
            "source_count": len(ledger.source_ids),
            "historically_unique_evidence": False,
        },
        "ranked_followup_actions": rank_followup_actions(results),
        "primary_references": PRIMARY_REFERENCES,
        "proof_warning": PROOF_WARNING,
        "interpretation_warning": INTERPRETATION_WARNING,
    }
    suite["suite_digest"] = evidence_payload_digest(suite)
    return suite


def compact_suite_summary(suite: Mapping[str, object]) -> dict[str, object]:
    return {
        "scientific_state": suite["scientific_state"],
        "formal_singularity_claim": suite["formal_singularity_claim"],
        "proof_language_allowed": suite["proof_language_allowed"],
        "runs": tuple(
            {
                "family": result["configuration"]["initial_condition"],
                "resolution": result["configuration"]["resolution"],
                "viscosity": result["configuration"]["viscosity"],
                "vorticity_amplification": result["vorticity_amplification"],
                "enstrophy_amplification": result["enstrophy_amplification"],
                "high_wavenumber_energy_fraction": result["maxima"][
                    "high_wavenumber_energy_fraction"
                ],
                "energy_balance_relative_defect": result["energy_balance"][
                    "relative_defect"
                ],
                "state": result["numerical_admission"]["state"],
            }
            for result in suite["results"]
        ),
        "resolution_transport": suite["resolution_transport"],
        "timestep_transport": suite["timestep_transport"],
        "top_followup_action": (
            suite["ranked_followup_actions"][0]
            if suite["ranked_followup_actions"]
            else None
        ),
        "suite_digest": suite["suite_digest"],
        "proof_warning": suite["proof_warning"],
    }


if __name__ == "__main__":
    import json

    try:
        print(json.dumps(compact_suite_summary(run_development_suite()), indent=2))
    except RuntimeError as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, indent=2))
