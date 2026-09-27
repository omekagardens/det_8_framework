#!/usr/bin/env python3
"""RI128 independently expressed saved reconstruction. SOURCE ONLY; UNEXECUTED.

This consumer uses normalized integer pairs, sparse coefficient dictionaries,
individual proper-ideal sums and explicit cleared coefficients. It never
imports the producer or a scientific helper. No execution authority is given
by this file. Final producer pins and declarations must be bound before use.
"""
from hashlib import sha256
from math import gcd
from pathlib import Path
import json
import os
import re
import resource
import signal
import stat
import sys
import time

PIN = {
    'ri88': (1828149, 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'),
    'ri88_root': (2783, '15cedc2d7683734450963dc147e2a0deef59f0713a6b9898d806d9dd1240bea6'),
    'ri122_root': (15477, '162949e859b16211106e3c0213a29db290d52ffc7bf7fdaf411d20387a2fdbbc'),
    'ri124_root': (3645, '85b6d5c84139b05d5a18f89614a415ecde962efc429092b914e6f2da33ccde9c'),
    'ri127_root': (4071, '66d274815c101015256ba506f3e6a125375797b1b7946831159d39692ffebd77'),
}
PRODUCER_PIN = (27288, '73bb32320be53c38cf85889ca108229d9c2ea2d79b27814ac258eb4b6f133e38')
INPUT_BITS, WORK_BITS, TRANSIENT_BITS = 32768, 1048576, 2097154
MAX_OPS, MAX_TEXT, MAX_BYTES = 200000, 20000, 8388608
SECONDS, RSS_BYTES = 120, 536870912
MAX_AGGREGATE_BYTES = 8 * MAX_BYTES
ZERO, ONE = (0, 1), (1, 1)
START, OPS = None, 0
C3, C4, C5, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 7)
ORDERS = (C3, C4, C5, H5)
COUNTS = (8, 8, 16, 8)
IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 31),
          (0, 1, 3, 7, 15, 23, 31))
FIELDS = ('schema', 'checker_sha256', 'input_identities', 'held_rows', 'seed',
          'profiles', 'scalars', 'domain', 'targets', 'decision', 'fixtures',
          'refusal_controls', 'limits', 'limitations')
RI88_FIELDS = ('admission', 'checker_sha256', 'compact_rows', 'coverage',
               'dependencies', 'design_sha256', 'domain', 'exact_decision',
               'expanded_rows', 'held_rows', 'parameters', 'prefix',
               'refusal_controls', 'schema', 'structure', 'transported_audit',
               'width_target')
DEPENDENCIES = {
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
}
CAPS = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 3), (0, 0, 1, 1),
        (0, 0, 1, 2), (0, 0, 1, 3), (0, 0, 1, 5), (0, 0, 3, 3),
        (0, 1, 1, 1), (0, 1, 1, 3), (0, 1, 3, 3))
WIDTHS = (4, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2)
SUPPORT = tuple(C3 + tuple(7 + 8 * p for p in cap) for cap in CAPS)
FIXTURES = (
    ('positive-constant', ('1',), (), '1', '1/4', 0, 'UNIFORM_STRICT_POSITIVE'),
    ('negative-constant', ('-1',), (), '1', '1/4', 0, 'UNIFORM_NONPOSITIVE'),
    ('identically-zero', (), (), '1', '1/4', 3, 'UNIFORM_NONPOSITIVE'),
    ('excluded-lower-zero-conservative', ('0', '1'), (), '1', '1/4', 1, 'UNRESOLVED'),
    ('included-upper-zero', ('-1', '1'), (), '1', '1/4', 1, 'UNIFORM_NONPOSITIVE'),
    ('mixed-sign-domain', ('-1', '2'), (), '1', '1/4', 1, 'UNRESOLVED'),
    ('affine-endpoint-zero', ('-1',), ('4',), '1', '1/4', 0, 'UNIFORM_NONPOSITIVE'),
    ('affine-endpoint-crossing', ('-1',), ('8',), '1', '1/4', 0, 'UNRESOLVED'),
    ('affine-positive', ('1',), ('4',), '1', '1/4', 0, 'UNIFORM_STRICT_POSITIVE'),
    ('affine-lower-zero-conservative', ('0',), ('4',), '1', '1/4', 0, 'UNRESOLVED'),
    ('degree-drop-zero-padding', ('-1', '0', '0', '0', '0', '0'), (), '1', '1/4', 5, 'UNIFORM_NONPOSITIVE'),
    ('quintic-upper-zero', ('-1', '0', '0', '0', '0', '1'), (), '1', '1/4', 5, 'UNIFORM_NONPOSITIVE'),
    ('cubic-upper-zero', ('-1', '0', '0', '1'), (), '1', '1/4', 3, 'UNIFORM_NONPOSITIVE'),
    ('negative-square-conservative', ('-1', '2', '-1'), (), '1', '1/4', 2, 'UNRESOLVED'),
    ('nonunit-domain', ('-1', '2'), (), '1/4', '1/4', 1, 'UNIFORM_NONPOSITIVE'),
)
BASE_CONTROL_PAIRS = (
    ('duplicate-json', 'duplicate-key'), ('float-json', 'noninteger-json'), ('nan-json', 'noninteger-json'),
    ('rational-boolean', 'rational-text-type'), ('rational-unreduced', 'rational-canonical'),
    ('rational-text-over', 'rational-text-budget'), ('rational-bits-over', 'rational-bits'),
    ('division-zero', 'zero-divisor'), ('power-boolean', 'power-domain'),
    ('degree-six', 'polynomial-degree'), ('boolean-coefficient', 'rational-type'),
    ('zero-radius', 'box-positive'), ('zero-y', 'box-positive'),
    ('row-extra', 'row-fields'), ('row-order-boolean', 'row-order'), ('row-record-boolean', 'row-record'),
    ('slot-boolean', 'slot-types'), ('slot-missing', 'slot-inventory'), ('slot-reordered', 'slot-inventory'),
    ('row-zero', 'row-positive'), ('row-sum', 'row-normalized'),
    ('seed-support-boolean', 'seed-support'), ('seed-short', 'seed-vector'), ('seed-large', 'seed-bound'),
    ('saved-type', 'saved-type'), ('saved-fields', 'saved-fields'), ('saved-value', 'saved-value'),
    ('saved-noncanonical', 'saved-bytes'), ('decision-missing', 'decision-targets'),
    ('decision-invalid', 'decision-status'),
    ('strict-zero-promotion', 'saved-value'),
    ('slot-extra', 'slot-inventory'),
    ('rational-output-over', 'rational-output-text-budget'),
)
CONTROL_PAIRS = (BASE_CONTROL_PAIRS
                 + tuple((kind + '-' + role, 'input-' + kind + '-' + role)
                         for role in PIN for kind in ('size', 'hash'))
                 + tuple(('status-' + role, 'root-status-' + role) for role in
                         ('ri88_root', 'ri122_root', 'ri124_root', 'ri127_root'))
                 + tuple(('section-' + name, 'saved-type') for name in FIELDS)
                 + tuple((name, 'saved-value') for name in
                         ('saved-q', 'saved-domain', 'saved-domain-shrunk', 'saved-target-a', 'saved-target-b',
                          'saved-degree', 'saved-upper', 'saved-lower', 'saved-status', 'saved-overclaim')))
LIMITS = {'seconds': 120, 'group_rss_bytes': 536870912, 'scientific_bytes': 8388608,
          'input_bits': 32768, 'working_bits': 1048576, 'transient_bits': 2097154,
          'operations': 200000, 'rational_text': 20000}
LIMITATIONS = {'conditional_on_accepted_record_pattern': True,
               'coefficient_bounds_are_sufficient_not_complete': True,
               'domain_is_containing_not_actual_scales': True,
               'two_local_intervals_not_full_H30': True,
               'outer_custody_and_fresh_qualification_required': True,
               'physical_or_all_size_claim': False}


class AuditFailure(RuntimeError):
    pass


def require(condition, reason):
    if not condition:
        raise AuditFailure(reason)


def budget():
    require(START is None or time.monotonic() - START <= SECONDS, 'wall-budget')
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((rss if sys.platform == 'darwin' else rss * 1024) <= RSS_BYTES, 'rss-budget')


def tick():
    global OPS
    OPS += 1
    require(OPS <= MAX_OPS, 'operation-budget')
    budget()


def bounded(value, bits=TRANSIENT_BITS):
    require(type(value) is int and abs(value).bit_length() <= bits, 'integer-bit-domain')
    return value


def rational(n, d=1, bits=WORK_BITS):
    bounded(n)
    bounded(d)
    require(d != 0, 'zero-denominator')
    if d < 0:
        n, d = -n, -d
    common = gcd(abs(n), d)
    n, d = n // common, d // common
    bounded(n, bits)
    bounded(d, bits)
    return n, d


def checked(q):
    require(type(q) is tuple and len(q) == 2
            and all(type(v) is int for v in q), 'rational-pair-type')
    bounded(q[0], WORK_BITS)
    bounded(q[1], WORK_BITS)
    require(q[1] > 0 and gcd(abs(q[0]), q[1]) == 1, 'normalized-rational-pair')
    return q


def qtext(q):
    n, d = checked(q)
    value = str(n) if d == 1 else str(n) + '/' + str(d)
    require(len(value) <= MAX_TEXT, 'rational-output-text-bound')
    return value


def parse_q(value):
    require(type(value) is str and len(value) <= MAX_TEXT, 'rational-text-domain')
    require(re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', value) is not None,
            'rational-syntax')
    parts = value.split('/')
    q = rational(int(parts[0]), int(parts[1]) if len(parts) == 2 else 1, INPUT_BITS)
    require(qtext(q) == value, 'noncanonical-rational')
    return q


def add(a, b):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    common = gcd(ad, bd)
    left, right = ad // common, bd // common
    return rational(bounded(an * right + bn * left), bounded(ad * right))


def negative(q):
    tick()
    n, d = checked(q)
    return -n, d


def sub(a, b):
    return add(a, negative(b))


def mul(a, b):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    ca, cb = gcd(abs(an), bd), gcd(abs(bn), ad)
    return rational(bounded((an // ca) * (bn // cb)),
                    bounded((ad // cb) * (bd // ca)))


def div(a, b):
    tick()
    bn, bd = checked(b)
    require(bn != 0, 'zero-rational-divisor')
    return mul(a, rational(bd, bn))


def compare(a, b=ZERO):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    left, right = bounded(an * bd), bounded(bn * ad)
    return (left > right) - (left < right)


def power(q, exponent):
    require(type(exponent) is int and 0 <= exponent <= 6, 'power-exponent-domain')
    checked(q)
    result = ONE
    for _ in range(exponent):
        result = mul(result, q)
    return result


def total(values):
    result = ZERO
    for q in values:
        result = add(result, q)
    return result


def poly(values):
    require(type(values) is dict and len(values) <= 6, 'sparse-polynomial-domain')
    normalized = {}
    for exponent, value in values.items():
        require(type(exponent) is int and 0 <= exponent <= 5, 'sparse-degree-domain')
        checked(value)
        if value != ZERO:
            normalized[exponent] = value
    return normalized


def as_poly(coefficients):
    require(type(coefficients) in (tuple, list) and len(coefficients) <= 6,
            'coefficient-list-domain')
    return poly(dict(enumerate(coefficients)))


def poly_add(a, b):
    a, b = poly(a), poly(b)
    return poly({i: add(a.get(i, ZERO), b.get(i, ZERO)) for i in sorted(set(a) | set(b))})


def poly_scale(p, q):
    checked(q)
    return poly({i: mul(c, q) for i, c in poly(p).items()})


def degree(p):
    p = poly(p)
    return max(p) if p else -1


def padded(p, cap):
    p = poly(p)
    require(type(cap) is int and 0 <= cap <= 5 and degree(p) <= cap, 'padded-degree-domain')
    return [qtext(p.get(i, ZERO)) for i in range(cap + 1)]


def endpoint(p, x, y, cap):
    p = poly(p)
    require(type(cap) is int and 0 <= cap <= 5 and degree(p) <= cap, 'endpoint-degree-domain')
    lower = upper = p.get(0, ZERO)
    terms = []
    for exponent in range(1, cap + 1):
        coefficient = p.get(exponent, ZERO)
        term = mul(coefficient, power(x, exponent))
        terms.append(qtext(term))
        sign = compare(coefficient)
        if sign < 0:
            lower = add(lower, term)
        elif sign > 0:
            upper = add(upper, term)
    require(compare(lower, upper) <= 0, 'inverted-envelope')
    return {'y': qtext(y), 'coefficients_padded': padded(p, cap),
            'degree': degree(p), 'power_terms': terms,
            'lower': qtext(lower), 'upper': qtext(upper)}, lower, upper


def target(label, a, b, x, y, cap):
    require(type(label) is str and bool(label), 'target-label-domain')
    require(type(cap) is int and 0 <= cap <= 5, 'target-cap-domain')
    require(compare(x) > 0 and compare(y) > 0, 'target-box-domain')
    a, b = poly(a), poly(b)
    require(degree(a) <= cap and degree(b) <= cap, 'target-degree-domain')
    second = poly_add(a, poly_scale(b, y))
    zero_evidence, lower_zero, upper_zero = endpoint(a, x, ZERO, cap)
    top_evidence, lower_top, upper_top = endpoint(second, x, y, cap)
    nonpositive = compare(upper_zero) <= 0 and compare(upper_top) <= 0
    positive = compare(lower_zero) > 0 and compare(lower_top) > 0
    require(not (nonpositive and positive), 'conflicting-sign-certificates')
    status = ('UNIFORM_NONPOSITIVE' if nonpositive else
              'UNIFORM_STRICT_POSITIVE' if positive else 'UNRESOLVED')
    return {'label': label, 'degree_cap': cap, 'a_padded': padded(a, cap),
            'b_padded': padded(b, cap), 'degree_a': degree(a), 'degree_b': degree(b),
            'endpoints': [zero_evidence, top_evidence], 'status': status}


def decision(targets):
    require(type(targets) is list and len(targets) == 2
            and [entry.get('label') for entry in targets] == ['j2', 'j3'],
            'decision-target-inventory')
    allowed = ('UNIFORM_NONPOSITIVE', 'UNIFORM_STRICT_POSITIVE', 'UNRESOLVED')
    require(all(entry.get('status') in allowed for entry in targets), 'decision-status-domain')
    nonpositive = [entry['label'] for entry in targets if entry['status'] == allowed[0]]
    positive = [entry['label'] for entry in targets if entry['status'] == allowed[1]]
    rejected = bool(nonpositive)
    local = not rejected and len(positive) == 2
    return {'disposition': 'REJECT_FIXED_H30' if rejected else 'LOCAL_INTERVALS_ONLY' if local else 'UNRESOLVED',
            'nonpositive_targets': nonpositive, 'strict_positive_targets': positive,
            'fixed_H30_rejected': rejected, 'two_local_intervals_certified': local,
            'full_H30_feasibility': False, 'actual_scales_selected': False}


def keys(value, names, label):
    require(type(value) is dict and set(value) == set(names), 'fields:' + label)


def exact(actual, expected, label='certificate'):
    require(type(actual) is type(expected), 'exact-type:' + label)
    if type(expected) is dict:
        keys(actual, expected, label)
        for name in expected:
            exact(actual[name], expected[name], label + '.' + name)
    elif type(expected) is list:
        require(len(actual) == len(expected), 'exact-list-length:' + label)
        for index, (a, b) in enumerate(zip(actual, expected)):
            exact(a, b, label + '[' + str(index) + ']')
    else:
        require(actual == expected, 'exact-value:' + label)


def decode(raw, allow_decimal_metadata=False):
    require(type(raw) is bytes and 0 < len(raw) <= MAX_BYTES, 'json-body-bound')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate-json-key')
            result[key] = value
        return result
    def reject(_value):
        raise AuditFailure('noninteger-json-number')
    def integer(value):
        require(len(value) <= MAX_TEXT, 'json-integer-text-bound')
        return int(value)
    def decimal_metadata(value):
        # Historical root resource durations are authenticated metadata, not
        # scientific operands. Preserve their lexemes without float arithmetic.
        require(allow_decimal_metadata and len(value) <= MAX_TEXT, 'noninteger-json-number')
        return ('decimal-metadata-lexeme', value)
    return json.loads(raw, object_pairs_hook=pairs, parse_int=integer,
                      parse_float=decimal_metadata, parse_constant=reject)


def canonical(value):
    raw = (json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    require(len(raw) <= MAX_BYTES, 'output-byte-bound')
    budget()
    return raw


def identity(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def accepted_premises(objects):
    expected = (
        ('ri88_root', 'ri88-root-finite-result-adjudication-v1', 'accepted_positive_finite_width_bias'),
        ('ri122_root', 'ri122-root-final-native-mathematical-adjudication-v1',
         'ACCEPT_FIXED_28_CHILD_POSITIVE_REPAIR_OBSTRUCTION'),
        ('ri124_root', 'ri124-root-final-proof-adjudication-v1',
         'ACCEPT_CONDITIONAL_ANALYTIC_THEOREM_AND_COMPLETE_CLOSURE_ONLY'),
        ('ri127_root', 'ri127-root-final-proof-adjudication-v1',
         'ACCEPT_COMPLETE_CONNECTED_CANCELLATION_AND_CONDITIONAL_STRICT_LOCAL_REDUCTION'),
    )
    for role, schema, status in expected:
        value = objects[role]
        require(type(value) is dict and value.get('schema') == schema
                and value.get('status') == status,
                'accepted-premise:' + role)
    r88 = objects['ri88_root']
    require(type(r88.get('certificate')) is dict
            and r88['certificate'].get('bytes') == PIN['ri88'][0]
            and type(r88['certificate'].get('bytes')) is int
            and r88['certificate'].get('sha256') == PIN['ri88'][1], 'accepted-seed-certificate-binding')
    result88 = r88.get('result')
    require(type(result88) is dict and result88.get('epsilon') == '1/4'
            and result88.get('h_range') == ['3/4', '5/4']
            and result88.get('all11_coordinates_nonzero') is True, 'accepted-seed-scope')
    r122, r124, r127 = (objects[k] for k in ('ri122_root', 'ri124_root', 'ri127_root'))
    require(r122.get('mathematical_result_accepted') is True
            and r122.get('held_rows') == 40 and type(r122.get('held_rows')) is int
            and r122.get('held_probability_slots') == 224
            and type(r122.get('held_probability_slots')) is int
            and r122.get('all_positive_extensions_rejected') is False,
            'accepted-complete-pattern')
    require(r124.get('positive_feasibility_accepted') is False
            and r124.get('new_support_obstruction_accepted') is False
            and r124.get('execution_admitted') is False, 'accepted-H30-conditional-scope')
    require(r127.get('actual_C_signs_decided') is False
            and r127.get('actual_connected_local_feasibility_accepted') is False
            and r127.get('H30_obstruction_accepted') is False
            and r127.get('positive_H30_accepted') is False
            and r127.get('execution_admitted') is False, 'accepted-strict-sign-scope')


def selected_rows(data):
    keys(data, RI88_FIELDS, 'RI88')
    require(data['schema'] == 'ri88-four-vertex-cap-v1'
            and data['checker_sha256'] == '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
            and data['design_sha256'] == 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a',
            'RI88-source')
    exact(data['dependencies'], DEPENDENCIES, 'RI88-dependencies')
    admission, prefix, coverage = data['admission'], data['prefix'], data['coverage']
    require(type(admission) is dict and admission.get('epsilon') == '1/4'
            and admission.get('later_h_prescribed') is False
            and admission.get('numerical_a6_evaluated') is False, 'RI88-admission')
    require(type(prefix) is dict
            and prefix.get('problem_sha256') == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
            and prefix.get('actual_probability_manifest_sha256') == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
            and type(prefix.get('canonical_lex_stages')) is int
            and prefix['canonical_lex_stages'] == 69, 'RI88-prefix')
    require(type(coverage) is dict and type(coverage.get('held_marked_rows')) is int
            and coverage['held_marked_rows'] == 40
            and type(coverage.get('held_probability_slots')) is int
            and coverage['held_probability_slots'] == 224, 'RI88-coverage')
    rows = data['held_rows']
    require(type(rows) is list and len(rows) == 40, 'held-inventory-count')
    expected = [(order, record) for order, count in zip(ORDERS, COUNTS) for record in range(count)]
    seen = []
    chosen, held = [], {}
    for row in rows:
        keys(row, ('order', 'record', 'probabilities'), 'held-entry')
        require(type(row['order']) is list and all(type(v) is int for v in row['order'])
                and type(row['record']) is int, 'held-key-types')
        key = (tuple(row['order']), row['record'])
        require(key in expected and key not in seen, 'held-key-inventory')
        seen.append(key)
        if key[1] not in (0, 1):
            continue  # No nonselected probability becomes an arithmetic operand.
        inventory = IDEALS[ORDERS.index(key[0])]
        slots = row['probabilities']
        require(type(slots) is list and len(slots) == len(inventory), 'selected-slot-count')
        require(all(type(slot) is list and len(slot) == 2 and type(slot[0]) is int
                    for slot in slots), 'selected-slot-types')
        require([slot[0] for slot in slots] == list(inventory), 'selected-slot-inventory')
        values = [parse_q(slot[1]) for slot in slots]
        require(all(compare(q) > 0 for q in values), 'selected-positive')
        require(total(values) == ONE, 'selected-normalization')
        held[key] = dict(zip(inventory, values))
        chosen.append(row)
    require(seen == expected, 'held-row-order')
    wanted = [(order, record) for order in ORDERS for record in (0, 1)]
    require(list(held) == wanted and len(chosen) == 8
            and sum(len(row['probabilities']) for row in chosen) == 44, 'selected-eight-forty-four')
    for order, inventory in zip(ORDERS, IDEALS):
        require(held[(order, 0)][0] == held[(order, 1)][0], 'selected-empty-locality')
        # With representatives 0/1, only an ideal omitting the least bit can
        # identify their restrictions. The complete record theorem is inherited.
        for ideal in inventory[:-1]:
            if not (ideal & 1):
                require(held[(order, 0)][ideal] == held[(order, 1)][ideal],
                        'selected-proper-locality')
    require(held[(C3, 0)][7] == held[(C3, 1)][7], 'selected-C3-full-equality')
    for record in (0, 1):
        require(held[(H5, record)][15] == held[(H5, record)][23], 'selected-twin-equality')
        left = mul(held[(C4, record)][7], held[(H5, record)][15])
        right = mul(held[(C4, record)][15], held[(C5, record)][7])
        require(left == right, 'selected-twin-diamond')
    return held, chosen


def selected_seed(data):
    structure = data['structure']
    require(type(structure) is dict and type(structure.get('ordered_support')) is list,
            'seed-support-domain')
    expected = [{'index': i, 'cap': list(cap), 'order': list(order), 'width': width}
                for i, (cap, order, width) in enumerate(zip(CAPS, SUPPORT, WIDTHS))]
    exact(structure['ordered_support'], expected, 'seed-ordered-support')
    decision_data = data['exact_decision']
    require(type(decision_data) is dict
            and decision_data.get('disposition') == 'positive-finite-width-bias',
            'accepted-seed-disposition')
    z = decision_data.get('z')
    require(type(z) is list and len(z) == 11 and all(type(q) is str for q in z)
            and z[0] == '1', 'seed-vector-shape')
    z2, z3 = parse_q(z[1]), parse_q(z[2])
    require(all(compare(q, rational(-1)) >= 0 and compare(q, ONE) <= 0 and q != ZERO
                for q in (z2, z3)), 'seed-selected-bound')
    return z2, z3


def profile(held, record):
    require(type(record) is int and record in (0, 1), 'profile-record-domain')
    rows = {order: held[(order, record)] for order in ORDERS}
    c, h, j = rows[C4][15], rows[H5][15], rows[H5][31]
    e, ell = rows[C5][15], rows[C5][31]
    m = div(power(h, 2), c)
    e_terms, e2_terms, c2_terms = [], [], []
    for ideal in (0, 1, 3, 7):
        a, b, g, d = (rows[order][ideal] for order in ORDERS[:2] + (H5, C5))
        e_terms.append(mul(a, power(div(g, b), 3)))
        e2_terms.append(div(mul(d, g), b))
        c2_terms.append(div(mul(mul(a, d), power(g, 3)), power(b, 4)))
    e2_terms.extend([div(mul(e, h), c), h, j, ell])
    c2_terms.append(mul(e, power(div(h, c), 2)))
    big_e = total(e_terms + [m, m, m, j, j, j])
    v = total(e_terms + [m, m, j])
    require(v == sub(sub(big_e, m), mul(rational(2), j)), 'V-two-expressions')
    e2, c2 = total(e2_terms), total(c2_terms)
    a2 = sub(add(big_e, mul(rational(2), e2)), j)
    b2 = total([m, m, j, j, ell])
    # Independently sum each of fourteen T2 and twelve T3 proper ideals.
    t2_ideals = [{3: term} for term in c2_terms]
    t2_ideals.extend([{2: m}, {2: m}, {2: j}, {2: j}, {1: j},
                      {0: ONE, 1: negative(big_e)}, {2: ell},
                      {0: ONE, 1: negative(e2)}, {0: ONE, 1: negative(e2)}])
    u2 = {}
    for p in t2_ideals:
        u2 = poly_add(u2, p)
    require(len(t2_ideals) == 14 and u2 == as_poly([rational(3), negative(a2), b2, c2]),
            'fourteen-ideal-U2-reconstruction')
    t3_ideals = [{2: term} for term in e_terms]
    t3_ideals.extend([{2: m}, {2: m}, {2: j}, {1: m}, {1: j}, {1: j},
                      {0: ONE, 1: negative(big_e)}, {0: ONE, 1: rational(-1)}])
    u3 = {}
    for p in t3_ideals:
        u3 = poly_add(u3, p)
    require(len(t3_ideals) == 12 and u3 == as_poly([rational(2), negative(add(ONE, v)), v]),
            'twelve-ideal-U3-reconstruction')
    r2, r3 = c2_terms[3], e_terms[3]
    values = {'E': big_e, 'V': v, 'A2': a2, 'B2': b2, 'C2': c2, 'r2': r2, 'r3': r3,
              'U2': u2, 'U3': u3, 'epsilon2': c2_terms[0], 'epsilon3': e_terms[0]}
    encoded = {'record': record, 'E_terms': [qtext(q) for q in e_terms],
               'c': qtext(c), 'h': qtext(h), 'j': qtext(j), 'm': qtext(m),
               'E': qtext(big_e), 'V': qtext(v),
               'E2_terms': [qtext(q) for q in e2_terms],
               'C2_terms': [qtext(q) for q in c2_terms],
               'A2': qtext(a2), 'B2': qtext(b2), 'C2': qtext(c2),
               'r2': qtext(r2), 'r3': qtext(r3)}
    return values, encoded


def fixture_evidence():
    evidence = []
    for name, a, b, x, y, cap, expected in FIXTURES:
        result = target(name, as_poly([parse_q(q) for q in a]),
                        as_poly([parse_q(q) for q in b]), parse_q(x), parse_q(y), cap)
        require(result['status'] == expected, 'fixture-sign:' + name)
        evidence.append({'name': name, 'a': list(a), 'b': list(b), 'X': x, 'Y': y,
                         'cap': cap, 'expected_status': expected, 'evidence': result})
    require(len(evidence) == 15 and len({row['name'] for row in evidence}) == 15,
            'fixture-inventory')
    return evidence


def reconstruct(objects):
    accepted_premises(objects)
    held, rows = selected_rows(objects['ri88'])
    z2, z3 = selected_seed(objects['ri88'])
    v0, p0 = profile(held, 0)
    v1, p1 = profile(held, 1)
    d2, d3, v = sub(v0['r2'], v1['r2']), sub(v0['r3'], v1['r3']), sub(v1['V'], v0['V'])
    require(all(compare(q) > 0 for q in (d2, d3, v)), 'native-positive-D2-D3-v')
    difference = poly_add(v0['U2'], poly_scale(v1['U2'], rational(-1)))
    require(difference.get(0, ZERO) == ZERO, 'U2-difference-zero-constant')
    q = poly({i - 1: coefficient for i, coefficient in difference.items() if i})
    require(degree(q) <= 2 and q.get(0, ZERO) == sub(v1['A2'], v0['A2'])
            and q.get(1, ZERO) == sub(v0['B2'], v1['B2'])
            and q.get(2, ZERO) == sub(v0['C2'], v1['C2']), 'q-from-complete-U2-difference')
    require(compare(q.get(0, ZERO)) > 0, 'accepted-positive-q-at-zero')
    radius = div(ONE, mul(rational(2), add(ONE, v0['E'] if compare(v0['E'], v1['E']) >= 0 else v1['E'])))
    quarter = rational(1, 4)
    require(compare(radius) > 0 and compare(radius, rational(1, 2)) < 0, 'original-radius-domain')
    x, y = (radius if compare(radius, quarter) <= 0 else quarter), quarter
    h2, h3 = add(v0['epsilon2'], v0['r2']), add(v0['epsilon3'], v0['r3'])
    q0, q1, q2 = (q.get(i, ZERO) for i in range(3))
    # Hand-expanded coefficients, not producer factored polynomial products.
    a2 = as_poly([mul(z2, q0), mul(z2, q1), add(mul(z2, q2), mul(rational(4), d2))])
    b2 = as_poly([ZERO, ZERO, mul(rational(-12), d2),
                  mul(rational(4), add(mul(h2, q0), mul(v0['A2'], d2))),
                  mul(rational(4), sub(mul(h2, q1), mul(v0['B2'], d2))),
                  mul(rational(4), sub(mul(h2, q2), mul(v0['C2'], d2)))])
    a3 = as_poly([mul(v, z3), sub(mul(rational(4), d3), mul(v, z3))])
    b3 = as_poly([ZERO, mul(rational(-8), d3),
                  mul(rational(4), add(mul(v, h3), mul(add(ONE, v0['V']), d3))),
                  mul(rational(-4), add(mul(v, h3), mul(v0['V'], d3)))])
    targets = [target('j2', a2, b2, x, y, 5), target('j3', a3, b3, x, y, 3)]
    result = {
        'schema': 'ri128-connected-strict-sign-v1', 'checker_sha256': PRODUCER_PIN[1],
        'input_identities': {role: {'bytes': pin[0], 'sha256': pin[1]} for role, pin in PIN.items()},
        'held_rows': rows,
        'seed': {'z2': qtext(z2), 'z3': qtext(z3), 'source_indices': [1, 2], 'reconstructed': False},
        'profiles': [p0, p1],
        'scalars': {'epsilon2': qtext(v0['epsilon2']), 'epsilon3': qtext(v0['epsilon3']),
                    'D2': qtext(d2), 'D3': qtext(d3), 'v': qtext(v), 'q_padded': padded(q, 2),
                    'U20_padded': padded(v0['U2'], 3), 'U30_padded': padded(v0['U3'], 2)},
        'domain': {'R': qtext(radius), 'X': qtext(x), 'Y': qtext(y),
                   'original': '0<rho<=R;0<s<1/2', 'certified': '0<rho<=min(R,1/4);0<s<=1/4',
                   'actual_scales_evaluated': False,
                   'containment_basis': 'RI127 outer bound; RI128 unique-maximum normalization'},
        'targets': targets, 'decision': decision(targets), 'fixtures': fixture_evidence(),
        'refusal_controls': [{'name': name, 'first_reason': reason} for name, reason in CONTROL_PAIRS],
        'limits': dict(LIMITS), 'limitations': dict(LIMITATIONS),
    }
    keys(result, FIELDS, 'reconstructed-certificate')
    return result


def source_pin(pin):
    require(type(pin) is tuple and len(pin) == 2 and type(pin[0]) is int
            and 0 < pin[0] <= MAX_BYTES and type(pin[1]) is str
            and re.fullmatch('[0-9a-f]{64}', pin[1]) is not None
            and pin[1] != '0' * 64, 'unbound-producer-source')
    return pin


def readiness():
    source_pin(PRODUCER_PIN)
    require(type(CONTROL_PAIRS) is tuple and len(CONTROL_PAIRS) == 71
            and len({name for name, _ in CONTROL_PAIRS}) == 71,
            'producer-control-declaration-inventory')
    require(all(type(item) is tuple and len(item) == 2
                and all(type(value) is str and bool(value) for value in item)
                for item in CONTROL_PAIRS), 'producer-control-declaration-types')


def saved_check(raw, expected):
    exact(decode(raw), expected)
    require(raw == canonical(expected), 'saved-canonical-bytes')


AUDITOR_REFUSALS = (
    ('duplicate-json', 'duplicate-json-key'),
    ('float-scientific-json', 'noninteger-json-number'),
    ('nan-json', 'noninteger-json-number'),
    ('boolean-rational', 'rational-text-domain'),
    ('unreduced-rational', 'noncanonical-rational'),
    ('zero-divisor', 'zero-rational-divisor'),
    ('boolean-exponent', 'power-exponent-domain'),
    ('degree-six', 'sparse-degree-domain'),
    ('zero-x-bound', 'target-box-domain'),
    ('zero-y-bound', 'target-box-domain'),
    ('boolean-cap', 'target-cap-domain'),
    ('missing-producer-pin', 'unbound-producer-source'),
    ('saved-type', 'exact-type:certificate.n'),
    ('saved-value', 'exact-value:certificate.n'),
    ('saved-bytes', 'saved-canonical-bytes'),
    ('strict-zero-promotion', 'exact-value:certificate.status'),
)


def own_refusal_checks():
    # These distinct fabricated checks run only during an admitted actual
    # consumer execution. Producer control declarations are never executed here.
    small = {'n': 1}
    zero = target('zero', {}, {}, ONE, rational(1, 4), 0)
    require(zero['status'] == 'UNIFORM_NONPOSITIVE', 'zero-is-not-positive')
    promoted = dict(zero, status='UNIFORM_STRICT_POSITIVE')
    actions = (
        lambda: decode(b'{"n":1,"n":2}'),
        lambda: decode(b'1.5'), lambda: decode(b'NaN'),
        lambda: parse_q(True), lambda: parse_q('2/4'),
        lambda: div(ONE, ZERO), lambda: power(ONE, True),
        lambda: poly({6: ONE}), lambda: target('bad-x', {}, {}, ZERO, ONE, 0),
        lambda: target('bad-y', {}, {}, ONE, ZERO, 0),
        lambda: target('bad-cap', {}, {}, ONE, ONE, True),
        lambda: source_pin(None),
        lambda: saved_check(b'{"n":true}\n', small),
        lambda: saved_check(b'{"n":2}\n', small),
        lambda: saved_check(b'{ "n":1 }\n', small),
        lambda: saved_check(canonical(promoted), zero),
    )
    require(len(actions) == len(AUDITOR_REFUSALS), 'auditor-refusal-inventory')
    outcomes = []
    for (name, expected), action in zip(AUDITOR_REFUSALS, actions):
        try:
            action()
        except AuditFailure as error:
            require(str(error) == expected, 'auditor-wrong-first-refusal:' + name)
        else:
            raise AuditFailure('auditor-missing-refusal:' + name)
        outcomes.append({'name': name, 'first_reason': expected})
    return outcomes


def file_signature(info):
    return info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns, info.st_ctime_ns


def literal_path(name):
    require(type(name) is str and name and '\x00' not in name
            and os.path.isabs(name) and os.path.normpath(name) == name, 'literal-absolute-path')
    p = Path(name)
    # Checking each component also excludes symlinks which happen to resolve
    # back to the same location. The runtime/host is separately owner-custodied.
    current = Path(p.anchor)
    for component in p.parts[1:]:
        current = current / component
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode), 'symlink-path-component')
        require(stat.S_ISREG(info.st_mode) if current == p else stat.S_ISDIR(info.st_mode),
                'path-component-type')
    require(str(p.resolve(strict=True)) == name, 'resolved-path-differs')
    return p


def snapshot(name, expected_pin=None):
    p = literal_path(name)
    before = p.lstat()
    require(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= MAX_BYTES, 'regular-bounded-file')
    if expected_pin is not None:
        source_pin(expected_pin)
        require(before.st_size == expected_pin[0], 'pinned-file-size')
    descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(descriptor)
        require(file_signature(opened) == file_signature(before), 'file-open-identity')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(MAX_BYTES + 1)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after = literal_path(name).lstat()
    require(file_signature(before) == file_signature(after_fd) == file_signature(after)
            and len(raw) == before.st_size, 'file-read-stability')
    ident = identity(raw)
    if expected_pin is not None:
        require(ident == {'bytes': expected_pin[0], 'sha256': expected_pin[1]}, 'pinned-file-hash')
    return raw, file_signature(after)


def emergency(error, postchecks):
    # No exhausted arithmetic timer or normal serialization check suppresses
    # these independently collected custody diagnostics. Never a disposition.
    def clipped(value):
        text = str(value)
        return text[:2048]
    checks = []
    for item in postchecks[:8]:
        checks.append({key: clipped(value) if type(value) is str else value
                       for key, value in item.items()})
    failure = {'schema': 'ri128-saved-audit-failure-v1', 'status': 'REFUSED',
               'error_type': type(error).__name__, 'error': clipped(error),
               'postchecks': checks, 'scientific_disposition_emitted': False}
    raw = (json.dumps(failure, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False) + '\n').encode('ascii')
    if len(raw) > 1048576:
        raw = b'{"schema":"ri128-saved-audit-failure-v1","status":"REFUSED","diagnostic_overflow":true}\n'
    sys.stderr.buffer.write(raw)
    sys.stderr.buffer.flush()


def audit():
    own = os.path.abspath(__file__)
    directory = os.path.dirname(own)
    files = [('auditor', own, None),
             ('producer', os.path.join(directory, 'check.py'), PRODUCER_PIN)]
    files.extend((role, os.path.join(directory, 'inputs', role + '.json'), pin)
                 for role, pin in PIN.items())
    files.append(('certificate', os.path.join(directory, 'CERTIFICATE.json'), None))
    require(len(files) == 8 and len({name for _, name, _ in files}) == 8, 'eight-protected-paths')
    captures, postchecks, own_checks = {}, [], []
    reconstructed = None
    original_error = None
    try:
        # Own capture precedes argument/source readiness failure.
        captures['auditor'] = snapshot(own)
        require(len(sys.argv) == 1, 'fixed-no-argument-auditor')
        require(sys.flags.isolated == 1 and sys.flags.no_site == 1
                and sys.flags.dont_write_bytecode == 1, 'isolated-no-site-no-bytecode-required')
        readiness()
        aggregate = len(captures['auditor'][0])
        for role, name, pin in files[1:]:
            captures[role] = snapshot(name, pin)
            aggregate += len(captures[role][0])
            require(aggregate <= MAX_AGGREGATE_BYTES, 'aggregate-protected-body-bound')
        require(len({snap[1][:2] for snap in captures.values()}) == 8, 'physical-file-alias')
        budget()
        # All five scientific/premise pins and producer source authenticate
        # before any numerical input is decoded or converted to operands.
        objects = {role: decode(captures[role][0], allow_decimal_metadata=True)
                   for role in PIN if role != 'ri88'}
        accepted_premises(objects)
        objects['ri88'] = decode(captures['ri88'][0])
        own_checks = own_refusal_checks()
        reconstructed = reconstruct(objects)
        saved_check(captures['certificate'][0], reconstructed)
    except BaseException as error:
        original_error = error
    finally:
        # Every named file is attempted independently, including an uncaptured
        # file after an earlier guard failure. No short-circuit omits evidence.
        for role, name, pin in files:
            try:
                after = snapshot(name, pin)
                require(role in captures and after == captures[role], 'protected-file-changed-or-uncaptured')
                postchecks.append({'role': role, 'path': name, 'unchanged': True,
                                   'identity': identity(after[0])})
            except BaseException as error:
                postchecks.append({'role': role, 'path': name, 'unchanged': False,
                                   'error_type': type(error).__name__, 'error': str(error)})
    if original_error is not None or any(not row['unchanged'] for row in postchecks):
        error = original_error or AuditFailure('protected-postcheck-failure')
        emergency(error, postchecks)
        raise AuditFailure('saved-audit-refused; preserved independent postchecks') from error
    try:
        require(len(postchecks) == 8 and reconstructed is not None, 'complete-eight-file-postchecks')
        rebuilt_bytes = canonical(reconstructed)
        report = {
            'schema': 'ri128-independent-saved-sign-audit-v1',
            'status': 'all_saved_fields_independently_match',
            'producer_identity': identity(captures['producer'][0]),
            'auditor_identity': identity(captures['auditor'][0]),
            'input_identities': {role: identity(captures[role][0]) for role in PIN},
            'reconstructed_certificate_identity': identity(rebuilt_bytes),
            'complete_top_level_sections': {name: identity(canonical(reconstructed[name])) for name in FIELDS},
            'reconstructed_certificate': reconstructed,
            'protected_files': [{'role': role, 'path': name, **identity(captures[role][0])}
                                for role, name, _ in files],
            'postchecks': postchecks,
            'independent_counted_operations': OPS,
            'independently_rebuilt_fixture_count': len(FIXTURES),
            'declared_producer_controls': {'count': len(CONTROL_PAIRS),
                'ordered_pairs': reconstructed['refusal_controls'], 'executed_by_consumer': False},
            'auditor_first_refusal_checks': own_checks,
            'custody_semantics_self_adjudicated': False,
            'arithmetic_route': 'normalized integer pairs; individual14/12ideal sums; sparse explicit coefficients; direct powers',
            'scope': 'fixed containing rectangle; sufficient bounds only; no actual scales or full H30 feasibility',
        }
        raw = canonical(report)
        budget()
        sys.stdout.buffer.write(raw)
        sys.stdout.buffer.flush()
        budget()
    except BaseException as error:
        emergency(error, postchecks)
        raise AuditFailure('saved-audit-output-refused; any partial stdout invalid') from error


def main():
    global START
    START = time.monotonic()
    sys.set_int_max_str_digits(2 * WORK_BITS)
    def alarm(_signum, _frame):
        raise AuditFailure('wall-budget')
    signal.signal(signal.SIGALRM, alarm)
    signal.alarm(SECONDS)
    try:
        audit()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
