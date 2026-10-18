"""Inspect a caller-pinned ASCII scalar NR reference without fitting or filtering.

The expected byte count and SHA-256 must come from an independent acquisition
receipt. Matching them binds the inspected snapshot; it does not authenticate
its origin or establish the physical meaning of its two columns. This is a
bounded reproducibility inspector, not a general or hostile-file ingester.
"""

import argparse
from collections import Counter
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import stat


MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOKEN_CHARACTERS = 128
MAX_ADJUSTED_EXPONENT = 1024
CANDIDATE_SPACING = Fraction(1, 4096)
DECIMAL_TOKEN = re.compile(
    r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z"
)
SHA256_TOKEN = re.compile(r"[0-9a-f]{64}\Z")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def verified_bytes(path, expected_bytes, expected_sha256):
    """Bind one complete retained snapshot before any text or number parsing."""
    _require(type(expected_bytes) is int and 0 < expected_bytes <= MAX_FILE_BYTES,
             "expected byte count must be an integer in [1, 8388608]")
    _require(type(expected_sha256) is str and
             SHA256_TOKEN.fullmatch(expected_sha256) is not None,
             "expected SHA-256 must be 64 lowercase hexadecimal characters")
    try:
        path = Path(path)
        information = path.lstat()
        _require(stat.S_ISREG(information.st_mode), "input must be a regular file")
        _require(information.st_size == expected_bytes, "input byte count mismatch")
        with path.open("rb") as stream:
            payload = stream.read(expected_bytes + 1)
    except OSError as error:
        raise ValueError("input cannot be read") from error
    _require(len(payload) == expected_bytes, "retained snapshot byte count mismatch")
    _require(hashlib.sha256(payload).hexdigest() == expected_sha256,
             "retained snapshot SHA-256 mismatch")
    return payload


def exact_decimal(token, label):
    """Return exact represented value and last-place quantum, without rounding."""
    _require(type(token) is str and 0 < len(token) <= MAX_TOKEN_CHARACTERS,
             label + ": decimal token exceeds supported length")
    _require(DECIMAL_TOKEN.fullmatch(token) is not None,
             label + ": expected a finite decimal token")
    try:
        value = Decimal(token)
    except InvalidOperation as error:
        raise ValueError(label + ": invalid decimal token") from error
    _require(value.is_finite(), label + ": nonfinite decimal")
    _require(abs(value.adjusted()) <= MAX_ADJUSTED_EXPONENT,
             label + ": adjusted decimal exponent exceeds supported bound")
    parts = value.as_tuple()
    coefficient = 0
    for digit in parts.digits:
        coefficient = coefficient * 10 + digit
    quantum = (Fraction(10 ** parts.exponent) if parts.exponent >= 0
               else Fraction(1, 10 ** -parts.exponent))
    exact = coefficient * quantum
    if parts.sign:
        exact = -exact
    return exact, quantum


def _ceil(value):
    return -((-value.numerator) // value.denominator)


def grid_diagnostics(times, quanta):
    """Distinguish printed rationals from a hypothetical uniform latent grid."""
    steps = [right - left for left, right in zip(times, times[1:])]
    counts = Counter(steps)
    phases = [time - index * CANDIDATE_SPACING
              for index, time in enumerate(times)]
    residuals = [phase - times[0] for phase in phases]
    lower = max(phase - quantum / 2 for phase, quantum in zip(phases, quanta))
    upper = min(phase + quantum / 2 for phase, quantum in zip(phases, quanta))
    compatible = lower <= upper
    integer_lower = _ceil(lower / CANDIDATE_SPACING)
    integer_upper = (upper / CANDIDATE_SPACING).__floor__()
    integer_compatible = compatible and integer_lower <= integer_upper
    return {
        "printed_time_support": {
            "first": str(times[0]),
            "last": str(times[-1]),
            "last_minus_first": str(times[-1] - times[0]),
            "interpretation": "Closed sample support; no continuation or end-exclusive time inferred.",
        },
        "strictly_increasing": all(step > 0 for step in steps),
        "adjacent_step_counts": [
            {"exact_spacing": str(step), "count": counts[step]}
            for step in sorted(counts)
        ],
        "exact_uniform_printed_spacing": str(steps[0]) if len(counts) == 1 else None,
        "candidate_grid": {
            "rate_hz": 4096,
            "spacing": str(CANDIDATE_SPACING),
            "candidate_authority": "Declared diagnostic, not inferred publisher provenance.",
            "printed_times_exactly_equal_first_plus_index_spacing": all(
                value == 0 for value in residuals
            ),
            "adjacent_steps_exactly_equal_candidate": counts[CANDIDATE_SPACING],
            "phase_minimum": str(min(phases)),
            "phase_maximum": str(max(phases)),
            "maximum_absolute_residual_from_printed_first": str(
                max(abs(value) for value in residuals)
            ),
            "closed_half_last_place_diagnostic": {
                "hypothesis": "Printed time i is within q_i/2 of a+i/4096, where q_i is its decimal last-place quantum.",
                "phase_lower": str(lower),
                "phase_upper": str(upper),
                "common_phase_exists": compatible,
                "zero_origin_integer_grid_phase_exists": integer_compatible,
                "integer_phase_index_minimum": integer_lower if integer_compatible else None,
                "integer_phase_index_maximum": integer_upper if integer_compatible else None,
                "interpretation": "Closed cells leave ties unspecified. Compatibility does not prove original rounding, reconstruction or physical timing; incompatibility rejects only this stated hypothesis.",
            },
            "selected_reconstruction": None,
        },
    }


def inspect_snapshot(payload):
    """Inspect all rows of an already bound byte snapshot; never open a path."""
    _require(type(payload) is bytes and 0 < len(payload) <= MAX_FILE_BYTES,
             "snapshot must contain between 1 byte and 8 MiB")
    try:
        text = payload.decode("ascii", errors="strict")
    except UnicodeDecodeError as error:
        raise ValueError("snapshot is not ASCII") from error
    _require(all(character in "\t\r\n" or 32 <= ord(character) <= 126
                 for character in text), "unsupported ASCII control character")
    lines = text.splitlines()
    rows, times, quanta, blank_lines = [], [], [], []
    for line_number, line in enumerate(lines, start=1):
        tokens = line.split()
        if not tokens:
            blank_lines.append(line_number)
            continue
        _require(len(tokens) == 2, f"line {line_number}: expected exactly two columns")
        time, quantum = exact_decimal(tokens[0], f"line {line_number} time")
        strain, strain_quantum = exact_decimal(tokens[1], f"line {line_number} strain")
        if times:
            _require(time > times[-1], f"line {line_number}: time must strictly increase")
        index = len(rows)
        rows.append({
            "index": index,
            "line_number": line_number,
            "time_token": tokens[0],
            "strain_token": tokens[1],
            "time_exact": str(time),
            "strain_exact": str(strain),
            "time_last_place_quantum": str(quantum),
            "strain_last_place_quantum": str(strain_quantum),
            "time_residual_from_printed_first_plus_index_over_4096": str(
                time - (times[0] if times else time) - index * CANDIDATE_SPACING
            ),
        })
        times.append(time)
        quanta.append(quantum)
    _require(len(rows) >= 2, "at least two numeric rows are required")
    return {
        "text_structure": {
            "encoding": "ASCII",
            "split_line_count": len(lines),
            "blank_line_numbers": blank_lines,
            "blank_line_count": len(blank_lines),
            "numeric_row_count": len(rows),
            "numeric_column_count": 2,
            "finite_decimal_value_count": 2 * len(rows),
            "headers_or_comments_supported": False,
            "ends_with_line_terminator": text.endswith(("\r", "\n")),
            "blank_line_policy": "Blank lines retained by one-based line number; no numeric row omitted.",
        },
        "time_grid": grid_diagnostics(times, quanta),
        "rows": rows,
    }


def inspect_reference(path, expected_bytes, expected_sha256):
    payload = verified_bytes(path, expected_bytes, expected_sha256)
    numeric = inspect_snapshot(payload)
    source = Path(__file__).read_bytes()
    return {
        "schema_version": "gwosc-nr-reference-inspection-v1",
        "status": "snapshot_identity_and_numeric_structure_verified",
        "input_identity": {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()},
        "source_identity": {"filename": "inspect_reference.py", "bytes": len(source),
                            "sha256": hashlib.sha256(source).hexdigest()},
        "identity_boundary": "Expected size and hash are caller-supplied acquisition claims, verified against the complete retained bytes before parsing. URL, redirects and publisher provenance are not independently verified by this program.",
        "supported_resource_limits": {
            "file_bytes_maximum": MAX_FILE_BYTES,
            "decimal_token_characters_maximum": MAX_TOKEN_CHARACTERS,
            "absolute_adjusted_decimal_exponent_maximum": MAX_ADJUSTED_EXPONENT,
            "numeric_rows_minimum": 2,
        },
        "column_interpretation": {
            "column_1": "Named time by contract; exact represented decimal values are inspected.",
            "column_2": "Named strain by contract; exact represented decimal values are inspected.",
            "units_and_physics": "Seconds, dimensionless strain, NR model identity, mass scaling and data-informed amplitude/phase are external publisher claims, not established by these numeric fields.",
        },
        "interpretation_boundary": {
            "numeric_representation": "Fraction arithmetic preserves every decimal token exactly; no binary64 conversion or resampling is performed.",
            "timing": "Printed-time diagnostics establish no absolute arrival time, V1-to-V2 offset transfer, placement or clock calibration.",
            "support": "No interpolation, extrapolation, waveform continuation or boundary condition is supplied.",
            "comparison": "No filter, overlay, fitted shift, sign change, normalization, residual score, significance or parameter recovery is performed.",
            "native_prediction": "No DET forward law, withheld prediction or DET-versus-GR inference is supplied.",
        },
        **numeric,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--expected-bytes", type=int, required=True)
    parser.add_argument("--expected-sha256", required=True)
    arguments = parser.parse_args(argv)
    try:
        report = inspect_reference(arguments.input, arguments.expected_bytes,
                                   arguments.expected_sha256)
    except ValueError as error:
        parser.exit(1, f"reference inspection refused: {error}\n")
    print(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False))


if __name__ == "__main__":
    main()
