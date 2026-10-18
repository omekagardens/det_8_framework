"""Exact source-aware certificates for nested supplied rectangle partitions.

This API deliberately sees full geometry and lineage, unlike the retained-order
observer. The native guard is statically carried from this primary's lineage;
no previous or alternative executable implementation is imported.
"""

import hashlib
import json
import re
from fractions import Fraction
from itertools import pairwise
from math import gcd

MAX_BITS = 4096
MAX_DEPTH = 64
MAX_NODES = 131072
MAX_BYTES = 4194304
MAX_LEVELS = 4
MAX_CELLS = 8
MAX_PROBES = 8
MAX_TILE_CHECKS = 9248
MAX_PAIR_CHECKS = 112
MAX_QUERY_CELL_TERMS = 256
MAX_TOTAL_WORK = 12000


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _string_size(value):
    _require(len(value) <= MAX_BYTES, "native string exceeds its byte cap")
    size = 2
    _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    for character in value:
        code = ord(character)
        if character in ('"', "\\") or code in (8, 9, 10, 12, 13):
            size += 2
        elif 32 <= code <= 126:
            size += 1
        elif code <= 65535:
            size += 6
        else:
            size += 12
        _require(size <= MAX_BYTES, "escaped string exceeds its byte cap")
    return size


def _scalar_info(value):
    kind = type(value)
    if value is None:
        return 1, 0, 4
    if kind is bool:
        return 1, 0, 4 if value else 5
    if kind is str:
        return 1, 0, _string_size(value)
    if kind is int:
        _require(value.bit_length() <= MAX_BITS, "native integer exceeds its bit cap")
        return 1, 0, len(str(value))
    raise ValueError("expected exact native JSON value")


def _native(value):
    """Preflight expanded JSON value nodes, root-zero depth and exact bytes."""
    active, completed = set(), {}
    pending = [(value, 0, False)]
    while pending:
        item, depth, leaving = pending.pop()
        _require(depth <= MAX_DEPTH, "native value exceeds depth cap")
        kind = type(item)
        if kind not in (list, dict):
            nodes, height, size = _scalar_info(item)
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native scalar exceeds cap")
            continue
        if leaving:
            active.remove(id(item))
            nodes, height, size = 1, 0, 2 + max(0, len(item) - 1)
            values = item if kind is list else item.values()
            if kind is dict:
                size += sum(_string_size(key) + 1 for key in item)
            for child in values:
                info = completed[id(child)] if type(child) in (list, dict) else _scalar_info(child)
                child_nodes, child_height, child_size = info
                nodes += child_nodes
                height = max(height, child_height + 1)
                size += child_size
                _require(nodes <= MAX_NODES, "expanded native node cap exceeded")
                _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "native container exceeds cap")
            completed[id(item)] = nodes, height, size
            continue
        _require(id(item) not in active, "cyclic native JSON is invalid")
        if id(item) in completed:
            nodes, height, size = completed[id(item)]
            _require(depth + height <= MAX_DEPTH, "shared subtree exceeds depth cap")
            _require(nodes <= MAX_NODES and size + 1 <= MAX_BYTES, "shared subtree exceeds cap")
            continue
        if kind is dict:
            _require(all(type(key) is str for key in item), "object keys must be native strings")
        _require(1 + len(item) <= MAX_NODES, "expanded native node cap exceeded")
        active.add(id(item))
        pending.append((item, depth, True))
        children = item if kind is list else list(item.values())
        pending.extend((child, depth + 1, False) for child in reversed(children))
    if type(value) in (list, dict):
        nodes, height, size = completed[id(value)]
    else:
        nodes, height, size = _scalar_info(value)
    _require(height <= MAX_DEPTH and nodes <= MAX_NODES, "expanded native tree cap exceeded")
    _require(size + 1 <= MAX_BYTES, "expanded canonical byte cap exceeded")
    return size + 1


def canonical(value):
    expected_bytes = _native(value)
    data = (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")
    _require(len(data) == expected_bytes, "canonical size preflight disagrees with serialization")
    _require(len(data) <= MAX_BYTES, "canonical byte cap exceeded")
    return data


def _fields(value, names):
    _require(type(value) is dict and set(value) == set(names), "unexpected object fields")


def _integer(value, minimum, maximum):
    _require(
        type(value) is int and minimum <= value <= maximum and value.bit_length() <= MAX_BITS,
        "native integer outside declared bounds",
    )


def _fraction(value, lower=None, upper=None):
    _require(type(value) is list and len(value) == 2, "expected native reduced fraction pair")
    numerator, denominator = value
    _require(
        type(numerator) is int
        and type(denominator) is int
        and denominator > 0
        and max(numerator.bit_length(), denominator.bit_length()) <= MAX_BITS,
        "invalid native fraction components",
    )
    _require(gcd(numerator, denominator) == 1, "fraction must already be reduced")
    result = Fraction(numerator, denominator)
    _require(
        (lower is None or lower <= result) and (upper is None or result <= upper),
        "fraction outside declared range",
    )
    return result


def _retained(value, lower=None, upper=None):
    _require(
        type(value) is Fraction
        and (lower is None or lower <= value)
        and (upper is None or value <= upper)
        and max(value.numerator.bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational outside range or bit bounds",
    )
    return value


def _pair(value, lower=None, upper=None):
    _retained(value, lower, upper)
    return [value.numerator, value.denominator]


def _name(value):
    _require(
        type(value) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", value) is not None,
        "invalid declared name",
    )
    return value


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "rectangle must have four coordinates")
    result = tuple(_fraction(x) for x in value)
    _require(result[0] < result[1] and result[2] < result[3], "positive rectangle widths required")
    return result


def _contains(outer, inner):
    return (
        outer[0] <= inner[0]
        and inner[1] <= outer[1]
        and outer[2] <= inner[2]
        and inner[3] <= outer[3]
    )


def _interior(bounds, point):
    return bounds[0] < point[0] < bounds[1] and bounds[2] < point[1] < bounds[3]


def _overlaps(left, right):
    return max(left[0], right[0]) < min(left[1], right[1]) and max(left[2], right[2]) < min(
        left[3], right[3]
    )


def _area(bounds):
    # Products and differences are unretained until their final wire fields.
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2]) / 2


def _partition(domain, cells):
    """Authenticate coverage using containment, pairwise interiors and area."""
    for i, cell in enumerate(cells):
        _require(_contains(domain, cell["bounds"]), "cell lies outside partition domain")
        for other in cells[:i]:
            _require(
                not _overlaps(cell["bounds"], other["bounds"]),
                "cell interiors overlap",
            )
    areas = [_area(cell["bounds"]) for cell in cells]
    _require(sum(areas, Fraction(0)) == _area(domain), "cells must cover the domain exactly")
    return areas


def _refinement(coarse, fine):
    """Check each stated parent's children, not only whole-level totals."""
    rows = []
    for parent in coarse:
        children = [cell for cell in fine if cell["parent"] == parent["name"]]
        _require(bool(children), "every previous parent must have children")
        _require(
            all(_contains(parent["bounds"], cell["bounds"]) for cell in children),
            "child lies outside its named parent",
        )
        geometric = sum((cell["geometric"] for cell in children), Fraction(0))
        supplied = sum((cell["volume"] for cell in children), Fraction(0))
        _require(
            geometric == parent["geometric"], "children must geometrically partition their parent"
        )
        _require(supplied == parent["volume"], "supplied marks must be additive per parent")
        # Children are already part of the validated globally disjoint fine
        # partition. Containment and exact area now prove local parent coverage.
        rows.append(
            {
                "parent": parent["name"],
                "children": [cell["name"] for cell in children],
                "geometric_volume": _pair(geometric, 0),
                "supplied_volume": _pair(supplied, 0),
            }
        )
    return rows


def _questions(cells, probes):
    """Compute full-geometry enclosures without treating marks as geometry."""
    result = []
    for probe in probes:
        bounds = probe["bounds"]
        inner = [cell for cell in cells if _contains(bounds, cell["bounds"])]
        outer = [cell for cell in cells if _overlaps(bounds, cell["bounds"])]
        representative = [cell for cell in cells if _interior(bounds, cell["representative"])]
        lower = sum((cell["geometric"] for cell in inner), Fraction(0))
        upper = sum((cell["geometric"] for cell in outer), Fraction(0))
        geometric = sum((cell["geometric"] for cell in representative), Fraction(0))
        supplied = sum((cell["volume"] for cell in representative), Fraction(0))
        continuum = _area(bounds)
        gap = upper - lower
        annotation = supplied - geometric
        quadrature = geometric - continuum
        total = supplied - continuum
        error_lower, error_upper = geometric - upper, geometric - lower
        _require(
            lower <= geometric <= upper and lower <= continuum <= upper,
            "geometric and continuum enclosure failed",
        )
        _require(
            error_lower <= quadrature <= error_upper
            and abs(quadrature) <= gap
            and total == annotation + quadrature,
            "signed boundary certificate failed",
        )
        result.append(
            {
                "probe": probe["name"],
                "inner_cells": [cell["name"] for cell in inner],
                "outer_cells": [cell["name"] for cell in outer],
                "representative_cells": [cell["name"] for cell in representative],
                "lower_bound": _pair(lower, 0),
                "upper_bound": _pair(upper, 0),
                "boundary_gap": _pair(gap, 0),
                "geometric_target": _pair(geometric, 0),
                "supplied_target": _pair(supplied, 0),
                "continuum_volume": _pair(continuum, 0),
                "annotation_error": _pair(annotation),
                "quadrature_error": _pair(quadrature),
                "total_error": _pair(total),
                "error_lower": _pair(error_lower),
                "error_upper": _pair(error_upper),
            }
        )
    return result


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "domain", "probes", "levels"))
    _require(
        problem["schema_version"] == "det8-qr05ah-problem-v1"
        and problem["family"] == "qr05ah_partition_bounds",
        "unknown partition-certificate schema",
    )
    domain = _rectangle(problem["domain"])
    raw_probes = problem["probes"]
    _require(
        type(raw_probes) is list and 1 <= len(raw_probes) <= min(8, MAX_PROBES),
        "probe inventory exceeds live cap",
    )
    probes, probe_names = [], set()
    for raw_probe in raw_probes:
        _fields(raw_probe, ("name", "bounds"))
        name = _name(raw_probe["name"])
        _require(name not in probe_names, "probe names must be unique")
        probe_names.add(name)
        bounds = _rectangle(raw_probe["bounds"])
        _require(_contains(domain, bounds), "probe must be contained in domain")
        probes.append({"name": name, "bounds": bounds})

    raw_levels = problem["levels"]
    _require(
        type(raw_levels) is list and 1 <= len(raw_levels) <= min(4, MAX_LEVELS),
        "level inventory exceeds live cap",
    )
    levels, level_names = [], set()
    previous = None
    for raw_level in raw_levels:
        _fields(raw_level, ("name", "cells"))
        name = _name(raw_level["name"])
        _require(name not in level_names, "level names must be unique")
        level_names.add(name)
        raw_cells = raw_level["cells"]
        _require(
            type(raw_cells) is list and 1 <= len(raw_cells) <= min(8, MAX_CELLS),
            "cell inventory exceeds live cap",
        )
        cells, names = [], []
        for raw_cell in raw_cells:
            _fields(raw_cell, ("name", "parent", "bounds", "representative", "volume"))
            cell_name = _name(raw_cell["name"])
            names.append(cell_name)
            parent = raw_cell["parent"]
            if previous is None:
                _require(parent is None, "initial cells have null parents")
            else:
                _name(parent)
                _require(parent in previous, "parent must name a previous-level cell")
            bounds = _rectangle(raw_cell["bounds"])
            _require(_contains(domain, bounds), "cell must be contained in domain")
            if previous is not None:
                _require(
                    _contains(previous[parent]["bounds"], bounds),
                    "cell must be contained in its declared parent",
                )
            representative = raw_cell["representative"]
            _require(
                type(representative) is list and len(representative) == 2,
                "representative must have two coordinates",
            )
            representative = tuple(_fraction(x) for x in representative)
            _require(
                _interior(bounds, representative),
                "representative must be strictly interior to its cell",
            )
            volume = _fraction(raw_cell["volume"], 0)
            _require(volume > 0, "supplied cell marks must be positive")
            cells.append(
                {
                    "name": cell_name,
                    "parent": parent,
                    "bounds": bounds,
                    "representative": representative,
                    "volume": volume,
                }
            )
        _require(names == sorted(set(names)), "cell names must be unique and sorted")
        levels.append({"name": name, "cells": cells})
        previous = {cell["name"]: cell for cell in cells}

    sizes = [len(level["cells"]) for level in levels]
    C, P = sum(sizes), len(probes)
    T = sum(size * (2 * size + 1) ** 2 for size in sizes)
    D = sum(size * (size - 1) // 2 for size in sizes)
    Q, R = P * C, sum(sizes[1:])
    W = T + D + 3 * Q + R
    for amount, cap, name in (
        (T, MAX_TILE_CHECKS, "tile checks"),
        (D, MAX_PAIR_CHECKS, "pair checks"),
        (Q, MAX_QUERY_CELL_TERMS, "query-cell terms"),
        (W, MAX_TOTAL_WORK, "total work"),
    ):
        _require(amount <= cap, name + " exceed live cap")
    return domain, probes, levels, (C, P, T, D, Q, R, W)


def certify(problem):
    domain, probes, levels, plan = _prepare(problem)
    C, P, T, D, Q, R, W = plan
    input_sha = hashlib.sha256(canonical(problem)).hexdigest()

    # Every global partition and per-parent refinement must be established
    # before the first query. Parsed cells are detached internal objects.
    for level in levels:
        areas = _partition(domain, level["cells"])
        _require(len(areas) == len(level["cells"]), "complete cell-area inventory required")
        for cell, area in zip(level["cells"], areas):
            cell["geometric"] = area
    parent_rows = [_refinement(coarse["cells"], fine["cells"]) for coarse, fine in pairwise(levels)]

    output_levels = []
    for level in levels:
        output_levels.append(
            {
                "name": level["name"],
                "cells": [
                    {
                        "name": cell["name"],
                        "geometric_volume": _pair(cell["geometric"], 0),
                        "annotation_error": _pair(cell["volume"] - cell["geometric"]),
                    }
                    for cell in level["cells"]
                ],
                "questions": _questions(level["cells"], probes),
            }
        )

    refinements = []
    for coarse, fine, parents in zip(output_levels, output_levels[1:], parent_rows):
        changes = []
        for left, right in zip(coarse["questions"], fine["questions"]):

            def value(row, key):
                return Fraction(*row[key])

            lower_gain = value(right, "lower_bound") - value(left, "lower_bound")
            upper_drop = value(left, "upper_bound") - value(right, "upper_bound")
            gap_drop = value(left, "boundary_gap") - value(right, "boundary_gap")
            error_change = value(right, "quadrature_error") - value(left, "quadrature_error")
            absolute_change = abs(value(right, "quadrature_error")) - abs(
                value(left, "quadrature_error")
            )
            _require(
                min(lower_gain, upper_drop, gap_drop) >= 0 and gap_drop == lower_gain + upper_drop,
                "nested enclosure must tighten monotonically",
            )
            changes.append(
                {
                    "probe": left["probe"],
                    "lower_gain": _pair(lower_gain, 0),
                    "upper_drop": _pair(upper_drop, 0),
                    "gap_drop": _pair(gap_drop, 0),
                    "quadrature_error_change": _pair(error_change),
                    "absolute_error_change": _pair(absolute_change),
                }
            )
        refinements.append(
            {
                "coarse": coarse["name"],
                "fine": fine["name"],
                "parents": parents,
                "questions": changes,
            }
        )
    result = {
        "input_sha256": input_sha,
        "domain_volume": _pair(_area(domain), 0),
        "levels": output_levels,
        "refinements": refinements,
        "counts": {
            "levels": len(levels),
            "cells": C,
            "probes": P,
            "tile_checks": T,
            "pair_checks": D,
            "query_cell_terms": Q,
            "refinement_links": R,
            "total_work": W,
        },
        "scope": {
            "observer_has_geometry": False,
            "marks_authenticated": False,
            "unknown_geometry_reconstructed": False,
            "monotone_absolute_error_guaranteed": False,
            "continuum_limit_established": False,
            "gravity_derived": False,
        },
    }
    return json.loads(canonical(result))
