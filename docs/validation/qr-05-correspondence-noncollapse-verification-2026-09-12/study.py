"""Source-bound exact report and write-once capture; no engine imports at import time."""

import argparse
import contextlib
import copy
import hashlib
import json
import math
import os
import platform
import signal
import stat
import sys
import time
import types
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
STUDY_SECONDS = 30
SUITE_SECONDS = 60
SOURCE_PATHS = (
    "README.md",
    "fixtures.py",
    "primary.py",
    "reference.py",
    "study.py",
    "test_calculus.py",
    "test_evidence.py",
    "../qr-05-correspondence-noncollapse-design-2026-09-12/README.md",
    "../qr-05-correspondence-noncollapse-design-2026-09-12/RESULTS.md",
)
FREEZE_SCHEMA = "qr05-correspondence-noncollapse-freeze-v1"
CAPTURE_SCHEMA = "qr05-correspondence-noncollapse-capture-v1"
REPORT_SCHEMA = "qr05-correspondence-noncollapse-report-v1"
ACTIVE_FREEZE_BYTES = None


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
        )
        + "\n"
    ).encode("utf-8")


def native_json(value):
    """No bool/int or Fraction/integer coercion, even for integral Fractions."""
    if type(value) is Fraction:
        return {"fraction": [value.numerator, value.denominator]}
    if value is None or type(value) in (str, int, bool):
        return value
    if type(value) is list:
        return [native_json(item) for item in value]
    if type(value) is dict and all(type(key) is str for key in value):
        return {key: native_json(item) for key, item in value.items()}
    raise TypeError("unsupported native report type")


def exact_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(exact_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(exact_equal(x, y) for x, y in zip(a, b))
    if a is None or type(a) in (Fraction, str, int, bool):
        return a == b
    raise TypeError("unsupported equality operand")


def read_regular(path, limit):
    path = Path(path)
    before = path.stat(follow_symlinks=False)
    if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
        raise ValueError("file must be bounded, regular and nonsymlink")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        first = os.fstat(handle.fileno())
        if not stat.S_ISREG(first.st_mode) or first.st_size > limit:
            raise ValueError("opened file violates bounds")
        data = handle.read(limit + 1)
        last = os.fstat(handle.fileno())
    after = path.stat(follow_symlinks=False)
    signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)
    if len(data) > limit or any(signature(s) != signature(before) for s in (first, last, after)):
        raise ValueError("source changed while reading")
    return data


def parse_canonical(data):
    if type(data) is not bytes or len(data) > ARTIFACT_LIMIT:
        raise ValueError("invalid artifact bytes or size")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate JSON key")
            out[key] = value
        return out

    def reject(_):
        raise ValueError("nonintegral/nonfinite JSON number")

    try:
        result = json.loads(
            data.decode("utf-8"), object_pairs_hook=pairs, parse_float=reject, parse_constant=reject
        )
        if canonical(result) != data:
            raise ValueError("noncanonical JSON bytes")
        return result
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("invalid JSON encoding/depth") from exc


def source_bytes(root=ROOT):
    return {name: read_regular(Path(root) / name, SOURCE_LIMIT) for name in SOURCE_PATHS}


def inventory(blobs):
    return {name: {"bytes": len(data), "sha256": sha(data)} for name, data in blobs.items()}


def write_new(path, data):
    if len(data) > ARTIFACT_LIMIT:
        raise ValueError("artifact exceeds byte cap")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags, 0o644), "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def create_freeze(root=ROOT):
    """Metadata only: never imports fixtures or mathematical engines."""
    capture_path = Path(root) / "results.json"
    if capture_path.exists() or capture_path.is_symlink():
        raise FileExistsError("cannot replace the source context of an existing capture")
    result = {
        "schema": FREEZE_SCHEMA,
        "sources": inventory(source_bytes(root)),
        "runtime": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "optimization": sys.flags.optimize,
        },
    }
    path = Path(root) / "source-freeze.json"
    data = canonical(result)
    write_new(path, data)
    if read_regular(path, ARTIFACT_LIMIT) != data:
        raise ValueError("freeze publication readback mismatch")
    if not exact_equal(result["sources"], inventory(source_bytes(root))):
        raise ValueError("sources changed during freeze publication")
    return result


def authenticated_sources(root=ROOT):
    freeze_bytes = read_regular(Path(root) / "source-freeze.json", ARTIFACT_LIMIT)
    freeze = parse_canonical(freeze_bytes)
    if type(freeze) is not dict or set(freeze) != {"schema", "sources", "runtime"}:
        raise ValueError("freeze structure")
    if freeze["schema"] != FREEZE_SCHEMA:
        raise ValueError("freeze schema")
    blobs = source_bytes(root)
    if not exact_equal(freeze["sources"], inventory(blobs)):
        raise ValueError("source binding mismatch")
    runtime = freeze["runtime"]
    if (
        type(runtime) is not dict
        or set(runtime) != {"implementation", "version", "optimization"}
        or type(runtime["implementation"]) is not str
        or type(runtime["version"]) is not str
        or type(runtime["optimization"]) is not int
        or runtime["optimization"] not in (0, 1, 2)
    ):
        raise ValueError("freeze runtime metadata")
    return freeze_bytes, freeze, blobs


def _module(name, source, root):
    module = types.ModuleType("qr05_cnv_" + name)
    module.__file__ = str(Path(root) / (name + ".py"))
    # Callers provide the bytes already authenticated against the fixed freeze.
    exec(compile(source, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


def load_engines(root=ROOT):
    fb, _, blobs = authenticated_sources(root)
    if ACTIVE_FREEZE_BYTES is not None and Path(root) == ROOT and fb != ACTIVE_FREEZE_BYTES:
        raise ValueError("suite source snapshot changed before engine loading")
    return (
        _module("primary", blobs["primary.py"], root),
        _module("reference", blobs["reference.py"], root),
    )


@contextlib.contextmanager
def deadline(seconds):
    """Preserve a surrounding suite alarm when a study gets its shorter cap."""
    if type(seconds) is not int or seconds <= 0:
        raise ValueError("positive integral deadline required")
    start = time.monotonic()
    old_handler = signal.getsignal(signal.SIGALRM)
    old_remaining, old_interval = signal.getitimer(signal.ITIMER_REAL)

    def timed_out(_signum, _frame):
        raise TimeoutError("bounded verification deadline exceeded")

    signal.signal(signal.SIGALRM, timed_out)
    signal.setitimer(signal.ITIMER_REAL, min(seconds, old_remaining) if old_remaining else seconds)
    try:
        yield
        if time.monotonic() - start > seconds:
            raise TimeoutError("study exceeded elapsed cap")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        if old_remaining:
            remaining = old_remaining - (time.monotonic() - start)
            signal.setitimer(signal.ITIMER_REAL, max(remaining, 0.000001), old_interval)


def _both(engines, method, *args):
    original = list(args)
    left, right = copy.deepcopy(original), copy.deepcopy(original)
    a = getattr(engines[0], method)(*left)
    b = getattr(engines[1], method)(*right)
    if not exact_equal(left, original) or not exact_equal(right, original):
        raise ValueError("mathematical route mutated its input")
    if not exact_equal(a, b):
        raise ValueError("independent route mismatch: " + method)
    native_json(a)  # Reject unsupported leaves before evidence retention.
    return a


def control_report(inputs, engines):
    out = {}
    t = inputs["triangle"]
    x, y, z = t["chains"]
    r = t["members"]
    composed = [list(pair) for pair in sorted({(a, c) for a, b in r for v, c in r if b == v})]
    out["triangle"] = {
        "input": t,
        "composed_members": composed,
        "xy": _both(engines, "compare", x, y),
        "yz": _both(engines, "compare", y, z),
        "xz": _both(engines, "compare", x, z),
        "yx": _both(engines, "compare", y, x),
        "relation_xy": _both(engines, "relation_record", x, y, r),
        "relation_yz": _both(engines, "relation_record", y, z, r),
        "relation_xz": _both(engines, "relation_record", x, z, composed),
    }
    g = inputs["gap_boundary"]
    out["gap_boundary"] = {
        "input": g,
        "comparison": _both(engines, "compare", g["x"], g["y"]),
        "relation": _both(engines, "relation_record", g["x"], g["y"], g["members"]),
    }
    f = inputs["fit_asymmetry"]
    half_b = [[f["scale"] * v for v in row] for row in f["b"]]
    out["fit_asymmetry"] = {
        "input": f,
        "scaled_b": half_b,
        "a_half_b": _both(engines, "compare", f["a"], half_b),
        "b_a": _both(engines, "compare", f["b"], f["a"]),
    }
    p = inputs["paired_list"]
    residuals = [a - p["c"] * b for a, b in zip(p["L"], p["tau"])]
    u = max(abs(v) for v in residuals)
    mean = sum(p["L"], Fraction(0)) / len(p["L"])
    out["paired_list"] = {
        "input": p,
        "residuals": residuals,
        "u": u,
        "mean": mean,
        "declared": p["ell"] * u,
        "surrogate": u / mean,
        "scale_factor": p["ell"] * mean,
        "lower_bound_identity": 3 * residuals[0] - residuals[2],
    }
    t = inputs["endpoint_trim"]
    rr = _both(engines, "relation_record", t["x"], t["y"], t["members"])
    err = rr["raw"]["errors"]
    positive = [err[i][j] for i in range(3) for j in range(3) if t["x"][i][j] > 0]
    out["endpoint_trim"] = {
        "input": t,
        "relation": rr,
        "full_mean": sum((sum(row, Fraction(0)) for row in err), Fraction(0)) / 9,
        "positive_mean": sum(positive, Fraction(0)) / len(positive),
        "trimmed_mean": sum((err[i][j] for i, j in t["included"]), Fraction(0))
        / len(t["included"]),
    }
    l = inputs["lipschitz"]
    zero = _both(engines, "closure", l["order"], l["zero"])
    unit = _both(engines, "closure", l["order"], l["unit"])
    ni = max(abs(l["unit"][i][j] - l["zero"][i][j]) for i in range(3) for j in range(3))
    no = max(abs(unit["closure"][i][j] - zero["closure"][i][j]) for i in range(3) for j in range(3))
    out["lipschitz"] = {
        "input": l,
        "zero": zero,
        "unit": unit,
        "input_norm": ni,
        "output_norm": no,
        "bound": 2 * ni,
    }
    return out


def _build_report(root, expected_freeze=None):
    if expected_freeze is None and Path(root) == ROOT:
        expected_freeze = ACTIVE_FREEZE_BYTES
    original_bytes, _, blobs = authenticated_sources(root)
    if expected_freeze is not None and original_bytes != expected_freeze:
        raise ValueError("source snapshot changed before engine loading")
    engines = (
        _module("primary", blobs["primary.py"], root),
        _module("reference", blobs["reference.py"], root),
    )
    fixtures = _module("fixtures", blobs["fixtures.py"], root)
    comparisons, closures = [], []
    census = {key: 0 for key in fixtures.EXPECTED_CENSUS}
    for case in fixtures.comparison_cases():
        result = _both(engines, "compare", case["x"], case["y"])
        comparisons.append(
            {
                "case": case,
                "inverse_x_map": [case["x_map"].index(i) for i in range(len(case["x"]))],
                "inverse_y_map": [case["y_map"].index(i) for i in range(len(case["y"]))],
                "result": result,
            }
        )
        m, n = len(case["x"]), len(case["y"])
        census["comparison_rows"] += 1
        census["input_nodes"] += m + n
        census["input_cells"] += m * m + n * n
        census["bitmask_universe"] += result["bitmask_universe"]
        census["relations"] += len(result["relations"])
        census["bijections"] += len(result["bijections"] or [])
        for relation in result["relations"]:
            k = len(relation["members"])
            census["relation_members"] += k
            census["raw_cells"] += sum(len(row) for row in relation["raw"]["errors"])
            if relation["normalized"] is not None:
                census["normalized_cells"] += sum(
                    len(row) for row in relation["normalized"]["errors"]
                )
    for case in fixtures.closure_cases():
        result = _both(engines, "closure", case["order"], case["weights"])
        n = len(case["weights"])
        closures.append(
            {
                "case": case,
                "inverse_map": [case["map"].index(i) for i in range(n)],
                "result": result,
            }
        )
        census["closure_rows"] += 1
        census["closure_nodes"] += n
        census["closure_cells"] += n * n
        census["comparable_slots"] += sum(sum(row) for row in case["order"])
    if not exact_equal(census, fixtures.EXPECTED_CENSUS):
        raise ValueError("study census mismatch")
    report = {
        "schema": REPORT_SCHEMA,
        "comparison_rows": comparisons,
        "closure_rows": closures,
        "controls": control_report(fixtures.controls(), engines),
        "census": census,
    }
    if authenticated_sources(root)[0] != original_bytes:
        raise ValueError("freeze changed during study")
    return report


def build_report(root=ROOT):
    with deadline(STUDY_SECONDS):
        result = _build_report(root)
        if len(canonical(native_json(result))) > ARTIFACT_LIMIT:
            raise ValueError("report exceeds artifact cap")
        return result


def validate_wire(value):
    """Reject malformed rational tags and non-native leaves before execution."""
    if value is None or type(value) in (str, int, bool):
        return
    if type(value) is list:
        for item in value:
            validate_wire(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        if "fraction" in value:
            pair = value["fraction"]
            if (
                set(value) != {"fraction"}
                or type(pair) is not list
                or len(pair) != 2
                or any(type(v) is not int for v in pair)
                or pair[1] <= 0
                or math.gcd(pair[0], pair[1]) != 1
            ):
                raise ValueError("malformed or unreduced Fraction tag")
        else:
            for item in value.values():
                validate_wire(item)
        return
    raise ValueError("unsupported wire value")


def validate_capture(data, root=ROOT, expected_freeze=None):
    value = parse_canonical(data)
    fb, freeze, _ = authenticated_sources(root)
    if expected_freeze is not None and fb != expected_freeze:
        raise ValueError("capture source snapshot changed")
    if type(value) is not dict or set(value) != {"schema", "freeze_sha256", "sources", "report"}:
        raise ValueError("capture structure")
    if value["schema"] != CAPTURE_SCHEMA or value["freeze_sha256"] != sha(fb):
        raise ValueError("capture schema/freeze binding")
    if not exact_equal(value["sources"], freeze["sources"]):
        raise ValueError("capture source bindings")
    report = value["report"]
    if type(report) is not dict or set(report) != {
        "schema",
        "comparison_rows",
        "closure_rows",
        "controls",
        "census",
    }:
        raise ValueError("report structure")
    if report["schema"] != REPORT_SCHEMA:
        raise ValueError("report schema")
    validate_wire(report)
    return value


def capture(root=ROOT):
    path = Path(root) / "results.json"
    if path.exists() or path.is_symlink():
        raise FileExistsError("first capture already exists")
    with deadline(STUDY_SECONDS):
        fb, freeze, _ = authenticated_sources(root)
        report = native_json(_build_report(root, fb))
        value = {
            "schema": CAPTURE_SCHEMA,
            "freeze_sha256": sha(fb),
            "sources": freeze["sources"],
            "report": report,
        }
        data = canonical(value)
        validate_capture(data, root, fb)
        write_new(path, data)
        retained = read_regular(path, ARTIFACT_LIMIT)
        if retained != data:
            raise ValueError("capture publication readback mismatch")
        validate_capture(retained, root, fb)
    return {
        "capture_bytes": len(data),
        "capture_sha256": sha(data),
        "report_bytes": len(canonical(report)),
        "report_sha256": sha(canonical(report)),
        "census": report["census"],
    }


def replay(root=ROOT):
    with deadline(STUDY_SECONDS):
        first = read_regular(Path(root) / "results.json", ARTIFACT_LIMIT)
        fb, _, _ = authenticated_sources(root)
        saved = validate_capture(first, root, fb)
        actual = native_json(_build_report(root, fb))
        if not exact_equal(saved["report"], actual):
            raise ValueError("full capture replay mismatch")
        if read_regular(Path(root) / "results.json", ARTIFACT_LIMIT) != first:
            raise ValueError("capture changed during replay")
        if authenticated_sources(root)[0] != fb:
            raise ValueError("freeze changed during replay")
    return {
        "capture_sha256": sha(first),
        "report_sha256": sha(canonical(actual)),
        "matched": True,
        "runtime": platform.python_version(),
        "optimization": sys.flags.optimize,
    }


def run_tests():
    global ACTIVE_FREEZE_BYTES
    start = time.monotonic()
    with deadline(SUITE_SECONDS):
        fb, _, blobs = authenticated_sources()
        capture_bytes = read_regular(ROOT / "results.json", ARTIFACT_LIMIT)
        validate_capture(capture_bytes, expected_freeze=fb)
        ACTIVE_FREEZE_BYTES = fb
        previous = sys.modules.get("study")
        sys.modules["study"] = sys.modules[__name__]
        try:
            modules = [
                _module(name, blobs[name + ".py"], ROOT)
                for name in ("test_calculus", "test_evidence")
            ]
            suite = unittest.TestSuite(
                unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules
            )
            outcome = unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
            if outcome.testsRun != 39 or not outcome.wasSuccessful():
                raise ValueError("full frozen test inventory did not pass")
            if authenticated_sources()[0] != fb:
                raise ValueError("sources changed during suite")
            if read_regular(ROOT / "results.json", ARTIFACT_LIMIT) != capture_bytes:
                raise ValueError("capture changed during suite")
        finally:
            ACTIVE_FREEZE_BYTES = None
            if previous is None:
                sys.modules.pop("study", None)
            else:
                sys.modules["study"] = previous
    return {
        "tests": outcome.testsRun,
        "successful": True,
        "elapsed_seconds": format(time.monotonic() - start, ".6f"),
        "runtime": platform.python_version(),
        "optimization": sys.flags.optimize,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("freeze", "capture", "replay", "sources", "tests"))
    action = parser.parse_args().action
    if action == "freeze":
        result = create_freeze()
    elif action == "capture":
        result = capture()
    elif action == "replay":
        result = replay()
    elif action == "tests":
        result = run_tests()
    else:
        fb, freeze, _ = authenticated_sources()
        result = {"freeze_sha256": sha(fb), "sources": len(freeze["sources"])}
    print(canonical(result).decode("utf-8"), end="")


if __name__ == "__main__":
    main()
