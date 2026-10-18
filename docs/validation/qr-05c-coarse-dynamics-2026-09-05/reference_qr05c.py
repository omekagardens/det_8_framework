"""Independent finite coarse-dynamics reference for QR-05C.

This module imports no QR, DET, T8, or RET implementation.  It enumerates
transitive upper-triangular orders independently and derives the diagonal
superoperator coefficients of the specified instruments from rational pairs.
Classical records are coarsened while quantum blocks are retained.  No
continuum, spacetime, or gravitational conclusion is implemented or asserted.

The fixed fixture interface is ``analyze(wire)``.  Zero source maps and zero
birth edges survive; universal and fixed-source comparisons remain separate.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import pairwise, permutations, product

F = Fraction
_ZERO = (F(0), F(0))
_ONE = (F(1), F(0))
_CASES = {
    "weak_phase": ("percolation", F(2, 5), False),
    "grouped_dephase": ("percolation", F(2, 5), True),
    "zero_link_boundary": ("percolation", F(0), False),
    "chain_boundary": ("percolation", F(1), False),
    "normalized_noncovariant_growth": ("uniform_ideals", None, False),
}
_SUMMARIES = ("marked_order", "shape_ones", "link_counts_ones", "size_ones")
_INPUTS = ((F(0), F(0), F(0)), (F(1, 2), F(0), F(0)), (F(0), F(1, 2), F(0)), (F(0), F(0), F(1, 2)))
_EFFECTS = ("P0", "P1", "P+X", "P+Y")


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _bounded(value):
    _require(
        abs(value.numerator).bit_length() <= 4096 and value.denominator.bit_length() <= 4096,
        "reference rational exceeds 4096-bit bound",
    )
    return value


def _plus(a, b):
    return (_bounded(a[0] + b[0]), _bounded(a[1] + b[1]))


def _times(a, b):
    return (_bounded(a[0] * b[0] - a[1] * b[1]), _bounded(a[0] * b[1] + a[1] * b[0]))


class _Diagonal(tuple):
    """Tag internal map values, so only referenced maps enter the wire bank."""

    def __new__(cls, values):
        result = tuple(values)
        _require(len(result) == 4, "reference diagonal must have four coefficients")
        for real, imag in result:
            _bounded(real)
            _bounded(imag)
        return tuple.__new__(cls, result)


_ZERO_MAP = _Diagonal((_ZERO,) * 4)
_IDENTITY = _Diagonal((_ONE,) * 4)


def _add(a, b):
    return _Diagonal(_plus(x, y) for x, y in zip(a, b))


def _scale(a, weight):
    return _Diagonal(_times(x, (weight, F(0))) for x in a)


def _compose(after, before):
    return _Diagonal(_times(x, y) for x, y in zip(after, before))


def _sum(maps):
    result = _ZERO_MAP
    for value in maps:
        result = _add(result, value)
    return result


def _cp(matrix):
    """Schur-multiplier CP test: its nonzero Choi block must be positive."""
    a, b, c, d = matrix
    return (
        a[1] == d[1] == 0
        and a[0] >= 0
        and d[0] >= 0
        and c == (b[0], -b[1])
        and b[0] ** 2 + b[1] ** 2 <= a[0] * d[0]
    )


def _tp(matrix):
    return matrix[0] == _ONE and matrix[3] == _ONE


def _check_row(row):
    _require(all(_cp(matrix) for matrix in row), "reference transition has a non-CP branch")
    _require(_tp(_sum(row)), "reference transition row is not trace preserving")


def _parse(wire):
    _require(
        type(wire) is dict and set(wire) == {"schema_version", "case"},
        "reference problem must have exactly the specified keys",
    )
    _require(
        type(wire["schema_version"]) is str and wire["schema_version"] == "det8-qr05c-problem-v1",
        "reference schema is unsupported",
    )
    _require(
        type(wire["case"]) is str and wire["case"] in _CASES, "reference case name is unsupported"
    )
    return wire["case"], _CASES[wire["case"]]


def _orders(size):
    cells = tuple((i, j) for i in range(size) for j in range(i + 1, size))
    result = []
    for bits in product((0, 1), repeat=len(cells)):
        relation = {pair for pair, bit in zip(cells, bits) if bit}
        if any(
            (i, j) in relation and (j, k) in relation and (i, k) not in relation
            for i in range(size)
            for j in range(size)
            for k in range(size)
        ):
            continue
        result.append(tuple(tuple(i for i in range(j) if (i, j) in relation) for j in range(size)))
    return tuple(sorted(result))


def _ideals(order):
    result = []
    for bits in product((0, 1), repeat=len(order)):
        selected = tuple(i for i, bit in enumerate(bits) if bit)
        if all(all(past in selected for past in order[node]) for node in selected):
            result.append(selected)
    return tuple(sorted(result))


def _weight(order, past, kind, p):
    if kind == "uniform_ideals":
        return F(1, len(_ideals(order)))
    maximal = sum(not any(node in order[other] for other in past) for node in past)
    return _bounded(p**maximal * (1 - p) ** (len(order) - len(past)))


def _instrument(record, past, outcome, dephase):
    parity = sum(record[node] for node in past) % 2
    a, d = (F(3, 5), F(4, 5)) if outcome == 0 else (F(4, 5), F(3, 5))
    attenuation = F(-7, 25) if dephase else F(1)
    cross = _bounded(a * d * attenuation)
    upper = (cross, F(0)) if parity == 0 else (F(0), -cross)
    lower = (upper[0], -upper[1])
    setting = ("dephase" if dephase else "weak") + str(parity)
    matrix = _Diagonal(((a * a, F(0)), upper, lower, (d * d, F(0))))
    _require(_cp(matrix), "reference fixed instrument branch is not CP")
    return setting, matrix


def _original_source(order, record, kind, p, dephase):
    result = _IDENTITY
    settings = []
    for event, past in enumerate(order):
        setting, matrix = _instrument(record[:event], past, record[event], dephase)
        result = _compose(_scale(matrix, _weight(order[:event], past, kind, p)), result)
        settings.append(setting)
    _require(_cp(result), "reference source map is not CP")
    return tuple(settings), result


def _relation(order, permutation):
    return "".join(
        "1" if first in order[second] else "0" for first in permutation for second in permutation
    )


def _key(name, order, record, settings):
    size = len(order)
    if name == "marked_order":
        return min(
            (_relation(order, perm), tuple((settings[i], record[i]) for i in perm))
            for perm in permutations(range(size))
        )
    if name == "shape_ones":
        return min(_relation(order, perm) for perm in permutations(range(size))), sum(record)
    if name == "link_counts_ones":
        links = sum(
            not any(ancestor in order[middle] for middle in past)
            for past in order
            for ancestor in past
        )
        incomparable = size * (size - 1) // 2 - sum(len(past) for past in order)
        return size, links, incomparable, sum(record)
    return size, sum(record)


def _key_wire(name, key):
    if name == "marked_order":
        return {"relation": key[0], "marks": [list(pair) for pair in key[1]]}
    if name == "shape_ones":
        return {"relation": key[0], "ones": key[1]}
    if name == "link_counts_ones":
        return dict(zip(("n", "links", "incomparable", "ones"), key))
    return dict(zip(("n", "ones"), key))


def _partitions(name, histories):
    levels, lookups = [], []
    for level in histories:
        grouped = {}
        for index, (order, record, settings, _) in enumerate(level):
            key = _key(name, order, record, settings)
            grouped.setdefault(key, []).append(index)
        # Insertion order is first-member order because histories are increasing.
        partition = [
            {"key": _key_wire(name, key), "members": members} for key, members in grouped.items()
        ]
        lookup = [None] * len(level)
        for class_index, group in enumerate(partition):
            for member in group["members"]:
                lookup[member] = class_index
        levels.append(partition)
        lookups.append(lookup)
    return levels, lookups


def _state(bloch):
    x, y, z = bloch
    return (((1 + z) / 2, F(0)), (x / 2, -y / 2), (x / 2, y / 2), ((1 - z) / 2, F(0)))


def _output(matrix, bloch):
    return tuple(_times(coefficient, cell) for coefficient, cell in zip(matrix, _state(bloch)))


def _probability(matrix, bloch, effect):
    cells = _output(matrix, bloch)
    if effect == "P0":
        value = cells[0][0]
    elif effect == "P1":
        value = cells[3][0]
    elif effect == "P+X":
        value = (cells[0][0] + cells[3][0]) / 2 + cells[1][0]
    elif effect == "P+Y":
        value = (cells[0][0] + cells[3][0]) / 2 - cells[1][1]
    else:
        raise ValueError("reference witness effect is unsupported")
    return _bounded(value)


def _trace_probability(matrix, bloch):
    cells = _output(matrix, bloch)
    return _bounded(cells[0][0] + cells[3][0])


def _output_wire(matrix, bloch):
    cells = _output(matrix, bloch)
    return [[[str(part) for part in cells[2 * i + j]] for j in range(2)] for i in range(2)]


def _comparison(size, actual, proposed, partition, lookup, histories):
    conflicts = []
    source_equal = True
    for history, row in enumerate(actual):
        group = lookup[history]
        representative = partition[group]["members"][0]
        trial = proposed[group]
        targets = [index for index, (left, right) in enumerate(zip(row, trial)) if left != right]
        if targets:
            conflicts.append(
                {"history": history, "representative": representative, "targets": targets}
            )
        source = histories[history][3]
        for left, right in zip(row, trial):
            if _compose(left, source) != _compose(right, source):
                source_equal = False
    witness = None
    if conflicts:
        conflict = conflicts[0]
        history, target = conflict["history"], conflict["targets"][0]
        left = actual[history][target]
        right = proposed[lookup[history]][target]
        for bloch in _INPUTS:
            for effect in _EFFECTS:
                a, b = _probability(left, bloch, effect), _probability(right, bloch, effect)
                if a != b:
                    witness = {
                        "history": history,
                        "representative": conflict["representative"],
                        "target": target,
                        "input_bloch": [str(value) for value in bloch],
                        "effect": effect,
                        "actual_probability": str(a),
                        "proposed_probability": str(b),
                    }
                    break
            if witness is not None:
                break
        _require(
            witness is not None, "reference Hermitian-spanning witness bank missed a discrepancy"
        )
    return {
        "births": size,
        "actual_rows": actual,
        "representative_rows": proposed,
        "consistent": not conflicts,
        "all_fixed_source_branches_equal": source_equal,
        "conflicts": conflicts,
        "first_witness": witness,
    }


def _quotient(name, histories, edges):
    partitions, class_of = _partitions(name, histories)
    steps = []
    for size in range(4):
        targets = len(partitions[size + 1])
        actual = []
        for edge_row in edges[size]:
            row = [_ZERO_MAP] * targets
            for edge in edge_row:
                target = class_of[size + 1][edge["target"]]
                row[target] = _add(row[target], edge["kernel"])
            _check_row(row)
            actual.append(row)
        proposed = [actual[group["members"][0]] for group in partitions[size]]
        for row in proposed:
            _check_row(row)
        steps.append(
            _comparison(size, actual, proposed, partitions[size], class_of[size], histories[size])
        )

    two_steps = []
    for size in range(3):
        targets = len(partitions[size + 2])
        actual = []
        # Follow individual fine edges; do not compose already coarsened rows.
        for edge_row in edges[size]:
            row = [_ZERO_MAP] * targets
            for first in edge_row:
                if first["kernel"] == _ZERO_MAP:
                    continue
                for second in edges[size + 1][first["target"]]:
                    if second["kernel"] == _ZERO_MAP:
                        continue
                    target = class_of[size + 2][second["target"]]
                    row[target] = _add(row[target], _compose(second["kernel"], first["kernel"]))
            _check_row(row)
            actual.append(row)
        proposed = []
        second_rows = steps[size + 1]["representative_rows"]
        for first_row in steps[size]["representative_rows"]:
            row = [_ZERO_MAP] * targets
            for middle, first in enumerate(first_row):
                if first == _ZERO_MAP:
                    continue
                for target, second in enumerate(second_rows[middle]):
                    if second != _ZERO_MAP:
                        row[target] = _add(row[target], _compose(second, first))
            _check_row(row)
            proposed.append(row)
        two_steps.append(
            _comparison(size, actual, proposed, partitions[size], class_of[size], histories[size])
        )
    return {
        "name": name,
        "partitions": partitions,
        "steps": steps,
        "two_steps": two_steps,
    }, class_of


def _controls(quotients, lookups, history_indices):
    by_name = {quotient["name"]: quotient for quotient in quotients}
    shape = by_name["shape_ones"]
    chain = ((), (0,))
    fork = ((), (0,), (0,))
    join = ((), (), (0, 1))
    single_edge = ((), (), (0,))
    chain_histories = [history_indices[2][(chain, record)] for record in ((0, 1), (1, 0))]
    fork_one = history_indices[3][(fork, (0, 0, 1))]
    fork_target = lookups["shape_ones"][3][fork_one]
    kernels = [
        shape["steps"][2]["actual_rows"][history][fork_target] for history in chain_histories
    ]
    pure_x = (F(1), F(0), F(0))
    chain_control = {
        "births": 2,
        "quotient": "shape_ones",
        "histories": chain_histories,
        "target": fork_target,
        "kernels": kernels,
        "input_bloch": ["1", "0", "0"],
        "outputs": [_output_wire(matrix, pure_x) for matrix in kernels],
        "trace_probabilities": [str(_trace_probability(matrix, pure_x)) for matrix in kernels],
        "probabilities_Px": [str(_probability(matrix, pure_x, "P+X")) for matrix in kernels],
    }
    one_history = history_indices[1][(((),), (1,))]
    one_class = lookups["shape_ones"][1][one_history]
    representative = shape["partitions"][1][one_class]["members"][0]
    one_step_exact = (
        shape["steps"][1]["actual_rows"][one_history]
        == shape["steps"][1]["representative_rows"][one_class]
    )
    actual = shape["two_steps"][1]["actual_rows"][one_history][fork_target]
    proposed = shape["two_steps"][1]["representative_rows"][one_class][fork_target]
    delayed = {
        "births": 1,
        "quotient": "shape_ones",
        "history": one_history,
        "representative": representative,
        "target": fork_target,
        "one_step_exact": one_step_exact,
        "actual": actual,
        "proposed": proposed,
        "input_bloch": ["1", "0", "0"],
        "outputs": [_output_wire(matrix, pure_x) for matrix in (actual, proposed)],
        "trace_probabilities": [
            str(_trace_probability(matrix, pure_x)) for matrix in (actual, proposed)
        ],
        "probabilities_Px": [
            str(_probability(matrix, pure_x, "P+X")) for matrix in (actual, proposed)
        ],
    }
    link = by_name["link_counts_ones"]
    order_histories = [history_indices[3][(order, (0, 0, 0))] for order in (fork, join)]
    order_rows = [link["steps"][3]["actual_rows"][history] for history in order_histories]
    probe_targets = [
        index
        for index, group in enumerate(link["partitions"][4])
        if group["key"]["incomparable"] == 1
    ]
    fork_join = {
        "births": 3,
        "quotient": "link_counts_ones",
        "histories": order_histories,
        "parent_class_same": lookups["link_counts_ones"][3][order_histories[0]]
        == lookups["link_counts_ones"][3][order_histories[1]],
        "one_step_rows_equal": order_rows[0] == order_rows[1],
        "counts_probe_incomparable": 1,
        "probabilities": [
            str(_trace_probability(_sum(row[index] for index in probe_targets), _INPUTS[0]))
            for row in order_rows
        ],
    }
    located = [history_indices[3][(single_edge, record)] for record in ((0, 0, 1), (0, 1, 0))]
    location_rows = [shape["steps"][3]["actual_rows"][history] for history in located]
    first_target = next(
        (index for index, pair in enumerate(zip(*location_rows)) if pair[0] != pair[1]), None
    )
    record_location = {
        "births": 3,
        "quotient": "shape_ones",
        "histories": located,
        "parent_class_same": lookups["shape_ones"][3][located[0]]
        == lookups["shape_ones"][3][located[1]],
        "row_equal": location_rows[0] == location_rows[1],
        "first_target": first_target,
        "kernels": [] if first_target is None else [row[first_target] for row in location_rows],
    }
    marked = by_name["marked_order"]
    marked_class = next(
        index for index, group in enumerate(marked["partitions"][2]) if len(group["members"]) > 1
    )
    members = marked["partitions"][2][marked_class]["members"]
    correct = marked["steps"][2]["representative_rows"][marked_class]
    wrong = [
        _sum(marked["steps"][2]["actual_rows"][history][target] for history in members)
        for target in range(len(correct))
    ]
    _require(all(_cp(matrix) for matrix in wrong), "reference multiplicity control lost CP")
    wrong_parent_sum = {
        "births": 2,
        "quotient": "marked_order",
        "parent_class": marked_class,
        "members": members,
        "correct_row": correct,
        "wrong_row": wrong,
        "correct_trace": str(_trace_probability(_sum(correct), _INPUTS[0])),
        "wrong_trace": str(_trace_probability(_sum(wrong), _INPUTS[0])),
    }
    return {
        "chain_record": chain_control,
        "delayed": delayed,
        "fork_join": fork_join,
        "record_location": record_location,
        "wrong_parent_sum": wrong_parent_sum,
    }


def _pack(raw):
    maps = {_ZERO_MAP}

    def collect(value):
        if isinstance(value, _Diagonal):
            maps.add(value)
        elif type(value) is dict:
            for nested in value.values():
                collect(nested)
        elif type(value) is list:
            for nested in value:
                collect(nested)

    collect(raw)
    _require(all(_cp(matrix) for matrix in maps), "reference map bank contains a non-CP map")
    flattened = lambda matrix: tuple(str(part) for cell in matrix for part in cell)
    ordered = [_ZERO_MAP, *sorted(maps - {_ZERO_MAP}, key=flattened)]
    indices = {matrix: index for index, matrix in enumerate(ordered)}

    def replace(value):
        if isinstance(value, _Diagonal):
            return indices[value]
        if type(value) is dict:
            return {key: replace(nested) for key, nested in value.items()}
        if type(value) is list:
            return [replace(nested) for nested in value]
        return value

    result = replace(raw)
    result["map_bank"] = [[[str(part) for part in cell] for cell in matrix] for matrix in ordered]
    result["counts"]["map_bank_entries"] = len(ordered)
    return result


def analyze(wire):
    """Return complete exact tables for one fixed, bounded QR-05C case."""
    case, (kind, p, dephase) = _parse(wire)
    histories, history_indices, levels = [], [], []
    for size in range(5):
        internal, public = [], []
        for order in _orders(size):
            for record in product((0, 1), repeat=size):
                settings, source = _original_source(order, record, kind, p, dephase)
                internal.append((order, record, settings, source))
                public.append(
                    {
                        "order": [list(past) for past in order],
                        "outcomes": list(record),
                        "settings": list(settings),
                        "source": source,
                    }
                )
        histories.append(internal)
        history_indices.append(
            {(entry[0], entry[1]): index for index, entry in enumerate(internal)}
        )
        levels.append({"births": size, "histories": public})

    edges, fine_steps = [], []
    for size in range(4):
        rows = []
        for order, record, _, _ in histories[size]:
            row = []
            for past in _ideals(order):
                scalar = _weight(order, past, kind, p)
                instrument_maps = []
                for outcome in (0, 1):
                    setting, matrix = _instrument(record, past, outcome, dephase)
                    instrument_maps.append(matrix)
                    kernel = _scale(matrix, scalar)
                    target = history_indices[size + 1][(order + (past,), record + (outcome,))]
                    row.append(
                        {
                            "target": target,
                            "precursor": list(past),
                            "growth_weight": str(scalar),
                            "setting": setting,
                            "outcome": outcome,
                            "kernel": kernel,
                        }
                    )
                _check_row(instrument_maps)
            _check_row([edge["kernel"] for edge in row])
            rows.append(row)
        edges.append(rows)
        fine_steps.append({"births": size, "rows": rows})

    quotients, lookups = [], {}
    for name in _SUMMARIES:
        quotient, class_of = _quotient(name, histories, edges)
        quotients.append(quotient)
        lookups[name] = class_of
    refinements = []
    for fine, coarse in pairwise(quotients):
        rows = []
        for size in range(5):
            parent_classes = []
            valid = True
            for group in fine["partitions"][size]:
                coarse_classes = {
                    lookups[coarse["name"]][size][member] for member in group["members"]
                }
                valid = valid and len(coarse_classes) == 1
                parent_classes.append(lookups[coarse["name"]][size][group["members"][0]])
            _require(valid, "reference proposed partition family is not nested")
            rows.append({"births": size, "parent_classes": parent_classes, "valid": valid})
        refinements.append({"fine": fine["name"], "coarse": coarse["name"], "levels": rows})

    covariance = []
    for size in range(5):
        conflicts = []
        for group in quotients[0]["partitions"][size]:
            representative = group["members"][0]
            for history in group["members"]:
                if histories[size][representative][3] != histories[size][history][3]:
                    conflicts.append([representative, history])
        covariance.append(
            {"births": size, "constant": not conflicts, "conflicts": sorted(conflicts)}
        )
    controls = _controls(quotients, lookups, history_indices)
    raw = {
        "case": case,
        "levels": levels,
        "fine_steps": fine_steps,
        "quotients": quotients,
        "refinements": refinements,
        "source_covariance": covariance,
        "controls": controls,
        "counts": {
            "level_histories": [len(level) for level in histories],
            "raw_birth_edges": sum(len(row) for level in edges for row in level),
            "marked_classes": [len(level) for level in quotients[0]["partitions"]],
            "one_step_checks": sum(
                len(histories[size]) * len(quotient["partitions"][size + 1])
                for quotient in quotients
                for size in range(4)
            ),
            "two_step_checks": sum(
                len(histories[size]) * len(quotient["partitions"][size + 2])
                for quotient in quotients
                for size in range(3)
            ),
            "map_bank_entries": 0,
        },
    }
    return _pack(raw)
