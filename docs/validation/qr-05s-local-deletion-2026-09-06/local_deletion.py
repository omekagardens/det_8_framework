"""QR-05S observed local deletions and local-only rank reconstruction.

Local utility lineage is copied statically from this primary's QR-05R.
Features and single-deletion counts use only the supplied observations.
The local-only constructor receives no observations, full subset counts,
fine kernels or prior outcomes. Full subsets are enumerated separately
after local reconstruction for the independent comparison within this route.
No external artifact or other executor is imported or read at runtime.
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

    Returns (model, features, registry, partition); it never reads a prior artifact.
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
    class_ids, vector, groups = {}, [], []
    for state, feature in zip(states, features, strict=True):
        key = [
            _frame_key(frames[state["frame_id"]]),
            feature["pair_graded"],
            feature["motif_count"],
            feature["path_count"],
        ]
        identity = _key(key)
        class_id = class_ids.get(identity)
        if class_id is None:
            class_id = len(groups)
            class_ids[identity] = class_id
            groups.append({"class_id": class_id, "key": key, "members": []})
        groups[class_id]["members"].append(state["state_id"])
        vector.append(class_id)
    if len(groups) > CLASS_CAP:
        raise ValueError("H class resource cap exceeded")
    fine_atoms = sum(2 ** sum(feature["color_sizes"]) for feature in features)
    if fine_atoms > FINE_ATOM_CAP:
        raise ValueError("fine subset atom resource cap exceeded")
    return model, features, identities, {"state_classes": vector, "classes": groups}


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


def _local_rows(model, features, registry, partition):
    classes = partition["classes"]
    for group in classes:
        first = model["states"][group["members"][0]]
        rank = features[group["members"][0]]["color_sizes"]
        for state_id in group["members"]:
            feature, state = features[state_id], model["states"][state_id]
            recovered = [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]]
            if (
                recovered != feature["color_sizes"]
                or recovered != rank
                or state["frame_id"] != first["frame_id"]
            ):
                raise ValueError("H fails to fix raw parent color ranks or frame")
    rows, choices = [], 0
    for state, feature in zip(model["states"], features, strict=True):
        frame = model["frames"][state["frame_id"]]
        counts = {"odd": {}, "even": {}}
        for vertex in frame["eligible"]:
            if vertex not in state["kept"]:
                continue
            kept = [v for v in state["kept"] if v != vertex]
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in registry:
                raise ValueError("missing single-deletion successor in the supplied domain")
            target_state = registry[identity]
            target = partition["state_classes"][target_state]
            name = "odd" if vertex % 2 else "even"
            expected = list(feature["color_sizes"])
            expected[0 if vertex % 2 else 1] -= 1
            if features[target_state]["color_sizes"] != expected:
                raise ValueError("single-deletion rank changed by an incorrect amount")
            counts[name][target] = counts[name].get(target, 0) + 1
            choices += 1
        if choices > LOCAL_CHOICE_CAP:
            raise ValueError("fine single-deletion choice cap exceeded")
        row = {
            "state_id": state["state_id"],
            "frame_id": state["frame_id"],
            "parent_color_sizes": list(feature["color_sizes"]),
            "odd": [
                {"target_class": h, "multiplicity": counts["odd"][h]} for h in sorted(counts["odd"])
            ],
            "even": [
                {"target_class": h, "multiplicity": counts["even"][h]}
                for h in sorted(counts["even"])
            ],
        }
        if [sum(edge["multiplicity"] for edge in row[name]) for name in ("odd", "even")] != feature[
            "color_sizes"
        ]:
            raise ValueError("local rows lost a deleted-vertex multiplicity")
        rows.append(row)
    return rows, choices


def _validated_local_fibers(local_rows, partition):
    _native(local_rows)
    _native(partition)
    _fields(partition, ("state_classes", "classes"))
    if type(local_rows) is not list or not 1 <= len(local_rows) <= STATE_CAP:
        raise ValueError("invalid local state domain")
    groups, vector = partition["classes"], partition["state_classes"]
    if (
        type(groups) is not list
        or not 1 <= len(groups) <= CLASS_CAP
        or type(vector) is not list
        or len(vector) != len(local_rows)
    ):
        raise ValueError("local partition has incompatible dimensions")
    seen = []
    for class_id, group in enumerate(groups):
        _fields(group, ("class_id", "key", "members"))
        _integer(group["class_id"], class_id, class_id)
        if type(group["members"]) is not list or not group["members"]:
            raise ValueError("local partition contains an empty class")
        previous = -1
        for state_id in group["members"]:
            _integer(state_id, previous + 1, len(local_rows) - 1)
            _integer(vector[state_id], class_id, class_id)
            previous = state_id
            seen.append(state_id)
        if class_id and groups[class_id - 1]["members"][0] >= group["members"][0]:
            raise ValueError("local classes are not in first-occurrence order")
    if sorted(seen) != list(range(len(local_rows))):
        raise ValueError("local partition does not cover each state once")
    for state_id, row in enumerate(local_rows):
        _fields(row, ("state_id", "frame_id", "parent_color_sizes", "odd", "even"))
        _integer(row["state_id"], state_id, state_id)
        _integer(row["frame_id"], 0, 1)
        parent = _colors(row["parent_color_sizes"])
        representative = local_rows[groups[vector[state_id]]["members"][0]]
        if (
            row["frame_id"] != representative["frame_id"]
            or row["parent_color_sizes"] != representative["parent_color_sizes"]
        ):
            raise ValueError("local fiber fails the color/frame measurability premise")
        for color, name in enumerate(("odd", "even")):
            edges = row[name]
            if type(edges) is not list or len(edges) > 3:
                raise ValueError("local color row has too many atoms")
            previous, total = -1, 0
            for edge in edges:
                _fields(edge, ("target_class", "multiplicity"))
                _integer(edge["target_class"], previous + 1, len(groups) - 1)
                _integer(edge["multiplicity"], 1, 3)
                previous = edge["target_class"]
                target = local_rows[groups[previous]["members"][0]]
                expected = list(parent)
                expected[color] -= 1
                if (
                    target["frame_id"] != row["frame_id"]
                    or target["parent_color_sizes"] != expected
                ):
                    raise ValueError("local target has inconsistent frame or color rank")
                total += edge["multiplicity"]
            if total != parent[color]:
                raise ValueError("local color row has the wrong vertex total")


def closure_from_local(local_rows, partition):
    _validated_local_fibers(local_rows, partition)
    maps = [
        {
            name: {edge["target_class"]: edge["multiplicity"] for edge in row[name]}
            for name in ("odd", "even")
        }
        for row in local_rows
    ]
    witness, comparisons = None, 0
    for group in partition["classes"]:
        left = group["members"][0]
        for right in group["members"][1:]:
            comparisons += 1
            for name in ("odd", "even"):
                lhs, rhs = maps[left][name], maps[right][name]
                differences = [
                    target
                    for target in sorted(set(lhs) | set(rhs))
                    if lhs.get(target, 0) != rhs.get(target, 0)
                ]
                if differences and witness is None:
                    target = differences[0]
                    witness = {
                        "class_id": group["class_id"],
                        "left_state": left,
                        "right_state": right,
                        "color": name,
                        "target_class": target,
                        "left_multiplicity": lhs.get(target, 0),
                        "right_multiplicity": rhs.get(target, 0),
                    }
    if comparisons != len(local_rows) - len(partition["classes"]):
        raise ValueError("local closure skipped nonrepresentative members")
    return {
        "closed": witness is None,
        "classes_checked": len(partition["classes"]),
        "member_comparisons": comparisons,
        "witness": witness,
    }


def _closure(partition, local_rows):
    closure = closure_from_local(local_rows, partition)
    if not closure["closed"]:
        return closure, [], None
    local_classes = []
    for group in partition["classes"]:
        rep = group["members"][0]
        row = local_rows[rep]
        local_classes.append(
            {
                "class_id": group["class_id"],
                "representative_state": rep,
                "frame_id": row["frame_id"],
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "odd": [dict(edge) for edge in row["odd"]],
                "even": [dict(edge) for edge in row["even"]],
            }
        )
    local_model = {
        "schema_version": "det8-qr05s-local-v1",
        "classes": [
            {key: row[key] for key in ("class_id", "frame_id", "parent_color_sizes", "odd", "even")}
            for row in local_classes
        ],
    }
    reconstructed = reconstruct_profiles(local_model)
    profiles = []
    for row in reconstructed["profiles"]:
        profiles.append(
            {
                "class_id": row["class_id"],
                "representative_state": local_classes[row["class_id"]]["representative_state"],
                "parent_color_sizes": row["parent_color_sizes"],
                "transitions": row["transitions"],
            }
        )
    return (
        closure,
        local_classes,
        {
            "class_profiles": profiles,
            "certificate": reconstructed["certificate"],
            "operator_checks": reconstructed["operator_checks"],
        },
    )


def _local_closure(partition, local_rows):
    return _closure(partition, local_rows)


def _direct_subsets(model, features, registry, partition):
    """Independent full subset census after the local-only calculation."""
    fine, profiles, kernel_cache = [], [], {}
    atoms = 0
    for state, feature in zip(model["states"], features, strict=True):
        frame = model["frames"][state["frame_id"]]
        present = [v for v in frame["eligible"] if v in state["kept"]]
        transitions, counts = [], {}
        for mask in range(1 << len(present)):
            kept = sorted(
                frame["fixed"] + [v for bit, v in enumerate(present) if mask & (1 << bit)]
            )
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in registry:
                raise ValueError("full subset audit found a missing induced successor")
            target_state = registry[identity]
            child = features[target_state]
            key = (tuple(feature["color_sizes"]), tuple(child["color_sizes"]))
            if key not in kernel_cache:
                kernel_cache[key] = _kernel_polynomial(*key)
            transitions.append({"target_state": target_state, "coefficients": kernel_cache[key]})
            target = partition["state_classes"][target_state]
            counts[target] = counts.get(target, 0) + 1
        transitions.sort(key=lambda edge: edge["target_state"])
        _normalized(transitions)
        fine.append({"state_id": state["state_id"], "transitions": transitions})
        atoms += len(transitions)
        if atoms > FINE_ATOM_CAP:
            raise ValueError("full subset atom resource cap exceeded")
        profile = []
        totals = [[0] * 4 for _ in range(4)]
        parent_odd, parent_even = feature["color_sizes"]
        for target in sorted(counts):
            rank = features[partition["classes"][target]["members"][0]]["color_sizes"]
            odd, even = rank
            count = counts[target]
            _integer(count, 1, min(9, _choose(parent_odd, odd) * _choose(parent_even, even)))
            totals[odd][even] += count
            profile.append(
                {
                    "target_class": target,
                    "retained_color_sizes": list(rank),
                    "multiplicity": count,
                }
            )
        if totals != [
            [_choose(parent_odd, odd) * _choose(parent_even, even) for even in range(4)]
            for odd in range(4)
        ]:
            raise ValueError("direct full profile lost rankwise normalization")
        profiles.append(
            {
                "state_id": state["state_id"],
                "parent_color_sizes": list(feature["color_sizes"]),
                "transitions": profile,
            }
        )
    return fine, profiles


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


def _comparison(fine, direct, partition, local_closure, reconstruction):
    full_closed = True
    for group in partition["classes"]:
        representative = direct[group["members"][0]]
        for member in group["members"][1:]:
            same = (
                direct[member]["parent_color_sizes"] == representative["parent_color_sizes"]
                and direct[member]["transitions"] == representative["transitions"]
            )
            if not same:
                full_closed = False
    if full_closed != local_closure["closed"]:
        raise ValueError("local/full constancy equivalence failed under the checked premises")
    pushed = _round_pushforwards(fine, partition["state_classes"])
    profile_atoms = 0
    for profile, row in zip(direct, pushed, strict=True):
        if _power_transitions(profile) != row["transitions"]:
            raise ValueError("direct profile expansion differs from the complete fine law")
        profile_atoms += len(profile["transitions"])
    reconstructed_rows, quotient = None, None
    if local_closure["closed"]:
        class_profiles = reconstruction["class_profiles"]
        reconstructed_rows = []
        for state_id, class_id in enumerate(partition["state_classes"]):
            profile = class_profiles[class_id]
            reconstructed_rows.append(
                {
                    "state_id": state_id,
                    "parent_color_sizes": profile["parent_color_sizes"],
                    "transitions": profile["transitions"],
                }
            )
        if _key(reconstructed_rows) != _key(direct):
            raise ValueError("local-only reconstruction differs from full raw subset profiles")
        quotient = []
        for row in class_profiles:
            transitions = _power_transitions(row)
            if transitions != pushed[row["representative_state"]]["transitions"]:
                raise ValueError("reconstructed class power row differs from its representative")
            quotient.append(
                {
                    "class_id": row["class_id"],
                    "representative_state": row["representative_state"],
                    "transitions": transitions,
                }
            )
    elif reconstruction is not None:
        raise ValueError("failed local closure exposed a reconstruction")
    return {
        "direct_profiles_sha256": _digest(direct),
        "reconstructed_profiles_sha256": _digest(reconstructed_rows)
        if reconstructed_rows is not None
        else None,
        "full_profile_closed": full_closed,
        "local_full_equivalent": full_closed == local_closure["closed"],
        "fine_kernel_sha256": _digest(fine),
        "pushed_rows_sha256": _digest(pushed),
        "quotient_rows_sha256": _digest(quotient) if quotient is not None else None,
        "profile_cells": 16 * profile_atoms if local_closure["closed"] else 0,
        "power_cells": 16 * profile_atoms,
        "max_abs_residual": 0,
    }


def analyze(problem):
    """Construct local evidence, then audit its independently enumerated full law."""
    _native(problem)
    _fields(problem, ("schema_version", "family", "model"))
    if (
        problem["schema_version"] != "det8-qr05s-problem-v1"
        or problem["family"] != "qr05s_local_deletion"
    ):
        raise ValueError("unsupported fixed investigation schema or family")
    model, features, registry, partition = _observations(problem["model"])
    local_rows, choices = _local_rows(model, features, registry, partition)
    closure, local_classes, reconstruction = _closure(partition, local_rows)
    # This direct census is not an input to the already-completed constructor.
    fine, direct = _direct_subsets(model, features, registry, partition)
    comparison = _comparison(fine, direct, partition, closure, reconstruction)
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partition": partition,
        "local_rows": local_rows,
        "local_closure": closure,
        "local_classes": local_classes,
        "reconstruction": reconstruction,
        "comparison": comparison,
        "counts": {
            "states": len(features),
            "classes": len(partition["classes"]),
            "fine_atoms": sum(len(row["transitions"]) for row in fine),
            "fine_local_choices": choices,
            "local_atoms": sum(len(row["odd"]) + len(row["even"]) for row in local_rows),
            "class_local_atoms": sum(len(row["odd"]) + len(row["even"]) for row in local_classes),
            "direct_profile_atoms": sum(len(row["transitions"]) for row in direct),
            "class_profile_atoms": sum(
                len(row["transitions"]) for row in reconstruction["class_profiles"]
            )
            if reconstruction is not None
            else 0,
        },
    }
    canonical(result)
    return result
