"""RI-64 fixed observed-context helpers; import performs no I/O or filtering.

Public flow: admission() -> reconcile_coefficients(admitted) ->
read_verified_inputs(input_dir, admitted) -> evaluate_detector(record, rows,
admitted). Only read_verified_inputs opens observed bodies; it requires the
private, state-bound token produced by successful sixteen-certificate replay.
The caller owns the new RI-64 receipt, final report, and exclusive output.

Pure APIs: extract_windows(float_values); array_record(float_values);
interval_dot(Fraction_intervals, Fraction_values); interval_sub(left, right);
distance_bound(Fraction_point, interval); nominal_differences(left, right);
selected_row_result(x, w, z, p_short, p_context, assembled_row, side).
The last helper accepts small synthetic dimensions; evaluation enforces the
fixed pilot. All JSON rational values use canonical Fraction strings.

complete_numeric(values, admitted) returns (output_float_tuple, diagnostic).
No helper writes files. No child qualifier/driver source is imported or pinned.
This is a fixed-source reproduction boundary, not a hostile-Python sandbox.
"""

from decimal import Decimal
from fractions import Fraction
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import re
import stat
import struct
import sys


N, L, T = 2769, 4096, 10961
RATE, SOURCE_COUNT, SOURCE_GPS, TIME_ORIGIN = 4096, 131072, 1126259446, 1126259462
CENTER_START, CENTER_STOP, EXTENDED_START, EXTENDED_STOP = 65536, 68305, 61440, 72401
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
MANIFEST_SHA256 = "700b2c2f0e339df4a003ee7d772917cf243d8e3ffdbb90d087c9044bee42e3a0"
DEPENDENCIES = {
    "design": {"path": "gwosc_observed_context_v1/DESIGN.md", "bytes": 19255,
        "sha256": "636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2"},
    "ri60_check": {"path": "gwosc_context_operator_v2/check.py", "bytes": 38088,
        "sha256": "a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02"},
    "ri60_qualification": {"path": "gwosc_context_operator_v2/QUALIFICATION_REPORT.json", "bytes": 9413345,
        "sha256": "1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f"},
    "ri47_process": {"path": "gwosc_nominal_result_v1/process.py", "bytes": 18823,
        "sha256": "f026667837cfb6e2040e228f8cd9dd73e983fb5bc0610cb106e8dce521d685fd"},
}
OBSERVED_DEPENDENCIES = {
    "crop": {"path": "gwosc_nominal_result_v1/CROP.json", "bytes": 395470,
        "sha256": "a580481b9f6ea8dbb90242f12023817709ee7ac208d504110966f01f353592e7"},
    "processing": {"path": "gwosc_nominal_result_v1/PROCESSING_REPORT.json", "bytes": 159384,
        "sha256": "98bf0c53d5b988d3bb2aaa5f60c0fbcd87512501dd1137175b25589cc4856820"},
}
_TOKEN_SEAL = object()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode("ascii")


def identity(payload):
    require(type(payload) is bytes, "identity requires retained bytes")
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def _pin(pin):
    require(type(pin) is dict and type(pin.get("bytes")) is int and
            0 < pin["bytes"] <= 128 * 1024 * 1024 and type(pin.get("sha256")) is str and
            re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), "invalid frozen pin")
    return {key: pin[key] for key in ("bytes", "sha256")}


def verify_snapshot(payload, pin, label="snapshot"):
    require(identity(payload) == _pin(pin), label + ": snapshot identity mismatch")
    return payload


def bound_bytes(path, pin, label="snapshot"):
    expected = _pin(pin)
    path = Path(path)
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == expected["bytes"],
                label + ": expected pinned regular file")
        with path.open("rb") as stream:
            payload = stream.read(expected["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read file") from error
    return verify_snapshot(payload, expected, label)


def parse_json(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def constant(value):
        raise ValueError("nonfinite JSON value: " + value)
    return json.loads(payload, object_pairs_hook=pairs, parse_constant=constant)


def _load(name, path, payload):
    spec = importlib.util.spec_from_file_location("ri64_context_" + name, path)
    require(spec is not None and spec.loader is not None, "cannot specify pinned module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def _floats(values, length=None):
    require(type(values) in (tuple, list) and 0 < len(values) <= SOURCE_COUNT and
            (length is None or len(values) == length) and
            all(type(value) is float and math.isfinite(value) for value in values),
            "expected complete finite binary64 sequence")
    return tuple(values)


def _fractions(values, length=None):
    require(type(values) in (tuple, list) and 0 < len(values) <= SOURCE_COUNT and
            (length is None or len(values) == length) and
            all(type(value) is Fraction for value in values), "expected exact Fraction sequence")
    return tuple(values)


def _exact(values):
    return tuple(Fraction.from_float(value) for value in _floats(values))


def array_identity(values):
    values = _floats(values)
    payload = b"".join(struct.pack("<d", value) for value in values)
    return {"shape": [len(values)], "dtype": "little-endian binary64", "order": "C",
            **identity(payload)}


def array_record(values):
    values = _floats(values)
    return {"values_hex": [value.hex() for value in values], "array_identity": array_identity(values)}


def interval(bounds):
    require(type(bounds) in (tuple, list) and len(bounds) == 2 and
            all(type(value) is Fraction for value in bounds) and bounds[0] <= bounds[1],
            "expected ordered exact Fraction interval")
    return tuple(bounds)


def encoded_interval(bounds):
    return [str(value) for value in interval(bounds)]


def interval_identity(bounds):
    return identity(canonical([encoded_interval(pair) for pair in bounds]))


def interval_sub(left, right):
    a, b = interval(left)
    c, d = interval(right)
    return a - d, b - c


def interval_dot(coefficients, values):
    values = _fractions(values)
    require(type(coefficients) in (tuple, list) and len(coefficients) == len(values),
            "interval dot dimensions differ")
    lo = hi = Fraction(0)
    for pair, value in zip(coefficients, values, strict=True):
        a, b = interval(pair)
        lo += (a if value >= 0 else b) * value
        hi += (b if value >= 0 else a) * value
    return lo, hi


def distance_bound(point, bounds):
    require(type(point) is Fraction, "distance point must be exact Fraction")
    lo, hi = interval(bounds)
    return max(abs(point - lo), abs(point - hi))


def require_width(bounds, limit, exact_zero=False):
    lo, hi = interval(bounds)
    require(type(limit) is Fraction and limit >= 0 and hi - lo <= limit,
            "direct known-context width gate failed")
    require(not exact_zero or lo == hi == 0, "zero input requires exact zero interval")


def endpoint_gate(point, bounds, limit):
    require(type(limit) is Fraction and limit >= 0, "invalid endpoint-distance limit")
    bound = distance_bound(point, bounds)
    require(bound <= limit, "production/exact endpoint-distance gate failed")
    return {"point_exact": str(point), "distance_bound_exact": str(bound),
            "limit_exact": str(limit), "passed": True}


def window_grid():
    require(CENTER_STOP - CENTER_START == N and EXTENDED_STOP - EXTENDED_START == T and
            CENTER_START - EXTENDED_START == L and EXTENDED_STOP - CENTER_STOP == L and
            SOURCE_GPS + Fraction(CENTER_START, RATE) == TIME_ORIGIN,
            "fixed window arithmetic changed")
    return {"rate_hz": RATE, "source_start_gps": SOURCE_GPS, "source_sample_count": SOURCE_COUNT,
            "central_source_slice": [CENTER_START, CENTER_STOP],
            "extended_source_slice": [EXTENDED_START, EXTENDED_STOP],
            "left_source_slice": [EXTENDED_START, CENTER_START],
            "right_source_slice": [CENTER_STOP, EXTENDED_STOP],
            "N": N, "L": L, "T": T, "time_origin_gps": TIME_ORIGIN,
            "central_offset_step_exact": "1/4096", "central_offset_end_exact": str(Fraction(N, RATE)),
            "central_offset_last_exact": str(Fraction(N - 1, RATE)),
            "interval_convention": "[start,end)", "rows": list(ROWS),
            "central_sample_indices": list(range(N)),
            "central_source_indices": list(range(CENTER_START, CENTER_STOP)),
            "extended_source_indices": list(range(EXTENDED_START, EXTENDED_STOP)),
            "context_source_indices": [*range(EXTENDED_START, CENTER_START), *range(CENTER_STOP, EXTENDED_STOP)]}


def extract_windows(values):
    values = _floats(values, SOURCE_COUNT)
    grid = window_grid()
    x, w = values[CENTER_START:CENTER_STOP], values[EXTENDED_START:EXTENDED_STOP]
    z = values[EXTENDED_START:CENTER_START] + values[CENTER_STOP:EXTENDED_STOP]
    require(array_identity(w) == array_identity(z[:L] + x + z[L:]),
            "signed binary64 window injection identity differs")
    return {"x": x, "w": w, "z": z, "grid": grid}


def nominal_differences(left, right):
    left, right = _floats(left), _floats(right)
    require(len(left) == len(right), "nominal difference dimensions differ")
    values = tuple(a - b for a, b in zip(_exact(left), _exact(right), strict=True))
    maximum = max(map(abs, values))
    return {"operation": "exact_binary64_left_minus_right", "sample_count": len(values),
            "values_exact": [str(value) for value in values],
            "maximum_absolute_difference_exact": str(maximum),
            "maximizing_indices": [i for i, value in enumerate(values) if abs(value) == maximum]}


def selected_row_result(x, w, z, p_short, p_context, row, side):
    x, w, z = _floats(x), _floats(w), _floats(z)
    central = len(x)
    require(type(side) is int and side > 0 and len(w) == central + 2 * side and len(z) == 2 * side,
            "known-context dimensions differ")
    require(array_identity(w) == array_identity(z[:side] + x + z[side:]),
            "known-context injection identity differs")
    p_short, p_context = _floats(p_short, central), _floats(p_context, central)
    require(type(row) is dict and type(row.get("row")) is int and 0 <= row["row"] < central,
            "selected row index is invalid")
    short, long = row["short"]["intervals"], row["long"]["intervals"]
    require(len(short) == central and len(long) == len(w), "adjoint row dimensions differ")
    a = tuple(interval_sub(v, s) for v, s in zip(long[side:side + central], short, strict=True))
    b = tuple(interval(pair) for pair in (*long[:side], *long[side + central:]))
    require(tuple(map(interval, row["a"])) == a and tuple(map(interval, row["b"])) == b,
            "assembled known-context rows differ")
    fx, fw, fz = _exact(x), _exact(w), _exact(z)
    short_dot, long_dot = interval_dot(short, fx), interval_dot(long, fw)
    center_dot, context_dot = interval_dot(a, fx), interval_dot(b, fz)
    direct = center_dot[0] + context_dot[0], center_dot[1] + context_dot[1]
    subtracted = interval_sub(long_dot, short_dot)
    intersection = max(direct[0], subtracted[0]), min(direct[1], subtracted[1])
    require(intersection[0] <= intersection[1], "known-context interval decompositions disagree")
    peak_x, peak_w = max(map(abs, fx)), max(map(abs, fw))
    width_limit = peak_w / 10**12
    require_width(direct, width_limit, exact_zero=peak_w == 0)
    index = row["row"]
    point_short, point_long = Fraction.from_float(p_short[index]), Fraction.from_float(p_context[index])
    gates = {"short": endpoint_gate(point_short, short_dot, peak_x / 10**9),
             "context": endpoint_gate(point_long, long_dot, peak_w / 10**9),
             "difference": endpoint_gate(point_long - point_short, direct, (peak_x + peak_w) / 10**9)}
    return {"row": index, "passed": True,
            "short_output_interval": encoded_interval(short_dot),
            "context_output_interval": encoded_interval(long_dot),
            "center_term_interval": encoded_interval(center_dot),
            "recorded_context_term_interval": encoded_interval(context_dot),
            "direct_delta_interval": encoded_interval(direct),
            "output_difference_interval": encoded_interval(subtracted),
            "consistency_intersection": encoded_interval(intersection),
            "direct_delta_width_exact": str(direct[1] - direct[0]),
            "direct_delta_width_limit_exact": str(width_limit),
            "short_input_peak_exact": str(peak_x), "extended_input_peak_exact": str(peak_w),
            "exact_zero_required": peak_w == 0, "endpoint_gates": gates,
            "a_enclosure_identity": interval_identity(a), "b_enclosure_identity": interval_identity(b),
            "short_enclosure_identity": interval_identity(short), "long_enclosure_identity": interval_identity(long)}


def admission():
    """Read only source/qualification/metadata; never crop or raw observations."""
    base = Path(__file__).resolve().parent.parent
    payloads = {name: bound_bytes(base / pin["path"], pin, name) for name, pin in DEPENDENCIES.items()}
    check = _load("ri60_check", base / DEPENDENCIES["ri60_check"]["path"], payloads["ri60_check"])
    ri47 = _load("ri47", base / DEPENDENCIES["ri47_process"]["path"], payloads["ri47_process"])
    closure_pins = {}
    inherited = [*check.DEPENDENCIES.values(), *ri47.DEPENDENCIES.values(),
        {"path": "gwosc_context_operator_v2/operator.py", **check.ENGINE_PIN},
        {"path": check.REUSED_ORACLE_PATH, **check.ORACLE_PIN}]
    for pin in inherited:
        path, expected = pin["path"], _pin(pin)
        require(path not in closure_pins or closure_pins[path] == expected, "inherited dependency pin conflict")
        closure_pins[path] = expected
    closure_payloads = {path: bound_bytes(base / path, pin, path) for path, pin in closure_pins.items()}
    numeric = check.admission()
    qualification = parse_json(payloads["ri60_qualification"])
    check.validate_qualification(qualification, numeric)
    custody = ri47.admission()
    require(canonical(custody["runtime"]) == canonical(numeric["runtime"]), "admission runtime mismatch")
    require(canonical(custody["manifest"]) == numeric["coefficient_bytes"], "admission coefficients mismatch")
    return {"base": base, "ri60_check": check, "numeric": numeric, "qualification60": qualification,
            "qualification60_identity": identity(payloads["ri60_qualification"]), "ri47": ri47,
            "custody": custody, "runtime": numeric["runtime"], "_payloads": payloads,
            "_closure_pins": closure_pins, "_closure_payloads": closure_payloads,
            "dependency_identities": {name: identity(body) for name, body in payloads.items()},
            "design_identity": identity(payloads["design"]), "_row_token": None, "_observed_token": None}


def _numeric_state(admitted):
    check, numeric, ri47 = admitted["ri60_check"], admitted["numeric"], admitted["ri47"]
    check.check_coefficients(numeric)
    ri47.check_coefficients(admitted["custody"]["production"], admitted["custody"]["stages"],
                           admitted["custody"]["manifest"])
    current = check.runtime()
    require(canonical(current) == canonical(numeric["runtime"]) == canonical(admitted["runtime"])
            == canonical(admitted["custody"]["runtime"]), "admitted runtime changed")
    require(identity(numeric["coefficient_bytes"])["sha256"] == MANIFEST_SHA256,
            "admitted coefficient bytes changed")
    for name, pin in DEPENDENCIES.items():
        verify_snapshot(admitted["_payloads"][name], pin, name)
        require(bound_bytes(admitted["base"] / pin["path"], pin, name) == admitted["_payloads"][name],
                "admitted dependency changed")
    for path, pin in admitted["_closure_pins"].items():
        verify_snapshot(admitted["_closure_payloads"][path], pin, path)
        require(bound_bytes(admitted["base"] / path, pin, path) == admitted["_closure_payloads"][path],
                "inherited numerical source or receipt changed")
    check.validate_qualification(admitted["qualification60"], numeric)
    require(admitted["qualification60_identity"] == _pin(DEPENDENCIES["ri60_qualification"]),
            "admitted receipt identity changed")
    return canonical({"coefficient_bytes_identity": identity(numeric["coefficient_bytes"]),
        "fraction_stages": [[[str(value) for value in section] for section in stage]
                            for stage in numeric["fraction_stages"]],
        "padlens": numeric["padlens"], "arithmetic": numeric["arithmetic"], "runtime": current,
        "qualification": admitted["qualification60_identity"],
        "qualification_content_identity": identity(canonical(admitted["qualification60"])),
        "dependencies": admitted["dependency_identities"], "closure": admitted["_closure_pins"],
        "input_metadata": identity(canonical(admitted["custody"]["baseline"])),
        "inspector_files": admitted["custody"]["inspector"].FILES})


def _row_state(rows, check):
    require(type(rows) is tuple and tuple(row["row"] for row in rows) == ROWS,
            "complete fixed row inventory required")
    return canonical([{ "summary": check.row_summary(row),
                        "short_intervals": interval_identity(row["short"]["intervals"]),
                        "long_intervals": interval_identity(row["long"]["intervals"])} for row in rows])


class _RowAdmission:
    __slots__ = ("owner", "rows", "row_state", "numeric_state", "seal")

    def __init__(self, owner, rows, row_state, numeric_state, seal):
        require(seal is _TOKEN_SEAL, "private row admission required")
        self.owner, self.rows, self.row_state = owner, rows, row_state
        self.numeric_state, self.seal = numeric_state, seal


def reconcile_coefficients(admitted):
    """Recompute and reconcile all sixteen certificates before observed access."""
    admitted["_row_token"] = None
    admitted["_observed_token"] = None
    state = _numeric_state(admitted)
    check = admitted["ri60_check"]
    rows = check.build_rows(admitted["numeric"])
    previous = {gate["detail"]["row"]["row"]: gate["detail"]["row"]
                for gate in admitted["qualification60"]["gates"] if gate["id"].startswith("enclosure:")}
    require(set(previous) == set(ROWS), "qualification certificate row inventory differs")
    for row in rows:
        require(canonical(check.row_summary(row)) == canonical(previous[row["row"]]),
                "recomputed certificate differs from qualification")
    require(_numeric_state(admitted) == state, "numeric state changed during certificate replay")
    admitted["_row_token"] = _RowAdmission(admitted, rows, _row_state(rows, check), state, _TOKEN_SEAL)
    return rows


def _require_rows(admitted, rows=None):
    token = admitted.get("_row_token")
    require(type(token) is _RowAdmission and token.seal is _TOKEN_SEAL and token.owner is admitted,
            "sixteen reconciled certificates required before observed access/evaluation")
    require(rows is None or rows is token.rows, "different row object after reconciliation")
    require(_numeric_state(admitted) == token.numeric_state and
            _row_state(token.rows, admitted["ri60_check"]) == token.row_state,
            "admitted numerical or row state changed after reconciliation")
    return token.rows


def read_both_snapshots(input_dir, inspector):
    """All fixed raw identities must bind before the caller invokes any parser."""
    require([entry["detector"] for entry in inspector.FILES] == ["H1", "L1"],
            "fixed detector inventory differs")
    return tuple(inspector._verified_bytes(Path(input_dir), expected) for expected in inspector.FILES)


def validate_crop(crop, processing, inspections, raw_arrays, admitted):
    """Validate an already bound crop and its complete processing provenance."""
    ri47 = admitted["ri47"]
    require(type(crop) is dict and crop.get("schema_version") == "ri47-nominal-strain-crop-v1" and
            crop.get("event") == "GW150914" and crop.get("quantity") == "nominal dimensionless strain" and
            crop.get("source_product") == "GWOSC V2" and
            crop.get("coefficient_manifest_sha256") == MANIFEST_SHA256 and
            crop.get("recipe_sha256") == ri47.RECIPE_SHA256 and
            canonical(crop.get("grid")) == canonical(ri47.grid()), "published crop schema/grid differs")
    expected_sources = {"process": {"filename": "process.py", **_pin(DEPENDENCIES["ri47_process"])},
                        "published_dependencies": ri47.DEPENDENCIES}
    require(canonical(crop.get("source_identity")) == canonical(expected_sources), "crop source identity differs")
    require(type(processing) is dict and processing.get("schema_version") == "ri47-nominal-processing-report-v1"
            and processing.get("status") == "admitted_nominal_processing_completed" and
            processing.get("event") == "GW150914" and
            canonical(processing.get("source_identity")) == canonical(expected_sources) and
            canonical(processing.get("grid")) == canonical(ri47.grid()) and
            canonical(processing.get("current_processing_runtime")) == canonical(admitted["runtime"]) and
            canonical(processing.get("processing")) == canonical(crop.get("processing")) and
            processing.get("exported_crop_file") == {"filename": "CROP.json", **_pin(OBSERVED_DEPENDENCIES["crop"])},
            "published processing provenance differs")
    require(type(crop.get("detectors")) is list and len(crop["detectors"]) == 2 and
            type(processing.get("detectors")) is list and len(processing["detectors"]) == 2 and
            len(inspections) == len(raw_arrays) == 2, "detector coverage differs")
    records = []
    for detector, entry, provenance, inspection, raw in zip(("H1", "L1"), crop["detectors"],
            processing["detectors"], inspections, raw_arrays, strict=True):
        raw = _floats(raw, SOURCE_COUNT)
        annotation = ri47.annotation(inspection, detector)
        require(entry.get("detector") == provenance.get("detector") == detector and
                entry.get("input_filename") == provenance.get("input_filename") == inspection["filename"] and
                entry.get("input_identity") == provenance.get("input_file_identity") == inspection["identity"] and
                canonical(entry.get("annotations")) == canonical(annotation) == canonical(provenance.get("annotations")) and
                canonical(provenance.get("input_inspection")) == canonical(inspection) and
                provenance.get("input_array_identity") == array_identity(raw),
                detector + ": input/annotation provenance differs")
        values_hex = entry.get("values_hex")
        require(type(values_hex) is list and len(values_hex) == RATE and
                all(type(value) is str and len(value) <= 32 for value in values_hex), "complete crop values required")
        try:
            values = tuple(float.fromhex(value) for value in values_hex)
        except (ValueError, OverflowError) as error:
            raise ValueError("invalid crop binary64 string") from error
        _floats(values, RATE)
        require([value.hex() for value in values] == values_hex and
                array_identity(values) == entry.get("crop_identity") == provenance.get("crop_identity"),
                detector + ": crop binary64 identity differs")
        records.append({"detector": detector, "input_filename": inspection["filename"],
            "input_identity": inspection["identity"], "input_array_identity": array_identity(raw),
            "annotations": annotation, "raw": raw, "baseline": values[:N],
            "baseline_identity": array_identity(values[:N]),
            "ri47_crop_array_identity": entry["crop_identity"]})
    return tuple(records)


def _record_state(record):
    return canonical({key: record[key] for key in ("detector", "input_filename", "input_identity",
        "input_array_identity", "annotations", "baseline_identity", "ri47_crop_array_identity")} | {
            "actual_raw_identity": array_identity(record["raw"]),
            "actual_baseline_identity": array_identity(record["baseline"])})


class _ObservedAdmission:
    __slots__ = ("owner", "row_token", "records", "states", "seal")

    def __init__(self, owner, records, seal):
        require(seal is _TOKEN_SEAL, "private observed admission required")
        self.owner, self.row_token, self.records = owner, owner["_row_token"], records
        self.states, self.seal = tuple(_record_state(record) for record in records), seal


def read_verified_inputs(input_dir, admitted):
    _require_rows(admitted)
    admitted["_observed_token"] = None
    inspector = admitted["custody"]["inspector"]
    snapshots = read_both_snapshots(input_dir, inspector)
    exports = {name: bound_bytes(admitted["base"] / pin["path"], pin, name)
               for name, pin in OBSERVED_DEPENDENCIES.items()}
    # No HDF5 or observed JSON parser has been called before all four pins bind.
    import h5py
    import numpy as np
    inspections = [inspector._inspect(body, expected)
                   for body, expected in zip(snapshots, inspector.FILES, strict=True)]
    require(canonical(inspections) == canonical(admitted["custody"]["baseline"]["detectors"]),
            "current inspection differs from complete RI-37 schema/flags")
    arrays = []
    for body in snapshots:
        with h5py.File(io.BytesIO(body), "r") as handle:
            values = handle["strain/Strain"][()]
        require(type(values) is np.ndarray and values.dtype == np.dtype("float64") and
                values.shape == (SOURCE_COUNT,) and bool(np.isfinite(values).all()),
                "raw array is not complete finite binary64")
        arrays.append(tuple(values.tolist()))
    crop, processing = parse_json(exports["crop"]), parse_json(exports["processing"])
    records = validate_crop(crop, processing, inspections, arrays, admitted)
    admitted["_observed_token"] = _ObservedAdmission(admitted, records, _TOKEN_SEAL)
    return {"detectors": records, "crop_identity": identity(exports["crop"]),
            "processing_identity": identity(exports["processing"]), "_snapshots": snapshots,
            "_export_snapshots": exports, "input_custody": {
                "sixteen_certificates_reconciled_before_observed_access": True,
                "both_raw_snapshots_verified_before_any_hdf5_parse": True,
                "same_bytes_supply_inspection_and_samples": True,
                "complete_crop_and_annotations_verified": True,
                "input_paths_not_exported": True}}


def complete_numeric(values, admitted):
    """Whole-array numerical diagnostic, with no unit floor or exact-map claim."""
    values = _floats(values)
    numeric = admitted["numeric"]
    admitted["ri60_check"].check_coefficients(numeric)
    import numpy as np
    source = np.array(values, dtype=np.float64)
    before = array_identity(values)
    output = numeric["production"].apply_filter(source, numeric["stages"])
    require(type(output) is np.ndarray and output.dtype == np.dtype("float64") and
            output.shape == source.shape and not np.shares_memory(source, output),
            "production output shape/type/alias differs")
    require(array_identity(tuple(source.tolist())) == before, "production changed input samples")
    result = _floats(tuple(output.tolist()), len(values))
    reference = numeric["reference"].reference_filter(list(values),
        [stage["sos"].tolist() for stage in numeric["stages"]], list(numeric["padlens"]))
    require(type(reference) is list and len(reference) == len(values) and
            all(type(value) is Decimal and value.is_finite() for value in reference), "invalid Decimal reference output")
    residuals = tuple(abs(Fraction.from_float(p) - Fraction(d)) for p, d in zip(result, reference, strict=True))
    peak = max(map(abs, _exact(values)))
    limit = peak / 10**9
    maximum = max(residuals)
    zero_output = all(value == 0 for value in result) and all(value == 0 for value in reference)
    require(maximum <= limit and (peak != 0 or zero_output), "complete actual-scale numeric gate failed")
    admitted["ri60_check"].check_coefficients(numeric)
    strings = [str(value) for value in reference]
    return result, {"passed": True, "sample_count": len(values), "input_identity": before,
        "output_identity": array_identity(result), "reference_decimal": strings,
        "reference_decimal_identity": identity(canonical(strings)),
        "absolute_residuals_exact": [str(value) for value in residuals],
        "input_peak_exact": str(peak), "limit_exact": str(limit),
        "maximum_absolute_residual_exact": str(maximum),
        "maximizing_indices": [i for i, value in enumerate(residuals) if value == maximum],
        "exact_zero_required": peak == 0, "exact_zero_output_and_reference": zero_output,
        "interpretation": "Numerical Decimal80 diagnostic; not by itself an exact-operator error certificate."}


def evaluate_detector(record, rows, admitted):
    _require_rows(admitted, rows)
    observed = admitted.get("_observed_token")
    require(type(observed) is _ObservedAdmission and observed.seal is _TOKEN_SEAL and
            observed.owner is admitted and observed.row_token is admitted["_row_token"],
            "verified observed snapshots required before evaluation")
    position = next((i for i, candidate in enumerate(observed.records) if candidate is record), None)
    require(position is not None and _record_state(record) == observed.states[position],
            "retained observed record changed or was substituted")
    require(type(record) is dict and record.get("detector") in ("H1", "L1"), "invalid detector record")
    raw = _floats(record["raw"], SOURCE_COUNT)
    require(array_identity(raw) == record["input_array_identity"], "retained raw input changed")
    baseline = _floats(record["baseline"], N)
    require(array_identity(baseline) == record["baseline_identity"], "retained RI-47 baseline changed")
    require(hashlib.sha256(canonical(record["annotations"])).hexdigest() ==
            admitted["ri47"].ANNOTATION_SHA256[record["detector"]], "retained annotation changed")
    windows = extract_windows(raw)
    short, short_check = complete_numeric(windows["x"], admitted)
    long, long_check = complete_numeric(windows["w"], admitted)
    contextual = long[L:L + N]
    selected = [selected_row_result(windows["x"], windows["w"], windows["z"], short, contextual, row, L)
                for row in rows]
    _require_rows(admitted, rows)
    require(_record_state(record) == observed.states[position], "observed record changed during evaluation")
    return {"detector": record["detector"], "passed": True, "status": "all_observed_context_gates_passed",
        "input_filename": record["input_filename"], "input_identity": record["input_identity"],
        "input_array_identity": record["input_array_identity"], "annotations": record["annotations"],
        "ri47_crop_array_identity": record["ri47_crop_array_identity"], "windows": windows["grid"],
        "inputs": {"short": array_record(windows["x"]), "extended": array_record(windows["w"]),
                   "context": array_record(windows["z"])},
        "outputs": {"short": array_record(short), "extended": array_record(long),
                    "context": array_record(contextual), "record": array_record(baseline)},
        "forward_checks": {"short": short_check, "extended": long_check},
        "differences": {"context": nominal_differences(contextual, short),
                        "record": nominal_differences(baseline, contextual)},
        "selected_rows": selected,
        "interpretation": "Finite recorded-context comparison only; no physical ground truth, monotonicity, envelope, fit or uncertainty inference."}
