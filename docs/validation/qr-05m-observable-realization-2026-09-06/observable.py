"""QR-05M constructive observed-order motif and recursive summary realization.

Observed-chain, binomial, quotient, and refinement utilities descend from this
route's QR-05L primary source, copied locally rather than imported at runtime.
The motif and candidate partition use only the supplied observed order/marks;
the independently computed stable partition is consulted only for comparison.
No files, previous executors, captured artifacts, or reference route are accessed.
"""

from fractions import Fraction
from itertools import combinations, pairwise, permutations
from math import comb

PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
EXTRA_RELATIONS = {
    "path6": ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6)),
    "cycle4_edge": ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5)),
}
PARTITIONS = ("mean_graded", "pair_graded", "color_order", "full_record")
BIT_LIMIT = 4096


def wire(value):
    """Encode exact native JSON without implicit type or container coercions."""
    if type(value) is Fraction:
        if max(value.numerator.bit_length(), value.denominator.bit_length()) > BIT_LIMIT:
            raise ValueError("rational exceeds the exact arithmetic bound")
        return str(value)
    if value is None or type(value) in (str, bool):
        return value
    if type(value) is int:
        if value.bit_length() > BIT_LIMIT:
            raise ValueError("integer exceeds the exact arithmetic bound")
        return value
    if type(value) is list:
        return [wire(item) for item in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise TypeError("wire dictionary keys must be native strings")
        return {key: wire(item) for key, item in value.items()}
    raise TypeError("unsupported exact wire value")


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


def _source(profile):
    past = [[] for _ in range(8)]
    for right in range(1, 8):
        past[right].append(0)
    past[7].extend(range(1, 7))
    if profile == "chain6":
        for right in range(2, 7):
            past[right].extend(range(1, right))
    elif profile in EXTRA_RELATIONS:
        for left, right in EXTRA_RELATIONS[profile]:
            past[right].append(left)
    else:
        for left in range(1, 4):
            for right in range(4, 7):
                related = (
                    left - 1 != right - 4
                    if profile == "standard_example3"
                    else left - 1 <= right - 4
                )
                if related:
                    past[right].append(left)
    return [sorted(row) for row in past]


def _kept(fixed, eligible, mask):
    return sorted(fixed + [vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit)])


def _induce(parent_kept, parent_past, kept):
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
    """List observed chains' eligible supports, retaining equal-mask chains."""
    positions = {vertex: index for index, vertex in enumerate(kept)}
    bits = {vertex: 1 << bit for bit, vertex in enumerate(eligible)}
    internal = [vertex for vertex in kept if vertex not in (0, 7)]
    result = [[] for _ in range(4)]
    for q in range(4):
        for vertices in combinations(internal, q):
            path = [0, *vertices, 7]
            if all(positions[left] in past[positions[right]] for left, right in pairwise(path)):
                result[q].append(sum(bits.get(vertex, 0) for vertex in vertices))
    return result


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


def _color_order(kept, past, fixed):
    """Canonical fixed-anchored order with named eligible color marks."""
    anchors = sorted(fixed)
    if len(set(anchors)) != len(anchors) or not set(anchors) <= set(kept):
        raise ValueError("fixed anchors must be distinct observed vertices")
    eligible = [vertex for vertex in kept if vertex not in anchors]
    if len(eligible) > 6:
        raise ValueError("canonical permutation bound exceeded")
    edges = [
        (kept[left], kept[right])
        for right, predecessors in enumerate(past)
        for left in predecessors
    ]
    size, best = len(kept), None
    for remaining in permutations(eligible):
        positions = {vertex: index for index, vertex in enumerate([*anchors, *remaining])}
        relation = sum(1 << (positions[left] * size + positions[right]) for left, right in edges)
        color = sum(1 << positions[vertex] for vertex in remaining if vertex % 2)
        if best is None or (relation, color) < best:
            best = (relation, color)
    return [size, *best]


def _frame_key(frame):
    return [frame["density"], frame["fixed"], frame["eligible"]]


def _state_from_observation(state_id, frame, mask, kept, past):
    odd_mask = sum(1 << bit for bit, vertex in enumerate(frame["eligible"]) if vertex % 2)
    supports = _supports(kept, past, frame["eligible"])
    mean, pairs = _summaries(supports, odd_mask)
    return {
        "state_id": state_id,
        "frame_id": frame["frame_id"],
        "mask": mask,
        "kept": kept,
        "past": past,
        "aliases": [],
        "color_sizes": [(mask & odd_mask).bit_count(), (mask & ~odd_mask).bit_count()],
        "chain_counts": [len(chains) for chains in supports],
        "mean_graded": mean,
        "pair_graded": pairs,
        "color_order": _color_order(kept, past, frame["fixed"]),
        "classes": {},
        "transitions": [],
        "summary_laws": {},
    }


def _enumerate_states():
    frames, profiles, states = [], [], []
    frame_ids, state_ids = {}, {}
    for profile_index, name in enumerate(PROFILES):
        fixed = [0, 3, 7] if name == "ferrers6_fixed" else [0, 7]
        eligible = [vertex for vertex in range(1, 7) if vertex not in fixed]
        frame_value = ["12", fixed, eligible]
        frame_identity = _key(frame_value)
        frame_id = frame_ids.get(frame_identity)
        if frame_id is None:
            frame_id = len(frames)
            frame_ids[frame_identity] = frame_id
            frames.append(
                {"frame_id": frame_id, "density": "12", "fixed": fixed, "eligible": eligible}
            )
        frame = frames[frame_id]
        source_past = _source(name)
        aliases = []
        for mask in range(1 << len(eligible)):
            kept = _kept(fixed, eligible, mask)
            past = _induce(list(range(8)), source_past, kept)
            identity = _key([frame_value, kept, past])
            state_id = state_ids.get(identity)
            if state_id is None:
                state_id = len(states)
                state_ids[identity] = state_id
                states.append(_state_from_observation(state_id, frame, mask, kept, past))
            states[state_id]["aliases"].append({"profile_index": profile_index, "mask": mask})
            aliases.append(state_id)
        profiles.append(
            {
                "profile_index": profile_index,
                "name": name,
                "frame_id": frame_id,
                "past": source_past,
                "state_ids": aliases,
            }
        )
    if len(states) != 257 or len(frames) != 2 or sum(len(p["state_ids"]) for p in profiles) != 352:
        raise ValueError("fixed observed-state universe changed")
    return frames, profiles, states, state_ids


def _partition_states(frames, states):
    partitions = {name: [] for name in PARTITIONS}
    identities = {name: {} for name in PARTITIONS}
    for state in states:
        frame = _frame_key(frames[state["frame_id"]])
        keys = {
            "mean_graded": [frame, state["mean_graded"]],
            "pair_graded": [frame, state["pair_graded"]],
            "color_order": [frame, state["color_order"]],
            "full_record": [frame, state["kept"], state["past"]],
        }
        for name in PARTITIONS:
            identity = _key(keys[name])
            class_id = identities[name].get(identity)
            if class_id is None:
                class_id = len(partitions[name])
                identities[name][identity] = class_id
                partitions[name].append({"class_id": class_id, "key": keys[name], "members": []})
            partitions[name][class_id]["members"].append(state["state_id"])
            state["classes"][name] = class_id
    return partitions


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


def _transitions(frames, states, identities):
    for state in states:
        frame = frames[state["frame_id"]]
        frame_value = _frame_key(frame)
        for mask in range(1 << len(frame["eligible"])):
            if mask & ~state["mask"]:
                continue
            kept = _kept(frame["fixed"], frame["eligible"], mask)
            past = _induce(state["kept"], state["past"], kept)
            identity = _key([frame_value, kept, past])
            if identity not in identities:
                raise ValueError("observed-state domain is not closed under restriction")
            target_id = identities[identity]
            target = states[target_id]
            state["transitions"].append(
                {
                    "target_state": target_id,
                    "coefficients": _kernel_polynomial(state["color_sizes"], target["color_sizes"]),
                }
            )
        state["transitions"].sort(key=lambda atom: atom["target_state"])
        _normalized(state["transitions"])
        for name in PARTITIONS:
            tables = {}
            for atom in state["transitions"]:
                target_class = states[atom["target_state"]]["classes"][name]
                if target_class not in tables:
                    tables[target_class] = [[0] * 4 for _ in range(4)]
                _add_table(tables[target_class], atom["coefficients"])
            state["summary_laws"][name] = [
                {"target_class": target_class, "coefficients": tables[target_class]}
                for target_class in sorted(tables)
            ]
            _normalized(state["summary_laws"][name])


def _refines(states, finer, coarser):
    assigned = {}
    for state in states:
        left, right = state["classes"][finer], state["classes"][coarser]
        if left in assigned and assigned[left] != right:
            return False
        assigned[left] = right
    return True


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


def _closure(states, partitions):
    result = {}
    zero = [[0] * 4 for _ in range(4)]
    for name in PARTITIONS:
        maps = [
            {atom["target_class"]: atom["coefficients"] for atom in state["summary_laws"][name]}
            for state in states
        ]
        collision = None
        for state in states:
            class_id = state["classes"][name]
            representative = partitions[name][class_id]["members"][0]
            left, right = maps[representative], maps[state["state_id"]]
            differences = [
                target
                for target in sorted(set(left) | set(right))
                if left.get(target, zero) != right.get(target, zero)
            ]
            if differences and collision is None:
                target = differences[0]
                collision = {
                    "class_id": class_id,
                    "left_state": representative,
                    "right_state": state["state_id"],
                    "target_class": target,
                    "left_coefficients": left.get(target, zero),
                    "right_coefficients": right.get(target, zero),
                }
        quotient = semigroup = None
        if collision is None:
            quotient = [
                {
                    "class_id": group["class_id"],
                    "representative_state": group["members"][0],
                    "transitions": states[group["members"][0]]["summary_laws"][name],
                }
                for group in partitions[name]
            ]
            semigroup = _semigroup(quotient)
        result[name] = {
            "closed": collision is None,
            "first_collision": collision,
            "quotient_rows": quotient,
            "semigroup": semigroup,
        }
    if not result["color_order"]["closed"] or not result["full_record"]["closed"]:
        raise ValueError("constructive sufficient closure control failed")
    return result


def _flatten_features(state):
    means = [v for table in state["mean_graded"] for row in table for v in row]
    pairs = [v for tensor in state["pair_graded"] for table in tensor for row in table for v in row]
    if len(means) != 64 or len(pairs) != 256:
        raise ValueError("feature padding changed")
    return [*means, *pairs]


def _expected_updates(states):
    features = [_flatten_features(state) for state in states]
    nonzero = [[(i, value) for i, value in enumerate(row) if value] for row in features]
    rows = []
    for state in states:
        computed = [[0] * 16 for _ in range(320)]
        for atom in state["transitions"]:
            for feature, value in nonzero[atom["target_state"]]:
                for degree, coefficient in _sparse_table(atom["coefficients"]):
                    computed[feature][degree] += value * coefficient
        maximum = 0
        for feature, coefficients in enumerate(computed):
            current = features[state["state_id"]][feature]
            maximum = max(
                maximum,
                max(
                    abs(coefficient - (current if degree == feature % 16 else 0))
                    for degree, coefficient in enumerate(coefficients)
                ),
            )
        if maximum:
            raise ValueError("support-graded expected update identity failed")
        rows.append(
            {
                "state_id": state["state_id"],
                "mean_features": 64,
                "pair_features": 256,
                "coefficient_cells": 5120,
                "max_abs_residual": 0,
            }
        )
    return {"verified": True, "rows": rows, "coefficient_cells": 5120 * len(states)}


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


def _next_round(current, rows):
    """Keep the current class in every key, preventing an improper merge."""
    identities, classes, groups = {}, [], []
    for state_id, row in enumerate(rows):
        identity = _key([current[state_id], row["transitions"]])
        class_id = identities.get(identity)
        if class_id is None:
            class_id = len(groups)
            identities[identity] = class_id
            groups.append({"class_id": class_id, "members": []})
        groups[class_id]["members"].append(state_id)
        classes.append(class_id)
    if not _class_vector_refines(classes, current):
        raise ValueError("synchronous refinement merged a required distinction")
    return classes, groups


def _separations(current, groups, rows, following, next_groups):
    """Attach each non-first child to its parent's first current member."""
    witnesses = []
    zero = [[0] * 4 for _ in range(4)]
    row_maps = [
        {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]} for row in rows
    ]
    for child in next_groups:
        right_state = child["members"][0]
        parent_class = current[right_state]
        left_state = groups[parent_class]["members"][0]
        if child["class_id"] == following[left_state]:
            continue
        if any(current[member] != parent_class for member in child["members"]):
            raise ValueError("a refinement child crosses parent blocks")
        left, right = row_maps[left_state], row_maps[right_state]
        target = next(
            (
                successor
                for successor in sorted(set(left) | set(right))
                if left.get(successor, zero) != right.get(successor, zero)
            ),
            None,
        )
        if target is None:
            raise ValueError("split child has no current-row separation")
        witnesses.append(
            {
                "parent_class_id": parent_class,
                "child_class_id": child["class_id"],
                "left_state": left_state,
                "right_state": right_state,
                "target_class": target,
                "left_coefficients": left.get(target, zero),
                "right_coefficients": right.get(target, zero),
            }
        )
    if len(witnesses) != len(next_groups) - len(groups):
        raise ValueError("refinement separation count does not match strict splits")
    return witnesses


def _stabilize(states, partitions):
    """Construct and certify the coarsest closed refinement of the pair blocks."""
    current = [state["classes"]["pair_graded"] for state in states]
    initial = list(current)
    groups = [
        {"class_id": group["class_id"], "members": list(group["members"])}
        for group in partitions["pair_graded"]
    ]
    initial_count = len(groups)
    rounds = []
    strict_rounds = 0
    while True:
        rows = _round_pushforwards(states, current)
        following, next_groups = _next_round(current, rows)
        stable = following == current
        if stable:
            if next_groups != groups:
                raise ValueError("stable assignments disagree with class memberships")
            separations = []
        else:
            if len(next_groups) <= len(groups):
                raise ValueError("nonterminal refinement did not strictly split")
            separations = _separations(current, groups, rows, following, next_groups)
        rounds.append(
            {
                "round_index": len(rounds),
                "state_classes": current,
                "classes": groups,
                "pushforward_rows": rows,
                "stable": stable,
                "separations": separations,
            }
        )
        if stable:
            break
        strict_rounds += 1
        if strict_rounds > len(states) - initial_count:
            raise ValueError("strict refinement violated the finite partition bound")
        current, groups = following, next_groups
    if not _class_vector_refines(current, initial):
        raise ValueError("terminal partition does not refine original B")
    for group in groups:
        representative = group["members"][0]
        if any(
            rows[member]["transitions"] != rows[representative]["transitions"]
            for member in group["members"]
        ):
            raise ValueError("terminal partition is not strongly closed")
    quotient = [
        {
            "class_id": group["class_id"],
            "representative_state": group["members"][0],
            "transitions": rows[group["members"][0]]["transitions"],
        }
        for group in groups
    ]
    semigroup = _semigroup(quotient)
    names = ["mean_graded", "pair_graded", "stable_pair", "color_order", "full_record"]
    vectors = {
        name: current if name == "stable_pair" else [state["classes"][name] for state in states]
        for name in names
    }
    comparison = [
        [_class_vector_refines(vectors[left], vectors[right]) for right in names] for left in names
    ]
    if not comparison[3][2] or not comparison[4][2] or not comparison[2][1]:
        raise ValueError("closed-refinement inclusion controls failed")
    round_atoms = sum(
        len(row["transitions"]) for round_item in rounds for row in round_item["pushforward_rows"]
    )
    return {
        "initial_partition": "pair_graded",
        "rounds": rounds,
        "strict_rounds": strict_rounds,
        "final_round": len(rounds) - 1,
        "state_classes": current,
        "classes": groups,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "comparison": {"names": names, "refinement": comparison},
        "counts": {
            "rounds": len(rounds),
            "strict_rounds": strict_rounds,
            "classes": len(groups),
            "round_transition_atoms": round_atoms,
            "round_coefficient_cells": 16 * round_atoms,
            "separation_witnesses": sum(len(item["separations"]) for item in rounds),
            "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
            "semigroup_intermediate_paths": semigroup["totals"]["intermediate_paths"],
            "semigroup_coefficient_cells": semigroup["totals"]["coefficient_cells"],
        },
    }


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


def _observable(frames, states):
    """Construct the observed feature and its quotient without stable classes."""
    observed, state_classes, classes, identities = [], [], [], {}
    for state in states:
        frame = frames[state["frame_id"]]
        supports = motif_supports(state["kept"], state["past"], frame["eligible"])
        count = len(supports)
        observed.append(
            {
                "state_id": state["state_id"],
                "motif_supports": supports,
                "motif_count": count,
            }
        )
        identity = _key([_frame_key(frame), state["pair_graded"], count])
        class_id = identities.get(identity)
        if class_id is None:
            class_id = len(classes)
            identities[identity] = class_id
            classes.append({"class_id": class_id, "members": []})
        state_classes.append(class_id)
        classes[class_id]["members"].append(state["state_id"])

    rows = _round_pushforwards(states, state_classes)
    maps = [
        {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]} for row in rows
    ]
    zero = [[0] * 4 for _ in range(4)]
    failure = None
    # The candidate's first witness is ordered by class, member, then target,
    # independently of the carried L basic-partition witness ordering.
    for group in classes:
        representative = group["members"][0]
        left = maps[representative]
        for member in group["members"][1:]:
            right = maps[member]
            for target in sorted(set(left) | set(right)):
                if left.get(target, zero) != right.get(target, zero):
                    failure = {
                        "class_id": group["class_id"],
                        "left_state": representative,
                        "right_state": member,
                        "target_class": target,
                        "left_coefficients": left.get(target, zero),
                        "right_coefficients": right.get(target, zero),
                    }
                    break
            if failure is not None:
                break
        if failure is not None:
            break

    quotient, semigroup = [], None
    if failure is None:
        quotient = [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": rows[group["members"][0]]["transitions"],
            }
            for group in classes
        ]
        semigroup = _semigroup(quotient)

    update_rows = []
    for state in states:
        actual = [[0] * 4 for _ in range(4)]
        for atom in state["transitions"]:
            _add_table(
                actual,
                atom["coefficients"],
                observed[atom["target_state"]]["motif_count"],
            )
        expected = [[0] * 4 for _ in range(4)]
        expected[2][2] = observed[state["state_id"]]["motif_count"]
        maximum = max(abs(actual[i][j] - expected[i][j]) for i in range(4) for j in range(4))
        update_rows.append(
            {
                "state_id": state["state_id"],
                "coefficients": actual,
                "expected_coefficients": expected,
                "max_abs_residual": maximum,
            }
        )
    update = {
        "verified": all(row["max_abs_residual"] == 0 for row in update_rows),
        "coefficient_cells": 16 * len(update_rows),
        "rows": update_rows,
    }
    state_atoms = sum(len(row["transitions"]) for row in rows)
    return {
        "definition": "eligible_color_layered_induced_k22",
        "states": observed,
        "state_classes": state_classes,
        "classes": classes,
        "pushforward_rows": rows,
        "closed": failure is None,
        "first_failure": failure,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "expected_update": update,
        "counts": {
            "states": len(observed),
            "motif_positive_states": sum(item["motif_count"] > 0 for item in observed),
            "motif_support_occurrences": sum(item["motif_count"] for item in observed),
            "max_motif_count": max((item["motif_count"] for item in observed), default=0),
            "classes": len(classes),
            "state_transition_atoms": state_atoms,
            "state_coefficient_cells": 16 * state_atoms,
            "expected_update_coefficient_cells": update["coefficient_cells"],
            "quotient_transition_atoms": sum(len(row["transitions"]) for row in quotient),
            "semigroup_intermediate_paths": (
                semigroup["totals"]["intermediate_paths"] if semigroup is not None else 0
            ),
            "semigroup_coefficient_cells": (
                semigroup["totals"]["coefficient_cells"] if semigroup is not None else 0
            ),
        },
    }


def _compare_observable(observable, stabilization):
    """Compare actual independently constructed partitions and complete rows."""
    candidate, stable = observable["state_classes"], stabilization["state_classes"]
    same = candidate == stable and observable["classes"] == stabilization["classes"]
    comparison = {
        "same_memberships_as_stable_pair": same,
        "candidate_refines_stable": _class_vector_refines(candidate, stable),
        "stable_refines_candidate": _class_vector_refines(stable, candidate),
    }
    if same:
        stable_rows = stabilization["rounds"][stabilization["final_round"]]["pushforward_rows"]
        if (
            observable["pushforward_rows"] != stable_rows
            or not observable["closed"]
            or observable["quotient_rows"] != stabilization["quotient_rows"]
            or observable["semigroup"] != stabilization["semigroup"]
        ):
            raise ValueError("equal candidate and stable partitions disagree in their update laws")
    return comparison


def analyze(problem):
    """Compute the exact deduplicated supplied observation/update universe."""
    if (
        type(problem) is not dict
        or any(type(key) is not str for key in problem)
        or set(problem) != {"schema_version", "family"}
        or type(problem.get("schema_version")) is not str
        or problem["schema_version"] != "det8-qr05m-problem-v1"
        or type(problem.get("family")) is not str
        or problem["family"] != "qr05m_observable_iid"
    ):
        raise ValueError("expected the exact QR-05M qr05m_observable_iid problem")
    frames, profiles, states, identities = _enumerate_states()
    partitions = _partition_states(frames, states)
    _transitions(frames, states, identities)
    observable = _observable(frames, states)
    refinement = [
        [_refines(states, finer, coarser) for coarser in PARTITIONS] for finer in PARTITIONS
    ]
    expected = _expected_updates(states)
    closure = _closure(states, partitions)
    stabilization = _stabilize(states, partitions)
    observable["comparison"] = _compare_observable(observable, stabilization)
    fine_atoms = sum(len(state["transitions"]) for state in states)
    summary_atoms = sum(len(law) for state in states for law in state["summary_laws"].values())
    closed = [item for item in closure.values() if item["closed"]]
    counts = {
        "frames": len(frames),
        "profiles": len(profiles),
        "aliases": sum(len(state["aliases"]) for state in states),
        "states": len(states),
        "partitions": len(PARTITIONS),
        "fine_transition_atoms": fine_atoms,
        "summary_transition_atoms": summary_atoms,
        "transition_coefficient_cells": 16 * (fine_atoms + summary_atoms),
        "mean_feature_cells": 64 * len(states),
        "pair_feature_cells": 256 * len(states),
        "expected_update_coefficient_cells": expected["coefficient_cells"],
        "closed_partitions": len(closed),
        "quotient_transition_atoms": sum(
            len(row["transitions"]) for item in closed for row in item["quotient_rows"]
        ),
        "semigroup_intermediate_paths": sum(
            item["semigroup"]["totals"]["intermediate_paths"] for item in closed
        ),
        "semigroup_coefficient_cells": sum(
            item["semigroup"]["totals"]["coefficient_cells"] for item in closed
        ),
    }
    return wire(
        {
            "frames": frames,
            "profiles": profiles,
            "states": states,
            "partitions": partitions,
            "partition_refinement": refinement,
            "closure": closure,
            "expected_updates": expected,
            "counts": counts,
            "stabilization": stabilization,
            "observable": observable,
        }
    )
