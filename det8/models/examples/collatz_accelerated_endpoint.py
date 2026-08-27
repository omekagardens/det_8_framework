"""Locked accelerated-Collatz endpoint/valuation transport experiment.

This module separates consumed protocol development (starts no larger than
``2**22``) from two untouched transport bands ending at ``2**24``.  The public
preparation function can only construct the consumed frontier.  The default
runner refuses to allocate, compute, or score a larger start unless it first
validates a persisted, byte-independent canonical manifest, reproduces its
entire consumed protocol, and confirms that the fixed candidate prequalified.

For ``n = 2**e0 * x0`` with odd ``x0``, one accelerated odd jump is

    A(x) = (3*x + 1) / 2**v2(3*x + 1).

After ``d`` nonterminal jumps, with valuations ``nu_0, ..., nu_(d-1)``,

    tau(n) = e0 + d + sum(nu_j) + tau(A**d(x0)),
    A**d(x0) = (3**d*x0 + c_d) / 2**sum(nu_j),
    c_(j+1) = 3*c_j + 2**sum(nu_0,...,nu_(j-1)).

Both identities are checked with exact integer arithmetic.  Prefixes that
encounter one are reported as deterministic early-terminal strata and never
silently forced through the statistical model.

The fixed H0 removes the exact origin toll, then uses a fixed quadratic/hinge
endpoint-height basis, a shrunken endpoint residue effect, and a same-depth
endpoint valuation basis.  H1 adds only the matched origin valuation basis as
new terms while jointly refitting the shared endpoint coefficients.
Thus an H1 gain means incremental compression relative to a deliberately
strong endpoint control; it is not evidence of nonlocal path memory and is
not a Collatz proof.  A broad-tail Student-t score is reported only as a
sensitivity analysis; it is not an open model and never supplies a posterior
or replication gate.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from array import array
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence

from det8.models.relational_evidence import (
    EvidenceLedger,
    EvidenceRecord,
    StudentT,
    evidence_payload_digest,
)


SCHEMA_VERSION = "collatz-accelerated-endpoint-v1"
RESERVATION_SCHEMA_VERSION = "collatz-accelerated-reservation-v1"
CONSUMED_LIMIT = 1 << 22
FUTURE_LIMIT = 1 << 24
EXACT_CHECKPOINT_SIZE = 1 << 18

DESIGN_DEPTH = 4
DESIGN_RESIDUE_BITS = 8
VALUATION_CAP = 8
SENSITIVITY_DESIGNS = ((2, 6), (4, 8), (6, 10))
HEIGHT_HINGES = (16.0, 20.0, 24.0)
RESIDUE_SHRINKAGE = 32.0
NORMAL_EQUATION_RIDGE = 1.0e-7

PRIMARY_FOLDS = (
    ((1 << 16, 1 << 19), (1 << 19, 1 << 20)),
    ((1 << 16, 1 << 20), (1 << 20, 1 << 21)),
    ((1 << 16, 1 << 21), (1 << 21, 1 << 22)),
)
FINAL_FIT_RANGE = (1 << 16, 1 << 22)
SENSITIVITY_TRAIN_RANGE = (1 << 16, 1 << 18)
SENSITIVITY_SCORE_RANGE = (1 << 18, 1 << 19)
FUTURE_BANDS = ((1 << 22, 1 << 23), (1 << 23, 1 << 24))

# Blocks are intervals of integer starts.  Only odd starts are statistically
# distinct and scored, so each complete block contains 2**13 observations.
SCORE_BLOCK_SIZE = 1 << 14
STUDENT_T_DF = 5.0
BROAD_TAIL_DF = 3.0
MINIMUM_MEAN_LOG_SCORE_GAIN = 0.02
HAC_LAG = 4
HAC_Z = 1.96
MINIMUM_POSITIVE_BLOCK_FRACTION = 0.75
MAXIMUM_SINGLE_BLOCK_POSITIVE_GAIN_SHARE = 0.20
MAXIMUM_ABSOLUTE_STANDARDIZED_BIAS = 0.10
MINIMUM_CENTRAL_80_COVERAGE = 0.70
MAXIMUM_CENTRAL_80_COVERAGE = 0.90
MINIMUM_CENTRAL_95_COVERAGE = 0.88
MAXIMUM_CENTRAL_95_COVERAGE = 0.99
MAXIMUM_ABSOLUTE_HEIGHT_SLOPE_IN_SCALE = 0.25
SCORE_DIAGNOSTIC_GATES_SIMULATION_CALIBRATED = False
OPEN_MODEL_CALIBRATED = False

_UINT32_UNRESOLVED = (1 << 32) - 1
_FUTURE_EXTENSION_AUTHORIZATION = object()

PROOF_WARNING = (
    "The arithmetic census is an exact bounded computation over the reported "
    "finite start frontier. It neither proves the Collatz conjecture nor "
    "turns checkpoint hashes into an independently replayable formal proof."
)
INTERPRETATION_WARNING = (
    "Any H1 score gain is incremental prediction beyond exact origin toll, "
    "endpoint height, endpoint residue, and matched endpoint valuations. It "
    "does not by itself identify nonlocal memory, a new invariant, or a proof."
)
REPLICATION_WARNING = (
    "A dyadic future band counts as at most one locked transport evaluation; "
    "its 2**14-width score blocks measure stability and are not replications. "
    "The broad-tail sensitivity is not an open model, so no model probability "
    "or formal RG2 claim is reported by this module."
)

# Machine-readable record of the completed consumed-only integration run.  It
# is intentionally not a launch manifest and cannot authorize future access.
CONSUMED_REFERENCE_FINDINGS = {
    "schema_version": "collatz-accelerated-consumed-reference-v1",
    "run_date": "2026-08-26",
    "consumed_limit_inclusive": CONSUMED_LIMIT,
    "fixed_design": {
        "depth": DESIGN_DEPTH,
        "endpoint_residue_bits": DESIGN_RESIDUE_BITS,
        "valuation_cap": VALUATION_CAP,
    },
    "exact_frontier": {
        "all_reached_one": True,
        "maximum_total_stopping_time": 596,
        "maximum_total_stopping_time_start": 3_732_423,
        "odd_state_sha256": (
            "3e3602fee2431838871ee6672dd62b1b82b4f8c6bd6647d3ca20161b2def8521"
        ),
        "resume_chain_sha256": (
            "40aa2a92278a41a9555dc5a0775a4ea3cb70e44f7c9f7befc12c53fd0777ef47"
        ),
        "all_direct_record_audits_match": True,
        "all_affine_toll_audits_hold": True,
    },
    "primary_fold_equal_block_weighted_gains": (
        {
            "score_range_half_open": (1 << 19, 1 << 20),
            "gain": -0.00029738461371436875,
            "diagnostic_gates_passed": True,
            "score_gates_passed": False,
        },
        {
            "score_range_half_open": (1 << 20, 1 << 21),
            "gain": -0.000040970894685340986,
            "diagnostic_gates_passed": True,
            "score_gates_passed": False,
        },
        {
            "score_range_half_open": (1 << 21, 1 << 22),
            "gain": -0.0000041561519516231105,
            "diagnostic_gates_passed": True,
            "score_gates_passed": False,
        },
    ),
    "sensitivity_equal_block_weighted_gains": (
        {"depth": 2, "residue_bits": 6, "gain": -0.00023165359454979662},
        {"depth": 4, "residue_bits": 8, "gain": -0.0004056205000125823},
        {"depth": 6, "residue_bits": 10, "gain": -0.0012403074559459992},
    ),
    "frozen_protocol_digest": (
        "ec45de146e290e758ce5bc8d721f2e537554b2149ef4a8e016069da34af0a338"
    ),
    "candidate_prequalified": False,
    "all_primary_fold_gains_negative": True,
    "consumed_statistical_state": "NO_CONSUMED_GAIN",
    "future_bands_status": "PRESERVED_UNTOUCHED",
    "manifest_persisted": False,
    "starts_above_consumed_limit_accessed": False,
    "prequalification_gates_simulation_calibrated": False,
    "open_model_available": False,
}
CONSUMED_REFERENCE_FINDINGS_SHA256 = (
    "b1b97493c76aad12337f12556344eaa36a2c657c805f697cf011a9329a4fb37e"
)


def v2(value: int) -> int:
    """Return the exact 2-adic valuation of a positive integer."""

    if value < 1:
        raise ValueError("v2 requires a positive integer")
    return (value & -value).bit_length() - 1


def accelerated_step(value: int) -> tuple[int, int]:
    """Return ``(A(value), nu)`` for an odd positive ``value``."""

    if value < 1 or value % 2 == 0:
        raise ValueError("accelerated odd jump requires a positive odd value")
    expanded = 3 * value + 1
    valuation = v2(expanded)
    return expanded >> valuation, valuation


def accelerated_prefix(value: int, depth: int = DESIGN_DEPTH) -> dict[str, object]:
    """Return an exact accelerated prefix and its toll/affine audits.

    Initial factors of two are stripped exactly.  ``early_terminal`` is true
    whenever one is encountered before a complete nonterminal prefix can be
    used for statistical scoring, including an endpoint equal to one.
    """

    if value < 1 or depth < 1:
        raise ValueError("accelerated prefix requires positive value and depth")
    initial_halvings = v2(value)
    odd_core = value >> initial_halvings
    current = odd_core
    valuations: list[int] = []
    valuation_sum = 0
    affine_constant = 0
    affine_audits: list[bool] = []
    for jump_index in range(depth):
        if current == 1:
            break
        next_value, valuation = accelerated_step(current)
        affine_constant = 3 * affine_constant + (1 << valuation_sum)
        valuation_sum += valuation
        current = next_value
        valuations.append(valuation)
        affine_audits.append(
            (3 ** (jump_index + 1)) * odd_core + affine_constant
            == current * (1 << valuation_sum)
        )
    used_depth = len(valuations)
    ordinary_toll = initial_halvings + used_depth + valuation_sum
    return {
        "start": value,
        "initial_halvings": initial_halvings,
        "odd_core": odd_core,
        "requested_depth": depth,
        "used_depth": used_depth,
        "valuations": tuple(valuations),
        "valuation_sum": valuation_sum,
        "ordinary_toll": ordinary_toll,
        "endpoint": current,
        "affine_constant": affine_constant,
        "affine_numerator": (3**used_depth) * odd_core + affine_constant,
        "affine_denominator": 1 << valuation_sum,
        "affine_identity_holds": all(affine_audits),
        "toll_identity_holds": ordinary_toll
        == initial_halvings + used_depth + sum(valuations),
        "early_terminal": current == 1 or used_depth < depth,
    }


def valuation_basis(
    valuations: Sequence[int], depth: int = DESIGN_DEPTH, cap: int = VALUATION_CAP
) -> tuple[float, ...]:
    """Return the fixed compressed valuation basis used at both endpoints.

    It consists of capped normalized valuations, cap-overflow indicators, and
    adjacent products.  Requiring exactly ``depth`` values prevents an early
    terminal prefix from being confused with an ordinary zero-padded row.
    """

    if depth < 1 or cap < 1 or len(valuations) != depth:
        raise ValueError("valuation basis requires depth values and positive cap")
    if any(value < 1 for value in valuations):
        raise ValueError("accelerated valuations must be positive")
    capped = tuple(min(int(value), cap) / float(cap) for value in valuations)
    overflow = tuple(float(value > cap) for value in valuations)
    adjacent = tuple(capped[index] * capped[index + 1] for index in range(depth - 1))
    return capped + overflow + adjacent


def _ordinary_next(value: int) -> int:
    return value // 2 if value % 2 == 0 else 3 * value + 1


def _ordinary_advance(start: int, steps: int) -> int:
    """Advance an ordinary Collatz trajectory by an exact fixed toll."""

    if start < 1 or steps < 0:
        raise ValueError("ordinary replay requires a positive start and nonnegative toll")
    current = start
    for _ in range(steps):
        current = _ordinary_next(current)
    return current


def _direct_total_stopping_time(start: int, maximum_steps: int = 100_000) -> int:
    current = start
    seen: set[int] = set()
    steps = 0
    while current != 1 and steps < maximum_steps:
        if current in seen:
            raise RuntimeError("direct Collatz audit encountered a cycle")
        seen.add(current)
        current = _ordinary_next(current)
        steps += 1
    if current != 1:
        raise RuntimeError("direct Collatz audit exhausted its resource limit")
    return steps


@dataclass
class _OddExactState:
    """Odd-only uint32 stopping times plus an ascending hash-chain frontier."""

    steps: array
    status: bytearray
    limit: int
    checkpoint_size: int
    max_descent_jumps: int
    chain_sha256: str
    checkpoints: list[dict[str, object]]
    exception_starts: list[int]
    maximum_stopping_time: int
    maximum_stopping_time_start: int

    @classmethod
    def empty(
        cls,
        checkpoint_size: int = EXACT_CHECKPOINT_SIZE,
        max_descent_jumps: int = 10_000,
    ) -> "_OddExactState":
        if checkpoint_size < 1 or max_descent_jumps < 1:
            raise ValueError("frontier controls must be positive")
        uint32_probe = array("I")
        if uint32_probe.itemsize != 4:
            raise RuntimeError("accelerated exact state requires a 4-byte uint32 array")
        return cls(
            steps=array("I", [0]),
            status=bytearray([1]),
            limit=0,
            checkpoint_size=checkpoint_size,
            max_descent_jumps=max_descent_jumps,
            chain_sha256=hashlib.sha256(
                (SCHEMA_VERSION + ":exact:" + str(checkpoint_size)).encode("ascii")
            ).hexdigest(),
            checkpoints=[],
            exception_starts=[],
            maximum_stopping_time=0,
            maximum_stopping_time_start=1,
        )

    @staticmethod
    def _odd_index(value: int) -> int:
        if value < 1 or value % 2 == 0:
            raise ValueError("odd-state lookup requires a positive odd value")
        return (value - 1) // 2

    def total_stopping_time(self, value: int) -> int:
        """Derive an even start from its stored odd core without duplication."""

        if value < 1 or value > self.limit:
            raise ValueError("start is outside the constructed exact frontier")
        return self._total_from_stored_odd_core(value)

    def _total_from_stored_odd_core(self, value: int) -> int:
        """Derive a row whose odd core has already been resolved.

        The ascending builder uses this private helper before advancing its
        public ``limit`` at the end of a checkpoint-aligned extension.
        """

        halvings = v2(value)
        odd = value >> halvings
        index = self._odd_index(odd)
        if index >= len(self.status) or self.status[index] != 1:
            raise RuntimeError("start is unresolved in the exact frontier")
        stored = int(self.steps[index])
        if stored == _UINT32_UNRESOLVED:
            raise RuntimeError("start has an unresolved uint32 sentinel")
        return halvings + stored

    def _resolve_odd(self, start: int) -> tuple[str, int, int, int]:
        if start == 1:
            return "reached_one", 0, 1, 0
        current = start
        local_toll = 0
        jumps = 0
        seen: set[int] = set()
        while current >= start:
            if current in seen:
                return "verified_cycle", -1, current, jumps
            if jumps >= self.max_descent_jumps:
                return "resource_limit", -1, current, jumps
            seen.add(current)
            current, valuation = accelerated_step(current)
            local_toll += 1 + valuation
            jumps += 1
        index = self._odd_index(current)
        if index >= len(self.status) or self.status[index] != 1:
            return "resource_limit", -1, current, jumps
        total = local_toll + int(self.steps[index])
        if total >= _UINT32_UNRESOLVED:
            raise OverflowError("stopping time does not fit odd-only uint32 storage")
        return "reached_one", total, current, jumps

    def extend_to(self, target: int, *, _authorization: object = None) -> None:
        """Extend in ascending order; future starts require private authorization."""

        if target < self.limit:
            raise ValueError("an exact frontier cannot be shrunk")
        if target > FUTURE_LIMIT:
            raise ValueError("this protocol never authorizes starts above 2**24")
        if target > CONSUMED_LIMIT and _authorization is not _FUTURE_EXTENSION_AUTHORIZATION:
            raise PermissionError(
                "extension above 2**22 requires a reproduced persisted manifest"
            )
        if target == self.limit:
            return
        if self.limit and self.limit % self.checkpoint_size:
            raise ValueError("staged extension requires a checkpoint-aligned frontier")
        if target % self.checkpoint_size:
            raise ValueError("target must be checkpoint aligned")

        required_odd_count = (target + 1) // 2
        missing = required_odd_count - len(self.steps)
        if missing > 0:
            self.steps.extend(array("I", [_UINT32_UNRESOLVED]) * missing)
            self.status.extend(bytearray(missing))

        block_start = self.limit + 1
        block_hash = hashlib.sha256()
        block_reached = 0
        block_resource = 0
        block_cycle = 0
        block_maximum = -1
        block_maximum_start = block_start

        for start in range(self.limit + 1, target + 1):
            if start == 1:
                outcome, total, merge, jumps = "reached_one", 0, 1, 0
            elif start & 1:
                outcome, total, merge, jumps = self._resolve_odd(start)
                index = self._odd_index(start)
                if outcome == "reached_one":
                    self.steps[index] = total
                    self.status[index] = 1
                else:
                    self.steps[index] = _UINT32_UNRESOLVED
                    self.status[index] = 2 if outcome == "resource_limit" else 3
                    self.exception_starts.append(start)
            else:
                try:
                    total = self._total_from_stored_odd_core(start)
                    outcome, merge, jumps = "reached_one", start >> v2(start), v2(start)
                except RuntimeError:
                    outcome, total, merge, jumps = "resource_limit", -1, start, 0
                    self.exception_starts.append(start)

            if outcome == "reached_one":
                block_reached += 1
                if total > block_maximum:
                    block_maximum, block_maximum_start = total, start
                if total > self.maximum_stopping_time:
                    self.maximum_stopping_time = total
                    self.maximum_stopping_time_start = start
            elif outcome == "resource_limit":
                block_resource += 1
            else:
                block_cycle += 1
            block_hash.update(
                f"{start}:{outcome}:{total}:{merge}:{jumps};".encode("ascii")
            )

            if start % self.checkpoint_size == 0:
                digest = block_hash.hexdigest()
                self.chain_sha256 = hashlib.sha256(
                    (
                        f"{self.chain_sha256}:{block_start}:{start}:{digest}"
                    ).encode("ascii")
                ).hexdigest()
                self.checkpoints.append(
                    {
                        "range_inclusive": (block_start, start),
                        "status_counts": {
                            "reached_one": block_reached,
                            "resource_limit": block_resource,
                            "verified_cycle": block_cycle,
                        },
                        "maximum_total_stopping_time": block_maximum,
                        "maximum_total_stopping_time_start": block_maximum_start,
                        "block_sha256": digest,
                        "chain_sha256": self.chain_sha256,
                    }
                )
                block_start = start + 1
                block_hash = hashlib.sha256()
                block_reached = block_resource = block_cycle = 0
                block_maximum = -1
                block_maximum_start = block_start
        self.limit = target

    def state_sha256(self) -> str:
        hasher = hashlib.sha256()
        canonical_steps = array("I", self.steps)
        if sys.byteorder != "little":
            canonical_steps.byteswap()
        hasher.update(canonical_steps.tobytes())
        hasher.update(bytes(self.status))
        hasher.update(str(self.limit).encode("ascii"))
        return hasher.hexdigest()

    def summary(self) -> dict[str, object]:
        resource = sum(
            int(row["status_counts"]["resource_limit"]) for row in self.checkpoints
        )
        cycles = sum(
            int(row["status_counts"]["verified_cycle"]) for row in self.checkpoints
        )
        reached = self.limit - resource - cycles
        audit_starts = {1, self.maximum_stopping_time_start}
        audit_starts.update(
            int(row["maximum_total_stopping_time_start"])
            for row in self.checkpoints
            if int(row["maximum_total_stopping_time_start"]) >= 1
        )
        direct_audits = []
        affine_audits = []
        for start in sorted(audit_starts):
            stored = self.total_stopping_time(start)
            direct = _direct_total_stopping_time(start)
            direct_audits.append(
                {"start": start, "stored": stored, "direct": direct, "matches": stored == direct}
            )
            prefix = accelerated_prefix(start, DESIGN_DEPTH)
            affine_audits.append(
                {
                    "start": start,
                    "affine_identity_holds": prefix["affine_identity_holds"],
                    "toll_identity_holds": prefix["toll_identity_holds"],
                    "early_terminal": prefix["early_terminal"],
                }
            )
        return {
            "scope_inclusive": (1, self.limit),
            "storage": (
                "odd-only 4-byte uint32 array; even stopping times derived by "
                "v2 stripping; state hash canonicalized to little endian"
            ),
            "stored_odd_count": len(self.steps),
            "status_counts": {
                "reached_one": reached,
                "resource_limit": resource,
                "verified_cycle": cycles,
            },
            "all_reached_one": resource == 0 and cycles == 0,
            "maximum_total_stopping_time": self.maximum_stopping_time,
            "maximum_total_stopping_time_start": self.maximum_stopping_time_start,
            "checkpoint_size": self.checkpoint_size,
            "checkpoint_count": len(self.checkpoints),
            "resume_chain_sha256": self.chain_sha256,
            "odd_state_sha256": self.state_sha256(),
            "direct_record_audits": tuple(direct_audits),
            "all_direct_record_audits_match": all(row["matches"] for row in direct_audits),
            "accelerated_affine_toll_audits": tuple(affine_audits),
            "all_affine_toll_audits_hold": all(
                row["affine_identity_holds"] and row["toll_identity_holds"]
                for row in affine_audits
            ),
            "bounded_exact_computation": True,
            "proof_warning": PROOF_WARNING,
        }


class _NormalEquations:
    def __init__(self, dimension: int, ridge: float = NORMAL_EQUATION_RIDGE) -> None:
        if dimension < 1:
            raise ValueError("normal equations require positive dimension")
        self.dimension = dimension
        self.ridge = ridge
        self.matrix = [[0.0] * dimension for _ in range(dimension)]
        self.vector = [0.0] * dimension
        self.count = 0

    def add(self, features: Sequence[float], target: float) -> None:
        if len(features) != self.dimension:
            raise ValueError("regression feature dimension changed")
        self.count += 1
        for row, left in enumerate(features):
            self.vector[row] += left * target
            for column in range(row, self.dimension):
                self.matrix[row][column] += left * features[column]

    def solve(self) -> tuple[float, ...]:
        if self.count < self.dimension:
            raise RuntimeError("insufficient rows for fixed regression design")
        matrix = [row[:] for row in self.matrix]
        for row in range(self.dimension):
            for column in range(row):
                matrix[row][column] = matrix[column][row]
            matrix[row][row] += self.ridge
        augmented = [matrix[row] + [self.vector[row]] for row in range(self.dimension)]
        for column in range(self.dimension):
            pivot_row = max(
                range(column, self.dimension),
                key=lambda row: abs(augmented[row][column]),
            )
            augmented[column], augmented[pivot_row] = augmented[pivot_row], augmented[column]
            pivot = augmented[column][column]
            if abs(pivot) < 1.0e-14:
                raise RuntimeError("fixed accelerated valuation design is singular")
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


class _GroupedNormalEquations:
    """Sparse ridge regression with one shrunken categorical intercept."""

    def __init__(self, dimension: int, group_count: int) -> None:
        if dimension < 1 or group_count < 1:
            raise ValueError("grouped normal equations require positive dimensions")
        self.dimension = dimension
        self.group_count = group_count
        self.matrix = [[0.0] * dimension for _ in range(dimension)]
        self.vector = [0.0] * dimension
        self.group_features = [[0.0] * dimension for _ in range(group_count)]
        self.group_targets = [0.0] * group_count
        self.group_counts = [0] * group_count
        self.target_square = 0.0
        self.count = 0

    def add(self, features: Sequence[float], target: float, group: int) -> None:
        if len(features) != self.dimension or not 0 <= group < self.group_count:
            raise ValueError("grouped regression row changed shape")
        self.count += 1
        self.target_square += target * target
        self.group_counts[group] += 1
        self.group_targets[group] += target
        for row, left in enumerate(features):
            self.vector[row] += left * target
            self.group_features[group][row] += left
            for column in range(row, self.dimension):
                self.matrix[row][column] += left * features[column]

    def solve(self, shrinkage: float) -> tuple[tuple[float, ...], tuple[tuple[int, float], ...]]:
        if (
            not math.isfinite(shrinkage)
            or shrinkage <= 0.0
            or self.count < self.dimension
        ):
            raise RuntimeError("invalid grouped regression support")
        equations = _NormalEquations(self.dimension)
        equations.matrix = [row[:] for row in self.matrix]
        equations.vector = self.vector[:]
        equations.count = self.count
        for group in range(self.group_count):
            denominator = self.group_counts[group] + shrinkage
            feature_sums = self.group_features[group]
            target_sum = self.group_targets[group]
            for row in range(self.dimension):
                equations.vector[row] -= (
                    feature_sums[row] * target_sum / denominator
                )
                for column in range(row, self.dimension):
                    equations.matrix[row][column] -= (
                        feature_sums[row] * feature_sums[column] / denominator
                    )
        coefficients = equations.solve()
        adjustments = []
        for group in range(self.group_count):
            denominator = self.group_counts[group] + shrinkage
            adjustment = (
                self.group_targets[group]
                - _dot(self.group_features[group], coefficients)
            ) / denominator
            adjustments.append((group, adjustment))
        return coefficients, tuple(adjustments)

    def residual_square(
        self,
        coefficients: Sequence[float],
        adjustments: Sequence[tuple[int, float]],
    ) -> float:
        """Recover unpenalized residual SSE from sufficient statistics."""

        if len(coefficients) != self.dimension:
            raise ValueError("coefficient dimension changed")
        adjustment_map = dict(adjustments)
        if len(adjustment_map) != self.group_count:
            raise ValueError("group adjustment support changed")
        fitted_quadratic = 0.0
        for row in range(self.dimension):
            fitted_quadratic += (
                coefficients[row] * coefficients[row] * self.matrix[row][row]
            )
            for column in range(row + 1, self.dimension):
                fitted_quadratic += (
                    2.0
                    * coefficients[row]
                    * coefficients[column]
                    * self.matrix[row][column]
                )
        residual = (
            self.target_square
            - 2.0 * _dot(coefficients, self.vector)
            + fitted_quadratic
        )
        for group in range(self.group_count):
            adjustment = adjustment_map[group]
            residual += (
                -2.0 * adjustment * self.group_targets[group]
                + 2.0
                * adjustment
                * _dot(self.group_features[group], coefficients)
                + self.group_counts[group] * adjustment * adjustment
            )
        if not math.isfinite(residual):
            raise RuntimeError("grouped regression residual square is not finite")
        return max(residual, 0.0)


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def _height_basis(endpoint: int) -> tuple[float, ...]:
    height = math.log2(endpoint)
    return (
        1.0,
        height,
        height * height,
        *(max(0.0, height - hinge) for hinge in HEIGHT_HINGES),
    )


@dataclass(frozen=True)
class _ModelRow:
    start: int
    stopping_time: int
    exact_origin_toll: int
    matched_endpoint_toll: int
    endpoint: int
    endpoint_residue: int
    height_endpoint_features: tuple[float, ...]
    endpoint_valuation_features: tuple[float, ...]
    origin_valuation_features: tuple[float, ...]
    origin_valuations: tuple[int, ...]
    endpoint_valuations: tuple[int, ...]

    @property
    def remaining_target(self) -> float:
        return float(self.stopping_time - self.exact_origin_toll)


def _model_row(
    state: _OddExactState, start: int, depth: int, residue_bits: int, cap: int
) -> tuple[Optional[_ModelRow], str]:
    if start < 1 or start % 2 == 0:
        raise ValueError("statistical rows are unique odd starts")
    stopping_time = state.total_stopping_time(start)
    origin = accelerated_prefix(start, depth)
    if not (
        bool(origin["affine_identity_holds"])
        and bool(origin["toll_identity_holds"])
    ):
        raise RuntimeError("origin accelerated toll/affine row audit failed")
    if bool(origin["early_terminal"]):
        if int(origin["endpoint"]) != 1 or stopping_time != int(
            origin["ordinary_toll"]
        ) or _ordinary_advance(start, int(origin["ordinary_toll"])) != 1:
            raise RuntimeError("origin-terminal stopping-time identity failed")
        return None, "origin_prefix_terminal"
    endpoint = int(origin["endpoint"])
    endpoint_prefix = accelerated_prefix(endpoint, depth)
    if not (
        bool(endpoint_prefix["affine_identity_holds"])
        and bool(endpoint_prefix["toll_identity_holds"])
    ):
        raise RuntimeError("endpoint accelerated toll/affine row audit failed")
    if bool(endpoint_prefix["early_terminal"]):
        if int(endpoint_prefix["endpoint"]) != 1 or stopping_time != int(
            origin["ordinary_toll"]
        ) + int(endpoint_prefix["ordinary_toll"]) or _ordinary_advance(
            start, int(origin["ordinary_toll"])
        ) != endpoint or _ordinary_advance(
            endpoint, int(endpoint_prefix["ordinary_toll"])
        ) != 1:
            raise RuntimeError("endpoint-terminal stopping-time identity failed")
        return None, "endpoint_prefix_terminal"
    origin_values = tuple(int(value) for value in origin["valuations"])
    endpoint_values = tuple(int(value) for value in endpoint_prefix["valuations"])
    exact_toll = int(origin["ordinary_toll"])
    if stopping_time < exact_toll:
        raise RuntimeError("nonterminal exact toll exceeds total stopping time")
    if _ordinary_advance(start, exact_toll) != endpoint:
        raise RuntimeError("nonterminal accelerated stopping-time identity failed")
    if endpoint <= state.limit and (
        stopping_time != exact_toll + state.total_stopping_time(endpoint)
    ):
        raise RuntimeError("stored endpoint continuation identity failed")
    return (
        _ModelRow(
            start=start,
            stopping_time=stopping_time,
            exact_origin_toll=exact_toll,
            matched_endpoint_toll=int(endpoint_prefix["ordinary_toll"]),
            endpoint=endpoint,
            endpoint_residue=endpoint % (1 << residue_bits),
            height_endpoint_features=_height_basis(endpoint),
            endpoint_valuation_features=valuation_basis(endpoint_values, depth, cap),
            origin_valuation_features=valuation_basis(origin_values, depth, cap),
            origin_valuations=origin_values,
            endpoint_valuations=endpoint_values,
        ),
        "statistical",
    )


def _iter_rows(
    state: _OddExactState,
    start_range: tuple[int, int],
    depth: int,
    residue_bits: int,
    cap: int,
) -> Iterable[tuple[Optional[_ModelRow], str]]:
    first, stop = start_range
    if first < 1 or stop <= first or stop - 1 > state.limit:
        raise ValueError("model range lies outside the constructed frontier")
    for start in range(first | 1, stop, 2):
        yield _model_row(state, start, depth, residue_bits, cap)


def _student_scale(variance: float, degrees: float = STUDENT_T_DF) -> float:
    return math.sqrt(max(variance, 1.0e-10) * (degrees - 2.0) / degrees)


@dataclass(frozen=True)
class _FrozenProtocol:
    depth: int
    residue_bits: int
    valuation_cap: int
    fit_range: tuple[int, int]
    base_coefficients: tuple[float, ...]
    residue_adjustments: tuple[tuple[int, float], ...]
    supported_endpoint_residues: tuple[int, ...]
    h1_base_coefficients: tuple[float, ...]
    h1_residue_adjustments: tuple[tuple[int, float], ...]
    origin_coefficients: tuple[float, ...]
    h0_scale: float
    h1_scale: float
    broad_tail_scale: float
    fit_statistical_count: int
    early_terminal_counts: tuple[tuple[str, int], ...]
    fit_data_sha256: str
    scale_calibration: str
    digest: str


def _protocol_payload(protocol: _FrozenProtocol, include_digest: bool = True) -> dict[str, object]:
    payload: dict[str, object] = {
        "depth": protocol.depth,
        "residue_bits": protocol.residue_bits,
        "valuation_cap": protocol.valuation_cap,
        "height_basis": {
            "terms": ("1", "h", "h^2", "hinge_16", "hinge_20", "hinge_24"),
            "hinges": HEIGHT_HINGES,
        },
        "endpoint_residue_shrinkage": RESIDUE_SHRINKAGE,
        "fit_range_half_open": protocol.fit_range,
        "base_coefficients": protocol.base_coefficients,
        "residue_adjustments": protocol.residue_adjustments,
        "supported_endpoint_residues": protocol.supported_endpoint_residues,
        "h1_base_coefficients": protocol.h1_base_coefficients,
        "h1_residue_adjustments": protocol.h1_residue_adjustments,
        "origin_coefficients": protocol.origin_coefficients,
        "h0_student_t_scale": protocol.h0_scale,
        "h1_student_t_scale": protocol.h1_scale,
        "student_t_degrees_of_freedom": STUDENT_T_DF,
        "broad_tail_sensitivity": {
            "scale": protocol.broad_tail_scale,
            "degrees_of_freedom": BROAD_TAIL_DF,
            "calibrated": False,
            "probability": None,
            "role": "broad-tail score sensitivity; not an open model",
        },
        "fit_statistical_count": protocol.fit_statistical_count,
        "early_terminal_counts": protocol.early_terminal_counts,
        "fit_data_sha256": protocol.fit_data_sha256,
        "scale_calibration": protocol.scale_calibration,
        "h0_definition": (
            "exact origin toll + fixed endpoint height basis + shrunken endpoint "
            "residue + same-depth endpoint valuation basis"
        ),
        "h1_increment": "matched origin valuation basis only",
    }
    if include_digest:
        payload["protocol_digest"] = protocol.digest
    return payload


def _fit_protocol(
    state: _OddExactState,
    fit_range: tuple[int, int],
    depth: int,
    residue_bits: int,
    cap: int,
) -> _FrozenProtocol:
    endpoint_dimension = len(_height_basis(3)) + (3 * depth - 1)
    origin_dimension = 3 * depth - 1
    group_count = 1 << residue_bits
    h0_equations = _GroupedNormalEquations(endpoint_dimension, group_count)
    h1_equations = _GroupedNormalEquations(
        endpoint_dimension + origin_dimension, group_count
    )
    strata = {"origin_prefix_terminal": 0, "endpoint_prefix_terminal": 0}
    data_hasher = hashlib.sha256()
    first_odd = fit_range[0] | 1
    for source_index, (row, stratum) in enumerate(
        _iter_rows(state, fit_range, depth, residue_bits, cap)
    ):
        source_start = first_odd + 2 * source_index
        if row is None:
            strata[stratum] += 1
            data_hasher.update(f"{source_start}:{stratum};".encode("ascii"))
            continue
        endpoint_features = (
            row.height_endpoint_features + row.endpoint_valuation_features
        )
        h0_equations.add(
            endpoint_features, row.remaining_target, row.endpoint_residue
        )
        h1_equations.add(
            endpoint_features + row.origin_valuation_features,
            row.remaining_target,
            row.endpoint_residue,
        )
        data_hasher.update(
            (
                f"{row.start}:{row.stopping_time}:{row.exact_origin_toll}:"
                f"{row.matched_endpoint_toll}:{row.endpoint}:"
                f"{row.origin_valuations}:{row.endpoint_valuations};"
            ).encode("ascii")
        )
    base_coefficients, adjustments = h0_equations.solve(RESIDUE_SHRINKAGE)
    h1_all_coefficients, h1_adjustments = h1_equations.solve(
        RESIDUE_SHRINKAGE
    )
    h1_base_coefficients = h1_all_coefficients[:endpoint_dimension]
    origin_coefficients = h1_all_coefficients[endpoint_dimension:]
    count = h0_equations.count
    if h1_equations.count != count:
        raise RuntimeError("H0/H1 grouped regression support diverged")
    h0_square = h0_equations.residual_square(base_coefficients, adjustments)
    h1_square = h1_equations.residual_square(
        h1_all_coefficients, h1_adjustments
    )
    if count < 2:
        raise RuntimeError("too few nonterminal rows to freeze protocol")
    h0_scale = _student_scale(h0_square / count)
    h1_scale = _student_scale(h1_square / count)
    broad_tail_scale = 2.0 * max(h0_scale, h1_scale)
    draft = _FrozenProtocol(
        depth=depth,
        residue_bits=residue_bits,
        valuation_cap=cap,
        fit_range=fit_range,
        base_coefficients=base_coefficients,
        residue_adjustments=adjustments,
        supported_endpoint_residues=tuple(
            index
            for index, count_in_group in enumerate(h0_equations.group_counts)
            if count_in_group > 0
        ),
        h1_base_coefficients=h1_base_coefficients,
        h1_residue_adjustments=h1_adjustments,
        origin_coefficients=origin_coefficients,
        h0_scale=h0_scale,
        h1_scale=h1_scale,
        broad_tail_scale=broad_tail_scale,
        fit_statistical_count=count,
        early_terminal_counts=tuple(sorted(strata.items())),
        fit_data_sha256=data_hasher.hexdigest(),
        scale_calibration="in-sample training residuals",
        digest="",
    )
    digest = evidence_payload_digest(_protocol_payload(draft, include_digest=False))
    return _FrozenProtocol(**{**draft.__dict__, "digest": digest})


def _predict(protocol: _FrozenProtocol, row: _ModelRow) -> tuple[float, float]:
    adjustments = dict(protocol.residue_adjustments)
    h1_adjustments = dict(protocol.h1_residue_adjustments)
    endpoint_features = (
        row.height_endpoint_features + row.endpoint_valuation_features
    )
    h0_remaining = _dot(
        protocol.base_coefficients,
        endpoint_features,
    ) + adjustments.get(row.endpoint_residue, 0.0)
    h1_remaining = _dot(
        protocol.h1_base_coefficients, endpoint_features
    ) + h1_adjustments.get(row.endpoint_residue, 0.0) + _dot(
        protocol.origin_coefficients, row.origin_valuation_features
    )
    return row.exact_origin_toll + h0_remaining, row.exact_origin_toll + h1_remaining


def _hac_standard_error(values: Sequence[float], lag: int = HAC_LAG) -> float:
    if len(values) < 2:
        return math.inf
    mean = sum(values) / len(values)
    centered = [value - mean for value in values]
    count = len(centered)
    long_run = sum(value * value for value in centered) / count
    effective_lag = min(lag, count - 1)
    for offset in range(1, effective_lag + 1):
        covariance = sum(
            centered[index] * centered[index - offset]
            for index in range(offset, count)
        ) / count
        long_run += 2.0 * (1.0 - offset / (effective_lag + 1.0)) * covariance
    return math.sqrt(max(long_run, 0.0) / count)


def _linear_slope(pairs: Sequence[tuple[float, float]]) -> float:
    if len(pairs) < 2:
        return 0.0
    mean_x = sum(left for left, _ in pairs) / len(pairs)
    mean_y = sum(right for _, right in pairs) / len(pairs)
    denominator = sum((left - mean_x) ** 2 for left, _ in pairs)
    if denominator == 0.0:
        return 0.0
    return sum(
        (left - mean_x) * (right - mean_y) for left, right in pairs
    ) / denominator


def _score_range(
    state: _OddExactState,
    protocol: _FrozenProtocol,
    score_range: tuple[int, int],
    label: str,
    manifest_digest: Optional[str] = None,
) -> dict[str, object]:
    start, stop = score_range
    width = stop - start
    if width < 2 * SCORE_BLOCK_SIZE or width % SCORE_BLOCK_SIZE:
        raise ValueError("score range must contain at least two complete fixed blocks")
    block_count = width // SCORE_BLOCK_SIZE
    binding_digest = manifest_digest or protocol.digest
    blocks = [
        {
            "count": 0,
            "h0_score": 0.0,
            "h1_score": 0.0,
            "broad_tail_score": 0.0,
            "h1_residual_sum": 0.0,
            "inside80": 0,
            "inside95": 0,
            "hasher": hashlib.sha256(
                f"{binding_digest}:{label}:{index};".encode("ascii")
            ),
        }
        for index in range(block_count)
    ]
    h0_distribution = StudentT(0.0, protocol.h0_scale, STUDENT_T_DF)
    h1_distribution = StudentT(0.0, protocol.h1_scale, STUDENT_T_DF)
    broad_tail_distribution = StudentT(
        0.0, protocol.broad_tail_scale, BROAD_TAIL_DF
    )
    early = {"origin_prefix_terminal": 0, "endpoint_prefix_terminal": 0}
    total_count = 0
    total_h0_score = total_h1_score = total_broad_tail_score = 0.0
    total_h0_square = total_h1_residual = total_h1_square = 0.0
    inside80 = inside95 = 0
    # Two-sided central cutoffs for t_5, included as fixed protocol constants.
    t80 = 1.4758840488558216
    t95 = 2.570581835636305
    score_hasher = hashlib.sha256(
        f"{binding_digest}:{label}:all;".encode("ascii")
    )
    unseen_endpoint_residue_count = 0
    total_endpoint_control_toll = 0
    total_endpoint_control_target_fraction = 0.0
    maximum_endpoint_control_toll = 0
    maximum_endpoint_control_target_fraction = 0.0
    total_combined_toll = 0
    total_combined_stopping_fraction = 0.0
    first_odd = score_range[0] | 1
    supported_residues = set(protocol.supported_endpoint_residues)
    for source_index, (row, stratum) in enumerate(
        _iter_rows(
            state,
            score_range,
            protocol.depth,
            protocol.residue_bits,
            protocol.valuation_cap,
        )
    ):
        source_start = first_odd + 2 * source_index
        if row is None:
            early[stratum] += 1
            block_index = (source_start - start) // SCORE_BLOCK_SIZE
            blocks[block_index]["hasher"].update(
                f"{source_start}:{stratum};".encode("ascii")
            )
            score_hasher.update(f"{source_start}:{stratum};".encode("ascii"))
            continue
        h0_prediction, h1_prediction = _predict(protocol, row)
        h0_residual = row.stopping_time - h0_prediction
        h1_residual = row.stopping_time - h1_prediction
        h0_score = h0_distribution.log_prob(h0_residual)
        h1_score = h1_distribution.log_prob(h1_residual)
        broad_tail_score = broad_tail_distribution.log_prob(h0_residual)
        unseen_endpoint_residue_count += (
            row.endpoint_residue not in supported_residues
        )
        block_index = (row.start - start) // SCORE_BLOCK_SIZE
        block = blocks[block_index]
        block["count"] += 1
        block["h0_score"] += h0_score
        block["h1_score"] += h1_score
        block["broad_tail_score"] += broad_tail_score
        block["h1_residual_sum"] += h1_residual
        block["inside80"] += abs(h1_residual) <= t80 * protocol.h1_scale
        block["inside95"] += abs(h1_residual) <= t95 * protocol.h1_scale
        block["hasher"].update(
            (
                f"{row.start}:{row.stopping_time}:{h0_prediction.hex()}:"
                f"{h1_prediction.hex()};"
            ).encode("ascii")
        )
        score_hasher.update(
            f"{row.start}:{row.stopping_time}:{row.endpoint};".encode("ascii")
        )
        total_h0_score += h0_score
        total_h1_score += h1_score
        total_broad_tail_score += broad_tail_score
        total_h0_square += h0_residual * h0_residual
        total_h1_residual += h1_residual
        total_h1_square += h1_residual * h1_residual
        endpoint_target_fraction = (
            row.matched_endpoint_toll / row.remaining_target
        )
        combined_toll = row.exact_origin_toll + row.matched_endpoint_toll
        total_endpoint_control_toll += row.matched_endpoint_toll
        total_endpoint_control_target_fraction += endpoint_target_fraction
        maximum_endpoint_control_toll = max(
            maximum_endpoint_control_toll, row.matched_endpoint_toll
        )
        maximum_endpoint_control_target_fraction = max(
            maximum_endpoint_control_target_fraction, endpoint_target_fraction
        )
        total_combined_toll += combined_toll
        total_combined_stopping_fraction += combined_toll / row.stopping_time
        inside80 += abs(h1_residual) <= t80 * protocol.h1_scale
        inside95 += abs(h1_residual) <= t95 * protocol.h1_scale
        total_count += 1
    if total_count < 2 or any(int(block["count"]) == 0 for block in blocks):
        raise RuntimeError("score range lacks complete nonterminal block support")

    block_rows = []
    gains = []
    height_residual_pairs = []
    for index, block in enumerate(blocks):
        count = int(block["count"])
        h0_score = float(block["h0_score"]) / count
        h1_score = float(block["h1_score"]) / count
        gain = h1_score - h0_score
        residual_mean = float(block["h1_residual_sum"]) / count
        block_start = start + index * SCORE_BLOCK_SIZE
        block_stop = block_start + SCORE_BLOCK_SIZE
        gains.append(gain)
        height_residual_pairs.append(
            (math.log2(0.5 * (block_start + block_stop)), residual_mean)
        )
        block_rows.append(
            {
                "index": index + 1,
                "range_half_open": (block_start, block_stop),
                "odd_statistical_count": count,
                "h1_over_h0_mean_log_score_gain": gain,
                "h1_mean_residual": residual_mean,
                "score_checkpoint_sha256": block["hasher"].hexdigest(),
            }
        )
    mean_gain = sum(gains) / len(gains)
    observation_weighted_gain = (
        total_h1_score - total_h0_score
    ) / total_count
    hac_se = _hac_standard_error(gains)
    hac_lower = mean_gain - HAC_Z * hac_se
    positive_fraction = sum(gain > 0.0 for gain in gains) / len(gains)
    loo_minimum = min(
        (sum(gains) - gain) / (len(gains) - 1) for gain in gains
    )
    positive_total = sum(max(gain, 0.0) for gain in gains)
    maximum_share = (
        max(max(gain, 0.0) for gain in gains) / positive_total
        if positive_total > 0.0
        else 0.0
    )
    mean_residual = total_h1_residual / total_count
    residual_variance = max(
        total_h1_square / total_count - mean_residual * mean_residual, 0.0
    )
    height_slope = _linear_slope(height_residual_pairs)
    score_gates = {
        "mean_gain_at_least_0_02": mean_gain >= MINIMUM_MEAN_LOG_SCORE_GAIN,
        "hac_95_lower_bound_positive": hac_lower > 0.0,
        "all_leave_one_block_out_means_positive": loo_minimum > 0.0,
        "at_least_75_percent_blocks_positive": positive_fraction
        >= MINIMUM_POSITIVE_BLOCK_FRACTION,
        "single_block_positive_gain_share_at_most_0_20": maximum_share
        <= MAXIMUM_SINGLE_BLOCK_POSITIVE_GAIN_SHARE,
    }
    diagnostics = {
        "h1_mean_residual": mean_residual,
        "h1_residual_standard_deviation": math.sqrt(residual_variance),
        "absolute_bias_in_training_scale": abs(mean_residual) / protocol.h1_scale,
        "central_80_coverage": inside80 / total_count,
        "central_95_coverage": inside95 / total_count,
        "height_slope_steps_per_log2": height_slope,
        "absolute_height_slope_in_training_scale": abs(height_slope)
        / protocol.h1_scale,
    }
    diagnostic_gates = {
        "bias": diagnostics["absolute_bias_in_training_scale"]
        <= MAXIMUM_ABSOLUTE_STANDARDIZED_BIAS,
        "central_80": MINIMUM_CENTRAL_80_COVERAGE
        <= diagnostics["central_80_coverage"]
        <= MAXIMUM_CENTRAL_80_COVERAGE,
        "central_95": MINIMUM_CENTRAL_95_COVERAGE
        <= diagnostics["central_95_coverage"]
        <= MAXIMUM_CENTRAL_95_COVERAGE,
        "height_transport": diagnostics["absolute_height_slope_in_training_scale"]
        <= MAXIMUM_ABSOLUTE_HEIGHT_SLOPE_IN_SCALE,
    }
    return {
        "label": label,
        "range_half_open": score_range,
        "integer_start_block_size": SCORE_BLOCK_SIZE,
        "block_count": block_count,
        "odd_statistical_count": total_count,
        "early_terminal_strata": early,
        "unseen_endpoint_residue_count": unseen_endpoint_residue_count,
        "matched_probe_horizon": {
            "origin_feature_accelerated_jumps": protocol.depth,
            "endpoint_control_accelerated_jumps": protocol.depth,
            "combined_observed_accelerated_jumps": 2 * protocol.depth,
            "mean_endpoint_control_ordinary_toll": (
                total_endpoint_control_toll / total_count
            ),
            "maximum_endpoint_control_ordinary_toll": (
                maximum_endpoint_control_toll
            ),
            "mean_endpoint_control_fraction_of_modeled_remaining_target": (
                total_endpoint_control_target_fraction / total_count
            ),
            "maximum_endpoint_control_fraction_of_modeled_remaining_target": (
                maximum_endpoint_control_target_fraction
            ),
            "mean_combined_ordinary_toll": total_combined_toll / total_count,
            "mean_combined_fraction_of_total_stopping_time": (
                total_combined_stopping_fraction / total_count
            ),
        },
        "h0_mean_student_t_log_score": total_h0_score / total_count,
        "h1_mean_student_t_log_score": total_h1_score / total_count,
        "observation_weighted_h1_over_h0_mean_log_score_gain": (
            observation_weighted_gain
        ),
        "h1_over_h0_mean_log_score_gain": mean_gain,
        "gain_gate_weighting": "equal weight per fixed integer-start block",
        "broad_tail_mean_log_score_sensitivity": (
            total_broad_tail_score / total_count
        ),
        "broad_tail_is_open_model": False,
        "open_model_available": False,
        "open_model_probability": None,
        "h0_residual_square_sum": total_h0_square,
        "h1_residual_square_sum": total_h1_square,
        "block_audit": {
            "mean_gain": mean_gain,
            "hac_lag": HAC_LAG,
            "hac_standard_error": hac_se,
            "mean_minus_1_96_hac_se": hac_lower,
            "positive_block_fraction": positive_fraction,
            "minimum_leave_one_block_out_mean": loo_minimum,
            "maximum_single_block_positive_gain_share": maximum_share,
        },
        "score_gates": score_gates,
        "score_gates_passed": all(score_gates.values()),
        "diagnostics": diagnostics,
        "diagnostic_gates": diagnostic_gates,
        "diagnostic_gates_passed": all(diagnostic_gates.values()),
        "prequalification_fold_passed": all(score_gates.values())
        and all(diagnostic_gates.values()),
        "prequalification_gates_are_simulation_calibrated": False,
        "score_data_sha256": score_hasher.hexdigest(),
        "score_blocks": tuple(block_rows),
        "score_blocks_are_replications": False,
    }


def _rolling_fold(
    state: _OddExactState,
    train_range: tuple[int, int],
    score_range: tuple[int, int],
    depth: int,
    residue_bits: int,
    cap: int,
    label: str,
) -> tuple[dict[str, object], _FrozenProtocol]:
    protocol = _fit_protocol(state, train_range, depth, residue_bits, cap)
    score = _score_range(state, protocol, score_range, label)
    score["training_range_half_open"] = train_range
    score["training_protocol_digest"] = protocol.digest
    score["training_rows_exclude_scored_range"] = train_range[1] <= score_range[0]
    return score, protocol


def _apply_rolling_out_of_fold_scales(
    protocol: _FrozenProtocol, folds: Sequence[Mapping[str, object]]
) -> _FrozenProtocol:
    count = sum(int(fold["odd_statistical_count"]) for fold in folds)
    if count < 2:
        raise RuntimeError("rolling folds do not calibrate a predictive scale")
    h0_variance = sum(float(fold["h0_residual_square_sum"]) for fold in folds) / count
    h1_variance = sum(float(fold["h1_residual_square_sum"]) for fold in folds) / count
    h0_scale = _student_scale(h0_variance)
    h1_scale = _student_scale(h1_variance)
    draft = replace(
        protocol,
        h0_scale=h0_scale,
        h1_scale=h1_scale,
        broad_tail_scale=2.0 * max(h0_scale, h1_scale),
        scale_calibration=(
            "pooled residual squares from the three disjoint consumed rolling "
            "score bands; final coefficients fit once on all consumed rows"
        ),
        digest="",
    )
    return replace(
        draft,
        digest=evidence_payload_digest(
            _protocol_payload(draft, include_digest=False)
        ),
    )


def _sensitivity_panel(state: _OddExactState) -> dict[str, object]:
    rows = []
    for depth, residue_bits in SENSITIVITY_DESIGNS:
        score, _ = _rolling_fold(
            state,
            SENSITIVITY_TRAIN_RANGE,
            SENSITIVITY_SCORE_RANGE,
            depth,
            residue_bits,
            VALUATION_CAP,
            f"consumed_sensitivity_d{depth}_k{residue_bits}",
        )
        rows.append(
            {
                "depth": depth,
                "residue_bits": residue_bits,
                "valuation_cap": VALUATION_CAP,
                "h1_over_h0_mean_log_score_gain": score[
                    "h1_over_h0_mean_log_score_gain"
                ],
                "score_gates_passed": score["score_gates_passed"],
                "diagnostic_gates_passed": score["diagnostic_gates_passed"],
                "prequalification_fold_passed": score[
                    "prequalification_fold_passed"
                ],
                "training_protocol_digest": score["training_protocol_digest"],
                "score_data_sha256": score["score_data_sha256"],
            }
        )
    best = max(rows, key=lambda row: float(row["h1_over_h0_mean_log_score_gain"]))
    return {
        "designs": SENSITIVITY_DESIGNS,
        "training_range_half_open": SENSITIVITY_TRAIN_RANGE,
        "score_range_half_open": SENSITIVITY_SCORE_RANGE,
        "rows": tuple(rows),
        "descriptive_maximum": {
            "depth": best["depth"],
            "residue_bits": best["residue_bits"],
            "gain": best["h1_over_h0_mean_log_score_gain"],
            "is_panel_endpoint": (
                (best["depth"], best["residue_bits"])
                in (SENSITIVITY_DESIGNS[0], SENSITIVITY_DESIGNS[-1])
            ),
        },
        "selection_performed": False,
        "panel_maximum_can_change_fixed_design": False,
        "fixed_design_is_interior": DESIGN_DEPTH == 4 and DESIGN_RESIDUE_BITS == 8,
        "interpretation": "consumed sensitivity only; never a depth/model selection step",
    }


def _odd_statistical_source_blocks(start: int, stop: int) -> tuple[str, ...]:
    """Return clipped inclusive odd-direct source IDs for a half-open range."""

    first = start - (start % SCORE_BLOCK_SIZE)
    sources = []
    for block in range(first, stop, SCORE_BLOCK_SIZE):
        low = max(start, block) | 1
        high = min(stop, block + SCORE_BLOCK_SIZE) - 1
        if high % 2 == 0:
            high -= 1
        if low <= high:
            sources.append(f"odd-direct-starts-{low}-{high}")
    return tuple(sources)


def _all_exact_source_blocks(first: int, last: int) -> tuple[str, ...]:
    """Return clipped inclusive all-direct source IDs."""

    if first < 1 or last < first:
        raise ValueError("exact source range must be positive and nonempty")
    block = (first // SCORE_BLOCK_SIZE) * SCORE_BLOCK_SIZE
    sources = []
    while block <= last:
        low = max(first, block)
        high = min(last, block + SCORE_BLOCK_SIZE - 1)
        if low <= high:
            sources.append(f"all-direct-starts-{low}-{high}")
        block += SCORE_BLOCK_SIZE
    return tuple(sources)


def _preparation_ledger_summary(
    exact: Mapping[str, object],
    folds: Sequence[Mapping[str, object]],
    sensitivity: Mapping[str, object],
    frozen: _FrozenProtocol,
) -> dict[str, object]:
    statistical_observation = {
        "role": "joint consumed development record; reused rolling training is not double-counted",
        "rolling_fold_protocol_digests": tuple(
            fold["training_protocol_digest"] for fold in folds
        ),
        "rolling_fold_score_digests": tuple(fold["score_data_sha256"] for fold in folds),
        "sensitivity_designs": sensitivity["designs"],
        "frozen_protocol_digest": frozen.digest,
    }
    statistical = EvidenceLedger().append(
        EvidenceRecord(
            record_id="collatz_accelerated_consumed_joint_development",
            source_ids=_odd_statistical_source_blocks(1 << 16, CONSUMED_LIMIT),
            action="rolling_development_sensitivity_and_freeze",
            coordinate=None,
            digest=evidence_payload_digest(statistical_observation),
            family="student_t_block_scores",
            scope="consumed_development",
            observation=statistical_observation,
            metadata={"overlapping_training_roles_encoded_once": True},
            joint=True,
        )
    )
    exact_observation = {
        "scope_inclusive": exact["scope_inclusive"],
        "status_counts": exact["status_counts"],
        "resume_chain_sha256": exact["resume_chain_sha256"],
        "odd_state_sha256": exact["odd_state_sha256"],
    }
    exact_ledger = EvidenceLedger().append(
        EvidenceRecord(
            record_id="collatz_accelerated_bounded_exact_consumed",
            source_ids=_all_exact_source_blocks(1, CONSUMED_LIMIT),
            action="ascending_exact_integer_census",
            coordinate=None,
            digest=evidence_payload_digest(exact_observation),
            family="exact_integer_computation",
            scope="bounded_exact",
            observation=exact_observation,
            joint=True,
        )
    )
    return {
        "statistical_record_ids": statistical.record_ids,
        "statistical_source_count": len(statistical.source_ids),
        "bounded_exact_record_ids": exact_ledger.record_ids,
        "bounded_exact_source_count": len(exact_ledger.source_ids),
        "separate_statistical_and_exact_ledgers": True,
        "statistical_reuse_encoded_as_one_joint_record": True,
        "canonical_payload_digests_verified": True,
    }


def _prepare_internal() -> tuple[dict[str, object], _OddExactState, _FrozenProtocol]:
    state = _OddExactState.empty()
    state.extend_to(CONSUMED_LIMIT)
    exact = state.summary()
    if not (
        bool(exact["all_reached_one"])
        and bool(exact["all_direct_record_audits_match"])
        and bool(exact["all_affine_toll_audits_hold"])
    ):
        raise RuntimeError("bounded exact arithmetic failed quarantine")

    folds = []
    for index, (train_range, score_range) in enumerate(PRIMARY_FOLDS, 1):
        score, _ = _rolling_fold(
            state,
            train_range,
            score_range,
            DESIGN_DEPTH,
            DESIGN_RESIDUE_BITS,
            VALUATION_CAP,
            f"consumed_rolling_fold_{index}",
        )
        folds.append(score)
    candidate_prequalified = all(
        bool(fold["prequalification_fold_passed"]) for fold in folds
    )
    all_primary_fold_gains_negative = all(
        float(fold["h1_over_h0_mean_log_score_gain"]) < 0.0 for fold in folds
    )
    sensitivity = _sensitivity_panel(state)
    frozen = _fit_protocol(
        state,
        FINAL_FIT_RANGE,
        DESIGN_DEPTH,
        DESIGN_RESIDUE_BITS,
        VALUATION_CAP,
    )
    frozen = _apply_rolling_out_of_fold_scales(frozen, folds)
    ledger = _preparation_ledger_summary(exact, folds, sensitivity, frozen)
    implementation_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    manifest: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "experiment": "accelerated odd-jump endpoint-matched valuation transport",
        "consumed_limit_inclusive": CONSUMED_LIMIT,
        "future_limit_inclusive": FUTURE_LIMIT,
        "preparation_accessed_starts_above_consumed_limit": False,
        "design_fixed_before_future_access": {
            "depth": DESIGN_DEPTH,
            "endpoint_residue_bits": DESIGN_RESIDUE_BITS,
            "valuation_cap": VALUATION_CAP,
            "height_hinges": HEIGHT_HINGES,
            "integer_start_score_block_size": SCORE_BLOCK_SIZE,
            "odd_starts_only_in_statistics": True,
            "h1_new_terms": "matched origin valuation basis only",
            "h1_jointly_refits_shared_endpoint_controls": True,
        },
        "exact_consumed_frontier": exact,
        "rolling_consumed_validation": tuple(folds),
        "candidate_prequalified": candidate_prequalified,
        "all_primary_fold_gains_negative": all_primary_fold_gains_negative,
        "consumed_statistical_state": (
            "NO_CONSUMED_GAIN"
            if all_primary_fold_gains_negative
            else (
                "CONSUMED_PREQUALIFIED"
                if candidate_prequalified
                else "CONSUMED_PREQUALIFICATION_FAILED"
            )
        ),
        "future_bands_status": (
            "ELIGIBLE_FOR_GOVERNED_RESERVATION"
            if candidate_prequalified
            else "PRESERVED_UNTOUCHED"
        ),
        "prequalification_is_simulation_calibrated": (
            SCORE_DIAGNOSTIC_GATES_SIMULATION_CALIBRATED
        ),
        "rigorous_future_launch_authorized": bool(
            candidate_prequalified
            and SCORE_DIAGNOSTIC_GATES_SIMULATION_CALIBRATED
            and OPEN_MODEL_CALIBRATED
        ),
        "launch_rule": (
            "all fixed-H1 consumed rolling folds must pass score and diagnostic "
            "gates; a rigorous launch additionally requires calibrated gates "
            "and a calibrated open model; exploratory consumption is opt-in"
        ),
        "consumed_sensitivity": sensitivity,
        "frozen_protocol": _protocol_payload(frozen),
        "future_plan": {
            "bands_half_open": FUTURE_BANDS,
            "integer_start_score_block_size": SCORE_BLOCK_SIZE,
            "expected_block_counts": (256, 512),
            "parameters_updated_on_future_data": False,
            "model_reselection_on_future_data": False,
            "maximum_replications_per_band": 1,
            "future_bands_accessed_during_preparation": False,
        },
        "evidence_ledgers": ledger,
        "broad_tail_sensitivity": {
            "calibrated": False,
            "probability": None,
            "is_open_model": False,
            "role": "broad-tail score sensitivity only; excluded from RG2 claims",
        },
        "implementation_sha256": implementation_sha256,
        "proof_warning": PROOF_WARNING,
        "interpretation_warning": INTERPRETATION_WARNING,
        "replication_warning": REPLICATION_WARNING,
    }
    manifest["manifest_digest"] = evidence_payload_digest(manifest)
    return manifest, state, frozen


def prepare_accelerated_protocol() -> dict[str, object]:
    """Build consumed data only and return an unpersisted manifest candidate.

    Calling this function does not create a manifest file and cannot authorize
    either future band.  Persisting the returned JSON is an explicit external
    governance action.  A manifest with ``candidate_prequalified == False`` is
    permanently ineligible for the default future runner.
    """

    manifest, _, _ = _prepare_internal()
    return manifest


def _canonical_manifest_digest(manifest: Mapping[str, object]) -> str:
    payload = dict(manifest)
    payload.pop("manifest_digest", None)
    return evidence_payload_digest(payload)


def _canonical_reservation_digest(reservation: Mapping[str, object]) -> str:
    payload = dict(reservation)
    payload.pop("reservation_digest", None)
    return evidence_payload_digest(payload)


def _canonical_claim_digest(claim: Mapping[str, object]) -> str:
    payload = dict(claim)
    payload.pop("claim_digest", None)
    return evidence_payload_digest(payload)


def _canonical_result_digest(result: Mapping[str, object]) -> str:
    payload = dict(result)
    payload.pop("result_digest", None)
    return evidence_payload_digest(payload)


def _atomic_write_json(
    path: Path, payload: Mapping[str, object], *, exclusive: bool
) -> None:
    """Write canonical JSON, optionally using create-if-absent semantics."""

    encoded = (
        json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        + "\n"
    ).encode("utf-8")
    if exclusive:
        descriptor = os.open(
            path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
        return

    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        descriptor = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(encoded)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def _read_json_mapping(path: Path, label: str) -> Mapping[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} is unreadable") from error
    if not isinstance(payload, Mapping):
        raise RuntimeError(f"{label} must be a JSON object")
    return payload


def _verify_persisted_manifest_static(manifest: object) -> Mapping[str, object]:
    if not isinstance(manifest, Mapping):
        raise RuntimeError("persisted accelerated protocol must be a JSON object")
    if manifest.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError("persisted accelerated protocol schema does not match")
    expected = _canonical_manifest_digest(manifest)
    if manifest.get("manifest_digest") != expected:
        raise RuntimeError("persisted accelerated protocol digest does not match")
    if manifest.get("consumed_limit_inclusive") != CONSUMED_LIMIT:
        raise RuntimeError("persisted protocol consumed frontier changed")
    if manifest.get("future_limit_inclusive") != FUTURE_LIMIT:
        raise RuntimeError("persisted protocol future frontier changed")
    design = manifest.get("design_fixed_before_future_access")
    if not isinstance(design, Mapping) or (
        design.get("depth") != DESIGN_DEPTH
        or design.get("endpoint_residue_bits") != DESIGN_RESIDUE_BITS
        or design.get("valuation_cap") != VALUATION_CAP
        or design.get("integer_start_score_block_size") != SCORE_BLOCK_SIZE
    ):
        raise RuntimeError("persisted fixed design does not match executable design")
    future = manifest.get("future_plan")
    if not isinstance(future, Mapping) or tuple(
        tuple(pair) for pair in future.get("bands_half_open", ())
    ) != FUTURE_BANDS:
        raise RuntimeError("persisted future bands do not match locked plan")
    if not bool(manifest.get("candidate_prequalified")):
        raise RuntimeError(
            "fixed H1 failed consumed prequalification; untouched future bands are preserved"
        )
    return manifest


def _future_statistical_source_ids() -> tuple[str, ...]:
    return tuple(
        source
        for start, stop in FUTURE_BANDS
        for source in _odd_statistical_source_blocks(start, stop)
    )


def _reservation_candidate(
    manifest: Mapping[str, object], launch_mode: str
) -> dict[str, object]:
    frozen = manifest.get("frozen_protocol")
    exact = manifest.get("exact_consumed_frontier")
    if not isinstance(frozen, Mapping) or not isinstance(exact, Mapping):
        raise RuntimeError("future reservation requires frozen and exact manifest state")
    protocol_digest = frozen.get("protocol_digest")
    implementation_digest = manifest.get("implementation_sha256")
    resume_digest = exact.get("resume_chain_sha256")
    state_digest = exact.get("odd_state_sha256")
    if not all(
        isinstance(value, str) and value
        for value in (
            protocol_digest,
            implementation_digest,
            resume_digest,
            state_digest,
        )
    ):
        raise RuntimeError("future reservation manifest bindings are incomplete")
    identity = {
        "manifest_digest": manifest["manifest_digest"],
        "frozen_protocol_digest": protocol_digest,
        "implementation_sha256": implementation_digest,
        "consumed_resume_chain_sha256": resume_digest,
        "consumed_odd_state_sha256": state_digest,
        "future_bands_half_open": FUTURE_BANDS,
        "statistical_source_ids": _future_statistical_source_ids(),
        "exact_extension_source_ids": _all_exact_source_blocks(
            CONSUMED_LIMIT + 1, FUTURE_LIMIT
        ),
    }
    reservation: dict[str, object] = {
        "schema_version": RESERVATION_SCHEMA_VERSION,
        **identity,
        "reservation_id": evidence_payload_digest(identity),
        "launch_mode": launch_mode,
        "status": "reserved",
        "history": ("reserved",),
        "access_claim_scope": (
            "local write-once guard for this reservation path; it does not "
            "certify global historical freshness or form a security boundary"
        ),
    }
    reservation["reservation_digest"] = _canonical_reservation_digest(reservation)
    return reservation


def _launch_mode(
    manifest: Mapping[str, object], allow_exploratory_consumption: bool
) -> str:
    if bool(manifest.get("rigorous_future_launch_authorized")):
        return "rigorous"
    if not allow_exploratory_consumption:
        raise RuntimeError(
            "future execution refused: calibrated rigorous launch gates are not "
            "available; untouched bands are preserved unless exploratory "
            "consumption is explicitly authorized"
        )
    return "exploratory"


def reserve_collatz_accelerated_future(
    manifest_path: object,
    reservation_path: object,
    *,
    allow_exploratory_consumption: bool = False,
) -> dict[str, object]:
    """Persist a write-once local reservation without accessing future starts.

    The reservation records the exact odd-direct sources and exact-extension
    sources that a later run would spend.  Creation is exclusive, so a second
    reservation at the same path is refused rather than overwritten.
    """

    manifest_file = Path(manifest_path)
    if not manifest_file.is_file():
        raise RuntimeError("future reservation refused: persisted manifest is missing")
    manifest = _verify_persisted_manifest_static(
        _read_json_mapping(manifest_file, "persisted manifest")
    )
    mode = _launch_mode(manifest, allow_exploratory_consumption)
    reservation_file = Path(reservation_path)
    if not reservation_file.parent.is_dir():
        raise RuntimeError("future reservation refused: parent directory is missing")
    if Path(str(reservation_file) + ".claim").exists():
        raise RuntimeError("future reservation refused: source claim already exists")
    reservation = _reservation_candidate(manifest, mode)
    try:
        _atomic_write_json(reservation_file, reservation, exclusive=True)
    except FileExistsError as error:
        raise RuntimeError(
            "future reservation refused: reservation path already exists"
        ) from error
    return reservation


def _verify_reservation_static(
    reservation: object,
    manifest: Mapping[str, object],
    launch_mode: str,
) -> Mapping[str, object]:
    if not isinstance(reservation, Mapping):
        raise RuntimeError("future reservation must be a JSON object")
    if reservation.get("schema_version") != RESERVATION_SCHEMA_VERSION:
        raise RuntimeError("future reservation schema does not match")
    if reservation.get("reservation_digest") != _canonical_reservation_digest(
        reservation
    ):
        raise RuntimeError("future reservation digest does not match")
    expected = _reservation_candidate(manifest, launch_mode)
    fixed_fields = (
        "manifest_digest",
        "frozen_protocol_digest",
        "implementation_sha256",
        "consumed_resume_chain_sha256",
        "consumed_odd_state_sha256",
        "future_bands_half_open",
        "statistical_source_ids",
        "exact_extension_source_ids",
        "reservation_id",
        "launch_mode",
    )
    for field in fixed_fields:
        if evidence_payload_digest(reservation.get(field)) != evidence_payload_digest(
            expected[field]
        ):
            raise RuntimeError(f"future reservation {field} does not match")
    if reservation.get("status") != "reserved" or tuple(
        reservation.get("history", ())
    ) != ("reserved",):
        raise RuntimeError("future reservation has already been claimed or completed")
    return reservation


def _claim_reservation(
    path: Path, reservation: Mapping[str, object]
) -> Mapping[str, object]:
    claim = {
        "schema_version": RESERVATION_SCHEMA_VERSION,
        "reservation_id": reservation["reservation_id"],
        "manifest_digest": reservation["manifest_digest"],
        "frozen_protocol_digest": reservation["frozen_protocol_digest"],
        "implementation_sha256": reservation["implementation_sha256"],
        "consumed_resume_chain_sha256": reservation[
            "consumed_resume_chain_sha256"
        ],
        "consumed_odd_state_sha256": reservation["consumed_odd_state_sha256"],
        "claimed_reservation_digest": reservation["reservation_digest"],
        "status": "claimed",
    }
    claim["claim_digest"] = _canonical_claim_digest(claim)
    claim_path = Path(str(path) + ".claim")
    try:
        _atomic_write_json(claim_path, claim, exclusive=True)
    except FileExistsError as error:
        raise RuntimeError(
            "future execution refused: reservation source claim already exists"
        ) from error
    persisted = _read_json_mapping(claim_path, "future source claim")
    if persisted.get("claim_digest") != _canonical_claim_digest(persisted):
        raise RuntimeError("future source claim failed its canonical digest audit")
    for field in (
        "reservation_id",
        "manifest_digest",
        "frozen_protocol_digest",
        "implementation_sha256",
        "consumed_resume_chain_sha256",
        "consumed_odd_state_sha256",
    ):
        if persisted.get(field) != reservation.get(field):
            raise RuntimeError(f"future source claim {field} does not match")
    return persisted


def _transition_reservation(
    path: Path,
    previous: Mapping[str, object],
    status: str,
    **fields: object,
) -> dict[str, object]:
    current = _read_json_mapping(path, "future reservation")
    if current.get("reservation_digest") != previous.get("reservation_digest"):
        raise RuntimeError("future reservation changed during execution")
    updated = dict(current)
    updated.update(fields)
    updated["status"] = status
    updated["history"] = tuple(current.get("history", ())) + (status,)
    updated.pop("reservation_digest", None)
    updated["reservation_digest"] = _canonical_reservation_digest(updated)
    _atomic_write_json(path, updated, exclusive=False)
    return updated


def _protocol_from_payload(payload: object) -> _FrozenProtocol:
    if not isinstance(payload, Mapping):
        raise RuntimeError("persisted frozen protocol is missing")
    early = tuple(
        (str(pair[0]), int(pair[1])) for pair in payload["early_terminal_counts"]
    )
    protocol = _FrozenProtocol(
        depth=int(payload["depth"]),
        residue_bits=int(payload["residue_bits"]),
        valuation_cap=int(payload["valuation_cap"]),
        fit_range=tuple(int(value) for value in payload["fit_range_half_open"]),
        base_coefficients=tuple(float(value) for value in payload["base_coefficients"]),
        residue_adjustments=tuple(
            (int(pair[0]), float(pair[1])) for pair in payload["residue_adjustments"]
        ),
        supported_endpoint_residues=tuple(
            int(value) for value in payload["supported_endpoint_residues"]
        ),
        h1_base_coefficients=tuple(
            float(value) for value in payload["h1_base_coefficients"]
        ),
        h1_residue_adjustments=tuple(
            (int(pair[0]), float(pair[1]))
            for pair in payload["h1_residue_adjustments"]
        ),
        origin_coefficients=tuple(float(value) for value in payload["origin_coefficients"]),
        h0_scale=float(payload["h0_student_t_scale"]),
        h1_scale=float(payload["h1_student_t_scale"]),
        broad_tail_scale=float(payload["broad_tail_sensitivity"]["scale"]),
        fit_statistical_count=int(payload["fit_statistical_count"]),
        early_terminal_counts=early,
        fit_data_sha256=str(payload["fit_data_sha256"]),
        scale_calibration=str(payload["scale_calibration"]),
        digest=str(payload["protocol_digest"]),
    )
    if evidence_payload_digest(_protocol_payload(protocol, include_digest=False)) != protocol.digest:
        raise RuntimeError("persisted frozen protocol digest does not match")
    return protocol


def _future_ledger_summary(
    bands: Sequence[Mapping[str, object]],
    exact: Mapping[str, object],
    consumed_exact: Mapping[str, object],
    manifest_digest: str,
) -> dict[str, object]:
    statistical = EvidenceLedger()
    for index, band in enumerate(bands, 1):
        observation = {
            "range_half_open": band["range_half_open"],
            "frozen_protocol_digest": band["frozen_protocol_digest"],
            "persisted_manifest_digest": manifest_digest,
            "h1_over_h0_mean_log_score_gain": band[
                "h1_over_h0_mean_log_score_gain"
            ],
            "score_gates_passed": band["score_gates_passed"],
            "diagnostic_gates_passed": band["diagnostic_gates_passed"],
            "formal_replication": False,
        }
        start, stop = (int(value) for value in band["range_half_open"])
        statistical = statistical.append(
            EvidenceRecord(
                record_id=f"collatz_accelerated_future_band_{index}",
                source_ids=_odd_statistical_source_blocks(start, stop),
                action="locked_future_transport_score",
                coordinate=float(index),
                digest=evidence_payload_digest(observation),
                family="student_t_block_scores",
                scope="locally_claimed_locked_transport",
                observation=observation,
                joint=True,
            )
        )
    extension_status_counts = {
        key: int(exact["status_counts"][key])
        - int(consumed_exact["status_counts"][key])
        for key in ("reached_one", "resource_limit", "verified_cycle")
    }
    exact_observation = {
        "full_frontier_scope_inclusive": exact["scope_inclusive"],
        "extension_scope_inclusive": (CONSUMED_LIMIT + 1, FUTURE_LIMIT),
        "extension_status_counts": extension_status_counts,
        "parent_resume_chain_sha256": consumed_exact["resume_chain_sha256"],
        "parent_odd_state_sha256": consumed_exact["odd_state_sha256"],
        "extended_resume_chain_sha256": exact["resume_chain_sha256"],
        "extended_odd_state_sha256": exact["odd_state_sha256"],
        "persisted_manifest_digest": manifest_digest,
    }
    exact_ledger = EvidenceLedger().append(
        EvidenceRecord(
            record_id="collatz_accelerated_bounded_exact_through_2pow24",
            source_ids=_all_exact_source_blocks(CONSUMED_LIMIT + 1, FUTURE_LIMIT),
            action="manifest_authorized_exact_extension",
            coordinate=None,
            digest=evidence_payload_digest(exact_observation),
            family="exact_integer_computation",
            scope="bounded_exact",
            observation=exact_observation,
            joint=True,
        )
    )
    return {
        "future_statistical_record_ids": statistical.record_ids,
        "future_statistical_source_count": len(statistical.source_ids),
        "bounded_exact_record_ids": exact_ledger.record_ids,
        "bounded_exact_source_count": len(exact_ledger.source_ids),
        "separate_statistical_and_exact_ledgers": True,
        "score_blocks_are_replications": False,
    }


def run_collatz_accelerated_endpoint(
    manifest_path: Optional[object] = None,
    reservation_path: Optional[object] = None,
    *,
    allow_exploratory_consumption: bool = False,
) -> dict[str, object]:
    """Run locked future bands after manifest reproduction and a one-shot claim.

    By default, an uncalibrated rigorous launch is refused.  Explicit
    exploratory consumption still requires a prequalified candidate and a
    separately persisted reservation.  The immutable ``.claim`` sidecar is
    created immediately before future access and is never reclaimed.
    """

    if manifest_path is None:
        raise RuntimeError(
            "future execution refused: pass a persisted accelerated protocol manifest"
        )
    if reservation_path is None:
        raise RuntimeError(
            "future execution refused: pass a persisted one-shot source reservation"
        )
    path = Path(manifest_path)
    reservation_file = Path(reservation_path)
    if not path.is_file():
        raise RuntimeError("future execution refused: persisted manifest is missing")
    if not reservation_file.is_file():
        raise RuntimeError("future execution refused: source reservation is missing")
    persisted = _verify_persisted_manifest_static(
        _read_json_mapping(path, "persisted manifest")
    )
    launch_mode = _launch_mode(persisted, allow_exploratory_consumption)
    reservation = _verify_reservation_static(
        _read_json_mapping(reservation_file, "future reservation"),
        persisted,
        launch_mode,
    )
    claim_file = Path(str(reservation_file) + ".claim")
    result_file = Path(str(reservation_file) + ".result.json")
    if claim_file.exists():
        raise RuntimeError(
            "future execution refused: reservation source claim already exists"
        )
    if result_file.exists():
        raise RuntimeError(
            "future execution refused: reservation result artifact already exists"
        )

    # Reproduce everything consumed while the state is still hard-capped at
    # 2**22.  Even a valid-looking manifest cannot authorize future allocation
    # until this canonical comparison succeeds.
    reproduced, state, reproduced_protocol = _prepare_internal()
    if reproduced["manifest_digest"] != persisted["manifest_digest"]:
        raise RuntimeError(
            "future execution refused: consumed protocol did not reproduce persisted digest"
        )
    persisted_protocol = _protocol_from_payload(persisted["frozen_protocol"])
    if persisted_protocol.digest != reproduced_protocol.digest:
        raise RuntimeError("future execution refused: frozen protocol did not reproduce")
    persisted_exact = persisted["exact_consumed_frontier"]
    if (
        persisted_exact["resume_chain_sha256"] != state.chain_sha256
        or persisted_exact["odd_state_sha256"] != state.state_sha256()
    ):
        raise RuntimeError("future execution refused: consumed exact frontier did not reproduce")

    # The O_EXCL sidecar is the irrevocable local access-claim event.  It shows
    # that this runner's claim predated access at this path; it does not prove
    # global historical freshness or act as a security boundary.
    _claim_reservation(reservation_file, reservation)
    active_reservation: Optional[Mapping[str, object]] = None
    try:
        active_reservation = _transition_reservation(
            reservation_file,
            reservation,
            "access_committed",
            local_access_claim_committed=True,
        )

        # This is the sole authorized extension point in the module.
        state.extend_to(
            FUTURE_LIMIT, _authorization=_FUTURE_EXTENSION_AUTHORIZATION
        )
        exact = state.summary()
        if not (
            bool(exact["all_reached_one"])
            and bool(exact["all_direct_record_audits_match"])
            and bool(exact["all_affine_toll_audits_hold"])
        ):
            raise RuntimeError("future exact frontier failed quarantine; scoring refused")
        bands = []
        for index, band_range in enumerate(FUTURE_BANDS, 1):
            score = _score_range(
                state,
                persisted_protocol,
                band_range,
                f"locked_future_band_{index}",
                manifest_digest=str(persisted["manifest_digest"]),
            )
            score.update(
                {
                    "band_index": index,
                    "local_claim_predated_access": True,
                    "source_reservation_id": reservation["reservation_id"],
                    "launch_mode": launch_mode,
                    "persisted_manifest_verified_before_extension": True,
                    "consumed_protocol_reproduced_before_extension": True,
                    "frozen_protocol_digest": persisted_protocol.digest,
                    "persisted_manifest_digest": persisted["manifest_digest"],
                    "parameters_updated_on_band": False,
                    "model_reselection_performed": False,
                    "maximum_replication_count": 1,
                    "formal_replication": False,
                    "formal_replication_reason": (
                        "the broad-tail sensitivity is not a calibrated open "
                        "model; directional transport is not an RG2 promotion"
                    ),
                }
            )
            bands.append(score)
        ledger = _future_ledger_summary(
            bands,
            exact,
            persisted_exact,
            str(persisted["manifest_digest"]),
        )
        directional_passes = sum(
            bool(band["score_gates_passed"] and band["diagnostic_gates_passed"])
            for band in bands
        )
        result = {
            "experiment": "accelerated odd-jump endpoint-matched valuation transport",
            "persisted_manifest_path": str(path),
            "persisted_manifest_digest": persisted["manifest_digest"],
            "candidate_prequalified_on_consumed_rolling_folds": True,
            "launch_mode": launch_mode,
            "exact_frontier": exact,
            "future_bands": tuple(bands),
            "directional_locked_band_pass_count": directional_passes,
            "formal_replication_count": 0,
            "statistical_state": (
                "TWO_DIRECTIONAL_LOCKED_PASSES_UNCALIBRATED"
                if directional_passes == 2
                else "LOCKED_TRANSPORT_DID_NOT_CLEAR_BOTH_BANDS"
            ),
            "broad_tail_sensitivity": {
                "is_open_model": False,
                "calibrated": False,
                "probability": None,
                "formal_gate_available": False,
            },
            "evidence_ledgers": ledger,
            "proof_warning": PROOF_WARNING,
            "interpretation_warning": INTERPRETATION_WARNING,
            "replication_warning": REPLICATION_WARNING,
            "source_reservation": {
                "path": str(reservation_file),
                "reservation_id": active_reservation["reservation_id"],
                "claim_path": str(claim_file),
                "local_claim_predated_access": True,
                "global_historical_freshness_certified": False,
            },
            "persisted_result_path": str(result_file),
        }
        result["result_digest"] = _canonical_result_digest(result)
        _atomic_write_json(result_file, result, exclusive=True)
        persisted_result = _read_json_mapping(
            result_file, "future result artifact"
        )
        if persisted_result.get("result_digest") != _canonical_result_digest(
            persisted_result
        ) or persisted_result.get("result_digest") != result["result_digest"]:
            raise RuntimeError("future result artifact failed its digest audit")
        _transition_reservation(
            reservation_file,
            active_reservation,
            "completed",
            result_path=str(result_file),
            result_digest=result["result_digest"],
        )
        return result
    except BaseException as error:
        if active_reservation is not None:
            try:
                _transition_reservation(
                    reservation_file,
                    active_reservation,
                    "failed_unknown",
                    failure_type=type(error).__name__,
                )
            except Exception:
                # The immutable claim still records the local access commitment.
                pass
        raise


if __name__ == "__main__":
    # Deliberately safe: module execution demonstrates the refusal path and
    # never prepares or touches a future start implicitly.
    try:
        run_collatz_accelerated_endpoint()
    except RuntimeError as error:
        print(json.dumps({"status": "REFUSED", "reason": str(error)}, indent=2))
