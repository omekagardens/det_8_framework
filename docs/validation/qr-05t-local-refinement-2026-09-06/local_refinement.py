"""QR-05T observed local refinement and independent full-subset splitting.

Static utility lineage comes from this primary's QR-05S. No previous or
other executor, artifact, mutable core, or external data is read at runtime.
Local refinement receives fine single-deletion rows and an initial partition
only; H is an independently checked comparator, never a construction input.
"""

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import comb

BIT_LIMIT = 4096
STATE_CAP = 4447
CLASS_CAP = 512
FINE_ATOM_CAP = 168388
LOCAL_CHOICE_CAP = 26682
CLASS_LOCAL_CAP = 3072
PROFILE_ATOM_CAP = 32768
WORKING_CAP = 512 * 1024 * 1024
FRAMES = [
    {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
    {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
]


def _native(value):
    """Validate the object graph and bound its expanded JSON value tree.

    Completed containers are memoized, while an active-path check still
    rejects cycles. Repeated child references contribute repeatedly to the
    tree-node count: deduplicating validation must not hide exponential JSON
    expansion. Each native value node occupies at least one serialized byte,
    so this preflight only rejects values already above the working byte cap.
    """
    active, completed, pending = set(), {}, [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        if leaving:
            children = item if type(item) is list else item.values()
            nodes, height = 1, 0
            for child in children:
                if type(child) in (list, dict):
                    child_nodes, child_height = completed[id(child)]
                    nodes += child_nodes
                    height = max(height, child_height + 1)
                else:
                    nodes += 1
                if nodes > WORKING_CAP:
                    raise ValueError("expanded native value tree exceeds the working-output cap")
            active.remove(id(item))
            completed[id(item)] = (nodes, height)
            continue
        if item is None or type(item) in (str, bool):
            if WORKING_CAP < 1:
                raise ValueError("native value exceeds the working-output cap")
            continue
        if type(item) is int:
            if item.bit_length() > BIT_LIMIT:
                raise ValueError("integer exceeds the exact arithmetic bound")
            if WORKING_CAP < 1:
                raise ValueError("native value exceeds the working-output cap")
            continue
        if type(item) not in (list, dict):
            raise ValueError("expected native exact JSON")
        if depth > 128 or id(item) in active:
            raise ValueError("native JSON is cyclic or exceeds the bounded schema depth")
        if id(item) in completed:
            if depth + completed[id(item)][1] > 128:
                raise ValueError("native JSON exceeds the bounded schema depth")
            continue
        if type(item) is dict and any(type(key) is not str for key in item):
            raise ValueError("wire dictionary keys must be native strings")
        if 1 + len(item) > WORKING_CAP:
            raise ValueError("native value tree exceeds the working-output cap")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if type(item) is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))


def canonical(value):
    _native(value)
    encoded = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    if len(encoded) > WORKING_CAP:
        raise ValueError("retained exact JSON exceeds the working-output cap")
    return encoded


def _digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def _fields(value, keys):
    if (
        type(value) is not dict
        or any(type(key) is not str for key in value)
        or set(value) != set(keys)
    ):
        raise ValueError("unexpected native object fields")


def _integer(value, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum or value.bit_length() > BIT_LIMIT:
        raise ValueError("native integer outside the declared bound")


def _table(table):
    if type(table) is not list or len(table) != 4:
        raise ValueError("polynomial must have four native rows")
    for row in table:
        if type(row) is not list or len(row) != 4:
            raise ValueError("polynomial must have four native columns")
        for value in row:
            if type(value) is not int or value.bit_length() > BIT_LIMIT:
                raise ValueError("polynomial coefficient is not a bounded native integer")


def _key(value):
    """Type-aware private identity for the eventual native wire."""
    if type(value) is Fraction:
        return ("str", str(value))
    if value is None:
        return ("null",)
    if type(value) is str:
        return ("str", value)
    if type(value) is bool:
        return ("bool", value)
    if type(value) is int:
        return ("int", value)
    if type(value) is list:
        return ("list", tuple(_key(item) for item in value))
    if type(value) is dict and all(type(key) is str for key in value):
        return ("dict", tuple((key, _key(value[key])) for key in sorted(value)))
    raise TypeError("unsupported identity value")


def _summaries(supports, odd_mask):
    mean = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    pairs = [[[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for q, chains in enumerate(supports):
        for support in chains:
            mean[q][(support & odd_mask).bit_count()][(support & ~odd_mask).bit_count()] += 1
        for r, others in enumerate(supports):
            for left in chains:
                for right in others:
                    union = left | right
                    odd, even = (union & odd_mask).bit_count(), (union & ~odd_mask).bit_count()
                    if odd > 3 or even > 3:
                        raise ValueError("eligible union exceeds the color bound")
                    pairs[q][r][odd][even] += 1
            if sum(map(sum, pairs[q][r])) != len(chains) * len(others):
                raise ValueError("ordered chain-pair multiplicity was lost")
    if pairs[0] != mean:
        raise ValueError("pair zero row does not recover chain grading")
    return mean, pairs


def _frame_key(frame):
    return [frame["density"], frame["fixed"], frame["eligible"]]


def _kernel_polynomial(parent_sizes, child_sizes):
    """Expand the induced-subset probability, not a fitted/interpolated law."""
    odd_total, even_total = parent_sizes
    odd, even = child_sizes
    if not (0 <= odd <= odd_total <= 3 and 0 <= even <= even_total <= 3):
        raise ValueError("invalid transition color sizes")
    coefficients = [[0] * 4 for _ in range(4)]
    for i in range(odd_total - odd + 1):
        for j in range(even_total - even + 1):
            coefficients[odd + i][even + j] += (
                (-1) ** (i + j) * comb(odd_total - odd, i) * comb(even_total - even, j)
            )
    return coefficients


def _add_table(target, source, multiplier=1):
    for i in range(4):
        for j in range(4):
            target[i][j] += multiplier * source[i][j]


def _normalized(atoms):
    total = [[0] * 4 for _ in range(4)]
    for atom in atoms:
        coefficients = atom["coefficients"]
        if not any(value for row in coefficients for value in row):
            raise ValueError("structural transition has an identically zero polynomial")
        _add_table(total, coefficients)
    if total != [[int(i == 0 and j == 0) for j in range(4)] for i in range(4)]:
        raise ValueError("transition row does not normalize coefficientwise")


def motif_supports(kept, past, eligible):
    """Recognize eligible induced layered K2,2 supports from observation alone.

    Local positions only index the supplied relation. Named colors come from
    original IDs, and every four-set is visited exactly once. Outside vertices
    and whether a relation is a cover have no role in the induced test.
    """
    observed = sorted(set(eligible) & set(kept))
    relation = {
        (kept[left], kept[right])
        for right, predecessors in enumerate(past)
        for left in predecessors
    }
    result = []
    for vertices in combinations(observed, 4):
        odd = [vertex for vertex in vertices if vertex % 2]
        even = [vertex for vertex in vertices if not vertex % 2]
        if len(odd) != 2 or len(even) != 2:
            continue
        # Both orientations of the same-color comparisons are forbidden.
        if any(
            (left, right) in relation or (right, left) in relation for left, right in (odd, even)
        ):
            continue
        forward = all((left, right) in relation for left in odd for right in even)
        reverse = all((right, left) in relation for left in odd for right in even)
        if forward or reverse:
            result.append(list(vertices))
    return result


def _valid_order(kept, past):
    """Validate local indexing and a full strict order, without label causality."""
    if len(set(kept)) != len(kept) or len(past) != len(kept):
        raise ValueError("observation has repeated IDs or inconsistent order size")
    for target, predecessors in enumerate(past):
        if predecessors != sorted(set(predecessors)):
            raise ValueError("past rows must be sorted without duplicate indices")
        if any(type(i) is not int or not 0 <= i < len(kept) for i in predecessors):
            raise ValueError("past index outside the supplied observation")
        if target in predecessors:
            raise ValueError("supplied order is not strict")
        ancestors = set(predecessors)
        if any(not set(past[left]) <= ancestors for left in predecessors):
            raise ValueError("supplied strict relation is not transitively closed")


def _induce(parent_kept, parent_past, kept):
    if len(set(kept)) != len(kept) or not set(kept) <= set(parent_kept):
        raise ValueError("restriction must be an observed vertex subset")
    old = {vertex: index for index, vertex in enumerate(parent_kept)}
    new = {vertex: index for index, vertex in enumerate(kept)}
    return [
        sorted(
            new[parent_kept[index]]
            for index in parent_past[old[vertex]]
            if parent_kept[index] in new
        )
        for vertex in kept
    ]


def _supports(kept, past, eligible):
    """Observed chain sets, retaining each ordered-pair support multiplicity.

    A subset of a strict partial order is a chain exactly when every pair is
    comparable. This criterion is invariant under local reindexing and permits
    such valid descending-ID comparisons as 3<2.
    """
    positions = {vertex: index for index, vertex in enumerate(kept)}
    if 0 not in positions or 7 not in positions:
        raise ValueError("the endpoint probes must be observed")
    bits = {vertex: 1 << bit for bit, vertex in enumerate(eligible)}
    internal = sorted(vertex for vertex in kept if vertex not in (0, 7))
    result = [[] for _ in range(4)]
    bottom, top = positions[0], positions[7]
    for q in range(4):
        for vertices in combinations(internal, q):
            local = [positions[vertex] for vertex in vertices]
            endpoints = bottom in past[top] and all(
                bottom in past[index] and index in past[top] for index in local
            )
            comparable = all(
                left in past[right] or right in past[left] for left, right in combinations(local, 2)
            )
            if endpoints and comparable:
                result[q].append(sum(bits.get(vertex, 0) for vertex in vertices))
    return result


def _state_identity(frame_id, kept, past):
    # Frame IDs are assigned only after exact frame-value equality is checked.
    return frame_id, tuple(kept), tuple(tuple(row) for row in past)


def _round_pushforwards(states, classes):
    rows = []
    for state in states:
        tables = {}
        for atom in state["transitions"]:
            target_class = classes[atom["target_state"]]
            if target_class not in tables:
                tables[target_class] = [[0] * 4 for _ in range(4)]
            _add_table(tables[target_class], atom["coefficients"])
        transitions = [
            {"target_class": target, "coefficients": tables[target]} for target in sorted(tables)
        ]
        _normalized(transitions)
        rows.append({"state_id": state["state_id"], "transitions": transitions})
    return rows


def path_supports(kept, past, eligible):
    """Recognize induced color-layered P4 four-sets from observation alone.

    The entire induced relation must contain exactly three uniformly oriented
    cross comparisons. A complete K2,2 contributes no path support; neither
    traversals, cover edges, nor ascending label order enter the criterion.
    """
    observed = sorted(set(kept) & set(eligible))
    relation = {
        (kept[left], kept[right])
        for right, predecessors in enumerate(past)
        for left in predecessors
    }
    result = []
    for vertices in combinations(observed, 4):
        odd = [vertex for vertex in vertices if vertex % 2]
        even = [vertex for vertex in vertices if not vertex % 2]
        if len(odd) != 2 or len(even) != 2:
            continue
        actual = {
            (left, right) for left, right in relation if left in vertices and right in vertices
        }
        forward = {(left, right) for left in odd for right in even}
        backward = {(right, left) for left in odd for right in even}
        if len(actual) == 3 and (actual < forward or actual < backward):
            result.append(list(vertices))
    return result


def _choose(total, selected):
    return comb(total, selected) if total >= 0 and 0 <= selected <= total else 0


def _colors(value):
    if type(value) is not list or len(value) != 2:
        raise ValueError("color sizes must be two native integers")
    for size in value:
        _integer(size, 0, 3)
    return tuple(value)


def _observations(model):
    """Validate the explicit raw domain and rebuild all observation-derived data.

    Returns (model, features, registry); it never reads a prior artifact.
    Missing induced successors are rejected, rather than supplied by a source
    generator or guessed from feature identities.
    """
    _native(model)
    _fields(model, ("frames", "states"))
    if canonical(model["frames"]) != canonical(FRAMES):
        raise ValueError("model frames differ from the declared marks")
    model = json.loads(canonical(model))
    frames, states = model["frames"], model["states"]
    if type(states) is not list or not 2 <= len(states) <= STATE_CAP:
        raise ValueError("raw observation count outside the parser bound")
    identities, represented, features = {}, set(), []
    for index, state in enumerate(states):
        _fields(state, ("state_id", "frame_id", "kept", "past"))
        _integer(state["state_id"], index, index)
        _integer(state["frame_id"], 0, 1)
        frame = frames[state["frame_id"]]
        kept, past = state["kept"], state["past"]
        if type(kept) is not list or type(past) is not list or not 2 <= len(kept) <= 8:
            raise ValueError("invalid observed vertex or relation lists")
        for vertex in kept:
            _integer(vertex, 0, 7)
        if kept != sorted(set(kept)) or not set(frame["fixed"]) <= set(kept):
            raise ValueError("kept IDs must be unique, sorted and contain fixed vertices")
        if not set(kept) <= set(frame["fixed"] + frame["eligible"]):
            raise ValueError("observed vertex has no declared frame mark")
        for row in past:
            if type(row) is not list:
                raise ValueError("past rows must be native lists")
            for predecessor in row:
                _integer(predecessor, 0, len(kept) - 1)
        _valid_order(kept, past)
        if (
            past[0]
            or past[-1] != list(range(len(kept) - 1))
            or any(0 not in row for row in past[1:])
        ):
            raise ValueError("declared endpoints must bound every observed vertex")
        identity = _state_identity(state["frame_id"], kept, past)
        if identity in identities:
            raise ValueError("duplicate observed state")
        identities[identity] = index
        represented.add(state["frame_id"])
        eligible = frame["eligible"]
        supports = _supports(kept, past, eligible)
        odd_mask = sum(1 << bit for bit, vertex in enumerate(eligible) if vertex % 2)
        mean, pairs = _summaries(supports, odd_mask)
        motifs = motif_supports(kept, past, eligible)
        paths = path_supports(kept, past, eligible)
        color_sizes = [
            sum(vertex % 2 == color for vertex in kept if vertex in eligible) for color in (1, 0)
        ]
        if set(map(tuple, motifs)) & set(map(tuple, paths)):
            raise ValueError("complete and missing-edge motif supports overlap")
        if len(motifs) + len(paths) > comb(color_sizes[0], 2) * comb(color_sizes[1], 2):
            raise ValueError("eligible quartet support bound failed")
        features.append(
            {
                "state_id": index,
                "color_sizes": color_sizes,
                "chain_counts": [len(chains) for chains in supports],
                "mean_graded": mean,
                "pair_graded": pairs,
                "motif_supports": motifs,
                "motif_count": len(motifs),
                "path_supports": paths,
                "path_count": len(paths),
            }
        )
    if represented != {0, 1}:
        raise ValueError("both declared frames must be represented")
    for feature in features:
        recovered = [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]]
        if recovered != feature["color_sizes"]:
            raise ValueError("pair grading does not recover observed eligible color ranks")
    if sum(2 ** sum(feature["color_sizes"]) for feature in features) > FINE_ATOM_CAP:
        raise ValueError("fine subset atom resource cap exceeded")
    return model, features, identities


def _validated_local(local_model):
    _native(local_model)
    _fields(local_model, ("schema_version", "classes"))
    if local_model["schema_version"] != "det8-qr05s-local-v1":
        raise ValueError("unknown local-model schema")
    classes = local_model["classes"]
    if type(classes) is not list or not 1 <= len(classes) <= CLASS_CAP:
        raise ValueError("local class count outside its resource bound")
    atoms = 0
    for class_id, row in enumerate(classes):
        _fields(row, ("class_id", "frame_id", "parent_color_sizes", "odd", "even"))
        _integer(row["class_id"], class_id, class_id)
        _integer(row["frame_id"], 0, 1)
        sizes = _colors(row["parent_color_sizes"])
        for color, name in enumerate(("odd", "even")):
            edges = row[name]
            if type(edges) is not list or len(edges) > 3:
                raise ValueError("each local color row has at most three atoms")
            previous, total = -1, 0
            for edge in edges:
                _fields(edge, ("target_class", "multiplicity"))
                _integer(edge["target_class"], previous + 1, len(classes) - 1)
                previous = edge["target_class"]
                _integer(edge["multiplicity"], 1, 3)
                total += edge["multiplicity"]
            if total != sizes[color]:
                raise ValueError("local row total differs from its parent color population")
            atoms += len(edges)
    if atoms > CLASS_LOCAL_CAP:
        raise ValueError("class-local atom resource cap exceeded")
    for row in classes:
        for color, name in enumerate(("odd", "even")):
            for edge in row[name]:
                target = classes[edge["target_class"]]
                expected = list(row["parent_color_sizes"])
                expected[color] -= 1
                if (
                    target["frame_id"] != row["frame_id"]
                    or target["parent_color_sizes"] != expected
                ):
                    raise ValueError(
                        "a local deletion must preserve frame and lower exactly one color"
                    )
    return json.loads(canonical(classes))


def _operator_product(classes, source, first, second):
    result = {}
    for edge in classes[source][first]:
        for following in classes[edge["target_class"]][second]:
            target = following["target_class"]
            result[target] = (
                result.get(target, 0) + edge["multiplicity"] * following["multiplicity"]
            )
    return result


def _operator_checks(classes, profiles):
    rows = []
    fields = (
        "odd_odd_targets",
        "even_even_targets",
        "mixed_targets",
        "coefficient_cells",
        "odd_odd_pairs",
        "even_even_pairs",
        "mixed_pairs",
        "max_abs_residual",
    )
    totals = {name: 0 for name in fields}
    for row, profile in zip(classes, profiles, strict=True):
        source = row["class_id"]
        odd, even = row["parent_color_sizes"]
        oo = _operator_product(classes, source, "odd", "odd")
        ee = _operator_product(classes, source, "even", "even")
        oe = _operator_product(classes, source, "odd", "even")
        eo = _operator_product(classes, source, "even", "odd")
        expected_oo, expected_ee, expected_mixed = {}, {}, {}
        for atom in profile["transitions"]:
            target, rank, count = (
                atom["target_class"],
                atom["retained_color_sizes"],
                atom["multiplicity"],
            )
            if rank == [odd - 2, even]:
                expected_oo[target] = 2 * count
            if rank == [odd, even - 2]:
                expected_ee[target] = 2 * count
            if rank == [odd - 1, even - 1]:
                expected_mixed[target] = count
        if oo != expected_oo or ee != expected_ee:
            raise ValueError("same-color deletion words disagree with the factor-two subset count")
        if oe != eo or oe != expected_mixed:
            raise ValueError("mixed deletion orders disagree with each other or the subset count")
        pairs = [sum(oo.values()), sum(ee.values()), sum(oe.values())]
        if pairs != [odd * (odd - 1), even * (even - 1), odd * even]:
            raise ValueError("local two-deletion row masses are incorrect")
        counts = {
            "class_id": source,
            "odd_odd_targets": len(oo),
            "even_even_targets": len(ee),
            "mixed_targets": len(oe),
            "coefficient_cells": len(oo) + len(ee) + 2 * len(oe),
            "odd_odd_pairs": pairs[0],
            "even_even_pairs": pairs[1],
            "mixed_pairs": pairs[2],
            "max_abs_residual": 0,
        }
        rows.append(counts)
        for name in fields:
            totals[name] += counts[name]
    return {"verified": True, "rows": rows, "totals": totals}


def reconstruct_profiles(local_model):
    """Reconstruct all subset counts from local rows alone, by rank induction.

    No raw observations or full-profile oracle are received or consulted.
    This is structural and algebraic validation, not an authentication of the
    class names or a guarantee of realization in an observed-order domain.
    """
    classes = _validated_local(local_model)
    size = len(classes)
    dense = [None] * size
    profiles = [None] * size
    base_cells, recurrence_cells, atoms = 0, 0, 0
    order = sorted(range(size), key=lambda i: (sum(classes[i]["parent_color_sizes"]), i))
    for source in order:
        row = classes[source]
        odd, even = row["parent_color_sizes"]
        values = [0] * size
        for target, following in enumerate(classes):
            m, n = following["parent_color_sizes"]
            if row["frame_id"] != following["frame_id"] or m > odd or n > even:
                continue
            if m == odd and n == even:
                values[target] = int(source == target)
                base_cells += 1
                continue
            odd_sum, even_sum = None, None
            if odd > m:
                odd_sum = 0
                for edge in row["odd"]:
                    child = dense[edge["target_class"]]
                    if child is None:
                        raise ValueError("smaller-parent induction used an unprocessed class")
                    odd_sum += edge["multiplicity"] * child[target]
                if odd_sum < 0 or odd_sum % (odd - m):
                    raise ValueError("odd recurrence is not exactly nonnegative integer divisible")
                recurrence_cells += 1
            if even > n:
                even_sum = 0
                for edge in row["even"]:
                    child = dense[edge["target_class"]]
                    if child is None:
                        raise ValueError("smaller-parent induction used an unprocessed class")
                    even_sum += edge["multiplicity"] * child[target]
                if even_sum < 0 or even_sum % (even - n):
                    raise ValueError("even recurrence is not exactly nonnegative integer divisible")
                recurrence_cells += 1
            count = odd_sum // (odd - m) if odd_sum is not None else even_sum // (even - n)
            if odd_sum is not None and even_sum is not None and even_sum != (even - n) * count:
                raise ValueError("odd and even reconstruction recurrences disagree")
            _integer(count, 0, min(9, _choose(odd, m) * _choose(even, n)))
            values[target] = count
        totals = [[0] * 4 for _ in range(4)]
        transitions = []
        for target, count in enumerate(values):
            m, n = classes[target]["parent_color_sizes"]
            totals[m][n] += count
            if count:
                transitions.append(
                    {
                        "target_class": target,
                        "retained_color_sizes": [m, n],
                        "multiplicity": count,
                    }
                )
        if totals != [[_choose(odd, m) * _choose(even, n) for n in range(4)] for m in range(4)]:
            raise ValueError("reconstructed counts do not satisfy rankwise binomial normalization")
        if len(transitions) > 64:
            raise ValueError("one class profile exceeds its subset atom bound")
        atoms += len(transitions)
        if atoms > PROFILE_ATOM_CAP:
            raise ValueError("reconstructed profile atom resource cap exceeded")
        dense[source] = values
        profiles[source] = {
            "class_id": source,
            "parent_color_sizes": [odd, even],
            "transitions": transitions,
        }
    if any(row is None for row in profiles):
        raise ValueError("class induction did not fill the full domain")
    result = {
        "profiles": profiles,
        "certificate": {
            "target_cells": size * size,
            "base_cells": base_cells,
            "recurrence_cells": recurrence_cells,
            "normalization_cells": 16 * size,
            "max_abs_residual": 0,
        },
        "operator_checks": _operator_checks(classes, profiles),
    }
    canonical(result)
    return result


def _groups(vector):
    groups = []
    seen = set()
    for state_id, class_id in enumerate(vector):
        _integer(class_id, 0, CLASS_CAP - 1)
        if class_id not in seen:
            if class_id != len(groups):
                raise ValueError("initial labels are not first-occurrence canonical")
            seen.add(class_id)
            groups.append({"class_id": class_id, "members": []})
        groups[class_id]["members"].append(state_id)
    if not groups:
        raise ValueError("a partition must contain at least one state")
    return groups


def _partition_from_keys(keys):
    labels, groups, registry = [], [], {}
    for state_id, key in enumerate(keys):
        encoded = _key(key)
        class_id = registry.get(encoded)
        if class_id is None:
            class_id = len(groups)
            if class_id >= CLASS_CAP:
                raise ValueError("partition exceeds the declared class cap")
            registry[encoded] = class_id
            groups.append({"class_id": class_id, "key": key, "members": []})
        labels.append(class_id)
        groups[class_id]["members"].append(state_id)
    return {"state_classes": labels, "classes": groups}


def _measurable(rows, vector):
    if type(vector) is not list or len(vector) != len(rows):
        raise ValueError("partition has incompatible native dimensions")
    groups = _groups(vector)
    for group in groups:
        first = rows[group["members"][0]]
        for state_id in group["members"]:
            row = rows[state_id]
            if (
                row["frame_id"] != first["frame_id"]
                or row["parent_color_sizes"] != first["parent_color_sizes"]
            ):
                raise ValueError("partition does not preserve frame and color rank")
    return groups


def _validate_raw_rows(rows, mode):
    _native(rows)
    if type(rows) is not list or not 1 <= len(rows) <= STATE_CAP:
        raise ValueError("fine count row domain is outside its bound")
    names = ("odd", "even") if mode == "local" else ("transitions",)
    keys = ("state_id", "frame_id", "parent_color_sizes", *names)
    atoms, choices = 0, 0
    for state_id, row in enumerate(rows):
        _fields(row, keys)
        _integer(row["state_id"], state_id, state_id)
        _integer(row["frame_id"], 0, 1)
        rank = _colors(row["parent_color_sizes"])
        for color, name in enumerate(names):
            edges = row[name]
            if type(edges) is not list or len(edges) > (3 if mode == "local" else 64):
                raise ValueError("fine count row exceeds its atom bound")
            previous, total = -1, 0
            for edge in edges:
                _fields(edge, ("target_state", "multiplicity"))
                _integer(edge["target_state"], previous + 1, len(rows) - 1)
                _integer(edge["multiplicity"], 1, 3 if mode == "local" else 9)
                previous = edge["target_state"]
                total += edge["multiplicity"]
            if mode == "local" and total != rank[color]:
                raise ValueError("fine local row has the wrong color mass")
            atoms += len(edges)
            choices += total
    cap = LOCAL_CHOICE_CAP if mode == "local" else FINE_ATOM_CAP
    if atoms > cap or choices > cap:
        raise ValueError("fine count rows exceed the weighted resource bound")
    for row in rows:
        parent = row["parent_color_sizes"]
        totals = [[0] * 4 for _ in range(4)]
        full_rank = {}
        for color, name in enumerate(names):
            for edge in row[name]:
                target = rows[edge["target_state"]]
                child = target["parent_color_sizes"]
                if target["frame_id"] != row["frame_id"]:
                    raise ValueError("fine deletion changes frame")
                if mode == "local":
                    wanted = list(parent)
                    wanted[color] -= 1
                    if child != wanted:
                        raise ValueError("fine deletion must lower exactly its named color")
                else:
                    odd, even = child
                    maximum = _choose(parent[0], odd) * _choose(parent[1], even)
                    if not maximum or edge["multiplicity"] > maximum:
                        raise ValueError("full atom exceeds its retained-rank count")
                    totals[odd][even] += edge["multiplicity"]
                    if child == parent:
                        full_rank[edge["target_state"]] = edge["multiplicity"]
        if mode == "full":
            if full_rank != {row["state_id"]: 1}:
                raise ValueError("full-rank fine mass is not exactly the self delta")
            expected = [
                [_choose(parent[0], m) * _choose(parent[1], n) for n in range(4)] for m in range(4)
            ]
            if totals != expected:
                raise ValueError("full count row fails a binomial rank normalization")
    return json.loads(canonical(rows))


def _aggregate_local(rows, vector):
    groups = _measurable(rows, vector)
    result = []
    for row in rows:
        output = {
            "state_id": row["state_id"],
            "frame_id": row["frame_id"],
            "parent_color_sizes": list(row["parent_color_sizes"]),
        }
        for color, name in enumerate(("odd", "even")):
            counts = {}
            for edge in row[name]:
                target = vector[edge["target_state"]]
                counts[target] = counts.get(target, 0) + edge["multiplicity"]
            if sum(counts.values()) != row["parent_color_sizes"][color]:
                raise ValueError("aggregation changed a local color mass")
            for target, count in counts.items():
                _integer(count, 1, 3)
                child = rows[groups[target]["members"][0]]
                wanted = list(row["parent_color_sizes"])
                wanted[color] -= 1
                if child["frame_id"] != row["frame_id"] or child["parent_color_sizes"] != wanted:
                    raise ValueError("aggregate local target has inconsistent rank or frame")
            output[name] = [
                {"target_class": target, "multiplicity": counts[target]}
                for target in sorted(counts)
            ]
        result.append(output)
    return result


def _aggregate_full(rows, vector):
    groups = _measurable(rows, vector)
    result = []
    for row in rows:
        counts = {}
        for edge in row["transitions"]:
            target = vector[edge["target_state"]]
            counts[target] = counts.get(target, 0) + edge["multiplicity"]
        transitions, totals = [], [[0] * 4 for _ in range(4)]
        parent = row["parent_color_sizes"]
        for target in sorted(counts):
            child = rows[groups[target]["members"][0]]
            rank = child["parent_color_sizes"]
            if child["frame_id"] != row["frame_id"]:
                raise ValueError("aggregate full target changes frame")
            _integer(
                counts[target], 1, min(9, _choose(parent[0], rank[0]) * _choose(parent[1], rank[1]))
            )
            totals[rank[0]][rank[1]] += counts[target]
            transitions.append(
                {
                    "target_class": target,
                    "retained_color_sizes": list(rank),
                    "multiplicity": counts[target],
                }
            )
        if totals != [
            [_choose(parent[0], m) * _choose(parent[1], n) for n in range(4)] for m in range(4)
        ]:
            raise ValueError("aggregate profile fails rankwise normalization")
        result.append(
            {
                "state_id": row["state_id"],
                "parent_color_sizes": list(parent),
                "transitions": transitions,
            }
        )
    return result


def _signature(row, mode):
    if mode == "local":
        return tuple(
            tuple((edge["target_class"], edge["multiplicity"]) for edge in row[name])
            for name in ("odd", "even")
        )
    return tuple(
        (edge["target_class"], tuple(edge["retained_color_sizes"]), edge["multiplicity"])
        for edge in row["transitions"]
    )


def _difference(left, right, mode):
    names = ("odd", "even") if mode == "local" else ("transitions",)
    for name in names:
        lhs = {edge["target_class"]: edge for edge in left[name]}
        rhs = {edge["target_class"]: edge for edge in right[name]}
        for target in sorted(set(lhs) | set(rhs)):
            a = lhs[target]["multiplicity"] if target in lhs else 0
            b = rhs[target]["multiplicity"] if target in rhs else 0
            if a != b:
                result = {
                    "target_class": target,
                    "left_multiplicity": a,
                    "right_multiplicity": b,
                }
                if mode == "local":
                    result["color"] = name
                else:
                    result["retained_color_sizes"] = list(
                        (lhs[target] if target in lhs else rhs[target])["retained_color_sizes"]
                    )
                return result
    raise ValueError("different refinement signatures have no count witness")


def _refine(rows, initial, mode):
    _native(initial)
    groups = _measurable(rows, initial)
    vector = list(initial)
    bound = min(6, len(rows) - len(groups))
    rounds = []
    for round_index in range(bound + 1):
        groups = _measurable(rows, vector)
        aggregated = (
            _aggregate_local(rows, vector) if mode == "local" else _aggregate_full(rows, vector)
        )
        signatures = [_signature(row, mode) for row in aggregated]
        comparisons, unequal = 0, False
        for group in groups:
            left = group["members"][0]
            for right in group["members"][1:]:
                comparisons += 1
                if signatures[left] != signatures[right]:
                    unequal = True
        if comparisons != len(rows) - len(groups):
            raise ValueError("refinement skipped a nonrepresentative member")
        next_vector, registry = [], {}
        for state_id, signature in enumerate(signatures):
            key = (vector[state_id], signature)
            if key not in registry:
                if len(registry) >= CLASS_CAP:
                    raise ValueError("refinement exceeds the declared class cap")
                registry[key] = len(registry)
            next_vector.append(registry[key])
        next_groups = _groups(next_vector)
        stable = next_vector == vector
        if stable == unequal:
            raise ValueError("split decisions disagree with complete member comparisons")
        if not stable and len(next_groups) <= len(groups):
            raise ValueError("a strict refinement must increase the class count")
        separations = []
        for child in next_groups:
            right = child["members"][0]
            parent = vector[right]
            left = groups[parent]["members"][0]
            if left == right:
                continue
            if any(vector[sid] != parent for sid in child["members"]):
                raise ValueError("refinement merged inherited classes")
            separations.append(
                {
                    "parent_class_id": parent,
                    "child_class_id": child["class_id"],
                    "left_state": left,
                    "right_state": right,
                    **_difference(aggregated[left], aggregated[right], mode),
                }
            )
        if len(separations) != len(next_groups) - len(groups):
            raise ValueError("refinement lacks one canonical witness per new child")
        signature_atoms = sum(
            len(row["odd"]) + len(row["even"]) if mode == "local" else len(row["transitions"])
            for row in aggregated
        )
        rounds.append(
            {
                "round_index": round_index,
                "state_classes": list(vector),
                "classes": groups,
                "rows_sha256": _digest(aggregated),
                "signature_atoms": signature_atoms,
                "member_comparisons": comparisons,
                "stable": stable,
                "separations": separations,
            }
        )
        if stable:
            break
        if round_index == bound:
            raise ValueError("refinement exceeded the rank/finite strict-round bound")
        vector = next_vector
    if not rounds[-1]["stable"]:
        raise ValueError("no stable refinement certificate was constructed")
    trace = {
        "mode": mode,
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "state_classes": vector,
        "classes": groups,
        "counts": {
            "rounds": len(rounds),
            "signature_atoms": sum(row["signature_atoms"] for row in rounds),
            "member_comparisons": sum(row["member_comparisons"] for row in rounds),
            "separations": sum(len(row["separations"]) for row in rounds),
        },
    }
    return json.loads(canonical(trace))


def refine_local(local_problem):
    """Find the least local count-stable refinement of the supplied partition.

    Only validated fine state-target rows and initial labels are available.
    This does not establish full-profile integrality, order realization, or H.
    """
    _native(local_problem)
    _fields(local_problem, ("schema_version", "state_classes", "rows"))
    if local_problem["schema_version"] != "det8-qr05t-local-v1":
        raise ValueError("unknown local refinement schema")
    rows = _validate_raw_rows(local_problem["rows"], "local")
    return _refine(rows, local_problem["state_classes"], "local")


def _refine_full(rows, state_classes):
    """Independent full-count signature route, also used by algebraic controls."""
    _native(state_classes)
    validated = _validate_raw_rows(rows, "full")
    return _refine(validated, state_classes, "full")


def _fine_local(model, features, registry):
    rows, choices = [], 0
    for state, feature in zip(model["states"], features, strict=True):
        frame = model["frames"][state["frame_id"]]
        by_color = {"odd": {}, "even": {}}
        for vertex in frame["eligible"]:
            if vertex not in state["kept"]:
                continue
            kept = [value for value in state["kept"] if value != vertex]
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in registry:
                raise ValueError("raw domain lacks an induced single-deletion successor")
            target = registry[identity]
            color = "odd" if vertex % 2 else "even"
            by_color[color][target] = by_color[color].get(target, 0) + 1
            choices += 1
        if choices > LOCAL_CHOICE_CAP:
            raise ValueError("fine deleted-vertex choices exceed the resource bound")
        if any(count != 1 for counts in by_color.values() for count in counts.values()):
            raise ValueError("distinct raw deleted vertices unexpectedly share a labeled state")
        rows.append(
            {
                "state_id": state["state_id"],
                "frame_id": state["frame_id"],
                "parent_color_sizes": list(feature["color_sizes"]),
                **{
                    color: [
                        {"target_state": target, "multiplicity": count}
                        for target, count in sorted(by_color[color].items())
                    ]
                    for color in ("odd", "even")
                },
            }
        )
    return _validate_raw_rows(rows, "local")


def _fine_full(model, features, registry):
    """Enumerate raw subsets independently of the completed local refinement."""
    rows, fine, kernels = [], [], {}
    total = 0
    for state, feature in zip(model["states"], features, strict=True):
        frame = model["frames"][state["frame_id"]]
        eligible = [vertex for vertex in frame["eligible"] if vertex in state["kept"]]
        counts, polynomial_atoms = {}, []
        for mask in range(1 << len(eligible)):
            kept = sorted(
                frame["fixed"]
                + [vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit)]
            )
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in registry:
                raise ValueError("raw domain is missing an induced retained subset")
            target = registry[identity]
            counts[target] = counts.get(target, 0) + 1
            key = (tuple(feature["color_sizes"]), tuple(features[target]["color_sizes"]))
            if key not in kernels:
                kernels[key] = _kernel_polynomial(*key)
            polynomial_atoms.append({"target_state": target, "coefficients": kernels[key]})
        if any(count != 1 for count in counts.values()):
            raise ValueError("different retained labeled subsets have merged raw observations")
        total += len(counts)
        if total > FINE_ATOM_CAP:
            raise ValueError("fine raw subset resource cap exceeded")
        polynomial_atoms.sort(key=lambda edge: edge["target_state"])
        _normalized(polynomial_atoms)
        fine.append({"state_id": state["state_id"], "transitions": polynomial_atoms})
        rows.append(
            {
                "state_id": state["state_id"],
                "frame_id": state["frame_id"],
                "parent_color_sizes": list(feature["color_sizes"]),
                "transitions": [
                    {"target_state": target, "multiplicity": count}
                    for target, count in sorted(counts.items())
                ],
            }
        )
    return _validate_raw_rows(rows, "full"), fine


def _check_slices(local, full):
    for left, right in zip(local, full, strict=True):
        if left["state_id"] != right["state_id"] or left["frame_id"] != right["frame_id"]:
            raise ValueError("local and full domains disagree")
        for color, name in enumerate(("odd", "even")):
            wanted = list(left["parent_color_sizes"])
            wanted[color] -= 1
            expected = [
                dict(edge)
                for edge in right["transitions"]
                if full[edge["target_state"]]["parent_color_sizes"] == wanted
            ]
            if _key(expected) != _key(left[name]):
                raise ValueError("fine local counts differ from the corresponding full rank slice")


def _class_map(source, target):
    if len(source) != len(target):
        raise ValueError("partitions have different state domains")
    groups = _groups(source)
    _groups(target)
    result = []
    for group in groups:
        value = target[group["members"][0]]
        if any(target[state_id] != value for state_id in group["members"]):
            return None
        result.append(value)
    return result


def _constancy(aggregated, vector, mode):
    groups = _groups(vector)
    signatures = [_signature(row, mode) for row in aggregated]
    comparisons, closed = 0, True
    for group in groups:
        representative = group["members"][0]
        for member in group["members"][1:]:
            comparisons += 1
            if signatures[member] != signatures[representative]:
                closed = False
    if comparisons != len(vector) - len(groups):
        raise ValueError("terminal constancy omitted a member")
    return closed, comparisons


def _power_transitions(profile):
    parent = profile["parent_color_sizes"]
    transitions = []
    for atom in profile["transitions"]:
        table = _kernel_polynomial(parent, atom["retained_color_sizes"])
        coefficients = [[atom["multiplicity"] * value for value in row] for row in table]
        _table(coefficients)
        transitions.append({"target_class": atom["target_class"], "coefficients": coefficients})
    _normalized(transitions)
    return transitions


def _terminal(local, full, fine, vector):
    groups = _measurable(local, vector)
    aggregated_local = _aggregate_local(local, vector)
    direct = _aggregate_full(full, vector)
    local_closed, comparisons = _constancy(aggregated_local, vector, "local")
    full_closed, full_comparisons = _constancy(direct, vector, "full")
    if not local_closed or not full_closed or comparisons != full_comparisons:
        raise ValueError("terminal partition is not completely local/full stable")
    class_local = []
    for group in groups:
        representative = group["members"][0]
        row = aggregated_local[representative]
        class_local.append(
            {
                "class_id": group["class_id"],
                "representative_state": representative,
                "frame_id": row["frame_id"],
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "odd": [dict(edge) for edge in row["odd"]],
                "even": [dict(edge) for edge in row["even"]],
            }
        )
    # Only local class rows enter the constructor; full profiles are a separate oracle.
    reconstructed = reconstruct_profiles(
        {
            "schema_version": "det8-qr05s-local-v1",
            "classes": [
                {
                    key: row[key]
                    for key in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")
                }
                for row in class_local
            ],
        }
    )
    class_profiles = [
        {
            "class_id": row["class_id"],
            "representative_state": class_local[row["class_id"]]["representative_state"],
            "parent_color_sizes": list(row["parent_color_sizes"]),
            "transitions": row["transitions"],
        }
        for row in reconstructed["profiles"]
    ]
    reconstructed_states = []
    for state_id, class_id in enumerate(vector):
        row = class_profiles[class_id]
        reconstructed_states.append(
            {
                "state_id": state_id,
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "transitions": row["transitions"],
            }
        )
    if _key(reconstructed_states) != _key(direct):
        raise ValueError("local-only terminal reconstruction differs from raw subset profiles")
    pushed = _round_pushforwards(fine, vector)
    atoms = 0
    for profile, law in zip(direct, pushed, strict=True):
        if _key(_power_transitions(profile)) != _key(law["transitions"]):
            raise ValueError("terminal profile expansion differs from fine polynomial pushforward")
        atoms += len(profile["transitions"])
    quotient = []
    for profile in class_profiles:
        power = _power_transitions(profile)
        if _key(power) != _key(pushed[profile["representative_state"]]["transitions"]):
            raise ValueError("terminal quotient is not its representative fine pushforward")
        quotient.append(
            {
                "class_id": profile["class_id"],
                "representative_state": profile["representative_state"],
                "transitions": power,
            }
        )
    return {
        "local_rows": class_local,
        "class_profiles": class_profiles,
        "reconstruction": {
            "certificate": reconstructed["certificate"],
            "operator_checks": reconstructed["operator_checks"],
        },
        "closure": {
            "local_closed": local_closed,
            "full_closed": full_closed,
            "classes_checked": len(groups),
            "member_comparisons": comparisons,
        },
        "comparison": {
            "direct_profiles_sha256": _digest(direct),
            "reconstructed_profiles_sha256": _digest(reconstructed_states),
            "pushed_rows_sha256": _digest(pushed),
            "quotient_rows_sha256": _digest(quotient),
            "profile_cells": 16 * atoms,
            "power_cells": 16 * atoms,
            "max_abs_residual": 0,
        },
    }


def analyze(problem):
    """Construct both C refinements directly, then compare the terminal with H."""
    _native(problem)
    _fields(problem, ("schema_version", "family", "model"))
    if (
        problem["schema_version"] != "det8-qr05t-problem-v1"
        or problem["family"] != "qr05t_local_refinement"
    ):
        raise ValueError("unsupported investigation schema or family")
    model, features, registry = _observations(problem["model"])
    keys = [
        [
            _frame_key(model["frames"][state["frame_id"]]),
            feature["pair_graded"],
            feature["motif_count"],
        ]
        for state, feature in zip(model["states"], features, strict=True)
    ]
    c_partition = _partition_from_keys(keys)
    local = _fine_local(model, features, registry)
    local_trace = refine_local(
        {
            "schema_version": "det8-qr05t-local-v1",
            "state_classes": c_partition["state_classes"],
            "rows": local,
        }
    )
    # The independently enumerated full table cannot influence the local trace.
    full, fine = _fine_full(model, features, registry)
    _check_slices(local, full)
    full_trace = _refine_full(full, c_partition["state_classes"])
    # H is constructed only now, as a comparator, never as a split seed.
    h_partition = _partition_from_keys(
        [key + [feature["path_count"]] for key, feature in zip(keys, features, strict=True)]
    )
    vectors = [
        c_partition["state_classes"],
        local_trace["state_classes"],
        full_trace["state_classes"],
        h_partition["state_classes"],
    ]
    map_matrix = [[_class_map(left, right) for right in vectors] for left in vectors]
    relation = [[entry is not None for entry in row] for row in map_matrix]
    equal_terminals = relation[1][2] and relation[2][1]
    if not equal_terminals:
        raise ValueError("local and full refinements have different terminal memberships")
    all_C, all_measurable = True, True
    for trace in (local_trace, full_trace):
        for round_row in trace["rounds"]:
            if _class_map(round_row["state_classes"], vectors[0]) is None:
                all_C = False
            _measurable(local, round_row["state_classes"])
        _measurable(local, trace["state_classes"])
    if not all_C:
        raise ValueError("a refinement round failed to preserve C")
    aligned = []
    for index in range(max(len(local_trace["rounds"]), len(full_trace["rounds"]))):
        left = local_trace["rounds"][min(index, len(local_trace["rounds"]) - 1)]["state_classes"]
        right = full_trace["rounds"][min(index, len(full_trace["rounds"]) - 1)]["state_classes"]
        aligned.append(_class_map(right, left) is not None)
    if not all(aligned):
        raise ValueError("an aligned full partition fails to refine the local partition")
    h_rows = _aggregate_local(local, vectors[3])
    h_closed, _ = _constancy(h_rows, vectors[3], "local")
    if map_matrix[3][0] is None:
        raise ValueError("H is not a refinement of the inherited C")
    if h_closed and map_matrix[3][1] is None:
        raise ValueError("a checked closed H does not refine the terminal C refinement")
    terminal = _terminal(local, full, fine, vectors[1])
    choices = sum(
        edge["multiplicity"] for row in local for color in ("odd", "even") for edge in row[color]
    )
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partitions": {"C": c_partition, "H": h_partition},
        "fine_kernel": {
            "sha256": _digest(fine),
            "atoms": sum(len(row["transitions"]) for row in fine),
        },
        "fine_deletions": {
            "sha256": _digest(local),
            "atoms": sum(len(row["odd"]) + len(row["even"]) for row in local),
            "choices": choices,
        },
        "local_refinement": local_trace,
        "full_refinement": full_trace,
        "comparison": {
            "names": ["C", "L", "F", "H"],
            "refinement": relation,
            "maps": {
                "L_to_C": map_matrix[1][0],
                "F_to_C": map_matrix[2][0],
                "L_to_F": map_matrix[1][2],
                "F_to_L": map_matrix[2][1],
                "L_to_H": map_matrix[1][3],
                "H_to_L": map_matrix[3][1],
            },
            "same_terminal_memberships": equal_terminals,
            "same_memberships_as_H": relation[1][3] and relation[3][1],
            "H_local_closed": h_closed,
            "aligned_full_refines_local": aligned,
        },
        "terminal": terminal,
        "minimality": {
            "verified": True,
            "initial_partition": "C",
            "terminal_partition": "L",
            "all_rounds_refine_C": all_C,
            "all_rounds_rank_frame_measurable": all_measurable,
            "local_full_terminals_equal": equal_terminals,
            "H_used_in_construction": False,
            "strict_round_bound": min(6, len(local) - len(c_partition["classes"])),
            "relative_to_C": True,
            "arbitrary_partitions_enumerated": False,
        },
        "counts": {
            "states": len(features),
            "C_classes": len(c_partition["classes"]),
            "H_classes": len(h_partition["classes"]),
            "L_classes": len(local_trace["classes"]),
            "F_classes": len(full_trace["classes"]),
            "fine_atoms": sum(len(row["transitions"]) for row in fine),
            "fine_local_choices": choices,
            "local_strict_rounds": local_trace["strict_rounds"],
            "full_strict_rounds": full_trace["strict_rounds"],
            "terminal_local_atoms": sum(
                len(row["odd"]) + len(row["even"]) for row in terminal["local_rows"]
            ),
            "terminal_profile_atoms": sum(
                len(row["transitions"]) for row in terminal["class_profiles"]
            ),
        },
    }
    return json.loads(canonical(result))
