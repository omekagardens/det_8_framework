"""QR-05R direct nonnegative subset-census executor.

Local primary P/Q utilities reconstruct observed chains, pair unions, motifs
and binomial fine laws from the explicit raw model. No external artifact,
source generator, previous executor or mutable hidden input is read.
The direct integer census, basis conversion and nested counts are distinct
checks; profile closure is evaluated without importing the prior outcome.
"""

import hashlib
import json
import re
from fractions import Fraction
from itertools import combinations, product
from math import comb

BIT_LIMIT = 4096
STATE_CAP = 4447
FINE_ATOM_CAP = 168388
WORKING_CAP = 512 * 1024 * 1024
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


def reconstruct(model):
    """Validate the explicit raw domain and rebuild all observation-derived data.

    Returns (features, fine_rows, partition); it never reads a prior artifact.
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
    identities, vector, groups = {}, [], []
    for state, feature in zip(states, features, strict=True):
        key = [
            _frame_key(frames[state["frame_id"]]),
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
        groups[class_id]["members"].append(state["state_id"])
        vector.append(class_id)
    return features, fine_rows, {"state_classes": vector, "classes": groups}


def _choose(total, selected):
    return comb(total, selected) if total >= 0 and 0 <= selected <= total else 0


def _colors(value):
    if type(value) is not list or len(value) != 2:
        raise ValueError("color sizes must be two native integers")
    for size in value:
        _integer(size, 0, 3)
    return tuple(value)


def expand_grade_table(grades, parent_color_sizes):
    """Expand all grades, including zero cells, in the unnormalized basis."""
    _native(grades)
    _table(grades)
    parent = _colors(parent_color_sizes)
    power = [[0] * 4 for _ in range(4)]
    for odd in range(4):
        for even in range(4):
            value = grades[odd][even]
            if odd > parent[0] or even > parent[1]:
                if value:
                    raise ValueError("grade lies outside the parent color degree")
                continue
            if not value:
                continue
            _add_table(power, _kernel_polynomial(parent, (odd, even)), value)
    _table(power)
    return power


def inverse_basis(power_coefficients, parent_color_sizes):
    """Invert the finite triangular tensor transform with zero padding."""
    _native(power_coefficients)
    _table(power_coefficients)
    odd_total, even_total = _colors(parent_color_sizes)
    for i in range(4):
        for j in range(4):
            if (i > odd_total or j > even_total) and power_coefficients[i][j]:
                raise ValueError("power coefficient exceeds the fixed parent degree")
    grades = [[0] * 4 for _ in range(4)]
    for odd in range(odd_total + 1):
        for even in range(even_total + 1):
            grades[odd][even] = sum(
                power_coefficients[i][j]
                * _choose(odd_total - i, odd - i)
                * _choose(even_total - j, even - j)
                for i in range(odd + 1)
                for j in range(even + 1)
            )
    _table(grades)
    return grades


def _validate_row(payload):
    _native(payload)
    _fields(payload, ("parent_color_sizes", "transitions"))
    parent = _colors(payload["parent_color_sizes"])
    transitions = payload["transitions"]
    if type(transitions) is not list or not 1 <= len(transitions) <= 64:
        raise ValueError("a sparse row must have one to sixty-four atoms")
    previous = -1
    totals = [[0] * 4 for _ in range(4)]
    for atom in transitions:
        _fields(atom, ("target_class", "retained_color_sizes", "multiplicity"))
        _integer(atom["target_class"], previous + 1, STATE_CAP - 1)
        previous = atom["target_class"]
        rank = _colors(atom["retained_color_sizes"])
        if any(child > full for child, full in zip(rank, parent, strict=True)):
            raise ValueError("retained color size exceeds its parent")
        rank_count = _choose(parent[0], rank[0]) * _choose(parent[1], rank[1])
        _integer(atom["multiplicity"], 1, min(9, rank_count))
        totals[rank[0]][rank[1]] += atom["multiplicity"]
    for odd in range(4):
        for even in range(4):
            if totals[odd][even] != _choose(parent[0], odd) * _choose(parent[1], even):
                raise ValueError("profile is not normalized at each retained rank")
    return parent


def _parse_rates(rates):
    if type(rates) is not list or len(rates) != 2:
        raise ValueError("rates must be two canonical native rational strings")
    result = []
    for value in rates:
        if (
            type(value) is not str
            or len(value) > 3000
            or re.fullmatch(r"(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value) is None
        ):
            raise ValueError("rate must have bounded unsigned integer/fraction syntax")
        parsed = Fraction(value)
        if str(parsed) != value or not 0 <= parsed <= 1:
            raise ValueError("rate must be reduced, canonical and in the closed unit interval")
        _bounded_fraction(parsed)
        result.append(parsed)
    return tuple(result)


def _bounded_fraction(value):
    if max(value.numerator.bit_length(), value.denominator.bit_length()) > BIT_LIMIT:
        raise ValueError("exact rational exceeds the arithmetic bound")
    return value


def _basis_value(parent, rank, rates, cache):
    key = (parent, rank, rates)
    if key not in cache:
        x, y = rates
        cache[key] = (
            x ** rank[0]
            * (1 - x) ** (parent[0] - rank[0])
            * y ** rank[1]
            * (1 - y) ** (parent[1] - rank[1])
        )
    return cache[key]


def _row_evaluation(payload, rates, parsed, cache):
    parent = tuple(payload["parent_color_sizes"])
    outcomes, total = [], Fraction(0)
    for atom in payload["transitions"]:
        rank = tuple(atom["retained_color_sizes"])
        probability = _bounded_fraction(
            atom["multiplicity"] * _basis_value(parent, rank, parsed, cache)
        )
        if probability < 0:
            raise ValueError("nonnegative profile produced a negative probability")
        total = _bounded_fraction(total + probability)
        outcomes.append({"target_class": atom["target_class"], "probability": str(probability)})
    if total != 1:
        raise ValueError("profile probabilities do not normalize")
    return {"rates": list(rates), "outcomes": outcomes}


def evaluate_row(payload, rates):
    """Evaluate a validated sparse count row without any observation lookup.

    The row cannot authenticate target H labels or initial-domain membership.
    Validation is performed afresh; returned containers do not alias inputs.
    """
    _validate_row(payload)
    parsed = _parse_rates(rates)
    return _row_evaluation(payload, rates, parsed, {})


def _profiles(features, fine, partition):
    class_sizes = []
    for group in partition["classes"]:
        representative = features[group["members"][0]]
        parent = representative["color_sizes"]
        for state_id in group["members"]:
            feature = features[state_id]
            recovered = [feature["pair_graded"][0][1][1][0], feature["pair_graded"][0][1][0][1]]
            if recovered != feature["color_sizes"] or recovered != parent:
                raise ValueError("H does not fix the raw parent color rank")
        class_sizes.append(parent)
    profiles = []
    for feature, row in zip(features, fine, strict=True):
        counts = {}
        for atom in row["transitions"]:
            target_id = atom["target_state"]
            target = partition["state_classes"][target_id]
            if features[target_id]["color_sizes"] != class_sizes[target]:
                raise ValueError("successor H class has inconsistent color rank")
            # Every fine atom is one observed eligible subset, not an alias.
            counts[target] = counts.get(target, 0) + 1
        transitions = [
            {
                "target_class": target,
                "retained_color_sizes": list(class_sizes[target]),
                "multiplicity": counts[target],
            }
            for target in sorted(counts)
        ]
        payload = {"parent_color_sizes": list(feature["color_sizes"]), "transitions": transitions}
        _validate_row(payload)
        profiles.append({"state_id": feature["state_id"], **payload})
    return profiles


def _profile_domain(partition, profiles):
    """Validate the finite profile partition, including global target ranks."""
    _native(partition)
    _native(profiles)
    _fields(partition, ("state_classes", "classes"))
    if type(profiles) is not list or not 1 <= len(profiles) <= STATE_CAP:
        raise ValueError("invalid finite profile domain")
    vector, groups = partition["state_classes"], partition["classes"]
    if (
        type(vector) is not list
        or len(vector) != len(profiles)
        or type(groups) is not list
        or not groups
    ):
        raise ValueError("profile partition has a different domain")
    seen, sizes = [], []
    for class_id, group in enumerate(groups):
        _fields(group, ("class_id", "key", "members"))
        _integer(group["class_id"], class_id, class_id)
        members = group["members"]
        if type(members) is not list or not members:
            raise ValueError("partition has an empty class")
        previous = -1
        for state_id in members:
            _integer(state_id, previous + 1, len(profiles) - 1)
            previous = state_id
            _integer(vector[state_id], class_id, class_id)
            seen.append(state_id)
        if class_id and groups[class_id - 1]["members"][0] >= members[0]:
            raise ValueError("classes are not in first-occurrence order")
        sizes.append(_colors(profiles[members[0]]["parent_color_sizes"]))
    if sorted(seen) != list(range(len(profiles))):
        raise ValueError("partition members do not cover each state exactly once")
    for state_id, profile in enumerate(profiles):
        _fields(profile, ("state_id", "parent_color_sizes", "transitions"))
        _integer(profile["state_id"], state_id, state_id)
        parent = _validate_row({key: profile[key] for key in ("parent_color_sizes", "transitions")})
        if parent != sizes[vector[state_id]]:
            raise ValueError("an H fiber has differing parent color ranks")
        for atom in profile["transitions"]:
            target = atom["target_class"]
            if target >= len(groups) or tuple(atom["retained_color_sizes"]) != sizes[target]:
                raise ValueError("target H class has the wrong retained color rank")
    return sizes


def closure_from_profiles(profiles, partition):
    """Check every fiber and retain only its canonical first obstruction."""
    _profile_domain(partition, profiles)
    maps = [{atom["target_class"]: atom for atom in row["transitions"]} for row in profiles]
    witness, comparisons = None, 0
    for group in partition["classes"]:
        left_state = group["members"][0]
        left = maps[left_state]
        for right_state in group["members"][1:]:
            comparisons += 1
            right = maps[right_state]
            differences = [
                target
                for target in sorted(set(left) | set(right))
                if left.get(target, {}).get("multiplicity", 0)
                != right.get(target, {}).get("multiplicity", 0)
            ]
            if not differences or witness is not None:
                continue
            target = differences[0]
            rank = (left.get(target) or right[target])["retained_color_sizes"]
            left_count = left.get(target, {}).get("multiplicity", 0)
            right_count = right.get(target, {}).get("multiplicity", 0)
            parent = tuple(profiles[left_state]["parent_color_sizes"])
            rates = next(
                (
                    rates
                    for rates in GRID
                    if (left_count - right_count) * _basis_value(parent, tuple(rank), rates, {})
                    != 0
                ),
                None,
            )
            if rates is None:
                raise ValueError("a count obstruction disappeared on the exact degree grid")
            witness = {
                "class_id": group["class_id"],
                "left_state": left_state,
                "right_state": right_state,
                "target_class": target,
                "retained_color_sizes": list(rank),
                "left_multiplicity": left_count,
                "right_multiplicity": right_count,
                "first_distinguishing_rates": [str(value) for value in rates],
            }
    if comparisons != len(profiles) - len(partition["classes"]):
        raise ValueError("closure did not scan all nonrepresentative members")
    return {
        "closed": witness is None,
        "classes_checked": len(partition["classes"]),
        "member_comparisons": comparisons,
        "witness": witness,
    }


def _composition(class_profiles):
    rows = []
    totals = {"final_targets": 0, "rank_cells": 0, "nested_pairs": 0, "max_abs_residual": 0}
    for profile in class_profiles:
        parent = profile["parent_color_sizes"]
        one = {atom["target_class"]: atom for atom in profile["transitions"]}
        nested = {}
        for first in profile["transitions"]:
            odd, even = first["retained_color_sizes"]
            middle = class_profiles[first["target_class"]]
            for second in middle["transitions"]:
                target = second["target_class"]
                cells = nested.setdefault(target, [[0] * 4 for _ in range(4)])
                cells[odd][even] += first["multiplicity"] * second["multiplicity"]
        if set(nested) != set(one):
            raise ValueError("one/two-step structural targets differ")
        for target, table in nested.items():
            final = one[target]
            odd_final, even_final = final["retained_color_sizes"]
            for odd in range(4):
                for even in range(4):
                    expected = (
                        final["multiplicity"]
                        * _choose(parent[0] - odd_final, odd - odd_final)
                        * _choose(parent[1] - even_final, even - even_final)
                    )
                    if table[odd][even] != expected:
                        raise ValueError("nested-subset superset identity failed")
        nested_pairs = sum(value for table in nested.values() for row in table for value in row)
        if nested_pairs != 3 ** sum(parent):
            raise ValueError("nested subset inventory is not three to the eligible count")
        counts = {
            "class_id": profile["class_id"],
            "final_targets": len(nested),
            "rank_cells": 16 * len(nested),
            "nested_pairs": nested_pairs,
            "max_abs_residual": 0,
        }
        rows.append(counts)
        for name in ("final_targets", "rank_cells", "nested_pairs"):
            totals[name] += counts[name]
    return {"verified": True, "rows": rows, "totals": totals}


def _closure(partition, profiles):
    closure = closure_from_profiles(profiles, partition)
    if not closure["closed"]:
        return closure, [], None
    class_profiles = []
    for group in partition["classes"]:
        representative = group["members"][0]
        row = profiles[representative]
        class_profiles.append(
            {
                "class_id": group["class_id"],
                "representative_state": representative,
                "parent_color_sizes": list(row["parent_color_sizes"]),
                "transitions": [
                    {
                        "target_class": atom["target_class"],
                        "retained_color_sizes": list(atom["retained_color_sizes"]),
                        "multiplicity": atom["multiplicity"],
                    }
                    for atom in row["transitions"]
                ],
            }
        )
    return closure, class_profiles, _composition(class_profiles)


def _conversion(profiles, fine, partition, class_profiles):
    pushed = _round_pushforwards(fine, partition["state_classes"])
    atoms = 0
    for profile, row in zip(profiles, pushed, strict=True):
        powers = {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]}
        targets = [atom["target_class"] for atom in profile["transitions"]]
        if targets != sorted(powers):
            raise ValueError("profile and power laws have different structural targets")
        for atom in profile["transitions"]:
            rank = atom["retained_color_sizes"]
            grades = [[0] * 4 for _ in range(4)]
            grades[rank[0]][rank[1]] = atom["multiplicity"]
            coefficients = expand_grade_table(grades, profile["parent_color_sizes"])
            if coefficients != powers[atom["target_class"]]:
                raise ValueError("direct count expansion differs from summed fine powers")
            if inverse_basis(powers[atom["target_class"]], profile["parent_color_sizes"]) != grades:
                raise ValueError("complete inverse grade table differs from direct census")
            atoms += 1
    quotient = None
    if class_profiles:
        quotient = []
        for profile in class_profiles:
            transitions = []
            for atom in profile["transitions"]:
                grades = [[0] * 4 for _ in range(4)]
                odd, even = atom["retained_color_sizes"]
                grades[odd][even] = atom["multiplicity"]
                transitions.append(
                    {
                        "target_class": atom["target_class"],
                        "coefficients": expand_grade_table(grades, profile["parent_color_sizes"]),
                    }
                )
            if transitions != pushed[profile["representative_state"]]["transitions"]:
                raise ValueError("class count conversion differs from its representative law")
            quotient.append(
                {
                    "class_id": profile["class_id"],
                    "representative_state": profile["representative_state"],
                    "transitions": transitions,
                }
            )
    return {
        "fine_kernel_sha256": _digest(fine),
        "pushed_rows_sha256": _digest(pushed),
        "quotient_rows_sha256": _digest(quotient) if quotient is not None else None,
        "profile_cells": 16 * atoms,
        "power_cells": 16 * atoms,
        "normalization_cells": 16 * len(profiles),
        "max_abs_residual": 0,
    }, pushed


def _evaluation(profiles, pushed):
    basis_cache, power_cache = {}, {}
    evaluations, normalizations = 0, 0
    for profile, row in zip(profiles, pushed, strict=True):
        powers = {atom["target_class"]: atom["coefficients"] for atom in row["transitions"]}
        parent = tuple(profile["parent_color_sizes"])
        for rates in RATES:
            total = Fraction(0)
            for atom in profile["transitions"]:
                rank = tuple(atom["retained_color_sizes"])
                direct = _bounded_fraction(
                    atom["multiplicity"] * _basis_value(parent, rank, rates, basis_cache)
                )
                converted = _evaluated(powers[atom["target_class"]], rates, power_cache)
                if direct < 0 or direct != converted:
                    raise ValueError("direct nonnegative evaluation differs from power law")
                total = _bounded_fraction(total + direct)
                evaluations += 1
            if total != 1:
                raise ValueError("profile probability row does not normalize at an audit rate")
            normalizations += 1
    atoms = sum(len(row["transitions"]) for row in profiles)
    return {
        "rate_points": len(RATES),
        "profile_atoms": atoms,
        "probability_evaluations": evaluations,
        "normalization_rows": normalizations,
        "max_abs_residual": 0,
    }


def analyze(problem):
    """Count the explicit observation-domain law and certify its finite interface."""
    _native(problem)
    _fields(problem, ("schema_version", "family", "model"))
    if (
        problem["schema_version"] != "det8-qr05r-problem-v1"
        or problem["family"] != "qr05r_deletion_profile"
    ):
        raise ValueError("unsupported fixed investigation schema or family")
    features, fine, partition = reconstruct(problem["model"])
    profiles = _profiles(features, fine, partition)
    closure, class_profiles, composition = _closure(partition, profiles)
    conversion, pushed = _conversion(profiles, fine, partition, class_profiles)
    evaluation = _evaluation(profiles, pushed)
    result = {
        "model_sha256": _digest(problem["model"]),
        "features": features,
        "partition": partition,
        "profiles": profiles,
        "closure": closure,
        "class_profiles": class_profiles,
        "conversion": conversion,
        "composition": composition,
        "evaluation": evaluation,
        "counts": {
            "states": len(features),
            "classes": len(partition["classes"]),
            "fine_atoms": sum(len(row["transitions"]) for row in fine),
            "profile_atoms": sum(len(row["transitions"]) for row in profiles),
            "class_profile_atoms": sum(len(row["transitions"]) for row in class_profiles),
        },
    }
    canonical(result)
    return result
