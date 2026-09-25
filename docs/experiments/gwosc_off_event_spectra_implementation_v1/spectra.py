"""Fixed RI-78 spectra; source-only until the coordinator freezes execution.

No input is opened at import. The caller owns pre-import source/runtime custody,
qualification admission, exclusive destinations, and the 180 s / 512 MiB sampled
RSS supervisor. This module neither authorizes nor launches an observed run.
"""
from __future__ import annotations

import copy
import functools
import hashlib
import io
import json
import math
from pathlib import Path

import h5py
import numpy as np
from scipy import signal

FS = 4096
M = 16384
STRIDE = 8192
N = 131072
EPS = 2.0 ** -52
TAU = 2.0 ** -40
DESIGN_PIN = {"bytes": 24390, "sha256": "3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce"}
REPORT_PIN = {"bytes": 31096, "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80"}
RECOVERY_PIN = {"bytes": 16293, "sha256": "be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0"}
INPUTS = (
    {"detector": "H1", "filename": "H-H1_LOSC_4_V2-1126259446-32.hdf5", "bytes": 1040592,
     "md5": "50441a42c13fc1f14e5c4ea5527f1515", "sha256": "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6"},
    {"detector": "L1", "filename": "L-L1_LOSC_4_V2-1126259446-32.hdf5", "bytes": 1007420,
     "md5": "361ae6a040a9fef7897b1e0124d5b0a1", "sha256": "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189"},
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


class SpectraError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(f"{code}: {message}")


def require(condition, code, message):
    if not condition:
        raise SpectraError(code, message)


def canonical(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def pin(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def fixed_indices():
    return {
        "left": {"interval": [0, 65536], "starts": [0, 8192, 16384, 24576, 32768, 40960, 49152],
                 "count": 7, "used_interval": [0, 65536], "unused_intervals": []},
        "right": {"interval": [69632, 131072], "starts": [69632, 77824, 86016, 94208, 102400, 110592],
                  "count": 6, "used_interval": [69632, 126976], "unused_intervals": [[126976, 131072]]},
    }


def method_contract():
    return {
        "design_pin": DESIGN_PIN.copy(), "fs": FS, "segment_length": M, "stride": STRIDE,
        "nfft": M, "exclusion": [65536, 69632], "sides": fixed_indices(), "bins": 8193,
        "endpoint_weights": [1, 1], "interior_weight": 2, "delta_f_hex": (0.25).hex(),
        "detrend": "arithmetic_per_segment_mean_before_window", "window": "periodic_hann_sym_false",
        "fft": "numpy_rfft_backward", "scaling": "density_fs_times_actual_window_energy",
        "average": "arithmetic_mean_periodograms", "asd": "sqrt_mean_psd",
        "eps_hex": EPS.hex(), "tau_hex": TAU.hex(), "sqrt_relative_budget_hex": (8 * EPS).hex(),
    }


@functools.lru_cache(maxsize=3)
def _window_bytes(size):
    require(size in (8, 16, M), "LENGTH", "unadmitted window length")
    return signal.windows.hann(size, sym=False).astype("<f8").tobytes(order="C")


def prepare_windows():
    """Materialize immutable window bytes before the observed-data freeze."""
    return {str(size): pin(_window_bytes(size)) for size in (8, 16, M)}


def _array(x, ndim, lengths=None):
    require(isinstance(x, np.ndarray), "DTYPE", "NumPy array required without implicit coercion")
    require(x.dtype == np.dtype("float64") and not np.iscomplexobj(x), "DTYPE", "real binary64 required")
    require(x.ndim == ndim, "DIMENSION", "unexpected array dimension")
    require(x.size > 0, "LENGTH", "empty array")
    if lengths is not None:
        require(x.shape[-1] in lengths, "LENGTH", "unsupported fixed length")
    require(bool(np.isfinite(x).all()), "NONFINITE", "nonfinite array value")
    return x


def _finite(x, label):
    require(math.isfinite(float(x)), "NONFINITE", label)
    return float(x)


def _sum(values):
    try:
        return _finite(math.fsum(float(x) for x in values), "nonfinite scalar sum")
    except OverflowError as exc:
        raise SpectraError("NONFINITE", "scalar accumulation overflow") from exc


def _power(values, denominator):
    squares = []
    for value in values:
        value = float(value)
        term = _finite(value * value, "square overflow")
        require(value == 0 or term > 0, "UNDERFLOW", "nonzero sample square vanished")
        squares.append(term)
    q = _finite(_sum(squares) / denominator, "power nonfinite")
    require(q > 0 or not any(float(v) != 0 for v in values), "UNDERFLOW", "nonzero vector power vanished")
    return q


def _scales(q, delta_f):
    q = _finite(q, "power scale")
    require(q >= 0, "ZERO_POWER", "negative power scale")
    require(delta_f in (0.25, 256.0, 512.0), "BINS", "unadmitted frequency spacing")
    if q == 0:
        return 0.0, 0.0, 0.0
    s = _finite(q / delta_f, "PSD scale")
    p_tol, q_tol = TAU * s, TAU * q
    require(s > 0 and p_tol > 0 and q_tol > 0, "UNDERFLOW", "positive tolerance scale vanished")
    return s, p_tol, q_tol


def check_psd(candidate, reference, q, delta_f):
    _array(candidate, 1)
    _array(reference, 1)
    require(candidate.shape == reference.shape and candidate.size in (5, 9, 8193), "BINS", "PSD bins differ")
    require(bool((candidate >= 0).all() and (reference >= 0).all()), "NEGATIVE_PSD", "negative PSD")
    _, tolerance, _ = _scales(q, delta_f)
    require(candidate.size == int(FS / (2 * delta_f)) + 1, "BINS", "bin count and spacing disagree")
    if q == 0:
        require(bool((candidate == 0).all() and (reference == 0).all()), "ZERO_POWER", "nonzero zero-power PSD")
    residual = np.abs(candidate - reference)
    require(bool(np.isfinite(residual).all()), "NONFINITE", "PSD residual overflow")
    require(bool((residual <= tolerance).all()), "TOLERANCE", "all-bin PSD comparison failed")
    return {"absolute_residual": residual, "threshold": tolerance}


def _parseval(psd, q, delta_f):
    _, _, tolerance = _scales(q, delta_f)
    integral = _finite(delta_f * _sum(psd), "spectral integral")
    residual = abs(integral - q)
    require(residual <= tolerance, "TOLERANCE", "Parseval comparison failed")
    if q == 0:
        require(bool((psd == 0).all()), "ZERO_POWER", "zero-power PSD is nonzero")
    return {"integral": integral, "power": q, "absolute_residual": residual, "threshold": tolerance}


def aggregate_periodograms(psds):
    _array(psds, 2)
    require(psds.shape[-1] in (5, 9, 8193), "BINS", "unadmitted periodogram bin count")
    require(bool((psds >= 0).all()), "NEGATIVE_PSD", "negative input periodogram")
    with np.errstate(all="raise"):
        try:
            mean = np.mean(psds, axis=0, dtype=np.float64)
            asd = np.sqrt(mean)
        except FloatingPointError as exc:
            raise SpectraError("NONFINITE", "aggregation arithmetic failed") from exc
    _array(mean, 1)
    _array(asd, 1)
    return mean, asd


def _sqrt_checks(psd, asd, reference_psd, q, delta_f):
    for values in (psd, asd, reference_psd):
        _array(values, 1)
    require(psd.shape == asd.shape == reference_psd.shape, "BINS", "sqrt array shapes differ")
    require(bool((psd >= 0).all() and (asd >= 0).all() and (reference_psd >= 0).all()), "NEGATIVE_PSD", "negative PSD/ASD")
    expected = np.array([math.sqrt(float(p)) for p in psd], dtype=np.float64)
    direct_error = np.abs(asd - expected)
    direct_limit = 8 * EPS * expected
    require(bool((direct_error <= direct_limit).all()), "TOLERANCE", "pointwise sqrt check")
    require(bool((asd[psd == 0] == 0).all()), "ZERO_POWER", "nonzero ASD at zero PSD")
    reference_asd = np.array([math.sqrt(float(p)) for p in reference_psd], dtype=np.float64)
    s, tolerance, _ = _scales(q, delta_f)
    cross_limit = math.sqrt(tolerance) + 8 * EPS * math.sqrt(s)
    cross_error = np.abs(asd - reference_asd)
    require(bool((cross_error <= cross_limit).all()), "TOLERANCE", "ASD conventional comparison")
    return reference_asd, {"pointwise_residual": direct_error, "pointwise_threshold": direct_limit,
                           "reference_residual": cross_error, "reference_threshold": cross_limit}


def segment_spectrum(x):
    """M=16384 in production; lengths 8/16 exist solely for fixed DFT fixtures."""
    _array(x, 1, (8, 16, M))
    size = x.size
    delta_f = FS / size
    try:
        with np.errstate(all="raise"):
            window = np.frombuffer(_window_bytes(size), dtype="<f8")
            mean = float(np.mean(x, dtype=np.float64))
            demeaned = x - mean
            windowed = window * demeaned
            w2 = float(np.sum(window * window, dtype=np.float64))
            transform = np.fft.rfft(windowed, n=size, norm="backward")
            psd = (transform.real * transform.real + transform.imag * transform.imag) / (FS * w2)
            psd[1:-1] *= 2
    except FloatingPointError as exc:
        raise SpectraError("NONFINITE", "segment arithmetic underflow/overflow/invalid") from exc
    _array(psd, 1)
    _array(demeaned, 1)
    _array(windowed, 1)
    require(bool(((window == 0) | (demeaned == 0) | (windowed != 0)).all()), "UNDERFLOW", "window product vanished")
    require(w2 > 0, "ZERO_POWER", "window energy is zero")
    wsum_ref = _sum(window)
    w2_ref = _sum(float(w) * float(w) for w in window)
    mean_ref = _sum(x) / size
    mean_error = abs(mean - mean_ref)
    input_peak = float(np.max(np.abs(x)))
    mean_limit = TAU * input_peak
    require(mean_error <= mean_limit, "TOLERANCE", "segment mean comparison")
    formula = np.array([(1 - math.cos(2 * math.pi * j / size)) / 2 for j in range(size)], dtype=np.float64)
    window_error = np.abs(window - formula)
    require(bool((window_error <= 16 * EPS).all()), "TOLERANCE", "periodic window formula")
    require(abs(wsum_ref - size / 2) <= TAU * (size / 2), "TOLERANCE", "window sum")
    require(abs(w2_ref - 3 * size / 8) <= TAU * (3 * size / 8), "TOLERANCE", "window energy")
    q = _power(windowed, w2_ref)
    if q == 0:
        require(bool((windowed == 0).all() and (psd == 0).all()), "ZERO_POWER", "nonzero zero-power segment")
    freq, reference = signal.welch(x, fs=FS, window=window, nperseg=size, noverlap=0,
                                   nfft=size, detrend="constant", return_onesided=True,
                                   scaling="density", axis=-1, average="mean")
    frequency = np.arange(size // 2 + 1, dtype=np.float64) * delta_f
    require(np.array_equal(freq, frequency), "BINS", "reference frequency grid")
    checks = {"mean": {"actual": mean, "reference": mean_ref, "input_peak": input_peak,
                       "absolute_residual": mean_error, "threshold": mean_limit},
              "parseval": _parseval(psd, q, delta_f), "reference_psd": check_psd(psd, reference, q, delta_f),
              "window": {"sum": float(np.sum(window, dtype=np.float64)), "w2": w2,
                         "sum_reference": wsum_ref, "w2_reference": w2_ref,
                         "sum_ideal_residual": abs(wsum_ref - size / 2), "sum_threshold": TAU * (size / 2),
                         "w2_ideal_residual": abs(w2_ref - 3 * size / 8), "w2_threshold": TAU * (3 * size / 8),
                         "formula_residual": window_error, "formula_threshold": 16 * EPS}}
    return {"window": window, "mean": mean, "demeaned": demeaned, "windowed": windowed,
            "fft_real": transform.real.copy(), "fft_imag": transform.imag.copy(), "psd": psd,
            "q": q, "w2": w2, "frequency_hz": frequency, "reference_psd": reference, "checks": checks}


def side_spectra(samples, side):
    _array(samples, 1, (N,))
    require(side in ("left", "right"), "SCHEMA", "unknown fixed side")
    indices = fixed_indices()[side]
    segments = [{"start": start, "end": start + M, "spectrum": segment_spectrum(samples[start:start + M])}
                for start in indices["starts"]]
    psds = np.stack([s["spectrum"]["psd"] for s in segments])
    mean, asd = aggregate_periodograms(psds)
    q = _sum(s["spectrum"]["q"] for s in segments) / indices["count"]
    first = segments[0]["spectrum"]
    a, b = indices["interval"]
    freq, reference = signal.welch(samples[a:b], fs=FS, window=first["window"], nperseg=M,
                                   noverlap=STRIDE, nfft=M, detrend="constant", return_onesided=True,
                                   scaling="density", axis=-1, average="mean")
    require(np.array_equal(freq, first["frequency_hz"]), "BINS", "side reference frequency grid")
    reference_asd, sqrt_checks = _sqrt_checks(mean, asd, reference, q, 0.25)
    return {"segments": segments, "mean_psd": mean, "asd": asd, "q": q,
            "reference_psd": reference, "reference_asd": reference_asd,
            "checks": {"parseval": _parseval(mean, q, 0.25),
                       "reference_psd": check_psd(mean, reference, q, 0.25), "sqrt": sqrt_checks}}


def _same(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    return a == b


def admit_metadata(actual, expected):
    """Pure comparison; the caller must authenticate expected separately."""
    require(type(actual) is dict and type(expected) is dict, "METADATA", "report objects required")
    require(type(actual.get("detectors")) is list and type(expected.get("detectors")) is list,
            "METADATA", "detector records missing")
    require(len(actual["detectors"]) == len(expected["detectors"]), "METADATA", "detector count differs")
    for got, wanted in zip(actual["detectors"], expected["detectors"]):
        require(type(got) is dict and type(wanted) is dict, "METADATA", "detector record malformed")
        for key in ("filename", "identity"):
            require(key in got and key in wanted and _same(got[key], wanted[key]), "INPUT_PIN", f"{key} differs")
        for key in ("data_quality", "hardware_injection_flags"):
            require(key in got and key in wanted and _same(got[key], wanted[key]), "FLAGS", f"{key} differs")
    require(_same(actual, expected), "METADATA", "complete metadata differs")
    return True


def array_bytes(values):
    _array(values, 1)
    return np.asarray(values, dtype="<f8", order="C").tobytes(order="C")


def array_record(values):
    payload = array_bytes(values)
    return {"dtype": "<f8", "shape": list(values.shape), "values_hex": [float(v).hex() for v in values],
            "sha256": hashlib.sha256(payload).hexdigest()}


def _export(value):
    if isinstance(value, np.ndarray):
        return array_record(value)
    if isinstance(value, (float, np.floating)):
        return _finite(value, "export scalar").hex()
    if isinstance(value, dict):
        return {key: _export(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_export(item) for item in value]
    require(type(value) in (str, int, bool) or value is None, "SCHEMA", "unhandled export type")
    return value


def _pin_record(value, label):
    require(type(value) is dict and set(value) == {"bytes", "sha256"}, "SCHEMA", f"{label} pin keys")
    require(type(value["bytes"]) is int and value["bytes"] > 0, "SCHEMA", f"{label} byte count")
    digest = value["sha256"]
    require(type(digest) is str and len(digest) == 64 and all(c in "0123456789abcdef" for c in digest),
            "SCHEMA", f"{label} SHA-256")
    return copy.deepcopy(value)


def build_result(payloads, inspector, expected_report, qualification_pin, window_pin, artifact_dir):
    """Observed worker entry, never called by import or automatic CLI.

    The coordinator must first admit the exact source/runtime, the inspector
    source, accepted fabricated qualification report and authorization manifest.
    payloads contains two already custody-bound complete byte snapshots. Check
    both here before either HDF5 parse; use these same objects for both reads.
    The return is (scientific_result, external_artifact_inventory).
    """
    require(type(payloads) is dict and set(payloads) == {"H1", "L1"}, "INPUT_PIN", "fixed pair required")
    require(pin(canonical(expected_report)) == REPORT_PIN, "INPUT_PIN", "published RI-37 report differs")
    qualification_pin = _pin_record(qualification_pin, "accepted qualification")
    # Materialize/compare the window before either observed HDF5 parser. The
    # caller must bind window_pin to its already accepted fabricated report.
    require(prepare_windows()[str(M)] == _pin_record(window_pin, "qualified window"),
            "IDENTITY", "production window differs from the pre-observed freeze")
    directory = Path(artifact_dir)
    require(directory.is_absolute() and directory.parent == directory.parent.resolve(), "PATH", "canonical absolute artifact parent required")
    require(not directory.exists() and not directory.is_symlink(), "PATH", "exclusive artifact destination required")
    for entry in INPUTS:
        body = payloads[entry["detector"]]
        require(type(body) is bytes and pin(body) == {k: entry[k] for k in ("bytes", "sha256")},
                "INPUT_PIN", "complete input byte identity differs")
        require(hashlib.md5(body, usedforsecurity=False).hexdigest() == entry["md5"], "INPUT_PIN", "publisher MD5 differs")
    expected_files = {item["detector"]: item for item in inspector.FILES}
    inspected = copy.deepcopy(expected_report)
    inspected["detectors"] = [inspector._inspect(payloads[e["detector"]], expected_files[e["detector"]]) for e in INPUTS]
    admit_metadata(inspected, expected_report)
    require(pin(canonical(inspected)) == REPORT_PIN, "METADATA", "RI-37 replay identity differs")
    arrays = {}
    for entry in INPUTS:
        with h5py.File(io.BytesIO(payloads[entry["detector"]]), "r") as handle:
            arrays[entry["detector"]] = handle["/strain/Strain"][()]
        _array(arrays[entry["detector"]], 1, (N,))
    directory.mkdir(mode=0o700)
    inventory = []

    def save(name, values):
        body = array_bytes(values)
        target = directory / (name + ".f64le")
        with target.open("xb") as stream:
            stream.write(body)
        inventory.append({"name": name, "path": str(target), **pin(body), "dtype": "<f8", "shape": list(values.shape)})
        return hashlib.sha256(body).hexdigest()

    return _assemble_result(arrays, inspected, qualification_pin, save), inventory


def fabricated_result_fixture(arrays, expected_report):
    """Complete schema fixture only; never an observed scientific result.

    No HDF5 or filesystem access occurs. Already public pinned metadata supplies
    the nested flag schema, while the arrays and qualification pin are expressly
    fabricated. The surrounding context marker must remain in qualification.
    """
    require(type(arrays) is dict and set(arrays) == {"H1", "L1"}, "SCHEMA", "fabricated pair arrays required")
    require(pin(canonical(expected_report)) == REPORT_PIN, "INPUT_PIN", "pinned metadata fixture differs")
    for values in arrays.values():
        _array(values, 1, (N,))

    def hash_only(name, values):
        return hashlib.sha256(array_bytes(values)).hexdigest()

    fabricated_pin = pin(b"fabricated schema fixture; no observed execution\n")
    result = _assemble_result(arrays, copy.deepcopy(expected_report), fabricated_pin, hash_only)
    return {"context": "fabricated_schema_fixture_not_observed", "result": result}


def _assemble_result(arrays, inspected, qualification_pin, save):
    detector_results, numerical_checks, input_records = [], [], []
    shared = None
    for entry, metadata in zip(INPUTS, inspected["detectors"]):
        detector = entry["detector"]
        input_records.append({**entry, "url": "https://gwosc.org/GW150914data/" + entry["filename"],
                              "ri37_detector": metadata, "inspector_report_pin": REPORT_PIN.copy(),
                              "recovery_handoff_pin": RECOVERY_PIN.copy()})
        sides, side_checks = [], []
        for side in ("left", "right"):
            output = side_spectra(arrays[detector], side)
            segments, segment_checks = [], []
            for row in output["segments"]:
                start, end, spectrum = row["start"], row["end"], row["spectrum"]
                if shared is None:
                    shared = spectrum
                    save("window", spectrum["window"])
                    save("frequency_hz", spectrum["frequency_hz"])
                else:
                    require(array_bytes(shared["window"]) == array_bytes(spectrum["window"]), "IDENTITY", "window changed")
                name = f"{detector}-{side}-{start}"
                flag_rows = list(range(start // FS, end // FS))
                raw = arrays[detector][start:end]
                record = {"start": start, "end": end, "gps_offset_numerators": [start, end], "gps_offset_denominator": FS,
                          "flag_rows": flag_rows, "dq_masks": [metadata["data_quality"]["raw_bitfields"][i] for i in flag_rows],
                          "injection_masks": [metadata["hardware_injection_flags"]["raw_bitfields"][i] for i in flag_rows],
                          "mean": spectrum["mean"], "q": spectrum["q"],
                          "raw_sha256": hashlib.sha256(array_bytes(raw)).hexdigest(),
                          "demeaned_sha256": save(name + "-demeaned", spectrum["demeaned"]),
                          "windowed_sha256": save(name + "-windowed", spectrum["windowed"]), "psd": spectrum["psd"]}
                save(name + "-psd", spectrum["psd"])
                save(name + "-reference_psd", spectrum["reference_psd"])
                segments.append(record)
                segment_checks.append({"start": start, "mean": spectrum["checks"]["mean"],
                                       "parseval": spectrum["checks"]["parseval"], "reference_psd": spectrum["reference_psd"],
                                       "comparison": spectrum["checks"]["reference_psd"]})
            for key in ("mean_psd", "asd", "reference_psd", "reference_asd"):
                save(f"{detector}-{side}-{key}", output[key])
            sides.append({"side": side, **fixed_indices()[side], "segments": segments,
                          "mean_psd": output["mean_psd"], "asd": output["asd"], "q": output["q"],
                          "psd_unit": "nominal_strain_squared_per_Hz", "asd_unit": "nominal_strain_per_sqrt_Hz"})
            side_checks.append({"side": side, "segments": segment_checks, "reference_psd": output["reference_psd"],
                                "reference_asd": output["reference_asd"], "parseval": output["checks"]["parseval"],
                                "comparison": output["checks"]["reference_psd"], "sqrt": output["checks"]["sqrt"]})
        detector_results.append({"detector": detector, "sides": sides})
        numerical_checks.append({"detector": detector, "sides": side_checks})
    result = {"schema": "ri78-off-event-spectra-v1", "method": method_contract(), "inputs": input_records,
              "frequency_hz": array_record(shared["frequency_hz"]),
              "window": {"values": array_record(shared["window"]), "checks": _export(shared["checks"]["window"])},
              "detectors": _export(detector_results),
              "checks": {"identity": {"inspector_report_pin": REPORT_PIN.copy(), "recovery_handoff_pin": RECOVERY_PIN.copy(),
                                      "qualification_report_pin": qualification_pin,
                                      "fixed_dimensions_indices_and_flags": True},
                         "detectors": _export(numerical_checks)}, "limitations": LIMITATIONS.copy()}
    def retain_array_records(value, trail):
        if type(value) is dict and set(value) == {"dtype", "shape", "values_hex", "sha256"}:
            values = np.array([float.fromhex(item) for item in value["values_hex"]], dtype=np.float64)
            require(save("result-" + "-".join(trail), values) == value["sha256"], "IDENTITY", "exported array bytes differ")
        elif type(value) is dict:
            for key in sorted(value):
                retain_array_records(value[key], trail + [key])
        elif type(value) is list:
            for index, item in enumerate(value):
                retain_array_records(item, trail + [str(index)])

    retain_array_records(result, [])
    # Validator is supplied by the source-pinned caller: no ambient sibling import
    # or hidden path-based code loading is performed here. Validate before writing
    # RESULT.json and the final custody manifest in that caller.
    return result
