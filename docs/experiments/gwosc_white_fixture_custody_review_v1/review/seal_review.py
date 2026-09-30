"""Exclusive RI158 administrative review seal; no subject code is loaded."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path

R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri158-independent-repair-review-nxij3eju')
Q=R.parent/'ri158-white-custody-repair-68cdvzn6'
HELPER=R.parent/'ri122-root-execution-review-6whn_vky'/'metadata.py'
raw=HELPER.read_bytes()
if len(raw)!=3144 or hashlib.sha256(raw).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted administrative helper pin')
spec=importlib.util.spec_from_file_location('ri158_seal_trusted_metadata',HELPER)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.D=R
before=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_SOURCE_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(p.name for p in R.iterdir())!=sorted(before):raise ValueError('exclusive preseal review namespace')
report=m.load(R/'METADATA_CHECK.json')
if m.pure(m.identity(R/'METADATA_CHECK.json'))!={'bytes':759737,'sha256':'5597fa2d49190d53a909ae3fb1a6264afd00a408e813e2ee5118b078acd13d93'}:raise ValueError('review metadata result pin')
if len(report['observed_identities'])!=553:raise ValueError('full previous identity count')
for row in report['observed_identities']:
 if m.identity(row['path'])!=row:raise ValueError('full identity changed: '+row['path'])
if sorted(p.name for p in Q.iterdir())!=report['subject_namespace']:raise ValueError('subject final namespace')
subject=m.load(Q/'HANDOFF.json')
if sorted(subject['namespace'])!=report['subject_namespace'] or len(subject['payloads'])!=26:raise ValueError('subject seal closure')
for row in subject['payloads']:
 if Path(row['path']).parent!=Q or m.ref(row['path'])!=row:raise ValueError('subject payload identity')
verdict=m.load(R/'VERDICT.json')
if verdict['verdict']!='REQUIRE_F02_FIXTURE_NAMESPACE_RECONCILIATION_BEFORE_QUALIFICATION' or len(verdict['findings'])!=1:raise ValueError('review verdict closure')
if verdict['controls']!={'old_defined':55,'new_defined':29,'total_defined':84,'executed':0,'passed_claimed':0}:raise ValueError('unexecuted control scope')
if (R/'CHECK.stderr').stat().st_size!=0:raise ValueError('unexpected check stderr')
preidentities=[m.identity(R/name) for name in sorted(before)]
final=m.save('FINAL_PIN_CHECK.json',{'schema':'ri158-independent-source-review-final-pins-v1','status':'COMPLETE_OPAQUE_SOURCE_EVIDENCE_RECHECK_NOT_QUALIFICATION','subject':report['subject'],'assignment':report['assignment'],
 'source_files':27,'payloads':26,'dependency_count':525,'complete_fresh_identity_rechecks':553,'all_553_selection_states_unchanged':True,'subject_namespace':report['subject_namespace'],
 'review_preseal_files':[{k:x[k] for k in ('path','bytes','sha256')} for x in preidentities],'review_verdict':verdict['verdict'],'controls_executed':0,'scientific_decode':False,'subject_import_compile_AST_probe_run':False,'runtime_observed':False,'root_adjudication_required':True})
namespace=sorted(before+['FINAL_PIN_CHECK.json','HANDOFF.json'])
payloads=[m.ref(R/n) for n in namespace if n!='HANDOFF.json']
external=[m.ref(R/'METADATA_CHECK.json')]
public=[n for n in namespace if n!='METADATA_CHECK.json']
h=m.save('HANDOFF.json',{'schema':'ri158-independent-source-repair-review-handoff-v1','owner':'/root/archive_repro_review','reservation':str(R),'verdict':verdict['verdict'],'findings':['F02-R'],
 'subject':report['subject'],'assignment':report['assignment'],'prior_review':m.ref(R.parent/'ri156-independent-adapter-review-dko2kzl_'/'HANDOFF.json'),
 'independence':'Nonauthor of RI158 and new RI156 integration. Earlier WHITE/caller/bootstrap authorship and prior reviews disclosed; unchanged retained modules are inherited adjudicated premises, not new self-acceptance.',
 'namespace':namespace,'payloads':payloads,'compact_publication_subset':public,'external_only_diagnostics':external,
 'actual_administrative_check':{'chunk_id':'d5b033','exit_code':0,'predicates':3888,'dependencies':525,'inherited':481,'additions':44,'opaque_dependency_bytes':30301774,'fresh_identity_rechecks':553},
 'source_coverage':{'changed_modules_complete':2,'added_modules_complete':1,'unchanged_modules_byte_identical':9,'retained_modules_inherited_complete_read':5,'unchanged_saved_mode_functions':8,'source_diff_reconstructed':True},
 'controls':{'retained_defined':55,'new_defined':29,'total_defined':84,'executed':0},'final_source_pin_check':final,
 'boundaries':['Source review only; all controls unexecuted','No scientific decode/evaluation, subject import/compile/AST/probe/run or runtime observation','No operational cards/admissions, repository/Git/index work or successor assignment','F02-R must be root adjudicated and repaired before qualification; root owns publication and operations','Full current environment, R01, runtime/custody/arithmetic and normal-before-optimized obligations remain','RI131/full32/public-data/native claims separate; RET paused'],
 'genuine_seal_command_result':'Parent handoff reports actual tool result separately; this metadata does not authenticate an operational process.'})
if sorted(p.name for p in R.iterdir())!=namespace:raise ValueError('complete sealed review namespace')
for row in payloads:
 if m.ref(row['path'])!=row:raise ValueError('sealed review payload changed')
for row in preidentities:
 if m.identity(row['path'])!=row:raise ValueError('review selection changed during seal')
print(json.dumps({'handoff':h,'final_pin_check':final,'namespace_files':len(namespace),'payloads':len(payloads),'source_identity_rechecks':553,'verdict':verdict['verdict'],'status':'SEALED_SOURCE_REVIEW_REQUIRES_REPAIR_NOT_EXECUTION_ACCEPTANCE'},sort_keys=True))
