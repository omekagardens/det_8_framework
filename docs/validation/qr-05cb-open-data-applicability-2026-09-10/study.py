"""QR-05CB open-data applicability driver.

Loads the fixed protocol, runs the independent primary and reference routes,
compares them, and (in ``main``) writes the create-only capture and source
freeze. No randomness, no floats, no network.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import sys
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
SOURCE_PATHS = ("README.md", "protocol.json", "primary.py", "reference.py", "study.py", "test_qr05cb.py")
DATA_PATHS = ("data/VBI_Coincidence_20230707.dat",)
CAPTURE_SCHEMA = "qr05cb-capture-v1"
FREEZE_SCHEMA = "qr05cb-source-freeze-v1"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    with mock.patch.dict(sys.modules, {spec.name: module}):
        spec.loader.exec_module(module)
    return module


def load_protocol():
    return json.loads((HERE / "protocol.json").read_bytes())


def encode(obj):
    if obj is None or isinstance(obj, (bool, int, str)):
        return obj
    if isinstance(obj, dict):
        return {key: encode(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(value) for value in obj]
    numerator = getattr(obj, "numerator", None)
    denominator = getattr(obj, "denominator", None)
    if isinstance(numerator, int) and isinstance(denominator, int):
        return [numerator, denominator]
    raise TypeError(type(obj))


def analyze_native():
    protocol = load_protocol()
    primary = load_module("_qr05cb_primary", HERE / "primary.py")
    reference = load_module("_qr05cb_reference", HERE / "reference.py")
    left = primary.build_report(protocol)
    right = reference.build_report(protocol)
    if encode(left) != encode(right):
        raise AssertionError("primary/reference report mismatch")
    return protocol, left, right


def analyze():
    return encode(analyze_native()[1])


def freeze():
    sources = {}
    for name in SOURCE_PATHS + DATA_PATHS:
        data = (HERE / name).read_bytes()
        sources[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    return {"schema": FREEZE_SCHEMA, "sources": sources}


def _write_create_only(path, payload):
    data = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8") + b"\n"
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path.name}")
    path.write_bytes(data)


def main(argv=None):
    parser = argparse.ArgumentParser(description="QR-05CB open-data applicability run")
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args(argv)
    if not (args.freeze or args.run):
        args.freeze = args.run = True

    protocol = load_protocol()
    for name in SOURCE_PATHS:
        if (HERE / name).stat().st_size > protocol["limits"]["source_bytes"]:
            raise ValueError(f"{name} exceeds source byte limit")
    if args.freeze:
        _write_create_only(HERE / "source-freeze.json", freeze())
    if args.run:
        _write_create_only(
            HERE / "results.json",
            {"schema": CAPTURE_SCHEMA,
             "runtime": {"implementation": platform.python_implementation(),
                         "version": platform.python_version()},
             "report": analyze()},
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
