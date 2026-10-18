"""Exact compatibility for one declared two-way, four-timestamp exchange.

This standalone module uses supplied records and premises only. Its intervals
are compatibility sets, not confidence intervals or calibration certificates.
The input fingerprint binds declarations; it does not authenticate a source.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json


MAX_INPUT_BITS = 256
MAX_RECORDS = 64
_MAX_TEXT = 128
_SLOTS = ("A1", "B2", "B3", "A4")
_ROLES = ("actual", "proposed", "withheld")
_RECORD_STATUSES = ("reading", "missing", "not_received_by_cutoff")
_COMPATIBLE = "compatible_given_premises"
_INCOMPATIBLE = "incompatible_given_premises"
_INSUFFICIENT = "insufficient_records"
_UNSUPPORTED = "unsupported_clock_or_channel_model"
_REPORT_STATUSES = (_COMPATIBLE, _INCOMPATIBLE, _INSUFFICIENT, _UNSUPPORTED)
_CLOCK_MODEL = "shared_unit_rate_constant_offsets"
_DOMAIN_TAG = b"det-exact-timing/request/v1\x00"


def _text(value: object, name: str) -> None:
    if type(value) is not str or not 1 <= len(value) <= _MAX_TEXT:
        raise ValueError(f"{name} must be nonempty text of at most {_MAX_TEXT} characters")


def _fraction(value: object, name: str, *, input_limit: bool = False) -> None:
    if type(value) is not Fraction:
        raise ValueError(f"{name} must be an exact Fraction")
    if input_limit and (
        value.numerator.bit_length() > MAX_INPUT_BITS
        or value.denominator.bit_length() > MAX_INPUT_BITS
    ):
        raise ValueError(f"{name} exceeds the {MAX_INPUT_BITS}-bit input limit")


def _identity(value: object) -> None:
    if (
        type(value) is not str
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("input_id must be a lowercase SHA-256 hexadecimal string")


@dataclass(frozen=True, slots=True)
class Interval:
    lower: Fraction
    upper: Fraction

    def __post_init__(self) -> None:
        _validate_interval(self)


def _validate_interval(value: object, *, input_limit: bool = False) -> None:
    if type(value) is not Interval:
        raise ValueError("interval must be an exact Interval")
    _fraction(value.lower, "interval.lower", input_limit=input_limit)
    _fraction(value.upper, "interval.upper", input_limit=input_limit)
    if value.lower > value.upper:
        raise ValueError("interval endpoints must be ordered")


@dataclass(frozen=True, slots=True)
class Bounds:
    forward: Interval | None = None
    reverse: Interval | None = None
    asymmetry: Interval | None = None

    def __post_init__(self) -> None:
        _validate_bounds(self)


def _validate_bounds(value: object, *, input_limit: bool = False) -> None:
    if type(value) is not Bounds:
        raise ValueError("bounds must be an exact Bounds")
    for name in ("forward", "reverse", "asymmetry"):
        interval = getattr(value, name)
        if interval is not None:
            _validate_interval(interval, input_limit=input_limit)
            if name != "asymmetry" and interval.lower < 0:
                raise ValueError(f"{name} delay bounds must be nonnegative")


@dataclass(frozen=True, slots=True)
class Record:
    record_id: str
    exchange_id: str
    slot: str
    clock_id: str
    message_id: str
    unit: str
    value: Fraction | None
    role: str = "actual"
    selected: bool = True
    status: str = "reading"
    error: Fraction = Fraction(0)
    disposition_reason: str = ""

    def __post_init__(self) -> None:
        _validate_record(self)


def _validate_record(value: object, *, input_limit: bool = False) -> None:
    if type(value) is not Record:
        raise ValueError("records must contain exact Record objects")
    for name in (
        "record_id", "exchange_id", "slot", "clock_id", "message_id", "unit",
        "role", "status",
    ):
        _text(getattr(value, name), f"record.{name}")
    if value.slot not in _SLOTS:
        raise ValueError("record.slot is not one of A1, B2, B3, A4")
    if value.role not in _ROLES:
        raise ValueError("record.role is not actual, proposed or withheld")
    if type(value.selected) is not bool:
        raise ValueError("record.selected must be a bool")
    if value.status not in _RECORD_STATUSES:
        raise ValueError("record.status is not a supported declaration")
    if type(value.disposition_reason) is not str or len(value.disposition_reason) > _MAX_TEXT:
        raise ValueError("record.disposition_reason must be text of at most 128 characters")
    if (
        value.role != "actual" or not value.selected or value.status != "reading"
    ) and not value.disposition_reason:
        raise ValueError("unused or non-reading records require a disposition_reason")
    _fraction(value.error, "record.error", input_limit=input_limit)
    if value.error < 0:
        raise ValueError("record.error must be nonnegative")
    if value.status == "reading":
        _fraction(value.value, "record.value", input_limit=input_limit)
    elif value.value is not None or value.error != 0:
        raise ValueError("non-reading records require value=None and zero error")
    if value.status == "not_received_by_cutoff" and value.slot not in ("B2", "A4"):
        raise ValueError("cutoff nonreceipt is valid only for receive slots B2 and A4")


@dataclass(frozen=True, slots=True)
class Request:
    exchange_id: str
    clock_a: str
    clock_b: str
    unit: str
    premise_id: str
    clock_model: str
    uncertainty_model: str
    records: tuple[Record, ...]
    bounds: Bounds
    tolerance: Fraction

    def __post_init__(self) -> None:
        _validate_request(self)


def _validate_request(value: object) -> None:
    if type(value) is not Request:
        raise ValueError("request must be an exact Request")
    for name in (
        "exchange_id", "clock_a", "clock_b", "unit", "premise_id",
        "clock_model", "uncertainty_model",
    ):
        _text(getattr(value, name), f"request.{name}")
    if value.clock_a == value.clock_b:
        raise ValueError("request clocks must be distinct")
    if type(value.records) is not tuple or len(value.records) > MAX_RECORDS:
        raise ValueError(f"request.records must be a tuple of at most {MAX_RECORDS} records")
    identifiers = set()
    for record in value.records:
        _validate_record(record, input_limit=True)
        if record.record_id in identifiers:
            raise ValueError("record IDs must be unique across every input row")
        identifiers.add(record.record_id)
    _validate_bounds(value.bounds, input_limit=True)
    _fraction(value.tolerance, "request.tolerance", input_limit=True)
    if value.tolerance < 0:
        raise ValueError("request.tolerance must be nonnegative")


@dataclass(frozen=True, slots=True)
class Report:
    input_id: str
    status: str
    reason: str
    interval: Interval | None
    estimate: Fraction | None
    radius: Fraction | None
    precision_met: bool | None

    def __post_init__(self) -> None:
        _identity(self.input_id)
        _text(self.status, "report.status")
        _text(self.reason, "report.reason")
        if self.status not in _REPORT_STATUSES:
            raise ValueError("report.status is unsupported")
        if self.status != _COMPATIBLE:
            if any(value is not None for value in (
                self.interval, self.estimate, self.radius, self.precision_met,
            )):
                raise ValueError("noncompatible reports cannot contain inference fields")
            return
        _validate_interval(self.interval)
        _fraction(self.estimate, "report.estimate")
        _fraction(self.radius, "report.radius")
        if type(self.precision_met) is not bool:
            raise ValueError("compatible precision_met must be a bool")
        if (
            self.estimate != (self.interval.lower + self.interval.upper) / 2
            or self.radius != (self.interval.upper - self.interval.lower) / 2
        ):
            raise ValueError("report estimate and radius must describe its interval")


@dataclass(frozen=True, slots=True)
class Witness:
    input_id: str
    theta: Fraction
    beta_a: Fraction
    beta_b: Fraction
    times: tuple[Fraction, Fraction, Fraction, Fraction]
    forward_delay: Fraction
    reverse_delay: Fraction
    turnaround: Fraction

    def __post_init__(self) -> None:
        _identity(self.input_id)
        for name in (
            "theta", "beta_a", "beta_b", "forward_delay", "reverse_delay", "turnaround",
        ):
            _fraction(getattr(self, name), f"witness.{name}")
        if type(self.times) is not tuple or len(self.times) != 4:
            raise ValueError("witness.times must contain exactly four Fraction times")
        for value in self.times:
            _fraction(value, "witness time")
        if self.beta_a != 0 or self.beta_b != self.theta:
            raise ValueError("witness must use beta_a=0 and beta_b=theta")
        t1, t2, t3, t4 = self.times
        if (
            self.forward_delay != t2 - t1
            or self.turnaround != t3 - t2
            or self.reverse_delay != t4 - t3
            or min(self.forward_delay, self.reverse_delay, self.turnaround) < 0
        ):
            raise ValueError("witness delays must match its chronological times")


def _ratio(value: Fraction) -> list[str]:
    return [str(value.numerator), str(value.denominator)]


def _interval_data(value: Interval | None) -> dict | None:
    if value is None:
        return None
    return {"lower": _ratio(value.lower), "upper": _ratio(value.upper)}


def _input_id(request: Request) -> str:
    """Encode only an already validated request, including unused rows/order."""
    data = {
        name: getattr(request, name)
        for name in (
            "exchange_id", "clock_a", "clock_b", "unit", "premise_id",
            "clock_model", "uncertainty_model",
        )
    }
    data["records"] = [
        {
            **{name: getattr(record, name) for name in (
                "record_id", "exchange_id", "slot", "clock_id", "message_id", "unit",
                "role", "selected", "status", "disposition_reason",
            )},
            "value": None if record.value is None else _ratio(record.value),
            "error": _ratio(record.error),
        }
        for record in request.records
    ]
    data["bounds"] = {
        name: _interval_data(getattr(request.bounds, name))
        for name in ("forward", "reverse", "asymmetry")
    }
    data["tolerance"] = _ratio(request.tolerance)
    encoded = json.dumps(data, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(_DOMAIN_TAG + encoded.encode("ascii")).hexdigest()


def fingerprint(request: Request) -> str:
    """Bind all supplied declarations; make no authentication claim."""
    _validate_request(request)
    return _input_id(request)


def _effective_rows(request: Request) -> tuple[Record, ...]:
    return tuple(row for row in request.records if row.role == "actual" and row.selected)


def _refusal(input_id: str, status: str, reason: str) -> Report:
    return Report(input_id, status, reason, None, None, None, None)


def infer(request: Request) -> Report:
    """Return the exact conditional offset projection or a typed refusal."""
    _validate_request(request)
    input_id = _input_id(request)
    if request.clock_model != _CLOCK_MODEL:
        return _refusal(input_id, _UNSUPPORTED, "clock_model")
    if request.uncertainty_model != "exact":
        return _refusal(input_id, _UNSUPPORTED, "uncertainty_model")

    effective = _effective_rows(request)
    rows = {row.slot: row for row in effective}
    if len(rows) != len(effective):
        return _refusal(input_id, _UNSUPPORTED, "ambiguous_slots")
    if len(rows) != 4 or any(row.status != "reading" for row in effective):
        return _refusal(input_id, _INSUFFICIENT, "incomplete_exchange")

    if (
        any(row.exchange_id != request.exchange_id for row in effective)
        or any(
            rows[slot].clock_id != (request.clock_a if slot in ("A1", "A4") else request.clock_b)
            for slot in _SLOTS
        )
        or rows["A1"].message_id != rows["B2"].message_id
        or rows["B3"].message_id != rows["A4"].message_id
        or rows["A1"].message_id == rows["B3"].message_id
    ):
        return _refusal(input_id, _UNSUPPORTED, "record_association")
    if any(row.unit != request.unit for row in effective):
        return _refusal(input_id, _UNSUPPORTED, "unit")
    if any(row.error > 0 for row in effective):
        return _refusal(input_id, _UNSUPPORTED, "nonexact_reading")

    a1, b2, b3, a4 = (rows[slot].value for slot in _SLOTS)
    u, v, turnaround = b2 - a1, a4 - b3, b3 - b2
    if turnaround < 0:
        return _refusal(input_id, _INCOMPATIBLE, "negative_turnaround")
    if u + v < 0:
        return _refusal(input_id, _INCOMPATIBLE, "negative_roundtrip")

    lower, upper = -v, u
    if request.bounds.forward is not None:
        interval = request.bounds.forward
        lower, upper = max(lower, u - interval.upper), min(upper, u - interval.lower)
    if request.bounds.reverse is not None:
        interval = request.bounds.reverse
        lower, upper = max(lower, interval.lower - v), min(upper, interval.upper - v)
    if request.bounds.asymmetry is not None:
        interval = request.bounds.asymmetry
        lower = max(lower, (u - v - interval.upper) / 2)
        upper = min(upper, (u - v - interval.lower) / 2)
    if lower > upper:
        return _refusal(input_id, _INCOMPATIBLE, "empty_compatibility")

    interval = Interval(lower, upper)
    estimate, radius = (lower + upper) / 2, (upper - lower) / 2
    return Report(
        input_id, _COMPATIBLE, "exact_projection", interval, estimate, radius,
        radius <= request.tolerance,
    )


def witness(request: Request, theta: Fraction) -> Witness | None:
    """Construct an attaining exchange from actual supplied readings alone."""
    _validate_request(request)
    _fraction(theta, "witness target")
    report = infer(request)
    if report.status != _COMPATIBLE:
        return None
    if theta < report.interval.lower or theta > report.interval.upper:
        return None
    rows = {row.slot: row for row in _effective_rows(request)}
    a1, b2, b3, a4 = (rows[slot].value for slot in _SLOTS)
    times = (a1, b2 - theta, b3 - theta, a4)
    return Witness(
        report.input_id, theta, Fraction(0), theta, times,
        times[1] - times[0], times[3] - times[2], times[2] - times[1],
    )


__all__ = [
    "MAX_INPUT_BITS", "MAX_RECORDS", "Interval", "Bounds", "Record", "Request",
    "Report", "Witness", "fingerprint", "infer", "witness",
]
