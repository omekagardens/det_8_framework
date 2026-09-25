#!/usr/bin/env python3
"""RI-84: bounded exact first-departure certificate under the frozen RI-82 design.

This source is not evidence that either rank outcome has been observed.
Only a separately authorized run may replay the pinned actual RI-63 prefix
through RI-74 and query the 16 C4 and 16 C5 top-zero marked rows. New
structural work concerns only the three supported children, their maximal
deletions, two parents, and fifteen forward children up to isomorphism.
No q6/q7 probability, numerical a6/M6, optimizer, all-size continuation,
global size-seven inventory, subprocess, download or file write is used.
Generic deletion factors retain raw records before analytically justified
top-bit reduction. Zero coefficients mean zero correction, not zero q6.
JSON/budget/prefix conventions are re-expressed from RI-77/79; those sources
are not imported. The 120-second/512-MiB checkpoints complement a separately
frozen external sampled watchdog; they are not an allocator hard cap.
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
DESIGN_REFERENCE = {
    'reviewed_sha256': 'e04ef588e1617befb5e25370c33c25912a9293d9f6e4ac159d73bd9cd2f14168',
    'accepted_note_sha256': 'ae4c40c4f5c6e5af8b7811f6963b6d98afa1cec405cf53133ae4ad743c017c8b',
    'runtime_dependency': False,
}
C4, C5 = (0, 1, 3, 7), (0, 1, 3, 7, 15)
PA, PB = (0, 1, 3, 7, 15, 15), (0, 1, 3, 7, 15, 31)
PARENTS = (PA, PB)
SUPPORT = ((0, 1, 3, 7, 15, 15, 15), (0, 1, 3, 7, 15, 31, 31),
           (0, 1, 3, 7, 15, 15, 31))
PARENT_IDEALS = ((0, 1, 3, 7, 15, 31, 47, 63), (0, 1, 3, 7, 15, 31, 63))
FORWARD_SUPPORT = {(0, 15): 0, (0, 31): 2, (0, 47): 2, (1, 31): 1, (1, 15): 2}
MAX_SECONDS, MAX_BYTES = 120, 512*1024**2
START, PREFIX = None, None
DEPENDENCY_PATHS, CANONICAL = {}, {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS,
            '120-second verification envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_BYTES,
            '512-MiB resident-memory envelope exceeded')
    if stage:
        print('RI84: '+stage, file=sys.stderr, flush=True)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def load_json(text):
    def bad_constant(value):
        raise RuntimeError('nonfinite JSON constant')
    def bad_float(value):
        raise RuntimeError('JSON decimals are forbidden; use canonical rationals')
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=bad_constant, parse_float=bad_float)


def fraction(value):
    require(type(value) is str, 'noncanonical rational encoding')
    try:
        result = F(value)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError('noncanonical rational encoding') from None
    require(str(result) == value, 'noncanonical rational encoding')
    return result


def integer(value, lower, upper, reason):
    require(type(value) is int and lower <= value <= upper, reason)


def check_pin(raw, expected):
    require(sha256(raw).hexdigest() == expected, 'accepted dependency byte pin mismatch')


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


def verify_certificate(certificate, expected):
    strict_shape(certificate, expected)
    require(certificate['schema'] == expected['schema'], 'certificate schema mismatch')
    require(canonical(certificate['dependencies']) == canonical(PINS), 'certificate dependency identities changed')
    require(canonical(certificate) == canonical(expected), 'certificate finite witness mismatch')


def bits(mask):
    return tuple(v for v in range(mask.bit_length()) if mask & (1 << v))


def validate_order(order):
    require(type(order) is tuple and 0 < len(order) <= 7
            and all(type(p) is int and 0 <= p < (1 << v) for v, p in enumerate(order)),
            'invalid bounded natural order or exact mask type')
    require(all(all(order[u] & past == order[u] for u in bits(past)) for past in order),
            'order is not transitively closed')


def seed_orders():
    return frozenset((C4, C5, PA, PB)+SUPPORT
                     +tuple(p+(s,) for p, ideals in zip(PARENTS, PARENT_IDEALS) for s in ideals))


def raw_ideals(order):
    validate_order(order)
    require(order in seed_orders(), 'ideal enumeration outside frozen structural seeds')
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


def validate_permutation(permutation, n):
    integer(n, 1, 7, 'permutation dimension outside frozen exact bounds')
    require(type(permutation) is tuple and len(permutation) == n
            and all(type(v) is int for v in permutation)
            and sorted(permutation) == list(range(n)), 'invalid permutation or exact vertex type')


def transport(mask, permutation):
    validate_permutation(permutation, len(permutation) if type(permutation) is tuple else 0)
    integer(mask, 0, (1 << len(permutation))-1, 'invalid transport mask or exact integer type')
    return sum(1 << permutation[v] for v in bits(mask))


def induce(order, keep):
    validate_order(order)
    integer(keep, 0, (1 << len(order))-1, 'invalid induced-suborder keep mask')
    vertices = bits(keep)
    result = tuple(sum(1 << i for i, u in enumerate(vertices) if order[v] & (1 << u)) for v in vertices)
    validate_order(result)
    return result, vertices


def restrict_mask(mask, vertices, old_size):
    integer(old_size, 1, 7, 'restriction dimension outside frozen exact bounds')
    integer(mask, 0, (1 << old_size)-1, 'invalid restricted record or precursor mask')
    require(type(vertices) is tuple and all(type(v) is int and 0 <= v < old_size for v in vertices)
            and tuple(sorted(set(vertices))) == vertices, 'invalid induced vertex list')
    return sum(((mask >> v) & 1) << i for i, v in enumerate(vertices))


def maxima(order):
    validate_order(order)
    pasts = 0
    for past in order:
        pasts |= past
    return bits(((1 << len(order))-1) ^ pasts)


def natural_relabelings(order):
    validate_order(order)  # Guard nested bool/unhashable masks before membership/cache.
    require(order in seed_orders(), 'canonicalization seed outside frozen domain')
    return _natural_relabelings(order)


@cache
def _natural_relabelings(order):
    result = []
    for sequence in permutations(range(len(order))):
        selected = 0
        for v in sequence:
            if order[v] & selected != order[v]:
                break
            selected |= 1 << v
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


def verify_support_order(support):
    require(type(support) is tuple and len(support) == 3, 'frozen support shape changed')
    for order in support:
        validate_order(order)
    require(support == SUPPORT, 'T1 T2 T3 support or variable order changed')


def support_index(order):
    key = canonical_key(order)
    keys = tuple(canonical_key(t) for t in SUPPORT)
    return keys.index(key) if key in keys else None


def width(order):
    require(support_index(order) is not None, 'width evaluation outside supported child classes')
    return max(s.bit_count() for s in range(1 << len(order))
               if all(not order[v] & s for v in bits(s)))


def verify_deletions(rows):
    require(type(rows) is list and all(type(x) is dict for x in rows), 'invalid deletion-role container')
    for row in rows:
        integer(row['support_index'], 0, 2, 'invalid exact deletion support index')
        integer(row['deleted_vertex'], 0, 6, 'invalid exact deleted vertex')
        integer(row['parent_index'], 0, 1, 'invalid exact deletion parent index')
    expected = [(0, 4, 0), (0, 5, 0), (0, 6, 0), (1, 5, 1), (1, 6, 1), (2, 5, 1), (2, 6, 0)]
    require([(x['support_index'], x['deleted_vertex'], x['parent_index']) for x in rows] == expected,
            'maximal-deletion closure or role multiplicity mismatch')


def verify_forward(rows):
    require(type(rows) is list and all(type(x) is dict for x in rows), 'invalid forward-slot container')
    for row in rows:
        integer(row['parent_index'], 0, 1, 'invalid exact forward parent index')
        integer(row['ideal'], 0, 63, 'invalid exact forward ideal')
        require(row['support_index'] is None or type(row['support_index']) is int
                and 0 <= row['support_index'] <= 2, 'invalid exact forward support index')
    expected = [(i, s, FORWARD_SUPPORT.get((i, s))) for i in range(2) for s in PARENT_IDEALS[i]]
    require([(x['parent_index'], x['ideal'], x['support_index']) for x in rows] == expected,
            'forward individual-ideal coverage or support classification mismatch')


def build_structure():
    verify_support_order(SUPPORT)
    canonicalizations = []
    for order in sorted(seed_orders()):
        budget()
        relabelings = natural_relabelings(order)
        images = sorted(set(image for _, image in relabelings))
        key = min(images)
        for image in images:
            require(image not in CANONICAL or CANONICAL[image] == key, 'canonical classes overlap inconsistently')
            CANONICAL[image] = key
        canonicalizations.append(dict(order=order, canonical=key, natural_images=images,
                                      topological_relabelings=[dict(permutation=p, image=q) for p, q in relabelings]))
    require(tuple(canonical_key(t) for t in SUPPORT) == SUPPORT, 'frozen support representatives are not canonical')
    require(tuple(width(t) for t in SUPPORT) == (3, 2, 2), 'intrinsic support widths disagree with design')
    deletions = []
    for j, target in enumerate(SUPPORT):
        for v in maxima(target):
            parent, vertices = induce(target, 127 ^ (1 << v))
            key = canonical_key(parent)
            require(key in PARENTS, 'supported maximal deletion escaped parent closure')
            deletions.append(dict(support_index=j, deleted_vertex=v, kept_vertices=vertices,
                                  induced_parent=parent, canonical_parent=key, parent_index=PARENTS.index(key)))
    verify_deletions(deletions)
    forward = []
    for i, parent in enumerate(PARENTS):
        require(raw_ideals(parent) == PARENT_IDEALS[i], 'complete parent ideal list mismatch')
        for part in raw_ideals(parent):
            child = parent+(part,)
            forward.append(dict(parent_index=i, ideal=part, child=child,
                                canonical_child=canonical_key(child), support_index=support_index(child)))
    verify_forward(forward)
    return dict(ordered_support=[dict(variable='T'+str(j+1), order=t, canonical=canonical_key(t), width=width(t))
                                 for j, t in enumerate(SUPPORT)],
                canonicalizations=canonicalizations, maximal_deletions=deletions, forward_slots=forward)


def verify_actual_prefix(report):
    require(report['problem_sha256'] == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and report['actual_probability_manifest_sha256'] == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and report['canonical_lex_stages'] == 69 and len(report['inherited_controls']) == 15,
            'accepted actual strict prefix identity mismatch')


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
    budget('four accepted inputs pinned; replaying canonical actual strict q5 proof')
    module = runpy.run_path(str(paths['ri74_checker']))
    PREFIX = module['prefix_row']
    wrapped = getattr(PREFIX, '__wrapped__', None)
    require(wrapped is not None and hasattr(wrapped, '__globals__'), 'cached prefix helper has no underlying function')
    require(wrapped.__globals__ is module['rebuild_prefix'].__globals__, 'prefix helper globals disagree')
    report = module['rebuild_prefix']()
    live = wrapped.__globals__
    require(live['HELPER'] is not None and len(live['Q5']) == 2961, 'actual strict q5 helper state not populated')
    verify_actual_prefix(report)
    budget('accepted prefix replay complete; new held queries restricted to C4/C5 top-zero rows')
    return report


def verify_held_row(order, row):
    require(type(row) is dict and all(type(s) is int for s in row)
            and set(row) == set(raw_ideals(order))
            and all(type(q) is F and q > 0 for q in row.values())
            and sum(row.values(), F(0)) == 1, 'held row lost exact labeled ideals or strict normalization')


def held_row(order, record):
    validate_order(order)
    require(len(order) < 6, 'q6 or q7 probability lookup forbidden')
    require(order in (C4, C5), 'held parent outside frozen C4 C5 domain')
    integer(record, 0, (1 << len(order))-1, 'held record is not an exact in-range integer')
    require(record < 16, 'C5 top-one held query forbidden')
    require(PREFIX is not None, 'accepted prefix not initialized')
    row = PREFIX(order, record)
    verify_held_row(order, row)
    return dict(row)


def request_global_scale(name):
    require(name not in ('a6', 'M6', 'q6', 'q7'), 'numerical future law or global scale forbidden')
    raise RuntimeError('unknown global-scale request')


def extract_parameters(q4, q5, masks=(15, 15, 31)):
    require(type(masks) is tuple and all(type(s) is int for s in masks) and masks == (15, 15, 31),
            'C4 full C5 precursor or C5 full mask confused')
    q, p, v = q4[15], q5[15], q5[31]
    verify_full_complement(q5, v)
    return q, p, v, p*p/q


def verify_full_complement(q5, claimed):
    require(type(claimed) is F
            and claimed == 1-sum((q5[s] for s in raw_ideals(C5) if s != 31), F(0)),
            'C5 full complement omitted proper slots')


def build_held():
    held, entries, parameters = {}, [], []
    for record in range(16):
        budget()
        for order in (C4, C5):
            row = held_row(order, record)
            held[(order, record)] = row
            entries.append(dict(order=order, record=record, probabilities=[[s, str(q)] for s, q in sorted(row.items())]))
        q, p, v, alpha = extract_parameters(held[(C4, record)], held[(C5, record)])
        parameters.append(dict(record=record, q=str(q), p=str(p), v=str(v), alpha=str(alpha)))
    for order in (C4, C5):
        full = (1 << len(order))-1
        for part in raw_ideals(order):
            if part == full:
                continue
            local = {}
            for record in range(16):
                key, q = record & part, held[(order, record)][part]
                require(key not in local or local[key] == q, 'held proper probability reads a nonprecursor base bit')
                local[key] = q
    require(len(entries) == 32 and sum(len(r['probabilities']) for r in entries) == 176,
            'held marked-row or probability-slot coverage mismatch')
    return held, entries, parameters


def parameter_values(parameters, record):
    integer(record, 0, 15, 'base parameter record outside frozen domain')
    row = parameters[record]
    require(type(row['record']) is int and row['record'] == record, 'parameter row ordering changed')
    return tuple(fraction(row[k]) for k in ('q', 'p', 'v', 'alpha'))


def compact_coefficients(parent_index, record, parameters):
    integer(parent_index, 0, 1, 'invalid exact parent index')
    _, p, v, alpha = parameter_values(parameters, record)
    return (alpha, F(0), 2*v) if parent_index == 0 else (F(0), v, p)


def verify_factor_transport(factor, order, record, part):
    validate_order(order)
    require(order in PARENTS, 'factor parent outside frozen domain')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(part, 0, 63, 'precursor is not an exact in-range integer')
    deletion = factor['deleted_mask']
    integer(deletion, 1, 63, 'invalid exact maximal-deletion mask')
    omitted = sum(1 << v for v in maxima(order) if not part & (1 << v))
    require(deletion & omitted == deletion, 'deleted vertices are not omitted maxima')
    keep = 63 ^ deletion
    smaller, vertices = induce(order, keep)
    raw_record = restrict_mask(record, vertices, 6)
    precursor = restrict_mask(part, vertices, 6)
    local = raw_record if precursor == (1 << len(smaller))-1 else raw_record & precursor
    reduced = local & 15
    require(type(factor['kept_vertices']) is list and all(type(v) is int for v in factor['kept_vertices'])
            and type(factor['induced_order']) is list and all(type(p) is int for p in factor['induced_order']),
            'induced vertex or order entries are not exact integers')
    require(factor['kept_vertices'] == list(vertices) and factor['induced_order'] == list(smaller)
            and type(factor['induced_precursor']) is int and factor['induced_precursor'] == precursor
            and type(factor['raw_transported_record']) is int and factor['raw_transported_record'] == raw_record
            and type(factor['local_read_record']) is int and factor['local_read_record'] == local
            and type(factor['held_query_record']) is int and factor['held_query_record'] == reduced,
            'induced record precursor or top-reduction transport corrupted')


def supported_potential(parent_index, record, part, held):
    integer(parent_index, 0, 1, 'invalid exact parent index')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(part, 0, 63, 'precursor is not an exact in-range integer')
    require((parent_index, part) in FORWARD_SUPPORT, 'potential request outside supported proper ideals')
    order = PARENTS[parent_index]
    omitted = sum(1 << v for v in maxima(order) if not part & (1 << v))
    deletion, value, factors = omitted, F(1), []
    while deletion:
        smaller, vertices = induce(order, 63 ^ deletion)
        require(smaller in (C4, C5), 'supported factor escaped held C4 C5 orders')
        precursor = restrict_mask(part, vertices, 6)
        raw_record = restrict_mask(record, vertices, 6)
        local = raw_record if precursor == (1 << len(smaller))-1 else raw_record & precursor
        reduced = local & 15
        require((smaller == C4 and precursor == 15) or (smaller == C5 and precursor in (15, 31)),
                'supported factor escaped frozen held precursor slots')
        q = held[(smaller, reduced)][precursor]
        exponent = 1 if deletion.bit_count() % 2 else -1
        value = value*q if exponent == 1 else value/q
        factor = dict(deleted_mask=deletion, kept_vertices=list(vertices), induced_order=list(smaller),
                      induced_precursor=precursor, raw_transported_record=raw_record,
                      local_read_record=local, held_query_record=reduced,
                      proper_locality_applied=precursor != (1 << len(smaller))-1,
                      top_zero_projection_theorem=('unique-maximum proper locality and full complement' if smaller == C5 else None),
                      exponent=exponent, probability=str(q))
        verify_factor_transport(factor, order, record, part)
        factors.append(factor)
        deletion = (deletion-1) & omitted
    require(factors and value > 0, 'supported deletion potential lost positivity')
    return value, factors


def verify_expanded_row(row, parameters):
    i, record = row['parent_index'], row['record']
    integer(i, 0, 1, 'invalid exact parent index')
    integer(record, 0, 63, 'expanded record is not an exact in-range integer')
    integer(row['base_record'], 0, 15, 'expanded base record is not an exact in-range integer')
    require(row['base_record'] == record & 15, 'expanded base-record reduction changed')
    require(type(row['entries']) is list, 'expanded ideal entries are not a list')
    for item in row['entries']:
        integer(item['ideal'], 0, 63, 'precursor is not an exact in-range integer')
    require([x['ideal'] for x in row['entries']] == list(PARENT_IDEALS[i]),
            'expanded row lost individual-ideal coverage')
    total = [F(0), F(0), F(0)]
    for item in row['entries']:
        integer(item['ideal'], 0, 63, 'precursor is not an exact in-range integer')
        index = FORWARD_SUPPORT.get((i, item['ideal']))
        require(item['support_index'] == index and (index is None or type(item['support_index']) is int),
                'expanded support-class index changed')
        value = fraction(item['correction_coefficient'])
        require((index is None and value == 0 and item['factors'] == []) or (index is not None and value > 0),
                'unsupported correction confused with a probability or supported positivity')
        if index is not None:
            total[index] += value
    expected = compact_coefficients(i, record & 15, parameters)
    require(tuple(total) == expected and row['coefficients'] == [str(v) for v in expected],
            'expanded coefficient multiplicity or top-bit reduction mismatch')


def verify_expanded_coverage(rows):
    require(type(rows) is list and all(type(row) is dict for row in rows), 'invalid expanded-row container')
    for row in rows:
        integer(row['parent_index'], 0, 1, 'invalid exact parent index')
        integer(row['record'], 0, 63, 'expanded record is not an exact in-range integer')
    require([(row['parent_index'], row['record']) for row in rows] == [(i, r) for i in range(2) for r in range(64)],
            'complete expanded marked-row coverage mismatch')


def build_expanded(held, parameters, structure):
    forwards = {(x['parent_index'], x['ideal']): x for x in structure['forward_slots']}
    rows = []
    for i, parent in enumerate(PARENTS):
        for record in range(64):
            budget()
            entries, total = [], [F(0), F(0), F(0)]
            for part in PARENT_IDEALS[i]:
                index = FORWARD_SUPPORT.get((i, part))
                value, factors = (F(0), []) if index is None else supported_potential(i, record, part, held)
                if index is not None:
                    total[index] += value
                entries.append(dict(ideal=part, canonical_child=forwards[(i, part)]['canonical_child'],
                                    support_index=index, correction_coefficient=str(value), factors=factors,
                                    baseline_probability_computed=False))
            row = dict(parent_index=i, record=record, base_record=record & 15,
                       entries=entries, coefficients=[str(v) for v in total])
            verify_expanded_row(row, parameters)
            rows.append(row)
    verify_expanded_coverage(rows)
    require(sum(len(r['entries']) for r in rows) == 960
            and sum(x['support_index'] is not None for r in rows for x in r['entries']) == 320
            and sum(x['support_index'] is None for r in rows for x in r['entries']) == 640,
            'expanded correction-occurrence coverage mismatch')
    return rows


def check_equivariance(rows):
    table = {(r['parent_index'], r['record']): {x['ideal']: x for x in r['entries']} for r in rows}
    cases = []
    for i, parent in enumerate(PARENTS):
        for permutation, image in natural_relabelings(parent):
            require(image == parent, 'affected parent acquired an unexpected natural representative')
            for record in range(64):
                moved_record = transport(record, permutation)
                for part in PARENT_IDEALS[i]:
                    moved_part = transport(part, permutation)
                    a, b = table[(i, record)][part], table[(i, moved_record)][moved_part]
                    require(a['support_index'] == b['support_index']
                            and a['correction_coefficient'] == b['correction_coefficient'],
                            'labeled correction failed transported-record equivariance')
                    cases.append([i, record, part, permutation, moved_record, moved_part])
    return dict(transported_marked_ideal_cases=len(cases), manifest_sha256=digest(cases))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def determinant(rows):
    a, b, c = rows
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])


def verify_amplitude(k, ell, epsilon, values):
    require(k > 0 and ell > 0 and epsilon > 0 and epsilon < 1/k,
            'amplitude is outside the strict positive interval')
    expected = (1+epsilon, 1+epsilon*k*ell, 1-epsilon*k)
    require(tuple(values) == expected and all(v > 0 for v in values), 'positive supported h values corrupted')


def verify_width(alpha, v, z, epsilon, functional, gain, conditioning):
    require(conditioning == 'complete parent row; both fair newborn bits summed',
            'width target conditions on a proper or supported birth')
    expected = 3*alpha*z[0]+4*v*z[2]
    require(functional == expected == alpha and gain == epsilon*expected and gain > 0,
            'complete-row width functional or positive gain corrupted')


def decide(parameters, expanded):
    _, p0, v0, alpha0 = parameter_values(parameters, 0)
    k, ell = alpha0/(2*v0), p0/v0
    z = (F(1), k*ell, -k)
    require(k > 0 and ell > 0, 'positive reference scales lost')
    compact = []
    for record in range(16):
        _, p, v, alpha = parameter_values(parameters, record)
        for i in range(2):
            coefficients = compact_coefficients(i, record, parameters)
            residual = alpha-2*v*k if i == 0 else p-v*ell
            require(dot(coefficients, z) == (residual if i == 0 else -k*residual),
                    'compact residual disagrees with normalized direction')
            compact.append(dict(record=record, parent_index=i, coefficients=[str(c) for c in coefficients],
                                balance_residual=str(residual), direction_dot=str(dot(coefficients, z))))
    first = next((index for index, row in enumerate(compact) if fraction(row['balance_residual']) != 0), None)
    references = (compact_coefficients(0, 0, parameters), compact_coefficients(1, 0, parameters))
    require(references[0][0]*references[1][1] > 0, 'reference rows are not independent')
    decision = dict(k=str(k), ell=str(ell), normalized_direction=[str(x) for x in z],
                    reference_rows=[[str(x) for x in row] for row in references],
                    compact_order='record 0..15; A before B', first_failed_compact_index=first,
                    rank=2 if first is None else 3, admission=None, minor=None,
                    disposition='positive_finite_prefix_width_bias' if first is None else 'no_nonzero_perturbation_on_frozen_support')
    for row in expanded:
        row['direction_residual'] = str(dot(tuple(fraction(c) for c in row['coefficients']), z))
    if first is not None:
        failed = compact[first]
        r, i = failed['record'], failed['parent_index']
        _, p, v, alpha = parameter_values(parameters, r)
        matrix = references+(compact_coefficients(i, r, parameters),)
        direct = determinant(matrix)
        formula = 2*v0*(alpha0*v-v0*alpha) if i == 0 else alpha0*(v0*p-p0*v)
        require(direct == formula and direct != 0
                and direct == -2*v0*v0*dot(matrix[2], z), 'first failed reference minor identity failed')
        decision['minor'] = dict(compact_index=first, matrix=[[str(x) for x in row] for row in matrix],
                                 determinant=str(direct), explicit_formula=str(formula))
    else:
        epsilon = 1/(2*k)
        values = (1+epsilon, 1+epsilon*k*ell, 1-epsilon*k)
        verify_amplitude(k, ell, epsilon, values)
        require(all(fraction(row['direction_residual']) == 0 for row in expanded),
                'claimed feasible direction fails an expanded row')
        target = next(row for row in expanded if row['parent_index'] == 0 and row['record'] == 0)
        functional = sum((fraction(x['correction_coefficient'])*z[x['support_index']]*width(SUPPORT[x['support_index']])
                          for x in target['entries'] if x['support_index'] is not None), F(0))
        conditioning = 'complete parent row; both fair newborn bits summed'
        gain = epsilon*functional
        verify_width(alpha0, v0, z, epsilon, functional, gain, conditioning)
        require(gain == v0, 'interior scaled width gain does not equal v0')
        decision['admission'] = dict(epsilon=str(epsilon), interval_upper=str(1/k), h_values=[str(h) for h in values],
                                     scaled_width_functional=str(functional), gain_divided_by_a6=str(gain),
                                     conditioning=conditioning, numerical_a6=None,
                                     expanded_normalization_corrections=[str(epsilon*fraction(row['direction_residual'])) for row in expanded])
    return compact, decision


def verify_decision(claim, parameters, expanded):
    # Work on a JSON copy so validation does not change the retained row list.
    _, expected = decide(parameters, load_json(canonical(expanded)))
    require(canonical(claim) == canonical(expected), 'rank residual minor or disposition corrupted')


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': wrong rejection reason')
        return name
    raise RuntimeError(name+': malformed candidate accepted')


def synthetic_decision_fixture(failed_parent=None):
    """Algebra only: not inherited prefix values or a claimed native law.

    Both rank branches are tested even if the actual held rows have only one
    outcome. The fixture reuses declared slot labels and makes no helper query.
    """
    parameters = [dict(record=r, q='1/2', p='1/2', v='1/4', alpha='1/2') for r in range(16)]
    if failed_parent == 0:
        parameters[1].update(q='1/4', alpha='1')
    elif failed_parent == 1:
        parameters[1].update(q='1/8', p='1/4', alpha='1/2')
    else:
        require(failed_parent is None, 'invalid synthetic rank fixture')
    rows = []
    for i in range(2):
        for record in range(64):
            _, p, v, alpha = parameter_values(parameters, record & 15)
            values = {(0, 15): alpha, (0, 31): v, (0, 47): v, (1, 31): v, (1, 15): p}
            entries = [dict(ideal=s, support_index=FORWARD_SUPPORT.get((i, s)),
                            correction_coefficient=str(values.get((i, s), F(0)))) for s in PARENT_IDEALS[i]]
            rows.append(dict(parent_index=i, record=record,
                             coefficients=[str(x) for x in compact_coefficients(i, record & 15, parameters)], entries=entries))
    return parameters, rows


def controls(witness, held):
    """Intended-reason refusals; no additional inherited probability queries."""
    result = []

    def reject(name, function, reason):
        result.append(expect_rejection(name, function, reason))

    def copy(value):
        return load_json(canonical(value))

    # Public guards run before membership and before any cached function.
    # These valid keys are already warm from the main reconstruction.
    reject('oversized_order', lambda: canonical_key((0,)*8), 'invalid bounded natural order or exact mask type')
    reject('extra_canonical_seed', lambda: natural_relabelings((0,)*6), 'canonicalization seed outside frozen domain')
    reject('warm_nested_boolean_order', lambda: natural_relabelings((0, True, 3, 7)),
           'invalid bounded natural order or exact mask type')
    reject('unhashable_nested_order', lambda: natural_relabelings((0, [1], 3, 7)),
           'invalid bounded natural order or exact mask type')
    reject('unhashable_order_container', lambda: canonical_key([0, 1, 3, 7]),
           'invalid bounded natural order or exact mask type')
    reject('warm_boolean_held_record', lambda: held_row(C4, True), 'held record is not an exact in-range integer')
    reject('unhashable_held_record', lambda: held_row(C4, []), 'held record is not an exact in-range integer')
    reject('out_of_range_base_record', lambda: held_row(C4, 16), 'held record is not an exact in-range integer')
    reject('top_one_held_query', lambda: held_row(C5, 16), 'C5 top-one held query forbidden')
    reject('six_parent_probability', lambda: held_row(PA, 0), 'q6 or q7 probability lookup forbidden')
    reject('seven_parent_probability', lambda: held_row(SUPPORT[0], 0), 'q6 or q7 probability lookup forbidden')
    reject('other_held_parent', lambda: held_row((0,)*4, 0), 'held parent outside frozen C4 C5 domain')
    for name in ('a6', 'M6', 'q6', 'q7'):
        reject('forbidden_'+name, lambda name=name: request_global_scale(name),
               'numerical future law or global scale forbidden')
    reject('boolean_precursor', lambda: supported_potential(0, 0, True, held), 'precursor is not an exact in-range integer')
    reject('unhashable_precursor', lambda: supported_potential(0, 0, [], held), 'precursor is not an exact in-range integer')
    reject('full_precursor_potential', lambda: supported_potential(0, 0, 63, held),
           'potential request outside supported proper ideals')
    reject('boolean_parent_index', lambda: supported_potential(False, 0, 15, held), 'invalid exact parent index')
    reject('boolean_permutation_vertex', lambda: transport(1, (False, 1, 2, 3)),
           'invalid permutation or exact vertex type')
    reject('unhashable_permutation_vertex', lambda: transport(1, ([], 1, 2, 3)),
           'invalid permutation or exact vertex type')
    reject('boolean_permutation_dimension', lambda: validate_permutation((0,), True),
           'permutation dimension outside frozen exact bounds')
    reject('oversized_permutation_dimension', lambda: validate_permutation(tuple(range(8)), 8),
           'permutation dimension outside frozen exact bounds')
    reject('boolean_transport_mask', lambda: transport(True, (0, 1, 2, 3)),
           'invalid transport mask or exact integer type')
    reject('boolean_restriction_dimension', lambda: restrict_mask(0, (0,), True),
           'restriction dimension outside frozen exact bounds')
    reject('unhashable_restriction_vertices', lambda: restrict_mask(0, ([0],), 4), 'invalid induced vertex list')

    reject('extra_support', lambda: verify_support_order(SUPPORT+(SUPPORT[0],)), 'frozen support shape changed')
    reject('canonical_sort_reorders_variables', lambda: verify_support_order((SUPPORT[0], SUPPORT[2], SUPPORT[1])),
           'T1 T2 T3 support or variable order changed')
    deletions = copy(witness['structure']['maximal_deletions'])
    reject('missing_maximal_deletion', lambda: verify_deletions(deletions[:-1]),
           'maximal-deletion closure or role multiplicity mismatch')
    altered = copy(deletions)
    altered[0]['support_index'] = False
    reject('boolean_deletion_index', lambda: verify_deletions(altered), 'invalid exact deletion support index')
    forward = copy(witness['structure']['forward_slots'])
    altered_forward = copy(forward)
    next(x for x in altered_forward if x['parent_index'] == 0 and x['ideal'] == 47)['support_index'] = None
    reject('literal_T3_misclassification', lambda: verify_forward(altered_forward),
           'forward individual-ideal coverage or support classification mismatch')
    reject('merged_distinct_arm_ideals', lambda: verify_forward([x for x in forward if not (x['parent_index'] == 0 and x['ideal'] == 47)]),
           'forward individual-ideal coverage or support classification mismatch')
    boolean_forward = copy(forward)
    boolean_forward[0]['ideal'] = False
    reject('boolean_forward_ideal', lambda: verify_forward(boolean_forward), 'invalid exact forward ideal')
    expanded = witness['expanded_rows']
    reject('missing_marked_row', lambda: verify_expanded_coverage(expanded[:-1]), 'complete expanded marked-row coverage mismatch')
    boolean_coverage = copy(expanded)
    boolean_coverage[0]['parent_index'] = False
    reject('boolean_coverage_parent', lambda: verify_expanded_coverage(boolean_coverage), 'invalid exact parent index')
    boolean_row = copy(expanded[0])
    boolean_row['base_record'] = False
    reject('boolean_base_record', lambda: verify_expanded_row(boolean_row, witness['parameters']),
           'expanded base record is not an exact in-range integer')
    top_leak = copy(expanded[16])
    top_leak['coefficients'][0] = str(fraction(top_leak['coefficients'][0])+1)
    reject('retained_top_bit_changes_coefficient', lambda: verify_expanded_row(top_leak, witness['parameters']),
           'expanded coefficient multiplicity or top-bit reduction mismatch')
    multiplicity = copy(expanded[0])
    next(x for x in multiplicity['entries'] if x['ideal'] == 31)['correction_coefficient'] = str(
        2*fraction(next(x for x in multiplicity['entries'] if x['ideal'] == 31)['correction_coefficient']))
    reject('backward_role_multiplies_forward_mass', lambda: verify_expanded_row(multiplicity, witness['parameters']),
           'expanded coefficient multiplicity or top-bit reduction mismatch')
    factor = copy(next(x for x in expanded[16]['entries'] if x['ideal'] == 31)['factors'][0])
    raw_top = copy(factor)
    raw_top['held_query_record'] = raw_top['raw_transported_record']
    reject('raw_top_bit_not_reduced', lambda: verify_factor_transport(raw_top, PA, 16, 31),
           'induced record precursor or top-reduction transport corrupted')
    boolean_factor = copy(factor)
    boolean_factor['kept_vertices'][0] = False
    reject('boolean_induced_vertex', lambda: verify_factor_transport(boolean_factor, PA, 16, 31),
           'induced vertex or order entries are not exact integers')
    raw_erasure = copy(factor)
    raw_erasure['raw_transported_record'] = 0
    reject('raw_record_erased_before_evidence', lambda: verify_factor_transport(raw_erasure, PA, 16, 31),
           'induced record precursor or top-reduction transport corrupted')
    wrong_precursor = copy(factor)
    wrong_precursor['induced_precursor'] = 15
    reject('transported_full_precursor_mislabeled', lambda: verify_factor_transport(wrong_precursor, PA, 16, 31),
           'induced record precursor or top-reduction transport corrupted')

    q4, q5 = held[(C4, 0)], held[(C5, 0)]
    reject('wrong_full_slot_mask', lambda: extract_parameters(q4, q5, (15, 15, 15)),
           'C4 full C5 precursor or C5 full mask confused')
    reject('full_complement_is_not_one_minus_p', lambda: verify_full_complement(q5, 1-q5[15]),
           'C5 full complement omitted proper slots')
    bad_row = dict(q5)
    bad_row[31] += 1
    reject('held_row_normalization', lambda: verify_held_row(C5, bad_row),
           'held row lost exact labeled ideals or strict normalization')
    bad_prefix = copy(witness['accepted_prefix'])
    bad_prefix['actual_probability_manifest_sha256'] = '0'*64
    reject('boundary_instead_of_actual_q5', lambda: verify_actual_prefix(bad_prefix),
           'accepted actual strict prefix identity mismatch')
    reject('changed_dependency_bytes', lambda: check_pin(b'not the pinned input', PINS['ri74_checker']),
           'accepted dependency byte pin mismatch')

    # Synthetic algebraic fixtures exercise both branches without asserting an
    # outcome for the actual prefix and without querying a single extra row.
    sp, sr = synthetic_decision_fixture()
    _, sd = decide(sp, sr)
    require(sd['rank'] == 2 and sd['admission'] is not None, 'synthetic rank-two control fixture failed')
    k, ell = fraction(sd['k']), fraction(sd['ell'])
    eps = fraction(sd['admission']['epsilon'])
    h = tuple(fraction(x) for x in sd['admission']['h_values'])
    reject('synthetic_zero_amplitude', lambda: verify_amplitude(k, ell, F(0), h),
           'amplitude is outside the strict positive interval')
    reject('synthetic_endpoint_amplitude', lambda: verify_amplitude(k, ell, 1/k, h),
           'amplitude is outside the strict positive interval')
    reject('synthetic_nonpositive_h', lambda: verify_amplitude(k, ell, eps, (h[0], h[1], F(0))),
           'positive supported h values corrupted')
    _, _, v0, alpha0 = parameter_values(sp, 0)
    z = tuple(fraction(x) for x in sd['normalized_direction'])
    conditioning = 'complete parent row; both fair newborn bits summed'
    reject('synthetic_wrong_width_sign', lambda: verify_width(alpha0, v0, z, eps, -alpha0, -eps*alpha0, conditioning),
           'complete-row width functional or positive gain corrupted')
    reject('synthetic_proper_birth_conditioning', lambda: verify_width(alpha0, v0, z, eps, alpha0, eps*alpha0, 'proper births only'),
           'width target conditions on a proper or supported birth')
    for failed_parent in (0, 1):
        fp, fr = synthetic_decision_fixture(failed_parent)
        _, fd = decide(fp, fr)
        require(fd['rank'] == 3 and fd['first_failed_compact_index'] == 2+failed_parent
                and fd['admission'] is None, 'synthetic rank-three control fixture failed')
        wrong_minor = copy(fd)
        wrong_minor['minor']['determinant'] = '0'
        reject('synthetic_wrong_'+('A' if failed_parent == 0 else 'B')+'_minor',
               lambda wrong_minor=wrong_minor, fp=fp, fr=fr: verify_decision(wrong_minor, fp, fr),
               'rank residual minor or disposition corrupted')
        wrong_first = copy(fd)
        wrong_first['first_failed_compact_index'] = fd['first_failed_compact_index']+1
        reject('synthetic_wrong_first_'+('A' if failed_parent == 0 else 'B')+'_failure',
               lambda wrong_first=wrong_first, fp=fp, fr=fr: verify_decision(wrong_first, fp, fr),
               'rank residual minor or disposition corrupted')
        fabricated = copy(fd)
        fabricated['admission'] = copy(sd['admission'])
        reject('synthetic_rank_three_fabricated_admission_'+str(failed_parent),
               lambda fabricated=fabricated, fp=fp, fr=fr: verify_decision(fabricated, fp, fr),
               'rank residual minor or disposition corrupted')
    changed_decision = copy(witness['decision'])
    changed_decision['disposition'] = 'unproved contrary outcome'
    reject('forged_actual_disposition', lambda: verify_decision(changed_decision, witness['parameters'], expanded),
           'rank residual minor or disposition corrupted')

    reject('duplicate_JSON_key', lambda: load_json('{"x":0,"x":1}'), 'duplicate JSON object key')
    reject('nonfinite_JSON', lambda: load_json('{"x":NaN}'), 'nonfinite JSON constant')
    reject('decimal_JSON', lambda: load_json('{"x":0.5}'), 'JSON decimals are forbidden; use canonical rationals')
    reject('noncanonical_rational', lambda: fraction('2/4'), 'noncanonical rational encoding')
    reject('boolean_rational', lambda: fraction(True), 'noncanonical rational encoding')
    extra = copy(witness)
    extra['additional_support'] = []
    reject('extra_certificate_field', lambda: verify_certificate(extra, witness), 'certificate object fields mismatch')
    alias = copy(witness)
    alias['coverage']['supported_child_classes'] = True
    reject('boolean_certificate_integer', lambda: verify_certificate(alias, witness), 'certificate value type mismatch')
    # These exercise whole-certificate reconstruction equality. Transport-only
    # validation above does not claim to re-evaluate a saved factor's arithmetic.
    residual = copy(witness)
    residual['compact_rows'][0]['balance_residual'] = '1'
    reject('forged_saved_compact_residual', lambda: verify_certificate(residual, witness),
           'certificate finite witness mismatch')
    factor_probability = copy(witness)
    saved_factor = next(x for x in factor_probability['expanded_rows'][0]['entries'] if x['ideal'] == 15)['factors'][0]
    saved_factor['probability'] = str(fraction(saved_factor['probability'])+1)
    reject('forged_saved_factor_probability', lambda: verify_certificate(factor_probability, witness),
           'certificate finite witness mismatch')
    factor_exponent = copy(witness)
    saved_exponent = next(x for x in factor_exponent['expanded_rows'][0]['entries'] if x['ideal'] == 15)['factors'][0]
    saved_exponent['exponent'] = -saved_exponent['exponent']
    reject('forged_saved_factor_exponent', lambda: verify_certificate(factor_exponent, witness),
           'certificate finite witness mismatch')
    forged = copy(witness)
    forged['checker_sha256'] = '0'*64
    reject('forged_saved_witness', lambda: verify_certificate(forged, witness), 'certificate finite witness mismatch')
    return result


def deadline(signum, frame):
    raise RuntimeError('120-second wall-time alarm expired')


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    source = Path(__file__).read_bytes()
    try:
        prefix = rebuild_prefix()
        budget('checking only declared structural isomorphism classes and labeled slots')
        structure = build_structure()
        held, held_rows, parameters = build_held()
        expanded = build_expanded(held, parameters, structure)
        equivariance = check_equivariance(expanded)
        compact, decision = decide(parameters, expanded)
        verify_decision(decision, parameters, expanded)
        coverage = dict(supported_child_classes=3, maximal_deletion_roles=len(structure['maximal_deletions']),
                        forward_slots=len(structure['forward_slots']), held_rows=len(held_rows),
                        held_probability_slots=sum(len(x['probabilities']) for x in held_rows),
                        expanded_rows=len(expanded), ideal_occurrences=sum(len(r['entries']) for r in expanded),
                        supported_occurrences=sum(x['support_index'] is not None for r in expanded for x in r['entries']),
                        zero_correction_occurrences=sum(x['support_index'] is None for r in expanded for x in r['entries']),
                        full_birth_occurrences=sum(x['ideal'] == 63 for r in expanded for x in r['entries']),
                        deletion_factors=sum(len(x['factors']) for r in expanded for x in r['entries']),
                        compact_rows=len(compact))
        require(coverage == dict(supported_child_classes=3, maximal_deletion_roles=7, forward_slots=15,
                                 held_rows=32, held_probability_slots=176, expanded_rows=128,
                                 ideal_occurrences=960, supported_occurrences=320,
                                 zero_correction_occurrences=640, full_birth_occurrences=128,
                                 deletion_factors=448, compact_rows=32),
                'complete frozen-domain coverage mismatch')
        witness = load_json(canonical(dict(schema='ri84-first-departure-v1', checker_sha256=sha256(source).hexdigest(),
                       design_reference=DESIGN_REFERENCE, dependencies=PINS, accepted_prefix=prefix,
                       scope=dict(new_structural_order_cap=7, q6_q7_probabilities_computed=False,
                                  numerical_a6_M6_computed=False, support_expansion=False, optimizer_calls=0,
                                  all_size_continuation=False, law_adopted=False, C5_query_top_bit=0),
                       structure=structure, held_rows=held_rows, parameters=parameters,
                       compact_rows=compact, expanded_rows=expanded, equivariance=equivariance,
                       coverage=coverage, decision=decision)))
        negative = controls(witness, held)
        for key, path in DEPENDENCY_PATHS.items():
            check_pin(path.read_bytes(), PINS[key])
        require(Path(__file__).read_bytes() == source, 'checker source changed during verification')
        budget('bounded witness and intended-reason controls complete; either rank outcome is admissible')
        if sys.argv[1:] == ['--witness']:
            print(canonical(witness))
        else:
            saved = load_json(Path(__file__).with_name('CERTIFICATE.json').read_bytes())
            verify_certificate(saved, witness)
            print('accepted_prefix='+canonical(prefix))
            print('coverage='+canonical(coverage))
            print('equivariance='+canonical(equivariance))
            print('decision='+canonical(decision))
            print('negative_controls='+canonical(negative))
            print('witness_sha256='+digest(witness))
            print('DONE: frozen-support finite-prefix decision only; no numerical q6 or all-size harmonic solution')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
