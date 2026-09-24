#!/usr/bin/env python3
"""Qualify the frozen RI-42 operations using synthetic arrays only.

No observed data, HDF5 files, output files, plotting, or network operations
are used. Numerical gates produce JSON on stdout and a nonzero exit status
on failure. Structural and runtime violations raise explicit exceptions.
"""

from decimal import Decimal, ROUND_HALF_EVEN, localcontext
import hashlib
import importlib.util
import inspect
import json
from pathlib import Path
import platform
import sys

import h5py
import numpy as np
import scipy


FS = 4096.0
LENGTH = 2048
NOTCHES = (
    (14.0, 1.0, 0.1), (34.70, 1.0, 0.1), (35.30, 1.0, 0.1),
    (35.90, 1.0, 0.1), (36.70, 1.0, 0.1), (37.30, 1.0, 0.1),
    (40.95, 1.0, 0.1), (60.0, 1.0, 0.1), (120.0, 1.0, 0.1),
    (179.99, 1.0, 0.1), (304.99, 1.0, 0.1), (331.49, 1.0, 0.1),
    (510.02, 1.0, 0.1), (1009.99, 1.0, 0.1),
    (510.0, 200.0, 20.0), (331.5, 10.0, 1.0),
)
TONE_FREQUENCIES = (
    0.0, 10.0, 43.0, 60.0, 100.0, 120.0,
    179.99, 260.0, 331.5, 510.0, 1009.99, 1500.0,
)
VERSION_PINS = {
    "python": "3.11.6", "numpy": "2.1.3",
    "scipy": "1.14.1", "h5py": "3.12.1",
}
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(payload):
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def array_identity(values):
    require(isinstance(values, np.ndarray) and values.dtype == np.dtype("float64"),
            "array identity requires a NumPy binary64 array")
    payload = np.ascontiguousarray(values, dtype="<f8").tobytes(order="C")
    return {"shape": list(values.shape), "dtype": "little-endian binary64",
            "order": "C", "bytes": len(payload), "sha256": sha256(payload)}


def runtime_identity():
    versions = {"python": platform.python_version(), "numpy": np.__version__,
                "scipy": scipy.__version__, "h5py": h5py.__version__}
    require(platform.python_implementation() == "CPython", "CPython is required")
    require(versions == VERSION_PINS, f"runtime version mismatch: {versions}")
    configuration = np.show_config(mode="dicts")
    require(type(configuration) is dict, "NumPy configuration must be a dictionary")
    return {
        "versions": versions, "required_versions": VERSION_PINS,
        "python_implementation": platform.python_implementation(),
        "python_build": sys.version,
        "operating_system": platform.system(), "os_release": platform.release(),
        "os_version": platform.version(), "machine": platform.machine(),
        "byte_order": sys.byteorder,
        "hdf5_version": h5py.version.hdf5_version,
        "numpy_configuration": configuration,
        "h5py_usage": "Imported for version metadata only; no HDF5 file is opened",
    }


def load_neighbor(name):
    """Execute the exact bytes whose digest is reported, without pyc writes."""
    path = Path(__file__).resolve().with_name(name + ".py")
    payload = path.read_bytes()
    module_name = "ri44_qualification_" + name
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(specification is not None and specification.loader is not None,
            f"cannot create module specification for {name}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module, {"filename": path.name, "bytes": len(payload),
                    "sha256": sha256(payload)}


def expected_specs():
    result = [{"function": "butter", "N": 4, "Wn": [43.0, 260.0],
               "btype": "bandpass", "analog": False, "fs": FS}]
    for center, half_pass, half_stop in NOTCHES:
        result.append({
            "function": "iirdesign",
            "wp": [center - half_pass, center + half_pass],
            "ws": [center - half_stop, center + half_stop],
            "gpass": 1.0, "gstop": 6.0, "analog": False,
            "ftype": "ellip", "fs": FS,
        })
    return result


def validate_stages(stages):
    require(type(stages) is list and len(stages) == 17, "expected 17 ordered stages")
    for index, (stage, specification) in enumerate(zip(stages, expected_specs())):
        require(type(stage) is dict and stage["index"] == index,
                "stage index or structure mismatch")
        require(canonical_json(stage["spec"]) == canonical_json(specification),
                f"stage {index}: design specification differs from RI-42")
        sos = stage["sos"]
        require(isinstance(sos, np.ndarray) and sos.dtype == np.dtype("float64")
                and sos.ndim == 2 and sos.shape[0] > 0 and sos.shape[1] == 6,
                f"stage {index}: invalid SOS array")
        require(bool(np.isfinite(sos).all()), f"stage {index}: nonfinite coefficient")
        require(bool(np.all(sos[:, 3] == 1.0)), f"stage {index}: a0 is not one")
        expected_padding = 3 * (2 * len(sos) + 1 - min(
            int(np.count_nonzero(sos[:, 2] == 0.0)),
            int(np.count_nonzero(sos[:, 5] == 0.0))))
        require(type(stage["padlen"]) is int and stage["padlen"] == expected_padding
                and 0 <= stage["padlen"] < LENGTH - 1,
                f"stage {index}: padding mismatch")
        for key in ("z", "p"):
            roots = np.asarray(stage[key])
            require(roots.ndim == 1 and bool(np.isfinite(roots).all()),
                    f"stage {index}: invalid {key} roots")
        require(bool(np.isfinite(stage["k"])), f"stage {index}: nonfinite ZPK gain")
        if index == 0:
            require(sos.shape == (4, 6) and len(stage["p"]) == 8,
                    "bandpass must have four sections and order eight")


def verify_manifest(stages, manifest):
    require(type(manifest) is dict and set(manifest) == {"schema_version", "stages"},
            "coefficient manifest schema mismatch")
    require(type(manifest["schema_version"]) is str and manifest["schema_version"],
            "missing coefficient manifest schema version")
    require(type(manifest["stages"]) is list and len(manifest["stages"]) == 17,
            "coefficient manifest must retain 17 stages")
    for stage, entry in zip(stages, manifest["stages"]):
        expected = {
            "index": stage["index"], "spec": stage["spec"],
            "shape": list(stage["sos"].shape),
            "coefficient_hex": [[float(value).hex() for value in row]
                                for row in stage["sos"]],
            "matrix_sha256": array_identity(stage["sos"])["sha256"],
            "padlen": stage["padlen"],
        }
        require(canonical_json(entry) == canonical_json(expected),
                f"stage {stage['index']}: coefficient manifest differs from actual matrix")
    return sha256(canonical_json(manifest))


def float_gate(residual, tolerance, *, strict=False):
    measured = float(residual)
    finite = bool(np.isfinite(measured))
    passed = finite and (measured < tolerance if strict else measured <= tolerance)
    return {
        "residual": measured if finite else str(measured),
        "residual_hex": measured.hex(), "finite": finite,
        "tolerance": float(tolerance), "tolerance_hex": float(tolerance).hex(),
        "comparison": "<" if strict else "<=", "passed": bool(passed),
    }


def direct_responses(stage, frequencies):
    """Evaluate two representations without SciPy frequency helpers."""
    z = np.exp(2j * np.pi * frequencies / FS)
    numerator = np.full(z.shape, complex(stage["k"]), dtype=np.complex128)
    denominator = np.ones(z.shape, dtype=np.complex128)
    for zero in stage["z"]:
        numerator *= z - zero
    for pole in stage["p"]:
        denominator *= z - pole
    zpk_response = numerator / denominator
    inverse = 1.0 / z
    inverse_squared = inverse * inverse
    sos_response = np.ones(z.shape, dtype=np.complex128)
    for b0, b1, b2, a0, a1, a2 in stage["sos"]:
        sos_response *= ((b0 + b1 * inverse + b2 * inverse_squared)
                         / (a0 + a1 * inverse + a2 * inverse_squared))
    return zpk_response, sos_response


def frequency_grid():
    points = {float(j) / 16.0 for j in range(32769)}
    points.update((43.0, 260.0))
    for center, half_pass, half_stop in NOTCHES:
        points.update((center, center - half_pass, center + half_pass,
                       center - half_stop, center + half_stop))
    return np.asarray(sorted(points), dtype=np.float64)


def dc_gain_record(sos):
    with localcontext() as context:
        context.prec = 80
        context.rounding = ROUND_HALF_EVEN
        section_gains = []
        stage_gain = Decimal(1)
        for row in sos:
            b0, b1, b2, a0, a1, a2 = [Decimal.from_float(float(x)) for x in row]
            denominator = a0 + a1 + a2
            require(denominator != 0, "zero DC denominator")
            gain = (b0 + b1 + b2) / denominator
            section_gains.append(str(gain))
            stage_gain *= gain
        return {"section_gains_decimal80": section_gains,
                "one_pass_stage_gain_decimal80": str(stage_gain),
                "forward_backward_stage_gain_decimal80": str(stage_gain * stage_gain)}


def frequency_checks(stages):
    frequencies = frequency_grid()
    zpk_gain = np.ones(len(frequencies), dtype=np.float64)
    sos_gain = np.ones(len(frequencies), dtype=np.float64)
    records = []
    for stage in stages:
        zpk, sos = direct_responses(stage, frequencies)
        sos_poles = np.concatenate([np.roots(row[3:]) for row in stage["sos"]])
        residuals = np.abs(zpk - sos)
        at = int(np.argmax(residuals))
        response_gate = float_gate(np.max(residuals), 1e-8)
        response_gate.update({"frequency_hz_at_maximum": float(frequencies[at]),
                              "frequency_hex_at_maximum": float(frequencies[at]).hex()})
        records.append({
            "index": stage["index"], "spec": stage["spec"],
            "one_pass_order": len(stage["p"]), "sos_sections": len(stage["sos"]),
            "padlen": stage["padlen"],
            "zpk_pole_radius": float_gate(np.max(np.abs(stage["p"])), 1.0, strict=True),
            "sos_pole_radius": float_gate(np.max(np.abs(sos_poles)), 1.0, strict=True),
            "coefficient_finiteness_and_unit_a0_verified": True,
            "dc_gains": dc_gain_record(stage["sos"]),
            "complex_response_gate": response_gate,
        })
        zpk_gain *= np.abs(zpk) ** 2
        sos_gain *= np.abs(sos) ** 2
    residuals = np.abs(zpk_gain - sos_gain)
    at = int(np.argmax(residuals))
    cascade = float_gate(np.max(residuals), 1e-8)
    cascade.update({"frequency_hz_at_maximum": float(frequencies[at]),
                    "frequency_hex_at_maximum": float(frequencies[at]).hex()})
    return {
        "grid_identity": array_identity(frequencies), "grid_count": len(frequencies),
        "grid_rule": "sorted binary64 union: j/16 for 0<=j<=32768; 43,260; notch centers and four edges",
        "stage_checks": records, "cascade_real_gain_gate": cascade,
        "design_independence_limit": "Separate ZPK and SOS designs share SciPy's design implementation",
    }


def short_fixtures():
    index = np.arange(LENGTH, dtype=np.float64)
    times = index / FS
    impulse = np.zeros(LENGTH, dtype=np.float64)
    impulse[1024] = 1.0
    mixed = (np.sin(2.0 * np.pi * 40.0 * times)
             + np.cos(2.0 * np.pi * 60.0 * times)
             + np.sin(2.0 * np.pi * 100.0 * times)
             + np.cos(2.0 * np.pi * 300.0 * times)) / 4.0
    return [
        ("zeros", np.zeros(LENGTH, dtype=np.float64)),
        ("ones", np.ones(LENGTH, dtype=np.float64)),
        ("ramp", 2.0 * index / (LENGTH - 1) - 1.0),
        ("impulse_at_1024", impulse), ("four_frequency_mixture", mixed),
    ]


def filtered_copy(production, values, stages):
    before = array_identity(values)
    result = production.apply_filter(values, stages)
    require(array_identity(values) == before, "production filtering mutated its input")
    require(isinstance(result, np.ndarray) and result.dtype == np.dtype("float64")
            and result.shape == values.shape and not np.shares_memory(result, values),
            "production filter must return a new binary64 array of unchanged shape")
    require(bool(np.isfinite(result).all()), "production filter returned nonfinite samples")
    return result


def recurrence_checks(production, reference, stages):
    sos_stages = [stage["sos"].tolist() for stage in stages]
    padlens = [stage["padlen"] for stage in stages]
    results = []
    for name, values in short_fixtures():
        actual = filtered_copy(production, values, stages)
        expected = reference.reference_filter(values.tolist(), sos_stages, padlens)
        require(type(expected) is list and len(expected) == LENGTH
                and all(type(value) is Decimal and value.is_finite() for value in expected),
                "reference must return the complete finite Decimal output")
        with localcontext() as context:
            context.prec = 80
            context.rounding = ROUND_HALF_EVEN
            differences = [abs(Decimal.from_float(float(value)) - exact)
                           for value, exact in zip(actual, expected)]
            maximum = max(differences)
            scale = max(1.0, float(np.max(np.abs(values))))
            tolerance = Decimal.from_float(scale) * Decimal("1e-9")
        results.append({
            "fixture": name, "input_identity": array_identity(values),
            "production_output_identity": array_identity(actual),
            "comparison_sample_count": LENGTH,
            "maximum_absolute_difference_decimal": str(maximum),
            "index_at_maximum": differences.index(maximum),
            "input_scale_hex": scale.hex(), "tolerance_decimal": str(tolerance),
            "comparison": "<=", "passed": maximum <= tolerance,
        })
    return {
        "reference_arithmetic": "80 significant Decimal digits; ROUND_HALF_EVEN; binary64 values converted exactly",
        "comparison": "Decimal.from_float(production output) minus unrounded Decimal reference at every sample",
        "fixtures": results,
    }


def tone_checks(production, stages):
    times = np.arange(524288, dtype=np.float64) / FS - 64.0
    results = []
    for frequency in TONE_FREQUENCIES:
        direct_gain = 1.0
        for stage in stages:
            zpk, _ = direct_responses(stage, np.asarray([frequency], dtype=np.float64))
            direct_gain *= float(np.abs(zpk[0]) ** 2)
        require(bool(np.isfinite(direct_gain)), "nonfinite tone reference gain")
        for phase_label, phase in (("zero", 0.0), ("pi_over_3", np.pi / 3.0)):
            full_input = np.sin(2.0 * np.pi * frequency * times + phase)
            short_input = full_input[196608:327680]
            full_output = filtered_copy(production, full_input, stages)
            short_output = filtered_copy(production, short_input, stages)
            full_crop = full_output[262144:266240]
            short_crop = short_output[65536:69632]
            input_crop = short_input[65536:69632]
            context_gate = float_gate(np.max(np.abs(short_crop - full_crop)), 1e-3)
            gain_gate = float_gate(np.max(np.abs(short_crop - direct_gain * input_crop)), 1e-3)
            results.append({
                "frequency_hz": frequency, "frequency_hex": frequency.hex(),
                "phase": phase_label, "phase_radians_hex": float(phase).hex(),
                "input_128s_identity": array_identity(full_input),
                "input_32s_identity": array_identity(short_input),
                "input_32s_source_slice": [196608, 327680],
                "output_32s_crop": [65536, 69632],
                "output_128s_crop": [262144, 266240],
                "crop_sample_count": 4096,
                "output_32s_crop_identity": array_identity(short_crop),
                "output_128s_crop_identity": array_identity(full_crop),
                "zpk_forward_backward_cascade_gain": direct_gain,
                "zpk_forward_backward_cascade_gain_hex": direct_gain.hex(),
                "context_gate": context_gate, "tone_gain_gate": gain_gate,
            })
    require(len(results) == 24, "tone inventory changed")
    return results


def main():
    require(not sys.argv[1:], "run_checks.py accepts no arguments")
    runtime = runtime_identity()
    production, production_identity = load_neighbor("filtering")
    reference, reference_identity = load_neighbor("reference")
    own_bytes = Path(__file__).read_bytes()
    stages = production.design_stages()
    validate_stages(stages)
    manifest = production.coefficient_manifest(stages)
    manifest_sha256 = verify_manifest(stages, manifest)
    frequency = frequency_checks(stages)
    recurrence = recurrence_checks(production, reference, stages)
    tones = tone_checks(production, stages)
    require(verify_manifest(stages, production.coefficient_manifest(stages)) == manifest_sha256,
            "synthetic filtering changed the stage coefficient identity")
    gates = [item[key]["passed"] for item in frequency["stage_checks"]
             for key in ("zpk_pole_radius", "sos_pole_radius")]
    gates.extend(item["complex_response_gate"]["passed"] for item in frequency["stage_checks"])
    gates.append(frequency["cascade_real_gain_gate"]["passed"])
    gates.extend(item["passed"] for item in recurrence["fixtures"])
    gates.extend(item[key]["passed"] for item in tones for key in ("context_gate", "tone_gain_gate"))
    passed = all(gates)
    report = {
        "schema_version": "ri44-synthetic-qualification-v1",
        "status": "all_synthetic_gates_passed" if passed else "synthetic_qualification_failed",
        "gate_counts": {"total": len(gates), "passed": sum(gates), "failed": len(gates) - sum(gates)},
        "runtime": runtime,
        "source_identity": {
            "filtering": production_identity, "reference": reference_identity,
            "runner": {"filename": "run_checks.py", "bytes": len(own_bytes), "sha256": sha256(own_bytes)},
            "accepted_recipe_sha256": RECIPE_SHA256,
        },
        "api_identity": {
            "filtering": {name: str(inspect.signature(getattr(production, name)))
                          for name in ("design_stages", "apply_filter", "coefficient_manifest")},
            "reference": {"reference_filter": str(inspect.signature(reference.reference_filter))},
            "loading": "Explicit neighboring importlib specifications; executed and hashed source bytes are identical",
        },
        "coefficient_manifest": manifest, "coefficient_manifest_sha256": manifest_sha256,
        "coefficient_manifest_hash_convention": "ASCII JSON; sorted keys; ensure_ascii=True; separators=(',',':'); no newline",
        "frequency_checks": frequency, "recurrence_checks": recurrence, "tone_checks": tones,
        "scope": {
            "observed_data_reads": False,
            "operations": "Synthetic qualification only; no strain input, calibration correction, plot, fit or inference",
            "boundary": "Declared-fixture discrepancies do not give a uniform arbitrary-signal error bound or establish physical continuation",
            "normal_optimized_comparison": "Compare complete stdout bytes from separate normal and -O invocations",
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
