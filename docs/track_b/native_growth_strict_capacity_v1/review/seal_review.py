"""RI155 review seal: administrative identities only, no subject execution."""
import hashlib, importlib.util, json
from pathlib import Path
R=Path('/Volumes/AI_DATA/development/det-review-evidence/ri155-independent-capacity-review-3gu50gvs')
A=R.parent/'ri155-strict-capacity-proof-jv0xliup'
p=R.parent/'ri122-root-execution-review-6whn_vky/metadata.py'
b=p.read_bytes()
if len(b)!=3144 or hashlib.sha256(b).hexdigest()!='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7':raise ValueError('metadata helper pin')
s=importlib.util.spec_from_file_location('trusted_metadata',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
expected=['ACTUAL_CHECKS.json','CHECK.stderr','CHECK.stdout','INDEPENDENT_PROOF_REVIEW.md','METADATA_CHECK.json','VERDICT.json','check_metadata.py','seal_review.py']
if sorted(x.name for x in R.iterdir())!=sorted(expected):raise ValueError('unexpected review preseal namespace')
for n in expected:
 if (R/n).is_symlink() or not (R/n).is_file():raise ValueError('review payload not regular')
report=m.load(R/'METADATA_CHECK.json')
if report['status']!='PASS_NOT_MATHEMATICAL_PROOF' or len(report['observed'])!=204:raise ValueError('prior check not complete')
for row in report['observed']:
 if m.identity(row['path'])!=row:raise ValueError('fresh source drift: '+row['path'])
H=m.load(A/'HANDOFF.json')
if sorted(x.name for x in A.iterdir())!=sorted(H['namespace']) or len(H['namespace'])!=10 or len(H['payloads'])!=9:raise ValueError('author namespace drift')
for row in H['payloads']:m.verify(row['path'],row)
for n in ['INDEPENDENT_PROOF_REVIEW.md','check_metadata.py','seal_review.py']:
 text=(R/n).read_text()
 if any(line.rstrip()!=line for line in text.splitlines()):raise ValueError('trailing whitespace '+n)
 for marker in ['<<<<<<< ','======= ','>>>>>>> ']:
  if any(line.startswith(marker) for line in text.splitlines()):raise ValueError('conflict marker '+n)
preseal=[m.identity(R/n) for n in sorted(expected)]
final={'schema':'ri155-independent-final-pin-check-v1','status':'PASS_ADMINISTRATIVE_ONLY','subject':m.ref(A/'HANDOFF.json'),'subject_namespace':sorted(H['namespace']),'subject_payloads_verified':9,'fresh_full_identity_rechecks':204,'preseal_review_namespace':sorted(expected),'preseal_review_identities':preseal,'scientific_body_decode':False,'subject_execution':False,'new_mathematical_evaluation_by_checker':False,'terminal_tool_completion':'external to this record; root receives actual final tool result'}
m.save('FINAL_PIN_CHECK.json',final)
names=sorted(expected+['FINAL_PIN_CHECK.json'])
payloads=[m.ref(R/n) for n in names]
for row in preseal:
 if m.identity(row['path'])!=row:raise ValueError('review source drift during seal')
handoff={'schema':'ri155-independent-proof-review-handoff-v1','status':'SEALED_NONAUTHOR_PROOF_REVIEW_FOR_ROOT_ADJUDICATION','reviewer':'/root/archive_repro_review','subject':m.ref(A/'HANDOFF.json'),'assignment':report['assignment'],'decision':'ACCEPT_ACTUAL_FIRST_CAPACITY_AND_EXACT_STRICT_REDUCTION_WITH_CORRELATED_CONTRAST_GAP','root_adjudication_claimed':False,'repair_findings':[],'actual_administrative_check':{'tool_chunk':'bf2a4f','exit_code':0,'counts':report['counts']},'final_fresh_identity_check':m.ref(R/'FINAL_PIN_CHECK.json'),'namespace':sorted(names+['HANDOFF.json']),'payloads':payloads,'compact_public_review_subset':['INDEPENDENT_PROOF_REVIEW.md','VERDICT.json','ACTUAL_CHECKS.json','CHECK.stdout','CHECK.stderr','check_metadata.py','seal_review.py','FINAL_PIN_CHECK.json','HANDOFF.json'],'external_only_diagnostic_files':['METADATA_CHECK.json'],'external_only_diagnostic_reason':'Complete approximately 2 MB predicate/reference/identity occurrence record is preserved externally and bound by this handoff; compact publication need not duplicate it. It remains part of the complete review seal.','remaining_actual_premise':'Same actual canonical-prefix strict contrast v>B; a pass still needs the adequate q/v budget. Equality fails the sufficient capacity.','source_and_proof_only':True,'scientific_execution_or_physical_acceptance':False,'RET_remains_paused':True,'successor_assigned':False,'terminal_completion_not_self_authenticated':True}
ref=m.save('HANDOFF.json',handoff)
if sorted(x.name for x in R.iterdir())!=handoff['namespace']:raise ValueError('final review namespace mismatch')
for row in payloads:m.verify(row['path'],row)
print(json.dumps({'status':'SEALED','handoff':ref,'namespace_count':len(handoff['namespace']),'payload_count':len(payloads),'fresh_source_identities':204},sort_keys=True))
