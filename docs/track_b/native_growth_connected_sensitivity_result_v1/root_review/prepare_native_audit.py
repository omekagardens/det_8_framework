from native_serial import *
source120=B/'ri120-root-source-review-sksu97l1/ROOT_ADJUDICATION.json'
fresh=check();save('AUDIT_ROOT_PRE_ISSUANCE_METADATA.json',fresh);assert fresh['all_match'] is True
for mode in ('witness','normal','optimized'):
 c=load(N/(mode.upper()+'_ROOT_CUSTODY.json'))
 assert c['status']=='ACCEPT_COMPLETED_PRODUCER_CUSTODY_ONLY' and c['mode']==mode and c['actual_outer_exit']==0 and c['terminal_owned_group_absent'] is True
 for key in ('receipt','stdout','genuine_outer','root_complete_review','independent_complete_review','root_admission','applicability','source_adjudication'):assert c[key]==full(c[key]['path'])
assert (N/'normal-01/stdout.log').read_bytes()==(N/'optimized-01/stdout.log').read_bytes()
for path in (N/'CERTIFICATE.json',T/'CERTIFICATE.json',N/'AUDIT_CANDIDATE.json'):assert path.read_bytes()==(N/'witness-01/stdout.log').read_bytes()
for name in ('AUDIT_INPUT.json','AUDIT_BINDING.json','AUDIT_APPLICABILITY.json','AUDIT_EXECUTION_FREEZE.json','AUDIT_AUTHORIZATION.json','AUDIT_ROOT_ADMISSION.json','audit-01'):assert not (N/name).exists()
files={k:ref(T/'inputs'/name) for k,name in dict(ri88='ri88.json',ri111='ri111.md',ri109_adjudication='ri109_adjudication.json',ri111_adjudication='ri111_adjudication.json',ri115_adjudication='ri115_adjudication.json',ri117='ri117.md',ri117_connected='ri117_connected.md',ri117_adjudication='ri117_adjudication.json').items()};files['candidate']=ref(N/'AUDIT_CANDIDATE.json')
sources=dict(checker=ref(T/'check.py'),protocol=ref(T/'IMPLEMENTATION.md'),contract=ref(T/'AUDIT_CONTRACT.md'))
custody=[dict(role='producer_witness_stdout',**ref(N/'witness-01/stdout.log'))]+[dict(role='producer_'+m+'_custody',**ref(N/(m.upper()+'_ROOT_CUSTODY.json'))) for m in ('witness','normal','optimized')]+[dict(role='consumer_source_review',**ref(source120))]
desc=dict(schema='ri120-independent-audit-input-v1',phase='fixed_saved_certificate_audit',files=files,accepted_sources=sources,audit_source=ref(T/'audit_saved_certificate.py'),custody_dependencies=custody)
write(N/'AUDIT_INPUT.json',desc)
write(N/'AUDIT_BINDING.json',dict(schema='ri122-actual-three-mode-audit-binding-v1',status='ACCEPT_COMPLETED_THREE_MODE_CUSTODY_FOR_SOURCE_BINDING_ONLY',audit_admitted=False,descriptor=full(N/'AUDIT_INPUT.json'),candidates=dict(original=full(N/'CERTIFICATE.json'),native=full(T/'CERTIFICATE.json'),audit=full(N/'AUDIT_CANDIDATE.json')),custodies={m:full(N/(m.upper()+'_ROOT_CUSTODY.json')) for m in ('witness','normal','optimized')},outer_completions={m:full(N/(m.upper()+'_OUTER_TOOL_RESULT.json')) for m in ('witness','normal','optimized')},candidate_custody=full(N/'CANDIDATE_CUSTODY.json'),source_adjudication=full(N/'ROOT_SOURCE_ADJUDICATION.json'),ri120_source_adjudication=full(source120),history_manifest=full(N/'HISTORY_RECONCILIATION.json')))
app=load(N/'WITNESS_APPLICABILITY.json');di=full(N/'AUDIT_INPUT.json')
argv=['/opt/homebrew/bin/python3','-I','-S','-B',str(T/'audit_saved_certificate.py'),str(N/'AUDIT_INPUT.json'),str(di['bytes']),di['sha256']]
app.update(mode='audit',supervisor=full(N/'launch_audit.py'),target=full(T/'audit_saved_certificate.py'),argv=argv);write(N/'AUDIT_APPLICABILITY.json',app)
f=load(N/'WITNESS_EXECUTION_FREEZE.json');f.pop('authorization');f.update(schema='ri95-certificate-audit-freeze-v1',mode='audit',supervisor_sha256=full(N/'launch_audit.py')['sha256'],supervisor=dict(path=str(N/'launch_audit.py'),identity=full(N/'launch_audit.py')),argv=argv,attempt_dir=str(N/'audit-01'),inputs=[dict(**r,identity=full(r['path'])) for r in ordered('audit')])
assert len(f['inputs'])==3770 and len({r['path'] for r in f['inputs']})==3753
payload=hashlib.sha256(json.dumps(f,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
write(N/'AUDIT_AUTHORIZATION.json',dict(schema='ri95-certificate-audit-authorization-v1',authorized=True,mode='audit',freeze_payload_sha256=payload,supervisor_sha256=f['supervisor_sha256']))
f['authorization']=dict(path=str(N/'AUDIT_AUTHORIZATION.json'),sha256=full(N/'AUDIT_AUTHORIZATION.json')['sha256']);write(N/'AUDIT_EXECUTION_FREEZE.json',f)
outer=['/opt/homebrew/bin/python3','-I','-S','-B',str(N/'launch_audit.py'),'audit'];env=f['environment']
invocation=dict(cmd='/usr/bin/env -i '+shlex.join([k+'='+v for k,v in env.items()])+' '+shlex.join(outer),workdir=str(C),login=False,yield_time_ms=1000,max_output_tokens=2000)
write(N/'AUDIT_ROOT_ADMISSION.json',dict(schema='ri122-root-stage-admission-v1',status='ADMITTED_ONE_FROZEN_AUDIT_INVOCATION',mode='audit',source_adjudication=full(N/'ROOT_SOURCE_ADJUDICATION.json'),applicability=full(N/'AUDIT_APPLICABILITY.json'),freeze=full(N/'AUDIT_EXECUTION_FREEZE.json'),authorization=full(N/'AUDIT_AUTHORIZATION.json'),outer_argv=outer,outer_cwd=str(C),outer_environment=env,outer_invocation=invocation,retry_or_limit_relaxation_authorized=False,history_manifest=full(N/'HISTORY_RECONCILIATION.json')))
print(json.dumps(save('RI122_AUDIT_ISSUANCE.json',dict(schema='ri122-root-independent-audit-issuance-v1',accepted_producer_custodies={m:ref(N/(m.upper()+'_ROOT_CUSTODY.json')) for m in ('witness','normal','optimized')},admission=ref(N/'AUDIT_ROOT_ADMISSION.json'),actual_invocation=invocation,scientific_math_accepted=False))))
