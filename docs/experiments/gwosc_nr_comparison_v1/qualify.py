"""Qualify the fixed length-2769 finite-array operation using synthetic inputs only."""

from decimal import (Context, Decimal, DivisionByZero, InvalidOperation, Overflow,
                     ROUND_HALF_EVEN, localcontext)
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import stat
import sys

import h5py
import numpy as np
import scipy


LENGTH = 2769
MANIFEST_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
RECIPE_SHA256 = "872ab0e63ac15abb40b45dfe58d6cdfd6b0e920f1ed3d167044b17062386ad5a"
DEPENDENCIES = {
    "filtering": {"path": "gwosc_nominal_processing_v1/filtering.py", "bytes": 8805,
                  "sha256": "9a93c1f218fecfa6fdf7ee0e30e054ad0973dfb1f04ae339dfbb0e7a6f8ae1be"},
    "reference": {"path": "gwosc_nominal_processing_v1/reference.py", "bytes": 7253,
                  "sha256": "c8cffaac8bf0c1647a120ecb00ba1505ef69b60f80cda653d60b2a2f7e9da305"},
    "coefficients": {"path": "gwosc_nominal_processing_v1/COEFFICIENTS.json", "bytes": 7698,
                     "sha256": MANIFEST_SHA256},
    "synthetic_qualification": {"path": "gwosc_nominal_processing_v1/SYNTHETIC_REPORT.json", "bytes": 107468,
                                "sha256": "2522ca70a1402700e644feba25bf70abf2b5720a80031304f82225ea0e5808c3"},
    "recipe": {"path": "gwosc_nominal_display_v1/RECIPE.md", "bytes": 14014,
               "sha256": RECIPE_SHA256},
}
FIXTURES = (
    {"name": "zeros", "kind": "constant", "value_hex": "0x0.0p+0"},
    {"name": "ones", "kind": "constant", "value_hex": "0x1.0000000000000p+0"},
    {"name": "impulse_0", "kind": "unit_impulse", "index": 0},
    {"name": "impulse_1384", "kind": "unit_impulse", "index": 1384},
    {"name": "impulse_2768", "kind": "unit_impulse", "index": 2768},
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def export_json(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True,
                       allow_nan=False) + "\n").encode("ascii")


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def bound_bytes(path, pin, label):
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode), label + ": expected regular file")
        require(info.st_size == pin["bytes"], label + ": byte count mismatch")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read file") from error
    require(identity(payload) == {"bytes": pin["bytes"], "sha256": pin["sha256"]},
            label + ": snapshot identity mismatch")
    return payload


def load_module(name, path, payload):
    spec = importlib.util.spec_from_file_location("ri53_pinned_" + name, path)
    require(spec is not None and spec.loader is not None, "cannot specify pinned source")
    module = importlib.util.module_from_spec(spec)
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def runtime():
    return {
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__, "h5py": h5py.__version__},
        "python_implementation": platform.python_implementation(), "python_build": sys.version,
        "operating_system": platform.system(), "os_release": platform.release(),
        "os_version": platform.version(), "machine": platform.machine(),
        "byte_order": sys.byteorder, "hdf5_version": h5py.version.hdf5_version,
        "numpy_configuration": np.show_config(mode="dicts"),
    }


def check_coefficients(admitted):
    actual = canonical(admitted["production"].coefficient_manifest(admitted["stages"]))
    require(actual == admitted["coefficient_bytes"] and
            hashlib.sha256(actual).hexdigest() == MANIFEST_SHA256,
            "coefficients differ from admitted manifest")


def admission():
    base = Path(__file__).resolve().parent.parent
    # Verify every dependency body before parsing or executing any of them.
    payloads = {name: bound_bytes(base / pin["path"], pin, name)
                for name, pin in DEPENDENCIES.items()}
    prior = json.loads(payloads["synthetic_qualification"])
    require(prior["schema_version"] == "ri44-synthetic-qualification-v1" and
            prior["status"] == "all_synthetic_gates_passed" and
            canonical(prior["gate_counts"]) == canonical({"total": 105, "passed": 105, "failed": 0}),
            "RI-44 synthetic qualification is not admitted")
    require(canonical(prior["coefficient_manifest"]) == payloads["coefficients"] and
            prior["coefficient_manifest_sha256"] == MANIFEST_SHA256 and
            prior["source_identity"]["accepted_recipe_sha256"] == RECIPE_SHA256,
            "RI-44 coefficient or recipe identity mismatch")
    for key in ("filtering", "reference"):
        require(prior["source_identity"][key]["sha256"] == DEPENDENCIES[key]["sha256"],
                "RI-44 source identity mismatch")
    current = runtime()
    require(current["versions"] == prior["runtime"]["required_versions"], "runtime version mismatch")
    for key, value in current.items():
        require(canonical(value) == canonical(prior["runtime"][key]), "runtime mismatch: " + key)
    production = load_module("filtering", base / DEPENDENCIES["filtering"]["path"], payloads["filtering"])
    reference = load_module("reference", base / DEPENDENCIES["reference"]["path"], payloads["reference"])
    admitted = {"production": production, "reference": reference, "stages": production.design_stages(),
                "coefficient_bytes": payloads["coefficients"], "runtime": current}
    check_coefficients(admitted)
    return admitted


def array_identity(values):
    require(type(values) is np.ndarray and values.dtype == np.dtype("float64") and
            values.shape == (LENGTH,) and bool(np.isfinite(values).all()),
            "expected a complete finite length-2769 binary64 array")
    payload = np.ascontiguousarray(values, dtype="<f8").tobytes(order="C")
    return {"shape": [LENGTH], "dtype": "little-endian binary64", "order": "C", **identity(payload)}


def fixture_values(spec):
    values = np.zeros(LENGTH, dtype=np.float64)
    if spec["kind"] == "constant":
        values.fill(float.fromhex(spec["value_hex"]))
    else:
        values[spec["index"]] = 1.0
    return values


def decimal_text(value):
    # Human-readable only; the gate below compares exact rational values.
    context = Context(prec=110, rounding=ROUND_HALF_EVEN, Emin=-999999,
                      Emax=999999, capitals=1, clamp=0, flags=[],
                      traps=[InvalidOperation, DivisionByZero, Overflow])
    with localcontext(context):
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def filter_audit(values, admitted, unit_floor, require_zero=False):
    """Return full production output and an exact discrepancy/threshold record."""
    require(type(unit_floor) is bool and type(require_zero) is bool, "invalid audit mode")
    input_identity = array_identity(values)
    peak = max(Fraction.from_float(float(value)) for value in np.abs(values))
    require(unit_floor or peak > 0, "actual scale-relative audit requires nonzero input")
    scale = max(Fraction(1), peak) if unit_floor else peak
    threshold = scale / 10**9
    check_coefficients(admitted)
    output = admitted["production"].apply_filter(values, admitted["stages"])
    output_identity = array_identity(output)
    require(array_identity(values) == input_identity and not np.shares_memory(values, output),
            "production modified or aliased its input")
    stages = admitted["stages"]
    exact = admitted["reference"].reference_filter(
        values.tolist(), [stage["sos"].tolist() for stage in stages],
        [stage["padlen"] for stage in stages])
    require(type(exact) is list and len(exact) == LENGTH and
            all(type(value) is Decimal and value.is_finite() for value in exact),
            "reference did not return a complete finite Decimal array")
    errors = [abs(Fraction.from_float(float(value)) - Fraction(reference))
              for value, reference in zip(output, exact)]
    maximum = max(errors)
    worst = errors.index(maximum)
    zero_passed = bool((output == 0.0).all()) and all(value == 0 for value in exact)
    passed = maximum <= threshold and (not require_zero or zero_passed)
    check_coefficients(admitted)
    return output, {
        "sample_count_compared": LENGTH, "input_array_identity": input_identity,
        "output_array_identity": output_identity,
        "reference_decimal_array_identity": identity(canonical([str(value) for value in exact])),
        "reference_precision": 80, "reference_rounding": "ROUND_HALF_EVEN",
        "reference_identity_convention": "Canonical compact ASCII JSON list of complete Decimal output strings, without newline.",
        "input_peak_exact": str(peak), "input_peak_decimal": decimal_text(peak),
        "scale_exact": str(scale),
        "criterion": "1e-9*max(1,maxabs(input))" if unit_floor else "1e-9*maxabs(input)",
        "threshold_exact": str(threshold), "threshold_decimal": decimal_text(threshold),
        "maximum_absolute_error_exact": str(maximum),
        "maximum_absolute_error_decimal": decimal_text(maximum),
        "maximum_error_index": worst,
        "production_at_maximum_error_hex": float(output[worst]).hex(),
        "reference_at_maximum_error_decimal": str(exact[worst]),
        "exact_zero_required": require_zero,
        "exact_zero_output_and_reference": zero_passed,
        "passed": passed,
        "comparison_arithmetic": "Exact Fraction difference between each binary64 output and the finite Decimal recurrence output; exact rational threshold comparison.",
    }


def common_record(admitted):
    return {
        "schema_version": "ri53-short-record-qualification-v1", "length": LENGTH,
        "source_identity": identity(Path(__file__).read_bytes()),
        "published_dependencies": DEPENDENCIES, "runtime": admitted["runtime"],
        "coefficient_manifest_sha256": MANIFEST_SHA256, "recipe_sha256": RECIPE_SHA256,
        "fixture_declarations": list(FIXTURES),
        "scope": "Five synthetic finite-array checks only. No observed or public NR inputs, physical continuation, endpoint-error bound, fitting or waveform interpretation.",
    }


def run_qualification(admitted):
    results = []
    for spec in FIXTURES:
        _, audit = filter_audit(fixture_values(spec), admitted, True, spec["name"] == "zeros")
        results.append({"fixture": spec, "audit": audit})
    passed = sum(item["audit"]["passed"] for item in results)
    return {**common_record(admitted), "fixtures": results,
            "status": "all_short_record_gates_passed" if passed == 5 else "numerical_gates_failed",
            "gate_counts": {"total": 5, "passed": passed, "failed": 5 - passed}}


def validate_qualification(report, admitted):
    """Validate an independently supplied report receipt without rerunning fixtures."""
    require(type(report) is dict, "qualification must be an object")
    for key, value in common_record(admitted).items():
        require(canonical(report.get(key)) == canonical(value), "qualification mismatch: " + key)
    require(report.get("status") == "all_short_record_gates_passed" and
            canonical(report.get("gate_counts")) == canonical({"total": 5, "passed": 5, "failed": 0}),
            "short-record qualification did not pass")
    results = report.get("fixtures")
    require(type(results) is list and len(results) == 5, "qualification fixture inventory mismatch")
    for spec, result in zip(FIXTURES, results):
        require(canonical(result["fixture"]) == canonical(spec), "qualification fixture changed")
        audit = result["audit"]
        require(canonical(audit["input_array_identity"]) == canonical(array_identity(fixture_values(spec))),
                "qualification fixture input identity changed")
        require(type(audit["sample_count_compared"]) is int and audit["sample_count_compared"] == LENGTH and
                type(audit["reference_precision"]) is int and audit["reference_precision"] == 80 and
                audit["reference_rounding"] == "ROUND_HALF_EVEN", "qualification recurrence coverage mismatch")
        require(audit["criterion"] == "1e-9*max(1,maxabs(input))" and
                audit["scale_exact"] == "1" and audit["threshold_exact"] == "1/1000000000" and
                audit["input_peak_exact"] == ("0" if spec["name"] == "zeros" else "1"),
                "qualification threshold changed")
        error = Fraction(audit["maximum_absolute_error_exact"])
        require(str(error) == audit["maximum_absolute_error_exact"] and 0 <= error <= Fraction(1, 10**9)
                and audit["passed"] is True, "qualification numerical gate failed")
        zero = spec["name"] == "zeros"
        require(audit["exact_zero_required"] is zero and
                (not zero or (audit["exact_zero_output_and_reference"] is True and error == 0)),
                "qualification exact-zero gate failed")
    return True


def main():
    require(len(sys.argv) == 1, "qualify.py takes no arguments and reads no scientific inputs")
    report = run_qualification(admission())
    sys.stdout.buffer.write(export_json(report))
    return 0 if report["gate_counts"]["failed"] == 0 else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, KeyError, TypeError, OSError) as error:
        print("short-record qualification refused: " + str(error), file=sys.stderr)
        raise SystemExit(1)
