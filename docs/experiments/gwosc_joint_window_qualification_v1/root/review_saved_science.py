"""Independent finite moment reconstruction of saved fields; no target imports.

Uses E[zz^T]=I for independent symmetric signs. No sign cube or controls rerun.
All fixed model choices are stated here; no expected matrix comes from the report.
"""
from fractions import Fraction as Q
from pathlib import Path
import importlib.util

D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m',D/'metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=m.B/'ri121-synthetic-caller-repair-7ys8vsc3'
body=(S/'controls/normal/RESULT.json').read_bytes()
report=m.load(S/'controls/normal/RESULT.json');science=report['scientific_result']
def need(v,s):
    if not v:raise ValueError(s)
def enc(x):
    if type(x)is Q:return str(x)
    if type(x)is list:return [enc(v)for v in x]
    if type(x)is dict:return {k:enc(v)for k,v in x.items()}
    return x
def transpose(a):return [list(c)for c in zip(*a)]
def product(a,b):
    return [[sum((x*y for x,y in zip(row,col)),Q(0))for col in zip(*b)]for row in a]
def trace(a):return sum((a[i][i]for i in range(len(a))),Q(0))
def same(actual,expected,label):need(m.canonical(actual)==m.canonical(enc(expected)),label)

ids=['Q02_white_two','Q03_periodic_two','Q05_white_three','Q06_constant_mean','Q07_quadratic_mean','Q08_scale_minus_one','Q08_scale_two','Q09_oriented_matrix','Q10_zero_map']
need([r['id']for r in science['cases']]==ids,'case inventory')
checks=[]
for index,case_id in enumerate(ids):
    n=3 if index in (2,4)else 2
    starts=list(range(0,2*n,2));size=2*n+2;latent=4 if index==1 else size
    q=2 if index==7 else 1;scale=Q(-1 if index==5 else 2 if index==6 else 1)
    a=[[Q(1),Q(0),Q(-1)]]
    if q==2:a+=[[Q(0),Q(1),Q(-1)]]
    if index==8:a=[[Q(0)]*3]
    factor=[[Q(int(j==(i%4 if index==1 else i)))for j in range(latent)]for i in range(size)]
    mean=[Q(3 if index==3 else i*i if index==4 else 0)for i in range(size)]
    model={'kind':'shared_periodic' if index==1 else 'shared_raw_white','M':4,'T':3,'stride':2,'n':n,'starts':starts,'raw_length':size,'latent_dimension':latent,'output_dimension':q,'A':a,'raw_factor':factor,'raw_mean':mean,'scale':scale}
    raw_mean=[scale*x for x in mean]
    raw_cov=[[scale*scale*x for x in row]for row in product(factor,transpose(factor))]
    selector=lambda start,length:[[int(j==start+i)for j in range(size)]for i in range(length)]
    output=[[row[j-start]if start<=j<start+3 else Q(0)for j in range(size)]for start in starts for row in a]
    out_mean=[row[0]for row in product(output,[[v]for v in raw_mean])]
    out_cov=product(product(output,raw_cov),transpose(output))
    avg=[[Q(int(j%q==i),n)for j in range(n*q)]for i in range(q)]
    bar_mean=[row[0]for row in product(avg,[[v]for v in out_mean])]
    bar_cov=product(product(avg,out_cov),transpose(avg))
    centered=[[sum((out_cov[k*q+i][k*q+j]for k in range(n)),Q(0))/n-bar_cov[i][j]for j in range(q)]for i in range(q)]
    dispersion=sum(((out_mean[k*q+i]-bar_mean[i])**2 for k in range(n)for i in range(q)),Q(0))/n
    covariance=trace(centered);v=covariance+dispersion
    u=(trace(out_cov)+sum((x*x for x in out_mean),Q(0)))/n
    bar_energy=trace(bar_cov)+sum((x*x for x in bar_mean),Q(0))
    need(u==v+bar_energy,'energy decomposition')
    expected={'id':case_id,'model':model,'selectors_M':[selector(s,4)for s in starts],'selectors_T':[selector(s,3)for s in starts],
              'output_map':output,'raw_mean':raw_mean,'raw_covariance':raw_cov,
              'window_marginal_covariances':[[[raw_cov[s+i][s+j]for j in range(4)]for i in range(4)]for s in starts],
              'stacked_output_mean':out_mean,'stacked_output_covariance':out_cov,
              'cross_blocks':[[[[out_cov[aa*q+i][bb*q+j]for j in range(q)]for i in range(q)]for bb in range(n)]for aa in range(n)],
              'mean_output_covariance':bar_cov,'centered_covariance_average':centered,
              'mean_dispersion':dispersion,'covariance_contribution':covariance,'expected_V':v,'direct_average_V':v,'expected_U':u,'mean_output_energy':bar_energy,'sign_count':2**latent}
    same(science['cases'][index],expected,'entire case '+case_id)
    checks.append({'case':case_id,'entire_fields':len(expected),'V':str(v),'U':str(u),'mean_output_energy':str(bar_energy),'mean_dispersion':str(dispersion)})
    if index==7:
        need(expected['cross_blocks'][0][1]==[[Q(-1),Q(0)],[Q(-1),Q(0)]],'Q09 directed block')
        need(centered==[[Q(3,2),Q(3,4)],[Q(3,4),Q(1)]],'Q09 centered full matrix')
pi=[[Q(1,2),Q(-1,2)],[Q(-1,2),Q(1,2)]];d=[[Q(1)],[Q(-1)]]
weight=trace(product(product(pi,product(d,transpose(d))),pi))/2
need(weight==1,'Q12 weight')
bounds=[{'id':'Q12_calibrated_constant','A':[[Q(1),Q(0),Q(-1)]],'C_cal':[[Q(1),Q(0),Q(0)],[Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(2)]],'input':[Q(1)]*3,'output':[Q(-1)],'constant_annihilation_claim':False,'output_dimension':1},
        {'id':'Q12_covariance_error','D':d,'Pi':pi,'Sigma_model':[[Q(1)]],'Sigma_true':[[Q(2)]],'eta':Q(1),'n':2,'output_dimension':1,'model_contribution':weight,'true_contribution':2*weight,'absolute_difference':weight,'bound':weight},
        {'id':'Q12_calibration_error','D':d,'Pi':pi,'F':[[Q(1)]],'C0':[[Q(1)]],'DeltaC':[[Q(1)]],'n':2,'output_dimension':1,'model_contribution':weight,'true_contribution':4*weight,'absolute_difference':3*weight,'bound':3*weight}]
same(science['bounds'],bounds,'entire bounds')
same(science['groups'],['Q'+str(i).zfill(2)for i in range(1,13)],'groups')
need(report['control_count_per_implementation']==41,'controls count')
for key,count in [('mutation_refusals',33),('parser_refusals',5),('psd_refusals',3)]:
    need(len(report[key])==count and all(r['primary']==r['validator']==r['expected']for r in report[key]),'saved labels '+key)
need((S/'controls/normal/RESULT.json').read_bytes()==body,'saved file drift')
print(m.save('ROOT_SAVED_SCIENTIFIC_RECONSTRUCTION.json',{'status':'ALL_9_CASES_AND_3_BOUNDS_MATCH_IN_FULL','saved_report':m.ref(S/'controls/normal/RESULT.json'),'review_source':m.ref(D/'review_saved_science.py'),'cases':checks,'bounds_full_fields_compared':True,'rational_route':'Independent fixed-model linear moment algebra, no expected matrix from saved report and no target imports or sign enumeration.','actual_controls_reexecuted':False,'pointwise_control_execution':'Separate captured normal worker and genuine custody; saved algebra alone does not witness execution.','claim':'Exact finite synthetic arithmetic only; no empirical/calibration/native/physical claim.'}))
