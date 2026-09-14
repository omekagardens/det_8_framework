"""Independent source-loading and refusal checks for the explicit RI-15 bridge."""

import hashlib
import json
import subprocess
import sys
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from scripts import run_qr_local_joint_adapter as launcher

ROOT = Path(__file__).resolve().parents[2]
ALIASES = ("local_source", "joint_source", "adapter", "check")
SMOKE = """import unittest
import local_source
import joint_source
import adapter
class Witness(unittest.TestCase):
    def test_aliases(self):
        self.assertIsNot(local_source.G, joint_source.G)
        self.assertTrue(callable(adapter.convert_local_state))
if __name__ == '__main__':
    unittest.main()
"""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def fixed_fixture(tmp_path, monkeypatch, source=SMOKE):
    """Copy fixed real-layout inputs; only explicit fixture pins are replaceable."""
    names = {pin.path for pin in (*launcher.SOURCE_BINDINGS, *launcher.STATEMENT_BINDINGS)}
    names.update((launcher.RUNNER_PATH, launcher.LAUNCHER_PATH))
    for name in names:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / name).read_bytes())
    check = next(pin for pin in launcher.SOURCE_BINDINGS if pin.alias == "check")
    (tmp_path / check.path).write_text(source)
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


def test_fixed_inventory_binds_both_model_names_without_colliding_or_executing(monkeypatch):
    # platform.platform() may itself call uname on a fresh macOS process.
    # Isolate that metadata lookup from the research-child execution guard.
    monkeypatch.setattr(launcher.platform, "platform", lambda: "inventory-test-platform")
    monkeypatch.setattr(
        launcher.subprocess, "run", lambda *a, **k: pytest.fail("no child for check")
    )
    report = launcher.check_sources(ROOT)
    assert report["successful"]
    assert report["mode"] == "check"
    assert report["runtime"]["platform"] == "inventory-test-platform"
    assert report["registered_by_general_research_runner"] is False
    assert tuple(row["alias"] for row in report["source_bindings"]) == ALIASES
    bindings = {row["alias"]: row for row in report["source_bindings"]}
    assert Path(bindings["local_source"]["path"]).name == "model.py"
    assert Path(bindings["joint_source"]["path"]).name == "model.py"
    assert bindings["local_source"]["path"] != bindings["joint_source"]["path"]
    assert bindings["local_source"]["sha256"] == (
        "173ad68ab8be40036a28e2806bfdb03dde8bd42030772a41084736d31e05fb86"
    )
    assert bindings["joint_source"]["sha256"] == (
        "666d3366e9b1be24d3b930973bb82b478a7af7901fe5b1321aecc06e47d26c30"
    )
    assert report["runner_sha256"] == (
        "35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f"
    )
    assert report["source_changes_after"] == []
    for pin in (*launcher.SOURCE_BINDINGS, *launcher.STATEMENT_BINDINGS):
        assert digest((ROOT / pin.path).read_bytes()) == pin.sha256
    with pytest.raises(FrozenInstanceError):
        launcher.SOURCE_BINDINGS[0].alias = "model"


@pytest.mark.parametrize("optimized", [False, True])
def test_real_interchange_suite_runs_under_exact_four_source_identities(optimized):
    report = launcher.run_checks(ROOT, optimized=optimized)
    assert report["successful"], report.get("test_output", report)
    assert report["mode"] == "run" and report["optimized"] is optimized
    assert report["tests_run"] == 20
    assert report["runtime"]["child_flags"] == ["-I", "-S", "-B"] + (["-O"] if optimized else [])
    assert report["executed_sources"] == sorted(
        str(ROOT / pin.path) for pin in launcher.SOURCE_BINDINGS
    )
    assert report["unexecuted_declared_sources"] == []
    assert report["source_changes_after"] == []
    assert not report["runner_source_changed"] and not report["launcher_source_changed"]
    assert all(report[key] == 0 for key in ("failures", "errors", "skipped", "expected_failures"))


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
    assert snapshot(root) == before
    assert not list(root.rglob("__pycache__"))
    assert not list(root.rglob(".pytest_cache"))


@pytest.mark.parametrize("mutation", ["missing", "extra", "collision", "reordered", "same_path"])
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
    else:
        rows = (rows[0], replace(rows[1], path=rows[0].path, sha256=rows[0].sha256), *rows[2:])
    monkeypatch.setattr(launcher, "SOURCE_BINDINGS", rows)
    monkeypatch.setattr(
        launcher.subprocess, "run", lambda *a, **k: pytest.fail("must refuse before run")
    )
    with pytest.raises(launcher.SourceError):
        launcher.run_checks(root)


@pytest.mark.parametrize("which", ["local_source", "joint_source", "statement", "runner"])
def test_old_pinned_source_or_statement_drift_is_refused(tmp_path, monkeypatch, which):
    root = fixed_fixture(tmp_path, monkeypatch)
    if which == "statement":
        path = launcher.STATEMENT_BINDINGS[0].path
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
    ["import os\n", "import unlisted\n", "from . import adapter\n", "import adapter.hidden\n"],
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
        source = "import unittest\nimport adapter\nimport local_source\nimport joint_source\n"
    elif kind == "skipped":
        source = source.replace(
            "    def test_aliases", "    @unittest.skip('fixture')\n    def test_aliases"
        )
    else:
        source = source.replace(
            "self.assertIsNot(local_source.G, joint_source.G)", "self.fail('fixture')"
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
    source = SMOKE.replace("import adapter\n", "if False:\n    import adapter\n")
    source = source.replace("        self.assertTrue(callable(adapter.convert_local_state))\n", "")
    root = fixed_fixture(tmp_path, monkeypatch, source)
    assert launcher.check_sources(root)["successful"]
    report = launcher.run_checks(root)
    assert report["tests_run"] == 1 and report["failures"] == 0
    assert not report["successful"]
    adapter_path = next(pin.path for pin in launcher.SOURCE_BINDINGS if pin.alias == "adapter")
    assert report["unexecuted_declared_sources"] == [str(root / adapter_path)]


@pytest.mark.parametrize("which", ["adapter", "launcher", "runner"])
def test_after_run_drift_is_reported_and_refuses_success(tmp_path, monkeypatch, which):
    root = fixed_fixture(tmp_path, monkeypatch)
    path = (
        launcher.LAUNCHER_PATH
        if which == "launcher"
        else launcher.RUNNER_PATH
        if which == "runner"
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
        "self.assertTrue(callable(adapter.convert_local_state))",
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
        assert result.returncode == 0, result.stderr + result.stdout
        report = json.loads(result.stdout)
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
