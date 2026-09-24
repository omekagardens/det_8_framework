"""Independent exact direct-form-I oracle for the small RI-55 systems.

Authored from the accepted design without reading the new operator engine.
Only standard-library Fraction arithmetic is used. This module does not load
coefficients or samples, implement the production filter, or certify admitted
coefficient rows. The published Decimal reference is a separate dependency of
the qualifier, not an implementation or independence claim made here.
"""

from collections.abc import Sequence
from fractions import Fraction
from itertools import product


MAX_LENGTH = 64
MAX_STAGES = 8
MAX_SECTIONS = 8
MAX_BOX_DIMENSION = 8
TOY_LENGTHS = (4, 7)
TOY_SIDE_LENGTHS = (1, 2)
TOY_AMPLITUDES = (Fraction(0), Fraction(1, 2), Fraction(2))


def _sequence(value, name):
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise ValueError(f"{name} must be a finite sequence")
    return tuple(value)


def _fraction(value, name):
    if type(value) is not Fraction:
        raise ValueError(f"{name} must be a Fraction, without numeric coercion")
    return value


def _length(value):
    if type(value) is not int or not 2 <= value <= MAX_LENGTH:
        raise ValueError(f"length must be an integer in [2, {MAX_LENGTH}]")
    return value


def _prepare(length, stages, padlens):
    _length(length)
    stage_sequence = _sequence(stages, "stages")
    padding = _sequence(padlens, "padlens")
    if not 1 <= len(stage_sequence) <= MAX_STAGES:
        raise ValueError(f"supply between 1 and {MAX_STAGES} stages")
    if len(stage_sequence) != len(padding):
        raise ValueError("one padding length is required for every stage")
    prepared = []
    for stage_index, (stage, padlen) in enumerate(zip(stage_sequence, padding)):
        if type(padlen) is not int or not 0 <= padlen < length - 1:
            raise ValueError(f"padlens[{stage_index}] must be in [0, length-1)")
        rows = _sequence(stage, f"stages[{stage_index}]")
        if not 1 <= len(rows) <= MAX_SECTIONS:
            raise ValueError(f"each stage must have between 1 and {MAX_SECTIONS} sections")
        sections = []
        for row_index, row in enumerate(rows):
            name = f"stages[{stage_index}][{row_index}]"
            coefficients = _sequence(row, name)
            if len(coefficients) != 6:
                raise ValueError(f"{name} must contain six coefficients")
            coefficients = tuple(
                _fraction(value, f"{name}[{column}]")
                for column, value in enumerate(coefficients)
            )
            b0, b1, b2, a0, a1, a2 = coefficients
            if a0 != 1:
                raise ValueError(f"{name}: a0 must equal one")
            denominator = a0 + a1 + a2
            if denominator == 0:
                raise ValueError(f"{name}: DC denominator must be nonzero")
            gain = (b0 + b1 + b2) / denominator
            sections.append((coefficients, gain))
        prepared.append((tuple(sections), padlen))
    return tuple(prepared)


def _pass_fraction(values, sections):
    """Exact DFI pass, including every section's constant prehistory."""
    current = tuple(values)
    original_first = current[0]
    preceding_gain = Fraction(1)
    for coefficients, gain in sections:
        b0, b1, b2, a0, a1, a2 = coefficients
        input_prehistory = original_first * preceding_gain
        output_prehistory = input_prehistory * gain
        x_previous = x_older = input_prehistory
        y_previous = y_older = output_prehistory
        result = []
        for x in current:
            y = (b0 * x + b1 * x_previous + b2 * x_older
                 - a1 * y_previous - a2 * y_older) / a0
            result.append(y)
            x_older, x_previous = x_previous, x
            y_older, y_previous = y_previous, y
        current = tuple(result)
        # Multiplication remains valid when an earlier section has zero gain.
        preceding_gain *= gain
    return current


def _forward_prepared(values, prepared):
    current = tuple(values)
    length = len(current)
    for sections, padlen in prepared:
        left = tuple(2 * current[0] - current[k]
                     for k in range(padlen, 0, -1))
        right = tuple(2 * current[-1] - current[length - 2 - k]
                      for k in range(padlen))
        extended = left + current + right
        first_pass = _pass_fraction(extended, sections)
        second_pass = _pass_fraction(tuple(reversed(first_pass)), sections)
        restored = tuple(reversed(second_pass))
        current = restored[padlen:padlen + length]
    return current


def forward_fraction(values, stages, padlens):
    """Return the complete exact filtered vector as a tuple of Fractions.

    Values and all six SOS coefficients must already be Fraction objects;
    ints, bools and floats are refused. Stages and padding are finite sequences.
    Every stage gets separate odd extension, freshly initialized ordered passes
    in both directions, and unpadding. Inputs are not mutated. Length is bounded
    to 2..64 for the small oracle; this is not an admitted-length processor.
    Checks are explicit and remain enabled under Python -O.
    """
    source = _sequence(values, "values")
    prepared = _prepare(len(source), stages, padlens)
    source = tuple(_fraction(value, f"values[{k}]")
                   for k, value in enumerate(source))
    return _forward_prepared(source, prepared)


def matrix_fraction(length, stages, padlens):
    """Construct the exact row-major matrix from all forward basis columns.

    This construction uses no adjoint, state-transpose formula or engine call.
    It returns a tuple of row tuples, each containing exact Fractions.
    """
    prepared = _prepare(length, stages, padlens)
    columns = []
    for selected in range(length):
        basis = tuple(Fraction(int(k == selected)) for k in range(length))
        columns.append(_forward_prepared(basis, prepared))
    return tuple(tuple(columns[column][row] for column in range(length))
                 for row in range(length))


def toy_configurations():
    """Return the eight RI-55 configurations in their frozen declaration order.

    Each call returns fresh dictionaries with name, stages and padlens fields.
    Nested coefficient/stage/padding sequences are immutable tuples.
    """
    def row(*values):
        return tuple(Fraction(value) for value in values)

    identity = row(1, 0, 0, 1, 0, 0)
    first_order = row(Fraction(1, 2), 0, 0, 1, Fraction(-1, 2), 0)
    biquad = row(Fraction(1, 4), Fraction(1, 8), 0,
                 1, Fraction(-1, 2), Fraction(1, 8))
    fir = row(Fraction(1, 2), Fraction(1, 2), 0, 1, 0, 0)
    zero_dc = row(Fraction(1, 2), Fraction(-1, 2), 0,
                  1, Fraction(-1, 2), 0)
    declarations = (
        ("identity", ((identity,),), (0,)),
        ("first_order", ((first_order,),), (1,)),
        ("biquad", ((biquad,),), (1,)),
        ("two_sections", ((first_order, biquad),), (1,)),
        ("two_stages", ((first_order,), (biquad,)), (1, 0)),
        ("fir", ((fir,),), (1,)),
        ("zero_dc", ((zero_dc,),), (1,)),
        ("zero_dc_then_biquad", ((zero_dc, biquad),), (1,)),
    )
    return tuple({"name": name, "stages": stages, "padlens": padding}
                 for name, stages, padding in declarations)


def toy_center(length):
    """Return the frozen central fixture x[k]=(k-2)/8 for length 4 or 7."""
    if type(length) is not int or length not in TOY_LENGTHS:
        raise ValueError("the frozen central lengths are 4 and 7")
    return tuple(Fraction(k - 2, 8) for k in range(length))


def box_corners_fraction(dimension, amplitude):
    """Enumerate all signed box corners; retain duplicates at zero amplitude."""
    if type(dimension) is not int or not 1 <= dimension <= MAX_BOX_DIMENSION:
        raise ValueError(f"box dimension must be in [1, {MAX_BOX_DIMENSION}]")
    amplitude = _fraction(amplitude, "amplitude")
    if amplitude < 0:
        raise ValueError("amplitude must be nonnegative")
    return tuple(tuple(amplitude * sign for sign in signs)
                 for signs in product((-1, 1), repeat=dimension))


def sharp_box_fraction(offset, row, amplitude):
    """Return exact gain, sharp scalar bound and an attaining box witness.

    The returned dictionary has gain, bound, witness and attained_value fields.
    Witnesses are row-specific. This theorem helper supplies no physical
    continuation and proves no coefficients or envelopes for an actual filter.
    """
    offset = _fraction(offset, "offset")
    amplitude = _fraction(amplitude, "amplitude")
    if amplitude < 0:
        raise ValueError("amplitude must be nonnegative")
    values = _sequence(row, "row")
    if not 1 <= len(values) <= MAX_LENGTH:
        raise ValueError(f"row length must be in [1, {MAX_LENGTH}]")
    values = tuple(_fraction(value, f"row[{k}]")
                   for k, value in enumerate(values))
    orientation = -1 if offset < 0 else 1
    witness = tuple(amplitude * orientation * ((value > 0) - (value < 0))
                    for value in values)
    gain = sum((abs(value) for value in values), Fraction(0))
    bound = abs(offset) + amplitude * gain
    attained = offset + sum((value * continuation
                             for value, continuation in zip(values, witness)),
                            Fraction(0))
    return {"gain": gain, "bound": bound, "witness": witness,
            "attained_value": attained}
