"""Shared fail-fast validation helpers for DET8 numerical state.

These helpers deliberately do not clamp invalid scientific inputs.  Callers
must opt in to normalization, and state-transition functions may separately
implement domain-defined saturation after their inputs have been validated.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from numbers import Real

DEFAULT_PROBABILITY_TOLERANCE = 1e-12


def require_real_finite(value: Real, name: str) -> float:
    """Return *value* as a finite float, rejecting booleans and non-reals."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number, not {type(value).__name__}")
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be representable as a finite float") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def require_nonnegative_finite(value: Real, name: str) -> float:
    """Return a finite real value greater than or equal to zero."""
    result = require_real_finite(value, name)
    if result < 0.0:
        raise ValueError(f"{name} must be non-negative")
    return result


def require_positive_finite(value: Real, name: str) -> float:
    """Return a finite real value strictly greater than zero."""
    result = require_real_finite(value, name)
    if result <= 0.0:
        raise ValueError(f"{name} must be positive")
    return result


def normalize_nonnegative_weights(
    weights: Iterable[Real],
    *,
    name: str = "weights",
    normalize: bool,
    require_total_one: bool | None = None,
    tolerance: float = DEFAULT_PROBABILITY_TOLERANCE,
) -> tuple[float, ...]:
    """Validate non-negative finite weights and optionally normalize them.

    ``normalize`` is intentionally mandatory so callers cannot normalize bad
    probability input accidentally.  When ``require_total_one`` is omitted,
    strict unit-total validation is the default for non-normalizing calls and
    is skipped for explicitly normalizing calls.

    Normalization is performed after scaling by the largest weight.  This
    avoids overflowing when otherwise valid finite weights have a sum larger
    than the largest representable float.
    """
    if not isinstance(normalize, bool):
        raise TypeError("normalize must be a bool")
    if require_total_one is not None and not isinstance(require_total_one, bool):
        raise TypeError("require_total_one must be a bool or None")
    tolerance_value = require_nonnegative_finite(tolerance, "tolerance")

    values = tuple(
        require_nonnegative_finite(weight, f"{name}[{index}]")
        for index, weight in enumerate(weights)
    )
    if not values:
        raise ValueError(f"{name} must be nonempty")

    largest = max(values)
    if largest == 0.0:
        raise ValueError(f"{name} must have positive total weight")

    check_total = (not normalize) if require_total_one is None else require_total_one
    if check_total:
        try:
            total = math.fsum(values)
        except OverflowError as exc:
            raise ValueError(f"{name} must sum to 1 within tolerance") from exc
        if not math.isfinite(total) or not math.isclose(
            total,
            1.0,
            rel_tol=tolerance_value,
            abs_tol=tolerance_value,
        ):
            raise ValueError(f"{name} must sum to 1 within tolerance; got {total!r}")

    if not normalize:
        return values

    scaled = tuple(weight / largest for weight in values)
    scaled_total = math.fsum(scaled)
    normalized = [weight / scaled_total for weight in scaled]

    # Correct the small rounding residual on the largest component so callers
    # receive a measure whose floating-point sum is as close to one as possible.
    largest_index = max(range(len(normalized)), key=normalized.__getitem__)
    normalized[largest_index] += 1.0 - math.fsum(normalized)
    return tuple(normalized)
