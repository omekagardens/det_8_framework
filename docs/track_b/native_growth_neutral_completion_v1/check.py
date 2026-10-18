#!/usr/bin/env python3
"""RI-45: fixed-prefix, exact first-free-layer completion check.

Standard library only; no project imports, no writes, no parent size above 5.
Naturally labeled orders are tuples of transitive predecessor bit masks.
"""

from fractions import Fraction as F
from functools import cache
from itertools import permutations
from hashlib import sha256
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
def parents(n):
    require(0 <= n <= 5, "parent size exceeds the authorized layer")
    if n == 0:
        return ((),)
    return tuple(p + (s,) for p in parents(n - 1) for s in ideals(p))


@cache
def depths(order):
    result = []
    for past in order:
        result.append(1 + max((result[v] for v in bits(past)), default=0))
    return tuple(result)


def height(order, part=None):
    if part is None:
        return max(depths(order), default=0)
    return max((depths(order)[v] for v in bits(part)), default=0)


@cache
def permutations_of(n):
    return tuple(permutations(range(n)))


@cache
def layout(order, part):
    n = len(order)
    candidates = []
    best = None
    for perm in permutations_of(n):
        edge = sum(1 << (n * perm[u] + perm[v]) for v, past in enumerate(order) for u in bits(past))
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
    return pair + (min(sum(1 << perm[v] for v in bits(inside)) for perm in candidates),)


def row_key(order, record):
    return node(order, (1 << len(order)) - 1, record)


A, C, D = F(2, 3), F(1, 5), F(1, 4)
FS = (F(1, 6), F(1, 3))
G, K = F(1, 10), F(11, 20)
HS, E = (F(19, 30), F(7, 15)), F(1, 44)


# Exact RI-41 component coefficients and canonical roots, re-expressed as data.
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
    return result


@cache
def restriction(order, keep):
    surviving = tuple(bits(keep))
    remap = {v:i for i,v in enumerate(surviving)}
    induced = tuple(sum(1 << remap[u] for u in bits(order[v] & keep)) for v in surviving)
    return induced, surviving


@cache
def potential(order, part, inside_record):
    n = len(order)
    require(n in (4,5) and part in ideals(order) and part != (1 << n)-1,
            "potential outside declared proper-slot domain")
    ancestors = 0
    for past in order:
        ancestors |= past
    omitted = ((1 << n)-1) & ~ancestors & ~part
    require(omitted, "proper ideal omitted no maximal vertex")
    result, deleted = F(1), omitted
    while deleted:
        keep = ((1 << n)-1) ^ deleted
        smaller, surviving = restriction(order,keep)
        s = sum(1 << i for i,v in enumerate(surviving) if part & (1 << v))
        r = sum(1 << i for i,v in enumerate(surviving) if inside_record & (1 << v))
        factor = row(smaller,r)[s]
        result = result*factor if deleted.bit_count()%2 else result/factor
        deleted = (deleted-1) & omitted
    require(result > 0, "nonpositive maximal-deletion potential")
    return result


def make_layer(n):
    values, classes, raw_rows = {}, {}, []
    proper_count = 0
    for order in parents(n):
        for record in range(1 << n):
            entries = []
            for part in ideals(order):
                if part == (1 << n)-1:
                    continue
                key = node(order,part,record)
                u = potential(order,part,record & part)
                require(key not in values or values[key] == u, "local quotient potential mismatch")
                values[key] = u
                child = order + (part,)
                h = height(child)
                tallest = sum(d == h for d in depths(child))
                classification = (h, tallest >= 2)
                require(key not in classes or classes[key] == classification,
                        "terminal height class changed inside quotient")
                classes[key] = classification
                raises = height(child) > height(order)
                require(height(child) == max(height(order),height(order,part)+1),
                        "actual height identity failure")
                entries.append((key,u,raises))
                proper_count += 1
            raw_rows.append((order,record,entries))
    representative = {key:key for key in values}

    def root(key):
        trail = []
        while representative[key] != key:
            trail.append(key)
            key = representative[key]
        for item in trail:
            representative[item] = key
        return key

    edge_count = zeros = equals = loops = 0
    for base in parents(n-1):
        for record in range(1 << (n-1)):
            old = row(base,record)
            for first in ideals(base):
                for second in ideals(base):
                    for b in (0,1):
                        for h in (0,1):
                            i = node(base+(first,),second,record|(b << (n-1)))
                            j = node(base+(second,),first,record|(h << (n-1)))
                            require(old[first]*values[i] == old[second]*values[j],
                                    "raw full-map ratio multiplier failure")
                            require(classes[i] == classes[j], "raw edge changes child height class")
                            ri,rj = root(i),root(j)
                            if ri != rj:
                                low,high = sorted((ri,rj))
                                representative[high] = low
                            edge_count += 1
                            zeros += int(record == 0 and b == h == 0)
                            equals += int(first == second)
                            loops += int(i == j)
    roots = sorted({root(key) for key in values})
    numbers = {key:i for i,key in enumerate(roots)}
    component = {key:numbers[root(key)] for key in values}
    component_class = [classes[key] for key in roots]
    unique_rows, all_rows = {}, []
    for order,record,entries in raw_rows:
        a,b = {},{}
        for key,u,raises in entries:
            c = component[key]
            a[c] = a.get(c,F(0))+u
            if not raises:
                b[c] = b.get(c,F(0))+u
            if component_class[c][1]:
                require(not raises and component_class[c][0] == height(order),
                        "neutral height-block decomposition failed")
        key = row_key(order,record)
        item = (height(order),a,b)
        require(key not in unique_rows or unique_rows[key][0] == item,
                "complete marked-parent quotient changed row multiplicities")
        unique_rows[key] = (item,order,record)
        all_rows.append((key,item))
    rows = [(key,*unique_rows[key]) for key in sorted(unique_rows)]
    counts = dict(parents=len(parents(n)), rows=len(raw_rows), proper=proper_count,
                  nodes=len(values), components=len(roots), edges=edge_count,
                  all_zero=zeros, equal=equals, loops=loops, marked_row_classes=len(rows))
    return dict(rows=rows, all_rows=all_rows, roots=roots, classes=component_class,
                values=values, component=component, counts=counts)


def main():
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
    require(certificate['schema'] == 'ri45-neutral-separator-v1' and certificate['parent_size'] == 5,
            "certificate domain mismatch")
    seed_data = dict(roots=ROOTS4,default_alpha='1/8',overrides={str(k):v for k,v in OVERRIDES4.items()})
    seed_bytes = (json.dumps(seed_data,sort_keys=True,separators=(',',':'))+'\n').encode()
    require(sha256(seed_bytes).hexdigest() == certificate['fixed_prefix_parameter_json_sha256'],
            "embedded RI-41 parameters differ from their independent data pin")
    require(tuple(len(parents(n)) for n in range(6)) == (1,1,2,7,40,357),
            "natural-parent enumeration changed")
    four = make_layer(4)
    require(tuple(four['roots']) == ROOTS4, "fixed RI-41 canonical components changed")
    for key,c in four['component'].items():
        COEFFICIENTS4[key] = F(OVERRIDES4.get(c,'1/8'))
    # Check the reconstructed fixed layer without running the accepted executor.
    full_min, tau_max, slot_min = F(1), F(0), F(1)
    for order in parents(4):
        for record in range(16):
            q = row(order,record)
            full_min = min(full_min,q[15])
            slot_min = min(slot_min,*q.values())
            tau_max = max(tau_max,sum((v for s,v in q.items() if height(order,s)==height(order)),F(0)))
    require((full_min,tau_max,slot_min) == (F(33901019,474368400),F(14082809,29648025),F(9,681472)),
            "fixed RI-41 probabilities changed")
    five = make_layer(5)
    require(five['counts'] == dict(parents=357,rows=11424,proper=142944,nodes=2961,components=798,
            edges=216128,all_zero=3377,equal=22848,loops=28176,marked_row_classes=1490),
            "first-free-layer coverage changed")
    manifest = certificate['canonical_components']
    root_digest = sha256(json.dumps(five['roots'],separators=(',',':')).encode()).hexdigest()
    require(manifest['count'] == len(five['roots']) and root_digest == manifest['roots_sha256'],
            "canonical component manifest mismatch")
    if sys.argv[1:] == ['--matrix']:
        print(json.dumps(dict(counts=five['counts'],roots=five['roots'],classes=five['classes'],
            rows=[dict(key=key,height=item[0],order=order,record=record,
                       A={str(c):str(v) for c,v in item[1].items()},
                       B={str(c):str(v) for c,v in item[2].items()})
                  for key,item,order,record in five['rows']])))
        return
    require(not sys.argv[1:], "unknown arguments")
    print('fixed_prefix_reconstruction='+json.dumps(four['counts'],sort_keys=True))
    print('parent_five='+json.dumps(five['counts'],sort_keys=True))
    for h in range(1,6):
        print('height',h,'marked_rows',sum(item[0]==h for _,item in five['all_rows']),
              'row_classes',sum(item[0]==h for _,item,_,_ in five['rows']),
              'neutral_components',sum(ch==h and neutral for ch,neutral in five['classes']))
    by_key = {key:item for key,item,_,_ in five['rows']}
    # Verify all record classes in the two analytically private extreme blocks.
    for h,expected_components in ((1,1),(5,16)):
        beta = {}
        for key,item in five['all_rows']:
            if item[0] != h:
                continue
            neutral = {c:u for c,u in item[1].items() if five['classes'][c][1]}
            require(len(neutral) == 1, "extreme block has an unexpected neutral support")
            c,u = next(iter(neutral.items()))
            require(c not in beta or beta[c] == 1/u, "private reciprocal inconsistent across marks")
            beta[c] = 1/u
        require(len(beta) == expected_components, "extreme marked-component inventory changed")
        require(all(sum((u*beta.get(c,F(0)) for c,u in item[1].items()),F(0)) == 1
                    for _,item in five['all_rows'] if item[0] == h), "extreme completion failed")
    print('extreme_blocks: all32 antichain marks / all32 chain marks; PASS')
    support, names, cs = [], {}, {}
    for entry in certificate['parents']:
        order,record,weight = tuple(entry['past_masks']),entry['record'],F(entry['y'])
        key = row_key(order,record)
        require(order in parents(5) and record == 0 and list(key) == entry['row_key'],
                "certificate marked parent mismatch")
        item = by_key[key]
        require(item[0] == 3, "separator leaves its height-three block")
        w = F(1)
        for v,past in enumerate(order):
            w *= row(order[:v],0)[past]
        aut = len(layout(order,31)[1])
        require(w == F(entry['path_weight']) and aut == entry['automorphisms'],
                "analytic weight/automorphism mismatch")
        require(weight == F(certificate['dual_scale'])*F(entry['c'])*w/aut,
                "signed coefficient does not match deletion-count proof")
        require(key not in names, "separator repeats an isomorphic representative")
        names[key],cs[entry['name']] = entry['name'],F(entry['c'])
        support.append((key,weight))
    require(len(support) == 7 and names[support[0][0]] == 'Q', "wrong sparse support")
    extra = certificate['extra_zero_parent']
    names[row_key(tuple(extra['past_masks']),0)],cs[extra['name']] = extra['name'],F(0)
    qorder = tuple(certificate['parents'][0]['past_masks'])
    qrow = by_key[support[0][0]]
    preserving_parts = {s for s in ideals(qorder) if height(qorder,s) < height(qorder)}
    require(preserving_parts == {x['past_mask'] for x in certificate['Q_child_deletions']},
            "analytic cut omitted a preserving precursor")
    for entry in certificate['Q_child_deletions']:
        child = qorder+(entry['past_mask'],)
        ancestors = 0
        for past in child:
            ancestors |= past
        counts = {}
        for v in bits(63 & ~ancestors):
            smaller,_ = restriction(child,63 ^ (1 << v))
            name = names[row_key(smaller,0)]
            counts[name] = counts.get(name,0)+1
        require(counts == entry['counts'], "six-child deletion table mismatch")
        require(sum(cs[name]*count for name,count in counts.items()) == 0,
                "analytic deletion cancellation failed")

    def check_dual(candidate):
        require(sum(w for _,w in candidate) < 0, "separator sum is not negative")
        paired = [F(0)]*len(five['roots'])
        for key,weight in candidate:
            for c,value in by_key[key][1].items():
                paired[c] += weight*value
        require(all(v >= 0 for v,(_,neutral) in zip(paired,five['classes']) if neutral),
                "negative neutral pairing")
        return paired

    check_dual(support)
    require(-sum(w for _,w in support) == F(certificate['negative_sum']), "separator sum mismatch")
    require(all(five['classes'][c][1] for c in qrow[2]), "preserving Q slot is mixed")
    direct = [F(0)]*len(five['roots'])
    require(support[0][1] < 0 and all(w > 0 for _,w in support[1:]), "not a one-negative-row cut")
    negative = -support[0][1]
    for key,weight in support[1:]:
        for c,value in by_key[key][1].items():
            direct[c] += weight*value
    for c,value in qrow[2].items():
        direct[c] -= negative*value
    require(all(v >= 0 for v in direct), "direct all-component height bound failed")
    positive = sum(w for _,w in support[1:])
    require(negative == F(certificate['Q_negative_coefficient']) and positive == F(certificate['positive_sum'])
            and (negative-positive)/negative == F(certificate['drift_lower_bound']), "bound arithmetic mismatch")
    qroots = [list(five['roots'][c]) for c in sorted(qrow[2])]
    require(qroots == manifest['Q_preserving_roots'], "negative-row neutral roots changed")
    for candidate,reason in (([(k,-w) for k,w in support],'separator sum is not negative'),
                             ([(k,w) for k,w in support if names[k] != 'P4'],'negative neutral pairing')):
        try:
            check_dual(candidate)
        except RuntimeError as error:
            require(str(error) == reason, "negative control failed for the wrong reason")
        else:
            raise RuntimeError("corrupted separator accepted")
    print('separator: negative_sum=1756883 neutral_pairings_nonnegative; PASS')
    print('direct_bound=1756883/3859907 all_component_pairings_nonnegative; PASS')
    print('six_child_deletion_table=PASS negative_controls=reversed_sign,missing_P4; PASS')
    print('Q_preserving_roots='+str(qroots))
    print('root_manifest_sha256='+root_digest)
    print('DONE: fixed-prefix parent-five obstruction; no propagation/asymptotic claim')


if __name__ == '__main__':
    main()
