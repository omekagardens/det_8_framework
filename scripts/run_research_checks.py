"""Run explicitly registered finite research witnesses without writing evidence files.

This is a source-bound unittest runner, not a theorem prover or a sandbox for
untrusted Python. Only the deliberately narrow import contract is supported.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = "docs/research/registry.json"
STDLIB_IMPORTS = frozenset(
    {"collections.abc", "dataclasses", "fractions", "itertools", "math", "types", "unittest"}
)
ID = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
MAX_FILE_BYTES = 1_000_000


class RegistryError(ValueError):
    """The manifest, source identity or supported execution contract is invalid."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise RegistryError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def keys(value, expected, label):
    if type(value) is not dict or set(value) != set(expected):
        raise RegistryError(f"{label}: expected fields {sorted(expected)}")


def strings(value, label):
    if type(value) is not list or not value or any(type(s) is not str or not s for s in value):
        raise RegistryError(f"{label}: expected a nonempty list of nonempty strings")
    if len(set(value)) != len(value):
        raise RegistryError(f"{label}: duplicate values")


def source_path(root: Path, name: str) -> Path:
    """Accept canonical repository-relative regular files, with no symlink components."""
    if type(name) is not str or not name or "\\" in name or "\x00" in name:
        raise RegistryError("invalid source path")
    relative = PurePosixPath(name)
    if (
        relative.is_absolute()
        or relative.as_posix() != name
        or any(part in {".", ".."} for part in relative.parts)
    ):
        raise RegistryError(f"noncanonical or escaping path: {name}")
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise RegistryError(f"symlink source path: {name}")
    if not path.is_file():
        raise RegistryError(f"source is not a regular file: {name}")
    return path


def read_source(root: Path, name: str) -> bytes:
    path = source_path(root, name)
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise RegistryError(f"source exceeds byte limit: {name}")
    return data


def pinned_source(root: Path, item: dict) -> bytes:
    keys(item, {"path", "sha256"}, "source")
    if type(item["sha256"]) is not str or not DIGEST.fullmatch(item["sha256"]):
        raise RegistryError("source: invalid SHA-256")
    data = read_source(root, item["path"])
    if digest(data) != item["sha256"]:
        raise RegistryError(f"source hash mismatch: {item['path']}")
    return data


def remember_source(snapshots: dict[str, bytes], name: str, data: bytes) -> None:
    if name in snapshots and snapshots[name] != data:
        raise RegistryError(f"conflicting repeated source identity: {name}")
    snapshots[name] = data


def import_closure(root: Path, entrypoint: str, sources: dict[str, bytes]) -> list[str]:
    """Prove the static sibling-module closure for this restricted source language.

    No packages, relative imports, dynamic import/code execution or arbitrary
    external imports are accepted. All Python source in the closure is pinned.
    Standard-library transitive dependencies belong to the identified runtime.
    """
    pending, visited, standard = [entrypoint], set(), set()
    forbidden = {"__import__", "eval", "exec", "compile", "open"}
    while pending:
        name = pending.pop()
        if name in visited:
            continue
        if name not in sources:
            raise RegistryError(f"unregistered executable dependency: {name}")
        visited.add(name)
        try:
            tree = ast.parse(sources[name], filename=name)
        except (SyntaxError, UnicodeError) as exc:
            raise RegistryError(f"cannot parse source {name}: {exc}") from exc
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in forbidden:
                raise RegistryError(f"unsupported dynamic code or file access in {name}")
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.level or not node.module:
                    raise RegistryError(f"relative import is unsupported: {name}")
                modules.append(node.module)
        for module in modules:
            if module in STDLIB_IMPORTS:
                standard.add(module)
            elif "." not in module and module.isidentifier():
                dependency = str(PurePosixPath(entrypoint).parent / f"{module}.py")
                if dependency not in sources:
                    raise RegistryError(f"unregistered or unsupported import {module} in {name}")
                if module in sys.stdlib_module_names:
                    raise RegistryError(f"local module shadows standard library: {module}")
                pending.append(dependency)
            else:
                raise RegistryError(f"unsupported import {module} in {name}")
    if visited != set(sources):
        raise RegistryError(
            f"declared executable sources outside import closure: {sorted(set(sources) - visited)}"
        )
    return sorted(standard)


def load_registry(root: Path, manifest: str = DEFAULT_MANIFEST) -> tuple[dict, dict[str, bytes]]:
    raw = read_source(root, manifest)
    try:
        registry = json.loads(raw, object_pairs_hook=no_duplicates)
    except (ValueError, UnicodeError) as exc:
        raise RegistryError(f"invalid manifest JSON: {exc}") from exc
    keys(registry, {"schema_version", "evidence_kind", "suites"}, "registry")
    if type(registry["schema_version"]) is not int or registry["schema_version"] != 1:
        raise RegistryError("unsupported registry schema")
    if registry["evidence_kind"] != "finite_witness_verification_not_theorem_proof":
        raise RegistryError("registry evidence kind is not finite witness verification")
    suites = registry["suites"]
    if type(suites) is not list or not 1 <= len(suites) <= 32:
        raise RegistryError("registry must contain 1 to 32 explicitly named suites")
    snapshots, ids = {manifest: raw}, set()
    for suite in suites:
        keys(
            suite,
            {
                "id",
                "statement",
                "premises",
                "limits",
                "document",
                "entrypoint",
                "sources",
                "stdlib_imports",
                "timeout_seconds",
            },
            "suite",
        )
        identifier = suite["id"]
        if type(identifier) is not str or not ID.fullmatch(identifier) or identifier in ids:
            raise RegistryError("invalid or duplicate suite id")
        ids.add(identifier)
        if type(suite["statement"]) is not str or not suite["statement"].strip():
            raise RegistryError(f"{identifier}: missing statement")
        strings(suite["premises"], "premises")
        strings(suite["limits"], "limits")
        timeout = suite["timeout_seconds"]
        if type(timeout) is not int or not 1 <= timeout <= 60:
            raise RegistryError("timeout_seconds must be an integer from 1 to 60")
        document = suite["document"]
        document_data = pinned_source(root, document)
        if not document["path"].endswith(".md"):
            raise RegistryError("statement document must be Markdown")
        remember_source(snapshots, document["path"], document_data)
        if type(suite["sources"]) is not list or not 1 <= len(suite["sources"]) <= 16:
            raise RegistryError("suite must declare 1 to 16 executable sources")
        sources = {}
        for item in suite["sources"]:
            data = pinned_source(root, item)
            name = item["path"]
            if not name.endswith(".py") or name in sources:
                raise RegistryError("invalid or duplicate executable source")
            sources[name] = data
        entry = suite["entrypoint"]
        if type(entry) is not str or entry not in sources:
            raise RegistryError("entrypoint must be a declared executable source")
        closure = import_closure(root, entry, sources)
        if type(suite["stdlib_imports"]) is not list or suite["stdlib_imports"] != closure:
            raise RegistryError(
                f"{identifier}: stdlib_imports must equal the audited sorted imports"
            )
        if "unittest" not in closure:
            raise RegistryError("entrypoint must supply a unittest suite")
        for name, data in sources.items():
            remember_source(snapshots, name, data)
    return registry, snapshots


# Source is supplied through stdin, never interpolated into a shell or command.
# Explicit module loading runs the selected unittest suite, not repository discovery.
CHILD = r"""
import importlib.abc
import importlib.util
import io
import json
import os
import sys
import types
import unittest

packet = json.load(sys.stdin)
loaded = []
sources = packet["sources"]

def audit(event, args):
    if event == "open":
        mode, flags = args[1], args[2]
        if (isinstance(mode, str) and any(x in mode for x in "wax+")) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND)
        ):
            raise RuntimeError("research check file writes are disabled")
    if event in {"os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.link", "os.symlink",
                 "os.chmod", "os.chown", "os.truncate", "os.utime", "os.system",
                 "subprocess.Popen", "socket.__new__", "os.chdir"}:
        raise RuntimeError("research check mutation/network/process action is disabled")

sys.addaudithook(audit)

class SourceLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in sources:
            return importlib.util.spec_from_loader(fullname, self)
        return None
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        item = sources[module.__name__]
        module.__file__ = item["path"]
        loaded.append(item["path"])
        exec(compile(item["text"], item["path"], "exec"), module.__dict__)

loader = SourceLoader()
sys.meta_path.insert(0, loader)
stream = io.StringIO()
try:
    entry = types.ModuleType("registered_research_check")
    sys.modules[entry.__name__] = entry
    sources[entry.__name__] = packet["entry"]
    loader.exec_module(entry)
    suite = unittest.defaultTestLoader.loadTestsFromModule(entry)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    report = {"successful": result.wasSuccessful() and result.testsRun > 0
                           and not result.skipped and not result.expectedFailures,
              "tests_run": result.testsRun, "failures": len(result.failures),
              "errors": len(result.errors), "skipped": len(result.skipped),
              "expected_failures": len(result.expectedFailures),
              "executed_sources": sorted(set(loaded)), "test_output": stream.getvalue()}
except BaseException as exc:
    report = {"successful": False, "error": type(exc).__name__ + ": " + str(exc),
              "executed_sources": sorted(set(loaded)), "test_output": stream.getvalue()}
print(json.dumps(report, sort_keys=True))
"""


def changed_sources(root: Path, snapshots: dict[str, bytes]) -> list[str]:
    changed = []
    for name, expected in snapshots.items():
        try:
            if read_source(root, name) != expected:
                changed.append(name)
        except (OSError, RegistryError):
            changed.append(name)
    return sorted(changed)


def run_suite(root: Path, suite: dict, snapshots: dict[str, bytes], *, optimized=False) -> dict:
    names = [item["path"] for item in suite["sources"]]
    items = {
        name: {"path": str(root / name), "text": snapshots[name].decode("utf-8")} for name in names
    }
    packet = {
        "entry": items[suite["entrypoint"]],
        "sources": {
            Path(name).stem: item for name, item in items.items() if name != suite["entrypoint"]
        },
    }
    command = [sys.executable, "-I", "-S", "-B", *(["-O"] if optimized else []), "-c", CHILD]
    try:
        child = subprocess.run(
            command,
            input=json.dumps(packet),
            text=True,
            capture_output=True,
            cwd=root,
            timeout=suite["timeout_seconds"],
            check=False,
        )
        try:
            result = json.loads(child.stdout)
        except (ValueError, UnicodeError):
            result = {
                "successful": False,
                "error": "child returned invalid JSON",
                "stdout": child.stdout,
            }
        if type(result) is not dict:
            result = {"successful": False, "error": "child returned a non-object report"}
        result.update({"id": suite["id"], "returncode": child.returncode, "stderr": child.stderr})
        result["successful"] = result.get("successful") is True and child.returncode == 0
        declared = {item["path"] for item in items.values()}
        executed = result.get("executed_sources", [])
        if type(executed) is not list or any(type(name) is not str for name in executed):
            result["successful"] = False
            result["error"] = "child returned invalid executed-source inventory"
        elif not set(executed) <= declared:
            result["successful"] = False
            result["error"] = "child returned unregistered executed source"
        else:
            result["unexecuted_declared_sources"] = sorted(declared - set(executed))
            result["executed_source_identities"] = [
                {"path": name, "sha256": digest(snapshots[name])}
                for name in sorted(names)
                if str(root / name) in executed
            ]
    except subprocess.TimeoutExpired:
        result = {"id": suite["id"], "successful": False, "error": "suite timeout"}
    return result


def evaluate(root: Path, manifest: str, selected: list[str], *, optimized=False) -> dict:
    runner_before = Path(__file__).read_bytes()
    registry, snapshots = load_registry(root, manifest)
    by_id = {suite["id"]: suite for suite in registry["suites"]}
    if len(set(selected)) != len(selected) or any(name not in by_id for name in selected):
        raise RegistryError("selected ids must be unique registered suite ids")
    before_changes = changed_sources(root, snapshots)
    if before_changes:
        raise RegistryError(f"source changed during validation: {before_changes}")
    results = []
    for name in selected:
        if changed_sources(root, snapshots):
            break
        results.append(run_suite(root, by_id[name], snapshots, optimized=optimized))
    after_changes = changed_sources(root, snapshots)
    runner_changed = Path(__file__).read_bytes() != runner_before
    return {
        "schema_version": 1,
        "evidence_kind": registry["evidence_kind"],
        "successful": not after_changes
        and not runner_changed
        and len(results) == len(selected)
        and all(row["successful"] for row in results),
        "manifest": manifest,
        "manifest_sha256": digest(snapshots[manifest]),
        "source_identities": [
            {"path": name, "sha256": digest(data), "bytes": len(data)}
            for name, data in sorted(snapshots.items())
        ],
        "source_check_before": "matched",
        "source_changes_after": after_changes,
        "runtime": {
            "executable": sys.executable,
            "executable_sha256": digest(Path(sys.executable).read_bytes()),
            "python": sys.version,
            "implementation": sys.implementation.name,
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
            },
            "optimized_checks": optimized,
            "child_flags": ["-I", "-S", "-B"] + (["-O"] if optimized else []),
        },
        "runner_sha256": digest(runner_before),
        "runner_source_changed": runner_changed,
        "registered_suites": registry["suites"],
        "results": results,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="repository-relative manifest")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", help="list validated registrations (default)")
    mode.add_argument(
        "--check", action="store_true", help="check all identities/imports without execution"
    )
    mode.add_argument(
        "--suite", action="append", metavar="ID", help="run an explicit suite; repeatable"
    )
    mode.add_argument("--all", action="store_true", help="run every explicitly registered suite")
    parser.add_argument(
        "--optimized", action="store_true", help="execute selected checks with Python -O"
    )
    args = parser.parse_args(argv)
    try:
        selected = args.suite or []
        if args.all:
            registry, _ = load_registry(ROOT, args.manifest)
            selected = [suite["id"] for suite in registry["suites"]]
        report = evaluate(ROOT, args.manifest, selected, optimized=args.optimized)
        report["mode"] = "run" if selected else "check" if args.check else "list"
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["successful"] else 1
    except (RegistryError, OSError, UnicodeError) as exc:
        print(
            json.dumps(
                {
                    "schema_version": 1,
                    "successful": False,
                    "error": type(exc).__name__ + ": " + str(exc),
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
