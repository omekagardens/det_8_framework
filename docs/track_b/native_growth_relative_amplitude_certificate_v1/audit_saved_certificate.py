#!/usr/bin/env python3
"""RI95 independent data-only complete-certificate consumer.

SOURCE PREPARATION ONLY until a separately accepted concrete descriptor,
caller, freeze and authorization admit an execution. No producer/prefix
module is imported. Arithmetic is independently reconstructed from RI94,
using dense coefficient rectangles and combinations of omitted maxima.
The RI91 input supplies only the seventeen fixed boundary coordinates.
This program emits a report; it never writes a certificate or other file.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import os
import resource
import signal
import stat
import sys
import time


ACCEPTED = {
    'ri88': {'bytes': 1828149, 'sha256': 'ad029d61adc2c8edbe4ae2c3c0969310762a70b411497d4404aa3b3c504f0f5b'},
    'ri91': {'bytes': 364312, 'sha256': '9e48c437e90cbeef6284ddbcdf5ec915aa520217172f580ef900e5c2bccd37ed'},
}
SOURCES = {
    'checker': {'bytes': 79250, 'sha256': '572b156ce1f8833a23288e2b079cf48c4a1742e8e847b3bacb5652879d772639'},
    'proof': {'bytes': 25150, 'sha256': '65645454993a81b70a0d9cd278eb137cd6b218055b1cb026f9950b7cb8895844'},
    'protocol': {'bytes': 24962, 'sha256': '043d01630d78ddeab718fc15a1ba2b1ea9ff36ffd4fb749150c37b033a06743d'},
}
RI88_SOURCE = '93eb721e933d90ba922b62f8a6844b64529d2acee1ae3bb3e15c81c4de153568'
RI91_SOURCE = 'b0a40587be40afa6972664784ec1844f1463564ba93d5ba6cd2b21173986770e'
RI85_PROOF = 'e0dd0b046d80564ddc4e6ffef78853156f5c418b327917f1d5fadc4e229ab58a'
RI89_PROOF = '56c45bb5aba5e9fa0ab1f09ff959a73235939cc850e6fdde91a4cc39180b5cd1'
DEPENDENCIES = {
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri74_checker': 'edcf26c071d56d2db4a5b553dff9be4ea926e375e59814170892b6e34a473c3c',
}
RI88_FIELDS = set('admission checker_sha256 compact_rows coverage dependencies design_sha256 domain exact_decision expanded_rows held_rows parameters prefix refusal_controls schema structure transported_audit width_target'.split())
RI91_FIELDS = set('schema checker_sha256 design_sha256 design_bytes accepted_input inputs selected_parent records scale_domain cross_multiplication decision coverage limitations refusal_controls'.split())
RESULT_FIELDS = set('schema design_sha256 design_bytes accepted_inputs inputs selected_parent records scale_domain cross_multiplication full_complement_s_endpoints fixed_division_evidence tensor_evidence decision coverage limitations checker_sha256 refusal_controls'.split())
C3, C4, H5 = (0, 1, 3), (0, 1, 3, 7), (0, 1, 3, 7, 7)
LOWER, UPPER = (0, 1, 3, 7, 7, 7), (0, 1, 3, 7, 7, 7, 7)
LEAVES = (C3, C4, H5)
LEAF_IDEALS = {C3: (0, 1, 3, 7), C4: (0, 1, 3, 7, 15), H5: (0, 1, 3, 7, 15, 23, 31)}
CAPS = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 0, 3), (0, 0, 1, 1), (0, 0, 1, 2),
        (0, 0, 1, 3), (0, 0, 1, 5), (0, 0, 3, 3), (0, 1, 1, 1), (0, 1, 1, 3), (0, 1, 3, 3))
WIDTHS = (4, 3, 3, 3, 2, 2, 2, 2, 3, 2, 2)
E_CEILING = F(1, 4)
CUSTODY_ROLES = ('producer_witness_stdout', 'producer_witness_custody', 'producer_normal_custody',
                 'producer_optimized_custody', 'consumer_source_review')
FIXTURES = ('positive', 'negative-generic-orientation', 'weak-A-zero', 'blind', 'included-binding-s-endpoint',
            'conservative-both-endpoints', 'positive-mixed-amplitude-basis', 'endpoint-positive-interior-zero',
            'strict-corner-only-support', 'included-rho-edge-zero', 'included-epsilon-edge-zero', 'unequal-axis-scaling')

# These strings are schema declarations from the reviewed protocol, not
# executable copies of producer controls and not evidence they ran.
DECLARED_CONTROLS = (
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
START = None


class AuditError(ValueError):
    pass


def need(condition, explanation):
    if not condition:
        raise AuditError(explanation)


def object_keys(value, names, context):
    need(type(value) is dict and set(value) == set(names), context + ': exact fields')


def canonical_bytes(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')


def byte_identity(body):
    return {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def json_body(body):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    def no_number(value):
        raise AuditError('decimal/nonfinite JSON number: '+value)
    return json.loads(body.decode('ascii'), object_pairs_hook=unique, parse_float=no_number, parse_constant=no_number)


def fraction(text):
    need(type(text) is str, 'canonical rational string required')
    try:
        value = F(text)
    except (ValueError, ZeroDivisionError) as error:
        raise AuditError('invalid rational string') from error
    need(str(value) == text, 'noncanonical rational string')
    return value


def identical(given, rebuilt, trail='certificate'):
    need(type(given) is type(rebuilt), trail+': exact type')
    if type(rebuilt) is dict:
        need(set(given) == set(rebuilt), trail+': complete field inventory')
        for key in rebuilt:
            identical(given[key], rebuilt[key], trail+'/'+key)
    elif type(rebuilt) is list:
        need(len(given) == len(rebuilt), trail+': complete list inventory')
        for position, (left, right) in enumerate(zip(given, rebuilt)):
            identical(left, right, trail+'/'+str(position))
    else:
        need(given == rebuilt, trail+': exact scalar')


def check_pin(pin):
    object_keys(pin, ('bytes', 'sha256'), 'pin')
    need(type(pin['bytes']) is int and pin['bytes'] > 0, 'positive exact byte size')
    digest = pin['sha256']
    need(type(digest) is str and len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'lowercase SHA256')


def read_fixed(entry):
    object_keys(entry, ('path', 'bytes', 'sha256'), 'file entry')
    pin = {key: entry[key] for key in ('bytes', 'sha256')}
    check_pin(pin)
    need(type(entry['path']) is str, 'literal file path')
    path = Path(entry['path'])
    need(path.is_absolute() and str(path.resolve()) == entry['path'], 'absolute symlink-free literal input')
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode), 'regular file required')
    def signature(info):
        return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
    with path.open('rb') as handle:
        opened = os.fstat(handle.fileno())
        need(signature(before) == signature(opened), 'file replaced while opening')
        body = handle.read()
        after_read = os.fstat(handle.fileno())
    after = path.lstat()
    need(signature(before) == signature(after_read) == signature(after), 'file changed while reading')
    need(byte_identity(body) == pin, 'file byte pin mismatch: '+entry['path'])
    return body, signature(after)


def budget():
    need(START is None or time.monotonic()-START <= 120, '120-second internal envelope')
    resident = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    need((resident if sys.platform == 'darwin' else resident*1024) <= 536870912, '512-MiB internal envelope')


# A polynomial is always a complete immutable 9-by-5 rectangle. No sparse
# producer arithmetic, dynamic valuation or fitted degree is reused.
def blank():
    return [[F(0) for _ in range(5)] for _ in range(9)]


def freeze(matrix):
    need(len(matrix) == 9 and all(len(row) == 5 for row in matrix), 'dense polynomial dimensions')
    need(all(type(q) is F for row in matrix for q in row), 'exact dense coefficients')
    return tuple(tuple(row) for row in matrix)


def mono(a=0, b=0, coefficient=F(1)):
    need(type(a) is int and 0 <= a <= 8 and type(b) is int and 0 <= b <= 4 and type(coefficient) is F, 'fixed monomial')
    result = blank()
    result[a][b] = coefficient
    return freeze(result)


def plus(*polynomials):
    out = blank()
    for p in polynomials:
        for a in range(9):
            for b in range(5):
                out[a][b] += p[a][b]
    return freeze(out)


def times_scalar(p, q):
    need(type(q) is F, 'exact multiplier')
    return freeze([[p[a][b]*q for b in range(5)] for a in range(9)])


def minus(left, right):
    return plus(left, times_scalar(right, F(-1)))


def convolve(left, right):
    out = blank()
    for a in range(9):
        for b in range(5):
            if not left[a][b]:
                continue
            for c in range(9):
                for d in range(5):
                    if right[c][d]:
                        need(a+c <= 8 and b+d <= 4, 'polynomial product outside fixed analytic rectangle')
                        out[a+c][b+d] += left[a][b]*right[c][d]
    return freeze(out)


def exponentiate(p, exponent):
    need(type(exponent) is int and 0 <= exponent <= 6, 'fixed algebraic exponent')
    value = mono()
    for _ in range(exponent):
        value = convolve(value, p)
    return value


def cap(p, rho, epsilon):
    need(all(not p[a][b] or (a <= rho and b <= epsilon) for a in range(9) for b in range(5)), 'prescribed polynomial bidegree')
    return p


def terms(p):
    return [[a, b, str(p[a][b])] for a in range(9) for b in range(5) if p[a][b]]


def value_at(p, rho, epsilon):
    need(type(rho) is F and type(epsilon) is F, 'exact proof endpoints')
    return sum((p[a][b]*rho**a*epsilon**b for a in range(9) for b in range(5)), F(0))


def prescribed_quotient(p, degree):
    need(degree in (2, 6) and type(degree) is int, 'fixed quotient degree')
    cap(p, degree+2, 4)
    need(all(p[a][b] == 0 for a in range(9) for b in range(5) if a < 2 or b == 0), 'epsilon*rho^2 valuation')
    out = blank()
    for a in range(degree+1):
        for b in range(4):
            out[a][b] = p[a+2][b+1]
    result = freeze(out)
    need(convolve(mono(2, 1), result) == p, 'fixed quotient reconstruction')
    return cap(result, degree, 3)


def quotient_record(p, degree):
    q = prescribed_quotient(p, degree)
    grid = [[str(p[a][b]) for b in range(5)] for a in range(degree+3)]
    zeros = [[a, b, grid[a][b]] for a in range(degree+3) for b in range(5) if a < 2 or b == 0]
    return {'raw_bidegree_bound': [degree+2, 4], 'quotient_bidegree_bound': [degree, 3],
            'rho_factor': 2, 'epsilon_factor': 1, 'raw_padded_power': grid,
            'forbidden_zero_coordinates': zeros, 'quotient': terms(q), 'reconstructed_raw': terms(p),
            'dynamic_valuation_used': False}


def ideals(order):
    need(order in LEAVES+(LOWER, UPPER), 'only frozen structural parents')
    return tuple(mask for mask in range(1 << len(order))
                 if all(not mask & (1 << v) or (order[v] & mask) == order[v] for v in range(len(order))))


def deletions(order, record, ideal):
    need(order in (LOWER, UPPER) and type(record) is int and record in (0, 1), 'fixed deletion domain')
    need(type(ideal) is int and ideal in ideals(order)[:-1], 'individual proper ideal')
    maxima = [v for v in range(len(order)) if all(not order[w] & (1 << v) for w in range(len(order)))]
    omitted = [v for v in maxima if not ideal & (1 << v)]
    choices = [subset for size in range(1, len(omitted)+1) for subset in combinations(omitted, size)]
    # Descending masks are serialization order only; combinations derive the
    # complete subsets independently of the producer's submask traversal.
    choices.sort(key=lambda subset: sum(1 << v for v in subset), reverse=True)
    for subset in choices:
        kept = [v for v in range(len(order)) if v not in subset]
        positions = {old: new for new, old in enumerate(kept)}
        def restrict(mask):
            return sum(1 << positions[v] for v in kept if mask & (1 << v))
        child = tuple(restrict(order[v]) for v in kept)
        need(child in LEAVES+(LOWER,), 'induced source remains held or symbolic lower')
        yield (sum(1 << v for v in subset), kept, child, restrict(record), restrict(ideal),
               1 if len(subset) % 2 else -1)


def accepted_seed(data):
    object_keys(data, RI88_FIELDS, 'RI88')
    need(data['schema'] == 'ri88-four-vertex-cap-v1' and data['checker_sha256'] == RI88_SOURCE
         and data['design_sha256'] == RI85_PROOF, 'RI88 accepted provenance')
    identical(data['dependencies'], DEPENDENCIES, 'inherited source pins')
    need(data['admission']['epsilon'] == '1/4' and data['admission']['later_h_prescribed'] is False
         and data['admission']['numerical_a6_evaluated'] is False
         and data['exact_decision']['disposition'] == 'positive-finite-width-bias', 'accepted seed scope')
    prefix = data['prefix']
    need(prefix['problem_sha256'] == 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
         and prefix['actual_probability_manifest_sha256'] == '7e27822390387111bf01b3c8e67a12a8b06a9023d2bd3f8bacfa8aeab20c0378'
         and type(prefix['canonical_lex_stages']) is int and prefix['canonical_lex_stages'] == 69, 'held strict-prefix identity')
    coverage = data['coverage']
    need(type(coverage['held_marked_rows']) is int and coverage['held_marked_rows'] == 40
         and type(coverage['held_probability_slots']) is int and coverage['held_probability_slots'] == 224, 'RI88 retained coverage')
    support = [{'index': j, 'cap': list(p), 'order': list(C3)+[7+8*x for x in p], 'width': WIDTHS[j]}
               for j, p in enumerate(CAPS)]
    identical(data['structure']['ordered_support'], support, 'complete eleven-support metadata')
    need(type(data['held_rows']) is list and len(data['held_rows']) == 40, 'held metadata inventory')
    selected, held = [], {}
    for entry in data['held_rows']:
        object_keys(entry, ('order', 'record', 'probabilities'), 'held metadata')
        need(type(entry['order']) is list and all(type(x) is int for x in entry['order'])
             and type(entry['record']) is int, 'exact held metadata')
        order, record = tuple(entry['order']), entry['record']
        if order not in LEAVES or record not in (0, 1):
            continue
        need((order, record) not in held, 'duplicate selected row')
        slots = entry['probabilities']
        need(type(slots) is list and all(type(x) is list and len(x) == 2 and type(x[0]) is int for x in slots), 'held slot types')
        need([x[0] for x in slots] == list(LEAF_IDEALS[order]) == list(ideals(order)), 'complete individual held ideals')
        values = {mask: fraction(q) for mask, q in slots}
        need(all(q > 0 for q in values.values()) and sum(values.values(), F(0)) == 1, 'positive normalized held row')
        held[(order, record)] = values
        selected.append(entry)
    need(list(held) == [(p, r) for p in LEAVES for r in (0, 1)], 'six ordered selected rows')
    for p in LEAVES:
        for s in ideals(p):
            if not s & 1:
                need(held[(p, 0)][s] == held[(p, 1)][s], 'precursor record locality')
    for r in (0, 1):
        need(held[(H5, r)][15] == held[(H5, r)][23], 'twin-top symmetry')
    all_h = data['admission']['h']
    need(type(all_h) is list and len(all_h) == 11 and all(type(q) is str for q in all_h), 'eleven retained H strings')
    h = [fraction(text) for text in all_h[:3]]
    need(h[0] == F(5, 4) and all(F(3, 4) <= q <= F(5, 4) for q in h), 'three admitted multipliers')
    direction = [4*(q-1) for q in h]
    evidence = {'held_rows': selected, 'H': [str(q) for q in h], 'z': [str(q) for q in direction],
                'full_support_provenance': {'ordered_support': support, 'all_eleven_H_strings': all_h,
                                           'arithmetic_indices': [0, 1, 2], 'other_eight_H_used_only_as_authenticated_strings': True},
                'provenance': {'schema': data['schema'], 'checker_sha256': RI88_SOURCE, 'design_sha256': RI85_PROOF,
                               'dependencies': DEPENDENCIES, 'actual_probability_manifest_sha256': prefix['actual_probability_manifest_sha256']},
                'helper_or_prefix_replayed': False}
    return held, direction, evidence


def held_leaf(held, order, record, part):
    need(order in LEAVES and type(record) is int and record in (0, 1) and part in LEAF_IDEALS[order], 'authorized held leaf only')
    proper = part != (1 << len(order))-1
    local = record & part if proper else record
    q = held[(order, local)][part]
    return q, {'order': list(order), 'raw_record': record, 'induced_precursor': part,
               'proper_locality_applied': proper, 'query_record': local, 'probability': str(q), 'top_marks_zero': True}


def lower_route(held, record):
    coefficients, rows = {}, []
    for s in ideals(LOWER)[:-1]:
        numerator, denominator, factors = F(1), F(1), []
        for mask, kept, p, raw, t, sign in deletions(LOWER, record, s):
            q, metadata = held_leaf(held, p, raw, t)
            if sign == 1:
                numerator *= q
            else:
                denominator *= q
            factors.append({'deleted_mask': mask, 'kept_vertices': kept, 'source': metadata, 'exponent': sign})
        coefficients[s] = numerator/denominator
        need(coefficients[s] > 0, 'positive lower potential')
        rows.append({'ideal': s, 'coefficient': str(coefficients[s]), 'factors': factors})
    need(len(rows) == 10 and sum(len(row['factors']) for row in rows) == 40, 'lower 10-slot/40-factor coverage')
    return coefficients, sum(coefficients.values(), F(0)), rows


def individual_multiplier(precursor, direction):
    need(precursor in ideals(LOWER), 'individual lower ideal')
    if precursor & 7 != 7 or precursor == 63:
        return mono(), None
    count = sum(bool(precursor & (1 << v)) for v in range(3, 6))
    need(count in (0, 1, 2), 'frozen modified cap class')
    return plus(mono(), mono(0, 1, direction[count])), count


def signed_constant_denominators(factors):
    """In this frozen domain every negative factor is a held scalar.

    This numerator/constant-denominator proof is independent of the producer
    Laurent-monomial multiplication and refuses an unproved inversion.
    """
    numerator, denominator = mono(), F(1)
    for p, sign in factors:
        need(type(sign) is int and sign in (-1, 1), 'alternating factor sign')
        if sign == 1:
            numerator = convolve(numerator, p)
        else:
            need(p == mono(coefficient=p[0][0]) and p[0][0] > 0, 'negative factor must be positive held constant')
            denominator *= p[0][0]
    return cap(times_scalar(numerator, 1/denominator), 4, 4)


def upper_route(held, direction, record, lower):
    baseline_sum, changed_sum = mono(coefficient=F(0)), mono(coefficient=F(0))
    rows = []
    for s in ideals(UPPER)[:-1]:
        factors, old_operands, new_operands = [], [], []
        for mask, kept, p, raw, t, sign in deletions(UPPER, record, s):
            if p == LOWER:
                coefficients, total, _ = lower[raw]
                need(sign == 1, 'symbolic lower factors have positive exponent')
                if t == 63:
                    operand = minus(mono(), mono(1, 0, total))
                    source = {'kind': 'symbolic-full-complement', 'lower_proper_sum': str(total), 'expression': '1-rho*E'}
                else:
                    need(t in coefficients, 'lower proper slot exists')
                    operand = mono(1, 0, coefficients[t])
                    source = {'kind': 'symbolic-proper-monomial', 'lower_ideal': t,
                              'lower_potential_coefficient': str(coefficients[t]), 'expression': 'rho*u6'}
                multiplier, index = individual_multiplier(t, direction)
            else:
                q, source = held_leaf(held, p, raw, t)
                operand, multiplier, index = mono(coefficient=q), mono(), None
            modified = convolve(operand, multiplier)
            old_operands.append((operand, sign))
            new_operands.append((modified, sign))
            factors.append({'deleted_mask': mask, 'kept_vertices': kept, 'induced_order': list(p),
                            'raw_record': raw, 'induced_precursor': t, 'source': source, 'exponent': sign,
                            'baseline_factor': terms(operand), 'amplitude_multiplier': terms(multiplier),
                            'multiplier_index': index, 'changed_factor': terms(modified)})
        old = signed_constant_denominators(old_operands)
        new = signed_constant_denominators(new_operands)
        count = sum(bool(s & (1 << v)) for v in range(3, 7))
        changed = (s & 7) == 7 and count < 3
        index, exponent = (count, 4-count) if changed else (None, 0)
        weight = exponentiate(plus(mono(), mono(0, 1, direction[index])), exponent) if changed else mono()
        need(convolve(old, weight) == new, 'independent terminal multiplier agreement')
        if count == 3:
            need(old == new == minus(mono(), mono(1, 0, lower[record][1])), 'unchanged full-complement slot')
        else:
            degree = 4-count
            need(old == mono(degree, 0, old[degree][0]) and old[degree][0] > 0, 'positive proper monomial slot')
        rows.append({'ideal': s, 'included_caps': count, 'factors': factors, 'baseline_potential': terms(old),
                     'multiplier': terms(weight), 'multiplier_index': index, 'multiplier_power': exponent,
                     'changed_potential': terms(new)})
        baseline_sum = plus(baseline_sum, old)
        changed_sum = plus(changed_sum, new)
    need(len(rows) == 18 and sum(len(row['factors']) for row in rows) == 110, 'upper 18-slot/110-factor coverage')
    return rows, baseline_sum, changed_sum


def theorem_route(held, direction, record):
    a, b, g = (held[(p, record)] for p in LEAVES)
    c, h, j = b[15], g[15], g[31]
    e_terms = [a[s]*g[s]**3/b[s]**3 for s in LEAF_IDEALS[C3]]
    k_terms = [a[s]**3*g[s]**6/b[s]**8 for s in LEAF_IDEALS[C3]]
    total, ksum = sum(e_terms, F(0))+3*h*h/c+3*j, sum(k_terms, F(0))
    p, v = k_terms[-1], h**3/c**2
    base = plus(mono(coefficient=F(4)), mono(1, 0, -4*total), mono(2, 0, 6*j), mono(3, 0, 4*v), mono(4, 0, ksum))
    raw = mono(coefficient=F(0))
    quotient = mono(coefficient=F(0))
    for rho_degree, coefficient, index, degree in ((4, p, 0, 4), (3, 4*v, 1, 3), (2, 6*j, 2, 2)):
        binomial = minus(exponentiate(plus(mono(), mono(0, 1, direction[index])), degree), mono())
        raw = plus(raw, convolve(mono(rho_degree, 0, coefficient), binomial))
        # Independent direct RI94 divided-binomial sum, without dividing raw.
        for k in range(1, degree+1):
            quotient = plus(quotient, mono(rho_degree-2, k-1, coefficient*comb(degree, k)*direction[index]**k))
    need(convolve(mono(2, 1), quotient) == raw, 'theorem raw/divided binomial identity')
    evidence = {'E': str(total), 'E_terms': [str(q) for q in e_terms], 'E_one_cap_total': str(3*h*h/c),
                'E_two_cap_total': str(3*j), 'K': str(ksum), 'K_terms': [str(q) for q in k_terms],
                'p': str(p), 'v': str(v), 'c': str(c), 'h': str(h), 'j': str(j),
                'U': terms(base), 'D': terms(raw), 'd': terms(quotient)}
    return total, cap(base, 4, 0), cap(raw, 4, 4), cap(quotient, 2, 3), evidence


def one_axis(coefficients, endpoint):
    degree = len(coefficients)-1
    return [sum((coefficients[k]*endpoint**k*F(comb(i, k), comb(degree, k)) for k in range(i+1)), F(0))
            for i in range(degree+1)]


def string_grid(grid):
    return [[str(q) for q in row] for row in grid]


def tensor_record(p, radius, degree):
    need(type(radius) is F and radius > 0 and type(degree) is int and degree in (2, 6), 'fixed tensor domain')
    cap(p, degree, 3)
    ordinary = [[p[a][b] for b in range(4)] for a in range(degree+1)]
    scaled = [[ordinary[a][b]*radius**a*E_CEILING**b for b in range(4)] for a in range(degree+1)]
    # Separable one-axis coordinate conversions, not the producer's double
    # binomial summation. First epsilon, then rho for each new column.
    epsilon_basis = [one_axis(row, E_CEILING) for row in ordinary]
    columns = [one_axis([epsilon_basis[a][j] for a in range(degree+1)], radius) for j in range(4)]
    beta = [[columns[j][i] for j in range(4)] for i in range(degree+1)]
    # Actually multiply Bernstein basis polynomials to reverse the transform.
    # x and y here are normalized formal coordinates, not actual scales.
    x, y = mono(1, 0), mono(0, 1)
    rebuilt = mono(coefficient=F(0))
    for i in range(degree+1):
        rho_basis = convolve(mono(i, 0, F(comb(degree, i))), exponentiate(minus(mono(), x), degree-i))
        for j in range(4):
            eps_basis = convolve(mono(0, j, F(comb(3, j))), exponentiate(minus(mono(), y), 3-j))
            rebuilt = plus(rebuilt, times_scalar(convolve(rho_basis, eps_basis), beta[i][j]))
    cap(rebuilt, degree, 3)
    back_scaled = [[rebuilt[a][b] for b in range(4)] for a in range(degree+1)]
    back_original = [[rebuilt[a][b]/(radius**a*E_CEILING**b) for b in range(4)] for a in range(degree+1)]
    need(back_scaled == scaled and back_original == ordinary, 'independent full tensor basis expansion and rescaling')
    edges = {
        'rho_zero': one_axis(ordinary[0], E_CEILING),
        'rho_upper': one_axis([sum((ordinary[a][b]*radius**a for a in range(degree+1)), F(0)) for b in range(4)], E_CEILING),
        'epsilon_zero': one_axis([ordinary[a][0] for a in range(degree+1)], radius),
        'epsilon_upper': one_axis([sum((ordinary[a][b]*E_CEILING**b for b in range(4)), F(0)) for a in range(degree+1)], radius),
    }
    need(edges['rho_zero'] == beta[0] and edges['rho_upper'] == beta[-1]
         and edges['epsilon_zero'] == [row[0] for row in beta]
         and edges['epsilon_upper'] == [row[-1] for row in beta], 'four independently evaluated edges')
    corner = value_at(p, radius, E_CEILING)
    need(corner == beta[-1][-1], 'included tensor corner')
    evidence = {'polynomial': terms(p), 'axis_order': ['rho', 'epsilon'], 'basis_degree': [degree, 3],
                'R': str(radius), 'E': '1/4', 'padded_power': string_grid(ordinary), 'scaled_power': string_grid(scaled),
                'bernstein': string_grid(beta), 'reverse_scaled_power': string_grid(back_scaled),
                'reverse_original_power': string_grid(back_original),
                'edges': {name: [str(q) for q in values] for name, values in edges.items()},
                'included_corner': str(corner), 'subdivision_used': False, 'adaptive_degree_elevation_used': False}
    return evidence, beta


def three_tensors(a, gs, radius):
    evidence, grids = {}, {}
    for name, p, degree in (('A', a, 2), ('G0', gs[0], 6), ('G1', gs[1], 6)):
        evidence[name], grids[name] = tensor_record(p, radius, degree)
    return evidence, grids


def signs_of(grids):
    tests, failed = {}, []
    for name in ('A', 'G0', 'G1'):
        beta = grids[name]
        tests[name] = {'all_nonnegative': all(q >= 0 for row in beta for q in row),
                       'strict_corner_required': name != 'A', 'included_corner': str(beta[-1][-1]),
                       'corner_condition': name == 'A' or beta[-1][-1] > 0}
        failed.extend({'polynomial': name, 'rho_index': i, 'epsilon_index': j, 'coefficient': str(q)}
                      for i, row in enumerate(beta) for j, q in enumerate(row) if q < 0)
    return {'sufficient_positive': all(item['all_nonnegative'] and item['corner_condition'] for item in tests.values()),
            'tests': tests, 'negative_coefficients': failed, 'negative_coefficients_do_not_assert_roots': True,
            'roots_examined': False}


def accepted_boundary(data, radius, grids):
    object_keys(data, RI91_FIELDS, 'RI91 complete outer schema')
    need(data['schema'] == 'ri91-relative-obstruction-v1' and data['checker_sha256'] == RI91_SOURCE
         and data['design_sha256'] == RI89_PROOF and type(data['design_bytes']) is int and data['design_bytes'] == 21769,
         'accepted RI91 provenance')
    identical(data['accepted_input'], ACCEPTED['ri88'], 'RI91 source-data identity')
    identical(data['selected_parent'], list(UPPER), 'RI91 fixed parent')
    need(type(data['records']) is list and len(data['records']) == 2
         and all(type(row) is dict and type(row['record']) is int for row in data['records'])
         and [row['record'] for row in data['records']] == [0, 1], 'RI91 two markings')
    need(data['scale_domain']['R'] == str(radius), 'same accepted outer radius')
    decision = data['decision']
    need(decision['disposition'] == 'certified-positive-obstruction' and decision['actual_global_scales_computed'] is False
         and decision['selector_acceptance_claimed'] is False, 'accepted RI91 conclusion scope')
    object_keys(decision['bernstein_evidence'], ('A', 'G0', 'G1'), 'RI91 coordinate labels')
    anchor = {}
    for name, degree in (('A', 2), ('G0', 6), ('G1', 6)):
        item = decision['bernstein_evidence'][name]
        need(type(item['rho_factor']) is int and item['rho_factor'] == 2 and type(item['basis_degree']) is int
             and item['basis_degree'] == degree and item['R'] == str(radius) and item['subdivision_used'] is False
             and item['adaptive_degree_elevation_used'] is False, 'RI91 fixed basis and factor')
        need(type(item['bernstein']) is list and len(item['bernstein']) == degree+1, 'seventeen boundary coordinates')
        beta = [fraction(q) for q in item['bernstein']]
        need(all(q > 0 for q in beta), 'strict accepted boundary anchor')
        last = [row[-1] for row in grids[name]]
        need(last == [4*q for q in beta], 'independently reconstructed factor-four boundary slice')
        anchor[name] = {'accepted': [str(q) for q in beta], 'new_last_column': [str(q) for q in last], 'factor': '4'}
    return {'entry_count': 17, 'strict_positive': True, 'epsilon': '1/4', 'identities': anchor,
            'saved_native_U_D_C_used': False, 'independent_derivation_claimed': False}


def synthetic_records():
    """Rebuild twelve synthetic identities, not producer mutation executions."""
    zero, one, x, y = mono(coefficient=F(0)), mono(), mono(1, 0), mono(0, 1, F(4))
    mixed = plus(exponentiate(minus(y, mono(coefficient=F(1, 2))), 2), mono(coefficient=F(1, 16)))
    interior = exponentiate(minus(times_scalar(y, F(2)), one), 2)
    cases = (
        ('positive', one, zero, True), ('negative-generic-orientation', times_scalar(one, F(-1)), zero, False),
        ('weak-A-zero', zero, times_scalar(one, F(-1)), True), ('blind', zero, zero, False),
        ('included-binding-s-endpoint', one, mono(coefficient=F(8)), False),
        ('conservative-both-endpoints', one, mono(coefficient=F(6)), False),
        ('positive-mixed-amplitude-basis', mixed, zero, False), ('endpoint-positive-interior-zero', interior, zero, False),
    )
    out = {}
    for name, a, c, positive in cases:
        u = [one, mono(coefficient=F(3))]
        d = [times_scalar(minus(a, c), F(1, 2)), times_scalar(minus(times_scalar(a, F(3)), c), F(1, 2))]
        need(minus(d[1], d[0]) == a and minus(convolve(d[1], u[0]), convolve(d[0], u[1])) == c, 'synthetic reduction')
        gs = [minus(times_scalar(convolve(plus(one, q), a), F(2)), c) for q in u]
        tensors, grids = three_tensors(a, gs, F(1))
        summary = signs_of(grids)
        need(summary['sufficient_positive'] is positive, 'fixed synthetic sign case: '+name)
        out[name] = {'kind': 'algebra-only-d-and-U', 'R': '1', 'E': '1/4', 'U': [terms(q) for q in u],
                     'd': [terms(q) for q in d], 'A': terms(a), 'C': terms(c), 'G': [terms(q) for q in gs],
                     'tensor_evidence': tensors, 'sign_summary': summary, 'expected_positive': positive,
                     'binding_s_upper_bound': '1/8', 'native_model_claimed': False}
        if name == 'negative-generic-orientation':
            _, reverse = three_tensors(times_scalar(a, F(-1)), [times_scalar(q, F(-1)) for q in gs], F(1))
            need(signs_of(reverse)['sufficient_positive'], 'generic reversed orientation only')
            out[name]['generic_reverse_orientation_passes'] = True
        if name == 'included-binding-s-endpoint':
            need(value_at(a, F(1), E_CEILING)-F(1, 8)*value_at(c, F(1), E_CEILING) == 0, 'included binding endpoint')
    need(value_at(interior, F(1), F(1, 8)) == 0 and value_at(interior, F(1), E_CEILING) == 1, 'synthetic interior zero')
    need(out['positive-mixed-amplitude-basis']['tensor_evidence']['A']['bernstein'][0]
         == ['5/16', '-1/48', '-1/48', '5/16'], 'mixed positive fixture coordinates')
    u = [one, plus(one, mono(4, 0))]
    d = convolve(mono(2, 0), exponentiate(y, 3))
    a, c = zero, minus(convolve(d, u[0]), convolve(d, u[1]))
    gs = [minus(times_scalar(convolve(plus(one, q), a), F(2)), c) for q in u]
    need(gs[0] == gs[1] == convolve(mono(6, 0), exponentiate(y, 3)), 'corner-only response')
    tensors, grids = three_tensors(a, gs, F(1))
    summary = signs_of(grids)
    need(summary['sufficient_positive'], 'excluded axes may vanish')
    for name in ('G0', 'G1'):
        need(all(q == F(int(i == 6 and j == 3)) for i, row in enumerate(grids[name]) for j, q in enumerate(row)), 'only strict corner coefficient')
    out['strict-corner-only-support'] = {'kind': 'algebra-only-d-and-U', 'R': '1', 'E': '1/4', 'U': [terms(q) for q in u],
                                        'd': [terms(d), terms(d)], 'A': terms(a), 'C': terms(c), 'G': [terms(q) for q in gs],
                                        'tensor_evidence': tensors, 'sign_summary': summary, 'expected_positive': True,
                                        'excluded_axes_may_vanish': True, 'native_model_claimed': False}
    for name, edge in (('included-rho-edge-zero', minus(one, x)), ('included-epsilon-edge-zero', minus(one, y))):
        tensors, grids = three_tensors(one, [edge, edge], F(1))
        summary = signs_of(grids)
        need(not summary['sufficient_positive'] and not summary['negative_coefficients'], 'included edge requires strictness')
        out[name] = {'kind': 'polynomial-only-edge', 'R': '1', 'E': '1/4', 'tensor_evidence': tensors,
                     'sign_summary': summary, 'expected_positive': False, 'native_model_claimed': False}
    unequal = plus(mono(2, 1), mono(1, 3, F(2)))
    evidence, _ = tensor_record(unequal, F(1), 2)
    need(evidence['scaled_power'][2][1] == '1/4' and evidence['scaled_power'][1][3] == '1/32', 'unequal axis scaling')
    out['unequal-axis-scaling'] = {'kind': 'polynomial-only-scaling', 'R': '1', 'E': '1/4', 'polynomial': terms(unequal),
                                  'tensor_evidence': evidence, 'native_model_claimed': False}
    need(tuple(out) == FIXTURES and len(out) == 12, 'complete ordered synthetic fixtures')
    need(len(DECLARED_CONTROLS) == len(set(DECLARED_CONTROLS)) == 134, 'complete declared control metadata')
    return {'intended_reason_refusals': list(DECLARED_CONTROLS), 'synthetic_algebra_fixtures': out,
            'fixed_fixture_names': list(FIXTURES), 'synthetic_fixtures_are_native_models': False, 'extra_native_inputs_used': False}


def reconstruct(ri88, ri91):
    held, direction, inputs = accepted_seed(ri88)
    lower = {record: lower_route(held, record) for record in (0, 1)}
    records, totals, us, ds, quotients = [], [], [], [], []
    for record in (0, 1):
        budget()
        slots, old, new = upper_route(held, direction, record, lower)
        delta = minus(new, old)
        q = prescribed_quotient(delta, 2)
        total, base_closed, raw_closed, q_closed, closed = theorem_route(held, direction, record)
        need(total == lower[record][1] and old == base_closed and delta == raw_closed and q == q_closed,
             'both independently derived deletion and theorem routes agree')
        totals.append(total); us.append(old); ds.append(delta); quotients.append(q)
        records.append({'record': record, 'lower_symbolic_slots': lower[record][2], 'top_proper_slots': slots,
                        'closed_form': closed, 'generic_U': terms(old), 'generic_V': terms(new),
                        'generic_D': terms(delta), 'divided_d': terms(q)})
    radius = F(1, 2)/(1+max(totals))
    margins = [1-radius*q for q in totals]
    need(radius > 0 and all(q > F(1, 2) for q in margins), 'symbolic positive full margins on outer domain')
    a_raw = minus(ds[1], ds[0])
    c_raw = minus(convolve(ds[1], us[0]), convolve(ds[0], us[1]))
    via_v = minus(convolve(plus(us[1], ds[1]), us[0]), convolve(plus(us[0], ds[0]), us[1]))
    need(via_v == c_raw, 'full complement cross-product via V and D')
    a, c = prescribed_quotient(a_raw, 2), prescribed_quotient(c_raw, 6)
    need(a == minus(quotients[1], quotients[0])
         and c == minus(convolve(quotients[1], us[0]), convolve(quotients[0], us[1])), 'divided cross-product independent form')
    raw_gs = [minus(times_scalar(convolve(plus(mono(), u), a_raw), F(2)), c_raw) for u in us]
    gs = [prescribed_quotient(p, 6) for p in raw_gs]
    endpoints = []
    for i, u in enumerate(us):
        denominator = times_scalar(plus(mono(), u), F(2))
        numerator = minus(convolve(denominator, a), c)
        raw_numerator = minus(convolve(denominator, a_raw), c_raw)
        need(numerator == gs[i] and raw_numerator == raw_gs[i] == convolve(mono(2, 1), gs[i]), 'both full-complement endpoint forms')
        endpoints.append({'index': i, 'denominator': terms(denominator), 'divided_numerator': terms(numerator),
                          'raw_numerator': terms(raw_numerator), 'divided_residual': terms(minus(numerator, gs[i])),
                          'raw_residual': terms(minus(raw_numerator, convolve(mono(2, 1), gs[i]))),
                          'reciprocal_defines_b_i': True, 'denominator_positive_by_domain_proof': True, 'numerical_s_selected': False})
    evidence, grids = three_tensors(a, gs, radius)
    anchor = accepted_boundary(ri91, radius, grids)
    summary = signs_of(grids)
    if summary['sufficient_positive']:
        disposition = 'certified-positive-amplitude-obstruction'
    else:
        need(bool(summary['negative_coefficients']), 'anchored unresolved outcome needs a negative tensor coordinate')
        disposition = 'unresolved-fixed-bivariate-bernstein'
    decision = {'disposition': disposition, 'sign_summary': summary, 'endpoint_regression': anchor,
                'negative_or_blind_native_branch': False, 'root_diagnostic_performed': False,
                'actual_global_scales_computed': False, 'selector_acceptance_claimed': False,
                'pair_obstruction_only': True, 'test_is_sufficient_not_necessary': True}
    fixed = {name: quotient_record(p, degree) for name, p, degree in
             (('D0', ds[0], 2), ('D1', ds[1], 2), ('A', a_raw, 2), ('C', c_raw, 6), ('G0', raw_gs[0], 6), ('G1', raw_gs[1], 6))}
    witness = {
        'schema': 'ri95-relative-amplitude-certificate-v1', 'design_sha256': SOURCES['proof']['sha256'],
        'design_bytes': SOURCES['proof']['bytes'], 'accepted_inputs': ACCEPTED, 'inputs': inputs,
        'selected_parent': list(UPPER), 'records': records,
        'scale_domain': {'R': str(radius), 'amplitude_ceiling': '1/4', 'selected_E': [str(q) for q in totals],
                         'symbolic_lower_full_margins_at_R': [str(q) for q in margins], 'rho_interval': '0<rho<=R',
                         'epsilon_interval': '0<epsilon<=1/4', 's_interval': '0<s<=min_i 1/[2(1+Ui(rho))]',
                         'actual_scales_selected': False, 'modified_full_positivity_not_claimed': True},
        'cross_multiplication': {'fixed_raw_divisor': {'rho_power': 2, 'epsilon_power': 1},
                                 'A_raw': terms(a_raw), 'C_raw': terms(c_raw), 'C_raw_via_V': terms(via_v),
                                 'G_raw': [terms(q) for q in raw_gs], 'A': terms(a), 'C': terms(c), 'G': [terms(q) for q in gs],
                                 'F_divided_by_s_power': [terms(a), terms(times_scalar(c, F(-1)))]},
        'full_complement_s_endpoints': endpoints, 'fixed_division_evidence': fixed, 'tensor_evidence': evidence,
        'decision': decision,
        'coverage': {'held_rows': 6, 'held_probability_slots': 32, 'H_values_in_arithmetic': 3,
                     'full_support_provenance_classes': 11, 'record_assignments': 2, 'lower_symbolic_slots': 20,
                     'lower_held_factors': 80, 'top_proper_slots': 36, 'top_deletion_factors': 220,
                     'tensor_degrees': [[2, 3], [6, 3], [6, 3]], 'tensor_entries': 68, 'regression_entries': 17,
                     'included_full_probability_rows': 0},
        'limitations': {'numeric_q6_q7_or_global_M_computed': False, 'helper_prefix_replayed': False,
                        'no_other_records_parents_or_adaptive_search': True, 'no_root_or_negative_native_search': True,
                        'regression_replay_is_not_independent_derivation': True, 'programme_or_gravity_completion_claimed': False},
        'checker_sha256': SOURCES['checker']['sha256'], 'refusal_controls': synthetic_records(),
    }
    object_keys(witness, RESULT_FIELDS, 'reconstructed seventeen-field witness')
    need(len(witness) == 17, 'seventeen sections')
    return witness


def descriptor_shape(descriptor, own_identity):
    object_keys(descriptor, ('schema', 'phase', 'files', 'accepted_sources', 'audit_source', 'custody_dependencies'), 'audit descriptor')
    need(descriptor['schema'] == 'ri95-independent-audit-input-v1'
         and descriptor['phase'] == 'fixed_saved_certificate_audit', 'fixed consumer mode')
    identical(descriptor['accepted_sources'], SOURCES, 'reviewed source premises')
    identical(descriptor['audit_source'], own_identity, 'consumer byte identity')
    check_pin(descriptor['audit_source'])
    object_keys(descriptor['files'], ('ri88', 'ri91', 'candidate'), 'exact three scientific bodies')
    paths = []
    for role in ('ri88', 'ri91', 'candidate'):
        entry = descriptor['files'][role]
        object_keys(entry, ('path', 'bytes', 'sha256'), 'scientific file '+role)
        pin = {k: entry[k] for k in ('bytes', 'sha256')}
        check_pin(pin)
        if role in ACCEPTED:
            identical(pin, ACCEPTED[role], 'accepted input identity '+role)
        need(type(entry['path']) is str and Path(entry['path']).is_absolute(), 'literal scientific path')
        paths.append(entry['path'])
    need(len(set(paths)) == 3, 'distinct scientific paths')
    custody = descriptor['custody_dependencies']
    need(type(custody) is list and len(custody) == len(CUSTODY_ROLES), 'complete concrete custody dependency list')
    for role, entry in zip(CUSTODY_ROLES, custody):
        object_keys(entry, ('role', 'path', 'bytes', 'sha256'), 'custody file')
        need(entry['role'] == role, 'literal custody role ordering')
        check_pin({k: entry[k] for k in ('bytes', 'sha256')})
        need(type(entry['path']) is str and Path(entry['path']).is_absolute(), 'absolute custody path')
        paths.append(entry['path'])
    need(len(paths) == len(set(paths)), 'distinct scientific and custody paths')
    witness_pin = {k: custody[0][k] for k in ('bytes', 'sha256')}
    identical(witness_pin, {k: descriptor['files']['candidate'][k] for k in ('bytes', 'sha256')}, 'candidate exactly pinned to genuine witness stdout')


def execute_audit():
    need(len(sys.argv) == 4, 'usage: audit_saved_certificate.py DESCRIPTOR BYTES SHA256')
    need(sys.argv[2].isascii() and sys.argv[2].isdigit() and str(int(sys.argv[2])) == sys.argv[2], 'canonical descriptor byte size')
    source = Path(__file__).resolve()
    own_body = source.read_bytes()
    own_identity = byte_identity(own_body)
    descriptor_entry = {'path': sys.argv[1], 'bytes': int(sys.argv[2]), 'sha256': sys.argv[3]}
    descriptor_raw, descriptor_stat = read_fixed(descriptor_entry)
    descriptor = json_body(descriptor_raw)
    descriptor_shape(descriptor, own_identity)
    entries = [(role, descriptor['files'][role]) for role in ('ri88', 'ri91', 'candidate')]
    entries += [(entry['role'], {k: entry[k] for k in ('path', 'bytes', 'sha256')}) for entry in descriptor['custody_dependencies']]
    # Authenticate all scientific/custody bytes before parsing any scientific
    # body. Custody semantics and actual root authorization remain external;
    # pinning their files is not a self-issued acceptance decision.
    snapshots = {role: read_fixed(entry) for role, entry in entries}
    need(snapshots['candidate'][0] == snapshots['producer_witness_stdout'][0], 'candidate is not unchanged witness stdout')
    held = json_body(snapshots['ri88'][0])
    regression = json_body(snapshots['ri91'][0])
    saved = json_body(snapshots['candidate'][0])
    object_keys(saved, RESULT_FIELDS, 'candidate complete top-level fields')
    expected = reconstruct(held, regression)
    identical(saved, expected)
    reconstructed = canonical_bytes(expected)
    need(reconstructed == snapshots['candidate'][0], 'entire canonical candidate bytes with exact newline')
    for role, entry in entries:
        body, signature = read_fixed(entry)
        need((body, signature) == snapshots[role], 'input/custody changed across audit: '+role)
    descriptor_after = read_fixed(descriptor_entry)
    need(descriptor_after == (descriptor_raw, descriptor_stat), 'descriptor changed across reconstruction')
    need(source.read_bytes() == own_body, 'consumer source changed during audit')
    budget()
    report = {
        'schema': 'ri95-independent-complete-certificate-audit-v1', 'status': 'all_saved_fields_independently_match',
        'audit_source_identity': own_identity, 'descriptor_identity': byte_identity(descriptor_raw),
        'accepted_sources': SOURCES,
        'scientific_inputs': {role: byte_identity(snapshots[role][0]) for role in ('ri88', 'ri91', 'candidate')},
        'custody_dependencies_pinned_not_self_adjudicated': [dict(role=role, **byte_identity(snapshots[role][0])) for role in CUSTODY_ROLES],
        'reconstructed_certificate_identity': byte_identity(reconstructed),
        'complete_top_level_sections': {key: byte_identity(canonical_bytes(value)) for key, value in expected.items()},
        'coverage': expected['coverage'], 'scale_domain': expected['scale_domain'],
        'cross_multiplication': expected['cross_multiplication'], 'full_complement_s_endpoints': expected['full_complement_s_endpoints'],
        'fixed_division_evidence': expected['fixed_division_evidence'], 'decision': expected['decision'],
        'independent_synthetic_reconstruction': expected['refusal_controls']['synthetic_algebra_fixtures'],
        'declared_producer_controls': {'ordered_names': list(DECLARED_CONTROLS), 'count': 134,
                                       'producer_controls_executed_by_this_consumer': False,
                                       'genuine_control_execution_is_separately_accepted_producer_custody_premise': True},
        'independence': [
            'No producer, prefix, inherited checker, optimizer, supervisor or helper is imported.',
            'Fixed-parent downsets and combinations of omitted maxima reconstruct every labeled source/order/record/precursor factor.',
            'Dense 9-by-5 coefficient rectangles replace producer sparse algebra; negative factors are independently proved held constants and accumulated in a separate denominator.',
            'RI94 closed binomial formulas and independent deletion products agree before classification.',
            'Separable one-axis Bernstein conversion is reversed by actual dense multiplication of Bernstein basis factors, with both rescalings and four edge evaluations.',
            'Only seventeen RI91 coordinates and authenticated scope metadata are read for regression; native RI91 polynomial coefficients are not used.',
            'All seventeen sections, exact types, array positions and canonical bytes are independently rebuilt; saved sign flags are never premises.',
        ],
        'premises_and_limits': [
            'Accepted RI88 probabilities, strict-prefix semantics, RI79/89 continuation constraints and RI94 theorem remain inherited premises.',
            'Only six held rows, thirty-two probabilities, three H values, two markings and the frozen symbolic parents enter native reconstruction.',
            'The fixed degree-(2,3)/(6,3) sufficient tensor test may be unresolved; no root, other amplitude/record/parent, new table or adaptive search is performed.',
            'The 134 producer refusals are reconciled as declarations, not reexecuted controls; the twelve synthetic algebra fixtures are independently reconstructed.',
            'Concrete source/caller/freeze/authorization and actual supervision acceptance are external root-owned prerequisites; descriptor pins do not authorize this program.',
            'No actual a6/a7/M6/M7, full future growth law, quantum derivation, physical geometry/gravity result, RET change or programme completion is claimed.',
        ],
    }
    body = (json.dumps(report, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False)+'\n').encode('ascii')
    sys.stdout.buffer.write(body)
    sys.stdout.buffer.flush()
    budget()


def main():
    global START
    START = time.monotonic()
    def expired(_number, _frame):
        raise AuditError('120-second internal envelope')
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(120)
    try:
        execute_audit()
    finally:
        signal.alarm(0)


if __name__ == '__main__':
    main()
