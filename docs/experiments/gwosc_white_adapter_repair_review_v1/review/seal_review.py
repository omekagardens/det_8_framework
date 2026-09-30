"""Administrative seal of RI156 review; never invokes a subject or control."""
import hashlib,importlib.util,json
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri156-independent-adapter-review-dko2kzl_';A=B/'ri156-white-external-adapter-source-1plzn4nm'
p=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=p.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('trusted metadata helper pin')
s=importlib.util.spec_from_file_location('trusted_metadata',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
expected=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','CHECK_V2.stderr','CHECK_V2.stdout','INDEPENDENT_SOURCE_REVIEW.md','METADATA_CHECK.json','METADATA_CHECK_V2.json','VERDICT.json','check_metadata.py','check_metadata_v2.py','seal_review.py']
if sorted(x.name for x in R.iterdir())!=sorted(expected):raise ValueError('unexpected review namespace')
report=m.load(R/'METADATA_CHECK_V2.json')
if report['status']!='PASS_ADMINISTRATIVE_NOT_SOURCE_OR_CONTROL_ACCEPTANCE' or len(report['observed'])!=508:raise ValueError('complete independent administrative report missing')
for row in report['observed']:
 if m.identity(row['path'])!=row:raise ValueError('source/dependency changed: '+row['path'])
H=m.load(A/'HANDOFF.json')
if sorted(x.name for x in A.iterdir())!=sorted(H['exact_namespace']):raise ValueError('author namespace changed')
for row in H['payloads']:m.verify(row['path'],row)
for name in expected:
 if (R/name).is_symlink() or not (R/name).is_file():raise ValueError('nonregular review member')
for name in ['INDEPENDENT_SOURCE_REVIEW.md','check_metadata.py','check_metadata_v2.py','seal_review.py']:
 text=(R/name).read_text()
 if any(x.rstrip()!=x for x in text.splitlines()):raise ValueError('trailing whitespace '+name)
 for marker in ['<<<<<<< ','======= ','>>>>>>> ']:
  if any(x.startswith(marker) for x in text.splitlines()):raise ValueError('conflict marker '+name)
preseal=[m.identity(R/name) for name in sorted(expected)]
m.save('FINAL_PIN_CHECK.json',{'schema':'ri156-independent-review-final-pin-check-v1','status':'PASS_ADMINISTRATIVE_ONLY','subject':m.ref(A/'HANDOFF.json'),'subject_namespace_count':26,'subject_payload_count':25,'fresh_complete_source_identity_rechecks':508,'preseal_review_namespace':sorted(expected),'preseal_review_identities':preseal,'subject_or_control_execution':False,'runtime_observation':False,'terminal_tool_completion':'External actual result to be reported to root after this source finishes; not self-authenticated.'})
names=sorted(expected+['FINAL_PIN_CHECK.json']);payloads=[m.ref(R/name) for name in names]
for row in preseal:
 if m.identity(row['path'])!=row:raise ValueError('review changed while sealing')
handoff={'schema':'ri156-independent-adapter-review-handoff-v1','status':'SEALED_COMPLETE_NONAUTHOR_NEW_SOURCE_REVIEW_FOR_ROOT_ADJUDICATION','reviewer':'/root/archive_repro_review','subject':m.ref(A/'HANDOFF.json'),'assignment':report['assignment'],'decision':'REQUIRE_F01_F02_CUSTODY_REPAIRS_BEFORE_QUALIFICATION_ADMISSION','findings':['F01 authenticated source baseline drift window','F02 final owned-output and saved-mode-root observations not reconciled to verified identities'],'root_adjudication_claimed':False,'namespace':sorted(names+['HANDOFF.json']),'payloads':payloads,'actual_administrative_run':{'tool_chunk':'dd4ebc','exit_code':0,'counts':report['counts']},'retained_diagnostics':'One failed filename read, original superseded administrative checker and outputs, both author failed-read records; see ACTUAL_CHECKS.json. No subject/control execution.','compact_public_review_subset':sorted([n for n in names if n not in ['METADATA_CHECK.json','METADATA_CHECK_V2.json']]+['HANDOFF.json']),'external_only_diagnostics':['METADATA_CHECK.json','METADATA_CHECK_V2.json'],'external_diagnostic_policy':'Both complete predicate/identity reports remain immutable and exactly pinned in this seal; compact publication may use their exact external references instead of duplicating repeated full identity dumps.','controls_defined':55,'controls_executed':0,'all_eleven_modules_read_completely':True,'new_modules_independently_reviewed':6,'unchanged_retained_modules_inherited':5,'prior_authorship_disclosed':True,'actual_monitor_runtime_source_qualification':False,'scientific_arithmetic_or_physical_acceptance':False,'RET_remains_paused':True,'successor_assigned':False,'root_owns_adjudication_execution_Git':True,'terminal_completion_not_self_authenticated':True}
ref=m.save('HANDOFF.json',handoff)
if sorted(x.name for x in R.iterdir())!=handoff['namespace']:raise ValueError('final review namespace mismatch')
for row in payloads:m.verify(row['path'],row)
print(json.dumps({'status':'SEALED','handoff':ref,'namespace_count':len(handoff['namespace']),'payload_count':len(payloads),'fresh_identity_rechecks':508},sort_keys=True))
