"""Administrative seal of RI161 independent review; no subject execution."""
import hashlib
import importlib.util
import json
from pathlib import Path
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri161-independent-qualification-review-2gvpjm9r');Q=R.parent/'ri161-grid-qualification-source-679wwadg'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted admin helper pin')
spec=importlib.util.spec_from_file_location('ri161_seal_admin',HELPER);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
before=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_SOURCE_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(p.name for p in R.iterdir())!=sorted(before):raise ValueError('exclusive preseal namespace')
if m.pure(m.identity(R/'METADATA_CHECK.json'))!={'bytes':4305399,'sha256':'5e438544e102b089b5f3bb317b83407577544bb8796b050b4842bbe8de272dfc'}:raise ValueError('own metadata pin')
x=m.load(R/'METADATA_CHECK.json')
if len(x['observed_identities'])!=292:raise ValueError('identity count')
for row in x['observed_identities']:
 if m.identity(row['path'])!=row:raise ValueError('changed selection: '+row['path'])
if sorted(p.name for p in Q.iterdir())!=x['subject_namespace']:raise ValueError('source namespace drift')
h=m.load(Q/'HANDOFF.json')
if sorted(h['namespace'])!=x['subject_namespace'] or len(h['payloads'])!=10:raise ValueError('source closure')
for row in h['payloads']:
 if Path(row['path']).parent!=Q or m.ref(row['path'])!=row:raise ValueError('source payload drift')
v=m.load(R/'VERDICT.json')
if v['recommendation']!='ACCEPT_EXACT_UNEXECUTED_GRID_QUALIFICATION_SOURCE_WITH_EXECUTION_PREREQUISITES' or v['blocking_source_findings']!=[]:raise ValueError('recommendation')
if v['actual']['source_control_execution']!=0 or v['actual']['actual_grid_result'] is not None:raise ValueError('unexecuted boundary')
if (R/'CHECK.stderr').stat().st_size!=0:raise ValueError('checker diagnostic boundary')
pre=[m.identity(R/n) for n in sorted(before)]
f=m.save('FINAL_PIN_CHECK.json',{'schema':'ri161-independent-qualification-review-final-pin-check-v1','status':'OPAQUE_SOURCE_AND_REVIEW_IDENTITIES_STABLE_NOT_EXECUTION_ACCEPTANCE','subject':x['subject'],'assignment':x['assignment'],'subject_files':11,'subject_payloads':10,'dependencies':280,'fresh_full_identity_rechecks':292,'historical_state_compared_to_current':False,'own_review_preseal_files':[{k:r[k] for k in ('path','bytes','sha256')} for r in pre],'recommendation':v['recommendation'],'cases_executed':0,'actual_grid_result':None,'root_adjudication_required':True})
namespace=sorted(before+['FINAL_PIN_CHECK.json','HANDOFF.json']);payloads=[m.ref(R/n) for n in namespace if n!='HANDOFF.json']
hand=m.save('HANDOFF.json',{'schema':'ri161-independent-qualification-source-review-handoff-v1','owner':'/root/archive_repro_review','reservation':str(R),'recommendation':v['recommendation'],'blocking_source_findings':[],'subject':x['subject'],'assignment':x['assignment'],'accepted_subject_prior_review':m.ref(R.parent/'ri159-independent-grid-review-p1uvnluc'/'HANDOFF.json'),'namespace':namespace,'payloads':payloads,'compact_publication_subset':[n for n in namespace if n!='METADATA_CHECK.json'],'external_only_diagnostics':[m.ref(R/'METADATA_CHECK.json')],
 'independence':'Nonauthor of all three current sources and both RI159 subjects. Prior native reviewer and separate historical WHITE validator/caller/bootstrap author; accepted old material not fresh self-review.',
 'fresh_coverage':v['fresh_coverage'],'planned_counts':v['planned_counts'],'actual_cases_executed':0,
 'actual_administrative_check':{'chunk_id':'83ba9b','exit_code':0,'stderr_empty':True,'predicates':21368,'dependencies':280,'selected_bytes':24169856,'inherited_rows':252,'additions':28,'administrative_bodies':98,'historical_typed_refs':2335,'current_typed_refs':49,'historical_identity_state_noncomparisons':17,'source_pairs':4,'fresh_identities':292,'subject_namespace_files':11,'payloads':10},'final_pin_check':f,
 'execution_prerequisites':v['required_prerequisites'],'boundaries':['No source/control/helper import,compile,AST,probe or execution; only authenticated administrative metadata helper loaded by separate own scripts','No scientific decode/evaluation, fixture creation, runtime observation/card/freeze/admission','No repository/index/Git, predecessor edits, new agents or successor assignment','Source-counted2547per-mode/5094two-mode are not executed outcomes','Root genuine bootstrap/host/runtime supervision, finite custody, hard-abort/kernel, address-space-not-RSS limitations retained','Actual grid/capacity/q-v/W/C2/C3/H30/globalM6-rho and physical/native-geometry/gravity conclusions remain open; all original fixed obligations retained','QP04 separate later actual-input admission; RET paused, measurement separate'],
 'diagnostics':'Own admin checker first run exit0; one aggregate old-source display clipped and complete affected span recovered. Full author failed search/incidental diagnostic/recoveries retained as declared historical evidence.',
 'genuine_seal_tool_outcome':'Reported separately from actual final tool return; this record does not self-authenticate an operational result.','root_owns_adjudication_admission_successors_and_publication':True})
if sorted(p.name for p in R.iterdir())!=namespace:raise ValueError('final review namespace')
for row in payloads:
 if m.ref(row['path'])!=row:raise ValueError('sealed payload changed')
for row in pre:
 if m.identity(row['path'])!=row:raise ValueError('review changed during seal')
print(json.dumps({'handoff':hand,'final_pin_check':f,'namespace_files':10,'payloads':9,'fresh_source_identity_rechecks':292,'recommendation':v['recommendation'],'status':'SEALED_UNEXECUTED_SOURCE_REVIEW_NOT_QUALIFICATION'},sort_keys=True))
