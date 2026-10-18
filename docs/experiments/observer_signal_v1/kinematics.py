"""Exact supplied exponential-FLRW radial kinematics on a noncompact line.

This is an adopted metric and null-propagation model, not a DET derivation,
an actualization rule, or a gravitational field equation. ``ell`` is the
nonnegative absolute comoving separation; direction belongs to the schedule.
For H != 0 the exact time coordinate is q = exp[-H(t - t_star)] > 0.
For H == 0 it is an ordinary rational coordinate time. Symbolic logarithms,
geometry parameters and q values are model/audit data, not observer records.

All domain, ordering, horizon and cutoff decisions use exact rational
arithmetic. There is no floating-point logarithm or boundary tolerance.
"""

from dataclasses import dataclass, field
from fractions import Fraction

F = Fraction
ZERO = F(0)
ONE = F(1)
FINITE = "finite"
ASYMPTOTIC = "asymptotic_future_only"
BEYOND_HORIZON = "beyond_future_horizon"


def exact(value: int | F, name: str = "value") -> F:
    """Accept only built-in integers or Fractions, never bools or floats."""
    if type(value) not in (int, F):
        raise TypeError(f"{name} must be an exact int or Fraction")
    return F(value)


@dataclass(frozen=True)
class QTime:
    """Positive q coordinate, meaningful only in a nonstatic Geometry."""

    q: F

    def __post_init__(self) -> None:
        q = exact(self.q, "q")
        if q <= 0:
            raise ValueError("q must be positive for a finite time")
        object.__setattr__(self, "q", q)

    def to_dict(self) -> dict[str, str]:
        return {"kind": "exponential_q", "q": str(self.q)}


@dataclass(frozen=True)
class StaticTime:
    """Rational coordinate time, meaningful only in a static Geometry."""

    t: F

    def __post_init__(self) -> None:
        object.__setattr__(self, "t", exact(self.t, "t"))

    def to_dict(self) -> dict[str, str]:
        return {"kind": "static_t", "t": str(self.t)}


@dataclass(frozen=True)
class LogExpression:
    """Audit expression constant + coefficient * ln(argument).

    Canonicalization handles log(1), a zero coefficient and reciprocal
    arguments below one. It is not a general logarithmic identity solver.
    No ordering or horizon decision is delegated to this expression.
    """

    constant: F = ZERO
    coefficient: F = ZERO
    argument: F = ONE

    def __post_init__(self) -> None:
        constant = exact(self.constant, "constant")
        coefficient = exact(self.coefficient, "coefficient")
        argument = exact(self.argument, "argument")
        if argument <= 0:
            raise ValueError("a logarithm argument must be positive")
        if coefficient == 0 or argument == 1:
            coefficient, argument = ZERO, ONE
        elif argument < 1:
            coefficient, argument = -coefficient, 1 / argument
        object.__setattr__(self, "constant", constant)
        object.__setattr__(self, "coefficient", coefficient)
        object.__setattr__(self, "argument", argument)

    def to_dict(self) -> dict[str, str]:
        return {
            "constant": str(self.constant),
            "coefficient": str(self.coefficient),
            "argument": str(self.argument),
        }


@dataclass(frozen=True)
class Geometry:
    """Supplied ds^2=-c^2 dt^2+a(t)^2 dchi^2 with exponential a(t)."""

    H: F = ZERO
    a_star: F = ONE
    c: F = ONE
    t_star: F = ZERO

    def __post_init__(self) -> None:
        for name in ("H", "a_star", "c", "t_star"):
            object.__setattr__(self, name, exact(getattr(self, name), name))
        if self.a_star <= 0 or self.c <= 0:
            raise ValueError("a_star and c must be positive")

    def _moment(self, moment: QTime | StaticTime) -> None:
        expected = StaticTime if self.H == 0 else QTime
        if type(moment) is not expected:
            raise TypeError(f"this geometry requires {expected.__name__}")

    def time(self, moment: QTime | StaticTime) -> LogExpression:
        self._moment(moment)
        if self.H == 0:
            return LogExpression(moment.t)
        return LogExpression(self.t_star, -1 / self.H, moment.q)

    def scale_factor(self, moment: QTime | StaticTime) -> F:
        self._moment(moment)
        return self.a_star if self.H == 0 else self.a_star / moment.q

    def compare_times(self, left: QTime | StaticTime, right: QTime | StaticTime) -> int:
        """Return -1/0/+1 for physical coordinate-time order, exactly."""
        self._moment(left)
        self._moment(right)
        if self.H == 0:
            difference = left.t - right.t
        else:
            difference = (right.q - left.q) if self.H > 0 else (left.q - right.q)
        return (difference > 0) - (difference < 0)

    def elapsed(self, first: QTime | StaticTime, second: QTime | StaticTime) -> LogExpression:
        """Signed second-minus-first interval, without subtracting log objects."""
        self._moment(first)
        self._moment(second)
        if self.H == 0:
            return LogExpression(second.t - first.t)
        return LogExpression(ZERO, -1 / self.H, second.q / first.q)

    def to_dict(self) -> dict[str, str]:
        return {
            "model": "supplied_exponential_flrw_radial_line_v1",
            "H": str(self.H),
            "a_star": str(self.a_star),
            "c": str(self.c),
            "t_star": str(self.t_star),
        }


@dataclass(frozen=True)
class Arrival:
    """Forward-bound arrival calculation; no forged or postselected output.

    Frequency ratio and redshift exist only at a finite reception. The raw
    reception q is retained for horizon audit, including zero or negative
    values, but those values are never constructed as finite QTime objects.
    Delay bounds are exact rational enclosures, not a measured clock error.
    """

    geometry: Geometry
    emission: QTime | StaticTime
    ell: F
    status: str = field(init=False)
    reception: QTime | StaticTime | None = field(init=False)
    delay: LogExpression | None = field(init=False)
    frequency_ratio: F | None = field(init=False)
    redshift: F | None = field(init=False)
    raw_reception_q: F | None = field(init=False)
    transfer_derivative: F | None = field(init=False)
    delay_bounds: tuple[F, F] | None = field(init=False)

    def __post_init__(self) -> None:
        if type(self.geometry) is not Geometry:
            raise TypeError("geometry must be a Geometry")
        g = self.geometry
        g._moment(self.emission)
        ell = exact(self.ell, "ell")
        if ell < 0:
            raise ValueError("ell is a nonnegative absolute comoving separation")
        object.__setattr__(self, "ell", ell)
        raw_q = None
        if g.H == 0:
            dt = g.a_star * ell / g.c
            reception = self.emission if ell == 0 else StaticTime(self.emission.t + dt)
            ratio = ONE
        else:
            raw_q = self.emission.q - g.H * g.a_star * ell / g.c
            if raw_q <= 0:
                status = ASYMPTOTIC if raw_q == 0 else BEYOND_HORIZON
                object.__setattr__(self, "status", status)
                object.__setattr__(self, "raw_reception_q", raw_q)
                for name in (
                    "reception",
                    "delay",
                    "frequency_ratio",
                    "redshift",
                    "transfer_derivative",
                    "delay_bounds",
                ):
                    object.__setattr__(self, name, None)
                return
            reception = self.emission if ell == 0 else QTime(raw_q)
            ratio = raw_q / self.emission.q
        tau = g.scale_factor(self.emission) * ell / g.c
        bounds = (min(tau, tau / ratio), max(tau, tau / ratio))
        object.__setattr__(self, "status", FINITE)
        object.__setattr__(self, "reception", reception)
        object.__setattr__(self, "delay", g.elapsed(self.emission, reception))
        object.__setattr__(self, "frequency_ratio", ratio)
        object.__setattr__(self, "redshift", 1 / ratio - 1)
        object.__setattr__(self, "raw_reception_q", raw_q)
        object.__setattr__(self, "transfer_derivative", 1 / ratio)
        object.__setattr__(self, "delay_bounds", bounds)

    def to_dict(self) -> dict[str, object]:
        def rational_or_none(value: F | None) -> str | None:
            return None if value is None else str(value)

        return {
            "geometry": self.geometry.to_dict(),
            "emission": self.emission.to_dict(),
            "ell": str(self.ell),
            "status": self.status,
            "reception": None if self.reception is None else self.reception.to_dict(),
            "delay": None if self.delay is None else self.delay.to_dict(),
            "frequency_ratio": rational_or_none(self.frequency_ratio),
            "redshift": rational_or_none(self.redshift),
            "raw_reception_q": rational_or_none(self.raw_reception_q),
            "transfer_derivative": rational_or_none(self.transfer_derivative),
            "delay_bounds": (
                None if self.delay_bounds is None else [str(value) for value in self.delay_bounds]
            ),
        }


def arrive(geometry: Geometry, emission: QTime | StaticTime, ell: int | F) -> Arrival:
    return Arrival(geometry, emission, ell)


def received_by(arrival: Arrival, cutoff: QTime | StaticTime) -> bool:
    """Exact finite receipt cutoff; an emission after cutoff is invalid.

    Nonfinite receptions produce False, never a fabricated missing reception
    timestamp. This model decision does not itself create an observer record.
    """
    if type(arrival) is not Arrival:
        raise TypeError("arrival must be an Arrival")
    g = arrival.geometry
    if g.compare_times(cutoff, arrival.emission) < 0:
        raise ValueError("the cutoff must not precede the scheduled emission")
    return arrival.status == FINITE and g.compare_times(arrival.reception, cutoff) <= 0
