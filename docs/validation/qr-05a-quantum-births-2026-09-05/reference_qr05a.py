"""Independent exact reference for the bounded QR-05A birth fixtures.

Natural orders are enumerated as transitive upper-triangular relation matrices,
not generated recursively by births.  Complete maps are composed as 4 by 4
superoperators using SHA-pinned QR-01 complex-pair arithmetic.  No primary
QR-05A implementation, DET model, RET source, or T8 implementation is imported.

The calculation concerns a fixed qubit and a classical mixture of finite order
births.  It does not construct coherent order growth, spacetime, or gravity.
All source-impossible and zero-weight branches, outcome labels, and selected
settings remain explicit.  ``analyze`` accepts exactly the README wire schema
and returns ordinary JSON-compatible data with canonical rational strings.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import re
from fractions import Fraction
from pathlib import Path

_REFERENCE_SHA256 = "d7fab84717c22632e8be7cfd18aca68d439cbf611cf3a47a11abf25a8fca856f"
_REFERENCE_PATH = (
    Path(__file__).resolve().parents[1] / "qr-01-quantum-records-2026-09-05" / "reference.py"
)
if not _REFERENCE_PATH.is_file() or _REFERENCE_PATH.is_symlink():
    raise RuntimeError("QR-05A reference requires a plain pinned arithmetic file")
_REFERENCE_BYTES = _REFERENCE_PATH.read_bytes()
if hashlib.sha256(_REFERENCE_BYTES).hexdigest() != _REFERENCE_SHA256:
    raise RuntimeError("QR-05A reference refuses changed QR-01 arithmetic source")
_SPEC = importlib.util.spec_from_file_location("qr05a_pinned_reference_arithmetic", _REFERENCE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("QR-05A reference could not load pinned arithmetic")
_R = importlib.util.module_from_spec(_SPEC)
# Execute precisely the bytes whose digest was checked, with no second read.
exec(compile(_REFERENCE_BYTES, str(_REFERENCE_PATH), "exec"), _R.__dict__)  # noqa: S102

ComplexPair = tuple[Fraction, Fraction]
Matrix = tuple[tuple[ComplexPair, ...], ...]
Order = tuple[tuple[int, ...], ...]

_ZERO = (Fraction(0), Fraction(0))
_ONE = (Fraction(1), Fraction(0))
_IDENTITY = tuple(tuple(_ONE if i == j else _ZERO for j in range(4)) for i in range(4))
_ZERO_MAP = tuple(tuple(_ZERO for _ in range(4)) for _ in range(4))
_FAMILIES = {"weak_phase", "weak_dephase", "parity_zx", "stage_zx"}


def _parse(wire: object) -> tuple[int, str, Fraction | None, str]:
    """Local validation; no QR-01 or primary-route input validator is reused."""
    if type(wire) is not dict or set(wire) != {"schema_version", "births", "growth", "instrument"}:
        raise ValueError("reference problem must have exactly the specified keys")
    if type(wire["schema_version"]) is not str or wire["schema_version"] != "det8-qr05a-problem-v1":
        raise ValueError("reference problem schema version is unsupported")
    births = wire["births"]
    if type(births) is not int or births not in (1, 2, 3):
        raise ValueError("reference birth count must be one, two, or three")
    family = wire["instrument"]
    if type(family) is not str or family not in _FAMILIES:
        raise ValueError("reference instrument family is unsupported")
    growth = wire["growth"]
    if type(growth) is not dict or type(growth.get("kind")) is not str:
        raise ValueError("reference growth rule must be an object with a string kind")
    kind = growth["kind"]
    if kind == "uniform_ideals":
        if set(growth) != {"kind"}:
            raise ValueError("reference uniform growth has unexpected fields")
        probability = None
    elif kind == "percolation":
        if set(growth) != {"kind", "p"}:
            raise ValueError("reference percolation growth has incorrect fields")
        token = growth["p"]
        if (
            type(token) is not str
            or not 1 <= len(token) <= 256
            or re.fullmatch(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?", token) is None
        ):
            raise ValueError("reference probability must be a bounded canonical rational string")
        try:
            probability = Fraction(token)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("reference probability is invalid") from exc
        if str(probability) != token:
            raise ValueError("reference probability must be canonical")
        if (
            abs(probability.numerator).bit_length() > 64
            or probability.denominator.bit_length() > 64
        ):
            raise ValueError("reference probability exceeds the 64-bit input bound")
        if not 0 <= probability <= 1:
            raise ValueError("reference probability must lie in the closed unit interval")
    else:
        raise ValueError("reference growth rule is unsupported")
    return births, kind, probability, family


def _natural_orders(size: int) -> tuple[Order, ...]:
    """Check all upper-triangular binary relations for transitivity directly."""
    positions = tuple((i, j) for i in range(size) for j in range(i + 1, size))
    accepted = []
    for bits in itertools.product((0, 1), repeat=len(positions)):
        relation = {position for position, bit in zip(positions, bits) if bit}
        if any(
            (i, j) in relation and (j, k) in relation and (i, k) not in relation
            for i in range(size)
            for j in range(size)
            for k in range(size)
        ):
            continue
        accepted.append(
            tuple(tuple(i for i in range(j) if (i, j) in relation) for j in range(size))
        )
    return tuple(sorted(accepted))


def _ideals(order: Order) -> tuple[tuple[int, ...], ...]:
    accepted = []
    for bits in itertools.product((0, 1), repeat=len(order)):
        subset = tuple(i for i, bit in enumerate(bits) if bit)
        if all(all(ancestor in subset for ancestor in order[node]) for node in subset):
            accepted.append(subset)
    return tuple(sorted(accepted))


def _growth(
    order: Order, past: tuple[int, ...], kind: str, probability: Fraction | None
) -> Fraction:
    if kind == "uniform_ideals":
        return Fraction(1, len(_ideals(order)))
    if probability is None:
        raise RuntimeError("reference percolation rule lost its probability")
    maximal_count = sum(not any(node in order[other] for other in past) for node in past)
    return _R._bounded(probability**maximal_count * (1 - probability) ** (len(order) - len(past)))


def _scale(matrix: Matrix, scalar: Fraction) -> Matrix:
    factor = (_R._bounded(scalar), Fraction(0))
    return tuple(tuple(_R._times(factor, cell) for cell in row) for row in matrix)


def _add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(_R._plus(a, b) for a, b in zip(lrow, rrow)) for lrow, rrow in zip(left, right)
    )


def _sum(matrices) -> Matrix:
    total = _ZERO_MAP
    for matrix in matrices:
        total = _add(total, matrix)
    return total


def _wire(matrix: Matrix) -> list:
    return [[[str(real), str(imag)] for real, imag in row] for row in matrix]


def _wire_order(order: Order) -> list[list[int]]:
    return [list(past) for past in order]


def _trace_preserving(matrix: Matrix) -> bool:
    # The trace functional is (1, 0, 0, 1), acting on each input matrix unit.
    return all(
        _R._plus(matrix[0][column], matrix[3][column]) == (_ONE if column in (0, 3) else _ZERO)
        for column in range(4)
    )


def _instrument(family: str, size: int, outcomes: tuple[int, ...], past: tuple[int, ...]):
    """Select a setting from the actual local read context, then fill Kraus maps."""
    parity = sum(outcomes[node] for node in past) % 2
    if family in ("weak_phase", "weak_dephase"):
        setting = ("weak" if family == "weak_phase" else "dephase") + str(parity)
        phase = _ONE if parity == 0 else (Fraction(0), Fraction(1))
        kraus_outcomes = []
        for outcome in (0, 1):
            a, b = (
                (Fraction(3, 5), Fraction(4, 5))
                if outcome == 0
                else (Fraction(4, 5), Fraction(3, 5))
            )
            base = (((a, Fraction(0)), _ZERO), (_ZERO, _R._times((b, Fraction(0)), phase)))
            if family == "weak_phase":
                operators = (base,)
            else:
                signed = (
                    base[0],
                    tuple(_R._times((Fraction(-1), Fraction(0)), cell) for cell in base[1]),
                )
                operators = (_scale(base, Fraction(3, 5)), _scale(signed, Fraction(4, 5)))
            kraus_outcomes.append(operators)
    else:
        setting = "Z" if (size % 2 if family == "stage_zx" else parity) == 0 else "X"
        if setting == "Z":
            kraus_outcomes = [
                (((_ONE, _ZERO), (_ZERO, _ZERO)),),
                (((_ZERO, _ZERO), (_ZERO, _ONE)),),
            ]
        else:
            half = (Fraction(1, 2), Fraction(0))
            minus_half = (Fraction(-1, 2), Fraction(0))
            kraus_outcomes = [
                (((half, half), (half, half)),),
                (((half, minus_half), (minus_half, half)),),
            ]
    complete = True
    for i in range(2):
        for j in range(2):
            value = _ZERO
            for operators in kraus_outcomes:
                for operator in operators:
                    for k in range(2):
                        value = _R._plus(
                            value, _R._times(_R._conjugate(operator[k][i]), operator[k][j])
                        )
            complete = complete and value == (_ONE if i == j else _ZERO)
    maps = tuple(_R._outcome_superoperator(operators, 2) for operators in kraus_outcomes)
    return setting, maps, complete


def _history(
    order: Order, outcomes: tuple[int, ...], kind: str, probability: Fraction | None, family: str
):
    matrix = _IDENTITY
    weight = Fraction(1)
    settings = []
    for node, past in enumerate(order):
        scalar = _growth(order[:node], past, kind, probability)
        setting, branches, _ = _instrument(family, node, outcomes[:node], past)
        matrix = _R._compose(_scale(branches[outcomes[node]], scalar), matrix)
        weight = _R._bounded(weight * scalar)
        settings.append(setting)
    return tuple(settings), weight, matrix


def analyze(wire: object) -> dict:
    """Return the full finite normalization, diamond, and relabeling inventory."""
    births, kind, probability, family = _parse(wire)
    orders_by_size = tuple(_natural_orders(size) for size in range(births + 1))
    inventory = []
    levels = []
    for size, orders in enumerate(orders_by_size):
        histories = []
        raw = []
        for order in orders:
            for outcomes in itertools.product((0, 1), repeat=size):
                settings, weight, matrix = _history(order, outcomes, kind, probability, family)
                raw.append((order, outcomes, settings, weight, matrix))
                histories.append(
                    {
                        "order": _wire_order(order),
                        "outcomes": list(outcomes),
                        "settings": list(settings),
                        "weight": str(weight),
                        "superoperator": _wire(matrix),
                    }
                )
        total_map = _sum(entry[4] for entry in raw)
        levels.append(
            {
                "births": size,
                "histories": histories,
                "total_map": _wire(total_map),
                "trace_preserving": _trace_preserving(total_map),
            }
        )
        inventory.append(raw)

    normalization = []
    for size in range(births):
        for order in orders_by_size[size]:
            ideals = _ideals(order)
            for outcomes in itertools.product((0, 1), repeat=size):
                growth_sum = Fraction(0)
                complete = True
                birth_sum = _ZERO_MAP
                for past in ideals:
                    scalar = _growth(order, past, kind, probability)
                    growth_sum = _R._bounded(growth_sum + scalar)
                    _, maps, valid = _instrument(family, size, outcomes, past)
                    complete = complete and valid
                    for matrix in maps:
                        birth_sum = _add(birth_sum, _scale(matrix, scalar))
                normalization.append(
                    {
                        "order": _wire_order(order),
                        "outcomes": list(outcomes),
                        "growth_sum": str(growth_sum),
                        "instrument_complete": complete,
                        "birth_sum_trace_preserving": _trace_preserving(birth_sum),
                    }
                )

    diamonds = []
    for size in range(births - 1):
        for order in orders_by_size[size]:
            ideals = _ideals(order)
            for outcomes in itertools.product((0, 1), repeat=size):
                for left in ideals:
                    for right in ideals:
                        fw = _R._bounded(
                            _growth(order, left, kind, probability)
                            * _growth(order + (left,), right, kind, probability)
                        )
                        rw = _R._bounded(
                            _growth(order, right, kind, probability)
                            * _growth(order + (right,), left, kind, probability)
                        )
                        branches = []
                        equal_unweighted = True
                        equal_weighted = True
                        for x, y in itertools.product((0, 1), repeat=2):
                            a_first, a_maps, _ = _instrument(family, size, outcomes, left)
                            b_second, bs_maps, _ = _instrument(
                                family, size + 1, outcomes + (x,), right
                            )
                            b_first, b_maps, _ = _instrument(family, size, outcomes, right)
                            a_second, as_maps, _ = _instrument(
                                family, size + 1, outcomes + (y,), left
                            )
                            forward = _R._compose(bs_maps[y], a_maps[x])
                            reverse = _R._compose(as_maps[x], b_maps[y])
                            weighted_forward, weighted_reverse = (
                                _scale(forward, fw),
                                _scale(reverse, rw),
                            )
                            forward_settings, reverse_settings = (
                                [a_first, b_second],
                                [a_second, b_first],
                            )
                            labels_equal = forward_settings == reverse_settings
                            equal_unweighted = (
                                equal_unweighted and labels_equal and forward == reverse
                            )
                            equal_weighted = (
                                equal_weighted
                                and labels_equal
                                and weighted_forward == weighted_reverse
                            )
                            branches.append(
                                {
                                    "outcomes": [x, y],
                                    "forward_settings": forward_settings,
                                    "reverse_settings": reverse_settings,
                                    "forward": _wire(forward),
                                    "reverse": _wire(reverse),
                                    "weighted_forward": _wire(weighted_forward),
                                    "weighted_reverse": _wire(weighted_reverse),
                                }
                            )
                        diamonds.append(
                            {
                                "order": _wire_order(order),
                                "outcomes": list(outcomes),
                                "left_ideal": list(left),
                                "right_ideal": list(right),
                                "forward_weight": str(fw),
                                "reverse_weight": str(rw),
                                "unweighted_equal": equal_unweighted,
                                "weighted_equal": equal_weighted,
                                "branches": branches,
                            }
                        )

    terminal = inventory[-1]
    index = {(entry[0], entry[1]): i for i, entry in enumerate(terminal)}
    relabelings = []
    grouped = {}
    nonidentity_count = 0
    identity = tuple(range(births))
    for history_index, (order, outcomes, settings, _, matrix) in enumerate(terminal):
        canonical_candidates = []
        for permutation in itertools.permutations(range(births)):
            position = {old: new for new, old in enumerate(permutation)}
            transported_outcomes = tuple(outcomes[old] for old in permutation)
            expected_settings = tuple(settings[old] for old in permutation)
            # Class representatives range over every permutation, not just birth orders.
            relation = "".join(
                "1" if permutation[i] in order[permutation[j]] else "0"
                for i in range(births)
                for j in range(births)
            )
            record = tuple(zip(expected_settings, transported_outcomes))
            canonical_candidates.append((relation, record))
            if not all(
                position[past] < position[node] for node in range(births) for past in order[node]
            ):
                continue
            transported_order = tuple(
                tuple(sorted(position[past] for past in order[old])) for old in permutation
            )
            target_index = index[(transported_order, transported_outcomes)]
            target_entry = terminal[target_index]
            settings_equal = target_entry[2] == expected_settings
            map_equal = target_entry[4] == matrix
            relabelings.append(
                {
                    "history": history_index,
                    "permutation": list(permutation),
                    "target": target_index,
                    "settings_expected": list(expected_settings),
                    "settings_equal": settings_equal,
                    "map_equal": map_equal,
                    "equal": settings_equal and map_equal,
                }
            )
            nonidentity_count += permutation != identity
        key = min(canonical_candidates)
        grouped.setdefault(key, []).append(history_index)
    classes = []
    for (relation, record), members in sorted(grouped.items()):
        total_map = _sum(terminal[member][4] for member in members)
        classes.append(
            {
                "key": {"relation": relation, "record": [list(pair) for pair in record]},
                "members": members,
                "superoperator": _wire(total_map),
            }
        )

    return {
        "levels": levels,
        "normalization": normalization,
        "diamonds": diamonds,
        "relabelings": relabelings,
        "classes": classes,
        "flags": {
            "normalized": all(level["trace_preserving"] for level in levels)
            and all(
                row["growth_sum"] == "1"
                and row["instrument_complete"]
                and row["birth_sum_trace_preserving"]
                for row in normalization
            ),
            "unweighted_diamonds_equal": all(row["unweighted_equal"] for row in diamonds),
            "weighted_diamonds_equal": all(row["weighted_equal"] for row in diamonds),
            "terminal_relabeling_equal": all(row["equal"] for row in relabelings),
        },
        "counts": {
            "level_histories": [len(level["histories"]) for level in levels],
            "normalization_rows": len(normalization),
            "diamond_contexts": len(diamonds),
            "diamond_outcome_pairs": 4 * len(diamonds),
            "terminal_relabelings": len(relabelings),
            "nonidentity_relabelings": nonidentity_count,
            "terminal_classes": len(classes),
            "zero_terminal_maps": sum(entry[4] == _ZERO_MAP for entry in terminal),
        },
    }
