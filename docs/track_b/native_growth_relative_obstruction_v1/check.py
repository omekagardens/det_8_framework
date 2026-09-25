#!/usr/bin/env python3
"""RI-91: exact certificate-data-only first-continuation obstruction test.

Source preparation is not coefficient execution. The sole scientific input
is the byte-pinned accepted RI-88 certificate. Arithmetic extracts only six
complete rows (32 probabilities) and H1,H2,H3. No helper or prefix is run.
rho and s remain formal variables. The only numerical scale evaluations are
the predeclared polynomial proof boundary rho=R and its algebraic root check;
they are never asserted to be the unknown actual global scales.
The fixed test divides by rho**2 and uses Bernstein degrees 2 and 6, without
subdivision, adaptive elevation, optimization, other records or parents.
The checker emits JSON to stdout and writes no file. Internal 120-second /
512-MiB checks supplement a separately authorized sampled external watchdog.
"""

from fractions import Fraction as Q
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import resource
import signal
import sys
import time


INPUT_SHA256 = 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'
INPUT_BYTES = 1828149
DESIGN_SHA256 = '56c45bb5aba5e9fa0ab1f09ff959a73235939cc850e6fdde91a4cc39180b5cd1'
DESIGN_BYTES = 21769
RI88_CHECKER = '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
RI85_DESIGN = 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a'
INHERITED_PINS = {
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
}
RI88_KEYS = {'admission', 'checker_sha256', 'compact_rows', 'coverage', 'dependencies', 'design_sha256',
             'domain', 'exact_decision', 'expanded_rows', 'held_rows', 'parameters', 'prefix',
             'refusal_controls', 'schema', 'structure', 'transported_audit', 'width_target'}
C3, C4, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 7)
P6, P7 = (0, 1, 3, 7, 7, 7), (0, 1, 3, 7, 7, 7, 7)
HELD = (C3, C4, H5)
HELD_IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 23, 31))
PROPER6 = (0, 1, 3, 7, 15, 23, 31, 39, 47, 55)
PROPER7 = (0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 119)
START = None
MAX_SECONDS, MAX_BYTES, MAX_DEGREE = 120, 512*1024**2, 8


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def exact_int(value, low, high, message):
    require(type(value) is int and low <= value <= high, message)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS, '120-second envelope exceeded')
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((rss if sys.platform == 'darwin' else 1024*rss) <= MAX_BYTES, '512-MiB resident envelope exceeded')
    if stage:
        print('RI91: '+stage, file=sys.stderr, flush=True)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def load_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def forbidden(_value):
        raise RuntimeError('JSON decimal or nonfinite value forbidden')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=forbidden, parse_constant=forbidden)


def copy_json(value):
    return load_json(canonical(value))


def rational(value):
    require(type(value) is str, 'noncanonical rational encoding')
    try:
        result = Q(value)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError('noncanonical rational encoding') from None
    require(str(result) == value, 'noncanonical rational encoding')
    return result


def strict_shape(value, reference):
    require(type(value) is type(reference), 'certificate exact value type mismatch')
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
    require(saved['schema'] == 'ri91-relative-obstruction-v1', 'certificate schema mismatch')
    require(canonical(saved) == canonical(expected), 'certificate exact reconstructed witness mismatch')


def verify_input_bytes(raw):
    require(type(raw) is bytes and len(raw) == INPUT_BYTES, 'accepted RI88 certificate byte size mismatch')
    require(sha256(raw).hexdigest() == INPUT_SHA256, 'accepted RI88 certificate byte hash mismatch')


def verify_provenance(data):
    require(type(data) is dict and set(data) == RI88_KEYS, 'accepted RI88 top-level schema changed')
    require(data['schema'] == 'ri88-four-vertex-cap-v1' and data['checker_sha256'] == RI88_CHECKER
            and data['design_sha256'] == RI85_DESIGN, 'accepted RI88 source provenance changed')
    require(type(data['dependencies']) is dict and canonical(data['dependencies']) == canonical(INHERITED_PINS),
            'accepted inherited dependency provenance changed')
    require(type(data['admission']) is dict and data['admission'].get('epsilon') == '1/4'
            and data['admission'].get('later_h_prescribed') is False
            and data['admission'].get('numerical_a6_evaluated') is False,
            'accepted finite-prefix admission provenance changed')
    require(type(data['exact_decision']) is dict
            and data['exact_decision'].get('disposition') == 'positive-finite-width-bias',
            'accepted RI88 positive disposition changed')
    prefix = data['prefix']
    require(type(prefix) is dict
            and prefix.get('problem_sha256') == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and prefix.get('actual_probability_manifest_sha256') == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and type(prefix.get('canonical_lex_stages')) is int and prefix['canonical_lex_stages'] == 69,
            'accepted actual strict-prefix provenance changed')
    coverage = data['coverage']
    require(type(coverage) is dict and type(coverage.get('held_marked_rows')) is int
            and coverage['held_marked_rows'] == 40 and type(coverage.get('held_probability_slots')) is int
            and coverage['held_probability_slots'] == 224, 'accepted held-coverage provenance changed')


def validate_order(order):
    require(type(order) is tuple and all(type(x) is int for x in order)
            and order in HELD+(P6, P7), 'order outside frozen exact structural domain')


def validate_record(record):
    exact_int(record, 0, 1, 'record outside the two frozen exact markings')


def validate_held_entry(entry):
    require(type(entry) is dict and set(entry) == {'order', 'record', 'probabilities'}, 'held row fields changed')
    require(type(entry['order']) is list and all(type(x) is int for x in entry['order']), 'held order exact mask types changed')
    order = tuple(entry['order'])
    require(order in HELD, 'held row outside C3 C4 H5 extraction domain')
    validate_record(entry['record'])
    values = entry['probabilities']
    require(type(values) is list and all(type(pair) is list and len(pair) == 2 and type(pair[0]) is int for pair in values),
            'held probability slots have invalid exact shape')
    require([pair[0] for pair in values] == list(HELD_IDEALS[HELD.index(order)]), 'held row lost labeled ideal coverage')
    row = {s: rational(q) for s, q in values}
    require(all(q > 0 for q in row.values()) and sum(row.values(), Q(0)) == 1, 'held row lost strict positive normalization')
    return row


def verify_multipliers(multipliers):
    require(type(multipliers) is list and len(multipliers) == 3 and all(type(q) is Q and q > 0 for q in multipliers),
            'selected terminal multipliers lost exact positive three-value domain')
    require(multipliers[0] == Q(5, 4), 'accepted H1 multiplier changed')
    require(all(Q(3, 4) <= q <= Q(5, 4) for q in multipliers), 'accepted multiplier interval changed')


def extract_input(data):
    verify_provenance(data)
    require(type(data['held_rows']) is list and len(data['held_rows']) == 40, 'accepted held-row inventory changed')
    selected = {}
    # Inspect order/record metadata only on the other 34 rows. Their rational
    # strings are authenticated by the full byte pin, never used in arithmetic.
    for entry in data['held_rows']:
        require(type(entry) is dict and set(entry) == {'order', 'record', 'probabilities'}, 'accepted held metadata fields changed')
        require(type(entry['order']) is list and all(type(x) is int for x in entry['order'])
                and type(entry['record']) is int, 'accepted held metadata exact types changed')
        key = (tuple(entry['order']), entry['record'])
        if key[0] in HELD and key[1] in (0, 1):
            require(key not in selected, 'duplicate selected held row')
            selected[key] = entry
    keys = [(order, record) for order in HELD for record in (0, 1)]
    require(set(selected) == set(keys), 'six selected held rows not complete')
    require(list(selected) == keys, 'selected held rows were reordered')
    held = {key: validate_held_entry(selected[key]) for key in keys}
    for order in HELD:
        for part in HELD_IDEALS[HELD.index(order)]:
            if not part & 1:
                require(held[(order, 0)][part] == held[(order, 1)][part], 'held strict precursor locality failed')
    for record in (0, 1):
        require(held[(H5, record)][15] == held[(H5, record)][23], 'held twin-top interchange failed')
    raw_h = data['admission'].get('h')
    require(type(raw_h) is list and len(raw_h) == 11, 'accepted multiplier list shape changed')
    multipliers = [rational(value) for value in raw_h[:3]]
    verify_multipliers(multipliers)
    evidence = dict(held_rows=[selected[key] for key in keys], multipliers=[str(q) for q in multipliers],
                    held_row_count=6, held_probability_count=32, multiplier_count=3,
                    provenance=dict(schema=data['schema'], checker_sha256=data['checker_sha256'],
                                    design_sha256=data['design_sha256'], dependencies=data['dependencies'],
                                    actual_probability_manifest_sha256=data['prefix']['actual_probability_manifest_sha256'],
                                    epsilon=data['admission']['epsilon']),
                    other_accepted_rationals_used=False, helper_or_prefix_replayed=False)
    return held, multipliers, evidence


def lookup(held, order, record, part):
    validate_order(order)
    require(order in HELD, 'numeric q6 or q7 probability lookup forbidden')
    validate_record(record)
    exact_int(part, 0, (1 << len(order))-1, 'invalid exact held ideal mask')
    require(part in HELD_IDEALS[HELD.index(order)], 'held precursor outside complete declared row')
    return held[(order, record)][part]


def forbidden_global(name):
    require(type(name) is str and name not in ('rho', 's', 'a6', 'a7', 'M6', 'M7', 'q6', 'q7'),
            'numeric actual global scale or future row forbidden')
    raise RuntimeError('unknown global request')


def poly(values):
    require(type(values) in (list, tuple) and values and len(values) <= MAX_DEGREE+1
            and all(type(q) is Q for q in values), 'polynomial exact coefficient or degree domain changed')
    result = list(values)
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


ZERO, ONE = (Q(0),), (Q(1),)


def add(left, right):
    left, right = poly(left), poly(right)
    return poly([sum((p[i] if i < len(p) else Q(0) for p in (left, right)), Q(0)) for i in range(max(len(left), len(right)))])


def scale(value, multiplier):
    require(type(multiplier) is Q, 'polynomial scale is not exact rational')
    return poly([q*multiplier for q in poly(value)])


def subtract(left, right):
    return add(left, scale(right, Q(-1)))


def multiply(left, right):
    left, right = poly(left), poly(right)
    require(len(left)+len(right)-2 <= MAX_DEGREE, 'polynomial multiplication exceeds frozen degree')
    result = [Q(0)]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i+j] += a*b
    return poly(result)


def evaluate(value, point):
    require(type(point) is Q, 'polynomial proof boundary must be rational')
    result = Q(0)
    for q in reversed(poly(value)):
        result = result*point+q
    return result


def encode(value):
    return [str(q) for q in poly(value)]


def decode(value):
    require(type(value) is list and value, 'serialized polynomial shape changed')
    result = poly([rational(q) for q in value])
    require(encode(result) == value, 'serialized polynomial has noncanonical trailing zeros')
    return result


def bits(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


def induced(order, deletion, record, part):
    validate_order(order)
    require(order in (P6, P7), 'deletion outside the two declared symbolic parents')
    validate_record(record)
    full = (1 << len(order))-1
    exact_int(part, 0, full, 'invalid exact symbolic precursor')
    proper = PROPER6 if order == P6 else PROPER7
    require(part in proper, 'symbolic deletion requires a declared proper ideal')
    omitted = (full ^ 7) & ~part
    exact_int(deletion, 1, full, 'invalid exact omitted-maxima deletion')
    require(deletion & omitted == deletion, 'deletion is not a subset of omitted maxima')
    vertices = tuple(v for v in range(len(order)) if not deletion & (1 << v))
    def project(mask):
        return sum(((mask >> old) & 1) << new for new, old in enumerate(vertices))
    smaller = tuple(project(order[v]) for v in vertices)
    validate_order(smaller)
    return smaller, project(record), project(part), vertices


def held_factor(held, order, raw_record, part):
    validate_order(order)
    require(order in HELD, 'held factor escaped the three retained classes')
    validate_record(raw_record)
    exact_int(part, 0, (1 << len(order))-1, 'invalid exact held factor precursor')
    proper = part != (1 << len(order))-1
    query_record = raw_record & part if proper else raw_record
    q = lookup(held, order, query_record, part)
    return q, dict(order=list(order), raw_record=raw_record, induced_precursor=part, proper_locality_applied=proper,
                   query_record=query_record, probability=str(q), top_marks_zero=True)


def reconstruct_p6(held, record):
    """Lower potential expressions only; no numeric size-six row or scale."""
    validate_record(record)
    rows, total = [], Q(0)
    for part in PROPER6:
        omitted = 56 & ~part
        deletion, value, factors = omitted, Q(1), []
        while deletion:
            order, raw, precursor, vertices = induced(P6, deletion, record, part)
            q, source = held_factor(held, order, raw, precursor)
            exponent = 1 if deletion.bit_count() % 2 else -1
            value *= q if exponent == 1 else 1/q
            factors.append(dict(deleted_mask=deletion, kept_vertices=list(vertices), source=source, exponent=exponent))
            deletion = (deletion-1) & omitted
        require(value > 0, 'lower deletion potential lost positivity')
        rows.append(dict(ideal=part, coefficient=str(value), factors=factors))
        total += value
    require(len(rows) == 10 and sum(len(row['factors']) for row in rows) == 40, 'lower symbolic factor inventory changed')
    return {row['ideal']: rational(row['coefficient']) for row in rows}, total, rows


def verify_lower_rows(held, record, rows, claimed_sum):
    _, expected_sum, expected_rows = reconstruct_p6(held, record)
    require(type(claimed_sum) is Q and claimed_sum == expected_sum, 'lower E differs from complete independent deletion sum')
    strict_shape(rows, expected_rows)
    require(canonical(rows) == canonical(expected_rows), 'lower held-factor provenance or labeled multiplicity changed')


def sparse_product(factors, field='symbolic_factor'):
    """Independent Laurent multiplication; only monomials may be inverted."""
    require(type(field) is str and field in ('symbolic_factor', 'changed_symbolic_factor'), 'unknown symbolic factor field')
    result = {0: Q(1)}
    for factor in factors:
        exponent = factor['exponent']
        require(type(exponent) is int and exponent in (-1, 1), 'deletion exponent is not exact alternating sign')
        value = decode(factor[field])
        terms = {i: q for i, q in enumerate(value) if q}
        require(terms, 'zero symbolic deletion factor')
        if exponent == -1:
            require(len(terms) == 1, 'nonmonomial symbolic denominator forbidden')
            power, q = next(iter(terms.items()))
            terms = {-power: 1/q}
        next_value = {}
        for i, a in result.items():
            for j, b in terms.items():
                next_value[i+j] = next_value.get(i+j, Q(0))+a*b
        result = {i: q for i, q in next_value.items() if q}
    require(result and min(result) >= 0 and max(result) <= 4, 'top deletion product escaped polynomial degree four')
    return poly([result.get(i, Q(0)) for i in range(max(result)+1)])


def symbolic_p6_factor(held, record, part, lower, total):
    validate_record(record)
    exact_int(part, 0, 63, 'invalid exact symbolic six-parent precursor')
    require(part in PROPER6+(63,), 'symbolic six-parent precursor not an ideal')
    if part == 63:
        return (Q(1), -total), dict(kind='symbolic-full-complement', lower_proper_sum=str(total),
                                    expression='1-rho*E', actual_probability_evaluated=False)
    value = lower[part]
    return (Q(0), value), dict(kind='symbolic-proper-monomial', lower_ideal=part,
                              lower_potential_coefficient=str(value), expression='rho*u6', actual_probability_evaluated=False)


def slot_multiplier(part, multipliers):
    exact_int(part, 0, 127, 'invalid exact seven-parent precursor')
    require(part in PROPER7, 'top slot outside eighteen proper ideals')
    cap_count = (part >> 3).bit_count()
    if part < 7 or cap_count == 3:
        return Q(1), None, 0
    index, power = cap_count, 4-cap_count
    return multipliers[index]**power, index, power


def six_birth_multiplier(part, multipliers):
    exact_int(part, 0, 63, 'invalid exact six-birth ideal')
    require(part in PROPER6+(63,), 'six-birth ideal outside frozen forward inventory')
    if part in (0, 1, 3, 63):
        return Q(1), None
    index = 0 if part == 7 else 1 if part in (15, 23, 39) else 2
    return multipliers[index], index


def reconstruct_p7(held, multipliers, record, lower, total):
    rows, baseline, changed = [], ZERO, ZERO
    for part in PROPER7:
        budget()
        omitted, factors = 120 & ~part, []
        deletion = omitted
        while deletion:
            order, raw, precursor, vertices = induced(P7, deletion, record, part)
            if order == P6:
                value, source = symbolic_p6_factor(held, raw, precursor, lower, total)
                seed_multiplier, seed_index = six_birth_multiplier(precursor, multipliers)
            else:
                q, source = held_factor(held, order, raw, precursor)
                value = (q,)
                seed_multiplier, seed_index = Q(1), None
            factors.append(dict(deleted_mask=deletion, kept_vertices=list(vertices), induced_order=list(order),
                                raw_record=raw, induced_precursor=precursor, source=source,
                                exponent=1 if deletion.bit_count() % 2 else -1, symbolic_factor=encode(value),
                                seed_multiplier=str(seed_multiplier), seed_multiplier_index=seed_index,
                                changed_symbolic_factor=encode(scale(value, seed_multiplier))))
            deletion = (deletion-1) & omitted
        value = sparse_product(factors)
        factor, index, power = slot_multiplier(part, multipliers)
        changed_value = sparse_product(factors, 'changed_symbolic_factor')
        require(changed_value == scale(value, factor), 'singleton terminal multiplier power identity failed')
        rows.append(dict(ideal=part, included_caps=(part >> 3).bit_count(), factors=factors,
                         baseline_potential=encode(value), multiplier=str(factor), multiplier_index=index,
                         multiplier_power=power, changed_potential=encode(changed_value)))
        baseline, changed = add(baseline, value), add(changed, changed_value)
    require(len(rows) == 18 and sum(len(row['factors']) for row in rows) == 110, 'eighteen-slot top deletion inventory changed')
    return rows, baseline, subtract(changed, baseline)


def closed_polynomials(held, multipliers, record):
    validate_record(record)
    A = {s: lookup(held, C3, record, s) for s in (0, 1, 3, 7)}
    B = {s: lookup(held, C4, record, s) for s in (0, 1, 3, 7)}
    G = {s: lookup(held, H5, record, s) for s in (0, 1, 3, 7)}
    c, h, j = lookup(held, C4, record, 15), lookup(held, H5, record, 15), lookup(held, H5, record, 31)
    e_terms = [A[s]*G[s]**3/B[s]**3 for s in (0, 1, 3, 7)]
    k_terms = [A[s]**3*G[s]**6/B[s]**8 for s in (0, 1, 3, 7)]
    E, K = sum(e_terms, Q(0))+3*h*h/c+3*j, sum(k_terms, Q(0))
    U = poly([Q(4), -4*E, 6*j, 4*h**3/c**2, K])
    D = poly([Q(0), Q(0), 6*j*(multipliers[2]**2-1), 4*h**3/c**2*(multipliers[1]**3-1),
              A[7]**3*G[7]**6/B[7]**8*(multipliers[0]**4-1)])
    return E, U, D, dict(base_ideals=[0, 1, 3, 7], E_terms=[str(q) for q in e_terms],
                         E_one_cap_total=str(3*h*h/c), E_two_cap_total=str(3*j),
                         E=str(E), K_terms=[str(q) for q in k_terms], K=str(K),
                         c=str(c), h=str(h), j=str(j), U=encode(U), D=encode(D))


def verify_upper_bound(sums, bound):
    require(type(sums) is list and len(sums) == 2 and all(type(q) is Q and q > 0 for q in sums),
            'selected lower-potential sums are not positive rationals')
    require(type(bound) is Q and bound == 1/(2*(1+max(sums))) and bound > 0,
            'selected-row outer rho bound changed or became an actual scale')
    require(all(1-bound*q > Q(1, 2) for q in sums), 'selected symbolic full-complement positivity bound failed')


def verify_slots(rows, lower_sum, multipliers):
    require(type(rows) is list and len(rows) == 18, 'top proper-slot list coverage changed')
    for row in rows:
        require(type(row) is dict, 'top proper-slot evidence is not an object')
        exact_int(row['ideal'], 0, 127, 'invalid exact seven-parent precursor')
    require([row['ideal'] for row in rows] == list(PROPER7), 'top proper-slot labeled multiplicity changed')
    for row in rows:
        part, k = row['ideal'], (row['ideal'] >> 3).bit_count()
        value = decode(row['baseline_potential'])
        require(type(row['included_caps']) is int and row['included_caps'] == k, 'included-cap count changed')
        if k == 3:
            require(value == (Q(1), -lower_sum), 'three-cap slot is not the unchanged symbolic full complement')
        else:
            degree = 4 if k == 0 else 4-k
            require(len(value) == degree+1 and value[-1] > 0 and not any(value[:-1]),
                    'proper top slot lost its positive monomial form')
        require(sparse_product(row['factors']) == value, 'top deletion product does not reconstruct its slot')
        changed = decode(row['changed_potential'])
        factor, index, power = slot_multiplier(part, multipliers)
        require(rational(row['multiplier']) == factor
                and (row['multiplier_index'] is None if index is None
                     else type(row['multiplier_index']) is int and row['multiplier_index'] == index)
                and type(row['multiplier_power']) is int and row['multiplier_power'] == power,
                'top slot multiplier or individual power changed')
        require(changed == sparse_product(row['factors'], 'changed_symbolic_factor') == scale(value, factor),
                'changed top slot product or multiplier identity failed')


def divide_rho_squared(value, degree):
    exact_int(degree, 2, 6, 'invalid fixed Bernstein basis degree')
    require(degree in (2, 6), 'invalid fixed Bernstein basis degree')
    value = poly(value)
    require(len(value) <= degree+3 and all((value[i] if i < len(value) else Q(0)) == 0 for i in (0, 1)),
            'polynomial does not have the prescribed exact rho-squared factor')
    return poly(list(value[2:]) or [Q(0)])


def reverse_bernstein(coefficients, bound, degree):
    """Expand binomial basis directly; not a call to the forward transform."""
    exact_int(degree, 2, 6, 'invalid fixed Bernstein basis degree')
    require(degree in (2, 6) and type(bound) is Q and bound > 0, 'invalid Bernstein interval or fixed degree')
    require(type(coefficients) is list and len(coefficients) == degree+1 and all(type(q) is Q for q in coefficients),
            'Bernstein coordinates lost exact types or full fixed-degree coverage')
    scaled = [Q(0)]*(degree+1)
    for k, coefficient in enumerate(coefficients):
        for ell in range(degree-k+1):
            scaled[k+ell] += coefficient*comb(degree, k)*comb(degree-k, ell)*(-1)**ell
    return [q/bound**j for j, q in enumerate(scaled)]


def bernstein(value, bound, degree):
    require(type(bound) is Q and bound > 0, 'Bernstein interval upper endpoint must be strictly positive')
    quotient = divide_rho_squared(value, degree)
    padded = list(quotient)+[Q(0)]*(degree+1-len(quotient))
    scaled = [q*bound**j for j, q in enumerate(padded)]
    coefficients = [sum((scaled[j]*Q(comb(k, j), comb(degree, j)) for j in range(k+1)), Q(0))
                    for k in range(degree+1)]
    reversed_power = reverse_bernstein(coefficients, bound, degree)
    require(reversed_power == padded, 'Bernstein reverse expansion failed')
    require(evaluate(poly(padded), bound) == coefficients[-1], 'included upper endpoint is not the last Bernstein coordinate')
    return dict(polynomial=encode(value), rho_factor=2, basis_degree=degree, R=str(bound),
                quotient_power=[str(q) for q in padded], scaled_power=[str(q) for q in scaled],
                bernstein=[str(q) for q in coefficients], reversed_power=[str(q) for q in reversed_power],
                included_upper_endpoint_value=str(coefficients[-1]), subdivision_used=False,
                adaptive_degree_elevation_used=False)


def verify_bernstein(value, bound, degree, evidence):
    require(type(evidence) is dict and 'bernstein' in evidence and 'rho_factor' in evidence
            and 'basis_degree' in evidence, 'Bernstein evidence fields missing')
    require(type(evidence['rho_factor']) is int and evidence['rho_factor'] == 2,
            'prescribed rho-squared factor was changed')
    require(type(evidence['basis_degree']) is int and evidence['basis_degree'] == degree,
            'predeclared Bernstein degree was changed')
    raw = evidence['bernstein']
    require(type(raw) is list, 'Bernstein coordinate container changed')
    coefficients = [rational(q) for q in raw]
    quotient = divide_rho_squared(value, degree)
    require(reverse_bernstein(coefficients, bound, degree) == list(quotient)+[Q(0)]*(degree+1-len(quotient)),
            'retained Bernstein coordinates fail the independent reverse identity')
    expected = bernstein(value, bound, degree)
    strict_shape(evidence, expected)
    require(canonical(evidence) == canonical(expected), 'fixed Bernstein evidence reconstruction mismatch')


def oriented_certificate(evidence, orientation, strict_upper):
    require(type(orientation) is int and orientation in (-1, 1) and type(strict_upper) is bool,
            'invalid exact sign-certificate orientation')
    coefficients = [rational(q) for q in evidence['bernstein']]
    return all(orientation*q >= 0 for q in coefficients) and (not strict_upper or orientation*coefficients[-1] > 0)


ROOT_SEMANTICS = {
    'C_nonzero': 'At any rho with C(rho)!=0, only s=A(rho)/C(rho) can solve F=0; admissibility must still be checked.',
    'A_C_zero': 'At any rho with A(rho)=C(rho)=0, every outer-admissible s solves this pair only.',
    'C_zero_A_nonzero': 'At any rho with C(rho)=0 and A(rho)!=0, this pair has no s root.',
    'no_actual_scale_claim': True,
}


def boundary_diagnostic(A, C, U, bound):
    require(type(U) is list and len(U) == 2, 'boundary test requires the two declared U polynomials')
    ar, cr = evaluate(A, bound), evaluate(C, bound)
    ur = [evaluate(value, bound) for value in U]
    require(all(q > 0 for q in ur), 'proof-boundary U denominator positivity failed')
    caps = [1/(2*(1+q)) for q in ur]
    if cr != 0:
        candidate, kind = ar/cr, 'unique-algebraic-root-at-included-boundary'
    elif ar == 0:
        candidate, kind = min(caps), 'every-outer-admissible-s-at-included-boundary'
    else:
        candidate, kind = None, 'no-s-root-at-included-boundary'
    residual = None if candidate is None else ar-candidate*cr
    valid = candidate is not None and candidate > 0 and all(candidate <= cap for cap in caps) and residual == 0
    return dict(examined=True, rho=str(bound), boundary_only_not_actual_rho=True,
                A_at_R=str(ar), C_at_R=str(cr), U_at_R=[str(q) for q in ur],
                s_upper_bounds_at_R=[str(q) for q in caps], root_kind=kind,
                candidate_s=None if candidate is None else str(candidate),
                residual=None if residual is None else str(residual), outer_admissible_root=valid,
                actual_scale_identified=False, full_modified_positivity_established=False)


def decide(A, C, U, bound):
    A, C = poly(A), poly(C)
    require(type(U) is list and len(U) == 2, 'decision requires exactly two U polynomials')
    U = [poly(value) for value in U]
    # The source freezes rho**2 even if a particular polynomial has higher
    # valuation or vanishes. No dynamic stripping or adaptive degree search.
    divide_rho_squared(C, 6)
    G = [subtract(scale(multiply(add(ONE, value), A), Q(2)), C) for value in U]
    evidence = dict(A=bernstein(A, bound, 2), G0=bernstein(G[0], bound, 6), G1=bernstein(G[1], bound, 6))
    for name, value, degree in (('A', A, 2), ('G0', G[0], 6), ('G1', G[1], 6)):
        verify_bernstein(value, bound, degree, evidence[name])
    tests = {}
    for sign, name in ((1, 'positive'), (-1, 'negative')):
        tests[name] = dict(A_weak=oriented_certificate(evidence['A'], sign, False),
                           G0_strict=oriented_certificate(evidence['G0'], sign, True),
                           G1_strict=oriented_certificate(evidence['G1'], sign, True))
    orientation = next((sign for sign, name in ((1, 'positive'), (-1, 'negative')) if all(tests[name].values())), None)
    if orientation is not None:
        disposition = 'certified-positive-obstruction' if orientation == 1 else 'certified-negative-obstruction'
        diagnostic = dict(examined=False, reason='strict sufficient Bernstein certificate already decides nonvanishing')
    elif A == ZERO and C == ZERO:
        disposition = 'identically-zero-pair'
        diagnostic = dict(examined=False, reason='exact A=C=0 polynomial identities; no selector acceptance')
    else:
        diagnostic = boundary_diagnostic(A, C, U, bound)
        disposition = 'outer-boundary-root-unresolved' if diagnostic['outer_admissible_root'] else 'unresolved-fixed-bernstein'
    return dict(disposition=disposition, orientation=orientation, A=encode(A), C=encode(C),
                G0=encode(G[0]), G1=encode(G[1]), bernstein_evidence=evidence, orientation_tests=tests,
                identically_zero_F=(A == ZERO and C == ZERO), boundary_diagnostic=diagnostic,
                root_locus_semantics=ROOT_SEMANTICS, selector_acceptance_claimed=False,
                actual_global_scales_computed=False, other_parent_or_record_tested=False)


def verify_decision(A, C, U, bound, evidence):
    expected = decide(A, C, U, bound)
    strict_shape(evidence, expected)
    require(canonical(evidence) == canonical(expected), 'exact fixed-protocol decision reconstruction mismatch')


def build_witness(data):
    held, multipliers, inputs = extract_input(data)
    records, sums, U, D = [], [], [], []
    for record in (0, 1):
        lower, lower_sum, lower_rows = reconstruct_p6(held, record)
        verify_lower_rows(held, record, lower_rows, lower_sum)
        E, closed_U, closed_D, closed = closed_polynomials(held, multipliers, record)
        require(E == lower_sum, 'closed E disagrees with independent lower deletion sum')
        slots, generic_U, generic_D = reconstruct_p7(held, multipliers, record, lower, lower_sum)
        verify_slots(slots, lower_sum, multipliers)
        require(E == lower_sum and closed_U == generic_U and closed_D == generic_D,
                'closed formulas disagree with independent individual deletion products')
        records.append(dict(record=record, lower_symbolic_slots=lower_rows, top_proper_slots=slots,
                            closed_form=closed, generic_U=encode(generic_U), generic_D=encode(generic_D),
                            generic_V=encode(add(generic_U, generic_D))))
        sums.append(E)
        U.append(generic_U)
        D.append(generic_D)
    bound = 1/(2*(1+max(sums)))
    verify_upper_bound(sums, bound)
    A = subtract(D[1], D[0])
    C = subtract(multiply(D[1], U[0]), multiply(D[0], U[1]))
    V = [add(u, d) for u, d in zip(U, D)]
    alternate_C = subtract(multiply(V[1], U[0]), multiply(V[0], U[1]))
    require(C == alternate_C, 'full-ratio cross multiplication lost a complement term')
    decision = decide(A, C, U, bound)
    return copy_json(dict(schema='ri91-relative-obstruction-v1', design_sha256=DESIGN_SHA256,
                         design_bytes=DESIGN_BYTES, accepted_input=dict(sha256=INPUT_SHA256, bytes=INPUT_BYTES),
                         inputs=inputs, selected_parent=list(P7), records=records,
                         scale_domain=dict(R=str(bound), selected_E=[str(q) for q in sums],
                                           symbolic_lower_full_margins_at_R=[str(1-bound*q) for q in sums],
                                           rho_interval='0<rho<=R', s_interval='0<s<=min_i 1/[2(1+Ui(rho))]',
                                           actual_scales_selected=False, full_modified_positivity_not_claimed=True),
                         cross_multiplication=dict(A=encode(A), C=encode(C),
                                                   C_via_V=encode(alternate_C), F_by_s_power=[encode(A), encode(scale(C, Q(-1)))]),
                         decision=decision,
                         coverage=dict(held_rows=6, held_probability_slots=32, terminal_multipliers=3,
                                       record_assignments=2, lower_symbolic_slots=20, lower_held_factors=80,
                                       top_proper_slots=36, top_deletion_factors=220, included_full_probability_rows=0,
                                       fixed_bernstein_degrees=[2, 6, 6]),
                         limitations=dict(numeric_q6_q7_or_global_M_computed=False, helper_prefix_replayed=False,
                                          uniform_obstruction_only_if_certified=True, pair_pass_does_not_accept_selector=True,
                                          no_other_records_parents_or_adaptive_search=True))), held, multipliers


def synthetic_fixtures():
    """Fixed rational algebra only, not additional growth rows or scale data."""
    r2 = (Q(0), Q(0), Q(1))
    U, R = [ONE, ONE], Q(1)
    cases = {
        'positive': (r2, ZERO, U, 'certified-positive-obstruction'),
        'negative': (scale(r2, Q(-1)), ZERO, U, 'certified-negative-obstruction'),
        'weak-A-zero': (ZERO, scale(r2, Q(-1)), U, 'certified-positive-obstruction'),
        'identically-zero': (ZERO, ZERO, U, 'identically-zero-pair'),
        'endpoint-every-s-root': (multiply(r2, (Q(1), Q(-1))), ZERO, U, 'outer-boundary-root-unresolved'),
        'endpoint-unique-root': (r2, scale(r2, Q(8)), U, 'outer-boundary-root-unresolved'),
        'mixed-Bernstein-but-positive': (multiply(r2, (Q(1, 3), Q(-1), Q(1))), ZERO, U, 'unresolved-fixed-bernstein'),
        'second-bound-excludes-root': (r2, scale(r2, Q(4)), [ONE, (Q(3),)], 'unresolved-fixed-bernstein'),
        'excluded-s-zero': (multiply(r2, (Q(1), Q(-1))), r2, U, 'unresolved-fixed-bernstein'),
        'origin-only-zero': (multiply(r2, (Q(0), Q(1))), ZERO, U, 'certified-positive-obstruction'),
    }
    results = {}
    for name, (A, C, fixture_U, expected) in cases.items():
        result = decide(A, C, fixture_U, R)
        require(result['disposition'] == expected, 'fixed synthetic algebra branch changed')
        results[name] = result
    square = add(multiply((Q(-1, 2), Q(1)), (Q(-1, 2), Q(1))), (Q(1, 12),))
    require(multiply(r2, square) == cases['mixed-Bernstein-but-positive'][0], 'synthetic completed-square identity failed')
    return cases, results


def refusal_controls(witness, raw_input, data, held, multipliers):
    passed = []
    def expect(name, reason, action):
        try:
            action()
        except RuntimeError as error:
            require(str(error) == reason, 'refusal '+name+' used the wrong reason: '+str(error))
        else:
            raise RuntimeError('refusal '+name+' did not reject')
        passed.append(name)
    def altered(value, path, replacement):
        result = copy_json(value)
        target = result
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = replacement
        return result
    def saved(name, path, replacement, reason='certificate exact reconstructed witness mismatch'):
        expect(name, reason, lambda: verify_certificate(altered(witness, path, replacement), witness))

    expect('duplicate-json-key', 'duplicate JSON key', lambda: load_json('{"a":0,"a":1}'))
    expect('decimal-json', 'JSON decimal or nonfinite value forbidden', lambda: load_json('[0.1]'))
    expect('nonfinite-json', 'JSON decimal or nonfinite value forbidden', lambda: load_json('[Infinity]'))
    expect('unreduced-rational', 'noncanonical rational encoding', lambda: rational('2/2'))
    expect('boolean-rational', 'noncanonical rational encoding', lambda: rational(True))
    expect('wrong-input-size', 'accepted RI88 certificate byte size mismatch', lambda: verify_input_bytes(raw_input[:-1]))
    expect('wrong-input-hash', 'accepted RI88 certificate byte hash mismatch', lambda: verify_input_bytes(b'!'+raw_input[1:]))
    expect('wrong-source-provenance', 'accepted RI88 source provenance changed',
           lambda: verify_provenance(altered(data, ['checker_sha256'], '0'*64)))
    expect('wrong-actual-prefix-provenance', 'accepted actual strict-prefix provenance changed',
           lambda: verify_provenance(altered(data, ['prefix', 'actual_probability_manifest_sha256'], '0'*64)))
    expect('bool-provenance-count', 'accepted held-coverage provenance changed',
           lambda: verify_provenance(altered(data, ['coverage', 'held_marked_rows'], True)))
    expect('extra-input-field', 'accepted RI88 top-level schema changed', lambda: verify_provenance(dict(data, extra=None)))
    expect('missing-input-field', 'accepted RI88 top-level schema changed',
           lambda: verify_provenance({k: v for k, v in data.items() if k != 'schema'}))
    reordered = copy_json(data)
    reordered['held_rows'][0], reordered['held_rows'][1] = reordered['held_rows'][1], reordered['held_rows'][0]
    expect('reordered-selected-rows', 'selected held rows were reordered', lambda: extract_input(reordered))
    entry = witness['inputs']['held_rows'][0]
    expect('extra-selected-record', 'record outside the two frozen exact markings',
           lambda: validate_held_entry(altered(entry, ['record'], 2)))
    expect('bool-selected-record', 'record outside the two frozen exact markings',
           lambda: validate_held_entry(altered(entry, ['record'], False)))
    expect('bool-held-order-mask', 'held order exact mask types changed',
           lambda: validate_held_entry(altered(entry, ['order', 0], False)))
    expect('missing-held-full-slot', 'held row lost labeled ideal coverage',
           lambda: validate_held_entry(altered(entry, ['probabilities'], entry['probabilities'][:-1])))
    expect('duplicate-held-slot', 'held row lost labeled ideal coverage',
           lambda: validate_held_entry(altered(entry, ['probabilities', 1, 0], 0)))
    expect('nonpositive-held-probability', 'held row lost strict positive normalization',
           lambda: validate_held_entry(altered(entry, ['probabilities', 0, 1], '-1')))
    expect('changed-H1', 'accepted H1 multiplier changed', lambda: verify_multipliers([Q(1)]+multipliers[1:]))
    expect('changed-H-interval', 'accepted multiplier interval changed', lambda: verify_multipliers([multipliers[0], Q(3, 2), multipliers[2]]))
    expect('zero-H', 'selected terminal multipliers lost exact positive three-value domain',
           lambda: verify_multipliers(multipliers[:2]+[Q(0)]))
    expect('numeric-six-parent-query', 'numeric q6 or q7 probability lookup forbidden', lambda: lookup(held, P6, 0, 0))
    expect('numeric-seven-parent-query', 'numeric q6 or q7 probability lookup forbidden', lambda: lookup(held, P7, 0, 0))
    expect('C5-query-refusal', 'order outside frozen exact structural domain', lambda: lookup(held, (0, 1, 3, 7, 15), 0, 0))
    expect('nested-unhashable-order', 'order outside frozen exact structural domain', lambda: lookup(held, (0, [1], 3), 0, 0))
    expect('extra-record-query', 'record outside the two frozen exact markings', lambda: lookup(held, C3, 2, 0))
    for name in ('rho', 's', 'a6', 'a7', 'M6', 'M7', 'q6', 'q7'):
        expect('no-actual-'+name, 'numeric actual global scale or future row forbidden', lambda name=name: forbidden_global(name))
    expect('full-top-ideal-not-proper', 'symbolic deletion requires a declared proper ideal', lambda: induced(P7, 8, 0, 127))
    expect('delete-nonmaximal-vertex', 'deletion is not a subset of omitted maxima', lambda: induced(P7, 1, 0, 7))
    expect('bool-deletion-mask', 'invalid exact omitted-maxima deletion', lambda: induced(P7, True, 0, 7))
    expect('bool-symbolic-precursor', 'invalid exact symbolic precursor', lambda: induced(P7, 8, 0, False))
    record = witness['records'][0]
    E = rational(record['closed_form']['E'])
    lower_rows = record['lower_symbolic_slots']
    expect('wrong-independent-E', 'lower E differs from complete independent deletion sum',
           lambda: verify_lower_rows(held, 0, lower_rows, E+1))
    expect('missing-lower-slot', 'certificate list coverage mismatch', lambda: verify_lower_rows(held, 0, lower_rows[:-1], E))
    expect('wrong-lower-factor-exponent', 'lower held-factor provenance or labeled multiplicity changed',
           lambda: verify_lower_rows(held, 0, altered(lower_rows, [0, 'factors', 0, 'exponent'], 0), E))
    slots = record['top_proper_slots']
    expect('missing-top-slot', 'top proper-slot list coverage changed', lambda: verify_slots(slots[:-1], E, multipliers))
    expect('duplicate-top-slot', 'top proper-slot labeled multiplicity changed',
           lambda: verify_slots(altered(slots, [1, 'ideal'], 0), E, multipliers))
    expect('bool-cap-count', 'included-cap count changed', lambda: verify_slots(altered(slots, [0, 'included_caps'], False), E, multipliers))
    expect('collapsed-multiple-ideal-weight', 'top deletion product does not reconstruct its slot',
           lambda: verify_slots(altered(slots, [0, 'baseline_potential'], encode(scale(decode(slots[0]['baseline_potential']), Q(4)))), E, multipliers))
    full_index = next(i for i, item in enumerate(slots) if item['included_caps'] == 3)
    expect('proper-full-complement-confusion', 'three-cap slot is not the unchanged symbolic full complement',
           lambda: verify_slots(altered(slots, [full_index, 'baseline_potential'], ['1']), E, multipliers))
    expect('incorrect-multiplier-power', 'top slot multiplier or individual power changed',
           lambda: verify_slots(altered(slots, [3, 'multiplier_power'], 1), E, multipliers))
    expect('zero-deletion-exponent', 'deletion exponent is not exact alternating sign',
           lambda: sparse_product(altered(slots[0]['factors'], [0, 'exponent'], 0)))
    expect('invert-binomial-factor', 'nonmonomial symbolic denominator forbidden',
           lambda: sparse_product([dict(exponent=-1, symbolic_factor=['1', '-1'])]))
    expect('bool-polynomial-coefficient', 'polynomial exact coefficient or degree domain changed', lambda: poly([False]))
    expect('polynomial-degree-expansion', 'polynomial exact coefficient or degree domain changed', lambda: poly([Q(0)]*10))
    expect('polynomial-trailing-zero', 'serialized polynomial has noncanonical trailing zeros', lambda: decode(['1', '0']))
    expect('wrong-rho-factor', 'polynomial does not have the prescribed exact rho-squared factor',
           lambda: divide_rho_squared((Q(1),), 2))
    sums = [rational(q) for q in witness['scale_domain']['selected_E']]
    bound = rational(witness['scale_domain']['R'])
    expect('selected-bound-as-half', 'selected-row outer rho bound changed or became an actual scale',
           lambda: verify_upper_bound(sums, Q(1, 2)))
    expect('zero-Bernstein-bound', 'Bernstein interval upper endpoint must be strictly positive', lambda: bernstein(ZERO, Q(0), 2))
    expect('adaptive-Bernstein-degree', 'invalid fixed Bernstein basis degree', lambda: bernstein(ZERO, Q(1), 3))

    cases, examples = synthetic_fixtures()
    positive = examples['positive']
    b_evidence = positive['bernstein_evidence']['A']
    expect('changed-factor-two', 'prescribed rho-squared factor was changed',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['rho_factor'], 1)))
    expect('changed-fixed-basis-degree', 'predeclared Bernstein degree was changed',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['basis_degree'], 6)))
    expect('bool-Bernstein-coordinate', 'noncanonical rational encoding',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['bernstein', 0], True)))
    expect('missing-Bernstein-coordinate', 'Bernstein coordinates lost exact types or full fixed-degree coverage',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['bernstein'], b_evidence['bernstein'][:-1])))
    expect('wrong-Bernstein-coordinate', 'retained Bernstein coordinates fail the independent reverse identity',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['bernstein', 0], '2')))
    expect('wrong-reverse-power-evidence', 'fixed Bernstein evidence reconstruction mismatch',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['reversed_power', 0], '2')))
    expect('wrong-scaled-power-evidence', 'fixed Bernstein evidence reconstruction mismatch',
           lambda: verify_bernstein(cases['positive'][0], Q(1), 2, altered(b_evidence, ['scaled_power', 0], '2')))
    expect('bool-sign-orientation', 'invalid exact sign-certificate orientation', lambda: oriented_certificate(b_evidence, True, False))
    for name, false_disposition in (('endpoint-every-s-root', 'certified-positive-obstruction'),
                                     ('weak-A-zero', 'identically-zero-pair'),
                                     ('mixed-Bernstein-but-positive', 'outer-boundary-root-unresolved'),
                                     ('second-bound-excludes-root', 'outer-boundary-root-unresolved'),
                                     ('excluded-s-zero', 'outer-boundary-root-unresolved'),
                                     ('origin-only-zero', 'unresolved-fixed-bernstein')):
        A, C, fixture_U, _ = cases[name]
        expect('false-'+name, 'exact fixed-protocol decision reconstruction mismatch',
               lambda A=A, C=C, fixture_U=fixture_U, name=name, false_disposition=false_disposition:
               verify_decision(A, C, fixture_U, Q(1), altered(examples[name], ['disposition'], false_disposition)))
    endpoint = examples['endpoint-every-s-root']
    expect('included-zero-endpoint-as-strict', 'exact fixed-protocol decision reconstruction mismatch',
           lambda: verify_decision(cases['endpoint-every-s-root'][0], ZERO, [ONE, ONE], Q(1),
                                   altered(endpoint, ['orientation_tests', 'positive', 'G0_strict'], True)))
    expect('outer-root-is-not-actual-scale', 'exact fixed-protocol decision reconstruction mismatch',
           lambda: verify_decision(cases['endpoint-unique-root'][0], cases['endpoint-unique-root'][1], [ONE, ONE], Q(1),
                                   altered(examples['endpoint-unique-root'], ['boundary_diagnostic', 'actual_scale_identified'], True)))

    saved('wrong-new-schema', ['schema'], 'wrong-schema', 'certificate schema mismatch')
    expect('extra-new-certificate-field', 'certificate object fields mismatch', lambda: verify_certificate(dict(witness, extra=None), witness))
    expect('missing-new-certificate-field', 'certificate object fields mismatch',
           lambda: verify_certificate({k: v for k, v in witness.items() if k != 'inputs'}, witness))
    saved('bool-new-record', ['records', 0, 'record'], False, 'certificate exact value type mismatch')
    saved('missing-retained-input-row', ['inputs', 'held_rows'], witness['inputs']['held_rows'][:-1], 'certificate list coverage mismatch')
    saved('altered-raw-factor-provenance', ['records', 0, 'top_proper_slots', 0, 'factors', 0, 'raw_record'], 1)
    saved('wrong-cross-complement-polynomial', ['cross_multiplication', 'C', 0], '1')
    saved('forged-native-disposition', ['decision', 'disposition'], 'scientific-outcome-not-derived')
    saved('claim-numeric-actual-scale', ['scale_domain', 'actual_scales_selected'], True)
    saved('claim-selector-acceptance', ['decision', 'selector_acceptance_claimed'], True)
    require(len(passed) == 83 and len(set(passed)) == 83, 'frozen intended-reason refusal inventory changed')
    return dict(intended_reason_refusals=passed,
                synthetic_algebra_fixtures={name: dict(disposition=value['disposition'],
                                                       A=encode(cases[name][0]), C=encode(cases[name][1]),
                                                       R='1', U=[encode(p) for p in cases[name][2]]) for name, value in examples.items()},
                synthetic_fixtures_are_native_models=False, extra_native_inputs_used=False)


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'only --witness or default saved-certificate mode is permitted')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, lambda _number, _frame: (_ for _ in ()).throw(RuntimeError('120-second envelope exceeded')))
    signal.alarm(MAX_SECONDS)
    source = Path(__file__).resolve()
    source_bytes = source.read_bytes()
    source_hash = sha256(source_bytes).hexdigest()
    input_path = source.parent.parent/'native_growth_four_vertex_cap_check_v1'/'CERTIFICATE.json'
    raw_input = input_path.read_bytes()
    verify_input_bytes(raw_input)  # Authentication precedes JSON parsing or extraction.
    data = load_json(raw_input)
    budget('accepted certificate pinned; no helper or prefix imports')
    witness, held, multipliers = build_witness(data)
    witness['checker_sha256'] = source_hash
    witness['refusal_controls'] = refusal_controls(witness, raw_input, data, held, multipliers)
    budget('fixed exact symbolic constructions and intended-reason controls completed')
    certificate_hash = None
    if not sys.argv[1:]:
        path = source.with_name('CERTIFICATE.json')
        raw_certificate = path.read_bytes()
        verify_certificate(load_json(raw_certificate), witness)
        certificate_hash = sha256(raw_certificate).hexdigest()
        require(path.read_bytes() == raw_certificate, 'saved certificate changed during verification')
    verify_input_bytes(input_path.read_bytes())
    require(source.read_bytes() == source_bytes, 'checker source changed during verification')
    budget()
    try:
        if sys.argv[1:]:
            print(canonical(witness), flush=True)
        else:
            result = dict(status='PASS', checker_sha256=source_hash, certificate_sha256=certificate_hash,
                          accepted_input_sha256=INPUT_SHA256, witness_sha256=digest(witness),
                          disposition=witness['decision']['disposition'], coverage=witness['coverage'],
                          actual_scales_or_future_probabilities_computed=False,
                          refusal_count=len(witness['refusal_controls']['intended_reason_refusals']),
                          refusal_controls=witness['refusal_controls']['intended_reason_refusals'])
            print(canonical(result), flush=True)
        budget()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
