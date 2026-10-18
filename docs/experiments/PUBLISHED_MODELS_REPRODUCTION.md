# Reproduce the two published small models

14 September 2026 UTC. RI-27 is a coordinator reproducibility companion to
[qubit/record RI-25](qubit_record_v1/EXPERIMENT.md) and
[supplied-geometry observer RI-26](observer_signal_v1/EXPERIMENT.md).
It changes neither model. The recipe extracts their published source into a
new temporary directory, checks its identities and exact file set, then runs
each bundle in its own isolated Python process. No unpublished core/RET
files, installed DET package or development dependencies are needed.

## Source and inventory

The [separate manifest](published_models_v1.json) contains exactly **23 files**:
RI-25's twelve files and RI-26's eleven files. Every digest was checked against
its accepted identity and the actual file blob in published commit
[2529bfd20e9dca88d58e891cb0e679f42bb67f54](https://github.com/omekagardens/det_8_framework/commit/2529bfd20e9dca88d58e891cb0e679f42bb67f54),
tree `1b6c9a34aecc20e7824d08b90a3d6e5b9d191051`.
The manifest SHA256 is
`e032fbac46cab28fd54cc49d94bf45958033500b24ca83f1b5acebeef5949915`.

Use the existing [read-only checker](../../scripts/check_review_snapshot.py),
whose separate accepted SHA256 is
`73cdb6bbe4754818736968b75ee3b84936750da22f21d881afdd09559202124e`.
The recipe checks that identity before running it. The checker is not one
of the 23 experiment files; the guide and manifest do not hash themselves.
The historical [RI-24 inventory](../coordination/REVIEW_SNAPSHOT.md) of
71 different accepted files and its checker remain unchanged. This is an
explicit new collection, not a refresh of historical expected digests.

A valid inventory match reports 23 declared, checked and matched files with
`executed_files: 0`. It establishes supplied byte agreement, not authentication,
an atomic capture, an import closure or a proof. Obtain this guide, manifest
and checker from a publication you trust. The declared checkpoint is checked
against git during construction; the runtime checker merely echoes it.
Its exit codes remain 0 for match, 1 for artifact mismatch/unreadability and
2 for invalid manifest/root. See its guide for the bounded-read/path contract.

## Clean extraction and replay

Start at the root of a published checkout containing this guide and manifest,
with the source commit object above available to `git archive`. Use an existing
**Python 3.11 or later** interpreter. Set `det_python` to its executable path
if `python3` on your PATH is older. No virtual environment is required.
The published exact-output evidence was obtained with **Python 3.11.6**;
record the version you use rather than assuming every future runtime has
identical output. The commands below are for a POSIX shell with git and tar.

The archive contains only the two complete bundle directories and the unchanged
checker. The copied manifest makes 25 regular files in the source directory.
The preflight refuses a different file set before running tests. This matters:
the integrity checker alone does not reject extra files, and both test runners
discover every sibling `test_*.py`. The two bundles also share module names,
so keep their supplied CLI invocations in separate processes.

The four worked runs use distinct new output directories outside the extracted
source. Their existing guards refuse nonempty destinations or output inside
the source root. Do not flatten the `docs/experiments/<bundle>/` layout.
The subset archive is an execution handoff; some scientific-document links
refer to material in the complete published repository outside that subset.

```sh
(
set -eu
det_python=python3
"$det_python" --version
det_repro=$(mktemp -d "${TMPDIR:-/tmp}/det-published-models.XXXXXX")
printf 'Reproduction artifacts: %s\n' "$det_repro"
mkdir "$det_repro/source"
git archive --format=tar --output="$det_repro/source.tar" \
  2529bfd20e9dca88d58e891cb0e679f42bb67f54 -- \
  docs/experiments/qubit_record_v1 \
  docs/experiments/observer_signal_v1 \
  scripts/check_review_snapshot.py
tar -xf "$det_repro/source.tar" -C "$det_repro/source"
cp docs/experiments/published_models_v1.json "$det_repro/source/docs/experiments/"

"$det_python" -I -S -B - "$det_repro/source" <<'PY'
from pathlib import Path
import hashlib
import json
import sys

if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11 or later is required")
root = Path(sys.argv[1])
manifest_name = "docs/experiments/published_models_v1.json"
checker_name = "scripts/check_review_snapshot.py"
pins = {
    manifest_name: "e032fbac46cab28fd54cc49d94bf45958033500b24ca83f1b5acebeef5949915",
    checker_name: "73cdb6bbe4754818736968b75ee3b84936750da22f21d881afdd09559202124e",
}
for name, expected in pins.items():
    if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
        raise SystemExit("Unexpected publication identity: " + name)
manifest = json.loads((root / manifest_name).read_text())
expected_paths = {row["path"] for row in manifest["artifacts"]} | set(pins)
paths = list(root.rglob("*"))
if any(path.is_symlink() for path in paths):
    raise SystemExit("The extracted source must not contain symlinks")
actual_paths = {path.relative_to(root).as_posix() for path in paths if not path.is_dir()}
if actual_paths != expected_paths or any(not (root / name).is_file() for name in actual_paths):
    raise SystemExit("Unexpected extracted file set")
print("Publication identities and exact 25-file source set match")
PY

"$det_python" -I -S -B "$det_repro/source/scripts/check_review_snapshot.py" \
  --manifest docs/experiments/published_models_v1.json > "$det_repro/integrity-before.json"

"$det_python" -I -S -B "$det_repro/source/docs/experiments/qubit_record_v1/run_checks.py"
"$det_python" -I -S -B -O "$det_repro/source/docs/experiments/qubit_record_v1/run_checks.py"
"$det_python" -I -S -B "$det_repro/source/docs/experiments/observer_signal_v1/run_checks.py"
"$det_python" -I -S -B -O "$det_repro/source/docs/experiments/observer_signal_v1/run_checks.py"

"$det_python" -I -S -B "$det_repro/source/docs/experiments/qubit_record_v1/worked_example.py" \
  --seed 20260914 --output "$det_repro/qubit-normal" > "$det_repro/qubit-normal-cli.json"
"$det_python" -I -S -B -O "$det_repro/source/docs/experiments/qubit_record_v1/worked_example.py" \
  --seed 20260914 --output "$det_repro/qubit-optimized" > "$det_repro/qubit-optimized-cli.json"
"$det_python" -I -S -B "$det_repro/source/docs/experiments/observer_signal_v1/worked_example.py" \
  --output "$det_repro/observer-normal" > "$det_repro/observer-normal-cli.json"
"$det_python" -I -S -B -O "$det_repro/source/docs/experiments/observer_signal_v1/worked_example.py" \
  --output "$det_repro/observer-optimized" > "$det_repro/observer-optimized-cli.json"

"$det_python" -I -S -B - "$det_repro" <<'PY'
from pathlib import Path
import hashlib
import sys

root = Path(sys.argv[1])
expected = {
    "qubit": (12, "72aca957a52cf5fc1024fdd4773ca5a6172280de9de2229bf1bf389d8d0084bb"),
    "observer": (52, "80a646f5dd007ba6a9d64f9ffd6dec7c3c4bb5a1a8d4974fa31c335545ac28a8"),
}
for name, (count, summary_pin) in expected.items():
    def files(mode):
        base = root / (name + "-" + mode)
        return {p.relative_to(base).as_posix(): p.read_bytes() for p in base.rglob("*") if p.is_file()}
    normal, optimized = files("normal"), files("optimized")
    if len(normal) != count or normal != optimized:
        raise SystemExit("Export count or normal/optimized byte mismatch: " + name)
    actual = hashlib.sha256(normal["summary.json"]).hexdigest()
    if actual != summary_pin:
        raise SystemExit("Published summary differs on this runtime: " + name + " " + actual)
    print(name, count, "exports match; summary SHA256", actual)
PY

"$det_python" -I -S -B -O "$det_repro/source/scripts/check_review_snapshot.py" \
  --manifest docs/experiments/published_models_v1.json > "$det_repro/integrity-after.json"
)
```

`set -e` stops this subshell on a failed command. Keep the printed directory
and reports if a mismatch needs investigation; this recipe performs no cleanup.
Compare exported relative paths and bytes, not worked CLI stdout (which names
different directories) or unittest timing text. The fixed summary pins describe
the recorded default runs. A mismatch is a reproduction finding to investigate,
not permission to replace accepted source or expected hashes.

## Expected result and limits

| Bundle | Tests in each mode | Export files in each mode | Default retained data |
|---|---:|---:|---|
| Qubit/record | 61 | 12 | 4,608 training attempts, 372 erased; 1,536 held W attempts, 119 erased. |
| Supplied observers | 51 | 52 | Ten fixtures; 11 emissions, eight receptions, 20 local closures. |

The two modes replay the same test sets. They add no new registered witnesses.
The historical 82 qubit and 331 observer coordinator export-audit assertions
are separate review evidence in [progress](../coordination/REVIEW_PROGRESS.md);
this recipe does not claim to rerun those temporary audit programs. Its export
comparison checks relative-path/byte equality and the two summary file hashes.
Source integrity checks before and after do not constitute an atomic snapshot
or prove which files an arbitrary program executed. Keep the extracted source
quiet during the run; this is not a hostile-filesystem sandbox.

The qubit model adopts ordinary qubit/Born/Lüders physics and a calibrated
measurement interface. Its conventional same-data estimate is identical by
construction; the default phase-pair W bands overlap. Measured W acquisition
and justified calibration/drift remain open. The observer model supplies its
geometry, ideal clocks and propagation law; it does not derive geometry or
supply an actualization feedback equation. Reproduction establishes the
published simulation/accounting behavior within those declared contracts.
The [data and follow-up note](../coordination/QUBIT_DATA_AND_FOLLOWUP.md)
retains the experimental and application prerequisites.


## Performed coordinator validation

The coordinator executed the extraction, identity/file-set checks, four test
commands and four worked commands with Python 3.11.6 in a fresh external
archive. Qubit tests passed 61 in each mode (0.642/0.651 s); observer tests
passed 51 in each mode (0.048/0.045 s). All twelve qubit and 52 observer
exports matched between modes, including both published summary hashes.
The before/after integrity reports were identical: 23 declared, checked and
matched files, zero artifact execution by the integrity checker.

A separate post-run inspection confirmed the exact 25-file source set and
every source hash unchanged, with no `.git`, `.venv`, `det8` package or extra
test files in that source directory. Independent inventory, packaging and
recipe reviews found no blocker. The output-directory line is printed at
creation so a later failure still leaves its location visible. Generated
archives, logs and data remained outside the project. These are replay and
packaging results; the two accepted scientific contracts are unchanged.
