#!/usr/bin/env python3
"""RI-88: bounded exact verifier for the accepted RI-85 four-cap design.

Source preparation is not execution evidence. A separately authorized run
replays only the pinned RI-74/RI-63 actual prefix and queries precisely the
40 specified held rows. No numerical q6/q7, a6/M6, optimizer, global order
inventory, all-size transform, subprocess, download or file write is used.
The structural domain is the natural-isomorphism closure of the eleven
children, five parents, their 43 forward extensions and four held orders.
Every parent natural relabeling transports all 64 records and every ideal;
generic factor products are recomputed on the transported order itself.
The 120-second/512-MiB checks supplement a separately frozen external sampled
watchdog; they are not an allocator-hard-cap or measured-performance claim.
RI-84 is a read-only source pattern, not an imported runtime dependency.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import json
import resource
import runpy
import signal
import sys
import time


PINS = {
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
DESIGN_SHA256 = 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a'
C3, C4, C5, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 7)
HELD = (C3, C4, C5, H5)
HELD_RECORDS = (8, 8, 16, 8)
CAPS = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 3), (0, 0, 1, 1),
        (0, 0, 1, 2), (0, 0, 1, 3), (0, 0, 1, 5), (0, 0, 3, 3),
        (0, 1, 1, 1), (0, 1, 1, 3), (0, 1, 3, 3))
SUPPORT = tuple(C3+tuple(7+8*p for p in cap) for cap in CAPS)
WIDTHS = (4, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2)
PARENTS = ((0, 1, 3, 7, 7, 7), (0, 1, 3, 7, 7, 15), (0, 1, 3, 7, 7, 31),
           (0, 1, 3, 7, 15, 15), (0, 1, 3, 7, 15, 31))
IDEALS = ((0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63), (0, 1, 3, 7, 15, 23, 31, 47, 63),
          (0, 1, 3, 7, 15, 23, 31, 63), (0, 1, 3, 7, 15, 31, 47, 63), (0, 1, 3, 7, 15, 31, 63))
FORWARD = ({7: 0, 15: 1, 23: 1, 39: 1, 31: 2, 47: 2, 55: 2},
           {7: 1, 15: 3, 23: 4, 31: 5, 47: 6}, {7: 2, 15: 5, 23: 5, 31: 7},
           {7: 3, 15: 8, 31: 9, 47: 9}, {7: 6, 15: 9, 31: 10})
# Entries are (deleted full vertex, zero-based parent index), not forward weights.
DELETIONS = (((3, 0), (4, 0), (5, 0), (6, 0)), ((4, 1), (5, 1), (6, 0)),
             ((5, 2), (6, 0)), ((4, 3), (5, 1), (6, 1)), ((5, 1), (6, 1)),
             ((5, 2), (6, 1)), ((4, 4), (6, 1)), ((5, 2), (6, 2)),
             ((4, 3), (5, 3), (6, 3)), ((5, 4), (6, 3)), ((5, 4), (6, 4)))
MAX_SECONDS, MAX_BYTES = 120, 512*1024**2
START, PREFIX = None, None
CANONICAL, DEPENDENCY_PATHS = {}, {}


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def integer(value, low, high, reason):
    require(type(value) is int and low <= value <= high, reason)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS, '120-second verification envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_BYTES, '512-MiB resident-memory envelope exceeded')
    if stage:
        print('RI88: '+stage, file=sys.stderr, flush=True)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def load_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON object key')
            result[key] = value
        return result
    def bad(value):
        raise RuntimeError('JSON decimals and nonfinite constants are forbidden')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=bad, parse_constant=bad)


def copy_json(value):
    return load_json(canonical(value))


def fraction(value):
    require(type(value) is str, 'noncanonical rational encoding')
    try:
        result = F(value)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError('noncanonical rational encoding') from None
    require(str(result) == value, 'noncanonical rational encoding')
    return result


def encoded(matrix):
    return [[str(value) for value in row] for row in matrix]


def strict_shape(value, reference):
    require(type(value) is type(reference), 'certificate value type mismatch')
    if type(reference) is dict:
        require(set(value) == set(reference), 'certificate object fields mismatch')
        for key in reference:
            strict_shape(value[key], reference[key])
    elif type(reference) is list:
        require(len(value) == len(reference), 'certificate list coverage mismatch')
        for item, expected in zip(value, reference):
            strict_shape(item, expected)


def verify_certificate(saved, expected):
    strict_shape(saved, expected)
    require(saved['schema'] == 'ri88-four-vertex-cap-v1', 'certificate schema mismatch')
    require(canonical(saved) == canonical(expected), 'certificate finite witness mismatch')


def check_pin(raw, pin):
    require(sha256(raw).hexdigest() == pin, 'accepted dependency byte pin mismatch')


def bits(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


def validate_order(order):
    require(type(order) is tuple and 0 < len(order) <= 7
            and all(type(p) is int and 0 <= p < (1 << i) for i, p in enumerate(order)),
            'invalid bounded natural order or exact mask type')
    require(all(all(order[i] & past == order[i] for i in bits(past)) for past in order),
            'order is not transitively closed')


def seeds():
    return frozenset(HELD+PARENTS+SUPPORT+tuple(p+(s,) for p, parts in zip(PARENTS, IDEALS) for s in parts))


def validate_permutation(permutation, n):
    integer(n, 1, 7, 'permutation dimension outside frozen exact bounds')
    require(type(permutation) is tuple and len(permutation) == n
            and all(type(i) is int for i in permutation) and sorted(permutation) == list(range(n)),
            'invalid permutation or exact vertex type')


def transport(mask, permutation):
    validate_permutation(permutation, len(permutation) if type(permutation) is tuple else 0)
    integer(mask, 0, (1 << len(permutation))-1, 'invalid transport mask or exact integer type')
    return sum(1 << permutation[i] for i in bits(mask))


def restrict_mask(mask, vertices, n):
    integer(n, 1, 7, 'restriction dimension outside frozen exact bounds')
    integer(mask, 0, (1 << n)-1, 'invalid restricted record or precursor mask')
    require(type(vertices) is tuple and all(type(i) is int and 0 <= i < n for i in vertices)
            and tuple(sorted(set(vertices))) == vertices, 'invalid induced vertex list')
    return sum(((mask >> old) & 1) << new for new, old in enumerate(vertices))


def induce(order, keep):
    validate_order(order)
    integer(keep, 1, (1 << len(order))-1, 'invalid induced-suborder keep mask')
    vertices = bits(keep)
    result = tuple(restrict_mask(order[v], vertices, len(order)) for v in vertices)
    validate_order(result)
    return result, vertices


def maxima(order):
    validate_order(order)
    pasts = 0
    for p in order:
        pasts |= p
    return bits(((1 << len(order))-1) ^ pasts)


def natural_relabelings(order):
    validate_order(order)  # Exact nested guards precede membership/cache.
    require(order in seeds(), 'canonicalization seed outside frozen domain')
    return _natural_relabelings(order)


@cache
def _natural_relabelings(order):
    result = []
    for sequence in permutations(range(len(order))):
        seen = 0
        for vertex in sequence:
            if order[vertex] & seen != order[vertex]:
                break
            seen |= 1 << vertex
        else:
            permutation = tuple(sequence.index(v) for v in range(len(order)))
            image = tuple(transport(order[v], permutation) for v in sequence)
            validate_order(image)
            result.append((permutation, image))
    require(result, 'selected order has no natural relabeling')
    return tuple(result)


def canonical_key(order):
    validate_order(order)
    require(order in CANONICAL, 'order outside declared structural isomorphism closure')
    return CANONICAL[order]


def ideals(order):
    validate_order(order)
    require(order in seeds() or order in CANONICAL, 'ideal enumeration outside frozen structural domain')
    return _ideals(order)


@cache
def _ideals(order):
    return tuple(s for s in range(1 << len(order)) if all(order[v] & s == order[v] for v in bits(s)))


def support_index(order):
    key = canonical_key(order)
    return SUPPORT.index(key) if key in SUPPORT else None


def intrinsic_width(order):
    require(support_index(order) is not None, 'width evaluation outside supported child classes')
    return max(s.bit_count() for s in range(1 << len(order)) if all(not order[v] & s for v in bits(s)))


def verify_support(support, widths):
    require(type(support) is tuple and len(support) == 11, 'frozen support shape changed')
    for order in support:
        validate_order(order)
    require(support == SUPPORT, 'support classes or variable order changed')
    require(type(widths) is tuple and all(type(w) is int for w in widths) and widths == WIDTHS,
            'intrinsic cap widths changed')


def verify_deletions(rows):
    require(type(rows) is list and all(type(row) is dict for row in rows), 'invalid deletion-role container')
    for row in rows:
        integer(row['support_index'], 0, 10, 'invalid exact deletion support index')
        integer(row['deleted_vertex'], 3, 6, 'invalid exact deleted vertex')
        integer(row['parent_index'], 0, 4, 'invalid exact deletion parent index')
    expected = [(j, v, i) for j, items in enumerate(DELETIONS) for v, i in items]
    require([(r['support_index'], r['deleted_vertex'], r['parent_index']) for r in rows] == expected,
            'maximal-deletion closure or role multiplicity mismatch')


def verify_forward(rows):
    require(type(rows) is list and all(type(row) is dict for row in rows), 'invalid forward-slot container')
    for row in rows:
        integer(row['parent_index'], 0, 4, 'invalid exact forward parent index')
        integer(row['ideal'], 0, 63, 'invalid exact forward ideal')
        require(row['support_index'] is None or type(row['support_index']) is int
                and 0 <= row['support_index'] < 11, 'invalid exact forward support index')
    expected = [(i, s, FORWARD[i].get(s)) for i in range(5) for s in IDEALS[i]]
    require([(r['parent_index'], r['ideal'], r['support_index']) for r in rows] == expected,
            'forward individual-ideal coverage or support classification mismatch')


def build_structure():
    verify_support(SUPPORT, WIDTHS)
    classes = []
    for order in sorted(seeds()):
        budget()
        relabelings = natural_relabelings(order)
        images = sorted(set(image for _, image in relabelings))
        key = min(images)
        for image in images:
            require(image not in CANONICAL or CANONICAL[image] == key, 'inconsistent canonical structural class')
            CANONICAL[image] = key
        classes.append(dict(order=order, canonical=key, natural_images=images,
                            topological_relabelings=[dict(permutation=p, image=q) for p, q in relabelings]))
    require(tuple(canonical_key(t) for t in SUPPORT) == SUPPORT, 'support representatives are not canonical')
    require(tuple(canonical_key(p) for p in PARENTS) == PARENTS, 'parent representatives are not canonical')
    verify_support(SUPPORT, tuple(intrinsic_width(t) for t in SUPPORT))
    deletions, forward = [], []
    for j, target in enumerate(SUPPORT):
        for v in maxima(target):
            parent, vertices = induce(target, 127 ^ (1 << v))
            key = canonical_key(parent)
            require(key in PARENTS, 'supported maximal deletion escaped parent closure')
            deletions.append(dict(support_index=j, deleted_vertex=v, kept_vertices=vertices,
                                  induced_parent=parent, canonical_parent=key, parent_index=PARENTS.index(key)))
    verify_deletions(deletions)
    for i, parent in enumerate(PARENTS):
        require(ideals(parent) == IDEALS[i], 'complete parent ideal list mismatch')
        for s in ideals(parent):
            child = parent+(s,)
            forward.append(dict(parent_index=i, ideal=s, child=child, canonical_child=canonical_key(child),
                                support_index=support_index(child)))
    verify_forward(forward)
    return dict(ordered_support=[dict(index=j, cap=CAPS[j], order=t, width=WIDTHS[j]) for j, t in enumerate(SUPPORT)],
                parent_orders=PARENTS, canonicalizations=classes, maximal_deletions=deletions, forward_slots=forward)


def verify_actual_prefix(report):
    require(report['problem_sha256'] == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and report['actual_probability_manifest_sha256'] == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and type(report['canonical_lex_stages']) is int and report['canonical_lex_stages'] == 69
            and len(report['inherited_controls']) == 15, 'accepted actual strict prefix identity mismatch')


def rebuild_prefix():
    global PREFIX, DEPENDENCY_PATHS
    directory = Path(__file__).resolve().parent.parent
    paths = dict(ri74_checker=directory/'native_growth_plancherel_graft_v1'/'check.py',
                 ri63_checker=directory/'native_growth_expected_defect_completion_v1'/'check.py',
                 ri63_certificate=directory/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
                 ri41_certificate=directory/'native_growth_height_normalization_v1'/'CERTIFICATE.json')
    for key, path in paths.items():
        check_pin(path.read_bytes(), PINS[key])
    DEPENDENCY_PATHS = paths
    budget('four dependencies pinned; replaying accepted actual strict prefix')
    module = runpy.run_path(str(paths['ri74_checker']))
    PREFIX = module['prefix_row']
    wrapped = getattr(PREFIX, '__wrapped__', None)
    require(wrapped is not None and hasattr(wrapped, '__globals__')
            and wrapped.__globals__ is module['rebuild_prefix'].__globals__, 'cached prefix helper globals disagree')
    report = module['rebuild_prefix']()
    require(wrapped.__globals__['HELPER'] is not None and len(wrapped.__globals__['Q5']) == 2961,
            'actual strict q5 helper state not populated')
    verify_actual_prefix(report)
    budget('accepted prefix replay complete; exactly forty held queries are permitted')
    return report


def verify_held_row(order, row):
    require(type(row) is dict and all(type(s) is int for s in row) and set(row) == set(ideals(order))
            and all(type(q) is F and q > 0 for q in row.values()) and sum(row.values(), F(0)) == 1,
            'held row lost exact labeled ideals or strict normalization')


def held_row(order, record):
    validate_order(order)
    require(len(order) < 6, 'q6 or q7 probability lookup forbidden')
    require(order in HELD, 'held parent outside frozen four-class domain')
    integer(record, 0, (1 << len(order))-1, 'held record is not an exact in-range integer')
    require(record < HELD_RECORDS[HELD.index(order)], 'unapproved held top-mark query')
    require(PREFIX is not None, 'accepted prefix not initialized')
    row = PREFIX(order, record)
    verify_held_row(order, row)
    return dict(row)


def forbidden_scale(name):
    require(name not in ('a6', 'M6', 'q6', 'q7'), 'numerical future law or global scale forbidden')
    raise RuntimeError('unknown global-scale request')


def verify_complement(row, full, claimed):
    integer(full, 1, 31, 'invalid held full-ideal mask')
    require(type(claimed) is F and full in row and claimed == 1-sum((v for s, v in row.items() if s != full), F(0)),
            'held full complement omitted proper slots')


def verify_twin_identity(b, c, d, h15, h23):
    require(all(type(q) is F and q > 0 for q in (b, c, d, h15, h23))
            and b*h15 == c*d and h15 == h23, 'actual H5 twin-top diamond identity failed')


def build_held():
    held, entries, base, extended = {}, [], [], []
    for order, count in zip(HELD, HELD_RECORDS):
        for record in range(count):
            budget()
            row = held_row(order, record)
            held[(order, record)] = row
            full = (1 << len(order))-1
            verify_complement(row, full, row[full])
            entries.append(dict(order=order, record=record, probabilities=[[s, str(q)] for s, q in sorted(row.items())]))
    for xi in range(8):
        a = held[(C3, xi)][7]
        b, c = held[(C4, xi)][7], held[(C4, xi)][15]
        d = held[(C5, xi)][7]
        g, h15, h23, j = (held[(H5, xi)][s] for s in (7, 15, 23, 31))
        verify_twin_identity(b, c, d, h15, h23)
        base.append(dict(record=xi, a=str(a), b=str(b), c=str(c), d=str(d), g=str(g), h=str(h15),
                         h23=str(h23), j=str(j), diamond_left=str(b*h15), diamond_right=str(c*d)))
    for eta in range(16):
        require(held[(C5, eta)][7] == held[(C5, eta & 7)][7], 'C5 core probability reads the first cap record')
        extended.append(dict(record=eta, e=str(held[(C5, eta)][15]), f=str(held[(C5, eta)][31])))
    for order, count in zip(HELD, HELD_RECORDS):
        for s in ideals(order):
            if s == (1 << len(order))-1:
                continue
            local = {}
            for record in range(count):
                key, q = record & s, held[(order, record)][s]
                require(key not in local or local[key] == q, 'held proper probability reads a nonprecursor record')
                local[key] = q
    require(len(entries) == 40 and sum(len(row['probabilities']) for row in entries) == 224,
            'held marked-row or probability-slot coverage mismatch')
    return held, entries, dict(base=base, extended=extended)


def parameters_at(parameters, record):
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    xi, eta = record & 7, record & 15
    base, extended = parameters['base'][xi], parameters['extended'][eta]
    require(type(base['record']) is int and base['record'] == xi
            and type(extended['record']) is int and extended['record'] == eta, 'parameter row ordering changed')
    result = {key: fraction(base[key]) for key in ('a', 'b', 'c', 'd', 'g', 'h', 'j')}
    result.update({key: fraction(extended[key]) for key in ('e', 'f')})
    return result


def formula_slots(parent_index, record, parameters):
    integer(parent_index, 0, 4, 'invalid exact parent index')
    p = parameters_at(parameters, record)
    a, b, c, d, e, f, g, h, j = (p[k] for k in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j'))
    return ({7: a*g**3/b**3, 15: h*h/c, 23: h*h/c, 39: h*h/c, 31: j, 47: j, 55: j},
            {7: d*g/b, 15: e*h/c, 23: h, 31: j, 47: f},
            {7: g, 15: h, 23: h, 31: j}, {7: d*d/b, 15: e*e/c, 31: f, 47: f},
            {7: d, 15: e, 31: f})[parent_index]


def compact_coefficients(parent_index, record, parameters):
    values = [F(0)]*11
    for s, q in formula_slots(parent_index, record, parameters).items():
        values[FORWARD[parent_index][s]] += q
    return values


def compact_id(parent_index, record):
    integer(parent_index, 0, 4, 'invalid exact parent index')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    return (0, 8, 24, 32, 48)[parent_index]+(record & (7 if parent_index in (0, 2) else 15))


def build_compact(parameters):
    rows = []
    for i, count in enumerate((8, 16, 8, 16, 16)):
        for record in range(count):
            require(compact_id(i, record) == len(rows), 'compact row ordering changed')
            rows.append(dict(parent_index=i, record=record, representative_expanded_id=64*i+record,
                             coefficients=[str(q) for q in compact_coefficients(i, record, parameters)]))
    require(len(rows) == 64, 'compact row coverage mismatch')
    return rows


def reduced_record(order, local):
    validate_order(order)
    require(order in HELD, 'factor order escaped held closure')
    integer(local, 0, (1 << len(order))-1, 'invalid factor local record')
    if order == C3:
        return local, 'no extra projection; all C3 records retained'
    if order == C5:
        return local & 15, 'unique-top locality and full complement; first cap bit retained'
    if order == C4:
        return local & 7, 'unique-top locality and full complement'
    return local & 7, 'H5 inherited b*h=c*d, top exchange, locality and full complement'


def factor_data(order, record, part, deletion, held):
    validate_order(order)
    require(canonical_key(order) in PARENTS, 'factor parent outside affected isomorphism classes')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(part, 0, 63, 'precursor is not an exact in-range integer')
    require(part in ideals(order) and part != 63 and support_index(order+(part,)) is not None,
            'factor request outside supported proper ideals')
    integer(deletion, 1, 63, 'invalid exact maximal-deletion mask')
    omitted = sum(1 << v for v in maxima(order) if not part & (1 << v))
    require(deletion & omitted == deletion, 'deleted vertices are not omitted maxima')
    smaller, vertices = induce(order, 63 ^ deletion)
    require(smaller in HELD, 'supported factor escaped four held orders')
    precursor = restrict_mask(part, vertices, 6)
    raw = restrict_mask(record, vertices, 6)
    proper = precursor != (1 << len(smaller))-1
    local = raw & precursor if proper else raw
    query, theorem = reduced_record(smaller, local)
    require(precursor in held[(smaller, query)], 'transported precursor is not a held ideal')
    q = held[(smaller, query)][precursor]
    exponent = 1 if deletion.bit_count() % 2 else -1
    return dict(deleted_mask=deletion, kept_vertices=list(vertices), induced_order=list(smaller),
                induced_precursor=precursor, raw_transported_record=raw, local_read_record=local,
                held_query_record=query, proper_locality_applied=proper, projection_theorem=theorem,
                exponent=exponent, probability=str(q))


def verify_factor(factor, order, record, part, held):
    require(type(factor) is dict and set(factor) == {'deleted_mask', 'kept_vertices', 'induced_order',
            'induced_precursor', 'raw_transported_record', 'local_read_record', 'held_query_record',
            'proper_locality_applied', 'projection_theorem', 'exponent', 'probability'},
            'factor evidence fields changed')
    integer(factor['deleted_mask'], 1, 63, 'invalid exact maximal-deletion mask')
    expected = factor_data(order, record, part, factor['deleted_mask'], held)
    strict_shape(factor, expected)
    require(canonical(factor) == canonical(expected), 'factor probability exponent or record transport corrupted')


def potential(order, record, part, held):
    validate_order(order)
    require(canonical_key(order) in PARENTS, 'potential parent outside affected isomorphism classes')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(part, 0, 63, 'precursor is not an exact in-range integer')
    require(part in ideals(order) and part != 63 and support_index(order+(part,)) is not None,
            'potential request outside supported proper ideals')
    omitted = sum(1 << v for v in maxima(order) if not part & (1 << v))
    deletion, value, factors = omitted, F(1), []
    while deletion:
        item = factor_data(order, record, part, deletion, held)
        verify_factor(item, order, record, part, held)
        q = fraction(item['probability'])
        value *= q if item['exponent'] == 1 else 1/q
        factors.append(item)
        deletion = (deletion-1) & omitted
    require(factors and value > 0, 'supported deletion potential lost strict positivity')
    return value, factors


def verify_expanded_row(row, parameters, compact):
    i, record = row['parent_index'], row['record']
    integer(i, 0, 4, 'invalid exact parent index')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(row['compact_id'], 0, 63, 'invalid exact compact row id')
    require(row['compact_id'] == compact_id(i, record), 'expanded compact correspondence changed')
    require(type(row['entries']) is list, 'expanded ideal entries are not a list')
    for item in row['entries']:
        integer(item['ideal'], 0, 63, 'precursor is not an exact in-range integer')
    require([item['ideal'] for item in row['entries']] == list(IDEALS[i]), 'expanded row lost individual-ideal coverage')
    total = [F(0)]*11
    formulas = formula_slots(i, record, parameters)
    for item in row['entries']:
        index = FORWARD[i].get(item['ideal'])
        require(item['support_index'] == index and (index is None or type(item['support_index']) is int),
                'expanded support-class index changed')
        q = fraction(item['correction_coefficient'])
        require((index is None and q == 0 and item['factors'] == []) or (index is not None and q > 0),
                'unsupported correction confused with probability or supported positivity')
        require(q == formulas.get(item['ideal'], F(0)), 'generic deletion product disagrees with symbolic slot formula')
        if index is not None:
            total[index] += q
    require(row['coefficients'] == [str(q) for q in total]
            and row['coefficients'] == compact[row['compact_id']]['coefficients'],
            'expanded coefficient multiplicity or record reduction mismatch')


def verify_expanded_coverage(rows):
    require(type(rows) is list and all(type(row) is dict for row in rows), 'invalid expanded-row container')
    for row in rows:
        integer(row['parent_index'], 0, 4, 'invalid exact parent index')
        integer(row['record'], 0, 63, 'expanded record is not an exact in-range integer')
    require([(r['parent_index'], r['record']) for r in rows] == [(i, r) for i in range(5) for r in range(64)],
            'complete expanded marked-row coverage mismatch')


def build_expanded(held, parameters, compact):
    rows = []
    for i, parent in enumerate(PARENTS):
        for record in range(64):
            budget()
            entries, total = [], [F(0)]*11
            for part in IDEALS[i]:
                index = support_index(parent+(part,))
                value, factors = (F(0), []) if index is None else potential(parent, record, part, held)
                if index is not None:
                    total[index] += value
                entries.append(dict(ideal=part, canonical_child=canonical_key(parent+(part,)), support_index=index,
                                    correction_coefficient=str(value), factors=factors, baseline_probability_computed=False))
            row = dict(parent_index=i, record=record, compact_id=compact_id(i, record),
                       entries=entries, coefficients=[str(q) for q in total])
            verify_expanded_row(row, parameters, compact)
            rows.append(row)
    verify_expanded_coverage(rows)
    for index, row in enumerate(compact):
        representative = row['representative_expanded_id']
        integer(representative, 0, 319, 'invalid exact expanded representative id')
        require(rows[representative]['compact_id'] == index and rows[representative]['coefficients'] == row['coefficients'],
                'compact representative row mapping failed')
    return rows


def verify_relabel_inventory(inventory):
    require(type(inventory) is list, 'transport inventory is not a list')
    for item in inventory:
        require(type(item) is dict and set(item) == {'parent_index', 'permutation', 'image'},
                'transport inventory fields changed')
        integer(item['parent_index'], 0, 4, 'invalid exact transported parent index')
        require(type(item['permutation']) is list and type(item['image']) is list,
                'transport inventory arrays changed')
        validate_permutation(tuple(item['permutation']), 6)
        validate_order(tuple(item['image']))
    expected = [dict(parent_index=i, permutation=list(p), image=list(q))
                for i, parent in enumerate(PARENTS) for p, q in natural_relabelings(parent)]
    require(canonical(inventory) == canonical(expected), 'natural relabeling or same-image automorphism omitted')


def verify_transport_case(case):
    require(type(case) is dict and all(k in case for k in ('record', 'ideal', 'permutation',
                                                          'transported_record', 'transported_ideal')),
            'transport case fields missing')
    p = case['permutation']
    validate_permutation(p, 6)
    for key in ('record', 'ideal', 'transported_record', 'transported_ideal'):
        integer(case[key], 0, 63, 'invalid exact transported record or ideal')
    require(case['transported_record'] == transport(case['record'], p)
            and case['transported_ideal'] == transport(case['ideal'], p), 'record and precursor were not transported together')


def check_equivariance(rows, held):
    inventory = [dict(parent_index=i, permutation=list(p), image=list(q))
                 for i, parent in enumerate(PARENTS) for p, q in natural_relabelings(parent)]
    verify_relabel_inventory(inventory)
    table = {(row['parent_index'], row['record']): {x['ideal']: x for x in row['entries']} for row in rows}
    cases, factor_count, parent_images, relabel_counts = [], 0, [], []
    for i, parent in enumerate(PARENTS):
        relabelings = natural_relabelings(parent)
        relabel_counts.append(len(relabelings))
        parent_images.append(sorted(set(image for _, image in relabelings)))
        for permutation, image in relabelings:
            require(canonical_key(image) == parent, 'transported parent changed isomorphism class')
            for record in range(64):
                budget()
                moved_record = transport(record, permutation)
                for part in IDEALS[i]:
                    moved_part = transport(part, permutation)
                    source = table[(i, record)][part]
                    moved_index = support_index(image+(moved_part,))
                    value, factors = (F(0), []) if moved_index is None else potential(image, moved_record, moved_part, held)
                    require(source['support_index'] == moved_index and fraction(source['correction_coefficient']) == value,
                            'transported natural-image coefficient equivariance failed')
                    factor_count += len(factors)
                    case = dict(parent_index=i, permutation=permutation, image=image, record=record, ideal=part,
                                transported_record=moved_record, transported_ideal=moved_part,
                                support_index=moved_index, coefficient=str(value), factors_sha256=digest(factors))
                    verify_transport_case(case)
                    cases.append(case)
    require(relabel_counts == [6, 3, 2, 2, 1] and [len(images) for images in parent_images] == [1, 3, 1, 1, 1]
            and len(cases) == 8448 and factor_count == 10752, 'frozen natural-relabel audit coverage mismatch')
    return dict(parent_natural_relabelings=relabel_counts, parent_natural_images=parent_images,
                marked_ideal_cases=len(cases), recomputed_factor_occurrences=factor_count, manifest_sha256=digest(cases))


def validate_matrix(matrix, width=None):
    require(type(matrix) is list and 1 <= len(matrix) <= 64 and all(type(row) is list for row in matrix),
            'matrix outside exact bounded row domain')
    n = len(matrix[0])
    require(1 <= n <= 65 and (width is None or n == width)
            and all(len(row) == n and all(type(q) is F for q in row) for row in matrix),
            'matrix outside exact rational column domain')


def rref(matrix, variables):
    """First available pivot, left-to-right columns, exact all-row elimination."""
    validate_matrix(matrix)
    integer(variables, 1, min(64, len(matrix[0])), 'invalid exact elimination variable count')
    work = [row[:] for row in matrix]
    pivots, operations, level = [], [], 0
    for column in range(variables):
        budget()
        found = next((i for i in range(level, len(work)) if work[i][column]), None)
        if found is None:
            continue
        if found != level:
            work[level], work[found] = work[found], work[level]
            operations.append(['swap', level, found])
        divisor = work[level][column]
        work[level] = [q/divisor for q in work[level]]
        operations.append(['divide', level, str(divisor)])
        for i in range(len(work)):
            if i != level and work[i][column]:
                multiplier = work[i][column]
                work[i] = [q-multiplier*p for q, p in zip(work[i], work[level])]
                operations.append(['subtract', i, level, str(multiplier)])
        pivots.append(column)
        level += 1
        if level == len(work):
            break
    return work, dict(variable_columns=variables, rank=level, pivot_columns=pivots,
                      reduced_matrix=encoded(work), operations=operations)


def verify_reduction(matrix, evidence):
    """Replay retained elementary operations, then independently recompute RREF."""
    validate_matrix(matrix)
    require(type(evidence) is dict and set(evidence) == {'variable_columns', 'rank', 'pivot_columns',
                                                      'reduced_matrix', 'operations'}, 'RREF evidence fields changed')
    integer(evidence['variable_columns'], 1, min(64, len(matrix[0])), 'invalid exact elimination variable count')
    integer(evidence['rank'], 0, min(len(matrix), evidence['variable_columns']), 'invalid exact matrix rank')
    require(type(evidence['pivot_columns']) is list and all(type(j) is int for j in evidence['pivot_columns']),
            'RREF pivot columns lost exact integer types')
    require(type(evidence['operations']) is list, 'RREF operations are not a list')
    replay = [row[:] for row in matrix]
    for operation in evidence['operations']:
        require(type(operation) is list and operation and type(operation[0]) is str, 'malformed RREF operation')
        kind = operation[0]
        require(kind in ('swap', 'divide', 'subtract')
                and len(operation) == (4 if kind == 'subtract' else 3), 'malformed RREF operation')
        integer(operation[1], 0, len(matrix)-1, 'invalid exact RREF row index')
        i = operation[1]
        if kind == 'swap':
            integer(operation[2], 0, len(matrix)-1, 'invalid exact RREF row index')
            replay[i], replay[operation[2]] = replay[operation[2]], replay[i]
        elif kind == 'divide':
            divisor = fraction(operation[2])
            require(divisor != 0, 'zero RREF row divisor')
            replay[i] = [q/divisor for q in replay[i]]
        else:
            integer(operation[2], 0, len(matrix)-1, 'invalid exact RREF row index')
            require(i != operation[2], 'RREF subtraction changed its pivot row')
            multiplier = fraction(operation[3])
            replay[i] = [q-multiplier*p for q, p in zip(replay[i], replay[operation[2]])]
    require(encoded(replay) == evidence['reduced_matrix'], 'retained RREF elementary-operation identity failed')
    _, expected = rref(matrix, evidence['variable_columns'])
    strict_shape(evidence, expected)
    require(canonical(evidence) == canonical(expected), 'deterministic RREF recomputation mismatch')


def dot(left, right):
    require(len(left) == len(right), 'rational dot-product dimensions disagree')
    return sum((a*b for a, b in zip(left, right)), F(0))


def null_basis(matrix, reduced, pivots):
    free = [j for j in range(11) if j not in pivots]
    basis = []
    for j in free:
        vector = [F(0)]*11
        vector[j] = F(1)
        for i, pivot in enumerate(pivots):
            vector[pivot] = -reduced[i][j]
        require(all(dot(row, vector) == 0 for row in matrix), 'standard null-basis residual failed')
        basis.append(vector)
    return free, basis


def verify_dual(matrix, dual):
    require(type(dual) is list and len(dual) == 64 and all(type(q) is F for q in dual),
            'signed dual vector dimensions or exact types changed')
    residual = [sum((dual[i]*matrix[i][j] for i in range(64)), F(0)) for j in range(11)]
    require(residual == [F(1)]+[F(0)]*10, 'signed row-span certificate identity failed')
    return residual


def decide(matrix):
    validate_matrix(matrix, 11)
    require(len(matrix) == 64, 'compact matrix must contain all sixty-four rows')
    reduced, reduction = rref(matrix, 11)
    verify_reduction(matrix, reduction)
    free, basis = null_basis(matrix, reduced, reduction['pivot_columns'])
    chosen = next((i for i, vector in enumerate(basis) if vector[0]), None)
    result = dict(reduction=reduction, free_columns=free, null_basis=encoded(basis),
                  first_width_basis_index=chosen, z=None, dual=None, dual_reduction=None, dual_identity=None)
    if chosen is not None:
        vector = [q/basis[chosen][0] for q in basis[chosen]]
        require(vector[0] == 1 and all(dot(row, vector) == 0 for row in matrix), 'canonical width-vector residual failed')
        result.update(disposition='positive-finite-width-bias', z=[str(q) for q in vector])
    else:
        augmented = [[matrix[i][j] for i in range(64)]+[F(j == 0)] for j in range(11)]
        reduced_dual, dual_reduction = rref(augmented, 64)
        verify_reduction(augmented, dual_reduction)
        require(all(any(row[:64]) or row[64] == 0 for row in reduced_dual), 'row-span alternative is inconsistent')
        dual = [F(0)]*64
        for i, j in enumerate(dual_reduction['pivot_columns']):
            dual[j] = reduced_dual[i][64]
        identity = verify_dual(matrix, dual)
        result.update(disposition='full-support-obstruction' if reduction['rank'] == 11 else 'named-width-target-obstruction',
                      dual=[str(q) for q in dual], dual_reduction=dual_reduction, dual_identity=[str(q) for q in identity])
    return result


def verify_decision(matrix, evidence):
    expected = decide(matrix)
    strict_shape(evidence, expected)
    require(canonical(evidence) == canonical(expected), 'canonical exact decision witness mismatch')


def verify_positive_transform(vector, epsilon, h):
    require(type(vector) is list and len(vector) == 11 and all(type(q) is F for q in vector),
            'finite transform vector lost exact coordinates')
    require(type(epsilon) is F and epsilon > 0, 'finite transform amplitude must be strictly positive')
    require(type(h) is list and len(h) == 11 and all(type(q) is F for q in h)
            and h == [1+epsilon*z for z in vector] and all(q > 0 for q in h),
            'supported transform lost strict positivity or affine identity')


def transform(vector):
    maximum = max(abs(q) for q in vector)
    epsilon = 1/(2*(1+maximum))
    h = [1+epsilon*q for q in vector]
    verify_positive_transform(vector, epsilon, h)
    negative = [q for q in vector if q < 0]
    require(negative and all(q > F(1, 2) for q in h), 'interior amplitude or negative-coordinate proof failed')
    endpoint = min(-1/q for q in negative)
    require(epsilon < endpoint, 'interior amplitude reaches the zero-h endpoint')
    return dict(maximum_absolute_coordinate=str(maximum), epsilon=str(epsilon), h=[str(q) for q in h],
                epsilon_max=str(endpoint), minimum_h=str(min(h)))


def width_functional(expanded):
    target = expanded[0]
    require(target['parent_index'] == 0 and target['record'] == 0, 'fixed complete-row target changed')
    coefficients, terms = [F(0)]*11, []
    for entry in target['entries']:
        j, value = entry['support_index'], fraction(entry['correction_coefficient'])
        width = None if j is None else intrinsic_width(PARENTS[0]+(entry['ideal'],))
        for newborn in range(2):
            term = F(0) if j is None else value*width/2
            if j is not None:
                coefficients[j] += term
            terms.append(dict(ideal=entry['ideal'], newborn_record=newborn, support_index=j,
                              child_width=width, coefficient_after_fair_bit=str(term)))
    harmonic = [fraction(q) for q in target['coefficients']]
    u0 = fraction(next(x['correction_coefficient'] for x in target['entries'] if x['ideal'] == 7))
    require(len(terms) == 22 and u0 > 0 and [a-3*b for a, b in zip(coefficients, harmonic)] == [u0]+[F(0)]*10,
            'complete-row width functional or fair-bit multiplicity identity failed')
    return dict(parent_index=0, record=0, all_ideal_count=11, fair_bit_term_count=22, terms=terms,
                coefficients=[str(q) for q in coefficients], positive_first_coordinate_multiplier=str(u0),
                baseline_probability_evaluated=False, conditional_on_support=False)


def admission(decision, compact, expanded, width):
    matrix = [[fraction(q) for q in row['coefficients']] for row in compact]
    if decision['z'] is not None:
        vector = [fraction(q) for q in decision['z']]
        residuals = [dot([fraction(q) for q in row['coefficients']], vector) for row in expanded]
        require(all(q == 0 for q in residuals), 'expanded harmonic residual failed')
        result = transform(vector)
        functional = dot([fraction(q) for q in width['coefficients']], vector)
        u0 = fraction(width['positive_first_coordinate_multiplier'])
        require(vector[0] == 1 and functional == u0 and functional > 0, 'named unconditional width gain is not positive')
        result.update(expanded_residuals=[str(q) for q in residuals], width_functional=str(functional),
                      width_gain_divided_by_a6=str(fraction(result['epsilon'])*functional),
                      numerical_a6_evaluated=False, later_h_prescribed=False, dual_lift=None)
        return result
    dual = [fraction(q) for q in decision['dual']]
    verify_dual(matrix, dual)
    lifted = [F(0)]*320
    for q, row in zip(dual, compact):
        lifted[row['representative_expanded_id']] += q
    residual = [sum((q*fraction(row['coefficients'][j]) for q, row in zip(lifted, expanded)), F(0)) for j in range(11)]
    require(residual == [F(1)]+[F(0)]*10, 'expanded signed-dual lift lost representative multiplicity')
    return dict(epsilon=None, h=None, width_gain_divided_by_a6=None, later_h_prescribed=False,
                numerical_a6_evaluated=False, dual_lift=[str(q) for q in lifted],
                expanded_dual_identity=[str(q) for q in residual])


def build_witness():
    structure = build_structure()
    prefix = rebuild_prefix()
    held, held_entries, parameters = build_held()
    compact = build_compact(parameters)
    expanded = build_expanded(held, parameters, compact)
    equivariance = check_equivariance(expanded, held)
    budget('bounded structures, held rows, generic factors and transported records checked')
    matrix = [[fraction(q) for q in row['coefficients']] for row in compact]
    decision = decide(matrix)
    width = width_functional(expanded)
    admitted = admission(decision, compact, expanded, width)
    coverage = dict(support_classes=11, maximal_deletion_roles=len(structure['maximal_deletions']),
                    affected_parent_classes=5, forward_individual_ideals=len(structure['forward_slots']),
                    held_marked_rows=len(held_entries), held_probability_slots=sum(len(row['probabilities']) for row in held_entries),
                    compact_rows=len(compact), matrix_columns=11, expanded_marked_rows=len(expanded),
                    expanded_ideal_occurrences=sum(len(row['entries']) for row in expanded),
                    supported_occurrences=sum(x['support_index'] is not None for row in expanded for x in row['entries']),
                    zero_correction_occurrences=sum(x['support_index'] is None for row in expanded for x in row['entries']),
                    full_birth_occurrences=sum(x['ideal'] == 63 for row in expanded for x in row['entries']),
                    strict_stem_prefix_occurrences=sum(x['ideal'] in (0, 1, 3) for row in expanded for x in row['entries']),
                    generic_factor_occurrences=sum(len(x['factors']) for row in expanded for x in row['entries']))
    require(coverage == dict(support_classes=11, maximal_deletion_roles=27, affected_parent_classes=5,
                            forward_individual_ideals=43, held_marked_rows=40, held_probability_slots=224,
                            compact_rows=64, matrix_columns=11, expanded_marked_rows=320,
                            expanded_ideal_occurrences=2752, supported_occurrences=1472,
                            zero_correction_occurrences=1280, full_birth_occurrences=320,
                            strict_stem_prefix_occurrences=960, generic_factor_occurrences=2752),
            'complete frozen finite-domain coverage mismatch')
    witness = dict(schema='ri88-four-vertex-cap-v1', design_sha256=DESIGN_SHA256, dependencies=PINS,
                   domain='RI85 frozen finite prefix; no numeric future-layer probabilities or scale',
                   prefix=prefix, structure=structure, held_rows=held_entries, parameters=parameters,
                   compact_rows=compact, expanded_rows=expanded, coverage=coverage,
                   transported_audit=equivariance, exact_decision=decision, width_target=width, admission=admitted)
    # Normalize tuples to their on-disk JSON representation before strict schema comparison.
    return copy_json(witness), held, matrix


def synthetic_matrix(kind):
    """Algebra-only fixtures, not additional native held rows or probability laws."""
    require(type(kind) is str and kind in ('positive', 'width-only', 'full-rank'), 'unknown synthetic algebra fixture')
    matrix = [[F(0)]*11 for _ in range(64)]
    matrix[0][:3] = [F(1), F(3), F(3)]
    if kind == 'width-only':
        matrix[1][1:3] = [F(3), F(3)]
    if kind == 'full-rank':
        for j in range(1, 11):
            matrix[j][j] = F(1)
    return matrix


def refusal_controls(witness, held, matrix):
    """Every control checks its named refusal, not merely any exception."""
    passed = []
    def expect(name, reason, action):
        try:
            action()
        except RuntimeError as error:
            require(str(error) == reason, 'control '+name+' failed for the wrong reason: '+str(error))
        else:
            raise RuntimeError('control '+name+' was not refused')
        passed.append(name)
    def altered(value, path, replacement):
        result = copy_json(value)
        cursor = result
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        return result
    def saved_change(name, path, replacement, reason='certificate finite witness mismatch'):
        expect(name, reason, lambda: verify_certificate(altered(witness, path, replacement), witness))

    expect('duplicate-json-key', 'duplicate JSON object key', lambda: load_json('{"a":0,"a":1}'))
    expect('decimal-json', 'JSON decimals and nonfinite constants are forbidden', lambda: load_json('{"a":0.5}'))
    expect('nonfinite-json', 'JSON decimals and nonfinite constants are forbidden', lambda: load_json('{"a":NaN}'))
    expect('noncanonical-rational', 'noncanonical rational encoding', lambda: fraction('2/2'))
    expect('numeric-rational', 'noncanonical rational encoding', lambda: fraction(1))
    expect('wrong-dependency-pin', 'accepted dependency byte pin mismatch', lambda: check_pin(b'not a dependency', PINS['ri74_checker']))
    expect('order-eight-refusal', 'invalid bounded natural order or exact mask type', lambda: validate_order((0,)*8))
    expect('unhashable-order-refusal', 'invalid bounded natural order or exact mask type', lambda: canonical_key([0, 1, 3]))
    expect('nested-unhashable-order-before-cache', 'invalid bounded natural order or exact mask type',
           lambda: natural_relabelings((0, [1], 3)))
    # Warm the valid caches before bool aliases: exact guards must precede lookup.
    ideals(PARENTS[0])
    natural_relabelings(PARENTS[0])
    bad_parent = (False,)+PARENTS[0][1:]
    expect('warm-cache-bool-order', 'invalid bounded natural order or exact mask type', lambda: ideals(bad_parent))
    expect('warm-cache-bool-canonicalization', 'invalid bounded natural order or exact mask type', lambda: natural_relabelings(bad_parent))
    expect('out-of-domain-order', 'canonicalization seed outside frozen domain', lambda: natural_relabelings((0, 0)))
    expect('bool-permutation', 'invalid permutation or exact vertex type', lambda: transport(1, (False, 1, 2, 3, 4, 5)))
    expect('bool-dimension', 'permutation dimension outside frozen exact bounds', lambda: validate_permutation((0,), True))
    expect('restriction-dimension', 'restriction dimension outside frozen exact bounds', lambda: restrict_mask(1, (0,), 8))
    expect('bool-record-transport', 'invalid transport mask or exact integer type', lambda: transport(True, tuple(range(6))))
    expect('held-bool-record-before-cache', 'held record is not an exact in-range integer', lambda: held_row(C3, True))
    expect('held-top-bit-query-refusal', 'unapproved held top-mark query', lambda: held_row(C5, 16))
    expect('held-twin-top-query-refusal', 'unapproved held top-mark query', lambda: held_row(H5, 8))
    expect('held-record-out-of-range', 'held record is not an exact in-range integer', lambda: held_row(C3, 8))
    expect('no-six-parent-probability-query', 'q6 or q7 probability lookup forbidden', lambda: held_row(PARENTS[0], 0))
    expect('no-seven-parent-probability-query', 'q6 or q7 probability lookup forbidden', lambda: held_row(SUPPORT[0], 0))
    expect('no-other-held-parent', 'held parent outside frozen four-class domain', lambda: held_row((0, 0), 0))
    for name in ('a6', 'M6', 'q6', 'q7'):
        expect('no-numerical-'+name, 'numerical future law or global scale forbidden', lambda name=name: forbidden_scale(name))
    bad_report = altered(witness['prefix'], ['actual_probability_manifest_sha256'], '0'*64)
    expect('actual-not-boundary-prefix', 'accepted actual strict prefix identity mismatch', lambda: verify_actual_prefix(bad_report))
    damaged_row = dict(held[(C5, 0)])
    damaged_row.pop(7)
    expect('held-omitted-ideal', 'held row lost exact labeled ideals or strict normalization', lambda: verify_held_row(C5, damaged_row))
    expect('full-is-not-one-minus-selected-p', 'held full complement omitted proper slots',
           lambda: verify_complement(held[(C5, 0)], 31, 1-held[(C5, 0)][15]))
    p = parameters_at(witness['parameters'], 0)
    expect('twin-top-factor-corruption', 'actual H5 twin-top diamond identity failed',
           lambda: verify_twin_identity(p['b'], p['c'], p['d'], p['h']+1, p['h']))
    expect('wrong-variable-order', 'support classes or variable order changed', lambda: verify_support(SUPPORT[::-1], WIDTHS))
    expect('extra-support-class', 'frozen support shape changed', lambda: verify_support(SUPPORT+(SUPPORT[0],), WIDTHS))
    expect('wrong-cap-width', 'intrinsic cap widths changed', lambda: verify_support(SUPPORT, (3,)+WIDTHS[1:]))
    roles = witness['structure']['maximal_deletions']
    expect('missing-maximal-deletion-role', 'maximal-deletion closure or role multiplicity mismatch', lambda: verify_deletions(roles[:-1]))
    expect('bool-deletion-index', 'invalid exact deletion support index',
           lambda: verify_deletions(altered(roles, [0, 'support_index'], False)))
    forwards = witness['structure']['forward_slots']
    expect('missing-forward-ideal', 'forward individual-ideal coverage or support classification mismatch',
           lambda: verify_forward(forwards[:-1]))
    expect('forward-child-class-corruption', 'forward individual-ideal coverage or support classification mismatch',
           lambda: verify_forward(altered(forwards, [3, 'support_index'], 1)))
    expect('bool-forward-ideal', 'invalid exact forward ideal', lambda: verify_forward(altered(forwards, [0, 'ideal'], False)))
    expect('missing-expanded-record', 'complete expanded marked-row coverage mismatch',
           lambda: verify_expanded_coverage(witness['expanded_rows'][:-1]))
    expect('bool-expanded-record', 'expanded record is not an exact in-range integer',
           lambda: verify_expanded_coverage(altered(witness['expanded_rows'], [0, 'record'], False)))
    row0 = witness['expanded_rows'][0]
    expect('backward-role-count-is-not-forward-weight', 'generic deletion product disagrees with symbolic slot formula',
           lambda: verify_expanded_row(altered(row0, ['entries', 3, 'correction_coefficient'],
                                              str(4*fraction(row0['entries'][3]['correction_coefficient']))),
                                      witness['parameters'], witness['compact_rows']))
    expect('missing-individual-expanded-ideal', 'expanded row lost individual-ideal coverage',
           lambda: verify_expanded_row(altered(row0, ['entries'], row0['entries'][:-1]), witness['parameters'], witness['compact_rows']))
    expect('zero-correction-not-zero-probability', 'unsupported correction confused with probability or supported positivity',
           lambda: verify_expanded_row(altered(row0, ['entries', 0, 'correction_coefficient'], '1'),
                                      witness['parameters'], witness['compact_rows']))
    expect('forward-multiplicity-corruption', 'expanded coefficient multiplicity or record reduction mismatch',
           lambda: verify_expanded_row(altered(row0, ['coefficients', 1], '0'), witness['parameters'], witness['compact_rows']))
    expect('wrong-expanded-representative', 'expanded compact correspondence changed',
           lambda: verify_expanded_row(altered(row0, ['compact_id'], 1), witness['parameters'], witness['compact_rows']))
    expect('unsupported-direct-factor', 'factor request outside supported proper ideals',
           lambda: factor_data(PARENTS[0], 0, 0, 8, held))
    expect('full-direct-factor', 'factor request outside supported proper ideals',
           lambda: factor_data(PARENTS[0], 0, 63, 8, held))
    expect('bool-factor-precursor', 'precursor is not an exact in-range integer',
           lambda: factor_data(PARENTS[0], 0, True, 8, held))
    expect('delete-nonmaximal-factor', 'deleted vertices are not omitted maxima',
           lambda: factor_data(PARENTS[0], 0, 7, 1, held))
    expect('missing-factor-mask', 'factor evidence fields changed', lambda: verify_factor({}, PARENTS[0], 0, 7, held))
    moved_parent = (0, 1, 3, 7, 7, 23)
    moved_factor = factor_data(moved_parent, 16, 23, 8, held)
    require(moved_factor['kept_vertices'] == [0, 1, 2, 4, 5]
            and moved_factor['raw_transported_record'] == moved_factor['local_read_record'] == moved_factor['held_query_record'] == 8
            and moved_factor['induced_precursor'] == 15, 'cap-root transport control fixture is not the declared case')
    for name, field, value in (('erase-retained-cap-bit', 'held_query_record', 0),
                               ('wrong-raw-record-transport', 'raw_transported_record', 0),
                               ('wrong-factor-exponent', 'exponent', -1),
                               ('wrong-factor-probability', 'probability', str(fraction(moved_factor['probability'])+1))):
        expect(name, 'factor probability exponent or record transport corrupted',
               lambda field=field, value=value: verify_factor(altered(moved_factor, [field], value), moved_parent, 16, 23, held))
    expect('bool-retained-vertex', 'certificate value type mismatch',
           lambda: verify_factor(altered(moved_factor, ['kept_vertices', 0], False), moved_parent, 16, 23, held))
    inventory = [dict(parent_index=i, permutation=list(p0), image=list(q))
                 for i, parent in enumerate(PARENTS) for p0, q in natural_relabelings(parent)]
    expect('omit-noncanonical-parent-image', 'natural relabeling or same-image automorphism omitted',
           lambda: verify_relabel_inventory([x for x in inventory if tuple(x['image']) != moved_parent]))
    expect('omit-same-image-automorphism', 'natural relabeling or same-image automorphism omitted',
           lambda: verify_relabel_inventory(inventory[1:]))
    permutation = (0, 1, 2, 4, 3, 5)
    transport_case = dict(permutation=permutation, record=8, ideal=15, transported_record=16, transported_ideal=23)
    verify_transport_case(transport_case)
    expect('transport-record-without-ideal', 'record and precursor were not transported together',
           lambda: verify_transport_case(dict(transport_case, transported_ideal=15)))
    expect('transport-ideal-without-record', 'record and precursor were not transported together',
           lambda: verify_transport_case(dict(transport_case, transported_record=8)))

    # These three small padded matrices exercise all outcomes regardless of the
    # as-yet-uncomputed native rank. They query no held data and prove no model.
    examples = {kind: synthetic_matrix(kind) for kind in ('positive', 'width-only', 'full-rank')}
    decisions = {kind: decide(value) for kind, value in examples.items()}
    require([decisions[k]['disposition'] for k in examples]
            == ['positive-finite-width-bias', 'named-width-target-obstruction', 'full-support-obstruction'],
            'synthetic three-branch algebra fixtures changed')
    vector = [fraction(q) for q in decisions['positive']['z']]
    admitted = transform(vector)
    epsilon, h = fraction(admitted['epsilon']), [fraction(q) for q in admitted['h']]
    require(dot([F(4), F(9), F(9)]+[F(0)]*8, vector) == 1,
            'synthetic complete width functional identity failed')
    require(any(fraction(q) < 0 for q in decisions['width-only']['dual']), 'synthetic dual no longer exercises signed coordinates')
    expect('bool-matrix-cell', 'matrix outside exact rational column domain', lambda: validate_matrix([[False]], 1))
    expect('short-compact-matrix', 'compact matrix must contain all sixty-four rows', lambda: decide(examples['positive'][:-1]))
    expect('zero-amplitude', 'finite transform amplitude must be strictly positive', lambda: verify_positive_transform(vector, F(0), [F(1)]*11))
    endpoint = fraction(admitted['epsilon_max'])
    expect('zero-h-endpoint', 'supported transform lost strict positivity or affine identity',
           lambda: verify_positive_transform(vector, endpoint, [1+endpoint*q for q in vector]))
    expect('affine-h-corruption', 'supported transform lost strict positivity or affine identity',
           lambda: verify_positive_transform(vector, epsilon, [h[0]+1]+h[1:]))
    expect('wrong-canonical-null-vector', 'canonical exact decision witness mismatch',
           lambda: verify_decision(examples['positive'], altered(decisions['positive'], ['z', 0], '2')))
    expect('wrong-first-null-basis-selection', 'canonical exact decision witness mismatch',
           lambda: verify_decision(examples['positive'], altered(decisions['positive'], ['first_width_basis_index'], 1)))
    expect('width-blind-kernel-is-not-success', 'canonical exact decision witness mismatch',
           lambda: verify_decision(examples['width-only'], altered(decisions['width-only'], ['disposition'], 'positive-finite-width-bias')))
    expect('full-rank-is-not-width-only', 'canonical exact decision witness mismatch',
           lambda: verify_decision(examples['full-rank'], altered(decisions['full-rank'], ['disposition'], 'named-width-target-obstruction')))
    signed = [fraction(q) for q in decisions['width-only']['dual']]
    expect('discard-negative-dual-coordinates', 'signed row-span certificate identity failed',
           lambda: verify_dual(examples['width-only'], [max(F(0), q) for q in signed]))
    expect('divide-dual-by-record-multiplicity', 'signed row-span certificate identity failed',
           lambda: verify_dual(examples['width-only'], [q/8 for q in signed]))
    evidence = decisions['positive']['reduction']
    expect('wrong-retained-rref-value', 'retained RREF elementary-operation identity failed',
           lambda: verify_reduction(examples['positive'], altered(evidence, ['reduced_matrix', 0, 0], '2')))
    expect('wrong-pivot-order', 'deterministic RREF recomputation mismatch',
           lambda: verify_reduction(examples['positive'], altered(evidence, ['pivot_columns', 0], 1)))
    expect('bool-rank', 'invalid exact matrix rank',
           lambda: verify_reduction(examples['positive'], altered(evidence, ['rank'], True)))
    expect('zero-elimination-divisor', 'zero RREF row divisor',
           lambda: verify_reduction(examples['positive'], altered(evidence, ['operations', 0, 2], '0')))

    saved_change('wrong-certificate-schema', ['schema'], 'not-ri88', 'certificate schema mismatch')
    expect('extra-certificate-field', 'certificate object fields mismatch',
           lambda: verify_certificate(dict(witness, unapproved_field=False), witness))
    expect('missing-certificate-field', 'certificate object fields mismatch',
           lambda: verify_certificate({k: v for k, v in witness.items() if k != 'domain'}, witness))
    saved_change('bool-certificate-index', ['compact_rows', 0, 'parent_index'], False, 'certificate value type mismatch')
    saved_change('missing-certificate-rows', ['expanded_rows'], witness['expanded_rows'][:-1], 'certificate list coverage mismatch')
    saved_change('wrong-compact-coefficient', ['compact_rows', 0, 'coefficients', 0], '0')
    saved_change('wrong-retained-factor-probability', ['expanded_rows', 0, 'entries', 3, 'factors', 0, 'probability'], '0')
    saved_change('wrong-retained-factor-exponent', ['expanded_rows', 0, 'entries', 3, 'factors', 0, 'exponent'], 0)
    saved_change('wrong-retained-factor-record', ['expanded_rows', 0, 'entries', 3, 'factors', 0, 'held_query_record'], 1)
    saved_change('forged-native-disposition', ['exact_decision', 'disposition'], 'uncomputed-is-not-a-result')
    saved_change('condition-width-on-support', ['width_target', 'conditional_on_support'], True)
    saved_change('drop-fair-newborn-multiplicity', ['width_target', 'fair_bit_term_count'], 11)
    saved_change('reverse-named-width-sign', ['width_target', 'coefficients', 0],
                 str(-fraction(witness['width_target']['coefficients'][0])))
    saved_change('forged-equivariance-manifest', ['transported_audit', 'manifest_sha256'], '0'*64)
    saved_change('wrong-design-pin', ['design_sha256'], '0'*64)
    require(len(passed) == 90 and len(set(passed)) == 90, 'frozen intended-reason refusal inventory changed')
    return dict(intended_reason_refusals=passed, synthetic_fixtures='algebra only; no native realization or extra held query',
                synthetic_branch_ranks={k: decisions[k]['reduction']['rank'] for k in examples},
                synthetic_branch_dispositions={k: decisions[k]['disposition'] for k in examples})


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'only default saved-certificate or --witness mode is permitted')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, lambda _number, _frame: (_ for _ in ()).throw(RuntimeError('120-second verification envelope exceeded')))
    signal.alarm(MAX_SECONDS)
    source_path = Path(__file__).resolve()
    source_before = source_path.read_bytes()
    source_sha256 = sha256(source_before).hexdigest()
    witness, held, matrix = build_witness()
    witness['checker_sha256'] = source_sha256
    witness['refusal_controls'] = refusal_controls(witness, held, matrix)
    budget('exact decision and intended-reason refusals completed')
    certificate_sha256 = None
    if not sys.argv[1:]:
        certificate_path = source_path.with_name('CERTIFICATE.json')
        certificate_before = certificate_path.read_bytes()
        verify_certificate(load_json(certificate_before), witness)
        certificate_sha256 = sha256(certificate_before).hexdigest()
        require(certificate_path.read_bytes() == certificate_before, 'saved certificate bytes changed during verification')
    for key, path in DEPENDENCY_PATHS.items():
        check_pin(path.read_bytes(), PINS[key])
    require(source_path.read_bytes() == source_before, 'checker source bytes changed during verification')
    budget()
    try:
        if sys.argv[1:]:
            print(canonical(witness), flush=True)
        else:
            result = dict(status='PASS', scope='finite RI85 four-cap exact decision only', source_sha256=source_sha256,
                          certificate_sha256=certificate_sha256, design_sha256=DESIGN_SHA256, dependencies=PINS,
                          witness_sha256=digest(witness), coverage=witness['coverage'],
                          transported_audit=witness['transported_audit'], rank=witness['exact_decision']['reduction']['rank'],
                          disposition=witness['exact_decision']['disposition'],
                          nullity=len(witness['exact_decision']['null_basis']), admission=witness['admission'],
                          intended_reason_refusal_count=len(witness['refusal_controls']['intended_reason_refusals']),
                          refusal_controls=witness['refusal_controls']['intended_reason_refusals'],
                          numerical_a6_M6_q6_q7_evaluated=False, later_h_prescribed=False)
            print(canonical(result), flush=True)
        budget()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
