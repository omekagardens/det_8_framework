"""RI-80 qualification of the fixed RI-78 statistic, on fabricated inputs only.

SOURCE-ONLY UNTIL COORDINATOR FREEZE. The external launcher must bind this
source, its complete imported closure, the admitted runtime and launch limits
before execution. This module does not authorize itself or open strain files.
It writes deterministic evidence to stdout; the launcher owns exclusive receipt
paths. An independent scalar DFT and analytic Fourier identities are the oracles;
SciPy Welch is a conventional API comparison, not an independent FFT engine.
"""

import copy
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import stat
import struct
import sys


FS = 4096
M = 16384
N = 131072
EPS = 2.0 ** -52
TAU = 2.0 ** -40
AMPLITUDES = (1.0, 2.0 ** -70)
FIXED_INDICES = {
    "left": {"interval": [0, 65536],
             "starts": [0, 8192, 16384, 24576, 32768, 40960, 49152],
             "count": 7, "used_interval": [0, 65536], "unused_intervals": []},
    "right": {"interval": [69632, 131072],
              "starts": [69632, 77824, 86016, 94208, 102400, 110592],
              "count": 6, "used_interval": [69632, 126976],
              "unused_intervals": [[126976, 131072]]},
}
FIXED_PINS = {
    "design": {"path": "gwosc_off_event_spectra_v1/DESIGN.md", "bytes": 24390,
               "sha256": "3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce"},
    "runtime_source": {"path": "gwosc_context_operator_v2/check.py", "bytes": 38088,
                       "sha256": "a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02"},
    "runtime_report": {"path": "gwosc_context_operator_v2/QUALIFICATION_REPORT.json",
                       "bytes": 9413345,
                       "sha256": "1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f"},
    "input_metadata_report": {"path": "gwosc_input_qualification_v1/INPUT_REPORT.json",
                              "bytes": 31096,
                              "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80"},
}


class QualificationError(ValueError):
    """An explicit failure, including in optimized Python."""


def require(condition, message):
    if not condition:
        raise QualificationError(message)


def identity(payload):
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def snapshot(path):
    require(stat.S_ISREG(path.lstat().st_mode), "source is not a regular file: " + str(path))
    return path.read_bytes()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=True).encode("ascii")


def canonical_chunks(value):
    """Exactly the validator's indent-2 encoding, without joining its chunks."""
    encoder = json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False,
                               ensure_ascii=True)
    for chunk in encoder.iterencode(value):
        yield chunk.encode("utf-8")
    yield b"\n"


def canonical_identity(value):
    digest, size = hashlib.sha256(), 0
    for chunk in canonical_chunks(value):
        digest.update(chunk)
        size += len(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def canonical_payload(value):
    with io.BytesIO() as stream:
        for chunk in canonical_chunks(value):
            stream.write(chunk)
        return stream.getvalue()


class FrozenHexValues:
    """Immutable evidence bits; materialize one hex list only during encoding.

    Every value is still retained. Unpacking the already finite little-endian
    binary64 bytes preserves the exact float.hex spelling, including signed zero.
    This is not a schema object sent to the result validator: it is an internal
    representation of qualification evidence until the final JSON writer.
    """
    def __init__(self, body):
        require(type(body) is bytes and len(body) % 8 == 0, "invalid evidence bytes")
        self.body = body

    def __len__(self):
        return len(self.body) // 8

    def __iter__(self):
        return (value.hex() for (value,) in struct.iter_unpack("<d", self.body))

    def __eq__(self, other):
        if isinstance(other, FrozenHexValues):
            return self.body == other.body
        if type(other) is list:
            return len(self) == len(other) and all(a == b for a, b in zip(self, other))
        return NotImplemented


def evidence_json_default(value):
    if isinstance(value, FrozenHexValues):
        return list(value)
    raise TypeError("unsupported qualification JSON value: " + type(value).__name__)


def strict_json(payload):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result

    def invalid(value):
        raise QualificationError("nonfinite JSON value: " + value)

    return json.loads(payload, object_pairs_hook=pairs, parse_constant=invalid)


def load_source(name, path, payload):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "module specification failed")
    module = importlib.util.module_from_spec(spec)
    require(name not in sys.modules, "unexpected preloaded module: " + name)
    sys.modules[name] = module
    exec(compile(payload, str(path), "exec"), module.__dict__)
    return module


def admission():
    """Repeat fixed design/runtime checks; the root launcher owns source admission."""
    base = Path(__file__).resolve().parent
    experiments = base.parent
    paths = {name: experiments / pin["path"] for name, pin in FIXED_PINS.items()}
    paths.update({"qualify": base / "qualify.py", "spectra": base / "spectra.py",
                  "validate_result": base / "validate_result.py"})
    # Snapshot all Python bodies before executing any local scientific source.
    bodies = {name: snapshot(path) for name, path in paths.items()}
    for name, pin in FIXED_PINS.items():
        require(identity(bodies[name]) == {key: pin[key] for key in ("bytes", "sha256")},
                "fixed dependency identity changed: " + name)
    runtime_source = load_source("ri80_admitted_ri60_runtime", paths["runtime_source"],
                                 bodies["runtime_source"])
    runtime = runtime_source.runtime()
    expected_runtime = strict_json(bodies["runtime_report"])["runtime"]
    require(canonical(runtime) == canonical(expected_runtime), "full RI-60 runtime mismatch")
    primary = load_source("spectra", paths["spectra"], bodies["spectra"])
    validator = load_source("validate_result", paths["validate_result"], bodies["validate_result"])
    return primary, validator, runtime, paths, bodies


def array_record(values, np):
    values = np.asarray(values, dtype=np.float64)
    require(bool(np.isfinite(values).all()), "nonfinite evidence array")
    raw = np.ascontiguousarray(values, dtype="<f8").tobytes(order="C")
    return {"dtype": "<f8", "shape": list(values.shape),
            "values_hex": FrozenHexValues(raw), **identity(raw)}


def array_pin(values, np):
    values = np.asarray(values, dtype=np.float64)
    require(bool(np.isfinite(values).all()), "nonfinite evidence array")
    raw = np.ascontiguousarray(values, dtype="<f8").tobytes(order="C")
    return {"dtype": "<f8", "shape": list(values.shape), **identity(raw)}


def hex_scalar(value):
    value = float(value)
    require(math.isfinite(value), "nonfinite evidence scalar")
    return value.hex()


def bound(label, difference, limit):
    difference, limit = float(difference), float(limit)
    require(math.isfinite(difference) and difference >= 0.0, label + ": invalid discrepancy")
    require(math.isfinite(limit) and limit >= 0.0, label + ": invalid budget")
    require(difference <= limit, label + ": discrepancy exceeds frozen budget")
    return {"passed": True, "absolute_error_hex": difference.hex(), "limit_hex": limit.hex()}


def finite_vector(values, n, np, label):
    require(type(values) is np.ndarray and values.dtype == np.dtype("float64") and
            values.shape == (n,) and bool(np.isfinite(values).all()),
            label + ": expected finite float64 vector of frozen length")


def compare_psd(label, candidate, reference, q, delta_f, np):
    require(candidate.shape == reference.shape, label + ": bin mismatch")
    require(bool(np.isfinite(candidate).all()) and bool(np.isfinite(reference).all()) and
            bool((candidate >= 0.0).all()) and bool((reference >= 0.0).all()),
            label + ": invalid PSD")
    require(math.isfinite(q) and q >= 0.0, label + ": invalid independent Q")
    scale = q / delta_f
    limit = TAU * scale
    require(q == 0.0 or (math.isfinite(scale) and scale > 0.0 and limit > 0.0),
            label + ": underflow or overflow in frozen scale")
    errors = np.abs(candidate - reference)
    maximum = max(float(x) for x in errors)
    checked = bound(label, maximum, limit)
    if q == 0.0:
        require(bool((candidate == 0.0).all()) and bool((reference == 0.0).all()),
                label + ": zero power must have exactly zero PSD")
    return {**checked, "q_hex": q.hex(), "delta_f_hex": float(delta_f).hex(),
            "candidate": array_record(candidate, np), "reference": array_record(reference, np),
            "absolute_errors": array_record(errors, np)}


def check_sqrt(label, psd, asd, np):
    finite_vector(asd, len(psd), np, label)
    require(bool((asd >= 0.0).all()), label + ": negative ASD")
    errors, limits = [], []
    for p, a in zip(psd, asd):
        expected = math.sqrt(float(p))
        error = abs(float(a) - expected)
        limit = 8.0 * EPS * expected
        bound(label, error, limit)
        errors.append(error)
        limits.append(limit)
    return {"passed": True, "asd": array_record(asd, np),
            "absolute_errors": array_record(errors, np), "limits": array_record(limits, np)}


def direct_dft(values):
    """Independent small scalar DFT: no primary helper, FFT, or Welch call."""
    n = len(values)
    require(n in (8, 16), "scalar DFT only admits frozen small fixtures")
    x = [float(value) for value in values]
    mu = math.fsum(x) / n
    window = [(1.0 - math.cos(2.0 * math.pi * j / n)) / 2.0 for j in range(n)]
    v = [window[j] * (x[j] - mu) for j in range(n)]
    energy = math.fsum(w * w for w in window)
    real = [math.fsum(v[j] * math.cos(2.0 * math.pi * j * k / n) for j in range(n))
            for k in range(n // 2 + 1)]
    imag = [-math.fsum(v[j] * math.sin(2.0 * math.pi * j * k / n) for j in range(n))
            for k in range(n // 2 + 1)]
    psd = [(real[k] * real[k] + imag[k] * imag[k]) / (FS * energy) *
           (1.0 if k in (0, n // 2) else 2.0) for k in range(n // 2 + 1)]
    return {"mean": mu, "window": window, "windowed": v, "real": real, "imag": imag,
            "psd": psd, "q": math.fsum(value * value for value in v) / energy}


def analytic_fixture(kind, amplitude, np):
    """Exact Fourier-series powers; never call the primary normalization helper."""
    a = amplitude
    if kind == "zero":
        x = np.zeros(M, dtype=np.float64)
    elif kind in ("constant_positive", "constant_negative"):
        x = np.full(M, a if kind == "constant_positive" else -a, dtype=np.float64)
    elif kind == "quarter_cosine":
        x = np.tile(np.array([a, 0.0, -a, 0.0], dtype=np.float64), M // 4)
    elif kind == "quarter_sine":
        x = np.tile(np.array([0.0, a, 0.0, -a], dtype=np.float64), M // 4)
    elif kind == "nyquist_cosine":
        x = np.tile(np.array([a, -a], dtype=np.float64), M // 2)
    elif kind == "lowest_cosine":
        x = np.array([a * math.cos(2.0 * math.pi * j / M) for j in range(M)], dtype=np.float64)
    else:
        raise QualificationError("unknown analytic fixture")
    expected = np.zeros(M // 2 + 1, dtype=np.float64)
    scale = a * a * M / FS
    q = 0.0
    if kind in ("quarter_cosine", "quarter_sine"):
        expected[M // 4 - 1:M // 4 + 2] = [scale / 12.0, scale / 3.0, scale / 12.0]
        q = a * a / 2.0
    elif kind == "nyquist_cosine":
        expected[-2:] = [scale / 3.0, 2.0 * scale / 3.0]
        q = a * a
    elif kind == "lowest_cosine":
        expected[:3] = [scale / 6.0, scale / 3.0, scale / 12.0]
        q = 7.0 * a * a / 12.0
    return x, expected, q


def segment_checks(label, x, output, signal, np):
    n = len(x)
    bins = n // 2 + 1
    for name in ("window", "demeaned", "windowed"):
        finite_vector(output[name], n, np, label + "/" + name)
    for name in ("psd", "fft_real", "fft_imag", "frequency_hz"):
        finite_vector(output[name], bins, np, label + "/" + name)
    w, v, p = output["window"], output["windowed"], output["psd"]
    require(bool((p >= 0.0).all()), label + ": negative PSD")
    require(all(float(f) == k * FS / n for k, f in enumerate(output["frequency_hz"])),
            label + ": wrong frequencies")
    mu = math.fsum(float(t) for t in x) / n
    mean_check = bound(label + "/mean", abs(float(output["mean"]) - mu),
                       TAU * max(abs(float(t)) for t in x))
    require(bool(np.array_equal(output["demeaned"], x - output["mean"])),
            label + ": wrong demeaning order or values")
    require(bool(np.array_equal(v, w * output["demeaned"])), label + ": wrong windowed values")
    ideal_window = np.array([(1.0 - math.cos(2.0 * math.pi * j / n)) / 2.0
                             for j in range(n)], dtype=np.float64)
    formula_check = bound(label + "/window_formula", max(abs(float(a) - float(b))
                          for a, b in zip(w, ideal_window)), 16.0 * EPS)
    wsum = math.fsum(float(t) for t in w)
    w2 = math.fsum(float(t) * float(t) for t in w)
    q = math.fsum(float(t) * float(t) for t in v) / w2
    window_checks = {
        "sum": bound(label + "/window_sum", abs(wsum - n / 2.0), TAU * n / 2.0),
        "energy": bound(label + "/window_energy", abs(w2 - 3.0 * n / 8.0), TAU * 3.0 * n / 8.0),
        "primary_energy": bound(label + "/primary_energy", abs(float(output["w2"]) - w2), TAU * w2),
        "formula": formula_check,
    }
    if q == 0.0:
        require(bool((v == 0.0).all()) and bool((p == 0.0).all()), label + ": nonzero zero-power output")
    else:
        require(math.isfinite(q) and q > 0.0 and TAU * q > 0.0,
                label + ": invalid or underflowed independent power")
    df = FS / n
    parseval = bound(label + "/parseval", abs(df * math.fsum(float(t) for t in p) - q), TAU * q)
    q_check = bound(label + "/primary_q", abs(float(output["q"]) - q), TAU * q)
    freq, ref = signal.welch(x, fs=FS, window=w, nperseg=n, noverlap=0,
                             nfft=n, detrend="constant", return_onesided=True,
                             scaling="density", axis=-1, average="mean")
    require(bool(np.array_equal(freq, output["frequency_hz"])), label + ": Welch frequencies differ")
    return {"input": array_pin(x, np), "window": array_pin(w, np),
            "demeaned": array_pin(output["demeaned"], np), "windowed": array_pin(v, np),
            "mean_hex": hex_scalar(output["mean"]), "q_hex": q.hex(), "w2_hex": w2.hex(),
            "mean_check": mean_check, "window_checks": window_checks,
            "parseval": parseval, "primary_q": q_check,
            "welch": compare_psd(label + "/welch", p, ref, q, df, np)}, q


def refusal(label, function, expected_code, error_type):
    try:
        function()
    except error_type as error:
        require(error.code == expected_code,
                label + ": wrong refusal reason " + str(error.code) + ", expected " + expected_code)
        return {"name": label, "passed": True, "expected_code": expected_code,
                "actual_code": error.code, "message": str(error)}
    except Exception as error:
        raise QualificationError(label + ": incidental exception " + type(error).__name__) from error
    raise QualificationError(label + ": unexpectedly accepted")


def refusal_checks(primary, np):
    result = []
    cases = [
        ("dimension", lambda: primary.segment_spectrum(np.zeros((2, 8), dtype=np.float64)), "DIMENSION"),
        ("dtype", lambda: primary.segment_spectrum(np.zeros(8, dtype=np.float32)), "DTYPE"),
        ("empty", lambda: primary.segment_spectrum(np.zeros(0, dtype=np.float64)), "LENGTH"),
        ("short", lambda: primary.segment_spectrum(np.zeros(7, dtype=np.float64)), "LENGTH"),
        ("nonfinite", lambda: primary.segment_spectrum(np.array([float("nan")] + [0.0] * 7)), "NONFINITE"),
        ("infinity", lambda: primary.segment_spectrum(np.array([float("inf")] + [0.0] * 7)), "NONFINITE"),
        ("negative_psd", lambda: primary.aggregate_periodograms(-np.ones((2, 5), dtype=np.float64)), "NEGATIVE_PSD"),
        ("aggregate_wrong_bins", lambda: primary.aggregate_periodograms(np.zeros((2, 4), dtype=np.float64)), "BINS"),
        ("aggregate_empty", lambda: primary.aggregate_periodograms(np.zeros((0, 5), dtype=np.float64)), "LENGTH"),
        ("comparison_wrong_bins", lambda: primary.check_psd(np.zeros(5), np.zeros(9), 1.0, FS / 8), "BINS"),
        ("comparison_tolerance", lambda: primary.check_psd(np.ones(5), np.zeros(5), 1.0, FS / 8), "TOLERANCE"),
        ("zero_power_nonzero", lambda: primary.check_psd(np.ones(5), np.zeros(5), 0.0, FS / 8), "ZERO_POWER"),
        ("underflowed_budget", lambda: primary.check_psd(np.zeros(5), np.zeros(5),
             float.fromhex("0x0.0000000000001p-1022"), FS / 8), "UNDERFLOW"),
        ("side_short", lambda: primary.side_spectra(np.zeros(N - 1, dtype=np.float64), "left"), "LENGTH"),
    ]
    for name, function, code in cases:
        result.append(refusal(name, function, code, primary.SpectraError))
    # A pure fabricated metadata report; it is never used to admit actual bytes.
    expected = {"schema_version": "ri80-fabricated-metadata-v1", "detectors": [
        {"filename": "fabricated-H1", "identity": {"bytes": 1, "sha256": "a" * 64},
         "data_quality": {"values": [127] * 32},
         "hardware_injection_flags": {"values": [31] * 32}, "strain": {"shape": [N]}},
        {"filename": "fabricated-L1", "identity": {"bytes": 1, "sha256": "b" * 64},
         "data_quality": {"values": [127] * 32},
         "hardware_injection_flags": {"values": [23] * 32}, "strain": {"shape": [N]}}]}
    primary.admit_metadata(copy.deepcopy(expected), expected)
    mutations = []
    wrong = copy.deepcopy(expected)
    wrong["detectors"][0]["identity"]["sha256"] = "0" * 64
    mutations.append(("wrong_input_pin", wrong, "INPUT_PIN"))
    wrong = copy.deepcopy(expected)
    del wrong["detectors"][1]["hardware_injection_flags"]
    mutations.append(("missing_flags", wrong, "FLAGS"))
    wrong = copy.deepcopy(expected)
    wrong["detectors"][1]["hardware_injection_flags"]["values"][0] = 31
    mutations.append(("changed_l1_flags", wrong, "FLAGS"))
    wrong = copy.deepcopy(expected)
    wrong["detectors"][0]["strain"]["shape"] = [N - 1]
    mutations.append(("changed_metadata", wrong, "METADATA"))
    for name, wrong, code in mutations:
        result.append(refusal(name, lambda wrong=wrong: primary.admit_metadata(wrong, expected), code, primary.SpectraError))
    return result


def schema_checks(primary, validator, metadata_report, samples, side_evidence, windows, np):
    """A marked fabricated complete shape, never an observed RESULT payload."""
    samples_pin = array_pin(samples, np)
    wrapper = primary.fabricated_result_fixture({"H1": samples, "L1": samples.copy()}, metadata_report)
    require(set(wrapper) == {"context", "result"} and
            wrapper["context"] == "fabricated_schema_fixture_not_observed", "fabricated context marker missing")
    result = wrapper["result"]
    require(array_pin(samples, np) == samples_pin, "schema assembler mutated the fabricated input")
    # Bind the shared serializer to numerical arrays already independently
    # checked above, rather than accepting only internal schema consistency.
    require(result["window"]["values"]["values_hex"] == windows[M]["values_hex"],
            "schema assembler changed the reviewed production window")
    for detector in result["detectors"]:
        for side in detector["sides"]:
            expected = side_evidence[side["side"]]
            require(side["mean_psd"]["values_hex"] == expected["independent_mean"]["candidate"]["values_hex"] and
                    side["asd"]["values_hex"] == expected["sqrt"]["asd"]["values_hex"] and
                    side["q"] == expected["independent_mean"]["q_hex"], "schema assembler changed side values")
            require(len(side["segments"]) == len(expected["segments"]), "schema assembler changed segment count")
            for segment, prior in zip(side["segments"], expected["segments"]):
                checked = prior["checks"]
                require(segment["start"] == prior["start"] and segment["end"] == prior["end"] and
                        segment["psd"]["values_hex"] == checked["welch"]["candidate"]["values_hex"] and
                        segment["mean"] == checked["mean_hex"] and segment["q"] == checked["q_hex"] and
                        segment["raw_sha256"] == checked["input"]["sha256"] and
                        segment["demeaned_sha256"] == checked["demeaned"]["sha256"] and
                        segment["windowed_sha256"] == checked["windowed"]["sha256"],
                        "schema assembler changed segment values or array custody")
    require(validator.validate_result(result) is True, "positive nested schema fixture refused")
    fixture_identity = canonical_identity(result)

    def rehash(record):
        raw = b"".join(struct.pack("<d", float.fromhex(value)) for value in record["values_hex"])
        record["sha256"] = hashlib.sha256(raw).hexdigest()

    def set_bin(record, index, value):
        record["values_hex"][index] = float(value).hex()
        rehash(record)

    missing = object()

    def replace(path, value):
        def change(target):
            for key in path[:-1]:
                target = target[key]
            previous = target.get(path[-1], missing) if type(target) is dict else target[path[-1]]
            target[path[-1]] = value
            def undo():
                if previous is missing:
                    del target[path[-1]]
                else:
                    target[path[-1]] = previous
            return undo
        return change

    def bin_change(path, index, value):
        def change(target):
            root = target
            for key in path:
                target = target[key]
            # Copy only the changed array record/list. Other fixture subtrees
            # remain untouched; restore the original record in finally below.
            changed = dict(target)
            changed["values_hex"] = list(target["values_hex"])
            set_bin(changed, index, value)
            return replace(path, changed)(root)
        return change

    segment = ("detectors", 0, "sides", 0, "segments", 0)
    checked_segment = ("checks", "detectors", 0, "sides", 0, "segments", 0)
    side = ("detectors", 0, "sides", 0)
    asd_peak = float.fromhex(result["detectors"][0]["sides"][0]["asd"]["values_hex"][M // 4])
    mean_peak = float.fromhex(result["detectors"][0]["sides"][0]["mean_psd"]["values_hex"][M // 4])
    require(asd_peak > 0.0 and mean_peak > 0.0, "fabricated mutation target is zero")
    changes = [
        ("unexpected_top_field", replace(("unexpected",), True), "SCHEMA"),
        ("changed_prior_access_context", replace(("limitations", 0), "Unseen protected validation inputs."), "SCHEMA"),
        ("changed_calibration_claim", replace(("limitations", 1), "Exact calibrated response with zero uncertainty."), "SCHEMA"),
        ("changed_method_budget", replace(("method", "tau_hex"), (2.0 * TAU).hex()), "SCHEMA"),
        ("wrong_array_shape", replace(("frequency_hz", "shape"), [8192]), "SCHEMA"),
        ("wrong_frequency_coordinate", bin_change(("frequency_hz",), 1, 0.5), "BINS"),
        ("stale_window_hash", replace(("window", "values", "sha256"), "0" * 64), "IDENTITY"),
        ("changed_embedded_l1_flag", replace(("inputs", 1, "ri37_detector", "hardware_injection_flags",
                                             "raw_bitfields", 0), 31), "METADATA"),
        ("changed_segment_count", replace(side + ("count",), 6), "SCHEMA"),
        ("negative_psd_with_valid_hash", bin_change(segment + ("psd",), 0, -1.0), "NEGATIVE_PSD"),
        ("nonfinite_scientific_scalar", replace(segment + ("mean",), "nan"), "NONFINITE"),
        ("mean_threshold_not_bound_to_input", replace(checked_segment + ("mean", "threshold"), (1.0).hex()), "TOLERANCE"),
        ("changed_comparison_budget", replace(checked_segment + ("comparison", "threshold"), (1.0).hex()), "SCHEMA"),
        ("wrong_periodogram_mean", bin_change(side + ("mean_psd",), M // 4, 2.0 * mean_peak), "TOLERANCE"),
        ("wrong_asd_with_valid_hash", bin_change(side + ("asd",), M // 4, 2.0 * asd_peak), "TOLERANCE"),
    ]
    refusals = []
    for name, mutate, code in changes:
        undo = mutate(result)
        try:
            refusals.append(refusal("schema/" + name, lambda: validator.validate_result(result),
                                    code, validator.ValidationError))
        finally:
            undo()
    del undo
    require(canonical_identity(result) == fixture_identity, "schema mutations changed positive fixture")
    payload = canonical_payload(result)
    require(identity(payload) == fixture_identity, "streamed canonical fixture differs")
    context = wrapper["context"]
    # Release the original tree and aliases before decoder/encoder validation.
    del result, wrapper, detector, side, segment
    validator.load_result(payload)  # Unchanged full canonical and schema gate.
    for name, body, code in (
        ("duplicate_json_key", b'{"schema": 1, "schema": 2}\n', "SCHEMA"),
        ("json_nonfinite_token", b'{"x": NaN}\n', "NONFINITE"),
    ):
        refusals.append(refusal("schema/" + name, lambda body=body: validator.load_result(body),
                                code, validator.ValidationError))
    # Keep exactly the same complete noncanonical fixture as before, but do not
    # retain its canonical byte twin during the decoder's expected refusal.
    payload = b" " + payload
    refusals.append(refusal("schema/noncanonical_serialization", lambda: validator.load_result(payload),
                            "SCHEMA", validator.ValidationError))
    refusals.append(refusal("schema/missing_top_level", lambda: validator.validate_result({}),
                            "SCHEMA", validator.ValidationError))
    require(len(refusals) == 19, "schema refusal coverage changed")
    return {"context": context, "positive_nested_validation": True,
            "canonical_round_trip": True, "assembly_matches_independently_checked_arrays": True,
            "fabricated_result_identity": fixture_identity,
            "fabricated_input_array": samples_pin, "refusals": refusals,
            "claim": "Deliberately fabricated schema fixture using public metadata; not an observed result or custody receipt."}


def whole_side_checks(primary, np, signal):
    # Index sentinels use only the already specified dyadic tone/constant patterns.
    samples = np.tile(np.array([1.0, 0.0, -1.0, 0.0], dtype=np.float64), N // 4)
    samples[65536:69632] = 1.0
    samples[126976:131072] = np.tile(np.array([1.0, -1.0], dtype=np.float64), 2048)
    sides = {}
    windows = {}
    for side, contract in FIXED_INDICES.items():
        out = primary.side_spectra(samples, side)
        segments = out["segments"]
        if M not in windows:
            windows[M] = array_record(segments[0]["spectrum"]["window"], np)
        require(len(segments) == contract["count"], side + ": count mismatch")
        records, qs, psds = [], [], []
        for expected_start, segment in zip(contract["starts"], segments):
            require(segment["start"] == expected_start and segment["end"] == expected_start + M,
                    side + ": segment endpoints differ")
            checks, q_s = segment_checks(side + "/" + str(expected_start),
                                         samples[expected_start:expected_start + M], segment["spectrum"], signal, np)
            records.append({"start": expected_start, "end": expected_start + M, "checks": checks})
            qs.append(q_s)
            psds.append(segment["spectrum"]["psd"])
        independent_mean = np.array([math.fsum(float(p[k]) for p in psds) / len(psds)
                                     for k in range(M // 2 + 1)], dtype=np.float64)
        q_side = math.fsum(qs) / len(qs)
        a, b = contract["interval"]
        frequency, conventional = signal.welch(samples[a:b], fs=FS, window=segments[0]["spectrum"]["window"],
             nperseg=M, noverlap=M // 2, nfft=M, detrend="constant", return_onesided=True,
             scaling="density", axis=-1, average="mean")
        require(all(float(f) == k / 4.0 for k, f in enumerate(frequency)), side + ": wrong reference frequencies")
        sides[side] = {"segments": records, "input": array_pin(samples[a:b], np),
            "independent_mean": compare_psd(side + "/mean", out["mean_psd"], independent_mean, q_side, FS / M, np),
            "whole_side_welch": compare_psd(side + "/whole_welch", out["mean_psd"], conventional, q_side, FS / M, np),
            "reported_reference": compare_psd(side + "/reported_reference", out["reference_psd"], conventional, q_side, FS / M, np),
            "sqrt": check_sqrt(side + "/sqrt", out["mean_psd"], out["asd"], np),
            "reference_sqrt": check_sqrt(side + "/reference_sqrt", conventional, out["reference_asd"], np),
            "parseval": bound(side + "/parseval", abs(FS / M * math.fsum(float(t) for t in out["mean_psd"]) - q_side), TAU * q_side),
            "primary_q": bound(side + "/q", abs(float(out["q"]) - q_side), TAU * q_side)}
    return samples, sides, windows


def qualification(primary, validator, metadata_report, np, signal):
    require(canonical(primary.fixed_indices()) == canonical(FIXED_INDICES), "fixed index contract differs")
    prepared_windows = primary.prepare_windows()
    require(set(prepared_windows) == {"8", "16", "16384"}, "prepared window length domain differs")
    # Check the large schema fixture before retaining the full analytic evidence.
    # The fixed gates are unchanged; this bounds unnecessary live allocations.
    samples, sides, windows = whole_side_checks(primary, np, signal)
    schema = schema_checks(primary, validator, metadata_report, samples, sides, windows, np)
    kinds = ("zero", "constant_positive", "constant_negative", "quarter_cosine",
             "quarter_sine", "nyquist_cosine", "lowest_cosine")
    analytic, held = [], {}
    for amplitude in AMPLITUDES:
        for kind in kinds:
            name = kind + "/A=" + amplitude.hex()
            x, ideal, ideal_q = analytic_fixture(kind, amplitude, np)
            out = primary.segment_spectrum(x)
            checks, numerical_q = segment_checks(name, x, out, signal, np)
            analytic.append({"name": name, "amplitude_hex": amplitude.hex(), "checks": checks,
                             "ideal_spectrum": compare_psd(name + "/analytic", out["psd"], ideal,
                                                           ideal_q, FS / M, np),
                             "ideal_power": bound(name + "/ideal_Q", abs(numerical_q - ideal_q), TAU * ideal_q)})
            held[(kind, amplitude)] = (out["psd"].copy(), ideal_q)
            if M not in windows:
                windows[M] = array_record(out["window"], np)
            else:
                require(array_record(out["window"], np) == windows[M], "production window changed between fixtures")
    small = []
    for n in (8, 16):
        fixtures = {
            "zero": [0.0] * n,
            "constant": [1.0] * n,
            "impulse_1": [1.0 if j == 1 else 0.0 for j in range(n)],
            "dyadic_period5": [((j % 5) - 2) / 4.0 for j in range(n)],
            "quarter_cosine": [float((1, 0, -1, 0)[j % 4]) for j in range(n)],
        }
        for name, values in fixtures.items():
            label = str(n) + "/" + name
            x = np.array(values, dtype=np.float64)
            out = primary.segment_spectrum(x)
            checks, q = segment_checks(label, x, out, signal, np)
            reference = direct_dft(values)
            dft_psd = np.array(reference["psd"], dtype=np.float64)
            direct_parseval = bound(label + "/direct_parseval",
                                   abs(FS / n * math.fsum(reference["psd"]) - reference["q"]),
                                   TAU * reference["q"])
            small.append({"name": label, "input": array_record(x, np), "checks": checks,
                          "direct_dft": {key: (array_record(value, np) if isinstance(value, list)
                                               else hex_scalar(value)) for key, value in reference.items()},
                          "direct_parseval": direct_parseval,
                          "comparison": compare_psd(label + "/direct", out["psd"], dft_psd, q, FS / n, np)})
            if n not in windows:
                windows[n] = array_record(out["window"], np)
            else:
                require(array_record(out["window"], np) == windows[n], "small window changed between fixtures")
    p, q = held[("quarter_cosine", 1.0)]
    mean, asd = primary.aggregate_periodograms(np.stack((p, 4.0 * p)))
    aggregate = {"mean": compare_psd("aggregation", mean, 2.5 * p, 2.5 * q, FS / M, np),
                 "sqrt": check_sqrt("aggregation_sqrt", mean, asd, np)}
    require(any(abs(float(a) - 1.5 * math.sqrt(float(v))) > 8.0 * EPS * math.sqrt(float(m))
                for a, v, m in zip(asd, p, mean)), "aggregation does not distinguish mean ASD")
    scaling = []
    for kind in kinds:
        p_big, q_big = held[(kind, 1.0)]
        p_small, q_small = held[(kind, AMPLITUDES[1])]
        _, asd_big = primary.aggregate_periodograms(p_big.reshape(1, -1))
        _, asd_small = primary.aggregate_periodograms(p_small.reshape(1, -1))
        expected = p_big * AMPLITUDES[1] ** 2
        cross_limit = math.sqrt(TAU * q_small / (FS / M)) + 8.0 * EPS * math.sqrt(q_small / (FS / M))
        scaling.append({"name": kind, "psd": compare_psd("scaling/" + kind, p_small, expected,
                         q_small, FS / M, np), "large_sqrt": check_sqrt(kind, p_big, asd_big, np),
                        "small_sqrt": check_sqrt(kind, p_small, asd_small, np),
                        "asd_scaling": bound(kind + "/ASD_scaling", max(abs(float(a) - AMPLITUDES[1] * float(b))
                                             for a, b in zip(asd_small, asd_big)), cross_limit)})
    refusals = refusal_checks(primary, np)
    require(len(analytic) == 14 and len(small) == 10 and len(scaling) == 7 and
            len(sides) == 2 and len(refusals) == 18, "qualification case coverage changed")
    for n, window in windows.items():
        require(prepared_windows[str(n)] == {key: window[key] for key in ("bytes", "sha256")},
                "prepared window pin differs from actual fixture window")
    require(primary.prepare_windows() == prepared_windows, "prepared window identities changed")
    return {"analytic_fixtures": analytic, "small_direct_dft": small, "aggregation": aggregate,
            "amplitude_scaling": scaling, "index_contract": FIXED_INDICES,
            "whole_side_fixtures": sides, "windows": {str(n): w for n, w in windows.items()},
            "prepared_windows": prepared_windows,
            "schema_qualification": schema,
            "refusals": refusals, "case_counts": {"analytic": 14, "direct_dft": 10,
            "aggregation": 1, "amplitude_scaling": 7, "whole_sides": 2,
            "producer_expected_refusals": 18, "validator_expected_refusals": 19,
            "validator_positive_cases": 2, "equal_fabricated_metadata_positive_control": 1}}


def main():
    require(len(sys.argv) == 1, "qualify.py takes no arguments and accepts no observed input path")
    primary, validator, runtime, paths, bodies = admission()
    import numpy as np
    from scipy import signal
    metadata_report = strict_json(bodies["input_metadata_report"])
    evidence = qualification(primary, validator, metadata_report, np, signal)
    for name, path in paths.items():
        require(snapshot(path) == bodies[name], "source changed during qualification: " + name)
    report = {"schema": "ri80-fabricated-spectral-qualification-v1",
              "status": "all_fabricated_gates_passed", "runtime": runtime,
              "source_identities": {name: {"path": str(path.relative_to(paths["design"].parent.parent)),
                                    **identity(bodies[name])} for name, path in paths.items()},
              "parameters": {"fs": FS, "segment_length": M, "record_length": N,
                             "eps_hex": EPS.hex(), "tau_hex": TAU.hex(),
                             "amplitudes_hex": [a.hex() for a in AMPLITUDES]},
              "evidence": evidence,
              "limitations": ["Fabricated finite numerical consistency only; no observed strain file opened.",
                              "No certified forward-error, uncertainty, stationarity, calibration or physical claim.",
                              "SciPy Welch and NumPy FFT share PocketFFT lineage.",
                              "Full actual-result admission/custody and actual output qualification remain separate gates."]}
    # Stream the deterministic encoding to avoid a second full evidence-sized
    # string allocation under the frozen sampled-memory budget.
    json.dump(report, sys.stdout, sort_keys=True, indent=2, allow_nan=False, ensure_ascii=True,
              default=evidence_json_default)
    sys.stdout.write("\n")


if __name__ == "__main__":
    try:
        main()
    except (QualificationError, ValueError, TypeError, KeyError, OSError, ArithmeticError, RuntimeError, MemoryError) as error:
        print("RI-80 fabricated qualification refused: " + str(error), file=sys.stderr)
        raise SystemExit(1)
