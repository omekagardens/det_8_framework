"""Check or explicitly run one source-pinned local-to-joint research adapter.

This coordinator-only fixed-alias contract is separate from the general
research registry's sibling-import contract. It does not register a suite,
discover research directories or import research into a supported DET API.
Use Python -B. No evidence or cache files are written by the launcher/child.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
import types
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = "EXPLICIT_FIXED_ALIAS_COORDINATOR_ADAPTER_V1"
LAUNCHER_PATH = "scripts/run_qr_local_joint_adapter.py"
RUNNER_PATH = "scripts/run_research_checks.py"
EXPECTED_RUNNER_SHA256 = "35b0793f87f175384a194f69ab18d3ed64c2e260528fc91849b139717d90cd2f"
TIMEOUT_SECONDS = 60
_ALIASES = ("local_source", "joint_source", "adapter", "check")
_MAX_FILE_BYTES = 1_000_000


class SourceError(ValueError):
    """Fixed source identity or the explicit alias contract failed before execution."""


@dataclass(frozen=True)
class SourceBinding:
    alias: str
    path: str
    sha256: str


@dataclass(frozen=True)
class FilePin:
    path: str
    sha256: str


# Fixed reviewed source identities. Later changes require coordinator review;
# a failed identity check must never trigger an automatic pin refresh.
SOURCE_BINDINGS = (
    SourceBinding(
        "local_source",
        "docs/validation/t8-q-repeatable-record-instrument-2026-09-13/model.py",
        "173ad68ab8be40036a28e2806bfdb03dde8bd42030772a41084736d31e05fb86",
    ),
    SourceBinding(
        "joint_source",
        "docs/validation/t8-q-joint-recordability-2026-09-13/model.py",
        "666d3366e9b1be24d3b930973bb82b478a7af7901fe5b1321aecc06e47d26c30",
    ),
    SourceBinding(
        "adapter",
        "docs/validation/t8-q-local-joint-adapter-2026-09-13/adapter.py",
        "0d94c188cbff0ccfe92f7d3335c36bd5e638333b3d9b13c1d6f4ac00c9a0e8e6",
    ),
    SourceBinding(
        "check",
        "docs/validation/t8-q-local-joint-adapter-2026-09-13/check.py",
        "faab57484d8c8e05a924d37d8325c10ecbf4f325a1f91ee3af66163b5a2e9d94",
    ),
)
STATEMENT_BINDINGS = (
    FilePin(
        "docs/validation/t8-q-repeatable-record-instrument-2026-09-13/REPEATABLE_INSTRUMENT.md",
        "7870bfa7549cb134a6dea54cd1b98ef3451736067ad6ebe6a86498576a40a62c",
    ),
    FilePin(
        "docs/validation/t8-q-joint-recordability-2026-09-13/JOINT_RECORDABILITY.md",
        "34d7fb69bc72764de2d0ee239ee5af3f132ec37247d67e6674a41f98e0beb444",
    ),
    FilePin(
        "docs/validation/t8-q-local-joint-adapter-2026-09-13/ADAPTER.md",
        "5d03f62504ae1ddc3b0bc1d30b7ef83ab58b228ab49dd72211e94a50ea571947",
    ),
)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_runner(root: Path) -> tuple[types.ModuleType, bytes]:
    """Verify before executing the helper's captured bytes, without a disk reload."""
    path = root
    for component in Path(RUNNER_PATH).parts:
        path = path / component
        if path.is_symlink():
            raise SourceError("Runner source path contains a symlink")
    if not path.is_file():
        raise SourceError("The pinned research runner is missing")
    with path.open("rb") as stream:
        data = stream.read(_MAX_FILE_BYTES + 1)
    if len(data) > _MAX_FILE_BYTES or _digest(data) != EXPECTED_RUNNER_SHA256:
        raise SourceError("Pinned research runner hash mismatch")
    module = types.ModuleType("_qr_local_joint_pinned_runner")
    module.__file__ = str(path)
    # The helper has no sibling imports or dataclasses. It is deliberately not
    # installed as a supported package module or reloaded through an import hook.
    exec(compile(data, str(path), "exec"), module.__dict__)  # noqa: S102 -- exact reviewed byte pin
    return module, data


@dataclass
class _Inspection:
    root: Path
    runner: types.ModuleType
    snapshots: dict[str, bytes]
    report: dict[str, object]


def _inspect(root: Path | None = None) -> _Inspection:
    root = ROOT if root is None else Path(root).absolute()
    if tuple(binding.alias for binding in SOURCE_BINDINGS) != _ALIASES:
        raise SourceError("Declare exactly the four fixed, ordered and unique source aliases")
    names = [binding.path for binding in SOURCE_BINDINGS]
    statement_names = [pin.path for pin in STATEMENT_BINDINGS]
    if len(set(names + statement_names + [RUNNER_PATH, LAUNCHER_PATH])) != 9:
        raise SourceError("Every source, statement and launcher path must be distinct")
    if len(STATEMENT_BINDINGS) != 3:
        raise SourceError("Retain both accepted statements and the adapter contract")
    runner, runner_bytes = _load_runner(root)
    snapshots = {RUNNER_PATH: runner_bytes}
    try:
        for pin in (*SOURCE_BINDINGS, *STATEMENT_BINDINGS):
            snapshots[pin.path] = runner.pinned_source(
                root, {"path": pin.path, "sha256": pin.sha256}
            )
        snapshots[LAUNCHER_PATH] = runner.read_source(root, LAUNCHER_PATH)
        # These virtual sibling filenames audit only the fixed alias graph.
        # Packet execution and all provenance continue to use the real paths.
        virtual = {binding.alias + ".py": snapshots[binding.path] for binding in SOURCE_BINDINGS}
        closure = runner.import_closure(root, "check.py", virtual)
        if "unittest" not in closure:
            raise SourceError("The explicit check entry must supply unittest witnesses")
    except (OSError, runner.RegistryError) as exc:
        raise SourceError(str(exc)) from exc
    report = {
        "mode": "check",
        "contract": CONTRACT,
        "registered_by_general_research_runner": False,
        "successful": True,
        "source_check_before": "matched",
        "source_bindings": [
            {"alias": binding.alias, "path": binding.path, "sha256": binding.sha256}
            for binding in SOURCE_BINDINGS
        ],
        "statements": [{"path": pin.path, "sha256": pin.sha256} for pin in STATEMENT_BINDINGS],
        "runner_sha256": _digest(runner_bytes),
        "launcher_sha256": _digest(snapshots[LAUNCHER_PATH]),
        "stdlib_imports": closure,
        "runtime": {
            "python_version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "executable_sha256": _digest(Path(sys.executable).read_bytes()),
            "platform": platform.platform(),
        },
    }
    return _Inspection(root, runner, snapshots, report)


def _finish(inspection: _Inspection) -> dict[str, object]:
    changes = inspection.runner.changed_sources(inspection.root, inspection.snapshots)
    inspection.report["source_changes_after"] = changes
    inspection.report["runner_source_changed"] = RUNNER_PATH in changes
    inspection.report["launcher_source_changed"] = LAUNCHER_PATH in changes
    if changes:
        inspection.report["successful"] = False
        inspection.report["error"] = "Captured source changed after inspection or execution"
    return inspection.report


def check_sources(root: Path | None = None) -> dict[str, object]:
    """Check fixed identities and alias closure; do not execute adapter/witness code."""
    return _finish(_inspect(root))


def run_checks(root: Path | None = None, *, optimized: bool = False) -> dict[str, object]:
    """Explicitly run one isolated captured witness suite with fixed source aliases."""
    if type(optimized) is not bool:
        raise TypeError("optimized must be a boolean")
    inspection = _inspect(root)
    report, runner = inspection.report, inspection.runner
    report.update({"mode": "run", "optimized": optimized, "successful": False})
    items = {
        binding.alias: {
            "path": str(inspection.root / binding.path),
            "text": inspection.snapshots[binding.path].decode("utf-8"),
        }
        for binding in SOURCE_BINDINGS
    }
    packet = {
        "entry": items["check"],
        "sources": {alias: item for alias, item in items.items() if alias != "check"},
    }
    flags = ["-I", "-S", "-B", *(["-O"] if optimized else [])]
    report["runtime"]["child_flags"] = flags
    expected = {item["path"] for item in items.values()}
    try:
        child = subprocess.run(
            [sys.executable, *flags, "-c", runner.CHILD],
            input=json.dumps(packet),
            text=True,
            capture_output=True,
            cwd=inspection.root,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired:
        report.update({"error": "Adapter witness timeout", "executed_sources": []})
        report["unexecuted_declared_sources"] = sorted(expected)
        return _finish(inspection)
    report.update({"returncode": child.returncode, "stderr": child.stderr})
    try:
        result = json.loads(child.stdout)
        if type(result) is not dict:
            raise ValueError("Child report is not an object")
    except (ValueError, UnicodeError) as exc:
        report.update({"error": "Invalid child report: " + str(exc), "executed_sources": []})
        report["unexecuted_declared_sources"] = sorted(expected)
        return _finish(inspection)
    for key in (
        "tests_run",
        "failures",
        "errors",
        "skipped",
        "expected_failures",
        "test_output",
        "error",
    ):
        if key in result:
            report[key] = result[key]
    executed = result.get("executed_sources", [])
    valid_inventory = (
        type(executed) is list
        and all(type(path) is str for path in executed)
        and len(executed) == len(set(executed))
    )
    if not valid_inventory:
        report.update({"error": "Invalid child source inventory", "executed_sources": []})
        report["unexecuted_declared_sources"] = sorted(expected)
        return _finish(inspection)
    report["executed_sources"] = executed
    report["unexecuted_declared_sources"] = sorted(expected - set(executed))
    counts_valid = (
        type(result.get("tests_run")) is int
        and result["tests_run"] > 0
        and all(
            type(result.get(key)) is int and result[key] == 0
            for key in ("failures", "errors", "skipped", "expected_failures")
        )
    )
    report["successful"] = (
        result.get("successful") is True
        and child.returncode == 0
        and counts_valid
        and set(executed) == expected
    )
    if set(executed) != expected:
        report["error"] = "Child execution did not load exactly the four declared real sources"
    return _finish(inspection)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check inventory only (the default)")
    mode.add_argument("--run", action="store_true", help="Explicitly execute the bounded witnesses")
    parser.add_argument("--optimized", action="store_true", help="Use -O with an explicit --run")
    args = parser.parse_args(argv)
    if args.optimized and not args.run:
        parser.error("--optimized requires explicit --run")
    try:
        report = run_checks(optimized=args.optimized) if args.run else check_sources()
    except (SourceError, OSError) as exc:
        report = {"contract": CONTRACT, "successful": False, "error": str(exc)}
    print(json.dumps(report, sort_keys=True, indent=2))
    return 0 if report["successful"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
