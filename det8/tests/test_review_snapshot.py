"""Independent byte-integrity and refusal contracts; no real snapshot is consulted."""

import builtins
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

CHECKER = Path(__file__).resolve().parents[2] / "scripts/check_review_snapshot.py"
MANIFEST = "docs/coordination/review_snapshot.json"
LIMIT = 1_000_000
CHECKPOINT = {"commit": "0123456789abcdef" * 2 + "01234567", "tree": "f" * 40}


def digest(data):
    return hashlib.sha256(data).hexdigest()


@pytest.fixture(scope="module")
def checker():
    spec = importlib.util.spec_from_file_location("review_snapshot_under_test", CHECKER)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def save(root, document, name=MANIFEST):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(document, ensure_ascii=False, indent=2).encode() + b"\n"
    path.write_bytes(data)
    return data


def fixture_snapshot(root, files=None):
    root.mkdir(parents=True, exist_ok=True)
    if files is None:
        files = {
            "notes/space \u00fc.md": b"A supplied mathematical statement.\n",
            "raw.bin": b"\x00\xff\r\n",
        }
    rows = []
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        rows.append({"path": name, "sha256": digest(data)})
    document = {"schema_version": 1, "checkpoint": CHECKPOINT.copy(), "artifacts": rows}
    save(root, document)
    return document


def assert_invalid(report, code):
    assert code == 2
    assert report["status"] == "invalid"
    assert report["executed_files"] == 0
    assert isinstance(report["error"], str) and report["error"]


def guard_opens(monkeypatch, basename, action):
    """Observe ordinary file APIs without depending on the checker's reader helper."""
    for owner, attribute in ((builtins, "open"), (io, "open"), (os, "open")):
        original = getattr(owner, attribute)

        def guarded(file, *args, _original=original, **kwargs):
            if (
                isinstance(file, (str, bytes, os.PathLike))
                and Path(os.fsdecode(file)).name == basename
            ):
                action()
            return _original(file, *args, **kwargs)

        monkeypatch.setattr(owner, attribute, guarded)


def test_matching_snapshot_binds_exact_manifest_bytes_and_counts(checker, tmp_path):
    document = fixture_snapshot(tmp_path)
    raw = (tmp_path / MANIFEST).read_bytes()
    report, code = checker.check_snapshot(tmp_path, MANIFEST)
    assert code == 0 and report["status"] == "match"
    assert report["manifest_sha256"] == digest(raw)
    assert report["checkpoint"] == CHECKPOINT
    assert report["declared_files"] == report["checked_files"] == report["matched_files"] == 2
    assert report["executed_files"] == 0
    assert report["files"] == [
        {
            "path": item["path"],
            "status": "match",
            "expected_sha256": item["sha256"],
            "actual_sha256": digest((tmp_path / item["path"]).read_bytes()),
        }
        for item in document["artifacts"]
    ]


def test_real_tamper_and_missing_file_have_distinct_counts(checker, tmp_path):
    document = fixture_snapshot(tmp_path, {"tampered": b"before", "missing": b"lost", "ok": b""})
    (tmp_path / "tampered").write_bytes(b"after")
    (tmp_path / "missing").unlink()
    report, code = checker.check_snapshot(tmp_path, MANIFEST)
    assert code == 1 and report["status"] == "mismatch"
    assert (report["declared_files"], report["checked_files"], report["matched_files"]) == (3, 2, 1)
    rows = {row["path"]: row for row in report["files"]}
    assert rows["tampered"] == {
        "path": "tampered",
        "status": "mismatch",
        "expected_sha256": document["artifacts"][0]["sha256"],
        "actual_sha256": digest(b"after"),
    }
    assert rows["missing"]["status"] == "unreadable"
    assert rows["missing"]["actual_sha256"] is None
    assert rows["missing"]["error"]
    assert rows["ok"]["status"] == "match"
    assert report["executed_files"] == 0


@pytest.mark.parametrize(
    ("location", "value"),
    [
        (("schema_version",), True),
        (("schema_version",), 1.0),
        (("schema_version",), 2),
        (("schema_version",), "1"),
        (("checkpoint",), None),
        (("checkpoint", "commit"), "A" * 40),
        (("checkpoint", "commit"), "a" * 39),
        (("checkpoint", "commit"), "a" * 41),
        (("checkpoint", "tree"), "g" * 40),
        (("checkpoint", "tree"), False),
        (("artifacts",), []),
        (("artifacts",), {}),
        (("artifacts",), None),
        (("artifacts", 0), "not an object"),
        (("artifacts", 0, "path"), None),
        (("artifacts", 0, "path"), True),
        (("artifacts", 0, "sha256"), "A" * 64),
        (("artifacts", 0, "sha256"), "a" * 63),
        (("artifacts", 0, "sha256"), "a" * 65),
        (("artifacts", 0, "sha256"), "z" * 64),
        (("artifacts", 0, "sha256"), 0),
    ],
)
def test_malformed_field_values_refuse(checker, tmp_path, location, value):
    document = fixture_snapshot(tmp_path)
    parent = document
    for key in location[:-1]:
        parent = parent[key]
    parent[location[-1]] = value
    save(tmp_path, document)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


@pytest.mark.parametrize("level", ["top", "checkpoint", "artifact"])
@pytest.mark.parametrize("change", ["unknown", "missing"])
def test_exact_schema_rejects_unknown_and_missing_fields(checker, tmp_path, level, change):
    document = fixture_snapshot(tmp_path)
    target, required = {
        "top": (document, "schema_version"),
        "checkpoint": (document["checkpoint"], "tree"),
        "artifact": (document["artifacts"][0], "sha256"),
    }[level]
    if change == "unknown":
        target["unexpected"] = "must refuse"
    else:
        del target[required]
    save(tmp_path, document)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


@pytest.mark.parametrize(
    "payload",
    [
        b"[]",
        b"null",
        b"42",
        b'"text"',
        b"{",
        b"\xff",
        b"{} {}",
        pytest.param(b"[" * 2000 + b"0" + b"]" * 2000, id="deeply-nested"),
    ],
)
def test_invalid_json_or_top_level_refuses(checker, tmp_path, payload):
    fixture_snapshot(tmp_path)
    (tmp_path / MANIFEST).write_bytes(payload)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


@pytest.mark.parametrize("field", ["schema_version", "commit", "path", "sha256"])
def test_duplicate_json_keys_are_not_silently_overwritten(checker, tmp_path, field):
    document = fixture_snapshot(tmp_path)
    encoded = json.dumps(document)
    value = {
        "schema_version": 1,
        "commit": CHECKPOINT["commit"],
        "path": document["artifacts"][0]["path"],
        "sha256": document["artifacts"][0]["sha256"],
    }[field]
    # The second spelling has a JSON escape but decodes to the same key.
    escaped = f"\\u{ord(field[0]):04x}{field[1:]}"
    token = f"{json.dumps(field)}: {json.dumps(value)}"
    encoded = encoded.replace(token, token + f', "{escaped}": {json.dumps(value)}', 1)
    (tmp_path / MANIFEST).write_text(encoded)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


def test_duplicate_artifact_paths_refuse_even_with_different_digests(checker, tmp_path):
    document = fixture_snapshot(tmp_path)
    duplicate = copy.deepcopy(document["artifacts"][0])
    duplicate["sha256"] = "0" * 64
    document["artifacts"].append(duplicate)
    save(tmp_path, document)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


BAD_PATHS = [
    "",
    ".",
    "..",
    "../outside",
    "/absolute",
    "./raw.bin",
    "a/../b",
    "a/./b",
    "a//b",
    "a/",
    "a\\b",
    "a\x00b",
]


@pytest.mark.parametrize("path", BAD_PATHS)
@pytest.mark.parametrize("target", ["artifact", "manifest"])
def test_noncanonical_paths_refuse(checker, tmp_path, path, target):
    document = fixture_snapshot(tmp_path)
    if target == "artifact":
        document["artifacts"][0]["path"] = path
        save(tmp_path, document)
        path = MANIFEST
    assert_invalid(*checker.check_snapshot(tmp_path, path))


def test_entire_lexical_schema_is_checked_before_any_artifact_read(checker, tmp_path, monkeypatch):
    document = fixture_snapshot(tmp_path, {"must_not_be_read.py": b"first", "later": b"second"})
    document["artifacts"][1]["sha256"] = "not a digest"
    save(tmp_path, document)

    def forbidden():
        pytest.fail("An artifact was opened before the later malformed row was rejected")

    guard_opens(monkeypatch, "must_not_be_read.py", forbidden)
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


@pytest.mark.parametrize("kind", ["file", "directory"])
@pytest.mark.parametrize("target", ["artifact", "manifest"])
def test_symlink_components_refuse_even_when_target_bytes_match(checker, tmp_path, kind, target):
    root = tmp_path / "archive"
    document = fixture_snapshot(root, {"data/item": b"safe bytes"})
    relative = "data/item" if target == "artifact" else MANIFEST
    path = root / relative
    outside = tmp_path / "outside"
    if kind == "file":
        outside.write_bytes(path.read_bytes())
        path.unlink()
        path.symlink_to(outside)
    else:
        path.parent.rename(outside)
        path.parent.symlink_to(outside, target_is_directory=True)
    report, code = checker.check_snapshot(root, MANIFEST)
    if target == "manifest":
        assert_invalid(report, code)
    else:
        assert code == 1 and report["status"] == "mismatch"
        assert report["checked_files"] == report["matched_files"] == 0
        assert report["files"][0]["expected_sha256"] == document["artifacts"][0]["sha256"]
        assert report["files"][0]["actual_sha256"] is None
        assert report["files"][0]["status"] == "unreadable"


def test_root_alias_is_allowed_but_missing_or_regular_file_root_refuses(checker, tmp_path):
    root = tmp_path / "archive"
    fixture_snapshot(root)
    alias = tmp_path / "alias"
    alias.symlink_to(root, target_is_directory=True)
    report, code = checker.check_snapshot(alias, MANIFEST)
    assert code == 0 and report["status"] == "match"
    assert_invalid(*checker.check_snapshot(tmp_path / "missing", MANIFEST))
    assert_invalid(*checker.check_snapshot(root / "raw.bin", MANIFEST))


def test_missing_manifest_is_invalid_not_an_artifact_mismatch(checker, tmp_path):
    assert_invalid(*checker.check_snapshot(tmp_path, MANIFEST))


@pytest.mark.parametrize("manifest_name", [None, True, 123])
def test_manifest_argument_requires_a_string(checker, tmp_path, manifest_name):
    fixture_snapshot(tmp_path)
    assert_invalid(*checker.check_snapshot(tmp_path, manifest_name))


@pytest.mark.parametrize("target", ["artifact", "manifest"])
def test_regular_files_are_required(checker, tmp_path, target):
    fixture_snapshot(tmp_path, {"item": b"data"})
    path = tmp_path / ("item" if target == "artifact" else MANIFEST)
    path.unlink()
    path.mkdir()
    report, code = checker.check_snapshot(tmp_path, MANIFEST)
    if target == "manifest":
        assert_invalid(report, code)
    else:
        assert code == 1 and report["files"][0]["status"] == "unreadable"
        assert report["checked_files"] == 0


def test_unreadable_artifact_does_not_prevent_checking_other_rows(checker, tmp_path, monkeypatch):
    fixture_snapshot(tmp_path, {"blocked.bin": b"secret", "ok": b"available"})

    def denied():
        raise PermissionError("Synthetic permission refusal")

    guard_opens(monkeypatch, "blocked.bin", denied)
    report, code = checker.check_snapshot(tmp_path, MANIFEST)
    assert code == 1 and report["status"] == "mismatch"
    assert (report["declared_files"], report["checked_files"], report["matched_files"]) == (2, 1, 1)
    assert report["files"][0]["status"] == "unreadable"
    assert report["files"][0]["actual_sha256"] is None
    assert report["files"][0]["error"]
    assert report["files"][1]["status"] == "match"


@pytest.mark.parametrize("extra", [0, 1])
@pytest.mark.parametrize("target", ["artifact", "manifest"])
def test_decimal_byte_limit_has_an_exact_boundary(checker, tmp_path, target, extra):
    if target == "artifact":
        fixture_snapshot(tmp_path, {"large": b"x" * (LIMIT + extra)})
    else:
        fixture_snapshot(tmp_path)
        path = tmp_path / MANIFEST
        raw = path.read_bytes()
        path.write_bytes(raw + b" " * (LIMIT + extra - len(raw)))
    report, code = checker.check_snapshot(tmp_path, MANIFEST)
    if not extra:
        assert code == 0 and report["status"] == "match"
    elif target == "manifest":
        assert_invalid(report, code)
    else:
        assert code == 1 and report["files"][0]["status"] == "unreadable"
        assert report["checked_files"] == 0


def byte_tree(root):
    return {
        path.relative_to(root).as_posix(): path.read_bytes() if path.is_file() else None
        for path in root.rglob("*")
    }


@pytest.mark.parametrize("optimized", [False, True])
@pytest.mark.parametrize("case", ["match", "mismatch", "invalid"])
def test_archive_cli_is_isolated_read_only_and_never_executes_artifacts(tmp_path, optimized, case):
    root = tmp_path / "archive"
    marker = root / "EXECUTED"
    malicious = f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\nraise RuntimeError('artifact imported')\n".encode()
    document = fixture_snapshot(root, {"untrusted.py": malicious, "bytes.bin": b"\x00\xff"})
    script = root / "scripts/check_review_snapshot.py"
    script.parent.mkdir()
    script.write_bytes(CHECKER.read_bytes())
    if case == "mismatch":
        (root / "bytes.bin").write_bytes(b"changed")
    elif case == "invalid":
        document["schema_version"] = True
        save(root, document)
    before = byte_tree(root)
    elsewhere = tmp_path / "unrelated-cwd"
    elsewhere.mkdir()
    command = [sys.executable, "-I", "-S", "-B"]
    if optimized:
        command.append("-O")
    result = subprocess.run(
        command + [str(script), "--root", str(root)],
        cwd=elsewhere,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == {"match": 0, "mismatch": 1, "invalid": 2}[case]
    assert result.stderr == ""
    report = json.loads(result.stdout)
    assert report["status"] == case and report["executed_files"] == 0
    if case != "invalid":
        assert report["declared_files"] == report["checked_files"] == 2
        assert report["matched_files"] == (2 if case == "match" else 1)
    assert byte_tree(root) == before
    assert not marker.exists() and not (root / ".git").exists()
    assert not list(root.rglob("__pycache__"))
    assert list(elsewhere.iterdir()) == []


@pytest.mark.parametrize("arguments", [["--unknown"], ["--root"], ["--manifest"]])
def test_cli_argument_errors_are_stderr_exit_two(tmp_path, arguments):
    result = subprocess.run(
        [sys.executable, "-I", "-S", "-B", str(CHECKER), *arguments],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 2 and result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("optimized", [False, True])
def test_cli_uses_the_explicit_alternate_manifest(tmp_path, optimized):
    document = fixture_snapshot(tmp_path, {"one": b"known bytes"})
    alternate = "audit/pins.json"
    exact_bytes = save(tmp_path, document, alternate)
    (tmp_path / MANIFEST).write_bytes(b"the default is deliberately invalid")
    command = [sys.executable, "-I", "-S", "-B"]
    if optimized:
        command.append("-O")
    result = subprocess.run(
        command + [str(CHECKER), "--root", str(tmp_path), "--manifest", alternate],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )
    assert result.returncode == 0 and result.stderr == ""
    report = json.loads(result.stdout)
    assert report["status"] == "match"
    assert report["manifest_sha256"] == digest(exact_bytes)
    assert report["declared_files"] == report["checked_files"] == report["matched_files"] == 1
    assert report["executed_files"] == 0
