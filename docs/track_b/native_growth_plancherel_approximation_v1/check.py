#!/usr/bin/env python3
"""RI-75: exact cutoff-zero toy of the proposed positive approximation.

Standard library only. RI-38's maximal-deletion potential and RI-74's
embedding weight are re-expressed; no predecessor/project code is imported.
Complete natural parents stop at three, terminals at four. This is not the
actual six-event-prefix graft or an all-size proof. The separate divergent
inactive-potential row is algebraic, not asserted to realize a poset graph.
No optimizer, downloads, subprocesses, or file writes occur in this checker.
--witness emits deterministic JSON; default checks neighboring CERTIFICATE.json.
The 120-second alarm and checkpointed 512-MiB peak RSS are an audit envelope,
not a hard OS allocator cap. Explicit checks remain enabled with Python -O.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from math import factorial
from pathlib import Path
import json
import resource
import signal
import sys
import time


EPSILONS = (F(1), F(1, 2), F(1, 4))
MAX_SECONDS, MAX_BYTES = 120, 512*1024**2
START = None
EMBEDDINGS = {}
COMPLEX_PAYLOAD = ((F(2), F(0)), (F(1, 3), F(2, 5)),
                   (F(1, 3), F(-2, 5)), (F(3), F(0)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def budget(stage=None):
    require(START is None or time.monotonic()-START <= MAX_SECONDS,
            '120-second toy envelope exceeded')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require((peak if sys.platform == 'darwin' else peak*1024) <= MAX_BYTES,
            '512-MiB toy memory envelope exceeded')
    if stage:
        print('RI75: '+stage, file=sys.stderr, flush=True)


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


def epsilon_value(text):
    require(isinstance(text, str), 'epsilon must be a canonical rational string')
    try:
        value = F(text)
    except (ValueError, ZeroDivisionError):
        raise RuntimeError('epsilon must be a canonical rational string') from None
    require(str(value) == text and 0 < value <= 1, 'epsilon must be canonical and in (0,1]')
    return value


def bits(mask):
    return tuple(i for i in range(mask.bit_length()) if mask & (1 << i))


@cache
def validate(order):
    n = len(order)
    require(n <= 4 and all(type(p) is int and 0 <= p < (1 << n) and not p & (1 << v)
            and all(order[u] & p == order[u] for u in bits(p)) for v, p in enumerate(order)),
            'order outside valid terminal-four domain')


@cache
def ideals(order):
    validate(order)
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


def induced(order, keep):
    vertices = bits(keep)
    return (tuple(sum(1 << i for i, u in enumerate(vertices) if order[v] & (1 << u))
                  for v in vertices), vertices)


def restrict_mask(mask, vertices):
    return sum(1 << i for i, v in enumerate(vertices) if mask & (1 << v))


def maxima(order):
    pasts = 0
    for past in order:
        pasts |= past
    return ((1 << len(order))-1) & ~pasts


def move(mask, permutation):
    return sum(1 << permutation[v] for v in bits(mask))


def relabel(order, permutation):
    result = [0]*len(order)
    for v, past in enumerate(order):
        result[permutation[v]] = move(past, permutation)
    return tuple(result)


@cache
def node(order, part, record):
    n = len(order)
    require(n <= 3 and part in ideals(order) and type(record) is int and 0 <= record < (1 << n),
            'malformed marked local node')
    inside = record & part
    return min((sum(1 << (n*permutation[u]+permutation[v])
                    for v, past in enumerate(order) for u in bits(past)),
                move(part, permutation), move(inside, permutation))
               for permutation in permutations(range(n)))


@cache
def natural_orders(n):
    require(0 <= n <= 4, 'natural inventory exceeds four')
    if n == 0:
        return ((),)
    return tuple(sorted(p+(s,) for p in natural_orders(n-1) for s in ideals(p)))


def independent_orders(n):
    edges = tuple((u, v) for v in range(n) for u in range(v))
    result = set()
    for encoded in range(1 << len(edges)):
        p = [0]*n
        for i, (u, v) in enumerate(edges):
            if encoded & (1 << i):
                p[v] |= 1 << u
        if all(not (p[w] & (1 << v) and p[v] & (1 << u)) or p[w] & (1 << u)
               for u in range(n) for v in range(u+1, n) for w in range(v+1, n)):
            result.add(tuple(p))
    return result


def partitions(n, ceiling=None):
    if n == 0:
        yield ()
    else:
        for first in range(min(n, n if ceiling is None else ceiling), 0, -1):
            for rest in partitions(n-first, first):
                yield (first,)+rest


@cache
def extensions(order):
    if not order:
        return 1
    return sum(extensions(induced(order, ((1 << len(order))-1) ^ (1 << v))[0])
               for v in bits(maxima(order)))


def build_target():
    inventory = []
    for n in range(5):
        require(set(natural_orders(n)) == independent_orders(n), 'independent natural-order coverage mismatch')
        embeddings = {}
        for partition in partitions(n):
            cells = tuple((i, j) for i, length in enumerate(partition) for j in range(length))
            p = tuple(sum(1 << u for u, (a, b) in enumerate(cells)
                          if a <= i and b <= j and (a, b) != (i, j)) for i, j in cells)
            for permutation in permutations(range(n)):
                q = relabel(p, permutation)
                embeddings[q] = embeddings.get(q, 0)+1
        EMBEDDINGS[n] = embeddings
        inventory.append(dict(size=n, natural_orders=len(natural_orders(n)),
                              ferrers_natural_orders=sum(p in embeddings for p in natural_orders(n)),
                              embedding_manifest=digest([[p, b] for p, b in sorted(embeddings.items())])))
    return inventory


def weight(order):
    return F(EMBEDDINGS[len(order)].get(order, 0)*extensions(order), factorial(len(order)))


@cache
def target_row(order, record):
    n, full = len(order), (1 << len(order))-1
    require(n <= 3 and type(record) is int and 0 <= record < (1 << n), 'target row outside toy domain')
    if weight(order):
        result = {s: weight(order+(s,))/weight(order) for s in ideals(order)}
    else:
        result = {s: F(int(s == full)) for s in ideals(order)}
    verify_row(order, result, strict=False)
    return result


def verify_row(order, row, strict):
    require(set(row) == set(ideals(order)) and sum(row.values(), F(0)) == 1,
            'complete labeled-ideal row does not normalize')
    require(all(q > 0 if strict else q >= 0 for q in row.values()), 'row probability sign failure')


def potential(order, part, record, old_row):
    require(part in ideals(order) and part != (1 << len(order))-1, 'potential requires a proper ideal')
    omitted = maxima(order) & ~part
    require(omitted, 'proper ideal omits no maximal vertex')
    value, deleted = F(1), omitted
    while deleted:
        smaller, vertices = induced(order, ((1 << len(order))-1) ^ deleted)
        s = restrict_mask(part, vertices)
        r = restrict_mask(record & part, vertices)
        factor = old_row(smaller, r)[s]
        require(factor > 0, 'potential factor is not positive')
        value = value*factor if deleted.bit_count() % 2 else value/factor
        deleted = (deleted-1) & omitted
    return value


class Components:
    def __init__(self, keys):
        self.parent = {k: k for k in keys}

    def root(self, key):
        while self.parent[key] != key:
            self.parent[key] = self.parent[self.parent[key]]
            key = self.parent[key]
        return key

    def join(self, a, b):
        low, high = sorted((self.root(a), self.root(b)))
        self.parent[high] = low


def active_check(order, part, active):
    require(active == bool(weight(order+(part,))), 'terminal-based active classification mismatch')


def structural_layer(n):
    slots, meta = [], {}
    for p in natural_orders(n):
        for r in range(1 << n):
            for s in ideals(p):
                if s == (1 << n)-1:
                    continue
                key, active = node(p, s, r), bool(weight(p+(s,)))
                active_check(p, s, active)
                require(key not in meta or meta[key] == active, 'local quotient changes active terminal type')
                meta[key] = active
                slots.append((p, r, s, key))
    graph, edges = Components(meta), []
    for base in natural_orders(n-1):
        for r in range(1 << (n-1)):
            for s in ideals(base):
                for t in ideals(base):
                    for b in (0, 1):
                        for h in (0, 1):
                            i = node(base+(s,), t, r | (b << (n-1)))
                            j = node(base+(t,), s, r | (h << (n-1)))
                            require(i in meta and j in meta and meta[i] == meta[j],
                                    'structural diamond changes terminal component activity')
                            graph.join(i, j)
                            edges.append((base, r, s, t, b, h, i, j))
    roots = sorted({graph.root(k) for k in meta})
    index = {k: roots.index(graph.root(k)) for k in meta}
    return dict(slots=slots, meta=meta, edges=edges, roots=roots, component=index)


def scales(epsilon, n, sums_h, sums_u):
    t, b, m = epsilon/F((n+1)**2), max(sums_h), max(sums_u)
    return t, b, m, (1-t)/max(F(1), b), t/(2*(1+m))


def verify_floor(t, tau, total_u):
    require(tau > 0 and tau*total_u < t/2, 'inactive-inclusive floor mass bound failed')


def sharp_bound(e, b, t):
    return min(F(1), e+max(b-1, F(0))+t*min(b, F(1))+t/2)


def verify_error_bound(d, e, t, b):
    require(0 <= d <= min(F(1), 2*e+3*t/2), 'finite-layer total-variation envelope failed')
    require(d <= sharp_bound(e, b, t), 'finite-layer sharp total-variation envelope failed')


def verify_payload_products(left, right):
    # Four complex Hermitian entries, on the unnormalized cone. This one
    # witness supplements the scalar identity; it does not prove all carriers.
    first = tuple((left*real/4, left*imag/4) for real, imag in COMPLEX_PAYLOAD)
    second = tuple((right*real/4, right*imag/4) for real, imag in COMPLEX_PAYLOAD)
    require(first == second, 'full complex-payload diamond failure')


def construct(epsilon, structures):
    tables = {0: {}}
    def row(p, r):
        n, full = len(p), (1 << len(p))-1
        require(n in tables and type(r) is int and 0 <= r < (1 << n), 'toy row used before construction')
        q = {s: tables[n][node(p, s, r)] for s in ideals(p) if s != full}
        q[full] = 1-sum(q.values(), F(0))
        return q
    reports = [dict(parent_size=0, maximum_row_tv='0', row_bound='0', sharp_row_bound='0')]
    for n in range(1, 4):
        budget()
        structural = structures[n]
        values, hvalues, a0 = {}, {}, {}
        component_a0 = {}
        for p, r, s, key in structural['slots']:
            u = potential(p, s, r, row)
            active = structural['meta'][key]
            coefficient = target_row(p, r)[s]/potential(p, s, r, target_row) if active else F(0)
            require((coefficient > 0) == active, 'active coefficient has wrong support')
            c = structural['component'][key]
            require(c not in component_a0 or component_a0[c] == coefficient,
                    'target coefficient is not constant on complete component')
            component_a0[c] = coefficient
            require(key not in values or values[key] == u, 'potential violates local quotient')
            values[key], a0[key], hvalues[key] = u, coefficient, coefficient*u
        for base, r, s, t, b, h, i, j in structural['edges']:
            old = row(base, r)
            require(old[s]*values[i] == old[t]*values[j], 'structural potential diamond failure')
            require(a0[i] == a0[j], 'component scale changes across retained raw edge')
        sums_h, sums_u, errors = [], [], []
        for p in natural_orders(n):
            for r in range(1 << n):
                keys = [(s, node(p, s, r)) for s in ideals(p) if s != (1 << n)-1]
                sums_h.append(sum((hvalues[k] for s, k in keys), F(0)))
                sums_u.append(sum((values[k] for s, k in keys), F(0)))
                errors.append(sum((abs(hvalues[k]-target_row(p, r)[s]) for s, k in keys), F(0)))
        t, bmax, mmax, lam, tau = scales(epsilon, n, sums_h, sums_u)
        tables[n] = {k: lam*hvalues[k]+tau*values[k] for k in values}
        row_manifest, ds, minimum_full, minimum_proper = [], [], F(1), F(1)
        locality = equivariance = 0
        for p in natural_orders(n):
            for r in range(1 << n):
                q, target = row(p, r), target_row(p, r)
                verify_row(p, q, strict=True)
                full = (1 << n)-1
                require(q[full] > t/2, 'strict full complement bound failed')
                verify_floor(t, tau, sum(values[node(p, s, r)] for s in ideals(p) if s != full))
                minimum_full = min(minimum_full, q[full])
                minimum_proper = min(minimum_proper, *(q[s] for s in q if s != full))
                ds.append(sum((abs(q[s]-target[s]) for s in q), F(0))/2)
                row_manifest.append([p, r, [[s, str(v)] for s, v in q.items()]])
                for s in ideals(p):
                    for other in range(1 << n):
                        if other & s == r & s:
                            require(row(p, other)[s] == q[s], 'precursor record-locality failure')
                            locality += 1
                for permutation in permutations(range(n)):
                    transported = row(relabel(p, permutation), move(r, permutation))
                    require(transported == {move(s, permutation): v for s, v in q.items()},
                            'full marked-parent equivariance failure')
                    equivariance += len(q)
        payload_diamonds = 0
        for base, r, s, u, b, h, i, j in structural['edges']:
            old = row(base, r)
            left = old[s]*row(base+(s,), r | (b << (n-1)))[u]
            right = old[u]*row(base+(u,), r | (h << (n-1)))[s]
            require(left == right, 'strict full scalar-map diamond failure')
            verify_payload_products(left, right)
            payload_diamonds += 1
            perm = tuple(range(n-1))+(n, n-1)
            terminal = base+(s, u)
            marks = r | (b << (n-1)) | (h << n)
            require(relabel(terminal, perm) == base+(u, s)
                    and move(marks, perm) == r | (h << (n-1)) | (b << n),
                    'terminal order/newborn record transport failure')
        d, e = max(ds), max(errors)
        verify_error_bound(d, e, t, bmax)
        reports.append(dict(parent_size=n, B=str(bmax), M=str(mmax), t=str(t),
                            lambda_scale=str(lam), tau=str(tau), e=str(e), maximum_row_tv=str(d),
                            row_bound=str(min(F(1), 2*e+3*t/2)), sharp_row_bound=str(sharp_bound(e, bmax, t)),
                            minimum_full=str(minimum_full),
                            minimum_proper=str(minimum_proper), marked_rows=len(row_manifest),
                            labeled_slots=sum(len(item[2]) for item in row_manifest),
                            locality_comparisons=locality, equivariance_comparisons=equivariance,
                            raw_scalar_diamonds=len(structural['edges']),
                            full_payload_diamonds=payload_diamonds,
                            maximum_floor_mass=str(tau*mmax),
                            component_coefficients=[str(component_a0[c]) for c in range(len(structural['roots']))],
                            potential_manifest=digest([[k, str(values[k]), str(hvalues[k])] for k in sorted(values)]),
                            row_manifest=digest(row_manifest)))
    @cache
    def history(p, r, target):
        if not p:
            return F(1)
        old_r = r & ((1 << (len(p)-1))-1)
        q = target_row(p[:-1], old_r) if target else row(p[:-1], old_r)
        return history(p[:-1], old_r, target)*q[p[-1]]/2
    histories = []
    for size in range(5):
        pairs = [(history(p, r, False), history(p, r, True))
                 for p in natural_orders(size) for r in range(1 << size)]
        require(sum(a for a, b in pairs) == sum(b for a, b in pairs) == 1,
                'complete marked histories do not normalize')
        tv = sum((abs(a-b) for a, b in pairs), F(0))/2
        bound = min(F(1), sum((F(item['row_bound']) for item in reports[:size]), F(0)))
        sharp_sum = min(F(1), sum((F(item['sharp_row_bound']) for item in reports[:size]), F(0)))
        survival = F(1)
        for item in reports[:size]:
            survival *= 1-F(item['sharp_row_bound'])
        require(tv <= bound, 'finite-history coupling bound failed')
        require(tv <= 1-survival <= sharp_sum, 'finite-history sharp product coupling bound failed')
        histories.append(dict(size=size, marked_histories=len(pairs), target_positive=sum(b > 0 for a, b in pairs),
                              approximation_positive=sum(a > 0 for a, b in pairs), tv=str(tv), bound=str(bound),
                              sharp_sum_bound=str(sharp_sum), sharp_product_bound=str(1-survival),
                              history_manifest=digest([[str(a), str(b)] for a, b in pairs])))
    return dict(epsilon=str(epsilon), layers=reports, finite_histories=histories)


def synthetic(epsilon, active_u=1):
    # This is deliberately not passed to the poset graph constructor.
    u, a0 = (F(active_u), 1/epsilon), (F(1, 2), F(0))
    h = tuple(x*y for x, y in zip(u, a0))
    t, b, m, lam, tau = scales(epsilon, 1, [sum(h)], [sum(u)])
    q = tuple(lam*x+tau*y for x, y in zip(h, u))
    full = 1-sum(q)
    require(all(x > 0 for x in q) and full > t/2 and epsilon*u[1] == 1,
            'synthetic algebraic row admission failure')
    verify_floor(t, tau, sum(u))
    target = (F(1, 2), F(0))
    d = (sum(abs(q[i]-target[i]) for i in range(2))+abs(full-F(1, 2)))/2
    e = sum(abs(h[i]-target[i]) for i in range(2))
    verify_error_bound(d, e, t, b)
    require((b > 1) == (active_u == 3), 'synthetic cap branch not exercised')
    return dict(epsilon=str(epsilon), poset_realization_claimed=False,
                purpose='inactive_divergence' if active_u == 1 else 'cap_branch_stress_not_convergence',
                u=list(map(str, u)), e=str(e),
                a0=list(map(str, a0)), B=str(b), M=str(m), t=str(t), lambda_scale=str(lam),
                tau=str(tau), proper=list(map(str, q)), full=str(full),
                inactive_floor_mass=str(tau*u[1]), total_floor_mass=str(tau*sum(u)), tv=str(d))


def verify_certificate(candidate, expected):
    require(isinstance(candidate, dict) and set(candidate) == set(expected)
            and candidate.get('schema') == expected['schema'], 'certificate schema mismatch')
    require(candidate['source_sha256'] == expected['source_sha256'], 'certificate source identity mismatch')
    require(canonical(candidate) == canonical(expected), 'certificate exact toy witness mismatch')


def rejection(name, function, reason):
    try:
        function()
    except RuntimeError as error:
        require(str(error) == reason, name+': wrong refusal reason')
        return name
    raise RuntimeError(name+': malformed input accepted')


def controls(witness):
    results = [rejection('zero_epsilon', lambda: epsilon_value('0'), 'epsilon must be canonical and in (0,1]'),
               rejection('noncanonical_epsilon', lambda: epsilon_value('2/2'), 'epsilon must be canonical and in (0,1]'),
               rejection('nonideal_local_node', lambda: node((0, 1), 2, 0), 'malformed marked local node'),
               rejection('parent_instead_of_terminal_activity', lambda: active_check((0, 1), 0, True), 'terminal-based active classification mismatch'),
               rejection('zero_target_denominator', lambda: potential((0, 0), 0, 0, target_row), 'potential factor is not positive'),
               rejection('missing_divergent_floor_denominator', lambda: verify_floor(F(1, 16), F(1, 32), F(5)), 'inactive-inclusive floor mass bound failed'),
               rejection('wrong_row_tv_envelope', lambda: verify_error_bound(F(1), F(0), F(1, 16), F(0)), 'finite-layer total-variation envelope failed'),
               rejection('overscope_parent_inventory', lambda: natural_orders(5), 'natural inventory exceeds four'),
               rejection('duplicate_json_key', lambda: load_json('{"a":0,"a":1}'), 'duplicate JSON object key')]
    bad_row = dict(target_row((0, 1, 1), 0)); del bad_row[5]
    results.append(rejection('dropped_labeled_arm', lambda: verify_row((0, 1, 1), bad_row, False),
                             'complete labeled-ideal row does not normalize'))
    bad = load_json(canonical(witness)); bad['source_sha256'] = '0'*64
    results.append(rejection('changed_source_identity', lambda: verify_certificate(bad, witness), 'certificate source identity mismatch'))
    bad = load_json(canonical(witness)); bad['approximations'][0]['layers'][1]['M'] = '999'
    results.append(rejection('changed_complete_layer_maximum', lambda: verify_certificate(bad, witness), 'certificate exact toy witness mismatch'))
    bad = load_json(canonical(witness)); bad['unknown'] = True
    results.append(rejection('unknown_certificate_field', lambda: verify_certificate(bad, witness), 'certificate schema mismatch'))
    return results


def deadline(signum, frame):
    raise RuntimeError('120-second toy wall-time alarm expired')


def main():
    global START
    require(sys.argv[1:] in ([], ['--witness']), 'unknown command arguments')
    START = time.monotonic()
    signal.signal(signal.SIGALRM, deadline)
    signal.setitimer(signal.ITIMER_REAL, MAX_SECONDS)
    source = Path(__file__).read_bytes()
    try:
        budget('constructing complete cutoff-zero toy through parent three only')
        inventory = build_target()
        structures = {n: structural_layer(n) for n in range(1, 4)}
        graph_reports = []
        for n, data in structures.items():
            for p, r, s, t, b, h, i, j in data['edges']:
                old = target_row(p, r)
                left = old[s]*target_row(p+(s,), r | (b << len(p)))[t]
                right = old[t]*target_row(p+(t,), r | (h << len(p)))[s]
                require(left == right, 'complete zero-aware target diamond failure')
                verify_payload_products(left, right)
            graph_reports.append(dict(parent_size=n, raw_proper_slots=len(data['slots']), nodes=len(data['meta']),
                                      components=len(data['roots']), active_components=len({data['component'][k] for k, a in data['meta'].items() if a}),
                                      raw_edges=len(data['edges']), equal_precursors=sum(s == t for p, r, s, t, b, h, i, j in data['edges']),
                                      target_full_payload_diamonds=len(data['edges']),
                                      loops=sum(i == j for p, r, s, t, b, h, i, j in data['edges']),
                                      all_zero_marks=sum(r == b == h == 0 for p, r, s, t, b, h, i, j in data['edges']),
                                      zero_target_edges=sum(target_row(p, r)[s]*target_row(p+(s,), r | (b << len(p)))[t] == 0
                                                            for p, r, s, t, b, h, i, j in data['edges']),
                                      node_manifest=digest([[k, a, data['component'][k]] for k, a in sorted(data['meta'].items())]),
                                      edge_manifest=digest(data['edges'])))
        target_manifest = [[p, r, [[s, str(q)] for s, q in target_row(p, r).items()]]
                           for n in range(4) for p in natural_orders(n) for r in range(1 << n)]
        witness = dict(schema='ri75-plancherel-approximation-toy-v1', source_sha256=sha256(source).hexdigest(),
                       finite_domain=dict(cutoff=0, parent_maximum=3, terminal_maximum=4,
                                          actual_six_event_prefix_evaluated=False, optimizer_calls=0,
                                          all_size_claim_from_enumeration=False, adopted_law=False),
                       inventory=inventory, structural_graphs=graph_reports,
                       complex_payload=[[str(real), str(imag)] for real, imag in COMPLEX_PAYLOAD],
                       target_row_manifest=digest(target_manifest),
                       approximations=[construct(epsilon_value(str(eps)), structures) for eps in EPSILONS],
                       synthetic_rows=[synthetic(eps, active_u) for active_u in (1, 3) for eps in EPSILONS])
        negative = controls(witness)
        require(Path(__file__).read_bytes() == source, 'checker source changed during execution')
        budget('exact bounded toy and explicitly synthetic row complete')
        if sys.argv[1:] == ['--witness']:
            print(canonical(witness))
        else:
            candidate = load_json(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
            verify_certificate(candidate, witness)
            print('structural_graphs='+canonical(graph_reports))
            print('finite_histories='+canonical([{k: v for k, v in item.items() if k != 'layers'} for item in witness['approximations']]))
            print('negative_controls='+canonical(negative))
            print('witness_sha256='+digest(witness))
            print('DONE: exact cutoff-zero toy only; no actual parent-six calculation or fixed-epsilon asymptotic verdict')
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == '__main__':
    main()
