"""QR-05N observed-order domain-portability executor.

Exact wire, ordered support-union, binomial, and composition utilities descend
from this route's QR-05M primary, copied locally rather than imported at runtime.
Chain vertex sets use the supplied partial order, never numeric label order.
The unchanged observed motif is tested without automatic partition refinement.
No files, prior artifacts, other executors, or reference routes are accessed.
"""

from fractions import Fraction
from itertools import combinations
from math import comb

OLD_PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
PROFILES = (
    OLD_PROFILES
    + tuple(f"layered_oe_{mask:03d}" for mask in range(512))
    + tuple(f"layered_eo_{mask:03d}" for mask in range(512))
)
EXTRA_RELATIONS = {
    "path6": ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6)),
    "cycle4_edge": ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5)),
}
PARTITIONS = ("pair_graded", "motif_pair")
BIT_LIMIT = 4096
STATE_CAP = 2579
FINE_ATOM_CAP = 100393


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


def _kept(fixed, eligible, mask):
    return sorted(fixed + [vertex for bit, vertex in enumerate(eligible) if mask & (1 << bit)])


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


def _source(profile):
    """Build old sources or the fixed row-major incidence convention."""
    past = [[] for _ in range(8)]
    for right in range(1, 8):
        past[right].append(0)
    past[7].extend(range(1, 7))
    if profile.startswith("layered_"):
        _, direction, mask_text = profile.split("_")
        mask = int(mask_text)
        if direction not in ("oe", "eo") or not 0 <= mask < 512:
            raise ValueError("invalid layered incidence profile")
        for i, odd in enumerate((1, 3, 5)):
            for j, even in enumerate((2, 4, 6)):
                if mask & (1 << (3 * i + j)):
                    left, right = (odd, even) if direction == "oe" else (even, odd)
                    past[right].append(left)
    elif profile == "chain6":
        for right in range(2, 7):
            past[right].extend(range(1, right))
    elif profile in EXTRA_RELATIONS:
        for left, right in EXTRA_RELATIONS[profile]:
            past[right].append(left)
    elif profile in ("ferrers6", "ferrers6_fixed", "standard_example3"):
        for left in range(1, 4):
            for right in range(4, 7):
                related = (
                    left - 1 != right - 4
                    if profile == "standard_example3"
                    else left - 1 <= right - 4
                )
                if related:
                    past[right].append(left)
    else:
        raise ValueError("unknown fixed-family source")
    past = [sorted(row) for row in past]
    _valid_order(list(range(8)), past)
    return past


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


def _state_from_observation(state_id, frame, mask, kept, past):
    _valid_order(kept, past)
    odd_mask = sum(1 << bit for bit, vertex in enumerate(frame["eligible"]) if vertex % 2)
    supports = _supports(kept, past, frame["eligible"])
    mean, pairs = _summaries(supports, odd_mask)
    motifs = motif_supports(kept, past, frame["eligible"])
    if len(motifs) > 9:
        raise ValueError("fixed-family motif count exceeds its four-subset bound")
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
        "motif_supports": motifs,
        "motif_count": len(motifs),
        "classes": {},
        "transitions": [],
        "summary_laws": {},
    }


def _enumerate_states():
    frames, profiles, states = [], [], []
    frame_ids, identities = {}, {}
    for profile_index, name in enumerate(PROFILES):
        fixed = [0, 3, 7] if name == "ferrers6_fixed" else [0, 7]
        eligible = [vertex for vertex in range(1, 7) if vertex not in fixed]
        if len(eligible) > 6 or any(
            sum(vertex % 2 == color for vertex in eligible) > 3 for color in (0, 1)
        ):
            raise ValueError("eligible count or named-color cap exceeded")
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
            if mask >= 64:
                raise ValueError("source mask cap exceeded")
            kept = _kept(fixed, eligible, mask)
            past = _induce(list(range(8)), source_past, kept)
            identity = _state_identity(frame_id, kept, past)
            state_id = identities.get(identity)
            if state_id is None:
                state_id = len(states)
                identities[identity] = state_id
                states.append(_state_from_observation(state_id, frame, mask, kept, past))
                if len(states) > STATE_CAP:
                    raise ValueError("state resource cap exceeded")
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
        if profile_index == 5 and len(states) != 257:
            raise ValueError("old observed-state prefix changed")
    if (
        len(profiles) != 1030
        or len(states) != 2470
        or len(frames) != 2
        or sum(len(p["state_ids"]) for p in profiles) != 65888
    ):
        raise ValueError("fixed observed-state universe changed")
    return frames, profiles, states, identities


def _partition_states(frames, states):
    partitions = {name: [] for name in PARTITIONS}
    identities = {name: {} for name in PARTITIONS}
    for state in states:
        frame = _frame_key(frames[state["frame_id"]])
        keys = {
            "pair_graded": [frame, state["pair_graded"]],
            "motif_pair": [frame, state["pair_graded"], state["motif_count"]],
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


def _transitions(frames, states, identities):
    kernels = {}
    fine_atoms = 0
    for state in states:
        frame = frames[state["frame_id"]]
        for mask in range(1 << len(frame["eligible"])):
            if mask & ~state["mask"]:
                continue
            kept = _kept(frame["fixed"], frame["eligible"], mask)
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in identities:
                raise ValueError("observed-state domain is not closed under restriction")
            target_id = identities[identity]
            target = states[target_id]
            key = (*state["color_sizes"], *target["color_sizes"])
            if key not in kernels:
                kernels[key] = _kernel_polynomial(state["color_sizes"], target["color_sizes"])
            state["transitions"].append({"target_state": target_id, "coefficients": kernels[key]})
        state["transitions"].sort(key=lambda atom: atom["target_state"])
        fine_atoms += len(state["transitions"])
        if fine_atoms > FINE_ATOM_CAP or len(kernels) > 100:
            raise ValueError("fine transition or kernel resource cap exceeded")
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
    if fine_atoms != 99180:
        raise ValueError("fixed-family fine transition inventory changed")


def _closure(states, partitions):
    result = {}
    zero = [[0] * 4 for _ in range(4)]
    for name in PARTITIONS:
        maps = [
            {atom["target_class"]: atom["coefficients"] for atom in state["summary_laws"][name]}
            for state in states
        ]
        collision = None
        for group in partitions[name]:
            representative = group["members"][0]
            left = maps[representative]
            for member in group["members"][1:]:
                right = maps[member]
                differences = [
                    target
                    for target in sorted(set(left) | set(right))
                    if left.get(target, zero) != right.get(target, zero)
                ]
                if differences:
                    target = differences[0]
                    collision = {
                        "class_id": group["class_id"],
                        "left_state": representative,
                        "right_state": member,
                        "target_class": target,
                        "left_coefficients": left.get(target, zero),
                        "right_coefficients": right.get(target, zero),
                    }
                    break
            if collision is not None:
                break
        quotient, semigroup = [], None
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
    return result


def _motif_expected_update(states):
    rows = []
    for state in states:
        actual = [[0] * 4 for _ in range(4)]
        for atom in state["transitions"]:
            _add_table(actual, atom["coefficients"], states[atom["target_state"]]["motif_count"])
        expected = [[0] * 4 for _ in range(4)]
        expected[2][2] = state["motif_count"]
        maximum = max(abs(actual[i][j] - expected[i][j]) for i in range(4) for j in range(4))
        if maximum:
            raise ValueError("eligible induced-motif expectation identity failed")
        rows.append(
            {
                "state_id": state["state_id"],
                "coefficients": actual,
                "expected_coefficients": expected,
                "max_abs_residual": 0,
            }
        )
    return {"verified": True, "rows": rows, "coefficient_cells": 16 * len(rows)}


def analyze(problem):
    """Compute the fixed finite family, retaining an honest closure decision."""
    if (
        type(problem) is not dict
        or any(type(key) is not str for key in problem)
        or set(problem) != {"schema_version", "family"}
        or type(problem.get("schema_version")) is not str
        or problem["schema_version"] != "det8-qr05n-problem-v1"
        or type(problem.get("family")) is not str
        or problem["family"] != "qr05n_layered_iid"
    ):
        raise ValueError("expected the exact QR-05N qr05n_layered_iid problem")
    frames, profiles, states, identities = _enumerate_states()
    partitions = _partition_states(frames, states)
    _transitions(frames, states, identities)
    expected = _expected_updates(states)
    motif_expected = _motif_expected_update(states)
    closure = _closure(states, partitions)
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
        "motif_support_occurrences": sum(state["motif_count"] for state in states),
        "motif_positive_states": sum(state["motif_count"] > 0 for state in states),
        "max_motif_count": max((state["motif_count"] for state in states), default=0),
        "expected_update_coefficient_cells": expected["coefficient_cells"],
        "motif_expected_update_coefficient_cells": motif_expected["coefficient_cells"],
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
            "closure": closure,
            "expected_updates": expected,
            "motif_expected_update": motif_expected,
            "counts": counts,
        }
    )
