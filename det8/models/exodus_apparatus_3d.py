"""Declared 3-D apparatus surrogate for the Exodus/DET discriminator runs.

This is the next geometric step after the 2-D blade/flat and floating-source
models.  A finite-difference Laplace solve places extruded electrodes and
explicit terminal leads inside a grounded rectangular chamber.  Two unit
solutions provide a reusable capacitance matrix and arbitrary source common
mode.  Maxwell stress on an outer closed surface is checked against chamber
pressure so every reported apparatus force has an external momentum endpoint.

No measured Exodus CAD or circuit values are available in this repository.
Consequently every dimension, lead route, capacitance, and leakage path below
is a declared surrogate and not an apparatus prediction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, replace
from typing import Dict, Iterable, List, Tuple

from det8.models.exodus_simulation import EPSILON_0


DIELECTRIC = 0
HIGH_TERMINAL = 1
RETURN_TERMINAL = 2
CHAMBER = 3


@dataclass(frozen=True)
class Grid3DConfig:
    nx: int = 41
    ny: int = 31
    nz: int = 27
    cell_size_m: float = 0.004
    sor_omega: float = 1.84
    tolerance: float = 5.0e-6
    max_iterations: int = 5_000

    def __post_init__(self) -> None:
        if min(self.nx, self.ny, self.nz) < 15:
            raise ValueError("3-D grid dimensions must each be at least 15")
        if self.cell_size_m <= 0.0:
            raise ValueError("cell size must be positive")
        if not 1.0 < self.sor_omega < 2.0:
            raise ValueError("SOR omega must lie between 1 and 2")
        if self.tolerance <= 0.0 or self.max_iterations < 1:
            raise ValueError("invalid convergence controls")


@dataclass(frozen=True)
class Apparatus3DGeometry:
    center_x: int
    center_y: int
    center_z: int
    orientation: int = 1
    electrode_height_cells: int = 13
    electrode_depth_cells: int = 7
    blade_length_cells: int = 3
    closest_gap_cells: int = 3
    blade_offsets: Tuple[int, ...] = (-4, 0, 4)
    lead_routing: str = "same_end"
    lead_wall_clearance_cells: int = 4
    high_potential_norm: float = 1.0
    return_potential_norm: float = 0.0

    def __post_init__(self) -> None:
        if self.orientation not in (-1, 1):
            raise ValueError("orientation must be -1 or +1")
        if self.lead_routing not in ("none", "same_end", "opposite_ends"):
            raise ValueError("unknown lead routing")
        if min(self.electrode_height_cells, self.electrode_depth_cells) < 3:
            raise ValueError("electrode dimensions are too small")
        if self.blade_length_cells < 1 or self.closest_gap_cells < 2:
            raise ValueError("blade length and gap must be positive")
        if self.lead_wall_clearance_cells < 2:
            raise ValueError("leads must remain separated from the chamber")
        if self.high_potential_norm == self.return_potential_norm:
            raise ValueError("terminals must have different potentials")


@dataclass
class FieldSolution3D:
    config: Grid3DConfig
    geometry: Apparatus3DGeometry
    potential: List[float]
    labels: List[int]
    fixed: List[bool]
    iterations: int
    max_delta: float
    converged: bool


@dataclass(frozen=True)
class CapacitanceMatrix3D:
    c_hh_f: float
    c_hr_f: float
    c_rh_f: float
    c_rr_f: float
    raw_reciprocity_relative_error: float

    @property
    def device_common_capacitance_f(self) -> float:
        return self.c_hh_f + self.c_hr_f + self.c_rh_f + self.c_rr_f

    @property
    def high_column_total_f(self) -> float:
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
            "raw_reciprocity_relative_error": self.raw_reciprocity_relative_error,
        }


@dataclass(frozen=True)
class FieldBasis3D:
    high_unit: FieldSolution3D
    return_unit: FieldSolution3D
    capacitance: CapacitanceMatrix3D


def _index(x: int, y: int, z: int, config: Grid3DConfig) -> int:
    return (z * config.ny + y) * config.nx + x


def _set_conductor_cell(
    x: int,
    y: int,
    z: int,
    label: int,
    value: float,
    config: Grid3DConfig,
    potential: List[float],
    labels: List[int],
    fixed: List[bool],
) -> None:
    if not (1 <= x < config.nx - 1 and 1 <= y < config.ny - 1 and 1 <= z < config.nz - 1):
        raise ValueError("apparatus conductor intersects chamber")
    idx = _index(x, y, z, config)
    if labels[idx] not in (DIELECTRIC, label):
        raise ValueError("apparatus conductors overlap")
    potential[idx] = value
    labels[idx] = label
    fixed[idx] = True


def _electrode_coordinates(geometry: Apparatus3DGeometry) -> Dict[str, int]:
    span = geometry.blade_length_cells + geometry.closest_gap_cells
    high_x = geometry.center_x - geometry.orientation * (span // 2)
    return_x = high_x + geometry.orientation * span
    return {
        "high_x": high_x,
        "return_x": return_x,
        "y_min": geometry.center_y - geometry.electrode_height_cells // 2,
        "y_max": geometry.center_y + geometry.electrode_height_cells // 2,
        "z_min": geometry.center_z - geometry.electrode_depth_cells // 2,
        "z_max": geometry.center_z + geometry.electrode_depth_cells // 2,
    }


def build_apparatus_grid(
    config: Grid3DConfig,
    geometry: Apparatus3DGeometry,
) -> Tuple[List[float], List[int], List[bool]]:
    """Construct chamber, extruded blade/flat electrodes, and lead stubs."""

    count = config.nx * config.ny * config.nz
    potential = [0.0] * count
    labels = [DIELECTRIC] * count
    fixed = [False] * count

    for z in range(config.nz):
        for y in range(config.ny):
            for x in range(config.nx):
                if x in (0, config.nx - 1) or y in (0, config.ny - 1) or z in (0, config.nz - 1):
                    idx = _index(x, y, z, config)
                    labels[idx] = CHAMBER
                    fixed[idx] = True

    coordinates = _electrode_coordinates(geometry)
    high_x = coordinates["high_x"]
    return_x = coordinates["return_x"]
    y_min = coordinates["y_min"]
    y_max = coordinates["y_max"]
    z_min = coordinates["z_min"]
    z_max = coordinates["z_max"]

    for z in range(z_min, z_max + 1):
        for y in range(y_min, y_max + 1):
            _set_conductor_cell(
                high_x,
                y,
                z,
                HIGH_TERMINAL,
                geometry.high_potential_norm,
                config,
                potential,
                labels,
                fixed,
            )
            _set_conductor_cell(
                return_x,
                y,
                z,
                RETURN_TERMINAL,
                geometry.return_potential_norm,
                config,
                potential,
                labels,
                fixed,
            )
        for offset in geometry.blade_offsets:
            y = geometry.center_y + offset
            for step in range(geometry.blade_length_cells + 1):
                x = high_x + geometry.orientation * step
                _set_conductor_cell(
                    x,
                    y,
                    z,
                    HIGH_TERMINAL,
                    geometry.high_potential_norm,
                    config,
                    potential,
                    labels,
                    fixed,
                )

    clearance = geometry.lead_wall_clearance_cells
    if geometry.lead_routing in ("same_end", "opposite_ends"):
        for z in range(clearance, z_min + 1):
            _set_conductor_cell(
                high_x,
                geometry.center_y,
                z,
                HIGH_TERMINAL,
                geometry.high_potential_norm,
                config,
                potential,
                labels,
                fixed,
            )
        if geometry.lead_routing == "same_end":
            return_z_values = range(clearance, z_min + 1)
        else:
            return_z_values = range(z_max, config.nz - clearance)
        for z in return_z_values:
            _set_conductor_cell(
                return_x,
                geometry.center_y,
                z,
                RETURN_TERMINAL,
                geometry.return_potential_norm,
                config,
                potential,
                labels,
                fixed,
            )

    return potential, labels, fixed


def solve_apparatus_field(
    config: Grid3DConfig,
    geometry: Apparatus3DGeometry,
) -> FieldSolution3D:
    """Solve the 3-D Laplace equation with red-black SOR."""

    potential, labels, fixed = build_apparatus_grid(config, geometry)
    nx = config.nx
    ny = config.ny
    nz = config.nz
    plane = nx * ny
    omega = config.sor_omega
    max_delta = math.inf

    for iteration in range(1, config.max_iterations + 1):
        max_delta = 0.0
        for parity in (0, 1):
            for z in range(1, nz - 1):
                z_offset = z * plane
                for y in range(1, ny - 1):
                    row = z_offset + y * nx
                    x_start = 1 + ((parity - y - z) & 1)
                    for x in range(x_start, nx - 1, 2):
                        idx = row + x
                        if fixed[idx]:
                            continue
                        average = (
                            potential[idx - 1]
                            + potential[idx + 1]
                            + potential[idx - nx]
                            + potential[idx + nx]
                            + potential[idx - plane]
                            + potential[idx + plane]
                        ) / 6.0
                        old = potential[idx]
                        new = old + omega * (average - old)
                        potential[idx] = new
                        delta = abs(new - old)
                        if delta > max_delta:
                            max_delta = delta
        if max_delta < config.tolerance:
            return FieldSolution3D(
                config,
                geometry,
                potential,
                labels,
                fixed,
                iteration,
                max_delta,
                True,
            )

    return FieldSolution3D(
        config,
        geometry,
        potential,
        labels,
        fixed,
        config.max_iterations,
        max_delta,
        False,
    )


def _surface_charge_c(
    solution: FieldSolution3D,
    conductor_label: int,
    voltage_scale_v: float,
) -> float:
    config = solution.config
    nx = config.nx
    ny = config.ny
    nz = config.nz
    h = config.cell_size_m
    charge_c = 0.0
    neighbor_directions = (
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    )
    for z in range(nz):
        for y in range(ny):
            row = (z * ny + y) * nx
            for x in range(nx):
                idx = row + x
                if solution.labels[idx] != conductor_label:
                    continue
                conductor_v = solution.potential[idx]
                for dx, dy, dz in neighbor_directions:
                    neighbor_x = x + dx
                    neighbor_y = y + dy
                    neighbor_z = z + dz
                    if not (
                        0 <= neighbor_x < nx
                        and 0 <= neighbor_y < ny
                        and 0 <= neighbor_z < nz
                    ):
                        continue
                    neighbor = _index(neighbor_x, neighbor_y, neighbor_z, config)
                    if solution.labels[neighbor] == DIELECTRIC:
                        # epsilon*(deltaV/h)*(h^2) for one voxel face.
                        charge_c += (
                            EPSILON_0
                            * (conductor_v - solution.potential[neighbor])
                            * voltage_scale_v
                            * h
                        )
    return charge_c


def conductor_charges_c(
    solution: FieldSolution3D,
    voltage_scale_v: float,
) -> Dict[str, float]:
    high_c = _surface_charge_c(solution, HIGH_TERMINAL, voltage_scale_v)
    return_c = _surface_charge_c(solution, RETURN_TERMINAL, voltage_scale_v)
    chamber_c = _surface_charge_c(solution, CHAMBER, voltage_scale_v)
    return {
        "high_c": high_c,
        "return_c": return_c,
        "device_c": high_c + return_c,
        "chamber_c": chamber_c,
        "all_conductors_residual_c": high_c + return_c + chamber_c,
    }


def extract_field_basis(
    config: Grid3DConfig,
    geometry: Apparatus3DGeometry,
) -> FieldBasis3D:
    high_unit = solve_apparatus_field(
        config,
        replace(geometry, high_potential_norm=1.0, return_potential_norm=0.0),
    )
    return_unit = solve_apparatus_field(
        config,
        replace(geometry, high_potential_norm=0.0, return_potential_norm=1.0),
    )
    q_high_basis = conductor_charges_c(high_unit, 1.0)
    q_return_basis = conductor_charges_c(return_unit, 1.0)
    raw_c_hr = q_return_basis["high_c"]
    raw_c_rh = q_high_basis["return_c"]
    mutual_scale = max(abs(raw_c_hr), abs(raw_c_rh), 1.0e-30)
    reciprocity_error = abs(raw_c_hr - raw_c_rh) / mutual_scale
    mutual_f = 0.5 * (raw_c_hr + raw_c_rh)
    capacitance = CapacitanceMatrix3D(
        c_hh_f=q_high_basis["high_c"],
        c_hr_f=mutual_f,
        c_rh_f=mutual_f,
        c_rr_f=q_return_basis["return_c"],
        raw_reciprocity_relative_error=reciprocity_error,
    )
    return FieldBasis3D(high_unit, return_unit, capacitance)


def compose_field(
    basis: FieldBasis3D,
    high_norm: float,
    return_norm: float,
) -> FieldSolution3D:
    high = basis.high_unit
    ret = basis.return_unit
    potential = [
        high_norm * high_value + return_norm * return_value
        for high_value, return_value in zip(high.potential, ret.potential)
    ]
    return FieldSolution3D(
        config=high.config,
        geometry=replace(
            high.geometry,
            high_potential_norm=high_norm,
            return_potential_norm=return_norm,
        ),
        potential=potential,
        labels=high.labels,
        fixed=high.fixed,
        iterations=max(high.iterations, ret.iterations),
        max_delta=max(high.max_delta, ret.max_delta),
        converged=high.converged and ret.converged,
    )


def solve_floating_potentials_v(
    capacitance: CapacitanceMatrix3D,
    drive_voltage_v: float,
    target_total_charge_c: float = 0.0,
    high_external_capacitance_f: float = 0.0,
    return_external_capacitance_f: float = 0.0,
) -> Tuple[float, float]:
    """Solve fixed differential voltage plus total assembly charge.

    External capacitances connect separately from each terminal to chamber
    ground, allowing realistic common-mode imbalance rather than assuming a
    single capacitance on the supply mean node.
    """

    if high_external_capacitance_f < 0.0 or return_external_capacitance_f < 0.0:
        raise ValueError("external capacitances cannot be negative")
    denominator = (
        capacitance.device_common_capacitance_f
        + high_external_capacitance_f
        + return_external_capacitance_f
    )
    if denominator <= 0.0:
        raise ValueError("total common-mode capacitance must be positive")
    return_v = (
        target_total_charge_c
        - (capacitance.high_column_total_f + high_external_capacitance_f)
        * drive_voltage_v
    ) / denominator
    return return_v + drive_voltage_v, return_v


def _electric_field_at(
    solution: FieldSolution3D,
    x: int,
    y: int,
    z: int,
    voltage_v: float,
) -> Tuple[float, float, float]:
    config = solution.config
    idx = _index(x, y, z, config)
    nx = config.nx
    plane = config.nx * config.ny
    scale = -voltage_v / (2.0 * config.cell_size_m)
    return (
        (solution.potential[idx + 1] - solution.potential[idx - 1]) * scale,
        (solution.potential[idx + nx] - solution.potential[idx - nx]) * scale,
        (solution.potential[idx + plane] - solution.potential[idx - plane]) * scale,
    )


def _stress_traction(
    electric: Tuple[float, float, float],
    normal: Tuple[float, float, float],
) -> Tuple[float, float, float]:
    dot = sum(e * n for e, n in zip(electric, normal))
    magnitude_sq = sum(e * e for e in electric)
    return tuple(
        EPSILON_0 * (electric[i] * dot - 0.5 * magnitude_sq * normal[i])
        for i in range(3)
    )


def _outer_maxwell_force_n(
    solution: FieldSolution3D,
    voltage_v: float,
) -> Tuple[float, float, float]:
    """Integrate Maxwell stress on a chamber-adjacent closed surface."""

    config = solution.config
    area = config.cell_size_m**2
    force = [0.0, 0.0, 0.0]

    for z in range(1, config.nz - 1):
        for y in range(1, config.ny - 1):
            for x, normal in (
                (1, (-1.0, 0.0, 0.0)),
                (config.nx - 2, (1.0, 0.0, 0.0)),
            ):
                traction = _stress_traction(
                    _electric_field_at(solution, x, y, z, voltage_v), normal
                )
                for axis in range(3):
                    force[axis] += traction[axis] * area

    for z in range(1, config.nz - 1):
        for x in range(1, config.nx - 1):
            for y, normal in (
                (1, (0.0, -1.0, 0.0)),
                (config.ny - 2, (0.0, 1.0, 0.0)),
            ):
                traction = _stress_traction(
                    _electric_field_at(solution, x, y, z, voltage_v), normal
                )
                for axis in range(3):
                    force[axis] += traction[axis] * area

    for y in range(1, config.ny - 1):
        for x in range(1, config.nx - 1):
            for z, normal in (
                (1, (0.0, 0.0, -1.0)),
                (config.nz - 2, (0.0, 0.0, 1.0)),
            ):
                traction = _stress_traction(
                    _electric_field_at(solution, x, y, z, voltage_v), normal
                )
                for axis in range(3):
                    force[axis] += traction[axis] * area

    return tuple(force)


def _chamber_pressure_force_n(
    solution: FieldSolution3D,
    voltage_v: float,
) -> Tuple[float, float, float]:
    config = solution.config
    area = config.cell_size_m**2
    h = config.cell_size_m
    force = [0.0, 0.0, 0.0]

    def add_face(boundary: int, neighbor: int, normal: Tuple[float, float, float]) -> None:
        normal_field = (
            solution.potential[boundary] - solution.potential[neighbor]
        ) * voltage_v / h
        pressure = 0.5 * EPSILON_0 * normal_field**2
        for axis in range(3):
            force[axis] += pressure * area * normal[axis]

    for z in range(1, config.nz - 1):
        for y in range(1, config.ny - 1):
            add_face(
                _index(0, y, z, config),
                _index(1, y, z, config),
                (1.0, 0.0, 0.0),
            )
            add_face(
                _index(config.nx - 1, y, z, config),
                _index(config.nx - 2, y, z, config),
                (-1.0, 0.0, 0.0),
            )
    for z in range(1, config.nz - 1):
        for x in range(1, config.nx - 1):
            add_face(
                _index(x, 0, z, config),
                _index(x, 1, z, config),
                (0.0, 1.0, 0.0),
            )
            add_face(
                _index(x, config.ny - 1, z, config),
                _index(x, config.ny - 2, z, config),
                (0.0, -1.0, 0.0),
            )
    for y in range(1, config.ny - 1):
        for x in range(1, config.nx - 1):
            add_face(
                _index(x, y, 0, config),
                _index(x, y, 1, config),
                (0.0, 0.0, 1.0),
            )
            add_face(
                _index(x, y, config.nz - 1, config),
                _index(x, y, config.nz - 2, config),
                (0.0, 0.0, -1.0),
            )
    return tuple(force)


def maxwell_ledger(solution: FieldSolution3D, voltage_v: float) -> Dict[str, object]:
    device = _outer_maxwell_force_n(solution, voltage_v)
    chamber = _chamber_pressure_force_n(solution, voltage_v)
    residual = tuple(device[i] + chamber[i] for i in range(3))
    residual_norm = math.sqrt(sum(value * value for value in residual))
    magnitude_sum = math.sqrt(sum(value * value for value in device)) + math.sqrt(
        sum(value * value for value in chamber)
    )
    return {
        "device_force_n": {"x": device[0], "y": device[1], "z": device[2]},
        "chamber_force_n": {"x": chamber[0], "y": chamber[1], "z": chamber[2]},
        "global_residual_n": {"x": residual[0], "y": residual[1], "z": residual[2]},
        "relative_closure_error": residual_norm / magnitude_sum if magnitude_sum else 0.0,
    }


def _evaluate_state(
    basis: FieldBasis3D,
    high_v: float,
    return_v: float,
    drive_voltage_v: float,
) -> Dict[str, object]:
    solution = compose_field(basis, high_v / drive_voltage_v, return_v / drive_voltage_v)
    direct_charge = conductor_charges_c(solution, drive_voltage_v)
    matrix_high_c, matrix_return_c = basis.capacitance.conductor_charges_c(high_v, return_v)
    return {
        "high_v": high_v,
        "return_v": return_v,
        "common_mode_v": 0.5 * (high_v + return_v),
        "direct_charge": direct_charge,
        "matrix_charge": {
            "high_c": matrix_high_c,
            "return_c": matrix_return_c,
            "device_c": matrix_high_c + matrix_return_c,
        },
        "ledger": maxwell_ledger(solution, drive_voltage_v),
    }


def run_apparatus_3d_suite(
    drive_voltage_v: float = 40_000.0,
    terminal_capacitance_total_ratios: Iterable[float] = (0.0, 0.5, 1.0, 2.0),
    high_terminal_fractions: Iterable[float] = (0.0, 0.25, 0.5, 0.75, 1.0),
    leakage_times_over_tau: Iterable[float] = (0.0, 0.1, 0.5, 1.0, 2.0, 5.0),
) -> Dict[str, object]:
    """Run 3-D lead routing, terminal-C imbalance, and leakage discriminators."""

    config = Grid3DConfig()
    base_geometry = Apparatus3DGeometry(
        center_x=config.nx // 2,
        center_y=config.ny // 2,
        center_z=config.nz // 2,
        lead_routing="same_end",
    )

    route_bases: Dict[str, FieldBasis3D] = {}
    route_sweep: List[Dict[str, object]] = []
    for routing in ("none", "same_end", "opposite_ends"):
        geometry = replace(base_geometry, lead_routing=routing)
        basis = extract_field_basis(config, geometry)
        route_bases[routing] = basis
        high_v, return_v = solve_floating_potentials_v(
            basis.capacitance,
            drive_voltage_v,
        )
        state = _evaluate_state(basis, high_v, return_v, drive_voltage_v)
        route_sweep.append(
            {
                "lead_routing": routing,
                "basis_high_converged": basis.high_unit.converged,
                "basis_return_converged": basis.return_unit.converged,
                "basis_high_iterations": basis.high_unit.iterations,
                "basis_return_iterations": basis.return_unit.iterations,
                "capacitance": basis.capacitance.as_dict(),
                "floating_neutral": state,
            }
        )

    basis = route_bases["same_end"]
    capacitance = basis.capacitance
    grounded = _evaluate_state(basis, drive_voltage_v, 0.0, drive_voltage_v)
    bipolar = _evaluate_state(
        basis,
        0.5 * drive_voltage_v,
        -0.5 * drive_voltage_v,
        drive_voltage_v,
    )
    floating_high_v, floating_return_v = solve_floating_potentials_v(
        capacitance,
        drive_voltage_v,
    )
    floating = _evaluate_state(
        basis,
        floating_high_v,
        floating_return_v,
        drive_voltage_v,
    )

    terminal_capacitance_sweep: List[Dict[str, object]] = []
    common_capacitance_f = capacitance.device_common_capacitance_f
    for total_ratio in terminal_capacitance_total_ratios:
        total_external_f = total_ratio * common_capacitance_f
        for high_fraction in high_terminal_fractions:
            high_external_f = high_fraction * total_external_f
            return_external_f = (1.0 - high_fraction) * total_external_f
            high_v, return_v = solve_floating_potentials_v(
                capacitance,
                drive_voltage_v,
                high_external_capacitance_f=high_external_f,
                return_external_capacitance_f=return_external_f,
            )
            state = _evaluate_state(basis, high_v, return_v, drive_voltage_v)
            external_charge_c = high_external_f * high_v + return_external_f * return_v
            terminal_capacitance_sweep.append(
                {
                    "external_to_device_common_capacitance_ratio": total_ratio,
                    "high_terminal_fraction": high_fraction,
                    "high_external_capacitance_f": high_external_f,
                    "return_external_capacitance_f": return_external_f,
                    "external_charge_c": external_charge_c,
                    "assembly_charge_residual_c": state["matrix_charge"]["device_c"]
                    + external_charge_c,
                    **state,
                }
            )

    # At fixed differential voltage, leakage through conductances G_H and G_R
    # relaxes V_R toward -G_H*V_d/(G_H+G_R).  Time is normalized by the
    # corresponding common-mode RC constant.
    leakage_endpoint_sweep: List[Dict[str, object]] = []
    for name, high_fraction in (
        ("return_only", 0.0),
        ("symmetric", 0.5),
        ("high_only", 1.0),
    ):
        equilibrium_return_v = -high_fraction * drive_voltage_v
        equilibrium_high_v = equilibrium_return_v + drive_voltage_v
        state = _evaluate_state(
            basis,
            equilibrium_high_v,
            equilibrium_return_v,
            drive_voltage_v,
        )
        leakage_endpoint_sweep.append(
            {
                "leakage_path": name,
                "high_conductance_fraction": high_fraction,
                **state,
            }
        )

    return_leakage_sweep: List[Dict[str, object]] = []
    for time_over_tau in leakage_times_over_tau:
        return_v = floating_return_v * math.exp(-time_over_tau)
        high_v = return_v + drive_voltage_v
        state = _evaluate_state(basis, high_v, return_v, drive_voltage_v)
        return_leakage_sweep.append({"time_over_tau": time_over_tau, **state})

    refinement_specs = (
        (
            "coarse",
            Grid3DConfig(
                nx=33,
                ny=25,
                nz=21,
                cell_size_m=0.005,
                sor_omega=1.80,
            ),
            Apparatus3DGeometry(
                center_x=16,
                center_y=12,
                center_z=10,
                electrode_height_cells=11,
                electrode_depth_cells=5,
                blade_length_cells=2,
                closest_gap_cells=3,
                blade_offsets=(-3, 0, 3),
                lead_routing="same_end",
                lead_wall_clearance_cells=3,
            ),
        ),
        ("base", config, base_geometry),
        (
            "fine",
            Grid3DConfig(
                nx=55,
                ny=41,
                nz=36,
                cell_size_m=0.003,
                sor_omega=1.88,
                max_iterations=7_000,
            ),
            Apparatus3DGeometry(
                center_x=27,
                center_y=20,
                center_z=18,
                electrode_height_cells=17,
                electrode_depth_cells=9,
                blade_length_cells=4,
                closest_gap_cells=4,
                blade_offsets=(-5, 0, 5),
                lead_routing="same_end",
                lead_wall_clearance_cells=5,
            ),
        ),
    )
    refinement: List[Dict[str, object]] = []
    for name, refinement_config, refinement_geometry in refinement_specs:
        refinement_basis = (
            basis if name == "base" else extract_field_basis(refinement_config, refinement_geometry)
        )
        refinement_high_v, refinement_return_v = solve_floating_potentials_v(
            refinement_basis.capacitance,
            drive_voltage_v,
        )
        neutral_state = (
            floating
            if name == "base"
            else _evaluate_state(
                refinement_basis,
                refinement_high_v,
                refinement_return_v,
                drive_voltage_v,
            )
        )
        grounded_state = (
            grounded
            if name == "base"
            else _evaluate_state(
                refinement_basis,
                drive_voltage_v,
                0.0,
                drive_voltage_v,
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
            "description": "declared 3-D blade/flat apparatus with explicit lead stubs",
            "drive_voltage_v": drive_voltage_v,
            "boundary": "grounded rectangular chamber",
            "geometry_is_measured_cad": False,
            "force_method": "outer closed-surface Maxwell stress with chamber-pressure closure",
        },
        "config": asdict(config),
        "geometry": asdict(base_geometry),
        "topologies": {
            "grounded_return": grounded,
            "arbitrary_bipolar": bipolar,
            "floating_neutral": floating,
        },
        "lead_routing_sweep": route_sweep,
        "terminal_capacitance_sweep": terminal_capacitance_sweep,
        "leakage_endpoint_sweep": leakage_endpoint_sweep,
        "return_leakage_sweep": return_leakage_sweep,
        "grid_refinement": refinement,
    }


if __name__ == "__main__":
    print(json.dumps(run_apparatus_3d_suite(), indent=2, sort_keys=True))
