"""Capture lifecycle checks use only temporary stub evidence, not real results."""

from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from types import SimpleNamespace

import pytest


@pytest.fixture
def runner(tmp_path, monkeypatch):
    path = Path(__file__).resolve().with_name("study.py")
    spec = importlib.util.spec_from_file_location("qr05g_lifecycle", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "RESULT", tmp_path / "report.json")
    monkeypatch.setattr(module, "ledger", lambda: {"source": {"sha256": "fixed"}})
    monkeypatch.setattr(module, "priors", lambda: {"prior": {"sha256": "fixed"}})
    monkeypatch.setattr(module, "run_suite", lambda: {"totals": {"stub": 1}})
    monkeypatch.setattr(module.platform, "platform", lambda: "lifecycle-test-platform")
    monkeypatch.setattr(sys, "argv", [str(path)])
    monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=1, optimize=0))
    monkeypatch.setattr(sys, "pycache_prefix", str(tmp_path / "cache"))
    return module


def test_create_only_and_unchanged_replay(runner, monkeypatch):
    runner.main()
    raw = runner.RESULT.read_bytes()
    with pytest.raises(FileExistsError):
        runner.main()
    assert runner.RESULT.read_bytes() == raw
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    runner.main()
    assert runner.RESULT.read_bytes() == raw


@pytest.mark.parametrize("field", ["schema_version", "source_ledger", "prior_artifacts", "suite"])
def test_replay_rejects_changed_evidence(runner, monkeypatch, field):
    runner.main()
    value = json.loads(runner.RESULT.read_bytes())
    value[field] = "altered"
    changed = runner.canonical(value)
    runner.RESULT.write_bytes(changed)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == changed


@pytest.mark.parametrize("kind", ["noncanonical", "extra_field", "wrong_type"])
def test_replay_requires_canonical_known_envelope(runner, monkeypatch, kind):
    runner.main()
    raw = runner.RESULT.read_bytes()
    value = json.loads(raw)
    if kind == "noncanonical":
        changed = b" " + raw
    elif kind == "extra_field":
        value["unknown"] = 1
        changed = runner.canonical(value)
    else:
        changed = runner.canonical([])
    runner.RESULT.write_bytes(changed)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == changed


@pytest.mark.parametrize("during", ["sources", "priors"])
def test_capture_rejects_midrun_identity_change(runner, monkeypatch, during):
    def changing_suite():
        monkeypatch.setattr(
            runner, "ledger" if during == "sources" else "priors", lambda: {"changed": {}}
        )
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    with pytest.raises(ValueError, match="changed during"):
        runner.main()
    assert not runner.RESULT.exists()


def test_replay_catches_midrun_artifact_change(runner, monkeypatch):
    runner.main()

    def changing_suite():
        runner.RESULT.write_bytes(b"concurrent change")
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError, match="result changed"):
        runner.main()
    assert runner.RESULT.read_bytes() == b"concurrent change"


@pytest.mark.parametrize("verify", [False, True])
def test_result_symlink_not_followed(runner, monkeypatch, verify):
    target = runner.RESULT.with_name("untouched.json")
    target.write_bytes(b"original")
    runner.RESULT.symlink_to(target)
    monkeypatch.setattr(sys, "argv", ["study.py", *(["--verify"] if verify else [])])
    with pytest.raises(ValueError if verify else FileExistsError):
        runner.main()
    assert target.read_bytes() == b"original"


@pytest.mark.parametrize("kind", ["not_isolated", "no_cache", "root_cache", "checkout_cache"])
def test_runtime_boundary(runner, monkeypatch, kind):
    if kind == "not_isolated":
        monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=0, optimize=0))
    elif kind == "no_cache":
        monkeypatch.setattr(sys, "pycache_prefix", None)
    elif kind == "root_cache":
        monkeypatch.setattr(sys, "pycache_prefix", runner.ROOT.anchor)
    else:
        monkeypatch.setattr(sys, "pycache_prefix", str(runner.ROOT / "local_cache"))
    with pytest.raises(ValueError):
        runner.main()
    assert not runner.RESULT.exists()


def test_plain_input_rejects_symlink(runner, tmp_path):
    source = tmp_path / "source.json"
    source.write_bytes(b"{}")
    link = tmp_path / "link.json"
    link.symlink_to(source)
    with pytest.raises(ValueError, match="plain file"):
        runner.plain_bytes(link)
    assert source.read_bytes() == b"{}"


def test_prior_json_rejects_changed_digest(runner, monkeypatch, tmp_path):
    prior = tmp_path / "prior"
    prior.mkdir()
    artifact = prior / "results.json"
    artifact.write_bytes(b"{}")
    monkeypatch.setattr(runner, "HERE", tmp_path / "study")
    monkeypatch.setattr(runner, "PRIORS", {"prior/results.json": "0" * 64})
    with pytest.raises(ValueError, match="prior artifact changed"):
        runner.prior_json("prior/results.json")
    assert artifact.read_bytes() == b"{}"


def test_retained_component_count_includes_integers(runner):
    assert runner.retained_bits([{"rational": "1/16", "count": 1 << 10}]) == 11
    assert runner.retained_bits([True, None, "mesh5"]) == 0


@pytest.mark.parametrize("value", [(1, 2), F(1, 2), 1.0, {"nested": (1,)}, {1: "key"}])
def test_exact_wire_rejects_coercions(runner, value):
    with pytest.raises(ValueError):
        runner.require_wire(value)


@pytest.mark.parametrize(
    "left,right",
    [
        (True, 1),
        (False, 0),
        ({"nested": [True]}, {"nested": [1]}),
        ({"nested": ["1"]}, {"nested": [1]}),
    ],
)
def test_exact_comparison_distinguishes_native_types(runner, left, right):
    with pytest.raises(ValueError):
        runner.require_same_wire(left, right, "different wire")


def test_native_wire_round_trip(runner):
    value = {"x": [None, True, False, 1, -2, "1/2", {"v": []}]}
    runner.require_same_wire(value, json.loads(runner.canonical(value)), "round trip")


@pytest.mark.parametrize("value", [{"totals": (1,)}, {"totals": {"value": F(1, 2)}}])
def test_capture_rejects_non_native_suite_before_write(runner, monkeypatch, value):
    monkeypatch.setattr(runner, "run_suite", lambda: value)
    with pytest.raises(ValueError):
        runner.main()
    assert not runner.RESULT.exists()


def test_replay_rejects_boolean_integer_substitution(runner, monkeypatch):
    runner.main()
    value = json.loads(runner.RESULT.read_bytes())
    value["suite"]["totals"]["stub"] = True
    changed = runner.canonical(value)
    runner.RESULT.write_bytes(changed)
    monkeypatch.setattr(sys, "argv", ["study.py", "--verify"])
    with pytest.raises(ValueError, match="exact replay"):
        runner.main()
    assert runner.RESULT.read_bytes() == changed
