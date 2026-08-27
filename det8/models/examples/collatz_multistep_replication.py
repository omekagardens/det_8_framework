"""Multistep Collatz revision and locked higher-band transport evaluation.

Revision is confined to starts below ``2**20``.  The mechanistic null applies
the exact shortcut map

    S(x) = x/2              (x even)
           (3*x + 1)/2      (x odd)

for ten steps.  If ``C_k = k + number_of_odd_shortcut_steps``, then exactly
``tau(n) = C_k + tau(S**k(n))`` on the modeled ranges (whose prefixes are
audited not to reach one early).  A saturated residue lookup, equivalently a
saturated parity-signature lookup because the two encodings are bijective, is kept
as a control, not promoted as a discovery candidate.  The compressed
candidate uses position-specific additive parity terms and adjacent-parity
interactions.  Its parameters are fit using starts below ``2**20`` and then
transported without refitting to ``[2**20,2**21)`` and ``[2**21,2**22)``.
Those bands were first accessed during integration before the final manifest
was persisted, so the module does not count them as historically fresh RG2
replications.

The arithmetic census and statistical comparison remain separate.  The
former is a bounded exact computation, not a proof of the global conjecture
or an independently replayable formal certificate.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from array import array
from dataclasses import dataclass
from pathlib import Path

from det8.models.relational_evidence import (
    EvidenceLedger,
    EvidenceRecord,
    StudentT,
    evidence_payload_digest,
)


EXACT_LIMIT = 1 << 22
EXACT_CHECKPOINT_SIZE = 1 << 18
REVISION_FIT_RANGE = (1 << 18, 1 << 19)
REVISION_SELECTION_RANGE = (1 << 19, 1 << 20)
REVISION_ALL_RANGE = (1 << 18, 1 << 20)
FRESH_BANDS = ((1 << 20, 1 << 21), (1 << 21, 1 << 22))
SHORTCUT_DEPTH = 10
DEPTH_SENSITIVITY_PANEL = (4, 6, 8, 10, 12, 14, 16)
GROUP_SHRINKAGE = 32.0
SCORE_BLOCK_SIZE = 1 << 14
STUDENT_T_DF = 5.0
NORMAL_EQUATION_RIDGE = 1.0e-8
MINIMUM_MEAN_LOG_SCORE_GAIN = 0.02
MINIMUM_CANDIDATE_OVER_SATURATED_GAIN = -0.02
HAC_LAG = 4
MAXIMUM_SINGLE_BLOCK_POSITIVE_GAIN_SHARE = 0.20
T50 = 0.7266868438004227
T80 = 1.4758840488558216
T95 = 2.570581835636305
T99 = 4.032142983557536

# The two evaluation bands were predeclared and were never used to fit or
# select the candidate.  During integration, however, they were executed
# before a final protocol manifest had been persisted.  They therefore remain
# locked transport evaluations, not historically fresh RG2 replications.
FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS = False

PROOF_WARNING = (
    "Convergence was computed with exact integer arithmetic only through the "
    "reported finite frontier. This is not a proof of the Collatz conjecture "
    "and the checkpoint hashes are not an independently replayable certificate."
)
REPLICATION_WARNING = (
    "Each dyadic evaluation band could count as at most one replication. "
    "Here the final manifest did not predate first band access, the candidate "
    "failed its consumed-data gate, and no calibrated open model exists. "
    "Internal score blocks describe stability; they are not independent "
    "replications or a calibrated posterior probability."
)

DIAGNOSTIC_THRESHOLDS = {
    "maximum_absolute_bias_in_revision_sd": 0.10,
    "minimum_central_50_coverage": 0.42,
    "maximum_central_50_coverage": 0.58,
    "minimum_central_80_coverage": 0.72,
    "maximum_central_80_coverage": 0.88,
    "minimum_central_95_coverage": 0.90,
    "maximum_central_95_coverage": 0.98,
    "minimum_central_99_coverage": 0.97,
    "maximum_central_99_coverage": 0.9995,
    "maximum_absolute_height_slope_in_revision_sd": 0.25,
    "minimum_positive_score_block_fraction": 0.75,
}


def shortcut_step(value: int) -> tuple[int, int]:
    """Return one shortcut-map step and its exact ordinary-map toll."""

    if value < 1:
        raise ValueError("shortcut Collatz input must be positive")
    if value & 1:
        return (3 * value + 1) // 2, 2
    return value // 2, 1


def shortcut_signature(value: int, depth: int) -> dict[str, object]:
    """Return terminal, exact toll, and parity word for ``depth`` steps.

    The integer encoding of the parity word is *not* generally numerically
    equal to ``value % 2**depth``.  Across a complete residue system, however,
    the shortcut parity words and residues are in one-to-one correspondence.
    """

    if value < 1 or depth < 1:
        raise ValueError("shortcut signature requires positive value and depth")
    current = value
    bits: list[int] = []
    toll = 0
    reached_one_before_depth = False
    for index in range(depth):
        if current == 1 and index < depth:
            reached_one_before_depth = True
        bit = current & 1
        bits.append(bit)
        current, increment = shortcut_step(current)
        toll += increment
    signature = sum(bit << index for index, bit in enumerate(bits))
    return {
        "terminal": current,
        "ordinary_toll": toll,
        "parity_bits": tuple(bits),
        "signature": signature,
        "residue": value % (1 << depth),
        "reached_one_before_depth": reached_one_before_depth,
    }


def shortcut_bijection_audit(depth: int) -> dict[str, object]:
    """Exhaustively verify the parity-word/residue bijection at one depth."""

    if depth < 1:
        raise ValueError("shortcut bijection audit requires positive depth")
    modulus = 1 << depth
    signatures: dict[int, int] = {}
    collisions: list[tuple[int, int, int]] = []
    hasher = hashlib.sha256()
    for residue in range(modulus):
        # 2**depth is the positive representative of residue zero.  Shortcut
        # parities through this depth depend only on the residue class.
        representative = residue if residue else modulus
        parity_code = int(shortcut_signature(representative, depth)["signature"])
        previous = signatures.get(parity_code)
        if previous is not None:
            collisions.append((parity_code, previous, residue))
        else:
            signatures[parity_code] = residue
        hasher.update(f"{residue}:{parity_code};".encode("ascii"))
    return {
        "depth": depth,
        "residue_count": modulus,
        "distinct_parity_word_count": len(signatures),
        "is_bijection": len(signatures) == modulus and not collisions,
        "collision_examples": tuple(collisions[:8]),
        "mapping_digest": hasher.hexdigest(),
        "numerical_equality_claimed": False,
    }


def _model_signature(value: int, depth: int) -> dict[str, object]:
    """Return a prefix whose stopping-time decomposition is unambiguous."""

    signature = shortcut_signature(value, depth)
    if bool(signature["reached_one_before_depth"]):
        raise RuntimeError(
            f"shortcut prefix for modeled start {value} reaches one before depth {depth}"
        )
    return signature


def _candidate_features(signature: dict[str, object]) -> tuple[float, ...]:
    bits = tuple(int(value) for value in signature["parity_bits"])
    # Starts in the statistical bands are odd, so bit 0 is constant.  Omitting
    # it and its duplicate first interaction keeps the design full-rank.
    additive = tuple(float(bits[index]) for index in range(1, len(bits)))
    adjacent = tuple(
        float(bits[index] * bits[index + 1])
        for index in range(1, len(bits) - 1)
    )
    return (
        1.0,
        math.log2(int(signature["terminal"])),
        *additive,
        *adjacent,
    )


def _null_features(signature: dict[str, object]) -> tuple[float, float]:
    return (1.0, math.log2(int(signature["terminal"])))


class _NormalEquations:
    def __init__(
        self, dimension: int, ridge: float = NORMAL_EQUATION_RIDGE
    ) -> None:
        self.dimension = dimension
        self.ridge = ridge
        self.matrix = [[0.0] * dimension for _ in range(dimension)]
        self.vector = [0.0] * dimension
        self.count = 0

    def add(self, features: tuple[float, ...], target: float) -> None:
        if len(features) != self.dimension:
            raise ValueError("regression feature dimension changed")
        self.count += 1
        for row, value in enumerate(features):
            self.vector[row] += value * target
            for column in range(row, self.dimension):
                self.matrix[row][column] += value * features[column]

    def solve(self) -> tuple[float, ...]:
        matrix = [row[:] for row in self.matrix]
        for row in range(self.dimension):
            for column in range(row):
                matrix[row][column] = matrix[column][row]
            matrix[row][row] += self.ridge
        augmented = [
            matrix[row] + [self.vector[row]] for row in range(self.dimension)
        ]
        for column in range(self.dimension):
            pivot_row = max(
                range(column, self.dimension),
                key=lambda row: abs(augmented[row][column]),
            )
            augmented[column], augmented[pivot_row] = (
                augmented[pivot_row], augmented[column]
            )
            pivot = augmented[column][column]
            if abs(pivot) < 1.0e-14:
                raise RuntimeError("compressed parity design is singular")
            for index in range(column, self.dimension + 1):
                augmented[column][index] /= pivot
            for row in range(self.dimension):
                if row == column:
                    continue
                multiplier = augmented[row][column]
                if multiplier == 0.0:
                    continue
                for index in range(column, self.dimension + 1):
                    augmented[row][index] -= multiplier * augmented[column][index]
        return tuple(augmented[row][-1] for row in range(self.dimension))


def _dot(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _require_resolved_value(state: _ExactState, value: int) -> None:
    if value < 1 or value >= len(state.status):
        raise ValueError(f"modeled start {value} is outside the exact state")
    if state.status[value] != 1 or state.steps[value] < 0:
        raise RuntimeError(
            f"modeled start {value} is unresolved and cannot enter statistics"
        )


def _student_scale(variance: float) -> float:
    return math.sqrt(max(variance, 1.0e-12) * (STUDENT_T_DF - 2.0) / STUDENT_T_DF)


@dataclass
class _ExactState:
    steps: array
    peaks: array
    status: bytearray


def _ordinary_next(value: int) -> int:
    return value // 2 if value % 2 == 0 else 3 * value + 1


def _direct_ordinary(start: int, limit: int = 100_000) -> dict[str, object]:
    current = start
    steps = 0
    peak = start
    seen: set[int] = set()
    while current != 1 and steps < limit:
        if current in seen:
            return {"status": "verified_cycle", "steps": steps, "peak": peak}
        seen.add(current)
        current = _ordinary_next(current)
        steps += 1
        peak = max(peak, current)
    return {
        "status": "reached_one" if current == 1 else "resource_limit",
        "steps": steps,
        "peak": peak,
        "terminal": current,
    }


def _direct_shortcut(start: int, limit: int = 100_000) -> dict[str, object]:
    current = start
    shortcut_steps = 0
    ordinary_toll = 0
    peak = start
    seen: set[int] = set()
    while current != 1 and shortcut_steps < limit:
        if current in seen:
            return {
                "status": "verified_cycle",
                "shortcut_steps": shortcut_steps,
                "ordinary_toll": ordinary_toll,
                "peak": peak,
            }
        seen.add(current)
        if current & 1:
            expanded = 3 * current + 1
            peak = max(peak, expanded)
            current = expanded // 2
            ordinary_toll += 2
        else:
            current //= 2
            ordinary_toll += 1
        shortcut_steps += 1
    return {
        "status": "reached_one" if current == 1 else "resource_limit",
        "shortcut_steps": shortcut_steps,
        "ordinary_toll": ordinary_toll,
        "peak": peak,
        "terminal": current,
    }


def exact_frontier_through_2pow22(
    limit: int = EXACT_LIMIT,
    checkpoint_size: int = EXACT_CHECKPOINT_SIZE,
    max_descent_steps: int = 10_000,
) -> tuple[dict[str, object], _ExactState]:
    """Compute a lean ascending exact frontier with hash-chained checkpoints."""

    if limit < 1 or checkpoint_size < 1 or max_descent_steps < 1:
        raise ValueError("exact frontier arguments must be positive")
    started = time.perf_counter()
    steps = array("i", [-1]) * (limit + 1)
    peaks = array("Q", [0]) * (limit + 1)
    status = bytearray(limit + 1)
    steps[1], peaks[1], status[1] = 0, 1, 1
    counts = {"reached_one": 0, "resource_limit": 0, "verified_cycle": 0}
    exceptions: list[dict[str, object]] = []
    record_starts: set[int] = {1}
    global_steps_record = -1
    global_steps_start = 1
    global_peak_record = -1
    global_peak_start = 1
    checkpoints = []
    chain = hashlib.sha256(
        f"collatz-multistep-v1:{limit}:{checkpoint_size}".encode("ascii")
    ).hexdigest()
    block_hash = hashlib.sha256()
    block_start = 1
    block_counts = {name: 0 for name in counts}
    block_steps_record = -1
    block_steps_start = 1
    block_peak_record = -1
    block_peak_start = 1

    for start in range(1, limit + 1):
        if start == 1:
            outcome, total_steps, peak, merge, descent = "reached_one", 0, 1, 1, 0
        else:
            current = start
            path: list[int] = []
            seen: set[int] = set()
            outcome = "reached_one"
            while current >= start:
                if current in seen:
                    outcome = "verified_cycle"
                    break
                if len(path) >= max_descent_steps:
                    outcome = "resource_limit"
                    break
                seen.add(current)
                path.append(current)
                current = _ordinary_next(current)
            merge = current
            descent = len(path)
            if outcome == "reached_one" and status[current] != 1:
                # A deliberately resource-limited run inherits the already
                # classified lower trajectory rather than mislabeling it.
                outcome = (
                    "verified_cycle" if status[current] == 3 else "resource_limit"
                )
            if outcome == "reached_one" and status[current] == 1:
                total_steps = descent + int(steps[current])
                peak = max(max(path, default=start), int(peaks[current]))
                steps[start], peaks[start], status[start] = total_steps, peak, 1
            else:
                total_steps = -1
                peak = max(max(path, default=start), current)
                code = 2 if outcome == "resource_limit" else 3
                steps[start], peaks[start], status[start] = total_steps, peak, code
                exceptions.append(
                    {"start": start, "status": outcome, "terminal": current}
                )
        counts[outcome] += 1
        block_counts[outcome] += 1
        if outcome == "reached_one":
            if total_steps > global_steps_record:
                global_steps_record, global_steps_start = total_steps, start
                record_starts.add(start)
            if peak > global_peak_record:
                global_peak_record, global_peak_start = peak, start
                record_starts.add(start)
            if total_steps > block_steps_record:
                block_steps_record, block_steps_start = total_steps, start
            if peak > block_peak_record:
                block_peak_record, block_peak_start = peak, start
        block_hash.update(
            f"{start}:{outcome}:{total_steps}:{peak}:{merge}:{descent};".encode(
                "ascii"
            )
        )
        if start % checkpoint_size == 0 or start == limit:
            digest = block_hash.hexdigest()
            chain = hashlib.sha256(
                f"{chain}:{block_start}:{start}:{digest}".encode("ascii")
            ).hexdigest()
            checkpoints.append(
                {
                    "range": (block_start, start),
                    "status_counts": dict(block_counts),
                    "maximum_total_stopping_time": block_steps_record,
                    "maximum_total_stopping_time_start": block_steps_start,
                    "maximum_peak": block_peak_record,
                    "maximum_peak_start": block_peak_start,
                    "block_sha256": digest,
                    "chain_sha256": chain,
                }
            )
            block_hash = hashlib.sha256()
            block_start = start + 1
            block_counts = {name: 0 for name in counts}
            block_steps_record = block_peak_record = -1

    # Exact shortcut/ordinary toll identity for every start, using a second
    # ascending recurrence.  This is an internal cross-check, not a second
    # independent implementation.
    shortcut_toll = array("i", [-1]) * (limit + 1)
    shortcut_toll[1] = 0
    identity_failures = []
    identity_unresolved = []
    for start in range(2, limit + 1):
        if status[start] != 1 or steps[start] < 0:
            identity_unresolved.append(start)
            continue
        current = start
        local_toll = 0
        seen: set[int] = set()
        while current >= start and len(seen) < max_descent_steps:
            if current in seen:
                break
            seen.add(current)
            current, increment = shortcut_step(current)
            local_toll += increment
        if current < start and shortcut_toll[current] >= 0:
            shortcut_toll[start] = local_toll + shortcut_toll[current]
        if shortcut_toll[start] < 0:
            identity_unresolved.append(start)
        elif shortcut_toll[start] != steps[start]:
            identity_failures.append(start)
            if len(identity_failures) >= 20:
                break
    del shortcut_toll

    audits = []
    for start in sorted(record_starts | {int(row["start"]) for row in exceptions}):
        ordinary = _direct_ordinary(start)
        shortcut = _direct_shortcut(start)
        matched = bool(
            ordinary["status"] == shortcut["status"] == "reached_one"
            and ordinary["steps"] == shortcut["ordinary_toll"] == steps[start]
            and ordinary["peak"] == shortcut["peak"] == peaks[start]
        )
        audits.append(
            {"start": start, "matched": matched, "ordinary": ordinary, "shortcut": shortcut}
        )
    summary = {
        "scope": (1, limit),
        "tested_count": limit,
        "status_counts": counts,
        "all_reached_one": counts["reached_one"] == limit,
        "maximum_total_stopping_time": global_steps_record,
        "maximum_total_stopping_time_start": global_steps_start,
        "maximum_peak": global_peak_record,
        "maximum_peak_start": global_peak_start,
        "checkpoint_size": checkpoint_size,
        "checkpoints": checkpoints,
        "resume_token": chain,
        "exceptions": exceptions,
        "shortcut_stopping_recurrence_holds": (
            not identity_failures and not identity_unresolved
        ),
        # Backward-compatible alias, now conservative for unresolved starts.
        "shortcut_toll_identity_holds": (
            not identity_failures and not identity_unresolved
        ),
        "shortcut_toll_identity_failures": tuple(identity_failures),
        "shortcut_toll_identity_unresolved_count": len(identity_unresolved),
        "shortcut_toll_identity_unresolved_examples": tuple(
            identity_unresolved[:20]
        ),
        "record_and_exception_audits": audits,
        "all_record_and_exception_audits_match": all(row["matched"] for row in audits),
        "bounded_exact_computation": True,
        "independently_replayable_certificate": False,
        "warning": PROOF_WARNING,
        "runtime_seconds": time.perf_counter() - started,
    }
    return summary, _ExactState(steps, peaks, status)


def _fit_model(
    state: _ExactState,
    value_range: tuple[int, int],
    depth: int,
    candidate: bool,
) -> tuple[float, ...]:
    dimension = 2 * depth - 1 if candidate else 2
    equations = _NormalEquations(dimension)
    for value in range(value_range[0] | 1, value_range[1], 2):
        _require_resolved_value(state, value)
        signature = _model_signature(value, depth)
        features = _candidate_features(signature) if candidate else _null_features(signature)
        target = float(state.steps[value] - int(signature["ordinary_toll"]))
        equations.add(features, target)
    return equations.solve()


def _residual(
    value: int,
    state: _ExactState,
    depth: int,
    coefficients: tuple[float, ...],
    candidate: bool,
) -> tuple[float, dict[str, object]]:
    _require_resolved_value(state, value)
    signature = _model_signature(value, depth)
    features = _candidate_features(signature) if candidate else _null_features(signature)
    prediction = int(signature["ordinary_toll"]) + _dot(coefficients, features)
    return float(state.steps[value]) - prediction, signature


def _training_variance_and_groups(
    state: _ExactState,
    value_range: tuple[int, int],
    depth: int,
    null_coefficients: tuple[float, ...],
) -> tuple[float, dict[int, list[float]], float]:
    sse = 0.0
    count = 0
    groups: dict[int, list[float]] = {}
    for value in range(value_range[0] | 1, value_range[1], 2):
        residual, signature = _residual(
            value, state, depth, null_coefficients, False
        )
        sse += residual * residual
        count += 1
        # The parity word is bijective with this residue but is not generally
        # numerically equal to it.  Use the residue explicitly as the lookup key.
        key = int(signature["residue"])
        cell = groups.setdefault(key, [0.0, 0.0, 0.0])
        cell[0] += 1.0
        cell[1] += residual
        cell[2] += residual * residual
    saturated_sse = 0.0
    for cell in groups.values():
        adjustment = cell[1] / (cell[0] + GROUP_SHRINKAGE)
        saturated_sse += cell[2] - 2.0 * adjustment * cell[1] + cell[0] * adjustment**2
    return sse / count, groups, saturated_sse / count


def _candidate_variance(
    state: _ExactState,
    value_range: tuple[int, int],
    depth: int,
    coefficients: tuple[float, ...],
) -> float:
    sse = 0.0
    count = 0
    for value in range(value_range[0] | 1, value_range[1], 2):
        residual, _ = _residual(value, state, depth, coefficients, True)
        sse += residual * residual
        count += 1
    return sse / count


def _historical_score(
    state: _ExactState,
    value_range: tuple[int, int],
    depth: int,
    null_coefficients: tuple[float, ...],
    candidate_coefficients: tuple[float, ...] | None,
    null_variance: float,
    candidate_variance: float | None,
    groups: dict[int, list[float]],
    saturated_variance: float,
) -> dict[str, object]:
    distributions = {
        "mechanistic_null": StudentT(0.0, _student_scale(null_variance), STUDENT_T_DF),
        "saturated_signature_control": StudentT(
            0.0, _student_scale(saturated_variance), STUDENT_T_DF
        ),
    }
    if candidate_coefficients is not None and candidate_variance is not None:
        distributions["compressed_parity_candidate"] = StudentT(
            0.0, _student_scale(candidate_variance), STUDENT_T_DF
        )
    scores = {name: 0.0 for name in distributions}
    squared = {name: 0.0 for name in distributions}
    count = 0
    for value in range(value_range[0] | 1, value_range[1], 2):
        null_residual, signature = _residual(
            value, state, depth, null_coefficients, False
        )
        residuals = {
            "mechanistic_null": null_residual,
            "saturated_signature_control": null_residual
            - (
                groups[int(signature["residue"])][1]
                / (groups[int(signature["residue"])][0] + GROUP_SHRINKAGE)
            ),
        }
        if candidate_coefficients is not None:
            residuals["compressed_parity_candidate"] = _residual(
                value, state, depth, candidate_coefficients, True
            )[0]
        for name, residual in residuals.items():
            scores[name] += distributions[name].log_prob(residual)
            squared[name] += residual * residual
        count += 1
    return {
        "range": value_range,
        "historically_fresh": False,
        "observation_count": count,
        "models": {
            name: {
                "mean_student_t_log_score": scores[name] / count,
                "rmse": math.sqrt(squared[name] / count),
            }
            for name in scores
        },
    }


def _cross_fitted_calibration(
    state: _ExactState, depth: int
) -> dict[str, object]:
    """Calibrate residual scales from two consumed-data cross-fit directions."""

    totals = {
        "mechanistic_null": 0.0,
        "compressed_parity_candidate": 0.0,
        "saturated_signature_control": 0.0,
    }
    total_count = 0
    directions = []
    for train_range, score_range in (
        (REVISION_FIT_RANGE, REVISION_SELECTION_RANGE),
        (REVISION_SELECTION_RANGE, REVISION_FIT_RANGE),
    ):
        null_coefficients = _fit_model(state, train_range, depth, False)
        candidate_coefficients = _fit_model(state, train_range, depth, True)
        null_variance, groups, saturated_variance = _training_variance_and_groups(
            state, train_range, depth, null_coefficients
        )
        candidate_variance = _candidate_variance(
            state, train_range, depth, candidate_coefficients
        )
        scored = _historical_score(
            state,
            score_range,
            depth,
            null_coefficients,
            candidate_coefficients,
            null_variance,
            candidate_variance,
            groups,
            saturated_variance,
        )
        count = int(scored["observation_count"])
        for name, metrics in scored["models"].items():
            totals[name] += float(metrics["rmse"]) ** 2 * count
        total_count += count
        directions.append(
            {
                "train_range": train_range,
                "score_range": score_range,
                "observation_count": count,
                "rmse": {
                    name: float(metrics["rmse"])
                    for name, metrics in scored["models"].items()
                },
            }
        )
    return {
        "method": "two-direction blocked cross-fit over consumed ranges",
        "directions": directions,
        "observation_count": total_count,
        "variance": {
            name: value / total_count for name, value in totals.items()
        },
    }


def _module_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def _revision_data_digest(state: _ExactState) -> str:
    hasher = hashlib.sha256()
    for value in range(REVISION_ALL_RANGE[0] | 1, REVISION_ALL_RANGE[1], 2):
        _require_resolved_value(state, value)
        hasher.update(
            f"{value}:{int(state.status[value])}:{int(state.steps[value])};".encode(
                "ascii"
            )
        )
    return hasher.hexdigest()


def _protocol_payload(
    *,
    depth: int,
    null_coefficients: tuple[float, ...],
    candidate_coefficients: tuple[float, ...],
    saturated_adjustments: tuple[tuple[int, float], ...],
    null_scale: float,
    candidate_scale: float,
    saturated_scale: float,
    candidate_prequalified: bool,
    revision_data_digest: str,
    code_sha256: str,
    parity_residue_bijection_digest: str,
) -> dict[str, object]:
    return {
        "protocol_version": "collatz-shortcut-transport-v2",
        "revision_fit_range": REVISION_FIT_RANGE,
        "revision_selection_range": REVISION_SELECTION_RANGE,
        "revision_all_range": REVISION_ALL_RANGE,
        "revision_data_sha256": revision_data_digest,
        "module_sha256": code_sha256,
        "shortcut_depth": depth,
        "null_family": "exact shortcut toll plus affine log2 terminal height",
        "candidate_family": "compressed start-parity additive plus adjacent terms",
        "endpoint_residue_matched_in_null": False,
        "null_coefficients": null_coefficients,
        "candidate_coefficients": candidate_coefficients,
        "normal_equation_ridge": NORMAL_EQUATION_RIDGE,
        "group_shrinkage": GROUP_SHRINKAGE,
        "saturated_adjustments": saturated_adjustments,
        "parity_residue_bijection_digest": parity_residue_bijection_digest,
        "scales": (null_scale, candidate_scale, saturated_scale),
        "scale_calibration": "two-direction blocked cross-fit",
        "student_t_degrees_of_freedom": STUDENT_T_DF,
        "central_quantiles": (T50, T80, T95, T99),
        "candidate_prequalified": candidate_prequalified,
        "minimum_mean_log_score_gain": MINIMUM_MEAN_LOG_SCORE_GAIN,
        "minimum_candidate_over_saturated_gain": (
            MINIMUM_CANDIDATE_OVER_SATURATED_GAIN
        ),
        "hac_lag": HAC_LAG,
        "hac_lower_bound_multiplier": 2.0,
        "maximum_single_block_positive_gain_share": (
            MAXIMUM_SINGLE_BLOCK_POSITIVE_GAIN_SHARE
        ),
        "fresh_bands": FRESH_BANDS,
        "score_block_size": SCORE_BLOCK_SIZE,
        "diagnostic_thresholds": tuple(sorted(DIAGNOSTIC_THRESHOLDS.items())),
        "open_model_probability_calibrated": False,
        "final_manifest_predated_first_band_access": (
            FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS
        ),
    }


@dataclass(frozen=True)
class _FrozenProtocol:
    depth: int
    null_coefficients: tuple[float, ...]
    candidate_coefficients: tuple[float, ...]
    saturated_adjustments: tuple[tuple[int, float], ...]
    null_scale: float
    candidate_scale: float
    saturated_scale: float
    candidate_prequalified: bool
    revision_data_digest: str
    code_sha256: str
    parity_residue_bijection_digest: str
    digest: str


def _verify_frozen_protocol(
    frozen: _FrozenProtocol, state: _ExactState | None = None
) -> None:
    if _module_sha256() != frozen.code_sha256:
        raise RuntimeError("module source changed after the Collatz protocol froze")
    if state is not None and _revision_data_digest(state) != frozen.revision_data_digest:
        raise RuntimeError("revision data changed after the Collatz protocol froze")
    payload = _protocol_payload(
        depth=frozen.depth,
        null_coefficients=frozen.null_coefficients,
        candidate_coefficients=frozen.candidate_coefficients,
        saturated_adjustments=frozen.saturated_adjustments,
        null_scale=frozen.null_scale,
        candidate_scale=frozen.candidate_scale,
        saturated_scale=frozen.saturated_scale,
        candidate_prequalified=frozen.candidate_prequalified,
        revision_data_digest=frozen.revision_data_digest,
        code_sha256=frozen.code_sha256,
        parity_residue_bijection_digest=frozen.parity_residue_bijection_digest,
    )
    if evidence_payload_digest(payload) != frozen.digest:
        raise RuntimeError("frozen Collatz protocol digest no longer matches")


def revise_and_freeze(state: _ExactState) -> tuple[dict[str, object], _FrozenProtocol]:
    """Use only historically consumed starts below 2^20 for model revision."""

    panel = []
    for depth in DEPTH_SENSITIVITY_PANEL:
        coefficients = _fit_model(state, REVISION_FIT_RANGE, depth, False)
        variance, groups, saturated_variance = _training_variance_and_groups(
            state, REVISION_FIT_RANGE, depth, coefficients
        )
        score = _historical_score(
            state,
            REVISION_SELECTION_RANGE,
            depth,
            coefficients,
            None,
            variance,
            None,
            groups,
            saturated_variance,
        )
        panel.append(
            {
                "depth": depth,
                "mechanistic_null": score["models"]["mechanistic_null"],
                "saturated_signature_control": score["models"]
                ["saturated_signature_control"],
                "saturated_control_gain_over_null": (
                    score["models"]["saturated_signature_control"]
                    ["mean_student_t_log_score"]
                    - score["models"]["mechanistic_null"]
                    ["mean_student_t_log_score"]
                ),
                "historically_fresh": False,
                "role": "revision sensitivity only",
            }
        )

    # Depth ten matches the old residue-tree claim and is design-fixed before
    # fresh scoring. It is neither selected as the best historical depth nor
    # advertised as an optimum.
    depth = SHORTCUT_DEPTH
    fit_null = _fit_model(state, REVISION_FIT_RANGE, depth, False)
    fit_candidate = _fit_model(state, REVISION_FIT_RANGE, depth, True)
    null_variance, fit_groups, saturated_variance = _training_variance_and_groups(
        state, REVISION_FIT_RANGE, depth, fit_null
    )
    candidate_variance = _candidate_variance(
        state, REVISION_FIT_RANGE, depth, fit_candidate
    )
    historical = _historical_score(
        state,
        REVISION_SELECTION_RANGE,
        depth,
        fit_null,
        fit_candidate,
        null_variance,
        candidate_variance,
        fit_groups,
        saturated_variance,
    )
    historical_models = historical["models"]

    candidate_gain = (
        historical_models["compressed_parity_candidate"]["mean_student_t_log_score"]
        - historical_models["mechanistic_null"]["mean_student_t_log_score"]
    )
    saturated_gain = (
        historical_models["saturated_signature_control"]
        ["mean_student_t_log_score"]
        - historical_models["mechanistic_null"]["mean_student_t_log_score"]
    )
    candidate_prequalified = candidate_gain >= MINIMUM_MEAN_LOG_SCORE_GAIN

    # Calibrate residual scales by predicting each consumed half from the
    # other, then fit coefficients exactly once on all consumed revision data.
    # This keeps the residual distribution aligned with the final functional
    # form without using either evaluation band.
    calibration = _cross_fitted_calibration(state, depth)
    calibration_variance = calibration["variance"]
    null_scale = _student_scale(
        float(calibration_variance["mechanistic_null"])
    )
    candidate_scale = _student_scale(
        float(calibration_variance["compressed_parity_candidate"])
    )
    saturated_scale = _student_scale(
        float(calibration_variance["saturated_signature_control"])
    )
    frozen_null = _fit_model(state, REVISION_ALL_RANGE, depth, False)
    frozen_candidate = _fit_model(state, REVISION_ALL_RANGE, depth, True)
    _, full_groups, _ = _training_variance_and_groups(
        state, REVISION_ALL_RANGE, depth, frozen_null
    )
    adjustments = tuple(
        sorted(
            (
                key,
                cell[1] / (cell[0] + GROUP_SHRINKAGE),
            )
            for key, cell in full_groups.items()
        )
    )
    bijection_audit = shortcut_bijection_audit(depth)
    if not bool(bijection_audit["is_bijection"]):
        raise RuntimeError("shortcut parity words did not form a residue bijection")
    revision_digest = _revision_data_digest(state)
    code_sha256 = _module_sha256()
    parameter_payload = _protocol_payload(
        depth=depth,
        null_coefficients=frozen_null,
        candidate_coefficients=frozen_candidate,
        saturated_adjustments=adjustments,
        null_scale=null_scale,
        candidate_scale=candidate_scale,
        saturated_scale=saturated_scale,
        candidate_prequalified=candidate_prequalified,
        revision_data_digest=revision_digest,
        code_sha256=code_sha256,
        parity_residue_bijection_digest=str(bijection_audit["mapping_digest"]),
    )
    digest = evidence_payload_digest(parameter_payload)
    frozen = _FrozenProtocol(
        depth,
        frozen_null,
        frozen_candidate,
        adjustments,
        null_scale,
        candidate_scale,
        saturated_scale,
        candidate_prequalified,
        revision_digest,
        code_sha256,
        str(bijection_audit["mapping_digest"]),
        digest,
    )
    _verify_frozen_protocol(frozen, state)
    return {
        "data_scope": "only starts below 2^20",
        "fit_range": REVISION_FIT_RANGE,
        "historical_selection_range": REVISION_SELECTION_RANGE,
        "historical_selection_is_fresh": False,
        "expanded_depth_sensitivity_panel": panel,
        "frozen_depth": depth,
        "depth_selection_rule": (
            "design-fixed ten-step shortcut matching the old depth claim; historical panel is sensitivity only"
        ),
        "historical_fixed_depth_comparison": historical,
        "historical_candidate_gain_over_null": candidate_gain,
        "minimum_prequalification_gain": MINIMUM_MEAN_LOG_SCORE_GAIN,
        "candidate_supported_before_fresh_scoring": candidate_prequalified,
        "historical_saturated_control_gain_over_null": saturated_gain,
        "saturated_control_supported_at_frozen_depth": saturated_gain > 0.0,
        "matched_mechanistic_negative_finding": (
            "the fixed-depth saturated residue control lost to the exact "
            "shortcut terminal-height null on consumed revision data"
            if saturated_gain <= 0.0
            else "not observed"
        ),
        "saturated_lookup_role": "control only",
        "saturated_lookup_key": "n modulo 2^k",
        "interpretation_scope": (
            "compressed start-residue prediction beyond exact ten-shortcut "
            "toll and terminal height; not an origin-memory test"
        ),
        "endpoint_residue_matched_in_null": False,
        "residual_scale_calibration": calibration,
        "parity_residue_bijection_audit": bijection_audit,
        "modeled_prefix_early_terminal_count": 0,
        "revision_data_sha256": revision_digest,
        "module_sha256": code_sha256,
        "frozen_parameter_digest": digest,
        "fresh_data_used_during_revision": False,
        "final_manifest_predated_first_band_access": (
            FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS
        ),
    }, frozen


def _linear_slope(pairs: list[tuple[float, float]]) -> float:
    mean_x = sum(x for x, _ in pairs) / len(pairs)
    mean_y = sum(y for _, y in pairs) / len(pairs)
    denominator = sum((x - mean_x) ** 2 for x, _ in pairs)
    return 0.0 if denominator == 0.0 else sum(
        (x - mean_x) * (y - mean_y) for x, y in pairs
    ) / denominator


def _hac_standard_error(values: list[float], lag: int) -> float:
    if len(values) < 2:
        return math.inf
    mean = sum(values) / len(values)
    centered = [value - mean for value in values]
    count = len(centered)
    long_run_variance = sum(value * value for value in centered) / count
    for offset in range(1, min(lag, count - 1) + 1):
        covariance = sum(
            centered[index] * centered[index - offset]
            for index in range(offset, count)
        ) / count
        weight = 1.0 - offset / (lag + 1.0)
        long_run_variance += 2.0 * weight * covariance
    return math.sqrt(max(long_run_variance, 0.0) / count)


def _lag_autocorrelation(values: list[float], lag: int) -> float:
    if len(values) <= lag:
        return 0.0
    mean = sum(values) / len(values)
    denominator = sum((value - mean) ** 2 for value in values)
    if denominator == 0.0:
        return 0.0
    return sum(
        (values[index] - mean) * (values[index - lag] - mean)
        for index in range(lag, len(values))
    ) / denominator


def evaluate_fresh_band(
    state: _ExactState,
    frozen: _FrozenProtocol,
    band: tuple[int, int],
    band_index: int,
) -> dict[str, object]:
    """Score one frozen comparison without fitting or model selection."""

    _verify_frozen_protocol(frozen, state)
    block_count = (band[1] - band[0]) // SCORE_BLOCK_SIZE
    if block_count < 1 or (band[1] - band[0]) % SCORE_BLOCK_SIZE:
        raise ValueError("fresh band must contain complete score blocks")
    adjustments = dict(frozen.saturated_adjustments)
    distributions = {
        "mechanistic_null": StudentT(0.0, frozen.null_scale, STUDENT_T_DF),
        "compressed_parity_candidate": StudentT(
            0.0, frozen.candidate_scale, STUDENT_T_DF
        ),
        "saturated_signature_control": StudentT(
            0.0, frozen.saturated_scale, STUDENT_T_DF
        ),
    }
    aggregate = {
        name: {
            "sum": 0.0,
            "square": 0.0,
            "absolute": 0.0,
            "inside50": 0,
            "inside80": 0,
            "inside95": 0,
            "inside99": 0,
            "log_score": 0.0,
        }
        for name in distributions
    }
    blocks = []
    for block_index in range(block_count):
        block_hasher = hashlib.sha256()
        block_hasher.update(
            f"{frozen.digest}:{band[0]}:{band[1]}:{block_index};".encode("ascii")
        )
        blocks.append(
            {
            "count": 0,
            "null_score": 0.0,
            "candidate_score": 0.0,
            "saturated_score": 0.0,
            "candidate_residual_sum": 0.0,
            "hasher": block_hasher,
            }
        )
    count = 0
    unseen_signatures = 0
    for value in range(band[0] | 1, band[1], 2):
        _require_resolved_value(state, value)
        block_index_local = (value - band[0]) // SCORE_BLOCK_SIZE
        signature = _model_signature(value, frozen.depth)
        toll = int(signature["ordinary_toll"])
        null_prediction = toll + _dot(
            frozen.null_coefficients, _null_features(signature)
        )
        candidate_prediction = toll + _dot(
            frozen.candidate_coefficients, _candidate_features(signature)
        )
        key = int(signature["residue"])
        if key not in adjustments:
            unseen_signatures += 1
        saturated_prediction = null_prediction + adjustments.get(key, 0.0)
        target = float(state.steps[value])
        residuals = {
            "mechanistic_null": target - null_prediction,
            "compressed_parity_candidate": target - candidate_prediction,
            "saturated_signature_control": target - saturated_prediction,
        }
        scores = {}
        for name, residual in residuals.items():
            row = aggregate[name]
            row["sum"] += residual
            row["square"] += residual * residual
            row["absolute"] += abs(residual)
            row["inside50"] += abs(residual) <= T50 * distributions[name].scale
            row["inside80"] += abs(residual) <= T80 * distributions[name].scale
            row["inside95"] += abs(residual) <= T95 * distributions[name].scale
            row["inside99"] += abs(residual) <= T99 * distributions[name].scale
            score = distributions[name].log_prob(residual)
            row["log_score"] += score
            scores[name] = score
        block = blocks[block_index_local]
        block["count"] += 1
        block["null_score"] += scores["mechanistic_null"]
        block["candidate_score"] += scores["compressed_parity_candidate"]
        block["saturated_score"] += scores["saturated_signature_control"]
        block["candidate_residual_sum"] += residuals[
            "compressed_parity_candidate"
        ]
        block["hasher"].update(
            (
                f"{value}:{int(target)}:{null_prediction.hex()}:"
                f"{candidate_prediction.hex()}:{saturated_prediction.hex()};"
            ).encode("ascii")
        )
        count += 1

    model_metrics = {}
    for name, row in aggregate.items():
        mean = row["sum"] / count
        variance = max(row["square"] / count - mean * mean, 0.0)
        model_metrics[name] = {
            "mean_residual": mean,
            "residual_standard_deviation": math.sqrt(variance),
            "rmse": math.sqrt(row["square"] / count),
            "mean_absolute_residual": row["absolute"] / count,
            "central_50_coverage": row["inside50"] / count,
            "central_80_coverage": row["inside80"] / count,
            "central_95_coverage": row["inside95"] / count,
            "central_99_coverage": row["inside99"] / count,
            "mean_student_t_log_score": row["log_score"] / count,
        }
    block_rows = []
    height_pairs = []
    for index, block in enumerate(blocks):
        block_start = band[0] + index * SCORE_BLOCK_SIZE
        block_stop = block_start + SCORE_BLOCK_SIZE
        observations = int(block["count"])
        null_score = block["null_score"] / observations
        candidate_score = block["candidate_score"] / observations
        saturated_score = block["saturated_score"] / observations
        residual_mean = block["candidate_residual_sum"] / observations
        midpoint = 0.5 * (block_start + block_stop)
        height_pairs.append((math.log2(midpoint), residual_mean))
        block_rows.append(
            {
                "index": index + 1,
                "range": (block_start, block_stop),
                "odd_observations": observations,
                "candidate_over_null_mean_log_score_gain": candidate_score
                - null_score,
                "candidate_over_saturated_mean_log_score_gain": candidate_score
                - saturated_score,
                "candidate_mean_residual": residual_mean,
                "score_checkpoint_sha256": block["hasher"].hexdigest(),
            }
        )
    candidate = model_metrics["compressed_parity_candidate"]
    score_gain = (
        candidate["mean_student_t_log_score"]
        - model_metrics["mechanistic_null"]["mean_student_t_log_score"]
    )
    candidate_over_saturated = (
        candidate["mean_student_t_log_score"]
        - model_metrics["saturated_signature_control"]
        ["mean_student_t_log_score"]
    )
    block_gains = [
        float(row["candidate_over_null_mean_log_score_gain"])
        for row in block_rows
    ]
    mean_block_gain = sum(block_gains) / len(block_gains)
    hac_standard_error = _hac_standard_error(block_gains, HAC_LAG)
    hac_lower_bound = mean_block_gain - 2.0 * hac_standard_error
    positive_fraction = sum(
        gain > 0.0 for gain in block_gains
    ) / len(block_gains)
    leave_one_out_minimum = (
        min(
            (sum(block_gains) - gain) / (len(block_gains) - 1)
            for gain in block_gains
        )
        if len(block_gains) > 1
        else -math.inf
    )
    positive_total = sum(max(gain, 0.0) for gain in block_gains)
    maximum_positive_gain_share = (
        max((max(gain, 0.0) for gain in block_gains), default=0.0)
        / positive_total
        if positive_total > 0.0
        else 0.0
    )
    block_residual_means = [
        float(row["candidate_mean_residual"]) for row in block_rows
    ]
    height_slope = _linear_slope(height_pairs)
    revision_sd = frozen.candidate_scale * math.sqrt(
        STUDENT_T_DF / (STUDENT_T_DF - 2.0)
    )
    diagnostics = {
        "absolute_bias_in_revision_sd": abs(candidate["mean_residual"]) / revision_sd,
        "central_50_coverage": candidate["central_50_coverage"],
        "central_80_coverage": candidate["central_80_coverage"],
        "central_95_coverage": candidate["central_95_coverage"],
        "central_99_coverage": candidate["central_99_coverage"],
        "height_slope_steps_per_log2": height_slope,
        "absolute_height_slope_in_revision_sd": abs(height_slope) / revision_sd,
        "positive_score_block_fraction": positive_fraction,
        "block_residual_autocorrelation_lags_1_to_4": tuple(
            _lag_autocorrelation(block_residual_means, lag)
            for lag in range(1, 5)
        ),
    }
    gates = {
        "residual_bias": diagnostics["absolute_bias_in_revision_sd"]
        <= DIAGNOSTIC_THRESHOLDS["maximum_absolute_bias_in_revision_sd"],
        "central_50": DIAGNOSTIC_THRESHOLDS["minimum_central_50_coverage"]
        <= candidate["central_50_coverage"]
        <= DIAGNOSTIC_THRESHOLDS["maximum_central_50_coverage"],
        "central_80": DIAGNOSTIC_THRESHOLDS["minimum_central_80_coverage"]
        <= candidate["central_80_coverage"]
        <= DIAGNOSTIC_THRESHOLDS["maximum_central_80_coverage"],
        "tail_95": DIAGNOSTIC_THRESHOLDS["minimum_central_95_coverage"]
        <= candidate["central_95_coverage"]
        <= DIAGNOSTIC_THRESHOLDS["maximum_central_95_coverage"],
        "tail_99": DIAGNOSTIC_THRESHOLDS["minimum_central_99_coverage"]
        <= candidate["central_99_coverage"]
        <= DIAGNOSTIC_THRESHOLDS["maximum_central_99_coverage"],
        "height_transport": diagnostics["absolute_height_slope_in_revision_sd"]
        <= DIAGNOSTIC_THRESHOLDS[
            "maximum_absolute_height_slope_in_revision_sd"
        ],
        "block_stability": positive_fraction
        >= DIAGNOSTIC_THRESHOLDS["minimum_positive_score_block_fraction"],
    }
    primary_score_gates = {
        "candidate_prequalified_on_consumed_data": frozen.candidate_prequalified,
        "mean_gain_at_least_0_02": mean_block_gain
        >= MINIMUM_MEAN_LOG_SCORE_GAIN,
        "hac_lower_bound_positive": hac_lower_bound > 0.0,
        "at_least_75_percent_blocks_positive": positive_fraction
        >= DIAGNOSTIC_THRESHOLDS["minimum_positive_score_block_fraction"],
        "all_leave_one_block_out_means_positive": leave_one_out_minimum > 0.0,
        "single_block_positive_gain_share_at_most_0_20": (
            maximum_positive_gain_share
            <= MAXIMUM_SINGLE_BLOCK_POSITIVE_GAIN_SHARE
        ),
        "candidate_noninferior_to_saturated_control": (
            candidate_over_saturated
            >= MINIMUM_CANDIDATE_OVER_SATURATED_GAIN
        ),
    }
    directional = score_gain > 0.0
    diagnostics_pass = all(gates.values())
    primary_score_pass = all(primary_score_gates.values())
    open_model = {
        "name": "M_bottom",
        "probability": None,
        "probability_calibrated": False,
        "gate_passed": False,
        "reason": "no development-calibrated robust open model is available",
    }
    historically_fresh = FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS
    formal_replication = bool(
        historically_fresh
        and primary_score_pass
        and diagnostics_pass
        and open_model["gate_passed"]
    )
    return {
        "band_index": band_index,
        "range_half_open": band,
        "historically_fresh": historically_fresh,
        "locked_transport_evaluation": True,
        "freshness_caveat": (
            "predeclared and excluded from fitting, but first access preceded "
            "the persisted final manifest"
        ),
        "frozen_parameter_digest": frozen.digest,
        "frozen_protocol_digest_verified_before_scoring": True,
        "parameters_updated_on_band": False,
        "model_reselection_performed": False,
        "odd_observation_count": count,
        "unseen_signature_count": unseen_signatures,
        "model_metrics": model_metrics,
        "candidate_over_null_mean_log_score_gain": score_gain,
        "candidate_over_saturated_mean_log_score_gain": candidate_over_saturated,
        "fresh_direction_favors_candidate": directional,
        "block_score_audit": {
            "block_count": len(block_gains),
            "mean_gain": mean_block_gain,
            "hac_lag": HAC_LAG,
            "hac_standard_error": hac_standard_error,
            "mean_minus_2_hac_se": hac_lower_bound,
            "positive_block_fraction": positive_fraction,
            "minimum_leave_one_block_out_mean": leave_one_out_minimum,
            "maximum_single_block_positive_gain_share": (
                maximum_positive_gain_share
            ),
        },
        "primary_score_gates": primary_score_gates,
        "primary_score_passed": primary_score_pass,
        "open_model": open_model,
        "diagnostics": diagnostics,
        "diagnostic_gates": gates,
        "diagnostics_passed": diagnostics_pass,
        "diagnostics_are_simultaneously_calibrated": False,
        "formal_replication": formal_replication,
        "score_blocks": block_rows,
        "score_blocks_are_replications": False,
    }


def _ledger_summary(
    revision: dict[str, object],
    bands: list[dict[str, object]],
    exact: dict[str, object],
) -> dict[str, object]:
    statistical = EvidenceLedger()
    observations = [
        (
            "collatz_multistep_revision",
            ("odd-starts-262144-1048575",),
            "historical_model_revision",
            "historical_revision",
            {
                "frozen_parameter_digest": revision["frozen_parameter_digest"],
                "historical_candidate_gain_over_null": revision[
                    "historical_candidate_gain_over_null"
                ],
            },
        )
    ]
    for band in bands:
        start, stop = band["range_half_open"]
        observations.append(
            (
                f"collatz_multistep_transport_{band['band_index']}",
                (f"odd-starts-{start}-{stop - 1}",),
                "locked_transport_band_score",
                "accessed_validation",
                {
                    "range": (start, stop),
                    "frozen_parameter_digest": band["frozen_parameter_digest"],
                    "candidate_over_null_mean_log_score_gain": band[
                        "candidate_over_null_mean_log_score_gain"
                    ],
                    "fresh_direction_favors_candidate": band[
                        "fresh_direction_favors_candidate"
                    ],
                    "formal_replication": band["formal_replication"],
                    "diagnostics_passed": band["diagnostics_passed"],
                },
            )
        )
    for record_id, sources, action, scope, observation in observations:
        statistical = statistical.append(
            EvidenceRecord(
                record_id,
                sources,
                action,
                None,
                evidence_payload_digest(observation),
                "student_t_block_score",
                scope,
                observation,
            )
        )
    exact_observation = {
        "scope": exact["scope"],
        "status_counts": exact["status_counts"],
        "resume_token": exact["resume_token"],
        "bounded_exact_computation": True,
    }
    exact_ledger = EvidenceLedger().append(
        EvidenceRecord(
            "collatz_multistep_bounded_exact",
            (f"all-starts-{exact['scope'][0]}-{exact['scope'][1]}",),
            "exact_integer_census",
            None,
            evidence_payload_digest(exact_observation),
            "exact_integer_computation",
            "bounded_exact",
            exact_observation,
        )
    )
    return {
        "statistical_record_ids": statistical.record_ids,
        "statistical_source_ids": statistical.source_ids,
        "bounded_exact_record_ids": exact_ledger.record_ids,
        "bounded_exact_source_ids": exact_ledger.source_ids,
        "separate_statistical_and_exact_ledgers": True,
        "canonical_payload_digests_verified": True,
    }


def run_collatz_multistep_replication() -> dict[str, object]:
    """Run revision, freeze, exact census, and two locked transport scores."""

    started = time.perf_counter()
    exact, state = exact_frontier_through_2pow22()
    if not (
        exact["all_reached_one"]
        and exact["shortcut_stopping_recurrence_holds"]
        and exact["all_record_and_exception_audits_match"]
    ):
        raise RuntimeError(
            "bounded arithmetic did not clear quarantine; statistical scoring refused"
        )
    revision, frozen = revise_and_freeze(state)
    bands = [
        evaluate_fresh_band(state, frozen, band, index + 1)
        for index, band in enumerate(FRESH_BANDS)
    ]
    directional_count = sum(
        bool(row["fresh_direction_favors_candidate"]) for row in bands
    )
    formal_replication_count = sum(
        bool(row["formal_replication"]) for row in bands
    )
    historical_supported = bool(revision["candidate_supported_before_fresh_scoring"])
    if not historical_supported:
        statistical_state = "NO_HISTORICAL_GAIN"
    elif not FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS:
        statistical_state = "NEEDS_FRESH_VALIDATION"
    elif any(not band["open_model"]["probability_calibrated"] for band in bands):
        statistical_state = "MODEL_REVISION"
    elif formal_replication_count < 2:
        statistical_state = "REPLICATION_FAILED"
    else:
        statistical_state = "TWO_FRESH_REPLICATIONS"
    ledger = _ledger_summary(revision, bands, exact)
    return {
        "search": "Collatz multistep shortcut revision and locked transport evaluation",
        "proof_warning": PROOF_WARNING,
        "replication_warning": REPLICATION_WARNING,
        "revision": revision,
        "frozen_protocol": {
            "shortcut_depth": frozen.depth,
            "shortcut_identity": (
                "tau(n) = C_k + tau(S^k(n)) when the audited k-step prefix "
                "does not encounter one early"
            ),
            "ordinary_toll": "C_k = k + number of odd shortcut steps",
            "parity_signature_bijection": (
                "the parity word is a one-to-one encoding of n modulo 2^k; "
                "it is not generally numerically equal to that residue"
            ),
            "parity_residue_bijection_audit": revision[
                "parity_residue_bijection_audit"
            ],
            "candidate": "position-additive plus adjacent-parity interactions",
            "candidate_interpretation": (
                "compressed start-residue predictor, not origin-memory evidence"
            ),
            "endpoint_residue_matched_in_null": False,
            "saturated_lookup": "residue-keyed control only",
            "student_t_degrees_of_freedom": STUDENT_T_DF,
            "residual_scale_calibration": "two-direction blocked cross-fit",
            "normal_equation_ridge": NORMAL_EQUATION_RIDGE,
            "parameter_digest": frozen.digest,
            "revision_data_sha256": frozen.revision_data_digest,
            "module_sha256": frozen.code_sha256,
            "evaluation_bands": FRESH_BANDS,
            "score_block_size": SCORE_BLOCK_SIZE,
            "minimum_mean_log_score_gain": MINIMUM_MEAN_LOG_SCORE_GAIN,
            "hac_lag": HAC_LAG,
            "diagnostic_thresholds": DIAGNOSTIC_THRESHOLDS,
            "model_parameters_frozen_before_band_scoring": True,
            "final_manifest_predated_first_band_access": (
                FINAL_MANIFEST_PREDATED_FIRST_BAND_ACCESS
            ),
            "open_model_probability_calibrated": False,
        },
        "fresh_band_results": bands,
        "locked_transport_bands_favoring_candidate": directional_count,
        "formal_replication_count": formal_replication_count,
        "statistical_state": statistical_state,
        "bounded_arithmetic": exact,
        "bounded_arithmetic_scope": exact["scope"],
        "bounded_arithmetic_is_global_proof": False,
        "provenance": ledger,
        "runtime_seconds": time.perf_counter() - started,
    }


if __name__ == "__main__":
    print(json.dumps(run_collatz_multistep_replication(), indent=2))
