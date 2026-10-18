#!/usr/bin/env python3
"""Independent RI112 saved-certificate consumer. SOURCE PREPARATION ONLY.

Arithmetic/custody predecessor: RI107 audit_saved_certificate.py, 40917 bytes,
SHA256 0ed91135d1656cdf46efb43e580c888589282166fba889e4c9e0eb5becd55877.
Its normalized integer-pair, sparse-polynomial and direct-power primitives
are retained; the eight-profile/six-minor reconstruction below is independent
of the producer. No Fraction, producer, prefix, checker or solver imports.
Preparation guards refuse any missing source pins or control declarations.
Future authorization and custody acceptance remain outside this consumer.
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
    'checker': (57049, '73b204ba8acdefed418aa803ea95c0fc0dddba7c436ea1595996a01002f9287d'),
    'protocol': (17714, '0666dabeb554991e3ce7a70774666e2c162806b00f2d27541572131054b275bf'),
    'contract': (11987, '355336403094890e0e8f62dc0e6d92662d16fcf0b3270fcd00582605ca820271'),
}
FILES = ('ri88', 'ri111', 'ri109_adjudication', 'ri111_adjudication', 'candidate')
PROOFS = ('ri111', 'ri109_adjudication', 'ri111_adjudication')
SOURCES = PROOFS + ('checker', 'protocol', 'contract')
CUSTODY = ('producer_witness_stdout', 'producer_witness_custody',
           'producer_normal_custody', 'producer_optimized_custody',
           'consumer_source_review')
FIELDS = ('schema', 'accepted_inputs', 'accepted_sources', 'inputs',
          'selected_parent', 'records', 'scale_domain', 'reference_contrasts',
          'pivot_root_certificate', 'minors', 'common_gcd', 'decision',
          'coverage', 'limitations', 'arithmetic_limits', 'checker_sha256',
          'fixtures', 'gcd_fixtures', 'refusal_controls')
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
C3, C4, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 7)
ORDERS = (C3, C4, H5)
IDEALS = ((0, 1, 3, 7), (0, 1, 3, 7, 15), (0, 1, 3, 7, 15, 23, 31))
T1 = (0, 1, 3, 7, 7, 7, 7)
RECORDS, MINOR_RECORDS = tuple(range(8)), tuple(range(2, 8))
INPUT_BITS, WORK_BITS, TRANSIENT_BITS = 32768, 1048576, 2097154
MAX_OPS, MAX_TEXT, MAX_BYTES = 200000, 20000, 8388608
SECONDS, RSS_BYTES = 120, 536870912
ZERO, ONE = (0, 1), (1, 1)
START = None
OPS = 0

# Independently retained fixed interface declarations; never read from a candidate.
# They are declarations only, not mutations executed by this consumer.
CONTROL_PAIRS = (
    ('duplicate-json', 'duplicate-json-key'),
    ('decimal-json', 'noninteger-json-number'),
    ('nonfinite-json', 'noninteger-json-number'),
    ('unreduced-rational', 'noncanonical-rational'),
    ('boolean-rational', 'noncanonical-rational'),
    ('rational-text-bound', 'rational-text-budget'),
    ('integer-bit-bound', 'integer-bit-budget'),
    ('boolean-polynomial', 'exact-rational-required'),
    ('polynomial-degree', 'polynomial-shape-degree'),
    ('root-degree', 'root-polynomial-domain'),
    ('zero-polynomial', 'root-polynomial-domain'),
    ('zero-radius', 'root-radius-domain'),
    ('zero-polynomial-divisor', 'zero-polynomial-divisor'),
    ('zero-rational-divisor', 'zero-rational-divisor'),
    ('boolean-power', 'power-domain'),
    ('wrong-size-ri88', 'input-size-ri88'),
    ('wrong-hash-ri88', 'input-hash-ri88'),
    ('wrong-size-ri111', 'input-size-ri111'),
    ('wrong-hash-ri111', 'input-hash-ri111'),
    ('wrong-size-ri109_adjudication', 'input-size-ri109_adjudication'),
    ('wrong-hash-ri109_adjudication', 'input-hash-ri109_adjudication'),
    ('wrong-size-ri111_adjudication', 'input-size-ri111_adjudication'),
    ('wrong-hash-ri111_adjudication', 'input-hash-ri111_adjudication'),
    ('wrong-status-ri109', 'adjudication-status-ri109_adjudication'),
    ('wrong-status-ri111', 'adjudication-status-ri111_adjudication'),
    ('wrong-scope-ri111', 'adjudication-scope-ri111'),
    ('extra-ri88-field', 'ri88-fields'),
    ('missing-ri88-field', 'ri88-fields'),
    ('wrong-ri88-source', 'ri88-source'),
    ('wrong-dependencies', 'ri88-dependencies'),
    ('wrong-admission', 'ri88-admission'),
    ('wrong-prefix', 'ri88-actual-prefix'),
    ('boolean-coverage', 'ri88-coverage'),
    ('boolean-record', 'held-record-domain'),
    ('extra-record', 'held-record-domain'),
    ('boolean-order', 'held-order-types'),
    ('boolean-slot', 'held-slot-types'),
    ('missing-slot', 'held-slot-inventory'),
    ('duplicate-slot', 'held-slot-inventory'),
    ('nonpositive-slot', 'held-positive-normalized'),
    ('reordered-rows', 'selected-row-order'),
    ('missing-selected-row', 'selected-row-completeness'),
    ('duplicate-selected-row', 'duplicate-selected-row'),
    ('changed-empty-locality', 'held-empty-locality'),
    ('changed-proper-locality', 'held-proper-locality'),
    ('changed-twin', 'held-twin-symmetry'),
    ('lookup-C5', 'lookup-order-domain'),
    ('lookup-q6', 'lookup-order-domain'),
    ('lookup-q7', 'lookup-order-domain'),
    ('lookup-record', 'lookup-record-domain'),
    ('lookup-slot', 'lookup-slot-domain'),
    ('radius-eight-records', 'radius-E-domain'),
    ('zero-delta-j', 'accepted-delta-j-nonzero'),
    ('changed-radius', 'fixed-radius'),
    ('wrong-fixed-division', 'contrast-fixed-division'),
    ('missing-contrast-row', 'contrast-row-count'),
    ('boolean-contrast-record', 'contrast-row-order'),
    ('wrong-contrast-identity', 'minor-contrast-identity'),
    ('zero-minor-pivot', 'minor-pivot-nonzero'),
    ('missing-minor', 'minor-family-count'),
    ('duplicate-minor-label', 'minor-family-label-inventory'),
    ('reordered-minor-labels', 'minor-family-label-order'),
    ('boolean-minor-label', 'minor-family-label-types'),
    ('minor-degree', 'minor-family-polynomial-degree'),
    ('family-zero-radius', 'root-radius-domain'),
    ('boolean-decision', 'decision-count-domain'),
    ('all-zero-fictitious-gcd', 'decision-all-zero-shape'),
    ('extra-saved-field', 'saved-fields'),
    ('missing-saved-field', 'saved-fields'),
    ('saved-boolean-record', 'saved-exact-type'),
    ('saved-missing-row', 'saved-list-coverage'),
    ('saved-core-p', 'saved-exact-value'),
    ('saved-core-flag', 'saved-exact-value'),
    ('saved-contrast', 'saved-exact-value'),
    ('saved-minor-left-factor', 'saved-exact-value'),
    ('saved-minor-right-factor', 'saved-exact-value'),
    ('saved-minor-sign', 'saved-exact-value'),
    ('saved-minor-raw-division', 'saved-exact-value'),
    ('saved-zero-member-omission', 'saved-list-coverage'),
    ('saved-nonmonic-gcd', 'saved-exact-value'),
    ('saved-wrong-gcd', 'saved-exact-value'),
    ('saved-fold-previous', 'saved-exact-value'),
    ('saved-fold-quotient', 'saved-exact-value'),
    ('saved-divisibility-quotient', 'saved-exact-value'),
    ('saved-divisibility-remainder', 'saved-list-coverage'),
    ('saved-divisibility-reconstruction', 'saved-exact-value'),
    ('saved-all-zero-gcd', 'saved-exact-type'),
    ('saved-constant-disposition', 'saved-exact-value'),
    ('saved-surviving-disposition', 'saved-exact-value'),
    ('saved-root-count', 'saved-exact-value'),
    ('saved-endpoint-sign', 'saved-exact-value'),
    ('saved-derivative-gcd', 'saved-exact-value'),
    ('saved-square-free-quotient', 'saved-exact-value'),
    ('saved-square-free-remainder', 'saved-list-coverage'),
    ('saved-root-reconstruction', 'saved-exact-value'),
    ('saved-sturm-chain', 'saved-exact-value'),
    ('saved-negative-remainder', 'saved-exact-value'),
    ('saved-upper-inclusion', 'saved-exact-value'),
    ('saved-lower-exclusion', 'saved-exact-value'),
    ('saved-variations', 'saved-exact-value'),
    ('saved-actual-scale-claim', 'saved-exact-value'),
    ('saved-global-rejection', 'saved-exact-value'),
    ('saved-positive-repair', 'saved-exact-value'),
    ('saved-remaining-parent-claim', 'saved-exact-value'),
    ('saved-rational-roots-claim', 'saved-exact-value'),
    ('saved-actual-root-claim', 'saved-exact-value'),
    ('saved-radius', 'saved-exact-value'),
    ('saved-fixture-trailing-zero', 'saved-list-coverage'),
    ('saved-missing-gcd-fixture', 'saved-list-coverage'),
    ('saved-noncanonical', 'saved-canonical-bytes'),
)
CONTROL_COUNT = 110

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
GCD_FIXTURES = (
    ('all-zero', (), '1', None, None),
    ('zero-plus-constant', ((), ('2',), ('-1', '1')), '1', ('1',), 0),
    ('coprime-linears', (('-1', '1'), ('-2', '1')), '1', ('1',), 0),
    ('common-excluded-zero', (('0', '1'), ('0', '0', '1')), '1', ('0', '1'), 0),
    ('common-included-upper', (('-1', '1'), ('-2', '2')), '1', ('-1', '1'), 1),
    ('repeated-common-upper', (('1', '-2', '1'), ('-1', '3', '-3', '1')),
     '1', ('1', '-2', '1'), 1),
    ('degree-drop-negative-scaling', (('-1', '1', '0', '0'), ('2', '-2')),
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
    need(type(members) is list and len(members) == 6, 'six-family-members')
    need(all(type(item) is tuple and len(item) == 2 and type(item[0]) is int
             for item in members), 'family-member-types')
    need(tuple(item[0] for item in members) == MINOR_RECORDS, 'family-record-order')
    checked(radius)
    need(compare(radius) > 0, 'positive-family-radius')
    normalized = [(r, polynomial(p)) for r, p in members]
    need(all(degree(p) <= 3 for _, p in normalized), 'family-cubic-domain')
    nonzero = [r for r, p in normalized if p]
    zeros = [r for r, p in normalized if not p]
    if not nonzero:
        return {'branch': 'all-zero-minors', 'nonzero_records': [],
                'zero_records': zeros, 'folds': [], 'gcd_monic': None,
                'divisibility': [], 'root_certificate': None,
                'all_minors_identically_zero': True}
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
            'all_minors_identically_zero': False}


def decision(common):
    all_zero = common['all_minors_identically_zero']
    need(type(all_zero) is bool, 'decision-branch-type')
    if all_zero:
        need(common['branch'] == 'all-zero-minors'
             and common['gcd_monic'] is None and common['root_certificate'] is None,
             'decision-zero-family')
        count, common_degree = None, None
        disposition = 'unresolved-identically-zero-minors'
        exclusion = False
    else:
        need(common['branch'] == 'nonzero-gcd', 'decision-nonzero-family')
        count = common['root_certificate']['distinct_real_roots']
        common_degree = len(common['gcd_monic'])-1
        need(type(count) is int and 0 <= count <= common_degree <= 3, 'decision-root-domain')
        exclusion = count == 0
        disposition = 'certified-rank-obstruction' if exclusion else 'unresolved-common-real-roots'
    return {
        'disposition': disposition, 'common_gcd_degree': common_degree,
        'distinct_common_real_roots': count, 'rank_condition_identically_true': all_zero,
        'no_common_real_root_on_admissible_interval': exclusion,
        'restricted_28_child_repair_rejected': exclusion,
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


def gcd_fixture_evidence():
    output = []
    for name, prefix, radius, expected_gcd, expected_count in GCD_FIXTURES:
        declared = [list(p) for p in prefix] + [[] for _ in range(6-len(prefix))]
        members = [(r, from_list([parse_q(q) for q in p]))
                   for r, p in zip(MINOR_RECORDS, declared)]
        evidence = common_evidence(members, parse_q(radius))
        expected = list(expected_gcd) if expected_gcd is not None else None
        need(evidence['gcd_monic'] == expected, 'fixture-family-gcd:'+name)
        roots = evidence['root_certificate']
        count = roots['distinct_real_roots'] if roots is not None else None
        need(count == expected_count, 'fixture-family-count:'+name)
        output.append({'name': name, 'input_polynomials': declared, 'R': radius,
                       'expected_gcd': expected, 'expected_distinct_real_roots': expected_count,
                       'common_gcd': evidence, 'decision': decision(evidence),
                       'native_model_claimed': False})
    need(len(output) == 10 and len({x['name'] for x in output}) == 10, 'gcd-fixture-inventory')
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


def adjudication_metadata(ri109, ri111):
    for data, schema, status in (
        (ri109, 'ri109-root-final-mathematical-adjudication-v1',
         'ACCEPT_INDEPENDENT_RESTRICTED_27_CHILD_REPAIR_OBSTRUCTION'),
        (ri111, 'ri111-root-analytic-adjudication-v1',
         'ACCEPT_CONDITIONAL_COMPLETE_28_CHILD_REDUCTION_ONLY'),
    ):
        need(type(data) is dict and data.get('schema') == schema
             and data.get('status') == status, 'accepted-root-adjudication')
    need(ri111.get('actual_28_child_feasibility') == 'UNRESOLVED'
         and ri111.get('new_native_coefficients_or_scales_evaluated') is False
         and ri111.get('new_numerical_execution_admitted') is False,
         'accepted-RI111-source-only-boundary')


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
    expected = [(p, r) for p in ORDERS for r in RECORDS]
    selected, seen = [], set()
    for entry in data['held_rows']:
        keys(entry, ('order', 'record', 'probabilities'), 'held-entry')
        need(type(entry['order']) is list and all(type(x) is int for x in entry['order'])
             and type(entry['record']) is int, 'held-metadata-types')
        key = (tuple(entry['order']), entry['record'])
        if key[0] in ORDERS and key[1] in RECORDS:
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
    for order, inventory in zip(ORDERS, IDEALS):
        for r in RECORDS:
            need(held[(order, r)][0] == held[(order, 0)][0], 'held-empty-locality')
        for ideal in inventory[:-1]:
            by_precursor = {}
            for r in RECORDS:
                local = r & ideal
                value = held[(order, r)][ideal]
                if local in by_precursor:
                    need(value == by_precursor[local], 'held-proper-record-locality')
                else:
                    by_precursor[local] = value
    for r in RECORDS:
        need(held[(H5, r)][15] == held[(H5, r)][23], 'held-twin-symmetry')
    return held, selected


def held_probability(held, order, record, ideal):
    need(type(order) is tuple and all(type(v) is int for v in order) and order in ORDERS,
         'held-lookup-order')
    need(type(record) is int and record in RECORDS, 'held-lookup-record')
    need(type(ideal) is int and ideal in IDEALS[ORDERS.index(order)], 'held-lookup-ideal')
    return held[(order, record)][ideal]


def record_evidence(held, r):
    es, ks = [], []
    for s in (0, 1, 3, 7):
        a = held_probability(held, C3, r, s)
        b = held_probability(held, C4, r, s)
        g = held_probability(held, H5, r, s)
        # Quotient-first grouping differs from producer multiply/divide grouping.
        ratio = over(g, b)
        es.append(times(a, power(ratio, 3)))
        ks.append(over(times(power(a, 3), power(ratio, 6)), power(b, 2)))
    c = held_probability(held, C4, r, 15)
    h = held_probability(held, H5, r, 15)
    j = held_probability(held, H5, r, 31)
    cap_one = times(pair(3), over(power(h, 2), c))
    cap_two = times(pair(3), j)
    e = plus(sum_q(es), plus(cap_one, cap_two))
    v = times(h, power(over(h, c), 2))
    k = sum_q(ks)
    # Independently form the core expression, not merely copying ks[-1].
    a_core = held_probability(held, C3, r, 7)
    b_core = held_probability(held, C4, r, 7)
    g_core = held_probability(held, H5, r, 7)
    core = over(times(power(a_core, 3), power(g_core, 6)), power(b_core, 8))
    need(core == ks[3] and compare(core) > 0, 'core-K-summand')
    u = from_list([pair(4), times(pair(-4), e), times(pair(6), j), times(pair(4), v), k])
    entry = {'record': r, 'E_terms': [text(q) for q in es],
             'E_one_cap_total': text(cap_one), 'E_two_cap_total': text(cap_two),
             'E': text(e), 'v_star': text(v), 'K_terms': [text(q) for q in ks],
             'K': text(k), 'c': text(c), 'h': text(h), 'j': text(j),
             'U_padded': padded(u, 5), 'p': text(core), 'p_is_core_K_term': True}
    return (e, j, v, k, core), u, entry


def pin_dict(role):
    need(type(PIN[role]) is tuple, 'source-pin-unbound:'+role)
    return {'bytes': PIN[role][0], 'sha256': PIN[role][1]}


def reconstruct(data):
    preparation_ready()
    held, rows = accepted_rows(data)
    scalars, us, records = [], [], []
    for r in RECORDS:
        values, u, evidence = record_evidence(held, r)
        scalars.append(values)
        us.append(u)
        records.append(evidence)
    es = [scalars[r][0] for r in (0, 1)]
    maximum = es[0] if compare(es[0], es[1]) >= 0 else es[1]
    radius = over(ONE, times(pair(2), plus(ONE, maximum)))
    need(compare(radius) > 0, 'radius-positive')
    contrasts, deltas, ps, raws = [], {}, {}, {}
    for r in range(1, 8):
        d = tuple(minus(scalars[r][i], scalars[0][i]) for i in range(5))
        p = from_list([times(pair(f), q) for f, q in zip((-4, 6, 4, 1), d[:4])])
        raw = poly_add(us[r], poly_negative(us[0]))
        quotient, remainder = quotient_remainder(raw, {1: ONE})
        need(not remainder and quotient == p and raw == poly_product({1: ONE}, p),
             'reference-fixed-rho-division')
        need(degree(p) <= 3, 'reference-cubic-bound')
        if r == 1:
            need(d[1] != ZERO and bool(p), 'accepted-pivot-nonzero')
        deltas[r], ps[r], raws[r] = d, p, raw
        contrasts.append({'record': r, 'delta_p': text(d[4]), 'delta_E': text(d[0]),
                          'delta_j': text(d[1]), 'delta_v_star': text(d[2]),
                          'delta_K': text(d[3]), 'P_padded': padded(p, 4),
                          'U_minus_reference_padded': padded(raw, 5),
                          'fixed_divisor': 'rho', 'quotient_matches_closed_formula': True,
                          'degree': degree(p), 'is_zero': not bool(p)})
    pivot = root_evidence(ps[1], radius)
    need(pivot['distinct_real_roots'] == 0, 'accepted-pivot-root-exclusion')
    minors, family = [], []
    for r in MINOR_RECORDS:
        left = poly_product({0: deltas[r][4]}, ps[1])
        right = poly_product({0: deltas[1][4]}, ps[r])
        minor = poly_add(left, poly_negative(right))
        raw = poly_add(poly_product({0: deltas[r][4]}, raws[1]),
                       poly_negative(poly_product({0: deltas[1][4]}, raws[r])))
        quotient, remainder = quotient_remainder(raw, {1: ONE})
        need(not remainder and quotient == minor
             and raw == poly_product({1: ONE}, minor), 'minor-fixed-rho-division')
        need(degree(minor) <= 3, 'minor-cubic-bound')
        minors.append({'record': r, 'delta_p': text(deltas[r][4]),
                       'pivot_delta_p': text(deltas[1][4]),
                       'left_padded': padded(left, 4), 'right_padded': padded(right, 4),
                       'M_padded': padded(minor, 4), 'raw_U_combination_padded': padded(raw, 5),
                       'fixed_divisor': 'rho', 'quotient_matches_closed_formula': True,
                       'degree': degree(minor), 'is_zero': not bool(minor)})
        family.append((r, minor))
    common = common_evidence(family, radius)
    margins = [minus(ONE, times(radius, e)) for e in es]
    need(all(compare(m, pair(1, 2)) > 0 for m in margins), 'lower-full-margins')
    result = {
        'schema': 'ri112-one-column-rank-certificate-v1',
        'accepted_inputs': {'ri88': pin_dict('ri88')},
        'accepted_sources': {r: pin_dict(r) for r in PROOFS},
        'inputs': {'held_rows': rows,
                   'selected_order': [name+':'+str(r) for name in ('C3', 'C4', 'H5') for r in RECORDS],
                   'prefix_replayed': False, 'H_or_z_values_read': False,
                   'transport_basis': 'RI111 maximal-bit and RI85 unique/twin-top transport',
                   'proper_locality_checked': True},
        'selected_parent': list(T1), 'records': records,
        'scale_domain': {'R': text(radius), 'selected_E': [text(e) for e in es],
                         'interval': '0<rho<=R', 'lower_full_margins_at_R': [text(m) for m in margins],
                         'actual_rho_evaluated': False, 'amplitude': '1/4', 'seed_unchanged': True},
        'reference_contrasts': contrasts, 'pivot_root_certificate': pivot,
        'minors': minors, 'common_gcd': common, 'decision': decision(common),
        'coverage': {'held_rows': 24, 'held_probability_slots': 128, 'records': 8,
                     'reference_contrasts': 7, 'rank_minors': 6,
                     'H_or_z_arithmetic_values': 0, 'new_q6_q7_rows': 0,
                     'native_polynomial_degree_cap': 3},
        'limitations': {'real_roots_do_not_imply_rational_roots': True,
                        'roots_in_outer_interval_do_not_locate_actual_scale': True,
                        'complete_all_size_extension_not_claimed': True,
                        'QM_geometry_gravity_derivation_not_claimed': True,
                        'restricted_candidate_only': True, 'external_custody_required': True,
                        'remaining_parent_feasibility_not_decided': True,
                        'rank_compatibility_not_positive_repair': True},
        'arithmetic_limits': {'input_rational_bits': INPUT_BITS, 'working_rational_bits': WORK_BITS,
                              'transient_integer_bits': TRANSIENT_BITS, 'counted_operations': MAX_OPS,
                              'rational_text_characters': MAX_TEXT, 'output_bytes': MAX_BYTES,
                              'active_child_seconds': SECONDS, 'resident_bytes': RSS_BYTES},
        'checker_sha256': PIN['checker'][1], 'fixtures': fixture_evidence(),
        'gcd_fixtures': gcd_fixture_evidence(),
        'refusal_controls': [{'name': n, 'reason': r} for n, r in CONTROL_PAIRS],
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
    for item in failure['postchecks'][:15]:
        items.append({key: clipped(value) if type(value) is str else value
                      for key, value in item.items()})
    diagnostic = dict(failure, error=clipped(failure['error']), postchecks=items,
                      diagnostic_text_limit=2048, normal_budget_reapplied=False)
    raw = (json.dumps(diagnostic, sort_keys=True, separators=(',', ':'),
                      ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
    # Fifteen bounded records remain bounded with worst-case JSON escaping.
    if len(raw) > 1048576:
        return b'{"schema":"ri112-audit-failure-v1","status":"REFUSED","diagnostic_overflow":true}\n'
    return raw


def descriptor_entries(value, descriptor_path, own_path):
    keys(value, ('schema', 'phase', 'files', 'accepted_sources', 'audit_source',
                 'custody_dependencies'), 'descriptor')
    need(value['schema'] == 'ri112-independent-audit-input-v1'
         and value['phase'] == 'fixed_saved_certificate_audit', 'descriptor-mode')
    keys(value['files'], FILES, 'descriptor-files')
    keys(value['accepted_sources'], SOURCES, 'descriptor-sources')
    bindings = []
    for group, roles in (('files', FILES), ('accepted_sources', SOURCES)):
        for role in roles:
            entry = value[group][role]
            entry_shape(entry)
            if role != 'candidate':
                exact({k: entry[k] for k in ('bytes', 'sha256')}, pin_dict(role), 'fixed-pin:'+role)
            bindings.append((group+'.'+role, entry))
    entry_shape(value['audit_source'])
    need(value['audit_source']['path'] == own_path, 'executing-audit-source-path')
    bindings.append(('audit_source', value['audit_source']))
    custody = value['custody_dependencies']
    need(type(custody) is list and len(custody) == 5, 'custody-count')
    for role, item in zip(CUSTODY, custody):
        keys(item, ('role', 'path', 'bytes', 'sha256'), 'custody-entry')
        need(type(item['role']) is str and item['role'] == role, 'custody-order')
        entry = {k: item[k] for k in ('path', 'bytes', 'sha256')}
        entry_shape(entry)
        bindings.append(('custody.'+role, entry))
    for role in PROOFS:
        exact(value['accepted_sources'][role], value['files'][role], 'proof-alias:'+role)
    unique, role_paths = {}, {}
    for role, entry in bindings:
        name = entry['path']
        need(name != descriptor_path, 'descriptor-payload-path-alias')
        role_paths[role] = name
        if name in unique:
            expected_alias = role.startswith('accepted_sources.') and role.split('.')[-1] in PROOFS
            need(expected_alias and name == value['files'][role.split('.')[-1]]['path'],
                 'unexpected-payload-alias')
            exact(entry, unique[name], 'same-file-alias')
        else:
            unique[name] = entry
    need(len(bindings) == 17 and len(unique) == 14, 'seventeen-roles-fourteen-files')
    candidate = value['files']['candidate']
    witness = custody[0]
    exact({k: candidate[k] for k in ('bytes', 'sha256')},
          {k: witness[k] for k in ('bytes', 'sha256')}, 'candidate-witness-pin')
    return bindings, unique, role_paths


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
        bindings, unique, role_paths = descriptor_entries(descriptor, descriptor_entry['path'], own_path)
        exact(descriptor['audit_source'], own_entry, 'admitted-self-source-identity')
        # Every source, data and custody identity precedes scientific parsing.
        for name, entry in unique.items():
            if name != own_path:
                snapshots[name] = stable_read(entry)
        for role, entry in bindings:
            exact(identity(snapshots[entry['path']][0]),
                  {k: entry[k] for k in ('bytes', 'sha256')}, 'captured-role:'+role)
        candidate_raw = snapshots[role_paths['files.candidate']][0]
        witness_raw = snapshots[role_paths['custody.producer_witness_stdout']][0]
        need(candidate_raw == witness_raw, 'candidate-not-genuine-stdout-copy')
        adjudication_metadata(
            json_load(snapshots[role_paths['files.ri109_adjudication']][0]),
            json_load(snapshots[role_paths['files.ri111_adjudication']][0]))
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
        failure = {'schema': 'ri112-audit-failure-v1', 'status': 'REFUSED',
                   'error_type': type(original_error).__name__ if original_error else 'PostcheckFailure',
                   'error': str(original_error) if original_error else 'postcheck failure',
                   'postchecks': postchecks, 'descriptor_postcheck_admitted': descriptor_valid,
                   'scientific_disposition_emitted': False}
        sys.stderr.buffer.write(failure_bytes(failure))
        sys.stderr.buffer.flush()
        raise AuditFailure('audit-refused; see preserved stderr/postchecks') from original_error
    need(len(postchecks) == 15 and reconstructed is not None, 'complete-postcheck-coverage')
    for role, entry in bindings:
        exact(identity(snapshots[entry['path']][0]),
              {k: entry[k] for k in ('bytes', 'sha256')}, 'final-role:'+role)
    report = {
        'schema': 'ri112-independent-complete-one-column-rank-audit-v1',
        'status': 'all_saved_fields_independently_match',
        'descriptor_identity': identity(descriptor_snapshot[0]),
        'audit_source_identity': identity(snapshots[own_path][0]),
        'accepted_source_identities': {role: pin_dict(role) for role in SOURCES},
        'payload_role_bindings': [{'role': role, **entry} for role, entry in bindings],
        'unique_payload_paths': 14, 'payload_role_count': 17,
        'reconstructed_certificate_identity': identity(reconstructed),
        'complete_top_level_sections': {name: identity(canonical(expected[name])) for name in FIELDS},
        'reconstructed_certificate': expected,
        'postchecks': postchecks, 'independent_counted_operations': OPS,
        'declared_producer_controls': {'count': CONTROL_COUNT,
                                      'ordered_pairs': expected['refusal_controls'],
                                      'producer_controls_executed_by_consumer': False},
        'independently_rebuilt_fixture_count': 16,
        'independently_rebuilt_gcd_fixture_count': 10,
        'custody_semantics_self_adjudicated': False,
        'independence': [
            'Normalized integer pairs and cross-cancellation; no Fraction or producer imports.',
            'Quotient-first profile reconstruction plus a separate direct core-p expression.',
            'Sparse polynomial products, fixed-rho divisions and monic family gcd folds.',
            'Exact long-division reconstruction and direct-power endpoints, not producer Horner.',
            'Every one of nineteen sections and complete canonical bytes is independently rebuilt.',
            'Sixteen root and ten gcd-family fixtures are independently reconstructed.',
            'Producer refusal names/reasons are declarations, not consumer-executed mutations.',
        ],
        'limits': [
            'Inherited RI88 probabilities and accepted RI111/RI109 premises are not rederived.',
            'Only twenty-four held rows and 128 probabilities; no H/z or new q6/q7 table.',
            'Radius uses only E0 and E1; no actual rho, s, beta or Gamma is evaluated.',
            'No rational-root computation or surviving-root feasibility inference.',
            'Only the specified twenty-eight-child family can be rejected by this rank test.',
            'All-zero minors or surviving common roots leave remaining parent feasibility open.',
            'Pinned custody does not self-authorize execution or establish semantic acceptance.',
            'No all-size extension, QM, empirical geometry, gravity or programme completion claim.',
        ],
    }
    output = canonical(report)
    budget()
    sys.stdout.buffer.write(output)
    sys.stdout.buffer.flush()
    budget()


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
