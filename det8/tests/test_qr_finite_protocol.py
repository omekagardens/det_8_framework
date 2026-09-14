"""Isolated source-binding contracts for the separate six-alias finite protocol."""

import hashlib
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from scripts import run_qr_finite_protocol as launcher

ROOT = Path(__file__).resolve().parents[2]
ALIASES = (
    "local_source",
    "joint_source",
    "local_joint_adapter",
    "terminal_read_source",
    "finite_protocol",
    "check",
)
PROTOCOL_FIXTURE = """import local_source
import joint_source
import local_joint_adapter
import terminal_read_source

def source_classes():
    return local_source.G, joint_source.G, terminal_read_source.G
"""
SMOKE = """import unittest
import local_source
import joint_source
import local_joint_adapter
import terminal_read_source
import finite_protocol
class Witness(unittest.TestCase):
    def test_aliases(self):
        self.assertIs(local_joint_adapter.c, local_source)
        self.assertIs(local_joint_adapter.d, joint_source)
        self.assertIs(finite_protocol.local_source, local_source)
        self.assertIs(finite_protocol.joint_source, joint_source)
        self.assertIs(finite_protocol.local_joint_adapter, local_joint_adapter)
        self.assertIs(finite_protocol.terminal_read_source, terminal_read_source)
        self.assertEqual(len(set(finite_protocol.source_classes())), 3)
if __name__ == '__main__':
    unittest.main()
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def fixed_fixture(tmp_path, monkeypatch, source=SMOKE):
    """Copy fixed real-layout inputs; only explicit fixture pins are replaceable."""
    # Keep refusal probes independent of protocol arithmetic. The four
    # dependencies are published bytes; protocol/check/statements are fixtures.
    for pin in launcher.SOURCE_BINDINGS:
        target = tmp_path / pin.path
        target.parent.mkdir(parents=True, exist_ok=True)
        if pin.alias == "finite_protocol":
            target.write_text(PROTOCOL_FIXTURE)
        elif pin.alias == "check":
            target.write_text(source)
        else:
            target.write_bytes((ROOT / pin.path).read_bytes())
    for index, pin in enumerate(launcher.STATEMENT_BINDINGS):
        target = tmp_path / pin.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"Synthetic statement fixture {index}\n")
    for name in (launcher.RUNNER_PATH, launcher.LAUNCHER_PATH):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    monkeypatch.setattr(
        launcher,
        "SOURCE_BINDINGS",
        tuple(
            replace(pin, sha256=digest((tmp_path / pin.path).read_bytes()))
            for pin in launcher.SOURCE_BINDINGS
        ),
    )
    monkeypatch.setattr(
        launcher,
        "STATEMENT_BINDINGS",
        tuple(
            replace(pin, sha256=digest((tmp_path / pin.path).read_bytes()))
            for pin in launcher.STATEMENT_BINDINGS
        ),
    )
    return tmp_path


def repin_fixture_source(root, monkeypatch, alias, text):
    pin = next(pin for pin in launcher.SOURCE_BINDINGS if pin.alias == alias)
    data = text.encode()
    (root / pin.path).write_bytes(data)
    monkeypatch.setattr(
        launcher,
        "SOURCE_BINDINGS",
        tuple(
            replace(item, sha256=digest(data)) if item.alias == alias else item
            for item in launcher.SOURCE_BINDINGS
        ),
    )


def test_all_reviewed_identities_are_fixed_before_inventory(monkeypatch):
    assert tuple(pin.alias for pin in launcher.SOURCE_BINDINGS) == ALIASES
    assert len({pin.path for pin in launcher.SOURCE_BINDINGS}) == 6
    assert len(launcher.STATEMENT_BINDINGS) == 6
    for pin in (*launcher.SOURCE_BINDINGS, *launcher.STATEMENT_BINDINGS):
        assert pin.sha256 != launcher._PENDING_SHA256
        assert digest((ROOT / pin.path).read_bytes()) == pin.sha256
    assert digest((ROOT / launcher.RUNNER_PATH).read_bytes()) == launcher.EXPECTED_RUNNER_SHA256
    with pytest.raises(FrozenInstanceError):
        launcher.SOURCE_BINDINGS[0].alias = "model"
    monkeypatch.setattr(launcher.platform, "platform", lambda: "inventory-test-platform")
    monkeypatch.setattr(launcher.subprocess, "run", lambda *a, **k: pytest.fail("no witness child"))
    report = launcher.check_sources(ROOT)
    assert report["successful"] and report["witness_execution"] == "not_requested"


@pytest.mark.parametrize("missing_pin", ["finite_protocol", "check", "statement"])
def test_missing_review_pin_refuses_inventory_and_execution(tmp_path, monkeypatch, missing_pin):
    root = fixed_fixture(tmp_path, monkeypatch)
    if missing_pin == "statement":
        pins = launcher.STATEMENT_BINDINGS
        monkeypatch.setattr(
            launcher,
            "STATEMENT_BINDINGS",
            (*pins[:-1], replace(pins[-1], sha256=launcher._PENDING_SHA256)),
        )
    else:
        monkeypatch.setattr(
            launcher,
            "SOURCE_BINDINGS",
            tuple(
                replace(pin, sha256=launcher._PENDING_SHA256) if pin.alias == missing_pin else pin
                for pin in launcher.SOURCE_BINDINGS
            ),
        )
    monkeypatch.setattr(launcher, "_load_runner", lambda *a: pytest.fail("no runner load"))
    for action in (launcher.check_sources, launcher.run_checks):
        with pytest.raises(launcher.SourceError, match="Pending reviewed source identities"):
            action(root)


@pytest.mark.parametrize("optimized", [False, True])
def test_production_suite_requires_reviewed_pins_before_exact_execution(optimized):
    report = launcher.run_checks(ROOT, optimized=optimized)
    assert report["successful"], report.get("test_output", report)
    assert report["tests_run"] == 31
    assert report["witness_execution"] == "returned"
    assert report["runtime"]["child_flags"] == ["-I", "-S", "-B"] + (["-O"] if optimized else [])
    assert report["executed_sources"] == sorted(
        str(ROOT / pin.path) for pin in launcher.SOURCE_BINDINGS
    )
    assert report["source_changes_after"] == report["unexecuted_declared_sources"] == []
    assert all(report[key] == 0 for key in ("failures", "errors", "skipped", "expected_failures"))


def test_fixture_inventory_is_not_witness_execution(tmp_path, monkeypatch):
    root = fixed_fixture(tmp_path, monkeypatch)
    monkeypatch.setattr(launcher.platform, "platform", lambda: "fixture-platform")
    monkeypatch.setattr(
        launcher.subprocess, "run", lambda *a, **k: pytest.fail("no child for check")
    )
    report = launcher.check_sources(root)
    assert report["successful"] and report["mode"] == "check"
    assert report["witness_execution"] == "not_requested" and "tests_run" not in report
    assert report["registered_by_general_research_runner"] is False
    assert report["contract"] == "EXPLICIT_FIXED_ALIAS_FINITE_PROTOCOL_V1"
    assert report["runner_sha256"] == launcher.EXPECTED_RUNNER_SHA256
    assert report["launcher_sha256"] == digest((root / launcher.LAUNCHER_PATH).read_bytes())
    assert report["source_changes_after"] == []


@pytest.mark.parametrize("optimized", [False, True])
def test_fixture_execution_creates_no_sources_caches_or_reports(tmp_path, monkeypatch, optimized):
    root = fixed_fixture(tmp_path, monkeypatch)
    before = snapshot(root)
    report = launcher.run_checks(root, optimized=optimized)
    assert report["successful"], report.get("test_output", report)
    assert report["tests_run"] == 1
    assert report["executed_sources"] == sorted(
        str(root / pin.path) for pin in launcher.SOURCE_BINDINGS
    )
    assert report["source_changes_after"] == []
    assert report["runtime"]["child_flags"] == ["-I", "-S", "-B"] + (["-O"] if optimized else [])
    assert report["executed_source_identities"] == [
        {"alias": pin.alias, "path": str(root / pin.path), "sha256": pin.sha256}
        for pin in launcher.SOURCE_BINDINGS
    ]
    assert snapshot(root) == before
    assert not list(root.rglob("__pycache__"))
    assert not list(root.rglob(".pytest_cache"))


@pytest.mark.parametrize(
    "mutation", ["missing", "extra", "collision", "reordered", "same_path", "wrong_mapping"]
)
def test_bad_alias_inventory_is_refused_before_a_child(tmp_path, monkeypatch, mutation):
    root = fixed_fixture(tmp_path, monkeypatch)
    rows = launcher.SOURCE_BINDINGS
    if mutation == "missing":
        rows = rows[:-1]
    elif mutation == "extra":
        rows += (replace(rows[0], alias="extra"),)
    elif mutation == "collision":
        rows = (rows[0], replace(rows[1], alias=rows[0].alias), *rows[2:])
    elif mutation == "reordered":
        rows = tuple(reversed(rows))
    elif mutation == "same_path":
        rows = (rows[0], replace(rows[1], path=rows[0].path, sha256=rows[0].sha256), *rows[2:])
    else:
        rows = (
            replace(rows[0], path=rows[1].path, sha256=rows[1].sha256),
            replace(rows[1], path=rows[0].path, sha256=rows[0].sha256),
            *rows[2:],
        )
    monkeypatch.setattr(launcher, "SOURCE_BINDINGS", rows)
    monkeypatch.setattr(
        launcher.subprocess, "run", lambda *a, **k: pytest.fail("must refuse before run")
    )
    with pytest.raises(launcher.SourceError):
        launcher.run_checks(root)


@pytest.mark.parametrize("which", [*ALIASES, "statement", "plan", "runner"])
def test_old_pinned_source_or_statement_drift_is_refused(tmp_path, monkeypatch, which):
    root = fixed_fixture(tmp_path, monkeypatch)
    if which == "statement":
        path = launcher.STATEMENT_BINDINGS[0].path
    elif which == "plan":
        path = launcher.STATEMENT_BINDINGS[-2].path
    elif which == "runner":
        path = launcher.RUNNER_PATH
    else:
        path = next(pin.path for pin in launcher.SOURCE_BINDINGS if pin.alias == which)
    (root / path).write_bytes((root / path).read_bytes() + b"\n# unreviewed drift\n")
    monkeypatch.setattr(launcher.subprocess, "run", lambda *a, **k: pytest.fail("must not execute"))
    with pytest.raises(launcher.SourceError):
        launcher.run_checks(root)


@pytest.mark.parametrize(
    "addition",
    [
        "import os\n",
        "import unlisted\n",
        "from . import finite_protocol\n",
        "import finite_protocol.hidden\n",
        'eval("1")\n',
        "import model\n",
    ],
)
def test_repinning_fixture_does_not_bypass_static_import_closure(tmp_path, monkeypatch, addition):
    root = fixed_fixture(tmp_path, monkeypatch)
    repin_fixture_source(root, monkeypatch, "check", addition + SMOKE)
    with pytest.raises(launcher.SourceError):
        launcher.check_sources(root)


@pytest.mark.parametrize("which", ["missing_file", "symlink"])
def test_fixed_binding_paths_must_be_actual_pinned_regular_files(tmp_path, monkeypatch, which):
    root = fixed_fixture(tmp_path, monkeypatch)
    path = root / launcher.SOURCE_BINDINGS[0].path
    data = path.read_bytes()
    path.unlink()
    if which == "symlink":
        elsewhere = root / "outside_alias.py"
        elsewhere.write_bytes(data)
        path.symlink_to(elsewhere)
    with pytest.raises(launcher.SourceError):
        launcher.check_sources(root)


@pytest.mark.parametrize("kind", ["empty", "skipped", "expected_failure", "failure"])
def test_incomplete_witness_results_do_not_report_success(tmp_path, monkeypatch, kind):
    source = SMOKE
    if kind == "empty":
        source = SMOKE[: SMOKE.index("class Witness")]
    elif kind == "skipped":
        source = source.replace(
            "    def test_aliases", "    @unittest.skip('fixture')\n    def test_aliases"
        )
    else:
        source = source.replace(
            "self.assertIs(local_joint_adapter.c, local_source)", "self.fail('fixture')"
        )
        if kind == "expected_failure":
            source = source.replace(
                "    def test_aliases", "    @unittest.expectedFailure\n    def test_aliases"
            )
    root = fixed_fixture(tmp_path, monkeypatch, source)
    report = launcher.run_checks(root)
    assert not report["successful"]
    assert report["source_changes_after"] == []
    if kind == "empty":
        assert report["tests_run"] == 0
    else:
        key = {
            "skipped": "skipped",
            "expected_failure": "expected_failures",
            "failure": "failures",
        }[kind]
        assert report[key] == 1


def test_statically_declared_but_unloaded_alias_cannot_satisfy_exact_runtime_closure(
    tmp_path, monkeypatch
):
    source = SMOKE.replace("import finite_protocol\n", "if False:\n    import finite_protocol\n")
    source = "\n".join(
        line
        for line in source.split("\n")
        if "self.assert" not in line or "finite_protocol" not in line
    )
    root = fixed_fixture(tmp_path, monkeypatch, source)
    assert launcher.check_sources(root)["successful"]
    report = launcher.run_checks(root)
    assert report["tests_run"] == 1 and report["failures"] == 0
    assert not report["successful"]
    adapter_path = next(
        pin.path for pin in launcher.SOURCE_BINDINGS if pin.alias == "finite_protocol"
    )
    assert report["unexecuted_declared_sources"] == [str(root / adapter_path)]


@pytest.mark.parametrize(
    "which", ["finite_protocol", "local_joint_adapter", "statement", "launcher", "runner"]
)
def test_after_run_drift_is_reported_and_refuses_success(tmp_path, monkeypatch, which):
    root = fixed_fixture(tmp_path, monkeypatch)
    path = (
        launcher.LAUNCHER_PATH
        if which == "launcher"
        else launcher.RUNNER_PATH
        if which == "runner"
        else launcher.STATEMENT_BINDINGS[-1].path
        if which == "statement"
        else next(pin.path for pin in launcher.SOURCE_BINDINGS if pin.alias == which)
    )
    actual = launcher.subprocess.run

    def mutate_after(*args, **kwargs):
        result = actual(*args, **kwargs)
        (root / path).write_bytes((root / path).read_bytes() + b"\n# changed after child\n")
        return result

    monkeypatch.setattr(launcher.subprocess, "run", mutate_after)
    report = launcher.run_checks(root)
    assert report["tests_run"] == 1 and report["failures"] == 0
    assert not report["successful"]
    assert report["source_changes_after"] == [path]
    assert report["launcher_source_changed"] is (which == "launcher")
    assert report["runner_source_changed"] is (which == "runner")


def test_child_uses_captured_alias_bytes_even_if_disk_changes_before_execution(
    tmp_path, monkeypatch
):
    root = fixed_fixture(tmp_path, monkeypatch)
    pin = next(pin for pin in launcher.SOURCE_BINDINGS if pin.alias == "local_source")
    actual = launcher.subprocess.run

    def mutate_before(*args, **kwargs):
        (root / pin.path).write_text("raise RuntimeError('disk replacement must never load')\n")
        return actual(*args, **kwargs)

    monkeypatch.setattr(launcher.subprocess, "run", mutate_before)
    report = launcher.run_checks(root)
    assert report["tests_run"] == 1 and report["errors"] == report["failures"] == 0
    assert not report["successful"]
    assert report["source_changes_after"] == [pin.path]
    assert pin.sha256 in {row["sha256"] for row in report["source_bindings"]}


def test_shared_child_audit_refuses_fixture_filesystem_mutation(tmp_path, monkeypatch):
    source = SMOKE.replace(
        "self.assertIs(local_joint_adapter.c, local_source)",
        "unittest.loader.os.mkdir('forbidden')",
    )
    root = fixed_fixture(tmp_path, monkeypatch, source)
    report = launcher.run_checks(root)
    assert not report["successful"]
    assert report["errors"] == 1
    assert not (root / "forbidden").exists()
    assert "action is disabled" in report["test_output"]


def test_timeout_has_no_success_or_fabricated_loaded_inventory(tmp_path, monkeypatch):
    root = fixed_fixture(tmp_path, monkeypatch)

    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("fixture", 60)

    monkeypatch.setattr(launcher.subprocess, "run", timeout)
    report = launcher.run_checks(root)
    assert not report["successful"]
    assert "timeout" in report["error"].lower()
    assert report["executed_sources"] == []
    assert report["unexecuted_declared_sources"] == sorted(
        str(root / pin.path) for pin in launcher.SOURCE_BINDINGS
    )
    assert report["source_changes_after"] == []


def test_cli_defaults_to_inventory_and_has_no_source_override():
    for arguments in ([], ["--check"]):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / launcher.LAUNCHER_PATH), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        report = json.loads(result.stdout)
        assert result.returncode == 0, result.stderr + result.stdout
        assert report["successful"] and report["mode"] == "check"
        assert "tests_run" not in report
    for arguments in (["--optimized"], ["--root", str(ROOT)], ["--run", "--check"]):
        result = subprocess.run(
            [sys.executable, "-B", str(ROOT / launcher.LAUNCHER_PATH), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 2


@pytest.mark.parametrize("optimized", [0, 1, "yes", None])
def test_optimization_mode_is_explicitly_boolean(optimized):
    with pytest.raises(TypeError):
        launcher.run_checks(ROOT, optimized=optimized)


@pytest.mark.parametrize("mutation", ["missing", "reordered", "source_path"])
def test_statement_inventory_cannot_be_dropped_or_turned_into_executable_evidence(
    tmp_path, monkeypatch, mutation
):
    root = fixed_fixture(tmp_path, monkeypatch)
    pins = launcher.STATEMENT_BINDINGS
    if mutation == "missing":
        pins = pins[:-1]
    elif mutation == "reordered":
        pins = tuple(reversed(pins))
    else:
        pins = (*pins[:-1], replace(pins[-1], path=launcher.SOURCE_BINDINGS[-1].path))
    monkeypatch.setattr(launcher, "STATEMENT_BINDINGS", pins)
    with pytest.raises(launcher.SourceError, match="statements"):
        launcher.check_sources(root)


@pytest.mark.parametrize(
    "mutation",
    [
        "invalid_json",
        "not_object",
        "duplicate_source",
        "foreign_source",
        "nonstring_source",
        "not_list",
        "boolean_count",
        "missing_count",
        "nonzero_exit",
        "false_success",
        "negative_count",
        "boolean_failures",
    ],
)
def test_malformed_child_accounting_cannot_claim_success(tmp_path, monkeypatch, mutation):
    root = fixed_fixture(tmp_path, monkeypatch)
    # Metadata collection can invoke uname; this stub applies only to the
    # following deliberate witness-child result injection.
    monkeypatch.setattr(launcher.platform, "platform", lambda: "fixture-platform")
    paths = sorted(str(root / pin.path) for pin in launcher.SOURCE_BINDINGS)
    result = {
        "successful": True,
        "tests_run": 1,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "expected_failures": 0,
        "executed_sources": paths,
    }
    returncode = 0
    if mutation == "duplicate_source":
        result["executed_sources"] = paths + paths[:1]
    elif mutation == "foreign_source":
        result["executed_sources"] = paths[:-1] + [str(root / "foreign.py")]
    elif mutation == "nonstring_source":
        result["executed_sources"] = [*paths[:-1], 1]
    elif mutation == "not_list":
        result["executed_sources"] = "wrong"
    elif mutation == "boolean_count":
        result["tests_run"] = True
    elif mutation == "missing_count":
        del result["skipped"]
    elif mutation == "negative_count":
        result["tests_run"] = -1
    elif mutation == "boolean_failures":
        result["failures"] = False
    elif mutation == "false_success":
        result["successful"] = False
    elif mutation == "nonzero_exit":
        returncode = 1
    stdout = (
        "invalid"
        if mutation == "invalid_json"
        else json.dumps([] if mutation == "not_object" else result)
    )
    monkeypatch.setattr(
        launcher.subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(a, returncode, stdout, "fixture stderr"),
    )
    report = launcher.run_checks(root)
    assert report["successful"] is False
    assert report["witness_execution"] == "returned"
    assert report["source_changes_after"] == []
