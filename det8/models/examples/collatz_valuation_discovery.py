"""Exact Collatz valuation-tree discovery with a model-selection band.

This module keeps two logically separate layers:

* an exact, hash-checkpointed arithmetic census using descent certificates; and
* descriptive model comparison for finite-range stopping-time structure.

The default run computes starts through ``2**20`` in exact arithmetic. Its
predictive models are trained only on ``[2**18, 2**19)`` and evaluated once on the locked interval
``[2**19, 2**20)``, which selects the reported panel winner and is therefore
not a post-selection replication. No finite result is promoted to a proof of
the Collatz conjecture.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from array import array
from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from det8.models.relational_evidence import (
    EvidenceLedger,
    EvidenceRecord,
    StudentT,
    evidence_payload_digest,
)


DEFAULT_LIMIT = 1 << 20
DEFAULT_CHECKPOINT_SIZE = 1 << 18
DEFAULT_TRAIN_RANGE = (1 << 18, 1 << 19)
DEFAULT_HOLDOUT_RANGE = (1 << 19, 1 << 20)
TREE_DEPTHS = tuple(range(3, 11))

def collatz_proof_warning(limit: int) -> str:
    return (
        f"Exact convergence through {limit} is a bounded exact computation, "
        "not an independently replayable certificate or a proof of the "
        "Collatz conjecture. A resource limit is unresolved, and predictive "
        "model weights or scores are not conjecture probabilities."
    )


PROOF_WARNING = collatz_proof_warning(DEFAULT_LIMIT)
MODEL_WARNING = (
    "The model-selection-band scores compare finite-range workload descriptions. "
    "Residue, valuation, drift, record, and coalescence structure cannot by "
    "themselves establish convergence or divergence."
)

_REACHED = 1
_RESOURCE = 2
_CYCLE = 3
_STATUS_NAME = {
    _REACHED: "reached_one",
    _RESOURCE: "resource_limit",
    _CYCLE: "verified_cycle",
}


def _ordinary_next(value: int) -> int:
    return value // 2 if value % 2 == 0 else 3 * value + 1


def two_adic_valuation(value: int) -> int:
    """Return v_2(value) for a positive integer."""

    if value < 1:
        raise ValueError("two-adic valuation requires a positive integer")
    return (value & -value).bit_length() - 1


def accelerated_odd_step(value: int) -> tuple[int, int]:
    """Return ``(A(value), v_2(3*value+1))`` for positive odd ``value``."""

    if value < 1 or value % 2 == 0:
        raise ValueError("accelerated Collatz input must be a positive odd integer")
    expanded = 3 * value + 1
    valuation = two_adic_valuation(expanded)
    return expanded >> valuation, valuation


def valuation_prefix(value: int, depth: int = 10) -> tuple[int, ...]:
    """Return a zero-padded prefix of accelerated-map valuations."""

    if value < 1 or value % 2 == 0:
        raise ValueError("valuation prefixes require a positive odd integer")
    if depth < 1:
        raise ValueError("valuation-prefix depth must be positive")
    prefix: list[int] = []
    current = value
    while len(prefix) < depth and current != 1:
        current, valuation = accelerated_odd_step(current)
        prefix.append(valuation)
    prefix.extend(0 for _ in range(depth - len(prefix)))
    return tuple(prefix)


def _canonical_cycle(cycle: Iterable[int]) -> tuple[int, ...]:
    values = tuple(cycle)
    if not values:
        return ()
    rotations = tuple(values[index:] + values[:index] for index in range(len(values)))
    return min(rotations)


@dataclass
class _FrontierState:
    steps: array
    peaks: list[int]
    status: bytearray
    odd_steps: array
    odd_toll: array


def _new_checkpoint(start: int) -> dict[str, object]:
    return {
        "start": start,
        "status_counts": Counter(),
        "maximum_total_stopping_time": -1,
        "maximum_total_stopping_time_start": None,
        "maximum_peak": -1,
        "maximum_peak_start": None,
        "hasher": hashlib.sha256(),
    }


def _finalize_checkpoint(
    block: dict[str, object],
    stop: int,
    prior_chain: str,
    cumulative_time_record: int,
    cumulative_peak_record: int,
) -> tuple[dict[str, object], str]:
    hasher = block.pop("hasher")
    assert isinstance(hasher, object) and hasattr(hasher, "hexdigest")
    block_digest = hasher.hexdigest()
    chain_digest = hashlib.sha256(
        (
            f"{prior_chain}:{block['start']}:{stop}:{block_digest}"
        ).encode("ascii")
    ).hexdigest()
    counts = dict(block["status_counts"])
    for name in _STATUS_NAME.values():
        counts.setdefault(name, 0)
    block["status_counts"] = counts
    block["stop"] = stop
    block["tested_count"] = stop - int(block["start"]) + 1
    block["all_reached_one"] = counts["reached_one"] == block["tested_count"]
    block["block_sha256"] = block_digest
    block["chain_sha256"] = chain_digest
    block["new_stopping_time_record"] = (
        int(block["maximum_total_stopping_time"]) > cumulative_time_record
    )
    block["new_peak_record"] = int(block["maximum_peak"]) > cumulative_peak_record
    return block, chain_digest


def _build_exact_frontier(
    limit: int,
    checkpoint_size: int,
    max_descent_steps: int,
) -> tuple[dict[str, object], _FrontierState]:
    if limit < 1:
        raise ValueError("frontier limit must be positive")
    if checkpoint_size < 1:
        raise ValueError("checkpoint size must be positive")
    if max_descent_steps < 1:
        raise ValueError("descent-step limit must be positive")

    started = time.perf_counter()
    steps = array("i", [-1]) * (limit + 1)
    peaks = [0] * (limit + 1)
    status = bytearray(limit + 1)
    steps[1] = 0
    peaks[1] = 1
    status[1] = _REACHED

    chain_digest = hashlib.sha256(
        f"collatz-valuation-discovery-v1:{limit}:{checkpoint_size}".encode("ascii")
    ).hexdigest()
    checkpoints: list[dict[str, object]] = []
    exceptions: list[dict[str, object]] = []
    time_record = -1
    time_record_start = 1
    peak_record = -1
    peak_record_start = 1
    record_starts: set[int] = {1}
    counts: Counter[str] = Counter()
    ordinary_merge_step_sum = 0
    ordinary_merge_step_max = 0
    ordinary_merge_step_max_start = 1
    block = _new_checkpoint(1)

    for start in range(1, limit + 1):
        repeated_value: int | None = None
        merge_value = 1
        descent_steps = 0
        if start == 1:
            result_status = _REACHED
            result_steps = 0
            result_peak = 1
        else:
            current = start
            path: list[int] = []
            seen: dict[int, int] = {}
            result_status = _REACHED
            while current >= start:
                if current in seen:
                    result_status = _CYCLE
                    repeated_value = current
                    cycle = _canonical_cycle(path[seen[current] :])
                    exceptions.append(
                        {
                            "start": start,
                            "status": "verified_cycle",
                            "cycle": cycle,
                        }
                    )
                    break
                if len(path) >= max_descent_steps:
                    result_status = _RESOURCE
                    exceptions.append(
                        {
                            "start": start,
                            "status": "resource_limit",
                            "steps_before_limit": len(path),
                            "terminal": current,
                        }
                    )
                    break
                seen[current] = len(path)
                path.append(current)
                current = _ordinary_next(current)

            descent_steps = len(path)
            merge_value = current
            if result_status == _REACHED:
                if current < 1 or current >= start or not status[current]:
                    raise RuntimeError("descent certificate reached an invalid predecessor")
                result_status = status[current]
                if result_status == _REACHED:
                    result_steps = descent_steps + int(steps[current])
                    result_peak = max(max(path, default=start), peaks[current])
                else:
                    result_steps = -1
                    result_peak = max(path, default=start)
                    exceptions.append(
                        {
                            "start": start,
                            "status": _STATUS_NAME[result_status],
                            "inherited_from": current,
                        }
                    )
            else:
                result_steps = -1
                result_peak = max(max(path, default=start), current)

            steps[start] = result_steps
            peaks[start] = result_peak
            status[start] = result_status

        counts[_STATUS_NAME[result_status]] += 1
        block_counts = block["status_counts"]
        assert isinstance(block_counts, Counter)
        block_counts[_STATUS_NAME[result_status]] += 1
        if result_status == _REACHED:
            if result_steps > int(block["maximum_total_stopping_time"]):
                block["maximum_total_stopping_time"] = result_steps
                block["maximum_total_stopping_time_start"] = start
            if result_peak > int(block["maximum_peak"]):
                block["maximum_peak"] = result_peak
                block["maximum_peak_start"] = start
            if result_steps > time_record:
                time_record = result_steps
                time_record_start = start
                record_starts.add(start)
            if result_peak > peak_record:
                peak_record = result_peak
                peak_record_start = start
                record_starts.add(start)
        ordinary_merge_step_sum += descent_steps
        if descent_steps > ordinary_merge_step_max:
            ordinary_merge_step_max = descent_steps
            ordinary_merge_step_max_start = start

        hasher = block["hasher"]
        hasher.update(
            (
                f"{start}:{_STATUS_NAME[result_status]}:{result_steps}:"
                f"{result_peak}:{merge_value}:{descent_steps}:{repeated_value};"
            ).encode("ascii")
        )

        if start % checkpoint_size == 0 or start == limit:
            finalized, chain_digest = _finalize_checkpoint(
                block,
                start,
                chain_digest,
                max(
                    (
                        int(item["maximum_total_stopping_time"])
                        for item in checkpoints
                    ),
                    default=-1,
                ),
                max((int(item["maximum_peak"]) for item in checkpoints), default=-1),
            )
            checkpoints.append(finalized)
            if start < limit:
                block = _new_checkpoint(start + 1)

    odd_steps = array("i", [-1]) * (limit + 1)
    odd_toll = array("i", [-1]) * (limit + 1)
    odd_steps[1] = 0
    odd_toll[1] = 0
    accelerated_consistency_failures: list[dict[str, object]] = []
    first_descent_histogram: Counter[int] = Counter()
    total_odd_step_sum = 0
    maximum_total_odd_steps = 0
    maximum_total_odd_steps_start = 1
    first_descent_sum = 0
    first_descent_max = 0
    first_descent_max_start = 1
    merge_ratio_sum = 0.0
    merge_below_half = 0
    delayed_merges: list[tuple[int, int, int, tuple[int, ...]]] = []

    for start in range(3, limit + 1, 2):
        current = start
        path_valuations: list[int] = []
        seen: set[int] = set()
        while current >= start:
            if current in seen or len(path_valuations) >= max_descent_steps:
                accelerated_consistency_failures.append(
                    {
                        "start": start,
                        "reason": (
                            "accelerated_repeat"
                            if current in seen
                            else "accelerated_resource_limit"
                        ),
                        "terminal": current,
                    }
                )
                break
            seen.add(current)
            current, valuation = accelerated_odd_step(current)
            path_valuations.append(valuation)
        if current >= start or current < 1 or odd_steps[current] < 0:
            continue
        odd_steps[start] = len(path_valuations) + odd_steps[current]
        odd_toll[start] = (
            sum(1 + valuation for valuation in path_valuations) + odd_toll[current]
        )
        if status[start] != _REACHED or odd_toll[start] != steps[start]:
            accelerated_consistency_failures.append(
                {
                    "start": start,
                    "reason": "ordinary_accelerated_toll_mismatch",
                    "ordinary_steps": int(steps[start]),
                    "accelerated_toll": int(odd_toll[start]),
                }
            )
        total_odd_step_sum += odd_steps[start]
        if odd_steps[start] > maximum_total_odd_steps:
            maximum_total_odd_steps = odd_steps[start]
            maximum_total_odd_steps_start = start
        descent = len(path_valuations)
        first_descent_histogram[descent] += 1
        first_descent_sum += descent
        merge_ratio_sum += current / start
        merge_below_half += current * 2 < start
        if descent > first_descent_max:
            first_descent_max = descent
            first_descent_max_start = start
        delayed_merges.append((descent, start, current, tuple(path_valuations[:10])))

    delayed_merges.sort(reverse=True)
    delayed_merges = delayed_merges[:10]
    odd_count = (limit + 1) // 2
    state = _FrontierState(steps, peaks, status, odd_steps, odd_toll)
    summary = {
        "certified_range": (1, limit),
        "tested_count": limit,
        "status_counts": {
            name: counts.get(name, 0) for name in _STATUS_NAME.values()
        },
        "all_reached_one": counts.get("reached_one", 0) == limit,
        "maximum_total_stopping_time": time_record,
        "maximum_total_stopping_time_start": time_record_start,
        "maximum_peak": peak_record,
        "maximum_peak_start": peak_record_start,
        "checkpoint_size": checkpoint_size,
        "checkpoints": checkpoints,
        "resume_token": chain_digest,
        "exceptions": exceptions,
        "record_starts": tuple(sorted(record_starts)),
        "descent_certificate": {
            "method": "ascending exact paths terminating at a certified smaller start",
            "mean_ordinary_steps_to_certificate": ordinary_merge_step_sum / limit,
            "maximum_ordinary_steps_to_certificate": ordinary_merge_step_max,
            "maximum_ordinary_steps_start": ordinary_merge_step_max_start,
        },
        "accelerated_odd_map": {
            "tested_odd_starts": odd_count,
            "ordinary_toll_identity_holds": not accelerated_consistency_failures,
            "consistency_failure_count": len(accelerated_consistency_failures),
            "consistency_failures": accelerated_consistency_failures[:20],
            "mean_total_odd_steps": total_odd_step_sum / max(odd_count - 1, 1),
            "maximum_total_odd_steps": maximum_total_odd_steps,
            "maximum_total_odd_steps_start": maximum_total_odd_steps_start,
            "first_descent_mean_odd_steps": first_descent_sum / max(odd_count - 1, 1),
            "first_descent_maximum_odd_steps": first_descent_max,
            "first_descent_maximum_start": first_descent_max_start,
            "first_descent_histogram": dict(sorted(first_descent_histogram.items())),
            "mean_merge_height_ratio": merge_ratio_sum / max(odd_count - 1, 1),
            "fraction_merging_below_half": merge_below_half / max(odd_count - 1, 1),
            "most_delayed_coalescences": tuple(
                {
                    "odd_steps_to_lower_certificate": depth,
                    "start": start,
                    "merge_value": merge,
                    "valuation_prefix": prefix,
                }
                for depth, start, merge, prefix in delayed_merges
            ),
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    return summary, state


def exact_certified_frontier(
    limit: int = DEFAULT_LIMIT,
    *,
    checkpoint_size: int = DEFAULT_CHECKPOINT_SIZE,
    max_descent_steps: int = 10_000,
) -> dict[str, object]:
    """Return an exact bounded frontier without exposing internal arrays."""

    summary, _ = _build_exact_frontier(limit, checkpoint_size, max_descent_steps)
    return summary


def _odd_feature_row(start: int, steps: array, depth: int = 10) -> dict[str, object]:
    first_target, first_valuation = accelerated_odd_step(start)
    prefix = valuation_prefix(start, depth)
    return {
        "start": start,
        "target": int(steps[start]),
        "height": math.log2(start),
        "first_target_height": math.log2(first_target),
        "first_toll": 1 + first_valuation,
        "first_valuation": first_valuation,
        "prefix": prefix,
    }


def _linear_fit(pairs: Iterable[tuple[float, float]]) -> dict[str, float]:
    count = 0
    sx = sy = sxx = sxy = 0.0
    for x_value, y_value in pairs:
        count += 1
        sx += x_value
        sy += y_value
        sxx += x_value * x_value
        sxy += x_value * y_value
    if count < 2:
        raise ValueError("linear fit requires at least two observations")
    denominator = count * sxx - sx * sx
    slope = 0.0 if abs(denominator) < 1e-15 else (
        count * sxy - sx * sy
    ) / denominator
    intercept = (sy - slope * sx) / count
    return {"intercept": intercept, "slope": slope, "count": float(count)}


def _predict_baseline(row: dict[str, object], fit: dict[str, float]) -> float:
    return fit["intercept"] + fit["slope"] * float(row["height"])


def _predict_first_jump(row: dict[str, object], fit: dict[str, float]) -> float:
    return (
        float(row["first_toll"])
        + fit["intercept"]
        + fit["slope"] * float(row["first_target_height"])
    )


def _group_add(
    groups: dict[object, list[float]], key: object, residual: float
) -> None:
    cell = groups.get(key)
    if cell is None:
        groups[key] = [1.0, residual, residual * residual]
    else:
        cell[0] += 1.0
        cell[1] += residual
        cell[2] += residual * residual


def _group_adjustment(cell: list[float] | None, shrinkage: float) -> float:
    return 0.0 if cell is None else cell[1] / (cell[0] + shrinkage)


def _gaussian_log_score(error: float, variance: float) -> float:
    safe_variance = max(variance, 1e-12)
    return -0.5 * (
        math.log(2.0 * math.pi * safe_variance) + error * error / safe_variance
    )


def _student_t_scale(variance: float, degrees_of_freedom: float = 5.0) -> float:
    """Choose a Student-t scale with the supplied finite variance."""

    return math.sqrt(max(variance, 1e-12) * (degrees_of_freedom - 2.0) / degrees_of_freedom)


def _mean_contrast(cells: dict[int, list[float]]) -> float:
    return cells[7][0] / cells[7][1] - cells[5][0] / cells[5][1]


def _mean_and_standard_error(values: list[float]) -> tuple[float, float]:
    mean = sum(values) / len(values)
    if len(values) < 2:
        return mean, 0.0
    variance = sum((value - mean) ** 2 for value in values) / (len(values) - 1)
    return mean, math.sqrt(variance / len(values))


def locked_tree_comparison(
    state: _FrontierState,
    *,
    train_range: tuple[int, int] = DEFAULT_TRAIN_RANGE,
    holdout_range: tuple[int, int] = DEFAULT_HOLDOUT_RANGE,
    depths: tuple[int, ...] = TREE_DEPTHS,
    shrinkage: float = 32.0,
) -> dict[str, object]:
    """Fit on one height band and score once on the locked higher band."""

    train_start, train_stop = train_range
    holdout_start, holdout_stop = holdout_range
    if not (1 <= train_start < train_stop <= holdout_start < holdout_stop):
        raise ValueError("training and holdout ranges must be ordered and disjoint")
    if holdout_stop > len(state.steps):
        raise ValueError("locked holdout exceeds the exact certified frontier")
    if not depths or min(depths) < 1 or max(depths) > 20:
        raise ValueError("tree depths must lie between one and twenty")
    score_block_size = 1 << 14
    if (holdout_stop - holdout_start) % score_block_size:
        raise ValueError("locked range must contain complete score blocks")
    score_block_count = (holdout_stop - holdout_start) // score_block_size
    score_block_observations = [0 for _ in range(score_block_count)]
    if shrinkage < 0.0:
        raise ValueError("tree shrinkage cannot be negative")

    train_odds = range(train_start | 1, train_stop, 2)
    baseline_fit = _linear_fit(
        (math.log2(start), float(state.steps[start])) for start in train_odds
    )
    first_jump_fit = _linear_fit(
        (
            math.log2(accelerated_odd_step(start)[0]),
            float(state.steps[start] - (1 + accelerated_odd_step(start)[1])),
        )
        for start in range(train_start | 1, train_stop, 2)
    )

    residue_groups: dict[int, dict[object, list[float]]] = {
        depth: {} for depth in depths
    }
    valuation_groups: dict[int, dict[object, list[float]]] = {
        depth: {} for depth in depths
    }
    train_sse = {"baseline_height": 0.0, "first_jump_controlled": 0.0}
    train_count = 0
    raw_train = {5: [0.0, 0.0], 7: [0.0, 0.0]}
    controlled_train = {5: [0.0, 0.0], 7: [0.0, 0.0]}

    for start in range(train_start | 1, train_stop, 2):
        row = _odd_feature_row(start, state.steps, max(depths))
        target = float(row["target"])
        baseline_error = target - _predict_baseline(row, baseline_fit)
        controlled_error = target - _predict_first_jump(row, first_jump_fit)
        train_sse["baseline_height"] += baseline_error**2
        train_sse["first_jump_controlled"] += controlled_error**2
        train_count += 1
        residue8 = start % 8
        if residue8 in raw_train:
            raw_train[residue8][0] += target
            raw_train[residue8][1] += 1.0
            controlled_train[residue8][0] += controlled_error
            controlled_train[residue8][1] += 1.0
        prefix = row["prefix"]
        assert isinstance(prefix, tuple)
        for depth in depths:
            _group_add(
                residue_groups[depth], start % (1 << depth), controlled_error
            )
            _group_add(valuation_groups[depth], prefix[:depth], controlled_error)

    model_specs: list[dict[str, object]] = [
        {
            "name": "baseline_height",
            "family": "height_only",
            "fit": baseline_fit,
            "train_variance": train_sse["baseline_height"] / train_count,
        },
        {
            "name": "first_jump_controlled",
            "family": "accelerated_first_jump",
            "fit": first_jump_fit,
            "train_variance": train_sse["first_jump_controlled"] / train_count,
        },
    ]
    for family, all_groups in (
        ("residue_tree", residue_groups),
        ("valuation_tree", valuation_groups),
    ):
        for depth in depths:
            group_sse = 0.0
            for cell in all_groups[depth].values():
                adjustment = _group_adjustment(cell, shrinkage)
                group_sse += (
                    cell[2] - 2.0 * adjustment * cell[1]
                    + cell[0] * adjustment * adjustment
                )
            model_specs.append(
                {
                    "name": f"{family}_depth_{depth}",
                    "family": family,
                    "depth": depth,
                    "group_count": len(all_groups[depth]),
                    "train_variance": group_sse / train_count,
                    "groups": all_groups[depth],
                }
            )

    metrics = {
        str(model["name"]): {
            "squared_error": 0.0,
            "log_score": 0.0,
            "student_t_log_score": 0.0,
            "unseen_groups": 0,
            "block_student_t_log_scores": [
                0.0 for _ in range(score_block_count)
            ],
        }
        for model in model_specs
    }
    robust_distributions = {
        str(model["name"]): StudentT(
            0.0, _student_t_scale(float(model["train_variance"])), 5.0
        )
        for model in model_specs
    }
    # A broad robust-open reference asks whether all named workload relations
    # are too narrow. It retains the simple height-only center, doubles the
    # residual scale, and uses heavier Student-t tails.
    baseline_variance = float(model_specs[0]["train_variance"])
    robust_open_distribution = StudentT(
        0.0,
        2.0 * _student_t_scale(baseline_variance),
        3.0,
    )
    robust_open_log_score = 0.0
    robust_open_block_log_scores = [0.0 for _ in range(score_block_count)]
    raw_holdout = {5: [0.0, 0.0], 7: [0.0, 0.0]}
    controlled_holdout = {5: [0.0, 0.0], 7: [0.0, 0.0]}
    holdout_count = 0
    for start in range(holdout_start | 1, holdout_stop, 2):
        block_index = (start - holdout_start) // score_block_size
        row = _odd_feature_row(start, state.steps, max(depths))
        target = float(row["target"])
        base_prediction = _predict_first_jump(row, first_jump_fit)
        baseline_prediction = _predict_baseline(row, baseline_fit)
        robust_open_score = robust_open_distribution.log_prob(
            target - baseline_prediction
        )
        robust_open_log_score += robust_open_score
        robust_open_block_log_scores[block_index] += robust_open_score
        controlled_error = target - base_prediction
        residue8 = start % 8
        if residue8 in raw_holdout:
            raw_holdout[residue8][0] += target
            raw_holdout[residue8][1] += 1.0
            controlled_holdout[residue8][0] += controlled_error
            controlled_holdout[residue8][1] += 1.0
        prefix = row["prefix"]
        assert isinstance(prefix, tuple)
        for model in model_specs:
            name = str(model["name"])
            if name == "baseline_height":
                prediction = _predict_baseline(row, baseline_fit)
            elif name == "first_jump_controlled":
                prediction = base_prediction
            else:
                depth = int(model["depth"])
                key = (
                    start % (1 << depth)
                    if model["family"] == "residue_tree"
                    else prefix[:depth]
                )
                groups = model["groups"]
                assert isinstance(groups, dict)
                cell = groups.get(key)
                if cell is None:
                    metrics[name]["unseen_groups"] += 1
                prediction = base_prediction + _group_adjustment(cell, shrinkage)
            error = target - prediction
            metrics[name]["squared_error"] += error * error
            metrics[name]["log_score"] += _gaussian_log_score(
                error, float(model["train_variance"])
            )
            robust_score = robust_distributions[name].log_prob(error)
            metrics[name]["student_t_log_score"] += robust_score
            metrics[name]["block_student_t_log_scores"][block_index] += robust_score
        score_block_observations[block_index] += 1
        holdout_count += 1

    results = []
    for model in model_specs:
        name = str(model["name"])
        metric = metrics[name]
        results.append(
            {
                "model": name,
                "family": model["family"],
                "depth": model.get("depth"),
                "parameter_or_group_count": (
                    2 if "group_count" not in model else int(model["group_count"]) + 2
                ),
                "train_residual_standard_deviation": math.sqrt(
                    float(model["train_variance"])
                ),
                "holdout_rmse": math.sqrt(
                    metric["squared_error"] / holdout_count
                ),
                "holdout_mean_log_score": metric["log_score"] / holdout_count,
                "holdout_mean_student_t_log_score": (
                    metric["student_t_log_score"] / holdout_count
                ),
                "holdout_observations_with_unseen_group": int(
                    metric["unseen_groups"]
                ),
            }
        )
    results.sort(
        key=lambda row: float(row["holdout_mean_student_t_log_score"]),
        reverse=True,
    )
    baseline_result = next(
        row for row in results if row["model"] == "baseline_height"
    )
    for row in results:
        row["holdout_rmse_improvement_over_baseline"] = (
            float(baseline_result["holdout_rmse"]) - float(row["holdout_rmse"])
        )
        row["student_t_log_score_gain_over_baseline"] = (
            float(row["holdout_mean_student_t_log_score"])
            - float(baseline_result["holdout_mean_student_t_log_score"])
        )

    raw_train_contrast = _mean_contrast(raw_train)
    raw_holdout_contrast = _mean_contrast(raw_holdout)
    controlled_train_contrast = _mean_contrast(controlled_train)
    controlled_holdout_contrast = _mean_contrast(controlled_holdout)
    selected_mean_score = float(results[0]["holdout_mean_student_t_log_score"])
    robust_open_mean_score = robust_open_log_score / holdout_count
    selected_name = str(results[0]["model"])
    first_jump_name = "first_jump_controlled"

    def block_means(name: str) -> list[float]:
        scores = metrics[name]["block_student_t_log_scores"]
        return [
            float(score) / count
            for score, count in zip(scores, score_block_observations)
        ]

    selected_block_scores = block_means(selected_name)
    first_jump_block_scores = block_means(first_jump_name)
    open_block_scores = [
        score / count
        for score, count in zip(
            robust_open_block_log_scores, score_block_observations
        )
    ]
    selected_over_first_jump = [
        selected - baseline
        for selected, baseline in zip(
            selected_block_scores, first_jump_block_scores
        )
    ]
    selected_over_open = [
        selected - open_score
        for selected, open_score in zip(selected_block_scores, open_block_scores)
    ]
    first_jump_gain_mean, first_jump_gain_se = _mean_and_standard_error(
        selected_over_first_jump
    )
    open_gain_mean, open_gain_se = _mean_and_standard_error(selected_over_open)
    selected_depth = results[0]["depth"]
    selected_at_minimum = selected_depth == min(depths)
    selected_at_maximum = selected_depth == max(depths)
    interior_panel_winner = bool(
        selected_depth is not None
        and min(depths) < int(selected_depth) < max(depths)
    )
    return {
        "protocol": {
            "train_range_half_open": train_range,
            "locked_holdout_range_half_open": holdout_range,
            "validation_role": (
                "within-run model selection; not post-selection replication"
            ),
            "odd_starts_only": True,
            "tree_depths": depths,
            "group_mean_shrinkage": shrinkage,
            "selection_metric": (
                "model-selection-band mean Student-t(5) log score"
            ),
            "secondary_metrics": ("RMSE", "Gaussian log score"),
        },
        "baseline_fit": baseline_fit,
        "first_jump_fit": {
            **first_jump_fit,
            "fixed_offset": "1 + v2(3n+1)",
            "coordinate": "log2(A(n))",
        },
        "train_count": train_count,
        "holdout_count": holdout_count,
        "model_comparison": results,
        "selected_model": results[0]["model"],
        "robust_open_reference": {
            "family": "M_bottom",
            "distribution": "StudentT(df=3, height-only center, doubled scale)",
            "holdout_mean_log_score": robust_open_mean_score,
            "selected_over_open_mean_log_score_gain": (
                selected_mean_score - robust_open_mean_score
            ),
            "calibrated_posterior_probability_available": False,
            "reason_probability_not_reported": (
                "the broad scale is a sensitivity reference and the "
                "deterministic block-score dependence is not calibrated"
            ),
            "individual_starts_treated_as_iid_evidence": False,
        },
        "block_score_audit": {
            "status": "descriptive validation stability, not replication",
            "block_size_integer_starts": score_block_size,
            "block_count": score_block_count,
            "odd_observations_per_block": tuple(score_block_observations),
            "selected_over_first_jump_mean_log_score_gain_by_block": tuple(
                selected_over_first_jump
            ),
            "selected_over_first_jump_gain_mean": first_jump_gain_mean,
            "selected_over_first_jump_between_block_dispersion_of_mean": (
                first_jump_gain_se
            ),
            "blocks_favoring_selected_over_first_jump": sum(
                value > 0.0 for value in selected_over_first_jump
            ),
            "selected_over_open_mean_log_score_gain_by_block": tuple(
                selected_over_open
            ),
            "selected_over_open_gain_mean": open_gain_mean,
            "selected_over_open_between_block_dispersion_of_mean": open_gain_se,
            "blocks_favoring_selected_over_open": sum(
                value > 0.0 for value in selected_over_open
            ),
            "replication_count": 0,
        },
        "selection_boundary_audit": {
            "selected_depth_equals_declared_minimum": selected_at_minimum,
            "selected_depth_equals_declared_maximum": selected_at_maximum,
            "interior_panel_winner": interior_panel_winner,
            "identified_optimum_within_declared_panel": interior_panel_winner,
            "reason": (
                "a boundary winner does not identify an optimal residue depth"
                if selected_at_minimum or selected_at_maximum
                else "the selected depth is interior to the declared panel"
            ),
        },
        "null_adequacy_audit": {
            "controlled_accelerated_odd_jumps": 1,
            "residue_prefix_encodes_multiple_future_parity_decisions": True,
            "adequate_for_novel_relation_claim": False,
            "reason": (
                "first-jump control is too weak against a residue prefix that "
                "encodes several future parity and valuation decisions"
            ),
        },
        "posterior_predictive_diagnostics_available": False,
        "mod8_7_minus_5": {
            "raw_train_steps": raw_train_contrast,
            "raw_locked_holdout_steps": raw_holdout_contrast,
            "after_first_jump_control_train_steps": controlled_train_contrast,
            "after_first_jump_control_locked_holdout_steps": controlled_holdout_contrast,
            "persists_descriptively_after_control": (
                controlled_train_contrast * controlled_holdout_contrast > 0.0
            ),
            "interpretation": (
                "Persistence means the first accelerated jump does not exhaust the "
                "finite-range contrast; it is not an inferential or proof claim."
            ),
        },
    }


def height_band_stability(
    state: _FrontierState,
    first_jump_fit: dict[str, float],
    *,
    minimum_power: int = 14,
    maximum_power: int = 20,
) -> dict[str, object]:
    """Track raw and first-jump-controlled mod-8 structure by dyadic height."""

    if minimum_power < 2 or maximum_power <= minimum_power:
        raise ValueError("height powers must define at least one nontrivial band")
    if 1 << maximum_power > len(state.steps):
        raise ValueError("height bands exceed the exact frontier")
    rows = []
    for power in range(minimum_power, maximum_power):
        start, stop = 1 << power, 1 << (power + 1)
        raw = {residue: [0.0, 0.0] for residue in (1, 3, 5, 7)}
        controlled = {residue: [0.0, 0.0] for residue in (1, 3, 5, 7)}
        for value in range(start | 1, stop, 2):
            row = _odd_feature_row(value, state.steps, 1)
            target = float(row["target"])
            residual = target - _predict_first_jump(row, first_jump_fit)
            residue = value % 8
            raw[residue][0] += target
            raw[residue][1] += 1.0
            controlled[residue][0] += residual
            controlled[residue][1] += 1.0
        raw_means = {
            residue: values[0] / values[1] for residue, values in raw.items()
        }
        controlled_means = {
            residue: values[0] / values[1]
            for residue, values in controlled.items()
        }
        rows.append(
            {
                "range_half_open": (start, stop),
                "odd_count": (stop - start) // 2,
                "raw_mod8_means": raw_means,
                "raw_7_minus_5": raw_means[7] - raw_means[5],
                "controlled_mod8_means": controlled_means,
                "controlled_7_minus_5": controlled_means[7] - controlled_means[5],
                "raw_spread": max(raw_means.values()) - min(raw_means.values()),
                "controlled_spread": (
                    max(controlled_means.values()) - min(controlled_means.values())
                ),
            }
        )
    controlled_contrasts = [float(row["controlled_7_minus_5"]) for row in rows]
    return {
        "bands": rows,
        "controlled_contrast_same_sign_all_bands": all(
            value > 0.0 for value in controlled_contrasts
        ) or all(value < 0.0 for value in controlled_contrasts),
        "controlled_contrast_range": (
            min(controlled_contrasts), max(controlled_contrasts)
        ),
    }


def record_hazard_subblocks(
    state: _FrontierState,
    *,
    stop: int,
    block_size: int = 1 << 14,
) -> dict[str, object]:
    """Describe record incidence and upper stopping-time tails in exact subblocks."""

    if stop < 1 or stop >= len(state.steps):
        raise ValueError("record-hazard stop must lie inside the exact frontier")
    if block_size < 1:
        raise ValueError("record-hazard block size must be positive")
    rows = []
    prior_time_record = -1
    prior_peak_record = -1
    time_record_blocks: list[int] = []
    peak_record_blocks: list[int] = []
    block_index = 0
    for start in range(1, stop + 1, block_size):
        block_index += 1
        end = min(stop, start + block_size - 1)
        values = sorted(int(state.steps[value]) for value in range(start, end + 1))
        maximum_steps = max(values)
        maximum_steps_start = min(
            value
            for value in range(start, end + 1)
            if state.steps[value] == maximum_steps
        )
        maximum_peak = max(state.peaks[start : end + 1])
        maximum_peak_start = min(
            value
            for value in range(start, end + 1)
            if state.peaks[value] == maximum_peak
        )
        new_time = maximum_steps > prior_time_record
        new_peak = maximum_peak > prior_peak_record
        if new_time:
            time_record_blocks.append(block_index)
        if new_peak:
            peak_record_blocks.append(block_index)
        time_excess = max(0, maximum_steps - prior_time_record) if prior_time_record >= 0 else maximum_steps
        peak_log_excess = (
            max(0.0, math.log(maximum_peak / prior_peak_record))
            if prior_peak_record > 0
            else math.log(maximum_peak)
        )
        prior_time_record = max(prior_time_record, maximum_steps)
        prior_peak_record = max(prior_peak_record, maximum_peak)
        count = len(values)
        q99 = values[min(count - 1, math.ceil(0.99 * count) - 1)]
        q999 = values[min(count - 1, math.ceil(0.999 * count) - 1)]
        odd_base = maximum_steps_start
        while odd_base % 2 == 0:
            odd_base //= 2
        rows.append(
            {
                "block_index": block_index,
                "range": (start, end),
                "maximum_total_stopping_time": maximum_steps,
                "maximum_total_stopping_time_start": maximum_steps_start,
                "stopping_time_q99": q99,
                "stopping_time_q999": q999,
                "maximum_peak": maximum_peak,
                "maximum_peak_start": maximum_peak_start,
                "new_stopping_time_record": new_time,
                "new_peak_record": new_peak,
                "stopping_time_record_excess": time_excess,
                "log_peak_record_excess": peak_log_excess,
                "stopping_record_odd_base": odd_base,
                "stopping_record_valuation_prefix": valuation_prefix(odd_base, 10),
            }
        )

    quartile_size = max(1, math.ceil(len(rows) / 4))
    quartiles = []
    for offset in range(0, len(rows), quartile_size):
        group = rows[offset : offset + quartile_size]
        quartiles.append(
            {
                "block_indices": (group[0]["block_index"], group[-1]["block_index"]),
                "stopping_record_count": sum(
                    bool(row["new_stopping_time_record"]) for row in group
                ),
                "peak_record_count": sum(bool(row["new_peak_record"]) for row in group),
            }
        )
    return {
        "block_size": block_size,
        "block_count": len(rows),
        "subblocks": rows,
        "stopping_record_block_indices": tuple(time_record_blocks),
        "peak_record_block_indices": tuple(peak_record_blocks),
        "stopping_record_interblock_waits": tuple(
            later - earlier
            for earlier, later in zip(time_record_blocks, time_record_blocks[1:])
        ),
        "peak_record_interblock_waits": tuple(
            later - earlier
            for earlier, later in zip(peak_record_blocks, peak_record_blocks[1:])
        ),
        "laplace_smoothed_next_block_stopping_record_hazard": (
            len(time_record_blocks) + 1
        ) / (len(rows) + 2),
        "laplace_smoothed_next_block_peak_record_hazard": (
            len(peak_record_blocks) + 1
        ) / (len(rows) + 2),
        "quartile_record_counts": quartiles,
        "warning": (
            "A record or a tail-model miss is a workload event, not a Collatz anomaly."
        ),
    }


def _direct_ordinary_audit(start: int, max_steps: int = 100_000) -> dict[str, object]:
    current = start
    steps = 0
    peak = start
    seen: dict[int, int] = {}
    path: list[int] = []
    while current != 1 and steps < max_steps:
        if current in seen:
            return {
                "status": "verified_cycle",
                "steps": steps,
                "peak": peak,
                "cycle": _canonical_cycle(path[seen[current] :]),
            }
        seen[current] = len(path)
        path.append(current)
        current = _ordinary_next(current)
        steps += 1
        peak = max(peak, current)
    return {
        "status": "reached_one" if current == 1 else "resource_limit",
        "steps": steps,
        "peak": peak,
        "terminal": current,
    }


def _direct_accelerated_audit(start: int, max_odd_steps: int = 100_000) -> dict[str, object]:
    current = start
    initial_halvings = two_adic_valuation(current)
    current >>= initial_halvings
    ordinary_toll = initial_halvings
    odd_steps = 0
    peak = start
    seen: dict[int, int] = {}
    odd_path: list[int] = []
    while current != 1 and odd_steps < max_odd_steps:
        if current in seen:
            return {
                "status": "verified_cycle",
                "ordinary_toll": ordinary_toll,
                "odd_steps": odd_steps,
                "peak": peak,
                "odd_cycle": _canonical_cycle(odd_path[seen[current] :]),
            }
        seen[current] = len(odd_path)
        odd_path.append(current)
        expanded = 3 * current + 1
        peak = max(peak, expanded)
        valuation = two_adic_valuation(expanded)
        ordinary_toll += 1 + valuation
        odd_steps += 1
        current = expanded >> valuation
    return {
        "status": "reached_one" if current == 1 else "resource_limit",
        "ordinary_toll": ordinary_toll,
        "odd_steps": odd_steps,
        "peak": peak,
        "terminal": current,
    }


def exact_anomaly_escalation(
    frontier: dict[str, object], state: _FrontierState
) -> dict[str, object]:
    """Independently audit every record and arithmetic exception."""

    starts = set(int(value) for value in frontier["record_starts"])
    starts.update(int(row["start"]) for row in frontier["exceptions"])
    audits = []
    mismatches = []
    for start in sorted(starts):
        ordinary = _direct_ordinary_audit(start)
        accelerated = _direct_accelerated_audit(start)
        match = (
            ordinary["status"] == accelerated["status"]
            and ordinary["status"] == _STATUS_NAME[state.status[start]]
            and (
                ordinary["status"] != "reached_one"
                or (
                    ordinary["steps"] == accelerated["ordinary_toll"]
                    == state.steps[start]
                    and ordinary["peak"] == accelerated["peak"]
                    == state.peaks[start]
                )
            )
        )
        row = {
            "start": start,
            "match": match,
            "ordinary": ordinary,
            "accelerated": accelerated,
        }
        audits.append(row)
        if not match:
            mismatches.append(row)

    counts = frontier["status_counts"]
    assert isinstance(counts, dict)
    if mismatches:
        gate = "implementation_quarantine"
    elif int(counts["verified_cycle"]) > 0:
        gate = "independently_verify_and_publish_nontrivial_cycle"
    elif int(counts["resource_limit"]) > 0:
        gate = "expand_exact_resources_unresolved"
    else:
        gate = "clean_bounded_computation"
    return {
        "active_gate": gate,
        "record_and_exception_audits": audits,
        "all_independent_audits_match": not mismatches,
        "ladder": (
            {
                "level": 0,
                "trigger": "workload record or model-tail miss",
                "action": "record and independently recompute; no conjecture claim",
            },
            {
                "level": 1,
                "trigger": "ordinary/accelerated or checkpoint disagreement",
                "action": "implementation quarantine",
            },
            {
                "level": 2,
                "trigger": "resource limit after exact recomputation",
                "action": "increase limits geometrically; remain unresolved",
            },
            {
                "level": 3,
                "trigger": "repeated positive state before one",
                "action": "canonicalize and independently verify every cycle transition",
            },
        ),
        "proof_boundary": collatz_proof_warning(
            int(frontier["certified_range"][1])
        ),
    }


def _record_digest(observation: object) -> str:
    return evidence_payload_digest(observation)


def _evidence_ledger_summary(
    frontier: dict[str, object], comparison: dict[str, object]
) -> dict[str, object]:
    """Commit exact, training, and holdout provenance with explicit derivation."""

    protocol = comparison["protocol"]
    assert isinstance(protocol, dict)
    train_range = tuple(protocol["train_range_half_open"])
    holdout_range = tuple(protocol["locked_holdout_range_half_open"])
    exact_observation = {
        "certified_range": frontier["certified_range"],
        "status_counts": frontier["status_counts"],
        "resume_token": frontier["resume_token"],
    }
    training_observation = {
        "range": train_range,
        "count": comparison["train_count"],
        "baseline_fit": comparison["baseline_fit"],
        "first_jump_fit": comparison["first_jump_fit"],
    }
    holdout_observation = {
        "range": holdout_range,
        "count": comparison["holdout_count"],
        "selected_model": comparison["selected_model"],
        "model_comparison": comparison["model_comparison"],
        "mod8_7_minus_5": comparison["mod8_7_minus_5"],
    }
    records = (
        EvidenceRecord(
            "collatz_exact_frontier",
            ("collatz_exact_integer_census",),
            "ascending_descent_certificates",
            None,
            _record_digest(exact_observation),
            "exact_integer_computation",
            "bounded_exact",
            exact_observation,
            {"proof_claim": False},
        ),
        EvidenceRecord(
            "collatz_tree_training",
            (f"odd_starts_{train_range[0]}_{train_range[1]}",),
            "fit_valuation_tree",
            math.log2(train_range[0]),
            _record_digest(training_observation),
            "student_t_workload",
            "statistical_training",
            training_observation,
            {
                "locked": False,
                "derived_from_record_ids": ("collatz_exact_frontier",),
            },
            False,
        ),
        EvidenceRecord(
            "collatz_tree_locked_holdout",
            (f"odd_starts_{holdout_range[0]}_{holdout_range[1]}",),
            "score_valuation_tree",
            math.log2(holdout_range[0]),
            _record_digest(holdout_observation),
            "student_t_workload",
            "locked_evaluation",
            holdout_observation,
            {
                "locked": True,
                "derived_from_record_ids": ("collatz_exact_frontier",),
            },
            False,
        ),
    )
    ledger = EvidenceLedger()
    for record in records:
        ledger = ledger.append(record)
    return {
        "record_ids": ledger.record_ids,
        "source_ids": ledger.source_ids,
        "records": tuple(
            {
                "record_id": record.record_id,
                "source_ids": record.source_ids,
                "scope": record.scope,
                "family": record.family,
                "digest": record.digest,
                "joint": record.joint,
            }
            for record in ledger.records
        ),
        "overlap_protection": True,
        "direct_source_ids_are_disjoint": True,
        "shared_exact_dependency_declared_by_lineage": True,
        "posterior_assimilation_performed": False,
    }


def run_collatz_valuation_discovery(
    *,
    limit: int = DEFAULT_LIMIT,
    checkpoint_size: int = DEFAULT_CHECKPOINT_SIZE,
    train_range: tuple[int, int] = DEFAULT_TRAIN_RANGE,
    holdout_range: tuple[int, int] = DEFAULT_HOLDOUT_RANGE,
    tree_depths: tuple[int, ...] = TREE_DEPTHS,
    shrinkage: float = 32.0,
) -> dict[str, object]:
    """Run the exact frontier and locked relational discovery protocol."""

    started = time.perf_counter()
    if holdout_range[1] > limit + 1:
        raise ValueError("the exact frontier must include the complete locked holdout")
    frontier, state = _build_exact_frontier(limit, checkpoint_size, 10_000)
    comparison = locked_tree_comparison(
        state,
        train_range=train_range,
        holdout_range=holdout_range,
        depths=tree_depths,
        shrinkage=shrinkage,
    )
    first_jump_fit = comparison["first_jump_fit"]
    assert isinstance(first_jump_fit, dict)
    height = height_band_stability(
        state,
        first_jump_fit,
        maximum_power=int(math.log2(limit)),
    )
    hazards = record_hazard_subblocks(state, stop=limit)
    escalation = exact_anomaly_escalation(frontier, state)
    ledger = _evidence_ledger_summary(frontier, comparison)
    return {
        "search": "exact Collatz valuation-tree and coalescence discovery",
        "proof_warning": collatz_proof_warning(limit),
        "model_warning": MODEL_WARNING,
        "frontier": frontier,
        "locked_tree_comparison": comparison,
        "height_band_stability": height,
        "record_hazard": hazards,
        "exact_anomaly_escalation": escalation,
        "evidence_ledger": ledger,
        "relational_evidence_backend": (
            "StudentT robust held-out score plus provenance-protected EvidenceLedger"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


if __name__ == "__main__":
    print(json.dumps(run_collatz_valuation_discovery(), indent=2))
