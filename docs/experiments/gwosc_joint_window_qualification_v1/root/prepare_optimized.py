"""Root creation of actual normal adjudication and a separate optimized card."""
import sys
from pathlib import Path
import importlib.util
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m',D/'metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=m.B/'ri121-synthetic-caller-repair-7ys8vsc3'
peer=Path(sys.argv[1]);m.verify(peer,{'bytes':int(sys.argv[2]),'sha256':sys.argv[3]})
f=m.load(S/'AUTHORIZED_FREEZE.json');r=f['runs']['normal']
check=m.load(D/'NORMAL_ROOT_SAVED_CUSTODY_CHECK.json')
math=m.load(D/'ROOT_SAVED_SCIENTIFIC_RECONSTRUCTION.json')
if check['status']!='ALL_SAVED_CUSTODY_GATES_PASS' or math['status']!='ALL_9_CASES_AND_3_BOUNDS_MATCH_IN_FULL':raise ValueError('root checks incomplete')
for dep in m.load(D/'ROOT_RUNTIME_ADJUDICATION.json')['required_root_custody']:m.verify(dep['path'],dep)
for key,other in [('receipt','receipt'),('result','stdout'),('worker','worker_receipt'),('custody','custody')]:
    if check[key if key!='result'else'report']!=m.ref(r[other]):raise ValueError('normal output drift')
review={'schema':'ri121-root-normal-synthetic-review-v1','status':'ACCEPT_NORMAL_SYNTHETIC_EXECUTION_AND_CUSTODY',
        'freeze':m.pure(m.identity(S/'AUTHORIZED_FREEZE.json')),'all41_controls_per_implementation':True,
        'complete_independent_saved_validation':True,'receipt':m.ref(r['receipt']),
        'result':m.ref(r['stdout']),'worker':m.ref(r['worker_receipt']),'custody':m.ref(r['custody']),
        'genuine_outer':m.ref(D/'NORMAL_OUTER_TOOL.json'),'independent_custody_review':m.ref(peer),
        'root_custody_check':m.ref(D/'NORMAL_ROOT_SAVED_CUSTODY_CHECK.json'),
        'root_full_scientific_reconstruction':m.ref(D/'ROOT_SAVED_SCIENTIFIC_RECONSTRUCTION.json'),
        'source_run_and_saved_review_boundary':'Actual captured qualifier.run executed the controls; source-qualified independent validator and new enumeration reference checked saved science in child. Root independent moment algebra reconstructs all case/bound fields, not historical controls or pointwise sign execution.',
        'claim':'Exact finite synthetic arithmetic qualification only; no empirical/calibration/native/physical validation.'}
print(m.save('ROOT_NORMAL_ADJUDICATION.json',review))
run=f['runs']['optimized']
card={'schema':'ri121-root-mode-admission-v1','status':'AUTHORIZED_SINGLE_SYNTHETIC_MODE',
      'mode':'optimized','phase':f['phase'],'freeze':m.pure(m.identity(S/'AUTHORIZED_FREEZE.json')),
      'caller_source_acceptance':f['evidence']['caller_source_acceptance'],
      'command':run['command'],'launcher_command':run['launcher_command'],
      'normal_acceptance':m.ref(D/'ROOT_NORMAL_ADJUDICATION.json')}
with (S/'ADMIT_OPTIMIZED.json').open('xb')as file:file.write(m.canonical(card))
print(m.save('OPTIMIZED_PREPARATION.json',{'normal_review':m.ref(D/'ROOT_NORMAL_ADJUDICATION.json'),'card':m.ref(S/'ADMIT_OPTIMIZED.json'),'freeze':m.ref(S/'AUTHORIZED_FREEZE.json'),'optimized_execution_so_far':False}))
