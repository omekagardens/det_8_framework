"""Floating-source boundary conditions for the Exodus/DET field simulation.

The earlier field run prescribed the two electrode potentials relative to the
grounded chamber.  That is appropriate for a grounded supply, but it is not a
self-contained floating circuit: an isolated two-terminal source determines
the voltage difference while its common-mode voltage is set by charge and
capacitance to the surroundings.

This module extracts the two-conductor Maxwell capacitance matrix from two
Laplace basis solutions.  It then imposes both

    V_high - V_return = V_drive
    Q_device + Q_supply,stray = Q_target

to determine the floating common mode.  Linearity lets every topology and
sensitivity point reuse the same two field solves.

All charges and capacitances are for the declared out-of-plane extrusion
depth.  This remains a 2-D electrostatic cross-section rather than a complete
3-D apparatus model.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import exp
from typing import Dict, Iterable, List, Tuple

from det8.models.exodus_field_solver import (
    CHAMBER,
    DIELECTRIC,
    HIGH_ELECTRODE,
    RETURN_ELECTRODE,
    BladeFlatGeometry,
    FieldGridConfig,
    FieldSolution,
    maxwell_pressure_ledger,
    solve_blade_flat_field,
)


EPSILON_0 = 8.8541878128e-12


@dataclass(frozen=True)
class CapacitanceMatrix:
    """Two-conductor capacitance coefficients relative to the chamber."""

    c_hh_f: float
    c_hr_f: float
    c_rh_f: float
    c_rr_f: float
    extrusion_depth_m: float
    raw_reciprocity_relative_error: float

    @property
    def device_common_capacitance_f(self) -> float:
        """d(Q_high + Q_return)/dV_common at fixed differential voltage."""

        return self.c_hh_f + self.c_hr_f + self.c_rh_f + self.c_rr_f

    @property
    def high_column_total_f(self) -> float:
        """Total-device charge from one volt on high with return grounded."""

        return self.c_hh_f + self.c_rh_f

    def conductor_charges_c(self, high_v: float, return_v: float) -> Tuple[float, float]:
        return (
            self.c_hh_f * high_v + self.c_hr_f * return_v,
            self.c_rh_f * high_v + self.c_rr_f * return_v,
        )

    def as_dict(self) -> Dict[str, float]:
        return {
            "c_hh_f": self.c_hh_f,
            "c_hr_f": self.c_hr_f,
            "c_rh_f": self.c_rh_f,
            "c_rr_f": self.c_rr_f,
            "device_common_capacitance_f": self.device_common_capacitance_f,
            "extrusion_depth_m": self.extrusion_depth_m,
            "raw_reciprocity_relative_error": self.raw_reciprocity_relative_error,
        }


@dataclass(frozen=True)
class FieldBasis:
    """Unit-potential solutions used to synthesize arbitrary source topology."""

    high_unit: FieldSolution
    return_unit: FieldSolution
    capacitance: CapacitanceMatrix


def _surface_charge_c(
    solution: FieldSolution,
    conductor_label: int,
    *,
    voltage_scale_v: float,
    extrusion_depth_m: float,
) -> float:
    """Integrate epsilon E_normal over grid faces bordering dielectric.

    For a face pointing from conductor into dielectric,
    E_normal=(V_conductor-V_dielectric)/h.  Multiplication by the 2-D face
    area h*depth cancels h, leaving epsilon*deltaV*depth per face.
    """

    labels = solution.labels
    potential = solution.potential
    nx = solution.config.nx
    ny = solution.config.ny
    charge_c = 0.0
    for j in range(ny):
        for i in range(nx):
            idx = j * nx + i
            if labels[idx] != conductor_label:
                continue
            conductor_v = potential[idx]
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni = i + di
                nj = j + dj
                neighbor = nj * nx + ni
                if 0 <= ni < nx and 0 <= nj < ny and labels[neighbor] == DIELECTRIC:
                    charge_c += (
                        EPSILON_0
                        * (conductor_v - potential[neighbor])
                        * voltage_scale_v
                        * extrusion_depth_m
                    )
    return charge_c


def conductor_charges_c(
    solution: FieldSolution,
    *,
    voltage_scale_v: float,
    extrusion_depth_m: float,
) -> Dict[str, float]:
    """Return direct grid-flux charges on high, return, and chamber surfaces."""

    high_c = _surface_charge_c(
        solution,
        HIGH_ELECTRODE,
        voltage_scale_v=voltage_scale_v,
        extrusion_depth_m=extrusion_depth_m,
    )
    return_c = _surface_charge_c(
        solution,
        RETURN_ELECTRODE,
        voltage_scale_v=voltage_scale_v,
        extrusion_depth_m=extrusion_depth_m,
    )
    chamber_c = _surface_charge_c(
        solution,
        CHAMBER,
        voltage_scale_v=voltage_scale_v,
        extrusion_depth_m=extrusion_depth_m,
    )
    return {
        "high_c": high_c,
        "return_c": return_c,
        "device_c": high_c + return_c,
        "chamber_c": chamber_c,
        "all_conductors_residual_c": high_c + return_c + chamber_c,
    }


def extract_field_basis(
    config: FieldGridConfig,
    geometry: BladeFlatGeometry,
    *,
    extrusion_depth_m: float = 0.01,
) -> FieldBasis:
    """Solve the two unit-voltage fields and extract a reciprocal C matrix."""

    high_geometry = replace(geometry, high_potential_norm=1.0, return_potential_norm=0.0)
    return_geometry = replace(geometry, high_potential_norm=0.0, return_potential_norm=1.0)
    high_unit = solve_blade_flat_field(config, high_geometry)
    return_unit = solve_blade_flat_field(config, return_geometry)

    high_basis_q = conductor_charges_c(
        high_unit,
        voltage_scale_v=1.0,
        extrusion_depth_m=extrusion_depth_m,
    )
    return_basis_q = conductor_charges_c(
        return_unit,
        voltage_scale_v=1.0,
        extrusion_depth_m=extrusion_depth_m,
    )

    raw_c_hr = return_basis_q["high_c"]
    raw_c_rh = high_basis_q["return_c"]
    mutual_scale = max(abs(raw_c_hr), abs(raw_c_rh), 1.0e-30)
    reciprocity_error = abs(raw_c_hr - raw_c_rh) / mutual_scale

    # Reciprocity is exact in the continuum.  The symmetric average removes
    # the small face-integration/discretization mismatch before charge solves.
    mutual_f = 0.5 * (raw_c_hr + raw_c_rh)
    capacitance = CapacitanceMatrix(
        c_hh_f=high_basis_q["high_c"],
        c_hr_f=mutual_f,
        c_rh_f=mutual_f,
        c_rr_f=return_basis_q["return_c"],
        extrusion_depth_m=extrusion_depth_m,
        raw_reciprocity_relative_error=reciprocity_error,
    )
    return FieldBasis(high_unit=high_unit, return_unit=return_unit, capacitance=capacitance)


def compose_field(basis: FieldBasis, high_norm: float, return_norm: float) -> FieldSolution:
    """Compose a field by Laplace linearity from the two unit solutions."""

    high = basis.high_unit
    ret = basis.return_unit
    potential = [
        high_norm * high_value + return_norm * return_value
        for high_value, return_value in zip(high.potential, ret.potential)
    ]
    geometry = replace(
        high.geometry,
        high_potential_norm=high_norm,
        return_potential_norm=return_norm,
    )
    return FieldSolution(
        config=high.config,
        geometry=geometry,
        potential=potential,
        labels=high.labels,
        fixed=high.fixed,
        iterations=max(high.iterations, ret.iterations),
        converged=high.converged and ret.converged,
        max_delta=max(high.max_delta, ret.max_delta),
    )


def solve_floating_potentials_v(
    capacitance: CapacitanceMatrix,
    *,
    drive_voltage_v: float,
    target_total_charge_c: float = 0.0,
    supply_stray_capacitance_f: float = 0.0,
) -> Tuple[float, float]:
    """Determine high and return potentials from differential V and net Q.

    The optional supply stray capacitance is connected between the supply's
    mean/common-mode node and chamber ground.  It contributes
    C_stray*(V_high+V_return)/2 to the isolated assembly's total charge.
    """

    c = capacitance
    common_c = c.device_common_capacitance_f
    high_column_c = c.high_column_total_f
    denominator = common_c + supply_stray_capacitance_f
    if denominator <= 0.0:
        raise ValueError("total common-mode capacitance must be positive")
    return_v = (
        target_total_charge_c
        - high_column_c * drive_voltage_v
        - 0.5 * supply_stray_capacitance_f * drive_voltage_v
    ) / denominator
    return return_v + drive_voltage_v, return_v


def _evaluate_state(
    basis: FieldBasis,
    *,
    high_v: float,
    return_v: float,
    drive_voltage_v: float,
) -> Dict[str, object]:
    if drive_voltage_v == 0.0:
        raise ValueError("drive_voltage_v must be nonzero")
    solution = compose_field(basis, high_v / drive_voltage_v, return_v / drive_voltage_v)
    direct_charge = conductor_charges_c(
        solution,
        voltage_scale_v=drive_voltage_v,
        extrusion_depth_m=basis.capacitance.extrusion_depth_m,
    )
    predicted_high_c, predicted_return_c = basis.capacitance.conductor_charges_c(high_v, return_v)
    ledger = maxwell_pressure_ledger(
        solution,
        voltage_v=drive_voltage_v,
        extrusion_depth_m=basis.capacitance.extrusion_depth_m,
    )
    return {
        "high_v": high_v,
        "return_v": return_v,
        "common_mode_v": 0.5 * (high_v + return_v),
        "direct_charge": direct_charge,
        "matrix_charge": {
            "high_c": predicted_high_c,
            "return_c": predicted_return_c,
            "device_c": predicted_high_c + predicted_return_c,
        },
        "ledger": ledger,
    }


def run_floating_supply_suite(
    *,
    drive_voltage_v: float = 40_000.0,
    extrusion_depth_m: float = 0.01,
    charge_fractions: Iterable[float] = (-0.5, -0.1, 0.0, 0.1, 0.5),
    stray_capacitance_ratios: Iterable[float] = (0.0, 0.1, 0.5, 1.0, 5.0),
    leakage_times_over_tau: Iterable[float] = (0.0, 0.1, 0.5, 1.0, 2.0, 5.0),
) -> Dict[str, object]:
    """Run floating-neutral, charge, stray-C, and return-leakage comparisons."""

    config = FieldGridConfig()
    geometry = BladeFlatGeometry(
        center_x=config.nx // 2,
        center_y=config.ny // 2,
        orientation=1,
    )
    basis = extract_field_basis(config, geometry, extrusion_depth_m=extrusion_depth_m)
    cap = basis.capacitance

    grounded = _evaluate_state(
        basis,
        high_v=drive_voltage_v,
        return_v=0.0,
        drive_voltage_v=drive_voltage_v,
    )
    bipolar = _evaluate_state(
        basis,
        high_v=0.5 * drive_voltage_v,
        return_v=-0.5 * drive_voltage_v,
        drive_voltage_v=drive_voltage_v,
    )
    floating_high_v, floating_return_v = solve_floating_potentials_v(
        cap,
        drive_voltage_v=drive_voltage_v,
    )
    floating = _evaluate_state(
        basis,
        high_v=floating_high_v,
        return_v=floating_return_v,
        drive_voltage_v=drive_voltage_v,
    )

    grounded_charge_scale_c = cap.high_column_total_f * drive_voltage_v
    charge_sweep: List[Dict[str, object]] = []
    for fraction in charge_fractions:
        target_c = fraction * grounded_charge_scale_c
        high_v, return_v = solve_floating_potentials_v(
            cap,
            drive_voltage_v=drive_voltage_v,
            target_total_charge_c=target_c,
        )
        state = _evaluate_state(
            basis,
            high_v=high_v,
            return_v=return_v,
            drive_voltage_v=drive_voltage_v,
        )
        charge_sweep.append({"charge_fraction": fraction, "target_charge_c": target_c, **state})

    stray_sweep: List[Dict[str, object]] = []
    for ratio in stray_capacitance_ratios:
        stray_f = ratio * cap.device_common_capacitance_f
        high_v, return_v = solve_floating_potentials_v(
            cap,
            drive_voltage_v=drive_voltage_v,
            supply_stray_capacitance_f=stray_f,
        )
        state = _evaluate_state(
            basis,
            high_v=high_v,
            return_v=return_v,
            drive_voltage_v=drive_voltage_v,
        )
        stray_charge_c = stray_f * state["common_mode_v"]
        stray_sweep.append(
            {
                "stray_to_device_common_capacitance_ratio": ratio,
                "stray_capacitance_f": stray_f,
                "stray_charge_c": stray_charge_c,
                "assembly_charge_residual_c": state["matrix_charge"]["device_c"] + stray_charge_c,
                **state,
            }
        )

    # Simple leakage boundary model: return potential relaxes exponentially
    # from the isolated value toward chamber ground while the ideal source
    # keeps the differential voltage fixed.
    leakage_sweep: List[Dict[str, object]] = []
    for time_over_tau in leakage_times_over_tau:
        return_v = floating_return_v * exp(-time_over_tau)
        high_v = return_v + drive_voltage_v
        state = _evaluate_state(
            basis,
            high_v=high_v,
            return_v=return_v,
            drive_voltage_v=drive_voltage_v,
        )
        leakage_sweep.append({"time_over_tau": time_over_tau, **state})

    refinement_specs = (
        (
            "coarse",
            FieldGridConfig(nx=41, ny=31, cell_size_m=0.004, sor_omega=1.75),
            BladeFlatGeometry(
                center_x=20,
                center_y=15,
                electrode_height_cells=13,
                blade_length_cells=3,
                closest_gap_cells=3,
                blade_offsets=(-4, 0, 4),
            ),
        ),
        ("base", config, geometry),
        (
            "fine",
            FieldGridConfig(
                nx=161,
                ny=121,
                cell_size_m=0.001,
                sor_omega=1.92,
                max_iterations=12_000,
            ),
            BladeFlatGeometry(
                center_x=80,
                center_y=60,
                electrode_height_cells=49,
                blade_length_cells=12,
                closest_gap_cells=10,
                blade_offsets=(-16, 0, 16),
            ),
        ),
    )
    refinement: List[Dict[str, object]] = []
    for name, refinement_config, refinement_geometry in refinement_specs:
        refinement_basis = (
            basis
            if name == "base"
            else extract_field_basis(
                refinement_config,
                refinement_geometry,
                extrusion_depth_m=extrusion_depth_m,
            )
        )
        refinement_high_v, refinement_return_v = solve_floating_potentials_v(
            refinement_basis.capacitance,
            drive_voltage_v=drive_voltage_v,
        )
        neutral_state = (
            floating
            if name == "base"
            else _evaluate_state(
                refinement_basis,
                high_v=refinement_high_v,
                return_v=refinement_return_v,
                drive_voltage_v=drive_voltage_v,
            )
        )
        grounded_state = (
            grounded
            if name == "base"
            else _evaluate_state(
                refinement_basis,
                high_v=drive_voltage_v,
                return_v=0.0,
                drive_voltage_v=drive_voltage_v,
            )
        )
        refinement.append(
            {
                "name": name,
                "cell_size_m": refinement_config.cell_size_m,
                "basis_high_converged": refinement_basis.high_unit.converged,
                "basis_return_converged": refinement_basis.return_unit.converged,
                "capacitance": refinement_basis.capacitance.as_dict(),
                "floating_neutral": neutral_state,
                "grounded_return": grounded_state,
            }
        )

    return {
        "model": {
            "description": "2-D electrostatic floating two-terminal source in a grounded chamber",
            "drive_voltage_v": drive_voltage_v,
            "extrusion_depth_m": extrusion_depth_m,
            "charge_constraint": "Q_high + Q_return + C_stray*V_common = Q_target",
            "leakage_model": "V_return(t)=V_return,floating*exp(-t/tau), fixed differential voltage",
        },
        "solver": {
            "basis_high_converged": basis.high_unit.converged,
            "basis_return_converged": basis.return_unit.converged,
            "basis_high_iterations": basis.high_unit.iterations,
            "basis_return_iterations": basis.return_unit.iterations,
        },
        "capacitance": cap.as_dict(),
        "topologies": {
            "grounded_return": grounded,
            "arbitrary_bipolar": bipolar,
            "floating_neutral": floating,
        },
        "grounded_charge_scale_c": grounded_charge_scale_c,
        "charge_sweep": charge_sweep,
        "stray_capacitance_sweep": stray_sweep,
        "return_leakage_sweep": leakage_sweep,
        "grid_refinement": refinement,
    }


if __name__ == "__main__":
    import json

    print(json.dumps(run_floating_supply_suite(), indent=2))
