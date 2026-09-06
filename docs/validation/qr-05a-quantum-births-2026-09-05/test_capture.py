"""Small lifecycle checks; temporary reports use a stub suite, never real evidence."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def runner(tmp_path, monkeypatch):
    path = Path(__file__).resolve().with_name("study.py")
    spec = importlib.util.spec_from_file_location("_qr05a_capture_lifecycle_test", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "RESULT", tmp_path / "report.json")
    monkeypatch.setattr(module, "ledger", lambda: {"source": {"sha256": "fixed"}})
    monkeypatch.setattr(module, "priors", lambda: {"prior": {"sha256": "fixed"}})
    monkeypatch.setattr(module, "run_suite", lambda: {"totals": {"stub": 1}, "exact": "3/5"})
    monkeypatch.setattr(module.platform, "platform", lambda: "lifecycle-test-platform")
    monkeypatch.setattr(sys, "argv", [str(path)])
    monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=1, optimize=0))
    monkeypatch.setattr(sys, "pycache_prefix", str(tmp_path / "external_cache"))
    return module


def test_capture_is_create_only_and_replay_is_byte_preserving(runner, monkeypatch):
    runner.main()
    first = runner.RESULT.read_bytes()
    with pytest.raises(FileExistsError):
        runner.main()
    assert runner.RESULT.read_bytes() == first
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    runner.main()
    assert runner.RESULT.read_bytes() == first


@pytest.mark.parametrize("field", ["schema_version", "source_ledger", "prior_artifacts", "suite"])
def test_replay_rejects_changed_evidence_without_repair(runner, monkeypatch, field):
    runner.main()
    content = json.loads(runner.RESULT.read_bytes())
    content[field] = {"changed": True}
    changed = runner.canonical(content)
    runner.RESULT.write_bytes(changed)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == changed


def test_capture_rejects_source_change_during_execution(runner, monkeypatch):
    def changing_suite():
        monkeypatch.setattr(runner, "ledger", lambda: {"different_source": {}})
        return {"totals": {}}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    with pytest.raises(ValueError, match="changed during"):
        runner.main()
    assert not runner.RESULT.exists()


def test_replay_rejects_result_change_during_execution(runner, monkeypatch):
    runner.main()

    def changing_suite():
        runner.RESULT.write_bytes(b"changed concurrently")
        return {"totals": {"stub": 1}, "exact": "3/5"}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError, match="result changed"):
        runner.main()
    assert runner.RESULT.read_bytes() == b"changed concurrently"


def test_capture_rejects_symlink_target_without_following(runner):
    target = runner.RESULT.with_name("untouched")
    target.write_bytes(b"original")
    runner.RESULT.symlink_to(target)
    with pytest.raises(FileExistsError):
        runner.main()
    assert target.read_bytes() == b"original"


def test_replay_rejects_symlink(runner, monkeypatch):
    runner.main()
    target = runner.RESULT.with_name("retained")
    runner.RESULT.rename(target)
    runner.RESULT.symlink_to(target)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError, match="plain file"):
        runner.main()


@pytest.mark.parametrize("failure", ["not_isolated", "no_cache", "root_cache", "checkout_cache"])
def test_runtime_boundary_rejects_before_capture(runner, monkeypatch, failure):
    if failure == "not_isolated":
        monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=0, optimize=0))
    elif failure == "no_cache":
        monkeypatch.setattr(sys, "pycache_prefix", None)
    elif failure == "root_cache":
        monkeypatch.setattr(sys, "pycache_prefix", runner.ROOT.anchor)
    else:
        monkeypatch.setattr(sys, "pycache_prefix", str(runner.ROOT / "local_cache"))
    with pytest.raises(ValueError):
        runner.main()
    assert not runner.RESULT.exists()
