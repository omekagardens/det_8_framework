#!/usr/bin/env python3
"""RI-69: bounded exact universal-top, streak and V=F-h corroboration.

Standard library only; byte-pinned RI-66 is fully reconstructed and its saved
certificate replayed in memory. RI-63 is then explicitly reconstructed once
more because RI-66 does not return its internal row matrix. Accepted sources
and their globals are not patched. No optimizer, download, subprocess or file
write occurs. Only orders of size at most six are constructed; no q6 is used.

The independent geometric checker tests every arbitrary retained subset.
Punctured rectangles are constructed directly, never by creating a forbidden
seven-point rectangle. Finite tests corroborate, but do not replace, the
all-size proof. --witness emits the proposed local certificate; default mode
checks the saved certificate. Alarm and checkpointed peak-RSS limits are 900
seconds and two GiB, not a hard operating-system allocation limit.
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
    'ri66_checker': 'cf54313465da754345406f58a1a60622e51c034d954f8147332c1578cd62fdab',
    'ri66_certificate': '67d6b6706da3100afa89f8c99c6a72b88a6b39c7a1bc628fa69a02e46eca9d01',
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
RI66_WITNESS_SHA256 = 'e667fbade262c694bceb1d40628391b6f3b4acfb2357381c662b31068332680a'
PROBLEM_SHA256 = 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
MAX_SECONDS = 900
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None
FERRERS = {}
PUNCTURED = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    if START_TIME is not None:
        require(time.monotonic()-START_TIME <= MAX_SECONDS, '900-second time envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_RESIDENT_BYTES,
            'two-GiB resident-memory envelope exceeded')
    if stage:
        print('RI69: '+stage, file=sys.stderr, flush=True)


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
            for v, past in enumerate(order)), 'invalid bounded naturally labeled order')


def induced(order, mask):
    require(0 <= mask < (1 << len(order)), 'retained subset outside order')
    kept = bits(mask)
    result = tuple(sum(1 << i for i, u in enumerate(kept) if order[v] & (1 << u)) for v in kept)
    validate_order(result)
    return result


def add_top(order):
    require(len(order) < 6, 'top would exceed size-six cap')
    return order+((1 << len(order))-1,)


def partitions(n, ceiling=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, n if ceiling is None else ceiling), 0, -1):
            for tail in partitions(n-first, first):
                yield (first,)+tail


def cell_order(cells):
    require(len(cells) <= 6, 'cell order exceeds size-six cap')
    result = tuple(sum(1 << u for u, (a, b) in enumerate(cells)
                       if a <= i and b <= j and (a, b) != (i, j)) for i, j in cells)
    validate_order(result)
    return result


def natural_orbit(order):
    found = set()
    for permutation in permutations(range(len(order))):
        relabeled = [0]*len(order)
        for v, past in enumerate(order):
            relabeled[permutation[v]] = sum(1 << permutation[u] for u in bits(past))
        if all(past < (1 << v) for v, past in enumerate(relabeled)):
            found.add(tuple(relabeled))
    return found


def build_catalogues(helper):
    inventory = []
    for n in range(7):
        ferrers, punctured = set(), set()
        for partition in partitions(n):
            cells = tuple((i, j) for i, length in enumerate(partition) for j in range(length))
            ferrers.update(natural_orbit(cell_order(cells)))
        # ab=n+1 is only an integer shape specification. The omitted greatest
        # cell is NEVER placed in an order, including for n=6.
        for a in range(1, n+2):
            if (n+1) % a:
                continue
            b = (n+1)//a
            cells = tuple((i, j) for i in range(a) for j in range(b)
                          if (i, j) != (a-1, b-1))
            punctured.update(natural_orbit(cell_order(cells)))
        require(punctured <= ferrers and ferrers == set(helper['FERRERS_BY_SIZE'][n]),
                'independent cell catalogue differs from accepted Ferrers catalogue')
        FERRERS[n], PUNCTURED[n] = frozenset(ferrers), frozenset(punctured)
        inventory.append(dict(size=n, ferrers_orders=len(ferrers), punctured_orders=len(punctured),
                              ferrers_sha256=digest(sorted(ferrers)),
                              punctured_sha256=digest(sorted(punctured))))
    return inventory


@cache
def height(order):
    validate_order(order)
    levels = []
    for past in order:
        levels.append(1+max((levels[u] for u in bits(past)), default=0))
    return max(levels, default=0)


def retained_profile(order, masks):
    largest_f = largest_r = largest_chain = 0
    for mask in masks:
        selected = induced(order, mask)
        n = len(selected)
        if selected in FERRERS[n]:
            largest_f = max(largest_f, n)
        if selected in PUNCTURED[n]:
            largest_r = max(largest_r, n)
        if sum(p.bit_count() for p in selected) == n*(n-1)//2:
            largest_chain = max(largest_chain, n)
    return largest_f, largest_r, largest_chain


@cache
def profile(order):
    validate_order(order)
    largest_f, largest_r, largest_chain = retained_profile(order, range(1 << len(order)))
    h = height(order)
    require(largest_chain == h and h <= largest_r <= largest_f <= len(order),
            'arbitrary-subset height or retained-size bounds failed')
    return dict(F=largest_f, R=largest_r, h=h, V=largest_f-h, delta=len(order)-largest_f)


def verify_streak(start, k, finish, raising):
    require(k >= 1, 'streak length must be positive')
    a = int(start['R'] == start['F'])
    require(finish['F'] == max(start['F'], start['R']+1, start['h']+k)
            and finish['R'] == max(start['R'], start['h']+k)
            and finish['h'] == start['h']+k, 'universal-top streak formula failed')
    expected_count = min(start['V'], max(0, k-a))
    require(raising == expected_count and finish['V'] == start['V']-raising,
            'full-streak raising count or V charge failed')
    quench = start['V']+a if start['V'] else 0
    require((finish['V'] == 0) == (k >= quench), 'permanent quenching threshold failed')


def birth_role(parent, child, full):
    before, after = profile(parent), profile(child)
    d = after['delta']-before['delta']
    dh = after['h']-before['h']
    dv = after['V']-before['V']
    require(d in (0, 1) and dh in (0, 1) and dv == 1-d-dh,
            'birth increment identity failed')
    recharge = int(not full and d == 0 and dh == 0)
    negative = int(not full and d == 1 and dh == 1)
    full_raising = int(full and d == 1)
    require(not full or (dh == 1 and dv == -d), 'full birth has wrong height or V increment')
    require(dv == recharge-negative-full_raising, 'birth V role partition failed')
    return dict(increment=d, height_increment=dh, V_increment=dv,
                recharge=recharge, proper_negative=negative, full_raising=full_raising)


def verify_path_charge(start_v, end_v, recharge, negative, full_raising):
    require(full_raising == start_v-end_v+recharge-negative
            and full_raising <= start_v+recharge, 'pathwise V charge failed')


def reconstruct_inputs():
    base = Path(__file__).resolve().parent.parent
    folders = dict(ri66='native_growth_terminal_cost_v1', ri63='native_growth_expected_defect_completion_v1',
                   ri41='native_growth_height_normalization_v1')
    paths = {name: base/folders[name[:4]]/('check.py' if name.endswith('checker') else 'CERTIFICATE.json')
             for name in PINS}
    raw = {name: path.read_bytes() for name, path in paths.items()}
    for name in PINS:
        check_pin(raw[name], PINS[name])
    budget('all dependencies byte-pinned; replaying RI-66 unchanged')
    helper66 = runpy.run_path(str(paths['ri66_checker']))
    accepted66 = helper66['reconstruct_witness']()
    require(digest(accepted66) == RI66_WITNESS_SHA256, 'accepted RI-66 witness identity changed')
    helper66['check_certificate'](helper66['load_json'](raw['ri66_certificate']), accepted66)
    helper66['expect_rejection']('missing_component_certificate',
        lambda: helper66['check_certificate'](dict(accepted66, components=accepted66['components'][:-1]), accepted66),
        'saved terminal-cost certificate differs from exact reconstruction')
    budget('RI-66 certificate rechecked; obtaining unmodified RI-63 row interface')
    helper = runpy.run_path(str(paths['ri63_checker']))
    problem = helper['build_problem']()
    require(problem['hashes']['problem_without_self_hash'] == PROBLEM_SHA256,
            'accepted RI-63 problem identity changed')
    proof = helper['check_certificate_core'](helper['load_json'](raw['ri63_certificate']), problem)
    return helper, problem, proof, accepted66, paths, raw


def geometry_checks(helper):
    inventory = build_catalogues(helper)
    orders = {n: helper['parents'](n) for n in range(6)}
    orders[6] = tuple(sorted(p+(s,) for p in orders[5] for s in helper['ideals'](p)))
    require(len(orders[6]) == 4824 and len(set(orders[6])) == 4824,
            'terminal-six geometry coverage changed')
    geometry_manifest, births_manifest, streak_manifest, paths_manifest = [], [], [], []
    birth_totals = {name: 0 for name in ('recharge', 'proper_negative', 'full_raising')}
    subset_count = quench_reached = 0
    for n in range(7):
        budget()
        for order in orders[n]:
            data = profile(order)
            require(data['delta'] == helper['defect'](order),
                    'independent subset Ferrers defect differs from accepted defect')
            subset_count += 1 << n
            geometry_manifest.append([order, data])
            roles = [birth_role(order[:k], order[:k+1], order[k] == (1 << k)-1) for k in range(n)]
            for m in range(n+1):
                recharge = sum(r['recharge'] for r in roles[m:])
                negative = sum(r['proper_negative'] for r in roles[m:])
                full_raising = sum(r['full_raising'] for r in roles[m:])
                verify_path_charge(profile(order[:m])['V'], data['V'], recharge, negative, full_raising)
                paths_manifest.append([order, m, recharge, negative, full_raising])
            if n < 6:
                for part in helper['ideals'](order):
                    role = birth_role(order, order+(part,), part == (1 << n)-1)
                    births_manifest.append([order, part, role])
                    for name in birth_totals:
                        birth_totals[name] += role[name]
                current, raising = order, 0
                for k in range(1, 7-n):
                    child = add_top(current)
                    raising += profile(child)['delta']-profile(current)['delta']
                    verify_streak(data, k, profile(child), raising)
                    quench_reached += int(profile(child)['V'] == 0)
                    streak_manifest.append([order, k, profile(child), raising])
                    current = child
    punctured = (0, 1, 1)
    punctured_streak = [dict(past_masks=punctured, **profile(punctured))]
    current = punctured
    increments = []
    for k in range(3):
        child = add_top(current)
        increments.append(profile(child)['delta']-profile(current)['delta'])
        punctured_streak.append(dict(past_masks=child, **profile(child)))
        current = child
    require(increments == [0, 1, 0], 'punctured-rectangle neutral-raising-neutral witness changed')
    return dict(catalogues=inventory, punctured_streak=punctured_streak,
                punctured_increments=increments, punctured_quenching_time=2,
                counts=dict(orders=sum(map(len, orders.values())),
                    arbitrary_subsets=subset_count, birth_roles=len(births_manifest),
                    one_top_cases=sum(len(orders[n]) for n in range(6)),
                    full_streak_cases=len(streak_manifest), quench_reached_cases=quench_reached,
                    path_cutoff_charges=len(paths_manifest),
                    **birth_totals), manifests=dict(geometry=digest(geometry_manifest),
                    birth_roles=digest(births_manifest), full_streaks=digest(streak_manifest),
                    path_charges=digest(paths_manifest)))


def verify_component_charge(item, terminal, accepted):
    u = F(accepted['U'])
    require(F(item['recharge_weight'])/u == F(terminal['J_num'], terminal['extensions'])
            and F(item['negative_V_weight'])/u == F(terminal['K_num'], terminal['extensions']),
            'terminal recharge or negative-V factorization failed')
    require(terminal['J_num']+terminal['sector_raising_num'] <= terminal['extensions'],
            'recharge and sector-raising roles are not disjoint')


def expected_quantities(problem, coefficients):
    result = {name: F(0) for name in ('G', 'K', 'L', 'Fplus', 'Aplus', 'V_drift', 'defect_drift',
                                               'height_drift', 'expected_V6')}
    for row in problem['rows']:
        p, pi = tuple(row['past_masks']), F(row['pi'])
        selected = row['defect'] > 0 and not row['critical']
        full_q = F(1)
        for slot in row['slots']:
            q = F(slot['u'])*coefficients[slot['component']]
            require(q >= 0, 'observable evaluation has negative proper probability')
            full_q -= q
            role = birth_role(p, p+(slot['past_mask'],), False)
            result['G'] += pi*q*role['recharge']
            result['K'] += pi*q*role['proper_negative']
            result['Aplus'] += pi*q*role['increment']*int(selected)
            result['V_drift'] += pi*q*role['V_increment']
            result['defect_drift'] += pi*q*role['increment']
            result['height_drift'] += pi*q*role['height_increment']
            result['expected_V6'] += pi*q*profile(p+(slot['past_mask'],))['V']
        require(full_q >= 0, 'observable evaluation has negative full complement')
        role = birth_role(p, add_top(p), True)
        result['L'] += pi*full_q*role['full_raising']
        result['Fplus'] += pi*full_q*role['full_raising']*int(selected)
        result['V_drift'] += pi*full_q*role['V_increment']
        result['defect_drift'] += pi*full_q*role['increment']
        result['height_drift'] += pi*full_q
        result['expected_V6'] += pi*full_q*profile(add_top(p))['V']
    require(result['V_drift'] == result['G']-result['K']-result['L'],
            'expected V drift does not match charged birth partition')
    require(result['Fplus'] <= result['L'], 'positive noncritical full sector exceeds whole full charge')
    result['charged_mass'] = result['Aplus']+result['G']
    return result


def verify_mixture(actual, boundary, interior, eta):
    require(eta == F(1, 36) and set(actual) == set(boundary) == set(interior)
            and all(actual[key] == (1-eta)*boundary[key]+eta*interior[key] for key in actual),
            'observable strict-mixture identity failed')


def observable_checks(helper, problem, proof, accepted66):
    width = len(problem['roots'])
    raw_u, raw_g, raw_k = [F(0)]*width, [F(0)]*width, [F(0)]*width
    node_component = {tuple(item['key']): item['component'] for item in problem['nodes']}
    raw_ev, raw_rows, raw_slots = F(0), 0, 0
    raw_manifest = sha256()
    for p in helper['parents'](5):
        budget()
        for record in range(32):
            pi = helper['history_probability'](p, record)
            raw_ev += pi*profile(p)['V']
            raw_rows += 1
            for s in helper['ideals'](p):
                if s == 31:
                    continue
                key = helper['node'](p, s, record)
                c = node_component[key]
                mass = pi*helper['potential'](p, s, record & s)
                role = birth_role(p, p+(s,), False)
                raw_u[c] += mass
                raw_g[c] += mass*role['recharge']
                raw_k[c] += mass*role['proper_negative']
                raw_slots += 1
                raw_manifest.update((canonical_json([p, record, s, c, str(mass), role])+'\n').encode())
    ev = sum((F(row['pi'])*profile(tuple(row['past_masks']))['V'] for row in problem['rows']), F(0))
    require(ev == raw_ev and raw_rows == 11424 and raw_slots == 142944,
            'expected V or complete marked-slot multiplicity mismatch')
    canonical_g, canonical_k = [F(0)]*width, [F(0)]*width
    for row in problem['rows']:
        p, pi = tuple(row['past_masks']), F(row['pi'])
        for slot in row['slots']:
            role = birth_role(p, p+(slot['past_mask'],), False)
            mass = pi*F(slot['u'])
            canonical_g[slot['component']] += mass*role['recharge']
            canonical_k[slot['component']] += mass*role['proper_negative']
    require(canonical_g == raw_g and canonical_k == raw_k,
            'canonical marked rows lost recharge slot multiplicities')
    terminals = []
    for t, old in enumerate(accepted66['terminals']):
        q, j_num, k_num, roles = tuple(old['past_masks']), 0, 0, []
        for old_role in old['roles']:
            v = old_role['vertex']
            p = induced(q, 63 ^ (1 << v))
            d = profile(q)['delta']-profile(p)['delta']
            dh = height(q)-height(p)
            j, k = int(d == 0 and dh == 0), int(d == 1 and dh == 1)
            weight = old_role['extensions']
            j_num += weight*j
            k_num += weight*k
            roles.append(dict(vertex=v, extensions=weight, increment=d, height_increment=dh,
                              recharge=j, proper_negative=k))
        terminals.append(dict(terminal_type=t, past_masks=q, extensions=old['extensions'],
                              J_num=j_num, K_num=k_num,
                              sector_raising_num=old['numerators']['sector_R'], roles=roles))
    components = []
    for c, old in enumerate(accepted66['components']):
        require(c == old['component'] and raw_u[c] == F(old['U']),
                'accepted component order or history-potential denominator changed')
        item = dict(component=c, terminal_type=old['terminal_type'],
                    recharge_weight=str(raw_g[c]), negative_V_weight=str(raw_k[c]))
        verify_component_charge(item, terminals[old['terminal_type']], old)
        components.append(item)
    staircase = cell_order(tuple((i, j) for i, length in enumerate((3, 2, 1)) for j in range(length)))
    staircase_type = min(natural_orbit(staircase))
    staircase_t = next(t for t, item in enumerate(terminals) if tuple(item['past_masks']) == staircase_type)
    stair, old_stair = terminals[staircase_t], accepted66['terminals'][staircase_t]
    require(stair['extensions'] == 16 and sorted(r['extensions'] for r in stair['roles']) == [5, 5, 6]
            and stair['J_num'] == 16 and stair['K_num'] == 0
            and old_stair['numerators']['beta'] == -6
            and all(r['recharge'] == 1 for r in stair['roles']),
            'three-two-one recharge diagnostic changed')
    recharge_diagnostic = dict(partition=[3, 2, 1], terminal_type=staircase_t,
        past_masks=staircase_type, extensions=16, deletion_extensions=[5, 5, 6],
        J_num=16, K_num=0, D_num=-6, recharge_share='1', reduced_cost_ratio='-3/8')
    eta, interior_c = F(problem['eta5']), F(problem['c5'])
    alpha = proof['alpha']
    interior_alpha = [interior_c]*width
    actual_alpha = [(1-eta)*a+eta*interior_c for a in alpha]
    boundary = expected_quantities(problem, alpha)
    interior = expected_quantities(problem, interior_alpha)
    actual = expected_quantities(problem, actual_alpha)
    verify_mixture(actual, boundary, interior, eta)
    for label, quantities, coefficients in (('boundary', boundary, alpha),
            ('interior', interior, interior_alpha), ('actual', actual, actual_alpha)):
        require(quantities['G'] == sum((a*g for a, g in zip(coefficients, raw_g)), F(0))
                and quantities['K'] == sum((a*k for a, k in zip(coefficients, raw_k)), F(0)),
                'terminal weighted component factors differ from row expectations')
        require(quantities['expected_V6'] == ev+quantities['V_drift'],
                'expected V does not telescope at the accepted layer')
    require(boundary['defect_drift'] == F('6650803/108900000'), 'accepted boundary defect optimum changed')
    epsilon = actual['V_drift']-boundary['V_drift']
    require(abs(epsilon) <= 2*eta and boundary['L'] == ev-actual['expected_V6']
            +boundary['G']-boundary['K']+epsilon, 'actual-to-boundary V charge transfer failed')
    encode = lambda row: {key: str(value) for key, value in row.items()}
    return dict(expected_V5=str(ev), eta=str(eta), epsilon=str(epsilon),
                epsilon_absolute_bound=str(2*eta), boundary=encode(boundary),
                interior=encode(interior), actual=encode(actual), terminals=terminals,
                components=components, recharge_diagnostic=recharge_diagnostic,
                counts=dict(raw_marked_rows=raw_rows,
                    proper_labeled_slots=raw_slots, components=width, terminal_types=len(terminals),
                    positive_recharge_components=sum(v > 0 for v in raw_g),
                    positive_negative_V_components=sum(v > 0 for v in raw_k)),
                manifests=dict(raw_marked_role_weights=raw_manifest.hexdigest(),
                    terminal_roles=digest(terminals), component_weights=digest(components)))


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': rejected for an unintended reason')
        return name
    raise RuntimeError(name+': malformed input accepted')


def negative_controls(witness, accepted66, raw):
    controls = [expect_rejection('changed_dependency_bytes',
        lambda: check_pin(raw['ri66_checker']+b' ', PINS['ri66_checker']),
        'accepted dependency byte pin mismatch')]
    start = profile((0, 1, 1))
    finish = dict(profile((0, 1, 1, 7)), F=3)
    controls.append(expect_rejection('wrong_top_F_formula', lambda: verify_streak(start, 1, finish, 0),
                                     'universal-top streak formula failed'))
    controls.append(expect_rejection('missing_first_neutral_streak_step',
        lambda: verify_streak(start, 1, profile((0, 1, 1, 7)), 1),
        'full-streak raising count or V charge failed'))
    join = (0, 0, 3)
    ideal_masks = [mask for mask in range(8) if all(join[v] & mask == join[v] for v in bits(mask))]
    def missing_subset():
        require(retained_profile(join, ideal_masks) == retained_profile(join, range(8)),
                'arbitrary retained subsets were omitted')
    controls.append(expect_rejection('ideal_only_retained_subsets', missing_subset,
                                     'arbitrary retained subsets were omitted'))
    controls.append(expect_rejection('wrong_path_charge', lambda: verify_path_charge(1, 0, 0, 0, 0),
                                     'pathwise V charge failed'))
    observables = witness['observables']
    item = next(c for c in observables['components'] if F(c['recharge_weight']) > 0)
    terminal = observables['terminals'][item['terminal_type']]
    old = accepted66['components'][item['component']]
    bad_old = dict(old, U=str(2*F(old['U'])))
    controls.append(expect_rejection('wrong_component_denominator',
        lambda: verify_component_charge(item, terminal, bad_old),
        'terminal recharge or negative-V factorization failed'))
    bad = dict(item, recharge_weight=str(F(item['recharge_weight'])+1))
    controls.append(expect_rejection('wrong_recharge_role_weight',
        lambda: verify_component_charge(bad, terminal, old),
        'terminal recharge or negative-V factorization failed'))
    parse = lambda row: {key: F(value) for key, value in row.items()}
    actual, boundary, interior = map(parse, (observables['actual'], observables['boundary'], observables['interior']))
    actual['V_drift'] += 1
    controls.append(expect_rejection('corrupt_strict_mixture',
        lambda: verify_mixture(actual, boundary, interior, F(observables['eta'])),
        'observable strict-mixture identity failed'))
    controls.append(expect_rejection('forbidden_seventh_top', lambda: add_top((0, 1, 3, 7, 15, 31)),
                                     'top would exceed size-six cap'))
    controls.append(expect_rejection('duplicate_json_key', lambda: load_json('{"G":0,"G":1}'),
                                     'duplicate JSON object key'))
    return controls


def reconstruct_witness():
    global START_TIME
    START_TIME = time.monotonic()
    helper, problem, proof, accepted66, paths, raw = reconstruct_inputs()
    budget('checking every bounded arbitrary-subset geometry and top streak')
    geometry = geometry_checks(helper)
    budget('checking all marked recharge factors and actual-prefix expectations')
    observables = observable_checks(helper, problem, proof, accepted66)
    witness = dict(schema='ri69-universal-top-drift-v1', order_size_cap=6, growth_parent_size=5,
                   dependencies=PINS, accepted_problem_sha256=PROBLEM_SHA256,
                   accepted_ri66_witness_sha256=RI66_WITNESS_SHA256,
                   accepted_ri66_counts=accepted66['counts'], geometry=geometry,
                   observables=observables, numerically_evaluated_q6=0,
                   scope='finite corroboration; no asymptotic charge or decay theorem')
    witness['negative_controls'] = negative_controls(witness, accepted66, raw)
    for name, path in paths.items():
        check_pin(path.read_bytes(), PINS[name])
    budget('exact finite geometry and expectation checks complete; no later law evaluated')
    return witness


def check_certificate(certificate, witness):
    require(canonical_json(certificate) == canonical_json(witness),
            'saved top-drift certificate differs from exact reconstruction')


def deadline_handler(signum, frame):
    raise RuntimeError('900-second wall-time alarm expired')


def main():
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    try:
        witness = reconstruct_witness()
        if sys.argv[1:] == ['--witness']:
            print(canonical_json(witness))
            return
        certificate = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
        check_certificate(certificate, witness)
        bad = dict(certificate, observables=dict(certificate['observables'], components=[]))
        expect_rejection('missing_component_certificate', lambda: check_certificate(bad, witness),
                         'saved top-drift certificate differs from exact reconstruction')
        print('geometry_coverage='+canonical_json(witness['geometry']['counts']))
        print('marked_coverage='+canonical_json(witness['observables']['counts']))
        print('expectations='+canonical_json({key: witness['observables'][key]
              for key in ('expected_V5', 'epsilon', 'epsilon_absolute_bound', 'boundary', 'actual')}))
        print('negative_controls='+canonical_json(witness['negative_controls']+['missing_component_certificate']))
        print('witness_sha256='+digest(witness))
        print('DONE: exact bounded universal-top charge; no all-size decay claim')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
