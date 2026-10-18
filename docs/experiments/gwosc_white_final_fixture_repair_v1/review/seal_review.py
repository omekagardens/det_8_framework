"""Seal RI160 independent review by administrative identities only."""
import hashlib
import importlib.util
import json
from pathlib import Path
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri160-independent-fixture-review-zhizl2vs')
Q=R.parent/'ri160-white-fixture-custody-repair-ufok1zpo'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted administrative helper pin')
spec=importlib.util.spec_from_file_location('ri160_seal_admin',HELPER);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
before=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_SOURCE_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(p.name for p in R.iterdir())!=sorted(before):raise ValueError('exclusive preseal review namespace')
if m.pure(m.identity(R/'METADATA_CHECK.json'))!={'bytes':817604,'sha256':'67b5f3aadf78538adfd48c1019b5ac84ba3bff100d00ee32497a079e484cce93'}:raise ValueError('own metadata report identity')
report=m.load(R/'METADATA_CHECK.json')
if len(report['observed_identities'])!=599:raise ValueError('full identity count')
for row in report['observed_identities']:
 if m.identity(row['path'])!=row:raise ValueError('changed full selection: '+row['path'])
if sorted(p.name for p in Q.iterdir())!=report['subject_namespace']:raise ValueError('source namespace changed')
h=m.load(Q/'HANDOFF.json')
if sorted(h['namespace'])!=report['subject_namespace'] or len(h['payloads'])!=30:raise ValueError('source seal closure')
for row in h['payloads']:
 if Path(row['path']).parent!=Q or m.ref(row['path'])!=row:raise ValueError('source payload drift')
v=m.load(R/'VERDICT.json')
if v['recommendation']!='ACCEPT_EXACT_UNEXECUTED_FIXTURE_CUSTODY_REPAIR_SOURCE_WITH_QUALIFICATION_PREREQUISITES' or v['blocking_findings']!=[]:raise ValueError('recommendation closure')
if v['controls']!={'retained':84,'new':22,'defined':106,'executed':0} or v['runtime_or_scientific_acceptance'] is not False:raise ValueError('no runtime credit')
if (R/'CHECK.stderr').stat().st_size!=0:raise ValueError('unexpected checker stderr')
pre=[m.identity(R/n) for n in sorted(before)]
f=m.save('FINAL_PIN_CHECK.json',{'schema':'ri160-independent-source-review-final-pin-check-v1','status':'OPAQUE_SOURCE_AND_REVIEW_IDENTITIES_STABLE_NOT_EXECUTION_ACCEPTANCE','subject':report['subject'],'assignment':report['assignment'],'subject_files':31,'subject_payloads':30,'dependency_count':567,'fresh_full_identity_rechecks':599,'historical_states_compared_to_current':False,'own_review_preseal_files':[{k:r[k] for k in ('path','bytes','sha256')} for r in pre],'recommendation':v['recommendation'],'controls_executed':0,'root_adjudication_required':True})
namespace=sorted(before+['FINAL_PIN_CHECK.json','HANDOFF.json']);payloads=[m.ref(R/n) for n in namespace if n!='HANDOFF.json']
hand=m.save('HANDOFF.json',{'schema':'ri160-independent-fixture-source-review-handoff-v1','owner':'/root/archive_repro_review','reservation':str(R),'recommendation':v['recommendation'],'blocking_findings':[],'subject':report['subject'],'assignment':report['assignment'],'predecessor_review':m.ref(R.parent/'ri158-independent-repair-review-nxij3eju'/'HANDOFF.json'),'namespace':namespace,'payloads':payloads,'compact_publication_subset':[n for n in namespace if n!='METADATA_CHECK.json'],'external_only_diagnostics':[m.ref(R/'METADATA_CHECK.json')],
 'independence':'Nonauthor of RI160 or RI156/RI158 adapter. Earlier separate WHITE validator/caller/preparation/bootstrap authorship and RI156/RI158 independent reviewer roles disclosed; inherited accepted originals not new self-review.',
 'fresh_coverage':{'adapter_lines':289,'integration_controls_lines':402,'changed_modules_complete':2,'new_controls_individually_traced':22,'unchanged_entire_executables':10,'unchanged_adapter_functions':8,'unchanged_integration_function_bodies':4,'entire_patch_reconstructed':True,'retained_control_ids':84},
 'source_finding':'RI158 F02-R addressed by two whole normalized fixture comparisons from the same final scan, with full mismatch collection and retained primary/partial behavior.',
 'actual_administrative_check':{'chunk_id':'f7ec63','exit_code':0,'stderr_empty':True,'predicates':4167,'dependencies':567,'selected_bytes':31853372,'inherited_rows':525,'additions':42,'fresh_identities':599,'subject_namespace_files':31,'payloads':30},'final_pin_check':f,
 'controls':{'retained':84,'new':22,'defined':106,'executed':0},'qualification_prerequisites':v['pending'],
 'boundaries':['No subject/control/helper import, compile, AST, probe or execution; only authenticated trusted administrative helper used by own metadata scripts','No scientific decode/evaluation, fixtures, runtime observations, operational cards/freezes/admissions','No repository/index/Git, historical edits, new agents or successor assignment','No actual106 pass, whole-entry/current-E/R01 qualification or saved scientific/arithmetic acceptance','All historical resource, genuine origin, loader/cache, supplier, normal-before-optimized, complete57/74/3 and full27/13/30 premises retained','RI131 actual-validator, actual15 WHITE/full32/public-data and physical/native-forward-map/calibration claims separate; RET paused'],
 'diagnostics':'Own checker succeeded first run. Author failed lookup and clipped display/recoveries remain exact pinned evidence. Own administrative source marker corrected before first run. All details retained in ACTUAL_CHECKS.',
 'genuine_seal_tool_outcome':'Reported separately in parent handoff; this record does not authenticate an operational process.','root_owns_adjudication_admission_successors_and_publication':True})
if sorted(p.name for p in R.iterdir())!=namespace:raise ValueError('final review namespace')
for row in payloads:
 if m.ref(row['path'])!=row:raise ValueError('sealed review payload changed')
for row in pre:
 if m.identity(row['path'])!=row:raise ValueError('review selection changed during seal')
print(json.dumps({'handoff':hand,'final_pin_check':f,'namespace_files':10,'payloads':9,'fresh_source_identity_rechecks':599,'recommendation':v['recommendation'],'status':'SEALED_UNEXECUTED_SOURCE_REVIEW_NOT_QUALIFICATION'},sort_keys=True))
