"""Regression tests for exact JSON-native evidence and the version-two driver.

The real aggregate suite is executed once, read-only.  Lifecycle tests instead
use temporary destinations and stub suites; no frozen v1 artifact is rewritten.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
V1_SHA = "ea3404f9401573c833965fc259b0f01dc28e3e3968ef79b4b3438e6535cd1238"


@pytest.fixture(scope="session", autouse=True)
def preserved_v1():
    path = HERE / "results.json"
    raw = path.read_bytes()
    assert len(raw) == 2523350
    assert hashlib.sha256(raw).hexdigest() == V1_SHA
    report = json.loads(raw)
    before = {name: (HERE / name).read_bytes() for name in report["source_ledger"]}
    for name, content in before.items():
        assert hashlib.sha256(content).hexdigest() == report["source_ledger"][name]["sha256"]
    yield report
    assert path.read_bytes() == raw
    assert all((HERE / name).read_bytes() == content for name, content in before.items())


@pytest.fixture(scope="session")
def v2():
    name = "_qr05d_v2_capture_regression"
    if name in sys.modules:
        raise RuntimeError("test-private runner namespace already occupied")
    spec = importlib.util.spec_from_file_location(name, HERE / "study_v2.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("version-two runner unavailable")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="session")
def real_suite(v2):
    # A corrected runner must not reuse v1's private executor module names.
    markers = {"qr05d_capture_direct": object(), "qr05d_capture_reference": object()}
    with pytest.MonkeyPatch.context() as patch:
        for name, marker in markers.items():
            patch.setitem(sys.modules, name, marker)
        suite = v2.run_suite()
        assert all(sys.modules[name] is marker for name, marker in markers.items())
    return suite


VALID_WIRE = [
    None,
    True,
    False,
    0,
    -17,
    1 << 128,
    "",
    "1/12",
    [],
    {},
    {"controls": {"collision": {"interior_orders": [{"relation": [[0, 1], [0, 0]]}, {}]}}},
    {"values": [None, True, False, 0, "phase", {"nested": []}]},
]


@pytest.mark.parametrize("value", VALID_WIRE)
def test_require_wire_accepts_native_exact_json_types(v2, value):
    v2.require_wire(value)
    assert json.loads(json.dumps(value, allow_nan=False)) == value


BAD_WIRE = [
    (),
    (1, 2),
    0.0,
    0.5,
    float("inf"),
    float("nan"),
    Fraction(1, 2),
    b"exact",
    {1, 2},
    {1: "integer key"},
    {False: "boolean key"},
    {None: "null key"},
    {"controls": {"collision": {"interior_orders": ({"order": []}, {"order": []})}}},
    {"nested": [0, {"coefficient": 0.5}]},
    {"nested": [{"row": {0: "converted key"}}]},
]


@pytest.mark.parametrize("value", BAD_WIRE)
def test_require_wire_rejects_coercible_and_nested_non_native_values(v2, value):
    with pytest.raises(ValueError):
        v2.require_wire(value)


@pytest.mark.parametrize("left,right", ((True, 1), (1, True), (False, 0), (0, False)))
@pytest.mark.parametrize("nested", (False, True))
def test_same_wire_distinguishes_native_boolean_and_integer_types(v2, left, right, nested):
    if nested:
        left, right = ({"outer": [{"value": value}]} for value in (left, right))
    v2.require_wire(left)
    v2.require_wire(right)
    assert left == right  # Python equality conceals the exact-wire discrepancy.
    assert json.dumps(left, sort_keys=True) != json.dumps(right, sort_keys=True)
    with pytest.raises(ValueError, match="typed wire differs"):
        v2.require_same_wire(left, right, "typed wire differs")


def test_same_wire_accepts_exact_values_with_different_dictionary_insertion_order(v2):
    left = {"a": [True, 1, None], "b": {"x": False, "y": 0}}
    right = {"b": {"y": 0, "x": False}, "a": [True, 1, None]}
    v2.require_same_wire(left, right, "equivalent wire was rejected")


@pytest.mark.parametrize("invalid_left", (False, True))
def test_same_wire_checks_both_trees_before_implicit_json_conversion(v2, invalid_left):
    native = {"items": [1, 2]}
    nonnative = {"items": (1, 2)}
    left, right = (nonnative, native) if invalid_left else (native, nonnative)
    assert v2.canonical(left) == v2.canonical(right)
    with pytest.raises(ValueError):
        v2.require_same_wire(left, right, "tuple was coerced")


def test_real_aggregate_suite_has_an_exact_json_round_trip(v2, real_suite):
    v2.require_wire(real_suite)
    decoded = json.loads(v2.canonical(real_suite))
    assert decoded == real_suite
    assert type(real_suite["controls"]["collision"]["interior_orders"]) is list


def test_real_v2_suite_preserves_every_saved_v1_mathematical_value(real_suite, preserved_v1):
    assert real_suite == preserved_v1["suite"]
    assert json.dumps(real_suite, sort_keys=True, allow_nan=False) == json.dumps(
        preserved_v1["suite"], sort_keys=True, allow_nan=False
    )


def test_original_tuple_regression_is_rejected_even_when_json_bytes_match(v2, real_suite):
    collision = dict(real_suite["controls"]["collision"])
    collision["interior_orders"] = tuple(collision["interior_orders"])
    controls = {**real_suite["controls"], "collision": collision}
    broken = {**real_suite, "controls": controls}
    assert broken != real_suite
    assert v2.canonical(broken) == v2.canonical(real_suite)
    with pytest.raises(ValueError):
        v2.require_wire(broken)


def test_v2_has_new_destination_schema_and_pins_v1(v2, preserved_v1):
    assert v2.RESULT == HERE / "results-v2.json"
    assert v2.SCHEMA == "det8-qr05d-results-v2"
    assert len(v2.SOURCES) == 9
    assert set(v2.SOURCES) == set(preserved_v1["source_ledger"]) | {
        "REVISION_V2.md",
        "study_v2.py",
        "test_capture_v2.py",
    }
    assert len(v2.PRIORS) == 8
    assert v2.PRIORS[HERE.name] == V1_SHA


@pytest.fixture
def runner(v2, tmp_path, monkeypatch):
    monkeypatch.setattr(v2, "RESULT", tmp_path / "results-v2.json")
    monkeypatch.setattr(v2, "ledger", lambda: {"source": {"sha256": "fixed"}})
    monkeypatch.setattr(v2, "priors", lambda: {"prior": {"sha256": "fixed"}})
    monkeypatch.setattr(v2, "run_suite", lambda: {"totals": {"stub": 1}, "exact": [None, "1/2", 3]})
    monkeypatch.setattr(v2.platform, "platform", lambda: "v2-lifecycle-test-platform")
    monkeypatch.setattr(sys, "argv", ["study_v2.py"])
    monkeypatch.setattr(sys, "flags", SimpleNamespace(isolated=1, optimize=0))
    monkeypatch.setattr(sys, "pycache_prefix", str(tmp_path / "cache"))
    return v2


def test_v2_create_only_capture_and_read_only_replay(runner, monkeypatch):
    runner.main()
    raw = runner.RESULT.read_bytes()
    assert json.loads(raw)["schema_version"] == "det8-qr05d-results-v2"
    with pytest.raises(FileExistsError):
        runner.main()
    assert runner.RESULT.read_bytes() == raw
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    runner.main()
    assert runner.RESULT.read_bytes() == raw


@pytest.mark.parametrize("saved,fresh", ((True, 1), (1, True), (False, 0), (0, False)))
def test_replay_rejects_boolean_integer_substitution_and_preserves_artifact(
    runner, monkeypatch, saved, fresh
):
    original = {"totals": {"stub": 1}, "nested": [{"value": saved}]}
    changed = {"totals": {"stub": 1}, "nested": [{"value": fresh}]}
    runner.require_wire(original)
    runner.require_wire(changed)
    assert original == changed
    monkeypatch.setattr(runner, "run_suite", lambda: original)
    runner.main()
    raw = runner.RESULT.read_bytes()
    retained = json.loads(raw)["suite"]["nested"][0]["value"]
    assert type(retained) is type(saved)
    monkeypatch.setattr(runner, "run_suite", lambda: changed)
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    with pytest.raises(ValueError, match="exact replay differs"):
        runner.main()
    assert runner.RESULT.read_bytes() == raw


@pytest.mark.parametrize(
    "bad",
    (
        {"totals": {}, "tuple": ({}, {})},
        {"totals": {}, "float": 0.5},
        {"totals": {}, "bad_key": {0: "zero"}},
    ),
)
def test_non_native_suite_fails_before_capture_or_serialization(runner, monkeypatch, bad):
    monkeypatch.setattr(runner, "run_suite", lambda: bad)

    def serialization_must_not_run(_value):
        raise RuntimeError("bad suite reached serialization")

    monkeypatch.setattr(runner, "canonical", serialization_must_not_run)
    with pytest.raises(ValueError):
        runner.main()
    assert not runner.RESULT.exists()


def test_bad_replay_suite_does_not_rewrite_captured_data(runner, monkeypatch):
    runner.main()
    raw = runner.RESULT.read_bytes()
    monkeypatch.setattr(runner, "run_suite", lambda: {"totals": {}, "nested": [({"x": 1},)]})
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == raw


@pytest.mark.parametrize("field", ("schema_version", "source_ledger", "prior_artifacts", "suite"))
def test_v2_replay_rejects_changed_retained_evidence(runner, monkeypatch, field):
    runner.main()
    report = json.loads(runner.RESULT.read_bytes())
    report[field] = "changed"
    altered = runner.canonical(report)
    runner.RESULT.write_bytes(altered)
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == altered


@pytest.mark.parametrize("kind", ("noncanonical", "extra_field", "wrong_type"))
def test_v2_replay_requires_exact_envelope(runner, monkeypatch, kind):
    runner.main()
    raw = runner.RESULT.read_bytes()
    report = json.loads(raw)
    if kind == "noncanonical":
        changed = b" " + raw
    elif kind == "extra_field":
        changed = runner.canonical({**report, "extra": None})
    else:
        changed = runner.canonical([])
    runner.RESULT.write_bytes(changed)
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    with pytest.raises(ValueError):
        runner.main()
    assert runner.RESULT.read_bytes() == changed


@pytest.mark.parametrize("during", ("sources", "priors"))
def test_v2_capture_rejects_identity_change_midrun(runner, monkeypatch, during):
    def changing_suite():
        monkeypatch.setattr(
            runner, "ledger" if during == "sources" else "priors", lambda: {"changed": {}}
        )
        return {"totals": {"stub": 1}}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    with pytest.raises(ValueError, match="changed during"):
        runner.main()
    assert not runner.RESULT.exists()


def test_v2_replay_detects_midrun_artifact_change(runner, monkeypatch):
    runner.main()

    def changing_suite():
        runner.RESULT.write_bytes(b"concurrent change")
        return {"totals": {"stub": 1}, "exact": [None, "1/2", 3]}

    monkeypatch.setattr(runner, "run_suite", changing_suite)
    monkeypatch.setattr(sys, "argv", ["study_v2.py", "--verify"])
    with pytest.raises(ValueError, match="result changed"):
        runner.main()
    assert runner.RESULT.read_bytes() == b"concurrent change"


@pytest.mark.parametrize("verify", (False, True))
def test_v2_does_not_follow_result_symlink(runner, monkeypatch, verify):
    target = runner.RESULT.with_name("untouched.json")
    target.write_bytes(b"unchanged")
    runner.RESULT.symlink_to(target)
    monkeypatch.setattr(sys, "argv", ["study_v2.py", *(["--verify"] if verify else [])])
    with pytest.raises(ValueError if verify else FileExistsError):
        runner.main()
    assert target.read_bytes() == b"unchanged"


@pytest.mark.parametrize("kind", ("not_isolated", "no_cache", "root_cache", "checkout_cache"))
def test_v2_enforces_runtime_boundaries(runner, monkeypatch, kind):
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
