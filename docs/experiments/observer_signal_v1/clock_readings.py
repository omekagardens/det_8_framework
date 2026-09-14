"""Local clock displays with exact error bounds; no geometry or global time API."""

from dataclasses import dataclass
from fractions import Fraction as F


def rational(value):
    if type(value) is int:
        return F(value)
    if type(value) is F:
        return value
    raise ValueError("use exact integers or Fractions, never float/Boolean")


def log_bounds(argument, terms=48):
    """Rational enclosure from the convergent atanh series, not float logging."""
    argument = rational(argument)
    if argument <= 0 or type(terms) is not int or terms < 1:
        raise ValueError("positive logarithm argument and integer terms>=1 required")
    y = (argument - 1) / (argument + 1)
    power, total = y, F(0)
    for j in range(terms):
        total += 2 * power / (2 * j + 1)
        power *= y * y
    error = 2 * abs(power) / ((2 * terms + 1) * (1 - y * y))
    return total - error, total + error


@dataclass(frozen=True)
class ClockReading:
    """Displayed local seconds ± a supplied/proved absolute display error.

    This contains neither a coordinate time nor synchronization information.
    Distinct events may have identical displayed values.
    """

    value: F
    error: F

    def __post_init__(self):
        object.__setattr__(self, "value", rational(self.value))
        object.__setattr__(self, "error", rational(self.error))
        if self.error < 0:
            raise ValueError("negative clock error")

    def to_dict(self):
        return {
            "value_seconds": str(self.value),
            "error_seconds": str(self.error),
            "kind": "bounded_local_clock_display",
        }

    @classmethod
    def from_dict(cls, data):
        if type(data) is not dict or set(data) != {"value_seconds", "error_seconds", "kind"}:
            raise ValueError("invalid local clock schema")
        if data["kind"] != "bounded_local_clock_display":
            raise ValueError("not a bounded local clock reading")
        return cls(parse_rational(data["value_seconds"]), parse_rational(data["error_seconds"]))


def parse_rational(value):
    if type(value) is not str or len(value) > 4096:
        raise ValueError("exact canonical rational string required")
    result = F(value)
    if str(result) != value:
        raise ValueError("noncanonical rational string")
    return result


def display_log(constant, coefficient, argument, places=9, terms=48):
    """Display a generic exact c+k ln(x), with certified truncation/rounding error.

    Used by the producer only. The numeric operands are not stored in records.
    Decimal-grid rounding is exact rational rounding, including tie-to-even.
    """
    constant, coefficient = rational(constant), rational(coefficient)
    if type(places) is not int or not 0 <= places <= 18:
        raise ValueError("display precision must be an integer in [0,18]")
    lo, hi = log_bounds(argument, terms)
    center = constant + coefficient * (lo + hi) / 2
    radius = abs(coefficient) * (hi - lo) / 2
    scale = 10**places
    shown = F(round(center * scale), scale)
    # Round the error upward too: keep a bounded-size local calibration value,
    # not the large series denominator or its producer-side operands.
    error_grid = 10 ** (places + 3)
    scaled_error = (radius + abs(shown - center)) * error_grid
    error_ticks = -(-scaled_error.numerator // scaled_error.denominator)
    return ClockReading(shown, F(error_ticks, error_grid))


def elapsed_bounds(first, second):
    """Same-clock seconds only; caller establishes observer/clock identity."""
    if type(first) is not ClockReading or type(second) is not ClockReading:
        raise ValueError("bounded local clock readings required")
    delta, error = second.value - first.value, first.error + second.error
    return delta - error, delta + error


def spacing_ratio(emitted_first, emitted_second, received_first, received_second):
    """Finite same-clock gaps; never an instantaneous frequency-redshift law."""
    e = elapsed_bounds(emitted_first, emitted_second)
    r = elapsed_bounds(received_first, received_second)
    if e[0] <= 0 or r[0] <= 0:
        return {
            "status": "unresolved_display_precision_or_order",
            "ratio_interval": None,
            "emission_gap": e,
            "reception_gap": r,
        }
    return {
        "status": "bounded_finite_spacing_not_instantaneous_redshift",
        "ratio_interval": (r[0] / e[1], r[1] / e[0]),
        "emission_gap": e,
        "reception_gap": r,
    }
