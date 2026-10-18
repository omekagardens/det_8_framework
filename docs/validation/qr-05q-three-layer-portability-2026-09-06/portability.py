"""QR-05Q primary: unchanged-summary portability on three-layer orders.

Observed chain subsets, ordered support unions, induced quartet recognizers
and binomial kernels use locally carried primary O/P utility lineage.
Full source closure precedes restriction. Parity, not layers, defines color.
No prior artifact, other executor or external state is read by this module.
"""

import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import comb

BIT_LIMIT = 4096
STATE_CAP = 35238
FINE_ATOM_CAP = 472428
WORKING_CAP = 512 * 1024 * 1024
OLD_PROFILES = ("ferrers6", "standard_example3", "chain6", "ferrers6_fixed", "path6", "cycle4_edge")
PROFILES = (
    OLD_PROFILES
    + tuple(f"layered_oe_{mask:03d}" for mask in range(512))
    + tuple(f"layered_eo_{mask:03d}" for mask in range(512))
    + tuple(f"three_layer_forward_{mask:03d}" for mask in range(256))
    + tuple(f"three_layer_reverse_{mask:03d}" for mask in range(256))
)
EXTRA_RELATIONS = {
    "path6": ((1, 2), (1, 4), (3, 4), (3, 6), (5, 6)),
    "cycle4_edge": ((1, 4), (1, 6), (3, 4), (3, 6), (2, 5)),
}
ADJACENT_EDGES = ((1, 3), (1, 4), (2, 3), (2, 4), (3, 5), (3, 6), (4, 5), (4, 6))
FRAMES = [
    {"frame_id": 0, "density": "12", "fixed": [0, 7], "eligible": [1, 2, 3, 4, 5, 6]},
    {"frame_id": 1, "density": "12", "fixed": [0, 3, 7], "eligible": [1, 2, 4, 5, 6]},
]
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


def _source(name):
    """Generate the fixed incidence source and close it before any deletion."""
    if type(name) is not str or name not in PROFILES:
        raise ValueError("unknown native source profile")
    past = [set() for _ in range(8)]
    for vertex in range(1, 8):
        past[vertex].add(0)
    past[7].update(range(1, 7))
    if name.startswith("three_layer_"):
        _, _, direction, mask_text = name.split("_")
        mask = int(mask_text)
        for bit, (left, right) in enumerate(ADJACENT_EDGES):
            if mask & (1 << bit):
                if direction == "reverse":
                    left, right = right, left
                past[right].add(left)
    elif name.startswith("layered_"):
        _, direction, mask_text = name.split("_")
        mask = int(mask_text)
        for i, odd in enumerate((1, 3, 5)):
            for j, even in enumerate((2, 4, 6)):
                if mask & (1 << (3 * i + j)):
                    left, right = (odd, even) if direction == "oe" else (even, odd)
                    past[right].add(left)
    elif name == "chain6":
        for right in range(2, 7):
            past[right].update(range(1, right))
    elif name in EXTRA_RELATIONS:
        for left, right in EXTRA_RELATIONS[name]:
            past[right].add(left)
    else:
        for i in range(3):
            for j in range(3):
                related = i != j if name == "standard_example3" else i <= j
                if related:
                    past[j + 4].add(i + 1)
    # Floyd-style predecessor closure permits both ascending and descending IDs.
    # No generating edge survives as a separate notion in an observation.
    for middle in range(8):
        for right in range(8):
            if middle in past[right]:
                past[right].update(past[middle])
    result = [sorted(row) for row in past]
    _valid_order(list(range(8)), result)
    if result[0] or result[7] != list(range(7)) or any(0 not in row for row in result[1:]):
        raise ValueError("source closure changed the fixed endpoint orientation")
    return result


def source_spec(index):
    """Pure public control hook; generation does not access old artifacts."""
    _integer(index, 0, len(PROFILES) - 1)
    name = PROFILES[index]
    return {
        "profile_index": index,
        "name": name,
        "frame_id": int(index == 3),
        "past": _source(name),
    }


def _feature(state, frame):
    kept, past, eligible = state["kept"], state["past"], frame["eligible"]
    _valid_order(kept, past)
    supports = _supports(kept, past, eligible)
    odd_mask = sum(1 << bit for bit, vertex in enumerate(eligible) if vertex % 2)
    mean, pairs = _summaries(supports, odd_mask)
    motifs = motif_supports(kept, past, eligible)
    paths = path_supports(kept, past, eligible)
    sizes = [sum(vertex in eligible and vertex % 2 == color for vertex in kept) for color in (1, 0)]
    if set(map(tuple, motifs)) & set(map(tuple, paths)):
        raise ValueError("complete and missing-edge motif supports overlap")
    if (
        len(motifs) + len(paths) > comb(sizes[0], 2) * comb(sizes[1], 2)
        or len(motifs) + len(paths) > 9
    ):
        raise ValueError("induced eligible quartet bound failed")
    return {
        "state_id": state["state_id"],
        "color_sizes": sizes,
        "chain_counts": [len(chains) for chains in supports],
        "mean_graded": mean,
        "pair_graded": pairs,
        "motif_supports": motifs,
        "motif_count": len(motifs),
        "path_supports": paths,
        "path_count": len(paths),
    }


def _domain():
    frames = [
        {key: list(value) if type(value) is list else value for key, value in frame.items()}
        for frame in FRAMES
    ]
    profiles, states, features, identities = [], [], [], {}
    aliases = 0
    for index, name in enumerate(PROFILES):
        frame_id = int(index == 3)
        frame = frames[frame_id]
        source_past = _source(name)
        state_ids = []
        for mask in range(1 << len(frame["eligible"])):
            kept = sorted(
                frame["fixed"]
                + [vertex for bit, vertex in enumerate(frame["eligible"]) if mask & (1 << bit)]
            )
            past = _induce(list(range(8)), source_past, kept)
            identity = _state_identity(frame_id, kept, past)
            state_id = identities.get(identity)
            if state_id is None:
                state_id = len(states)
                identities[identity] = state_id
                state = {"state_id": state_id, "frame_id": frame_id, "kept": kept, "past": past}
                states.append(state)
                features.append(_feature(state, frame))
                if len(states) > STATE_CAP:
                    raise ValueError("observed-state resource cap exceeded")
            state_ids.append(state_id)
        profiles.append(
            {
                "profile_index": index,
                "name": name,
                "frame_id": frame_id,
                "past": source_past,
                "state_ids": state_ids,
            }
        )
        aliases += len(state_ids)
        if index == 1029 and (len(states) != 2470 or aliases != 65888):
            raise ValueError("original-family observation/alias prefix changed")
    if len(profiles) != 1542 or aliases != 98656:
        raise ValueError("fixed source or mask-alias inventory changed")
    return {"frames": frames, "profiles": profiles, "states": states}, features, identities


def _fine_rows(domain, features, identities):
    fine, kernels, atoms = [], {}, 0
    for state, feature in zip(domain["states"], features, strict=True):
        frame = domain["frames"][state["frame_id"]]
        present = [vertex for vertex in frame["eligible"] if vertex in state["kept"]]
        transitions = []
        for mask in range(1 << len(present)):
            kept = sorted(
                frame["fixed"] + [vertex for bit, vertex in enumerate(present) if mask & (1 << bit)]
            )
            past = _induce(state["kept"], state["past"], kept)
            identity = _state_identity(state["frame_id"], kept, past)
            if identity not in identities:
                raise ValueError("observed-state domain is not closed under induced restriction")
            target_id = identities[identity]
            target = features[target_id]
            key = (tuple(feature["color_sizes"]), tuple(target["color_sizes"]))
            if key not in kernels:
                kernels[key] = _kernel_polynomial(*key)
            transitions.append({"target_state": target_id, "coefficients": kernels[key]})
        transitions.sort(key=lambda atom: atom["target_state"])
        _normalized(transitions)
        fine.append({"state_id": state["state_id"], "transitions": transitions})
        atoms += len(transitions)
        if atoms > FINE_ATOM_CAP:
            raise ValueError("fine transition resource cap exceeded")
    return fine


def _partition(domain, features):
    identities, vector, groups = {}, [], []
    for state, feature in zip(domain["states"], features, strict=True):
        frame = domain["frames"][state["frame_id"]]
        key = [
            _frame_key(frame),
            feature["pair_graded"],
            feature["motif_count"],
            feature["path_count"],
        ]
        identity = _key(key)
        class_id = identities.get(identity)
        if class_id is None:
            class_id = len(groups)
            identities[identity] = class_id
            groups.append({"class_id": class_id, "key": key, "members": []})
        vector.append(class_id)
        groups[class_id]["members"].append(state["state_id"])
    return {"state_classes": vector, "classes": groups}


def reconstruct():
    """Rebuild the fixed raw universe, observed features and exact fine law."""
    domain, features, identities = _domain()
    fine = _fine_rows(domain, features, identities)
    partition = _partition(domain, features)
    return domain, features, fine, partition


def _closure(partition, pushed):
    maps = [
        {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]}
        for row in pushed
    ]
    zero, witness, comparisons = [[0] * 4 for _ in range(4)], None, 0
    for group in partition["classes"]:
        left_state = group["members"][0]
        left = maps[left_state]
        for right_state in group["members"][1:]:
            comparisons += 1
            right = maps[right_state]
            different = [
                target
                for target in sorted(set(left) | set(right))
                if left.get(target, zero) != right.get(target, zero)
            ]
            if not different or witness is not None:
                continue
            target = different[0]
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
                raise ValueError("nonzero bounded row difference vanished on the exact grid")
            witness = {
                "class_id": group["class_id"],
                "left_state": left_state,
                "right_state": right_state,
                "target_class": target,
                "left_coefficients": left_table,
                "right_coefficients": right_table,
                "first_distinguishing_rates": [str(value) for value in rates],
            }
    if comparisons != len(pushed) - len(partition["classes"]):
        raise ValueError("not every nonrepresentative member was compared")
    quotient, semigroup = [], None
    if witness is None:
        quotient = [
            {
                "class_id": group["class_id"],
                "representative_state": group["members"][0],
                "transitions": pushed[group["members"][0]]["transitions"],
            }
            for group in partition["classes"]
        ]
        semigroup = _semigroup(quotient)
    return (
        {
            "closed": witness is None,
            "classes_checked": len(partition["classes"]),
            "member_comparisons": comparisons,
            "witness": witness,
        },
        quotient,
        semigroup,
    )


def _expected(features, fine):
    for feature, row in zip(features, fine, strict=True):
        actual_m, actual_t = [[0] * 4 for _ in range(4)], [[0] * 4 for _ in range(4)]
        for atom in row["transitions"]:
            child = features[atom["target_state"]]
            _add_table(actual_m, atom["coefficients"], child["motif_count"])
            _add_table(actual_t, atom["coefficients"], child["path_count"])
        for name, table in (("motif_count", actual_m), ("path_count", actual_t)):
            expected = [[0] * 4 for _ in range(4)]
            expected[2][2] = feature[name]
            if table != expected:
                raise ValueError("eligible induced-support expectation identity failed")
    return {
        "motif_cells": 16 * len(features),
        "path_cells": 16 * len(features),
        "max_abs_residual": 0,
    }


def analyze(problem):
    """Compute the prescribed enlarged domain without changing the H summary."""
    _native(problem)
    _fields(problem, ("schema_version", "family"))
    if (
        problem["schema_version"] != "det8-qr05q-problem-v1"
        or problem["family"] != "qr05q_three_layer"
    ):
        raise ValueError("unsupported fixed investigation schema or family")
    domain, features, fine, partition = reconstruct()
    fine_kernel = _audit_fine(domain, fine)
    pushed = _round_pushforwards(fine, partition["state_classes"])
    closure, quotient, semigroup = _closure(partition, pushed)
    expected = _expected(features, fine)
    result = {
        "domain": domain,
        "features": features,
        "partition": partition,
        "fine_kernel": fine_kernel,
        "pushed_rows": pushed,
        "closure": closure,
        "quotient_rows": quotient,
        "semigroup": semigroup,
        "expected_updates": expected,
        "counts": {
            "profiles": len(domain["profiles"]),
            "aliases": sum(len(profile["state_ids"]) for profile in domain["profiles"]),
            "states": len(domain["states"]),
            "classes": len(partition["classes"]),
            "fine_atoms": fine_kernel["transition_atoms"],
            "pushed_atoms": sum(len(row["transitions"]) for row in pushed),
        },
    }
    canonical(result)
    return result
