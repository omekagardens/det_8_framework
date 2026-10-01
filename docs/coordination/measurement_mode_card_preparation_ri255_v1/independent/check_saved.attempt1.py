"""Independent administrative saved-preparation review. No target/helper import or execution."""
from pathlib import Path
import os,stat,json,hashlib
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
D=B/'ri249-normal-mode-card-preparation-y170alnf';O=B/'ri156-operation-ri249-mode-card-y170alnf';E=B/'ri154-white-execution-proposed-42_uvw15'
R=B/'ri255-root-compensation-review-m__fsupr';W=Path('/private/tmp/ri249-mode-card-preparation-proposal-y170alnf');Q=Path('/private/tmp/ri255-independent-mode-preparation-6qxmfcv3')
CAP=67108864; predicates=0; identities={}; payload={}; expected={}; decoded=[]
def require(ok,label):
 global predicates
 predicates+=1
 if not ok:raise ValueError(label)
def canon(v):return (json.dumps(v,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode('ascii')
def eq(a,b,label):require(canon(a)==canon(b),label)
def state(s):return [s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns]
def identity(path):
 p=Path(path);require(p.is_absolute(),'absolute '+str(p));pending=list(p.parts[1:]);cur=Path('/');links=[]
 while pending:
  part=pending.pop(0)
  if part in ('','.'):continue
  if part=='..':cur=cur.parent;continue
  nxt=cur/part;s=nxt.lstat()
  if stat.S_ISLNK(s.st_mode):
   require(len(links)<64,'link limit');target=os.readlink(nxt);links.append({'path':str(nxt),'target':target});t=Path(target)
   if t.is_absolute():cur=Path('/');pending=list(t.parts[1:])+pending
   else:pending=list(t.parts)+pending
  else:cur=nxt
 a=cur.lstat();require(stat.S_ISREG(a.st_mode) and a.st_size<=CAP,'bounded file '+str(p));h=hashlib.sha256();n=0
 with os.fdopen(os.open(cur,os.O_RDONLY|os.O_NOFOLLOW),'rb') as f:
  eq(state(os.fstat(f.fileno())),state(a),'opened stable '+str(p))
  while True:
   chunk=f.read(1024*1024)
   if not chunk:break
   n+=len(chunk);h.update(chunk)
  eq(state(os.fstat(f.fileno())),state(a),'descriptor stable '+str(p))
 eq(state(cur.lstat()),state(a),'path stable '+str(p));require(n==a.st_size and p.resolve()==cur,'resolution stable '+str(p))
 for link in links:eq(os.readlink(link['path']),link['target'],'link stable')
 return {'path':str(p),'resolved_path':str(cur),'symlink_chain':links,'bytes':n,'sha256':h.hexdigest(),'state':state(a)}
def pure(row):return {k:row[k] for k in ('path','bytes','sha256')}
def observe(path):
 path=str(path)
 if path not in identities:identities[path]=identity(path)
 return identities[path]
def verify(row,domain=False):
 require(isinstance(row,dict) and {'path','bytes','sha256'}<=set(row),'pin shape')
 actual=observe(row['path']);eq({k:actual[k] for k in row},row,'whole expected identity '+row['path'])
 if domain:expected[row['path']]=actual
 return actual
def parse(path,canonical=True):
 p=Path(path);require(not str(p).startswith(str(E)+'/'),'no E body decode');require(p.suffix=='.json','admin JSON only')
 before=observe(p);b=p.read_bytes();require(len(b)==before['bytes'] and hashlib.sha256(b).hexdigest()==before['sha256'],'admin read matches hash')
 def pairs(items):
  out={}
  for k,v in items:require(k not in out,'duplicate JSON field');out[k]=v
  return out
 def bad(v):raise ValueError('nonfinite '+v)
 v=json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
 if canonical:eq(b.decode('ascii'),canon(v).decode('ascii'),'canonical '+str(p))
 payload[str(p)]=b;decoded.append(str(p));return v
def read(row):verify(row,True);return parse(row['path'])
def keep(v):
 if type(v) is dict:
  if {'path','bytes','sha256'}<=set(v):verify(pure(v),True)
  elif set(v)=={'path','pin'} and type(v['pin']) is dict:verify({'path':v['path'],**v['pin']},True)
  else:
   for c in v.values():keep(c)
 elif type(v) is list:
  for c in v:keep(c)
def filepin(path):return pure(observe(path))
# Exact root authority and retained whole accepted source.
decisionpin={'path':str(R/'PREPARATION_DECISION.json'),'bytes':1038,'sha256':'5ed6d0a72d6ddbdcacda804d7ab677f971650ba8f6e5af100a677735a539ecc4'}
decision=read(decisionpin);eq(set(decision)==set(['schema','status','preparation_source','proposal_handoff','output','host_transcript','root_attests_fresh_genuine_host_tool_origin','operational_authorization']),True,'decision8')
eq([decision['schema'],decision['status'],decision['output'],decision['root_attests_fresh_genuine_host_tool_origin'],decision['operational_authorization']],['ri249-root-unissued-mode-card-preparation-decision-v1','AUTHORIZE_ONE_ADMINISTRATIVE_PREPARATION_ONLY',str(D),True,False],'whole authority limits')
verify({'path':str(B/'ri122-root-execution-review-6whn_vky/metadata.py'),'bytes':3144,'sha256':'d2825bb1ea78306388a410d9b5aa9b931f72cb6a78334bc69151560f6b2584a7'},True)
verify(decision['preparation_source'],True);h=read(decision['proposal_handoff']);eq(sorted(p.name for p in W.iterdir()),h['namespace'],'source17 namespace')
for row in h['files']:verify(row,True)
refs=read(filepin(W/'REFERENCES.json'));require(len(refs)==27,'complete27 reference roles')
for row in refs.values():verify(row,True)
manifest=read(refs['source_manifest']);require(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'complete11/567')
for row in [manifest['adapter'],*manifest['modules'].values(),*manifest['dependencies']]:verify(row,True)
require(manifest['bootstrap_provenance'] in manifest['dependencies'],'bootstrap provenance')
binding=verify(manifest['bootstrap_binding'],True)
qual=read(refs['qualification']);eq(qual['source_manifest'],refs['source_manifest'],'qualification source');eq([qual['status'],qual['all_passed'],qual['scientific_execution'],len(qual['controls'])],['ACCEPT_EXACT_INERT_ADAPTER_CONTROLS',True,False,106],'original106 acceptance')
for k in ['report','genuine_outer','independent_review']:verify(qual[k],True)
input_review=read(refs['input_review']);keep(input_review);eq([input_review['request'],input_review['runtime']],[refs['request'],refs['runtime']],'whole accepted input refs')
request=read(refs['request']);runtime=read(refs['runtime']);require(len(request)==5 and len(runtime)==13,'old request5/runtime13');keep(request);keep(runtime)
eq(runtime['freeze'],{k:request['freeze'][k] for k in ('bytes','sha256')},'freeze representations');eq([runtime['mode'],runtime['phase'],request['mode']],['normal','pre','normal'],'normal pre runtime')
eq(read(runtime['snapshot']),read(runtime['baseline']),'complete current snapshot/baseline');eq(read(runtime['vendor_before']),read(runtime['vendor_after']),'stable supplier projection')
eq(read(runtime['observed_dyld_routes']),read(runtime['snapshot'])['preobserved_dyld_routes'],'all dyld routes')
ra=read(runtime['runtime_acceptance']);keep(ra);profiles=read(ra['profile_review']);keep(profiles);normal=read(profiles['completions']['profile_normal']);keep(normal)
eq([normal['artifacts']['PRE'],normal['environment']],[request['baseline'],runtime['environment']],'genuine profile baseline/env')
collection=read(refs['collection']);keep(collection);capture=read(refs['capture_review']);keep(capture)
pre_review=read(refs['pre_mode_acceptance']);keep(pre_review)
eq([pre_review['status'],pre_review['scientific_execution'],pre_review['mode_card_created'],pre_review['qualification_credit'],pre_review['RET_paused']],['ACCEPT_ONE_NORMAL_PRE_MODE_METADATA_OPERATION_ONLY',False,False,0,True],'predecessor scope')
eq([pre_review['result'],pre_review['root_custody'],pre_review['root_check']],[refs['pre_result'],refs['pre_mode_postflight'],refs['pre_mode_root_check']],'predecessor exact links')
pre=read(refs['pre_result']);keep(pre)
eq(pre,{'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':'normal','freeze':runtime['freeze'],'runtime_acceptance':runtime['runtime_acceptance'],'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,'observed_dyld_routes':runtime['observed_dyld_routes'],'metadata_record':refs['runtime']},'full pre_result9')
previous=read(refs['pre_mode_postflight']);keep(previous);require(len(previous['input_identities'])==2883,'all2883 prior objects')
for row in previous['input_identities']:verify(row,True)
priorcheck=read(refs['pre_mode_root_check']);keep(priorcheck);eq(priorcheck['full_result'],pre,'full prior root result')
for row in priorcheck['output_identities']+priorcheck['monitor_identities']:verify(row,True)
oldroles=read(refs['old_roles']);require(len(oldroles['observed_identities'])==2811,'all2811 older roles')
for row in oldroles['observed_identities']:verify(row,True)
frozen=read(refs['copy_observation']);eq(frozen['source_states'],oldroles['source_states'],'frozen complete source roles');eq({k:len(v) for k,v in frozen['source_states'].items()},{'copies':48,'history':124,'target_originals':30},'all48/124/30 roles')
oldvendor=read(refs['old_supplier']);oldE=read(refs['old_E']);oldhost=read(refs['old_host']);host=read(decision['host_transcript'])
eq(sorted(host),['arguments','observation','result'],'whole host3');eq(host['arguments'],oldhost['arguments'],'same benign command');eq(json.loads(host['result']['output']),host['observation'],'whole genuine host stdout');eq(host['observation'],oldhost['observation'],'whole saved host unchanged');eq(host['observation']['uname'],list(os.uname()),'current uname')
require(host['result']['chunk_id']=='a2776e' and host['result']['exit_code']==0 and 'session_id' not in host['result'],'actual current host terminal')
oldpre=read(refs['old_preflight']);keep(oldpre)
oldadmit=read({'path':str(B/'ri204-root-adapters-f04k2tg9/ADMIT_ADAPTERS.json'),'bytes':2114,'sha256':'ac86cac1f9973266d84b2a1ad1b9a34e9655d897153dc264d6b0805f437389cd'})
static=read(oldpre['static_native_adjudication'])
# Independent live opaque closure including whole supplier selection/namespace.
for row in oldvendor['vendor']+oldvendor['tools']:verify(row,True)
for row in oldvendor['namespace']:
 p=Path(row['path']);st=state(p.lstat());v={'path':str(p),'kind':row['kind'],'state':st}
 if row['kind']=='directory':require(stat.S_ISDIR(st[2]),'supplier directory');v['entries']=sorted(x.name for x in p.iterdir())
 else:require(row['kind']=='symlink' and p.is_symlink(),'supplier symlink');v['target']=os.readlink(p)
 eq(state(p.lstat()),st,'namespace stable');eq(v,row,'whole supplier namespace')
for p in oldvendor['absent']:require(not os.path.lexists(p),'supplier absent')
for row in oldE:
 p=E/row['relative'];require(p.resolve()==p and not p.is_symlink(),'literal E');st=state(p.lstat());v={'relative':row['relative'],'kind':row['kind'],'state':st}
 if row['kind']=='directory':require(stat.S_ISDIR(st[2]),'E directory');v['entries']=sorted(x.name for x in p.iterdir())
 else:require(row['kind']=='file','E file kind');v['identity']=verify(row['identity'],True)
 eq(state(p.lstat()),st,'E stable');eq(v,row,'whole E record')
require(len(oldE)==58 and sum(r['kind']=='file' for r in oldE)==49,'complete E49/9')
# Read only produced administrative bodies and capture literal output states.
names=['PREPARATION_ATTEMPT.json','CUSTODY_BEFORE.json','SUPPLIER_BEFORE.json','E_BEFORE.json','BOOTSTRAP_PREFLIGHT.json','MODE_CARD_REQUEST.json','MODE_CARD_BOOTSTRAP.proposal.py','ADMISSION_CANDIDATE.json','PREPARATION_COMPLETE.json']
eq(sorted(p.name for p in D.iterdir()),sorted(names+['tmp','monitor']),'final9file2dir namespace')
output_states={}
for n in names:
 r=observe(D/n);require(r['resolved_path']==r['path'] and r['symlink_chain']==[] and r['state'][3]==1 and stat.S_ISREG(r['state'][2]),'literal regular single-link output '+n);output_states[n]=r
for n in ['tmp','monitor']:
 p=D/n;require(p.resolve()==p and not p.is_symlink() and p.is_dir(),'literal empty owned directory');eq(sorted(x.name for x in p.iterdir()),[],'no monitor or temp activity')
attempt=parse(D/'PREPARATION_ATTEMPT.json');custody=parse(D/'CUSTODY_BEFORE.json');vendor=parse(D/'SUPPLIER_BEFORE.json');e=parse(D/'E_BEFORE.json');flight=parse(D/'BOOTSTRAP_PREFLIGHT.json');newreq=parse(D/'MODE_CARD_REQUEST.json');wrapper=parse(D/'ADMISSION_CANDIDATE.json');complete=parse(D/'PREPARATION_COMPLETE.json')
ENV={'LC_ALL':'C','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1','OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','PATH':'/usr/bin:/bin','TMPDIR':str(D/'tmp'),'TZ':'UTC','VECLIB_MAXIMUM_THREADS':'1','__CF_USER_TEXT_ENCODING':'0x1F5:0x0:0x0'}
BOUNDS={'wall_seconds':180,'rss_kib':524288,'target_poll_seconds':0.025,'maximum_sample_gap_seconds':0.1,'ps_timeout_seconds':0.05,'file_bytes':67108864}
eq(attempt,{'schema':'ri249-unissued-mode-card-preparation-attempt-v1','decision':decisionpin,'proposal':decision['proposal_handoff'],'no_retry':True,'operational_authorization':False},'entire attempt5')
require(len(custody['identities'])==2920 and len(expected)==2920,'independently reconstructed2920 domain')
eq(sorted(r['path'] for r in custody['identities']),sorted(expected),'complete expected source/input membership')
for row in custody['identities']:eq(row,expected[row['path']],'all six-field saved identity and seven-state')
eq({k:v for k,v in custody.items() if k!='identities'},{'schema':'ri249-complete-mode-card-preparation-custody-v1','source_states':frozen['source_states'],'historical_roles':refs['old_roles'],'source_manifest':refs['source_manifest'],'root_decision':decisionpin,'host_transcript':decision['host_transcript']},'complete custody envelope')
eq({k:v for k,v in vendor.items() if k not in ['environment','observed_at_unix_ns']},{k:v for k,v in oldvendor.items() if k not in ['environment','observed_at_unix_ns']},'whole old/new vendor stable fields');eq(vendor['environment'],ENV,'complete administrative env10');require(type(vendor['observed_at_unix_ns']) is int and vendor['observed_at_unix_ns']>0,'observed supplier time')
eq(e,oldE,'complete saved E tree');eq(newreq,{'freeze':request['freeze'],'mode':'normal','pre':refs['pre_result'],'normal_acceptance':None},'request4 exact')
require((D/'MODE_CARD_REQUEST.json').read_bytes()==(W/'MODE_CARD_REQUEST.proposal.json').read_bytes(),'exact sealed request bytes')
eq(flight,{'schema':'ri249-root-unissued-mode-card-preflight-v1','status':'PREPARED_UNISSUED_PENDING_INDEPENDENT_ROOT_REVIEW','selected_interpreter_binding':binding,'source_observation':filepin(D/'CUSTODY_BEFORE.json'),'runtime_observation':filepin(D/'SUPPLIER_BEFORE.json'),'E_observation':filepin(D/'E_BEFORE.json'),'genuine_host':decision['host_transcript'],'source_acceptance':refs['source_review'],'input_acceptance':refs['pre_mode_acceptance'],'static_native_adjudication':oldpre['static_native_adjudication'],'platform_premises':static['platform_premises_accepted'],'operation_premises':oldpre['operation_premises'],'environment':ENV,'scientific_execution_authorized':False,'operational_authorization':False},'whole preflight15')
boot=(D/'MODE_CARD_BOOTSTRAP.proposal.py').read_bytes();require(boot==(W/'MODE_CARD_BOOTSTRAP.proposal.txt').read_bytes(),'whole sealed bootstrap unchanged')
candidate={'schema':'ri156-root-adapter-admission-v1','status':'AUTHORIZE_ONE_BOUNDED_METADATA_ACTION','action':'mode_card','source_manifest':refs['source_manifest'],'source_review':refs['source_review'],'qualification':refs['qualification'],'request':filepin(D/'MODE_CARD_REQUEST.json'),'output':str(O),'environment':ENV,'bootstrap_preflight':filepin(D/'BOOTSTRAP_PREFLIGHT.json'),'bounds':BOUNDS,'genuine_outer_required':True}
eq(wrapper,{'schema':'ri249-wrapped-unissued-mode-card-admission-v1','status':'UNISSUED_NOT_OPERATIONAL_AUTHORITY','candidate':candidate,'bootstrap_proposal':filepin(D/'MODE_CARD_BOOTSTRAP.proposal.py'),'root_input_acceptance':refs['pre_mode_acceptance'],'future_admission_path':str(D/'ADMIT_MODE_CARD.json'),'operational_authorization':False},'whole wrapper7/candidate12')
# Complete all six saved tails, their full observations, artifact set, and success envelope.
artifacts={n:filepin(D/n) for n in names if n!='PREPARATION_COMPLETE.json'}
namespace=sorted([n for n in names if n!='PREPARATION_COMPLETE.json']+['tmp','monitor'])
observations=complete['tail_observations'];eq(set(observations)=={'inputs','supplier','outputs','namespace'},True,'complete tail observations4')
eq(observations['inputs'],{'values':custody['identities'],'errors':[]},'all inputs post-body retained same order')
eq(observations['outputs'],{'values':artifacts,'errors':[]},'all8 output post-body pins');eq(observations['namespace'],namespace,'pre-COMPLETE namespace')
eq({k:v for k,v in observations['supplier'].items() if k!='observed_at_unix_ns'},{k:v for k,v in vendor.items() if k!='observed_at_unix_ns'},'whole supplier tail except time');require(type(observations['supplier']['observed_at_unix_ns']) is int and observations['supplier']['observed_at_unix_ns']>0,'tail supplier timestamp')
tails={'inputs':{'value':2920,'error':None},'supplier':{'value':{'vendor':1810,'namespace':195,'tools':4,'absent':2},'error':None},'E':{'value':oldE,'error':None},'authority_absences':{'value':None,'error':None},'outputs':{'value':artifacts,'error':None},'namespace':{'value':namespace,'error':None}}
eq(complete,{'schema':'ri249-unissued-mode-card-preparation-completion-v1','status':'UNISSUED_PREPARED_PENDING_INDEPENDENT_ROOT_REVIEW','first_error':None,'independent_tails':tails,'tail_observations':observations,'artifacts':artifacts,'input_count':2920,'root_decision':decisionpin,'operational_authorization':False,'subject_executed':False,'installed_freeze_decoded':False,'E_written':False,'RET_paused':True},'whole COMPLETE13')
for p in [O,D/'ADMIT_MODE_CARD.json',D/'DISPATCH.json',E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:require(not os.path.lexists(p),'no authority or operation '+str(p))
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized']:eq(sorted(x.name for x in p.iterdir()),[],'unexecuted E mode '+str(p))
eq(sorted(x.name for x in Path(refs['request']['path']).parent.iterdir()),['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json'],'preserved RI241 namespace')
priorout=Path(refs['pre_result']['path']).parent;priormon=Path(priorcheck['monitor_identities'][0]['path']).parent
for p,want in [(priorout,['ATTEMPT.json','COMPLETE.json','RESULT.json']),(priormon,['PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stderr','PRE_MODE.stdout']),(priormon.parent,previous['D_namespace']),(priormon.parent/'tmp',[])]:eq(sorted(x.name for x in p.iterdir()),sorted(want),'previous namespace '+str(p))
# Tool wrappers deliberately preserve original JSON serialization, not canonical demand.
toolpin={'path':str(R/'GENUINE_PREPARATION_TOOLS.json'),'bytes':1184,'sha256':'7da6b5e80b2388f5dfa137f9f5dc43596b7a22d3e345f33fd2111f0c0768c79b'};verify(toolpin);tools=parse(toolpin['path'],False)
command='/opt/homebrew/bin/python3 -I -B '+str(W/'prepare_unissued.py')+' --root-decision '+decisionpin['path']+' --root-decision-sha256 '+decisionpin['sha256']
eq(tools['initial']['arguments']['cmd'],command,'exact genuine initial command');eq(tools['initial']['arguments']['workdir'],'/Volumes/AI_DATA/development/det_8_framework-ret','explicit outer cwd');require(tools['initial']['arguments']['login'] is False,'loginfalse')
eq([tools['initial']['result']['chunk_id'],tools['initial']['result']['session_id'],tools['initial']['result']['output'],tools['terminal']['chunk_id'],tools['terminal']['exit_code'],tools['terminal']['output']],['ba403e',49699,'','8b2cd4',0,''],'genuine one-shot completion')
lineage=parse(R/'PREPARATION_ROOT_LINEAGE.json');eq(lineage['decision'],decisionpin,'root lineage decision');eq(lineage['fresh_host'],decision['host_transcript'],'root lineage host');verify(lineage['interpreter'])
for row in lineage['stdlib_loaded']:verify(row)
verify(lineage['source_adjudication']);sourceaccept=parse(lineage['source_adjudication']['path']);require(sourceaccept.get('operational_authorization',False) is False,'source decision not operational')
# No giant log display. Save complete independently fresh input states separately.
current=[expected[p] for p in sorted(expected)]
body=canon({'schema':'ri255-independent-fresh-inputs-v1','identities':current,'scope':'Complete saved-domain opaque identity and selected metadata namespace review only.'})
with (Q/'FRESH_INPUTS.json').open('xb') as f:f.write(body)
require((Q/'FRESH_INPUTS.json').read_bytes()==body,'whole fresh report readback')
for n,r in output_states.items():eq(identity(D/n),r,'final regular output whole custody '+n)
result={'schema':'ri255-independent-mode-card-preparation-check-v1','status':'PASS_COMPLETE_UNISSUED_PREPARATION_RECONSTRUCTION','predicates':predicates,'input_domain':2920,'source_modules':11,'source_dependencies':567,'retained_old_roles':2811,'prior_operation_input_domain':2883,'vendor_files':1810,'vendor_bytes':48024515,'supplier_namespaces':195,'tools':4,'absences':2,'E_files':49,'E_directories':9,'role_counts':{'copies':48,'history':124,'target_originals':30},'request_fields':4,'wrapper_fields':7,'candidate_fields':12,'preflight_fields':15,'complete_fields':13,'tails':6,'prepared_artifacts_before_complete':8,'final_output_files':9,'empty_directories':2,'output_identities':[output_states[n] for n in sorted(output_states)],'source_handoff':decision['proposal_handoff'],'preparation_decision':decisionpin,'genuine_tool_record':toolpin,'genuine_host':decision['host_transcript'],'fresh_inputs':{'path':str(Q/'FRESH_INPUTS.json'),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()},'decoded_administrative_paths':sorted(set(decoded)),'limits':{'root_tool_origin_external_premise':True,'ordinary_administrative_interpreter_trusted':True,'selected_vendor_not_started':True,'no_scientific_body_decode':True,'no_writer_or_subject_reexecution':True,'mode_card_authority_absent':True,'prospective_operation_absent':True,'science_or_new_qualification_credit':0}}
out=canon(result)
with (Q/'CHECK.json').open('xb') as f:f.write(out)
require((Q/'CHECK.json').read_bytes()==out,'exact final result readback')
print(json.dumps({'passed':True,'predicates_saved':result['predicates'],'additional_check_readback':1,'fresh_inputs':result['fresh_inputs'],'CHECK':{'path':str(Q/'CHECK.json'),'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest()},'outputs':9,'tails':6,'input_domain':2920}))
