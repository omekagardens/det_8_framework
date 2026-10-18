#!/usr/bin/env python3
"""RI-74: bounded exact corroboration of a zero-allowed Ferrers graft.

No optimizer, downloads, subprocesses or file writes. Byte-pinned RI-63 is
replayed as a read-only dependency, including its canonical and actual strict
parent-five certificate. New pure Ferrers orders stop at six; selected graft
orders stop at nine. No exhaustive higher-layer inventory is constructed.
The scalar law is a boundary benchmark, not an adopted strict-positive law.
--witness prints deterministic certificate data; default verifies the saved
CERTIFICATE.json. The 900-second alarm and checkpointed two-GiB peak RSS are
an audit envelope, not a hard operating-system allocator cap.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from math import factorial
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
CORES = ((0, 1, 3, 7, 15, 31), (0, 0, 0, 0, 0, 0), (0, 1, 1, 7, 7, 7))
MAX_SECONDS = 900
MAX_BYTES = 2*1024**3
START = None
B = {}
HELPER = None
Q5 = {}
DEPENDENCY_PATHS = {}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS,
            '900-second verification envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_BYTES,
            'two-GiB resident-memory envelope exceeded')
    if stage:
        print('RI74: '+stage, file=sys.stderr, flush=True)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def digest(value):
    return sha256(canonical(value).encode()).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def load_json(text):
    def bad(value):
        raise RuntimeError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=bad)


def check_pin(raw, expected):
    require(sha256(raw).hexdigest() == expected, 'accepted dependency byte pin mismatch')


def bits(mask):
    return tuple(v for v in range(mask.bit_length()) if mask & (1 << v))


@cache
def validate(order):
    n = len(order)
    require(n <= 9 and all(type(p) is int and 0 <= p < (1 << n)
            and not p & (1 << v) and all(order[u] & p == order[u] for u in bits(p))
            for v, p in enumerate(order)), 'invalid bounded transitive order')
    return True


@cache
def ideals(order):
    validate(order)
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


def induced(order, keep):
    kept = bits(keep)
    return tuple(sum(1 << i for i, u in enumerate(kept) if order[v] & (1 << u))
                 for v in kept)


def transport(mask, permutation):
    return sum(1 << permutation[v] for v in bits(mask))


def relabel(order, permutation):
    require(sorted(permutation) == list(range(len(order))), 'invalid vertex permutation')
    result = [0]*len(order)
    for v, past in enumerate(order):
        result[permutation[v]] = transport(past, permutation)
    return tuple(result)


def maxima(order):
    pasts = 0
    for past in order:
        pasts |= past
    return bits(((1 << len(order))-1) & ~pasts)


@cache
def extensions(order):
    validate(order)
    require(len(order) <= 6, 'extension count outside size-six domain')
    if not order:
        return 1
    full = (1 << len(order))-1
    return sum(extensions(induced(order, full ^ (1 << v))) for v in maxima(order))


def ideal_extensions(order):
    """Independent forward ideal dynamic program; no maximal recursion."""
    counts = {0: 1}
    full = (1 << len(order))-1
    for size in range(len(order)):
        for past in tuple(s for s in counts if s.bit_count() == size):
            for v in range(len(order)):
                if not past & (1 << v) and order[v] & past == order[v]:
                    child = past | (1 << v)
                    counts[child] = counts.get(child, 0)+counts[past]
    return counts[full]


def partitions(n, ceiling=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, n if ceiling is None else ceiling), 0, -1):
            for tail in partitions(n-first, first):
                yield (first,)+tail


def diagram(partition):
    cells = tuple((i, j) for i, length in enumerate(partition) for j in range(length))
    return tuple(sum(1 << u for u, (a, b) in enumerate(cells)
                     if a <= i and b <= j and (a, b) != (i, j)) for i, j in cells)


@cache
def natural_orders(n):
    require(0 <= n <= 6, 'exhaustive natural inventory outside size-six cap')
    if n == 0:
        return ((),)
    return tuple(sorted(p+(s,) for p in natural_orders(n-1) for s in ideals(p)))


def verify_weight_data(order, data):
    require(isinstance(data, dict) and set(data) == {'b', 'e', 'factorial'},
            'weight data schema mismatch')
    require(data['b'] == B[len(order)].get(order, 0), 'oriented embedding multiplicity lost')
    require(data['e'] == ideal_extensions(order), 'extension count corrupted')
    require(data['factorial'] == factorial(len(order)), 'factorial weight corrupted')
    return F(data['b']*data['e'], data['factorial'])


@cache
def weight(order):
    validate(order)
    require(len(order) <= 6, 'pure weight outside size-six domain')
    return verify_weight_data(order, dict(b=B[len(order)].get(order, 0),
                                         e=extensions(order), factorial=factorial(len(order))))


def verify_normalized_row(order, row, reason):
    require(isinstance(row, dict) and set(row) == set(ideals(order))
            and all(isinstance(q, F) and q >= 0 for q in row.values())
            and sum(row.values(), F(0)) == 1, reason)


def verify_row_equal(actual, expected, reason):
    require(actual == expected, reason)


@cache
def pure_row(order):
    require(len(order) <= 5 and weight(order) > 0, 'pure parent is outside Ferrers support')
    result = {s: weight(order+(s,))/weight(order) for s in ideals(order)}
    verify_normalized_row(order, result, 'individual-ideal Ferrers row fails normalization')
    return result


def pure_q(order, part):
    require(part in ideals(order), 'precursor is not an ideal')
    return pure_row(order)[part]


def pure_product(order, first, second):
    value = pure_q(order, first)
    # A zero first leg never requests a row or divides by the zero child weight.
    return F(0) if not value else value*pure_q(order+(first,), second)


def rebuild_prefix():
    global HELPER, Q5, DEPENDENCY_PATHS
    directory = Path(__file__).resolve().parent.parent
    paths = dict(ri63_checker=directory/'native_growth_expected_defect_completion_v1'/'check.py',
                 ri63_certificate=directory/'native_growth_expected_defect_completion_v1'/'CERTIFICATE.json',
                 ri41_certificate=directory/'native_growth_height_normalization_v1'/'CERTIFICATE.json')
    raw = {key: path.read_bytes() for key, path in paths.items()}
    DEPENDENCY_PATHS = paths
    for key in PINS:
        check_pin(raw[key], PINS[key])
    budget('all accepted files pinned; replaying unchanged RI-63 canonical/strict proof')
    HELPER = runpy.run_path(str(paths['ri63_checker']))
    problem = HELPER['build_problem']()
    certificate = HELPER['load_json'](raw['ri63_certificate'])
    proof = HELPER['check_certificate_core'](certificate, problem)
    report = HELPER['certificate_reports'](certificate, problem, proof)
    controls = HELPER['certificate_controls'](certificate, problem)
    eta, c = F(problem['eta5']), F(problem['c5'])
    Q5 = {tuple(item['key']): F(item['u'])*((1-eta)*proof['alpha'][item['component']]+eta*c)
          for item in problem['nodes']}
    for n in range(6):
        require(natural_orders(n) == HELPER['parents'](n), 'independent natural prefix inventory mismatch')
    require(set(natural_orders(6)) == HELPER['independent_relation_inventory'](6),
            'independent terminal-six relation inventory mismatch')
    return dict(problem_sha256=problem['hashes']['problem_without_self_hash'],
                inherited_controls=controls, canonical_lex_stages=len(proof['stage_reports']),
                actual_probability_manifest_sha256=report['actual_probability_manifest_sha256'])


@cache
def prefix_row(order, record):
    n = len(order)
    require(n < 6 and type(record) is int and 0 <= record < (1 << n),
            'prefix lookup outside held marked domain')
    validate(order)
    # This is only an evaluation relabeling of an already equivariant held law.
    # It never selects or tags a graft core.
    selected, labels = 0, []
    while len(labels) < n:
        v = next(v for v in range(n) if not selected & (1 << v)
                 and order[v] & selected == order[v])
        labels.append(v)
        selected |= 1 << v
    permutation = tuple(labels.index(v) for v in range(n))
    natural = relabel(order, permutation)
    r = transport(record, permutation)
    if n < 5:
        q = HELPER['row'](natural, r)
    else:
        q = {s: Q5[HELPER['node'](natural, s, r)] for s in HELPER['ideals'](natural) if s != 31}
        q[31] = 1-sum(q.values(), F(0))
    return {s: q[transport(s, permutation)] for s in ideals(order)}


@cache
def core(order):
    validate(order)
    require(6 < len(order) <= 9, 'graft recognition outside selected domain')
    candidates = tuple(s for s in ideals(order) if s.bit_count() == 6)
    if len(candidates) != 1:
        return None
    k = candidates[0]
    remainder = ((1 << len(order))-1) ^ k
    if not all(order[v] & k == k for v in bits(remainder)):
        return None
    suffix = induced(order, remainder)
    if not B[len(suffix)].get(suffix, 0):
        return None
    return k, suffix, bits(remainder)


def verify_core_claim(order, mask):
    found = core(order)
    require(found is not None and found[0] == mask, 'intrinsic core claim mismatch')
    return found


@cache
def boundary_row(order):
    n = len(order)
    validate(order)
    require(6 <= n <= 8, 'boundary row outside selected domain')
    full = (1 << n)-1
    result = {s: F(0) for s in ideals(order)}
    found = core(order) if n > 6 else None
    if found is None:
        result[full] = F(1)
    else:
        k, suffix, vertices = found
        for s, q in pure_row(suffix).items():
            lifted = k | sum(1 << vertices[v] for v in bits(s))
            require(lifted in result, 'suffix lift is not a parent ideal')
            result[lifted] = q
    verify_normalized_row(order, result, 'graft row fails normalization')
    return result


def graft_row(order, record):
    n = len(order)
    require(n <= 8 and type(record) is int and 0 <= record < (1 << n),
            'graft row outside selected marked domain')
    return prefix_row(order, record) if n < 6 else boundary_row(order)


def ordinal(core_order, suffix):
    full = (1 << len(core_order))-1
    return core_order+tuple(full | (past << len(core_order)) for past in suffix)


def verify_pushforward_class(item):
    require(item['natural_histories']*item['automorphisms'] == item['linear_extensions'],
            'natural-history orbit multiplicity mismatch')
    require(F(item['labeled_history_mass']) == F(item['diagram_mass']),
            'unmarked-class Plancherel pushforward mismatch')


def pure_checks():
    inventory, diagram_rows, class_rows = [], [], []
    for n in range(7):
        budget()
        counts, classes, class_of = {}, {}, {}
        for partition in partitions(n):
            p = diagram(partition)
            images = {}
            for permutation in permutations(range(n)):
                q = relabel(p, permutation)
                counts[q] = counts.get(q, 0)+1
                images[q] = images.get(q, 0)+1
            e = extensions(p)
            require(e == ideal_extensions(p), 'independent diagram extension count mismatch')
            key, aut = min(images), images[p]
            require(len(images)*aut == factorial(n), 'diagram isomorphism orbit-stabilizer mismatch')
            for q in images:
                require(q not in class_of or class_of[q] == key, 'canonical diagram classes overlap')
                class_of[q] = key
            if key not in classes:
                classes[key] = dict(e=e, aut=aut, diagrams=[], mass=F(0))
            require((classes[key]['e'], classes[key]['aut']) == (e, aut),
                    'isomorphic diagrams disagree on extension or automorphism count')
            classes[key]['diagrams'].append(partition)
            classes[key]['mass'] += F(e*e, factorial(n))
            diagram_rows.append([partition, e, str(F(e*e, factorial(n)))])
        B[n] = counts
        natural = tuple(p for p in natural_orders(n) if p in counts)
        require(set(natural) == set(HELPER['FERRERS_BY_SIZE'][n]),
                'independent isomorphism catalogue disagrees with accepted membership')
        require(sum((weight(p) for p in natural), F(0)) == 1,
                'natural Ferrers histories fail normalization')
        require(sum((F(extensions(diagram(part))**2, factorial(n)) for part in partitions(n)), F(0)) == 1,
                'diagram Plancherel marginal fails normalization')
        for key, data in sorted(classes.items()):
            representatives = tuple(p for p in natural if class_of[p] == key)
            item = dict(size=n, canonical_order=key, oriented_diagrams=data['diagrams'],
                        natural_histories=len(representatives), automorphisms=data['aut'],
                        linear_extensions=data['e'],
                        labeled_history_mass=str(sum((weight(p) for p in representatives), F(0))),
                        diagram_mass=str(data['mass']))
            verify_pushforward_class(item)
            class_rows.append(item)
        for p in natural_orders(n):
            require(extensions(p) == ideal_extensions(p), 'independent all-order extension count mismatch')
        inventory.append(dict(size=n, natural_orders=len(natural_orders(n)),
                              ferrers_natural_orders=len(natural), arbitrary_labeled_ferrers=len(counts),
                              natural_isomorphisms=sum(counts[p] for p in natural),
                              total_isomorphisms=sum(counts.values()),
                              b_manifest_sha256=digest([[p, b] for p, b in sorted(counts.items())])))
    rows, diamonds = [], []
    positive = zero = equal = 0
    for n in range(6):
        for p in natural_orders(n):
            if not B[n].get(p):
                continue
            q = pure_row(p)
            rows.append([p, [[s, str(v)] for s, v in q.items()]])
            if n <= 4:
                for first in ideals(p):
                    for second in ideals(p):
                        left, right = pure_product(p, first, second), pure_product(p, second, first)
                        require(left == right, 'pure positive/zero sibling diamond failure')
                        # Both terminal presentations differ only by swapping newborn vertices.
                        end = p+(first, second)
                        swap = tuple(range(n))+(n+1, n)
                        require(relabel(end, swap) == p+(second, first), 'terminal newborn transport failure')
                        require(left == (weight(end)/weight(p) if weight(end) else 0),
                                'pure diamond does not telescope to terminal weight')
                        diamonds.append([p, first, second, str(left)])
                        positive += int(left > 0)
                        zero += int(left == 0)
                        equal += int(first == second)
    hand = {name: [[s, str(v)] for s, v in pure_row(p).items()]
            for name, p in (('singleton', (0,)), ('chain_two', (0, 1)), ('fork_three', (0, 1, 1)))}
    require(pure_row((0,))[1] == 1 and pure_row((0,))[0] == 0,
            'singleton-to-chain multiplicity failure')
    require(pure_row((0, 1))[3] == F(1, 3) and pure_row((0, 1))[1] == F(2, 3),
            'chain-to-fork multiplicity failure')
    require(pure_row((0, 1, 1))[7] == F(1, 4)
            and pure_row((0, 1, 1))[3] == pure_row((0, 1, 1))[5] == F(3, 8),
            'distinct fork-arm multiplicity failure')
    return dict(inventory=inventory, diagram_marginals=diagram_rows, unmarked_classes=class_rows,
                row_count=len(rows), labeled_ideal_slots=sum(len(row[1]) for row in rows),
                row_manifest_sha256=digest(rows), diamond_count=len(diamonds),
                positive_diamonds=positive, zero_diamonds=zero, equal_precursor_diamonds=equal,
                diamond_manifest_sha256=digest(diamonds), hand_examples=hand)


def graft_checks():
    prefix_digest = sha256()
    prefix_rows = prefix_slots = 0
    for n in range(6):
        budget()
        for p in natural_orders(n):
            for r in range(1 << n):
                expected = prefix_row(p, r)
                actual = graft_row(p, r)
                verify_row_equal(actual, expected, 'graft changed held strict-prefix row')
                require(all(q > 0 for q in actual.values()), 'held prefix ceased to be strict')
                prefix_digest.update((canonical([p, r, [[s, str(v)] for s, v in actual.items()]])+'\n').encode())
                prefix_rows += 1
                prefix_slots += len(actual)
    examples, rows, deletions = [], [], []
    for k in CORES:
        for n in range(4):
            for suffix in natural_orders(n):
                if not B[n].get(suffix):
                    continue
                p = ordinal(k, suffix)
                if n:
                    require(verify_core_claim(p, 63) == (63, suffix, tuple(range(6, 6+n))),
                            'selected ordinal sum has no intrinsic core')
                    for v in maxima(p):
                        smaller = induced(p, ((1 << len(p))-1) ^ (1 << v))
                        require(len(smaller) == 6 or core(smaller) is not None,
                                'maximal deletion leaves selected graft family')
                        deletions.append([p, v, smaller])
                    permutation = tuple(reversed(range(len(p))))
                    shuffled = relabel(p, permutation)
                    found = verify_core_claim(shuffled, transport(63, permutation))
                    require(found[0] != 63, 'chronological-core relabeling test is vacuous')
                examples.append([p, n, core(p)[0] if n else None])
                if n <= 2:
                    q = graft_row(p, 0)
                    require(q == graft_row(p, (1 << len(p))-1), 'post-cutoff row reads records')
                    expected = ({s: F(int(s == 63)) for s in ideals(p)} if not n else
                                {s: (pure_row(suffix).get(s >> 6, F(0)) if s & 63 == 63 else F(0))
                                 for s in ideals(p)})
                    verify_row_equal(q, expected, 'selected graft suffix probability mismatch')
                    permutation = tuple(reversed(range(len(p))))
                    shuffled_q = graft_row(relabel(p, permutation), 0)
                    require(shuffled_q == {transport(s, permutation): value for s, value in q.items()},
                            'graft row fails transported-ideal equivariance')
                    rows.append([p, [[s, str(v)] for s, v in q.items()]])
    off = ((0,)*7, (0, 1, 3, 7, 15, 31, 0), ordinal(CORES[0], (0, 0)))
    for p in off:
        require(core(p) is None, 'off-family order incorrectly recognized')
        require(graft_row(p, 0) == {s: F(int(s == (1 << len(p))-1)) for s in ideals(p)},
                'off-family fallback is not full-only')
    # Complete ordered pairs on declared bases only; all old records and all
    # four newborn records are retained, including equal/full precursor cases.
    bases = sorted(set(k[:-1] for k in CORES) | set(CORES)
                   | {ordinal(k, (0,)) for k in CORES} | {off[0], off[1]})
    cases = zeros = positives = equal = full = 0
    diamond_digest = sha256()
    for p in bases:
        budget()
        n = len(p)
        old_rows = {r: graft_row(p, r) for r in range(1 << n)}
        for first in ideals(p):
            for second in ideals(p):
                for r, old in old_rows.items():
                    for b in (0, 1):
                        for h in (0, 1):
                            left = old[first]*graft_row(p+(first,), r | (b << n))[second]
                            right = old[second]*graft_row(p+(second,), r | (h << n))[first]
                            require(left == right, 'selected cutoff/off-family graft diamond failure')
                            cases += 1
                            zeros += int(left == 0)
                            positives += int(left > 0)
                            equal += int(first == second)
                            full += int(first == (1 << n)-1 or second == (1 << n)-1)
                            diamond_digest.update((canonical([p, first, second, r, b, h, str(left)])+'\n').encode())
    return dict(prefix_rows=prefix_rows, prefix_labeled_slots=prefix_slots,
                prefix_manifest_sha256=prefix_digest.hexdigest(), selected_cores=CORES,
                selected_states=examples, selected_rows=rows, selected_maximal_deletions=len(deletions),
                deletion_manifest_sha256=digest(deletions), off_family_states=off,
                diamond_bases=bases, raw_marked_diamonds=cases, zero_diamonds=zeros,
                positive_diamonds=positives, equal_precursor_diamonds=equal,
                full_precursor_diamonds=full, diamond_manifest_sha256=diamond_digest.hexdigest())


def expect_rejection(name, function, message):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == message, name+': wrong rejection reason')
        return name
    raise RuntimeError(name+': malformed candidate accepted')


def verify_certificate(certificate, expected):
    require(isinstance(certificate, dict) and set(certificate) == set(expected)
            and certificate.get('schema') == expected['schema'], 'certificate schema mismatch')
    require(certificate['dependencies'] == PINS, 'certificate dependency identities changed')
    require(canonical(certificate) == canonical(expected), 'certificate finite witness mismatch')


def controls(witness):
    result = []
    def bad_weight(name, order, field, value, reason):
        data = dict(b=B[len(order)][order], e=extensions(order), factorial=factorial(len(order)))
        data[field] = value
        result.append(expect_rejection(name, lambda: verify_weight_data(order, data), reason))
    bad_weight('lost_oriented_diagram_multiplicity', (0, 1), 'b', 1, 'oriented embedding multiplicity lost')
    bad_weight('lost_automorphism_multiplicity', (0, 1, 1), 'b', 1, 'oriented embedding multiplicity lost')
    bad_weight('wrong_extension_count', (0, 1, 1), 'e', 3, 'extension count corrupted')
    bad_weight('wrong_factorial_weight', (0, 1, 1), 'factorial', 2, 'factorial weight corrupted')
    altered = dict(pure_row((0, 1, 1))); del altered[5]
    result.append(expect_rejection('merged_distinct_arm_ideals',
                  lambda: verify_normalized_row((0, 1, 1), altered, 'individual-ideal Ferrers row fails normalization'),
                  'individual-ideal Ferrers row fails normalization'))
    result.append(expect_rejection('nonideal_precursor', lambda: pure_q((0, 1), 2), 'precursor is not an ideal'))
    def bad_row(name, order, row, reason):
        result.append(expect_rejection(name, lambda: verify_row_equal(row, graft_row(order, 0), reason), reason))
    p = CORES[0][:-1]
    altered = dict(prefix_row(p, 0)); altered[31] += 1
    bad_row('altered_q5', p, altered, 'graft changed held strict-prefix row')
    bad_row('cutoff_moved_to_five', p, {s: F(int(s == 31)) for s in ideals(p)}, 'graft changed held strict-prefix row')
    altered = dict(graft_row(CORES[0], 0)); altered[63] = F(0); altered[0] = F(1)
    bad_row('omitted_full_only_bridge', CORES[0], altered, 'selected graft suffix probability mismatch')
    p = ordinal(CORES[0], (0,))
    shuffled = relabel(p, tuple(reversed(range(7))))
    result.append(expect_rejection('chronological_core_tag', lambda: verify_core_claim(shuffled, 63), 'intrinsic core claim mismatch'))
    altered = dict(graft_row(p, 0)); altered[0] = F(1, 2); altered[127] = F(1, 2)
    bad_row('nonlifted_ideal_mass', p, altered, 'selected graft suffix probability mismatch')
    p = ordinal(CORES[0], (0, 1))
    altered = dict(graft_row(p, 0)); altered[127], altered[255] = altered[255], altered[127]
    bad_row('wrong_suffix_probability', p, altered, 'selected graft suffix probability mismatch')
    result.append(expect_rejection('changed_dependency_bytes', lambda: check_pin(b'changed', PINS['ri63_checker']), 'accepted dependency byte pin mismatch'))
    altered = load_json(canonical(witness)); altered['pure']['row_manifest_sha256'] = '0'*64
    result.append(expect_rejection('changed_certificate_manifest', lambda: verify_certificate(altered, witness), 'certificate finite witness mismatch'))
    result.append(expect_rejection('duplicate_json_key', lambda: load_json('{"x":0,"x":1}'), 'duplicate JSON object key'))
    altered = dict(witness['pure']['unmarked_classes'][-1])
    altered['diagram_mass'] = str(F(altered['diagram_mass'])+1)
    result.append(expect_rejection('wrong_unmarked_class_marginal',
                  lambda: verify_pushforward_class(altered), 'unmarked-class Plancherel pushforward mismatch'))
    return result


def deadline(signum, frame):
    raise RuntimeError('900-second wall-time alarm expired')


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    try:
        prefix = rebuild_prefix()
        budget('checking oriented Ferrers isomorphism weights and individual-ideal transitions')
        pure = pure_checks()
        budget('checking held prefix and declared intrinsic graft examples only')
        graft = graft_checks()
        witness = dict(schema='ri74-plancherel-graft-v1', dependencies=PINS,
                       finite_domain=dict(exhaustive_order_maximum=6, pure_parent_maximum=5,
                                          pure_diamond_base_maximum=4, selected_graft_order_maximum=9,
                                          graft_cutoff=6, optimizer_calls=0, adopted_law=False,
                                          strict_positive_above_cutoff=False),
                       accepted_prefix=prefix, pure=pure, graft=graft)
        negative = controls(witness)
        for key, path in DEPENDENCY_PATHS.items():
            check_pin(path.read_bytes(), PINS[key])
        budget('bounded exact corroboration complete; no all-size theorem inferred from enumeration')
        if sys.argv[1:] == ['--witness']:
            print(canonical(witness))
        else:
            saved = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
            verify_certificate(saved, witness)
            print('pure_inventory='+canonical(pure['inventory']))
            print('coverage='+canonical({k: v for k, v in graft.items() if k.endswith('diamonds') or k.startswith('prefix_') or k == 'selected_maximal_deletions'}))
            print('negative_controls='+canonical(negative))
            print('witness_sha256='+digest(witness))
            print('DONE: finite zero-allowed Ferrers/graft corroboration; no replacement law or strict approximation')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
