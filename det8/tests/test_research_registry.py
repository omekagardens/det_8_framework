"""Research registration binds real imports and preserves execution/refusal boundaries."""

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts import run_research_checks as runner

ROOT = Path(__file__).resolve().parents[2]
PASSING = """import unittest
class Witness(unittest.TestCase):
    def test_exact(self):
        self.assertEqual(1 + 1, 2)
if __name__ == '__main__':
    unittest.main()
"""


def fixture_registry(tmp_path, source=PASSING, dependencies=None):
    directory = tmp_path / "docs/validation/example"
    directory.mkdir(parents=True)
    files = {"check.py": source, **(dependencies or {})}
    for name, text in files.items():
        (directory / name).write_text(text)
    (directory / "THEOREM.md").write_text("Conditional statement; tests are finite witnesses.\n")

    def pin(name):
        path = directory / name
        return {
            "path": path.relative_to(tmp_path).as_posix(),
            "sha256": runner.digest(path.read_bytes()),
        }

    manifest = {
        "schema_version": 1,
        "evidence_kind": "finite_witness_verification_not_theorem_proof",
        "suites": [
            {
                "id": "example",
                "statement": "A finite exact illustration.",
                "premises": ["Declared finite inputs."],
                "limits": ["No universal proof."],
                "document": pin("THEOREM.md"),
                "entrypoint": pin("check.py")["path"],
                "sources": [pin(name) for name in files],
                "stdlib_imports": ["unittest"],
                "timeout_seconds": 5,
            }
        ],
    }
    target = tmp_path / runner.DEFAULT_MANIFEST
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps(manifest))
    return manifest, target, directory


def save(target, manifest):
    target.write_text(json.dumps(manifest))


def test_real_registry_covers_coherent_imports_and_lists_without_executing(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("list/check must not start a process")

    monkeypatch.setattr(runner.subprocess, "run", forbidden)
    result = runner.evaluate(ROOT, runner.DEFAULT_MANIFEST, [])
    assert result["successful"] and result["results"] == []
    suites = {row["id"]: row for row in result["registered_suites"]}
    assert set(suites) == {
        "strict-derivation",
        "operation-domain",
        "hypothesis-countermodels",
        "chosen-law",
        "coherent-readout",
        "record-context",
        "controlled-context",
        "first-commit-quotient",
        "maximal-record-domain",
        "control-selected-qubit",
        "repeatable-record-instrument",
        "joint-recordability",
        "repeatability-robustness",
        "joint-repeatability",
        "cut-closed-completion",
        "reversible-generator",
        "terminal-read-observability",
        "observation-stability",
        "retained-word-first-commit",
    }
    paths = {Path(row["path"]).name for row in suites["coherent-readout"]["sources"]}
    assert paths == {"check.py", "algebra.py", "reference.py"}
    controlled_paths = {Path(row["path"]).name for row in suites["controlled-context"]["sources"]}
    assert controlled_paths == {"check.py", "model.py"}
    quotient_paths = {Path(row["path"]).name for row in suites["first-commit-quotient"]["sources"]}
    assert quotient_paths == {"check.py", "model.py"}
    qubit_paths = {Path(row["path"]).name for row in suites["control-selected-qubit"]["sources"]}
    assert qubit_paths == {"check.py", "model.py"}
    instrument_paths = {
        Path(row["path"]).name for row in suites["repeatable-record-instrument"]["sources"]
    }
    assert instrument_paths == {"check.py", "model.py"}
    joint_paths = {Path(row["path"]).name for row in suites["joint-recordability"]["sources"]}
    assert joint_paths == {"check.py", "model.py"}
    robustness_paths = {
        Path(row["path"]).name for row in suites["repeatability-robustness"]["sources"]
    }
    assert robustness_paths == {"check.py", "model.py"}
    joint_repeatability_paths = {
        Path(row["path"]).name for row in suites["joint-repeatability"]["sources"]
    }
    assert joint_repeatability_paths == {"check.py", "model.py"}
    cut_closed_paths = {
        Path(row["path"]).name for row in suites["cut-closed-completion"]["sources"]
    }
    assert cut_closed_paths == {"check.py", "model.py"}
    generator_paths = {Path(row["path"]).name for row in suites["reversible-generator"]["sources"]}
    assert generator_paths == {"check.py", "model.py"}
    terminal_read_paths = {
        Path(row["path"]).name for row in suites["terminal-read-observability"]["sources"]
    }
    assert terminal_read_paths == {"check.py", "model.py"}
    stability_paths = {Path(row["path"]).name for row in suites["observation-stability"]["sources"]}
    assert stability_paths == {"check.py", "model.py"}
    retained_word_paths = {
        Path(row["path"]).name for row in suites["retained-word-first-commit"]["sources"]
    }
    assert retained_word_paths == {"check.py", "model.py"}
    assert all(
        result["source_identities"][i]["sha256"] for i in range(len(result["source_identities"]))
    )


def test_transitive_local_import_must_be_pinned_even_when_never_executed(tmp_path):
    source = "import bridge\n" + PASSING
    manifest, target, directory = fixture_registry(
        tmp_path, source, {"bridge.py": "if False:\n    import leaf\n", "leaf.py": "VALUE = 2\n"}
    )
    manifest["suites"][0]["sources"] = [
        row for row in manifest["suites"][0]["sources"] if not row["path"].endswith("leaf.py")
    ]
    save(target, manifest)
    with pytest.raises(runner.RegistryError, match="unregistered or unsupported import leaf"):
        runner.load_registry(tmp_path)
    assert (directory / "leaf.py").is_file()


def test_unreachable_declared_code_is_not_treated_as_a_dependency(tmp_path):
    fixture_registry(tmp_path, dependencies={"unrelated.py": "VALUE = 3\n"})
    with pytest.raises(runner.RegistryError, match="outside import closure"):
        runner.load_registry(tmp_path)


def test_controlled_context_stdlib_extension_executes_pinned_local_dependency(tmp_path):
    source = "import helper\n" + PASSING.replace("1 + 1", "helper.VALUE['answer']")
    helper = (
        "from collections.abc import Iterable\n"
        "from types import MappingProxyType\n"
        "VALUE = MappingProxyType({'answer': 2})\n"
    )
    manifest, target, directory = fixture_registry(tmp_path, source, {"helper.py": helper})
    manifest["suites"][0]["stdlib_imports"] = ["collections.abc", "types", "unittest"]
    save(target, manifest)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert result["successful"]
    assert result["results"][0]["executed_sources"] == sorted(
        [str(directory / "check.py"), str(directory / "helper.py")]
    )
    assert result["results"][0]["unexecuted_declared_sources"] == []


@pytest.mark.parametrize("optimized", [False, True])
def test_math_isqrt_requires_declared_closure_and_executes_exactly(tmp_path, optimized):
    source = "import helper\n" + PASSING.replace(
        "self.assertEqual(1 + 1, 2)", "self.assertEqual(helper.ROOT, 10**30 + 123456788)"
    )
    helper = "from math import isqrt\nROOT = isqrt((10**30 + 123456789)**2 - 1)\n"
    manifest, target, directory = fixture_registry(tmp_path, source, {"helper.py": helper})
    with pytest.raises(runner.RegistryError, match="stdlib_imports must equal"):
        runner.load_registry(tmp_path)
    manifest["suites"][0]["stdlib_imports"] = ["math", "unittest"]
    save(target, manifest)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"], optimized=optimized)
    assert result["successful"]
    assert result["runtime"]["optimized_checks"] is optimized
    assert result["results"][0]["tests_run"] == 1
    assert result["results"][0]["executed_sources"] == sorted(
        [str(directory / "check.py"), str(directory / "helper.py")]
    )
    assert result["results"][0]["unexecuted_declared_sources"] == []
    assert result["source_changes_after"] == []


@pytest.mark.parametrize(
    "statement",
    [
        "import numpy",
        "from importlib import import_module",
        "from . import relative",
        "from collections.abc.fake import Unsupported",
        "from math.fake import isqrt",
        "__import__('unittest')",
        "eval('1 + 1')",
    ],
)
def test_external_dynamic_and_relative_import_contracts_are_refused(tmp_path, statement):
    fixture_registry(tmp_path, statement + "\n" + PASSING)
    with pytest.raises(runner.RegistryError):
        runner.load_registry(tmp_path)


@pytest.mark.parametrize(
    "path",
    [
        "../outside.py",
        "/tmp/outside.py",
        "a/../check.py",
        "a//check.py",
        "./check.py",
        "a\\check.py",
    ],
)
def test_noncanonical_and_escaping_paths_are_rejected(tmp_path, path):
    manifest, target, _ = fixture_registry(tmp_path)
    manifest["suites"][0]["sources"][0]["path"] = path
    save(target, manifest)
    with pytest.raises(runner.RegistryError, match="path"):
        runner.load_registry(tmp_path)


def test_symlink_inside_root_is_not_a_pinned_source(tmp_path):
    _, _, directory = fixture_registry(tmp_path)
    original = directory / "check.py"
    original.rename(directory / "original.py")
    original.symlink_to(directory / "original.py")
    with pytest.raises(runner.RegistryError, match="symlink"):
        runner.load_registry(tmp_path)


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate_id",
        "shell_id",
        "boolean_timeout",
        "unknown_key",
        "wrong_stdlib",
        "document_drift",
        "source_drift",
    ],
)
def test_malformed_registry_and_stale_claim_or_code_are_rejected(tmp_path, mutation):
    manifest, target, directory = fixture_registry(tmp_path)
    suite = manifest["suites"][0]
    if mutation == "duplicate_id":
        manifest["suites"].append(copy.deepcopy(suite))
    elif mutation == "shell_id":
        suite["id"] = "example; touch injected"
    elif mutation == "boolean_timeout":
        suite["timeout_seconds"] = True
    elif mutation == "unknown_key":
        suite["command"] = "anything"
    elif mutation == "wrong_stdlib":
        suite["stdlib_imports"] = ["fractions", "unittest"]
    elif mutation == "document_drift":
        (directory / "THEOREM.md").write_text("Different premise set\n")
    else:
        (directory / "check.py").write_text(PASSING + "# changed\n")
    save(target, manifest)
    with pytest.raises(runner.RegistryError):
        runner.load_registry(tmp_path)


def test_duplicate_json_keys_are_rejected(tmp_path):
    _, target, _ = fixture_registry(tmp_path)
    target.write_text('{"schema_version":1,"schema_version":1}')
    with pytest.raises(runner.RegistryError, match="duplicate JSON key"):
        runner.load_registry(tmp_path)


@pytest.mark.parametrize("role", ["document", "sources"])
def test_conflicting_shared_path_is_rejected_even_if_each_read_matches_its_pin(
    tmp_path, monkeypatch, role
):
    manifest, target, _ = fixture_registry(tmp_path)
    second = copy.deepcopy(manifest["suites"][0])
    second["id"] = "later"
    row = second[role] if role == "document" else second[role][0]
    changed = b"Changed statement\n" if role == "document" else (PASSING + "# changed\n").encode()
    row["sha256"] = runner.digest(changed)
    manifest["suites"].append(second)
    save(target, manifest)
    actual_read = runner.read_source
    count = 0

    def racing_read(root, name):
        nonlocal count
        if name == row["path"]:
            count += 1
            if count == 2:
                (root / name).write_bytes(changed)
        return actual_read(root, name)

    monkeypatch.setattr(runner, "read_source", racing_read)
    with pytest.raises(runner.RegistryError, match="conflicting repeated source identity"):
        runner.load_registry(tmp_path)


@pytest.mark.parametrize("optimized", [False, True])
def test_selected_module_and_pinned_sibling_execute_without_source_writes(tmp_path, optimized):
    source = "import helper\n" + PASSING.replace("1 + 1", "helper.VALUE")
    _, _, directory = fixture_registry(tmp_path, source, {"helper.py": "VALUE = 2\n"})
    before = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"], optimized=optimized)
    assert result["successful"] and result["source_changes_after"] == []
    check = result["results"][0]
    assert check["tests_run"] == 1
    assert check["executed_sources"] == sorted(
        [str(directory / "check.py"), str(directory / "helper.py")]
    )
    after = {p.relative_to(tmp_path): p.read_bytes() for p in tmp_path.rglob("*") if p.is_file()}
    assert before == after
    assert not list(tmp_path.rglob("__pycache__"))
    assert not list(tmp_path.rglob(".pytest_cache"))


@pytest.mark.parametrize(
    "source, tests_run", [(PASSING.replace("1 + 1", "3"), 1), ("import unittest\n", 0)]
)
def test_failed_witness_and_empty_suite_do_not_report_success(tmp_path, source, tests_run):
    fixture_registry(tmp_path, source)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert not result["successful"]
    assert result["results"][0]["tests_run"] == tests_run


@pytest.mark.parametrize(
    "decorator, expression, field",
    [
        ("@unittest.skip('missing premise')", "1 + 1", "skipped"),
        ("@unittest.expectedFailure", "3", "expected_failures"),
    ],
)
def test_incomplete_witnesses_are_not_successful_verification(
    tmp_path, decorator, expression, field
):
    source = PASSING.replace("    def test_exact", f"    {decorator}\n    def test_exact")
    fixture_registry(tmp_path, source.replace("1 + 1", expression))
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert not result["successful"]
    assert result["results"][0][field] == 1


def test_conditional_import_remains_pinned_but_is_reported_as_unexecuted(tmp_path):
    fixture_registry(
        tmp_path, "if False:\n    import helper\n" + PASSING, {"helper.py": "VALUE = 2\n"}
    )
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert result["successful"]
    assert result["results"][0]["unexecuted_declared_sources"] == [
        str(tmp_path / "docs/validation/example/helper.py")
    ]
    identities = result["results"][0]["executed_source_identities"]
    assert [row["path"] for row in identities] == ["docs/validation/example/check.py"]


def test_child_executes_pinned_snapshots_and_disk_drift_remains_detectable(tmp_path):
    source = "import helper\n" + PASSING.replace("1 + 1", "helper.VALUE")
    fixture_registry(tmp_path, source, {"helper.py": "VALUE = 2\n"})
    registry, snapshots = runner.load_registry(tmp_path)
    changed = "docs/validation/example/helper.py"
    (tmp_path / changed).write_text("raise RuntimeError('must not execute changed disk bytes')\n")
    # The low-level executor consumes the supplied snapshot; evaluate() wraps
    # this with source checks and would refuse or fail on the changed disk file.
    result = runner.run_suite(tmp_path, registry["suites"][0], snapshots)
    assert result["successful"]
    assert runner.changed_sources(tmp_path, snapshots) == [changed]


def test_source_change_during_run_fails_and_stops_later_checks(tmp_path, monkeypatch):
    manifest, target, directory = fixture_registry(tmp_path)
    second = copy.deepcopy(manifest["suites"][0])
    second["id"] = "later"
    manifest["suites"].append(second)
    save(target, manifest)
    actual_run = runner.run_suite

    def mutate_after(root, suite, snapshots, **kwargs):
        result = actual_run(root, suite, snapshots, **kwargs)
        (directory / "check.py").write_text(PASSING + "# changed during run\n")
        return result

    monkeypatch.setattr(runner, "run_suite", mutate_after)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example", "later"])
    assert not result["successful"]
    assert result["source_changes_after"] == ["docs/validation/example/check.py"]
    assert [row["id"] for row in result["results"]] == ["example"]


def test_timeout_is_a_failed_result(tmp_path):
    manifest, target, _ = fixture_registry(tmp_path, "while True:\n    pass\n" + PASSING)
    manifest["suites"][0]["timeout_seconds"] = 1
    save(target, manifest)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert not result["successful"]
    assert result["results"][0]["error"] == "suite timeout"


def test_child_write_guard_refuses_mutation_even_through_a_stdlib_object(tmp_path):
    # unittest exposes os internally; the runtime audit is additional write
    # protection beyond the declared import audit, not a hostile-code sandbox.
    source = PASSING.replace("self.assertEqual(1 + 1, 2)", "unittest.loader.os.mkdir('forbidden')")
    fixture_registry(tmp_path, source)
    result = runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, ["example"])
    assert not result["successful"]
    assert not (tmp_path / "forbidden").exists()
    assert "action is disabled" in result["results"][0]["test_output"]


def test_unknown_or_duplicate_selection_never_executes(tmp_path, monkeypatch):
    fixture_registry(tmp_path)
    monkeypatch.setattr(
        runner, "run_suite", lambda *args, **kwargs: pytest.fail("must not execute")
    )
    for selected in (["missing"], ["example", "example"], ["example; touch nope"]):
        with pytest.raises(runner.RegistryError, match="unique registered"):
            runner.evaluate(tmp_path, runner.DEFAULT_MANIFEST, selected)


def test_cli_emits_json_with_failure_exit_for_unknown_id():
    result = subprocess.run(
        [
            sys.executable,
            "-B",
            str(ROOT / "scripts/run_research_checks.py"),
            "--suite",
            "unregistered",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert json.loads(result.stdout)["successful"] is False
