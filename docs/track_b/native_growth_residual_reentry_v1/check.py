#!/usr/bin/env python3
"""RI-65: one exact noncritical-rectangle re-entry witness.

Standard library only; no solver, downloads, subprocesses or writes. This
explicitly reuses SHA-pinned RI-63 helper code and its accepted certificate;
it does not independently reimplement the accepted first-layer matrix.
The whole accepted reconstruction and canonical proof are rechecked. New
work covers only the (3,2) parent class, its records and naturally labeled
histories, its full (3,3) rectangle child and that child's ten ideal births.
Seven-point children are compared only with the two diagrams permitted by
the accepted RI-54 intrinsic corner lemma. There is no size-seven catalogue,
new parent-six law, q6 lookup, layer-six optimization or asymptotic test.

--witness prints the exact proposed new certificate to stdout. Otherwise the
local certificate is checked. Runs have a 900-second alarm and checkpointed
two-GiB peak-RSS envelope; accepted helpers retain their own budget checks.
"""

from fractions import Fraction as F
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
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
B = (0, 1, 3, 1, 11)
R = B + (31,)
AXES = (7, 9)
MAX_SECONDS = 900
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    if START_TIME is not None:
        require(time.monotonic()-START_TIME <= MAX_SECONDS, '900-second time envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == 'darwin' else peak * 1024
    require(peak_bytes <= MAX_RESIDENT_BYTES, 'two-GiB resident-memory envelope exceeded')
    if stage:
        print('RI65: ' + stage, file=sys.stderr, flush=True)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical_json(value).encode()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def load_json(text):
    def bad_constant(value):
        raise RuntimeError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=bad_constant)


def check_pin(raw, expected):
    require(sha256(raw).hexdigest() == expected, 'accepted dependency byte pin mismatch')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask -= bit


def validate_order(order):
    require(len(order) <= 7 and all(type(past) is int and 0 <= past < (1 << v)
            and all(order[u] & past == order[u] for u in bits(past))
            for v, past in enumerate(order)), 'invalid targeted naturally labeled order')


def relabel_order(order, permutation):
    require(tuple(sorted(permutation)) == tuple(range(len(order))), 'invalid vertex permutation')
    result = [0]*len(order)
    for v, past in enumerate(order):
        result[permutation[v]] = sum(1 << permutation[u] for u in bits(past))
    return tuple(result)


def relabel_mask(mask, permutation):
    return sum(1 << permutation[v] for v in bits(mask))


def isomorphism(order, target):
    require(len(order) == len(target) <= 7, 'targeted isomorphism domain mismatch')
    def profile(p):
        return sorted((p[v].bit_count(), sum(bool(past & (1 << v)) for past in p))
                      for v in range(len(p)))
    if profile(order) != profile(target):
        return None
    return next((perm for perm in permutations(range(len(order)))
                 if relabel_order(order, perm) == target), None)


def diagram(partition):
    require(partition in ((3, 2), (3, 3), (4, 3), (3, 3, 1)),
            'undeclared diagram outside targeted rectangle/corner witness')
    cells = tuple((i, j) for i, count in enumerate(partition) for j in range(count))
    order = tuple(sum(1 << u for u, (a, b) in enumerate(cells)
                      if a <= i and b <= j and (a, b) != (i, j))
                  for i, j in cells)
    validate_order(order)
    return order


def verify_mixture(actual, alpha, eta, interior):
    require(eta == F(1, 36) and all(x == (1-eta)*a + eta*interior
                                  for x, a in zip(actual, alpha))
            and len(actual) == len(alpha), 'accepted strict mixture formula mismatch')


def verify_affine_residual(f, a0, a1, gap, formal_mu):
    require(f > 0 and a0 > 0 and a1 > 0 and gap == f-a0-a1 and gap > 0,
            'formal rectangle identity has invalid known factors')
    left = {name: f*value for name, value in formal_mu.items()}
    left['1'] -= gap
    right = {'1': a0+a1, 'z0': -a0, 'z1': -a1}
    require(left == right, 'formal affine residual identity failed')
    # z0,z1 are unknown companion probabilities, NOT generated q6 values.
    # Under their assumed normalization bounds 0<=z_i<=1, the affine residual
    # has box minimum zero. Positive a_i and strict z_i<1 make it positive.
    box_minimum = right['1'] + min(F(0), right['z0']) + min(F(0), right['z1'])
    require(box_minimum == 0, 'formal companion probability box bound failed')
    return {name: str(value) for name, value in right.items()}


def verify_newborn_transport(left, right, permutation, left_record, right_record):
    require(relabel_order(left, permutation) == right
            and relabel_mask(left_record, permutation) == right_record,
            'common terminal newborn transport failed')


def reconstruct_accepted():
    directory = Path(__file__).resolve().parent.parent
    paths = {
        'ri63_checker': directory/'native_growth_expected_defect_completion_v1'/'check.py',
        'ri63_certificate': directory/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
        'ri41_certificate': directory/'native_growth_height_normalization_v1'/'CERTIFICATE.json',
    }
    raw = {name: path.read_bytes() for name, path in paths.items()}
    for name in paths:
        check_pin(raw[name], PINS[name])
    budget('all accepted dependencies byte-pinned before helper loading')
    helper = runpy.run_path(str(paths['ri63_checker']))
    problem = helper['build_problem']()
    certificate = helper['load_json'](raw['ri63_certificate'])
    proof = helper['check_certificate_core'](certificate, problem)
    report = helper['certificate_reports'](certificate, problem, proof)
    accepted_controls = helper['certificate_controls'](certificate, problem)
    require(report['m5'] == '6650803/108900000'
            and report['certified_positive_lex_stages'] == 69,
            'accepted canonical first-layer result changed')
    eta, interior = F(problem['eta5']), F(problem['c5'])
    actual = [(1-eta)*a + eta*interior for a in proof['alpha']]
    verify_mixture(actual, proof['alpha'], eta, interior)
    return helper, problem, proof, report, accepted_controls, actual, raw


def targeted_geometry(helper):
    require(B == diagram((3, 2)) and R == diagram((3, 3)), 'declared Ferrers representatives changed')
    require(helper['defect'](R) == 0 and not helper['critical'](R)
            and helper['maximal_mask'](R) == 32, 'rectangle is not noncritical with one maximum')
    candidates = helper['ideals'](R)
    require(len(candidates) == 10, 'targeted rectangle ideal count changed')
    corner_orders = {7: diagram((4, 3)), 9: diagram((3, 3, 1))}
    children = []
    for part in candidates:
        child = R+(part,)
        validate_order(child)
        matches = [(axis, isomorphism(child, target)) for axis, target in corner_orders.items()]
        matching = [(axis, perm) for axis, perm in matches if perm is not None]
        require(bool(matching) == (part in AXES), 'targeted child disagrees with intrinsic corner lemma')
        if part in AXES:
            require(len(matching) == 1 and matching[0][0] == part,
                    'declared labeled axis has the wrong corner diagram')
        # RI-54 proves that any Ferrers child of this rectangle is one of these
        # two corners. For a noncorner, retaining old R gives defect <=1 and
        # the lemma gives defect !=0; no general seven-point recognizer is used.
        require(child[:6] == R, 'targeted birth changed its retained rectangle ideal')
        children.append(dict(past_mask=part, child=child, defect=0 if matching else 1,
                             neutral=bool(matching), corner_partition=
                             ((4, 3) if part == 7 else (3, 3, 1)) if matching else None,
                             explicit_isomorphism=matching[0][1] if matching else None))
    return dict(parent=B, rectangle=R, rectangle_defect=0, rectangle_critical=False,
                rectangle_maximal_mask=32, axes=AXES, children=children,
                seven_point_scope='only ten specified rectangle births; RI-54 intrinsic corner lemma',
                seven_point_ferrers_catalogue=False)


def reconstruct_witness():
    global START_TIME
    START_TIME = time.monotonic()
    helper, problem, proof, accepted_report, accepted_controls, actual, raw = reconstruct_accepted()
    budget('accepted canonical law rechecked; restricting new work to the B class')
    geometry = targeted_geometry(helper)
    local_nodes = {tuple(item['key']): item for item in problem['nodes']}
    canonical_rows = {tuple(item['key']): item for item in problem['rows']}

    def q5(order, record, coefficients=actual):
        require(len(order) == 5 and 0 <= record < 32, 'new witness q lookup is not parent five')
        result = {}
        for part in helper['ideals'](order):
            if part != 31:
                item = local_nodes[helper['node'](order, part, record)]
                result[part] = F(item['u'])*coefficients[item['component']]
        result[31] = 1-sum(result.values(), F(0))
        require(sum(result.values(), F(0)) == 1 and all(value >= 0 for value in result.values()),
                'targeted parent-five row is not normalized nonnegative')
        if coefficients is actual:
            require(all(value > 0 for value in result.values()), 'actual targeted row is not strict')
        return result

    fixed_rows = {}
    formal_residuals = []
    interior_coefficients = [F(problem['c5'])]*len(actual)
    for record in range(32):
        q, boundary = q5(B, record), q5(B, record, proof['alpha'])
        interior_row = q5(B, record, interior_coefficients)
        f, a0, a1 = q[31], q[7], q[9]
        gap = f-a0-a1
        require(gap > 0, 'actual full-rectangle probability does not exceed both axis probabilities')
        nu = helper['history_probability'](B, record)
        require(nu > 0, 'declared marked B history is not reached with positive probability')
        cap = F(1325, 8869) if record & 1 else F(7000, 18447)
        require(boundary[7]+boundary[9] == cap and boundary[31] == 1-cap,
                'canonical boundary does not attain the declared root-bit capacity')
        require(interior_row[31] > F(1, 2)
                and sum((v for s, v in interior_row.items() if s != 31), F(0)) < F(1, 2),
                'accepted interior is not full-dominant')
        eta = F(problem['eta5'])
        floor = (1-eta)*(1-2*cap)
        require(gap == floor+eta*(interior_row[31]-interior_row[7]-interior_row[9])
                and gap > floor > 0, 'analytic boundary/interior gap identity failed')
        formal_mu = {'1': F(1), 'z0': -a0/f, 'z1': -a1/f}
        residual = verify_affine_residual(f, a0, a1, gap, formal_mu)
        formal_residuals.append(dict(record=record, residual=residual,
                                     formal_mu={k: str(v) for k, v in formal_mu.items()}))
        fixed_rows[record] = dict(record=record, key=helper['row_key'](B, record),
                                  f=str(f), a7=str(a0), a9=str(a1), b=str(a0+a1), gap=str(gap),
                                  boundary_f=str(boundary[31]),
                                  boundary_b=str(boundary[7]+boundary[9]),
                                  interior_f=str(interior_row[31]),
                                  interior_b=str(interior_row[7]+interior_row[9]),
                                  analytic_gap_floor=str(floor),
                                  conditional_rectangle_drift_floor=str(gap/f),
                                  fixed_fullbirth_probability_per_newborn=str(nu*f/2),
                                  fixed_natural_history_probability=str(nu))
    shape_key = helper['node'](B, 0, 0)[0]
    natural_parents = [p for p in helper['parents'](5) if helper['node'](p, 0, 0)[0] == shape_key]
    raw_histories, transport_manifest, diamond_manifest = [], [], []
    class_weights, class_counts = {}, {}
    single_lower = all_lower = F(0)
    swap_newborns = (0, 1, 2, 3, 4, 6, 5)
    fixed_diamonds = 0
    for parent in natural_parents:
        budget()
        transports = [perm for perm in permutations(range(5)) if relabel_order(parent, perm) == B]
        require(len(transports) == 1, 'canonical B type does not have a unique explicit isomorphism')
        to_fixed = transports[0]
        inverse = tuple(to_fixed.index(v) for v in range(5))
        local_axes = tuple(relabel_mask(axis, inverse) for axis in AXES)
        require(all(part in helper['ideals'](parent) for part in local_axes),
                'transported B axis is not an ideal')
        transport_manifest.append(dict(parent=parent, to_fixed_B=to_fixed, local_axes=local_axes))
        for record in range(32):
            fixed_record = relabel_mask(record, to_fixed)
            q = q5(parent, record)
            expected = fixed_rows[fixed_record]
            require((q[31], q[local_axes[0]], q[local_axes[1]])
                    == tuple(F(expected[field]) for field in ('f', 'a7', 'a9')),
                    'actual row probabilities are not label-covariant')
            key = helper['row_key'](parent, record)
            require(key == tuple(expected['key']), 'marked-row transport changed the canonical class')
            weight = helper['history_probability'](parent, record)
            require(weight > 0, 'raw B marked-history weight is not positive')
            require(weight == F(expected['fixed_natural_history_probability']),
                    'transported naturally labeled history has a different path weight')
            class_weights[key] = class_weights.get(key, F(0))+weight
            class_counts[key] = class_counts.get(key, 0)+1
            gap = F(expected['gap'])
            contribution = sum(((weight*q[31]/2)*(gap/q[31]) for newborn in (0, 1)), F(0))
            require(contribution == weight*gap, 'fair newborn aggregation has an extra factor of two')
            all_lower += contribution
            if parent == B:
                single_lower += contribution
            raw_histories.append(dict(parent=parent, record=record, fixed_record=fixed_record,
                                      key=key, probability=str(weight), gap=str(gap)))
            for axis in local_axes:
                rectangle, companion = parent+(31,), parent+(axis,)
                require(axis in helper['ideals'](rectangle)
                        and 31 in helper['ideals'](companion) and axis != 63 and 31 != 63,
                        'second diamond precursor is not a proper ideal')
                left, right = rectangle+(axis,), companion+(31,)
                validate_order(left)
                validate_order(right)
                require(relabel_order(left, swap_newborns) == right,
                        'newborn label swap does not identify the common terminal order')
                for u in (0, 1):
                    for v in (0, 1):
                        left_record = record | (u << 5) | (v << 6)
                        right_record = record | (v << 5) | (u << 6)
                        verify_newborn_transport(left, right, swap_newborns, left_record, right_record)
                        require((record | (u << 5)) & axis == record & axis
                                and (record | (v << 5)) & 31 == record,
                                'unknown second probability reads the wrong newborn record')
                        diamond_manifest.append(dict(parent=parent, record=record, axis=axis,
                            first_newborn=u, companion_newborn=v, left_terminal=left,
                            right_terminal=right, left_full_record=left_record,
                            right_full_record=right_record,
                            left_known_map_factor=str(q[31]/4),
                            right_known_map_factor=str(q[axis]/4)))
                        fixed_diamonds += int(parent == B)
    require(len(natural_parents) == 5 and len(raw_histories) == 160 and len(class_weights) == 32,
            'complete B-class history coverage changed')
    all_B_keys = {tuple(item['key']) for item in problem['rows']
                  if helper['node'](tuple(item['past_masks']), 0, 0)[0] == shape_key}
    require(set(class_weights) == all_B_keys, 'raw B histories omit a canonical marked B row')
    canonical_lower = F(0)
    record_rows = []
    for record, item in sorted(fixed_rows.items()):
        key = tuple(item['key'])
        pi = F(canonical_rows[key]['pi'])
        require(class_weights[key] == pi, 'direct raw-history sum differs from accepted canonical pi')
        item['canonical_history_probability'] = str(pi)
        item['natural_history_count'] = class_counts[key]
        item['canonical_fullbirth_probability_per_newborn'] = str(pi*F(item['f'])/2)
        item['weighted_lower_bound'] = str(pi*F(item['gap']))
        canonical_lower += pi*F(item['gap'])
        record_rows.append(item)
    require(canonical_lower == all_lower and all_lower > 0 and single_lower > 0,
            'positive all-class re-entry lower bound failed')
    groups = {}
    for item in record_rows:
        signature = tuple(item[field] for field in ('f', 'a7', 'a9', 'gap',
                                                   'boundary_f', 'boundary_b',
                                                   'fixed_natural_history_probability'))
        if signature not in groups:
            groups[signature] = dict(records=[], signature=dict(zip(
                ('f', 'a7', 'a9', 'gap', 'boundary_f', 'boundary_b',
                 'fixed_natural_history_probability'), signature)),
                history_mass=F(0), lower_bound=F(0))
        groups[signature]['records'].append(item['record'])
        groups[signature]['history_mass'] += F(item['canonical_history_probability'])
        groups[signature]['lower_bound'] += F(item['weighted_lower_bound'])
    grouped = [dict(records=value['records'], **value['signature'],
                    canonical_history_mass=str(value['history_mass']),
                    weighted_lower_bound=str(value['lower_bound'])) for value in groups.values()]
    grouped.sort(key=lambda item: item['records'])
    coverage = dict(natural_B_parents=len(natural_parents), raw_marked_B_histories=len(raw_histories),
                    canonical_marked_B_rows=len(record_rows), fixed_natural_B_records=32,
                    grouped_equal_record_tuples=len(grouped), symbolic_marked_diamonds=len(diamond_manifest),
                    fixed_B_symbolic_diamonds=fixed_diamonds, targeted_rectangle_ideal_children=10,
                    formal_affine_residual_identities=len(formal_residuals),
                    numerically_evaluated_q6=0, optimized_parent_six_rows=0)
    require(len(diamond_manifest) == 1280 and fixed_diamonds == 256,
            'symbolic complete-record diamond coverage changed')
    totals = dict(all_B_history_probability=str(sum(class_weights.values(), F(0))),
                  fixed_natural_B_history_probability=str(sum(
                      (F(item['fixed_natural_history_probability']) for item in record_rows), F(0))),
                  all_B_lower_bound=str(all_lower), fixed_natural_B_lower_bound=str(single_lower),
                  minimum_gap=str(min(F(item['gap']) for item in record_rows)),
                  maximum_gap=str(max(F(item['gap']) for item in record_rows)))
    totals['root_bit_history_masses'] = {str(bit): str(sum(
        (F(item['canonical_history_probability']) for item in record_rows if item['record'] & 1 == bit), F(0)))
        for bit in (0, 1)}
    witness = dict(schema='ri65-residual-reentry-certificate-v1', accepted_source_pins=PINS,
                    accepted_problem_sha256=problem['hashes']['problem_without_self_hash'],
                    parent=B, rectangle=R, axes=AXES, first_newborn_bit_weight='1/2',
                    two_birth_full_map_factor='1/4', coverage=coverage, record_rows=record_rows,
                    record_groups=grouped, totals=totals, geometry=geometry,
                    symbolic_scope='conditional full-D diamonds and affine bounds; no evaluated q6',
                    formal_companion_bounds='0<=z0,z1<=1; strict admitted rows give z0,z1<1',
                    history_transports=transport_manifest,
                    manifests=dict(raw_marked_histories=digest(raw_histories),
                                   canonical_record_rows=digest(record_rows),
                                   symbolic_full_record_diamonds=digest(diamond_manifest),
                                   formal_affine_residuals=digest(formal_residuals),
                                   targeted_geometry=digest(geometry)))
    evidence = dict(problem=problem, proof=proof, actual=actual, accepted_controls=accepted_controls,
                    accepted_report=accepted_report, raw=raw)
    budget('all B records, histories and structural diamonds checked; no q6 evaluated')
    return witness, evidence


def verify_certificate(certificate, expected):
    require(isinstance(certificate, dict) and set(certificate) == set(expected),
            'new certificate fields are missing or unknown')
    require(certificate['accepted_source_pins'] == expected['accepted_source_pins'],
            'new certificate accepted-source pins mismatch')
    require(certificate['axes'] == list(AXES), 'new certificate has wrong labeled rectangle axes')
    require(isinstance(certificate['record_rows'], list)
            and [item['record'] for item in certificate['record_rows']] == list(range(32)),
            'new certificate omits or duplicates a full B record')
    require(certificate['first_newborn_bit_weight'] == '1/2'
            and certificate['two_birth_full_map_factor'] == '1/4',
            'new certificate has an incorrect newborn-bit factor')
    for actual, target in zip(certificate['record_rows'], expected['record_rows']):
        require(actual['fixed_natural_history_probability'] == target['fixed_natural_history_probability']
                and actual['canonical_history_probability'] == target['canonical_history_probability'],
                'new certificate history weights mismatch')
    require(certificate['totals']['all_B_lower_bound'] == expected['totals']['all_B_lower_bound'],
            'new certificate residual lower bound mismatch')
    require(canonical_json(certificate) == canonical_json(expected),
            'new certificate differs from exact targeted reconstruction')


def rejected(name, function, message):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == message, name + ': rejected for unintended reason')
        return name
    raise RuntimeError(name + ': malformed witness accepted')


def controls(expected, evidence):
    result = []
    def clone():
        return load_json(canonical_json(expected))
    bad = clone()
    bad['accepted_source_pins']['ri63_checker'] = '0'*64
    result.append(rejected('wrong_dependency_pin', lambda: verify_certificate(bad, expected),
                           'new certificate accepted-source pins mismatch'))
    result.append(rejected('changed_dependency_bytes',
                           lambda: check_pin(evidence['raw']['ri63_checker']+b'\n', PINS['ri63_checker']),
                           'accepted dependency byte pin mismatch'))
    bad = clone()
    bad['axes'] = [7, 31]
    result.append(rejected('wrong_axis', lambda: verify_certificate(bad, expected),
                           'new certificate has wrong labeled rectangle axes'))
    bad = clone()
    bad['record_rows'].pop()
    result.append(rejected('missing_record', lambda: verify_certificate(bad, expected),
                           'new certificate omits or duplicates a full B record'))
    altered_mix = list(evidence['actual'])
    altered_mix[0] += 1
    result.append(rejected('corrupt_mixture', lambda: verify_mixture(altered_mix, evidence['proof']['alpha'],
                           F(1, 36), F(evidence['problem']['c5'])),
                           'accepted strict mixture formula mismatch'))
    bad = clone()
    bad['record_rows'][0]['canonical_history_probability'] = str(
        F(bad['record_rows'][0]['canonical_history_probability'])+1)
    result.append(rejected('corrupt_history', lambda: verify_certificate(bad, expected),
                           'new certificate history weights mismatch'))
    bad = clone()
    bad['first_newborn_bit_weight'] = '1'
    result.append(rejected('wrong_factor_two', lambda: verify_certificate(bad, expected),
                           'new certificate has an incorrect newborn-bit factor'))
    bad = clone()
    bad['totals']['all_B_lower_bound'] = str(F(bad['totals']['all_B_lower_bound'])+F(1, 1000))
    result.append(rejected('wrong_lower_bound', lambda: verify_certificate(bad, expected),
                           'new certificate residual lower bound mismatch'))
    first = expected['record_rows'][0]
    f, a0, a1, gap = (F(first[name]) for name in ('f', 'a7', 'a9', 'gap'))
    bad_mu = {'1': F(1), 'z0': a0/f, 'z1': -a1/f}
    result.append(rejected('wrong_formal_residual_sign',
                           lambda: verify_affine_residual(f, a0, a1, gap, bad_mu),
                           'formal affine residual identity failed'))
    result.append(rejected('untransported_newborn_labels',
                           lambda: verify_newborn_transport(B+(31, 7), B+(7, 31),
                                                            tuple(range(7)), 32, 64),
                           'common terminal newborn transport failed'))
    return result


def deadline(signum, frame):
    raise RuntimeError('900-second wall-time alarm expired')


def main():
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    try:
        witness, evidence = reconstruct_witness()
        if sys.argv[1:] == ['--witness']:
            print(canonical_json(witness))
            return
        certificate = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
        verify_certificate(certificate, witness)
        negative_controls = controls(witness, evidence)
        print('targeted_coverage=' + canonical_json(witness['coverage']))
        print('reentry_bounds=' + canonical_json(witness['totals']))
        print('record_groups=' + canonical_json(witness['record_groups']))
        print('negative_controls=' + canonical_json(negative_controls))
        print('witness_sha256=' + digest(witness))
        print('DONE: exact positive noncritical re-entry lower bound; no q6 or asymptotic verdict')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
