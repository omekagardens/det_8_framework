"""Independent exact superoperator reference for bounded QR-02 comparisons.

The fixed QR-01 reference is imported from its SHA-verified source bytes.  No
QR-01 executor, QR-02 executor, or DET8 package is imported.  Its private exact
tuple arithmetic and superoperator composition are deliberately reused under
the source pin; QR-02's table/schema validation is independent of coarse.py.

Every supplied instrument is wrapped as one QR-01 event, which independently
checks exact completeness, dimensions, tensor support and rational bounds.
Source grouping sums maps rather than amplitudes.  All zero blocks survive.
The unrestricted mappings concern independently variable fine CQ input blocks;
the composed mappings concern all operator inputs to the stated source only.
"""

from __future__ import annotations

import hashlib
import importlib.util
import re
from fractions import Fraction
from pathlib import Path
from types import ModuleType

ComplexPair = tuple[Fraction, Fraction]
Matrix = tuple[tuple[ComplexPair, ...], ...]
Record = tuple[tuple[str, str], ...]
RecordMaps = dict[Record, Matrix]

QR01_REFERENCE_SHA256 = "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f"
QR01_REFERENCE_PATH = (
    Path(__file__).resolve().parent.parent / "qr-01-quantum-records-2026-09-05" / "reference.py"
)


def _load_qr01_reference() -> ModuleType:
    path = QR01_REFERENCE_PATH
    if not path.is_file() or path.is_symlink():
        raise ValueError("QR-02 independent reference requires a plain QR-01 source file")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != QR01_REFERENCE_SHA256:
        raise ValueError("QR-01 independent reference source SHA differs from the frozen pin")
    specification = importlib.util.spec_from_file_location("qr02_pinned_reference_qr01", path)
    if specification is None:
        raise ValueError("cannot construct the pinned QR-01 reference file import")
    module = importlib.util.module_from_spec(specification)
    # Compile the verified bytes, rather than asking a loader to reread the path.
    exec(compile(raw, str(path), "exec"), module.__dict__)  # noqa: S102
    return module


_QR01 = _load_qr01_reference()


def _keys(value: object, expected: set[str], context: str) -> dict:
    if type(value) is not dict or set(value) != expected:
        raise ValueError(f"QR-02 reference {context} must have exactly its specified keys")
    return value


def _label(value: object, context: str) -> str:
    if (
        type(value) is not str
        or not 1 <= len(value) <= 128
        or re.fullmatch(r"[A-Za-z0-9_+.-]{1,128}", value) is None
    ):
        raise ValueError(f"QR-02 reference {context} must match the bounded label grammar")
    return value


def _instrument(value: object, qubits: int) -> dict[str, Matrix]:
    instrument = _keys(value, {"support", "outcomes"}, "instrument")
    wrapper = {
        "schema_version": "det8-qr01-problem-v1",
        "qubits": qubits,
        "events": [
            {
                "event_id": "stage",
                "record_id": "stage",
                "support": instrument["support"],
                "outcomes": instrument["outcomes"],
            }
        ],
        "precedence": [],
    }
    outcomes = _QR01.reference_schedule(wrapper, ("stage",))
    return {record[0][1]: outcome_map for record, outcome_map in outcomes.items()}


def _table(value: object, key_name: str, expected: set[str], qubits: int) -> dict:
    if type(value) is not list or len(value) != len(expected):
        raise ValueError("QR-02 reference future table must cover its label inventory exactly")
    result = {}
    for item in value:
        row = _keys(item, {key_name, "instrument"}, "future-table row")
        key = _label(row[key_name], f"{key_name} future-table key")
        if key not in expected or key in result:
            raise ValueError("QR-02 reference future table has an unknown or duplicate label")
        result[key] = _instrument(row["instrument"], qubits)
    if set(result) != expected:
        raise ValueError("QR-02 reference future table omits a required label")
    return result


def _decode(wire: object) -> tuple[int, dict, dict, dict, dict, tuple[str, ...]]:
    data = _keys(
        wire,
        {"schema_version", "qubits", "source", "groups", "fine_future", "coarse_future"},
        "problem",
    )
    if type(data["schema_version"]) is not str or data["schema_version"] != "det8-qr02-problem-v1":
        raise ValueError("QR-02 reference schema version is unsupported")
    qubits = data["qubits"]
    if type(qubits) is not int or qubits not in (1, 2):
        raise ValueError("QR-02 reference accepts one or two qubits")
    source = _instrument(data["source"], qubits)
    fine_labels = set(source)
    entries = data["groups"]
    if type(entries) is not list or len(entries) != len(fine_labels):
        raise ValueError("QR-02 reference grouping must cover every source label exactly")
    groups = {}
    for item in entries:
        row = _keys(item, {"fine", "coarse"}, "group row")
        fine = _label(row["fine"], "fine group label")
        coarse = _label(row["coarse"], "coarse group label")
        if fine not in fine_labels or fine in groups:
            raise ValueError("QR-02 reference grouping has an unknown or duplicate fine label")
        groups[fine] = coarse
    if set(groups) != fine_labels:
        raise ValueError("QR-02 reference grouping omits a source outcome")
    coarse_labels = set(groups.values())
    fine_future = _table(data["fine_future"], "fine", fine_labels, qubits)
    coarse_future = _table(data["coarse_future"], "coarse", coarse_labels, qubits)
    first_fine = min(fine_labels)
    future_labels = set(fine_future[first_fine])
    for future in (*fine_future.values(), *coarse_future.values()):
        if set(future) != future_labels:
            raise ValueError("QR-02 reference future outcome-label inventories must all match")
    return qubits, source, groups, fine_future, coarse_future, tuple(sorted(future_labels))


def _zero_matrix(dimension: int) -> Matrix:
    return tuple(tuple(_QR01._ZERO for _ in range(dimension)) for _ in range(dimension))


def _sum_matrices(matrices: tuple[Matrix, ...], dimension: int) -> Matrix:
    result = _zero_matrix(dimension)
    for matrix in matrices:
        result = tuple(
            tuple(
                _QR01._plus(result[row][column], matrix[row][column]) for column in range(dimension)
            )
            for row in range(dimension)
        )
    return result


def reference_maps(wire: dict) -> dict[str, RecordMaps]:
    """Return six exact record-indexed maps under the QR-02 wire contract.

    ``source_fine`` and ``source_coarse`` contain the original and grouped
    source outcome maps.  ``fine_then_forget`` and ``forget_then_candidate``
    compare the two reachable routes and retain ``(coarse, future)`` records.
    ``unrestricted_fine_future`` and ``unrestricted_coarse_future`` contain
    F[x,y] and G[g(x),y] respectively, indexed by ``(fine, future)``.  They act
    on independently variable quantum blocks, not on the source input state.

    Every record key is a sorted tuple of literal slot-name/label pairs.
    Every value is a row-major d*d square superoperator made of Fraction pairs.
    No selected-state projection, normalization, Kraus compression, or pruning
    is used, and a grouped map is not mistaken for a two-Kraus input instrument.
    """
    qubits, source, groups, fine_future, coarse_future, future_labels = _decode(wire)
    operator_dimension = (1 << qubits) ** 2
    fine_labels = tuple(sorted(source))
    coarse_labels = tuple(sorted(set(groups.values())))

    grouped_source = {
        coarse: _sum_matrices(
            tuple(source[fine] for fine in fine_labels if groups[fine] == coarse),
            operator_dimension,
        )
        for coarse in coarse_labels
    }
    source_fine = {(("fine", fine),): source[fine] for fine in fine_labels}
    source_coarse = {(("coarse", coarse),): grouped_source[coarse] for coarse in coarse_labels}
    fine_then_forget = {}
    forget_then_candidate = {}
    for coarse in coarse_labels:
        for future in future_labels:
            key = (("coarse", coarse), ("future", future))
            fine_then_forget[key] = _sum_matrices(
                tuple(
                    _QR01._compose(fine_future[fine][future], source[fine])
                    for fine in fine_labels
                    if groups[fine] == coarse
                ),
                operator_dimension,
            )
            forget_then_candidate[key] = _QR01._compose(
                coarse_future[coarse][future], grouped_source[coarse]
            )
    unrestricted_fine_future = {}
    unrestricted_coarse_future = {}
    for fine in fine_labels:
        for future in future_labels:
            key = (("fine", fine), ("future", future))
            unrestricted_fine_future[key] = fine_future[fine][future]
            unrestricted_coarse_future[key] = coarse_future[groups[fine]][future]
    return {
        "source_fine": source_fine,
        "source_coarse": source_coarse,
        "fine_then_forget": fine_then_forget,
        "forget_then_candidate": forget_then_candidate,
        "unrestricted_fine_future": unrestricted_fine_future,
        "unrestricted_coarse_future": unrestricted_coarse_future,
    }
