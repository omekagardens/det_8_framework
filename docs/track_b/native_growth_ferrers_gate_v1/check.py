#!/usr/bin/env python3
"""RI-52: exact fixed-prefix Ferrers admission matrix and certificate check.

Standard library only. No project imports, downloads or writes. Prefix helper
formulas and RI-41 coefficient data are re-expressed from the accepted RI-45
standalone checker; its executor is neither imported nor run. Only parent sizes
0..4 are fully enumerated. At size five only the four declared Ferrers orders
are used, with their full binary record cubes. Six-vertex orders are used only
for shape classification and the four proper-target child ratio graphs.

--matrix prints the exact target matrix to stdout for separate discovery; this
is not an optimization or an admission verdict.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


@cache
def ideals(order):
    return tuple(s for s in range(1 << len(order))
                 if all(order[v] & s == order[v] for v in bits(s)))


@cache
def prefix_parents(n):
    require(0 <= n <= 4, "full parent enumeration is capped at four")
    if n == 0:
        return ((),)
    return tuple(p + (s,) for p in prefix_parents(n - 1) for s in ideals(p))


@cache
def depths(order):
    result = []
    for past in order:
        result.append(1 + max((result[v] for v in bits(past)), default=0))
    return tuple(result)


def height(order, part=None):
    # Restricted use is only on ideals, where inherited depths are correct.
    if part is None:
        return max(depths(order), default=0)
    require(part in ideals(order), "height restriction is not an ideal")
    return max((depths(order)[v] for v in bits(part)), default=0)


@cache
def permutations_of(n):
    require(0 <= n <= 6, "canonicalization outside declared size range")
    return tuple(permutations(range(n)))


@cache
def layout(order, part):
    n = len(order)
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
    pair, candidates = layout(order, part)
    inside = record & part
    return pair + (min(sum(1 << perm[v] for v in bits(inside))
                       for perm in candidates),)


def row_key(order, record):
    return node(order, (1 << len(order)) - 1, record)


def shape_key(order):
    return layout(order, 0)[0][0]


def maximal_mask(order):
    ancestors = 0
    for past in order:
        ancestors |= past
    return ((1 << len(order)) - 1) & ~ancestors


A, C, D = F(2, 3), F(1, 5), F(1, 4)
FS = (F(1, 6), F(1, 3))
G, K = F(1, 10), F(11, 20)
HS, E = (F(19, 30), F(7, 15)), F(1, 44)

# Exact RI-41 coefficients and canonical roots, copied as data, not imported.
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
    (2186,7,4),(2186,7,5),(2186,7,6),(2186,7,7),(2190,7,0),(2190,7,1),(2190,7,2),
    (2190,7,3),(2190,7,6),(2190,7,7),(2252,7,0),(2252,7,1),(2252,7,3),(2252,7,4),
    (2252,7,5),(2252,7,7),(2254,7,0),(2254,7,1),(2254,7,2),(2254,7,3),(2254,7,4),
    (2254,7,5),(2254,7,6),(2254,7,7)
)
COEFFICIENTS4 = {}
PREFIX_PARAMETER_SHA256 = '465c5de48c69527fc59e8df1f494fd8cea33f8aec243f59b9b2820bd5b1c07a7'
RI41_CERTIFICATE_SHA256 = '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969'


@cache
def row(order, record):
    n, full = len(order), (1 << len(order)) - 1
    require(n <= 4, "prefix lookup above parent four")
    if n == 0:
        return {0:F(1)}
    if n == 1:
        return {0:A, full:1-A}
    edge_count = sum(p.bit_count() for p in order)
    if n == 2:
        if edge_count:
            return {0:C, 1:FS[record & 1], full:HS[record & 1]}
        return {0:D, 1:G, 2:G, full:K}
    if n == 3:
        result = {s:E for s in ideals(order) if s != full}
        if edge_count == 0:
            for s in result:
                if s.bit_count() == 1:
                    result[s] *= G/D
                elif s.bit_count() == 2:
                    result[s] *= K/D
        elif edge_count == 1:
            tip = next(v for v,past in enumerate(order) if past)
            root = next(bits(order[tip]))
            isolated = next(v for v in range(3) if v not in (root,tip))
            bit = (record >> root) & 1
            result[1 << root] *= FS[bit]/C
            result[(1 << root)|(1 << tip)] *= HS[bit]/C
            result[(1 << root)|(1 << isolated)] *= K/G
        elif edge_count == 2:
            roots = [v for v in range(3) if sum(bool(p & (1 << v)) for p in order) == 2]
            if roots:
                bit = (record >> roots[0]) & 1
                for s in result:
                    if s.bit_count() == 2:
                        result[s] *= HS[bit]/FS[bit]
    else:
        require(COEFFICIENTS4, "RI-41 table used before reconstruction")
        result = {s:COEFFICIENTS4[node(order,s,record)] * potential(order,s,record & s)
                  for s in ideals(order) if s != full}
    result[full] = 1 - sum(result.values(), F(0))
    require(all(q > 0 for q in result.values()), "nonpositive fixed prefix row")
    require(sum(result.values(), F(0)) == 1, "fixed prefix normalization failure")
    return result


@cache
def restriction(order, keep):
    surviving = tuple(bits(keep))
    remap = {v:i for i,v in enumerate(surviving)}
    induced = tuple(sum(1 << remap[u] for u in bits(order[v] & keep)) for v in surviving)
    return induced, surviving


def transport(mask, surviving):
    return sum(1 << i for i,v in enumerate(surviving) if mask & (1 << v))


@cache
def potential(order, part, inside_record):
    n, full = len(order), (1 << len(order))-1
    require(n in (4,5) and part in ideals(order) and part != full,
            "potential outside declared proper-slot domain")
    omitted = maximal_mask(order) & ~part
    require(omitted, "proper ideal omitted no maximal vertex")
    result, deleted = F(1), omitted
    while deleted:
        smaller, surviving = restriction(order, full ^ deleted)
        s, r = transport(part,surviving), transport(inside_record,surviving)
        factor = row(smaller,r)[s]
        result = result*factor if deleted.bit_count()%2 else result/factor
        deleted = (deleted-1) & omitted
    require(result > 0, "nonpositive maximal-deletion potential")
    return result


class Components:
    def __init__(self, keys):
        self.parent = {key:key for key in keys}

    def root(self, key):
        trail = []
        while self.parent[key] != key:
            trail.append(key)
            key = self.parent[key]
        for item in trail:
            self.parent[item] = key
        return key

    def join(self, first, second):
        low, high = sorted((self.root(first),self.root(second)))
        self.parent[high] = low

    def finish(self):
        roots = sorted({self.root(key) for key in self.parent})
        numbers = {key:i for i,key in enumerate(roots)}
        return roots, {key:numbers[self.root(key)] for key in self.parent}


def reconstruct_prefix():
    seed_data = dict(roots=ROOTS4,default_alpha='1/8',
                     overrides={str(k):v for k,v in OVERRIDES4.items()})
    seed_bytes = (json.dumps(seed_data,sort_keys=True,separators=(',',':'))+'\n').encode()
    require(sha256(seed_bytes).hexdigest() == PREFIX_PARAMETER_SHA256,
            "embedded RI-41 data pin mismatch")
    require(tuple(len(prefix_parents(n)) for n in range(5)) == (1,1,2,7,40),
            "fixed-prefix natural enumeration changed")
    values, proper_count = {}, 0
    for order in prefix_parents(4):
        for record in range(16):
            for part in ideals(order):
                if part == 15:
                    continue
                key, u = node(order,part,record), potential(order,part,record & part)
                require(key not in values or values[key] == u, "prefix quotient potential mismatch")
                values[key] = u
                proper_count += 1
    graph = Components(values)
    edges = zeros = equals = loops = 0
    raw_ratios = []
    for base in prefix_parents(3):
        for record in range(8):
            old = row(base,record)
            for first in ideals(base):
                for second in ideals(base):
                    for b in (0,1):
                        for h in (0,1):
                            i = node(base+(first,),second,record|(b << 3))
                            j = node(base+(second,),first,record|(h << 3))
                            require(old[first]*values[i] == old[second]*values[j],
                                    "fixed-prefix potential ratio failure")
                            raw_ratios.append((old[first],old[second],i,j))
                            graph.join(i,j)
                            edges += 1
                            zeros += int(record == b == h == 0)
                            equals += int(first == second)
                            loops += int(i == j)
    roots, component = graph.finish()
    require(tuple(roots) == ROOTS4, "fixed RI-41 canonical components changed")
    for key,c in component.items():
        COEFFICIENTS4[key] = F(OVERRIDES4.get(c,'1/8'))
    for first,second,i,j in raw_ratios:
        require(first*COEFFICIENTS4[i]*values[i] == second*COEFFICIENTS4[j]*values[j],
                "reconstructed RI-41 scalar-map ratio failure")
    lower_ratios = fixed_rows = fixed_slots = 0
    canonical_probabilities = {}
    for n in range(5):
        for order in prefix_parents(n):
            for record in range(1 << n):
                q = row(order,record)
                require(set(q) == set(ideals(order)) and all(v > 0 for v in q.values())
                        and sum(q.values(),F(0)) == 1, "fixed row domain/strictness/normalization failure")
                fixed_rows += 1
                for part,value in q.items():
                    key = (n,node(order,part,record))
                    require(key not in canonical_probabilities or canonical_probabilities[key] == value,
                            "fixed row violates its marked-local canonical quotient")
                    canonical_probabilities[key] = value
                    fixed_slots += 1
    for n in range(3):
        for base in prefix_parents(n):
            for record in range(1 << n):
                old = row(base,record)
                for first in ideals(base):
                    for second in ideals(base):
                        for b in (0,1):
                            for h in (0,1):
                                left = old[first]*row(base+(first,),record|(b << n))[second]
                                right = old[second]*row(base+(second,),record|(h << n))[first]
                                require(left == right, "lower fixed-prefix scalar-map ratio failure")
                                lower_ratios += 1
    full_min, tau_max, slot_min = F(1), F(0), F(1)
    for order in prefix_parents(4):
        for record in range(16):
            q = row(order,record)
            full_min = min(full_min,q[15])
            slot_min = min(slot_min,*q.values())
            tau_max = max(tau_max,sum((v for s,v in q.items() if height(order,s)==height(order)),F(0)))
    require((full_min,tau_max,slot_min) == (F(33901019,474368400),F(14082809,29648025),F(9,681472)),
            "fixed RI-41 probabilities changed")
    return dict(parents=40,rows=640,proper=proper_count,nodes=len(values),components=len(roots),
                edges=edges,all_zero=zeros,equal=equals,loops=loops,
                minimum_full=str(full_min),maximum_height_drift=str(tau_max),minimum_slot=str(slot_min),
                lower_raw_ratios=lower_ratios,fixed_rows_through_four=fixed_rows,
                fixed_slots_through_four=fixed_slots,canonical_probability_keys=len(canonical_probabilities))


def partitions(total, ceiling=None):
    if total == 0:
        yield ()
        return
    if ceiling is None:
        ceiling = total
    for first in range(min(total,ceiling),0,-1):
        for tail in partitions(total-first,first):
            yield (first,)+tail


def ferrers(partition):
    require(sum(partition) in (5,6) and all(x > 0 for x in partition)
            and tuple(sorted(partition,reverse=True)) == partition, "invalid Ferrers shape")
    cells = tuple((i,j) for i,length in enumerate(partition) for j in range(length))
    return tuple(sum(1 << u for u,(k,l) in enumerate(cells) if k <= i and l <= j and (k,l)!=(i,j))
                 for i,j in cells)


PARENTS5 = {'5':(5,), '41':(4,1), '311':(3,1,1), '32':(3,2)}
CHILDREN6 = {'6':(6,), '51':(5,1), '42':(4,2), '411':(4,1,1),
             '33':(3,3), '321':(3,2,1)}
TARGETS6 = ('51','42','411','321')


def shape_inventory():
    inventory, maps = {}, {}
    for n,reps,expected in ((5,PARENTS5,7),(6,CHILDREN6,11)):
        mapping = {shape_key(ferrers(partition)):name for name,partition in reps.items()}
        require(len(mapping) == len(reps), "proposed shape representatives are isomorphic")
        all_parts = tuple(partitions(n))
        require(len(all_parts) == expected, "integer partition coverage changed")
        rows = []
        for partition in all_parts:
            key = shape_key(ferrers(partition))
            require(key in mapping, "Ferrers order missing from proposed shape list")
            rows.append(dict(partition=partition,shape=mapping[key],key=key))
        inventory[str(n)] = rows
        maps[n] = mapping
    return inventory,maps


def target_matrix():
    inventory,maps = shape_inventory()
    values, child_class, raw_rows = {}, {}, []
    target_slots = other_slots = full_good = 0
    slot_inventory = {}
    for name,partition in PARENTS5.items():
        order = ferrers(partition)
        target_parts, other_parts = {}, []
        for part in ideals(order):
            child = order+(part,)
            child_name = maps[6].get(shape_key(child))
            if part == 31:
                expected = {'5':'6','32':'33'}.get(name)
                require(child_name == expected, "full-birth Ferrers boundary classification changed")
                good_full = child_name is not None
            elif child_name is not None:
                require(child_name in TARGETS6, "a proper birth reached a rectangle")
                target_parts[part] = child_name
            else:
                other_parts.append(part)
        slot_inventory[name] = dict(past_masks=order,target_parts=target_parts,
                                   other_parts=other_parts,full_is_ferrers=good_full)
        for record in range(32):
            entries = []
            for part,child_name in target_parts.items():
                key, u = node(order,part,record), potential(order,part,record & part)
                require(key not in values or values[key] == u, "target local quotient potential mismatch")
                require(key not in child_class or child_class[key] == child_name,
                        "local key changed its terminal unmarked shape")
                values[key], child_class[key] = u,child_name
                entries.append((key,u,part))
                target_slots += 1
            other_slots += len(other_parts)
            full_good += int(good_full)
            raw_rows.append((name,order,record,not good_full,entries))
    graph, covered = Components(values), set()
    edges = zeros = equal_precursors = loops = 0
    deletion_inventory, edge_by_shape, raw_ratios = {}, {}, []
    for name in TARGETS6:
        child = ferrers(CHILDREN6[name])
        maxima = tuple(bits(maximal_mask(child)))
        require(len(maxima) >= 2, "proper Ferrers child has only one maximum")
        deletions = []
        for x in maxima:
            parent,surviving = restriction(child,63 ^ (1 << x))
            part = transport(child[x],surviving)
            require(part != 31, "target child has a full incoming role")
            deletions.append(dict(vertex=x,parent=maps[5][shape_key(parent)],past_mask=part))
        deletion_inventory[name] = deletions
        shape_edges = 0
        for record in range(64):
            for x in maxima:
                for y in maxima:
                    if x == y:
                        continue
                    base,surviving = restriction(child,63 ^ (1 << x) ^ (1 << y))
                    require(base in prefix_parents(4), "deletion base is not a natural prefix order")
                    first,second = transport(child[x],surviving),transport(child[y],surviving)
                    r = transport(record,surviving)
                    b,h = (record >> x) & 1,(record >> y) & 1
                    p,q = base+(first,),base+(second,)
                    i,j = node(p,second,r|(b << 4)),node(q,first,r|(h << 4))
                    require(i in values and j in values, "target graph edge escaped the target rows")
                    require(child_class[i] == child_class[j] == name, "raw edge changed child shape")
                    ui,uj = potential(p,second,(r|(b << 4)) & second),potential(q,first,(r|(h << 4)) & first)
                    require(values[i] == ui and values[j] == uj, "transported parent potential changed")
                    old = row(base,r)
                    require(old[first]*ui == old[second]*uj, "restricted full-map scalar ratio failure")
                    raw_ratios.append((old[first],old[second],i,j))
                    graph.join(i,j)
                    covered.update((i,j))
                    edges += 1
                    shape_edges += 1
                    zeros += int(record == 0)
                    equal_precursors += int(first == second)
                    loops += int(i == j)
        edge_by_shape[name] = shape_edges
    require(covered == set(values), "target node omitted from maximal-deletion graph")
    roots,component = graph.finish()
    classes = [child_class[key] for key in roots]
    for key,c in component.items():
        require(child_class[key] == classes[c], "component crosses terminal shape")
    unique_rows = {}
    for name,order,record,equality,entries in raw_rows:
        a = {}
        for key,u,part in entries:
            c = component[key]
            a[c] = a.get(c,F(0))+u
        key = row_key(order,record)
        item = (name,equality,a)
        require(key not in unique_rows or unique_rows[key][0] == item,
                "marked-parent quotient changed labeled ideal multiplicities")
        unique_rows[key] = (item,order,record)
    rows = [dict(key=key,shape=item[0],equality=item[1],past_masks=order,record=record,
                 A={str(c):str(v) for c,v in sorted(item[2].items())})
            for key,(item,order,record) in sorted(unique_rows.items())]
    counts = dict(parent_types=4,marked_parent_rows=len(raw_rows),target_proper_slots=target_slots,
                  other_proper_slots=other_slots,full_ferrers_rows=full_good,
                  nodes=len(values),components=len(roots),raw_ratios=edges,all_zero=zeros,
                  equal_precursors=equal_precursors,loops=loops,marked_row_classes=len(rows),
                  marked_child_completions=64*len(TARGETS6),ratios_by_shape=edge_by_shape)
    matrix = dict(counts=counts,roots=roots,classes=classes,rows=rows,shape_inventory=inventory,
                  slot_inventory=slot_inventory,maximal_deletions=deletion_inventory)
    evidence = dict(raw_rows=raw_rows,raw_ratios=raw_ratios,component=component,values=values)
    return matrix,evidence


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def check_boundary(matrix, coefficients):
    require(len(coefficients) == len(matrix['roots']) and all(v >= 0 for v in coefficients),
            "boundary coefficients are not nonnegative")
    masses = []
    for item in matrix['rows']:
        mass = sum((F(value)*coefficients[int(c)] for c,value in item['A'].items()),F(0))
        require(mass <= 1, "boundary row sum exceeds one")
        if item['equality']:
            require(mass == 1, "boundary equality failed")
        masses.append(mass)
    return masses


def check_certificate(certificate, matrix, evidence):
    require(certificate['schema'] == 'ri52-ferrers-primal-v1' and certificate['parent_size'] == 5,
            "certificate domain mismatch")
    require(certificate['fixed_prefix_parameter_json_sha256'] == PREFIX_PARAMETER_SHA256
            and certificate['ri41_certificate_source_sha256'] == RI41_CERTIFICATE_SHA256,
            "certificate prefix provenance mismatch")
    require(certificate['prefix_counts'] == matrix['prefix_counts'], "prefix coverage manifest mismatch")
    require(certificate['target_counts'] == matrix['counts'], "target coverage manifest mismatch")
    manifest = certificate['canonical_components']
    require(tuple(map(tuple,manifest['roots'])) == tuple(matrix['roots'])
            and manifest['roots_sha256'] == matrix['roots_sha256'], "canonical component manifest mismatch")
    require(certificate['target_matrix_sha256'] == matrix['matrix_sha256'], "target matrix manifest mismatch")
    default = F(certificate['default_alpha'])
    coefficients = [default]*len(matrix['roots'])
    for key,value in certificate['overrides'].items():
        c = int(key)
        require(str(c) == key and 0 <= c < len(coefficients), "invalid coefficient index")
        coefficients[c] = F(value)
    masses = check_boundary(matrix,coefficients)
    require(sum(value > 0 for value in coefficients) == 4, "unexpected active-component count")
    require(default == 0, "certificate is not the declared sparse boundary point")
    component, values = evidence['component'],evidence['values']
    for first,second,i,j in evidence['raw_ratios']:
        require(first*values[i]*coefficients[component[i]]
                == second*values[j]*coefficients[component[j]],
                "boundary target scalar-map ratio failure")
    expected = certificate['analytic_target_masses']
    require(set(expected) == set(PARENTS5), "analytic mass table omits a parent shape")
    for shape,by_bit in expected.items():
        require(set(by_bit) == {'0','1'} and all(set(item) <= set(TARGETS6) for item in by_bit.values()),
                "analytic mass table has an invalid record or child shape")
    raw_masses = {name:set() for name in PARENTS5}
    for name,order,record,equality,entries in evidence['raw_rows']:
        actual = {child:F(0) for child in TARGETS6}
        for key,u,part in entries:
            c = component[key]
            actual[matrix['classes'][c]] += u*coefficients[c]
        # Vertex zero is the unique minimum in each declared row-major Ferrers order.
        require(order[0] == 0 and all(past & 1 for past in order[1:]), "Ferrers root-bit role changed")
        target = expected[name][str(record & 1)]
        require(actual == {child:F(target.get(child,'0')) for child in TARGETS6},
                "analytic masses disagree with a full-record row")
        mass = sum(actual.values(),F(0))
        require(0 <= mass <= 1 and (not equality or mass == 1), "raw marked-row boundary failure")
        raw_masses[name].add(mass)
    controls = []
    missing_411 = [F(0) if shape == '411' else value
                   for shape,value in zip(matrix['classes'],coefficients)]
    doubled_51 = list(coefficients)
    doubled_51[0] *= 2
    for name,candidate,reason in (
            ('zero_411',missing_411,'boundary equality failed'),
            ('double_51_component_0',doubled_51,'boundary row sum exceeds one')):
        try:
            check_boundary(matrix,candidate)
        except RuntimeError as error:
            require(str(error) == reason, "negative control failed for the wrong reason")
            controls.append(name)
        else:
            raise RuntimeError("corrupted boundary certificate accepted")
    return dict(active_components=[i for i,v in enumerate(coefficients) if v > 0],
                row_masses={name:[str(v) for v in sorted(vs)] for name,vs in raw_masses.items()},
                minimum_rectangle_slack=str(min(1-mass for item,mass in zip(matrix['rows'],masses)
                                                if not item['equality'])),
                negative_controls=controls)


def main():
    require(sys.argv[1:] in ([],['--matrix']), "unknown arguments")
    prefix = reconstruct_prefix()
    matrix,evidence = target_matrix()
    matrix['prefix_counts'] = prefix
    matrix['fixed_prefix_parameter_json_sha256'] = PREFIX_PARAMETER_SHA256
    matrix['ri41_certificate_source_sha256'] = RI41_CERTIFICATE_SHA256
    matrix['roots_sha256'] = digest(matrix['roots'])
    matrix['matrix_sha256'] = digest(matrix['rows'])
    if sys.argv[1:] == ['--matrix']:
        print(json.dumps(matrix,sort_keys=True))
        return
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
    result = check_certificate(certificate,matrix,evidence)
    print('fixed_prefix_reconstruction='+json.dumps(prefix,sort_keys=True))
    print('ferrers_target='+json.dumps(matrix['counts'],sort_keys=True))
    print('component_children='+json.dumps(matrix['classes']))
    print('boundary_primal='+json.dumps(result,sort_keys=True))
    print('root_manifest_sha256='+matrix['roots_sha256'])
    print('target_matrix_sha256='+matrix['matrix_sha256'])
    print('scalar_identities: 436 lower + 7616 RI-41 + 768 target; full-D implication algebraic, no numerical payload test')
    print('DONE: zero-leakage boundary feasible; strict laws require the analytic interior mixture; no later-layer claim')


if __name__ == '__main__':
    main()
