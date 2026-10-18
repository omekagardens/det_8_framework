#!/usr/bin/env python3
"""RI-63: bounded exact parent-five expected-defect problem reconstruction.

Standard library only; no project imports, downloads, subprocesses or writes.
RI-52 prefix formulas and RI-41 coefficients are re-expressed here. The actual
RI-41 certificate is byte-pinned and reconciled before any reconstruction.
Every naturally labeled parent through five is enumerated, but unknown growth
probabilities are considered only at parent five. Six-event orders are used
only as terminal orders and for intrinsic induced-suborder defect diagnostics.

--problem emits exact rational JSON for separate optimization discovery. It is
not an optimizer, a certificate of optimality, or an all-size performance test.
Without arguments the supplied certificate is checked using exact primal and
dual arithmetic, sequential face-dual canonical tie-break proofs, a distinct
primary optimum, and complete strict-mixture row/diamond replays.
The bounded run has a fifteen-minute wall-time alarm and checks peak resident
memory against two GiB at stage/parent boundaries. No claim of efficiency.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import json
import resource
import signal
import sys
import time


RI41_CERTIFICATE_SHA256 = '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969'
PREFIX_PARAMETER_SHA256 = '465c5de48c69527fc59e8df1f494fd8cea33f8aec243f59b9b2820bd5b1c07a7'
MAX_SECONDS = 900
MAX_RESIDENT_BYTES = 2 * 1024 ** 3
START_TIME = None


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    if START_TIME is not None:
        require(time.monotonic() - START_TIME <= MAX_SECONDS,
                'fifteen-minute reconstruction limit exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == 'darwin' else peak * 1024
    require(peak_bytes <= MAX_RESIDENT_BYTES, 'two-GiB resident-memory limit exceeded')
    if stage is not None:
        print('RI63: ' + stage, file=sys.stderr, flush=True)


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


def unique_json_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key')
        result[key] = value
    return result


def load_json(text):
    def bad_constant(value):
        raise RuntimeError('nonfinite JSON constant')
    return json.loads(text, object_pairs_hook=unique_json_object, parse_constant=bad_constant)


def digest(value):
    return sha256(canonical_json(value).encode()).hexdigest()


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


@cache
def valid_order(order):
    require(len(order) <= 6, 'order outside terminal-size-six cap')
    return all(isinstance(past, int) and 0 <= past < (1 << v)
               and all(order[u] & past == order[u] for u in bits(past))
               for v, past in enumerate(order))


@cache
def ideals(order):
    require(valid_order(order), 'invalid naturally labeled transitive order')
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


@cache
def parents(n):
    require(0 <= n <= 5, 'full parent enumeration is capped at five')
    if n == 0:
        return ((),)
    return tuple(sorted(p + (s,) for p in parents(n - 1) for s in ideals(p)))


def independent_relation_inventory(n):
    """Enumerate every forward relation and retain exactly transitive ones.

    Unlike parents(), this does not generate by admissible birth ideals. The
    finite domain is all 2^(n choose 2) possible naturally oriented relations.
    """
    require(0 <= n <= 6, 'independent relation inventory capped at terminal size six')
    possible = tuple((u, v) for v in range(n) for u in range(v))
    found = set()
    for code in range(1 << len(possible)):
        order = [0] * n
        for i, (u, v) in enumerate(possible):
            if code & (1 << i):
                order[v] |= 1 << u
        transitive = all(not (order[w] & (1 << v))
                         or not (order[v] & (1 << u))
                         or bool(order[w] & (1 << u))
                         for u in range(n) for v in range(u + 1, n)
                         for w in range(v + 1, n))
        if transitive:
            found.add(tuple(order))
    return found


@cache
def permutations_of(n):
    require(0 <= n <= 6, 'permutation domain exceeds terminal size six')
    return tuple(permutations(range(n)))


@cache
def layout(order, part):
    n = len(order)
    require(n <= 5 and 0 <= part < (1 << n), 'local canonical domain exceeded')
    candidates, best = [], None
    for perm in permutations_of(n):
        edge = sum(1 << (n * perm[u] + perm[v])
                   for v, past in enumerate(order) for u in bits(past))
        selected = sum(1 << perm[v] for v in bits(part))
        pair = (edge, selected)
        if best is None or pair < best:
            best, candidates = pair, [perm]
        elif pair == best:
            candidates.append(perm)
    return best, tuple(candidates)


@cache
def node(order, part, record):
    require(isinstance(record, int) and 0 <= record < (1 << len(order)),
            'record outside full binary cube')
    require(part in ideals(order), 'local precursor is not an ideal')
    pair, candidates = layout(order, part)
    inside = record & part
    return pair + (min(sum(1 << perm[v] for v in bits(inside))
                       for perm in candidates),)


def row_key(order, record):
    # At fixed n the middle field is the same full mask for every row, so this
    # has exactly RI-59's (canonical relation, full marking) ordering.
    return node(order, (1 << len(order)) - 1, record)


def maximal_mask(order):
    ancestors = 0
    for past in order:
        ancestors |= past
    return ((1 << len(order)) - 1) & ~ancestors


@cache
def restriction(order, keep):
    surviving = tuple(bits(keep))
    remap = {v: i for i, v in enumerate(surviving)}
    induced = tuple(sum(1 << remap[u] for u in bits(order[v] & keep))
                    for v in surviving)
    require(valid_order(induced), 'induced restriction is not an order')
    return induced, surviving


def transport(mask, surviving):
    return sum(1 << i for i, v in enumerate(surviving) if mask & (1 << v))


A, C, D = F(2, 3), F(1, 5), F(1, 4)
FS = (F(1, 6), F(1, 3))
G, K = F(1, 10), F(11, 20)
HS, E = (F(19, 30), F(7, 15)), F(1, 44)
OVERRIDES4 = {
    0:'486413/200', 7:'27949/1000', 12:'268323/500', 17:'1851/500', 18:'101/500',
    22:'31/10', 25:'3/20', 30:'171/200', 31:'171/200', 32:'171/200', 33:'203153/1000',
    38:'361/1000', 39:'361/1000', 40:'361/1000', 41:'361/1000', 42:'12729/500',
    45:'64901/1000', 46:'29417/500', 47:'331/1000', 48:'333/1000', 53:'54747/1000',
    59:'429/1000', 60:'181/200', 61:'429/1000', 62:'181/200', 66:'141/1000',
    67:'79/500', 68:'7/40', 74:'27/125', 76:'27/125', 77:'99/100', 78:'99/100',
    79:'99/100', 80:'99/100', 81:'237/200', 82:'1193/1000', 83:'237/200',
    84:'1193/1000', 85:'237/200', 86:'1193/1000', 87:'237/200', 88:'1193/1000',
    89:'1083/1000', 90:'121/125', 91:'1083/1000', 92:'121/125', 93:'1083/1000',
    94:'121/125', 95:'249/250', 96:'199/200', 97:'199/200', 98:'249/250',
    99:'199/200', 100:'199/200', 101:'197/200', 102:'983/1000', 103:'197/200',
    104:'983/1000', 105:'197/200', 106:'983/1000', 107:'197/200', 108:'983/1000'
}
ROOTS4 = (
    (0,0,0),(0,1,0),(0,3,0),(0,7,0),(2,1,0),(2,3,0),(2,4,0),(2,5,0),
    (2,7,0),(2,12,0),(2,13,0),(2,13,1),(6,1,0),(6,3,0),(6,7,0),(6,8,0),
    (6,9,0),(6,9,1),(6,11,0),(6,11,1),(14,1,0),(14,1,1),(14,3,0),(14,3,1),
    (14,7,0),(14,7,1),(68,3,0),(68,7,0),(68,9,0),(68,9,1),(68,11,0),(68,11,1),
    (68,11,3),(70,3,0),(70,7,0),(70,8,0),(70,9,0),(70,9,1),(70,11,0),(70,11,1),
    (70,11,2),(70,11,3),(72,3,0),(72,7,0),(72,7,1),(76,3,0),(76,3,1),(76,7,0),
    (76,7,1),(76,11,0),(76,11,1),(76,11,2),(76,11,3),(78,3,0),(78,3,1),(78,7,0),
    (78,7,1),(78,9,0),(78,9,1),(78,11,0),(78,11,1),(78,11,2),(78,11,3),(204,3,0),
    (204,3,1),(204,3,3),(204,7,0),(204,7,1),(204,7,3),(206,3,0),(206,3,1),
    (206,3,2),(206,3,3),(206,7,0),(206,7,1),(206,7,2),(206,7,3),(2184,7,0),
    (2184,7,1),(2184,7,3),(2184,7,7),(2186,7,0),(2186,7,1),(2186,7,2),(2186,7,3),
    (2186,7,4),(2186,7,5),(2186,7,6),(2186,7,7),(2190,7,0),(2190,7,1),(2190,7,2),(2190,7,3),
    (2190,7,6),(2190,7,7),(2252,7,0),(2252,7,1),(2252,7,3),(2252,7,4),
    (2252,7,5),(2252,7,7),(2254,7,0),(2254,7,1),(2254,7,2),(2254,7,3),(2254,7,4),
    (2254,7,5),(2254,7,6),(2254,7,7)
)
COEFFICIENTS4 = {}


def pin_prefix_certificate():
    path = Path(__file__).resolve().parent.parent / 'native_growth_height_normalization_v1' / 'CERTIFICATE.json'
    raw = path.read_bytes()
    require(sha256(raw).hexdigest() == RI41_CERTIFICATE_SHA256,
            'actual RI-41 certificate byte pin mismatch')
    certificate = load_json(raw)
    require(certificate['schema'] == 'ri41-height-primal-v1'
            and certificate['seed'] == 'interior_a'
            and certificate['parent_size'] == 4, 'RI-41 certificate domain mismatch')
    require(tuple(map(tuple, certificate['roots'])) == ROOTS4
            and certificate['default_alpha'] == '1/8'
            and certificate['overrides'] == {str(k): v for k, v in OVERRIDES4.items()},
            'embedded RI-41 coefficients disagree with actual pinned certificate')
    seed_data = dict(roots=ROOTS4, default_alpha='1/8',
                     overrides={str(k): v for k, v in OVERRIDES4.items()})
    require(sha256((canonical_json(seed_data) + '\n').encode()).hexdigest()
            == PREFIX_PARAMETER_SHA256, 'RI-41 parameter identity mismatch')


@cache
def row(order, record):
    n, full = len(order), (1 << len(order)) - 1
    require(0 <= n <= 4 and isinstance(record, int) and 0 <= record < (1 << n),
            'fixed-law lookup outside prefix')
    require(valid_order(order), 'fixed-law lookup has malformed order')
    if n == 0:
        return {0: F(1)}
    if n == 1:
        return {0: A, full: 1-A}
    edge_count = sum(p.bit_count() for p in order)
    if n == 2:
        if edge_count:
            return {0: C, 1: FS[record & 1], full: HS[record & 1]}
        return {0: D, 1: G, 2: G, full: K}
    if n == 3:
        result = {s: E for s in ideals(order) if s != full}
        if edge_count == 0:
            for s in result:
                if s.bit_count() == 1:
                    result[s] *= G/D
                elif s.bit_count() == 2:
                    result[s] *= K/D
        elif edge_count == 1:
            tip = next(v for v, past in enumerate(order) if past)
            root = next(bits(order[tip]))
            isolated = next(v for v in range(3) if v not in (root, tip))
            bit = (record >> root) & 1
            result[1 << root] *= FS[bit]/C
            result[(1 << root) | (1 << tip)] *= HS[bit]/C
            result[(1 << root) | (1 << isolated)] *= K/G
        elif edge_count == 2:
            roots = [v for v in range(3)
                     if sum(bool(p & (1 << v)) for p in order) == 2]
            if roots:
                bit = (record >> roots[0]) & 1
                for s in result:
                    if s.bit_count() == 2:
                        result[s] *= HS[bit]/FS[bit]
    else:
        require(COEFFICIENTS4, 'RI-41 coefficients used before reconstruction')
        result = {s: COEFFICIENTS4[node(order, s, record)] * potential(order, s, record & s)
                  for s in ideals(order) if s != full}
    result[full] = 1 - sum(result.values(), F(0))
    require(all(q > 0 for q in result.values()), 'nonpositive fixed-prefix probability')
    require(sum(result.values(), F(0)) == 1, 'fixed-prefix normalization failure')
    return result


@cache
def potential(order, part, inside_record):
    n, full = len(order), (1 << len(order)) - 1
    require(n in (4, 5) and part in ideals(order) and part != full
            and inside_record & ~part == 0,
            'potential outside declared proper-slot domain')
    omitted = maximal_mask(order) & ~part
    require(omitted, 'proper ideal omitted no maximal vertex')
    value, deleted = F(1), omitted
    while deleted:
        smaller, surviving = restriction(order, full ^ deleted)
        s, r = transport(part, surviving), transport(inside_record, surviving)
        factor = row(smaller, r)[s]
        value = value * factor if deleted.bit_count() % 2 else value / factor
        deleted = (deleted - 1) & omitted
    require(value > 0, 'nonpositive maximal-deletion potential')
    return value


class Components:
    def __init__(self, keys):
        self.parent = {key: key for key in keys}

    def root(self, key):
        trail = []
        while self.parent[key] != key:
            trail.append(key)
            key = self.parent[key]
        for item in trail:
            self.parent[item] = key
        return key

    def join(self, first, second):
        low, high = sorted((self.root(first), self.root(second)))
        self.parent[high] = low

    def finish(self):
        roots = sorted({self.root(key) for key in self.parent})
        numbers = {key: i for i, key in enumerate(roots)}
        return roots, {key: numbers[self.root(key)] for key in self.parent}


def reconstruct_prefix():
    values, proper_count = {}, 0
    for order in parents(4):
        for record in range(16):
            for part in ideals(order):
                if part == 15:
                    continue
                key, u = node(order, part, record), potential(order, part, record & part)
                require(key not in values or values[key] == u, 'prefix local-potential mismatch')
                values[key] = u
                proper_count += 1
    graph = Components(values)
    edges = zeros = equals = loops = 0
    for base in parents(3):
        for record in range(8):
            old = row(base, record)
            for first in ideals(base):
                for second in ideals(base):
                    for b in (0, 1):
                        for h in (0, 1):
                            i = node(base + (first,), second, record | (b << 3))
                            j = node(base + (second,), first, record | (h << 3))
                            require(old[first] * values[i] == old[second] * values[j],
                                    'prefix potential diamond failure')
                            graph.join(i, j)
                            edges += 1
                            zeros += int(record == b == h == 0)
                            equals += int(first == second)
                            loops += int(i == j)
    roots, component = graph.finish()
    require(tuple(roots) == ROOTS4, 'RI-41 canonical components changed')
    for key, c in component.items():
        COEFFICIENTS4[key] = F(OVERRIDES4.get(c, '1/8'))
    lower_ratios = fixed_rows = fixed_slots = 0
    canonical_probabilities = {}
    for n in range(5):
        for order in parents(n):
            for record in range(1 << n):
                q = row(order, record)
                require(set(q) == set(ideals(order)) and all(v > 0 for v in q.values())
                        and sum(q.values(), F(0)) == 1, 'fixed row admission failure')
                fixed_rows += 1
                for part, value in q.items():
                    key = (n, node(order, part, record))
                    require(key not in canonical_probabilities or canonical_probabilities[key] == value,
                            'fixed row violates marked-local canonical quotient')
                    canonical_probabilities[key] = value
                    fixed_slots += 1
    for n in range(4):
        for base in parents(n):
            for record in range(1 << n):
                old = row(base, record)
                for first in ideals(base):
                    for second in ideals(base):
                        for b in (0, 1):
                            for h in (0, 1):
                                left = old[first] * row(base + (first,), record | (b << n))[second]
                                right = old[second] * row(base + (second,), record | (h << n))[first]
                                require(left == right, 'fixed full-map scalar diamond failure')
                                lower_ratios += int(n < 3)
    full_min = min(row(p, r)[15] for p in parents(4) for r in range(16))
    slot_min = min(q for p in parents(4) for r in range(16) for q in row(p, r).values())
    require((full_min, slot_min) == (F(33901019, 474368400), F(9, 681472)),
            'fixed RI-41 extrema changed')
    result = dict(parent_four_orders=40, marked_rows=640, proper_slots=proper_count,
                  nodes=len(values), components=len(roots), raw_ratios=edges,
                  all_zero=zeros, equal_precursors=equals, loops=loops,
                  lower_raw_ratios=lower_ratios, fixed_rows_through_four=fixed_rows,
                  fixed_slots_through_four=fixed_slots,
                  canonical_probability_keys=len(canonical_probabilities),
                  minimum_full=str(full_min), minimum_slot=str(slot_min))
    require((proper_count, len(values), len(roots), edges, lower_ratios,
             fixed_rows, fixed_slots, len(canonical_probabilities))
            == (5072, 305, 109, 7616, 436, 707, 6065, 585),
            'independently reconstructed prefix counts changed')
    return result


def partitions(total, ceiling=None):
    if total == 0:
        yield ()
        return
    if ceiling is None:
        ceiling = total
    for first in range(min(total, ceiling), 0, -1):
        for tail in partitions(total-first, first):
            yield (first,) + tail


def ferrers(partition):
    require(sum(partition) <= 6 and all(x > 0 for x in partition)
            and tuple(sorted(partition, reverse=True)) == partition, 'invalid Ferrers partition')
    cells = tuple((i, j) for i, length in enumerate(partition) for j in range(length))
    order = tuple(sum(1 << u for u, (k, l) in enumerate(cells)
                      if k <= i and l <= j and (k, l) != (i, j))
                  for i, j in cells)
    require(valid_order(order), 'Ferrers cell order is not natural')
    return order


FERRERS_BY_SIZE = {}


def build_ferrers_catalogue():
    inventory = []
    for n in range(7):
        found = set()
        parts = tuple(partitions(n))
        for partition in parts:
            original = ferrers(partition)
            for perm in permutations_of(n):
                relabeled = [0] * n
                for v, past in enumerate(original):
                    relabeled[perm[v]] = sum(1 << perm[u] for u in bits(past))
                candidate = tuple(relabeled)
                if all(past < (1 << v) for v, past in enumerate(candidate)):
                    require(valid_order(candidate), 'Ferrers permutation broke transitivity')
                    found.add(candidate)
        require(found, 'empty Ferrers catalogue at a declared size')
        if n <= 5:
            require(found <= set(parents(n)), 'natural Ferrers order missing from parent inventory')
        FERRERS_BY_SIZE[n] = frozenset(found)
        inventory.append(dict(size=n, partitions=len(parts), natural_orders=len(found),
                              natural_orders_sha256=digest(sorted(found))))
    require(tuple(item['partitions'] for item in inventory) == (1, 1, 2, 3, 5, 7, 11),
            'integer partition inventory changed')
    return inventory


@cache
def defect(order):
    require(valid_order(order) and len(order) in FERRERS_BY_SIZE,
            'intrinsic defect requested before catalogue or outside domain')
    if order in FERRERS_BY_SIZE[len(order)]:
        return 0
    full = (1 << len(order)) - 1
    # Every nonempty exceptional set removes some vertex. This recursion tests
    # arbitrary vertex deletions, not only ideals, maxima or immediate births.
    return 1 + min(defect(restriction(order, full ^ (1 << v))[0])
                   for v in range(len(order)))


@cache
def critical(order):
    maxima = tuple(bits(maximal_mask(order)))
    full = (1 << len(order)) - 1
    return len(maxima) >= 2 and all(
        defect(restriction(order, full ^ (1 << v))[0]) == defect(order) - 1
        for v in maxima)


@cache
def history_probability(order, record):
    require(len(order) <= 5 and 0 <= record < (1 << len(order)), 'history outside prefix-child cap')
    if not order:
        return F(1)
    n = len(order) - 1
    old_record = record & ((1 << n) - 1)
    return history_probability(order[:-1], old_record) * row(order[:-1], old_record)[order[-1]] / 2


def sparse(values):
    return {str(k): str(v) for k, v in sorted(values.items()) if v}


def expect_rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name + ': rejected for an unintended reason')
        return name
    raise RuntimeError(name + ': malformed input accepted')


def input_controls():
    controls = [
        expect_rejection('nontransitive_order', lambda: ideals((0, 1, 2)),
                         'invalid naturally labeled transitive order'),
        expect_rejection('backward_relation', lambda: row((2, 0), 0),
                         'fixed-law lookup has malformed order'),
        expect_rejection('record_outside_cube', lambda: node((0, 1, 3, 7, 1), 0, 32),
                         'record outside full binary cube'),
        expect_rejection('nonideal_precursor', lambda: node((0, 1), 2, 0),
                         'local precursor is not an ideal'),
    ]
    v_order = (0, 1, 1)
    antichain, surviving = restriction(v_order, 6)
    require(defect(v_order) == 0 and antichain == (0, 0) and defect(antichain) == 1,
            'arbitrary-suborder nonheredity control failed')
    controls.append('ferrers_V_to_nonferrers_antichain')
    return controls


def direct_subset_defect(order):
    """Independent minimization: test every arbitrary retained vertex subset.

    This deliberately does not call restriction() or the deletion recurrence.
    It shares only the completely generated finite Ferrers membership sets.
    """
    largest = 0
    for mask in range(1 << len(order)):
        selected = tuple(v for v in range(len(order)) if mask & (1 << v))
        induced = tuple(sum(1 << i for i, u in enumerate(selected)
                            if order[v] & (1 << u)) for v in selected)
        if induced in FERRERS_BY_SIZE[len(selected)]:
            largest = max(largest, len(selected))
    return len(order) - largest


def build_problem():
    """Construct the complete finite problem in memory; no optimizer is run."""
    global START_TIME
    START_TIME = time.monotonic()
    pin_prefix_certificate()
    budget('pinned RI-41 certificate; checking independent parent coverage')
    parent_coverage = []
    for n in range(6):
        generated = set(parents(n))
        reference = independent_relation_inventory(n)
        require(len(generated) == len(parents(n)) and generated == reference,
                'birth-ideal inventory differs from independent forward-relation enumeration')
        parent_coverage.append(dict(size=n, natural_orders=len(generated),
                                    forward_relations=1 << (n * (n-1) // 2),
                                    orders_sha256=digest(sorted(generated))))
    require(tuple(item['natural_orders'] for item in parent_coverage) == (1, 1, 2, 7, 40, 357),
            'natural parent count changed')
    prefix_counts = reconstruct_prefix()
    budget('fixed prefix reconstructed; building complete Ferrers catalogue through six')
    ferrers_inventory = build_ferrers_catalogue()
    controls = input_controls()
    history_totals = []
    for n in range(6):
        total = sum((history_probability(p, r) for p in parents(n)
                     for r in range(1 << n)), F(0))
        require(total == 1, 'unconditional finite-history probability does not sum to one')
        history_totals.append(str(total))
    values, metadata, unique_rows, terminal_orders = {}, {}, {}, set()
    raw_rows = proper_slots = 0
    history_digest = sha256()
    budget('enumerating every parent-five record and labeled ideal')
    for order in parents(5):
        budget()
        delta = defect(order)
        increments = {}
        for part in ideals(order):
            terminal = order + (part,)
            terminal_orders.add(terminal)
            increments[part] = defect(terminal) - delta
            require(increments[part] in (0, 1), 'maximal-birth defect increment is not zero or one')
        for record in range(32):
            entries = []
            weight = history_probability(order, record)
            require(weight > 0, 'strict-prefix marked history has zero probability')
            history_digest.update((canonical_json([order, record, str(weight)]) + '\n').encode())
            for part in ideals(order):
                if part == 31:
                    continue
                key, u = node(order, part, record), potential(order, part, record & part)
                data = (increments[part], increments[31], critical(order + (part,)))
                require(key not in values or values[key] == u,
                        'proper marked-local quotient changed potential')
                require(key not in metadata or metadata[key] == data,
                        'proper local quotient changed order diagnostics')
                values[key], metadata[key] = u, data
                entries.append((key, u, part, increments[part]))
                proper_slots += 1
            key = row_key(order, record)
            signature = tuple(sorted((key, u, d) for key, u, part, d in entries))
            invariant = (delta, increments[31], critical(order), signature)
            if key not in unique_rows:
                unique_rows[key] = dict(order=order, record=record, pi=F(0), multiplicity=0,
                                        invariant=invariant, entries=entries)
            item = unique_rows[key]
            require(item['invariant'] == invariant,
                    'marked-row quotient changed labeled ideal multiplicities or diagnostics')
            item['pi'] += weight
            item['multiplicity'] += 1
            raw_rows += 1
    require(sum((item['pi'] for item in unique_rows.values()), F(0)) == 1,
            'canonical marked-row history weights do not sum to one')
    require(sum(item['multiplicity'] for item in unique_rows.values()) == raw_rows,
            'marked-row quotient lost natural-history multiplicity')
    require(len(terminal_orders) == 4824, 'terminal-six birth inventory changed')
    require(terminal_orders == independent_relation_inventory(6),
            'terminal births differ from independent forward-relation enumeration')
    budget('checking arbitrary-subset defect independently on every terminal order')
    for order in sorted(terminal_orders):
        budget()
        require(defect(order) == direct_subset_defect(order),
                'deletion recurrence disagrees with direct arbitrary-subset defect')

    budget('constructing every base-four complete-record scalar diamond')
    graph, covered = Components(values), set()
    edges = zeros = equals = loops = 0
    edge_digest = sha256()
    for base in parents(4):
        budget()
        for record in range(16):
            old = row(base, record)
            for first in ideals(base):
                for second in ideals(base):
                    for b in (0, 1):
                        for h in (0, 1):
                            left = base + (first,)
                            right = base + (second,)
                            i = node(left, second, record | (b << 4))
                            j = node(right, first, record | (h << 4))
                            require(i in values and j in values, 'complete diamond endpoint not seeded')
                            require(old[first] * values[i] == old[second] * values[j],
                                    'new-layer potential ratio failure')
                            require(metadata[i][2] == metadata[j][2],
                                    'diamond changed terminal critical membership')
                            graph.join(i, j)
                            covered.update((i, j))
                            edge_digest.update((canonical_json(
                                [base, record, first, second, b, h, i, j,
                                 str(old[first]), str(old[second])]) + '\n').encode())
                            edges += 1
                            zeros += int(record == b == h == 0)
                            equals += int(first == second)
                            loops += int(i == j)
    roots, component = graph.finish()
    # Isolates are deliberately seeded even if this particular finite graph
    # happens to cover every node with an edge.
    unincident = sorted(set(values) - covered)
    rows, beta = [], [F(0)] * len(roots)
    baseline = expected_delta = critical_probability = F(0)
    maximum_u = F(0)
    for key, item in sorted(unique_rows.items()):
        delta, full_drift, is_critical, _ = item['invariant']
        cap, derivative, raising, slots = {}, {}, {}, []
        for local_key, u, part, d in item['entries']:
            c = component[local_key]
            cap[c] = cap.get(c, F(0)) + u
            derivative[c] = derivative.get(c, F(0)) + (d-full_drift) * u
            raising[c] = raising.get(c, F(0)) + d * u
            slots.append(dict(past_mask=part, node=local_key, component=c, u=str(u), increment=d))
        pi = item['pi']
        baseline += pi * full_drift
        expected_delta += pi * delta
        critical_probability += pi * int(is_critical)
        maximum_u = max(maximum_u, sum(cap.values(), F(0)))
        for c, coefficient in derivative.items():
            beta[c] += pi * coefficient
        rows.append(dict(key=key, past_masks=item['order'], record=item['record'],
                         natural_history_multiplicity=item['multiplicity'], pi=str(pi),
                         defect=delta, full_increment=full_drift, critical=is_critical,
                         A=sparse(cap), D=sparse(derivative), raising=sparse(raising), slots=slots))
    everywhere_raising, critical_components = [], []
    for c in range(len(roots)):
        data = [metadata[key] for key in values if component[key] == c]
        if all(d == 1 for d, f, is_critical in data):
            require(beta[c] >= 0, 'everywhere-raising component has negative coefficient')
            everywhere_raising.append(c)
        if any(is_critical for d, f, is_critical in data):
            require(all(is_critical and d == 1 for d, f, is_critical in data),
                    'critical-child component contains a noncritical or neutral occurrence')
            critical_components.append(c)
    counts = dict(natural_parents=357, raw_marked_rows=raw_rows, proper_labeled_slots=proper_slots,
                  all_labeled_slots=proper_slots+raw_rows, proper_local_nodes=len(values),
                  components=len(roots), marked_row_classes=len(rows), raw_ratios=edges,
                  all_zero=zeros, equal_precursors=equals, loops=loops,
                  unincident_nodes=len(unincident), terminal_orders=len(terminal_orders),
                  positive_beta=sum(v > 0 for v in beta), zero_beta=sum(v == 0 for v in beta),
                  negative_beta=sum(v < 0 for v in beta),
                  critical_parent_classes=sum(item['critical'] for item in rows),
                  everywhere_raising_components=len(everywhere_raising),
                  critical_child_components=len(critical_components))
    require((raw_rows, proper_slots, len(values), len(roots), len(rows), edges, zeros, equals, loops)
            == (11424, 142944, 2961, 798, 1490, 216128, 3377, 22848, 28176),
            'complete parent-five inventory differs from independent expected counts')
    hook_roles = []
    hook_component = component[node((0, 1, 3, 7, 1), 0, 0)]
    for name, order, part, d, f in (
            ('empty_F', (0, 1, 3, 7, 1), 0, 1, 1),
            ('long_arm_restore_G', (0, 1, 3, 1, 0), 7, 0, 1),
            ('short_arm_restore_chain', (0, 1, 3, 7, 0), 1, 0, 0)):
        keys = set()
        for record in range(32):
            key = node(order, part, record)
            require(component[key] == hook_component and metadata[key][:2] == (d, f),
                    'all-mark hook mixed-component classification changed')
            keys.add(key)
        hook_roles.append(dict(role=name, past_masks=order, past_mask=part,
                               increment=d, full_increment=f, all_records=32,
                               local_keys=sorted(keys)))
    require(beta[hook_component] < 0, 'hook component is not genuinely negative')
    require(all(d-f <= 0 for key, (d, f, is_critical) in metadata.items()
                if component[key] == hook_component), 'hook component contains a positive reduced cost')
    interior_c, eta = 1 / (2 * (1+maximum_u)), F(1, 36)
    interior_objective = baseline + interior_c * sum(beta, F(0))
    require(0 <= interior_objective <= 1 and baseline > 0,
            'invalid interior objective or all-full baseline')
    node_manifest = [dict(key=key, component=component[key], u=str(values[key]),
                          increment=metadata[key][0], full_increment=metadata[key][1],
                          critical_child=metadata[key][2]) for key in sorted(values)]
    problem = dict(schema='ri63-expected-defect-problem-v1', parent_size=5,
                   terminal_size=6, fixed_prefix_parent_maximum=4,
                   ri41_certificate_source_sha256=RI41_CERTIFICATE_SHA256,
                   fixed_prefix_parameter_json_sha256=PREFIX_PARAMETER_SHA256,
                   parent_coverage=parent_coverage, prefix_counts=prefix_counts,
                   ferrers_inventory=ferrers_inventory, history_mass_by_size=history_totals,
                   diagnostic_checks=dict(terminal_forward_relations=1 << 15,
                                          terminal_orders=4824,
                                          terminal_arbitrary_subsets=4824 * 64,
                                          negative_controls=controls),
                   counts=counts, roots=roots, rows=rows, nodes=node_manifest,
                   beta=[str(v) for v in beta], B5=str(baseline),
                   expected_delta5=str(expected_delta), critical_probability5=str(critical_probability),
                   M5=str(maximum_u), c5=str(interior_c), eta5=str(eta),
                   interior_expected_increment=str(interior_objective),
                   everywhere_raising_components=everywhere_raising,
                   critical_child_components=critical_components, unincident_node_keys=unincident,
                   hook=dict(component=hook_component, beta=str(beta[hook_component]), roles=hook_roles))
    problem['hashes'] = dict(
        roots=digest(roots), row_matrix=digest(rows), local_nodes=digest(node_manifest),
        canonical_history_weights=digest([[item['key'], item['pi'], item['natural_history_multiplicity']]
                                          for item in rows]),
        raw_marked_histories=history_digest.hexdigest(), raw_complete_diamonds=edge_digest.hexdigest(),
        terminal_defects=digest([[p, defect(p)] for p in sorted(terminal_orders)]),
        affine_objective=digest(dict(B5=str(baseline), beta=[str(v) for v in beta])))
    problem['hashes']['problem_without_self_hash'] = digest(problem)
    budget('exact parent-five problem complete; no optimization performed')
    return problem


def parse_sparse(encoded, count, name, *, signed=False):
    require(isinstance(encoded, dict), name + ': expected sparse object')
    result = {}
    for key, value in encoded.items():
        require(isinstance(key, str) and key.isascii() and key.isdecimal()
                and str(int(key)) == key and 0 <= int(key) < count,
                name + ': invalid canonical index')
        require(isinstance(value, str), name + ': coefficient is not a fraction string')
        try:
            fraction = F(value)
        except (ValueError, ZeroDivisionError):
            raise RuntimeError(name + ': invalid fraction') from None
        require(str(fraction) == value, name + ': noncanonical fraction string')
        require(fraction != 0 and (signed or fraction > 0),
                name + ': sparse coefficient has invalid sign or explicit zero')
        result[int(key)] = fraction
    return result


def verify_problem_consistency(problem):
    """Recompute exact objective/weights from the exported labeled slots."""
    rows, width = problem['rows'], len(problem['roots'])
    weights = [F(item['pi']) for item in rows]
    require(all(p > 0 for p in weights) and sum(weights, F(0)) == 1,
            'complete marked-row history weights do not normalize')
    beta = [F(0)] * width
    baseline = expected_delta = F(0)
    maximum_u = F(0)
    for item, pi in zip(rows, weights):
        cap, derivative, raising = {}, {}, {}
        for slot in item['slots']:
            c, u, d = slot['component'], F(slot['u']), slot['increment']
            require(type(c) is int and 0 <= c < width and u > 0 and d in (0, 1),
                    'exported labeled proper slot is malformed')
            cap[c] = cap.get(c, F(0)) + u
            derivative[c] = derivative.get(c, F(0)) + (d-item['full_increment']) * u
            raising[c] = raising.get(c, F(0)) + d * u
        require(item['A'] == sparse(cap) and item['D'] == sparse(derivative)
                and item['raising'] == sparse(raising), 'exported row loses labeled-slot multiplicity')
        baseline += pi * item['full_increment']
        expected_delta += pi * item['defect']
        maximum_u = max(maximum_u, sum(cap.values(), F(0)))
        for c, value in derivative.items():
            beta[c] += pi * value
    require([str(v) for v in beta] == problem['beta'] and str(baseline) == problem['B5'],
            'exported affine objective differs from complete history-weighted slots')
    require(str(expected_delta) == problem['expected_delta5'] and str(maximum_u) == problem['M5'],
            'exported initial defect or potential bound changed')
    require(F(problem['c5']) == 1/(2*(1+maximum_u)) and F(problem['eta5']) == F(1, 36),
            'declared RI-59 mixture changed')
    hashed = dict(problem)
    hashed['hashes'] = dict(problem['hashes'])
    claimed_hash = hashed['hashes'].pop('problem_without_self_hash')
    require(digest(hashed) == claimed_hash, 'exported problem self-manifest mismatch')
    return weights, [{int(k): F(v) for k, v in item['A'].items()} for item in rows], beta


def check_certificate_core(certificate, problem):
    required = {'schema', 'parent_size', 'problem_hashes', 'alpha', 'primary_dual', 'tie_break',
                'alternative_primary_alpha'}
    allowed = required | {'ri41_certificate_source_sha256',
                          'fixed_prefix_parameter_json_sha256', 'claims'}
    require(isinstance(certificate, dict) and required <= set(certificate)
            and set(certificate) <= allowed, 'certificate has missing or unknown fields')
    require(certificate['schema'] == 'ri63-expected-defect-lex-certificate-v1'
            and type(certificate['parent_size']) is int and certificate['parent_size'] == 5,
            'certificate schema or parent domain mismatch')
    require(certificate['problem_hashes'] == problem['hashes'], 'certificate problem manifest mismatch')
    for field in ('ri41_certificate_source_sha256', 'fixed_prefix_parameter_json_sha256'):
        require(field not in certificate or certificate[field] == problem[field],
                'certificate fixed-prefix identity mismatch')
    weights, matrix, beta = verify_problem_consistency(problem)
    row_count, width = len(matrix), len(beta)
    sparse_alpha = parse_sparse(certificate['alpha'], width, 'alpha')
    alpha = [sparse_alpha.get(c, F(0)) for c in range(width)]
    y = parse_sparse(certificate['primary_dual'], row_count, 'primary_dual')
    masses = [sum((v*alpha[c] for c, v in row.items()), F(0)) for row in matrix]
    require(all(0 <= mass <= 1 for mass in masses), 'primary primal row cap failure')
    reduced = list(beta)
    for j, multiplier in y.items():
        for c, value in matrix[j].items():
            reduced[c] += multiplier * value
    require(all(v >= 0 for v in reduced), 'primary dual feasibility failure')
    objective = sum((v*x for v, x in zip(beta, alpha)), F(0))
    require(objective == -sum(y.values(), F(0)), 'primary exact duality gap is nonzero')
    require(all(alpha[c] == 0 for c in range(width) if beta[c] >= 0),
            'nonnegative-cost coordinate survives canonical elimination')
    require(all(alpha[c] == 0 for c in range(width) if reduced[c] > 0)
            and all(masses[j] == 1 for j in y), 'primary complementarity failure')

    tie = certificate['tie_break']
    require(isinstance(tie, dict) and set(tie) == {'kind', 'stages'}
            and tie['kind'] == 'sequential_face_duals' and isinstance(tie['stages'], dict),
            'canonical tie-break proof schema mismatch')
    required_stages = {str(c) for c, value in enumerate(alpha) if value > 0}
    require(set(tie['stages']) == required_stages, 'canonical positive-coordinate stages incomplete')
    free = {c for c in range(width) if beta[c] < 0 and reduced[c] == 0}
    stage_reports = []
    for k in sorted(sparse_alpha):
        budget()
        stage = tie['stages'][str(k)]
        require(isinstance(stage, dict) and set(stage) == {'row_dual', 'equality_dual'},
                'canonical stage has missing or unknown fields')
        row_dual = parse_sparse(stage['row_dual'], row_count, 'stage_row_dual')
        equality_dual = parse_sparse(stage['equality_dual'], row_count,
                                     'stage_equality_dual', signed=True)
        require(set(equality_dual) <= set(y), 'stage equality is not a primary forced row')
        remaining = {c for c in free if c >= k}
        require(k in remaining, 'positive canonical target is outside the primary optimal face')
        rhs = [1 - sum((value*alpha[c] for c, value in row.items() if c < k), F(0))
               for row in matrix]
        require(all(value >= 0 for value in rhs), 'canonical fixed prefix violates a row cap')
        gradient = {c: F(int(c == k)) for c in remaining}
        for j, multiplier in row_dual.items():
            for c, value in matrix[j].items():
                if c in remaining:
                    gradient[c] += multiplier * value
        for j, multiplier in equality_dual.items():
            for c, value in matrix[j].items():
                if c in remaining:
                    gradient[c] -= multiplier * value
        require(all(v >= 0 for v in gradient.values()), 'canonical stage dual feasibility failure')
        lower_bound = -sum((v*rhs[j] for j, v in row_dual.items()), F(0))
        lower_bound += sum((v*rhs[j] for j, v in equality_dual.items()), F(0))
        require(lower_bound == alpha[k], 'canonical stage exact lower bound misses target')
        stage_reports.append(dict(component=k, minimum=str(lower_bound),
                                  row_multipliers=len(row_dual),
                                  equality_multipliers=len(equality_dual),
                                  remaining_columns=len(remaining)))
    alternative_sparse = parse_sparse(certificate['alternative_primary_alpha'], width,
                                      'alternative_primary_alpha')
    alternative = [alternative_sparse.get(c, F(0)) for c in range(width)]
    require(all(sum((value*alternative[c] for c, value in row.items()), F(0)) <= 1
                for row in matrix), 'alternative primary primal row cap failure')
    require(sum((v*x for v, x in zip(beta, alternative)), F(0)) == objective,
            'alternative primary objective differs from certified optimum')
    require(alternative != alpha, 'alternative primary witness is not distinct')
    require(all(alternative[c] == 0 for c in range(width) if beta[c] >= 0),
            'alternative witness does not lie on the eliminated primary face')
    return dict(alpha=alpha, primary_dual=y, reduced=reduced, masses=masses,
                objective=objective, weights=weights, matrix=matrix, beta=beta,
                stage_reports=stage_reports, alternative=alternative)


def certificate_reports(certificate, problem, proof):
    rows, alpha, matrix = problem['rows'], proof['alpha'], proof['matrix']
    beta, pi = proof['beta'], proof['weights']
    eta, interior_c = F(problem['eta5']), F(problem['c5'])
    mixed = [(1-eta)*value + eta*interior_c for value in alpha]
    require(all(value > 0 for value in mixed), 'strict mixture has a zero component')
    contributions = {key: F(0) for key in ('A_critical', 'A_out', 'F_critical', 'F_out')}
    actual_contributions = {key: F(0) for key in contributions}
    suppressed_probability = critical_child_probability = F(0)
    maximum_suppressed = F(0)
    boundary_critical_children = F(0)
    boundary_drifts = []
    minimum_full = F(1)
    minimum_proper = None
    canonical_full = {}
    local_items = {tuple(item['key']): item for item in problem['nodes']}
    proper_q = {key: F(item['u'])*mixed[item['component']] for key, item in local_items.items()}
    actual_increment = F(0)
    for j, item in enumerate(rows):
        boundary_full = 1-proof['masses'][j]
        actual_full = 1-sum((value*mixed[c] for c, value in matrix[j].items()), F(0))
        require(actual_full > eta/2, 'strict mixed full complement is not above eta/2')
        canonical_full[tuple(item['key'])] = actual_full
        minimum_full = min(minimum_full, actual_full)
        suffix = 'critical' if item['critical'] else 'out'
        contributions['F_' + suffix] += pi[j]*item['full_increment']*boundary_full
        actual_contributions['F_' + suffix] += pi[j]*item['full_increment']*actual_full
        mu = item['full_increment']*actual_full
        boundary_mu = item['full_increment']*boundary_full
        suppressed = F(0)
        for slot in item['slots']:
            c, u, d = slot['component'], F(slot['u']), slot['increment']
            q0, q = u*alpha[c], u*mixed[c]
            require(q > 0, 'strict mixture proper slot is not positive')
            minimum_proper = q if minimum_proper is None else min(minimum_proper, q)
            contributions['A_' + suffix] += pi[j]*d*q0
            boundary_mu += d*q0
            actual_contributions['A_' + suffix] += pi[j]*d*q
            mu += d*q
            if beta[c] >= 0:
                require(q == eta*interior_c*u, 'eliminated component exceeds exact mixing restoration')
                suppressed += q
            if local_items[tuple(slot['node'])]['critical_child']:
                boundary_critical_children += pi[j]*q0
                critical_child_probability += pi[j]*q
        require(suppressed < eta/2, 'aggregate suppressed row mass is not below eta/2')
        suppressed_probability += pi[j]*suppressed
        maximum_suppressed = max(maximum_suppressed, suppressed)
        actual_increment += pi[j]*mu
        boundary_drifts.append(boundary_mu)
    boundary_increment = F(problem['B5']) + proof['objective']
    require(boundary_increment >= F(2401, 450000), 'RI-59 fixed-prefix weighted lower bound failed')
    interior_increment = F(problem['interior_expected_increment'])
    require(sum(contributions.values(), F(0)) == boundary_increment,
            'boundary mixed/full contribution split differs from certified objective')
    require(actual_increment == (1-eta)*boundary_increment + eta*interior_increment
            and sum(actual_contributions.values(), F(0)) == actual_increment,
            'actual mixed drift differs from affine objective or contribution split')
    require(boundary_critical_children == 0 and critical_child_probability <= suppressed_probability,
            'critical-child suppression consequence failed')
    active = [c for c, value in enumerate(alpha) if value > 0]
    active_neutral = [c for c in active
                      if all(item['increment'] == 0 for item in local_items.values()
                             if item['component'] == c)]
    noncritical_rows = [j for j, item in enumerate(rows) if not item['critical']]
    noncritical_zero_rows = [j for j in noncritical_rows if boundary_drifts[j] == 0]
    require(len(active_neutral) == len(active),
            'certified active boundary component is not everywhere neutral')
    require(noncritical_zero_rows == noncritical_rows,
            'certified noncritical boundary row has nonzero drift')
    hook_c = problem['hook']['component']
    hook_probabilities = {proper_q[node((0, 1, 3, 7, 1), 0, record)] for record in range(32)}
    require(len(hook_probabilities) == 1, 'hook empty-ideal probability reads excluded marks')
    hook_report = dict(component=hook_c, beta=str(beta[hook_c]), boundary_alpha=str(alpha[hook_c]),
                       strict_alpha=str(mixed[hook_c]),
                       empty_ideal_probability=str(next(iter(hook_probabilities))),
                       records_checked=32)

    budget('replaying actual strict probabilities on every marked history and diamond')
    actual_rows, actual_local, raw_expectation = {}, {}, F(0)
    raw_slots = 0
    for order in parents(5):
        budget()
        delta = defect(order)
        for record in range(32):
            q = {s: proper_q[node(order, s, record)] for s in ideals(order) if s != 31}
            q[31] = 1-sum(q.values(), F(0))
            require(q[31] == canonical_full[row_key(order, record)] and q[31] > eta/2
                    and all(value > 0 for value in q.values()), 'raw marked strict row failure')
            require(sum(q.values(), F(0)) == 1, 'raw marked strict row normalization failure')
            for s, value in q.items():
                key = node(order, s, record)
                require(key not in actual_local or actual_local[key] == value,
                        'actual probability violates the marked-local quotient')
                actual_local[key] = value
                raw_slots += 1
            raw_expectation += history_probability(order, record) * sum(
                ((defect(order+(s,))-delta)*value for s, value in q.items()), F(0))
            actual_rows[(order, record)] = q
    require(raw_expectation == actual_increment and raw_slots == 154368,
            'raw-history actual objective or slot coverage differs from canonical calculation')
    actual_ratios = 0
    for base in parents(4):
        budget()
        for record in range(16):
            old = row(base, record)
            for first in ideals(base):
                for second in ideals(base):
                    for b in (0, 1):
                        for h in (0, 1):
                            left = old[first]*actual_rows[(base+(first,), record|(b << 4))][second]
                            right = old[second]*actual_rows[(base+(second,), record|(h << 4))][first]
                            require(left == right, 'actual strict scalar-map diamond failure')
                            actual_ratios += 1
    require(actual_ratios == 216128, 'actual scalar-map diamond coverage changed')
    negative = {c for c, value in enumerate(beta) if value < 0}
    comparison_t = max(sum((v for c, v in row.items() if c in negative), F(0)) for row in matrix)
    comparison_lambda = -sum((beta[c] for c in negative), F(0))
    comparison = F(problem['B5']) - comparison_lambda/comparison_t
    require(0 <= boundary_increment <= comparison < F(problem['B5']),
            'negative-support feasible comparison envelope failed')
    result = dict(
        m5=str(boundary_increment), B5=problem['B5'],
        ri59_weighted_lower_bound='2401/450000', hook=hook_report,
        expected_delta5=problem['expected_delta5'], actual_expected_increment=str(actual_increment),
        expected_delta6=str(F(problem['expected_delta5'])+actual_increment),
        boundary_expected_delta6=str(F(problem['expected_delta5'])+boundary_increment),
        interior_expected_increment=str(interior_increment),
        boundary_contributions={k: str(v) for k, v in contributions.items()},
        actual_contributions={k: str(v) for k, v in actual_contributions.items()},
        active_boundary_components=sum(value > 0 for value in alpha),
        active_everywhere_neutral_components=len(active_neutral),
        noncritical_parent_rows=len(noncritical_rows),
        noncritical_boundary_zero_drift_rows=len(noncritical_zero_rows),
        alternative_primary_feasible=True, primary_optimum_unique=False,
        alternative_active_components=sum(value > 0 for value in proof['alternative']),
        canonical_alternative_differing_coordinates=sum(
            first != second for first, second in zip(alpha, proof['alternative'])),
        primary_positive_dual_rows=len(proof['primary_dual']),
        primary_negative_zero_slack_columns=sum(beta[c] < 0 and proof['reduced'][c] == 0
                                                for c in range(len(beta))),
        certified_positive_lex_stages=len(proof['stage_reports']),
        lex_stages_sha256=digest(proof['stage_reports']),
        boundary_full_zero_rows=sum(mass == 1 for mass in proof['masses']),
        minimum_actual_full=str(minimum_full), minimum_actual_proper=str(minimum_proper),
        maximum_suppressed_row_probability=str(maximum_suppressed),
        suppressed_birth_probability=str(suppressed_probability),
        critical_child_probability6=str(critical_child_probability),
        critical_parent_probability5=problem['critical_probability5'],
        comparison_T=str(comparison_t), comparison_Lambda=str(comparison_lambda),
        comparison_epsilon=str(comparison), actual_marked_rows=len(actual_rows),
        actual_labeled_slots=raw_slots, actual_canonical_probability_keys=len(actual_local),
        actual_raw_diamonds=actual_ratios,
        actual_probability_manifest_sha256=digest([[key, str(v)] for key, v in sorted(actual_local.items())]))
    if 'claims' in certificate:
        require(isinstance(certificate['claims'], dict) and set(certificate['claims']) <= set(result),
                'certificate claims contain unknown fields')
        require(all(canonical_json(value) == canonical_json(result[key])
                    for key, value in certificate['claims'].items()), 'certificate exact claim mismatch')
    return result


def certificate_controls(certificate, problem):
    controls = []
    def clone():
        return load_json(canonical_json(certificate))
    bad = clone()
    bad['problem_hashes']['roots'] = '0'*64
    controls.append(expect_rejection('wrong_problem_manifest',
                    lambda: check_certificate_core(bad, problem), 'certificate problem manifest mismatch'))
    bad = clone()
    first = next(item for item in problem['rows'] if item['A'])
    c, value = next(iter(first['A'].items()))
    bad['alpha'] = {c: str(2/F(value))}
    controls.append(expect_rejection('infeasible_primal', lambda: check_certificate_core(bad, problem),
                                     'primary primal row cap failure'))
    bad = clone()
    bad['alpha'] = {}
    controls.append(expect_rejection('positive_primary_gap', lambda: check_certificate_core(bad, problem),
                                     'primary exact duality gap is nonzero'))
    bad = clone()
    bad['primary_dual'] = {}
    controls.append(expect_rejection('infeasible_primary_dual', lambda: check_certificate_core(bad, problem),
                                     'primary dual feasibility failure'))
    bad = clone()
    bad['tie_break']['kind'] = 'uncertified_solver_vertex'
    controls.append(expect_rejection('missing_canonical_proof', lambda: check_certificate_core(bad, problem),
                                     'canonical tie-break proof schema mismatch'))
    bad = clone()
    bad['alpha'] = bad['alternative_primary_alpha']
    controls.append(expect_rejection('optimal_but_noncanonical_primary_vertex',
                    lambda: check_certificate_core(bad, problem),
                    'canonical positive-coordinate stages incomplete'))
    first_positive = min(map(int, certificate['alpha']))
    row_index = next(int(j) for j in certificate['primary_dual']
                     if str(first_positive) in problem['rows'][int(j)]['A'])
    value = F(problem['rows'][row_index]['A'][str(first_positive)])
    bad = clone()
    bad['tie_break']['stages'][str(first_positive)] = {
        'row_dual': {}, 'equality_dual': {str(row_index): str(2/value)}}
    controls.append(expect_rejection('infeasible_canonical_stage_dual',
                    lambda: check_certificate_core(bad, problem),
                    'canonical stage dual feasibility failure'))
    bad = clone()
    bad['tie_break']['stages'][str(first_positive)] = {'row_dual': {}, 'equality_dual': {}}
    controls.append(expect_rejection('incorrect_canonical_stage_bound',
                    lambda: check_certificate_core(bad, problem),
                    'canonical stage exact lower bound misses target'))
    bad_problem = dict(problem)
    bad_problem['rows'] = [dict(item) for item in problem['rows']]
    bad_problem['rows'][0]['pi'] = str(F(bad_problem['rows'][0]['pi'])+1)
    controls.append(expect_rejection('corrupt_history_weight',
                    lambda: verify_problem_consistency(bad_problem),
                    'complete marked-row history weights do not normalize'))
    bad_problem = dict(problem)
    bad_problem['beta'] = list(problem['beta'])
    bad_problem['beta'][0] = str(F(bad_problem['beta'][0])+1)
    controls.append(expect_rejection('corrupt_affine_objective',
                    lambda: verify_problem_consistency(bad_problem),
                    'exported affine objective differs from complete history-weighted slots'))
    controls.append(expect_rejection('duplicate_json_key', lambda: load_json('{"alpha":{},"alpha":{}}'),
                                     'duplicate JSON object key'))
    controls.append(expect_rejection('noncanonical_fraction', lambda: parse_sparse({'0':'2/2'}, 798, 'alpha'),
                                     'alpha: noncanonical fraction string'))
    controls.append(expect_rejection('boolean_index', lambda: parse_sparse({True:'1'}, 798, 'alpha'),
                                     'alpha: invalid canonical index'))
    controls.append(expect_rejection('out_of_range_index', lambda: parse_sparse({'798':'1'}, 798, 'alpha'),
                                     'alpha: invalid canonical index'))
    bad = clone()
    bad['unrecognized_instruction'] = True
    controls.append(expect_rejection('unknown_certificate_field',
                    lambda: check_certificate_core(bad, problem),
                    'certificate has missing or unknown fields'))
    return controls


def deadline_handler(signum, frame):
    raise RuntimeError('fifteen-minute wall-time alarm expired')


def main():
    require(sys.argv[1:] in ([], ['--problem']), 'unknown command arguments')
    signal.signal(signal.SIGALRM, deadline_handler)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    try:
        problem = build_problem()
        if sys.argv[1:] == ['--problem']:
            print(canonical_json(problem))
            return
        certificate = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
        proof = check_certificate_core(certificate, problem)
        result = certificate_reports(certificate, problem, proof)
        result['negative_controls'] = certificate_controls(certificate, problem)
        print('coverage=' + canonical_json(problem['counts']))
        print('certificate=' + canonical_json(result))
        print('problem_manifest_sha256=' + problem['hashes']['problem_without_self_hash'])
        print('DONE: exact first-free-layer canonical optimum and strict completion; no asymptotic verdict')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
