"""Root adjudication of a reviewed actual preparation; no operational authority."""
from pathlib import Path
import importlib.util,hashlib,json,os
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri230-root-lower-combinations-review-v9mxbmtc';I=B/'ri230-independent-concrete-preparation-yehbzc6e';D=B/'ri226-directory-custody-recovery-yvfg_p1b'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
m.verify(I/'HANDOFF.json',dict(bytes=6311,sha256='86961c641d1e1f501e5f196fe0d3b36c886cb6ab516281ff6c3ce51c2aab4013'))
seal=m.load(I/'HANDOFF.json');assert sorted(x.name for x in I.iterdir())==seal['namespace']
for row in seal['files']+seal['root_receipts']:m.verify(row['path'],row)
v=m.load(I/'VERDICT.json');assert v['blocking_findings']==[] and v['recommendation']=='ACCEPT_ACTUAL_ADMINISTRATIVE_PREPARATION_ONLY' and v['predicate_count']==7563
check=m.load(R/'ROOT_CONCRETE_PREPARATION_CHECK.json');assert check['canonical_comparisons']==6492 and check['status']=='PASS_ACTUAL_NINE_OUTPUT_PREPARATION_PENDING_INDEPENDENT_REVIEW'
assert len(check['outputs'])==9
for row in check['outputs']:assert m.identity(row['path'])==row
g=m.load(R/'GENUINE_PREPARATION_TOOL.json');a=m.load(R/'GENUINE_PREPARATION_SESSION_LINKAGE.json')
assert g['initial']['result']['session_id']==a['initial_session']==16198
assert a['intermediate_write_stdin_calls']==[] and m.canonical(a['terminal_call']['result'])==m.canonical(g['terminal'])
assert a['terminal_call']['arguments']==dict(session_id=16198,chars='',yield_time_ms=1000,max_output_tokens=4000)
assert g['terminal']['exit_code']==0 and g['terminal']['chunk_id']=='1db8d4'
for name in ['ADMIT_RECONCILE.json','DISPATCH.json']:assert not os.path.lexists(D/name)
assert not os.path.lexists(B/'ri226-freeze-reconciliation-operation-yvfg_p1b')
for name in ['tmp','monitor']:assert list((D/name).iterdir())==[]
post=m.load(B/'ri224-root-cwd-review-nyvru347/POST_FAILURE_CUSTODY.json');assert m.identity(post['installed_partial']['path'])==post['installed_partial']
for row in post['operation_files']+post['monitor_files']:m.verify(row['path'],row)
assert m.snapshot()==m.load(R/'REPO_ENTRY.json')
record=dict(schema='ri230-root-actual-preparation-acceptance-v1',status='ACCEPT_ACTUAL_ADMINISTRATIVE_PREPARATION_ONLY',source_acceptance=m.ref(R/'RI229_PREPARATION_SOURCE_ACCEPTANCE.json'),one_preparation_decision=m.ref(R/'ROOT_ONE_PREPARATION_DECISION.json'),genuine_initial_and_terminal=m.ref(R/'GENUINE_PREPARATION_TOOL.json'),genuine_session_linkage=m.ref(R/'GENUINE_PREPARATION_SESSION_LINKAGE.json'),root_concrete_check=m.ref(R/'ROOT_CONCRETE_PREPARATION_CHECK.json'),independent_review=m.ref(I/'HANDOFF.json'),independent_verdict=m.ref(I/'VERDICT.json'),full_root_review_reads=['2be679 exit0','5fb09b exit0'],actual_preparation='0f12a4/session16198 ->1db8d4 exit0',root_custody_check='6006e5/session62605 ->4ff069 exit0;6492 canonical comparisons',independent_checks=['d93b90 exit0;7544 predicates/2842 whole-file identities','dbf108 exit0;19 session-linkage predicates'],outputs=check['outputs'],scope='Nine actual administrative records and empty controls only. Retained installation remains an unaccepted partial; original failure is not superseded as a success.',retained_failure_unchanged=True,retained_partial_unchanged=True,reconciliation_admitted=False,reconciliation_executed=False,frozen_custody_accepted=False,mode_admission=False,scientific_execution=False,qualification_credit=0,RET_paused=True,next_root_action='Fresh predispatch custody and separate one-attempt read-only reconciliation admission/dispatch under unchanged limits, then genuine monitored outcome and independent adjudication.',remaining_premises=v['remaining_premises'][1:])
with (R/'accept_actual_preparation.py').open('xb') as out:out.write(Path(__file__).read_bytes())
print(json.dumps(m.save('ACTUAL_PREPARATION_ACCEPTANCE.json',record)))
