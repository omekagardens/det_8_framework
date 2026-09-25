#!/usr/bin/env python3
"""RI-95: bounded exact bivariate amplitude certificate, source-only preparation.

Scientific arithmetic consumes only the accepted RI-88 six complete rows
(32 probabilities) and first three H multipliers. The other eight H strings
are retained solely as authenticated eleven-support provenance. Accepted
RI-91 contributes only its 17 Bernstein coordinates and scope metadata for
the epsilon=1/4 regression; its native polynomial coefficients are not used.
rho, epsilon and s are formal variables. R is a mathematical outer bound,
not an evaluated actual global scale. There are no new probability queries,
helper imports, searches, subdivisions, root tests or adaptive degrees.
JSON is emitted to stdout; no files are written. Internal 120-second and
512-MiB checks supplement the separately authorized sampled watchdog.
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


SCHEMA = 'ri95-relative-amplitude-certificate-v1'
DESIGN_SHA256 = '65645454993a81b70a0d9cd278eb137cd6b218055b1cb026f9950b7cb8895844'
DESIGN_BYTES = 25150
INPUT_PINS = {
    'ri88': (1828149, 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    'ri91': (364312, '9e48c437e90cbeef6284ddbcdf5ec915aa520217172f580ef900e5c2bccd37ed'),
}
RI88_CHECKER = '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
RI91_CHECKER = 'b0a40587be40afa6972664784ec1844f1463564ba93d5ba6cd2b21173986770e'
RI85_DESIGN = 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a'
RI89_DESIGN = '56c45bb5aba5e9fa0ab1f09ff959a73235939cc850e6fdde91a4cc39180b5cd1'
INHERITED_PINS = {
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
}
RI88_KEYS = {'admission', 'checker_sha256', 'compact_rows', 'coverage', 'dependencies', 'design_sha256',
             'domain', 'exact_decision', 'expanded_rows', 'held_rows', 'parameters', 'prefix',
             'refusal_controls', 'schema', 'structure', 'transported_audit', 'width_target'}
RI91_KEYS = {'schema', 'checker_sha256', 'design_sha256', 'design_bytes', 'accepted_input', 'inputs',
             'selected_parent', 'records', 'scale_domain', 'cross_multiplication', 'decision', 'coverage',
             'limitations', 'refusal_controls'}
C3, C4, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 7)
P6, P7 = (0, 1, 3, 7, 7, 7), (0, 1, 3, 7, 7, 7, 7)
HELD = (C3, C4, H5)
HELD_IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 23, 31))
PROPER6 = (0, 1, 3, 7, 15, 23, 31, 39, 47, 55)
PROPER7 = (0, 1, 3, 7, 15, 23, 31, 39, 47, 55, 63, 71, 79, 87, 95, 103, 111, 119)
CAPS = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 3), (0, 0, 1, 1), (0, 0, 1, 2),
        (0, 0, 1, 3), (0, 0, 1, 5), (0, 0, 3, 3), (0, 1, 1, 1), (0, 1, 1, 3), (0, 1, 3, 3))
WIDTHS = (4, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2)
AMPLITUDE = Q(1, 4)
START = None
MAX_SECONDS, MAX_BYTES = 120, 512*1024**2


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
        print('RI95: '+stage, file=sys.stderr, flush=True)


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
    require(saved['schema'] == SCHEMA, 'certificate schema mismatch')
    require(canonical(saved) == canonical(expected), 'certificate exact reconstructed witness mismatch')


def verify_saved_bytes(raw, expected):
    require(type(raw) is bytes, 'saved certificate must be bytes')
    verify_certificate(load_json(raw), expected)
    require(raw == (canonical(expected)+'\n').encode(), 'saved certificate is not exact canonical bytes with one newline')


def verify_input_bytes(role, raw):
    require(type(role) is str and role in INPUT_PINS, 'unknown accepted input role')
    size, pin = INPUT_PINS[role]
    require(type(raw) is bytes and len(raw) == size, 'accepted '+role+' certificate byte size mismatch')
    require(sha256(raw).hexdigest() == pin, 'accepted '+role+' certificate byte hash mismatch')


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
    expected = [dict(index=j, cap=list(cap), order=list(C3)+[7+8*p for p in cap], width=WIDTHS[j])
                for j, cap in enumerate(CAPS)]
    require(type(data['structure']) is dict and 'ordered_support' in data['structure'], 'accepted full support provenance missing')
    require(canonical(data['structure']['ordered_support']) == canonical(expected), 'accepted eleven-class support order changed')


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


def verify_direction(H, z):
    require(type(H) is list and len(H) == 3 and all(type(q) is Q and q > 0 for q in H), 'three selected H values lost exact positivity')
    require(H[0] == Q(5, 4), 'accepted H1 multiplier changed')
    require(all(Q(3, 4) <= q <= Q(5, 4) for q in H), 'accepted multiplier interval changed')
    require(type(z) is list and len(z) == 3 and all(type(q) is Q for q in z)
            and z == [4*(q-1) for q in H], 'amplitude direction is not four times H minus one')


def extract_input(data):
    verify_provenance(data)
    require(type(data['held_rows']) is list and len(data['held_rows']) == 40, 'accepted held-row inventory changed')
    selected = {}
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
        require(held[(order, 0)][0] == held[(order, 1)][0], 'held strict precursor locality failed')
    for record in (0, 1):
        require(held[(H5, record)][15] == held[(H5, record)][23], 'held twin-top interchange failed')
    raw_h = data['admission'].get('h')
    require(type(raw_h) is list and len(raw_h) == 11 and all(type(x) is str for x in raw_h), 'accepted multiplier list shape changed')
    H = [rational(x) for x in raw_h[:3]]
    z = [4*(q-1) for q in H]
    verify_direction(H, z)
    evidence = dict(held_rows=[selected[key] for key in keys], H=[str(q) for q in H], z=[str(q) for q in z],
                    full_support_provenance=dict(ordered_support=data['structure']['ordered_support'],
                                                 all_eleven_H_strings=raw_h, arithmetic_indices=[0, 1, 2],
                                                 other_eight_H_used_only_as_authenticated_strings=True),
                    provenance=dict(schema=data['schema'], checker_sha256=data['checker_sha256'],
                                    design_sha256=data['design_sha256'], dependencies=data['dependencies'],
                                    actual_probability_manifest_sha256=data['prefix']['actual_probability_manifest_sha256']),
                    helper_or_prefix_replayed=False)
    return held, H, z, evidence


def lookup(held, order, record, part):
    validate_order(order)
    require(order in HELD, 'numeric q6 or q7 probability lookup forbidden')
    validate_record(record)
    exact_int(part, 0, (1 << len(order))-1, 'invalid exact held ideal mask')
    require(part in HELD_IDEALS[HELD.index(order)], 'held precursor outside complete declared row')
    return held[(order, record)][part]


def forbidden_global(name):
    require(type(name) is str and name not in ('rho', 'epsilon', 's', 'a6', 'a7', 'M6', 'M7', 'q6', 'q7'),
            'numeric actual scale or future row forbidden')
    raise RuntimeError('unknown global request')


def poly(value):
    require(type(value) is dict, 'bivariate polynomial must be an exact sparse object')
    for key, q in value.items():
        require(type(key) is tuple and len(key) == 2 and all(type(i) is int for i in key)
                and 0 <= key[0] <= 8 and 0 <= key[1] <= 4 and type(q) is Q,
                'bivariate exact powers coefficients or global degree changed')
    return {key: q for key, q in value.items() if q}


ZERO, ONE = {}, {(0, 0): Q(1)}


def monomial(a, b, q=Q(1)):
    exact_int(a, 0, 8, 'invalid exact rho power')
    exact_int(b, 0, 4, 'invalid exact epsilon power')
    return poly({(a, b): q})


def add(left, right):
    result = poly(left)
    for key, q in poly(right).items():
        result[key] = result.get(key, Q(0))+q
    return poly(result)


def scale(value, q):
    require(type(q) is Q, 'polynomial scale is not exact rational')
    return poly({key: c*q for key, c in poly(value).items()})


def subtract(left, right):
    return add(left, scale(right, Q(-1)))


def multiply(left, right):
    result = {}
    for (a, b), q in poly(left).items():
        for (c, d), r in poly(right).items():
            key = (a+c, b+d)
            require(key[0] <= 8 and key[1] <= 4, 'polynomial product exceeds frozen bidegree')
            result[key] = result.get(key, Q(0))+q*r
    return poly(result)


def power(value, exponent):
    exact_int(exponent, 0, 4, 'power outside fixed amplitude binomials')
    result = ONE
    for _ in range(exponent):
        result = multiply(result, value)
    return result


def degree_guard(value, rho_degree, epsilon_degree):
    exact_int(rho_degree, 0, 8, 'invalid rho degree bound')
    exact_int(epsilon_degree, 0, 4, 'invalid epsilon degree bound')
    require(all(a <= rho_degree and b <= epsilon_degree for a, b in poly(value)), 'polynomial exceeds prescribed bidegree')
    return poly(value)


def encode(value):
    return [[a, b, str(q)] for (a, b), q in sorted(poly(value).items())]


def decode(value):
    require(type(value) is list and all(type(x) is list and len(x) == 3 and type(x[0]) is int and type(x[1]) is int for x in value),
            'serialized bivariate polynomial shape changed')
    require(len({(x[0], x[1]) for x in value}) == len(value), 'duplicate serialized polynomial power')
    result = poly({(a, b): rational(q) for a, b, q in value})
    require(encode(result) == value, 'serialized polynomial powers are not canonical')
    return result


def evaluate(value, rho, epsilon):
    require(type(rho) is Q and type(epsilon) is Q, 'polynomial proof endpoints must be exact rationals')
    return sum((q*rho**a*epsilon**b for (a, b), q in poly(value).items()), Q(0))


def divide_fixed(value, degree):
    require(type(degree) is int and degree in (2, 6), 'invalid prescribed quotient rho degree')
    value = degree_guard(value, degree+2, 4)
    require(all(a >= 2 and b >= 1 for a, b in value), 'raw polynomial lacks exact epsilon times rho squared factor')
    return degree_guard({(a-2, b-1): q for (a, b), q in value.items()}, degree, 3)


def division_evidence(value, degree):
    quotient = divide_fixed(value, degree)
    raw = [[value.get((a, b), Q(0)) for b in range(5)] for a in range(degree+3)]
    forbidden = [[a, b, str(raw[a][b])] for a in range(degree+3) for b in range(5) if a < 2 or b < 1]
    require(all(q == '0' for _, _, q in forbidden), 'forbidden raw valuation coefficient is nonzero')
    require(multiply(monomial(2, 1), quotient) == poly(value), 'fixed divisor does not reconstruct raw polynomial')
    return dict(raw_bidegree_bound=[degree+2, 4], quotient_bidegree_bound=[degree, 3],
                rho_factor=2, epsilon_factor=1, raw_padded_power=[[str(q) for q in row] for row in raw],
                forbidden_zero_coordinates=forbidden, quotient=encode(quotient), reconstructed_raw=encode(value),
                dynamic_valuation_used=False)


def induced(order, deletion, record, part):
    validate_order(order)
    require(order in (P6, P7), 'deletion outside the two declared symbolic parents')
    validate_record(record)
    full = (1 << len(order))-1
    exact_int(part, 0, full, 'invalid exact symbolic precursor')
    require(part in (PROPER6 if order == P6 else PROPER7), 'symbolic deletion requires a declared proper ideal')
    omitted = (full ^ 7) & ~part
    exact_int(deletion, 1, full, 'invalid exact omitted-maxima deletion')
    require(deletion & omitted == deletion, 'deletion is not a subset of omitted maxima')
    kept = tuple(v for v in range(len(order)) if not deletion & (1 << v))
    def project(mask):
        return sum(((mask >> old) & 1) << new for new, old in enumerate(kept))
    smaller = tuple(project(order[v]) for v in kept)
    validate_order(smaller)
    return smaller, project(record), project(part), kept


def held_factor(held, order, raw_record, part):
    validate_order(order)
    require(order in HELD, 'held factor escaped the three retained classes')
    validate_record(raw_record)
    exact_int(part, 0, (1 << len(order))-1, 'invalid exact held factor precursor')
    proper = part != (1 << len(order))-1
    query = raw_record & part if proper else raw_record
    q = lookup(held, order, query, part)
    return q, dict(order=list(order), raw_record=raw_record, induced_precursor=part,
                   proper_locality_applied=proper, query_record=query, probability=str(q), top_marks_zero=True)


def reconstruct_p6(held, record):
    validate_record(record)
    rows, total = [], Q(0)
    for part in PROPER6:
        omitted = 56 & ~part
        deletion, value, factors = omitted, Q(1), []
        while deletion:
            order, raw, precursor, kept = induced(P6, deletion, record, part)
            q, source = held_factor(held, order, raw, precursor)
            exponent = 1 if deletion.bit_count() % 2 else -1
            value *= q if exponent == 1 else 1/q
            factors.append(dict(deleted_mask=deletion, kept_vertices=list(kept), source=source, exponent=exponent))
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


def sparse_product(factors, field='baseline_factor'):
    require(type(field) is str and field in ('baseline_factor', 'changed_factor'), 'unknown symbolic factor field')
    require(type(factors) is list, 'symbolic factor list changed')
    result = {(0, 0): Q(1)}
    for factor in factors:
        require(type(factor) is dict and 'exponent' in factor and field in factor, 'symbolic factor fields missing')
        exponent = factor['exponent']
        require(type(exponent) is int and exponent in (-1, 1), 'deletion exponent is not exact alternating sign')
        terms = decode(factor[field])
        require(terms, 'zero symbolic deletion factor')
        if exponent == -1:
            require(len(terms) == 1, 'nonmonomial symbolic denominator forbidden')
            (a, b), q = next(iter(terms.items()))
            terms = {(-a, -b): 1/q}
        next_value = {}
        for (a, b), q in result.items():
            for (c, d), r in terms.items():
                key = (a+c, b+d)
                next_value[key] = next_value.get(key, Q(0))+q*r
        result = {key: q for key, q in next_value.items() if q}
    require(result and all(0 <= a <= 4 and 0 <= b <= 4 for a, b in result), 'top Laurent product escaped nonnegative bidegree four')
    return poly(result)


def six_multiplier(part, z):
    exact_int(part, 0, 63, 'invalid exact six-birth ideal')
    require(part in PROPER6+(63,), 'six-birth ideal outside frozen forward inventory')
    if part in (0, 1, 3, 63):
        return ONE, None
    index = 0 if part == 7 else 1 if part in (15, 23, 39) else 2
    return add(ONE, monomial(0, 1, z[index])), index


def slot_multiplier(part, z):
    exact_int(part, 0, 127, 'invalid exact seven-parent precursor')
    require(part in PROPER7, 'top slot outside eighteen proper ideals')
    count = (part >> 3).bit_count()
    if part < 7 or count == 3:
        return ONE, None, 0
    return power(add(ONE, monomial(0, 1, z[count])), 4-count), count, 4-count


def reconstruct_p7(held, z, record, lower, total):
    rows, baseline, changed = [], ZERO, ZERO
    for part in PROPER7:
        budget()
        omitted, factors = 120 & ~part, []
        deletion = omitted
        while deletion:
            order, raw, precursor, kept = induced(P7, deletion, record, part)
            exponent = 1 if deletion.bit_count() % 2 else -1
            if order == P6:
                if precursor == 63:
                    value = subtract(ONE, monomial(1, 0, total))
                    source = dict(kind='symbolic-full-complement', lower_proper_sum=str(total), expression='1-rho*E')
                else:
                    require(precursor in PROPER6, 'symbolic six-parent precursor not an ideal')
                    value = monomial(1, 0, lower[precursor])
                    source = dict(kind='symbolic-proper-monomial', lower_ideal=precursor,
                                  lower_potential_coefficient=str(lower[precursor]), expression='rho*u6')
                multiplier, index = six_multiplier(precursor, z)
                require(exponent == 1, 'six-parent amplitude or complement would become a denominator')
            else:
                q, source = held_factor(held, order, raw, precursor)
                value, multiplier, index = monomial(0, 0, q), ONE, None
            factors.append(dict(deleted_mask=deletion, kept_vertices=list(kept), induced_order=list(order),
                                raw_record=raw, induced_precursor=precursor, source=source, exponent=exponent,
                                baseline_factor=encode(value), amplitude_multiplier=encode(multiplier),
                                multiplier_index=index, changed_factor=encode(multiply(value, multiplier))))
            deletion = (deletion-1) & omitted
        value, changed_value = sparse_product(factors), sparse_product(factors, 'changed_factor')
        multiplier, index, exponent = slot_multiplier(part, z)
        require(changed_value == multiply(value, multiplier), 'singleton amplitude multiplier power identity failed')
        rows.append(dict(ideal=part, included_caps=(part >> 3).bit_count(), factors=factors,
                         baseline_potential=encode(value), multiplier=encode(multiplier), multiplier_index=index,
                         multiplier_power=exponent, changed_potential=encode(changed_value)))
        baseline, changed = add(baseline, value), add(changed, changed_value)
    require(len(rows) == 18 and sum(len(row['factors']) for row in rows) == 110, 'eighteen-slot top deletion inventory changed')
    return rows, baseline, changed


def verify_top_rows(held, z, record, lower, total, rows):
    expected, _, _ = reconstruct_p7(held, z, record, lower, total)
    require(type(rows) is list and len(rows) == 18, 'top proper-slot list coverage changed')
    for row in rows:
        require(type(row) is dict and 'ideal' in row and 'multiplier' in row and 'changed_potential' in row,
                'top slot multiplier evidence fields missing')
        multiplier, _, _ = slot_multiplier(row['ideal'], z)
        require(decode(row['multiplier']) == multiplier, 'top slot lost its prescribed amplitude polynomial')
        if (row['ideal'] >> 3).bit_count() == 3:
            require(decode(row['changed_potential']) == subtract(ONE, monomial(1, 0, total)),
                    'three-cap full complement was modified')
    strict_shape(rows, expected)
    require(canonical(rows) == canonical(expected), 'top labeled factors transport multipliers or multiplicity changed')


def L(z, exponent):
    require(type(z) is Q, 'binomial direction must be exact rational')
    exact_int(exponent, 2, 4, 'binomial degree outside two three four')
    result = {(0, k-1): Q(comb(exponent, k))*z**k for k in range(1, exponent+1)}
    result = poly(result)
    require(multiply(monomial(0, 1), result) == subtract(power(add(ONE, monomial(0, 1, z)), exponent), ONE),
            'amplitude divided-binomial polynomial identity failed')
    return result


def closed_polynomials(held, z, record):
    validate_record(record)
    A = {s: lookup(held, C3, record, s) for s in (0, 1, 3, 7)}
    B = {s: lookup(held, C4, record, s) for s in (0, 1, 3, 7)}
    G = {s: lookup(held, H5, record, s) for s in (0, 1, 3, 7)}
    c, h, j = lookup(held, C4, record, 15), lookup(held, H5, record, 15), lookup(held, H5, record, 31)
    e_terms = [A[s]*G[s]**3/B[s]**3 for s in (0, 1, 3, 7)]
    k_terms = [A[s]**3*G[s]**6/B[s]**8 for s in (0, 1, 3, 7)]
    total, K = sum(e_terms, Q(0))+3*h*h/c+3*j, sum(k_terms, Q(0))
    p, v = k_terms[-1], h**3/c**2
    U = poly({(0, 0): Q(4), (1, 0): -4*total, (2, 0): 6*j, (3, 0): 4*v, (4, 0): K})
    d = add(add(multiply(monomial(2, 0, p), L(z[0], 4)), multiply(monomial(1, 0, 4*v), L(z[1], 3))),
            scale(L(z[2], 2), 6*j))
    D = multiply(monomial(2, 1), d)
    direct_D = ZERO
    for rho_degree, coefficient, index, exponent in ((4, p, 0, 4), (3, 4*v, 1, 3), (2, 6*j, 2, 2)):
        direct_D = add(direct_D, multiply(monomial(rho_degree, 0, coefficient),
                                         subtract(power(add(ONE, monomial(0, 1, z[index])), exponent), ONE)))
    require(D == direct_D, 'closed raw and divided amplitude formulas disagree')
    evidence = dict(E=str(total), E_terms=[str(q) for q in e_terms], E_one_cap_total=str(3*h*h/c),
                    E_two_cap_total=str(3*j), K=str(K), K_terms=[str(q) for q in k_terms],
                    p=str(p), v=str(v), c=str(c), h=str(h), j=str(j), U=encode(U), D=encode(D), d=encode(d))
    return total, U, D, d, evidence


def verify_upper_bound(sums, bound, amplitude):
    require(type(sums) is list and len(sums) == 2 and all(type(q) is Q and q > 0 for q in sums),
            'selected lower-potential sums are not positive rationals')
    require(type(bound) is Q and bound == 1/(2*(1+max(sums))) and bound > 0,
            'selected-row outer rho bound changed or became an actual scale')
    require(type(amplitude) is Q and amplitude == AMPLITUDE, 'fixed amplitude ceiling changed')
    require(all(1-bound*q > Q(1, 2) for q in sums), 'selected symbolic full-complement positivity bound failed')


def tensor_domain(bound, amplitude, degree):
    require(type(bound) is Q and bound > 0, 'tensor rho bound must be exact positive rational')
    require(type(amplitude) is Q and amplitude == AMPLITUDE, 'fixed amplitude ceiling changed')
    require(type(degree) is tuple and len(degree) == 2 and all(type(n) is int for n in degree)
            and degree in ((2, 3), (6, 3)), 'predeclared tensor degree or axis order changed')


def rational_grid(value, degree):
    require(type(value) is list and len(value) == degree[0]+1
            and all(type(row) is list and len(row) == degree[1]+1 for row in value),
            'tensor grid lost complete padded dimensions')
    return [[rational(q) for q in row] for row in value]


def grid_strings(value):
    return [[str(q) for q in row] for row in value]


def padded_grid(value, degree):
    value = degree_guard(value, *degree)
    return [[value.get((a, b), Q(0)) for b in range(degree[1]+1)] for a in range(degree[0]+1)]


def reverse_tensor(beta, bound, amplitude, degree):
    """Independent binomial basis expansion to scaled, then original powers."""
    tensor_domain(bound, amplitude, degree)
    require(type(beta) is list and len(beta) == degree[0]+1
            and all(type(row) is list and len(row) == degree[1]+1 and all(type(q) is Q for q in row) for row in beta),
            'reverse tensor requires exact full rational grid')
    m, n = degree
    scaled = [[Q(0) for _ in range(n+1)] for _ in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            for a in range(i, m+1):
                for b in range(j, n+1):
                    scaled[a][b] += beta[i][j]*comb(m, i)*comb(m-i, a-i)*comb(n, j)*comb(n-j, b-j)*(-1)**(a-i+b-j)
    original = [[scaled[a][b]/(bound**a*amplitude**b) for b in range(n+1)] for a in range(m+1)]
    return scaled, original


def univariate_bernstein(coefficients, endpoint, degree):
    """Fixed-degree edge transform, independent of the tensor forward loops."""
    require(type(endpoint) is Q and endpoint > 0 and type(degree) is int and degree in (2, 3, 6),
            'invalid fixed edge transform domain')
    require(type(coefficients) is list and len(coefficients) == degree+1 and all(type(q) is Q for q in coefficients),
            'edge polynomial lost padded coefficient coverage')
    return [sum((coefficients[a]*endpoint**a*Q(comb(i, a), comb(degree, a)) for a in range(i+1)), Q(0))
            for i in range(degree+1)]


def tensor(value, bound, amplitude, degree):
    tensor_domain(bound, amplitude, degree)
    original = padded_grid(value, degree)
    m, n = degree
    scaled = [[original[a][b]*bound**a*amplitude**b for b in range(n+1)] for a in range(m+1)]
    beta = [[sum((scaled[a][b]*Q(comb(i, a), comb(m, a))*Q(comb(j, b), comb(n, b))
                  for a in range(i+1) for b in range(j+1)), Q(0)) for j in range(n+1)] for i in range(m+1)]
    reverse_scaled, reverse_original = reverse_tensor(beta, bound, amplitude, degree)
    require(reverse_scaled == scaled, 'tensor reverse expansion does not recover scaled powers')
    require(reverse_original == original, 'tensor reverse rescaling does not recover original powers')
    rho_zero = univariate_bernstein(original[0], amplitude, n)
    rho_upper_power = [sum((original[a][b]*bound**a for a in range(m+1)), Q(0)) for b in range(n+1)]
    rho_upper = univariate_bernstein(rho_upper_power, amplitude, n)
    epsilon_zero = univariate_bernstein([original[a][0] for a in range(m+1)], bound, m)
    epsilon_upper_power = [sum((original[a][b]*amplitude**b for b in range(n+1)), Q(0)) for a in range(m+1)]
    epsilon_upper = univariate_bernstein(epsilon_upper_power, bound, m)
    require(rho_zero == beta[0] and rho_upper == beta[-1]
            and epsilon_zero == [row[0] for row in beta] and epsilon_upper == [row[-1] for row in beta],
            'tensor four-edge endpoint identities failed')
    corner = evaluate(value, bound, amplitude)
    require(corner == beta[-1][-1], 'included two-axis corner identity failed')
    return dict(polynomial=encode(value), axis_order=['rho', 'epsilon'], basis_degree=list(degree),
                R=str(bound), E=str(amplitude), padded_power=grid_strings(original), scaled_power=grid_strings(scaled),
                bernstein=grid_strings(beta), reverse_scaled_power=grid_strings(reverse_scaled),
                reverse_original_power=grid_strings(reverse_original),
                edges=dict(rho_zero=[str(q) for q in rho_zero], rho_upper=[str(q) for q in rho_upper],
                           epsilon_zero=[str(q) for q in epsilon_zero], epsilon_upper=[str(q) for q in epsilon_upper]),
                included_corner=str(corner), subdivision_used=False, adaptive_degree_elevation_used=False)


def verify_tensor(value, bound, amplitude, degree, evidence):
    tensor_domain(bound, amplitude, degree)
    require(type(evidence) is dict and 'axis_order' in evidence and 'basis_degree' in evidence and 'bernstein' in evidence,
            'tensor evidence fields missing')
    require(canonical(evidence['axis_order']) == canonical(['rho', 'epsilon']), 'tensor axis order changed')
    require(type(evidence['basis_degree']) is list and all(type(x) is int for x in evidence['basis_degree'])
            and evidence['basis_degree'] == list(degree), 'predeclared tensor degree or axis order changed')
    beta = rational_grid(evidence['bernstein'], degree)
    reverse_scaled, reverse_original = reverse_tensor(beta, bound, amplitude, degree)
    original = padded_grid(value, degree)
    require(reverse_original == original, 'retained tensor coordinates fail independent reverse identity')
    require(reverse_scaled == [[original[a][b]*bound**a*amplitude**b for b in range(degree[1]+1)]
                               for a in range(degree[0]+1)], 'retained tensor coordinates fail scaled reverse identity')
    expected = tensor(value, bound, amplitude, degree)
    strict_shape(evidence, expected)
    require(canonical(evidence) == canonical(expected), 'fixed tensor evidence reconstruction mismatch')


def extract_regression(data, bound):
    require(type(data) is dict and set(data) == RI91_KEYS, 'accepted RI91 top-level schema changed')
    require(data['schema'] == 'ri91-relative-obstruction-v1' and data['checker_sha256'] == RI91_CHECKER
            and data['design_sha256'] == RI89_DESIGN and type(data['design_bytes']) is int and data['design_bytes'] == 21769,
            'accepted RI91 source provenance changed')
    require(canonical(data['accepted_input']) == canonical(dict(sha256=INPUT_PINS['ri88'][1], bytes=INPUT_PINS['ri88'][0])),
            'accepted RI91 construction input provenance changed')
    require(canonical(data['selected_parent']) == canonical(list(P7)) and type(data['records']) is list
            and len(data['records']) == 2 and all(type(x) is dict and type(x.get('record')) is int for x in data['records'])
            and [x['record'] for x in data['records']] == [0, 1], 'accepted RI91 parent or record scope changed')
    require(type(data['scale_domain']) is dict and data['scale_domain'].get('R') == str(bound), 'accepted RI91 outer radius changed')
    decision = data['decision']
    require(type(decision) is dict and decision.get('disposition') == 'certified-positive-obstruction'
            and decision.get('actual_global_scales_computed') is False and decision.get('selector_acceptance_claimed') is False,
            'accepted RI91 positive boundary disposition changed')
    evidence = decision.get('bernstein_evidence')
    require(type(evidence) is dict and set(evidence) == {'A', 'G0', 'G1'}, 'accepted seventeen-coordinate labels changed')
    result = {}
    for name, degree in (('A', 2), ('G0', 6), ('G1', 6)):
        item = evidence[name]
        require(type(item) is dict and type(item.get('rho_factor')) is int and item['rho_factor'] == 2
                and type(item.get('basis_degree')) is int and item['basis_degree'] == degree and item.get('R') == str(bound)
                and item.get('subdivision_used') is False and item.get('adaptive_degree_elevation_used') is False,
                'accepted RI91 fixed degree factor or radius changed')
        raw = item.get('bernstein')
        require(type(raw) is list and len(raw) == degree+1, 'accepted seventeen-coordinate coverage changed')
        values = [rational(q) for q in raw]
        require(all(q > 0 for q in values), 'accepted endpoint anchor is not strictly positive')
        result[name] = values
    return result


def verify_anchor(evidence, reference, factor=Q(4)):
    require(type(factor) is Q and factor == 4, 'endpoint regression requires exact factor four')
    require(type(reference) is dict and set(reference) == {'A', 'G0', 'G1'}, 'accepted seventeen-coordinate labels changed')
    result = {}
    for name, degree in (('A', 2), ('G0', 6), ('G1', 6)):
        require(type(reference[name]) is list and len(reference[name]) == degree+1
                and all(type(q) is Q and q > 0 for q in reference[name]), 'accepted endpoint anchor is not strictly positive')
        beta = rational_grid(evidence[name]['bernstein'], (degree, 3))
        endpoint = [row[-1] for row in beta]
        require(endpoint == [factor*q for q in reference[name]], 'amplitude endpoint does not equal four times accepted RI91 anchor')
        result[name] = dict(accepted=[str(q) for q in reference[name]], new_last_column=[str(q) for q in endpoint], factor='4')
    return dict(entry_count=17, strict_positive=True, epsilon='1/4', identities=result,
                saved_native_U_D_C_used=False, independent_derivation_claimed=False)


def sign_summary(evidence):
    require(type(evidence) is dict and set(evidence) == {'A', 'G0', 'G1'}, 'sign test requires A and both G grids')
    tests, failing = {}, []
    for name, degree in (('A', 2), ('G0', 6), ('G1', 6)):
        grid = rational_grid(evidence[name]['bernstein'], (degree, 3))
        tests[name] = dict(all_nonnegative=all(q >= 0 for row in grid for q in row),
                           strict_corner_required=name != 'A', included_corner=str(grid[-1][-1]),
                           corner_condition=name == 'A' or grid[-1][-1] > 0)
        for i, row in enumerate(grid):
            for j, q in enumerate(row):
                if q < 0:
                    failing.append(dict(polynomial=name, rho_index=i, epsilon_index=j, coefficient=str(q)))
    passes = all(x['all_nonnegative'] and x['corner_condition'] for x in tests.values())
    return dict(sufficient_positive=passes, tests=tests, negative_coefficients=failing,
                negative_coefficients_do_not_assert_roots=True, roots_examined=False)


def verify_sign_summary(evidence, saved):
    expected = sign_summary(evidence)
    strict_shape(saved, expected)
    require(canonical(saved) == canonical(expected), 'positive-only sign summary or ordered failing indices changed')


def decide_native(evidence, reference):
    anchor = verify_anchor(evidence, reference)
    signs = sign_summary(evidence)
    if signs['sufficient_positive']:
        disposition = 'certified-positive-amplitude-obstruction'
    else:
        require(bool(signs['negative_coefficients']), 'native endpoint-anchored failure has no negative coefficient')
        disposition = 'unresolved-fixed-bivariate-bernstein'
    return dict(disposition=disposition, sign_summary=signs, endpoint_regression=anchor,
                negative_or_blind_native_branch=False, root_diagnostic_performed=False,
                actual_global_scales_computed=False, selector_acceptance_claimed=False,
                pair_obstruction_only=True, test_is_sufficient_not_necessary=True)


def build_witness(data, regression):
    held, H, z, inputs = extract_input(data)
    records, sums, U, D, d = [], [], [], [], []
    for record in (0, 1):
        lower, lower_sum, lower_rows = reconstruct_p6(held, record)
        verify_lower_rows(held, record, lower_rows, lower_sum)
        total, closed_U, closed_D, closed_d, closed = closed_polynomials(held, z, record)
        require(total == lower_sum, 'closed E disagrees with independent lower deletion sum')
        slots, generic_U, generic_V = reconstruct_p7(held, z, record, lower, lower_sum)
        verify_top_rows(held, z, record, lower, lower_sum, slots)
        generic_D = subtract(generic_V, generic_U)
        generic_d = divide_fixed(generic_D, 2)
        require(generic_U == closed_U and generic_D == closed_D and generic_d == closed_d,
                'closed formulas disagree with independent individual deletion products')
        records.append(dict(record=record, lower_symbolic_slots=lower_rows, top_proper_slots=slots, closed_form=closed,
                            generic_U=encode(generic_U), generic_V=encode(generic_V), generic_D=encode(generic_D),
                            divided_d=encode(generic_d)))
        sums.append(total)
        U.append(generic_U)
        D.append(generic_D)
        d.append(generic_d)
    bound = 1/(2*(1+max(sums)))
    verify_upper_bound(sums, bound, AMPLITUDE)
    A_raw = subtract(D[1], D[0])
    C_raw = subtract(multiply(D[1], U[0]), multiply(D[0], U[1]))
    V = [add(u, delta) for u, delta in zip(U, D)]
    alternate_C_raw = subtract(multiply(V[1], U[0]), multiply(V[0], U[1]))
    require(C_raw == alternate_C_raw, 'full-ratio cross multiplication lost a complement term')
    A, C = divide_fixed(A_raw, 2), divide_fixed(C_raw, 6)
    require(A == subtract(d[1], d[0]) and C == subtract(multiply(d[1], U[0]), multiply(d[0], U[1])),
            'raw division and divided cross multiplication disagree')
    G_raw = [subtract(scale(multiply(add(ONE, u), A_raw), Q(2)), C_raw) for u in U]
    G = [divide_fixed(value, 6) for value in G_raw]
    require(G == [subtract(scale(multiply(add(ONE, u), A), Q(2)), C) for u in U], 'raw and divided G constructions disagree')
    s_endpoints = []
    for i, u in enumerate(U):
        denominator = scale(add(ONE, u), Q(2))
        numerator = subtract(multiply(denominator, A), C)
        raw_numerator = subtract(multiply(denominator, A_raw), C_raw)
        require(numerator == G[i] and raw_numerator == G_raw[i]
                and raw_numerator == multiply(monomial(2, 1), G[i]), 'full-complement s endpoint numerator identity failed')
        s_endpoints.append(dict(index=i, denominator=encode(denominator), divided_numerator=encode(numerator),
                               raw_numerator=encode(raw_numerator), divided_residual=encode(subtract(numerator, G[i])),
                               raw_residual=encode(subtract(raw_numerator, multiply(monomial(2, 1), G[i]))),
                               reciprocal_defines_b_i=True, denominator_positive_by_domain_proof=True,
                               numerical_s_selected=False))
    evidence = {name: tensor(value, bound, AMPLITUDE, (degree, 3))
                for name, value, degree in (('A', A, 2), ('G0', G[0], 6), ('G1', G[1], 6))}
    for name, value, degree in (('A', A, 2), ('G0', G[0], 6), ('G1', G[1], 6)):
        verify_tensor(value, bound, AMPLITUDE, (degree, 3), evidence[name])
    reference = extract_regression(regression, bound)
    decision = decide_native(evidence, reference)
    witness = dict(schema=SCHEMA, design_sha256=DESIGN_SHA256, design_bytes=DESIGN_BYTES,
                   accepted_inputs={role: dict(bytes=size, sha256=pin) for role, (size, pin) in INPUT_PINS.items()},
                   inputs=inputs, selected_parent=list(P7), records=records,
                   scale_domain=dict(R=str(bound), amplitude_ceiling='1/4', selected_E=[str(q) for q in sums],
                                     symbolic_lower_full_margins_at_R=[str(1-bound*q) for q in sums],
                                     rho_interval='0<rho<=R', epsilon_interval='0<epsilon<=1/4',
                                     s_interval='0<s<=min_i 1/[2(1+Ui(rho))]', actual_scales_selected=False,
                                     modified_full_positivity_not_claimed=True),
                   cross_multiplication=dict(fixed_raw_divisor=dict(rho_power=2, epsilon_power=1),
                                             A_raw=encode(A_raw), C_raw=encode(C_raw), C_raw_via_V=encode(alternate_C_raw),
                                             G_raw=[encode(x) for x in G_raw], A=encode(A), C=encode(C), G=[encode(x) for x in G],
                                             F_divided_by_s_power=[encode(A), encode(scale(C, Q(-1)))]),
                   full_complement_s_endpoints=s_endpoints,
                   fixed_division_evidence={name: division_evidence(value, degree) for name, value, degree in
                                            (('D0', D[0], 2), ('D1', D[1], 2), ('A', A_raw, 2),
                                             ('C', C_raw, 6), ('G0', G_raw[0], 6), ('G1', G_raw[1], 6))},
                   tensor_evidence=evidence, decision=decision,
                   coverage=dict(held_rows=6, held_probability_slots=32, H_values_in_arithmetic=3,
                                 full_support_provenance_classes=11, record_assignments=2, lower_symbolic_slots=20,
                                 lower_held_factors=80, top_proper_slots=36, top_deletion_factors=220,
                                 tensor_degrees=[[2, 3], [6, 3], [6, 3]], tensor_entries=68, regression_entries=17,
                                 included_full_probability_rows=0),
                   limitations=dict(numeric_q6_q7_or_global_M_computed=False, helper_prefix_replayed=False,
                                    no_other_records_parents_or_adaptive_search=True, no_root_or_negative_native_search=True,
                                    regression_replay_is_not_independent_derivation=True,
                                    programme_or_gravity_completion_claimed=False))
    return copy_json(witness), held, H, z, reference


FIXTURE_NAMES = (
    'positive', 'negative-generic-orientation', 'weak-A-zero', 'blind', 'included-binding-s-endpoint',
    'conservative-both-endpoints', 'positive-mixed-amplitude-basis', 'endpoint-positive-interior-zero',
    'strict-corner-only-support', 'included-rho-edge-zero', 'included-epsilon-edge-zero', 'unequal-axis-scaling',
)

REFUSAL_NAMES = (
    'duplicate-json-key', 'decimal-json', 'nonfinite-json', 'unreduced-rational', 'boolean-rational',
    'wrong-ri88-size', 'wrong-ri88-hash', 'wrong-ri91-size', 'wrong-ri91-hash',
    'wrong-ri88-source', 'wrong-actual-prefix', 'bool-provenance-count', 'extra-ri88-field', 'missing-ri88-field',
    'changed-full-eleven-support-order', 'missing-full-eleven-H-provenance', 'reordered-selected-rows',
    'extra-selected-record', 'bool-selected-record', 'bool-held-order', 'missing-held-full-slot',
    'duplicate-held-slot', 'nonpositive-held-probability', 'changed-held-locality', 'changed-twin-top-invariance',
    'changed-H1', 'changed-H-bound', 'wrong-direction-factor-four', 'bool-direction-value',
    'numeric-six-parent-query', 'numeric-seven-parent-query', 'C5-query-refusal', 'nested-unhashable-order', 'extra-record-query',
    'no-actual-rho', 'no-actual-epsilon', 'no-actual-s', 'no-actual-a6', 'no-actual-a7',
    'no-actual-M6', 'no-actual-M7', 'no-actual-q6', 'no-actual-q7',
    'full-top-ideal-not-proper', 'delete-nonmaximal-vertex', 'bool-deletion-mask', 'bool-symbolic-precursor',
    'wrong-independent-E', 'missing-lower-slot', 'wrong-lower-factor-exponent', 'missing-top-slot', 'duplicate-top-slot',
    'collapsed-labeled-slot-weight', 'wrong-transported-record', 'wrong-proper-locality-record',
    'missing-singleton-amplitude', 'wrong-amplitude-individual-power', 'modified-symbolic-full-complement',
    'zero-deletion-exponent', 'invert-amplitude-binomial', 'invert-full-complement-binomial', 'surviving-negative-Laurent-power',
    'bool-polynomial-power', 'bool-polynomial-coefficient', 'polynomial-global-bidegree-expansion',
    'polynomial-duplicate-power', 'polynomial-explicit-zero', 'raw-epsilon-zero-coefficient',
    'raw-rho-zero-coefficient', 'raw-rho-one-coefficient', 'raw-D-rho-degree-expansion',
    'divided-A-degree-expansion', 'divided-G-amplitude-degree-expansion', 'selected-bound-as-half',
    'changed-amplitude-ceiling', 'zero-tensor-radius', 'adaptive-tensor-degree', 'bool-tensor-degree',
    'transposed-tensor-axis-order', 'changed-fixed-tensor-degree', 'missing-tensor-row', 'missing-tensor-column',
    'extra-tensor-column', 'bool-tensor-coordinate', 'altered-tensor-coordinate', 'wrong-amplitude-scaled-power',
    'wrong-reverse-sign', 'scaled-is-not-original-grid', 'omitted-zero-padding', 'wrong-upper-edge-identity',
    'wrong-included-corner', 'missing-second-G-sign-grid',
    'false-sign-positive', 'false-sign-negative-generic-orientation', 'false-sign-weak-A-zero', 'false-sign-blind',
    'false-sign-included-binding-s-endpoint', 'false-sign-conservative-both-endpoints',
    'false-sign-positive-mixed-amplitude-basis', 'false-sign-endpoint-positive-interior-zero',
    'false-sign-strict-corner-only-support', 'false-sign-included-rho-edge-zero', 'false-sign-included-epsilon-edge-zero',
    'missing-ordered-failure', 'reordered-failure-indices', 'wrong-failure-value', 'bool-failure-index',
    'wrong-ri91-source', 'wrong-ri91-input-provenance', 'wrong-ri91-parent', 'bool-ri91-record',
    'wrong-ri91-radius', 'wrong-ri91-degree', 'missing-ri91-anchor-entry', 'zero-ri91-anchor',
    'wrong-endpoint-factor-four', 'anchor-positivity-without-equality', 'wrong-new-schema',
    'extra-new-certificate-field', 'missing-new-certificate-field', 'noncanonical-saved-serialization',
    'bool-new-record', 'missing-retained-input-row', 'wrong-raw-divisor-rho', 'wrong-raw-divisor-epsilon',
    'forged-raw-zero-coordinate', 'wrong-full-complement-s-endpoint', 'full-complement-endpoint-is-not-actual-s',
    'claim-native-negative-branch', 'claim-native-blind-branch', 'claim-native-root-branch',
    'claim-numeric-actual-scale', 'claim-selector-acceptance', 'claim-independent-regression',
)


def synthetic_fixtures():
    """The fixed twelve algebra-only fixtures; none is an additional native model."""
    R, E = Q(1), AMPLITUDE
    x, y = monomial(1, 0), monomial(0, 1, 1/E)
    centered = subtract(y, monomial(0, 0, Q(1, 2)))
    mixed = add(power(centered, 2), monomial(0, 0, Q(1, 16)))
    interior_zero = power(subtract(scale(y, Q(2)), ONE), 2)
    configurations = (
        ('positive', ONE, ZERO, True),
        ('negative-generic-orientation', scale(ONE, Q(-1)), ZERO, False),
        ('weak-A-zero', ZERO, scale(ONE, Q(-1)), True),
        ('blind', ZERO, ZERO, False),
        ('included-binding-s-endpoint', ONE, scale(ONE, Q(8)), False),
        ('conservative-both-endpoints', ONE, scale(ONE, Q(6)), False),
        ('positive-mixed-amplitude-basis', mixed, ZERO, False),
        ('endpoint-positive-interior-zero', interior_zero, ZERO, False),
    )
    results = {}
    for name, A, C, expected in configurations:
        U = [ONE, monomial(0, 0, Q(3))]
        d = [scale(subtract(A, C), Q(1, 2)), scale(subtract(scale(A, Q(3)), C), Q(1, 2))]
        require(subtract(d[1], d[0]) == A
                and subtract(multiply(d[1], U[0]), multiply(d[0], U[1])) == C,
                'synthetic d U cross identities failed')
        G = [subtract(scale(multiply(add(ONE, u), A), Q(2)), C) for u in U]
        require(G == [subtract(scale(A, Q(4)), C), subtract(scale(A, Q(8)), C)], 'synthetic unequal-cap G identity failed')
        tensors = {label: tensor(value, R, E, (degree, 3)) for label, value, degree in
                   (('A', A, 2), ('G0', G[0], 6), ('G1', G[1], 6))}
        signs = sign_summary(tensors)
        require(signs['sufficient_positive'] is expected, 'fixed synthetic sign outcome changed')
        results[name] = dict(kind='algebra-only-d-and-U', R='1', E='1/4', U=[encode(u) for u in U],
                             d=[encode(value) for value in d], A=encode(A), C=encode(C), G=[encode(value) for value in G],
                             tensor_evidence=tensors, sign_summary=signs, expected_positive=expected,
                             binding_s_upper_bound='1/8', native_model_claimed=False)
    negative = results['negative-generic-orientation']
    reverse_evidence = {label: tensor(scale(decode(negative[key][index] if key == 'G' else negative[key]), Q(-1)), R, E, (degree, 3))
                        for label, key, index, degree in (('A', 'A', 0, 2), ('G0', 'G', 0, 6), ('G1', 'G', 1, 6))}
    require(sign_summary(reverse_evidence)['sufficient_positive'], 'synthetic reverse orientation identity failed')
    negative['generic_reverse_orientation_passes'] = True
    require(evaluate(decode(results['included-binding-s-endpoint']['A']), R, E)
            -Q(1, 8)*evaluate(decode(results['included-binding-s-endpoint']['C']), R, E) == 0,
            'synthetic included binding endpoint identity failed')
    require(evaluate(interior_zero, R, E/2) == 0 and evaluate(interior_zero, R, E) == 1,
            'synthetic interior zero and positive endpoint identity failed')
    require(results['positive-mixed-amplitude-basis']['tensor_evidence']['A']['bernstein'][0]
            == ['5/16', '-1/48', '-1/48', '5/16'], 'synthetic mixed amplitude coordinates changed')
    U = [ONE, add(ONE, monomial(4, 0))]
    shared_d = multiply(monomial(2, 0), power(y, 3))
    A, C = ZERO, subtract(multiply(shared_d, U[0]), multiply(shared_d, U[1]))
    G = [subtract(scale(multiply(add(ONE, u), A), Q(2)), C) for u in U]
    require(G[0] == G[1] == multiply(monomial(6, 0), power(y, 3)), 'strict corner support identity failed')
    tensors = {label: tensor(value, R, E, (degree, 3)) for label, value, degree in
               (('A', A, 2), ('G0', G[0], 6), ('G1', G[1], 6))}
    signs = sign_summary(tensors)
    require(signs['sufficient_positive'], 'excluded axes were incorrectly required strict')
    for label in ('G0', 'G1'):
        grid = rational_grid(tensors[label]['bernstein'], (6, 3))
        require(all(q == (1 if (i, j) == (6, 3) else 0) for i, row in enumerate(grid) for j, q in enumerate(row)),
                'strict corner-only grid support changed')
    results['strict-corner-only-support'] = dict(kind='algebra-only-d-and-U', R='1', E='1/4', U=[encode(u) for u in U],
                                                d=[encode(shared_d), encode(shared_d)], A=encode(A), C=encode(C),
                                                G=[encode(value) for value in G], tensor_evidence=tensors,
                                                sign_summary=signs, expected_positive=True, excluded_axes_may_vanish=True,
                                                native_model_claimed=False)
    for name, Gedge in (('included-rho-edge-zero', subtract(ONE, x)), ('included-epsilon-edge-zero', subtract(ONE, y))):
        tensors = dict(A=tensor(ONE, R, E, (2, 3)), G0=tensor(Gedge, R, E, (6, 3)), G1=tensor(Gedge, R, E, (6, 3)))
        signs = sign_summary(tensors)
        require(not signs['sufficient_positive'] and not signs['negative_coefficients'], 'included zero edge was accepted as strict')
        results[name] = dict(kind='polynomial-only-edge', R='1', E='1/4', tensor_evidence=tensors,
                             sign_summary=signs, expected_positive=False, native_model_claimed=False)
    unequal = add(monomial(2, 1), monomial(1, 3, Q(2)))
    evidence = tensor(unequal, R, E, (2, 3))
    verify_tensor(unequal, R, E, (2, 3), evidence)
    require(evidence['scaled_power'][2][1] == '1/4' and evidence['scaled_power'][1][3] == '1/32',
            'unequal-axis fixture lost distinct amplitude scaling powers')
    results['unequal-axis-scaling'] = dict(kind='polynomial-only-scaling', R='1', E='1/4',
                                          polynomial=encode(unequal), tensor_evidence=evidence, native_model_claimed=False)
    require(tuple(results) == FIXTURE_NAMES and len(results) == 12, 'frozen synthetic fixture inventory changed')
    return results


def refusal_controls(witness, raw_inputs, data, regression, held, H, z, reference):
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
    for role in ('ri88', 'ri91'):
        expect('wrong-'+role+'-size', 'accepted '+role+' certificate byte size mismatch',
               lambda role=role: verify_input_bytes(role, raw_inputs[role][:-1]))
        expect('wrong-'+role+'-hash', 'accepted '+role+' certificate byte hash mismatch',
               lambda role=role: verify_input_bytes(role, b'!'+raw_inputs[role][1:]))
    expect('wrong-ri88-source', 'accepted RI88 source provenance changed',
           lambda: verify_provenance(altered(data, ['checker_sha256'], '0'*64)))
    expect('wrong-actual-prefix', 'accepted actual strict-prefix provenance changed',
           lambda: verify_provenance(altered(data, ['prefix', 'actual_probability_manifest_sha256'], '0'*64)))
    expect('bool-provenance-count', 'accepted held-coverage provenance changed',
           lambda: verify_provenance(altered(data, ['coverage', 'held_marked_rows'], True)))
    expect('extra-ri88-field', 'accepted RI88 top-level schema changed', lambda: verify_provenance(dict(data, extra=None)))
    expect('missing-ri88-field', 'accepted RI88 top-level schema changed',
           lambda: verify_provenance({k: v for k, v in data.items() if k != 'schema'}))
    expect('changed-full-eleven-support-order', 'accepted eleven-class support order changed',
           lambda: verify_provenance(altered(data, ['structure', 'ordered_support'], list(reversed(data['structure']['ordered_support'])))))
    expect('missing-full-eleven-H-provenance', 'accepted multiplier list shape changed',
           lambda: extract_input(altered(data, ['admission', 'h'], data['admission']['h'][:-1])))
    reordered = copy_json(data)
    reordered['held_rows'][0], reordered['held_rows'][1] = reordered['held_rows'][1], reordered['held_rows'][0]
    expect('reordered-selected-rows', 'selected held rows were reordered', lambda: extract_input(reordered))
    entry = witness['inputs']['held_rows'][0]
    expect('extra-selected-record', 'record outside the two frozen exact markings',
           lambda: validate_held_entry(altered(entry, ['record'], 2)))
    expect('bool-selected-record', 'record outside the two frozen exact markings',
           lambda: validate_held_entry(altered(entry, ['record'], False)))
    expect('bool-held-order', 'held order exact mask types changed', lambda: validate_held_entry(altered(entry, ['order', 0], False)))
    expect('missing-held-full-slot', 'held row lost labeled ideal coverage',
           lambda: validate_held_entry(altered(entry, ['probabilities'], entry['probabilities'][:-1])))
    expect('duplicate-held-slot', 'held row lost labeled ideal coverage', lambda: validate_held_entry(altered(entry, ['probabilities', 1, 0], 0)))
    expect('nonpositive-held-probability', 'held row lost strict positive normalization',
           lambda: validate_held_entry(altered(entry, ['probabilities', 0, 1], '-1')))
    changed_locality = copy_json(data)
    row = changed_locality['held_rows'][0]['probabilities']
    transfer = rational(row[0][1])/2
    row[0][1], row[-1][1] = str(transfer), str(rational(row[-1][1])+transfer)
    expect('changed-held-locality', 'held strict precursor locality failed', lambda: extract_input(changed_locality))
    changed_twin = copy_json(data)
    twin_entry = next(x for x in changed_twin['held_rows'] if x['order'] == list(H5) and x['record'] == 0)
    row = twin_entry['probabilities']
    transfer = rational(row[4][1])/2
    row[4][1], row[6][1] = str(transfer), str(rational(row[6][1])+transfer)
    expect('changed-twin-top-invariance', 'held twin-top interchange failed', lambda: extract_input(changed_twin))
    expect('changed-H1', 'accepted H1 multiplier changed', lambda: verify_direction([Q(1)]+H[1:], z))
    expect('changed-H-bound', 'accepted multiplier interval changed', lambda: verify_direction([H[0], Q(3, 2), H[2]], z))
    expect('wrong-direction-factor-four', 'amplitude direction is not four times H minus one',
           lambda: verify_direction(H, [q-1 for q in H]))
    expect('bool-direction-value', 'amplitude direction is not four times H minus one', lambda: verify_direction(H, [True]+z[1:]))
    expect('numeric-six-parent-query', 'numeric q6 or q7 probability lookup forbidden', lambda: lookup(held, P6, 0, 0))
    expect('numeric-seven-parent-query', 'numeric q6 or q7 probability lookup forbidden', lambda: lookup(held, P7, 0, 0))
    expect('C5-query-refusal', 'order outside frozen exact structural domain', lambda: lookup(held, (0, 1, 3, 7, 15), 0, 0))
    expect('nested-unhashable-order', 'order outside frozen exact structural domain', lambda: lookup(held, (0, [1], 3), 0, 0))
    expect('extra-record-query', 'record outside the two frozen exact markings', lambda: lookup(held, C3, 2, 0))
    for name in ('rho', 'epsilon', 's', 'a6', 'a7', 'M6', 'M7', 'q6', 'q7'):
        expect('no-actual-'+name, 'numeric actual scale or future row forbidden', lambda name=name: forbidden_global(name))
    expect('full-top-ideal-not-proper', 'symbolic deletion requires a declared proper ideal', lambda: induced(P7, 8, 0, 127))
    expect('delete-nonmaximal-vertex', 'deletion is not a subset of omitted maxima', lambda: induced(P7, 1, 0, 7))
    expect('bool-deletion-mask', 'invalid exact omitted-maxima deletion', lambda: induced(P7, True, 0, 7))
    expect('bool-symbolic-precursor', 'invalid exact symbolic precursor', lambda: induced(P7, 8, 0, False))
    item = witness['records'][0]
    lower, total, lower_rows = reconstruct_p6(held, 0)
    expect('wrong-independent-E', 'lower E differs from complete independent deletion sum',
           lambda: verify_lower_rows(held, 0, lower_rows, total+1))
    expect('missing-lower-slot', 'certificate list coverage mismatch', lambda: verify_lower_rows(held, 0, lower_rows[:-1], total))
    expect('wrong-lower-factor-exponent', 'lower held-factor provenance or labeled multiplicity changed',
           lambda: verify_lower_rows(held, 0, altered(lower_rows, [0, 'factors', 0, 'exponent'], 0), total))
    slots = item['top_proper_slots']
    expect('missing-top-slot', 'top proper-slot list coverage changed', lambda: verify_top_rows(held, z, 0, lower, total, slots[:-1]))
    expect('duplicate-top-slot', 'top labeled factors transport multipliers or multiplicity changed',
           lambda: verify_top_rows(held, z, 0, lower, total, altered(slots, [1, 'ideal'], 0)))
    expect('collapsed-labeled-slot-weight', 'top labeled factors transport multipliers or multiplicity changed',
           lambda: verify_top_rows(held, z, 0, lower, total,
                                   altered(slots, [0, 'baseline_potential'], encode(scale(decode(slots[0]['baseline_potential']), Q(4))))))
    expect('wrong-transported-record', 'top labeled factors transport multipliers or multiplicity changed',
           lambda: verify_top_rows(held, z, 0, lower, total, altered(slots, [0, 'factors', 0, 'raw_record'], 1)))
    expect('wrong-proper-locality-record', 'lower held-factor provenance or labeled multiplicity changed',
           lambda: verify_lower_rows(held, 0, altered(lower_rows, [0, 'factors', 0, 'source', 'query_record'], 1), total))
    expect('missing-singleton-amplitude', 'top slot lost its prescribed amplitude polynomial',
           lambda: verify_top_rows(held, z, 0, lower, total, altered(slots, [3, 'multiplier'], encode(ONE))))
    expect('wrong-amplitude-individual-power', 'top labeled factors transport multipliers or multiplicity changed',
           lambda: verify_top_rows(held, z, 0, lower, total, altered(slots, [3, 'multiplier_power'], 1)))
    full_index = next(i for i, row in enumerate(slots) if row['included_caps'] == 3)
    expect('modified-symbolic-full-complement', 'three-cap full complement was modified',
           lambda: verify_top_rows(held, z, 0, lower, total, altered(slots, [full_index, 'changed_potential'], encode(ONE))))
    expect('zero-deletion-exponent', 'deletion exponent is not exact alternating sign',
           lambda: sparse_product(altered(slots[0]['factors'], [0, 'exponent'], 0)))
    expect('invert-amplitude-binomial', 'nonmonomial symbolic denominator forbidden',
           lambda: sparse_product([dict(exponent=-1, baseline_factor=encode(add(ONE, monomial(0, 1))))]))
    expect('invert-full-complement-binomial', 'nonmonomial symbolic denominator forbidden',
           lambda: sparse_product([dict(exponent=-1, baseline_factor=encode(subtract(ONE, monomial(1, 0))))]))
    expect('surviving-negative-Laurent-power', 'top Laurent product escaped nonnegative bidegree four',
           lambda: sparse_product([dict(exponent=-1, baseline_factor=encode(monomial(1, 0)))]))
    expect('bool-polynomial-power', 'bivariate exact powers coefficients or global degree changed', lambda: poly({(True, 0): Q(1)}))
    expect('bool-polynomial-coefficient', 'bivariate exact powers coefficients or global degree changed', lambda: poly({(0, 0): True}))
    expect('polynomial-global-bidegree-expansion', 'bivariate exact powers coefficients or global degree changed', lambda: poly({(9, 0): Q(1)}))
    expect('polynomial-duplicate-power', 'duplicate serialized polynomial power', lambda: decode([[0, 0, '1'], [0, 0, '2']]))
    expect('polynomial-explicit-zero', 'serialized polynomial powers are not canonical', lambda: decode([[0, 0, '0']]))
    expect('raw-epsilon-zero-coefficient', 'raw polynomial lacks exact epsilon times rho squared factor', lambda: divide_fixed(monomial(2, 0), 2))
    expect('raw-rho-zero-coefficient', 'raw polynomial lacks exact epsilon times rho squared factor', lambda: divide_fixed(monomial(0, 1), 2))
    expect('raw-rho-one-coefficient', 'raw polynomial lacks exact epsilon times rho squared factor', lambda: divide_fixed(monomial(1, 1), 2))
    expect('raw-D-rho-degree-expansion', 'polynomial exceeds prescribed bidegree', lambda: divide_fixed(monomial(5, 1), 2))
    expect('divided-A-degree-expansion', 'polynomial exceeds prescribed bidegree', lambda: tensor(monomial(3, 0), Q(1), AMPLITUDE, (2, 3)))
    expect('divided-G-amplitude-degree-expansion', 'polynomial exceeds prescribed bidegree', lambda: tensor(monomial(0, 4), Q(1), AMPLITUDE, (6, 3)))
    sums, bound = [rational(q) for q in witness['scale_domain']['selected_E']], rational(witness['scale_domain']['R'])
    expect('selected-bound-as-half', 'selected-row outer rho bound changed or became an actual scale', lambda: verify_upper_bound(sums, Q(1, 2), AMPLITUDE))
    expect('changed-amplitude-ceiling', 'fixed amplitude ceiling changed', lambda: verify_upper_bound(sums, bound, Q(1)))
    expect('zero-tensor-radius', 'tensor rho bound must be exact positive rational', lambda: tensor(ZERO, Q(0), AMPLITUDE, (2, 3)))
    expect('adaptive-tensor-degree', 'predeclared tensor degree or axis order changed', lambda: tensor(ZERO, Q(1), AMPLITUDE, (3, 3)))
    expect('bool-tensor-degree', 'predeclared tensor degree or axis order changed', lambda: tensor(ZERO, Q(1), AMPLITUDE, (True, 3)))

    fixtures = synthetic_fixtures()
    unequal = fixtures['unequal-axis-scaling']
    value, evidence = decode(unequal['polynomial']), unequal['tensor_evidence']
    def bad_tensor(name, path, replacement, reason='fixed tensor evidence reconstruction mismatch'):
        expect(name, reason, lambda: verify_tensor(value, Q(1), AMPLITUDE, (2, 3), altered(evidence, path, replacement)))
    bad_tensor('transposed-tensor-axis-order', ['axis_order'], ['epsilon', 'rho'], 'tensor axis order changed')
    bad_tensor('changed-fixed-tensor-degree', ['basis_degree'], [6, 3], 'predeclared tensor degree or axis order changed')
    bad_tensor('missing-tensor-row', ['bernstein'], evidence['bernstein'][:-1], 'tensor grid lost complete padded dimensions')
    bad_tensor('missing-tensor-column', ['bernstein', 0], evidence['bernstein'][0][:-1], 'tensor grid lost complete padded dimensions')
    bad_tensor('extra-tensor-column', ['bernstein', 0], evidence['bernstein'][0]+['0'], 'tensor grid lost complete padded dimensions')
    bad_tensor('bool-tensor-coordinate', ['bernstein', 0, 0], True, 'noncanonical rational encoding')
    bad_tensor('altered-tensor-coordinate', ['bernstein', 0, 0], '1', 'retained tensor coordinates fail independent reverse identity')
    bad_tensor('wrong-amplitude-scaled-power', ['scaled_power', 2, 1], '1')
    bad_tensor('wrong-reverse-sign', ['reverse_scaled_power', 2, 1], '-1/4')
    bad_tensor('scaled-is-not-original-grid', ['reverse_original_power'], evidence['reverse_scaled_power'])
    bad_tensor('omitted-zero-padding', ['padded_power', 0], [], 'certificate list coverage mismatch')
    bad_tensor('wrong-upper-edge-identity', ['edges', 'epsilon_upper', 0], '1')
    bad_tensor('wrong-included-corner', ['included_corner'], '0')
    expect('missing-second-G-sign-grid', 'sign test requires A and both G grids',
           lambda: sign_summary({k: v for k, v in fixtures['positive']['tensor_evidence'].items() if k != 'G1'}))
    for name in FIXTURE_NAMES[:-1]:
        item = fixtures[name]
        expect('false-sign-'+name, 'positive-only sign summary or ordered failing indices changed',
               lambda item=item: verify_sign_summary(item['tensor_evidence'],
                                                     altered(item['sign_summary'], ['sufficient_positive'], not item['expected_positive'])))
    mixed = fixtures['positive-mixed-amplitude-basis']
    failures = mixed['sign_summary']['negative_coefficients']
    require(len(failures) > 1, 'synthetic ordered-negative list lacks its fixed multiplicity')
    expect('missing-ordered-failure', 'certificate list coverage mismatch',
           lambda: verify_sign_summary(mixed['tensor_evidence'], altered(mixed['sign_summary'], ['negative_coefficients'], failures[:-1])))
    expect('reordered-failure-indices', 'positive-only sign summary or ordered failing indices changed',
           lambda: verify_sign_summary(mixed['tensor_evidence'], altered(mixed['sign_summary'], ['negative_coefficients'], list(reversed(failures)))))
    expect('wrong-failure-value', 'positive-only sign summary or ordered failing indices changed',
           lambda: verify_sign_summary(mixed['tensor_evidence'], altered(mixed['sign_summary'], ['negative_coefficients', 0, 'coefficient'], '-1')))
    expect('bool-failure-index', 'certificate exact value type mismatch',
           lambda: verify_sign_summary(mixed['tensor_evidence'], altered(mixed['sign_summary'], ['negative_coefficients', 0, 'rho_index'], False)))

    expect('wrong-ri91-source', 'accepted RI91 source provenance changed',
           lambda: extract_regression(altered(regression, ['checker_sha256'], '0'*64), bound))
    expect('wrong-ri91-input-provenance', 'accepted RI91 construction input provenance changed',
           lambda: extract_regression(altered(regression, ['accepted_input', 'sha256'], '0'*64), bound))
    expect('wrong-ri91-parent', 'accepted RI91 parent or record scope changed',
           lambda: extract_regression(altered(regression, ['selected_parent'], list(P6)), bound))
    expect('bool-ri91-record', 'accepted RI91 parent or record scope changed',
           lambda: extract_regression(altered(regression, ['records', 0, 'record'], False), bound))
    expect('wrong-ri91-radius', 'accepted RI91 outer radius changed',
           lambda: extract_regression(altered(regression, ['scale_domain', 'R'], '1'), bound))
    expect('wrong-ri91-degree', 'accepted RI91 fixed degree factor or radius changed',
           lambda: extract_regression(altered(regression, ['decision', 'bernstein_evidence', 'A', 'basis_degree'], 6), bound))
    anchor_a = regression['decision']['bernstein_evidence']['A']['bernstein']
    expect('missing-ri91-anchor-entry', 'accepted seventeen-coordinate coverage changed',
           lambda: extract_regression(altered(regression, ['decision', 'bernstein_evidence', 'A', 'bernstein'], anchor_a[:-1]), bound))
    expect('zero-ri91-anchor', 'accepted endpoint anchor is not strictly positive',
           lambda: extract_regression(altered(regression, ['decision', 'bernstein_evidence', 'A', 'bernstein', 0], '0'), bound))
    expect('wrong-endpoint-factor-four', 'endpoint regression requires exact factor four',
           lambda: verify_anchor(witness['tensor_evidence'], reference, Q(1)))
    wrong_reference = {name: list(values) for name, values in reference.items()}
    wrong_reference['A'][0] += 1
    expect('anchor-positivity-without-equality', 'amplitude endpoint does not equal four times accepted RI91 anchor',
           lambda: verify_anchor(witness['tensor_evidence'], wrong_reference))

    saved('wrong-new-schema', ['schema'], 'wrong-schema', 'certificate schema mismatch')
    expect('extra-new-certificate-field', 'certificate object fields mismatch', lambda: verify_certificate(dict(witness, extra=None), witness))
    expect('missing-new-certificate-field', 'certificate object fields mismatch',
           lambda: verify_certificate({k: v for k, v in witness.items() if k != 'inputs'}, witness))
    expect('noncanonical-saved-serialization', 'saved certificate is not exact canonical bytes with one newline',
           lambda: verify_saved_bytes((canonical(witness)+'\n\n').encode(), witness))
    saved('bool-new-record', ['records', 0, 'record'], False, 'certificate exact value type mismatch')
    saved('missing-retained-input-row', ['inputs', 'held_rows'], witness['inputs']['held_rows'][:-1], 'certificate list coverage mismatch')
    saved('wrong-raw-divisor-rho', ['cross_multiplication', 'fixed_raw_divisor', 'rho_power'], 1)
    saved('wrong-raw-divisor-epsilon', ['cross_multiplication', 'fixed_raw_divisor', 'epsilon_power'], 0)
    saved('forged-raw-zero-coordinate', ['fixed_division_evidence', 'D0', 'forbidden_zero_coordinates', 0, 2], '1')
    saved('wrong-full-complement-s-endpoint', ['full_complement_s_endpoints', 0, 'divided_residual'], encode(ONE),
          'certificate list coverage mismatch')
    saved('full-complement-endpoint-is-not-actual-s', ['full_complement_s_endpoints', 1, 'numerical_s_selected'], True)
    saved('claim-native-negative-branch', ['decision', 'disposition'], 'certified-negative-amplitude-obstruction')
    saved('claim-native-blind-branch', ['decision', 'disposition'], 'identically-zero-pair')
    saved('claim-native-root-branch', ['decision', 'disposition'], 'outer-boundary-root-unresolved')
    saved('claim-numeric-actual-scale', ['scale_domain', 'actual_scales_selected'], True)
    saved('claim-selector-acceptance', ['decision', 'selector_acceptance_claimed'], True)
    saved('claim-independent-regression', ['limitations', 'regression_replay_is_not_independent_derivation'], False)
    require(tuple(passed) == REFUSAL_NAMES and len(passed) == len(set(passed)) == 134,
            'frozen ordered intended-reason refusal inventory changed')
    return dict(intended_reason_refusals=passed, synthetic_algebra_fixtures=fixtures,
                fixed_fixture_names=list(FIXTURE_NAMES), synthetic_fixtures_are_native_models=False,
                extra_native_inputs_used=False)


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'only --witness or default saved-certificate mode is permitted')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, lambda _number, _frame: (_ for _ in ()).throw(RuntimeError('120-second envelope exceeded')))
    signal.alarm(MAX_SECONDS)
    source = Path(__file__).resolve()
    source_bytes = source.read_bytes()
    source_hash = sha256(source_bytes).hexdigest()
    paths = {'ri88': source.parent.parent/'native_growth_four_vertex_cap_check_v1'/'CERTIFICATE.json',
             'ri91': source.parent.parent/'native_growth_relative_obstruction_v1'/'CERTIFICATE.json'}
    raw_inputs = {role: path.read_bytes() for role, path in paths.items()}
    for role in ('ri88', 'ri91'):
        verify_input_bytes(role, raw_inputs[role])  # Both full pins precede JSON parsing and extraction.
    data, regression = load_json(raw_inputs['ri88']), load_json(raw_inputs['ri91'])
    budget('both accepted certificates pinned; no helper or prefix imports')
    witness, held, H, z, reference = build_witness(data, regression)
    witness['checker_sha256'] = source_hash
    witness['refusal_controls'] = refusal_controls(witness, raw_inputs, data, regression, held, H, z, reference)
    budget('fixed bivariate constructions fixtures and intended-reason controls completed')
    certificate_hash = None
    if not sys.argv[1:]:
        path = source.with_name('CERTIFICATE.json')
        raw_certificate = path.read_bytes()
        verify_saved_bytes(raw_certificate, witness)
        certificate_hash = sha256(raw_certificate).hexdigest()
        require(path.read_bytes() == raw_certificate, 'saved certificate changed during verification')
    for role, path in paths.items():
        verify_input_bytes(role, path.read_bytes())
    require(source.read_bytes() == source_bytes, 'checker source changed during verification')
    budget()
    try:
        if sys.argv[1:]:
            print(canonical(witness), flush=True)
        else:
            result = dict(status='PASS', checker_sha256=source_hash, certificate_sha256=certificate_hash,
                          accepted_inputs_sha256={role: pin for role, (_, pin) in INPUT_PINS.items()}, witness_sha256=digest(witness),
                          disposition=witness['decision']['disposition'], coverage=witness['coverage'],
                          actual_scales_or_future_probabilities_computed=False,
                          refusal_count=len(witness['refusal_controls']['intended_reason_refusals']), fixture_count=12,
                          refusal_controls=witness['refusal_controls']['intended_reason_refusals'])
            print(canonical(result), flush=True)
        budget()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
