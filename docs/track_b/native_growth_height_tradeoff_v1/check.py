#!/usr/bin/env python3
"""RI-70: exact height endpoints on the original RI-63 primary-optimal face.

Standard library only. This is a certificate checker, NEVER a solver or search.
It byte-pins accepted RI-63/RI-66 sources and certificates, replays RI-63's
complete canonical proof and strict rows through the unchanged RI-66 interface,
and reuses the accepted terminal factors explicitly. New height coefficients
are rebuilt from all raw marked histories and labeled proper ideal occurrences.
The endpoint face retains all 798 coordinates, including zero-primary-cost
coordinates; it does not impose the canonical tie-break on endpoint witnesses.

Only orders through size six and the accepted parent-five probability layer
are used. --problem emits the exact derived coefficients and manifests; default
mode checks two supplied rational primal-dual endpoints. No file writes, subprocesses,
downloads, numerical libraries or optimization calls are used. The predeclared
envelope is 1800 seconds and two GiB, with alarm/checkpoint enforcement (not a
hard OS allocation limit); accepted helper subruns retain their own limits.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from pathlib import Path
import json
import resource
import runpy
import signal
import sys
import time


PINS = {
    'ri66_checker': 'cf54313465da754345406f58a1a60622e51c034d954f8147332c1578cd62fdab',
    'ri66_certificate': '67d6b6706da3100afa89f8c99c6a72b88a6b39c7a1bc628fa69a02e46eca9d01',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
RI66_WITNESS_SHA256 = 'e667fbade262c694bceb1d40628391b6f3b4acfb2357381c662b31068332680a'
RI63_PROBLEM_SHA256 = 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
MAX_SECONDS = 1800
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    if START_TIME is not None:
        require(time.monotonic()-START_TIME <= MAX_SECONDS, '1800-second time envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_RESIDENT_BYTES,
            'two-GiB resident-memory envelope exceeded')
    if stage:
        print('RI70: '+stage, file=sys.stderr, flush=True)


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
    def reject_constant(value):
        raise RuntimeError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def check_pin(raw, expected):
    require(sha256(raw).hexdigest() == expected, 'accepted dependency byte pin mismatch')


def bits(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


@cache
def height(order):
    require(len(order) <= 6 and all(type(past) is int and 0 <= past < (1 << v)
            and all(order[u] & past == order[u] for u in bits(past))
            for v, past in enumerate(order)), 'height order outside bounded domain')
    levels = []
    for past in order:
        levels.append(1+max((levels[u] for u in bits(past)), default=0))
    answer = max(levels, default=0)
    # Independent arbitrary-subset comparison, not another chain recurrence.
    subset_maximum = 0
    for mask in range(1 << len(order)):
        if all(order[v] & (1 << u) for v in bits(mask) for u in bits(mask) if u < v):
            subset_maximum = max(subset_maximum, mask.bit_count())
    require(answer == subset_maximum, 'height recurrence differs from arbitrary chain subsets')
    return answer


def verify_factor(kappa, mass, numerator, extensions):
    require(mass > 0 and kappa/mass == F(numerator, extensions),
            'intrinsic height factorization failed')


def verify_aggregation(raw, canonical):
    require(raw == canonical, 'raw marked-height aggregation lost labeled multiplicities')


def reconstruct_problem():
    global START_TIME
    START_TIME = time.monotonic()
    base = Path(__file__).resolve().parent.parent
    folders = dict(ri66='native_growth_terminal_cost_v1', ri63='native_growth_expected_defect_completion_v1',
                   ri41='native_growth_height_normalization_v1')
    paths = {name: base/folders[name[:4]]/('check.py' if name.endswith('checker') else 'CERTIFICATE.json')
             for name in PINS}
    raw = {name: path.read_bytes() for name, path in paths.items()}
    for name in PINS:
        check_pin(raw[name], PINS[name])
    budget('accepted inputs pinned; replaying complete RI-63 canonical and strict certificates')
    helper66 = runpy.run_path(str(paths['ri66_checker']))
    helper, original, accepted_report, accepted_controls, _, _ = helper66['reconstruct_accepted']()
    require(original['hashes']['problem_without_self_hash'] == RI63_PROBLEM_SHA256,
            'accepted original problem identity changed')
    accepted_certificate = helper['load_json'](raw['ri63_certificate'])
    proof = helper['check_certificate_core'](accepted_certificate, original)
    terminal_certificate = helper66['load_json'](raw['ri66_certificate'])
    require(digest(terminal_certificate) == RI66_WITNESS_SHA256, 'accepted terminal-factor identity changed')
    # This explicitly reuses the accepted RI-66 certificate, not a second
    # complete RI-66 reconstruction. Its factors are checked below against
    # independently recomputed raw masses and intrinsic height statistics.
    for terminal in terminal_certificate['terminals']:
        helper66['verify_type_record'](terminal)
    width, row_count = len(original['roots']), len(original['rows'])
    node_component = {tuple(item['key']): item['component'] for item in original['nodes']}
    raw_kappa, raw_mass = [F(0)]*width, [F(0)]*width
    marked_rows = proper_slots = 0
    first_height_preserving_slot = None
    heights_seen, terminals_seen, nodes_seen = set(), set(), set()
    raw_manifest = sha256()
    budget('deriving height costs from every raw marked history and labeled proper slot')
    for parent in helper['parents'](5):
        budget()
        h = height(parent)
        heights_seen.add(parent)
        require(height(parent+(31,)) == h+1, 'universal-top height baseline is not one')
        heights_seen.add(parent+(31,))
        for record in range(32):
            pi = helper['history_probability'](parent, record)
            marked_rows += 1
            for part in helper['ideals'](parent):
                if part == 31:
                    continue
                q = parent+(part,)
                heights_seen.add(q)
                terminals_seen.add(q)
                dh = height(q)-h
                require(dh in (0, 1), 'proper birth has invalid height increment')
                key = helper['node'](parent, part, record)
                c = node_component[key]
                mass = pi*helper['potential'](parent, part, record & part)
                raw_mass[c] += mass
                raw_kappa[c] += mass*(dh-1)
                if dh == 0 and first_height_preserving_slot is None:
                    first_height_preserving_slot = (c, mass)
                nodes_seen.add(key)
                proper_slots += 1
                raw_manifest.update((canonical_json([parent, record, part, c, str(mass), dh])+'\n').encode())
    canonical_kappa, canonical_mass = [F(0)]*width, [F(0)]*width
    canonical_slot_count = 0
    for row in original['rows']:
        parent, pi = tuple(row['past_masks']), F(row['pi'])
        for slot in row['slots']:
            c, mass = slot['component'], pi*F(slot['u'])
            canonical_mass[c] += mass
            canonical_kappa[c] += mass*(height(parent+(slot['past_mask'],))-height(parent)-1)
            canonical_slot_count += 1
    verify_aggregation(raw_kappa, canonical_kappa)
    verify_aggregation(raw_mass, canonical_mass)
    require(nodes_seen == set(node_component) and all(x <= 0 for x in raw_kappa),
            'height coefficient coverage or sign failure')
    terminal_factors = []
    for t, terminal in enumerate(terminal_certificate['terminals']):
        q, numerator, roles = tuple(terminal['past_masks']), 0, []
        require(helper66['extension_count'](q) == terminal['extensions'],
                'accepted terminal linear-extension count changed')
        for role in terminal['roles']:
            parent = helper66['delete_vertex'](q, role['vertex'])
            require(helper66['extension_count'](parent) == role['extensions'],
                    'accepted maximal-deletion multiplicity changed')
            dh = height(q)-height(parent)
            require(dh in (0, 1), 'maximal-deletion role has invalid height increment')
            numerator += role['extensions']*(dh-1)
            roles.append([role['vertex'], role['extensions'], dh])
        terminal_factors.append(dict(terminal_type=t, past_masks=q, extensions=terminal['extensions'],
                                     height_numerator=numerator, roles=roles))
    component_factors = []
    for c, component in enumerate(terminal_certificate['components']):
        require(c == component['component'] and raw_mass[c] == F(component['U'])
                and F(component['beta']) == proof['beta'][c],
                'accepted component mass or primary objective changed')
        t = component['terminal_type']
        helper66['verify_factorization'](component, terminal_certificate['terminals'][t])
        verify_factor(raw_kappa[c], raw_mass[c], terminal_factors[t]['height_numerator'],
                      terminal_factors[t]['extensions'])
        component_factors.append(dict(component=c, terminal_type=t, kappa=str(raw_kappa[c]),
                                      kappa_over_U=str(raw_kappa[c]/raw_mass[c])))
    matrix, beta = proof['matrix'], proof['beta']
    eta, interior_c = F(original['eta5']), F(original['c5'])
    def affine_height(alpha):
        return 1+sum((k*a for k, a in zip(raw_kappa, alpha)), F(0))
    canonical_h = affine_height(proof['alpha'])
    alternative_h = affine_height(proof['alternative'])
    interior_h = affine_height([interior_c]*width)
    actual_h = (1-eta)*canonical_h+eta*interior_h
    # Independent full-complement row calculation for both retained witnesses.
    for alpha, expected in ((proof['alpha'], canonical_h), (proof['alternative'], alternative_h)):
        direct = F(0)
        for row in original['rows']:
            parent, pi = tuple(row['past_masks']), F(row['pi'])
            full = F(1)
            for slot in row['slots']:
                probability = F(slot['u'])*alpha[slot['component']]
                full -= probability
                direct += pi*probability*(height(parent+(slot['past_mask'],))-height(parent))
            require(full >= 0, 'retained primary witness has negative full complement')
            direct += pi*full
        require(direct == expected and 0 <= direct <= 1,
                'affine height differs from complete marked-row expectation')
    require(canonical_h == F('25799901101980099/26711031029760000'),
            'retained canonical height disagrees with accepted RI-69 result')
    counts = dict(original_rows=row_count, original_columns=width, raw_marked_rows=marked_rows,
                  proper_labeled_slots=proper_slots, canonical_labeled_slots=canonical_slot_count,
                  local_nodes=len(nodes_seen), natural_proper_terminals=len(terminals_seen),
                  distinct_height_orders=len(heights_seen), intrinsic_terminal_types=len(terminal_factors),
                  negative_kappa=sum(x < 0 for x in raw_kappa), zero_kappa=sum(x == 0 for x in raw_kappa),
                  numerically_evaluated_q6=0, solver_calls=0)
    require((row_count, width, marked_rows, proper_slots, canonical_slot_count, len(nodes_seen))
            == (1490, 798, 11424, 142944, 15702, 2961), 'original complete face coverage changed')
    derived = dict(schema='ri70-height-face-problem-v1', dependencies=PINS,
        accepted_problem_sha256=RI63_PROBLEM_SHA256, accepted_terminal_certificate_sha256=RI66_WITNESS_SHA256,
        counts=counts, primary_face_value=str(proof['objective']), m5=accepted_report['m5'],
        B5=original['B5'], kappa=[str(x) for x in raw_kappa],
        canonical_height=str(canonical_h), alternative_height=str(alternative_h),
        interior_height=str(interior_h), actual_canonical_height=str(actual_h),
        fixed_eta=str(eta), fixed_interior_c=str(interior_c), terminal_factors=terminal_factors,
        component_factors=component_factors, accepted_certificate_controls=accepted_controls,
        manifests=dict(original_caps=digest(original['rows']), roots=digest(original['roots']),
                       raw_marked_height_weights=raw_manifest.hexdigest(), kappa=digest([str(x) for x in raw_kappa]),
                       terminal_factors=digest(terminal_factors), component_factors=digest(component_factors)))
    derived['problem_sha256'] = digest(derived)
    for name, path in paths.items():
        check_pin(path.read_bytes(), PINS[name])
    budget('exact original height-face problem rebuilt; no solver or search performed')
    return dict(derived=derived, matrix=matrix, beta=beta, kappa=raw_kappa, face=proof['objective'],
                canonical=proof['alpha'], alternative=proof['alternative'], raw=raw,
                raw_mass=raw_mass, terminal_factors=terminal_factors,
                component_factors=component_factors, paths=paths,
                first_height_preserving_slot=first_height_preserving_slot)


def parse_fraction(value, name):
    require(isinstance(value, str), name+': expected fraction string')
    try:
        fraction = F(value)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError(name+': invalid fraction') from None
    require(str(fraction) == value, name+': noncanonical fraction')
    return fraction


def parse_sparse(encoded, count, name):
    require(isinstance(encoded, dict), name+': expected sparse object')
    result = {}
    for key, value in encoded.items():
        require(isinstance(key, str) and key.isascii() and key.isdecimal()
                and str(int(key)) == key and 0 <= int(key) < count, name+': invalid index')
        fraction = parse_fraction(value, name)
        require(fraction > 0, name+': sparse entries must be positive')
        result[int(key)] = fraction
    return result


def check_endpoint(endpoint, mode, state):
    require(isinstance(endpoint, dict) and set(endpoint) == {'alpha', 'row_dual', 'face_multiplier', 'height'},
            'endpoint has missing or unknown fields')
    require(mode in ('minimum', 'maximum'), 'unknown height endpoint')
    matrix, beta, kappa, face = (state[k] for k in ('matrix', 'beta', 'kappa', 'face'))
    width = len(beta)
    sparse_alpha = parse_sparse(endpoint['alpha'], width, 'endpoint_alpha')
    alpha = [sparse_alpha.get(c, F(0)) for c in range(width)]
    # Every original row and column is retained. In particular no beta>=0
    # elimination or lexicographic constraints are imposed on this face.
    masses = [sum((a*alpha[c] for c, a in row.items()), F(0)) for row in matrix]
    require(all(0 <= mass <= 1 for mass in masses), 'endpoint original-row primal cap failure')
    require(sum((b*a for b, a in zip(beta, alpha)), F(0)) == face,
            'endpoint is not on original primary-optimal face')
    y = parse_sparse(endpoint['row_dual'], len(matrix), 'endpoint_row_dual')
    multiplier = parse_fraction(endpoint['face_multiplier'], 'face_multiplier')
    sign = 1 if mode == 'minimum' else -1
    cost = [sign*k for k in kappa]
    reduced = [value-multiplier*b for value, b in zip(cost, beta)]
    for j, value in y.items():
        for c, a in matrix[j].items():
            reduced[c] += value*a
    require(all(value >= 0 for value in reduced), 'endpoint original-column dual feasibility failure')
    primal = sum((value*a for value, a in zip(cost, alpha)), F(0))
    dual = -sum(y.values(), F(0))+multiplier*face
    require(primal == dual, 'endpoint exact primal-dual gap is nonzero')
    require(all(alpha[c]*reduced[c] == 0 for c in range(width))
            and all(value*(1-masses[j]) == 0 for j, value in y.items()),
            'endpoint exact complementarity failed')
    height_value = 1+sum((k*a for k, a in zip(kappa, alpha)), F(0))
    require(height_value == parse_fraction(endpoint['height'], 'endpoint_height')
            and 0 <= height_value <= 1, 'endpoint claimed height mismatch')
    eta = F(state['derived']['fixed_eta'])
    mixture = (1-eta)*height_value+eta*F(state['derived']['interior_height'])
    return dict(height=str(height_value), signed_cost=str(primal), dual_value=str(dual),
                face_multiplier=str(multiplier), positive_primal_coordinates=len(sparse_alpha),
                positive_dual_rows=len(y), original_rows_checked=len(matrix), original_columns_checked=width,
                tight_original_rows=sum(mass == 1 for mass in masses),
                zero_reduced_columns=sum(value == 0 for value in reduced),
                positive_zero_beta_coordinates=sum(alpha[c] > 0 and beta[c] == 0 for c in range(width)),
                counterfactual_fixed_mixture_height=str(mixture),
                primal_sha256=digest(endpoint['alpha']), dual_sha256=digest(endpoint['row_dual']))


def check_certificate(certificate, state):
    require(isinstance(certificate, dict) and set(certificate) == {
        'schema', 'problem_sha256', 'dependencies', 'endpoints'}, 'certificate has missing or unknown fields')
    require(certificate['schema'] == 'ri70-height-face-endpoints-v1', 'certificate schema mismatch')
    require(certificate['problem_sha256'] == state['derived']['problem_sha256']
            and certificate['dependencies'] == PINS, 'height-face certificate input identity mismatch')
    require(isinstance(certificate['endpoints'], dict)
            and set(certificate['endpoints']) == {'minimum', 'maximum'}, 'both height endpoints are required')
    result = {mode: check_endpoint(certificate['endpoints'][mode], mode, state)
              for mode in ('minimum', 'maximum')}
    low, high = F(result['minimum']['height']), F(result['maximum']['height'])
    require(low <= F(state['derived']['canonical_height']) <= high
            and low <= F(state['derived']['alternative_height']) <= high,
            'retained primary witnesses fall outside certified endpoint interval')
    result['width'] = str(high-low)
    result['actual_law_changed'] = False
    return result


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': rejected for an unintended reason')
        return name
    raise RuntimeError(name+': malformed input accepted')


def certificate_controls(certificate, state):
    clone = lambda: load_json(canonical_json(certificate))
    controls = [expect_rejection('changed_dependency_bytes',
        lambda: check_pin(state['raw']['ri66_checker']+b' ', PINS['ri66_checker']),
        'accepted dependency byte pin mismatch')]
    bad = clone(); bad['problem_sha256'] = '0'*64
    controls.append(expect_rejection('wrong_problem_manifest', lambda: check_certificate(bad, state),
                                     'height-face certificate input identity mismatch'))
    bad = clone(); del bad['endpoints']['maximum']
    controls.append(expect_rejection('missing_maximum_endpoint', lambda: check_certificate(bad, state),
                                     'both height endpoints are required'))
    original = certificate['endpoints']['minimum']
    bad_endpoint = dict(original, alpha={'0': '-1'})
    controls.append(expect_rejection('negative_primal_coordinate', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint_alpha: sparse entries must be positive'))
    row = next(row for row in state['matrix'] if row)
    c, value = next(iter(row.items()))
    bad_endpoint = dict(original, alpha={str(c): str(2/value)})
    controls.append(expect_rejection('violated_original_row_cap', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint original-row primal cap failure'))
    bad_endpoint = dict(original, alpha={})
    controls.append(expect_rejection('wrong_primary_face', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint is not on original primary-optimal face'))
    bad_endpoint = dict(original, row_dual={'0': '-1'})
    controls.append(expect_rejection('negative_inequality_dual', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint_row_dual: sparse entries must be positive'))
    bad_endpoint = dict(original, row_dual={}, face_multiplier='0')
    controls.append(expect_rejection('infeasible_full_column_dual', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint original-column dual feasibility failure'))
    wrong_y = dict(original['row_dual']); wrong_y['0'] = str(F(wrong_y.get('0', '0'))+1)
    bad_endpoint = dict(original, row_dual=wrong_y)
    controls.append(expect_rejection('positive_exact_duality_gap', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint exact primal-dual gap is nonzero'))
    bad_endpoint = dict(original, height=str(F(original['height'])+1))
    controls.append(expect_rejection('wrong_endpoint_height', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'endpoint claimed height mismatch'))
    bad_endpoint = dict(original, face_multiplier='0/2')
    controls.append(expect_rejection('noncanonical_face_multiplier', lambda: check_endpoint(bad_endpoint, 'minimum', state),
                                     'face_multiplier: noncanonical fraction'))
    c = next(c for c, value in enumerate(state['kappa']) if value < 0)
    t = state['component_factors'][c]['terminal_type']; terminal = state['terminal_factors'][t]
    controls.append(expect_rejection('corrupt_intrinsic_height_cost',
        lambda: verify_factor(state['kappa'][c]+1, state['raw_mass'][c], terminal['height_numerator'], terminal['extensions']),
        'intrinsic height factorization failed'))
    omitted_c, omitted_mass = state['first_height_preserving_slot']
    wrong = list(state['kappa']); wrong[omitted_c] += omitted_mass
    controls.append(expect_rejection('dropped_marked_slot_multiplicity', lambda: verify_aggregation(wrong, state['kappa']),
                                     'raw marked-height aggregation lost labeled multiplicities'))
    controls.append(expect_rejection('duplicate_json_key', lambda: load_json('{"height":0,"height":1}'),
                                     'duplicate JSON object key'))
    return controls


def deadline_handler(signum, frame):
    raise RuntimeError('1800-second wall-time alarm expired')


def main():
    require(sys.argv[1:] in ([], ['--problem']), 'unknown command arguments')
    signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    try:
        state = reconstruct_problem()
        if sys.argv[1:] == ['--problem']:
            print(canonical_json(state['derived']))
            return
        certificate = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
        result = check_certificate(certificate, state)
        controls = certificate_controls(certificate, state)
        for name, path in state['paths'].items():
            check_pin(path.read_bytes(), PINS[name])
        print('coverage='+canonical_json(state['derived']['counts']))
        print('retained_heights='+canonical_json({key: state['derived'][key]
              for key in ('canonical_height', 'alternative_height', 'actual_canonical_height')}))
        print('endpoints='+canonical_json(result))
        print('negative_controls='+canonical_json(controls))
        print('problem_sha256='+state['derived']['problem_sha256'])
        print('DONE: exact bounded original-face height endpoints; unchanged actual law')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
