"""Geometry-aware electrostatic field run for the DET8 Exodus sandbox.

This module solves the two-dimensional Laplace equation for a transparent,
patent-like comb/blade electrode facing a flat return electrode inside a
grounded rectangular chamber. It then integrates conductor surface pressure

    p = epsilon_0 E_n^2 / 2

on the high electrode, return electrode, and chamber wall.

The geometry is a normalized surrogate because US 11,511,891 B2 does not
publish enough dimensions and field-map data to reconstruct the reported test
article. No result from this module is an Exodus or DET8 force prediction.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

from det8.models.exodus_simulation import EPSILON_0


DIELECTRIC = 0
HIGH_ELECTRODE = 1
RETURN_ELECTRODE = 2
CHAMBER = 3


@dataclass(frozen=True)
class FieldGridConfig:
    """Finite-difference grid and solver controls."""

    nx: int = 81
    ny: int = 61
    cell_size_m: float = 0.002
    sor_omega: float = 1.86
    tolerance: float = 2e-6
    max_iterations: int = 8_000

    def __post_init__(self) -> None:
        if self.nx < 25 or self.ny < 25:
            raise ValueError("Grid must be at least 25 x 25")
        if self.cell_size_m <= 0.0:
            raise ValueError("Cell size must be positive")
        if not 1.0 < self.sor_omega < 2.0:
            raise ValueError("SOR omega must lie between 1 and 2")
        if self.tolerance <= 0.0:
            raise ValueError("Tolerance must be positive")
        if self.max_iterations < 1:
            raise ValueError("Maximum iterations must be positive")


@dataclass(frozen=True)
class BladeFlatGeometry:
    """Grid-cell definition of the comb/blade and flat-return pair."""

    center_x: int
    center_y: int
    orientation: int = 1
    electrode_height_cells: int = 25
    blade_length_cells: int = 6
    closest_gap_cells: int = 5
    blade_offsets: tuple[int, ...] = (-8, 0, 8)
    high_potential_norm: float = 1.0
    return_potential_norm: float = 0.0

    def __post_init__(self) -> None:
        if self.orientation not in (-1, 1):
            raise ValueError("Orientation must be -1 or +1")
        if self.electrode_height_cells < 5:
            raise ValueError("Electrode height is too small")
        if self.blade_length_cells < 1 or self.closest_gap_cells < 2:
            raise ValueError("Blade length and gap must be positive")
        if self.high_potential_norm == self.return_potential_norm:
            raise ValueError("Electrodes must have different potentials")


@dataclass
class FieldSolution:
    """Converged normalized electrostatic potential."""

    config: FieldGridConfig
    geometry: BladeFlatGeometry
    potential: list[float]
    labels: list[int]
    fixed: list[bool]
    iterations: int
    max_delta: float
    converged: bool


def _index(x: int, y: int, nx: int) -> int:
    return y * nx + x


def _set_conductor_cell(
    x: int,
    y: int,
    label: int,
    value: float,
    config: FieldGridConfig,
    potential: list[float],
    labels: list[int],
    fixed: list[bool],
) -> None:
    if not (1 <= x < config.nx - 1 and 1 <= y < config.ny - 1):
        raise ValueError("Electrode intersects the chamber boundary")
    idx = _index(x, y, config.nx)
    if labels[idx] not in (DIELECTRIC, label):
        raise ValueError("Electrode geometry overlaps another conductor")
    potential[idx] = value
    labels[idx] = label
    fixed[idx] = True


def build_blade_flat_grid(
    config: FieldGridConfig,
    geometry: BladeFlatGeometry,
) -> tuple[list[float], list[int], list[bool]]:
    """Create normalized Dirichlet data for the chamber and electrodes."""

    count = config.nx * config.ny
    potential = [0.0] * count
    labels = [DIELECTRIC] * count
    fixed = [False] * count

    # The outer grounded chamber is a physical conductor, not merely a
    # numerical boundary. Its pressure is integrated after solving.
    for x in range(config.nx):
        for y in (0, config.ny - 1):
            idx = _index(x, y, config.nx)
            labels[idx] = CHAMBER
            fixed[idx] = True
    for y in range(config.ny):
        for x in (0, config.nx - 1):
            idx = _index(x, y, config.nx)
            labels[idx] = CHAMBER
            fixed[idx] = True

    device_span = geometry.blade_length_cells + geometry.closest_gap_cells
    half_span = device_span // 2
    high_x = geometry.center_x - geometry.orientation * half_span
    return_x = high_x + geometry.orientation * device_span
    half_height = geometry.electrode_height_cells // 2
    y_min = geometry.center_y - half_height
    y_max = geometry.center_y + half_height

    # High-voltage spine.
    for y in range(y_min, y_max + 1):
        _set_conductor_cell(
            high_x,
            y,
            HIGH_ELECTRODE,
            geometry.high_potential_norm,
            config,
            potential,
            labels,
            fixed,
        )

    # Three proximal blades attached to that spine and pointing toward the
    # flat return. This is intentionally simple and completely declared.
    for offset in geometry.blade_offsets:
        y = geometry.center_y + offset
        for step in range(geometry.blade_length_cells + 1):
            x = high_x + geometry.orientation * step
            _set_conductor_cell(
                x,
                y,
                HIGH_ELECTRODE,
                geometry.high_potential_norm,
                config,
                potential,
                labels,
                fixed,
            )

    # Flat grounded return electrode.
    for y in range(y_min, y_max + 1):
        _set_conductor_cell(
            return_x,
            y,
            RETURN_ELECTRODE,
            geometry.return_potential_norm,
            config,
            potential,
            labels,
            fixed,
        )

    return potential, labels, fixed


def solve_blade_flat_field(
    config: FieldGridConfig,
    geometry: BladeFlatGeometry,
) -> FieldSolution:
    """Solve Laplace's equation with red-black SOR."""

    potential, labels, fixed = build_blade_flat_grid(config, geometry)
    nx = config.nx
    ny = config.ny
    omega = config.sor_omega
    max_delta = math.inf

    for iteration in range(1, config.max_iterations + 1):
        max_delta = 0.0
        for parity in (0, 1):
            for y in range(1, ny - 1):
                x_start = 1 + ((parity - y) & 1)
                row = y * nx
                for x in range(x_start, nx - 1, 2):
                    idx = row + x
                    if fixed[idx]:
                        continue
                    average = 0.25 * (
                        potential[idx - 1]
                        + potential[idx + 1]
                        + potential[idx - nx]
                        + potential[idx + nx]
                    )
                    old = potential[idx]
                    new = old + omega * (average - old)
                    potential[idx] = new
                    delta = abs(new - old)
                    if delta > max_delta:
                        max_delta = delta
        if max_delta < config.tolerance:
            return FieldSolution(
                config=config,
                geometry=geometry,
                potential=potential,
                labels=labels,
                fixed=fixed,
                iterations=iteration,
                max_delta=max_delta,
                converged=True,
            )

    return FieldSolution(
        config=config,
        geometry=geometry,
        potential=potential,
        labels=labels,
        fixed=fixed,
        iterations=config.max_iterations,
        max_delta=max_delta,
        converged=False,
    )


def _electric_field_at(
    solution: FieldSolution,
    x: int,
    y: int,
    voltage_v: float,
) -> tuple[float, float]:
    """Central-difference electric field at a dielectric grid point."""

    nx = solution.config.nx
    h = solution.config.cell_size_m
    idx = _index(x, y, nx)
    ex = -(
        solution.potential[idx + 1] - solution.potential[idx - 1]
    ) * voltage_v / (2.0 * h)
    ey = -(
        solution.potential[idx + nx] - solution.potential[idx - nx]
    ) * voltage_v / (2.0 * h)
    return ex, ey


def _stress_traction(
    ex: float,
    ey: float,
    normal_x: float,
    normal_y: float,
) -> tuple[float, float]:
    """Return T dot n for the electrostatic Maxwell stress tensor."""

    t_xx = 0.5 * EPSILON_0 * (ex**2 - ey**2)
    t_yy = 0.5 * EPSILON_0 * (ey**2 - ex**2)
    t_xy = EPSILON_0 * ex * ey
    return (
        t_xx * normal_x + t_xy * normal_y,
        t_xy * normal_x + t_yy * normal_y,
    )


def _maxwell_force_on_contour(
    solution: FieldSolution,
    x_left: int,
    x_right: int,
    y_bottom: int,
    y_top: int,
    voltage_v: float,
    extrusion_depth_m: float,
) -> tuple[float, float]:
    """Integrate T dot n around a dielectric rectangular contour."""

    nx = solution.config.nx
    ny = solution.config.ny
    if not (1 <= x_left < x_right <= nx - 2):
        raise ValueError("Stress contour has invalid horizontal bounds")
    if not (1 <= y_bottom < y_top <= ny - 2):
        raise ValueError("Stress contour has invalid vertical bounds")

    edge_area = solution.config.cell_size_m * extrusion_depth_m
    force_x = 0.0
    force_y = 0.0

    # Vertical sides. Exclude corner nodes here; horizontal sides include them.
    for y in range(y_bottom + 1, y_top):
        for x, normal_x in ((x_left, -1.0), (x_right, 1.0)):
            ex, ey = _electric_field_at(solution, x, y, voltage_v)
            tx, ty = _stress_traction(ex, ey, normal_x, 0.0)
            force_x += tx * edge_area
            force_y += ty * edge_area

    for x in range(x_left, x_right + 1):
        for y, normal_y in ((y_bottom, -1.0), (y_top, 1.0)):
            ex, ey = _electric_field_at(solution, x, y, voltage_v)
            tx, ty = _stress_traction(ex, ey, 0.0, normal_y)
            force_x += tx * edge_area
            force_y += ty * edge_area

    return force_x, force_y


def _geometry_bounds(
    geometry: BladeFlatGeometry,
) -> dict[str, tuple[int, int, int, int]]:
    device_span = geometry.blade_length_cells + geometry.closest_gap_cells
    half_span = device_span // 2
    high_x = geometry.center_x - geometry.orientation * half_span
    return_x = high_x + geometry.orientation * device_span
    blade_end_x = high_x + geometry.orientation * geometry.blade_length_cells
    half_height = geometry.electrode_height_cells // 2
    y_min = geometry.center_y - half_height
    y_max = geometry.center_y + half_height
    high_bounds = (
        min(high_x, blade_end_x),
        max(high_x, blade_end_x),
        y_min,
        y_max,
    )
    return_bounds = (return_x, return_x, y_min, y_max)
    device_bounds = (
        min(high_bounds[0], return_x),
        max(high_bounds[1], return_x),
        y_min,
        y_max,
    )
    return {
        "high": high_bounds,
        "return": return_bounds,
        "device": device_bounds,
    }


def _expanded_contour(
    bounds: tuple[int, int, int, int],
    margin: int,
) -> tuple[int, int, int, int]:
    x_min, x_max, y_min, y_max = bounds
    return (
        x_min - margin,
        x_max + margin,
        y_min - margin,
        y_max + margin,
    )


def _direct_chamber_pressure(
    solution: FieldSolution,
    voltage_v: float,
    extrusion_depth_m: float,
) -> tuple[float, float]:
    """Independently integrate normal electric pressure on the chamber."""

    config = solution.config
    nx = config.nx
    ny = config.ny
    h = config.cell_size_m
    edge_area = h * extrusion_depth_m
    force_x = 0.0
    force_y = 0.0

    for y in range(1, ny - 1):
        for boundary_x, neighbor_x, normal_x in (
            (0, 1, 1.0),
            (nx - 1, nx - 2, -1.0),
        ):
            boundary = _index(boundary_x, y, nx)
            neighbor = _index(neighbor_x, y, nx)
            normal_field = (
                (solution.potential[boundary] - solution.potential[neighbor])
                * voltage_v
                / h
            )
            pressure = 0.5 * EPSILON_0 * normal_field**2
            force_x += pressure * edge_area * normal_x

    for x in range(1, nx - 1):
        for boundary_y, neighbor_y, normal_y in (
            (0, 1, 1.0),
            (ny - 1, ny - 2, -1.0),
        ):
            boundary = _index(x, boundary_y, nx)
            neighbor = _index(x, neighbor_y, nx)
            normal_field = (
                (solution.potential[boundary] - solution.potential[neighbor])
                * voltage_v
                / h
            )
            pressure = 0.5 * EPSILON_0 * normal_field**2
            force_y += pressure * edge_area * normal_y

    return force_x, force_y


def maxwell_pressure_ledger(
    solution: FieldSolution,
    voltage_v: float = 40_000.0,
    extrusion_depth_m: float = 0.01,
) -> dict:
    """Integrate Maxwell stress on nested closed dielectric contours.

    Separate contours enclose the high electrode and return electrode. Their
    sum is compared with a contour enclosing the complete device. A second,
    chamber-adjacent contour transports the net device force through the
    charge-free dielectric, while normal pressure is integrated independently
    on the grounded chamber. Their sum tests global closure.
    """

    if voltage_v == 0.0:
        voltage_v = 0.0
    if extrusion_depth_m <= 0.0:
        raise ValueError("Extrusion depth must be positive")

    bounds = _geometry_bounds(solution.geometry)
    high = _maxwell_force_on_contour(
        solution,
        *_expanded_contour(bounds["high"], 2),
        voltage_v,
        extrusion_depth_m,
    )
    return_electrode = _maxwell_force_on_contour(
        solution,
        *_expanded_contour(bounds["return"], 2),
        voltage_v,
        extrusion_depth_m,
    )
    separate_sum = (
        high[0] + return_electrode[0],
        high[1] + return_electrode[1],
    )
    inner_device = _maxwell_force_on_contour(
        solution,
        *_expanded_contour(bounds["device"], 3),
        voltage_v,
        extrusion_depth_m,
    )
    transported = _maxwell_force_on_contour(
        solution,
        2,
        solution.config.nx - 3,
        2,
        solution.config.ny - 3,
        voltage_v,
        extrusion_depth_m,
    )
    # The outer contour is the most stable device-force evaluation on a
    # stair-step grid: it transports the net Maxwell stress through a broad
    # charge-free region. Chamber pressure is integrated independently at the
    # grounded wall, so their agreement is a nontrivial closure check.
    device = transported
    chamber = _direct_chamber_pressure(
        solution, voltage_v, extrusion_depth_m
    )
    residual = (device[0] + chamber[0], device[1] + chamber[1])
    total_absolute = math.hypot(*device) + math.hypot(*chamber)
    residual_norm = math.hypot(*residual)
    return {
        "voltage_v": voltage_v,
        "extrusion_depth_m": extrusion_depth_m,
        "high_electrode_force_n": {"x": high[0], "y": high[1]},
        "return_electrode_force_n": {
            "x": return_electrode[0],
            "y": return_electrode[1],
        },
        "separate_electrode_sum_n": {
            "x": separate_sum[0],
            "y": separate_sum[1],
        },
        "inner_device_contour_diagnostic_n": {
            "x": inner_device[0],
            "y": inner_device[1],
        },
        "device_force_n": {"x": device[0], "y": device[1]},
        "outer_transported_force_n": {
            "x": transported[0],
            "y": transported[1],
        },
        "chamber_force_n": {"x": chamber[0], "y": chamber[1]},
        "global_residual_n": {"x": residual[0], "y": residual[1]},
        "relative_closure_error": (
            residual_norm / total_absolute if total_absolute > 0.0 else 0.0
        ),
    }


def run_field_case(
    config: FieldGridConfig,
    geometry: BladeFlatGeometry,
    voltage_v: float = 40_000.0,
    extrusion_depth_m: float = 0.01,
) -> dict:
    solution = solve_blade_flat_field(config, geometry)
    ledger = maxwell_pressure_ledger(solution, voltage_v, extrusion_depth_m)
    return {
        "config": asdict(config),
        "geometry": asdict(geometry),
        "solver": {
            "iterations": solution.iterations,
            "max_delta": solution.max_delta,
            "converged": solution.converged,
        },
        "ledger": ledger,
    }


def run_field_suite() -> dict:
    """Run translation, reversal, chamber-size, and voltage discriminators."""

    base_config = FieldGridConfig()
    center_y = base_config.ny // 2
    translated_cases = []
    base_solution: FieldSolution | None = None
    for center_x in (21, 30, 40, 50, 59):
        geometry = BladeFlatGeometry(center_x=center_x, center_y=center_y)
        solution = solve_blade_flat_field(base_config, geometry)
        if center_x == 40:
            base_solution = solution
        translated_cases.append(
            {
                "center_x": center_x,
                "center_x_m": center_x * base_config.cell_size_m,
                "solver_iterations": solution.iterations,
                "converged": solution.converged,
                "ledger": maxwell_pressure_ledger(solution),
            }
        )

    if base_solution is None:  # pragma: no cover - fixed sweep contains center.
        raise RuntimeError("Centered field solution was not generated")

    reversed_geometry = BladeFlatGeometry(
        center_x=40,
        center_y=center_y,
        orientation=-1,
    )
    reversed_solution = solve_blade_flat_field(base_config, reversed_geometry)

    chamber_size_cases = []
    for nx, ny in ((61, 51), (81, 61), (101, 71)):
        if nx == 81 and ny == 61:
            solution = base_solution
            config = base_config
        else:
            config = FieldGridConfig(nx=nx, ny=ny)
            geometry = BladeFlatGeometry(
                center_x=nx // 2,
                center_y=ny // 2,
            )
            solution = solve_blade_flat_field(config, geometry)
        chamber_size_cases.append(
            {
                "chamber_width_m": (nx - 1) * config.cell_size_m,
                "chamber_height_m": (ny - 1) * config.cell_size_m,
                "solver_iterations": solution.iterations,
                "converged": solution.converged,
                "ledger": maxwell_pressure_ledger(solution),
            }
        )

    voltage_scaling = [
        maxwell_pressure_ledger(base_solution, voltage_v=voltage)
        for voltage in (20_000.0, 40_000.0, 60_000.0)
    ]

    source_topology_cases = []
    for name, common_mode in (
        ("high_at_chamber_ground", -1.0),
        ("bipolar", -0.5),
        ("return_at_chamber_ground", 0.0),
        ("positive_common_mode", 0.5),
    ):
        if common_mode == 0.0:
            solution = base_solution
        else:
            geometry = BladeFlatGeometry(
                center_x=40,
                center_y=30,
                high_potential_norm=1.0 + common_mode,
                return_potential_norm=common_mode,
            )
            solution = solve_blade_flat_field(base_config, geometry)
        source_topology_cases.append(
            {
                "name": name,
                "high_potential_norm": 1.0 + common_mode,
                "return_potential_norm": common_mode,
                "differential_potential_norm": 1.0,
                "solver_iterations": solution.iterations,
                "converged": solution.converged,
                "ledger": maxwell_pressure_ledger(solution),
            }
        )

    refinement_specs = (
        (
            "coarse",
            FieldGridConfig(
                nx=41,
                ny=31,
                cell_size_m=0.004,
                sor_omega=1.75,
            ),
            BladeFlatGeometry(
                center_x=20,
                center_y=15,
                electrode_height_cells=13,
                blade_length_cells=3,
                closest_gap_cells=3,
                blade_offsets=(-4, 0, 4),
            ),
        ),
        ("base", base_config, BladeFlatGeometry(center_x=40, center_y=30)),
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
    refinement_cases = []
    for name, config, geometry in refinement_specs:
        if name == "base":
            solution = base_solution
        else:
            solution = solve_blade_flat_field(config, geometry)
        bipolar_geometry = BladeFlatGeometry(
            center_x=geometry.center_x,
            center_y=geometry.center_y,
            orientation=geometry.orientation,
            electrode_height_cells=geometry.electrode_height_cells,
            blade_length_cells=geometry.blade_length_cells,
            closest_gap_cells=geometry.closest_gap_cells,
            blade_offsets=geometry.blade_offsets,
            high_potential_norm=0.5,
            return_potential_norm=-0.5,
        )
        bipolar_solution = solve_blade_flat_field(config, bipolar_geometry)
        refinement_cases.append(
            {
                "name": name,
                "cell_size_m": config.cell_size_m,
                "solver_iterations": solution.iterations,
                "converged": solution.converged,
                "ledger": maxwell_pressure_ledger(solution),
                "bipolar_solver_iterations": bipolar_solution.iterations,
                "bipolar_converged": bipolar_solution.converged,
                "bipolar_ledger": maxwell_pressure_ledger(bipolar_solution),
            }
        )

    return {
        "status": "normalized blade/flat field surrogate; actual CAD still required",
        "geometry_note": (
            "Three one-cell blades on a high-voltage spine face a flat grounded "
            "return inside a grounded rectangular chamber."
        ),
        "base_config": asdict(base_config),
        "translation_sweep": translated_cases,
        "orientation_reversal": {
            "forward": maxwell_pressure_ledger(base_solution),
            "reversed": maxwell_pressure_ledger(reversed_solution),
        },
        "chamber_size_sweep": chamber_size_cases,
        "voltage_scaling": voltage_scaling,
        "source_topology_sweep": source_topology_cases,
        "grid_refinement": refinement_cases,
    }


def main() -> None:
    print(json.dumps(run_field_suite(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
