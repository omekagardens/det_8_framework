from pathlib import Path
import importlib.util,hashlib,json,os,time
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=B/'ri234-root-reconciliation-tzop5ais';D=B/'ri226-directory-custody-recovery-yvfg_p1b';P=B/'ri230-root-lower-combinations-review-v9mxbmtc'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
host=m.load('/private/tmp/ri234_host_record.json');assert host['result']['chunk_id']=='c804b9' and host['result']['exit_code']==0
obs=json.loads(host['result']['output']);oldhost=m.load(D/'HOST_BEFORE.json');assert m.canonical(obs)==m.canonical({k:v for k,v in oldhost.items() if k not in ('schema','genuine_tool')})
host['observation']=obs;hostref=m.save('GENUINE_PREDISPATCH_HOST.json',host)
check=m.verify(R/'FRESH_PREDISPATCH_CHECK.json',dict(bytes=6610,sha256='8b87fe6e1df34404a5cb138c106fed7d2e7b87c59132c49a17e432c2a125cbb7'));cv=m.load(check['path']);assert cv['status']=='PASS_FRESH_RECONCILIATION_PREDISPATCH_CUSTODY'
for row in cv['outputs']:assert m.canonical(m.identity(row['path']))==m.canonical(row)
proposal=m.load(D/'RECONCILIATION_PROPOSAL.json');card=proposal['proposed_admission_fields'];dispatch=proposal['dispatch_fields_without_admission']
for p in [D/'ADMIT_RECONCILE.json',D/'DISPATCH.json',Path(card['output'])]:assert not os.path.lexists(p)
for p in [D/'tmp',D/'monitor']:assert list(p.iterdir())==[]
assert m.canonical(m.snapshot())==m.canonical(m.load(R/'REPO_ENTRY.json'))
review=m.load(R/'PREDISPATCH_PEER_CLEARANCE.json');assert review['disposition']=='NO_BLOCKER_TO_ONE_READ_ONLY_OPERATION'
decision=dict(schema='ri234-root-one-read-only-operation-decision-v1',status='AUTHORIZE_ONE_RI226_READ_ONLY_RECONCILIATION',accepted_preparation=m.ref(P/'ACTUAL_PREPARATION_ACCEPTANCE.json'),source_review=m.ref(D/'ROOT_SOURCE_REVIEW.json'),fresh_current_custody=m.ref(R/'FRESH_PREDISPATCH_CHECK.json'),genuine_current_host=hostref,independent_predispatch_review=m.ref(R/'PREDISPATCH_PEER_CLEARANCE.json'),proposal=m.ref(D/'RECONCILIATION_PROPOSAL.json'),admission_fields=card,dispatch_fields_without_admission=dispatch,administrative_interpreter=m.identity('/opt/homebrew/bin/python3'),issuer=m.ref(Path(__file__).resolve()),original_failure_remains_refused=True,E_read_only=True,one_attempt_no_retry=True,original_limits_unchanged=True,scientific_execution=False,mode_admission=False,independent_postreview_required=True,RET_paused=True,premises=['Stable host and declared supplier selections during observed intervals','Apple loader/cache/kernel and prior runtime applicability remain explicit conditional premises','No descendants; sampled sole-child RSS is not continuous whole-process-group accounting','Historical preparation records are immutable; this decision uses fresh current identity and genuine host rechecks'])
dec=m.save('ROOT_ONE_RECONCILIATION_DECISION.json',decision)
m.D=D;admit=m.save('ADMIT_RECONCILE.json',card);dispatch=dict(dispatch,admission=admit);dp=m.save('DISPATCH.json',dispatch);m.D=R
record=m.save('ISSUED_CONTROLS.json',dict(decision=dec,admission=m.identity(admit['path']),dispatch=m.identity(dp['path']),observed_at_unix_ns=time.time_ns(),genuine_predispatch_check=dict(initial_chunk='480a86',session_id=74231,terminal_chunk='c6a559',exit_code=0),operation_not_started=True))
print(json.dumps(dict(issued=record,exact_tool_arguments=dict(cmd=dispatch['shell_command'],workdir=dispatch['cwd'],login=False,yield_time_ms=1000,max_output_tokens=4000))))
