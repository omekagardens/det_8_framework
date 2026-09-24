#!/usr/bin/env python3
"""RI-72: exact minimum height with intrinsic critical-child suppression.

Standard library certificate verification only: no optimizer, search, download,
subprocess or file write. Pinned RI-70 reconstruction and endpoint proofs are
replayed unchanged. RI-63 is reconstructed once more to obtain its raw marked
row/node interface, which RI-70 does not return. Criticality is independently
derived from arbitrary-subset Ferrers defects and all maximal deletions, never
from a parent flag. No order above six or parent-six probability is evaluated.

All original 1490 caps, 798 columns and the exact primary face are retained;
only intrinsic terminal-critical coordinates are additionally set to zero.
Other zero-primary-cost coordinates remain legal. A supplied rational dual
certifies the minimum VALUE, not a lexicographic endpoint witness or a new law.
--problem exports reconstructed metadata. Default use verifies CERTIFICATE.json.
The 1800-second alarm and checkpointed two-GiB peak-RSS envelope are not a hard
OS allocator cap; inherited helper subruns keep their own declared limits.
"""

from fractions import Fraction as F
from functools import cache
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
    'ri70_checker': 'af145a06b8028533d85be5853a4e840735a2ccf2e673846ad5465cb58b793995',
    'ri70_certificate': 'de716ec1e07274ebdb431b6d7e2ccd37ba21af67268d208923db76d95c51c8dd',
    'ri66_checker': 'cf54313465da754345406f58a1a60622e51c034d954f8147332c1578cd62fdab',
    'ri66_certificate': '67d6b6706da3100afa89f8c99c6a72b88a6b39c7a1bc628fa69a02e46eca9d01',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
RI70_PROBLEM_SHA256 = '69db0630770c4a0f61ed234e974d8c699e6ea29c6bac4ed9d566ad0a7fad22ba'
RI63_PROBLEM_SHA256 = 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
MAX_SECONDS = 1800
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None
FERRERS = {}


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
        print('RI72: '+stage, file=sys.stderr, flush=True)


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


def validate_order(order):
    require(len(order) <= 6 and all(type(past) is int and 0 <= past < (1 << v)
            and all(order[u] & past == order[u] for u in bits(past))
            for v, past in enumerate(order)), 'criticality order outside bounded domain')


def induced(order, mask):
    kept = bits(mask)
    return tuple(sum(1 << i for i, u in enumerate(kept) if order[v] & (1 << u)) for v in kept)


def maxima(order):
    ancestors = 0
    for past in order:
        ancestors |= past
    return bits(((1 << len(order))-1) & ~ancestors)


def partitions(n, ceiling=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, n if ceiling is None else ceiling), 0, -1):
            for tail in partitions(n-first, first):
                yield (first,)+tail


def build_ferrers(helper):
    inventory = []
    for n in range(7):
        found = set()
        for partition in partitions(n):
            cells = tuple((i, j) for i, length in enumerate(partition) for j in range(length))
            order = tuple(sum(1 << u for u, (a, b) in enumerate(cells)
                              if a <= i and b <= j and (a, b) != (i, j)) for i, j in cells)
            for permutation in permutations(range(n)):
                relabeled = [0]*n
                for v, past in enumerate(order):
                    relabeled[permutation[v]] = sum(1 << permutation[u] for u in bits(past))
                if all(past < (1 << v) for v, past in enumerate(relabeled)):
                    found.add(tuple(relabeled))
        require(found == set(helper['FERRERS_BY_SIZE'][n]), 'independent Ferrers catalogue mismatch')
        FERRERS[n] = frozenset(found)
        inventory.append(dict(size=n, natural_orders=len(found), sha256=digest(sorted(found))))
    return inventory


@cache
def defect(order):
    validate_order(order)
    largest = 0
    for mask in range(1 << len(order)):
        kept = induced(order, mask)
        if kept in FERRERS[len(kept)]:
            largest = max(largest, len(kept))
    return len(order)-largest


@cache
def critical(order):
    validate_order(order)
    vertices = maxima(order)
    full = (1 << len(order))-1
    return len(vertices) >= 2 and all(defect(induced(order, full ^ (1 << v))) == defect(order)-1
                                      for v in vertices)


def verify_classification(order, claimed):
    require(type(claimed) is bool and critical(order) == claimed,
            'incorrect intrinsic terminal-critical classification')


def verify_raw_masses(raw, canonical):
    require(raw == canonical, 'critical-entry marked or labeled multiplicity mismatch')


def reference_report(alpha, base, critical_weights):
    height = 1+sum((k*a for k, a in zip(base['kappa'], alpha)), F(0))
    entry = sum((w*a for w, a in zip(critical_weights, alpha)), F(0))
    eta = F(base['derived']['fixed_eta'])
    interior_c = F(base['derived']['fixed_interior_c'])
    return dict(height=str(height), critical_entry_mass=str(entry),
                critical_suppressed=entry == 0,
                fixed_mixture_critical_entry_mass=str((1-eta)*entry+eta*interior_c*sum(critical_weights, F(0))))


def reconstruct_problem():
    global START_TIME
    START_TIME = time.monotonic()
    root = Path(__file__).resolve().parent.parent
    folders = dict(ri70='native_growth_height_tradeoff_v1', ri66='native_growth_terminal_cost_v1',
                   ri63='native_growth_expected_defect_completion_v1', ri41='native_growth_height_normalization_v1')
    paths = {name: root/folders[name[:4]]/('check.py' if name.endswith('checker') else 'CERTIFICATE.json')
             for name in PINS}
    raw = {name: path.read_bytes() for name, path in paths.items()}
    for name in PINS:
        check_pin(raw[name], PINS[name])
    budget('all accepted inputs pinned; replaying RI-70 original-face certificates')
    helper70 = runpy.run_path(str(paths['ri70_checker']))
    base = helper70['reconstruct_problem']()
    require(base['derived']['problem_sha256'] == RI70_PROBLEM_SHA256, 'accepted RI-70 problem changed')
    certificate70 = helper70['load_json'](raw['ri70_certificate'])
    report70 = helper70['check_certificate'](certificate70, base)
    controls70 = helper70['certificate_controls'](certificate70, base)
    budget('obtaining raw marked row interface; independently classifying terminal orders')
    helper = runpy.run_path(str(paths['ri63_checker']))
    original = helper['build_problem']()
    require(original['hashes']['problem_without_self_hash'] == RI63_PROBLEM_SHA256,
            'accepted original raw problem changed')
    inventory = build_ferrers(helper)
    terminal_classes, critical_types = [], set()
    for item in base['terminal_factors']:
        order = tuple(item['past_masks'])
        t = item['terminal_type']
        full = (1 << len(order))-1
        deletion_defects = [[v, defect(induced(order, full ^ (1 << v)))] for v in maxima(order)]
        is_critical = critical(order)
        if is_critical:
            critical_types.add(t)
        terminal_classes.append(dict(terminal_type=t, past_masks=order, defect=defect(order),
                                     maximal_deletion_defects=deletion_defects, critical=is_critical))
    critical_components = {item['component'] for item in base['component_factors']
                           if item['terminal_type'] in critical_types}
    require(sorted(critical_components) == original['critical_child_components'],
            'independent critical-child set differs from accepted classification')
    width = len(base['beta'])
    node_component = {tuple(item['key']): item['component'] for item in original['nodes']}
    raw_u, raw_critical = [F(0)]*width, [F(0)]*width
    raw_rows = raw_slots = raw_critical_slots = 0
    nodes_seen = set()
    first_critical_slot = confusion = None
    raw_manifest = sha256()
    for parent in helper['parents'](5):
        budget()
        parent_critical = critical(parent)
        require(not critical(parent+(31,)), 'a full birth unexpectedly has a critical terminal')
        for record in range(32):
            pi = helper['history_probability'](parent, record)
            raw_rows += 1
            for part in helper['ideals'](parent):
                if part == 31:
                    continue
                q = parent+(part,)
                child_critical = critical(q)
                key = helper['node'](parent, part, record)
                c = node_component[key]
                require(child_critical == (c in critical_components),
                        'marked component has inconsistent intrinsic terminal criticality')
                mass = pi*helper['potential'](parent, part, record & part)
                raw_u[c] += mass
                if child_critical:
                    raw_critical[c] += mass
                    raw_critical_slots += 1
                    if first_critical_slot is None:
                        first_critical_slot = (c, mass)
                if parent_critical != child_critical and confusion is None:
                    confusion = dict(parent=parent, past_mask=part, child=q,
                                     parent_critical=parent_critical, child_critical=child_critical)
                nodes_seen.add(key)
                raw_slots += 1
                raw_manifest.update((canonical_json([parent, record, part, c, str(mass), child_critical])+'\n').encode())
    canonical_critical = [F(0)]*width
    canonical_slots = 0
    for row in original['rows']:
        p, pi = tuple(row['past_masks']), F(row['pi'])
        for slot in row['slots']:
            if critical(p+(slot['past_mask'],)):
                canonical_critical[slot['component']] += pi*F(slot['u'])
            canonical_slots += 1
    verify_raw_masses(raw_critical, canonical_critical)
    verify_raw_masses(raw_u, base['raw_mass'])
    require(all(raw_critical[c] == (raw_u[c] if c in critical_components else 0) for c in range(width))
            and all(raw_u[c] > 0 for c in range(width)), 'critical-entry mass support mismatch')
    references = dict(canonical=base['canonical'], alternative=base['alternative'])
    for mode in ('minimum', 'maximum'):
        sparse = helper70['parse_sparse'](certificate70['endpoints'][mode]['alpha'], width, 'ri70_alpha')
        references['ri70_'+mode] = [sparse.get(c, F(0)) for c in range(width)]
    reports = {name: reference_report(alpha, base, raw_critical) for name, alpha in references.items()}
    require(reports['canonical']['critical_entry_mass'] == '0'
            and all(base['canonical'][c] == 0 for c in critical_components),
            'accepted canonical witness does not prove nonempty critical-suppressed slice')
    removed = list(references['ri70_minimum'])
    removed_coordinates = [c for c in sorted(critical_components) if removed[c] > 0]
    for c in critical_components:
        removed[c] = F(0)
    require(all(sum((value*removed[c] for c, value in row.items()), F(0)) <= 1 for row in base['matrix'])
            and sum((b*a for b, a in zip(base['beta'], removed)), F(0)) == base['face'],
            'mechanical critical-coordinate removal is not on the original face')
    reports['ri70_minimum_critical_removed'] = reference_report(removed, base, raw_critical)
    counts = dict(original_rows=len(base['matrix']), original_columns=width, raw_marked_rows=raw_rows,
                  proper_labeled_slots=raw_slots, canonical_labeled_slots=canonical_slots,
                  local_nodes=len(nodes_seen), terminal_types=len(terminal_classes),
                  critical_terminal_types=len(critical_types), critical_components=len(critical_components),
                  critical_positive_beta=sum(base['beta'][c] > 0 for c in critical_components),
                  critical_zero_beta=sum(base['beta'][c] == 0 for c in critical_components),
                  noncritical_zero_beta=sum(base['beta'][c] == 0 for c in range(width) if c not in critical_components),
                  raw_critical_proper_slots=raw_critical_slots, solver_calls=0, numerically_evaluated_q6=0)
    require((counts['original_rows'], width, raw_rows, raw_slots, canonical_slots, len(nodes_seen))
            == (1490, 798, 11424, 142944, 15702, 2961), 'original critical-height coverage changed')
    derived = dict(schema='ri72-critical-height-problem-v1', dependencies=PINS,
        accepted_ri70_problem_sha256=RI70_PROBLEM_SHA256, accepted_original_problem_sha256=RI63_PROBLEM_SHA256,
        counts=counts, critical_components=sorted(critical_components), critical_types=sorted(critical_types),
        terminal_classes=terminal_classes, ferrers_inventory=inventory,
        parent_terminal_confusion=confusion, references=reports, removed_coordinates=removed_coordinates,
        primary_face_value=str(base['face']), fixed_eta=base['derived']['fixed_eta'],
        fixed_interior_c=base['derived']['fixed_interior_c'], accepted_ri70_controls=controls70,
        accepted_ri70_endpoint_report_sha256=digest(report70),
        manifests=dict(critical_components=digest(sorted(critical_components)), terminal_classes=digest(terminal_classes),
            raw_critical_entry_weights=raw_manifest.hexdigest(),
            critical_component_masses=digest([str(v) for v in raw_critical]),
            inherited_kappa=base['derived']['manifests']['kappa']))
    derived['problem_sha256'] = digest(derived)
    for name, path in paths.items():
        check_pin(path.read_bytes(), PINS[name])
    budget('complete critical-suppressed face reconstructed; no search performed')
    return dict(derived=derived, base=base, critical=critical_components, critical_weights=raw_critical,
                removed=removed, references=references, raw=raw, paths=paths,
                first_critical_slot=first_critical_slot)


def parse_fraction(value, name):
    require(isinstance(value, str), name+': expected fraction string')
    try:
        fraction = F(value)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError(name+': invalid fraction') from None
    require(str(fraction) == value, name+': noncanonical fraction')
    return fraction


def parse_sparse(encoded, count, name, signed=False):
    require(isinstance(encoded, dict), name+': expected sparse object')
    result = {}
    for key, value in encoded.items():
        require(isinstance(key, str) and key.isascii() and key.isdecimal()
                and str(int(key)) == key and 0 <= int(key) < count, name+': invalid index')
        fraction = parse_fraction(value, name)
        require(fraction != 0 and (signed or fraction > 0), name+': invalid sparse sign or explicit zero')
        result[int(key)] = fraction
    return result


def check_minimum(minimum, state):
    require(isinstance(minimum, dict) and set(minimum) == {
        'alpha', 'row_dual', 'face_multiplier', 'critical_multipliers', 'height'},
        'minimum has missing or unknown fields')
    base, forbidden = state['base'], state['critical']
    matrix, beta, kappa, face = (base[name] for name in ('matrix', 'beta', 'kappa', 'face'))
    width = len(beta)
    sparse_alpha = parse_sparse(minimum['alpha'], width, 'minimum_alpha')
    alpha = [sparse_alpha.get(c, F(0)) for c in range(width)]
    require(all(alpha[c] == 0 for c in forbidden), 'minimum uses a forbidden terminal-critical coordinate')
    masses = [sum((value*alpha[c] for c, value in row.items()), F(0)) for row in matrix]
    require(all(0 <= mass <= 1 for mass in masses), 'minimum original-row primal cap failure')
    require(sum((b*a for b, a in zip(beta, alpha)), F(0)) == face,
            'minimum is not on original primary-optimal face')
    y = parse_sparse(minimum['row_dual'], len(matrix), 'minimum_row_dual')
    multiplier = parse_fraction(minimum['face_multiplier'], 'face_multiplier')
    mu = parse_sparse(minimum['critical_multipliers'], width, 'critical_multipliers', signed=True)
    require(set(mu) <= forbidden, 'critical equality multiplier has noncritical support')
    reduced = [k-multiplier*b-mu.get(c, F(0)) for c, (k, b) in enumerate(zip(kappa, beta))]
    for j, value in y.items():
        for c, a in matrix[j].items():
            reduced[c] += value*a
    require(all(value >= 0 for value in reduced), 'minimum original-column dual feasibility failure')
    primal = sum((k*a for k, a in zip(kappa, alpha)), F(0))
    dual = -sum(y.values(), F(0))+multiplier*face
    require(primal == dual, 'minimum exact primal-dual gap is nonzero')
    require(all(alpha[c]*reduced[c] == 0 for c in range(width))
            and all(value*(1-masses[j]) == 0 for j, value in y.items()),
            'minimum exact complementarity failure')
    height_value = 1+primal
    require(height_value == parse_fraction(minimum['height'], 'minimum_height') and 0 <= height_value <= 1,
            'minimum claimed height mismatch')
    entry = sum((a*w for a, w in zip(alpha, state['critical_weights'])), F(0))
    require(entry == 0, 'minimum has positive raw critical-entry mass')
    reports = state['derived']['references']
    require(F(reports['ri70_minimum']['height']) <= height_value
            <= F(reports['canonical']['height']) <= F(reports['ri70_maximum']['height']),
            'certified restricted height is inconsistent with retained feasible witnesses')
    removed_height = F(reports['ri70_minimum_critical_removed']['height'])
    require(height_value <= removed_height, 'mechanically removed feasible point beats certified minimum')
    eta, interior_c = F(base['derived']['fixed_eta']), F(base['derived']['fixed_interior_c'])
    return dict(height=str(height_value), signed_cost=str(primal), dual_value=str(dual),
                critical_entry_mass=str(entry), positive_primal_coordinates=len(sparse_alpha),
                positive_noncritical_zero_beta_coordinates=sum(alpha[c] > 0 and beta[c] == 0 for c in range(width)),
                positive_dual_rows=len(y), critical_multiplier_count=len(mu), face_multiplier=str(multiplier),
                original_rows_checked=len(matrix), original_columns_checked=width,
                critical_zero_equalities_checked=len(forbidden), tight_original_rows=sum(v == 1 for v in masses),
                zero_reduced_columns=sum(v == 0 for v in reduced),
                height_increase_over_ri70_minimum=str(height_value-F(reports['ri70_minimum']['height'])),
                canonical_height_gap=str(F(reports['canonical']['height'])-height_value),
                removed_reference_also_attains=removed_height == height_value,
                removed_reference_differing_coordinates=sum(a != b for a, b in zip(alpha, state['removed'])),
                fixed_mixture_critical_entry_mass=str(eta*interior_c*sum(state['critical_weights'], F(0))),
                fixed_mixture_height=str((1-eta)*height_value+eta*F(base['derived']['interior_height'])),
                lexicographic_witness_certified=False, actual_law_changed=False,
                primal_sha256=digest(minimum['alpha']), dual_sha256=digest(minimum['row_dual']),
                critical_multipliers_sha256=digest(minimum['critical_multipliers']))


def check_certificate(certificate, state):
    require(isinstance(certificate, dict) and set(certificate) == {
        'schema', 'problem_sha256', 'dependencies', 'minimum'}, 'certificate has missing or unknown fields')
    require(certificate['schema'] == 'ri72-critical-height-minimum-v1', 'certificate schema mismatch')
    require(certificate['problem_sha256'] == state['derived']['problem_sha256']
            and certificate['dependencies'] == PINS, 'critical-height certificate input identity mismatch')
    return check_minimum(certificate['minimum'], state)


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': rejected for an unintended reason')
        return name
    raise RuntimeError(name+': malformed input accepted')


def certificate_controls(certificate, state):
    original = certificate['minimum']
    base, forbidden = state['base'], state['critical']
    clone = lambda: load_json(canonical_json(certificate))
    controls = [expect_rejection('changed_dependency_bytes',
        lambda: check_pin(state['raw']['ri70_checker']+b' ', PINS['ri70_checker']),
        'accepted dependency byte pin mismatch')]
    bad = clone(); bad['problem_sha256'] = '0'*64
    controls.append(expect_rejection('wrong_problem_manifest', lambda: check_certificate(bad, state),
                                     'critical-height certificate input identity mismatch'))
    terminal = next(item for item in state['derived']['terminal_classes'] if item['critical'])
    controls.append(expect_rejection('wrong_critical_terminal_classification',
        lambda: verify_classification(tuple(terminal['past_masks']), False),
        'incorrect intrinsic terminal-critical classification'))
    confusion = state['derived']['parent_terminal_confusion']
    controls.append(expect_rejection('parent_flag_used_for_terminal',
        lambda: verify_classification(tuple(confusion['child']), confusion['parent_critical']),
        'incorrect intrinsic terminal-critical classification'))
    bad_min = dict(original, alpha={str(min(forbidden)): '1'})
    controls.append(expect_rejection('forbidden_critical_coordinate', lambda: check_minimum(bad_min, state),
                                     'minimum uses a forbidden terminal-critical coordinate'))
    bad_min = dict(original, alpha={'0': '-1'})
    controls.append(expect_rejection('negative_primal_coordinate', lambda: check_minimum(bad_min, state),
                                     'minimum_alpha: invalid sparse sign or explicit zero'))
    c, value = next((c, value) for row in base['matrix'] for c, value in row.items() if c not in forbidden)
    bad_min = dict(original, alpha={str(c): str(2/value)})
    controls.append(expect_rejection('violated_original_row_cap', lambda: check_minimum(bad_min, state),
                                     'minimum original-row primal cap failure'))
    bad_min = dict(original, alpha={})
    controls.append(expect_rejection('wrong_primary_face', lambda: check_minimum(bad_min, state),
                                     'minimum is not on original primary-optimal face'))
    bad_min = dict(original, row_dual={'0': '-1'})
    controls.append(expect_rejection('negative_inequality_dual', lambda: check_minimum(bad_min, state),
                                     'minimum_row_dual: invalid sparse sign or explicit zero'))
    c = next(c for c in range(len(base['beta'])) if c not in forbidden)
    bad_min = dict(original, critical_multipliers={str(c): '1'})
    controls.append(expect_rejection('critical_multiplier_on_wrong_coordinate', lambda: check_minimum(bad_min, state),
                                     'critical equality multiplier has noncritical support'))
    bad_min = dict(original, critical_multipliers={})
    controls.append(expect_rejection('omitted_signed_critical_equalities', lambda: check_minimum(bad_min, state),
                                     'minimum original-column dual feasibility failure'))
    bad_min = dict(original, row_dual={}, face_multiplier='0', critical_multipliers={})
    controls.append(expect_rejection('infeasible_original_column_dual', lambda: check_minimum(bad_min, state),
                                     'minimum original-column dual feasibility failure'))
    wrong_y = dict(original['row_dual']); wrong_y['0'] = str(F(wrong_y.get('0', '0'))+1)
    bad_min = dict(original, row_dual=wrong_y)
    controls.append(expect_rejection('positive_exact_duality_gap', lambda: check_minimum(bad_min, state),
                                     'minimum exact primal-dual gap is nonzero'))
    bad_min = dict(original, height=str(F(original['height'])+1))
    controls.append(expect_rejection('wrong_claimed_height', lambda: check_minimum(bad_min, state),
                                     'minimum claimed height mismatch'))
    bad_min = dict(original, face_multiplier='0/2')
    controls.append(expect_rejection('noncanonical_face_multiplier', lambda: check_minimum(bad_min, state),
                                     'face_multiplier: noncanonical fraction'))
    omitted_c, omitted_mass = state['first_critical_slot']
    wrong = list(state['critical_weights']); wrong[omitted_c] -= omitted_mass
    controls.append(expect_rejection('dropped_marked_critical_slot',
        lambda: verify_raw_masses(wrong, state['critical_weights']),
        'critical-entry marked or labeled multiplicity mismatch'))
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
        report = check_certificate(certificate, state)
        controls = certificate_controls(certificate, state)
        for name, path in state['paths'].items():
            check_pin(path.read_bytes(), PINS[name])
        print('coverage='+canonical_json(state['derived']['counts']))
        print('references='+canonical_json(state['derived']['references']))
        print('minimum='+canonical_json(report))
        print('negative_controls='+canonical_json(controls))
        print('problem_sha256='+state['derived']['problem_sha256'])
        print('DONE: exact critical-suppressed height minimum value; no lexicographic witness or law adoption')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
