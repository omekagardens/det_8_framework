"""Independent Decimal direct-form-I reference for the RI-42 filter recipe.

This module uses only the standard library. It does not design coefficients or
call a production filter, NumPy, SciPy, or their initialization helpers. Each
supplied SOS stage receives its own odd extension, ordered forward cascade,
ordered backward cascade, and removal of that stage's padding. Decimal values
remain Decimal between stages. This implements the prescribed finite-array
operation; it supplies neither a filter-design proof nor a physical error bound.
"""

from collections.abc import Sequence
from decimal import (
    Context,
    Decimal,
    DecimalException,
    DivisionByZero,
    InvalidOperation,
    Overflow,
    ROUND_HALF_EVEN,
    localcontext,
)
from math import isfinite


def _sequence(value: object, name: str) -> tuple:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ValueError(f"{name} must be a sequence")
    return tuple(value)


def _exact_float(value: object, name: str) -> Decimal:
    if type(value) is not float or not isfinite(value):
        raise ValueError(f"{name} must be a finite Python float")
    # from_float preserves the complete binary64 value, without context rounding.
    return Decimal.from_float(float(value))


def _cascade(
    values: list[Decimal],
    sections: list[tuple[Decimal, ...]],
    dc_gains: list[Decimal],
) -> list[Decimal]:
    """One ordered DFI pass, with the cascade's constant input prehistory."""
    current = values
    prehistory = values[0]
    for section, dc_gain in zip(sections, dc_gains):
        b0, b1, b2, a0, a1, a2 = section
        x_previous = x_older = prehistory
        output_prehistory = dc_gain * prehistory
        y_previous = y_older = output_prehistory
        output = []
        for x in current:
            y = (
                b0 * x + b1 * x_previous + b2 * x_older
                - a1 * y_previous - a2 * y_older
            ) / a0
            if not y.is_finite():
                raise RuntimeError("nonfinite Decimal recurrence output")
            output.append(y)
            x_older, x_previous = x_previous, x
            y_older, y_previous = y_previous, y
        current = output
        prehistory = output_prehistory
    return current


def reference_filter(
    values: Sequence[float],
    sos_stages: Sequence[Sequence[Sequence[float]]],
    padlens: Sequence[int],
) -> list[Decimal]:
    """Filter finite Python binary64 floats using independently implemented DFI.

    Each nonempty SOS stage contains six-column rows [b0,b1,b2,a0,a1,a2],
    with a0 exactly 1 and a nonzero DC denominator. Coefficients and samples
    must be Python floats, not Decimal or other numeric objects; array callers
    should supply ordinary nested lists. There must be one nonnegative Python
    integer padding length per stage, strictly less than len(values)-1.

    Inputs are copied and never mutated. Exact float-to-Decimal conversion is
    followed by arithmetic at precision 80 with ROUND_HALF_EVEN in a fresh
    local context. At each pass, section j has constant input prehistory equal
    to the pass's first sample times all preceding sections' DC gains. The
    backward pass starts at the last complete forward output, with the same
    section order. Returned values retain Decimal precision; callers must not
    round them to binary64 before computing qualification discrepancies.

    Invalid inputs raise ValueError. Decimal arithmetic failures raise
    RuntimeError. Validation remains active under Python -O. This generic
    reference does not certify coefficient identity, pole stability, the
    number of stages, or any qualification threshold; the runner owns those
    recipe-specific checks.
    """
    source = _sequence(values, "values")
    stages = _sequence(sos_stages, "sos_stages")
    padding = _sequence(padlens, "padlens")
    if len(source) < 2:
        raise ValueError("values must contain at least two samples")
    if not stages or len(stages) != len(padding):
        raise ValueError("supply nonempty stages and one pad length per stage")
    for index, padlen in enumerate(padding):
        if type(padlen) is not int or not 0 <= padlen < len(source) - 1:
            raise ValueError(f"padlens[{index}] must be an integer in [0, L-1)")

    # All context settings are explicit, so a caller's Decimal context cannot
    # change precision, rounding, exponent range, or arithmetic traps.
    context = Context(
        prec=80,
        rounding=ROUND_HALF_EVEN,
        Emin=-999999,
        Emax=999999,
        capitals=1,
        clamp=0,
        flags=[],
        traps=[InvalidOperation, DivisionByZero, Overflow],
    )
    try:
        with localcontext(context):
            current = [
                _exact_float(value, f"values[{index}]")
                for index, value in enumerate(source)
            ]
            prepared = []
            for stage_index, stage in enumerate(stages):
                rows = _sequence(stage, f"sos_stages[{stage_index}]")
                if not rows:
                    raise ValueError("every SOS stage must contain a section")
                sections = []
                dc_gains = []
                for row_index, row in enumerate(rows):
                    name = f"sos_stages[{stage_index}][{row_index}]"
                    raw = _sequence(row, name)
                    if len(raw) != 6:
                        raise ValueError(f"{name} must have six coefficients")
                    section = tuple(
                        _exact_float(value, f"{name}[{column}]")
                        for column, value in enumerate(raw)
                    )
                    b0, b1, b2, a0, a1, a2 = section
                    if a0 != Decimal(1):
                        raise ValueError(f"{name} must have a0 exactly 1")
                    denominator = a0 + a1 + a2
                    if denominator == 0:
                        raise ValueError(f"{name} has a zero DC denominator")
                    dc_gain = (b0 + b1 + b2) / denominator
                    if not dc_gain.is_finite():
                        raise RuntimeError("nonfinite Decimal DC gain")
                    sections.append(section)
                    dc_gains.append(dc_gain)
                prepared.append((sections, dc_gains))

            for (sections, dc_gains), padlen in zip(prepared, padding):
                length = len(current)
                left = [
                    2 * current[0] - current[index]
                    for index in range(padlen, 0, -1)
                ]
                right = [
                    2 * current[-1] - current[index]
                    for index in range(length - 2, length - padlen - 2, -1)
                ]
                extended = left + current + right
                forward = _cascade(extended, sections, dc_gains)
                backward = _cascade(list(reversed(forward)), sections, dc_gains)
                restored = list(reversed(backward))
                current = restored[padlen:len(restored) - padlen]
            return current
    except DecimalException as exc:
        raise RuntimeError("Decimal reference arithmetic failed") from exc
