#!/usr/bin/env python3
"""RI120 complete connected sensitivity. SOURCE ONLY, NOT EXECUTED.

Literal arithmetic-source predecessor: RI112 check.py, 1101 lines/57049 bytes,
SHA256 73b204ba8acdefed418aa803ea95c0fc0dddba7c436ea1595996a01002f9287d.
Fraction operations, dense division and unrescaled Sturm engines are copied
without imports from that source. Native operands are exactly 40 held rows/
224 slots; no H/z, new law query, scale choice or remaining-parent solver.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import re
import resource
import signal
import sys
import time

SCHEMA = 'ri120-connected-sensitivity-certificate-v1'
PINS = {
    'ri88': (1828149, 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    'ri111': (20656, 'ca07943f8d2f9d9c396b4484193dc5797900f6c7a18c5f8c2a5b8333759ccf53'),
    'ri109_adjudication': (4849, '26ddd81d5fc1ae80c30d68aeadcb0ada0e18168bf3892b0995643294e6a64ddf'),
    'ri111_adjudication': (3838, 'fc4e9147db50ceb750d1f9fdcf503ffbb53363d2f1379557d1713bb844093249'),
    'ri115_adjudication': (6678, 'a23c0ac1208c78cc28590727675869968e2f579c863857aad67a9ea08b1d2480'),
    'ri117': (15564, '9726383aabb01cfa922b90f64bd572ac0a04a390111f57e722ed29d896289194'),
    'ri117_connected': (11893, 'ede2d82067a4259266d61988e0897756507e06b28040d8d5bd324991aa79dad0'),
    'ri117_adjudication': (4617, '862545fde8a9006dd39593c0aca7f47d6d82426dc47ffccea140e6f64957aec3'),
}
INPUT_ROLES = ('ri88', 'ri111', 'ri109_adjudication', 'ri111_adjudication',
               'ri115_adjudication', 'ri117', 'ri117_connected', 'ri117_adjudication')
ADJUDICATION_ROLES = ('ri109_adjudication', 'ri111_adjudication',
                      'ri115_adjudication', 'ri117_adjudication')
RI88_KEYS = {
    'admission', 'checker_sha256', 'compact_rows', 'coverage', 'dependencies',
    'design_sha256', 'domain', 'exact_decision', 'expanded_rows', 'held_rows',
    'parameters', 'prefix', 'refusal_controls', 'schema', 'structure',
    'transported_audit', 'width_target',
}
DEPENDENCIES = {
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
}
C3, C4, C5, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 7)
HELD = (C3, C4, C5, H5)
IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 31),
          (0, 1, 3, 7, 15, 23, 31))
RECORDS = tuple(range(8))
RECORD_DOMAIN = {C3: RECORDS, C4: RECORDS, C5: tuple(range(16)), H5: RECORDS}
MAX_SECONDS, MAX_BYTES = 120, 536870912
INPUT_BITS, MAX_BITS, MAX_OPS = 32768, 1048576, 200000
MAX_TEXT, MAX_OUTPUT = 20000, 8388608
START = None
OPS = 0


class Refusal(RuntimeError):
    pass


def require(condition, reason):
    if not condition:
        raise Refusal(reason)


def budget():
    require(START is None or time.monotonic()-START <= MAX_SECONDS, 'wall-budget')
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((rss if sys.platform == 'darwin' else rss*1024) <= MAX_BYTES, 'rss-budget')


def tick():
    global OPS
    OPS += 1
    require(OPS <= MAX_OPS, 'operation-budget')
    budget()


def bounded(q, bits=MAX_BITS):
    require(type(q) is Q, 'exact-rational-required')
    require(max(abs(q.numerator).bit_length(), q.denominator.bit_length()) <= bits,
            'integer-bit-budget')
    return q


def calc(op, left, right=Q(0)):
    """Count rational arithmetic and ordered comparisons; equality is structural."""
    tick()
    bounded(left)
    bounded(right)
    if op == 'add':
        result = left+right
    elif op == 'sub':
        result = left-right
    elif op == 'mul':
        result = left*right
    elif op == 'div':
        require(right != 0, 'zero-rational-divisor')
        result = left/right
    elif op == 'cmp':
        return (left > right)-(left < right)
    else:
        raise Refusal('unknown-arithmetic-operation')
    return bounded(result)


def add(a, b):
    return calc('add', a, b)


def sub(a, b):
    return calc('sub', a, b)


def mul(a, b):
    return calc('mul', a, b)


def div(a, b):
    return calc('div', a, b)


def sign(a):
    return calc('cmp', a)


def power(a, exponent):
    require(type(exponent) is int and 0 <= exponent <= 8, 'power-domain')
    result = Q(1)
    for _ in range(exponent):
        result = mul(result, a)
    return result


def total(values):
    result = Q(0)
    for value in values:
        result = add(result, value)
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def load_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate-json-key')
            result[key] = value
        return result
    def forbidden(_value):
        raise Refusal('noninteger-json-number')
    def integer(text):
        require(len(text) <= MAX_TEXT, 'json-integer-text-budget')
        return int(text)
    return json.loads(raw, object_pairs_hook=pairs, parse_int=integer,
                      parse_float=forbidden, parse_constant=forbidden)


def clone(value):
    return load_json(canonical(value))


def rational(text):
    require(type(text) is str, 'noncanonical-rational')
    require(len(text) <= MAX_TEXT, 'rational-text-budget')
    require(re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', text) is not None,
            'noncanonical-rational')
    value = Q(text)
    require(str(value) == text, 'noncanonical-rational')
    return bounded(value, INPUT_BITS)


def input_bytes(role, raw):
    require(type(role) is str and role in PINS, 'input-role')
    require(type(raw) is bytes and len(raw) == PINS[role][0], 'input-size-'+role)
    require(sha256(raw).hexdigest() == PINS[role][1], 'input-hash-'+role)


def adjudication(role, data):
    require(type(role) is str and role in ADJUDICATION_ROLES, 'adjudication-role')
    expected = {
        'ri109_adjudication': ('ri109-root-final-mathematical-adjudication-v1',
                              'ACCEPT_INDEPENDENT_RESTRICTED_27_CHILD_REPAIR_OBSTRUCTION'),
        'ri111_adjudication': ('ri111-root-analytic-adjudication-v1',
                              'ACCEPT_CONDITIONAL_COMPLETE_28_CHILD_REDUCTION_ONLY'),
        'ri115_adjudication': ('ri115-root-final-native-mathematical-adjudication-v1',
                              'ACCEPT_EXACT_ZERO_MINOR_RESULT_WITH_FEASIBILITY_OPEN'),
        'ri117_adjudication': ('ri117-root-coupled-family-adjudication-v1',
                              'ACCEPT_COMPLETE_CONDITIONAL_COUPLED_REDUCTION_ONLY'),
    }
    schema, status = expected[role]
    require(type(data) is dict and data.get('schema') == schema and data.get('status') == status,
            'adjudication-status-'+role)
    if role == 'ri111_adjudication':
        require(data.get('actual_28_child_feasibility') == 'UNRESOLVED'
                and data.get('new_native_coefficients_or_scales_evaluated') is False
                and data.get('new_numerical_execution_admitted') is False,
                'adjudication-scope-ri111')
    if role == 'ri115_adjudication':
        require(data.get('mathematical_result_accepted') is True
                and data.get('whole_positive_extension_established') is False,
                'adjudication-scope-ri115')
    if role == 'ri117_adjudication':
        require(data.get('active_execution_admission') is False
                and data.get('fixed_28_child_repair_rejected') is False
                and data.get('full_positive_repair_proved') is False,
                'adjudication-scope-ri117')


def provenance(data):
    require(type(data) is dict and set(data) == RI88_KEYS, 'ri88-fields')
    require(data['schema'] == 'ri88-four-vertex-cap-v1'
            and data['checker_sha256'] == '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
            and data['design_sha256'] == 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a',
            'ri88-source')
    require(type(data['dependencies']) is dict
            and canonical(data['dependencies']) == canonical(DEPENDENCIES), 'ri88-dependencies')
    admission = data['admission']
    require(type(admission) is dict and admission.get('epsilon') == '1/4'
            and admission.get('later_h_prescribed') is False
            and admission.get('numerical_a6_evaluated') is False, 'ri88-admission')
    require(type(data['exact_decision']) is dict
            and data['exact_decision'].get('disposition') == 'positive-finite-width-bias',
            'ri88-disposition')
    prefix = data['prefix']
    require(type(prefix) is dict
            and prefix.get('problem_sha256') == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and prefix.get('actual_probability_manifest_sha256') == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and type(prefix.get('canonical_lex_stages')) is int
            and prefix['canonical_lex_stages'] == 69, 'ri88-actual-prefix')
    coverage = data['coverage']
    require(type(coverage) is dict and type(coverage.get('held_marked_rows')) is int
            and coverage['held_marked_rows'] == 40
            and type(coverage.get('held_probability_slots')) is int
            and coverage['held_probability_slots'] == 224, 'ri88-coverage')


def held_entry(entry):
    require(type(entry) is dict and set(entry) == {'order', 'record', 'probabilities'},
            'held-fields')
    require(type(entry['order']) is list and all(type(x) is int for x in entry['order']),
            'held-order-types')
    order = tuple(entry['order'])
    require(order in HELD, 'held-order-domain')
    require(type(entry['record']) is int and entry['record'] in RECORD_DOMAIN[order],
            'held-record-domain')
    pairs = entry['probabilities']
    require(type(pairs) is list and all(type(p) is list and len(p) == 2
            and type(p[0]) is int for p in pairs), 'held-slot-types')
    require([p[0] for p in pairs] == list(IDEALS[HELD.index(order)]), 'held-slot-inventory')
    row = {part: rational(q) for part, q in pairs}
    require(all(sign(q) > 0 for q in row.values()) and total(row.values()) == 1,
            'held-positive-normalized')
    return row


def extract(data):
    provenance(data)
    require(type(data['held_rows']) is list and len(data['held_rows']) == 40, 'held-row-inventory')
    held, selected = {}, {}
    for entry in data['held_rows']:
        row = held_entry(entry)
        key = (tuple(entry['order']), entry['record'])
        require(key not in selected, 'duplicate-selected-row')
        selected[key] = entry
        held[key] = row
    keys = [(order, record) for order in HELD for record in RECORD_DOMAIN[order]]
    require(set(selected) == set(keys), 'selected-row-completeness')
    require(list(selected) == keys, 'selected-row-order')
    for order in HELD:
        records = RECORD_DOMAIN[order]
        require(all(held[(order, r)][0] == held[(order, 0)][0] for r in records),
                'held-empty-locality')
        for part in IDEALS[HELD.index(order)][:-1]:
            for r in records:
                for other in records:
                    if r & part == other & part:
                        require(held[(order, r)][part] == held[(order, other)][part],
                                'held-proper-locality')
    for record in RECORDS:
        require(held[(H5, record)][15] == held[(H5, record)][23], 'held-twin-symmetry')
    for record in RECORDS:
        lhs = mul(held[(C4, record)][7], held[(H5, record)][15])
        for sigma in (0, 1):
            rhs = mul(held[(C4, record)][15], held[(C5, record+8*sigma)][7])
            require(lhs == rhs, 'held-twin-diamond')
    return held, [selected[key] for key in keys]


def lookup(held, order, record, part):
    require(type(order) is tuple and all(type(x) is int for x in order)
            and order in HELD, 'lookup-order-domain')
    require(type(record) is int and record in RECORD_DOMAIN[order], 'lookup-record-domain')
    require(type(part) is int and part in IDEALS[HELD.index(order)], 'lookup-slot-domain')
    return held[(order, record)][part]


def poly(coefficients):
    require(type(coefficients) is list and len(coefficients) <= 5, 'polynomial-shape-degree')
    for q in coefficients:
        bounded(q)
    result = list(coefficients)
    while result and result[-1] == 0:
        result.pop()
    return result


def enc(coefficients):
    return [str(q) for q in poly(coefficients)]


def derivative(p):
    p = poly(p)
    return poly([mul(Q(i), p[i]) for i in range(1, len(p))])


def product(a, b):
    a, b = poly(a), poly(b)
    if not a or not b:
        return []
    require(len(a)+len(b)-1 <= 5, 'polynomial-product-degree')
    result = [Q(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] = add(result[i+j], mul(x, y))
    return poly(result)


def padd(a, b):
    a, b = poly(a), poly(b)
    return poly([add(a[i] if i < len(a) else Q(0), b[i] if i < len(b) else Q(0))
                 for i in range(max(len(a), len(b)))])


def divide(a, b):
    a, b = poly(a), poly(b)
    require(bool(b), 'zero-polynomial-divisor')
    r = list(a)
    q = [Q(0)]*max(0, len(a)-len(b)+1)
    steps = 0
    while r and len(r) >= len(b):
        steps += 1
        require(steps <= 5, 'division-step-budget')
        previous = len(r)
        shift = len(r)-len(b)
        factor = div(r[-1], b[-1])
        q[shift] = add(q[shift], factor)
        for i, coefficient in enumerate(b):
            r[i+shift] = sub(r[i+shift], mul(factor, coefficient))
        r = poly(r)
        require(len(r) < previous, 'division-degree-drop')
    q = poly(q)
    require(padd(product(b, q), r) == a, 'division-identity')
    return q, r


def euclidean(a, b):
    a, b = poly(a), poly(b)
    require(bool(a), 'zero-gcd-input')
    trace = []
    while b:
        require(len(trace) < 4, 'gcd-step-budget')
        quotient, remainder = divide(a, b)
        trace.append(dict(dividend=enc(a), divisor=enc(b), quotient=enc(quotient),
                          remainder=enc(remainder)))
        a, b = b, remainder
    monic = [div(c, a[-1]) for c in a]
    return monic, trace


def evaluate(p, x):
    bounded(x)
    result = Q(0)
    for q in reversed(poly(p)):
        result = add(mul(result, x), q)
    return result


def endpoint(chain, x):
    values = [evaluate(p, x) for p in chain]
    signs = [sign(q) for q in values]
    nonzero = [q for q in signs if q]
    variations = sum(a != b for a, b in zip(nonzero, nonzero[1:]))
    return dict(x=str(x), values=[str(q) for q in values], signs=signs,
                nonzero_signs=nonzero, variations=variations)


def root_certificate(p, radius):
    p = poly(p)
    require(bool(p) and len(p) <= 4, 'root-polynomial-domain')
    require(type(radius) is Q and sign(radius) > 0, 'root-radius-domain')
    gcd, gcd_steps = euclidean(p, derivative(p))
    square_free, square_free_remainder = divide(p, gcd)
    require(not square_free_remainder and product(gcd, square_free) == p, 'square-free-division')
    coprime, coprime_steps = euclidean(square_free, derivative(square_free))
    require(coprime == [Q(1)], 'square-free-coprimality')
    chain = [square_free]
    deriv = derivative(square_free)
    if deriv:
        chain.append(deriv)
    sturm_steps = []
    while len(chain) > 1:
        require(len(sturm_steps) < 3, 'sturm-step-budget')
        quotient, remainder = divide(chain[-2], chain[-1])
        next_term = [sub(Q(0), q) for q in remainder]
        sturm_steps.append(dict(dividend=enc(chain[-2]), divisor=enc(chain[-1]),
                                quotient=enc(quotient), remainder=enc(remainder),
                                next_term=enc(next_term)))
        if not next_term:
            break
        require(len(next_term) < len(chain[-1]), 'sturm-degree-drop')
        chain.append(next_term)
    require(len(chain[-1]) == 1 and len(chain) <= 4, 'sturm-terminal-constant')
    lower, upper = endpoint(chain, Q(0)), endpoint(chain, radius)
    count = lower['variations']-upper['variations']
    require(type(count) is int and 0 <= count <= len(square_free)-1, 'root-count-range')
    return dict(polynomial=enc(p), interval='(0,R]', R=str(radius),
                derivative=enc(derivative(p)), gcd_euclidean=gcd_steps, gcd_monic=enc(gcd),
                square_free=enc(square_free), square_free_quotient=enc(square_free),
                square_free_remainder=enc(square_free_remainder),
                reconstructed_polynomial=enc(product(gcd, square_free)),
                coprime_euclidean=coprime_steps, coprime_gcd=enc(coprime),
                sturm_chain=[enc(q) for q in chain], sturm_divisions=sturm_steps,
                lower=lower, upper=upper, distinct_real_roots=count,
                lower_excluded=True, upper_included=True,
                rational_root_decision_performed=False, actual_scale_evaluated=False)


def stem_formula(held, record):
    slots = (0, 1, 3, 7)
    A = [lookup(held, C3, record, part) for part in slots]
    B = [lookup(held, C4, record, part) for part in slots]
    G = [lookup(held, H5, record, part) for part in slots]
    c = lookup(held, C4, record, 15)
    h = lookup(held, H5, record, 15)
    j = lookup(held, H5, record, 31)
    terms = [div(mul(a, power(g, 3)), power(b, 3)) for a, b, g in zip(A, B, G)]
    m = div(power(h, 2), c)
    E = total(terms+[mul(Q(3), m), mul(Q(3), j)])
    V = sub(sub(E, m), mul(Q(2), j))
    U3 = [Q(2), sub(Q(-1), V), V]
    evidence = dict(record=record, E_terms=[str(q) for q in terms], c=str(c), h=str(h),
                    j=str(j), m=str(m), E=str(E), V=str(V),
                    U3_padded=[str(q) for q in U3])
    return (E, V), evidence


def connected_formula(held, record, stem):
    xi = record & 7
    slots = (0, 1, 3, 7)
    A = [lookup(held, C3, xi, part) for part in slots]
    B = [lookup(held, C4, xi, part) for part in slots]
    G = [lookup(held, H5, xi, part) for part in slots]
    D = [lookup(held, C5, record, part) for part in slots]
    c = lookup(held, C4, xi, 15)
    h = lookup(held, H5, xi, 15)
    j = lookup(held, H5, xi, 31)
    e = lookup(held, C5, record, 15)
    ell = lookup(held, C5, record, 31)
    m = div(power(h, 2), c)
    e2_terms = [div(mul(d, g), b) for d, g, b in zip(D, G, B)]
    e2_terms += [div(mul(e, h), c), h, j, ell]
    c2_terms = [div(mul(mul(a, power(g, 3)), d), power(b, 4))
                for a, g, d, b in zip(A, G, D, B)]
    c2_terms += [div(mul(e, power(h, 2)), power(c, 2))]
    E2, C2 = total(e2_terms), total(c2_terms)
    A2 = sub(add(stem[xi][0], mul(Q(2), E2)), j)
    B2 = total([mul(Q(2), m), mul(Q(2), j), ell])
    U2 = [Q(3), sub(Q(0), A2), B2, C2]
    evidence = dict(record=record, stem_record=xi, sigma=record >> 3, e=str(e), ell=str(ell),
                    E2_terms=[str(q) for q in e2_terms], E2=str(E2),
                    C2_terms=[str(q) for q in c2_terms], C2=str(C2),
                    A2=str(A2), B2=str(B2), U2_padded=[str(q) for q in U2])
    return (A2, B2, C2), U2, evidence


def sensitivity_contrasts(stem, coeffs, U, radius):
    require(type(stem) is list and len(stem) == 8 and all(type(row) is tuple and len(row) == 2
            and all(type(q) is Q for q in row) for row in stem), 'stem-profile-domain')
    require(type(coeffs) is list and len(coeffs) == 16 and all(type(row) is tuple and len(row) == 3
            and all(type(q) is Q for q in row) for row in coeffs), 'connected-coefficient-domain')
    require(type(U) is list and len(U) == 16 and all(type(row) is list and len(row) == 4
            and all(type(q) is Q for q in row) for row in U), 'connected-U-domain')
    require(type(radius) is Q and radius == radius_for([stem[0][0], stem[1][0]]), 'fixed-radius')
    deltas, v_evidence = [], []
    for record in range(1, 8):
        delta = sub(stem[record][1], stem[0][1])
        deltas.append(delta)
        v_evidence.append(dict(record=record, V=str(stem[record][1]), V0=str(stem[0][1]),
                               delta_V=str(delta), is_zero=delta == 0))
    family, q_evidence = [], []
    for record in range(1, 16):
        delta = [sub(b, a) for a, b in zip(coeffs[0], coeffs[record])]
        q2 = [sub(Q(0), delta[0]), delta[1], delta[2]]
        raw = [sub(b, a) for a, b in zip(U[0], U[record])]
        require(raw == [Q(0)]+q2, 'Q2-fixed-division')
        family.append(dict(record=record, polynomial=q2))
        q_evidence.append(dict(record=record, delta_A2=str(delta[0]), delta_B2=str(delta[1]),
                               delta_C2=str(delta[2]), Q2_padded=[str(q) for q in q2],
                               U2_difference_padded=[str(q) for q in raw], fixed_divisor='rho',
                               quotient_matches_closed_formula=True,
                               degree=len(poly(q2))-1, is_zero=not poly(q2)))
    return deltas, v_evidence, family, q_evidence


def radius_for(E):
    require(type(E) is list and len(E) == 2 and all(type(q) is Q and sign(q) > 0 for q in E),
            'radius-E-domain')
    maximum = E[0] if calc('cmp', E[0], E[1]) >= 0 else E[1]
    return div(Q(1), mul(Q(2), add(Q(1), maximum)))


def common_gcd(family, radius):
    require(type(family) is list and len(family) == 15, 'Q2-family-count')
    require(all(type(row) is dict and set(row) == {'record', 'polynomial'} for row in family),
            'Q2-family-fields')
    require(all(type(row['record']) is int for row in family), 'Q2-family-label-types')
    labels = [row['record'] for row in family]
    require(set(labels) == set(range(1, 16)), 'Q2-family-label-inventory')
    require(labels == list(range(1, 16)), 'Q2-family-label-order')
    require(type(radius) is Q and sign(radius) > 0, 'root-radius-domain')
    normalized = []
    for row in family:
        require(type(row['polynomial']) is list and len(row['polynomial']) <= 3,
                'Q2-family-polynomial-degree')
        normalized.append((row['record'], poly(row['polynomial'])))
    nonzero = [record for record, p in normalized if p]
    zero = [record for record, p in normalized if not p]
    if not nonzero:
        return dict(branch='all-zero-Q2', nonzero_records=[], zero_records=zero,
                    folds=[], gcd_monic=None, divisibility=[], root_certificate=None,
                    all_Q2_identically_zero=True)
    current, folds = [], []
    for record, p in normalized:
        if not p:
            continue
        previous = list(current)
        current, trace = euclidean(current, p) if current else euclidean(p, [])
        require(bool(current) and current[-1] == 1, 'common-gcd-monic')
        folds.append(dict(record=record, previous_gcd=enc(previous), input_polynomial=enc(p),
                          gcd_euclidean=trace, gcd_monic=enc(current)))
    divisibility = []
    for record, p in normalized:
        quotient, remainder = divide(p, current)
        reconstructed = padd(product(current, quotient), remainder)
        require(not remainder and reconstructed == p, 'common-gcd-divisibility')
        divisibility.append(dict(record=record, polynomial=enc(p), quotient=enc(quotient),
                                 remainder=enc(remainder), reconstructed_polynomial=enc(reconstructed)))
    return dict(branch='nonzero-gcd', nonzero_records=nonzero, zero_records=zero,
                folds=folds, gcd_monic=enc(current), divisibility=divisibility,
                root_certificate=root_certificate(current, radius),
                all_Q2_identically_zero=False)


FIXTURES = (
    ('constant-positive', ('1',), '1', 0),
    ('constant-negative', ('-1',), '1', 0),
    ('lower-zero-excluded', ('0', '1'), '1', 0),
    ('upper-zero-included', ('-1', '1'), '1', 1),
    ('outside-root', ('-2', '1'), '1', 0),
    ('double-upper-root', ('1', '-2', '1'), '1', 1),
    ('both-endpoints', ('0', '-1', '1'), '1', 1),
    ('common-zero-endpoint-trap', ('-2', '5', '-4', '1'), '1', 1),
    ('triple-upper-root', ('-1', '3', '-3', '1'), '1', 1),
    ('three-admissible-roots', ('-2/9', '11/9', '-2', '1'), '1', 3),
    ('irrational-positive-root', ('-1', '-1', '1'), '2', 1),
    ('negative-leading', ('1', '-1'), '1', 1),
    ('no-real-root', ('1', '0', '1'), '1', 0),
    ('all-negative-roots', ('6', '11', '6', '1'), '1', 0),
    ('double-interior-root', ('1/4', '-1', '1'), '1', 1),
    ('nonunit-radius', ('-1/3', '1'), '1/2', 1),
)

def native_decision(evidence, V_deltas):
    require(type(V_deltas) is list and len(V_deltas) == 7
            and all(type(q) is Q for q in V_deltas), 'decision-V-domain')
    require(type(evidence) is dict and evidence.get('branch') in ('all-zero-Q2', 'nonzero-gcd'),
            'decision-branch-domain')
    all_zero = evidence['branch'] == 'all-zero-Q2'
    f3_status = 'constant' if all(q == 0 for q in V_deltas) else 'nonconstant'
    if all_zero:
        require(evidence.get('gcd_monic') is None and evidence.get('root_certificate') is None
                and evidence.get('all_Q2_identically_zero') is True, 'decision-all-zero-shape')
        degree = count = None
        f2_status = 'constant'
    else:
        gcd, roots = evidence.get('gcd_monic'), evidence.get('root_certificate')
        require(type(gcd) is list and 1 <= len(gcd) <= 3 and all(type(q) is str for q in gcd)
                and type(roots) is dict and evidence.get('all_Q2_identically_zero') is False,
                'decision-nonzero-shape')
        degree = len(gcd)-1
        count = roots.get('distinct_real_roots')
        require(type(count) is int and 0 <= count <= degree, 'decision-count-domain')
        f2_status = 'nonconstant' if count == 0 else 'undetermined'
    rejected = f2_status == 'nonconstant' and f3_status == 'nonconstant'
    return dict(f2_status=f2_status, f3_status=f3_status,
                disposition='certified-connected-obstruction' if rejected else 'unresolved-connected-sensitivity',
                common_gcd_degree=degree, distinct_common_real_roots=count,
                no_common_real_root_on_admissible_interval=f2_status == 'nonconstant',
                restricted_28_child_repair_rejected=rejected,
                rational_root_decision_performed=False, rational_roots_remaining_asserted=False,
                actual_scale_root_asserted=False, positive_repair_asserted=False,
                all_positive_extensions_rejected=False, actual_scale_computed=False,
                remaining_parent_feasibility_decided=False)


GCD_FIXTURES = (
    ('all-zero', (), '1', None, None),
    ('zero-plus-constant', ((), ('2',), ('-1', '1')), '1', ('1',), 0),
    ('coprime-linears', (('-1', '1'), ('-2', '1')), '1', ('1',), 0),
    ('common-excluded-zero', (('0', '1'), ('0', '0', '1')), '1', ('0', '1'), 0),
    ('common-included-upper', (('-1', '1'), ('-2', '2')), '1', ('-1', '1'), 1),
    ('repeated-common-upper', (('1', '-2', '1'), ('2', '-4', '2')),
     '1', ('1', '-2', '1'), 1),
    ('degree-drop-negative-scaling', (('-1', '1', '0'), ('2', '-2')),
     '1', ('-1', '1'), 1),
    ('common-both-endpoints', (('0', '-1', '1'), ('0', '-2', '2')),
     '1', ('0', '-1', '1'), 1),
    ('common-irrational', (('-1', '-1', '1'), ('-2', '-2', '2')),
     '2', ('-1', '-1', '1'), 1),
    ('common-no-real', (('1', '0', '1'), ('2', '0', '2')),
     '1', ('1', '0', '1'), 0),
)


def family_fixtures():
    result = []
    for name, prefix, radius, expected_gcd, expected_count in GCD_FIXTURES:
        declared = [list(p) for p in prefix]+[[] for _ in range(15-len(prefix))]
        family = [dict(record=i+1, polynomial=[rational(q) for q in p])
                  for i, p in enumerate(declared)]
        evidence = common_gcd(family, rational(radius))
        expected = None if expected_gcd is None else list(expected_gcd)
        require(evidence['gcd_monic'] == expected, 'fixture-gcd-'+name)
        count = None if evidence['root_certificate'] is None else evidence['root_certificate']['distinct_real_roots']
        require(count == expected_count, 'fixture-common-root-count-'+name)
        result.append(dict(name=name, input_polynomials=declared, R=radius,
                           expected_gcd=expected, expected_distinct_real_roots=expected_count,
                           common_gcd=evidence, decision=native_decision(evidence, [Q(1)]+[Q(0)]*6),
                           native_model_claimed=False))
    return result


def decision_fixtures(families):
    result = []
    for index, f2_status in ((0, 'constant'), (1, 'nonconstant'), (4, 'undetermined')):
        family = families[index]
        for nonconstant in (False, True):
            name = family['name']+('--V-nonconstant' if nonconstant else '--V-constant')
            deltas = [Q(1) if nonconstant else Q(0)]+[Q(0)]*6
            f3_status = 'nonconstant' if nonconstant else 'constant'
            rejected = index == 1 and nonconstant
            decision = native_decision(family['common_gcd'], deltas)
            require(decision['f2_status'] == f2_status and decision['f3_status'] == f3_status
                    and decision['restricted_28_child_repair_rejected'] is rejected,
                    'fixture-connected-decision-'+name)
            result.append(dict(name=name, family_fixture=family['name'],
                               V_deltas=[str(q) for q in deltas], expected_f2_status=f2_status,
                               expected_f3_status=f3_status, expected_rejected=rejected,
                               decision=decision, native_model_claimed=False))
    return result


def fixtures():
    result = []
    for name, coefficients, radius, expected in FIXTURES:
        evidence = root_certificate([rational(q) for q in coefficients], rational(radius))
        require(evidence['distinct_real_roots'] == expected, 'fixture-root-count-'+name)
        result.append(dict(name=name, expected_distinct_real_roots=expected,
                           root_certificate=evidence, native_model_claimed=False))
    return result


def strict_equal(saved, expected):
    require(type(saved) is type(expected), 'saved-exact-type')
    if type(expected) is dict:
        require(set(saved) == set(expected), 'saved-fields')
        for key in expected:
            strict_equal(saved[key], expected[key])
    elif type(expected) is list:
        require(len(saved) == len(expected), 'saved-list-coverage')
        for a, b in zip(saved, expected):
            strict_equal(a, b)
    else:
        require(saved == expected, 'saved-exact-value')


def verify_saved(raw, expected):
    require(type(raw) is bytes and len(raw) <= MAX_OUTPUT, 'saved-byte-domain')
    strict_equal(load_json(raw), expected)
    require(raw == (canonical(expected)+'\n').encode('ascii'), 'saved-canonical-bytes')


def altered(value, path, replacement):
    result = clone(value)
    target = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement
    return result


CONTROL_PAIRS = (
    ("duplicate-json", "duplicate-json-key"),
    ("decimal-json", "noninteger-json-number"),
    ("nonfinite-json", "noninteger-json-number"),
    ("unreduced-rational", "noncanonical-rational"),
    ("boolean-rational", "noncanonical-rational"),
    ("rational-text-bound", "rational-text-budget"),
    ("integer-bit-bound", "integer-bit-budget"),
    ("boolean-polynomial", "exact-rational-required"),
    ("polynomial-degree", "polynomial-shape-degree"),
    ("root-degree", "root-polynomial-domain"),
    ("zero-polynomial", "root-polynomial-domain"),
    ("zero-radius", "root-radius-domain"),
    ("zero-polynomial-divisor", "zero-polynomial-divisor"),
    ("zero-rational-divisor", "zero-rational-divisor"),
    ("boolean-power", "power-domain"),
    ("wrong-size-ri88", "input-size-ri88"),
    ("wrong-hash-ri88", "input-hash-ri88"),
    ("wrong-size-ri111", "input-size-ri111"),
    ("wrong-hash-ri111", "input-hash-ri111"),
    ("wrong-size-ri109_adjudication", "input-size-ri109_adjudication"),
    ("wrong-hash-ri109_adjudication", "input-hash-ri109_adjudication"),
    ("wrong-size-ri111_adjudication", "input-size-ri111_adjudication"),
    ("wrong-hash-ri111_adjudication", "input-hash-ri111_adjudication"),
    ("wrong-size-ri115_adjudication", "input-size-ri115_adjudication"),
    ("wrong-hash-ri115_adjudication", "input-hash-ri115_adjudication"),
    ("wrong-size-ri117", "input-size-ri117"),
    ("wrong-hash-ri117", "input-hash-ri117"),
    ("wrong-size-ri117_connected", "input-size-ri117_connected"),
    ("wrong-hash-ri117_connected", "input-hash-ri117_connected"),
    ("wrong-size-ri117_adjudication", "input-size-ri117_adjudication"),
    ("wrong-hash-ri117_adjudication", "input-hash-ri117_adjudication"),
    ("wrong-status-ri109", "adjudication-status-ri109_adjudication"),
    ("wrong-status-ri111", "adjudication-status-ri111_adjudication"),
    ("wrong-status-ri115", "adjudication-status-ri115_adjudication"),
    ("wrong-status-ri117", "adjudication-status-ri117_adjudication"),
    ("wrong-scope-ri111", "adjudication-scope-ri111"),
    ("wrong-scope-ri115", "adjudication-scope-ri115"),
    ("wrong-scope-ri117", "adjudication-scope-ri117"),
    ("extra-ri88-field", "ri88-fields"),
    ("missing-ri88-field", "ri88-fields"),
    ("wrong-ri88-source", "ri88-source"),
    ("wrong-dependencies", "ri88-dependencies"),
    ("wrong-admission", "ri88-admission"),
    ("wrong-prefix", "ri88-actual-prefix"),
    ("boolean-coverage", "ri88-coverage"),
    ("boolean-record", "held-record-domain"),
    ("extra-record", "held-record-domain"),
    ("boolean-order", "held-order-types"),
    ("boolean-slot", "held-slot-types"),
    ("missing-slot", "held-slot-inventory"),
    ("duplicate-slot", "held-slot-inventory"),
    ("nonpositive-slot", "held-positive-normalized"),
    ("reordered-rows", "selected-row-order"),
    ("missing-held-row", "held-row-inventory"),
    ("duplicate-selected-row", "duplicate-selected-row"),
    ("changed-empty-locality", "held-empty-locality"),
    ("changed-proper-locality", "held-proper-locality"),
    ("changed-twin", "held-twin-symmetry"),
    ("changed-twin-diamond", "held-twin-diamond"),
    ("lookup-q6", "lookup-order-domain"),
    ("lookup-q7", "lookup-order-domain"),
    ("lookup-record", "lookup-record-domain"),
    ("lookup-C5-record", "lookup-record-domain"),
    ("lookup-slot", "lookup-slot-domain"),
    ("radius-eight-records", "radius-E-domain"),
    ("missing-stem-profile", "stem-profile-domain"),
    ("missing-connected-profile", "connected-coefficient-domain"),
    ("wrong-U2-domain", "connected-U-domain"),
    ("changed-radius", "fixed-radius"),
    ("wrong-Q2-fixed-division", "Q2-fixed-division"),
    ("missing-Q2", "Q2-family-count"),
    ("duplicate-Q2-label", "Q2-family-label-inventory"),
    ("reordered-Q2-labels", "Q2-family-label-order"),
    ("boolean-Q2-label", "Q2-family-label-types"),
    ("Q2-native-cubic", "Q2-family-polynomial-degree"),
    ("family-zero-radius", "root-radius-domain"),
    ("missing-V-decision", "decision-V-domain"),
    ("boolean-V-decision", "decision-V-domain"),
    ("boolean-decision", "decision-count-domain"),
    ("all-zero-fictitious-gcd", "decision-all-zero-shape"),
    ("extra-saved-field", "saved-fields"),
    ("missing-saved-field", "saved-fields"),
    ("saved-boolean-record", "saved-exact-type"),
    ("saved-missing-row", "saved-list-coverage"),
    ("saved-schema", "saved-exact-value"),
    ("saved-input-pin", "saved-exact-value"),
    ("saved-new-premise-pin", "saved-exact-value"),
    ("saved-selected-order", "saved-exact-value"),
    ("saved-locality-claim", "saved-exact-value"),
    ("saved-twin-claim", "saved-exact-value"),
    ("saved-stem-term", "saved-exact-value"),
    ("saved-stem-c", "saved-exact-value"),
    ("saved-stem-h", "saved-exact-value"),
    ("saved-stem-j", "saved-exact-value"),
    ("saved-stem-m", "saved-exact-value"),
    ("saved-stem-E", "saved-exact-value"),
    ("saved-stem-V", "saved-exact-value"),
    ("saved-U3-linear", "saved-exact-value"),
    ("saved-U3-quadratic", "saved-exact-value"),
    ("saved-connected-stem", "saved-exact-value"),
    ("saved-connected-sigma", "saved-exact-value"),
    ("saved-connected-e", "saved-exact-value"),
    ("saved-connected-ell", "saved-exact-value"),
    ("saved-E2-term", "saved-exact-value"),
    ("saved-E2", "saved-exact-value"),
    ("saved-C2-term", "saved-exact-value"),
    ("saved-C2", "saved-exact-value"),
    ("saved-A2", "saved-exact-value"),
    ("saved-B2", "saved-exact-value"),
    ("saved-U2-sign", "saved-exact-value"),
    ("saved-V-contrast", "saved-exact-value"),
    ("saved-V-zero-flag", "saved-exact-value"),
    ("saved-Q2-delta-A2", "saved-exact-value"),
    ("saved-Q2-delta-B2", "saved-exact-value"),
    ("saved-Q2-delta-C2", "saved-exact-value"),
    ("saved-Q2-sign", "saved-exact-value"),
    ("saved-Q2-raw-division", "saved-exact-value"),
    ("saved-Q2-zero-flag", "saved-exact-value"),
    ("saved-zero-member-omission", "saved-list-coverage"),
    ("saved-nonmonic-gcd", "saved-exact-value"),
    ("saved-wrong-gcd", "saved-exact-value"),
    ("saved-fold-previous", "saved-exact-value"),
    ("saved-fold-quotient", "saved-exact-value"),
    ("saved-skipped-late-fold", "saved-list-coverage"),
    ("saved-divisibility-quotient", "saved-exact-value"),
    ("saved-divisibility-remainder", "saved-list-coverage"),
    ("saved-divisibility-reconstruction", "saved-exact-value"),
    ("saved-all-zero-gcd", "saved-exact-type"),
    ("saved-constant-disposition", "saved-exact-value"),
    ("saved-surviving-disposition", "saved-exact-value"),
    ("saved-root-count", "saved-exact-value"),
    ("saved-endpoint-sign", "saved-exact-value"),
    ("saved-derivative-gcd", "saved-exact-value"),
    ("saved-square-free-quotient", "saved-exact-value"),
    ("saved-square-free-remainder", "saved-list-coverage"),
    ("saved-root-reconstruction", "saved-exact-value"),
    ("saved-sturm-chain", "saved-exact-value"),
    ("saved-negative-remainder", "saved-exact-value"),
    ("saved-upper-inclusion", "saved-exact-value"),
    ("saved-lower-exclusion", "saved-exact-value"),
    ("saved-variations", "saved-exact-value"),
    ("saved-f2-status", "saved-exact-value"),
    ("saved-f3-status", "saved-exact-value"),
    ("saved-only-f3-rejection", "saved-exact-value"),
    ("saved-only-f2-rejection", "saved-exact-value"),
    ("saved-both-sensitivity-not-rejected", "saved-exact-value"),
    ("saved-undetermined-rejection", "saved-exact-value"),
    ("saved-decision-fixture-delta", "saved-exact-value"),
    ("saved-decision-fixture-expectation", "saved-exact-value"),
    ("saved-actual-scale-claim", "saved-exact-value"),
    ("saved-global-rejection", "saved-exact-value"),
    ("saved-positive-repair", "saved-exact-value"),
    ("saved-remaining-parent-claim", "saved-exact-value"),
    ("saved-rational-decision-claim", "saved-exact-value"),
    ("saved-rational-roots-claim", "saved-exact-value"),
    ("saved-actual-root-claim", "saved-exact-value"),
    ("saved-radius", "saved-exact-value"),
    ("saved-coverage", "saved-exact-value"),
    ("saved-limitation", "saved-exact-value"),
    ("saved-limit", "saved-exact-value"),
    ("saved-checker-pin", "saved-exact-value"),
    ("saved-fixture-trailing-zero", "saved-list-coverage"),
    ("saved-missing-root-fixture", "saved-list-coverage"),
    ("saved-missing-family-fixture", "saved-list-coverage"),
    ("saved-missing-decision-fixture", "saved-list-coverage"),
    ("saved-noncanonical", "saved-canonical-bytes"),
)

SAVED_MUTATIONS = (
    ("saved-schema", ["schema"], "other", "saved-exact-value"),
    ("saved-input-pin", ["accepted_inputs", "ri88", "sha256"], "0000000000000000000000000000000000000000000000000000000000000000", "saved-exact-value"),
    ("saved-new-premise-pin", ["accepted_sources", "ri117_adjudication", "sha256"], "0000000000000000000000000000000000000000000000000000000000000000", "saved-exact-value"),
    ("saved-selected-order", ["inputs", "selected_order", 0], "C3:1", "saved-exact-value"),
    ("saved-locality-claim", ["inputs", "proper_locality_checked"], False, "saved-exact-value"),
    ("saved-twin-claim", ["inputs", "twin_diamond_checked"], False, "saved-exact-value"),
    ("saved-stem-term", ["stem_profiles", 0, "E_terms", 0], None, "saved-exact-value"),
    ("saved-stem-c", ["stem_profiles", 0, "c"], None, "saved-exact-value"),
    ("saved-stem-h", ["stem_profiles", 0, "h"], None, "saved-exact-value"),
    ("saved-stem-j", ["stem_profiles", 0, "j"], None, "saved-exact-value"),
    ("saved-stem-m", ["stem_profiles", 0, "m"], None, "saved-exact-value"),
    ("saved-stem-E", ["stem_profiles", 0, "E"], None, "saved-exact-value"),
    ("saved-stem-V", ["stem_profiles", 0, "V"], None, "saved-exact-value"),
    ("saved-U3-linear", ["stem_profiles", 0, "U3_padded", 1], None, "saved-exact-value"),
    ("saved-U3-quadratic", ["stem_profiles", 0, "U3_padded", 2], None, "saved-exact-value"),
    ("saved-connected-stem", ["connected_profiles", 0, "stem_record"], 1, "saved-exact-value"),
    ("saved-connected-sigma", ["connected_profiles", 0, "sigma"], 1, "saved-exact-value"),
    ("saved-connected-e", ["connected_profiles", 0, "e"], None, "saved-exact-value"),
    ("saved-connected-ell", ["connected_profiles", 0, "ell"], None, "saved-exact-value"),
    ("saved-E2-term", ["connected_profiles", 0, "E2_terms", 0], None, "saved-exact-value"),
    ("saved-E2", ["connected_profiles", 0, "E2"], None, "saved-exact-value"),
    ("saved-C2-term", ["connected_profiles", 0, "C2_terms", 4], None, "saved-exact-value"),
    ("saved-C2", ["connected_profiles", 0, "C2"], None, "saved-exact-value"),
    ("saved-A2", ["connected_profiles", 0, "A2"], None, "saved-exact-value"),
    ("saved-B2", ["connected_profiles", 0, "B2"], None, "saved-exact-value"),
    ("saved-U2-sign", ["connected_profiles", 0, "U2_padded", 1], None, "saved-exact-value"),
    ("saved-V-contrast", ["V_contrasts", 0, "delta_V"], None, "saved-exact-value"),
    ("saved-V-zero-flag", ["V_contrasts", 0, "is_zero"], None, "saved-exact-value"),
    ("saved-Q2-delta-A2", ["Q2_contrasts", 0, "delta_A2"], None, "saved-exact-value"),
    ("saved-Q2-delta-B2", ["Q2_contrasts", 0, "delta_B2"], None, "saved-exact-value"),
    ("saved-Q2-delta-C2", ["Q2_contrasts", 0, "delta_C2"], None, "saved-exact-value"),
    ("saved-Q2-sign", ["Q2_contrasts", 0, "Q2_padded", 0], None, "saved-exact-value"),
    ("saved-Q2-raw-division", ["Q2_contrasts", 0, "U2_difference_padded", 0], "1", "saved-exact-value"),
    ("saved-Q2-zero-flag", ["Q2_contrasts", 0, "is_zero"], None, "saved-exact-value"),
    ("saved-zero-member-omission", ["family_fixtures", 1, "common_gcd", "zero_records"], [], "saved-list-coverage"),
    ("saved-nonmonic-gcd", ["family_fixtures", 1, "common_gcd", "gcd_monic", 0], "2", "saved-exact-value"),
    ("saved-wrong-gcd", ["family_fixtures", 4, "common_gcd", "gcd_monic", 0], None, "saved-exact-value"),
    ("saved-fold-previous", ["family_fixtures", 2, "common_gcd", "folds", 1, "previous_gcd", 0], None, "saved-exact-value"),
    ("saved-fold-quotient", ["family_fixtures", 2, "common_gcd", "folds", 1, "gcd_euclidean", 0, "quotient", 0], None, "saved-exact-value"),
    ("saved-skipped-late-fold", ["family_fixtures", 1, "common_gcd", "folds"], [], "saved-list-coverage"),
    ("saved-divisibility-quotient", ["family_fixtures", 2, "common_gcd", "divisibility", 0, "quotient", 0], None, "saved-exact-value"),
    ("saved-divisibility-remainder", ["family_fixtures", 2, "common_gcd", "divisibility", 0, "remainder"], ["1"], "saved-list-coverage"),
    ("saved-divisibility-reconstruction", ["family_fixtures", 2, "common_gcd", "divisibility", 0, "reconstructed_polynomial", 0], None, "saved-exact-value"),
    ("saved-all-zero-gcd", ["family_fixtures", 0, "common_gcd", "gcd_monic"], ["1"], "saved-exact-type"),
    ("saved-constant-disposition", ["family_fixtures", 1, "decision", "disposition"], "unresolved-connected-sensitivity", "saved-exact-value"),
    ("saved-surviving-disposition", ["family_fixtures", 4, "decision", "disposition"], "certified-connected-obstruction", "saved-exact-value"),
    ("saved-root-count", ["root_fixtures", 7, "root_certificate", "distinct_real_roots"], 4, "saved-exact-value"),
    ("saved-endpoint-sign", ["root_fixtures", 7, "root_certificate", "upper", "signs", 0], 2, "saved-exact-value"),
    ("saved-derivative-gcd", ["root_fixtures", 7, "root_certificate", "gcd_monic", 0], None, "saved-exact-value"),
    ("saved-square-free-quotient", ["root_fixtures", 7, "root_certificate", "square_free_quotient", 0], None, "saved-exact-value"),
    ("saved-square-free-remainder", ["root_fixtures", 7, "root_certificate", "square_free_remainder"], ["1"], "saved-list-coverage"),
    ("saved-root-reconstruction", ["root_fixtures", 7, "root_certificate", "reconstructed_polynomial", 0], None, "saved-exact-value"),
    ("saved-sturm-chain", ["root_fixtures", 7, "root_certificate", "sturm_chain", 0, 0], None, "saved-exact-value"),
    ("saved-negative-remainder", ["root_fixtures", 7, "root_certificate", "sturm_divisions", 0, "next_term", 0], None, "saved-exact-value"),
    ("saved-upper-inclusion", ["root_fixtures", 7, "root_certificate", "upper_included"], False, "saved-exact-value"),
    ("saved-lower-exclusion", ["root_fixtures", 7, "root_certificate", "lower_excluded"], False, "saved-exact-value"),
    ("saved-variations", ["root_fixtures", 7, "root_certificate", "lower", "variations"], 99, "saved-exact-value"),
    ("saved-f2-status", ["decision", "f2_status"], None, "saved-exact-value"),
    ("saved-f3-status", ["decision", "f3_status"], None, "saved-exact-value"),
    ("saved-only-f3-rejection", ["decision_fixtures", 1, "decision", "restricted_28_child_repair_rejected"], True, "saved-exact-value"),
    ("saved-only-f2-rejection", ["decision_fixtures", 2, "decision", "restricted_28_child_repair_rejected"], True, "saved-exact-value"),
    ("saved-both-sensitivity-not-rejected", ["decision_fixtures", 3, "decision", "restricted_28_child_repair_rejected"], False, "saved-exact-value"),
    ("saved-undetermined-rejection", ["decision_fixtures", 5, "decision", "restricted_28_child_repair_rejected"], True, "saved-exact-value"),
    ("saved-decision-fixture-delta", ["decision_fixtures", 0, "V_deltas", 0], "1", "saved-exact-value"),
    ("saved-decision-fixture-expectation", ["decision_fixtures", 3, "expected_rejected"], False, "saved-exact-value"),
    ("saved-actual-scale-claim", ["decision", "actual_scale_computed"], True, "saved-exact-value"),
    ("saved-global-rejection", ["decision", "all_positive_extensions_rejected"], True, "saved-exact-value"),
    ("saved-positive-repair", ["decision", "positive_repair_asserted"], True, "saved-exact-value"),
    ("saved-remaining-parent-claim", ["decision", "remaining_parent_feasibility_decided"], True, "saved-exact-value"),
    ("saved-rational-decision-claim", ["decision", "rational_root_decision_performed"], True, "saved-exact-value"),
    ("saved-rational-roots-claim", ["decision", "rational_roots_remaining_asserted"], True, "saved-exact-value"),
    ("saved-actual-root-claim", ["decision", "actual_scale_root_asserted"], True, "saved-exact-value"),
    ("saved-radius", ["scale_domain", "R"], None, "saved-exact-value"),
    ("saved-coverage", ["coverage", "connected_records"], 8, "saved-exact-value"),
    ("saved-limitation", ["limitations", "sensitivity_not_positive_repair"], False, "saved-exact-value"),
    ("saved-limit", ["arithmetic_limits", "counted_operations"], 200001, "saved-exact-value"),
    ("saved-checker-pin", ["checker_sha256"], "0000000000000000000000000000000000000000000000000000000000000000", "saved-exact-value"),
    ("saved-fixture-trailing-zero", ["family_fixtures", 6, "input_polynomials", 0], ["-1", "1"], "saved-list-coverage"),
    ("saved-missing-root-fixture", ["root_fixtures"], [], "saved-list-coverage"),
    ("saved-missing-family-fixture", ["family_fixtures"], [], "saved-list-coverage"),
    ("saved-missing-decision-fixture", ["decision_fixtures"], [], "saved-list-coverage"),
)


def refusal_controls(data, raw_inputs, adjudications, rows, witness):
    passed = []
    def expect(name, reason, action):
        require(len(passed) < len(CONTROL_PAIRS) and CONTROL_PAIRS[len(passed)] == (name, reason),
                'refusal-declaration-order')
        try:
            action()
        except Refusal as error:
            require(str(error) == reason, 'wrong-refusal-reason-'+name)
        else:
            raise Refusal('missing-refusal-'+name)
        passed.append(dict(name=name, reason=reason))
    expect('duplicate-json', 'duplicate-json-key', lambda: load_json('{"x":0,"x":1}'))
    expect('decimal-json', 'noninteger-json-number', lambda: load_json('[0.5]'))
    expect('nonfinite-json', 'noninteger-json-number', lambda: load_json('[NaN]'))
    expect('unreduced-rational', 'noncanonical-rational', lambda: rational('2/2'))
    expect('boolean-rational', 'noncanonical-rational', lambda: rational(True))
    expect('rational-text-bound', 'rational-text-budget', lambda: rational('1'*(MAX_TEXT+1)))
    expect('integer-bit-bound', 'integer-bit-budget', lambda: bounded(Q(1 << INPUT_BITS), INPUT_BITS))
    expect('boolean-polynomial', 'exact-rational-required', lambda: poly([True]))
    expect('polynomial-degree', 'polynomial-shape-degree', lambda: poly([Q(1)]*6))
    expect('root-degree', 'root-polynomial-domain', lambda: root_certificate([Q(1)]*5, Q(1)))
    expect('zero-polynomial', 'root-polynomial-domain', lambda: root_certificate([], Q(1)))
    expect('zero-radius', 'root-radius-domain', lambda: root_certificate([Q(1)], Q(0)))
    expect('zero-polynomial-divisor', 'zero-polynomial-divisor', lambda: divide([Q(1)], []))
    expect('zero-rational-divisor', 'zero-rational-divisor', lambda: div(Q(1), Q(0)))
    expect('boolean-power', 'power-domain', lambda: power(Q(1), True))
    for role in INPUT_ROLES:
        expect('wrong-size-'+role, 'input-size-'+role,
               lambda role=role: input_bytes(role, raw_inputs[role][:-1]))
        expect('wrong-hash-'+role, 'input-hash-'+role, lambda role=role:
               input_bytes(role, bytes([raw_inputs[role][0] ^ 1])+raw_inputs[role][1:]))
    for short, role in (('ri109', 'ri109_adjudication'), ('ri111', 'ri111_adjudication'),
                        ('ri115', 'ri115_adjudication'), ('ri117', 'ri117_adjudication')):
        expect('wrong-status-'+short, 'adjudication-status-'+role,
               lambda role=role: adjudication(role, altered(adjudications[role], ['status'], 'NOT_ACCEPTED')))
    expect('wrong-scope-ri111', 'adjudication-scope-ri111', lambda: adjudication('ri111_adjudication',
           altered(adjudications['ri111_adjudication'], ['new_numerical_execution_admitted'], True)))
    expect('wrong-scope-ri115', 'adjudication-scope-ri115', lambda: adjudication('ri115_adjudication',
           altered(adjudications['ri115_adjudication'], ['whole_positive_extension_established'], True)))
    expect('wrong-scope-ri117', 'adjudication-scope-ri117', lambda: adjudication('ri117_adjudication',
           altered(adjudications['ri117_adjudication'], ['active_execution_admission'], True)))
    expect('extra-ri88-field', 'ri88-fields', lambda: provenance(dict(data, extra=None)))
    expect('missing-ri88-field', 'ri88-fields', lambda: provenance({k: v for k, v in data.items() if k != 'prefix'}))
    expect('wrong-ri88-source', 'ri88-source', lambda: provenance(altered(data, ['checker_sha256'], '0'*64)))
    expect('wrong-dependencies', 'ri88-dependencies', lambda: provenance(altered(data, ['dependencies'], {})))
    expect('wrong-admission', 'ri88-admission', lambda: provenance(altered(data, ['admission', 'epsilon'], '1/8')))
    expect('wrong-prefix', 'ri88-actual-prefix', lambda: provenance(altered(data, ['prefix', 'canonical_lex_stages'], True)))
    expect('boolean-coverage', 'ri88-coverage', lambda: provenance(altered(data, ['coverage', 'held_marked_rows'], True)))
    expect('boolean-record', 'held-record-domain', lambda: held_entry(altered(rows[0], ['record'], False)))
    expect('extra-record', 'held-record-domain', lambda: held_entry(altered(rows[0], ['record'], 8)))
    expect('boolean-order', 'held-order-types', lambda: held_entry(altered(rows[0], ['order', 0], False)))
    expect('boolean-slot', 'held-slot-types', lambda: held_entry(altered(rows[0], ['probabilities', 0, 0], False)))
    expect('missing-slot', 'held-slot-inventory', lambda: held_entry(altered(rows[0], ['probabilities'], rows[0]['probabilities'][:-1])))
    expect('duplicate-slot', 'held-slot-inventory', lambda: held_entry(altered(rows[0], ['probabilities', 1, 0], 0)))
    expect('nonpositive-slot', 'held-positive-normalized', lambda: held_entry(altered(rows[0], ['probabilities', 0, 1], '0')))
    reordered = clone(data)
    reordered['held_rows'][0], reordered['held_rows'][1] = reordered['held_rows'][1], reordered['held_rows'][0]
    expect('reordered-rows', 'selected-row-order', lambda: extract(reordered))
    expect('missing-held-row', 'held-row-inventory',
           lambda: extract(altered(data, ['held_rows'], data['held_rows'][:-1])))
    duplicate = clone(data)
    duplicate['held_rows'][1] = clone(duplicate['held_rows'][0])
    expect('duplicate-selected-row', 'duplicate-selected-row', lambda: extract(duplicate))
    for name, order, slot, reason in (
        ('changed-empty-locality', C3, 0, 'held-empty-locality'),
        ('changed-proper-locality', C3, 1, 'held-proper-locality'),
        ('changed-twin', H5, 4, 'held-twin-symmetry'),
    ):
        modified = clone(data)
        row = next(e['probabilities'] for e in modified['held_rows'] if e['order'] == list(order) and e['record'] == 0)
        transfer = div(rational(row[slot][1]), Q(2))
        row[slot][1] = str(transfer)
        row[-1][1] = str(add(rational(row[-1][1]), transfer))
        expect(name, reason, lambda modified=modified: extract(modified))
    diamond = clone(data)
    row = next(e['probabilities'] for e in diamond['held_rows'] if e['order'] == list(H5) and e['record'] == 0)
    for slot in (4, 5):
        transfer = div(rational(row[slot][1]), Q(2))
        row[slot][1] = str(transfer)
        row[-1][1] = str(add(rational(row[-1][1]), transfer))
    expect('changed-twin-diamond', 'held-twin-diamond', lambda: extract(diamond))
    for label, order in (('q6', (0, 1, 3, 7, 7, 7)), ('q7', (0, 1, 3, 7, 7, 7, 7))):
        expect('lookup-'+label, 'lookup-order-domain', lambda order=order: lookup({}, order, 0, 0))
    expect('lookup-record', 'lookup-record-domain', lambda: lookup({}, C3, 8, 0))
    expect('lookup-C5-record', 'lookup-record-domain', lambda: lookup({}, C5, 16, 0))
    expect('lookup-slot', 'lookup-slot-domain', lambda: lookup({}, C3, 0, 2))
    expect('radius-eight-records', 'radius-E-domain', lambda: radius_for([Q(1)]*8))
    stem = [(Q(1), Q(1))]*8
    base, other = (Q(1), Q(2), Q(3)), (Q(4), Q(6), Q(8))
    u0, u1 = [Q(3), Q(-1), Q(2), Q(3)], [Q(3), Q(-4), Q(6), Q(8)]
    coeffs, us = [base, other]+[base]*14, [u0, u1]+[u0]*14
    expect('missing-stem-profile', 'stem-profile-domain',
           lambda: sensitivity_contrasts(stem[:-1], coeffs, us, Q(1, 4)))
    expect('missing-connected-profile', 'connected-coefficient-domain',
           lambda: sensitivity_contrasts(stem, coeffs[:-1], us, Q(1, 4)))
    expect('wrong-U2-domain', 'connected-U-domain',
           lambda: sensitivity_contrasts(stem, coeffs, us[:-1], Q(1, 4)))
    expect('changed-radius', 'fixed-radius', lambda: sensitivity_contrasts(stem, coeffs, us, Q(1)))
    expect('wrong-Q2-fixed-division', 'Q2-fixed-division',
           lambda: sensitivity_contrasts(stem, coeffs, [u0]*16, Q(1, 4)))
    _, _, _, synthetic_q = sensitivity_contrasts(stem, coeffs, us, Q(1, 4))
    require(synthetic_q[0]['Q2_padded'] == ['-3', '4', '5']
            and synthetic_q[0]['U2_difference_padded'] == ['0', '-3', '4', '5'],
            'synthetic-Q2-orientation')
    family = [dict(record=i, polynomial=[Q(1)]) for i in range(1, 16)]
    expect('missing-Q2', 'Q2-family-count', lambda: common_gcd(family[:-1], Q(1)))
    expect('duplicate-Q2-label', 'Q2-family-label-inventory',
           lambda: common_gcd([dict(family[0], record=2)]+family[1:], Q(1)))
    expect('reordered-Q2-labels', 'Q2-family-label-order',
           lambda: common_gcd([family[1], family[0]]+family[2:], Q(1)))
    expect('boolean-Q2-label', 'Q2-family-label-types',
           lambda: common_gcd([dict(family[0], record=True)]+family[1:], Q(1)))
    expect('Q2-native-cubic', 'Q2-family-polynomial-degree',
           lambda: common_gcd([dict(family[0], polynomial=[Q(1)]*4)]+family[1:], Q(1)))
    expect('family-zero-radius', 'root-radius-domain', lambda: common_gcd(family, Q(0)))
    expect('missing-V-decision', 'decision-V-domain',
           lambda: native_decision(witness['family_fixtures'][0]['common_gcd'], [Q(0)]*6))
    expect('boolean-V-decision', 'decision-V-domain',
           lambda: native_decision(witness['family_fixtures'][0]['common_gcd'], [False]+[Q(0)]*6))
    expect('boolean-decision', 'decision-count-domain', lambda: native_decision(altered(
           witness['family_fixtures'][1]['common_gcd'], ['root_certificate', 'distinct_real_roots'], True), [Q(0)]*7))
    expect('all-zero-fictitious-gcd', 'decision-all-zero-shape', lambda: native_decision(altered(
           witness['family_fixtures'][0]['common_gcd'], ['gcd_monic'], ['1']), [Q(0)]*7))
    expect('extra-saved-field', 'saved-fields', lambda: strict_equal(dict(witness, extra=None), witness))
    expect('missing-saved-field', 'saved-fields', lambda: strict_equal({k: v for k, v in witness.items() if k != 'inputs'}, witness))
    expect('saved-boolean-record', 'saved-exact-type', lambda: strict_equal(altered(witness, ['stem_profiles', 0, 'record'], False), witness))
    expect('saved-missing-row', 'saved-list-coverage', lambda: strict_equal(altered(witness, ['inputs', 'held_rows'], rows[:-1]), witness))
    # None denotes a guaranteed-different value of the SAME declared type.
    # Rational strings are toggled 0/1 without interpreting native operands.
    # All branch-specific paths below refer to fixed synthetic fixtures.
    for name, path, value, reason in SAVED_MUTATIONS:
        original = witness
        for key in path:
            original = original[key]
        if name == 'saved-skipped-late-fold':
            # Fixed zero-plus-constant fixture: keep its first constant fold
            # and omit the later nonzero member's required fold.
            value = original[:1]
        if value is None:
            require(type(original) in (str, bool), 'control-field-type')
            value = not original if type(original) is bool else ('1' if original == '0' else '0')
        require(type(original) is type(value) or reason == 'saved-exact-type',
                'control-replacement-type')
        expect(name, reason, lambda path=path, value=value:
               strict_equal(altered(witness, path, value), witness))
    expect('saved-noncanonical', 'saved-canonical-bytes',
           lambda: verify_saved((canonical(witness)+'\n\n').encode('ascii'), witness))
    require(tuple((item['name'], item['reason']) for item in passed) == CONTROL_PAIRS
            and len({name for name, _reason in CONTROL_PAIRS}) == len(CONTROL_PAIRS),
            'refusal-ordered-inventory')
    return passed


def build(data, source_hash):
    held, rows = extract(data)
    stem, stem_evidence = [], []
    for record in RECORDS:
        values, evidence = stem_formula(held, record)
        stem.append(values)
        stem_evidence.append(evidence)
    coeffs, U, connected_evidence = [], [], []
    for record in range(16):
        values, u, evidence = connected_formula(held, record, stem)
        coeffs.append(values)
        U.append(u)
        connected_evidence.append(evidence)
    E = [stem[0][0], stem[1][0]]
    radius = radius_for(E)
    V_deltas, v_evidence, family, q_evidence = sensitivity_contrasts(stem, coeffs, U, radius)
    common = common_gcd(family, radius)
    margins = [sub(Q(1), mul(radius, e)) for e in E]
    require(all(calc('cmp', margin, Q(1, 2)) > 0 for margin in margins), 'radius-full-margin')
    families = family_fixtures()
    witness = dict(
        schema=SCHEMA,
        accepted_inputs={'ri88': dict(bytes=PINS['ri88'][0], sha256=PINS['ri88'][1])},
        accepted_sources={role: dict(bytes=PINS[role][0], sha256=PINS[role][1]) for role in INPUT_ROLES[1:]},
        inputs=dict(held_rows=rows,
                    selected_order=[name+':'+str(r) for name, order in zip(('C3', 'C4', 'C5', 'H5'), HELD)
                                    for r in RECORD_DOMAIN[order]],
                    prefix_replayed=False, H_or_z_values_read=False,
                    transport_basis='RI117 complete connected profiles; RI111 maximal-bit and RI85 unique/twin-top transport',
                    proper_locality_checked=True, twin_diamond_checked=True),
        stem_profiles=stem_evidence, connected_profiles=connected_evidence,
        scale_domain=dict(R=str(radius), selected_E=[str(e) for e in E], interval='0<rho<=R',
                          lower_full_margins_at_R=[str(q) for q in margins],
                          actual_rho_evaluated=False, amplitude='1/4', seed_unchanged=True),
        V_contrasts=v_evidence, Q2_contrasts=q_evidence,
        common_gcd=common, decision=native_decision(common, V_deltas),
        coverage=dict(held_rows=40, held_probability_slots=224, stem_records=8,
                      connected_records=16, V_contrasts=7, Q2_contrasts=15,
                      H_or_z_arithmetic_values=0, new_q6_q7_rows=0, native_polynomial_degree_cap=2),
        limitations=dict(real_roots_do_not_imply_rational_roots=True,
                         roots_in_outer_interval_do_not_locate_actual_scale=True,
                         complete_all_size_extension_not_claimed=True,
                         QM_geometry_gravity_derivation_not_claimed=True,
                         restricted_candidate_only=True, external_custody_required=True,
                         remaining_parent_feasibility_not_decided=True,
                         sensitivity_not_positive_repair=True),
        arithmetic_limits=dict(input_rational_bits=INPUT_BITS, working_rational_bits=MAX_BITS,
                               transient_integer_bits=2*MAX_BITS+2, counted_operations=MAX_OPS,
                               rational_text_characters=MAX_TEXT, output_bytes=MAX_OUTPUT,
                               active_child_seconds=MAX_SECONDS, resident_bytes=MAX_BYTES),
        checker_sha256=source_hash, root_fixtures=fixtures(), family_fixtures=families,
        decision_fixtures=decision_fixtures(families))
    return witness, rows


def read_bounded(path, limit):
    require(path.stat().st_size <= limit, 'file-byte-budget')
    with path.open('rb') as stream:
        raw = stream.read(limit+1)
    require(len(raw) <= limit, 'file-byte-budget')
    return raw


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'invocation-domain')
    START = time.monotonic()
    def alarm(_number, _frame):
        raise Refusal('wall-budget')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(MAX_SECONDS)
    sys.set_int_max_str_digits(2*MAX_BITS)
    source = Path(__file__).resolve()
    source_bytes = read_bounded(source, MAX_OUTPUT)
    source_hash = sha256(source_bytes).hexdigest()
    # Self-hash is custody output, not independent source authentication.
    # The admitted outer caller and separately pinned auditor bind this source.
    paths = {
        'ri88': source.parent/'inputs'/'ri88.json',
        'ri111': source.parent/'inputs'/'ri111.md',
        'ri109_adjudication': source.parent/'inputs'/'ri109_adjudication.json',
        'ri111_adjudication': source.parent/'inputs'/'ri111_adjudication.json',
        'ri115_adjudication': source.parent/'inputs'/'ri115_adjudication.json',
        'ri117': source.parent/'inputs'/'ri117.md',
        'ri117_connected': source.parent/'inputs'/'ri117_connected.md',
        'ri117_adjudication': source.parent/'inputs'/'ri117_adjudication.json',
    }
    raw_inputs = {role: read_bounded(paths[role], PINS[role][0]) for role in INPUT_ROLES}
    for role in INPUT_ROLES:
        input_bytes(role, raw_inputs[role])
    adjudications = {role: load_json(raw_inputs[role]) for role in ADJUDICATION_ROLES}
    for role in ADJUDICATION_ROLES:
        adjudication(role, adjudications[role])
    data = load_json(raw_inputs['ri88'])  # All eight pins and four metadata guards precede this parse.
    witness, rows = build(data, source_hash)
    witness['refusal_controls'] = refusal_controls(data, raw_inputs, adjudications, rows, witness)
    require(len(witness) == 19, 'certificate-section-count')
    encoded = (canonical(witness)+'\n').encode('ascii')
    require(len(encoded) <= MAX_OUTPUT, 'output-byte-budget')
    saved_raw = None
    saved_path = source.with_name('CERTIFICATE.json')
    if not sys.argv[1:]:
        saved_raw = read_bounded(saved_path, MAX_OUTPUT)
        verify_saved(saved_raw, witness)
    for role in INPUT_ROLES:
        require(read_bounded(paths[role], PINS[role][0]) == raw_inputs[role], 'input-changed-'+role)
    require(read_bounded(source, MAX_OUTPUT) == source_bytes, 'source-changed')
    if saved_raw is not None:
        require(read_bounded(saved_path, MAX_OUTPUT) == saved_raw, 'saved-changed')
    budget()
    try:
        if sys.argv[1:]:
            sys.stdout.buffer.write(encoded)
            sys.stdout.buffer.flush()
        else:
            summary = dict(status='PASS', schema=SCHEMA, checker_sha256=source_hash,
                           certificate_sha256=sha256(saved_raw).hexdigest(),
                           witness_sha256=sha256(encoded).hexdigest(), decision=witness['decision'],
                           root_fixture_count=len(witness['root_fixtures']),
                           family_fixture_count=len(witness['family_fixtures']),
                           decision_fixture_count=len(witness['decision_fixtures']),
                           refusal_count=len(witness['refusal_controls']),
                           producer_replay_is_independent_audit=False)
            print(canonical(summary), flush=True)
        budget()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
