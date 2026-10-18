"""Independent source-aware nested-partition certifier for QR-05AH.

Own AG native guards are statically carried. Whole-level partitions are
proved by endpoint-arrangement tiles, not area equality alone. Local lineage
combines declared parent containment with complete per-parent sums after all
whole-level partitions have been verified.
"""

import hashlib
import json
import re
from fractions import Fraction as F
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
SCOPE = (
    "observer_has_geometry",
    "marks_authenticated",
    "unknown_geometry_reconstructed",
    "monotone_absolute_error_guaranteed",
    "continuum_limit_established",
    "gravity_derived",
)


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _fields(obj, names, message):
    _require(
        type(obj) is dict and all(type(k) is str for k in obj) and set(obj) == set(names), message
    )


def _string_bytes(value):
    # Exact ensure_ascii=True JSON size without serializing an unbounded tree.
    _require(type(value) is str, "native object key or string")
    _require(len(value) <= MAX_BYTES, "string byte cap")
    count = 2
    for char in value:
        code = ord(char)
        if char in ('"', "\\", "\b", "\t", "\n", "\f", "\r"):
            count += 2
        elif code < 32 or code >= 127:
            count += 6 if code <= 65535 else 12
        else:
            count += 1
        _require(count <= MAX_BYTES, "escaped string byte cap")
    return count


def _native(value):
    # Nodes are JSON values, not object keys. A scalar/empty container has
    # height zero: root depth is zero and deepest scalar leaves count.
    pending, active, complete = [(value, False, 0)], set(), {}

    def scalar(v):
        if v is None:
            return (1, 0, 4)
        if type(v) is bool:
            return (1, 0, 4 if v else 5)
        if type(v) is str:
            return (1, 0, _string_bytes(v))
        if type(v) is int:
            _require(abs(v).bit_length() <= MAX_BITS, "native integer component bit cap")
            return (1, 0, len(str(v)))
        _require(type(v) in (list, dict), "non-native JSON value")
        return None

    while pending:
        current, leaving, depth = pending.pop()
        _require(depth <= MAX_DEPTH, "early native traversal depth cap")
        simple = scalar(current)
        if simple is not None:
            continue
        identity = id(current)
        if leaving:
            children = list(current.values()) if type(current) is dict else current
            nodes, height = 1, 0
            size = 2 + max(0, len(children) - 1)
            if type(current) is dict:
                for key in current:
                    size += _string_bytes(key) + 1
                    _require(size <= MAX_BYTES, "object-key expanded byte cap")
            for child in children:
                info = complete[id(child)] if type(child) in (list, dict) else scalar(child)
                nodes += info[0]
                height = max(height, info[1] + 1)
                size += info[2]
                _require(nodes <= MAX_NODES, "expanded value-node cap")
                _require(height <= MAX_DEPTH, "native depth cap")
                _require(size <= MAX_BYTES, "expanded canonical byte cap")
            _require(
                nodes <= MAX_NODES and height <= MAX_DEPTH and size <= MAX_BYTES,
                "native tree resource cap",
            )
            complete[identity] = (nodes, height, size)
            active.remove(identity)
            continue
        _require(identity not in active, "cyclic JSON container")
        if identity in complete:
            _require(depth + complete[identity][1] <= MAX_DEPTH, "cached subtree depth cap")
            continue
        _require(len(current) + 1 <= MAX_NODES, "container width value-node lower bound")
        if type(current) is dict:
            _require(all(type(key) is str for key in current), "non-native object key")
        active.add(identity)
        pending.append((current, True, depth))
        children = current.values() if type(current) is dict else current
        pending.extend((child, False, depth + 1) for child in children)
    info = complete[id(value)] if type(value) in (list, dict) else scalar(value)
    _require(
        info[0] <= MAX_NODES and info[1] <= MAX_DEPTH and info[2] + 1 <= MAX_BYTES,
        "complete expanded native wire cap",
    )


def _canonical(value):
    try:
        return (
            json.dumps(
                value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, OverflowError, RecursionError, ValueError) as error:
        raise ValueError("canonical JSON serialization failed") from error


def _wire(value):
    _require(type(value) is F, "retained exact rational")
    _require(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) <= MAX_BITS,
        "retained rational bit cap",
    )
    return [value.numerator, value.denominator]


def _fraction(value, positive=False):
    _require(type(value) is list and len(value) == 2, "native rational pair")
    n, d = value
    _require(type(n) is int and type(d) is int and d > 0, "native rational components")
    _require(gcd(n, d) == 1, "reduced fraction")
    _require(max(abs(n).bit_length(), d.bit_length()) <= MAX_BITS, "input rational bits")
    _require(not positive or n > 0, "positive supplied volume")
    return F(n, d)


def _name(value):
    _require(
        type(value) is str and re.fullmatch(r"[a-z][a-z0-9_]{0,39}", value) is not None,
        "bounded native name",
    )
    return value


def _rectangle(value):
    _require(type(value) is list and len(value) == 4, "four-coordinate rectangle")
    rect = [_fraction(v) for v in value]
    _require(rect[0] < rect[1] and rect[2] < rect[3], "strictly positive rectangle widths")
    return rect


def _contained(inner, outer):
    return (
        outer[0] <= inner[0] < inner[1] <= outer[1] and outer[2] <= inner[2] < inner[3] <= outer[3]
    )


def _inside(point, rect):
    return rect[0] < point[0] < rect[1] and rect[2] < point[1] < rect[3]


def _area(rect):
    return (rect[1] - rect[0]) * (rect[3] - rect[2]) / 2


def _partition(domain, cells):
    xs = sorted({domain[0], domain[1], *(v for c in cells for v in c["bounds"][:2])})
    ys = sorted({domain[2], domain[3], *(v for c in cells for v in c["bounds"][2:])})
    for xa, xb in pairwise(xs):
        for ya, yb in pairwise(ys):
            point = ((xa + xb) / 2, (ya + yb) / 2)
            covered = sum(_inside(point, c["bounds"]) for c in cells)
            _require(covered == 1, "every endpoint-arrangement tile covered exactly once")


def _refinement(coarse, fine):
    groups = {cell["name"]: [] for cell in coarse["cells"]}
    for child in fine["cells"]:
        groups[child["parent"]].append(child)
    result = []
    for parent in coarse["cells"]:
        children = groups[parent["name"]]
        _require(bool(children), "each previous parent has children")
        geometric = sum((_area(c["bounds"]) for c in children), F(0))
        supplied = sum((c["volume"] for c in children), F(0))
        _require(geometric == _area(parent["bounds"]), "per-parent geometric coverage")
        _require(supplied == parent["volume"], "per-parent additive supplied marks")
        result.append(
            {
                "parent": parent["name"],
                "children": [c["name"] for c in children],
                "geometric_volume": _wire(geometric),
                "supplied_volume": _wire(supplied),
            }
        )
    return result


def _questions(cells, probes):
    rows = []
    for probe in probes:
        bounds = probe["bounds"]
        inner, outer, representative = [], [], []
        L, U, G, T = F(0), F(0), F(0), F(0)
        for cell in cells:
            rect, point, area = cell["bounds"], cell["representative"], _area(cell["bounds"])
            if _contained(rect, bounds):
                inner.append(cell["name"])
                L += area
            if max(rect[0], bounds[0]) < min(rect[1], bounds[1]) and max(rect[2], bounds[2]) < min(
                rect[3], bounds[3]
            ):
                outer.append(cell["name"])
                U += area
            if _inside(point, bounds):
                representative.append(cell["name"])
                G += area
                T += cell["volume"]
        V, gap = _area(bounds), U - L
        _require(L <= G <= U and L <= V <= U, "both geometric sandwiches")
        _require(G - U <= G - V <= G - L and abs(G - V) <= gap, "signed boundary-error enclosure")
        row = {
            "probe": probe["name"],
            "inner_cells": inner,
            "outer_cells": outer,
            "representative_cells": representative,
        }
        row.update(
            {
                key: _wire(value)
                for key, value in {
                    "lower_bound": L,
                    "upper_bound": U,
                    "boundary_gap": gap,
                    "geometric_target": G,
                    "supplied_target": T,
                    "continuum_volume": V,
                    "annotation_error": T - G,
                    "quadrature_error": G - V,
                    "total_error": T - V,
                    "error_lower": G - U,
                    "error_upper": G - L,
                }.items()
            }
        )
        rows.append(row)
    return rows


def _prepare(problem):
    _native(problem)
    _fields(problem, ("schema_version", "family", "domain", "probes", "levels"), "exact AH input")
    _require(problem["schema_version"] == "det8-qr05ah-problem-v1", "AH schema")
    _require(problem["family"] == "qr05ah_partition_bounds", "AH family")
    domain = _rectangle(problem["domain"])
    raw_probes = problem["probes"]
    _require(type(raw_probes) is list and 1 <= len(raw_probes) <= MAX_PROBES, "bounded probes")
    probes, probe_names = [], set()
    for raw in raw_probes:
        _fields(raw, ("name", "bounds"), "exact probe fields")
        name, bounds = _name(raw["name"]), _rectangle(raw["bounds"])
        _require(name not in probe_names, "unique probe names")
        _require(_contained(bounds, domain), "probe contained in domain")
        probe_names.add(name)
        probes.append({"name": name, "bounds": bounds})
    raw_levels = problem["levels"]
    _require(type(raw_levels) is list and 1 <= len(raw_levels) <= MAX_LEVELS, "bounded levels")
    levels, level_names, previous = [], set(), {}
    for i, raw_level in enumerate(raw_levels):
        _fields(raw_level, ("name", "cells"), "exact level fields")
        name = _name(raw_level["name"])
        _require(name not in level_names, "unique level names")
        level_names.add(name)
        raw_cells = raw_level["cells"]
        _require(
            type(raw_cells) is list and 1 <= len(raw_cells) <= MAX_CELLS, "bounded cells per level"
        )
        cells, names = [], []
        for raw in raw_cells:
            _fields(
                raw, ("name", "parent", "bounds", "representative", "volume"), "exact cell fields"
            )
            cell_name = _name(raw["name"])
            rect = _rectangle(raw["bounds"])
            _require(_contained(rect, domain), "cell contained in domain")
            rep = raw["representative"]
            _require(type(rep) is list and len(rep) == 2, "representative coordinate pair")
            point = [_fraction(v) for v in rep]
            _require(_inside(point, rect), "strict representative interiority")
            volume = _fraction(raw["volume"], positive=True)
            parent = raw["parent"]
            if i == 0:
                _require(parent is None, "first-level parent is null")
            else:
                _require(
                    type(parent) is str and parent in previous, "exact previous-level parent name"
                )
                _require(
                    _contained(rect, previous[parent]["bounds"]),
                    "child contained in its declared parent",
                )
            cells.append(
                {
                    "name": cell_name,
                    "parent": parent,
                    "bounds": rect,
                    "representative": point,
                    "volume": volume,
                }
            )
            names.append(cell_name)
        _require(names == sorted(set(names)), "unique increasing cell names")
        levels.append({"name": name, "cells": cells})
        previous = {c["name"]: c for c in cells}
    sizes, P = [len(level["cells"]) for level in levels], len(probes)
    tile = sum(C * (2 * C + 1) ** 2 for C in sizes)
    pair = sum(C * (C - 1) // 2 for C in sizes)
    query, links = P * sum(sizes), sum(sizes[1:])
    total = tile + pair + 3 * query + links
    _require(tile <= MAX_TILE_CHECKS, "reserved tile checks")
    _require(pair <= MAX_PAIR_CHECKS, "reserved pair checks")
    _require(query <= MAX_QUERY_CELL_TERMS, "reserved query-cell terms")
    _require(total <= MAX_TOTAL_WORK, "reserved total work")
    counts = {
        "levels": len(levels),
        "cells": sum(sizes),
        "probes": P,
        "tile_checks": tile,
        "pair_checks": pair,
        "query_cell_terms": query,
        "refinement_links": links,
        "total_work": total,
    }
    return domain, probes, levels, counts


def certify(problem):
    domain, probes, levels, counts = _prepare(problem)
    raw_input = _canonical(problem)
    for level in levels:
        _partition(domain, level["cells"])
    parents = [_refinement(coarse, fine) for coarse, fine in pairwise(levels)]
    results = []
    for level in levels:
        cells = [
            {
                "name": c["name"],
                "geometric_volume": _wire(_area(c["bounds"])),
                "annotation_error": _wire(c["volume"] - _area(c["bounds"])),
            }
            for c in level["cells"]
        ]
        results.append(
            {"name": level["name"], "cells": cells, "questions": _questions(level["cells"], probes)}
        )
    refinements = []
    for i, (coarse, fine) in enumerate(pairwise(results)):
        questions = []
        for old, new in zip(coarse["questions"], fine["questions"], strict=True):
            a = {
                k: F(*v)
                for k, v in old.items()
                if type(v) is list and len(v) == 2 and all(type(x) is int for x in v)
            }
            b = {
                k: F(*v)
                for k, v in new.items()
                if type(v) is list and len(v) == 2 and all(type(x) is int for x in v)
            }
            differences = {
                "lower_gain": b["lower_bound"] - a["lower_bound"],
                "upper_drop": a["upper_bound"] - b["upper_bound"],
                "gap_drop": a["boundary_gap"] - b["boundary_gap"],
                "quadrature_error_change": b["quadrature_error"] - a["quadrature_error"],
                "absolute_error_change": abs(b["quadrature_error"]) - abs(a["quadrature_error"]),
            }
            _require(
                all(differences[k] >= 0 for k in ("lower_gain", "upper_drop", "gap_drop")),
                "nested enclosure monotonicity",
            )
            questions.append(
                {"probe": old["probe"], **{k: _wire(v) for k, v in differences.items()}}
            )
        refinements.append(
            {
                "coarse": coarse["name"],
                "fine": fine["name"],
                "parents": parents[i],
                "questions": questions,
            }
        )
    result = {
        "input_sha256": hashlib.sha256(raw_input).hexdigest(),
        "domain_volume": _wire(_area(domain)),
        "levels": results,
        "refinements": refinements,
        "counts": counts,
        "scope": dict.fromkeys(SCOPE, False),
    }
    _native(result)
    return json.loads(_canonical(result))
