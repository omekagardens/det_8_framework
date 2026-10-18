"""Independent administrative review of RI201; no mathematical target execution."""
import hashlib,importlib.util,re
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri202-root-two-maxima-review-kw07pwnj';Q=B/'ri201-native-two-maxima-09928c97'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
fresh={}
def check(r):
 assert set(r) in ({'path','bytes','sha256'},{'path','bytes','sha256','resolved_path','symlinks'})
 now=m.verify(r['path'],r);assert now['resolved_path']==r['path'] and now['symlink_chain']==[]
 if 'resolved_path' in r:assert r['resolved_path']==now['resolved_path'] and r['symlinks']==[]
 if r['path'] in fresh:assert fresh[r['path']]==now
 fresh[r['path']]=now
 return now
h=dict(path=str(Q/'HANDOFF.json'),bytes=5866,sha256='b3c6de222485d29b14fd33984ffa23bc7be4479826ab6134e1882f3314d18ad7');check(h);H=m.load(h['path'])
for r in H['payloads']:check(r)
assert H['namespace']==sorted(p.name for p in Q.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in H['payloads']]) and len(H['namespace'])==5
S=m.load(Q/'SOURCE_REFERENCES.json');A=m.load(Q/'AUTHOR_VERIFICATION.json');by={r['identity']['path']:r['identity'] for r in S['direct_sources']}
assert len(by)==len(S['direct_sources'])==S['direct_scope']['files']==18 and sum(r['bytes'] for r in by.values())==S['direct_scope']['bytes']==617021
for r in S['direct_sources']:assert r['access'] in ('administrative-reference','accepted-analytic-text','opaque-historical-support');check(r['identity'])
refs=[S['assignment'],S['accepted_predecessor'],S['predecessor_handoff'],S['predecessor_references'],S['inherited_manifest_by_reference']['identity']]
for group in S['current_literal_source_reads']:refs.extend(group['files'])
assignment=m.load(S['assignment']['path']);decision=m.load(S['accepted_predecessor']['path']);prior=m.load(S['predecessor_handoff']['path']);P=Path(S['predecessor_handoff']['path']).parent
assert assignment['reservation']==str(Q) and assignment['status']=='ASSIGNED_AFTER_RI199_INDEPENDENT_ADJUDICATION' and assignment['predecessor']==S['accepted_predecessor']
refs.extend(decision[k] for k in ('handoff','proof','root_metadata','root_review'));refs.extend(prior['payloads']);refs.extend([H['assignment'],H['accepted_predecessor']]);assert len(refs)==23
for r in refs:assert m.pure(r)==m.pure(by[r['path']]);check(r)
assert sorted(p.name for p in P.iterdir())==prior['namespace']==S['predecessor_namespace'] and len(prior['namespace'])==5
assert sorted([Path(r['path']).name for r in prior['payloads']]+['HANDOFF.json'])==prior['namespace']
previous=m.load(S['predecessor_references']['path']);inherited=m.load(S['inherited_manifest_by_reference']['identity']['path'])
bound={k:v for k,v in inherited.items() if k not in ('schema','status','protected_files','scope')};assert len(bound)==15 and bound==S['inherited_manifest_by_reference']['boundary_objects']==previous['inherited_manifest_by_reference']['boundary_objects']
assert len(inherited['protected_files'])==423 and S['inherited_manifest_by_reference']['fresh423_file_or_transitive_reference_replay'] is False and S['inherited_manifest_by_reference']['predecessor26_direct_manifest_replayed_in_full'] is False
assert H['executable_obligations']==S['executable_obligations']==A['executable_obligations']==previous['executable_obligations']
assert H['complete_two_maxima_bound_proved'] is True and H['manual_analysis_only'] is True
for k in ('global_M6_bound_proved','concrete_violating_parent_proved','actual_W_decided','both_individual_margins_or_H30_proved','printed_numerical_M5_used','new_scientific_body_or_vector_read','automated_proof_arithmetic_or_subject_execution','qualification_credit','repository_or_Git_written'):assert H[k] is False
assert H['ret_paused'] is True and A['status']=='AUTHOR_MANUAL_PROOF_NOT_INDEPENDENT_ACCEPTANCE' and A['final5_not_yet_run_at_author_creation'] is True
for r in A['preseal']['actual_result']['current_payloads']:check(r)
assert len(A['checker_revisions'])==3 and [r['exit_code'] for r in A['checker_revisions']]==[1,1,0]
# Retain diagnostics rather than mistaking failed administrative attempts for proof failures.
assert len(A['diagnostics'])==6
for name in ('TWO_MAXIMA.md','HANDOFF.md'):
 text=(Q/name).read_text();assert not re.search(r'[ \t]+$',text,re.M)
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):assert target in H['namespace']
assert len(fresh)==23
for r in fresh.values():assert m.identity(r['path'])==r
print(m.save('RI201_ROOT_METADATA_CHECK.json',dict(schema='ri202-independent-ri201-check-v1',status='PASS_METADATA_NOT_MATHEMATICAL_EXECUTION',handoff=h,direct_sources=18,direct_bytes=617021,current_payloads=5,selected_references=23,fresh_identities=list(fresh.values()),current_and_previous_namespaces=5,inherited_boundary_objects=15,inherited423_and_previous26_by_reference=True,fresh_inherited_replay=False,all_six_author_diagnostics_retained=True,scientific_body_decoded=False,automatic_proof_arithmetic=False,subject_execution=False)))
