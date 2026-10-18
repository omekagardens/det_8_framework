"""RI64 fixed synthetic consumer qualification; never open observed samples.

The reused RI60 receipt binds its earlier 196 gates. This module executes a
separate, explicitly enumerated 75-gate consumer suite. Indexed arrays, exact
oracle systems and synthetic provenance/refusal fixtures are not observations.
"""

from contextlib import contextmanager
import copy
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import struct
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace


CONTEXT_PIN = {"bytes": 32566, "sha256": "fb0ec155f16292a07a5884e686e1dca167d5e37d7efc87e26ea1c41eb35f717b"}
DESIGN_PIN = {"bytes": 19255, "sha256": "636401b05620f227115362e1ecbf175a4a90a9dd34a021e0813f14e73ed58be2"}
RI60_PIN = {"bytes": 9413345, "sha256": "1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f"}
N, L, T, SOURCE_COUNT = 2769, 4096, 10961, 131072
ROWS = (0, 1, 27, 805, 1384, 2741, 2767, 2768)
TOYS = ("identity", "first_order", "biquad", "two_sections", "two_stages", "fir", "zero_dc", "zero_dc_then_biquad")
INDEX_CASES = ("positive_plain", "negative_plain", "positive_zeros_a", "negative_zeros_a", "positive_zeros_b", "negative_zeros_b")
CONTROLS = ("endpoint_outside_pass", "endpoint_outside_fail", "nominal_all_ties", "nominal_signed_reduction")
REFUSALS = ("source_changed", "source_missing", "coefficients", "stage_order", "padding",
    "current_receipt_missing", "current_receipt_failed", "current_receipt_stale", "ri60_receipt_failed", "ri60_receipt_stale",
    "runtime_mismatch", "unreconciled_rows", "resource_exhaustion", "input_missing", "input_swapped", "input_truncated",
    "input_corrupt_same_size", "grid_mismatch", "nonfinite_samples", "data_inconsistency", "altered_flags",
    "altered_annotations", "index_shift", "crop_values_changed", "crop_identity_changed", "output_exists",
    "interval_misses_exact", "interval_reversed", "interval_overwide", "numerical_threshold", "midpoint_only",
    "overlap_only", "both_inputs_bound_before_parse")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def export_json(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + "\n").encode("ascii")


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def bound_bytes(path, pin, label):
    require(type(pin.get("bytes")) is int and pin["bytes"] > 0 and
            type(pin.get("sha256")) is str and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]), label + ": pin not frozen")
    try:
        info = path.lstat()
        require(stat.S_ISREG(info.st_mode) and info.st_size == pin["bytes"], label + ": file size/type changed")
        with path.open("rb") as stream:
            payload = stream.read(pin["bytes"] + 1)
    except OSError as error:
        raise ValueError(label + ": cannot read pinned file") from error
    require(identity(payload) == pin, label + ": byte identity changed")
    return payload


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


def admission():
    base = Path(__file__).resolve().parent
    payload = bound_bytes(base / "context.py", CONTEXT_PIN, "context source")
    bound_bytes(base / "DESIGN.md", DESIGN_PIN, "accepted design")
    spec = importlib.util.spec_from_file_location("ri64_pinned_context", base / "context.py")
    require(spec is not None and spec.loader is not None, "cannot load pinned context")
    context = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = context
    exec(compile(payload, str(base / "context.py"), "exec"), context.__dict__)
    shared = context.admission()
    require(shared["qualification60_identity"] == RI60_PIN and shared["design_identity"] == DESIGN_PIN,
            "current RI60 receipt or design differs")
    return {"context": context, "shared": shared}


def inventory():
    return (["index:" + name for name in INDEX_CASES] +
            [f"toy:{name}:{n}:{l}" for name in TOYS for n in (4, 7) for l in (1, 2)] +
            ["control:" + name for name in CONTROLS] + ["refusal:" + name for name in REFUSALS])


def external_destination(path):
    path = Path(path)
    require(not path.exists() and not path.is_symlink() and path.name not in ("", ".", ".."), "output leaf must be new")
    require(path.parent.is_dir(), "output parent must exist")
    resolved = path.parent.resolve() / path.name
    require(not any((parent / ".git").exists() for parent in (resolved.parent, *resolved.parent.parents)),
            "output must be outside Git checkouts")
    return resolved


def contains(bounds, value):
    require(type(value) is F and bounds[0] <= value <= bounds[1], "interval misses known exact toy value")


def decoded(bounds):
    require(type(bounds) is list and len(bounds) == 2, "encoded interval shape")
    values = tuple(F(value) for value in bounds)
    require([str(value) for value in values] == bounds and values[0] <= values[1], "encoded interval not canonical")
    return values


def expect_refusal(work, reason=None):
    try:
        work()
    except (ValueError, TypeError, KeyError, ArithmeticError, RuntimeError) as error:
        require(reason is None or str(error) == reason, "synthetic refusal occurred for an unintended reason")
        return {"refused": True}
    raise ValueError("invalid synthetic request was accepted")


@contextmanager
def patched(obj, name, value):
    previous = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, previous)


def indexed_case(name, admitted):
    context = admitted["context"]
    sign = -1 if name.startswith("negative") else 1
    values = [sign * k / 2**20 for k in range(SOURCE_COUNT)]
    if "zeros" in name:
        signs = (-1, 1, -1) if name.endswith("a") else (1, -1, 1)
        for index, polarity in zip((61440, 65536, 68305), signs):
            values[index] = -0.0 if polarity < 0 else 0.0
    before = identity(b"".join(struct.pack("<d", value) for value in values))
    windows = context.extract_windows(values)
    expected = {"x": tuple(values[65536:68305]), "w": tuple(values[61440:72401]),
                "z": tuple(values[61440:65536] + values[68305:72401])}
    indices = {"x": list(range(65536, 68305)), "w": list(range(61440, 72401)),
               "z": [*range(61440, 65536), *range(68305, 72401)]}
    grid = windows["grid"]
    require(grid["central_source_indices"] == indices["x"] and grid["extended_source_indices"] == indices["w"] and
            grid["context_source_indices"] == indices["z"] and grid["central_sample_indices"] == list(range(N)),
            "synthetic original/central/context indices differ")
    require(grid["central_source_slice"] == [65536, 68305] and grid["extended_source_slice"] == [61440, 72401] and
            grid["left_source_slice"] == [61440, 65536] and grid["right_source_slice"] == [68305, 72401] and
            grid["central_offset_step_exact"] == "1/4096" and
            grid["central_offset_end_exact"] == str(F(N, 4096)) and
            grid["central_offset_last_exact"] == str(F(N - 1, 4096)), "window clock/slices differ")
    checked = 0
    array_pins = {}
    for key, expected_values in expected.items():
        actual = tuple(windows[key])
        hexes = [value.hex() for value in expected_values]
        require([value.hex() for value in actual] == hexes, "indexed values or signed zeros differ")
        record = context.array_record(actual)
        pin = {"shape": [len(actual)], "dtype": "little-endian binary64", "order": "C",
               **identity(b"".join(struct.pack("<d", value) for value in expected_values))}
        require(record == {"values_hex": hexes, "array_identity": pin}, "canonical source/output export differs")
        for offset, source_index in enumerate(indices[key]):
            require(actual[offset].hex() == values[source_index].hex(), "individual source coordinate differs")
            if key == "x":
                require(F(1126259446) + F(source_index, 4096) == F(1126259462) + F(offset, 4096),
                        "central rational clock differs")
            checked += 1
        array_pins[key] = pin
    require([v.hex() for v in windows["w"]] == [v.hex() for v in (*windows["z"][:L], *windows["x"], *windows["z"][L:])],
            "signed-zero injection identity differs")
    require(identity(b"".join(struct.pack("<d", value) for value in values)) == before, "window operation mutated source")
    crop, processing, inspections, raw = synthetic_crop(admitted, tuple(values))
    records = context.validate_crop(crop, processing, inspections, raw, admitted["shared"])
    require_crop_prefix(records, expected["x"], context)
    # A controlled one-sample selection error retains internally consistent
    # array identities, so the independent source-index comparison must reject.
    shifted = tuple(float.fromhex(value) for value in crop["detectors"][0]["values_hex"][1:N + 1])
    shifted_records = tuple({**record, "baseline": shifted,
                             "baseline_identity": context.array_identity(shifted)} for record in records)
    refused = expect_refusal(lambda: require_crop_prefix(shifted_records, expected["x"], context),
                             "crop baseline prefix differs from original central source indices")
    return {"case": name, "source_length": SOURCE_COUNT, "retained_coordinates_checked": checked,
            "central_clocks_checked": N, "arrays": array_pins, "signed_zero_variant": "zeros" in name,
            "crop_prefix_coordinates_checked": 2 * N, "crop_prefix_off_by_one_refused": refused["refused"]}


def require_crop_prefix(records, expected, context):
    require(type(records) is tuple and [record["detector"] for record in records] == ["H1", "L1"],
            "indexed crop detector order differs")
    for record in records:
        require([value.hex() for value in record["baseline"]] == [value.hex() for value in expected] and
                record["baseline_identity"] == context.array_identity(expected),
                "crop baseline prefix differs from original central source indices")


def toy_case(config, central, side, admitted):
    context = admitted["context"]
    oracle = admitted["shared"]["numeric"]["oracle"]
    total = central + 2 * side
    stages, pads = config["stages"], config["padlens"]
    sm = oracle.matrix_fraction(central, stages, pads)
    lm = oracle.matrix_fraction(total, stages, pads)
    original_x = tuple(F(j - 2, 8) for j in range(central))
    original_z = tuple(F((-1) ** k * (k + 1), 16) for k in range(2 * side))
    point_rows = broad_rows = 0
    for zero_x, zero_z in ((False, False), (True, False), (False, True), (True, True)):
        x = (F(0),) * central if zero_x else original_x
        z = (F(0),) * (2 * side) if zero_z else original_z
        w = z[:side] + x + z[side:]
        exact_short = oracle.forward_fraction(x, stages, pads)
        exact_context = oracle.forward_fraction(w, stages, pads)[side:side + central]
        for i in range(central):
            short_row, long_row = sm[i], lm[side + i]
            exact_delta = exact_context[i] - exact_short[i]
            for broad in (False, True):
                def bounds(row):
                    return tuple((v - F(j % 3 + 1, 1024), v + F(j % 3 + 1, 1024)) if broad else (v, v)
                                 for j, v in enumerate(row))
                s, v = bounds(short_row), bounds(long_row)
                a = tuple((v[side + j][0] - s[j][1], v[side + j][1] - s[j][0]) for j in range(central))
                b = v[:side] + v[side + central:]
                short = context.interval_dot(s, x); extended = context.interval_dot(v, w)
                center = context.interval_dot(a, x); surrounding = context.interval_dot(b, z)
                direct = (center[0] + surrounding[0], center[1] + surrounding[1])
                difference = context.interval_sub(extended, short)
                for interval, value in ((short, exact_short[i]), (extended, exact_context[i]),
                                        (direct, exact_delta), (difference, exact_delta)):
                    contains(interval, value)
                require(max(direct[0], difference[0]) <= min(direct[1], difference[1]), "toy decompositions disjoint")
                # Independent signed endpoint reduction, not just containment.
                for coefficients, vector, returned in ((s, x, short), (v, w, extended), (a, x, center), (b, z, surrounding)):
                    products = [(lo * value, hi * value) for (lo, hi), value in zip(coefficients, vector)]
                    expected = (sum((min(pair) for pair in products), F(0)), sum((max(pair) for pair in products), F(0)))
                    require(returned == expected, "signed or unequal-radius interval reduction differs")
                if broad:
                    broad_rows += 1
                    if not any(w):
                        require(direct == (F(0), F(0)), "zero broad-interval input not exact zero")
                else:
                    row = {"row": i, "a": a, "b": b, "short": {"intervals": s}, "long": {"intervals": v}}
                    result = context.selected_row_result(tuple(map(float, x)), tuple(map(float, w)), tuple(map(float, z)),
                        tuple(map(float, exact_short)), tuple(map(float, exact_context)), row, side)
                    require(result["passed"] is True and decoded(result["short_output_interval"]) == short and
                            decoded(result["context_output_interval"]) == extended and
                            decoded(result["direct_delta_interval"]) == direct and
                            decoded(result["output_difference_interval"]) == difference and
                            all(gate["passed"] is True for gate in result["endpoint_gates"].values()),
                            "point-row consumer result differs")
                    require(F(result["direct_delta_width_limit_exact"]) == max(map(abs, w)) / 10**12,
                            "point-row width scale changed")
                    point_rows += 1
    return {"configuration": config["name"], "central": central, "side": side, "input_combinations": 4,
            "forward_basis_columns": central + total, "point_rows": point_rows, "broad_interval_rows": broad_rows,
            "broad_radius_rule": "((coordinate mod 3)+1)/1024; containment only, not actual width admission"}


def controls(name, admitted):
    context = admitted["context"]
    if name == "endpoint_outside_pass":
        point = F(1) + F(1, 2**40)
        result = context.endpoint_gate(point, (F(1), F(1)), F(1, 10**9))
        require(result["passed"] is True and F(result["distance_bound_exact"]) == F(1, 2**40), "outside-point pass failed")
        return {"point_outside_interval": True, "gate": result}
    if name == "endpoint_outside_fail":
        return expect_refusal(lambda: context.endpoint_gate(F(1) + F(1, 2**20), (F(1), F(1)), F(1, 10**9)))
    if name == "nominal_all_ties":
        left, right = (1.0, -1.0, -0.0, 0.0), (0.0, 0.0, 1.0, -1.0)
    else:
        left, right = (0.1, -0.1, -0.0, 0.0), (0.3, 0.2, 0.0, -0.0)
    expected = tuple(F.from_float(a) - F.from_float(b) for a, b in zip(left, right))
    maximum = max(map(abs, expected))
    result = context.nominal_differences(left, right)
    require(result["values_exact"] == [str(v) for v in expected] and
            result["maximum_absolute_difference_exact"] == str(maximum) and
            result["maximizing_indices"] == [i for i, value in enumerate(expected) if abs(value) == maximum],
            "exact nominal reduction or complete maximizers differ")
    return result


def common_record(admitted):
    shared = admitted["shared"]
    return {"schema_version": "ri64-consumer-qualification-v1", "source_identity": identity(Path(__file__).read_bytes()),
        "context_identity": CONTEXT_PIN, "design_identity": DESIGN_PIN,
        "ri60_qualification_identity": RI60_PIN, "ri60_prior_gates": {"total": 196, "status": "previously_passed_not_rerun_here"},
        "published_dependency_identities": shared["dependency_identities"], "runtime": shared["runtime"],
        "dimensions": {"source_count": SOURCE_COUNT, "N": N, "L": L, "T": T}, "rows": list(ROWS),
        "gate_inventory": inventory(), "scope": "New consumer synthetic/index/interval/custody controls only. No observed sample/crop access or new admitted coefficient-row computation."}


def validate_qualification(report, admitted):
    require(type(report) is dict, "missing current consumer qualification")
    for key, value in common_record(admitted).items():
        require(canonical(report.get(key)) == canonical(value), "consumer qualification mismatch: " + key)
    ids = inventory()
    require(report.get("status") == "all_consumer_gates_passed" and
            canonical(report.get("gate_counts")) == canonical({"total": len(ids), "passed": len(ids), "failed": 0}),
            "current consumer qualification failed or incomplete")
    gates = report.get("gates")
    require(type(gates) is list and [g["id"] for g in gates] == ids and all(g["passed"] is True for g in gates),
            "consumer gate coverage differs")
    for gate in gates:
        parts = gate["id"].split(":")
        detail = gate["detail"]
        if parts[0] == "toy":
            central, side = int(parts[2]), int(parts[3])
            require(detail["configuration"] == parts[1] and detail["central"] == central and detail["side"] == side and
                    detail["input_combinations"] == 4 and detail["point_rows"] == 4 * central and
                    detail["broad_interval_rows"] == 4 * central and detail["forward_basis_columns"] == 2 * central + 2 * side,
                    "toy subcase coverage changed")
        if parts[0] == "index":
            require(detail["case"] == parts[1] and detail["source_length"] == SOURCE_COUNT and
                    detail["retained_coordinates_checked"] == N + T + 2 * L and detail["central_clocks_checked"] == N and
                    detail["crop_prefix_coordinates_checked"] == 2 * N and detail["crop_prefix_off_by_one_refused"] is True,
                    "index subcase coverage changed")
        if parts[0] == "refusal":
            require(detail["refused"] is True, "controlled invalid request accepted")
    return True


def synthetic_receipt(admitted):
    """A validator fixture only, never returned as executed qualification."""
    gates = []
    for identifier in inventory():
        parts = identifier.split(":")
        if parts[0] == "toy":
            central, side = int(parts[2]), int(parts[3])
            detail = {"configuration": parts[1], "central": central, "side": side,
                      "input_combinations": 4, "point_rows": 4 * central,
                      "broad_interval_rows": 4 * central, "forward_basis_columns": 2 * central + 2 * side}
        elif parts[0] == "index":
            detail = {"case": parts[1], "source_length": SOURCE_COUNT,
                      "retained_coordinates_checked": N + T + 2 * L, "central_clocks_checked": N,
                      "crop_prefix_coordinates_checked": 2 * N, "crop_prefix_off_by_one_refused": True}
        else:
            detail = {"refused": True} if parts[0] == "refusal" else {}
        gates.append({"id": identifier, "passed": True, "detail": detail})
    fixture = {**common_record(admitted), "gates": gates, "status": "all_consumer_gates_passed",
               "gate_counts": {"total": len(gates), "passed": len(gates), "failed": 0}}
    validate_qualification(fixture, admitted)
    return fixture


def numerical_threshold_fixture(context):
    """Exercise the complete-array consumer with synthetic identity outputs."""
    import numpy as np
    values = (2.0**-20, -2.0**-21, 0.0, -0.0)
    stages = [{"sos": np.array([[1.0, 0.0, 0.0, 1.0, 0.0, 0.0]], dtype=np.float64)}]
    calls = []
    def coefficients(numeric):
        calls.append("mock_coefficients")
    def production(source, passed_stages):
        require(passed_stages is stages, "mock stages changed")
        return source.copy()
    def reference(passed_values, matrices, pads):
        require(passed_values == list(values) and pads == [0], "mock reference inputs changed")
        return [Decimal.from_float(value) for value in passed_values]
    numeric = {"production": SimpleNamespace(apply_filter=production),
               "reference": SimpleNamespace(reference_filter=reference), "stages": stages, "padlens": [0]}
    admitted = {"numeric": numeric, "ri60_check": SimpleNamespace(check_coefficients=coefficients)}
    output, diagnostic = context.complete_numeric(values, admitted)
    require([v.hex() for v in output] == [v.hex() for v in values] and diagnostic["passed"] is True and
            diagnostic["input_peak_exact"] == str(F(1, 2**20)) and
            diagnostic["limit_exact"] == str(F(1, 2**20 * 10**9)) and
            diagnostic["maximum_absolute_residual_exact"] == "0" and len(calls) == 2,
            "synthetic complete-vector passing control differs")
    def displaced(source, passed_stages):
        result = production(source, passed_stages)
        result[0] += 2.0**-40
        return result
    numeric["production"] = SimpleNamespace(apply_filter=displaced)
    result = expect_refusal(lambda: context.complete_numeric(values, admitted))
    require(F(1, 2**40) > F(1, 2**20 * 10**9) and F(1, 2**40) < F(1, 10**9),
            "fixture no longer distinguishes subunit peak from a unit floor")
    zero_values = (0.0, -0.0, 0.0, -0.0)
    numeric["production"] = SimpleNamespace(apply_filter=production)
    numeric["reference"] = SimpleNamespace(reference_filter=lambda values, matrices, pads:
        [Decimal.from_float(value) for value in values])
    zero_output, zero_check = context.complete_numeric(zero_values, admitted)
    require([v.hex() for v in zero_output] == [v.hex() for v in zero_values] and
            zero_check["exact_zero_required"] is True and zero_check["exact_zero_output_and_reference"] is True and
            zero_check["limit_exact"] == zero_check["maximum_absolute_residual_exact"] == "0",
            "complete-vector signed-zero control differs")
    numeric["production"] = SimpleNamespace(apply_filter=displaced)
    expect_refusal(lambda: context.complete_numeric(zero_values, admitted))
    return {**result, "passing_control": True, "sample_count": 4,
            "input_peak_exact": str(F(1, 2**20)), "limit_exact": str(F(1, 2**20 * 10**9)),
            "rejected_residual_exact": str(F(1, 2**40)), "no_unit_floor": True,
            "signed_zero_control": True, "nonzero_output_for_zero_input_refused": True}


def synthetic_crop(admitted, source_values=None):
    """Fabricated indexed/zero arrays and retained metadata, never observations.

    With an indexed source, the synthetic crop is an identity-transform slice.
    This controls subset/index custody; it makes no claim about filtering it.
    """
    context, shared = admitted["context"], admitted["shared"]
    ri47 = shared["ri47"]
    inspections = copy.deepcopy(shared["custody"]["baseline"]["detectors"])
    raw = ((0.0,) * SOURCE_COUNT if source_values is None else source_values,) * 2
    crop_values = raw[0][65536:69632]
    sources = {"process": {"filename": "process.py", **{k: context.DEPENDENCIES["ri47_process"][k] for k in ("bytes", "sha256")}},
               "published_dependencies": ri47.DEPENDENCIES}
    entries, reports = [], []
    for detector, inspection in zip(("H1", "L1"), inspections):
        annotation = ri47.annotation(inspection, detector)
        crop_id = context.array_identity(crop_values)
        entries.append({"detector": detector, "input_filename": inspection["filename"], "input_identity": inspection["identity"],
                        "annotations": annotation, "values_hex": [value.hex() for value in crop_values], "crop_identity": crop_id})
        reports.append({"detector": detector, "input_filename": inspection["filename"], "input_file_identity": inspection["identity"],
                        "annotations": annotation, "input_inspection": inspection, "input_array_identity": context.array_identity(raw[0]),
                        "crop_identity": crop_id})
    crop = {"schema_version": "ri47-nominal-strain-crop-v1", "event": "GW150914", "quantity": "nominal dimensionless strain",
            "source_product": "GWOSC V2", "coefficient_manifest_sha256": context.MANIFEST_SHA256, "recipe_sha256": ri47.RECIPE_SHA256,
            "grid": ri47.grid(), "source_identity": sources, "processing": {"synthetic_fixture": True}, "detectors": entries}
    processing = {"schema_version": "ri47-nominal-processing-report-v1", "status": "admitted_nominal_processing_completed",
            "event": "GW150914", "source_identity": sources, "grid": ri47.grid(), "current_processing_runtime": shared["runtime"],
            "processing": crop["processing"], "exported_crop_file": {"filename": "CROP.json", **{k: context.OBSERVED_DEPENDENCIES["crop"][k] for k in ("bytes", "sha256")}},
            "detectors": reports}
    require(len(context.validate_crop(crop, processing, inspections, raw, shared)) == 2, "synthetic crop control invalid")
    return crop, processing, inspections, raw


def refusal_case(name, admitted):
    context, shared = admitted["context"], admitted["shared"]
    old = shared["ri60_check"]
    if name == "source_changed":
        return expect_refusal(lambda: context.verify_snapshot(b"abd", identity(b"abc")))
    if name == "source_missing":
        with TemporaryDirectory(prefix="ri64-missing-") as directory:
            return expect_refusal(lambda: context.bound_bytes(Path(directory) / "absent", identity(b"abc")))
    if name in ("coefficients", "stage_order", "padding"):
        numeric = dict(shared["numeric"]); numeric["stages"] = copy.deepcopy(numeric["stages"])
        if name == "coefficients":
            numeric["stages"][0]["sos"][0, 0] *= 2
        elif name == "stage_order":
            numeric["stages"][1], numeric["stages"][2] = numeric["stages"][2], numeric["stages"][1]
        else:
            numeric["stages"][0]["padlen"] += 1
        return expect_refusal(lambda: old.check_coefficients(numeric))
    if name.startswith("current_receipt"):
        report = None if name.endswith("missing") else synthetic_receipt(admitted)
        if report is not None:
            if name.endswith("failed"):
                report["status"] = "consumer_qualification_failed"
            if name.endswith("stale"):
                report["context_identity"] = {"bytes": 1, "sha256": "0" * 64}
        return expect_refusal(lambda: validate_qualification(report, admitted))
    if name.startswith("ri60_receipt"):
        report = dict(shared["qualification60"])
        if name.endswith("failed"):
            report["status"] = "context_qualification_failed"
        else:
            report["schema_version"] = "ri57-context-qualification-v1"
        return expect_refusal(lambda: old.validate_qualification(report, shared["numeric"]))
    if name == "runtime_mismatch":
        changed = dict(shared); changed["runtime"] = {"changed": True}
        return expect_refusal(lambda: context._numeric_state(changed))
    if name == "unreconciled_rows":
        changed = dict(shared); changed["_row_token"] = None
        return expect_refusal(lambda: context.read_verified_inputs(Path("not-opened"), changed))
    if name == "resource_exhaustion":
        oracle = shared["numeric"]["oracle"]
        cfg = oracle.toy_configurations()[0]
        return expect_refusal(lambda: shared["numeric"]["engine"].forward_fraction((F(0),) * 65, cfg["stages"], cfg["padlens"]))
    if name.startswith("input_"):
        original = b"synthetic-H1"
        expected = {"filename": "synthetic.bin", "bytes": len(original), "md5": hashlib.md5(original).hexdigest(),
                    "sha256": hashlib.sha256(original).hexdigest()}
        with TemporaryDirectory(prefix="ri64-byte-fixture-") as directory:
            if name != "input_missing":
                data = {"input_swapped": b"synthetic-L1", "input_truncated": original[:-1],
                        "input_corrupt_same_size": b"Synthetic-H1"}[name]
                (Path(directory) / expected["filename"]).write_bytes(data)
            return expect_refusal(lambda: shared["custody"]["inspector"]._verified_bytes(Path(directory), expected))
    if name in ("grid_mismatch", "nonfinite_samples", "data_inconsistency", "altered_flags", "altered_annotations",
                "crop_values_changed", "crop_identity_changed"):
        crop, processing, inspections, raw = synthetic_crop(admitted)
        if name == "grid_mismatch":
            crop["grid"]["source_crop"][0] += 1
        elif name == "nonfinite_samples":
            raw = ((float("nan"),) + raw[0][1:], raw[1])
        elif name == "data_inconsistency":
            inspections[0]["missing_and_excluded_by_DATA"] = {"synthetic_changed": True}
        elif name == "altered_flags":
            inspections[1]["hardware_injection_flags"] = {"synthetic_changed": True}
        elif name == "altered_annotations":
            crop["detectors"][1]["annotations"]["cw_display_annotation"] = "incorrectly suppressed"
        elif name == "crop_values_changed":
            crop["detectors"][0]["values_hex"][0] = "0x1.0000000000000p+0"
        else:
            crop["detectors"][0]["crop_identity"] = {"changed": True}
        return expect_refusal(lambda: context.validate_crop(crop, processing, inspections, raw, shared))
    if name == "index_shift":
        with patched(context, "CENTER_START", 65537):
            return expect_refusal(lambda: context.extract_windows((0.0,) * SOURCE_COUNT))
    if name == "output_exists":
        with TemporaryDirectory(prefix="ri64-output-fixture-") as directory:
            return expect_refusal(lambda: external_destination(Path(directory)))
    if name == "interval_misses_exact":
        return expect_refusal(lambda: contains(context.interval((F(0), F(1))), F(2)))
    if name == "interval_reversed":
        return expect_refusal(lambda: context.interval((F(1), F(0))))
    if name == "interval_overwide":
        return expect_refusal(lambda: context.require_width((F(-1), F(1)), F(1, 10**12)))
    if name == "numerical_threshold":
        return numerical_threshold_fixture(context)
    if name == "midpoint_only":
        return expect_refusal(lambda: context.endpoint_gate(F(1), (F(0), F(2)), F(1, 10**9)))
    if name == "overlap_only":
        return expect_refusal(lambda: context.endpoint_gate(F(0), (F(-1, 10**10), F(1)), F(1, 10**9)))
    if name == "both_inputs_bound_before_parse":
        calls = []
        parser_calls = []
        def verify(directory, expected):
            calls.append(expected["detector"])
            if expected["detector"] == "L1":
                raise ValueError("controlled second-snapshot mismatch")
            return b"synthetic first snapshot"
        def parser(*args):
            parser_calls.append(True)
            raise RuntimeError("parser must not be reached before both raw identities bind")
        inspector = SimpleNamespace(FILES=({"detector": "H1"}, {"detector": "L1"}),
                                    _verified_bytes=verify, _inspect=parser)
        fixture = {"custody": {"inspector": inspector}}
        with patched(context, "_require_rows", lambda admitted: None):
            result = expect_refusal(lambda: context.read_verified_inputs(Path("not-opened"), fixture))
        require(calls == ["H1", "L1"] and not parser_calls, "both-snapshot binding/parse order changed")
        return {**result, "verified_attempt_order": calls, "parser_calls": len(parser_calls),
                "row_prerequisite_mocked_only_for_synthetic_order_control": True}
    raise ValueError("unknown frozen refusal")


def run_checks(admitted):
    gates = []
    context, shared = admitted["context"], admitted["shared"]
    configs = shared["numeric"]["oracle"].toy_configurations()
    require(tuple(config["name"] for config in configs) == TOYS, "published oracle configuration inventory changed")
    by_name = {config["name"]: config for config in configs}
    for identifier in inventory():
        parts = identifier.split(":")
        try:
            if parts[0] == "index":
                detail = indexed_case(parts[1], admitted)
            elif parts[0] == "toy":
                detail = toy_case(by_name[parts[1]], int(parts[2]), int(parts[3]), admitted)
            elif parts[0] == "control":
                detail = controls(parts[1], admitted)
            else:
                detail = refusal_case(parts[1], admitted)
            gates.append({"id": identifier, "passed": True, "detail": detail})
        except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
            gates.append({"id": identifier, "passed": False,
                          "detail": {"error_type": type(error).__name__, "error": str(error)}})
    # Check that controlled mutations were restored; this does not compute rows.
    context._numeric_state(shared)
    failed = sum(gate["passed"] is not True for gate in gates)
    return {**common_record(admitted), "gates": gates,
        "status": "all_consumer_gates_passed" if failed == 0 else "consumer_qualification_failed",
        "gate_counts": {"total": len(gates), "passed": len(gates) - failed, "failed": failed}}


def main():
    require(len(sys.argv) == 1, "check.py takes no arguments and opens no observed input")
    report = run_checks(admission())
    sys.stdout.buffer.write(export_json(report))
    return 0 if report["status"] == "all_consumer_gates_passed" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
        print("observed-context qualification refused: " + str(error), file=sys.stderr)
        raise SystemExit(1)
