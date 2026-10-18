#!/usr/bin/env python3
"""Independent RI120 connected-sensitivity consumer. SOURCE PREPARATION ONLY.

Retained arithmetic/custody engine: accepted RI112 audit_saved_certificate.py,
54458 bytes, SHA256 0c3a781aee84f2d66fbe93e1aa3b07eb2961c3cd451abd6e5275931c25adbe3f.
Integer-pair, sparse polynomial and direct-power operations are retained.
New complete connected reconstruction and individual-ideal crosschecks are
separately authored. No Fraction, producer, prefix, checker or solver imports.
Unbound source pins/control declarations refuse; no admission is created here.
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
    'ri111': (20656, 'ca07943f8d2f9d9c396b4484193dc5797900f6c7a18c5f8c2a5b8333759ccf53'),
    'ri109_adjudication': (4849, '26ddd81d5fc1ae80c30d68aeadcb0ada0e18168bf3892b0995643294e6a64ddf'),
    'ri111_adjudication': (3838, 'fc4e9147db50ceb750d1f9fdcf503ffbb53363d2f1379557d1713bb844093249'),
    'ri115_adjudication': (6678, 'a23c0ac1208c78cc28590727675869968e2f579c863857aad67a9ea08b1d2480'),
    'ri117': (15564, '9726383aabb01cfa922b90f64bd572ac0a04a390111f57e722ed29d896289194'),
    'ri117_connected': (11893, 'ede2d82067a4259266d61988e0897756507e06b28040d8d5bd324991aa79dad0'),
    'ri117_adjudication': (4617, '862545fde8a9006dd39593c0aca7f47d6d82426dc47ffccea140e6f64957aec3'),
    'checker': (66669, '51c90364d76078d0202cebf96c23e0a71f36b718caa8df5b215bb3ae1e37174f'),
    'protocol': (16451, '40999dcf33e64207f042e419a9ebccc4475b0890e69e3cfa2d3b2053e0f0960b'),
    'contract': (11664, 'f3151110e6a2a4090aa3ea12fae593b2c9692b4408652e43e91d4fba5d9c87ab'),
}
PREMISES = ('ri88', 'ri111', 'ri109_adjudication', 'ri111_adjudication',
            'ri115_adjudication', 'ri117', 'ri117_connected', 'ri117_adjudication')
FILES = PREMISES + ('candidate',)
PROOFS = PREMISES[1:]
SOURCES = ('checker', 'protocol', 'contract')
CUSTODY = ('producer_witness_stdout', 'producer_witness_custody',
           'producer_normal_custody', 'producer_optimized_custody',
           'consumer_source_review')
FIELDS = ('schema', 'accepted_inputs', 'accepted_sources', 'inputs',
          'stem_profiles', 'connected_profiles', 'scale_domain', 'V_contrasts',
          'Q2_contrasts', 'common_gcd', 'decision', 'coverage', 'limitations',
          'arithmetic_limits', 'checker_sha256', 'root_fixtures', 'family_fixtures',
          'decision_fixtures', 'refusal_controls')
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
C3, C4, C5, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 7)
ORDERS = (C3, C4, C5, H5)
IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15),
          (0, 1, 3, 7, 15, 31), (0, 1, 3, 7, 15, 23, 31))
COUNTS = (8, 8, 16, 8)
RECORDS, CONNECTED_RECORDS, FAMILY_RECORDS = tuple(range(8)), tuple(range(16)), tuple(range(1, 16))
INPUT_BITS, WORK_BITS, TRANSIENT_BITS = 32768, 1048576, 2097154
MAX_OPS, MAX_TEXT, MAX_BYTES = 200000, 20000, 8388608
SECONDS, RSS_BYTES = 120, 536870912
ZERO, ONE = (0, 1), (1, 1)
START = None
OPS = 0

# Fixed interface declarations independently reviewed against the full contract.
# Literal names/reasons only: producer mutation actions are not run or imported.
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
CONTROL_COUNT = 166

FIXTURES = (
    ('constant-positive', ('1',), '1', 0), ('constant-negative', ('-1',), '1', 0),
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
FAMILY_FIXTURES = (
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


class AuditFailure(RuntimeError):
    pass


def need(condition, reason):
    if not condition:
        raise AuditFailure(reason)


def preparation_ready():
    for role in ('checker', 'protocol', 'contract'):
        value = PIN[role]
        need(type(value) is tuple and len(value) == 2
             and type(value[0]) is int and 0 < value[0] <= MAX_BYTES
             and type(value[1]) is str
             and re.fullmatch('[0-9a-f]{64}', value[1]) is not None,
             'source-preparation-unbound:'+role)
    need(type(CONTROL_COUNT) is int and CONTROL_COUNT > 0
         and type(CONTROL_PAIRS) is tuple and len(CONTROL_PAIRS) == CONTROL_COUNT,
         'source-preparation-unbound:controls')
    need(all(type(p) is tuple and len(p) == 2
             and all(type(v) is str and bool(v) for v in p) for p in CONTROL_PAIRS)
         and len({name for name, _ in CONTROL_PAIRS}) == CONTROL_COUNT,
         'source-control-declarations')


def budget():
    need(START is None or time.monotonic()-START <= SECONDS, 'wall-budget')
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    need((rss if sys.platform == 'darwin' else rss*1024) <= RSS_BYTES, 'rss-budget')


def tick():
    global OPS
    OPS += 1
    need(OPS <= MAX_OPS, 'operation-budget')
    budget()


def integer_bound(n, limit=TRANSIENT_BITS):
    need(type(n) is int and abs(n).bit_length() <= limit, 'integer-bound')
    return n


def pair(n, d=1, limit=WORK_BITS):
    integer_bound(n)
    integer_bound(d)
    need(d != 0, 'zero-denominator')
    if d < 0:
        n, d = -n, -d
    common = gcd(abs(n), d)
    n, d = n//common, d//common
    integer_bound(n, limit)
    integer_bound(d, limit)
    return (n, d)


def checked(q):
    need(type(q) is tuple and len(q) == 2 and all(type(v) is int for v in q),
         'rational-pair-type')
    integer_bound(q[0], WORK_BITS)
    integer_bound(q[1], WORK_BITS)
    need(q[1] > 0 and gcd(abs(q[0]), q[1]) == 1, 'normalized-pair')
    return q


def text(q):
    n, d = checked(q)
    return str(n) if d == 1 else str(n)+'/'+str(d)


def parse_q(value):
    need(type(value) is str and len(value) <= MAX_TEXT, 'rational-text-domain')
    need(re.fullmatch(r'-?(0|[1-9][0-9]*)(/[1-9][0-9]*)?', value) is not None,
         'canonical-rational-syntax')
    parts = value.split('/')
    q = pair(int(parts[0]), int(parts[1]) if len(parts) == 2 else 1, INPUT_BITS)
    need(text(q) == value, 'canonical-rational-value')
    return q


def plus(a, b):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    common = gcd(ad, bd)
    left, right = ad//common, bd//common
    return pair(integer_bound(an*right+bn*left), integer_bound(ad*right))


def minus(a, b):
    tick()
    checked(b)
    return plus(a, (-b[0], b[1]))


def times(a, b):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    ca, cb = gcd(abs(an), bd), gcd(abs(bn), ad)
    return pair(integer_bound((an//ca)*(bn//cb)),
                integer_bound((ad//cb)*(bd//ca)))


def over(a, b):
    tick()
    bn, bd = checked(b)
    need(bn != 0, 'zero-rational-divisor')
    return times(a, pair(bd, bn))


def compare(a, b=ZERO):
    tick()
    an, ad = checked(a)
    bn, bd = checked(b)
    left, right = integer_bound(an*bd), integer_bound(bn*ad)
    return (left > right)-(left < right)


def power(q, exponent):
    need(type(exponent) is int and 0 <= exponent <= 8, 'power-domain')
    checked(q)
    result = ONE
    for _ in range(exponent):
        result = times(result, q)
    return result


def sum_q(values):
    result = ZERO
    for q in values:
        result = plus(result, q)
    return result


def polynomial(p):
    need(type(p) is dict and len(p) <= 5, 'sparse-polynomial-domain')
    out = {}
    for degree, coefficient in p.items():
        need(type(degree) is int and 0 <= degree <= 4, 'sparse-exponent-domain')
        checked(coefficient)
        if coefficient != ZERO:
            out[degree] = coefficient
    return out


def from_list(values):
    need(type(values) in (list, tuple) and len(values) <= 5, 'coefficient-list-domain')
    return polynomial({i: q for i, q in enumerate(values)})


def encoded(p):
    p = polynomial(p)
    return [text(p.get(i, ZERO)) for i in range(max(p)+1)] if p else []


def padded(p, length):
    p = polynomial(p)
    need(type(length) is int and 0 <= length <= 5
         and (not p or max(p) < length), 'padded-polynomial-domain')
    return [text(p.get(i, ZERO)) for i in range(length)]


def degree(p):
    p = polynomial(p)
    return max(p) if p else -1


def poly_add(a, b):
    a, b = polynomial(a), polynomial(b)
    return polynomial({i: plus(a.get(i, ZERO), b.get(i, ZERO))
                       for i in sorted(set(a) | set(b))})


def poly_negative(p):
    return polynomial({i: minus(ZERO, q) for i, q in polynomial(p).items()})


def poly_product(a, b):
    a, b = polynomial(a), polynomial(b)
    result = {}
    for i in sorted(a):
        for j in sorted(b):
            need(i+j <= 4, 'product-degree')
            result[i+j] = plus(result.get(i+j, ZERO), times(a[i], b[j]))
    return polynomial(result)


def differentiate(p):
    return polynomial({i-1: times(pair(i), q)
                       for i, q in polynomial(p).items() if i})


def quotient_remainder(numerator, denominator):
    numerator, denominator = polynomial(numerator), polynomial(denominator)
    need(bool(denominator), 'zero-polynomial-divisor')
    residue, quotient = dict(numerator), {}
    degree = max(denominator)
    steps = 0
    while residue and max(residue) >= degree:
        steps += 1
        need(steps <= 5, 'division-step-budget')
        before = max(residue)
        shift = before-degree
        coefficient = over(residue[before], denominator[degree])
        quotient[shift] = plus(quotient.get(shift, ZERO), coefficient)
        monomial = {shift: coefficient}
        residue = poly_add(residue, poly_negative(poly_product(monomial, denominator)))
        need(not residue or max(residue) < before, 'division-degree-drop')
    quotient = polynomial(quotient)
    need(poly_add(poly_product(denominator, quotient), residue) == numerator,
         'independent-division-reconstruction')
    return quotient, residue


def gcd_trace(a, b):
    a, b = polynomial(a), polynomial(b)
    need(bool(a), 'zero-gcd-input')
    need(max(a) <= 3 and (not b or max(b) <= 3), 'gcd-cubic-domain')
    steps = []
    while b:
        # A lower-degree previous gcd followed by a cubic may require a first
        # zero-quotient division. Four divisions still suffice for cubics.
        need(len(steps) < 4, 'gcd-step-budget')
        quotient, remainder = quotient_remainder(a, b)
        steps.append({'dividend': encoded(a), 'divisor': encoded(b),
                      'quotient': encoded(quotient), 'remainder': encoded(remainder)})
        a, b = b, remainder
    leading = a[max(a)]
    return polynomial({i: over(q, leading) for i, q in a.items()}), steps


def direct_evaluation(p, endpoint):
    # Direct powers are independent of the producer's Horner recurrence.
    return sum_q(times(q, power(endpoint, i)) for i, q in sorted(polynomial(p).items()))


def endpoint_evidence(chain, x):
    values = [direct_evaluation(p, x) for p in chain]
    signs = [compare(v) for v in values]
    nonzero = [s for s in signs if s != 0]
    changes = sum(nonzero[i] != nonzero[i-1] for i in range(1, len(nonzero)))
    return {'x': text(x), 'values': [text(v) for v in values], 'signs': signs,
            'nonzero_signs': nonzero, 'variations': changes}


def root_evidence(p, radius):
    p = polynomial(p)
    need(bool(p) and max(p) <= 3, 'root-polynomial-domain')
    need(compare(radius) > 0, 'positive-radius')
    derivative = differentiate(p)
    common, common_steps = gcd_trace(p, derivative)
    free, free_remainder = quotient_remainder(p, common)
    reconstructed = poly_product(common, free)
    need(not free_remainder and reconstructed == p, 'square-free-product')
    coprime, coprime_steps = gcd_trace(free, differentiate(free))
    need(coprime == {0: ONE}, 'square-free-coprimality')
    chain = [free]
    derivative_free = differentiate(free)
    if derivative_free:
        chain.append(derivative_free)
    divisions = []
    while len(chain) >= 2:
        need(len(divisions) < 3, 'sturm-step-budget')
        quotient, remainder = quotient_remainder(chain[-2], chain[-1])
        negative = poly_negative(remainder)
        divisions.append({'dividend': encoded(chain[-2]), 'divisor': encoded(chain[-1]),
                          'quotient': encoded(quotient), 'remainder': encoded(remainder),
                          'next_term': encoded(negative)})
        if not negative:
            break
        need(max(negative) < max(chain[-1]), 'sturm-degree-drop')
        chain.append(negative)
    need(chain[-1] and max(chain[-1]) == 0 and len(chain) <= 4, 'constant-sturm-tail')
    lower, upper = endpoint_evidence(chain, ZERO), endpoint_evidence(chain, radius)
    count = lower['variations']-upper['variations']
    need(type(count) is int and 0 <= count <= max(free), 'root-count-range')
    return {
        'polynomial': encoded(p), 'interval': '(0,R]', 'R': text(radius),
        'derivative': encoded(derivative), 'gcd_euclidean': common_steps,
        'gcd_monic': encoded(common), 'square_free': encoded(free),
        'square_free_quotient': encoded(free), 'square_free_remainder': encoded(free_remainder),
        'reconstructed_polynomial': encoded(reconstructed), 'coprime_euclidean': coprime_steps,
        'coprime_gcd': encoded(coprime), 'sturm_chain': [encoded(q) for q in chain],
        'sturm_divisions': divisions, 'lower': lower, 'upper': upper,
        'distinct_real_roots': count, 'lower_excluded': True, 'upper_included': True,
        'rational_root_decision_performed': False, 'actual_scale_evaluated': False,
    }


def common_evidence(members, radius):
    need(type(members) is list and len(members) == 15, 'fifteen-family-members')
    need(all(type(item) is tuple and len(item) == 2 and type(item[0]) is int
             for item in members), 'family-member-types')
    need(tuple(item[0] for item in members) == FAMILY_RECORDS, 'family-record-order')
    checked(radius)
    need(compare(radius) > 0, 'positive-family-radius')
    normalized = [(r, polynomial(p)) for r, p in members]
    need(all(degree(p) <= 2 for _, p in normalized), 'family-quadratic-domain')
    nonzero = [r for r, p in normalized if p]
    zeros = [r for r, p in normalized if not p]
    if not nonzero:
        return {'branch': 'all-zero-Q2', 'nonzero_records': [],
                'zero_records': zeros, 'folds': [], 'gcd_monic': None,
                'divisibility': [], 'root_certificate': None,
                'all_Q2_identically_zero': True}
    common, folds = {}, []
    for r, p in normalized:
        if not p:
            continue
        before = common
        common, trace = gcd_trace(common, p) if common else gcd_trace(p, {})
        folds.append({'record': r, 'previous_gcd': encoded(before),
                      'input_polynomial': encoded(p), 'gcd_euclidean': trace,
                      'gcd_monic': encoded(common)})
    need(common and common[max(common)] == ONE, 'family-monic-result')
    divisibility = []
    for r, p in normalized:
        quotient, remainder = quotient_remainder(p, common)
        reconstructed = poly_product(common, quotient)
        need(not remainder and reconstructed == p, 'family-divisibility')
        divisibility.append({'record': r, 'polynomial': encoded(p),
                             'quotient': encoded(quotient), 'remainder': encoded(remainder),
                             'reconstructed_polynomial': encoded(reconstructed)})
    return {'branch': 'nonzero-gcd', 'nonzero_records': nonzero,
            'zero_records': zeros, 'folds': folds, 'gcd_monic': encoded(common),
            'divisibility': divisibility, 'root_certificate': root_evidence(common, radius),
            'all_Q2_identically_zero': False}


def decision(common, v_deltas):
    need(type(v_deltas) is list and len(v_deltas) == 7, 'decision-V-domain')
    for q in v_deltas:
        checked(q)
    f3 = 'nonconstant' if any(q != ZERO for q in v_deltas) else 'constant'
    all_zero = common['all_Q2_identically_zero']
    need(type(all_zero) is bool, 'decision-branch-type')
    if all_zero:
        need(common['branch'] == 'all-zero-Q2'
             and common['gcd_monic'] is None and common['root_certificate'] is None,
             'decision-zero-family')
        count, common_degree = None, None
        f2 = 'constant'
    else:
        need(common['branch'] == 'nonzero-gcd', 'decision-nonzero-family')
        count = common['root_certificate']['distinct_real_roots']
        common_degree = len(common['gcd_monic'])-1
        need(type(count) is int and 0 <= count <= common_degree <= 2, 'decision-root-domain')
        f2 = 'nonconstant' if count == 0 else 'undetermined'
    rejected = f2 == 'nonconstant' and f3 == 'nonconstant'
    return {
        'f2_status': f2, 'f3_status': f3,
        'disposition': 'certified-connected-obstruction' if rejected else 'unresolved-connected-sensitivity',
        'common_gcd_degree': common_degree, 'distinct_common_real_roots': count,
        'no_common_real_root_on_admissible_interval': f2 == 'nonconstant',
        'restricted_28_child_repair_rejected': rejected,
        'rational_root_decision_performed': False, 'rational_roots_remaining_asserted': False,
        'actual_scale_root_asserted': False, 'positive_repair_asserted': False,
        'all_positive_extensions_rejected': False, 'actual_scale_computed': False,
        'remaining_parent_feasibility_decided': False,
    }

def fixture_evidence():
    output = []
    for name, coefficients, radius, expected in FIXTURES:
        evidence = root_evidence(from_list([parse_q(v) for v in coefficients]), parse_q(radius))
        need(evidence['distinct_real_roots'] == expected, 'fixture-root-count:'+name)
        output.append({'name': name, 'expected_distinct_real_roots': expected,
                       'root_certificate': evidence, 'native_model_claimed': False})
    need(len(output) == 16 and len({x['name'] for x in output}) == 16, 'fixture-inventory')
    return output


def family_fixture_evidence():
    output = []
    for name, prefix, radius, expected_gcd, expected_count in FAMILY_FIXTURES:
        declared = [list(p) for p in prefix] + [[] for _ in range(15-len(prefix))]
        members = [(r, from_list([parse_q(q) for q in p]))
                   for r, p in zip(FAMILY_RECORDS, declared)]
        evidence = common_evidence(members, parse_q(radius))
        expected = list(expected_gcd) if expected_gcd is not None else None
        need(evidence['gcd_monic'] == expected, 'fixture-family-gcd:'+name)
        roots = evidence['root_certificate']
        count = roots['distinct_real_roots'] if roots is not None else None
        need(count == expected_count, 'fixture-family-count:'+name)
        output.append({'name': name, 'input_polynomials': declared, 'R': radius,
                       'expected_gcd': expected, 'expected_distinct_real_roots': expected_count,
                       'common_gcd': evidence, 'decision': decision(evidence, [ONE]+[ZERO]*6),
                       'native_model_claimed': False})
    need(len(output) == 10 and len({x['name'] for x in output}) == 10, 'family-fixture-inventory')
    return output


def decision_fixture_evidence(families):
    by_name = {item['name']: item for item in families}
    output = []
    for family_name, expected_f2 in (('all-zero', 'constant'),
                                     ('zero-plus-constant', 'nonconstant'),
                                     ('common-included-upper', 'undetermined')):
        for nonconstant in (False, True):
            deltas = [ONE if nonconstant else ZERO]+[ZERO]*6
            expected_f3 = 'nonconstant' if nonconstant else 'constant'
            expected_rejected = family_name == 'zero-plus-constant' and nonconstant
            result = decision(by_name[family_name]['common_gcd'], deltas)
            need(result['f2_status'] == expected_f2
                 and result['f3_status'] == expected_f3
                 and result['restricted_28_child_repair_rejected'] is expected_rejected,
                 'fixture-combined-decision')
            output.append({'name': family_name+'--V-'+expected_f3,
                           'family_fixture': family_name,
                           'V_deltas': [text(q) for q in deltas],
                           'expected_f2_status': expected_f2,
                           'expected_f3_status': expected_f3,
                           'expected_rejected': expected_rejected,
                           'decision': result, 'native_model_claimed': False})
    need(len(output) == 6 and len({x['name'] for x in output}) == 6, 'decision-fixture-inventory')
    return output

def keys(value, expected, label):
    need(type(value) is dict and set(value) == set(expected), 'fields:'+label)


def exact(actual, expected, label='body'):
    need(type(actual) is type(expected), 'exact-type:'+label)
    if type(expected) is dict:
        keys(actual, expected, label)
        for key in expected:
            exact(actual[key], expected[key], label+'.'+key)
    elif type(expected) is list:
        need(len(actual) == len(expected), 'list-coverage:'+label)
        for i, (a, b) in enumerate(zip(actual, expected)):
            exact(a, b, label+'['+str(i)+']')
    else:
        need(actual == expected, 'exact-value:'+label)


def adjudication_metadata(ri109, ri111, ri115, ri117):
    for data, schema, status in (
        (ri109, 'ri109-root-final-mathematical-adjudication-v1',
         'ACCEPT_INDEPENDENT_RESTRICTED_27_CHILD_REPAIR_OBSTRUCTION'),
        (ri111, 'ri111-root-analytic-adjudication-v1',
         'ACCEPT_CONDITIONAL_COMPLETE_28_CHILD_REDUCTION_ONLY'),
        (ri115, 'ri115-root-final-native-mathematical-adjudication-v1',
         'ACCEPT_EXACT_ZERO_MINOR_RESULT_WITH_FEASIBILITY_OPEN'),
        (ri117, 'ri117-root-coupled-family-adjudication-v1',
         'ACCEPT_COMPLETE_CONDITIONAL_COUPLED_REDUCTION_ONLY'),
    ):
        need(type(data) is dict and data.get('schema') == schema
             and data.get('status') == status, 'accepted-root-adjudication')
    need(ri111.get('actual_28_child_feasibility') == 'UNRESOLVED'
         and ri111.get('new_native_coefficients_or_scales_evaluated') is False
         and ri111.get('new_numerical_execution_admitted') is False,
         'accepted-RI111-source-only-boundary')
    need(ri115.get('mathematical_result_accepted') is True
         and ri115.get('whole_positive_extension_established') is False,
         'accepted-RI115-mathematical-boundary')
    need(ri117.get('active_execution_admission') is False
         and ri117.get('fixed_28_child_repair_rejected') is False
         and ri117.get('full_positive_repair_proved') is False,
         'accepted-RI117-conditional-boundary')

def accepted_rows(data):
    keys(data, RI88_FIELDS, 'RI88')
    need(data['schema'] == 'ri88-four-vertex-cap-v1'
         and data['checker_sha256'] == '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
         and data['design_sha256'] == 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a',
         'RI88-source')
    exact(data['dependencies'], DEPENDENCIES, 'RI88-dependencies')
    admission = data['admission']
    need(type(admission) is dict and admission.get('epsilon') == '1/4'
         and admission.get('later_h_prescribed') is False
         and admission.get('numerical_a6_evaluated') is False, 'RI88-admission')
    need(type(data['exact_decision']) is dict
         and data['exact_decision'].get('disposition') == 'positive-finite-width-bias',
         'RI88-disposition')
    prefix, coverage = data['prefix'], data['coverage']
    need(type(prefix) is dict
         and prefix.get('problem_sha256') == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
         and prefix.get('actual_probability_manifest_sha256') == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
         and type(prefix.get('canonical_lex_stages')) is int
         and prefix['canonical_lex_stages'] == 69, 'RI88-prefix')
    need(type(coverage) is dict and type(coverage.get('held_marked_rows')) is int
         and coverage['held_marked_rows'] == 40
         and type(coverage.get('held_probability_slots')) is int
         and coverage['held_probability_slots'] == 224, 'RI88-coverage')
    need(type(data['held_rows']) is list and len(data['held_rows']) == 40, 'held-row-count')
    expected = [(p, r) for p, count in zip(ORDERS, COUNTS) for r in range(count)]
    selected, seen = [], set()
    for entry in data['held_rows']:
        keys(entry, ('order', 'record', 'probabilities'), 'held-entry')
        need(type(entry['order']) is list and all(type(x) is int for x in entry['order'])
             and type(entry['record']) is int, 'held-metadata-types')
        key = (tuple(entry['order']), entry['record'])
        need(key[0] in ORDERS, 'held-order-domain')
        count = COUNTS[ORDERS.index(key[0])]
        need(0 <= key[1] < count, 'held-record-domain')
        need(key not in seen, 'duplicate-held-row')
        seen.add(key)
        selected.append(entry)
    need([(tuple(e['order']), e['record']) for e in selected] == expected, 'held-selected-order')
    held = {}
    for entry, key in zip(selected, expected):
        row, inventory = entry['probabilities'], IDEALS[ORDERS.index(key[0])]
        need(type(row) is list and len(row) == len(inventory), 'held-slot-count')
        for item in row:
            need(type(item) is list and len(item) == 2 and type(item[0]) is int, 'held-slot-type')
        need([item[0] for item in row] == list(inventory), 'held-slot-inventory')
        values = [parse_q(item[1]) for item in row]
        need(all(compare(q) > 0 for q in values) and sum_q(values) == ONE, 'held-positive-normalized')
        held[key] = dict(zip(inventory, values))
    for order, inventory, count in zip(ORDERS, IDEALS, COUNTS):
        for r in range(count):
            need(held[(order, r)][0] == held[(order, 0)][0], 'held-empty-locality')
        for ideal in inventory[:-1]:
            by_precursor = {}
            for r in range(count):
                local = r & ideal
                value = held[(order, r)][ideal]
                if local in by_precursor:
                    need(value == by_precursor[local], 'held-proper-record-locality')
                else:
                    by_precursor[local] = value
    for r in RECORDS:
        need(held[(H5, r)][15] == held[(H5, r)][23], 'held-twin-symmetry')
        for sigma in (0, 1):
            left = times(held[(C4, r)][7], held[(H5, r)][15])
            right = times(held[(C4, r)][15], held[(C5, r+8*sigma)][7])
            need(left == right, 'held-whole-map-diamond')
    return held, selected


def held_probability(held, order, record, ideal):
    need(type(order) is tuple and all(type(v) is int for v in order) and order in ORDERS,
         'held-lookup-order')
    need(type(record) is int and 0 <= record < COUNTS[ORDERS.index(order)], 'held-lookup-record')
    need(type(ideal) is int and ideal in IDEALS[ORDERS.index(order)], 'held-lookup-ideal')
    return held[(order, record)][ideal]


def stem_evidence(held, record):
    terms = []
    for ideal in (0, 1, 3, 7):
        a = held_probability(held, C3, record, ideal)
        b = held_probability(held, C4, record, ideal)
        g = held_probability(held, H5, record, ideal)
        terms.append(times(a, power(over(g, b), 3)))
    c = held_probability(held, C4, record, 15)
    h = held_probability(held, H5, record, 15)
    j = held_probability(held, H5, record, 31)
    m = times(h, over(h, c))
    e = sum_q(terms + [m, m, m, j, j, j])
    v = sum_q(terms + [m, m, j])
    need(v == minus(minus(e, m), times(pair(2), j)), 'stem-V-identity')
    u3 = from_list([pair(2), minus(ZERO, plus(ONE, v)), v])
    # Twelve distinct proper ideals, with duplicated symmetric ideals retained.
    ideals = [{2: term} for term in terms]
    ideals += [{2: m}, {2: m}, {2: j}, {1: m}, {1: j}, {1: j},
               from_list([ONE, minus(ZERO, e)]), from_list([ONE, pair(-1)])]
    summed = {}
    for potential in ideals:
        summed = poly_add(summed, potential)
    need(len(ideals) == 12 and summed == u3, 'twelve-T3-ideal-sum')
    scalars = {'E': e, 'V': v, 'm': m, 'c': c, 'h': h, 'j': j}
    entry = {'record': record, 'E_terms': [text(q) for q in terms],
             'c': text(c), 'h': text(h), 'j': text(j), 'm': text(m),
             'E': text(e), 'V': text(v), 'U3_padded': padded(u3, 3)}
    return scalars, entry


def connected_evidence(held, record, stem):
    xi = record & 7
    e = held_probability(held, C5, record, 15)
    ell = held_probability(held, C5, record, 31)
    c, h, j, m, big_e = (stem[key] for key in ('c', 'h', 'j', 'm', 'E'))
    e2_terms, c2_terms = [], []
    for ideal in (0, 1, 3, 7):
        a = held_probability(held, C3, xi, ideal)
        b = held_probability(held, C4, xi, ideal)
        g = held_probability(held, H5, xi, ideal)
        d = held_probability(held, C5, record, ideal)
        ratio = over(g, b)
        e2_terms.append(times(d, ratio))
        c2_terms.append(times(over(times(a, d), b), power(ratio, 3)))
    ratio_h = over(h, c)
    e2_terms += [times(e, ratio_h), h, j, ell]
    c2_terms.append(times(e, power(ratio_h, 2)))
    e2, c2 = sum_q(e2_terms), sum_q(c2_terms)
    a2 = minus(plus(big_e, times(pair(2), e2)), j)
    b2 = sum_q([m, m, j, j, ell])
    u2 = from_list([pair(3), minus(ZERO, a2), b2, c2])
    # Re-express all fourteen RI117 ideals using direct products/denominators,
    # separate from the quotient-first C2 profile arithmetic above.
    ideals = []
    for ideal in (0, 1, 3, 7):
        a = held_probability(held, C3, xi, ideal)
        b = held_probability(held, C4, xi, ideal)
        g = held_probability(held, H5, xi, ideal)
        d = held_probability(held, C5, record, ideal)
        coefficient = over(times(times(a, power(g, 3)), d), power(b, 4))
        ideals.append({3: coefficient})
    ideals += [{3: over(times(e, power(h, 2)), power(c, 2))},
               {2: m}, {2: m}, {2: j}, {2: j}, {1: j},
               from_list([ONE, minus(ZERO, big_e)]), {2: ell},
               from_list([ONE, minus(ZERO, e2)]),
               from_list([ONE, minus(ZERO, e2)])]
    summed = {}
    for potential in ideals:
        summed = poly_add(summed, potential)
    need(len(ideals) == 14 and summed == u2, 'fourteen-T2-ideal-sum')
    entry = {'record': record, 'stem_record': xi, 'sigma': record >> 3,
             'e': text(e), 'ell': text(ell),
             'E2_terms': [text(q) for q in e2_terms], 'E2': text(e2),
             'C2_terms': [text(q) for q in c2_terms], 'C2': text(c2),
             'A2': text(a2), 'B2': text(b2), 'U2_padded': padded(u2, 4)}
    return (a2, b2, c2), u2, entry


def pin_dict(role):
    need(type(PIN[role]) is tuple, 'source-pin-unbound:'+role)
    return {'bytes': PIN[role][0], 'sha256': PIN[role][1]}


def reconstruct(data):
    preparation_ready()
    held, rows = accepted_rows(data)
    stem_scalars, stem_profiles = [], []
    for record in RECORDS:
        scalars, profile = stem_evidence(held, record)
        stem_scalars.append(scalars)
        stem_profiles.append(profile)
    connected_scalars, connected_us, connected_profiles = [], [], []
    for record in CONNECTED_RECORDS:
        scalars, u, profile = connected_evidence(held, record, stem_scalars[record & 7])
        connected_scalars.append(scalars)
        connected_us.append(u)
        connected_profiles.append(profile)
    es = [stem_scalars[record]['E'] for record in (0, 1)]
    maximum = es[0] if compare(es[0], es[1]) >= 0 else es[1]
    radius = over(ONE, times(pair(2), plus(ONE, maximum)))
    need(compare(radius) > 0, 'radius-positive')
    margins = [minus(ONE, times(radius, e)) for e in es]
    need(all(compare(m, pair(1, 2)) > 0 for m in margins), 'lower-full-margins')
    v_deltas, v_contrasts = [], []
    for record in range(1, 8):
        v, v0 = stem_scalars[record]['V'], stem_scalars[0]['V']
        delta = minus(v, v0)
        v_deltas.append(delta)
        v_contrasts.append({'record': record, 'V': text(v), 'V0': text(v0),
                            'delta_V': text(delta), 'is_zero': delta == ZERO})
    q2_contrasts, family = [], []
    for record in FAMILY_RECORDS:
        da, db, dc = [minus(current, reference) for current, reference in
                      zip(connected_scalars[record], connected_scalars[0])]
        q2 = from_list([minus(ZERO, da), db, dc])
        raw = poly_add(connected_us[record], poly_negative(connected_us[0]))
        quotient, remainder = quotient_remainder(raw, {1: ONE})
        need(not remainder and quotient == q2
             and raw == poly_product({1: ONE}, q2), 'Q2-fixed-rho-division')
        need(degree(q2) <= 2, 'Q2-quadratic-bound')
        q2_contrasts.append({'record': record, 'delta_A2': text(da),
                             'delta_B2': text(db), 'delta_C2': text(dc),
                             'Q2_padded': padded(q2, 3),
                             'U2_difference_padded': padded(raw, 4),
                             'fixed_divisor': 'rho', 'quotient_matches_closed_formula': True,
                             'degree': degree(q2), 'is_zero': not bool(q2)})
        family.append((record, q2))
    common = common_evidence(family, radius)
    family_fixtures = family_fixture_evidence()
    result = {
        'schema': 'ri120-connected-sensitivity-certificate-v1',
        'accepted_inputs': {'ri88': pin_dict('ri88')},
        'accepted_sources': {role: pin_dict(role) for role in PROOFS},
        'inputs': {'held_rows': rows,
                   'selected_order': [name+':'+str(record)
                                      for name, count in zip(('C3', 'C4', 'C5', 'H5'), COUNTS)
                                      for record in range(count)],
                   'prefix_replayed': False, 'H_or_z_values_read': False,
                   'transport_basis': 'RI117 complete connected profiles; RI111 maximal-bit and RI85 unique/twin-top transport',
                   'proper_locality_checked': True, 'twin_diamond_checked': True},
        'stem_profiles': stem_profiles, 'connected_profiles': connected_profiles,
        'scale_domain': {'R': text(radius), 'selected_E': [text(e) for e in es],
                         'interval': '0<rho<=R', 'lower_full_margins_at_R': [text(m) for m in margins],
                         'actual_rho_evaluated': False, 'amplitude': '1/4', 'seed_unchanged': True},
        'V_contrasts': v_contrasts, 'Q2_contrasts': q2_contrasts,
        'common_gcd': common, 'decision': decision(common, v_deltas),
        'coverage': {'held_rows': 40, 'held_probability_slots': 224, 'stem_records': 8,
                     'connected_records': 16, 'V_contrasts': 7, 'Q2_contrasts': 15,
                     'H_or_z_arithmetic_values': 0, 'new_q6_q7_rows': 0,
                     'native_polynomial_degree_cap': 2},
        'limitations': {'real_roots_do_not_imply_rational_roots': True,
                        'roots_in_outer_interval_do_not_locate_actual_scale': True,
                        'complete_all_size_extension_not_claimed': True,
                        'QM_geometry_gravity_derivation_not_claimed': True,
                        'restricted_candidate_only': True, 'external_custody_required': True,
                        'remaining_parent_feasibility_not_decided': True,
                        'sensitivity_not_positive_repair': True},
        'arithmetic_limits': {'input_rational_bits': INPUT_BITS, 'working_rational_bits': WORK_BITS,
                              'transient_integer_bits': TRANSIENT_BITS, 'counted_operations': MAX_OPS,
                              'rational_text_characters': MAX_TEXT, 'output_bytes': MAX_BYTES,
                              'active_child_seconds': SECONDS, 'resident_bytes': RSS_BYTES},
        'checker_sha256': PIN['checker'][1], 'root_fixtures': fixture_evidence(),
        'family_fixtures': family_fixtures,
        'decision_fixtures': decision_fixture_evidence(family_fixtures),
        'refusal_controls': [{'name': name, 'reason': reason} for name, reason in CONTROL_PAIRS],
    }
    keys(result, FIELDS, 'reconstructed-nineteen-sections')
    return result


def json_load(raw):
    need(type(raw) is bytes and len(raw) <= MAX_BYTES, 'JSON-byte-bound')
    def object_pairs(items):
        result = {}
        for name, value in items:
            need(name not in result, 'duplicate-JSON-key')
            result[name] = value
        return result
    def no_decimal(_value):
        raise AuditFailure('noninteger-JSON-number')
    def integer(value):
        need(len(value) <= MAX_TEXT, 'JSON-integer-text-bound')
        return int(value)
    return json.loads(raw, object_pairs_hook=object_pairs, parse_int=integer,
                      parse_float=no_decimal, parse_constant=no_decimal)


def canonical(value):
    raw = (json.dumps(value, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
    need(len(raw) <= MAX_BYTES, 'output-byte-bound')
    budget()
    return raw


def identity(raw):
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}


def path_text(value):
    need(type(value) is str and value and '\x00' not in value
         and os.path.isabs(value) and os.path.normpath(value) == value, 'absolute-literal-path')
    return value


def entry_shape(value):
    keys(value, ('path', 'bytes', 'sha256'), 'file-entry')
    path_text(value['path'])
    need(type(value['bytes']) is int and 0 < value['bytes'] <= MAX_BYTES, 'file-byte-pin')
    need(type(value['sha256']) is str
         and re.fullmatch('[0-9a-f]{64}', value['sha256']) is not None, 'file-hash-pin')


def signature(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def stable_read(entry):
    entry_shape(entry)
    name = entry['path']
    p = Path(name)
    need(str(p.resolve(strict=True)) == name, 'symlink-path')
    before = p.lstat()
    need(stat.S_ISREG(before.st_mode) and not stat.S_ISLNK(before.st_mode), 'regular-file')
    need(before.st_size == entry['bytes'], 'file-size')
    descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(descriptor)
        need(signature(opened) == signature(before), 'open-identity-change')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(entry['bytes']+1)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after = p.lstat()
    need(str(p.resolve(strict=True)) == name, 'postread-symlink-path')
    need(signature(before) == signature(after_fd) == signature(after), 'read-identity-change')
    need(identity(raw) == {'bytes': entry['bytes'], 'sha256': entry['sha256']}, 'file-byte-hash')
    budget()
    return raw, signature(after)


def capture_self(name):
    """Observed source custody before descriptor parsing; not self-authorization."""
    path_text(name)
    p = Path(name)
    need(str(p.resolve(strict=True)) == name, 'self-symlink-path')
    before = p.lstat()
    need(stat.S_ISREG(before.st_mode) and 0 < before.st_size <= MAX_BYTES, 'self-file-domain')
    descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        need(signature(os.fstat(descriptor)) == signature(before), 'self-open-change')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(before.st_size+1)
        after_fd = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    after = p.lstat()
    need(str(p.resolve(strict=True)) == name and len(raw) == before.st_size
         and signature(before) == signature(after_fd) == signature(after), 'self-read-change')
    # Do not let an exhausted normal budget discard a captured failure snapshot.
    return {'path': name, **identity(raw)}, (raw, signature(after))


def failure_bytes(failure):
    """Bounded emergency evidence only; never success or arithmetic fallback."""
    def clipped(value):
        value = str(value)
        return value[:2048] if len(value) > 2048 else value
    items = []
    for item in failure['postchecks'][:19]:
        items.append({key: clipped(value) if type(value) is str else value
                      for key, value in item.items()})
    diagnostic = dict(failure, error=clipped(failure['error']), postchecks=items,
                      diagnostic_text_limit=2048, normal_budget_reapplied=False)
    raw = (json.dumps(diagnostic, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
    # Nineteen bounded records remain bounded with worst-case JSON escaping.
    if len(raw) > 1048576:
        return b'{"schema":"ri120-audit-failure-v1","status":"REFUSED","diagnostic_overflow":true}\n'
    return raw


def refuse(original_error, postchecks, descriptor_valid):
    # Any partial stdout is invalid after this failure. The false disposition
    # flag denies an accepted scientific result; it is not a no-bytes-written claim.
    failure = {'schema': 'ri120-audit-failure-v1', 'status': 'REFUSED',
               'error_type': type(original_error).__name__ if original_error else 'PostcheckFailure',
               'error': str(original_error) if original_error else 'postcheck failure',
               'postchecks': postchecks, 'descriptor_postcheck_admitted': descriptor_valid,
               'scientific_disposition_emitted': False}
    sys.stderr.buffer.write(failure_bytes(failure))
    sys.stderr.buffer.flush()
    raise AuditFailure('audit-refused; see preserved stderr/postchecks') from original_error


def descriptor_entries(value, descriptor_path, own_path, bindings, unique, role_paths):
    # Populate protected identities incrementally: a later malformed entry or
    # alias must not discard earlier discovered paths from failure postchecks.
    keys(value, ('schema', 'phase', 'files', 'accepted_sources', 'audit_source',
                 'custody_dependencies'), 'descriptor')
    need(value['schema'] == 'ri120-independent-audit-input-v1'
         and value['phase'] == 'fixed_saved_certificate_audit', 'descriptor-mode')
    keys(value['files'], FILES, 'descriptor-files')
    keys(value['accepted_sources'], SOURCES, 'descriptor-sources')

    def register(role, entry):
        entry_shape(entry)
        name = entry['path']
        need(name != descriptor_path, 'descriptor-payload-path-alias')
        need(name not in role_paths.values(), 'payload-path-alias')
        if name == own_path:
            need(role == 'audit_source', 'own-source-path-alias')
            exact(entry, unique[own_path], 'admitted-self-source-identity')
        else:
            unique[name] = entry
        role_paths[role] = name
        bindings.append((role, entry))

    for group, roles in (('files', FILES), ('accepted_sources', SOURCES)):
        for role in roles:
            entry = value[group][role]
            register(group+'.'+role, entry)
            if role != 'candidate':
                exact({key: entry[key] for key in ('bytes', 'sha256')},
                      pin_dict(role), 'fixed-pin:'+role)
    entry_shape(value['audit_source'])
    need(value['audit_source']['path'] == own_path, 'executing-audit-source-path')
    register('audit_source', value['audit_source'])
    custody = value['custody_dependencies']
    need(type(custody) is list and len(custody) == 5, 'custody-count')
    for role, item in zip(CUSTODY, custody):
        keys(item, ('role', 'path', 'bytes', 'sha256'), 'custody-entry')
        need(type(item['role']) is str and item['role'] == role, 'custody-order')
        register('custody.'+role, {key: item[key] for key in ('path', 'bytes', 'sha256')})
    need(len(bindings) == 18 and len(unique) == 18, 'eighteen-roles-eighteen-files')
    candidate, witness = value['files']['candidate'], custody[0]
    exact({key: candidate[key] for key in ('bytes', 'sha256')},
          {key: witness[key] for key in ('bytes', 'sha256')}, 'candidate-witness-pin')


def distinct_physical_inputs(snapshots, descriptor_path, descriptor_snapshot):
    need(descriptor_snapshot is not None, 'descriptor-not-snapshotted')
    physical = {}
    for name, snapshot in list(snapshots.items()) + [(descriptor_path, descriptor_snapshot)]:
        signature_value = snapshot[1]
        pair_identity = signature_value[:2]
        need(pair_identity not in physical, 'physical-hardlink-alias')
        physical[pair_identity] = name
    need(len(physical) == 19, 'nineteen-physical-identities')


def audit():
    own_path = path_text(os.path.abspath(__file__))
    descriptor_entry = None
    descriptor_valid = False
    descriptor_snapshot = None
    snapshots, unique, bindings, role_paths = {}, {}, [], {}
    expected = reconstructed = descriptor = None
    original_error = None
    postchecks = []
    try:
        own_entry, own_snapshot = capture_self(own_path)
        unique[own_path] = own_entry
        snapshots[own_path] = own_snapshot
        budget()
        preparation_ready()
        need(len(sys.argv) == 4, 'usage: audit_saved_certificate.py DESCRIPTOR BYTES SHA256')
        need(sys.flags.isolated == 1 and sys.flags.no_site == 1 and sys.flags.dont_write_bytecode == 1,
             'isolated-no-site-no-bytecode-required')
        size = sys.argv[2]
        need(type(size) is str and re.fullmatch('[1-9][0-9]{0,7}', size) is not None,
             'canonical-descriptor-size')
        descriptor_entry = {'path': sys.argv[1], 'bytes': int(size), 'sha256': sys.argv[3]}
        entry_shape(descriptor_entry)
        descriptor_valid = True
        descriptor_snapshot = stable_read(descriptor_entry)
        descriptor = json_load(descriptor_snapshot[0])
        descriptor_entries(descriptor, descriptor_entry['path'], own_path,
                           bindings, unique, role_paths)
        exact(descriptor['audit_source'], own_entry, 'admitted-self-source-identity')
        # Every source, data and custody identity precedes scientific parsing.
        for name, entry in unique.items():
            if name != own_path:
                snapshots[name] = stable_read(entry)
        for role, entry in bindings:
            exact(identity(snapshots[entry['path']][0]),
                  {k: entry[k] for k in ('bytes', 'sha256')}, 'captured-role:'+role)
        distinct_physical_inputs(snapshots, descriptor_entry['path'], descriptor_snapshot)
        candidate_raw = snapshots[role_paths['files.candidate']][0]
        witness_raw = snapshots[role_paths['custody.producer_witness_stdout']][0]
        need(candidate_raw == witness_raw, 'candidate-not-genuine-stdout-copy')
        adjudication_metadata(
            json_load(snapshots[role_paths['files.ri109_adjudication']][0]),
            json_load(snapshots[role_paths['files.ri111_adjudication']][0]),
            json_load(snapshots[role_paths['files.ri115_adjudication']][0]),
            json_load(snapshots[role_paths['files.ri117_adjudication']][0]))
        data = json_load(snapshots[role_paths['files.ri88']][0])
        saved = json_load(candidate_raw)
        expected = reconstruct(data)
        exact(saved, expected, 'complete-certificate')
        reconstructed = canonical(expected)
        need(reconstructed == candidate_raw, 'complete-canonical-certificate-bytes')
    except BaseException as error:
        original_error = error
    finally:
        # Independent attempts: no boolean short-circuit can omit later checks.
        for name, entry in unique.items():
            try:
                after = stable_read(entry)
                need(name in snapshots and after == snapshots[name], 'changed-or-uncaptured-input')
                postchecks.append({'path': name, 'unchanged': True, 'identity': identity(after[0])})
            except BaseException as error:
                postchecks.append({'path': name, 'unchanged': False,
                                   'error_type': type(error).__name__, 'error': str(error)})
        if own_path not in unique:
            try:
                _entry, after = capture_self(own_path)
                need(own_path in snapshots and after == snapshots[own_path], 'uncaptured-self-source')
                postchecks.append({'path': own_path, 'unchanged': True, 'identity': identity(after[0])})
            except BaseException as error:
                postchecks.append({'path': own_path, 'unchanged': False,
                                   'error_type': type(error).__name__, 'error': str(error)})
        if descriptor_valid:
            try:
                after = stable_read(descriptor_entry)
                need(descriptor_snapshot is not None and after == descriptor_snapshot, 'changed-descriptor')
                postchecks.append({'path': descriptor_entry['path'], 'unchanged': True,
                                   'identity': identity(after[0])})
            except BaseException as error:
                postchecks.append({'path': descriptor_entry['path'], 'unchanged': False,
                                   'error_type': type(error).__name__, 'error': str(error)})
    if original_error is not None or any(not item['unchanged'] for item in postchecks):
        refuse(original_error, postchecks, descriptor_valid)
    try:
        need(len(postchecks) == 19 and reconstructed is not None, 'complete-postcheck-coverage')
        for role, entry in bindings:
            exact(identity(snapshots[entry['path']][0]),
                  {k: entry[k] for k in ('bytes', 'sha256')}, 'final-role:'+role)
        report = {
            'schema': 'ri120-independent-complete-connected-sensitivity-audit-v1',
            'status': 'all_saved_fields_independently_match',
            'descriptor_identity': identity(descriptor_snapshot[0]),
            'audit_source_identity': identity(snapshots[own_path][0]),
            'accepted_source_identities': {role: pin_dict(role) for role in SOURCES},
            'payload_role_bindings': [{'role': role, **entry} for role, entry in bindings],
            'unique_payload_paths': 18, 'payload_role_count': 18,
            'reconstructed_certificate_identity': identity(reconstructed),
            'complete_top_level_sections': {name: identity(canonical(expected[name])) for name in FIELDS},
            'reconstructed_certificate': expected,
            'postchecks': postchecks, 'independent_counted_operations': OPS,
            'declared_producer_controls': {'count': CONTROL_COUNT,
                                          'ordered_pairs': expected['refusal_controls'],
                                          'producer_controls_executed_by_consumer': False},
            'independently_rebuilt_fixture_count': 16,
            'independently_rebuilt_family_fixture_count': 10,
            'independently_rebuilt_decision_fixture_count': 6,
            'custody_semantics_self_adjudicated': False,
            'independence': [
                'Normalized integer pairs and cross-cancellation; no Fraction or producer imports.',
                'Quotient-first connected profiles and direct-product fourteen/twelve individual-ideal sums.',
                'Sparse polynomial products, fixed-rho divisions and monic family gcd folds.',
                'Exact long-division reconstruction and direct-power endpoints, not producer Horner.',
                'Every one of nineteen sections and complete canonical bytes is independently rebuilt.',
                'Sixteen root, ten fifteen-member family and six combined-decision fixtures are independently reconstructed.',
                'Producer refusal names/reasons are declarations, not consumer-executed mutations.',
            ],
            'limits': [
                'Inherited RI88 probabilities and fixed RI109/RI111/RI115/RI117 premises are not rederived.',
                'All forty held rows and 224 probabilities; no H/z or new q6/q7 table.',
                'Radius uses only E0 and E1; no actual rho or s is evaluated.',
                'No rational-root computation or surviving-root feasibility inference.',
                'Only both proven connected sensitivities reject the specified twenty-eight-child family.',
                'Any constant/undetermined sensitivity leaves complete parent feasibility unresolved.',
                'Pinned custody does not self-authorize execution or establish semantic acceptance.',
                'No all-size extension, QM, empirical geometry, gravity or programme completion claim.',
            ],
        }
        output = canonical(report)
        budget()
        sys.stdout.buffer.write(output)
        sys.stdout.buffer.flush()
        budget()
    except BaseException as error:
        refuse(error, postchecks, descriptor_valid)



def main():
    global START
    START = time.monotonic()
    sys.set_int_max_str_digits(2*WORK_BITS)
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
