"""Exact structural identifiability of a linear functional on unrestricted R^n.

Rows and targets are supplied rational model coefficients, not observed data.
Certificates concern the mean map H theta and q theta. They make no claim of
finite-sample certainty, feasibility, parameter constraints or model selection.
See docs/coordination/IDENTIFIABILITY_CONTRACT.md for the theorem and limits.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from fractions import Fraction

MAX_DESIGN_ROWS = 32
MAX_PARAMETERS = 8
MAX_CANDIDATES = 16
MAX_COEFFICIENT_BITS = 64
MAX_LABEL_LENGTH = 128

ExactScalar = int | Fraction
RationalRow = tuple[Fraction, ...]
RationalDesign = tuple[RationalRow, ...]


@dataclass(frozen=True, slots=True)
class LinearCertificate:
    """Detached coefficients and an exactly checkable row-space/nullspace witness.

    Coordinates retain their supplied positional order theta[0], ..., theta[n-1].
    Identified: row_weights^T design = target. Otherwise: design null_direction
    = 0 and target dot null_direction = 1. Exactly one witness is present.
    """

    design: RationalDesign
    target: RationalRow
    n_rows: int
    n_parameters: int
    rank: int
    identified: bool
    row_weights: RationalRow | None
    null_direction: RationalRow | None


@dataclass(frozen=True, slots=True)
class CandidateAnalysis:
    """One supplied available row, without a feasibility or cost/ranking claim.

    Separation concerns the base certificate's displayed pair only. The
    certificate independently answers identification after appending this row
    alone. If the base target is identified, there is no displayed pair and
    both separation fields are None.
    """

    label: str
    row: RationalRow
    separation: Fraction | None
    separates_displayed_pair: bool | None
    certificate: LinearCertificate


@dataclass(frozen=True, slots=True)
class IdentifiabilityAnalysis(LinearCertificate):
    """Base certificate and candidate analyses in supplied order, without ranking."""

    candidates: tuple[CandidateAnalysis, ...]


def _bounded_items(values, limit: int, name: str) -> tuple:
    """Materialize a supplied iterable once, reading at most limit+1 entries."""
    if isinstance(values, (str, bytes, bytearray, Mapping)):
        raise TypeError(f"{name} must be an iterable of entries, not text or a mapping")
    try:
        iterator = iter(values)
    except TypeError as exc:
        raise TypeError(f"{name} must be iterable") from exc
    entries = []
    for _ in range(limit + 1):
        try:
            entries.append(next(iterator))
        except StopIteration:
            break
    result = tuple(entries)
    if len(result) > limit:
        raise ValueError(f"{name} exceeds the limit of {limit} entries")
    return result


def _coefficient(value, name: str) -> Fraction:
    if type(value) not in (int, Fraction):
        raise TypeError(f"{name} must be a built-in int or fractions.Fraction")
    numerator, denominator = (value, 1) if type(value) is int else (value.numerator, value.denominator)
    if max(numerator.bit_length(), denominator.bit_length()) > MAX_COEFFICIENT_BITS:
        raise ValueError(f"{name} exceeds the {MAX_COEFFICIENT_BITS}-bit coefficient limit")
    return Fraction(numerator, denominator)


def _row(values, n: int, name: str) -> RationalRow:
    entries = _bounded_items(values, n, name)
    if len(entries) != n:
        raise ValueError(f"{name} must have exactly {n} coefficients")
    return tuple(_coefficient(value, name) for value in entries)


def _certificate(design: RationalDesign, target: RationalRow) -> LinearCertificate:
    """Rational RREF with tracked row operations; no numeric tolerance or prior."""
    m, n = len(design), len(target)
    matrix = [list(row) for row in design]
    transform = [[Fraction(i == j) for j in range(m)] for i in range(m)]
    pivots = []
    for column in range(n):
        rank = len(pivots)
        pivot = next((row for row in range(rank, m) if matrix[row][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        transform[rank], transform[pivot] = transform[pivot], transform[rank]
        divisor = matrix[rank][column]
        matrix[rank] = [value / divisor for value in matrix[rank]]
        transform[rank] = [value / divisor for value in transform[rank]]
        for row in range(m):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [a - factor * b for a, b in zip(matrix[row], matrix[rank])]
            transform[row] = [a - factor * b for a, b in zip(transform[row], transform[rank])]
        pivots.append(column)

    residual = list(target)
    weights = [Fraction(0)] * m
    for row, column in enumerate(pivots):
        factor = residual[column]
        residual = [a - factor * b for a, b in zip(residual, matrix[row])]
        weights = [a + factor * b for a, b in zip(weights, transform[row])]
    free = next((column for column, value in enumerate(residual) if value != 0), None)
    if free is None:
        return LinearCertificate(design, target, m, n, len(pivots), True, tuple(weights), None)

    # The residual has zero pivot entries. Set one free coordinate, then solve
    # the pivot coordinates. Scaling fixes q delta = 1 exactly.
    direction = [Fraction(0)] * n
    direction[free] = 1 / residual[free]
    for row, column in enumerate(pivots):
        direction[column] = -matrix[row][free] / residual[free]
    return LinearCertificate(design, target, m, n, len(pivots), False, None, tuple(direction))


def analyze_identifiability(
    design: Iterable[Iterable[ExactScalar]],
    target: Iterable[ExactScalar],
    candidates: Iterable[tuple[str, Iterable[ExactScalar]]] = (),
) -> IdentifiabilityAnalysis:
    """Certify identification of target dot theta from design theta on R^n.

    Only exact built-in int/Fraction coefficients are accepted. Target must be
    nonempty; design may be empty. Each candidate is (unique nonblank label,
    single row), analyzed separately. Input limits apply before elimination;
    candidate certificates can contain MAX_DESIGN_ROWS+1 rows. Derived exact
    fractions are not restricted to the input coefficient bit limit.

    Type violations raise TypeError. Shape, size, label and coefficient-limit
    violations raise ValueError. Inputs are detached and results immutable.
    All containers are consumed once with bounded materialization.
    """
    raw_target = _bounded_items(target, MAX_PARAMETERS, "target")
    if not raw_target:
        raise ValueError("target must contain at least one coefficient")
    target = tuple(_coefficient(value, "target coefficient") for value in raw_target)
    n = len(target)
    raw_design = _bounded_items(design, MAX_DESIGN_ROWS, "design")
    design = tuple(_row(row, n, "design row") for row in raw_design)

    raw_candidates = _bounded_items(candidates, MAX_CANDIDATES, "candidates")
    supplied = []
    labels = set()
    for candidate in raw_candidates:
        entries = _bounded_items(candidate, 2, "candidate")
        if len(entries) != 2:
            raise ValueError("each candidate must contain a label and one row")
        label, row = entries
        if type(label) is not str:
            raise TypeError("candidate label must be a built-in str")
        if len(label) > MAX_LABEL_LENGTH or not label.strip():
            raise ValueError(f"candidate label must be nonblank and at most {MAX_LABEL_LENGTH} characters")
        if label in labels:
            raise ValueError("candidate labels must be unique")
        labels.add(label)
        supplied.append((label, _row(row, n, "candidate row")))

    base = _certificate(design, target)
    analyses = []
    for label, row in supplied:
        separation = (sum((a * b for a, b in zip(row, base.null_direction)), Fraction(0))
                      if base.null_direction is not None else None)
        analyses.append(CandidateAnalysis(
            label, row, separation, separation != 0 if separation is not None else None,
            _certificate(design + (row,), target),
        ))
    return IdentifiabilityAnalysis(
        base.design, base.target, base.n_rows, base.n_parameters, base.rank,
        base.identified, base.row_weights, base.null_direction, tuple(analyses),
    )
