"""Root actual normal-profile adjudication, whole fresh custody and stage card."""
from pathlib import Path
import hashlib,importlib.util
D=Path(__file__).parent;hp=D/'publication_helpers.py';assert hashlib.sha256(hp.read_bytes()).hexdigest()=='8b04758d4e19988f67d0d96e86c93a8eb5405704f5b2a3e3d0b401f33afa4277'
s=importlib.util.spec_from_file_location('p',hp);p=importlib.util.module_from_spec(s);s.loader.exec_module(p);m=p.m
R=m.B/'ri190-current-e-normal-profile-review-zzmi16rs'
m.verify(R/'HANDOFF.json',dict(bytes=4717,sha256='477cf88201847d2e357cf4fde1d510d50edd5bd60e56ec1775c60e41d9d1e115'))
h=m.load(R/'HANDOFF.json');assert sorted(x.name for x in R.iterdir())==h['exclusive_namespace']
for row in h['files']:m.verify(row['path'],row)
m.verify(R/'check_normal_saved.py',dict(bytes=37343,sha256='d275f5e629fab94a2f4689b9840701f8f63b7fc75a127057654ed56bfbeb6d64'))
assert (R/'profile_checks_fragment.txt').read_text() in (R/'check_normal_saved.py').read_text()
v=m.load(R/'VERDICT.json');a=m.load(R/'ADMIN_CHECK.json');final=m.load(R/'FINAL_CHECK.json')
assert v['status']=='ACCEPT_CURRENT_E_NORMAL_PROFILE_EVIDENCE' and not v['blocking_findings']
assert a['predicates']==689436 and a['opaque_unique_identities']==12453
assert final['status']=='PASS' and final['identities_rehashed']==12453
rows=m.load(R/'IDENTITIES.json')['identities'];assert len(rows)==12453
for row in rows:assert m.identity(row['path'])==row
print(m.save('RI190_ROOT_FRESH_CHECK.json',dict(schema='ri190-root-fresh-normal-profile-review-check-v1',status='PASS',review=m.ref(R/'HANDOFF.json'),identities=m.ref(R/'IDENTITIES.json'),whole_identities_rehashed=12453,complete_seven_field_state_and_links_equal=True,full_checker_read_receipts=['1009fc','2feafc'],checker_pin_read='6a2710',complete_review_and_verdict_read='e720de',builder_and_seal_read='1faafc',fragment_equals_already_read_checker_subset=True,subject_execution=False)))
decision=dict(schema='ri190-root-current-e-normal-profile-adjudication-v1',status='ACCEPT_EXACT_CURRENT_E_NORMAL_PROFILE',review=m.ref(R/'INDEPENDENT_REVIEW.md'),verdict=m.ref(R/'VERDICT.json'),fresh_root_check=m.ref(D/'RI190_ROOT_FRESH_CHECK.json'),prior_root_check=m.ref(D/'ROOT_PROFILE_NORMAL_CHECK.json'),actual_terminal='9aba56 exit0',review_actual_check='d3bdb9 exit0; final677c80 and sealverificationf89a84 exit0',scope='One actual nonscientific normal candidate-interpreter profile, original RI130 observer under exact current-E custody and independently accepted baseline. Complete closed evidence and all116 samples independently reconstructed. Source semantics inherit earlier independent acceptance; reviewer source authorship disclosed. Root reconciled the entire reviewer source/interpretation with its separate whole-output arithmetic and metadata checks.',retained_premises=['Genuine external root/tool receipt origin and accepted driver semantics.','Trusted host/kernel/loader/shared-cache/supplier and inspection infrastructure; complete saved module descriptors are not a dynamic instruction trace.','Saved pid_owner is parent PID, not authenticated child identity; sampled child RSS/no-descendants is not hard group quota.','Finite read-window and opaque source/pyc stability do not prove continuous freeze or source/bytecode semantic equivalence.','RI170 R01 nonauthor path-sensitive applicability review decides the smallest genuinely needed extra control; no blanket65 rerun.'],normal_profile_only=True,scientific_credit=False,optimized_or_guard_executed=False,ret_paused=True,next='Fresh preflight and separately admitted optimized profile, independent actual outcome review, then both-mode reconciliation. WHITE/GWOSC/calibration/protected-validation/native-forward-map stages remain separate.')
print(m.save('RI190_ROOT_ADJUDICATION.json',decision))
RR=m.B/'ri170-current-e-root-records-proposed-gikj2giy';ad=m.load(RR/'ADMIT_PROFILE_NORMAL.json');O=Path(ad['output']);c=m.load(O/'COMPLETE.json');outer=m.load(D/'GENUINE_OUTER.json')
assert c['sources']==ad['sources'] and c['first_error'] is None and not c['independent_tail_errors']
assert outer['completion']==m.ref(O/'COMPLETE.json') and outer['command']==c['command'] and outer['environment']==c['environment'] and outer['exit_code']==0
card=dict(schema='ri133-root-preparation-stage-review-v1',status='ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE',stage='normal',sources=ad['sources'],packet=ad['packet'],environment_root=ad['environment_root'],completions=dict(profile_normal=m.ref(O/'COMPLETE.json')),genuine_outer=dict(profile_normal=m.ref(D/'GENUINE_OUTER.json')),independent_review=m.ref(R/'INDEPENDENT_REVIEW.md'),scientific_execution=False)
assert len(card)==10 and list(card['completions'])==list(card['genuine_outer'])==['profile_normal']
print(m.save(str(RR/'NORMAL_ACCEPTANCE.json'),card))
print(m.save('NORMAL_CARD_CHECK.json',dict(status='PASS_CLOSED_TEN_FIELD_NORMAL_CARD',card=m.ref(RR/'NORMAL_ACCEPTANCE.json'),decision=m.ref(D/'RI190_ROOT_ADJUDICATION.json'),current_e=ad['environment_root'],next_profile_admitted=False,subject_execution=False)))
