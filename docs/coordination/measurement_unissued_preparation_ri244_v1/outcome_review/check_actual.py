"""Independent administrative review of saved RI244 preparation; no subject imports."""
from pathlib import Path
import json,hashlib,os,stat
Q=Path(__file__).resolve().parent
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri247-root-hook-branch-review-6fgw5qd9';D=B/'ri244-current-normal-premode-2kfsmiea'
W=Path('/private/tmp/ri244-preparation-proposal-3udz0imk');E=B/'ri154-white-execution-proposed-42_uvw15';O=B/'ri156-operation-ri244-premode-2kfsmiea'
NAMES=sorted(['PREPARATION_ATTEMPT.json','CUSTODY_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','BOOTSTRAP_PREFLIGHT.json','PRE_MODE_BOOTSTRAP.proposal.py','ADMISSION_CANDIDATE.json'])
ENV={'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(D/'tmp'),'TZ':'UTC','VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
BOUNDS={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864}
count=0;observed={};loaded={}
def need(v,label):
 global count
 if not v:raise ValueError(label)
 count+=1

def canon(v):return (json.dumps(v,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
def eq(a,b,label):need(canon(a)==canon(b),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def rawpin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pure(r):return {k:r[k] for k in ('path','bytes','sha256')}
def route(p):
 pending=list(p.parts[1:]);cur=Path('/');links=[]
 while pending:
  v=pending.pop(0)
  if v in ('','.'):continue
  if v=='..':cur=cur.parent;continue
  x=cur/v;s=x.lstat()
  if stat.S_ISLNK(s.st_mode):
   need(len(links)<64,'bounded link chain');t=os.readlink(x);links.append({'path':str(x),'target':t});tp=Path(t)
   if tp.is_absolute():cur=Path('/');pending=list(tp.parts[1:])+pending
   else:pending=list(tp.parts)+pending
  else:cur=x
 return cur,links

def observe(path):
 p=Path(path);need(p.is_absolute(),'absolute file');resolved,links=route(p);before=resolved.lstat()
 need(stat.S_ISREG(before.st_mode) and 0<=before.st_size<=67108864,'bounded regular file '+str(p))
 h=hashlib.sha256();n=0
 with os.fdopen(os.open(resolved,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  eq(state(os.fstat(f.fileno())),state(before),'opened descriptor '+str(p))
  while True:
   b=f.read(1048576)
   if not b:break
   h.update(b);n+=len(b)
  eq(state(os.fstat(f.fileno())),state(before),'final descriptor '+str(p))
 eq(state(resolved.lstat()),state(before),'final file state '+str(p));need(n==before.st_size and p.resolve()==resolved,'complete file and route '+str(p))
 for l in links:need(os.readlink(l['path'])==l['target'],'retained link target')
 value={'path':str(p),'resolved_path':str(resolved),'symlink_chain':links,'state':state(before),'bytes':n,'sha256':h.hexdigest()}
 if str(p) in observed:eq(value,observed[str(p)],'repeated complete current file '+str(p))
 observed[str(p)]=value
 return value

def verify(row):
 got=observe(row['path']);eq({k:got[k] for k in row},row,'expected full/subset identity '+row['path']);return got

def pairs(items):
 d={}
 for k,v in items:
  need(k not in d,'unique administrative key');d[k]=v
 return d

def load(path,expected=None):
 p=Path(path);got=verify(expected) if expected else observe(p)
 b=p.read_bytes();eq(rawpin(b),{k:got[k] for k in ('bytes','sha256')},'captured whole metadata');eq(state(p.resolve().lstat()),got['state'],'metadata read state')
 need(not p.is_relative_to(E),'no E body decoding')
 v=json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
 need(canon(v)==b,'canonical administrative JSON '+str(p));loaded[str(p)]=v;return v

def ref(path):return pure(observed.get(str(path)) or observe(path))
# Exact root and proposal identity anchors.
decision_ref={'path':str(R/'RI244_PREPARATION_DECISION.json'),'bytes':1007,'sha256':'94e8beecfbb0c19fe206b4e45c22692649aaa4992ec352daf6483b22817f702c'}
decision=load(decision_ref['path'],decision_ref)
seal=load(W/'HANDOFF.json',{'path':str(W/'HANDOFF.json'),'bytes':4462,'sha256':'31e3265d02d9323c0b3224800e70ccac16955c696e0f3f2c2e84af23857b0ba1'})
refs=load(W/'REFERENCES.json');rootcheck=load(R/'RI244_ROOT_PREPARATION_CHECK.json',{'path':str(R/'RI244_ROOT_PREPARATION_CHECK.json'),'bytes':6647,'sha256':'0f65554fce43c28e57bc55953f2644a4c01a68245e49cf82e5aee3d4637302c5'})
for row in seal['files']:verify(row)
eq(sorted(x.name for x in W.iterdir()),seal['namespace'],'source full namespace')
need(decision['operational_authorization'] is False and decision['root_attests_fresh_genuine_host_tool_origin'] is True,'preparation-only decision')
eq(set(decision),set(decision),'set validation replaced below') if False else None
eq(sorted(decision),sorted(['schema','status','preparation_source','proposal_handoff','output','host_transcript','root_attests_fresh_genuine_host_tool_origin','operational_authorization']),'rootdecision8')
eq(decision['preparation_source'],seal['writer'],'exact source selected');eq(decision['proposal_handoff'],ref(W/'HANDOFF.json'),'exact seal selected');eq(decision['output'],str(D),'exact reservation')
eq(decision['status'],'AUTHORIZE_ONE_ADMINISTRATIVE_PREPARATION_ONLY','limited authority')
# Fresh final namespace, regular no-link single-link outputs, and empty directories.
expected_names=sorted(NAMES+['PREPARATION_COMPLETE.json','tmp','monitor']);eq(sorted(x.name for x in D.iterdir()),expected_names,'full D namespace')
need(D.resolve()==D and not D.is_symlink(),'literal D root')
outputs=[];dirs=[]
for name in NAMES+['PREPARATION_COMPLETE.json']:
 p=D/name;s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and p.resolve()==p,'final literal regular single-link '+name)
 got=observe(p);need(got['symlink_chain']==[],'no output symlink route');outputs.append(got)
 if name.endswith('.json'):load(p)
for name in ['tmp','monitor']:
 p=D/name;s=p.lstat();need(stat.S_ISDIR(s.st_mode) and p.resolve()==p and not p.is_symlink(),'literal directory '+name);eq(sorted(x.name for x in p.iterdir()),[],'empty '+name);eq(state(p.lstat()),state(s),'directory stable');dirs.append({'path':str(p),'state':state(s),'entries':[]})
byname={Path(r['path']).name:r for r in outputs};c=loaded[str(D/'PREPARATION_COMPLETE.json')];cust=loaded[str(D/'CUSTODY_BEFORE.json')];pre=loaded[str(D/'BOOTSTRAP_PREFLIGHT.json')];wrapper=loaded[str(D/'ADMISSION_CANDIDATE.json')];vendor=loaded[str(D/'SUPPLIER_BEFORE.json')];etree=loaded[str(D/'E_BEFORE.json')]
eq(c['status'],'UNISSUED_PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','success remains unissued');eq(c['first_error'],None,'no first error')
eq(sorted(c),sorted(['schema','status','first_error','independent_tails','tail_observations','artifacts','input_count','root_decision','operational_authorization','subject_executed','installed_freeze_decoded','E_written','RET_paused']),'COMPLETE13')
for flag in ['operational_authorization','subject_executed','installed_freeze_decoded','E_written']:need(c[flag] is False,'exact false '+flag)
need(c['RET_paused'] is True,'RET paused');eq(c['root_decision'],decision_ref,'complete decision')
artifacts={n:pure(byname[n]) for n in NAMES};eq(c['artifacts'],artifacts,'complete seven real artifact refs')
eq(loaded[str(D/'PREPARATION_ATTEMPT.json')],{'schema':'ri244-unissued-preparation-attempt-v1','decision':decision_ref,'proposal':decision['proposal_handoff'],'no_retry':True,'operational_authorization':False},'whole ATTEMPT')
# Verify every recorded immutable preownership identity, then reconstruct its domain.
rows=cust['identities'];need(len(rows)==2854 and len({x['path'] for x in rows})==2854,'2854 unique whole inputs')
for row in rows:verify(row)
inputmap={x['path']:x for x in rows};registry={}
def reg(row):
 need(row['path'] in inputmap,'input not omitted '+row['path']);eq({k:inputmap[row['path']][k] for k in row},row,'registered expected source/custody '+row['path']);registry.setdefault(row['path'],inputmap[row['path']])
def rd(row):
 reg(row)
 return loaded.get(row['path']) if row['path'] in loaded else load(row['path'],row)
def keep(value):
 if type(value) is dict:
  if {'path','bytes','sha256'}<=set(value):reg(pure(value))
  elif set(value)=={'path','pin'} and type(value['pin']) is dict:reg({'path':value['path'],**value['pin']})
  else:
   for v in value.values():keep(v)
 elif type(value) is list:
  for v in value:keep(v)
helper={'path':str(B/'ri122-root-execution-review-6whn_vky/metadata.py'),'bytes':3144,'sha256':'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'}
reg(helper);reg(decision_ref);rd(decision['proposal_handoff'])
for row in seal['files']:reg(row)
rd(ref(W/'REFERENCES.json'))
for row in refs.values():reg(row)
manifest=rd(refs['source_manifest'])
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:reg(row)
reg(manifest['bootstrap_binding']);qual=rd(refs['qualification'])
for k in ['report','genuine_outer','independent_review']:reg(qual[k])
accepted=rd(refs['input_review']);keep(accepted);request=rd(refs['request']);runtime=rd(refs['runtime']);keep(request);keep(runtime)
eq(rd(runtime['snapshot']),rd(runtime['baseline']),'whole accepted metadata/baseline');eq(rd(runtime['vendor_before']),rd(runtime['vendor_after']),'whole stable supplier projection');eq(rd(runtime['observed_dyld_routes']),rd(runtime['snapshot'])['preobserved_dyld_routes'],'whole sidecar')
ra=rd(runtime['runtime_acceptance']);keep(ra);profiles=rd(ra['profile_review']);keep(profiles);normal=rd(profiles['completions']['profile_normal']);keep(normal)
eq([normal['artifacts']['PRE'],normal['environment']],[request['baseline'],runtime['environment']],'normal baseline/environment relation')
collection=rd(refs['collection']);keep(collection);capture=rd(refs['capture_review']);keep(capture);oldroles=rd(refs['old_roles'])
for row in oldroles['observed_identities']:reg(row)
frozen=rd(refs['copy_observation']);oldvendor=rd(refs['old_supplier']);oldE=rd(refs['old_E']);oldhost=rd(refs['old_host']);host=rd(decision['host_transcript']);oldpre=rd(refs['old_preflight']);keep(oldpre)
oldcard=rd({'path':str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),'bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'});static=rd(oldpre['static_native_adjudication'])
for row in oldvendor['vendor']+oldvendor['tools']:reg(row)
for row in oldE:
 if row['kind']=='file':reg(row['identity'])
eq(list(registry),[r['path'] for r in rows],'exact complete source-derived ordered input domain')
eq([registry[p] for p in registry],rows,'complete registry bodies');eq(c['input_count'],len(rows),'complete input count')
eq(cust,{'schema':'ri244-complete-preparation-custody-v1','identities':rows,'source_states':frozen['source_states'],'historical_roles':refs['old_roles'],'source_manifest':refs['source_manifest'],'root_decision':decision_ref,'host_transcript':decision['host_transcript']},'whole custody record')
eq(oldroles['source_states'],frozen['source_states'],'whole historical source role map');eq({k:len(v) for k,v in frozen['source_states'].items()},{'copies':48,'history':124,'target_originals':30},'retained role multiplicities')
# Whole raw host transcription and live opaque supplier namespace.
eq(host['arguments'],oldhost['arguments'],'unchanged genuine host command');eq(json.loads(host['result']['output']),host['observation'],'exact host stdout');eq(host['observation'],oldhost['observation'],'saved host unchanged');need(host['result']['exit_code']==0 and host['result'].get('session_id') is None and host['result']['chunk_id']=='527491','genuine host receipt')
eq(host['observation']['uname'],list(os.uname()),'current uname still equal')
expected_host={'argv':host['observation']['command'],'exit_code':host['observation']['returncode'],'stdout':host['observation']['stdout'],'stderr':host['observation']['stderr'],'uname':host['observation']['uname']}
eq(vendor['host'],expected_host,'whole generated supplier host');eq(vendor['environment'],ENV,'actual admin environment')
need(type(vendor['observed_at_unix_ns']) is int and vendor['observed_at_unix_ns']>oldvendor['observed_at_unix_ns'],'new vendor observation timestamp')
eq({k:v for k,v in vendor.items() if k not in ('environment','observed_at_unix_ns')},{k:v for k,v in oldvendor.items() if k not in ('environment','observed_at_unix_ns')},'whole supplier historic correspondence')
for row in vendor['vendor']+vendor['tools']:eq(inputmap[row['path']],row,'complete supplier file in verified registry')
for row in vendor['namespace']:
 p=Path(row['path']);s=p.lstat();value={'path':str(p),'kind':row['kind'],'state':state(s)}
 if row['kind']=='directory':need(stat.S_ISDIR(s.st_mode),'supplier directory kind');value['entries']=sorted(x.name for x in p.iterdir())
 else:need(row['kind']=='symlink' and stat.S_ISLNK(s.st_mode),'supplier link kind');value['target']=os.readlink(p)
 eq(state(p.lstat()),state(s),'supplier namespace stable');eq(value,row,'complete actual supplier namespace row')
for path in vendor['absent']:need(not os.path.lexists(path),'current supplier absence')
eq([len(vendor['vendor']),sum(r['bytes'] for r in vendor['vendor']),len(vendor['tools']),len(vendor['namespace']),len(vendor['absent'])],[1810,48024515,4,195,2],'supplier whole domain')
# Whole E metadata and all live rows, without parsing a single E file body.
eq(etree,oldE,'whole saved E body identical');need(len(etree)==58,'58 E entries')
for row in etree:
 p=E/row['relative'];s=p.lstat();need(not stat.S_ISLNK(s.st_mode) and p.resolve()==p,'literal E entry');value={'relative':row['relative'],'kind':row['kind'],'state':state(s)}
 if row['kind']=='directory':need(stat.S_ISDIR(s.st_mode),'E directory');value['entries']=sorted(x.name for x in p.iterdir())
 else:need(row['kind']=='file' and stat.S_ISREG(s.st_mode),'E file');value['identity']=inputmap[str(p)]
 eq(state(p.lstat()),state(s),'E state stable');eq(value,row,'entire fresh E row')
need(sum(r['kind']=='file' for r in etree)==49 and sum(r['kind']=='directory' for r in etree)==9,'E49/9')
# Exact derived preflight/candidate and literal sealed bootstrap.
expected_pre={'schema':'ri244-root-unissued-premode-preflight-v1','status':'PREPARED_UNISSUED_PENDING_INDEPENDENT_ROOT_REVIEW','selected_interpreter_binding':inputmap[manifest['bootstrap_binding']['path']],'source_observation':artifacts['CUSTODY_BEFORE.json'],'runtime_observation':artifacts['SUPPLIER_BEFORE.json'],'E_observation':artifacts['E_BEFORE.json'],'genuine_host':decision['host_transcript'],'source_acceptance':refs['source_review'],'input_acceptance':refs['input_review'],'static_native_adjudication':oldpre['static_native_adjudication'],'platform_premises':static['platform_premises_accepted'],'operation_premises':oldpre['operation_premises'],'environment':ENV,'scientific_execution_authorized':False,'operational_authorization':False}
eq(pre,expected_pre,'whole 16-field actual preflight')
expected_candidate={'schema':'ri156-root-adapter-admission-v1','status':'AUTHORIZE_ONE_BOUNDED_METADATA_ACTION','action':'pre_mode','source_manifest':refs['source_manifest'],'source_review':refs['source_review'],'qualification':refs['qualification'],'request':refs['request'],'output':str(O),'environment':ENV,'bootstrap_preflight':artifacts['BOOTSTRAP_PREFLIGHT.json'],'bounds':BOUNDS,'genuine_outer_required':True}
need(len(expected_candidate)==12,'literal candidate12');eq(wrapper,{'schema':'ri244-wrapped-unissued-admission-v1','status':'UNISSUED_NOT_OPERATIONAL_AUTHORITY','candidate':expected_candidate,'bootstrap_proposal':artifacts['PRE_MODE_BOOTSTRAP.proposal.py'],'root_input_acceptance':refs['input_review'],'future_admission_path':str(D/'ADMIT_PRE_MODE.json'),'operational_authorization':False},'whole wrapped unissued card')
need((D/'PRE_MODE_BOOTSTRAP.proposal.py').read_bytes()==(W/'PRE_MODE_BOOTSTRAP.proposal.txt').read_bytes(),'whole sealed bootstrap exact bytes')
eq(runtime['environment']['TMPDIR'],str(E/'tmp'),'runtime E/tmp');eq(expected_candidate['environment']['TMPDIR'],str(D/'tmp'),'admin D/tmp')
# Complete six tail records, every inner observation and exact completion shape.
expected_tail={'E':{'error':None,'value':etree},'authority_absences':{'error':None,'value':None},'inputs':{'error':None,'value':2854},'namespace':{'error':None,'value':sorted(NAMES+['tmp','monitor'])},'outputs':{'error':None,'value':artifacts},'supplier':{'error':None,'value':{'absent':2,'namespace':195,'tools':4,'vendor':1810}}}
eq(c['independent_tails'],expected_tail,'all complete six tails')
postvendor=c['tail_observations']['supplier'];need(type(postvendor['observed_at_unix_ns']) is int and postvendor['observed_at_unix_ns']>=vendor['observed_at_unix_ns'],'post timestamp ordering')
eq({k:v for k,v in postvendor.items() if k!='observed_at_unix_ns'},{k:v for k,v in vendor.items() if k!='observed_at_unix_ns'},'entire supplier before/post stable fields')
eq(c['tail_observations'],{'inputs':{'errors':[],'values':rows},'namespace':sorted(NAMES+['tmp','monitor']),'outputs':{'errors':[],'values':artifacts},'supplier':postvendor},'every complete tail observation')
for p in [D/'ADMIT_PRE_MODE.json',D/'DISPATCH.json',O,E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:need(not os.path.lexists(p),'authority/operation remains absent')
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized']:eq(sorted(x.name for x in p.iterdir()),[],'no scientific/monitor output')
eq(sorted(p.name for p in Path(refs['request']['path']).parent.iterdir()),['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json'],'original RI241 namespace')
# Genuine invocation and independent startup binding: no replay.
tools=load(R/'RI244_GENUINE_PREPARATION_TOOLS.json');context=load(R/'RI244_PREPARATION_INVOCATION_CONTEXT.json');startup=load(R/'RI244_ADMINISTRATIVE_STARTUP_BINDING.json');adjud=load(R/'RI244_SOURCE_ADJUDICATION.json')
need(tools['initial']['result']['chunk_id']=='b36217' and tools['initial']['result']['session_id']==74730 and tools['terminal']['chunk_id']=='eeaf85' and tools['terminal']['exit_code']==0,'actual initial and terminal relation')
need(tools['initial']['result']['output']==tools['terminal']['output']=='','empty captured outer output')
command="/usr/bin/perl -e 'alarm 300; exec @ARGV or die $!' /opt/homebrew/bin/python3 -I -B "+str(W/'prepare_unissued.py')+' --root-decision '+str(R/'RI244_PREPARATION_DECISION.json')+' --root-decision-sha256 '+decision_ref['sha256']
eq(tools['initial']['arguments']['cmd'],command,'exact admitted preparation command');need(tools['initial']['arguments']['login'] is False and 'workdir' not in tools['initial']['arguments'],'saved actual login/default cwd')
verify(startup['ordinary_administrative_interpreter']);verify(startup['writer']);verify(startup['source_adjudication']);eq(adjud['writer'],seal['writer'],'root accepted exact writer');eq(adjud['status'],'ACCEPT_EXACT_UNEXECUTED_PREPARATION_SOURCE_ONLY','root source-only acceptance')
# Close read-window identities and root-check agreement without trusting its pass label.
for row in rows:verify(row)
for row in outputs:verify(row)
eq(outputs,rootcheck['outputs'],'all complete root-observed output states retained');eq(dirs,rootcheck['directories'],'both root-observed empty directories retained');eq(sorted(p.name for p in D.iterdir()),expected_names,'final full D namespace')
full={'schema':'ri244-independent-preparation-observations-v1','observations':list(observed.values())}
b=canon(full)
with (Q/'OBSERVATIONS.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
need((Q/'OBSERVATIONS.json').read_bytes()==b,'observations exact readback')
result={'schema':'ri244-independent-actual-preparation-check-v1','status':'PASS_COMPLETE_UNISSUED_PREPARATION_ONLY','predicates':count,'distinct_fresh_file_identities':len(observed),'complete_immutable_input_rows':2854,'exact_ordered_input_domain_reconstructed':True,'final_regular_literal_single_link_outputs':outputs,'empty_directories':dirs,'six_full_tail_records_reconstructed':True,'candidate_fields':12,'preflight_fields':len(pre),'COMPLETE_fields':len(c),'bootstrap_exact_sealed_bytes':True,'E_files':49,'E_directories':9,'E_states_membership_and_opaque_bytes_unchanged':True,'supplier_files':1810,'supplier_bytes':48024515,'supplier_namespace_rows':195,'supplier_tools':4,'supplier_absences':2,'source_roles':[48,124,30],'decision':decision_ref,'genuine_tools':ref(R/'RI244_GENUINE_PREPARATION_TOOLS.json'),'invocation_context':ref(R/'RI244_PREPARATION_INVOCATION_CONTEXT.json'),'complete':ref(D/'PREPARATION_COMPLETE.json'),'observations':{'path':str(Q/'OBSERVATIONS.json'),**rawpin(b)},'subject_or_writer_reexecuted':False,'scientific_E_body_decoded':False,'operational_admission_or_pre_mode_result_accepted':False,'global_atomic_snapshot_claim':False}
b=canon(result)
with (Q/'CHECK.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
assert (Q/'CHECK.json').read_bytes()==b
print(json.dumps({'predicates':count,'fresh_files':len(observed),'input_rows':2854,'report':{'path':str(Q/'CHECK.json'),**rawpin(b)},'raw_readback':True}))
