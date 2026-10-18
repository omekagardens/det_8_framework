"""Closed RI-78 scientific schema and numerical-consistency validator.

This stdlib-only consumer imports no producer, FFT or data file. Shape, byte and
internal-consistency checks are not proof of observed provenance: the caller
must independently bind inputs, admitted qualification and execution custody.
"""
from __future__ import annotations

import hashlib
import json
import math
import struct

EPS = 2.0 ** -52
TAU = 2.0 ** -40
DESIGN_PIN = {"bytes": 24390, "sha256": "3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce"}
REPORT_PIN = {"bytes": 31096, "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80"}
RECOVERY_PIN = {"bytes": 16293, "sha256": "be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0"}
INPUTS = (
    ("H1", "H-H1_LOSC_4_V2-1126259446-32.hdf5", 1040592, "50441a42c13fc1f14e5c4ea5527f1515", "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6"),
    ("L1", "L-L1_LOSC_4_V2-1126259446-32.hdf5", 1007420, "361ae6a040a9fef7897b1e0124d5b0a1", "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189"),
)
LIMITATIONS = [
    "Known public development inputs with prior display and context access; not blind/protected validation.",
    "Nominal released V2/C02 strain; literal Yunits is empty; no extra calibration correction or uncertainty band.",
    "L1 NO_CW_HW_INJ is clear throughout; continuous-wave injection absence/effect is not established.",
    "Off-event names the fixed exclusion only; short overlapping sides have unequal seven/six segment counts.",
    "Finite descriptive spectra do not establish signal-free data, stationarity, Gaussianity or detector independence.",
    "Estimated spectra are not known covariance, unit-white covariance, whitening, a chi-square law or significance.",
    "Calibration/timing/mean-response/noise-estimation premises and a native forward map remain separate prerequisites.",
    "Retained bins below 10 Hz have no added calibrated physical interpretation; no RET work is implied.",
]


class ValidationError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(f"{code}: {message}")


def need(condition, code, message):
    if not condition:
        raise ValidationError(code, message)


def canonical(value):
    try:
        return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")
    except (ValueError, TypeError, OverflowError) as exc:
        raise ValidationError("SCHEMA", "not finite canonical JSON") from exc


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "SCHEMA", "duplicate JSON key")
        result[key] = value
    return result


def load_result(payload):
    """Decode only a canonical finite UTF-8 byte result, rejecting duplicates."""
    need(type(payload) is bytes and len(payload) <= 64 * 1024 * 1024, "SCHEMA", "result bytes or cap")
    try:
        value = json.loads(payload.decode("utf-8"), object_pairs_hook=_pairs,
                           parse_constant=lambda s: (_ for _ in ()).throw(ValidationError("NONFINITE", s)))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError("SCHEMA", "invalid UTF-8 JSON") from exc
    need(canonical(value) == payload, "SCHEMA", "noncanonical result serialization")
    validate_result(value)
    return value


def obj(value, keys, label):
    need(type(value) is dict and set(value) == set(keys), "SCHEMA", label + " keys")
    return value


def seq(value, length, label):
    need(type(value) is list and len(value) == length, "SCHEMA", label + " length")
    return value


def exact(actual, expected, label):
    # Canonical bytes distinguish bool/int and integer/float metadata values.
    need(canonical(actual) == canonical(expected), "SCHEMA", label + " differs")


def number(value):
    need(type(value) is str, "SCHEMA", "scientific float must be a hex string")
    try:
        result = float.fromhex(value)
    except (ValueError, OverflowError) as exc:
        raise ValidationError("SCHEMA", "invalid float hex") from exc
    need(math.isfinite(result), "NONFINITE", "nonfinite scientific scalar")
    need(result.hex() == value, "SCHEMA", "noncanonical float hex")
    return result


def digest(value):
    need(type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value), "IDENTITY", "SHA-256 syntax")


def check_pin(value):
    obj(value, ("bytes", "sha256"), "pin")
    need(type(value["bytes"]) is int and value["bytes"] > 0, "IDENTITY", "pin byte count")
    digest(value["sha256"])


def finite_sum(values):
    try:
        value = math.fsum(values)
    except (OverflowError, ValueError) as exc:
        raise ValidationError("NONFINITE", "scalar accumulation failed") from exc
    need(math.isfinite(value), "NONFINITE", "nonfinite scalar sum")
    return value


def indices():
    return {
        "left": {"interval": [0, 65536], "starts": [0, 8192, 16384, 24576, 32768, 40960, 49152],
                 "count": 7, "used_interval": [0, 65536], "unused_intervals": []},
        "right": {"interval": [69632, 131072], "starts": [69632, 77824, 86016, 94208, 102400, 110592],
                  "count": 6, "used_interval": [69632, 126976], "unused_intervals": [[126976, 131072]]},
    }


def method():
    return {
        "design_pin": DESIGN_PIN.copy(), "fs": 4096, "segment_length": 16384, "stride": 8192,
        "nfft": 16384, "exclusion": [65536, 69632], "sides": indices(), "bins": 8193,
        "endpoint_weights": [1, 1], "interior_weight": 2, "delta_f_hex": (0.25).hex(),
        "detrend": "arithmetic_per_segment_mean_before_window", "window": "periodic_hann_sym_false",
        "fft": "numpy_rfft_backward", "scaling": "density_fs_times_actual_window_energy",
        "average": "arithmetic_mean_periodograms", "asd": "sqrt_mean_psd",
        "eps_hex": EPS.hex(), "tau_hex": TAU.hex(), "sqrt_relative_budget_hex": (8 * EPS).hex(),
    }


def validate_result(result):
    """Return True only for the complete fixed schema and all numerical gates."""
    obj(result, ("schema", "method", "inputs", "frequency_hz", "window", "detectors", "checks", "limitations"), "result")
    exact(result["schema"], "ri78-off-event-spectra-v1", "schema")
    exact(result["method"], method(), "method")
    exact(result["limitations"], LIMITATIONS, "limitations")
    cache = {}

    def array(record, size, nonnegative=False):
        obj(record, ("dtype", "shape", "values_hex", "sha256"), "array")
        exact(record["dtype"], "<f8", "array dtype")
        exact(record["shape"], [size], "array shape")
        seq(record["values_hex"], size, "array values")
        digest(record["sha256"])
        if id(record) not in cache:
            values = tuple(number(x) for x in record["values_hex"])
            body = b"".join(struct.pack("<d", x) for x in values)
            need(hashlib.sha256(body).hexdigest() == record["sha256"], "IDENTITY", "array byte hash")
            cache[id(record)] = values
        values = cache[id(record)]
        if nonnegative:
            need(all(v >= 0 for v in values), "NEGATIVE_PSD", "negative array value")
        return values

    def scalar_record(record, keys):
        obj(record, keys, "numeric record")
        return {key: number(record[key]) for key in keys}

    def scales(q):
        need(q >= 0, "ZERO_POWER", "negative Q")
        scale = q / 0.25
        need(math.isfinite(scale), "NONFINITE", "power scale overflow")
        need(q == 0 or (TAU * scale > 0 and TAU * q > 0), "UNDERFLOW", "power scale vanished")
        return TAU * scale, TAU * q

    def comparison(record, candidate, reference, q):
        obj(record, ("absolute_residual", "threshold"), "comparison")
        errors = array(record["absolute_residual"], 8193, True)
        threshold = number(record["threshold"])
        exact(threshold.hex(), scales(q)[0].hex(), "PSD threshold")
        for p, r, e in zip(candidate, reference, errors):
            need(e == abs(p - r) and e <= threshold, "TOLERANCE", "all-bin PSD discrepancy")
            if q == 0:
                need(p == 0 and r == 0, "ZERO_POWER", "zero-power bin")

    def parseval(record, psd, q):
        values = scalar_record(record, ("integral", "power", "absolute_residual", "threshold"))
        integral = 0.25 * finite_sum(psd)
        residual = abs(integral - q)
        exact(values["power"].hex(), q.hex(), "Parseval Q")
        exact(values["integral"].hex(), integral.hex(), "Parseval integral")
        exact(values["absolute_residual"].hex(), residual.hex(), "Parseval error")
        exact(values["threshold"].hex(), scales(q)[1].hex(), "Parseval limit")
        need(residual <= values["threshold"], "TOLERANCE", "Parseval failed")
        if q == 0:
            need(all(p == 0 for p in psd), "ZERO_POWER", "zero-power periodogram")

    frequency = array(result["frequency_hz"], 8193)
    need(all(value == k / 4 for k, value in enumerate(frequency)), "BINS", "frequency grid")
    obj(result["window"], ("values", "checks"), "window")
    window = array(result["window"]["values"], 16384)
    wc = result["window"]["checks"]
    obj(wc, ("sum", "w2", "sum_reference", "w2_reference", "sum_ideal_residual", "sum_threshold",
             "w2_ideal_residual", "w2_threshold", "formula_residual", "formula_threshold"), "window checks")
    ws, w2 = finite_sum(window), finite_sum(w * w for w in window)
    need(w2 > 0, "ZERO_POWER", "empty window energy")
    exact(number(wc["sum_reference"]).hex(), ws.hex(), "window independent sum")
    exact(number(wc["w2_reference"]).hex(), w2.hex(), "window independent energy")
    need(abs(number(wc["sum"]) - ws) <= TAU * 8192, "TOLERANCE", "window production sum")
    need(abs(number(wc["w2"]) - w2) <= TAU * 6144, "TOLERANCE", "window production energy")
    for label, value, ideal in (("sum", ws, 8192), ("w2", w2, 6144)):
        exact(number(wc[label + "_ideal_residual"]).hex(), abs(value - ideal).hex(), "window ideal residual")
        exact(number(wc[label + "_threshold"]).hex(), (TAU * ideal).hex(), "window ideal limit")
        need(abs(value - ideal) <= TAU * ideal, "TOLERANCE", "window ideal identity")
    formula_errors = array(wc["formula_residual"], 16384, True)
    exact(number(wc["formula_threshold"]).hex(), (16 * EPS).hex(), "window formula threshold")
    for j, (w, err) in enumerate(zip(window, formula_errors)):
        expected = (1 - math.cos(2 * math.pi * j / 16384)) / 2
        need(err == abs(w - expected) and err <= 16 * EPS, "TOLERANCE", "periodic window formula")

    input_records = seq(result["inputs"], 2, "inputs")
    admitted_metadata = []
    for row, (detector, filename, size, md5, sha256) in zip(input_records, INPUTS):
        obj(row, ("detector", "filename", "bytes", "md5", "sha256", "url", "ri37_detector", "inspector_report_pin", "recovery_handoff_pin"), "input")
        for key, value in (("detector", detector), ("filename", filename), ("bytes", size), ("md5", md5),
                           ("sha256", sha256), ("url", "https://gwosc.org/GW150914data/" + filename),
                           ("inspector_report_pin", REPORT_PIN), ("recovery_handoff_pin", RECOVERY_PIN)):
            exact(row[key], value, "fixed input " + key)
        admitted_metadata.append(row["ri37_detector"])
    # Reassemble the complete published report; its fixed canonical SHA closes
    # every nested metadata/flag field, including spelling and the L1 clear bit.
    report = {"schema_version": "gwosc-fixed-pair-qualification-v1", "status": "identity_and_structure_verified",
              "event": "GW150914", "strain_product_version": "V2", "detectors": admitted_metadata,
              "interpretation_boundary": {
                  "dimensionless_strain": "publisher interpretation; the literal strain Yunits attribute is empty",
                  "C02_calibration": "external publisher release identification, not a literal calibration header",
                  "calibration_uncertainty": "applicable artifact values, interpolation and correlations remain unqualified",
                  "scientific_fit_readiness": "not established by identity, structure, finite samples or quality flags",
                  "prior_access": "known public reference event; not blind evaluation data",
                  "native_gravity_comparison": "no native forward law or DET-versus-GR inference supplied"}}
    report_bytes = canonical(report)
    need(len(report_bytes) == REPORT_PIN["bytes"] and hashlib.sha256(report_bytes).hexdigest() == REPORT_PIN["sha256"],
         "METADATA", "complete pinned RI-37 metadata/flags changed")
    obj(result["checks"], ("identity", "detectors"), "checks")
    identity = obj(result["checks"]["identity"], ("inspector_report_pin", "recovery_handoff_pin", "qualification_report_pin", "fixed_dimensions_indices_and_flags"), "identity checks")
    exact(identity["inspector_report_pin"], REPORT_PIN, "inspector identity")
    exact(identity["recovery_handoff_pin"], RECOVERY_PIN, "recovery identity")
    check_pin(identity["qualification_report_pin"])
    exact(identity["fixed_dimensions_indices_and_flags"], True, "fixed dimensions gate")
    detectors = seq(result["detectors"], 2, "detectors")
    numerical = seq(result["checks"]["detectors"], 2, "detector checks")
    for detector_index, (row, checked) in enumerate(zip(detectors, numerical)):
        name = ("H1", "L1")[detector_index]
        for item in (row, checked):
            obj(item, ("detector", "sides"), "detector result/checks")
            exact(item["detector"], name, "detector order")
            seq(item["sides"], 2, "sides")
        for side_index, side in enumerate(("left", "right")):
            output, checks = row["sides"][side_index], checked["sides"][side_index]
            spec = indices()[side]
            obj(output, ("side", "interval", "starts", "count", "used_interval", "unused_intervals", "segments", "mean_psd", "asd", "q", "psd_unit", "asd_unit"), "side result")
            exact(output["side"], side, "side name")
            for key, value in spec.items():
                exact(output[key], value, "fixed side " + key)
            exact(output["psd_unit"], "nominal_strain_squared_per_Hz", "PSD units")
            exact(output["asd_unit"], "nominal_strain_per_sqrt_Hz", "ASD units")
            obj(checks, ("side", "segments", "reference_psd", "reference_asd", "parseval", "comparison", "sqrt"), "side checks")
            exact(checks["side"], side, "check side name")
            segments = seq(output["segments"], spec["count"], "segments")
            segment_checks = seq(checks["segments"], spec["count"], "segment checks")
            powers, psds = [], []
            for segment, sc, start in zip(segments, segment_checks, spec["starts"]):
                obj(segment, ("start", "end", "gps_offset_numerators", "gps_offset_denominator", "flag_rows", "dq_masks", "injection_masks", "mean", "q", "raw_sha256", "demeaned_sha256", "windowed_sha256", "psd"), "segment")
                flag_rows = list(range(start // 4096, (start + 16384) // 4096))
                for key, value in (("start", start), ("end", start + 16384), ("gps_offset_numerators", [start, start + 16384]),
                                   ("gps_offset_denominator", 4096), ("flag_rows", flag_rows), ("dq_masks", [127] * 4),
                                   ("injection_masks", [(31, 23)[detector_index]] * 4)):
                    exact(segment[key], value, "segment " + key)
                for key in ("raw_sha256", "demeaned_sha256", "windowed_sha256"):
                    digest(segment[key])
                mean, q = number(segment["mean"]), number(segment["q"])
                psd = array(segment["psd"], 8193, True)
                powers.append(q)
                psds.append(psd)
                obj(sc, ("start", "mean", "parseval", "reference_psd", "comparison"), "segment checks")
                exact(sc["start"], start, "check segment start")
                mc = scalar_record(sc["mean"], ("actual", "reference", "input_peak", "absolute_residual", "threshold"))
                exact(mc["actual"].hex(), mean.hex(), "segment mean")
                need(mc["input_peak"] >= 0 and mc["threshold"] == TAU * mc["input_peak"]
                     and mc["absolute_residual"] == abs(mean - mc["reference"])
                     and mc["absolute_residual"] <= mc["threshold"], "TOLERANCE", "mean comparison")
                reference = array(sc["reference_psd"], 8193, True)
                comparison(sc["comparison"], psd, reference, q)
                parseval(sc["parseval"], psd, q)
            q = number(output["q"])
            exact(q.hex(), (finite_sum(powers) / spec["count"]).hex(), "side Q average")
            psd, asd = array(output["mean_psd"], 8193, True), array(output["asd"], 8193, True)
            mean_reference = tuple(finite_sum(p[k] for p in psds) / spec["count"] for k in range(8193))
            need(all(abs(p - r) <= scales(q)[0] for p, r in zip(psd, mean_reference)), "TOLERANCE", "arithmetic PSD mean")
            reference = array(checks["reference_psd"], 8193, True)
            reference_asd = array(checks["reference_asd"], 8193, True)
            comparison(checks["comparison"], psd, reference, q)
            parseval(checks["parseval"], psd, q)
            sqrt = obj(checks["sqrt"], ("pointwise_residual", "pointwise_threshold", "reference_residual", "reference_threshold"), "sqrt checks")
            errors = array(sqrt["pointwise_residual"], 8193, True)
            limits = array(sqrt["pointwise_threshold"], 8193, True)
            cross_errors = array(sqrt["reference_residual"], 8193, True)
            cross_limit = number(sqrt["reference_threshold"])
            expected_cross = math.sqrt(scales(q)[0]) + 8 * EPS * math.sqrt(q / 0.25)
            exact(cross_limit.hex(), expected_cross.hex(), "ASD reference limit")
            for p, a, r, ra, err, limit, cross_err in zip(psd, asd, reference, reference_asd, errors, limits, cross_errors):
                ideal = math.sqrt(p)
                need(ra == math.sqrt(r), "TOLERANCE", "reference ASD sqrt")
                need(err == abs(a - ideal) and limit == 8 * EPS * ideal and err <= limit, "TOLERANCE", "ASD pointwise sqrt")
                need(cross_err == abs(a - ra) and cross_err <= cross_limit, "TOLERANCE", "ASD reference discrepancy")
                if p == 0:
                    need(a == 0, "ZERO_POWER", "zero PSD/ASD")
    return True
