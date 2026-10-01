"""Root actual optimized/both-mode acceptance after independent review and fresh custody."""
from pathlib import Path
import hashlib,importlib.util
D=Path(__file__).parent;hp=D/'publication_helpers.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277'
s=importlib.util.spec_from_file_location('p',hp);p=importlib.util.module_from_spec(s);s.loader.exec_module(p);m=p.m
R=m.B/'ri193-current-e-optimized-review-p2ylnt9f'
m.verify(R/'HANDOFF.json',dict(bytes=5225,sha256='2b638d8290e573324084f751edbc16166cf41db36aed128396bbd08740640505'))
h=m.load(R/'HANDOFF.json');assert sorted(x.name for x in R.iterdir())==h['exclusive_namespace']
for row in h['files']:m.verify(row['path'],row)
for row in m.load(D/'RI193_ROOT_MANUAL_REVIEW.json')['refs'].values():m.verify(row['path'],row)
assert (R/'normal_relation_fragment.txt').read_text() in (R/'check_optimized_saved.py').read_text()
v=m.load(R/'VERDICT.json');a=m.load(R/'ADMIN_CHECK.json');final=m.load(R/'FINAL_CHECK.json')
assert v['status']=='ACCEPT_CURRENT_E_OPTIMIZED_AND_BOTH_MODE_PROFILE_EVIDENCE' and not v['blocking_findings']
assert a['predicates']==697704 and a['opaque_unique_identities']==12478
assert final['status']=='PASS' and final['identities_rehashed']==12478
rows=m.load(R/'IDENTITIES.json')['identities'];assert len(rows)==12478
for row in rows:assert m.identity(row['path'])==row
print(m.save('RI193_ROOT_FRESH_CHECK.json',dict(schema='ri193-root-fresh-both-profile-review-check-v1',status='PASS',review=m.ref(R/'HANDOFF.json'),identities=m.ref(R/'IDENTITIES.json'),whole_identities_rehashed=12478,whole_state_and_links_equal=True,complete_manual_review=m.ref(D/'RI193_ROOT_MANUAL_REVIEW.json'),complete_checker_reads=['767696','470379','ad12c6'],complete_review_read='3484e8',seal_and_handoff_read='18a7a7',subject_execution=False)))
decision=dict(schema='ri193-root-current-e-optimized-profile-adjudication-v1',status='ACCEPT_CURRENT_E_OPTIMIZED_AND_BOTH_PROFILES',review=m.ref(R/'INDEPENDENT_REVIEW.md'),verdict=m.ref(R/'VERDICT.json'),relation=m.ref(R/'BOTH_MODE_RELATION.json'),fresh_root_check=m.ref(D/'RI193_ROOT_FRESH_CHECK.json'),root_saved_check=m.ref(D/'ROOT_PROFILE_OPTIMIZED_CHECK.json'),actual_terminal='e3f394 exit0',review_actual_checks=['5098a1 exit0','dfee32 exit0','cab6c5 exit0'],scope='One actual optimized nonscientific profile and complete relation to accepted normal outcome. Each full213-descriptor object and all228 saved monitor samples independently reconstructed. Two flags and30 cache paths exhaust full raw-report differences. Earlier source semantics remain independently accepted inherited premises, with reviewer source authorship disclosed.',retained_premises=v['retained_premises']+['Trusted Apple kernel/loader/shared-cache and selected suppliers; finite read-window stability and no descendants remain explicit.','Two optimized absent cache alternatives are preserved; no cache-body equivalence or import instruction trace is inferred.'],scientific_credit=False,guard_execution=False,ret_paused=True,next='Separate nonauthor R01 path-sensitive applicability review and explicit eight-premise current-runtime decision before acceptance adapters or any science admission. No blanket65 rerun; only a justified smallest additional control under separate admission.')
print(m.save('RI193_ROOT_ADJUDICATION.json',decision))
RR=m.B/'ri170-current-e-root-records-proposed-gikj2giy';ad=m.load(RR/'ADMIT_PROFILE_OPTIMIZED.json');O=Path(ad['output']);c=m.load(O/'COMPLETE.json');outer=m.load(D/'GENUINE_OUTER.json');normal=m.load(RR/'NORMAL_ACCEPTANCE.json')
m.verify(RR/'NORMAL_ACCEPTANCE.json',dict(bytes=1680,sha256='5470ddd468cba8a5168042ceb73d1ce5204971233f3b26ecbbe657d617da95d2'))
assert c['sources']==ad['sources']==normal['sources'] and c['first_error'] is None and not c['independent_tail_errors']
assert outer['completion']==m.ref(O/'COMPLETE.json') and outer['command']==c['command'] and outer['environment']==c['environment'] and outer['exit_code']==0
card=dict(schema='ri133-root-preparation-stage-review-v1',status='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage='profiles',sources=ad['sources'],packet=ad['packet'],environment_root=ad['environment_root'],completions=dict(profile_normal=normal['completions']['profile_normal'],profile_optimized=m.ref(O/'COMPLETE.json')),genuine_outer=dict(profile_normal=normal['genuine_outer']['profile_normal'],profile_optimized=m.ref(D/'GENUINE_OUTER.json')),independent_review=m.ref(R/'INDEPENDENT_REVIEW.md'),scientific_execution=False)
assert len(card)==10 and list(card['completions'])==list(card['genuine_outer'])==['profile_normal','profile_optimized']
print(m.save(str(RR/'PROFILES_ACCEPTANCE.json'),card))
print(m.save('PROFILES_CARD_CHECK.json',dict(status='PASS_CLOSED_TEN_FIELD_BOTH_PROFILE_CARD',card=m.ref(RR/'PROFILES_ACCEPTANCE.json'),decision=m.ref(D/'RI193_ROOT_ADJUDICATION.json'),current_e=ad['environment_root'],normal_card_unchanged=True,guard_or_scientific_admission=False,subject_execution=False)))
