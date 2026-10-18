"""Bounded exact QR-05BM evidence and public packet boundary (stdlib only)."""

import argparse
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
from contextlib import contextmanager
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_LIMIT = 262144
ARTIFACT_LIMIT = 16777216
PROTOCOL_SHA256 = "776d6a8645903f763748a2e1804a43d45bb9f78c4869f2b8254e21fdec74e46f"
SOURCE_PATHS = (
    "README.md",
    "protocol.json",
    "primary.py",
    "reference.py",
    "study.py",
    "test_qr05bm.py",
    "../qr-05bl-relative-volume-design-2026-09-09/README.md",
    "../qr-05bl-relative-volume-design-2026-09-09/RESULTS.md",
)
EXPECTED_PROTOCOL = {
    "schema": "qr05bm-protocol-v1",
    "quota": 4,
    "worlds": [
        {"id": "A", "eta": 0, "scale": 1, "density_uv": 0},
        {"id": "B", "eta": 1, "scale": 1, "density_uv": 0},
        {"id": "C", "eta": 0, "scale": 1, "density_uv": 1},
        {"id": "D", "eta": 0, "scale": 4, "density_uv": 0},
        {"id": "E", "eta": 1, "scale": 4, "density_uv": 0},
    ],
    "regions": {"Q": [[0, 1], [1, 1], [0, 1], [1, 1]], "I": [[0, 1], [1, 2], [0, 1], [1, 2]]},
    "chart": {"U_scale": 2, "U_offset": 1, "V_scale": 3, "V_offset": -1},
    "menus": [
        {"id": "positive", "worlds": ["A", "B"]},
        {"id": "expanded", "worlds": ["A", "B", "C", "D", "E"]},
    ],
    "observer": {
        "protocol": "qr05bm-v1",
        "query": "o-m-t",
        "variants": ["membership", "membership-z"],
    },
    "coverage": {"membership": 80, "cq": 1280, "histogram": 25},
    "limits": {
        "source_bytes": SOURCE_LIMIT,
        "artifact_bytes": ARTIFACT_LIMIT,
        "analysis_seconds": 30,
        "suite_seconds": 120,
        "alternate_reference_runs": 1,
    },
}


def require_equal(left, right, path="$"):
    """Do not let bool/int, Fraction/int, tuples/lists or extra keys compare equal."""
    if type(left) is not type(right):
        raise ValueError(f"native type mismatch at {path}")
    kind = type(left)
    if kind is dict:
        if any(type(k) is not str for k in left) or any(type(k) is not str for k in right):
            raise ValueError(f"non-string key at {path}")
        if left.keys() != right.keys():
            raise ValueError(f"key mismatch at {path}")
        for key in left:
            require_equal(left[key], right[key], f"{path}.{key}")
    elif kind is list:
        if len(left) != len(right):
            raise ValueError(f"length mismatch at {path}")
        for index, (a, b) in enumerate(zip(left, right)):
            require_equal(a, b, f"{path}[{index}]")
    elif kind in (str, int, bool, Fraction):
        if left != right:
            raise ValueError(f"value mismatch at {path}")
    else:
        raise ValueError(f"unsupported native type at {path}")


def _json_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _no_float(value):
    raise ValueError("floating/nonfinite JSON value forbidden")


def strict_loads(data):
    if type(data) is not bytes or len(data) > ARTIFACT_LIMIT:
        raise ValueError("JSON requires bounded bytes")
    try:
        return json.loads(
            data.decode("utf-8"),
            object_pairs_hook=_json_object,
            parse_float=_no_float,
            parse_constant=_no_float,
        )
    except (UnicodeError, RecursionError) as exc:
        raise ValueError("invalid JSON encoding/depth") from exc


def encode(value):
    kind = type(value)
    if kind is Fraction:
        return {"$fraction": [value.numerator, value.denominator]}
    if kind in (str, int, bool):
        return value
    if kind is list:
        return [encode(item) for item in value]
    if kind is dict:
        if any(type(k) is not str or k.startswith("$") for k in value):
            raise ValueError("invalid native report key")
        return {key: encode(item) for key, item in value.items()}
    raise ValueError("unsupported native report type")


def decode(value):
    kind = type(value)
    if kind in (str, int, bool):
        return value
    if kind is list:
        return [decode(item) for item in value]
    if kind is dict:
        if any(type(k) is not str for k in value):
            raise ValueError("non-string encoded key")
        if "$fraction" in value:
            pair = value["$fraction"]
            if (
                set(value) != {"$fraction"}
                or type(pair) is not list
                or len(pair) != 2
                or any(type(v) is not int for v in pair)
                or pair[1] <= 0
                or math.gcd(pair[0], pair[1]) != 1
            ):
                raise ValueError("noncanonical fraction")
            return Fraction(*pair)
        if any(k.startswith("$") for k in value):
            raise ValueError("unknown encoded tag")
        return {key: decode(item) for key, item in value.items()}
    raise ValueError("unsupported encoded type")


def canonical(value):
    # decode/encode is not done here: source identities and runtime are plain JSON.
    def check(item):
        if type(item) in (str, int, bool):
            return
        if type(item) is list:
            for part in item:
                check(part)
            return
        if type(item) is dict and all(type(k) is str for k in item):
            for part in item.values():
                check(part)
            return
        raise ValueError("noncanonical JSON type")

    check(value)
    data = (
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        )
        + "\n"
    ).encode("utf-8")
    if len(data) > ARTIFACT_LIMIT:
        raise ValueError("artifact byte bound exceeded")
    return data


def read_bounded(path, limit=ARTIFACT_LIMIT):
    path = Path(path)
    if type(limit) is not int or not 0 < limit <= ARTIFACT_LIMIT or path.is_symlink():
        raise ValueError("invalid read target or limit")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    try:
        if not stat.S_ISREG(path.stat(follow_symlinks=False).st_mode):
            raise ValueError("read requires a regular file")
        with os.fdopen(os.open(path, flags), "rb") as handle:
            before = os.fstat(handle.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
                raise ValueError("read requires a bounded regular file")
            data = handle.read(limit + 1)
            after = os.fstat(handle.fileno())
        visible = path.stat(follow_symlinks=False)
    except OSError as exc:
        raise ValueError("unreadable file") from exc
    key = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    if (
        len(data) > limit
        or key(before) != key(after)
        or key(after) != key(visible)
        or not stat.S_ISREG(visible.st_mode)
    ):
        raise ValueError("file changed during bounded read")
    return data


def source_snapshot():
    return {name: read_bounded(ROOT / name, SOURCE_LIMIT) for name in SOURCE_PATHS}


def identities(snapshot):
    return {
        name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        for name, data in snapshot.items()
    }


def _check_snapshot(snapshot):
    if snapshot != source_snapshot():
        raise ValueError("source bytes changed")


def load_engine(blob, name):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / (name + ".py"))
    # Deliberate fresh execution of the driver's source-bound local engine bytes.
    exec(compile(blob, module.__file__, "exec"), module.__dict__)  # noqa: S102
    return module


@contextmanager
def _analysis_deadline():
    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)
    earlier_outer = 0 < previous_timer[0] <= 30

    def expired(signum, frame):
        if earlier_outer:
            if callable(previous_handler):
                previous_handler(signum, frame)
            raise ValueError("enclosing deadline expired during analysis")
        raise ValueError("30-second analysis bound exceeded")

    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, previous_timer[0] if earlier_outer else 30)
    started = time.monotonic()
    try:
        yield
        if time.monotonic() - started > 30:
            raise ValueError("30-second analysis bound exceeded")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer[0] > 0:
            remaining = max(0.000001, previous_timer[0] - (time.monotonic() - started))
            signal.setitimer(signal.ITIMER_REAL, remaining, previous_timer[1])


def analyze():
    with _analysis_deadline():
        snapshot = source_snapshot()
        if hashlib.sha256(snapshot["protocol.json"]).hexdigest() != PROTOCOL_SHA256:
            raise ValueError("protocol bytes differ from prospective specification")
        protocol = strict_loads(snapshot["protocol.json"])
        require_equal(protocol, EXPECTED_PROTOCOL)
        reports = []
        for filename in ("primary.py", "reference.py"):
            supplied = copy.deepcopy(protocol)
            engine = load_engine(snapshot[filename], filename[:-3])
            report = engine.analyze(supplied)
            require_equal(supplied, protocol)
            # Validate supported native types even if both engines share a mistake.
            require_equal(report, report)
            reports.append(report)
        require_equal(reports[0], reports[1])
        _check_snapshot(snapshot)
        return reports[0]


def estimate(packet):
    """Public record-only estimator. No file, model, world or likelihood input."""
    if (
        type(packet) is not dict
        or any(type(k) is not str for k in packet)
        or set(packet) != {"protocol", "query", "variant", "records"}
    ):
        raise ValueError("packet fields")
    for field in ("protocol", "query", "variant"):
        if type(packet[field]) is not str:
            raise ValueError("metadata type")
    if (
        packet["protocol"] != "qr05bm-v1"
        or packet["query"] != "o-m-t"
        or packet["variant"] not in ("membership", "membership-z")
    ):
        raise ValueError("metadata value")
    records = packet["records"]
    if type(records) is not list or len(records) != 4:
        raise ValueError("quota")
    fields = {"attempt", "y"}
    with_z = packet["variant"] == "membership-z"
    if with_z:
        fields = fields | {"z"}
    total = 0
    for attempt, record in enumerate(records, 1):
        if (
            type(record) is not dict
            or any(type(k) is not str for k in record)
            or set(record) != fields
        ):
            raise ValueError("record fields")
        if type(record["attempt"]) is not int or record["attempt"] != attempt:
            raise ValueError("attempt identity/order")
        if type(record["y"]) is not int or record["y"] not in (0, 1):
            raise ValueError("membership value")
        if with_z and (type(record["z"]) is not int or record["z"] not in (-1, 1)):
            raise ValueError("Z value")
        total += record["y"]
    return Fraction(total, 4)


def _write_new(path, data):
    if type(data) is not bytes or len(data) > ARTIFACT_LIMIT:
        raise ValueError("invalid output bytes")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    # Preserve any partial or failed file for audit; never unlink or overwrite it.
    with os.fdopen(os.open(Path(path), flags, 0o644), "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if read_bounded(path) != data:
        raise ValueError("publication readback differs")


def freeze(path):
    snapshot = source_snapshot()
    if hashlib.sha256(snapshot["protocol.json"]).hexdigest() != PROTOCOL_SHA256:
        raise ValueError("protocol bytes differ from prospective specification")
    require_equal(strict_loads(snapshot["protocol.json"]), EXPECTED_PROTOCOL)
    artifact = {
        "schema": "qr05bm-source-freeze-v1",
        "sources": identities(snapshot),
        "runtime": {
            "implementation": platform.python_implementation(),
            "version": platform.python_version(),
            "optimization": sys.flags.optimize,
        },
    }
    _check_snapshot(snapshot)
    data = canonical(artifact)
    _write_new(path, data)
    _check_snapshot(snapshot)
    if read_bounded(path) != data:
        raise ValueError("freeze changed after publication")
    return artifact


def _checked_freeze(path, snapshot):
    data = read_bounded(path)
    value = strict_loads(data)
    if type(value) is not dict or set(value) != {"schema", "sources", "runtime"}:
        raise ValueError("freeze schema")
    runtime = value["runtime"]
    if (
        type(runtime) is not dict
        or set(runtime) != {"implementation", "version", "optimization"}
        or type(runtime["implementation"]) is not str
        or not runtime["implementation"]
        or type(runtime["version"]) is not str
        or not runtime["version"]
        or type(runtime["optimization"]) is not int
        or runtime["optimization"] not in (0, 1, 2)
    ):
        raise ValueError("freeze runtime types")
    require_equal(value["schema"], "qr05bm-source-freeze-v1")
    require_equal(value["sources"], identities(snapshot))
    if canonical(value) != data:
        raise ValueError("noncanonical freeze bytes")
    return data


def _stable_inputs(snapshot, freeze_path, freeze_data):
    _check_snapshot(snapshot)
    if read_bounded(freeze_path) != freeze_data:
        raise ValueError("freeze changed")


def capture(path, freeze_path=ROOT / "source-freeze.json"):
    if Path(path).exists() or Path(path).is_symlink():
        raise FileExistsError(str(path))
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    report = analyze()
    _stable_inputs(snapshot, freeze_path, freeze_data)
    artifact = {
        "schema": "qr05bm-capture-v1",
        "sources": identities(snapshot),
        "freeze_sha256": hashlib.sha256(freeze_data).hexdigest(),
        "report": encode(report),
    }
    data = canonical(artifact)
    _write_new(path, data)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("capture changed after publication")
    return report


def replay(path, freeze_path=ROOT / "source-freeze.json"):
    snapshot = source_snapshot()
    freeze_data = _checked_freeze(freeze_path, snapshot)
    data = read_bounded(path)
    artifact = strict_loads(data)
    if type(artifact) is not dict or set(artifact) != {
        "schema",
        "sources",
        "freeze_sha256",
        "report",
    }:
        raise ValueError("capture schema")
    require_equal(artifact["schema"], "qr05bm-capture-v1")
    require_equal(artifact["sources"], identities(snapshot))
    require_equal(artifact["freeze_sha256"], hashlib.sha256(freeze_data).hexdigest())
    retained = decode(artifact["report"])
    if canonical(artifact) != data:
        raise ValueError("noncanonical capture bytes")
    recomputed = analyze()
    require_equal(retained, recomputed)
    _stable_inputs(snapshot, freeze_path, freeze_data)
    if read_bounded(path) != data:
        raise ValueError("capture changed during replay")
    return recomputed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_mutually_exclusive_group(required=True)
    actions.add_argument("--freeze", type=Path)
    actions.add_argument("--capture", type=Path)
    actions.add_argument("--replay", type=Path)
    options = parser.parse_args()
    started = time.monotonic()
    if options.freeze is not None:
        result = freeze(options.freeze)
        print(json.dumps({"action": "freeze", "sources": len(result["sources"])}))
        return
    result = capture(options.capture) if options.capture is not None else replay(options.replay)
    data = canonical(encode(result))
    print(
        json.dumps(
            {
                "action": "capture" if options.capture is not None else "replay",
                "worlds": len(result["worlds"]),
                "membership": sum(len(w["membership"]) for w in result["worlds"]),
                "cq": sum(len(w["cq"]) for w in result["worlds"]),
                "report_bytes": len(data),
                "report_sha256": hashlib.sha256(data).hexdigest(),
                "seconds": round(time.monotonic() - started, 6),
            }
        )
    )


if __name__ == "__main__":
    main()
