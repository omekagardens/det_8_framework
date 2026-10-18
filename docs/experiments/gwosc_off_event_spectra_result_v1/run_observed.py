"""RI83 captured-source caller proposal; no observed run or CLI at import.

A reviewed external worker calls execute after admitting this source and the
complete source/runtime/helper freeze. The supervisor owns stdout, failure
receipts and the unchanged 180-second / 512-MiB sampled-RSS limits. This source
never authorizes itself, downloads data, or chooses a method or data interval.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys


SCIENCE = "gwosc_off_event_spectra_implementation_v1/"
INSPECTION = "gwosc_input_qualification_v1/"
RESULT = "gwosc_off_event_spectra_result_v1/"
QUALIFICATION_PIN = {"bytes": 63464716, "sha256": "f247c20f9e112b48cc037d6256b47b5056ec354d58c0cf2817aad0363fc0fa0d"}
WINDOW_PIN = {"bytes": 131072, "sha256": "525f6eb5be56990ea0a936ca11c8860797ee83df453e972cd734d5e065a170e8"}
FIXED_PINS = {
    SCIENCE + "spectra.py": {"bytes": 25668, "sha256": "591321eafeae2faa231bae2409fb6d95227d67976a3ff0f801a37686bc745093"},
    SCIENCE + "validate_result.py": {"bytes": 18529, "sha256": "00514faa329cb4bc05d83de74db49d3b603fe8512f9435844f9af48c0c032a63"},
    SCIENCE + "qualify.py": {"bytes": 38194, "sha256": "1ef4df335fbd1fb50878e1961d41a2697e51351e703f1f743ada08ea1c8b8682"},
    SCIENCE + "QUALIFICATION.json": QUALIFICATION_PIN,
    "gwosc_off_event_spectra_v1/DESIGN.md": {"bytes": 24390, "sha256": "3393eaf9252c55ddd4bb5de6fe87455dd7479f79812dbce245ec7c7611f4b4ce"},
    "gwosc_context_operator_v2/check.py": {"bytes": 38088, "sha256": "a9440a15f31002209ec90519291af510d69813a2c6215b31944beb2eac14fd02"},
    "gwosc_context_operator_v2/QUALIFICATION_REPORT.json": {"bytes": 9413345, "sha256": "1156cd98799c2b458489dd34b4bf5d9a1dfe2c870514691be99fdb1598bc3a6f"},
    INSPECTION + "inspect_inputs.py": {"bytes": 14817, "sha256": "bdafb9c694fc9f33071072f1a2fc027bdb85e9262245ad3f9e29f860935d142a"},
    INSPECTION + "INPUT_REPORT.json": {"bytes": 31096, "sha256": "a734d2f73ed08749090a160f88e5a034077deffcfb4f8bd9abc4cc1c9ccbbe80"},
    INSPECTION + "requirements.txt": {"bytes": 26, "sha256": "d620e6f33b9fedd517072fd58eb8ee36c489edb96f4f57b2f79101d3e68027c4"},
    INSPECTION + "QUALIFICATION.md": {"bytes": 10677, "sha256": "02a99c288d8dbd5be2321f5f947d97c0fe33f1db004146830803b5a6351242f8"},
    "accepted/INPUT_RECOVERY_HANDOFF.json": {"bytes": 16293, "sha256": "be0b518ca43e423d7e2a737b85eec0cad119a1b4cbd19ed4f056f662277d2dc0"},
    "accepted/production_window.f64le": WINDOW_PIN,
}
SOURCE_NAMES = set(FIXED_PINS) | {SCIENCE + "IMPLEMENTATION.md", RESULT + "run_observed.py", RESULT + "EXECUTION.md"}
INPUT_ROOT = Path("/Volumes/AI_DATA/development/det-review-evidence/ri37-input-recovery-20260924T221315Z-9ac44e02/inputs")
INPUTS = (
    {"detector": "H1", "filename": "H-H1_LOSC_4_V2-1126259446-32.hdf5", "bytes": 1040592,
     "md5": "50441a42c13fc1f14e5c4ea5527f1515", "sha256": "6e6976e932074a3b4e4a398ed02c62e30fcaa2781811762caea04937133583f6"},
    {"detector": "L1", "filename": "L-L1_LOSC_4_V2-1126259446-32.hdf5", "bytes": 1007420,
     "md5": "361ae6a040a9fef7897b1e0124d5b0a1", "sha256": "56706e68c811b15548f1d7ed69d7c48d5fcc62aeb21fbaf131355f3cc5c07189"},
)
STARTS = {"left": [0, 8192, 16384, 24576, 32768, 40960, 49152],
          "right": [69632, 77824, 86016, 94208, 102400, 110592]}
LIMITS = {"wall_seconds": 180, "rss_kib": 524288, "target_poll_seconds": 0.025,
          "maximum_sample_gap_seconds": 0.1, "ps_timeout_seconds": 0.05}


class CustodyError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(code + ": " + message)


def require(condition, code, message):
    if not condition:
        raise CustodyError(code, message)


def identity(body):
    return {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()}


def canonical_chunks(value):
    encoder = json.JSONEncoder(sort_keys=True, indent=2, allow_nan=False, ensure_ascii=True)
    for chunk in encoder.iterencode(value):
        yield chunk.encode("utf-8")
    yield b"\n"


def canonical_identity(value):
    size, digest = 0, hashlib.sha256()
    for chunk in canonical_chunks(value):
        size += len(chunk)
        digest.update(chunk)
    return {"bytes": size, "sha256": digest.hexdigest()}


def canonical_path(value):
    path = Path(value)
    require(path.is_absolute() and path == path.resolve() and not path.is_symlink(), "PATH", "canonical nonsymlink path required")
    return path


def source_table(manifest, control):
    rows = manifest["sources"]
    require(type(rows) is list and len(rows) == len(SOURCE_NAMES), "SOURCE", "complete sixteen-file closure required")
    table = {row["relative"]: row for row in rows}
    require(len(table) == len(rows) and set(table) == SOURCE_NAMES, "SOURCE", "source names differ")
    root = canonical_path(manifest["root"])
    for name, row in table.items():
        require(canonical_path(row["copy"]) == root / "experiments" / name, "PATH", "copy layout differs")
        if name in FIXED_PINS:
            require(row["pin"] == FIXED_PINS[name], "SOURCE", "accepted source/report/window pin differs: " + name)
    # The root's freeze supplies the noncircular caller and descriptive-note pins.
    checked = control.verify_sources(manifest)
    require(canonical_path(__file__) == Path(table[RESULT + "run_observed.py"]["copy"]), "SOURCE", "caller is not the captured copy")
    return table, checked


def load_captured(name, item, body):
    path = canonical_path(item["copy"])
    require(identity(body) == item["pin"], "SOURCE", "captured executable body differs")
    require(name not in sys.modules, "SOURCE", "unexpected preloaded local module")
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, "SOURCE", "module specification failed")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    exec(compile(body, str(path), "exec"), module.__dict__)
    return module


def admit_paths(manifest, mode, scientific_stream):
    require(manifest["schema"] == "ri83-observed-execution-freeze-v1" and
            manifest["status"] == "authorized_observed_execution", "ADMISSION", "prospective freeze is not authorization")
    require(mode in ("normal", "optimized"), "ADMISSION", "unknown mode")
    require(sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and
            sys.flags.optimize == (0 if mode == "normal" else 1), "ADMISSION", "launch flags differ")
    root = canonical_path(manifest["root"])
    require(root.is_dir() and canonical_path(root / "tmp").is_dir(), "PATH", "frozen durable root missing")
    require(manifest["limits"] == LIMITS, "ADMISSION", "resource gates differ")
    environment = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TZ": "UTC", "TMPDIR": str(root / "tmp"),
                   "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1",
                   "VECLIB_MAXIMUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1",
                   "__CF_USER_TEXT_ENCODING": "0x1F5:0x0:0x0"}
    require(manifest["environment"] == environment and dict(os.environ) == environment, "ADMISSION", "exact environment differs")
    run = manifest["runs"][mode]
    folder = canonical_path(root / "controls" / mode)
    require(folder.is_dir(), "PATH", "mode parent missing")
    paths = {key: folder / name for key, name in (("stdout", "RESULT.json"), ("input_snapshots", "inputs"),
                                                 ("artifacts", "arrays"), ("custody", "CUSTODY.json"))}
    for key, path in paths.items():
        require(run[key] == str(path) and canonical_path(path) == path, "PATH", "exclusive destination differs")
        if key != "stdout":
            require(not path.exists() and not path.is_symlink(), "PATH", "prior artifact or attempt remains")
    # Parent opened stdout with O_EXCL. Bind the supplied binary stream to that
    # exact empty regular file before output; never open a second result target.
    fd = scientific_stream.fileno()
    opened, named = os.fstat(fd), paths["stdout"].lstat()
    require(stat.S_ISREG(opened.st_mode) and stat.S_ISREG(named.st_mode) and
            opened.st_nlink == named.st_nlink == 1 and opened.st_size == named.st_size == 0 and
            (opened.st_dev, opened.st_ino) == (named.st_dev, named.st_ino) and
            os.lseek(fd, 0, os.SEEK_CUR) == 0, "OUTPUT", "scientific stdout binding differs")
    require(manifest["inputs"] == [{"path": str(INPUT_ROOT / e["filename"]), **e} for e in INPUTS],
            "INPUT", "fixed recovered pair declaration differs")
    return paths, (opened.st_dev, opened.st_ino)


def input_snapshot(entry, destination, control):
    path = canonical_path(INPUT_ROOT / entry["filename"])
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size == entry["bytes"], "INPUT", "input type/size differs")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        require((opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino), "INPUT", "input changed during open")
        payload = stream.read(entry["bytes"] + 1)
        after = os.fstat(stream.fileno())
    key = lambda value: (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns)
    require(key(before) == key(after) == key(path.lstat()), "INPUT", "input changed during snapshot")
    expected = {key: entry[key] for key in ("bytes", "sha256")}
    require(identity(payload) == expected and hashlib.md5(payload, usedforsecurity=False).hexdigest() == entry["md5"],
            "INPUT", "raw input byte identity differs")
    target = destination / entry["filename"]
    with target.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    target.chmod(0o444)
    require(control.file_pin(target) == expected, "INPUT", "retained snapshot differs")
    snapshot_stat = target.lstat()
    describe = lambda value: {"device": value.st_dev, "inode": value.st_ino, "size": value.st_size, "mtime_ns": value.st_mtime_ns}
    return payload, {"detector": entry["detector"], "original": str(path), "snapshot": str(target),
                     "pin": expected, "md5": entry["md5"], "source_stat": describe(before),
                     "snapshot_stat": describe(snapshot_stat)}


def expected_artifacts(result):
    """Enumerate every direct and recursive array retained by accepted build_result."""
    expected = {}
    def add(name, shape, sha256):
        require(name not in expected, "ARTIFACT", "duplicate expected array name")
        expected[name] = {"bytes": shape[0] * 8, "sha256": sha256, "dtype": "<f8", "shape": shape}
    def record(name, row):
        add(name, row["shape"], row["sha256"])
    record("window", result["window"]["values"])
    record("frequency_hz", result["frequency_hz"])
    for detector, checks in zip(result["detectors"], result["checks"]["detectors"], strict=True):
        name = detector["detector"]
        for side, checked in zip(detector["sides"], checks["sides"], strict=True):
            prefix = name + "-" + side["side"]
            require([s["start"] for s in side["segments"]] == STARTS[side["side"]], "ARTIFACT", "segment starts differ")
            for segment, segment_check in zip(side["segments"], checked["segments"], strict=True):
                stem = prefix + "-" + str(segment["start"])
                add(stem + "-demeaned", [16384], segment["demeaned_sha256"])
                add(stem + "-windowed", [16384], segment["windowed_sha256"])
                record(stem + "-psd", segment["psd"])
                record(stem + "-reference_psd", segment_check["reference_psd"])
            for key in ("mean_psd", "asd"):
                record(prefix + "-" + key, side[key])
            for key in ("reference_psd", "reference_asd"):
                record(prefix + "-" + key, checked[key])
    require(len(expected) == 122, "ARTIFACT", "direct array closure differs")
    def walk(value, trail):
        if type(value) is dict and set(value) == {"dtype", "shape", "values_hex", "sha256"}:
            record("result-" + "-".join(trail), value)
        elif type(value) is dict:
            for key in sorted(value):
                walk(value[key], trail + [key])
        elif type(value) is list:
            for index, item in enumerate(value):
                walk(item, trail + [str(index)])
    walk(result, [])
    require(len(expected) == 235, "ARTIFACT", "complete array closure differs")
    return expected


def verify_artifacts(result, inventory, directory, control):
    expected = expected_artifacts(result)
    require(type(inventory) is list and len(inventory) == len(expected), "ARTIFACT", "array inventory count differs")
    seen, output = set(), []
    for row in inventory:
        require(type(row) is dict and set(row) == {"name", "path", "bytes", "sha256", "dtype", "shape"}, "ARTIFACT", "array inventory keys differ")
        require(type(row["name"]) is str and type(row["bytes"]) is int and type(row["shape"]) is list and
                all(type(value) is int for value in row["shape"]), "ARTIFACT", "array inventory field types differ")
        name = row["name"]
        require(name in expected and name not in seen, "ARTIFACT", "missing, duplicate or unexpected array")
        seen.add(name)
        target = directory / (name + ".f64le")
        require(row["path"] == str(target) and canonical_path(target) == target, "PATH", "array path differs")
        require({key: row[key] for key in ("bytes", "sha256", "dtype", "shape")} == expected[name], "ARTIFACT", "array identity/schema differs")
        actual = control.file_pin(target)
        require(actual == {key: row[key] for key in ("bytes", "sha256")}, "ARTIFACT", "retained array bytes differ")
        output.append(dict(row))
    require(set(directory.iterdir()) == {directory / (name + ".f64le") for name in expected}, "ARTIFACT", "unlisted artifact or missing file")
    return sorted(output, key=lambda row: row["name"])


def stream_result(result, scientific_stream, output_path, output_binding, control):
    """Stream exact canonical bytes after the caller's full schema validation."""
    expected_result_pin = canonical_identity(result)
    # Stream the unchanged full scientific schema; never join a second full
    # JSON string or drop all-bin evidence to satisfy the memory envelope.
    digest, size = hashlib.sha256(), 0
    for chunk in canonical_chunks(result):
        scientific_stream.write(chunk)
        digest.update(chunk)
        size += len(chunk)
    scientific_stream.flush()
    os.fsync(scientific_stream.fileno())
    actual_result_pin = {"bytes": size, "sha256": digest.hexdigest()}
    opened, named = os.fstat(scientific_stream.fileno()), output_path.lstat()
    require((opened.st_dev, opened.st_ino) == (named.st_dev, named.st_ino) == output_binding and
            stat.S_ISREG(named.st_mode) and named.st_nlink == 1, "OUTPUT", "scientific output target changed")
    require(actual_result_pin == expected_result_pin == control.file_pin(output_path), "OUTPUT", "canonical scientific output differs")
    return actual_result_pin


def execute(manifest, mode, control, runtime_probe, scientific_stream):
    """Called only by the separately frozen source-capturing external worker.

    control and runtime_probe are that worker's admitted modules, not ambient
    imports or arbitrary callbacks. No function in this file creates permission.
    scientific_stream is the parent-opened binary stdout bound to RESULT.json.
    A return means caller gates passed, not independent/root acceptance.
    """
    paths, output_binding = admit_paths(manifest, mode, scientific_stream)
    table, sources_before = source_table(manifest, control)
    runtime_bytes_before = control.verify_runtime(manifest)
    expected_runtime = control.parse_json(control.verified_body(table["gwosc_context_operator_v2/QUALIFICATION_REPORT.json"]["copy"],
                                                                 FIXED_PINS["gwosc_context_operator_v2/QUALIFICATION_REPORT.json"]))["runtime"]
    runtime_before = runtime_probe.runtime()
    require(runtime_before == manifest["expected_runtime"] == expected_runtime, "RUNTIME", "full qualified runtime differs")
    report_item = table[INSPECTION + "INPUT_REPORT.json"]
    expected_report = control.parse_json(control.verified_body(report_item["copy"], report_item["pin"]))
    # Snapshot each local executable before executing any scientific module.
    bodies = {name: control.verified_body(table[name]["copy"], table[name]["pin"])
              for name in (SCIENCE + "spectra.py", SCIENCE + "validate_result.py", INSPECTION + "inspect_inputs.py")}
    modules = {}
    for name, module_name in ((SCIENCE + "spectra.py", "ri83_captured_spectra"),
                              (SCIENCE + "validate_result.py", "ri83_captured_validator"),
                              (INSPECTION + "inspect_inputs.py", "ri83_captured_inspector")):
        # Reopened bytes must match the already captured executable body.
        require(control.verified_body(table[name]["copy"], table[name]["pin"]) == bodies[name], "SOURCE", "captured source changed")
        modules[module_name] = load_captured(module_name, table[name], bodies[name])
    primary, validator, inspector = (modules[key] for key in ("ri83_captured_spectra", "ri83_captured_validator", "ri83_captured_inspector"))
    require(primary.prepare_windows()["16384"] == WINDOW_PIN, "WINDOW", "qualified pre-observed window differs")
    paths["input_snapshots"].mkdir(mode=0o700)
    payloads, input_records = {}, []
    for entry in INPUTS:
        payload, record = input_snapshot(entry, paths["input_snapshots"], control)
        payloads[entry["detector"]] = payload
        input_records.append(record)
    # Both complete immutable bodies and exclusive retained snapshots exist
    # before build_result performs either unchanged RI37 HDF5 inspection.
    result, inventory = primary.build_result(payloads, inspector, expected_report,
                                             QUALIFICATION_PIN, WINDOW_PIN, paths["artifacts"])
    require(validator.validate_result(result) is True, "VALIDATION", "full scientific result refused")
    artifacts = verify_artifacts(result, inventory, paths["artifacts"], control)
    sources_after = control.verify_sources(manifest)
    runtime_after = runtime_probe.runtime()
    runtime_bytes_after = control.verify_runtime(manifest)
    require(runtime_after == runtime_before and runtime_bytes_after == runtime_bytes_before,
            "RUNTIME", "runtime changed during observed calculation")
    require(primary.prepare_windows()["16384"] == WINDOW_PIN, "WINDOW", "prepared window changed")
    for entry, row in zip(INPUTS, input_records, strict=True):
        require(identity(payloads[entry["detector"]]) == row["pin"], "INPUT", "in-memory snapshot changed")
        for key in ("original", "snapshot"):
            path = canonical_path(row[key])
            information = path.lstat()
            state = {"device": information.st_dev, "inode": information.st_ino,
                     "size": information.st_size, "mtime_ns": information.st_mtime_ns}
            expected_stat = row["source_stat" if key == "original" else "snapshot_stat"]
            require(state == expected_stat and control.file_pin(path) == row["pin"], "INPUT", "post-run input identity or bytes changed")
    actual_result_pin = stream_result(result, scientific_stream, paths["stdout"], output_binding, control)
    # Reopen every binary artifact after serialization as well as before it.
    require(verify_artifacts(result, inventory, paths["artifacts"], control) == artifacts, "ARTIFACT", "artifact closure changed")
    custody = {"schema": "ri83-observed-caller-custody-v1", "status": "caller_gates_passed_pending_independent_review",
               "mode": mode, "inputs": input_records, "qualification_pin": QUALIFICATION_PIN, "window_pin": WINDOW_PIN,
               "result": {"path": str(paths["stdout"]), **actual_result_pin}, "artifacts": artifacts,
               "source_before": sources_before, "source_after": sources_after,
               "runtime_before": runtime_before, "runtime_after": runtime_after,
               "runtime_bytes_before": runtime_bytes_before, "runtime_bytes_after": runtime_bytes_after,
               "limitations": list(primary.LIMITATIONS),
               "external_gates": "Supervisor must admit exact source/runtime/helper/authorization bytes, enforce limits, retain failures, recheck after exit, and require serial normal/optimized result equality. Independent observed evidence review and root acceptance remain separate."}
    control.write_exclusive(paths["custody"], custody)
    return {"custody": {"path": str(paths["custody"]), **control.file_pin(paths["custody"])},
            "result": custody["result"], "artifact_count": len(artifacts)}


if __name__ == "__main__":
    raise SystemExit("RI83 requires the separately reviewed captured-source worker; no direct observed CLI is authorized.")
