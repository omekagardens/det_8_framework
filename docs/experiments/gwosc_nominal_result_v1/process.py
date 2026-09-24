#!/usr/bin/env python3
"""Consume the admitted RI-42/44 operations for the fixed public V2 pair.

Write only CROP.json and PROCESSING_REPORT.json to a new external directory.
All published dependencies, the admitted runtime and the actual coefficient
manifest are checked before the two input snapshots are read. Those same
retained snapshots supply both the RI-37 inspection and the sample arrays.
"""

import argparse
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import platform
import stat
import sys

import h5py
import numpy as np
import scipy


RATE = 4096
SOURCE_COUNT = 131072
SOURCE_GPS = 1126259446
CROP_START = 65536
CROP_STOP = 69632
CROP_COUNT = CROP_STOP - CROP_START
TIME_ORIGIN = 1126259462
MANIFEST_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"
DEPENDENCIES = {
    "input_inspector": {
        "path": "gwosc_input_qualification_v1/inspect_inputs.py", "bytes": 14817,
        "sha256": "bdafb9c694fc9f33071072f1a2fc027bdb85e9262245ad3f9e29f860935d142a",
    },
    "input_qualification": {
        "path": "gwosc_input_qualification_v1/INPUT_REPORT.json", "bytes": 31096,
        "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80",
    },
    "filtering": {
        "path": "gwosc_nominal_processing_v1/filtering.py", "bytes": 8805,
        "sha256": "9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be",
    },
    "coefficients": {
        "path": "gwosc_nominal_processing_v1/COEFFICIENTS.json", "bytes": 7698,
        "sha256": MANIFEST_SHA256,
    },
    "synthetic_qualification": {
        "path": "gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json", "bytes": 107468,
        "sha256": "2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3",
    },
    "recipe": {
        "path": "gwosc_nominal_display_v1/RECIPE.md", "bytes": 14014,
        "sha256": RECIPE_SHA256,
    },
}
ANNOTATION_SHA256 = {
    "H1": "da67bb7ba8e4bd7638cb04872e0f52dec06531099dbf1e3db6d25f3c5db337d2",
    "L1": "109d1ffec046b36e7fab31811fc6240b40f92250a47dc16c3359482869335515",
}
CW_ANNOTATION = {
    "H1": "H1 NO_CW_HW_INJ flag is set throughout input interval.",
    "L1": (
        "L1 NO_CW_HW_INJ flag is clear throughout input interval; samples retained. "
        "Injection absence and negligible effect are not claimed."
    ),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(payload):
    return hashlib.sha256(payload).hexdigest()


def canonical_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii")


def export_json(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def file_identity(payload):
    return {"bytes": len(payload), "sha256": digest(payload)}


def array_identity(values):
    require(type(values) is np.ndarray and values.dtype == np.dtype("float64"),
            "array identity requires NumPy binary64")
    payload = np.ascontiguousarray(values, dtype="<f8").tobytes(order="C")
    return {"shape": list(values.shape), "dtype": "little-endian binary64",
            "order": "C", "bytes": len(payload), "sha256": digest(payload)}


def pinned_dependencies():
    """Verify all six bodies before parsing JSON or executing either source."""
    base = Path(__file__).resolve().parent.parent
    payloads = {}
    for name, pin in DEPENDENCIES.items():
        path = base / pin["path"]
        try:
            information = path.lstat()
            require(stat.S_ISREG(information.st_mode),
                    f"{pin['path']}: expected a regular dependency file")
            require(information.st_size == pin["bytes"],
                    f"{pin['path']}: published byte count changed")
            with path.open("rb") as stream:
                payload = stream.read(pin["bytes"] + 1)
        except OSError as error:
            raise ValueError(f"{pin['path']}: published dependency cannot be read") from error
        require(len(payload) == pin["bytes"] and digest(payload) == pin["sha256"],
                f"{pin['path']}: published identity changed")
        payloads[name] = payload
    return base, payloads


def load_verified_module(name, path, payload):
    module_name = "ri47_pinned_" + name
    specification = importlib.util.spec_from_file_location(module_name, path)
    require(specification is not None and specification.loader is not None,
            f"{name}: cannot create the pinned module specification")
    module = importlib.util.module_from_spec(specification)
    sys.modules[module_name] = module
    # Compilation uses exactly the already verified bytes, not a second file read.
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def current_runtime():
    configuration = np.show_config(mode="dicts")
    require(type(configuration) is dict, "NumPy configuration is unavailable")
    return {
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "h5py": h5py.__version__},
        "python_implementation": platform.python_implementation(),
        "python_build": sys.version,
        "operating_system": platform.system(), "os_release": platform.release(),
        "os_version": platform.version(), "machine": platform.machine(),
        "byte_order": sys.byteorder, "hdf5_version": h5py.version.hdf5_version,
        "numpy_configuration": configuration,
    }


def check_coefficients(production, stages, manifest):
    actual = production.coefficient_manifest(stages)
    encoded = canonical_json(actual)
    require(encoded == canonical_json(manifest) and digest(encoded) == MANIFEST_SHA256,
            "designed coefficients differ from the admitted ordered manifest")


def admission():
    base, payloads = pinned_dependencies()
    baseline = json.loads(payloads["input_qualification"])
    qualification = json.loads(payloads["synthetic_qualification"])
    manifest = json.loads(payloads["coefficients"])
    require(canonical_json(manifest) == payloads["coefficients"],
            "published coefficient manifest is not its canonical byte representation")
    require(qualification["schema_version"] == "ri44-synthetic-qualification-v1"
            and qualification["status"] == "all_synthetic_gates_passed"
            and qualification["gate_counts"] == {"total": 105, "passed": 105, "failed": 0},
            "published synthetic admission record is not a passing qualification")
    require(canonical_json(qualification["coefficient_manifest"]) == payloads["coefficients"]
            and qualification["coefficient_manifest_sha256"] == MANIFEST_SHA256,
            "qualification and coefficient identities disagree")
    require(qualification["source_identity"]["filtering"]["sha256"]
            == DEPENDENCIES["filtering"]["sha256"]
            and qualification["source_identity"]["accepted_recipe_sha256"] == RECIPE_SHA256,
            "qualification source or recipe identity disagrees")
    require(baseline["schema_version"] == "gwosc-fixed-pair-qualification-v1"
            and baseline["status"] == "identity_and_structure_verified"
            and baseline["event"] == "GW150914" and baseline["strain_product_version"] == "V2",
            "published input qualification domain differs")
    runtime = current_runtime()
    admitted = qualification["runtime"]
    require(runtime["versions"] == admitted["required_versions"],
            "current package/interpreter versions differ from numerical admission")
    for key, value in runtime.items():
        require(canonical_json(value) == canonical_json(admitted[key]),
                f"current runtime field {key} differs from numerical admission")
    inspector = load_verified_module(
        "input_inspector", base / DEPENDENCIES["input_inspector"]["path"],
        payloads["input_inspector"])
    production = load_verified_module(
        "filtering", base / DEPENDENCIES["filtering"]["path"], payloads["filtering"])
    stages = production.design_stages()
    check_coefficients(production, stages, manifest)
    require((inspector.GPS_START, inspector.RATE, inspector.NPOINTS) ==
            (SOURCE_GPS, RATE, SOURCE_COUNT), "pinned inspector grid differs")
    require([item["detector"] for item in inspector.FILES] == ["H1", "L1"],
            "pinned inspector detector inventory differs")
    return {
        "inspector": inspector, "production": production, "stages": stages,
        "baseline": baseline, "qualification": qualification,
        "manifest": manifest, "runtime": runtime,
    }


def read_pair(input_dir, admitted):
    inspector = admitted["inspector"]
    # Both complete input identities bind before either HDF5 parser is called.
    payloads = [inspector._verified_bytes(Path(input_dir), expected)
                for expected in inspector.FILES]
    try:
        inspections = [inspector._inspect(payload, expected)
                       for payload, expected in zip(payloads, inspector.FILES, strict=True)]
        require(canonical_json(inspections) == canonical_json(admitted["baseline"]["detectors"]),
                "current schema/grid/flags differ from the published RI-37 inspection")
        arrays = []
        for payload in payloads:
            with h5py.File(io.BytesIO(payload), "r") as handle:
                values = handle["strain/Strain"][()]
            require(type(values) is np.ndarray and values.dtype == np.dtype("float64")
                    and values.shape == (SOURCE_COUNT,) and bool(np.isfinite(values).all()),
                    "complete input is not the admitted finite binary64 sample array")
            arrays.append(np.array(values, dtype=np.float64, order="C", copy=True))
    except (OSError, KeyError, TypeError, OverflowError) as error:
        raise ValueError("verified input failed fixed-release parsing") from error
    return inspections, arrays


def annotation(record, detector):
    value = {name: record[name] for name in (
        "data_quality", "hardware_injection_flags", "warnings", "missing_and_excluded_by_DATA")}
    value["cw_display_annotation"] = CW_ANNOTATION[detector]
    require(digest(canonical_json(value)) == ANNOTATION_SHA256[detector],
            f"{detector}: quality/injection annotation differs from the agreed crop schema")
    return value


def grid():
    require(CROP_START % RATE == 0 and CROP_START // RATE + SOURCE_GPS == TIME_ORIGIN
            and CROP_COUNT == RATE, "fixed crop arithmetic changed")
    return {
        "rate_hz": RATE, "source_start_gps": SOURCE_GPS, "source_sample_count": SOURCE_COUNT,
        "source_crop": [CROP_START, CROP_STOP], "sample_count": CROP_COUNT,
        "time_origin_gps": TIME_ORIGIN, "interval_gps": [TIME_ORIGIN, TIME_ORIGIN + 1],
        "interval_convention": "[start,end)", "offset_step_rational": "1/4096",
        "offset_last_rational": "4095/4096", "sample_indices": list(range(CROP_COUNT)),
        "source_sample_indices": list(range(CROP_START, CROP_STOP)),
    }


def build_outputs(admitted, inspections, arrays):
    require(len(inspections) == len(arrays) == 2, "exactly two detector arrays are required")
    production, stages = admitted["production"], admitted["stages"]
    crop_detectors, detector_reports = [], []
    for detector, record, values in zip(("H1", "L1"), inspections, arrays, strict=True):
        require(record["metadata"]["Detector"] == detector,
                "inspection detector order differs")
        require(type(values) is np.ndarray and values.dtype == np.dtype("float64")
                and values.shape == (SOURCE_COUNT,) and bool(np.isfinite(values).all()),
                f"{detector}: unexpected full input array")
        retained_annotation = annotation(record, detector)
        input_array_identity = array_identity(values)
        check_coefficients(production, stages, admitted["manifest"])
        filtered = production.apply_filter(values, stages)
        require(array_identity(values) == input_array_identity, "filtering mutated input samples")
        require(type(filtered) is np.ndarray and filtered.dtype == np.dtype("float64")
                and filtered.shape == values.shape and bool(np.isfinite(filtered).all())
                and not np.shares_memory(filtered, values), "filtering returned an invalid array")
        cropped = filtered[CROP_START:CROP_STOP].copy(order="C")
        crop_identity = array_identity(cropped)
        crop_detectors.append({
            "detector": detector, "input_filename": record["filename"],
            "input_identity": record["identity"],
            "values_hex": [float(value).hex() for value in cropped],
            "crop_identity": crop_identity, "annotations": retained_annotation,
        })
        detector_reports.append({
            "detector": detector, "input_filename": record["filename"],
            "input_file_identity": record["identity"],
            "input_array_identity": input_array_identity,
            "filtered_array_identity": array_identity(filtered), "crop_identity": crop_identity,
            "input_inspection": record, "annotations": retained_annotation,
        })
    check_coefficients(production, stages, admitted["manifest"])
    own_payload = Path(__file__).read_bytes()
    sources = {
        "process": {"filename": "process.py", **file_identity(own_payload)},
        "published_dependencies": DEPENDENCIES,
    }
    processing = {
        "operation": "17 ordered stages of SOS forward-backward filtering on each complete detector array",
        "coefficient_manifest_sha256": MANIFEST_SHA256,
        "padding": "odd extension independently at each stage with its admitted explicit padlen",
        "baseline_removal": "none", "taper": "none", "whitening": "none",
        "rescaling": "none", "alignment_or_time_shift": "none", "extra_calibration_correction": "none",
        "crop": [CROP_START, CROP_STOP],
    }
    crop = {
        "schema_version": "ri47-nominal-strain-crop-v1", "event": "GW150914",
        "quantity": "nominal dimensionless strain", "source_product": "GWOSC V2",
        "coefficient_manifest_sha256": MANIFEST_SHA256, "recipe_sha256": RECIPE_SHA256,
        "grid": grid(), "detectors": crop_detectors,
        "source_identity": sources, "processing": processing,
        "interpretation": "Nominal offline display crop; no uncertainty band, detection statistic, fitted lag or native-gravity comparison",
    }
    crop_bytes = export_json(crop)
    report = {
        "schema_version": "ri47-nominal-processing-report-v1",
        "status": "admitted_nominal_processing_completed", "event": "GW150914",
        "source_identity": sources, "current_processing_runtime": admitted["runtime"],
        "numerical_admission": {
            "synthetic_report_identity": DEPENDENCIES["synthetic_qualification"],
            "qualification_source_identity": admitted["qualification"]["source_identity"],
            "qualification_gate_counts": admitted["qualification"]["gate_counts"],
            "runtime_identity_fields_compared": sorted(admitted["runtime"]),
            "runtime_matches_published_qualification": True,
            "coefficient_manifest_sha256": MANIFEST_SHA256,
            "qualification_not_rerun_during_processing": True,
        },
        "input_custody": {
            "both_snapshots_verified_before_hdf5_parsing": True,
            "schema_flags_and_samples_use_same_retained_snapshots": True,
            "current_detector_inspections_equal_published_RI37": True,
            "input_directory_and_output_directory_not_recorded": True,
        },
        "processing": processing, "grid": grid(), "detectors": detector_reports,
        "exported_crop_file": {"filename": "CROP.json", **file_identity(crop_bytes)},
        "interpretation_boundary": {
            "observable": "Released nominal dimensionless calibrated strain after the declared filter response",
            "literal_HDF5_Yunits": "",
            "calibration": "No further correction or uncertainty propagation; C02 association is external release provenance",
            "L1_CW_flag": CW_ANNOTATION["L1"],
            "edge_handling": "Synthetic fixture qualification is not a uniform arbitrary-signal or physical-continuation guarantee",
            "inference": "No detection claim, fitted waveform, confidence band, intersite timing estimate or DET-versus-GR comparison",
        },
    }
    return {"CROP.json": crop_bytes, "PROCESSING_REPORT.json": export_json(report)}


def external_destination(output_dir):
    requested = Path(output_dir).expanduser()
    require(not requested.exists() and not requested.is_symlink(),
            "output directory already exists; a new external directory is required")
    destination = requested.resolve()
    require(destination.parent.is_dir(), "output parent directory must already exist")
    require(not any((parent / ".git").exists() for parent in (destination, *destination.parents)),
            "output directory must be outside Git checkouts")
    return destination


def write_outputs(destination, outputs):
    require(set(outputs) == {"CROP.json", "PROCESSING_REPORT.json"}, "unexpected output inventory")
    require(not destination.exists() and not destination.is_symlink(), "output destination appeared meanwhile")
    try:
        destination.mkdir(mode=0o700)
        for name in ("CROP.json", "PROCESSING_REPORT.json"):
            with (destination / name).open("xb") as stream:
                stream.write(outputs[name])
    except OSError as error:
        raise ValueError("output write failed; the newly created directory may contain a partial result") from error


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    try:
        destination = external_destination(arguments.output_dir)
        admitted = admission()
        inspections, arrays = read_pair(arguments.input_dir, admitted)
        outputs = build_outputs(admitted, inspections, arrays)
        write_outputs(destination, outputs)
    except ValueError as error:
        parser.exit(1, f"nominal processing refused: {error}\n")
    summary = {"status": "admitted_nominal_processing_completed",
               "files": {name: file_identity(payload) for name, payload in outputs.items()}}
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))


if __name__ == "__main__":
    main()
