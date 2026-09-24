#!/usr/bin/env python3
"""RI-54: exact first-layer Ferrers bottleneck certificates.

Standard library only; no downloads, optimizer, writes, or successor-row
evaluation. This checker has an explicit read-only dependency on the SHA-pinned
accepted RI-52 checker and certificate. runpy loads its helper definitions with
a non-main module name; its main routine is not invoked. Its bounded prefix and
Ferrers-target reconstruction is reused, not independently reimplemented here.

--report emits structural metadata for certificate preparation, not a verdict.
"""

from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import runpy
import sys


DEPENDENCIES = {
    'ri52_checker_sha256': '822d49b766a2ef2862f289f9e4abb4a262cfafcf58ac3ff4c34c044e75f6c654',
    'ri52_certificate_sha256': '33dd1a9d3659b92d02009185bc1e681309380c03c08fc83a8cb6555198203d6b',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_fixed_matrix():
    predecessor = Path(__file__).resolve().parent.parent / 'native_growth_ferrers_gate_v1'
    source = predecessor / 'check.py'
    accepted_certificate = predecessor / 'CERTIFICATE.json'
    source_bytes, certificate_bytes = source.read_bytes(), accepted_certificate.read_bytes()
    require(sha256(source_bytes).hexdigest() == DEPENDENCIES['ri52_checker_sha256'],
            'accepted RI-52 checker source pin mismatch')
    require(sha256(certificate_bytes).hexdigest() == DEPENDENCIES['ri52_certificate_sha256'],
            'accepted RI-52 certificate source pin mismatch')
    dependency = runpy.run_path(str(source), run_name='ri52_readonly_dependency')
    prefix = dependency['reconstruct_prefix']()
    matrix, evidence = dependency['target_matrix']()
    matrix['prefix_counts'] = prefix
    matrix['fixed_prefix_parameter_json_sha256'] = dependency['PREFIX_PARAMETER_SHA256']
    matrix['ri41_certificate_source_sha256'] = dependency['RI41_CERTIFICATE_SHA256']
    matrix['roots_sha256'] = dependency['digest'](matrix['roots'])
    matrix['matrix_sha256'] = dependency['digest'](matrix['rows'])
    # Verify the unchanged baseline certificate as well as the two source pins.
    baseline = dependency['check_certificate'](json.loads(certificate_bytes),matrix,evidence)
    return dependency,matrix,evidence,baseline


def marked_rows(dependency, matrix, evidence):
    rows, by_shape = [], {}
    for shape,order,record,equality,entries in evidence['raw_rows']:
        vector = [F(0)]*len(matrix['roots'])
        for key,u,part in entries:
            vector[evidence['component'][key]] += u
        key = dependency['row_key'](order,record)
        require(order[0] == 0 and all(past & 1 for past in order[1:]),
                'root-bit vertex is not the unique Ferrers minimum')
        item = dict(shape=shape,record=record,key=key,vector=vector,equality=equality)
        rows.append(item)
        by_shape.setdefault(shape,[]).append(item)
    require(set(by_shape) == {'5','41','311','32'}
            and all(len(items) == 32 for items in by_shape.values()),
            'complete raw marked-parent coverage changed')
    classes = {tuple(item['key']):item for item in matrix['rows']}
    for item in rows:
        expected = classes[item['key']]
        require(item['vector'] == [F(expected['A'].get(str(c),'0'))
                                   for c in range(len(matrix['roots']))],
                'raw marked row disagrees with the canonical matrix')
    return rows,by_shape


def one_component(item, matrix, child):
    indices = [c for c,value in enumerate(item['vector'])
               if value and matrix['classes'][c] == child]
    require(len(indices) == 1, 'row has unexpected target-child component multiplicity')
    return indices[0]


def matched_rows(matrix, by_shape):
    matches = []
    for b in by_shape['32']:
        c42 = one_component(b,matrix,'42')
        c321 = one_component(b,matrix,'321')
        candidates_a = [a for a in by_shape['41'] if a['vector'][c42] > 0]
        candidates_e = [e for e in by_shape['311'] if e['vector'][c321] > 0]
        require(candidates_a and candidates_e, 'no matching A/E row for a marked B row')
        bit = b['record'] & 1
        require((matrix['roots'][c42][2] & 1) == bit
                and (matrix['roots'][c321][2] & 1) == bit,
                'component root-bit correspondence changed')
        require(all((item['record'] & 1) == bit for item in candidates_a+candidates_e),
                'matched A/E rows disagree on the retained root record')
        # Completion selection is deterministic and component-based, not a search
        # for a favorable dual residual. Every B record assignment is retained.
        a = min(candidates_a,key=lambda item:item['record'])
        e = min(candidates_e,key=lambda item:item['record'])
        matches.append(dict(B=b,A=a,E=e,root_bit=bit,component42=c42,component321=c321,
                            A_candidate_count=len(candidates_a),E_candidate_count=len(candidates_e)))
    return matches


def structural_report(matrix, rows, matches):
    counts = dict(marked_rows=len(rows),marked_row_classes=len(matrix['rows']),
                  marked_B_rows=len(matches),
                  B_rows_by_root_bit={str(bit):sum(m['root_bit'] == bit for m in matches) for bit in (0,1)},
                  dual_residual_columns=len(matches)*len(matrix['roots']),
                  target_scalar_ratios=matrix['counts']['raw_ratios'],
                  A_candidate_counts=sorted({m['A_candidate_count'] for m in matches}),
                  E_candidate_counts=sorted({m['E_candidate_count'] for m in matches}))
    return dict(dependencies=DEPENDENCIES,prefix_counts=matrix['prefix_counts'],
                target_counts=matrix['counts'],verification_counts=counts,
                canonical_components=dict(roots=matrix['roots'],roots_sha256=matrix['roots_sha256']),
                target_matrix_sha256=matrix['matrix_sha256'],
                matches=[dict(B_record=m['B']['record'],A_record=m['A']['record'],E_record=m['E']['record'],
                              root_bit=m['root_bit'],component42=m['component42'],component321=m['component321'])
                         for m in matches])


def check_dual(matrix, matches, dual):
    require(set(dual) == {'0','1'}, 'dual table omits a retained root record')
    caps, residuals = {}, []
    for bit,entry in dual.items():
        ya,ye,cap = F(entry['A']),F(entry['E']),F(entry['cap'])
        require(ya >= 0 and ye >= 0 and ya+ye == cap and cap < F(1,2),
                'dual weights/cap are invalid')
        caps[int(bit)] = cap
    for match in matches:
        entry = dual[str(match['root_bit'])]
        ya,ye = F(entry['A']),F(entry['E'])
        residual = [ya*a+ye*e-b for a,e,b in zip(match['A']['vector'],
                                               match['E']['vector'],match['B']['vector'])]
        require(all(value >= 0 for value in residual), 'negative dual residual coefficient')
        residuals.append(residual)
    # This certificate uses only the A/E target-mass caps <=1. The equalities
    # of the zero-leakage face are NOT a premise of the dual upper bounds.
    return caps,residuals


def read_coefficients(matrix, primal):
    coefficients = [F(primal['default_alpha'])]*len(matrix['roots'])
    for key,value in primal['overrides'].items():
        c = int(key)
        require(str(c) == key and 0 <= c < len(coefficients), 'invalid primal component index')
        coefficients[c] = F(value)
    return coefficients


def check_primal(matrix, evidence, rows, coefficients):
    require(len(coefficients) == len(matrix['roots']) and all(value >= 0 for value in coefficients),
            'primal coefficients are not nonnegative')
    masses = []
    for item in rows:
        mass = sum((u*alpha for u,alpha in zip(item['vector'],coefficients)),F(0))
        require(mass <= 1, 'primal row sum exceeds one')
        require(not item['equality'] or mass == 1, 'primal equality failed')
        masses.append(mass)
    for item in matrix['rows']:
        mass = sum((F(u)*coefficients[int(c)] for c,u in item['A'].items()),F(0))
        require(mass <= 1 and (not item['equality'] or mass == 1), 'canonical primal row failure')
    values,component = evidence['values'],evidence['component']
    for first,second,i,j in evidence['raw_ratios']:
        require(first*values[i]*coefficients[component[i]]
                == second*values[j]*coefficients[component[j]], 'primal scalar-map ratio failure')
    return masses


def check_certificate(certificate, matrix, evidence, rows, matches, report):
    require(certificate['schema'] == 'ri54-ferrers-bottleneck-v1' and certificate['parent_size'] == 5,
            'certificate domain mismatch')
    for name in ('dependencies','prefix_counts','target_counts','verification_counts',
                 'target_matrix_sha256'):
        require(certificate[name] == report[name], 'certificate '+name+' mismatch')
    manifest = certificate['canonical_components']
    require(tuple(map(tuple,manifest['roots'])) == tuple(matrix['roots'])
            and manifest['roots_sha256'] == matrix['roots_sha256'], 'canonical component manifest mismatch')
    caps,residuals = check_dual(matrix,matches,certificate['dual_by_root_bit'])
    coefficients = read_coefficients(matrix,certificate['primal'])
    masses = check_primal(matrix,evidence,rows,coefficients)
    for match,residual in zip(matches,residuals):
        b = sum((u*alpha for u,alpha in zip(match['B']['vector'],coefficients)),F(0))
        require(b == caps[match['root_bit']], 'primal does not attain every marked B-row cap')
        require(sum((value*alpha for value,alpha in zip(residual,coefficients)),F(0)) == 0,
                'dual/primal complementary residual is not zero')
    # Both mutations stay in memory and must fail for the intended reason.
    corrupted_dual = {bit:dict(entry) for bit,entry in certificate['dual_by_root_bit'].items()}
    corrupted_dual['0']['A'] = '0'
    corrupted_dual['0']['cap'] = corrupted_dual['0']['E']
    try:
        check_dual(matrix,matches,corrupted_dual)
    except RuntimeError as error:
        require(str(error) == 'negative dual residual coefficient', 'dual control failed for the wrong reason')
    else:
        raise RuntimeError('corrupted dual accepted')
    doubled = list(coefficients)
    doubled[4] *= 2
    try:
        check_primal(matrix,evidence,rows,doubled)
    except RuntimeError as error:
        require(str(error) == 'primal row sum exceeds one', 'primal control failed for the wrong reason')
    else:
        raise RuntimeError('corrupted primal accepted')
    by_shape = {shape:sorted({str(mass) for item,mass in zip(rows,masses) if item['shape'] == shape})
                for shape in ('5','41','311','32')}
    return dict(caps={str(bit):str(value) for bit,value in caps.items()},
                gaps_below_half={str(bit):str(F(1,2)-value) for bit,value in caps.items()},
                primal_row_masses=by_shape,active_primal_components=[c for c,value in enumerate(coefficients) if value],
                dual_zero_coefficients=sum(value == 0 for residual in residuals for value in residual),
                dual_positive_coefficients=sum(value > 0 for residual in residuals for value in residual),
                negative_controls=['zero_A_weight_root0','double_primal_component4'])


def main():
    require(sys.argv[1:] in ([],['--report']), 'unknown arguments')
    dependency,matrix,evidence,baseline = load_fixed_matrix()
    rows,by_shape = marked_rows(dependency,matrix,evidence)
    matches = matched_rows(matrix,by_shape)
    report = structural_report(matrix,rows,matches)
    if sys.argv[1:] == ['--report']:
        print(json.dumps(report,sort_keys=True))
        return
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text(encoding='utf-8'))
    result = check_certificate(certificate,matrix,evidence,rows,matches,report)
    print('pinned_RI52_dependency='+json.dumps(DEPENDENCIES,sort_keys=True))
    print('accepted_RI52_baseline=PASS active_components='+str(baseline['active_components']))
    print('bounded_coverage='+json.dumps(report['verification_counts'],sort_keys=True))
    print('dual_and_sharp_boundary='+json.dumps(result,sort_keys=True))
    print('root_manifest_sha256='+matrix['roots_sha256'])
    print('target_matrix_sha256='+matrix['matrix_sha256'])
    print('scalar_identities=768; full-D consequence is algebraic, no numerical payload or successor-row test')
    print('DONE: every marked B-row cap is below 1/2; the necessary gate is infeasible; sharpness is boundary-only')


if __name__ == '__main__':
    main()
