from pathlib import Path
import importlib.util,hashlib,json,os,stat,shlex
B=Path('/Volumes/AI_DATA/development/det-review-evidence');R=Path(Path('/private/tmp/ri234_root_path.txt').read_text());P0=B/'ri230-root-lower-combinations-review-v9mxbmtc';D=B/'ri226-directory-custody-recovery-yvfg_p1b';W=D/'worker_proposal';PW=B/'ri229-reconciliation-preparation-t93t1607/worker_proposal';E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri226-freeze-reconciliation-operation-yvfg_p1b'
h=B/'ri122-root-execution-review-6whn_vky/metadata.py';raw=h.read_bytes();assert len(raw)==3144 and hashlib.sha256(raw).hexdigest()=='d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'
s=importlib.util.spec_from_file_location('m',h);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.D=R
count=0
def eq(a,b):
 global count
 assert m.canonical(a)==m.canonical(b);count+=1
def loadref(r):m.verify(r['path'],r);return m.load(r['path'])
def current(r):eq(m.identity(r['path']),r)
def state(p):
 t=p.lstat();return [t.st_dev,t.st_ino,t.st_mode,t.st_nlink,t.st_size,t.st_mtime_ns,t.st_ctime_ns]
def treecheck(rows):
 assert len(rows)==58 and len({r['relative'] for r in rows})==58
 for row in rows:
  p=E/row['relative'];eq(state(p),row['state']);assert not p.is_symlink()
  if row['kind']=='directory':eq(sorted(x.name for x in p.iterdir()),row['entries'])
  else:assert row['kind']=='file';current(row['identity']);assert row['identity']['state'][3]==1
 for row in rows:eq(state(E/row['relative']),row['state'])
m.verify(P0/'ACTUAL_PREPARATION_ACCEPTANCE.json',dict(bytes=8585,sha256='28d04703c3ce81c952c1ba34a2b2c4cd5021a4411c76fa0fd5871722a1a26fd8'))
assert m.load(P0/'ACTUAL_PREPARATION_ACCEPTANCE.json')['status']=='ACCEPT_ACTUAL_ADMINISTRATIVE_PREPARATION_ONLY'
names=['HOST_GENUINE_TOOL.json','HOST_BEFORE.json','RECONCILE_BOOTSTRAP.py','SOURCES_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','RECONCILE_PREFLIGHT.json','RECONCILIATION_PROPOSAL.json','PREPARATION_CUSTODY.json'];outputs={n:m.identity(D/n) for n in names}
for row in outputs.values():assert row['state'][3]==1 and row['bytes']<=67108864 and row['symlink_chain']==[]
genuine=m.load(P0/'GENUINE_PREPARATION_TOOL.json');decision=m.load(P0/'ROOT_ONE_PREPARATION_DECISION.json');initial=genuine['initial'];terminal=genuine['terminal'];assert initial['result']['session_id']==16198 and terminal['exit_code']==0 and terminal['chunk_id']=='1db8d4'
eq(shlex.split(initial['arguments']['cmd']),decision['command']);eq(initial['arguments']['workdir'],str(D));assert initial['arguments']['login'] is False
stdout=json.loads(terminal['output']);eq(stdout['status'],'PREPARED_FOR_ROOT_PREFLIGHT_REVIEW_NO_ADMISSION');custody=loadref(stdout['custody']);proposal=loadref(stdout['proposal']);eq(stdout['custody'],m.ref(D/'PREPARATION_CUSTODY.json'));eq(stdout['proposal'],m.ref(D/'RECONCILIATION_PROPOSAL.json'))
eq(custody['status'],'PREPARED_NOT_ADMITTED_OR_DISPATCHED');assert len(custody)==35 and not custody['reconciliation_admitted'] and not custody['reconciliation_dispatched'] and not custody['scientific_execution'] and custody['E_read_only'] and custody['ret_paused']
eq(custody['preparation_source_review'],decision['source_review']);eq(custody['preparation_source_manifest'],decision['source_manifest']);eq(custody['preparation_source'],m.ref(PW/'prepare_reconciliation.py'));current(decision['administrative_interpreter']);current(decision['writer'])
for name in ('sealed_source_packet','root_review_support','preparation_support','preparation_dependency_states'):
 for row in custody[name]:current(row)
eq(custody['source_domain'],971);eq(custody['prior_roles'],810);eq(custody['copy_history_targets'],[48,124,30]);assert len(custody['preparation_dependency_states'])==992
eq(sorted(p.name for p in D.iterdir()),custody['root_namespace_expected_after']);eq(custody['root_namespace_expected_after'],sorted(custody['root_namespace_before']+names+['tmp','monitor']))
eq(custody['produced_before_custody'],{n:m.ref(D/n) for n in names if n!='PREPARATION_CUSTODY.json'})
pre=loadref(custody['preflight']);assert len(pre)==10 and pre['schema']=='ri226-root-reconciliation-preflight-v1' and pre['status']=='FRESH_EXACT_READ_ONLY_RECONCILIATION_PREFLIGHT' and pre['scientific_execution'] is False
for role,name in [('sources','SOURCES_BEFORE.json'),('supplier','SUPPLIER_BEFORE.json'),('E_before','E_BEFORE.json'),('host_tool_receipts','HOST_BEFORE.json'),('monitor_bootstrap','RECONCILE_BOOTSTRAP.py')]:eq(pre[role],m.ref(D/name))
manifest=loadref(pre['source_manifest']);inputs=loadref(manifest['files'][0]);repair=loadref(manifest['files'][2]);oldbefore=loadref(repair['roles']['original_before']);oldobs=loadref(repair['roles']['original_observations']);oldcomplete=loadref(repair['roles']['original_complete']);assert oldcomplete['status']=='REFUSED_RETAIN_ALL_PARTIALS'
eq(custody['retained_failure'],repair['roles']['original_complete']);eq(custody['retained_postflight'],repair['roles']['postflight']);eq(custody['original_bindings'],oldbefore['bindings']);eq(custody['original_source_observation'],repair['roles']['original_sources'])
oldsrc=loadref(custody['original_source_observation']);eq(oldsrc,oldbefore['source_observations']);assert len(oldsrc)==904
for row in oldsrc+list(oldbefore['bindings'].values()):current(row)
eq(sorted(x.name for x in Path(repair['roles']['original_complete']['path']).parent.iterdir()),['ATTEMPT.json','BEFORE.json','COMPLETE.json','OBSERVATIONS.json'])
expected={r['path']:r for r in inputs['files']+repair['files']+manifest['files']+[pre['source_manifest'],m.ref(D/'ROOT_SOURCE_REVIEW.json'),pre['monitor_bootstrap']]};sources=loadref(pre['sources']);eq([r['path'] for r in sources],sorted(expected));assert len(sources)==971
for row in sources:eq(m.pure(row),m.pure(expected[row['path']]));current(row)
boot=m.ref(PW/'RECONCILE_BOOTSTRAP.source-only.py');eq(m.pure(boot),m.pure(pre['monitor_bootstrap']));assert (D/'RECONCILE_BOOTSTRAP.py').read_bytes()==Path(boot['path']).read_bytes()
ENV=dict(LC_ALL='C',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',PATH='/usr/bin:/bin',TMPDIR=str(D/'tmp'),TZ='UTC',VECLIB_MAXIMUM_THREADS='1',__CF_USER_TEXT_ENCODING='0x1F5:0x0:0x0');eq(pre['environment'],ENV)
supplier=loadref(pre['supplier']);history=loadref(inputs['roles']['historical_supplier']);eq({k:v for k,v in supplier.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in history.items() if k not in ('environment','observed_at_unix_ns')});eq(supplier['environment'],ENV);assert len(supplier)==7 and len(supplier['vendor'])==1810 and len(supplier['tools'])==4 and len(supplier['namespace'])==195 and len(supplier['absent'])==2
for row in supplier['vendor']+supplier['tools']:current(row)
for row in supplier['namespace']:
 p=Path(row['path']);eq(state(p),row['state'])
 if row['kind']=='directory':assert p.is_dir();eq(sorted(x.name for x in p.iterdir()),row['entries'])
 else:assert row['kind']=='symlink' and p.is_symlink();eq(os.readlink(p),row['target'])
for path in supplier['absent']:assert not os.path.lexists(path)
eq(list(os.uname()),supplier['host']['uname'])
host=loadref(pre['host_tool_receipts']);hostraw=loadref(host['genuine_tool']);originalhost=loadref(custody['original_genuine_host']);eq(originalhost,hostraw);eq(custody['original_genuine_host'],decision['host']);eq(custody['canonical_genuine_host'],host['genuine_tool']);eq(hostraw['observation'],json.loads(hostraw['result']['output']));assert hostraw['result']['chunk_id']=='ff059f' and hostraw['result']['exit_code']==0
eq(host,dict(schema='ri209-root-host-command-record-v1',**hostraw['observation'],genuine_tool=host['genuine_tool']));eq(host['stdout'],supplier['host']['stdout']);eq(host['command'],supplier['host']['argv']);eq(host['uname'],supplier['host']['uname'])
etree=loadref(pre['E_before']);eq(etree,sorted(oldobs['E_after'],key=lambda r:r['relative']));treecheck(etree);post=loadref(custody['retained_postflight']);current(post['installed_partial']);eq(m.ref(E/'AUTHORIZED_FREEZE.json')['sha256'],inputs['roles']['result']['sha256']);assert (E/'AUTHORIZED_FREEZE.json').read_bytes()==Path(inputs['roles']['result']['path']).read_bytes()
assert len(proposal)==7 and proposal['schema']=='ri229-unissued-reconciliation-proposal-v1' and proposal['status']=='UNISSUED_REQUIRES_ROOT_PREFLIGHT_REVIEW' and proposal['active_card_created'] is False and proposal['dispatch_created'] is False
limits=dict(wall_seconds=180,rss_kib=524288,target_poll_seconds=.025,maximum_sample_gap_seconds=.1,ps_timeout_seconds=.05,file_bytes=67108864)
eq(proposal['proposed_admission_fields'],dict(schema='ri226-root-read-only-reconciliation-admission-v1',status='AUTHORIZE_ONE_READ_ONLY_RECONCILIATION',source_manifest=pre['source_manifest'],source_review=m.ref(D/'ROOT_SOURCE_REVIEW.json'),preflight=custody['preflight'],output=str(O),environment=ENV,limits=limits,genuine_outer_required=True));eq(proposal['future_admission_path'],str(D/'ADMIT_RECONCILE.json'))
vendor='/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9';outer=['/usr/bin/env','-i',*[k+'='+v for k,v in ENV.items()],'/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',vendor,'-I','-B',str(D/'RECONCILE_BOOTSTRAP.py')];dispatch=proposal['dispatch_fields_without_admission'];eq(dispatch,dict(outer_argv=outer,shell_command=shlex.join(outer),cwd=str(D),login=False,bootstrap=pre['monitor_bootstrap'],monitor_source=m.ref(B/'ri141-white-bootstrap-source-h58ls076/prepare.py'),external_timeout_seconds=960,single_attempt=True,actual_execution_not_yet_started=True));eq(stdout['exact_tool_arguments'],dict(cmd=shlex.join(outer),workdir=str(D),login=False,yield_time_ms=1000,max_output_tokens=4000))
for p in [D/'tmp',D/'monitor',E/'tmp',E/'runs/normal',E/'runs/optimized']:eq(list(p.iterdir()),[])
for p in [O,D/'ADMIT_RECONCILE.json',D/'DISPATCH.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:assert not os.path.lexists(p)
for row in outputs.values():current(row)
eq(m.snapshot(),m.load(R/'REPO_ENTRY.json'));treecheck(etree)
result=dict(schema='ri234-root-current-predispatch-check-v1',status='PASS_FRESH_RECONCILIATION_PREDISPATCH_CUSTODY',accepted_preparation=m.ref(P0/'ACTUAL_PREPARATION_ACCEPTANCE.json'),historical_checker=m.ref(P0/'check_concrete_preparation.py'),canonical_comparisons=count,outputs=list(outputs.values()),source_domain=971,preparation_dependencies=992,old_sources=904,old_bindings=9,vendor=1810,tools=4,namespaces=195,absences=2,E_files=49,E_directories=9,full_E_unchanged=True,original_failure_unchanged=True,proposal_unissued=True,no_admission_or_dispatch=True,bootstrap_not_run=True,repository_unchanged=True,qualification_credit=0,RET_paused=True)
result['fresh_observed_at_unix_ns']=__import__('time').time_ns()
result['checker']=m.ref(Path(__file__).resolve())
print(json.dumps(dict(record=m.save('FRESH_PREDISPATCH_CHECK.json',result),canonical_comparisons=count,status=result['status'])))
