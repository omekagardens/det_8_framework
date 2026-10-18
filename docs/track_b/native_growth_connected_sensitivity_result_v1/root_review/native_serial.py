from check_native_metadata import *
import sys,shlex
N=B/'ri122-native-caller-source-jgehvvxx';C=N/'closure';T=C/'native_growth_connected_sensitivity_v1'
def full(path):
 z=identity(path);return dict(path=z['path'],resolved_path=z['resolved_path'],symlinks=z['symlink_chain'],bytes=z['bytes'],sha256=z['sha256'])
def write(path,value):
 with path.open('xb') as f:f.write(canonical(value));f.flush();os.fsync(f.fileno())
 return full(path)
def accept(mode,peerpath):
 p=mode.upper();peer=load(peerpath);root=load(N/(p+'_ROOT_COMPLETE_REVIEW.json'))
 assert peer['schema']=='ri122-independent-completed-mode-review-v1' and peer['status']=='PASS_COMPLETED_'+p+'_CUSTODY_ONLY' and peer['mode']==mode and not peer['blocking_findings']
 for k in ('source_adjudication','applicability','genuine_outer','root_admission','freeze','authorization','receipt','outputs','before_after_current_identities_match','terminal_owned_group_absent','native_arithmetic_recomputed','native_mathematics_accepted','programme_complete'):assert peer[k]==root[k]
 for row in root['outputs'].values():assert row==full(row['path'])
 for k in ('source_adjudication','applicability','genuine_outer','root_admission','freeze','authorization'):assert root[k]==full(root[k]['path'])
 body=Path(peerpath).read_bytes()
 with (N/(p+'_INDEPENDENT_COMPLETE_REVIEW.json')).open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
 outer=load(N/(p+'_OUTER_TOOL_RESULT.json'))
 value=dict(schema='ri122-root-completed-producer-custody-v1',status='ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY',mode=mode,source_adjudication=full(N/'ROOT_SOURCE_ADJUDICATION.json'),applicability=full(N/(p+'_APPLICABILITY.json')),receipt=full(N/(mode+'-01/receipt.json')),stdout=full(N/(mode+'-01/stdout.log')),genuine_outer=full(N/(p+'_OUTER_TOOL_RESULT.json')),root_complete_review=full(N/(p+'_ROOT_COMPLETE_REVIEW.json')),independent_complete_review=full(N/(p+'_INDEPENDENT_COMPLETE_REVIEW.json')),root_admission=full(N/(p+'_ROOT_ADMISSION.json')),before_after_current_identities_match=True,terminal_owned_group_absent=True,actual_outer_exit=outer['result']['exit_code'],actual_outer_chunk_id=outer['result']['chunk_id'],scientific_math_accepted=False,programme_complete=False,root_witness_acceptance=None if mode=='witness' else full(N/'WITNESS_ROOT_CUSTODY.json'),root_normal_acceptance=full(N/'NORMAL_ROOT_CUSTODY.json') if mode=='optimized' else None,candidate_custody=None if mode=='witness' else full(N/'CANDIDATE_CUSTODY.json'),saved_summary_whole_bytes_equal=True if mode=='optimized' else None)
 return write(N/(p+'_ROOT_CUSTODY.json'),value)
def ordered(mode):
 v=load(N/'PROSPECTIVE_STAGE_INVENTORY.json');d={r['key']:{k:r[k]for k in ('role','path')}for r in v['catalogue']}
 return [d[k]for k in v['stages'][mode]['input_order']]
def prepare(mode):
 assert mode in ('normal','optimized');p=mode.upper()
 fresh=check();save(mode.upper()+'_ROOT_PRE_ISSUANCE_METADATA.json',fresh);assert fresh['all_match'] is True
 preceding='WITNESS' if mode=='normal' else 'NORMAL'
 assert load(N/(preceding+'_ROOT_CUSTODY.json'))['status']=='ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY'
 if mode=='normal':
  body=(N/'witness-01/stdout.log').read_bytes();assert pin(body)==pure(full(N/'witness-01/stdout.log'))
  for dest in (N/'CERTIFICATE.json',T/'CERTIFICATE.json',N/'AUDIT_CANDIDATE.json'):
   with dest.open('xb') as f:f.write(body);f.flush();os.fsync(f.fileno())
   assert dest.read_bytes()==body
  wr=load(N/'witness-01/receipt.json')
  add=dict(schema='ri84-saved-certificate-addendum-v1',authorized_modes=['normal','optimized'],supervisor_sha256=full(N/'supervise.py')['sha256'],checker_sha256=full(T/'check.py')['sha256'],certificate_sha256=pin(body)['sha256'],witness_freeze_payload_sha256=wr['freeze_payload_sha256'],witness_receipt_sha256=full(N/'witness-01/receipt.json')['sha256'])
  write(N/'SAVED_CERTIFICATE_ADDENDUM.json',add)
  write(N/'CANDIDATE_CUSTODY.json',dict(schema='ri122-exact-candidate-custody-v1',whole_bytes_equal=True,scientific_math_accepted=False,replays_admitted=False,original=full(N/'CERTIFICATE.json'),copy=full(T/'CERTIFICATE.json'),audit_copy=full(N/'AUDIT_CANDIDATE.json'),source_stdout=full(N/'witness-01/stdout.log'),saved_addendum=full(N/'SAVED_CERTIFICATE_ADDENDUM.json'),root_witness_acceptance=full(N/'WITNESS_ROOT_CUSTODY.json')))
 app=load(N/'WITNESS_APPLICABILITY.json');app['mode']=mode
 argv=['/opt/homebrew/bin/python3','-I','-S','-B']+(['-O'] if mode=='optimized' else [])+[str(T/'check.py')]
 app['argv']=argv;write(N/(p+'_APPLICABILITY.json'),app)
 f=load(N/'WITNESS_EXECUTION_FREEZE.json');f['mode']=mode;f['argv']=argv;f['attempt_dir']=str(N/(mode+'-01'))
 f.pop('authorization');f['inputs']=[dict(**r,identity=full(r['path'])) for r in ordered(mode)]
 payload=hashlib.sha256(json.dumps(f,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
 au=dict(schema='ri84-execution-authorization-v1',authorized=True,mode=mode,freeze_payload_sha256=payload,supervisor_sha256=f['supervisor_sha256'],addendum_sha256=full(N/'SAVED_CERTIFICATE_ADDENDUM.json')['sha256'])
 write(N/(p+'_AUTHORIZATION.json'),au);f['authorization']=dict(path=str(N/(p+'_AUTHORIZATION.json')),sha256=full(N/(p+'_AUTHORIZATION.json'))['sha256'])
 write(N/(p+'_EXECUTION_FREEZE.json'),f)
 outer=['/opt/homebrew/bin/python3','-I','-S','-B',str(N/'supervise.py'),mode]
 env=f['environment'];cmd='/usr/bin/env -i '+shlex.join([k+'='+v for k,v in env.items()])+' '+shlex.join(outer)
 invocation=dict(cmd=cmd,workdir=str(C),login=False,yield_time_ms=1000,max_output_tokens=2000)
 ra=dict(schema='ri122-root-stage-admission-v1',status='ADMITTED_ONE_FROZEN_'+p+'_INVOCATION',mode=mode,source_adjudication=full(N/'ROOT_SOURCE_ADJUDICATION.json'),applicability=full(N/(p+'_APPLICABILITY.json')),freeze=full(N/(p+'_EXECUTION_FREEZE.json')),authorization=full(N/(p+'_AUTHORIZATION.json')),outer_argv=outer,outer_cwd=str(C),outer_environment=env,outer_invocation=invocation,retry_or_limit_relaxation_authorized=False,history_manifest=full(N/'HISTORY_RECONCILIATION.json'))
 write(N/(p+'_ROOT_ADMISSION.json'),ra)
 return save('RI122_'+p+'_ISSUANCE.json',dict(schema='ri122-root-serial-producer-issuance-v1',mode=mode,accepted_predecessor=ref(N/(preceding+'_ROOT_CUSTODY.json')),admission=ref(N/(p+'_ROOT_ADMISSION.json')),actual_invocation=invocation,later_modes_admitted=False,scientific_math_accepted=False))
if __name__=='__main__':
 if sys.argv[1]=='accept':print(json.dumps(accept(sys.argv[2],sys.argv[3])))
 elif sys.argv[1]=='prepare':print(json.dumps(prepare(sys.argv[2])))
 else:raise ValueError('unknown action')
