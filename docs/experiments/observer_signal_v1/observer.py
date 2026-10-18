"""Receiver-only interpretation. No geometry, arrival, simulator or audit imports."""

from clock_readings import spacing_ratio
from local_records import LocalRecord, RecordError, text_id, validate_history


def infer(observer_id, local_records, expected_signals, calibration_id):
    """Declared signal IDs are preannounced, not inferred from generator state.

    Missing IDs mean only no local receipt by a recorded cutoff. They do not
    establish whether an emission occurred, a horizon, or eternal nonarrival.
    """
    rows = validate_history(observer_id, local_records)
    text_id(calibration_id)
    if (
        type(expected_signals) is not tuple
        or any(type(s) is not str for s in expected_signals)
        or len(set(expected_signals)) != len(expected_signals)
    ):
        raise RecordError("unique preannounced signal identity tuple required")
    for signal in expected_signals:
        text_id(signal)
    if not rows or rows[-1].kind != "window_closed":
        raise RecordError("absence report needs an actual local window-closure record")
    if any(r.calibration_id != calibration_id for r in rows):
        raise RecordError("declared ideal clock/frequency calibration mismatch")
    found, reports = set(), []
    for row in rows:
        if row.kind != "reception":
            continue
        p = row.payload
        if p.signal_id in found:
            raise RecordError("duplicate signal receipt in this one-arrival contract")
        found.add(p.signal_id)
        ratio = row.measured_frequency / p.reference_frequency
        reports.append(
            {
                "signal_id": p.signal_id,
                "event_id": row.event_id,
                "status": "received",
                "frequency_ratio": str(ratio),
                "redshift": str(1 / ratio - 1),
                "flight_time": None,
                "flight_time_status": "unknown_cross_observer_clock_offset",
            }
        )
    for signal in expected_signals:
        if signal not in found:
            reports.append(
                {
                    "signal_id": signal,
                    "event_id": None,
                    "status": "not_received_by_cutoff",
                    "frequency_ratio": None,
                    "redshift": None,
                    "flight_time": None,
                    "flight_time_status": "no_local_receipt",
                }
            )
    return {
        "observer_id": observer_id,
        "cutoff_event_id": rows[-1].event_id,
        "calibration_premise": "unit_rate_local_clocks_common_units_ideal_frequency_reference",
        "results": reports,
    }


def pulse_spacing(first, second):
    """Two ordered receipts from one emitter/receiver and one declared pulse train.

    Transmitted local readings support emitter durations, never clock sync.
    Call on rows retained in validated local-history order.
    """
    if (
        type(first) is not LocalRecord
        or type(second) is not LocalRecord
        or first.kind != "reception"
        or second.kind != "reception"
    ):
        raise RecordError("pulse-spacing requires two actual reception records")
    p, q = first.payload, second.payload
    if (
        first.observer_id != second.observer_id
        or p.emitter_id != q.emitter_id
        or p.message != q.message
        or p.crest_id == q.crest_id
        or p.signal_id == q.signal_id
        or first.calibration_id != second.calibration_id
        or first.provenance != second.provenance
        or first.event_id == second.event_id
        or p.emission_id == q.emission_id
    ):
        raise RecordError("pulse clocks, train or distinct crest identities do not match")
    result = spacing_ratio(
        p.emitter_timestamp, q.emitter_timestamp, first.timestamp, second.timestamp
    )
    return {k: ([str(x) for x in v] if type(v) is tuple else v) for k, v in result.items()}
