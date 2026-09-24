#!/usr/bin/env python3
"""RI-58: bounded exact twin-top defect-drift certificate.

Standard library only; no writes, optimizer, global growth table or later kernel.
The accepted RI-52 checker is SHA-pinned before loading its prefix/row/potential
helpers with runpy under a non-main name. Its Ferrers target_matrix and shape
helpers are NOT called. An independent permutation/partition implementation here
checks every induced subset of only the declared small orders (at most six
vertices). The actual RI-41 certificate bytes are separately pinned.

--report prints certificate-preparation data, including all 16 fixed-base record
cases. It does not choose or evaluate unknown five-parent probabilities.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import json
import runpy
import sys


DEPENDENCIES = {
    'ri52_checker_sha256': '822d49b766a2ef2862f289f9e4abb4a262cfafcf58ac3ff4c34c044e75f6c654',
    'ri41_certificate_sha256': '3d966fb20911d630a427ceb777a41539e930d1ba75c3098dcad35e08e4b1d969',
}
BASE = (0,1,1,7)
BASE_RECORD = 1
CLONE_PRECURSOR = 7
AXES = (3,5)
GEOMETRY_ORDERS = set()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vertices(mask):
    return tuple(v for v in range(mask.bit_length()) if mask & (1 << v))


def validate_order(order):
    require(len(order) <= 6, 'order exceeds the bounded geometry domain')
    for v,past in enumerate(order):
        require(type(past) is int and 0 <= past < (1 << v), 'order is not naturally labeled')
        require(all(order[u] & past == order[u] for u in vertices(past)),
                'predecessor relation is not transitive')


def own_ideals(order):
    validate_order(order)
    return tuple(part for part in range(1 << len(order))
                 if all(order[v] & part == order[v] for v in vertices(part)))


def own_induced(order, keep):
    retained = vertices(keep)
    return tuple(sum(1 << j for j,u in enumerate(retained) if order[v] & (1 << u))
                 for v in retained)


def relabel_order(order, old_to_new):
    result = [0]*len(order)
    for v,past in enumerate(order):
        result[old_to_new[v]] = sum(1 << old_to_new[u] for u in vertices(past))
    return tuple(result)


def relabel_record(record, old_to_new):
    return sum(1 << old_to_new[v] for v in vertices(record))


@cache
def own_canonical(order):
    validate_order(order)
    # This tuple-of-predecessor-masks canonical form is independent of the
    # accepted helper's relation-code/precursor/inside-record canonical key.
    return min(relabel_order(order,perm) for perm in permutations(range(len(order))))


def integer_partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    maximum = total if maximum is None else min(total,maximum)
    for length in range(maximum,0,-1):
        for rest in integer_partitions(total-length,length):
            yield (length,)+rest


def own_ferrers(partition):
    # Diagonal order, rather than the accepted checker's row-major order.
    cells = sorted(((i,j) for i,length in enumerate(partition) for j in range(length)),
                   key=lambda cell:(sum(cell),cell))
    return tuple(sum(1 << u for u,(a,b) in enumerate(cells)
                     if a <= i and b <= j and (a,b) != (i,j)) for i,j in cells)


@cache
def ferrers_catalogue(n):
    require(0 <= n <= 6, 'Ferrers catalogue exceeds six vertices')
    return frozenset(own_canonical(own_ferrers(partition)) for partition in integer_partitions(n))


@cache
def defect(order):
    validate_order(order)
    GEOMETRY_ORDERS.add(order)
    largest, retained_masks = -1, []
    # All subsets are tested, not only ideals or guessed top deletions.
    for keep in range(1 << len(order)):
        retained = own_induced(order,keep)
        if own_canonical(retained) in ferrers_catalogue(len(retained)):
            size = keep.bit_count()
            if size > largest:
                largest,retained_masks = size,[keep]
            elif size == largest:
                retained_masks.append(keep)
    require(largest >= 0, 'empty Ferrers suborder was omitted')
    return len(order)-largest,tuple(retained_masks)


def load_prefix():
    track_b = Path(__file__).resolve().parent.parent
    source = track_b / 'native_growth_ferrers_gate_v1' / 'check.py'
    ri41_file = track_b / 'native_growth_height_normalization_v1' / 'CERTIFICATE.json'
    source_bytes,certificate_bytes = source.read_bytes(),ri41_file.read_bytes()
    require(sha256(source_bytes).hexdigest() == DEPENDENCIES['ri52_checker_sha256'],
            'accepted helper source pin mismatch')
    require(sha256(certificate_bytes).hexdigest() == DEPENDENCIES['ri41_certificate_sha256'],
            'accepted RI-41 certificate source pin mismatch')
    helper = runpy.run_path(str(source),run_name='ri52_fixed_prefix_dependency')
    prefix_counts = helper['reconstruct_prefix']()
    certificate = json.loads(certificate_bytes)
    require(tuple(map(tuple,certificate['roots'])) == helper['ROOTS4']
            and certificate['default_alpha'] == '1/8'
            and certificate['overrides'] == {str(k):v for k,v in helper['OVERRIDES4'].items()},
            'actual RI-41 certificate differs from embedded prefix data')
    return helper,prefix_counts


def prepare_report(helper, prefix_counts):
    clone = BASE+(CLONE_PRECURSOR,)
    base_defect,_ = defect(BASE)
    clone_defect,optimal_keeps = defect(clone)
    children = []
    for part in own_ideals(clone):
        child_defect,_ = defect(clone+(part,))
        increment = child_defect-clone_defect
        require(increment in (0,1), 'selected maximal birth violated defect stability')
        children.append(dict(precursor=part,child_defect=child_defect,increment=increment))
    neutral = [item['precursor'] for item in children if item['increment'] == 0]
    require(neutral == list(AXES), 'proposed neutral-slot classification failed')
    counterparts,diamonds = [],[]
    old = helper['row'](BASE,BASE_RECORD)
    p = old[CLONE_PRECURSOR]
    weights = [old[axis] for axis in AXES]
    require(all(value > 0 for value in [p]+weights), 'nonpositive fixed-prefix factor')
    selected_row_keys = {helper['row_key'](clone,BASE_RECORD)}
    marked_checks = 0
    swap = (0,1,2,3,5,4)
    for axis,weight in zip(AXES,weights):
        corner_parent = BASE+(axis,)
        corner_defect,_ = defect(corner_parent)
        restored = corner_parent+(CLONE_PRECURSOR,)
        restored_defect,_ = defect(restored)
        require(corner_defect == 0 and restored_defect == 1,
                'companion slot is not Ferrers-to-raising')
        require(CLONE_PRECURSOR in own_ideals(corner_parent), 'restored-top past is not an ideal')
        selected_row_keys.add(helper['row_key'](corner_parent,BASE_RECORD))
        counterparts.append(dict(axis=axis,past_masks=list(corner_parent),parent_defect=corner_defect,
                                 restored_precursor=CLONE_PRECURSOR,restored_child_defect=restored_defect,
                                 restored_increment=restored_defect-corner_defect))
        representative = None
        for u in (0,1):
            for v in (0,1):
                left_child = clone+(axis,)
                left_record = BASE_RECORD|(u << 4)|(v << 5)
                right_record = BASE_RECORD|(v << 4)|(u << 5)
                require(relabel_order(left_child,swap) == restored
                        and relabel_record(left_record,swap) == right_record,
                        'marked terminal-label transport failed')
                left_parent_record,right_parent_record = BASE_RECORD|(u << 4),BASE_RECORD|(v << 4)
                left_node = helper['node'](clone,axis,left_parent_record)
                right_node = helper['node'](corner_parent,CLONE_PRECURSOR,right_parent_record)
                left_u = helper['potential'](clone,axis,left_parent_record & axis)
                right_u = helper['potential'](corner_parent,CLONE_PRECURSOR,
                                               right_parent_record & CLONE_PRECURSOR)
                require(left_node != right_node and p*left_u == weight*right_u,
                        'mixed proper-slot potential ratio failed')
                item = dict(axis=axis,left_node=list(left_node),right_node=list(right_node),
                            left_potential=str(left_u),right_potential=str(right_u),
                            shared_old_times_potential=str(p*left_u))
                require(representative is None or item == representative,
                        'a slot read an excluded newborn record')
                representative = item
                marked_checks += 1
        diamonds.append(representative)
    geometry = dict(base_defect=base_defect,clone_past_masks=list(clone),clone_defect=clone_defect,
                    clone_optimal_retained_masks=list(optimal_keeps),clone_children=children,
                    full_increment=children[-1]['increment'],counterparts=counterparts)
    record_cases = []
    for record in range(16):
        q = helper['row'](BASE,record)
        factors = (q[CLONE_PRECURSOR],q[AXES[0]],q[AXES[1]])
        record_cases.append(dict(record=record,p=str(factors[0]),a=str(factors[1]),b=str(factors[2]),
                                 bound=str(factors[0]/sum(factors,F(0)))))
    require(base_defect == 0 and clone_defect == 1 and optimal_keeps == (15,23),
            'clone optimal induced-suborder claim failed')
    counts = dict(selected_geometry_orders=len(GEOMETRY_ORDERS),
                  induced_subsets_checked=sum(1 << len(order) for order in GEOMETRY_ORDERS),
                  maximum_geometry_size=max(map(len,GEOMETRY_ORDERS)),
                  clone_ideals=len(children),neutral_slots=len(neutral),
                  selected_raw_marked_rows=3,selected_marked_row_classes=len(selected_row_keys),
                  old_record_cases=len(record_cases),marked_diamond_roles=marked_checks,
                  ferrers_partitions={str(n):len(tuple(integer_partitions(n))) for n in range(7)},
                  ferrers_order_types={str(n):len(ferrers_catalogue(n)) for n in range(7)})
    total = p+sum(weights,F(0))
    return dict(dependencies=DEPENDENCIES,prefix_counts=prefix_counts,
                base=dict(past_masks=list(BASE),record=BASE_RECORD),clone_precursor=CLONE_PRECURSOR,
                axis_precursors=list(AXES),geometry=geometry,old_factors=dict(p=str(p),a=str(weights[0]),b=str(weights[1])),
                lower_bound=str(p/total),normalized_weights=[str(p/total)]+[str(value/total) for value in weights],
                local_diamonds=diamonds,verification_counts=counts,old_record_cases=record_cases)


def check_certificate(certificate, report):
    require(certificate['schema'] == 'ri58-defect-bottleneck-v1', 'certificate schema mismatch')
    record = certificate['base']['record']
    require(type(record) is int and 0 <= record < 16, 'base record outside four-bit cube')
    require(certificate['base'] == report['base'], 'selected marked base mismatch')
    require(certificate['axis_precursors'] == report['axis_precursors'], 'neutral precursor inventory mismatch')
    require(certificate['clone_precursor'] == report['clone_precursor'], 'clone precursor mismatch')
    for field in ('dependencies','prefix_counts','geometry','local_diamonds','verification_counts'):
        require(certificate[field] == report[field], 'certificate '+field+' mismatch')
    require(set(certificate['old_factors']) == {'p','a','b'}, 'old-factor inventory mismatch')
    factors = [F(certificate['old_factors'][name]) for name in ('p','a','b')]
    require(factors == [F(report['old_factors'][name]) for name in ('p','a','b')],
            'fixed-prefix factors mismatch')
    total = sum(factors,F(0))
    bound = F(certificate['lower_bound'])
    require(0 < bound < 1 and bound == factors[0]/total, 'incorrect derived drift lower bound')
    normalized = [F(value) for value in certificate['normalized_weights']]
    require(normalized == [value/total for value in factors] and sum(normalized,F(0)) == 1,
            'symbolic drift-weight normalization failed')
    # No unknown q at parent five is assigned here: the exact coefficients
    # certify p*phi_P+a*phi_F1+b*phi_F2 >= p once the two proved diamond
    # identities and nonnegative remaining drift contributions are applied.
    return bound


def negative_controls(certificate, report):
    wrong_axis = dict(certificate,axis_precursors=[3,7])
    wrong_bound = dict(certificate,lower_bound=str(F(certificate['lower_bound'])+F(1,1000)))
    wrong_record = dict(certificate,base=dict(certificate['base'],record=16))
    controls = []
    for name,bad,reason in (
            ('wrong_axis_7',wrong_axis,'neutral precursor inventory mismatch'),
            ('wrong_bound',wrong_bound,'incorrect derived drift lower bound'),
            ('record_16',wrong_record,'base record outside four-bit cube')):
        try:
            check_certificate(bad,report)
        except RuntimeError as error:
            require(str(error) == reason, 'negative control failed for the wrong reason')
            controls.append(name)
        else:
            raise RuntimeError('malformed certificate accepted')
    return controls


def main():
    require(sys.argv[1:] in ([],['--report']), 'unknown arguments')
    helper,prefix_counts = load_prefix()
    report = prepare_report(helper,prefix_counts)
    if sys.argv[1:] == ['--report']:
        print(json.dumps(report,sort_keys=True))
        return
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
    bound = check_certificate(certificate,report)
    controls = negative_controls(certificate,report)
    print('pinned_dependencies='+json.dumps(DEPENDENCIES,sort_keys=True))
    print('bounded_coverage='+json.dumps(report['verification_counts'],sort_keys=True))
    print('clone_defect=1 optimal_retained_masks=[15,23] neutral_precursors=[3,5] full_increment=1')
    print('selected_record='+str(BASE_RECORD)+' old_factors='+json.dumps(report['old_factors'],sort_keys=True))
    print('drift_lower_bound='+str(bound)+' normalized_weights='+json.dumps(report['normalized_weights']))
    print('negative_controls='+json.dumps(controls))
    print('marked_potential_identities=8; full-D/4 consequence algebraic; no unknown new-row or numeric payload evaluation')
    print('DONE: positive fixed-layer uniform-drift obstruction, not an optimum or an actual-history Cesaro obstruction')


if __name__ == '__main__':
    main()
