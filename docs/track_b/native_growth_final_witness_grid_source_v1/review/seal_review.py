"""Seal RI159 independent source review using only administrative identities."""
import hashlib
import importlib.util
import json
from pathlib import Path
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri159-independent-grid-review-p1uvnluc')
Q=R.parent/'ri159-final-witness-grid-source-47ofu03n'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted administrative helper pin')
spec=importlib.util.spec_from_file_location('ri159_seal_admin',HELPER);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
before=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_SOURCE_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(p.name for p in R.iterdir())!=sorted(before):raise ValueError('exclusive preseal review namespace')
if m.pure(m.identity(R/'METADATA_CHECK.json'))!={'bytes':3691552,'sha256':'9855f134e59bda76620b0537d49cd20c26aa9c49fcae0ae2194c7db173f7af2d'}:raise ValueError('own metadata report identity')
report=m.load(R/'METADATA_CHECK.json')
if len(report['observed_identities'])!=264:raise ValueError('full identity count')
for row in report['observed_identities']:
 if m.identity(row['path'])!=row:raise ValueError('changed full selection: '+row['path'])
if sorted(p.name for p in Q.iterdir())!=report['subject_namespace']:raise ValueError('source namespace changed')
h=m.load(Q/'HANDOFF.json')
if sorted(h['namespace'])!=report['subject_namespace'] or len(h['payloads'])!=10:raise ValueError('source seal closure')
for row in h['payloads']:
 if Path(row['path']).parent!=Q or m.ref(row['path'])!=row:raise ValueError('source payload drift')
v=m.load(R/'VERDICT.json')
if v['recommendation']!='ACCEPT_EXACT_UNEXECUTED_GRID_AUDIT_SOURCE_WITH_QUALIFICATION_PREREQUISITES' or v['blocking_source_findings']!=[]:raise ValueError('recommendation closure')
if v['cases_executed']!=0 or v['fixtures_created']!=0 or v['scope']['actual_grid_result'] is not None:raise ValueError('no runtime/scientific credit')
if v['fresh_coverage']['current_markdown_documents']!=5 or (R/'CHECK.stderr').stat().st_size!=0:raise ValueError('review coverage/diagnostic boundary')
pre=[m.identity(R/n) for n in sorted(before)]
f=m.save('FINAL_PIN_CHECK.json',{'schema':'ri159-independent-source-review-final-pin-check-v1','status':'OPAQUE_SOURCE_AND_REVIEW_IDENTITIES_STABLE_NOT_EXECUTION_ACCEPTANCE','subject':report['subject'],'assignment':report['assignment'],'subject_files':11,'subject_payloads':10,'dependency_count':252,'fresh_full_identity_rechecks':264,'historical_states_compared_to_current':False,'own_review_preseal_files':[{k:r[k] for k in ('path','bytes','sha256')} for r in pre],'recommendation':v['recommendation'],'cases_executed':0,'actual_grid_result':None,'root_adjudication_required':True})
namespace=sorted(before+['FINAL_PIN_CHECK.json','HANDOFF.json']);payloads=[m.ref(R/n) for n in namespace if n!='HANDOFF.json']
hand=m.save('HANDOFF.json',{'schema':'ri159-independent-grid-source-review-handoff-v1','owner':'/root/archive_repro_review','reservation':str(R),'recommendation':v['recommendation'],'blocking_source_findings':[],'subject':report['subject'],'assignment':report['assignment'],'prior_native_review':m.ref(R.parent/'ri157-independent-cap-review-wt1tl1ip'/'HANDOFF.json'),'namespace':namespace,'payloads':payloads,'compact_publication_subset':[n for n in namespace if n!='METADATA_CHECK.json'],'external_only_diagnostics':[m.ref(R/'METADATA_CHECK.json')],
 'independence':'Nonauthor of current producer/auditor/contract/provenance; prior WHITE/caller/bootstrap authorship and native/source reviewer involvement disclosed. RI157/root law premises inherited; no current self-acceptance.',
 'fresh_read_scope':{'producer_lines':374,'auditor_lines':521,'current_markdown_files':5,'Q_families':35,'R_families':16,'P_families':12,'case_execution_count':0,'actual_certificate_decoded':False},
 'actual_administrative_check':{'chunk_id':'111d3d','exit_code':0,'predicates':18296,'dependencies':252,'selected_bytes':16345304,'inherited_rows':223,'additions':29,'allowlisted_administrative_bodies':88,'historical_typed_refs':1981,'current_typed_refs':48,'extended_historical_identities':17,'source_pairs':4,'fresh_identities':264,'subject_namespace_files':11,'payloads':10},'final_pin_check':f,
 'qualification_prerequisites':[x['requirement'] for x in v['qualification_prerequisites']],
 'boundaries':['No actual grid result, capacity or W/C2/C3/sharedH30 decision','No subject import/compile/AST/probe/run, scientific decode/evaluation, fixture/runtime/card/admission/freeze','No repository/index/Git operations, new agents or successor assignment','Only authenticated trusted metadata helper executed by own bounded administrative scripts','All historical/source law premises, P2/P3,Y1/4,31/139/20/42,other8parents,fiveDi,sharedT1,multiplicity,strict endpoints remain','Physical/native-forward-map/calibration claims open; RET paused; measurement separate'],
 'genuine_seal_tool_outcome':'Reported separately in the parent handoff; this record does not authenticate an operational process.','root_owns_adjudication_admission_and_publication':True})
if sorted(p.name for p in R.iterdir())!=namespace:raise ValueError('final review namespace')
for row in payloads:
 if m.ref(row['path'])!=row:raise ValueError('sealed review payload changed')
for row in pre:
 if m.identity(row['path'])!=row:raise ValueError('review selection changed during seal')
print(json.dumps({'handoff':hand,'final_pin_check':f,'namespace_files':10,'payloads':9,'fresh_source_identity_rechecks':264,'recommendation':v['recommendation'],'status':'SEALED_UNEXECUTED_SOURCE_REVIEW_NOT_QUALIFICATION'},sort_keys=True))
