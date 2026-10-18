"""Independent metadata check of RI212; no proof arithmetic or subject execution."""
from pathlib import Path
import hashlib,importlib.util,re
B=Path('/Volumes/AI_DATA/development/det-review-evidence');D=B/'ri215-root-margin-review-a1inhpxr';Q=B/'ri212-native-individual-margins-u1l72g3n'
hp=B/'ri122-root-execution-review-6whn_vky/metadata.py';b=hp.read_bytes();assert len(b)==3144 and hashlib.sha256(b).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',hp);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=D
fresh={}
def check(r):
 assert set(r) in ({'path','bytes','sha256'},{'path','bytes','sha256','resolved_path','symlinks'})
 now=m.verify(r['path'],r);assert now['resolved_path']==r['path'] and now['symlink_chain']==[]
 if 'resolved_path' in r:assert r['resolved_path']==r['path'] and r['symlinks']==[]
 if r['path'] in fresh:assert fresh[r['path']]==now
 fresh[r['path']]=now
handoff=dict(path=str(Q/'HANDOFF.json'),bytes=8390,sha256='76b6e1d543d3ea39acedbb3561c102887c8879cf145a824bf54a8a419de4c71c');check(handoff);H=m.load(Q/'HANDOFF.json')
for r in H['payloads']:check(r)
assert sorted(p.name for p in Q.iterdir())==H['namespace']==sorted(['HANDOFF.json']+[Path(r['path']).name for r in H['payloads']])
S=m.load(Q/'SOURCE_REFERENCES.json');A=m.load(Q/'AUTHOR_VERIFICATION.json');by={x['identity']['path']:x['identity'] for x in S['direct_sources']}
assert len(by)==len(S['direct_sources'])==S['direct_scope']['files']==24 and list(by)==sorted(by)
assert sum(r['bytes'] for r in by.values())==S['direct_scope']['bytes']==693919
for row in S['direct_sources']:
 assert row['access'] in ('administrative-reference','accepted-analytic-text','opaque-historical-support');check(row['identity'])
refs=[S[k] for k in ('assignment','accepted_predecessor','predecessor_handoff','predecessor_references')]+[S['inherited_manifest_by_reference']['identity']]
for row in S['current_literal_reads']:assert row['receipt']['exit_code']==0;refs.extend(row['files'])
assignment=m.load(S['assignment']['path']);decision=m.load(S['accepted_predecessor']['path']);prior=m.load(S['predecessor_handoff']['path']);P=Path(S['predecessor_handoff']['path']).parent
assert assignment['reservation']==str(Q) and assignment['status']=='ASSIGNED_AFTER_RI210_INDEPENDENT_ADJUDICATION' and assignment['predecessor']==S['accepted_predecessor'] and assignment['new_scientific_execution_authority'] is False
assert decision['status']=='ACCEPT_COMPLETE_SIX_MAXIMA_GLOBAL_BOUND_AND_STRICT_WEIGHTED_W' and decision['actual_W_positive'] is True and decision['global_M6_bound_proved'] is True and decision['both_individual_margins_or_H30_decided'] is False
refs.extend(decision[k] for k in ('handoff','proof','global_proof','metadata','root_review','independent_review'));refs.extend(prior['payloads'])
assert decision['handoff']==S['predecessor_handoff']
assert sorted(p.name for p in P.iterdir())==S['predecessor_namespace']==prior['namespace']==sorted(['HANDOFF.json']+[Path(r['path']).name for r in prior['payloads']])
old=m.load(S['predecessor_references']['path']);inventory=m.load(S['inherited_manifest_by_reference']['identity']['path'])
bound={k:v for k,v in inventory.items() if k not in ('schema','status','protected_files','scope')}
assert len(bound)==15 and bound==S['inherited_manifest_by_reference']['boundary_objects'] and S['inherited_manifest_by_reference']==old['inherited_manifest_by_reference']
assert len(inventory['protected_files'])==S['inherited_manifest_by_reference']['selected_paths']==423
inv={r['identity']['path']:r for r in inventory['protected_files']}
def match(r):
 assert inv[r['path']]['identity']==r and inv[r['path']]['classification']=='analytic-source-text-or-review' and inv[r['path']]['access_policy']=='text-reading-and-opaque-identity-no-execution'
assert S['original_six_literal_admissions']==assignment['source_admission'] and len(assignment['source_admission'])==6
for r in assignment['source_admission']:
 refs.append(r['identity']);assert r['access']=='accepted-analytic-text' and r['typed_reference_expansion'] is False and r['inherited_matches']
 for i in r['inherited_matches']:match(i);assert m.pure(i)==m.pure(r['identity'])
for key,status in [('additional_seed_admission','ADMIT_ONE_EXISTING_ANALYTIC_TEXT_FOR_MANUAL_SEED_RELATION'),('additional_complement_admission','ADMIT_ONE_EXISTING_ANALYTIC_TEXT_FOR_SAME_LAW_SEED_SIGN')]:
 row=S[key];refs.extend([row['authority'],row['reference']]);ad=m.load(row['authority']['path'])
 assert row['typed_reference_expansion'] is False and ad['status']==status and ad['assignment']==S['assignment'] and ad['reference']==row['reference']
 assert all(ad[k] is False for k in ('new_execution_authority','typed_reference_expansion','automatic_proof_arithmetic'))
 if key=='additional_seed_admission':match(ad['inherited_row']['identity']);assert inv[ad['inherited_row']['identity']['path']]==ad['inherited_row']
 else:
  assert ad['previous_admission']==S['additional_seed_admission']['authority'] and len(ad['inherited_matches'])==1
  for prev in ad['inherited_matches']:match(prev['identity']);assert inv[prev['identity']['path']]==prev and m.pure(prev['identity'])==m.pure(ad['reference'])
  assert m.pure(ad['original'])==m.pure(ad['reference'])
refs.append(S['predecessor_author_support']['identity']);refs.extend([H['assignment'],H['accepted_predecessor']]);refs.extend(H['additional_literal_admissions'])
assert len(refs)==46
for r in refs:assert m.pure(r)==m.pure(by[r['path']]);check(r)
assert S['predecessor_author_support']['typed_reference_expansion'] is False
assert H['scope']==S['scope']==A['scope'] and H['executable_obligations']==S['executable_obligations']==A['executable_obligations']==old['executable_obligations']
assert H['executable_obligations']['new_credit']==0 and H['scope']['qualification_credit']==0
for k in ('individual_native_signs_decided','both_individual_margins_or_H30_decided','physical_correspondence_proved','scientific_body_vector_or_certificate_read','automated_proof_arithmetic_graph_LP_or_subject_execution','numerical_H_or_z_reconstruction','actual_M6_or_scales_evaluated','repository_or_Git_written','native_determinant_sign_decided','both_native_margin_signs_decided'):assert H['scope'][k] is False
assert A['status']=='AUTHOR_MANUAL_PROOF_NOT_INDEPENDENT_ACCEPTANCE' and A['final6_not_yet_run_at_author_creation'] is True
assert len(A['current_failed_commands_or_patches'])==1 and A['current_failed_commands_or_patches'][0]['status']=='rejected-before-write' and len(A['current_diagnostics'])==2
assert A['preseal']['receipt']==dict(chunk_id='6ceada',exit_code=0) and A['preseal']['actual_result']['current_namespace']==4
for r in A['preseal']['actual_result']['current_payloads']:check(r)
for name in ('INDIVIDUAL_MARGINS.md','SEED_COMPARISON.md','HANDOFF.md'):
 text=(Q/name).read_text();assert not re.search(r'[ \t]+$',text,re.M)
 for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):assert target in H['namespace'] and (Q/target).is_file()
assert len(fresh)==30
for r in fresh.values():assert m.identity(r['path'])==r
assert sorted(p.name for p in Q.iterdir())==H['namespace'] and sorted(p.name for p in P.iterdir())==prior['namespace']
with (D/'review_metadata.py').open('xb') as f:f.write(Path(__file__).read_bytes())
print(m.save('RI212_ROOT_METADATA_CHECK.json',dict(schema='ri215-independent-ri212-metadata-v1',status='PASS_METADATA_NOT_MATHEMATICAL_EXECUTION',handoff=handoff,direct_sources=24,direct_bytes=693919,selected_references=46,fresh_identities=list(fresh.values()),current_namespace=6,predecessor_namespace=6,inherited_boundary_objects=15,inherited423_by_reference=True,fresh_inherited_replay=False,original_analytic_matches=6,additional_analytic_matches=2,author_diagnostics_and_phases_retained=True,scientific_body_decoded=False,automatic_proof_arithmetic=False,subject_execution=False)))
