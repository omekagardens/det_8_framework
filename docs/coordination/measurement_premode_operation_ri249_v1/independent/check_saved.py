"""Independent administrative review of saved RI249 pre_mode operation; no subject imports."""
from pathlib import Path
import json,hashlib,os,stat,math,shlex
Q=Path(__file__).resolve().parent
B=Path('/Volumes/AI_DATA/development/det-review-evidence')
R=B/'ri249-root-premode-operation-hcybjv4k';D=B/'ri244-current-normal-premode-2kfsmiea'
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
P=B/'ri247-root-hook-branch-review-6fgw5qd9';S=B/'ri160-white-fixture-custody-repair-ufok1zpo';M=D/'monitor'
accept=load(P/'RI244_PREPARATION_ADJUDICATION.json',{'path':str(P/'RI244_PREPARATION_ADJUDICATION.json'),'bytes':3323,'sha256':'673689def36a4720a9f14d647147048fc150fc4a19fdfdc56a8816fdd87ee274'})
need(accept['status']=='ACCEPT_UNISSUED_PREPARATION_ONLY' and accept['operational_authorization'] is False,'accepted predecessor scope')
card=load(D/'ADMIT_PRE_MODE.json',{'path':str(D/'ADMIT_PRE_MODE.json'),'bytes':2126,'sha256':'b0608199b2d596e028588ee4718605f07d66738de2110d7f1dfa79a32e8ee0b2'})
wrapper=load(D/'ADMISSION_CANDIDATE.json');eq(card,wrapper['candidate'],'exact separately issued full candidate')
need(len(card)==12 and card['action']=='pre_mode' and card['status']=='AUTHORIZE_ONE_BOUNDED_METADATA_ACTION' and card['schema']=='ri156-root-adapter-admission-v1' and card['genuine_outer_required'] is True,'closed admitted operation')
eq(card['environment'],ENV,'exact10 operational environment');eq(card['bounds'],BOUNDS,'unchanged limits');eq(card['output'],str(O),'exact fresh output path')
source_review=load(R/'PREDISPATCH_SOURCE_REVIEW.json');need(source_review['status']=='ACCEPT_BOUNDED_ROOT_METADATA_PREFLIGHT_SOURCE','genuine predispatch source decision')
for k in ['source','archived_source','independent_review']:verify(source_review[k])
startup=load(R/'ADMINISTRATIVE_STARTUP.json');verify(startup['interpreter']);verify(startup['script'])
manifest=load(card['source_manifest']['path'],card['source_manifest']);need(len(manifest['modules'])==11 and len(manifest['dependencies'])==567,'source closure cardinalities')
allsource={**manifest['modules'],'adapter':manifest['adapter'],'manifest':card['source_manifest']};source_before={}
for name,row in allsource.items():
 got=verify(row);need(got['path']==got['resolved_path'] and got['symlink_chain']==[],'literal source');source_before[name]={k:got[k] for k in ['path','bytes','sha256','state']}
for row in manifest['dependencies']:verify(row)
verify(manifest['bootstrap_binding']);verify(manifest['bootstrap_provenance']);verify(card['source_review']);pre=load(card['bootstrap_preflight']['path'],card['bootstrap_preflight']);eq(pre['selected_interpreter_binding'],manifest['bootstrap_binding'],'whole selected vendor binding')
qual=load(card['qualification']['path'],card['qualification']);need(qual['status']=='ACCEPT_EXACT_INERT_ADAPTER_CONTROLS' and qual['all_passed'] is True and qual['scientific_execution'] is False and len(qual['controls'])==106,'accepted106 scope');eq(qual['source_manifest'],card['source_manifest'],'qualified exact manifest')
for k in ['report','genuine_outer','independent_review']:verify(qual[k])
req=load(card['request']['path'],card['request']);need(len(req)==5 and req['mode']=='normal','request5 normal');runtime=load(req['actual_runtime']['path'],req['actual_runtime']);need(len(runtime)==13 and runtime['phase']=='pre' and runtime['mode']=='normal','runtime13 normalpre')
freeze=verify(req['freeze']);eq(runtime['freeze'],{k:freeze[k] for k in ('bytes','sha256')},'whole opaque frozen identity')
snapshot=load(runtime['snapshot']['path'],runtime['snapshot']);baseline=load(req['baseline']['path'],req['baseline']);eq(snapshot,baseline,'whole accepted current/baseline metadata')
eq(runtime['baseline'],req['baseline'],'same baseline ref');eq(runtime['copy_observation'],req['copies'],'same copy ref');eq(runtime['environment']['TMPDIR'],str(E/'tmp'),'distinct runtime E/tmp')
need(snapshot['schema']=='ri133-complete-current-metadata-snapshot-v1','retained complete metadata shape')
eq(load(runtime['observed_dyld_routes']['path'],runtime['observed_dyld_routes']),snapshot['preobserved_dyld_routes'],'whole observed route sidecar')
eq(load(runtime['vendor_before']['path'],runtime['vendor_before']),load(runtime['vendor_after']['path'],runtime['vendor_after']),'whole stable vendor bracket')
verify(runtime['genuine_collection_tools']);copies=load(req['copies']['path'],req['copies'])
ra=load(runtime['runtime_acceptance']['path'],runtime['runtime_acceptance']);profiles=load(ra['profile_review']['path'],ra['profile_review'])
eq([profiles['schema'],profiles['status'],profiles['stage'],profiles['environment_root']],['ri133-root-preparation-stage-review-v1','ACCEPT_NONSCIENTIFIC_PREPARATION_EVIDENCE','profiles',str(E)],'accepted new-environment profile chain')
normal=load(profiles['completions']['profile_normal']['path'],profiles['completions']['profile_normal']);eq(normal['artifacts']['PRE'],req['baseline'],'authentic accepted normal PRE');eq(normal['environment'],runtime['environment'],'authentic runtime environment')
# Exact operation namespace and saved result, without reading the E freeze JSON.
eq(sorted(p.name for p in O.iterdir()),['ATTEMPT.json','COMPLETE.json','RESULT.json'],'three-file complete operation')
need(O.resolve()==O and O.is_dir() and not O.is_symlink(),'literal O')
for name in ['ATTEMPT.json','COMPLETE.json','RESULT.json']:
 p=O/name;s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and p.resolve()==p,'literal regular single-link '+name)
attempt=load(O/'ATTEMPT.json');result=load(O/'RESULT.json');complete=load(O/'COMPLETE.json')
expected_result={'schema':'ri130-root-pre-mode-runtime-custody-v1','mode':'normal','freeze':runtime['freeze'],'runtime_acceptance':runtime['runtime_acceptance'],'selection_unchanged':True,'optional_namespaces_unchanged':True,'host_identity_unchanged':True,'observed_dyld_routes':runtime['observed_dyld_routes'],'metadata_record':req['actual_runtime']}
need(len(expected_result)==9,'result9 literal');eq(result,expected_result,'whole nine result fields')
expected_attempt={'schema':'ri156-exclusive-metadata-attempt-v1','admission':ref(D/'ADMIT_PRE_MODE.json'),'action':'pre_mode','no_retry':True,'scientific_execution':False};eq(attempt,expected_attempt,'whole ATTEMPT')
artifacts={'attempt':ref(O/'ATTEMPT.json'),'result':ref(O/'RESULT.json')};produced={'ATTEMPT.json':artifacts['attempt'],'RESULT.json':artifacts['result']}
pre_tree=[{'relative':'.','kind':'directory'}]+[{'relative':n,'kind':'file',**{k:produced[n][k] for k in ('bytes','sha256')}} for n in sorted(produced)]
tails={'sources':{'value':source_before,'error':None},'admission':{'value':ref(D/'ADMIT_PRE_MODE.json'),'error':None},'request':{'value':card['request'],'error':None},'dependencies':{'value':manifest['dependencies'],'error':None},'output:ATTEMPT.json':{'value':produced['ATTEMPT.json'],'error':None},'output:RESULT.json':{'value':produced['RESULT.json'],'error':None},'namespace':{'value':pre_tree,'error':None}}
observations={'sources':source_before,'outputs':produced,'namespace':pre_tree,'namespace_member_mismatches':[],'namespace_output_mismatches':[],'namespace_fixture_mismatches':[]}
need(type(complete['elapsed_seconds_before_complete_write']) in (float,int) and math.isfinite(complete['elapsed_seconds_before_complete_write']) and 0<=complete['elapsed_seconds_before_complete_write']<=180,'bounded source-before-COMPLETE elapsed')
expected_complete={'schema':'ri156-adapter-completion-v1','action':'pre_mode','status':'COMPLETED_PENDING_INDEPENDENT_ROOT_REVIEW','admission':ref(D/'ADMIT_PRE_MODE.json'),'artifacts':artifacts,'first_error':None,'independent_tails':tails,'elapsed_seconds_before_complete_write':complete['elapsed_seconds_before_complete_write'],'authenticated_source_before':source_before,'produced_output_pins':produced,'tail_observations':observations,'scientific_execution':False,'root_acceptance_created':False,'ret_paused':True}
need(len(expected_complete)==14,'COMPLETE14 literal');eq(complete,expected_complete,'whole COMPLETE fourteen fields seven tails')
# Whole root preflight/issue/dispatch/postflight and independent live identity checks.
roots={n:load(R/(n+'.json')) for n in ['PREFLIGHT','ISSUE','DISPATCH','POSTFLIGHT']}
eq(ref(R/'POSTFLIGHT.json'),{'path':str(R/'POSTFLIGHT.json'),'bytes':1759691,'sha256':'79d2662a53da46dcb68f83df25e01563726f4942838b30bc023711a3cb742acc'},'root supplied postflight pin')
custody=load(D/'CUSTODY_BEFORE.json');need(len(custody['identities'])==2854,'retained immutable2854')
rootold=load(accept['root_check']['path'],accept['root_check']);prepared=rootold['outputs'];base_names=sorted([Path(r['path']).name for r in prepared]+['tmp','monitor']);all_D_names=sorted(base_names+['ADMIT_PRE_MODE.json','DISPATCH.json'])
allidentitymap={}
for phase,obj in roots.items():
 need(len(obj)==17 and obj['schema']=='ri249-whole-premode-custody-v1' and obj['phase']==phase.lower() and obj['status']=='PASS_METADATA_CUSTODY','root custody exact phase')
 eq(obj['prepared_outputs'],prepared,'complete preparation outputs preserved '+phase);need(obj['immutable_preparation_input_rows']==2854 and obj['E_files']==49 and obj['E_directories']==9 and obj['E_unchanged'] is True and obj['original_preparation_preserved'] is True and obj['subject_executed_by_this_script'] is False,'root retained whole scope '+phase)
 eq(obj['D_namespace'],base_names if phase=='PREFLIGHT' else all_D_names,'exact phase D membership')
 ids=obj['input_identities'];need(len(ids)==len({x['path'] for x in ids}),'no duplicate phase identity');mp={x['path']:x for x in ids}
 for row in custody['identities']:eq(mp.get(row['path']),row,'whole retained preparation row in '+phase)
 for row in ids:
  if row['path'] in allidentitymap:eq(row,allidentitymap[row['path']],'whole cross-phase identity '+row['path'])
  else:allidentitymap[row['path']]=row
 if phase=='PREFLIGHT':eq(obj['controls'],{},'no controls before issuance')
 else:eq(obj['controls'],roots['ISSUE']['controls'],'whole issued control states through postflight')
 eq(obj['supplier_reference'],ref(D/'SUPPLIER_BEFORE.json'),'supplier anchor');eq(obj['E_reference'],ref(D/'E_BEFORE.json'),'E anchor')
for row in allidentitymap.values():verify(row)
need(roots['PREFLIGHT']['observed_at_unix_ns']<=roots['ISSUE']['observed_at_unix_ns']<=roots['DISPATCH']['observed_at_unix_ns']<=roots['POSTFLIGHT']['observed_at_unix_ns'],'recorded preparation phase order')
for row in prepared:verify(row);need(row['state'][3]==1 and row['symlink_chain']==[] and row['path']==row['resolved_path'],'retained preparation regular single link')
for row in roots['ISSUE']['controls'].values():verify(row)
# Fresh supplier namespace, host bracket and entire E without E body decoding.
vendor=load(D/'SUPPLIER_BEFORE.json');etree=load(D/'E_BEFORE.json');need(len(vendor['vendor'])==1810 and len(vendor['namespace'])==195 and len(vendor['tools'])==4 and len(vendor['absent'])==2 and sum(r['bytes'] for r in vendor['vendor'])==48024515,'supplier1810/full finite scope')
for row in vendor['vendor']+vendor['tools']:verify(row)
for row in vendor['namespace']:
 p=Path(row['path']);s=p.lstat();v={'path':str(p),'kind':row['kind'],'state':state(s)}
 if row['kind']=='directory':need(stat.S_ISDIR(s.st_mode),'supplier directory kind');v['entries']=sorted(x.name for x in p.iterdir())
 else:need(row['kind']=='symlink' and stat.S_ISLNK(s.st_mode),'supplier link');v['target']=os.readlink(p)
 eq(state(p.lstat()),state(s),'supplier row stable');eq(v,row,'whole supplier namespace')
for p in vendor['absent']:need(not os.path.lexists(p),'supplier absence')
prehost=load(R/'GENUINE_PRE_HOST.json');posthost=load(R/'GENUINE_POST_HOST.json',{'path':str(R/'GENUINE_POST_HOST.json'),'bytes':1506,'sha256':'712cb72dbe3c27ec41ffe48ce7bf6c102714eb7a12e38e6e8736c84380aeb585'})
for h in [prehost,posthost]:
 eq(json.loads(h['result']['output']),h['observation'],'exact raw genuine host output');need(h['result']['exit_code']==0 and h['result'].get('session_id') is None,'host terminal');eq(h['observation']['uname'],list(os.uname()),'whole host uname');eq(h['arguments'],prehost['arguments'],'same benign host args')
eq(prehost['observation'],posthost['observation'],'whole host bracket');need(prehost['result']['chunk_id']!=posthost['result']['chunk_id'],'distinct actual host receipts')
eq(vendor['host'],{'argv':posthost['observation']['command'],'exit_code':posthost['observation']['returncode'],'stdout':posthost['observation']['stdout'],'stderr':posthost['observation']['stderr'],'uname':posthost['observation']['uname']},'supplier whole host stable')
for phase,obj in roots.items():eq(obj['host'],ref(R/('GENUINE_POST_HOST.json' if phase=='POSTFLIGHT' else 'GENUINE_PRE_HOST.json')),'correct phase host binding')
need(len(etree)==58 and sum(x['kind']=='file' for x in etree)==49 and sum(x['kind']=='directory' for x in etree)==9,'whole frozenE49/9')
for row in etree:
 p=E/row['relative'];s=p.lstat();need(not p.is_symlink() and p.resolve()==p,'literal E member');v={'relative':row['relative'],'kind':row['kind'],'state':state(s)}
 if row['kind']=='directory':need(stat.S_ISDIR(s.st_mode),'E directory kind');v['entries']=sorted(x.name for x in p.iterdir())
 else:need(row['kind']=='file' and stat.S_ISREG(s.st_mode),'E regular');v['identity']=verify(row['identity'])
 eq(v,row,'whole current E member');eq(state(p.lstat()),state(s),'E state stable')
for p in [E/'ADMIT_NORMAL.json',E/'ADMIT_OPTIMIZED.json']:need(not os.path.lexists(p),'no scientific mode authority')
for p in [E/'tmp',E/'runs/normal',E/'runs/optimized',D/'tmp']:eq(sorted(x.name for x in p.iterdir()),[],'empty untouched output '+str(p))
eq(sorted(x.name for x in Path(card['request']['path']).parent.iterdir()),['ACTUAL_RUNTIME_NORMAL.json','PRE_MODE_REQUEST.json'],'original input namespace')
# Genuine operation command/session/polls, exactly separated from root admin calls.
tool=load(R/'GENUINE_OPERATION_TOOLS.json',{'path':str(R/'GENUINE_OPERATION_TOOLS.json'),'bytes':3806,'sha256':'3f1d159344dc18dd669f4b2b91dc83b403314fdb55cbb207ea692426180f5965'})
op=tool['operation'];expected_vector=['/usr/bin/env','-i']+[k+'='+ENV[k] for k in sorted(ENV)]+['/usr/bin/perl','-e','$SIG{ALRM}="DEFAULT"; alarm 960; exec @ARGV; die $!;',manifest['bootstrap_binding']['path'],'-I','-B',str(D/'PRE_MODE_BOOTSTRAP.proposal.py')]
eq(shlex.split(op['arguments']['cmd']),expected_vector,'entire literal outer vector');eq(op['arguments']['cmd'],shlex.join(expected_vector),'exact literal shell command');need(op['arguments']['workdir']==str(D) and op['arguments']['login'] is False and op['arguments']['yield_time_ms']==1000 and op['arguments']['max_output_tokens']==2000,'actual cwd/tool flags')
need(op['result']['chunk_id']=='aa86d9' and op['result']['session_id']==78888 and op['result'].get('exit_code') is None and op['result']['output']=='','genuine initial result');need(len(op['polls'])==1,'all actual polls')
eq(op['polls'][0]['arguments'],{'session_id':78888,'chars':'','yield_time_ms':1000,'max_output_tokens':2000},'exact terminal arguments');fin=op['polls'][0]['result'];need(fin['chunk_id']=='cd41a9' and fin['exit_code']==0 and fin.get('session_id') is None and fin['output']=='','genuine terminal success')
dispatch=load(D/'DISPATCH.json');eq(dispatch,{'schema':'ri249-one-premode-dispatch-v1','admission':ref(D/'ADMIT_PRE_MODE.json'),'bootstrap':wrapper['bootstrap_proposal'],'preparation_acceptance':ref(P/'RI244_PREPARATION_ADJUDICATION.json'),'environment':ENV,'outer_cwd':str(D),'child_cwd':str(M),'label':'PRE_MODE','outer_alarm_seconds':960,'one_attempt':True,'scientific_execution':False},'whole actual dispatch')
need((D/'PRE_MODE_BOOTSTRAP.proposal.py').read_bytes()==(W/'PRE_MODE_BOOTSTRAP.proposal.txt').read_bytes(),'unchanged whole bootstrap source')
# RI141 actual record schema, complete raw ps correspondence and resource arithmetic.
mon=load(M/'PRE_MODE.COMPLETION.json');matt=load(M/'PRE_MODE.ATTEMPT.json');command=[manifest['bootstrap_binding']['path'],'-I','-B',str(S/'adapter.py'),'--admission',str(D/'ADMIT_PRE_MODE.json')]
eq(mon['command'],command,'whole monitored command');eq(mon['environment'],ENV,'whole monitor environment');need(mon['wall_seconds']==180,'monitor bound');need(type(matt['pid_owner']) is int and matt['pid_owner']>0,'actual parentPID recorded')
eq(matt,{'command':command,'environment':ENV,'wall_seconds':180,'pid_owner':matt['pid_owner'],'scientific_target_entry':False},'whole monitor ATTEMPT')
expected_mon_fields=['command','environment','wall_seconds','samples','monitor_attempts','peak_sampled_rss_kib','stop_reason','child_exit_code','first_error','tail_errors','elapsed_seconds','final_sample_to_reap_gap_seconds','final_sample_gap_passed','stdout','stderr','passed'];eq(sorted(mon),sorted(expected_mon_fields),'RI141 complete17 record shape')
need(mon['passed'] is True and mon['first_error'] is None and mon['stop_reason'] is None and mon['tail_errors']==[] and type(mon['child_exit_code']) is int and mon['child_exit_code']==0,'all owned monitor success gates')
duration=mon['elapsed_seconds'];need(type(duration) in (int,float) and math.isfinite(duration) and 0<=duration<=180,'actual child wall')
need(complete['elapsed_seconds_before_complete_write']<=duration,'inner interval within owned child elapsed')
raw=mon['monitor_attempts'];samples=mon['samples'];need(len(raw)==len(samples)==42,'actual42 attempts42samples no terminal malformed record')
previous=0.0;peak=0;maxgap=0
for i,(r,s) in enumerate(zip(raw,samples)):
 eq(sorted(r),['elapsed_seconds','returncode','stderr','stdout'],'whole raw ps shape');eq(sorted(s),['elapsed_seconds','gap_seconds','rss_kib'],'whole sample shape')
 need(type(r['returncode']) is int and r['returncode']==0 and type(r['stdout']) is str and r['stdout'].strip().isdigit() and r['stderr']=='','actual successful raw ps')
 t=r['elapsed_seconds'];need(type(t) in (int,float) and math.isfinite(t) and previous<=t<=duration,'ordered monitor timestamp')
 eq(s['elapsed_seconds'],t,'exact raw/sample timestamp');need(type(s['rss_kib']) is int and s['rss_kib']==int(r['stdout'].strip()) and 0<=s['rss_kib']<=524288,'exact bounded RSS')
 gap=t-previous;need(type(s['gap_seconds']) in (int,float) and math.isfinite(s['gap_seconds']) and abs(s['gap_seconds']-gap)<=8*math.ulp(max(abs(gap),abs(s['gap_seconds']),1.0)),'gap arithmetic');need(0<=s['gap_seconds']<=.1 and gap<=.1,'unchanged sample gap limit')
 previous=t;peak=max(peak,s['rss_kib']);maxgap=max(maxgap,gap)
gap=duration-previous;need(abs(mon['final_sample_to_reap_gap_seconds']-gap)<=8*math.ulp(max(abs(gap),1.0)) and 0<=gap<=.1 and 0<=mon['final_sample_to_reap_gap_seconds']<=.1 and mon['final_sample_gap_passed'] is True,'final reap arithmetic and bound')
need(type(mon['peak_sampled_rss_kib']) is int and mon['peak_sampled_rss_kib']==peak,'full peak arithmetic')
for label in ['stdout','stderr']:
 got=observe(M/('PRE_MODE.'+label));eq(mon[label],pure(got),'complete stream binding');need(got['bytes']==0 and got['state'][3]==1 and not got['symlink_chain'],'actual empty literal single-link stream')
eq(sorted(p.name for p in M.iterdir()),['PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stderr','PRE_MODE.stdout'],'exact four monitor artifacts')
eq(sorted(p.name for p in D.iterdir()),all_D_names,'final complete D namespace')
for folder,names in [(O,['ATTEMPT.json','COMPLETE.json','RESULT.json']),(M,['PRE_MODE.ATTEMPT.json','PRE_MODE.COMPLETION.json','PRE_MODE.stderr','PRE_MODE.stdout'])]:
 need(folder.resolve()==folder and not folder.is_symlink(),'literal output directory')
 for name in names:
  p=folder/name;s=p.lstat();need(stat.S_ISREG(s.st_mode) and s.st_nlink==1 and p.resolve()==p,'final literal regular single-link output');observe(p)
# Recheck all bound input/output file identities at the end; never a global freeze claim.
for row in list(observed.values()):verify(row)
b=canon({'schema':'ri249-independent-observations-v1','identities':list(observed.values())})
with (Q/'OBSERVATIONS.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
need((Q/'OBSERVATIONS.json').read_bytes()==b,'whole observation readback')
report={'schema':'ri249-independent-complete-premode-check-v1','status':'PASS_COMPLETE_PREMODE_METADATA_OUTCOME_ONLY','predicates':count,'distinct_fresh_identities':len(observed),'result_fields':9,'COMPLETE_fields':14,'complete_tails':7,'authenticated_source_rows':13,'dependency_rows':567,'immutable_preparation_inputs':2854,'root_phase_input_counts':{k:len(v['input_identities']) for k,v in roots.items()},'exact_card_fields':12,'observed_monitored_attempts':len(raw),'observed_samples':len(samples),'peak_sampled_rss_kib':peak,'child_elapsed_seconds':duration,'max_reconstructed_sample_gap_seconds':maxgap,'final_reconstructed_reap_gap_seconds':gap,'inner_elapsed_before_complete_write':complete['elapsed_seconds_before_complete_write'],'E_files':49,'E_directories':9,'supplier_files':1810,'supplier_namespace_rows':195,'supplier_tools':4,'supplier_absences':2,'exact_O_files':3,'exact_monitor_files':4,'D_files':10,'D_directories':2,'empty_streams':True,'result':ref(O/'RESULT.json'),'completion':ref(O/'COMPLETE.json'),'genuine_tools':ref(R/'GENUINE_OPERATION_TOOLS.json'),'postflight':ref(R/'POSTFLIGHT.json'),'observations':{'path':str(Q/'OBSERVATIONS.json'),**rawpin(b)},'subject_replay':False,'scientific_E_body_decoded':False,'genuine_origin_is_external_premise':True,'runtime_performance_or_scientific_qualification':False,'global_atomic_snapshot_claim':False}
b=canon(report)
with (Q/'CHECK.json').open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
assert (Q/'CHECK.json').read_bytes()==b
print(json.dumps({'predicates':count,'identities':len(observed),'report':{'path':str(Q/'CHECK.json'),**rawpin(b)},'monitored_seconds':duration,'peak_kib':peak,'raw_readback':True}))
