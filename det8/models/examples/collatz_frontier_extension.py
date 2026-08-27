"""Checkpointed Collatz frontier and multi-modulus residue extension."""

from __future__ import annotations

import hashlib
import json
import math

from det8.models.examples.collatz_search import (
    COLLATZ_PROOF_WARNING,
    bounded_collatz_verification,
    collatz_trajectory,
)


COLLATZ_FRONTIER_WARNING = (
    "The checkpoint manifest certifies reproducible bounded integer trajectories, "
    "not convergence beyond the reported frontier. Residue profiles are finite-range "
    "descriptions and are not counterexamples or conjecture probabilities."
)


def _checkpoint_block(
    start: int,
    stop: int,
    *,
    max_steps: int,
    prior_chain_digest: str,
) -> dict[str, object]:
    block_hash = hashlib.sha256()
    counts = {"reached_one": 0, "resource_limit": 0, "verified_cycle": 0}
    longest_steps = -1
    longest_start = start
    largest_peak = -1
    largest_peak_start = start
    step_sum = 0
    step_square_sum = 0
    completed_count = 0

    for value in range(start, stop + 1):
        trajectory = collatz_trajectory(value, max_steps=max_steps)
        counts[trajectory.status] += 1
        block_hash.update(
            (
                f"{trajectory.start}:{trajectory.status}:{trajectory.steps}:"
                f"{trajectory.peak}:{trajectory.terminal}:"
                f"{trajectory.repeated_value};"
            ).encode("ascii")
        )
        if trajectory.status != "reached_one":
            continue
        completed_count += 1
        step_sum += trajectory.steps
        step_square_sum += trajectory.steps**2
        if trajectory.steps > longest_steps:
            longest_steps = trajectory.steps
            longest_start = trajectory.start
        if trajectory.peak > largest_peak:
            largest_peak = trajectory.peak
            largest_peak_start = trajectory.start

    block_digest = block_hash.hexdigest()
    chain_digest = hashlib.sha256(
        f"{prior_chain_digest}:{start}:{stop}:{block_digest}".encode("ascii")
    ).hexdigest()
    if completed_count:
        mean_steps = step_sum / completed_count
        variance = step_square_sum / completed_count - mean_steps**2
        standard_deviation = math.sqrt(max(variance, 0.0))
    else:
        mean_steps = math.nan
        standard_deviation = math.nan
    return {
        "start": start,
        "stop": stop,
        "tested_count": stop - start + 1,
        "status_counts": counts,
        "all_reached_one": counts["reached_one"] == stop - start + 1,
        "mean_total_stopping_time": mean_steps,
        "stopping_time_standard_deviation": standard_deviation,
        "maximum_total_stopping_time": (
            longest_steps if completed_count else None
        ),
        "maximum_total_stopping_time_start": (
            longest_start if completed_count else None
        ),
        "maximum_peak": largest_peak if completed_count else None,
        "maximum_peak_start": largest_peak_start if completed_count else None,
        "block_sha256": block_digest,
        "chain_sha256": chain_digest,
    }


def checkpointed_collatz_frontier(
    *,
    start: int = 65_537,
    stop: int = 262_144,
    checkpoint_size: int = 65_536,
    max_steps: int = 10_000,
) -> dict[str, object]:
    """Extend an already verified prefix using deterministic hash-chained blocks."""

    if start < 2 or stop < start:
        raise ValueError("frontier must satisfy 2 <= start <= stop")
    if checkpoint_size < 1:
        raise ValueError("checkpoint size must be positive")
    if max_steps < 1:
        raise ValueError("maximum step count must be positive")

    baseline = bounded_collatz_verification(start - 1)
    cumulative_longest_steps = int(baseline["maximum_total_stopping_time"])
    cumulative_longest_start = int(
        baseline["maximum_total_stopping_time_start"]
    )
    cumulative_largest_peak = int(baseline["maximum_peak"])
    cumulative_largest_peak_start = int(baseline["maximum_peak_start"])
    cumulative_counts = dict(baseline["status_counts"])
    chain_digest = hashlib.sha256(
        f"collatz-frontier-v1:{start}:{max_steps}".encode("ascii")
    ).hexdigest()
    checkpoints = []

    block_start = start
    while block_start <= stop:
        block_stop = min(stop, block_start + checkpoint_size - 1)
        checkpoint = _checkpoint_block(
            block_start,
            block_stop,
            max_steps=max_steps,
            prior_chain_digest=chain_digest,
        )
        chain_digest = str(checkpoint["chain_sha256"])
        for status, count in checkpoint["status_counts"].items():
            cumulative_counts[status] += int(count)

        previous_longest = cumulative_longest_steps
        previous_peak = cumulative_largest_peak
        if int(checkpoint["maximum_total_stopping_time"]) > cumulative_longest_steps:
            cumulative_longest_steps = int(
                checkpoint["maximum_total_stopping_time"]
            )
            cumulative_longest_start = int(
                checkpoint["maximum_total_stopping_time_start"]
            )
        if int(checkpoint["maximum_peak"]) > cumulative_largest_peak:
            cumulative_largest_peak = int(checkpoint["maximum_peak"])
            cumulative_largest_peak_start = int(
                checkpoint["maximum_peak_start"]
            )
        checkpoint["new_stopping_time_record"] = (
            cumulative_longest_steps > previous_longest
        )
        checkpoint["new_peak_record"] = cumulative_largest_peak > previous_peak
        checkpoint["cumulative_records"] = {
            "maximum_total_stopping_time": cumulative_longest_steps,
            "maximum_total_stopping_time_start": cumulative_longest_start,
            "maximum_peak": cumulative_largest_peak,
            "maximum_peak_start": cumulative_largest_peak_start,
        }
        checkpoints.append(checkpoint)
        block_start = block_stop + 1

    return {
        "verified_prefix_before_extension": (1, start - 1),
        "extended_range": (start, stop),
        "checkpoint_size": checkpoint_size,
        "max_steps": max_steps,
        "checkpoints": checkpoints,
        "resume_token": chain_digest,
        "cumulative_status_counts": cumulative_counts,
        "all_reached_one_through_frontier": (
            cumulative_counts["reached_one"] == stop
        ),
        "verified_through": stop,
        "final_records": {
            "maximum_total_stopping_time": cumulative_longest_steps,
            "maximum_total_stopping_time_start": cumulative_longest_start,
            "maximum_peak": cumulative_largest_peak,
            "maximum_peak_start": cumulative_largest_peak_start,
        },
    }


def collatz_residue_profile(
    start: int,
    stop: int,
    modulus: int,
    *,
    max_steps: int = 10_000,
) -> dict[str, object]:
    """Compare odd residue classes without mixing in the trivial even step."""

    if start < 1 or stop < start:
        raise ValueError("residue profile must satisfy 1 <= start <= stop")
    if modulus < 4 or modulus % 2:
        raise ValueError("residue modulus must be an even integer of at least four")
    rows = []
    for residue in range(1, modulus, 2):
        count = 0
        completed = 0
        step_sum = 0
        step_square_sum = 0
        maximum_steps = -1
        maximum_start = None
        resource_limited = 0
        verified_cycles = 0
        for value in range(start, stop + 1):
            if value % modulus != residue:
                continue
            count += 1
            trajectory = collatz_trajectory(value, max_steps=max_steps)
            if trajectory.status == "resource_limit":
                resource_limited += 1
                continue
            if trajectory.status == "verified_cycle":
                verified_cycles += 1
                continue
            completed += 1
            step_sum += trajectory.steps
            step_square_sum += trajectory.steps**2
            if trajectory.steps > maximum_steps:
                maximum_steps = trajectory.steps
                maximum_start = trajectory.start
        if not completed:
            mean_steps = math.nan
            standard_deviation = math.nan
        else:
            mean_steps = step_sum / completed
            variance = step_square_sum / completed - mean_steps**2
            standard_deviation = math.sqrt(max(variance, 0.0))
        rows.append(
            {
                "residue": residue,
                "tested_count": count,
                "completed_count": completed,
                "resource_limit_count": resource_limited,
                "verified_cycle_count": verified_cycles,
                "mean_total_stopping_time": mean_steps,
                "stopping_time_standard_deviation": standard_deviation,
                "maximum_total_stopping_time": (
                    maximum_steps if completed else None
                ),
                "maximum_total_stopping_time_start": maximum_start,
            }
        )

    minimum_row = min(rows, key=lambda row: row["mean_total_stopping_time"])
    maximum_row = max(rows, key=lambda row: row["mean_total_stopping_time"])
    return {
        "range": (start, stop),
        "modulus": modulus,
        "odd_residues_only": True,
        "rows": rows,
        "minimum_mean_residue": minimum_row["residue"],
        "maximum_mean_residue": maximum_row["residue"],
        "mean_spread": (
            maximum_row["mean_total_stopping_time"]
            - minimum_row["mean_total_stopping_time"]
        ),
        "all_completed": all(
            row["completed_count"] == row["tested_count"] for row in rows
        ),
    }


def run_collatz_frontier_extension(
    *,
    start: int = 65_537,
    stop: int = 262_144,
    checkpoint_size: int = 65_536,
    moduli: tuple[int, ...] = (8, 16, 32),
) -> dict[str, object]:
    frontier = checkpointed_collatz_frontier(
        start=start,
        stop=stop,
        checkpoint_size=checkpoint_size,
    )
    aggregate_profiles = {
        str(modulus): collatz_residue_profile(start, stop, modulus)
        for modulus in moduli
    }
    height_profiles = [
        collatz_residue_profile(
            int(checkpoint["start"]),
            int(checkpoint["stop"]),
            8,
        )
        for checkpoint in frontier["checkpoints"]
    ]
    mod8_rows = {
        int(row["residue"]): row
        for row in aggregate_profiles["8"]["rows"]
    }
    return {
        "search": "checkpointed Collatz frontier and multi-modulus residue profiles",
        "warning": COLLATZ_FRONTIER_WARNING,
        "proof_warning": COLLATZ_PROOF_WARNING,
        "frontier": frontier,
        "aggregate_residue_profiles": aggregate_profiles,
        "mod8_height_profiles": height_profiles,
        "mod8_7_minus_5_mean_contrast": (
            mod8_rows[7]["mean_total_stopping_time"]
            - mod8_rows[5]["mean_total_stopping_time"]
        ),
        "resource_limit_followup_required": (
            frontier["cumulative_status_counts"]["resource_limit"] > 0
        ),
        "verified_cycle_followup_required": (
            frontier["cumulative_status_counts"]["verified_cycle"] > 0
        ),
    }


if __name__ == "__main__":
    print(json.dumps(run_collatz_frontier_extension(), indent=2))
