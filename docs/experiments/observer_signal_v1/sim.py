"""Deterministic supplied-geometry producer. Global model/audit is not observation."""

from dataclasses import dataclass
from functools import cmp_to_key

from clock_readings import display_log, rational
from kinematics import Geometry, arrive, received_by
from local_records import LocalRecord, Payload, RecordError, text_id, validate_history


@dataclass(frozen=True)
class ObserverConfig:
    observer_id: str
    chi: object
    offset: object = 0

    def __post_init__(self):
        text_id(self.observer_id)
        object.__setattr__(self, "chi", rational(self.chi))
        object.__setattr__(self, "offset", rational(self.offset))


@dataclass(frozen=True)
class EmissionSpec:
    signal_id: str
    emitter_id: str
    target_id: str
    emitted_at: object
    reference_frequency: object = 1
    crest_id: str = "crest-1"
    message: str = "declared-pulse-train"

    def __post_init__(self):
        for name in ("signal_id", "emitter_id", "target_id", "crest_id"):
            text_id(getattr(self, name))
        if len(self.signal_id) > 60 or self.emitter_id == self.target_id:
            raise ValueError("bounded distinct signal endpoint identities required")
        frequency = rational(self.reference_frequency)
        if frequency <= 0:
            raise ValueError("positive emitted reference frequency required")
        object.__setattr__(self, "reference_frequency", frequency)


@dataclass(frozen=True)
class Simulation:
    """Immutable local histories and separate mutable producer audit, not custody."""

    histories: tuple
    audit: dict

    def history(self, observer_id):
        for name, records in self.histories:
            if name == observer_id:
                return records
        raise ValueError("observer not in this experiment")


def simulate(geometry, observers, emissions, cutoff, places=9, calibration_id="ideal-v1"):
    """Produce every in-window emission; no scheduled future emission is invented.

    All supplied emissions must already be at/before cutoff. Invalid schedules
    are refused, not filtered. Existence, order and cutoff comparisons are exact.
    Rounded local clocks are created only after those decisions.
    """
    if type(geometry) is not Geometry:
        raise ValueError("this supplied geometry type is required")
    if (
        type(observers) is not tuple
        or len(observers) != 2
        or any(type(o) is not ObserverConfig for o in observers)
        or len({o.observer_id for o in observers}) != 2
    ):
        raise ValueError("two distinct nominal comoving observers required")
    if type(emissions) is not tuple or any(type(e) is not EmissionSpec for e in emissions):
        raise ValueError("immutable actual emission schedule required")
    if len({e.signal_id for e in emissions}) != len(emissions):
        raise ValueError("signal identity reused")
    text_id(calibration_id)
    geometry.time(cutoff)
    configs = {o.observer_id: o for o in observers}
    events, forecast = [], []

    def local_clock(moment, observer_id):
        expression = geometry.time(moment)
        return display_log(
            expression.constant + configs[observer_id].offset,
            expression.coefficient,
            expression.argument,
            places=places,
        )

    for spec in emissions:
        if spec.emitter_id not in configs or spec.target_id not in configs:
            raise ValueError("unknown signal endpoint")
        if geometry.compare_times(spec.emitted_at, cutoff) > 0:
            raise ValueError("future scheduled emission cannot be an actual in-window record")
        ell = abs(configs[spec.target_id].chi - configs[spec.emitter_id].chi)
        prediction = arrive(geometry, spec.emitted_at, ell)
        emission_id = "emit:" + spec.signal_id
        payload = Payload(
            emission_id,
            spec.signal_id,
            spec.emitter_id,
            spec.target_id,
            spec.crest_id,
            spec.reference_frequency,
            local_clock(spec.emitted_at, spec.emitter_id),
            spec.message,
        )
        events.append((spec.emitted_at, 0, emission_id, spec.emitter_id, "emission", payload, None))
        visible = received_by(prediction, cutoff)
        if visible:
            events.append(
                (
                    prediction.reception,
                    1,
                    "receive:" + spec.signal_id,
                    spec.target_id,
                    "reception",
                    payload,
                    spec.reference_frequency * prediction.frequency_ratio,
                )
            )
        forecast.append(
            {
                "signal_id": spec.signal_id,
                "emitter_id": spec.emitter_id,
                "target_id": spec.target_id,
                "comoving_separation": str(ell),
                "emission": spec.emitted_at.to_dict(),
                "forecast": prediction.to_dict(),
                "receipt_inside_cutoff": visible,
                "emission_reference_frequency": str(spec.reference_frequency),
            }
        )
    for name in configs:
        events.append((cutoff, 2, "close:" + name, name, "window_closed", None, None))

    def compare(left, right):
        time_order = geometry.compare_times(left[0], right[0])
        if time_order:
            return time_order
        return (left[1:3] > right[1:3]) - (left[1:3] < right[1:3])

    # Equal-time emissions precede receipts; closure comes last. Tie-breaking
    # between unrelated equal-time events is bookkeeping, not new causal order.
    events.sort(key=cmp_to_key(compare))
    history = {name: [] for name in configs}
    for moment, priority, event_id, name, kind, payload, frequency in events:
        previous = history[name][-1].event_id if history[name] else "start:" + name
        timestamp = payload.emitter_timestamp if kind == "emission" else local_clock(moment, name)
        history[name].append(
            LocalRecord(
                event_id,
                name,
                kind,
                timestamp,
                previous,
                payload,
                frequency,
                calibration_id,
                "synthetic:observer-signal-v1",
            )
        )
    histories = tuple((name, validate_history(name, tuple(rows))) for name, rows in history.items())
    # A cross-observer match check is producer-side, never fed to receiver inference.
    emitted = {
        row.payload.signal_id: row
        for _, rows in histories
        for row in rows
        if row.kind == "emission"
    }
    for _, rows in histories:
        for row in rows:
            if row.kind == "reception" and row.payload != emitted[row.payload.signal_id].payload:
                raise RecordError("producer changed a transmitted payload")
    audit = {
        "model_status": "supplied_geometry_and_null_propagation_only",
        "geometry": geometry.to_dict(),
        "cutoff": cutoff.to_dict(),
        "observers": [
            {"observer_id": o.observer_id, "chi": str(o.chi), "offset": str(o.offset)}
            for o in observers
        ],
        "forecast": forecast,
        "display_places": places,
        "actualization_to_geometry_rule": None,
    }
    return Simulation(histories, audit)
