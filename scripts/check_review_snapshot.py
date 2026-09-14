#!/usr/bin/env python3
"""Compare an explicit review manifest with bounded reads of local files.

This does not execute artifacts, authenticate the manifest or its checkpoint,
or certify a complete repository snapshot. Reads are not an atomic capture or
a filesystem sandbox: callers must keep the manifest and source files stable.
Only JSON is written to stdout; no files, caches, or git state are modified.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


MAX_FILE_BYTES = 1_000_000
DEFAULT_MANIFEST = "docs/coordination/review_snapshot.json"


def _error_text(error: Exception) -> str:
    message = str(error)
    return message if len(message) <= 240 else message[:237] + "..."


def _canonical_path(value: object) -> str:
    if (
        type(value) is not str
        or not value
        or "\\" in value
        or "\x00" in value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        raise ValueError("path must be a canonical POSIX relative file path")
    return value


def _exact_keys(value: object, keys: set[str], label: str) -> None:
    if type(value) is not dict or set(value) != keys:
        raise ValueError(f"{label} must have exactly these fields: {', '.join(sorted(keys))}")


def _hex_digest(value: object, length: int, label: str) -> None:
    if type(value) is not str or re.fullmatch(rf"[0-9a-f]{{{length}}}", value) is None:
        raise ValueError(f"{label} must be {length} lowercase hexadecimal characters")


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"invalid JSON constant: {value}")


def _validate_manifest(data: object) -> dict:
    """Finish all lexical/schema checks before any artifact is opened."""
    _exact_keys(data, {"schema_version", "checkpoint", "artifacts"}, "manifest")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("schema_version must be integer 1")
    checkpoint = data["checkpoint"]
    _exact_keys(checkpoint, {"commit", "tree"}, "checkpoint")
    for key in ("commit", "tree"):
        _hex_digest(checkpoint[key], 40, f"checkpoint {key}")
    artifacts = data["artifacts"]
    if type(artifacts) is not list or not artifacts:
        raise ValueError("artifacts must be a nonempty list")
    seen = set()
    for artifact in artifacts:
        _exact_keys(artifact, {"path", "sha256"}, "artifact")
        path = _canonical_path(artifact["path"])
        if path in seen:
            raise ValueError(f"duplicate artifact path: {path}")
        seen.add(path)
        _hex_digest(artifact["sha256"], 64, f"artifact sha256 for {path}")
    return data


def _read_file(root: Path, name: str) -> bytes:
    """Refuse symlink components and nonregular files; enforce the byte cap."""
    current = root
    parts = name.split("/")
    for index, part in enumerate(parts):
        current = current / part
        mode = current.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError("symlink components are not allowed")
        if index < len(parts) - 1:
            if not stat.S_ISDIR(mode):
                raise ValueError("intermediate path component is not a directory")
        elif not stat.S_ISREG(mode):
            raise ValueError("path is not a regular file")

    # These flags also refuse a changed final symlink or avoid blocking on a
    # changed FIFO where supported. Ancestor checks are still not atomic.
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    descriptor = os.open(current, flags)
    try:
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("opened path is not a regular file")
        if info.st_size > MAX_FILE_BYTES:
            raise ValueError(f"file exceeds {MAX_FILE_BYTES}-byte limit")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            data = stream.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES:
            raise ValueError(f"file exceeds {MAX_FILE_BYTES}-byte limit")
        return data
    finally:
        os.close(descriptor)


def check_snapshot(
    root: Path, manifest_name: str = DEFAULT_MANIFEST
) -> tuple[dict, int]:
    """Return a JSON-compatible report and exit code without writing files.

    The supplied root may be an alias; checks use its resolved directory.
    Every path component below that boundary must be free of symlinks.
    Checkpoint identities are echoed declarations, not independently checked.
    """
    try:
        resolved_root = Path(root).resolve(strict=True)
        if not resolved_root.is_dir():
            raise ValueError("root must resolve to an existing directory")
        manifest_name = _canonical_path(manifest_name)
        raw_manifest = _read_file(resolved_root, manifest_name)
        manifest = _validate_manifest(
            json.loads(
                raw_manifest.decode("utf-8"),
                object_pairs_hook=_unique_object,
                parse_constant=_reject_constant,
            )
        )
    except (OSError, ValueError, TypeError, RuntimeError) as error:
        return {"status": "invalid", "error": _error_text(error), "executed_files": 0}, 2

    files = []
    checked = 0
    matched = 0
    for artifact in manifest["artifacts"]:
        row = {
            "path": artifact["path"],
            "status": "unreadable",
            "expected_sha256": artifact["sha256"],
            "actual_sha256": None,
        }
        try:
            actual = hashlib.sha256(_read_file(resolved_root, artifact["path"])).hexdigest()
        except (OSError, ValueError) as error:
            row["error"] = _error_text(error)
        else:
            checked += 1
            row["actual_sha256"] = actual
            row["status"] = "match" if actual == artifact["sha256"] else "mismatch"
            matched += int(row["status"] == "match")
        files.append(row)
    complete = matched == len(files)
    return {
        "status": "match" if complete else "mismatch",
        "checkpoint": dict(manifest["checkpoint"]),
        "manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
        "declared_files": len(files),
        "checked_files": checked,
        "matched_files": matched,
        "files": files,
        "executed_files": 0,
    }, 0 if complete else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST)
    args = parser.parse_args(argv)
    report, exit_code = check_snapshot(args.root, args.manifest)
    print(json.dumps(report, sort_keys=True, allow_nan=False))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
