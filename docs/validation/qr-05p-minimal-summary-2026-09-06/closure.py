"""QR-05P finite observation model, closed refinement and summary consumer.

This primary route reconstructs observed chain subsets, ordered support pairs,
eligible induced motifs and binomial transition polynomials. Local utility
lineage is carried from the primary QR-05O source, without importing it.
Only the explicit model argument is consumed; this module performs no I/O.
"""

import hashlib
import json
import re
from fractions import Fraction
from itertools import combinations, product
from math import comb

BIT_LIMIT = 4096
STATE_CAP = 2470
FINE_ATOM_CAP = 99180
WORKING_CAP = 512 * 1024 * 1024
FRAMES = [
    {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
    {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
]
QUESTIONS = (
    "chain_counts",
    "motif_count",
    "path_count",
    "counts_motif_path",
    "named_relation_1_7",
)
GRID = tuple(product((Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(1)), repeat=2))
RATES = GRID + (
    (Fraction(1, 2), Fraction(1, 2)),
    (Fraction(2, 5), Fraction(3, 7)),
    (Fraction(1, 5), Fraction(4, 5)),
    (Fraction(1, 2), Fraction(1, 3)),
    (Fraction(0), Fraction(2, 5)),
    (Fraction(3, 7), Fraction(1)),
)


def _native(value):
    """Reject subclass/container coercion and oversized exact components."""
    if value is None or type(value) in (str, bool):
        return
    if type(value) is int:
        if value.bit_length() > BIT_LIMIT:
            raise ValueError("integer exceeds the exact arithmetic bound")
        return
    if type(value) is list:
        for item in value:
            _native(item)
        return
    if type(value) is dict and all(type(key) is str for key in value):
        for item in value.values():
            _native(item)
        return
    raise ValueError("expected native exact JSON")


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


def evaluate(table, rates):
    """Exact polynomial evaluation; public parsers validate its inputs."""
    x, y = rates
    result = Fraction(0)
    for row in reversed(table):
        inner = Fraction(0)
        for coefficient in reversed(row):
            inner = inner * y + coefficient
        result = result * x + inner
    if max(result.numerator.bit_length(), result.denominator.bit_length()) > BIT_LIMIT:
        raise ValueError("evaluated rational exceeds the arithmetic bound")
    return result


def reconstruct(model):
    """Validate the explicit raw domain and rebuild all observation-derived data.

    Returns (features, fine_rows, partitions); it never reads a prior artifact.
    Missing induced successors are rejected, rather than supplied by a source
    generator or guessed from feature identities.
    """
    _native(model)
    _fields(model, ("frames", "states"))
    if canonical(model["frames"]) != canonical(FRAMES):
        raise ValueError("model frames differ from the declared marks")
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
    fine_rows, atoms, polynomial_cache = [], 0, {}
    for state, feature in zip(states, features, strict=True):
        frame = frames[state["frame_id"]]
        present = [vertex for vertex in frame["eligible"] if vertex in state["kept"]]
        transitions = []
        for mask in range(1 << len(present)):
            kept = sorted(
                frame["fixed"] + [vertex for bit, vertex in enumerate(present) if mask & (1 << bit)]
            )
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in identities:
                raise ValueError("observation domain is missing an induced successor")
            target = identities[identity]
            sizes = (tuple(feature["color_sizes"]), tuple(features[target]["color_sizes"]))
            if sizes not in polynomial_cache:
                polynomial_cache[sizes] = _kernel_polynomial(*sizes)
            transitions.append({"target_state": target, "coefficients": polynomial_cache[sizes]})
        transitions.sort(key=lambda atom: atom["target_state"])
        _normalized(transitions)
        fine_rows.append({"state_id": state["state_id"], "transitions": transitions})
        atoms += len(transitions)
        if atoms > FINE_ATOM_CAP:
            raise ValueError("fine transition atom resource cap exceeded")
    partitions = {}
    for name in ("C", "H"):
        ids, vector, groups = {}, [], []
        for state, feature in zip(states, features, strict=True):
            key = [
                _frame_key(frames[state["frame_id"]]),
                feature["pair_graded"],
                feature["motif_count"],
            ]
            if name == "H":
                key.append(feature["path_count"])
            identity = _key(key)
            class_id = ids.get(identity)
            if class_id is None:
                class_id = len(groups)
                ids[identity] = class_id
                groups.append({"class_id": class_id, "key": key, "members": []})
            groups[class_id]["members"].append(state["state_id"])
            vector.append(class_id)
        partitions[name] = {"state_classes": vector, "classes": groups}
    return features, fine_rows, partitions


def _audit_fine(model, fine_rows):
    evaluations, corners, cache = 0, 0, {}
    for state, row in zip(model["states"], fine_rows, strict=True):
        _normalized(row["transitions"])
        frame = model["frames"][state["frame_id"]]
        for rates in RATES:
            probabilities = [
                _evaluated(atom["coefficients"], rates, cache) for atom in row["transitions"]
            ]
            if min(probabilities) < 0 or sum(probabilities) != 1:
                raise ValueError("fine row is not a probability law at an audit rate")
            evaluations += len(probabilities)
        for rates in (
            (Fraction(0), Fraction(0)),
            (Fraction(0), Fraction(1)),
            (Fraction(1), Fraction(0)),
            (Fraction(1), Fraction(1)),
        ):
            expected_kept = sorted(
                frame["fixed"]
                + [
                    vertex
                    for vertex in state["kept"]
                    if vertex in frame["eligible"] and rates[0 if vertex % 2 else 1] == 1
                ]
            )
            for atom in row["transitions"]:
                expected = int(model["states"][atom["target_state"]]["kept"] == expected_kept)
                if _evaluated(atom["coefficients"], rates, cache) != expected:
                    raise ValueError("fine corner is not the deterministic marked restriction")
            corners += 1
    atoms = sum(len(row["transitions"]) for row in fine_rows)
    return {
        "sha256": _digest(fine_rows),
        "transition_atoms": atoms,
        "coefficient_cells": 16 * atoms,
        "normalization_rows": len(fine_rows),
        "deterministic_corner_rows": corners,
        "rate_points": len(RATES),
        "evaluated_atoms": evaluations,
    }


def _groups(vector):
    if type(vector) is not list or not vector:
        raise ValueError("partition vector must be a nonempty native list")
    groups = []
    for state_id, class_id in enumerate(vector):
        _integer(class_id, 0, len(groups))
        if class_id == len(groups):
            groups.append({"class_id": class_id, "members": []})
        groups[class_id]["members"].append(state_id)
    return groups


def _validate_fine(fine_rows):
    _native(fine_rows)
    if type(fine_rows) is not list or not 1 <= len(fine_rows) <= STATE_CAP:
        raise ValueError("fine row count outside the synthetic/helper bound")
    atoms = 0
    for state_id, row in enumerate(fine_rows):
        _fields(row, ("state_id", "transitions"))
        _integer(row["state_id"], state_id, state_id)
        if type(row["transitions"]) is not list or not row["transitions"]:
            raise ValueError("fine row must contain structural transition atoms")
        previous = -1
        for atom in row["transitions"]:
            _fields(atom, ("target_state", "coefficients"))
            _integer(atom["target_state"], previous + 1, len(fine_rows) - 1)
            previous = atom["target_state"]
            _table(atom["coefficients"])
        _normalized(row["transitions"])
        atoms += len(row["transitions"])
    if atoms > FINE_ATOM_CAP:
        raise ValueError("fine transition atom resource cap exceeded")


def _next_round(current, rows):
    identities, following, groups = {}, [], []
    for state_id, row in enumerate(rows):
        identity = _key([current[state_id], row["transitions"]])
        class_id = identities.get(identity)
        if class_id is None:
            class_id = len(groups)
            identities[identity] = class_id
            groups.append({"class_id": class_id, "members": []})
        following.append(class_id)
        groups[class_id]["members"].append(state_id)
    if not _class_vector_refines(following, current):
        raise ValueError("a refinement step merged an old distinction")
    return following, groups


def _separations(current, groups, rows, following, next_groups):
    maps = [
        {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]} for row in rows
    ]
    zero, witnesses = [[0] * 4 for _ in range(4)], []
    for child in next_groups:
        right_state = child["members"][0]
        parent = current[right_state]
        left_state = groups[parent]["members"][0]
        if following[left_state] == child["class_id"]:
            continue
        if any(current[member] != parent for member in child["members"]):
            raise ValueError("refinement child crosses parent classes")
        left, right = maps[left_state], maps[right_state]
        target = next(
            (t for t in sorted(set(left) | set(right)) if left.get(t, zero) != right.get(t, zero)),
            None,
        )
        if target is None:
            raise ValueError("strict child has no current-row separating polynomial")
        left_table, right_table = left.get(target, zero), right.get(target, zero)
        rates = next(
            (
                rates
                for rates in GRID
                if evaluate(left_table, rates) != evaluate(right_table, rates)
            ),
            None,
        )
        if rates is None:
            raise ValueError("bounded polynomial difference vanished on the unisolvent grid")
        witnesses.append(
            {
                "parent_class_id": parent,
                "child_class_id": child["class_id"],
                "left_state": left_state,
                "right_state": right_state,
                "target_class": target,
                "left_coefficients": left_table,
                "right_coefficients": right_table,
                "first_distinguishing_rates": [str(value) for value in rates],
            }
        )
    if len(witnesses) != len(next_groups) - len(groups):
        raise ValueError("strict splits do not match canonical witnesses")
    return witnesses


def refine(fine_rows, initial):
    """Synchronous exact-coefficient refinement for bounded native fine rows.

    This generic helper assumes a polynomial Markov law and checks native
    structure and coefficient normalization. It does not prove positivity
    on a continuum or require the thinning semigroup identity of the retained
    model. Its synthetic uses do not expand the gate's certified domain.
    """
    _validate_fine(fine_rows)
    groups = _groups(initial)
    if len(initial) != len(fine_rows):
        raise ValueError("partition and fine-law domains differ")
    current, rounds, strict, initial_count = list(initial), [], 0, len(groups)
    retained_size = 0
    while True:
        rows = _round_pushforwards(fine_rows, current)
        following, next_groups = _next_round(current, rows)
        stable = following == current
        if stable and next_groups != groups:
            raise ValueError("stable vector has inconsistent groups")
        if not stable and len(next_groups) <= len(groups):
            raise ValueError("a nonstable round did not strictly split")
        witnesses = [] if stable else _separations(current, groups, rows, following, next_groups)
        item = {
            "round_index": len(rounds),
            "state_classes": current,
            "classes": groups,
            "pushed_rows_sha256": _digest(rows),
            "pushed_atoms": sum(len(row["transitions"]) for row in rows),
            "stable": stable,
            "separations": witnesses,
        }
        retained_size += len(canonical(item))
        if retained_size > WORKING_CAP:
            raise ValueError("refinement certificate exceeds the working-output cap")
        rounds.append(item)
        if stable:
            break
        strict += 1
        if strict > len(fine_rows) - initial_count:
            raise ValueError("refinement violated its finite strict-round bound")
        current, groups = following, next_groups
    return rounds


def _class_map(finer, coarser):
    if not _class_vector_refines(finer, coarser):
        return None
    result = [None] * (max(finer) + 1)
    for left, right in zip(finer, coarser, strict=True):
        result[left] = right
    return result


def _refinement(fine_rows, partitions):
    rounds = refine(fine_rows, partitions["C"]["state_classes"])
    terminal = rounds[-1]
    vector, groups = terminal["state_classes"], terminal["classes"]
    rows = _round_pushforwards(fine_rows, vector)
    quotient = []
    for group in groups:
        representative = group["members"][0]
        if any(
            rows[member]["transitions"] != rows[representative]["transitions"]
            for member in group["members"]
        ):
            raise ValueError("terminal refinement is not strongly closed")
        quotient.append(
            {
                "class_id": group["class_id"],
                "representative_state": representative,
                "transitions": rows[representative]["transitions"],
            }
        )
    semigroup = _semigroup(quotient)
    names = ["C", "R", "H"]
    vectors = [partitions["C"]["state_classes"], vector, partitions["H"]["state_classes"]]
    comparisons = [[_class_vector_refines(left, right) for right in vectors] for left in vectors]
    if not comparisons[1][0]:
        raise ValueError("terminal partition does not refine the required C")
    atoms = sum(item["pushed_atoms"] for item in rounds)
    return {
        "initial_partition": "C",
        "rounds": rounds,
        "strict_rounds": len(rounds) - 1,
        "final_round": len(rounds) - 1,
        "state_classes": vector,
        "classes": groups,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "comparison": {
            "names": names,
            "refinement": comparisons,
            "same_memberships_as_H": comparisons[1][2] and comparisons[2][1],
            "R_to_C": _class_map(vector, vectors[0]),
            "R_to_H": _class_map(vector, vectors[2]),
            "H_to_R": _class_map(vectors[2], vector),
        },
        "counts": {
            "rounds": len(rounds),
            "strict_rounds": len(rounds) - 1,
            "classes": len(groups),
            "round_transition_atoms": atoms,
            "round_coefficient_cells": 16 * atoms,
            "separation_witnesses": sum(len(item["separations"]) for item in rounds),
            "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
            "semigroup_intermediate_paths": semigroup["totals"]["intermediate_paths"],
            "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
        },
    }


def _evaluated(table, rates, cache):
    identity = (tuple(tuple(row) for row in table), rates)
    if identity not in cache:
        cache[identity] = evaluate(table, rates)
    return cache[identity]


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


def _sparse_table(table):
    return [(4 * i + j, c) for i, row in enumerate(table) for j, c in enumerate(row) if c]


def _semigroup(quotient):
    """Verify all four-variable coefficients, including every zero residual."""
    rows = []
    totals = {
        "transition_pairs": 0,
        "intermediate_paths": 0,
        "coefficient_cells": 0,
        "max_abs_residual": 0,
    }
    sparse = {
        (row["class_id"], atom["target_class"]): _sparse_table(atom["coefficients"])
        for row in quotient
        for atom in row["transitions"]
    }
    for row in quotient:
        start = row["class_id"]
        two_steps, paths = {}, 0
        for first in row["transitions"]:
            middle = first["target_class"]
            for second in quotient[middle]["transitions"]:
                paths += 1
                final = second["target_class"]
                table = two_steps.setdefault(final, [0] * 256)
                for ij, left in sparse[start, middle]:
                    for ab, right in sparse[middle, final]:
                        table[16 * ij + ab] += left * right
        one_step = {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]}
        if set(two_steps) != set(one_step):
            raise ValueError("one- and two-step structural target sets differ")
        maximum = 0
        for final, computed in two_steps.items():
            expected = [0] * 256
            for ij, coefficient in _sparse_table(one_step[final]):
                expected[16 * ij + ij] = coefficient
            maximum = max(
                maximum,
                max(abs(left - right) for left, right in zip(computed, expected, strict=True)),
            )
        if maximum:
            raise ValueError("four-variable quotient semigroup identity failed")
        counts = {
            "class_id": start,
            "transition_pairs": len(two_steps),
            "intermediate_paths": paths,
            "coefficient_cells": 256 * len(two_steps),
            "max_abs_residual": 0,
        }
        rows.append(counts)
        for key in ("transition_pairs", "intermediate_paths", "coefficient_cells"):
            totals[key] += counts[key]
    return {"verified": True, "rows": rows, "totals": totals}


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


def _class_vector_refines(left, right):
    """Whether every left-class fiber has one right-class assignment."""
    if len(left) != len(right):
        raise ValueError("partition vectors have different domains")
    mapping = {}
    for finer, coarser in zip(left, right, strict=True):
        if finer in mapping and mapping[finer] != coarser:
            return False
        mapping[finer] = coarser
    return True


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


def _question_values(model, features):
    values = {name: [] for name in QUESTIONS}
    for state, feature in zip(model["states"], features, strict=True):
        counts = feature["chain_counts"]
        values["chain_counts"].append(counts)
        values["motif_count"].append(feature["motif_count"])
        values["path_count"].append(feature["path_count"])
        values["counts_motif_path"].append([*counts, feature["motif_count"], feature["path_count"]])
        positions = {vertex: i for i, vertex in enumerate(state["kept"])}
        named = int(1 in positions and positions[1] in state["past"][positions[7]])
        values["named_relation_1_7"].append(named)
    return values


def _observable(name, values, groups):
    class_values, failure = [], None
    for group in groups:
        left = group["members"][0]
        for right in group["members"][1:]:
            if _key(values[left]) != _key(values[right]):
                failure = {
                    "class_id": group["class_id"],
                    "left_state": left,
                    "right_state": right,
                    "left_value": values[left],
                    "right_value": values[right],
                }
                break
        if failure is not None:
            break
        class_values.append(values[left])
    return {
        "name": name,
        "measurable": failure is None,
        "class_values": class_values if failure is None else None,
        "first_failure": failure,
    }


def _hash_string(value):
    if (
        type(value) is not str
        or len(value) != 64
        or any(char not in "0123456789abcdef" for char in value)
    ):
        raise ValueError("digest must be a native lowercase SHA-256 string")


def _observable_value(name, value):
    if name in ("chain_counts", "counts_motif_path"):
        length = 4 if name == "chain_counts" else 6
        if type(value) is not list or len(value) != length:
            raise ValueError("observable vector has the wrong native shape")
        bounds = (1, 6, 15, 20) if length == 4 else (1, 6, 15, 20, 9, 9)
        for index, (component, maximum) in enumerate(zip(value, bounds, strict=True)):
            _integer(component, int(index == 0), maximum)
    elif name in ("motif_count", "path_count"):
        _integer(value, 0, 9)
    elif name == "named_relation_1_7":
        _integer(value, 0, 1)
    else:
        raise ValueError("unknown declared question")


def validate_consumer(consumer):
    """Validate structure and coefficient normalization, without authentication.

    No raw observed order is available here. This validates the declared
    payload, not its correspondence to an external artifact or initial record.
    """
    _native(consumer)
    _fields(
        consumer,
        (
            "schema_version",
            "model_sha256",
            "state_classes_sha256",
            "class_count",
            "quotient_rows",
            "observables",
        ),
    )
    if consumer["schema_version"] != "det8-qr05p-consumer-v1":
        raise ValueError("unknown consumer schema")
    _hash_string(consumer["model_sha256"])
    _hash_string(consumer["state_classes_sha256"])
    count = consumer["class_count"]
    _integer(count, 1, STATE_CAP)
    quotient = consumer["quotient_rows"]
    if type(quotient) is not list or len(quotient) != count:
        raise ValueError("consumer quotient size differs from its class count")
    previous_representative, atom_count = -1, 0
    for class_id, row in enumerate(quotient):
        _fields(row, ("class_id", "representative_state", "transitions"))
        _integer(row["class_id"], class_id, class_id)
        _integer(row["representative_state"], previous_representative + 1, STATE_CAP - 1)
        if class_id == 0 and row["representative_state"] != 0:
            raise ValueError("first canonical consumer representative must be state zero")
        previous_representative = row["representative_state"]
        if type(row["transitions"]) is not list or not row["transitions"]:
            raise ValueError("consumer row has no structural transitions")
        previous = -1
        for atom in row["transitions"]:
            _fields(atom, ("target_class", "coefficients"))
            _integer(atom["target_class"], previous + 1, count - 1)
            previous = atom["target_class"]
            _table(atom["coefficients"])
        _normalized(row["transitions"])
        atom_count += len(row["transitions"])
    if atom_count > FINE_ATOM_CAP:
        raise ValueError("consumer transition atom bound exceeded")
    observables = consumer["observables"]
    if type(observables) is not list or len(observables) != len(QUESTIONS):
        raise ValueError("consumer question menu is not the declared menu")
    for name, item in zip(QUESTIONS, observables, strict=True):
        _fields(item, ("name", "measurable", "class_values", "first_failure"))
        if (
            type(item["name"]) is not str
            or item["name"] != name
            or type(item["measurable"]) is not bool
        ):
            raise ValueError("consumer question order or measurability type changed")
        if item["measurable"]:
            if (
                type(item["class_values"]) is not list
                or len(item["class_values"]) != count
                or item["first_failure"] is not None
            ):
                raise ValueError("measurable question lacks exactly one value per class")
            for value in item["class_values"]:
                _observable_value(name, value)
        else:
            if item["class_values"] is not None:
                raise ValueError("nonmeasurable question must not guess class values")
            failure = item["first_failure"]
            _fields(failure, ("class_id", "left_state", "right_state", "left_value", "right_value"))
            _integer(failure["class_id"], 0, count - 1)
            _integer(failure["left_state"], 0, STATE_CAP - 1)
            _integer(failure["right_state"], failure["left_state"] + 1, STATE_CAP - 1)
            _observable_value(name, failure["left_value"])
            _observable_value(name, failure["right_value"])
            if _key(failure["left_value"]) == _key(failure["right_value"]):
                raise ValueError("nonmeasurability witness has equal values")
    return {item["name"]: item for item in observables}


def _parse_rates(rates):
    if type(rates) is not list or len(rates) != 2:
        raise ValueError("rates must be two canonical native rational strings")
    result = []
    for value in rates:
        if (
            type(value) is not str
            or len(value) > 3000
            or re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is None
        ):
            raise ValueError("rate is not a bounded canonical integer/fraction string")
        try:
            parsed = Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational rate") from exc
        if str(parsed) != value or not 0 <= parsed <= 1:
            raise ValueError("rate must be canonical and lie in the closed unit interval")
        if max(parsed.numerator.bit_length(), parsed.denominator.bit_length()) > BIT_LIMIT:
            raise ValueError("rate exceeds the exact arithmetic bound")
        result.append(parsed)
    return tuple(result)


def _predict_core(consumer, observable, class_id, rates, parsed, cache):
    """Shared mathematical operation after public or audit-time validation."""
    probabilities, values = {}, {}
    for atom in consumer["quotient_rows"][class_id]["transitions"]:
        probability = _evaluated(atom["coefficients"], parsed, cache)
        if probability < 0:
            raise ValueError("requested quotient row has a negative probability at these rates")
        value = observable["class_values"][atom["target_class"]]
        identity = canonical(value)
        probabilities[identity] = probabilities.get(identity, Fraction(0)) + probability
        values[identity] = value
    if sum(probabilities.values()) != 1:
        raise ValueError("requested prediction does not normalize")
    outcomes = []
    for identity in sorted(probabilities):
        value = values[identity]
        probability = probabilities[identity]
        if (
            max(probability.numerator.bit_length(), probability.denominator.bit_length())
            > BIT_LIMIT
        ):
            raise ValueError("grouped probability exceeds the exact arithmetic bound")
        outcomes.append(
            {
                "value": list(value) if type(value) is list else value,
                "probability": str(probability),
            }
        )
    return {
        "question": observable["name"],
        "class_id": class_id,
        "rates": list(rates),
        "outcomes": outcomes,
    }


def predict(consumer, question, class_id, rates):
    """Predict a declared measurable observable from a verified summary payload.

    Initial domain membership and payload provenance remain caller premises.
    This function always validates the supplied native payload; it does not
    cache validation by object identity or read raw orders or hidden targets.
    """
    observables = validate_consumer(consumer)
    if type(question) is not str or question not in observables:
        raise ValueError("unknown native question")
    _integer(class_id, 0, consumer["class_count"] - 1)
    parsed = _parse_rates(rates)
    observable = observables[question]
    if not observable["measurable"]:
        raise ValueError("the requested observable is not measurable in this summary")
    return _predict_core(consumer, observable, class_id, rates, parsed, {})


def _marginal(atoms, values, target_field):
    tables, exact_values = {}, {}
    for atom in atoms:
        value = values[atom[target_field]]
        identity = canonical(value)
        if identity not in tables:
            tables[identity] = [[0] * 4 for _ in range(4)]
            exact_values[identity] = value
        _add_table(tables[identity], atom["coefficients"])
    outcomes = [{"value": exact_values[key], "coefficients": tables[key]} for key in sorted(tables)]
    _normalized(outcomes)
    return outcomes


def _named_control(model, fine_rows, values, partitions, refinement):
    state_ids = []
    for vertex in (1, 3):
        matches = [
            state["state_id"]
            for state in model["states"]
            if state["frame_id"] == 0
            and state["kept"] == [0, vertex, 7]
            and state["past"] == [[], [0], [0, 1]]
        ]
        if len(matches) != 1:
            raise ValueError("retained case requires both named singleton observations")
        state_ids.append(matches[0])
    coefficients = []
    for state_id in state_ids:
        table = [[0] * 4 for _ in range(4)]
        for atom in fine_rows[state_id]["transitions"]:
            _add_table(
                table, atom["coefficients"], values["named_relation_1_7"][atom["target_state"]]
            )
        coefficients.append(table)
    x = [[0] * 4 for _ in range(4)]
    x[1][0] = 1
    if coefficients != [x, [[0] * 4 for _ in range(4)]]:
        raise ValueError("named singleton future-event control changed")
    c = [partitions["C"]["state_classes"][i] for i in state_ids]
    h = [partitions["H"]["state_classes"][i] for i in state_ids]
    r = [refinement["state_classes"][i] for i in state_ids]
    current = [values["named_relation_1_7"][i] for i in state_ids]
    if c[0] != c[1] or h[0] != h[1] or r[0] != r[1] or current != [1, 0]:
        raise ValueError("named-query exclusion does not hold on the supplied finite case")
    return {
        "state_ids": state_ids,
        "C_classes": c,
        "H_classes": h,
        "R_classes": r,
        "current_values": current,
        "next_coefficients": coefficients,
        "half_probabilities": [
            str(evaluate(table, (Fraction(1, 2), Fraction(1, 2)))) for table in coefficients
        ],
        "same_R_class": r[0] == r[1],
    }


def _consumer(model, features, fine_rows, partitions, refinement):
    values = _question_values(model, features)
    consumer = {
        "schema_version": "det8-qr05p-consumer-v1",
        "model_sha256": _digest(model),
        "state_classes_sha256": _digest(refinement["state_classes"]),
        "class_count": len(refinement["classes"]),
        "quotient_rows": refinement["quotient_rows"],
        "observables": [
            _observable(name, values[name], refinement["classes"]) for name in QUESTIONS
        ],
    }
    observables = validate_consumer(consumer)
    marginals, prediction_checks, cache = [], 0, {}
    for name in QUESTIONS:
        observable = observables[name]
        if not observable["measurable"]:
            try:
                predict(consumer, name, 0, ["1/2", "1/2"])
            except ValueError:
                continue
            raise ValueError("public predictor accepted a nonmeasurable observable")
        rows = [
            {
                "class_id": row["class_id"],
                "outcomes": _marginal(
                    row["transitions"], observable["class_values"], "target_class"
                ),
            }
            for row in consumer["quotient_rows"]
        ]
        cells = 0
        for fine in fine_rows:
            outcomes = _marginal(fine["transitions"], values[name], "target_state")
            class_id = refinement["state_classes"][fine["state_id"]]
            if _key(outcomes) != _key(rows[class_id]["outcomes"]):
                raise ValueError("summary observable marginal differs from the fine law")
            cells += 16 * len(outcomes)
        for row in rows:
            class_id = row["class_id"]
            for rates in RATES:
                texts = [str(x) for x in rates]
                prediction = _predict_core(consumer, observable, class_id, texts, rates, cache)
                expected = [
                    {
                        "value": atom["value"],
                        "probability": str(_evaluated(atom["coefficients"], rates, cache)),
                    }
                    for atom in row["outcomes"]
                ]
                if _key(prediction["outcomes"]) != _key(expected):
                    raise ValueError("prediction operation differs from the polynomial marginal")
                prediction_checks += 1
        marginals.append({"name": name, "rows": rows, "fine_coefficient_cells": cells})
    named = _named_control(model, fine_rows, values, partitions, refinement)
    audit = {
        "marginals": marginals,
        "prediction_checks": prediction_checks,
        "nonmeasurable_questions": [
            name for name in QUESTIONS if not observables[name]["measurable"]
        ],
        "named_singleton_control": named,
        "verified": True,
    }
    return consumer, audit


def analyze(problem):
    """Reconstruct the declared model and certify its closed summary consumer."""
    _native(problem)
    _fields(problem, ("schema_version", "family", "model"))
    if (
        problem["schema_version"] != "det8-qr05p-problem-v1"
        or problem["family"] != "qr05p_summary_contract"
    ):
        raise ValueError("unsupported fixed investigation schema or family")
    model = problem["model"]
    features, fine_rows, partitions = reconstruct(model)
    fine = _audit_fine(model, fine_rows)
    refinement = _refinement(fine_rows, partitions)
    consumer, consumer_audit = _consumer(model, features, fine_rows, partitions, refinement)
    result = {
        "model_sha256": _digest(model),
        "features": features,
        "partitions": partitions,
        "fine_kernel": fine,
        "refinement": refinement,
        "consumer": consumer,
        "consumer_audit": consumer_audit,
        "counts": {
            "states": len(model["states"]),
            "features": len(features),
            "C_classes": len(partitions["C"]["classes"]),
            "H_classes": len(partitions["H"]["classes"]),
            "R_classes": len(refinement["classes"]),
            "fine_atoms": fine["transition_atoms"],
            "refinement_rounds": len(refinement["rounds"]),
            "strict_rounds": refinement["strict_rounds"],
            "measurable_questions": sum(item["measurable"] for item in consumer["observables"]),
            "consumer_prediction_checks": consumer_audit["prediction_checks"],
            "consumer_fine_coefficient_cells": sum(
                item["fine_coefficient_cells"] for item in consumer_audit["marginals"]
            ),
        },
    }
    canonical(result)
    return result
