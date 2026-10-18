"""Seal finite administrative preflight; no proposed invocation is executed."""
from pathlib import Path
import hashlib,json,shlex,os
D=Path(__file__).resolve().parent;B=D.parent
R=B/'ri160-root-fixture-adjudication-0rmgmo7y';S=B/'ri160-white-fixture-custody-repair-ufok1zpo'
def pin(p):
 assert p.is_file() and not p.is_symlink() and p.resolve()==p
 s=p.stat();b=p.read_bytes();t=p.stat();fields=lambda x:(x.st_dev,x.st_ino,x.st_mode,x.st_nlink,x.st_size,x.st_mtime_ns,x.st_ctime_ns)
 assert fields(s)==fields(t) and len(b)==s.st_size
 return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(p):return json.loads(p.read_bytes())
def write(name,x):
 with (D/name).open('x') as f:json.dump(x,f,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False);f.write('\n')
auth=read(D/'SOURCE_AND_MONITOR_AUTHENTICATION.json');proposal=read(D/'QUALIFICATION_PROPOSAL.json');facts=read(D/'FIXED_CURRENT_FACTS.json')
for row in auth['all_verified_source_evidence_identities']:assert pin(Path(row['path']))==row,row['path']
for item in auth['complete_packet_checks']:
 assert sorted(p.name for p in Path(item['root']).iterdir())==sorted(item['namespace'])
assert shlex.split(proposal['exec_command_arguments_proposal']['cmd'])==proposal['outer_argv_proposal']
assert proposal['outer_argv_proposal'][-1]==(D/'MONITOR_INVOCATION.proposal.txt').read_text()
assert len(proposal['adapter_admission_field_proposal'])==12
assert proposal['adapter_admission_field_proposal']['qualification'] is None
assert proposal['request_fields']=={'phase':'INERT_METADATA_ONLY'}
assert proposal['monitor_call']['seconds']==180 and proposal['monitor_call']['label']=='CONTROLS'
assert proposal['adapter_admission_field_proposal']['source_manifest']==pin(S/'SOURCE_SET.json')
assert proposal['adapter_admission_field_proposal']['source_review']==pin(R/'RI160_ROOT_ADJUDICATION.json')
assert all(not os.path.lexists(p) for p in proposal['operation_paths_not_created'].values())
write('FINAL_PREPARATION_CHECK.json',{'schema':'ri162-final-preparation-check-v1','source_evidence_identities_still_exact':len(auth['all_verified_source_evidence_identities']),'source_review_monitor_namespaces_unchanged':True,'exact_shell_quote_round_trip':True,'whole_literal_invocation_binding':True,'twelve_card_fields_non_authorizing_envelope':True,'all_prospective_paths_still_absent':True,'fresh_fixed_vendor_binding_exact_to_accepted':facts['current_binding_equals_immutable_expected_binding'],'controls_executed':0,'operationally_ready':False,'missing':'Root concrete inspection and fresh supplier/host bracket, exclusive setup, genuine admission/dispatch and later complete outcomes review.'})
base=sorted(p.name for p in D.iterdir());namespace=sorted(base+['PUBLICATION_SUBSET.json','HANDOFF.json'])
write('PUBLICATION_SUBSET.json',{'schema':'ri162-publication-subset-v1','include_names':namespace,'external_only_preserved':[],'historical_source_operands':'623 exact whole source/review identities remain at their original paths; no repeated scientific payload archive or fixture tree exists here.'})
payloads=[pin(p) for p in sorted(D.iterdir())]
write('HANDOFF.json',{'schema':'ri162-inert106-preflight-handoff-v1','status':'PREPARATION_SEALED_FOR_ROOT_INSPECTION_NOT_ADMISSION','reservation':str(D),'author':'/root/ri116_complete_caller_review','prior_authorship':'RI156/158/160 adapter, RI125 primary/qualifier and RI131; prior RI141 independent source review reused as historical acceptance, not new self-review.','assignment':pin(R/'MEASUREMENT_SUCCESSOR_ASSIGNMENT.json'),'root_accepted_source':pin(R/'RI160_ROOT_ADJUDICATION.json'),'source':pin(S/'HANDOFF.json'),'source_manifest':pin(S/'SOURCE_SET.json'),'proposal':pin(D/'QUALIFICATION_PROPOSAL.json'),'literal_monitor_invocation':pin(D/'MONITOR_INVOCATION.proposal.txt'),'preflight_and_command_contract':pin(D/'PREFLIGHT_AND_COMMAND.md'),'current_fixed_facts':pin(D/'FIXED_CURRENT_FACTS.json'),'source_monitor_authentication':pin(D/'SOURCE_AND_MONITOR_AUTHENTICATION.json'),'diagnostics':pin(D/'ACTUAL_READ_ONLY_DIAGNOSTICS.json'),'final_check':pin(D/'FINAL_PREPARATION_CHECK.json'),'actual_checks':[{'chunk_id':'78f5ea','exit_code':0,'meaning':'Authorized six fixed-file bytes/resolution/states and read-only host OS facts; direct vendor not executed.'},{'chunk_id':'546634','exit_code':0,'meaning':'567 source dependencies,623 distinct source/review identities, eight unchanged monitor/helper spans and exact non-authorizing proposals.'}],'control_counts':{'defined':106,'executed':0},'actual_binding_drift':False,'missing_immediate_prerequisites':['Root inspect/adopt exact finite command, current source and same unchanged monitor selection','Fresh genuine complete vendor supplier/framework/host and source/card preflight with stable host/cache/loader premises; current finite facts are not full supplier qualification','Root exclusively creates declared records/environment/empty monitor directory, canonical request and separate12-field adapter admission; adapter output stays absent until authenticated child ownership','Root records actual dispatch then invokes once, retains exact initial/pending/terminal tool evidence and whole raw monitoring/streams/partials','Root independent post source/card/supplier/environment/namespace checks even after failure, then complete actual106 evidence review'],'not_immediate_blockers':['R01 path transfer','current-E capture/profiles','scientific WHITE mode admission and saved arithmetic','RI131/full32/periodic/mean/join/public-data/calibration'],'thresholds_unchanged':True,'new_launcher_framework':False,'source_or_control_import_compile_AST_probe_execute':False,'active_card_freeze_admission_E_fixture_created':False,'new_agents':0,'repository_or_Git_operation':False,'RET':'paused','sealed_immutable':True,'namespace':namespace,'payload_count':len(payloads),'payloads':payloads,'genuine_seal_tool_result':'Delivered separately; this handoff does not self-authenticate tool origin.'})
assert sorted(p.name for p in D.iterdir())==namespace
for row in payloads:assert pin(Path(row['path']))==row
print(json.dumps({'status':'SEALED_PREPARATION_ONLY','namespace':len(namespace),'payloads':len(payloads),'handoff':pin(D/'HANDOFF.json'),'proposal':pin(D/'QUALIFICATION_PROPOSAL.json'),'fixed_facts':pin(D/'FIXED_CURRENT_FACTS.json'),'controls_executed':0},sort_keys=True))
