#!/usr/bin/env python3
"""RI-66: exact bounded terminal-cost factorization at parent size five.

Standard library only. Byte-pinned accepted RI-63 code is loaded read-only;
its complete reconstruction, canonical certificate and strict-law replay are
rechecked. New work independently aggregates every marked natural history and
labeled proper slot, identifies terminal isomorphism types, and counts linear
extensions by arbitrary maximal deletion. No growth law above parent five,
terminal order above six, optimizer, download, subprocess or file write occurs.

--witness emits the complete proposed certificate to stdout. Ordinary use
checks the adjacent certificate. The finite computation is corroboration of
the written factorization, not proof by enumeration of an all-size theorem.
The 900-second alarm and checkpointed two-GiB peak-RSS envelope are not a hard
operating-system allocation limit.
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
    'ri63_checker': '39d64d11c20675c08e430ceeb335f5b879ffdede1b61ed9fa48f402f21e69b2b',
    'ri63_certificate': 'f55625a686b4c859a8b3e720c80fbabbe9cfa0972cb7a9e78a50d1705833c28b',
    'ri41_certificate': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
PROBLEM_SHA256 = 'dd65ca6cb186946664436e54e8bdc1ef51693e96929cd66af519d00c2a3dbf0c'
MAX_SECONDS = 900
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None
TYPE_CACHE = {}
PERMUTATION_EXTENSIONS = {}
NATURAL_ORBIT_SIZES = {}
FIELDS = ('U', 'R', 'beta', 'sector_U', 'sector_R', 'sector_beta')


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
        print('RI66: ' + stage, file=sys.stderr, flush=True)


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
    require(len(order) <= 6 and all(type(past) is int and 0 <= past < (1 << v)
            and all(order[u] & past == order[u] for u in bits(past))
            for v, past in enumerate(order)), 'invalid bounded naturally labeled order')


def maxima(order):
    ancestors = 0
    for past in order:
        ancestors |= past
    return tuple(bits(((1 << len(order))-1) & ~ancestors))


def delete_vertex(order, vertex):
    require(0 <= vertex < len(order), 'deletion vertex outside order')
    surviving = tuple(v for v in range(len(order)) if v != vertex)
    result = tuple(sum(1 << i for i, u in enumerate(surviving)
                       if order[v] & (1 << u)) for v in surviving)
    validate_order(result)
    return result


@cache
def extension_count(order):
    validate_order(order)
    if not order:
        return 1
    return sum(extension_count(delete_vertex(order, v)) for v in maxima(order))


def order_type(order):
    """Full permutation orbit, retaining every natural labeling of the order.

    Counting accepted permutations counts linear extensions WITH automorphism
    multiplicity. Distinct orbit members are not used as an extension count.
    This routine does not use the accepted marked-local canonicalizer.
    """
    validate_order(order)
    if order in TYPE_CACHE:
        return TYPE_CACHE[order]
    n = len(order)
    require(n in (5, 6), 'isomorphism types requested outside sizes five and six')
    orbit, count = set(), 0
    for permutation in permutations(range(n)):
        relabeled = [0]*n
        for v, past in enumerate(order):
            relabeled[permutation[v]] = sum(1 << permutation[u] for u in bits(past))
        if all(past < (1 << v) for v, past in enumerate(relabeled)):
            count += 1
            orbit.add(tuple(relabeled))
    require(orbit and count == extension_count(order),
            'maximal-deletion count disagrees with permutation extension count')
    canonical = min(orbit)
    for member in orbit:
        require(member not in TYPE_CACHE or TYPE_CACHE[member] == canonical,
                'overlapping terminal isomorphism orbits disagree')
        TYPE_CACHE[member] = canonical
    PERMUTATION_EXTENSIONS[canonical] = count
    NATURAL_ORBIT_SIZES[canonical] = len(orbit)
    return canonical


def reconstruct_accepted():
    base = Path(__file__).resolve().parent.parent
    paths = {
        'ri63_checker': base/'native_growth_expected_defect_completion_v1'/'check.py',
        'ri63_certificate': base/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
        'ri41_certificate': base/'native_growth_height_normalization_v1'/'CERTIFICATE.json',
    }
    raw = {name: path.read_bytes() for name, path in paths.items()}
    for name in PINS:
        check_pin(raw[name], PINS[name])
    budget('all accepted dependencies pinned before read-only helper loading')
    helper = runpy.run_path(str(paths['ri63_checker']))
    problem = helper['build_problem']()
    require(problem['hashes']['problem_without_self_hash'] == PROBLEM_SHA256,
            'accepted complete problem identity changed')
    certificate = helper['load_json'](raw['ri63_certificate'])
    proof = helper['check_certificate_core'](certificate, problem)
    report = helper['certificate_reports'](certificate, problem, proof)
    controls = helper['certificate_controls'](certificate, problem)
    require(report['m5'] == '6650803/108900000'
            and report['certified_positive_lex_stages'] == 69,
            'accepted canonical first-layer result changed')
    return helper, problem, report, controls, paths, raw


def add_slot(target, mass, increment, full_increment, selected):
    contribution = (mass, mass*increment, mass*(increment-full_increment))
    for i, value in enumerate(contribution):
        target[i] += value
        if selected:
            target[i+3] += value


def verify_weight(actual, expected):
    require(actual == expected, 'marked history weight or multiplicity mismatch')


def verify_type(actual, expected):
    require(actual == expected, 'component joins nonisomorphic terminal orders')


def type_record(order, helper):
    delta, critical = helper['defect'], helper['critical']
    total = extension_count(order)
    require(len(maxima(order)) >= 2, 'proper component has a unique-maximal terminal')
    roles = []
    for vertex in maxima(order):
        parent = delete_vertex(order, vertex)
        parent_type = order_type(parent)
        top = parent+(31,)
        require(delta(parent) == helper['direct_subset_defect'](parent)
                and delta(top) == helper['direct_subset_defect'](top),
                'role defect differs from arbitrary-subset minimization')
        roles.append(dict(vertex=vertex, parent_type=parent_type,
                          extensions=extension_count(parent), parent_defect=delta(parent),
                          top_defect=delta(top), parent_critical=critical(parent),
                          selected=delta(parent) > 0 and not critical(parent),
                          increment=delta(order)-delta(parent),
                          reduced_cost=delta(order)-delta(top)))
    result = dict(past_masks=order, defect=delta(order), critical=critical(order),
                  extensions=total, permutation_extensions=PERMUTATION_EXTENSIONS[order],
                  natural_labelings=NATURAL_ORBIT_SIZES[order],
                  automorphisms=total//NATURAL_ORBIT_SIZES[order],
                  roles=roles)
    result['numerators'] = dict(
        U=total,
        R=sum(r['extensions']*r['increment'] for r in roles),
        beta=sum(r['extensions']*r['reduced_cost'] for r in roles),
        sector_U=sum(r['extensions'] for r in roles if r['selected']),
        sector_R=sum(r['extensions']*r['increment'] for r in roles if r['selected']),
        sector_beta=sum(r['extensions']*r['reduced_cost'] for r in roles if r['selected']))
    verify_type_record(result)
    return result


def verify_type_record(item):
    roles, numerator = item['roles'], item['numerators']
    require(item['extensions'] == item['permutation_extensions']
            == sum(r['extensions'] for r in roles), 'terminal extension normalization failed')
    require(item['extensions'] == item['natural_labelings']*item['automorphisms']
            and item['automorphisms'] > 0, 'terminal orbit-automorphism normalization failed')
    expected = dict(U=item['extensions'],
        R=sum(r['extensions']*(item['defect']-r['parent_defect']) for r in roles),
        beta=sum(r['extensions']*(item['defect']-r['top_defect']) for r in roles),
        sector_U=sum(r['extensions'] for r in roles if r['selected']),
        sector_R=sum(r['extensions']*(item['defect']-r['parent_defect'])
                     for r in roles if r['selected']),
        sector_beta=sum(r['extensions']*(item['defect']-r['top_defect'])
                        for r in roles if r['selected']))
    require(numerator == expected, 'terminal deletion-role numerator mismatch')


def verify_factorization(item, terminal):
    values = {name: F(item[name]) for name in FIELDS}
    require(values['U'] > 0, 'component has nonpositive history-potential mass')
    for name in FIELDS:
        require(values[name]/values['U']
                == F(terminal['numerators'][name], terminal['extensions']),
                'component terminal-cost factorization failed: ' + name)
    for field, numerator in (('conditional_sector_R', 'sector_R'),
                             ('conditional_sector_beta', 'sector_beta')):
        expected = (str(F(terminal['numerators'][numerator], terminal['numerators']['sector_U']))
                    if terminal['numerators']['sector_U'] else None)
        require(item[field] == expected, 'conditional sector factorization failed')


def verify_fiber_mass(mass, extensions, fiber_sum, automorphisms, fair_factor=64):
    require(mass > 0 and fiber_sum > 0 and automorphisms > 0
            and mass == extensions*fiber_sum/(fair_factor*automorphisms),
            'marked fiber mass does not factor through terminal extensions')
    return fiber_sum/(fair_factor*automorphisms)


def reconstruct_witness():
    global START_TIME
    START_TIME = time.monotonic()
    helper, problem, report, accepted_controls, paths, raw = reconstruct_accepted()
    budget('accepted layer rechecked; aggregating every raw marked proper slot')
    width = len(problem['roots'])
    component = {tuple(item['key']): item['component'] for item in problem['nodes']}
    node_u = {tuple(item['key']): F(item['u']) for item in problem['nodes']}
    canonical_rows = {tuple(item['key']): item for item in problem['rows']}
    sums = [[F(0)]*6 for _ in range(width)]
    quotient_sums = [[F(0)]*6 for _ in range(width)]
    role_masses = [{} for _ in range(width)]
    terminal_by_component, terminal_by_node = {}, {}
    weights, multiplicities = {}, {}
    raw_rows = raw_slots = 0
    raw_digest = sha256()
    for parent in helper['parents'](5):
        budget()
        parent_type = order_type(parent)
        delta = helper['defect'](parent)
        full_increment = helper['defect'](parent+(31,))-delta
        selected = delta > 0 and not helper['critical'](parent)
        terminal_types = {s: order_type(parent+(s,))
                          for s in helper['ideals'](parent) if s != 31}
        for record in range(32):
            history = helper['history_probability'](parent, record)
            row_key = helper['row_key'](parent, record)
            weights[row_key] = weights.get(row_key, F(0))+history
            multiplicities[row_key] = multiplicities.get(row_key, 0)+1
            raw_rows += 1
            for part, terminal_type in terminal_types.items():
                key = helper['node'](parent, part, record)
                c = component[key]
                u = helper['potential'](parent, part, record & part)
                require(u == node_u[key], 'raw local potential differs from accepted node')
                increment = helper['defect'](parent+(part,))-delta
                verify_type(terminal_type, terminal_by_component.setdefault(c, terminal_type))
                verify_type(terminal_type, terminal_by_node.setdefault(key, terminal_type))
                mass = history*u
                add_slot(sums[c], mass, increment, full_increment, selected)
                role_masses[c][parent_type] = role_masses[c].get(parent_type, F(0))+mass
                raw_digest.update((canonical_json([parent, record, part, key, c,
                    str(history), str(u), increment, full_increment, selected, terminal_type])+'\n').encode())
                raw_slots += 1
    require(set(terminal_by_node) == set(component) and set(terminal_by_component) == set(range(width)),
            'terminal typing did not cover every accepted node and component')
    require(set(weights) == set(canonical_rows), 'raw histories did not cover every marked row class')
    for key, item in canonical_rows.items():
        verify_weight((weights[key], multiplicities[key]),
                      (F(item['pi']), item['natural_history_multiplicity']))
        selected = item['defect'] > 0 and not item['critical']
        for slot in item['slots']:
            add_slot(quotient_sums[slot['component']], F(item['pi'])*F(slot['u']),
                     slot['increment'], item['full_increment'], selected)
    require(sums == quotient_sums, 'canonical marked-row aggregation lost slot multiplicities')
    require([str(values[2]) for values in sums] == problem['beta'],
            'raw weighted reduced costs differ from accepted affine objective')
    budget('raw and quotient masses agree; checking all terminal deletion-role factors')
    terminal_orders = sorted(set(terminal_by_component.values()))
    terminals = [type_record(order, helper) for order in terminal_orders]
    type_ids = {order: i for i, order in enumerate(terminal_orders)}
    fiber_sums, fiber_counts, first_phi = [F(0)]*width, [0]*width, {}
    fiber_digest = sha256()
    marked_terminal_roles = 0
    for t, terminal in enumerate(terminals):
        order = terminal_orders[t]
        for record in range(64):
            found_component = common_phi = None
            for vertex in maxima(order):
                parent = delete_vertex(order, vertex)
                surviving = tuple(v for v in range(6) if v != vertex)
                part = sum(1 << i for i, v in enumerate(surviving)
                           if order[vertex] & (1 << v))
                parent_record = sum(1 << i for i, v in enumerate(surviving)
                                    if record & (1 << v))
                key = helper['node'](parent, part, parent_record)
                c = component[key]
                phi = 32*helper['history_probability'](parent, parent_record)*node_u[key]
                require(found_component is None or found_component == c,
                        'complete terminal marking crosses component fibers')
                require(common_phi is None or common_phi == phi,
                        'complete terminal marking changes deletion-role path product')
                require(terminal_by_component[c] == order,
                        'terminal record fiber has incorrect unmarked type')
                found_component, common_phi = c, phi
                marked_terminal_roles += 1
            fiber_sums[found_component] += common_phi
            fiber_counts[found_component] += 1
            first_phi.setdefault(found_component, common_phi)
            fiber_digest.update((canonical_json([t, record, found_component, str(common_phi)])+'\n').encode())
    components, role_manifest = [], []
    for c in range(width):
        t = type_ids[terminal_by_component[c]]
        terminal = terminals[t]
        require(fiber_counts[c] > 0, 'component has an empty complete-mark fiber')
        fiber_k = verify_fiber_mass(sums[c][0], terminal['extensions'],
                                    fiber_sums[c], terminal['automorphisms'])
        item = dict(component=c, root=problem['roots'][c], terminal_type=t,
                    terminal_mark_fiber_size=fiber_counts[c], K=str(fiber_k),
                    conditional_sector_R=(str(sums[c][4]/sums[c][3]) if sums[c][3] else None),
                    conditional_sector_beta=(str(sums[c][5]/sums[c][3]) if sums[c][3] else None),
                    **{name: str(sums[c][i]) for i, name in enumerate(FIELDS)})
        verify_factorization(item, terminal)
        expected_roles = {}
        for role in terminal['roles']:
            key = tuple(role['parent_type'])
            expected_roles[key] = expected_roles.get(key, 0)+role['extensions']
        require(set(role_masses[c]) == set(expected_roles),
                'component omits a maximal-deletion parent type')
        for parent_type, numerator in sorted(expected_roles.items()):
            require(role_masses[c][parent_type]/sums[c][0] == F(numerator, terminal['extensions']),
                    'marked component has incorrect maximal-deletion role weight')
            role_manifest.append([c, parent_type, str(role_masses[c][parent_type]), numerator])
        components.append(item)
    grouped = [dict(terminal_type=t, components=[item['component'] for item in components
                                                if item['terminal_type'] == t])
               for t in range(len(terminals))]
    hook = problem['hook']['component']
    hook_type = components[hook]['terminal_type']
    require(order_type((0, 1, 3, 7, 1, 0)) == terminal_orders[hook_type],
            'accepted hook component has wrong unmarked terminal')
    hook_report = dict(component=hook, terminal_type=hook_type,
        U=components[hook]['U'], R_over_U=str(sums[hook][1]/sums[hook][0]),
        beta_over_U=str(sums[hook][2]/sums[hook][0]),
        sector_U_over_U=str(sums[hook][3]/sums[hook][0]),
        sector_R_over_U=str(sums[hook][4]/sums[hook][0]),
        conditional_sector_R=components[hook]['conditional_sector_R'],
        conditional_sector_beta=components[hook]['conditional_sector_beta'])
    counts = dict(raw_marked_rows=raw_rows, proper_labeled_slots=raw_slots,
                  canonical_marked_rows=len(canonical_rows), proper_local_nodes=len(component),
                  proper_components=width, proper_terminal_types=len(terminals),
                  typed_natural_terminal_orders=sum(len(p) == 6 for p in TYPE_CACHE),
                  maximal_deletion_roles=sum(len(t['roles']) for t in terminals),
                  complete_marked_terminal_types=64*len(terminals),
                  complete_marked_deletion_roles=marked_terminal_roles,
                  component_parent_type_roles=len(role_manifest),
                  component_factor_equalities=6*width,
                  positive_sector_mass_components=sum(values[3] > 0 for values in sums),
                  positive_sector_raising_components=sum(values[4] > 0 for values in sums),
                  negative_beta_components=sum(values[2] < 0 for values in sums),
                  zero_beta_components=sum(values[2] == 0 for values in sums),
                  positive_beta_components=sum(values[2] > 0 for values in sums),
                  numerically_evaluated_q6=0, terminal_seven_orders=0)
    require((raw_rows, raw_slots, len(canonical_rows), len(component), width)
            == (11424, 142944, 1490, 2961, 798), 'accepted finite coverage changed')
    witness = dict(schema='ri66-terminal-cost-factorization-v1', parent_size=5, terminal_size=6,
                   sector='positive parent defect and noncritical parent', dependencies=PINS,
                   accepted_problem_sha256=PROBLEM_SHA256, accepted_counts=problem['counts'],
                   accepted_certificate_report_sha256=digest(report),
                   accepted_certificate_controls=accepted_controls, counts=counts,
                   terminals=terminals, components=components, groups=grouped, hook=hook_report,
                   manifests=dict(raw_marked_slots=raw_digest.hexdigest(),
                       terminal_types=digest(terminals), component_masses=digest(components),
                       component_deletion_roles=digest(role_manifest),
                       complete_terminal_mark_fibers=fiber_digest.hexdigest(),
                       local_node_terminal_types=digest([[key, type_ids[terminal_by_node[key]]]
                                                         for key in sorted(component)])))
    witness['negative_controls'] = negative_controls(witness, raw, weights, multiplicities,
                                                    canonical_rows, fiber_sums, first_phi)
    for name, path in paths.items():
        check_pin(path.read_bytes(), PINS[name])
    budget('all finite component and sector factorizations verified; no later law evaluated')
    return witness


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': rejected for an unintended reason')
        return name
    raise RuntimeError(name+': malformed input accepted')


def negative_controls(witness, raw, weights, multiplicities, rows, fiber_sums, first_phi):
    controls = [expect_rejection('changed_dependency_bytes',
        lambda: check_pin(raw['ri63_checker']+b' ', PINS['ri63_checker']),
        'accepted dependency byte pin mismatch')]
    key = next(k for k in rows if multiplicities[k] > 1)
    expected = (F(rows[key]['pi']), rows[key]['natural_history_multiplicity'])
    controls.append(expect_rejection('wrong_marked_history_weight',
        lambda: verify_weight((weights[key]+F(1, 2), multiplicities[key]), expected),
        'marked history weight or multiplicity mismatch'))
    controls.append(expect_rejection('dropped_natural_label_multiplicity',
        lambda: verify_weight((weights[key]/multiplicities[key], 1), expected),
        'marked history weight or multiplicity mismatch'))
    terminal = witness['terminals'][0]
    bad = load_json(canonical_json(terminal))
    bad['extensions'] += 1
    controls.append(expect_rejection('wrong_linear_extension_count', lambda: verify_type_record(bad),
                                     'terminal extension normalization failed'))
    bad = load_json(canonical_json(terminal))
    bad['roles'][0]['top_defect'] += 1
    controls.append(expect_rejection('wrong_full_top_defect', lambda: verify_type_record(bad),
                                     'terminal deletion-role numerator mismatch'))
    item = next(c for c in witness['components'] if F(c['R']) > 0)
    terminal = witness['terminals'][item['terminal_type']]
    bad = dict(item, beta=str(F(item['beta'])+1))
    controls.append(expect_rejection('wrong_global_reduced_cost', lambda: verify_factorization(bad, terminal),
                                     'component terminal-cost factorization failed: beta'))
    bad = dict(item, sector_U=str(F(item['sector_U'])+1))
    controls.append(expect_rejection('wrong_sector_weight', lambda: verify_factorization(bad, terminal),
                                     'component terminal-cost factorization failed: sector_U'))
    c, mass, e, aut = item['component'], F(item['U']), terminal['extensions'], terminal['automorphisms']
    reason = 'marked fiber mass does not factor through terminal extensions'
    controls.append(expect_rejection('wrong_automorphism_factor',
        lambda: verify_fiber_mass(mass, e, fiber_sums[c], aut+1), reason))
    controls.append(expect_rejection('omitted_newborn_fair_bit',
        lambda: verify_fiber_mass(mass, e, fiber_sums[c], aut, 32), reason))
    controls.append(expect_rejection('missing_complete_terminal_mark',
        lambda: verify_fiber_mass(mass, e, fiber_sums[c]-first_phi[c], aut), reason))
    first, second = witness['terminals'][:2]
    controls.append(expect_rejection('merged_nonisomorphic_terminals',
        lambda: verify_type(first['past_masks'], second['past_masks']),
        'component joins nonisomorphic terminal orders'))
    controls.append(expect_rejection('duplicate_json_key', lambda: load_json('{"U":0,"U":1}'),
                                     'duplicate JSON object key'))
    controls.append(expect_rejection('terminal_above_cap', lambda: validate_order((0,)*7),
                                     'invalid bounded naturally labeled order'))
    return controls


def check_certificate(certificate, witness):
    require(canonical_json(certificate) == canonical_json(witness),
            'saved terminal-cost certificate differs from exact reconstruction')


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
        bad = dict(certificate, components=certificate['components'][:-1])
        expect_rejection('missing_component_certificate', lambda: check_certificate(bad, witness),
                         'saved terminal-cost certificate differs from exact reconstruction')
        print('coverage='+canonical_json(witness['counts']))
        print('hook='+canonical_json(witness['hook']))
        print('negative_controls='+canonical_json(witness['negative_controls']+['missing_component_certificate']))
        print('witness_sha256='+digest(witness))
        print('DONE: exact terminal and sector cost factors at parent five; no all-size inference from tests')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
