"""Root-only creation of concrete runtime acceptance, freeze and normal card."""
import sys
from pathlib import Path
import importlib.util

D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('m',D/'metadata.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
C=m.B/'ri121-runtime-candidate-rIMnamYh'
S=m.B/'ri121-synthetic-caller-repair-7ys8vsc3'
review=Path(sys.argv[1]);review_pin={'bytes':int(sys.argv[2]),'sha256':sys.argv[3]}
m.verify(review,review_pin)
accepted_review=m.load(review)
print('Binding independent actual review status:',accepted_review['status'])
for r in m.load(C/'HANDOFF.json')['files']:m.verify(r['path'],r)
source=m.B/'ri121-root-caller-review-e6_dha8i/ROOT_CALLER_SOURCE_ADJUDICATION.json'
m.verify(source,dict(bytes=5892,sha256='bda7bd10e58320c2912a4405fec16d0b386b34c7edb6f9f5b86869cf7e936f92'))
saved=m.load(D/'ROOT_SAVED_PROFILE_CHECK.json')
pre=m.load(D/'PRE_SCIENCE_RUNTIME_METADATA.json')
if pre['observed_dyld_routes']!=m.ref(D/'ACTUAL_DYLD_ROUTE_SIDECAR.json'):
    raise ValueError('root-side observed route custody missing')
if saved['status']!='ALL_SAVED_PROFILE_GATES_PASS':raise ValueError('saved profile gates')
manifest=m.load(S/'MANIFEST.source-only-template.json')
inventory_body=(C/'RUNTIME_INVENTORY.candidate.json').read_bytes()
with (D/'RUNTIME_INVENTORY.json').open('xb') as f:f.write(inventory_body)
runtime_row={'path':str(D/'RUNTIME_INVENTORY.json'),'pin':m.pin(inventory_body)}
acceptance={
 'schema':'ri121-root-current-runtime-adjudication-v1',
 'status':'ACCEPT_CURRENT_STDLIB_INTERPRETER_CLOSURE',
 'runtime_inventory':runtime_row,'interpreter':manifest['interpreter'],
 'expected_runtime':saved['expected_runtime'],
 'complete_pure_python_stdlib':True,'site_startup_surface_bound':True,
 'non_os_shared_library_closure_bound':True,'fresh_actual_profile_checked':True,
 'scientific_targets_executed':False,'independent_actual_review':m.ref(review),
 'source_acceptance':m.ref(source),
 'evidence':[m.ref(p)for p in [C/'HANDOFF.json',D/'ROOT_SAVED_PROFILE_CHECK.json',D/'PROFILE_NORMAL_OUTER_TOOL.json',D/'PROFILE_OPTIMIZED_OUTER_TOOL.json',D/'PRE_SCIENCE_RUNTIME_METADATA.json',m.B/'ri121-root-caller-review-e6_dha8i/ROOT_STATIC_CLOSURE_REVIEW.json']],
 'required_root_custody':[m.ref(p)for p in [D/'check_runtime_metadata.py',D/'metadata.py',D/'ACTUAL_DYLD_ROUTE_SIDECAR.json',C/'FILE_SELECTION_METADATA.candidate.json',C/'OPTIONAL_NATIVE_NAMESPACES.candidate.json']],
 'required_pre_post_record':'Every actual scientific mode requires a fresh complete root metadata record before/after with exact observed_dyld_routes sidecar ref, matching selection/file identity digest and optional namespaces, stable uname/SystemVersion. No absent/null sidecar accepted.',
 'premises':[
  'Trusted installed Python/package suppliers and captured executable source/cache alternatives. Header equality is not source-cache semantic equivalence; file/module descriptors are not a complete dynamic execution trace.',
  'Trusted Apple kernel/loader/shared-cache implementation and stable filesystem during the bounded run; visible uname/SystemVersion identity checked. No complete OS image or hermetic runtime claim.',
  'All applicable third-party binary/config bytes are pinned. Config has no active external include/engine; default algorithm use and legacy/engine conservative bytes retained. Available digest names are not provider identities.',
  'Actual Python decimal fallback observed in both modes after genuine missing-libmpdec3 ImportError; fixed eight absences plus three actual overlay/resolved routes and optlink are separately retained.',
  'Source/cache selection metadata, optional native namespaces and extra dyld routes are external root pre/post custody, not additions to unchanged runtime_support v2 in-process guards.',
 ],
 'qualification_boundary':'Runtime qualification only. Full synthetic scientific qualification must execute separately; no empirical/native/physical validation, release, or programme completion.',
}
print(m.save('ROOT_RUNTIME_ADJUDICATION.json',acceptance))
manifest['schema']='ri121-synthetic-qualification-freeze-v1'
manifest['status']='authorized_synthetic_qualification'
manifest['runtime_inventory']=runtime_row
manifest['expected_runtime']=saved['expected_runtime']
manifest['evidence']['caller_source_acceptance']=m.ref(source)
manifest['evidence']['runtime_acceptance']=m.ref(D/'ROOT_RUNTIME_ADJUDICATION.json')
with (S/'AUTHORIZED_FREEZE.json').open('xb')as f:f.write(m.canonical(manifest))
for mode in ('normal','optimized'):(S/'controls'/mode).mkdir(parents=True,exist_ok=False)
run=manifest['runs']['normal']
card={'schema':'ri121-root-mode-admission-v1','status':'AUTHORIZED_SINGLE_SYNTHETIC_MODE',
      'mode':'normal','phase':manifest['phase'],'freeze':m.pure(m.identity(S/'AUTHORIZED_FREEZE.json')),
      'caller_source_acceptance':m.ref(source),'command':run['command'],
      'launcher_command':run['launcher_command'],'normal_acceptance':None}
with (S/'ADMIT_NORMAL.json').open('xb')as f:f.write(m.canonical(card))
print(m.save('NORMAL_PREPARATION.json',{'runtime':m.ref(D/'ROOT_RUNTIME_ADJUDICATION.json'),'freeze':m.ref(S/'AUTHORIZED_FREEZE.json'),'card':m.ref(S/'ADMIT_NORMAL.json'),'optimized_admitted':False,'scientific_execution_so_far':False}))
