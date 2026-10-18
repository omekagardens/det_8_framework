"""Root administrative checks, separate from the manual mathematical review."""
import hashlib, importlib.util, re
from pathlib import Path
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri204-root-adapters-f04k2tg9';Q=B/'ri203-native-three-maxima-p1oxdw_6'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=hp.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
fresh={}
def check(r):
    assert set(r) in ({'path','bytes','sha256'},{'path','bytes','sha256','resolved_path','symlinks'})
    now=m.verify(r['path'],r);assert now['resolved_path']==r['path'] and now['symlink_chain']==[]
    if 'resolved_path' in r: assert r['resolved_path']==now['resolved_path'] and r['symlinks']==[]
    if r['path'] in fresh: assert fresh[r['path']]==now
    fresh[r['path']]=now
handoff=dict(path=str(Q/'HANDOFF.json'),bytes=6708,sha256='bba9a2e36c9bfff8b456c8d1f4d0fac5b189ba6008a173251f891cea608cda9c')
check(handoff);H=m.load(handoff['path'])
for r in H['payloads']:check(r)
assert H['namespace']==sorted(p.name for p in Q.iterdir())==sorted(['HANDOFF.json']+[Path(r['path']).name for r in H['payloads']]) and len(H['namespace'])==6
S=m.load(Q/'SOURCE_REFERENCES.json');A=m.load(Q/'AUTHOR_VERIFICATION.json')
by={r['identity']['path']:r['identity'] for r in S['direct_sources']}
assert len(by)==len(S['direct_sources'])==S['direct_scope']['files']==13
assert sum(r['bytes'] for r in by.values())==S['direct_scope']['bytes']==545142
assert list(by)==sorted(by)
for r in S['direct_sources']:
    assert r['access'] in ('administrative-reference','accepted-analytic-text','opaque-historical-support');check(r['identity'])
refs=[S[k] for k in ('assignment','accepted_predecessor','scalar_clarification','predecessor_handoff','predecessor_references')]+[S['inherited_manifest_by_reference']['identity']]
for group in S['current_literal_reads']:refs.extend(group['files'])
assignment=m.load(S['assignment']['path']);decision=m.load(S['accepted_predecessor']['path']);clarification=m.load(S['scalar_clarification']['path']);prior=m.load(S['predecessor_handoff']['path']);P=Path(S['predecessor_handoff']['path']).parent
assert assignment['reservation']==str(Q) and assignment['status']=='ASSIGNED_AFTER_RI201_INDEPENDENT_ADJUDICATION' and assignment['predecessor']==S['accepted_predecessor']
assert decision['status']=='ACCEPT_COMPLETE_TWO_MAXIMA_CLASS_CONDITIONAL_THEOREM' and decision['actual_W_decided'] is False
refs.extend(decision[k] for k in ('handoff','proof','metadata','root_review'));refs.append(clarification['source']);refs.extend(prior['payloads']);refs.append(S['predecessor_author_support']['identity']);refs.extend(H[k] for k in ('assignment','accepted_predecessor','scalar_clarification'))
assert len(refs)==26
for r in refs:assert m.pure(r)==m.pure(by[r['path']]);check(r)
assert clarification['status']=='NAMED_ACCEPTED_FINITE_SCALAR_ALLOWED_AS_INHERITED_PREMISE'
assert all(clarification[k] is False for k in ('new_vector_or_certificate_read','automatic_scientific_arithmetic','new_execution_authority','RI203_candidate_accepted'))
assert S['predecessor_author_support']['typed_reference_expansion'] is False
assert sorted(p.name for p in P.iterdir())==prior['namespace']==S['predecessor_namespace'] and len(prior['namespace'])==5
assert sorted([Path(r['path']).name for r in prior['payloads']]+['HANDOFF.json'])==prior['namespace']
previous=m.load(S['predecessor_references']['path']);inherited=m.load(S['inherited_manifest_by_reference']['identity']['path'])
bound={k:v for k,v in inherited.items() if k not in ('schema','status','protected_files','scope')}
assert len(bound)==15 and bound==S['inherited_manifest_by_reference']['boundary_objects']==previous['inherited_manifest_by_reference']['boundary_objects']
history=S['inherited_manifest_by_reference'];assert len(inherited['protected_files'])==history['selected_paths']==423
assert history['fresh423_or_previous26_or_previous18_replay'] is False and history['inherited_boundaries_not_new_read_authority'] is True
assert history['RI197_literal_certificate_exception_used_for_new_read'] is False and history['RI164_operational_boundary_remains_unexpanded'] is True
assert H['executable_obligations']==S['executable_obligations']==A['executable_obligations']==previous['executable_obligations'] and H['executable_obligations']['new_credit']==0
assert H['complete_three_maxima_class_bound_proved'] is True and H['manual_analysis_only'] is True and H['ret_paused'] is True
for k in ('global_M6_bound_proved','concrete_violating_parent_proved','actual_W_decided','both_individual_margins_or_H30_proved','four_through_six_maxima_settled','printed_numerical_M5_used','new_scientific_body_or_vector_read','automated_proof_arithmetic_or_subject_execution','qualification_credit','repository_or_Git_written'): assert H[k] is False
assert A['status']=='AUTHOR_MANUAL_PROOF_NOT_INDEPENDENT_ACCEPTANCE' and A['final6_not_yet_run_at_author_creation'] is True
assert A['current_failed_commands_or_patches']==[] and len(A['current_diagnostics'])==1 and len(A['manuscript_phases'])==2
assert A['preseal']['actual_receipt']['exit_code']==0 and A['preseal']['actual_result']['current_namespace']==4
for r in A['preseal']['actual_result']['current_payloads']:check(r)
for name in ('THREE_MAXIMA.md','DENOMINATOR_LEMMA.md','HANDOFF.md'):
    text=(Q/name).read_text();assert not re.search(r'[ \t]+$',text,re.M)
    for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):assert target in H['namespace']
assert len(fresh)==19
for r in fresh.values():assert m.identity(r['path'])==r
assert sorted(p.name for p in Q.iterdir())==H['namespace'] and sorted(p.name for p in P.iterdir())==prior['namespace']
print(m.save('RI203_ROOT_METADATA_CHECK.json',dict(schema='ri204-independent-ri203-metadata-v1',status='PASS_METADATA_NOT_MATHEMATICAL_EXECUTION',handoff=handoff,direct_sources=13,direct_bytes=545142,current_payloads=6,selected_references=26,fresh_identities=list(fresh.values()),current_namespace=6,predecessor_namespace=5,inherited_boundary_objects=15,inherited423_previous26_previous18_by_reference=True,fresh_inherited_replay=False,author_diagnostic_and_phases_retained=True,scientific_body_decoded=False,automatic_proof_arithmetic=False,subject_execution=False)))
