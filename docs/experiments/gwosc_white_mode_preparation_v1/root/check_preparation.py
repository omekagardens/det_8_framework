"""Root independent administrative binding reconciliation; no scientific import/decode."""
import importlib.util
from pathlib import Path
sp=importlib.util.spec_from_file_location('metadata','/Volumes/AI_DATA/development/det-review-evidence/ri122-root-execution-review-6whn_vky/metadata.py')
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);m.D=Path(__file__).resolve().parent
S=m.B/'ri154-white-mode-preparation-42_uvw15'; OLD=m.B/'ri130-white-qualification-caller-source-Q4Aq7hZg'; Q=m.B/'ri141-white-bootstrap-source-h58ls076'; checks=[]; identities={}
def need(ok,label):
 checks.append(dict(check=label,passed=bool(ok)))
 if not ok:raise ValueError(label)
def verify(row):
 p=Path(row['path']);need(p.is_relative_to(m.B) or p.is_relative_to(m.REPO),'permitted source/evidence input '+str(p));need('/env/' not in str(p),'not installed runtime '+str(p))
 r=m.verify(p,row);need(not r['symlink_chain'],'literal opaque input '+str(p));identities[str(p)]=r;return r
def admin(p):
 r=m.ref(p);verify(r);return m.load(p)
h=admin(S/'HANDOFF.json');need(m.pure(m.ref(S/'HANDOFF.json'))==dict(bytes=7336,sha256='48aa2c11468fab405a1e15793916c42e38ee4562a6212d71987149076c8814d6'),'fixed author handoff')
for row in h['files']:verify(row)
need(sorted(p.name for p in S.iterdir())==h['exact_namespace'],'closed15 source namespace')
need(len(h['files'])==14 and len(h['exact_namespace'])==15,'source closure counts')
d=admin(S/'DEPENDENCIES.json');g=admin(S/'BINDING_GRAPH.source-only.json');a=admin(S/'PREPARATION_CHECK.json');f=admin(S/'INTERFACE_FIELDS.source-only.json');old=admin(OLD/'HANDOFF.json');t=admin(OLD/'TARGET_CLOSURE.source-only.json');hist=admin(OLD/'HISTORY_CLOSURE.source-only.json');inherited=admin(Q/'DEPENDENCIES.source-only.json')
E=Path(g['prospective_root']);need(E==m.B/'ri154-white-execution-proposed-42_uvw15' and not E.exists() and not E.is_symlink(),'prospective root absent and exact')
need(len(d['complete_read_files'])==463 and len({r['path'] for r in d['complete_read_files']})==463,'463 unique input identities')
for row in d['complete_read_files']:verify(row)
need(d['inherited_ri141']==inherited['opaque_files'] and len(d['inherited_ri141'])==442,'whole442 inherited declaration')
for row in d['inherited_ri141']:verify(row)
need(g['evidence']==d['direct_premises'] and len(g['evidence'])==19,'whole19 named current premises')
for row in g['evidence'].values():verify(row)
old_names=sorted(['HANDOFF.json']+[r['relative'] for r in old['artifacts']]);need(len(old_names)==48,'original48 names')
need(sorted(str(p.relative_to(OLD)) for p in OLD.rglob('*') if p.is_file())==old_names and not any(p.is_symlink() for p in OLD.rglob('*')),'exact original48 namespace')
expected=[]
for name in old_names:
 r=m.ref(OLD/name);verify(r);expected.append(dict(relative=name,source=r,destination=str(E/name)))
need(g['copied_files']==expected and g['copied_file_count']==48,'whole48 deterministic copies')
expected=[]
for row in t['sources']:
 verify(dict(path=row['original'],**row['pin']));verify(dict(path=str(OLD/row['relative']),**row['pin']))
 expected.append(dict(relative=row['relative'],original=row['original'],copy=str(E/row['relative']),pin=row['pin']))
need(g['sources']==expected and len(expected)==g['target_count']==30,'all30 original/copy target mappings')
helper_names=['control.py','runtime_support.py','caller_contract.py','evidence.py','monitor.py','worker.py','launch.py','profile_observe.source-only.py','guard_controls.source-only.py','TARGET_CLOSURE.source-only.json','HISTORY_CLOSURE.source-only.json']
expected=[dict(path=str(E/n),pin=m.pure(m.ref(OLD/n))) for n in helper_names]
need(g['helpers']==expected and len(expected)==g['helper_count']==11,'all11 ordered helpers')
need(g['history_originals']==hist and g['history_count']==len(hist)==124,'whole124 original historical roles')
for row in hist:verify(row)
roles={'white_kernel':'science/primary/white_kernel.py','white_path':'science/primary/white_path.py','wrapper_controls':'science/primary/white_controls.py','white_contract':'science/primary/CONTRACT.md','cases':'science/primary/CASES.md','kernel_refusals':'science/primary/KERNEL_REFUSALS.md','fabricated_interfaces':'science/primary/FABRICATED_INTERFACES.md','white_refusals_text':'science/primary/WHITE_REFUSALS.md','white_source_handoff':'science/primary/HANDOFF.json','fixtures':'science/qualifier/white_fixtures.py','kernel_controls':'science/qualifier/kernel_controls.py','orchestrator':'science/qualifier/qualify_white_only.py','stage_contract':'science/qualifier/STAGE_CONTRACT.md','control_expectations':'science/qualifier/CONTROL_EXPECTATIONS.json','validator':'science/validator/white_validator.py','validator_controls':'science/validator/validator_controls.py'}
by_name={r['relative']:r for r in t['sources']};expected={k:dict(path=str(E/v),pin=by_name[v]['pin']) for k,v in roles.items()};expected['white_root_disposition']=dict(path=t['white_root']['path'],pin=m.pure(t['white_root']))
need(g['stage_bindings']==expected and g['stage_role_count']==len(expected)==17,'whole17 stage role map')
need(g['integrated_root']==t['integrated_root'],'unchanged integration disposition');verify(t['white_root']);verify(t['integrated_root'])
guard=admin(Path(g['evidence']['guard_acceptance']['path']));profiles=admin(Path(g['evidence']['profiles_acceptance']['path']))
need(len(guard['helpers'])==11 and g['prior_original_guard_helpers']==guard['helpers'],'whole original guard helper map')
need(guard['helpers']==[dict(path=str(OLD/n),pin=m.pure(m.ref(OLD/n))) for n in helper_names],'original guard11 exact paths/pins')
need(guard['helpers']!=g['helpers'],'R01 literal path mismatch')
need(profiles['packet']==str(OLD) and profiles['environment_root']==g['old_environment_root'] and profiles['environment_root']!=str(E),'R02 old environment cannot be reused verbatim')
need(g['proposed_environment']=={'PATH':'/usr/bin:/bin','LC_ALL':'C','TZ':'UTC','TMPDIR':str(E/'tmp'),'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'},'exact ten-field proposed environment')
need(len(a['checks'])==4071 and all(set(x)=={'check','passed'} and type(x['check']) is str and x['passed'] is True for x in a['checks']),'whole author administrative predicate report; not independent qualification')
need(a['counts']=={'ri130_files':48,'prospective_copies':48,'target_pairs':30,'helpers':11,'history_roles':124,'stage_roles':17,'inherited_dependencies':442,'unique_opaque_inputs':463},'whole author count declaration')
need(set(f['field_counts'])==set(f['field_sets']) and all(len(v)==len(set(v))==f['field_counts'][k] for k,v in f['field_sets'].items()),'all22 field sets exact count and no duplicates')
need(len(f['field_sets'])==22,'22 declared field inventories')
need(a['prohibited_actions_performed']==[] and a['qualification_claim'] is False and a['driver_implemented'] is False and a['proposed_root_created'] is False,'author scope retained')
need(g['root_created'] is False and g['source_changes']==[] and g['all_proposed_copies_uncreated'] is True,'proposed source only')
need([x['id'] for x in h['current_applicability_gaps']]==['R01','R02','R03','R04'],'four explicit readiness gaps')
# Recheck whole observed files after all comparisons; this is an opaque read-window observation.
for p,r in sorted(identities.items()):need(m.identity(p)==r,'final full identity unchanged '+p)
need(sorted(p.name for p in S.iterdir())==h['exact_namespace'] and not E.exists() and not E.is_symlink(),'final closed source namespace and proposed absence')
print(m.save('SOURCE_RECONCILIATION.json',dict(schema='ri154-root-source-reconciliation-v1',status='PASS',checks=checks,opaque_identities=list(identities.values()),unique_observed=len(identities),source_files=15,declared_inputs=463,inherited_inputs=442,author_report_predicates=4071,counts=a['counts'],field_inventory_count=22,scientific_import_compile_ast_probe_decode_execution=False,current_runtime_observation=False,proposed_root_created=False,operational_qualification=False)))
