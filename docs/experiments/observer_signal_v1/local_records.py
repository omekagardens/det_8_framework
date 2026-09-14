"""Retained local records, without geometry parameters, forecasts or global clocks."""

import json
from dataclasses import dataclass

from clock_readings import ClockReading, parse_rational, rational


class RecordError(ValueError):
    """Malformed local record/history, retained caller inputs are not repaired."""


def text_id(value):
    if (
        type(value) is not str
        or not value
        or len(value) > 96
        or any(not (c.isascii() and (c.isalnum() or c in "_.:-")) for c in value)
    ):
        raise RecordError("canonical nominal identity required")
    return value


def keys(data, names):
    if type(data) is not dict or set(data) != set(names):
        raise RecordError("unexpected record schema fields")


@dataclass(frozen=True)
class Payload:
    emission_id: str
    signal_id: str
    emitter_id: str
    target_id: str
    crest_id: str
    reference_frequency: object
    emitter_timestamp: ClockReading
    message: str

    def __post_init__(self):
        for name in ("emission_id", "signal_id", "emitter_id", "target_id", "crest_id"):
            text_id(getattr(self, name))
        if self.emitter_id == self.target_id:
            raise RecordError("two distinct observer identities required, even if colocated")
        frequency = rational(self.reference_frequency)
        if frequency <= 0:
            raise RecordError("positive calibrated transmitted reference frequency required")
        object.__setattr__(self, "reference_frequency", frequency)
        if type(self.emitter_timestamp) is not ClockReading:
            raise RecordError("transmitted local timestamp must retain its display error")
        if type(self.message) is not str or len(self.message) > 256:
            raise RecordError("bounded payload text required")

    def to_dict(self):
        return {
            **{n: getattr(self, n) for n in self.__dataclass_fields__},
            "reference_frequency": str(self.reference_frequency),
            "emitter_timestamp": self.emitter_timestamp.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        keys(data, cls.__dataclass_fields__)
        values = dict(data)
        values["reference_frequency"] = parse_rational(values["reference_frequency"])
        values["emitter_timestamp"] = ClockReading.from_dict(values["emitter_timestamp"])
        return cls(**values)


@dataclass(frozen=True)
class LocalRecord:
    event_id: str
    observer_id: str
    kind: str
    timestamp: ClockReading
    precursor_id: str
    payload: Payload | None
    measured_frequency: object
    calibration_id: str
    provenance: str

    def __post_init__(self):
        for name in ("event_id", "observer_id", "precursor_id", "calibration_id", "provenance"):
            text_id(getattr(self, name))
        if self.event_id in (self.precursor_id, "start:" + self.observer_id):
            raise RecordError("event cannot reuse its local anchor or self-link")
        if type(self.timestamp) is not ClockReading:
            raise RecordError("bounded local clock timestamp required")
        if self.kind == "window_closed":
            if self.payload is not None or self.measured_frequency is not None:
                raise RecordError("window closure is not a signal receipt")
        elif self.kind in ("emission", "reception"):
            if type(self.payload) is not Payload:
                raise RecordError("emitted/received reference payload required")
            if self.kind == "emission":
                if (
                    self.observer_id != self.payload.emitter_id
                    or self.event_id != self.payload.emission_id
                    or self.timestamp != self.payload.emitter_timestamp
                    or self.measured_frequency is not None
                ):
                    raise RecordError("emission must preserve its actual local identity/time")
            else:
                if (
                    self.observer_id != self.payload.target_id
                    or self.event_id == self.payload.emission_id
                ):
                    raise RecordError("reception is a distinct target-local event")
                frequency = rational(self.measured_frequency)
                if frequency <= 0:
                    raise RecordError("positive locally measured frequency required")
                object.__setattr__(self, "measured_frequency", frequency)
        else:
            raise RecordError("only actual local emissions, receipts and window closures allowed")

    def to_dict(self):
        return {
            "schema_version": 1,
            **{n: getattr(self, n) for n in self.__dataclass_fields__},
            "timestamp": self.timestamp.to_dict(),
            "payload": None if self.payload is None else self.payload.to_dict(),
            "measured_frequency": None
            if self.measured_frequency is None
            else str(self.measured_frequency),
        }

    @classmethod
    def from_dict(cls, data):
        keys(data, ("schema_version", *cls.__dataclass_fields__))
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise RecordError("unsupported schema version")
        values = dict(data)
        del values["schema_version"]
        values["timestamp"] = ClockReading.from_dict(values["timestamp"])
        if values["payload"] is not None:
            values["payload"] = Payload.from_dict(values["payload"])
        if values["measured_frequency"] is not None:
            values["measured_frequency"] = parse_rational(values["measured_frequency"])
        return cls(**values)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def decode_record(line):
    def unique_pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise RecordError("duplicate JSON key")
            result[key] = value
        return result

    try:
        value = json.loads(
            line,
            object_pairs_hook=unique_pairs,
            parse_constant=lambda x: (_ for _ in ()).throw(RecordError("nonfinite JSON")),
        )
        return LocalRecord.from_dict(value)
    except (TypeError, ValueError, ZeroDivisionError) as error:
        raise RecordError("invalid local record") from error


def validate_history(observer_id, records):
    text_id(observer_id)
    if type(records) is not tuple:
        raise RecordError("immutable local history tuple required")
    previous, seen = "start:" + observer_id, {"start:" + observer_id}
    last, running_lower = None, None
    for row in records:
        if type(row) is not LocalRecord or row.observer_id != observer_id:
            raise RecordError("foreign/nonlocal record")
        if row.precursor_id != previous or row.event_id in seen:
            raise RecordError("broken/duplicate local history")
        if last is not None:
            if last.kind == "window_closed":
                raise RecordError("no event after a closed observation window")
            if (row.calibration_id, row.provenance) != (last.calibration_id, last.provenance):
                raise RecordError("local clock/calibration/provenance changed")
        lo = row.timestamp.value - row.timestamp.error
        hi = row.timestamp.value + row.timestamp.error
        running_lower = lo if running_lower is None else max(running_lower, lo)
        if running_lower > hi:
            raise RecordError("clock intervals admit no chronological local history")
        seen.add(row.event_id)
        previous, last = row.event_id, row
    return records
