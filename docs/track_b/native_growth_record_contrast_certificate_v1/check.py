#!/usr/bin/env python3
"""RI105 fixed two-record contrast. SOURCE PREPARATION, NOT AN EXECUTED RESULT.

Exact arithmetic is confined to six RI88 rows / 32 slots. All other native
probability values remain unconverted strings. No seed multipliers are read.
The degree-at-most-three polynomial and R are exactly the RI103 formulas.
Only complete real-root exclusion is attempted; surviving real roots do not
establish rational roots, equality at the actual scale, or a feasible repair.
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

SCHEMA = 'ri105-record-contrast-certificate-v1'
PINS = {
    'ri88': (1828149, 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    'ri103': (20198, '8a2a4bf9142341e2511763cbfd799183860e907372d577b9b32d8c1cf24a955c'),
    'ri94': (25150, '65645454993a81b70a0d9cd278eb137cd6b218055b1cb026f9950b7cb8895844'),
}
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
C3, C4, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 7)
HELD = (C3, C4, H5)
IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 23, 31))
T1 = (0, 1, 3, 7, 7, 7, 7)
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
    require(type(entry['record']) is int and entry['record'] in (0, 1), 'held-record-domain')
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
    selected = {}
    for entry in data['held_rows']:
        require(type(entry) is dict and set(entry) == {'order', 'record', 'probabilities'},
                'held-metadata-fields')
        require(type(entry['order']) is list and all(type(x) is int for x in entry['order'])
                and type(entry['record']) is int, 'held-metadata-types')
        key = (tuple(entry['order']), entry['record'])
        if key[0] in HELD and key[1] in (0, 1):
            require(key not in selected, 'duplicate-selected-row')
            selected[key] = entry
    keys = [(order, record) for order in HELD for record in (0, 1)]
    require(set(selected) == set(keys), 'selected-row-completeness')
    require(list(selected) == keys, 'selected-row-order')
    held = {key: held_entry(selected[key]) for key in keys}
    for order in HELD:
        require(held[(order, 0)][0] == held[(order, 1)][0], 'held-empty-locality')
    for record in (0, 1):
        require(held[(H5, record)][15] == held[(H5, record)][23], 'held-twin-symmetry')
    return held, [selected[key] for key in keys]


def lookup(held, order, record, part):
    require(type(order) is tuple and all(type(x) is int for x in order)
            and order in HELD, 'lookup-order-domain')
    require(type(record) is int and record in (0, 1), 'lookup-record-domain')
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


def record_formula(held, record):
    slots = (0, 1, 3, 7)
    A = [lookup(held, C3, record, s) for s in slots]
    B = [lookup(held, C4, record, s) for s in slots]
    G = [lookup(held, H5, record, s) for s in slots]
    c = lookup(held, C4, record, 15)
    h = lookup(held, H5, record, 15)
    j = lookup(held, H5, record, 31)
    e_terms = [div(mul(a, power(g, 3)), power(b, 3)) for a, b, g in zip(A, B, G)]
    k_terms = [div(mul(power(a, 3), power(g, 6)), power(b, 8)) for a, b, g in zip(A, B, G)]
    one_cap = div(mul(Q(3), power(h, 2)), c)
    two_cap = mul(Q(3), j)
    E = total(e_terms+[one_cap, two_cap])
    v = div(power(h, 3), power(c, 2))
    K = total(k_terms)
    U = [Q(4), mul(Q(-4), E), mul(Q(6), j), mul(Q(4), v), K]
    evidence = dict(record=record, E_terms=[str(q) for q in e_terms],
                    E_one_cap_total=str(one_cap), E_two_cap_total=str(two_cap),
                    E=str(E), v_star=str(v), K_terms=[str(q) for q in k_terms],
                    K=str(K), c=str(c), h=str(h), j=str(j), U_padded=[str(q) for q in U])
    return (E, j, v, K), U, evidence


def radius_for(E):
    require(type(E) is list and len(E) == 2 and all(type(q) is Q and sign(q) > 0 for q in E),
            'radius-E-domain')
    maximum = E[0] if calc('cmp', E[0], E[1]) >= 0 else E[1]
    return div(Q(1), mul(Q(2), add(Q(1), maximum)))


def contrast(coeffs, U, radius):
    require(type(coeffs) is list and len(coeffs) == 2 and all(type(row) is tuple
            and len(row) == 4 and all(type(q) is Q for q in row) for row in coeffs),
            'contrast-coefficient-domain')
    delta = [sub(b, a) for a, b in zip(*coeffs)]
    require(delta[1] != 0, 'accepted-delta-j-nonzero')
    require(type(radius) is Q and radius == radius_for([row[0] for row in coeffs]),
            'fixed-radius')
    p = [mul(Q(factor), d) for factor, d in zip((-4, 6, 4, 1), delta)]
    require(type(U) is list and len(U) == 2 and all(type(row) is list and len(row) == 5
            and all(type(q) is Q for q in row) for row in U), 'contrast-U-domain')
    raw = [sub(b, a) for a, b in zip(*U)]
    require(raw == [Q(0)]+p and p[1] != 0, 'contrast-fixed-division')
    return p, dict(delta_E=str(delta[0]), delta_j=str(delta[1]), delta_v_star=str(delta[2]),
                   delta_K=str(delta[3]), P_padded=[str(q) for q in p],
                   U1_minus_U0_padded=[str(q) for q in raw], fixed_divisor='rho',
                   quotient_matches_closed_formula=True, degree=len(poly(p))-1,
                   delta_j_nonzero_checked=True, actual_rho_is_rational_by_premise=True)


def native_decision(evidence):
    n = evidence['distinct_real_roots']
    require(type(n) is int and 0 <= n <= 3, 'decision-count-domain')
    return dict(disposition='certified-record-contrast' if n == 0 else 'unresolved-real-roots-remain',
                distinct_real_roots=n, no_real_root_on_admissible_interval=n == 0,
                restricted_27_child_repair_rejected=n == 0,
                rational_root_exclusion_claimed=n == 0,
                rational_roots_remaining_asserted=False,
                actual_scale_root_asserted=False, positive_repair_asserted=False,
                all_positive_extensions_rejected=False, actual_scale_computed=False)


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


def fixtures():
    result = []
    for name, coefficients, radius, expected in FIXTURES:
        evidence = root_certificate([rational(q) for q in coefficients], rational(radius))
        require(evidence['distinct_real_roots'] == expected, 'fixture-root-count-'+name)
        result.append(dict(name=name, expected_distinct_real_roots=expected,
                           root_certificate=evidence, decision=native_decision(evidence),
                           native_model_claimed=False))
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


REFUSAL_NAMES = (
    'duplicate-json', 'decimal-json', 'nonfinite-json', 'unreduced-rational',
    'boolean-rational', 'rational-text-bound', 'integer-bit-bound', 'boolean-polynomial',
    'polynomial-degree', 'root-degree', 'zero-polynomial', 'zero-radius',
    'zero-polynomial-divisor', 'zero-rational-divisor', 'boolean-power',
    'wrong-size-ri88', 'wrong-hash-ri88', 'wrong-size-ri103', 'wrong-hash-ri103',
    'wrong-size-ri94', 'wrong-hash-ri94', 'extra-ri88-field', 'missing-ri88-field',
    'wrong-ri88-source', 'wrong-dependencies', 'wrong-admission', 'wrong-prefix',
    'boolean-coverage', 'boolean-record', 'extra-record', 'boolean-order',
    'boolean-slot', 'missing-slot', 'duplicate-slot', 'nonpositive-slot',
    'reordered-rows', 'missing-selected-row', 'duplicate-selected-row',
    'changed-locality', 'changed-twin', 'lookup-C5', 'lookup-q6', 'lookup-q7',
    'lookup-record', 'lookup-slot', 'zero-delta-j', 'changed-radius',
    'wrong-fixed-division', 'boolean-decision', 'extra-saved-field',
    'missing-saved-field', 'saved-boolean-record', 'saved-missing-row',
    'saved-root-count', 'saved-endpoint-sign', 'saved-gcd', 'saved-quotient',
    'saved-actual-scale-claim', 'saved-global-rejection', 'saved-positive-repair',
    'saved-radius', 'saved-square-free-quotient', 'saved-reconstruction',
    'saved-sturm-chain', 'saved-negative-remainder', 'saved-upper-inclusion',
    'saved-lower-exclusion', 'saved-variations', 'saved-square-free-remainder',
    'saved-noncanonical',
)


def refusal_controls(data, raw_inputs, rows, witness):
    passed = []
    def expect(name, reason, action):
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
    for role in ('ri88', 'ri103', 'ri94'):
        expect('wrong-size-'+role, 'input-size-'+role,
               lambda role=role: input_bytes(role, raw_inputs[role][:-1]))
        expect('wrong-hash-'+role, 'input-hash-'+role,
               lambda role=role: input_bytes(role, b'!'+raw_inputs[role][1:]))
    expect('extra-ri88-field', 'ri88-fields', lambda: provenance(dict(data, extra=None)))
    expect('missing-ri88-field', 'ri88-fields', lambda: provenance({k: v for k, v in data.items() if k != 'prefix'}))
    expect('wrong-ri88-source', 'ri88-source', lambda: provenance(altered(data, ['checker_sha256'], '0'*64)))
    expect('wrong-dependencies', 'ri88-dependencies', lambda: provenance(altered(data, ['dependencies'], {})))
    expect('wrong-admission', 'ri88-admission', lambda: provenance(altered(data, ['admission', 'epsilon'], '1/8')))
    expect('wrong-prefix', 'ri88-actual-prefix', lambda: provenance(altered(data, ['prefix', 'canonical_lex_stages'], True)))
    expect('boolean-coverage', 'ri88-coverage', lambda: provenance(altered(data, ['coverage', 'held_marked_rows'], True)))
    expect('boolean-record', 'held-record-domain', lambda: held_entry(altered(rows[0], ['record'], False)))
    expect('extra-record', 'held-record-domain', lambda: held_entry(altered(rows[0], ['record'], 2)))
    expect('boolean-order', 'held-order-types', lambda: held_entry(altered(rows[0], ['order', 0], False)))
    expect('boolean-slot', 'held-slot-types', lambda: held_entry(altered(rows[0], ['probabilities', 0, 0], False)))
    expect('missing-slot', 'held-slot-inventory', lambda: held_entry(altered(rows[0], ['probabilities'], rows[0]['probabilities'][:-1])))
    expect('duplicate-slot', 'held-slot-inventory', lambda: held_entry(altered(rows[0], ['probabilities', 1, 0], 0)))
    expect('nonpositive-slot', 'held-positive-normalized', lambda: held_entry(altered(rows[0], ['probabilities', 0, 1], '0')))
    reordered = clone(data)
    indices = [i for i, e in enumerate(reordered['held_rows']) if e['order'] == list(C3) and e['record'] in (0, 1)]
    reordered['held_rows'][indices[0]], reordered['held_rows'][indices[1]] = reordered['held_rows'][indices[1]], reordered['held_rows'][indices[0]]
    expect('reordered-rows', 'selected-row-order', lambda: extract(reordered))
    missing = clone(data)
    missing['held_rows'][indices[0]]['record'] = 2
    expect('missing-selected-row', 'selected-row-completeness', lambda: extract(missing))
    duplicate = clone(data)
    duplicate['held_rows'][indices[1]] = clone(duplicate['held_rows'][indices[0]])
    expect('duplicate-selected-row', 'duplicate-selected-row', lambda: extract(duplicate))
    for name, order, slot, reason in (
        ('changed-locality', C3, 0, 'held-empty-locality'),
        ('changed-twin', H5, 4, 'held-twin-symmetry'),
    ):
        modified = clone(data)
        row = next(e['probabilities'] for e in modified['held_rows'] if e['order'] == list(order) and e['record'] == 0)
        transfer = div(rational(row[slot][1]), Q(2))
        row[slot][1] = str(transfer)
        row[-1][1] = str(add(rational(row[-1][1]), transfer))
        expect(name, reason, lambda modified=modified: extract(modified))
    for label, order in (('C5', (0, 1, 3, 7, 15)), ('q6', (0, 1, 3, 7, 7, 7)), ('q7', T1)):
        expect('lookup-'+label, 'lookup-order-domain', lambda order=order: lookup({}, order, 0, 0))
    expect('lookup-record', 'lookup-record-domain', lambda: lookup({}, C3, 2, 0))
    expect('lookup-slot', 'lookup-slot-domain', lambda: lookup({}, C3, 0, 2))
    same = (Q(1), Q(1), Q(1), Q(1))
    expect('zero-delta-j', 'accepted-delta-j-nonzero', lambda: contrast([same, same], [], Q(1)))
    other = (Q(1), Q(2), Q(1), Q(1))
    expect('changed-radius', 'fixed-radius', lambda: contrast([same, other], [], Q(1)))
    expect('wrong-fixed-division', 'contrast-fixed-division',
           lambda: contrast([same, other], [[Q(0)]*5, [Q(0)]*5], Q(1, 4)))
    expect('boolean-decision', 'decision-count-domain', lambda: native_decision(dict(distinct_real_roots=True)))
    expect('extra-saved-field', 'saved-fields', lambda: strict_equal(dict(witness, extra=None), witness))
    expect('missing-saved-field', 'saved-fields', lambda: strict_equal({k: v for k, v in witness.items() if k != 'inputs'}, witness))
    expect('saved-boolean-record', 'saved-exact-type', lambda: strict_equal(altered(witness, ['records', 0, 'record'], False), witness))
    expect('saved-missing-row', 'saved-list-coverage', lambda: strict_equal(altered(witness, ['inputs', 'held_rows'], rows[:-1]), witness))
    for name, path, value in (
        ('saved-root-count', ['root_certificate', 'distinct_real_roots'], 4),
        ('saved-endpoint-sign', ['root_certificate', 'upper', 'signs', 0], 2),
        ('saved-gcd', ['root_certificate', 'gcd_monic', 0], 'not-a-rational'),
        ('saved-quotient', ['contrast', 'P_padded', 1], '0'),
        ('saved-actual-scale-claim', ['decision', 'actual_scale_computed'], True),
        ('saved-global-rejection', ['decision', 'all_positive_extensions_rejected'], True),
        ('saved-positive-repair', ['decision', 'positive_repair_asserted'], True),
        ('saved-radius', ['scale_domain', 'R'], '1'),
        ('saved-square-free-quotient', ['root_certificate', 'square_free_quotient', 0], 'not-a-rational'),
        ('saved-reconstruction', ['root_certificate', 'reconstructed_polynomial', 0], 'not-a-rational'),
        ('saved-sturm-chain', ['root_certificate', 'sturm_chain', 0, 0], 'not-a-rational'),
        ('saved-negative-remainder', ['fixtures', 7, 'root_certificate', 'sturm_divisions', 0, 'next_term', 0], 'not-a-rational'),
        ('saved-upper-inclusion', ['root_certificate', 'upper_included'], False),
        ('saved-lower-exclusion', ['root_certificate', 'lower_excluded'], False),
        ('saved-variations', ['root_certificate', 'lower', 'variations'], 99),
    ):
        expect(name, 'saved-exact-value', lambda path=path, value=value: strict_equal(altered(witness, path, value), witness))
    expect('saved-square-free-remainder', 'saved-list-coverage',
           lambda: strict_equal(altered(witness, ['root_certificate', 'square_free_remainder'], ['1']), witness))
    expect('saved-noncanonical', 'saved-canonical-bytes',
           lambda: verify_saved((canonical(witness)+'\n\n').encode('ascii'), witness))
    require(tuple(item['name'] for item in passed) == REFUSAL_NAMES
            and len(set(REFUSAL_NAMES)) == len(REFUSAL_NAMES) == 70, 'refusal-ordered-inventory')
    return passed


def build(data, source_hash):
    held, rows = extract(data)
    coefficients, U, records = [], [], []
    for record in (0, 1):
        terms, u, evidence = record_formula(held, record)
        coefficients.append(terms)
        U.append(u)
        records.append(evidence)
    E = [row[0] for row in coefficients]
    radius = radius_for(E)
    p, contrast_evidence = contrast(coefficients, U, radius)
    root_evidence = root_certificate(p, radius)
    margins = [sub(Q(1), mul(radius, e)) for e in E]
    require(all(calc('cmp', margin, Q(1, 2)) > 0 for margin in margins), 'radius-full-margin')
    witness = dict(
        schema=SCHEMA,
        accepted_inputs={'ri88': dict(bytes=PINS['ri88'][0], sha256=PINS['ri88'][1])},
        accepted_sources={role: dict(bytes=PINS[role][0], sha256=PINS[role][1]) for role in ('ri103', 'ri94')},
        inputs=dict(held_rows=rows, selected_order=['C3:0', 'C3:1', 'C4:0', 'C4:1', 'H5:0', 'H5:1'],
                    prefix_replayed=False, H_or_z_values_read=False),
        selected_parent=list(T1), records=records,
        scale_domain=dict(R=str(radius), selected_E=[str(e) for e in E], interval='0<rho<=R',
                          lower_full_margins_at_R=[str(q) for q in margins],
                          actual_rho_evaluated=False, amplitude='1/4', seed_unchanged=True),
        contrast=contrast_evidence, root_certificate=root_evidence,
        decision=native_decision(root_evidence),
        coverage=dict(held_rows=6, held_probability_slots=32, records=2,
                      H_or_z_arithmetic_values=0, new_q6_q7_rows=0, native_polynomial_degree_cap=3),
        limitations=dict(real_roots_do_not_imply_rational_roots=True,
                         roots_in_outer_interval_do_not_locate_actual_scale=True,
                         complete_all_size_extension_not_claimed=True,
                         QM_geometry_gravity_derivation_not_claimed=True,
                         restricted_candidate_only=True, external_custody_required=True),
        arithmetic_limits=dict(input_rational_bits=INPUT_BITS, working_rational_bits=MAX_BITS,
                               transient_integer_bits=2*MAX_BITS+2, counted_operations=MAX_OPS,
                               rational_text_characters=MAX_TEXT, output_bytes=MAX_OUTPUT,
                               active_child_seconds=MAX_SECONDS, resident_bytes=MAX_BYTES),
        checker_sha256=source_hash, fixtures=fixtures())
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
    # Bound decimal conversion explicitly; covers 1,048,576-bit working values.
    sys.set_int_max_str_digits(2*MAX_BITS)
    source = Path(__file__).resolve()
    source_bytes = read_bounded(source, MAX_OUTPUT)
    source_hash = sha256(source_bytes).hexdigest()
    parent = source.parent.parent
    paths = {
        'ri88': parent/'native_growth_four_vertex_cap_check_v1'/'CERTIFICATE.json',
        'ri103': parent/'native_growth_full_birth_repair_v1'/'REPAIR.md',
        'ri94': parent/'native_growth_relative_amplitude_v1'/'AMPLITUDE.md',
    }
    raw_inputs = {role: read_bounded(paths[role], PINS[role][0]) for role in ('ri88', 'ri103', 'ri94')}
    for role in ('ri88', 'ri103', 'ri94'):
        input_bytes(role, raw_inputs[role])
    data = load_json(raw_inputs['ri88'])  # All three pins verified BEFORE this parse.
    witness, rows = build(data, source_hash)
    witness['refusal_controls'] = refusal_controls(data, raw_inputs, rows, witness)
    encoded = (canonical(witness)+'\n').encode('ascii')
    require(len(encoded) <= MAX_OUTPUT, 'output-byte-budget')
    saved_raw = None
    saved_path = source.with_name('CERTIFICATE.json')
    if not sys.argv[1:]:
        saved_raw = read_bounded(saved_path, MAX_OUTPUT)
        verify_saved(saved_raw, witness)
    for role in ('ri88', 'ri103', 'ri94'):
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
                           witness_sha256=sha256(encoded).hexdigest(),
                           decision=witness['decision'], fixture_count=len(witness['fixtures']),
                           refusal_count=len(witness['refusal_controls']),
                           producer_replay_is_independent_audit=False)
            print(canonical(summary), flush=True)
        budget()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
